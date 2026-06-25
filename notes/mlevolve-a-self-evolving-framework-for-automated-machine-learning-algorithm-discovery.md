<!--
metadata:
  schema_version: '1.0'
  title: 'MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery'
  short_title: 'MLEvolve'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'system'
  paper_status: 'preprint'
  venue: 'arXiv'
  venue_track: ''
  evolution_object: 'Solution Graph / Retrospective Memory'
  learning_stage: 'test-time'
  parameter_update: 'no'
  cross_task: 'no'
  arxiv_id: '2606.06473'
  arxiv_version: 'v1'
  arxiv_url: 'https://arxiv.org/abs/2606.06473'
  pdf_url: 'https://arxiv.org/pdf/2606.06473'
  html_url: 'https://arxiv.org/html/2606.06473'
  project_url: 'https://internscience.github.io/MLEvolve/'
  code_url: 'https://github.com/InternScience/MLEvolve'
  original_code_url: 'https://github.com/InternScience/MLEvolve'
  resource_url: ''
  model_url: ''
  code_status: 'official_available'
  model_status: 'not_found'
  first_submitted: '2026-06-04'
  last_revised: ''
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-24'
  authors:
    - 'Shangheng Du'
    - 'Xiangchao Yan'
    - 'Jinxin Shi'
    - 'Zongsheng Cao'
    - 'Shiyang Feng'
    - 'Zichen Liang'
    - 'Boyuan Sun'
    - 'Tianshuo Peng'
    - 'Yifan Zhou'
    - 'Xin Li'
    - 'Jie Zhou'
    - 'Liang He'
    - 'Bo Zhang'
    - 'Lei Bai'
  institutions:
    - 'Shanghai Artificial Intelligence Laboratory'
    - 'East China Normal University'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Machine Learning Engineering'
    - 'Automated ML Algorithm Discovery'
    - 'Monte Carlo Graph Search'
    - 'Retrospective Memory'
    - 'Hierarchical Planning'
    - 'Adaptive Code Generation'
    - 'MLE-Bench'
  tags:
    - 'self-evolving-agent'
    - 'mle-agent'
    - 'automl'
    - 'algorithm-discovery'
    - 'mcgs'
    - 'retrospective-memory'
    - 'adaptive-code-generation'
    - 'mle-bench'
    - 'arxiv-2026'
  related_notes:
    - 'notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md'
    - 'notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md'
  created: '2026-06-15'
  updated: '2026-06-25'
-->

# 《MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery》读书笔记

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

## 1. 基本信息

- 论文标题：MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery
- arXiv：<https://arxiv.org/abs/2606.06473>
- PDF：<https://arxiv.org/pdf/2606.06473>
- arXiv HTML：<https://arxiv.org/html/2606.06473>
- 项目主页：<https://internscience.github.io/MLEvolve/>
- 官方代码仓库：<https://github.com/InternScience/MLEvolve>
- 模型权重：暂未找到官方单独发布的模型权重。

这篇论文研究的是：**如何让 LLM Agent 在端到端机器学习工程任务中持续搜索、执行、评估、复用经验，并自动发现更好的 ML pipeline / 算法方案。** 它不是一个单轮代码生成器，而是一个围绕 MLE-Bench 和数学优化任务构建的长时程自演化系统。

我的一句话理解是：

> MLEvolve 把自动机器学习算法发现建模成“多分支代码方案搜索 + 运行反馈 + 经验记忆 + 自适应代码生成”的闭环，让 Agent 像参加 Kaggle 比赛一样持续试方案、看分数、吸收经验、融合分支，再生成更好的下一版方案。

## 2. 投稿 / 发布状态

arXiv 页面显示：

- arXiv 编号：**2606.06473**
- 分类：Computer Science > Artificial Intelligence，同时也列在 Computation and Language
- v1 提交时间：**2026-06-04**
- DOI：arXiv DOI pending / arXiv DataCite DOI 页面可用

官方 GitHub README 和项目主页显示：

