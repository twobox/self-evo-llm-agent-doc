#!/usr/bin/env python3
"""Inventory external Markdown images referenced by notes."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
OUT_DIR = ROOT / "maintenance"
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")


def source_kind(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host == "arxiv.org":
        return "arxiv-html"
    if host in {"raw.githubusercontent.com", "github.com"}:
        return "official-github"
    if host.endswith("github.io"):
        return "project-site"
    return "external-site"


def suggested_action(kind: str) -> str:
    if kind in {"arxiv-html", "official-github"}:
        return "candidate-for-localization"
    return "review-license-before-localization"


def main() -> None:
    records: list[dict[str, object]] = []
    for note in sorted(NOTES.glob("*.md")):
        text = note.read_text(encoding="utf-8")
        for index, match in enumerate(IMAGE_RE.finditer(text), start=1):
            alt, url = match.groups()
            line = text.count("\n", 0, match.start()) + 1
            kind = source_kind(url)
            records.append({
                "id": hashlib.sha256(f"{note.name}\n{url}".encode()).hexdigest()[:12],
                "note": note.relative_to(ROOT).as_posix(),
                "line": line,
                "ordinal_in_note": index,
                "alt": alt,
                "url": url,
                "host": urlparse(url).netloc,
                "source_kind": kind,
                "suggested_action": suggested_action(kind),
                "status": "external",
            })

    summary: dict[str, int] = {}
    by_note: dict[str, int] = {}
    for record in records:
        summary[str(record["source_kind"])] = summary.get(str(record["source_kind"]), 0) + 1
        by_note[str(record["note"])] = by_note.get(str(record["note"]), 0) + 1

    payload = {
        "schema_version": "1.0",
        "generated_at": "2026-06-25",
        "total_external_images": len(records),
        "by_source_kind": summary,
        "by_note": by_note,
        "images": records,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "image-inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = [
        "# 笔记图片资源清单",
        "",
        "> 本清单由 `scripts/inventory_note_images.py` 生成。它只记录外链图片，不代表已经确认转载许可。",
        "",
        f"- 外链图片总数：**{len(records)}**",
        f"- 涉及笔记数：**{len(by_note)}**",
        "",
        "| ID | 笔记 | 行号 | 图片说明 | 来源类型 | 原始地址 | 建议 |",
        "|---|---|---:|---|---|---|---|",
    ]
    for record in records:
        alt = str(record["alt"]).replace("|", "\\|")
        rows.append(
            f"| `{record['id']}` | `{record['note']}` | {record['line']} | {alt} | "
            f"{record['source_kind']} | <{record['url']}> | {record['suggested_action']} |"
        )
    rows.extend([
        "",
        "## 本地化规则",
        "",
        "1. 只迁移笔记正文已经引用、并且来源明确的论文或项目图。",
        "2. 本地文件必须保留原始 URL、论文 Figure 编号和许可 / 使用说明。",
        "3. 许可不明确的项目站点图片默认保留外链，不自动复制。",
        "4. 本地化后笔记使用 `../assets/images/<note-slug>/<file>` 相对路径。",
        "5. 不把截图重新编码成有损格式；保持原始 PNG / JPG / SVG 类型。",
        "",
    ])
    (OUT_DIR / "image-inventory.md").write_text("\n".join(rows), encoding="utf-8")
    print(f"Inventoried {len(records)} external images across {len(by_note)} notes")


if __name__ == "__main__":
    main()
