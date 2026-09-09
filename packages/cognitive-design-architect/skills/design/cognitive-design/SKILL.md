---
name: cognitive-design
description: "Explains why designs work: perception, memory, attention."
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: design
    tags: [Cognitive Load, Visual Hierarchy, Gestalt, Perception, Working Memory, Design Principles]
    related_skills: [design-evaluation-audit, cognitive-fallacies-guard, visual-storytelling-design, information-architecture]
---
# Cognitive Design Principles

Grounds design decisions in the perception, attention, memory, and decision-making research that explains why a design works: Tufte, Norman, Ware, Cleveland & McGill, Mayer, and the Gestalt psychologists. It supplies the foundations, three structuring frameworks (Cognitive Design Pyramid, Design Feedback Loop, Three-Layer Model), and domain guidance for visualizations, product interfaces, and educational material. It does not evaluate finished designs, detect misleading charts, or build data stories; sibling skills do that.

## When to Use

- The user mentions cognitive load, visual hierarchy, working memory, preattentive processing, Gestalt principles, encoding hierarchy, or the cognitive design pyramid.
- A new interface, dashboard, visualization, or educational module needs its design decisions grounded in perception, attention, and memory research before anything is drawn.
- Someone asks *why* a design works or fails, or which visual encoding fits a comparison, trend, or lookup task.
- A design in progress needs a 5-minute go/no-go check against attention, memory, and clarity basics.
- Not for evaluating an existing design (`design-evaluation-audit`), checking for misleads (`cognitive-fallacies-guard`), or building a data story (`visual-storytelling-design`).

Load any reference file with `skill_view("cognitive-design", file_path="references/<file>.md")`; the paths below are relative to this skill.

---

## Overview

This skill provides the cognitive science foundations for effective design — the perception, attention, memory, and decision-making principles that explain WHY certain designs work. It helps ground design decisions in research (Tufte, Norman, Ware, Cleveland & McGill, Mayer), apply systematic frameworks (Cognitive Design Pyramid, Design Feedback Loop, Three-Layer Model), choose appropriate visual encodings, and manage attention, memory limits, and cognitive load.

**Related skills:** `design-evaluation-audit` for systematic reviews, `cognitive-fallacies-guard` for detecting misleads, `visual-storytelling-design` for data journalism, `information-architecture` for content organization, `d3-visualization` for D3.js implementation.

---

## Workflows

### Apply Cognitive Principles Workflow

**Use when:** Creating a new interface, dashboard, visualization, or educational content from scratch

**Time:** 1-2 hours

**Copy this checklist and track your progress:**

```
Cognitive Design Progress:
- [ ] Step 1: Orient to cognitive principles
- [ ] Step 2: Structure design thinking with frameworks
- [ ] Step 3: Apply domain-specific guidance
- [ ] Step 4: Validate against quick reference
```

**Step 1: Orient to cognitive principles**

Start with [Cognitive Foundations](references/cognitive-foundations.md) for deep understanding of WHY designs work (perception, memory, Gestalt principles) OR use [Quick Reference](references/quick-reference.md) for rapid orientation (20 core principles, decision rules). Foundations give you theoretical grounding; Quick Reference gets you started faster.

**Step 2: Structure design thinking with frameworks**

Use [Design Frameworks](references/frameworks.md) to apply systematic approaches: Cognitive Design Pyramid (4-tier quality assessment), Design Feedback Loop (interaction cycles), and Three-Layer Visualization Model (data communication fidelity). These provide repeatable structure for design decisions.

**Step 3: Apply domain-specific guidance**

Choose your domain: [Data Visualization](references/data-visualization.md) for charts/dashboards, [UX Product Design](references/ux-product-design.md) for interfaces/apps, or [Educational Design](references/educational-design.md) for e-learning/training. Apply tailored cognitive principles for your specific context.

**Step 4: Validate against quick reference**

Use [Quick Reference](references/quick-reference.md) to verify your design against the 3-question check (Attention? Memory? Clarity?) and 20 core principles. Confirm your design passes basic cognitive alignment.

**Next steps:** Use `design-evaluation-audit` skill for systematic evaluation, `cognitive-fallacies-guard` to check for misleads.

---

### Quick Validation Workflow

**Use when:** Need rapid go/no-go decision, spot-checking changes, or validating against cognitive basics during active design work

**Time:** 5-10 minutes

**Copy this checklist and track your progress:**

```
Quick Validation Progress:
- [ ] Step 1: Three-question rapid check
- [ ] Step 2: Spot checks if issues found
```

**Step 1: Three-question rapid check**

