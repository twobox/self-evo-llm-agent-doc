#!/usr/bin/env python3
"""Add quick-reading layers to the eight remaining notes and enable strict validation."""

from __future__ import annotations

import re
from pathlib import Path

from parse_metadata import parse_metadata_file

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
UPDATED = "2026-06-25"

ACE = r"""
## 30 秒读懂

> **一句话总结：** ACE 不更新模型参数，而是把任务轨迹和反馈持续整理成一个结构化 playbook；Generator 使用经验，Reflector 提取增量，Curator 去重和维护，从而避免反复重写整份上下文造成的 context collapse。

| 维度 | 内容 |
|---|---|
| 文章性质 | Context Engineering 系统论文 |
| 核心问题 | 上下文能否像模型参数一样持续积累能力，同时避免越总结越短、越改越丢细节？ |
| 核心机制 | Generator / Reflector / Curator 三角色，以增量方式维护 evolving playbook |
| 更新对象 | 外部 Context / Playbook 条目 |
| 学习阶段 | 混合，可在历史任务批量整理，也可随任务流持续更新 |
| 是否跨任务 | 是，前序任务经验进入后续任务上下文 |
| 是否更新模型参数 | 否 |
| 最重要结论 | 结构化增量更新比整份上下文反复重写更能保留细粒度经验，并支持后续任务改进 |
| 最大局限 | Playbook 会持续增长，效果仍依赖检索、上下文预算以及执行模型能否正确使用条目 |

### 不要误读

ACE 不是模型微调，也不只是把完整历史塞进长上下文。它演化的是一份经过反思、去重和组织的外部上下文资产。

---

## 论文定位

ACE 位于 **Agentic Context Engineering、Agent Memory 与 Test-Time Adaptation** 的交叉处。它把 self-improvement 的主要载体从模型参数转移到可维护的 playbook：

```text
当前 Playbook + 新任务
    ↓
Generator 执行并产生轨迹
    ↓
Reflector 提取有用与有害经验
    ↓
Curator 增量写入、合并和去重
    ↓
后续任务继续使用更新后的 Playbook
```

相比普通 RAG，ACE 保存的主要不是外部事实，而是任务策略和操作经验；相比 EvolveR，它不通过 SFT / RL 更新 executor；相比简单反思，它强调增量维护而不是整体重写。

## 研究问题

> 在冻结基础模型的条件下，怎样让上下文从连续任务反馈中持续改进，并避免 brevity bias 和 context collapse？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 读取当前 playbook 执行任务的 Generator |
| 学习信号来源 | 任务轨迹、环境反馈、成功与失败结果 |
| 被更新的对象 | 结构化 context items / playbook |
| 经验形式 | 可复用策略、边界条件、工具规则、正负证据及具体注意事项 |
| 存储位置 | 外部 playbook，作为后续请求的上下文资产 |
| 更新时间 | 完成任务或一批任务后，由 Reflector 与 Curator 增量维护 |
| 后续使用方式 | Generator 在新任务中读取相关条目并据此推理或调用工具 |
| 作用范围 | 跨任务持续积累 |
| 是否更新模型参数 | 否 |
| 是否需要明确奖励 | 不要求统一标量奖励，但需要结果或反馈判断经验是否有用 |
| 是否依赖教师模型 | 不要求固定教师；不同角色可由 LLM 实现 |
| 主要计算与 Token 成本 | 额外反思和整理调用、不断增长的 playbook、长上下文推理成本 |

---
""".strip()

