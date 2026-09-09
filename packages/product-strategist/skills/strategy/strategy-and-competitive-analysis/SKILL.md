---
name: strategy-and-competitive-analysis
description: Pick strategy frameworks that fit a competitive question.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: strategy
    tags: [Strategy, Competitive Analysis, Porter Five Forces, Positioning, Moats]
    related_skills: [business-narrative-builder, systems-thinking-leverage, layered-reasoning, strategy-concept-notes]
---
# Strategy & Competitive Analysis

Develops business strategy grounded in competitive and market analysis, using established
frameworks (Good Strategy kernel, Porter's 5 Forces, SWOT, Blue Ocean, Playing to Win, Value Chain
Analysis, BCG Matrix) and choosing the two or three that fit the question. It produces a diagnosis,
a guiding policy and coherent actions with evidence behind each. It does not produce a textbook
tour of every framework; a framework that does not sharpen the answer is left out, and the
omission is named.

## When to Use

- Developing strategy for market entry, a product launch, expansion, M&A, or a turnaround.
- Conducting competitive analysis or profiling specific competitors.
- Making a strategic decision such as build vs buy, pricing, or positioning.
- Planning strategic initiatives for a year or a product line.
- Reverse-engineering where a company competes and how it wins, from public material.
- The user mentions strategy, competitive analysis, Porter's 5 Forces, SWOT, market positioning,
  or strategic frameworks.

**Core approach, the Good Strategy Kernel** (Rumelt): Diagnosis (what is the challenge) → Guiding
Policy (overall approach) → Coherent Actions (specific coordinated steps).

**Example**: SaaS startup entering a crowded market → **Diagnosis**: commoditized features, price
competition, high CAC. **Guiding Policy**: vertical specialization (healthcare) + product-led
growth. **Coherent Actions**: build HIPAA compliance, create compliance templates, offer a free
tier, invest in SEO for "healthcare SaaS".

## Procedure

Copy this checklist and track your progress:

```
Strategy & Competitive Analysis Progress:
- [ ] Step 1: Frame strategic question and gather context
- [ ] Step 2: Choose framework(s) based on question type
- [ ] Step 3: Conduct analysis using chosen framework(s)
- [ ] Step 4: Synthesize insights and formulate strategy
- [ ] Step 5: Validate and create action plan
```

**Step 1: Frame the strategic question**

