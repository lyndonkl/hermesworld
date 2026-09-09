#!/usr/bin/env python3
"""Mechanically convert a Claude Code skill directory into the Hermes layout.

This does the deterministic part of a port. It does NOT write the final
60-character description or the `## When to Use` prose — those need judgment
and are left as clearly marked drafts for a human or agent to finish.
tools/validate.py fails until they are.

What it does
------------
Layout (Claude `resources/` -> Hermes support dirs; see agent/skill_utils.py
SKILL_SUPPORT_DIRS and tools/skills_tool.py _LINKED_FILE_SPECS):

    resources/*.py                   -> scripts/
    resources/data/**                -> scripts/data/**      (scripts locate data next to themselves)
    resources/template*.md,
    resources/*templates*.md         -> templates/
    resources/evaluators/*.json      -> assets/evaluators/
    resources/*.json                 -> assets/
    resources/examples/<x>.md        -> references/example-<x>.md   (flattened: only top-level
                                                                     references/*.md are listed)
    resources/*.md (everything else) -> references/
    <top-level>/*.md except SKILL.md -> references/
    hooks/                           -> dropped (Claude Code hook mechanism)

SKILL.md text: every `resources/...` path is rewritten to its new home. Script
invocations become `python3 ${HERMES_SKILL_DIR}/scripts/<x>.py` so they
resolve from any working directory (Hermes substitutes the token when the
skill is viewed). Cross-skill paths `../<skill>/resources/<x>.py` become
`${HERMES_SKILL_DIR}/../<skill>/scripts/<x>.py`.

Frontmatter: keeps `name`, keeps the long Claude description verbatim (it
carries the trigger phrases) and adds version/author/license/metadata.hermes.
A `## When to Use` draft holding that description is inserted after the H1 so
nothing is lost while the description is shortened.

Usage:
    python3 tools/convert_claude_skill.py SRC_DIR DST_DIR --category writing \
        [--author "Name (handle)"] [--license MIT] [--tags a,b,c] [--related x,y]
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

FRONTMATTER_END_RE = re.compile(r"\n---\s*\n")


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = FRONTMATTER_END_RE.search(text[3:])
    if not end:
        return {}, text
    fm = yaml.safe_load(text[3: end.start() + 3]) or {}
    return fm, text[end.end() + 3:]


def dump_frontmatter(fm: dict) -> str:
    class Dumper(yaml.SafeDumper):
        pass

    def str_presenter(dumper, data):
        style = '"' if any(c in data for c in ':#') and "\n" not in data else None
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)

    Dumper.add_representer(str, str_presenter)
    return "---\n" + yaml.dump(fm, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000) + "---\n"


def plan_moves(src: Path):
    """Yield (source_file, destination_relative_path) pairs."""
    res = src / "resources"
    if res.is_dir():
        for f in sorted(res.rglob("*")):
            if not f.is_file() or f.name == ".DS_Store":
                continue
            rel_in = f.relative_to(res)
            parts = rel_in.parts
            if parts[0] == "data":
                yield f, Path("scripts") / rel_in
            elif f.suffix == ".py":
                yield f, Path("scripts") / f.name
            elif parts[0] == "evaluators":
                yield f, Path("assets") / rel_in
            elif parts[0] == "examples":
                yield f, Path("references") / f"example-{f.name}"
            elif f.suffix == ".json":
                yield f, Path("assets") / rel_in
            elif f.suffix == ".md" and ("template" in f.stem):
                yield f, Path("templates") / f.name
            elif f.suffix == ".md":
                yield f, Path("references") / f.name
            else:
                yield f, Path("assets") / rel_in
    for f in sorted(src.iterdir()):
        if f.is_file() and f.suffix == ".md" and f.name != "SKILL.md":
            yield f, Path("references") / f.name


def rewrite_paths(body: str, moves: dict) -> str:
    """Rewrite resources/ references using the concrete move table, then generic fallbacks."""
    # Normalise the explicit-relative spelling so every rule below sees one form.
    body = re.sub(r"(?<![\w/])\./resources/", "resources/", body)
    # Cross-skill script references first (they contain 'resources/' too).
    body = re.sub(r"(?:\.\./)+([\w-]+)/resources/([\w./-]+\.py)",
                  r"${HERMES_SKILL_DIR}/../\1/scripts/\2", body)
    # Concrete moves, longest source path first so 'resources/data/x' wins over 'resources/x'.
    for old_rel, new_rel in sorted(moves.items(), key=lambda kv: -len(kv[0])):
        old = f"resources/{old_rel}"
        new = new_rel.as_posix()
        if new.startswith("scripts/") and new.endswith(".py"):
            # `python3 resources/x.py` -> `python3 ${HERMES_SKILL_DIR}/scripts/x.py`
            body = re.sub(rf"(python3?\s+){re.escape(old)}\b", rf"\1${{HERMES_SKILL_DIR}}/{new}", body)
            # `| python3 resources/x.py` inside pipelines is covered above; bare mentions:
            body = re.sub(rf"(?<![\w/$}}]){re.escape(old)}\b", new, body)
        else:
            body = re.sub(rf"(?<![\w/$}}]){re.escape(old)}\b", new, body)
    # Generic fallbacks for anything not in the table (e.g. globs like resources/*.md).
    body = re.sub(r"(?<![\w/])resources/data/", "scripts/data/", body)
    body = re.sub(r"(?<![\w/])resources/evaluators/", "assets/evaluators/", body)
    body = re.sub(r"(?<![\w/])resources/examples/", "references/", body)
    body = re.sub(r"(?<![\w/])resources/(\S+\.py)\b", r"scripts/\1", body)
    body = re.sub(r"(?<![\w/])resources/(\S*template\S*\.md)\b", r"templates/\1", body)
    body = re.sub(r"(?<![\w/])resources/(\S+\.md)\b", r"references/\1", body)
    body = re.sub(r"(?<![\w/])resources/(\S+\.json)\b", r"assets/\1", body)
    body = re.sub(r"(?<![\w/])resources/", "references/", body)
    return body


def insert_when_to_use(body: str, description: str) -> str:
    if re.search(r"^#+\s+When to [Uu]se", body, re.M):
        return body
    draft = (
        "\n## When to Use\n\n"
        "<!-- CONVERT: turn the original Claude description below into 3-6 crisp trigger bullets, "
        "then delete this comment. -->\n\n"
        f"{description.strip()}\n"
    )
    m = re.search(r"^# .+\n", body, re.M)
    if m:
        # After the H1 and its intro paragraph(s), before the first H2.
        first_h2 = re.search(r"^## ", body[m.end():], re.M)
        cut = m.end() + (first_h2.start() if first_h2 else 0)
        return body[:cut].rstrip("\n") + "\n" + draft + "\n" + body[cut:]
    return draft + body


def convert(src: Path, dst: Path, category: str, author: str, license_: str, tags, related) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    skill_md = (src / "SKILL.md").read_text(encoding="utf-8")
    fm, body = split_frontmatter(skill_md)
    name = fm.get("name") or src.name
    if name != src.name:
        print(f"  note: frontmatter name '{name}' != dir '{src.name}', using dir name", file=sys.stderr)
        name = src.name
    moves = {}
    for f, new_rel in plan_moves(src):
        target = dst / new_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
        try:
            moves[f.relative_to(src / "resources").as_posix()] = new_rel
        except ValueError:
            moves[f.name] = new_rel  # top-level md moved into references/
    body = rewrite_paths(body, moves)
    description = str(fm.get("description", "")).strip()
    body = insert_when_to_use(body, description)
    new_fm = {
        "name": name,
        "description": description,
        "version": "1.0.0",
        "author": author,
        "license": license_,
        "platforms": ["linux", "macos", "windows"],
        "metadata": {"hermes": {"category": category, "tags": tags, "related_skills": related}},
    }
    (dst / "SKILL.md").write_text(dump_frontmatter(new_fm) + body.lstrip("\n"), encoding="utf-8")
    dropped = [p.name for p in src.iterdir() if p.is_dir() and p.name not in ("resources",)]
    if dropped:
        print(f"  dropped Claude-only dirs: {dropped}", file=sys.stderr)
    print(f"converted {src.name} -> {dst} ({len(moves)} support files)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--category", required=True)
    ap.add_argument("--author", default="Kushal D'Souza (lyndonkl)")
    ap.add_argument("--license", default="MIT")
    ap.add_argument("--tags", default="", help="comma-separated")
    ap.add_argument("--related", default="", help="comma-separated related skill names")
    args = ap.parse_args()
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    related = [r.strip() for r in args.related.split(",") if r.strip()]
    convert(args.src, args.dst, args.category, args.author, args.license, tags, related)
    return 0


if __name__ == "__main__":
    sys.exit(main())
