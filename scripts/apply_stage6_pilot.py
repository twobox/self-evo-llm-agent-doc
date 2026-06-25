#!/usr/bin/env python3
"""Restructure three pilot notes and add claim-evidence-boundary analysis layers."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
H2_RE = re.compile(r"(?m)^## (.+)$")

ACE_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 冻结模型参数，只演化外部 Context / Playbook 也能显著提升复杂 Agent | AppWorld 中 ReAct 为 42.4，ACE offline 为 59.4，ACE online 为 59.5 | ICL 46.0、GEPA 46.4、Dynamic Cheatsheet 51.9 | 在相同基础模型和论文设置下，结构化上下文维护能带来明显任务收益 | 不能证明所有 Agent、所有基础模型或长期开放环境都同样有效 |
| 增量式 playbook 维护比反复重写整份上下文更稳 | Context collapse 案例中上下文从 18,282 tokens 压缩到 122 tokens 后性能下降；ACE 使用 delta update、去重与局部合并 | 全量 prompt evolution / adaptive memory rewriting | 说明整体重写存在丢失细粒度经验的真实风险，局部更新具有工程合理性 | 不能单独证明收益全部来自“增量”而不是更长上下文、更多调用或整体系统设计 |
| 没有人工标签时，自然执行反馈也可以驱动上下文改进 | AppWorld offline 无 GT 为 57.2，online 无 GT 为 59.5 | Base ReAct 42.4、DC online 51.9 | 在有可执行环境反馈的任务上，ground truth 不是唯一可用信号 | 不能推广到缺少 verifier 的任务；FiNER online 无 GT 从 70.7 降到 67.3，说明错误反馈会污染 playbook |
| ACE 的适配过程比强 prompt optimizer 或全量记忆重写更省成本 | AppWorld offline 相比 GEPA latency 降 82.3%、rollout 降 75.1%；FiNER online 相比 DC token cost 降 83.6% | GEPA、Dynamic Cheatsheet | 在论文实现和预算下，delta update 可以降低适配开销 | 不能保证不同 API、缓存策略、并发和计费模式下仍有同样成本优势 |

### 我的判断

ACE 对“上下文可以成为持续改进对象”给出了较强的 benchmark 证据，也用无标签 AppWorld 和金融任务展示了不同反馈条件。最可信的结论是：**结构化增量维护比把历史原样堆进上下文或反复重写整份 Prompt 更可控。**

更弱的结论是“ACE 已经解决长期自我改进”。实验仍集中在 AppWorld 与金融 XBRL，playbook 污染、任务分布漂移和长期安全治理并未被系统验证。

### 其他可能解释

- ACE 使用更长、更细粒度的上下文，部分收益可能来自信息量增加，而不只是更新算法本身。
- Generator、Reflector、Curator 带来了额外模型调用；与 baseline 的计算预算未必在所有维度完全等价。
- 成本优势依赖 prompt cache / KV cache 命中率，真实部署结果会受服务基础设施影响。
""".strip()

EVOLVER_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 经验驱动生命周期能提升搜索增强问答 Agent | Qwen2.5-3B 平均 EM 0.382，高于 Search-R1-instruct 0.325；7B 为 0.417，对照为 0.385 | Search-R1-instruct 等 RL Search Agent | 在论文 QA 设置中，经验原则、检索和策略训练的组合优于只训练搜索策略 | 不能证明相同闭环会在代码、GUI、科研或长期开放任务中保持收益 |
| 推理时检索经验原则是核心组件，不只是训练阶段装饰 | 3B 去掉 experience retrieval 后从 0.382 降到 0.340；0.5B 从 0.150 降到 0.078，1.5B 从 0.270 降到 0.123 | EvolveR w/o exp-retrieve | 说明显式经验检索对最终表现有直接贡献，尤其对小模型更重要 | 不能证明当前 embedding、Top-k 和原则格式是最优检索方案 |
| Self-distillation 可能因认知对齐而优于更强教师 | 3B self-distill 为 0.382，GPT-4o-mini teacher-distill 为 0.370；但 0.5B 和 1.5B 仍是教师更好 | GPT-4o-mini teacher-distill | 说明经验总结者更强不必然意味着经验更适合执行模型 | 不能推广为“自蒸馏总是优于教师”；结果明显依赖模型规模和总结能力 |
| 经验原则与 RL 具有互补性 | 无经验无 RL 为 0.134；RL only 为 0.325；经验+检索无 RL 为 0.357；完整系统为 0.382 | RL only、experience only、去检索消融 | 支持经验外挂和策略学习分别贡献收益，组合最好 | 不完全排除数据量、rollout 数和训练预算差异造成的部分提升 |
| 动态打分与过滤能提高经验库质量 | 人工检查 100 条原则：High-Score 中 Ideal 82%，Low-Score 中 Ideal 26%；经验库约 45k 后继续增长时性能下降 | 高分与低分原则、不同经验库规模 | 说明经验治理和删除低质量原则是必要的 | 样本量有限，人工分类和当前分数是否能长期识别过期经验仍未验证 |

