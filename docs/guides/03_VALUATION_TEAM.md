# Phase 2: Finance & The Valuation Team

The Valuation Team runs end-to-end corporate analyses, from parsing SEC filings to writing investment reports.

## The Roster
- **`valuation-orchestrator` (Orchestrator):** Manages the mandate and routes the stages.
- **`company-diagnostician`, `intrinsic-valuation-analyst`, etc. (Strong):** Judgment specialists.
- **`financial-data-collector`, `cost-of-capital-analyst` (Fast):** Procedure executors.
- **`investment-reconciler` (Writer):** Writes the final report.

## Creative Use Case: The "Hostile Takeover" Defense Analysis

**The Situation:** You are a consultant analyzing whether a legacy retail company is vulnerable to a private equity buyout.

**The Workflow:**
1. **The Mandate:**
   You open a Bot Chat with `valuation-orchestrator` and type: *"Run an LBO/Takeover vulnerability analysis on [Ticker]. Assume a 20% premium on current market cap."*
2. **Silent Delegation:**
   The Orchestrator doesn't write back immediately. In the background, it uses `message_agent`:
   - It wakes up `company-diagnostician` to classify the target's moat and asset base (real estate vs IP).
   - It wakes up `financial-data-collector` to pull the last 3 years of 10-Ks and calculate free cash flow.
   - It passes the cash flows to `cost-of-capital-analyst` to calculate the WACC and debt capacity.
3. **Synthesis:**
   Once the sub-agents finish their background computations, the Orchestrator feeds the data to the `investment-reconciler`, which drafts a hostile-takeover defense memo. The Orchestrator delivers the markdown memo directly into your chat.
