---
name: coding-workflow-core
description: Internal policy dependency for the chained coding workflow. Apply shared invariants from workflow-router, clarify-and-plan, architecture-decision maintenance, implementation, and review while allowing the model to scale questions, delegation, and verification to the actual work. Do not present this as a direct user entry point or use it alone for read-only questions.
user-invocable: false
---

# Coding Workflow Core

Apply a minimum safe workflow without turning it into a rigid state machine.

## Respect authority and scope

- Treat the user's current request and active repository instructions as authoritative.
- Do not turn an explanation, diagnosis, review, research, plan-only request, or status request into an unauthorized repository change.
- Keep changes surgical. Preserve unrelated user work and existing repository style.
- Do not add features, abstractions, dependencies, or documents that the requested outcome does not need.
- Stop at a higher-priority instruction, permission, credential, or destructive-action boundary and report the exact boundary.

## Judge four facets independently

Do not infer one facet from another or collapse them into a single size label.

```text
mode: read-only | change
clarification: proceed | ask
adr: none | reference | reconcile
execution: direct | delegate | decompose
verification: self | independent | multi-axis
delivery_boundary: answer | plan | local-change | commit | draft-pr
```

`mode` and `delivery_boundary` are authority boundaries around the four adaptive facets. Evaluate execution only for an authorized change. Never infer commit, push, or pull-request authority from permission to edit files.

When a change request does not mention commit or remote delivery, default to `local-change` without asking. Require explicit authority for `commit` and `draft-pr`.

- `clarification` reflects unresolved consequential choices, not prompt length or implementation size.
- `adr` reflects persistent architectural intent, not the number of questions or changed lines.
- `execution` reflects separable work, integration cost, and available agents.
- `verification` reflects failure impact, uncertainty, and the value of a fresh perspective.

A large but fully bounded change may proceed without questions. A one-line policy change may require clarification, ADR reconciliation, direct implementation, and independent review.

## Preserve hard invariants

These are required outcomes, regardless of the chosen workflow shape:

1. Inspect repository instructions, relevant evidence, and existing ADR context before asking questions or editing.
2. Do not begin implementation while a material ambiguity could produce meaningfully different behavior, scope, risk, compatibility, or acceptance.
3. Do not silently violate, rewrite, or bypass an accepted architectural decision. Reconcile a confirmed conflict before implementation dispatch.
4. Keep durable architectural intent in the ADR system when authorized; keep question queues, plans, and task state transient.
5. Give every implementation unit a bounded outcome, constraints, relevant ADR subset, and observable acceptance checks.
6. Verify the resulting behavior. Use a fresh verifier for architecturally significant, high-impact, security-sensitive, or otherwise risky changes.
7. Run the ADR source-conformance gate before and after implementation when an ADR system exists; a failing gate is unfinished work until code, an explicit enforcement exception, or authorized ADR intent is reconciled.
8. Never discard, rewrite, stage, commit, push, or include unrelated user changes.
9. Stop at the requested delivery boundary. Local implementation authority does not grant commit, push, or pull-request authority.

## Leave judgment as heuristics

Use these as signals, not numeric gates:

- Ask when another reasonable answer would materially change the result; infer low-cost internal choices from the repository.
- Delegate when a bounded unit can be performed independently without increasing coordination risk.
- Decompose when multiple bounded units can progress independently or require different expertise.
- Implement directly when the edit is compact or tightly coupled, even if its architectural meaning is large.
- Increase verification independence and breadth with impact, uncertainty, cross-boundary effects, and reversibility cost.
- Treat question count, ADR diff size, changed-line count, and worker count as observations, never as routing formulas.

## Use ADRs as persistent intent

Treat `adr/` as a structured, revisable map of architectural decisions that code inspection alone cannot reliably recover.

- Read `adr/index.yaml` first when it exists, then load only records relevant to likely paths, scopes, topics, and decision relationships.
- Do not create `adr/` merely because the workflow ran. Initialize it only when an authorized change confirms durable architectural intent worth preserving.
- Prefer `reference` when an existing decision already governs the work.
- Use `reconcile` when intent must be improved, revised, created, superseded, retired, or clarified.
- Update the record that owns the same decision question instead of appending a chronological duplicate.
- Keep revision and supersession relationships explicit so future agents can challenge or reverse a decision without losing its context.
- Give one coordinator or architecture-decision maintainer logical write ownership. Workers, diagnosticians, researchers, and reviewers report conflicts or stale records and never edit `adr/**`.
- Validate and reindex ADR records after an ADR write.
- Run `skills/maintain-architecture-decisions/scripts/adr check --root <repository-root>` against the baseline and final source; it mechanically enforces each accepted record's declared checks.

## Maintain compact workflow state

Keep this state in conversation context or the harness plan facility:

```text
goal:
constraints:
acceptance:
open_material_decisions:
relevant_adr_ids:
adr_action:
mode:
clarification:
execution:
verification:
delivery_boundary:
phase:
```

Do not create permanent task databases, question logs, implementation briefs, or issue records unless the user requests them.

## Protect verification and Git state

- Define observable acceptance before non-trivial implementation.
- Prefer existing tests, regression tests, type checks, linters, builds, and concrete API, CLI, UI, data, or performance assertions.
- Never weaken, delete, skip, or rewrite a relevant check merely to obtain a pass.
- Treat a failing required check as unfinished unless evidence shows it is pre-existing and out of scope.
- Let an independent verifier inspect requirements, relevant ADRs, the raw diff, and test evidence rather than relying on the implementer's summary.
- Inspect branch, worktree, and remote state before changing or staging files.
- Never force-push, rewrite published history, bypass repository protections, or fabricate a remote result.

## Finish with evidence

Report what changed, the relevant ADR action and IDs, which checks ran and their results, and the last completed Git or remote phase. If the requested outcome is incomplete, report the precise blocker instead of claiming completion.
