# Architecture workflow skills

This package provides a small architecture-first workflow for repository changes.

```text
architect (sole public entry point)
  ├─ inspect repository evidence and relevant accepted ADRs
  ├─ expose consequential unresolved design choices
  ├─ maintain durable intent through the internal ADR skill
  ├─ choose implementation and verification tactics autonomously
  └─ run the global ADR conformance gate before and after change

maintain-architecture-decisions (internal)
  ├─ maintain a semantic living decision map
  ├─ require invariant-level executable or manual enforcement
  └─ run registered contract checks locally or in CI
```

Architecture is treated as the identification and preservation of consequential choices: contracts, authority and ownership, failure semantics, compatibility, security and privacy, irreversible state, operational risk, and durable constraints. The workflow does not prescribe a planning document, phase sequence, delegation topology, reviewer count, branch strategy, or PR ritual.

## Skills

- `architect`: use for every repository change. It asks when a consequential design choice remains unresolved and proceeds without ritual questions for reversible implementation details.
- `maintain-architecture-decisions`: internal living-ADR maintenance and conformance tooling.

## ADR gate

Repositories using the bundled ADR system register argv-based deterministic checks in `adr/.adr-system.yaml`. Every accepted invariant maps exactly once to either a registered executable check or a fully evidenced manual entry. Manual entries are reported as not mechanically verified.

```sh
skills/maintain-architecture-decisions/scripts/adr check --root .
```

The same command is suitable for CI. It validates the complete ADR system, rejects stale indexes and incomplete invariant coverage, executes each referenced check once without a shell, and exits non-zero on any failure.

## Install

Copy or symlink the directories under `skills/` into your agent's skill directory. The included Claude plugin manifest exposes the same skill directory.

## Development

```sh
./scripts/check.sh
```
