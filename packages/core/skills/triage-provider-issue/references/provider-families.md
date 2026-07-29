# Provider Implementation Families

Routing guide for identifying initial resource ownership boundaries across Pulumi provider families.

---

| Provider Family | Subsystem Ownership Boundaries | Key Discriminator Strategy |
| :--- | :--- | :--- |
| **Bridged Provider** | • Pulumi engine lifecycle & checkpoints<br>• Pulumi-to-TF bridge translation (`pkg/bridge`)<br>• Provider metadata, overlays, & patches<br>• Upstream Terraform provider schema/runtime<br>• `tfgen` & docs converter tools | **Terraform Parity Test:** Compare behavior against TF equivalent. If TF succeeds & Pulumi fails $\rightarrow$ Bridge boundary. |
| **Native Provider** | • Pulumi engine lifecycle<br>• Native provider runtime (`pulumi-aws-native`)<br>• Schema generation & OpenAPI/CloudControl specs<br>• Cloud API / SDK runtime behavior<br>• Resource ID, import, refresh, & state normalization | **Cloud Spec & Schema Check:** Do **not** use TF parity. Check generated schema vs underlying Cloud API spec. |
| **Component Provider** | • Component construct logic (`pulumi-awsx`)<br>• Parent & child resource options propagation<br>• Language host vs provider execution<br>• Underlying resource provider behavior | **Parent-Child Dataflow:** Preserve resource options & options propagation when staging repros. |

---

## Mixed / Ambiguous Repositories

For repos containing mixed implementation styles, probe the exact failing resource path using `references/provider-families.md` rules rather than assigning a single family to the entire repo by name.
