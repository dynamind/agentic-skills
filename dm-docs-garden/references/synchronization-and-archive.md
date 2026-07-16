# Synchronization and Archive

## Synchronize from a changed behavior

1. Define the change boundary from code, tests, configuration, schema, or release evidence.
2. Search documentation for affected terms, paths, interfaces, examples, diagrams, and operational procedures.
3. Classify each affected statement as authoritative detail, summary, explanation, procedure, or historical record.
4. Update authoritative current material first.
5. Update summaries and task paths.
6. Preserve decision records and historical releases; supersede rather than rewrite them.
7. Verify links, generated references, builds, and repository-wide terminology.

Do not treat a clean text search as proof that no affected page exists. Consider synonyms, renamed concepts, diagrams, generated docs, external consumers, and implicit operational dependencies.

## Archive deliberately

Archive when material is no longer current but retains historical, migration, audit, or explanatory value.

Before moving it:

- identify its replacement, if any;
- mark authority and lifecycle visibly;
- record why and when it was superseded;
- repair or redirect incoming links;
- ensure search results cannot easily present it as current;
- preserve immutable records such as accepted ADRs and release notes.

Delete only when content has no continuing value, retention requirement, meaningful inbound reference, or unique evidence. Do not use the archive as a dumping ground for unresolved classification.
