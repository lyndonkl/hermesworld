---
name: layered-reasoning
description: Align strategy, tactics and operations across levels.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: thinking
    tags: [Abstraction Levels, Strategy To Execution, Consistency Checks, Top-Down Design]
    related_skills: [strategy-and-competitive-analysis, systems-thinking-leverage, communication-storytelling]
---
# Layered Reasoning

Structures thinking across multiple abstraction levels (30,000 ft strategic, 3,000 ft tactical,
300 ft operational) while keeping the layers consistent with each other. It guides top-down
decomposition, bottom-up aggregation, cross-layer translation, and constraint propagation, and it
ends with an explicit consistency check. It does not pick the strategy or design the system; it
makes sure that what was picked at one altitude still holds at the others.

## When to Use

- Reasoning across multiple abstraction levels at once, for example vision to strategy to
  tactics to product surface.
- Designing systems with hierarchical layers, or explaining one concept at different depths to
  different audiences (board, manager, engineer).
- Checking that principles and implementation still agree, or that a stated strategy matches what
  actually ships and where money goes.
- The user mentions 30,000-foot view, layered thinking, abstraction levels, top-down design, or
  strategy-to-execution alignment.

## Common Patterns

### Pattern 1: 30K → 3K → 300 ft Decomposition (Top-Down)

**When**: Starting from vision/principles, deriving concrete actions

