---
name: stage-terraform-provider-repro
description: Stage durable Terraform-side repros for bridged-provider issues. Use when triage selects Terraform behavior as the decisive discriminator, an upstream acceptance-style repro is needed, or the user asks for a Terraform repro.
---

# Stage Terraform Provider Repro

Stage the sharpest Terraform-side discriminator (HCL config or upstream TF acceptance test) for a bridged-provider issue.

---

## Terraform Repro Pipeline

| Step | Objective | Execution Guideline |
| :--- | :--- | :--- |
| **1. Define Discriminator Question** | Target Question | State exact question (e.g. *"Does TF reproduce the same read failure with `-refresh=false`?"*). |
| **2. Select Artifact Surface** | Native Surface | Prefer upstream TF acceptance tests or repo-native TF test configs over scratch temp files. |
| **3. Preserve Semantic Flags** | Execution Mode | Preserve flags (`-refresh=false`, `terraform import`, read-after-update) explicitly. |
| **4. Minimal Config** | Input Minimization | Keep HCL config minimal without erasing the target behavior. |
| **5. Stage & Document** | Deliverable Stage | Stage artifact locally; list exact `terraform` CLI commands to execute. |

---

## Discriminator Checklist

- [ ] **Upstream Harness:** If the upstream provider repository has an acceptance testing harness, use it over custom wrappers.
- [ ] **Semantic Equivalence:** Verify the TF repro matches the exact multi-step lifecycle reported in Pulumi.
- [ ] **Credential Fallback:** If credentials are missing, leave ready-to-run HCL/go test files and exact CLI commands.

---

## Deliverable Artifact Format

```markdown
## Staged Terraform Repro Artifact

- **Discriminator Question:** <Question being answered by TF execution>
- **Staged File:** `<path/to/repro.tf>` or `<path/to/acc_test.go>`
- **Execution Command:** `terraform apply` or `go test -run TestAcc...`
- **Settled vs Unsettled:** <What TF execution proves vs what remains open>
```
