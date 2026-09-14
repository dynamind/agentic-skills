#!/usr/bin/env python3
"""Scaffold the living-documentation baseline: a VitePress site under docs/ and the
agent layer (AGENTS.md, CLAUDE.md, .agents/) at the repository root.

Additive by default: an existing file is left alone and reported. Templates come from
../assets and carry {{SITE_NAME}}, {{SITE_SLUG}}, {{PORT}} and {{BACKLOG}} placeholders.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# destination (relative to repository root) -> template (relative to assets/)
DOCS_FILES = {
    "docs/package.json": "vitepress/package.json",
    "docs/.npmrc": "vitepress/.npmrc",
    "docs/.vitepress/config.mts": "vitepress/config.mts",
    "docs/.vitepress/theme/index.ts": "vitepress/theme/index.ts",
    "docs/.vitepress/theme/custom.css": "vitepress/theme/custom.css",
    "docs/.vitepress/glossary/extract-terms.mjs": "vitepress/glossary/extract-terms.mjs",
    "docs/.vitepress/glossary/glossary-plugin.mjs": "vitepress/glossary/glossary-plugin.mjs",
    "docs/.vitepress/glossary/dedupe-html.mjs": "vitepress/glossary/dedupe-html.mjs",
    "docs/.vitepress/glossary/watch-sources.mjs": "vitepress/glossary/watch-sources.mjs",
    "docs/index.md": "pages/index.md",
    "docs/guide/index.md": "pages/guide-index.md",
    "docs/glossary.md": "pages/glossary.md",
    "docs/product/ideas.md": "pages/ideas.md",
    "docs/product/questions.md": "pages/questions.md",
    "docs/architecture/overview.md": "pages/architecture-overview.md",
    "docs/architecture/exceptions.md": "pages/exceptions.md",
}
AGENT_FILES = {
    "AGENTS.md": "agents/AGENTS.md",
    "CLAUDE.md": "agents/CLAUDE.md",
    ".agents/writing-guide.md": "agents/writing-guide.md",
    ".agents/decisions.md": "agents/decisions.md",
}
GITIGNORE_LINES = ("docs/node_modules/", "docs/.vitepress/cache/", "docs/.vitepress/dist/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: cwd)")
    parser.add_argument("--site-name", help="Site title (default: repository directory name, title case)")
    parser.add_argument("--slug", help="npm package prefix (default: kebab-case of the directory name)")
    parser.add_argument("--port", type=int, default=8000, help="Dev and preview server port (default: 8000)")
    parser.add_argument("--backlog-url", help="Link to the formal backlog, used by docs/product/ideas.md")
    parser.add_argument("--without-agents", action="store_true", help="Do not create AGENTS.md, CLAUDE.md, or .agents/")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing scaffold-owned files")
    return parser.parse_args()


def kebab(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value or "project"


def render(template: Path, values: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.findall(r"{{[A-Z_]+}}", text)
    if leftover:
        raise SystemExit(f"error: unreplaced placeholders {sorted(set(leftover))} in {template}")
    return text


def plan_file(root: Path, relative: str, content: str, overwrite: bool) -> tuple[str, Path, str | None]:
    destination = root / relative
    if not destination.exists():
        return "create", destination, content
    if destination.read_text(encoding="utf-8") == content:
        return "unchanged", destination, None
    if relative == "CLAUDE.md":
        # A CLAUDE.md with its own content holds guidance that must move into
        # AGENTS.md, .agents/, or docs/ first. Never clobber it.
        return "fold-into-agents", destination, None
    if overwrite:
        return "overwrite", destination, content
    return "skip", destination, None


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"error: repository root does not exist: {root}", file=sys.stderr)
        return 2

    site_name = args.site_name or root.name.replace("-", " ").replace("_", " ").title()
    values = {
        "SITE_NAME": site_name,
        "SITE_SLUG": args.slug or kebab(root.name),
        "PORT": str(args.port),
        "BACKLOG": f"[backlog]({args.backlog_url})" if args.backlog_url else "backlog",
    }

    files = dict(DOCS_FILES)
    if not args.without_agents:
        files.update(AGENT_FILES)

    actions = []
    for relative, template in files.items():
        content = render(ASSETS / template, values)
        actions.append(plan_file(root, relative, content, args.overwrite))

    gitignore = root / ".gitignore"
    existing_ignore = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    missing_ignore = [line for line in GITIGNORE_LINES if line not in existing_ignore.splitlines()]

    for action, destination, _ in actions:
        print(f"{action:>17}  {destination.relative_to(root).as_posix()}")
    if missing_ignore:
        print(f"{'append':>17}  .gitignore  ({', '.join(missing_ignore)})")
    print(f"{'ensure dir':>17}  docs/architecture/adrs/  (first ADR is adr-001-<kebab-title>.md)")

    if args.dry_run:
        print("\nDry run: nothing written.")
        return 0

    for action, destination, content in actions:
        if content is None:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    (root / "docs" / "architecture" / "adrs").mkdir(parents=True, exist_ok=True)
    if missing_ignore:
        prefix = "" if not existing_ignore or existing_ignore.endswith("\n") else "\n"
        with gitignore.open("a", encoding="utf-8") as handle:
            handle.write(prefix + "\n# Docs site toolchain\n" + "\n".join(missing_ignore) + "\n")

    folded = [d for a, d, _ in actions if a == "fold-into-agents"]
    if folded:
        print(
            "\nCLAUDE.md has its own content. Move the durable guidance into AGENTS.md, a "
            ".agents/ module, or docs/, then replace CLAUDE.md with the single line @AGENTS.md."
        )
    print("\nNext: npm --prefix docs install, then npm --prefix docs run docs:build.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
