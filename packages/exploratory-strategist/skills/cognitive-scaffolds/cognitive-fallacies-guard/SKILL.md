---
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
