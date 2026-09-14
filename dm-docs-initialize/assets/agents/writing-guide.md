# Writing guide

This guide applies to everything that you write that is not executable code: docs, ADRs,
glossary entries, commit messages, and code comments.

## The one rule

**Use plain language, in proportion to the subject.** Most of our work is ordinary work, and
it must read that way. Dense jargon and elaborate structure do not prove rigor. They usually
show that the author did not know what to say. Generated text tends toward heavy structure
for a small change, and it produces documents that nobody reads.

## Documents

- **A document has one job.** If you cannot say what a page is for in one sentence, split
  the page or delete it.
- **State the current state. Do not state how you reached it.** Reasoning that no longer
  applies goes in an ADR or in `docs/archived/`. It does not stay in the page.
- **A document that a reader cannot scan in five minutes does not earn its place.** Every
  future reader pays for its length.
- **Do not duplicate.** Link to the authoritative page. Do not repeat it. A fact in two
  places is wrong in one of them within a month.
- **Date every snapshot**: a review, an audit, a migration status. An undated snapshot
  becomes canon without anybody deciding so. Use a blockquote at the top of the page
  (`> **Reviewed:** 2026-09-14`), not frontmatter.
- **Mark what is not confirmed.** Follow a fact from one unconfirmed source with
  *(unverified)*. A verified fact names its source. A question for a human goes in
  `docs/product/questions.md`, not in the page.
- **A register has sections.** `docs/product/questions.md`, `docs/product/ideas.md`, and
  `docs/architecture/exceptions.md` hold open items apart from answered ones. Insert a new
  entry in the open section, in the format of the file. Never append at the end.
- **Fold or drop displaced content. Never make a new page for it.** If a restructure leaves
  content without a home, put it in an existing section, or drop it and say that you did.
- **Put a new page in the sidebar** in `docs/.vitepress/config.mts`. Otherwise nobody finds
  it.
- **A heading that is a link target uses a colon, never an em-dash.** The slugifier keeps
  the em-dash, and the dead-link check does not validate an `#anchor`, so the broken link is
  silent.
- **Cite a file outside `docs/` in a code span**, not in a markdown link. The dead-link check
  cannot follow it.

## ADRs and decisions

- **A decision is a constraint, not an essay.** Write one statement and one consequence that
  can be verified: a test, a type, a lint rule, a schema constraint, or a config default.
- **Do not add "Rationale / Alternatives Considered / Trade-off Analysis" sections by
  default.** Write such a section when somebody disputes the decision. Write only the section
  that answers the dispute.
- **Rigor is in the output, not in the process.** Typed artifacts, contract tests, schemas
  and IaC plans carry it. A process step that produces no artifact produces no rigor.
- An ADR lives in `docs/architecture/adrs/adr-NNN-kebab-title.md`, with three digits, in
  sequence.
- **A reader reads an ADR for years.** Use no ticket keys, no list of the files that exist
  today, and no names that change each iteration. A rejected alternative and its reason go in
  the rejected-alternatives section, not in the decision text.
- **Never weaken an ADR to match what the code does.** A principle that is edited to match
  reality constrains nothing. Record the difference in
  [`docs/architecture/exceptions.md`](../docs/architecture/exceptions.md) as an `EX-nnn`
  entry: what we do, the reason, what limits it, and what ends it. Add a pointer from the ADR,
  so that a reader is not misled. If a deviation proves permanent and correct, write a new
  ADR that supersedes the old one. Do not leave the entry in the register.

## Glossary entries

`docs/glossary.md` is the authoritative glossary. It is the one document to read before you
work in the domain.

- An entry states **what we mean**. It does not state how we implement it. Implementation
  detail stays in the code.
- A domain term stays in the language that the business speaks. A translation loses the word
  that the user says.
- **Use no wire identifiers and no code identifiers**, and describe no mechanics. An entry is
  one or two sentences of domain meaning. Mechanics belong in the feature page.
- **Do not add an entry unless you are asked.** The bar is a term that the business needs
  defined. If you are not sure, propose the text in chat.

## Diagrams

The docs site renders Mermaid itself, in a light theme and a dark theme.

- **Use theme-neutral diagrams only.** Use no `fill:`, no hex colors, and no `style`
  overrides. They break in one of the two themes. Show meaning with shape, stroke weight, and
  link style.
- **`<br/>` is dropped without a warning.** For a label on more than one line, use the
  `htmlLabels: true` frontmatter config and a backtick markdown-string label with real
  newlines:

  ```
  ---
  config:
    htmlLabels: true
  ---
  flowchart TD
      A["`**Node name**
      one qualifier line`"]
  ```

- **A node holds a bold name and at most one more line.** Put the explanation in the prose
  around the diagram. A box full of text is a paragraph in a rectangle.
- **A label in a sequence diagram is one source line.** A backtick string cannot span lines
  there. Write the label on one line and separate the parts with ` · `.

## Commit messages

Use conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, with an optional scope
(`feat(route):`). Write the subject in the imperative. The body explains why, if the diff
does not. Use no hard line breaks in the body. Let it wrap.

**Say what the change is. Do not say how you reached it.** Most commits need no body, or one
or two lines. Never describe the investigation. A finding worth keeping goes in the document
or the ADR that owns the subject.

A commit that belongs to a backlog item ends its first line with the ticket ID, for example
`docs: propose ADR-042 support infinite probability drive (KEY-123)`. A ticket ID appears
nowhere else, except in a feature sketch before it is built. The rule is in `AGENTS.md`.

## Code comments

- **State the intent**: why the code exists, or which rule it enforces. Do not state what the
  syntax does.
- **Give a short reason only**: one statement, or two short clauses. A paragraph usually
  means that the code is unclear, or that the text belongs in a document.
- **Do not narrate.** Use direct language in the present tense. Do not open with a setup
  sentence and do not hedge.
- **Do not give history.** Never explain what the code did before, or how an earlier defect
  behaved. A comment states the present intent. It can describe a platform behavior that the
  code guards against.
- **Write short phrases**: "all states; sent work still counts as done" is better than "the
  reason we take this in all states is that sent work is still work done".
