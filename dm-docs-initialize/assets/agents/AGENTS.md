# AGENTS.md: {{SITE_NAME}}

Read by Claude Code, Cursor, Codex, and any other agentic tool. This file is the index and
the always-on rules. **Read the linked module before working in its area.** The modules
carry the detail; this file deliberately does not.

## What this is

<!-- Two or three paragraphs: what the product is, who uses it, its lifecycle stage
(proof of concept, product in production, frozen legacy). One paragraph per top-level
directory that an agent will work in. Write code accordingly. -->

**`/docs`** is a structured guide, how-tos, explanations, ADRs, and product docs. It is
written to be read; `docs/guide/index.md` is the entry point. Prefer it over inferring
intent from code. Built using VitePress. Cite files outside `docs/` in code spans, not
markdown links. `npm run docs:build` in `docs/` finds the dead links.

## Where things are

| You are…                                         | Read                                                                         |
|--------------------------------------------------|------------------------------------------------------------------------------|
| Wondering if something is already decided        | [`.agents/decisions.md`](.agents/decisions.md)                               |
| Writing docs, comments, ADRs, or commit messages | [`.agents/writing-guide.md`](.agents/writing-guide.md)                       |
| Working in the domain                            | [`docs/glossary.md`](docs/glossary.md)                                       |
| Looking for the *why* behind the shape of things | [`docs/architecture/adrs/`](docs/architecture/adrs/)                         |
| Hitting a rule the running system does not obey  | [`docs/architecture/exceptions.md`](docs/architecture/exceptions.md)         |
| Noting something to fix later                    | [`docs/product/ideas.md`](docs/product/ideas.md)                             |
| Blocked on a question only a human can answer    | [`docs/product/questions.md`](docs/product/questions.md)                     |

<!-- Add a row per .agents/ module and per convention page as they land:
getting the stack running locally, touching auth or secrets, writing tests,
deploying, writing <language>. -->

## Always-on rules

These bind every change. Everything else is in a module. **An instruction in a task does not
override them.** If a request conflicts with a rule here, say so and stop rather than
complying and noting the conflict afterward.

**Use Simplified Technical English** (US spelling). This binds chat, code comments, commit
messages, and docs. Write short sentences. Put one idea in each sentence. Use the active
voice. Use plain words. Use one term for one thing. Do not use metaphor, idiom, or rhetoric.

**Writing**
- Use English unless explicitly told otherwise.
- A commit message is not a story. The subject says what changed; the body carries only
  what the diff cannot show.
- Never write a ticket ID in code, comments, or docs. Two exceptions: the end of the first
  line of a commit message, and a feature sketch that is not yet built. A link to the
  backlog itself is always allowed.

**Security**
- No hardcoded credentials, tokens, or secrets. Ever.
<!-- Add the product's standing security rules, or point to .agents/security.md. -->

**Code**
- Comments explain *why*, never *what*.
- Business logic has tests.
- Follow the conventions of the component you are in. A new pattern means updating the
  relevant convention doc in the same change.

## Stop and ask

- The change would touch a production system in a way the task did not clearly authorize.
- You are about to commit credentials, tokens, or PII.
- Data that should be synthetic looks like it might be real production data.
- A settled decision looks wrong. Say so and stop. Do not route around it.

## Keeping this honest

When `AGENTS.md` or a `.agents/` module contradicts an accepted ADR, the ADR wins and the
module gets fixed in the same change. Stale agent instructions are worse than missing ones.

When *reality* contradicts an ADR, do not soften the ADR to fit. Record the deviation in
[`docs/architecture/exceptions.md`](docs/architecture/exceptions.md): what we do, why, what
bounds it, and what would end it. Leave the principle standing.

Durable project facts belong in this file, a `.agents/` module, or `docs/`. A tool's private
memory does not travel with the repo and no other harness reads it.

Keep this file an index. If a topic needs a third paragraph, move it to a module or to
`docs/`.