Use [Quick Reference](references/quick-reference.md) and apply: (1) Attention - "Is it obvious what to look at first?" (visual hierarchy clear, primary elements salient, predictable scanning), (2) Memory - "Is user required to remember anything that could be shown?" (state visible, options presented, fits 4±1 chunks), (3) Clarity - "Can someone unfamiliar understand in 5 seconds?" (purpose graspable, no unnecessary decoration, familiar terminology). If all YES → likely cognitively sound.

**Step 2: Spot checks if issues found**

If any question fails, consult the relevant cognitive foundation: Failed attention? Check hierarchy and visual salience in [Cognitive Foundations](references/cognitive-foundations.md). Failed memory? Check chunking and memory constraints. Failed clarity? Check simplicity principles and labeling guidance.

---

## Path Selection Menu

**Choose your path based on current need:**

### Path 1: Understand Cognitive Foundations

**Choose this when:** You want to learn the core cognitive psychology principles underlying effective design (attention, memory, perception, Gestalt grouping, visual encoding hierarchy).

**What you'll get:** Deep understanding of WHY certain designs work, grounded in research.

**Time:** 20-40 minutes

**→ [Go to Cognitive Foundations resource](references/cognitive-foundations.md)**

---

### Path 2: Apply Design Frameworks

**Choose this when:** You want systematic frameworks to structure your design thinking.

**What you'll get:** Three complementary frameworks:
- **Cognitive Design Pyramid** (4 tiers: Perceptual Efficiency → Cognitive Coherence → Emotional Engagement → Behavioral Alignment)
- **Design Feedback Loop** (Perceive → Interpret → Decide → Act → Learn)
- **Three-Layer Visualization Model** (Data → Visual Encoding → Cognitive Interpretation)

**Time:** 30-45 minutes

**→ [Go to Frameworks resource](references/frameworks.md)**

---

### Path 3: Get Domain-Specific Guidance

**Choose this when:** You're working on a specific type of design and want tailored cognitive principles.

**Choose your domain:**

#### 3a. Data Visualization (Charts, Dashboards, Analytics)

**→ [Go to Data Visualization resource](references/data-visualization.md)**

**Covers:** Chart selection via task-encoding alignment, dashboard hierarchy and grouping, progressive disclosure for exploration, narrative data visualization

---

#### 3b. Product/UX Design (Interfaces, Mobile Apps, Web Applications)

**→ [Go to UX Product Design resource](references/ux-product-design.md)**

**Covers:** Learnability via familiar patterns, task flow efficiency, cognitive load management, onboarding design, error handling

---

#### 3c. Educational Design (E-Learning, Training, Instructional Materials)

**→ [Go to Educational Design resource](references/educational-design.md)**

**Covers:** Multimedia learning principles, dual coding, worked examples, retrieval practice, segmenting, coherence principle

---

### Path 4: Access Quick Reference

**Choose this when:** You need rapid design guidance, core principles summary, or quick validation checks.

**What you'll get:** 20 core principles, 3-question check, common decision rules, design heuristics

**Time:** 5-15 minutes

**→ [Go to Quick Reference resource](references/quick-reference.md)**

---

### Path 5: Explore Source Landscape

**Choose this when:** You want to understand the research traditions and key authors behind cognitive design principles.

**What you'll get:** Key researchers (Tufte, Norman, Ware, Cleveland & McGill, Mayer, Nielsen), their contributions, and when to cite them.

**Time:** 10-20 minutes

**→ [Go to Source Landscape resource](references/source-landscape.md)**

---

### Path 6: Exit

**Choose this when:** You've completed your design work or gathered the information you need.

**Before you exit:**
- Have you achieved your goal for this session?
- Need to evaluate your design? → Use `design-evaluation-audit` skill
- Need to check for misleads? → Use `cognitive-fallacies-guard` skill
- Need to tell a data story? → Use `visual-storytelling-design` skill

---

## Verification

Before handing a design on, run the 3-question check from [Quick Reference](references/quick-reference.md) and record the answers:

1. Attention: is it obvious what to look at first?
2. Memory: is the user asked to remember anything that could be shown?
3. Clarity: can someone unfamiliar understand it in 5 seconds?

Three yes answers clear the design for `design-evaluation-audit`; any no sends you back to the matching foundation section. `assets/evaluation-rubric.json` scores the guidance in this skill itself (completeness, clarity, actionability) and is for maintainers, not for judging a design.

---

## Related Skills

| Skill | Use For |
|---|---|
| `design-evaluation-audit` | Systematic design reviews using cognitive checklists and visualization audits |
| `cognitive-fallacies-guard` | Detecting chartjunk, misleading axes, cognitive biases, data integrity violations |
| `visual-storytelling-design` | Data journalism, presentations, infographics, narrative visualization |
| `information-architecture` | Content organization, navigation design, taxonomy, findability |
| `d3-visualization` | Implementing interactive data visualizations with D3.js |
