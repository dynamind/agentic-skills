#!/usr/bin/env python3
"""Create an additive Material for MkDocs documentation scaffold."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


MKDOCS_VERSION = "1.6.1"
MATERIAL_VERSION = "9.7.6"


SECTIONS = {
    "overview": (
        "Overview",
        "Orient readers to the product purpose, context, boundaries, terminology, and system at a glance.",
    ),
    "getting-started": (
        "Getting Started",
        "Guide a newcomer from prerequisites to a verified first successful action.",
    ),
    "features": (
        "Features",
        "Explain user-visible and system capabilities from purpose through behavior and limitations.",
    ),
    "architecture": (
        "Architecture",
        "Explain system structure, runtime flows, data, integrations, deployment, and design decisions.",
    ),
    "interfaces": (
        "Interfaces",
        "Route readers to APIs, user-interface guidance, events, messages, and external integrations.",
    ),
    "development": (
        "Development",
        "Support repository navigation, local workflows, testing, debugging, standards, and contribution.",
    ),
    "operations": (
        "Operations",
        "Support deployment, observability, troubleshooting, recovery, runbooks, and known failure modes.",
    ),
    "security": (
        "Security, Privacy, and Compliance",
        "Explain the security model, access control, data classification, privacy, threats, and audit concerns.",
    ),
    "cookbook": (
        "Cookbook",
        "Collect bounded, goal-oriented development, operational, integration, data, and diagnostic recipes.",
    ),
    "releases": (
        "Releases and Roadmap",
        "Separate shipped versions, migrations, compatibility, and deprecations from planned direction.",
    ),
    "reference": (
        "Reference",
        "Provide exact, authoritative facts organized for lookup rather than narrative reading.",
    ),
    "archive": (
        "Archive",
        "Preserve visibly historical and superseded material without presenting it as current guidance.",
    ),
}


def frontmatter(purpose: str, doc_type: str = "landing", authority: str = "explanatory") -> str:
    return f"""---
purpose: {purpose}
audience:
  - all readers
doc_type: {doc_type}
authority: {authority}
lifecycle: draft
owner: unassigned
last_reviewed: null
sources: []
---
"""


def landing_page() -> str:
    routes = "\n".join(
        f"- **{title}**: [{purpose.split('.')[0]}]({slug}/index.md)."
        for slug, (title, purpose) in SECTIONS.items()
    )
    return (
        frontmatter("Route readers to documentation by intent and system concern.")
        + """
# Documentation

Use this documentation to learn, develop, operate, maintain, and investigate the system.

## Choose a path

- **New to the system:** begin with [Overview](overview/index.md), then follow [Getting Started](getting-started/index.md).
- **Understand a capability:** use [Features](features/index.md), then follow its architecture and interface links.
- **Understand the design:** start with [Architecture](architecture/index.md).
- **Make a change:** combine [Development](development/index.md) with the affected feature, architecture, and interface pages.
- **Investigate a problem:** begin with [Operations](operations/index.md), then follow links to runtime flows and components.
- **Perform a specific task:** search the [Cookbook](cookbook/index.md) and relevant how-to guides.
- **Find an exact fact:** use [Reference](reference/index.md).

## Browse by concern

"""
        + routes
        + """

## Documentation conventions

- Page metadata declares purpose, audience, type, authority, lifecycle, owner, review date, and evidence.
- Summaries may repeat context but link to authoritative detail.
- Historical and superseded material belongs in [Archive](archive/index.md).
- See [Documentation contribution guide](contributing/documentation.md) for the documentation contract.
"""
    )


def section_page(title: str, purpose: str, links: str = "") -> str:
    contents = links or "Add links here as material becomes available. Describe why each destination is relevant rather than listing filenames without context."
    return (
        frontmatter(f"Route readers through {title} documentation.")
        + f"""
# {title}

{purpose}

## In this section

{contents}

## Boundaries

State what belongs in this section and link to adjacent concerns when readers could reasonably look in more than one place.
"""
    )


def overview_page(title: str, purpose: str) -> str:
    return (
        frontmatter(purpose, "explanation")
        + f"""
