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

Use an immutable release tag and APM's string dependency form so Renovate can discover and update the package reference.

A bridged provider can declare:

```yaml
name: my-provider-agent-context
version: "1.0.0"

targets:
  - codex
  - claude
  - opencode

dependencies:
  apm:
    - pulumi-labs/provider-agent-skills/packages/bridged#v0.1.0
```

A native or component provider can install the family-neutral package:

```yaml
targets:
  - codex
  - claude
  - opencode

dependencies:
  apm:
    - pulumi-labs/provider-agent-skills/packages/core#v0.1.0
```

Keep the targets explicit: a clean checkout has no generated target directories for APM to auto-detect. Then run:

```bash
apm install
```

Commit `apm.yml` and `apm.lock.yaml`. Treat the installed shared skills and package store as generated output:

```gitignore
apm_modules/
.agents/skills/*

# Explicitly track each repository-owned skill.
!.agents/skills/my-local-skill/
```

Do not commit `apm_modules/` or installed shared skill files. A broad skills ignore requires an exception for every repository-owned skill so that Git does not hide local work.

The lockfile records the resolved repository commits and deployed-file content hashes. To adopt APM in a repository that already vendors a shared skill, remove its tracked `.claude/skills/<name>` and `.agents/skills/<name>` copies in the same change; otherwise the old files can collide with or duplicate the APM deployment.

### Install Through mise

Provider repositories can pin APM and model the package store and shared deployment directory as mise dependency outputs:

```toml
[settings]
experimental = true

[tools]
"pipx:apm-cli" = "0.26.0"

[deps.agent-skills]
sources = ["apm.yml", "apm.lock.yaml"]
outputs = [
  "apm_modules/",
  ".agents/skills/",
]
run = "apm install --frozen"
```

`mise deps` is currently experimental. Directory outputs avoid duplicating the dynamic skill inventory: a changed manifest or lockfile makes the dependency stale and installs newly added skills. Mise checks that the directories exist, not every deployed file; force a repair after partial deletion with:

```bash
mise deps install agent-skills --force
```

Expose a standard command for developers and remote-agent bootstrap:

```make
install_agent_skills: .make/mise_install
	mise deps install agent-skills
.PHONY: install_agent_skills
```

Invoke this command before starting an agent. Keep it separate from ordinary workspace preparation and CI jobs that do not need agent skills.

### Releases

All packages currently share one version and release from a repository tag. A normal Git tag is sufficient; APM clones the repository at that tag and does not require a package-specific release asset. Update the declared `#vX.Y.Z` reference and regenerate the consumer lockfile to adopt a new release.

The `v0.1.0` release has been validated from a clean remote APM 0.26 consumer: the bridged dependency resolved the tagged commit, installed all eight transitive skills, and passed `apm audit --ci --no-policy`.

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