- 论文于 **2026-06-05** 在 arXiv 发布；
- 代码仓库已公开；
- README 标注项目为 MIT License；
- 项目页称 MLEvolve 在 MLE-Bench 全量 75 个任务上以 12 小时预算达到 65.3% medal rate。

因此，截至 2026-06-15，这篇论文应写作：**arXiv 预印本 + 官方代码已开源**。我暂未找到会议接收状态或正式出版信息。

## 3. 作者与机构

论文作者共 14 位：

| 作者 | 机构 |
|---|---|
| Shangheng Du | Shanghai Artificial Intelligence Laboratory; East China Normal University |
| Xiangchao Yan | Shanghai Artificial Intelligence Laboratory |
| Jinxin Shi | Shanghai Artificial Intelligence Laboratory; East China Normal University |
| Zongsheng Cao | Shanghai Artificial Intelligence Laboratory |
| Shiyang Feng | Shanghai Artificial Intelligence Laboratory |
| Zichen Liang | Shanghai Artificial Intelligence Laboratory |
| Boyuan Sun | Shanghai Artificial Intelligence Laboratory |
| Tianshuo Peng | Shanghai Artificial Intelligence Laboratory |
| Yifan Zhou | Shanghai Artificial Intelligence Laboratory |
| Xin Li | Shanghai Artificial Intelligence Laboratory |
| Jie Zhou | Shanghai Artificial Intelligence Laboratory; East China Normal University |
| Liang He | Shanghai Artificial Intelligence Laboratory; East China Normal University |
| Bo Zhang | Shanghai Artificial Intelligence Laboratory |
| Lei Bai | Shanghai Artificial Intelligence Laboratory |

论文首页脚注标注通信邮箱为 `yanxiangchao@pjlab.org.cn`、`zhangbo@pjlab.org.cn`、`bailei@pjlab.org.cn`，因此 Xiangchao Yan、Bo Zhang、Lei Bai 可以视作通信作者线索。

## 4. 作者背景和研究圈子

从机构、项目名和 README 引用关系看，这篇论文主要来自 **Shanghai AI Lab / InternScience / InternAgent** 相关研究圈子。项目 README 明确提到：

- MLEvolve 是 AutoMLGen 的高级版本；
- MLEvolve 也作为 InternAgent 系统中的 coding / algorithm optimization module；
- README 的 citation 同时列出 AutoMLGen 和 InternAgent-1.5。

只做一个粗略判断的话，这个圈子的关注点不是单个 benchmark 的 prompt trick，而是 **AI for Science / MLE Agent / 长时程自主科研系统**：

1. **机器学习工程自动化**：让 Agent 自动处理数据理解、特征工程、模型选择、训练、调参、提交文件生成。
2. **长时程 Agent 搜索**：任务预算以小时计，Agent 需要持续试错和重新分配搜索资源。
3. **多 Agent / 多模块协作**：planner、coder、debugger、fusion 等角色分工明显。
4. **自演化经验复用**：不只是保留最优分数，而是把 plan、code、metric、analysis、失败反馈等写入全局记忆。

这篇论文和仓库里已有几篇笔记的关系可以这样放：

| 对比对象 | 共同点 | 差异 |
|---|---|---|
| EvolveR | 都强调 experience / memory 和自演化闭环 | EvolveR 面向搜索增强 QA，并训练模型策略；MLEvolve 面向 MLE / 算法发现，主要通过外层搜索、记忆和代码生成模式演化 |
| SE-Agent | 都把多条轨迹 / 分支当成可复用资源 | SE-Agent 更偏当前任务内 trajectory pool 和代码修复；MLEvolve 更偏 ML pipeline 搜索图、跨分支引用和长时程 leaderboard 优化 |
| Agentic Context Engineering | 都把经验沉淀到外部结构中供后续使用 | ACE 的进化对象是 context playbook；MLEvolve 的进化对象是 candidate solution graph、global memory 和代码方案 |
| Gödel Agent | 都讨论 self-improvement / self-evolution | Gödel Agent 修改 agent 程序逻辑；MLEvolve 不强调自改代码框架本身，而是演化 ML 解法和搜索过程 |

## 5. 研究方向与论文定位

