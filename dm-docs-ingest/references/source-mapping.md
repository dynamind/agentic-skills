# Source Mapping

Build a compact claim map before writing a substantial slice.

```markdown
| Claim or question | Evidence | Authority | Confidence | Conflict | Destination |
|---|---|---|---|---|---|
| Tokens expire after 15 minutes | config/auth.yaml; AuthConfigTest | enforced configuration | high | operations page says 30 | reference/auth.md |
```

## Mapping procedure

1. Start with reader questions, not files.
2. Locate evidence for each question.
3. Group claims by stable documentation concern.
4. Choose one authoritative destination for exact facts.
5. Identify the summaries and routes that should link to it.
6. Stop when the bounded slice is supportable; record adjacent gaps separately.

## Source coverage

For code ingestion, consider:

- entry points and public interfaces;
- domain terms and invariants;
- persistence and owned data;
- integration boundaries;
- configuration and environment differences;
- tests and fixtures;
- deployment and operational wiring;
- observability and failure handling;
- decisions and known exceptions.

For document ingestion, consider:

- owner and date;
- intended versus observed lifecycle;
- version and product scope;
- duplicated or copied origin;
- links to evidence;
- current, historical, proposal, or unknown authority;
- claims worth preserving separately from obsolete structure.

Do not publish the claim map unless it is useful to maintainers. It is working evidence, not automatically part of the documentation corpus.
