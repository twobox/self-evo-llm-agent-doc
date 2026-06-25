#!/usr/bin/env python3
"""Inventory local and external Markdown images referenced by notes."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
OUT_DIR = ROOT / "maintenance"
MANIFEST_PATH = ROOT / "assets" / "images" / "manifest.json"
INVENTORY_PATH = OUT_DIR / "image-inventory.json"
IMAGE_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)"
)


def source_kind(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host == "arxiv.org":
        return "arxiv-html"
    if host in {"raw.githubusercontent.com", "github.com"}:
        return "official-github"
    if host.endswith("github.io"):
        return "project-site"
    return "external-site"


def load_json(path: Path, default: object) -> object:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def record_id(note: str, original_url: str) -> str:
    return hashlib.sha256(f"{note}\n{original_url}".encode()).hexdigest()[:12]


def main() -> None:
    manifest_payload = load_json(MANIFEST_PATH, {"images": []})
    manifest_images = manifest_payload.get("images", []) if isinstance(manifest_payload, dict) else []
    manifest_by_path = {
        str(item["local_path"]): item
        for item in manifest_images
        if isinstance(item, dict) and item.get("local_path")
    }

    previous_payload = load_json(INVENTORY_PATH, {"images": []})
    previous_images = previous_payload.get("images", []) if isinstance(previous_payload, dict) else []
    previous_by_source = {
        (str(item.get("note", "")), str(item.get("original_url") or item.get("url") or "")): item
        for item in previous_images
        if isinstance(item, dict)
    }

    records: list[dict[str, object]] = []
    for note in sorted(NOTES.glob("*.md")):
        note_rel = note.relative_to(ROOT).as_posix()
        text = note.read_text(encoding="utf-8")
        for index, match in enumerate(IMAGE_RE.finditer(text), start=1):
            alt, target = match.groups()
            line = text.count("\n", 0, match.start()) + 1
            if target.startswith(("http://", "https://")):
                previous = previous_by_source.get((note_rel, target), {})
                status = str(previous.get("status", "external-unreviewed"))
                if status == "external":
                    status = "external-unreviewed"
                record = {
                    "id": str(previous.get("id") or record_id(note_rel, target)),
                    "note": note_rel,
                    "line": line,
                    "ordinal_in_note": index,
                    "alt": alt,
                    "reference": target,
                    "original_url": target,
                    "local_path": "",
                    "host": urlparse(target).netloc,
                    "source_kind": str(previous.get("source_kind") or source_kind(target)),
                    "status": status,
                    "license": str(previous.get("license", "")),
                    "license_url": str(previous.get("license_url", "")),
                    "reason": str(previous.get("reason", "license review required")),
                }
            else:
                resolved = (note.parent / target).resolve()
                try:
                    local_path = resolved.relative_to(ROOT).as_posix()
                except ValueError:
                    local_path = target
                manifest = manifest_by_path.get(local_path, {})
                original_url = str(manifest.get("original_url", ""))
                record = {
                    "id": str(manifest.get("id") or record_id(note_rel, original_url or local_path)),
                    "note": note_rel,
                    "line": line,
                    "ordinal_in_note": index,
                    "alt": alt,
                    "reference": target,
                    "original_url": original_url,
                    "local_path": local_path,
                    "host": urlparse(original_url).netloc if original_url else "",
                    "source_kind": str(manifest.get("source_kind", "local-untracked")),
                    "status": "localized" if manifest else "local-untracked",
                    "license": str(manifest.get("license", "")),
                    "license_url": str(manifest.get("license_url", "")),
                    "reason": "",
                }
            records.append(record)

    by_source: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_note: dict[str, int] = {}
    for record in records:
        source = str(record["source_kind"])
        status = str(record["status"])
        note = str(record["note"])
        by_source[source] = by_source.get(source, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        by_note[note] = by_note.get(note, 0) + 1

    localized = sum(record["status"] == "localized" for record in records)
    external = sum(str(record["reference"]).startswith(("http://", "https://")) for record in records)
    payload = {
        "schema_version": "2.0",
        "generated_at": "2026-06-25",
        "total_images": len(records),
        "localized_images": localized,
        "external_images": external,
        "by_source_kind": by_source,
        "by_status": by_status,
        "by_note": by_note,
        "images": records,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = [
        "# 笔记图片资源清单",
        "",
        "> 本清单由 `scripts/inventory_note_images.py` 生成，同时记录已本地化图片和因许可原因保留的外链图片。",
        "",
        f"- 图片总数：**{len(records)}**",
        f"- 已本地化：**{localized}**",
        f"- 保留外链：**{external}**",
        f"- 涉及笔记数：**{len(by_note)}**",
        "",
        "| ID | 笔记 | 行号 | 图片说明 | 状态 | 许可 | 本地路径 / 延后原因 | 原始地址 |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for record in records:
        alt = str(record["alt"]).replace("|", "\\|")
        location = str(record["local_path"] or record["reason"]).replace("|", "\\|")
        original = f"<{record['original_url']}>" if record["original_url"] else ""
        rows.append(
            f"| `{record['id']}` | `{record['note']}` | {record['line']} | {alt} | "
            f"{record['status']} | {record['license']} | `{location}` | {original} |"
        )
    rows.extend([
        "",
        "## 本地化规则",
        "",
        "1. 只迁移笔记正文已经引用、来源明确且许可允许再分发的论文或项目图。",
        "2. 本地文件保留原始 URL、Figure 信息、许可、署名、SHA-256 和字节数。",
        "3. CC BY-NC-ND 图片必须保持原始字节，不裁剪、不重编码、不叠加标记。",
        "4. 仅有 arXiv nonexclusive distribution license 的论文图默认保留外链。",
        "5. 本地化后笔记使用 `../assets/images/<note-slug>/<file>` 相对路径。",
        "",
    ])
    (OUT_DIR / "image-inventory.md").write_text("\n".join(rows), encoding="utf-8")
    print(f"Inventoried {len(records)} images: {localized} localized, {external} external")


if __name__ == "__main__":
    main()
