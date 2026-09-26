---
name: handoff-compaction
description: "Compact the conversation into a structured handoff doc."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    related_skills: []

    tags: [Handoff, Compaction, Delegation, Planning]
---

# Handoff Compaction

Compacts the current unstructured conversational context and Socratic ideation into a highly structured handoff document. This artifact acts as an "Epic" that orchestrators on other Kanban boards can immediately consume.

## When to Use

- The user states that the brainstorming phase is over and it is time to hand the work off.
- The user uses a trigger phrase like "handoff", "summarize for engineering", or "create the epic".

## Procedure

Write a `handoff.md` (or `epic.md`) document summarizing the current conversation so a fresh agent (like the `engineering-planner`) can continue the work without needing the chat history.

The document MUST contain the following rigid structure:

1. **Goal:** A clear, unambiguous statement of what needs to be built.
2. **Decisions Made:** A bulleted list of all critical design decisions, constraints, and assumptions validated during the grilling phase.
3. **Known Unknowns:** A list of ambiguities that were intentionally left unresolved, which the next agent will need to figure out.
4. **Suggested Downstream Skills:** A list of Hermes skills the downstream agent should invoke (e.g., `engineering-playbooks`).
5. **Context Links:** Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits). Reference them strictly by absolute path or URL.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information. Save this document to the user's current workspace directory.
