from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PilotNoteStructureTests(unittest.TestCase):
    def test_harness_has_quick_read_and_analysis_card(self) -> None:
        text = (ROOT / "notes" / "harness-updating-is-not-harness-benefit.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## 30 秒读懂",
            "## 论文定位",
            "## 研究问题",
            "## 分析框架卡片",
            "参考资料",
        ):
            self.assertIn(heading, text)

    def test_memopilot_has_quick_read_and_mechanism_card(self) -> None:
        text = (
            ROOT
            / "notes"
            / "from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md"
        ).read_text(encoding="utf-8")
        for heading in (
            "## 30 秒读懂",
            "## 论文定位",
            "## 研究问题",
            "## 进化机制卡片",
            "## 11. 参考资料",
        ):
            self.assertIn(heading, text)
        self.assertIn("第 t+1 轮 Reward", text)
        self.assertIn("Player 不更新；只训练外部 memory updater", text)

    def test_se_agent_has_quick_read_and_mechanism_card(self) -> None:
        text = (
            ROOT
            / "notes"
            / "se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md"
        ).read_text(encoding="utf-8")
        for heading in (
            "## 30 秒读懂",
            "## 论文定位",
            "## 研究问题",
            "## 进化机制卡片",
            "参考资料",
        ):
            self.assertIn(heading, text)
        self.assertIn("不是长期跨任务经验库", text)
        self.assertIn("Revision", text)
        self.assertIn("Recombination", text)
        self.assertIn("Refinement", text)


if __name__ == "__main__":
    unittest.main()
