# Terraform Repro Shape

Keeping Terraform repro work honest and useful for routing.

| Category | Guideline |
| :--- | :--- |
| Preserve | The exact upstream question, the exact lifecycle or flag variant being tested (`-refresh=false`, import, read-after-update), and the smallest durable config or acceptance test that still answers it. |
| Prefer | Upstream acceptance tests (`TestAcc...`), repo-native Terraform repro artifacts, and narrow command matrices tied to explicit outcomes. |
| Avoid | Presenting a convenience config as equivalent to the real discriminator, vague "Terraform works" claims that do not state what was exercised, and changing more than one semantic variable at a time. |

## If Execution Is Blocked

Stage the HCL or Go files anyway and report:

1. The exact command to run (`terraform apply` or `go test -run TestAcc...`).
2. The required cloud credentials, approvals, or environment variables.
3. What result would change routing.
