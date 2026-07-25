---
id: execution.adaptive-delegation
status: superseded
scope: execution
decision_type: workflow
applies_to:
  - skills/execute-to-pr/**
summary: "Scale implementer delegation and independent verification to execution shape and risk."
constrains: []
depends_on:
  - architecture.living-decisions
supersedes: []
superseded_by:
  - workflow.minimal-authority-boundary
last_reviewed: "2026-07-26"
enforcement: []
enforcement_exception: null
---

# Adaptive implementation and verification

Superseded by `workflow.minimal-authority-boundary`. The ADR conformance gate and the requirement that a risky change be judged by a context that did not write it both survive there. What was withdrawn is the topology around them: the delegation policy duplicated harness-level and user-level instructions that already govern subagent use, the `self`/`independent`/`multi-axis` scale prescribed reviewer counts, and the `review-change` skill that carried the reviewer role was removed.

## Decision question

How should implementation and verification roles scale after intent is sufficiently clear?

## Current decision

This decision is no longer in force. It required a coordinator to choose direct work, delegation, or decomposition from the implementation shape, to choose verification depth independently from risk and architectural significance, and to give architecturally meaningful changes independent verification even when the code edit was small. Only the last requirement survives, in `workflow.minimal-authority-boundary`.

## Context and forces

Question count and ADR edits measure intent discovery, not implementation parallelism. Diff size also fails to capture security, compatibility, or architectural risk.

## Invariants

The withdrawn decision required a coordinator to retain user intent, ADR reconciliation, integration, and final evidence; delegated workers to receive bounded work packets and only relevant ADRs; shared worktrees to avoid concurrent overlapping writers; reviewers to inspect requirements, relevant ADRs, raw diffs, and verification evidence independently of implementer summaries; implementers and reviewers to report ADR conflicts without editing `adr/`; and new material ambiguity to return to clarification.

The reviewer-independence and single-ADR-writer requirements survive, in `workflow.minimal-authority-boundary` and `architecture.living-decisions` respectively. The delegation and worktree topology did not.

## Alternatives and trade-offs

Always delegating maximizes role separation but adds overhead to trivial work. Never delegating wastes parallel capacity and weakens independent review. Scaling solely by lines changed misses small high-risk decisions.

## Consequences

A coordinator may directly make a tiny high-impact edit and delegate only review, while a broad mechanical change may use multiple bounded workers without additional user questions.

## Enforcement

While in force, execution scenarios covered direct-plus-independent-review, decomposed implementation, shared-worktree ownership, and reviewer detection of ADR conflicts. Only the independent-review expectation is still asserted.

## Revisit when

Revisit if harnesses provide stronger isolated-worktree guarantees or measured delegation overhead changes the practical threshold for worker use.
