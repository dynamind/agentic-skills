# Material for MkDocs Profile

Use this profile as the default for a new site. Preserve and adapt an existing MkDocs configuration instead of replacing it.

## Generated files

```text
mkdocs.yml
requirements-docs.txt
docs/
├── index.md
├── documentation.yaml
└── architecture/adrs/
    ├── index.md
    └── 000-record-architecture-decisions.md
```

Pin the tested runtime:

```text
mkdocs==1.6.1
mkdocs-material==9.7.6
```

Detect first:

```bash
python3 -m mkdocs --version
python3 -m pip show mkdocs mkdocs-material
```

Install only with explicit user authorization:

```bash
python3 -m pip install -r requirements-docs.txt
```

Prefer the module form because it binds pip and MkDocs to the selected Python 3 interpreter. Use `pip3` as a fallback; do not use ambiguous bare `pip`.

## Navigation

Use `docs/index.md` as the site homepage. Define explicit navigation and include every current Markdown page. Label a section's `index.md` as `Overview`; use `Introduction` when the section itself is named Overview. Avoid doubled labels such as `Architecture > Architecture` and `Overview > Overview`. Put `ADRs` immediately after `Architecture` as a sibling navigation entry while keeping files under `docs/architecture/adrs/`.

Use `lifecycle` for document state. Do not use Material's reserved `status` frontmatter key unless a deliberate navigation badge is wanted.

Exclude authoring-only files:

```yaml
exclude_docs: |
  documentation.yaml
  contributing/templates/
```

## Mermaid and dark mode

Use Material's native Mermaid support:

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

Do not install `mkdocs-mermaid2-plugin` for this profile. Author diagrams as `mermaid` fences. Prefer topology, shapes, labels, subgraphs, and line types over fixed colors. Avoid diagram-local `style`, color-bearing `classDef`, `themeVariables`, and init directives. Put unavoidable styling at site level and verify both light and dark palettes.

## Validation

Set `strict: true`, enable warnings for omitted navigation, absolute links, unrecognized links, and anchors, then run:

```bash
python3 -m mkdocs build --strict
```

Treat the MkDocs build as authoritative for configuration, navigation, plugin, and rendered-link validity. Use the gardening inspector for additional repository conventions and diagnostic findings.
