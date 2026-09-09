---
name: communication-storytelling
description: Shape findings into a narrative built for a named audience.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: writing
    tags: [Storytelling, Audience Adaptation, Narrative Structure, Executive Communication, Persuasion]
    related_skills: [reader-first-prose, layered-reasoning, slop-detector]
---
# Communication Storytelling

Transforms analysis, data, and complex information into a clear, persuasive narrative tailored to
a specific audience: executives, customers, investors, or non-technical stakeholders. It supplies
story structures (Hero's Journey, Problem-Solution-Benefit, Before-After-Bridge,
Situation-Complication-Resolution) and audience adaptation techniques, and it ends with a
headline, key points, proof, and a call to action. It does not do the underlying analysis, and it
does not make a weak finding sound strong.

## When to Use

- Presenting findings, analysis, or data to executives, customers, investors, or non-technical
  stakeholders.
- Explaining a technical concept to a non-technical audience.
- Writing an announcement, update, proposal, board memo, or postmortem that has to land on the
  first read.
- Keeping a long analysis's verdict from getting lost in its own evidence.
- The user says "write this for", "explain to", "present findings", "make this compelling", or
  "audience is".

## Overview

This skill crafts the story with a fixed frame: (1) Headline, a single clear statement capturing
the essence, (2) Key Points, 3-5 supporting ideas with logical flow, (3) Proof, the evidence, data
and examples that substantiate them, (4) Call-to-Action, what the audience should think, feel, or
do.

**Quick example:**

**Bad (data dump):**
"Our Q2 revenue was $2.3M, up from $1.8M in Q1. Customer count went from 450 to 520. Churn
decreased from 5% to 3.2%. NPS improved from 42 to 58. We launched 3 new features..."

**Good (storytelling):**
"We've reached product-market fit. Three signals prove it: (1) Revenue grew 28% while sales
capacity stayed flat: customers are pulling product from us, not the other way around. (2) Churn
dropped 36% as we focused on power users, with our top segment now at 1% monthly churn. (3) NPS
jumped 16 points to 58, with customers specifically praising the three features we bet on.
Recommendation: double down on the power user segment with a premium tier."

## Procedure

Copy this checklist and track your progress:

```
Communication Storytelling Progress:
- [ ] Step 1: Gather inputs and clarify audience
- [ ] Step 2: Choose appropriate narrative structure
- [ ] Step 3: Craft the narrative
- [ ] Step 4: Validate quality and clarity
- [ ] Step 5: Deliver and adapt
```

**Step 1: Gather inputs and clarify the audience**

Pin down the message (the analysis, data, or information to communicate), the audience (who will
receive this), the purpose (inform, persuade, inspire, build trust), the context (situation,
stakes, constraints), and the tone (formal, casual, urgent, celebratory). If any of these is
genuinely unknown, ask with `clarify`; otherwise infer it from the material and say what you
assumed. Understanding the audience deeply is critical: their expertise level, concerns, decision
authority, and time constraints shape everything. See
[templates/template.md](templates/template.md) for the input questions.

**Step 2: Choose the narrative structure**

For standard communications (announcements, updates, presentations) → use the
[templates/template.md](templates/template.md) quick template. For complex multi-stakeholder
communications requiring different versions → study
[references/methodology.md](references/methodology.md) for audience segmentation and narrative
adaptation techniques. To see what good looks like → read
[references/example-product-launch-announcement.md](references/example-product-launch-announcement.md)
and
[references/example-technical-incident-postmortem.md](references/example-technical-incident-postmortem.md).

**Step 3: Craft the narrative**

Write `communication-storytelling.md` with `write_file`: (1) a headline that captures the essence
in one sentence, (2) 3-5 key points arranged in logical flow (chronological, problem-solution,
importance-ranked), (3) concrete proof for each point (data, examples, quotes, stories), (4) a
clear call-to-action stating what the audience should do next. Use storytelling techniques:
specificity over generality, show don't tell, human stories over abstract concepts,
tension/resolution arcs. See [Story Structure](#story-structure) for narrative patterns.

**Step 4: Validate quality and clarity**

Self-assess using
[assets/evaluators/rubric_communication_storytelling.json](assets/evaluators/rubric_communication_storytelling.json).
Check: the headline is clear, the key points are distinct and well-supported, the proof is
concrete and relevant, the flow is logical, the tone matches the audience, jargon is appropriate
for the expertise level, the call-to-action is clear and achievable, the length matches the time
constraints. Read it aloud to test clarity. Test with the "so what?" question: does each point
answer why the audience should care? Minimum standard: average score at least 3.5 before
delivering.

**Step 5: Deliver and adapt**

Present the completed `communication-storytelling.md`. Highlight how the narrative addresses the
audience's key concerns. Note the storytelling techniques used (data humanized,
tension-resolution, specificity). If the user has feedback or needs adaptations for different
audiences, use [references/methodology.md](references/methodology.md) for the multi-version
strategy.

## Story Structure

### The Hero's Journey (Transformation Story)

**When to use:** Major changes, pivots, overcoming challenges

**Structure:**
1. **Status Quo** - Where we were (comfort, but a problem lurking)
2. **Call to Adventure** - Why we had to change (the problem emerges)
3. **Trials** - What we tried, what we learned (struggle builds credibility)
4. **Victory** - What worked (resolution)
5. **Return with Knowledge** - What we do now (new normal, lessons learned)

