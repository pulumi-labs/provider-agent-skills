# Pulumi Repro Shape

Keeping Pulumi repro work durable and narrow.

| Category | Guideline |
| :--- | :--- |
| Preserve | The exact lifecycle path, the smallest input shape that still matters, the exact failure mode, and any required config, provider version, or local binary wiring. |
| Prefer | Provider repo example programs, provider harness tests, and focused existing test surfaces over new ad hoc scaffolding. |
| Avoid | Temp-dir repros as the main deliverable, simplifying away the lifecycle transition that causes the bug, and broad snapshot assertions when one concrete failure proves the point. |

## If Execution Is Blocked

Stage the repro anyway and report:

1. The exact command to run (`go test ...` or `pulumi up`).
2. The required credentials or environment.
3. The expected signal if the issue reproduces.
