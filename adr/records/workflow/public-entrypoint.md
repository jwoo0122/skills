---
id: workflow.public-entrypoint
status: accepted
scope: workflow
decision_type: interface
applies_to:
  - skills/clarify-and-plan/**
  - skills/*/agents/openai.yaml
summary: "clarify-and-plan is the sole user-facing entry point for the workflow skill set."
constrains:
  - workflow.minimal-authority-boundary
  - interaction.material-ambiguity-loop
depends_on: []
supersedes: []
superseded_by: []
last_reviewed: "2026-07-26"
enforcement:
  - id: sole-entry
    path: skills/clarify-and-plan/SKILL.md
    must_contain:
      - "sole user-facing entry point"
      - "Never ask the user to invoke another skill."
  - id: internal-metadata
    path: skills/*/agents/openai.yaml
    must_not_contain:
      - "$execute-to-pr"
      - "$maintain-architecture-decisions"
---

# Sole public workflow entry point

## Decision question

How does a user start the chained workflow without learning its internal stages?

## Current decision

`clarify-and-plan` MUST be the sole intended user-facing entry point. Supporting skills MUST remain internally chainable and MUST NOT require another user invocation.

## Context and forces

The workflow spans clarification, ADR maintenance, and implementation delivery. Exposing each stage as a user command leaks orchestration details and makes behavior harness-dependent.

## Invariants

- `clarify-and-plan` owns the workflow from direct invocation through the authorized delivery boundary.
- Internal transitions happen without asking the user to invoke another skill.
- Internal-skill visibility metadata remains a best-effort harness hint, not a security boundary.

## Alternatives and trade-offs

Multiple public commands would make individual stages easier to invoke but would require users to understand and manually preserve workflow state.

## Consequences

Users get one stable interaction contract. Harnesses that ignore internal visibility hints may still display supporting skills.

## Enforcement

Package tests verify that only `clarify-and-plan` lacks the internal visibility marker and that internal metadata does not advertise direct invocation.

## Revisit when

Revisit if the portable Agent Skills specification adds deterministic private skill composition or if a separate public workflow is explicitly required.
