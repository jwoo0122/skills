---
id: interaction.material-ambiguity-loop
status: accepted
scope: interaction
decision_type: interaction
applies_to:
  - skills/architect/**
summary: "Expose consequential unresolved design choices without interrogating reversible implementation details."
constrains:
  - architecture.living-decisions
depends_on:
  - workflow.minimal-authority-boundary
supersedes: []
superseded_by: []
last_reviewed: "2026-08-15"
invariants:
  - id: evidence-before-questions
    statement: "Repository evidence and relevant accepted ADRs are investigated before asking."
  - id: consequential-forks-exposed
    statement: "The architect asks when plausible answers materially change durable contracts, boundaries, risk, or reversibility."
  - id: reversible-details-delegated
    statement: "Local reversible implementation choices do not trigger ritual questions."
  - id: protected-boundaries-confirmed
    statement: "Broad design delegation does not silently authorize high-risk, irreversible, contract-breaking, or ADR-reversing choices."
enforcement:
  - invariant: evidence-before-questions
    kind: manual
    reason: "Whether the selected evidence is sufficient depends on the repository and conversational context."
    evidence:
      - tests/scenarios.json#evidence-before-question
    revisit_when:
      - "A portable deterministic harness can inspect model tool use and conversation order."
  - invariant: consequential-forks-exposed
    kind: manual
    reason: "Recognizing material design alternatives requires contextual model judgment."
    evidence:
      - tests/scenarios.json#consequential-design-fork
    revisit_when:
      - "Portable deterministic behavioral evaluation becomes available."
  - invariant: reversible-details-delegated
    kind: manual
    reason: "Distinguishing local implementation technique from durable design is context-sensitive."
    evidence:
      - tests/scenarios.json#reversible-local-choice
    revisit_when:
      - "Portable deterministic behavioral evaluation becomes available."
  - invariant: protected-boundaries-confirmed
    kind: manual
    reason: "The meaning and breadth of user delegation must be judged from conversation context."
    evidence:
      - tests/scenarios.json#delegated-design-protected-boundary
    revisit_when:
      - "Portable deterministic behavioral evaluation becomes available."
---

# Consequential design clarification

## Decision question

When must the architect question the user, and which choices should it make autonomously?

## Current decision

The architect investigates evidence first and asks whenever multiple plausible answers would materially change contracts, authority or ownership, failure semantics, compatibility, security or privacy, irreversible state, operational risk, or durable future constraints. It exposes alternatives, consequences, and a supported recommendation instead of silently choosing a default. It proceeds autonomously when only reversible local implementation details remain.

Explicit delegation permits ordinary design judgment but does not implicitly authorize reversing accepted ADRs, breaking public contracts, deciding security/privacy/consent policy, risking data loss, performing irreversible migration, materially increasing operational risk or cost, or contradicting explicit requirements.

## Context and forces

Premature implementation converts model preference into product policy. Fixed questionnaires and questions about every possible implementation do the opposite: they make ordinary work unusably ceremonial.

## Invariants

- `evidence-before-questions`: Repository evidence and relevant accepted ADRs are investigated before asking.
- `consequential-forks-exposed`: The architect asks when plausible answers materially change durable contracts, boundaries, risk, or reversibility.
- `reversible-details-delegated`: Local reversible implementation choices do not trigger ritual questions.
- `protected-boundaries-confirmed`: Broad design delegation does not silently authorize high-risk, irreversible, contract-breaking, or ADR-reversing choices.

## Alternatives and trade-offs

Always asking is predictable but shifts implementation judgment to the user. Never asking is fast but hides policy decisions. The chosen boundary is based on consequences, not request or diff size.

## Consequences

Question count varies naturally. These behavior invariants remain manual until a portable deterministic model-evaluation harness exists; CI reports that limitation rather than claiming prose presence proves behavior.

## Enforcement

Scenario evidence describes positive and negative cases. The ADR gate validates that each manual claim has a reason, evidence, and automation revisit condition, but reports it as not mechanically verified.

## Revisit when

Revisit if models routinely over-question reversible choices or silently choose materially different contracts.
