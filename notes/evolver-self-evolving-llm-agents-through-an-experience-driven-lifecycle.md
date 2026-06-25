<!--
metadata:
  schema_version: '1.0'
  title: 'EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle'
  short_title: 'EvolveR'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'method'
  paper_status: 'accepted'
  venue: 'ICML 2026'
  venue_track: ''
  evolution_object: 'Experience Base / Executor Policy'
  learning_stage: 'mixed'
  parameter_update: 'yes'
  cross_task: 'yes'
  arxiv_id: '2510.16079'
  arxiv_version: 'v3'
  arxiv_url: 'https://arxiv.org/abs/2510.16079'
  pdf_url: 'https://arxiv.org/pdf/2510.16079'
  html_url: 'https://arxiv.org/html/2510.16079v3'
  project_url: ''
  code_url: 'https://github.com/KnowledgeXLab/EvolveR'
  original_code_url: 'https://github.com/Edaizi/EvolveR'
  resource_url: ''
  model_url: 'https://huggingface.co/Edaizi/EvolveR'
  code_status: 'official_available'
  model_status: 'official_available'
  first_submitted: '2025-10-17'
  last_revised: '2026-05-16'
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-24'
  authors:
    - 'Rong Wu'
    - 'Xiaoman Wang'
    - 'Jianbiao Mei'
    - 'Pinlong Cai'
    - 'Daocheng Fu'
    - 'Cheng Yang'
    - 'Licheng Wen'
    - 'Xuemeng Yang'
    - 'Yufan Shen'
    - 'Yuxin Wang'
    - 'Botian Shi'
  institutions:
    - 'Zhejiang University'
    - 'Shanghai Artificial Intelligence Laboratory'
    - 'East China Normal University'
    - 'Fudan University'
    - 'Central South University'
    - 'Shanghai Innovation Institute'
    - 'Shanghai Jiao Tong University'
    - 'University of Science and Technology of China'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Experience Base'
    - 'Agent Memory'
    - 'Experience Self-Distillation'
    - 'Experience Retrieval'
    - 'GRPO'
    - 'Policy Evolution'
    - 'Search Agent'
  tags:
    - 'self-evolving-agent'
    - 'experience-base'
    - 'agent-memory'
    - 'self-distillation'
    - 'experience-retrieval'
    - 'grpo'
    - 'search-agent'
    - 'icml-2026'
  related_notes:
    - 'notes/harness-updating-is-not-harness-benefit.md'
  created: '2026-06-05'
  updated: '2026-06-25'
-->

# 《EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle》读书笔记

> 论文：**EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle**  
> arXiv：<https://arxiv.org/abs/2510.16079>  
> PDF 下载地址：<https://arxiv.org/pdf/2510.16079>  
> arXiv HTML：<https://arxiv.org/html/2510.16079v3>  
> 官方代码仓库：<https://github.com/Edaizi/EvolveR>，当前会跳转到 <https://github.com/KnowledgeXLab/EvolveR>  
> 模型权重：<https://huggingface.co/Edaizi/EvolveR>  
> 当前状态：arXiv v3，最后修订时间为 2026-05-16；arXiv 页面备注为 **Accepted by ICML 2026**。

---


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

## 与相邻路线的关系

### 2.1 所属研究方向

这篇论文属于 **Self-Evolving LLM Agents**，也可以放在更大的 **LLM Agent Memory + Reinforcement Learning** 方向里。

它关心的不是“模型有没有外部知识”，而是：

> Agent 做完任务之后，能不能把自己的成功经验和失败教训沉淀下来，并且在后续任务里真正用起来？

这和普通 RAG 的区别很重要：

- RAG 主要解决 **外部知识缺失**，例如不知道某个事实就去搜索；
- EvolveR 想解决的是 **问题解决策略缺失**，例如不知道遇到某类问题时应该先查什么、怎么验证、如何避免常见错误。

所以 EvolveR 的经验库不是百科知识库，而更像是一个 **策略原则库**。

### 2.2 在方向里的定位

EvolveR 在 self-evolving agent 方向里的定位可以概括为一句话：

> 它把“经验存储”推进到了“经验抽象 + 经验检索 + 策略训练”的闭环。

