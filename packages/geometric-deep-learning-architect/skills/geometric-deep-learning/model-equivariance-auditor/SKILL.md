---
name: model-equivariance-auditor
description: Verify and debug equivariance in an implemented model.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: geometric-deep-learning
    tags: [Equivariance Testing, Model Verification, Debugging, PyTorch, Geometric Deep Learning]
    related_skills: [symmetry-validation-suite, equivariant-architecture-designer, readability-check]
---
# Model Equivariance Auditor

Checks that an implemented neural network really respects the symmetry it claims. It runs end-to-end numerical equivariance tests, isolates layers one by one to find the offending module, and tests gradients so training does not unlearn the symmetry. Even with equivariant libraries, implementation bugs break equivariance. A model that claims equivariance but lacks it trains poorly and predicts inconsistently. It audits code that exists; it does not decide whether the symmetry was the right one (that is `symmetry-validation-suite`).

## When to Use

- Testing model equivariance or checking if a model is actually equivariant after implementation.
- Debugging symmetry bugs, or diagnosing why an equivariant model isn't working (unstable training, predictions that change under rotation).
- Verifying implementation correctness after an architecture change, a dependency upgrade, or a performance optimization.
- Phase 5 of the geometric deep learning pipeline, once the design from `equivariant-architecture-designer` has been implemented.
- Not for datasets or hypotheses without code; use `symmetry-validation-suite` for those.

## Procedure

Copy this checklist and track it with `todo`:

```
Equivariance Audit Progress:
- [ ] Step 1: Gather model and symmetry specification
- [ ] Step 2: Run numerical equivariance tests
- [ ] Step 3: Test individual layers
- [ ] Step 4: Check gradient equivariance
- [ ] Step 5: Identify and diagnose failures
- [ ] Step 6: Document audit results
```

**Step 1: Gather model and symmetry specification**

Collect the implemented model, the intended symmetry group, whether each output should be invariant or equivariant, and the transformation functions for the input and output spaces. Read the model code with `read_file`. Use `search_files` to locate custom layers, normalization, padding, and any reshaping that could mix representation channels. Review the architecture specification from the design phase. Clarify ambiguities with the user (`clarify`) before testing.

**Step 2: Run numerical equivariance tests**

