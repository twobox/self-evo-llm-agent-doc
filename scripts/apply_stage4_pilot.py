#!/usr/bin/env python3
"""Insert the Stage 4 quick-reading layer into three representative notes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"

HARNESS = r"""
## 30 秒读懂

> **一句话总结：** 这篇论文没有再提出一个新的自演化算法，而是把“谁写出了更好的 harness 更新”和“谁真正能从更新中受益”拆开评测，发现两种能力并不等价，实际瓶颈往往出现在 Task-Solver 对 harness 的激活和持续遵循上。

| 维度 | 内容 |
|---|---|
| 文章性质 | 分析 / 诊断 / 评测论文 |
| 核心问题 | 自演化 Agent 的性能提升究竟来自 Evolver 写得好，还是 Task-Solver 用得好？ |
| 核心机制 | 交叉固定 Evolver 与 Task-Solver，分别测量 Harness Updating 和 Harness Benefit |
| 分析对象 | Prompt、Skill、Memory、Tool、Workflow 等外部 harness |
| 学习阶段 | 不适用；被分析的 harness 更新发生在跨任务部署过程中 |
| 是否跨任务 | 是，前序任务产生的更新用于后续任务 |
| 是否更新模型参数 | 否，论文分析的是冻结模型下的外部 harness 更新 |
| 最重要结论 | 更新质量随基础模型能力提升较平坦；受益能力呈非单调关系；弱模型常败在激活和遵循 |
| 最大局限 | 结论主要适用于冻结参数、外部 harness 更新和论文覆盖的三个 Agent benchmark |

### 三个关键结论

1. **Harness Updating 较平坦**：更强的 Evolver 不一定稳定写出显著更有用的更新。
2. **Harness Benefit 非单调**：中等能力模型常获得最大增益；强模型受天花板限制，弱模型则难以正确使用更新。
3. **弱模型的主要失败不是没有经验，而是不会调用和坚持执行经验**：论文将其归纳为 activation failure 与 adherence failure。

### 不要误读

这篇论文不是说 Evolver 不重要，也不是说弱模型一定最需要 harness 就一定获益最大。它说明的是：**写更新与用更新是两种需要独立测量的能力，端到端分数会把二者混在一起。**

---

## 论文定位

这是一篇 **Self-Evolving Agent / Harness Engineering 的诊断型论文**。它的主要贡献不是新增 memory、skill 或反思算法，而是提供一套能力解耦框架，把自演化链条拆成：

```text
Evolver 生成更新
    ↓
外部 Harness 被修改
    ↓
Task-Solver 激活并遵循更新
    ↓
后续任务性能变化
```

因此，这篇论文最适合作为评估其他自演化方法时的“分析尺子”：当系统变好或变差时，先判断问题在更新生成端，还是在更新使用端。

## 研究问题

> 在冻结模型参数、只演化外部 harness 的系统中，基础模型能力如何分别影响更新生成质量与更新使用收益？

论文进一步追问：

- 更强的模型作为 Evolver，是否一定写出更好的 prompt、skill 或 memory？
- 同一份更新交给不同 Task-Solver，谁能真正把它转化为任务收益？
- 弱模型为什么即使拥有相关 harness，仍然无法完成任务？

## 分析框架卡片

| 维度 | 内容 |
|---|---|
| 被质疑的常见假设 | 更强模型写出的反思或经验更好，因此自演化收益会随模型能力单调提高 |
| 研究对象 | Evolver、Task-Solver，以及二者之间传递的外部 harness 更新 |
| 关键变量 | Evolver 模型、Task-Solver 模型、benchmark、harness 类型 |
| 控制方法 | 固定 Task-Solver 替换 Evolver；固定 Evolver 替换 Task-Solver |
| 主要诊断指标 | 更新带来的下游增益、Harness Updating、Harness Benefit、激活与遵循失败 |
| 覆盖任务 | SWE-bench Verified、MCP-Atlas、SkillsBench |
| 核心发现 | 写更新能力较平坦；使用更新收益非单调；弱模型主要存在 activation / adherence failure |
| 结论边界 | 不直接覆盖参数持续训练、长期开放环境或完全不同的 harness 接口 |

