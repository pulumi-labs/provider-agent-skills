# Specialist Capability Switches

Routing trigger criteria for transitioning from generic triage to specialized investigation skills.

---

| Specialist Skill | Activation Trigger Criteria | Key Boundary Rule |
| :--- | :--- | :--- |
| **`stage-pulumi-provider-repro`** | • Durable Pulumi repro artifact needed.<br>• Failure touches update, read, refresh, import, preview, diff, or `--refresh --run-program`. | Prefer repo-native examples over temporary scratch directories. |
| **`stage-terraform-provider-repro`** | • Terraform behavior is sharpest discriminator.<br>• Upstream TF acceptance test needed. | **Bridged providers only.** Do not use as default for native or component providers. |
| **`bridge-parity-investigation`** | • Pulumi behavior established AND Terraform behavior established.<br>• Behavior differs (Pulumi fails, TF succeeds). | Do **not** switch early while TF parity is still unknown. |
| **`pulumi-rpc-lifecycle-investigation`** | • `PULUMI_DEBUG_GRPC=grpc.json` log available.<br>• Ownership depends on RPC payload ordering or value mutations across layers. | Use before bridge parity cross-tests when lifecycle path itself is ambiguous. |
| **`investigate-converted-provider-docs`** | • Generated docs, converted examples, casing, or PCL output is wrong.<br>• Unclear ownership across `tfgen`, converter, bridge, or `hcl2` generators. | Compare source TF HCL, PCL, and target language output side-by-side. |
| **`workaround-investigation`** | • Ownership boundary clear enough.<br>• User needs immediate mitigation before official fix. | State triage complete and explicitly announce workaround mode. |
