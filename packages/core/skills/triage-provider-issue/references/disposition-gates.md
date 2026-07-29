# Disposition Gates

Strict gate criteria required before making a strong routing disposition or closing issue claim.

---

## Disposition Gate Matrix

| Label / Disposition | Required Criteria (MUST be True) | Negative Criteria (DO NOT Use If...) |
| :--- | :--- | :--- |
| **`awaiting-upstream`** | • Matching upstream issue/PR exists for same failure mode & action, **OR**<br>• Terraform reproduces failure strongly. | • Issue is only in same general area.<br>• Upstream issue is merely suggestive.<br>• TF parity is still unknown. |
| **`awaiting/bridge`** | • Matching bridge issue exists, **OR**<br>• Pulumi & TF behavior established, gap is bridge-owned. | • Bridge is only a plausible theory.<br>• TF parity is still unknown.<br>• Bridge repro artifact has not been staged. |
| **`duplicate`** | • Covers **same** user-facing failure mode, **AND**<br>• Requires **same** next maintainer action. | • Issue only touches same subsystem or general area.<br>*(Label as `same-family` or `umbrella issue` instead)*. |
| **`awaiting-feedback`** | • Explanation is outside provider code (env/version mismatch).<br>• Repro depends on missing reporter stack details. | • Issue is simply annoying or hard to reproduce.<br>*(Stage maintainer repro instead)*. |
| **`local-fix`** | • Repo-local evidence settles ownership boundary.<br>• Opposite upstream result would **not** overturn routing. | • Ownership boundary is still unconfirmed. |
| **`fixed by upgrade`** | • Issue explained by fix/feature landed in later release. | • Open bug remains in `HEAD`.<br>*(Must cite exact version boundary)*. |

---

## Hypothesis Discipline Rules

- **Label Unproven Claims Plainly:** Use explicit labels (*"likely but unconfirmed"*, *"related upstream fix, applicability unverified"*).
- **No False Decisiveness:** Never present a plausible static code mechanism as if the issue text or repro already proved it.
