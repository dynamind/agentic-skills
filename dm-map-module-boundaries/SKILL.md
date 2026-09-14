---
name: dm-map-module-boundaries
description: "Map and reshape module boundaries so a change fits in one bounded context. TRIGGER when the user asks where something should live, how to split or carve up a subsystem, why a change keeps touching many packages, or says 'this is too coupled', 'module boundaries', 'hidden coupling', 'which layer owns this'. Also use before a refactor that spans 3+ packages. SKIP for single-module edits and for defining the API of one module (use dm-contract-first-modules)."
---

# Map Module Boundaries

Use this skill to make a codebase easier for agents and humans to reason about by aligning module boundaries with reasoning boundaries.

## Boundary Map

Start by identifying the smallest semantically complete unit that can own the requested behavior. Prefer existing module language from the repo over imposing a new architecture vocabulary.

Capture:

- **Purpose**: what behavior this module owns.
- **Inputs**: public calls, commands, events, files, tables, messages, or UI flows entering the module.
- **Outputs**: return values, events, writes, calls, side effects, logs, and user-visible effects.
- **State**: data the module owns, reads, caches, or mutates.
- **External dependencies**: APIs, databases, queues, filesystem, configuration, clocks, randomness, and framework callbacks.
- **Known callers and consumers**: where visible evidence shows use, plus where undiscovered use may exist.
- **Contract surface**: public interfaces, schemas, tests, examples, docs, and conventions.

## Reasoning Boundary Test

Ask whether a competent agent can make the requested change from bounded evidence.

Answer these questions:

- What files or artifacts must be loaded to understand the change?
- What behavior can be trusted through contracts instead of reading internals?
- Which relevant effects are hidden behind shared state, reflection, ambient context, global config, deployment wiring, or undocumented consumers?
- What evidence would reveal that the current slice is incomplete?
- Can the change be verified through local tests, contract tests, smoke tests, or observable behavior?

If the answer requires understanding many unrelated areas, mark the boundary as leaky and propose a smaller behavioral slice or a contract improvement before implementation.

## Boundary Quality Signals

Treat these as positive signals:

- The module has one coherent responsibility that can be named in domain language.
- The public surface is smaller than the implementation.
- Invariants are represented by types, checks, tests, schemas, or examples.
- External effects are explicit at the boundary.
- Internal changes can be made while public behavior stays stable.
- Tests fail when the contract is broken.

Treat these as risk signals:

- Behavior depends on shared mutable state outside the module.
- Callers depend on internals or data layout.
- Configuration or environment silently changes behavior.
- Tests mock away the real boundary.
- A change requires reading both sides of many integrations.
- Absence of visible callers is being treated as proof that no callers exist.

## Output Shape

For planning or review, produce a concise boundary brief:

```markdown
## Boundary Brief

Module:
Purpose:
Owned state:
Contract surface:
Trusted without inspection:
Must inspect:
Hidden coupling risks:
Verification:
Recommendation:
```

Keep the brief short enough that a human can verify it quickly. Escalate only the uncertainties that affect correctness.
