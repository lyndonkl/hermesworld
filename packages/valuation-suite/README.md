# valuation-suite

A Hermes Agent profile that runs a complete company analysis end to end. It classifies the
company first and routes it through the specialist stages its type allows. It enforces the
gates between stages, has the result attacked by a critic, and reconciles everything into
one verdict with a range and a margin of safety. The method is Aswath Damodaran's corporate
finance and valuation curriculum, packaged as tested stdlib-Python scripts so the agent
argues about assumptions rather than arithmetic. The design goal is to prevent confident
nonsense — a discounted cash flow on a bank, an optimal debt ratio for a REIT, a
going-concern value for a firm months from insolvency — by making classification bind every
later stage.

## The six modes

| Mode | The question | Ends with |
|---|---|---|
| `valuation` | What is this company worth? Buy, sell or hold? | value per share and a verdict |
| `corporate-finance` | Are its investing, financing and payout choices right? | assessment across all three |
| `acquisition` | What should we pay for this target? | maximum price and synergy split |
| `project` | Should we make this investment? | project NPV and a decision |
| `ipo` | What is this private company worth going public? | offer price range |
| `restructuring` | What is it worth run differently? | status quo against optimal, value of control |

## How it is organised in Hermes

One profile, three parts:

- **The orchestrator is `SOUL.md`.** It owns the workspace, the state file and the
  conversation. It never computes; it decides what runs, in what order, with what inputs,
  and checks each gate by reading artifacts on disk. It is injected into every session of
  the profile.
- **Fourteen stage briefs** under `skills/valuation-specialists/`, one per specialist
  (data collector, diagnostician, narrative analyst, statement analyst, cost of capital,
  intrinsic valuation, relative valuation, special situations, capital structure, payout,
  investment, real options, critic, reconciler). Hermes has no named subagents, so at each
  stage the orchestrator loads the brief with `skill_view` and hands it to `delegate_task`
  as the child's `context`. Alongside the brief go the absolute paths to read and write,
  the constraints from `classification.json`, the currency and date, and the resolved
  skills path. Parallel stages go in one `delegate_task` call as several `tasks`. The
  briefs are not meant to be triggered on their own.
- **Nineteen finance skills** under `skills/corporate-finance/` (DCF engine, cost of
  capital toolkit, statement normalization, multiples, options, project analysis, payout,
  special situations, Monte Carlo, consistency checks, classification routing, narrative to
  numbers, red team, data sourcing, governance, debt design, reporting, unit economics,
  narrative builder), each with stdlib Python under `scripts/` and a `selftest`. The
  `valuation-playbooks` skill bundles the 32 framework and concept notes the briefs cite.
  `skills/writing/readability-check` scores the final report.

Every run lives in a workspace the orchestrator creates (`00-mandate/` through
`11-verdict/`), with exactly one stage authorized to write each file, and a `state.json`
that lets an interrupted run resume.

## Install

From the repository root:

```bash
tools/install.sh valuation-suite
```

or directly:

```bash
hermes profile install ./packages/valuation-suite --alias
```

The package pins no model or provider. The installer seeds the profile's model block from
your root profile; change it any time with `hermes -p valuation-suite model`. Then:

```bash
hermes -p valuation-suite chat
```

## First prompts to try

- "Value Nike in USD as of today. I have no files; go find the filings."
- "Here are the last five annual reports and the latest 10-Q for Vale (attached). Should I
  buy at the current price?"
- "Assess Deutsche Bank's corporate finance decisions — is its capital, payout and
  investment policy right?"
- "We are considering acquiring Company X at 40 dollars a share. Motive is synergy. What is
  the most we should pay, and who captures the synergy at that price?"
- "Evaluate this project: 120 million upfront, ten-year life, cash flows attached, in
  Brazilian real. Hurdle rate matched to the project, not the parent."
- "A private logistics company wants to IPO. Here are its statements. What is the offer
  price range?"

The orchestrator will ask for whatever it cannot infer (mode, currency, valuation date) and
then say what it is about to run and roughly how long it will take.

## Model note

Hermes uses one model for delegated children: they inherit the parent's model unless
`delegation.model` (and `delegation.provider`) is set in the profile's `config.yaml`. The
Claude version's per-agent model tiers are gone; there is no per-stage model choice. The
shipped `config.yaml` sets `delegation.max_iterations: 250`,
`max_concurrent_children: 4` and `max_spawn_depth: 1` — specialists are leaves, only the
orchestrator delegates — and `reasoning_effort: high`.

## Running the scripts' selftests

Every finance script carries a `selftest` subcommand that runs its bundled worked examples:

```bash
python3 packages/valuation-suite/skills/corporate-finance/dcf-valuation-engine/scripts/dcf.py selftest
python3 packages/valuation-suite/skills/corporate-finance/cost-of-capital-toolkit/scripts/costofcapital.py selftest
```

To run all of them at once, along with the repository's structural checks:

```bash
python3 tools/validate.py valuation-suite --selftest
```

After install the same scripts live under the profile, at
`~/.hermes/profiles/valuation-suite/skills/corporate-finance/<skill>/scripts/`. Any
subcommand prints its input shape with `--example`.

## What changed from the Claude version

- The orchestrator agent became `SOUL.md`; the fourteen specialist agents became stage
  briefs (skills) that the orchestrator passes to anonymous `delegate_task` children as
  `context`. Children see no system prompt and no history, so each brief is
  self-contained and tells the child which finance skills to load with `skill_view`.
- Delegation runs in the background: the orchestrator dispatches a stage, ends its turn,
  and continues when the results message arrives. Parallel stages are one call with
  several `tasks`.
- Children cannot ask the user; they return `needs_input` and the orchestrator asks with
  `clarify`.
- The `<skills>` placeholder in every brief now means the absolute path of the
  `corporate-finance` skills directory of the installed profile. The orchestrator resolves
  it once per run from `skill_view("dcf-valuation-engine")` (the parent of `skill_dir`),
  verifies the validator script exists there, and substitutes it before delegating.
- Script paths moved from the Claude layout to Hermes's `scripts/` directory, and bundled
  data tables to `scripts/data/` inside each skill. The Claude knowledge notes are bundled
  as the `valuation-playbooks` skill and cited as `skill_view` references.
- Per-agent model tiers were dropped (see the model note). Claude Code tool names were
  replaced by Hermes tools (`read_file`, `write_file`, `terminal`, `web_search`,
  `web_extract`, `skill_view`, `clarify`, `delegate_task`).
- The toolkit gained a few subcommands since the Claude version and the briefs point at
  them: `costofcapital.py stress|apv|implied-erp`, `reference_data.py
  erp-for-operations|vintage`, `special.py ipo`, `project.py control-value|deal`,
  `multiples.py sum-of-parts|cross-holdings`, and `macrosensitivity.py` in `debt-design`.
- Three long artifact contracts moved into `references/` inside their briefs
  (statement analyst, special situations, capital structure) and are loaded on demand.

## Models

`config.yaml` pins `meta/muse-spark-1.3` for the orchestrator and, via `delegation.model`,
for every specialist child; the single-profile form cannot give the reconciler its own
writing model. The Bot team (`valuation-orchestrator` and members) can, and runs its
reconciler on the writer tier. See `docs/MODELS.md`.
