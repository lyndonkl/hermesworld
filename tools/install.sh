#!/usr/bin/env bash
# Install packages from this checkout as Hermes profiles.
#
#   tools/install.sh superforecaster              # one package
#   tools/install.sh --all                        # every package (standalone agents + teams)
#   tools/install.sh --team valuation             # a Bot team: its orchestrator + every member
#   tools/install.sh superforecaster --no-alias   # skip the shell wrapper
#
# Uses `hermes profile install <local dir>`, the documented way to install a
# distribution before (or instead of) pushing it to its own repo. The installer
# copies the package into ~/.hermes/profiles/<name>/ and records this directory
# as the update source, so `git pull && hermes profile update <name>` picks up
# new versions.
#
# After each install, tools/post_install.py:
#   1. seeds the profile's model block from your root profile when the package
#      ships no model pin (none of ours do); change it with `hermes -p <name> model`;
#   2. for team members (packages with a bot.yaml), writes the profile's Bot
#      metadata once — description and Bot title in profile.yaml — so the
#      desktop roster and every teammate's system prompt show who does what.
#      Existing values are kept, so your desktop customisations survive updates.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME_ROOT="${HERMES_HOME:-$HOME/.hermes}"
ALIAS="--alias"
PKGS=()

team_members() {  # print orchestrator + member names of teams/<name>-team.yaml
  python3 - "$ROOT/teams/$1-team.yaml" <<'PY'
import sys, yaml
t = yaml.safe_load(open(sys.argv[1]))
print(t["orchestrator"]["name"])
for m in t["members"]:
    print(m["name"])
PY
}

i=0; args=("$@")
while [ $i -lt ${#args[@]} ]; do
  arg="${args[$i]}"
  case "$arg" in
    --all) for d in "$ROOT"/packages/*/; do PKGS+=("$(basename "$d")"); done ;;
    --team)
      i=$((i+1)); team="${args[$i]:-}"
      [ -f "$ROOT/teams/$team-team.yaml" ] || { echo "no team manifest teams/$team-team.yaml" >&2; exit 2; }
      while IFS= read -r m; do PKGS+=("$m"); done < <(team_members "$team") ;;
    --no-alias) ALIAS="" ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) PKGS+=("$arg") ;;
  esac
  i=$((i+1))
done

if [ ${#PKGS[@]} -eq 0 ]; then
  echo "usage: tools/install.sh <package>... | --all | --team <name>  [--no-alias]" >&2
  exit 2
fi
command -v hermes >/dev/null || { echo "hermes is not on PATH (the desktop app installs it at ~/.local/bin/hermes)" >&2; exit 1; }

for pkg in "${PKGS[@]}"; do
  src="$ROOT/packages/$pkg"
  [ -f "$src/distribution.yaml" ] || { echo "no distribution.yaml in $src" >&2; exit 1; }
  echo "==> installing $pkg"
  # shellcheck disable=SC2086
  hermes profile install "$src" $ALIAS --yes --force
  python3 "$ROOT/tools/post_install.py" "$src" "$HERMES_HOME_ROOT/profiles/$pkg" "$HERMES_HOME_ROOT/config.yaml"
  echo "    run:  hermes -p $pkg chat      (or just: $pkg chat, if the alias was created)"
done

if printf '%s\n' "${PKGS[@]}" | grep -q "^valuation-orchestrator$"; then
  cat <<'EOF'

Team installed. Next:
  - optional model tiers:  python3 tools/team_models.py valuation --strong <model-id> --fast <model-id>
  - in the Hermes desktop app: Settings -> Plugins -> Bots on, then open valuation-orchestrator
    from the Bots roster and give it a company. Teammates are addressed with message_agent,
    which exists only in Bot Chats, so the team does not run from the CLI.
EOF
fi
