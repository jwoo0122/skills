---
name: diagnose-bug
description: Internal bug-diagnosis stage for routed coding work. Use when a reported failure needs reproduction, hypothesis testing, or targeted instrumentation before a fix can be planned; produce red evidence and hand off any architecture-decision conflict without silently changing code intent. Do not present this as a direct user entry point.
user-invocable: false
---

# Diagnose Bug

Find the supported root cause and a falsifiable acceptance boundary. Do not implement the production fix unless the coordinator separately grants implementation authority.

## Establish the evidence boundary

- Read repository instructions, the reported behavior, relevant code and tests, and the routed ADR subset.
- Separate observed symptoms from assumptions. Record the smallest reliable reproduction, or state why reproduction is unavailable.
- Preserve read-only scope when the user requested diagnosis only. In an authorized change workflow, a focused failing regression test may remain as the implementation handoff artifact.

## Run a red-capable loop

1. State a ranked hypothesis with the evidence that would support or falsify it.
2. Reproduce with the narrowest existing check.
3. Add a focused regression test when practical and authorized; confirm it fails for the reported behavior rather than for setup noise.
4. Add minimal temporary instrumentation only when existing signals cannot distinguish the hypotheses.
5. Change one diagnostic variable at a time, update the ranking, and stop when evidence supports one cause strongly enough to guide a fix.

Remove temporary instrumentation and artifacts before handoff. Never weaken a check to create or remove a red result. If no hypothesis is supported, report the missing evidence instead of guessing.

## Handle architecture decisions

Use accepted ADR invariants as evidence of intended behavior, not as unquestionable facts.

- If the implementation violates a relevant ADR, identify the violation as the likely bug boundary.
- If repository evidence contradicts an ADR, or a fix would revise an accepted decision, do not edit the ADR or choose a new intent.
- Return the relevant ADR IDs, the exact conflict, and the decision that must be clarified or handed to `maintain-architecture-decisions`.

## Return a diagnostic packet

```text
status: confirmed | likely | unresolved
symptom_and_reproduction:
scope:
hypotheses_tested:
root_cause:
red_evidence:
proposed_acceptance_check:
adr_impact:
  relevant_ids:
  conflict:
implementation_handoff:
remaining_uncertainty:
```

Link claims to commands, test output, logs, or exact code locations. Keep proposed changes minimal and distinguish confirmed facts from inference.
