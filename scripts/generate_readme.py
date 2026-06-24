#!/usr/bin/env python3
"""Generate deterministic README note-index tables from note metadata."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from parse_metadata import MetadataError, find_note_files, parse_metadata_file

BEGIN = "<!-- BEGIN GENERATED NOTE INDEX -->"
END = "<!-- END GENERATED NOTE INDEX -->"
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)


def _display_type(metadata: dict[str, Any]) -> str:
    return str(metadata.get("paper_type") or "unknown")


def _display_topics(metadata: dict[str, Any], limit: int = 5) -> str:
    topics = metadata.get("topics")
    if not isinstance(topics, list):
        return ""
    values = [str(item) for item in topics if item]
    suffix = "、…" if len(values) > limit else ""
    return "、".join(values[:limit]) + suffix


def _display_status(metadata: dict[str, Any]) -> str:
    venue = str(metadata.get("venue") or "").strip()
    track = str(metadata.get("venue_track") or "").strip()
    status = str(metadata.get("paper_status") or metadata.get("status") or "").strip()
    if metadata.get("schema_version") == "1.0":
        parts = [part for part in (venue, track, status) if part]
        return " · ".join(parts)
    return venue or status or "unknown"


def _is_boundary(metadata: dict[str, Any]) -> bool:
    tags = metadata.get("tags")
    topics = metadata.get("topics")
    values: list[str] = []
    if isinstance(tags, list):
        values.extend(str(item).casefold() for item in tags)
    if isinstance(topics, list):
        values.extend(str(item).casefold() for item in topics)
    joined = " ".join(values)
    return "boundary-study" in joined or "边界" in joined


def _table(rows: list[tuple[Path, dict[str, Any]]], root: Path) -> str:
    lines = [
        "| 序号 | 论文 | 笔记 | 类型 | 主题 | Venue / 状态 |",
        "|---:|---|---|---|---|---|",
    ]
    for index, (path, metadata) in enumerate(rows, start=1):
        rel = path.relative_to(root).as_posix()
        title = str(metadata.get("title") or path.stem)
        lines.append(
            f"| {index} | {title} | [{rel}]({rel}) | {_display_type(metadata)} | "
            f"{_display_topics(metadata)} | {_display_status(metadata)} |"
        )
    return "\n".join(lines)


def generate_index(root: Path) -> str:
    entries: list[tuple[Path, dict[str, Any]]] = []
    for path in find_note_files(root):
        entries.append((path, parse_metadata_file(path).metadata))

    main = [(path, meta) for path, meta in entries if not _is_boundary(meta)]
    boundary = [(path, meta) for path, meta in entries if _is_boundary(meta)]
    main.sort(key=lambda item: (-(item[1].get("year") or 0), str(item[1].get("title") or "")))
    boundary.sort(key=lambda item: (-(item[1].get("year") or 0), str(item[1].get("title") or "")))

    parts = [BEGIN, "## 笔记目录", "", _table(main, root)]
    if boundary:
        parts.extend(["", "## 相关基础与边界研究", "", _table(boundary, root)])
    parts.append(END)
    return "\n".join(parts)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="Repository root")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check the marked README block")
    mode.add_argument("--write", action="store_true", help="Replace the marked README block")
    parser.add_argument("--output", type=Path, help="Write generated Markdown to a separate file")
    parser.add_argument(
        "--require-markers",
        action="store_true",
        help="Fail instead of warning when README has no generated markers",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    try:
        generated = generate_index(root)
    except (OSError, MetadataError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(generated + "\n", encoding="utf-8")

    readme = root / "README.md"
    if args.check or args.write:
        if not readme.is_file():
            print("ERROR: README.md does not exist", file=sys.stderr)
            return 1
        current = readme.read_text(encoding="utf-8")
        match = BLOCK_RE.search(current)
        if not match:
            message = "README has no generated note-index markers; preview only"
            if args.require_markers:
                print(f"ERROR: {message}", file=sys.stderr)
                return 1
            print(f"WARNING: {message}")
            if not args.output:
                print(generated)
            return 0
        if args.check:
            actual = match.group(0).strip()
            if actual != generated.strip():
                print("ERROR: README generated note index is stale", file=sys.stderr)
                return 1
            print("README generated note index is up to date")
            return 0
        updated = BLOCK_RE.sub(generated, current, count=1)
        readme.write_text(updated, encoding="utf-8")
        print("Updated README generated note index")
        return 0

    if not args.output:
        print(generated)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
