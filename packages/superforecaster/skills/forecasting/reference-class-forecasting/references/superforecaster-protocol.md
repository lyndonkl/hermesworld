# Superforecaster protocol: per-phase scaffolding

The superforecaster agent's SOUL.md fixes the order of the pipeline, the gates between phases, and what each phase hands forward. This file holds the scaffolding that was too long to keep there: the copyable progress checklists, the hand-off record formats, the question scripts for collaborating with the user, the search-query families, and the manual fallbacks for each step when its skill cannot be loaded. The forecasting method itself lives in the skills; nothing here replaces `reference-class-forecasting`, `estimation-fermi`, `bayesian-reasoning-calibration`, `forecast-premortem`, or `scout-mindset-bias-check`.

## Master checklist

Copy into `todo` at the start of a forecast.

```
Superforecasting Pipeline Progress:
- [ ] Phase 1.1: Triage check - is this forecastable?
- [ ] Phase 1.2: Reference class - find the base rate via web search
- [ ] Phase 2.1: Fermi decomposition - break into components
- [ ] Phase 2.2: Reconcile - compare structural vs base rate
- [ ] Phase 3.1: Evidence gathering - web search (3-5 queries minimum)
- [ ] Phase 3.2: Bayesian update - update with each piece of evidence
- [ ] Phase 4.1: Premortem - identify failure modes
- [ ] Phase 4.2: Bias check - run the debiasing tests
- [ ] Phase 5.1: Set confidence intervals - determine CI width
- [ ] Phase 5.2: Kill criteria - define monitoring triggers
- [ ] Phase 5.3: Final output - write and present the forecast
```

## Depth settings

| Depth | Time | Base-rate searches | Evidence searches | Premortem | Bias tests |
|---|---|---|---|---|---|
| Quick | ~5 min | 1-2 | 2-3 | Failure premortem only, top 3 modes | Reversal + surprise test |
| Standard | ~30 min | 2-3 | 3-5 | Failure premortem + tail risks | All four tests + quick audit |
| Deep | 1-2 h | 3+ per candidate class | 5-10, incl. prediction markets | Dragonfly eye + CI adjustment | All four tests + full audit |

Pick from the request (a one-line question implies Quick; a decision memo implies Deep), state the choice, and let the user redirect.

## Three rules that apply to every phase

**Search, do not generate.** No invented base rates, statistics, or data points, and no estimating from memory when a search could settle it. Use `web_search` to find published data and `web_extract` to read it. Cite URLs. If nothing turns up after searching, write "No data found", list the queries tried, and only then make an explicit assumption labelled as such.

**Every assumption is visible.** Before any assumption is used, state it and why. Defer to the user's domain knowledge when they have it. When information is missing, prefer asking to guessing; when the user is not available, proceed on the labelled assumption and collect all open assumptions in the write-up so they can be challenged.

**Every data point has a source.** Format: `[Finding] - Source: [URL or citation]`. User-supplied data: `[Finding] - Source: User provided`.

---

## Phase 1: Triage and the outside view

```
Phase 1 Progress:
- [ ] Step 1.1: Triage check
- [ ] Step 1.2: Reference class selection
- [ ] Step 1.3: Base rate web search
- [ ] Step 1.4: Validate with the user
- [ ] Step 1.5: Set the starting probability
```

### Step 1.1 Triage: the Goldilocks test

| Kind | Examples | Verdict |
|---|---|---|
| Clock-like (deterministic) | Physics, arithmetic, scheduled events with no uncertainty | Not forecasting; calculate or look it up |
| Cloud-like (pure chaos) | Truly random draws, no patterns, no reference class | Do not forecast; say why it is unknowable |
| Complex (skill + luck) | Games, markets, elections, launches, human systems | Forecastable; proceed |

If the question is not forecastable, say why and stop. If it is, also restate it as a resolvable proposition: event, threshold, resolution date, resolution source.

### Step 1.2 Reference class

Load `reference-class-forecasting` and run procedure 1 (Find the base rate), then procedure 4 (Validate). Manual fallback if the skill cannot be loaded: propose one class that is specific but data-rich, name two alternatives (one broader, one narrower), and pick the one with N >= 20 and the closest match on stage, domain, and period.

Script: "I think the appropriate reference class is [X]. Does that seem right, or is there a closer class you know of?"

### Step 1.3 Base rate search

Run the query family from the skill's Search strategy (success rate, failure statistics, survival rate, "what percentage of"). At least 2-3 searches. Record:

```
Web Search Results:
- Source 1: [URL] - Finding: [X]%  (N = [n], period [years])
- Source 2: [URL] - Finding: [Y]%
- Source 3: [URL] - Finding: [Z]%
```

No data found: "I couldn't find published data after searching [queries]. Do you have any sources, or should we proceed on an explicit assumption?" Then try a proxy class, then a funnel (procedure 3), then the skill's default anchors, labelled.

### Step 1.4 Validate with the user

Share the findings and the average, then ask: (1) does this base rate seem reasonable given your domain knowledge? (2) do you know of other sources or data? (3) should the class be more or less specific? Incorporate the answers.

