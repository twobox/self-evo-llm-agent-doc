#!/usr/bin/env python3
"""Apply small Stage 9 fixes before regenerating the comparison survey."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_experimental_comparison.py"
DATA = ROOT / "surveys" / "experimental-comparison-data.json"

OLD_COST = '''        cost = record["cost_profile"]
        lowered = cost.lower()
        if "很高" in cost or "高：" in cost or "高推理" in cost:
            difficulty = "高"
        elif "中高" in cost:
            difficulty = "中高"
'''
NEW_COST = '''        cost = record["cost_profile"]
        if "中高" in cost:
            difficulty = "中高"
        elif "很高" in cost or "高：" in cost or "高推理" in cost:
            difficulty = "高"
'''


def main() -> None:
    generator = GENERATOR.read_text(encoding="utf-8")
    if OLD_COST not in generator:
        raise RuntimeError("cost classification block not found")
    GENERATOR.write_text(generator.replace(OLD_COST, NEW_COST, 1), encoding="utf-8")

    data = DATA.read_text(encoding="utf-8")
    data = data.replace("Task-Solver的交叉实验", "Task-Solver 的交叉实验", 1)
    data = data.replace(
        "multiple toxicity / hate-speech annotation datasets",
        "多套 toxicity / hate-speech 标注数据集",
        1,
    )
    DATA.write_text(data, encoding="utf-8")
    print("Patched Stage 9 comparison cost labels and wording")


if __name__ == "__main__":
    main()
