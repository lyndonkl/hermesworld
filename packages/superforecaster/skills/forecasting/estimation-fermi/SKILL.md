---
name: estimation-fermi
description: Decompose an unknown into parts and bound the estimate.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: forecasting
    tags: [Estimation, Fermi, Order of Magnitude, Market Sizing, Decomposition]
    related_skills: [reference-class-forecasting, bayesian-reasoning-calibration]
---
# Fermi Estimation

Decomposes a complex unknown into components that can each be estimated, then combines them into a rapid order-of-magnitude answer with explicit upper and lower bounds. It produces a defensible ballpark and a record of every assumption behind it. It does not produce precision: when a decision needs better than a factor of two, collect real data instead.

## When to Use

- Making a quick estimate: market sizing, resource planning, a feasibility check.
- Bounding an unknown with upper and lower limits before deciding.
- Sanity-checking a strategic assumption or someone else's number.
- Building a structural estimate to compare against a base rate in a forecast.
- The user mentions Fermi estimation, back-of-envelope calculation, order of magnitude, ballpark estimate, or triangulation.

## Example

**Question**: How many piano tuners are in Chicago?

**Decomposition**:
1. Chicago ~3M people / 3 per household = 1M households
2. ~1 in 20 has a piano = 50,000 pianos, tuned once a year
3. Tuner: 250 days/year x 4 tunings/day = 1,000/year
4. 50,000 / 1,000 = **~50 piano tuners** (actual: ~80-100, within an order of magnitude)

## Procedure

Copy this checklist and track progress:

```
Fermi Estimation Progress:
- [ ] Step 1: Clarify the question and define the metric
- [ ] Step 2: Decompose into estimable components
- [ ] Step 3: Estimate components using anchors
- [ ] Step 4: Bound with upper/lower limits
- [ ] Step 5: Calculate and sanity-check
- [ ] Step 6: Triangulate with an alternate path
```

**Step 1: Clarify the question and define the metric**

