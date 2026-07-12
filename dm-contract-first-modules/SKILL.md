---
name: dm-contract-first-modules
description: Design or repair module contracts before changing internals. Use when creating a module, changing an integration, defining APIs, events, schemas, service boundaries, plugin surfaces, adapters, or tests that should let agents reason about one side of a boundary without reading the other.
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
