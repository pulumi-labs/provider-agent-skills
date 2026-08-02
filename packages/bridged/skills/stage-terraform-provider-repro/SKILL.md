---
name: stage-terraform-provider-repro
description: Stage durable Terraform-side repros for bridged-provider issues. Use when triage selects Terraform behavior as the decisive discriminator, an upstream acceptance-style repro is needed, or the user asks for a Terraform repro.
---

# Stage Terraform Provider Repro

Stage the sharpest Terraform-side discriminator for the issue: an HCL config or an upstream acceptance test.

Prefer durable upstream or repo-native artifacts over disposable local experiments. When a temporary config is useful as a quick check, treat it as a probe, not the final repro artifact.

Stay in the repro lane. Do not drift back into broad routing or bridge-theory work unless the Terraform result directly changes the question. Prefer `triage-provider-issue` first unless a prior pass already established that a Terraform repro is the next best action, or the user invoked this skill directly.

Read [`references/repro-shape.md`](references/repro-shape.md) before editing.

## Workflow

1. **State the exact question Terraform needs to answer.** For example: does Terraform reproduce the same read failure? Does the issue disappear with `-refresh=false`? Is this accepted upstream behavior?
2. **Choose the strongest durable artifact available.** Prefer upstream acceptance tests or the closest durable Terraform repro in the relevant repo.
3. **Preserve the exact discriminator.** If refresh semantics matter, stage that explicitly.
4. **Keep the config minimal,** but not so minimal that it erases the behavior.
5. **Resolve repository ownership.** If the repro surface lives in another repository, continue there only when the environment can preserve correct repository and artifact ownership. Otherwise leave a repository-scoped handoff naming the exact artifact required.
6. **Stage the artifact locally and run only what is safe and available.**
7. **If credentials or approvals are missing,** stop with a ready-to-run artifact and exact commands.

## Operating Rules

- Do not substitute a loose temp-dir config when the real next step is an upstream acceptance-style repro.
- Preserve semantic variants intentionally, including `-refresh=false`, import, or read-after-update behavior. Change one semantic variable at a time.
- Treat "Terraform did not reproduce" as a meaningful result only when the repro actually matches the question being asked. Do not make vague "Terraform works" claims without stating what was exercised.
- If the upstream repo has a testing harness, use it instead of inventing a new convention.
- Verify the Terraform repro matches the exact multi-step lifecycle reported in Pulumi.

## Deliverable

```markdown
## Staged Terraform Repro

- **Current State:** <what is staged and whether it ran>
- **Discriminator Question:** <what TF execution answers>
- **Confidence:** <>=90% / 60-89% / <60%>
- **Settled Facts:** <what TF execution proves>
- **Unsettled Questions:** <what remains open>
- **Next Best Action:** <concrete next step>
- **Staged File:** `<path/to/repro.tf>` or `<path/to/acc_test.go>`
- **Command Matrix:** `terraform apply` / `go test -run TestAcc...`
- **Result That Would Change Routing:** <the counterfactual outcome>
- **Blocked Execution & Required Access:** <what could not run and what it needs, or None>
- **Workaround Status:** <mitigation and validation level, or None>
```
