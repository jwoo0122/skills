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
      - "obtain a review from a context that did not write the change"
---

# Minimal authority boundary

## Decision question

What must the workflow constrain, and what must it leave to the model running it?

## Current decision

The workflow MUST constrain three things: the authority boundary of a request, the durable architectural intent it touches, and the independence of the evidence that a risky change is correct. It MUST record `mode` as `read-only` or `change` and stop at the user's authorized `delivery_boundary` of `answer`, `plan`, `local-change`, `commit`, or `draft-pr`. It MUST obtain a review from a context that did not write the change when that change is architecturally significant, security-sensitive, or expensive to reverse. It MUST NOT prescribe an execution topology, a delegation policy, a reviewer count, or a routing table; those tactics belong to the model and the harness.

## Context and forces

The superseded records described a four-facet router and an adaptive delegation policy. Both prescribed orchestration shape that a capable model already chooses well, and both were carried by dedicated skills whose prose restated general agent conduct. Two properties are different, because a model cannot supply either from its own judgment. Permission to edit files does not reveal whether the user authorized a commit, a push, or a pull request. An implementer reading its own diff is not independent evidence, however capable it is, because it re-applies the assumptions that produced the change.

## Invariants

- `mode` and `delivery_boundary` are recorded before any repository mutation.
- A change request without explicit commit or remote authority defaults to local work without asking a delivery question or switching branches.
- Permission to implement never implies permission to commit, push, or open a pull request.
- Read-only work does not mutate the repository or `adr/`.
- Request size alone never forces or suppresses clarification.
- The ADR conformance gate runs before and after an authorized implementation.
- An architecturally significant, security-sensitive, or hard-to-reverse change is reviewed by a context that did not write it, regardless of diff size.
- A reviewing context receives the brief, relevant ADRs, the raw diff, and verification evidence rather than the implementer's summary, and does not edit the files it judges.
- Execution tactics, including whether to delegate bounded work and which context supplies the review, are left to the model and are not encoded as workflow policy.

## Alternatives and trade-offs

Keeping the four-facet vocabulary preserved a shared description of routing, but `execution` and the `self`/`independent`/`multi-axis` scale produced no observable difference in behavior beyond what the authority boundary, the ADR gate, and the independence requirement already state. Prescribing delegation guaranteed role separation but duplicated harness-level and user-level instructions that already govern subagent use. Dropping the independence requirement along with that vocabulary was considered and rejected: it is a requirement about the evidence, not about topology, and self-review cannot substitute for it.

## Consequences

The skill set shrinks to clarification, architectural memory, and bounded delivery. Models gain freedom over execution shape and over which context performs a review, while the requirement that risky work be judged by a context that did not write it survives. Like every other rule here, it is an instruction rather than a mechanical gate; `adr check` can assert that the instruction is present, not that it was followed.

## Enforcement

`adr check` asserts that the clarification stage declares both authority boundaries and that the execution stage declares the conformance gate and the independent-review requirement. Forward-test scenarios cover implicit local delivery, blocked remote delivery, read-only requests, and small changes with large architectural meaning.

## Revisit when

Revisit if authority mistakes reappear despite the declared boundaries, if removing the delegation policy measurably degrades results on large changes, if independent review is routinely skipped or performed by the implementing context, or if a harness begins to require an explicit execution topology.
