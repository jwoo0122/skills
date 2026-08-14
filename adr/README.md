# Architecture decisions

This directory is repository-owned architecture data. It is not owned by a particular model, skill, or checker. Any model or tool may read and maintain it if the resulting repository preserves the contract below. The bundled `maintain-architecture-decisions` skill and checker are reference clients, not exclusive authorities.

## Data model

- `.adr-system.yaml` identifies the `semantic-living-adr` protocol version and registers executable checks as argv arrays.
- `index.yaml` is a deterministic, generated routing map. Records are authoritative when it is stale.
- `records/<scope>/<stable-question>.md` owns one stable design question.
- `_template.md` defines record frontmatter and required prose sections.
- Records are revised as current intent changes; this is not a chronological decision log.
- Semantic IDs and record paths are stable across revisions.
- `depends_on`, `constrains`, `supersedes`, and `superseded_by` refer to record IDs. Supersession is bidirectional.
- Record IDs use `<scope>.<stable-question>` with lowercase letters, digits, dots, and hyphens; the file path is `records/<id with dots as slashes>.md`.
- Status is `proposed`, `accepted`, `superseded`, or `retired`. Only accepted records impose current constraints.
- Frontmatter fields are `id`, `status`, `scope`, `decision_type`, `applies_to`, `summary`, `constrains`, `depends_on`, `supersedes`, `superseded_by`, `last_reviewed`, `invariants`, and `enforcement`.

## Accepted-record contract

Every accepted record:

- declares the current decision, context, alternatives, consequences, invariants, enforcement, and revisit conditions;
- gives every invariant a stable ID and statement;
- maps each invariant exactly once to `executable` or `manual` enforcement;
- uses registered executable checks for deterministic evidence;
- gives manual enforcement a reason, inspectable evidence, and a condition for reconsidering automation.

Manual invariants are not mechanically verified. A source string or instruction appearing in a file is not, by itself, proof of architectural conformance.

## Maintenance

Use `index.yaml` to select relevant records instead of loading every ADR. Prefer revising the record that owns an existing question. Create a record only for a new durable, constraining, non-obvious decision. Keep one logical writer during a change to avoid conflicting edits; this is a concurrency rule, not tool ownership.

A conforming implementation must validate record structure and relationships, generate `index.yaml` deterministically, ensure complete invariant coverage, execute each referenced check once from the repository root without a shell, and report manual invariants as not mechanically verified.

This repository exposes a replaceable command interface:

```sh
scripts/adr reindex --root .
scripts/adr validate --root .
scripts/adr check --root .
```

CI and agents should call that repository-level interface rather than depend on the current reference client's internal path. Another implementation may replace it while preserving the declared data and conformance contract.
