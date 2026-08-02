---
name: investigate-converted-provider-docs
description: Investigate bridged-provider generated docs and converted Terraform examples. Use for incorrect casing, malformed PCL, wrong target-language output, or unclear ownership across schema generation, tfgen, the Terraform converter, the bridge, and language generators.
---

# Investigate Converted Provider Docs

Isolate bugs in generated docs, converted Terraform examples, casing, or PCL conversion across `tfgen`, `pulumi-converter-terraform`, the bridge, and the core language generators.

## Pipeline

For bridged providers, generated docs examples usually flow through:

1. `tfgen` extracts upstream Terraform markdown and HCL examples.
2. The bridge invokes `pulumi convert --from terraform --language pcl`.
3. `pulumi-converter-terraform` emits PCL.
4. The bridge converts PCL to target languages with core `hcl2*` generators.

Do not assign ownership from final SDK docs alone. Compare source Terraform, generated PCL, and target-language output.

## Discriminator

Create the smallest synthetic example that reproduces the suspicious shape. Prefer real resource tokens and property names when they are known.

```bash
# Terraform to PCL
pulumi convert --from terraform --language pcl --out out-pcl --generate-only

# Known-good PCL to representative languages
pulumi convert --from pcl --language typescript --out out-ts --generate-only
pulumi convert --from pcl --language python --out out-python --generate-only
pulumi convert --from pcl --language go --out out-go --generate-only
```

| Observation | Suspected owner |
| :--- | :--- |
| Source Terraform correct, PCL wrong or malformed | `pulumi-converter-terraform`, or the mapping information passed to it |
| PCL correct, target language wrong | Core `hcl2*` language generator |
| PCL cannot bind because schema or mappings are absent | Report the limitation; use checked-in generated docs or `tfgen` output as supporting evidence |
| Pulumi schema has the wrong shape before conversion | Provider or bridge schema generation |

## Any And Dynamic Values

Object keys inside `Any`, dynamic, JSON-like, or otherwise opaque values are data keys unless explicit provider metadata says otherwise. Recasing them can change provider behavior.

| Pulumi schema shape | Casing rule |
| :--- | :--- |
| Typed Pulumi object property | Convert HCL keys to Pulumi property names. |
| Map | Preserve exact key casing. |
| `Any`, dynamic, JSON-like, or unknown | Preserve exact key casing. |

If an `Any` value appears to require Pulumi-shaped nested casing, do not infer that from examples alone. Call out that the converter needs explicit metadata or a targeted override to do that safely.

## Deliverable

For the converter issue:

```markdown
## Converted Docs Investigation

- **Source HCL:** <minimal TF snippet>
- **Generated PCL:** <generated PCL snippet>
- **Target Language Output:** <TS / Python / Go snippet, if useful>
- **Pulumi Schema Shape:** <typed object / map / Any / unknown>
- **Why The Key Spelling Matters:** <semantic consequence of the observed casing>
- **Identified Failure Layer:** <tfgen / converter-terraform / hcl2 generator / bridge schema>
```

For the provider-side issue, also report:

- the user-visible workaround
- a link to the upstream converter, core, or bridge issue
- whether local provider action remains
- labels reflecting the provider-side state, such as docs or usability, plus an awaiting label when the actionable fix moved elsewhere
