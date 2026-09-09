# geometric-deep-learning-architect

A Hermes profile that helps ML engineers apply group theory and symmetry to neural network design. It takes a problem from "what is symmetric about my data?" through empirical validation, group identification, and equivariant architecture design to a numerical audit of the implemented model. The agent is an orchestrator: it carries the state of the pipeline and loads one of five skills for each phase.

## What it does

- Asks the questions that surface candidate symmetries in a dataset, without requiring group theory from the user.
- Writes and runs tests that show whether a hypothesized symmetry actually holds, and by how much.
- Names the mathematical group (cyclic, dihedral, symmetric, SO(3), SE(3), E(3), and their products) and the properties that matter for architecture.
- Designs an equivariant architecture for that group, with a library recommendation and a code skeleton.
- Audits an implemented model end to end, layer by layer, and through its gradients, and locates the module that breaks equivariance.

## The pipeline

0. Context gathering: data type, task, invariant or equivariant output, constraints, user level, operating mode.
1. Symmetry discovery: candidate symmetries with evidence and confidence.
2. Symmetry validation: empirical pass or fail per candidate, with error metrics.
3. Group identification: group, product structure, properties, architecture family.
4. Architecture design: layer stack, representations, library, parameter estimate, code skeleton.
5. Implementation audit: end-to-end, layer-wise, and gradient equivariance tests.
6. Final summary: one specification document covering all of the above.

Quick mode runs 0 → 1 → 4 → 6 in about 15 minutes. Standard adds phases 2 and 3 (about an hour). Deep adds phase 5 (2 to 3 hours). The agent also enters mid-pipeline when the user already has candidates, a group, or code to audit.

## Install

From the repository root:

```bash
tools/install.sh geometric-deep-learning-architect
hermes -p geometric-deep-learning-architect chat
```

Or directly with Hermes:

```bash
hermes profile install ./packages/geometric-deep-learning-architect --alias
```

No model or provider is pinned. `tools/install.sh` seeds the profile's model block from your root profile; change it any time with `hermes -p geometric-deep-learning-architect model`. Running equivariance tests requires Python with PyTorch, plus e3nn, escnn, or pytorch_geometric as the design calls for, in the environment where the agent's `terminal` runs.

## First prompts to try

- "I'm predicting formation energies for small molecules from atomic coordinates. What symmetries should my model respect?"
- "My point cloud classifier loses 20 points of accuracy when I rotate the test set. Is the model actually SO(3) invariant?"
- "My images have 90-degree rotation and flip symmetry. Which group is that, and which escnn layers do I use?"
- "Here is my e3nn model at /path/to/model.py. Audit it for E(3) equivariance and tell me which layer breaks it."
- "Walk me through the whole pipeline for a graph-level regression task, start to finish."

## Skills

| Skill | Category | What it produces |
|---|---|---|
| `symmetry-discovery-questionnaire` | geometric-deep-learning | Symmetry candidate summary with evidence and confidence |
| `symmetry-validation-suite` | geometric-deep-learning | Validation report: per-hypothesis error metrics, group structure checks, recommendation |
| `symmetry-group-identifier` | geometric-deep-learning | Group specification: name, product structure, properties, architecture family |
| `equivariant-architecture-designer` | geometric-deep-learning | Architecture specification with code skeleton; also carries the pipeline patterns reference |
| `model-equivariance-auditor` | geometric-deep-learning | Audit report with located failures and fixes; test suite templates |
| `slop-detector` | writing | Prose quality pass on written deliverables (shared skill) |
| `readability-check` | writing | Readability scoring and rewrite guidance (shared skill) |

## What changed from the Claude version

- The Claude subagent body became `SOUL.md`. Skills are loaded with `skill_view` and followed in the same conversation rather than invoked as separate skill runs. Each phase in `SOUL.md` now records its inputs, output block, and exit criterion so the hand-off between skills is explicit.
- Each skill's single resource folder from the Claude layout was split into `references/`, `templates/`, and `assets/`, and links were rewritten to `skill_view(name, file_path=...)`.
- Each skill received a one-line description, tags, related skills, a `When to Use` list, a `Pitfalls` section, and a `Verification` section. The test-based skills verify with harness controls (identity gives zero error, a broken model fails); the group identifier verifies axioms and determinants on concrete elements.
- The agent's data-type table, common-patterns table, mode table, beginner and expert explanation templates, and the final specification template moved to `skills/geometric-deep-learning/equivariant-architecture-designer/references/gdl-pipeline-patterns.md`.
- Tool names follow Hermes: `read_file`, `write_file`, `terminal`, `search_files`, `web_search`, `web_extract`, `clarify`, `todo`, `delegate_task`. No model tier is pinned per role.
