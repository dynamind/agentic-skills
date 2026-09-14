---
name: dm-bounded-agent-work
description: "Plan a software change as bounded, verifiable work before coding, including mapping module boundaries and defining the contract when the change crosses one. TRIGGER before any change likely to touch 3+ files or several modules; when the user says 'plan this', 'how should we approach', 'split this up', 'break this down', 'scope', 'what's the first step'; when they ask where something should live, why a change keeps touching many packages, or say 'too coupled', 'module boundaries', 'hidden coupling', 'which layer owns this'; or when creating a module, service, plugin, or adapter, or changing an API, event, schema, or integration ('interface', 'contract', 'API design', 'breaking change'). SKIP for one-file fixes, plain questions, work the user has already scoped precisely, and post-implementation review (use dm-understandability-review)."
---

# Bounded Agent Work

Use this skill to shape work so the required context approximately matches what an agent can safely load and verify. It is the single planning entry point: boundary mapping and contract design live in `references/` and are loaded only when the task calls for them.

## Task Frame

Define the work as a bounded change:

- **Intent**: what outcome the user wants.
- **Behavioral slice**: the smallest end-to-end behavior that proves progress.
- **Relevant module**: the primary owner of the behavior.
- **Trusted contracts**: boundaries that can be relied on without reading internals.
- **Evidence to load**: files, tests, schemas, docs, or examples required for correctness.
- **Evidence to avoid**: broad context that would distract without changing the decision.
- **Verification**: the command, test, check, or manual observation that proves the slice.

## Risk-Based Rigor

Scale process to stakes:

- **Light**: docs, local cleanup, small UI copy, simple config, exploratory spike. Use minimal planning and direct verification.
- **Standard**: ordinary feature or bug fix inside a clear module. Use a short task frame, inspect boundary evidence, implement, and run focused tests.
- **High**: auth, payments, migrations, data loss, security, concurrency, public APIs, cross-module contracts, or unclear ownership. Add explicit contract review, broader tests, rollback thinking, and human decision points.

Do not turn every task into a ceremony. Preserve conversational momentum.

## Routing

Decide depth from the task frame, then load only what applies:

- **Boundary unclear** (several candidate owner modules, a change that keeps touching many packages, possible hidden consumers, or any refactor spanning 3+ packages): read `references/boundary-brief.md` and produce a Boundary Brief before choosing the slice.
- **Crossing a contract** (new module, service, plugin, or adapter; a changed API, event, schema, message shape, or integration; or any High-rigor task): read `references/module-contract.md` and write the Module Contract before implementation.
- **Ambiguous requirement or diagnosis**: use `dm-hypothesis-space-reasoning`; when the reason for the work itself is in question, use `dm-problem-solution-provenance`.
- **After implementation** of a Standard or High task: run `dm-understandability-review` as the verification step.

A Light task loads no references. Do not produce a Boundary Brief or Module Contract for a change that stays inside one clear module.

## Stop Conditions

Pause and ask or investigate when:

- multiple plausible implementations have different user-visible behavior;
- the module boundary is unclear;
- hidden consumers or writers may exist;
- the verification path is missing;
- the change crosses a contract that is undocumented or untested;
- the current evidence would encourage a closed-world assumption.

If uncertainty is low and the blast radius is small, proceed.

## Human Attention Budget

When reporting progress, show only:

- what changed;
- what failed;
- what decision is needed;
- how to verify.

Keep audit detail available in artifacts or command output, but do not force the human to read process logs during normal collaboration.

## Output Shape

Use this plan format before substantial work:

```markdown
## Bounded Task Plan

Intent:
Slice:
Primary module:
Context to inspect:
Contracts to trust:
Risks:
Verification:
Decision needed:
```

For small tasks, collapse this to one or two sentences and proceed. Attach the Boundary Brief or Module Contract beneath the plan when Routing produced one.
