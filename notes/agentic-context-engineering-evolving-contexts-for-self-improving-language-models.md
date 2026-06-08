<!--
metadata:
  title: 'Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models'
  short_title: 'ACE'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'method / system paper'
  status: 'Published as ICLR 2026 conference paper / poster; arXiv v3, last revised on 2026-03-29; OpenReview last modified on 2026-04-11'
  venue: 'ICLR 2026 / arXiv / OpenReview'
  arxiv_id: '2510.04618'
  arxiv_url: 'https://arxiv.org/abs/2510.04618'
  pdf_url: 'https://arxiv.org/pdf/2510.04618'
  html_url: 'https://ar5iv.labs.arxiv.org/html/2510.04618v3'
  code_url: 'https://github.com/ace-agent/ace'
  original_code_url: ''
  model_url: ''
  authors:
    - 'Qizheng Zhang'
    - 'Changran Hu'
    - 'Shubhangi Upasani'
    - 'Boyuan Ma'
    - 'Fenglu Hong'
    - 'Vamsidhar Kamanuru'
    - 'Jay Rainton'
    - 'Chen Wu'
    - 'Mengmeng Ji'
    - 'Hanchen Li'
    - 'Urmish Thakker'
    - 'James Zou'
    - 'Kunle Olukotun'
  institutions:
    - 'Stanford University'
    - 'SambaNova Systems, Inc.'
    - 'UC Berkeley'
  topics:
    - 'Agentic Context Engineering'
    - 'Context Adaptation'
    - 'Self-Improving LLMs'
    - 'Agent Memory'
    - 'Playbook'
    - 'Test-Time Scaling'
    - 'Continual Learning'
    - 'AppWorld'
  tags:
    - 'context-engineering'
    - 'agent-memory'
    - 'self-improving-llm'
    - 'playbook'
    - 'test-time-adaptation'
    - 'appworld'
    - 'finance'
    - 'iclr-2026'
  related_notes:
    - 'notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'notes/harness-updating-is-not-harness-benefit.md'
  created: '2026-06-08'
  updated: '2026-06-08'
-->

# 《Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models》读书笔记

> 论文：**Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models**  
> arXiv：<https://arxiv.org/abs/2510.04618>  
> PDF 下载地址：<https://arxiv.org/pdf/2510.04618>  
> arXiv HTML：<https://ar5iv.labs.arxiv.org/html/2510.04618v3>  
> OpenReview：<https://openreview.net/forum?id=eC4ygDs02R>  
> 官方项目页：<https://ace-agent.github.io/>  
> 官方代码仓库：<https://github.com/ace-agent/ace>  
> 模型权重：暂未找到 ACE 单独发布的模型权重；论文实验主要使用 **DeepSeek-V3.1-671B** 作为基础模型。  
> 当前状态：ICLR 2026 conference paper / poster；arXiv v3 最后修订于 2026-03-29；OpenReview 页面最后修改于 2026-04-11。

---

## 1. 一句话总结

这篇论文提出 **ACE（Agentic Context Engineering）**：不更新模型参数，而是让 LLM 应用把 prompt、memory、工具使用经验、领域策略等上下文维护成一个会持续增长和整理的 **playbook**。它用 **Generator / Reflector / Curator** 三个角色，把任务执行轨迹和反馈转成结构化的上下文增量，从而让 Agent 或领域应用在后续任务中表现更好。

我的理解：ACE 不是“训练一个更强模型”，而是“训练 / 维护一个更好的上下文系统”。它把 self-improving LLM 的重点从参数更新转移到 **上下文资产的持续积累、纠错和组织**。

---

## 2. 论文外部信息

### 2.1 投稿与发表状态

- 会议状态：**ICLR 2026 conference paper / poster**。
- arXiv 编号：**arXiv:2510.04618**。
- arXiv 初始提交：2025-10-06；v3 最后修订：2026-03-29。
- OpenReview 页面显示：Published 2026-01-26，Last Modified 2026-04-11。
- 论文许可证：OpenReview 页面显示 **CC BY 4.0**。
- 代码许可证：官方 GitHub 仓库中 `LICENSE.txt` 为 **Apache License 2.0**。项目页底部和仓库许可证描述存在轻微不一致，实际复现和引用时建议以仓库 `LICENSE.txt` 为准。

