# Memory for these agents: self-hosted Honcho, models on OpenRouter

How to give every profile in this repo a shared, persistent model of you. The memory
server runs on your machine in Docker; its model calls go to cheap OpenRouter models. The
choice between Honcho and Mem0, and what each learns, is discussed at the end of
[MODELS.md](MODELS.md#memory-providers-briefly); this page is the how-to.

## The decision in one paragraph

Honcho runs one **user peer** shared by every profile and one **AI peer** per
profile, so the valuation team's fifteen Bots learn one model of you while each
keeps its own conclusions. Its server does its own LLM work in four jobs. A *deriver* turns each message
into observations and updates the representations. A *summariser* condenses
sessions. *Dreams* consolidate when the system is idle. The *dialectic* answers
"what does this person want right now" for Hermes to inject each turn. Hermes
allows one external provider per profile, and all of that server-side work can be
pointed at any OpenAI-compatible endpoint per job, which is what makes a local
model practical.

## Which models Honcho uses, and why not a local one

Honcho's server makes its own LLM calls: tool calling in the OpenAI format for the
deriver, dialectic and dream jobs, JSON output for the deriver, plus an embedding
model. Its defaults are mini-class cloud models, so the jobs are designed for small,
fast models, not frontier ones. The set-up routes them like this:

| Honcho job | Model (OpenRouter id) | Why | Price per 1M tokens in / out |
|---|---|---|---|
| Deriver, summaries, dreams | `z-ai/glm-5.3-flash` | Runs on every message; needs tool calling and JSON, not depth; GDPval-AA 1669 | 0.07 / 0.23 |
| Dialectic minimal, low, medium | `z-ai/glm-5.3-flash` | Runs before a reply, so the conversation waits on it; answers in seconds | 0.07 / 0.23 |
| Dialectic high, max | `z-ai/glm-5.3` | Multi-step reasoning when a Bot explicitly asks for depth; Intelligence Index 45 | 1.40 / 4.40 |
| Embeddings | `openai/text-embedding-3-small` | 1536 dimensions, Honcho's default schema; served through OpenRouter's `/v1/embeddings` | about 0.02 |

At the volumes an individual produces this is cents per day. Change any of them with
`tools/memory.sh --fast-model ... --deep-model ... --embed-model ... --embed-dims ...`;
a different embedding size means starting the database again
(`python3 tools/memory_setup.py down --wipe`).

**A local model was tried and removed.** On an M3 Max with 96 GB, a 27B reasoning
model served through vllm-mlx handled the background jobs, but the per-turn dialectic
queued behind them at 70 to 200 seconds per call, and the laptop ran hot. The
existing Qwen3-Coder build on that machine was also unsuitable on its own: a coding
specialist without reasoning, Intelligence Index 10. If you still want local
inference, pass `--llm-base-url http://host.docker.internal:<port>/v1` and the model
ids of any OpenAI-compatible server that supports tool calling; expect the latency
above unless the machine is dedicated to it.

## Set-up: one command

Prerequisites: Docker Desktop installed (the command starts it); `uv` installed;
Hermes profiles installed from this repo (`tools/install.sh --all`); an OpenRouter
key already configured in Hermes; Python 3 with PyYAML.

```bash
tools/memory.sh --peer-name "Your Name"
```

Every step is checked first and skipped when already done, so the same command is
the installer, the restart after a reboot, and the health check:

1. **Docker.** Starts Docker Desktop if it is not running.
2. **Honcho CLI.** `uv tool install honcho-cli` if missing.
3. **Honcho stack.** Renders `infra/honcho/honcho.env.template` into
   `~/.honcho/profiles/hermes/.env` with your OpenRouter key and the models above,
   then `honcho start --profile hermes --api-port 8001` unless it is already healthy.
   If the rendered settings changed, the stack is restarted.
4. **Wiring.** For every installed hermesworld profile not yet attached: a
   `hosts.hermes_<profile>` block in `~/.hermes/honcho.json`, `memory.provider: honcho`
   in the profile's `config.yaml`, then `hermes honcho sync` to create the AI peers.
   Your default `~/.hermes` profile is left alone unless you pass `--include-default`.

Then a status table: Honcho health and, per profile, whether it is installed, its
provider, and whether it has a host block.

Secrets stay on your machine. The Honcho `.env` under `~/.honcho/profiles/hermes/`
and each profile's `.env` are written with mode 600 and are never part of this
repository; the only env file in the repo is the placeholder template.

Honcho's containers restart with Docker Desktop; enable "Start Docker Desktop when
you sign in" and memory is back after a reboot without any command.

## What each profile is set to observe

| Profiles | Observation | Effect |
|---|---|---|
| `valuation-orchestrator`, `superforecaster`, `product-strategist`, `cognitive-design-architect`, `geometric-deep-learning-architect` | directional (Honcho default): both peers observe themselves and each other | Full model of you; the agent also builds a self-model from its replies |
| The 14 specialist Bots | strong persona: the AI peer observes you but not itself | Their SOUL is the persona; they should not drift by re-modelling themselves from their own stage reports |

Change any block in `~/.hermes/honcho.json`; the keys are documented in the Hermes
Honcho page (`observation`, `recallMode`, `contextTokens`, `dialecticCadence`,
`dialecticDepth`, `sessionStrategy`).

## What gets learned, and what does not

Learned: preferences, habits and goals inferred from how you talk. Facts you
state, kept on your peer card. A running summary of each session. Conclusions the
server reasons out over time. And, for the directional profiles, a self-model of
the agent. All of it lives in the Postgres volume of the Honcho stack on your
machine.

Not learned: the valuation method, the gates, the scripts, or anything about how
to do the work. Those stay in the briefs and skills, which is why improving an
agent is still an edit to this repo. Run artifacts stay in the workspace on disk.
The built-in `MEMORY.md` and `USER.md` keep working underneath; Honcho mirrors the
agent's own memory writes.

## Capacity

The dialectic is the one job the conversation waits on: Hermes asks for it every
few turns before replying. The set-up therefore keeps it on the fast model with
output caps per level, and asks for it less often on specialist Bots
(`dialecticCadence` 4 at level `minimal`) than on the orchestrator and standalone
agents (cadence 3 at `low`). All of those are per-profile keys in
`~/.hermes/honcho.json` and can be changed by hand.

## Limits to know

- One external provider per profile; Honcho and Mem0 cannot share a profile.
- The injected dialectic is capped at 600 characters by default
  (`dialecticMaxChars`); the base context is uncapped unless you set `contextTokens`.
- Embedding dimensions are fixed at stack creation. Changing the embedding model
  later means `python3 tools/memory_setup.py down --wipe` and starting over.
- Sessions map to directories by default (`sessionStrategy: per-directory`), so a
  valuation run's workspace becomes its own Honcho session.

## Troubleshooting and undo

| Symptom | Fix |
|---|---|
| `up` says Docker is not running | Start Docker Desktop, re-run (`tools/memory.sh` starts it for you on macOS) |
| API container unhealthy, log says "embedding dim (1536) does not match" | The image creates pgvector columns at 1536; `tools/memory.sh` now runs Honcho's `configure_embeddings.py --yes` and retries. By hand: `cd ~/.honcho/profiles/hermes && docker compose -p honcho-hermes run --rm --no-deps --entrypoint /app/.venv/bin/python api scripts/configure_embeddings.py --yes` |
| `hermes honcho sync` says "not configured on default profile" | It inherits from a `hosts.hermes` block; `wire` now writes one with `enabled: false` so your default profile stays detached |
| A Bot answers `HTTP 401: User not found` | The profile has no API key: named profiles read only their own `.env`. `tools/install.sh` seeds the pinned provider's key from `~/.hermes/.env`; re-run it, or `hermes -p <name> config set OPENROUTER_API_KEY ...` |
| A Bot answers `HTTP 403 ... 18+ age confirmation` | OpenRouter gates some models (Meta's Muse Spark among them) behind a one-time confirmation at https://openrouter.ai/settings/preferences |
| `honcho start` fails to pull or start | `honcho doctor`; `docker ps`; check ports 8001, 5432, 6379 are free, or pass `--api-port` |
| Deriver errors mention JSON | The template already sets `DERIVER_MODEL_CONFIG__STRUCTURED_OUTPUT_MODE=json_object`; confirm the model supports tool calling |
| A profile shows `provider: builtin` in `status` | It was not installed when you ran `wire`; run `wire` again |
| Turn it off | `python3 tools/memory_setup.py down --unwire` keeps the data and detaches the profiles; add `--wipe` to delete the data |

References: Hermes memory providers doc (installed at
`~/.hermes/hermes-agent/website/docs/user-guide/features/honcho.md`), Honcho
configuration reference (`https://honcho.dev/docs/v3/contributing/configuration`),
Honcho self-hosting (`https://honcho.dev/docs/v3/contributing/self-hosting`).
Model scores are from Artificial Analysis as of 2026-09-09.
