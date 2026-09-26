# Phase 0: Ideation & The Exploratory Team

Before the first line of code is written, you need a **Shared Mental Model**. The Exploratory Team acts as a relentless Socratic sounding board to turn fuzzy product ideas into concrete architectural epics.

## The Roster
- **`exploratory-strategist` (Orchestrator):** Refuses to write code. Instead, it cross-questions you, models the domain, and compacts handoff documents.

## Creative Use Case: The "Spotify for Podcast Transcripts" App

**The Situation:** You have a vague idea to build a desktop app that searches podcast transcripts using local LLMs. You don't know if you should use Electron, Tauri, SQLite, or vector databases.

**The Workflow:**
1. **Divergent Brainstorming:**
   You open a Bot Chat with `exploratory-strategist` and say: *"I want to build a local podcast search app. Give me lateral ideas."*
   The Strategist triggers its `brainstorm-diverge-converge` scaffold. It instantly outputs 6 wildly different approaches (e.g., an OS-level menu bar app, a CLI tool, a full web-app, etc.) and asks *exactly one* question: *"Which of these form factors fits your usage pattern?"*

2. **Red-Teaming the Choice:**
   You reply: *"Let's go with the Tauri desktop app using a local Qdrant instance."*
   The Strategist flips to `deliberation-debate-red-teaming`. It takes an adversarial stance: *"Qdrant is heavy for a local desktop bundle. You are assuming users want semantic search over keyword search. How will you handle the 500MB binary size constraint for distribution?"* 

3. **Compacting the Epic:**
   After defending your choice and pivoting to `lancedb` for embedded vector search, you say: *"We have a shared mental model. Handoff."*
   The Strategist triggers `handoff-compaction`, distilling the entire debate into a Kanban-ready `epic.md` file in your workspace, complete with known unknowns and phase gates.

4. **Next Steps:** You take `epic.md` and toss it to the Engineering Team.
