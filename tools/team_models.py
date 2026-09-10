#!/usr/bin/env python3
"""Apply model tiers to the installed profiles of a Bot team.

The Claude Code version of the valuation team ran some agents on opus and some
on sonnet. Every package here ships a model per tier in its config.yaml (see
docs/MODELS.md); this helper switches the installed profiles to another preset,
or to models you name, after `tools/install.sh --team`:

    python3 tools/team_models.py valuation --preset balanced      # frontier | balanced | budget
    python3 tools/team_models.py valuation --orchestrator <model> --strong <model> --fast <model>
    python3 tools/team_models.py valuation --preset budget --strong meta/muse-spark-1.3   # preset + override
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

# OpenRouter model ids per tier. Rationale and the benchmark rows behind them: docs/MODELS.md
# (Artificial Analysis + OpenRouter prices as of 2026-09-09; re-check before relying on them).
PRESETS = {
    "frontier": {"orchestrator": "anthropic/claude-fable-5.1", "strong": "anthropic/claude-opus-5",
                 "fast": "anthropic/claude-sonnet-5", "writer": "openai/gpt-5.6-sol"},
    "balanced": {"orchestrator": "meta/muse-spark-1.3", "strong": "meta/muse-spark-1.3",
                 "fast": "google/gemini-3.7-flash", "writer": "google/gemini-3.7-flash"},
    "budget":   {"orchestrator": "z-ai/glm-5.3", "strong": "z-ai/glm-5.3", "fast": "z-ai/glm-5.3-flash",
                 "writer": "google/gemini-3.7-flash"},
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("team")
    ap.add_argument("--preset", choices=sorted(PRESETS), help="apply a named preset from docs/MODELS.md")
    ap.add_argument("--orchestrator", help="model id for tier 'orchestrator'")
    ap.add_argument("--strong", help="model id for tier 'strong'")
    ap.add_argument("--fast", help="model id for tier 'fast'")
    ap.add_argument("--writer", help="model id for tier 'writer' (report writing)")
    ap.add_argument("--provider", help="provider to set alongside the model (default: keep existing)")
    ap.add_argument("--show", action="store_true", help="print each member's tier and current model")
    args = ap.parse_args()

    manifest = ROOT / "teams" / args.team / "team.yaml"
    if not manifest.is_file():
        sys.exit(f"no manifest at {manifest}")
    team = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    members = [team["orchestrator"], *team["members"]]
    home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
    tiers = dict(PRESETS[args.preset]) if args.preset else {}
    for tier in ("orchestrator", "strong", "fast", "writer"):
        if getattr(args, tier):
            tiers[tier] = getattr(args, tier)
    if not args.show and not tiers:
        ap.error("pass --preset, or --orchestrator/--strong/--fast, or --show")

    changed = 0
    for m in members:
        cfg_path = home / "profiles" / m["name"] / "config.yaml"
        if not cfg_path.is_file():
            print(f"  {m['name']:<30} tier={m['tier']:<12} not installed")
            continue
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        model = cfg.get("model")
        if isinstance(model, str):            # legacy string form
            model = {"default": model}
        model = model or {}
        current = model.get("default", "")
        if args.show:
            print(f"  {m['name']:<30} tier={m['tier']:<12} model={current or '(unset)'}")
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
        print(f"  {m['name']:<30} tier={m['tier']:<12} -> {wanted}")
    if not args.show:
        print(f"{changed} profile(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