# {title}

## In brief

Document the smallest useful orientation here. Mark unknowns instead of inferring product facts from repository structure alone.

## Details

Populate this page from verified sources.

## Related material

Add semantic links to authoritative detail.
"""
    )


def adr_index() -> str:
    return (
        frontmatter("Index accepted, proposed, and superseded architecture decision records.", "landing")
        + """
# Architecture Decision Records

Record decisions that materially affect system structure, qualities, interfaces, data, operations, or team constraints.

## Decisions

Store ADRs in this directory using `NNN-kebab-case-title.md`. Reserve `000` for the decision to record architecture decisions; begin product and system decisions at `001`. Preserve accepted records and supersede them with a later decision instead of rewriting history.

- [000 Record architecture decisions](000-record-architecture-decisions.md)
"""
    )


def adr_zero() -> str:
    return (
        frontmatter("Record the convention for architecture decision records.", "decision", "authoritative")
        + """
# ADR-000: Record architecture decisions

Date: YYYY-MM-DD

Decision status: accepted

## Context

Important structural decisions need durable context for onboarding, change planning, and future reconsideration.

## Decision

Record important, structural, hard-to-reverse decisions as ADRs under `docs/architecture/adrs/`. Name files with a three-digit identifier and kebab-case title. Reserve `000` for this convention and begin system decisions at `001`.

## Consequences

- Important rationale remains discoverable beside the architecture documentation.
- Accepted records remain immutable; later ADRs supersede them.
- Routine feature choices stay out of ADRs unless they materially change system structure or constraints.

## Alternatives considered

Document alternatives if this convention is reconsidered.
"""
    )


def documentation_contract() -> str:
    return (
        frontmatter("Define how this documentation is organized, written, governed, and maintained.", "reference", "authoritative")
        + """
# Documentation contribution guide

## Organizing principle

Topic determines where a page lives. Reader intent determines how it is written. Authority determines which facts other pages may repeat.

## Page types

- `landing`: route readers by intent or concern.
- `tutorial`: teach through a guided, reliable learning path.
- `how-to`: help a competent reader achieve a bounded outcome.
- `reference`: provide exact, authoritative facts for lookup.
- `explanation`: build understanding of concepts, behavior, rationale, and trade-offs.
- `decision`: record a decision and its consequences.
- `runbook`: support safe action under operational conditions.
- `release`: describe shipped change.
- `roadmap`: communicate planned direction.

Diataxis informs the first four contracts but does not dictate the top-level navigation.

## Authority and lifecycle

Use `authoritative`, `explanatory`, `generated`, `proposal`, `historical`, or `superseded` for authority. Use `draft`, `current`, `needs-review`, or `archived` for `lifecycle`. Do not use `status` for the page lifecycle because Material for MkDocs reserves it for navigation badges.

Keep exact facts in one authoritative location. Repeat concise narrative context when it helps a page stand alone, and link summaries to authoritative detail.

## Evidence

Use code for current implementation, tests for enforced behavior, accepted requirements for business intent, ADRs for rationale, and runtime evidence for deployed behavior. Report conflicts instead of silently blending sources.

## Links and boundaries

Use link text that explains why the destination matters. State important exclusions and unverified boundaries explicitly.

## Diagrams

Use Mermaid for diagrams. Prefer structure, shapes, labels, subgraphs, and line types over color. Avoid diagram-local `style`, color-bearing `classDef`, `themeVariables`, and init directives because fixed presentation commonly fails across light and dark palettes.

## Architecture decisions

Store ADRs under `architecture/adrs/` using `NNN-kebab-case-title.md`. Reserve `000` for the ADR convention. Add each ADR to the ADR index and MkDocs navigation immediately after the Architecture section.

## Source of truth

Treat the documentation tree as authoritative for product, setup, configuration, architecture, development, and operations guidance. Keep the repository `README.md` as a thin signpost containing only product identity and links that are unlikely to drift. Keep `AGENTS.md` at the root for agent operating instructions; move other narrative documentation into this tree unless an explicit exception is justified.

