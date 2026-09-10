#!/usr/bin/env python3
"""Post-install step run by tools/install.sh after `hermes profile install`.

    python3 tools/post_install.py <package dir> <profile dir> [<root config.yaml>]

1. Seeds the profile's `model:` block from the root profile's config.yaml when the
   package ships no model pin. Mirrors hermes_cli.profiles._seed_model_config.
1b. Seeds the API key(s) the pinned provider needs into the profile's .env from the
   root profile's .env when missing. Named profiles are credential-isolated (their
   HERMES_HOME has its own .env), so without this a fresh profile gets HTTP 401
   from the provider even though the root profile works.
2. For Bot-team members (packages that carry a bot.yaml), writes the profile's Bot
   metadata into profile.yaml: `description` and `ui_meta.hermes-bots.title`.
   Hermes reads exactly these two fields to (a) treat the profile as a Bot and
   (b) build the "who does what" roster line every teammate sees
   (tools/bot_mode_probe.py in the Hermes source). Only missing values are
   filled in, so titles, avatars and sections set in the desktop survive
   `hermes profile update` and re-runs of this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("  PyYAML missing: skipped model seeding and Bot metadata (python3 -m pip install pyyaml)")
    sys.exit(0)


def seed_model(profile: Path, root_cfg: Path) -> None:
    cfg_path = profile / "config.yaml"
    cfg = (yaml.safe_load(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}) or {}
    if cfg.get("model") or not root_cfg.is_file():
        return
    root = yaml.safe_load(root_cfg.read_text(encoding="utf-8")) or {}
    if not root.get("model"):
        return
    cfg = {"model": root["model"], **cfg}
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    print(f"  seeded model block from {root_cfg}")


# Provider -> the env var(s) Hermes reads for it (hermes_cli config docs / cli-config.yaml.example).
PROVIDER_KEYS = {
    "openrouter": ["OPENROUTER_API_KEY"], "anthropic": ["ANTHROPIC_API_KEY"], "openai": ["OPENAI_API_KEY"],
    "gemini": ["GEMINI_API_KEY", "GOOGLE_API_KEY"], "zai": ["GLM_API_KEY"], "kimi-coding": ["KIMI_API_KEY"],
    "minimax": ["MINIMAX_API_KEY"], "nous-api": ["NOUS_API_KEY"], "huggingface": ["HF_TOKEN"],
    "nvidia": ["NVIDIA_API_KEY"], "deepinfra": ["DEEPINFRA_API_KEY"], "copilot": ["GITHUB_TOKEN"],
    "ai-gateway": ["AI_GATEWAY_API_KEY"], "kilocode": ["KILOCODE_API_KEY"],
}


def _env_lines(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out


def seed_provider_key(profile: Path, root_env: Path) -> None:
    """Named profiles are credential-isolated: their .env is the only .env Hermes reads for
    them. Copy the API key(s) the pinned provider needs from the root profile when missing."""
    cfg_path = profile / "config.yaml"
    cfg = (yaml.safe_load(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}) or {}
    model = cfg.get("model") or {}
    provider = (model.get("provider") if isinstance(model, dict) else "") or ""
    keys = PROVIDER_KEYS.get(provider, [])
    delegation = cfg.get("delegation") or {}
    keys += PROVIDER_KEYS.get(delegation.get("provider") or "", [])
    root = _env_lines(root_env)
    have = _env_lines(profile / ".env")
    to_copy = [k for k in dict.fromkeys(keys) if k not in have and root.get(k)]
    if not to_copy:
        return
    env_path = profile / ".env"
    header = "" if env_path.is_file() else "# Per-profile secrets for this Hermes profile (seeded from the root profile by tools/post_install.py).\n"
    with env_path.open("a", encoding="utf-8") as fh:
        fh.write(header + "".join(f"{k}={root[k]}\n" for k in to_copy))
    env_path.chmod(0o600)
    print(f"  seeded {', '.join(to_copy)} into {env_path} from the root profile")


def write_bot_meta(pkg: Path, profile: Path) -> None:
    bot_path = pkg / "bot.yaml"
    if not bot_path.is_file():
        return
    bot = yaml.safe_load(bot_path.read_text(encoding="utf-8")) or {}
    meta_path = profile / "profile.yaml"
    meta = (yaml.safe_load(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}) or {}
    changed = False
    if not meta.get("description") and bot.get("description"):
        meta["description"] = bot["description"]
        changed = True
    ui = meta.get("ui_meta")
    if not isinstance(ui, dict):
        ui = {}
        meta["ui_meta"] = ui
    bots = ui.get("hermes-bots")
    if not isinstance(bots, dict):
        bots = {}
        ui["hermes-bots"] = bots
        changed = True
    if not bots.get("title") and bot.get("title"):
        bots["title"] = bot["title"]
        changed = True
    if changed:
        meta_path.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"  Bot metadata written: {bot.get('title')} (tier {bot.get('tier')})")


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    pkg, profile = Path(argv[1]), Path(argv[2])
    root_cfg = Path(argv[3]) if len(argv) > 3 else Path.home() / ".hermes" / "config.yaml"
    if not profile.is_dir():
        print(f"  profile directory not found: {profile}")
        return 1
    seed_model(profile, root_cfg)
    seed_provider_key(profile, root_cfg.parent / ".env")
    write_bot_meta(pkg, profile)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
