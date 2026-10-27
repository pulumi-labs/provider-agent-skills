---
name: adopt-provider-agent-skills
description: Install shared APM-managed skills in a Pulumi provider that has no apm.yml, alongside delegated work or as an explicit adoption trial. Publish adoption in a separate PR. Not for updating existing APM consumers.
---

# Adopt Provider Agent Skills

Run `test -f apm.yml` from the provider root. If it succeeds, stop this skill
and continue the assigned task. Otherwise, make adoption a separate PR from a
branch or worktree based on the default branch, excluding the assigned task's
changes. An explicit local trial may stop at a reviewable diff.

## Remove Legacy Skills

Remove these entries from both `.agents/skills/` and `.claude/skills/`, including
symlinks, references and assets inside each directory:

- `provider-code-review`
- `pulumi-upgrade-provider`
- `upstream-patches`

This is the approved migration list, not an ownership investigation. Remove
stale routing to `provider-code-review`; the maintenance skills return through
the bridged package. Preserve other repository-owned skills and their wrappers.
Stage tracked removals before APM recreates ignored files at the same paths.
Remove superseded entries from `skills-lock.json`, deleting it only if empty.

If another shared skill collides with retained local content, stop adoption
before enabling the hook. An initial APM collision-skip message does not protect
files from a later frozen install. Leave no newly active destructive hook and
continue independent task work.

## Apply The Canned Setup

Assets below are relative to this skill. Use them rather than inventing new
configuration or agent guidance:

- `assets/apm.yml`: replace `PROVIDER` with the repository name. Use
  `packages/bridged` for Terraform-bridged providers, or change it to
  `packages/core` for native and component providers. Bridged includes core.
- `assets/mise.toml`: merge into root `mise.toml`, preserving existing tools and
  composing any existing postinstall hook. Install APM and create the initial
  lockfile before enabling the hook, which uses frozen installation.
- `assets/gitignore.txt`: append the ignore rules, adding explicit exceptions
  for each retained local skill in both deployment roots. Symlink exceptions
  must match the link itself, without a trailing slash.
- `assets/agent-guidance.md`: append to the existing agent instruction file,
  or create `AGENTS.md` if none exists. Preserve repository-specific guidance.

The snippets pin APM 0.35.0, supported by Renovate's Containerbase installer,
and shared skills v0.3.0. Keep explicit targets for clean-checkout deployment.
Use the pipx backend. The 0.35.0 standalone Linux x86_64 bundle still requires
glibc 2.38. Renovate CLI alignment belongs in shared `pulumi/renovate-config`,
not per-provider overrides.

Leave generated CI and `.config/mise.toml` alone. Older provider CI mise versions
may skip skill deployment successfully; CI does not need the skills.

## Verify And Publish

Run APM through the consumer's mise environment, not a global CLI:

1. `mise exec -- apm install` creates `apm.lock.yaml` with the pinned writer.
2. Enable the hook, then run `mise deps install agent-skills --force` and
   `mise exec -- apm audit --ci`. Report unavailable policy discovery separately
   from integrity results.
3. Repeat frozen installation. Confirm no manifest or lockfile churn, retained
   local skills unchanged, all requested targets deployed, and generated files
   ignored. Directory outputs miss partial deletions; `--force` repairs them.
4. Verify a disposable clean consumer with the final config, lockfile and local
   skills but no generated directories. Check lockfile and local-skill bytes
   afterward. `git diff --check` and the staged equivalent must pass.

Commit the manifest, lockfile, configuration, guidance and legacy removals, not
`apm_modules/` or generated skills. Open the separate adoption PR with validation
results and any limitations, then return to the assigned task. Do not publish
when the user requested a local-only trial. Do not add a permanent trial report
unless requested.
