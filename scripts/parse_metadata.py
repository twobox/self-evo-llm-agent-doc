#!/usr/bin/env python3
"""Parse the repository's HTML-comment metadata blocks without external deps."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

COMMENT_RE = re.compile(r"\A\s*<!--(?P<body>.*?)-->", re.DOTALL)
KEY_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_]*):(?:\s*(?P<value>.*))?$")
LIST_RE = re.compile(r"^(?P<indent>\s*)-\s*(?P<value>.*)$")


class MetadataError(ValueError):
    """Raised when a note's metadata block cannot be parsed safely."""


@dataclass(frozen=True)
class ParsedMetadata:
    path: Path
    metadata: dict[str, Any]
    raw_comment: str


def _parse_scalar(raw: str, *, line_no: int) -> Any:
    value = raw.strip()
    if value == "":
        return None
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith(("'", '"')):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise MetadataError(f"line {line_no}: invalid quoted scalar: {value}") from exc
        if not isinstance(parsed, str):
            raise MetadataError(f"line {line_no}: quoted metadata values must be strings")
        return parsed
    # Legacy files occasionally contain unquoted values. Preserve them as strings.
    return value


def parse_metadata_text(text: str, *, source: str = "<memory>") -> dict[str, Any]:
    match = COMMENT_RE.search(text)
    if not match:
        raise MetadataError(f"{source}: missing leading HTML metadata comment")

    raw = match.group("body")
    lines = raw.splitlines()
    metadata_idx = None
    metadata_indent = 0
    for idx, line in enumerate(lines):
        key_match = KEY_RE.match(line)
        if key_match and key_match.group("key") == "metadata":
            metadata_idx = idx
            metadata_indent = len(key_match.group("indent"))
            if (key_match.group("value") or "").strip():
                raise MetadataError(f"{source}: metadata root must not have an inline value")
            break
    if metadata_idx is None:
        raise MetadataError(f"{source}: leading HTML comment does not contain metadata:")

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_key_indent: int | None = None

    for offset, line in enumerate(lines[metadata_idx + 1 :], start=metadata_idx + 2):
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= metadata_indent:
            break

        list_match = LIST_RE.match(line)
        if list_match:
            if current_list_key is None or current_key_indent is None:
                raise MetadataError(f"{source}: line {offset}: list item without a list key")
            if indent <= current_key_indent:
                raise MetadataError(f"{source}: line {offset}: list item indentation is invalid")
            result[current_list_key].append(_parse_scalar(list_match.group("value"), line_no=offset))
            continue

        key_match = KEY_RE.match(line)
        if not key_match:
            raise MetadataError(f"{source}: line {offset}: unsupported metadata syntax: {line.strip()}")

        key_indent = len(key_match.group("indent"))
        if key_indent != metadata_indent + 2:
            raise MetadataError(
                f"{source}: line {offset}: metadata keys must be indented exactly two spaces"
            )
        key = key_match.group("key")
        if key in result:
            raise MetadataError(f"{source}: line {offset}: duplicate metadata key: {key}")
        raw_value = key_match.group("value") or ""
        if raw_value.strip() == "":
            result[key] = []
            current_list_key = key
            current_key_indent = key_indent
        else:
            result[key] = _parse_scalar(raw_value, line_no=offset)
            current_list_key = None
            current_key_indent = None

    if not result:
        raise MetadataError(f"{source}: metadata block is empty")
    return result


def parse_metadata_file(path: Path) -> ParsedMetadata:
    text = path.read_text(encoding="utf-8")
    match = COMMENT_RE.search(text)
    if not match:
        raise MetadataError(f"{path}: missing leading HTML metadata comment")
    metadata = parse_metadata_text(text, source=str(path))
    return ParsedMetadata(path=path, metadata=metadata, raw_comment=match.group("body"))


def find_note_files(root: Path) -> list[Path]:
    notes_dir = root / "notes"
    if not notes_dir.is_dir():
        raise MetadataError(f"{root}: notes/ directory does not exist")
    return sorted(path for path in notes_dir.glob("*.md") if path.is_file())


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="A note file or repository root")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args(argv)

    try:
        if args.path.is_dir():
            payload = {
                str(path): parse_metadata_file(path).metadata
                for path in find_note_files(args.path)
            }
        else:
            payload = parse_metadata_file(args.path).metadata
    except (OSError, MetadataError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
