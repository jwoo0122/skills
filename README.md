# Autonomous Coding Workflow Skills

This package gives coding agents a durable minimum workflow for turning one user request into an appropriately clarified, architecturally coherent, implemented, and verified change, with an independent check when impact warrants it.

The user starts one public skill. The agent then decides how much clarification and architectural reconciliation the actual work needs, and stops at the authority boundary the user granted:

```text
clarify-and-plan (only public entry point)
  -> record mode and delivery boundary
  -> inspect repository and relevant ADRs
  -> clarify material ambiguity until none remains
  -> reconcile durable architectural intent
  -> execute-to-pr
     -> implement, run the ADR conformance gate, verify
     -> review from a fresh context when impact warrants it
     -> stop at local changes, or commit, push, and open a draft PR when authorized
```

## Purpose

The skill set is designed to reduce two recurring failures in agentic coding:

1. A lightweight task is buried under ritual questions and planning artifacts.
2. A consequential task is implemented from guessed intent, without persistent architectural context or an independent check.

It keeps the workflow adaptive rather than deterministic. A clear typo can be fixed directly. A vague product change is grilled until material ambiguity is resolved. A one-line change with system-wide meaning can update an architecture decision and be reviewed by a context that did not write it. A large but fully specified migration can skip product questions entirely.

The package also maintains `adr/` as revisable architectural memory: durable intent that code inspection alone cannot reliably recover, organized by semantic decision rather than chronological numbering. ADRs constrain future work without becoming immutable; later evidence can improve, challenge, revise, split, supersede, or retire a decision.

## Included skills

Install all three skills because the public entry point chains to the other two by name.

```text
skills/
  clarify-and-plan/                 public entry, grilling, acceptance
  execute-to-pr/                    implementation, verification, delivery boundary
  maintain-architecture-decisions/  semantic ADR maintenance and validation
```

Only `clarify-and-plan` is intended for direct user invocation. The remaining skills carry internal instructions and are loaded by the model when the workflow needs them. Hiding internal skills from command menus is harness-dependent; see [compatibility notes](docs/COMPATIBILITY.md).

## Installation

