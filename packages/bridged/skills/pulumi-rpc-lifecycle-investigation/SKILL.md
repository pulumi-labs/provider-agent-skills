---
name: pulumi-rpc-lifecycle-investigation
description: Investigate bridged-provider lifecycle behavior from Pulumi gRPC logs. Use for unexpected Check/Diff/Read ordering or payloads, confusing refresh/import/replacement semantics, stale inputs or state, or uncertain ownership across engine, bridge, provider, and upstream Terraform layers.
---

# Pulumi RPC Lifecycle Investigation

Reconstruct the actual Pulumi RPC conversation before assigning ownership. Treat engine, bridge, Pulumi provider, and upstream Terraform provider as separate layers until the evidence shows how a value or decision moved between them.

Use this skill when the question is about bridged-provider lifecycle semantics or ownership from logs. Use `stage-pulumi-provider-repro`, `stage-terraform-provider-repro`, or `bridge-parity-investigation` instead when the next best action is a durable repro or bridge cross-test artifact.

Read [`references/payload-trace.md`](references/payload-trace.md) for the fields to collect, how to attribute each value, and how to check lifecycle assumptions against the architecture docs.

## Get Evidence First

If a gRPC log is not already available, ask the user to reproduce with:

```bash
PULUMI_DEBUG_GRPC=grpc.json pulumi <operation> ...
```

Use any explicit log path the user provides. Otherwise search the workspace lightly for `grpc.json`, `*.grpc.json`, or `debug-grpc*.json`. Do not assume a repo-specific debug folder.

Capture the operation context alongside the log:

- Pulumi command and flags, especially `--refresh`, `--run-program`, `--preview-only`, import, destroy, or replacement options.
- Provider name and versions, old and new if this is an upgrade.
- Resource URN, type, name, and the specific property or lifecycle decision under investigation.
- Whether the failure occurred during preview, update execution, refresh, import, read, replacement planning, or destroy.

## Common Lifecycles

| Phase | Expected sequence | Polarity and notes |
| :--- | :--- | :--- |
| Normal update | `RegisterResource` -> `Check` -> `Diff` -> `Update` | `Check` takes old checked inputs plus new program inputs. `Diff` compares old state against checked new inputs. |
| Refresh | `Read` -> `Diff` | `Read` returns refreshed candidate state and inputs. `Diff` receives the refreshed candidate as `olds`/`oldInputs` and the pre-refresh checkpoint inputs as `news`. This polarity is intentional. |
| Import / read | `Read` | Distinguish managed refresh `Read` from external get/import reads. Check whether state, inputs, or only an ID was supplied. |
| Replacement | `Check` (no old inputs) -> `Diff` (requires replace) | Watch for a second `Check` without old inputs during replacement planning. Separate replacement planning from create-before-delete or delete-before-replace execution. |

## Guardrails

These are the recurring misreads. Check each before naming an owner.

- A value in `__defaults` proves it was stored as a Pulumi default in that input bag. It does not prove the current provider schema still has that default.
- A value in refresh `Diff.news` may be a pre-refresh checkpoint input, not the current program input.
- A value returned by `Read` can be actual cloud state, provider reconstruction, bridge extraction from outputs, or state-upgrader output. Inspect the provider and bridge path before assuming which.
- Do not infer a bridge bug just because Terraform `CustomizeDiff` fails. First identify the raw config and state Terraform actually received.

## Layer Ownership

| Layer | Responsibility |
| :--- | :--- |
| Engine | Operation scheduling, refresh polarity, checkpoint selection, dependency graph, unknowns, `ignoreChanges`, replacement orchestration. |
| Bridge | Pulumi RPC to Terraform config/state translation, checked input and default handling, state upgrade invocation, raw config construction, diff and detail adaptation, provider callbacks. |
| Provider | Pulumi provider metadata, callbacks, schema overlays, local patches, generated SDK shape. |
| Upstream Terraform | Terraform schema, state upgraders, validators, `CustomizeDiff`, plan modifiers, CRUD implementation. |

State what each layer did with direct evidence. If attribution is not proven, say what remains unknown.

## Output

Use this structure for non-trivial investigations. For short answers, keep the same discipline without the full table: cite the exact RPC payloads that prove the conclusion.

```markdown
## Lifecycle Phase
<preview / update / refresh / import / replacement, and why>

## RPC Timeline
1. <method> <important value or decision>
2. ...

## Property Trace
| Step | Payload field | Observed value | Interpretation |
| :--- | :--- | :--- | :--- |

## Layer Assessment
- **Engine:** <evidence>
- **Bridge:** <evidence>
- **Provider:** <evidence>
- **Upstream Terraform:** <evidence>

## Likely Root Cause
<what the evidence supports, with a confidence level>

## Unknowns
<what is not yet proven>

## Next Checks
<specific code paths, logs, or repros to inspect>

## Blocked Execution & Required Access
<what could not run and what it needs, or None>
```
