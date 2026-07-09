from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "surveys" / "research-gap-map.md").read_text(encoding="utf-8")


def project_sections() -> list[str]:
    matches = list(re.finditer(r"(?m)^## 11\.\d+ 课题 [A-Z]：.*$", TEXT))
    sections: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else TEXT.find("\n---\n", match.end())
        sections.append(TEXT[match.start() : end if end != -1 else len(TEXT)])
    return sections


class ResearchGapMapTests(unittest.TestCase):
    def test_repository_context(self) -> None:
        self.assertIn("issues/13", TEXT)
        self.assertIn("experimental-comparison.md", TEXT)
        linked_notes = re.findall(r"\.\./notes/([^)\s]+\.md)", TEXT)
        self.assertGreaterEqual(len(set(linked_notes)), 11)
        for relative in linked_notes:
            self.assertTrue((ROOT / "notes" / relative).is_file(), relative)

    def test_gap_and_project_counts(self) -> None:
        self.assertGreaterEqual(len(re.findall(r"(?m)^## \d+\. Gap [A-Z]：", TEXT)), 5)
        self.assertGreaterEqual(len(project_sections()), 3)

    def test_top_projects_are_executable(self) -> None:
        required = ("核心假设", "最小实验", "Baseline", "指标", "预算", "最大风险")
        for section in project_sections()[:3]:
            for field in required:
                self.assertIn(field, section)

    def test_secondary_projects_remain_testable(self) -> None:
        for section in project_sections()[3:]:
            self.assertIn("核心假设", section)
            self.assertTrue("最小实验" in section or "最小环境" in section)
            self.assertTrue("Baseline" in section or "对照" in section)
            self.assertIn("指标", section)
            self.assertIn("最大风险", section)

    def test_recent_external_evidence(self) -> None:
        for work in (
            "PACE: Two-Timescale Self-Evolution",
            "SkillLearnBench",
            "When Does Memory Help Multi-Trajectory Inference?",
            "Memora: From Recall to Forgetting",
            "AgentHER",
            "AgentRx",
            "HarnessFix",
        ):
            self.assertIn(work, TEXT)

    def test_stale_novelty_claims_are_rejected(self) -> None:
        for claim in ("失败经验基本没人利用", "还没有长期遗忘 benchmark", "小模型无法自演化"):
            self.assertIn(claim, TEXT)
        self.assertIn("不再成立", TEXT)

    def test_cost_and_failure_chain(self) -> None:
        for term in (
            "固定 memory token",
            "activation / adherence",
            "write",
            "retrieve",
            "utility per 1k memory tokens",
            "equal wall-clock",
            "regression rate",
        ):
            self.assertIn(term, TEXT)


if __name__ == "__main__":
    unittest.main()
