#!/usr/bin/env python3
"""Validate note metadata, required sections, and README index coverage."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from parse_metadata import MetadataError, find_note_files, parse_metadata_file

SCHEMA_VERSION = "1.0"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NOTE_LINK_RE = re.compile(r"\((notes/[^)\s]+\.md)(?:#[^)]+)?\)")
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)

PAPER_TYPES = {
    "method",
    "system",
    "analysis",
    "diagnostic",
    "evaluation",
    "survey",
    "position",
    "benchmark",
    "dataset",
    "theory",
}
PAPER_STATUSES = {"preprint", "submitted", "accepted", "published", "withdrawn", "unknown"}
CODE_STATUSES = {
    "official_available",
    "unofficial_available",
    "claimed_public_link_missing",
    "not_found",
    "not_applicable",
    "unknown",
}
MODEL_STATUSES = {"official_available", "not_found", "not_applicable", "unknown"}
URL_FIELDS = {
    "arxiv_url",
    "pdf_url",
    "html_url",
    "project_url",
    "code_url",
    "original_code_url",
    "resource_url",
    "model_url",
}
DATE_FIELDS = {
    "first_submitted",
    "last_revised",
    "accepted_at",
    "published_at",
    "last_verified",
    "created",
    "updated",
}
STRICT_REQUIRED = {
    "schema_version",
    "title",
    "short_title",
    "year",
    "note_type",
    "paper_type",
    "paper_status",
    "venue",
    "authors",
    "topics",
    "tags",
    "related_notes",
    "created",
    "updated",
    "last_verified",
}
LEGACY_REQUIRED = {
    "title",
    "short_title",
    "year",
    "note_type",
    "paper_type",
    "status",
    "venue",
    "authors",
    "topics",
    "tags",
    "related_notes",
    "created",
    "updated",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    code: str
    message: str


class Reporter:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def error(self, path: Path | str, code: str, message: str) -> None:
        self.findings.append(Finding("error", str(path), code, message))

    def warning(self, path: Path | str, code: str, message: str) -> None:
        self.findings.append(Finding("warning", str(path), code, message))

    @property
    def errors(self) -> int:
        return sum(item.severity == "error" for item in self.findings)

    @property
    def warnings(self) -> int:
        return sum(item.severity == "warning" for item in self.findings)


def _is_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_list_of_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _normalized_heading(value: str) -> str:
    value = value.strip().replace("《", "").replace("》", "")
    value = re.sub(r"\s*读书笔记\s*$", "", value)
    return re.sub(r"\s+", " ", value).strip().casefold()


def _has_heading(headings: Iterable[str], keyword: str) -> bool:
    return any(keyword.casefold() in heading.casefold() for heading in headings)


def _validate_common(path: Path, metadata: dict[str, Any], text: str, reporter: Reporter) -> None:
    h1 = H1_RE.search(text)
    if not h1:
        reporter.error(path, "missing-h1", "note must contain a level-1 title")
    elif isinstance(metadata.get("title"), str):
        expected = _normalized_heading(metadata["title"])
        actual = _normalized_heading(h1.group(1))
        if expected not in actual and actual not in expected:
            reporter.warning(path, "title-mismatch", "metadata title and H1 appear inconsistent")

    for field in ("authors", "topics", "tags", "related_notes"):
        if field in metadata and not _is_list_of_strings(metadata[field]):
            reporter.error(path, "invalid-list", f"{field} must be a list of strings")

    root = path.parent.parent
    related = metadata.get("related_notes")
    if isinstance(related, list):
        for item in related:
            if not isinstance(item, str):
                continue
            if not item.startswith("notes/"):
                reporter.warning(path, "legacy-related-path", f"related_notes should use repo-root path: {item}")
                candidate = path.parent / item
            else:
                candidate = root / item
            if not candidate.exists():
                reporter.error(path, "missing-related-note", f"related note does not exist: {item}")


def _validate_schema_1(path: Path, metadata: dict[str, Any], text: str, reporter: Reporter) -> None:
    missing = sorted(field for field in STRICT_REQUIRED if field not in metadata)
    for field in missing:
        reporter.error(path, "missing-field", f"schema 1.0 requires metadata field: {field}")

    if metadata.get("schema_version") != SCHEMA_VERSION:
        reporter.error(path, "schema-version", f"schema_version must be {SCHEMA_VERSION!r}")
    if metadata.get("note_type") != "中文读书笔记":
        reporter.error(path, "note-type", "note_type must be '中文读书笔记'")
    if metadata.get("paper_type") not in PAPER_TYPES:
        reporter.error(path, "paper-type", f"invalid paper_type: {metadata.get('paper_type')!r}")
    if metadata.get("paper_status") not in PAPER_STATUSES:
        reporter.error(path, "paper-status", f"invalid paper_status: {metadata.get('paper_status')!r}")
    if "code_status" in metadata and metadata.get("code_status") not in CODE_STATUSES:
        reporter.error(path, "code-status", f"invalid code_status: {metadata.get('code_status')!r}")
    if "model_status" in metadata and metadata.get("model_status") not in MODEL_STATUSES:
        reporter.error(path, "model-status", f"invalid model_status: {metadata.get('model_status')!r}")

    year = metadata.get("year")
    if not isinstance(year, int) or not 1900 <= year <= 2100:
        reporter.error(path, "year", "year must be an integer between 1900 and 2100")

    for field in URL_FIELDS:
        value = metadata.get(field)
        if value in {None, ""}:
            continue
        if not _is_url(value):
            reporter.error(path, "invalid-url", f"{field} must be an http(s) URL or empty string")

    for field in DATE_FIELDS:
        value = metadata.get(field)
        if value in {None, ""}:
            continue
        if not isinstance(value, str) or not DATE_RE.fullmatch(value):
            reporter.error(path, "invalid-date", f"{field} must use YYYY-MM-DD or empty string")

    tags = metadata.get("tags")
    if isinstance(tags, list):
        for tag in tags:
            if isinstance(tag, str) and not TAG_RE.fullmatch(tag):
                reporter.error(path, "invalid-tag", f"tag must be lowercase kebab-case: {tag!r}")

    headings = H2_RE.findall(text)
    required_headings = ["30 秒读懂", "论文定位", "研究问题", "参考资料"]
    for heading in required_headings:
        if not _has_heading(headings, heading):
            reporter.error(path, "missing-section", f"schema 1.0 note is missing section containing: {heading}")

    paper_type = metadata.get("paper_type")
    if paper_type in {"method", "system"} and not _has_heading(headings, "进化机制卡片"):
        reporter.error(path, "missing-mechanism-card", "method/system note requires a 进化机制卡片 section")
    if paper_type in {"analysis", "diagnostic", "evaluation"} and not _has_heading(headings, "分析框架卡片"):
        reporter.error(path, "missing-analysis-card", "analysis/diagnostic/evaluation note requires an 分析框架卡片 section")


def _validate_legacy(path: Path, metadata: dict[str, Any], reporter: Reporter) -> None:
    reporter.warning(path, "legacy-schema", "metadata has no schema_version; applying transitional checks")
    for field in sorted(LEGACY_REQUIRED):
        if field not in metadata:
            reporter.error(path, "missing-legacy-field", f"legacy metadata is missing field: {field}")

    for field in URL_FIELDS:
        if field not in metadata:
            continue
        value = metadata.get(field)
        if value in {None, ""}:
            continue
        if not _is_url(value):
            reporter.warning(path, "legacy-invalid-url", f"{field} contains non-URL text and must be migrated")

    tags = metadata.get("tags")
    if isinstance(tags, list):
        for tag in tags:
            if isinstance(tag, str) and not TAG_RE.fullmatch(tag):
                reporter.warning(path, "legacy-tag", f"tag is not lowercase kebab-case: {tag!r}")


def validate_repository(root: Path) -> Reporter:
    reporter = Reporter()
    try:
        note_files = find_note_files(root)
    except MetadataError as exc:
        reporter.error(root, "notes-directory", str(exc))
        return reporter

    for path in note_files:
        try:
            parsed = parse_metadata_file(path)
        except (OSError, MetadataError) as exc:
            reporter.error(path, "metadata-parse", str(exc))
            continue
        text = path.read_text(encoding="utf-8")
        metadata = parsed.metadata
        _validate_common(path, metadata, text, reporter)
        if metadata.get("schema_version") == SCHEMA_VERSION:
            _validate_schema_1(path, metadata, text, reporter)
        else:
            _validate_legacy(path, metadata, reporter)

    readme = root / "README.md"
    if not readme.is_file():
        reporter.error(readme, "missing-readme", "README.md does not exist")
        return reporter

    readme_text = readme.read_text(encoding="utf-8")
    indexed = set(NOTE_LINK_RE.findall(readme_text))
    expected = {path.relative_to(root).as_posix() for path in note_files}
    for missing in sorted(expected - indexed):
        reporter.error(readme, "unindexed-note", f"note is not linked from README: {missing}")
    for stale in sorted(indexed - expected):
        reporter.error(readme, "stale-note-link", f"README links to missing note: {stale}")

    return reporter


def _print_text(reporter: Reporter, *, strict_warnings: bool) -> None:
    for item in reporter.findings:
        label = item.severity.upper()
        print(f"{label} [{item.code}] {item.path}: {item.message}")
    effective_errors = reporter.errors + (reporter.warnings if strict_warnings else 0)
    print(
        f"Summary: {reporter.errors} error(s), {reporter.warnings} warning(s), "
        f"effective failures={effective_errors}"
    )


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    reporter = validate_repository(args.root.resolve())
    if args.json:
        print(
            json.dumps(
                {
                    "errors": reporter.errors,
                    "warnings": reporter.warnings,
                    "strict": args.strict,
                    "findings": [asdict(item) for item in reporter.findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        _print_text(reporter, strict_warnings=args.strict)
    return 1 if reporter.errors or (args.strict and reporter.warnings) else 0


if __name__ == "__main__":
    raise SystemExit(_main())
