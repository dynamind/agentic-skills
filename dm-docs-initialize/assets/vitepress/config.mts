import {defineConfig} from 'vitepress'
import {withMermaid} from 'vitepress-plugin-mermaid'
import {extractGlossaryTerms} from './glossary/extract-terms.mjs'
import {glossaryPlugin} from './glossary/glossary-plugin.mjs'
import {dedupeGlossaryLinks} from './glossary/dedupe-html.mjs'
import {glossarySourceWatcher} from './glossary/watch-sources.mjs'

// Glossary terms are scraped from glossary.md itself (see glossary/extract-terms.mjs)
// so that page stays the only place a term is authored. The first mention of a
// term on each page links to its definition with a CSS-only tooltip.
const docsDir = new URL('../', import.meta.url)
const glossaryTerms = extractGlossaryTerms(docsDir)

// Living documentation for {{SITE_NAME}}. VitePress + Mermaid, the same
// toolchain as the other living-documentation sites, so they feel alike.
//
// cleanUrls stays off because a plain static server serves files as-is (no
// extensionless-URL rewriting). Set base and outDir when the site is hosted
// under a path or built into a repo-level folder.
export default withMermaid(
  defineConfig({
    title: '{{SITE_NAME}}',
    description: 'Living guide and knowledge base for {{SITE_NAME}}',
    lang: 'en',
    base: '/',
    cleanUrls: false,
    lastUpdated: false,

    // Content that lives in docs/ but is kept out of the rendered site.
    srcExclude: ['archived/**'],

    // Dead-link checking stays ON. Add a pattern here only for links that
    // deliberately point outside the rendered site (repo files, auth-gated
    // wikis) and say why in a comment.
    ignoreDeadLinks: [],

    // vitepress-plugin-mermaid: mermaid's CommonJS deps (fastdom) need
    // pre-bundling or the dev server's browser rejects their default export.
    markdown: {
      config: (md) => {
        md.use(glossaryPlugin, {terms: glossaryTerms, firstOccurrenceOnly: true})
      },
    },

    // VitePress renders a page more than once per build, so the plugin's own
    // first-occurrence bookkeeping is not enough. This hook runs once per final page.
    transformHtml(code) {
      return dedupeGlossaryLinks(code)
    },

    vite: {
      plugins: [glossarySourceWatcher(docsDir)],
      optimizeDeps: {include: ['mermaid', 'dayjs', 'fastdom', '@braintree/sanitize-url']},
    },

    themeConfig: {
      nav: [
        {text: 'Guide', link: '/guide/'},
        {text: 'Architecture', link: '/architecture/overview'},
        {text: 'Glossary', link: '/glossary'},
      ],
      search: {provider: 'local'},
      outline: {level: [2, 3]},

      // Every page goes in the sidebar, or nobody finds it. Grow the groups
      // below as pages land; a group with no pages yet is not listed.
      sidebar: [
        {text: 'Home', link: '/'},
        {
          text: 'Guide',
          collapsed: false,
          items: [
            {text: 'Introduction', link: '/guide/'},
            {text: 'Glossary', link: '/glossary'},
          ],
        },
        {
          text: 'Product',
          collapsed: false,
          items: [
            {text: 'Ideas', link: '/product/ideas'},
            {text: 'Questions', link: '/product/questions'},
          ],
        },
        {
          text: 'Architecture',
          collapsed: false,
          items: [
            {text: 'Overview', link: '/architecture/overview'},
            {text: 'Exceptions', link: '/architecture/exceptions'},
            // {text: 'Decision records', collapsed: true, items: [
            //   {text: 'ADR-001 Title', link: '/architecture/adrs/adr-001-title'},
            // ]},
          ],
        },
      ],
    },

    // Mermaid rendering: vitepress-plugin-mermaid switches diagrams between
    // mermaid's default and dark themes with the site palette. That only works
    // because the diagrams themselves stay theme-neutral: no diagram-local
    // fills or colors (line types and stroke widths are fine).
  }),
)
