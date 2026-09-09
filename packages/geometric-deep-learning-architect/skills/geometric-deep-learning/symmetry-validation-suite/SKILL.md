---
name: symmetry-validation-suite
description: Test empirically whether hypothesized symmetries hold.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: geometric-deep-learning
    tags: [Symmetry, Invariance Testing, Equivariance Testing, Validation, Geometric Deep Learning]
    related_skills: [symmetry-discovery-questionnaire, symmetry-group-identifier, model-equivariance-auditor]
---
# Symmetry Validation Suite

Provides test protocols and metrics for checking whether hypothesized symmetries actually hold in data or in a model, before anyone commits to an equivariant architecture. It covers invariance and equivariance tests, group structure verification, and distribution analysis under transforms. Wrong symmetry assumptions hurt: too much symmetry over-constrains, missing symmetry wastes capacity. This skill validates hypotheses; auditing a finished implementation layer by layer is `model-equivariance-auditor`.

## When to Use

- Testing invariance or validating equivariance of a dataset, a labeling function, or a candidate model.
- Checking symmetry assumptions that came out of discovery with Medium or Low confidence.
- Debugging symmetry-related model failures, when it is unclear whether the data or the model is at fault.
- Needing data-driven validation before architecture decisions (Phase 2 of the pipeline).
- Deciding between a hard equivariance constraint, a soft constraint, augmentation, or no symmetry at all.

## Procedure

Copy this checklist and track it with `todo`:

```
Symmetry Validation Progress:
- [ ] Step 1: List symmetry hypotheses to test
- [ ] Step 2: Design transformation test sets
- [ ] Step 3: Run invariance/equivariance tests
- [ ] Step 4: Verify group structure
- [ ] Step 5: Analyze data distribution under transforms
- [ ] Step 6: Document validation results
```

**Step 1: List symmetry hypotheses to test**

Gather candidate symmetries from the discovery work. For each, record the transformation type, whether invariance or equivariance is expected, and the confidence level. Test low-confidence hypotheses first. If no hypotheses exist, run `symmetry-discovery-questionnaire` with the user before testing anything.

**Step 2: Design transformation test sets**

