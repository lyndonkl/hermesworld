---
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
