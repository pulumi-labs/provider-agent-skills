# Confidence & Artifact Rules

Grounded rules for confidence estimation, counterfactual checks, and triage artifact structures.

---

## Confidence Thresholds

| Confidence Level | Strategy & Posture |
| :--- | :--- |
| **$\ge$ 90%** | Provisional disposition is supported by evidence. |
| **60% – 89%** | Focus on: *"What exact action gets us to certainty?"* |
| **$<$ 60%** | Avoid leading hypotheses. Focus purely on evidence acquisition. |

---

## Counterfactual Discriminator Check

Before declaring a strong routing decision, perform this test:

> **Test:** *"Would the opposite repro or parity result change my recommendation?"*  
> - If **YES** $\rightarrow$ Recommendation is **unsettled**. Staging a repro is mandatory before routing.

---

## Standard Triage Artifact Structure

Every triage pass must leave behind this compact structure:

```markdown
1. Current State
2. Confidence Level (>=90% / 60-89% / <60%)
3. Settled Evidence
4. Unsettled Questions
5. Next Best Action
6. Prepared Artifacts
7. Blocked Execution & Required Access
8. Workaround Status
9. Related Issues (Duplicate vs Same-Family vs Background)
```

### Mechanism Evidence Labels
- `proven by evidence`
- `likely but unconfirmed`
- `related but applicability unverified`
