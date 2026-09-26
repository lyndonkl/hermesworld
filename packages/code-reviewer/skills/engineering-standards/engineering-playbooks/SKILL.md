---
name: engineering-playbooks
description: "Standard procedures and best practices for engineering."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: engineering-standards
    tags: [Engineering, Playbooks, Standards]
    related_skills: []
---
# Engineering playbooks

This skill contains the standard operating procedures for the engineering team. It enforces consistency across the codebase, ensuring that all code written and reviewed adheres to a strict set of design and testing principles. It does not contain code generation scripts.

## When to Use

- When planning a new feature or breaking down an architectural change into smaller tasks.
- When reviewing a pull request for style, security, and performance issues.
- When setting up a new isolated workspace or testing environment.

## Procedure

1. For new features, always start by defining the interface (e.g., function signatures, API endpoints) before implementing the logic.
2. Use explicit type hinting for all function parameters and return values.
3. Create unit tests for every new file introduced into the workspace.
4. Keep functions small (under 50 lines) and avoid deep nesting.

## Pitfalls

- Skipping the unit testing phase before submitting a patch back to the orchestrator.
- Not using a fresh isolated Git worktree for invasive experimental changes.
- Writing monolithic scripts instead of modularizing functions.

## Verification

To verify that the code meets standards, run the language's native linter and test suite (e.g., `pytest` or `npm test`) over the modified files.
