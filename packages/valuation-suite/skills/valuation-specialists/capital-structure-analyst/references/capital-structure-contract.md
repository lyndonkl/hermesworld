# `capital-structure.json` — the artifact contract

The capital-structure stage writes exactly this shape. The reconciler reads
`recommendation`, `value_effect` and `debt_design`; the critic reads the whole file; the
intrinsic stage's second run in `corporate-finance` and `restructuring` reads
`recommendation.point` and the schedule row it sits on.

```json
{
  "agent": "capital-structure-analyst",
  "status": "complete|blocked|not_applicable|needs_input|needs_script",
  "currency": "USD",
  "valuation_date": "YYYY-MM-DD",
  "reference_data": [{"source": "synthetic_ratings.json", "table": "large_manufacturing", "as_of": "2021-01"}],
  "constraints_honored": [{"rule": "require-normalized-earnings", "effect": "schedule run on LTM and normalized EBIT"}],
  "current_mix": {"market_debt_ratio": 0.0, "book_debt_ratio": 0.0, "net_debt_ratio": 0.0,
                  "instruments": [], "maturity_profile": {}, "currency_mix": [], "fixed_floating_split": {}},
  "qualitative": {"forces": [{"force": "tax benefit", "score": "", "proxy": 0.0}],
                  "predicted_direction": "under_levered|at_the_mix|over_levered"},
  "schedule": [{"debt_ratio": 0.0, "debt_equity_ratio": 0.0, "dollar_debt": 0.0,
                "interest_expense": 0.0, "interest_coverage_ratio": 0.0, "rating": "",
                "default_spread": 0.0, "pre_tax_cost_of_debt": 0.0, "tax_rate_applied": 0.0,
                "levered_beta": 0.0, "cost_of_equity": 0.0, "after_tax_cost_of_debt": 0.0,
                "cost_of_capital": 0.0}],
  "schedule_normalized": [],
  "optimum_standard": {"debt_ratio": 0.0, "cost_of_capital": 0.0, "rating": ""},
  "curve_shape": {"flat_band": [0.0], "spread_within_band_bp": 0.0,
                  "cliff_step": 0.0, "reading": ""},
  "excess_debt_capacity": 0.0,
  "value_effect": {"full_revaluation": 0.0, "incremental": 0.0, "implied_growth": 0.0,
                   "gain_per_share": 0.0, "rational_buyback_price": null},
  "protection": {"route": "stress|rating_constraint",
                 "ebit_volatility": {"sd_pct_change": 0.0, "worst_year_pct": 0.0},
                 "stress_table": [{"haircut": 0.1, "ebit": 0.0, "optimal_debt_ratio": 0.0}],
                 "safety_buffer": 0.0,
                 "rating_constraint": {"minimum_rating": "", "constrained_ratio": 0.0,
                                       "cost": 0.0, "motive": ""}},
  "alternate_lens": {"method": "enhanced|peer_regression|apv|none", "result": {}, "not_computed": []},
  "drivers": {"marginal_tax_rate": 0.0, "ebitda_to_ev": 0.0, "ebit_to_ev": 0.0,
              "operating_risk": "", "erp_to_baa_spread": 0.0},
  "recommendation": {"direction": "under_levered|at_the_mix|over_levered",
                     "range": [0.0, 0.0], "point": 0.0, "mechanical_argmin": 0.0,
                     "urgency": "immediate|gradual", "method": "", "instruments": [],
                     "rationale": ""},
  "debt_design": {"route": "intuitive|project_duration|macro_regression|bottom_up",
                  "target_duration": 0.0,
                  "currency_mix": [{"currency": "", "share": 0.0}],
                  "fixed_floating_split": {"fixed": 0.0, "floating": 0.0},
                  "special_features": [], "convertible_yes_no": false,
                  "regression_table": [{"dependent": "", "regressor": "", "slope": 0.0,
                                        "t_stat": 0.0, "level": "firm|bottom_up"}],
                  "existing_profile": {}, "gap_table": [], "closure_instruments": [],
                  "one_sentence_recommendation": ""},
  "feedback_rerun": {"performed": false, "revised_optimum": null},
  "needs_script": [],
  "open_questions": []
}
```

## Field notes

- `schedule` is the `debt-schedule` output row by row, unedited. `schedule_normalized`
  is filled only when `require-normalized-earnings` made you run it twice.
- `value_effect.full_revaluation` and `value_effect.incremental` are both reported; the
  gap between them is the growth assumption, and the markdown says so.
- `protection.route` is one of the two, never both. Fill only the block for the route
  used; leave the other's fields null.
- Every entry in `debt_design.regression_table` carries `t_stat`. A slope without one is
  not usable evidence, and a slope with absolute t below 2 is recorded but marked as not
  driving the decision.
- On `not_applicable` (`no-optimal-debt-ratio`), `status` says so, `open_questions`
  carries the constraint, the reason and the alternative approach with its owning stage,
  and every numeric block is `null`, not zero.
- `needs_script` lists each calculation that had no script — the buyback fixed point, the
  distress-adjusted firm value under the enhanced approach — with one line on what it would
  have contributed.