## Templates

Use the templates under `contributing/templates/` as starting points. Adapt them to the page contract; do not preserve headings that add no reader value.
"""
    )


def manifest() -> str:
    section_lines = "\n".join(f"  - {slug}" for slug in SECTIONS)
    return f"""version: 1
entrypoint: index.md
sections:
{section_lines}
metadata:
  required:
    - purpose
    - audience
    - doc_type
    - authority
    - lifecycle
    - owner
    - last_reviewed
  doc_types: [landing, tutorial, how-to, reference, explanation, decision, runbook, release, roadmap]
  authorities: [authoritative, explanatory, generated, proposal, historical, superseded]
  lifecycles: [draft, current, needs-review, archived]
archive:
  path: archive/
  current_content_allowed: false
adrs:
  path: architecture/adrs/
  filename_pattern: NNN-kebab-case-title.md
  convention_record: 000-record-architecture-decisions.md
diagrams:
  format: mermaid
  inline_color_styling: discouraged
authority:
  primary_documentation: docs/
  root_readme: signpost-only
  root_documentation_exceptions: [README.md, AGENTS.md]
"""


def scaffold_files() -> dict[Path, str]:
    files = {Path("index.md"): landing_page(), Path("documentation.yaml"): manifest()}
    for slug, (title, purpose) in SECTIONS.items():
        files[Path(slug) / "index.md"] = section_page(title, purpose)
    files[Path("overview") / "index.md"] = section_page(
        "Overview",
        SECTIONS["overview"][1],
        """- [Business Context](business-context.md) explains the problem, stakeholders, value, and constraints.
- [System at a Glance](system-at-a-glance.md) loads the smallest useful system mental model.
- [Concepts and Terminology](concepts-and-terminology.md) defines stable domain language and distinctions.
- [Scope and Boundaries](scope-and-boundaries.md) states system ownership, dependencies, and exclusions.""",
    )
    files[Path("architecture") / "index.md"] = section_page(
        "Architecture",
        SECTIONS["architecture"][1],
        "Begin with the current architecture overview, then descend into context, components, runtime flows, data, integrations, deployment, and cross-cutting concerns as those pages are established. See [Architecture Decision Records](adrs/index.md) for consequential design decisions and their status.",
    )
    files[Path("overview") / "business-context.md"] = overview_page(
        "Business Context", "Explain the business problem, stakeholders, value, and constraints."
    )
    files[Path("overview") / "system-at-a-glance.md"] = overview_page(
        "System at a Glance", "Give a compact mental model of capabilities, components, dependencies, data flows, and constraints."
    )
    files[Path("overview") / "concepts-and-terminology.md"] = overview_page(
        "Concepts and Terminology", "Define stable domain language, synonyms, and easily confused concepts."
    )
    files[Path("overview") / "scope-and-boundaries.md"] = overview_page(
        "Scope and Boundaries", "State what the system owns, depends on, exposes, and explicitly does not cover."
    )
    files[Path("architecture") / "adrs" / "index.md"] = adr_index()
    files[Path("architecture") / "adrs" / "000-record-architecture-decisions.md"] = adr_zero()
    files[Path("contributing") / "documentation.md"] = documentation_contract()
    return files


def mkdocs_config(site_name: str, docs_dir: str) -> str:
    return f"""site_name: {json.dumps(site_name)}
docs_dir: {json.dumps(docs_dir)}
site_dir: site
strict: true

theme:
  name: material
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

markdown_extensions:
  - meta
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

exclude_docs: |
  documentation.yaml
  contributing/templates/

validation:
  omitted_files: warn
  absolute_links: relative_to_docs
  unrecognized_links: warn
  anchors: warn

