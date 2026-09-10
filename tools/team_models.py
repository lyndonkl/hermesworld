#!/usr/bin/env python3
"""Apply model tiers to the installed profiles of a Bot team.

The Claude Code version of the valuation team ran some agents on opus and some
on sonnet. Hermes packages here pin no model, so installers keep their own
credentials. This helper restores the split after `tools/install.sh --team`:

    python3 tools/team_models.py valuation --strong anthropic/claude-opus-4.6 \
                                           --fast anthropic/claude-sonnet-4.5
    python3 tools/team_models.py valuation --strong <model> --fast <model> --provider openrouter
    python3 tools/team_models.py valuation --show

It edits `model.default` (and `model.provider` when --provider is given) in
~/.hermes/profiles/<member>/config.yaml for every member whose tier matches.
Everything else in each config is preserved. Reverse or adjust any single
profile with `hermes -p <name> model`.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("team")
    ap.add_argument("--strong", help="model id for tier 'strong'")
    ap.add_argument("--fast", help="model id for tier 'fast'")
    ap.add_argument("--provider", help="provider to set alongside the model (default: keep existing)")
    ap.add_argument("--show", action="store_true", help="print each member's tier and current model")
    args = ap.parse_args()

    manifest = ROOT / "teams" / f"{args.team}-team.yaml"
    if not manifest.is_file():
        sys.exit(f"no manifest at {manifest}")
    team = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    members = [team["orchestrator"], *team["members"]]
    home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
    tiers = {"strong": args.strong, "fast": args.fast}
    if not args.show and not any(tiers.values()):
        ap.error("pass --strong and/or --fast, or --show")

    changed = 0
    for m in members:
        cfg_path = home / "profiles" / m["name"] / "config.yaml"
        if not cfg_path.is_file():
            print(f"  {m['name']:<30} tier={m['tier']:<6} not installed")
            continue
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        model = cfg.get("model")
        if isinstance(model, str):            # legacy string form
            model = {"default": model}
        model = model or {}
        current = model.get("default", "")
        if args.show:
            print(f"  {m['name']:<30} tier={m['tier']:<6} model={current or '(unset)'}")
            continue
        wanted = tiers.get(m["tier"])
        if not wanted:
            continue
        if current == wanted and (not args.provider or model.get("provider") == args.provider):
            continue
        model["default"] = wanted
        if args.provider:
            model["provider"] = args.provider
        cfg["model"] = model
        cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
        changed += 1
        print(f"  {m['name']:<30} tier={m['tier']:<6} -> {wanted}")
    if not args.show:
        print(f"{changed} profile(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
