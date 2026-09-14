---
name: dm-docs-garden
description: "Audit and repair an existing documentation corpus without losing authoritative facts. TRIGGER when the user says 'docs are stale', 'sync the docs', 'check the documentation', 'broken links', 'update docs after this change', 'docs cleanup', 'are the docs still right', or asks about documentation health or duplication. Audit only, no edits, when the user asks just for a review or diagnosis. SKIP for creating a docs tree from scratch (dm-docs-initialize) or writing new pages from code (dm-docs-ingest)."
---

# DM Docs Garden

Keep documentation coherent, current, and traversable without confusing aesthetic tidiness with correctness.

## Choose the Mode

- **Audit**: inspect and report findings without changing files.
- **Synchronize**: reconcile a bounded code, configuration, interface, or behavior change with affected documentation.
- **Garden**: improve navigation, page contracts, links, repetition, metadata, ownership, and archive boundaries.

Use the narrowest mode matching the request. Never turn a read-only audit into an edit.

## Workflow

1. Establish the documentation contract.
   - Read repository instructions, `mkdocs.yml` when present, landing page, navigation, metadata conventions, glossary, and archive policy.
   - Identify generated and externally owned documentation that must not be hand-edited.
2. Bound the inspection.
   - For synchronization, start from the changed behavior and search outward to affected consumers and pages.
   - For gardening, name the section, quality concern, or traversal path under review.
   - For a broad health check, run `python3 scripts/inspect_docs.py <docs-directory>` as supporting evidence, not as the whole review. It checks MkDocs entrypoints, ADR filenames and identifiers, Mermaid conventions, links, metadata, titles, and traversal.
3. Collect evidence.
   - Inspect relevant code, tests, configuration, operational material, and history before declaring a page stale.
   - Read [references/health-checks.md](references/health-checks.md) for the quality dimensions and severity model.
4. Diagnose before changing.
   - Distinguish incorrect facts, missing facts, poor placement, weak links, obsolete lifecycle, and stylistic preference.
   - Distinguish useful narrative repetition from drifting canonical duplication using [references/repetition-and-links.md](references/repetition-and-links.md).
   - State evidence and risk for each material finding.
5. Repair with the smallest coherent change when authorized.
   - Correct authoritative facts before summaries.
   - Preserve useful local context while pointing to canonical detail.
   - Split mixed-purpose pages only when the resulting navigation remains discoverable.
   - Archive or supersede material according to [references/synchronization-and-archive.md](references/synchronization-and-archive.md).
   - Add redirects or link repairs when paths change.
6. Verify.
   - Re-run structural checks and documentation builds.
   - Run `python3 -m mkdocs build --strict` from the repository root when MkDocs is configured.
   - Search for references to renamed or archived pages.
   - Confirm summaries, navigation, metadata, and authority markers agree.
   - Report residual uncertainty and unexamined areas.

## Prioritization

Prioritize findings in this order:

1. Incorrect or dangerous instructions.
2. Contradictions about behavior, security, privacy, data, compatibility, or operations.
3. Current and historical material that readers can easily confuse.
4. Broken traversal on onboarding, incident, and change-making paths.
5. Missing ownership, authority, or review state.
6. Authoritative facts duplicated in a root README or scattered narrative documents.
7. Mixed page contracts and harmful duplication.
8. Fixed-color or inline-themed Mermaid diagrams that fail across palettes.
9. Cosmetic consistency.

## Output

For an audit, lead with findings:

```markdown
## Findings

- [High|Medium|Low] Title
  Evidence:
  Reader or agent risk:
  Suggested repair:

## Coverage
## Residual uncertainty
## Positive patterns to preserve
```

For authorized edits, lead with the outcome and include changed pages, verification performed, archived or redirected material, and remaining risks.
