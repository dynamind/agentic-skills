# Repetition and Links

Classify repetition before removing it.

## Narrative repetition

Repeat enough context for a page to stand alone. Keep it brief and stable. This is useful when a feature, component, overview, and runbook all need the same orienting sentence.

## Referential repetition

Summarize a related fact, then link to the authoritative detail. Ensure the summary remains true across expected changes.

## Canonical duplication

Treat copied tables, defaults, fields, retention periods, compatibility statements, and formal rules as drift risks. Consolidate them into one authoritative location and repair incoming links.

## Semantic links

Prefer links that describe both destination and reason:

```markdown
See [Authentication flow](../architecture/authentication.md) for token validation and identity propagation.
```

Avoid `here`, `more`, or bare filenames when the surrounding phrase provides no relationship.

When moving content:

1. identify incoming links and likely external bookmarks;
2. retain a redirect or short supersession notice when supported;
3. repair semantic context around links, not only paths;
4. check that summaries still match the new canonical detail.
