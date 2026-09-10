# product-strategist

A Hermes Agent profile that reverse-engineers a real product's strategy from the outside, using
only public material. Give it a product or company name and an output path, and it works
top-down through vision, competitive strategy, tactical moves, and the product surfaces users
touch, grading every strategic claim by how much evidence stands behind it. It thinks in prose
scratchpads first, consolidates them into one markdown report, then rewrites that report until a
reader with no background in the company or the industry can follow every sentence, and renders
a PDF. It does not analyse engineering or architecture; that would be speculation dressed as
analysis.

## What you get

One markdown report at the path you name, a `scratch/` folder of analyst working notes beside
it, and a PDF next to the markdown when the toolchain is present. The report has eight sections:

0. **Executive Brief**: what the company sells and to whom, its life-cycle stage and the one
   question that stage raises, the top bets with their grades, the verdict.
1. **Vision**: what the company says, what its actions show, the stage, the business model as a
   loop.
2. **Strategy**: where it competes, how it wins, each bet graded probable / plausible / possible
   with a promotion trigger and a failure signal, whether its market-size claim is coherent, the
   moat, the risks.
3. **Tactics**: the last 18-24 months of launches, deals, pricing and hiring, each move tagged as
   a break, a shift or a change; acquisitions scored against the empirical base rate.
4. **Operational Surface**: the main features a user touches and which bet each one executes.
5. **Strategic Synthesis**: where the strategy holds together, the strongest case against, what
   the company actually optimises for, defendable takes, open questions, the verdict.
6. **Plain-Language Glossary**: every load-bearing term, explained.
7. **Sources**: numbered footnotes grouped by source type.

## Install

From the root of this repository:

```bash
tools/install.sh product-strategist
```

or directly with Hermes:

```bash
hermes profile install ./packages/product-strategist --alias
```

Then start a session:

```bash
hermes -p product-strategist chat
```

The package pins no model or provider. `tools/install.sh` seeds the profile's model block from
your root profile; change it any time with `hermes -p product-strategist model`. The model needs
web tools (`web_search`, `web_extract`) enabled, because every finding comes from public
material.

## Optional tooling

Two steps use tools you install yourself. Neither is required for the markdown report.

- **PDF rendering (Step 10)** needs pandoc and a LaTeX engine with xelatex. macOS:
  `brew install pandoc basictex`, then `sudo tlmgr update --self && sudo tlmgr install xetex`.
  Debian/Ubuntu: `sudo apt install pandoc texlive-xetex texlive-fonts-recommended`. Open a new
  shell afterwards. Without them the agent reports the install commands and delivers the
  markdown.
- **Readability scoring (Step 9)** uses a bundled Python script that depends on `textstat`:
  `python3 -m pip install --user textstat`. Without it the agent notes the score was skipped and
  continues.

## First prompts to try

```
Analyse Figma. Write the report to reports/figma.md.
```

```
Analyse Notion, focused on its AI features and how they compete with Microsoft Loop.
Output: ~/strategy/notion.md
```

```
Analyse Peloton. Depth: short. Emphasise whether management is facing the decline stage
honestly. Write to peloton/report.md.
```

The product name and output path are required; the focusing sentence is optional. If either
required input is missing the agent asks once and then stops.

## Skills it carries

| Skill | Category | Role in the workflow |
|---|---|---|
| `business-narrative-builder` | strategy | Step 3: place the company on the six-stage corporate life cycle |
| `strategy-and-competitive-analysis` | strategy | Step 4: pick two or three frameworks that fit, name the rejected ones |
| `systems-thinking-leverage` | strategy | Step 4: sketch any reinforcing loop the strategy rests on and when it reverses |
| `term-interrogation` | strategy | Standing lens; Step 9: unpack every concept-bearing term until it reads plainly |
| `strategy-concept-notes` | strategy | Fourteen Damodaran concept notes loaded at Steps 1, 3, 4, 5, 7; the report skeleton |
| `layered-reasoning` | thinking | Steps 3-7: keep vision, strategy, tactics and surfaces consistent |
| `communication-storytelling` | writing | Step 7: keep the verdict landing |
| `reader-first-prose` | writing | Standing lens; Step 9: write for a first-time reader, no em dashes |
| `slop-detector` | writing | Step 8: scan the consolidated draft for generated-prose signatures |
| `readability-check` | writing | Step 9: score the report on the `general` profile with the bundled script |
| `markdown-to-pdf` | writing | Step 10: render the PDF with pandoc and xelatex |

`business-narrative-builder`, `readability-check` and `slop-detector` are shared with other
packages in this repository and are synced from `shared/skills/`.

## What changed from the Claude version

- The agent body became `SOUL.md`, injected into every session of the profile. The workflow, the
  two-reader stance, the bet grading, the acquisition scorecard and the report structure are the
  same.
- The concept notes the Claude agent cited from its knowledge folder are bundled as `references/`
  inside a new skill, `strategy-concept-notes`, and each citation in `SOUL.md` is now a `skill_view`
  call at the same step. The report skeleton moved from the agent body into that skill's
  `templates/`.
- Claude tool names became Hermes tools: `web_search` and `web_extract` for research,
  `write_file` and `read_file` for scratchpads and the report, `terminal` for the readability
  script and the PDF render, `skill_view` to load skills at the step that needs them.
- The Claude agent, being a subagent, could not ask questions and wrote a failure note when an
  input was missing. This profile asks once with `clarify` before doing the same.
- Each skill's long Claude description became a 60-character description plus a `When to Use`
  section carrying the original trigger phrases. Skill `resources/` folders became `scripts/`,
  `references/`, `templates/` and `assets/`.
- No model tier is pinned. The Claude agent ran on `opus`; here the installer's own model applies.
- Em dashes used as separators in the report skeleton became colons and parentheses, in line with
  the agent's own style rule.

## Models

Two models, both on OpenRouter and both changeable in `config.yaml`: `meta/muse-spark-1.3`
does the research, curation and analysis; a delegated child on `google/gemini-3.7-flash`
(`delegation.model`) writes the report and runs the comprehension pass, because that model
leads the non-Anthropic rows of the human creative-writing leaderboard. Rationale and
alternatives: `docs/MODELS.md`.