---
""".strip()

MEMOPILOT = r"""
## 30 秒读懂

> **一句话总结：** MemoPilot 冻结执行任务的 player，单独训练一个外部 memory updater，让它在每次交互后把轨迹压缩成下一轮真正可执行的记忆，并用后续任务奖励通过 multi-turn GRPO 学会“怎样写 memory 才有用”。

| 维度 | 内容 |
|---|---|
| 文章性质 | 方法 / 系统论文 |
| 核心问题 | 完整历史和手写反思并不一定能帮助 frozen agent，memory 写入策略如何直接对齐未来任务收益？ |
| 核心机制 | 将 memory updater 视为可训练策略，用 multi-turn GRPO 和下一轮奖励优化跨轮 memory 更新 |
| 更新对象 | Memory updater 的参数，以及部署时持续变化的外部结构化 memory |
| 学习阶段 | 混合：离线训练 updater，测试 / 部署时在线更新 memory |
| 是否跨任务 | 是，在相关任务流中将前序交互经验用于后续任务 |
| 是否更新模型参数 | Player 不更新；只训练外部 memory updater |
| 最重要结论 | 学习得到的 memory policy 比完整历史和 prompt-based memory 更能促进连续任务中的 test-time learning |
| 最大局限 | 依赖明确 reward 和多轮 rollout，实验以可控环境为主，非平稳环境仍会退化 |

### 三个关键结论

1. **历史更多不等于信息更有用**：Full History 可能引入噪声，甚至弱于 No Memory。
2. **Memory update 可以成为独立的 RL policy**：训练目标不是生成漂亮总结，而是提高 frozen player 的后续奖励。
3. **Credit assignment 必须跨轮理解**：第 `t` 次 memory update 无法改变已经发生的第 `t` 轮结果，它主要通过影响第 `t+1` 次交互获得学习信号。

### 不要误读

MemoPilot 不是在测试时微调主模型，也不是简单把所有历史塞进上下文。它训练的是一个 **外挂 memory copilot**；部署时变化的是外部 memory，player 参数保持冻结。

---

## 论文定位

MemoPilot 位于 **Agent Memory、Test-Time Learning 与 RL for Agent** 的交叉处。它把常见的“让 LLM 根据 prompt 写反思”改写为一个明确的策略学习问题：

```text
过去轨迹 + 旧 Memory
    ↓
可训练 Memory Updater
    ↓
新 Memory
    ↓
冻结 Player 在下一轮读取
    ↓
后续环境 Reward 反向训练 Updater
```

相比 EvolveR，MemoPilot 更集中于连续任务流中的 memory 写入策略；相比 ACE，它不是用固定 Generator / Reflector / Curator 提示维护 playbook，而是让 updater 通过奖励学习；相比 Harness Updating 的诊断结论，它直接尝试提升“写出的 memory 能否被 frozen solver 使用”。

## 研究问题

> 能否在不更新执行模型参数的情况下，训练一个外部 memory updater，使冻结 Agent 从连续交互中越来越会做后续任务？

具体包括：

- 怎样从带有噪声和偶然性的历史中提取稳定规律？
- 怎样让 memory 对齐行动，而不只是对过去做自然语言总结？
- memory update 的动作跨多轮产生效果时，奖励应如何归因？
- 学到的 updater 能否迁移到不同规模或不同家族的 player？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 冻结的 player，加一个可训练 memory model / copilot |
| 学习信号来源 | 连续交互的环境 reward，重点使用更新后下一轮表现形成 turn-wise proxy reward |
| 被更新的对象 | 训练阶段更新 memory updater 参数；部署阶段更新外部 memory 内容 |
| 经验形式 | 从交互轨迹抽取的结构化文本，包括模式识别、记忆维护和行动指导 |
| 存储位置 | 受固定预算约束的外部 memory，上下文中提供给 frozen player |
| 更新时间 | 每轮交互结束后，用当前轨迹与旧 memory 生成新 memory |
| 后续使用方式 | 下一轮 player 读取 memory 并据此调整行动 |
| 作用范围 | 相关任务流中的跨任务积累；并评估跨 player 迁移 |
| 是否更新模型参数 | Player 否；memory updater 是 |
| 是否需要明确奖励 | 是，训练依赖可计算的下游 reward |
| 是否依赖教师模型 | 不以更强教师生成标签为核心，但训练依赖环境 rollout 与策略优化 |
| 主要计算与 Token 成本 | 多轮 rollout、GRPO 采样与更新；实验采用 512-token memory budget |

