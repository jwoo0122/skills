---
name: execute-to-pr
description: Internal execution coordinator for the chained coding workflow. Use after workflow-router determines that a change is ready, adapting direct work, bounded implementer subagents, independent reviewers, ADR reconciliation, verification, and delivery up to the user's explicit local, commit, or draft-PR boundary. Do not present this as a direct user entry point or use it for read-only requests or when the user forbids implementation.
user-invocable: false
---

# Execute and Deliver

Coordinate an authorized, sufficiently clear change through verified delivery. Own the whole intent and integration even when subagents perform bounded work.

## Load the shared policy

Activate `coding-workflow-core` if it is not already active. If nested activation is unavailable, locate and read the installed sibling `SKILL.md`.

## Check entry conditions

Start only when all are true:

- the user requested a codebase change;
- the outcome and scope are sufficiently clear;
- no material blocking decision remains;
- observable acceptance checks are known; and
- relevant accepted ADRs have been read and any architectural conflict has been reconciled; and
- the authorized delivery boundary is explicit; and
- active instructions permit implementation.

Return to `clarify-and-plan` if implementation exposes a material unresolved decision.

## Choose execution and verification independently

Judge execution topology from implementation complexity, ownership boundaries, context pressure, and safe parallelism. Judge verification topology separately from architectural significance, behavioral risk, and the chance of a plausible but wrong implementation.

- Work directly when the change is bounded and delegation would add more coordination than useful isolation.
- Delegate one bounded packet when implementation is context-heavy but coherent.
- Decompose into vertical slices only when slices have independent acceptance and explicit blocking edges.
- Parallelize writers only in isolated worktrees with disjoint ownership. Keep one writer in a shared worktree.
- Use an independent reviewer for architecturally significant, materially risky, or non-trivial changes even when the code diff is small.
- Do not derive subagent count from question count, ADR volume, changed line count, or a fixed small/medium/large table.

Read [the implementation loop](references/implementation-loop.md) when production behavior or tests must change. Read [work packets](references/work-packets.md) before delegating or decomposing work.

## Establish a safe Git baseline

Inspect status, branch, upstream, remotes, and the repository's default branch before editing.

- Record which pre-existing changes belong to the user.
- Do not include unrelated changes in tests, formatting, staging, commits, or the PR.
- If isolation is not reliable, stop and explain the collision.
- For `local-change`, preserve the current branch and worktree; do not create or switch branches merely to edit locally.
- For `commit` or `draft-pr`, create a focused work branch when on a default or protected branch, unless the harness already provided an isolated task branch or worktree.
- Never switch branches in a way that risks uncommitted user work.

## Coordinate implementation

If working directly, follow the implementation loop and make the smallest coherent change. If delegating, give the implementer only the accepted brief, relevant repository instructions, owned paths, relevant ADR IDs and invariants, acceptance checks, verification commands, baseline, and forbidden actions.

Activate `diagnose-bug` when a reliable red feedback loop or cause is missing. Activate `evidence-research` when implementation depends on unstable external facts, standards, or third-party behavior. Do not ask either specialist to implement unrelated production changes.

Implementers may edit only their owned scope. They must return changed paths, behavior implemented, checks and outcomes, open risks, and unexpected decisions. They must not commit, push, create a pull request, or silently resolve an architectural conflict.

Reserve every `adr/**` path for the coordinator's architecture-decision writer role. Implementers, diagnosticians, researchers, and reviewers may return ADR findings but must not edit those paths, even sequentially.

## Verify and iterate

- Run targeted checks while iterating.
- Run every repository-required pre-PR check that applies to the changed area.
- Capture command names and outcomes.
- Fix in-scope failures and rerun until they pass.
- If a failure is pre-existing, prove that from the baseline or untouched area; do not merely label it pre-existing.
- Do not edit verification configuration or snapshots unless the requested behavior legitimately changes them and the diff is reviewed.

## Reconcile architecture decisions

Reassess the completed diff against the relevant ADR subset before review.

- If it follows an accepted decision, do not edit the ADR merely to restate the implementation.
- If an accepted decision's scope, invariant, consequence, or enforcement pointer became stale, invoke `maintain-architecture-decisions` through the coordinator's single-writer role.
- If the implementation would reverse or contradict accepted intent, stop and return to `clarify-and-plan`; never rewrite the ADR after the fact to justify the code.
- When a new durable architectural intent was resolved during clarification, persist it before dispatch and refine only concrete consequences discovered during implementation.

## Review at the selected depth

For `verification=self`, let the coordinator inspect the complete task diff and verification evidence without spawning a reviewer. For `verification=independent`, activate one fresh `review-change` context. For `verification=multi-axis`, activate separate acceptance/specification and standards/risk reviewer contexts; do not give either reviewer the other's findings.

Give reviewers the accepted brief, relevant ADRs, raw task diff, repository rules, and verification evidence. Keep them read-only and independent of the implementer's rationale.

Require findings to identify severity, evidence, affected file or decision, violated requirement or invariant, and consequence. The coordinator decides which findings are valid. Return accepted findings to the original bounded implementer when its local context remains useful; use a new implementer only when ownership or independence requires it. After fixes, use fresh review context for the latest full diff.

At minimum, ensure the review covers:

- missed requirements and edge cases;
- accidental API or behavior changes;
- unrelated files or broad formatting churn;
- secrets, generated artifacts, debug output, or temporary files;
- test assertions that cannot fail for the regression;
- changes to verification that weaken the gate.

Fix accepted findings and rerun affected checks. Do not let a reviewer patch the files it is judging.

## Stop or deliver at the authorized boundary

Follow [Git and PR guardrails](references/git-and-pr-guardrails.md).

1. For `local-change`, stop after implementation, ADR reconciliation, verification, and review.
2. For `commit`, stage only task-owned paths or hunks, confirm the staged diff, and create the minimum coherent commit set in repository style. Do not push.
3. For `draft-pr`, perform the commit steps, push the current branch without force, create a draft pull request with a concise summary and exact verification evidence, and query the provider to confirm its URL and draft state.

Never escalate `local-change` to commit or `commit` to push merely because tools and credentials are available.

Prefer an available purpose-built GitHub integration; otherwise use authenticated `gh`. Do not fabricate a URL when authentication, remote access, or PR tooling is unavailable.

## Report the outcome

Return:

- a concise change summary;
- verification commands and pass/fail results;
- commit identifier when the boundary included a commit;
- draft pull request URL and confirmed draft state when the boundary was `draft-pr`; or
- the exact blocking condition and completed local state.

Also report any ADR created, revised, superseded, or deliberately left unchanged after reconciliation, and summarize delegated implementation and independent review without exposing unnecessary internal transcripts.
