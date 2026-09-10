---
name: valuation-playbooks
description: "Damodaran playbooks and concept notes behind the suite."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: corporate-finance
    tags: [Damodaran, Valuation, Corporate Finance, Playbooks, Reference Notes]
    related_skills: [dcf-valuation-engine]
---
# Valuation playbooks

The reference shelf for the corporate-finance skills. It holds the three Damodaran frameworks
that sequence a full analysis (intrinsic valuation, corporate finance, special-situations
routing), the concept notes those frameworks and the other skills cite, and the design record
of the suite itself. Nothing here computes anything; every method skill points here when it
summarizes an argument rather than restating it.

## When to Use

- When a corporate-finance skill points here for the framework or concept behind a step it summarizes.
- When you need the full stage sequence, gates and decision thresholds of the intrinsic valuation, corporate finance or special-situations pipeline.
- When a routing, cost-of-capital, capital-structure, real-option or reporting question needs Damodaran's reasoning rather than a formula.
- When you need the suite design spec: analysis modes, artifact names, JSON keys, gate names and the constraint catalogue.

## Contents

Each concept note opens with a core idea, the formulas, a procedure and reference data, in
that order; the frameworks are stage-by-stage orchestration documents.

### Frameworks

| File | What it holds |
|---|---|
| `corporate-finance-playbook.md` | Stages S0–S12 of the end-to-end corporate finance assessment: governance and objective, marginal investor, accounting cleanup, hurdle rates, returns on existing and new investments, optimal debt ratio, moving to it, debt design, dividend policy, the tie to valuation, synthesis; plus firm-type branches. About 100 KB. |
| `intrinsic-valuation-playbook.md` | Stages S0–S18 of a DCF from narrative and landscape survey to value per share, the gap and the feedback loop; branches B1–B10 (negative earnings, banks, emerging markets, private firms, distress, cyclicals, multi-business, real options, control); cross-cutting invariants, the circularity register and the double-count register. About 120 KB. |
| `special-situations-routing.md` | The decision tree that turns company signals into a route: pipeline S0–S11, branches B1–B16 with what breaks and what replaces it, the compiled constraint catalogue, and the determinism boundary. About 100 KB. |
| `suite-design-spec.md` | Design record of the original suite: design rules, analysis modes, workspace layout, state machine and gates, abridged artifact schemas, agent and skill rosters, reference data, hard-stop constraints. The stage, gate, artifact and JSON-key names used across the skills come from here. |

### Capital structure

| File | What it holds |
|---|---|
| `debt-vs-equity-choices.md` | What counts as debt or equity, lease capitalization into debt, and how to measure the mix at market values. |
| `debt-equity-tradeoff.md` | The five forces: tax benefit and management discipline against expected bankruptcy, agency and lost-flexibility costs. |
| `determinants-of-optimal-debt-ratio.md` | Why the optimum depends on the marginal tax rate, EBITDA/EV, operating risk and the ERP-to-default-spread ratio. |
| `enhanced-cost-of-capital-approach.md` | The schedule with indirect bankruptcy costs: operating income falls as the rating falls. |
| `downside-risk-and-rating-constraints.md` | EBIT haircuts, the safety buffer, and the cost of a rating floor. |
| `moving-to-the-optimal.md` | The decision tree for speed and instruments once actual and optimal debt ratios differ. |
| `recapitalization-and-buyback-price.md` | Valuing the move: firm-value gain, per-share effect and the rational buyback price. |

### Real options

| File | What it holds |
|---|---|
| `real-options-framework.md` | The three tests an opportunity must pass before an option premium is admitted on top of a DCF. |
| `opportunities-are-not-options.md` | Scaling option value by exclusivity, and the conditions under which the premium is zero. |
| `decision-trees-vs-option-pricing.md` | Rolling back a staged investment when option pricing cannot be applied, and the two reconciliations. |
| `equity-option-inputs-troubled-firms.md` | Estimating firm-value variance, option life and the strike for a distressed firm (Eurotunnel). |

### Cost of equity and debt

| File | What it holds |
|---|---|
| `riskfree-rate-fundamentals.md` | Definition, instrument choice and the ten-year default-free convention. |
| `currency-riskfree-rate.md` | Stripping the sovereign spread, the build-up route and the differential-inflation route. |
| `cost-of-equity-assembly.md` | Riskfree rate, equity risk premium and beta assembled under the consistency rules, with currency conversion. |
| `operation-weighted-erp.md` | Weighting country risk by where the firm operates, and the four ways to attach it. |
| `synthetic-rating.md` | A rating from interest coverage, by firm class, to a default spread and a cost of debt. |
| `default-spreads-over-time.md` | Spreads as a function of rating and date, and why the vintage is an input. |
| `hurdle-rate-choice.md` | Cost of equity or cost of capital, matched to whose returns are being measured. |
| `net-debt-vs-gross-debt.md` | The two debt conventions, their effect on beta and weights, and the error of mixing them. |

### Narrative and numbers

| File | What it holds |
|---|---|
| `value-vs-price-gap.md` | Value and price as different processes; the gap, the expected return and the closing mechanism. |
| `valuation-misconceptions.md` | Three myths: objectivity, precision, and more inputs meaning a better model. |
| `narrative-scenario-grids.md` | Different stories, different numbers: building and reading a scenario grid and its breakeven cell. |
| `monte-carlo-valuation-simulation.md` | Replacing the uncertain inputs with distributions, and reading percentiles instead of a point. |

### Accounting

| File | What it holds |
|---|---|
| `accounting-standards-gaap-ifrs.md` | GAAP against IFRS, expense classification by nature or function, and where to anchor comparisons. |
| `sector-differences-in-financial-statements.md` | How commodity, bank and R&D-heavy statements break the standard template, and what to read instead. |

### Deliverables

| File | What it holds |
|---|---|
| `dcf-sensitivity-analysis.md` | The two-input sensitivity grid and the plausibility filter on its cells. |
| `valuation-triangulation-and-recommendation.md` | Turning DCF, peer and regression estimates into one buy, sell or hold call. |
| `project-executive-summary-scorecard.md` | The one-page scorecard that opens a corporate finance deliverable, row by row. |

### Difficult companies

| File | What it holds |
|---|---|
| `difficult-company-taxonomy.md` | The four questions every valuation answers, and where each company type breaks them. |

## How to Load

Load one file at a time, by name:

```
skill_view("valuation-playbooks", file_path="references/riskfree-rate-fundamentals.md")
```

The three frameworks run to about 100 KB each. Load the one you need and work from its stage or
branch numbers (S4.5, B6) rather than reading the whole file into context; the skills cite those
numbers when they point here.