### 2.2 作者与机构

论文作者来自三个主要机构：

- **Stanford University**：Qizheng Zhang、James Zou、Kunle Olukotun。
- **SambaNova Systems, Inc.**：Changran Hu、Shubhangi Upasani、Boyuan Ma、Fenglu Hong、Vamsidhar Kamanuru、Jay Rainton、Chen Wu、Mengmeng Ji、Urmish Thakker。
- **UC Berkeley**：Hanchen Li。

从作者圈子看，这篇论文明显处在 **Stanford + SambaNova** 的交叉区域：一边是 Stanford 的 AI / Systems / Agent 研究生态，另一边是 SambaNova 的模型服务、推理系统和企业 AI 应用背景。因此它不是单纯的 prompt 技巧论文，而是很强调 **可部署性、延迟、rollout 成本、长上下文服务成本** 的系统型工作。

### 2.3 作者背景和研究圈子

- **James Zou** 是 Stanford 机器学习、AI for Science / AI for Health、可信 AI 等方向的重要研究者。论文中 ACE 也继承了其团队在 **Dynamic Cheatsheet / adaptive memory / test-time learning** 这一类方向上的研究脉络。
- **Kunle Olukotun** 是 Stanford 计算机体系结构和并行计算方向的重要学者，也是 SambaNova Systems 的联合创始人之一。因此这篇论文对 **长上下文推理的成本、KV cache reuse、低延迟适配** 有比较强的系统视角。
- **SambaNova Systems** 这边的作者占比很高，说明 ACE 很可能是面向真实 LLM 应用部署的一套上下文工程框架，而不是只追求 benchmark 分数的算法原型。

暂未逐一找到所有作者的公开主页和详细背景；本笔记只基于论文、OpenReview、官方项目页和官方 GitHub 仓库整理，不对未确认信息做扩展猜测。

---

## 3. 所属研究方向与论文定位

这篇论文属于以下几个交叉方向：

1. **Context Engineering / Context Adaptation**：通过修改输入上下文、系统提示词、示例、记忆和策略，而不是更新模型参数来提高 LLM 应用性能。
2. **Self-Improving LLM / Self-Evolving Agent**：系统能从历史任务、执行轨迹和反馈中提取经验，并在后续任务中利用这些经验。
3. **Agent Memory / Test-Time Learning**：把运行时反馈转成可复用 memory，服务后续推理。
4. **Long-Context Agent System**：接受“上下文可以很长”这一趋势，但通过结构化、去重、缓存等方式让长上下文仍然可用。

它和仓库里其他几篇笔记的关系可以这样理解：

- 相比 **EvolveR**：EvolveR 更强调经验库 + 参数训练 / RL 共同驱动 Search Agent 演化；ACE 基本不训练模型参数，更强调上下文本身的持续工程化维护。
- 相比 **Harness Updating Is Not Harness Benefit**：那篇文章提醒“写出 harness 更新”和“Task-Solver 会用更新”不是一回事；ACE 则给出一种更具体的 harness / context 更新机制：把经验组织成 playbook，并让 Generator 在后续任务中调用。
- 相比 **Dynamic Cheatsheet**：ACE 继承 adaptive memory 的思路，但重点解决 **context collapse** 和 **brevity bias**：不要让上下文被反复重写成越来越短的摘要，而是用结构化增量来保留细节。

---

## 4. 核心问题

论文要解决的问题是：**如果不更新模型参数，只更新上下文，LLM Agent 能不能持续自我改进？如果可以，怎样避免上下文越改越短、越改越丢信息？**

作者指出已有 context adaptation 方法有两个典型问题。

### 4.1 Brevity Bias：过度追求短提示词

很多 prompt optimizer 会把复杂经验压缩成更短、更抽象的指令。短提示词看起来更优雅，但在真实 Agent 任务里，很多有价值的信息恰恰是很具体的，例如：

