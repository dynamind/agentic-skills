---
name: dm-understandability-review
description: Review code, designs, tests, or architecture for how reliably humans and agents can infer correct behavior. Use when evaluating module design, large-codebase maintainability, hidden coupling, confusing tests, plausible reasoning errors, closed-world assumptions, or whether a change is safe for agentic implementation.
---

# Understandability Review

Use this skill to assess whether behavior can be reasoned about from bounded, discoverably complete evidence.

## Review Lens

Review understandability as three related properties:

- **Local comprehensibility**: the visible code or design can be understood without excessive mental bookkeeping.
- **Boundary completeness**: relevant external behavior is represented at the module boundary.
- **Uncertainty discoverability**: the system exposes when the current evidence is incomplete.

The goal is not aesthetic simplicity. The goal is fewer plausible wrong conclusions.

## Findings To Look For

Prioritize issues that make a reasonable agent or developer form a false mental model:

- hidden writes, reads, callbacks, retries, or consumers;
- shared state with unclear ownership;
- tests that pass while production behavior could fail;
- names that imply a narrower behavior than the code performs;
- documentation that states intent but omits failure or timing semantics;
- module boundaries that force nonlocal reasoning for routine changes;
- configuration, deployment, or environment behavior that is invisible in code;
- abstractions that split one concept across too many places;
- large modules where unrelated behaviors share lifecycle or state.

Also call out positive patterns worth preserving when they materially reduce reasoning risk.

## Closed-World Check

Before concluding something is absent, search or reason for how it might be hidden:

- dynamic dispatch or reflection;
- framework conventions;
- generated code;
- runtime configuration;
- database triggers or scheduled jobs;
- external consumers;
- event subscribers;
- scripts and operational runbooks.

Phrase uncertainty explicitly: "No evidence found in X; possible hidden paths are Y."

## Severity

Use severity by reasoning risk:

- **High**: likely to cause plausible incorrect changes, production divergence, data corruption, security risk, or broken cross-module behavior.
- **Medium**: creates avoidable ambiguity or verification gaps for future changes.
- **Low**: local clarity issue with limited behavioral risk.

Avoid long audit reports. A good review protects human attention.

## Output Shape

Lead with findings:

```markdown
## Findings

- [High|Medium|Low] Title
  Evidence:
  Why this harms understandability:
  Suggested repair:

## Open Questions

## Positive Signals

## Verification Gaps
```

If there are no material findings, say so and name any residual uncertainty.
