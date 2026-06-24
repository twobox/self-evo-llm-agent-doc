<!--
metadata:
  schema_version: '1.0'
  title: 'From Player to Master: Enhancing Test-Time Learning of LLM Agents via Reinforcement Learning over Memory'
  short_title: 'MemoPilot'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'method'
  paper_status: 'accepted'
  venue: 'ICML 2026'
  venue_track: ''
  evolution_object: 'Memory Update Policy / External Memory'
  learning_stage: 'mixed'
  parameter_update: 'auxiliary-only'
  cross_task: 'yes'
  arxiv_id: '2606.08656'
  arxiv_version: 'v1'
  arxiv_url: 'https://arxiv.org/abs/2606.08656'
  pdf_url: 'https://arxiv.org/pdf/2606.08656'
  html_url: 'https://arxiv.org/html/2606.08656v1'
  project_url: ''
  code_url: ''
  original_code_url: ''
  resource_url: ''
  model_url: ''
  code_status: 'claimed_public_link_missing'
  model_status: 'not_found'
  first_submitted: '2026-06-07'
  last_revised: ''
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-24'
  authors:
    - 'Yishuo Cai'
    - 'Xingyu Guo'
    - 'Xuancheng Huang'
    - 'Jinhua Du'
    - 'Can Huang'
    - 'Wenxuan Huang'
    - 'Wenhan Ma'
    - 'Yuyang Hu'
    - 'Aohan Zeng'
    - 'Jie Tang'
    - 'Xu Sun'
  institutions:
    - 'Peking University'
    - 'Central South University'
    - 'Zhipu AI'
    - 'Tsinghua University'
    - 'East China Normal University'
    - 'Renmin University of China'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Agent Memory'
    - 'Test-Time Learning'
    - 'RL for Agent'
    - 'Memory Update Policy'
    - 'Multi-turn GRPO'
    - 'Context Engineering'
  tags:
    - 'self-evolving-agent'
    - 'agent-memory'
    - 'test-time-learning'
    - 'reinforcement-learning'
    - 'grpo'
    - 'memory-updater'
    - 'icml-2026'
  related_notes:
    - 'notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md'
    - 'notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'notes/harness-updating-is-not-harness-benefit.md'
    - 'notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md'
  created: '2026-06-15'
  updated: '2026-06-24'
-->

# 《From Player to Master: Enhancing Test-Time Learning of LLM Agents via Reinforcement Learning over Memory》读书笔记

> 论文：**From Player to Master: Enhancing Test-Time Learning of LLM Agents via Reinforcement Learning over Memory**  
> arXiv：<https://arxiv.org/abs/2606.08656>  
> PDF 下载地址：<https://arxiv.org/pdf/2606.08656>  
> arXiv HTML：<https://arxiv.org/html/2606.08656v1>  
> 官方项目页：暂未找到  
> 官方代码仓库：论文摘要称 “code is publicly available here”，但当前笔记尚未补入具体链接
> 模型权重：暂未找到  
> 当前状态：arXiv v1，提交时间为 **2026-06-07**；arXiv 页面 comments 标注为 **Accepted by ICML 2026**。

---


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

## 1. 论文外部信息

### 1.1 投稿与发表状态

这篇论文在 arXiv 上的编号是 **arXiv:2606.08656**，分类为 **Computation and Language (cs.CL)**。arXiv 页面显示提交时间为 **2026-06-07**，comments 中写明：

> Accepted by ICML 2026

所以它不是只停留在普通预印本状态，而是可以暂时定位为：

> 一篇已经被 **ICML 2026** 接收的 Agent Memory / Test-Time Learning / RL for Agent 方向论文，arXiv 版本是公开稿。

如果后续正式会议页面、OpenReview 页面、代码仓库或模型权重发布，可以再补充到本笔记和 README 索引中。

```bibtex
@misc{cai2026fromplayertomaster,
  title={From Player to Master: Enhancing Test-Time Learning of LLM Agents via Reinforcement Learning over Memory},
  author={Yishuo Cai and Xingyu Guo and Xuancheng Huang and Jinhua Du and Can Huang and Wenxuan Huang and Wenhan Ma and Yuyang Hu and Aohan Zeng and Jie Tang and Xu Sun},
  year={2026},
  eprint={2606.08656},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2606.08656}
}
```

