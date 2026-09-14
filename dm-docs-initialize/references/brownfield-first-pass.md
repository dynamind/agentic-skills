# Brownfield first pass

An existing repository with little or no documentation gets a first pass: the orientation
pages, written from evidence, with uncertainty marked. One session can produce a site a
newcomer can read in an afternoon. Deeper per-subsystem work is `dm-docs-ingest`.

## Before writing

Read `assets/agents/writing-guide.md`. Every page in the pass is written in Simplified
Technical English with US spelling from the first draft: short sentences, active voice, one
term for one thing, no metaphor. The rules in `SKILL.md`, Writing rules, apply to every
sentence below.

## Evidence, in order of authority

1. **The code** in the repository, including build files, configuration per environment,
   pipelines, and infrastructure definitions. Note drifted copies of the same thing.
2. **Wiki pages** the user points at. Mirror them under `docs/reference/<wiki>/`
   (see below) before working their content into pages.
3. **Chat and mail digests** the user provides. Digest under `docs/reference/`, dated.
4. **People.** What the maintainer says goes in as a fact with the person as source.

Where sources disagree, record the disagreement in `docs/product/questions.md`. Do not
resolve it silently.

## The page set

Write these, in this order, and stop when the evidence runs out:

| Page | Evidence |
|---|---|
| `guide/index.md` | what the product is, why the documentation exists, how the site is organized, conventions used (language of domain terms, ticket key pattern, the *(unverified)* marker) |
| `guide/business-context.md` | who uses it, the process it supports, the systems around it |
| `guide/history.md` | when a legacy app's story matters: origin, ownership changes, incidents that shaped it |
| `glossary.md` | terms from UI strings, code, and wiki; domain language kept |
| `product/personas/` | user groups from login rules, roles in code, wiki pages; a comparison table in the index |
| `product/features/index.md` | the feature inventory; the menu or route table is the most honest list. Each row: purpose, main code, where its rules live |
| `product/features/<flow>.md` | the main user journey end to end |
| `product/business-rules/` | rules found in validation code, with the code path as evidence |
| `architecture/overview.md`, `diagrams.md` | C4 context and container diagrams in Mermaid, request flow |
| `architecture/technology-stack.md`, `configuration.md` | versions, layering of config per environment |
| `architecture/hazards.md` | security, reliability, maintainability findings as fact + evidence + why it matters |
| `operations/index.md` | environments table, health checks, deployment pipeline, access table, runbook links |
| `operations/<runbook>.md` | release, incident handling, run locally |
| `product/questions.md` | everything the sources do not settle, grouped by urgency, each to be answered by a named person |
| `reference/<wiki>/` | mirrors |

A living document states when it started: `docs/index.md` carries the start date and the
three sources it draws on, in order of authority.

## Marking uncertainty

Two tiers:

- **Inline.** A fact from a single unconfirmed source, or a reading of code not confirmed
  with the maintainer, ends with *(unverified)*. A verified fact names its source.
- **Register.** A gap that needs a human goes in `docs/product/questions.md`, one line,
  with who should answer it. On a legacy app, group by urgency: blocking for any release,
  architecture and code, operations.

No `TODO`, no `needs-review`, no frontmatter status. The marker is in the sentence.

## Mirrors of external sources

- One folder per source under `docs/reference/`, with an index page that lists each mirrored
  page, its original id, when it was written, and where it is mirrored.
- Date the mirror. Mirrors are snapshots.
- Condense. Where a mirror's content is already in a product or operations page, the
  mirror is short and links there.
- Omit secrets on purpose and say so in a callout. Wiki release pages often carry keystore
  passwords.
- Attachments and images are not mirrored when they need a login.
- Auth-gated origins go in `ignoreDeadLinks` with a comment.

## Hazards register

A legacy app's first pass turns up findings nobody wrote down: a password in a query
string, no monitoring, a shipped version not in the repository. They go in
`docs/architecture/hazards.md`, in tables per category, each row a fact, its evidence (a
file, a config key, a page id), and why it matters. Severity is a judgement to be
confirmed, and the page says so.

## What the pass does not do

- It does not invent a business purpose from class names. It says what the evidence shows
  and marks the rest.
- It does not write ADRs for a frozen app. Decisions are recorded when the project makes
  them. The directory and the convention exist; the first ADR is written when the first
  decision is made.
- It does not copy a wiki's navigation. It extracts claims and gives them the site's shape.
- It does not commit. The user reviews the pass first.
