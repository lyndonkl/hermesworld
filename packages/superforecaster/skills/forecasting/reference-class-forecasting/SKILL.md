---
name: reference-class-forecasting
description: Anchor a forecast on the base rate of similar past cases.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: forecasting
    tags: [Forecasting, Base Rates, Outside View, Reference Class, Superforecasting]
    related_skills: [estimation-fermi, bayesian-reasoning-calibration, scout-mindset-bias-check]
---
# Reference Class Forecasting

Anchors a prediction in historical reality. Identify the class of similar past events, take their statistical frequency as the starting probability (the outside view), and only then look at what is specific to this case. The output is a base rate, a confidence grade for it, and a bound on how far the inside view may move it. Weighing the case-specific evidence itself belongs to `bayesian-reasoning-calibration`.

## When to Use

- Starting a forecast or prediction, before analysing the specifics of the case.
- Establishing a base rate or statistical baseline for an event.
- Testing a "this time is different" claim or any argument that a case is unique.
- The user mentions reference classes, the outside view, base rates, or starting a new prediction.
- No single published base rate exists and a multi-stage funnel has to be built instead.

## Procedures

1. [Find the base rate](#1-find-the-base-rate): identify the reference class and its statistical baseline.
2. [Test "this time is different"](#2-test-this-time-is-different): challenge uniqueness claims.
3. [Calculate funnel base rates](#3-calculate-funnel-base-rates): multi-stage probability chains when no single statistic exists.
4. [Validate the reference class](#4-validate-the-reference-class): too broad vs too narrow, homogeneity, sample size.
5. [Learn the framework](#5-learn-the-framework): the reference files.

In the superforecaster pipeline procedure 1 is mandatory, procedure 4 is run on its result, and procedures 2 and 3 are called when the case demands them. The pipeline's own per-phase checklists and hand-off formats are in [superforecaster-protocol.md](references/superforecaster-protocol.md).

---

## 1. Find the base rate

### Step 1: State what is being forecast

Write the specific event or outcome as a resolvable proposition: what happens, at what threshold, by when.

Examples: "Will this startup raise a Series A within 18 months?", "Will this bill pass Congress this session?", "Will this project launch by the planned date?"

### Step 2: Identify the reference class

Decide which bucket the case belongs to.

- Too broad: "All companies" -> meaningless
- Just right: "Seed-stage B2B SaaS startups in fintech"
- Too narrow: "Companies founded by people named Steve in 2024" -> no data

Key questions:
1. What type of entity is this? (company, bill, project, person, ...)
2. What stage, size, or category?
3. What industry or domain?
4. What time period is relevant?

Refine with the user's domain knowledge until the class is specific and searchable, and state it explicitly: "The reference class is [X], because [reasons]."

### Step 3: Search for historical data

Find the base rate with `web_search` for published statistics, academic studies on success rates, and government or industry reports, then `web_extract` the figures from the pages found. Use proxy metrics when direct data is unavailable. Run at least two or three distinct queries.

Search strategy:
```
"historical success rate of [reference class]"
"[reference class] failure statistics"
"[reference class] survival rate"
"what percentage of [reference class]"
```

Record every hit as `[figure] - Source: [URL]`. If nothing turns up, say so and list the queries tried. Do not fill the gap from memory.

### Step 4: Set the anchor

The base rate found becomes the starting probability.

> Treat this base rate as the starting point. Adjust only for specific, evidence-based reasons from the inside-view analysis.

Default anchors when no data can be found (label them as assumptions):
- Novel innovation: 10-20% (most innovations fail)
- Established industry: 50% (uncertain)
- Regulated or proven process: 70-80% (systems work)

Hand forward: base rate, reference class, sample size, sources, and the High/Medium/Low confidence grade from procedure 4.

---

## 2. Test "this time is different"

When anyone, including the forecaster, believes "this case is special", stress-test that belief.

### The uniqueness audit

**Question 1: Similarity matching**
- What are the five historical cases most similar to this one?
- For each, what was the outcome?
- How is this case materially different from them?

**Question 2: The reversal test**
- If someone claimed a different case was "unique" for the same reasons, would the claim be accepted?
- Is this special pleading?

**Question 3: Burden of proof**
The base rate says [X]%. The claim is that it should be [Y]%. Calculate the gap `|Y - X|`.

Required evidence strength:
- Gap < 10 points: minimal evidence needed
- Gap 10-30 points: moderate evidence needed (2-3 specific factors)
- Gap > 30 points: extraordinary evidence needed (multiple independent strong signals)

### Output

1. Whether "this time is different" is justified.
2. How far the estimate may reasonably move from the base rate.
3. What evidence would be needed to justify a larger move.

---

## 3. Calculate funnel base rates

For multi-stage processes without a single base rate: no direct statistic exists, the event requires several sequential steps, and each stage has its own probability.

### The funnel method

Example: "Will Bill X become law?" There is no data on "Bill X success rate", but the funnel can be modelled:

1. Bills introduced -> bills that reach committee: P(committee | introduced) = ?
2. Bills in committee -> bills that reach a floor vote: P(floor | committee) = ?
3. Bills voted on -> bills that pass: P(pass | floor vote) = ?

```
P(law) = P(committee) x P(floor) x P(pass)
```

### Process

1. Decompose the event into sequential stages.
2. Search for statistics on each stage.
3. Multiply the probabilities (product rule).
4. Validate the model: are the stages really independent? Correlated stages make the product too low.

Common funnels:
- Startup success: Seed -> Series A -> Profitability -> Exit
- Drug approval: Discovery -> Trials -> FDA -> Market
- Project delivery: Planning -> Development -> Testing -> Launch

When the funnel needs more than a product of stage rates, load `estimation-fermi`.

---

## 4. Validate the reference class

### The three tests

**Test 1: Homogeneity.** Are the members of this class similar enough? Is the variance in outcomes high? Should it be subdivided? Example: "Tech startups" is too broad (consumer, B2B, and hardware differ a lot). Subdivide.

**Test 2: Sample size.** Are there enough historical cases? Minimum 20-30 for meaningful statistics. If N < 20, widen the class or acknowledge high uncertainty.

**Test 3: Relevance.** Have conditions changed since the data was collected? Are there structural differences (regulation, technology, market)? Data more than 10 years old may be stale.

### Validation checklist

- [ ] Class has 20+ historical examples
- [ ] Members are reasonably homogeneous
- [ ] Data is from a relevant time period
- [ ] No major structural change since data collection
- [ ] Class is specific enough to be meaningful
- [ ] Class is broad enough to have data

Output: confidence in the reference class, High / Medium / Low.

---

## 5. Learn the framework

Load with `skill_view("reference-class-forecasting", file_path="references/<file>")`.

- [outside-view-principles.md](references/outside-view-principles.md): statistical vs narrative thinking, why the outside view beats experts, Kahneman's planning-fallacy research, when the outside view fails.
- [reference-class-selection.md](references/reference-class-selection.md): systematic method for choosing comparison sets, balancing specificity against data availability, similarity metrics, edge cases.
- [common-pitfalls.md](references/common-pitfalls.md): base rate neglect, "this time is different" bias, overfitting to small samples, ignoring regression to the mean, availability bias in class selection.
- [superforecaster-protocol.md](references/superforecaster-protocol.md): the five-phase pipeline's checklists, hand-off record formats, question scripts, and manual fallbacks (used by the superforecaster agent).

---

## Quick Reference

### The outside view commandments

1. **Base rate first:** establish the statistical baseline before analysing specifics.
2. **Assume average:** treat the case as typical until proven otherwise.
3. **Burden of proof:** large deviations from the base rate require strong evidence.
4. **Class precision:** the reference class should be specific but data-rich.
5. **No narratives:** resist compelling stories; trust frequencies.

> Find what usually happens to things like this, start there, and only move with evidence.

### Integration with other skills

- **Before:** `estimation-fermi` when the base rate must be built from components.
- **After:** `bayesian-reasoning-calibration` to update from the base rate with new evidence.
- **Companion:** `scout-mindset-bias-check` to confirm the reference class was not cherry-picked.

## Pitfalls

- Picking the class that gives the answer you expected. Choose the class before looking at its rate.
- Quoting a rate without its N. A 70% success rate from 6 cases is an anecdote.
- Treating a proxy rate as the real one without saying so.
- Stacking a funnel of correlated stages and calling the product a base rate.

## Verification

The base rate is ready to hand forward when every line of the validation checklist in procedure 4 is ticked or the unticked lines are written down as caveats, and every figure in the hand-off carries a source URL or the label "assumption". A hand-off with a number but no source fails.
