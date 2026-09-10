#!/usr/bin/env python3
"""Validate every package in this monorepo against the Hermes Agent rules.

The rules below are ported from the Hermes source (v0.21.1):

  * hermes_cli/profile_distribution.py   distribution.yaml schema, symlink ban,
                                          user-owned paths that must never ship
  * tools/skill_manager_tool.py           hard SKILL.md validator (frontmatter,
                                          name regex, size limits, allowed subdirs)
  * tools/skill_linter.py                 advisory linter (60-char description,
                                          metadata, When to Use, dangling refs,
                                          forbidden files, shell-utility prose)
  * tools/skills_guard.py                 structural limits (file count, sizes,
                                          binaries)
  * skills/AGENTS.md + CONTRIBUTING.md    authoring standards

Plus repo conventions of our own: no leftover Claude Code constructs, no
unported knowledge/ or resources/ paths, shared skills byte-identical to their
canonical copy under shared/skills/.

Usage:
    python3 tools/validate.py                 # all packages
    python3 tools/validate.py superforecaster # one package
    python3 tools/validate.py --selftest      # also run every script's selftest
    python3 tools/validate.py --hermes-src ~/.hermes/hermes-agent
                                              # additionally run the real Hermes linter

Exit status is non-zero when any ERROR is found. Warnings never fail the run.
Stdlib only, except PyYAML which Hermes itself requires.
"""
from __future__ import annotations

import argparse
import filecmp
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"
SHARED = ROOT / "shared" / "skills"

# ---- Hermes constants (verbatim values from the source) ---------------------
SKILL_PROMPT_DESC_LIMIT = 60          # agent/skill_utils.py
MAX_DESCRIPTION_LENGTH = 1024         # tools/skill_manager_tool.py
MAX_SKILL_CONTENT_CHARS = 100_000     # tools/skill_manager_tool.py
MAX_SKILL_FILE_BYTES = 1_048_576      # tools/skill_manager_tool.py
VALID_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")   # tools/skill_linter.py (stricter than manager)
ALLOWED_SUBDIRS = {"references", "templates", "scripts", "assets"}  # skill_manager_tool.py
MAX_FILE_COUNT, MAX_TOTAL_SIZE_KB, MAX_SINGLE_FILE_KB = 50, 5120, 256  # skills_guard.py
FORBIDDEN_SKILL_FILES = ("README.md", "CHANGELOG.md", "install.sh", ".env", ".env.example", ".gitignore")
MARKETING_WORDS = ("powerful", "comprehensive", "seamless", "advanced", "cutting-edge",
                   "state-of-the-art", "revolutionary", "robust")
SHELL_UTIL_TO_TOOL = {
    "grep": "search_files", "rg": "search_files", "cat": "read_file", "head": "read_file",
    "tail": "read_file", "sed": "patch", "awk": "patch",
    "find": "search_files (target='files')", "ls": "search_files (target='files')"}
POSIX_PRIMITIVES = ("fcntl", "termios", "os.setsid", "signal.SIGKILL", "osascript", "/proc/",
                    "apt-get", "systemctl")
SUSPICIOUS_BINARY_EXTENSIONS = {".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".pyo", ".o",
                                ".a", ".class", ".jar", ".war", ".msi", ".dmg", ".pkg", ".deb", ".rpm"}
USER_OWNED_EXCLUDE = frozenset({
    "auth.json", ".env", "state.db", "state.db-shm", "state.db-wal", "hermes_state.db",
    "response_store.db", "response_store.db-shm", "response_store.db-wal", "gateway.pid",
    "gateway_state.json", "processes.json", "auth.lock", "active_profile", ".update_check",
    "errors.log", ".hermes_history", "memories", "sessions", "logs", "plans", "workspace",
    "home", "image_cache", "audio_cache", "document_cache", "browser_screenshots",
    "checkpoints", "sandboxes", "backups", "cache", "hermes-agent", ".worktrees", "profiles",
    "bin", "node_modules", "local"})
RESERVED_PROFILE_NAMES = {"hermes", "test", "tmp", "root", "sudo", "default"}

