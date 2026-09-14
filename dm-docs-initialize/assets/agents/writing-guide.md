# Writing guide

Applies to anything you write that isn't executable code: docs, ADRs, glossary entries, commit
messages, and code comments.

## The one rule

**Plain language, proportional to the thing being described.** Most of what we build is
ordinary work, and it should read that way. Jargon density and structural ceremony are not
evidence of rigor. They are usually evidence that the author didn't know what they wanted to
say. Generated material has a strong pull toward heavy framing for a small change, and it
makes documents nobody reads.

## Documents

- **A document has one job.** If you can't say what a page is for in one sentence, split it
  or delete it.
- **Say the current state, not the history of how you got there.** Superseded reasoning
  belongs in an ADR or `docs/archived/`, not inline.
- **If a document isn't scannable in five minutes, it doesn't earn its place.** Length is a
  cost paid by every future reader.
- **Don't duplicate.** Link to the authoritative page instead of restating it. A fact stated
  in two places will be wrong in one of them within a month.
- **Date anything that is a snapshot**: a review, an audit, a migration status. Undated
  snapshots quietly become canon. Use a blockquote at the top of the page
  (`> **Reviewed:** 2026-09-14`), not frontmatter.
- **Mark what is not confirmed.** A fact from a single unconfirmed source is followed by
  *(unverified)*. A verified fact names its source. A question for a human goes in
  `docs/product/questions.md`, not in the page.
- **Registers have sections.** `docs/product/questions.md`, `docs/product/ideas.md`, and
  `docs/architecture/exceptions.md` separate open items from answered ones. Insert a new
  entry in the open section, in the file's own format. Never append at the bottom.
- **Displaced content gets folded or dropped, never a new page.** When a restructure
  leaves content without a home, put it in an existing section or drop it and say so.
- **A new page goes in the sidebar** in `docs/.vitepress/config.mts`, or nobody finds it.
- **No em-dashes, anywhere.** Not in prose, headings, tables, register entries, comments,
  or commit messages. Use a colon, a comma, parentheses, or a second sentence. In a
  link-target heading a dash also breaks the slug.
- **Cite files outside `docs/` in code spans**, not markdown links. The dead-link check
  cannot follow them.

## ADRs and decisions

- **A decision is a constraint, not an essay.** One-line statement, plus one verifiable
  consequence: a test, a type, a lint rule, a schema constraint, a config default.
- **No "Rationale / Alternatives Considered / Trade-off Analysis" scaffolding by default.**
  Write those sections when someone actually disputes the decision, and write only the
  section that answers the dispute.
- **Determinism lives on the output, not the process.** Typed artifacts, contract tests,
  schemas, IaC plans carry the rigor. Process ceremony that produces no artifact produces
  no rigor.
- ADRs live in `docs/architecture/adrs/adr-NNN-kebab-title.md`, three digits, sequential.
- **An ADR is read for years.** No ticket keys, no inventory of existing files, no names
  that change per iteration. A rejected alternative and its reason go in the
  rejected-alternatives section, not in the decision text.
- **Never weaken an ADR to accommodate what the code actually does.** A principle edited to
  match reality stops constraining anything. Record the gap in
  [`docs/architecture/exceptions.md`](../docs/architecture/exceptions.md) as an `EX-nnn`
  entry (what we do, why, what bounds it, what ends it) and add a pointer from the ADR so a
  reader isn't misled. If a deviation turns out to be permanent and right, supersede the
  ADR with a new one; don't let the register hold it forever.

## Glossary entries

`docs/glossary.md` is the authoritative glossary and the one doc worth reading before working
in the domain.

- Entries say **what we mean**, not how we implement it. Implementation detail lives in code.
- Domain terms stay in the language the business speaks. Translating them loses the thing
  the user actually says.
- **No wire or code identifiers** and no mechanics. An entry is one or two sentences of
  domain meaning; mechanics belong in the feature doc.
- **Do not add entries unprompted.** The bar is a term the business needs defined. When in
  doubt, propose the text in chat.

## Diagrams

The docs site renders Mermaid natively with light and dark themes.

- **Theme-neutral only.** No `fill:`, no hex colors, no `style` overrides. They break in one
  of the two themes. Convey semantics with shapes, stroke weight, and link style.
- **`<br/>` is silently dropped.** For multi-line labels use the `htmlLabels: true`
  frontmatter config and backtick markdown-string labels with real newlines:

  ```
  ---
  config:
    htmlLabels: true
  ---
  flowchart TD
      A["`**Node name**
      one qualifier line`"]
  ```

- **A node is a bold name plus at most one qualifier line.** Explanation goes in the prose
  around the diagram. A box full of text is a paragraph wearing a rectangle.
- **Sequence-diagram labels are one source line.** Backtick strings cannot span lines
  there, so write the label on one line with ` · ` separators.

## Commit messages

Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, optional scope (`feat(route):`).
Subject in the imperative. Body explains *why* if the diff doesn't. No hard line breaks in
the body; let it soft-wrap.

**Say what the change is, not how you got there.** Most commits need no body, or one or two
lines. Never narrate the investigation. A finding worth keeping belongs in the doc or ADR
that owns the subject.

A commit that belongs to a backlog item ends its first line with the ticket ID, for example
`docs: propose ADR-042 support infinite probability drive (KEY-123)`. Ticket IDs appear
nowhere else, except in a feature sketch before it is built; the rule is in `AGENTS.md`.

## Code comments

- **Specify intent**: state why the code exists or what rule it enforces, not what the
  syntax does.
- **Use at most a short rationale**: one direct assertion or two short clauses. A paragraph
  usually signals implicit code or misplaced documentation.
- **Avoid narrative**: direct, present-tense language without conversational setup or
  hedging.
- **Exclude historic context**: never explain what the code used to do or how a prior bug
  behaved. The comment owns present intent, with allowance for platform behaviors the code
  guards against.
- **Prefer staccato phrasing**: "all states; sent work still counts as done" beats "the
  reason we take this in all states is that sent work is still work done."
