# How to Use Hermes: Interfaces and Modes

Hermes is a flexible, multi-agent system that can be driven through various interfaces depending on the complexity of your task. This guide covers how to interact with the system across different modes.

---

## 1. Chatting from the Terminal (CLI)
The most direct way to interact with a specific Hermes profile is through the terminal.

*   **Interactive Chat:** Launch a continuous chat session inside your current working directory.
    ```bash
    hermes -p <profile-name> chat
    ```
    *Example:* `hermes -p welch-ai-guide chat`

*   **One-Shot Query:** Feed a specific input to an agent and exit immediately once it responds. Great for piping logs or diffs.
    ```bash
    hermes chat -p <profile-name> -Q < "What does this error mean?"
    ```

---

## 2. Chatting from the UI (Desktop App / Bot Mode)
The Hermes Desktop App (Bot Mode) provides a rich, persistent interface for chatting with agents.

*   **How to Run:** Launch the Hermes Desktop application. Select your desired profile (e.g., `valuation-orchestrator`) from the sidebar to open a chat.
*   **Working Directories:** Because you don't launch the UI from a specific folder (like you do in the CLI), **always provide absolute paths** in your first message if you want the agent to analyze a specific local project.
    *   *Example:* `"Please review the code in /Users/kushaldsouza/Desktop/my-project"`

---

## 3. Agent-to-Agent Chat (Inter-message Chat)
Hermes agents can communicate with *each other* to delegate work or ask for specialized analysis.

*   **Within the UI (Bot Mode):** 
    When chatting with an Orchestrator profile (like `valuation-orchestrator`) in the UI, the orchestrator has access to the `message_agent` tool. If you ask it a highly specific question, it will silently message a specialist (e.g., `company-diagnostician`) in the background, wait for the response, and then reply to you. You do not need to manage this—the Orchestrator handles the routing automatically.
*   **Within the Terminal (CLI):** 
    Terminal sessions are generally isolated 1-on-1 chats. To achieve agent-to-agent delegation in the terminal, the active agent uses the `delegate_task` tool to spawn a subagent child process. The child process completes its goal and returns the result to the parent agent.

---

## 4. Kanban (Asynchronous Multi-Agent Factory)
The Kanban system is designed for long-running, durable tasks (like generating a massive valuation report) where multiple agents work in parallel. 

### **CRITICAL REQUIREMENT: The Gateway Daemon**
If you just create tickets, they will sit in the `todo` column forever. To make agents wake up and execute the tickets, you **must start the background dispatcher**. The dispatcher lives inside the Hermes gateway.

Open a separate terminal window and run:
```bash
hermes gateway start
```
*(Leave this running in the background).*

### **Creating and Managing the Board**
With the gateway running, you manage the board purely from your terminal:

1.  **Create a Ticket:**
    ```bash
    hermes kanban create
    ```
    *(Follow the prompts to title and describe the task).*
2.  **Assign the Ticket:**
    ```bash
    hermes kanban assign
    ```
    *(Assign it to the profile best suited for the job, e.g., `intrinsic-valuation-analyst`).*
3.  **Review the Board:**
    There is no separate web UI for Kanban. You review the board directly in your terminal:
    *   `hermes kanban ls` (Prints a table view of Todo, In Progress, Review, and Done).
    *   `hermes kanban show <id>` (Prints the full details and comments of a specific ticket).
    *   `hermes kanban watch` (Live-streams events to your terminal as bots claim and complete tasks).
