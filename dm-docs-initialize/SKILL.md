---
name: dm-docs-initialize
description: "Set up or restructure a repository documentation system with Material for MkDocs, progressive onboarding, three-digit ADRs, Mermaid, and page templates. TRIGGER when the user says 'set up docs', 'add mkdocs', 'create a docs folder', 'ADR structure', 'documentation skeleton', 'restructure the docs tree', or a repo has no docs system yet and one is requested. SKIP for filling pages with content from code (dm-docs-ingest) and for fixing existing docs (dm-docs-garden)."
---

# DM Docs Initialize

Establish a durable, topic-first documentation system without pretending to know facts that have not been investigated.

## Workflow

1. Inspect the repository before proposing a tree.
   - Read repository instructions and existing documentation configuration.
   - Identify existing docs, generated references, ADRs, runbooks, release notes, and archives.
   - Preserve local terminology. Inventory established paths without assuming they must remain authoritative.
2. Resolve initialization decisions before moving or generating files.
   - Identify the existing documentation generator from repository configuration. If none exists and the user has no preference, default to Material for MkDocs.
   - Ask whether to **consolidate** scattered documentation into the tree or **route in place**. Default to consolidation for this suite, but do not relocate files without making the choice visible.
   - Ask where authoritative documentation should live. Default to the docs tree; keep the root `README.md` as a thin signpost and `AGENTS.md` as root agent instructions.
   - Confirm the ADR scheme. Default to one file per ADR under `docs/architecture/adrs/` using `NNN-short-kebab-title.md`, with `000` reserved for the convention.
   - Read [references/migration-and-authority.md](references/migration-and-authority.md) before reorganizing existing documentation.
3. Define the documentation contract.
   - Separate current, explanatory, generated, proposed, historical, and superseded material.
   - Define page purpose, audience, document type, authority, lifecycle, owner, review date, and evidence links.
   - Use `lifecycle`, not `status`; Material for MkDocs reserves `status` for navigation badges.
   - Treat Diataxis as a page-level writing discipline, not a mandatory top-level taxonomy.
   - Read [references/documentation-model.md](references/documentation-model.md) before designing or changing the tree.
   - Read [references/mkdocs-material.md](references/mkdocs-material.md) before creating or changing MkDocs, Mermaid, or ADR configuration.
4. Design recognizable navigation.
   - Use a landing page to route readers by intent.
   - Prefer topic names readers actively seek, such as `Architecture`, `Operations`, and `Reference`.
   - Keep `Overview` for orientation and `Getting Started` for first successful action.
   - Keep `Archive` visibly separate from current material.
   - Label a section's `index.md` as `Overview` in navigation. When the section itself is named `Overview`, use `Introduction` for its index. Never produce doubled labels such as `Architecture > Architecture` or `Overview > Overview`.
5. Create only the justified structure.
   - For a conventional baseline, run `python3 scripts/scaffold_docs.py --root <repository> --site-name "<name>"`.
   - Use `--dry-run` first in a populated repository.
   - Never pass `--overwrite` unless the user explicitly authorizes replacing scaffold-owned files.
   - Preserve and adapt an existing `mkdocs.yml`; never replace it merely to impose the baseline.
   - Customize or create files directly when an existing documentation tool or structure makes the baseline unsuitable.
6. Consolidate or connect existing material according to the selected mode.
   - In consolidation mode, create an old-to-new path map, use `git mv` for tracked files, rewire repository links and MkDocs navigation, and mark relocated but unverified pages `lifecycle: needs-review` with a temporary migration notice.
   - Keep only `README.md` and `AGENTS.md` as root-level narrative documentation by default. Rewrite the README as a stable signpost after its facts have authoritative destinations in the docs tree.
   - In route-in-place mode, state which external paths remain authoritative and link to them semantically; do not create shadow copies.
   - Relocate content losslessly during initialization. Hand substantive reconciliation and rewriting to `dm-docs-ingest`.
7. Connect the structure.
   - Make the landing page the explicit entry point.
   - Add semantic links that state why the destination is relevant.
   - Ensure each empty section says what belongs there; do not generate fake product content.
8. Set up MkDocs when selected.
   - Detect with `python3 -m mkdocs --version` and `python3 -m pip show mkdocs mkdocs-material`.
   - Prefer `python3 -m pip`; use `pip3` only when the Python module form is unavailable. Never use bare `pip` on a machine where it may select a legacy interpreter.
   - Run `python3 -m pip install -r requirements-docs.txt` only with explicit authorization because it downloads and installs packages.
   - Use Material's native Mermaid integration; do not add `mkdocs-mermaid2-plugin`.
9. Verify the result.
   - Confirm existing material was preserved or moved according to the recorded path map.
   - Check links, navigation configuration, and build commands when available.
   - Run `python3 -m mkdocs build --strict` from the repository root when MkDocs is configured.
   - Report created structure, preserved content, deliberate deviations, and remaining decisions.

## Boundaries

- Do not populate architecture, features, or operations from superficial repository guesses.
- Do not silently choose preservation-in-place. Resolve consolidation versus routing before restructuring.
- Do not force every page into one Diataxis category. Use `decision`, `runbook`, `landing`, `release`, and `roadmap` when those contracts are clearer.
- Do not make this skill a prerequisite for ingestion or gardening. Adapt to an existing corpus when one already exists.
- Keep ADRs under `docs/architecture/adrs/` with `NNN-kebab-case-title.md`; reserve `000` for the ADR convention.
- Use Mermaid for diagrams and avoid fixed inline colors or themes that fail across light and dark palettes.
- Keep product, setup, configuration, architecture, development, and operations facts authoritative inside the docs tree unless the user selects another policy.

## Resources

- Use `scripts/scaffold_docs.py` for an additive Material for MkDocs baseline; pass `--without-mkdocs` only when another generator governs the corpus.
- Copy or adapt templates from `assets/page-templates/`; do not publish unused templates as product documentation.
- Read [references/documentation-model.md](references/documentation-model.md) for the default information architecture, metadata model, repetition rules, and customization decisions.
- Read [references/mkdocs-material.md](references/mkdocs-material.md) for generated files, dependency installation, navigation, Mermaid, ADR, and validation conventions.
- Read [references/migration-and-authority.md](references/migration-and-authority.md) for consolidation, path mapping, `git mv`, migration notices, link rewiring, root exceptions, and the initialize/ingest boundary.

## Handoff

Conclude with:

- documentation entry point;
- created and preserved paths;
- consolidation or route-in-place mode and the old-to-new path map;
- authoritative documentation location and root-level exceptions;
- chosen conventions and deviations;
- unresolved ownership or tooling decisions;
- a bounded next ingestion slice suitable for `dm-docs-ingest`.
