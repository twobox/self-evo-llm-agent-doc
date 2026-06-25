#!/usr/bin/env python3
"""Complete the fourth research-gap project with the required experiment fields."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "surveys" / "research-gap-map.md"


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"expected exactly one occurrence of: {old!r}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "### 最小环境\n\n构造工具版本变化：",
        "### 最小实验\n\n在可控工具环境中构造版本变化：",
    )
    text = replace_once(text, "### 对照\n\n- append-only memory；", "### Baseline\n\n- append-only memory；")
    text = replace_once(
        text,
        "### 最大风险\n\n人工构造变化可能缺乏现实性。可先作为 benchmark / evaluation paper，而不是声称解决真实长期 Agent。",
        "### 预算\n\n不训练基础模型；使用 1 个工具任务环境、3–4 类可控版本变化和 2 个开源模型。主要成本来自多阶段任务流执行、版本切换和 memory 检索评测。\n\n### 最大风险\n\n人工构造变化可能缺乏现实性。可先作为 benchmark / evaluation paper，而不是声称解决真实长期 Agent。",
    )
    PATH.write_text(text, encoding="utf-8")
    print("Completed project D experiment fields")


if __name__ == "__main__":
    main()
