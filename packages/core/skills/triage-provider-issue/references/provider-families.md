# Provider Implementation Families

First ownership boundaries to inspect per family. This is a routing aid, not a substitute for repository evidence.

| Family | Subsystem ownership boundaries | Discriminator strategy |
| :--- | :--- | :--- |
| **Bridged** | Pulumi engine lifecycle and checkpoints<br>Pulumi-to-TF bridge translation<br>Provider metadata, overlays, mappings, patches<br>Upstream TF provider schema and runtime<br>`tfgen`, converters, and language generators | Terraform parity can be decisive, but is conditional. Direct source evidence (Go source, parser logic, schema metadata) can settle ownership without a Terraform repro. |
| **Native** | Pulumi engine lifecycle<br>Native provider runtime<br>Schema source, schema generation, and cloud specs<br>Cloud API or SDK behavior<br>Identifier, import, refresh, and state normalization<br>Native code generation | Do not substitute Terraform parity for native-provider evidence. Compare generated schema against the underlying cloud spec or native runtime code. |
| **Component** | Component construction logic<br>Parent and child resource options<br>Provider propagation to child resources<br>Language host vs provider execution<br>Component schema and generated SDKs<br>Behavior inherited from underlying resource providers | Preserve the parent-to-child dataflow and resource options when staging a repro. |

## Direct Source Evidence Principle

If direct source inspection (log traces, Go code, parser logic, schema metadata) identifies the bug boundary, settle ownership directly. Do not defer a source-supported diagnosis or demand a Terraform repro when repository evidence is already sufficient.

The reverse also holds: ask which observation would actually change the ownership recommendation. If a repro would not change it, do not stage one.

## Unknown Or Mixed Family

Inspect the repository layout and the resource implementation before selecting a family. Some repositories contain more than one implementation style. Route the specific resource or failing path rather than assigning one family to the entire repository by name alone.
