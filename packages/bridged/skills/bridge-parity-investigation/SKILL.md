---
name: bridge-parity-investigation
description: Investigate established Pulumi-vs-Terraform parity gaps with bridge cross-tests. Use after triage establishes that Pulumi fails while Terraform succeeds and selects bridge parity work, or when the user asks for a bridge cross-test.
---

# Bridge Parity Investigation

Turn an established parity gap into the smallest useful bridge cross-test and narrow the failing boundary.

This skill is cross-test-only. Prefer `triage-provider-issue` first unless a prior pass selected bridge parity work or the user explicitly requested a cross-test.

Read [`references/cross-test-playbook.md`](references/cross-test-playbook.md) before editing. Its entry gate is mandatory; if the gate fails, switch to the appropriate repro skill.

## Workflow

1. **Resolve repository ownership.** If the work belongs in the bridge repository, continue there only when the environment can preserve correct repository and artifact ownership. Otherwise leave a bridge-repository handoff naming the exact cross-test required.
2. **Build or refine the cross-test** around the established lifecycle and dataflow.
3. **Instrument the first divergence narrowly and run the targeted test.**
4. **Record the observed result, narrowed boundary, and remaining question.**

## Operating Rules

- Showing the parity gap cleanly is success even when the final root cause remains unknown.
- If a focused cross-test cannot preserve the real discriminator, stop and report the blocking constraint instead of widening indefinitely.

## Deliverable

```markdown
## Bridge Parity Investigation

- **Parity Gap:** <Pulumi behavior vs Terraform behavior>
- **Lifecycle Path:** <operations preserved by the test>
- **Cross-Test Files:** <repository-relative paths>
- **Execution Command:** <exact `go test` command>
- **Execution Status:** <not run / completed / blocked / failed before the discriminator>
- **Observed Result:** <parity gap reproduced / not reproduced / inconclusive / None if not reached>
- **Narrowed Failing Boundary:** <first Pulumi RPC to Terraform translation divergence>
- **Remaining Question:** <bridge mechanism still under review>
- **Next Best Action:** <concrete next step>
- **Blocked Execution & Required Access:** <what could not run and what it needs, or None>
```

Do not claim a parity result from an unexecuted cross-test.
