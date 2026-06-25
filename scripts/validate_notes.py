#!/usr/bin/env python3
"""Validate note metadata, structure, links between notes, and README coverage."""

from __future__ import annotations

import argparse
import json
import re
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
H3_RE = re.compile(r"^###\s+(.+)$", re.MULTILINE)

PAPER_TYPES = {
    "method", "system", "analysis", "diagnostic", "evaluation", "survey",
    "position", "benchmark", "dataset", "theory",
}
PAPER_STATUSES = {"preprint", "submitted", "accepted", "published", "withdrawn", "unknown"}
CODE_STATUSES = {
    "official_available", "unofficial_available", "claimed_public_link_missing",
    "not_found", "not_applicable", "unknown",
}
MODEL_STATUSES = {"official_available", "not_found", "not_applicable", "unknown"}
LEARNING_STAGES = {"training", "test-time", "deployment", "mixed", "not-applicable"}
PARAMETER_UPDATES = {"yes", "no", "auxiliary-only", "mixed", "not-applicable"}
CROSS_TASK_VALUES = {"yes", "no", "conditional", "not-applicable"}
URL_FIELDS = {
    "arxiv_url", "pdf_url", "html_url", "project_url", "code_url",
    "original_code_url", "resource_url", "model_url",
}
DATE_FIELDS = {
    "first_submitted", "last_revised", "accepted_at", "published_at",
    "last_verified", "created", "updated",
}
STRICT_REQUIRED = {
    "schema_version", "title", "short_title", "year", "note_type", "paper_type",
    "paper_status", "venue", "evolution_object", "learning_stage",
    "parameter_update", "cross_task", "authors", "topics", "tags",
    "related_notes", "created", "updated", "last_verified",
}
LEGACY_REQUIRED = {
    "title", "short_title", "year", "note_type", "paper_type", "status", "venue",
    "authors", "topics", "tags", "related_notes", "created", "updated",
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

    def add(self, severity: str, path: Path | str, code: str, message: str) -> None:
        self.findings.append(Finding(severity, str(path), code, message))

    def error(self, path: Path | str, code: str, message: str) -> None:
        self.add("error", path, code, message)

    def warning(self, path: Path | str, code: str, message: str) -> None:
        self.add("warning", path, code, message)

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
            candidate = root / item if item.startswith("notes/") else path.parent / item
            if not item.startswith("notes/"):
                reporter.warning(path, "legacy-related-path", f"use repo-root path in related_notes: {item}")
            if not candidate.exists():
                reporter.error(path, "missing-related-note", f"related note does not exist: {item}")


def _structure_finding(
    reporter: Reporter, path: Path, code: str, message: str, *, require_structure: bool
) -> None:
    if require_structure:
        reporter.error(path, code, message)
    else:
        reporter.warning(path, code, message)


def _validate_schema_1(
    path: Path,
    metadata: dict[str, Any],
    text: str,
    reporter: Reporter,
    *,
    require_structure: bool,
) -> None:
    for field in sorted(STRICT_REQUIRED - metadata.keys()):
        reporter.error(path, "missing-field", f"schema 1.0 requires metadata field: {field}")

    enum_checks = {
        "paper_type": PAPER_TYPES,
        "paper_status": PAPER_STATUSES,
        "code_status": CODE_STATUSES,
        "model_status": MODEL_STATUSES,
        "learning_stage": LEARNING_STAGES,
        "parameter_update": PARAMETER_UPDATES,
        "cross_task": CROSS_TASK_VALUES,
    }
    if metadata.get("schema_version") != SCHEMA_VERSION:
        reporter.error(path, "schema-version", f"schema_version must be {SCHEMA_VERSION!r}")
    if metadata.get("note_type") != "中文读书笔记":
        reporter.error(path, "note-type", "note_type must be '中文读书笔记'")
    for field, allowed in enum_checks.items():
        value = metadata.get(field)
        if field in {"code_status", "model_status"} and value is None:
            continue
        if value not in allowed:
            reporter.error(path, f"invalid-{field}", f"invalid {field}: {value!r}")

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
    for heading in ("30 秒读懂", "论文定位", "研究问题", "参考资料"):
        if not _has_heading(headings, heading):
            _structure_finding(
                reporter, path, "missing-section",
                f"note is missing section containing: {heading}",
                require_structure=require_structure,
            )

    paper_type = metadata.get("paper_type")
    if paper_type in {"method", "system"} and not _has_heading(headings, "进化机制卡片"):
        _structure_finding(
            reporter, path, "missing-mechanism-card",
            "method/system note requires a 进化机制卡片 section",
            require_structure=require_structure,
        )
    if paper_type in {"analysis", "diagnostic", "evaluation"} and not _has_heading(headings, "分析框架卡片"):
        _structure_finding(
            reporter, path, "missing-analysis-card",
            "analysis/diagnostic/evaluation note requires an 分析框架卡片 section",
            require_structure=require_structure,
        )


    for heading, code in (
        ("主张—证据—边界", "missing-evidence-layer"),
        ("论文外部信息", "missing-external-info"),
    ):
        if not _has_heading(headings, heading):
            _structure_finding(
                reporter, path, code,
                f"note is missing section containing: {heading}",
                require_structure=require_structure,
            )

    subheadings = H3_RE.findall(text)
    for heading, code in (
        ("我的判断", "missing-evidence-judgment"),
        ("其他可能解释", "missing-alternative-explanations"),
    ):
        if not _has_heading(subheadings, heading):
            _structure_finding(
                reporter, path, code,
                f"evidence layer is missing subsection containing: {heading}",
                require_structure=require_structure,
            )

    evidence_match = re.search(r"(?m)^## .*主张—证据—边界.*$", text)
    external_match = re.search(r"(?m)^## .*论文外部信息.*$", text)
    reference_matches = list(re.finditer(r"(?m)^## .*参考资料.*$", text))
    if evidence_match and external_match and reference_matches:
        if not evidence_match.start() < external_match.start() < reference_matches[-1].start():
            _structure_finding(
                reporter, path, "section-order",
                "expected evidence layer before external information and external information before references",
                require_structure=require_structure,
            )


def _validate_legacy(path: Path, metadata: dict[str, Any], reporter: Reporter, *, require_schema: bool) -> None:
    message = "metadata has no schema_version; migrate to schema 1.0"
    if require_schema:
        reporter.error(path, "legacy-schema", message)
    else:
        reporter.warning(path, "legacy-schema", message)
    for field in sorted(LEGACY_REQUIRED - metadata.keys()):
        reporter.error(path, "missing-legacy-field", f"legacy metadata is missing field: {field}")


def validate_repository(
    root: Path, *, require_schema: bool = False, require_structure: bool = False
) -> Reporter:
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
            _validate_schema_1(
                path, metadata, text, reporter, require_structure=require_structure
            )
        else:
            _validate_legacy(path, metadata, reporter, require_schema=require_schema)

    readme = root / "README.md"
    if not readme.is_file():
        reporter.error(readme, "missing-readme", "README.md does not exist")
        return reporter
    indexed = set(NOTE_LINK_RE.findall(readme.read_text(encoding="utf-8")))
    expected = {path.relative_to(root).as_posix() for path in note_files}
    for missing in sorted(expected - indexed):
        reporter.error(readme, "unindexed-note", f"note is not linked from README: {missing}")
    for stale in sorted(indexed - expected):
        reporter.error(readme, "stale-note-link", f"README links to missing note: {stale}")
    return reporter


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--require-schema", action="store_true", help="Reject legacy metadata")
    parser.add_argument("--require-structure", action="store_true", help="Require the new note sections")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    reporter = validate_repository(
        args.root.resolve(),
        require_schema=args.require_schema,
        require_structure=args.require_structure,
    )
    if args.json:
        print(json.dumps({
            "errors": reporter.errors,
            "warnings": reporter.warnings,
            "strict": args.strict,
            "findings": [asdict(item) for item in reporter.findings],
        }, ensure_ascii=False, indent=2))
    else:
        for item in reporter.findings:
            print(f"{item.severity.upper()} [{item.code}] {item.path}: {item.message}")
        print(f"Summary: {reporter.errors} error(s), {reporter.warnings} warning(s)")
    return 1 if reporter.errors or (args.strict and reporter.warnings) else 0


if __name__ == "__main__":
    raise SystemExit(_main())