nav:
  - Home: index.md
  - Overview:
      - Introduction: overview/index.md
      - Business Context: overview/business-context.md
      - System at a Glance: overview/system-at-a-glance.md
      - Concepts and Terminology: overview/concepts-and-terminology.md
      - Scope and Boundaries: overview/scope-and-boundaries.md
  - Getting Started: getting-started/index.md
  - Features: features/index.md
  - Architecture:
      - Overview: architecture/index.md
  - ADRs:
      - Overview: architecture/adrs/index.md
      - 000 Record architecture decisions: architecture/adrs/000-record-architecture-decisions.md
  - Interfaces: interfaces/index.md
  - Development:
      - Overview: development/index.md
      - Documentation standards: contributing/documentation.md
  - Operations: operations/index.md
  - Security, Privacy, and Compliance: security/index.md
  - Cookbook: cookbook/index.md
  - Releases and Roadmap: releases/index.md
  - Reference: reference/index.md
  - Archive: archive/index.md
"""


def requirements() -> str:
    return f"mkdocs=={MKDOCS_VERSION}\nmkdocs-material=={MATERIAL_VERSION}\n"


def root_readme(site_name: str, docs_dir: str) -> str:
    return f"""# {site_name}

Project documentation is authoritative under [`{docs_dir}/`]({docs_dir}/index.md).

- Start with the [documentation home]({docs_dir}/index.md).
- Follow [Getting Started]({docs_dir}/getting-started/index.md) for setup and first use.
- Use [Architecture]({docs_dir}/architecture/index.md) for system design.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory)")
    parser.add_argument("--docs-dir", default="docs", help="Relative documentation directory (default: docs)")
    parser.add_argument("--site-name", help="MkDocs site name (default: repository directory name)")
    parser.add_argument("--without-mkdocs", action="store_true", help="Do not create MkDocs configuration and dependencies")
    parser.add_argument("--without-root-readme", action="store_true", help="Do not create a thin root README when one is absent")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing scaffold-owned files")
    return parser.parse_args()


def resolve_target(root: Path, docs_dir: str) -> Path:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Repository root does not exist or is not a directory: {root}")
    relative = Path(docs_dir)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("--docs-dir must be a relative path inside the repository")
    return root / relative


def main() -> int:
    args = parse_args()
    try:
        target = resolve_target(args.root, args.docs_dir)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    root = args.root.expanduser().resolve()
    site_name = args.site_name or root.name.replace("-", " ").replace("_", " ").title()
    asset_dir = Path(__file__).resolve().parent.parent / "assets" / "page-templates"
    operations: list[tuple[str, Path]] = []

    for relative, content in scaffold_files().items():
        destination = target / relative
        if destination.exists() and not args.overwrite:
            operations.append(("skip", destination))
            continue
        operations.append(("overwrite" if destination.exists() else "create", destination))
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")

    if not args.without_mkdocs:
        repository_files = {
            root / "mkdocs.yml": mkdocs_config(site_name, args.docs_dir),
            root / "requirements-docs.txt": requirements(),
        }
        for destination, content in repository_files.items():
            if destination.exists() and not args.overwrite:
                operations.append(("skip", destination))
                continue
            operations.append(("overwrite" if destination.exists() else "create", destination))
            if not args.dry_run:
                destination.write_text(content, encoding="utf-8")

    if not args.without_root_readme:
        readme = root / "README.md"
        if readme.exists():
            operations.append(("skip", readme))
        else:
            operations.append(("create", readme))
            if not args.dry_run:
                readme.write_text(root_readme(site_name, args.docs_dir), encoding="utf-8")

    template_target = target / "contributing" / "templates"
    for source in sorted(asset_dir.glob("*.md")):
        destination = template_target / source.name
        if destination.exists() and not args.overwrite:
            operations.append(("skip", destination))
            continue
        operations.append(("overwrite" if destination.exists() else "create", destination))
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

    for action, path in operations:
        print(f"{action:9} {path}")
    counts = {action: sum(1 for value, _ in operations if value == action) for action in ("create", "overwrite", "skip")}
    prefix = "Would process" if args.dry_run else "Processed"
    print(f"{prefix} {len(operations)} files: {counts['create']} create, {counts['overwrite']} overwrite, {counts['skip']} skip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
