# Documentation Health Checks

Review dimensions in risk order.

## Correctness

- Do current claims agree with appropriate source evidence?
- Are security, privacy, compatibility, operational, and data instructions safe?
- Are generated or externally owned facts hand-copied elsewhere?

## Authority and currency

- Can readers distinguish authoritative, explanatory, proposed, generated, historical, and superseded pages?
- Are dated snapshot blockquotes (`> **Reviewed:**`, `> **Moved:**`) and *(unverified)* markers still true, and removed once verified?
- Do content pages carry no YAML frontmatter? State is in the page: `## Status` on an ADR, a dated blockquote on a snapshot.
- Do open items in the registers (`ideas.md`, `questions.md`, `exceptions.md`) still belong there, and does every exception have an exit condition?
- Does archived material remain visibly non-current?
- Is the docs tree authoritative, with the root README acting only as a signpost?
- Are root-level narrative Markdown files limited to `README.md`, `AGENTS.md`, and documented exceptions?

## Traversal

- Does the landing page route by common intent?
- Can a new developer, operator, product reader, and incident investigator find a useful path?
- Are important pages orphaned or linked with vague text?
- Do moved pages have repaired links or redirects?

## Page contracts

- Does each page primarily teach, guide action, provide reference, explain, record a decision, route, or support operations?
- Does a hybrid page force readers to alternate repeatedly between incompatible intents?
- Is progressive disclosure appropriate to its page type?

## VitePress, ADRs, and diagrams

- Does `docs/index.md` exist and does the sidebar in `docs/.vitepress/config.mts` reach every current page?
- Is each section index labeled `Overview` in navigation, using `Introduction` for the section named Overview, without doubled labels?
- Does `npm --prefix docs run docs:build` succeed?
- Do ADRs live under `docs/architecture/adrs/` as `adr-NNN-kebab-case-title.md` with unique three-digit identifiers and `## Status` in the body?
- Is every ADR listed in the collapsed Decision records group inside Architecture in the sidebar?
- Are diagrams Mermaid unless an exception is documented?
- Do Mermaid diagrams avoid fixed inline colors, themes, and initialization directives that undermine light and dark rendering?

## Coverage and boundaries

- Are major components, runtime flows, integrations, data, and failure modes discoverable?
- Do pages state important exclusions and unverified boundaries?
- Are roadmap statements presented as current behavior?

## Severity

- **High**: likely to cause unsafe action, material misunderstanding, production divergence, security or privacy harm, or use of historical material as current truth.
- **Medium**: creates a likely reasoning error, broken task path, ownership gap, or maintainability problem.
- **Low**: local clarity or consistency issue with limited behavioral risk.

Do not inflate severity for style preferences. Preserve positive patterns that materially help readers or agents.
