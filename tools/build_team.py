#!/usr/bin/env python3
"""Generate the Bot-team packages for a team manifest under teams/.

A team is one Hermes profile per agent, coordinated through Bot Chat teammate
messages (`message_agent`). The canonical sources live once under
teams/<team>/skills/: the stage briefs in valuation-specialists/ and the finance
skills in corporate-finance/. This script turns them into installable member
packages, so improving a brief or a skill regenerates every member that uses it.

For every member in teams/<team>/team.yaml it writes packages/<member>/ with:

    distribution.yaml   manifest; description = the roster line teammates see
    SOUL.md             team preamble + the brief body (from "## Role" onward)
    config.yaml         model + reasoning effort by tier from the manifest, cheap auxiliary model
    bot.yaml            title, tier, description — read by tools/install.sh to
                        write the profile's profile.yaml (Bot metadata) once
    README.md, .gitignore, .no-bundled-skills, shared-skills.txt
    skills/             the member's brief + its finance skills + dependency
                        closure (cross-skill loads and sibling scripts), with
                        related_skills pruned to what is bundled

The orchestrator package keeps a hand-written SOUL.md and README.md; only its
generated files and skills/ are (re)written.

Usage:
    python3 tools/build_team.py [valuation]        # (re)generate
    python3 tools/build_team.py --check            # exit 1 if generated files drifted
"""
from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"
SHARED = ROOT / "shared" / "skills"
# Canonical sources for the team being built: teams/<team>/skills/<category>/<skill>.
# Set by build() from the manifest's location.
SUITE = ROOT / "teams" / "valuation" / "skills"
FINANCE = SUITE / "corporate-finance"
BRIEFS = SUITE / "valuation-specialists"


def _set_sources(team_dir: Path) -> None:
    global SUITE, FINANCE, BRIEFS
    SUITE = team_dir / "skills"
    FINANCE = SUITE / "corporate-finance"
    BRIEFS = SUITE / "valuation-specialists"

# Where each bundled skill comes from and which category folder it lands in.
def _source_for(name: str) -> tuple[Path, str] | None:
    if (FINANCE / name / "SKILL.md").is_file():
        return FINANCE / name, "corporate-finance"
    if (BRIEFS / name / "SKILL.md").is_file():
        return BRIEFS / name, "valuation-specialists"
    if (SHARED / name / "SKILL.md").is_file():
        return SHARED / name, "writing"
    return None


SKILL_VIEW_RE = re.compile(r'skill_view\(\s*["\']([a-z0-9][a-z0-9_-]*)["\']')
SIBLING_RE = re.compile(r"\$\{HERMES_SKILL_DIR\}/\.\./([a-z0-9][a-z0-9_-]*)")
ENGINE_NAMES = ("dcf-valuation-engine", "cost-of-capital-toolkit", "valuation-consistency-checks")
FRONTMATTER_END_RE = re.compile(r"\n---\s*\n")
GITIGNORE = (PACKAGES / "superforecaster" / ".gitignore").read_text(encoding="utf-8")
NO_BUNDLED = (PACKAGES / "superforecaster" / ".no-bundled-skills").read_text(encoding="utf-8")


def _deps_of(skill_dir: Path) -> set[str]:
    """Skills a skill needs beside it: cross-skill skill_view loads, sibling script paths,
    and engines imported by its scripts."""
    deps: set[str] = set()
    md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    deps.update(SKILL_VIEW_RE.findall(md))
    deps.update(SIBLING_RE.findall(md))
    for py in (skill_dir / "scripts").glob("*.py") if (skill_dir / "scripts").is_dir() else []:
        text = py.read_text(encoding="utf-8", errors="ignore")
        deps.update(n for n in ENGINE_NAMES if n in text)
    deps.discard(skill_dir.name)
    return {d for d in deps if _source_for(d) is not None}


def _closure(names: list[str], own_brief: str | None, log: list[str]) -> list[str]:
    bundle = set(names)
    if own_brief:
        bundle.add(own_brief)
    changed = True
    while changed:
        changed = False
        for name in sorted(bundle):
            src, _ = _source_for(name)
            for dep in _deps_of(src):
                if dep not in bundle:
                    bundle.add(dep)
                    log.append(f"    + {dep} (needed by {name})")
                    changed = True
    return sorted(bundle)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    end = FRONTMATTER_END_RE.search(text[3:])
    fm = yaml.safe_load(text[3: end.start() + 3]) or {}
    return fm, text[end.end() + 3:]