### 1.2 作者与机构

arXiv 页面可以确认论文作者列表，PDF 首页则已经给出了完整作者机构。另一个需要区分的点是：论文致谢部分提到 **This work was done during the first author’s internship at Zhipu AI**，这说明第一作者在智谱 AI 实习期间完成了该工作，但并不等于整篇论文只有这一个机构来源。

| 作者 | 机构 / 备注 |
|---|---|
| Yishuo Cai | Peking University |
| Xingyu Guo | Central South University |
| Xuancheng Huang | Zhipu AI |
| Jinhua Du | Tsinghua University |
| Can Huang | Zhipu AI |
| Wenxuan Huang | East China Normal University |
| Wenhan Ma | Peking University |
| Yuyang Hu | Renmin University of China |
| Aohan Zeng | Tsinghua University |
| Jie Tang | Tsinghua University |
| Xu Sun | Peking University |

这也说明这篇工作更准确的外部定位应当是：以北大、清华、智谱等机构共同参与的多方合作论文，而不是“机构暂不明确，只知道第一作者和智谱 AI 有关联”。

### 1.3 作者背景和研究圈子观察

由于当前可查页面没有完整机构列表，这里只能做**粗略判断**，不要把下面内容当作最终作者履历。

从论文题目、方法和实验看，这篇工作处在以下几个研究圈子的交叉处：

1. **LLM Agent Memory / Experience Learning**：论文直接研究 agent 如何在测试时通过显式 memory 吸收连续交互经验。
2. **RL for Agent / GRPO 训练**：论文不是只用 prompt 让模型写记忆，而是把 memory updater 当成可训练策略，用 multi-turn GRPO 优化。
3. **Test-Time Learning / Lifelong Agent Evaluation**：论文把 agent 面对连续任务流时的性能提升作为核心问题，而不是只看单次任务成功率。
4. **Agent 系统工程**：论文采用“冻结 player + 外部 memory copilot”的设计，这和真实系统中外挂 memory / advisor / context module 的工程方式很接近。

这篇论文可以和仓库中已有几篇文章建立关系：

- 和 **From Storage to Experience** 的关系：它是“从存储到经验”这条线上的一个具体方法，把 memory update 从启发式规则推进到可训练策略。
- 和 **EvolveR** 的关系：两者都关注经验驱动改进，也都用 RL；但 EvolveR 更像问答 / search agent 的 experience base 生命周期，MemoPilot 更集中在“训练 memory 更新器，使冻结 agent 在连续交互中变强”。
- 和 **Harness Updating Is Not Harness Benefit** 的关系：Harness Updating 提醒我们“写了 memory 不等于 solver 会用”；MemoPilot 的目标正是通过下游奖励训练 memory，让 memory 更可执行、更能被 frozen player 用起来。
- 和 **Agentic Context Engineering** 的关系：ACE 把 context playbook 当成可维护资产，MemoPilot 则进一步把 memory 的写入策略作为 RL policy 来训练。

---

## 2. 研究方向与论文定位

### 2.1 所属方向

这篇论文属于 **Self-Evolving LLM Agent / Agent Memory / Test-Time Learning / RL for Agent** 的交叉方向。

它研究的问题不是“LLM 会不会玩游戏”，而是：

> 一个冻结的 LLM agent 在部署时连续遇到相关任务，能不能通过外部 memory 的在线更新，在不改模型参数的情况下越做越好？

这里的重点是 **test-time learning**。也就是说，agent 在测试或部署阶段接收一串相关交互，每次只能看到过去，不能看到未来；它需要从前几次交互中识别规律，把规律写成 memory，再在后续交互中利用。

### 2.2 论文定位

这篇论文可以概括为：

> 不是训练 player 本身，而是训练一个外部 memory copilot，让它学会如何把连续交互轨迹压缩成对 frozen player 真正有用的行动建议。

论文提出的方法叫 **MemoPilot**。它的核心思想是：

