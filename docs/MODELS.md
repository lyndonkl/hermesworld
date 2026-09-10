# Choosing models for these agents

Where a model can be set in Hermes, what each agent here actually demands, and
which OpenRouter models fit each demand as of 2026-09-09. Benchmark numbers are
from [Artificial Analysis](https://artificialanalysis.ai) (Intelligence Index
v4.3 and its agentic evaluations); prices are OpenRouter's live list prices per
1M tokens on the same day. Re-check both before spending real money; they move.

## Where a model can be set

Hermes picks a model per **profile** (session), never per skill. A skill is a
document loaded into the running agent's context, so it runs on whatever model
that agent is using.

| Scope | Config | Applies to |
|---|---|---|
| A profile | `model.default` and `model.provider` in that profile's `config.yaml`, or `hermes -p <name> model` | Everything that profile does, including every skill it loads |
| Delegated children | `delegation.model` / `delegation.provider` in the parent's `config.yaml` | Every `delegate_task` child of that profile, all the same model |
| Auxiliary jobs | `auxiliary.<role>` in `config.yaml`: `compression`, `background_review`, `review`, `title_generation`, `vision`, `approval`, `skills_hub`, `mcp`, `memory_query_rewrite`, `tts_audio_tags`, `triage_specifier`, `kanban_decomposer`, `profile_describer`, `goal_judge`, `curator`, `monitor`, `moa_reference`, `moa_aggregator` | Housekeeping calls, independent of the main model. A role left unset runs on the main model at its price; the packages pin every text role to the cheap model |
| Reasoning effort | `agent.reasoning_effort` (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, `ultra`) and per-model `agent.reasoning_overrides` | How hard the chosen model thinks; each model accepts a subset, and on OpenRouter Hermes rounds an unsupported level down to the nearest one the model offers |
| Mixture of Agents | `moa.presets` (reference models + an aggregator), selected as the model | Several models per turn, one acting; expensive, not a per-skill switch |
| Kanban task | `hermes kanban set-model <id> <model>` | One board task, when using the Kanban dispatcher |

Consequences for this repo:

- The **fifteen-profile valuation team** uses a model per specialist, set in each
  member's `config.yaml` from the tier map in `teams/valuation/team.yaml`.
- Skills that need a different model must move to a different profile or to a
  delegated child; there is no other mechanism.

## What each agent demands

| Workload | Agents | What matters | Benchmarks that proxy it |
|---|---|---|---|
| Long-horizon orchestration | `valuation-orchestrator` | Multi-turn state tracking, tool discipline, reading artifacts, not drifting over 20+ turns | AA-Briefcase (long-horizon knowledge work), GDPval-AA v2 (shell + web agent loop) |
| Judgment specialists | `company-diagnostician`, `business-narrative-analyst`, `intrinsic-valuation-analyst`, `special-situations-analyst`, `capital-structure-analyst`, `investment-analyst`, `real-options-analyst`, `valuation-critic`, `investment-reconciler`; standalone `superforecaster`, `product-strategist` | Domain reasoning over long references (the playbooks are ~100 KB), defensible choices of inputs, adversarial review, prose quality | Intelligence Index, GDPval-AA v2 (finance occupations included), AA-LCR long-context reasoning |
| Procedure specialists | `financial-data-collector`, `financial-statement-analyst`, `cost-of-capital-analyst`, `relative-valuation-analyst`, `payout-policy-analyst` | Follow a fixed procedure, run the bundled Python engines correctly, source numbers with citations | AA-AnalystAgent (spreadsheet/document quantitative work, pass^5), Terminal-Bench, GDPval-AA v2 |
| Code-heavy design | `geometric-deep-learning-architect`, `cognitive-design-architect` | Maths and PyTorch or D3 code alongside explanation | Terminal-Bench v4.0, Intelligence Index |
| Housekeeping | `auxiliary.*` roles, delegation children that only summarise | Cheap and fast; correctness of short outputs | price and tokens/sec |

## The numbers that drove the picks

Artificial Analysis, 2026-09-09. Elo columns are pairwise-comparison ratings;
higher is better. Blanks mean the row was not in the tables retrieved.