### 我的判断

EvolveR 最有说服力的地方不是单个主表分数，而是消融形成了较完整的因果链：经验原则本身有用、检索有用、RL 有用，三者组合更强。Self-distill 与 teacher-distill 的规模差异也让“认知对齐”不只是口号，而有可观察的边界。

不过，论文仍是一个高成本 QA 系统。把结果解释成通用 Self-Evolving Agent 范式时，需要保留任务类型、训练预算和基础模型能力这三个前提。

### 其他可能解释

- 完整系统包含更多轨迹、检索和训练步骤，收益可能部分来自更高计算预算。
- 域外 QA 的迁移仍与训练任务共享搜索和问答结构，不等于跨动作空间泛化。
- 原则质量分数来自当前任务成功率，任务分布变化后可能产生滞后或错误降权。
""".strip()

LIMITS_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 模型内部概念与任务定义的对齐，比文本记忆更能解释标注表现 | 控制 dataset-level confounds 后，Definition-Specific Familiarity 与性能的 partial r = +0.41；ROUGE-L、BERTScore、embedding cosine 没有正相关 | 三类文本熟悉度 / 相似度指标 | 支持“概念定义对齐”是独立于简单文本记忆的重要解释变量 | 相关性不能直接证明内部先验导致性能，也不能完全排除未观测混杂因素 |
| Prompt、定义和 few-shot 对既有错误的纠正能力有明显上限 | Zero-shot 错误的总体 rescue rate 只有 34.8% | 多种 prompt / definition / few-shot 增强设置 | 说明平均准确率之外，很多原始错误具有 decision stickiness | 不能推广到所有任务、所有模型，也不等于参数训练无法纠正这些错误 |
| 高置信错误通常更难被后续提示纠正 | 对 zero-shot 错误按 confidence 分析，高置信错误 rescue 更困难 | 低置信错误 | 支持 confidence 可能反映更强的内部判断惯性，而不只是答案可靠性 | 模型自报 confidence 不等于严格概率校准，不同模型的 confidence 生成方式也可能不同 |
| 错误任务定义不会稳定触发模型降低信心 | Misaligned definition 会改变模型输出，但 confidence 没有可靠下降 | Aligned definition 条件 | 说明不能仅依赖模型自信度发现定义冲突 | 不能证明模型在所有错误指令下都会盲从，也不能替代更广泛的校准与安全实验 |

### 我的判断

这篇论文最强的贡献是把“Prompt 是否有效”从平均性能问题改造成错误可修复性问题。DSF、rescue rate 和 decision stickiness 为外部文本更新提供了比单一准确率更细的诊断工具。

它对 Self-Evolving Agent 的意义主要是方法论警示，而不是直接证明 Agent memory 无效：**外部经验写入之后，必须测量原本失败的样本是否被救回，以及原本成功的样本是否被干扰。**

### 其他可能解释

- Toxicity / hate-speech 数据集具有社会概念和标签边界差异，现象可能比格式、数学或代码任务更强。
- DSF 的测量方式本身依赖模型输出和任务设计，可能仍混入模型能力或数据分布因素。
- Prompt correction 的上限可能随上下文长度、示例选择、模型版本和推理策略改变。
""".strip()


