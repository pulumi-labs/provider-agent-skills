# Pulumi Provider Agent Skills

Shared Agent Skills for investigating and maintaining Pulumi providers. The repository is distributed as a small APM package graph so each provider repository can install the capabilities appropriate to its implementation family.

## Packages

| Package | Intended consumers | Skills |
| --- | --- | --- |
| [`core`](packages/core) | All Pulumi provider repositories | `triage-provider-issue`, `stage-pulumi-provider-repro` |
| [`bridged`](packages/bridged) | Bridged provider repositories | Core plus bridge investigation skills and the upstream `pulumi-upgrade-provider` and `upstream-patches` maintenance skills |

Native and component packages should be added when there is justified family-specific content to ship. Until then, those repositories can install `core`.

The bridged package also depends on the `package-maintenance` skill bundle from [`pulumi/agent-skills`](https://github.com/pulumi/agent-skills/tree/main/package-maintenance) and tracks its `main` branch. APM records the resolved commit in the consumer's lockfile; run `apm update` to advance an existing consumer to a newer upstream commit.

## Install With APM

A bridged provider can declare:

```yaml
name: my-provider-agent-context
version: "1.0.0"
targets:
  - opencode
  - codex
  - claude

dependencies:
  apm:
    - git: https://github.com/pulumi-labs/provider-agent-skills.git
      path: packages/bridged
      ref: v0.1.0
```

A native or component provider can install the family-neutral package:

```yaml
dependencies:
  apm:
    - git: https://github.com/pulumi-labs/provider-agent-skills.git
      path: packages/core
      ref: v0.1.0
```

Then run:

```bash
apm install
```

Commit the consumer repository's:

- `apm.yml`
- `apm.lock.yaml`
- generated target context such as `.agents/`, `.opencode/`, `.codex/`, or `.claude/`

Do not commit `apm_modules/`.

Use an immutable release tag or commit in `ref`. The lockfile records the resolved commit and content hashes, while the declared ref controls intentional updates.

## Repository Layout

Each package is independently installable:

```text
packages/<package>/
├── apm.yml
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

APM recognizes this as a `skill_bundle`: the optional `apm.yml` supplies package metadata and dependencies, while each `skills/<name>/SKILL.md` directory is installed as an independent skill. This layout also remains compatible with standard Agent Skills tooling. Use `.apm/` if a package later needs APM-native instructions, prompts, agents, or hooks; do not mix both source layouts in one package.

Skills remain self-contained. References, scripts, assets, and harness metadata needed at runtime belong inside the owning skill directory.

## Package Design

Package boundaries follow what provider repositories consume together:

- `core` contains only family-neutral provider capabilities.
- A family package depends on `core` and adds specialized capabilities.
- Skill names remain globally unique because APM deploys packages into a shared skill namespace.
- Do not create empty family packages or placeholder skills.
- Do not put generic engineering skills here unless they encode Pulumi provider-team judgment.

The repository currently uses lockstep versioning. All package manifests should carry the same version and release from one repository tag until independent package release cadences provide a clear benefit.

## Development

Read [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md). The repository uses [mise](https://mise.jdx.dev/) to pin development tools and expose the same tasks locally and in CI:

```bash
mise install
mise run validate
```

`mise run validate` checks each skill with the Agent Skills reference validator, enforces repository-specific package and portability policies, lints shell scripts, installs each package into a clean APM consumer project, verifies the transitive skill sets, and runs `apm audit --ci` against each resulting lockfile and deployment. Run `mise tasks ls` to see the individual checks.

## License

Apache-2.0. See [`LICENSE`](LICENSE).
