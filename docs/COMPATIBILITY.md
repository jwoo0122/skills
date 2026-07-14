# Compatibility notes

Verified against first-party public documentation on 2026-07-14.

## Portable core and extensions

The [Agent Skills specification](https://agentskills.io/specification) standardizes a skill directory, `SKILL.md`, required `name` and `description`, optional resources, and progressive disclosure. It does not standardize install locations, explicit invocation syntax, deterministic activation, or the `user-invocable` field.

This package uses the common skill-directory structure plus `user-invocable: false` on the seven internal skills. That extension preserves model invocation while hiding direct user invocation only in harnesses that honor it. `clarify-and-plan` leaves user and model invocation enabled and chains to the other skills by name.

The specification recommends keeping `SKILL.md` below 500 lines and resolving resources relative to the skill root. The package's references are one level below each skill entry point.

## Standard installation

The [Vercel `skills` CLI](https://github.com/vercel-labs/skills) accepts local paths and GitHub repositories. Install all eight skills; installing only `clarify-and-plan` leaves its named dependencies unavailable.

From a local checkout:

```sh
npx skills add . --skill '*'
```

From GitHub, after replacing `OWNER/REPOSITORY`:

```sh
npx skills add OWNER/REPOSITORY --skill '*'
```

Project installation is the default. Add `--global` for user scope or `--agent <agent>` to select a supported harness. The CLI installs discovered skill folders; it does not make this package an always-loaded instruction layer.

The seven `user-invocable` fields are deliberate Claude-compatible extensions. Strict Agent Skills validators that accept only specification fields may reject those files even though the Vercel CLI installs them. Removing the fields restores strict frontmatter portability but also removes the only supported model-only visibility hint; it does not improve chaining.

## Codex

Sources: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Custom instructions with `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

- Codex discovers repository skills in `.agents/skills` from the current directory to the repository root, user skills in `~/.agents/skills`, admin skills in `/etc/codex/skills`, and built-ins.
- Codex sees skill name, description, and path first, then reads full instructions when explicitly or implicitly selected.
- A user can explicitly select the entry point as `$clarify-and-plan` or by naming it in the prompt.
- Implicit activation is model-selected, not a guaranteed trigger.
- Codex documentation does not make the non-standard `user-invocable` field a portable visibility guarantee; internal skills may remain visible in some Codex surfaces.
- Codex may show same-name skills from multiple scopes rather than merging them. Avoid installing differing copies of this package at multiple visible scopes.

## Claude Code

Sources: [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands), [Manage memory](https://code.claude.com/docs/en/memory).

- Personal skills live in `~/.claude/skills/<name>/SKILL.md`; project skills live in `.claude/skills/<name>/SKILL.md`.
- Claude may load a skill from its description, and a user can invoke the public entry point as `/clarify-and-plan`.
- Claude Code supports `user-invocable: false` for skills intended only for model activation, so the seven internal skills can remain chainable without being user-facing commands.
- `CLAUDE.md` is separate persistent context. Installing these skills does not create or edit one.

## Pi

Sources: [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md), [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md), [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

- Pi supports `~/.pi/agent/skills`, `~/.agents/skills`, project `.pi/skills`, and project `.agents/skills` along the discovery path.
- Skills are exposed progressively and can be invoked with `/skill:name`, so the public entry point is `/skill:clarify-and-plan`.
- Pi's documentation warns that a model may fail to load a relevant skill automatically.
- `package.json` retains `pi.skills` so Pi can also load this repository as a native package.
- Pi does not provide a portable guarantee for the `user-invocable` extension; the seven internal skills may still appear as direct commands.

## OpenCode

Sources: [OpenCode Agent Skills](https://opencode.ai/docs/skills/), [OpenCode rules](https://opencode.ai/docs/rules/), [OpenCode configuration](https://opencode.ai/docs/config/).

- Native skills live in project `.opencode/skills` or user `~/.config/opencode/skills`. OpenCode also discovers `.agents/skills` and `.claude/skills` at supported scopes.
- The native `skill` tool exposes available metadata and loads full content on demand.
- OpenCode does not define the same explicit slash-command syntax as Claude Code or Pi; ask it to use `clarify-and-plan` through its normal prompt and skill-selection flow.
- OpenCode does not provide a portable guarantee for the `user-invocable` extension, so internal-skill visibility is harness-dependent.
- Installing these skills does not create or edit `AGENTS.md` or `opencode.json`.

## What “supports” means

Support means the harness can discover all eight skill folders, start from `clarify-and-plan`, let the model load the internal dependencies, run repository commands, maintain relevant ADRs, and attempt Git/PR operations through available tools. It does not mean identical command syntax, skill visibility, model behavior, or permission policy. Internal chaining is instructional rather than mechanically enforced.