### 时间与信用分配

```text
第 t 轮交互得到轨迹 e_t
        ↓
Updater 生成新记忆 m_t
        ↓
第 t+1 轮 Player 读取 m_t
        ↓
第 t+1 轮 Reward 主要评价第 t 次更新是否有用
```

这也是 turn-wise reward / one-step proxy reward 的直观含义：把一次 memory update 的主要责任归到它最直接影响的下一次交互，而不是归到已经发生的当前轮。

---
""".strip()

SE_AGENT = r"""
## 30 秒读懂

> **一句话总结：** SE-Agent 不训练模型参数，也不建立长期跨任务经验库，而是把同一任务的多条完整 reasoning / acting 轨迹保存到 trajectory pool 中，通过 Revision、Recombination 和 Refinement 继续加工这些尝试，在测试时搜索出更好的最终解。

| 维度 | 内容 |
|---|---|
| 文章性质 | 方法 / 测试时搜索框架 |
| 核心问题 | 多条 Agent 轨迹通常被独立采样，怎样利用不同轨迹中互补的定位、证据和操作步骤？ |
| 核心机制 | 对完整轨迹执行单轨修正、跨轨重组和候选精炼，并把新轨迹继续放回池中 |
| 更新对象 | 当前任务的 trajectory pool 与候选解 |
| 学习阶段 | 测试时 |
| 是否跨任务 | 否，核心机制主要在同一个任务内部演化轨迹 |
| 是否更新模型参数 | 否 |
| 最重要结论 | 轨迹级操作比简单独立多采样更能利用过程信息，适合代码修复等长程 Agent 任务 |
| 最大局限 | 需要生成、保存、读取和评估多条完整轨迹，推理成本较高，也不自动形成长期能力 |

### 三个关键结论

1. **完整轨迹本身可以成为优化对象**：失败常发生在中间定位、工具使用或假设形成，而不只是最终答案。
2. **多轨迹价值来自互补，而不只是数量**：Recombination 尝试组合不同轨迹中的有效局部步骤。
3. **这种 self-evolution 是任务内搜索，不是长期学习**：任务结束后，模型参数不会因此永久变强。

### 不要误读

SE-Agent 不是 SFT / RL 训练，也不是类似 EvolveR、ACE 的长期经验库。它更接近一种 **带反思与遗传式操作的测试时 trajectory search**。

---

## 论文定位

SE-Agent 位于 **Code Agent、Multi-Step Reasoning 与 Test-Time Optimization** 的交叉处。它将 Agent 优化从参数层、Prompt 层和独立采样层，推进到完整轨迹层：

```text
生成多条初始轨迹
    ↓
写入 Trajectory Pool
    ↓
Revision / Recombination / Refinement
    ↓
产生新的候选轨迹并继续迭代
    ↓
选择更好的最终解
```

它与长期 self-evolving 系统的区别在于：知识主要停留在当前任务的轨迹池中，目的是提高本次问题求解，而不是跨任务持续更新模型或外部经验库。

## 研究问题

> 对复杂多步任务，怎样让不同完整轨迹之间相互纠错和互补，而不是仅靠独立多采样或局部搜索？

论文主要针对两个问题：