# ---- Repo conventions -------------------------------------------------------
# Claude Code constructs that must not survive conversion (checked in prose, not code fences).
CLAUDE_ISMS = [
    (r"\bAskUserQuestion\b", "use the `clarify` tool"),
    (r"\bWebFetch\b", "use `web_extract`"),
    (r"\bWebSearch\b", "use `web_search`"),
    (r"\bTodoWrite\b", "use `todo_list`"),
    (r"`todo`", "the Hermes tool is `todo_list` (`todo` is the toolset name)"),
    (r"\bSkill tool\b", "use `skill_view`"),
    (r"\bTask tool\b", "use `delegate_task`"),
    (r"\bAgent tool\b", "use `delegate_task`"),
    (r"\bsubagent_type\b", "use `delegate_task`"),
    (r"`Read`\s+tool|\bthe Read tool\b", "use `read_file`"),
    (r"`Write`\s+tool|\bthe Write tool\b", "use `write_file`"),
    (r"`Bash`\s+tool|\bthe Bash tool\b", "use `terminal`"),
    (r"\bCLAUDE_PLUGIN_ROOT\b", "no plugin root in Hermes"),
    (r"~/\.claude\b|\.claude/", "no Claude home paths"),
    (r"\bclaude-in-chrome\b|\bmcp__", "no Claude MCP tool names"),
    (r"\$ARGUMENTS\b", "no slash-command arguments"),
]
UNPORTED_PATHS = [
    (r"(?<![\w/])(?:\./)?knowledge/[\w./-]+", "unported knowledge/ path; bundle it under references/"),
    (r"(?<![\w/])(?:\./)?resources/[\w./-]+", "Claude layout leftover; use scripts/ references/ templates/ assets/"),
    (r"\.\./[\w-]+/resources/", "cross-skill path still points at resources/"),
]

MACHINE_LOCAL_RE = re.compile(r"/Users/[A-Za-z]|/home/[a-z][a-z0-9_-]*/|C:\\\\Users\\\\")
CROSS_SKILL_VIEW_RE = re.compile(
    r"skill_view\(\s*[\"']([a-z0-9][a-z0-9_.-]*)[\"']\s*,\s*(?:file_path\s*=\s*)?[\"']"
    r"((?:\./)?(?:references|templates|assets|scripts)/[\w./-]+)[\"']")
FENCE_RE = re.compile(r"```.*?```", re.S)
FRONTMATTER_END_RE = re.compile(r"\n---\s*\n")


@dataclass
class Finding:
    severity: str  # ERROR | WARN | INFO
    where: str
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity:5} {self.where}: [{self.rule}] {self.message}"


class Report:
    def __init__(self) -> None:
        self.findings: List[Finding] = []

    def err(self, where, rule, msg): self.findings.append(Finding("ERROR", where, rule, msg))
    def warn(self, where, rule, msg): self.findings.append(Finding("WARN", where, rule, msg))
    def info(self, where, rule, msg): self.findings.append(Finding("INFO", where, rule, msg))

    @property
    def errors(self) -> int:
        return sum(1 for f in self.findings if f.severity == "ERROR")

    @property
    def warnings(self) -> int:
        return sum(1 for f in self.findings if f.severity == "WARN")


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def parse_frontmatter(content: str):
    """Mirror of agent/skill_utils.parse_frontmatter (BOM strip, fence search)."""
    content = content.removeprefix("﻿")
    end = FRONTMATTER_END_RE.search(content[3:]) if content.startswith("---") else None
    if not end:
        return None, content
    raw = content[3: end.start() + 3]
    body = content[end.end() + 3:]
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return {"__yaml_error__": str(exc)}, body
    return (parsed if isinstance(parsed, dict) else {"__not_mapping__": True}), body


def strip_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`\n]*`", "", text)


# ---- Skill checks -----------------------------------------------------------

