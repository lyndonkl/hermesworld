---
name: scout-mindset-bias-check
description: Test a forecast for motivated reasoning and cognitive bias.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: forecasting
    tags: [Cognitive Bias, Scout Mindset, Debiasing, Calibration, Forecasting]
    related_skills: [forecast-premortem, reference-class-forecasting, bayesian-reasoning-calibration]
---
# Scout Mindset and Bias Check

Detects and removes cognitive biases from a forecast using Julia Galef's Scout Mindset framework: a reversal test, a scope sensitivity check, a status quo test, a confidence-interval audit, and a full bias audit, each ending in a concrete probability or interval adjustment. It maps the territory rather than defending a position. It does not generate evidence or failure modes; it checks how the ones already gathered were weighed.

**Core principle:** biases systematically distort probabilities, emotional attachment clouds judgment, and motivated reasoning leads to overconfidence. Forecasting requires intellectual honesty.

## When to Use

- A prediction feels emotional, or the forecaster wants a particular answer.
- A forecast is stuck at 50/50 or refuses to move with evidence.
- Validating the forecasting process before a number is published.
- A confidence interval needs an audit for overconfidence.
- The user mentions scout mindset, soldier mindset, bias check, reversal test, scope sensitivity, or cognitive distortions.

## Procedures

1. [Run the reversal test](#1-run-the-reversal-test): would the opposite evidence be accepted as readily?
2. [Check scope sensitivity](#2-check-scope-sensitivity): do probabilities scale with the inputs?
3. [Test status quo bias](#3-test-status-quo-bias): is "no change" assumed by default?
4. [Audit confidence intervals](#4-audit-confidence-intervals): does the CI width reflect true uncertainty?
5. [Run the full bias audit](#5-run-the-full-bias-audit): a systematic scan of the major biases.
6. [Learn the framework](#6-learn-the-framework): the reference files.

In the superforecaster pipeline procedures 1-4 are the four mandatory tests, and procedure 5 follows them.

---

## 1. Run the reversal test

```
Reversal Test Progress:
- [ ] Step 1: State the current conclusion
- [ ] Step 2: Identify supporting evidence
- [ ] Step 3: Reverse the evidence
- [ ] Step 4: Ask "Would I still accept it?"
- [ ] Step 5: Adjust for double standards
```

**Step 1.** Prediction: [event]. Probability: [X]%. Direction: high or low confidence.

**Step 2.** List the evidence that supports the conclusion. Example, "Candidate A will win (75%)": polls show A ahead by 5%; A has more campaign funding; expert pundits favour A; A has better debate ratings.

**Step 3.** Imagine the same evidence pointed the OTHER way: polls showed B ahead, B had more funding, experts favoured B, B had better ratings.

**Step 4.** The critical question:
> If this reversed evidence existed, would I accept it as valid and change my prediction?

- **A) YES, I would accept the reversed evidence.** No bias detected; continue.
- **B) NO, I would dismiss it.** Warning: motivated reasoning. Evidence is accepted when it supports the view and dismissed when it does not (special pleading).
- **C) UNSURE.** Warning: asymmetric evidence standards suggest rationalising, not reasoning.

**Step 5.** If B or C: ask why the evidence is dismissed in one direction and accepted in the other. Is there an objective reason, or a preference? Common rationalisations: "this source is biased" (only when it disagrees); "sample size too small" (only for unfavourable polls); "outlier data" (only for disliked data); "context matters" (invoked selectively).

The fix: reject the evidence entirely (if it would not be trusted reversed, do not trust it now), or accept it in both directions, or weight it as weak both ways.

**Probability adjustment:** if double standards were detected, move the probability 10-15 points toward 50%.

---

## 2. Check scope sensitivity

```
Scope Sensitivity Progress:
- [ ] Step 1: Identify the variable scale
- [ ] Step 2: Test linear scaling
- [ ] Step 3: Check reference point calibration
- [ ] Step 4: Validate magnitude assessment
- [ ] Step 5: Adjust for scope insensitivity
```

**Step 1.** What dimension has magnitude? Number of people (100 vs 10,000 vs 1,000,000), dollar amounts ($1K vs $100K vs $10M), time (1 month vs 1 year vs 10 years).

**Step 2. The linearity test.** Double the input; check whether the impact doubles. Example, startup funding: if it raised $1M: ___%; $10M: ___%; $100M: ___%. If the probabilities barely changed, the forecast is scope insensitive.

**Step 3. The anchoring test.** Did the estimate start from a number (base rate, someone else's forecast, a round number) and adjust insufficiently? Fix: generate the probability from scratch without looking at others, then compare and reconcile. Do not just split the difference; reason about why the estimates differ.

**Step 4. The "1 vs 10 vs 100" test.** Vary the scale by 10x. Example, project timeline: 1 month P(success) = ___%; 10 months = ___%; 100 months = ___%. The probability should change a lot. If all three are within 10 points, scope insensitivity.

**Step 5. Adjust.** The emotional system responds to the category, not the magnitude. Fixes:
- **Logarithmic scaling:** use a log scale for intuition.
- **Reference class by scale:** not "startups" but "startups that raised $1M" (10% success) vs "startups that raised $100M" (60% success).
- **Explicit calibration:** P(success) = base_rate + k x log(amount).

---

## 3. Test status quo bias

```
Status Quo Bias Progress:
- [ ] Step 1: Identify a status quo prediction
- [ ] Step 2: Calculate the energy to maintain the status quo
- [ ] Step 3: Invert the default
- [ ] Step 4: Apply the entropy principle
- [ ] Step 5: Adjust probabilities
```

**Step 1.** Is this a "no change" prediction? "This trend will continue", "market share will stay the same", "policy won't change". Status quo predictions get inflated probabilities because change feels risky.

**Step 2. The entropy principle.** Without active energy input, systems decay toward disorder. What effort is required to keep things the same? Market share: maintaining it requires matching competitor innovation; energy high; status quo is HARD. Policy: maintaining it requires no proposals for change; energy low; status quo is easier.

**Step 3. Invert the default.** Normal framing: "Will X change?" (default no). Inverted: "Will X stay the same?" (default no). If P(change) + P(same) != 100%, there is status quo bias.

**Step 4.** Is the system open or closed? Is energy being put in to maintain or improve it? Is that energy sufficient?

**Step 5. Adjust.** For "no change" predictions that require high energy: reduce P(status quo) by 10-20 points and raise P(change) to match. Where inertia genuinely helps, no adjustment. Heuristic: if maintaining the status quo takes active effort, decay is more likely than it feels.

---

## 4. Audit confidence intervals

```
Confidence Interval Audit Progress:
- [ ] Step 1: State the current CI
- [ ] Step 2: Run the surprise test
- [ ] Step 3: Check historical calibration
- [ ] Step 4: Compare to reference class variance
- [ ] Step 5: Adjust the CI width
```

**Step 1.** Point estimate ___%, lower bound ___%, upper bound ___%, width ___ points, confidence level ___ (usually 80% or 90%).

**Step 2. The surprise test.** "Would I be **genuinely shocked** if the true value fell outside this interval?" An 80% CI should shock 20% of the time; a 90% CI, 10%. Imagine the outcome just below the lower bound and just above the upper bound.
- **A) "Yes, very surprised."** CI appropriately calibrated.
- **B) "No, not that surprised."** CI too narrow (overconfident); widen.
- **C) "I'd be amazed if it landed in the range."** CI too wide; narrow.

**Step 3. Historical calibration.** Collect the last 20-50 forecasts with CIs, count how many outcomes fell outside, compare to expectation.

| CI Level | Expected Outside | Your Actual |
|----------|------------------|-------------|
| 80% | 20% | ___% |
| 90% | 10% | ___% |

Actual > expected means CIs too narrow (overconfident), the most common finding.

**Step 4. Reference class variance.** If reference class data exists, its standard deviation should roughly match the CI. Example: reference class SD 12%, so an 80% CI of about point estimate +/- 15%. A CI narrower than the reference class variance claims to know more than average; justify it or widen.

**Step 5. Adjust.** If overconfident: multiply the width by 1.5x to 2x. If underconfident: reduce the width to 0.5x-0.75x.

---

## 5. Run the full bias audit

```
Full Bias Audit Progress:
- [ ] Step 1: Confirmation bias check
- [ ] Step 2: Availability bias check
- [ ] Step 3: Anchoring bias check
- [ ] Step 4: Affect heuristic check
- [ ] Step 5: Overconfidence check
- [ ] Step 6: Attribution error check
- [ ] Step 7: Prioritise and remediate
```

See [cognitive-bias-catalog.md](references/cognitive-bias-catalog.md) for detailed descriptions. Quick audit questions; a NO to any question in a group means that bias is detected:

1. **Confirmation bias.** Did I seek disconfirming evidence? Give equal weight to evidence against my position? Actively try to prove myself wrong?
2. **Availability bias.** Did I rely on recent or memorable examples? Use systematic data rather than "what comes to mind"? Check that my examples are representative?
3. **Anchoring bias.** Did I generate my estimate independently first? Avoid being influenced by others' numbers? Adjust sufficiently from the initial anchor?
4. **Affect heuristic.** Do I have an emotional preference for the outcome? Did I separate "what I want" from "what will happen"? Would I make the same forecast with reversed incentives?
5. **Overconfidence.** Did I run a premortem? Are my CIs wide enough (surprise test)? Did I identify ways I could be wrong?
6. **Fundamental attribution error.** Did I attribute success to skill vs luck appropriately? Consider situational factors, not just personal traits? Avoid "great man" narratives?

**Step 7: Prioritise and remediate.** For each detected bias record severity (High/Medium/Low), direction (pushing the probability up or down), and magnitude (estimated percentage-point impact).

| Bias | Severity | Direction | Adjustment |
|------|----------|-----------|------------|
| Confirmation | High | Up | -15% |
| Availability | Medium | Up | -10% |
| Affect heuristic | High | Up | -20% |

Net adjustment: -45 points (e.g. 80% -> 35%). Adjustments this large mean the earlier phases must be revisited, not just the number.

---

## 6. Learn the framework

Load with `skill_view("scout-mindset-bias-check", file_path="references/<file>")`.

- [scout-vs-soldier.md](references/scout-vs-soldier.md): Julia Galef's framework, motivated reasoning, intellectual honesty, identity and beliefs.
- [cognitive-bias-catalog.md](references/cognitive-bias-catalog.md): 20+ major biases, how they affect forecasting, detection methods, remediation strategies.
- [debiasing-techniques.md](references/debiasing-techniques.md): systematic debiasing process, pre-commitment strategies, external accountability, algorithmic aids.

---

## Quick Reference

### The scout commandments

1. **Truth over comfort.** Accuracy beats wishful thinking.
2. **Seek disconfirmation.** Try to prove yourself wrong.
3. **Hold beliefs lightly.** Probabilistic, not binary.
4. **Update incrementally.** Change your mind with evidence.
5. **Separate wanting from expecting.** Desire is not a forecast.
6. **Check your work.** Run bias audits routinely.
7. **Stay calibrated.** Track accuracy over time.

> Scout mindset is the drive to see things as they are, not as you wish them to be.

### Integration with other skills

- **Before:** `forecast-premortem` supplies the failure modes the overconfidence check relies on.
- **Companion:** `reference-class-forecasting`, to confirm the reference class was not cherry-picked.
- **After:** the adjusted probability and interval go straight into the final calibration.

## Pitfalls

- Passing every test by reflex. A bias check with no adjustments on a contested question is itself a warning sign.
- Adjusting the number without naming the bias and its direction, which cannot be audited later.
- Treating the surprise test as rhetorical. Actually picture the value just outside each bound.
- Running the audit once and never re-running it after new evidence changes the picture.

## Verification

All four tests (reversal, scope sensitivity, status quo, surprise) have a recorded pass or fail with one sentence of reasoning; every detected bias has a direction and a magnitude in percentage points; and the surprise-test answer is "yes, shocked" for both ends of the final interval.
