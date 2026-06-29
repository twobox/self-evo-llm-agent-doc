#!/usr/bin/env python3
"""Generate the repository-wide experimental comparison survey from structured data."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

from parse_metadata import find_note_files, parse_metadata_file

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {
    "id", "short_title", "note", "paper_type", "evidence_kind",
    "evolution_object", "learning_stage", "parameter_update", "cross_task",
    "agent_type", "tasks", "method", "benchmarks", "metrics",
    "strongest_baseline", "headline_result", "cost_profile",
    "reproducibility", "evidence_strength", "boundary",
}
PAPER_TYPE_LABELS = {
    "method": "方法", "system": "系统", "diagnostic": "诊断",
    "position": "立场 / 理论", "survey": "综述",
}
LEARNING_STAGE_LABELS = {
    "training": "训练时", "test-time": "测试时", "deployment": "部署时",
    "mixed": "混合", "not-applicable": "不适用",
}
PARAMETER_UPDATE_LABELS = {
    "yes": "是", "no": "否", "auxiliary-only": "仅辅助模块",
    "mixed": "混合", "not-applicable": "不适用",
}
CROSS_TASK_LABELS = {
    "yes": "是", "no": "否", "conditional": "条件性",
    "not-applicable": "不适用",
}
EVIDENCE_LABELS = {
    "empirical-method": "方法实证", "empirical-system": "系统实证",
    "controlled-diagnostic": "受控诊断", "empirical-diagnostic": "实证诊断",
    "theoretical-position": "理论论证", "survey-taxonomy": "综述 / 分类",
}


def load_data(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read comparison data {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        raise ValueError("comparison data root must be an object with schema_version 1.0")
    if not isinstance(payload.get("records"), list):
        raise ValueError("comparison data records must be a list")
    return payload


def validate_data(root: Path, payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[str] = []
    records = payload["records"]
    actual_notes = {path.relative_to(root).as_posix() for path in find_note_files(root)}
    ids: set[str] = set()
    note_paths: set[str] = set()

    for index, record in enumerate(records):
        prefix = f"record[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - set(record))
        extra = sorted(set(record) - REQUIRED_FIELDS)
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
            continue
        if extra:
            errors.append(f"{prefix} has unsupported fields: {', '.join(extra)}")

        record_id, note = str(record["id"]), str(record["note"])
        if record_id in ids:
            errors.append(f"duplicate id: {record_id}")
        if note in note_paths:
            errors.append(f"duplicate note: {note}")
        ids.add(record_id)
        note_paths.add(note)
        if note not in actual_notes:
            errors.append(f"comparison record points to missing note: {note}")
            continue

        for field in ("benchmarks", "metrics"):
            value = record[field]
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                errors.append(f"{prefix}.{field} must be a list of non-empty strings")
        for field in REQUIRED_FIELDS - {"benchmarks", "metrics"}:
            if not isinstance(record[field], str) or not record[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")

        metadata = parse_metadata_file(root / note).metadata
        for field in ("paper_type", "evolution_object", "learning_stage", "parameter_update", "cross_task"):
            if record[field] != metadata.get(field):
                errors.append(
                    f"{note}: comparison {field}={record[field]!r} "
                    f"does not match metadata {metadata.get(field)!r}"
                )
        enum_checks = (
            ("paper_type", PAPER_TYPE_LABELS),
            ("learning_stage", LEARNING_STAGE_LABELS),
            ("parameter_update", PARAMETER_UPDATE_LABELS),
            ("cross_task", CROSS_TASK_LABELS),
            ("evidence_kind", EVIDENCE_LABELS),
        )
        for field, labels in enum_checks:
            if record[field] not in labels:
                errors.append(f"{note}: unsupported {field} {record[field]!r}")

    if note_paths != actual_notes:
        missing = sorted(actual_notes - note_paths)
        extra = sorted(note_paths - actual_notes)
        if missing:
            errors.append(f"notes missing from comparison data: {', '.join(missing)}")
        if extra:
            errors.append(f"unknown notes in comparison data: {', '.join(extra)}")
    if errors:
        raise ValueError("\n".join(errors))
    return records


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def note_link(record: dict[str, Any]) -> str:
    return f"[{md_escape(record['short_title'])}](../{record['note']})"


def join_items(items: list[str]) -> str:
    return "；".join(md_escape(item) for item in items) if items else "—"


def table_section(title: str, headers: list[str], rows: list[list[str]], intro: list[str] | None = None) -> list[str]:
    lines = [title, ""]
    if intro:
        lines.extend(intro + [""])
    lines.extend([
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ])
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def render_positioning(records: list[dict[str, Any]]) -> list[str]:
    rows = []
    for r in records:
        rows.append([
            note_link(r), PAPER_TYPE_LABELS[r["paper_type"]], md_escape(r["agent_type"]),
            md_escape(r["evolution_object"]), LEARNING_STAGE_LABELS[r["learning_stage"]],
            PARAMETER_UPDATE_LABELS[r["parameter_update"]], CROSS_TASK_LABELS[r["cross_task"]],
            md_escape(r["method"]),
        ])
    return table_section(
        "## 1. 研究定位总表",
        ["论文", "类型", "Agent / 任务", "进化或分析对象", "学习阶段", "参数更新", "跨任务", "核心机制"],
        rows,
    )


def render_evidence(records: list[dict[str, Any]]) -> list[str]:
    rows = []
    for r in records:
        rows.append([
            note_link(r), EVIDENCE_LABELS[r["evidence_kind"]], join_items(r["benchmarks"]),
            md_escape(r["strongest_baseline"]), md_escape(r["headline_result"]),
            md_escape(r["evidence_strength"]), md_escape(r["boundary"]),
        ])
    return table_section(
        "## 2. 主实验与证据边界",
        ["论文", "证据类型", "数据集 / 环境", "最强对照", "代表结果", "证据强度", "不能直接推出什么"],
        rows,
        ["> 不同论文的任务、模型、预算和指标并不一致。下表用于比较证据结构，不用于把不同 benchmark 的数字直接排名。"],
    )


def render_cost(records: list[dict[str, Any]]) -> list[str]:
    rows = []
    for r in records:
        cost = r["cost_profile"]
        if "中高" in cost:
            difficulty = "中高"
        elif "很高" in cost or "高：" in cost or "高推理" in cost:
            difficulty = "高"
        elif "中：" in cost:
            difficulty = "中"
        elif "不适用" in cost:
            difficulty = "无系统复现 / 概念复核"
        else:
            difficulty = "中"
        rows.append([note_link(r), md_escape(cost), md_escape(r["reproducibility"]), difficulty])
    return table_section(
        "## 3. 成本与复现条件",
        ["论文", "训练 / 推理成本特征", "复现条件", "复现难度判断"],
        rows,
    )


def render_benchmark_map(records: list[dict[str, Any]]) -> list[str]:
    mapping: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        for benchmark in r["benchmarks"]:
            mapping[benchmark].append(r)
    rows = []
    for benchmark in sorted(mapping, key=str.casefold):
        papers = mapping[benchmark]
        tasks = list(dict.fromkeys(r["tasks"] for r in papers))
        rows.append([
            md_escape(benchmark),
            "、".join(note_link(r) for r in papers),
            "；".join(md_escape(task) for task in tasks),
        ])
    no_benchmark = [r["short_title"] for r in records if not r["benchmarks"]]
    if no_benchmark:
        rows.append(["无新增 benchmark", "、".join(no_benchmark), "理论框架与综述分类"])
    return table_section(
        "## 4. Benchmark / 环境索引",
        ["Benchmark / 环境", "出现论文", "主要任务类型"],
        rows,
    )


def render_metric_map(records: list[dict[str, Any]]) -> list[str]:
    mapping: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        for metric in r["metrics"]:
            mapping[metric].append(r)
    explanations = {
        "Exact Match": "答案标准化后完全匹配，适合开放域 / 多跳问答。",
        "F Score": "允许部分匹配，用于补充问答表现。",
        "F1": "允许部分匹配；Gödel Agent 在 DROP 使用。",
        "TGC": "AppWorld 的 Task Goal Completion。",
        "SGC": "AppWorld 的 Scenario Goal Completion。",
        "Accuracy": "分类、抽取、公式计算或推理正确率。",
        "Pass@1": "单次采样成功率；代码修复中也对应 resolution rate。",
        "Pass@4": "四次采样至少一次成功。",
        "Pass@5": "五次候选至少一次成功，反映有限预算搜索。",
        "resolution rate": "真实 issue 被正确修复的比例。",
        "Medal Rate": "MLE-Bench 达到 medal 阈值的任务比例。",
        "Gold Medal Rate": "达到 gold medal 阈值的任务比例。",
        "Valid Submission Rate": "提交文件可运行且满足格式要求的比例。",
        "Above Median Rate": "超过 Kaggle 人类中位数的任务比例。",
        "Beat Ratio": "超过的人类参赛者比例。",
        "Harness Activation": "是否检索并加载相关 harness。",
        "Harness Adherence": "加载后是否持续遵循 harness。",
        "partial correlation": "控制数据集层混杂因素后的相关性。",
        "rescue rate": "原 zero-shot 错误被后续提示纠正的比例。",
        "confidence": "模型自报或生成的置信度；不等同于严格校准概率。",
        "RPS@k": "连续石头剪刀布任务的 k 轮表现。",
        "LHE@k": "Leduc Hold'em 连续对局表现。",
        "Elo": "相对对战强度评分。",
        "latency": "适配或运行耗时。",
        "rollouts": "获取更新或训练信号所需交互次数。",
        "token cost": "模型调用 token 消耗。",
        "Temporary Drop": "自修改过程中性能短暂下降。",
        "Optimization Failure": "自修改未能超过初始策略。",
        "Task Success Rate": "真实网页任务被自动评价为完成的比例；受网站可访问性与评测时段影响。",
        "Structural Correctness": "世界模型生成的 accessibility tree 是否满足结构和语法约束。",
        "Similarity": "世界模型生成页面与真实下一页面内容的相似程度。",
        "Overall Assessment": "对世界模型生成页面功能与语义连贯性的综合自动评分。",
    }
    rows = []
    for metric in sorted(mapping, key=str.casefold):
        rows.append([
            md_escape(metric),
            "、".join(note_link(r) for r in mapping[metric]),
            md_escape(explanations.get(metric, "论文特定指标；解释时需回到对应任务和评测协议。")),
        ])
    return table_section("## 5. 指标索引", ["指标", "出现论文", "应如何理解"], rows)


def render_conclusions() -> list[str]:
    return [
        "## 6. 横向结论", "",
        "### 6.1 进化对象至少分为五层", "",
        "1. **外部上下文 / 经验资产**：ACE、EvolveR、MemoPilot。",
        "2. **当前任务轨迹或候选解**：SE-Agent、MLEvolve。",
        "3. **模型参数或辅助策略参数**：EvolveR、Self-Challenging、MemoPilot 的 updater、WebEvolver 的策略模型与世界模型。",
        "4. **Agent 可执行程序**：Gödel Agent。",
        "5. **能力边界与评价框架**：Harness Updating、Theory of Agent、On the Limits、Memory Survey。", "",
        "因此，论文都使用 self-evolving / self-improving 术语，并不表示它们在更新同一种东西。", "",
        "### 6.2 测试时优化不等于长期学习", "",
        "SE-Agent、Gödel Agent 和 MLEvolve 都能在当前任务中持续产生更好候选，但 metadata 中均不把它们标记为跨任务长期记忆。WebEvolver 同时包含参数级跨任务训练和测试时 WMLA，必须把 42.49 的训练后策略结果与 51.37 的额外前瞻搜索结果分开理解。判断“是否学习”时，应同时检查：结果是否跨任务保留、是否修改参数、是否有持久经验库。", "",
        "### 6.3 外部经验存在四个独立环节", "",
        "```text", "生成 / 写入 → 检索 / 激活 → 遵循 / 执行 → 产生真实收益", "```", "",
        "ACE 和 EvolveR 重点研究生成与治理；Harness Updating 强调激活和遵循；MemoPilot 直接优化 frozen Player 可执行的 memory。只报告“写出了经验”不足以证明 Harness Benefit。WebEvolver 则把网页转移经验压入模型参数，并通过合成轨迹间接影响后续策略。", "",
        "### 6.4 主结果必须和预算一起阅读", "",
        "MLEvolve 的 12 小时 / 500 expansion / H200、Self-Challenging 的约 12k rollout、SE-Agent 的多轨迹池、EvolveR 的 SFT + GRPO，以及 WebEvolver 的双 70B SFT、真实网页 rollout 和 WMLA 分支搜索都说明：更高结果往往来自更复杂的系统与更高预算。横向比较应优先寻找同模型、同环境、同 rollout 或同 wall-clock 的对照。", "",
        "### 6.5 诊断论文提供了比平均分更细的研究变量", "",
        "- Harness Updating：activation 与 adherence；",
        "- On the Limits：DSF、rescue rate 与 decision stickiness；",
        "- Theory of Agent：tool-use necessity 与 effort allocation；",
        "- Memory Survey：repository、retrieval、utility 与 lifecycle；",
        "- WebEvolver：世界模型结构正确性、页面相似度、可信前瞻深度与分支数。", "",
        "这些变量可用于设计后续 Self-Evolving Agent 实验，而不只是在 benchmark 上再提高一个平均分。",
    ]


def render_gaps() -> list[str]:
    rows = [
        ["成本不可比", "论文常只报告分数，训练、rollout、token、wall-clock 和硬件口径不统一", "同模型、同工具、同 wall-clock / token / rollout 预算的 Pareto 曲线"],
        ["跨任务持久性不足", "多数方法只在当前任务或同构任务流中复用经验", "明确 train task、adapt task、held-out task 和长期 retention test"],
        ["写入与使用混淆", "Memory / skill 写得更好，不代表 solver 会检索和遵循", "分别记录 write quality、retrieval、activation、adherence 和 downstream benefit"],
        ["失败经验治理不足", "多数系统展示新增经验，较少系统研究删除、过期、冲突和污染", "长期任务流中的去重、遗忘、版本回滚与错误经验注入实验"],
        ["参数与外挂经验难分", "同时使用经验库、SFT 和 RL 时，收益来源容易混合", "Experience-only、parameter-only、combined 和 equal-budget 消融"],
        ["评价过度依赖最终成功", "最终答对可能掩盖无必要工具调用、过度搜索或偶然成功", "过程级 reward、必要性、校准、执行成本和可审计轨迹指标"],
        ["开放环境证据有限", "WebEvolver 补充了真实网页证据，但动态网站、过滤任务、自动评价和短期时间窗仍限制结论", "跨月份、跨地区、跨网站版本的长期任务流，以及世界模型错误注入和恢复实验"],
        ["世界模型忠实度不足", "短前瞻有效，深度增加后页面预测快速退化，幻觉缺少直接度量", "校准置信度、分支状态分布、真实状态回放和错误模拟对策略污染的长期评测"],
    ]
    return table_section("## 7. 当前实验缺口", ["缺口", "当前表现", "更理想的实验"], rows)


def render(payload: dict[str, Any], records: list[dict[str, Any]]) -> str:
    count = len(records)
    lines = [
        "<!--", "metadata:",
        "  title: 'Self-Evolving LLM Agent 实验设置横向对比'",
        "  short_title: '实验设置横向对比'",
        "  note_type: '横向综述 / 对比笔记'",
        "  status: '持续维护'",
        f"  scope: '仓库内 {count} 篇笔记的进化对象、实验设计、主要结果、成本与证据边界'",
        "  created: '2026-06-06'", f"  updated: '{payload['updated']}'", "-->", "",
        "# Self-Evolving LLM Agent 实验设置横向对比", "",
        f"本文档覆盖仓库当前全部 **{count} 篇笔记**，用于比较进化对象、学习阶段、参数更新、跨任务能力、实验环境、代表结果、成本、复现条件和证据边界。", "",
        "> **阅读原则：** 不同论文的 benchmark 数字不可直接横向排名。优先比较实验设计、同设置 baseline、消融、预算和“不能证明什么”。", "",
        "数据源：[`experimental-comparison-data.json`](experimental-comparison-data.json)。本文档由 `scripts/generate_experimental_comparison.py` 确定性生成。", "", "---", "",
    ]
    sections: list[Callable[[list[dict[str, Any]]], list[str]]] = [
        render_positioning, render_evidence, render_cost,
        render_benchmark_map, render_metric_map,
    ]
    rendered = [section(records) for section in sections] + [render_conclusions(), render_gaps()]
    for index, section in enumerate(rendered):
        lines.extend(section)
        if index != len(rendered) - 1:
            lines.extend(["", "---", ""])
    lines.extend([
        "", "---", "", "## 8. 维护规则", "", "新增或更新论文时：", "",
        "1. 先更新对应单篇笔记及 metadata；",
        "2. 在 `experimental-comparison-data.json` 中新增或修改记录；",
        "3. 主结果必须同时写最强对照、成本条件和证据边界；",
        "4. Position / Survey 不得伪装成传统 SOTA 实验；",
        "5. 运行：", "", "```bash",
        "python scripts/generate_experimental_comparison.py --check",
        "python -m unittest discover -s tests -v", "```", "",
        f"生成器会检查全部 {count} 篇笔记是否被覆盖，以及 research-positioning 字段是否与 note metadata 一致。", "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    data_path = args.data or root / "surveys" / "experimental-comparison-data.json"
    output_path = args.output or root / "surveys" / "experimental-comparison.md"
    try:
        payload = load_data(data_path)
        records = validate_data(root, payload)
        generated = render(payload, records)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        try:
            current = output_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot read {output_path}: {exc}", file=sys.stderr)
            return 1
        if current != generated:
            print("ERROR: experimental comparison is stale; run python scripts/generate_experimental_comparison.py", file=sys.stderr)
            return 1
        print("Experimental comparison is up to date")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generated, encoding="utf-8")
    print(f"Wrote {output_path.relative_to(root)} with {len(records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
