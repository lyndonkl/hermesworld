# superforecaster

A Hermes Agent profile that produces calibrated probability forecasts the way Good Judgment Project superforecasters do: outside view first, then decomposition, then evidence, then a stress test and a bias check, and only then a number, with an 80% interval, kill criteria, and the sources behind every figure.

## What it does

Given a question such as "Will X happen by Y?", the agent restates it as a resolvable proposition, checks that it is forecastable at all, and then runs a fixed five-phase pipeline. Every base rate and data point comes from a web search and is cited; nothing is estimated from memory. The result is a forecast document plus a summary block in the conversation, and the user is drawn in at each phase boundary to challenge the reference class, the decomposition, the evidence weights, and the failure modes.

It will not give a bare probability, skip a phase, or invent a statistic. It will say "no data found" and proceed on a labelled assumption instead.

## The pipeline

1. **Triage and outside view.** Is the question clock-like (calculate), cloud-like (unknowable), or complex (forecastable)? Then `reference-class-forecasting`: choose the reference class, search for its base rate, validate it. Hands forward a base rate with N and sources.
2. **Decomposition.** `estimation-fermi`: break the event into components, estimate each with a search, combine, and reconcile the structural estimate with the base rate. Hands forward a weighted prior.
3. **Inside view.** Three to five evidence searches across news, expert views, prediction markets, statistics, and research, then `bayesian-reasoning-calibration`: one likelihood-ratio update per piece of evidence. Hands forward a posterior.
4. **Stress test and bias check.** `forecast-premortem`: assume failure, quantify the failure modes, compare with the implied failure. Then `scout-mindset-bias-check`: reversal test, scope sensitivity, status quo, surprise test, full bias audit. Hands forward an adjusted probability and an 80% interval.
5. **Calibration and output.** Confidence interval, kill criteria ("if X happens, probability drops to Y%"), monitoring signposts, then the write-up, which passes through `strategist-voice`, `slop-detector`, and `readability-check` before delivery.

## Install

From the root of this repository:

```bash
tools/install.sh superforecaster
```

or directly with Hermes:

```bash
hermes profile install ./packages/superforecaster --alias
```

Then start a session:

```bash
hermes -p superforecaster chat
```

The package pins `meta/muse-spark-1.3` on OpenRouter at high reasoning effort (see `docs/MODELS.md`); change it any time with `hermes -p superforecaster model`. The agent needs a web-capable provider (it searches for every base rate) and nothing else.

Optional: `readability-check` scores the final write-up with the `textstat` package. Without it the script prints the install line and exits 3, and the agent states the exception instead of scoring.

```bash
python3 -m pip install --user textstat
```

## First prompts to try

- "What is the probability that [company] ships [product] before [date]?"
- "Forecast whether [bill] passes the Senate this session."
- "Will our Q4 launch reach 10,000 sign-ups in its first 30 days? Standard depth."
- "Quick forecast: will this Series A round close within 90 days?"
- "Deep forecast: probability this seed-stage B2B SaaS company reaches $10M ARR within 24 months. I can answer questions about the team and pipeline."

Ambiguous questions get a clarifying question first (what counts as the event, by when, judged by what source). Well-posed ones go straight into Phase 1.

## Skills it carries

| Category | Skill | What it does | When the agent loads it |
|---|---|---|---|
| forecasting | `reference-class-forecasting` | Base rate from a validated reference class; funnels when no single statistic exists. Also holds the pipeline's protocol reference. | Phase 1 |
| forecasting | `estimation-fermi` | Decompose an unknown into estimable parts, bound it, triangulate. | Phase 2 |
| forecasting | `bayesian-reasoning-calibration` | Likelihood-ratio updates from prior to posterior, with a calibration check. | Phase 3 |
| forecasting | `forecast-premortem` | Failure and success premortems, dragonfly eye, tail risks, kill criteria, signposts, CI adjustment. | Phase 4 |
| forecasting | `scout-mindset-bias-check` | Reversal, scope sensitivity, status quo, CI audit, full bias audit. | Phase 4 |
| writing | `strategist-voice` | Analyst house style: no em dashes, footnoted sources, graded opinion signalling. | Write-up |
| writing | `slop-detector` (shared) | Ten signatures of AI-written explainer prose. | Write-up |
| writing | `readability-check` (shared) | Five readability formulas plus the sentences to fix; a Python script. | Write-up |

The two shared skills are copied from `shared/skills/` by `tools/sync_shared.py`; edit them there, not here.

## What changed from the Claude version

- **No readability hook.** The Claude plugin scored long output automatically through editor hooks. Hermes profiles have no such hook, so `readability-check` runs on demand: the agent runs its script through `terminal` as the last step of the write-up, and you can ask for it at any time.
- **Skills are loaded with `skill_view`.** The agent's body (`SOUL.md`) keeps the order of the phases, the gates between them, and what each hands forward. The long per-step scaffolding of the original agent (progress checklists, hand-off record formats, question scripts, manual fallbacks) moved into `skills/forecasting/reference-class-forecasting/references/superforecaster-protocol.md`, which the agent loads once per forecast.
- **Depth is inferred, then confirmable.** The original opened by asking "Quick, Standard or Deep?". This version infers the depth from the request, states it, and lets you redirect; the clarifying question is reserved for ambiguity in the forecasting question itself.
- **Tool names** follow Hermes: `web_search` and `web_extract` for evidence, `write_file` for the forecast document, `todo` for the pipeline checklist.
- **Skill layout** follows Hermes: `resources/` became `scripts/`, `references/`, `templates/`, and `assets/`, and every skill carries a 60-character description, tags, and related skills for the Hermes skill index.
- **A pinned model.** The Claude agent inherited its model from the plugin; here `config.yaml` pins `meta/muse-spark-1.3` on OpenRouter, chosen for reasoning plus web research (`docs/MODELS.md`).

## Files

```
distribution.yaml     manifest
SOUL.md               the agent: identity, standing rules, the five-phase pipeline, output template
config.yaml           model (meta/muse-spark-1.3), reasoning effort, cheap auxiliary model
shared-skills.txt     shared skills copied in by tools/sync_shared.py
skills/forecasting/   the five forecasting skills and the protocol reference
skills/writing/       strategist-voice, slop-detector, readability-check
```
