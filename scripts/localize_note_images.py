#!/usr/bin/env python3
"""Download allowlisted note images, preserve bytes, and rewrite note references."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "images"
DATE = "2026-06-25"


def asset(
    image_id: str,
    note: str,
    alt: str,
    original_url: str,
    local_path: str,
    source_kind: str,
    source_reference: str,
    license_name: str,
    license_url: str,
    attribution: str,
    *,
    reference_url: str | None = None,
) -> dict[str, object]:
    return {
        "id": image_id,
        "note": note,
        "alt": alt,
        "reference_url": reference_url or original_url,
        "original_url": original_url,
        "local_path": local_path,
        "source_kind": source_kind,
        "source_reference": source_reference,
        "license": license_name,
        "license_url": license_url,
        "attribution": attribution,
        "modified": False,
    }


ACE_NOTE = "notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md"
EVOLVER_NOTE = "notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md"
GODEL_NOTE = "notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md"
LIMITS_NOTE = "notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md"
TOA_NOTE = "notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md"
SE_NOTE = "notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md"
CC_BY = "https://creativecommons.org/licenses/by/4.0/"
CC_BY_NC_ND = "https://creativecommons.org/licenses/by-nc-nd/4.0/"

ASSETS = [
    asset("f830691648bd", ACE_NOTE, "Figure 2: Context Collapse", "https://arxiv.org/html/2510.04618v3/x2.png", "assets/images/ace/context-collapse.png", "arxiv-html", "https://arxiv.org/abs/2510.04618", "CC BY 4.0", CC_BY, "Qizheng Zhang et al., Agentic Context Engineering, Figure 2"),
    asset("7ced975d07d0", ACE_NOTE, "Figure 4: The ACE Framework", "https://raw.githubusercontent.com/ace-agent/ace/main/assets/images/ace_framework.png", "assets/images/ace/framework.png", "official-github", "https://github.com/ace-agent/ace/blob/main/assets/images/ace_framework.png", "Apache-2.0", "https://github.com/ace-agent/ace/blob/main/LICENSE.txt", "ace-agent/ace contributors, ACE framework image"),
    asset("07aff7f58783", ACE_NOTE, "Figure 1: Overall Performance Results", "https://arxiv.org/html/2510.04618v3/x1.png", "assets/images/ace/overall-performance.png", "arxiv-html", "https://arxiv.org/abs/2510.04618", "CC BY 4.0", CC_BY, "Qizheng Zhang et al., Agentic Context Engineering, Figure 1"),
    asset("2bf3ba68be70", EVOLVER_NOTE, "Figure 2: Overview of the EvolveR experience lifecycle", "https://raw.githubusercontent.com/KnowledgeXLab/EvolveR/main/assets/framework.png", "assets/images/evolver/framework.png", "official-github", "https://github.com/KnowledgeXLab/EvolveR/blob/main/assets/framework.png", "MIT", "https://github.com/KnowledgeXLab/EvolveR/blob/main/LICENSE", "KnowledgeXLab/EvolveR contributors, EvolveR framework image"),
    asset("9682fbd1b4db", GODEL_NOTE, "Comparison of three agent paradigms", "https://raw.githubusercontent.com/Arvid-pku/Godel_Agent/main/figures/compare.png", "assets/images/godel-agent/paradigm-comparison.png", "official-github", "https://github.com/Arvid-pku/Godel_Agent/blob/main/figures/compare.png", "MIT", "https://github.com/Arvid-pku/Godel_Agent/blob/main/LICENSE", "Arvid-pku/Godel_Agent contributors, agent paradigm comparison"),
    asset("090309f5a099", GODEL_NOTE, "Gödel Agent implemented by Monkey Patching", "https://raw.githubusercontent.com/Arvid-pku/Godel_Agent/main/figures/method.png", "assets/images/godel-agent/monkey-patching-method.png", "official-github", "https://github.com/Arvid-pku/Godel_Agent/blob/main/figures/method.png", "MIT", "https://github.com/Arvid-pku/Godel_Agent/blob/main/LICENSE", "Arvid-pku/Godel_Agent contributors, Gödel Agent method figure"),
    asset("d9199e39f31f", LIMITS_NOTE, "Figure 1: overview from On the Limits of LLM Adaptability", "https://arxiv.org/html/2606.00467v1/x1.png", "assets/images/llm-adaptability/overview.png", "arxiv-html", "https://arxiv.org/abs/2606.00467", "CC BY 4.0", CC_BY, "Etienne Casanova, Rafal Kocielnik, and R. Michael Alvarez, On the Limits of LLM Adaptability, Figure 1"),
    asset("5f3d41bfccc4", LIMITS_NOTE, "Figure 3: decision stickiness and rescue rate from On the Limits of LLM Adaptability", "https://arxiv.org/html/2606.00467v1/rescue_vs_confidence.png", "assets/images/llm-adaptability/decision-stickiness-rescue-rate.png", "arxiv-html", "https://arxiv.org/abs/2606.00467", "CC BY 4.0", CC_BY, "Etienne Casanova, Rafal Kocielnik, and R. Michael Alvarez, On the Limits of LLM Adaptability, Figure 3", reference_url="https://arxiv.org/html/2606.00467v1/x3.png"),
    asset("b9e579ba9ac2", LIMITS_NOTE, "Figure 4: misaligned definitions and confidence from On the Limits of LLM Adaptability", "https://arxiv.org/html/2606.00467v1/calibration_curve.png", "assets/images/llm-adaptability/misaligned-definitions-confidence.png", "arxiv-html", "https://arxiv.org/abs/2606.00467", "CC BY 4.0", CC_BY, "Etienne Casanova, Rafal Kocielnik, and R. Michael Alvarez, On the Limits of LLM Adaptability, Figure 4", reference_url="https://arxiv.org/html/2606.00467v1/x4.png"),
    asset("6dd82801fec8", TOA_NOTE, "Figure 3: Internal, world and population-relative task sets", "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/figures/kb.png", "assets/images/theory-of-agent/knowledge-boundary.png", "project-site", "https://arxiv.org/abs/2506.00886", "CC BY-NC-ND 4.0", CC_BY_NC_ND, "Hongru Wang et al., Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary, Figure 3"),
    asset("aa0667551cb6", TOA_NOTE, "Figure 4: Epistemic effort decomposition for internal and external task sets", "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/figures/toa_intro.png", "assets/images/theory-of-agent/epistemic-effort.png", "project-site", "https://arxiv.org/abs/2506.00886", "CC BY-NC-ND 4.0", CC_BY_NC_ND, "Hongru Wang et al., Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary, Figure 4"),
    asset("14570ebeba78", TOA_NOTE, "Figure 1: Tool-use decisions shape the trajectory of agent intelligence", "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/figures/toa_example.png", "assets/images/theory-of-agent/tool-use-trajectories.png", "project-site", "https://arxiv.org/abs/2506.00886", "CC BY-NC-ND 4.0", CC_BY_NC_ND, "Hongru Wang et al., Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary, Figure 1"),
    asset("996c2e23bf83", SE_NOTE, "SE-Agent Framework", "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/framework.jpg?raw=true", "assets/images/se-agent/framework.jpg", "official-github", "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/framework.jpg", "MIT", "https://github.com/JARVIS-Xs/SE-Agent/blob/main/LICENSE", "JARVIS-Xs/SE-Agent contributors, SE-Agent framework image"),
    asset("95cacfa9cdee", SE_NOTE, "SE-Agent Case Study", "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/se-agent-case-study.png?raw=true", "assets/images/se-agent/case-study.png", "official-github", "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/se-agent-case-study.png", "MIT", "https://github.com/JARVIS-Xs/SE-Agent/blob/main/LICENSE", "JARVIS-Xs/SE-Agent contributors, SE-Agent case-study image"),
]

DEFERRED_REASON = (
    "Paper is distributed on arXiv under the nonexclusive distribution license; "
    "keep the figure external until a separate redistribution license is verified."
)


def image_type(data: bytes) -> str:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.lstrip().startswith(b"<svg") or b"<svg" in data[:512]:
        return "svg"
    raise RuntimeError("downloaded content is not a recognized PNG, JPEG, or SVG image")


def download(url: str) -> bytes:
    headers = {
        "User-Agent": "self-evo-llm-agent-doc-image-localizer/1.0",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read()
            if not data:
                raise RuntimeError("download returned an empty body")
            return data
        except Exception as exc:  # pragma: no cover - network path
            last_error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"failed to download {url}: {last_error}")


def mark_deferred_inventory() -> None:
    path = ROOT / "maintenance" / "image-inventory.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    localized_references = {str(item["reference_url"]) for item in ASSETS}
    for item in payload.get("images", []):
        url = str(item.get("original_url") or item.get("url") or "")
        if url in localized_references:
            continue
        item.update({
            "status": "deferred-license",
            "license": "arXiv nonexclusive distribution license",
            "license_url": "https://info.arxiv.org/help/license/nonexclusive-distrib.html",
            "reason": DEFERRED_REASON,
            "original_url": url,
        })
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remove_invalid_limits_figure(text: str) -> str:
    pattern = re.compile(
        r"> 图源：论文 arXiv HTML Figure 2；用于读书笔记中的学习引用和阅读辅助。\n\n"
        r"!\[Figure 2: DSF and familiarity results from On the Limits of LLM Adaptability\]"
        r"\(https://arxiv\.org/html/2606\.00467v1/x2\.png\)\n\n"
        r"图 2 适合放在 DSF 概念后面。.*?分开理解。\n",
        re.DOTALL,
    )
    replacement = (
        "> **图示校正：** 论文当前版本的 Figure 2 是置信度输出模板，arXiv HTML 将其直接渲染为正文，"
        "并不存在 `x2.png`。DSF 与文本熟悉度的比较主要由回归结果、Table 4 和附录 E 支撑，"
        "因此这里保留文字分析，不再引用失效图片。\n"
    )
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("failed to replace the invalid On the Limits Figure 2 reference")
    return text


def rewrite_notes() -> None:
    by_note: dict[str, list[dict[str, object]]] = {}
    for item in ASSETS:
        by_note.setdefault(str(item["note"]), []).append(item)
    for note_rel, items in by_note.items():
        path = ROOT / note_rel
        text = path.read_text(encoding="utf-8")
        if note_rel == LIMITS_NOTE:
            text = remove_invalid_limits_figure(text)
        for item in items:
            old = str(item["reference_url"])
            replacement = (Path("..") / Path(str(item["local_path"]))).as_posix()
            count = text.count(old)
            if count != 1:
                raise RuntimeError(f"expected one image reference for {old}, found {count}")
            text = text.replace(old, replacement, 1)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_assets_and_manifest() -> None:
    entries: list[dict[str, object]] = []
    for item in ASSETS:
        data = download(str(item["original_url"]))
        kind = image_type(data)
        path = ROOT / str(item["local_path"])
        expected = path.suffix.lower().lstrip(".")
        if expected == "jpeg":
            expected = "jpg"
        if kind != expected:
            raise RuntimeError(f"file type mismatch for {item['original_url']}: {kind} != {expected}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        manifest_item = {key: value for key, value in item.items() if key != "reference_url"}
        manifest_item.update({
            "retrieved_at": DATE,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
        })
        entries.append(manifest_item)

    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "1.0",
        "generated_at": DATE,
        "policy": {
            "preserve_original_bytes": True,
            "allowed_licenses": ["Apache-2.0", "MIT", "CC BY 4.0", "CC BY-NC-ND 4.0"],
            "deferred_license": "arXiv nonexclusive distribution license",
        },
        "images": entries,
    }
    (ASSET_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rows = [
        "# 本地化图片资产",
        "",
        "> 图片来自笔记已经引用的论文或官方项目，下载时保持原始字节。每项记录原始地址、许可、署名和 SHA-256。",
        "",
        "| ID | 笔记 | 本地文件 | 原始来源 | 许可 | 署名 | 是否修改 |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in entries:
        rows.append(
            f"| `{item['id']}` | `{item['note']}` | `{item['local_path']}` | <{item['original_url']}> | "
            f"[{item['license']}]({item['license_url']}) | {item['attribution']} | 否 |"
        )
    rows.extend([
        "",
        "## 使用说明",
        "",
        "- CC BY 4.0 图片使用时需要保留署名和许可证链接。",
        "- CC BY-NC-ND 4.0 图片按原始字节保存，不得裁剪、重编码或添加覆盖层，且不得用于商业目的。",
        "- MIT / Apache-2.0 项目资源保留项目来源与许可链接。",
        "- `manifest.json` 中的 SHA-256 和字节数由 CI 校验。",
        "- 仅有 arXiv nonexclusive distribution license 的图片仍保留外链。",
        "",
    ])
    (ASSET_ROOT / "README.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> None:
    mark_deferred_inventory()
    write_assets_and_manifest()
    rewrite_notes()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "inventory_note_images.py")], check=True)
    print(f"Localized {len(ASSETS)} images; removed one invalid image reference")


if __name__ == "__main__":
    main()
