# `cleaned-financials.json` — the artifact contract

The financial-statement-analyst stage writes exactly this shape. Every downstream stage
(cost of capital, intrinsic and special-situations valuation, relative valuation, capital
structure, payout, the critic and the reconciler) reads it, so keys are never renamed and
placeholder numbers are never emitted as if computed. Omit `leases` or `research` blocks
that did not run, or set `applied` to `false` with a reason.

```json
{
  "company": {"name": "", "ticker": "", "currency": "", "valuation_date": "YYYY-MM-DD"},
  "basis": {"period": "TTM", "years_since_last_10k": 0.0, "ttm_source": {}},
  "reported": {"revenue": 0, "ebit": 0, "net_income": 0, "interest_expense": 0,
               "depreciation_amortization": 0, "capital_expenditures": 0, "cash": 0,
               "book_value_of_equity": 0, "book_value_of_debt": 0},
  "adjusted": {"revenue": 0, "ebit": 0, "ebit_after_tax": 0, "net_income": 0,
               "interest_expense": 0, "depreciation_amortization": 0,
               "capital_expenditures": 0, "book_value_of_debt": 0, "lease_debt": 0,
               "research_asset": 0},
  "adjustments": [{"id": "A1", "item": "", "reason": "", "ebit_effect": 0,
                   "capital_effect": 0, "debt_effect": 0, "source": "", "judgment": ""}],
  "leases": {"applied": true, "commitments": [], "lump_sum_beyond": 0,
             "inferred_tail_years": 0, "lease_life": 0, "lease_debt": 0,
             "depreciation_on_lease_asset": 0, "imputed_lease_interest": 0,
             "pre_tax_cost_of_debt_used": 0.0},
  "research": {"applied": true, "amortizable_life": 0, "life_basis": "",
               "research_asset": 0, "amortization_this_year": 0,
               "adjustment_to_operating_income": 0, "padded_years": 0},
  "one_time_items": [{"description": "", "ebit_effect": 0, "frequency": 0.0,
                      "variability": 0.0, "verdict": "non-recurring|recurring|annualized",
                      "annualized_amount": 0}],
  "normalization": {"applied": false, "reason": "", "method": "", "window_years": 0,
                    "window_start": "", "window_end": "", "normalized_ebit": 0,
                    "caveat": ""},
  "tax": {"effective_rate": 0.0, "marginal_rate": 0.0, "basis": "",
          "path": [{"year": 1, "rate": 0.0}], "nol_balance": 0, "nol_source": ""},
  "capital": {"invested_capital": 0, "measured_at": "start_of_period", "roic": 0.0,
              "cost_of_capital_used": 0.0, "return_spread": 0.0,
              "economic_value_added": 0},
  "reinvestment": {"net_capital_expenditures": 0, "acquisitions_normalized": 0,
                   "change_in_noncash_working_capital": 0, "reinvestment": 0,
                   "reinvestment_rate": 0.0},
  "cash_flows": {"fcff": 0, "fcfe": 0, "fcfe_route": ""},
  "ratios": {},
  "circularity": {"resolved": true, "iterations": 0, "final_pre_tax_cost_of_debt": 0.0,
                  "final_interest_coverage": 0.0, "synthetic_rating": "", "spread": 0.0,
                  "table": "", "oscillation_note": ""},
  "checks": {"net_income_unchanged_after_leases": true,
             "fcff_unchanged_after_rd": true,
             "roic_moved_down": true,
             "reconciliation_ties": [{"tie": "", "status": "pass|fail", "detail": ""}]},
  "reference_data": [{"source": "", "as_of": ""}],
  "constraints_honored": [],
  "constraints_refused": [{"rule": "", "reason": "", "alternative": ""}],
  "unresolved": []
}
```

## Field notes

- `adjusted.ebit` is the single EBIT every later stage uses; `capital.invested_capital` is
  the single capital base. No stage recomputes either.
- Every row in `adjustments` carries both legs: `ebit_effect` and `capital_effect` (and
  `debt_effect` where the correction adds debt). A row with one leg is the error this stage
  exists to prevent.
- `one_time_items[].ebit_effect` is signed from the point of view of operating income: a
  charge added back is positive, a non-recurring gain removed is negative.
- `tax.path` is the standard path — effective for years 1 to 5, a linear ramp to marginal
  over years 6 to 10, marginal thereafter — unless the artifact says why it differs. The
  cost-of-capital stage reuses `tax.marginal_rate` in the after-tax cost of debt.
- `capital.measured_at` is `start_of_period` so the numerator's income was earned on it.
- `circularity.table` names the synthetic-rating table used (`large_manufacturing`,
  `small_or_risky` or `financial_service`), and `oscillation_note` says whether the loop
  settled or was capped at six passes.
- For a financial service firm (`no-fcff-valuation`), `cash_flows.fcff` and the
  debt-inclusive `capital.roic` are `null` with the reason in `constraints_refused`; the
  artifact carries book equity, ROE, the earnings base and the regulatory capital lines
  instead.
