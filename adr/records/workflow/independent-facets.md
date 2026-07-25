---
id: workflow.independent-facets
status: superseded
scope: workflow
decision_type: workflow
applies_to:
  - skills/clarify-and-plan/**
summary: "Route clarification, architecture, execution, and verification as independent facets."
constrains: []
depends_on:
  - workflow.public-entrypoint
supersedes: []
superseded_by:
  - workflow.minimal-authority-boundary
last_reviewed: "2026-07-26"
enforcement: []
enforcement_exception: null
---

# Independent workflow facets

Superseded by `workflow.minimal-authority-boundary`. The `mode` and `delivery_boundary` boundaries survive there; the `adr` action remains governed by `architecture.living-decisions`. The `execution` and `verification` facets were withdrawn because they prescribed orchestration shape without producing an observable difference in behavior, and the `workflow-router` and `coding-workflow-core` skills that carried them were removed.

## Decision question

How should the workflow represent decisions that do not correlate with code-change size?

## Current decision

This decision is no longer in force. It required a dedicated router stage to assess clarification, architecture impact, execution strategy, and verification strategy as four independent facets, rather than collapsing them into one linear size-based route, and to evaluate those facets inside an explicit read-only/change mode.

## Context and forces

A tiny diff can carry a major architectural decision, while a large mechanical migration can be fully specified. Question count, ADR volume, worker count, and review depth therefore do not share one reliable scale.

## Invariants

The withdrawn decision required:

- clarification to be `proceed` or `ask` based on material ambiguity;
- architecture to be `none`, `reference`, or `reconcile` based on durable intent;
- execution to be `direct`, `delegate`, or `decompose` based on implementation shape;
- verification to be `self`, `independent`, or `multi-axis` based on risk and significance;
- request size alone never to force questions or delegation;
- read-only work never to invent an implementation topology or mutate ADRs;
- permission to implement never to imply permission to commit, push, or open a pull request;
- a change request without explicit commit or remote authority to default to local work.

The last four survive in `workflow.minimal-authority-boundary`. The `execution` and `verification` scales did not.

## Alternatives and trade-offs

A single `direct`, `standard`, or `clarify` route is simpler to describe but couples unrelated decisions and produces incorrect behavior for small high-impact or large well-specified work.

## Consequences

Different capable models may choose different valid tactics while still honoring the same minimum workflow invariants.

## Enforcement

While in force, routing scenarios covered small architectural changes, large ADR-defined changes, and ordinary local fixes with facet-specific expectations. Those scenarios now assert the successor's vocabulary.

## Revisit when

Revisit if empirical forward tests show that a facet is redundant or a missing independent concern repeatedly causes unsafe routing.
