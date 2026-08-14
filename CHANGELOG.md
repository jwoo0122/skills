# Changelog

All notable changes to this project are documented in this file.

## [3.0.0] (2026-08-15)

### ⚠ BREAKING CHANGES

- `architect` replaces `clarify-and-plan` as the sole intended public entry point, and `execute-to-pr` is removed. Existing installations may need to remove the obsolete skills explicitly before installing `architect`.
- Existing `maintain-architecture-decisions` schema version 2 directories require semantic migration. Do not update only `.adr-system.yaml`: use `architect` with the bundled `migrate-legacy-v2` playbook to reinterpret accepted invariants and enforcement.
- The ADR protocol is now repository-owned `semantic-living-adr` version 1. Source substring assertions and record-wide enforcement exceptions are replaced by invariant-level executable or evidenced manual enforcement.

### Features

- add consequential design clarification and model-directed execution through `architect`;
- add executable argv check registration and honest manual invariant reporting;
- expose a replaceable repository-level `scripts/adr` interface;
- teach models to migrate legacy ADRs semantically and reject marker-only upgrades.

### Upgrade

1. Remove obsolete `clarify-and-plan` and `execute-to-pr` installations, then install `architect` and the updated internal ADR skill.
2. Repositories without `adr/` need no data migration.
3. For legacy v2 repositories, ask `architect` to migrate the ADR system; review any ambiguity or weakened enforcement it reports.
4. Run the repository ADR check and update CI to use the repository-owned ADR interface when available.

## [2.0.0](https://github.com/jwoo0122/skills/compare/v1.0.1...v2.0.0) (2026-07-25)


### ⚠ BREAKING CHANGES

* five skills are removed from the package. Installations that reference workflow-router, coding-workflow-core, diagnose-bug, evidence-research, or review-change by name must be reinstalled.

### Features

* enforce ADR source conformance ([#3](https://github.com/jwoo0122/skills/issues/3)) ([dbba364](https://github.com/jwoo0122/skills/commit/dbba364478671260c846a5318cd6076fa0ebd5d5))
* reduce the workflow to clarification, ADR, and delivery ([#5](https://github.com/jwoo0122/skills/issues/5)) ([ecdb702](https://github.com/jwoo0122/skills/commit/ecdb702ef4bf7813a62af3d65c90b86fdd69d70f))

## [1.0.1](https://github.com/jwoo0122/skills/compare/v1.0.0...v1.0.1) (2026-07-16)


### Bug Fixes

* discover PyYAML-capable Python for ADR tooling ([a71c17b](https://github.com/jwoo0122/skills/commit/a71c17b6c7619766fea6baced784b477dd5340e9))
* discover PyYAML-capable Python for ADR tooling ([968c64e](https://github.com/jwoo0122/skills/commit/968c64e6ebca6c81bfad4d55bb6c1f4922766921))

## 1.0.0 (2026-07-15)

- Introduced one public `clarify-and-plan` entry point backed by seven internally chained workflow skills.
- Added adaptive clarification, semantic ADR reconciliation, implementation delegation, and independent verification.
- Added a living semantic ADR system with deterministic initialization, indexing, and validation.
- Adopted the standard Vercel Skills CLI installation flow and removed the custom installer.
- Added cross-harness compatibility notes, scenario fixtures, regression tests, and third-party attribution.
