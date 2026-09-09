---
name: symmetry-group-identifier
description: Map symmetries to groups such as Cn, Dn, Sn, SO(3), SE(3).
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: geometric-deep-learning
    tags: [Group Theory, Lie Groups, Symmetry, Representation Theory, Geometric Deep Learning]
    related_skills: [symmetry-discovery-questionnaire, symmetry-validation-suite, equivariant-architecture-designer]
---
# Symmetry Group Identifier

Formalizes a list of identified transformations into the language of group theory: which group each symmetry is, how the groups combine, and which properties (compact, abelian, connected, finite) the architecture will depend on. Knowing the group is what tells you which equivariant architecture patterns apply. It does not decide whether a symmetry holds and does not design layers; it hands a group specification to `equivariant-architecture-designer`.

## When to Use

- Candidate symmetries have been identified and need formalization into group theory language.
- The user mentions cyclic groups, dihedral groups, Lie groups, SO(3), SE(3), E(3), or permutation groups.
- The user knows their symmetries informally ("rotations and flips") and asks which mathematical group that is.
- Phase 3 of the geometric deep learning pipeline, after validation and before architecture design.
- Skip it when the group is already named and only the architecture is missing.

## Procedure

Copy this checklist and track it with `todo`:

```
Group Identification Progress:
- [ ] Step 1: List symmetries from discovery phase
- [ ] Step 2: Classify each as discrete or continuous
- [ ] Step 3: Match to specific groups using taxonomy
- [ ] Step 4: Determine how groups combine
- [ ] Step 5: Verify group properties
- [ ] Step 6: Document final group specification
```

**Step 1: List symmetries from discovery phase**

Gather the identified symmetries from the discovery phase. List each transformation and whether it requires invariance or equivariance. Note confidence levels. If symmetries have not been discovered yet, run `symmetry-discovery-questionnaire` with the user first.

**Step 2: Classify each as discrete or continuous**