EVOLVER = r"""
## 30 秒读懂

> **一句话总结：** EvolveR 把 Agent 的成功与失败轨迹自蒸馏成经验原则，存入可检索的 experience base，再用检索到的经验辅助新任务，并通过 SFT / GRPO 更新 executor，形成“交互—抽象—检索—训练—再交互”的经验驱动生命周期。

| 维度 | 内容 |
|---|---|
| 文章性质 | 方法 / 系统论文 |
| 核心问题 | Agent 做完任务后怎样真正吸收操作经验，而不是下次继续从零开始？ |
| 核心机制 | 轨迹自蒸馏、经验库治理、经验检索与策略参数训练闭环 |
| 更新对象 | Experience Base 与 Executor Policy |
| 学习阶段 | 混合：离线经验整理和训练，在线任务中检索与继续采集轨迹 |
| 是否跨任务 | 是 |
| 是否更新模型参数 | 是，包含 cold-start SFT 和 GRPO 等策略更新 |
| 最重要结论 | 经验不仅可以外挂检索，也能作为策略训练信号，推动搜索 Agent 在生命周期中持续改进 |
| 最大局限 | 系统组件和计算链路较重，效果难完全拆分为经验质量、检索质量或额外训练预算 |

### 不要误读

EvolveR 不是单纯的向量数据库，也不是只在 prompt 中拼接历史轨迹。它同时维护显式经验库并更新 executor 参数。

---

## 论文定位

EvolveR 是一套 **经验驱动的 Self-Evolving Search Agent 生命周期**。它将经验从原始轨迹提升为可治理、可检索的原则，并进一步进入策略训练：

```text
任务交互产生轨迹
    ↓
从成功与失败中自蒸馏经验原则
    ↓
经验去重、合并、过滤并写入 Experience Base
    ↓
新任务检索相关经验辅助推理
    ↓
SFT / GRPO 更新 Executor Policy
    ↓
产生更好的新轨迹与新经验
```

相比 ACE，EvolveR 会更新模型参数；相比 MemoPilot，它既维护经验内容，又训练主 executor；相比 SE-Agent，它面向跨任务生命周期，而不是只优化当前任务的轨迹池。

## 研究问题

> 怎样把 Agent 的交互轨迹转化为可复用经验，并让经验检索与参数训练共同形成持续自我改进闭环？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 可搜索外部知识并执行多步推理的 Search Agent |
| 学习信号来源 | 成功 / 失败轨迹、任务奖励与检索后的下游表现 |
| 被更新的对象 | Experience Base、训练数据和 Executor Policy 参数 |
| 经验形式 | 从轨迹自蒸馏出的策略原则，以及与任务关联的执行经验 |
| 存储位置 | 外部 experience base / 向量检索系统，以及更新后的模型参数 |
| 更新时间 | 轨迹收集后离线整理，并在生命周期迭代中周期更新 |
| 后续使用方式 | 相似任务检索经验进入上下文，同时用于 SFT / GRPO 策略训练 |
| 作用范围 | 跨任务持续积累 |
| 是否更新模型参数 | 是 |
| 是否需要明确奖励 | 是，GRPO 和经验筛选依赖任务反馈 |
| 是否依赖教师模型 | 不以固定更强教师为必要条件，但经验抽象依赖 LLM 自蒸馏能力 |
| 主要计算与 Token 成本 | 轨迹生成、经验抽取、embedding / VDB 检索、SFT 与多轮 RL rollout |

---
""".strip()

TOA = r"""
## 30 秒读懂

> **一句话总结：** Theory of Agent 提出一个规范性原则：只有当 Agent 现有参数、上下文、记忆和内部推理不足以可靠消除任务所需的不确定性时，外部工具调用才是 epistemically necessary。

| 维度 | 内容 |
|---|---|
| 文章性质 | Position / 理论框架论文 |
| 核心问题 | Agent 什么时候应该继续内部推理，什么时候才应该搜索、执行代码或调用外部系统？ |
| 核心观点 | 以知识边界和 epistemic necessity 判断外部工具调用，而不是只看最终答案是否正确 |
| 分析对象 | Internal reasoning 与 external acting 的选择边界 |
| 学习阶段 | 不适用；论文主要提出原则与研究议程 |
| 是否跨任务 | 不适用 |
| 是否更新模型参数 | 不适用 |
| 最重要结论 | 过度推理、过度行动和过度委托都可能损害效率、自主性与长期能力发展 |
| 最大局限 | 核心概念仍需被操作化为可测量信号，并通过更系统的训练和 benchmark 验证 |

### 不要误读

论文不是反对工具使用，也不是要求 Agent 尽量少调用工具。它要求调用发生在**内部认知资源确实不足、外部交互能带来必要新信息或状态变化**的时候。

---

## 论文定位

这篇论文为 Tool-use Agent 提供的是一条 **决策原则**，而不是新的工具调用算法。它将 reasoning、reflection、planning 等视为内部认知工具，将搜索、API、代码执行器和环境操作视为外部物理工具，并追问每一步努力是否与真实知识缺口一致。

其研究意义在于：Agent 评测不能只奖励“最后答对”，还应区分是否 overthinking、overacting 或 over-delegation，以及外部工具是否真的带来了模型内部无法获得的信息。

## 研究问题

> 如何根据 Agent 当前的知识边界，判断一次外部工具调用是否在知识论上必要，并让训练目标鼓励 effort-consistent 的推理与行动？

## 分析框架卡片

| 维度 | 内容 |
|---|---|
| 被质疑的常见假设 | 工具越多、调用越频繁，只要最终成功就越好 |
| 研究对象 | 内部推理、外部行动、知识边界和任务不确定性 |
| 关键变量 | Agent 已有知识、可通过推理获得的信息、外部工具新增信息、调用成本 |
| 主要失配 | Overthinking、Overacting / Tool Overuse、Over-delegation |
| 规范目标 | 让认知与行动投入和真实 epistemic gap 一致 |
| 证据性质 | 理论论证、案例与相关实证工作的综合，而非单一 SOTA 主实验 |
| 核心命题 | 外部工具应在内部能力不足以可靠解决任务时使用 |
| 结论边界 | 如何估计知识边界、必要性和长期能力变化仍是开放问题 |

---
""".strip()

