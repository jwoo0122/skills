---
id: workflow.minimal-authority-boundary
status: accepted
scope: workflow
decision_type: workflow
applies_to:
  - skills/clarify-and-plan/**
  - skills/execute-to-pr/**
summary: "Constrain the workflow with explicit authority boundaries instead of a facet or delegation topology."
constrains:
  - interaction.material-ambiguity-loop
  - architecture.living-decisions
depends_on:
  - workflow.public-entrypoint
supersedes:
  - workflow.independent-facets
  - execution.adaptive-delegation
superseded_by: []
last_reviewed: "2026-07-26"
enforcement:
  - id: authority-mode
    path: skills/clarify-and-plan/SKILL.md
    must_contain:
      - "mode: read-only | change"
      - "delivery_boundary: answer | plan | local-change | commit | draft-pr"
  - id: implementation-gate
    path: skills/execute-to-pr/SKILL.md
    must_contain:
      - "Run the ADR conformance gate before and after implementation."
---

# Minimal authority boundary

## Decision question

What must the workflow constrain, and what must it leave to the model running it?

## Current decision

The workflow MUST constrain only two things: the authority boundary of a request and the durable architectural intent it touches. It MUST record `mode` as `read-only` or `change` and stop at the user's authorized `delivery_boundary` of `answer`, `plan`, `local-change`, `commit`, or `draft-pr`. It MUST NOT prescribe an execution topology, a delegation policy, a reviewer count, or a routing table; those tactics belong to the model and the harness.

## Context and forces

The superseded records described a four-facet router and an adaptive delegation policy. Both prescribed orchestration shape that a capable model already chooses well, and both were carried by dedicated skills whose prose restated general agent conduct. The authority boundary is different: it is the one property a model cannot safely infer, because permission to edit files does not reveal whether the user authorized a commit, a push, or a pull request.

## Invariants

- `mode` and `delivery_boundary` are recorded before any repository mutation.
- A change request without explicit commit or remote authority defaults to local work without asking a delivery question or switching branches.
- Permission to implement never implies permission to commit, push, or open a pull request.
- Read-only work does not mutate the repository or `adr/`.
- Request size alone never forces or suppresses clarification.
- The ADR conformance gate runs before and after an authorized implementation.
- Execution tactics, including whether to delegate bounded work, are left to the model and are not encoded as workflow policy.

## Alternatives and trade-offs

Keeping the four-facet vocabulary preserved a shared description of routing, but `execution` and `verification` produced no observable difference in behavior beyond what the authority boundary and the ADR gate already enforce. Prescribing delegation guaranteed role separation but duplicated harness-level and user-level instructions that already govern subagent use.

## Consequences

The skill set shrinks to clarification, architectural memory, and bounded delivery. Models gain freedom over execution shape, and the workflow loses its ability to require independent review as a structural rule; that risk is carried instead by the conformance gate, the acceptance checks, and the diff inspection listed in the execution stage.

## Enforcement

`adr check` asserts that the clarification stage declares both authority boundaries and that the execution stage declares the conformance gate. Forward-test scenarios cover implicit local delivery, blocked remote delivery, and read-only requests.

## Revisit when

Revisit if authority mistakes reappear despite the declared boundaries, if removing the delegation policy measurably degrades results on large changes, or if a harness begins to require an explicit execution topology.
