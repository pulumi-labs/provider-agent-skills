# Pulumi Repro Shape

Reference rules for staging durable, minimal Pulumi provider repro artifacts.

---

## Repro Principles Matrix

| Category | Guideline |
| :--- | :--- |
| **PRESERVE** | Exact lifecycle path, smallest input shape, failure mode, provider version, & binary overrides. |
| **PREFER** | Repo-native example programs (`examples/`), provider test harness over ad hoc scaffolding. |
| **AVOID** | One-off temp-dir repros, simplifying away bug-causing lifecycle transitions, broad snapshot assertions. |

---

## Blocked Execution Fallback

If credentials/environment block test execution, stage the repro files anyway and report:
1. Exact command to run (`go test ...` or `pulumi up`).
2. Required credentials or environment variables.
3. Expected failure signal when issue reproduces.