```text
连续交互轨迹 e_t
    ↓
可训练 memory model G_θ 更新 memory m_t
    ↓
冻结 player π 在下一局/下一轮任务中读取 memory
    ↓
环境给出 reward
    ↓
memory model 用 multi-turn GRPO 学习“怎么写 memory 才能提高后续表现”
```

这和普通“让 LLM 反思一下并写入记忆”有明显区别：

| 维度 | 启发式记忆更新 | MemoPilot |
|---|---|---|
| 更新规则来源 | 人写 prompt / 人工规则 | 下游 reward 训练出来 |
| 优化目标 | 看起来像总结 / 反思 | 让 frozen player 后续表现更好 |
| 记忆形式 | 往往是自由文本 | 三层结构：识别、维护、行动指导 |
| 学习方式 | 不训练或只靠提示词 | multi-turn GRPO |
| 适用目标 | 保存经验 | 训练可执行、可验证、可迁移的 memory update policy |

---

## 3. 核心问题

论文的核心问题可以拆成三层。

### 3.1 第一层：测试时学习不能只靠“把历史塞进上下文”

在连续交互任务里，一个直接方案是把完整历史放到上下文中，让 agent 自己看过去发生了什么。

但论文实验显示，**Full History** 并不稳定，甚至会比 No Memory 更差。这说明历史越长不一定越有用，因为历史里既有信号，也有噪声、偶然结果、无关细节和误导性样本。

所以真正需要的是：

> 从历史轨迹中筛出对下一步决策最有用的信息，并压缩成可执行指导。

### 3.2 第二层：prompt-based memory update 不一定能对齐下游目标

已有 memory agent 常见做法是：

- Reflexion：做完一次任务后写反思；
- ExpeL：抽取成功/失败经验；
- MemoryBank：保存和检索长期记忆；
- AWM / ReasoningBank：维护工作流或推理经验。

这些方法很有启发，但很多更新规则仍然依赖人工设计 prompt。问题是：

> memory 写得“像反思”不代表 frozen player 读了之后真的会变强。

MemoPilot 要解决的正是这个 gap：让 memory 的写入方式被下游任务奖励直接塑形。

### 3.3 第三层：长期 credit assignment 很难

这里的 **credit assignment** 可以先翻译成“功劳 / 责任分配”：训练时看到后面某一轮成功或失败，要判断到底是哪一次 memory update 导致了这个结果。

在 MemoPilot 里，这个问题尤其容易误读。因为第 `t` 次 memory update 不是先发生、再影响第 `t` 轮；它是在第 `t` 轮结束后才发生，所以它最直接影响的是下一轮。

更准确的时间顺序是：

```text
第 t 轮：
  1. player π 读取旧 memory m_{t-1}
  2. player 与环境 / 对手交互
  3. 环境返回轨迹 e_t 和奖励 r_t
  4. memory updater G_θ 读取 e_t 和 m_{t-1}
  5. 写出新的 memory m_t

第 t+1 轮：
  6. player π 读取新的 memory m_t
  7. player 再次交互
  8. 环境返回下一轮奖励 r_{t+1}
```

所以，第 `t` 次 memory update 的直接效果，不应该主要看已经发生过的 `r_t`，而应该看它写出来的 `m_t` 在下一轮有没有帮到 player，也就是看 `r_{t+1}`。

这就是论文里的关键训练设计：

> 用 **turn-wise reward / one-step proxy reward**，把第 `t` 次 memory update 主要归因到下一次交互的 reward。

可以把它理解成下面这个近似：

```text
复杂目标：
第 t 次 memory update 对未来很多轮总收益到底贡献了多少？

MemoPilot 的简化目标：
第 t 次 memory update 写出的 m_t，是否让第 t+1 轮表现更好？
```

举个石头剪刀布的例子：

```text
第 1 轮结束后，memory updater 写入：
“对手连续出石头，下一轮优先出布。”

第 2 轮，player 读到这条 memory，真的出布并赢了。

训练时就把第 2 轮的好结果，主要归因给第 1 轮之后的这次 memory update。
```

