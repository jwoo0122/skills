---
id: interaction.material-ambiguity-loop
status: accepted
scope: interaction
decision_type: interaction
applies_to:
  - skills/clarify-and-plan/**
  - skills/workflow-router/**
summary: "Iterate clarification until no unresolved ambiguity can materially change the result."
constrains:
  - architecture.living-decisions
depends_on:
  - workflow.independent-facets
supersedes: []
superseded_by: []
last_reviewed: "2026-07-15"
---

# Material ambiguity interview loop

## Decision question

When must the agent question the user, and when is clarification complete?

## Current decision

The agent MUST inspect available evidence before asking and MUST repeat focused questions while an unresolved choice could materially change behavior, scope, risk, or expensive-to-reverse intent. It MUST proceed without ritual questions when only reversible implementation details remain.

## Context and forces

Premature implementation silently chooses product intent. Conversely, asking about facts available in the repository or low-impact preferences makes light work unnecessarily slow.

## Invariants

- Repository facts and accepted ADRs are investigated before asking the user.
- Dependent questions are asked after their prerequisites; independent high-value questions may be grouped.
- Vague or contradictory answers are narrowed rather than silently interpreted.
- Clarification can resume when implementation exposes new material ambiguity.
- Exit requires bounded behavior, visible assumptions, and observable acceptance.

## Alternatives and trade-offs

Always asking one fixed questionnaire is predictable but ignores context. Never asking maximizes speed but amplifies model-specific guesses.

## Consequences

The number of questions varies by task and model, while the stopping condition remains stable and testable.

## Enforcement

The interview playbook and behavioral scenarios check evidence-first questioning, contradiction recovery, and re-entry from implementation.

## Revisit when

Revisit if models routinely over-interview harmless tasks or proceed with unresolved choices that produce materially divergent outcomes.
