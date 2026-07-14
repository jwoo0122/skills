---
name: workflow-router
description: Internal routing stage for the chained coding workflow. Use automatically from clarify-and-plan or for a model-detected codebase change; inspect repository instructions and the ADR index, judge clarification, ADR, execution, and verification independently, then activate the lightest safe internal flow without another user skill command. Do not present this as a direct user entry point.
user-invocable: false
---

# Workflow Router

Choose the lightest safe workflow while preserving the shared invariants.

## Load the shared policy

Activate `coding-workflow-core`. If nested activation is unavailable, locate and read the installed sibling `SKILL.md`.

## Inspect in low-to-high resolution

Before broad code inspection or any edit:

1. Read active repository instructions and the user's scope limits.
2. If `adr/index.yaml` exists, read it and select records relevant to likely paths, scopes, topics, and linked decisions. If it does not exist, continue without creating it.
3. Inspect only enough code, tests, public behavior, Git state, and external evidence to distinguish repository facts from choices that require the user.

Answer:

- Is this read-only work or an authorized change?
- What is the authorized delivery boundary: answer, plan, local change, commit, or draft PR?
- What result and observable checks define success?
- Which unanswered choices would materially change behavior, scope, risk, compatibility, or acceptance?
- Which accepted ADRs constrain or conflict with the request?
- What implementation units are actually separable?
- How much verification independence does the impact and uncertainty warrant?

Do not ask the user for file placement, naming, internal APIs, or conventions that repository evidence or an accepted ADR already determines.

Default an authorized change to `local-change` when the user does not mention commit, push, or a pull request. This least-authority default is not a reason to ask another question. Select `commit` or `draft-pr` only from explicit user authority.

## Select four facets

Record `mode=read-only|change` and the authorized delivery boundary before selecting the four adaptive facets. For read-only work, do not select or simulate an execution topology.

Choose each facet independently:

| Facet | Choices | Selection guidance |
|---|---|---|
| Clarification | `proceed`, `ask` | Ask only for unresolved material choices; size alone never forces questions. |
| ADR | `none`, `reference`, `reconcile` | Reconcile confirmed durable intent or conflicts; do not create a record for routine implementation detail. |
| Execution | `direct`, `delegate`, `decompose` | Scale to separability and integration cost, not questions, ADR edits, or line count. |
| Verification | `self`, `independent`, `multi-axis` | Scale to impact, uncertainty, cross-boundary effects, and reversibility cost. |

Record a short rationale and the relevant ADR IDs. Do not use fixed question counts, worker counts, changed-line thresholds, or a route matrix as a substitute for judgment.

Read [routing examples](references/routing-examples.md) when the facet combination is uncertain.

## Chain the lightest safe flow

- For read-only work, activate `diagnose-bug`, `evidence-research`, or `review-change` when its specialized contract fits; otherwise perform the bounded inspection directly. Do not activate an implementation stage. If ADR maintenance would be useful, report a proposed ADR action without mutating the repository.
- If `clarification=ask`, activate `clarify-and-plan` and transfer ownership of the remaining workflow to it. Do not resume a second ADR or execution tail after clarification returns.
- If `adr=reconcile` for an authorized change, give one coordinator or `maintain-architecture-decisions` write ownership and reconcile before dispatching implementation.
- If `adr=reference`, pass the relevant IDs and invariants into implementation and verification packets.
- For an authorized, sufficiently clear change, activate `execute-to-pr` with the selected execution and verification facets plus the explicit delivery boundary. Let that stage choose the concrete worker topology.
- Do not ask the user to invoke another skill or approve routine internal chaining.

If the harness cannot activate a named skill, locate and read the installed sibling `SKILL.md`. Honor limits such as “plan only,” “do not commit,” and “stop after tests.” Re-enter routing when the request changes materially or implementation reveals a new consequential choice.