SELF_CHALLENGING = r"""
## 30 秒读懂

> **一句话总结：** Self-Challenging Agent 先探索工具环境并生成带可执行验证器的 Code-as-Task，再让 executor 解这些自生成任务，用验证结果进行强化学习或蒸馏，从而把“缺少人工训练任务”转化为 Agent 自己出题并训练自己的闭环。

| 维度 | 内容 |
|---|---|
| 文章性质 | 自生成任务 + RL 训练方法论文 |
| 核心问题 | 没有大量人工任务和人工评分时，怎样规模化训练多轮工具使用 Agent？ |
| 核心机制 | Challenger 生成 instruction、verification function、example solution 和 failure cases，Executor 解题并由验证器给奖励 |
| 更新对象 | Synthetic Tasks 与 Executor Policy 参数 |
| 学习阶段 | 训练时 |
| 是否跨任务 | 是，自生成任务集用于提升通用工具执行能力 |
| 是否更新模型参数 | 是 |
| 最重要结论 | 可执行验证器让自生成任务具备可过滤、可训练的硬奖励，减少对人工标注任务的依赖 |
| 最大局限 | 依赖能写出可靠验证器的环境；验证器漏洞、任务偏差和自生成数据分布会限制提升 |

### 不要误读

这不是部署阶段的在线自我反思，也不是只生成自然语言问题。核心资产是带验证代码和正反例约束的训练任务，最终改进来自 executor 参数训练。

---

## 论文定位

Self-Challenging 位于 **Synthetic Task Generation、Tool-use Agent 与 RL for Agent** 的交叉处。它把同一个系统拆成两个角色：

```text
Task Challenger 探索环境
    ↓
生成 Code-as-Task 与验证器
    ↓
自动过滤不可行或验证器失效的任务
    ↓
Task Executor 采样多轮工具轨迹
    ↓
验证器给出可复现奖励
    ↓
RL / Distillation 更新 Executor
```

相比经验库方法，它不主要保存过去策略，而是制造新的可验证练习题；相比普通 benchmark 生成，它直接把任务转化为训练闭环。

## 研究问题

> Agent 能否在缺少人工任务集和人工评价标准时，自主生成可行、有难度、可自动判分的工具使用任务，并据此提升自己的 executor？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 能探索工具环境的 Challenger 与待训练的 Executor |
| 学习信号来源 | Code-as-Task 中 verification function 的可执行结果 |
| 被更新的对象 | Synthetic task distribution 与 Executor Policy 参数 |
| 经验形式 | Instruction、验证函数、示例解、失败样例和 executor 轨迹 |
| 存储位置 | 过滤后的任务集、训练轨迹和更新后的模型参数 |
| 更新时间 | 训练阶段分批生成任务、采样轨迹并更新 executor |
| 后续使用方式 | 新任务作为 RL / 蒸馏训练数据，提升多轮工具调用策略 |
| 作用范围 | 跨任务能力训练 |
| 是否更新模型参数 | 是 |
| 是否需要明确奖励 | 是，依赖可执行验证器 |
| 是否依赖教师模型 | 不依赖人工教师标签为核心，但任务和验证器质量受基础模型能力约束 |
| 主要计算与 Token 成本 | 环境探索、任务生成与过滤、多轮 rollout、验证执行和 RL 训练 |

---
""".strip()

