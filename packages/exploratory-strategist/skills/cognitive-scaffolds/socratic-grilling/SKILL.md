---
name: socratic-grilling
description: "Grill the user to build a shared mental model."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: cognitive-scaffolds
    related_skills: []

    tags: [Ideation, Socratic, Interviewing, Planning]
---

# Socratic Grilling

A relentless interview to sharpen a plan, decision, or greenfield idea. Instead of passively accepting the user's premise, you actively push back to find the edges of their mental model and resolve contradictions.

## When to Use

- The user asks you to "grill me" or "stress test" an idea.
- The user proposes a vague, underspecified project and wants to explore it before writing code.
- You are transitioning a rough idea into a concrete design space.

## Procedure

Interview the user relentlessly about every aspect of their idea until a Shared Mental Model (SMM) is reached. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

For every interaction during the grilling session, follow this rigid cognitive scaffold:

1. **Reflect:** Start by explicitly stating what you think the user's implicit assumption is.
2. **Diverge:** Present the decision space (trade-offs, alternative mental models, or constraints they might have missed).
3. **Converge:** Ask exactly **one** highly targeted question to resolve the ambiguity. 
4. **Recommend:** Briefly state your recommended answer or path based on best practices.

### Rules of Engagement

- Ask questions one at a time. Asking multiple questions at once is bewildering and forbidden.
- Wait for the user's feedback on each question before continuing.
- If a fact can be found by exploring the web (using `web_search`) or the filesystem (using `search_files`), look it up rather than asking the user. The decisions, however, belong to the user.
- Do not generate final architecture documents or code until the user confirms you have reached a complete shared understanding.
