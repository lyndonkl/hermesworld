# Hermesworld Usage Guide Overview

Welcome to the Hermesworld agent network. This ecosystem relies on **autonomous bot teams** working across asynchronous kanban boards, synchronized desktop chats, and embedded CLI toolchains. 

## The Core Interfaces

1. **Hermes Kanban (The Async Factory):**
   * **Best for:** Long-running, multi-file engineering epics or end-to-end financial valuations.
   * **How it works:** A background `hermes gateway start` daemon monitors a SQLite board. You drop tickets (via `hermes kanban create`), and Orchestrator profiles wake up, break down the work, spawn Subagents into isolated `worktree:` environments, and run tests.

2. **Bot Chat / UI Messaging (The Synchronous Office):**
   * **Best for:** Ad-hoc questions, Phase 0 ideation, and architectural drafting.
   * **How it works:** Open the Hermes Desktop app. Selecting an Orchestrator spawns an interactive session. The orchestrator may silently spin up teammates in the background via `message_agent` while keeping your chat interface clean.

3. **CLI One-Shots (The Terminal Tools):**
   * **Best for:** Piping git diffs, logs, or error traces to specialists.
   * **How it works:** `hermes chat -p <profile> -Q < "Traceback..."`.

## Dive Deeper
- [Phase 0: Ideation (Exploratory Team)](01_EXPLORATORY_TEAM.md)
- [Phase 1: Building (Engineering Team)](02_ENGINEERING_TEAM.md)
- [Phase 2: Finance & Valuations (Valuation Team)](03_VALUATION_TEAM.md)
- [Specialists & Standalones](04_SPECIALISTS.md)
- [How to Use Hermes: Interfaces and Modes](05_USAGE_MODES.md)
