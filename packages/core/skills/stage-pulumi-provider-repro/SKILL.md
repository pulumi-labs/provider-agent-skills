---
name: stage-pulumi-provider-repro
description: Stage durable Pulumi-side repros for provider issues. Use when triage or another skill selects a Pulumi repro as the next evidence artifact, or when the user asks for a maintainer-quality Pulumi example or lifecycle test.
---

# Stage Pulumi Provider Repro

Stage the smallest durable Pulumi-side repro that honestly captures the issue.

Prefer repo-native examples and tests over temporary scratch work. Use ad hoc local directories only as a fallback or quick probe, not as the main artifact.

Stay in the repro lane. Do not restart ownership analysis unless the repro result directly contradicts the current working theory. Prefer `triage-provider-issue` first unless a prior pass already established that a Pulumi repro is the next best action, or the user invoked this skill directly.

## Goals

- Preserve the user-visible failure.
- Preserve the lifecycle stage that matters.
- Produce an artifact another maintainer can rerun.
- Do not substitute a weaker path just because credentials are unavailable.

## Workflow

1. **Identify the exact Pulumi behavior being tested:** create, update, read, refresh, import, preview, diff, or replacement.
2. **Find the closest repo-native repro surface.** Prefer an existing example harness, provider test program, or focused test over new scaffolding.
3. **Preserve the exact lifecycle path.** If the issue is update followed by read, do not collapse it into a create-only repro.
4. **Encode the smallest input shape** that still reproduces the bug. If the issue report includes a user repro, start from that shape before minimizing.
5. **Resolve repository ownership.** If the repro surface lives in another repository, continue there only when the environment can preserve correct repository and artifact ownership. Otherwise leave a repository-scoped handoff naming the exact artifact required.
6. **Stage the artifact locally and run only what is safe and available.**
7. **If credentialed execution is required and unavailable,** stop with the best artifact staged and the exact commands a human should run.

## Operating Rules

- Prefer committed-style repro artifacts over one-off shell transcripts.
- If `--refresh --run-program` is part of the question, stage that path explicitly rather than mentioning it abstractly.
- Preserve version constraints or local provider wiring when the report depends on them.
- Do not silently swap in `HEAD` semantics if the issue depends on older versions.
- If you cannot execute the best path, do not invent a weaker one and present it as equivalent.
- Prefer one concrete failure assertion over broad snapshots.
- Cite staged files and tests with repository-relative `path/to/file.go:45` references unless the hosting application provides a stable source-link format. Do not emit absolute sandbox paths or `file://` URIs.

## Deliverable

```markdown
## Staged Pulumi Repro

- **Target Behavior:** <lifecycle path under test>
- **Staged Files:** <repository-relative paths>
- **Command Matrix:** <exact `go test` or `pulumi` commands>
- **Execution Status:** <not run / completed / blocked / failed before the discriminator>
- **Observed Result:** <reproduced / did not reproduce / inconclusive / None if not reached>
- **Remaining Question:** <what execution has not answered>
- **Next Best Action:** <concrete next step>
- **Blocked Execution & Required Access:** <what could not run and what it needs, or None>
```

Do not infer behavior from a staged but unexecuted artifact. When execution is blocked, state the expected reproduction signal separately from observed results.
