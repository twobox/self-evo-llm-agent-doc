from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from parse_metadata import find_note_files  # noqa: E402

H2_RE = re.compile(r"(?m)^## (.+)$")
H3_RE = re.compile(r"(?m)^### (.+)$")


class EvidenceLayerStructureTests(unittest.TestCase):
    def test_all_notes_have_evidence_judgment_and_alternatives(self) -> None:
        notes = find_note_files(ROOT)
        self.assertGreater(len(notes), 0)
        for path in notes:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                h2 = H2_RE.findall(text)
                h3 = H3_RE.findall(text)
                self.assertTrue(any("主张—证据—边界" in heading for heading in h2))
                self.assertTrue(any("我的判断" in heading for heading in h3))
                self.assertTrue(any("其他可能解释" in heading for heading in h3))

    def test_external_information_is_after_evidence_and_before_references(self) -> None:
        for path in find_note_files(ROOT):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                evidence = text.index("## 主张—证据—边界")
                external = text.index("## 论文外部信息")
                references = [
                    match.start()
                    for match in H2_RE.finditer(text)
                    if "参考资料" in match.group(1)
                ]
                self.assertTrue(references)
                self.assertLess(evidence, external)
                self.assertLess(external, references[-1])

    def test_evidence_tables_express_claim_and_boundary(self) -> None:
        required_headers = (
            "论文主张",
            "支持实验或论证",
            "能证明什么",
            "不能证明什么",
        )
        for path in find_note_files(ROOT):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                start = text.index("## 主张—证据—边界")
                next_h2 = H2_RE.search(text, start + len("## 主张—证据—边界"))
                section = text[start : next_h2.start() if next_h2 else len(text)]
                for header in required_headers:
                    self.assertIn(header, section)


if __name__ == "__main__":
    unittest.main()
