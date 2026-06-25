#!/usr/bin/env python3
"""Create a classified research-note skeleton from docs/note-template.md."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "docs" / "note-template.md"

PAPER_TYPES = (
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
)
METHOD_TYPES = {"method", "system"}
PAPER_STATUSES = ("preprint", "submitted", "accepted", "published", "withdrawn", "unknown")
LEARNING_STAGES = ("training", "test-time", "deployment", "mixed", "not-applicable")
PARAMETER_UPDATES = ("yes", "no", "auxiliary-only", "mixed", "not-applicable")
CROSS_TASK_VALUES = ("yes", "no", "conditional", "not-applicable")


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise ValueError("title does not produce a non-empty ASCII slug; pass --slug explicitly")
    return slug[:160].rstrip("-")


def replace_metadata(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^  {re.escape(field)}:.*$")
    replacement = f"  {field}: '{value}'"
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError(f"template metadata field not found: {field}")
    return text


def remove_section(text: str, start_heading: str, next_heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^## {re.escape(start_heading)}.*?(?=^## {re.escape(next_heading)})"
    )
    text, count = pattern.subn("", text, count=1)
    if count != 1:
        raise ValueError(f"template section not found: {start_heading}")
    return text


def render_note(
    template: str,
    *,
    title: str,
    short_title: str,
    year: int,
    paper_type: str,
    paper_status: str,
    evolution_object: str,
    learning_stage: str,
    parameter_update: str,
    cross_task: str,
    created: str,
) -> str:
    text = template
    scalar_fields = {
        "title": title,
        "short_title": short_title,
        "paper_type": paper_type,
        "paper_status": paper_status,
        "evolution_object": evolution_object,
        "learning_stage": learning_stage,
        "parameter_update": parameter_update,
        "cross_task": cross_task,
        "created": created,
        "updated": created,
        "last_verified": created,
    }
    for field, value in scalar_fields.items():
        text = replace_metadata(text, field, value)

    text, count = re.subn(r"(?m)^  year:\s*$", f"  year: {year}", text, count=1)
    if count != 1:
        raise ValueError("template metadata field not found: year")

    text = text.replace("# 《论文标题》读书笔记", f"# 《{title}》读书笔记", 1)
    text = text.replace("> 论文：[标题](论文链接)", f"> 论文：[{title}](论文链接)", 1)
    text = text.replace(
        "> 当前状态：会议、期刊或预印本状态；最近核验日期为 YYYY-MM-DD。",
        f"> 当前状态：{paper_status}；最近核验日期为 {created}。",
        1,
    )

    if paper_type in METHOD_TYPES:
        text = remove_section(text, "3B. 分析框架卡片", "4. 核心方法或分析过程")
        text = text.replace("## 3A. 进化机制卡片", "## 3. 进化机制卡片", 1)
        text = text.replace("### 3A.1 知识或经验流动", "### 3.1 知识或经验流动", 1)
        text = text.replace(
            "> 方法型 Self-Evolving Agent 论文保留本节；分析、诊断、综述和 Position 论文可删除本节，改用 3B。\n\n",
            "",
            1,
        )
    else:
        text = remove_section(text, "3A. 进化机制卡片", "3B. 分析框架卡片")
        text = text.replace("## 3B. 分析框架卡片", "## 3. 分析框架卡片", 1)
        text = text.replace(
            "> 分析、诊断、边界研究、综述或 Position 论文保留本节；方法论文可删除本节，改用 3A。\n\n",
            "",
            1,
        )

    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Official paper title")
    parser.add_argument("--short-title", required=True, help="Short display name")
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--paper-type", required=True, choices=PAPER_TYPES)
    parser.add_argument("--paper-status", required=True, choices=PAPER_STATUSES)
    parser.add_argument("--evolution-object", required=True)
    parser.add_argument("--learning-stage", required=True, choices=LEARNING_STAGES)
    parser.add_argument("--parameter-update", required=True, choices=PARAMETER_UPDATES)
    parser.add_argument("--cross-task", required=True, choices=CROSS_TASK_VALUES)
    parser.add_argument("--slug", help="Override generated filename slug")
    parser.add_argument("--date", default=date.today().isoformat(), help="Created/updated date")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, help="Defaults to <root>/notes")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    template_path = root / "docs" / "note-template.md"
    try:
        template = template_path.read_text(encoding="utf-8")
        slug = args.slug or slugify(args.title)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError("slug must contain lowercase ASCII letters, numbers and single hyphens")
        content = render_note(
            template,
            title=args.title,
            short_title=args.short_title,
            year=args.year,
            paper_type=args.paper_type,
            paper_status=args.paper_status,
            evolution_object=args.evolution_object,
            learning_stage=args.learning_stage,
            parameter_update=args.parameter_update,
            cross_task=args.cross_task,
            created=args.date,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    output_dir = args.output_dir.resolve() if args.output_dir else root / "notes"
    target = output_dir / f"{slug}.md"
    if target.exists():
        print(f"ERROR: refusing to overwrite existing file: {target}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"# Target: {target}")
        print(content, end="")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"Created {target}")
    print("Next steps:")
    print("1. Fill authors, institutions, topics, tags, URLs and verified dates.")
    print("2. Complete the note body and claim–evidence–boundary analysis.")
    print("3. Update related_notes, README, experimental comparison and image inventory.")
    print("4. Run the full validation commands from AGENTS.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
