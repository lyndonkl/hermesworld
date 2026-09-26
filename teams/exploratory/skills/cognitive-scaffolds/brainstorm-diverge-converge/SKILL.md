---
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
