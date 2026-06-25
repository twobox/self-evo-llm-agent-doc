from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "surveys" / "research-gap-map.md"
NOTES = ROOT / "notes"


class ResearchGapMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = MAP.read_text(encoding="utf-8")

    def test_map_exists_and_links_issue_and_comparison(self) -> None:
        self.assertTrue(MAP.is_file())
        self.assertIn("issues/13", self.text)
        self.assertIn("experimental-comparison.md", self.text)

    def test_all_existing_notes_are_linked(self) -> None:
        notes = sorted(NOTES.glob("*.md"))
        self.assertEqual(len(notes), 11)
        for note in notes:
            relative = f"../notes/{note.name}"
            with self.subTest(note=note.name):
                self.assertIn(relative, self.text)

    def test_at_least_five_explicit_gaps(self) -> None:
        gaps = re.findall(r"(?m)^## \d+\. Gap [A-Z]：", self.text)
        self.assertGreaterEqual(len(gaps), 5)
        self.assertEqual(len(gaps), len(set(gaps)))

    def test_at_least_three_executable_projects(self) -> None:
        projects = re.findall(r"(?m)^## 11\.\d+ 课题 [A-Z]：", self.text)
        self.assertGreaterEqual(len(projects), 3)

    def test_each_project_contains_required_design_fields(self) -> None:
        project_matches = list(re.finditer(r"(?m)^## 11\.\d+ 课题 [A-Z]：.*$", self.text))
        self.assertGreaterEqual(len(project_matches), 3)
        required = (
            "核心假设",
            "最小实验",
            "Baseline",
            "指标",
            "预算",
            "最大风险",
        )
        for index, match in enumerate(project_matches):
            end = project_matches[index + 1].start() if index + 1 < len(project_matches) else self.text.find("\n---\n", match.end())
            if end == -1:
                end = len(self.text)
            section = self.text[match.start() : end]
            with self.subTest(project=match.group(0)):
                for field in required:
                    self.assertIn(field, section)

    def test_external_evidence_is_recorded(self) -> None:
        expected = (
            "PACE: Two-Timescale Self-Evolution",
            "SkillLearnBench",
            "When Does Memory Help Multi-Trajectory Inference?",
            "Memora: From Recall to Forgetting",
            "AgentHER",
            "AgentRx",
            "HarnessFix",
        )
        for work in expected:
            with self.subTest(work=work):
                self.assertIn(work, self.text)

    def test_gap_map_rejects_stale_novelty_claims(self) -> None:
        self.assertIn("失败经验基本没人利用", self.text)
        self.assertIn("还没有长期遗忘 benchmark", self.text)
        self.assertIn("小模型无法自演化", self.text)
        self.assertIn("不再成立", self.text)

    def test_cost_and_failure_chain_are_explicit(self) -> None:
        for term in (
            "fixed memory token",
            "activation / adherence",
            "write",
            "retrieve",
            "utility per 1k memory tokens",
            "equal wall-clock",
            "regression rate",
        ):
            with self.subTest(term=term):
                self.assertIn(term, self.text)


if __name__ == "__main__":
    unittest.main()
