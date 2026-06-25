from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"


class Stage6PilotStructureTests(unittest.TestCase):
    def _read(self, filename: str) -> str:
        return (NOTES / filename).read_text(encoding="utf-8")

    def _assert_common_order(self, text: str) -> None:
        self.assertIn("## 主张—证据—边界", text)
        self.assertIn("### 我的判断", text)
        self.assertIn("### 其他可能解释", text)
        self.assertIn("## 论文外部信息", text)
        self.assertLess(text.index("## 30 秒读懂"), text.index("## 主张—证据—边界"))
        self.assertLess(text.index("## 主张—证据—边界"), text.index("## 论文外部信息"))
        reference_positions = [
            text.index(line)
            for line in text.splitlines()
            if line.startswith("## ") and "参考资料" in line
        ]
        self.assertTrue(reference_positions)
        self.assertLess(text.index("## 论文外部信息"), reference_positions[-1])

    def test_ace_reorders_external_info_and_adds_evidence(self) -> None:
        text = self._read(
            "agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md"
        )
        self._assert_common_order(text)
        self.assertNotIn("## 1. 一句话总结", text)
        self.assertNotIn("## 2. 论文外部信息", text)
        self.assertNotIn("## 3. 所属研究方向与论文定位", text)
        self.assertIn("## 与相关路线的关系", text)
        self.assertIn("## 问题背景：Brevity Bias 与 Context Collapse", text)
        self.assertIn("AppWorld 中 ReAct 为 42.4", text)
        self.assertIn("FiNER online 无 GT 从 70.7 降到 67.3", text)
        self.assertIn("### 核心理解", text)
        self.assertIn("### 进一步总结", text)

    def test_evolver_reorders_external_info_and_adds_evidence(self) -> None:
        text = self._read("evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md")
        self._assert_common_order(text)
        self.assertNotIn("## 1. 论文外部信息", text)
        self.assertNotIn("## 2. 研究方向与论文定位", text)
        self.assertIn("## 与相邻路线的关系", text)
        self.assertIn("## 问题背景：操作性遗忘、轨迹抽象与认知对齐", text)
        self.assertIn("Qwen2.5-3B 平均 EM 0.382", text)
        self.assertIn("3B self-distill 为 0.382", text)
        self.assertIn("High-Score 中 Ideal 82%", text)

    def test_limits_reorders_external_info_and_adds_evidence(self) -> None:
        text = self._read(
            "on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md"
        )
        self._assert_common_order(text)
        self.assertNotIn("## 2. 投稿 / 发表状态", text)
        self.assertNotIn("## 3. 作者与研究圈子", text)
        self.assertNotIn("## 4. 所属研究方向与论文定位", text)
        self.assertIn("## 研究坐标与边界", text)
        self.assertIn("## 三个可检验问题", text)
        self.assertIn("partial r = +0.41", text)
        self.assertIn("rescue rate 只有 34.8%", text)
        self.assertIn("### 投稿与发表状态", text)
        self.assertIn("### 作者与研究圈子", text)


if __name__ == "__main__":
    unittest.main()