- 某个 API 的边界条件；
- 某类工具调用的常见错误；
- 某个领域任务的特殊格式；
- 某类环境反馈背后的隐含规则。

如果过度总结，这些细节会被删掉，导致上下文看似简洁，实际不可用。

### 4.2 Context Collapse：反复重写导致上下文坍缩

论文用 AppWorld 上的案例说明，单纯让 LLM 反复“重写整个上下文”，可能会突然把原来很长的上下文压缩成极短摘要。论文中一个例子是：上下文在某一步有 **18,282 tokens**，准确率 **66.7**；下一步坍缩成 **122 tokens** 后，准确率降到 **57.1**，甚至低于无上下文 baseline 的 **63.7**。

这说明：上下文不是越“总结”越好。对 Agent 来说，很多细节应该被保留下来，而不是被摘要器主动删除。

---

## 5. 方法：ACE 怎么做？

ACE 的核心设计是把上下文看成一个 **evolving playbook**，也就是“持续积累的操作手册”。它不是每次把整份上下文重写一遍，而是把经验拆成结构化条目，然后增量更新。

### 5.1 三角色架构：Generator / Reflector / Curator

ACE 把上下文更新拆成三个角色：

| 角色 | 作用 | 可以怎么理解 |
|---|---|---|
| Generator | 读取当前 context playbook，针对新 query 生成推理轨迹、工具调用或答案 | 真正执行任务的 Agent |
| Reflector | 根据成功 / 失败轨迹、执行反馈、ground-truth 或环境信号，总结哪些策略有用、哪些错误要避免 | 复盘者 / 反思者 |
| Curator | 把 Reflector 的经验整理成结构化 delta context items，并合并到 playbook | 知识管理员 / 经验库维护者 |

论文特别强调：三者使用同一个基础模型，避免“Reflector 或 Curator 用更强模型给 Generator 偷渡知识”。这能更干净地说明性能提升来自上下文构造，而不是来自更强外部模型。

### 5.2 关键图：ACE 框架