MLEvolve 属于 **Self-Evolving LLM Agent**，但更准确地说，它是：

```text
Self-Evolving LLM Agent
└── MLE / AutoML / Algorithm Discovery Agent
    ├── Code-generation Agent
    ├── Monte Carlo Graph Search
    ├── Agent Memory / Experience Reuse
    └── Hierarchical Planning / Adaptive Coding
```

这篇论文的重要性在于，它把 self-evolving agent 放到了一个非常硬的工程场景里：**Kaggle-style 机器学习比赛**。在这个场景中，Agent 不能只会回答问题，它必须：

- 读懂任务说明和数据格式；
- 写可运行的训练 / 推理代码；
- 产生有效 submission；
- 根据本地评分或 leaderboard 代理指标继续改；
- 在有限时间内分配探索和利用预算；
- 防止反复在无效分支里浪费时间。

所以它和很多问答型、网页型、工具调用型 Agent 的区别是：**评价信号更硬，搜索空间更大，运行成本更高，且每次代码变更都要经过执行验证。**

## 6. 核心问题

论文认为现有 MLE Agent 有三个主要瓶颈。

### 6.1 分支之间信息隔离

很多方法使用线性搜索、树搜索或多分支搜索，但不同分支之间通常不共享足够的信息。结果是：

- A 分支找到好的模型选择，但 B 分支不知道；
- B 分支解决了数据预处理问题，但 A 分支仍然重复犯错；
- MCTS 的树结构保留父子关系，但难以表达“这个节点参考了另一个非父节点”的关系。

MLEvolve 用 **Monte Carlo Graph Search** 替代纯树结构，允许用 reference edges 表达跨分支参考。

### 6.2 搜索过程缺少经验记忆

很多搜索框架只回传标量 reward：成功、失败、分数高低。这样做虽然能更新节点价值，但会丢掉大量有用信息：

- 这次方案为什么失败？
- 哪个模型在相似任务上有效？
- 某个报错以前怎么修过？
- 哪类特征工程方向在这个任务里值得继续？

MLEvolve 的 **Retrospective Memory** 试图把每个有效节点的 plan、outcome、analysis、feedback signal 等结构化记录存下来，并在后续 planning / debugging 阶段检索。

### 6.3 规划和代码生成耦合太紧

很多 Agent 在每次迭代中直接要求 LLM 重写完整代码。问题是：

- 已经有效的部分容易被破坏；
- 小改动也要重写全文件，成本高且不稳定；
- 模型同时决定“改什么”和“怎么写”，容易失控。

MLEvolve 把 planner 和 coder 分开：planner 决定 **what / why**，coder 决定 **how**，并根据搜索状态选择 full rewrite、module-by-module 或 diff patch。

## 7. 方法：MLEvolve 的三个核心组件

### 7.1 总体框架

论文 Figure 1 / Figure 2 把系统概括成三个模块：

1. **Progressive MCGS**：从 MCTS 扩展到图搜索，支持分支内演化、跨分支参考、多分支聚合，并用 progressive schedule 从探索转向利用。
2. **Retrospective Memory**：由冷启动领域知识库和动态全局记忆组成，支持计划阶段和调试阶段的经验检索。
3. **Hierarchical Planning with Adaptive Code Generation**：把 planner 和 coder 解耦，并根据当前状态选择 Base / Stepwise / Diff 三种代码生成模式。

我觉得这三个模块分别对应现有 MLE Agent 的三个失败点：

```text
分支隔离          -> Progressive MCGS / reference edges
无记忆搜索        -> Retrospective Memory / global experience
一把梭重写代码    -> Hierarchical Planning / adaptive coding modes
```

### 7.2 Progressive MCGS：从树搜索到图搜索

MLEvolve 把搜索空间组织成有向图：

```text
G = (V, E), E = E_T ∪ E_ref
```

其中：

- `E_T` 是 primary edges，表示一个节点由父节点通过某个 operator 生成，参与 selection 和 backpropagation；
- `E_ref` 是 reference edges，表示新节点额外参考了其他节点的信息，但不参与 reward 回传。