| Model (AA name) | Intelligence Index v4.3 | AA-Briefcase Elo | GDPval-AA v2 Elo | Other | OpenRouter id | $/1M in / out |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 (xhigh) | 53 | 1650 | 1745 | Terminal-Bench v4 55.1%, AA-LCR 85.3% (max) | `anthropic/claude-fable-5.1` | 10 / 50 |
| GPT-6 Astra (xhigh) | 53 | 1534 | | Terminal-Bench v4 59.6% (best) | `openai/gpt-6-astra` | 10 / 50 |
| Claude Opus 5 (xhigh) | 50 | 1625 | 1708 | | `anthropic/claude-opus-5` | 5 / 25 |
| Muse Spark 1.3 (max) | 48 | 1589 | 1703 | 222 tokens/s | `meta/muse-spark-1.3` | 1.25 / 4.25 |
| GPT-5.6 Sol (max) | 47 | | 1624 | | `openai/gpt-5.6-sol` | 2 / 10 |
| GLM-5.3 (max) | 45 | 1515 | 1675 | | `z-ai/glm-5.3` | 1.40 / 4.40 |
| Grok 4.6 (xhigh) | 44 | 1545 | 1663 | | `x-ai/grok-4.6` | 2 / 6 |
| Kimi K3 (max) | 44 | 1497 | 1584 | AA-LCR 88.7% (best) | `moonshotai/kimi-k3` | 3 / 15 |
| GLM-5.3-Flash | 42 | | 1669 | | `z-ai/glm-5.3-flash` | 0.07 / 0.23 |
| Qwen3.8-Flash-Next | 40 | 1587 | 1647 | | `qwen/qwen3.8-flash` (name mapping unverified) | 0.15 / 0.47 |
| Gemini 3.7 Flash (high) | | | | AA-AnalystAgent 60.0% pass^5 (best) | `google/gemini-3.7-flash` | 0.75 / 3.75 |
| Claude Sonnet 5 | | | | not in the retrieved rows | `anthropic/claude-sonnet-5` | 2 / 10 |
| DeepSeek V4 Pro / Flash | | | | not in the retrieved rows | `deepseek/deepseek-v4-pro`, `deepseek/deepseek-v4-flash` | 0.96 / 1.91, 0.09 / 0.18 |

Two things stand out. Muse Spark 1.3 sits within about 60 Elo of the frontier on
both agentic evaluations at an eighth of the price and three times the speed.
GLM-5.3-Flash scores 1669 on GDPval-AA at $0.07 per million input tokens, which
makes it hard to justify anything dearer for procedure work until a real run
shows it failing.

## A writing model, for reports

Long-form prose is judged by people, not by pass rates, so the evidence here is the
Arena (formerly LMArena) Creative Writing leaderboard, human pairwise votes, updated
2026-09-02. Anthropic models top it, but the owner of this repo does not want Opus
writing reports, so the picks below are the strongest non-Anthropic rows that are on
OpenRouter:

| Model (Arena name) | Arena score | Votes | OpenRouter id | $/1M in / out |
|---|---|---|---|---|
| gemini-3.7-flash-high | 1496 ± 18 | 1,203 | `google/gemini-3.7-flash` at `high` | 0.75 / 3.75 |
| gemini-3.8-flash-high | 1495 ± 19 | 1,086 | `google/gemini-3.8-flash` at `high` | 0.75 / 3.75 |
| gemini-3-pro / 3.1-pro-preview | 1483 / 1479 | 6,236 / 17,972 | `google/gemini-3.1-pro-preview` | 2 / 12 |
| gpt-5.6-sol-xhigh | 1477 ± 10 | 4,670 | `openai/gpt-5.6-sol` at `xhigh` | 2 / 10 |
| glm-5.3-max | 1467 ± 15 | 1,719 | `z-ai/glm-5.3` at `max` | 1.40 / 4.40 |
| qwen3.8-max | 1466 ± 13 | 2,604 | `qwen/qwen3.8-max-0902` | 2 / 6 |
| muse-spark | 1464 ± 14 | 1,949 | `meta/muse-spark-1.3` | 1.25 / 4.25 |
| kimi-k3-max | 1460 ± 11 | 3,577 | `moonshotai/kimi-k3` | 3 / 15 |

For reference, the Anthropic rows: claude-fable-5 1504, claude-opus-4-6-high 1500,
claude-fable-5.1-max 1487, claude-opus-5-high 1475.

**Writer tier = `google/gemini-3.7-flash` at `high`.** It ties for the best non-Anthropic
writing score, it also holds the best AA-AnalystAgent result (60% pass^5 on spreadsheet and
document work, which is what a strategy or valuation report is built from), and it costs
a fifth of the alternatives. `openai/gpt-5.6-sol` at `xhigh` is the frontier alternative
when the report needs more reasoning of its own: Intelligence Index 47 and GDPval-AA 1624.

Where the writer tier is used:

- `investment-reconciler` in the Bot team writes `REPORT.md`, so its profile runs the
  writer model. Its reconciliation judgment is bounded by artifacts the strong-tier
  specialists already produced.
- `product-strategist` runs two models: the profile's own model does the research and
  curation (Steps 1 to 7), and a `delegate_task` child on `delegation.model` writes the
  report and runs the comprehension pass (Step 8). The parent verifies (Step 9).

## Presets

`tools/team_models.py` applies these to the installed team; the same ids work
for `hermes -p <name> model` on the standalone agents.

