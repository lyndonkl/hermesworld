---
name: domain-modeling-grill
description: "Grill the user and maintain living architecture docs."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    tags: [Domain Modeling, ADR, Architecture, Ideation]
    related_skills: [socratic-grilling]
---

# Domain Modeling Grill

An extension of the Socratic Grilling session that adds living documentation. As the interview progresses, you actively codify the emerging shared mental model into Architecture Decision Records (ADRs) and a Domain Glossary.

## When to Use

- The user wants to design a complex system and explicitly asks to "grill with docs" or model the domain.
- The ideation phase reaches a point where terminology and data structures need to be formally defined.

## Procedure

1. **Activate Scaffolding:** First, adopt the rigid conversational loop defined in the `socratic-grilling` skill (Reflect, Diverge, Converge on one question, Recommend).
2. **Draft the Glossary:** As domain terms are introduced by the user or yourself, maintain a living glossary in a scratchpad or explicitly echo the definitions back to the user for validation.
3. **Draft ADRs:** For every major architectural decision resolved during the grilling, draft a lightweight Architecture Decision Record (Context, Decision, Consequences) and save it to the workspace (e.g., `docs/adr/`).
4. **Maintain Alignment:** Use these documents as the source of truth. If the user contradicts an earlier ADR, gently point out the conflict and ask how they want to resolve it.

Do not write implementation code during this phase. Focus entirely on codifying the conceptual domain model.
