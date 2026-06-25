#!/usr/bin/env python3
"""Validate note image references, localization manifest, licenses, and hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

IMAGE_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)"
)
ALLOWED_LICENSES = {"Apache-2.0", "MIT", "CC BY 4.0", "CC BY-NC-ND 4.0"}
DEFERRED_LICENSE = "arXiv nonexclusive distribution license"


def _load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing JSON file: {path}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read JSON file {path}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"JSON root must be an object: {path}")
        return {}
    return payload


def _image_kind(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.lstrip().startswith(b"<svg") or b"<svg" in data[:512]:
        return "svg"
    return None


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    notes_dir = root / "notes"
    assets_dir = root / "assets" / "images"
    manifest_path = assets_dir / "manifest.json"
    inventory_path = root / "maintenance" / "image-inventory.json"
    errors: list[str] = []

    manifest = _load_json(manifest_path, errors)
    inventory = _load_json(inventory_path, errors)
    manifest_images = manifest.get("images", [])
    inventory_images = inventory.get("images", [])
    if not isinstance(manifest_images, list):
        errors.append("assets/images/manifest.json: images must be a list")
        manifest_images = []
    if not isinstance(inventory_images, list):
        errors.append("maintenance/image-inventory.json: images must be a list")
        inventory_images = []

    manifest_by_path: dict[str, dict[str, Any]] = {}
    manifest_by_source: dict[tuple[str, str], dict[str, Any]] = {}
    for item in manifest_images:
        if not isinstance(item, dict):
            errors.append("manifest image entry must be an object")
            continue
        local_path = str(item.get("local_path", ""))
        note = str(item.get("note", ""))
        original_url = str(item.get("original_url", ""))
        if not local_path or local_path in manifest_by_path:
            errors.append(f"manifest has missing or duplicate local_path: {local_path!r}")
            continue
        manifest_by_path[local_path] = item
        manifest_by_source[(note, original_url)] = item

        license_name = str(item.get("license", ""))
        if license_name not in ALLOWED_LICENSES:
            errors.append(f"unsupported localized-image license for {local_path}: {license_name!r}")
        if not str(item.get("license_url", "")).startswith("https://"):
            errors.append(f"missing https license_url for {local_path}")
        if not str(item.get("attribution", "")).strip():
            errors.append(f"missing attribution for {local_path}")
        if item.get("modified") is not False:
            errors.append(f"localized image must declare modified=false: {local_path}")

        file_path = root / local_path
        if not file_path.is_file():
            errors.append(f"manifest file does not exist: {local_path}")
            continue
        data = file_path.read_bytes()
        actual_sha = hashlib.sha256(data).hexdigest()
        if actual_sha != item.get("sha256"):
            errors.append(f"SHA-256 mismatch: {local_path}")
        if len(data) != item.get("size_bytes"):
            errors.append(f"size mismatch: {local_path}")
        kind = _image_kind(data)
        expected = file_path.suffix.lower().lstrip(".")
        if expected == "jpeg":
            expected = "jpg"
        if kind != expected:
            errors.append(f"image type mismatch for {local_path}: extension={expected}, content={kind}")

    inventory_by_source: dict[tuple[str, str], dict[str, Any]] = {}
    for item in inventory_images:
        if not isinstance(item, dict):
            errors.append("inventory image entry must be an object")
            continue
        note = str(item.get("note", ""))
        original_url = str(item.get("original_url", ""))
        key = (note, original_url)
        if key in inventory_by_source:
            errors.append(f"duplicate inventory source: {note} {original_url}")
        inventory_by_source[key] = item

    referenced_local: set[str] = set()
    referenced_manifest_sources: set[tuple[str, str]] = set()
    note_image_count = 0
    for note_path in sorted(notes_dir.glob("*.md")):
        note_rel = note_path.relative_to(root).as_posix()
        text = note_path.read_text(encoding="utf-8")
        for match in IMAGE_RE.finditer(text):
            note_image_count += 1
            target = match.group(2)
            if target.startswith(("http://", "https://")):
                item = inventory_by_source.get((note_rel, target))
                if item is None:
                    errors.append(f"external image is not inventoried: {note_rel} -> {target}")
                    continue
                if item.get("status") != "deferred-license":
                    errors.append(f"external image must be deferred-license: {note_rel} -> {target}")
                if item.get("license") != DEFERRED_LICENSE:
                    errors.append(f"external image has unexpected license status: {note_rel} -> {target}")
                if not str(item.get("reason", "")).strip():
                    errors.append(f"external image needs a deferral reason: {note_rel} -> {target}")
                continue

            resolved = (note_path.parent / target).resolve()
            try:
                local_path = resolved.relative_to(root).as_posix()
            except ValueError:
                errors.append(f"image path escapes repository: {note_rel} -> {target}")
                continue
            if not local_path.startswith("assets/images/"):
                errors.append(f"local note image must live under assets/images: {note_rel} -> {target}")
                continue
            item = manifest_by_path.get(local_path)
            if item is None:
                errors.append(f"local note image missing from manifest: {note_rel} -> {local_path}")
                continue
            if item.get("note") != note_rel:
                errors.append(f"manifest note mismatch for {local_path}: {item.get('note')} != {note_rel}")
            referenced_local.add(local_path)
            referenced_manifest_sources.add((note_rel, str(item.get("original_url", ""))))

    for local_path, item in manifest_by_path.items():
        if local_path not in referenced_local:
            errors.append(f"manifest image is not referenced by a note: {local_path}")
        key = (str(item.get("note", "")), str(item.get("original_url", "")))
        inventory_item = inventory_by_source.get(key)
        if inventory_item is None:
            errors.append(f"localized image missing from inventory: {key[0]} -> {key[1]}")
        elif inventory_item.get("status") != "localized":
            errors.append(f"localized inventory entry has wrong status: {key[0]} -> {key[1]}")

    tracked_files = set(manifest_by_path)
    actual_files = {
        path.relative_to(root).as_posix()
        for path in assets_dir.rglob("*")
        if path.is_file() and path.name not in {"README.md", "manifest.json"}
    } if assets_dir.is_dir() else set()
    for extra in sorted(actual_files - tracked_files):
        errors.append(f"untracked image asset: {extra}")
    for missing in sorted(tracked_files - actual_files):
        errors.append(f"manifest points to missing asset: {missing}")

    inventory_total = inventory.get("total_images")
    if inventory_total != note_image_count:
        errors.append(f"inventory total_images mismatch: {inventory_total} != {note_image_count}")
    if inventory.get("localized_images") != len(referenced_local):
        errors.append(
            f"inventory localized_images mismatch: {inventory.get('localized_images')} != {len(referenced_local)}"
        )
    external_count = note_image_count - len(referenced_local)
    if inventory.get("external_images") != external_count:
        errors.append(
            f"inventory external_images mismatch: {inventory.get('external_images')} != {external_count}"
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors = check_repository(args.root)
    if args.json:
        print(json.dumps({"errors": len(errors), "findings": errors}, ensure_ascii=False, indent=2))
    else:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Summary: {len(errors)} image error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
