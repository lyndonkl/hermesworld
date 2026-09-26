# Hermesworld Ecosystem Usage Guide

This document is a comprehensive guide to operating the agents within the `hermesworld` ecosystem. It outlines the primary interaction paradigms (how to talk to agents) and provides concrete usage scenarios for every team and standalone profile in your repository.

---

## 1. Interaction Paradigms

Hermes allows you to interact with agents in two distinct ways: asynchronously for massive projects, or synchronously for targeted jobs.

### A. Hermes Kanban (The Asynchronous Factory)
**Best for:** Multi-stage, multi-file engineering pipelines that take hours to run and require isolation.

Hermes Kanban moves away from synchronous chat. Instead, you put tickets on a shared SQLite board, and a background dispatcher spawns the appropriate bots to execute them in isolated workspaces.

**How to Spawn & Interact:**
1. **Start the Dispatcher:** In a background terminal, run the dispatcher daemon:
   ```bash
   hermes gateway start
   ```
   *This polls `~/.hermes/kanban.db` every 60 seconds looking for ready tasks.*
2. **Create a Task:** From any terminal, push a ticket to the board and assign it to an orchestrator profile:
   ```bash
   hermes kanban create --board engineering \
     --assignee engineering-planner \
     --title "Build a new rate limiter" \
     --body "Implement a Redis-backed rate limiter in src/middleware." \
     --workspace worktree:./rate-limiter-feature
   ```
   *Note: Using `--workspace worktree:<path>` forces the agent to clone the repo into an isolated git branch, preventing it from breaking your main code.*
3. **Monitor the Board:**
   ```bash
   hermes kanban board --name engineering
   ```
4. **Human-in-the-loop:** If the `engineering-planner` gets blocked, its state changes to `blocked` and it leaves a comment on the ticket. You interact by replying to the ticket:
   ```bash
   hermes kanban comment <task-id> "Use the generic Redis driver we built last week."
   ```

### B. Desktop Bot Mode & UI Messaging (The Synchronous Office)
**Best for:** Ad-hoc questions, targeted refactors, or human-driven design sessions.

Instead of a durable queue, you can spawn an agent directly in the Hermes Desktop app and talk to them like a coworker.

**How to Spawn & Interact:**
1. **Enable Bot Mode:** Open Hermes Desktop -> Settings -> Plugins -> Toggle `Bots` ON.
2. **Open a Bot Chat:** Click on any bot (e.g., `company-diagnostician`) in your right-hand roster. This spawns a dedicated session.
3. **Direct Delegation:** If you are talking to an orchestrator (like `valuation-orchestrator`), it will automatically delegate sub-tasks to its teammates using the `message_agent` tool in the background. You just wait for the final answer.
4. **Direct Messaging (The `@` Mention):** If you are working on code and want a specific bot's opinion without switching chats, you can directly mention them or use the CLI:
   ```bash
   hermes chat -p code-reviewer -c "Ad-hoc Review" "Can you look at src/auth.py and tell me if it's secure?"
   ```

---

## 2. Phase 0: Ideation (The Exploratory Team)
*Before writing tickets or code, you need a Shared Mental Model. The Exploratory Team acts as your Socratic sounding board.*

### Roster
- **`exploratory-strategist` (Orchestrator):** Cross-questions the user, maintains domain models, and compacts handoff epics.

### Scenario: Greenfield Project Brainstorming (UI Messaging)
**Goal:** You want to build a real-time recommendation engine but don't know the exact architecture.
1. Open Hermes Desktop and click `exploratory-strategist` in the Bot roster.
2. Type: *"I want to build a real-time recommendation engine. Grill me on the architecture."*
3. The strategist activates its `socratic-grilling` scaffold. Instead of writing code, it states your implicit assumptions and asks exactly *one* targeted question (e.g., *"Are you prioritizing latency or recommendation accuracy?"*).
4. As you answer, the strategist uses its `domain-modeling-grill` to silently draft Architecture Decision Records (ADRs) to your workspace.
5. Once you reach a Shared Mental Model, type: *"Handoff the context."*
6. The strategist uses `handoff-compaction` to generate a structured `epic.md` file containing all decisions made and known unknowns.
7. You are now ready to pass `epic.md` to the Engineering Kanban board!

---