Use the standard [`skills` CLI](https://github.com/vercel-labs/skills). No repository-specific installer is required.

From GitHub:

```sh
npx skills add jwoo0122/skills
```

At the skill prompt, select the **Jwoo0122 Skills** group to toggle all three workflow skills together. The group comes from the bundled Claude plugin manifest, which the Skills CLI also uses for grouped selection.

From a local checkout, use the same grouped prompt:

```sh
npx skills add .
```

For a non-interactive installation of every skill, use `--skill '*' -y`. Project installation is the default. Add `--global` for a user-level installation or `--agent <agent>` to select a supported harness. Start a new agent session if the harness builds its skill catalog only at session start.

ADR structural validation uses PyYAML. The bundled launcher checks installed Python interpreters and uses one that can import it:

```sh
skills/maintain-architecture-decisions/scripts/adr --print-python
```

The launcher never installs Python packages. Set `ADR_PYTHON` to choose an interpreter explicitly; if no candidate can import PyYAML, it reports the environment boundary without editing ADR files.

## Usage

Give the initial requirement to `clarify-and-plan` using the syntax supported by the harness:

- Codex: `$clarify-and-plan`
- Claude Code: `/clarify-and-plan`
- Pi: `/skill:clarify-and-plan`
- Other harnesses: name `clarify-and-plan` in the request or use their normal skill selector

Example:

```text
$clarify-and-plan Add retry support to webhook delivery and open a draft PR.
```

After entry, do not invoke each stage manually. The workflow constrains two authority boundaries, one architectural judgment, and the independence of the evidence behind a risky change; it leaves execution tactics to the model:

```text
mode: read-only | change
delivery_boundary: answer | plan | local-change | commit | draft-pr
clarification: proceed | ask
adr: none | reference | reconcile
```

Permission to edit does not imply permission to commit or push. A change request that does not mention delivery defaults to local changes without asking.

- Clarification depends on unresolved consequential choices, not prompt length or code size.
- ADR handling depends on durable architectural intent, not question count or changed lines.
- Independent review depends on architectural significance, security sensitivity, and reversibility cost, not diff size.

The workflow continues automatically until it reaches the requested boundary: an answer, a plan, verified local changes, a local commit, or a confirmed draft pull request. Explicit limits such as “plan only,” “do not commit,” or “stop after tests” remain authoritative.

### ADR behavior

When `adr/index.yaml` exists, the workflow reads it first and loads only relevant records. The workflow does not create `adr/` for a routine task. It initializes the structure when an authorized change establishes durable architectural intent worth preserving.

Records use stable semantic IDs and own an architectural decision question. The workflow prefers improving or revising that record over appending a new file. One role owns ADR writes for a task; any other context returns conflicts or improvement candidates instead of racing to edit architectural intent.

The maintenance tool supports:

```sh
skills/maintain-architecture-decisions/scripts/adr init
skills/maintain-architecture-decisions/scripts/adr reindex
skills/maintain-architecture-decisions/scripts/adr validate
skills/maintain-architecture-decisions/scripts/adr check
```

## Why I think this structure fits the purpose

I want the user to provide the first requirement and then let the agent carry the workflow. A small, obvious change should stay small. A vague or consequential change should trigger a real design conversation, similar to a grilling session, until the choices that materially change the result are resolved.

Accepted ADRs may declare repository-relative `enforcement` checks (`must_contain` and `must_not_contain`). When static enforcement is inappropriate, they may declare an explicit `enforcement_exception` with a status, reason, evidence, and revisit conditions. The `adr check` command reads declared targets and fails mechanically on source drift or undocumented exceptions. This is a deterministic conformance gate for explicit assertions, not a semantic proof of every natural-language statement; use tests, parsers, and independent review for the remaining behavior.

The durable output of that conversation should not be a linear pile of decision logs. It should be structured architectural intent: the reasons, boundaries, invariants, and trade-offs that future agents cannot reliably reconstruct by scanning code. That intent must remain open to correction, contradiction, and reversal as evidence changes. Used this way, ADRs reduce the variance between models by narrowing how much hidden intent each model has to guess.

Clarification difficulty, architectural significance, and implementation size are different dimensions. Coupling them would make the workflow brittle: a tiny edit can carry a major system decision, while a large mechanical migration can be unambiguous. The workflow keeps them separate and leaves concrete tactics to the model.

It deliberately does not prescribe an execution topology, a delegation policy, or a reviewer count. Those tactics are already governed by the harness and the user's own instructions, and encoding them here only added prose that a capable model does not need.

What remains is what a model cannot supply from its own judgment. The first is authority: whether a request permits a repository change at all, and whether editing files also permits committing, pushing, or opening a pull request. The second is the durable architectural intent recorded in `adr/`. The third is independence: an implementer reading its own diff re-applies the assumptions that produced it, so a change that is architecturally significant, security-sensitive, or expensive to reverse is judged by a context that did not write it. Which context that is — a subagent, another session, or the user — is left to the model.

The result is deliberately a set of minimum interaction and engineering invariants, not a workflow engine. It aims to reduce dangerous differences between models while preserving the intelligence, flexibility, and efficiency of the model running it.

## Verification

Run the package checks:

```sh
./scripts/check.sh
```

They validate skill metadata and visibility intent, required resources, the forward-test catalog schema, ADR structure and index consistency, ADR-to-source enforcement checks, removal of obsolete installation paths, and standard installation documentation. They do not execute an LLM or prove behavioral compliance beyond the declared mechanical checks. The scenario catalog is intended for independent forward tests across models, where success is judged by preserved intent and safety rather than identical wording, question counts, or agent counts.

## Releases

The current release is `1.0.0`. Future versions are managed by Release Please from Conventional Commit messages on `main`:

- `fix:` proposes a patch release.
- `feat:` proposes a minor release.
- `feat!:` or a `BREAKING CHANGE:` footer proposes a major release.

Release Please maintains a release pull request containing the version and changelog update. Merging that pull request creates the corresponding Git tag and GitHub Release. Commits that do not describe a user-visible release, such as `docs:`, `test:`, or `chore:`, do not force a version bump by themselves.

## Limits

This package is a soft instruction layer, not a runtime security boundary. Harnesses may expose internal skills, deny tools or credentials, or choose not to activate an implicit dependency. Git and remote delivery also depend on the repository, worktree, authentication, and active instructions. When the workflow cannot safely continue, it reports the last completed phase and exact blocker rather than claiming completion.

See [compatibility notes](docs/COMPATIBILITY.md) for current harness behavior and portability constraints.
