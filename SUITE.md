# Dynamind Agentic Skills Suite

This suite aligns software structure, documentation, and agent work with human reasoning boundaries. Its central premise is that agents perform more reliably when a change fits inside a bounded, understandable slice of evidence and everything outside that slice is represented by an honest contract or link.

## Shared principles

- Align module boundaries with reasoning boundaries.
- Make contracts strong enough that internals can remain hidden until they matter.
- Treat hidden coupling and undiscovered consumers as first-class risks.
- Make uncertainty visible instead of silently choosing one interpretation.
- Preserve why problems and solution branches exist so upstream choices can be reconsidered.
- Keep documentation traversable, authoritative, and progressively disclosed.
- Prefer concise outputs that humans can verify.

## Skill boundaries

### Modularity skills

`dm-bounded-agent-work` defines the work slice, acceptance evidence, and risk-scaled verification. Use it first when a request is broad or likely to exceed one reasoning boundary.

`dm-agentic-module-boundaries` maps modules, dependencies, consumers, and hidden coupling before implementation.

`dm-contract-first-modules` designs or repairs the contract across a module boundary, including inputs, outputs, errors, timing, and ownership.

`dm-hypothesis-space-reasoning` expands and compares plausible explanations when requirements or evidence are ambiguous, then identifies the smallest useful next check.

`dm-problem-solution-provenance` maps goals, observed problems, solution options, trade-offs, and newly introduced
problems. It distinguishes experienced needs from requested implementations and exposes downstream branches that an
upstream decision may invalidate.

`dm-understandability-review` evaluates whether humans and agents can form a reliable model of code, designs, tests, and boundaries.

`dm-new-project` scaffolds the preferred Quarkus, Vue, documentation, Terraform, and Azure DevOps monorepo. It is a project bootstrapper rather than a general architecture-review skill.

### Documentation skills

`dm-docs-initialize` creates a topic-first Material for MkDocs system with a landing page, navigation, Mermaid support, ADR conventions, authority and lifecycle metadata, archive boundaries, and page templates.

`dm-docs-ingest` inventories and reconciles code, tests, configuration, existing documents, and other bounded evidence before writing documentation. It preserves provenance and keeps conflicting reader intents in separate page contracts.

`dm-docs-garden` maintains an existing corpus in three modes: read-only audit, bounded synchronization after a source change, and structural gardening. It checks links, metadata, traversal, ADRs, Mermaid conventions, authority, and harmful duplication.

## Recommended compositions

### Large codebase change

```text
problem-solution-provenance (when solution framing matters)
                   → bounded-agent-work → module-boundaries → contract-first-modules (if needed)
                   → implementation → understandability-review
                   → docs-garden (to synchronize affected documentation)
```

Use hypothesis-space-reasoning at any point where the evidence supports multiple plausible interpretations. Feed the
result into problem-solution provenance when those interpretations imply different interventions.

### New project

```text
new-project → bounded-agent-work → module-boundaries → contract-first-modules
           → docs-initialize → docs-ingest → docs-garden
```

### Existing documentation corpus

```text
docs-ingest (missing or migrated knowledge) → docs-garden
```

For review-only work, use `docs-garden` in audit mode and do not edit files.

## Repository contract

The root `dm-*` directories are the installable skills and the source of truth for synchronization. `docs-skills/` and `modularity-skills/` retain the original pack documentation from the merge; the root `README.md` and this file are the unified pack-level documentation. The installer synchronizes only root skill directories and leaves unrelated global skills untouched.
