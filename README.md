# Autonomous Coding Workflow Skills

This package gives coding agents a durable minimum workflow for turning one user request into an appropriately clarified, architecturally coherent, implemented, and verified change, with independent review when impact warrants it.

The user starts one public skill. The agent then decides how much clarification, architectural reconciliation, delegation, and verification the actual work needs:

```text
clarify-and-plan (only public entry point)
  -> workflow-router
     -> inspect repository and relevant ADRs
     -> clarify material ambiguity when necessary
     -> reconcile durable architectural intent
     -> execute-to-pr
        -> work directly or dispatch bounded implementers
        -> diagnose or research when evidence is missing
        -> review independently when impact warrants it
        -> verify, commit, push, and open a draft PR when authorized
```

## Purpose

The skill set is designed to reduce two recurring failures in agentic coding:

1. A lightweight task is buried under ritual questions, planning artifacts, and unnecessary delegation.
2. A consequential task is implemented from guessed intent, without persistent architectural context or an independent check.

It keeps the workflow adaptive rather than deterministic. A clear typo can be fixed directly. A vague product change is grilled until material ambiguity is resolved. A one-line change with system-wide meaning can update an architecture decision and receive independent review. A large but fully specified migration can skip product questions and use bounded parallel work.

The package also maintains `adr/` as revisable architectural memory: durable intent that code inspection alone cannot reliably recover, organized by semantic decision rather than chronological numbering. ADRs constrain future work without becoming immutable; later evidence can improve, challenge, revise, split, supersede, or retire a decision.

## Included skills

Install all eight skills because the public entry point chains to the other seven by name.

```text
skills/
  clarify-and-plan/                 public entry, grilling, acceptance
  workflow-router/                  four-facet adaptive routing
  coding-workflow-core/             shared workflow invariants
  execute-to-pr/                    implementation and delivery coordinator
  diagnose-bug/                     evidence-driven bug diagnosis
  evidence-research/                read-only primary-source research
  review-change/                    independent specification and quality review
  maintain-architecture-decisions/  semantic ADR maintenance and validation
```

Only `clarify-and-plan` is intended for direct user invocation. The remaining skills carry internal instructions and are loaded by the model when the workflow needs them. Hiding internal skills from command menus is harness-dependent; see [compatibility notes](docs/COMPATIBILITY.md).

## Installation

Use the standard [`skills` CLI](https://github.com/vercel-labs/skills). No repository-specific installer is required.

From a local checkout:

```sh
npx skills add . --skill '*'
```

From GitHub, after replacing `OWNER/REPOSITORY`:

```sh
npx skills add OWNER/REPOSITORY --skill '*'
```

Project installation is the default. Add `--global` for a user-level installation or `--agent <agent>` to select a supported harness. Start a new agent session if the harness builds its skill catalog only at session start.

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

After entry, do not invoke each stage manually. The router judges four facets independently:

```text
clarification: proceed | ask
adr: none | reference | reconcile
execution: direct | delegate | decompose
verification: self | independent | multi-axis
```

Around those facets it preserves two authority boundaries: `mode` (`read-only` or `change`) and the requested delivery boundary (`answer`, `plan`, `local-change`, `commit`, or `draft-pr`). Permission to edit does not imply permission to commit or push.

- Clarification depends on unresolved consequential choices, not prompt length or code size.
- ADR handling depends on durable architectural intent, not question count or changed lines.
- Execution depends on separability, integration cost, and safe ownership boundaries.
- Verification depends on impact, uncertainty, and the value of a fresh perspective.

The workflow continues automatically until it reaches the requested boundary: an answer, a plan, verified local changes, a local commit, or a confirmed draft pull request. Explicit limits such as “plan only,” “do not commit,” or “stop after tests” remain authoritative.

### ADR behavior

When `adr/index.yaml` exists, the router reads it first and loads only relevant records. The workflow does not create `adr/` for a routine task. It initializes the structure when an authorized change establishes durable architectural intent worth preserving.

Records use stable semantic IDs and own an architectural decision question. The workflow prefers improving or revising that record over appending a new file. A single coordinator owns ADR writes; implementers, researchers, and reviewers return conflicts or improvement candidates instead of racing to edit architectural intent.

The maintenance tool supports:

```sh
skills/maintain-architecture-decisions/scripts/adr init
skills/maintain-architecture-decisions/scripts/adr reindex
skills/maintain-architecture-decisions/scripts/adr validate
```

## Why I think this structure fits the purpose

I want the user to provide the first requirement and then let the agent carry the workflow. A small, obvious change should stay small. A vague or consequential change should trigger a real design conversation, similar to a grilling session, until the choices that materially change the result are resolved.

The durable output of that conversation should not be a linear pile of decision logs. It should be structured architectural intent: the reasons, boundaries, invariants, and trade-offs that future agents cannot reliably reconstruct by scanning code. That intent must remain open to correction, contradiction, and reversal as evidence changes. Used this way, ADRs reduce the variance between models by narrowing how much hidden intent each model has to guess.

Clarification difficulty, architectural significance, implementation size, and verification risk are different dimensions. Coupling them would make the workflow brittle: a tiny edit can carry a major system decision, while a large mechanical migration can be unambiguous. The four-facet router preserves that distinction and leaves concrete tactics to the model.

Subagents follow the same principle. The coordinator retains user intent and integration responsibility; bounded implementers spend context on execution; fresh reviewers spend context on finding mismatches. The skill set requires that separation when it protects the result, but it does not prescribe a fixed number of questions, workers, reviewers, files, or lines. Better future models should be able to use better judgment without being trapped by today's routing thresholds.

The result is deliberately a set of minimum interaction and engineering invariants, not a workflow engine. It aims to reduce dangerous differences between models while preserving the intelligence, flexibility, and efficiency of the model running it.

## Verification

Run the package checks:

```sh
./scripts/check.sh
```

They validate skill metadata and visibility intent, required resources, the forward-test catalog schema, ADR structure and index consistency, removal of obsolete installation paths, and standard installation documentation. They do not execute an LLM or prove behavioral compliance. The scenario catalog is intended for independent forward tests across models, where success is judged by preserved intent and safety rather than identical wording, question counts, or agent counts.

## Releases

The current release is `1.0.0`. Future versions are managed by Release Please from Conventional Commit messages on `main`:

- `fix:` proposes a patch release.
- `feat:` proposes a minor release.
- `feat!:` or a `BREAKING CHANGE:` footer proposes a major release.

Release Please maintains a release pull request containing the version and changelog update. Merging that pull request creates the corresponding Git tag and GitHub Release. Commits that do not describe a user-visible release, such as `docs:`, `test:`, or `chore:`, do not force a version bump by themselves.

## Limits

This package is a soft instruction layer, not a runtime security boundary. Harnesses may expose internal skills, deny tools or credentials, or choose not to activate an implicit dependency. Git and remote delivery also depend on the repository, worktree, authentication, and active instructions. When the workflow cannot safely continue, it reports the last completed phase and exact blocker rather than claiming completion.

See [compatibility notes](docs/COMPATIBILITY.md) for current harness behavior and portability constraints.