## 3. Team 1: Engineering (The Builders)
*The Engineering Team builds, tests, and reviews software architectures.*

### Roster
- **`engineering-planner` (Orchestrator):** Breaks down features into dependency graphs.
- **`software-engineer` (Strong):** Executes standard coding tasks in isolated worktrees.
- **`ml-engineer` (Strong):** Handles PyTorch pipelines and heavy numerical work.
- **`code-reviewer` (Writer):** Audits architecture, reads diffs, and writes docs.

### Scenario 1: Architecting a New Feature (Kanban)
**Goal:** Build a new recommendation microservice.
1. Run `hermes kanban create --assignee engineering-planner --title "Build Recommendation Service" --workspace worktree:./rec-svc`.
2. The `engineering-planner` wakes up, queries Honcho memory for past architectural standards, and breaks the ticket into three sub-tasks: Data Pipeline, API Layer, and Review.
3. It assigns Data Pipeline to `ml-engineer` and API Layer to `software-engineer`.
4. `ml-engineer` writes the PyTorch code; `software-engineer` writes the FastAPI endpoints.
5. The planner assigns `code-reviewer` to audit the diff. The reviewer writes a `README.md` and approves.
6. The planner marks the parent ticket `done`.

### Scenario 2: Quick Script Fix (UI Messaging)
**Goal:** You have a broken Python script and want a quick fix.
1. Open Hermes Desktop.
2. Click `software-engineer` in the Bot roster.
3. Type: *"I'm getting a KeyError in `scripts/parse.py`. Here's the traceback. Fix it."*
4. The engineer loads its `engineering-playbooks` skill, edits the file, and runs a test in the terminal before replying to you.

---

## 3. Team 2: Valuation (The Financiers)
*The Valuation Team runs end-to-end corporate analyses, from parsing SEC filings to writing investment reports.*

### Roster
- **`valuation-orchestrator` (Orchestrator):** Manages the mandate and routes the stages.
- **`company-diagnostician`, `intrinsic-valuation-analyst`, etc. (Strong):** Judgment specialists.
- **`financial-data-collector`, `cost-of-capital-analyst` (Fast):** Procedure executors.
- **`investment-reconciler` (Writer):** Writes the final report.

### Scenario 1: End-to-End DCF Valuation (Bot Chat Delegation)
**Goal:** Value Apple Inc. (AAPL).
1. Open Hermes Desktop and click `valuation-orchestrator`.
2. Type: *"Run a full valuation on AAPL in USD for Q3 2026."*
3. The orchestrator takes over. It uses `message_agent` to silently wake up the `company-diagnostician` to classify AAPL's business model.
4. It then delegates data pulling to `financial-data-collector`.
5. Finally, it delegates the DCF math to `intrinsic-valuation-analyst` and hands the results to `investment-reconciler` to write the markdown report. You just watch the final artifacts appear in your directory.

### Scenario 2: Ad-Hoc Breakdown (CLI)
**Goal:** You want to know the Cost of Capital for a specific risky venture, ignoring a full valuation.
1. Run a one-shot CLI command:
   ```bash
   hermes chat -p cost-of-capital-analyst --query-file mandate.txt
   ```
2. The specialist asks you (via `needs_input`) for the risk-free rate and beta assumptions, runs the math, and exits.

---

## 4. Standalone Profiles (The Specialists)
*Independent agents that operate outside of team orchestrators.*

### Roster
- **`superforecaster`:** Deep web research and predictive reasoning.
- **`product-strategist`:** Curates news and drafts product reports.
- **`geometric-deep-learning-architect` & `cognitive-design-architect`:** Heavy math and PyTorch/D3 code design.
- **`welch-ai-guide`:** Documentation and guidance.

### Scenario: Product Strategy Curation (UI Messaging)
**Goal:** You want a market landscape report on AI hardware startups.
1. Open Hermes Desktop and click `product-strategist`.
2. Type: *"Curate the latest news on AI hardware startups and draft a market landscape report."*
3. The strategist runs web searches to compile the data.
4. **Subagent Delegation:** Instead of writing the report itself, the strategist spawns an ephemeral `delegate_task` child running on a cheaper `gemini-3.7-flash` model to draft the prose, saving you OpenRouter credits.
5. The strategist verifies the draft and delivers it to you in the chat.
