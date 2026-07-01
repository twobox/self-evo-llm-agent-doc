<!--
metadata:
  schema_version: '1.0'
  title: 'From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms'
  short_title: 'From Storage to Experience'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'survey'
  paper_status: 'accepted'
  venue: 'ACL 2026'
  venue_track: 'Findings'
  evolution_object: 'Agent Memory Taxonomy'
  learning_stage: 'not-applicable'
  parameter_update: 'not-applicable'
  cross_task: 'not-applicable'
  arxiv_id: '2605.06716'
  arxiv_version: 'v1'
  arxiv_url: 'https://arxiv.org/abs/2605.06716'
  pdf_url: 'https://arxiv.org/pdf/2605.06716'
  html_url: 'https://arxiv.org/html/2605.06716v1'
  project_url: ''
  code_url: ''
  original_code_url: ''
  resource_url: 'https://github.com/FeishuLuo/Evolving-LLM-Agent-Memory-Survey'
  model_url: ''
  code_status: 'not_applicable'
  model_status: 'not_applicable'
  first_submitted: '2026-05-07'
  last_revised: ''
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-24'
  authors:
    - 'Jinghao Luo'
    - 'Yuchen Tian'
    - 'Chuxue Cao'
    - 'Ziyang Luo'
    - 'Hongzhan Lin'
    - 'Kaixin Li'
    - 'Chuyi Kong'
    - 'Ruichao Yang'
    - 'Jing Ma'
  institutions:
    - 'Hong Kong Baptist University'
    - 'South China Normal University'
    - 'Hong Kong University of Science and Technology'
    - 'National University of Singapore'
    - 'University of Science and Technology Beijing'
  topics:
    - 'LLM Agent Memory'
    - 'Memory Mechanism Evolution'
    - 'Storage'
    - 'Reflection'
    - 'Experience'
    - 'Trajectory Preservation'
    - 'Trajectory Refinement'
    - 'Trajectory Abstraction'
    - 'Active Exploration'
    - 'Cross-Trajectory Abstraction'
    - 'Continual Learning'
  tags:
    - 'agent-memory'
    - 'survey'
    - 'taxonomy'
    - 'storage-reflection-experience'
    - 'experience-abstraction'
    - 'self-evolving-agent'
    - 'acl-2026-findings'
  related_notes:
    - 'notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md'
    - 'notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md'
    - 'notes/harness-updating-is-not-harness-benefit.md'
  created: '2026-06-10'
  updated: '2026-06-25'
-->

# 《From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms》读书笔记

> 论文：**From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms**  
> DOI：<https://doi.org/10.48550/arXiv.2605.06716>  
> arXiv：<https://arxiv.org/abs/2605.06716>  
> PDF 下载地址：<https://arxiv.org/pdf/2605.06716>  
> arXiv HTML：<https://arxiv.org/html/2605.06716v1>  
> 官方资源列表 / 论文列表：<https://github.com/FeishuLuo/Evolving-LLM-Agent-Memory-Survey>  
> 代码仓库：这是一篇综述论文，暂未找到单独实验代码；官方 GitHub 主要维护相关论文、benchmark 和资源列表。  
> 当前状态：arXiv:2605.06716v1，2026-05-07 提交；论文信息标注 **Accepted by ACL 2026 Findings**。

---

## 自己笔记

这篇综述主要讲的是大模型记忆的机制，就是要搞清楚“什么时候记、什么时候忘、什么时候反思、什么时候抽象、什么时候把外部经验内化为能力”。



Storage：轨迹保存方法：线性日志、向量数据库、结构化数据库、知识图谱等

> 但问题也明显：存得越多，噪声、错误、过期信息也越多，检索成本也会上升。

Reflection：对一次任务轨迹进行评价、纠错、压缩，把“这次哪里错了、下次应该怎么做”变成更高质量的记忆。

> 它认为 Reflection 仍然太依赖单次任务上下文，容易变成“这次任务的教训”，而不是可迁移的能力。

Experience：跨多条轨迹做抽象，把很多相似成功或失败经历压缩成更通用的规则、技能、策略，甚至内化到模型参数中。

> 从“我记得某次怎么做”变成“我学会了这一类问题该怎么做”。这是文章标题里 From Storage to Experience 的真正含义。



