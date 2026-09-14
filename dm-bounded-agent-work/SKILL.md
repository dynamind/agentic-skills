---
name: dm-bounded-agent-work
description: "Turn a software request into bounded, verifiable tasks before coding. TRIGGER before any change likely to touch 3+ files or several modules, and whenever the user says 'plan this', 'how should we approach', 'split this up', 'break this down', 'scope', 'what's the first step', or hands over a vague or large feature request. This is the entry point for planning; it routes to dm-map-module-boundaries, dm-contract-first-modules, and dm-understandability-review as needed. SKIP for one-file fixes, questions, and work the user has already scoped precisely."
---

# Bounded Agent Work

Use this skill to shape work so the required context approximately matches what an agent can safely load and verify.

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

For small tasks, collapse this to one or two sentences and proceed.
