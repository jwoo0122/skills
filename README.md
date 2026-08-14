# Architecture workflow skills

A small skill set for making consequential engineering decisions explicit, preserving them as living architecture decisions, and checking that implementation still conforms.

## The problem

Capable coding agents can usually find a plausible implementation. The harder problem is deciding whether they are authorized to choose among several plausible system designs.

Without an explicit architecture boundary, agents tend to:

- turn an unstated product or engineering choice into an implementation default;
- treat the current source tree as intent, even when it only reflects accidental drift;
- lose the rationale and constraints that future changes must preserve;
- keep ADRs as historical prose that no longer constrains the repository;
- or compensate with a heavyweight workflow that adds ceremony to every change.

This package takes a narrower position: **architecture work is the identification, clarification, preservation, and verification of consequential choices.** It constrains those choices while leaving ordinary implementation tactics to the active model and harness.

## What it proposes

```text
architect (sole intended public entry point)
  ├─ inspect repository evidence and relevant accepted ADRs
  ├─ expose unresolved consequential design choices
  ├─ reconcile durable intent through living ADRs
  ├─ choose implementation and verification tactics autonomously
  └─ run the global ADR conformance gate before and after change

maintain-architecture-decisions (internal)
  ├─ maintain a semantic map of current decisions
  ├─ connect each accepted invariant to executable or manual evidence
  └─ run registered architecture checks locally or in CI
```

The workflow deliberately does **not** prescribe a planning document, phase sequence, delegation topology, reviewer count, branch strategy, or PR ritual. Those are execution choices, not universal architecture rules.

## When this is useful

Use these skills when one or more of the following matters:

- coding agents make changes to the same repository over time;
- design intent must survive beyond one conversation or implementation;
- a request may hide choices about contracts, ownership, failure semantics, compatibility, security, data, or operational risk;
- you want the agent to challenge ambiguous design intent instead of silently selecting a reasonable default;
- accepted ADRs should be checked against the repository in local development or CI.

The package adds less value to disposable work with no durable constraints, no shared repository, and no need to preserve design intent.

## How to use it

Invoke `architect` for repository changes and state the goal, known constraints, and delivery authority. For example:

```text
Use $architect to add webhook retries without breaking existing consumers.
Implement the change and open a draft PR.
```

`architect` then:

1. inspects repository evidence and the relevant accepted ADRs;
2. runs the global ADR gate when the repository has an ADR system;
3. asks before choosing among consequential unresolved designs;
4. updates durable architectural intent when needed;
5. chooses an appropriate implementation and verification strategy;
6. runs the global ADR gate again before delivery.

Be explicit about authority. Permission to edit does not imply permission to commit, push, or open a pull request.

Do not invoke `maintain-architecture-decisions` directly. `architect` uses it when a durable decision needs to be created or reconciled. A repository without ADRs should not gain an ADR system merely because the skill is installed.

## What triggers a design question

`architect` asks when plausible answers would materially change:

- public or internal contracts;
- authority, ownership, or source of truth;
- failure, consistency, retry, ordering, or recovery semantics;
- compatibility and migration obligations;
- security, privacy, consent, or data lifecycle;
- irreversible state or expensive-to-reverse constraints;
- operational cost or risk.

It should not ask merely because multiple implementation techniques exist. Local, reversible choices that fit repository conventions remain the model's responsibility.

If the user delegates design discretion, the model may choose ordinary design details. That delegation does not silently authorize breaking accepted ADRs or public contracts, deciding security or privacy policy, risking data loss, performing irreversible migration, or materially increasing operational risk.

## Living ADRs and conformance

An ADR belongs in the system when a decision is **durable**, **constrains future work**, and is **not obvious from code and tests alone**. Records own stable design questions and are revised as current intent changes; they are not an append-only implementation history.

The `adr/` directory is repository-owned data, not the private output of these skills. Any model or tool may maintain it if it preserves the declared semantics and conformance contract. The bundled skill and checker are reference clients that can be replaced by a better implementation.

Every accepted ADR invariant has exactly one enforcement status:

- `executable`: references a deterministic argv-based check registered in `adr/.adr-system.yaml`;
- `manual`: records why deterministic verification is unavailable, what evidence can be inspected, and when automation should be reconsidered.

Manual invariants are reported as **not mechanically verified**. A prose string appearing in a file is not treated as proof that the architecture is followed.

Run the global gate through this repository's replaceable interface:

```sh
scripts/adr check --root .
```

An installed skill can fall back to its bundled reference launcher when a target repository does not provide an ADR command. The command validates the ADR system and index, verifies complete invariant coverage, executes each referenced check once without a shell, and exits non-zero on failure. The same command can be used in CI.

## Install

Copy or symlink the directories under `skills/` into your agent's skill directory. The included Claude plugin manifest exposes the same directory.

When upgrading from 2.x, remove obsolete `clarify-and-plan` and `execute-to-pr` installations. If a repository already has a version 2 ADR marker, ask `architect` to perform the semantic migration; do not update only `.adr-system.yaml`. Repositories without `adr/` need no data migration. See `CHANGELOG.md` for the release checklist.

## Development

```sh
./scripts/check.sh
```