| Tier | frontier | balanced (shipped default) | budget |
|---|---|---|---|
| `orchestrator` | `anthropic/claude-fable-5.1` at `xhigh` | `meta/muse-spark-1.3` at `high` | `z-ai/glm-5.3` at `high` |
| `strong` | `anthropic/claude-opus-5` at `xhigh` | `meta/muse-spark-1.3` at `high` | `z-ai/glm-5.3` at `high` |
| `fast` | `anthropic/claude-sonnet-5` at `high` | `google/gemini-3.7-flash` at `medium` | `z-ai/glm-5.3-flash` at `high` |
| `writer` | `openai/gpt-5.6-sol` at `xhigh` | `google/gemini-3.7-flash` at `high` | `google/gemini-3.7-flash` at `high` |
| auxiliary | `z-ai/glm-5.3-flash` | `z-ai/glm-5.3-flash` | `z-ai/glm-5.3-flash` |

The balanced column is what every package now ships in its `config.yaml` (provider
`openrouter`), so a fresh install already runs on these. The team's picks live in
`teams/valuation/team.yaml` under `models:`; the standalone agents' in their own
`config.yaml`. Installers keep their `config.yaml` across updates, so a later change of
mind is made on the installed profile, not by re-installing.

```bash
python3 tools/team_models.py valuation --preset balanced          # after tools/install.sh --team valuation
python3 tools/team_models.py valuation --preset frontier --provider openrouter
python3 tools/team_models.py valuation --orchestrator anthropic/claude-fable-5.1 \
        --strong meta/muse-spark-1.3 --fast z-ai/glm-5.3-flash    # or mix by hand
python3 tools/team_models.py valuation --show
```

Per-profile picks for the standalone agents, same reasoning:

| Profile | Start with | Why |
|---|---|---|
| `superforecaster` | `meta/muse-spark-1.3` | Reasoning plus many web searches; frontier `anthropic/claude-fable-5.1` |
| `product-strategist` | `meta/muse-spark-1.3` for research, `delegation.model: google/gemini-3.7-flash` for the report | Reasoning and news curation first; the writing model drafts the report as a delegated child |
| `cognitive-design-architect` | `meta/muse-spark-1.3` | Design reasoning and D3 code; frontier `openai/gpt-6-astra` for the coding end |
| `geometric-deep-learning-architect` | `openai/gpt-6-astra` at `high`, or `meta/muse-spark-1.3` to start | Maths plus PyTorch; GPT-6 Astra leads Terminal-Bench v4 |

Reasoning effort: set it in the profile's `config.yaml` (`agent.reasoning_effort`).
Each model accepts a specific set of levels. On OpenRouter, Hermes rounds a level
the model does not offer down to the nearest one it does, so a wrong level is not
an error. Natively: Fable 5.1, GPT-6 Astra and Opus 5 take `low` to `max`; Muse
Spark 1.3 takes `minimal` to `xhigh`; GLM-5.3 and GLM-5.3-Flash take `low`,
`medium`, `high` and `max`; Gemini 3.7 Flash takes `low` to `high`. The generated
team configs use `high` for the strong and orchestrator tiers and `medium` for fast.

## How to decide for real

1. Install the team, apply `--preset balanced`, run one valuation of a company you
   know well, and read the critic's findings and the reconciler's report.
2. Move single stages up or down a tier with `hermes -p <member> model` and
   re-run only that stage (the orchestrator resumes from `state.json`).
3. Keep `auxiliary.*` on the cheapest model regardless; nothing there needs
   reasoning.
4. Re-check the leaderboards before committing to a long project. The rows
   above were retrieved on 2026-09-09.

## Memory providers, briefly

Only one external memory provider can be active per profile (`memory.provider`; the
memory manager refuses a second). Different profiles may use different providers.

| | Honcho | Mem0 |
|---|---|---|
| What it adds | Cross-session user modelling: a shared user peer across profiles, one AI peer per profile, LLM "dialectic" reasoning about the user, semantic search, session context | Automatic fact extraction from conversations, deduplication, semantic search with optional reranking |
| Cloud cost (2026-09-09) | Ingestion $2.00 per 1M tokens; reasoning per query $0.001 (minimal) to $0.50 (max); `context()` unlimited; $1,000 startup credits programme | Hobby free: 10,000 adds and 1,000 retrievals a month; Starter $19/month; Pro $249/month; Enterprise custom |
| Self-hosted | Free, AGPL-3.0; needs Postgres with pgvector and an LLM key for reasoning | Free, Apache-2.0; needs an LLM key and a vector store such as Qdrant |
| Config location | `memory.provider: honcho` in the profile's `config.yaml`; `honcho.json` in the profile dir; key in the profile's `.env` | `memory.provider: mem0`; `mem0.json` in the profile dir; `MEM0_API_KEY` in `.env` |
| Enable | `hermes -p <name> memory setup` | `hermes -p <name> memory setup` |

Nothing memory-related ships in these packages; memory is user-owned by design.
The chosen set-up, self-hosted Honcho on a local model, is in [MEMORY.md](MEMORY.md).
