#!/usr/bin/env python3
"""Self-hosted Honcho memory for every profile in this repo.

One command does everything and is safe to re-run; it checks each step and skips
what is already done:

    tools/memory.sh                        # = python3 tools/memory_setup.py start

`start` = Docker -> Honcho CLI -> env file (all LLM jobs on OpenRouter) -> Honcho
stack on :8001 -> wire every installed profile -> status. The pieces are also
available on their own:

    python3 tools/memory_setup.py up       # start the Honcho stack (Docker) on :8001, LLM jobs on OpenRouter
    python3 tools/memory_setup.py wire     # point every hermesworld profile at it and create their peers
    python3 tools/memory_setup.py status   # what is running and which profiles use Honcho
    python3 tools/memory_setup.py down     # stop the stack (add --wipe to delete its data, --unwire to detach profiles)

What `up` does
  * checks Docker and the Honcho CLI (installs the CLI with `uv tool install honcho-cli`)
  * renders infra/honcho/honcho.env.template into ~/.honcho/profiles/hermes/.env,
    routing every Honcho LLM job (extraction, summaries, dreams, per-turn reasoning,
    embeddings) to OpenRouter models, using the key in ~/.hermes/.env
  * runs `honcho start --profile hermes --api-port 8001` and waits for /health

What `wire` does
  * writes ~/.hermes/honcho.json: baseUrl plus one host block per hermesworld profile
    (`hosts.hermes_<profile>`), all sharing the workspace "hermes" and your user peer,
    each with its own AI peer; specialist Bots get a strong-persona observation preset
  * sets `memory.provider: honcho` in each profile's config.yaml
  * sets `timeout: 120` for Honcho requests (Hermes's default of 30 s drops slow queries)
  * runs `hermes honcho sync`; the AI peers themselves are created on each profile's first chat

Nothing here touches your default ~/.hermes profile unless you pass --include-default.
Reads: teams/*/team.yaml and packages/*/ to know which profiles are ours.
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
import urllib.parse
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
    for manifest in sorted((ROOT / "teams").glob("*/team.yaml")):
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
    key = env_value(HERMES_HOME / ".env", "OPENROUTER_API_KEY")
    if not key:
        sys.exit("no OPENROUTER_API_KEY in ~/.hermes/.env; Honcho's jobs run on OpenRouter. "
                 "Add the key to Hermes first (hermes setup), then re-run.")
    values = {
        "OPENROUTER_API_KEY": key,
        "BASE_URL": args.llm_base_url,
        "FAST_MODEL": args.fast_model,
        "DEEP_MODEL": args.deep_model,
        "EMBED_MODEL": args.embed_model,
        "EMBED_DIMS": str(args.embed_dims),
    }
    text = TEMPLATE.read_text(encoding="utf-8")
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if leftover:
        sys.exit(f"unfilled placeholders in template: {leftover}")
    return text


def ensure_docker() -> None:
    if sh(["docker", "info"]).returncode == 0:
        return
    if sys.platform == "darwin" and Path("/Applications/Docker.app").exists():
        print("  Docker is not running; starting Docker Desktop...")
        subprocess.run(["open", "-a", "Docker"])
        for _ in range(60):
            time.sleep(3)
            if sh(["docker", "info"]).returncode == 0:
                print("  Docker is up")
                return
        sys.exit("Docker Desktop did not come up within 3 minutes; open it by hand and re-run")
    sys.exit("Docker is not running and could not be started. Install/start Docker, then re-run.")


def ensure_honcho_cli() -> None:
    if shutil.which("honcho"):
        return
    if shutil.which("uv") is None:
        sys.exit("Honcho CLI missing and uv not found; install uv, then `uv tool install honcho-cli`.")
    print("  installing honcho-cli...")
    if subprocess.run(["uv", "tool", "install", "honcho-cli"]).returncode != 0:
        sys.exit("could not install honcho-cli")


def write_env(args) -> bool:
    """Render the template into the Honcho profile .env; returns True when the file changed."""
    HONCHO_DIR.mkdir(parents=True, exist_ok=True)
    env_path = HONCHO_DIR / ".env"
    rendered = render_env(args)
    marker = "# --- kept from the previous .env ---"
    if env_path.is_file():
        existing = env_path.read_text(encoding="utf-8")
        managed_before = existing.split(marker)[0]
        if managed_before == rendered:
            return False  # nothing we manage changed; leave the file (and the stack) alone
        ours = {l.split("=", 1)[0] for l in rendered.splitlines() if "=" in l and not l.startswith("#")}
        extra = [l for l in existing.splitlines()
                 if "=" in l and not l.startswith("#") and l.split("=", 1)[0] not in ours]
        if extra:
            rendered += "\n" + marker + "\n" + "\n".join(extra) + "\n"
    env_path.write_text(rendered, encoding="utf-8")
    print(f"  wrote {env_path}")
    return True


def _fix_embedding_dims() -> bool:
    """Honcho's image creates the pgvector columns at 1536 dims; a local embedding model with
    a different size fails startup with 'embedding dim (1536) does not match'. Honcho ships
    scripts/configure_embeddings.py for exactly this; run it inside the API image."""
    logs = sh(["docker", "compose", "-p", f"honcho-{HONCHO_PROFILE}", "logs", "api", "--tail", "80"]).stdout
    if "does not match EMBEDDING_VECTOR_DIMENSIONS" not in logs:
        return False
    print("  pgvector schema dimension differs from the embedding model; reconfiguring (empty tables only)...")
    r = subprocess.run(["docker", "compose", "-p", f"honcho-{HONCHO_PROFILE}", "run", "--rm", "--no-deps",
                        "--entrypoint", "/app/.venv/bin/python", "api", "scripts/configure_embeddings.py", "--yes"],
                       cwd=str(HONCHO_DIR))
    return r.returncode == 0


def start_stack(args) -> None:
    cmd = ["honcho", "start", "--profile", HONCHO_PROFILE, "--api-port", str(args.api_port)]
    print("  $ " + " ".join(cmd))
    if subprocess.run(cmd).returncode != 0:
        if not _fix_embedding_dims() or subprocess.run(cmd).returncode != 0:
            sys.exit("honcho start failed; run it by hand to see the output "
                     f"(docker compose -p honcho-{HONCHO_PROFILE} logs api)")
    base = f"http://127.0.0.1:{args.api_port}"
    for _ in range(60):
        if health(base):
            print(f"  Honcho is up at {base}")
            return
        time.sleep(3)
    sys.exit(f"Honcho did not answer on {base}/health within 3 minutes; check `docker ps` and `honcho doctor`")


def cmd_start(args) -> int:
    print("1/4 Docker"); ensure_docker()
    print("2/4 Honcho CLI"); ensure_honcho_cli()
    print("3/4 Honcho stack")
    changed = write_env(args)
    base = args.base_url
    if health(base) and not changed:
        print(f"  already running at {base}")
    else:
        if health(base) and changed:
            print("  settings changed; restarting the stack")
            subprocess.run(["honcho", "stop", "--profile", HONCHO_PROFILE])
        start_stack(args)
    print("4/4 wire profiles")
    cfg_path = HERMES_HOME / "honcho.json"
    hosts = (json.loads(cfg_path.read_text()) if cfg_path.is_file() else {}).get("hosts", {})
    pending = []
    for p in our_profiles():
        c_path = HERMES_HOME / "profiles" / p["name"] / "config.yaml"
        if not c_path.is_file():
            continue
        prov = ((yaml.safe_load(c_path.read_text()) or {}).get("memory") or {}).get("provider")
        if prov != "honcho" or host_key(p["name"]) not in hosts:
            pending.append(p["name"])
    if pending:
        args.profiles = pending
        cmd_wire(args)
    else:
        print("  all installed profiles already wired")
        if cfg_path.is_file():
            cfg = json.loads(cfg_path.read_text())
            if apply_tuning(cfg):
                cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
                print("  cadence tuning added to existing host blocks")
    print()
    return cmd_status(args)


def cmd_up(args) -> int:
    ensure_docker()
    ensure_honcho_cli()
    write_env(args)
    if args.no_start:
        return 0
    start_stack(args)
    print(f"  next: python3 tools/memory_setup.py wire --base-url {args.base_url}")
    return 0


# ---------------------------------------------------------------- wire

# Hermes-side cadence per kind of profile. The dialectic is an LLM call before a reply,
# so specialists (which mostly execute a fixed procedure) ask for it less often and at the
# lightest level; the orchestrator and standalone agents keep the default level.
#
# contextTokens is the budget for the memory block Hermes attaches to every turn. Hermes fills
# it in a fixed order (session summary, facts about the user, cards, the dialectic) and cuts
# at the budget. Measured on real turns: the session summary alone runs to ~11,000 characters
# (~2,750 tokens), the fact list 700-900 tokens, the dialectic up to 150; at the old 1,600
# the cut landed inside the summary and everything after it, including the dialectic that
# had just been paid for, was dropped. 6,000 fits the whole block with headroom.
TUNING = {
    "member": {"dialecticCadence": 4, "dialecticReasoningLevel": "minimal", "contextTokens": 6000},
    "orchestrator": {"dialecticCadence": 3, "dialecticReasoningLevel": "low", "contextTokens": 6000},
    "standalone": {"dialecticCadence": 3, "dialecticReasoningLevel": "low", "contextTokens": 6000},
}
# Values this script wrote in earlier versions. A block still carrying one of them is updated to
# the current default; any other value is a hand edit and is left alone.
SUPERSEDED = {"contextTokens": {1200, 1600}}


def apply_tuning(cfg: dict) -> int:
    hosts = cfg.setdefault("hosts", {})
    n = 0
    for p in our_profiles():
        block = hosts.get(host_key(p["name"]))
        if not isinstance(block, dict):
            continue
        for k, v in TUNING[p["kind"]].items():
            if k not in block or block[k] in SUPERSEDED.get(k, ()):
                if block.get(k) != v:
                    block[k] = v
                    n += 1
    return n


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
    # Hermes gives a Honcho request 30 s by default and drops the result on timeout; the per-turn
    # query runs several tool rounds on a cloud model and often needs 20-50 s.
    cfg.setdefault("timeout", 120)
    hosts = cfg.setdefault("hosts", {})
    if args.include_default:
        hosts.setdefault(HOST_ROOT, {}).update({"enabled": True, "aiPeer": HOST_ROOT, "workspace": WORKSPACE, "peerName": peer})
    elif HOST_ROOT not in hosts:
        # `hermes honcho sync` inherits from the default block and refuses without one; keep the
        # default ~/.hermes profile itself detached (enabled: false).
        hosts[HOST_ROOT] = {"enabled": False, "aiPeer": HOST_ROOT, "workspace": WORKSPACE, "peerName": peer}
    for p in wanted:
        block = hosts.setdefault(host_key(p["name"]), {})
        block.update({"enabled": True, "aiPeer": p["name"], "workspace": WORKSPACE, "peerName": peer})
        if p["kind"] == "member":
            block.setdefault("observation", STRONG_PERSONA)
    apply_tuning(cfg)
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {cfg_path} ({len(wanted)} host block(s), workspace '{WORKSPACE}', user peer '{peer}')")

    for p in wanted:
        c_path = HERMES_HOME / "profiles" / p["name"] / "config.yaml"
        c = yaml.safe_load(c_path.read_text(encoding="utf-8")) or {}
        mem = c.get("memory") or {}
        changed = False
        if mem.get("provider") != "honcho":
            mem["provider"] = "honcho"
            changed = True
        if mem.get("nudge_interval") != 0:
            mem["nudge_interval"] = 0   # Honcho extracts on its own; the built-in nudge would double up
            changed = True
        if changed:
            c["memory"] = mem
            c_path.write_text(yaml.safe_dump(c, sort_keys=False), encoding="utf-8")
    print(f"  memory.provider: honcho and nudge_interval: 0 set on {len(wanted)} profile(s)")

    first = wanted[0]["name"]
    print(f"  $ hermes -p {first} honcho sync   (registers the profiles; AI peers are created on first chat)")
    r = subprocess.run(["hermes", "-p", first, "honcho", "sync"], text=True)
    if r.returncode != 0:
        print("  sync did not complete; peers are created lazily on first chat, so this is not fatal")
    print("  done. Verify with: python3 tools/memory_setup.py status")
    return 0


# ---------------------------------------------------------------- status / down

def cmd_status(args) -> int:
    base = args.base_url
    print(f"Honcho API {base}: {'up' if health(base) else 'DOWN'}")
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
    ap.add_argument("command", choices=["start", "up", "wire", "status", "down"])
    ap.add_argument("--api-port", type=int, default=8001, help="host port for the Honcho API (default 8001; :8000 is the model server)")
    ap.add_argument("--base-url", default="http://127.0.0.1:8001", help="Honcho API URL as seen from Hermes")
    ap.add_argument("--llm-base-url", default="https://openrouter.ai/api/v1", help="OpenAI-compatible endpoint for every Honcho job")
    ap.add_argument("--fast-model", default="z-ai/glm-5.3-flash",
                    help="extraction, summaries, dreams, dialectic minimal/low/medium")
    ap.add_argument("--deep-model", default="z-ai/glm-5.3", help="dialectic high/max")
    ap.add_argument("--embed-model", default="openai/text-embedding-3-small")
    ap.add_argument("--embed-dims", type=int, default=1536, help="must match the embedding model")
    ap.add_argument("--no-start", action="store_true", help="up: render the env file but do not start the stack")
    ap.add_argument("--peer-name", help="wire: your user peer name (default: $USER)")
    ap.add_argument("--profiles", type=lambda s: [x.strip() for x in s.split(",") if x.strip()], help="wire: subset, comma-separated")
    ap.add_argument("--include-default", action="store_true", help="wire: also attach the default ~/.hermes profile")
    ap.add_argument("--wipe", action="store_true", help="down: delete the stack's database volumes")
    ap.add_argument("--unwire", action="store_true", help="down: remove Honcho from the profiles' config and honcho.json")
    args = ap.parse_args()
    return {"start": cmd_start, "up": cmd_up, "wire": cmd_wire, "status": cmd_status, "down": cmd_down}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
