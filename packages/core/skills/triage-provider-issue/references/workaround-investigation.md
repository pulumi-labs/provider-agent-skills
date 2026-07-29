# Workaround Investigation

Protocol for finding, validating, and reporting temporary mitigations when ownership boundary is clear but official fix is pending.

---

## Search Hierarchy (Narrowest to Broadest)

1. **Config / Usage Change:** Resource input property adjustment or explicit program workaround.
2. **Lifecycle Option / CLI Flag:** Invocation options (e.g. `--refresh=false`, `ignoreChanges`, `replaceOnChanges`).
3. **Narrow Normalization Guard:** Local state/input override.
4. **Alternate Resource Flow:** Alternative Pulumi component or SDK construct.
5. **Upstream / Bridge Patch:** Upstream provider or bridge override.

---

## Validation Level Matrix

| Validation Level | Definition | Reporting Rule |
| :--- | :--- | :--- |
| **Idea Only** | Conceptual workaround; unverified locally | **Do not** present as verified. |
| **Locally Staged** | Workaround code written in test file | Staged in local repro. |
| **Locally Validated** | Executed cleanly in local test harness | Confirmed locally. |
| **Real Path Validated** | Verified against real cloud/provider failure path | Verified end-to-end workaround. |

---

## Workaround Deliverable Template

```markdown
## Workaround Summary

- **Target Behavior Avoided:** <Exact bug/failure being suppressed>
- **Best Candidate:** <Description of recommended mitigation>
- **Validation Level:** <Idea Only / Locally Staged / Locally Validated / Real Path Validated>
- **User Impact & Tradeoffs:** <Limitations introduced by workaround>
- **Next Validation Step:** <How user or maintainer can verify>
```
