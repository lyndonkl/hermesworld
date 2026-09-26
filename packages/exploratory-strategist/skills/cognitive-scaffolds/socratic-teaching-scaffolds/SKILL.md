---
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
