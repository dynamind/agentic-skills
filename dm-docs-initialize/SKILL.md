---
name: dm-docs-initialize
description: "Set up a repository's living-documentation system: a VitePress docs site with role-based entry points, three-digit ADRs, an exceptions register, ideas and questions registers, a glossary, theme-neutral Mermaid, plus the agent layer (AGENTS.md index, CLAUDE.md, .agents/ modules with the writing guide). Includes the brownfield first pass that writes orientation pages from code, wiki, and chat evidence with uncertainty marked. TRIGGER when the user says 'set up docs', 'add vitepress', 'create a docs folder', 'ADR structure', 'documentation skeleton', 'restructure the docs tree', 'first documentation pass', 'document this brownfield repo', 'add AGENTS.md', or a repo has no docs system and one is requested. SKIP for documenting one subsystem in depth (dm-docs-ingest) and for fixing existing docs (dm-docs-garden)."
---

# DM Docs Initialize

Establish the living-documentation system: a docs site written for humans first, an agent
layer written for tools first, and the registers that hold what does not yet belong to a
page. Do not state facts that have not been investigated.

## Writing rules

Every page, register entry, `AGENTS.md`, and handoff this skill produces obeys these rules
from the first draft. Read `assets/agents/writing-guide.md` in full before writing the first
page; it is the complete rule set and is also what the scaffold installs as
`.agents/writing-guide.md`. The short form:

- **Simplified Technical English, US spelling.** Short sentences. One idea per sentence.
  Active voice. Plain words. One term for one thing. No metaphor, idiom, or rhetoric.
- **English**, unless the user says otherwise. Domain terms stay in the language the
  business speaks and go in the glossary.
- **Open with what the reader gets.** A page starts with what it covers and who it is for,
  not with history or a definition.
- **No frontmatter on content pages.** State in the page: `## Status` on an ADR, a dated
  blockquote on a snapshot, `**Status:**` and `**Evidence basis:**` lines on a persona.
- **Mark what is not confirmed.** A fact from a single unconfirmed source ends with
  *(unverified)*. A verified fact names its source. No `TODO`, no `needs-review`.
- **No ticket IDs** in docs. A link to the backlog is allowed.
- **Links inside `docs/` are relative markdown links ending in `.md`.** Files outside
  `docs/` are cited in code spans, never linked.
- **Headings are short noun phrases.** A heading that is a link target uses a colon, never
  an em-dash; the slugifier breaks on it. In prose, a colon or a second sentence beats an
  em-dash. The register separators (`**Q: who** — text`) are a fixed format and stay.
- **Tables for parallel facts, prose for argument.** A list item is one or two sentences.
- **Mermaid only, theme-neutral.** No fill, hex color, `style`, `classDef` color, or
  `%%{init}`. A node is a bold name plus at most one qualifier.
- **Registers keep their format.** Insert in the open section, in the file's own format.
  Never append at the bottom.
- **Commit messages**, when the user asks for one: the subject says what changed, the body
  carries only what the diff cannot show, the ticket key at the end of the subject only.

## Workflow

1. **Inspect the repository.** Read `assets/agents/writing-guide.md` first (see Writing rules).
   - Read `README.md`, `CLAUDE.md`, `AGENTS.md`, any `.cursorrules` or copilot file, and
     every existing docs folder, wiki export, ADR, and runbook.
   - Identify the project profile: active product, proof of concept, or frozen legacy app
     maintained by few people. The profile decides which sections apply and whether ADRs
     are written now.
   - Identify the existing docs generator, if any. Check Node availability
     (`node --version`, npm 11.10 or later for `min-release-age`).
   - Preserve local terminology and the language of domain terms.
2. **Settle the decisions.** Read [references/migration-and-authority.md](references/migration-and-authority.md).
   - Consolidate scattered documents into `docs/` or route in place. Default: consolidate.
     Present the old-to-new map before moving anything.
   - Site name, dev port, backlog URL, ticket key pattern.
   - Whether the agent layer is created now. Default: yes. An existing `CLAUDE.md` with
     content is folded, never overwritten; see [references/agent-layer.md](references/agent-layer.md).
3. **Scaffold.** Read [references/documentation-model.md](references/documentation-model.md)
   and [references/vitepress.md](references/vitepress.md).
   - Run `python3 scripts/scaffold_docs.py --root <repo> --site-name "<name>" --dry-run`,
     then without `--dry-run`. It is additive: existing files are reported, not replaced.
     Pass `--overwrite` only when the user says so.
   - Adapt an existing VitePress config instead of replacing it. Another generator that
     governs the corpus stays unless the user wants to switch; then record the switch.
   - The scaffold creates only pages with content: home, introduction, glossary, the three
     registers, the architecture overview. Sections grow when pages land. No empty index
     pages, no placeholder ADRs.
