# Compatibility notes

The package uses portable Agent Skills conventions:

- each skill is a directory under `skills/` with a `SKILL.md` frontmatter block;
- `architect` is the sole public entry point;
- internal visibility of `maintain-architecture-decisions` is a best-effort harness hint, not a security boundary;
- OpenAI-facing metadata lives under `agents/openai.yaml`;
- the Claude plugin manifest points at the whole `skills/` directory.

The ADR launcher requires an existing Python interpreter with PyYAML and does not install dependencies. Registered ADR checks are repository-controlled argv arrays run without a shell from the repository root. CI is responsible for preparing their dependencies.