**Example:** "We were growing 20% YoY, but churning 10% monthly, which was unsustainable. Data
showed we were solving the wrong problem for the wrong users. We tested 5 hypotheses over 3
months, failing at 4. The one that worked: focusing on power users willing to pay 5x more. Churn
dropped to 2%, growth hit 40% YoY. Now we're betting everything on the premium tier."

### Problem-Solution-Benefit (Decision Story)

**When to use:** Recommendations, proposals, project updates

**Structure:**
1. **Problem** - Clearly defined issue with stakes (what happens if unaddressed)
2. **Solution** - Your recommendation with rationale (why this, not alternatives)
3. **Benefit** - Tangible outcomes (quantified impact)

**Example:** "We lose 30% of signups at checkout, $2M ARR left on the table. Root cause: we ask
for a credit card before users see value. Proposal: 14-day trial, no card required, with
onboarding emails showing ROI. Comparable companies saw a 60% conversion lift. Expected impact:
+$1.2M ARR with a 4-week implementation."

### Before-After-Bridge (Contrast Story)

**When to use:** Product launches, feature announcements, process improvements

**Structure:**
1. **Before** - Current painful state (the audience's lived experience)
2. **After** - Improved future state (what becomes possible)
3. **Bridge** - How to get there (your solution)

**Example:** "Before: the sales team spends 10 hours a week manually exporting data, cleaning it
in spreadsheets, and pasting it into slide decks; error-prone and soul-crushing. After: one-click
report generation with live data, auto-refreshing dashboards, 30 minutes a week. Bridge: we built
sales analytics v2.0, launching Monday with training sessions."

### Situation-Complication-Resolution (Executive Story)

**When to use:** Executive communications, board updates, investor relations

**Structure:**
1. **Situation** - Context and baseline (set the stage)
2. **Complication** - What changed or what is at stake (creates tension)
3. **Resolution** - Your path forward (releases tension)

**Example:** "Situation: we budgeted $5M for customer acquisition in 2024. Complication: iOS 17
privacy changes killed our primary ad channel, a 50% drop in conversion overnight. Resolution:
shifting $2M to content marketing (3-month ROI), $1M to partnerships (immediate distribution),
keeping $2M in ads for testing new channels. Risk: content takes time to scale, but partnerships
derisk the timeline."

## Common Patterns

**Data-Heavy Communications:**
- Lead with the insight, not the data
- One number per point (too many = confusion)
- Humanize data with stories: "42% churn" → "We lose 12 customers every week; that is Sarah's
  entire cohort from January"
- Use comparisons for context: "200ms latency" → "2x slower than competitors, 3x slower than last
  year"

**Technical → Non-Technical:**
- Translate jargon: "distributed consensus algorithm" → "how servers agree on truth without a
  central authority"
- Use analogies from the audience's domain: "Kubernetes is like airport air traffic control for
  containers"
- Focus on business impact, not technical implementation
- Anticipate "why does this matter?" and answer it explicitly

**Change Management:**
- Acknowledge the loss or pain (do not gloss over difficulty)
- Paint a credible future state (hope, not just fear)
- Show the path from here to there (make it concrete)
- Address "what about me?" early (personal impact)

**Crisis Communications:**
- Lead with facts (what happened, when, impact)
- Take accountability (no blame-shifting or weasel words)
- State what you are doing (concrete actions with a timeline)
- Commit to transparency (when they will hear next)

## Guardrails

**Do:**
- Test headline clarity: can someone understand the essence in 10 seconds?
- Use concrete specifics over vague generalities
- Match the sophistication level to the audience (avoid talking up or down)
- Front-load conclusions (executives decide in the first 30 seconds)
- Show your work for major claims (data sources, assumptions)
- Acknowledge limitations and risks (builds credibility)

**Don't:**
- Bury the lede (the most important thing must be first)
- Use jargon the audience does not know (or define it)
- Make claims without proof (erodes trust)
- Assume the audience cares; make them care by showing stakes
- Write walls of text (use bullets, headers, white space)
- Lie or mislead (including by omission)

## Pitfalls

- The draft is mostly bullet points with no narrative arc
- You cannot summarize the message in one sentence
- Passive voice used to avoid accountability ("mistakes were made")
- Data included that does not support the points
- A vague call-to-action ("be better", "work harder")
- A verdict stated more confidently than the evidence behind it allows; storytelling arranges
  the evidence, it does not upgrade it

## Quick Reference

**Bundled files:**
- **[templates/template.md](templates/template.md)** - Quick-start template with headline, key
  points, proof structure
- **[references/methodology.md](references/methodology.md)** - Advanced techniques for
  multi-stakeholder communications, narrative frameworks, persuasion principles
- **[references/example-product-launch-announcement.md](references/example-product-launch-announcement.md)**
  and
  **[references/example-technical-incident-postmortem.md](references/example-technical-incident-postmortem.md)**
  - Worked examples showing different story structures and audiences
- **[assets/evaluators/rubric_communication_storytelling.json](assets/evaluators/rubric_communication_storytelling.json)**
  - 10-criteria quality rubric with audience-based thresholds

**Which file when:**
- Standard communication → start with the template
- Multiple audiences for the same message → methodology, multi-version strategy
- Complex persuasion (board pitch, investor update) → methodology, persuasion frameworks
- Unsure what good looks like → the two worked examples
- Before delivering → validate with the rubric (score at least 3.5 required)

## Verification

- The headline states the conclusion in one sentence and survives the 10-second test.
- Every key point answers "so what?" for this audience, and every point has proof attached.
- The call-to-action names a concrete next step.
- Rubric average is at least 3.5 before delivering.
