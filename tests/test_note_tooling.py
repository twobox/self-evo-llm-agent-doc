from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_links import check_links  # noqa: E402
from generate_readme import BEGIN, END, generate_index  # noqa: E402
from parse_metadata import MetadataError, parse_metadata_text  # noqa: E402
from validate_notes import validate_repository  # noqa: E402


VALID_NOTE = """<!--
metadata:
  schema_version: '1.0'
  title: 'Example Agent'
  short_title: 'Example'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'method'
  paper_status: 'preprint'
  venue: 'arXiv'
  venue_track: ''
  evolution_object: 'External Memory'
  learning_stage: 'mixed'
  parameter_update: 'auxiliary-only'
  cross_task: 'yes'
  arxiv_id: '2601.00001'
  arxiv_url: 'https://arxiv.org/abs/2601.00001'
  pdf_url: 'https://arxiv.org/pdf/2601.00001'
  html_url: ''
  project_url: ''
  code_url: ''
  original_code_url: ''
  resource_url: ''
  model_url: ''
  code_status: 'not_found'
  model_status: 'not_found'
  first_submitted: '2026-01-01'
  last_revised: ''
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-24'
  authors:
    - 'A'
  institutions:
    - 'U'
  topics:
    - 'Self-Evolving Agent'
  tags:
    - 'self-evolving-agent'
  related_notes:
  created: '2026-06-24'
  updated: '2026-06-24'
-->
# 《Example Agent》读书笔记

## 30 秒读懂

## 1. 论文定位

## 2. 研究问题与动机

## 3. 进化机制卡片

## 4. 参考资料
"""


class ParseMetadataTests(unittest.TestCase):
    def test_parses_scalars_and_lists(self) -> None:
        text = """<!--
metadata:
  schema_version: '1.0'
  title: 'Example'
  year: 2026
  authors:
    - 'A'
    - 'B'
-->
# Example
"""
        metadata = parse_metadata_text(text)
        self.assertEqual(metadata["schema_version"], "1.0")
        self.assertEqual(metadata["year"], 2026)
        self.assertEqual(metadata["authors"], ["A", "B"])

    def test_preserves_legacy_unquoted_scalar(self) -> None:
        text = """<!--
metadata:
  title: Example title
-->
"""
        self.assertEqual(parse_metadata_text(text)["title"], "Example title")

    def test_rejects_duplicate_key(self) -> None:
        text = """<!--
metadata:
  title: 'A'
  title: 'B'
-->
"""
        with self.assertRaises(MetadataError):
            parse_metadata_text(text)

    def test_requires_leading_comment(self) -> None:
        with self.assertRaises(MetadataError):
            parse_metadata_text("# no metadata")


class ValidateNotesTests(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "notes").mkdir()
        return temp, root

    def test_valid_schema_note_passes(self) -> None:
        temp, root = self._repo()
        self.addCleanup(temp.cleanup)
        path = root / "notes" / "example-agent.md"
        path.write_text(VALID_NOTE, encoding="utf-8")
        (root / "README.md").write_text(
            "[notes/example-agent.md](notes/example-agent.md)\n", encoding="utf-8"
        )
        reporter = validate_repository(root)
        self.assertEqual(reporter.errors, 0, reporter.findings)

    def test_invalid_url_and_tag_fail_schema_1(self) -> None:
        temp, root = self._repo()
        self.addCleanup(temp.cleanup)
        broken = VALID_NOTE.replace("code_url: ''", "code_url: 'not found'").replace(
            "self-evolving-agent", "Self Evolving Agent"
        )
        path = root / "notes" / "example-agent.md"
        path.write_text(broken, encoding="utf-8")
        (root / "README.md").write_text(
            "[notes/example-agent.md](notes/example-agent.md)\n", encoding="utf-8"
        )
        reporter = validate_repository(root)
        codes = {item.code for item in reporter.findings if item.severity == "error"}
        self.assertIn("invalid-url", codes)
        self.assertIn("invalid-tag", codes)

    def test_legacy_note_warns_but_does_not_fail(self) -> None:
        temp, root = self._repo()
        self.addCleanup(temp.cleanup)
        legacy = """<!--
metadata:
  title: 'Legacy'
  short_title: 'Legacy'
  year: 2025
  note_type: '中文读书笔记'
  paper_type: 'method / system paper'
  status: 'arXiv'
  venue: 'arXiv'
  authors:
    - 'A'
  topics:
    - 'Agent'
  tags:
    - 'LLM Agent'
  related_notes:
  created: '2026-01-01'
  updated: '2026-01-01'
-->
# 《Legacy》读书笔记
"""
        path = root / "notes" / "legacy.md"
        path.write_text(legacy, encoding="utf-8")
        (root / "README.md").write_text("[legacy](notes/legacy.md)\n", encoding="utf-8")
        reporter = validate_repository(root)
        self.assertEqual(reporter.errors, 0, reporter.findings)
        self.assertGreater(reporter.warnings, 0)


class CheckLinksTests(unittest.TestCase):
    def test_detects_missing_local_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes").mkdir()
            (root / "README.md").write_text("[missing](notes/missing.md)\n", encoding="utf-8")
            issues = check_links(root)
            self.assertEqual(len(issues), 1)

    def test_accepts_existing_and_external_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes").mkdir()
            target = root / "notes" / "a.md"
            target.write_text("# A\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[a](notes/a.md) [web](https://example.com)\n", encoding="utf-8"
            )
            self.assertEqual(check_links(root), [])

    def test_ignores_links_inside_fenced_examples(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes").mkdir()
            (root / "README.md").write_text("```markdown\n[x](missing.md)\n```\n", encoding="utf-8")
            self.assertEqual(check_links(root), [])


class GenerateReadmeTests(unittest.TestCase):
    def test_generates_marked_deterministic_table(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes").mkdir()
            (root / "notes" / "example.md").write_text(VALID_NOTE, encoding="utf-8")
            first = generate_index(root)
            second = generate_index(root)
            self.assertEqual(first, second)
            self.assertIn(BEGIN, first)
            self.assertIn(END, first)
            self.assertIn("arXiv · preprint", first)
            self.assertIn("notes/example.md", first)


if __name__ == "__main__":
    unittest.main()
