from pathlib import Path

base = Path('teams/exploratory/skills/cognitive-scaffolds')

# brainstorm-diverge-converge
(base / 'brainstorm-diverge-converge' / 'SKILL.md').write_text("""---
name: brainstorm-diverge-converge
description: "Facilitate divergent brainstorming followed by convergence."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    tags: [Scaffolds, Cognitive, Ideation]
    related_skills: []
---

# Brainstorm Diverge-Converge

Applies structured divergent-convergent thinking to generate many creative options, organize them into clusters, and systematically narrow them down.

## When to Use

- The user asks for "brainstorming", "ideation", or "divergent thinking".
- Exploring product ideas or solving open-ended strategic problems.

## Procedure

You are an autonomous Hermes orchestrator. Maintain state internally and execute this scaffold across conversational turns:

1. **Diverge Phase:** When the user proposes a seed idea, generate 5-7 radically divergent lateral options. Do not ask for permission; provide the options immediately.
2. **Present & Clarify:** Group the options into logical clusters. Present the clusters and ask the user **exactly one** clarifying question about which direction they prefer.
3. **Converge Phase:** Once they select a cluster, systematically prune the others. Generate a concrete synthesis of the winning direction.
4. **Handoff:** Suggest using `handoff-compaction` to formalize the synthesized result.
""")

# deliberation-debate-red-teaming
(base / 'deliberation-debate-red-teaming' / 'SKILL.md').write_text("""---
name: deliberation-debate-red-teaming
description: "Run a structured red-teaming debate to test hypotheses."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    tags: [Scaffolds, Cognitive, Ideation]
    related_skills: []
---

# Deliberation, Debate & Red Teaming

Challenges plans and decisions from adversarial perspectives to surface blind spots, hidden assumptions, and vulnerabilities.

## When to Use

- The user asks to "red team", "validate strategy", or "test for blind spots".
- The user presents a complex plan that requires adversarial review.

## Procedure

You are an autonomous Hermes orchestrator running a Socratic red-teaming session. 

1. **Adopt Adversarial Stance:** When the user presents a plan, explicitly state the most catastrophic vulnerability or hidden assumption you see.
2. **The Debate Loop:** 
   - Attack one specific component of their plan.
   - Wait for their defense.
   - If their defense is weak, push harder. If it is strong, concede the point and attack the next vulnerability.
3. **One Question Constraint:** Never ask more than one question per turn. Force the user to resolve the contradiction before moving on.
4. **Synthesis:** Once all vectors are exhausted, produce a "Risk Register & Mitigations" summary.
""")

# cognitive-fallacies-guard
(base / 'cognitive-fallacies-guard' / 'SKILL.md').write_text("""---
name: cognitive-fallacies-guard
description: "Audit visualizations for cognitive fallacies and misleads."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    tags: [Scaffolds, Cognitive, Ideation]
    related_skills: []
---

# Cognitive Fallacies Guard

Detects visual misleads, cognitive biases, and data integrity violations in charts, dashboards, and presentations.

## When to Use

- The user asks to "audit for chartjunk", "check data integrity", or "scan for cognitive biases".
- The user provides a design or visualization description to review.

## Procedure

When asked to audit a chart, presentation, or design, execute this silently and output the final audit:

1. **Scan for Misleads:** Identify chartjunk, 3D effects, and truncated axes.
2. **Cognitive Bias Check:** Analyze the text framing for confirmation bias and anchoring.
3. **Data Integrity:** Verify honest axes, fair comparisons, and context completeness.
4. **Output Report:** Generate a structured audit listing severity levels (High/Medium/Low) for each detected fallacy and specific mitigation recommendations.
""")

# socratic-teaching-scaffolds
(base / 'socratic-teaching-scaffolds' / 'SKILL.md').write_text("""---
name: socratic-teaching-scaffolds
description: "Guide users through Socratic teaching and scaffolding."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    tags: [Scaffolds, Cognitive, Ideation]
    related_skills: []
---

# Socratic Teaching Scaffolds

Uses the Socratic method and cognitive scaffolding to guide the user to their own "aha" moments instead of providing direct answers.

## When to Use

- The user is struggling to grasp a concept and wants to learn.
- The user has a deep misconception that requires structured dismantling.

## Procedure

Execute the teaching scaffold across multiple turns. Do not dump the entire curriculum at once.

1. **Diagnose:** Ask one probing question to identify the user's current knowledge level and misconceptions. Wait for response.
2. **Laddering:** Based on the response, design a progression. Provide a hint, analogy, or partial example (Scaffolding Level 4 or 3).
3. **Fade:** As the user gets it right, remove the scaffolding. Ask them to explain it back or solve a harder variant.
4. **Guardrail:** Never give the direct answer unless the user is completely stuck and frustrated. Always use the Socratic method to lead them to the insight.
""")