def _span(text: str, heading: str) -> tuple[int, int]:
    matches = list(H2_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() == heading:
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            return match.start(), end
    raise RuntimeError(f"missing section: {heading}")


def _clean_section(section: str) -> str:
    section = section.strip()
    section = re.sub(r"\n---\s*$", "", section).strip()
    return section


def _pop_section(text: str, heading: str) -> tuple[str, str]:
    start, end = _span(text, heading)
    section = _clean_section(text[start:end])
    remaining = (text[:start].rstrip() + "\n\n" + text[end:].lstrip()).strip() + "\n"
    return remaining, section


def _section_body(section: str) -> str:
    return _clean_section(section.split("\n", 1)[1] if "\n" in section else "")


def _replace_section(text: str, heading: str, replacement: str) -> str:
    start, end = _span(text, heading)
    return text[:start] + replacement.strip() + "\n\n" + text[end:].lstrip()


def _rename_heading(text: str, old: str, new: str) -> str:
    old_line = f"## {old}"
    if old_line not in text:
        raise RuntimeError(f"missing heading to rename: {old}")
    return text.replace(old_line, f"## {new}", 1)


def _insert_after(text: str, heading: str, block: str) -> str:
    _, end = _span(text, heading)
    prefix = text[:end].rstrip()
    suffix = text[end:].lstrip()
    return prefix + "\n\n---\n\n" + block.strip() + "\n\n---\n\n" + suffix


def _insert_before_reference(text: str, block: str) -> str:
    matches = [match for match in H2_RE.finditer(text) if "参考资料" in match.group(1)]
    if not matches:
        raise RuntimeError("reference section not found")
    start = matches[-1].start()
    prefix = text[:start].rstrip()
    suffix = text[start:].lstrip()
    return prefix + "\n\n---\n\n" + block.strip() + "\n\n---\n\n" + suffix


def _normalize_external(section: str, title: str, subheadings: dict[str, str]) -> str:
    lines = section.splitlines()
    lines[0] = f"## {title}"
    normalized = "\n".join(lines)
    for old, new in subheadings.items():
        normalized = normalized.replace(f"### {old}", f"### {new}")
    return normalized


def _update_metadata_date(text: str) -> str:
    comment_end = text.find("-->")
    head, tail = text[:comment_end], text[comment_end:]
    head, count = re.subn(r"(?m)^  updated: '[^']*'$", "  updated: '2026-06-25'", head, count=1)
    if count != 1:
        raise RuntimeError("metadata updated field not found")
    return head + tail


def restructure_ace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text, summary = _pop_section(text, "1. 一句话总结")
    summary_body = _section_body(summary)

    start, end = _span(text, "11. 我的理解与总结")
    current = _clean_section(text[start:end])
    current_body = _section_body(current)
    merged = (
        "## 11. 我的理解与总结\n\n"
        "### 核心理解\n\n"
        + summary_body
        + "\n\n### 进一步总结\n\n"
        + current_body
    )
    text = _replace_section(text, "11. 我的理解与总结", merged)

    text, external = _pop_section(text, "2. 论文外部信息")
    external = _normalize_external(
        external,
        "论文外部信息",
        {
            "2.1 投稿与发表状态": "投稿与发表状态",
            "2.2 作者与机构": "作者与机构",
            "2.3 作者背景和研究圈子": "作者背景和研究圈子",
        },
    )
    text = _rename_heading(text, "3. 所属研究方向与论文定位", "与相关路线的关系")
    text = _rename_heading(text, "4. 核心问题", "问题背景：Brevity Bias 与 Context Collapse")
    text = _insert_after(text, "7. 主要实验结果", ACE_EVIDENCE)
    text = _insert_before_reference(text, external)
    path.write_text(_update_metadata_date(text).rstrip() + "\n", encoding="utf-8")


def restructure_evolver(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text, external = _pop_section(text, "1. 论文外部信息")
    external = _normalize_external(
        external,
        "论文外部信息",
        {
            "1.1 投稿与发表状态": "投稿与发表状态",
            "1.2 作者与机构": "作者与机构",
            "1.3 作者背景和研究圈子观察": "作者背景和研究圈子观察",
        },
    )
    text = _rename_heading(text, "2. 研究方向与论文定位", "与相邻路线的关系")
    text = _rename_heading(text, "3. 核心问题", "问题背景：操作性遗忘、轨迹抽象与认知对齐")
    text = _insert_after(text, "7. 主要实验结论", EVOLVER_EVIDENCE)
    text = _insert_before_reference(text, external)
    path.write_text(_update_metadata_date(text).rstrip() + "\n", encoding="utf-8")


def restructure_limits(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text, status = _pop_section(text, "2. 投稿 / 发表状态")
    text, authors = _pop_section(text, "3. 作者与研究圈子")
    external = (
        "## 论文外部信息\n\n"
        "### 投稿与发表状态\n\n"
        + _section_body(status)
        + "\n\n### 作者与研究圈子\n\n"
        + _section_body(authors)
    )
    text = _rename_heading(text, "4. 所属研究方向与论文定位", "研究坐标与边界")
    text = _rename_heading(text, "7. 论文研究问题", "三个可检验问题")
    text = _insert_after(text, "9. 主要实验结论", LIMITS_EVIDENCE)
    text = _insert_before_reference(text, external)
    path.write_text(_update_metadata_date(text).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    targets = {
        "agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md": restructure_ace,
        "evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md": restructure_evolver,
        "on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md": restructure_limits,
    }
    for name, operation in targets.items():
        path = NOTES / name
        if "## 主张—证据—边界" in path.read_text(encoding="utf-8"):
            raise RuntimeError(f"pilot evidence layer already exists: {name}")
        operation(path)
    print("Restructured 3 pilot notes and added claim-evidence-boundary layers")


if __name__ == "__main__":
    main()
