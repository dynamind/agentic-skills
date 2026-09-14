# VitePress profile

The toolchain is VitePress with `vitepress-plugin-mermaid`. `docs/` is a self-contained
npm project so the docs build needs no other part of the repository.

## Files

| File | Purpose |
|---|---|
| `docs/package.json` | `docs:dev`, `docs:build`, `docs:preview` scripts; `engines.node` pinned to the current LTS major |
| `docs/.npmrc` | supply-chain hardening: `ignore-scripts`, `save-exact`, `min-release-age` |
| `docs/.vitepress/config.mts` | site config, nav, sidebar, dead-link policy, `srcExclude` |
| `docs/.vitepress/theme/index.ts`, `custom.css` | default theme plus brand color, the Mermaid label fix, and the glossary tooltip style |
| `docs/.vitepress/glossary/*.mjs` | build-time glossary linking, see below |

Templates are in `../assets/vitepress/`.

## Running npm

Run npm against `docs/`, never against the repository root. The root has no
`package.json`, so npm would silently create a stub `node_modules/` there. Set the
directory on the command:

```bash
npm --prefix docs install
npm --prefix docs run docs:build
npm --prefix docs run docs:dev
```

`install` downloads packages. Ask before the first install in a repository the user has
not built before.

## Config decisions

- `cleanUrls: false`. A plain static host serves files as-is.
- `lastUpdated: false`. Git dates are not accurate on a living document.
- `srcExclude` keeps `archived/**` and other non-rendered material out of the site but in
  the repository.
- `ignoreDeadLinks` is a list of patterns, never `true`. Each pattern has a comment that
  says which links it exempts and why (a repo file outside the site, an auth-gated wiki).
- `search: {provider: 'local'}`. No external service.
- `outline: {level: [2, 3]}`.
- The `optimizeDeps.include` list for Mermaid's CommonJS dependencies is needed for the
  dev server, not the build. Keep it; the failure without it is a blank diagram in dev.
- `base` and `outDir` change only when hosting requires it. Record the hosting setup in a
  how-to when the site is deployed.

## Glossary linking

A markdown-it rule links the first mention of each glossary term on a page to its
`#### Term` heading in `docs/glossary.md` and attaches the definition's first sentence as a
CSS-only tooltip. No Vue component, no client JavaScript, no second data file: the term
list is scraped from the glossary page at build time, so that page stays the only place a
term is authored.

- `extract-terms.mjs` reads every `#### Term` heading. A heading `Term / Alias` yields two
  aliases; a trailing `(qualifier)` is dropped from the alias. Headings with `vs.` or a
  backtick are skipped. Entries under `## Systems` are tagged `system`, the rest `domain`.
- `glossary-plugin.mjs` links the first occurrence per page, skipping headings, link text,
  and the glossary page itself. Longest alias wins.
- `dedupe-html.mjs` runs in `transformHtml`, once per final page, and is the real
  first-occurrence guarantee.
- `watch-sources.mjs` restarts the dev server when the glossary changes, because the
  scrape is a plain file read that Vite does not track.

The slugify in `extract-terms.mjs` is a port of VitePress's own. Do not replace it with
the markdown-it-anchor default; the two disagree on punctuation and the anchors break.

## Sidebar

Every page must be in the sidebar. Otherwise, a reader cannot find it. Groups follow the tree: Home, Guide,
Product, Architecture (with a collapsed Decision records group listing each ADR by number
and title), Explanation, How-to or Operations, Reference. A group is listed when it has a
page. Section indexes are labeled `Introduction` under Guide and `Overview` elsewhere.
Never `Architecture > Architecture`.

The sidebar is not checked by the build. A sidebar link to a page that does not exist
renders a 404 silently. Add the sidebar entry in the same change as the page.

## Verification

```bash
npm --prefix docs run docs:build
```

The build fails on a dead relative link. It does not check `#anchors`, sidebar links, or
links in code spans. After the build:

- open the dev server and check each Mermaid diagram in light and dark;
- confirm every new page appears in the sidebar;
- confirm `docs/.vitepress/cache/`, `docs/.vitepress/dist/`, and `docs/node_modules/` are
  ignored by git.

## CI

Add a step that runs `npm --prefix docs run docs:build` first and on its own, with a
pinned Node and npm, so a broken page fails the run before anything else is built. The
site is deployed as a standalone static site; the application artifact does not carry it.
