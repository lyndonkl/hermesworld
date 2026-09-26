# Specialists & Standalones

Independent agents that operate outside of team orchestrators, optimized for specific high-leverage tasks.

## The Roster
- **`superforecaster`:** Deep web research and predictive reasoning using Brier scoring frameworks.
- **`product-strategist`:** Curates news and drafts product landscape reports.
- **`geometric-deep-learning-architect`:** Heavy math and PyTorch/D3 code design.
- **`welch-ai-guide`:** Documentation and guidance for the Hermes ecosystem.

## Creative Use Case: The "Black Swan" Market Forecast

**The Situation:** You want to know the probability of a major supply chain disruption in the semiconductor industry in the next 18 months.

**The Workflow:**
1. **CLI One-Shot Pipeline:**
   You want the `superforecaster` to read a custom corpus of PDFs and news clippings you've saved in `~/market-research`.
   ```bash
   cat ~/market-research/*.txt | hermes chat -p superforecaster -Q "Generate a Brier-scored forecast for a Taiwan semiconductor disruption."
   ```
2. **Web Augmentation:**
   The Superforecaster uses its `web_search` and `web_extract` tools to read recent geopolitical analyses, cross-references it with your local text stream, and outputs a highly structured forecast with explicit confidence intervals and base-rate calibrations.
