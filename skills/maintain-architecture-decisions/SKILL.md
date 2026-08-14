---
name: maintain-architecture-decisions
description: Internal ADR oversight for architect. Maintain a semantic living map of durable architectural intent, connect every accepted invariant to executable or explicit manual enforcement, and run the global conformance gate. Do not present this as a user-facing entry point.
---

# Maintain architecture decisions

Operate as `architect`'s internal ADR reference client. The repository owns `adr/`; this skill has no exclusive authority over it. Any model or tool may maintain the same data if it preserves the directory's declared semantics and conformance contract. Keep durable intent discoverable, revisable, and honestly verified.

## Model

- `adr/index.yaml` is the low-resolution router map.
- `adr/records/<scope>/<question>.md` owns one stable design question.
- Improve or revise the owning record instead of appending chronology.
- Create a record only when a decision is durable, constraining, and non-obvious.
- Accepted decisions may be corrected, superseded, or retired; keep relationships bidirectional.
- One logical writer edits `adr/`. Other contexts report evidence and conflicts.

## Reconciliation

Classify the durable effect as `none`, `reference`, `improve`, `revise`, `create`, `supersede`, or `retire`. Never rewrite an accepted decision solely because code drifted. A current explicit user decision can change an ADR; accidental implementation state cannot.

Read `references/decision-policy.md` before changing records. Use the repository's template and semantic IDs. Update `last_reviewed` when meaning or enforcement changes, then reindex.

## Invariants and enforcement

Every accepted record declares stable invariant IDs in frontmatter. Every invariant has exactly one enforcement entry:

- `executable`: references a check registered in `adr/.adr-system.yaml`; `adr check` executes its argv without a shell from the repository root.
- `manual`: includes a concrete reason, evidence, and revisit conditions. It is accepted by CI but reported as not mechanically verified.

Do not use source substring presence as a general proxy for conformance. Put meaningful contract checks in repository-owned tests, linters, schema validators, graph checks, simulations, or other deterministic commands. A test that only searches prose for an instruction remains weak evidence and must not be represented as semantic enforcement.

Never downgrade executable enforcement to manual, weaken a check, or add an exception merely to pass the gate. If intent, scope, and source disagree, return the conflict to `architect`.

## Commands

Prefer a repository-provided ADR command such as `scripts/adr`, which may point to any conforming implementation. If the repository provides none, use this skill's bundled reference launcher. It is side-effect-free, selects an existing Python with PyYAML, and never installs dependencies.

```sh
# Repository-provided interface in this package:
scripts/adr check --root .

# Bundled reference client when no repository interface exists:
skills/maintain-architecture-decisions/scripts/adr check --root .
```

`check` includes validation, verifies complete invariant coverage, executes each referenced registry check once, and fails globally on any error. Run it before and after every repository change when the ADR system exists. CI may use the same command as its architecture gate.
