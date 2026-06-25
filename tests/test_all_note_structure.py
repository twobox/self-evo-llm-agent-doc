from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from parse_metadata import find_note_files, parse_metadata_file  # noqa: E402
from validate_notes import validate_repository  # noqa: E402


class AllNoteStructureTests(unittest.TestCase):
    def test_all_notes_pass_strict_repository_validation(self) -> None:
        reporter = validate_repository(
            ROOT,
            require_schema=True,
            require_structure=True,
        )
        self.assertEqual(reporter.errors, 0, reporter.findings)
        self.assertEqual(reporter.warnings, 0, reporter.findings)

    def test_all_notes_have_shared_reading_entry(self) -> None:
        notes = find_note_files(ROOT)
        self.assertEqual(len(notes), 11)
        for path in notes:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                for heading in (
                    "## 30 秒读懂",
                    "## 论文定位",
                    "## 研究问题",
                ):
                    self.assertIn(heading, text)
                self.assertRegex(text, r"(?m)^## .*参考资料")

    def test_card_matches_paper_type(self) -> None:
        for path in find_note_files(ROOT):
            metadata = parse_metadata_file(path).metadata
            text = path.read_text(encoding="utf-8")
            paper_type = metadata["paper_type"]
            with self.subTest(path=path.name, paper_type=paper_type):
                if paper_type in {"method", "system"}:
                    self.assertIn("## 进化机制卡片", text)
                if paper_type in {"analysis", "diagnostic", "evaluation"}:
                    self.assertIn("## 分析框架卡片", text)


if __name__ == "__main__":
    unittest.main()
