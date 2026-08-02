# Confidence And Triage Artifact Rules

Confidence estimation, the counterfactual check, and the handoff left by the triage skill.

## Confidence Thresholds

| Level | Posture |
| :--- | :--- |
| `>= 90%` | A provisional disposition is useful and supported by evidence. |
| `60-89%` | Answer "what exact action gets us to certainty?" rather than naming a disposition. |
| `< 60%` | Do not name a leading hypothesis just to sound decisive. Acquire evidence. |

Do not let a detailed issue report or a clever static explanation inflate confidence.

## Counterfactual Discriminator Check

Run this test before routing strongly:

> Would the opposite repro or parity result change my recommendation?

If yes, the recommendation is not settled and the repro is not optional. A detailed static explanation does not bypass this check.

## Triage Handoff

A triage pass leaves behind these fields. Specialist skills use task-specific outputs and should not repeat unrelated triage fields.

| Field | Contents |
| :--- | :--- |
| Current state | Where the investigation stands in one or two lines. |
| Confidence | `>=90%` / `60-89%` / `<60%`. |
| Settled facts | What is proven by evidence. |
| Unsettled questions | What remains unconfirmed, stated as a question. |
| Next best action | One concrete step, not "continue investigating". |
| Artifacts prepared | Staged repros, tests, or logs, with repository-relative paths. |
| Blocked execution and required access | What could not run and exactly what it needs. |
| Workaround status | Mitigation and its validation level, or None. |
| Related issues | Duplicate vs same-family vs background, with the reason. |

Keep each field short and evidence-backed.

## Mechanism Evidence Labels

Label an unproven mechanism explicitly:

- `proven by evidence`
- `likely but unconfirmed`
- `related but applicability unverified`

Do not use a stronger label later in the report than the evidence justifies.
