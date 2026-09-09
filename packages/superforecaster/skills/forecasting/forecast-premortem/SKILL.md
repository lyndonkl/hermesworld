---
name: forecast-premortem
description: Assume the forecast failed and work back to failure modes.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: forecasting
    tags: [Premortem, Stress Test, Tail Risk, Kill Criteria, Forecasting]
    related_skills: [bayesian-reasoning-calibration, scout-mindset-bias-check, reference-class-forecasting]
---
# Forecast Pre-Mortem

Stress-tests a prediction by assuming it has already failed and working backward to explain why. Gary Klein's premortem technique, applied to probabilistic forecasting, surfaces blind spots, tail risks, and overconfidence, and turns them into quantified failure modes, kill criteria, and monitoring signposts. It does not replace the evidence update that precedes it; it tests whether that update has left anything out.

**Core principle**: invert the problem. Instead of "Will this succeed?", ask "It has failed. Why?"

## When to Use

- Confidence is high (>80%) or low (<20%) and needs a stress test before it is published.
- Tail risks and unknown unknowns must be identified for a forecast or plan.
- A confidence interval feels too narrow and needs a principled reason to widen.
- Kill criteria and early-warning signposts are needed for monitoring a live forecast.
- The user mentions a premortem, backcasting, what could go wrong, a stress test, or black swans.

## Procedures

