# Agent layer

The files that tell an agentic tool how to work in the repository. They are part of the
documentation system: the site is written for humans first, the agent layer for tools
first, and the two link rather than repeat.

## Files

| File | Role |
|---|---|
| `AGENTS.md` | The index and the always-on rules. Read by every tool. Kept short on purpose. |
| `CLAUDE.md` | One line: `@AGENTS.md`. Claude Code reads the same index as every other tool. |
| `.agents/writing-guide.md` | The style guide for everything that is not code: docs, ADRs, glossary, commit messages, comments. Always present; it carries the documentation rules. |
| `.agents/decisions.md` | Settled decisions, one bold line each, with a pointer to the ADR or page. Present when the project has decisions. |
| `.agents/<topic>.md` | One module per area an agent works in: local development, security, testing, review, a native shell. Added when the area has rules that a task must not override. |

Templates are in `../assets/agents/`.

## AGENTS.md, section by section

1. **Preamble.** Who reads it, and the instruction to read the linked module before working
   in its area.
2. **What this is.** Two or three paragraphs: the product, its users, its lifecycle stage.
   One paragraph per top-level directory an agent works in. The `docs/` paragraph names
   the entry point, the toolchain, the code-span rule for files outside `docs/`, and the
   build command that finds dead links.
3. **Where things are.** A two-column table, *You are…* / *Read*. One row per module and
   per convention page. The rows for the glossary, the ADRs, the exceptions register, the
   ideas register, the questions register, and the backlog are always there.
4. **Always-on rules.** Grouped: writing, security, design, tooling, code. Each rule is one
   line. The Simplified Technical English rule opens the section. A task instruction does
   not override these; conflicts stop the work.
5. **Stop and ask.** The situations where the agent halts: production impact, a contract
   change, credentials or PII, real-looking data, a settled decision that looks wrong.
6. **Keeping this honest.** Three rules: an accepted ADR beats a module; reality that
   contradicts an ADR goes in the exceptions register and the ADR stands; durable facts
   live in the repository, not in a tool's private memory.

If a topic needs a third paragraph, it belongs in a module or in `docs/`.

## Where a fact goes

| The fact is… | It goes in |
|---|---|
| a rule every change must obey | `AGENTS.md`, always-on rules |
| a rule for one area of work | `.agents/<topic>.md` |
| a decision with a rationale | `docs/architecture/adrs/`, pointer in `.agents/decisions.md` |
| how a subsystem works | `docs/explanation/` |
| how to perform a task | `docs/how-to/` (agents follow the same steps humans do) |
| a term | `docs/glossary.md` |
| a deviation from a decision | `docs/architecture/exceptions.md` |

A module never restates a docs page; it links and adds only what an agent needs that a
human reader does not (a preflight, a command line that works without a TTY, a trap).

## Folding an existing CLAUDE.md

Most repositories that have agent guidance have it in one `CLAUDE.md`. Fold it:

1. Read it. Sort each paragraph into the table above.
2. Move rules to `AGENTS.md` or a module. Move facts about the product to `docs/`. Move
   commands to a how-to, and keep in a module only what an agent needs beyond the how-to.
3. Drop status digests and dated operational context, or date them and put them in the
   page that owns the subject.
4. Replace `CLAUDE.md` with `@AGENTS.md`.

The scaffold script never overwrites a `CLAUDE.md` that has content. It reports it.

## Other tools

Cursor, Codex, and Copilot read `AGENTS.md` directly. A tool that needs its own file
(`.cursorrules`, `.github/copilot-instructions.md`) gets one line pointing at `AGENTS.md`,
not a copy.
