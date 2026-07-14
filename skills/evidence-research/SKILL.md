---
name: evidence-research
description: Internal read-only research stage for routed coding work. Use in the background when an architectural, technical, compatibility, security, or product decision needs current external evidence; prefer primary sources and return a cited transient result plus ADR impact without changing the repository. Do not present this as a direct user entry point.
user-invocable: false
---

# Evidence Research

Resolve a bounded evidence question without modifying code, ADRs, planning files, dependencies, or external systems.

## Bound and schedule the research

- Restate the question, the decision it informs, and what evidence would change that decision.
- Read the routed ADR subset and repository facts before searching externally.
- Run independently in the background when other work does not depend on the answer. Tell the coordinator when implementation must wait for the result.
- Stop when the decision has enough reliable evidence; do not broaden into a general survey.

## Build defensible evidence

- Prefer specifications, official documentation, source repositories, standards, and original research over summaries.
- Match evidence to the repository's actual versions and constraints. Record publication or access dates when freshness matters.
- Cite the source next to every externally verifiable claim. Clearly label inference and unresolved disagreement.
- Use secondary sources only to discover primary material or when no adequate primary source exists; disclose that limitation.
- Do not turn popularity, a single benchmark, or an undocumented convention into a recommendation without stating its limits.

## Report ADR impact

Compare the evidence with relevant ADR decisions, invariants, consequences, and revisit conditions.

- Do not create or edit an ADR.
- Identify which ADR IDs are supported, challenged, stale, or candidates for reconsideration.
- Return evidence and trade-offs to the coordinator; leave the architectural choice to the authorized decision workflow.

## Return a transient research packet

```text
question_and_decision:
repository_constraints:
findings:
options_and_tradeoffs:
recommendation_or_unknown:
citations:
adr_impact:
  relevant_ids:
  support_or_conflict:
  revisit_signal:
uncertainties:
```

Keep the packet in conversation or the harness result unless the user explicitly requests a permanent artifact.