GODEL = r"""
## 30 秒读懂

> **一句话总结：** Gödel Agent 把 Agent 当成可读写的运行时程序，让它检查自身代码、与环境交互、修改策略和自我改进逻辑，再递归运行修改后的版本，从固定 pipeline 扩展到 Agent 程序级设计搜索。

| 维度 | 内容 |
|---|---|
| 文章性质 | 自指 / 程序自修改方法论文 |
| 核心问题 | Agent 能否修改的不只是任务策略，还包括负责“如何改进自己”的程序逻辑？ |
| 核心机制 | self-inspect、环境交互、self-update 与递归调用，使用 monkey patching 修改运行时代码 |
| 更新对象 | Agent Code、Policy、Action Set 与 Self-Improvement Loop |
| 学习阶段 | 测试时 / 优化运行时 |
| 是否跨任务 | 核心实验更接近给定任务或任务集内的递归搜索，不是长期经验库 |
| 是否更新模型参数 | 否 |
| 最重要结论 | 允许 Agent 改写自身程序可以探索比固定 meta-learning routine 更大的 agent design space |
| 最大局限 | 自修改容易过拟合评估、引入不可控代码错误和高昂反复执行成本，必须在沙箱中验证 |

### 不要误读

Gödel Agent 不是具有形式证明保证的 Gödel Machine，也不是模型权重递归自训练。它是由 LLM 驱动、依赖环境反馈和代码执行的工程化程序自修改框架。

---

## 论文定位

Gödel Agent 将 self-evolution 的对象推进到 **Agent 程序本身**。与固定的人类 pipeline 或固定 meta-learning 更新器不同，它允许新的 agent 版本成为下一轮自我修改的主体：

```text
读取当前 Agent Code
    ↓
执行任务并观察反馈
    ↓
生成并应用代码修改
    ↓
运行与评估新 Agent
    ↓
新版本继续检查和修改自己
```

它与 SE-Agent 的任务内轨迹优化不同，也与 ACE / EvolveR 的外部经验维护不同：这里直接改变执行逻辑和更新逻辑。

## 研究问题

> 如果固定的 agent pipeline 和 meta-learning algorithm 本身也可能成为能力上限，能否让 Agent 读写自身代码，递归搜索更大的设计空间？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 带有限基础 action functions 的可执行 Agent 程序 |
| 学习信号来源 | 环境交互结果、任务性能和新版本评估 |
| 被更新的对象 | Agent policy、工具 / 动作集合、代码结构和自我更新逻辑 |
| 经验形式 | 代码补丁、运行日志、评估结果和改进假设 |
| 存储位置 | 运行时代码、monkey-patched 模块和生成后的 Agent 版本 |
| 更新时间 | 每轮递归自我改进时 |
| 后续使用方式 | 修改后的程序直接成为下一轮执行与自修改主体 |
| 作用范围 | 当前优化任务或评估任务集内部 |
| 是否更新模型参数 | 否 |
| 是否需要明确奖励 | 需要可比较的任务性能或 fitness 判断版本是否更好 |
| 是否依赖教师模型 | 不要求独立教师，但依赖基础 LLM 生成和理解代码 |
| 主要计算与 Token 成本 | 多轮代码生成、执行、评估、回滚和递归搜索 |

---
""".strip()

