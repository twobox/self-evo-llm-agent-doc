<!--
metadata:
  schema_version: '1.0'
  title: 'WebEvolver: Enhancing Web Agent Self-Improvement with Co-evolving World Model'
  short_title: 'WebEvolver'
  year: 2025
  note_type: '中文读书笔记'
  paper_type: 'method'
  paper_status: 'published'
  venue: 'EMNLP 2025'
  venue_track: 'Main Conference'
  evolution_object: 'Agent Policy / World Model Parameters'
  learning_stage: 'mixed'
  parameter_update: 'yes'
  cross_task: 'yes'
  arxiv_id: '2504.21024'
  arxiv_version: 'v2'
  arxiv_url: 'https://arxiv.org/abs/2504.21024'
  pdf_url: 'https://aclanthology.org/2025.emnlp-main.454.pdf'
  html_url: 'https://aclanthology.org/2025.emnlp-main.454/'
  project_url: ''
  code_url: 'https://github.com/Tencent/SelfEvolvingAgent/tree/main/WebEvolver'
  original_code_url: ''
  resource_url: 'https://huggingface.co/datasets/CognitiveKernel/WebEvolver'
  model_url: ''
  code_status: 'official_available'
  model_status: 'not_found'
  first_submitted: '2025-04-23'
  last_revised: '2025-08-21'
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-29'
  authors:
    - 'Tianqing Fang'
    - 'Hongming Zhang'
    - 'Zhisong Zhang'
    - 'Kaixin Ma'
    - 'Wenhao Yu'
    - 'Haitao Mi'
    - 'Dong Yu'
  institutions:
    - 'Tencent AI Lab'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Web Agent'
    - 'World Model'
    - 'Synthetic Trajectory'
    - 'Model-Based Planning'
    - 'Inference-Time Search'
  tags:
    - 'llm-agent'
    - 'self-improvement'
    - 'web-agent'
    - 'world-model'
    - 'synthetic-trajectory'
    - 'model-based-planning'
    - 'inference-time-search'
    - 'wmla'
    - 'emnlp-2025'
  related_notes:
    - 'notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'notes/self-challenging-language-model-agents.md'
    - 'notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md'
  created: '2026-06-29'
  updated: '2026-06-29'
-->

# 《WebEvolver: Enhancing Web Agent Self-Improvement with Co-evolving World Model》读书笔记