这个设计很关键。标准 MCTS 的树结构只能表达“父子生成关系”，而 MLEvolve 还要表达：

- 这个新方案参考了同一分支的历史尝试；
- 这个新方案吸收了其他高分分支的模型选择；
- 这个新方案融合了多个分支的互补 insight。

所以它用 `E_ref` 把“信息来源”显式记下来，同时避免把 reference 节点也纳入父子 credit assignment，减少奖励归因混乱。

### 7.3 Progressive exploration schedule：前期广探索，后期重利用

MLEvolve 没有一直用固定 UCT 探索强度，而是让探索权重随时间下降：

- 早期：更偏 UCT，鼓励多分支探索；
- 中期：逐渐降低探索常数；
- 后期：更多选择 elite nodes，集中资源优化高潜力方案。

论文用 entropy-inspired schedule 描述这个过程。直观理解是：早期让搜索努力分散在更多分支上，后期让搜索熵下降，把计算集中到更有希望的方案附近。

这对 MLE 任务很合理。Kaggle 式任务常常前期需要试很多方向：

- 先判断任务类型；
- 尝试 baseline 模型；
- 试不同预处理；
- 观察指标和错误。

但到后期，如果还平均探索所有分支，就会浪费宝贵时间。后期更应该围绕高分方案做稳定改进。

### 7.4 四种 expansion 类型

论文把 graph-based expansion 具体实现为四类：

| Expansion 类型 | 参考信息 | 作用 |
|---|---|---|
| Primary expansion | 只参考父节点 | 标准扩展，生成普通子方案 |
| Intra-branch evolution | 参考同一分支最近 k 个节点 | 回顾本分支哪些修改有效，避免重复错误 |
| Cross-branch reference | 参考全局 top-N 节点 | 分支停滞时借鉴其他高分分支 |
| Multi-branch aggregation | 融合多个强分支 | 创建新的分支根，综合互补方案 |

这里最像 self-evolution 的部分，是它不只保存“当前最好节点”，而是把历史分支作为可回顾、可引用、可聚合的资源。

和 SE-Agent 的 recombination 相比，MLEvolve 的跨分支融合更偏 **ML solution / code plan 层面**，目标是构造更强的候选 pipeline；SE-Agent 的 recombination 更偏 **代码修复轨迹 / reasoning-action 序列层面**。

### 7.5 停滞检测：什么时候触发跨分支机制

论文设计了两级 stagnation detection：

- **Branch-level stagnation**：某个分支连续若干次没有刷新本分支最好指标，先触发 intra-branch evolution，后期再触发 cross-branch reference。
- **Global-level stagnation**：全局最好指标连续若干步没有提升，触发 multi-branch aggregation。

这点很工程化：跨分支融合不是每一步都做，而是在“这个方向明显卡住”时做。否则系统会过早融合，导致搜索多样性不足。

### 7.6 Retrospective Memory：冷启动知识库 + 动态全局记忆

Retrospective Memory 包含两部分。

第一部分是 **Domain Knowledge Base**。它按任务类型组织候选模型和简短使用指南，例如图像分类、NLP、表格回归等任务适合哪些模型。这主要解决冷启动：

```text
任务刚开始时还没有本任务经验
-> 用领域先验生成初始 plan / code
```

第二部分是 **Dynamic Global Memory**。搜索过程中每个有效节点都会写入结构化记录，包括：

- plan；
- outcome；
- analysis；
- metric；
- feedback signal；
- debugging 信息。

检索时使用 hybrid retrieval：lexical keyword matching + FAISS semantic search，再用 Reciprocal Rank Fusion 合并排序。

### 7.7 Stage-aware retrieval：计划和调试要查不同经验

MLEvolve 不是简单用同一个 query 查所有 memory，而是区分阶段：

| 阶段 | Query / 过滤方式 | 检索目标 |
|---|---|---|
| Planning stage | 用初始 plan 作为 query | 查相似成功 / 失败经验，帮助把自由文本计划改成结构化模块级方案 |
| Debugging stage | 用 error message 作为 query | 查类似错误和已解决办法，指导修 bug |

