---
name: symmetry-discovery-questionnaire
description: Identify candidate symmetries in data through questions.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: geometric-deep-learning
    tags: [Symmetry, Invariance, Equivariance, Data Analysis, Geometric Deep Learning]
    related_skills: [symmetry-validation-suite, symmetry-group-identifier]
---
# Symmetry Discovery Questionnaire

Walks an ML engineer through structured questions about their domain, coordinate system, candidate transformations, and physical constraints, and produces a ranked list of symmetry candidates with evidence and confidence. The user needs no group theory. It does not test whether a symmetry holds (that is `symmetry-validation-suite`) and does not name the group (that is `symmetry-group-identifier`).

## When to Use

- The user has data but does not know which symmetries their model should respect.
- The user mentions data symmetry, invariance discovery, or asks what transformations matter.
- The user needs help recognizing patterns their model should respect before choosing an architecture.
- Phase 1 of the geometric deep learning pipeline, once data type, task, and constraints are known.
- Skip it when the symmetries are already known and only need formalizing; go straight to `symmetry-group-identifier`.

## Procedure

Copy this checklist and track it with `todo`:

```
Symmetry Discovery Progress:
- [ ] Step 1: Classify the domain and data type
- [ ] Step 2: Analyze coordinate system choices
- [ ] Step 3: Test candidate transformations
- [ ] Step 4: Analyze physical constraints
- [ ] Step 5: Determine output behavior under transformations
- [ ] Step 6: Document symmetry candidates
```

**Step 1: Classify the domain and data type**

Ask the user what their primary data type is (use `clarify` when several fit). Use this map to seed the likely symmetries and the questions that follow. Images (2D grids) → likely translation, rotation, reflection. 3D data (point clouds, meshes) → likely SE(3), E(3). Molecules → E(3) + permutation + point groups. Graphs and networks → permutation. Sets → permutation. Time series → time-translation, periodicity. Tabular → rarely symmetric. Physical systems → conservation laws imply symmetries. For worked examples by domain, load `skill_view("symmetry-discovery-questionnaire", file_path="references/domain-examples.md")`.

**Step 2: Analyze coordinate system choices**

Guide the user through the coordinate questions: Is there a preferred origin? (NO → translation invariance). Is there a preferred orientation? (NO → rotation invariance). Is there a preferred handedness? (NO → reflection invariance). Is there a preferred scale? (NO → scale invariance). Is element ordering meaningful? (NO → permutation invariance). Document each answer with its reasoning.

**Step 3: Test candidate transformations**