def check_skill(skill_dir: Path, rep: Report) -> None:
    where = rel(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        rep.err(where, "missing-skill-md", "directory under skills/<category>/ has no SKILL.md")
        return
    content = skill_md.read_text(encoding="utf-8", errors="replace")
    if not content.strip():
        rep.err(where, "empty", "SKILL.md is empty")
        return
    if not content.lstrip("﻿").startswith("---"):
        rep.err(where, "frontmatter", "SKILL.md must start with YAML frontmatter (---)")
        return
    fm, body = parse_frontmatter(content)
    if fm is None:
        rep.err(where, "frontmatter", "frontmatter is not closed with a '---' line")
        return
    if "__yaml_error__" in fm:
        rep.err(where, "frontmatter", f"YAML parse error: {fm['__yaml_error__']}")
        return
    if "__not_mapping__" in fm:
        rep.err(where, "frontmatter", "frontmatter must be a YAML mapping")
        return

    # Hard validator (skill_manager_tool._validate_frontmatter)
    for field in ("name", "description"):
        if field not in fm:
            rep.err(where, "frontmatter", f"missing required field '{field}'")
    name = str(fm.get("name", "")).strip()
    desc = str(fm.get("description", "")).strip().strip("'\"")
    if name and not VALID_NAME_RE.fullmatch(name):
        rep.err(where, "name-format", f"name '{name}' must be lowercase letters, digits, hyphens, underscores")
    if name and name != skill_dir.name:
        rep.err(where, "name-dir-mismatch", f"frontmatter name '{name}' != directory '{skill_dir.name}'")
    if len(desc) > MAX_DESCRIPTION_LENGTH:
        rep.err(where, "description-length", f"description exceeds {MAX_DESCRIPTION_LENGTH} chars")
    if len(desc) > SKILL_PROMPT_DESC_LIMIT:
        rep.err(where, "description-length",
                f"description is {len(desc)} chars; Hermes truncates the skill index past "
                f"{SKILL_PROMPT_DESC_LIMIT} — one sentence, trigger first")
    if desc and not desc.endswith("."):
        rep.err(where, "description-period", "description must be one sentence ending with a period")
    if desc and name and name.replace("-", " ") in desc.lower():
        rep.warn(where, "description-repeats-name", "description repeats the skill name")
    hits = [w for w in MARKETING_WORDS if re.search(rf"\b{re.escape(w)}\b", desc.lower())]
    if hits:
        rep.err(where, "description-marketing", f"marketing words in description: {hits}")
    if not body.strip():
        rep.err(where, "empty-body", "SKILL.md has no content after the frontmatter")
    if len(content) > MAX_SKILL_CONTENT_CHARS:
        rep.err(where, "content-size", f"SKILL.md is {len(content):,} chars (limit {MAX_SKILL_CONTENT_CHARS:,})")

    # Advisory linter (skill_linter.py) — we treat metadata gaps as errors in this repo.
    for key in ("version", "author", "license", "platforms"):
        if key not in fm:
            rep.err(where, "missing-metadata", f"frontmatter is missing '{key}' (Hermes CI requires it)")
    meta = fm.get("metadata")
    hermes_meta = meta.get("hermes") if isinstance(meta, dict) else None
    if not isinstance(hermes_meta, dict):
        rep.err(where, "missing-metadata", "frontmatter is missing metadata.hermes")
    else:
        if not isinstance(hermes_meta.get("tags"), list) or not hermes_meta.get("tags"):
            rep.err(where, "missing-metadata", "metadata.hermes.tags must be a non-empty list")
        if "related_skills" not in hermes_meta or not isinstance(hermes_meta.get("related_skills"), list):
            rep.err(where, "missing-metadata", "metadata.hermes.related_skills must be a list (may be empty)")
        for rs in hermes_meta.get("related_skills") or []:
            if not _skill_exists_in_package(skill_dir, str(rs)):
                rep.err(where, "related-skill-missing", f"related_skills entry '{rs}' is not a skill in this package")
        if "category" in hermes_meta and hermes_meta["category"] != skill_dir.parent.name:
            rep.err(where, "category-mismatch",
                    f"metadata.hermes.category '{hermes_meta['category']}' != folder '{skill_dir.parent.name}'")
    platforms = fm.get("platforms")
    if platforms:
        valid = {"linux", "macos", "windows", "darwin"}
        items = platforms if isinstance(platforms, list) else [platforms]
        bad = [p for p in items if str(p).lower() not in valid]
        if bad:
            rep.err(where, "platforms-value", f"unrecognized platforms {bad}; expected subset of {sorted(valid)}")
    for claude_key in ("allowed-tools", "argument-hint", "disable-model-invocation", "user-invocable", "context"):
        if claude_key in fm:
            rep.err(where, "claude-frontmatter", f"Claude Code frontmatter key '{claude_key}' must be removed")

    # Body conventions
    if not re.search(r"^#+\s+When to [Uu]se", body, re.M):
        rep.err(where, "missing-section", "no '## When to Use' section")
    prose = strip_fences(body)
    for util, tool in SHELL_UTIL_TO_TOOL.items():
        if re.search(rf"`{re.escape(util)}`", prose):
            rep.warn(where, "shell-utility-reference", f"prose names `{util}`; say `{tool}` instead")
    prose_no_code = strip_inline_code(prose)
    for pattern, fix in CLAUDE_ISMS:
        if re.search(pattern, prose_no_code):
            rep.err(where, "claude-ism", f"'{pattern}' found in prose — {fix}")
    for pattern, fix in UNPORTED_PATHS:
        m = re.search(pattern, body)
        if m:
            rep.err(where, "unported-path", f"'{m.group(0)}' — {fix}")
    m = MACHINE_LOCAL_RE.search(body)
    if m:
        rep.err(where, "machine-local-path", f"'{m.group(0)}' is a machine-local path")
    # Cross-skill loads: skill_view("<other-skill>", file_path="references/x.md") must resolve
    # inside THAT skill (same package or shared/). Their paths are exempt from the local check.
    cross_paths = set()
    for m in CROSS_SKILL_VIEW_RE.finditer(body):
        other, ref = m.group(1), m.group(2).lstrip("./")
        cross_paths.add(m.group(2))
        if other == name:
            continue
        other_dir = _find_skill_dir(skill_dir, other)
        if other_dir is None:
            rep.err(where, "cross-skill-missing", f"skill_view(\"{other}\", ...) names a skill not in this package")
        elif not (other_dir / ref).exists():
            rep.err(where, "cross-skill-dangling", f"'{other}' has no '{ref}'")
    if re.search(r"file_path\s*=\s*[\"']\./", body):
        rep.warn(where, "reference-spelling", "use file_path=\"references/x.md\" (no leading ./)")
    # Dangling references (references/, templates/, assets/ are skill-owned; scripts/ too in this repo)
    seen = set()
    for m in re.finditer(r"(?<![\w/])(references|templates|assets|scripts)/[\w./-]+", body):
        ref = m.group(0).rstrip(".,;:)")
        if ref in seen or "*" in ref or ref.endswith("/") or "<" in ref or ref in cross_paths:
            continue
        seen.add(ref)
        if not (skill_dir / ref).exists():
            rep.err(where, "dangling-reference", f"body references '{ref}' but it does not exist")
    # ${HERMES_SKILL_DIR} usage sanity: every scripts/ invocation should be absolute via the token
    for m in re.finditer(r"python3?\s+(?!\$\{HERMES_SKILL_DIR\}|<skills>)(\S*scripts/\S+\.py)", body):
        rep.warn(where, "relative-script-path",
                 f"'{m.group(1)}' — prefer ${{HERMES_SKILL_DIR}}/scripts/... so it resolves from any cwd")

    # Files & structure
    for fname in FORBIDDEN_SKILL_FILES:
        if (skill_dir / fname).exists():
            rep.err(where, "forbidden-file", f"skill ships '{fname}'")
    for child in skill_dir.iterdir():
        if child.name == ".DS_Store":
            rep.err(where, "junk-file", ".DS_Store inside skill")
        if child.is_dir() and child.name not in ALLOWED_SUBDIRS:
            rep.err(where, "subdir", f"'{child.name}/' is not one of {sorted(ALLOWED_SUBDIRS)}")
    file_count = total = 0
    for f in skill_dir.rglob("*"):
        if f.is_symlink():
            rep.err(where, "symlink", f"symlink inside skill: {rel(f)}")
            continue
        if not f.is_file():
            continue
        file_count += 1
        size = f.stat().st_size
        total += size
        if size > MAX_SKILL_FILE_BYTES:
            rep.err(where, "oversized-file", f"{rel(f)} is {size // 1024}KB (hard limit 1 MiB)")
        elif size > MAX_SINGLE_FILE_KB * 1024:
            rep.warn(where, "oversized-file", f"{rel(f)} is {size // 1024}KB (guard limit {MAX_SINGLE_FILE_KB}KB)")
        if f.suffix.lower() in SUSPICIOUS_BINARY_EXTENSIONS:
            rep.err(where, "binary-file", f"binary file {rel(f)}")
        if f.suffix in (".py", ".sh", ".bash") and not platforms:
            text = f.read_text(encoding="utf-8", errors="ignore")
            hit = [p for p in POSIX_PRIMITIVES if p in text]
            if hit:
                rep.err(where, "platforms-gating", f"{f.name} uses POSIX-only {hit}; declare platforms: or fix")
    if file_count > MAX_FILE_COUNT:
        rep.warn(where, "too-many-files", f"{file_count} files (guard limit {MAX_FILE_COUNT})")
    if total > MAX_TOTAL_SIZE_KB * 1024:
        rep.info(where, "oversized-skill", f"{total // 1024}KB total (guard informational limit {MAX_TOTAL_SIZE_KB}KB)")
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        n = sum(1 for p in refs_dir.rglob("*.md") if not any(part.startswith("_") for part in p.parts))
        if n > 60:
            rep.warn(where, "references-sprawl", f"{n} reference files (linter limit 60)")


def _find_skill_dir(skill_dir: Path, name: str) -> Optional[Path]:
    """Locate another skill by name in the same package's skills tree, else in shared/."""
    skills_root = skill_dir.parent.parent
    if skills_root.name != "skills":
        skills_root = skill_dir.parent
    for p in skills_root.rglob(name):
        if p.is_dir() and (p / "SKILL.md").is_file():
            return p
    cand = SHARED / name
    return cand if (cand / "SKILL.md").is_file() else None


def _skill_exists_in_package(skill_dir: Path, name: str) -> bool:
    """related_skills must resolve to a skill shipped in the same package (or shared/)."""
    skills_root = skill_dir.parent.parent  # <pkg>/skills or shared/skills
    if skills_root.name != "skills":
        skills_root = skill_dir.parent
    if any(p.name == name and (p / "SKILL.md").is_file() for p in skills_root.rglob(name)):
        return True
    return (SHARED / name / "SKILL.md").is_file()


def run_selftests(skill_dir: Path, rep: Report) -> None:
    scripts = skill_dir / "scripts"
    if not scripts.is_dir():
        return
    for script in sorted(scripts.glob("*.py")):
        text = script.read_text(encoding="utf-8", errors="ignore")
        if '"selftest"' not in text and "'selftest'" not in text:
            continue
        proc = subprocess.run([sys.executable, str(script), "selftest"], capture_output=True, text=True,
                              timeout=600, cwd=str(skill_dir))
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout).strip().splitlines()[-3:]
            rep.err(rel(script), "selftest", f"exit {proc.returncode}: {' | '.join(tail)}")
        else:
            rep.info(rel(script), "selftest", "passed")


