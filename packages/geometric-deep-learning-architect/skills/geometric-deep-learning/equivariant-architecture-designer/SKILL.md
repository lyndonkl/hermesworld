---
name: equivariant-architecture-designer
description: Design a network that respects a validated symmetry group.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: geometric-deep-learning
    tags: [Equivariant Networks, Architecture Design, Group Convolution, Graph Neural Networks, Geometric Deep Learning]
    related_skills: [symmetry-group-identifier, model-equivariance-auditor, readability-check]
---
# Equivariant Architecture Designer

Turns a group specification and task requirements into an architecture. It picks the family (G-CNN, steerable CNN, e3nn tensor product network, message passing, DeepSets), lays out the layer-by-layer representation flow, chooses the nonlinearity, normalization, and pooling that keep equivariance, and names the library to build it in. The output is a specification with a code skeleton, not a trained model. It does not verify a finished implementation; that is `model-equivariance-auditor`.

## When to Use

- The user has validated symmetry groups and needs equivariant architecture design.
- The user mentions equivariant layers, G-CNN, e3nn, escnn, steerable networks, or building symmetry into a model.
- The user asks which library or layer type supports their group, or how to get an invariant output from equivariant features.
- Phase 4 of the geometric deep learning pipeline, after group identification.
- Skip it when the user already has an implementation and wants it checked; go to `model-equivariance-auditor`.

## Procedure

Copy this checklist and track it with `todo`:

```
Architecture Design Progress:
- [ ] Step 1: Review group specification and requirements
- [ ] Step 2: Select architecture family
- [ ] Step 3: Choose specific layers and components
- [ ] Step 4: Design network topology
- [ ] Step 5: Select implementation library
- [ ] Step 6: Create architecture specification
```

**Step 1: Review group specification and requirements**

Gather the validated group specification. Confirm which group(s) are involved, whether invariance or equivariance is needed, the data domain (images, point clouds, graphs, and so on), the task type (classification, regression, generation), and the computational constraints. If the group is not specified, run `symmetry-group-identifier` with the user first; if any of these is genuinely open, ask with `clarify`.

**Step 2: Select architecture family**

