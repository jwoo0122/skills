# Routing examples

Use these combinations as calibration, not as an exhaustive decision table.

| Request | Clarification | ADR | Execution | Verification | Why |
|---|---|---|---|---|---|
| Explain why a test is flaky without changing files. | `proceed` | `reference` if relevant, otherwise `none` | no implementation | `self` | Read-only scope is authoritative. |
| Fix an obvious typo in CLI help. | `proceed` | `none` | `direct` | `self` | The result is bounded, reversible, and locally checkable. |
| Apply a fully documented migration across several packages. | `proceed` | `reference` | `decompose` | `independent` or `multi-axis` | Work size affects execution, not whether a design question exists. |
| Change one authorization condition with unclear policy semantics. | `ask` | `reconcile` | `direct` or `delegate` | `independent` | A small diff can encode durable, high-impact intent. |
| Improve first-run onboarding without a defined outcome. | `ask` | `none` until durable architectural intent emerges | decide after clarification | decide from the resolved design | The product behavior and acceptance boundary are unresolved. |
| Implement behavior already fixed by an accepted ADR. | `proceed` | `reference` | scale to the work | scale to impact | Do not ask the user to repeat a recorded decision. |
| Make a request that contradicts an accepted ADR. | `ask` | `reconcile` | wait | plan independent review | Do not silently favor either the request wording or stale architecture context. |
| Fix code that violates a still-valid ADR invariant. | `proceed` | `reference` | scale to the edit | at least as strong as the failure impact | Fix the implementation; do not append a duplicate decision. |

Route by unresolved consequences, durable intent, separability, and verification risk. Prompt length, question count, ADR diff size, and worker count are not proxies for those judgments.