过去很多 Agent 记忆机制大致停留在下面几种形式：

1. **Stateless Execution**：每次任务做完就丢掉轨迹，下次从零开始。
2. **Raw Trajectory Retrieval**：把过去完整轨迹存起来，下次遇到相似任务直接拿来参考。
3. **External Scribing**：用一个更强的外部模型替 Agent 总结经验或反思。
4. **EvolveR**：Agent 自己从轨迹中提炼原则，并且通过 RL 学会在后续任务中检索和使用这些原则。

> 图源：论文 arXiv HTML Figure 1；仅用于读书笔记引用和学习说明。

![Figure 1: Four major paradigms for LLM agent learning](https://arxiv.org/html/2510.16079v3/x1.png)

图 1 很适合用来理解 EvolveR 的定位：它不是简单保存历史轨迹，也不是依赖外部老师写反思，而是让 Agent 自己从交互轨迹中抽象原则，再在后续任务中检索原则并通过 RL 更新策略。

这篇论文的核心贡献不是“我多加了一个 memory”，而是把 memory 放进了一个可循环的生命周期里：

```text
在线交互生成轨迹
    ↓
离线自蒸馏，把轨迹总结成原则
    ↓
维护经验库：去重、合并、打分、过滤
    ↓
新任务中检索经验原则并辅助推理
    ↓
根据任务结果用 RL 更新策略
    ↓
继续生成更好的轨迹和经验
```

因此，它比较像是 self-evolving agent 方向的一篇“框架型论文”。

---

## 问题背景：操作性遗忘、轨迹抽象与认知对齐

论文要解决的问题可以拆成三层。

### 3.1 第一层：Agent 的“操作性遗忘”

很多 LLM Agent 可以在单个任务中表现不错，例如调用搜索工具、做多步推理、最终回答问题。

但问题是：

> 它做完一次任务之后，并不会真正吸收这次任务的经验。

比如它今天犯了一个错误：只查了 A，没有查 B，导致比较类问题回答错了。明天遇到类似问题，它仍然可能重复同样错误。

这就是论文里说的 **operational amnesia**，可以理解为“操作层面的失忆”。

### 3.2 第二层：只存原始轨迹不够

一个直接想法是：把过去的任务轨迹都存下来，下次遇到类似任务就检索过去案例。

但原始轨迹有几个问题：

- 太长，检索和阅读成本高；
- 和具体问题强绑定，泛化性差；
- 容易让 Agent 模仿表面步骤，而不是理解背后的策略；
- 错误轨迹如果处理不好，还可能污染后续行为。

所以论文认为，关键不是“存更多轨迹”，而是从轨迹里抽象出 **可复用的原则**。

### 3.3 第三层：外部老师总结经验也不一定最好

另一种做法是让一个更强的外部模型帮忙总结经验。

这看起来合理，但论文提出一个很有意思的点：

> 更强的老师总结出来的原则，不一定最适合当前这个 Agent 使用。

原因是不同模型的能力边界、常见错误、推理风格不同。一个强模型觉得显然的策略，小模型可能不一定执行得好。相反，Agent 自己根据自己的成功和失败总结出来的经验，可能更贴近它自己的能力和错误模式。

论文把这个现象称为 **cognitive alignment**，可以理解为：

> 经验原则要和执行者自己的认知方式、能力边界、错误模式对齐。

---

## 4. 核心概念解释

### 4.1 Trajectory：交互轨迹

Trajectory 是 Agent 做一个任务时产生的完整过程，包括：

- 任务问题；
- 中间思考；
- 是否检索经验；
- 是否检索外部知识；
- 搜索到的信息；
- 最终答案；
- 成功或失败结果。

在 EvolveR 中，轨迹不是终点，而是下一轮经验蒸馏的原材料。

### 4.2 Principle：经验原则

Principle 是从轨迹里总结出来的抽象策略。它不是事实知识，而是“遇到某类问题应该怎么做”的规则。

例如论文中的例子类似于：

```text
对于比较类问题，在下结论前要分别收集两个对象的信息。
```

一个 principle 通常包括两部分：

1. **自然语言描述**：一句可读的策略或警告；
2. **结构化三元组**：把策略表示成若干 `(subject, predicate, object)` 形式，方便组织和检索。

### 4.3 Experience Base：经验库

Experience Base 可以理解为 Agent 的“策略笔记本”。

它不是简单 append-only 的日志库，而是有维护机制：

- 新原则要和已有原则做相似度检索；
- 相似原则要进一步用模型判断语义是否等价；
- 重复原则合并，不重复原则新增；
- 每条原则记录使用次数和成功次数；
- 低分原则会被过滤或剪枝。

所以 Experience Base 的重点是 **curation**，也就是持续整理，而不是无脑堆积。

### 4.4 `<search_experience>`：搜索内部经验

EvolveR 给 Agent 增加了一个动作：

```text
<search_experience>
```

这个动作的作用是从内部 Experience Base 中检索相关原则。

这和普通搜索动作不同：

- `<search_knowledge>` 搜的是外部事实知识；
- `<search_experience>` 搜的是内部经验原则。

可以这样理解：

```text
search_knowledge   = 查资料
search_experience  = 翻自己的错题本/经验本
```

### 4.5 Policy Evolution：策略演化

EvolveR 不只是在 prompt 里塞经验，它还通过强化学习更新模型策略。

这一步的意义是：

> 让模型不只是“看到经验”，而是逐渐学会什么时候该查经验、怎么用经验、用完经验后怎么继续查知识和回答。

论文使用的是 **GRPO**，奖励包括两部分：

1. **Outcome Reward**：最终答案是否正确；
2. **Format Reward**：推理过程格式是否合理，例如是否包含必要的 `<think>`、`<search_experience>`、`<search_knowledge>`、`<answer>` 等结构。

---

## 5. 方法设计

### 5.1 整体生命周期

EvolveR 的整体框架由三个环节组成。

> 图源：论文官方代码仓库 README / assets/framework.png，对应论文 Figure 2；仅用于读书笔记引用和学习说明。

![Figure 2: Overview of the EvolveR experience lifecycle](https://raw.githubusercontent.com/KnowledgeXLab/EvolveR/main/assets/framework.png)

图 2 是理解 EvolveR 方法最关键的一张图：左侧是 online phase 与 offline phase 交替运行的闭环；右上角展示 `<search_experience>` 如何从经验库中检索带分数的原则；右下角展示经验库如何通过 distill、deduplicate、update、filter 等操作持续维护。

#### 环节一：Offline Experience Self-Distillation

离线阶段，模型参数冻结。系统读取之前在线交互产生的轨迹，然后让 Agent 自己扮演“专家分析者”，从成功和失败轨迹中总结原则：

- 成功轨迹：总结 guiding principle，告诉以后应该怎么做；
- 失败轨迹：总结 cautionary principle，告诉以后要避免什么坑。

这里的关键是 **self-distillation**：不是外部老师来总结，而是 Agent 自己总结。

#### 环节二：Experience Base Maintenance

蒸馏出来的原则不会直接全部写进经验库，而是经过维护流程：

1. **去重**：同一个问题可能采样出多条类似轨迹，先去掉重复原则；
2. **相似检索**：用 embedding 找到经验库中最相似的已有原则；
3. **语义判断**：再让模型判断两个原则是否表达同一个核心含义；
4. **合并或新增**：等价就合并轨迹，不等价就作为新原则加入；
5. **动态打分**：根据原则被使用后的成功率更新分数；
6. **低分过滤**：分数过低的原则会被剪掉。

这套机制的意义在于控制经验库质量。如果没有这些步骤，经验库会越来越大，也会越来越脏。

#### 环节三：Online Interaction + RL Update

在线阶段，Agent 面对新任务时可以执行三类动作：

```text
<search_experience>  搜索内部经验原则
<search_knowledge>   搜索外部知识
<answer>             给出最终答案
```

Agent 在解题过程中先思考，再根据需要查经验、查知识，最后回答。在线阶段产生的新轨迹又会成为下一轮离线蒸馏的材料。

最后，系统用 GRPO 根据这些轨迹更新模型策略，形成闭环。

### 5.2 这篇论文真正新在哪里

我觉得它的新意不在某一个单独模块，而在 **模块之间形成闭环**：

```text
经验不是只存储，而是被抽象；
经验不是只抽象，而是被检索；
经验不是只检索，而是影响行动；
行动不是只完成任务，而是产生新轨迹；
新轨迹不是只用于评估，而是继续训练策略和更新经验库。
```

这和普通 Agent memory 的差别很大。普通 memory 更像“外挂提示”，EvolveR 更像“训练一个会使用自己经验本的 Agent”。

---

## 6. 实验设计

### 6.1 模型

论文实验基于 **Qwen2.5** 系列模型，包括：

- Qwen2.5-0.5B；
- Qwen2.5-1.5B；
- Qwen2.5-3B；
- Qwen2.5-7B。

其中很多消融实验主要围绕 Qwen2.5-3B 展开，主结果表中也给出了 3B 和 7B 的结果。

### 6.2 数据集

论文把数据集分成域内和域外。

| 类型 | 数据集 | 作用 |
|---|---|---|
| 域内 | Natural Questions, HotpotQA | 用训练集构建经验库，并用于评测 |
| 域外 | TriviaQA, PopQA, 2WikiMultiHopQA, MuSiQue, Bamboogle | 只用于泛化评测 |

这个设置比较重要，因为作者想证明 EvolveR 学到的不是某个数据集的固定答案，而是能迁移到其他复杂问答任务的策略。

### 6.3 对比方法

论文对比了三类基线。

第一类是 **prompting / retrieval 方法**：

- Direct Inference；
- Chain-of-Thought；
- IRCoT；
- Search-o1；
- RAG。

第二类是 **监督微调方法**：

- SFT；
- Rejection Sampling。

第三类是 **RL agent 方法**：

- R1-base；
- R1-instruct；
- Search-R1-base；
- Search-R1-instruct。

这些 baseline 覆盖了“直接回答”“显式推理”“外部检索”“静态专家数据学习”“基于轨迹反馈的 RL 搜索 Agent”等不同路线。

### 6.4 评价指标

主指标是 **Exact Match (EM)**，即预测答案和标准答案经过标准化后是否完全一致。

论文也在模型规模泛化分析中报告了 F Score，因为复杂问答任务可能存在别名或多个可接受答案。主表仍然用 EM，便于和已有工作直接对比。

### 6.5 训练实现

实验实现上有几个值得注意的工程点：

1. 先做 **cold-start**，用少量格式正确的 CoT 交互轨迹让模型学会基本输出格式；
2. cold-start 数据来自 NQ 和 HotpotQA 的约 700 个样本；
3. SFT 阶段使用 **LLaMA-Factory** 和 LoRA；
4. 后续策略优化使用 **GRPO**；
5. 训练实现依赖 **verl**；
6. 论文实验使用 **8 张 A100 GPU**；
7. 代码仓库还包含 embedding server、local retrieval server、experience vector database 等工程组件。

这说明 EvolveR 不是一个轻量 prompt trick，而是一个训练和检索系统。

---

## 7. 主要实验结论

### 7.1 EvolveR 在主结果上超过强 baseline

在 Qwen2.5-3B 上，EvolveR 的平均 EM 为 **0.382**，超过 Search-R1-instruct 的 **0.325**。

在 Qwen2.5-7B 上，EvolveR 的平均 EM 为 **0.417**，超过 Search-R1-instruct 的 **0.385**。

这说明在搜索增强 QA 场景中，仅仅训练模型会用搜索工具还不够；如果能让模型同时检索和利用自己的经验原则，效果会更好。

### 7.2 模型越大，EvolveR 效果越明显

论文报告 EvolveR 在不同规模模型上的平均表现呈上升趋势：

```text
Qwen2.5-0.5B  → 0.150
Qwen2.5-1.5B  → 0.270
Qwen2.5-3B    → 0.382
```

> 图源：论文 arXiv HTML Figure 4；仅用于读书笔记引用和学习说明。

![Figure 4: Performance of EvolveR across various model scales](https://arxiv.org/html/2510.16079v3/img/evolver_scaling_results.png)

图 4 用更直观的方式说明：EvolveR 并不是只对某一个模型规模有效，而是在 0.5B、1.5B、3B 上表现出比较一致的规模趋势。模型越强，越能理解、筛选并执行经验原则，因此经验库的收益也更明显。

这说明 EvolveR 比较依赖基础模型的推理能力和指令遵循能力。经验库给了原则，但模型还得能理解原则、判断原则是否适用、把原则转化为具体行动。

### 7.3 自蒸馏不一定弱于外部老师

论文做了一个很有价值的实验：把 EvolveR 的 self-distill 换成 teacher-distill，即用更强的 GPT-4o-mini 来总结经验。

结果很有意思：

| 模型 | self-distill 平均分 | teacher-distill 平均分 | 观察 |
|---|---:|---:|---|
| Qwen2.5-0.5B | 0.150 | 0.220 | 小模型自己总结能力弱，老师更有帮助 |
| Qwen2.5-1.5B | 0.270 | 0.290 | 老师略好 |
| Qwen2.5-3B | 0.382 | 0.370 | 自蒸馏反而更好 |

这个结果的启发是：

> 经验总结的质量不能只看“总结者强不强”，还要看总结出来的经验和执行模型是否对齐。

对 3B 模型来说，自己总结的原则可能更贴近自己的能力边界和常见错误，因此比外部老师总结的经验更好用。

### 7.4 经验检索非常关键

论文比较了完整 EvolveR 和去掉经验检索的版本。

在 Qwen2.5-3B 上：

```text
EvolveR                 0.382
EvolveR w/o exp-retrieve 0.340
```

在小模型上差距更大：

```text
Qwen2.5-0.5B: 0.150 → 0.078
Qwen2.5-1.5B: 0.270 → 0.123
```

这说明经验库不是训练时的装饰。推理时能不能检索并使用原则，是 EvolveR 成功的重要条件。

### 7.5 各模块是互补的

论文还做了组件级消融，在 Qwen2.5-3B 上结果大致是：

| Principle Distillation | Principle Retrieval | RL | Avg. Score |
|---|---|---|---:|
| No | No | No | 0.134 |
| No | No | Yes | 0.325 |
| Yes | Yes | No | 0.357 |
| Yes | No | Yes | 0.340 |
| Yes | Yes | Yes | 0.382 |

我的理解是：

- **RL 本身很有用**，从 0.134 提升到 0.325；
- **经验原则 + 检索也很有用**，即使没有 RL，也能到 0.357；
- **最强的是两者结合**，即 Agent 既能看到经验，也通过 RL 学会如何使用经验。

### 7.6 经验库质量确实需要维护

论文人工标注了 100 条经验原则，把它们分为：

- Ideal：正确且可执行；
- Vague：正确但太泛泛；
- Incorrect / Misleading：错误或误导。

高分原则和低分原则差别很明显：

| 分数层级 | Ideal | Vague | Incorrect / Misleading |
|---|---:|---:|---:|
| Low-Score | 26% | 50% | 24% |
| High-Score | 82% | 10% | 8% |

这说明动态打分和过滤是必要的。经验库如果不维护，会有大量“看起来正确但没什么用”的空泛原则。

### 7.7 经验库扩展后没有明显崩掉，但也不是无限增长越大越好

论文还观察了经验库规模和检索延迟、性能的关系。经验库接近 5 万条原则时，Top-3 检索延迟约 **0.20 秒**，没有形成严重瓶颈。

但性能在约 45k 条原则附近达到高点，继续增长到约 50k 时平均分从 **0.410** 降到 **0.387**。

这说明经验库规模扩大是可行的，但并不意味着经验越多越好。后续还是要关注噪声积累、过期经验、任务分布变化和检索相关性。

---

---

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

---

## 8. 工程启发

### 8.1 Agent 记忆应该存“原则”，不只是存“日志”

EvolveR 对工程系统最大的启发是：不要简单保存完整历史对话或轨迹。

更可行的方式是把轨迹压缩成可复用原则：

```text
原始轨迹：很长、具体、难泛化
经验原则：短、抽象、可迁移、便于检索
```

如果我要做一个自演化 Agent 系统，经验存储可以分三层：

1. 原始轨迹：用于追溯和再分析；
2. 摘要原则：用于在线检索和指导；
3. 统计分数：用于过滤和排序。

### 8.2 经验库必须有治理机制

经验库不是越大越好。应该至少包括：

- 去重；
- 合并；
- 版本管理；
- 使用次数统计；
- 成功率统计；
- 低质量经验删除；
- 过期经验处理。

这和数据治理很像。Agent memory 本质上也需要“数据清洗”。

### 8.3 检索内部经验和检索外部知识应该分开

EvolveR 把动作分成：

```text
<search_experience>  检索策略经验
<search_knowledge>   检索事实知识
```

这个设计很清晰。

在工程实现中，也可以把两个库完全分开：

- 外部知识库：文档、网页、百科、论文、代码；
- 内部经验库：失败原因、成功策略、工具调用模式、调试流程。

这样可以避免“事实知识”和“策略经验”混在一起。

### 8.4 仅仅把经验塞进 prompt 不够，模型还要学会使用经验

EvolveR 的 RL 部分提醒我：

> memory 的价值不只取决于 memory 写得好，还取决于模型是否会读、会判断、会执行。

这和 self-evolving agent 中的 harness benefit 问题是相通的。经验库写得很好，但如果 Task-Solver 不会使用，最终效果仍然有限。

### 8.5 经验不要轻易直接写进参数

论文附录里做了 experience internalization 实验，也就是让 retrieved experience tokens 参与训练损失，希望模型把经验“吸收到参数里”。结果表现略降。

这说明直接内化经验有风险，因为检索到的 top-k 原则不一定都和当前任务强相关。如果把噪声经验也写进参数，可能会产生负迁移。

工程上更稳的做法可能是：

1. 先把经验作为外部上下文使用；
2. 给经验加相关性和可信度过滤；
3. 只对高置信、高复用、高收益经验做更强的参数内化。

### 8.6 冷启动很重要

EvolveR 不是从完全空白开始自演化，而是先用少量格式正确的轨迹做 cold-start。

这说明自演化系统需要一个初始“行为规范”，否则早期轨迹太乱，后续蒸馏出来的经验也会很差。

类比到自己的 Agent 系统，可以先人工或用强模型构造少量高质量示例，让 Agent 学会基本格式和工具调用流程，再让它进入自我改进循环。

---

## 9. 局限性

### 9.1 主要验证在问答任务上

论文实验集中在复杂 QA 和多跳 QA。虽然这些任务能体现搜索、推理和经验复用，但还不能直接说明 EvolveR 在代码修复、网页操作、科研助理、机器人控制等更复杂场景中同样有效。

尤其是长期任务和真实软件工程任务中，轨迹更长、动作空间更复杂、反馈更延迟，经验原则的抽象和验证会更难。

### 9.2 自蒸馏质量受基础模型能力限制

论文自己也承认，蒸馏原则的质量和基础模型能力强相关。

小模型自蒸馏不如 teacher-distill，说明它可能总结不出好经验，甚至会总结出错误经验。

所以 EvolveR 对模型能力有门槛：

> 模型不仅要会做题，还要会复盘自己做题的过程。

这比普通推理能力要求更高。

### 9.3 经验原则可能空泛或错误

人工标注结果显示，低分原则中有大量 vague 原则，例如“要仔细阅读上下文”这类建议。

这类原则看起来正确，但对实际行动帮助不大。

因此经验库的质量控制仍然是核心问题，后续可以继续研究：

- 如何判断原则是否可执行；
- 如何判断原则适用于哪些任务；
- 如何防止错误原则被反复使用；
- 如何处理过时原则。

### 9.4 训练和系统成本不低

EvolveR 涉及：

- 冷启动 SFT；
- GRPO 训练；
- 外部知识检索；
- 内部经验检索；
- embedding server；
- local retrieval server；
- experience vector database；
- 离线蒸馏和经验库维护。

这套系统比普通 RAG 或 prompt-based agent 复杂很多。论文使用 8 张 A100 训练，说明复现和扩展都有一定门槛。

### 9.5 经验库和参数学习的关系还没有完全解决

当前 EvolveR 的经验主要作为上下文被检索使用，并没有很好地内化到参数中。

附录里的 exp-absorb 实验表现下降，说明“把经验写进模型参数”不是简单打开 loss mask 就能解决。

更理想的自演化 Agent 可能需要同时具备：

```text
短期经验：外部 memory / context
中期经验：高质量原则库
长期经验：可控的参数内化
```

EvolveR 已经把前两步做得比较清楚，但第三步仍然是开放问题。

---

## 10. 我的理解与总结

我对这篇论文的理解是：

> EvolveR 不是简单给 Agent 加一个记忆库，而是提出了一套“做任务—复盘—写经验—查经验—再训练”的闭环。

这篇论文最值得记住的点有三个。

第一，**经验要抽象成原则**。原始轨迹太具体，难以泛化。真正有价值的是从轨迹中抽出来的可执行策略。

第二，**经验库要被治理**。如果经验库没有去重、合并、打分、过滤，很快会变成一堆重复、空泛、甚至错误的规则。

第三，**模型要学会使用经验**。经验不是放在 prompt 里就自动有用。EvolveR 用 GRPO 让模型在训练中学习如何检索经验、如何结合外部知识、如何产生正确答案。

我觉得这篇论文可以和“Harness Updating Is Not Harness Benefit”一起看：

- Harness Updating 那篇提醒我们：写出更新和用好更新是两种不同能力；
- EvolveR 给出了一种系统实现：让 Agent 自己写经验，并通过 RL 学会用经验。

所以从研究路线看，self-evolving agent 可能正在从早期的“反思 prompt”走向更完整的系统范式：

```text
反思 / 记忆
    ↓
结构化经验库
    ↓
经验库治理
    ↓
经验检索增强推理
    ↓
基于轨迹反馈的策略训练
    ↓
持续自我演化
```

这对后续做组会汇报时也很有用。可以把 EvolveR 讲成一个核心问题：

> Agent 能不能像学生一样，不只做题，还会整理错题本，并且在下一次做题时真的用上错题本？

---

## 11. 后续值得继续追的问题

1. EvolveR 的经验原则如果迁移到代码修复任务，还能不能保持有效？
2. 经验库中的原则能否自动形成层次结构，例如从具体策略抽象成更高层 workflow？
3. self-distill 和 teacher-distill 能不能结合，而不是二选一？
4. 如何判断一条经验原则“适合当前模型”而不是只看它是否语义正确？
5. 经验何时应该外部检索，何时应该内化进参数？
6. 如果任务分布持续变化，旧经验如何遗忘或降权？
7. 能不能把这种 experience lifecycle 用到科研 Agent、代码 Agent、实验平台 Agent 中？

---

## 12. 组会汇报建议

如果要用这篇论文做一次组会，可以按下面逻辑讲。

### 12.1 一句话开场

> 这篇论文研究的是：LLM Agent 如何从自己的历史交互中总结经验，并在后续任务中通过检索经验和强化学习实现自我进化。

### 12.2 三页核心 PPT

第一页讲问题：

```text
现有 Agent 每次任务相互独立 → 做完就忘 → 不能持续积累策略经验
```

第二页讲方法：

```text
Online interaction → Offline self-distillation → Experience Base → Experience retrieval → GRPO policy evolution
```

第三页讲结论：

```text
EvolveR > Search-R1 等强 baseline；
self-distill 在 3B 上超过 teacher-distill；
去掉经验检索明显掉点；
经验库需要动态打分和过滤。
```

### 12.3 最值得讨论的问题

我觉得组会里最值得讨论的是：

> 自演化 Agent 的关键到底是“写经验”，还是“用经验”？

EvolveR 的答案是两者都重要，而且需要 RL 把它们连接起来。

---

---

## 论文外部信息

### 投稿与发表状态

这篇论文最早在 arXiv 上提交于 **2025 年 10 月 17 日**，编号为 **arXiv:2510.16079**，分类包括：

- **Computation and Language (cs.CL)**；
- **Artificial Intelligence (cs.AI)**。

截至本笔记记录时，arXiv 页面显示当前版本为 **v3**，最后修订于 **2026 年 5 月 16 日**，并且 comments 中写明：

> Accepted by ICML 2026

所以这篇论文不能只说是“普通 arXiv 预印本”，更准确的说法是：

> 这是一篇已经被 **ICML 2026** 接收的 self-evolving LLM agent 方向论文，arXiv 版本为公开稿。

如果后续正式引用，可以先采用 arXiv 给出的 BibTeX 形式，等 ICML 会议页面更新后再补充正式会议信息。

```bibtex
@misc{wu2025evolverselfevolvingllmagents,
  title={EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle},
  author={Rong Wu and Xiaoman Wang and Jianbiao Mei and Pinlong Cai and Daocheng Fu and Cheng Yang and Licheng Wen and Xuemeng Yang and Yufan Shen and Yuxin Wang and Botian Shi},
  year={2025},
  eprint={2510.16079},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2510.16079}
}
```

### 作者与机构

论文作者共 11 位，机构以 **上海人工智能实验室** 为中心，同时联合了浙江大学、华东师范大学、复旦大学、中南大学、上海创新研究院、上海交通大学、中国科学技术大学等单位。

| 作者 | 机构 |
|---|---|
| Rong Wu | Zhejiang University; Shanghai Artificial Intelligence Laboratory |
| Xiaoman Wang | East China Normal University |
| Jianbiao Mei | Zhejiang University; Shanghai Artificial Intelligence Laboratory |
| Pinlong Cai | Shanghai Artificial Intelligence Laboratory |
| Daocheng Fu | Shanghai Artificial Intelligence Laboratory; Fudan University |
| Cheng Yang | Shanghai Artificial Intelligence Laboratory; Central South University |
| Licheng Wen | Shanghai Artificial Intelligence Laboratory; Shanghai Innovation Institute; Shanghai Jiao Tong University |
| Xuemeng Yang | Shanghai Artificial Intelligence Laboratory |
| Yufan Shen | Shanghai Artificial Intelligence Laboratory |
| Yuxin Wang | University of Science and Technology of China |
| Botian Shi | Shanghai Artificial Intelligence Laboratory |

论文首页标注 **Rong Wu 和 Xiaoman Wang 为共同一作**，**Botian Shi 为通讯作者**。

### 作者背景和研究圈子观察

从作者机构和代码仓库来看，这篇论文主要来自 **Shanghai AI Lab / Knowledge Lab / KnowledgeXLab** 这一研究圈子。这个圈子的特点是：

1. **偏系统型 LLM Agent 研究**：不是只做单个 prompt 技巧，而是把工具调用、搜索、经验库、强化学习训练、模型权重发布放在一个系统里考虑。
2. **和知识驱动、检索增强、工具调用关系密切**：EvolveR 的任务场景是复杂问答和多跳问答，Agent 需要调用外部知识搜索，也需要调用内部经验搜索。
3. **有较强工程实现意识**：论文开源了代码，README 中给出了训练脚本、检索服务器、向量数据库、模型权重等内容，说明它不是纯概念论文。
4. **与自演化 Agent 方向靠得很近**：论文关注的是 Agent 如何从自己的轨迹中抽象经验，再把经验用于后续任务，并通过 RL 进一步让策略学会使用经验。

这篇文章所在的圈子，可以理解为：

```text
LLM Agent
├── Search Agent / Tool-use Agent
├── Agent Memory / Experience Base
├── Reinforcement Learning for Agent
└── Self-Evolving Agent
    └── Experience-driven lifecycle / Self-distillation / Policy evolution
```

如果和仓库中已有的《Harness Updating Is Not Harness Benefit》对比：

- Harness Updating 那篇更像是 **分析/诊断论文**，重点是拆解“写更新”和“用更新”两个能力；
- EvolveR 更像是 **方法/系统论文**，重点是提出一个完整生命周期，让 Agent 通过经验库和 RL 形成闭环自我改进。

---

## 参考资料

- arXiv：<https://arxiv.org/abs/2510.16079>
- PDF：<https://arxiv.org/pdf/2510.16079>
- HTML：<https://arxiv.org/html/2510.16079v3>
- 代码：<https://github.com/KnowledgeXLab/EvolveR>
- 模型：<https://huggingface.co/Edaizi/EvolveR>