### Step 1.5 Hand-off record

```
Base Rate: [X]%
Reference Class: [Description]
Sample Size: N = [Number] (if available)
Sources: [URLs]
Reference-class confidence: [High/Medium/Low]
```

Do not enter Phase 2 without this record. The base rate is the prior for everything that follows.

---

## Phase 2: Decomposition (the structure)

```
Phase 2 Progress:
- [ ] Step 2.1a: Propose the decomposition structure
- [ ] Step 2.1b: Estimate components with web search
- [ ] Step 2.1c: Combine components mathematically
- [ ] Step 2.2: Reconcile with the base rate
```

### Step 2.1a Propose the structure

Load `estimation-fermi` and run its procedure. Manual fallback: write the event as an AND/OR tree of 3-6 conditions that each have a findable rate, and stop decomposing when every leaf is a quantity someone has measured.

Script: "I'm breaking this into [components]. Are there critical components missing? Should any be decomposed further?"

### Step 2.1b Estimate each component

For each component: search first (1-2 queries: "[component] success rate", "[component] statistics", "[component] probability"), ask whether the user has domain knowledge about it, combine, and record the source.

### Step 2.1c Combine

- **AND** (all must happen): multiply the probabilities. Independence is an assumption; say so.
- **OR** (any can happen): add the probabilities and subtract the overlap.

Show the arithmetic. Hand-off record:

```
Decomposition:
- Component 1: [X]% (reasoning + source)
- Component 2: [Y]% (reasoning + source)
- Component 3: [Z]% (reasoning + source)

Structural Estimate: [Combined]%
Formula: [the calculation]
```

### Step 2.2 Reconcile with the base rate

Present: "Base rate [X]%, structural [Y]%, difference [Z] points."

- **Difference > 20 points:** do not average. Form a hypothesis about why they differ (missing component? stale base rate? correlated stages?), ask the user which is more reliable, and weight: `Weighted = w1 x Base_Rate + w2 x Structural`, with the weights justified in one sentence each.
- **Difference <= 20 points:** average them, or use the more reliable one.

```
Reconciliation:
- Base Rate: [X]%
- Structural: [Y]%
- Difference: [Z] points
- Explanation: [why they differ]
- Weighted Estimate: [W]%   (weights: [w1]/[w2], because ...)
```

The weighted estimate is the prior for Phase 3.

---

## Phase 3: The inside view (update with evidence)

```
Phase 3 Progress:
- [ ] Step 3.1: Gather specific evidence (web search)
- [ ] Step 3.2: Bayesian updating (one update per piece of evidence)
```

### Step 3.1 Evidence search families

At least 3-5 distinct searches, covering different families:

1. Recent news: "[topic] latest news [current year]"
2. Expert opinion: "[topic] expert forecast", "[topic] analysis"
3. Market prices: "[event] prediction market", "[event] betting odds"
4. Statistical data: "[topic] statistics", "[topic] data"
5. Research: "[topic] research study"

Share findings as they arrive, ask "Do you have insider knowledge or other sources?", and log everything:

```
Evidence from Web Search:
1. [Finding] - Source: [URL] - Date: [publication date]
2. [Finding] - Source: [URL] - Date: [publication date]
3. [Finding] - Source: [URL] - Date: [publication date]
[User-provided evidence, if any]
```

### Step 3.2 Bayesian updating

Load `bayesian-reasoning-calibration`. Prior = the weighted estimate from Phase 2. For each piece of evidence: present it; rate its strength (weak / moderate / strong); set a likelihood ratio and say why ("I think LR = [X]; do you agree?"); compute the posterior; show the move ("this took us from [X]% to [Y]%"); ask whether the magnitude seems right; make the posterior the next prior. Drop evidence with LR near 1. After the last update ask: "Are there other factors we should consider?"

Manual fallback: posterior = prior x LR / (prior x LR + (1 - prior)); use LR 1.5 for weak, 3 for moderate, 10 for strong evidence.

```
Prior: [starting %]

Evidence #1: [Description]
- Source: [URL]
- Likelihood Ratio: [X]
- Update: [Prior]% -> [Posterior]%
- Reasoning: [why this LR]

Evidence #2: ...

Bayesian Updated Probability: [Final]%
```

---

## Phase 4: Stress test and bias check

```
Phase 4 Progress:
- [ ] Step 4.1a: Run the premortem - imagine failure
- [ ] Step 4.1b: Identify failure modes
- [ ] Step 4.1c: Quantify and adjust
- [ ] Step 4.2a: Run the bias tests
- [ ] Step 4.2b: Debias and adjust
```

### Step 4.1 Premortem

Load `forecast-premortem`: procedure 1 (failure premortem), or procedure 2 when the posterior is below 20%; procedure 4 for tail risks, kill criteria, and signposts. Manual fallback: "It is [resolution date] and the prediction failed. What caused it?" Capture the user's failure scenarios, add your own, describe each concretely, search for historical rates of each cause, estimate each, sum them.

Compare: sum of failure-mode probabilities vs `100 - forecast` (the implied failure). If the premortem sum is larger, lower the forecast, or explain the overlap.