SURVEY = r"""
## 30 秒读懂

> **一句话总结：** 这篇综述用 Storage → Reflection → Experience 组织 Agent Memory 的演化：从保存原始轨迹，到纠错和提纯轨迹，再到主动探索并跨多条轨迹抽象可迁移的规则、技能或策略。

| 维度 | 内容 |
|---|---|
| 文章性质 | Agent Memory 分类综述 |
| 核心问题 | 不同 memory 工作到底是在保存历史、修正历史，还是已经形成可迁移经验？ |
| 核心框架 | Storage、Reflection、Experience 三阶段 taxonomy |
| 分析对象 | 轨迹保存、轨迹提纯、跨轨迹抽象与主动探索 |
| 学习阶段 | 不适用；覆盖多类训练时和测试时方法 |
| 是否跨任务 | 不适用；被综述方法各不相同 |
| 是否更新模型参数 | 不适用；分类同时覆盖外部记忆与参数化经验 |
| 最重要结论 | “经验”不应等同于任何历史记录，而应强调从多条交互中抽象出可迁移策略先验 |
| 最大局限 | 三阶段之间存在重叠，taxonomy 不能替代统一 benchmark、成本和真实长期记忆评测 |

### 不要误读

Storage 中保存一个成功案例并不自动等于 Experience。论文所说的 Experience 更强调主动获取信息和跨轨迹抽象，而不是简单检索相似历史。

---

## 论文定位

这是一篇 **Agent Memory / Self-Evolving Agent 的总纲型综述**。它提供的价值不是新算法，而是一套判断坐标：

```text
Storage：记住发生过什么
Reflection：判断哪些轨迹可信、应怎样修正
Experience：从多条轨迹抽象以后可迁移的策略
```

用这套框架可以区分：SE-Agent 更接近任务内轨迹保存和反思，ACE 把经验维护成 playbook，EvolveR 维护经验原则并训练策略，MemoPilot 则学习 memory update policy。

## 研究问题

> LLM Agent Memory 如何从被动存储演化为能主动探索、抽象规律并支持持续适应的经验系统？

## 分析框架卡片

| 维度 | 内容 |
|---|---|
| 被澄清的常见混淆 | 任何历史日志、反思文本或相似案例都被统一称为 experience |
| 研究对象 | LLM Agent 的 memory 写入、管理、检索和经验形成机制 |
| 第一层 | Storage：线性、向量或结构化保存轨迹 |
| 第二层 | Reflection：内省、外部反馈或交互反馈驱动的轨迹修正与提纯 |
| 第三层 | Experience：主动探索与跨轨迹抽象形成可迁移先验 |
| 核心区分 | 全局 memory repository 不等于某次推理实际检索到的 memory |
| 综述证据 | 对相关方法、benchmark 和研究趋势的分类综合 |
| 结论边界 | 分类边界可重叠，尚缺统一长期、动态和成本敏感评测 |

---
""".strip()

MLEVOLVE = r"""
## 30 秒读懂

> **一句话总结：** MLEvolve 把自动机器学习工程建模成长期方案搜索：用 Monte Carlo Graph Search 连接不同代码分支，以 Retrospective Memory 保存计划、代码、分数和失败分析，再用分层规划与自适应代码生成持续产生更好的 ML pipeline。

| 维度 | 内容 |
|---|---|
| 文章性质 | MLE / AutoML Agent 系统论文 |
| 核心问题 | 长时程 ML 工程搜索中，怎样让不同分支共享发现、保存可解释经验，并避免每轮粗暴重写全部代码？ |
| 核心机制 | Progressive MCGS、Retrospective Memory、Hierarchical Planning 与 Adaptive Code Generation |
| 更新对象 | Solution Graph、Retrospective Memory 与候选代码方案 |
| 学习阶段 | 测试时长程搜索 |
| 是否跨任务 | 核心机制主要服务当前 MLE 任务，不等于跨任务长期学习 |
| 是否更新模型参数 | 否 |
| 最重要结论 | 图搜索和结构化回顾让 Agent 能跨分支引用有效方案，并根据反馈更稳定地迭代代码 |
| 最大局限 | 单任务预算可达小时级，计算和模型调用成本高；最终提升同时受到基础模型、搜索预算和执行基础设施影响 |

### 不要误读

MLEvolve 不是在训练一个新的通用 AutoML 模型，也不是像 Gödel Agent 那样改写 Agent 框架本身。它演化的是当前任务的 ML 解法、搜索图和外部经验。

---

## 论文定位

MLEvolve 位于 **Machine Learning Engineering Agent、Algorithm Discovery 与 Self-Evolving Search** 的交叉处。它面向需要反复运行代码和读取硬指标的 Kaggle-style 任务：

```text
规划候选方案
    ↓
生成 / 修改并执行代码
    ↓
读取 metric、报错和分析
    ↓
写入 Solution Graph 与 Retrospective Memory
    ↓
跨分支参考、融合或继续探索
```

相比纯树搜索，图结构允许非父子分支互相引用；相比只回传标量 reward，它保存“为什么成功或失败”；相比整文件重写，它根据改动范围选择 full rewrite、模块生成或 diff patch。

## 研究问题

> 如何让 MLE Agent 在有限时间预算内跨分支共享信息、复用执行经验，并根据任务状态选择合适粒度的规划与代码修改？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | 可规划、编写和运行 ML pipeline 的 MLE Agent |
| 学习信号来源 | 本地验证指标、submission 代理分数、运行错误和执行反馈 |
| 被更新的对象 | Candidate solution graph、retrospective memory 和代码候选 |
| 经验形式 | Plan、code、metric、outcome、错误分析、feedback 与分支引用关系 |
| 存储位置 | Monte Carlo solution graph 与全局 retrospective memory |
| 更新时间 | 当前任务的长期搜索与每次代码执行之后 |
| 后续使用方式 | 支持节点选择、跨分支融合、规划、调试和下一版代码生成 |
| 作用范围 | 单个 MLE / 算法发现任务内部 |
| 是否更新模型参数 | 否 |
| 是否需要明确奖励 | 是，依赖可执行的模型评价指标 |
| 是否依赖教师模型 | 不要求独立教师，但依赖强代码与规划模型 |
| 主要计算与 Token 成本 | 多分支代码生成、模型训练运行、指标评估和小时级搜索预算 |

---
""".strip()

