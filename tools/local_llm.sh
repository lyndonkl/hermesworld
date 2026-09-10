#!/usr/bin/env bash
# Start the local OpenAI-compatible model server that Honcho's memory jobs use.
#
#   tools/local_llm.sh                 # serve the default chat + embedding models on :8000
#   tools/local_llm.sh --check         # is a server answering on the port?
#   LOCAL_LLM_MODEL=mlx-community/Qwen3.8-27B-8bit tools/local_llm.sh   # override
#
# Uses vllm-mlx (https://github.com/waybarrios/vllm-mlx), an OpenAI- and
# Anthropic-compatible server for Apple Silicon. Defaults chosen in docs/MEMORY.md:
#   chat/tools:  mlx-community/Qwen3.8-27B-4bit   (~15 GB; reasoning; tool calling)
#   embeddings:  mlx-community/all-MiniLM-L6-v2-4bit (384 dimensions)
# The first start downloads the models from Hugging Face.
#
# Honcho's own API listens on :8001 (tools/memory_setup.py), so this stays on :8000.
set -euo pipefail

MODEL="${LOCAL_LLM_MODEL:-mlx-community/Qwen3.8-27B-4bit}"
EMBED="${LOCAL_EMBED_MODEL:-mlx-community/all-MiniLM-L6-v2-4bit}"
PORT="${LOCAL_LLM_PORT:-8000}"

if [ "${1:-}" = "--check" ]; then
  if out=$(curl -s -m 3 "http://127.0.0.1:${PORT}/v1/models"); then
    echo "server on :${PORT} -> $(echo "$out" | python3 -c 'import sys,json; print(", ".join(m["id"] for m in json.load(sys.stdin).get("data") or []) or "(no models)")' 2>/dev/null || echo "$out" | head -c 200)"
    exit 0
  fi
  echo "no server answering on :${PORT}"; exit 1
fi

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) ;;
  *) echo "vllm-mlx runs on Apple Silicon only. On other machines run vLLM, Ollama, or LM Studio" >&2
     echo "and point Honcho at it with: python3 tools/memory_setup.py up --local-url http://host.docker.internal:<port>/v1 --local-model <id>" >&2
     exit 1 ;;
esac

if ! command -v vllm-mlx >/dev/null; then
  command -v uv >/dev/null || { echo "uv is required (https://docs.astral.sh/uv/)" >&2; exit 1; }
  echo "installing vllm-mlx with uv tool install..."
  uv tool install vllm-mlx
fi

echo "serving ${MODEL} (+ embeddings ${EMBED}) on http://127.0.0.1:${PORT}/v1"
exec vllm-mlx serve "$MODEL" --port "$PORT" --continuous-batching --embedding-model "$EMBED"
