#!/usr/bin/env python3
"""Self-hosted Honcho memory for every profile in this repo, in four commands.

    python3 tools/memory_setup.py up       # start the Honcho stack (Docker) on :8001, LLM jobs on your local model
    python3 tools/memory_setup.py wire     # point every hermesworld profile at it and create their peers
    python3 tools/memory_setup.py status   # what is running and which profiles use Honcho
    python3 tools/memory_setup.py down     # stop the stack (add --wipe to delete its data, --unwire to detach profiles)

What `up` does
  * checks Docker and the Honcho CLI (installs the CLI with `uv tool install honcho-cli`)
  * renders infra/honcho/honcho.env.template into ~/.honcho/profiles/hermes/.env,
    routing Honcho's LLM jobs to the local server from tools/local_llm.sh and, when an
    OpenRouter key exists in ~/.hermes/.env, the two heavy dialectic levels to a cheap
    cloud model (docs/MEMORY.md explains the split)
  * runs `honcho start --profile hermes --api-port 8001` and waits for /health

What `wire` does
  * writes ~/.hermes/honcho.json: baseUrl plus one host block per hermesworld profile
    (`hosts.hermes_<profile>`), all sharing the workspace "hermes" and your user peer,
    each with its own AI peer; specialist Bots get a strong-persona observation preset
  * sets `memory.provider: honcho` in each profile's config.yaml
  * runs `hermes honcho sync` to create the peers on the server

Nothing here touches your default ~/.hermes profile unless you pass --include-default.
Reads: teams/*-team.yaml and packages/*/ to know which profiles are ours.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
HONCHO_PROFILE = "hermes"
HONCHO_DIR = Path.home() / ".honcho" / "profiles" / HONCHO_PROFILE
TEMPLATE = ROOT / "infra" / "honcho" / "honcho.env.template"
WORKSPACE = "hermes"
HOST_ROOT = "hermes"  # Hermes's host key for the default profile; named profiles are hermes_<name>

STRONG_PERSONA = {"user": {"observeMe": True, "observeOthers": True},
                  "ai": {"observeMe": False, "observeOthers": True}}


# ---------------------------------------------------------------- profiles

def our_profiles() -> list[dict]:
    """Every installable package: name, kind (orchestrator|member|standalone)."""
    out, orchestrators = [], set()
    for manifest in sorted((ROOT / "teams").glob("*-team.yaml")):
        team = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        orchestrators.add(team["orchestrator"]["name"])
    for pkg in sorted(p for p in (ROOT / "packages").iterdir() if (p / "distribution.yaml").is_file()):
        if pkg.name in orchestrators:
            kind = "orchestrator"
        elif (pkg / "bot.yaml").is_file():
            kind = "member"
        else:
            kind = "standalone"
        out.append({"name": pkg.name, "kind": kind})
    return out


def host_key(profile: str) -> str:
    sanitized = "".join(c if c.isalnum() or c in "_-" else "_" for c in profile).strip("_")
    return f"{HOST_ROOT}_{sanitized or 'profile'}"


def installed(profile: str) -> bool:
    return (HERMES_HOME / "profiles" / profile / "config.yaml").is_file()


# ---------------------------------------------------------------- helpers

def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


def env_value(path: Path, key: str) -> str:
    if not path.is_file():
        return ""
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith(f"{key}=") and not line.startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def health(base_url: str, timeout: float = 3.0) -> bool:
    try:
        with urllib.request.urlopen(f"{base_url.rstrip('/')}/health", timeout=timeout) as r:
            return 200 <= r.status < 300
    except Exception:
        return False


# ---------------------------------------------------------------- up

def render_env(args) -> str:
    key = "" if args.dialectic_high == "local" else env_value(HERMES_HOME / ".env", "OPENROUTER_API_KEY")
    if args.dialectic_high != "local" and not key:
        print("  no OPENROUTER_API_KEY in ~/.hermes/.env: dialectic high/max will run locally too")
    cloud = bool(key)
    values = {
        "OPENROUTER_API_KEY": key,
        "LOCAL_LLM_BASE_URL": args.local_url,
        "LOCAL_LLM_MODEL": args.local_model,
        "LOCAL_EMBED_MODEL": args.embed_model,
        "LOCAL_EMBED_DIMS": str(args.embed_dims),
        "DIALECTIC_HIGH_MODEL": args.dialectic_high if cloud else args.local_model,
        "DIALECTIC_HIGH_BASE_URL": "https://openrouter.ai/api/v1" if cloud else args.local_url,
        "DIALECTIC_HIGH_KEY_ENV": "LLM_OPENROUTER_API_KEY" if cloud else "LLM_OPENAI_API_KEY",
    }
    text = TEMPLATE.read_text(encoding="utf-8")
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if leftover:
        sys.exit(f"unfilled placeholders in template: {leftover}")
    return text


def cmd_up(args) -> int:
    if sh(["docker", "info"]).returncode != 0:
        sys.exit("Docker is not running. Start Docker Desktop (or another daemon), then re-run.")
    if shutil.which("honcho") is None:
        if shutil.which("uv") is None:
            sys.exit("Honcho CLI missing and uv not found; install uv, then `uv tool install honcho-cli`.")
        print("installing honcho-cli...")
        if subprocess.run(["uv", "tool", "install", "honcho-cli"]).returncode != 0:
            sys.exit("could not install honcho-cli")
    local_check = args.local_url.replace("host.docker.internal", "127.0.0.1")
    if not health_models(local_check):
        print(f"  warning: no model server answering at {local_check} — start tools/local_llm.sh "
              f"in another terminal, or Honcho's LLM jobs will fail until it is up")
    HONCHO_DIR.mkdir(parents=True, exist_ok=True)
    env_path = HONCHO_DIR / ".env"
    rendered = render_env(args)
    if env_path.is_file():
        ours = {l.split("=", 1)[0] for l in rendered.splitlines() if "=" in l and not l.startswith("#")}
        extra = [l for l in env_path.read_text(encoding="utf-8").splitlines()
                 if "=" in l and not l.startswith("#") and l.split("=", 1)[0] not in ours]
        if extra:
            rendered += "\n# --- kept from the previous .env ---\n" + "\n".join(extra) + "\n"
            print(f"  kept {len(extra)} existing setting(s) not managed by the template")
    env_path.write_text(rendered, encoding="utf-8")
    print(f"  wrote {env_path}")
    if args.no_start:
        return 0
    cmd = ["honcho", "start", "--profile", HONCHO_PROFILE, "--api-port", str(args.api_port)]
    print("  $ " + " ".join(cmd))
    if subprocess.run(cmd).returncode != 0:
        sys.exit("honcho start failed; run it by hand to see the wizard/output")
    base = f"http://127.0.0.1:{args.api_port}"
    for _ in range(60):
        if health(base):
            print(f"  Honcho is up at {base}")
            print(f"  next: python3 tools/memory_setup.py wire --base-url {base}")
            return 0
        time.sleep(3)
    sys.exit(f"Honcho did not answer on {base}/health within 3 minutes; check `docker ps` and `honcho doctor`")


def health_models(base_url: str) -> bool:
    try:
        with urllib.request.urlopen(f"{base_url.rstrip('/')}/models", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


# ---------------------------------------------------------------- wire

def cmd_wire(args) -> int:
    base = args.base_url
    if not health(base):
        sys.exit(f"Honcho is not answering at {base}; run `python3 tools/memory_setup.py up` first")
    peer = args.peer_name or os.environ.get("USER") or "user"
    wanted = [p for p in our_profiles() if (not args.profiles or p["name"] in args.profiles)]
    missing = [p["name"] for p in wanted if not installed(p["name"])]
    if missing:
        print(f"  skipping {len(missing)} profile(s) not installed: {', '.join(missing)}")
    wanted = [p for p in wanted if installed(p["name"])]
    if not wanted:
        sys.exit("no installed hermesworld profiles found; run tools/install.sh first")

    cfg_path = HERMES_HOME / "honcho.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    cfg["baseUrl"] = base
    hosts = cfg.setdefault("hosts", {})
    if args.include_default:
        hosts.setdefault(HOST_ROOT, {}).update({"enabled": True, "aiPeer": HOST_ROOT, "workspace": WORKSPACE, "peerName": peer})
    for p in wanted:
        block = hosts.setdefault(host_key(p["name"]), {})
        block.update({"enabled": True, "aiPeer": p["name"], "workspace": WORKSPACE, "peerName": peer})
        if p["kind"] == "member":
            block.setdefault("observation", STRONG_PERSONA)
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {cfg_path} ({len(wanted)} host block(s), workspace '{WORKSPACE}', user peer '{peer}')")

    for p in wanted:
        c_path = HERMES_HOME / "profiles" / p["name"] / "config.yaml"
        c = yaml.safe_load(c_path.read_text(encoding="utf-8")) or {}
        mem = c.get("memory") or {}
        if mem.get("provider") != "honcho":
            mem["provider"] = "honcho"
            c["memory"] = mem
            c_path.write_text(yaml.safe_dump(c, sort_keys=False), encoding="utf-8")
    print(f"  memory.provider: honcho set on {len(wanted)} profile(s)")

    first = wanted[0]["name"]
    print(f"  $ hermes -p {first} honcho sync   (creates the AI peers on the server)")
    r = subprocess.run(["hermes", "-p", first, "honcho", "sync"], text=True)
    if r.returncode != 0:
        print("  sync did not complete; peers are created lazily on first chat, so this is not fatal")
    print("  done. Verify with: python3 tools/memory_setup.py status")
    return 0


# ---------------------------------------------------------------- status / down

def cmd_status(args) -> int:
    base = args.base_url
    print(f"Honcho API {base}: {'up' if health(base) else 'DOWN'}")
    local = args.local_url.replace("host.docker.internal", "127.0.0.1")
    print(f"local model server {local}: {'up' if health_models(local) else 'DOWN'}")
    if shutil.which("honcho"):
        r = sh(["honcho", "doctor"], env={**os.environ, "HONCHO_BASE_URL": base})
        print("honcho doctor:", (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else f"exit {r.returncode}")
    cfg_path = HERMES_HOME / "honcho.json"
    hosts = (json.loads(cfg_path.read_text()) if cfg_path.is_file() else {}).get("hosts", {})
    print(f"\n{'profile':<36} {'installed':<10} {'provider':<9} host block")
    for p in our_profiles():
        c_path = HERMES_HOME / "profiles" / p["name"] / "config.yaml"
        prov = "-"
        if c_path.is_file():
            prov = ((yaml.safe_load(c_path.read_text()) or {}).get("memory") or {}).get("provider", "builtin")
        print(f"{p['name']:<36} {'yes' if c_path.is_file() else 'no':<10} {prov:<9} {'yes' if host_key(p['name']) in hosts else 'no'}")
    return 0


def cmd_down(args) -> int:
    if shutil.which("honcho"):
        cmd = ["honcho", "stop", "--profile", HONCHO_PROFILE] + (["--wipe"] if args.wipe else [])
        print("  $ " + " ".join(cmd))
        subprocess.run(cmd)
    if args.unwire:
        cfg_path = HERMES_HOME / "honcho.json"
        if cfg_path.is_file():
            cfg = json.loads(cfg_path.read_text())
            for p in our_profiles():
                (cfg.get("hosts") or {}).pop(host_key(p["name"]), None)
            cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        n = 0
        for p in our_profiles():
            c_path = HERMES_HOME / "profiles" / p["name"] / "config.yaml"
            if not c_path.is_file():
                continue
            c = yaml.safe_load(c_path.read_text()) or {}
            if (c.get("memory") or {}).get("provider") == "honcho":
                c["memory"].pop("provider")
                if not c["memory"]:
                    c.pop("memory")
                c_path.write_text(yaml.safe_dump(c, sort_keys=False), encoding="utf-8")
                n += 1
        print(f"  detached {n} profile(s); built-in memory keeps working")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["up", "wire", "status", "down"])
    ap.add_argument("--api-port", type=int, default=8001, help="host port for the Honcho API (default 8001; :8000 is the model server)")
    ap.add_argument("--base-url", default="http://127.0.0.1:8001", help="Honcho API URL as seen from Hermes")
    ap.add_argument("--local-url", default="http://host.docker.internal:8000/v1",
                    help="local OpenAI-compatible server as seen from inside Docker")
    ap.add_argument("--local-model", default="mlx-community/Qwen3.8-27B-4bit")
    ap.add_argument("--embed-model", default="mlx-community/all-MiniLM-L6-v2-4bit")
    ap.add_argument("--embed-dims", type=int, default=384, help="must match the embedding model (MiniLM 384, embeddinggemma 768)")
    ap.add_argument("--dialectic-high", default="z-ai/glm-5.3-flash",
                    help="OpenRouter model for dialectic high/max, or 'local' to keep everything on the local server")
    ap.add_argument("--no-start", action="store_true", help="up: render the env file but do not start the stack")
    ap.add_argument("--peer-name", help="wire: your user peer name (default: $USER)")
    ap.add_argument("--profiles", type=lambda s: [x.strip() for x in s.split(",") if x.strip()], help="wire: subset, comma-separated")
    ap.add_argument("--include-default", action="store_true", help="wire: also attach the default ~/.hermes profile")
    ap.add_argument("--wipe", action="store_true", help="down: delete the stack's database volumes")
    ap.add_argument("--unwire", action="store_true", help="down: remove Honcho from the profiles' config and honcho.json")
    args = ap.parse_args()
    return {"up": cmd_up, "wire": cmd_wire, "status": cmd_status, "down": cmd_down}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
