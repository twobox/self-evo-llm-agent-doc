#!/usr/bin/env python3
"""Check local Markdown links without making network requests."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

FENCE_RE = re.compile(r"```.*?```|~~~~.*?~~~~", re.DOTALL)
LINK_RE = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")


@dataclass(frozen=True)
class LinkIssue:
    path: Path
    target: str
    message: str


def _strip_code_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def _clean_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith("data:"):
        target = target.split(" ", 1)[0]
    return target


def _iter_markdown_files(root: Path, include_docs: bool) -> list[Path]:
    paths: list[Path] = []
    readme = root / "README.md"
    if readme.is_file():
        paths.append(readme)
    for directory in ("notes", "surveys"):
        base = root / directory
        if base.is_dir():
            paths.extend(sorted(base.rglob("*.md")))
    if include_docs and (root / "docs").is_dir():
        paths.extend(sorted((root / "docs").rglob("*.md")))
    return paths


def check_links(root: Path, *, include_docs: bool = False) -> list[LinkIssue]:
    issues: list[LinkIssue] = []
    for path in _iter_markdown_files(root, include_docs):
        text = _strip_code_fences(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            target = _clean_target(match.group("target"))
            if not target or target.startswith("#"):
                continue
            parsed = urlparse(target)
            if parsed.scheme in {"http", "https", "mailto"}:
                if parsed.scheme in {"http", "https"} and not parsed.netloc:
                    issues.append(LinkIssue(path, target, "external URL has no host"))
                continue
            if parsed.scheme:
                issues.append(LinkIssue(path, target, f"unsupported link scheme: {parsed.scheme}"))
                continue

            relative = unquote(parsed.path)
            if not relative:
                continue
            if "<" in relative or ">" in relative:
                continue
            candidate = (path.parent / relative).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                issues.append(LinkIssue(path, target, "local link escapes repository root"))
                continue
            if not candidate.exists():
                issues.append(LinkIssue(path, target, "local link target does not exist"))
    return issues


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--include-docs", action="store_true", help="Also scan docs/*.md")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    issues = check_links(root, include_docs=args.include_docs)
    for issue in issues:
        print(f"ERROR {issue.path}: {issue.target}: {issue.message}")
    print(f"Summary: {len(issues)} broken local link(s)")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(_main())