- 独立轨迹无法共享对仓库、错误位置和工具反馈的发现；
- 多次采样容易围绕高概率路径同质化，增加数量却没有真正扩大有效搜索空间。

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 可生成完整 reasoning / acting 轨迹的多步 Agent，如代码修复 Agent |
| 学习信号来源 | 任务反馈、测试结果、轨迹评价以及历史轨迹中的成功与失败信息 |
| 被更新的对象 | 当前任务的完整轨迹、候选 patch / answer 和 trajectory pool |
| 经验形式 | 完整工具交互轨迹、轨迹摘要、错误定位、策略指导和候选解 |
| 存储位置 | trajectory pool，以及实现中的 `.traj` / `.tra` / pool 文件 |
| 更新时间 | 同一任务的测试时迭代过程中 |
| 后续使用方式 | Operator 读取一条或多条历史轨迹，生成修正版、组合版或精炼版新轨迹 |
| 作用范围 | 单个任务内部；核心方法不依赖跨任务长期复用 |
| 是否更新模型参数 | 否 |
| 是否需要明确奖励 | 需要任务反馈或 evaluator 对候选轨迹进行选择，但不是参数训练奖励 |
| 是否依赖教师模型 | 不必依赖单独教师；通常依赖具备长上下文和工具推理能力的 LLM 执行 operators |
| 主要计算与 Token 成本 | 多条完整 Agent rollout、轨迹上下文读取、测试执行和候选评价 |

### 三类轨迹操作

| Operator | 输入 | 主要作用 |
|---|---|---|
| Revision | 一条已有轨迹 | 识别其中的错误假设或操作，并生成修正版 |
| Recombination | 多条已有轨迹 | 组合不同轨迹中的互补信息与有效步骤 |
| Refinement | 当前较优候选 | 清理冗余、补足遗漏并提高最终解的一致性 |

---
""".strip()


def insert_after_intro(text: str, block: str, *, after_resources: bool) -> str:
    if "## 30 秒读懂" in text:
        raise RuntimeError("quick-read section already exists")
    h1 = re.search(r"^# .+$", text, re.MULTILINE)
    if not h1:
        raise RuntimeError("missing H1")
    if after_resources:
        separator = text.find("\n---\n", h1.end())
        if separator == -1:
            raise RuntimeError("intro separator not found")
        pos = separator + len("\n---\n")
    else:
        pos = h1.end()
    return text[:pos] + "\n\n" + block + "\n\n" + text[pos:].lstrip("\n")


def update(path: Path, block: str, *, after_resources: bool) -> None:
    text = path.read_text(encoding="utf-8")
    text = insert_after_intro(text, block, after_resources=after_resources)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    harness = NOTES / "harness-updating-is-not-harness-benefit.md"
    memo = NOTES / "from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md"
    se_agent = NOTES / "se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md"

    update(harness, HARNESS, after_resources=True)
    update(memo, MEMOPILOT, after_resources=True)
    update(se_agent, SE_AGENT, after_resources=False)

    text = harness.read_text(encoding="utf-8").replace(
        "## 10. 参考链接", "## 10. 参考资料与链接", 1
    )
    harness.write_text(text, encoding="utf-8")

    text = se_agent.read_text(encoding="utf-8").replace(
        "## 14. 参考信息", "## 14. 参考资料与链接", 1
    )
    se_agent.write_text(text, encoding="utf-8")

    text = memo.read_text(encoding="utf-8")
    if "## 11. 参考资料" not in text:
        text += """

---

## 11. 参考资料

- arXiv：<https://arxiv.org/abs/2606.08656>
- PDF：<https://arxiv.org/pdf/2606.08656>
- arXiv HTML：<https://arxiv.org/html/2606.08656v1>
- 相关综述笔记：[From Storage to Experience](from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md)
- 相关诊断笔记：[Harness Updating Is Not Harness Benefit](harness-updating-is-not-harness-benefit.md)
"""
    memo.write_text(text.rstrip() + "\n", encoding="utf-8")

    print("Inserted Stage 4 quick-reading layers into Harness, MemoPilot, and SE-Agent")


if __name__ == "__main__":
    main()
