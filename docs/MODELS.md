# Model providers and reasoning for hermesworld profiles

The default `codex-pro` policy uses `openai-codex` for all 25 profiles,
authenticated with your ChatGPT account. OpenRouter is available through the
`balanced`, `qwen`, `budget`, and `frontier` presets. Honcho continues to use OpenRouter for its server-side reasoning and
embeddings; its settings and stored memories are independent of these routes.

## Authenticate and migrate existing profiles

Use a current Hermes release and authenticate once in the root Hermes home:

```bash
hermes auth add openai-codex
python3 tools/profile_models.py --all          # preview installed profile changes
python3 tools/profile_models.py --all --apply  # apply with per-profile backups
```

The migration updates only model routes and reasoning settings. It preserves
Honcho, memory, tools, Bot metadata, and unrelated configuration. Existing
profile updates preserve config.yaml, so pulling this PR alone does not migrate
your installed profiles. Restart active profile sessions after applying it.
The backup beside each config can be copied back to restore the previous setup.

For a single profile or a complete team:

```bash
python3 tools/profile_models.py --profile product-strategist --apply
python3 tools/team_models.py valuation --preset codex-pro
python3 tools/team_models.py engineering --preset codex-pro
python3 tools/team_models.py exploratory --preset codex-pro
```

Fresh installs use the shipped settings automatically (`tools/install.sh --all`).
Distribution manifests do not require an OpenAI API key or an OpenRouter key for
bot inference. Keep your OpenRouter credentials for Honcho; `tools/memory.sh`
and the Honcho environment template continue to use them.

## Model and effort choices

Models are selected per profile, not per skill. These starting allocations follow
the actual work described by each profile; they are recommendations, not measured
performance results. Team member overrides live in `teams/<team>/team.yaml`.
Standalone choices live in the package config.yaml. Regenerate teams with
`python3 tools/build_team.py <team>` after changing their source manifests.

| Work | Profiles | Model | Reasoning effort |
|---|---|---|---|
| Coordination | valuation-orchestrator, engineering-planner, exploratory-strategist | gpt-5.6-sol | high |
| Difficult judgment and maths | intrinsic-valuation-analyst, special-situations-analyst, real-options-analyst, valuation-critic, geometric-deep-learning-architect, ml-engineer | gpt-6-astra | high |
| Analysis and implementation | company-diagnostician, business-narrative-analyst, capital-structure-analyst, investment-analyst, software-engineer, product-strategist, superforecaster, cognitive-design-architect | gpt-5.6-sol | high |
| Financial procedures | financial-statement-analyst, cost-of-capital-analyst, relative-valuation-analyst, payout-policy-analyst | gpt-5.6-terra | medium |
| Collection and assistance | financial-data-collector, welch-ai-guide | gpt-5.6-terra | low |
| Reconciliation and review | investment-reconciler, code-reviewer | gpt-5.6-sol | high |

Delegated children use their parent's model and effort through explicit routes.
The product strategist's report writer is explicitly pinned to Sol at high effort.
All primary and delegated fallback chains are disabled: subscription exhaustion
surfaces a failure rather than switching to OpenRouter.

Auxiliary policy is shared by generation and migration in `tools/profile_models.py`:

| Auxiliary work | Model | Effort |
|---|---|---|
| Compression | gpt-5.6-terra | low |
| Review, background review | gpt-5.6-sol | high |
| Vision, goal judging, Kanban decomposition | gpt-5.6-terra | medium |
| Titles, approval assistance, skill lookup, MCP assistance, profile descriptions, curator, monitor, query rewrites, audio tags, triage | gpt-5.6-luna | low |

MoA auxiliary routes also use OpenAI, but reasoning for an active MoA preset must
be specified in its reference and aggregator slots. No MoA presets ship here.

Every auxiliary provider is explicitly `openai-codex`. Query rewriting is a
Hermes-side auxiliary job; Honcho's own model calls still use OpenRouter.
Explicit auxiliary endpoints and API keys are removed during migration because
they override provider routing. Per-model reasoning overrides are cleared so the
profile's selected effort applies. The migration preserves unrelated task options.

## Subscription access and usage

These routes use ChatGPT/Codex OAuth, not the separately billed OpenAI API.
Authenticate in Hermes rather than copying OAuth tokens between profiles.
Pro includes Astra and the GPT-5.6 family in Codex, subject to account access and
usage limits. Availability changes; check the Hermes model picker before a long run.
Higher effort and additional auxiliary calls consume allowance and increase latency.
Hermes currently does not document exact plan-quota accounting for its Codex route.

Sources checked 2026-10-04:

- [Hermes providers and subscription authentication](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Hermes auxiliary model and reasoning configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [OpenAI model availability in Codex](https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt)
- [Codex usage with ChatGPT plans](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)

## Choose OpenAI or OpenRouter during setup

```bash
# ChatGPT/Codex subscription (default); complete OAuth first
hermes auth add openai-codex
tools/install.sh --all --models codex-pro

# OpenRouter; use `hermes model` to configure OPENROUTER_API_KEY first
tools/install.sh --all --models balanced

# Switch installed profiles with a preview, then apply
python3 tools/profile_models.py --all --preset balanced
python3 tools/profile_models.py --all --preset balanced --apply
python3 tools/profile_models.py --all --preset codex-pro --apply
```

Both providers update primary, auxiliary, delegated routes and reasoning together.
OpenRouter presets use the previous project's tier choices: `balanced` and
`budget` use GLM-5.3-Flash throughout; `qwen` uses Qwen3.6-Plus for coordination
and judgment; `frontier` uses Fable/Opus/Sonnet and GPT-5.6 Sol for writing.
Their auxiliary calls use GLM-5.3-Flash with role-specific effort. These are
historical picks, not live benchmark guarantees; confirm model availability.
The provider and model IDs are selected together so OpenRouter IDs cannot
accidentally be sent to the Codex endpoint. Named profile API keys are seeded
locally from the root Hermes .env when missing; OAuth tokens are never copied.
The migration writes a protected backup beside each changed config.
Honcho's OpenRouter routing is preserved under either inference policy.

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
