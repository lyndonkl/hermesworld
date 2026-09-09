---
name: reader-first-prose
description: Rewrite prose so a first-time reader can follow every line.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: writing
    tags: [Plain Language, Clarity, Editing, First-Time Reader, Honesty]
    related_skills: [term-interrogation, slop-detector, readability-check]
---
# Reader-First Prose

Rewrites expository prose for a reader meeting the subject for the first time, not an insider who
already shares the writer's knowledge. It enforces introduce-before-use, grounds or cuts every
metaphor in the same breath it appears, converts compressed or nominalized logic into a plain
if-then, and removes the two loudest machine tells: the em dash and the terse two-beat antithesis
("X. Not Y."). It carries an honesty pass so the prose never out-claims its evidence. It does not
simplify the argument, and it does not recurse into explanations of explanations; that is
`term-interrogation`.

## When to Use

- A draft assumes knowledge the reader lacks, or name-drops terms before defining them.
- A draft reads as insider or "clever", or leans on unexplained metaphor.
- A draft sounds AI-written: em dashes, clipped "X. Not Y." sentences, rhythm doing the work of
  explanation.
- As the standing style lens on any report written for a non-expert, and as an explicit pass
  before `term-interrogation`.
- The user mentions first-time reader, plain language, define before use, sounds like AI, em
  dash, too clever, or jargon.

**Related skills in this package:** this runs at the sentence layer. Hand the recursive
explaining of terms to `term-interrogation`, other AI signatures to `slop-detector`, and scoring
to `readability-check`. Altitude problems (a passage abstract all the way through), detailed
number handling and evidence audits have dedicated skills elsewhere that are not bundled here;
apply the honesty rules below directly when you meet them.

## The stance

One question governs every edit: **who does this sentence think it is talking to?**

Two stances produce two drafts of the same fact.

- **The insider draft** is written for a reader who already knows the world. It moves fast,
  gestures, names things it never defined, and lets rhythm carry meaning. It reads as clever. It
  sounds like it already knows the answer. This is the default a language model reaches for,
  because it is trained on finished, insider prose.
- **The reader-first draft** is written for a sharp person meeting the subject for the first
  time. Not a less capable reader; just one who was not already in the room. It introduces before
  it leans, grounds before it flies, and states plainly what the insider draft compresses.

This skill converts the first into the second. Plainness here is not simplicity of thought. It is
respect for the reader and for the evidence.

## Clarity rules

Run these in order over the draft.

1. **Introduce before use.** Every entity, term, acronym and proper noun is defined or placed on
   first mention, before any sentence depends on the reader knowing it. Who a party is before its
   role; what a device is before its result; that an acronym expands before it recurs. Test: read
   each sentence as if the earlier ones taught you nothing about that noun. If a noun arrives
   unexplained, move its introduction earlier.
2. **Order for a newcomer.** Facts arrive in the order a first-time reader needs them, not the
   order the source or the writer discovered them. Actor before action, cause before consequence,
   definition before use.
3. **Ground the metaphor or cut it.** A figure of speech is allowed only if it is cashed out in
   the same breath ("the ruler, the tool used to measure the audience"). An ungrounded metaphor
   carrying real weight ("the hands took a cut", "the plates stack up") is decoration the reader
   cannot spend. Replace it with the literal thing.
4. **Plain over clever.** Rewrite compressed or nominalized logic into a plain if-then or
   cause-and-effect a reader follows in one pass. A clear sentence beats a writerly one. A line
   that works only because the reader already agrees is performing, not explaining.

## Honesty rules

Clear prose can still quietly over-claim. Guard the edges.

1. **Fact vs reading.** State as fact only what the source supports. When a sentence is your
   interpretation, mark it as one ("read this way...", "one reading is...") or move it into an
   explicitly flagged aside.
2. **No unstated mechanism.** Do not describe how something works if the source never described
   it. If the source does describe it, show it and cite it. To add it, source it first.
