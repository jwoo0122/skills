---
id: architecture.living-decisions
status: accepted
scope: architecture
decision_type: knowledge-system
applies_to:
  - adr/**
  - skills/maintain-architecture-decisions/**
  - skills/clarify-and-plan/**
  - skills/execute-to-pr/**
summary: "Maintain ADRs as a semantic, revisable map of durable architectural intent."
constrains: []
depends_on:
  - interaction.material-ambiguity-loop
supersedes: []
superseded_by: []
last_reviewed: "2026-07-26"
enforcement:
  - id: checker-implementation
    path: skills/maintain-architecture-decisions/scripts/adr.py
    must_contain:
      - "def enforce_repository"
      - "enforcement failed:"
  - id: workflow-gate-documentation
    path: skills/maintain-architecture-decisions/SKILL.md
    must_contain:
      - "scripts/adr check"
---

# Semantic living architecture decisions

## Decision question

How should durable architectural intent remain discoverable and consistent across models and future changes?

## Current decision

The repository MUST maintain `adr/` as a semantic, indexed, revisable decision system. A record MUST own a stable architectural question and MUST be improved or revised before a new record is created for that same question.

## Context and forces

Code reveals implementation but often not why a boundary, authority, compatibility rule, or trade-off must persist. Chronological append-only ADR logs grow linearly and force future agents to reconstruct current intent from a sequence of stale documents.

## Invariants

- IDs and paths describe stable questions rather than sequence numbers.
- `index.yaml` is the low-resolution router map and matches all records.
- Accepted decisions remain open to explicit correction, reversal, supersession, and retirement.
- Supersession relationships are bidirectional.
- One logical writer owns ADR changes; any other context reports candidates and conflicts instead of editing.
- Deterministic tooling validates structure and declared source-conformance assertions, not architectural importance or unconstrained prose.
- Every accepted record MUST declare at least one repository-relative enforcement check or an explicit, evidenced enforcement exception; the gate MUST run before and after an authorized implementation.
- ADR operations use a repository-provided, side-effect-free launcher that selects an interpreter capable of importing its required dependencies without installing packages.

## Alternatives and trade-offs

Chronological append-only ADRs preserve a visible narrative but accumulate stale decisions. Keeping intent only in code avoids documentation work but increases model-to-model interpretation variance.

## Consequences

Agents can load a small relevant decision subset and avoid re-asking settled intent. Maintaining semantic relationships requires deliberate revisions when questions split or merge.

## Enforcement

The ADR launcher reports the selected Python interpreter and PyYAML location, then runs the structural and source-conformance tool with that same interpreter. It never installs dependencies. The tool validates semantic IDs, paths, statuses, relationships, required sections, index freshness, enforcement declarations, and idempotent indexing. `adr check` reads every accepted record's declared targets and fails on an explicit source mismatch or undocumented enforcement exception. Change review compares the diff with relevant accepted records and the gate result.

## Revisit when

Revisit if repository scale makes the YAML index insufficient, if automated selection needs richer metadata, or if the semantic-update policy causes decision loss in practice.