For each symmetry, write a test protocol: sample representative inputs from the data distribution; define the transformation sampling strategy (random rotations, all permutations, and so on); pick sample sizes that give statistical significance; include edge cases and boundary conditions. See [Transformation Sampling](#transformation-sampling). For the design principles, load `skill_view("symmetry-validation-suite", file_path="references/methodology.md")`.

**Step 3: Run invariance/equivariance tests**

For invariance: apply transformation T to input x, compute f(x) and f(T(x)), and measure ||f(T(x)) - f(x)||. For equivariance: compute f(T(x)) and T'(f(x)), where T' is the output transformation, and measure ||f(T(x)) - T'(f(x))||. Use the [Testing Protocols](#testing-protocols). Read the user's data loader or model with `read_file` first so the transforms match the tensor layout, write the test script with `write_file`, and run it with `terminal` in the user's environment. Aggregate across samples and report statistics. For complete, runnable examples (C4 images, SO(3) point clouds, graph permutation, E(3) forces, group structure), load `skill_view("symmetry-validation-suite", file_path="references/test-examples.md")`.

**Step 4: Verify group structure**

Check that the claimed transformations form a group: closure (composing two transforms gives a transform), associativity, an identity element, and inverses. For Lie groups, check that the generators close under the commutator. See [Group Structure Tests](#group-structure-tests).

**Step 5: Analyze data distribution under transforms**

Check that transformed data stays in-distribution: apply the transforms to training data, compare statistics of original versus transformed data, look for distributional shift that would break the assumption, and identify the transformation range within which validity holds. This is what catches "approximate symmetry", where the symmetry holds only within bounds.

**Step 6: Document validation results**

Write the report with the [Output Template](#output-template). For each symmetry: hypothesis, test method, quantitative results, pass/fail decision. Recommend a hard equivariance constraint, a soft constraint (regularization), data augmentation, or no symmetry. Quality criteria are in `assets/evaluators/rubric_validation.json`.

## Testing Protocols

### Invariance Test Protocol

```python
def test_invariance(model, data_samples, transform_fn, n_transforms=100):
    """
    Test if model output is invariant to transformations.

    Returns:
        mean_error: Average ||f(T(x)) - f(x)||
        max_error: Maximum error observed
        pass_rate: Fraction with error < threshold
    """
    errors = []
    for x in data_samples:
        y_orig = model(x)
        for _ in range(n_transforms):
            x_transformed = transform_fn(x)
            y_transformed = model(x_transformed)
            error = norm(y_transformed - y_orig)
            errors.append(error)

    return {
        'mean_error': mean(errors),
        'max_error': max(errors),
        'std_error': std(errors),
        'pass_rate': sum(e < threshold for e in errors) / len(errors)
    }
```

### Equivariance Test Protocol

```python
def test_equivariance(model, data_samples, input_transform, output_transform):
    """
    Test if f(T(x)) = T'(f(x)) for equivariance.

    Returns:
        mean_error: Average ||f(T(x)) - T'(f(x))||
        relative_error: Error normalized by output magnitude
    """
    errors = []
    for x in data_samples:
        # Method 1: Transform then model
        x_T = input_transform(x)
        y1 = model(x_T)

        # Method 2: Model then transform
        y = model(x)
        y2 = output_transform(y)

        error = norm(y1 - y2)
        relative = error / (norm(y2) + eps)
        errors.append({'absolute': error, 'relative': relative})

    return aggregate_stats(errors)
```

### Statistical Significance

For reliable results:
- Use at least 100 data samples
- Test at least 50 random transformations per sample
- Report mean, std, and percentiles (95th, 99th)
- Set the threshold from numerical precision expectations
- Use hypothesis testing when comparing methods

## Transformation Sampling

### Continuous Groups

| Group | Sampling Strategy |
|-------|-------------------|
| SO(2) | Uniform random angles θ ∈ [0, 2π) |
| SO(3) | Uniform random quaternions or axis-angle |
| SE(3) | Combine SO(3) rotation + uniform translation |
| Translations | Uniform within expected data range |

### Discrete Groups

| Group | Sampling Strategy |
|-------|-------------------|
| Cₙ | All n rotations |
| Dₙ | All 2n elements (rotations + reflections) |
| Sₙ | Random permutations (full enumeration if n ≤ 6) |

## Group Structure Tests

### Closure Test

```
For random g₁, g₂ ∈ G:
  Compute g₃ = g₁ · g₂
  Verify g₃ ∈ G (within numerical tolerance)
```

### Associativity Test

```
For random g₁, g₂, g₃ ∈ G:
  Compute (g₁ · g₂) · g₃
  Compute g₁ · (g₂ · g₃)
  Verify equality (within tolerance)
```

### Identity and Inverse Test

```
For random g ∈ G:
  Verify g · e = e · g = g
  Find g⁻¹ and verify g · g⁻¹ = e
```

## Interpretation Guide

### Error Thresholds

| Error Level | Interpretation |
|-------------|----------------|
| < 1e-6 | Exact symmetry (numerical precision) |
| 1e-6 to 1e-3 | Strong approximate symmetry |
| 1e-3 to 0.01 | Weak approximate symmetry |
| > 0.01 | Symmetry likely does not hold |

### Decision Matrix

| Validation Result | Recommendation |
|-------------------|----------------|
| Exact symmetry confirmed | Use hard equivariant constraint |
| Strong approximate | Use equivariant architecture |
| Weak approximate | Consider soft constraint or augmentation |
| Symmetry broken | Do not enforce this symmetry |
| Partial symmetry | Use conditional/local equivariance |

## Pitfalls

- Too few samples or transforms: a mean over ten cases hides the tail. Report percentiles and the max.
- Threshold not matched to precision: float32 arithmetic alone gives errors near 1e-6. Rerun in float64 to separate precision from real breakage before calling a symmetry "weak".
- Sampling only near the identity: small rotations pass where large ones fail. Sample the whole group, and include the reflections when the hypothesis is O(3) or E(3).
- Measuring the model when you meant the data: running the invariance test on a trained network measures that network. To validate a data symmetry, test label or target consistency across transforms of the raw data.
- Interpolation artifacts: rotating images by angles that are not multiples of 90° resamples pixels and produces error that looks like broken symmetry. Test the discrete subgroup exactly and the continuous group with a tolerance that accounts for resampling.

## Output Template

```
SYMMETRY VALIDATION REPORT
==========================

Tested Symmetries:

1. [Transformation]: [Invariance/Equivariance]
   - Sample size: [N samples × M transforms]
   - Mean error: [value]
   - Max error: [value]
   - Pass rate: [%] at threshold [value]
   - RESULT: [PASS/FAIL/PARTIAL]
   - Recommendation: [Hard constraint/Soft/Augmentation/None]

2. [Transformation]: [Invariance/Equivariance]
   ...

Group Structure:
- Closure: [PASS/FAIL]
- Associativity: [PASS/FAIL]
- Identity/Inverse: [PASS/FAIL]

Distribution Analysis:
- Transform range where symmetry holds: [bounds]
- Detected breaking factors: [list]

SUMMARY:
- Confirmed symmetries: [list]
- Rejected symmetries: [list]
- Proceed to architecture design with: [group specification]
```

## Verification

Sanity-check the harness before trusting any verdict, with two controls run through `terminal`:

```python
# 1. Identity control: must give error 0 to numerical precision.
identity = test_invariance(f, samples, transform_fn=lambda x: x)
assert identity['max_error'] < 1e-6

# 2. Broken control: a deliberately asymmetric function must FAIL.
#    e.g. under random rotation, f(x) = x[..., 0] (the raw x-coordinate)
broken = test_invariance(lambda x: x[..., 0], samples, transform_fn=random_rotate)
assert broken['max_error'] > 1e-2
```

If the identity control is not zero, the transform or the norm is wrong. If the broken control passes, the sampled transforms are too small or the metric is blind to the change. Only after both controls behave do the results for the real hypotheses mean anything.