4. **Build the agent layer.**
   - `AGENTS.md` from the template: what this is, the *You are… / Read* table, always-on
     rules, stop-and-ask, keeping-this-honest. Fill *What this is* from evidence only.
   - `CLAUDE.md` is `@AGENTS.md`. `.agents/writing-guide.md` is always present.
     `.agents/decisions.md` when the project has decisions. Other modules when an area has
     rules a task must not override.
5. **Consolidate existing material** in the chosen mode: `git mv`, sidebar entries, link
   rewiring, a dated *Moved* notice on pages whose facts are not yet re-checked.
6. **Run the brownfield first pass when asked**, or when the repository has no docs and
   the user wants a first version. Read [references/brownfield-first-pass.md](references/brownfield-first-pass.md).
   Write the orientation pages from code, mirrored wiki pages, and digests, in the listed
   order, and stop when the evidence runs out. Mark single-source facts *(unverified)*.
   Put every gap that needs a human in `docs/product/questions.md`. Findings go in
   `docs/architecture/hazards.md`.
7. **Verify.**
   - `npm --prefix docs install` (ask before the first install), then
     `npm --prefix docs run docs:build`. The build fails on dead relative links.
   - Every page is in the sidebar. A term from the glossary is linked and shows its tooltip
     on a page that mentions it. Mermaid diagrams are theme-neutral and render in light
     and dark. `docs/node_modules/`, `docs/.vitepress/cache/`, `docs/.vitepress/dist/`
     are git-ignored.
   - Moved files kept their history. The old-to-new map matches the tree.
   - Propose a CI step that builds the docs first and fails fast.
8. **Hand off.** Do not commit; the user reviews first.

## Boundaries

- Do not populate architecture, features, or operations from class names or endpoint
  names. Evidence or *(unverified)*.
- Do not create empty sections, index-only pages, or placeholder ADRs. A comment in a
  scaffolded page says what belongs there.
- Do not add frontmatter to content pages. State in the page: `## Status` on an ADR, a
  dated blockquote on a snapshot, *(unverified)* on a fact.
- Do not weaken a decision to match reality. Register the deviation as `EX-nnn`.
- Do not write ticket IDs in docs. The backlog link is allowed.
- Do not run `npm` against the repository root. Always `--prefix docs` or `cd docs &&`.
- Do not overwrite a `CLAUDE.md` that has content. Fold it.
- Do not make this skill a prerequisite for ingestion or gardening.
- Do not write a page and fix its language afterward. The first draft follows the writing
  rules; a rewrite pass is not part of the workflow.

## Resources

- `scripts/scaffold_docs.py`: additive scaffold of the VitePress site and the agent layer.
  `--dry-run`, `--overwrite`, `--without-agents`, `--port`, `--backlog-url`.
- `assets/vitepress/`: `package.json`, `.npmrc`, `config.mts`, theme, and the `glossary/`
  build-time plugin that links term mentions to `docs/glossary.md` with tooltips.
- `assets/pages/`: templates per page kind (home, introduction, glossary, registers,
  ADR, how-to, explanation, feature, persona, hazards, reference mirror, conventions).
  Copy the shape, not the placeholder text.
- `assets/agents/`: `AGENTS.md`, `CLAUDE.md`, `.agents/writing-guide.md`,
  `.agents/decisions.md`.
- [references/documentation-model.md](references/documentation-model.md): the tree, page
  kinds and contracts, registers, glossary, metadata, links, diagrams.
- [references/agent-layer.md](references/agent-layer.md): `AGENTS.md` section by section,
  where a fact goes, folding an existing `CLAUDE.md`.
- [references/vitepress.md](references/vitepress.md): files, npm rules, config decisions,
  sidebar, verification, CI.
- [references/brownfield-first-pass.md](references/brownfield-first-pass.md): evidence
  order, the page set, uncertainty marking, mirrors, hazards.
- [references/migration-and-authority.md](references/migration-and-authority.md):
  consolidate or route in place, authority, initialize versus ingest.

## Handoff

Conclude with:

- the entry points: `docs/guide/index.md` and `AGENTS.md`;
- created, moved, and preserved paths, with the old-to-new map;
- the consolidation mode and any path that stays authoritative outside the tree;
- what the first pass wrote, and the count of *(unverified)* marks and open questions;
- deviations from the model and why;
- unresolved decisions (hosting, CI step, brand color, backlog link);
- a bounded next slice for `dm-docs-ingest`.
