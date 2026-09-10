# Memory for these agents: self-hosted Honcho on a local model

How to give every profile in this repo a shared, persistent model of you, run on
your own machine, with the heavy reasoning optionally on a cheap cloud model. The
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

## Can a local model do Honcho's inference?

Honcho's requirement is tool calling in the OpenAI format for the deriver,
dialectic and dream jobs, plus JSON output for the deriver, plus an embedding
model. Its defaults are a small cloud model for text and `text-embedding-3-small`
for vectors, so the jobs are designed for mini-class models, not frontier ones.

**Your current server** is vllm-mlx serving `mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit`
on port 8000 of an M3 Max with 96 GB. It supports tool calling, and vllm-mlx
supports JSON-schema output and an `--embedding-model`. But the model itself is a
coding specialist and a non-reasoning model: Artificial Analysis scores it 10 on
the Intelligence Index v4.3. It will follow the deriver's extraction format, and it
is fine for summaries and embeddings, but its observations about a person and its
dialectic answers will be shallow. Not a good idea as the only model.

**A better local choice on the same machine:** `mlx-community/Qwen3.8-27B-4bit`.
Qwen3.8 27B is a reasoning model with tool calling, Apache-2.0, Intelligence Index
34 at high effort, and about 15 GB as a 4-bit MLX build (the 8-bit is about 29 GB
and also fits). That is the model `tools/local_llm.sh` serves by default. The two
open-weights models that score higher on the leaderboards are out of reach
locally: Qwen3.8-Flash-Next is 104 GB at 4-bit, and GLM-5.3 is larger still.

**The hybrid the tooling sets up by default:**

| Honcho job | Runs on | Why |
|---|---|---|
| Deriver, summaries, dreams, embeddings | Local Qwen3.8 27B + MiniLM embeddings via vllm-mlx | Background work; nobody waits on it; free |
| Dialectic, all levels | OpenRouter `z-ai/glm-5.3-flash` | Runs before a reply, so the conversation waits on it; a fast cloud model answers in seconds at $0.07 per 1M input tokens |

Pass `--dialectic-model local` to keep everything on the machine; expect the per-turn
reasoning to take a minute or more when several agents are active. With the hybrid,
the cloud share is cents per day of heavy use. Honcho Cloud, for comparison, charges $2.00 per 1M ingested tokens plus
$0.001 to $0.50 per reasoning query.

If you do not have Apple Silicon, any OpenAI-compatible server works: vLLM,
Ollama, LM Studio. Point `tools/memory_setup.py up` at it with `--local-url` and
`--local-model`, and pick a model that supports tool calling and is at least in
the Qwen3.8 27B class.

## Set-up: one command

Prerequisites: Docker Desktop installed (the command starts it); `uv` installed;
Hermes profiles installed from this repo (`tools/install.sh --all`); Python 3 with
PyYAML. Apple Silicon for the default local server; other machines pass
`--local-url` and `--local-model` for a server they run themselves.

```bash
tools/memory.sh --peer-name "Your Name"
```

Every step is checked first and skipped when already done, so the same command is
the installer, the restart after a reboot, and the health check:

1. **Local model server.** If nothing answers on `:8000`, installs vllm-mlx with
   `uv tool install`, writes a LaunchAgent (`com.hermesworld.local-llm`) so the
   server starts at login and restarts if it dies, and waits for
   `mlx-community/Qwen3.8-27B-4bit` plus the MiniLM embedding model to load. The
   first start downloads about 15 GB; progress is in
   `~/Library/Logs/hermesworld-local-llm.log`.
2. **Docker.** Starts Docker Desktop if it is not running.
3. **Honcho CLI.** `uv tool install honcho-cli` if missing.
4. **Honcho stack.** Renders `infra/honcho/honcho.env.template` into
   `~/.honcho/profiles/hermes/.env`, then `honcho start --profile hermes --api-port 8001`
   unless it is already healthy. If the rendered settings changed, the stack is
   restarted. Port 8001 because Honcho's default collides with the model server.
5. **Wiring.** For every installed hermesworld profile not yet attached: a
   `hosts.hermes_<profile>` block in `~/.hermes/honcho.json`, `memory.provider: honcho`
   in the profile's `config.yaml`, then `hermes honcho sync` to create the AI peers.
   Your default `~/.hermes` profile is left alone unless you pass `--include-default`.

Then a status table: Honcho health, model server health, and per profile whether it
is installed, its provider, and whether it has a host block.

Secrets stay on your machine. The Honcho `.env` under `~/.honcho/profiles/hermes/`
and each profile's `.env` are written with mode 600 and are never part of this
repository; the only env file in the repo is the placeholder template.

The OpenRouter key for the dialectic is read from `~/.hermes/.env`; without it the
dialectic runs locally too. Useful options: `--dialectic-model local`,
`--local-model mlx-community/Qwen3.8-27B-8bit`, `--wait-minutes 180` on a slow link.
The individual steps remain available as `python3 tools/memory_setup.py up|wire|status|down`
and `tools/local_llm.sh --status|--stop`.

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

## Capacity on one machine

The first live session showed why the split above matters. Two chats produced 42
calls to the local model in half an hour; 39 were the per-turn dialectic, each with
an 8,000-token prompt and an 8,192-token output allowance, and a 27B reasoning model
serving several of them at once took 70 to 200 seconds per call. Nothing failed on
Honcho's side, but the reasoning arrived too late to be injected. The setup now
sends the dialectic to the fast cloud model, caps output per level, keeps the
background jobs local, and asks for the dialectic less often on specialist Bots
(`dialecticCadence` 4 at level `minimal`) than on the orchestrator and standalone
agents (cadence 3 at `low`). All of those are per-profile keys in
`~/.hermes/honcho.json` and can be changed by hand.

## Limits to know

- One external provider per profile; Honcho and Mem0 cannot share a profile.
- The injected dialectic is capped at 600 characters by default
  (`dialecticMaxChars`); the base context is uncapped unless you set `contextTokens`.
- A 27B local model answers the dialectic in a few seconds; the first token after
  a cold start takes longer while the model loads.
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
| Deriver errors mention JSON | The template already sets `DERIVER_MODEL_CONFIG__STRUCTURED_OUTPUT_MODE=json_object`; confirm the local model supports tool calling |
| Honcho cannot reach the model server | Inside Docker the host is `host.docker.internal`; check `tools/local_llm.sh --check` on the host |
| A profile shows `provider: builtin` in `status` | It was not installed when you ran `wire`; run `wire` again |
| Turn it off | `python3 tools/memory_setup.py down --unwire` keeps the data and detaches the profiles; add `--wipe` to delete the data |

References: Hermes memory providers doc (installed at
`~/.hermes/hermes-agent/website/docs/user-guide/features/honcho.md`), Honcho
configuration reference (`https://honcho.dev/docs/v3/contributing/configuration`),
Honcho self-hosting (`https://honcho.dev/docs/v3/contributing/self-hosting`),
vllm-mlx (`https://github.com/waybarrios/vllm-mlx`). Model scores are from
Artificial Analysis as of 2026-09-09.
