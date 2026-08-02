# Workaround Investigation

Finding, validating, and reporting a temporary mitigation once the ownership boundary is clear enough for practical purposes and the user still needs a path forward.

Stay in the workaround lane. Reopen broad triage only when workaround evidence contradicts the current understanding.

## Workflow

1. Restate the exact behavior the workaround must avoid, suppress, normalize, or redirect.
2. Search from the narrowest surface to the broadest (see hierarchy below).
3. Compare serious candidates by practicality, user impact, and risk rather than by which owning layer appears conceptually cleaner.
4. Validate the strongest candidate when safe and possible.
5. If validation requires credentials or a long-running environment, stage the artifact and state the exact remaining check.

## Search Hierarchy

| Order | Surface | Examples |
| :--- | :--- | :--- |
| 1 | Configuration or usage change | Resource input property adjustment, explicit program-level workaround |
| 2 | Lifecycle option or command flag | `--refresh=false`, `ignoreChanges`, `replaceOnChanges` |
| 3 | Narrow normalization or behavioral guard | Local state or input override |
| 4 | Alternate resource flow | Different Pulumi component, resource, or SDK construct |
| 5 | Broader downstream or upstream patch | Upstream provider or bridge override |

## Validation Levels

Label each candidate accurately. Do not present a plausible idea as a verified workaround.

| Level | Meaning |
| :--- | :--- |
| `idea only` | Conceptual; not exercised anywhere. |
| `locally staged` | Written into a repro or test file, not run. |
| `locally validated` | Executed cleanly in a local test harness. |
| `validated in the real failing path` | Verified against the real cloud or provider failure path. |

## Deliverable

```markdown
## Workaround Summary

- **Failure Boundary:** <exact behavior being avoided or suppressed>
- **Candidates Considered:** <surfaces searched and why each was kept or dropped>
- **Best Candidate:** <recommended mitigation and why it wins>
- **Validation Level:** <idea only / locally staged / locally validated / validated in the real failing path>
- **User Impact & Tradeoffs:** <limitations the workaround introduces>
- **Remaining Risk Or Uncertainty:** <what could still bite the user>
- **Next Validation Step:** <how the user or maintainer confirms it>
- **Blocked Execution & Required Access:** <what could not run and what it needs, or None>
```
