#!/usr/bin/env python3
"""Run dependency-free structural checks over a Markdown documentation tree."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, deque
from pathlib import Path
from urllib.parse import unquote


REQUIRED_METADATA = (
    "purpose",
    "audience",
    "doc_type",
    "authority",
    "lifecycle",
    "owner",
    "last_reviewed",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
ADR_NAME_RE = re.compile(r"^(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
MERMAID_RE = re.compile(r"```mermaid[ \t]*\n(.*?)```", re.DOTALL | re.IGNORECASE)
NON_MERMAID_DIAGRAM_RE = re.compile(r"```(?:plantuml|puml|graphviz|dot)[ \t]*\n", re.IGNORECASE)
MERMAID_INLINE_STYLE_RE = re.compile(
    r"(^\s*style\s+|^\s*classDef\b.*(?:fill|stroke|color|background)\s*:|themeVariables|%%\{init:|^\s*theme\s*:)",
    re.MULTILINE | re.IGNORECASE,
)
NAV_SECTION_RE = re.compile(r"^  - ([^:]+):\s*$")
NAV_INDEX_RE = re.compile(r"^      - ([^:]+):\s+.+/index\.md\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_dir", type=Path, help="Documentation directory to inspect")
    parser.add_argument("--entrypoint", help="Relative landing page; defaults to index.md, then README.md")
    parser.add_argument("--exclude", action="append", default=[], help="Relative directory or file to exclude; repeatable")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when warnings exist")
    return parser.parse_args()


def parse_frontmatter(text: str) -> tuple[dict[str, str], bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return metadata, True
        if line.startswith((" ", "\t", "-")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return {}, False


def excluded(relative: Path, exclusions: tuple[Path, ...]) -> bool:
    return any(relative == item or item in relative.parents for item in exclusions)


def markdown_files(root: Path, exclusions: tuple[Path, ...]) -> list[Path]:
    result = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if not excluded(relative, exclusions):
            result.append(path)
    return result


def clean_link(raw: str) -> str | None:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target or target.startswith(("#", "/", "//")) or SCHEME_RE.match(target):
        return None
    return target


def resolve_markdown_target(source: Path, target: str) -> Path | None:
    candidate = (source.parent / target).resolve()
    if candidate.is_file():
        return candidate
    if candidate.is_dir():
        for name in ("index.md", "README.md"):
            nested = candidate / name
            if nested.is_file():
                return nested.resolve()
    if not candidate.suffix:
        markdown = candidate.with_suffix(".md")
        if markdown.is_file():
            return markdown.resolve()
    return None


def add_finding(findings: list[dict[str, str]], severity: str, code: str, path: Path, message: str) -> None:
    findings.append({"severity": severity, "code": code, "path": path.as_posix(), "message": message})


def inspect_mkdocs_navigation(config: Path, findings: list[dict[str, str]]) -> None:
    section: str | None = None
    for line in config.read_text(encoding="utf-8").splitlines():
        section_match = NAV_SECTION_RE.match(line)
        if section_match:
            section = section_match.group(1).strip().strip('"\'')
            continue
        index_match = NAV_INDEX_RE.match(line)
        if section and index_match:
            label = index_match.group(1).strip().strip('"\'')
            expected = "Introduction" if section.casefold() == "overview" else "Overview"
            if label.casefold() == section.casefold():
                add_finding(
                    findings,
                    "warning",
                    "nav-section-label-duplicate",
                    Path("../mkdocs.yml"),
                    f"Section {section} repeats its name for its index page; label the index {expected}",
                )
            elif label != expected:
                add_finding(
                    findings,
                    "warning",
                    "nav-section-index-label",
                    Path("../mkdocs.yml"),
                    f"Label the {section} section index {expected}, not {label}",
                )
            section = None


def inspect(root: Path, entrypoint: Path, exclusions: tuple[Path, ...]) -> tuple[list[dict[str, str]], dict[str, int]]:
    findings: list[dict[str, str]] = []
    files = markdown_files(root, exclusions)
    resolved_to_relative = {path.resolve(): path.relative_to(root) for path in files}
    graph: dict[Path, set[Path]] = {path.relative_to(root): set() for path in files}
    titles: dict[str, list[Path]] = {}
    adr_identifiers: dict[str, list[Path]] = {}

    for path in files:
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")

        if relative.parts[:2] == ("architecture", "adrs") and relative.name != "index.md":
            adr_match = ADR_NAME_RE.fullmatch(relative.name)
            if not adr_match:
                add_finding(
                    findings,
                    "error",
                    "adr-name-invalid",
                    relative,
                    "ADR filename must use NNN-kebab-case-title.md",
                )
            else:
                adr_identifiers.setdefault(adr_match.group(1), []).append(relative)

        if NON_MERMAID_DIAGRAM_RE.search(text):
            add_finding(
                findings,
                "warning",
                "diagram-not-mermaid",
                relative,
                "Non-Mermaid diagram fence conflicts with the documentation convention",
            )
        for diagram in MERMAID_RE.findall(text):
            if MERMAID_INLINE_STYLE_RE.search(diagram):
                add_finding(
                    findings,
                    "warning",
                    "mermaid-inline-style",
                    relative,
                    "Mermaid diagram contains local styling or theming that may fail across light and dark palettes",
                )
        metadata, complete = parse_frontmatter(text)
        if not complete:
            add_finding(findings, "warning", "frontmatter-missing", relative, "Missing or incomplete YAML frontmatter")
        else:
            if "status" in metadata:
                add_finding(
                    findings,
                    "error",
                    "material-status-collision",
                    relative,
                    "Use lifecycle for document state; Material for MkDocs reserves status for navigation badges",
                )
            for key in REQUIRED_METADATA:
                if key not in metadata:
                    add_finding(findings, "warning", "metadata-missing", relative, f"Missing metadata field: {key}")
            lifecycle = metadata.get("lifecycle", "")
            if lifecycle and lifecycle not in {"draft", "current", "needs-review", "archived"}:
                add_finding(
                    findings,
                    "warning",
                    "lifecycle-invalid",
                    relative,
                    f"Unknown lifecycle value: {lifecycle}",
                )
            if metadata.get("owner", "").lower() in {"", "null", "unassigned", "[team or role]"}:
                add_finding(findings, "info", "owner-unassigned", relative, "Documentation owner is not assigned")
            if metadata.get("last_reviewed", "").lower() in {"", "null"}:
                add_finding(findings, "info", "review-date-missing", relative, "Review date is not set")

        match = H1_RE.search(text)
        if not match:
            add_finding(findings, "warning", "title-missing", relative, "No level-one title found")
        else:
            title = re.sub(r"\s+", " ", match.group(1).strip()).casefold()
            titles.setdefault(title, []).append(relative)

        for raw_target in LINK_RE.findall(text):
            target = clean_link(raw_target)
            if target is None:
                continue
            resolved = resolve_markdown_target(path, target)
            if resolved is None:
                add_finding(findings, "error", "link-broken", relative, f"Broken local link: {target}")
            elif resolved in resolved_to_relative:
                graph[relative].add(resolved_to_relative[resolved])

    for title, paths in sorted(titles.items()):
        if len(paths) > 1 and not title.startswith("adr-nnn"):
            joined = ", ".join(path.as_posix() for path in paths)
            for path in paths:
                add_finding(findings, "warning", "title-duplicate", path, f"Duplicate title appears in: {joined}")

    for identifier, paths in sorted(adr_identifiers.items()):
        if len(paths) > 1:
            joined = ", ".join(path.as_posix() for path in paths)
            for path in paths:
                add_finding(findings, "error", "adr-id-duplicate", path, f"ADR identifier {identifier} also appears in: {joined}")

    if entrypoint not in graph:
        add_finding(findings, "error", "entrypoint-missing", entrypoint, "Documentation entrypoint does not exist")
    else:
        reachable: set[Path] = set()
        queue: deque[Path] = deque([entrypoint])
        while queue:
            current = queue.popleft()
            if current in reachable:
                continue
            reachable.add(current)
            queue.extend(graph[current] - reachable)
        for relative in sorted(set(graph) - reachable):
            if "archive" not in relative.parts and "templates" not in relative.parts:
                add_finding(findings, "warning", "page-orphaned", relative, f"Not reachable from {entrypoint.as_posix()}")

    repository_root = root.parent
    if (repository_root / "mkdocs.yml").is_file():
        inspect_mkdocs_navigation(repository_root / "mkdocs.yml", findings)
        for path in sorted(repository_root.glob("*.md")):
            if path.name not in {"README.md", "AGENTS.md"}:
                add_finding(
                    findings,
                    "warning",
                    "root-document-outside-tree",
                    Path("..") / path.name,
                    "Move narrative documentation into the authoritative docs tree or document an exception",
                )

    counts = Counter(finding["severity"] for finding in findings)
    summary = {
        "files": len(files),
        "errors": counts["error"],
        "warnings": counts["warning"],
        "info": counts["info"],
    }
    return findings, summary


def main() -> int:
    args = parse_args()
    root = args.docs_dir.expanduser().resolve()
    if not root.is_dir():
        print(f"error: documentation directory does not exist: {root}", file=sys.stderr)
        return 2
    if args.entrypoint:
        entrypoint = Path(args.entrypoint)
    elif (root / "index.md").is_file():
        entrypoint = Path("index.md")
    elif (root / "README.md").is_file():
        entrypoint = Path("README.md")
    else:
        entrypoint = Path("index.md")
    exclusions = tuple(Path(value) for value in (args.exclude or ["contributing/templates"]))
    findings, summary = inspect(root, entrypoint, exclusions)

    if entrypoint == Path("README.md"):
        add_finding(
            findings,
            "warning",
            "mkdocs-homepage-readme",
            entrypoint,
            "Use index.md as the MkDocs homepage",
        )
        counts = Counter(finding["severity"] for finding in findings)
        summary.update(errors=counts["error"], warnings=counts["warning"], info=counts["info"])

    if args.format == "json":
        print(json.dumps({"root": str(root), "entrypoint": entrypoint.as_posix(), "summary": summary, "findings": findings}, indent=2))
    else:
        for finding in findings:
            print(f"[{finding['severity'].upper()}] {finding['code']} {finding['path']}: {finding['message']}")
        print(
            f"Inspected {summary['files']} Markdown files: "
            f"{summary['errors']} errors, {summary['warnings']} warnings, {summary['info']} info"
        )

    if summary["errors"] or (args.strict and summary["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
