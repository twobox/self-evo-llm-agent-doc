from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_images import check_repository  # noqa: E402


class ImageAssetTests(unittest.TestCase):
    def test_repository_image_integrity(self) -> None:
        self.assertEqual(check_repository(ROOT), [])

    def test_expected_localization_split(self) -> None:
        inventory = json.loads(
            (ROOT / "maintenance" / "image-inventory.json").read_text(encoding="utf-8")
        )
        self.assertEqual(inventory["total_images"], 27)
        self.assertEqual(inventory["localized_images"], 14)
        self.assertEqual(inventory["external_images"], 13)
        self.assertEqual(inventory["by_status"]["localized"], 14)
        self.assertEqual(inventory["by_status"]["deferred-license"], 13)

    def test_deferred_images_have_explicit_license_reason(self) -> None:
        inventory = json.loads(
            (ROOT / "maintenance" / "image-inventory.json").read_text(encoding="utf-8")
        )
        deferred = [item for item in inventory["images"] if item["status"] == "deferred-license"]
        self.assertEqual(len(deferred), 13)
        for item in deferred:
            with self.subTest(image=item["id"]):
                self.assertEqual(item["license"], "arXiv nonexclusive distribution license")
                self.assertIn("separate redistribution license", item["reason"])
                self.assertTrue(item["reference"].startswith("https://"))

    def test_localized_images_use_allowlisted_licenses(self) -> None:
        manifest = json.loads(
            (ROOT / "assets" / "images" / "manifest.json").read_text(encoding="utf-8")
        )
        allowed = {"Apache-2.0", "MIT", "CC BY 4.0", "CC BY-NC-ND 4.0"}
        self.assertEqual(len(manifest["images"]), 14)
        for item in manifest["images"]:
            with self.subTest(image=item["id"]):
                self.assertIn(item["license"], allowed)
                self.assertFalse(item["modified"])
                self.assertEqual(len(item["sha256"]), 64)
                self.assertGreater(item["size_bytes"], 0)

    def test_invalid_on_limits_figure_two_reference_is_removed(self) -> None:
        note = (
            ROOT
            / "notes"
            / "on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("https://arxiv.org/html/2606.00467v1/x2.png", note)
        self.assertIn("论文当前版本的 Figure 2 是置信度输出模板", note)


if __name__ == "__main__":
    unittest.main()
