#!/usr/bin/env bash
# One command for memory: self-hosted Honcho (LLM jobs on OpenRouter) + wiring of every
# installed hermesworld profile. Safe to re-run; each step is checked and skipped when
# already done. Details and options: docs/MEMORY.md, `python3 tools/memory_setup.py -h`.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
exec python3 tools/memory_setup.py start "$@"
