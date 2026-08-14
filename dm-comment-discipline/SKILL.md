---
name: dm-comment-discipline
description: Review code comment blocks touched by a bounded diff, or every comment in explicitly named current-state files, for concise present-tense intent and short rationale. Use for comment-quality reviews of commits, branches, PRs, diffs, or specified files; never scan unrelated files.
---

# Comment Discipline Review

Assess in-scope code comments for concise present-tense intent, at most a short rationale, no narrative, and no historic context.

## Resolve the Scope

Determine the review scope before inspecting comments. Do not ask when the request or repository state makes the scope clear.

- **Diff, commit, branch, or PR**: review every comment block touched by the change. If one line in a block changes, review the entire resulting block. In a new file, every comment block is touched. Read unchanged surrounding code for context, but do not report untouched comment blocks.
- **Explicitly named files**: review every comment block in each file's current state, independent of change history, unless the user explicitly limits the request to a diff.
- **Removed blocks**: ignore blocks deleted in full; no current comment remains to fix.

Common scopes:

- **Last commit**: `git show HEAD`
- **Current branch**: identify the base branch, then use `git diff <base>...HEAD`
- **Pull request**: use the PR diff or its changed-file patch
- **Specific files**: inspect the named files in their current state

Never widen a diff-scoped review to the entire codebase.

## Review Workflow

1. Resolve the requested scope.
2. Collect the in-scope comment blocks and their current line numbers.
3. Read adjacent code to determine whether each block adds intent or rationale beyond the implementation.
4. Apply the discipline rules below to the whole block.
5. Report actionable findings. If none exist, say the scoped review is clean.

## Discipline Rules

A comment should:

1. **Specify intent** — state why the code exists or what rule it enforces, not what the syntax does.
2. **Use at most a short rationale** — prefer one direct assertion or two short clauses. A paragraph usually signals implicit code or misplaced documentation.
3. **Avoid narrative** — use direct, present-tense language without conversational setup, flowing exposition, or hedging.
4. **Exclude historic context** — never explain what the code used to do or how a prior bug behaved. The commit or PR owns history; the comment owns present intent.
5. **Prefer staccato phrasing** — "all states; sent work still counts as done" beats "the reason we take this in all states is that sent work is still work done."

## What Not to Comment

- **What the code does**: "increment counter" for `count++` adds noise.
- **Obvious intent**: `if (x > 0)` needs no "check if positive."
- **Self-documenting operations**: routine `.map()`, `.filter()`, or equivalent calls.
- **Facts enforced by code**: do not restate a type, modifier, identifier, or assertion.
- **Historic narrative**: prior failures, old behavior, or the story of a fix.

Exclude mandatory license headers, generated comments, and framework-required directives from findings unless the change adds discretionary narrative to them.

## What to Comment

- **Hidden constraints**: "oldest first; prevents reprocessing" when ordering is required but not obvious.
- **Subtle invariants**: "all states; sent work still counts as done" when a wider state set is intentional.
- **Active workarounds**: state the current external constraint and mechanism; include a stable issue reference or removal condition when useful, never the discovery story.
- **Non-obvious consequences**: "hiding sent rows makes completed work disappear" when the consequence explains the choice.
- **Runtime guarantees not expressed in syntax**: "single-threaded by design" when callers must preserve that constraint.

## Finding Violations

Find comment blocks that:

- Explain implementation mechanics instead of intent.
- Repeat facts already clear from names, types, modifiers, or control flow.
- Tell the story of a prior bug or problem state.
- Use flowing exposition instead of a terse assertion.
- Explain another component's design instead of stating the local invariant.
- Repeat the commit message or PR description.

## Output Shape

Report actionable findings by file and current line number:

```markdown
## Findings

**file_path**
- **Lines X–Y** (element): ⚠️|🔴 Verdict
  Quote or summary of the comment.
  Why this matters and a concrete deletion or rewrite.

## Summary

Actionable: N findings (F fail, W warn).
```

Use severity:

- **⚠️ Warn**: redundant, prose-heavy, overly broad, or longer than its rationale requires. Remove or shorten it.
- **🔴 Fail**: historic context, narrative about an old state, or commit/PR prose copied into code. Rewrite in present-tense intent or delete it.

Do not list compliant comments by default. When positive examples would help, add a separate `## Clear examples` section with at most three `✓ Clear` blocks and count them separately from actionable findings.
