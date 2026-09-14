// Scrapes glossary terms directly out of glossary.md so that page
// stays the ONLY place a term is authored. No separate glossary.json: the
// tooltip data and the human-readable definition are the same text,
// extracted at build time.
//
// Known limitations (acceptable for the prototype, not fixed here):
// - Headings that contrast two distinct terms (containing "vs." or a
//   backtick) are skipped rather than guessed at, e.g.
//   "Customer service vs. `customer-support`".
import {readFileSync} from 'node:fs'

const SOURCE = {file: 'glossary.md', href: '/glossary'}
const SYSTEM_SECTION = 'Systems'

function stripMarkdown(text) {
  return text
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
}

// Ported verbatim from VitePress's own slugify (node_modules/vitepress/dist/node,
// search "const slugify = (str) =>"; this is VitePress's own override, not the
// markdown-it-anchor library default, and the two disagree). Guessing at this
// from a handful of observed anchors cost two rounds of wrong output (a
// double-hyphen theory, then a "strip punctuation, don't hyphenate it" theory
// that missed apostrophes specifically). Reading the real implementation is
// what finally matched every case, including "don't" -> "don-t".
const R_COMBINING = /[\u0300-\u036F]/g
const R_CONTROL = /[\u0000-\u001f]/g
const R_SPECIAL = /[\s~`!@#$%^&*()\-_+=[\]{}|\\;:"'“”‘’<>,.?/]+/g

function slugify(headingText) {
  return stripMarkdown(headingText)
    .normalize('NFKD')
    .replace(R_COMBINING, '')
    .replace(R_CONTROL, '')
    .replace(R_SPECIAL, '-')
    .replace(/-{2,}/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/^(\d)/, '_$1')
    .toLowerCase()
}

function firstSentence(bodyText) {
  const plain = stripMarkdown(bodyText)
    .split('\n')
    .filter((line) => !line.trim().startsWith('>')) // drop blockquote/TODO admonitions
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim()
  const match = plain.match(/^(.*?[.!?])\s/)
  const sentence = match ? match[1] : plain
  return sentence.length > 220 ? `${sentence.slice(0, 217)}...` : sentence
}

function aliasesFor(headingText) {
  if (/\bvs\.?\b/i.test(headingText) || headingText.includes('`')) return []
  return headingText
    .split(' / ')
    .map((part) => part.replace(/\s*\([^)]*\)\s*$/, '').trim())
    .filter(Boolean)
}

// Every `#### Term` heading becomes an entry; `kind` follows which `## Section`
// it falls under (SYSTEM_SECTION -> 'system', everything else -> 'domain') so
// downstream code can tell "real-world system" apart from "our domain word"
// without needing a second source file.
export function extractGlossaryTerms(docsDir) {
  const raw = readFileSync(new URL(SOURCE.file, docsDir), 'utf8')
  const headingRe = /^(#{2,4})\s+(.+)$/gm
  const matches = []
  let match
  while ((match = headingRe.exec(raw))) {
    matches.push({level: match[1].length, heading: match[2], index: match.index, end: headingRe.lastIndex})
  }

  const entries = []
  let currentSection = ''
  for (let i = 0; i < matches.length; i++) {
    const {level, heading, end} = matches[i]
    if (level === 2) {
      currentSection = heading
      continue
    }
    if (level !== 4) continue

    const nextIndex = i + 1 < matches.length ? matches[i + 1].index : raw.length
    const body = raw.slice(end, nextIndex)
    const anchor = slugify(heading)
    const blurb = firstSentence(body)
    const kind = currentSection === SYSTEM_SECTION ? 'system' : 'domain'

    for (const alias of aliasesFor(heading)) {
      entries.push({
        alias,
        heading,
        anchor,
        href: `${SOURCE.href}#${anchor}`,
        blurb,
        kind,
        sourcePath: SOURCE.file,
      })
    }
  }
  return entries
}