一个很有价值的区分是 Reflection 和 Experience 的区别。Reflection 是 intra-trajectory transformation，即对**单条轨迹做修正**；Experience 是 inter-trajectory induction，即从**多条轨迹中归纳规则**。前者回答“这次我哪里做错了”，后者回答“这一类情况通常应该怎么处理”。所以 Experience 不只是更高级的总结，而是记忆机制从“检索过去”变成“指导未来”的关键一步。

记忆机制为什么必须演化？作者说有三个驱动力。第一是长程一致性，Agent 要在长任务里保持状态、目标和行为一致；第二是动态环境，现实世界里的知识会过期，因果关系也会延迟显现，所以静态记忆不够；第三是持续学习，Agent 不能永远重复试错，必须把交互经验转化成可复用知识。

这篇 survey 实际上在反对一种“记忆 = 向量库 + 检索”的狭窄理解。它认为未来 Agent memory 的核心问题不是如何无限扩容，而是如何管理记忆生命周期：**什么时候记、什么时候忘、什么时候反思、什么时候抽象、什么时候把外部经验内化为能力**。这个视角比普通 memory survey 更接近“自进化 Agent”的问题。



这篇文章最有价值的地方是给了一个判断 Agent 记忆系统成熟度的框架：低级系统只会存历史，中级系统会从历史中纠错，高级系统会从多次历史中抽象经验，并用这些经验主动探索和改进行为。



什么时候记、什么时候忘、什么时候反思、什么时候抽象、什么时候把外部经验内化为能力?

**“什么时候记”**：对应的是 memory acquisition，也就是哪些信息值得进入记忆。不是所有交互都该记。值得记的通常有几类：用户长期偏好、任务目标、环境状态变化、失败原因、成功策略、罕见但高价值的观察、会影响后续决策的约束。反过来，过程噪声、一次性中间步骤、可随时重新获取的信息、低置信度猜测，就不一定该进入长期记忆。这里的关键是：记忆不应该以“发生过”为标准，而应该以“未来是否会改变决策”为标准。

**“什么时候忘”**：，其实比“什么时候记”更高级。很多 Agent memory 系统的问题不是记得太少，而是记得太多、太旧、太脏。过期信息如果还被检索出来，会比没有记忆更危险，因为它看起来相关，但实际已经不适用。比如用户以前说“我偏好 A 方法”，后来项目目标变了，继续调用旧偏好就会误导 Agent。所以忘记不是删除能力，而是维护记忆质量。它包括过期、降权、合并、覆盖、归档、标记不确定性。一个好的系统不是永远记住，而是让旧记忆逐渐失去行动支配权。

**“什么时候反思”**，发生在一次任务完成之后，尤其是成功/失败结果已经显现之后。反思不是普通总结，而是把轨迹里的因果关系提炼出来：为什么成功？为什么失败？哪个假设错了？哪个检索有用？哪个步骤浪费？下次遇到类似情况要改变什么？所以反思的对象不是事实本身，而是“行动—结果”之间的关系。它把原始经历变成可复用教训。没有反思，记忆只是日志；有了反思，记忆才开始变成经验的原材料。

**“什么时候抽象”**，是在积累了多次相似经历之后。单次失败之后生成的反思，可能只是偶然教训；多次轨迹中反复出现的模式，才值得抽象成经验。比如 Agent 多次发现“用户问论文精华时，不想要普通摘要，而想要可讨论的核心洞见”，这就可以从单次反思上升为一个更稳定的策略：论文交流场景中，优先讲研究问题、框架价值、关键区分、可追问点，而不是逐段摘要。抽象的本质是从“某一次怎么做”提升到“这一类问题怎么做”。

**“什么时候把外部经验内化为能力”**，这是最高层。外部记忆还需要检索、选择、放进上下文；内化后的能力则变成 Agent 的默认行为倾向。比如一开始 Agent 需要查一条记忆：“回答论文问题要先看 metadata.yaml 和 paper.md”；但如果这种规则长期稳定、频繁使用、低争议，就可以内化成工作习惯。对应到系统实现上，可能是 prompt policy、工具调用策略、技能库、程序化流程，甚至微调后的模型参数。这里的关键判断是：如果某条经验稳定、通用、频繁、收益高、风险低，就更适合内化；如果它临时、个性化、易变、有上下文依赖，就更适合保留为外部记忆。

