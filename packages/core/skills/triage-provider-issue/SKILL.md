---
name: triage-provider-issue
description: Triage Pulumi provider issues from evidence to disposition or next action. Use for initial issue assessment, uncertain ownership, duplicate decisions, or selecting a repro, lifecycle, parity, docs, or workaround specialist.
---

# Triage Provider Issue

Triage Pulumi provider issues as an evidence-driven routing problem. Determine settled vs. unsettled facts, estimate confidence, and select the optimal specialist or next action.

> ⚠️ **Core Rule:** Do not post GitHub comments, apply labels, or close issues directly. Produce a bounded triage artifact for maintainers or automated integrations.

---

## Confidence Fork & Decision Table

Estimate confidence after your first evidence pass:

| Confidence Level | Routing Posture | Actionable Strategy |
| :--- | :--- | :--- |
| **$\ge$ 90% (Settled)** | Provisional Disposition | State provisional disposition, explain strongest evidence, name ruled-out alternatives, and define maintainer next step. |
| **60% – 89% (Uncertain)** | Unresolved Question | Center on the unresolved question. Stage the sharper discriminator (repro/parity test) before making a strong ownership call. |
| **$<$ 60% (Low)** | Evidence Acquisition | Avoid leading hypotheses. Focus purely on gathering logs, layout probes, or search evidence. |

> **Discriminator Test:** Ask: *"Would the opposite repro, parity result, or ownership observation change my recommendation?"* If yes, routing is **not** settled.

---

## Specialist Capability Routing Matrix

Select a specialist explicitly when routing is not settled or when a specific evidence artifact is required:

| Specialist Skill | When to Select | Primary Deliverable |
| :--- | :--- | :--- |
| **`stage-pulumi-provider-repro`** | Pulumi lifecycle (create/update/refresh/import) needs maintainer-quality test | Staged Pulumi repro harness & command matrix |
| **`stage-terraform-provider-repro`** | Terraform behavior is the decisive discriminator or upstream TF repro is needed | Staged HCL/TF acceptance test artifact |
| **`bridge-parity-investigation`** | Pulumi fails, Terraform succeeds, and the gap is at the bridge boundary | Focused bridge cross-test |
| **`pulumi-rpc-lifecycle-investigation`** | `grpc.json` log available; unexpected `Check`/`Diff`/`Read` ordering or payload bug | RPC Timeline & Layer Breakdown (Engine vs Bridge vs TF) |
| **`investigate-converted-provider-docs`** | Generated docs, examples, casing, or PCL conversion bugs | Converter pipeline triage (`tfgen` vs PCL vs HCL2) |
| **`workaround-investigation`** | Ownership is clear but user needs immediate mitigation | Documented user workaround & fallback |

---

## GitHub Search Hygiene

```bash
# Explicit repo search (issues / PRs)
gh search issues --repo owner/repo 'search terms' --json number,title,state,url --limit 20
gh search prs --repo owner/repo 'search terms' --json number,title,state,url,closedAt,updatedAt --limit 20
```

- **State Filter:** `--state` accepts `open` or `closed` (never `all`). Omit `--state` to search both.
- **Merge Metadata:** `gh search prs` does **not** expose `mergedAt`. Use `closedAt` then `gh pr view <PR> --json mergedAt`.

---

## Default Triage Output Template

Always output this compact triage artifact:

```markdown
## Triage Summary: Issue #<number>

- **Current State:** <Brief summary>
- **Confidence:** < >=90% / 60-89% / <60% >
- **Settled Facts:** <What is proven by evidence>
- **Unsettled Questions:** <What remains unconfirmed>
- **Selected Specialist:** <Specialist skill name or None>
- **Next Best Action:** <Concrete maintainer step>
- **Workaround Status:** <Available mitigation or None>
- **Related Issues:** <Duplicates, same-family, or background issues>
```
