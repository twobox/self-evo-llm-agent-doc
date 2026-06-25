#!/usr/bin/env python3
"""Enable repository-wide evidence-layer validation and refresh maintenance docs."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_notes.py"
DOCS = ROOT / "docs" / "maintenance-tooling.md"


def update_validator() -> None:
    text = VALIDATOR.read_text(encoding="utf-8")
    if "H3_RE =" not in text:
        text = text.replace(
            'H2_RE = re.compile(r"^##\\s+(.+)$", re.MULTILINE)\n',
            'H2_RE = re.compile(r"^##\\s+(.+)$", re.MULTILINE)\n'
            'H3_RE = re.compile(r"^###\\s+(.+)$", re.MULTILINE)\n',
            1,
        )

    marker = "\n\ndef _validate_legacy("
    if marker not in text:
        raise RuntimeError("validator insertion marker not found")
    if "missing-evidence-layer" not in text:
        addition = r'''

    for heading, code in (
        ("主张—证据—边界", "missing-evidence-layer"),
        ("论文外部信息", "missing-external-info"),
    ):
        if not _has_heading(headings, heading):
            _structure_finding(
                reporter, path, code,
                f"note is missing section containing: {heading}",
                require_structure=require_structure,
            )

    subheadings = H3_RE.findall(text)
    for heading, code in (
        ("我的判断", "missing-evidence-judgment"),
        ("其他可能解释", "missing-alternative-explanations"),
    ):
        if not _has_heading(subheadings, heading):
            _structure_finding(
                reporter, path, code,
                f"evidence layer is missing subsection containing: {heading}",
                require_structure=require_structure,
            )

    evidence_match = re.search(r"(?m)^## .*主张—证据—边界.*$", text)
    external_match = re.search(r"(?m)^## .*论文外部信息.*$", text)
    reference_matches = list(re.finditer(r"(?m)^## .*参考资料.*$", text))
    if evidence_match and external_match and reference_matches:
        if not evidence_match.start() < external_match.start() < reference_matches[-1].start():
            _structure_finding(
                reporter, path, "section-order",
                "expected evidence layer before external information and external information before references",
                require_structure=require_structure,
            )
'''
        text = text.replace(marker, addition + marker, 1)

    VALIDATOR.write_text(text, encoding="utf-8")


def update_docs() -> None:
    text = DOCS.read_text(encoding="utf-8")
    text = text.replace("Stage 3 完成后：", "Stage 7 完成后：", 1)
    old = "- 全部笔记已具备“30 秒读懂”、论文定位、研究问题和适用的机制 / 分析卡片；"
    new = (
        "- 全部笔记已具备“30 秒读懂”、论文定位、研究问题和适用的机制 / 分析卡片；\n"
        "- 全部笔记已具备“主张—证据—边界”“我的判断”和“其他可能解释”；\n"
        "- 作者、机构与投稿信息统一放在证据分析之后、参考资料之前；"
    )
    if old in text:
        text = text.replace(old, new, 1)

    redundant = (
        "\nStage 4 完成快速阅读层和机制卡片后，使用：\n\n"
        "```bash\npython scripts/validate_notes.py . --require-schema --require-structure --strict\n```\n"
    )
    text = text.replace(redundant, "", 1)

    old_list = (
        "- 分析 / 诊断 / 评测论文的分析框架卡片。"
    )
    new_list = (
        "- 分析 / 诊断 / 评测论文的分析框架卡片；\n"
        "- “主张—证据—边界”表格；\n"
        "- 证据层中的“我的判断”和“其他可能解释”；\n"
        "- “论文外部信息”位于证据层之后、参考资料之前。"
    )
    text = text.replace(old_list, new_list, 1)

    text = text.replace(
        "测试覆盖 metadata 解析、严格与过渡校验、本地链接和 README 索引确定性生成。",
        "测试覆盖 metadata 解析、严格与过渡校验、正文证据层与章节顺序、本地链接和 README 索引确定性生成。",
        1,
    )
    DOCS.write_text(text, encoding="utf-8")


def main() -> None:
    update_validator()
    update_docs()
    print("Enabled evidence-layer validation and updated maintenance documentation")


if __name__ == "__main__":
    main()
