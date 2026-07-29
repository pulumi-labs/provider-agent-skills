---
name: investigate-converted-provider-docs
description: Investigate bridged-provider generated docs and converted Terraform examples. Use for incorrect casing, malformed PCL, wrong target-language output, or unclear ownership across schema generation, tfgen, the Terraform converter, the bridge, and language generators.
---

# Investigate Converted Provider Docs

Triage and isolate bugs in generated docs, converted Terraform examples, casing, or PCL conversion across **`tfgen`**, **`pulumi-converter-terraform`**, **Bridge**, and **Core Language Generators**.

---

## Docs Conversion Pipeline & Attribution Matrix

```
[Upstream TF HCL] ──(tfgen)──> [PCL Intermediate] ──(hcl2 generators)──> [Target SDK Docs (TS/Py/Go)]
```

| Pipeline Step | Conversion Command | Failure Symptom & Suspected Layer |
| :--- | :--- | :--- |
| **1. TF $\rightarrow$ PCL** | `pulumi convert --from terraform --language pcl --out out-pcl --generate-only` | Source TF correct, PCL wrong/malformed $\rightarrow$ Suspect `pulumi-converter-terraform` or bridge mapping. |
| **2. PCL $\rightarrow$ TS/Py/Go** | `pulumi convert --from pcl --language typescript --out out-ts --generate-only` | PCL correct, target language wrong $\rightarrow$ Suspect core `hcl2*` language generator. |
| **3. Schema Binding** | *(PCL binding fails due to missing schema)* | Missing schema/mappings $\rightarrow$ Suspect bridge/provider schema generation. |

---

## Casing & Any-Type Key Routing Rules

| Data Shape in Pulumi Schema | Casing Routing Rule |
| :--- | :--- |
| **Typed Pulumi Object Property** | Convert HCL keys to camelCase / Pulumi property names. |
| **Map Type** | Preserve exact key casing. |
| **`Any`, Dynamic, or JSON-like** | **Preserve exact key casing.** Object keys inside `Any`/opaque shapes are data keys; recasing breaks provider runtime behavior. |

---

## Deliverable Artifact Format

```markdown
## Converted Docs Investigation

- **Source HCL:** `<Minimal TF HCL snippet>`
- **Generated PCL:** `<Generated PCL snippet>`
- **Target Language Output:** `<TS / Python / Go output snippet>`
- **Pulumi Schema Type:** `<Typed Object / Map / Any>`
- **Identified Failure Layer:** `<converter-terraform / hcl2 generator / bridge schema / tfgen>`
- **User Workaround:** `<Available mitigation for docs/examples>`
```