3. **Numbers exact.** Every figure matches the source; direction before magnitude.

## The two tics to kill

These are the loudest signals that a machine, not a person, arranged the sentence.

- **The em dash (—).** Remove every one. Use a semicolon for a clause join, a colon or comma for
  an aside or a definition, a short en dash (–) only for a true parenthetical range. Often a
  period is better than all of them.
- **The terse two-beat antithesis.** The clipped "X. Not Y." shape ("Same method, different
  number." / "The audience did not shrink."). It feels punchy and reads as generated. Say the
  thing plainly, in one sentence, with the concrete detail restored.

## Procedure: the per-sentence pass

For each sentence, in order:

- [ ] Is every noun known to a first-time reader here? If not, introduce it earlier.
- [ ] Is this a plain statement, or a performance? If rhythm is doing the work, rewrite it
      plainly.
- [ ] Any metaphor I have not paid for in the same breath?
- [ ] Is this a fact the source supports, or my reading of it? Mark the reading.
- [ ] Any em dash, or any "X. Not Y." antithesis? Remove it.
- [ ] Are the numbers exactly as sourced?

## Worked examples

Each pair is an insider draft rewritten reader-first. The topic is incidental; the moves
generalize to any expository writing.

**1. Introduce before use.**
- Before: "The price of the middleman's work was a published figure."
- After: "The agencies were the middlemen: they bought the space and made the ads. What they
  charged for that work, a 15% commission, was published."
- Fix: the reader met "the middleman" before being told who it was. Name it first.

**2. Ground the metaphor.**
- Before: "Behind the 15% stood a stack of hands, and most of them were not public."
- After: "Behind the 15% were several other parties, each taking a cut of the same dollar, and
  most of those cuts were never public."
- Fix: "hands" was decoration. Replace with the literal parties and cuts.

**3. Plain over clever.**
- Before: "A market where the seller simply inflates its own count does not predict a seller
  adopting a ruler that shrinks its numbers."
- After: "If sellers always just inflated the count, they would not adopt a standard that shrank
  their own numbers; yet here they did."
- Fix: an abstract, nominalized claim becomes a plain if-then a reader follows in one pass.

**4. Kill the antithesis and the em dash.**
- Before: "No viewer got up off the couch. The audience did not shrink. The instrument changed —
  and the number dropped."
- After: "Nothing had happened to the audience; the same people sat on the same couches. What
  changed was the way they were counted."
- Fix: the clipped two-beat pattern and the em dash both go; the concrete image stays, stated
  plainly.

**5. Fact vs reading (honesty).**
- Before: "The more honest count cut the sellers' own figures, which is why the 'sellers rig
  everything' story fails."
- After (in a flagged aside): "One reading: the newer count is the more honest one, and that is
  what makes this strange. If sellers always inflated the count, they would not adopt a standard
  that shrank their numbers."
- Fix: the interpretive leap is marked as a reading, not stated as established fact.

## Guardrails

- **Do not flatten voice into blandness.** Reader-first is not tone-deaf or listy. Keep the
  writer's rhythm and warmth; remove only what a newcomer cannot follow or what over-claims.
- **Simplify the demands, not the content.** The facts, the argument and the precision stay.
  What drops is the assumed prior knowledge and the unearned compression.
- **Do not delete a hedge that carries real uncertainty** to make a sentence cleaner. "Appears
  to" and "on the available evidence" are load-bearing when the evidence is thin.
- **Preserve every number and named source.** This skill rewrites how a claim reads, never what
  it asserts.
- **Introduce once.** Define a term at first use; do not re-explain it on every mention.

## Verification

- Use `search_files` on the finished file for the em dash character; the count must be zero.
- Read the first paragraph of each section as a stranger: no noun arrives before it is placed.
- Every interpretive sentence is marked as a reading or sits in a flagged aside.
- Every number matches its source exactly.
- Then hand the document to `term-interrogation`, and score it last with `readability-check`.
