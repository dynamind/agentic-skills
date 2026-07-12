# Dynamind Agentic Modularity Skills

This suite helps Codex reason about large codebases through bounded modules, explicit contracts, and honest uncertainty.

The source idea is that agentic AI performs better when architectural boundaries align with reasoning boundaries: a change should fit inside a bounded, understandable slice of evidence, while other modules are represented by honest contracts.

## Skills

- `dm-agentic-module-boundaries`: map module boundaries and identify hidden coupling before implementation.
- `dm-contract-first-modules`: define contracts that let one side of a boundary be trusted without reading the other.
- `dm-understandability-review`: review code or design for plausible reasoning errors, hidden behavior, and closed-world assumptions.
- `dm-hypothesis-space-reasoning`: handle ambiguity by expanding and reducing multiple plausible hypotheses.
- `dm-bounded-agent-work`: turn requests into agent-sized, verifiable tasks with risk-scaled rigor.
- `dm-new-project`: scaffold Roy's preferred Quarkus, Vue, docs, Terraform, and Azure DevOps monorepo.

## Principles

- Align module boundaries with reasoning boundaries.
- Make contracts strong enough that internals can stay hidden until they matter.
- Treat hidden coupling and undiscovered consumers as first-class risks.
- Express uncertainty through the remaining hypothesis space.
- Prefer concise, human-verifiable outputs over process-heavy reports.

## Suggested Use Together

For a large codebase change:

1. Use `dm-bounded-agent-work` to define the slice and verification.
2. Use `dm-agentic-module-boundaries` to locate the reasoning boundary.
3. Use `dm-contract-first-modules` if the change crosses a boundary.
4. Use `dm-hypothesis-space-reasoning` when the question is under-specified.
5. Use `dm-understandability-review` before accepting the design or implementation.

For a new project, use `dm-new-project` first, then use the other skills to keep the codebase understandable as it grows.
