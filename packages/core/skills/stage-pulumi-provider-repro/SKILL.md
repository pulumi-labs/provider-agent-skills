---
name: stage-pulumi-provider-repro
description: Stage durable Pulumi-side repros for provider issues. Use when triage or another skill selects a Pulumi repro as the next evidence artifact, or when the user asks for a maintainer-quality Pulumi example or lifecycle test.
---

# Stage Pulumi Provider Repro

Stage the smallest durable Pulumi-side repro harness that captures the issue across lifecycle operations.

---

## Repro Execution Pipeline

| Step | Focus | Execution Instruction |
| :--- | :--- | :--- |
| **1. Identify Lifecycle Path** | Target Operation | Identify exact path: `create`, `update`, `read`, `refresh`, `import`, `preview`, `diff`, or `replacement`. |
| **2. Select Repro Surface** | Native Placement | Prefer repo-native examples (`examples/`) or Go integration tests over temporary scratch directories. |
| **3. Preserve Lifecycle Sequence** | Multi-Step Integrity | If the issue is update $\rightarrow$ read, do not collapse into a create-only test. |
| **4. Minimize Input Payload** | Smallest Reproduction | Encode the smallest input schema/properties that still reproduce the failure. |
| **5. Stage & Verify** | Execution & Fallback | Run safe local checks. If missing credentials, stop with staged files and exact CLI commands. |

---

## Repro Hygiene Checklist

- [ ] **Committed Artifacts:** Prefer committed-style test files over one-off shell transcripts.
- [ ] **Explicit CLI Flags:** If `--refresh --run-program` is relevant, stage that execution path explicitly.
- [ ] **Version Constraints:** Preserve exact provider versions or local provider overrides required for reproduction.
- [ ] **Relative Citations:** Cite staged files using repo-relative paths (`examples/my_test.go:45`). Never output `file://` sandbox URIs.

---

## Deliverable Artifact Format

```markdown
## Staged Pulumi Repro Artifact

- **Target Behavior:** <Lifecycle path being proven>
- **Staged File:** `<path/to/repro_test.go>`
- **Execution Command:** `<exact go test or pulumi command>`
- **Settled vs Unsettled:** <What this repro proves vs what remains open>
- **Execution Status:** <Executed successfully / Blocked by credentials>
```
