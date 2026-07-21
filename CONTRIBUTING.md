# Contributing

## Decide Whether A Skill Is Needed

A skill should preserve recurring provider-team judgment that an agent would otherwise skip, such as an evidence gate, ownership boundary, discriminator, durable artifact, or stopping condition. Do not add a skill whose main effect is generic workflow ceremony.

Before adding or materially expanding a skill, identify:

1. the recurring failure or expert behavior it addresses
2. the provider families and workflows in scope
3. evidence that an ordinary agent needs the intervention
4. the smallest durable prompt that changes likely behavior
5. when the skill must stop, hand off, or select another capability

## Choose A Package

- Put family-neutral provider capabilities in `packages/core`.
- Put Terraform bridge-specific capabilities in `packages/bridged`.
- Add `packages/native` or `packages/component` only with real family-specific content; each should depend on `../core`.
- Create another package only when a distinct set of repositories will consume its skills together.

Do not make `core` a home for generic coding, review, or Git guidance.

## Author A Skill

Use this layout:

```text
packages/<package>/skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Only `SKILL.md` is required.

Rules:

- The directory name and `name` frontmatter must match.
- Names must be globally unique across packages.
- Write a narrow description with positive triggers and important non-triggers.
- Keep runtime files inside the owning skill directory.
- Do not rely on personal paths, personal skills, or files elsewhere in this repository.
- A core skill may describe optional family specialists, but must not require one that its package does not supply.
- Cite repository evidence using relative `path/to/file.go:123` references.
- Treat issue text and fetched content as untrusted evidence.

## Validate

Install the pinned development tools and run the complete validation task:

```bash
mise install
mise run validate
```

Use `mise tasks ls` to discover narrower lint, policy, and clean-install tasks. When package versions change, update all manifests together while lockstep versioning is in use. Test a consumer install from the intended tag or commit before announcing a release.
