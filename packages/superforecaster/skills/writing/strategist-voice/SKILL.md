---
name: strategist-voice
description: Apply the analyst house style to a long-form report.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: writing
    tags: [Writing, House Style, Analyst Report, Citations, Editing]
    related_skills: [slop-detector, readability-check]
---
# Strategist voice

The house style for analyst-grade writing: third-person register with sparing first person, no em dashes, no "not X, not Y, not Z" negation cascades, numbered footnote citations instead of inline source parentheticals, specific opinion-signalling phrases, and topic-forward paragraphs. It is modelled on the voice patterns of Damodaran's Musings on Markets and Thompson's Stratechery. Apply it in the final consolidation step, when working notes become a publishable document; it is not a drafting aid and it does not check readability or slop (see `readability-check` and `slop-detector`).

## When to Use

- Consolidating working notes into a finished long-form strategist, analyst, or forecast report.
- The document must read as written by a senior human analyst rather than an assistant.
- A draft is full of em dashes, negation cascades, inline `(Source: ...)` citations, or `Strategist inference:` prefixes.
- Opinion needs to be signalled with graded conviction rather than hedged or asserted flatly.
- The user asks for the house style, the analyst voice, or a research-note register.

## The two reference voices

The house style synthesises two analyst-blogger voices:

- **Aswath Damodaran** (Musings on Markets): academic-conversational, rigorous frameworks delivered in a personal voice; first-person opinion stated openly; historical or philosophical hooks; data woven into prose without footnote interruption.
- **Ben Thompson** (Stratechery): counterintuitive openings; named frameworks earning their analytical keep; punchy declaratives alternated with subordinate-clause sentences; sources named in prose; opinion signalled through specific phrasing.

Both write at a sentence level that no assistant default produces. The rules below capture what they share. Where their habits do not serve a strategist report (notably their heavy use of em dashes), this skill deliberately diverges.

## Hard rules

The consolidating agent must enforce these. They are non-negotiable. Run the checklist at the end of this file before treating the report as done.

1. **Zero em dashes.** Use a period, semicolon, comma, parenthesis, or rewrite the sentence. Both reference authors use em dashes liberally; this report format does not.
2. **Zero "not X, not Y, not Z" negation cascades.** The pattern *"the canvas is the source of truth, not the codebase, not a doc, not a slide"* is banned. Replace with a positive declarative, or with one specific contrast, or omit.
3. **Zero `Strategist inference:` prefixes.** Signal synthesis through phrasing (see "Opinion signalling" below).
4. **Footnoted citations only.** Use `claim text.[^7]` in the body with `[^7]: Source, URL` in a bibliography section. Never inline `[Source: Org, URL]` or `(Source: Org, URL)`.
5. **No "It's worth noting that..." hollow openings.** Either state the thing directly or omit. Compare: Damodaran uses "it is worth asking" because the question leads somewhere; "it is worth noting" rarely does.
6. **No tl;dr-style closers.** No "In conclusion," "Ultimately," "To summarize." The verdict section is the conclusion; the rest of the report should not summarise itself in passing.
7. **Bulleted lists only where the structure earns them.** Strategic bet lists, surface cards, metric lists, and the bibliography are correct uses. A list as a substitute for an argument-in-prose paragraph is incorrect.
8. **No "X is doing Y because Z" as a primary sentence shape repeated across paragraphs.** It reads as machine output. Vary.
9. **No undefined strategy jargon.** Terms like *the wedge*, *flywheel*, *TAM*, *NDR*, *aggregation theory*, *platform-shaped*, *land-and-expand*, *moat*, *take rate*, *attach rate* must be defined on first appearance, or rewritten away. Define inline (a brief parenthetical, an appositive phrase, or a setup sentence immediately before the term). If defining the term breaks the prose flow, restructure the sentence to avoid the term entirely. The reader is a smart generalist, not a strategy consultant. A term used twice without ever being defined is the single clearest signal that the writer has copied a register rather than thought through the argument.
10. **No abstract X-shaped / Y-shaped labels doing analytical work.** Phrases like *"the vision is platform-shaped, not feature-shaped"* sound analytical but explain nothing. Replace with the concrete description the label was standing in for. Example: *"the credible vision at this stage is a base layer that other products build on, not a single feature."*

## Opinion signalling

Replace `Strategist inference:` with specific phrasing. The strength scale runs from tentative to high conviction:

