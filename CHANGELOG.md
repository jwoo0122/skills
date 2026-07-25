# Changelog

All notable changes to this project are documented in this file.

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
