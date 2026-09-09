#!/usr/bin/env python3
"""Copy canonical shared skills into every package that declares them.

A Hermes distribution must be self-contained (the installer clones one
directory and rejects symlinks), so a skill used by several packages is
authored once under shared/skills/<skill>/ and copied into each package.

Each package lists what it borrows in packages/<pkg>/shared-skills.txt, one
entry per line as <category>/<skill>:

    writing/readability-check
    writing/slop-detector

Usage:
    python3 tools/sync_shared.py            # sync all packages
    python3 tools/sync_shared.py --check    # exit 1 if any copy has drifted

Edit shared skills only under shared/skills/. tools/validate.py fails when a
package copy differs from the canonical one.
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"
SHARED = ROOT / "shared" / "skills"


def entries(pkg: Path):
    manifest = pkg / "shared-skills.txt"
    if not manifest.is_file():
        return
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        category, _, skill = line.partition("/")
        if not skill:
            sys.exit(f"{manifest}: entry '{line}' must be '<category>/<skill>'")
        yield category, skill


def differs(src: Path, dst: Path) -> bool:
    if not dst.is_dir():
        return True
    cmp = filecmp.dircmp(src, dst, ignore=[".DS_Store"])

    def walk(c: filecmp.dircmp) -> bool:
        if c.left_only or c.right_only or c.diff_files or c.funny_files:
            return True
        return any(walk(s) for s in c.subdirs.values())

    return walk(cmp)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report drift without copying")
    args = ap.parse_args()
    drift = 0
    for pkg in sorted(p for p in PACKAGES.iterdir() if p.is_dir()):
        for category, skill in entries(pkg):
            src = SHARED / skill
            if not src.is_dir():
                sys.exit(f"shared/skills/{skill} does not exist (declared by {pkg.name})")
            dst = pkg / "skills" / category / skill
            if not differs(src, dst):
                continue
            drift += 1
            if args.check:
                print(f"DRIFT  {dst.relative_to(ROOT)}")
                continue
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
            print(f"synced {dst.relative_to(ROOT)}")
    if args.check:
        print("all shared copies in sync" if not drift else f"{drift} copy(ies) drifted")
        return 1 if drift else 0
    print("done" if drift else "nothing to sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