# ---- Package checks ---------------------------------------------------------

def check_text_file_conventions(path: Path, rep: Report) -> None:
    """SOUL.md / README.md inside a package: no Claude-isms, no unported paths."""
    where = rel(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    prose = strip_inline_code(strip_fences(text))
    for pattern, fix in CLAUDE_ISMS:
        if re.search(pattern, prose):
            rep.err(where, "claude-ism", f"'{pattern}' — {fix}")
    for pattern, fix in UNPORTED_PATHS:
        m = re.search(pattern, text)
        if m:
            rep.err(where, "unported-path", f"'{m.group(0)}' — {fix}")


def check_shared_sync(pkg: Path, rep: Report) -> None:
    manifest = pkg / "shared-skills.txt"
    if not manifest.is_file():
        return
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        category, _, skill = line.partition("/")
        if not skill:
            rep.err(rel(manifest), "shared-manifest", f"entry '{line}' must be '<category>/<skill>'")
            continue
        src = SHARED / skill
        dst = pkg / "skills" / category / skill
        if not src.is_dir():
            rep.err(rel(manifest), "shared-missing", f"shared/skills/{skill} does not exist")
            continue
        if not dst.is_dir():
            rep.err(rel(manifest), "shared-unsynced", f"{rel(dst)} missing — run tools/sync_shared.py")
            continue
        cmp = filecmp.dircmp(src, dst, ignore=[".DS_Store"])
        diffs = _dircmp_diffs(cmp)
        if diffs:
            rep.err(rel(dst), "shared-drift", f"differs from shared/skills/{skill}: {diffs[:5]} — run tools/sync_shared.py")


def _dircmp_diffs(cmp: filecmp.dircmp) -> List[str]:
    out = list(cmp.left_only) + list(cmp.right_only) + list(cmp.diff_files) + list(cmp.funny_files)
    for sub in cmp.subdirs.values():
        out.extend(_dircmp_diffs(sub))
    return out


def check_package(pkg: Path, rep: Report, selftest: bool) -> None:
    where = rel(pkg)
    manifest = pkg / "distribution.yaml"
    if not manifest.is_file():
        rep.err(where, "manifest", "distribution.yaml missing at package root")
        return
    try:
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        rep.err(where, "manifest", f"distribution.yaml YAML error: {exc}")
        return
    if not isinstance(data, dict):
        rep.err(where, "manifest", "distribution.yaml must be a mapping")
        return
    name = str(data.get("name", "")).strip()
    if not name:
        rep.err(where, "manifest", "distribution.yaml missing 'name'")
    elif name != pkg.name:
        rep.err(where, "manifest", f"name '{name}' != package directory '{pkg.name}'")
    if name.lower() in RESERVED_PROFILE_NAMES:
        rep.err(where, "manifest", f"'{name}' is a reserved profile name")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name):
        rep.err(where, "manifest", f"name '{name}' should be lowercase letters, digits, hyphens")
    version = str(data.get("version", "")).strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        rep.err(where, "manifest", f"version '{version}' is not MAJOR.MINOR.PATCH")
    for key in ("description", "author", "license"):
        if not data.get(key):
            rep.warn(where, "manifest", f"distribution.yaml has no '{key}'")
    env = data.get("env_requires") or []
    if not isinstance(env, list):
        rep.err(where, "manifest", "env_requires must be a list")
    else:
        for e in env:
            if not isinstance(e, dict) or not e.get("name"):
                rep.err(where, "manifest", f"env_requires entry needs a 'name': {e!r}")
    owned = data.get("distribution_owned")
    if owned is not None and not isinstance(owned, list):
        rep.err(where, "manifest", "distribution_owned must be a list")
    for key in ("source", "installed_at"):
        if data.get(key):
            rep.err(where, "manifest", f"'{key}' is written by the installer; do not ship it")

    soul = pkg / "SOUL.md"
    if not soul.is_file() or not soul.read_text(encoding="utf-8").strip():
        rep.err(where, "soul", "SOUL.md missing or empty")
    else:
        check_text_file_conventions(soul, rep)
        n = len(soul.read_text(encoding="utf-8"))
        # Hermes cuts context files (SOUL.md included) above `context_file_max_chars`, or above
        # 20,000 chars when that key is unset and the model's window is unknown: head and tail
        # are kept, the middle is dropped, silently. Every package here pins the cap.
        cap = None
        cfg_for_cap = pkg / "config.yaml"
        if cfg_for_cap.is_file():
            try:
                cap = (yaml.safe_load(cfg_for_cap.read_text(encoding="utf-8")) or {}).get("context_file_max_chars")
            except yaml.YAMLError:
                cap = None
        limit = cap if isinstance(cap, int) and cap > 0 else 20_000
        if n > limit:
            rep.err(where, "soul-size", f"SOUL.md is {n:,} chars; Hermes would cut it above {limit:,} "
                    + ("(context_file_max_chars)" if cap else "(no context_file_max_chars in config.yaml)"))
        elif n > 60_000:
            rep.warn(where, "soul-size", f"SOUL.md is {n:,} chars; it is injected into every system prompt")
    cfg = pkg / "config.yaml"
    if cfg.is_file():
        try:
            parsed = yaml.safe_load(cfg.read_text(encoding="utf-8"))
            if parsed is not None and not isinstance(parsed, dict):
                rep.err(where, "config", "config.yaml must be a mapping")
        except yaml.YAMLError as exc:
            rep.err(where, "config", f"config.yaml YAML error: {exc}")
    else:
        rep.warn(where, "config", "no config.yaml (installer will fall back to defaults)")
    readme = pkg / "README.md"
    if readme.is_file():
        check_text_file_conventions(readme, rep)
    else:
        rep.warn(where, "readme", "no README.md at package root")

    # Symlinks are rejected by the installer anywhere in the tree.
    for p in pkg.rglob("*"):
        if p.is_symlink():
            rep.err(where, "symlink", f"symlink in distribution: {rel(p)}")
    for child in pkg.iterdir():
        if child.name in USER_OWNED_EXCLUDE:
            rep.err(where, "user-owned", f"'{child.name}' is user-owned runtime state and must not ship")
        if child.name == ".DS_Store":
            rep.err(where, "junk-file", ".DS_Store in package root")

    skills_root = pkg / "skills"
    if not skills_root.is_dir():
        rep.err(where, "skills", "no skills/ directory")
        return
    for category in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        if category.name.startswith(".") or category.name == "_org":
            rep.err(where, "category", f"'{category.name}' would be skipped or token-gated by Hermes")
            continue
        if (category / "SKILL.md").exists():
            rep.err(where, "layout", f"'{rel(category)}' is a bare skill; skills must live under skills/<category>/<skill>/")
            continue
        desc = category / "DESCRIPTION.md"
        if not desc.is_file():
            rep.err(where, "category", f"skills/{category.name}/ has no DESCRIPTION.md")
        else:
            fm, _ = parse_frontmatter(desc.read_text(encoding="utf-8"))
            if not fm or not fm.get("description"):
                rep.err(where, "category", f"skills/{category.name}/DESCRIPTION.md needs frontmatter with 'description'")
        for skill_dir in sorted(p for p in category.iterdir() if p.is_dir()):
            check_skill(skill_dir, rep)
            if selftest:
                run_selftests(skill_dir, rep)
        for stray in category.iterdir():
            if stray.is_file() and stray.name not in ("DESCRIPTION.md",):
                rep.err(where, "category", f"stray file {rel(stray)} in category folder")
    check_shared_sync(pkg, rep)


