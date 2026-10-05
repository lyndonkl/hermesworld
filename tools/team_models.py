#!/usr/bin/env python3
"""Switch all inference routes of an installed Bot team.

Examples:
    python3 tools/team_models.py valuation --preset codex-pro
    python3 tools/team_models.py engineering --preset balanced
    python3 tools/team_models.py valuation --strong openai/gpt-6-astra --provider openrouter

Presets select primary models, reasoning levels, auxiliary and delegated models
as one policy. Honcho remains configured independently. Use --show to inspect
installed settings, or --dry-run to preview a switch without writing.
"""
import argparse
import os
from pathlib import Path
import yaml
from profile_models import ROOT, PRESETS, migrate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("team")
    parser.add_argument("--preset", choices=PRESETS)
    for tier in ("orchestrator", "strong", "fast", "writer"):
        parser.add_argument("--" + tier, help=f"model override for {tier} profiles")
    parser.add_argument("--provider", choices=("openai-codex", "openrouter"))
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = ROOT / "teams" / args.team / "team.yaml"
    if not manifest.is_file():
        parser.error(f"no team manifest at {manifest}")
    team = yaml.safe_load(manifest.read_text())
    members = [team["orchestrator"], *team["members"]]
    home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
    if args.show:
        for member in members:
            path = home / "profiles" / member["name"] / "config.yaml"
            cfg = yaml.safe_load(path.read_text()) if path.is_file() else {}
            print(f"{member['name']}: model={cfg.get('model', '(not installed)')} effort={(cfg.get('agent') or {}).get('reasoning_effort')}")
        return 0
    overrides = {tier: getattr(args, tier) for tier in ("orchestrator", "strong", "fast", "writer")}
    if not args.preset and not any(overrides.values()):
        parser.error("pass --preset, a tier override, or --show")
    expected = "openai-codex" if args.preset == "codex-pro" else "openrouter"
    if args.preset and args.provider and args.provider != expected:
        parser.error(f"{args.preset} requires provider {expected}")
    if not args.preset and not args.provider:
        parser.error("custom tier overrides require --provider")
    return migrate([m["name"] for m in members], args.preset, not args.dry_run,
                   overrides=overrides, provider=args.provider)


if __name__ == "__main__":
    raise SystemExit(main())
