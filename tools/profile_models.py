#!/usr/bin/env python3
"""Preview or apply OpenAI subscription or OpenRouter routes to installed profiles.

Authenticate the selected provider in Hermes before applying. Defaults to a preview; --apply
writes configs and creates a backup beside each changed file. Honcho settings
and credentials remain user-owned and are preserved.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
PROVIDER = "openai-codex"
ROLES = ("compression", "title_generation", "background_review", "review", "vision",
         "approval", "skills_hub", "mcp", "memory_query_rewrite", "tts_audio_tags",
         "triage_specifier", "kanban_decomposer", "profile_describer", "goal_judge",
         "curator", "monitor", "moa_reference", "moa_aggregator")


def auxiliary_route(role: str, provider: str = PROVIDER) -> dict:
    model, effort = "gpt-5.6-luna", "low"
    if role == "compression":
        model = "gpt-5.6-terra"
    elif role in {"review", "background_review", "moa_aggregator"}:
        model, effort = "gpt-5.6-sol", "high"
    elif role in {"vision", "goal_judge", "kanban_decomposer", "moa_reference"}:
        model, effort = "gpt-5.6-terra", "medium"
    if provider == "openrouter":
        model = "z-ai/glm-5.3-flash"
    route = {"provider": provider, "model": model}
    if role not in {"moa_reference", "moa_aggregator"}:
        route["reasoning_effort"] = effort
    return route


def routed(block: dict | None, route: dict) -> dict:
    result = deepcopy(block) if isinstance(block, dict) else {}
    # Explicit endpoints bypass provider auth; stale API credentials must not
    # turn a subscription route into a request to another provider.
    for key in ("base_url", "api_key", "fallback_model", "fallback_provider",
                "fallback_providers", "reasoning_effort"):
        result.pop(key, None)
    extra = result.get("extra_body")
    if isinstance(extra, dict):
        for key in ("reasoning", "reasoning_effort", "thinking", "thinking_config"):
            extra.pop(key, None)
    result.update(route)
    return result


def apply_routes(config: dict, model: str, effort: str, provider: str = PROVIDER) -> dict:
    result = deepcopy(config)
    # Replace the primary routing block; keep all unrelated profile settings.
    result["model"] = {"provider": provider, "default": model}
    agent = result.setdefault("agent", {})
    agent["reasoning_effort"] = effort
    agent.pop("reasoning_overrides", None)
    result.pop("fallback_model", None)
    result.pop("fallback_provider", None)
    result["fallback_providers"] = []
    auxiliary = result.setdefault("auxiliary", {})
    for role in [*ROLES, *sorted(set(auxiliary) - set(ROLES))]:
        auxiliary[role] = routed(auxiliary.get(role), auxiliary_route(role, provider))
    # Explicitly pin children so a root-profile default cannot select OpenRouter.
    result["delegation"] = routed(result.get("delegation"), {
        "provider": provider, "model": model, "reasoning_effort": effort})
    result["delegation"]["fallback_providers"] = []
    if "compression" in result:
        result["compression"] = routed(result["compression"], auxiliary_route("compression", provider))
    return result


def shipped_policy(name: str) -> tuple[str, str]:
    source = yaml.safe_load((ROOT / "packages" / name / "config.yaml").read_text())
    return source["model"]["default"], source["agent"]["reasoning_effort"]


OPENROUTER_PRESETS = {
    "frontier": {"orchestrator": "anthropic/claude-fable-5.1", "strong": "anthropic/claude-opus-5",
                 "fast": "anthropic/claude-sonnet-5", "writer": "openai/gpt-5.6-sol"},
    "balanced": {tier: "z-ai/glm-5.3-flash" for tier in ("orchestrator", "strong", "fast", "writer")},
    "qwen": {"orchestrator": "qwen/qwen3.6-plus", "strong": "qwen/qwen3.6-plus",
             "fast": "z-ai/glm-5.3-flash", "writer": "z-ai/glm-5.3-flash"},
    "budget": {tier: "z-ai/glm-5.3-flash" for tier in ("orchestrator", "strong", "fast", "writer")},
}
PRESETS = ("codex-pro", *OPENROUTER_PRESETS)


def profile_tier(name: str) -> str:
    bot = ROOT / "packages" / name / "bot.yaml"
    if bot.is_file():
        return yaml.safe_load(bot.read_text())["tier"]
    return "strong"


def migrate(names: list[str], preset: str | None, apply: bool, *,
            overrides: dict | None = None, provider: str | None = None) -> int:
    home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    changed = 0
    for name in names:
        path = home / "profiles" / name / "config.yaml"
        if not path.is_file():
            print(f"{name}: not installed")
            continue
        original = path.read_text(encoding="utf-8")
        config = yaml.safe_load(original) or {}
        model, effort = shipped_policy(name)
        tier = profile_tier(name)
        if preset is None and not (overrides or {}).get(tier):
            continue
        route_provider = provider or ("openrouter" if preset in OPENROUTER_PRESETS else PROVIDER)
        if preset in OPENROUTER_PRESETS:
            model = OPENROUTER_PRESETS[preset][tier]
        if overrides and overrides.get(tier):
            model = overrides[tier]
        desired = apply_routes(config, model, effort, route_provider)
        if name == "product-strategist":
            writer = OPENROUTER_PRESETS[preset]["writer"] if preset in OPENROUTER_PRESETS else "gpt-5.6-sol"
            desired["delegation"].update(model=writer, reasoning_effort="high")
        if desired != config:
            changed += 1
            print(f"{name}: {route_provider}/{model}, effort={effort}")
            if apply:
                backup = path.with_name(f"config.yaml.before-models-{stamp}")
                backup.write_text(original, encoding="utf-8")
                backup.chmod(0o600)
                path.write_text(yaml.safe_dump(desired, sort_keys=False), encoding="utf-8")
        else:
            print(f"{name}: already configured")
        if apply and route_provider == "openrouter":
            from post_install import seed_provider_key
            seed_provider_key(path.parent, home / ".env")
    print(f"{changed} profile(s) {'updated' if apply else 'would be updated'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--all", action="store_true")
    choice.add_argument("--team", choices=sorted(p.parent.name for p in (ROOT / "teams").glob("*/team.yaml")))
    choice.add_argument("--profile", action="append", choices=sorted(
        p.name for p in (ROOT / "packages").iterdir() if (p / "config.yaml").is_file()))
    parser.add_argument("--preset", choices=PRESETS, default="codex-pro")
    parser.add_argument("--apply", action="store_true", help="write configs (default: preview)")
    args = parser.parse_args()
    if args.team:
        team = yaml.safe_load((ROOT / "teams" / args.team / "team.yaml").read_text())
        names = [m["name"] for m in [team["orchestrator"], *team["members"]]]
    else:
        names = sorted(p.name for p in (ROOT / "packages").iterdir()
                       if (p / "config.yaml").is_file()) if args.all else args.profile
    return migrate(names, args.preset, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
