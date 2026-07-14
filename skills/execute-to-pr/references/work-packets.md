# Work packets

Use work packets to preserve the coordinator's full context while giving each implementer only what it needs.

## Decompose vertically

Prefer a tracer-bullet slice that crosses the necessary layers and has its own observable acceptance. Do not split solely by file type or technical layer when that creates partially integrated work with no independent verification.

Record blocking edges between packets. Dispatch only the unblocked frontier. Keep cross-cutting migrations sequential unless an expand-contract sequence makes old and new forms coexist safely.

## Implementer input

```text
Role:
Goal:
Required behavior:
Non-goals:
Constraints:
Baseline:
Owned paths:
Relevant ADR IDs and invariants:
Acceptance checks:
Verification commands:
Artifacts to read:
Forbidden actions:
```

Forbidden actions always include editing `adr/**`, resolving product or architectural ambiguity, committing, pushing, and creating a pull request. They also include editing outside the packet's owned implementation scope.

## Implementer output

```text
Status:
Changed paths:
Behavior implemented:
Red/green or equivalent evidence:
Checks and outcomes:
Open risks:
Unexpected decisions or ADR conflicts:
```

## Reviewer packet

Give a fresh reviewer the accepted brief, relevant ADRs, repository rules, baseline and latest raw diff, and verification evidence. Do not include the implementer's persuasive narrative or another reviewer's findings. Reviewers return findings and residual risks, never patches.