For each symmetry, decide whether the transformation set is finite (discrete) or infinite (continuous). Discrete examples: 90° rotations (4 elements), permutations of n items (n! elements). Continuous examples: rotation by any angle, translation by any distance. Use the [Group Taxonomy](#group-taxonomy) to guide the classification. For the mathematical foundations, load `skill_view("symmetry-group-identifier", file_path="references/group-theory-primer.md")`.

**Step 3: Match to specific groups using taxonomy**

Use the [Discrete Groups](#discrete-groups) and [Continuous Groups](#continuous-groups-lie-groups) sections. Identify the group name and notation for each symmetry. Common matches: n-fold rotation → Cₙ, rotation+reflection → Dₙ, permutation → Sₙ, 3D rotation → SO(3), rigid motion → SE(3), full Euclidean → E(3). For Lie group detail (SO(3), SE(3), E(3), irreps, spherical harmonics), load `skill_view("symmetry-group-identifier", file_path="references/lie-groups.md")`.

**Step 4: Determine how groups combine**

If several symmetries are present, determine how they combine. Direct product (G × H): the symmetries act independently. Semidirect product (G ⋊ H): one symmetry "twists" the other (SE(3) = SO(3) ⋊ ℝ³). Use [Combining Groups](#combining-groups).

**Step 5: Verify group properties**

Check that the identified structure satisfies the group axioms: closure, associativity, identity, inverses. Then check the properties that drive the architecture: Is it compact? (affects representation theory). Is it abelian? (commutative or not). Is it connected? (affects implementation). Use the [Group Properties Checklist](#group-properties-checklist). For the verification methodology and representation theory background, load `skill_view("symmetry-group-identifier", file_path="references/methodology.md")`.

**Step 6: Document final group specification**

Write the specification with the [Output Template](#output-template). Include group name and notation, dimension or size, key properties, invariance versus equivariance requirements, and the recommended architecture family. This specification is the input to architecture design. Quality criteria are in `assets/evaluators/rubric_group_identification.json`.

## Group Taxonomy

### Overview Diagram

```
                    SYMMETRY GROUPS
                          │
          ┌───────────────┴───────────────┐
          │                               │
     DISCRETE                        CONTINUOUS
          │                          (Lie Groups)
          │                               │
    ┌─────┼─────┐               ┌────────┼────────┐
    │     │     │               │        │        │
  Cyclic Dihedral Symmetric   SO(n)   SE(n)    E(n)
   Cₙ     Dₙ      Sₙ         rotations rigid   Euclidean
                              only    motions  (w/ reflect)
```

### Quick Reference Table

| Symmetry Type | Group | Notation | Elements | Common Use |
|---------------|-------|----------|----------|------------|
| n-fold rotation | Cyclic | Cₙ | n | Image rotation (90°, 60°) |
| Rotation + reflection | Dihedral | Dₙ | 2n | Regular polygons |
| Permutation | Symmetric | Sₙ | n! | Sets, graphs |
| 2D rotation (continuous) | Special orthogonal | SO(2) | ∞ | Continuous rotation |
| 3D rotation | Special orthogonal | SO(3) | ∞ | 3D orientation |
| 3D rigid motion | Special Euclidean | SE(3) | ∞ | Robotics, molecules |
| 3D with reflections | Euclidean | E(3) | ∞ | Chemistry, physics |

## Discrete Groups

### Cyclic Groups (Cₙ)

**What they represent**: Rotations by multiples of 360°/n

**Elements**: {e, r, r², ..., rⁿ⁻¹} where rⁿ = e (identity)

| Group | Rotations | Example |
|-------|-----------|---------|
| C₂ | 0°, 180° | Playing cards |
| C₄ | 0°, 90°, 180°, 270° | Square images |
| C₆ | 60° increments | Hexagonal patterns |

**Use when**: Rotation symmetry is present but NOT reflection symmetry.

### Dihedral Groups (Dₙ)

**What they represent**: Rotations + reflections of a regular n-gon

**Elements**: n rotations + n reflections = 2n total

| Group | Elements | Example |
|-------|----------|---------|
| D₄ | 8 | Square with diagonals (p4m group) |
| D₆ | 12 | Regular hexagon |

**Use when**: Both rotation AND reflection symmetry are present.

### Symmetric Groups (Sₙ)

**What they represent**: All permutations of n elements

**Elements**: n! permutations

**Use when**: Element ordering is arbitrary (sets, graphs, point clouds).

## Continuous Groups (Lie Groups)

### SO(2) - 2D Rotations

**Elements**: Rotation by any angle θ ∈ [0, 2π)

**Matrix form**: R(θ) = [[cos θ, -sin θ], [sin θ, cos θ]]

**Use when**: Continuous rotation symmetry in 2D.

### SO(3) - 3D Rotations

**Elements**: All rotations in 3D (3 degrees of freedom)

**Representations**: Rotation matrices, quaternions, Euler angles, axis-angle

**Use when**: 3D orientation does not matter, but handedness does.

### SE(3) - 3D Rigid Motions

**Elements**: Rotations + translations in 3D

**Structure**: SE(3) = SO(3) ⋊ ℝ³ (semidirect product)

**Use when**: Objects can be anywhere and in any orientation, and handedness matters.

### E(3) - Full Euclidean Group

**Elements**: SE(3) + reflections

**Structure**: E(3) = O(3) ⋊ ℝ³

**Use when**: SE(3) symmetry PLUS reflection symmetry (most molecules).

### Group Hierarchy

```
E(3) = O(3) ⋊ ℝ³
    │ exclude reflections
    ▼
SE(3) = SO(3) ⋊ ℝ³
    │ exclude translations
    ▼
SO(3)
    │ 2D restriction
    ▼
SO(2)
```

## Combining Groups

### Direct Product (G × H)

**When to use**: The symmetries act independently (neither affects the other).

**Example**: Image with separate translation and color permutation → SE(2) × S₃

**Property**: (g₁, h₁) · (g₂, h₂) = (g₁g₂, h₁h₂)

### Semidirect Product (G ⋊ H)

**When to use**: One symmetry "twists" the other (they do not commute).

**Example**: SE(3) = SO(3) ⋊ ℝ³ (rotating then translating ≠ translating then rotating)

**Common cases**: SE(n) = SO(n) ⋊ ℝⁿ, E(n) = O(n) ⋊ ℝⁿ, Dₙ = Cₙ ⋊ C₂

## Group Properties Checklist

For the identified group, verify:

| Property | Question | Why It Matters |
|----------|----------|----------------|
| Compact | Is the group "bounded"? | Affects representation theory |
| Abelian | Does order matter? (g₁g₂ = g₂g₁?) | Simplifies architecture |
| Connected | Is the group in one piece? | Affects irreducible representations |
| Finite | Finite number of elements? | Discrete vs continuous architecture |

## Group Selection by Domain

| Domain | Typical Group | Notes |
|--------|--------------|-------|
| 2D Image Classification | C₄ or D₄ | p4 or p4m groups |
| 3D Molecular Energy | E(3) × Sₙ | Full Euclidean + atom permutation |
| 3D Molecular Chirality | SE(3) × Sₙ | No reflections |
| Point Cloud Classification | SO(3) × Sₙ | Rotation + permutation |
| Graph Classification | Sₙ | Permutation invariant |
| Robotics | SE(3) | Sometimes with gravity constraint |

## Pitfalls

- SO(3) versus O(3)/E(3): if mirror images must be distinguished (chirality, handedness), do not include reflections. Including them silently forces the model to treat enantiomers as identical.
- Forgetting the semidirect structure: rotations and translations do not commute, so SE(3) is SO(3) ⋊ ℝ³, not SO(3) × ℝ³. The distinction changes how features transform.
- Over-large permutation groups: identical atoms permute among themselves (a product of small Sₖ), not all n atoms at once. Say which elements are interchangeable.
- Exact versus approximate on grids: a pixel grid supports exact C₄ or D₄; continuous SO(2) only holds up to interpolation error. Prefer the discrete group unless validation says otherwise.
- Calling interacting symmetries a direct product: if one transformation changes how another acts (rotation changes which pixels are neighbors), the groups are not independent.

## Output Template

```
SYMMETRY GROUP SPECIFICATION
============================

Identified Symmetries:
1. [Symmetry] → Group: [name] ([notation])
2. [Symmetry] → Group: [name] ([notation])

Combined Group Structure:
- Full group: [G₁ × G₂] or [G₁ ⋊ G₂]
- Size: [# elements] or [continuous]

Group Properties:
- Compact: [Yes/No]
- Abelian: [Yes/No]
- Connected: [Yes/No]

Symmetry Requirements:
- [Group]: [Invariant/Equivariant] for [task type]

Recommended Architecture Family:
- [Architecture] supporting [group]

NEXT STEPS:
- Empirically validate symmetry hypotheses if not yet confirmed
- Design equivariant architecture based on group specification
```

## Verification

Before handing the specification on, check the axioms on concrete elements rather than by assertion. Compose two sampled elements and confirm the result is still in the set (closure). Confirm the identity is in the set. Confirm each sampled element has an inverse in the set. For matrix groups, add the determinant test. SO(3) has RᵀR = I and det R = +1; O(3) also allows det R = −1. If the user's transforms include det −1 matrices, the group is O(3) or E(3), not SO(3). The numerical form of these checks is under Group Structure Tests in `symmetry-validation-suite`. Run it with `terminal` when the group is anything beyond the standard families.