Clarify the strategic question, business context (industry, stage, constraints), competitive
landscape, and success criteria. If the question is genuinely ambiguous, ask with `clarify`. See
[Common Patterns](#common-patterns) for typical question types.

**Step 2: Choose framework(s)**

For industry or competitive structure → Porter's 5 Forces. For positioning → Blue Ocean Strategy
Canvas or Value Chain Analysis. For overall strategy → Good Strategy kernel. For multiple options →
SWOT per option. See [Strategic Frameworks Overview](#strategic-frameworks-overview) and
[references/methodology.md](references/methodology.md) for selection guidance. Name the frameworks
you rejected and why.

**Step 3: Conduct the analysis**

For a straightforward competitive analysis → use [templates/template.md](templates/template.md).
For complex multi-framework strategy → study [references/methodology.md](references/methodology.md)
for the integrated approach. Gather evidence with `web_search` and `web_extract` (competitor
research, market analysis, customer insight), apply the framework systematically, and document
findings with sources.

**Step 4: Synthesize insights**

Apply the Good Strategy kernel: **Diagnosis** (the core challenge the analysis exposed), **Guiding
Policy** (the overall approach to it), **Coherent Actions** (3-5 specific coordinated steps). Check
coherence: actions reinforce each other, support the guiding policy, and address the diagnosis.

**Step 5: Validate and write the action plan**

Self-assess against
[assets/evaluators/rubric_strategy_and_competitive_analysis.json](assets/evaluators/rubric_strategy_and_competitive_analysis.json).
Check: diagnosis grounded in evidence, guiding policy addresses the root challenge, actions
coherent and specific, competitive positioning clear, assumptions explicit, risks identified. Write
`strategy-and-competitive-analysis.md` with `write_file`: strategy summary, supporting analysis,
action plan with owners and timelines.

## Strategic Frameworks Overview

| Framework | Use When | Key Output |
|-----------|----------|------------|
| **Good Strategy Kernel** | Overall strategy formulation | Diagnosis + Guiding Policy + Coherent Actions |
| **Porter's 5 Forces** | Assess industry attractiveness, competitive intensity | Industry structure analysis, profit potential |
| **SWOT Analysis** | Evaluate internal/external factors, compare options | Strengths, Weaknesses, Opportunities, Threats |
| **Blue Ocean Strategy** | Find uncontested market space, redefine competition | Strategy canvas, value innovation |
| **Playing to Win** | Define strategic choices explicitly | Where to play (markets/segments), How to win (advantage) |
| **Value Chain Analysis** | Identify cost advantages, differentiation opportunities | Value activities, cost drivers, linkages |
| **BCG Matrix** | Manage product portfolio | Stars, Cash Cows, Dogs, Question Marks |
| **Competitive Profiling** | Understand specific competitors deeply | Competitor SWOT, positioning, strategy inference |

**Framework Selection:**
- **Single product launch** → Blue Ocean Strategy Canvas + Competitive Profiling
- **Market entry decision** → Porter's 5 Forces + Playing to Win
- **Annual strategic planning** → Good Strategy Kernel + SWOT
- **Turnaround/crisis** → Good Strategy Kernel (diagnosis critical)
- **Portfolio management** → BCG Matrix + Resource allocation
- **Outside-in read of a real company** → Playing to Win + Competitive Profiling, with Porter's 5
  Forces only where industry structure is the live question

See [references/methodology.md](references/methodology.md) for detailed framework application
guidance.

## Competitive Analysis Overview

**Competitor Profiling:**
- **Identify competitors**: Direct (same solution), Indirect (different solution, same job),
  Potential (adjacent markets, new entrants)
- **Profile each**: Product/features, Pricing, Target customers, Positioning/messaging,
  Strengths/weaknesses, Strategy inference, Financial health, Recent moves
- **Analyze**: SWOT per competitor, Competitive positioning map (2x2: price vs features, etc.),
  Share of wallet, Win/loss patterns

**Porter's 5 Forces:**
1. **Competitive Rivalry**: Number of competitors, market growth rate, differentiation, switching
   costs, exit barriers
2. **Threat of New Entrants**: Barriers to entry (capital, technology, brand, regulation, network
   effects)
3. **Threat of Substitutes**: Alternative solutions, price-performance trade-offs, switching costs
4. **Bargaining Power of Buyers**: Concentration, price sensitivity, switching costs, backward
   integration threat
5. **Bargaining Power of Suppliers**: Concentration, uniqueness, switching costs, forward
   integration threat

**Output**: Industry attractiveness (high/medium/low profit potential), key competitive dynamics,
strategic implications.

**Competitive Moats** (sustainable advantages):
- **Network effects**: Value increases with more users (platforms, marketplaces)
- **Switching costs**: High cost to change providers (data lock-in, integration, learning curve)
- **Brand**: Strong brand recognition and loyalty
- **Cost advantages**: Scale economies, proprietary technology, favorable access to resources
- **Regulatory**: Licenses, patents, compliance barriers

## Common Patterns

**Pattern 1: Market Entry Strategy**
- Diagnosis: Assess market using Porter's 5 Forces + competitive profiling
- Guiding Policy: Choose positioning (Blue Ocean or competitive response)
- Coherent Actions: Go-to-market, product roadmap, pricing, partnerships

**Pattern 2: Competitive Response**
- Diagnosis: Analyze competitor threat (new entrant, feature launch, price cut)
- Guiding Policy: Defend, ignore, or leapfrog
- Coherent Actions: Feature parity, differentiation doubling-down, or new positioning

**Pattern 3: Strategic Planning (Annual)**
- Diagnosis: Current state SWOT + market trends + competitive landscape
- Guiding Policy: Focus areas (3-5 strategic themes) for next year
- Coherent Actions: OKRs, initiatives, resource allocation

**Pattern 4: Differentiation Strategy**
- Diagnosis: Competitive positioning map + customer needs analysis
- Guiding Policy: Differentiation axis (vertical, feature set, experience, business model)
- Coherent Actions: Product roadmap, marketing messaging, pricing structure

## Guardrails

**Evidence-Based:**
- Ground diagnosis in data (market research, customer interviews, competitor analysis)
- State assumptions explicitly (market size, growth rate, competitive response)
- Distinguish facts from hypotheses
- Cite sources for key claims

**Coherence:**
- Actions must reinforce each other (not independent initiatives)
- Actions must support the guiding policy
- Guiding policy must address the diagnosis (not aspirational goals)
- Strategy must be internally consistent (no contradictions)

**Realism:**
- Acknowledge constraints (resources, capabilities, time, competition)
- Identify risks and mitigation plans
- Avoid wishful thinking ("if we just execute perfectly...")
- Test strategy against competitive response scenarios

**Specificity:**
- Diagnosis: a specific challenge (not "we need to grow" but "customer acquisition cost exceeds
  LTV in current market")
- Guiding Policy: a clear approach (not "be customer-focused" but "vertical specialization in
  healthcare")
- Coherent Actions: concrete steps with owners and timelines (not "improve product" but "build
  HIPAA compliance by Q2, led by Security Team")

**Differentiation:**
- Strategy must be defensible against competition
- Identify sustainable competitive advantages (moats)
- Avoid "best practices" that competitors can easily copy
- Explain why this strategy is hard for competitors to replicate

## Quick Reference

**Inputs Required:**
- Strategic question or decision to make
- Business context (industry, stage, goals, constraints)
- Competitive landscape (who the competitors are, market dynamics)
- Available resources and capabilities

**Frameworks to Use:**
- Industry analysis → Porter's 5 Forces
- Overall strategy → Good Strategy Kernel
- Positioning → Blue Ocean Strategy Canvas, Value Chain Analysis
- Portfolio → BCG Matrix
- Competitor analysis → SWOT, Competitive Profiling

**Outputs Produced:**
- `strategy-and-competitive-analysis.md` with:
  - Strategic question and context
  - Analysis (frameworks applied, findings, evidence)
  - Strategy summary (diagnosis, guiding policy, coherent actions)
  - Competitive positioning
  - Action plan (initiatives, owners, timelines, success metrics)
  - Assumptions, risks, mitigations

**Bundled files:**
- Quick competitive analysis → [templates/template.md](templates/template.md)
- Complex multi-framework strategy → [references/methodology.md](references/methodology.md)
- Quality validation →
  [assets/evaluators/rubric_strategy_and_competitive_analysis.json](assets/evaluators/rubric_strategy_and_competitive_analysis.json)

## Verification

- Every claim in the diagnosis points at a source or a stated assumption.
- Each coherent action traces back to the guiding policy, and the policy to the diagnosis.
- "Why is this hard to copy" has a specific answer, not "great user experience".
- The frameworks you did not use are named, with the reason.
- Rubric average is at least 3.5/5 before delivering.
