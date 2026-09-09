# GDL Pipeline Patterns and Templates

Orientation material for the geometric deep learning pipeline: what to expect from a data type before discovery starts, the domain patterns that recur, the operating modes, and the template for the final specification. None of it replaces validation. The tables say what is usually true; the validation phase says whether it is true for this dataset.

## Data Type Orientation (Phase 0)

Use this before discovery to form a first guess. Offer it to the user as a hypothesis, not a finding.

| Data type | Likely symmetries | Common groups | What usually breaks it |
|---|---|---|---|
| 2D images | Translation, rotation, reflection | Cₙ, Dₙ, SE(2) | A canonical orientation (text, faces, medical scans with a fixed view); gravity in natural photographs |
| 3D point clouds | 3D rotation, translation, point permutation | SO(3), SE(3), Sₙ | Gravity (a distinguished vertical axis); scanner-fixed frames |
| Molecules | Euclidean motion + identical-atom permutation | E(3) × Sₙ | Chirality: a reflection produces a different molecule, so SE(3) rather than E(3) |
| Graphs and networks | Node permutation | Sₙ | Node identity that carries meaning (an ID that is really a feature) |
| Sets | Element permutation | Sₙ | A hidden ordering, such as time of arrival |
| Time series | Time translation, periodicity | ℤ, Cₙ | Trends, calendar effects, a meaningful t = 0 |
| Physics simulations | Conservation-law symmetries | SE(3), Galilean group, gauge groups | External fields, boundaries, dissipation |
| Tabular | Usually none | — | Column permutation only when columns are exchangeable |

## Common Patterns by Domain

| Domain | Symmetries | Group | Output | Architecture family | Library |
|---|---|---|---|---|---|
| Molecular energy | E(3) + permutation | E(3) × Sₙ | Invariant scalar | E(3) equivariant GNN | e3nn, NequIP, MACE |
| Molecular forces | E(3) + permutation | E(3) × Sₙ | Equivariant vector (l=1) | E(3) equivariant GNN; forces as the gradient of energy | e3nn, NequIP, MACE |
| Protein structure | SE(3) + permutation | SE(3) × Sₙ | Equivariant coordinates | SE(3) transformer or equivariant GNN | e3nn |
| Image classification | Rotation, reflection | Cₙ, Dₙ (p4, p4m) | Invariant label | G-CNN with group pooling | escnn |
| Image segmentation | Rotation, reflection | Cₙ, Dₙ | Equivariant mask | G-CNN encoder-decoder, no final pooling | escnn |
| Point cloud classification | 3D rotation + permutation | SO(3) × Sₙ | Invariant label | Equivariant point network + invariant pool | e3nn |
| Graph classification | Node permutation | Sₙ | Invariant label | Message passing + sum or mean readout | pytorch_geometric |
| Node prediction | Node permutation | Sₙ | Equivariant per node | Message passing, no readout | pytorch_geometric |
| Set prediction | Element permutation | Sₙ | Invariant or per element | DeepSets | plain PyTorch or JAX |
| Robotics pose | Rigid motion | SE(3); under gravity SO(2) ⋊ ℝ³ | Equivariant transform | SE(3) equivariant network | e3nn |

Notes:

- Energy and forces are one model. Predict an invariant energy and take its gradient with respect to positions; the forces are then exactly equivariant by construction.
- "Invariant label" tasks still use equivariant layers internally. Only the final pooling is invariant; pooling earlier throws away orientation the middle layers need.
- When gravity is present, full SO(3) is the wrong group. Rotation about the vertical axis (SO(2)) plus translation is the honest one.
- A pixel grid supports exact C₄ and D₄. Continuous SO(2) on images holds only up to interpolation error; prefer the discrete group unless validation says otherwise.

## Operating Modes

| Mode | Phases | Time | Use when | What the final summary must say |
|---|---|---|---|---|
| Quick | 0 → 1 → 4 → 6 | ~15 min | User knows the symmetries, needs an architecture | Every symmetry marked "Assumed", not validated |
| Standard | 0 → 1 → 2 → 3 → 4 → 6 | ~1 hr | Full discovery and design | Implementation "Not audited" |
| Deep | 0 through 6 | 2-3 hr | Complete pipeline with verification | Audit verdict and error metric |

## Explaining a Group at the User's Level

Beginner: "Your symmetries correspond to [group]. Think of it like [concrete object]. This tells us exactly how to build layers that respect these transformations." Concrete objects that work: the rotations and flips of a square for D₄; shuffling a deck for Sₙ; turning a globe for SO(3); a globe you can also pick up and move for SE(3). Draw the Cayley diagram for small groups.

Expert: "The symmetry structure is [group with product structure]. Key properties: [compact or non-compact], [abelian or non-abelian], [connected or not]. This maps to [architecture family] with [irreps or representations]."

## Final Specification Template (Phase 6)

```
═══════════════════════════════════════════════════════════════
GEOMETRIC DEEP LEARNING SPECIFICATION
═══════════════════════════════════════════════════════════════

PROJECT: [User's project/data description]
MODE: [Quick/Standard/Deep]

───────────────────────────────────────────────────────────────
SYMMETRY ANALYSIS
───────────────────────────────────────────────────────────────

Data Type: [Description]
Task: [Classification/Regression/etc.]
Output Type: [Invariant/Equivariant]

Identified Symmetries:
1. [Symmetry] - [Invariant/Equivariant] - Validated: [Yes/No/Assumed]
2. [Symmetry] - [Invariant/Equivariant] - Validated: [Yes/No/Assumed]

───────────────────────────────────────────────────────────────
GROUP SPECIFICATION
───────────────────────────────────────────────────────────────

Group: [Name and notation]
Structure: [Product structure if applicable]
Key Properties:
- Compact: [Yes/No]
- Abelian: [Yes/No]
- Connected: [Yes/No]

───────────────────────────────────────────────────────────────
ARCHITECTURE
───────────────────────────────────────────────────────────────

Architecture Family: [e.g., E(3) Equivariant GNN]
Library: [e.g., e3nn 0.5.x]
Framework: [PyTorch/JAX]

Layer Summary:
1. [Layer 1]: [Input type] → [Output type]
2. [Layer 2]: [Input type] → [Output type]
...

Estimated Parameters: [Count]

Key Implementation Notes:
- [Note 1]
- [Note 2]

───────────────────────────────────────────────────────────────
IMPLEMENTATION STATUS
───────────────────────────────────────────────────────────────

Implementation: [Not started / In progress / Complete]
Audit Status: [Not audited / PASS / FAIL]
Equivariance Verified: [Yes / No / Pending]

───────────────────────────────────────────────────────────────
NEXT STEPS
───────────────────────────────────────────────────────────────

1. [Immediate next action]
2. [Follow-up action]
3. [Future consideration]

───────────────────────────────────────────────────────────────
QUALITY ASSESSMENT
───────────────────────────────────────────────────────────────

Symmetry Analysis: [Strong / Adequate / Needs Work]
Group Identification: [Strong / Adequate / Needs Work]
Architecture Design: [Strong / Adequate / Needs Work]
Implementation: [Verified / Unverified / Failed]

═══════════════════════════════════════════════════════════════
```

Rules for filling it in:

- "Validated: Assumed" is the only honest value for any symmetry that skipped Phase 2, which is every symmetry in Quick mode.
- "Equivariance Verified: Yes" requires a Phase 5 PASS with the error metric quoted. A library's claim is not a verification.
- The quality assessment grades the evidence, not the effort. A well-reasoned but untested symmetry analysis is "Adequate", not "Strong".
