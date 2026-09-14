# Migration and authority

Two decisions, made before any file moves. Both are visible in the handoff.

## Where facts are authoritative

Default: the docs tree. `README.md` is a signpost to `docs/guide/index.md` and `AGENTS.md`,
with the two or three commands a newcomer needs. `AGENTS.md` holds the always-on rules and
the routing table, and nothing else.

Root-level narrative files beyond `README.md`, `CLAUDE.md` (`@AGENTS.md`), and `AGENTS.md`
are a finding. Move each into the tree or record why it stays.

## Consolidate or route in place

**Consolidate** (default). Scattered documents move into the tree:

1. Inventory every document outside `docs/` and every wiki page the user names.
2. Map old path to new path. Present the map before moving.
3. Move tracked files with `git mv` so history follows. Wiki pages become mirrors under
   `docs/reference/`.
4. Rewire links in the repository and add each page to the sidebar.
5. Mark a moved page whose facts are not yet checked with a dated blockquote at the top:
   `> **Moved:** 2026-09-14, from \`old/path.md\`. Facts not yet re-verified.` The
   `dm-docs-ingest` pass removes the notice once the page's claims are checked.
6. Rewrite `README.md` as a signpost only after each fact in it has a home in the tree.

**Route in place**. A document stays outside the tree only when its location serves a real
consumer: a `README.md` inside a package that a registry renders, a runbook a tool reads
from a fixed path. State which paths stay authoritative, link to them from the tree with
semantic text, and do not copy them.

## Initialize versus ingest

Initialization moves content losslessly and rewires. It does not check claims against
code, resolve contradictions, or rewrite. That is `dm-docs-ingest`, one bounded slice at a
time. The brownfield first pass ([brownfield-first-pass.md](brownfield-first-pass.md)) is
the exception: it writes orientation pages from evidence, marks uncertainty inline, and
leaves subsystem depth to ingestion.