> 一条链路：记，是把有未来价值的信息留下；忘，是防止旧信息污染未来；反思，是从一次经历中提取教训；抽象，是从多次经历中归纳模式；内化，是把稳定模式变成默认能力。

>  Memory should be governed by decision impact, temporal validity, causal feedback, abstraction stability, and internalization cost.
>
> 记忆系统要根据决策影响、时效性、因果反馈、抽象稳定性和内化成本来管理，而不是简单按相似度检索历史。

作者认为现在的研究**已经推进到 Experience 的早期阶段**，但整体还处于探索期，Storage 和 Reflection 相对更成熟，Experience 是当前最前沿、最不稳定、也最有潜力的方向。

> 证据是：Experience 方向作为一个连贯研究方向主要是在 2025 年下半年才开始形成；现有 benchmark 主要还是评估 Storage 和 Reflection，比如检索、去噪、记忆保持，而对 Experience 阶段的“抽象能力”和“泛化能力”评估明显不足；另外很多 Experience 相关工作还是近期预印本，尚未完全经过正式同行评审。

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

## 与相邻路线的关系

这篇论文属于以下几个方向：

1. **LLM Agent Memory**：Agent 如何保存、组织、检索和利用历史交互信息。
2. **Self-Evolving / Self-Improving Agent**：Agent 如何从过去任务中提取经验，并影响后续行为。
3. **Experience-based Agent**：经验不只是 raw log，而是从多条轨迹中归纳出的规则、技能、策略或参数化能力。
4. **Continual Learning for Agents**：在长期任务流和动态环境中，Agent 如何持续适应而不是每次从零开始。
5. **Agent Memory Survey / Taxonomy**：它不是提出单个新算法，而是给相关研究建立统一分类框架。

在本仓库的脉络中，它可以被看作一篇“总纲型综述”：

- **EvolveR** 的 experience base、自蒸馏经验原则、GRPO 训练，可以放到 Experience / Hybrid Experience 视角下理解。
- **ACE** 的 playbook 和 context items，可以看成显式经验与上下文资产治理。
- **SE-Agent** 的测试时轨迹池优化，更偏 Storage / Reflection / test-time trajectory optimization，还不一定形成长期跨任务经验。
- **Harness Updating Is Not Harness Benefit** 提醒我们：写入 memory / skill / workflow 不等于后续 agent 能真正用好这些更新。

---

## 三个分类问题

这篇综述想回答三个问题：

1. **为什么 Agent 需要记忆机制演化？**  
   因为 LLM 本身是近似无状态的，长程任务中容易出现重复探索、推理断裂、错误累积，动态环境中还会遇到记忆过期、因果关系变化、历史经验污染等问题。

2. **记忆机制是如何演化的？**  
   论文提出三阶段路径：**Storage** 保存轨迹，**Reflection** 反思和清洗轨迹，**Experience** 从多条轨迹中抽象出更高层经验。

3. **Experience 阶段带来了什么新变化？**  
   Experience 不再满足于“把过去拿出来参考”，而是强调 **主动探索** 和 **跨轨迹抽象**，让 agent 形成可迁移的策略先验。

---

## 5. 方法框架：Storage → Reflection → Experience

论文最重要的贡献，是把 LLM Agent memory 的发展形式化为三个抽象层次。

### 5.1 LLM Agent Memory 的基本定义

论文把 LLM-based agent 看成一个与动态环境交互的决策实体。Agent 在每一步接收观察、从记忆模块中检索相关信息，然后把系统指令、当前上下文和检索到的记忆一起送入模型生成动作。

这里有一个关键区分：

- **global memory repository**：长期存在的全局记忆库。
- **retrieved memory at time t**：某一步真正被取出并进入上下文的记忆片段。

这个区分很重要。很多讨论会把“记忆库里存了什么”和“这次推理实际用了什么”混在一起，但工程上这两个问题完全不同：前者是写入和管理，后者是检索、压缩和上下文组织。

### 5.2 Storage：轨迹保存