1. [Run a failure premortem](#1-run-a-failure-premortem): assume the prediction failed and explain why.
2. [Run a success premortem](#2-run-a-success-premortem): for pessimistic predictions (<20%).
3. [Dragonfly eye perspective](#3-dragonfly-eye-perspective): view failure through several conflicting lenses.
4. [Identify tail risks](#4-identify-tail-risks): find black swans, then set kill criteria and signposts.
5. [Adjust confidence intervals](#5-adjust-confidence-intervals): quantify the adjustment.
6. [Learn the framework](#6-learn-the-framework): the reference files.

In the superforecaster pipeline procedure 1 (or 2 when the forecast is below 20%) is mandatory, procedure 4 supplies the kill criteria and signposts for the final output, and procedures 3 and 5 are used when the first pass leaves the adjustment unclear.

---

## 1. Run a failure premortem

```
Failure Premortem Progress:
- [ ] Step 1: State the prediction and current confidence
- [ ] Step 2: Time travel to failure
- [ ] Step 3: Write the history of failure
- [ ] Step 4: Identify concrete failure modes
- [ ] Step 5: Assess plausibility and adjust
```

### Step 1: State the prediction and current confidence

Record: (1) what is being predicted, (2) the current probability, (3) the current confidence interval.

Example: "This startup will reach $10M ARR within 2 years." Probability: 75%, CI: 60-85%.

### Step 2: Time travel to failure

**The crystal ball exercise.** Jump forward to the resolution date. **It is now [resolution date]. The event did NOT happen.** This is a certainty; do not argue with it.

How does it feel? Surprising? Expected? Shocking? The emotional response is information about true confidence.

### Step 3: Write the history of failure

**Backcasting narrative.** Starting from the failure point, work backward in time and write the story of how it happened.

Prompts:
- "The headlines that led to this were..."
- "The first sign of trouble was when..."
- "In retrospect, we should have known because..."
- "The critical mistake was..."

Frameworks to consider:
- **Internal friction:** team burned out, co-founders fought, execution failed
- **External shocks:** regulation changed, competitor launched, market shifted
- **Structural flaws:** unit economics did not work, market too small, tech did not scale
- **Black swans:** pandemic, war, financial crisis, unexpected disruption

See [failure-mode-taxonomy.md](references/failure-mode-taxonomy.md) for the full set of categories.

### Step 4: Identify concrete failure modes

Extract specific, actionable failure causes from the narrative. For each: (1) what happened, (2) why it caused failure, (3) how likely it is, (4) early warning signals. Where a historical failure rate exists, find it with `web_search` ("[domain] failure rate [cause]") rather than guessing.

| Failure Mode | Mechanism | Likelihood | Warning Signals |
|--------------|-----------|------------|-----------------|
| Key engineer quit | Lost technical leadership, delayed product | 15% | Declining code commits, complaints |
| Competitor launched free tier | Destroyed unit economics | 20% | Hiring spree, beta leaks |
| Regulation passed | Made business model illegal | 5% | Proposed legislation, lobbying |

### Step 5: Assess plausibility and adjust

**The plausibility test.**
- How easy was it to write the failure narrative? Very easy: drop confidence by 15-30%. Very hard, felt absurd: confidence was appropriate.
- How many plausible failure modes appeared? 5+ modes each >5% likely: too much uncertainty for high confidence. 1-2 modes, low likelihood: confidence can stay high.
- Were any unknown unknowns discovered? Yes, several: widen the confidence interval by 20%. No, all known risks: confidence appropriate.

**Quantitative method.** Sum the probabilities of the failure modes:
```
P(failure) = P(mode_1) + P(mode_2) + ... + P(mode_n)
```
If this sum is greater than `1 - current_probability`, the probability is too high. (Where modes overlap heavily, treat the sum as an upper bound and say so.)

Example: current success 75% (implied failure 25%); sum of failure modes 40%. Conclusion: failure risk is underestimated by 15 points; adjusted success 60%.

---

## 2. Run a success premortem

For pessimistic predictions: assume the unlikely success happened.

```
Success Premortem Progress:
- [ ] Step 1: State the pessimistic prediction (<20%)
- [ ] Step 2: Time travel to success
- [ ] Step 3: Write the history of success
- [ ] Step 4: Identify how you could be wrong
- [ ] Step 5: Assess and adjust upward if needed
```

**Step 1.** Record the low-probability event and why confidence is so low. Example: "Fusion energy will be commercialised by 2030." Probability 10%; reasoning: technical challenges too great.

**Step 2.** It is now 2030. Fusion energy is commercially available. This happened. How?

**Step 3.** Backcast the unlikely: "The breakthrough came when...", "We were wrong about [assumption] because...", "The key enabler was...", "In retrospect, we underestimated..."

**Step 4.** Challenge the pessimism: anchoring too heavily on current constraints? underestimating exponential progress? ignoring parallel approaches? biased by past failures?

**Step 5.** If the success narrative was surprisingly plausible, increase the probability.

---

## 3. Dragonfly eye perspective

View the failure through several conflicting perspectives. The dragonfly's compound eye sees from many angles at once; simulate it by adopting radically different viewpoints.

```
Dragonfly Eye Progress:
- [ ] Step 1: The Skeptic (why this will definitely fail)
- [ ] Step 2: The Fanatic (why failure is impossible)
- [ ] Step 3: The Disinterested Observer (neutral analysis)
- [ ] Step 4: Synthesize perspectives
- [ ] Step 5: Extract robust failure modes
```

**Step 1: The Skeptic.** Channel the harshest critic: a short-seller, a competitor, a pessimist. Why will this DEFINITELY fail? Be extreme: worst case, every flaw, no charity. Output: failure reasons from the skeptical view.

**Step 2: The Fanatic.** Channel the strongest believer: the founder's mother, a zealot, an optimist. Why is failure IMPOSSIBLE? Be extreme: best case, every strength, maximum charity. Output: success reasons from the optimistic view.

**Step 3: The Disinterested Observer.** Channel a neutral analyst with no stake, running a simulation and reading the data dispassionately: pure statistical and reference-class reasoning. Output: a balanced probability with reasoning.

**Step 4: Synthesise.** Which failure modes appeared in ALL THREE perspectives? The skeptic named it, even the fanatic could not dismiss it, and the observer found it statistically. These are the robust failure modes, the ones most likely to happen.

**Step 5: Extract robust failure modes.**

| Failure Mode | Skeptic | Fanatic | Observer | Robust? |
|--------------|---------|---------|----------|---------|
| Market too small | Definitely | Debatable | Base rate suggests yes | YES |
| Execution risk | Definitely | No way | 50/50 | Maybe |
| Tech won't scale | Definitely | Already solved | Unknown | Investigate |

Focus the adjustment on the robust failures that survived all perspectives.

---

## 4. Identify tail risks

```
Tail Risk Identification Progress:
- [ ] Step 1: Define what counts as "tail risk"
- [ ] Step 2: Systematic enumeration
- [ ] Step 3: Impact x Probability matrix
- [ ] Step 4: Set kill criteria
- [ ] Step 5: Monitor signposts
```

**Step 1: Define tail risk.** Low probability (<5%), high impact (would completely change the outcome), outside normal planning, often an exogenous shock. Examples: pandemic, war, financial crisis, regulatory ban, key-person death, natural disaster, technological disruption.

**Step 2: Systematic enumeration.** Use PESTLE for coverage and ask, for each category, "What low-probability event would kill this prediction?"
- **Political:** elections, coups, policy changes, geopolitical shifts
- **Economic:** recession, inflation, currency crisis, market crash
- **Social:** cultural shifts, demographic changes, social movements
- **Technological:** breakthrough inventions, disruptions, cyber attacks
- **Legal:** new regulations, lawsuits, IP challenges, compliance changes
- **Environmental:** climate events, pandemics, natural disasters

See [failure-mode-taxonomy.md](references/failure-mode-taxonomy.md) for detailed categories.

**Step 3: Impact x probability matrix.** Plot the tail risks; focus on high impact even when probability is very low.

```
High Impact
|
|  [Pandemic]        [Key Founder Dies]
|
|  [Recession]       [Competitor Emerges]
|
+-------------------------------------> Probability
  Low                              High
```

**Step 4: Set kill criteria.** For each major tail risk define the kill criterion in the form "If [event X] happens, probability drops to [Y]%".
- "If the FDA rejects the drug, probability drops to 5%"
- "If the key engineer quits, probability drops to 30%"
- "If a competitor launches a free tier, probability drops to 20%"
- "If the regulation passes, probability drops to 0%"

**Step 5: Monitor signposts.** For each kill criterion identify early warning signals and a check frequency.

| Kill Criterion | Warning Signals | Check Frequency |
|----------------|----------------|-----------------|
| FDA rejection | Phase 2 trial results, FDA feedback | Monthly |
| Engineer quits | Code velocity, satisfaction surveys | Weekly |
| Competitor launch | Hiring spree, beta leaks, patents | Monthly |
| Regulation | Proposed bills, lobbying, hearings | Quarterly |

Set up the monitoring: calendar reminders, news alerts, automated tracking.

---

## 5. Adjust confidence intervals

```
Confidence Interval Adjustment Progress:
- [ ] Step 1: State the current CI
- [ ] Step 2: Evaluate the premortem findings
- [ ] Step 3: Calculate the width adjustment
- [ ] Step 4: Set new bounds
- [ ] Step 5: Document the reasoning
```

**Step 1.** Current interval: lower bound __%, upper bound __%, width ___ percentage points.

**Step 2.** Score the premortem on four dimensions, 1-5 each:
1. **Narrative plausibility**: 1 = failure felt absurd, 5 = failure felt inevitable
2. **Number of failure modes**: 1 = only 1-2 unlikely modes, 5 = 5+ plausible modes
3. **Unknown unknowns discovered**: 1 = no surprises, 5 = many blind spots revealed
4. **Dragonfly synthesis**: 1 = perspectives diverged completely, 5 = all agreed on the failure modes

Total: __ / 20.

**Step 3.** Width multiplier = 1 + (score / 20). Score 4/20 -> 1.2 (widen 20%); 10/20 -> 1.5 (widen 50%); 16/20 -> 1.8 (widen 80%). Adjusted width = current width x multiplier.

**Step 4.** Symmetric widening around the current estimate: new lower = estimate - adjusted width / 2; new upper = estimate + adjusted width / 2. Clip at 0% and 100%. Example: estimate 70%, CI 60-80% (width 20), score 12/20, multiplier 1.6, new width 32, **new CI 54-86%**.

**Step 5.** Record which failure modes drove the adjustment, which perspective was most revealing, what unknown unknowns were discovered, and what will be monitored.

---

## 6. Learn the framework

Load with `skill_view("forecast-premortem", file_path="references/<file>")`.

- [premortem-principles.md](references/premortem-principles.md): why humans are overconfident, hindsight and outcome bias, the power of inversion, research on premortem effectiveness.
- [backcasting-method.md](references/backcasting-method.md): structured backcasting, temporal reasoning, causal chain construction, narrative vs quantitative backcasting.
- [failure-mode-taxonomy.md](references/failure-mode-taxonomy.md): failure categories, internal vs external, preventable vs unpreventable, PESTLE for tail risks, kill criteria templates.

---

## Quick Reference

### The premortem commandments

1. **Assume failure is certain.** Do not debate whether; debate why.
2. **Be specific.** Vague risks do not help; concrete mechanisms do.
3. **Use multiple perspectives.** Skeptic, fanatic, observer.
4. **Quantify failure modes.** Estimate the probability of each.
5. **Set kill criteria.** Know what would change your mind.
6. **Monitor signposts.** Track early warning signals.
7. **Widen CIs.** If the premortem was too easy, you were overconfident.

> Assume the prediction has failed, write the history of how, and use it to find blind spots and adjust confidence.

### Integration with other skills

- **Before:** run after the inside-view update; there must be something to stress-test.
- **After:** `scout-mindset-bias-check` validates the adjustments.
- **Companion:** `bayesian-reasoning-calibration` for the quantitative updates.
- **Feeds into:** the kill criteria and signposts of the final forecast.

## Pitfalls

- Listing risks in the abstract ("execution risk") instead of mechanisms that could be observed happening.
- Summing overlapping failure modes and treating the total as exact.
- Running the premortem and then leaving the probability where it was because the narrative was "just a story".
- Kill criteria without a revised probability attached, which makes them impossible to act on.

## Verification

Sum the probabilities of the failure modes you listed and compare the total with `1 - P(forecast)`. If the sum is larger, the forecast has not absorbed the premortem: lower it, or explain in writing why the modes overlap. Every kill criterion must name an observable event and a revised probability, and every one must have at least one warning signal with a check frequency.