- 论文：[ACL Anthology](https://aclanthology.org/2025.emnlp-main.454/)
- arXiv：[2504.21024](https://arxiv.org/abs/2504.21024)
- 代码：[Tencent/SelfEvolvingAgent - WebEvolver](https://github.com/Tencent/SelfEvolvingAgent/tree/main/WebEvolver)
- 数据：[CognitiveKernel/WebEvolver](https://huggingface.co/datasets/CognitiveKernel/WebEvolver)

## 30 秒读懂

> **一句话总结：** WebEvolver 用真实网页轨迹同时训练 Agent 策略模型和网页世界模型，再让世界模型生成失败任务的合成轨迹，并在推理时模拟候选动作的未来网页状态，从而同时扩展训练数据和动作搜索。

| 维度 | 内容 |
|---|---|
| 文章性质 | Web Agent 自我改进方法论文 |
| 核心问题 | 只依赖成功的真实网页轨迹反复 SFT 时，探索范围有限、提升很快停滞，怎样继续制造有效训练信号？ |
| 核心机制 | 世界模型预测“执行动作后的下一网页观察”，离线充当虚拟网页服务器生成合成轨迹，在线充当前瞻模拟器辅助选动作 |
| 更新对象 | Llama-3.3-70B 策略模型参数与 Llama-3.3-70B 世界模型参数 |
| 学习阶段 | 混合：训练时共同演化，测试时可选用 World Model Look-ahead |
| 是否跨任务 | 是；训练后的参数用于未见过的网页查询，但论文没有验证长期连续部署中的保持与遗忘 |
| 是否更新模型参数 | 是；策略模型和世界模型都经 SFT 更新 |
| 最重要结论 | 普通真实轨迹自训练在第二轮后停滞，而加入世界模型合成轨迹后，WebVoyager 成功率由基础模型的 32.98 提升到 42.49；再加两步 WMLA 达到 51.37 |
| 最大局限 | 成本高、依赖两个 70B 模型与真实网页基础设施；世界模型在更深预测时迅速失真，WMLA 还使用 GPT-4o 评分 |
| 复现状态 | 官方代码和 SFT 数据公开，但未找到官方模型权重；动态网站、地区/IP 限制和评测时段会影响结果 |

### 不要误读

WebEvolver **不是**只在当前任务里多搜索几条轨迹的测试时方法。它的主要自我改进来自把真实与世界模型合成轨迹转成 SFT 数据、更新策略模型参数；WMLA 是训练完成后的可选推理增强。它也不是一个精确复制互联网的通用模拟器：论文训练的是根据历史、当前可访问性树和动作预测下一观察的 LLM 世界模型。

---

## 论文定位

WebEvolver 位于三条路线的交叉处：

1. **Agent 自训练**：从自身成功轨迹构造监督数据并更新策略模型；
2. **世界模型辅助数据生成**：学习网页状态转移，用虚拟环境补充真实交互无法覆盖的轨迹；
3. **模型式测试时规划**：在真正执行前，用世界模型想象候选动作后果，再选择动作。

与仓库中相邻工作相比：

- [EvolveR](evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) 主要把轨迹压缩为可检索经验并配合 SFT / RL；WebEvolver 不维护显式经验库，而是把网页转移知识写入世界模型参数，并把合成轨迹写入策略模型参数。
- [Self-Challenging Agents](self-challenging-language-model-agents.md) 自主生成带验证器的训练任务；WebEvolver 的任务来源仍是已有网页查询，新增部分主要是世界模型模拟出的观察—动作轨迹，而不是重新发明任务目标。
- [SE-Agent](se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) 在单个代码任务内搜索和重组轨迹，不更新模型参数；WebEvolver 的训练结果可以跨查询复用，但需要昂贵的 70B 参数训练。

“Co-evolving”在这里更准确的含义是：策略模型产生真实轨迹，轨迹训练世界模型；世界模型再为策略模型合成数据。它是交替的数据闭环，而不是两个模型通过同一个可微目标端到端联合优化。

## 研究问题与动机

网页 Agent 的常见自训练流程是：

```text
用当前策略访问真实网页
→ 保留成功轨迹
→ 转成 SFT 数据
→ 微调策略模型
→ 再采样
```

问题在于，当前策略已经容易成功的任务会被反复采到，而失败任务缺少可用轨迹。论文实验中，第一轮自训练有明显提升，但第二、三轮基本停滞，说明“从已有能力附近继续采样”很难扩展探索边界。

> **本文试图回答：** 能否从真实交互轨迹中学出一个网页世界模型，让它既为失败任务生成新的训练轨迹，又在推理时预测候选动作后果，从而突破网页 Agent 自训练的平台期？

## 进化机制卡片

| 维度 | 内容 |
|---|---|
| 初始 Agent | Cognitive Kernel 风格的文本网页 Agent，策略骨干为 Llama-3.3-70B |
| 学习信号来源 | 1,516 个训练查询上的真实网页轨迹、自评成功标签、下一观察监督、世界模型合成轨迹 |
| 被更新的对象 | Agent policy 参数与 World Model 参数 |
| 经验形式 | 历史观察—动作—下一观察、转移解释、成功真实轨迹、最长 7 步的合成轨迹 |
| 存储位置 | SFT 数据集以及两个 Llama-3.3-70B 模型的参数 |
| 更新时间 | 每轮真实轨迹采样后分别训练策略模型和世界模型；最终再用合成轨迹训练 WebEvolver |
| 后续使用方式 | 策略模型直接生成网页动作；世界模型离线生成训练轨迹，或在 WMLA 中预测候选动作的未来观察 |
| 作用范围 | 同类网页操作与搜索任务间复用；未验证跨月长期部署或环境突变后的持续更新 |
| 是否更新模型参数 | 是，两个核心模型都更新 |
| 是否需要明确奖励 | 需要成功/失败筛选；训练闭环中使用 Llama-3.3-70B 自评，正式测试用 GPT-4o 自动评价 |
| 是否依赖教师模型 | 自训练数据筛选不依赖更强闭源教师；但 WMLA 用 GPT-4o 给候选前瞻结果打分，GAIA 实验也用 GPT-4o 做任务分解和结果生成 |
| 主要计算与 Token 成本 | 真实网页浏览、多轮 rejection sampling、两个 70B 模型的多轮 SFT、深度 7 合成 rollout；WMLA 每步最多分支 3 个动作并前瞻 1–3 层 |

---

## 核心方法

### 1. 用真实网页轨迹启动策略自训练

作者收集 Mind2Web 训练集以及 WebVoyager、Mind2Web 网站上的 self-instruct 查询，共 1,516 条。Llama-3.3-70B Agent 在真实网页上执行这些查询，再由同一基础模型判断任务是否完成，只保留通过筛选的轨迹。

第一批成功轨迹用于 SFT，得到 `self-improve (iter 1)`。随后用该模型再次采样，把新成功轨迹与第一轮数据合并，得到 `iter 2`。实验继续做了第三轮，以观察普通轨迹自训练是否还能持续提升。

这里的“自我改进”有两个边界：

- 成功标准仍由人为设计的评价提示和网页任务定义给出；
- 同一 70B 模型同时承担执行与训练阶段的筛选，不等于完全无外部监督。

### 2. 从同一批轨迹训练网页世界模型

世界模型的目标不是预测最终任务得分，而是学习一步网页转移：

```text
历史观察与动作 + 当前观察 + 当前动作
→ 转移解释
→ 下一网页观察
```

网页观察主要使用文本化 accessibility tree。作者把真实轨迹重排为世界模型训练样本，并让基础 LLM 先生成“动作为什么会导致该页面变化”的 transition rationale，再对 Llama-3.3-70B 做 SFT，得到 `world model (iter 1/2)`。

这种设计利用了预训练模型已有的网页常识。例如，即便训练轨迹没有覆盖 GitHub 搜索页的某个排序菜单，模型也可能凭预训练知识生成合理菜单项。但这也意味着世界模型可能生成“看似合理却与当时真实网页不一致”的内容。

### 3. 世界模型充当虚拟网页服务器

普通自训练最缺的是失败查询上的成功轨迹。WebEvolver 只针对真实采样中没有成功完成的查询生成合成轨迹：

1. 从初始观察—动作开始；
2. 世界模型预测下一观察；
3. 策略模型根据合成观察产生下一动作；
4. 两个模型交替推进，最多 7 步；
5. 若世界模型生成终止状态则提前结束；
6. 再用零样本 Llama-3.3-70B 做 rejection sampling；
7. 将通过筛选的合成轨迹与第一轮真实 SFT 数据合并，微调出最终 WebEvolver。

关键不是简单“让 LLM 编轨迹”，而是把动作与下一网页状态之间的转移建模成单独模型，并只为现有策略失败的查询补数据。

### 4. WMLA：推理时先想象再点击

World Model Look-ahead 在真实执行每个动作前进行有限深度搜索：

1. 策略模型生成最多 3 个不同候选动作；
2. 世界模型分别预测各动作导致的下一观察；
3. 若深度大于 1，再让策略模型基于合成观察继续动作，形成短前瞻轨迹；
4. GPT-4o 根据目标和前瞻结果给候选动作评分；
5. 只在真实网页中执行得分最高的第一个动作。

因此 WMLA 的提升不能只归因于“世界模型更懂网页”，还包含更多候选采样、额外模型调用和强评分器。深度 2 是论文中效果与误差之间的最佳点；深度继续增加后，合成页面误差会累积。

---

## 实验设计

### 模型与训练设置

- 策略基础模型：Llama-3.3-70B；
- 世界模型基础模型：Llama-3.3-70B；
- 训练查询：1,516 条；
- 普通自训练：最多 3 轮真实轨迹采样与 SFT；
- 合成轨迹：世界模型与策略模型交替生成，最长 7 步；
- 自训练筛选：零样本 Llama-3.3-70B；
- 正式任务评价：GPT-4o 二值自动评价；
- WMLA：最多 3 个候选动作，前瞻深度 1、2、3，GPT-4o 评分。

论文没有给出完整 GPU 数、总训练时长、总 token 数或 API 成本，因此不能把它与低成本 memory / prompt 更新方法做同预算比较。

### 数据集与环境

| 数据集 / 环境 | 作用 | 规模与特点 |
|---|---|---|
| Text-only WebVoyager | 主要真实网页评测 | 473 个过滤后查询，覆盖 11 类网站 |
| Mind2Web-Live-filtered | 主要真实网页评测 | 53 个查询，网站和页面随时间变化 |
| GAIA-web | 分布外、多步网页任务 | 报告 Level 1 与 Level 2 |
| SimpleQA + web agent | 分布外事实搜索 | 用网页 Agent 搜索答案 |
| 世界模型内部评测集 | 检查下一页面预测 | 按预测深度比较结构、相似度和整体可用性 |

由于地理位置和 IP 屏蔽，作者过滤了一些无法访问的网站，并在相近时间窗口重复实验两次取平均。这个处理提升了内部稳健性，但也使结果与原始 benchmark 全量设置不完全等价。

### 对比方法

- GPT-4o-mini、GPT-4o；
- 原始 Llama-3.3-70B；
- 三轮普通 self-improve；
- 不使用世界模型的 synthetic trajectory baseline；
- WebDreamer；
- 不同 WMLA 深度和分支数。

### 指标

- 任务成功率；
- 世界模型 Structural Correctness（生成 accessibility tree 的结构有效性）；
- Similarity（与真实页面内容的相似性）；
- Overall Assessment（功能和语义连贯性）；
- GAIA 与 SimpleQA 准确率。

---

## 主要结果

### 1. 普通自训练快速进入平台期

| 模型 | WebVoyager | Mind2Web-Live |
|---|---:|---:|
| Llama-3.3-70B | 32.98 | 18.86 |
| self-improve (iter 1) | 38.68 | 15.09 |
| self-improve (iter 2) | 38.23 | 16.98 |
| self-improve (iter 3) | 38.65 | 16.98 |

WebVoyager 上第一轮提升约 5.7 个百分点，之后基本不再增长。Mind2Web-Live 上普通自训练甚至没有稳定超过基础模型。这支持了论文的核心动机：继续重复相似的成功轨迹不足以拓宽能力边界。

### 2. 世界模型合成轨迹带来额外提升

| 模型 | WebVoyager | Mind2Web-Live |
|---|---:|---:|
| 不含世界模型的 Synthetic Trajectory | 38.98 | 18.86 |
| WebEvolver | 42.49 | 22.64 |

WebEvolver 相对第一轮自训练在 WebVoyager 再提高 3.81 个百分点，也超过普通合成轨迹。这说明“学习网页转移后再生成轨迹”比无世界模型的轨迹合成更有效。

但该表不能单独分离两个因素：世界模型可能提高了轨迹的网页一致性，也可能只是产生了更多、覆盖失败查询的新样本。论文没有给出严格相同有效样本数和 token 数下的消融。

### 3. WMLA 继续提高成功率，但成本显著增加

| 推理设置 | WebVoyager | Mind2Web-Live |
|---|---:|---:|
| WebEvolver | 42.49 | 22.64 |
| + WebDreamer | 44.61 | 22.64 |
| + WMLA，深度 1 | 46.24 | 28.30 |
| + WMLA，深度 2 | **51.37** | 24.53 |

深度 2 在 WebVoyager 最好；Mind2Web-Live 则是深度 1 最好，说明更深搜索并不稳定。WMLA 的最高结果使用多候选动作、世界模型 rollout 和 GPT-4o 评分，不能与单次贪心动作直接做等成本比较。

分支数消融也呈现平台期：`k=2/3/5` 在 WebVoyager 分别为 `48.62/51.37/50.73`，三个候选已基本覆盖有差异的动作。

### 4. 世界模型只适合短视野前瞻

世界模型总体 O/A 从基础 Llama-3.3-70B 的 38.77 提升到 iter-2 的 51.82；在深度 1 时 iter-2 达到 72.86，但深度至少 4 时降到 45.31。

这组结果很重要：世界模型不是越滚越远越好。它在一两步内可以帮助比较动作，长链预测会累积结构错误和内容幻觉，正好解释了 WMLA 深度增加后的边际收益下降。

### 5. 分布外结果有提升，但复杂推理仍薄弱

| 模型 | GAIA Level 1 | GAIA Level 2 | SimpleQA |
|---|---:|---:|---:|
| Llama-3.3-70B | 19.2 | 10.9 | 36 |
| WebEvolver | 30.7 | 17.2 | 48 |
| WebEvolver + WMLA | 34.6 | 17.2 | 58 |

Level 1 和 SimpleQA 提升明显；Level 2 在加 WMLA 后没有继续提高。作者也承认，当前系统主要训练动作生成，缺少独立规划模块，深层推理和长程任务不在训练范围内。

同时，GAIA 实验使用 GPT-4o 做任务分解、结果生成和计算，因此它证明的是混合系统中的 WebEvolver 组件有增益，不是纯 Llama Web Agent 独立完成全部任务。

---

## 消融、失败案例与成本

### 世界模型误差会沿前瞻深度累积

论文没有直接量化 hallucination rate。作者认为相似度与整体评估会间接反映幻觉，并推测某些“合理但不真实”的生成可能增加训练多样性。这个解释有启发，但证据不足：在真实网页操作中，错误按钮、过期价格或不存在的菜单也可能引导策略学习无效动作。

### 动态网页使严格复现困难

真实网站会修改 DOM、登录流程、地区内容、反爬策略和 CAPTCHA。作者通过相近时间窗口重复运行来缓解波动，但同一代码在数月后不一定获得相同结果。Mind2Web-Live 只有 53 个过滤后任务，单个任务变化会显著影响百分比。

### 训练与推理预算没有统一报告

至少包含：

- 1,516 个查询的真实浏览 rollout；
- 多轮成功筛选；
- 策略模型和世界模型分别做 70B SFT；
- 失败查询上的深度 7 合成 rollout；
- WMLA 每个真实动作最多 3 个分支、最多 2–3 层模拟；
- GPT-4o 评分与正式自动评价。

因此 WebEvolver 的结果更适合说明“世界模型路线可行”，不适合证明它比轻量 memory、prompt 或 context 更新更高效。

### 代码与数据公开，但缺少模型权重

官方仓库提供轨迹采样、策略 SFT 数据转换、世界模型数据构造、合成轨迹生成与评测脚本；Hugging Face 数据集提供策略模型和世界模型的 SFT 数据。当前未找到官方训练后权重，完整复现仍需自行训练两个 70B 模型并搭建浏览器与服务。

---

## 创新点与局限性

### 实际新增的机制

1. **一套世界模型，两种用途**：同一个模型既在训练时生成合成轨迹，又在推理时做动作前瞻。
2. **针对失败任务补轨迹**：合成数据不是无差别扩增，而是集中覆盖当前策略没有成功轨迹的查询。
3. **把网页预训练知识转化为状态转移**：模型不仅回答网页内容，还预测操作后 accessibility tree 如何变化。
4. **展示普通自训练的平台期**：多轮真实成功轨迹 SFT 的停滞，为引入世界模型提供直接对照。

### 主要局限

1. 世界模型只在短深度可靠，尚不能支撑长程规划。
2. 系统主要训练 action generation，没有独立 planner。
3. WMLA 使用 GPT-4o 评分，最高结果不是完全开源、同模型闭环。
4. GAIA 实验也依赖 GPT-4o 的任务分解和结果生成。
5. 动态网站与过滤设置削弱严格可复现性。
6. 没有统一报告训练时间、硬件、token 和每任务推理成本。
7. 未直接测量世界模型幻觉或因错误模拟导致的策略污染。
8. “跨任务”指参数在不同查询上复用，不代表持续部署中的长期学习、遗忘控制或版本治理。

---

## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 世界模型合成轨迹可以突破普通自训练平台期 | 普通 iter 1/2/3 在 WebVoyager 为 38.68/38.23/38.65，WebEvolver 为 42.49 | 普通多轮 self-improve、无世界模型 Synthetic Trajectory 38.98 | 在该数据和模型设置下，基于转移模型的合成轨迹比继续重复真实成功轨迹更有效 | 不能证明增益完全来自更准确的世界建模；样本量、覆盖度和训练 token 未严格等预算 |
| 世界模型可用于测试时动作前瞻 | WebEvolver 42.49，WMLA d=1 为 46.24，d=2 为 51.37 | WebDreamer 44.61 | 短深度模拟能够改善真实网页动作选择 | 不能证明低成本；WMLA 增加分支和调用，并使用 GPT-4o 评分 |
| 策略模型和世界模型可以形成互相促进的数据闭环 | 真实轨迹训练两者，世界模型再给策略产生失败任务轨迹 | 只训练策略、普通轨迹合成 | 支持交替训练闭环的可行性 | 没有做完全解耦的交叉实验，不能量化每个反馈方向的独立贡献 |
| 世界模型获得了可用的网页转移能力 | iter-2 总体 O/A 51.82，深度 1 O/A 72.86 | GPT-4o 37.85、基础 Llama 38.77 | 微调显著改善短步下一页面预测 | 不能证明其忠实复制实时网站；深度≥4 的 O/A 已降到 45.31，且幻觉未直接测量 |
| 改进可迁移到其他网页任务 | GAIA L1 19.2→30.7、SimpleQA 36→48；WMLA 后 34.6/58 | 原始 Llama 与普通 iter | 支持对未见查询和 Bing 搜索的迁移 | GAIA 管线依赖 GPT-4o，Level 2 提升有限，不能代表通用长程 Web Agent |
| 不需要更强闭源模型蒸馏即可自训练 | 真实与合成轨迹筛选使用 Llama-3.3-70B 自身 | 使用强教师蒸馏的方法 | 训练数据闭环没有把 GPT-4o 轨迹作为教师数据 | 最高 WMLA 与 GAIA 系统仍调用 GPT-4o；“无闭源蒸馏”不等于“全流程无闭源依赖” |

### 我的判断

WebEvolver 最有价值的地方不是“把世界模型接到 Agent 上”这一口号，而是明确展示了两个可检验现象：

- 真实成功轨迹的重复 SFT 很快饱和；
- 世界模型只在短步预测上可靠，却足以用于有价值的数据扩增和局部动作选择。

它把世界模型从“宏大的环境模拟器”收窄为一个实用部件：预测下一小段 accessibility tree。这个尺度选择较合理，也让失败模式可以通过深度消融直接观察。

不过，论文把训练时数据扩增和测试时搜索放在同一套最终系统里，容易让读者把 51.37 全部理解为参数级自我改进。更公平的结论是：**WebEvolver 参数训练本身把 WebVoyager 从 32.98 提升到 42.49；额外的测试时搜索与强评分器进一步推到 51.37。**

### 其他可能解释

- 世界模型的主要价值可能是增加失败任务覆盖，而不一定是精确模拟网页；需要等样本数、等 token 的随机或规则合成对照。
- 第一轮 self-improve 的提升可能部分来自格式遵循和任务熟悉，而不是更强的通用网页推理。
- WMLA 的收益可能来自 best-of-3 搜索和 GPT-4o 评分器，而非世界模型独立贡献；需要无世界模型但同分支、同评分预算的对照。
- GPT-4o 自动评价可能偏好语言上更完整的轨迹，且不能完全替代网站内部状态或人工核验。
- 动态网站的时间差、可访问网站过滤和小规模 Mind2Web-Live 可能造成结果波动。
- 合成页面的“有益幻觉”也可能是数据污染；短期 benchmark 提升不能证明长期部署不会积累错误网页知识。

---

## 工程启发

### 1. 世界模型不必复刻整个环境

对复杂软件或网页 Agent，可以先训练局部转移模型：

```text
当前界面摘要 + 动作 → 下一界面摘要
```

只要它在一两步内足够可靠，就能用于候选动作筛选和失败任务数据扩增，不必先解决完整数字孪生。

### 2. 合成数据应优先覆盖当前策略的失败区

WebEvolver 只为未成功查询生成合成轨迹。这个原则可迁移到代码、Office、数据库和 GUI Agent：先识别真实 rollout 的空白区，再定向制造训练数据，而不是平均扩增所有任务。

### 3. 训练增益与测试时搜索必须分账

工程评估至少应分别报告：

- 单次策略执行；
- 训练后策略执行；
- 加候选采样；
- 加世界模型前瞻；
- 加外部评分器；
- 每项的 token、延迟和 API 成本。

否则无法判断提升来自能力学习还是更多推理预算。

### 4. 长前瞻前先校准世界模型误差

本论文中深度超过 2 后预测明显退化。实际系统应把世界模型的可信深度当成一个需要在线估计的变量，低置信度时缩短前瞻或回到真实环境，而不是固定滚动很长轨迹。

---

## 未解决问题与研究想法

1. 能否用真实网页状态校准世界模型置信度，并自动决定前瞻深度？
2. 合成轨迹的收益来自状态真实性、动作多样性还是失败任务覆盖？需要等预算拆分实验。
3. 如何检测和删除由过期网页知识产生的错误合成轨迹？
4. 能否把世界模型从 accessibility tree 扩展到视觉、表单状态和登录态，同时保持可审计性？
5. 能否用开源 verifier 或环境状态替代 WMLA 的 GPT-4o 评分器？
6. 长期部署时，策略模型与世界模型更新频率是否应不同？如何避免一个模型的错误放大到另一个模型？
7. 世界模型能否输出“不知道”或多个可能后继状态，而不是单一确定页面？
8. 在固定 wall-clock、token 和真实网页访问次数下，世界模型路线是否优于外部经验库或 context 更新？

---

## 论文外部信息

### 基本信息

- 正式标题：WebEvolver: Enhancing Web Agent Self-Improvement with Co-evolving World Model
- 作者：Tianqing Fang、Hongming Zhang、Zhisong Zhang、Kaixin Ma、Wenhao Yu、Haitao Mi、Dong Yu
- 机构：Tencent AI Lab
- 正式发表：EMNLP 2025 Main Conference
- 页码：8959–8975
- DOI：10.18653/v1/2025.emnlp-main.454
- arXiv：2504.21024，v1 为 2025-04-23，v2 为 2025-08-21
- 官方代码：已公开，仓库许可证为 MIT
- 官方数据：Hugging Face 数据集已公开，包含策略模型与世界模型的 SFT 数据
- 官方模型权重：截至 2026-06-29 未在论文页、官方仓库或数据页找到明确发布链接

### 图片与许可

本笔记未复制论文图片。ACL Anthology 的 2016 年后论文采用 CC BY 4.0，官方代码仓库采用 MIT；但当前正文用文字和表格已经能完整解释核心机制，因此没有新增本地图片资产，也无需修改图片 manifest 与 inventory。

### 复现入口

官方代码给出了：

- OpenWebVoyager 查询准备和真实轨迹采样；
- 从轨迹生成策略模型 SFT 数据；
- 蒸馏 transition rationale 并构造世界模型 SFT 数据；
- 策略模型与世界模型交替生成合成轨迹；
- WebVoyager、Mind2Web、GAIA、SimpleQA 的推理与自动评价入口。

完整复现仍需两个可服务的 70B 模型、浏览器和网页环境、训练框架以及 GPT-4o / Azure OpenAI 配置。

---

## 参考资料与 BibTeX

1. [ACL Anthology 正式论文页](https://aclanthology.org/2025.emnlp-main.454/)
2. [ACL Anthology PDF](https://aclanthology.org/2025.emnlp-main.454.pdf)
3. [arXiv:2504.21024](https://arxiv.org/abs/2504.21024)
4. [官方代码：Tencent/SelfEvolvingAgent/WebEvolver](https://github.com/Tencent/SelfEvolvingAgent/tree/main/WebEvolver)
5. [官方数据：CognitiveKernel/WebEvolver](https://huggingface.co/datasets/CognitiveKernel/WebEvolver)

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{fang-etal-2025-webevolver,
  title = "{W}eb{E}volver: Enhancing Web Agent Self-Improvement with Co-evolving World Model",
  author = "Fang, Tianqing and Zhang, Hongming and Zhang, Zhisong and Ma, Kaixin and Yu, Wenhao and Mi, Haitao and Yu, Dong",
  editor = "Christodoulopoulos, Christos and Chakraborty, Tanmoy and Rose, Carolyn and Peng, Violet",
  booktitle = "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing",
  month = nov,
  year = "2025",
  address = "Suzhou, China",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/2025.emnlp-main.454/",
  doi = "10.18653/v1/2025.emnlp-main.454",
  pages = "8959--8975",
  ISBN = "979-8-89176-332-6"
}
```

</details>
