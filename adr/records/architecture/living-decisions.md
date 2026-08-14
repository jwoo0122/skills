---
id: architecture.living-decisions
status: accepted
scope: architecture
decision_type: knowledge-system
applies_to:
  - adr/**
  - skills/maintain-architecture-decisions/**
  - skills/architect/**
summary: "Maintain ADRs as a semantic, revisable map whose accepted invariants have honest executable or manual enforcement."
constrains: []
depends_on:
  - interaction.material-ambiguity-loop
supersedes: []
superseded_by: []
last_reviewed: "2026-08-15"
invariants:
  - id: semantic-living-map
    statement: "Stable questions own records that are revised rather than accumulated chronologically."
  - id: indexed-consistency
    statement: "The generated index matches all records and semantic relationships remain valid."
  - id: complete-invariant-coverage
    statement: "Every accepted invariant has exactly one executable or fully evidenced manual enforcement mapping."
  - id: executable-registry
    statement: "Executable enforcement references an argv-only central registry and each referenced check runs once without a shell."
  - id: honest-manual-status
    statement: "Manual invariants are structurally complete and reported as not mechanically verified."
  - id: meaningful-conformance
    statement: "General source substring assertions are not an ADR enforcement mechanism."
  - id: repository-owned-protocol
    statement: "ADR data and conformance belong to the repository; the bundled skill and checker are replaceable reference clients."
  - id: portable-launcher
    statement: "The reference ADR tooling uses an existing compatible interpreter and never installs dependencies."
enforcement:
  - invariant: semantic-living-map
    kind: manual
    reason: "Whether two records own the same stable architectural question requires semantic judgment."
    evidence:
      - skills/maintain-architecture-decisions/references/decision-policy.md
    revisit_when:
      - "A reliable semantic duplicate detector becomes portable."
  - invariant: indexed-consistency
    kind: executable
    check: adr-tool-contract
  - invariant: complete-invariant-coverage
    kind: executable
    check: adr-tool-contract
  - invariant: executable-registry
    kind: executable
    check: adr-tool-contract
  - invariant: honest-manual-status
    kind: executable
    check: adr-tool-contract
  - invariant: meaningful-conformance
    kind: executable
    check: adr-tool-contract
  - invariant: repository-owned-protocol
    kind: executable
    check: package-contract
  - invariant: portable-launcher
    kind: executable
    check: adr-tool-contract
---

# Semantic living architecture decisions

## Decision question

How should durable architectural intent remain discoverable, revisable, and verifiably consistent?

## Current decision

The repository owns `adr/` as a semantic living decision map. The data and conformance contract are independent of any particular model, skill, or checker. The bundled skill and checker are replaceable reference clients. Each record owns a stable question. Accepted records declare stable invariant IDs, and each invariant is connected exactly once to either a centrally registered executable check or an explicit manual entry with reason, evidence, and revisit conditions.

The repository-level `scripts/adr check` interface validates the complete system and executes every referenced argv-based check once from the repository root without a shell. The exact `{python}` argv token resolves to the compatible interpreter selected by the launcher. It reports manual invariants as not mechanically verified. Source substring assertions are not a general conformance mechanism.

## Context and forces

Code reveals implementation but often not why a boundary or trade-off must persist. Chronological logs accumulate stale answers. The prior string-presence mechanism also created false confidence: preserving a sentence did not prove the architecture was followed, and one weak assertion could make an entire ADR appear enforced.

## Invariants

- `semantic-living-map`: Stable questions own records that are revised rather than accumulated chronologically.
- `indexed-consistency`: The generated index matches all records and semantic relationships remain valid.
- `complete-invariant-coverage`: Every accepted invariant has exactly one executable or fully evidenced manual enforcement mapping.
- `executable-registry`: Executable enforcement references an argv-only central registry and each referenced check runs once without a shell.
- `honest-manual-status`: Manual invariants are structurally complete and reported as not mechanically verified.
- `meaningful-conformance`: General source substring assertions are not an ADR enforcement mechanism.
- `repository-owned-protocol`: ADR data and conformance belong to the repository; the bundled skill and checker are replaceable reference clients.
- `portable-launcher`: The reference ADR tooling uses an existing compatible interpreter and never installs dependencies.

## Alternatives and trade-offs

Embedding arbitrary shell commands in each ADR is flexible but unsafe, duplicated, and difficult to audit. Keeping substring assertions is cheap but measures implementation traces rather than contracts. Requiring automation for every invariant would misrepresent context-sensitive model behavior; explicit manual status is more honest.

## Consequences

CI and agents can use a stable repository-level interface while the underlying conforming implementation remains replaceable. The current reference client runs meaningful repository-owned checks. Adding accepted invariants requires explicit coverage. Manual claims remain visible debt rather than silently passing as machine proof.

## Enforcement

The package contract verifies that `adr/` states its repository ownership and exposes a repository-level command. The ADR tool contract exercises schema rejection, complete coverage, registry validation, command execution, deduplication, failure attribution, and manual reporting. The package contract exercises the repository's selected architectural surface. The launcher tests verify interpreter selection without installation.

## Revisit when

Revisit if command isolation needs a stronger trust model, check runtime requires selection or caching beyond one invocation, or manual invariants can be evaluated deterministically.
