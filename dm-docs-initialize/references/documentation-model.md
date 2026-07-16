# Documentation Model

Use this default only after inspecting the repository. Adapt names and depth to the product rather than creating empty bureaucracy.

## Topic-first baseline

```text
Documentation Home
├── Overview
├── Getting Started
├── Features
├── Architecture
├── Interfaces
├── Development
├── Operations
├── Security, Privacy, and Compliance
├── Cookbook
├── Releases and Roadmap
├── Reference
└── Archive
```

The landing page routes by intent; it does not repeat the system overview. Suggested routes include new to the system, understand a feature, understand the design, make a change, investigate a problem, perform a task, and find an exact fact.

## Decisions before initialization

Make these choices visible instead of allowing preservation behavior to decide them accidentally:

| Decision | Recommended default |
|---|---|
| Site generator | Material for MkDocs when no existing tool governs the corpus |
| Existing scattered docs | Consolidate into the tree; use route-in-place only for justified consumers |
| Authoritative facts | Docs tree |
| Root narrative files | Thin `README.md` signpost and `AGENTS.md` operating instructions only |
| Section index nav label | `Overview`; use `Introduction` when the section itself is named Overview |
| ADR scheme | `docs/architecture/adrs/NNN-short-kebab-title.md`; reserve `000` |

## Page-level intent

Use Diataxis as an editorial compass:

- `tutorial`: acquire skill through a guided, reliable learning path;
- `how-to`: apply existing skill to achieve a bounded outcome;
- `reference`: retrieve exact, authoritative facts;
- `explanation`: build understanding of concepts, rationale, and trade-offs.

Use additional contracts when clearer:

- `landing`: route readers;
- `decision`: record a decision and rationale;
- `runbook`: support action under operational conditions;
- `release`: describe shipped change;
- `roadmap`: communicate planned direction.

Topic determines where a page lives. Intent determines how it is written. Do not make four giant Diataxis navigation buckets unless readers demonstrably seek them.

## Architecture decisions and diagrams

- Store ADRs under `docs/architecture/adrs/` using `NNN-kebab-case-title.md`.
- Reserve `000-record-architecture-decisions.md` for the ADR convention and begin system decisions at `001`.
- Put the ADR navigation entry immediately after Architecture.
- Use Mermaid for diagrams.
- Avoid fixed inline colors, diagram themes, and styling directives that fail across light and dark palettes.

## Metadata contract

Prefer repository-native frontmatter. When none exists, use:

```yaml
purpose: Explain what question this page answers.
audience:
  - developers
doc_type: explanation
authority: explanatory
lifecycle: current
owner: Team or role
last_reviewed: YYYY-MM-DD
sources:
  - path/to/evidence
```

Allowed values:

- `authority`: `authoritative`, `explanatory`, `generated`, `proposal`, `historical`, `superseded`;
- `lifecycle`: `draft`, `current`, `needs-review`, `archived`.

Do not use `status` for the document lifecycle in Material for MkDocs. Material reserves that field for navigation badges and will render an icon for pages that set it.

Use `sources` for evidence traceability, not as a substitute for semantic prose links.

## Repetition and authority

- Repeat enough context for a page to stand alone.
- Summarize related detail and link to its authoritative page.
- Keep exact facts such as configuration defaults, API fields, retention periods, and supported versions in one canonical location.
- Treat conflicting copies as a correctness problem, not merely a style problem.
- Keep the docs tree authoritative by default. Reduce the root README to product identity and semantic links after consolidating its detailed facts.

## Progressive disclosure

For explanation pages, prefer this descent when appropriate:

```text
Summary → relevance → mental model → normal flow → details → failure modes → related material
```

Do not force the same headings onto reference, tutorial, runbook, or landing pages. Provide consistency within a page contract rather than uniformity across all documents.

## Customization decisions

Before applying the baseline, decide:

- which sections have real material now;
- which documentation tool and navigation files already govern the corpus;
- which references are generated;
- where ADRs, runbooks, releases, and API specifications already live;
- whether security material needs restricted access;
- how redirects and archived content are handled;
- whether ownership is by person, team, or role.
- whether an existing MkDocs configuration, dependency runner, or publishing pipeline must be preserved.
- whether scattered documentation should be consolidated or deliberately routed in place;
- which root-level narrative files are explicit exceptions to the docs-tree authority policy.

Create shallow landing pages for justified empty sections. Do not fabricate product content to make the tree look complete.