Run the end-to-end tests in [Test Implementation](#test-implementation). For invariance, verify ||f(T(x)) - f(x)|| < ε. For equivariance, verify ||f(T(x)) - T'(f(x))|| < ε. Use several random inputs and transformations and record error statistics. Thresholds are in [Error Interpretation](#error-interpretation). Write the test file with `write_file` from `skill_view("model-equivariance-auditor", file_path="templates/test-templates.md")` (a complete audit suite with SO(3), SE(3), and permutation auditors, quick checks, and pytest integration) and run it with `terminal` in the user's environment.

**Step 3: Test individual layers**

If the end-to-end test fails, isolate the problem by testing layers one at a time: for each layer, test its equivariance alone, holding the rest fixed. This names the layer that breaks equivariance. Use the [Layer-wise Testing](#layer-wise-testing) protocol; look hardest at nonlinearities, normalizations, and custom operations.

**Step 4: Check gradient equivariance**

Verify that gradients respect equivariance too, since training depends on it. Compute gradients at x and at T(x) and check that they transform as they should. Gradient bugs make training "unlearn" equivariance. See [Gradient Testing](#gradient-testing).

**Step 5: Identify and diagnose failures**

Diagnose failures with [Common Failure Modes](#common-failure-modes): non-equivariant nonlinearities, batch normalization, an output transformation that does not match the output representation, numerical precision, bugs in custom layers, padding. Give a specific fix for each. For the step-by-step troubleshooting workflow, including binary search over large models and a regression test to add after the fix, load `skill_view("model-equivariance-auditor", file_path="references/debugging.md")`.

**Step 6: Document audit results**

Write the report with the [Output Template](#output-template). Include pass/fail per test, error magnitudes, identified issues, and recommendations. Distinguish exact equivariance (numerical precision), approximate equivariance (acceptable error), and broken equivariance (needs fixing). For the full auditing framework, threshold calibration, and CI integration, load `skill_view("model-equivariance-auditor", file_path="references/methodology.md")`. Quality criteria are in `assets/evaluators/rubric_audit.json`.

## Test Implementation

### End-to-End Equivariance Test

```python
import torch

def test_model_equivariance(model, x, input_transform, output_transform,
                            n_tests=100, tol=1e-5):
    """
    Test if model is equivariant: f(T(x)) ≈ T'(f(x))

    Args:
        model: The neural network to test
        x: Sample input tensor
        input_transform: Function that transforms input
        output_transform: Function that transforms output
        n_tests: Number of random transformations to test
        tol: Error tolerance

    Returns:
        dict with test results
    """
    model.eval()
    errors = []

    with torch.no_grad():
        for _ in range(n_tests):
            # Generate random transformation
            T = sample_random_transform()

            # Method 1: Transform input, then apply model
            x_transformed = input_transform(x, T)
            y1 = model(x_transformed)

            # Method 2: Apply model, then transform output
            y = model(x)
            y2 = output_transform(y, T)

            # Compute error
            error = torch.norm(y1 - y2).item()
            relative_error = error / (torch.norm(y2).item() + 1e-8)
            errors.append({
                'absolute': error,
                'relative': relative_error
            })

    return {
        'mean_absolute': np.mean([e['absolute'] for e in errors]),
        'max_absolute': np.max([e['absolute'] for e in errors]),
        'mean_relative': np.mean([e['relative'] for e in errors]),
        'max_relative': np.max([e['relative'] for e in errors]),
        'pass': all(e['relative'] < tol for e in errors)
    }
```

### Invariance Test (Simpler Case)

```python
def test_model_invariance(model, x, transform, n_tests=100, tol=1e-5):
    """Test if model output is invariant to transformations."""
    model.eval()
    errors = []

    with torch.no_grad():
        y_original = model(x)

        for _ in range(n_tests):
            T = sample_random_transform()
            x_transformed = transform(x, T)
            y_transformed = model(x_transformed)

            error = torch.norm(y_transformed - y_original).item()
            errors.append(error)

    return {
        'mean_error': np.mean(errors),
        'max_error': np.max(errors),
        'pass': max(errors) < tol
    }
```

## Layer-wise Testing

### Protocol

```python
def test_layer_equivariance(layer, x, input_transform, output_transform):
    """Test a single layer for equivariance."""
    layer.eval()

    with torch.no_grad():
        T = sample_random_transform()

        # Transform then layer
        y1 = layer(input_transform(x, T))

        # Layer then transform
        y2 = output_transform(layer(x), T)

        error = torch.norm(y1 - y2).item()

    return {
        'layer': layer.__class__.__name__,
        'error': error,
        'pass': error < tolerance
    }

def audit_all_layers(model, x, transforms):
    """Test each layer individually."""
    results = []

    for name, layer in model.named_modules():
        if is_testable_layer(layer):
            result = test_layer_equivariance(layer, x, *transforms)
            result['name'] = name
            results.append(result)

    return results
```

### What to Test Per Layer

| Layer Type | What to Check |
|------------|---------------|
| Convolution | Kernel equivariance |
| Nonlinearity | Should preserve equivariance |
| Normalization | Often breaks equivariance |
| Pooling | Correct aggregation |
| Linear | Weight sharing patterns |
| Attention | Permutation equivariance |

## Gradient Testing

### Why Test Gradients?

The forward pass can be equivariant while the backward pass is not. This causes:
- Training instability
- The model "unlearning" equivariance
- Inconsistent optimization

### Gradient Equivariance Test

```python
def test_gradient_equivariance(model, x, loss_fn, transform, tol=1e-4):
    """Test if gradients respect equivariance."""
    model.train()

    # Gradients at original input
    x1 = x.clone().requires_grad_(True)
    y1 = model(x1)
    loss1 = loss_fn(y1)
    loss1.backward()
    grad1 = x1.grad.clone()

    # Gradients at transformed input
    model.zero_grad()
    T = sample_random_transform()
    x2 = transform(x.clone(), T).requires_grad_(True)
    y2 = model(x2)
    loss2 = loss_fn(y2)
    loss2.backward()
    grad2 = x2.grad.clone()

    # Transform grad1 and compare to grad2
    grad1_transformed = transform_gradient(grad1, T)
    error = torch.norm(grad2 - grad1_transformed).item()

    return {'error': error, 'pass': error < tol}
```

## Error Interpretation

### Error Thresholds

| Error Level | Interpretation | Action |
|-------------|----------------|--------|
| < 1e-6 | Perfect (float32 precision) | Pass |
| 1e-6 to 1e-4 | Excellent (acceptable) | Pass |
| 1e-4 to 1e-2 | Approximate equivariance | Investigate |
| > 1e-2 | Broken equivariance | Fix required |

Context sets the bar: research prototypes tolerate 1e-3 relative error, production 1e-4, safety-critical 1e-6. Calibrate by measuring a known-good reference implementation and setting the threshold at ten times its baseline error.

### Relative vs Absolute Error

- **Absolute error**: raw difference magnitude
- **Relative error**: normalized by output magnitude

Use relative error when output magnitudes vary. Use absolute error when comparing to numerical precision.

## Common Failure Modes

### 1. Non-Equivariant Nonlinearity

**Symptom**: Error increases after nonlinearity layers
**Cause**: ReLU or sigmoid applied to equivariant features
**Fix**: Use gated or norm-based nonlinearities, or restrict activation to invariant features

### 2. Batch Normalization Breaking Equivariance

**Symptom**: Error varies with batch composition
**Cause**: BN computes different statistics for different orientations
**Fix**: Use LayerNorm, GroupNorm, or an equivariant batch norm

### 3. Incorrect Output Transformation

**Symptom**: Test fails even for the identity transform
**Cause**: output_transform does not match the model's output type
**Fix**: Verify the output transformation matches the output representation

### 4. Numerical Precision Issues

**Symptom**: Small but non-zero error everywhere
**Cause**: Floating point accumulation, interpolation
**Fix**: Test in float64; accept a small tolerance

### 5. Custom Layer Bug

**Symptom**: Error isolated to a specific layer
**Cause**: Implementation error in a custom equivariant layer
**Fix**: Review the layer against the equivariance constraint f(ρ_in(g)x) = ρ_out(g)f(x)

### 6. Padding/Boundary Effects

**Symptom**: Error higher near edges
**Cause**: Padding does not respect the symmetry
**Fix**: Use circular padding or handle boundaries explicitly

## Output Template

```
MODEL EQUIVARIANCE AUDIT REPORT
===============================

Model: [Model name/description]
Intended Symmetry: [Group]
Symmetry Type: [Invariant/Equivariant]

END-TO-END TESTS:
-----------------
Test samples: [N]
Transformations tested: [M]

Invariance/Equivariance Error:
- Mean absolute: [value]
- Max absolute: [value]
- Mean relative: [value]
- Max relative: [value]
- RESULT: [PASS/FAIL]

LAYER-WISE ANALYSIS:
--------------------
[For each layer]
- Layer: [name]
- Error: [value]
- Result: [PASS/FAIL]

GRADIENT TEST:
--------------
- Gradient equivariance error: [value]
- RESULT: [PASS/FAIL]

IDENTIFIED ISSUES:
------------------
1. [Issue description]
   - Location: [layer/component]
   - Severity: [High/Medium/Low]
   - Recommended fix: [description]

OVERALL VERDICT: [PASS/FAIL/NEEDS_ATTENTION]

Recommendations:
- [List of actions needed]
```

## Verification

Run the generated test file with `terminal`:

```bash
python test_equivariance.py          # prints the audit report
pytest test_equivariance.py -v       # or as a test suite
```

Before believing a PASS, prove the harness can fail. Two controls, in the same file:

```python
# Identity control: the identity transform must give zero error.
assert test_model_equivariance(model, x, lambda x, T: x, lambda y, T: y)['max_relative'] < 1e-6

# Broken control: a model known to break equivariance must FAIL.
broken = torch.nn.Sequential(model, torch.nn.ReLU())   # ReLU on vector outputs
assert not test_model_equivariance(broken, x, input_transform, output_transform)['pass']
```

If the identity control is non-zero, the transform functions are wrong (Failure Mode 3). If the broken control passes, the sampled transforms are too small or the output transform is not being applied. After a fix, keep the failing case as a regression test so the bug cannot return silently.