它没有试图完整回答“这条 memory 对第 3、4、5 轮总成绩分别贡献多少”。这当然牺牲了一部分长期归因的完整性，但好处是训练信号更近、更清楚、方差更低。

对扑克这类随机性更强的环境尤其如此。如果第 1 局写入的 memory 到第 5 局才表现变好，中间可能混入随机牌面、下注噪声、对手策略波动等因素。直接用整段累计回报训练，会很难判断到底是哪一次 memory update 起了作用。

这里几个术语可以对应起来：

| 术语 | 在这篇论文里的直观含义 |
|---|---|
| **turn-wise reward** | 每一轮单独计算 reward，不只看整段 episode 的总 reward |
| **one-step proxy reward** | 用“下一轮 reward”近似衡量这次 memory update 的质量 |
| **credit assignment** | 判断成功 / 失败应该归因到哪一次 memory update |
| **proxy** | 代理指标 / 近似指标，不是完整长期目标，但更容易训练 |

一句话总结：

> MemoPilot 不直接要求 memory updater 学会优化很长未来的总收益，而是先让它学会：**我这次写的 memory，下一轮能不能立刻帮到 frozen player。**

---

## 4. 方法或系统设计

### 4.1 总体框架：MemoPilot

MemoPilot 由两个角色组成：

| 组件 | 是否训练 | 作用 |
|---|---|---|
| Frozen player π | 不训练 | 负责实际执行任务 / 玩游戏 / 做决策 |
| Memory model G_θ | 训练 | 根据上一轮轨迹和旧 memory 生成新 memory |

每一轮的过程可以写成：

```text
m_0 = 空
第 t 轮：
  1. player π 根据当前 memory m_{t-1} 执行任务或对局
  2. 环境返回轨迹 e_t 和奖励 r_t
  3. memory model G_θ 读取 e_t 和 m_{t-1}
  4. 生成更新后的 memory m_t
  5. m_t 作为下一轮 player 的外部指导
```

重要的是：**所有跨轮次学习都发生在 memory 里，player 参数不变**。

这让 MemoPilot 更像一个可插拔的“记忆驾驶员”或“策略副驾驶”：它不改变驾驶员本体，但不断给驾驶员更新战术提示。

### 4.2 把 memory updating 建模成 MDP

论文把 memory update 看成一个多轮决策问题：

| MDP 元素 | 在本文中的含义 |
|---|---|
| State | 当前交互轨迹 `e_t` + 上一轮 memory `m_{t-1}` |
| Action | 生成新的文本 memory `m_t` |
| Transition | frozen player 根据 `m_t` 与环境/对手交互，产生下一轮轨迹和奖励 |
| Reward | 下一轮或当前任务定义的分数，例如 RPS 分差、LHE chip、StreamBench pass@4 |

这个建模的关键在于：memory 不是静态数据库，而是一个会影响未来行为的策略动作。

### 4.3 三层 memory 结构

论文为 memory 设计了三层结构，避免 free-form memory 太散：

| 层次 | 作用 | 可以怎么理解 |
|---|---|---|
| Identification / diagnostic analysis | 分析近期交互证据，识别对手或任务模式 | “我现在观察到了什么？” |
| Maintenance / belief state | 维护假设、置信度、证据和验证状态 | “我当前相信什么？证据够不够？” |
| Guidance / actionable prompt | 给 frozen player 的下一步行动建议 | “下一局具体应该怎么做？” |

这个设计和仓库里 ACE 的 playbook 思路有相通之处：不要只写一段自然语言总结，而要把 memory 拆成可维护、可验证、可执行的结构。

论文还指出，只有 `FINAL_STRATEGY_PROMPT` 部分会暴露给 player，而完整 cheatsheet 会继续传给 memory updater。这一点很有工程意义：

> memory updater 可以保留更多内部诊断信息，但执行 agent 只需要看到简洁可执行的策略。

### 4.4 multi-turn GRPO 训练

MemoPilot 使用 **multi-turn GRPO** 训练 memory model。训练时对同一个对手策略采样多个 rollout，每个 rollout 包含多局连续交互。

核心改动有两个：

