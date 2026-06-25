from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_experimental_comparison.py"
DATA = ROOT / "surveys" / "experimental-comparison-data.json"
OUTPUT = ROOT / "surveys" / "experimental-comparison.md"

spec = importlib.util.spec_from_file_location("generate_experimental_comparison", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ExperimentalComparisonTests(unittest.TestCase):
    def test_data_covers_all_notes_and_matches_metadata(self) -> None:
        payload = module.load_data(DATA)
        records = module.validate_data(ROOT, payload)
        self.assertEqual(len(records), 11)
        self.assertEqual(len({record["id"] for record in records}), 11)
        self.assertEqual(len({record["note"] for record in records}), 11)

    def test_generated_document_is_current(self) -> None:
        payload = module.load_data(DATA)
        records = module.validate_data(ROOT, payload)
        generated = module.render(payload, records)
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), generated)

    def test_all_records_have_cost_evidence_and_boundary(self) -> None:
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        for record in payload["records"]:
            with self.subTest(record=record["id"]):
                self.assertTrue(record["headline_result"].strip())
                self.assertTrue(record["cost_profile"].strip())
                self.assertTrue(record["evidence_strength"].strip())
                self.assertTrue(record["boundary"].strip())

    def test_non_empirical_papers_do_not_claim_new_benchmarks(self) -> None:
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        by_id = {record["id"]: record for record in payload["records"]}
        self.assertEqual(by_id["theory-of-agent"]["benchmarks"], [])
        self.assertEqual(by_id["memory-survey"]["benchmarks"], [])
        self.assertIn("无新增", by_id["theory-of-agent"]["headline_result"])
        self.assertIn("无新增", by_id["memory-survey"]["headline_result"])

    def test_on_limits_and_memopilot_are_included(self) -> None:
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        ids = {record["id"] for record in payload["records"]}
        self.assertIn("adaptability-limits", ids)
        self.assertIn("memopilot", ids)


if __name__ == "__main__":
    unittest.main()