这个设计很值得借鉴。Agent memory 如果不区分场景，很容易检索出“语义相似但行动无关”的记录。MLEvolve 把 memory 的使用绑定到 planner / debugger 的具体需求上，降低噪声。

### 7.8 Hierarchical Planning and Adaptive Code Generation

MLEvolve 把代码生成拆成 planner 和 coder：

- planner：根据任务、历史轨迹、执行反馈、检索记忆决定要改什么、为什么改；
- coder：根据 planner 的模块级计划写代码，关注怎么实现。

coder 有三种模式：

| 模式 | 作用 | 适用场景 |
|---|---|---|
| Base mode | 从零生成完整 solution | 初始阶段，还没有可靠方案 |
| Stepwise mode | 按模块逐步生成 | 任务复杂，需要拆成数据处理、训练、预测等模块 |
| Diff mode | 对已有代码做局部 patch | 已有可运行方案，需要稳定小改 |

这套设计的工程意义是：**越到后期越应该少重写、多局部修改**。因为 MLE 任务中一个已经能产出 valid submission 的脚本很宝贵，随意全量重写可能把数据格式、提交逻辑、依赖处理都弄坏。

## 8. 实验设计

### 8.1 Benchmark

论文使用两个评测场景。

| Benchmark | 任务 | 用途 |
|---|---|---|
| MLE-Bench | 75 个 Kaggle-style 机器学习工程任务，覆盖低 / 中 / 高复杂度 | 主实验，评估端到端 MLE 能力 |
| AlphaEvolve mathematical optimization tasks | 15 个开放数学优化 / 算法发现任务 | 测试跨域算法优化能力 |

MLE-Bench 来自 OpenAI，用于评估 autonomous machine learning engineering。论文附录说明 75 个任务来自人工筛选的 Kaggle 竞赛，覆盖 NLP、CV、信号处理、表格数据等方向，并按复杂度分为：

- 22 个 low-complexity 任务；
- 38 个 medium-complexity 任务；
- 15 个 high-complexity 任务。

### 8.2 模型和运行设置

主实验使用：

- backbone LLM：**Gemini-3.1-Pro-preview**
- decoding temperature：1.0
- 每个任务最多 500 expansion steps
- 每个任务 12 小时运行预算
- 资源：21 vCPUs、234 GB RAM、单张 NVIDIA H200 GPU

这个设置说明 MLEvolve 的目标不是轻量推理，而是高预算长时程 Agent 系统。它的优势和成本都要在这个前提下理解。

### 8.3 Baselines

论文比较了 proprietary 和 open-source 两类 MLE agent：

| 类别 | Baseline |
|---|---|
| Proprietary methods | FM-Agent、MLE-STAR-Pro-1.5、MARS、MARS+、AIBuildAI |
| Open-source methods | AIDE、R&D-Agent、ML-Master、AIRA-Dojo、Leeroo、ML-Master 2.0 |
| 数学优化任务 | AlphaEvolve、AlphaEvolve-v2、SimpleTES、TTT-Discover、OpenEvolve |

阅读时要注意：Table 1 的 baseline 结果来自 MLE-Bench leaderboard 或对应论文，并非都在完全同一模型和预算下重新跑。MLEvolve 的一个亮点是用 12 小时预算超过许多 24 小时设置。

### 8.4 评价指标

MLE-Bench 主指标包括：

| 指标 | 含义 |
|---|---|
| Medal Rate | 达到 Kaggle bronze / silver / gold 阈值的任务比例 |
| Gold Medal Rate | 达到 gold medal 阈值的任务比例 |
| Valid Submission Rate | 产出有效 submission 文件并通过格式 / 正确性检查的任务比例 |
| Above Median Rate | 超过一半 Kaggle 人类参赛者的任务比例 |
| Beat Ratio | 平均超过的人类参赛者比例 |

这些指标比普通 accuracy 更贴近真实 MLE 场景：既看能不能提交，也看提交相对人类 leaderboard 的竞争力。

## 9. 主要实验结果

### 9.1 MLE-Bench 主结果

