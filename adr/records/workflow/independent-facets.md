---
id: workflow.independent-facets
status: accepted
scope: workflow
decision_type: workflow
applies_to:
  - skills/workflow-router/**
  - skills/coding-workflow-core/**
summary: "Route clarification, architecture, execution, and verification as independent facets."
constrains:
  - interaction.material-ambiguity-loop
  - execution.adaptive-delegation
depends_on:
  - workflow.public-entrypoint
supersedes: []
superseded_by: []
last_reviewed: "2026-07-15"
enforcement:
  - id: router-facets
    path: skills/workflow-router/SKILL.md
    must_contain:
      - "| Clarification | `proceed`, `ask` |"
      - "| Verification | `self`, `independent`, `multi-axis` |"
  - id: authority-mode
    path: skills/coding-workflow-core/SKILL.md
    must_contain:
      - "mode: read-only | change"
      - "delivery_boundary: answer | plan | local-change | commit | draft-pr"
---

# Independent workflow facets

## Decision question

How should the workflow represent decisions that do not correlate with code-change size?

## Current decision

The router MUST assess clarification, architecture impact, execution strategy, and verification strategy independently. It MUST NOT collapse them into one linear size-based route. It MUST evaluate those facets inside an explicit read-only/change mode and stop at the user's authorized delivery boundary.

## Context and forces

A tiny diff can carry a major architectural decision, while a large mechanical migration can be fully specified. Question count, ADR volume, worker count, and review depth therefore do not share one reliable scale.

## Invariants

- Clarification is `proceed` or `ask` based on material ambiguity.
- Architecture is `none`, `reference`, or `reconcile` based on durable intent.
- Execution is `direct`, `delegate`, or `decompose` based on implementation shape.
- Verification is `self`, `independent`, or `multi-axis` based on risk and significance.
- Request size alone never forces questions or delegation.
- Read-only work does not invent an implementation topology or mutate ADRs.
- Permission to implement does not imply permission to commit, push, or open a pull request.
- A change request without explicit commit or remote authority defaults to local work without a delivery question or branch switch.

## Alternatives and trade-offs

A single `direct`, `standard`, or `clarify` route is simpler to describe but couples unrelated decisions and produces incorrect behavior for small high-impact or large well-specified work.

## Consequences

Different capable models may choose different valid tactics while still honoring the same minimum workflow invariants.

## Enforcement

Routing scenarios cover small architectural changes, large ADR-defined changes, and ordinary local fixes with facet-specific expectations.

## Revisit when

Revisit if empirical forward tests show that a facet is redundant or a missing independent concern repeatedly causes unsafe routing.
