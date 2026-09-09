---
name: cognitive-fallacies-guard
description: Flags chartjunk, truncated axes, and biased data framing.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: design
    tags: [Misleading Charts, Chartjunk, Data Integrity, Cognitive Bias, Truncated Axis]
    related_skills: [design-evaluation-audit, cognitive-design, d3-visualization]
---
# Cognitive Fallacies Guard

Detects visual misleads, cognitive bias exploitation, and data integrity violations in visualizations, dashboards, reports, and presentations, then prescribes the specific fix for each. It works as a three-layer scan: visual noise and perceptual distortion, bias reinforcement, and data honesty. It does not create designs, evaluate general usability, or judge aesthetics; `cognitive-design` and `design-evaluation-audit` do that.

## When to Use

- The user mentions chartjunk, misleading chart, truncated axis, data integrity, visual deception, 3D chart problems, or cherry-picking data.
- A visualization, dashboard, report, or presentation must be audited for accuracy and honesty before it is published.
- Someone asks "is this chart honest?" or why readers keep misinterpreting a chart.
- A data story or dashboard framing may exploit confirmation bias, anchoring, or one-sided comparisons.
- Not for general design evaluation (`design-evaluation-audit`) or cognitive foundations (`cognitive-design`).

Load any reference file with `skill_view("cognitive-fallacies-guard", file_path="references/<file>.md")`; the paths below are relative to this skill.

---

## Overview

Visualizations are persuasive — common mistakes cause systematic misinterpretation, not just aesthetic failures. This skill scans for visual misleads (chartjunk, truncated axes, 3D distortion), checks for cognitive bias exploitation (confirmation bias reinforcement, anchoring, framing manipulation), and verifies data integrity (honest axes, complete data, fair comparisons).

**Related skills:** `design-evaluation-audit` for general design evaluation, `cognitive-design` for cognitive foundations, `d3-visualization` for creating visualizations, `visual-storytelling-design` for data stories.

---

## Fallacy Audit Workflow

**Time:** 15-30 minutes

**Copy this checklist and track your progress:**

```
Fallacy Audit Progress:
- [ ] Step 1: Scan for Visual Misleads
- [ ] Step 2: Check for Cognitive Biases
- [ ] Step 3: Verify Data Integrity
```

### Step 1: Scan for Visual Misleads

Check for chartjunk, 3D effects, truncated axes, volume illusions, and inappropriate chart types. These are the most common and visible fallacies.

**Resource:** [Fallacies Catalog](references/fallacies-catalog.md) — Sections 1-2 (Visual Noise, Perceptual Distortion)

### Step 2: Check for Cognitive Biases

Look for confirmation bias reinforcement, anchoring effects, and framing manipulation. These are subtler but can significantly influence interpretation.

**Resource:** [Fallacies Catalog](references/fallacies-catalog.md) — Section 3 (Cognitive Bias Exploitation)

### Step 3: Verify Data Integrity

Confirm honest axes, complete data, fair comparisons, proper context, and no spurious correlations. This is the most critical layer.

**Resource:** [Detection Patterns](references/detection-patterns.md) — Integrity Principles and Quick Scan Checklist

---

## Path Selection Menu

### Path 1: Visual Misleads Scan

**Choose this when:** Checking for chartjunk, 3D effects, truncated axes, and encoding problems.

**→ [Go to Fallacies Catalog](references/fallacies-catalog.md) — Sections 1-2**

---

### Path 2: Cognitive Bias Check

**Choose this when:** Looking for bias reinforcement in dashboard design, presentation framing, or data selection.

**→ [Go to Fallacies Catalog](references/fallacies-catalog.md) — Section 3**

---

### Path 3: Data Integrity Verification

**Choose this when:** Verifying completeness, honesty, and context of data presentation.

**→ [Go to Detection Patterns](references/detection-patterns.md)**

---

## Quick Reference

### 5 Integrity Principles

1. **Honest Axes** — Bar charts start at zero; uniform scale intervals; clear labels
2. **Fair Comparisons** — Same scale for compared items; no dual-axis manipulation
3. **Complete Context** — Full time period shown; baselines provided; denominators clarified
4. **Accurate Encoding** — Visual proportional to numerical; no volume illusions; 2D design
5. **Transparency** — Data sources cited; limitations acknowledged; methodology stated

### Quick Severity Guide

- **CRITICAL:** Integrity violations (truncated bars without disclosure, cherry-picked data, implied causation)
- **HIGH:** Perceptual distortions (3D effects, volume illusions, missing denominators)
- **MEDIUM:** Bias reinforcement (one-sided framing, anchoring order, confirmation bias layout)
- **LOW:** Visual noise (excessive gridlines, decorative elements, ornamental borders)

---

## Verification

- Run the [Quick Scan Checklist](references/detection-patterns.md#quick-scan-checklist) in full and record a result for every item, including the ones that pass.
- Report with the [Reporting Template](references/detection-patterns.md#reporting-template): each fallacy named, its severity, the misreading it would cause, and the specific fix.
- Score the audit against [assets/evaluators/rubric_cognitive_fallacies.json](assets/evaluators/rubric_cognitive_fallacies.json) (seven criteria, 1-5). An average of 3.5 or above passes; a score below 3 on Visual Mislead Detection or Data Integrity Verification requires a re-audit.

---

## Guardrails

**Scope boundaries:** This skill detects visual misleads, identifies cognitive bias exploitation, verifies data integrity, and provides specific fixes for each fallacy found. It does not create designs, evaluate general usability, teach cognitive theory, or assess aesthetic quality.
