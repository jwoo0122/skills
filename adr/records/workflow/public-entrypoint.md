---
id: workflow.public-entrypoint
status: accepted
scope: workflow
decision_type: interface
applies_to:
  - skills/architect/**
  - skills/*/agents/openai.yaml
summary: "architect is the sole intended public entry point and owns authorized repository changes through delivery."
constrains:
  - workflow.minimal-authority-boundary
  - interaction.material-ambiguity-loop
depends_on: []
supersedes: []
superseded_by: []
last_reviewed: "2026-08-15"
invariants:
  - id: exact-skill-surface
    statement: "The package contains architect and internal ADR maintenance, with no dedicated planning or execution skill."
  - id: sole-public-entry
    statement: "architect is the sole intended public skill; supporting ADR maintenance remains internal."
  - id: continuous-ownership
    statement: "architect continues after clarification without requiring another user invocation or a fixed execution stage."
enforcement:
  - invariant: exact-skill-surface
    kind: executable
    check: package-contract
  - invariant: sole-public-entry
    kind: manual
    reason: "Portable Agent Skills metadata cannot make another skill private across every harness."
    evidence:
      - skills/maintain-architecture-decisions/agents/openai.yaml
      - docs/COMPATIBILITY.md
    revisit_when:
      - "Portable skill metadata defines deterministic public and internal visibility."
  - invariant: continuous-ownership
    kind: manual
    reason: "Continuing through a conversation is model behavior, not a repository structure property."
    evidence:
      - tests/scenarios.json#continuous-architect-ownership
    revisit_when:
      - "A portable deterministic conversational harness becomes available."
---

# Sole public architecture entry point

## Decision question

How should a user enter a repository-change workflow without inheriting its internal orchestration?

## Current decision

`architect` is the sole intended public entry point for every repository change. It owns the request through the authorized delivery boundary. ADR maintenance is an internal responsibility, and implementation, verification, and delivery do not require dedicated workflow skills.

## Context and forces

Architectural oversight must apply even to apparently small changes because change size does not predict architectural significance or existing ADR drift. At the same time, fixed planning and execution stages duplicate capabilities of the active model and harness.

## Invariants

- `exact-skill-surface`: The package contains architect and internal ADR maintenance, with no dedicated planning or execution skill.
- `sole-public-entry`: `architect` is the sole intended public skill; supporting ADR maintenance remains internal.
- `continuous-ownership`: `architect` continues after clarification without requiring another user invocation or a fixed execution stage.

## Alternatives and trade-offs

Exposing planning, execution, and ADR commands separately provides explicit phases but leaks orchestration and invites bypassing global supervision. Using `architect` only for visibly architectural work is lighter but cannot guarantee the repository-wide ADR gate.

## Consequences

Simple changes pass through without ritual questions. The name describes the architectural oversight applied to all changes rather than requiring every change to produce architecture. Harnesses without portable private-skill composition may still display the internal ADR skill, so intended visibility is reported as manual rather than falsely machine-enforced.

## Enforcement

The package contract parses the actual skill and OpenAI metadata surface and verifies the absence of obsolete workflow stages. Cross-harness visibility and continuous conversational ownership remain explicit manual claims.

## Revisit when

Revisit if a second genuinely independent public workflow is required or skill harnesses provide a stronger portable composition boundary.