def run_hermes_linter(hermes_src: Path, rep: Report, packages: List[Path]) -> None:
    """Run the real Hermes skill_linter against every SKILL.md (advisory)."""
    sys.path.insert(0, str(hermes_src))
    try:
        from tools.skill_linter import lint_skill  # type: ignore
    except Exception as exc:  # pragma: no cover
        rep.warn("hermes-linter", "import", f"could not import Hermes linter from {hermes_src}: {exc}")
        return
    for pkg in packages:
        for skill_md in (pkg / "skills").rglob("SKILL.md"):
            for f in lint_skill(skill_md):
                sev = "ERROR" if f.severity == "error" else "WARN"
                rep.findings.append(Finding(sev, rel(skill_md.parent), f"hermes:{f.rule}", f.message))


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packages", nargs="*", help="package names (default: all)")
    ap.add_argument("--selftest", action="store_true", help="run every script that supports 'selftest'")
    ap.add_argument("--hermes-src", type=Path, help="path to a hermes-agent checkout to run its linter too")
    ap.add_argument("--quiet", action="store_true", help="only print the summary and errors")
    args = ap.parse_args(argv)

    if args.packages:
        pkgs = [PACKAGES / p for p in args.packages]
    else:
        pkgs = sorted(p for p in PACKAGES.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))
    rep = Report()
    for pkg in pkgs:
        if not pkg.is_dir():
            rep.err(rel(pkg), "package", "no such package")
            continue
        check_package(pkg, rep, selftest=args.selftest)
    if args.hermes_src:
        run_hermes_linter(args.hermes_src.expanduser(), rep, [p for p in pkgs if p.is_dir()])

    for f in rep.findings:
        if args.quiet and f.severity != "ERROR":
            continue
        print(f)
    n_skills = sum(1 for p in pkgs if p.is_dir() for _ in (p / "skills").rglob("SKILL.md"))
    print(f"\n{len(pkgs)} package(s), {n_skills} skill(s): {rep.errors} error(s), {rep.warnings} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
