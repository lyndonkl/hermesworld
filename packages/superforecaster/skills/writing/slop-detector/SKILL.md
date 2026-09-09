---
name: slop-detector
description: Flag the ten signatures of AI-written explainer prose.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Writing, AI Slop, Editing, Prose Quality]
    related_skills: [readability-check]
---
# Slop Detector

Scans a draft for ten fixed signatures of AI-generated explainer slop: meta-framing openers ("In this post"), list-carried argument, nominalization clusters, generic examples with no first-person texture, prompt-residue phrases ("Let's break this down"), buzzword stuffing, outline-shaped paragraphs, hedge clusters, and flattened uncertainty. Each signature has a concrete detection rule and is reported as `clean` or `flagged` with the offending span quoted. It does not measure sentence-level readability; that is `readability-check`'s job.

## When to Use

- A draft "feels generic" even after a voice pass has been applied.
- Reviewing any long-form output (report, essay, memo, forecast write-up) before it is delivered.
- The user mentions slop, AI-written, generic, template, meta-framing, zombie nouns, prompt residue, or outline-shaped prose.
- A document is heavy on "First / Second / Third" lists, "To summarize" closers, or "a company might" examples.

**Related skills:** run this before `readability-check`; slop is a content problem, readability a structural one, and fixing slop often changes the sentences the readability pass would have scored.

## The 10 signatures

Fixed list. Each is either `clean` or `flagged` with the offending span.

| # | Signature | Detection |
|---|---|---|
| S1 | Meta-framing opener | First paragraph contains `In this post`, `This article`, `We will explore`, `Let's dive into`, `Today we'll look at` |
| S2 | List-carrying-argument | Any bulleted list where the argument collapses if the bullets are removed. Test: does the prose still stand without the list? |
| S3 | Zombie nouns (Sword) | >3 nominalizations per 100 words (suffixes -ation, -ity, -ment, -ence on abstract nouns) |
| S4 | Generic examples | "a company" / "a model" / "a user" with no specific name, scale, or dataset |
| S5 | No first person | Zero `I`, `my`, `we-as-me` in a >800-word reflective essay |
| S6 | Prompt residue | `Let's break this down`, `To summarize`, `In conclusion`, `Key takeaways`, `Let me explain` |
| S7 | Outline-shaped paragraphs | >60% of paragraphs follow the same syntactic shape: topic, three supporting sentences, transition |
| S8 | Hedge cluster | >=2 epistemic-weakness hedges within 50 words (`it could be argued`, `some might say`, `perhaps`, `arguably`, `it seems that`, `to some extent`) |
| S9 | Buzzword stuffing | >=3 terms from {game-changer, paradigm shift, under the hood, delve, unpack, dive into} in a single draft |
| S10 | Flattened uncertainty | A small-N or data-quality caveat that appears in the author's working notes but was removed from the submitted draft (requires the notes; otherwise skip this signature) |

## Procedure

```
Slop scan draft D:
- [ ] Step 1: For each signature, run the detection rule
- [ ] Step 2: Mark each signature clean | flagged (with quote)
- [ ] Step 3: Tier-1 signatures: S1, S2, S6 (generic framing + prompt residue)
- [ ] Step 4: Tier-2 signatures: S3, S4, S5, S7, S8, S9
- [ ] Step 5: Emit the slop-signatures subsection with each labelled clean/flagged
```

### S3 nominalization scoring

Count suffix hits (`-ation`, `-ity`, `-ment`, `-ence`, `-ness`, `-ance`) on abstract nouns per 100 words. >3 = flag. Example: "provides analysis of" is nominalized; "analyzes" is active.

### S4 generic-example rule

Flag an example if it uses only generic pronouns or nouns without a specific anchor:
- "A company might use this": flag.
- "At Google in 2024, Chen et al. used this": clean.

### S7 outline-shape rule

Parse paragraphs; count those with the shape:
- Sentence 1: topic statement
- Sentences 2-4: three supporting sentences
- Last sentence: transition

>60% of paragraphs following this shape means the draft reads like an outline expanded by a model.

### S8 hedge-cluster rule

Count epistemic-weakness hedges (phrases that weaken a claim without adding information). Two or more within 50 words is a cluster. A single precise hedge ("the sample is 12 firms, so treat the rate as indicative") is not a hedge for this purpose; it is a caveat and belongs in the text.

## Worked example

**Draft fragment**:
> In this post, we'll explore why RAG beats fine-tuning.
>
> First, let's define RAG. It's a technique where models retrieve documents before generating. A company might use RAG for their customer service chatbot.
>
> Second, fine-tuning involves training. A team might fine-tune to adapt style.
>
> Third, RAG has benefits. Fine-tuning has drawbacks. It could be argued that hybrid works.
>
> To summarize, both approaches have merit.

**Detections**:
- S1: flagged ("In this post, we'll explore").
- S2: flagged (argument carried by the "First / Second / Third" list-in-prose).
- S3: zombie-noun check: "technique", "documents", "benefits", "drawbacks"; borderline, not flagged yet.
- S4: flagged ("A company might use RAG", "a team might fine-tune"); no specifics.
- S5: clean (has "we").
- S6: flagged ("To summarize").
- S7: flagged (each paragraph: topic, supporting, transition).
- S8: weakness hedges: "It could be argued"; just one, not a cluster (yet).
- S9: buzzwords: "explore" is close; not flagged (one term).
- S10: skipped (no notes).

**Output**: 5 signatures flagged (S1, S2, S4, S6, S7). Tier-1: S1, S2, S6, so 3 tier-1 slop violations.

## Output format

```
Slop signatures:
- S1 meta-framing opener: flagged - "In this post, we'll explore"
- S2 list-carrying-argument: flagged - "First ... Second ... Third"
- S3 zombie nouns: clean (2.1 per 100 words)
- ...
Tier-1 violations: 3 (S1, S2, S6). Tier-2 violations: 2 (S4, S7).
```

## Guardrails

1. Each signature has a concrete detection rule. No "feels like slop."
2. Quote the offending span. Do not just say "S1 triggered"; quote the opener.
3. Signatures are additive, not exclusive. A draft can trip 8 signatures and still be revisable; the calling workflow decides the no-go threshold (a common rule: any tier-1 hit blocks delivery).
4. S10 requires the author's working notes; skip quietly if absent.
5. If a separate hedge-detection pass has already run, take its cluster count as the S8 input rather than scanning twice.
6. S5 (no first person) applies to reflective essays only. How-to and methodology documents may legitimately lack "I".

## Quick Reference

- 10 fixed signatures, deterministic detection.
- Tier-1: S1, S2, S6. Tier-2: the rest.
- Output is a per-signature clean/flagged list with quotes, then the tier counts.

## Verification

Run the scan on the worked example above: it must reproduce exactly five flags (S1, S2, S4, S6, S7) with the quoted spans. A scan that flags fewer is skipping rules; one that flags S3 or S8 on this fragment is not applying the thresholds.