LIMITS = r"""
## 30 秒读懂

> **一句话总结：** 这篇论文发现 LLM 在标注任务中不是可被 prompt 任意重写的空白分类器；模型内部概念与任务定义越对齐，表现通常越好，而当二者冲突时，补充定义和 few-shot 示例也常受 decision stickiness 限制。

| 维度 | 内容 |
|---|---|
| 文章性质 | LLM 可适应性边界 / 诊断论文 |
| 核心问题 | 用户提供的定义和示例能否稳定覆盖模型在训练中形成的内部概念先验？ |
| 核心机制 | 用 Definition-Specific Familiarity、文本熟悉度和行为干预分析内部先验与 prompt steerability |
| 分析对象 | Model-Internalized Priors、标注定义与决策粘性 |
| 学习阶段 | 不适用；研究的是推理时提示适应能力 |
| 是否跨任务 | 不适用 |
| 是否更新模型参数 | 不适用 |
| 最重要结论 | 性能更受模型内部概念与定义的对齐程度影响，而不只是文本记忆；既有决策可能难被定义和示例纠正 |
| 最大局限 | 结论主要来自特定标注概念、数据集、模型和提示干预，不能直接外推到所有领域或参数训练 |

### 不要误读

论文不是说 prompt 和 few-shot 永远无效，也不是说模型完全不能适应。它说明适应能力有边界，并且边界与模型已经内化的概念和决策惯性有关。

---

## 论文定位

这篇文章不属于核心 Self-Evolving Agent 方法，而是一篇重要的 **外部文本更新有效性边界研究**。它质疑一个常见假设：只要把新定义、规则或示例写进 prompt，模型就会按照新标准行动。

这一结论与 Harness Updating 的问题直接相关：外部 memory、skill 或定义被写入上下文后，Task-Solver 是否真正改变行为，取决于外部信息与模型内部先验的关系以及模型的可操控性。

## 研究问题

> 当标注定义与模型内部已经形成的概念边界不一致时，定义说明和 few-shot 示例在多大程度上能纠正模型判断？

## 分析框架卡片

| 维度 | 内容 |
|---|---|
| 被质疑的常见假设 | LLM 是服从 prompt 的通用标注器，只要定义清楚就会采用用户标准 |
| 研究对象 | LLM-as-Annotator / Judge、内部概念先验和提示干预 |
| 关键变量 | Definition-Specific Familiarity、定义对齐程度、示例与原始决策 |
| 对照因素 | 文本熟悉度、数据集层混杂和不同提示设置 |
| 主要诊断指标 | 标注性能、DSF 相关性、提示纠错效果和 decision stickiness |
| 核心发现 | 概念定义的内部熟悉度比简单文本相似或记忆更能解释表现 |
| 行为边界 | 与内部先验冲突的决策不一定能被新增定义或 few-shot 稳定翻转 |
| 结论边界 | 不直接覆盖参数微调、所有任务类型或开放式 Agent 长程行为 |

---
""".strip()