Restate the question precisely (units, scope, timeframe). Identify what decision hinges on the estimate (is a directional answer enough? an order of magnitude?). See [templates/template.md](templates/template.md#clarification-template) for the clarification framework.

**Step 2: Decompose into estimable components**

Break the unknown into a product or quotient of knowable parts. Choose a decomposition strategy (top-down, bottom-up, dimensional analysis). See [templates/template.md](templates/template.md#decomposition-strategies) for decomposition patterns.

**Step 3: Estimate components using anchors**

Ground each estimate in a known quantity (population, physical constants, market sizes, direct experience). Prefer a searched figure to a remembered one: one or two `web_search` queries per component, source recorded. State assumptions explicitly. See [references/methodology.md](references/methodology.md#anchoring-techniques) for anchor sources and calibration.

**Step 4: Bound with upper and lower limits**

Calculate optimistic (upper) and pessimistic (lower) bounds to bracket the answer. Check whether the decision changes across the range. See [references/methodology.md](references/methodology.md#bounding-techniques) for constraint-based bounding.

**Step 5: Calculate and sanity-check**

Compute the estimate and round to 1-2 significant figures. Sanity-check against reality: does the answer pass the smell test? See [templates/template.md](templates/template.md#sanity-check-template) for validation criteria.

**Step 6: Triangulate with an alternate path**

Re-estimate using a different decomposition. Check whether both paths land in the same order of magnitude. Score the work against [assets/evaluators/rubric_estimation_fermi.json](assets/evaluators/rubric_estimation_fermi.json). **Minimum standard**: average score >= 3.5.

## Common Patterns

**Pattern 1: Market sizing (TAM/SAM/SOM)**
- **Decomposition**: Total population -> Target segment -> Addressable -> Reachable -> Price point
- **Anchors**: Census data, industry reports, analogous markets, penetration rates
- **Bounds**: Optimistic (high penetration, premium pricing) vs pessimistic (low penetration, discount pricing)
- **Sanity check**: Compare to public company revenues in the space and to VC market-size estimates
- **Example**: E-commerce TAM = US population x online shopping % x average spend/year

**Pattern 2: Infrastructure capacity**
- **Decomposition**: Users -> Requests per user -> Compute/storage per request -> Overhead
- **Anchors**: Similar services, known capacity (instance limits), load-testing data
- **Bounds**: Peak (Black Friday) vs average load; growth trajectory (2x/year vs 10x/year)
- **Sanity check**: Cost per user should be < LTV; compare to public cloud bills at similar scale
- **Example**: Servers needed = (DAU x requests/user x ms/request) / (instance capacity x utilization)

**Pattern 3: Staffing and headcount**
- **Decomposition**: Work to be done (features, tickets, customers) -> Productivity per person -> Overhead (meetings, support)
- **Anchors**: Industry benchmarks (engineers per X users, support agents per Y customers), team velocity, hiring timelines
- **Bounds**: Experienced team (high productivity) vs new team (ramp time); aggressive timeline vs sustainable pace
- **Sanity check**: Headcount growth should track the revenue growth curve; compare to peers at similar scale
- **Example**: Engineers needed = (story points in roadmap / velocity per engineer) + 20% overhead

**Pattern 4: Financial projections**
- **Decomposition**: Revenue = Users x Conversion rate x ARPU; Costs = COGS + Sales/Marketing + R&D + G&A
- **Anchors**: Cohort data, industry CAC/LTV benchmarks, comparable company metrics, historical growth
- **Bounds**: Bull case (high growth, efficient scaling) vs bear case (slow growth, rising costs)
- **Sanity check**: Margins should approach industry norms at scale; growth should follow an S-curve, not an exponential forever
- **Example**: Year 2 revenue = Year 1 revenue x (1 + growth rate) x (1 - churn)

**Pattern 5: Impact assessment**
- **Decomposition**: Total impact = Units affected x Impact per unit x Duration
- **Anchors**: Emission factors (kg CO2/kWh), conversion rates (program -> behaviour change), precedent studies
- **Bounds**: Conservative (low adoption, small effect) vs optimistic (high adoption, large effect)
- **Sanity check**: Impact should scale linearly or sub-linearly (diminishing returns); compare to similar interventions
- **Example**: Carbon saved = (Users switching x Miles driven/year x Emissions/mile) - Baseline

## Guardrails

1. **State assumptions explicitly.** Every Fermi estimate rests on assumptions. Make them visible ("assuming 250 workdays/year", "if conversion is ~3%"). Unstated assumptions create false precision.
2. **Aim for order of magnitude, not precision.** The goal is 10^X, not X.XX. Round to 1-2 significant figures (50 not 47.3, 3M not 2,847,291). If the decision needs precision, get real data instead.
3. **Decompose until components are estimable.** Break down until you reach quantities you can estimate from knowledge and experience. If a component is still "how would I know that?", decompose further.
4. **Use multiple paths (triangulation).** Estimate the same quantity via different decompositions (top-down vs bottom-up, supply-side vs demand-side). If paths agree within a factor of 3, confidence increases. If they differ by 10x or more, investigate which decomposition is flawed.
5. **Bound the answer.** Calculate optimistic and pessimistic cases to bracket reality. If the decision holds across the range, the bounds matter less. If the decision flips, invest in a better estimate.
6. **Sanity-check against reality.** Compare to known quantities, use dimensional analysis (units should cancel), and check extreme cases (what if everyone did X? does it break physics?).
7. **Calibrate on known problems.** Practise on questions with verifiable answers to find personal biases (overestimating? underestimating? anchoring?).
8. **Acknowledge uncertainty ranges.** Express estimates as ranges when appropriate ("10-100k users", "likely $1-5M").

## Pitfalls

- **Anchoring on the wrong number**: an irrelevant or biased starting point. If someone asks "Is it 1 million?" you anchor there for no reason.
- **Double-counting**: including the same quantity twice in the decomposition (counting both businesses and employees when businesses already include employees).
- **Unit errors**: mixing per-day and per-year, confusing millions and billions, wrong currency conversion. Always check units.
- **Survivor bias**: estimating from successful cases (average startup revenue from unicorns, ignoring failures).
- **Linear extrapolation**: assuming linear growth when it is exponential, or vice versa. Growth rates change over time.
- **Ignoring constraints**: physical limits and economic limits (a market cannot grow faster than GDP forever).

## Quick Reference

**Key resources:**

- **[templates/template.md](templates/template.md)**: clarification framework, decomposition strategies, estimation template, sanity-check criteria
- **[references/methodology.md](references/methodology.md)**: anchoring techniques, bounding methods, triangulation approaches, calibration exercises
- **[assets/evaluators/rubric_estimation_fermi.json](assets/evaluators/rubric_estimation_fermi.json)**: quality criteria for decomposition, assumptions, bounds, sanity checks

**Common anchors:**

- Demographics: US population ~330M, households ~130M, labour force ~165M; world population ~8B, urban ~55%, internet users ~5B
- Business: Fortune 500 revenue $100k to $600B (median ~$30B); startup valuations seed ~$5-10M, Series A ~$30-50M, unicorn >$1B; SaaS CAC ~$1-5k, LTV/CAC >3, churn <5%/year
- Technology: a cloud VM ~10k requests/sec, object storage ~$0.023/GB/month; mobile app ~5-10 screens/day per user, 50-100 API calls/session; website ~2-3 pages/session, 1-2 min sessions
- Physical: person ~70kg, 2000 kcal/day, 8 hours sleep; car ~25 mpg, 12k miles/year, $30k new, 200k-mile lifetime; house ~2000 sq ft, $300k median US, 30-year mortgage
- Conversion factors: 1 year ~ 250 workdays ~ 2000 work hours; 1 million seconds ~ 11.5 days, 1 billion seconds ~ 32 years; 1 mile ~ 1.6 km, 1 kg ~ 2.2 lb, 1 gallon ~ 3.8 litres

**Decomposition strategies:**

- **Top-down**: start with the total population and filter down (US population -> car owners -> EV buyers)
- **Bottom-up**: start with a unit and scale up (one store's revenue x number of stores)
- **Rate x Time**: flow rate x duration (customers/day x days/year)
- **Density x Area/Volume**: concentration x space (people/sq mile x city area)
- **Analogous scaling**: a known similar system, adjusted for size (competitor revenue x our market share)

**Typical estimation time:** simple question (1-2 levels) 3-5 minutes; market sizing (3-4 levels) 10-15 minutes; complex business case (several metrics, triangulation) 20-30 minutes.

**When to escalate:** the decision needs better than a factor-of-2 uncertainty; the estimate spans more than two orders of magnitude even with bounds; no reasonable decomposition path exists; stakeholders need confidence intervals and statistical rigour. Then invest in data collection, detailed modelling, or expert consultation.

**Inputs required:** the question (units, scope), the decision context (required precision), known anchors.

**Outputs produced:** `estimation-fermi.md` with question, decomposition, assumptions, calculation, bounds, sanity check, triangulation, and the final estimate with its range.

## Verification

Two checks close the step: the two triangulation paths agree within a factor of 3 (if they differ by 10x or more, one decomposition is wrong; find which before handing anything forward), and the self-score against `assets/evaluators/rubric_estimation_fermi.json` averages 3.5 or higher.
