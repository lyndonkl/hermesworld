---
name: design-evaluation-audit
description: Scores designs on cognitive checklists with ranked fixes.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: design
    tags: [Design Review, Usability Audit, Cognitive Checklist, Visualization Audit, Severity Triage]
    related_skills: [cognitive-design, cognitive-fallacies-guard, readability-check]
---
# Design Evaluation & Audit

Evaluates an existing design against cognitive science principles with a repeatable 8-dimension checklist (visibility, hierarchy, chunking, simplicity, memory, feedback, consistency, scanning), a 4-criteria visualization audit scored 1-5 (clarity, efficiency, integrity, aesthetics), and severity-classified fix recommendations. The output is an audit report with evidence, not a redesign; `cognitive-design` handles creating designs and `cognitive-fallacies-guard` handles misleading charts.

## When to Use

- Conducting design reviews or critiques: "review this design", "evaluate", "audit", "what's wrong with this".
- Evaluating a design for cognitive alignment against repeatable checklists rather than taste.
- Quality assurance before launch, or diagnosing usability issues in a shipped interface, form, or dashboard.
- Choosing between design alternatives with objective, scored criteria.
- Not for creating new designs (`cognitive-design`) or detecting misleading visualizations (`cognitive-fallacies-guard`).

Load any reference file with `skill_view("design-evaluation-audit", file_path="references/<file>.md")`; the paths below are relative to this skill.

---

## Skill Boundaries

**Use instead of this skill for:**
- Creating new designs from scratch: use `cognitive-design`
- Learning cognitive theory: use `cognitive-design` Path 1
- Detecting misleading visualizations: use `cognitive-fallacies-guard`

---

## Design Review Workflow

**Time:** 30-90 minutes depending on scope

**Copy this checklist and track your progress:**

```
Design Evaluation Progress:
- [ ] Step 1: Systematic Assessment
- [ ] Step 2: Visualization Quality Audit (if applicable)
- [ ] Step 3: Severity Classification & Prioritization
- [ ] Step 4: Fix Recommendations
```

### Step 1: Systematic Assessment

Apply the Cognitive Design Checklist across all 8 dimensions: Visibility, Visual Hierarchy, Chunking, Simplicity, Memory Support, Feedback, Consistency, Scanning Patterns. Check every item. Record pass/fail for each dimension with specific evidence.

**Resource:** [Cognitive Design Checklist](references/cognitive-checklist.md)

### Step 2: Visualization Quality Audit (if applicable)

If the design includes data visualizations, apply the 4-Criteria Visualization Audit. Score each criterion 1-5: Clarity, Efficiency, Integrity, Aesthetics. Calculate average and identify weakest dimension.

**Resource:** [Visualization Audit Framework](references/visualization-audit.md)

### Step 3: Severity Classification & Prioritization

Classify every finding by severity:
- **CRITICAL:** Integrity violations, accessibility failures, users cannot complete core tasks. Fix immediately.
- **HIGH:** Clarity/efficiency issues preventing use, missing feedback for critical actions, working memory overload (>10 ungrouped items). Fix before launch.
- **MEDIUM:** Suboptimal patterns, aesthetic issues, minor inconsistencies. Fix in next iteration.
- **LOW:** Minor optimizations, polish items. Fix when convenient.

**Priority rule:** Fix foundation-first — perception before coherence, integrity before aesthetics, critical before high.

### Step 4: Fix Recommendations

For each finding, document:
1. **What is wrong** — specific description with evidence
2. **Why it matters** — which cognitive principle is violated
3. **How to fix** — concrete, actionable recommendation
4. **Expected outcome** — what improves after the fix
5. **Effort estimate** — quick fix (minutes), moderate (hours), significant (days)

Verify fixes don't harm other dimensions.

---

## Path Selection Menu

### Path 1: Run Cognitive Design Checklist

**Choose this when:** Evaluating any interface, layout, content page, form, or general design.

**What you'll get:** Pass/fail across 8 cognitive dimensions, test methods, common failures, severity-classified findings.

**Time:** 20-40 minutes

**→ [Go to Cognitive Design Checklist](references/cognitive-checklist.md)**

---

### Path 2: Run Visualization Audit

**Choose this when:** Evaluating data visualizations — charts, graphs, dashboards, infographics.

**What you'll get:** 1-5 scores on Clarity, Efficiency, Integrity, Aesthetics with pass/fail threshold.

**Time:** 15-30 minutes per visualization

**→ [Go to Visualization Audit Framework](references/visualization-audit.md)**

---

### Path 3: Combined Review

**Choose this when:** Comprehensive review covering both interface elements and data visualizations.

**Process:** Run Cognitive Checklist first, then Visualization Audit on each data component, merge findings, produce unified fix list.

**Time:** 45-90 minutes

**→ Start with [Cognitive Checklist](references/cognitive-checklist.md), then [Visualization Audit](references/visualization-audit.md)**

---

## Quick Reference

### 3-Question Rapid Check

**1. Attention** — "Is it obvious what to look at first?"
- If NO: hierarchy and visibility issues

**2. Memory** — "Is the user required to remember anything that could be shown?"
- If NO: memory support and chunking issues

**3. Clarity** — "Can someone unfamiliar understand in 5 seconds?"
- If NO: simplicity and comprehension issues

All YES = likely cognitively sound. Any NO = run full checklist on the failing area.

---

## Verification

An audit report is complete when:

- All 8 checklist dimensions have a pass/fail with specific evidence, and every visualization has four 1-5 scores (see [Scoring Summary](references/cognitive-checklist.md#scoring-summary) and [Using the 4-Criteria Framework](references/visualization-audit.md#using-the-4-criteria-framework)).
- Every finding carries all five fields: what is wrong, why it matters (the violated principle), how to fix, expected outcome, effort.
- Findings are ordered CRITICAL, HIGH, MEDIUM, LOW, foundation-first.
- Scoring the report against [assets/evaluators/rubric_design_evaluation.json](assets/evaluators/rubric_design_evaluation.json) averages 3.5 or higher, with Severity Classification and Evidence Quality both at 3 or above.

Write the report to a file with `write_file` and run `readability-check` on it before delivery.

---

## Guardrails

**Out of scope:** Creating designs, teaching theory, providing domain guidance, replacing user testing, or covering full accessibility compliance.

**In scope:** Systematic evaluation against cognitive principles, severity-classified findings, prioritized fix recommendations, and visualization quality scoring.
