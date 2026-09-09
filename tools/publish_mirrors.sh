#!/usr/bin/env bash
# Publish each package as its own git repository so it can be installed by URL.
#
# Why this exists: `hermes profile install <git-url>` shallow-clones the URL and
# requires distribution.yaml at the ROOT of the clone (hermes_cli/
# profile_distribution.py, _stage_source). It has no sub-directory or #ref
# syntax, so a package inside this monorepo cannot be installed by URL
# directly. `git subtree split` produces a branch whose root IS the package;
# pushing that branch to a mirror repo gives installers a plain
# `hermes profile install github.com/<owner>/hermes-<pkg>`.
#
#   tools/publish_mirrors.sh <owner> [package...]      # push mirrors
#   tools/publish_mirrors.sh <owner> --create [pkg...] # also create missing repos with gh
#   DRY_RUN=1 tools/publish_mirrors.sh <owner>         # print what would happen
#
# Mirror repos are named hermes-<package>. Local install (tools/install.sh)
# needs none of this.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWNER="${1:-}"; shift || true
[ -n "$OWNER" ] || { sed -n '2,17p' "$0"; exit 2; }

CREATE=0
PKGS=()
for arg in "$@"; do
  case "$arg" in
    --create) CREATE=1 ;;
    *) PKGS+=("$arg") ;;
  esac
done
if [ ${#PKGS[@]} -eq 0 ]; then
  for d in "$ROOT"/packages/*/; do PKGS+=("$(basename "$d")"); done
fi

cd "$ROOT"
git diff --quiet && git diff --cached --quiet || { echo "commit or stash your changes first" >&2; exit 1; }

run() { if [ "${DRY_RUN:-0}" = "1" ]; then echo "+ $*"; else "$@"; fi; }

for pkg in "${PKGS[@]}"; do
  repo="hermes-$pkg"
  branch="mirror/$pkg"
  echo "==> $pkg -> github.com/$OWNER/$repo"
  if [ "$CREATE" = "1" ] && ! gh repo view "$OWNER/$repo" >/dev/null 2>&1; then
    run gh repo create "$OWNER/$repo" --private \
      --description "Hermes Agent profile distribution: $pkg (mirror of $OWNER/hermesworld)"
  fi
  run git subtree split --prefix="packages/$pkg" -b "$branch"
  run git push --force "git@github.com:$OWNER/$repo.git" "$branch:main"
  run git branch -D "$branch"
  echo "    install with: hermes profile install github.com/$OWNER/$repo --alias"
done
