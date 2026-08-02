# Cross-Test Playbook

Constructing targeted bridge cross-tests that isolate a Pulumi-vs-Terraform parity gap.

## Entry Gate

Run a bridge cross-test only when all three hold:

1. Pulumi behavior is established (the bug reproduces).
2. Terraform behavior is established (the TF path succeeds).
3. The mismatch matters for routing or root-cause work.

If any is missing, go back to repro staging first.

## Construction

| Objective | Do | Avoid |
| :--- | :--- | :--- |
| Preserve the lifecycle transition | Recreate the exact multi-step flow that triggers the mismatch (`update` then `read`, `refresh`, `import`). | Collapsing a multi-step flow into a simple `create` test. |
| Preserve dataflow integrity | Keep the smallest schema and raw-state/readback shape that keeps the mismatch alive. | Copying the real provider implementation wholesale into a synthetic test. |
| Recover panics | Recover bridge panics into assertable failures. | Letting a bridge crash take down the test process. |
| Assert narrowly | Assert the specific translation failure point, and the exact user-visible divergence. | Broad, non-specific assertions or large synthetic harnesses. |

Add minimal instrumentation around the failing boundary. Prefer one precise cross-test over a large synthetic harness.

## Diagnostic Questions

- Which lifecycle stage is the first point of divergence?
- Is the problem in request construction, state translation, or output projection?
- Does the synthetic test preserve the same raw-state or readback shape that matters in the real issue?

## Avoid

- Falling back to non-cross-test harnesses once parity is established.
- Claiming the final root cause before the test actually isolates it.
