# Compatibility notes

The package uses portable Agent Skills conventions:

- each skill is a directory under `skills/` with a `SKILL.md` frontmatter block;
- `architect` is the sole public entry point;
- internal visibility of `maintain-architecture-decisions` is a best-effort harness hint, not a security boundary;
- OpenAI-facing metadata lives under `agents/openai.yaml`;
- the Claude plugin manifest points at the whole `skills/` directory.

The `adr/` format is repository-owned and independent of a particular skill implementation. This repository exposes `scripts/adr` as its stable agent and CI interface; it currently delegates to the bundled reference client and may be replaced by another conforming implementation.

The reference client requires an existing Python interpreter with PyYAML and does not install dependencies. Registered ADR checks are repository-controlled argv arrays run without a shell from the repository root. CI is responsible for preparing their dependencies.