在 MLE-Bench 75 个任务全量集合上，MLEvolve 取得：

| 指标 | 结果 |
|---|---:|
| Low complexity medal rate | 80.3 ± 1.5 |
| Medium complexity medal rate | 64.0 ± 0.9 |
| High complexity medal rate | 46.7 ± 0.0 |
| All medal rate | 65.3 ± 0.8 |
| Valid submission rate | 100.0 ± 0.0 |
| Above median rate | 76.0 ± 2.3 |
| Gold medal rate | 34.7 ± 0.0 |

几个值得记住的点：

1. **65.3% overall medal rate** 是论文主打结果；
2. **100% valid submission rate** 说明系统稳定性很强，不只是少数任务刷高分；
3. 在 high-complexity 任务上仍有 46.7% medal rate，说明长时程搜索确实带来收益；
4. 它用的是 12 小时预算，而许多 baseline 是 24 小时预算。

### 9.2 数学优化任务

论文还在 AlphaEvolve 的 15 个数学编程 / 优化任务上测试。项目页总结为：MLEvolve 在 15 个任务中 **14 个匹配或超过 AlphaEvolve**，并在论文 Table 2 中显示相对 AlphaEvolve、AlphaEvolve-v2、SimpleTES、TTT-Discover、OpenEvolve 的比较。

这组实验的意义不是说 MLEvolve 已经是通用数学发现系统，而是说明：

> 它的自演化机制不只适用于 Kaggle-style ML pipeline，也能迁移到“提出候选方案 -> 执行评估 -> 继续优化”的算法发现问题。

### 9.3 组件消融

论文在 MLE-Bench Lite 22 个任务上做组件级消融：

| 配置 | Medal (%) | Gold (%) | Beat Ratio (%) |
|---|---:|---:|---:|
| MLEvolve | 81.82 | 54.55 | 88.39 |
| w/o Progressive MCGS | 68.18 | 40.91 | 79.91 |
| w/o Retrospective Memory | 68.18 | 50.00 | 81.90 |
| w/o Adaptive Code Generation | 72.73 | 40.91 | 84.14 |

我的理解是：

- Progressive MCGS 对整体搜索最关键，去掉后回到更标准的 tree-based MCTS，后期资源容易浪费在低价值分支；
- Retrospective Memory 影响长时程任务中的经验反馈和规划质量；
- Adaptive Code Generation 主要影响迭代稳定性，避免每次都全量重写导致有效代码被破坏。

### 9.4 细粒度消融

附录在 9 个代表任务上进一步拆分机制：

| 模块 | 去掉机制 | Medal (%) | Beat Ratio (%) |
|---|---|---:|---:|
| MLEvolve | 无 | 66.67 | 82.43 |
| Progressive MCGS | w/o Evolution | 33.33 | 74.95 |
| Progressive MCGS | w/o Cross-branch | 55.56 | 75.93 |
| Progressive MCGS | w/o Elite-Guided | 55.56 | 71.39 |
| Retrospective Memory | w/o Knowledge Base | 44.44 | 76.07 |
| Retrospective Memory | w/o Global Memory | 44.44 | 73.58 |

这里最有信息量的是：

- 去掉 **intra-branch evolution** 掉得最厉害，说明同一分支历史复盘对避免重复错误很重要；
- 去掉 Knowledge Base 和 Global Memory 都会明显下降，说明冷启动先验和动态经验都不可少；
- Global Memory 的 beat ratio 影响更大，说明动态积累的任务内经验对长期质量提升更重要。

### 9.5 不同 LLM backbone

附录 Table 6 比较了 Gemini-3.1-Pro-preview、GPT-5.5、DeepSeek-v4-Pro、Kimi-K2.6 在 8 个代表 MLE-Bench 任务上的得分。论文结论是没有单一模型在所有任务上占优，但四个 backbone 在同一 MLEvolve pipeline 下都能产生竞争性结果。

这个结果支持一个判断：MLEvolve 的核心贡献更偏 **agent scaffold / search framework**，而不是只依赖某一个闭源模型。

## 10. 主要结论

我把论文结论概括成四点：

