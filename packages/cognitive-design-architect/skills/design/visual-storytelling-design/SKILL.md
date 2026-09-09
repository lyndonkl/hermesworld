---
name: visual-storytelling-design
description: Turns data into annotated stories for reports and decks.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: design
    tags: [Data Storytelling, Annotation, Scrollytelling, Presentation Design, Narrative Visualization]
    related_skills: [cognitive-design, d3-visualization, cognitive-fallacies-guard, readability-check]
---
# Visual Storytelling Design

Turns data into a guided narrative for data journalism, reports, presentations, and infographics: a Context, Problem, Evidence, Insight arc; an opening strategy; annotation that points at the insight; scrollytelling for progressive reveal; and framing with baselines, comparisons, and clear denominators. It produces a story structure and annotation plan, not the chart code and not an integrity audit; `d3-visualization` and `cognitive-fallacies-guard` cover those.

## When to Use

- The user mentions data storytelling, presentation design, annotated chart, or narrative visualization.
- Creating data-driven articles or reports where the reader must reach an insight rather than just see the numbers.
- Designing infographics with narrative or building scrollytelling experiences on the web.
- Annotating charts to guide interpretation: callouts, arrows, shaded regions, direct labels.
- Framing findings honestly with baselines, comparisons, and denominators so the audience reads them correctly.

Load any reference file with `skill_view("visual-storytelling-design", file_path="references/<file>.md")`; the paths below are relative to this skill.

---

**Core principle:** Structuring data as narrative (Context → Problem → Evidence → Insight) aids comprehension and retention. Annotations guide attention, progressive disclosure reveals complexity gradually, and framing provides context for accurate interpretation.

**Related skills:** Use `cognitive-design` for cognitive principles, `d3-visualization` for D3.js implementation, `design-evaluation-audit` for systematic evaluation, `cognitive-fallacies-guard` for integrity checks.

---

## Story Design Workflow

**Time:** 1-2 hours

**Copy this checklist and track your progress:**

```
Story Design Progress:
- [ ] Step 1: Define Narrative
- [ ] Step 2: Choose Structure
- [ ] Step 3: Apply Cognitive Techniques
- [ ] Step 4: Review for Clarity & Integrity
```

### Step 1: Define Narrative

Determine the story arc: What's the context? What's the question/problem? What data answers it? What's the insight? Choose an opening strategy: lead with human impact, surprising finding, or visual.

**Resource:** [Narrative Techniques](references/narrative-techniques.md) — Narrative Structure section

### Step 2: Choose Structure

Select a template and pattern that fits your story type, audience, and medium. Options include step-by-step article, magazine style, annotated chart, interactive exploration, or presentation deck.

**Resource:** [Storytelling Patterns](references/storytelling-patterns.md) — Templates and Decision Matrix

### Step 3: Apply Cognitive Techniques

Add annotations (callouts, arrows, shaded regions, direct labels). Apply framing with baselines, comparisons, and denominator clarity. Use scrollytelling for progressive revelation if web-based. Consider visual metaphors.

**Resource:** [Narrative Techniques](references/narrative-techniques.md) — Annotations, Scrollytelling, Framing sections

### Step 4: Review for Clarity & Integrity

Verify the story is honest (no cherry-picking, balanced framing), clear (insight obvious in 5 seconds), and complete (sources cited, limitations noted). Use `design-evaluation-audit` for systematic evaluation and `cognitive-fallacies-guard` for integrity verification.

---

## Path Selection Menu

### Path 1: Build Narrative Structure

**Choose this when:** Starting a data story and need to define the narrative arc and opening strategy.

**→ [Go to Narrative Techniques](references/narrative-techniques.md) — Sections 1-2**

---

### Path 2: Master Annotation

**Choose this when:** Adding annotations to guide interpretation of existing charts and visualizations.

**→ [Go to Narrative Techniques](references/narrative-techniques.md) — Section 3**

---

### Path 3: Design Scrollytelling

**Choose this when:** Building web-based progressive revelation experiences.

**→ [Go to Narrative Techniques](references/narrative-techniques.md) — Section 4**

---

### Path 4: Apply Framing & Metaphors

**Choose this when:** Providing context, baselines, comparisons, and visual metaphors.

**→ [Go to Narrative Techniques](references/narrative-techniques.md) — Sections 5-6**

---

## Quick Reference

### 5 Storytelling Principles

1. **Lead with insight, not topic** — Title: "Remote workers report 23% higher satisfaction" not "Remote work survey results"
2. **Annotate the insight** — Don't make readers discover it; point it out with callouts
3. **Provide context** — Baselines, historical comparisons, denominators for every percentage
4. **One change at a time** — Scrollytelling: highlight OR annotate, not both simultaneously
5. **Be honest** — Show full data, acknowledge limitations, avoid cherry-picking

---

## Verification

Score the finished story against [assets/evaluators/rubric_visual_storytelling.json](assets/evaluators/rubric_visual_storytelling.json): seven criteria (Narrative Structure, Opening Effectiveness, Annotation Quality, Pattern Appropriateness, Context and Framing, Self-Containedness, Takeaway Clarity) on a 1-5 scale. The story passes at an average of 3.5 or above; a score below 3 on Narrative Structure or Takeaway Clarity means revise before publication. Then run `cognitive-fallacies-guard` on every chart and `readability-check` on the prose.

---

## Guardrails

**Scope:** This skill provides narrative structure, annotation techniques, scrollytelling patterns, framing guidance, story templates, and quality checklists for data storytelling. It does not implement code, evaluate general usability, teach cognitive theory, or check for misleading patterns.
