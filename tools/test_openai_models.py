"""Routing and migration checks; all profile writes use temporary directories."""
from copy import deepcopy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import yaml
from profile_models import ROOT, PROVIDER, ROLES, apply_routes


class RoutingTests(unittest.TestCase):
    def test_memory_preserved_and_old_routes_removed(self):
        config = {
            "memory": {"provider": "honcho", "nudge_interval": 0},
            "honcho": {"host": "user-owned"},
            "tools": {"custom": True},
            "model": {"provider": "openrouter", "base_url": "https://old.invalid", "api_key": "fixture"},
            "agent": {"max_turns": 33, "reasoning_overrides": {"gpt-5.6-sol": "none"}},
            "auxiliary": {"compression": {"provider": "openrouter", "base_url": "https://old.invalid", "api_key": "fixture", "timeout": 12, "extra_body": {"reasoning": {"effort": "none"}}}},
            "delegation": {"provider": "openrouter", "max_iterations": 120},
            "compression": {"provider": "openrouter", "threshold": 0.8},
            "fallback_model": "openrouter/old", "fallback_providers": [{"provider": "openrouter"}],
        }
        untouched = deepcopy(config)
        routed = apply_routes(config, "gpt-5.6-sol", "high")
        self.assertEqual(config, untouched)
        for key in ("memory", "honcho", "tools"):
            self.assertEqual(routed[key], config[key])
        self.assertEqual(routed["agent"], {"max_turns": 33, "reasoning_effort": "high"})
        self.assertEqual(routed["delegation"]["max_iterations"], 120)
        self.assertEqual(routed["fallback_providers"], [])
        self.assertEqual(routed["delegation"]["fallback_providers"], [])
        self.assertNotIn("fallback_model", routed)
        self.assertEqual(routed["compression"]["threshold"], 0.8)
        for block in [routed["model"], routed["delegation"], routed["compression"], *routed["auxiliary"].values()]:
            self.assertEqual(block["provider"], PROVIDER)
            self.assertNotIn("base_url", block)
            self.assertNotIn("api_key", block)
        self.assertEqual(routed["auxiliary"]["compression"]["timeout"], 12)
        self.assertEqual(routed, apply_routes(routed, "gpt-5.6-sol", "high"))

    def test_openrouter_routes_cover_auxiliary_and_children(self):
        cfg = apply_routes({"memory": {"provider": "honcho"}}, "qwen/qwen3.6-plus", "high", "openrouter")
        self.assertEqual(cfg["memory"], {"provider": "honcho"})
        for block in [cfg["model"], cfg["delegation"], *cfg["auxiliary"].values()]:
            self.assertEqual(block["provider"], "openrouter")
        self.assertEqual(cfg["auxiliary"]["title_generation"]["model"], "z-ai/glm-5.3-flash")

    def test_all_shipped_profiles_route_to_subscription(self):
        configs = list((ROOT / "packages").glob("*/config.yaml"))
        self.assertEqual(len(configs), 25)
        for path in configs:
            with self.subTest(profile=path.parent.name):
                cfg = yaml.safe_load(path.read_text())
                self.assertEqual(cfg["model"]["provider"], PROVIDER)
                self.assertEqual(set(cfg["auxiliary"]), set(ROLES))
                for block in [cfg["delegation"], *cfg["auxiliary"].values()]:
                    self.assertEqual(block["provider"], PROVIDER)
                manifest = yaml.safe_load((path.parent / "distribution.yaml").read_text())
                self.assertNotIn("OPENROUTER_API_KEY", [x["name"] for x in manifest["env_requires"]])

    def test_cli_preview_backup_and_idempotence(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            path = home / "profiles/product-strategist/config.yaml"
            path.parent.mkdir(parents=True)
            old = "model:\n  provider: openrouter\n  default: old\nmemory:\n  provider: honcho\n"
            path.write_text(old)
            env = {**os.environ, "HERMES_HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1"}
            command = [sys.executable, str(ROOT / "tools/profile_models.py"), "--profile", "product-strategist"]
            subprocess.run(command, env=env, check=True, capture_output=True)
            self.assertEqual(path.read_text(), old)
            subprocess.run([*command, "--apply"], env=env, check=True, capture_output=True)
            desired = yaml.safe_load(path.read_text())
            self.assertEqual(desired["memory"], {"provider": "honcho"})
            self.assertEqual(desired["delegation"]["model"], "gpt-5.6-sol")
            backups = list(path.parent.glob("config.yaml.before-models-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), old)
            subprocess.run([*command, "--apply"], env=env, check=True, capture_output=True)
            self.assertEqual(len(list(path.parent.glob("config.yaml.before-models-*"))), 1)
            (home / ".env").write_text("OPENROUTER_API_KEY=fixture-key\n")
            subprocess.run([*command, "--preset", "balanced", "--apply"], env=env, check=True, capture_output=True)
            cfg = yaml.safe_load(path.read_text())
            self.assertEqual(cfg["memory"], {"provider": "honcho"})
            self.assertEqual(cfg["model"]["provider"], "openrouter")
            self.assertEqual((path.parent / ".env").read_text().splitlines()[-1], "OPENROUTER_API_KEY=fixture-key")


if __name__ == "__main__":
    unittest.main()