1. **MLE 任务需要长时程自演化，而不是单轮代码生成。** 机器学习 pipeline 优化需要持续执行、看分数、调策略。
2. **图搜索比纯树搜索更适合多分支经验共享。** Reference edges 可以表达跨分支借鉴，而不破坏 primary edge 的奖励回传。
3. **记忆要服务于具体阶段。** Planning 查成功 / 失败方案，debugging 查类似错误，这比“统一 memory 检索”更贴近工程需求。
4. **代码生成粒度要随搜索阶段变化。** 初期可全量生成，后期应更多使用模块化生成和 diff patch，保护已有有效方案。

## 11. 工程启发

### 11.1 Agent 搜索日志应该结构化成可检索经验

MLEvolve 每个有效节点都记录 plan、code、metric、analysis、feedback。这对真实 Agent 系统很重要。不要只保存最终答案，也不要只保存分数。

一个可复用的 MLE Agent 日志至少应该包括：

- task metadata；
- 当前代码版本；
- 执行日志；
- 指标；
- 和上一版本相比改了什么；
- 为什么这么改；
- 成功 / 失败分析；
- 可被检索的摘要。

### 11.2 分支不是独立尝试，而是互相供料的资源

很多多采样系统的问题是：跑了 10 条路径，但最后只是选最好的一条。MLEvolve 的启发是，多个分支之间可以有更丰富的关系：

- 分支 A 的模型选择可用于分支 B；
- 分支 B 的 debug 经验可用于分支 C；
- 多个分支的局部最佳实践可以聚合成新分支。

这比 best-of-N 更接近真正的搜索系统。

### 11.3 后期不要轻易全量重写代码

MLE 任务中的有效 submission 脚本很脆弱。全量重写可能让格式、路径、依赖、预处理、提交文件生成全部出错。

工程上可以参考 MLEvolve 的三段式：

```text
初期：Base mode，全量生成 baseline
中期：Stepwise mode，按模块改进
后期：Diff mode，只做局部稳定优化
```

这个设计对代码修复 Agent、数据分析 Agent、实验自动化 Agent 也有借鉴意义。

### 11.4 Memory 检索要和执行阶段绑定

同一条 memory 在不同阶段价值不同：

- 规划时需要“这个任务适合什么模型 / pipeline”；
- 调试时需要“这个错误怎么修”；
- 融合分支时需要“哪些高分方案可组合”；
- 后期利用时需要“哪些小改动可能稳定涨分”。

所以 memory schema 不能只是一堆文本块，最好带上 stage、operator、metric、task type、success/failure label 等字段。

### 11.5 自演化不一定意味着训练模型参数

MLEvolve 的 self-evolution 主要发生在系统层：

- 搜索图结构演化；
- 分支选择策略演化；
- global memory 增长；
- candidate solutions 迭代；
- 代码生成模式自适应切换。

这提醒我们，自演化 Agent 可以有多种层次：

```text
参数演化：SFT / RL / continual learning
上下文演化：playbook / memory / prompt
轨迹演化：trajectory pool / recombination
搜索演化：graph search / branch fusion
代码方案演化：candidate solution / diff refinement
```

MLEvolve 主要位于搜索演化和代码方案演化层。

## 12. 局限性

### 12.1 成本很高

主实验每个任务 12 小时，资源包括 H200 GPU、大内存和多 vCPU。对于普通研究者或小团队，这个成本不低。即使代码开源，完整复现 75 个 MLE-Bench 任务也需要相当预算。

### 12.2 依赖强闭源模型

主结果使用 Gemini-3.1-Pro-preview。虽然附录测试了多个 backbone，但最强主表结果仍依赖强模型能力。弱模型是否能稳定完成复杂 MLE planning、debugging、diff editing，还需要更系统验证。

### 12.3 MLE-Bench 之外的泛化仍有限

数学优化任务说明 MLEvolve 有跨域潜力，但主验证仍集中在 Kaggle-style MLE 和 AlphaEvolve 数学任务。迁移到真实科研实验、湿实验、长期项目管理、复杂软件工程等场景，还需要新的环境和评价。

