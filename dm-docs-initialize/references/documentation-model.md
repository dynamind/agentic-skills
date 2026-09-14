# Documentation model

The shape a living-documentation site takes. It is the shape two production sites use;
adapt names to the project, keep the roles.

## Two layers, one repository

| Layer | Reader | Location | Rule |
|---|---|---|---|
| Documentation site | humans first, agents second | `docs/` | Written to be read. The entry point is `docs/guide/index.md`. Rendered with VitePress. |
| Agent layer | agentic tools | `AGENTS.md`, `CLAUDE.md`, `.agents/` | An index plus always-on rules. Detail lives in modules or in `docs/`. See [agent-layer.md](agent-layer.md). |

Both layers are authoritative for what they hold. Neither restates the other; they link.
The root `README.md` is a signpost to both.

## The tree

```
docs/
  index.md                     home: role-based reading paths
  guide/index.md               Introduction: what the product is, what the site covers
  guide/business-context.md    who it is for, the process it supports
  guide/roadmap.md, how-we-work.md, ...
  glossary.md                  the domain vocabulary; one authoring place per term
  product/
    personas/                  one page per persona; index compares them
    features/                  one page per feature; index is the feature inventory
    business-rules/            when rules outgrow the feature pages (legacy apps)
    ideas.md                   register: observations and ideas, prefixed by who raised them
    questions.md               register: questions waiting on a human
  architecture/
    overview.md                the parts, conventions, and the ADR list
    diagrams.md                C4 context, container, component; Mermaid, theme-neutral
    technology-stack.md
    exceptions.md              register: EX-nnn deviations from accepted ADRs
    hazards.md                 register: findings with evidence (brownfield first pass)
    <language>-conventions.md  living rule pages with Wrong / Right pairs
    adrs/adr-NNN-kebab-title.md
  explanation/                 how a subsystem works and why; does not restate ADRs
  how-to/                      one task per page; "operations/" for a legacy app with runbooks
  reference/                   mirrors of external sources: wiki exports, legacy specs, chat digests
  public/                      static files the site serves (source PDFs, screenshots)
  archived/                    kept, not rendered (srcExclude)
```

A section exists when it has a page. Do not create empty sections, index pages that only
list children, or pages that promise content. A comment in a scaffolded page says what
belongs there; that is enough.

## Page kinds and their contracts

| Kind | Job | Shape |
|---|---|---|
| Home (`index.md`) | route by role | two to four reading paths, each a numbered list of links with one line of why |
| Introduction (`guide/index.md`) | orient | what the product is, a table of guide pages and what each brings, one link to Architecture |
| Explanation | make a subsystem understandable | scope statement, premise, how it works, constraints, related; depends on ADRs, never restates them |
| How-to | complete one task | imperative title, prerequisites, numbered steps with commands, verify, when it fails |
| Feature | say what the product does for whom | flow, business rules with sources, data, edge cases, related decisions |
| Persona | say who we build for | status and evidence basis in bold lines, who, what they do, what they fear, sources |
| Conventions | settle recurring style discussions | scope and status blockquote, one rule per section, Wrong / Right pairs |
| ADR | constrain | `# ADR-NNN: statement`, `## Status`, `## Context`, `## Decision`, `## Consequences`; alternatives only when disputed |
| Register | hold items until they land elsewhere | open section first, closed or answered section last, one format per file |
| Reference mirror | preserve an external source | dated, ids of the originals, secrets removed, links to the page that worked the content in |

Templates for each kind are in `../assets/pages/`. Copy the shape, not the placeholder text.

## Registers

Three registers carry what does not yet belong to a page:

- `docs/product/ideas.md`: observations, annoyances, ideas. Prefix each with who raised
  it. Committed work moves to the backlog and out of this file.
- `docs/product/questions.md`: one line per question, `**Q (who):** text` then
  `**A (date):** text`. References point outward from the register; code never points
  back at it. An answered question names the page where the answer landed.
- `docs/architecture/exceptions.md`: `EX-nnn` entries for deviations from accepted ADRs,
  each with what we do, which decision it departs from, why, what bounds it, and what
  ends it. An entry with no exit condition is an undocumented decision, not an exception.

A brownfield first pass adds a fourth: `docs/architecture/hazards.md`, findings from
reading code and history, each a fact with its evidence and a severity to be confirmed.

Registers have sections. Insert in the open section, in the file's format. Never append at
the bottom.

## Glossary

`docs/glossary.md` is the one page to read before working in the domain. Entries are
`#### Term` headings with one or two sentences of domain meaning. No code identifiers, no
mechanics. Domain terms stay in the language the business speaks. Group entries under
`##` headings when the list passes about twenty terms. No entry is added unprompted; the
bar is a term the business needs defined.

The site links the first mention of a term on every page to its glossary entry and shows
the first sentence of the definition as a tooltip. Write that first sentence so it stands
alone. See [vitepress.md](vitepress.md), Glossary linking.

## Metadata

No frontmatter on content pages. VitePress needs none, and a metadata block nobody
maintains is worse than none. State what matters in the page:

- an ADR carries `## Status` with state, date, and author;
- a snapshot (review, audit, migration status) opens with a blockquote:
  `> **Reviewed:** 2026-09-14` and `> **Scope:** ...`;
- a persona opens with `**Status:**` and `**Evidence basis:**` lines;
- a fact from a single unconfirmed source ends with *(unverified)*.

The only frontmatter in the tree is VitePress's own: `layout: home` on `index.md` when a
hero page is wanted, and Mermaid's `config: htmlLabels: true` inside a diagram.

## Links

- Inside `docs/`, link with relative markdown links ending in `.md`. The build resolves
  them and fails on a dead one.
- Files outside `docs/` (source, scripts, agent skills) are cited in code spans, not
  linked. The dead-link check cannot follow them, and a link that is never checked can
  become wrong without warning.
- Link text says why the destination matters, not "here".
- No em-dashes anywhere in the tree. A heading uses a colon where it needs a divider.

## Diagrams

Mermaid only, rendered natively by the site in light and dark. Theme-neutral: no `fill`,
no hex colors, no `style` or `classDef` with colors, no `%%{init}` themes. A node is a bold
name plus at most one qualifier line. Multi-line labels need `htmlLabels: true` and
backtick strings with real newlines; `<br/>` is dropped silently. Sequence-diagram labels
are one source line.