BLOCKS = {
    "agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md": (ACE, True),
    "evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md": (EVOLVER, True),
    "position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md": (TOA, False),
    "self-challenging-language-model-agents.md": (SELF_CHALLENGING, False),
    "godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md": (GODEL, False),
    "from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md": (SURVEY, True),
    "mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md": (MLEVOLVE, False),
    "on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md": (LIMITS, False),
}


def insert_block(text: str, block: str, after_resources: bool) -> str:
    if "## 30 秒读懂" in text:
        raise RuntimeError("quick-reading section already exists")
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


def update_date(text: str) -> str:
    comment_end = text.find("-->")
    head, tail = text[:comment_end], text[comment_end:]
    head, count = re.subn(r"(?m)^  updated: '[^']*'$", f"  updated: '{UPDATED}'", head, count=1)
    if count != 1:
        raise RuntimeError("metadata updated field not found")
    return head + tail


def ensure_reference_heading(path: Path, text: str) -> str:
    if re.search(r"(?m)^## .*参考资料", text):
        return text
    pattern = re.compile(r"(?m)^## (?P<num>\d+\.\s*)?参考(?:信息|链接)(?P<rest>.*)$")
    match = pattern.search(text)
    if match:
        num = match.group("num") or ""
        return text[: match.start()] + f"## {num}参考资料与链接" + text[match.end() :]

    metadata = parse_metadata_file(path).metadata
    links = []
    for label, field in (
        ("arXiv", "arxiv_url"),
        ("PDF", "pdf_url"),
        ("HTML", "html_url"),
        ("项目页", "project_url"),
        ("代码", "code_url"),
        ("资源列表", "resource_url"),
        ("模型", "model_url"),
    ):
        value = metadata.get(field)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            links.append(f"- {label}：<{value}>")
    return text.rstrip() + "\n\n---\n\n## 参考资料\n\n" + "\n".join(links) + "\n"


def update_ci() -> None:
    path = ROOT / ".github" / "workflows" / "validate-notes.yml"
    text = path.read_text(encoding="utf-8")
    old = "python scripts/validate_notes.py . --require-schema"
    new = "python scripts/validate_notes.py . --require-schema --require-structure --strict"
    if old not in text:
        raise RuntimeError("validation command not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def update_docs() -> None:
    path = ROOT / "docs" / "maintenance-tooling.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- “30 秒读懂”和机制卡片等正文结构暂时只报告 warning，Stage 4 完成后再设为强制要求。",
        "- 全部笔记已具备“30 秒读懂”、论文定位、研究问题和适用的机制 / 分析卡片；",
    )
    text = text.replace(
        "python scripts/validate_notes.py . --require-schema\n```\n\n这会强制所有笔记使用 schema 1.0，同时继续把尚未完成的正文结构迁移报告为 warning。",
        "python scripts/validate_notes.py . --require-schema --require-structure --strict\n```\n\n这会同时强制 schema 1.0、统一正文入口，并把所有 warning 视为失败。",
    )
    text = text.replace(
        "当前检查但不阻塞：",
        "当前强制检查：",
    )
    text = text.replace(
        "\n传入 `--require-structure` 后，这些项目会变成 error。",
        "",
    )
    text = text.replace(
        "python scripts/validate_notes.py . --require-schema\npython scripts/check_links.py .",
        "python scripts/validate_notes.py . --require-schema --require-structure --strict\npython scripts/check_links.py .",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    expected = set(BLOCKS)
    actual = {path.name for path in NOTES.glob("*.md") if "## 30 秒读懂" not in path.read_text(encoding="utf-8")}
    if actual != expected:
        raise RuntimeError(f"remaining note set mismatch: expected={sorted(expected)}, actual={sorted(actual)}")

    for name, (block, after_resources) in BLOCKS.items():
        path = NOTES / name
        text = path.read_text(encoding="utf-8")
        text = insert_block(text, block, after_resources)
        text = update_date(text)
        text = ensure_reference_heading(path, text)
        path.write_text(text, encoding="utf-8")

    update_ci()
    update_docs()
    print(f"Updated {len(BLOCKS)} remaining notes and enabled strict structure validation")


if __name__ == "__main__":
    main()
