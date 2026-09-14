import {fileURLToPath} from 'node:url'

// extract-terms.mjs reads glossary.md via fs.readFileSync, not
// import, so Vite's dev server has no idea it's a dependency of config.mts
// and won't reload glossaryTerms when it changes. This plugin watches it
// explicitly and restarts the server on change — without it, editing the
// glossary during `docs:dev` silently keeps serving the term list from
// whenever the server last started.
export function glossarySourceWatcher(docsDir) {
  const watched = ['glossary.md'].map((file) => fileURLToPath(new URL(file, docsDir)))

  return {
    name: 'glossary-source-watcher',
    configureServer(server) {
      server.watcher.add(watched)
      server.watcher.on('change', (file) => {
        if (watched.includes(file)) server.restart()
      })
    },
  }
}
