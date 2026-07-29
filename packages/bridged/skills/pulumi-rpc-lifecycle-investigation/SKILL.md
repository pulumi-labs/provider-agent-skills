---
name: pulumi-rpc-lifecycle-investigation
description: Investigate bridged-provider lifecycle behavior from Pulumi gRPC logs. Use for unexpected Check/Diff/Read ordering or payloads, confusing refresh/import/replacement semantics, stale inputs or state, or uncertain ownership across engine, bridge, provider, and upstream Terraform layers.
---

# Pulumi RPC Lifecycle Investigation

Reconstruct the Pulumi gRPC conversation to isolate lifecycle bugs and property mutations across **Engine**, **Bridge**, **Provider**, and **Upstream Terraform** layers.

---

## Log Capture & Command Reference

```bash
# Capture gRPC conversation to JSON log
PULUMI_DEBUG_GRPC=grpc.json pulumi <operation>

# Search Pulumi architecture docs source for RPC definitions
gh search code "RegisterResourceRequest path:docs/architecture" --repo pulumi/pulumi --limit 10 --json path,url
gh api repos/pulumi/pulumi/contents/docs/architecture/deployment-execution/resource-registration.md --jq '.content' | base64 -d | rg -n "Read|Diff|oldInputs|refresh"
```

---

## Common RPC Lifecycles

| Phase | Expected RPC Sequence | Polarity / Special Notes |
| :--- | :--- | :--- |
| **Normal Update** | `RegisterResource` $\rightarrow$ `Check` $\rightarrow$ `Diff` $\rightarrow$ `Update` | `Check` takes old checked inputs + new program inputs; `Diff` compares old state vs checked new inputs. |
| **Refresh** | `Read` $\rightarrow$ `Diff` | `Read` returns refreshed cloud state; `Diff` compares refreshed candidate (`olds`) vs pre-refresh checkpoint (`news`). |
| **Import / Read** | `Read` | Distinguish managed refresh `Read` from external get/import `Read`. Check whether state, inputs, or ID was supplied. |
| **Replacement** | `Check` (no old inputs) $\rightarrow$ `Diff` (requires replace) | Watch for second `Check` without old inputs during replacement planning. |

---

## Layer Ownership Breakdown Matrix

| Layer | Responsibility & Evidence Scope |
| :--- | :--- |
| **Engine** | Operation scheduling, refresh polarity, checkpoint selection, dependency graph, unknowns, `ignoreChanges`. |
| **Bridge** | Pulumi RPC $\leftrightarrow$ TF config/state translation, checked input defaults, state upgraders, diff detail adaptation. |
| **Provider** | Pulumi provider metadata, callbacks, schema overlays, local patches, generated SDK surface. |
| **Upstream TF** | Upstream schema, state upgraders, validators, `CustomizeDiff`, plan modifiers, CRUD logic. |

---

## Output Template

```markdown
## Lifecycle Phase
<preview / update / refresh / import / replacement>

## RPC Timeline
1. `<method>` `<key payload value or decision>`
2. ...

## Property Trace
| Step | Payload Field | Observed Value | Interpretation |
| :--- | :--- | :--- | :--- |

## Layer Assessment
- **Engine:** <Evidence / Role>
- **Bridge:** <Evidence / Role>
- **Provider:** <Evidence / Role>
- **Upstream TF:** <Evidence / Role>

## Likely Root Cause
<Evidence-supported diagnosis>
```