**Storage** 是最基础的阶段，目标是保存历史交互轨迹。论文把轨迹理解为按时间排列的 observation-action pairs，即任务执行过程中 agent 看到什么、做了什么。

Storage 阶段的典型形态：

| 类型 | 核心思路 | 优点 | 问题 |
|---|---|---|---|
| Linear storage | 把历史按时间顺序保存，类似长上下文或 FIFO 日志 | 简单、忠实 | 容量受限，噪声多，检索粗糙 |
| Vector storage | 把轨迹或摘要 embedding 到向量空间，按相似度检索 | 容量更大，适合语义检索 | 相似不等于有用，容易检索到过期或错误经验 |
| Structured storage | 用数据库、层级结构、图结构等组织记忆 | 可解释、可约束、可局部更新 | 建模成本高，需要设计 schema 和维护策略 |

我的理解：Storage 解决的是“不要忘记发生过什么”，但还没有解决“哪些记忆值得相信、值得保留、值得迁移”。

### 5.3 Reflection：轨迹修正与提纯

**Reflection** 解决 Storage 的一个核心缺陷：原始轨迹中充满失败尝试、幻觉、无效动作和偶然成功。如果全部照单全收，记忆库会越来越脏。

Reflection 阶段把 memory 从被动记录器变成主动批评者。它会对完成后的轨迹进行评价、纠错、摘要、提纯，再把更高质量的 memory unit 写回记忆库。

论文把 Reflection 分成三类：

| 类型 | 反馈来源 | 典型作用 |
|---|---|---|
| Introspection | LLM 自身知识和自我批评 | 找出推理错误、压缩长轨迹、维护 memory lifecycle |
| Environment | 外部环境、执行结果、reward、verification | 用真实反馈校准记忆，减少幻觉和错误策略 |
| Coordination | 多 agent 协作、角色分工、共识机制 | 用群体反思克服单个模型认知瓶颈 |

我的理解：Reflection 的关键是“单条轨迹内部的质量提升”。它通常还是围绕某一次任务或某条执行路径做修正，并不一定能抽象出跨任务通用经验。

### 5.4 Experience：跨轨迹经验抽象

**Experience** 是论文认为更前沿、更接近 self-evolving agent 的阶段。它不再只是修正一条轨迹，而是从多条相似或相关轨迹中归纳出稳定模式。

论文强调：Experience 的本质是 **cross-trajectory abstraction**。也就是说，agent 不只是记住“上次怎么做”，而是归纳出“这一类任务应该怎么做”。

Experience 可以有三种形态：

| 类型 | 经验形态 | 例子 | 优点 | 风险 |
|---|---|---|---|---|
| Explicit experience | 人类可读、可编辑的规则、策略、skill、library | 经验原则、prompt list、skill library、程序函数 | 可解释、易维护、可直接检索 | 仍有检索延迟和上下文占用 |
| Implicit experience | 模型参数、latent state、内部能力 | fine-tuning、RL、latent memory | 推理时负担小，更像“内化能力” | 更新成本高，可解释性弱，可能遗忘 |
| Hybrid experience | 显式经验库 + 周期性内化 | 先积累经验，再蒸馏 / RL 到模型中 | 兼顾灵活性和内化能力 | 系统复杂，容易出现同步和版本问题 |

我的理解：这里的 Experience 已经很接近我们关心的 **经验库、自蒸馏、策略库、skill library、长期自演化**。如果一篇论文只是把历史轨迹存进向量库，它还只是 Storage；如果它从成功和失败轨迹中总结可迁移原则，并在后续任务中复用或训练进模型，才更接近 Experience。

---

## 6. 关键图表

### 6.1 记忆机制演化总图

