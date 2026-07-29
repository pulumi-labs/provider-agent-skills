# Cross-Test Playbook

Playbook for constructing targeted bridge cross-tests to isolate Pulumi vs. Terraform parity gaps.

---

## Entry Gate Requirements

Execute a bridge cross-test **only** when:
1. Pulumi behavior is established (bug reproduced).
2. Terraform behavior is established (TF path succeeds).
3. Parity mismatch matters for routing or root-cause work.

---

## Cross-Test Construction Matrix

| Objective | Execution Guideline | Anti-Pattern (AVOID) |
| :--- | :--- | :--- |
| **Preserve Lifecycle Transition** | Recreate exact multi-step flow (`update` $\rightarrow$ `read`, `refresh`, `import`). | Collapsing multi-step flow into a simple `create` test. |
| **Dataflow Integrity** | Preserve raw-state and readback schema shapes. | Copying wholesale provider business logic into synthetic test. |
| **Panic Recovery** | Recover bridge panics into assertable failures (`assert.Panics`). | Allowing bridge crashes to fail the test process. |
| **Focused Assertion** | Assert specific translation failure point. | Relying on broad non-specific test assertions. |
