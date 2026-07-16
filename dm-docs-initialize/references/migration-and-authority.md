# Migration and Authority

Resolve two independent decisions before restructuring an existing repository.

## Where facts are authoritative

Recommended default:

- Keep product, setup, configuration, architecture, development, operations, security, and reference facts authoritative under `docs/`.
- Keep root `README.md` as a thin signpost: product identity, one stable summary sentence, and links into the docs tree.
- Keep root `AGENTS.md` for agent operating instructions.
- Move other root-level narrative Markdown into the docs tree unless a justified consumer requires its location.

Do not keep installation commands, supported versions, configuration defaults, architecture summaries, or operational procedures in both the root README and the docs tree.

## Consolidate or route in place

Ask the user to select a mode when scattered documentation exists.

### Consolidate — recommended default

1. Inventory narrative documentation inside and outside the existing docs directory.
2. Map every old path to a destination, archive, generated source, or explicit exception.
3. Use `git mv <old> <new>` for tracked files to preserve discoverable history.
4. Move content losslessly before rewriting it.
5. Add `lifecycle: needs-review` and a short migration notice when correctness has not yet been reconciled.
6. Rewire repository links, navigation, CI references, contribution instructions, and agent instructions.
7. Use redirect stubs only when an external consumer cannot be updated; never retain a second full copy.
8. Reduce the root README to a signpost after its facts have authoritative destinations.
9. Hand the relocated, bounded page set to `dm-docs-ingest` for evidence-based reconciliation.

Suggested temporary notice:

```markdown
> **Migrated documentation:** This page was moved from `<old-path>`. Its content still requires evidence-based review before `lifecycle` can become `current`.
```

### Route in place

Keep a page outside the tree only when its location serves a real consumer, generator, or repository convention. Record that it remains authoritative, link to it semantically, include it in health checks when possible, and do not create a copied placeholder containing the same facts.

## Initialize versus ingest

Initialization may inventory, map, move, label, and rewire documentation. It must not silently reinterpret or modernize factual content during the move.

Ingestion validates claims against code, tests, configuration, decisions, runtime evidence, and current requirements; resolves contradictions; rewrites content; removes migration notices; and changes `lifecycle` to `current` when justified.