1. **turn-wise reward**：第 `t` 次 memory 更新不直接使用整段累计回报，而是使用下一局 reward 作为 proxy return，即 `R_{i,t}=r_{i,t+1}`。
2. **turn-level advantage**：在同一 turn 的多个 rollout 之间做 **context-independent, group-normalized advantage estimation**，而不是只对整条 episode 做总回报比较。

这里的 `R_{i,t}=r_{i,t+1}` 就是上一节解释的 one-step proxy reward。它的意思不是“第 `t` 轮的 reward 训练第 `t` 次 update”，而是：

```text
第 i 条 rollout 中：
第 t 次 memory 写法 m_t
    ↓
影响第 t+1 轮 player 行为
    ↓
用第 t+1 轮奖励 r_{i,t+1}
近似评价这次 memory update 好不好
```

再结合 GRPO 的 group 比较，可以理解成：

```text
同一个对手策略下：
  rollout 1 第 t 次 memory 写法 → 下一局得分
  rollout 2 第 t 次 memory 写法 → 下一局得分
  rollout 3 第 t 次 memory 写法 → 下一局得分
  ...

比较这些“同一位置的 memory 写法”谁带来更好的下一局结果，
再更新 memory model。
```

这种训练方式的好处是：

- credit assignment 更细：每次 memory update 都有更近的反馈；
- 训练方差更低：不把很久之后的随机波动都算到早期 update 头上；
- 更符合 memory updater 的真实作用链：写 memory → 下一轮 player 使用 → 下一轮 reward 变化。

论文的 reward ablation 也支持这一点：在 LHE@5 上，cumulative reward 只有 0.61，而 one-step reward 达到 2.03。

---

## 5. 实验设计

### 5.1 实验对象 / Agent 类型

论文主要评估的是：

> 冻结 LLM player + 可训练 memory updater 的 test-time learning agent。

其中 player 在训练和测试时都不更新参数。训练的是外部 memory model。

默认训练中使用：

- MemoPilot base model：**Qwen2.5-14B-Instruct**；
- 训练时 player：**Qwen2.5-14B-Instruct**；
- 泛化评估还把训练好的 memory model 接到更强 player：**Qwen3-235B-A22B**。

### 5.2 核心任务

论文有三类评测：

| 任务 / 环境 | 作用 |
|---|---|
| Multi-round Rock-Paper-Scissors (RPS) | 小动作空间，但通过多轮历史构造可学习的对手模式 |
| Limit Texas Hold’em (LHE) | 不完全信息、随机性更强，更能测试 memory 是否能维护和修正假设 |
| StreamBench | 连续任务 benchmark，用于观察方法是否能从游戏迁移到真实任务流 |

RPS 来自 TextArena，LHE 来自 RLCard。StreamBench 中论文使用了两个任务来源：**CoSQL database** 和 **DS-1000 Python library**。

### 5.3 训练数据或更新方式

训练数据不是普通静态问答数据，而是通过可控对手池生成的多轮交互轨迹。

对手构造有三个原则：

1. **Controllability**：对手由可执行自然语言策略定义，方便复现。
2. **Behavioral diversity**：RPS 覆盖固定序列、一步反应、多步反制；LHE 覆盖下注频率偏置、阶段性激进、诱捕等模式。
3. **Mechanism-based train-test separation**：训练和测试对手在机制上分离，测试对手保留战略意图但改变触发条件或表现形式。

论文附录给出的规模是：

| 环境 | 训练对手 | held-out 对手 |
|---|---:|---:|
| RPS | 32 | 32 |
| LHE | 45 | 9 |

### 5.4 Baseline

论文比较了三类 baseline。

| 类别 | 方法 |
|---|---|
| 基础方法 | No Memory、Full History、Human-Written Counter-Strategy |
| 既有 memory / experience 方法 | Reflexion、ExpeL、MemoryBank、AWM、ReasoningBank |
| 强模型 memory updater | Memory w/ Qwen2.5-7B、Memory w/ Qwen2.5-14B、Memory w/ DeepSeek-V3.2、Memory w/ Gemini-3.0-Flash |

需要注意的是：很多“以前的方法”在本文中被重新实现到 sequential-game setting 里，并使用相同 memory budget 做比较，因此它们不是原论文原始 benchmark 数字，而是本文实验设置下的复现式比较。

