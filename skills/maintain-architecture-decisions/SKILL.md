---
name: maintain-architecture-decisions
description: Internal architecture-decision maintenance for the chained coding workflow. Use when a durable architectural intent is confirmed, an existing decision needs correction or reversal, or code and accepted decisions conflict. Maintain a semantic living ADR system without chronological document accumulation. Do not present this as a direct user entry point.
user-invocable: false
---

# Maintain Architecture Decisions

Preserve architectural intent that future agents cannot reliably recover from code alone.

## Read before deciding

If `adr/index.yaml` exists, read it before architecture-sensitive clarification, implementation, or review. Load only records relevant to the affected paths, scopes, and decision relationships.

Treat an accepted ADR as current intent, not immutable truth. A newer explicit user decision may revise, supersede, or retire it. Never silently implement through a conflict.

Read [the decision policy](references/decision-policy.md) before creating or structurally changing a record.

## Classify the effect

Use the lightest applicable action:

- `none`: no durable architectural intent is involved.
- `reference`: follow an existing decision without editing it.
- `improve`: clarify metadata, scope, invariants, enforcement, or relationships without changing the decision.
- `revise`: change the answer to the same stable decision question in the existing record.
- `create`: add a record only for a genuinely new stable decision question.
- `supersede`: split, merge, or replace decision questions and link both directions.
- `retire`: mark a decision whose context no longer exists.
- `clarify`: stop when the durable intent cannot be established from the repository, evidence, or user.

Do not create an ADR for local implementation details, routine bug fixes, test names, private helpers, or behavior already obvious from code and public contracts.

## Keep one logical writer

The coordinator owns ADR writes. Implementers, researchers, diagnosticians, and reviewers return relevant IDs, conflicts, and proposed actions; they do not edit `adr/` concurrently. The coordinator may apply this skill directly or delegate one bounded ADR-maintainer task.

## Maintain the living structure

Initialize `adr/` when the first durable architectural decision is confirmed:

```sh
<skill-root>/scripts/adr init --root <repository-root>
```

Initialization marks ownership and schema version. Refuse to adopt a non-empty `adr/` without a compatible marker; never follow symlinks outside the repository.

Store records as `adr/records/<scope>/<question>.md`. Use semantic IDs such as `identity.session-authority`; never use chronological numbers. Update the existing record when the stable question is unchanged.

After editing records, rebuild and validate the index:

```sh
<skill-root>/scripts/adr reindex --root <repository-root>
<skill-root>/scripts/adr validate --root <repository-root>
```

The launcher checks candidate Python interpreters by importing PyYAML, then runs the structural tool with the selected interpreter. It never installs packages. Set `ADR_PYTHON` to override discovery. The tool validates syntax, duplicate keys, IDs, status, paths, relationships, complete sections, and index freshness. Reindexing replaces the index atomically and can recover a missing index in a marked ADR system. It does not decide whether an intent is architecturally important.

## Hand off

Before implementation, provide the coordinator with:

```text
adr_action:
relevant_ids:
changed_ids:
conflicts:
implementation_invariants:
```

Return to clarification if a conflict remains. Otherwise give implementers and reviewers only the relevant records and invariants.
