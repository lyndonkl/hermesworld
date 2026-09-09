---
name: strategy-concept-notes
description: Damodaran narrative-and-numbers notes for strategy analysis.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: strategy
    tags: [Damodaran, Narrative And Numbers, Corporate Life Cycle, Acquisitions, Growth Quality, Governance]
    related_skills: [business-narrative-builder, strategy-and-competitive-analysis, systems-thinking-leverage]
---
# Strategy concept notes

Fourteen concept notes distilled from Aswath Damodaran's teaching on narrative and numbers,
acquisitions, growth and corporate governance, bundled as references for an outside-in strategy
read of a real company. Each note has the same shape: core idea, formulas, a numbered procedure,
reference data, and usually a worked example. They supply priors and screens, not conclusions.
This skill has no scripts and computes nothing; it is a library the strategist loads one note at
a time, at the step that needs it. It also carries the strategist report skeleton as a template.

## When to Use

- Declaring your own bias and screening for a runaway story before researching a company.
- Placing a company on the corporate life cycle and naming the one question its stage raises.
- Grading strategic bets as possible, plausible, or probable, and writing the trigger that would
  promote each.
- Testing a market-size claim against every competitor chasing the same pot.
- Auditing acquisitions, synergy claims, and growth initiatives against the empirical base rates.
- Asking what a company actually optimises for and whether maximising that number builds or
  erodes the business.

## Contents

| Note | What it gives you | Strategist step |
|---|---|---|
| `valuation-misconceptions` | Three myths (valuation is objective, precise, better when more quantitative) and the bias-declaration procedure: who pays, what you already believe, what public position you hold. Includes the revision-symmetry test for bias. | 1 |
| `runaway-stories` | The three-ingredient screen for a story that stops getting questioned (charismatic narrator, disliked status quo, societal benefit) and the three-ingredient meltdown pattern. Theranos board as the reference case. | 1 |
| `life-cycle-uncertainty` | Six life-cycle stages, the single dominant question at each, and whether the uncertainty is company-specific or macro. Survival-rate data by sector. | 3 |
| `landscape-survey` | How to map a business model as a loop (who supplies, who buys, how money moves, who sets price, what must be invested) and benchmark against the industry. Second half is base-year financial clean-up, less relevant here. | 3 |
| `possible-plausible-probable` | Sort each claim by whether you can assign it odds; "possible" means unassessable, not unlikely. Promotion triggers between grades. Uber and Zomato worked examples. | 4 |
| `big-market-delusion` | Sum the market shares every competitor's story implies and check the total can be true; include foreign players. 2015 online-advertising table as the worked case. | 4 |
| `narrative-consistency-checks` | Impossible, implausible and improbable screens on the growth, risk and reinvestment triangle; profits without competition, growth without reinvestment; "who loses that revenue". | 4 |
| `narrative-updating-feedback-loop` | Classify news as a break, a shift or a change, each with its own response. Build and value the counter-narrative; reduce disagreement to named variables. Uber 2014 example. | 5, 7 |
| `growth-quality-and-excess-returns` | Value created per incremental dollar by growth mode, from new-product development (positive) to share fights and acquisitions (negative). ROIC-versus-cost-of-capital buckets by region. | 5 |
| `acquisition-empirical-record` | Announcement returns to targets (+17% to +19%) versus acquirers (about zero); McKinsey and KPMG failure rates; divestiture rates as the admission a deal failed. | 5 |
| `synergy-delivery-odds` | Cost synergies mostly arrive; 70% of mergers miss their revenue synergies. Concreteness, named ownership and bidder count as the tests that predict delivery. | 5 |
| `seven-sins-of-acquisitions` | Seven testable deal defects as a pass/fail scorecard with a column for the rationalization offered; HP and Autonomy audited as the worked example. | 5 |
| `synergy-taxonomy` | Maps each claimed synergy to the one valuation input it must move; anything that fits no row is a buzzword. AB InBev and SABMiller as the worked example. | 5 |
| `alternative-objective-functions` | The test for any intermediate metric (does maximising it alone raise long-run value?), the classic decouplings, and why a stakeholder scorecard with no tiebreaker means no accountability. | 7 |

The notes cross-reference each other with `[[double-bracket]]` links. Some of those targets are
valuation notes that are not bundled in this package (Monte Carlo simulation, scenario grids,
contingent-claim valuation); treat such links as pointers to a wider curriculum, not as files to
open.

## How to Load

Load one note at the step that needs it, by file path:

```
skill_view("strategy-concept-notes", file_path="references/runaway-stories.md")
skill_view("strategy-concept-notes", file_path="references/possible-plausible-probable.md")
```

The strategist report skeleton lives in this skill too:

```
skill_view("strategy-concept-notes", file_path="templates/strategist-report.md")
```

Copy that skeleton to the report path and fill every placeholder; do not paste it in fragments.

## How to Read a Note

1. Read the **core idea** for the claim the note makes and the failure it guards against.
2. Run the **procedure** as written; the numbered steps are the operating content.
3. Use the **reference data** as a prior, quoting the figure and its vintage when you lean on it.
4. Use the **worked example** to check your own application looks like the source's.

## Pitfalls

- The numbers are priors from dated source material (mostly 2014 to 2021 decks). Cite them as
  base rates, with their vintage, never as facts about the company in front of you.
- The notes were written for valuation. Where a step asks for a DCF input, translate it to the
  strategy question (which bet, which competitor, which metric) rather than building a model.
- `landscape-survey` and `narrative-consistency-checks` each have a numeric half that belongs to
  valuation work; the strategist uses the first half of one and the strategy screens of the other.
- A screen that passes is not evidence for the story. It only removes one way the story could be
  wrong.

## Verification

- Every base-rate figure quoted in the report names the note it came from and the year of the
  underlying data.
- Every bet in the report carries one of the three grades from `possible-plausible-probable` and
  a written promotion trigger.
- Every significant acquisition in the report has a filled four-row scorecard derived from
  `seven-sins-of-acquisitions`.
