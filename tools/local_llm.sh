#!/usr/bin/env bash
# The local OpenAI-compatible model server that Honcho's memory jobs use.
#
#   tools/local_llm.sh                 # run in the foreground on :8000
#   tools/local_llm.sh --install-agent # install + start a macOS LaunchAgent (keeps it running, survives reboots)
#   tools/local_llm.sh --status        # agent state and whether the server answers
#   tools/local_llm.sh --check         # exit 0 if a server answers on the port
#   tools/local_llm.sh --stop          # stop and remove the LaunchAgent
#   LOCAL_LLM_MODEL=mlx-community/Qwen3.8-27B-8bit tools/local_llm.sh --install-agent   # override
#
# Uses vllm-mlx (https://github.com/waybarrios/vllm-mlx), an OpenAI- and Anthropic-
# compatible server for Apple Silicon. Defaults chosen in docs/MEMORY.md:
#   chat/tools:  mlx-community/Qwen3.8-27B-4bit     (~15 GB; reasoning; tool calling)
#   embeddings:  mlx-community/all-MiniLM-L6-v2-4bit (384 dimensions)
# The first start downloads the models from Hugging Face; watch the log.
# Honcho's own API listens on :8001 (tools/memory_setup.py), so this stays on :8000.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="${LOCAL_LLM_MODEL:-mlx-community/Qwen3.8-27B-4bit}"
EMBED="${LOCAL_EMBED_MODEL:-mlx-community/all-MiniLM-L6-v2-4bit}"
PORT="${LOCAL_LLM_PORT:-8000}"
LABEL="com.hermesworld.local-llm"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/hermesworld-local-llm.log"

check() {
  out=$(curl -s -m 3 "http://127.0.0.1:${PORT}/v1/models" 2>/dev/null) || return 1
  echo "$out" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(", ".join(m["id"] for m in d.get("data") or []) or "(no models yet)")' 2>/dev/null
}

ensure_binary() {
  if ! command -v vllm-mlx >/dev/null; then
    command -v uv >/dev/null || { echo "uv is required (https://docs.astral.sh/uv/)" >&2; exit 1; }
    echo "installing vllm-mlx with uv tool install..."
    uv tool install vllm-mlx
  fi
}

require_apple_silicon() {
  case "$(uname -s)-$(uname -m)" in
    Darwin-arm64) ;;
    *) echo "vllm-mlx runs on Apple Silicon only. Elsewhere run vLLM, Ollama or LM Studio and point Honcho at it:" >&2
       echo "  python3 tools/memory_setup.py start --local-url http://host.docker.internal:<port>/v1 --local-model <id>" >&2
       exit 1 ;;
  esac
}

install_agent() {
  require_apple_silicon; ensure_binary
  mkdir -p "$(dirname "$PLIST")" "$(dirname "$LOG")"
  local bin; bin="$(command -v vllm-mlx)"
  cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$bin</string><string>serve</string><string>$MODEL</string>
    <string>--port</string><string>$PORT</string>
    <string>--continuous-batching</string>
    <string>--embedding-model</string><string>$EMBED</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>ThrottleInterval</key><integer>30</integer>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
EOF
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null || launchctl load -w "$PLIST"
  echo "LaunchAgent installed: $PLIST"
  echo "serving $MODEL (+ embeddings $EMBED) on http://127.0.0.1:${PORT}/v1 ; log: $LOG"
}

case "${1:-}" in
  --check)
    if models=$(check); then echo "server on :${PORT} -> $models"; exit 0; fi
    echo "no server answering on :${PORT}"; exit 1 ;;
  --status)
    if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then echo "LaunchAgent: loaded ($PLIST)"; else echo "LaunchAgent: not installed"; fi
    if models=$(check); then echo "server on :${PORT} -> $models"; else echo "server on :${PORT}: not answering (loading or down; tail -f $LOG)"; fi
    exit 0 ;;
  --install-agent) install_agent; exit 0 ;;
  --stop)
    launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || launchctl unload -w "$PLIST" >/dev/null 2>&1 || true
    rm -f "$PLIST"; echo "LaunchAgent stopped and removed"; exit 0 ;;
  --uninstall-agent) "$0" --stop; exit 0 ;;
  -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
  "") ;;
  *) echo "unknown option: $1" >&2; exit 2 ;;
esac

require_apple_silicon; ensure_binary
echo "serving ${MODEL} (+ embeddings ${EMBED}) on http://127.0.0.1:${PORT}/v1"
exec vllm-mlx serve "$MODEL" --port "$PORT" --continuous-batching --embedding-model "$EMBED"
