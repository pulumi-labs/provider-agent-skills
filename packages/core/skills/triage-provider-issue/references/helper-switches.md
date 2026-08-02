# Specialist Capability Switches

Trigger criteria for moving from generic triage to a specialist skill.

Specialists in the `pulumi-bridged-provider` package are not installed in every repository. Confirm the capability exists before naming it. When the right specialist is missing, leave a handoff describing the exact artifact required instead of routing to an unavailable skill.

| Specialist | Package | Activation triggers | Boundary rule |
| :--- | :--- | :--- | :--- |
| `stage-pulumi-provider-repro` | core | A durable Pulumi repro artifact is the next evidence.<br>The issue turns on update, read, refresh, import, preview, diff, or `--refresh --run-program`.<br>The opposite Pulumi repro result would change routing. | Do not use as a substitute when Terraform behavior is the real discriminator. |
| `stage-terraform-provider-repro` | bridged | Terraform behavior is the sharpest discriminator.<br>Parity with Terraform determines bridged-provider routing.<br>An upstream acceptance test or durable TF artifact is needed.<br>The opposite Terraform result would change routing. | Bridged providers only. Do not use TF parity as a default discriminator for native or component providers. |
| `bridge-parity-investigation` | bridged | Pulumi behavior is established.<br>Terraform behavior is known and differs meaningfully.<br>The next useful step is capturing the bridge parity gap. | Do not switch early. If TF parity is unknown, use the Terraform repro specialist first. Do not call `awaiting/bridge` while the real open question is still whether Terraform behaves the same way. |
| `pulumi-rpc-lifecycle-investigation` | bridged | The next best evidence is the actual RPC timeline.<br>gRPC logs exist or can be collected with `PULUMI_DEBUG_GRPC`.<br>Ownership depends on how values moved across engine, bridge, provider, and upstream TF.<br>Refresh, import, replacement, `Check`, `Diff`, `Read`, old inputs, state, or unknowns are central. | Use before a bridge parity cross-test when the lifecycle path itself is ambiguous. |
| `investigate-converted-provider-docs` | bridged | A bridged provider has incorrect generated documentation or examples.<br>Source TF, generated PCL, and target-language output must be compared.<br>Ownership may lie in schema generation, `tfgen`, the converter, the bridge, or a core language generator. | Do not assign ownership from final SDK docs alone. |

## Entering Workaround Investigation

Workaround investigation is a mode, not a specialist skill. Read [`workaround-investigation.md`](workaround-investigation.md) when:

- the ownership boundary is clear enough for practical purposes
- the user still needs a mitigation
- another attribution pass is less valuable than workaround validation

State that triage is complete and that the session is entering workaround mode.
