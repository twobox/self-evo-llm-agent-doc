#!/usr/bin/env python3
"""Download allowlisted note images, preserve bytes, and rewrite note references."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "images"
MANIFEST_PATH = ASSET_ROOT / "manifest.json"
DATE = "2026-06-25"

ASSETS: list[dict[str, str | bool]] = [
    {
        "id": "f830691648bd",
        "note": "notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md",
        "alt": "Figure 2: Context Collapse",
        "original_url": "https://arxiv.org/html/2510.04618v3/x2.png",
        "local_path": "assets/images/ace/context-collapse.png",
        "source_kind": "arxiv-html",
        "source_reference": "https://arxiv.org/abs/2510.04618",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Qizheng Zhang et al., Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models, Figure 2",
        "modified": False,
    },
    {
        "id": "7ced975d07d0",
        "note": "notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md",
        "alt": "Figure 4: The ACE Framework",
        "original_url": "https://raw.githubusercontent.com/ace-agent/ace/main/assets/images/ace_framework.png",
        "local_path": "assets/images/ace/framework.png",
        "source_kind": "official-github",
        "source_reference": "https://github.com/ace-agent/ace/blob/main/assets/images/ace_framework.png",
        "license": "Apache-2.0",
        "license_url": "https://github.com/ace-agent/ace/blob/main/LICENSE.txt",
        "attribution": "ace-agent/ace contributors, ACE framework image",
        "modified": False,
    },
    {
        "id": "07aff7f58783",
        "note": "notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md",
        "alt": "Figure 1: Overall Performance Results",
        "original_url": "https://arxiv.org/html/2510.04618v3/x1.png",
        "local_path": "assets/images/ace/overall-performance.png",
        "source_kind": "arxiv-html",
        "source_reference": "https://arxiv.org/abs/2510.04618",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Qizheng Zhang et al., Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models, Figure 1",
        "modified": False,
    },
    {
        "id": "2bf3ba68be70",
        "note": "notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md",
        "alt": "Figure 2: Overview of the EvolveR experience lifecycle",
        "original_url": "https://raw.githubusercontent.com/KnowledgeXLab/EvolveR/main/assets/framework.png",
        "local_path": "assets/images/evolver/framework.png",
        "source_kind": "official-github",
        "source_reference": "https://github.com/KnowledgeXLab/EvolveR/blob/main/assets/framework.png",
        "license": "MIT",
        "license_url": "https://github.com/KnowledgeXLab/EvolveR/blob/main/LICENSE",
        "attribution": "KnowledgeXLab/EvolveR contributors, EvolveR framework image",
        "modified": False,
    },
    {
        "id": "9682fbd1b4db",
        "note": "notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md",
        "alt": "Comparison of three agent paradigms",
        "original_url": "https://raw.githubusercontent.com/Arvid-pku/Godel_Agent/main/figures/compare.png",
        "local_path": "assets/images/godel-agent/paradigm-comparison.png",
        "source_kind": "official-github",
        "source_reference": "https://github.com/Arvid-pku/Godel_Agent/blob/main/figures/compare.png",
        "license": "MIT",
        "license_url": "https://github.com/Arvid-pku/Godel_Agent/blob/main/LICENSE",
        "attribution": "Arvid-pku/Godel_Agent contributors, agent paradigm comparison",
        "modified": False,
    },
    {
        "id": "090309f5a099",
        "note": "notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md",
        "alt": "Gödel Agent implemented by Monkey Patching",
        "original_url": "https://raw.githubusercontent.com/Arvid-pku/Godel_Agent/main/figures/method.png",
        "local_path": "assets/images/godel-agent/monkey-patching-method.png",
        "source_kind": "official-github",
        "source_reference": "https://github.com/Arvid-pku/Godel_Agent/blob/main/figures/method.png",
        "license": "MIT",
        "license_url": "https://github.com/Arvid-pku/Godel_Agent/blob/main/LICENSE",
        "attribution": "Arvid-pku/Godel_Agent contributors, Gödel Agent method figure",
        "modified": False,
    },
    {
        "id": "d9199e39f31f",
        "note": "notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md",
        "alt": "Figure 1: overview from On the Limits of LLM Adaptability",
        "original_url": "https://arxiv.org/html/2606.00467v1/x1.png",
        "local_path": "assets/images/llm-adaptability/overview.png",
        "source_kind": "arxiv-html",
        "source_reference": "https://arxiv.org/abs/2606.00467",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Etienne Casanova, Liye Wang, and Rafal Kocielnik, On the Limits of LLM Adaptability, Figure 1",
        "modified": False,
    },
    {
        "id": "26d526c234b5",
        "note": "notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md",
        "alt": "Figure 2: DSF and familiarity results from On the Limits of LLM Adaptability",
        "original_url": "https://arxiv.org/html/2606.00467v1/x2.png",
        "local_path": "assets/images/llm-adaptability/dsf-familiarity-results.png",
        "source_kind": "arxiv-html",
        "source_reference": "https://arxiv.org/abs/2606.00467",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Etienne Casanova, Liye Wang, and Rafal Kocielnik, On the Limits of LLM Adaptability, Figure 2",
        "modified": False,
    },
    {
        "id": "5f3d41bfccc4",
        "note": "notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md",
        "alt": "Figure 3: decision stickiness and rescue rate from On the Limits of LLM Adaptability",
        "original_url": "https://arxiv.org/html/2606.00467v1/x3.png",
        "local_path": "assets/images/llm-adaptability/decision-stickiness-rescue-rate.png",
        "source_kind": "arxiv-html",
        "source_reference": "https://arxiv.org/abs/2606.00467",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Etienne Casanova, Liye Wang, and Rafal Kocielnik, On the Limits of LLM Adaptability, Figure 3",
        "modified": False,
    },
    {
        "id": "b9e579ba9ac2",
        "note": "notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md",
        "alt": "Figure 4: misaligned definitions and confidence from On the Limits of LLM Adaptability",
        "original_url": "https://arxiv.org/html/2606.00467v1/x4.png",
        "local_path": "assets/images/llm-adaptability/misaligned-definitions-confidence.png",
        "source_kind": "arxiv-html",
        "source_reference": "https://arxiv.org/abs/2606.00467",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Etienne Casanova, Liye Wang, and Rafal Kocielnik, On the Limits of LLM Adaptability, Figure 4",
        "modified": False,
    },
    {
        "id": "6dd82801fec8",
        "note": "notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md",
        "alt": "Figure 3: Internal, world and population-relative task sets",
        "original_url": "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/figures/kb.png",
        "local_path": "assets/images/theory-of-agent/knowledge-boundary.png",
        "source_kind": "project-site",
        "source_reference": "https://arxiv.org/abs/2506.00886",
        "license": "CC BY-NC-ND 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "attribution": "Hongru Wang et al., Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary, Figure 3",
        "modified": False,
    },
    {
        "id": "aa0667551cb6",
        "note": "notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md",
        "alt": "Figure 4: Epistemic effort decomposition for internal and external task sets",
        "original_url": "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/figures/toa_intro.png",
        "local_path": "assets/images/theory-of-agent/epistemic-effort.png",
        "source_kind": "project-site",
        "source_reference": "https://arxiv.org/abs/2506.00886",
        "license": "CC BY-NC-ND 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "attribution": "Hongru Wang et al., Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary, Figure 4",
        "modified": False,
    },
    {
        "id": "14570ebeba78",
        "note": "notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md",
        "alt": "Figure 1: Tool-use decisions shape the trajectory of agent intelligence",
        "original_url": "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/figures/toa_example.png",
        "local_path": "assets/images/theory-of-agent/tool-use-trajectories.png",
        "source_kind": "project-site",
        "source_reference": "https://arxiv.org/abs/2506.00886",
        "license": "CC BY-NC-ND 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "attribution": "Hongru Wang et al., Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary, Figure 1",
        "modified": False,
    },
    {
        "id": "996c2e23bf83",
        "note": "notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md",
        "alt": "SE-Agent Framework",
        "original_url": "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/framework.jpg?raw=true",
        "local_path": "assets/images/se-agent/framework.jpg",
        "source_kind": "official-github",
        "source_reference": "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/framework.jpg",
        "license": "MIT",
        "license_url": "https://github.com/JARVIS-Xs/SE-Agent/blob/main/LICENSE",
        "attribution": "JARVIS-Xs/SE-Agent contributors, SE-Agent framework image",
        "modified": False,
    },
    {
        "id": "95cacfa9cdee",
        "note": "notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md",
        "alt": "SE-Agent Case Study",
        "original_url": "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/se-agent-case-study.png?raw=true",
        "local_path": "assets/images/se-agent/case-study.png",
        "source_kind": "official-github",
        "source_reference": "https://github.com/JARVIS-Xs/SE-Agent/blob/main/static/img/se-agent-case-study.png",
        "license": "MIT",
        "license_url": "https://github.com/JARVIS-Xs/SE-Agent/blob/main/LICENSE",
        "attribution": "JARVIS-Xs/SE-Agent contributors, SE-Agent case-study image",
        "modified": False,
    },
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


def update_inventory_deferred() -> None:
    inventory_path = ROOT / "maintenance" / "image-inventory.json"
    payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    localized_urls = {str(asset["original_url"]) for asset in ASSETS}
    for item in payload.get("images", []):
        url = str(item.get("original_url") or item.get("url") or "")
        if url in localized_urls:
            continue
        item["status"] = "deferred-license"
        item["license"] = "arXiv nonexclusive distribution license"
        item["license_url"] = "https://info.arxiv.org/help/license/nonexclusive-distrib.html"
        item["reason"] = DEFERRED_REASON
        item["original_url"] = url
    inventory_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def rewrite_notes() -> None:
    by_note: dict[str, list[dict[str, str | bool]]] = {}
    for asset in ASSETS:
        by_note.setdefault(str(asset["note"]), []).append(asset)
    for note_rel, assets in by_note.items():
        path = ROOT / note_rel
        text = path.read_text(encoding="utf-8")
        for asset in assets:
            original = str(asset["original_url"])
            local_path = Path(str(asset["local_path"]))
            relative = Path("..") / local_path
            replacement = relative.as_posix()
            count = text.count(original)
            if count != 1:
                raise RuntimeError(f"expected one image reference for {original}, found {count}")
            text = text.replace(original, replacement, 1)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_assets_and_manifest() -> None:
    entries: list[dict[str, object]] = []
    for asset in ASSETS:
        data = download(str(asset["original_url"]))
        kind = image_type(data)
        local_path = ROOT / str(asset["local_path"])
        expected = local_path.suffix.lower().lstrip(".")
        if expected == "jpeg":
            expected = "jpg"
        if kind != expected:
            raise RuntimeError(
                f"file type mismatch for {asset['original_url']}: expected {expected}, got {kind}"
            )
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(data)
        entry = dict(asset)
        entry.update({
            "retrieved_at": DATE,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
        })
        entries.append(entry)

    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "generated_at": DATE,
        "policy": {
            "preserve_original_bytes": True,
            "allowed_licenses": ["Apache-2.0", "MIT", "CC BY 4.0", "CC BY-NC-ND 4.0"],
            "deferred_license": "arXiv nonexclusive distribution license",
        },
        "images": entries,
    }
    MANIFEST_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = [
        "# 本地化图片资产",
        "",
        "> 这些图片均来自笔记已经引用的论文或官方项目，下载时保持原始字节。每项记录原始地址、许可、署名和 SHA-256。",
        "",
        "| ID | 笔记 | 本地文件 | 原始来源 | 许可 | 署名 | 是否修改 |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in entries:
        rows.append(
            f"| `{item['id']}` | `{item['note']}` | `{item['local_path']}` | "
            f"<{item['original_url']}> | [{item['license']}]({item['license_url']}) | "
            f"{item['attribution']} | 否 |"
        )
    rows.extend([
        "",
        "## 使用说明",
        "",
        "- CC BY 4.0 图片使用时需要保留署名和许可证链接。",
        "- CC BY-NC-ND 4.0 图片仅按原始字节保存，不得裁剪、重编码或添加覆盖层，且不得用于商业目的。",
        "- MIT / Apache-2.0 项目资源保留项目来源与许可链接。",
        "- `manifest.json` 中的 SHA-256 和字节数由 CI 校验。",
        "- 仅有 arXiv nonexclusive distribution license 的图片仍保留外链，见 `maintenance/image-inventory.md`。",
        "",
    ])
    (ASSET_ROOT / "README.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> None:
    update_inventory_deferred()
    write_assets_and_manifest()
    rewrite_notes()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "inventory_note_images.py")], check=True)
    print(f"Localized {len(ASSETS)} images and preserved remaining external references")


if __name__ == "__main__":
    main()
