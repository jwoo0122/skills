---
name: review-change
description: Internal read-only review stage for routed coding work. Use after an implementation is ready for independent validation; review the fresh diff against the user brief and relevant ADRs, then separately review code quality and return only concrete, evidenced findings. Do not present this as a direct user entry point.
user-invocable: false
---

# Review Change

Review independently without editing files, applying fixes, committing, or resolving findings. Use checks that are safe for the current worktree.

When assigned one review axis, perform only that pass and do not infer the other reviewer's result. When assigned a combined independent review, perform both passes while keeping their findings in separate groups.

## Start from fresh evidence

- Run the ADR conformance gate when the repository has `adr/`; report a failing gate as an architecture or verification finding rather than treating it as a soft warning.
- Read repository instructions, the user brief, acceptance checks, relevant ADRs, the base state, the complete task diff, and verification output.
- Do not rely on the implementer's explanation, suspected weak spots, or self-review as proof.
- Separate task-owned changes from unrelated pre-existing work. Review only the requested scope, but report an overlap that prevents reliable attribution.

## Pass 1: specification and architecture

Check the diff against required behavior, constraints, non-goals, observable acceptance checks, and relevant ADR invariants. Look for omissions, unintended behavior changes, compatibility gaps, and missing or unjustified ADR impact.

## Pass 2: change quality

Independently inspect correctness, failure paths, boundary cases, security and data risks, concurrency, performance, public contracts, regression coverage, verification integrity, and unrelated churn. Apply these lenses only where the changed behavior makes them relevant. Do not report style preferences or speculative refactors.

Run focused non-mutating checks when they can confirm or reject a suspected issue. A test pass is evidence, not proof that no defect exists.

## Return concrete findings

Report a finding only when it is actionable and supported by the diff or reproducible evidence:

```text
priority: P0 | P1 | P2 | P3
title:
category: specification | architecture | quality | verification
location:
evidence:
violated_requirement_or_invariant:
impact:
minimal_remediation:
verification:
```

- `P0`: unsafe to proceed; destructive, security-critical, or broadly breaking.
- `P1`: required behavior is wrong or a serious regression is likely.
- `P2`: bounded correctness or maintainability defect worth fixing before merge.
- `P3`: low-impact issue with clear value; omit mere preference.

Keep locations tight and explain the triggering input or execution path. Group duplicates by root cause and order findings by priority.

If there are no findings, say so explicitly and report residual risks or checks not run. Return specification findings and quality findings as separate groups so one clean pass cannot mask the other.
