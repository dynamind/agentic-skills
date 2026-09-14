// VitePress renders a page's markdown more than once per build, so
// glossary-plugin.mjs's own "first occurrence" bookkeeping can't see across
// every pass — see the comment in glossary-plugin.mjs. This runs once per
// FINAL page (VitePress's transformHtml hook, right before the file is
// written) and is the actual guarantee: keep only the first glossary link to
// a given anchor, unwrap any later one back to plain text.
const LINK_RE = /<a href="([^"]*)" class="glossary-term" data-tooltip="[^"]*">([^<]*)<\/a>/g

export function dedupeGlossaryLinks(html) {
  const seen = new Set()
  return html.replace(LINK_RE, (full, href, text) => {
    if (seen.has(href)) return text
    seen.add(href)
    return full
  })
}
