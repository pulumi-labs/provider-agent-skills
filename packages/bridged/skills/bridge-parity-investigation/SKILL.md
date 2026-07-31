---
name: bridge-parity-investigation
description: Investigate established Pulumi-vs-Terraform parity gaps with bridge cross-tests. Use after triage establishes that Pulumi fails while Terraform succeeds and selects bridge parity work, or when the user asks for a bridge cross-test.
---

# Bridge Parity Investigation

Investigate established parity gaps where **Pulumi fails while Terraform succeeds**, isolating the root cause to the bridge translation layer (see [`references/cross-test-playbook.md`](references/cross-test-playbook.md)).

> ⚠️ **Precondition:** Use this skill **only** after parity status is established (Pulumi behavior known, Terraform behavior known). Read [`references/cross-test-playbook.md`](references/cross-test-playbook.md) before editing.

---

## Parity Cross-Test Pipeline

| Step | Objective | Execution Guideline |
| :--- | :--- | :--- |
| **1. Parity Gap Statement** | Define Divergence | Restate divergence clearly (e.g. *"Pulumi update+read fails; TF equivalent path succeeds"*). |
| **2. Lifecycle Preservation** | Match Path | Preserve exact multi-step path (e.g. `update` $\rightarrow$ `read`, `refresh`, `import`, `diff`). |
| **3. Bridge Cross-Test** | Build Test | Build targeted bridge cross-test in bridge test harness (`pkg/tests`). |
| **4. Dataflow Isolation** | Instrument Boundary | Instrument failing boundary (Pulumi RPC $\leftrightarrow$ TF Schema/State conversion). |
| **5. Panic Recovery** | Test Stability | If bridge panics occur, recover into assertable test failures (`assert.Panics`). |

---

## Operating Rules

- [ ] **Terraform Behavior Required:** Do not start unless Terraform behavior has already been verified.
- [ ] **Preserve Dataflow:** Test dataflow translation, not just final state values.
- [ ] **Bridge Scope:** Keep focus strictly on the bridge translation boundary.
- [ ] **Clear Failure Ownership:** Proving the parity gap cleanly in a cross-test constitutes success even if final root-cause fix is pending.

---

## Deliverable Artifact Format

```markdown
## Bridge Parity Investigation

- **Parity Gap:** <Pulumi behavior vs Terraform behavior>
- **Lifecycle Path:** <Preserved operations>
- **Cross-Test File:** `<path/to/bridge_test.go>`
- **Execution Command:** `<go test command>`
- **Failing Boundary:** <Pulumi RPC -> TF Config/State translation point>
- **Unresolved Bridge Question:** <Exact bridge mechanism under review>
```