![Overview of the LLM agent memory mechanisms](https://arxiv.org/html/2605.06716v1/x1.png)

图源：arXiv HTML，Figure 1。  
这张图最适合作为组会讲解开场图：左边是 LLM Agent workflow，中间是 Storage → Reflection → Experience 的主路径，右边把 Experience 拆成 explicit、implicit、hybrid 三种形式。

### 6.2 跨轨迹抽象

![Overview of Cross-Trajectory Abstraction](https://arxiv.org/html/2605.06716v1/x3.png)

图源：arXiv HTML，Figure 3。  
这张图解释了 Experience 阶段为什么不是普通记忆检索：多条 trajectory group 经过 contrastive induction、action distillation、code encapsulation、gradient internalization 等方式，变成不同抽象层级的经验。

---

## 7. 论文中的核心驱动力

论文认为 LLM Agent memory 之所以从 Storage 走向 Reflection 和 Experience，主要有三个驱动力。

### 7.1 Long-range consistency

长程一致性是最早的驱动力。Agent 做多步任务时，如果没有记忆，就容易重复探索、忘记之前已经验证过的事实、在中途改变目标，或者把局部推理错误不断放大。

Storage 阶段主要回应这个问题：至少要保存历史，让 agent 有机会恢复上下文。

### 7.2 Dynamic environments

真实环境是动态的，记忆会过期，因果关系会变化，用户偏好和任务状态也会变化。因此记忆不能只增长，还要会评价、更新、删除、衰减和重组。

Reflection 阶段主要回应这个问题：把记忆从“静态仓库”升级成“可维护资产”。

### 7.3 Continual learning

如果 agent 要长期变强，就不能只保存历史，而要把历史经验变成可迁移能力。否则记忆库会越来越大，但 agent 的策略未必越来越好。

Experience 阶段主要回应这个问题：把局部轨迹抽象成规则、skill、library、latent prior 或参数能力。

---

## 8. Transformative Experience：Experience 阶段的新机制

论文特别强调 Experience 阶段有两个代表性机制。

### 8.1 Active Exploration：主动探索

在 Storage / Reflection 阶段，agent 更像是“发生了什么就记什么”。而 Experience 阶段要求 agent 变成主动收集经验的系统：它会基于目标、奖励、课程难度或历史经验，有方向地探索环境。

可以理解为：

- 不是“做完任务顺手存一下”；
- 而是“为了获得更有价值的经验，主动选择要探索什么”。

主动探索的驱动包括：

- reward signal：探索高价值状态空间；
- curriculum：从简单到复杂逐步探索；
- reuse：复用历史经验，提高探索效率。

### 8.2 Cross-Trajectory Abstraction：跨轨迹抽象

跨轨迹抽象是这篇综述最值得记住的概念。它强调经验不是单条轨迹的总结，而是从一组轨迹中提炼规律。

典型抽象方式：

- **contrastive induction**：对比成功轨迹和失败轨迹，找出策略边界；
- **action distillation**：把细粒度动作序列蒸馏成高层思维模式；
- **code encapsulation**：把常见动作模式封装成可执行函数或 skill；
- **gradient internalization**：把经验通过训练写进模型参数。

抽象层级也不同：

- 浅层：自然语言规则、经验原则；
- 中层：模块化执行骨架、程序函数、skill；
- 深层：模型参数或 latent representation 中的隐式先验。

---

## 9. 方法 / 实验设计

这是一篇综述论文，不是一个提出新模型并跑 benchmark 的方法论文。因此它没有传统意义上的“本文方法 vs baseline”的主实验。

它的实验与评价相关内容主要体现在：

1. **文献分类**：把现有 LLM Agent memory 研究放入 Storage、Reflection、Experience 三阶段。
2. **机制归纳**：总结每个阶段的代表技术路线，如线性存储、向量存储、结构化存储、自省反思、环境反思、多 agent 协同反思、显式经验、隐式经验、混合经验。
3. **benchmark 梳理**：附录整理了 memory 相关 benchmark，尤其指出现有 benchmark 更偏检索和去噪，对 Experience 阶段的抽象、泛化和生命周期评估仍不足。
4. **未来方向**：提出 active memory perception、working memory organization、benchmark for experience、distributed shared memory、multimodal memory 等研究方向。

因此，在横向实验对比表里，这篇论文应被标记为 **survey / taxonomy**：它提供实验设计地图，但本身不报告新的统一实验分数。

---

## 10. 主要结论

### 10.1 Memory evolution 不是单纯扩容

论文最重要的结论是：LLM Agent memory 的演化不是“存更多东西”，而是从容量扩展走向信息密度提升和认知抽象提升。

也就是说，问题不只是：

> 记忆库能不能更大？

而是：

> 记忆能不能更干净、更可用、更抽象、更可迁移？

### 10.2 Reflection 和 Experience 的边界很关键

很多论文都会说自己在做 experience，但这篇综述提醒我们要区分：

- Reflection：对单条轨迹做修正、总结、批评；
- Experience：从多条轨迹中抽象出脱离具体场景的通用策略。

这个边界对阅读 self-evolving agent 论文很重要。否则很容易把“任务后总结一句经验”误认为真正的长期自演化。

### 10.3 Experience 阶段推动 Agent 从被动记忆到主动学习

Experience 阶段的两个关键能力是主动探索和跨轨迹抽象。它们让 memory 不再只是历史缓存，而成为 agent 形成新策略的核心中介。

### 10.4 评测体系仍明显不足

论文明确指出，现有 benchmark 更多评估 Storage / Reflection 阶段的检索、保持和去噪能力，对 Experience 阶段的抽象能力、泛化能力、生命周期管理、meta-learning 能力评估不足。

---

## 11. 工程启发

### 11.1 不要只做“无限记忆库”

工程上很容易把 agent memory 做成一个不断增长的向量库。但这篇论文提醒：无限增长会带来检索延迟、错误传播、过期记忆污染、相似但不适用的经验误导。

更合理的 memory 系统至少要有：

- 写入过滤；
- 重要性评分；
- 时间衰减；
- 删除和合并；
- 错误经验隔离；
- 经验抽象；
- 检索后再判断是否真的要使用。

### 11.2 经验库要区分“事实记忆”和“策略经验”

事实记忆回答“世界是什么”，策略经验回答“这类任务怎么做”。

例如：

- 用户偏好、历史订单、网页状态：更偏事实 / 状态记忆；
- 搜索策略、代码调试套路、工具调用顺序：更偏经验 / policy prior；
- 可执行函数、workflow、skill：更偏中层或显式 experience。

### 11.3 经验不是越具体越好

具体轨迹有细节，但泛化差；抽象经验泛化更好，但可能丢失关键条件。

工程上需要维护多层 memory：

- 原始轨迹：用于审计和回放；
- 轨迹摘要：用于快速定位；
- 反思结论：用于纠错；
- 经验规则：用于泛化；
- skill / function：用于执行复用；
- 参数内化：用于降低推理时检索负担。

### 11.4 Retrieval 之前要先判断“需不需要记忆”

论文提出 future direction 中的 active memory perception 很重要。Agent 不应该每次都无脑检索一大堆记忆，而应该先判断：当前任务是否需要记忆？需要哪类记忆？记忆是否过期？是否会干扰当前推理？

这和工具调用校准中的 “epistemic necessity” 有相似思想：不是能调用就调用，而是需要时才调用。

### 11.5 Experience benchmark 是一个研究机会

如果想做后续研究，可以考虑设计专门评估 Experience 阶段的 benchmark：

- 任务以 stream 形式到来；
- 有分布变化；
- 单条轨迹经验不足以泛化；
- 需要从多次成功 / 失败中抽象规则；
- 后续任务检验抽象经验是否可迁移；
- 同时记录 memory 写入、检索、使用、删除和更新的全过程。

---

## 12. 局限性

论文自己也指出了几类局限：

1. **缺少直接量化比较**：不同 memory 机制的目标、基础模型、环境、prompt 都不同，强行做统一分数比较容易误导。
2. **Experience 与已有学习范式有交叉**：implicit experience 会和 fine-tuning、RL、meta-learning 重叠，论文并不是说 Experience 是全新学习范式，而是强调这些技术在 memory-centric agent 架构中的位置。
3. **时间覆盖和近期偏差**：Agent memory 领域在 2024–2025 增长很快，Experience 作为清晰方向更是近期才形成，部分 preprint 尚未正式同行评审。
4. **综述框架仍偏定性**：这篇文章给出清晰 taxonomy，但还没有给出统一实验协议来验证三阶段划分是否能预测系统性能。

我的补充理解：这篇综述提出了很有用的概念边界，但实际论文往往是混合形态，比如一个系统既有向量库，又有反思器，又用 SFT/RL 内化经验。阅读具体论文时，不能只把它硬塞进一个阶段，而要看它的主贡献到底落在哪个层次。

---

## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| Agent Memory 可以按 Storage → Reflection → Experience 理解 | 对线性、向量、结构化存储，内省 / 外部 / 交互反馈，以及显式 / 隐式 / 混合经验方法的文献分类 | 只按 memory 数据结构或检索方式分类 | 提供一个跨方法比较“保存、纠错、抽象”的统一坐标 | Taxonomy 是解释框架，不是经过实验验证的自然阶段，也不能保证类别互斥 |
| Experience 不等于保存成功案例 | 综述强调主动探索、跨轨迹抽象和可迁移策略先验，并区分 raw trajectory、reflection 与 experience | 把所有历史日志、摘要和案例统一称为经验 | 澄清经验形成需要比存储和单轨反思更强的抽象机制 | 不同论文中 experience 的定义仍有重叠，无法仅凭名称判断机制层级 |
| 全局记忆库与某一步真正检索到的记忆必须分开分析 | 形式化区分 global memory repository 与 retrieved memory at time t | 只报告“系统有 memory”而不追踪实际使用 | 支持把写入、检索、激活和收益拆成不同评测环节 | 综述本身未提供统一日志协议或因果指标来测量每一环节 |
| 当前 benchmark 尚不足以评估长期 Experience | 对现有 benchmark 的整理，以及对任务流、分布变化、跨轨迹抽象、写入 / 删除全过程的未来评测建议 | 单任务成功率或静态检索准确率 | 明确指出长期、动态、成本敏感评测的研究缺口 | 这些 benchmark 设计仍是研究议程，尚未通过实证证明可预测真实长期能力 |

### 我的判断

这篇综述最有价值的是概念校准：它迫使读者回答一个方法到底只是保存轨迹、在修正轨迹，还是已经抽象出跨任务策略。它也为 EvolveR、ACE、SE-Agent 和 MemoPilot 提供了共同语言。

其证据主要是文献覆盖与分类一致性，而不是统一实验。使用这套 taxonomy 时，应允许混合系统跨越多个阶段，并继续检查实际检索、使用收益、成本和长期退化。

### 其他可能解释

- Storage、Reflection、Experience 也可以被看作并行模块而不是线性演化阶段。
- 近期论文和预印本占比较高，分类可能受时间窗口与作者选文范围影响。
- 参数化经验、RL 和 meta-learning 与 memory 的边界具有定义依赖性。

---

## 13. 和已有笔记的关系

### 13.1 和 EvolveR 的关系

EvolveR 的 experience base、经验自蒸馏、GRPO policy evolution 可以放在这篇综述的 **Experience / Hybrid Experience** 框架下理解。EvolveR 不是单纯存轨迹，而是从轨迹中蒸馏经验原则，再用检索和训练影响后续搜索 agent。

### 13.2 和 ACE 的关系

ACE 把上下文维护成 playbook，从轨迹与反馈中生成 delta context items，并做合并、去重和统计。它更像是 **Explicit Experience + Context Asset Governance**：经验以文本条目形式存在，后续任务通过上下文读取。

### 13.3 和 SE-Agent 的关系

SE-Agent 主要是测试时轨迹层优化。它保存多条 trajectory，并做 revision、recombination、refinement。按照这篇综述的框架，它更接近 **trajectory preservation + trajectory refinement**，但不一定形成跨任务长期 experience。

### 13.4 和 Harness Updating Is Not Harness Benefit 的关系

这篇综述解释 memory / experience 如何演化；Harness Updating 那篇则提醒：即便 memory、skill、workflow 被更新，也要检验 Task-Solver 是否真的会用。两篇合起来看，可以形成一个检查项：

> Agent memory 不仅要能写入和抽象，还要能在后续任务中被正确检索、激活和遵循。

### 13.5 和 Gödel Agent 的关系

Gödel Agent 更进一步，把 agent 的程序本身也变成可读、可改、可递归优化的对象。它超出了传统 memory mechanism，但也可以被看作更广义 self-evolving agent 的一个极端：不仅经验库演化，连产生和使用经验的程序逻辑也演化。

---

## 14. 我的理解与总结

### 核心理解

这篇综述把 **LLM Agent 的记忆机制** 从“存储历史记录”的工程问题，重新组织成一条从 **Storage → Reflection → Experience** 的演化路径：先保存轨迹，再反思和清洗轨迹，最后从多条轨迹中抽象出可迁移的经验、规则、技能或参数化能力。

我的理解：这篇文章非常适合作为理解 **Agent Memory / Experience Base / Self-Evolving Agent** 的总框架。它的核心价值不是提出一个新 agent，而是给现有工作提供一个统一坐标系：一篇论文到底是在做“轨迹存储”、 “轨迹反思”，还是已经进入“跨轨迹经验抽象”。

### 进一步总结

这篇综述让我更清楚地区分了几个容易混淆的概念：

- **memory** 不等于 vector database；
- **reflection** 不等于真正经验抽象；
- **experience** 不等于保存成功案例；
- **self-evolving agent** 不一定训练模型参数，也不一定只是更新 prompt；
- 真正关键的是：历史交互如何被压缩、清洗、抽象，并在未来任务中产生稳定收益。

我认为可以用一句话概括这篇论文的定位：

> 它把 LLM Agent Memory 从“存什么、怎么检索”的工程问题，提升为“轨迹如何变成经验，经验如何变成可迁移策略”的自演化问题。

对后续读论文，我会用这篇文章提供的三阶段框架做一个检查表：

| 检查项 | 要问的问题 |
|---|---|
| Storage | 它保存的是 raw trajectory、summary、状态、事实，还是结构化图？ |
| Reflection | 它有没有用模型自省、环境反馈或多 agent 协作来纠错？ |
| Experience | 它有没有跨多条轨迹抽象出规则、skill、程序或参数能力？ |
| Retrieval | 后续任务如何取用这些记忆？是否会误取、过期、污染？ |
| Benefit | 写入经验后，Task-Solver 是否真的激活并遵循了它？ |
| Evaluation | benchmark 是否评估长期泛化，而不是只评估单次检索准确率？ |

这篇文章本身不是最复杂的算法论文，但它的概念密度很高。适合反复用来校准我们对 Agent Memory、Experience Base、Context Engineering、自演化 Agent 等工作的理解边界。

---

## 论文外部信息

### 投稿与发表状态

- arXiv 编号：**arXiv:2605.06716**。
- arXiv v1 提交时间：**2026-05-07**。
- 论文标注：**Accepted by ACL 2026 Findings**。
- 主题分类：**Artificial Intelligence (cs.AI)**、**Computation and Language (cs.CL)**。
- 官方资源列表：作者维护了 `FeishuLuo/Evolving-LLM-Agent-Memory-Survey`，其中整理了 LLM Agent memory 相关论文与 benchmarks。

### 作者与机构

论文作者：Jinghao Luo、Yuchen Tian、Chuxue Cao、Ziyang Luo、Hongzhan Lin、Kaixin Li、Chuyi Kong、Ruichao Yang、Jing Ma。

论文首页列出的机构包括：

- **Hong Kong Baptist University**
- **South China Normal University**
- **Hong Kong University of Science and Technology**
- **National University of Singapore**
- **University of Science and Technology Beijing**

论文首页脚注显示 Jinghao Luo 与 Yuchen Tian 为 equal contribution，Yuchen Tian 为 project leader，Jing Ma 为 corresponding author。

### 作者背景和研究圈子

从机构与参考文献脉络看，这篇论文处在 **NLP / LLM Agent / Agent Memory / Self-Evolving Agent** 的交叉研究圈子中。作者团队以香港浸会大学相关研究者为核心，并联动华南师范大学、香港科技大学、新加坡国立大学和北京科技大学等机构。

需要注意：我暂未逐一核验所有作者的个人主页、长期研究方向和导师关系；本节只基于论文首页、arXiv 信息和官方资源列表做保守整理，不扩展未确认背景。

---

## 参考资料

- arXiv：<https://arxiv.org/abs/2605.06716>
- PDF：<https://arxiv.org/pdf/2605.06716>
- HTML：<https://arxiv.org/html/2605.06716v1>
- 资源列表：<https://github.com/FeishuLuo/Evolving-LLM-Agent-Memory-Survey>