### 12.4 Memory 质量控制仍是开放问题

论文使用 dynamic global memory 和 hybrid retrieval，但没有像 EvolveR 那样重点展开经验去重、质量评分、错误经验污染、过期经验删除等治理问题。随着搜索历史变长，memory 噪声和检索误导仍可能成为瓶颈。

### 12.5 Baseline 比较存在预算和来源差异

Table 1 中 baseline 结果来自 leaderboard 或对应论文，不完全是统一重新运行。MLEvolve 使用 12 小时预算取得强结果很亮眼，但不同方法的模型版本、运行环境、工程实现细节仍可能影响公平性。

### 12.6 “自演化”的长期学习边界需要区分

MLEvolve 会在一个任务内积累经验并优化方案，但它是否能把跨任务经验长期稳定迁移到新任务，还取决于 memory 持久化、任务类型泛化和知识库更新方式。它不是参数级 continual learning，也不等于 Agent 框架本身自动重写自己。

## 13. 我的理解与总结

我觉得 MLEvolve 最值得记住的是：**它把 self-evolving agent 放进了一个强反馈、长时程、代码执行驱动的真实工程环境。**

很多 Agent 论文里的自演化比较容易停留在“反思一下、更新一下 prompt、下次再试”。MLEvolve 则把这个过程具体化为：

```text
生成 ML 方案
-> 执行代码并得到指标
-> 写入搜索图和全局记忆
-> 检索相似经验
-> 判断分支是否停滞
-> 分支内复盘 / 跨分支参考 / 多分支聚合
-> planner 决定改什么
-> coder 选择全量、模块化或 diff 方式实现
-> 再执行、再评估、再更新
```

这套闭环里，LLM 不是单独解决问题的“大脑”，而是被放进一个搜索和实验基础设施中。真正提升性能的是：

- 有硬反馈；
- 有结构化历史；
- 有跨分支信息流；
- 有阶段化控制；
- 有稳定代码编辑模式；
- 有明确时间预算下的探索 / 利用调度。

如果和 EvolveR、SE-Agent 放在一起看，可以得到一个很清晰的研究地图：

| 工作 | 自演化对象 | 主要反馈 | 长期复用方式 |
|---|---|---|---|
| EvolveR | QA Agent 的经验原则和策略 | 答案正确性、检索轨迹 | Experience Base + SFT / GRPO |
| SE-Agent | 代码修复任务中的执行轨迹 | patch / reward / judge | 当前任务 trajectory pool |
| MLEvolve | ML pipeline / algorithm solution graph | 代码执行指标、Kaggle-style score | Retrospective Memory + graph search |
| ACE | 可维护上下文 / playbook | benchmark labels / 执行反馈 | Context playbook |

一句话总结：

> MLEvolve 的核心不是“让 LLM 一次写出更好的 ML 代码”，而是“搭一个能持续试验、记忆、融合和局部修改的 MLE 搜索系统”。

## 14. 后续值得继续追的问题

1. Retrospective Memory 能否跨 MLE-Bench 任务长期复用，而不是主要服务于当前任务搜索？
2. Global Memory 中错误经验、过时经验、低价值经验如何自动降权或删除？
3. Progressive MCGS 能否迁移到 SWE-bench、WebArena、科研实验设计等其他长时程任务？
4. Planner-Coder 解耦是否可以和更强的形式化代码验证 / 单元测试生成结合？
5. 在较弱开源模型上，三种 coding mode 的切换是否仍然稳定？
6. 如果把 MLEvolve 的历史节点蒸馏成训练数据，是否能进一步形成参数级 MLE Agent？
7. 如何把 cross-branch reference 的信息来源解释给用户，方便人工审计和调试？

## 15. 参考资料与链接

- arXiv abs：<https://arxiv.org/abs/2606.06473>
- arXiv PDF：<https://arxiv.org/pdf/2606.06473>
- 项目主页：<https://internscience.github.io/MLEvolve/>
- 官方代码仓库：<https://github.com/InternScience/MLEvolve>
- MLE-Bench：<https://github.com/openai/mle-bench>
