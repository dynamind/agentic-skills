# Evidence and Authority

Do not use one universal source-precedence ladder. Authority depends on the claim.

| Claim | Strong evidence | Common trap |
|---|---|---|
| Current implementation | code, generated artifacts | treating design prose as runtime truth |
| Enforced behavior | relevant tests plus production path | assuming mocked tests cover real wiring |
| Public contract | schema, API specification, contract tests | inferring it from one implementation |
| Deployed behavior | runtime configuration, manifests, telemetry | assuming repository defaults are deployed |
| Business intent | product decisions, accepted requirements, domain experts | deriving purpose from technical names |
| Design rationale | accepted ADRs and decision records | inventing a rationale that fits current code |
| Operational procedure | exercised runbooks, incident evidence | trusting an untested command sequence |
| Historical state | versioned docs, releases, history | presenting old truth as current truth |

## Reconciliation rules

1. State the claim being evaluated.
2. Identify the evidence type needed for that claim.
3. Record visible agreement and conflict.
4. Prefer direct, current, enforced evidence within its proper scope.
5. Mark inference explicitly.
6. Preserve unresolved conflict as a finding or question.

Use phrases such as:

- `Implemented behavior:` for directly supported runtime structure.
- `Stated intent:` for accepted but not verified prose.
- `Inferred from:` when connecting evidence that does not state the claim directly.
- `Unverified:` when an important boundary was not inspected.
- `Conflict:` when credible sources disagree.

Absence of evidence is not proof of absence. Search for generated code, framework conventions, dynamic wiring, runtime configuration, external consumers, database behavior, schedules, and operational scripts before closing a boundary.
