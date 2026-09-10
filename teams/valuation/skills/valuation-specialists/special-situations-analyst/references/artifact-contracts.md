# Artifact contracts for the special-situations stage

The special-situations stage writes the same three files as the intrinsic-valuation stage —
`forecast.json`, `dcf-result.json`, `intrinsic.md` — so that the critic, the reconciler and
the report never branch on company type. This file gives the shapes and the conventions
that let one contract carry every branch.

## `forecast.json`

The intrinsic stage's payload, extended with a `branch` block and a `not_applicable` list.

```json
{
  "currency": "USD",
  "model_variant": {"cash_flow": "fcff|fcfe|ddm|excess_return", "discount_rate": "wacc|cost_of_equity",
                    "stages": 2, "phase_years": [10], "basis": "nominal"},
  "driver_basis": "operating|equity",
  "base_revenue": 0, "base_ebit": 0, "base_invested_capital": 0,
  "net_operating_loss_carryforward": 0, "forecast_years": 10,
  "revenue_growth": {"start": 0.0, "end": 0.0, "converge_by": 10},
  "operating_margin": {"start": 0.0, "end": 0.0, "converge_by": 7},
  "sales_to_capital": 0.0,
  "tax_rate": {"start": 0.0, "end": 0.0, "converge_by": 10},
  "cost_of_capital": {"start": 0.0, "end": 0.0, "converge_by": 10},
  "terminal": {"growth_rate": 0.0, "cost_of_capital": 0.0, "return_on_capital": 0.0},
  "failure": {"probability": 0.0, "probability_source": "bond|rating|statistical|sector-survival|stated",
              "horizon_years": 10, "proceeds_basis": "book_value|going_concern",
              "proceeds_percent": 0.0},
  "bridge": {"debt": 0, "cash": 0, "minority_interests": 0, "non_operating_assets": 0,
             "employee_options_value": 0, "shares_outstanding": 0, "current_price": 0},
  "equity_drivers": {"book_equity": 0, "roe_path": [], "payout_or_retention": 0.0,
                     "capital_ratio_path": [], "cost_of_equity": 0.0},
  "not_applicable": [{"key": "sales_to_capital", "reason": "equity engine; reinvestment is retention"}],
  "branch": {
    "engine_branch": "B5",
    "primary_path": "excess-return",
    "overlays": ["emerging-market"],
    "excluded_methods": [
      {"method": "fcff-wacc", "reason": "debt is raw material for a bank", "constraint": "no-fcff-valuation"}
    ],
    "reference_vintages": [{"table": "distress_reference.json", "as_of": "2024-01-01"}]
  },
  "vintages": {"price_date": "", "cost_of_capital_date": "", "reference_tables": ""}
}
```

Conventions:

- Keep every key the intrinsic contract names. A key with no meaning in the branch is
  `null`, with an entry in `not_applicable` giving the reason. Downstream consumers then read
  one shape whatever ran.
- Equity-engine branches (B5, dividend-discount) set `driver_basis: "equity"` and fill
  `equity_drivers` (ROE, payout or retention, book equity, the capital ratio path).
- `failure.probability` is the cumulative probability over the forecast horizon, never the
  annual one, and `probability_source` names the channel.
- `branch.excluded_methods` is the list the critic uses to check route conformance. Every
  entry names the constraint that closed the method.

## `dcf-result.json`

The engine output (per-year cash flow table, present values, terminal value, operating asset
value, bridge line items, value per share), plus:

- `method`: `fcff`, `fcfe`, `ddm` or `excess_return` — the validator reads it.
- `currency`.
- `sensitivity`: the grid from `dcf.py sensitivity`, and `simulation` percentiles from
  `simulate.py simulate` when run.
- Where the engine produced equity value directly, `value_of_operating_assets` and any
  enterprise-level field are `null` with a `reason`, and `bridge` records what was actually
  walked (book equity to equity value, or firm value to equity through the option lens).
- For a distress blend, `distress` carries `going_concern_value`, `distress_value`,
  `probability`, `probability_source`, `horizon_years`, `equity_loss_fraction` and
  `blended_value`, and `alternative_estimates` carries the equity-as-option value when the
  option lens ran, marked as an alternative and never added.
- For B13, `discounts` carries the illiquidity route used, the three routes returned, the
  discount applied and the stake basis; for B14 it records that no illiquidity discount
  applies and lists the three IPO adjustments.
- For B6, `commodity` carries the price used, its date, the regression R² and the price
  ladder behind any separate price view.

## `intrinsic.md`

Sections, in order:

1. Which branch ran and why, with the engine it beat on precedence.
2. The standard methods excluded, each under its constraint.
3. The two or three judgments the answer turns on.
4. The value with its range, and where the market price sits.
5. The outer adjustments applied, each with its probability and source.
6. A defence for every surviving validator warning.
7. The data vintages.

For a commodity firm, the value at today's price comes first and any macro view sits in its
own paragraph. For a bank, state the sustainable ROE, the target
capital ratio and their peer anchors. For a private company, state which buyer the value
is for and which illiquidity route produced the discount.
