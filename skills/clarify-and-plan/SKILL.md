---
name: clarify-and-plan
description: User-facing entry point for a coding workflow that inspects repository and ADR facts, repeatedly resolves material ambiguity, reconciles durable architectural intent, and defines observable acceptance before implementation. Use when the user invokes clarify-and-plan or when workflow-router selects clarification; continue until consequential choices are resolved, then chain internally into ADR maintenance and execution without requiring another user invocation.
---

# Clarify and Plan

Turn an ambiguous request into a bounded implementation brief and reconcile any durable architectural decisions before implementation dispatch.

## Route direct entry once

When invoked directly, activate `workflow-router` and transfer workflow ownership to it. Do not independently interview, reconcile, or dispatch after the router has chosen and chained a path. The remaining sections apply when `workflow-router` activates this skill for `clarification=ask`; in that case, do not route again and own the workflow tail through the authorized delivery boundary.

## Load policy and existing intent

Activate `coding-workflow-core` if it is not already active. If nested activation is unavailable, locate and read the installed sibling `SKILL.md`.

Before asking a question:

1. Read active repository instructions.
2. Read `adr/index.yaml` when it exists and load only decisions relevant to likely paths, scopes, topics, and linked records. Do not create `adr/` just to begin clarification.
3. Inspect relevant code, tests, public interfaces, conventions, and Git state.
4. Separate facts established by that evidence from choices only the user can make.

Do not ask the user to restate an accepted ADR or decide an internal detail that the repository already determines.

## Maintain a transient decision queue

For each unresolved choice, track internally:

- the decision and why different answers matter;
- plausible interpretations and their trade-offs;
- dependencies on earlier answers;
- whether it blocks implementation or ADR reconciliation;
- the answer, evidence, or disclosed low-impact assumption;
- affected acceptance checks and ADR IDs.

Keep the queue in conversation or plan state, never in the repository. Reorder it after each answer and after new evidence.

## Run the grilling loop

Repeat until no material ambiguity remains:

1. Select the unresolved choice with the greatest behavioral impact, divergence between answers, and cost of reversing later.
2. Ask dependent questions sequentially so the next question reflects the previous answer.
3. Batch a small set of independent questions when their answers do not constrain one another and answering together reduces needless turns.
4. Offer concrete interpretations and the material trade-off instead of asking a broad preference question.
5. If an answer remains vague, contradicts earlier intent, or conflicts with repository evidence or an accepted ADR, narrow the distinction and ask again.
6. Infer or disclose a reversible, low-impact assumption when it does not materially change the result.
7. Reinspect the repository or ADRs whenever an answer exposes a fact that can be verified there.

Do not target a fixed number of questions. Do not start implementation because the interview feels long. Also do not continue asking once remaining uncertainty is immaterial, assumptions are visible, and acceptance can distinguish success from failure.

Read [the grilling loop](references/grilling-loop.md) when answers remain vague, decisions multiply, or the stopping condition is unclear.

## Reconcile architectural intent

After the user resolves consequential choices, determine whether any answer expresses persistent architectural intent that code inspection alone could not reliably recover and that future changes should respect.

- Use `none` for local implementation choices and routine bug fixes.
- Use `reference` when an existing ADR already expresses the governing intent.
- Use `reconcile` when the same decision needs improvement or revision, a genuinely new decision question exists, or an accepted decision is superseded or retired.
- Prefer revising the record that owns the same decision question over creating a chronological duplicate.
- Preserve explicit relationships when a decision is split, merged, challenged, or reversed.

When repository mutation is authorized, give one coordinator or `maintain-architecture-decisions` write ownership, reconcile the records, validate and reindex them, then dispatch implementation. Workers, diagnosticians, researchers, and reviewers may report ADR findings but must never edit `adr/**`. For a read-only or plan-only request, include the proposed ADR action in the brief without mutating the repository.

Do not let ADR reconciliation silently decide an unresolved product or architecture choice. Return to the grilling loop instead.

## Produce the implementation brief

State a compact handoff:

```text
Goal:
Required behavior:
Constraints and non-goals:
Assumptions:
Acceptance checks:
Relevant ADR IDs and invariants:
ADR action:
Execution facet:
Verification facet:
Delivery boundary:
Implementation units:
```

Map every important behavior to an observable automated check or, when automation is disproportionate, an explicit manual check. Scale execution to the actual implementation units and verification to impact and uncertainty; do not derive either from the number of questions or ADR edits.

## Exit and continue

Exit only when:

- no material blocking decision remains;
- contradictions and accepted-ADR conflicts are resolved or explicitly blocked;
- assumptions and non-goals are visible;
- the outcome is bounded and acceptance checks can distinguish success from failure;
- durable architectural intent is reconciled or proposed within the authorized scope; and
- implementation units have enough context to start.

If implementation is authorized, activate `execute-to-pr` immediately with the brief, selected facets, relevant ADR subset, and explicit delivery boundary. Ask again only when required authority or a material decision is still missing, or when the next action is irreversible, destructive, or scope-expanding beyond what the user authorized. Treat security sensitivity and cost as verification signals; do not request redundant approval when the user already granted informed authority. If implementation later exposes a new material ambiguity, return to this loop.