Match the symmetry group to a family using the [Architecture Selection Guide](#architecture-selection-guide). Key families: G-CNNs for discrete groups on grids, steerable CNNs for continuous 2D groups, e3nn/NequIP for E(3) on point data, GNNs for permutation on graphs, DeepSets for permutation on sets. Weigh expressiveness against efficiency. The domain-to-group-to-library patterns that recur across projects are collected in `skill_view("equivariant-architecture-designer", file_path="references/gdl-pipeline-patterns.md")`.

**Step 3: Choose specific layers and components**

Pick layer types from the [Layer Patterns](#layer-patterns). For each layer decide four things. Convolution type: regular, group, or steerable. Nonlinearity: it must preserve equivariance, so use gated, norm-based, or tensor product. Normalization: batch norm breaks equivariance, so use layer norm or an equivariant batch norm. Pooling: invariant pooling for invariant outputs, structure-preserving for equivariant outputs. For the design principles and the three canonical patterns, load `skill_view("equivariant-architecture-designer", file_path="references/methodology.md")`.

**Step 4: Design network topology**

Design the overall structure: the encoder (how features are extracted), the feature representation at each stage (irreps for Lie groups), the pooling or aggregation strategy, and an output head that matches the task. Use the [Topology Patterns](#topology-patterns). Balance depth against width for the group size.

**Step 5: Select implementation library**

Choose from the [Library Reference](#library-reference) by group, framework preference (PyTorch or JAX), and performance needs. Common choices: e3nn (E(3)/O(3), PyTorch), escnn (discrete and 2D continuous groups, PyTorch), pytorch_geometric (permutation, PyTorch). Library APIs change between releases: confirm the current class names and irreps syntax with `web_extract` on the library's documentation before writing code, and pin the version in the specification.

**Step 6: Create architecture specification**

Document the design with the [Output Template](#output-template) and save it with `write_file`. Include the layer-by-layer specification, representation types, library dependencies, expected parameter count, and a code skeleton. This specification drives implementation and the later equivariance audit. For ready-to-adapt implementations (E(3) GNN in e3nn, discrete-group CNN in escnn, DeepSets, permutation-equivariant GNN), load `skill_view("equivariant-architecture-designer", file_path="templates/templates.md")`. Quality criteria are in `assets/evaluators/rubric_architecture.json`.

## Architecture Selection Guide

### By Symmetry Group

| Group | Domain | Recommended Architecture | Library |
|-------|--------|-------------------------|---------|
| Cₙ, Dₙ | 2D Images | G-CNN, Group Equivariant CNN | escnn, e2cnn |
| SO(2), O(2) | 2D Images | Steerable CNN, Harmonic Networks | escnn |
| SO(3) | Spherical | Spherical CNN | e3nn, s2cnn |
| SE(3), E(3) | Point clouds | Equivariant GNN, Tensor Field Networks | e3nn, NequIP |
| Sₙ | Sets | DeepSets | pytorch, jax |
| Sₙ | Graphs | Message Passing GNN | pytorch_geometric |
| E(3) × Sₙ | Molecules | E(3) Equivariant GNN | e3nn, SchNet |

### By Task Type

| Task | Output Type | Key Consideration |
|------|-------------|-------------------|
| Classification | Invariant scalar | Use invariant pooling |
| Regression (scalar) | Invariant scalar | Same as classification |
| Segmentation | Equivariant per-point | Preserve equivariance to output |
| Force prediction | Equivariant vector | Output as l=1 irrep |
| Pose estimation | Equivariant transform | Output rotation + translation |
| Generation | Equivariant structure | Equivariant decoder |

## Layer Patterns

### Equivariant Convolution Patterns

**Standard G-Convolution**:
```
(f ⋆ ψ)(g) = ∫_G f(h) ψ(g⁻¹h) dh
```
- Input: Feature map on group G
- Kernel: Function on G
- Output: Feature map on G

**Steerable Convolution**:
- Uses steerable kernels that transform predictably
- Parameterized by irreducible representations
- More efficient for continuous groups

**e3nn Tensor Product Layer**:
```python
# Combine features with different angular momenta
tp = o3.FullyConnectedTensorProduct(
    irreps_in1, irreps_in2, irreps_out
)
output = tp(input1, input2)
```

### Equivariant Nonlinearities

**Problem**: Standard nonlinearities (ReLU and friends) break equivariance.

**Solutions**:

| Type | How It Works | When to Use |
|------|--------------|-------------|
| Norm-based | Apply nonlinearity to ||x|| | Scalars, invariant features |
| Gated | Use invariant to gate equivariant | General purpose |
| Tensor product | Nonlinearity via Clebsch-Gordan | e3nn, high-quality |
| Invariant features | Only apply to l=0 components | Simple, fast |

### Equivariant Normalization

**Batch Norm**: breaks equivariance (different statistics per orientation)
**Solutions**:
- Layer Norm (normalize per sample)
- Equivariant Batch Norm (normalize per irrep channel)
- Instance Norm (often fine)

### Pooling for Invariance

To get an invariant output from equivariant features:

| Method | Formula | When to Use |
|--------|---------|-------------|
| Mean pooling | mean over group | Continuous groups |
| Sum pooling | sum over elements | Sets, graphs |
| Max pooling | max ||x|| | Discrete groups |
| Attention pooling | weighted sum | When importance varies |

## Topology Patterns

### Encoder-Decoder (Segmentation, Generation)

```
Input → [Equiv. Encoder] → Latent (equiv.) → [Equiv. Decoder] → Output
```
- Encoder: progressive feature extraction
- Latent: equivariant representation
- Decoder: reconstruct with symmetry

### Encoder-Pooling (Classification)

```
Input → [Equiv. Encoder] → Features (equiv.) → [Invariant Pool] → [MLP] → Class
```
- Pool at the end to get invariant features
- The final MLP operates on the invariant representation

### Message Passing (Graphs/Point Clouds)

```
Nodes → [MP Layer 1] → [MP Layer 2] → ... → [Aggregation] → Output
```
- Each layer: aggregate neighbors, update node
- Aggregation: sum/mean for invariance, per-node for equivariance

## Library Reference

### e3nn (PyTorch)

**Groups**: E(3), O(3), SO(3)
**Strengths**: Full irrep support, tensor products, spherical harmonics
**Use for**: Molecular modeling, 3D point clouds, physics

```python
from e3nn import o3
irreps = o3.Irreps("2x0e + 2x1o + 1x2e")  # 2 scalars, 2 vectors, 1 tensor
```

### escnn (PyTorch)

**Groups**: Discrete groups (Cₙ, Dₙ), continuous 2D (SO(2), O(2))
**Strengths**: Image processing, well documented
**Use for**: 2D images with rotation/reflection symmetry

```python
from escnn import gspaces, nn
gspace = gspaces.rot2dOnR2(N=4)  # C4 rotation group
```

### pytorch_geometric (PyTorch)

**Groups**: Permutation (Sₙ)
**Strengths**: Graphs, batching, many GNN layers
**Use for**: Graph classification/regression, node prediction

```python
from torch_geometric.nn import GCNConv, global_mean_pool
```

### Other Libraries

| Library | Groups | Framework | Notes |
|---------|--------|-----------|-------|
| NequIP | E(3) | PyTorch | Molecular dynamics |
| MACE | E(3) | PyTorch | Molecular potentials |
| jraph | Sₙ | JAX | Graph networks |
| geomstats | Lie groups | NumPy/PyTorch | Manifold learning |

## Pitfalls

- ReLU, sigmoid, or tanh applied to vector (l ≥ 1) features breaks equivariance. Use gated or norm-based nonlinearities, or apply the nonlinearity only to scalar (l = 0) channels.
- BatchNorm computes orientation-dependent statistics. Use LayerNorm, instance norm, or the library's per-irrep equivariant norm.
- Irreps mismatch: the output irreps of each layer must equal the input irreps of the next. Print them during construction rather than trusting the plan.
- Pooling too early: once features are pooled to invariants, orientation information is gone. Pool at the point where the task stops needing it.
- Zero padding breaks translation and rotation equivariance at image borders. Use circular or replicate padding, or crop the output to the valid region.
- Enforcing exact equivariance for a symmetry that validation rated weak or approximate. A soft penalty or augmentation may be the better fit; the validation report says which.
- Guessing library APIs from memory. Irreps notation, class names, and gate signatures differ across e3nn and escnn versions; check the docs.

## Output Template

```
ARCHITECTURE SPECIFICATION
==========================

Target Symmetry: [Group name and notation]
Symmetry Type: [Invariant/Equivariant]
Task: [Classification/Regression/etc.]
Domain: [Images/Point clouds/Graphs/etc.]

Architecture Family: [e.g., E(3) Equivariant GNN]
Library: [e.g., e3nn]

Layer Specification:
1. Input Layer
   - Input type: [e.g., 3D coordinates + features]
   - Representation: [e.g., positions (l=1) + scalars (l=0)]

2. [Layer Name]
   - Type: [Convolution/Tensor Product/Message Passing]
   - Input irreps: [specification]
   - Output irreps: [specification]
   - Nonlinearity: [Gated/Norm/None]

3. [Continue for each layer...]

N. Output Layer
   - Aggregation: [Mean/Sum/Attention]
   - Output: [Invariant scalar / Equivariant vector / etc.]

Estimated Parameters: [count]
Key Dependencies: [library versions]

Code Skeleton:
[Provide implementation outline or pseudo-code]

NEXT STEPS:
- Implement the architecture using the specified library
- Verify equivariance through numerical testing after implementation
```

## Verification

On paper, before anyone implements, walk the layer stack and check four things. Each layer's output representation equals the next layer's input representation. Every nonlinearity acts only on invariant quantities or through a gate. No normalization mixes orientations. The final pooling matches the required output type (invariant scalar versus equivariant vector). The specification should also pass the checklist at the end of `references/methodology.md`.

In code, as soon as a skeleton runs, execute a quick equivariance check with `terminal`. The `quick_equivariance_check` function is in the test templates of `model-equivariance-auditor`; load that skill with `skill_view` to get it:

```python
err = quick_equivariance_check(model, x, in_transform, out_transform, n=20)
assert err < 1e-4, f"design leaks equivariance: max error {err:.2e}"
```

A max relative error below 1e-4 in float32 passes; anything above 1e-2 means a layer in the specification is wrong, not the implementation.
