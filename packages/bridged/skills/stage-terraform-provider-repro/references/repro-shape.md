# Terraform Repro Shape

Reference rules for staging durable, minimal Terraform-side repro artifacts.

---

## Repro Principles Matrix

| Category | Guideline |
| :--- | :--- |
| **PRESERVE** | Discriminator question, exact semantic flags (`-refresh=false`, import, read-after-update), HCL config. |
| **PREFER** | Upstream provider acceptance tests (`TestAcc...`) or repo-native TF test configs over temp directories. |
| **AVOID** | Loose temp-dir configs when upstream acceptance tests are needed; assuming TF mismatch without testing. |

---

## Blocked Execution Fallback

If credentials/environment block execution, stage the HCL/Go files anyway and report:
1. Exact command to run (`terraform apply` or `go test -run TestAcc...`).
2. Required cloud credentials or env variables.
3. Discriminator outcome being verified.
