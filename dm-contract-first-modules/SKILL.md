---
name: dm-contract-first-modules
description: "Design or repair a module's contract before touching its internals. TRIGGER when creating a new module, service, plugin, or adapter; when changing an API, event, schema, message shape, or integration between two components; or when the user says 'interface', 'contract', 'API design', 'what should this expose', 'schema change', 'breaking change'. SKIP when the boundary is fixed and only internals change, and for deciding where boundaries go (use dm-map-module-boundaries)."
---

# Contract-First Modules

Use this skill to make module boundaries honest enough that an agent can trust the contract instead of reconstructing behavior from both sides.

## Contract Checklist

Define the contract before the implementation details when the change crosses a boundary.

Include:

- **Capability**: what the module promises in plain domain language.
- **Inputs**: accepted commands, parameters, messages, files, or states.
- **Outputs**: returned data, emitted events, writes, calls, and user-visible effects.
- **Errors**: validation failures, retries, partial failure, timeouts, and recovery expectations.
- **State transitions**: allowed before/after states and forbidden states.
- **Ownership**: which module owns each piece of data and which modules may read or mutate it.
- **Compatibility**: versioning, migration, backward compatibility, and deprecation rules.
- **Timing**: sync or async behavior, ordering, idempotency, concurrency, and retry semantics.
- **Examples**: representative happy path, edge case, and failure case.
- **Executable checks**: contract tests, schema validation, assertions, smoke tests, or golden examples.

## Honesty Test

A contract is not honest if important behavior is only discoverable by reading internals.

Probe for:

- hidden side effects;
- shared database or cache coupling;
- implicit framework lifecycle behavior;
- configuration that changes semantics;
- multiple consumers with different assumptions;
- mocks that differ from production behavior;
- ambiguous names that hide business rules.

If the contract is incomplete, extend the contract first or explicitly mark the unknown as an implementation risk.

## Contract Granularity

Keep contracts smaller than subsystems but larger than incidental functions. A useful contract names a stable capability, not every private step.

Prefer:

- `Pricing quotes an order under a versioned rule set`
- `Billing consumes CustomerRegistered and creates an account balance`
- `Search indexes documents after successful publication`

Avoid:

- contracts that mirror implementation call stacks;
- contracts that hide several unrelated capabilities behind one generic service;
- contracts that require a global architecture essay to understand.

## Output Shape

Produce contracts in this form when useful:

```markdown
## Module Contract

Capability:
Inputs:
Outputs:
Errors:
State transitions:
Ownership:
Compatibility:
Timing:
Examples:
Executable checks:
Open questions:
```

Keep open questions specific. Ask only for information that would collapse materially different designs or prevent a plausible wrong implementation.