For each candidate transformation T, ask: "If I transform my input by T, should my output change?" If NO → invariance to T. If YES, predictably → equivariance to T. If YES, unpredictably → no symmetry. Work through the domain checklists in [Domain Transformation Tests](#domain-transformation-tests) and test every relevant transformation. The reasoning behind this testing approach is in `skill_view("symmetry-discovery-questionnaire", file_path="references/methodology.md")`.

**Step 4: Analyze physical constraints**

Ask about conservation laws and physical symmetries. Noether's theorem: every conservation law implies a symmetry. Energy conserved → time-translation symmetry. Momentum conserved → space-translation symmetry. Angular momentum conserved → rotation symmetry. Ask: Are there physical conservation laws? Is the system isolated from external reference frames? Are there gauge freedoms?

**Step 5: Determine output behavior under transformations**

The critical question: when the input transforms, how should the output transform? Classification labels → stay the same (invariance). Bounding boxes → move with the object (equivariance). Force vectors → rotate with the system (equivariance). Scalar properties → stay the same (invariance). Segmentation masks → transform with the image (equivariance). This decides whether an invariant or an equivariant architecture is needed.

**Step 6: Document symmetry candidates**

Write the summary with the [Output Template](#output-template). List identified symmetries with confidence levels. Note uncertain cases that need empirical validation. Identify non-symmetries (transformations that DO matter). Recommend next steps for validation and formalization. Quality criteria for the output are in `assets/evaluators/rubric_symmetry_discovery.json`.

## Domain Transformation Tests

### Image Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Translation | Does object position matter for label? | Translation invariance |
| Rotation (90°) | Would rotated image have same label? | C4 symmetry |
| Rotation (any) | Would any rotation preserve label? | SO(2) symmetry |
| Horizontal flip | Would mirror image have same label? | Reflection |
| Scale | Would zoomed image have same label? | Scale invariance |

### 3D Data Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| 3D Translation | Does absolute position matter? | Translation invariance |
| 3D Rotation | Does orientation matter? | SO(3) or SE(3) |
| Reflection | Does handedness matter? | O(3) or E(3) |
| Point permutation | Does point ordering matter? | Permutation invariance |

### Graph Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Node relabeling | Does node ID matter, or just connectivity? | Permutation invariance |

### Molecular Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Rotation | Is property independent of orientation? | SO(3) |
| Translation | Is property independent of position? | Translation |
| Reflection | Are both enantiomers equivalent? | Include reflections |
| Atom permutation | Do identical atoms behave identically? | Permutation |

### Temporal Symmetries

| Transformation | Test Question | If NO → |
|----------------|---------------|---------|
| Time shift | Can pattern occur at any time? | Time-translation |
| Time reversal | Is forward same as backward? | Time-reversal |
| Periodicity | Do patterns repeat with period T? | Cyclic symmetry |

## Quick Reference

**The 5 key questions:**
1. Is there a preferred coordinate system? (origin, orientation, scale)
2. Does element ordering matter?
3. What transformations leave the label unchanged?
4. What physical constraints apply?
5. How should outputs transform when inputs transform?

**Common symmetry → group mapping:**
- Rotation (2D, discrete) → Cyclic group Cₙ
- Rotation + reflection (2D) → Dihedral group Dₙ
- Rotation (2D, continuous) → SO(2)
- Rotation (3D) → SO(3)
- Rotation + translation (3D) → SE(3)
- Full Euclidean (3D) → E(3)
- Permutation → Symmetric group Sₙ

## Pitfalls

- Assuming a symmetry without verification: anything not backed by a domain argument goes in the Uncertain list and on to `symmetry-validation-suite`.
- Missing broken symmetries: gravity breaks rotation for falling objects, edge effects break translation near boundaries, camera orientation breaks rotation in natural photographs. Ask what breaks the symmetry and whether to condition on it.
- Confusing data symmetry with label symmetry: the data may be symmetric while the task is not. Always ask how the OUTPUT should transform.
- Over-constraining: too much symmetry limits expressiveness. Start with the obvious symmetries and add cautiously.
- Ignoring approximate symmetries: when exact symmetry is not needed, soft equivariance or augmentation is often the better design. Note the range in which the symmetry holds.
- Task-dependent symmetries: the same molecule data is E(3)-invariant for energy, E(3)-equivariant for forces, and only SE(3) for chirality. Analyze symmetries relative to the specific task.

The reasoning behind each is in `references/methodology.md`.

## Output Template

```
SYMMETRY CANDIDATE SUMMARY
==========================

Domain: [Data type]
Task: [Classification/Regression/Detection/etc.]

IDENTIFIED SYMMETRIES:
1. [Transformation]: [Invariance/Equivariance]
   - Evidence: [Why you believe this]
   - Confidence: [High/Medium/Low]

2. [Transformation]: [Invariance/Equivariance]
   - Evidence: [Why you believe this]
   - Confidence: [High/Medium/Low]

UNCERTAIN SYMMETRIES (need validation):
- [Transformation]: [Reason for uncertainty]

NON-SYMMETRIES (transformations that DO matter):
- [Transformation]: [Why it matters]

NEXT STEPS:
- Empirically validate uncertain symmetry candidates
- Map confirmed symmetries to mathematical groups
- Design architecture based on validated group structure
```

## Verification

The summary is done when three things hold. Every identified symmetry names the transformation, states invariance or equivariance, gives evidence, and carries a confidence level. Every Medium or Low confidence entry also appears under Uncertain. At least one non-symmetry is listed; a discovery that finds nothing that matters is usually incomplete. Read the result back to the user and ask whether it matches their domain intuition. Then score it against `assets/evaluators/rubric_symmetry_discovery.json`.
