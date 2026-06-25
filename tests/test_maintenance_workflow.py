from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "scaffold_note.py"

spec = importlib.util.spec_from_file_location("scaffold_note", SCRIPT)
assert spec and spec.loader
scaffold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scaffold)


class MaintenanceWorkflowTests(unittest.TestCase):
    def test_persistent_entrypoints_exist(self) -> None:
        expected = [
            "AGENTS.md",
            "maintenance/roadmap.md",
            "docs/new-note-workflow.md",
            "skills/note-maintainer/SKILL.md",
            ".github/ISSUE_TEMPLATE/new-paper-note.yml",
            ".github/pull_request_template.md",
        ]
        for relative in expected:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_entrypoints_cross_reference_each_other(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "maintenance" / "roadmap.md").read_text(encoding="utf-8")
        workflow = (ROOT / "docs" / "new-note-workflow.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills" / "note-maintainer" / "SKILL.md").read_text(encoding="utf-8")

        for reference in (
            "maintenance/roadmap.md",
            "docs/new-note-workflow.md",
            "skills/note-maintainer/SKILL.md",
        ):
            self.assertIn(reference, agents)
        self.assertIn("issues/13", roadmap)
        self.assertIn("scripts/scaffold_note.py", workflow)
        self.assertIn("AGENTS.md", skill)
        self.assertIn("generate_experimental_comparison.py", agents)
        self.assertIn("check_images.py", agents)

    def test_slugify(self) -> None:
        self.assertEqual(
            scaffold.slugify("Example: A Self-Evolving Agent Paper"),
            "example-a-self-evolving-agent-paper",
        )
        self.assertEqual(scaffold.slugify("Gödel Agent"), "godel-agent")

    def test_method_scaffold_keeps_only_mechanism_card(self) -> None:
        template = (ROOT / "docs" / "note-template.md").read_text(encoding="utf-8")
        result = scaffold.render_note(
            template,
            title="Example Method",
            short_title="Example",
            year=2026,
            paper_type="method",
            paper_status="preprint",
            evolution_object="Memory",
            learning_stage="test-time",
            parameter_update="no",
            cross_task="conditional",
            created="2026-06-25",
        )
        self.assertIn("# 《Example Method》读书笔记", result)
        self.assertIn("paper_type: 'method'", result)
        self.assertIn("## 3. 进化机制卡片", result)
        self.assertNotIn("## 3B. 分析框架卡片", result)
        self.assertNotIn("## 3A. 进化机制卡片", result)

    def test_diagnostic_scaffold_keeps_only_analysis_card(self) -> None:
        template = (ROOT / "docs" / "note-template.md").read_text(encoding="utf-8")
        result = scaffold.render_note(
            template,
            title="Example Diagnostic",
            short_title="Diagnostic",
            year=2026,
            paper_type="diagnostic",
            paper_status="unknown",
            evolution_object="Capability Boundary",
            learning_stage="not-applicable",
            parameter_update="not-applicable",
            cross_task="not-applicable",
            created="2026-06-25",
        )
        self.assertIn("paper_type: 'diagnostic'", result)
        self.assertIn("## 3. 分析框架卡片", result)
        self.assertNotIn("## 3A. 进化机制卡片", result)
        self.assertNotIn("## 3B. 分析框架卡片", result)

    def test_pull_request_template_requires_generated_views(self) -> None:
        template = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        self.assertIn("experimental-comparison-data.json", template)
        self.assertIn("generate_readme.py", template)
        self.assertIn("check_images.py", template)
        self.assertIn("Roadmap / active Issue", template)


if __name__ == "__main__":
    unittest.main()