def _copy_skill(src: Path, dst: Path, bundle: set[str]) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    if src.parent == SHARED:
        return  # shared copies stay byte-identical; their related_skills resolve against shared/
    md = dst / "SKILL.md"
    text = md.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    hermes = (fm.get("metadata") or {}).get("hermes") or {}
    related = [r for r in (hermes.get("related_skills") or []) if r in bundle]
    if related != (hermes.get("related_skills") or []):
        # Rewrite only the related_skills line; keep the rest of the frontmatter byte-identical.
        text = re.sub(r"^(\s+related_skills:).*$",
                      lambda m: f"{m.group(1)} [{', '.join(related)}]", text, count=1, flags=re.M)
        md.write_text(text, encoding="utf-8")


def _brief_body(brief_dir: Path) -> str:
    """Everything from '## Role' onward: the H1 and the orchestration-only 'When to Use'
    section are replaced by the team preamble."""
    _, body = _split_frontmatter((brief_dir / "SKILL.md").read_text(encoding="utf-8"))
    m = re.search(r"^## Role\b", body, re.M)
    if not m:
        raise SystemExit(f"{brief_dir.name}: brief has no '## Role' section")
    return body[m.start():].rstrip() + "\n"


def _member_soul(member: dict, team: dict, bundled: list[str]) -> str:
    name, title = member["name"], member["title"]
    orch = team["orchestrator"]["name"]
    finance = [s for s in bundled if s not in (name, "readability-check")]
    pre = f"""<!-- Generated by tools/build_team.py from teams/valuation/skills/valuation-specialists/{name}/SKILL.md.
     Edit that brief and rebuild; do not edit this file. -->
# {title}

You are the {title.lower()} of the valuation team: one of fifteen Hermes Bots that together
run a company analysis. The orchestrator, `{orch}`, owns the mandate, the workspace and the
conversation with the user. You own one stage. {member['description'].strip()}

## How work reaches you

- A job arrives as a message from `{orch}` (prefixed "Message from 🤖 {orch}"). It
  carries the goal for this stage, the absolute paths to read and what each holds, the
  absolute paths to write and the contract each must satisfy, the binding constraints from
  `classification.json`, and the mandate currency and valuation date. If any of these is
  missing, do not guess: return `needs_input` naming what is missing.
- Your final answer is delivered back to `{orch}` automatically when your turn ends. Only
  the last 2,000 characters of it reach the orchestrator, so keep the whole answer under
  1,500 characters and end it with the status line described under "Return" below. Hermes
  adds its own `session_id:` line after your answer; that is expected.
- Your prompt also carries a Hermes section that says to reply through `message_agent`. For
  a job from the orchestrator, do not: the answer travels back on its own, and a message
  would deliver it twice. Use `message_agent` only when you have something for a teammate
  that is not your job's answer. Do not wait for anything after your answer; stop.
- Never call `clarify` during a job. Nobody is there to answer: Hermes replies on the
  user's behalf with "make an assumption and continue", which is a silent guess. A question
  becomes a `needs_input` return; the orchestrator asks the user and sends the job again
  with the answer.
- A job runs as a one-shot turn with limits a normal chat does not have. A `terminal`
  command stops after 180 seconds unless you pass `timeout` (at most 600 for a foreground
  command); pass one that fits and split long web fetches. For anything longer, run the
  command with `background=true` and wait for it with the `process` tool (`action: wait`,
  up to 180 seconds per call, repeated) until it exits, before you answer. Never end your
  turn with a process still running: its result would reach nobody. Destructive shell
  commands (recursive deletes, redirects into config files, `sudo`, piping a download into
  a shell) are refused in a job, not asked about; leave scratch files in the output folder.
- Script paths below are written as `python3 <skills>/<skill>/scripts/<file>.py`. Resolve
  `<skills>` yourself at the start of every job: call `skill_view("dcf-valuation-engine")`,
  take the parent directory of the `skill_dir` field in the result, and confirm with
  `terminal` that `<skills>/dcf-valuation-engine/scripts/dcf.py` exists. Use that absolute
  path everywhere; never guess it.
- Load the skills your process names with `skill_view` before working; the method, the
  reference tables and the scripts live there. Your bundled skills: {', '.join(f'`{s}`' for s in finance)}.
  Your own stage brief is installed as the skill `{name}`; load its reference files with
  `skill_view("{name}", file_path="references/<file>.md")`.
- You share one filesystem with the orchestrator and your teammates. Write only the paths
  the job names, and never edit another stage's artifact.
- A person can also ask you directly, outside any orchestrated run. Then you are in a
  normal conversation: do the work of your stage for them, ask with `clarify` for the inputs
  the job envelope would normally carry (statements or paths, currency, valuation date,
  constraints), resolve `<skills>` as above, write artifacts under a directory they name or a
  `valuation-<company>/` folder in the working directory, and explain the result in prose.
  The method below does not change; only the source of the inputs does.

"""
    return pre + _brief_body(BRIEFS / name)


