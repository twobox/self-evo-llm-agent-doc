#!/usr/bin/env python3
"""One-time migration of all notes to metadata schema 1.0 and generated README index."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from generate_readme import generate_index
from parse_metadata import find_note_files, parse_metadata_file

VERIFIED = "2026-06-24"

OVERRIDES: dict[str, dict[str, Any]] = {
    "agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md": {
        "year": 2026, "paper_type": "system", "paper_status": "published",
        "venue": "ICLR 2026", "venue_track": "Poster", "arxiv_version": "v3",
        "project_url": "https://ace-agent.github.io/", "code_status": "official_available",
        "model_status": "not_found", "first_submitted": "2025-10-06",
        "last_revised": "2026-03-29", "evolution_object": "Context / Playbook",
        "learning_stage": "mixed", "parameter_update": "no", "cross_task": "yes",
    },
    "evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md": {
        "year": 2026, "paper_type": "method", "paper_status": "accepted",
        "venue": "ICML 2026", "venue_track": "", "arxiv_version": "v3",
        "project_url": "", "code_status": "official_available",
        "model_status": "official_available", "first_submitted": "2025-10-17",
        "last_revised": "2026-05-16", "evolution_object": "Experience Base / Executor Policy",
        "learning_stage": "mixed", "parameter_update": "yes", "cross_task": "yes",
    },
    "harness-updating-is-not-harness-benefit.md": {
        "year": 2026, "paper_type": "diagnostic", "paper_status": "preprint",
        "venue": "arXiv", "venue_track": "", "arxiv_version": "v1",
        "project_url": "", "code_status": "official_available",
        "model_status": "not_applicable", "first_submitted": "2026-05-28",
        "last_revised": "", "evolution_object": "Harness Updating / Harness Benefit",
        "learning_stage": "not-applicable", "parameter_update": "no", "cross_task": "yes",
    },
    "position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md": {
        "year": 2026, "paper_type": "position", "paper_status": "accepted",
        "venue": "ICML 2026", "venue_track": "Position Paper", "arxiv_version": "v4",
        "project_url": "https://hrwise-nlp.github.io/assets/websites/theory-of-agent/",
        "code_status": "not_found", "model_status": "not_applicable",
        "first_submitted": "2025-06-01", "last_revised": "2026-05-08",
        "evolution_object": "Tool-use Decision Boundary", "learning_stage": "not-applicable",
        "parameter_update": "not-applicable", "cross_task": "not-applicable",
        "tags": ["llm-agent", "external-tools", "overthinking", "overacting", "over-delegation", "meta-cognition", "agentic-rl"],
        "related_notes": [
            "notes/self-challenging-language-model-agents.md",
            "notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md",
            "notes/harness-updating-is-not-harness-benefit.md",
        ],
    },
    "se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md": {
        "year": 2025, "paper_type": "method", "paper_status": "published",
        "venue": "NeurIPS 2025", "venue_track": "Poster", "arxiv_version": "v6",
        "project_url": "https://quantaalpha.com/", "code_status": "official_available",
        "model_status": "not_found", "first_submitted": "2025-08-04",
        "last_revised": "2025-11-03", "evolution_object": "Trajectory Pool",
        "learning_stage": "test-time", "parameter_update": "no", "cross_task": "no",
        "tags": ["llm-agent", "self-evolution", "trajectory-level-evolution", "revision", "recombination", "refinement", "trajectory-pool", "test-time-optimization", "swe-agent", "swe-search", "swe-bench-verified"],
        "related_notes": [
            "notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md",
            "notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md",
            "notes/harness-updating-is-not-harness-benefit.md",
            "notes/self-challenging-language-model-agents.md",
        ],
    },
    "self-challenging-language-model-agents.md": {
        "year": 2025, "paper_type": "method", "paper_status": "published",
        "venue": "NeurIPS 2025", "venue_track": "Poster", "arxiv_version": "v1",
        "project_url": "", "code_status": "not_found", "model_status": "not_found",
        "first_submitted": "2025-06-02", "last_revised": "",
        "evolution_object": "Synthetic Tasks / Executor Policy", "learning_stage": "training",
        "parameter_update": "yes", "cross_task": "yes",
        "tags": ["llm-agent", "self-improvement", "multi-turn-tool-use", "reinforcement-learning", "verifiable-reward", "m3tooleval", "taubench"],
        "related_notes": [
            "notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md",
            "notes/harness-updating-is-not-harness-benefit.md",
        ],
    },
    "godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md": {
        "year": 2025, "paper_type": "method", "paper_status": "published",
        "venue": "ACL 2025", "venue_track": "Long Paper", "arxiv_version": "v4",
        "project_url": "", "code_status": "official_available", "model_status": "not_found",
        "first_submitted": "2024-10-06", "last_revised": "2025-05-31",
        "evolution_object": "Agent Code / Self-Improvement Loop", "learning_stage": "test-time",
        "parameter_update": "no", "cross_task": "no",
        "tags": ["llm-agent", "self-evolution", "recursive-self-improvement", "self-reference", "self-modification", "agent-design-space", "meta-agent-search", "drop", "mgsm", "mmlu", "gpqa"],
        "related_notes": [
            "notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md",
            "notes/harness-updating-is-not-harness-benefit.md",
            "notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md",
            "notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md",
            "notes/self-challenging-language-model-agents.md",
        ],
    },
    "from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md": {
        "year": 2026, "paper_type": "survey", "paper_status": "accepted",
        "venue": "ACL 2026", "venue_track": "Findings", "arxiv_version": "v1",
        "project_url": "", "code_url": "", "resource_url": "https://github.com/FeishuLuo/Evolving-LLM-Agent-Memory-Survey",
        "code_status": "not_applicable", "model_status": "not_applicable",
        "first_submitted": "2026-05-07", "last_revised": "",
        "evolution_object": "Agent Memory Taxonomy", "learning_stage": "not-applicable",
        "parameter_update": "not-applicable", "cross_task": "not-applicable",
    },
    "from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md": {
        "year": 2026, "paper_type": "method", "paper_status": "accepted",
        "venue": "ICML 2026", "venue_track": "", "arxiv_version": "v1",
        "project_url": "", "code_url": "", "original_code_url": "", "resource_url": "",
        "model_url": "", "code_status": "claimed_public_link_missing", "model_status": "not_found",
        "first_submitted": "2026-06-07", "last_revised": "",
        "evolution_object": "Memory Update Policy / External Memory", "learning_stage": "mixed",
        "parameter_update": "auxiliary-only", "cross_task": "yes",
    },
    "mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md": {
        "year": 2026, "paper_type": "system", "paper_status": "preprint",
        "venue": "arXiv", "venue_track": "", "arxiv_version": "v1",
        "project_url": "https://internscience.github.io/MLEvolve/", "code_status": "official_available",
        "model_status": "not_found", "first_submitted": "2026-06-04", "last_revised": "",
        "evolution_object": "Solution Graph / Retrospective Memory", "learning_stage": "test-time",
        "parameter_update": "no", "cross_task": "no",
    },
    "on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md": {
        "year": 2026, "paper_type": "diagnostic", "paper_status": "published",
        "venue": "ICML 2026", "venue_track": "Oral & Spotlight", "arxiv_version": "v1",
        "project_url": "", "code_status": "not_found", "model_status": "not_applicable",
        "first_submitted": "2026-05-30", "last_revised": "",
        "evolution_object": "Model Priors / Prompt Adaptability", "learning_stage": "not-applicable",
        "parameter_update": "not-applicable", "cross_task": "not-applicable",
    },
}

ORDER = [
    "schema_version", "title", "short_title", "year", "note_type", "paper_type",
    "paper_status", "venue", "venue_track", "evolution_object", "learning_stage",
    "parameter_update", "cross_task", "arxiv_id", "arxiv_version", "arxiv_url",
    "pdf_url", "html_url", "project_url", "code_url", "original_code_url",
    "resource_url", "model_url", "code_status", "model_status", "first_submitted",
    "last_revised", "accepted_at", "published_at", "last_verified", "authors",
    "institutions", "topics", "tags", "related_notes", "created", "updated",
]


def _quote(value: str) -> str:
    return repr(value)


def _render(metadata: dict[str, Any]) -> str:
    lines = ["<!--", "metadata:"]
    for key in ORDER:
        value = metadata.get(key, "")
        if isinstance(value, list):
            lines.append(f"  {key}:")
            for item in value:
                lines.append(f"    - {_quote(str(item))}")
        elif isinstance(value, int):
            lines.append(f"  {key}: {value}")
        else:
            lines.append(f"  {key}: {_quote(str(value or ''))}")
    lines.append("-->")
    return "\n".join(lines)


def _migrate_note(path: Path) -> None:
    existing = parse_metadata_file(path).metadata
    override = OVERRIDES[path.name]
    metadata = {
        "schema_version": "1.0",
        "title": existing["title"],
        "short_title": existing["short_title"],
        "year": override["year"],
        "note_type": "中文读书笔记",
        "paper_type": override["paper_type"],
        "paper_status": override["paper_status"],
        "venue": override["venue"],
        "venue_track": override["venue_track"],
        "evolution_object": override["evolution_object"],
        "learning_stage": override["learning_stage"],
        "parameter_update": override["parameter_update"],
        "cross_task": override["cross_task"],
        "arxiv_id": existing.get("arxiv_id", ""),
        "arxiv_version": override["arxiv_version"],
        "arxiv_url": existing.get("arxiv_url", ""),
        "pdf_url": existing.get("pdf_url", ""),
        "html_url": existing.get("html_url", ""),
        "project_url": override.get("project_url", ""),
        "code_url": override.get("code_url", existing.get("code_url", "")),
        "original_code_url": override.get("original_code_url", existing.get("original_code_url", "")),
        "resource_url": override.get("resource_url", ""),
        "model_url": override.get("model_url", existing.get("model_url", "")),
        "code_status": override["code_status"],
        "model_status": override["model_status"],
        "first_submitted": override["first_submitted"],
        "last_revised": override["last_revised"],
        "accepted_at": "",
        "published_at": "",
        "last_verified": VERIFIED,
        "authors": existing.get("authors", []),
        "institutions": existing.get("institutions", []),
        "topics": existing.get("topics", []),
        "tags": override.get("tags", existing.get("tags", [])),
        "related_notes": override.get("related_notes", existing.get("related_notes", [])),
        "created": existing.get("created", ""),
        "updated": VERIFIED,
    }
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\A\s*<!--.*?-->", _render(metadata), text, count=1, flags=re.DOTALL)
    path.write_text(text, encoding="utf-8")


def _patch_docs(root: Path) -> None:
    schema = root / "docs" / "metadata-schema.md"
    text = schema.read_text(encoding="utf-8")
    text = text.replace(
        "  paper_status: ''\n  venue: ''",
        "  paper_status: ''\n  venue: ''\n  venue_track: ''\n  evolution_object: ''\n  learning_stage: ''\n  parameter_update: ''\n  cross_task: ''",
    ).replace("  venue_track: ''\n  venue_track: ''\n", "  venue_track: ''\n")
    if "| `evolution_object` |" not in text:
        text = text.replace(
            "| `venue` | string | 主要会议、期刊或 `arXiv`；不要混入日期和版本 |",
            "| `venue` | string | 主要会议、期刊或 `arXiv`；不要混入日期和版本 |\n"
            "| `evolution_object` | string | 论文主要更新、演化或分析的对象 |\n"
            "| `learning_stage` | enum | 机制发生在训练时、测试时、部署时或混合阶段 |\n"
            "| `parameter_update` | enum | 是否更新模型参数 |\n"
            "| `cross_task` | enum | 是否在不同任务之间积累或复用 |",
        )
    if "### 4.4 `learning_stage`" not in text:
        marker = "## 5. URL 字段"
        extra = """### 4.4 `learning_stage`\n\n- `training`\n- `test-time`\n- `deployment`\n- `mixed`\n- `not-applicable`\n\n### 4.5 `parameter_update`\n\n- `yes`\n- `no`\n- `auxiliary-only`\n- `mixed`\n- `not-applicable`\n\n### 4.6 `cross_task`\n\n- `yes`\n- `no`\n- `conditional`\n- `not-applicable`\n\n"""
        text = text.replace(marker, extra + marker)
    text = text.replace(
        "  paper_status: 'accepted'\n  venue: 'ICML 2026'\n  venue_track: 'Poster'",
        "  paper_status: 'accepted'\n  venue: 'ICML 2026'\n  venue_track: 'Poster'\n  evolution_object: 'External Memory'\n  learning_stage: 'mixed'\n  parameter_update: 'auxiliary-only'\n  cross_task: 'yes'",
    )
    schema.write_text(text, encoding="utf-8")

    template = root / "docs" / "note-template.md"
    text = template.read_text(encoding="utf-8")
    if "  evolution_object: ''" not in text:
        text = text.replace(
            "  venue_track: ''\n  arxiv_id:",
            "  venue_track: ''\n  evolution_object: ''\n  learning_stage: ''\n  parameter_update: ''\n  cross_task: ''\n  arxiv_id:",
        )
    template.write_text(text, encoding="utf-8")

    tests = root / "tests" / "test_note_tooling.py"
    text = tests.read_text(encoding="utf-8")
    if "  evolution_object: 'External Memory'" not in text:
        text = text.replace(
            "  venue: 'arXiv'\n  venue_track: ''",
            "  venue: 'arXiv'\n  venue_track: ''\n  evolution_object: 'External Memory'\n  learning_stage: 'mixed'\n  parameter_update: 'auxiliary-only'\n  cross_task: 'yes'",
            1,
        )
    tests.write_text(text, encoding="utf-8")


def _replace_readme_index(root: Path) -> None:
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    generated = generate_index(root)
    pattern = re.compile(r"## 笔记目录.*?(?=## 横向综述与对比)", re.DOTALL)
    if not pattern.search(text):
        raise RuntimeError("README note-index section was not found")
    readme.write_text(pattern.sub(generated + "\n\n", text, count=1), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    notes = find_note_files(root)
    names = {path.name for path in notes}
    if names != set(OVERRIDES):
        raise RuntimeError(f"migration mapping mismatch: missing={names - set(OVERRIDES)}, extra={set(OVERRIDES) - names}")
    for path in notes:
        _migrate_note(path)
    _patch_docs(root)
    _replace_readme_index(root)
    print(f"Migrated {len(notes)} notes to schema 1.0 and regenerated README index")


if __name__ == "__main__":
    main()
