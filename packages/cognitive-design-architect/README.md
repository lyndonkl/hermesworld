# cognitive-design-architect

A Hermes Agent profile that applies cognitive science to design work. It explains why a design works or fails in terms of perception, attention, working memory, and decision-making (Tufte, Norman, Ware, Cleveland and McGill, Mayer, Gestalt), and it refuses to produce misleading graphics. It routes each request to one of six design skills, chains them for larger projects, and finishes every written deliverable with a slop and readability pass.

## What it does

- Grounds design decisions in research instead of taste, and tells you which principle each decision rests on.
- Structures content and navigation so people can find things, with tree-test plans to prove it.
- Writes D3.js code for custom charts, networks, and maps, delivered as self-contained HTML files.
- Turns data into an annotated narrative for articles, reports, and slide decks.
- Audits existing designs against an 8-dimension cognitive checklist and a 4-criteria visualization audit, with severity-ranked fixes.
- Checks charts and dashboards for chartjunk, truncated axes, bias exploitation, and data-integrity violations.

## What you can ask it for

| Area | Examples |
|---|---|
| Interfaces | dashboard layouts, onboarding flows, form design, navigation and labeling, progressive disclosure |
| Data visualizations | chart-type choice for a given task, D3 implementations, interaction design, color and encoding decisions |
| Educational content | e-learning modules, worked examples, segmenting and dual-coding decisions, slide sequences |
| Presentations and stories | narrative arcs, annotation plans, scrollytelling structure, honest framing of a finding |
| Audits | design critiques with evidence, visualization scoring, "is this chart honest?", before-launch QA |

Hand it a screenshot or mockup and it reads the image before commenting; hand it a data file and it reads that before choosing an encoding.

## Install

From the root of this repository:

```bash
tools/install.sh cognitive-design-architect
```

or directly:

```bash
hermes profile install ./packages/cognitive-design-architect --alias
```

Then start a session with `hermes -p cognitive-design-architect chat` (or `cognitive-design-architect chat` if the alias was created). The package pins `meta/muse-spark-1.3` on OpenRouter at high reasoning effort (`docs/MODELS.md`); `hermes -p cognitive-design-architect model` changes it.

Updating later: `git pull` in this checkout, then `hermes profile update cognitive-design-architect`. `SOUL.md` and the skills are replaced on update; your `config.yaml` is kept.

## First prompts to try

- "I have a dashboard with 14 KPI tiles. Here is a screenshot. What is wrong with it and in what order should I fix it?"
- "Build a D3 line chart of monthly revenue for three regions. The task is spotting which region diverged in Q3."
- "Our docs navigation has 22 top-level items. Help me restructure it and write the tree test."
- "Is this chart honest? The y-axis starts at 40 and the caption says sales doubled."
- "Design a 20-minute training module on reading a P&L for new managers. Explain the cognitive reasoning behind the sequence."
- "Turn this survey result into a data story for the leadership deck, one slide per beat."

## Skills it carries

| Skill | Category | What it does |
|---|---|---|
| `cognitive-design` | design | Perception, memory, attention, Gestalt, and encoding-hierarchy foundations; three structuring frameworks; domain guidance for visualization, product UX, and education |
| `information-architecture` | design | Content audits, card sorting, taxonomy and facet design, navigation depth, labeling, tree testing |
| `d3-visualization` | design | D3.js data joins, scales, shapes, layouts (force, hierarchy, geo), transitions, and interactions, with workflows and templates |
| `visual-storytelling-design` | design | Narrative arc, opening strategy, annotation, scrollytelling, and framing for data stories and presentations |
| `design-evaluation-audit` | design | 8-dimension cognitive checklist, 4-criteria visualization audit, severity classification, fix recommendations |
| `cognitive-fallacies-guard` | design | Visual-mislead scan, cognitive-bias check, data-integrity verification, per-fallacy fixes |
| `slop-detector` | writing | Flags generic, AI-explainer patterns in written rationale before it ships |
| `readability-check` | writing | Scores prose on five readability formulas and rewrites the sentences that fail |

The two `writing` skills are copied from `shared/skills/` and are shared with other packages in this repository.

## What changed from the Claude version

- The agent body became `SOUL.md`. The "I will now use the X skill" invocation ritual is now "load X with `skill_view` before the work", and the six-phase pipeline, routing tables, and collaboration principles carry over intact.
- Tool names were mapped to Hermes tools: `web_search` and `web_extract` for research, `read_file` and `vision_analyze` for supplied designs and screenshots, `write_file` and `patch` for deliverables, `clarify` for design-direction choices, `terminal` for the readability script.
- Each skill's `resources` folder was split into the Hermes support directories (`references/`, `templates/`, `assets/`); every link in the SKILL.md files was checked against the files that now exist, and eight stale section anchors in `d3-visualization` were repointed.
- Skill descriptions were cut to the 60-character Hermes index limit, with the original trigger phrases moved into a `## When to Use` section in each skill.
- Every skill gained a `## Verification` section that names the check proving the work is done (the tree-test threshold, the audit rubric, the browser checks for D3 output).
- The agent now finishes written deliverables with `slop-detector` and `readability-check`, which the Claude agent listed but never scheduled.
- The model is pinned in `config.yaml`: `meta/muse-spark-1.3` on OpenRouter at high effort; switch to `openai/gpt-6-astra` for the coding end (`docs/MODELS.md`).