### 5.5 评价指标

| 指标 | 含义 |
|---|---|
| RPS@k | 连续 k 局 RPS 的平均每局分差 |
| LHE@k | 连续 k 局 LHE duplicate match 的平均每局 chip |
| mean@64 | 对 64 次 evaluation runs 取平均 |
| Elo rating | 对 memory methods 做 head-to-head 后的强度排名 |
| StreamBench overall accuracy (pass@4) | 按各 turn 汇总的平均通过率 |

论文主表报告的是 **RPS@5 / LHE@5**。

---

## 6. 主要实验结论

### 6.1 MemoPilot 在 RPS 和 LHE 上显著优于 memory-free 和 prompt-based memory

主结果中，使用 Qwen2.5-14B-Instruct 作为 frozen player 时：

| 方法 | RPS@5 | LHE@5 |
|---|---:|---:|
| No Memory | 0.43 | -1.36 |
| Full History | 0.02 | -1.22 |
| Human-Written Counter-Strategy | 1.00 | 1.08 |
| Memory w/ Qwen2.5-14B-Instruct | 0.21 | -0.23 |
| Memory w/ MemoPilot | **3.28** | **2.03** |

这说明几个点：

1. 只把历史塞进去不够，甚至可能引入噪声。
2. 让强模型按 prompt 更新 memory，也不一定稳定。
3. 训练出来的 memory updater 能写出更适合 frozen player 执行的策略。

### 6.2 MemoPilot 可以迁移到更强 frozen player

虽然训练 memory model 时 player 是 Qwen2.5-14B-Instruct，但测试时接到 **Qwen3-235B-A22B** 后仍然有效：

| 方法 | Qwen3 RPS@5 | Qwen3 LHE@5 |
|---|---:|---:|
| Memory w/ Qwen2.5-14B-Instruct | 0.34 | -0.29 |
| Memory w/ MemoPilot | **3.27** | **1.31** |

这表明 MemoPilot 学到的不是只服务于某个模型的表面 prompt，而是较通用的 memory update 行为。

### 6.3 StreamBench 上也有提升，但提升幅度更温和

在 StreamBench 上，MemoPilot 也优于 No Memory、Full History 和 prompt-based memory updater：

| 方法 | CoSQL | DS-1000 |
|---|---:|---:|
| No Memory | 69.5 | 50.0 |
| Full History | 70.0 | 52.5 |
| Memory w/ DeepSeek-V3.2 | 67.5 | 50.0 |
| Memory w/ Qwen2.5-14B | 66.0 | 48.8 |
| Memory w/ MemoPilot | **73.5** | **56.3** |

这组结果说明方法不只是在游戏上有效，但也要注意：StreamBench 部分是扩展评估，规模是 32 个 held-out episodes，每个 episode 5 个连续任务，因此还不能过度外推到所有真实 agent 场景。

### 6.4 Memory 的“可执行性”比“语义正确”更关键

论文做了一个很有价值的对照：给 player 提供 ground-truth opponent strategy，效果不如 MemoPilot。

| Memory Input | RPS@5 | LHE@5 |
|---|---:|---:|
| No Memory | 0.43 | -1.36 |
| Ground-Truth Opponent Strategy | 0.75 | -0.48 |
| Human-Written Counter-Strategy | 1.00 | 1.08 |
| MemoPilot | **3.28** | **2.07** |
| + Rewrite w/ DeepSeek-V3.2 | 3.12 | 1.65 |

这个实验非常重要，因为它说明：

> 记忆不只是“说对了对手策略”，还要把策略转换成 frozen player 真正能执行的行动提示。

这也和 Harness Benefit 的观点吻合：外部组件写得对，不代表下游模型会用。

### 6.5 三层结构和 RL 都重要

LHE@5 的 memory format ablation：

| 方法 | LHE@5 |
|---|---:|
| No Memory | -1.36 |
| Full History | -1.22 |
| 3-tier memory w/o RL | -0.23 |
| Free-form memory w/ RL | 1.04 |
| 3-tier memory w/ RL | **2.03** |

