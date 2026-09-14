// markdown-it core rule: links the first mention of each glossary term (per
// page) to its definition and attaches the definition's first sentence as a
// CSS-only hover/focus tooltip (see theme/custom.css, .glossary-term). No Vue
// component, no client-side JS: plain <a data-tooltip> and a couple of
// pseudo-elements, so it survives static prerendering with zero hydration
// risk.
//
// Deliberately skips:
// - link label text (avoids nesting a focusable element inside an <a>)
// - heading text (avoids a term self-linking inside its own `#### Heading`)
// - a term linking back to the very page that defines it
export function glossaryPlugin(md, {terms = [], firstOccurrenceOnly = true} = {}) {
  if (terms.length === 0) return

  // Longest alias first, so "Route Start" matches whole rather than being
  // shadowed by the shorter "Route" alternative earlier in the pattern.
  const sorted = [...terms].sort((a, b) => b.alias.length - a.alias.length)
  const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const matchRe = new RegExp(`\\b(${sorted.map((t) => escapeRe(t.alias)).join('|')})\\b`, 'i')
  const byLowerAlias = new Map(sorted.map((t) => [t.alias.toLowerCase(), t]))

  md.core.ruler.push('glossary_link', (state) => {
    const relativePath = state.env?.relativePath
    // Container titles (`::: warning <title>`) render through their own
    // renderInline() pass, a separate core-ruler run from the page body's;
    // stash dedup state on the shared env object, not a call-local Set, so
    // "first occurrence" means first on the page, not first per render call.
    // VitePress renders each page's markdown more than once per build (e.g.
    // once for content, once while resolving page data); each call gets its
    // own `env`, so per-page "first occurrence" can't be enforced here.
    // Scoping to env is still worth doing (it cuts down what the final,
    // definitely-once-per-page cleanup in transformHtml (see config.mts)
    // has to remove) but is not itself the correctness guarantee.
    const env = state.env ?? {}
    const used = (env.__glossaryUsed ??= new Set())
    let headingDepth = 0

    for (let bi = 0; bi < state.tokens.length; bi++) {
      const block = state.tokens[bi]
      if (block.type === 'heading_open') {
        headingDepth++
        continue
      }
      if (block.type === 'heading_close') {
        headingDepth--
        continue
      }
      if (block.type !== 'inline' || headingDepth > 0 || !block.children) continue

      const children = block.children
      let linkDepth = 0
      for (let i = 0; i < children.length; i++) {
        const tok = children[i]
        if (tok.type === 'link_open') {
          linkDepth++
          continue
        }
        if (tok.type === 'link_close') {
          linkDepth--
          continue
        }
        if (tok.type !== 'text' || linkDepth > 0) continue

        const content = tok.content
        const m = matchRe.exec(content)
        if (!m) continue

        const term = byLowerAlias.get(m[1].toLowerCase())
        if (!term || term.sourcePath === relativePath) continue
        if (firstOccurrenceOnly && used.has(term.anchor)) continue
        if (firstOccurrenceOnly) used.add(term.anchor)

        const beforeTok = new state.Token('text', '', 0)
        beforeTok.content = content.slice(0, m.index)
        const openTok = new state.Token('link_open', 'a', 1)
        openTok.attrs = [
          ['href', term.href],
          ['class', 'glossary-term'],
          ['data-tooltip', term.blurb],
        ]
        const textTok = new state.Token('text', '', 0)
        textTok.content = m[1]
        const closeTok = new state.Token('link_close', 'a', -1)
        const afterTok = new state.Token('text', '', 0)
        afterTok.content = content.slice(m.index + m[1].length)

        children.splice(i, 1, beforeTok, openTok, textTok, closeTok, afterTok)
        // Resume scanning at afterTok; the remainder of this text node may
        // still contain a different, still-unused term.
        i += 3
      }
    }
  })
}
