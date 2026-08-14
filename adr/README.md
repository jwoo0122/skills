# Architecture decisions

This directory is a semantic living map of current architectural intent, not a chronological log.

- Use `index.yaml` to route to relevant records; do not load every ADR by default.
- Keep one record per stable design question and revise it when the answer changes.
- Every accepted invariant has exactly one `executable` or `manual` enforcement entry.
- Executable entries reference argv commands registered in `.adr-system.yaml`.
- Manual entries require reason, evidence, and revisit conditions and are reported as not mechanically verified.
- Keep supersession relationships bidirectional and use one logical ADR writer.

```sh
skills/maintain-architecture-decisions/scripts/adr reindex --root .
skills/maintain-architecture-decisions/scripts/adr validate --root .
skills/maintain-architecture-decisions/scripts/adr check --root .
```

`check` includes structural validation and runs each referenced executable registry check once. It must pass globally before and after repository changes and can be used directly in CI.
