# Valuation orchestrator (Bot team)

The orchestrator of a fifteen-Bot valuation team for Hermes Agent. It fixes the mandate,
creates the run's workspace, dispatches fourteen specialist Bots stage by stage, verifies
every gate against the artifacts on disk, and hands over the reconciler's report. It never
computes, forecasts or values anything itself.

It is one of fifteen Bots. Each specialist is its own profile with its own
personality file, skills, memory and model, listed in the desktop's Bots roster, and
each can also be asked to do its stage directly. Plain-language definitions of profile,
Bot, Bot Chat and teammate message are in the repository README under "Words used here".

## The team

| Bot | Stage | Tier |
|---|---|---|
| `valuation-orchestrator` | Mandate, workspace, routing, gates, verdict hand-over | strong |
| `financial-data-collector` | Filings, market data, reference tables; honest gaps | fast |
| `company-diagnostician` | Classification, route, binding constraints | strong |
| `business-narrative-analyst` | The story, graded, mapped to drivers | strong |
| `financial-statement-analyst` | Statement repair: leases, R&D, one-offs, TTM | fast |
| `cost-of-capital-analyst` | Riskfree rate, ERP, beta, cost of debt, WACC | fast |
| `intrinsic-valuation-analyst` | DCF to value per share; implied expectations | strong |
| `relative-valuation-analyst` | Multiples, regressions, when a multiple is unusable | fast |
| `special-situations-analyst` | Banks, young, distressed, cyclical, private firms | strong |
| `capital-structure-analyst` | Optimal debt ratio and debt design | strong |
| `payout-policy-analyst` | Cash returned versus FCFE, dividend matrix | fast |
| `investment-analyst` | Projects and acquisitions: NPV, control, synergy, price | strong |
| `real-options-analyst` | Genuine optionality, priced; look-alikes rejected | strong |
| `valuation-critic` | Adversarial review; findings, never edits | strong |
| `investment-reconciler` | Verdict, range, margin of safety, the report | writer |

Tiers map to OpenRouter models pinned in each member's `config.yaml`: orchestrator and
strong on `z-ai/glm-5.3-flash`, fast and writer on `google/gemini-3.7-flash`, housekeeping
on `z-ai/glm-5.3-flash`. Change them all at once with `tools/team_models.py` or one at a time
with `hermes -p <member> model`; the reasoning is in `docs/MODELS.md`.

## How it works

1. You open `valuation-orchestrator`'s chat in the Hermes desktop app with Bot Mode on.
2. It fixes the mandate with you, creates a numbered workspace, and writes `state.json`.
3. For each stage it composes a short job (goal, absolute paths to read and write, binding
   constraints, currency and date) and sends it with `message_agent` to the right teammate.
   Parallel stages go to different teammates in the same turn.
4. Each teammate runs the stage in its own chat, loads its finance skills with `skill_view`,
   runs the stdlib Python engines through `terminal`, writes only the artifacts it was
   named to write, and its final answer returns to the orchestrator automatically.
5. The orchestrator verifies the gate by reading the artifacts, updates `state.json`, and
   dispatches the next stage. The critic's findings reopen the owning stage, at most twice.
6. It presents the reconciler's report: value against price, the verdict, the range, the
   load-bearing assumptions, and anything unresolved.

Each teammate's job is capped at 16,000 characters by Hermes, which is why the job carries
paths and facts while the method lives in the teammate's own SOUL. A teammate takes one job
at a time; the orchestrator combines or serialises repeated stages (both cost-of-capital
rates in `ipo` mode travel in one job).

## Install

From the repository root, with Hermes 0.21 or newer and a working model:

```bash
tools/install.sh --team valuation
python3 tools/team_models.py valuation --strong <model-id> --fast <model-id>   # optional
```

`tools/install.sh --team` installs the orchestrator and all fourteen members as profiles.
It seeds each one's model from your root profile. It also writes each profile's Bot metadata,
the title and the role, so the roster and every teammate's system prompt show who does what.
`team_models.py` then sets `model.default` per tier if you want the opus/sonnet split back.
That step is optional and reversible with `hermes -p <name> model`.

Start it from a terminal with the command the installer created:

```bash
valuation            # opens this orchestrator's Bot Chat; add --tui for the terminal UI
```

or in the desktop app: Settings → Plugins → Bots on, then click **valuation-orchestrator**
in the Bots list. Either way you are in its Bot Chat, the one conversation from which it
can message its teammates. Try:

- "Value Costco as of last Friday's close, in USD. Valuation mode."
- "Corporate-finance review of Deere: is its debt, payout and investment policy right?"
- "What is the most we should pay for a target? I will upload its 10-K."

You can switch to other chats while a stage runs. Close the teammates' chats before you
start and keep them closed until the run reports back: a teammate whose chat is open when
its job arrives works inside that chat instead, and the orchestrator stops waiting for the
answer after five minutes. Open a teammate's chat afterwards to read what it did; the
workspace folder shows the stage's artifacts as they land.

## Requirements and limits

- The orchestrator must be in its Bot Chat: the `valuation` command in a terminal, or the
  Bot's chat in the desktop. In any other conversation it cannot reach its teammates and
  says so. Use one surface at a time; the second is refused with `already has a live owner`.
- All fifteen profiles on the same machine (they share the run's workspace on disk).
- Replies arrive between turns as background notifications. The orchestrator dispatches,
  reports one line, and ends its turn; results wake it. A full valuation is many turns.
- The orchestrator's `config.yaml` sets `dashboard.ws_orphan_reap_grace_s: 0`. Without it
  the desktop closes an idle chat 20 seconds after you switch away, and closing the chat
  kills every stage job it has out. Existing installs pick this up only through
  `tools/install.sh --team valuation`; `hermes profile update` keeps the old `config.yaml`.
- No schema validation on replies, unlike `delegate_task`; the orchestrator therefore trusts
  artifacts on disk, never a teammate's summary.

## Verify the install

```bash
hermes profile list                              # fifteen rows with the Distribution column filled
hermes -p cost-of-capital-analyst skills list    # its bundled finance skills, all enabled
hermes profile show cost-of-capital-analyst      # SOUL.md: exists, Distribution filled
```

## Regenerating the team

Every member package is generated by `tools/build_team.py` from
`teams/valuation/team.yaml`, the stage briefs in
`teams/valuation/skills/valuation-specialists/`, and the finance skills in
`teams/valuation/skills/corporate-finance/`. Edit those sources, run
`python3 tools/build_team.py valuation`, and validate. This orchestrator's `SOUL.md` and
`README.md` are hand-written; everything else in this package is generated.