![ACE Framework](https://raw.githubusercontent.com/ace-agent/ace/main/assets/images/ace_framework.png)

图源：ACE 官方 GitHub 仓库 `assets/images/ace_framework.png`。这张图比实验柱状图更适合放在笔记里，因为它直接解释了 ACE 的主流程：Query 和 Context Playbook 输入 Generator，产生 Trajectory；Reflector 从轨迹中提取 Insights；Curator 生成 Delta Context Items，再回写到 Playbook。

### 5.3 Incremental Delta Updates：只改局部，不重写全局

ACE 把 context 表示为一组结构化 bullet，而不是一大段 monolithic prompt。每条 bullet 类似一个经验条目，通常包含：

- 唯一 ID；
- helpful / harmful 计数；
- 内容文本，例如策略、领域概念、公式、常见错误、工具调用注意事项。

当新任务完成后，系统不是让 LLM 重新生成完整上下文，而是生成一小组 **delta context items**。这些增量会被合并进已有 playbook。这样做的好处是：

- 不容易把历史经验整段删掉；
- 更新粒度更细；
- 可以并行合并多个 delta；
- 维护和调试更可解释。

### 5.4 Grow-and-Refine：允许增长，但要去重和修剪

ACE 不是简单地无限追加 memory。它允许 playbook 逐渐变长，但也会做去重、合并和修剪：

- 新知识作为新 bullet 加入；
- 已有 bullet 可以更新计数或内容；
- 语义重复的 bullet 通过 embedding 相似度去重；
- 只有在上下文窗口接近限制时，也可以采用 lazy refinement。

这点很重要：ACE 并不是“长上下文万能论”，而是“先保留细节，再通过结构化机制控制冗余”。

### 5.5 Offline 与 Online 两种适配模式

论文同时研究两类使用方式：

| 模式 | 输入反馈 | 典型用途 | 本质 |
|---|---|---|---|
| Offline adaptation | 训练集 / 验证集 / 可用标签 | 优化 system prompt 或任务 playbook | 部署前调好上下文 |
| Online adaptation | 测试时顺序样本、执行反馈、环境信号 | Agent memory / test-time learning | 边做任务边更新上下文 |

这也是论文工程价值比较大的地方：ACE 不只适用于有标注数据的 prompt 优化，也尝试利用自然执行反馈做无标签适配。

---

## 6. 实验设计

### 6.1 实验对象

论文评测两个大类任务：

| 类别 | 数据集 / 环境 | 任务特点 |
|---|---|---|
| LLM Agent | **AppWorld** | 需要 API 理解、代码生成、工具调用和环境交互；分 test-normal 与 test-challenge |
| 金融领域任务 | **FiNER** | XBRL 金融文档 token-level entity labeling，共 139 类细粒度实体 |
| 金融领域任务 | **Formula** | 从结构化 XBRL filings 中抽取数值并执行计算，属于金融数值推理 |

### 6.2 基础模型与设置

- 主要基础模型：**DeepSeek-V3.1-671B**。
- AppWorld 基于官方 **ReAct** 实现。
- ACE 中 Generator、Reflector、Curator 使用同一个模型，避免不同角色间的模型能力不公平。
- offline adaptation 最大 Reflector refinement rounds 和最大 epoch 设置为 5。
- online adaptation 在测试集顺序样本上边预测边更新。

### 6.3 对比方法 / baseline

论文主要比较：

- **Base LLM / ReAct**：无上下文适配的基础设置。
- **ICL**：把示例放进上下文。
- **MIPROv2**：DSPy 中的 prompt optimizer。
- **GEPA**：基于 reflective prompt evolution 的强 prompt optimizer。
- **Dynamic Cheatsheet (DC-CU)**：测试时维护 adaptive memory 的方法。
- **ACE**：本文方法，分有无 ground-truth labels、offline / online 两种模式。

### 6.4 评价指标

| 任务 | 指标 |
|---|---|
| AppWorld | Task Goal Completion（TGC）、Scenario Goal Completion（SGC）、Average |
| FiNER / Formula | Accuracy，即预测答案与 ground truth 精确匹配比例 |
| 成本分析 | adaptation latency、rollouts 数量、token dollar cost |

---

## 7. 主要实验结果

### 7.1 AppWorld：ACE 在 Agent 任务上显著优于 ICL / GEPA / DC

论文表 1 中，DeepSeek-V3.1-671B 作为基础模型时，AppWorld 平均分大致如下：

| 方法 | 模式 | 是否用 GT labels | Average |
|---|---|---:|---:|
| ReAct | Base | - | 42.4 |
| ReAct + ICL | Offline | 是 | 46.0 |
| ReAct + GEPA | Offline | 是 | 46.4 |
| ReAct + ACE | Offline | 是 | 59.4 |
| ReAct + ACE | Offline | 否 | 57.2 |
| ReAct + DC (CU) | Online | 否 | 51.9 |
| ReAct + ACE | Online | 否 | 59.5 |

最值得注意的不是单个最高分，而是：

- ACE offline 有标签时达到 **59.4**，明显高于 ICL / GEPA；
- ACE offline 无标签时仍有 **57.2**，说明自然执行反馈也能提供可用学习信号；
- ACE online 无标签时达到 **59.5**，高于 Dynamic Cheatsheet 的 **51.9**；
- 论文报告 ACE 在 AppWorld 上平均优于 selected baselines **10.6%**。

论文还提到，在当时 AppWorld leaderboard 上，ReAct + ACE 平均分 **59.4%** 接近 top-ranked IBM CUGA 的 **60.3%**，并在更难的 test-challenge split 上超过它。不过这只是 leaderboard 参考，论文脚注也说明 IBM CUGA 不是严格同设置 methodological baseline。

### 7.2 金融任务：ACE 对专业领域 playbook 很有效

论文表 2 中，金融任务结果如下：

| 方法 | 模式 | 是否用 GT labels | FiNER Acc | Formula Acc | Average |
|---|---|---:|---:|---:|---:|
| Base LLM | Base | - | 70.7 | 67.5 | 69.1 |
| ICL | Offline | 是 | 72.3 | 67.0 | 69.6 |
| MIPROv2 | Offline | 是 | 72.4 | 69.5 | 70.9 |
| GEPA | Offline | 是 | 73.5 | 71.5 | 72.5 |
| ACE | Offline | 是 | 78.3 | 85.5 | 81.9 |
| ACE | Offline | 否 | 71.1 | 83.0 | 77.1 |
| DC (CU) | Online | 是 | 74.2 | 69.5 | 71.8 |
| ACE | Online | 是 | 76.7 | 76.5 | 76.6 |
| ACE | Online | 否 | 67.3 | 78.5 | 72.9 |

这说明 ACE 对金融这种“规则、格式、术语、计算细节很多”的任务很适合。它不是只给模型几个示例，而是把领域规则、公式、错误模式持续写进 playbook。

但这里也暴露一个限制：当没有可靠标签或执行反馈时，online 适配可能退化。例如 ACE online 无 GT 时 FiNER 从 70.7 降到 67.3。也就是说，**上下文自我改进的质量高度依赖反馈信号质量**。

### 7.3 成本和速度：ACE 比全量 prompt 搜索 / 全量记忆重写更便宜

论文表 4 报告：

| 场景 | 对比 | latency 降低 | 其他成本降低 |
|---|---|---:|---:|
| AppWorld offline | ACE vs GEPA | -82.3% | rollouts -75.1% |
| FiNER online | ACE vs DC | -91.5% | token cost -83.6% |

原因是 ACE 不需要像 GEPA 那样做大量 prompt validation / evolutionary search，也不需要像一些 adaptive memory 方法那样频繁重写整份上下文。它主要更新小的 delta，并用非 LLM 逻辑做合并、去重和剪枝。

论文还讨论了长上下文的 serving cost：ACE 生成的 playbook 更长，但如果系统支持 KV cache / prompt cache，重复上下文可以复用。论文报告在 GPT-5.1 API 的 prompt-caching study 中，ACE evaluation stage 有 **91.8%** input tokens 来自 cache，从而使 billed input-token cost 相比原始 token 计数降低 **82.6%**。

---

## 8. 主要结论

1. **Context 可以作为自我改进对象**：不训练模型参数，也可以通过改进系统提示、记忆和经验 playbook 提升 Agent 表现。
2. **长而结构化的上下文比短摘要更适合复杂 Agent**：在 AppWorld 和金融任务里，详细策略、失败案例和领域规则比“简洁提示词”更有价值。
3. **避免 context collapse 的关键是增量更新**：不要每次让 LLM 重写全文，而是让 Curator 维护结构化 delta。
4. **自然执行反馈是可用信号**：在 AppWorld 这类有环境执行结果的任务中，即使没有 GT labels，ACE 也能明显提升。
5. **反馈质量决定上限**：如果任务没有可靠标签、执行结果或可验证反馈，ACE 也可能把错误经验写进 playbook，导致性能下降。
6. **工程上比很多 prompt optimizer 更轻**：ACE 报告了明显更低的 adaptation latency、rollouts 和 token cost。

---

## 9. 工程启发

### 9.1 把 prompt 当成“可维护资产”，而不是一次性文本

ACE 给我的最大启发是：prompt / memory / system instruction 不应该只是一个字符串，而应该像代码库一样维护：

- 有条目 ID；
- 有来源和反馈；
- 有 helpful / harmful 统计；
- 有合并、去重、回滚、剪枝机制；
- 有离线优化和在线更新两种工作流。

这对真实 Agent 系统很重要。否则 prompt 越迭代越容易变成“人工玄学”。

### 9.2 Context Engineering 可以和 Experience Base 打通

EvolveR 维护的是格式化经验库；ACE 维护的是 context playbook。两者本质上都在回答：**历史任务中学到的东西，应该以什么形式保存，并在后续任务中怎么用？**

区别在于：

- EvolveR 更像“经验检索 + 模型再训练 / 策略演化”；
- ACE 更像“经验条目直接进入上下文，成为可解释 playbook”。

工程上二者可以结合：先用 ACE 维护 playbook，再对高价值 playbook 条目做检索、蒸馏或训练。

### 9.3 反思和整理要分开

很多 Agent 反思方法把“评价轨迹、总结经验、改写记忆”交给同一个 LLM 一次完成。ACE 把它拆成 Reflector 和 Curator，这个设计很实用：

- Reflector 负责判断哪里对、哪里错、提炼 lesson；
- Curator 负责把 lesson 写成可维护的上下文条目；
- 非 LLM 合并逻辑负责去重和计数。

这更接近真实工程中的日志分析、知识库更新和配置管理。

### 9.4 长上下文不等于无脑塞信息

ACE 支持长上下文，但不是把所有历史轨迹原样塞进去。它强调：

- 保留有价值细节；
- 结构化组织；
- 用 embedding 去重；
- 依靠 KV cache / prompt cache 降低服务成本；
- 当上下文窗口接近上限时再 refine。

所以它不是“RAG 失败就上长上下文”，而是“长上下文也需要工程化治理”。

---

## 10. 局限性

1. **依赖反馈信号质量**：没有可靠 ground-truth、执行结果或 verifier 时，ACE 可能把错误经验写进 playbook，金融任务的无 GT online 结果已经体现了这个问题。
2. **评测范围仍有限**：主实验集中在 AppWorld 与金融 XBRL 任务，尚不足以说明所有 Agent 任务都适合这种 playbook 机制。
3. **长上下文成本依赖服务基础设施**：论文讨论了 KV cache / prompt cache，但真实成本取决于模型服务商、缓存命中率、上下文更新频率和并发模式。
4. **playbook 污染和安全问题还需要更多研究**：如果恶意输入或错误反馈进入 playbook，系统可能持续继承坏策略。论文主要从性能角度分析，还没有系统展开安全治理。
5. **AppWorld leaderboard 对比不是严格同设置实验**：IBM CUGA 是生产级 GPT-4.1 agent，ACE 使用 DeepSeek-V3.1。这个对比能体现实际竞争力，但不应被理解成严格控制变量的 baseline 对比。
6. **代码虽然开源，但迁移到新任务仍需适配 DataProcessor、反馈函数和 prompt 模板**：官方 README 也说明扩展新任务需要准备数据、实现 `process_task_data()`、`answer_is_correct()` 和 `evaluate_accuracy()` 等接口。

---

## 11. 我的理解与总结

这篇论文的价值在于，它把“上下文”从静态 prompt 提升为一种可以持续演化的系统组件。

传统 prompt engineering 更像一次性写说明书；ACE 更像维护一份持续更新的团队 runbook：每次任务之后，把成功经验、失败教训、领域规则和工具使用细节写进去，并且保证这份 runbook 不会被反复总结到失真。

在 self-evolving agent 方向里，这篇论文提供了一个很清晰的分支：

- 不一定要训练模型参数；
- 不一定要做复杂 RL；
- 可以先把外部 harness / memory / prompt 做成可积累、可审计、可剪枝的 playbook；
- 只要反馈可靠，Agent 就能通过上下文迭代获得持续提升。

我觉得 ACE 最值得学习的不是某个具体分数，而是它的工程化思路：**经验不是简单追加，也不是反复摘要，而是结构化增量维护。** 这对后续做 Agent Memory、工具调用规范、企业知识库 Agent、代码 Agent 的长期运行都很有启发。

---

## 12. 参考链接

- arXiv：<https://arxiv.org/abs/2510.04618>
- PDF：<https://arxiv.org/pdf/2510.04618>
- arXiv HTML：<https://ar5iv.labs.arxiv.org/html/2510.04618v3>
- OpenReview：<https://openreview.net/forum?id=eC4ygDs02R>
- 官方项目页：<https://ace-agent.github.io/>
- 官方 GitHub：<https://github.com/ace-agent/ace>
- 官方框架图：<https://raw.githubusercontent.com/ace-agent/ace/main/assets/images/ace_framework.png>
