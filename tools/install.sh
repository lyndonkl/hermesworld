#!/usr/bin/env bash
# Install one or more packages from this checkout as Hermes profiles.
#
#   tools/install.sh superforecaster              # one package
#   tools/install.sh --all                        # every package
#   tools/install.sh superforecaster --no-alias   # skip the shell wrapper
#
# Uses `hermes profile install <local dir>`, which is the documented way to
# install a distribution before (or instead of) pushing it to its own repo.
# The installer copies the package into ~/.hermes/profiles/<name>/, strips
# nothing you authored, and records this directory as the update source, so
# `git pull && hermes profile update <name>` picks up new versions.
#
# After install the script seeds the profile's model block from your root
# profile when the package ships no model pin (packages here deliberately do
# not pin a model or provider). Change it any time with `hermes -p <name> model`.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME_ROOT="${HERMES_HOME:-$HOME/.hermes}"
ALIAS="--alias"
PKGS=()

for arg in "$@"; do
  case "$arg" in
    --all) for d in "$ROOT"/packages/*/; do PKGS+=("$(basename "$d")"); done ;;
    --no-alias) ALIAS="" ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    *) PKGS+=("$arg") ;;
  esac
done

if [ ${#PKGS[@]} -eq 0 ]; then
  echo "usage: tools/install.sh <package> [<package>...] | --all  [--no-alias]" >&2
  exit 2
fi
command -v hermes >/dev/null || { echo "hermes is not on PATH" >&2; exit 1; }

seed_model_block() {
  # Mirror hermes_cli.profiles._seed_model_config: copy the root profile's
  # model block into the new profile when its config.yaml has none.
  local profile_cfg="$1"
  python3 - "$profile_cfg" "$HERMES_HOME_ROOT/config.yaml" <<'PY'
import sys, pathlib
try:
    import yaml
except ImportError:
    sys.exit(0)
dst, src = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
if not src.is_file():
    sys.exit(0)
cfg = yaml.safe_load(dst.read_text()) if dst.is_file() else {}
cfg = cfg or {}
if cfg.get("model"):
    sys.exit(0)
root = yaml.safe_load(src.read_text()) or {}
if not root.get("model"):
    sys.exit(0)
cfg = {"model": root["model"], **cfg}
dst.write_text(yaml.safe_dump(cfg, sort_keys=False))
print(f"  seeded model block from {src}")
PY
}

for pkg in "${PKGS[@]}"; do
  src="$ROOT/packages/$pkg"
  [ -f "$src/distribution.yaml" ] || { echo "no distribution.yaml in $src" >&2; exit 1; }
  echo "==> installing $pkg"
  # shellcheck disable=SC2086
  hermes profile install "$src" $ALIAS --yes --force
  seed_model_block "$HERMES_HOME_ROOT/profiles/$pkg/config.yaml"
  echo "    run:  hermes -p $pkg chat      (or just: $pkg chat, if the alias was created)"
done