def _member_readme(member: dict, team: dict, bundled: list[str]) -> str:
    name, title = member["name"], member["title"]
    orch = team["orchestrator"]["name"]
    rows = "\n".join(f"| `{s}` | {_source_for(s)[1]} |" for s in bundled)
    return f"""# {title} (valuation team)

One member of the fifteen-Bot valuation team for Hermes Agent. {member['description'].strip()}

In a team run it receives jobs from `{orch}`, runs its stage, writes the artifacts the job
names, and its answer returns to the orchestrator automatically. You can also open it on its
own and ask it to do its stage for a company you name; it will ask for the inputs it needs.

## Install

Install the whole team from the repository root; the team only works together and only in
the Hermes desktop app with Bot Mode on (Settings → Plugins → Bots):

```bash
tools/install.sh --team {team['team']}
python3 tools/team_models.py {team['team']} --strong <model-id> --fast <model-id>   # optional model tiers
```

This member's tier is **{member['tier']}**. `tools/install.sh` also writes the profile's Bot
metadata (title and role) so teammates see it in their roster.

## Skills bundled

| Skill | Category |
|---|---|
{rows}

## Generated file

`SOUL.md` and this package are generated by `tools/build_team.py` from the stage brief
`teams/valuation/skills/valuation-specialists/{name}/SKILL.md` and the finance skills under
`teams/valuation/skills/corporate-finance/`. Edit those and rebuild.
"""


def _manifest_yaml(name: str, version: str, description: str, env_var: str = "OPENROUTER_API_KEY") -> str:
    desc = " ".join(description.split()).replace('"', '\\"')
    return f"""# Hermes profile distribution manifest (generated by tools/build_team.py).
name: {name}
version: {version}
description: "{desc}"
hermes_requires: ">=0.21.0"
author: "Kushal D'Souza (lyndonkl)"
license: "MIT"
env_requires:
  - name: {env_var}
    description: "API key for the provider every model in config.yaml is routed through"
    required: true
"""


