---
id: workflow.minimal-authority-boundary
status: accepted
scope: workflow
decision_type: workflow
applies_to:
  - skills/architect/**
summary: "Constrain user authority and global ADR conformance while leaving execution tactics to the model."
constrains:
  - interaction.material-ambiguity-loop
  - architecture.living-decisions
depends_on:
  - workflow.public-entrypoint
supersedes: []
superseded_by: []
last_reviewed: "2026-08-15"
invariants:
  - id: exact-user-authority
    statement: "Read, edit, commit, push, and PR authority are not inferred from one another."
  - id: no-dedicated-execution-stage
    statement: "The package has no fixed planning or execution stage."
  - id: autonomous-execution-tactics
    statement: "No fixed brief, phase sequence, delegation topology, review count, branch strategy, or PR ritual is required."
  - id: global-adr-gate
    statement: "When an ADR system exists, the global ADR check runs before and after every repository change and any failure blocks delivery."
  - id: gate-does-not-expand-scope
    statement: "A global gate failure does not itself authorize unrelated repairs."
enforcement:
  - invariant: exact-user-authority
    kind: manual
    reason: "Authority is supplied by the live user interaction and cannot be inferred from repository files."
    evidence:
      - tests/scenarios.json#authority-boundary
    revisit_when:
      - "A harness exposes machine-verifiable user authority capabilities."
  - invariant: no-dedicated-execution-stage
    kind: executable
    check: package-contract
  - invariant: autonomous-execution-tactics
    kind: manual
    reason: "The model's chosen execution strategy depends on the live task and active harness."
    evidence:
      - tests/scenarios.json#adaptive-execution-tactics
    revisit_when:
      - "A portable harness can expose and evaluate execution-policy choices."
  - invariant: global-adr-gate
    kind: manual
    reason: "Repository code can provide the gate, but only the live agent or CI can prove that it ran at both workflow boundaries."
    evidence:
      - tests/scenarios.json#pre-post-global-gate
      - scripts/check.sh
    revisit_when:
      - "A harness exposes machine-verifiable lifecycle hooks for repository changes."
  - invariant: gate-does-not-expand-scope
    kind: manual
    reason: "Whether a repair is related and authorized depends on task context."
    evidence:
      - tests/scenarios.json#unrelated-global-drift
    revisit_when:
      - "A harness exposes machine-verifiable task scope and mutation authorization."
---

# Minimal authority and conformance boundary

## Decision question

What must the workflow constrain, and what should remain under model judgment?

## Current decision

The workflow constrains user authority, consequential design choices, durable ADR intent, and global ADR conformance. It leaves implementation, verification, delegation, review, Git, and delivery tactics to the model unless the user or active repository instructions constrain them.

When `adr/.adr-system.yaml` exists, the global `adr check` runs before and after every repository change. Any failure blocks delivery, even when unrelated to the requested diff. The failure does not grant authority to modify unrelated areas; ambiguous repair requires a scope or design question.

## Context and forces

A capable model can adapt execution tactics better than a generic workflow state machine. It cannot manufacture user authority or safely treat an existing architecture conflict as irrelevant.

## Invariants

- `exact-user-authority`: Read, edit, commit, push, and PR authority are not inferred from one another.
- `no-dedicated-execution-stage`: The package has no fixed planning or execution stage.
- `autonomous-execution-tactics`: No fixed brief, phase sequence, delegation topology, review count, branch strategy, or PR ritual is required.
- `global-adr-gate`: When an ADR system exists, the global ADR check runs before and after every repository change and any failure blocks delivery.
- `gate-does-not-expand-scope`: A global gate failure does not itself authorize unrelated repairs.

## Alternatives and trade-offs

A scoped gate avoids unrelated blockers but permits accepted decisions to drift indefinitely. A fixed execution workflow is predictable but adds ceremony and duplicates harness policy. The global gate intentionally accepts occasional blocking work in exchange for repository-wide architectural integrity.

## Consequences

Models choose efficient tactics. CI can execute the architecture gate deterministically, while workflow timing, contextual authority, and task scope remain honestly manual claims.

## Enforcement

The package contract verifies that no dedicated planning or execution stage exists. Behavioral scenarios document authority, adaptive tactics, pre/post gate timing, and unrelated-drift handling without representing prose presence as behavioral proof.

## Revisit when

Revisit if global gate failures routinely block work without improving architectural integrity or if a harness supplies stronger authority primitives.
