---
id: execution.adaptive-delegation
status: accepted
scope: execution
decision_type: workflow
applies_to:
  - skills/execute-to-pr/**
  - skills/review-change/**
  - skills/coding-workflow-core/**
summary: "Scale implementer delegation and independent verification to execution shape and risk."
constrains: []
depends_on:
  - architecture.living-decisions
  - workflow.independent-facets
supersedes: []
superseded_by: []
last_reviewed: "2026-07-15"
enforcement:
  - id: implementation-gate
    path: skills/execute-to-pr/SKILL.md
    must_contain:
      - "Run the ADR conformance gate before review and delivery."
  - id: independent-review-gate
    path: skills/review-change/SKILL.md
    must_contain:
      - "Run the ADR conformance gate"
---

# Adaptive implementation and verification

## Decision question

How should implementation and verification roles scale after intent is sufficiently clear?

## Current decision

The coordinator MUST choose direct work, delegation, or decomposition from the implementation shape and MUST choose verification depth independently from risk and architectural significance. Architecturally meaningful changes MUST receive independent verification even when the code edit is small.

## Context and forces

Question count and ADR edits measure intent discovery, not implementation parallelism. Diff size also fails to capture security, compatibility, or architectural risk.

## Invariants

- The coordinator retains user intent, ADR reconciliation, integration, and final evidence.
- Delegated workers receive bounded work packets and only relevant ADRs.
- Shared worktrees avoid concurrent overlapping writers unless isolation is explicit.
- Reviewers inspect requirements, relevant ADRs, raw diffs, and verification evidence independently of implementer summaries.
- Implementers and reviewers report ADR conflicts but do not concurrently edit `adr/`.
- New material ambiguity returns to clarification before work continues.

## Alternatives and trade-offs

Always delegating maximizes role separation but adds overhead to trivial work. Never delegating wastes parallel capacity and weakens independent review. Scaling solely by lines changed misses small high-risk decisions.

## Consequences

A coordinator may directly make a tiny high-impact edit and delegate only review, while a broad mechanical change may use multiple bounded workers without additional user questions.

## Enforcement

Execution scenarios cover direct-plus-independent-review, decomposed implementation, shared-worktree ownership, and reviewer detection of ADR conflicts.

## Revisit when

Revisit if harnesses provide stronger isolated-worktree guarantees or measured delegation overhead changes the practical threshold for worker use.