**Structure**:
- **30,000 ft (Strategic)**: Why? Core principles, invariants, constraints (e.g., "Customer
  privacy is non-negotiable")
- **3,000 ft (Tactical)**: What? Approaches, architectures, policies (e.g., "Zero-trust security
  model, end-to-end encryption")
- **300 ft (Operational)**: How? Specific actions, procedures, code (e.g., "Implement AES-256
  encryption for data at rest")

**Example**: Product strategy
- **30K**: "Become the most trusted platform" (principle)
- **3K**: "Achieve SOC 2 compliance, publish security reports, 24/7 support" (tactics)
- **300 ft**: "Implement MFA, conduct quarterly audits, hire 5 support engineers" (actions)

**Process**: (1) Define strategic layer invariants, (2) Derive tactical options that satisfy
invariants, (3) Select tactics, (4) Design operational procedures implementing tactics,
(5) Validate that the operational layer does not violate strategic constraints

### Pattern 2: Bottom-Up Aggregation

**When**: Starting from observations/data, building up to principles

**Structure**:
- **300 ft**: Specific observations, measurements, incidents (e.g., "User A clicked 5 times, User
  B abandoned")
- **3,000 ft**: Patterns, trends, categories (e.g., "40% abandon at checkout, slow load times
  correlate with abandonment")
- **30,000 ft**: Principles, theories, root causes (e.g., "Performance impacts conversion; every
  100ms costs 1% conversion")

**Example**: Engineering postmortem
- **300 ft**: "Service crashed at 3:42 PM, memory usage spiked to 32GB, 500 errors returned"
- **3K**: "Memory leak in caching layer, triggered by specific API call pattern under load"
- **30K**: "Our caching strategy lacks eviction policy; need TTL-based expiration for all caches"

**Process**: (1) Collect operational data, (2) Identify patterns and group, (3) Formulate
hypotheses at tactical layer, (4) Validate with more data, (5) Distill strategic principles

### Pattern 3: Layer Translation (Cross-Layer Communication)

**When**: Explaining the same concept to different audiences (CEO, manager, engineer)

**Technique**: Translate preserving core meaning while adjusting abstraction

**Example**: Explaining tech debt
- **CEO (30K)**: "We built quickly early on. Now growth slows 20% annually unless we invest $2M to
  modernize."
- **Manager (3K)**: "Monolithic architecture prevents independent team velocity. Migrate to
  microservices over 6 months."
- **Engineer (300 ft)**: "Extract user service from monolith. Create API layer, implement service
  mesh, migrate traffic."

**Process**: (1) Identify the audience's layer, (2) Extract the core message, (3) Translate using
concepts and metrics relevant to that layer, (4) Maintain causal links across layers

### Pattern 4: Constraint Propagation (Top-Down)

**When**: High-level constraints must guide low-level decisions

**Mechanism**: Strategic constraints flow down, narrowing options at each layer

**Example**: Healthcare app design
- **30K constraint**: "HIPAA compliance is non-negotiable" (strategic)
- **3K derivation**: "All PHI must be encrypted, audit logs required, access control mandatory"
  (tactical)
- **300 ft implementation**: "Use AWS KMS for encryption, CloudTrail for audits, IAM for access"
  (operational)

**Guardrail**: Lower layers cannot violate upper constraints (e.g., an operational decision to
skip encryption violates the strategic constraint)

### Pattern 5: Emergent Property Recognition (Bottom-Up)

**When**: Lower-layer interactions create unexpected upper-layer behavior

**Example**: Team structure
- **300 ft**: "Each team owns a microservice, deploys independently, uses Slack for coordination"
- **3K emergence**: "Conway's Law: architecture mirrors communication structure; slow cross-team
  features"
- **30K insight**: "Org structure determines system architecture; realign teams to product lines,
  not services"

**Process**: (1) Observe operational behavior, (2) Identify emerging patterns at the tactical
layer, (3) Recognize strategic implications, (4) Adjust strategy if needed

### Pattern 6: Consistency Checking Across Layers

**When**: Validating that all layers align (no contradictions)

**Check types**:
- **Upward consistency**: Do operations implement tactics? Do tactics achieve strategy?
- **Downward consistency**: Can strategy be executed with these tactics? Can tactics be
  implemented operationally?
- **Lateral consistency**: Do parallel tactical choices contradict? Do operational procedures
  conflict?

**Example inconsistency**: Strategy says "Move fast," tactics say "Extensive approval process,"
operations say "3-week release cycle" → Contradiction

**Fix**: Align layers. Either (1) change strategy ("Move carefully"), (2) change tactics
("Lightweight approvals"), or (3) change operations ("Daily releases")

---

## Procedure

Use this structured approach when applying layered reasoning:

```
□ Step 1: Identify relevant layers and abstraction levels
□ Step 2: Define strategic layer (principles, invariants, constraints)
□ Step 3: Derive tactical layer (approaches that satisfy strategy)
□ Step 4: Design operational layer (concrete actions implementing tactics)
□ Step 5: Validate consistency across all layers
□ Step 6: Translate between layers for different audiences
□ Step 7: Iterate based on feedback from any layer
□ Step 8: Document reasoning at each layer
```

Each step is expanded in [references/methodology.md](references/methodology.md): layer design
principles (Step 1-4), consistency validation techniques (Step 5), emergence detection and
bidirectional propagation (Step 7).

**Step 1: Identify relevant layers and abstraction levels**
Determine how many layers are needed (typically 3-5). Map layers to domains: business
(vision/strategy/execution), technical (architecture/design/code), organizational
(mission/goals/tasks).

**Step 2: Define the strategic layer**
Establish the high-level principles, invariants, and constraints that must hold. These are
non-negotiable and guide all lower layers.

**Step 3: Derive the tactical layer**
Generate approaches, policies or architectures that satisfy the strategic constraints. Multiple
tactical options may exist; choose based on tradeoffs.

**Step 4: Design the operational layer**
Create the specific procedures, implementations, or actions that realize the tactical choices.
This is where execution happens.

**Step 5: Validate consistency across all layers**
Check upward (do ops implement tactics?), downward (can strategy be executed?), and lateral (do
parallel choices conflict?) consistency.

**Step 6: Translate between layers for different audiences**
Communicate at the appropriate abstraction level for each stakeholder. A CEO needs the strategic
view; engineers need operational detail.

**Step 7: Iterate based on feedback from any layer**
If operational constraints make tactics infeasible, adjust tactics or strategy. If a strategic
shift occurs, propagate the change downward.

**Step 8: Document reasoning at each layer**
Write explicit rationale at each layer explaining how it relates to the layers above and below.
This makes assumptions visible and aids future iteration.

---

## Guardrails

### 1. Maintain Consistency Across Layers

**Danger**: Strategic goals contradict operational reality, or implementation violates principles

**Guardrail**: Regularly check upward, downward, and lateral consistency. Propagate changes
bidirectionally (strategy changes → update tactics/ops; operational constraints → update
tactics/strategy).

**Red flag**: "Our strategy is X but we actually do Y" signals a layer mismatch

### 2. Don't Skip Layers When Communicating

**Danger**: Jumping from 30K to 300 ft confuses audiences, loses context

**Guardrail**: Move through layers sequentially. If explaining to an executive, start 30K → 3K
(stop there unless asked). If explaining to an engineer, provide 30K context first, then dive to
300 ft.

**Test**: Can the listener answer "why does this matter?" (links to the upper layer) and "how do
we do this?" (links to the lower layer)

### 3. Each Layer Should Be Independently Useful

**Danger**: Layers that only make sense when combined, not standalone

**Guardrail**: The strategic layer should guide decisions even without seeing operations. The
tactical layer should be understandable without code. The operational layer should be executable
without re-deriving strategy.

**Principle**: Good layers can be consumed independently by different audiences

### 4. Limit Layers to 3-5 Levels

**Danger**: Too many layers create overhead; too few lose nuance

**Guardrail**: For most domains, 3 layers suffice (strategy/tactics/operations or
architecture/design/code). Complex domains may need 4-5 but rarely more.

**Rule of thumb**: Can you name each layer clearly? If not, you have too many.

### 5. Upper Layers Constrain, Lower Layers Implement

**Danger**: Treating layers as independent rather than hierarchical

**Guardrail**: The strategic layer sets constraints ("must be HIPAA compliant"). The tactical
layer chooses approaches within constraints ("encryption + audit logs"). The operational layer
implements ("AES-256 + CloudTrail"). Nothing may violate upward.

**Anti-pattern**: An operational decision ("skip encryption for speed") violating a strategic
constraint ("HIPAA compliance")

### 6. Propagate Changes Bidirectionally

**Danger**: A strategic shift without updating tactics/ops, or an operational constraint
discovered but strategy unchanged

**Guardrail**: **Top-down**: strategy changes → re-evaluate tactics → adjust operations.
**Bottom-up**: operational constraint → re-evaluate tactics → potentially adjust strategy.

**Example**: Strategy shift to "privacy-first" → Update tactics (end-to-end encryption) → Update
ops (implement encryption). Or: Operational constraint (performance) → Tactical adjustment
(different approach) → Strategic clarification ("privacy-first within performance constraints")

### 7. Make Assumptions Explicit at Each Layer

**Danger**: Implicit assumptions lead to inconsistency when the assumptions are violated

**Guardrail**: Document assumptions at each layer. Strategic: "Assuming competitive market."
Tactical: "Assuming cloud infrastructure." Operational: "Assuming Python 3.9+."

**Benefit**: When assumptions change, you know which layers need updating

### 8. Recognize Emergent Properties

**Danger**: Focusing only on designed properties, missing unintended consequences

**Guardrail**: Regularly observe the bottom layer, look for emerging patterns at the middle
layer, consider strategic implications. Emergent properties can invalidate strategic assumptions.

**Example**: Microservices (operational) → Coordination overhead (tactical emergence) → Slower
feature delivery (strategic failure if the goal was speed)

---

## Quick Reference

### Layer Mapping by Domain

| Domain | Layer 1 (30K ft) | Layer 2 (3K ft) | Layer 3 (300 ft) |
|--------|------------------|-----------------|------------------|
| **Business** | Vision, mission | Strategy, objectives | Tactics, tasks |
| **Product** | Market positioning | Feature roadmap | User stories |
| **Technical** | Architecture principles | System design | Code implementation |
| **Organizational** | Culture, values | Policies, processes | Daily procedures |

### Consistency Check Questions

| Check Type | Question |
|------------|----------|
| **Upward** | Do these operations implement the tactics? Do the tactics achieve the strategy? |
| **Downward** | Can this strategy be executed with the available tactics? Can the tactics be implemented operationally? |
| **Lateral** | Do parallel tactical choices contradict each other? Do operational procedures conflict? |

### Translation Hints by Audience

| Audience | Layer | Focus | Metrics |
|----------|-------|-------|---------|
| **CEO / Board** | 30K ft | Why, outcomes, risk | Revenue, market share, strategic risk |
| **VP / Director** | 3K ft | What, approach, resources | Team velocity, roadmap, budget |
| **Manager / Lead** | 300-3K ft | How, execution, timeline | Sprint velocity, milestones, quality |
| **Engineer** | 300 ft | Implementation, details | Code quality, test coverage, performance |

### Bundled files

- [templates/template.md](templates/template.md): layered reasoning document template,
  consistency check template, cross-layer communication template
- [references/methodology.md](references/methodology.md): layer design principles, consistency
  validation techniques, emergence detection, bidirectional propagation
- [assets/evaluators/rubric_layered_reasoning.json](assets/evaluators/rubric_layered_reasoning.json):
  evaluation criteria for layered reasoning quality (10 criteria)

### Related skills in this package

- `communication-storytelling` for translating between audiences at different layers
- `strategy-and-competitive-analysis` for defining the strategic layer of a business
- `systems-thinking-leverage` when a layer's behaviour comes from a feedback loop rather than a
  decision

---

## Examples in Context

### Example 1: SaaS Product Strategy

**30K (Strategic)**: "Become the easiest CRM for small businesses" (positioning)

**3K (Tactical)**: "Simple UI, 5-minute setup, mobile-first, $20/user pricing, self-serve
onboarding"

**300 ft (Operational)**: "React app, OAuth for auth, Stripe for billing, onboarding flow: signup
→ import contacts → send first email"

**Consistency check**: Does $20 pricing support "easiest" (yes, low barrier)? Does 5-minute setup
work with the current implementation (measure in practice)? Does mobile-first align with the React
architecture (yes)?

### Example 2: Technical Architecture

**30K**: "Highly available system with <1% downtime, supports 10× traffic growth"

**3K**: "Multi-region deployment, auto-scaling, circuit breakers, blue-green deployments"

**300 ft**: "AWS multi-AZ, ECS Fargate with target tracking, Istio circuit breakers, CodeDeploy
blue-green"

**Emergence**: Observed: cross-region latency 200ms → Tactical adjustment: regional data
replication → Strategic clarification: "High availability within regions, eventual consistency
across regions"

### Example 3: Organizational Change

**30K**: "Build a customer-centric culture where customer feedback drives decisions"

**3K**: "Monthly customer advisory board, NPS surveys after each interaction, customer support
KPIs in exec dashboards"

**300 ft**: "Schedule CAB meetings first Monday monthly, automated NPS via Delighted after ticket
close, Looker dashboard with CS CSAT by rep"

**Consistency**: Does a monthly CAB support "customer-centric" (or is it too infrequent)? Do the
support KPIs incentivize the right behavior (check for gaming)? Does automation reduce personal
touch (potential conflict)?

## Verification

- Each layer is named, and there are no more than five.
- The three consistency questions (upward, downward, lateral) each have a written answer, and
  every "no" has a named fix at one specific layer.
- Every layer states its assumptions.
- Rubric average against
  [assets/evaluators/rubric_layered_reasoning.json](assets/evaluators/rubric_layered_reasoning.json)
  is at least 3.5/5 before delivering.
