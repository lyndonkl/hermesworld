---
name: bayesian-reasoning-calibration
description: Update a probability with evidence via likelihood ratios.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: forecasting
    tags: [Bayesian, Calibration, Probability, Likelihood Ratio, Forecasting]
    related_skills: [reference-class-forecasting, estimation-fermi, forecast-premortem, scout-mindset-bias-check]
---
# Bayesian Reasoning and Calibration

Applies Bayes' theorem to move a probability estimate, one piece of evidence at a time, from an explicit prior to a documented posterior. Each update is justified by a likelihood ratio, so the reasoning can be audited and the forecast tracked for calibration later. It does not set the prior from nothing: that comes from `reference-class-forecasting` (base rate) or `estimation-fermi` (structural estimate).

## When to Use

- Making a prediction or judgment under uncertainty and new evidence has arrived.
- Forecasting an outcome, evaluating a probability, or testing competing hypotheses.
- Calibrating confidence or assessing a risk with uncertain data.
- Turning a base rate into a case-specific probability inside a forecasting pipeline.
- The user mentions priors, likelihoods, Bayes' theorem, probability updates, calibration, or belief revision.

**Core formula:** P(H|E) = P(E|H) x P(H) / P(E), where P(H) is the prior, P(E|H) the likelihood, and P(H|E) the posterior.

## Quick Example

```markdown
# Should we launch Feature X?

## Prior Belief
Before beta testing: 60% chance of adoption >20%
- Base rate: similar features get 15-25% adoption
- Our feature seems stronger than average
- Prior: 60%

## New Evidence
Beta test: 35% of users adopted (70 of 200 users)

## Likelihoods
If true adoption is >20%:
- P(seeing 35% in beta | adoption >20%) = 75% (likely to see a high beta if true)

If true adoption is <=20%:
- P(seeing 35% in beta | adoption <=20%) = 15% (unlikely to see a high beta if false)

## Bayesian Update
Posterior = (75% x 60%) / [(75% x 60%) + (15% x 40%)]
Posterior = 45% / (45% + 6%) = 88%

## Conclusion
Updated belief: 88% confident adoption will exceed 20%
Evidence strongly supports launch, but not certain.
```

## Procedure

Copy this checklist and track progress:

```
Bayesian Reasoning Progress:
- [ ] Step 1: Define the question
- [ ] Step 2: Establish prior beliefs
- [ ] Step 3: Identify evidence and likelihoods
- [ ] Step 4: Calculate the posterior
- [ ] Step 5: Calibrate and document
```

**Step 1: Define the question**

Clarify the hypothesis (a specific, testable claim), the probability to estimate, the timeframe (when the outcome is known), the success criteria, and why it matters (what decision depends on it). Example: "The feature will reach >20% adoption within 3 months", which matters for the launch decision.

**Step 2: Establish prior beliefs**

Set the initial probability from base rates (general frequency), a reference class (similar situations), the specific differences of this case, and an explicit probability with justification. Good priors rest on base rates, account for differences, are honest about uncertainty, and carry a range when unsure (e.g. 40-60%). Avoid purely intuitive priors, ignoring base rates, or extreme values without justification.

**Step 3: Identify evidence and likelihoods**

For each piece of evidence record the observation, its diagnostic power (does it separate the hypotheses?), P(E|H) (probability of seeing it if the hypothesis is true), P(E|not H) (probability if false), and the likelihood ratio LR = P(E|H) / P(E|not H). LR > 10 is very strong evidence, 3-10 moderate, 1-3 weak, about 1 not diagnostic (drop it), below 1 evidence against.

**Step 4: Calculate the posterior**

Apply Bayes' theorem, P(H|E) = [P(E|H) x P(H)] / P(E), or the odds form, Posterior Odds = Prior Odds x LR. Compute P(E) = P(E|H) x P(H) + P(E|not H) x P(not H), read off the posterior, and interpret the change. Chain updates by making each posterior the next prior. For simple cases use the calculator in `templates/template.md`; for several hypotheses study `references/methodology.md`.

**Step 5: Calibrate and document**

Check calibration (over- or under-confident?), validate the assumptions (are the likelihoods reasonable?), run a sensitivity analysis, write `bayesian-reasoning-calibration.md`, and note limitations. Self-check with `assets/evaluators/rubric_bayesian_reasoning_calibration.json`: prior based on base rates, likelihoods justified, evidence diagnostic (LR != 1), calculation correct, posterior calibrated, assumptions stated, sensitivity noted. Minimum standard: score >= 3.5.

## Common Patterns

**For forecasting:** start from base rates; update incrementally as evidence arrives; track forecast accuracy over time; calibrate by comparing predictions to outcomes.

**For hypothesis testing:** state the competing hypotheses explicitly; calculate a likelihood ratio for each piece of evidence; update in proportion to evidence strength; do not claim certainty unless the LR is extreme.

**For risk assessment:** consider several scenarios, not just a binary; update risks as data arrives; use ranges when unsure about likelihoods; run a sensitivity analysis.

**For avoiding bias:** force explicit priors (prevents anchoring on the evidence); use reference classes (prevents ignoring base rates); calculate mathematically (prevents motivated reasoning); document before the outcome is known (enables calibration).

## Guardrails

**Do:** state priors explicitly before seeing all the evidence; use base rates and reference classes; estimate likelihoods with justification; update incrementally; be honest about uncertainty; run a sensitivity analysis; track forecasts for calibration; acknowledge the limits of the model.

**Don't:** use extreme priors (1%, 99%) without exceptional justification; ignore base rates; treat all evidence as equally diagnostic; update to 100% certainty (almost never justified); cherry-pick evidence; skip documenting the reasoning; forget to calibrate against outcomes; apply the method where probability is meaningless.

## Pitfalls

- Counting the same fact twice because two sources report it. One underlying observation is one update.
- Letting a vivid single source carry an LR of 10. Ask what it would take to see that evidence if the hypothesis were false.
- Updating on evidence that was already priced into the base rate.
- Reporting the posterior without the chain of LRs that produced it; nobody can audit it later.

## Quick Reference

- **Standard template**: `templates/template.md`
- **Multiple hypotheses**: `references/methodology.md`
- **Worked example**: `references/example-product-launch.md`
- **Quality rubric**: `assets/evaluators/rubric_bayesian_reasoning_calibration.json`

**Bayesian formula (odds form)**:
```
Posterior Odds = Prior Odds x Likelihood Ratio
```

**Likelihood ratio**:
```
LR = P(Evidence | Hypothesis True) / P(Evidence | Hypothesis False)
```

**Output naming**: `bayesian-reasoning-calibration.md` or `{topic}-forecast.md`

## Verification

Recompute the final posterior both ways: the probability form P(H|E) = P(E|H) x P(H) / P(E), and the odds form (prior odds x the product of all LRs, converted back to a probability). They must agree to the rounding used. Then self-score against `assets/evaluators/rubric_bayesian_reasoning_calibration.json`; 3.5 or higher is the bar.