可以看出：

- 没有 RL，只靠三层格式，收益有限；
- 有 RL，即使 free-form memory 也能提升；
- 最好的是 **结构化 memory + RL 训练**。

### 6.6 主要失败模式：记忆维护和快速修正之间的矛盾

论文指出 MemoPilot 的主要失败模式是 **maintenance–refinement tradeoff**：

- 如果环境有随机性，memory 不能因为单次异常就立刻推翻旧假设；
- 但如果对手真的改变策略，memory 又不能太保守。

在 LHE 中，对手切换越频繁，性能越下降：

| 设置 | LHE@5 |
|---|---:|
| No Memory | -1.36 |
| Same opponent | 2.03 |
| Opponent switches every 5 games | 1.76 |
| Opponent switches every 2 games | 1.21 |
| Opponent with Memory (DeepSeek-V3.2) | 1.25 |

这说明 MemoPilot 适合“过去经验有可复用规律”的场景；面对高度非平稳或对抗性适应环境，仍然需要更强的遗忘、重置、漂移检测或多假设维护机制。

---

## 7. 工程启发

### 7.1 Memory 应该被看作可训练的 policy，而不是只看作数据库

很多 agent memory 工程默认是：

```text
保存历史 → 检索相似历史 → 拼进 prompt
```

MemoPilot 提醒我们，memory update 本身也是一个决策问题：

```text
什么该保留？
什么该删除？
什么是假设？
什么是已确认规律？
什么该暴露给执行 agent？
怎么写才能让执行 agent 真正照做？
```

这些问题不一定能靠手写 prompt 解决，未来可以考虑用 reward 或偏好信号训练 memory writer。

### 7.2 对执行 agent 只暴露“行动层 memory”

论文的三层 memory 很适合工程复用：

```text
内部 memory：诊断 + 证据 + 假设 + 置信度
外部 memory：给 executor 的短策略提示
```

这比把全部反思过程都塞给 executor 更清晰，也能减少 token 成本和干扰。

### 7.3 Full History 不是 Memory 的上限，而可能是噪声源

从实验看，Full History 很弱。这对 agent 系统开发有一个直接提醒：

> 不要把“上下文窗口更长”误当作“agent 记忆更好”。

长期系统需要的是选择性记忆、结构化记忆和可执行记忆，不是无限追加历史。

### 7.4 Reward 设计要尽量靠近 memory update 的直接后果

在多轮 agent 任务里，如果把很久之后的成功都回传给早期 memory，训练信号可能很噪。MemoPilot 的 one-step reward 给了一个实用启发：

> 对 memory update 这种中间组件，先用局部、低方差、可归因的 reward 训练，可能比追求完整长期回报更稳定。

### 7.5 这类方法适合插件化部署

MemoPilot 不训练 player，意味着它有机会作为外挂模块服务于：

- 闭源模型；
- 多个不同规模的执行模型；
- 多个环境中的任务流；
- 需要在线适应但不方便频繁微调主模型的 agent 系统。

这对工业系统很重要：主模型可能由第三方 API 提供，无法微调；但 memory updater 可以作为自有模块持续优化。

---

## 8. 局限性

### 8.1 场景依赖明确 reward

MemoPilot 训练需要下游 reward。RPS、LHE、StreamBench 都有比较明确的结果反馈。但很多真实 agent 场景里 reward 可能是：

- 延迟反馈；
- 稀疏反馈；
- 主观反馈；
- 多目标反馈；
- 难以自动验证的用户满意度。

如果没有可靠 reward，multi-turn GRPO 训练就会困难。

### 8.2 主要实验仍偏可控环境

RPS 和 LHE 很适合研究 test-time learning，因为对手策略可控、reward 明确、可重复评测。但它们和真实 Web Agent、Code Agent、Office Agent、Tool-use Agent 还有距离。

StreamBench 扩展评估提供了迁移证据，但规模和任务类型仍有限。

### 8.3 代码链接在当前笔记中尚未补全

论文摘要明确写了 **Our code is publicly available here**，所以严格来说，不能把它写成“暂未找到代码”。更准确的说法是：**论文声称已公开代码，但当前笔记尚未补入具体仓库链接**。在这种情况下，复现时仍然会遇到几个实际问题：