```
Premortem Failure Modes:
1. [Failure Mode 1]: [X]% (description + source)
2. [Failure Mode 2]: [Y]% (description + source)
3. [Failure Mode 3]: [Z]% (description + source)

Total Failure Probability: [Sum]%
Current Implied Failure: [100 - forecast]%
Adjustment Needed: [Yes/No - by how much]

Post-Premortem Probability: [Adjusted]%
```

### Step 4.2 Bias tests

Load `scout-mindset-bias-check` and run its procedures 1-4, then 5. The four mandatory tests, with the question that settles each:

| Test | Question | Pass | Fail |
|---|---|---|---|
| Reversal | If the evidence pointed the opposite way, would we accept it as readily? | Yes; truth-seeking | No; confirmation bias; move 10-15 points toward 50% |
| Scope sensitivity | If the scale changed 10x (timeline doubled, funding tenfold), should the forecast change proportionally? | Yes; forecast is sensitive | Barely moves; scope insensitivity |
| Status quo (if predicting "no change") | Are we assuming "no change" by default without evidence? | Evidence supports the status quo | Defaulting to it; cut P(status quo) 10-20 points |
| Overconfidence (surprise test) | Would we be genuinely shocked if the outcome fell outside the interval? | Shocked; CI appropriate | Not shocked; widen 1.5x-2x |

Then the full audit: confirmation, availability, anchoring, affect heuristic, overconfidence, attribution. For each detected bias: name it and the reason, ask whether the user agrees, agree the correction, adjust the probability and/or the interval. Set the 80% CI.

```
Bias Check Results:
- Reversal Test: [Pass/Fail - adjustment if needed]
- Scope Sensitivity: [Pass/Fail - adjustment if needed]
- Status Quo Bias: [N/A or adjustment if needed]
- Overconfidence Check: [CI width appropriate? adjustment if needed]
- Other biases detected: [list with adjustments]

Post-Bias-Check Probability: [Adjusted]%
Confidence Interval (80%): [Low]% - [High]%
```

---

## Phase 5: Final calibration and output

```
Phase 5 Progress:
- [ ] Step 5.1: Set confidence intervals
- [ ] Step 5.2: Identify kill criteria
- [ ] Step 5.3: Set monitoring signposts
- [ ] Step 5.4: Final output
```

### Step 5.1 Confidence interval

The CI reflects uncertainty, not confidence. Width is driven by the premortem findings, the bias check, the reference-class variance, the evidence quality, and the user's own uncertainty. Default: 80% CI (10th to 90th percentile). Propose the range, run the surprise test on both ends, adjust.

```
Confidence Interval (80%): [Low]% - [High]%
Reasoning: [why this width]
- Evidence quality: [Strong/Moderate/Weak]
- Premortem risk: [High/Medium/Low]
- User uncertainty: [High/Medium/Low]
```

### Step 5.2 Kill criteria

From the top 3-5 failure modes, each in the form "If [event X] happens, probability drops to [Y]%". Ask the user for the revised probability per scenario and whether these are the right triggers.

```
Kill Criteria:
1. If [Event A] -> probability drops to [X]%
2. If [Event B] -> probability drops to [Y]%
3. If [Event C] -> probability drops to [Z]%
```

### Step 5.3 Monitoring signposts

For each kill criterion: the early warning signals, and a check frequency (daily / weekly / monthly / quarterly). Ask whether the user can actually track them.

```
| Kill Criterion | Warning Signals | Check Frequency |
|----------------|-----------------|-----------------|
| [Event 1]      | [Indicators]    | [Frequency]     |
| [Event 2]      | [Indicators]    | [Frequency]     |
| [Event 3]      | [Indicators]    | [Frequency]     |
```

### Step 5.4 Final output

Fill the Final Output Template from SOUL.md: question restatement, final probability and CI, the complete reasoning pipeline (all five phases), risk monitoring (kill criteria and signposts), and the forecast quality metrics. Close with: "Does this forecast make sense? Any adjustments needed?"

### Forecast quality metrics (definitions)

- **Brier risk:** High if predicting an extreme (>90% or <10%); Low if moderate (30-70%). Extreme forecasts are penalised hardest when wrong.
- **Evidence quality:** Strong = multiple independent sources with quantitative data; Weak = anecdotal, single source, qualitative.
- **Confidence assessment:** High = narrow CI, strong evidence, low failure-mode risk; Low = wide CI, weak evidence, high failure-mode risk.

---

## Loading skills: what "let the skill do its work" means here

- Load the skill with `skill_view` at the step that names it, read its procedure, and follow it. Do not paraphrase what the skill would do and move on; the skill's checklist, tables, and thresholds are the method.
- Announce the step in one line ("Loading `reference-class-forecasting` to establish the base rate") so the user can follow the pipeline, then continue from where the skill's output leaves off.
- If a skill cannot be loaded, use the manual fallback in this file for that step, say that the fallback was used, and treat the step's output as lower confidence.
- Several skills in sequence is the normal case: base rate, then decomposition, then Bayesian update, then premortem, then bias check. Never reorder them.
