# Disposition Gates

Gate criteria required before making a strong routing or duplicate claim.

## Gate Matrix

| Disposition | Use when at least one is true | Do not use when |
| :--- | :--- | :--- |
| `awaiting-upstream` | An upstream issue or fix matches the same user-facing failure mode and maintainer next action.<br>Terraform reproduces strongly enough that routing would not change if Pulumi-specific details were refined later. | The issue is only in the same general area as an upstream issue.<br>The upstream issue is merely suggestive.<br>TF parity is unknown and would change the recommendation. |
| `awaiting/bridge` | An existing bridge issue matches the same failure mode.<br>Pulumi and Terraform behavior are both established and the remaining gap is bridge-owned. | The bridge is only a plausible layer.<br>TF parity is still unknown.<br>The first bridge repro artifact has not been staged yet. |
| `duplicate` | **Both:** the existing issue covers the same user-facing failure mode, **and** the next maintainer action is the same. | The issue only touches the same subsystem or root area. Say `same-family`, `possible umbrella/root issue`, or `historical background` instead. |
| `awaiting-feedback` | The strongest explanation is outside the provider's current bug surface (version resolution, environment mismatch).<br>The repro depends on missing stack or state details.<br>Current `HEAD` does not reproduce and the missing discriminator lives with the reporter. | The issue is merely annoying or hard to reproduce. If maintainer repro is the sharpest next step, stage the repro artifact instead. |
| `local-fix` | Repo-local evidence settles the ownership boundary well enough that the next maintainer action happens in this repo. | The ownership boundary is still unconfirmed, or the opposite upstream/parity result would overturn the routing. |
| `fixed by upgrade` | The issue is best explained by a capability or fix that already landed in a later released version. | An open bug remains in `HEAD`. |

`local-fix` does not require certainty about the exact final patch. It requires that the opposite upstream or parity result would not overturn the routing recommendation.

A `fixed by upgrade` report must still state the exact version boundary, why the reported version explains the report, and why this is not an open current bug in `HEAD`.

Do not collapse "same general area" into "duplicate."

## Hypothesis Discipline

If the best explanation is still a leading theory, say so.

Good:

- "likely but unconfirmed root cause"
- "related upstream fix, exact applicability unverified"
- "same family as `#1234`, not yet justified as duplicate"

Bad:

- presenting a plausible static mechanism as if the issue text or repro already proved it
- naming a strong routing label and then quietly adding caveats later