- 对手池构造细节需要完整代码；
- multi-turn GRPO 训练环境需要 rollout 框架；
- RPS / LHE / StreamBench 的统一接口需要实现；
- Qwen2.5-14B / Qwen3-235B / DeepSeek / Gemini 等模型调用成本较高。

### 8.4 Memory budget 固定为 512 tokens

论文为公平比较设置了 512-token memory budget。这个设置有利于实验控制，但真实系统中 memory 长度、压缩策略、分层索引和历史归档都会更复杂。

### 8.5 非平稳对手下仍会退化

当对手频繁切换或对手自己也有 memory 时，MemoPilot 表现下降。这提示真实系统需要额外机制：

- drift detection；
- memory reset；
- 多假设并行维护；
- 对 memory item 做时效性衰减；
- 区分稳定规律和临时现象。

---

## 9. 和仓库已有论文的关系

| 相关笔记 | 相同点 | 差异点 |
|---|---|---|
| From Storage to Experience | 都关心 memory 从存储走向经验 | 综述是分类框架，MemoPilot 是具体 RL 方法 |
| EvolveR | 都用经验和 RL 提升 agent | EvolveR 更偏 search QA agent 和 experience base；MemoPilot 更偏训练 memory updater |
| Harness Updating Is Not Harness Benefit | 都关心外部 harness / memory 是否真正带来收益 | Harness Updating 更偏诊断，MemoPilot 直接优化 memory 的下游可用性 |
| Agentic Context Engineering | 都把上下文/记忆当作可维护资产 | ACE 用 Generator / Reflector / Curator 维护 playbook；MemoPilot 用 multi-turn GRPO 训练 memory policy |
| SE-Agent | 都不直接改变基础模型参数 | SE-Agent 优化测试时轨迹；MemoPilot 优化测试时 memory 更新 |

这篇文章在仓库中的位置可以放在：

```text
Self-Evolving LLM Agent
├── Agent Memory / Experience
│   ├── From Storage to Experience：记忆机制综述
│   ├── EvolveR：经验库 + search agent + RL
│   └── MemoPilot：训练 memory updater 支持 test-time learning
├── Harness Engineering
│   └── Harness Updating Is Not Harness Benefit：分析写更新和用更新的 gap
└── Context Engineering
    └── ACE：把 context playbook 作为可持续演化资产
```

---

## 10. 我的理解与总结

这篇论文最值得记住的观点是：

> Agent memory 的关键不只是“存什么”，而是“怎么把过去经验写成未来执行模型真的能用的指导”。

MemoPilot 的贡献在于把 memory update 从 prompt engineering 推向了 **reinforcement learning over memory**。它把 memory 生成视为一个会影响未来 reward 的动作，通过 multi-turn GRPO 学习如何写出可执行的、可维护的、可迁移的 memory。

我觉得这篇论文对 self-evolving agent 方向有三个重要启发：

1. **进化对象可以是 memory updater**：不一定要微调主模型，也不一定只更新 memory 内容；还可以训练“写 memory 的策略”。
2. **memory 要和 executor 对齐**：正确事实、完整历史、漂亮总结都不等于有用；有用 memory 必须能改变 frozen player 的行动。
3. **测试时学习需要过程级评估**：只看最后任务成功率不够，还要看 agent 是否能从前几轮经验中快速识别规律、维护假设、修正错误和迁移到新 executor。

如果用一句话概括这篇文章：

> MemoPilot 把“经验记忆”从手写反思模板变成了一个可以用多轮奖励训练的外部策略模块，让冻结 LLM agent 在连续任务中真正表现出 test-time learning。


---

## 11. 参考资料

- arXiv：<https://arxiv.org/abs/2606.08656>
- PDF：<https://arxiv.org/pdf/2606.08656>
- arXiv HTML：<https://arxiv.org/html/2606.08656v1>
- 相关综述笔记：[From Storage to Experience](from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md)
- 相关诊断笔记：[Harness Updating Is Not Harness Benefit](harness-updating-is-not-harness-benefit.md)
