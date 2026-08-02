---
name: bridge-parity-investigation
description: Investigate established Pulumi-vs-Terraform parity gaps with bridge cross-tests. Use after triage establishes that Pulumi fails while Terraform succeeds and selects bridge parity work, or when the user asks for a bridge cross-test.
---

# Bridge Parity Investigation

Turn an established parity gap into the smallest useful bridge cross-test, and narrow the failing boundary enough that the next pass can reason about root cause or workaround work.

**Precondition:** use this skill only when the issue is already understood as a real parity gap. Pulumi has the problem, Terraform does not, and the bridge is the next evidence surface. If parity is not established, stop and switch back to the appropriate repro skill. Prefer `triage-provider-issue` first unless a prior pass already established the parity gap and selected this helper, or the user invoked this skill directly.

This skill is cross-test-only. Do not spend time debating provider-only tests, generic `pkg/tests`, or other harnesses here.

Stay in the bridge lane. Do not restart broad issue triage unless the cross-test evidence contradicts the established parity story.

Read [`references/cross-test-playbook.md`](references/cross-test-playbook.md) before editing.

## Workflow

1. **Restate the parity gap in one line.** For example: "Pulumi update+read fails, Terraform equivalent path succeeds."
2. **Identify the lifecycle path that must be preserved.** Update then read, refresh, import, diff.
3. **Resolve repository ownership.** If the work belongs in the bridge repository, continue there only when the environment can preserve correct repository and artifact ownership. Otherwise leave a bridge-repository handoff naming the exact cross-test required.
4. **Build or refine the bridge cross-test** around that path.
5. **Preserve the dataflow that matters,** not just the final values.
6. **Instrument the failing boundary narrowly.**
7. **Run the targeted cross-test.**
8. **Record what the test proves and what it still does not prove.**

## Operating Rules

- Do not start unless Terraform behavior is already known.
- Preserve lifecycle shape first, then minimize.
- If a synthetic case is too clean to reproduce the gap, widen only the dataflow you need. Do not copy large chunks of provider business logic.
- If a bridge panic would crash the test process, recover it into an assertable test failure rather than abandoning the cross-test approach.
- Keep the output focused on the parity boundary, not a full implementation theory.
- Showing the parity gap cleanly in a cross-test is success, even if the final root cause is not finished.
- If a focused cross-test still cannot preserve the real discriminator, stop. Record exactly what constraint prevented it and hand control back with that constraint instead of looping on cross-test shaping.

## Deliverable

```markdown
## Bridge Parity Investigation

- **Current State:** <where the cross-test stands>
- **Parity Gap:** <Pulumi behavior vs Terraform behavior>
- **Confidence:** <>=90% / 60-89% / <60%>
- **Settled Facts:** <what the cross-test proves>
- **Unsettled Questions:** <the exact bridge mechanism still under review>
- **Next Best Action:** <concrete next step>
- **Lifecycle Path Preserved:** <operations the test reproduces>
- **Cross-Test File:** `<path/to/bridge_test.go>`
- **Execution Command:** `<go test command>`
- **Narrowed Failing Boundary:** <Pulumi RPC to TF config/state translation point>
- **Blocked Execution & Required Access:** <what could not run and what it needs, or None>
- **Workaround Status:** <mitigation and validation level, or None>
```