# Provider id (team.yaml `provider:`) -> the env var Hermes reads for it (hermes_cli/auth.py).
PROVIDER_ENV = {"openrouter": "OPENROUTER_API_KEY", "anthropic": "ANTHROPIC_API_KEY",
                "openai-api": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY", "zai": "ZAI_API_KEY"}


def _config_yaml(name: str, tier: str, team: dict) -> str:
    models, efforts = team.get("models") or {}, team.get("effort") or {}
    provider = team.get("provider", "openrouter")
    model = models.get(tier, "")
    effort = efforts.get(tier, "medium" if tier == "fast" else "high")
    prior = {"strong": "opus", "fast": "sonnet"}.get(tier, "opus")
    aux = team.get("auxiliary_model", "")
    aux_block = "".join(
        f"  {role}:\n    provider: {provider}\n    model: {aux}\n"
        for role in ("compression", "title_generation", "background_review", "approval", "skills_hub",
                     "mcp", "profile_describer", "goal_judge", "curator", "monitor",
                     "triage_specifier", "kanban_decomposer", "memory_query_rewrite")) if aux else ""
    model_block = (f"model:\n  provider: {provider}\n  default: {model}\n\n" if model else
                   "# model: none pinned — run `hermes -p " + name + " model`\n\n")
    # The desktop backend unloads a Bot Chat 20 s after the app stops showing it, and unloading
    # kills the session's background processes: that is where every message_agent delivery and
    # the teammate turn inside it run. 0 is Hermes's documented "never unload a detached chat"
    # value, so a stage survives switching chats or closing the window. Orchestrator only: it is
    # the one profile that has jobs out while nobody is looking at its chat.
    reap_block = (
        "\n# The desktop otherwise closes this chat 20 s after you switch away from it, and closing it\n"
        "# kills every stage job it has out (Hermes tui_gateway ws-orphan reap). 0 = never close.\n"
        "dashboard:\n  ws_orphan_reap_grace_s: 0\n") if tier == "orchestrator" else ""
    return f"""# Behavioural defaults for the {name} Bot (generated by tools/build_team.py).
# Tier: {tier} (the Claude Code version ran this agent on {prior}). The model below is the
# team manifest's pick for this tier (see docs/MODELS.md). Change it with
# `python3 tools/team_models.py {team['team']} --preset ...` or `hermes -p {name} model`.
# This file is preserved across `hermes profile update`.

{model_block}agent:
  reasoning_effort: "{effort}"

skills:
  creation_nudge_interval: 0     # curated agent; do not nudge it to write new skills

# SOUL.md is a context file. Hermes cuts context files above 20,000 characters when it cannot
# tell the model's window; ours run to 30,000, so pin a cap that fits.
context_file_max_chars: 60000
{reap_block}
# Housekeeping calls on a cheap model; nothing here needs reasoning. Any role left unset runs
# on the main model at its price. vision stays unset (the cheap model has no vision); review
# stays on the main model on purpose.
auxiliary:
{aux_block}"""


def _bot_yaml(member: dict, team: str) -> str:
    return yaml.safe_dump({
        "team": team, "title": member["title"], "tier": member["tier"],
        "description": " ".join(member["description"].split()),
    }, sort_keys=False, allow_unicode=True)


def _write_package(pkg: Path, member: dict, team: dict, *, is_orchestrator: bool) -> None:
    log: list[str] = []
    bundled = _closure(list(member.get("skills") or []), None if is_orchestrator else member["name"], log)
    if log:
        print(f"  {member['name']}: dependency closure added")
        print("\n".join(log))
    keep = {"SOUL.md", "README.md"} if is_orchestrator else set()
    if pkg.exists():
        for child in pkg.iterdir():
            if child.name in keep:
                continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "distribution.yaml").write_text(_manifest_yaml(
        member["name"], team["version"], member["description"],
        env_var=PROVIDER_ENV.get(team.get("provider", "openrouter"), "OPENROUTER_API_KEY")), encoding="utf-8")
    (pkg / "config.yaml").write_text(_config_yaml(member["name"], member["tier"], team), encoding="utf-8")
    (pkg / "bot.yaml").write_text(_bot_yaml(member, team["team"]), encoding="utf-8")
    (pkg / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    (pkg / ".no-bundled-skills").write_text(NO_BUNDLED, encoding="utf-8")
    if not is_orchestrator:
        (pkg / "SOUL.md").write_text(_member_soul(member, team, bundled), encoding="utf-8")
        (pkg / "README.md").write_text(_member_readme(member, team, bundled), encoding="utf-8")
    else:
        for f in keep:
            if not (pkg / f).is_file():
                raise SystemExit(f"{pkg.name}: hand-written {f} is missing")
    categories: dict[str, list[str]] = {}
    for name in bundled:
        src, cat = _source_for(name)
        _copy_skill(src, pkg / "skills" / cat / name, set(bundled))
        categories.setdefault(cat, []).append(name)
    for cat in categories:
        desc_src = SUITE / cat / "DESCRIPTION.md"
        shutil.copy2(desc_src, pkg / "skills" / cat / "DESCRIPTION.md")
    shared = [f"writing/{n}" for n in categories.get("writing", [])]
    if shared:
        (pkg / "shared-skills.txt").write_text(
            "# <category>/<skill> — copied from shared/skills/<skill> by tools/sync_shared.py\n" + "\n".join(shared) + "\n",
            encoding="utf-8")


def build(manifest: Path, out_root: Path) -> list[Path]:
    _set_sources(manifest.parent)
    team = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    written = []
    orch = team["orchestrator"]
    pkg = out_root / orch["name"]
    if out_root != PACKAGES:
        # --check: stage the hand-written files so the comparison is like-for-like.
        pkg.mkdir(parents=True, exist_ok=True)
        for f in ("SOUL.md", "README.md"):
            shutil.copy2(PACKAGES / orch["name"] / f, pkg / f)
    _write_package(pkg, orch, team, is_orchestrator=True)
    written.append(pkg)
    for member in team["members"]:
        p = out_root / member["name"]
        _write_package(p, member, team, is_orchestrator=False)
        written.append(p)
    return written


def _diff(a: Path, b: Path) -> list[str]:
    cmp = filecmp.dircmp(a, b, ignore=[".DS_Store", "__pycache__"])
    out = [f"{a.name}: {x}" for x in (*cmp.left_only, *cmp.right_only, *cmp.diff_files, *cmp.funny_files)]
    for sub in cmp.subdirs.values():
        out.extend(_diff(Path(sub.left), Path(sub.right)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("team", nargs="?", default="valuation")
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    args = ap.parse_args()
    manifest = ROOT / "teams" / args.team / "team.yaml"
    if not manifest.is_file():
        sys.exit(f"no manifest at {manifest}")
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            staged = build(manifest, Path(tmp))
            drift: list[str] = []
            for p in staged:
                live = PACKAGES / p.name
                drift.extend(_diff(p, live) if live.is_dir() else [f"{p.name}: package missing"])
        if drift:
            print("\n".join(f"DRIFT  {d}" for d in drift))
            print(f"{len(drift)} difference(s) — run tools/build_team.py {args.team}")
            return 1
        print(f"team '{args.team}' packages are up to date")
        return 0
    written = build(manifest, PACKAGES)
    print(f"generated {len(written)} packages: " + ", ".join(p.name for p in written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