- **Tentative**: "appears to," "the evidence suggests," "perhaps," "arguably"
- **Reasoned**: "the more likely reading is," "this analyst's reading is," "in our reading," "the more interesting question is"
- **Confident**: "without question," "the evidence is clear," "this is the central bet," "the reasons are simple"
- **Provocative**: "it is worth asking," "the bet is wrong," "the more obvious explanation"

Use first person ("we," "this analyst's reading," "in our reading") sparingly. Once or twice per long section is correct; once per paragraph is wrong. Reserve it for the genuine judgment calls.

## Paragraph and sentence structure

- **Topic-forward.** Lead the paragraph with the claim. Then elaborate, qualify, support.
- **Vary sentence length deliberately.** Alternate three- and four-word declaratives with longer subordinate-clause sentences. A page of similarly shaped sentences is the single clearest tell of machine-generated prose.
- **Short paragraphs.** Three or four sentences is plenty. Long paragraphs are usually buried arguments.

## Opening paragraphs

Use one of these three patterns. None of them define the company.

1. **Counterintuitive frame.** Name a tension or paradox, then pivot to the subject. Thompson's "Tim Cook's Impeccable Timing" opens by observing that CEO eulogies typically occur at retirement rather than death.
2. **Historical or philosophical comparison.** Set up a broad observation, then place the subject inside it. Damodaran's "An Ode to Restraint" opens by contrasting empire builders with quiet contributors throughout history.
3. **Specific data point with a take on it.** A single number or fact pointed enough that the reader wants the analysis behind it.

Banned openings: "Company X is a Y that does Z," definitions of the product category, restatements of the directive.

## Citation form

Numbered footnotes. In the body:

> Figma's Q4 2025 revenue grew 40% year on year.[^7]

In the bibliography section at the end of the report, grouped by source type:

```
**Primary company material**
[^1]: Figma — How Figma's multiplayer technology works — https://www.figma.com/blog/...
[^7]: Figma Investor Relations — Q4 2025 results — https://investor.figma.com/...

**Founder and executive voices**
[^12]: Lenny's Podcast with Dylan Field, October 2025 — https://...

**Engineering and architecture material**
[^18]: ...

**Secondary analysis**
[^24]: ...
```

Footnote markers go after the sentence punctuation. Never two markers on the same fact. Never a parenthetical citation inside a sentence. The dashes in bibliography lines are the one place the em dash is tolerated; they are not prose.

## Examples

Load [style-examples.md](references/style-examples.md) with `skill_view("strategist-voice", file_path="references/style-examples.md")` for annotated good-and-bad rewrites of opening paragraphs, opinion-signalled sentences, negation-cascade fixes, citation forms, and synthesis statements.

## Final-pass checklist

Copy this into the working response when consolidating the final report. Tick each item before declaring the report finished.

```
Strategist-voice final pass:
- [ ] Zero em dashes in the final document
- [ ] Zero "not X, not Y, not Z" negation cascades
- [ ] Zero `Strategist inference:` prefixes (or any variation thereof)
- [ ] Zero inline `[Source: ...]` or `(Source: ...)` citations
- [ ] Zero "It's worth noting" hollow openings
- [ ] Zero "In conclusion / Ultimately / To summarize" closers
- [ ] The opening paragraph uses one of the three permitted patterns
- [ ] At least three opinion-signalling phrases (from the list above) appear in the synthesis section
- [ ] Sentence length varies visibly within paragraphs
- [ ] First person ("we," "this analyst's reading") used at most twice per major section
- [ ] Bibliography is grouped by source type and uses numbered footnote anchors that match in-text markers
- [ ] Every strategy-jargon term ("wedge", "flywheel", "TAM", "NDR", "moat", "attach rate", "X-shaped" labels, etc.) is either defined on first use or rewritten away
- [ ] No abstract X-shaped / Y-shaped label is doing the analytical work that a concrete description should be doing
```

If any box cannot be ticked, return to the draft and fix before producing the final markdown.

## Verification

Run `search_files` over the finished document for the em dash character, `Strategist inference`, `[Source:`, `(Source:`, `It's worth noting`, `In conclusion`, `Ultimately`, and `To summarize`. Zero hits outside the bibliography is the bar. Then hand the document to `slop-detector` and `readability-check`; this skill's pass is complete only when those two also pass.
