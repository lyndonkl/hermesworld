# Phase 1: Building & The Engineering Team

The Engineering Team builds, tests, and reviews software architectures based on compacted epics.

## The Roster
- **`engineering-planner` (Orchestrator):** Breaks down features into dependency graphs.
- **`software-engineer` (Strong):** Executes standard coding tasks in isolated worktrees.
- **`ml-engineer` (Strong):** Handles PyTorch pipelines and heavy numerical work.
- **`code-reviewer` (Writer):** Audits architecture, reads diffs, and writes docs.

## Creative Use Case: Implementing the Vector Search Microservice

**The Situation:** You just finished ideation and have `epic.md`. It's time to build the `lancedb` Rust backend.

**The Workflow:**
1. **Spawning the Async Factory:**
   You create a Kanban ticket:
   ```bash
   hermes kanban create --board engineering \
     --assignee engineering-planner \
     --title "Build LanceDB backend" \
     --body "$(cat epic.md)" \
     --workspace worktree:./lancedb-backend
   ```
2. **The Planner Wakes Up:**
   The `engineering-planner` reads the Epic. It realizes this requires Rust systems code and an API boundary. It splits the ticket into three sub-tasks: "Schema Setup", "Rust Actix API", and "Code Review".
3. **Parallel Execution:**
   The Planner delegates "Schema Setup" and "Rust Actix API" to the `software-engineer`. Because you specified `--workspace worktree:./lancedb-backend`, the engineer automatically clones a new git worktree. It writes the code, runs `cargo check`, fixes a borrow checker error, and commits the code.
4. **Peer Review:**
   The Planner assigns the `code-reviewer` to audit the diff. The reviewer flags that the API doesn't have rate limiting, adds a comment to the PR, and pushes a fix.
5. **Human Sign-off:**
   You receive a notification that the ticket is in "Review". You check the code, merge the PR, and delete the worktree.
