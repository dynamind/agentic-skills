---
name: dm-docs-ingest
description: Populate or revise repository documentation from bounded source evidence such as code, tests, configuration, schemas, ADRs, runbooks, release history, legacy documents, wiki exports, and stakeholder-provided material. Use when documenting a subsystem, migrating existing documentation into a new tree, reconciling multiple sources, or building trustworthy onboarding material with traceable evidence. Do not use for empty-tree scaffolding or general documentation cleanup.
---

# DM Docs Ingest

Turn bounded evidence into trustworthy documentation while preserving conflicts, provenance, and uncertainty.

## Workflow

1. Define a bounded ingestion slice.
   - Name the subsystem, feature, journey, document set, or question being documented.
   - Identify intended readers and the decisions or tasks the result must support.
   - Avoid repository-wide ingestion in one pass unless the corpus is genuinely small.
2. Discover local documentation rules.
   - Read repository instructions, `mkdocs.yml` when present, the documentation landing page, navigation, metadata conventions, glossary, and nearby pages.
   - Preserve established vocabulary and page authority.
   - If no contract exists, apply the fallback model in [references/page-contracts.md](references/page-contracts.md) and propose it explicitly.
   - Respect the selected authority and consolidation policy. Treat the docs tree as authoritative by default and root `README.md` as a signpost rather than a second source of facts.
3. Build an evidence inventory before writing.
   - Search code, tests, configuration, schemas, deployment files, operational artifacts, existing docs, and history relevant to the slice.
   - Read [references/evidence-and-authority.md](references/evidence-and-authority.md) when sources differ or authority is unclear.
   - Record claims, evidence, contradictions, confidence, and intended destinations using [references/source-mapping.md](references/source-mapping.md).
4. Reconcile rather than blend.
   - Treat code as evidence of current implementation, tests as evidence of enforced behavior, documentation as stated intent, decisions as rationale, and runtime evidence as deployed behavior.
   - Never silently choose a convenient source when authoritative sources disagree.
   - State what is known, what is inferred, and what remains unverified.
5. Design the page set.
   - Organize by recognizable system concerns.
   - Use the reader's primary intent to select page contracts.
   - Split pages whose tutorial, procedure, reference, and explanation responsibilities fight one another.
   - Keep canonical facts in one authoritative location; summarize and link elsewhere.
   - Read [references/page-contracts.md](references/page-contracts.md) before writing mixed or unfamiliar artifact types.
6. Write from outside inward.
   - Begin with purpose, boundaries, terminology, normal behavior, and the simplest useful mental model.
   - Add technical detail, exceptions, failure modes, operational implications, and evidence only as needed.
   - Use semantic link text that explains the destination's relevance.
   - Preserve negative boundaries: state what the page does not cover when confusion is likely.
   - Use Mermaid for diagrams. Prefer structure and labels over fixed colors; avoid diagram-local styles and themes unless both light and dark rendering are verified.
   - Store new ADRs under `docs/architecture/adrs/` as `NNN-kebab-case-title.md`, then update the ADR index and MkDocs navigation. Reserve `000` for the ADR convention.
7. Validate against evidence.
   - Re-read every material claim against its supporting source.
   - Check links and local documentation builds when available.
   - Search for contradictions introduced elsewhere by the new pages.
   - Mark incomplete sections honestly instead of filling them with plausible prose.
   - Run `python3 -m mkdocs build --strict` when the repository uses MkDocs.

## Existing Documents

When migrating legacy or external material:

- classify each source as current, explanatory, proposed, historical, superseded, or unknown;
- extract reusable claims instead of copying its old navigation wholesale;
- preserve attribution and useful historical context;
- quarantine unresolved conflicts rather than laundering them into current documentation;
- archive source documents only when preservation and redirect behavior are clear.
- when initialization consolidated pages losslessly, reconcile their claims at the new path, remove temporary migration notices after verification, and change `lifecycle: needs-review` to `lifecycle: current` only when evidence supports it;
- update the thin root README only when authoritative destinations or stable links change.

## Boundaries

- Do not infer business purpose solely from class names, endpoints, or database tables.
- Do not describe intended behavior as implemented behavior without evidence.
- Do not document every implementation detail; prefer stable contracts, important flows, invariants, and failure modes.
- Do not broaden the slice silently. Report adjacent gaps as follow-up candidates.
- Do not introduce PlantUML, Graphviz, hand-authored SVG, or fixed-color Mermaid when the repository contract specifies Mermaid.
- Do not move scattered documents back outside the authoritative docs tree merely to preserve historical paths.

## Handoff

Conclude with:

- documented scope and readers;
- created or updated pages;
- strongest evidence used;
- contradictions and unresolved questions;
- unexamined boundaries;
- recommended next ingestion or gardening task.
