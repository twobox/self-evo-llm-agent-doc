<!--
metadata:
  title: 'Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary'
  short_title: 'Theory of Agent'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'position paper / theory paper / tool-use decision-making paper'
  status: 'arXiv v4 last revised on 2026-05-08; official project page marks it as ICML 2026 Position Paper'
  venue: 'ICML 2026 / arXiv'
  arxiv_id: '2506.00886'
  arxiv_url: 'https://arxiv.org/abs/2506.00886'
  pdf_url: 'https://arxiv.org/pdf/2506.00886'
  html_url: 'https://arxiv.org/html/2506.00886v4'
  code_url: ''
  original_code_url: ''
  model_url: ''
  authors:
    - 'Hongru Wang'
    - 'Cheng Qian'
    - 'Manling Li'
    - 'Jiahao Qiu'
    - 'Boyang Xue'
    - 'Mengdi Wang'
    - 'Heng Ji'
    - 'Amos Storkey'
    - 'Kam-Fai Wong'
  institutions:
    - 'University of Edinburgh'
    - 'The Chinese University of Hong Kong'
    - 'University of Illinois Urbana-Champaign'
    - 'Northwestern University'
    - 'Princeton University'
  topics:
    - 'Theory of Agent'
    - 'Tool-use Agent'
    - 'Epistemic Necessity'
    - 'Knowledge Boundary'
    - 'Effort-Consistent Alignment'
    - 'Self-Evolving Agent'
  tags:
    - 'LLM Agent'
    - 'external tools'
    - 'overthinking'
    - 'overacting'
    - 'over-delegation'
    - 'meta-cognition'
    - 'agentic RL'
  related_notes:
    - 'self-challenging-language-model-agents.md'
    - 'evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'harness-updating-is-not-harness-benefit.md'
  created: '2026-06-06'
  updated: '2026-06-06'
-->

# 《Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary》读书笔记

## 1. 基本信息

- 论文标题：Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary
- 副标题 / 项目页标题：Introducing the Theory of Agent (ToA)
- arXiv：<https://arxiv.org/abs/2506.00886>
- PDF：<https://arxiv.org/pdf/2506.00886>
- arXiv HTML：<https://arxiv.org/html/2506.00886v4>
- 官方项目页：<https://hrwise-nlp.github.io/assets/websites/theory-of-agent/>
- 中文博客：官方项目页提供 Notion 中文博客入口；本文整理时未进一步核验完整博客内容。
- 代码仓库：暂未找到官方公开代码仓库。
- 模型权重：暂未找到官方公开模型权重。

一句话概括：这篇 position paper 不是提出一个新的工具调用算法，而是给 LLM Agent 的工具调用行为提出一个规范性判断标准：**只有当内部推理无法可靠消除任务所需的不确定性时，Agent 才应该调用外部工具。**

## 2. 投稿 / 发表状态

- arXiv 编号为 **2506.00886**。
- arXiv 摘要页显示：v1 提交于 2025-06-01，当前版本 v4 修订于 2026-05-08。
- 官方项目页标注为 **ICML 2026 · Position Paper**。
- arXiv HTML 页面主题处标注为 Machine Learning, ICML。
- 需要注意：这是一篇 **position / theory paper**，重点是提出理论框架和研究立场，不是典型的 benchmark + SOTA 实验论文。

## 3. 作者与机构

论文作者与机构如下：

| 作者 | 机构 |
|---|---|
| Hongru Wang | University of Edinburgh；The Chinese University of Hong Kong |
| Cheng Qian | University of Illinois Urbana-Champaign |
| Manling Li | Northwestern University |
| Jiahao Qiu | Princeton University |
| Boyang Xue | The Chinese University of Hong Kong |
| Mengdi Wang | Princeton University |
| Heng Ji | University of Illinois Urbana-Champaign |
| Amos Storkey | University of Edinburgh |
| Kam-Fai Wong | The Chinese University of Hong Kong |

从作者组合看，这篇论文横跨 **EdinburghNLP / EdinburghAI、CUHK、UIUC Blender Lab、Northwestern、Princeton** 等研究圈子。它不是单点工程论文，而是把 LLM Agent、工具学习、推理效率、自演化、世界模型、强化学习与认知层面的 metacognition 放在一起讨论。

## 4. 作者背景和研究圈子

### 4.1 Hongru Wang

Hongru Wang 当前页面显示为 University of Edinburgh 的 Research Associate，方向围绕 **Theory of Agent**，尤其关注 planning、memory、self-evolving agent。他此前在 CUHK 完成博士，并与 UIUC Blender Lab、Heng Ji、Kam-Fai Wong、Mengdi Wang 等研究者有密切合作。

从他个人主页列出的代表工作看，其研究线索很清楚：

- Agent 如何学习：ToolRL、Self-Evolving Agents、World Models；
- Agent 如何行为：overthinking、overacting、tool overuse、when to reason and when to act；
- Agent 如何评估：工具使用安全、个性化、reward modeling、process-level evaluation。

这篇 ToA 论文可以看作这些工作背后的理论总纲：把“什么时候推理、什么时候行动、什么时候调用外部工具”抽象成一个统一的 epistemic decision problem。

### 4.2 Cheng Qian

Cheng Qian 是 UIUC 的 PhD student，导师为 Heng Ji。他的主页描述其研究聚焦 **LLM agent、tool use、reasoning、alignment、creativity**，此前也在 CMU 合作过 LLM knowledge 与 tool use 相关方向。本论文中的 ToA 问题与他在 SMART、ToolRL 等工具使用 / 工具过度调用方向的研究高度相关。

### 4.3 Manling Li 与其他合作者

Manling Li 是 Northwestern University 计算机系助理教授，领导 Multimodal Learning with Language Lab，研究方向包括 multimodal reasoning、embodied agents、foundation agent training、world modeling、agent safety 等。她的加入使论文不仅停留在文本 Agent，还能自然延伸到 embodied agent、vision agent 和多模态交互系统。

Heng Ji、Kam-Fai Wong、Amos Storkey、Mengdi Wang 等作者分别代表 NLP、信息抽取 / 语言智能、机器学习、强化学习与理论建模等背景。这种作者组合也说明：ToA 试图解决的是 Agent 领域中更基础的概念问题，而不是单一任务上的工程调参。

## 5. 所属研究方向与论文定位

这篇论文属于：

- LLM Agent / Tool-use Agent；
- Agent theory / agent decision-making；
- Tool-use alignment；
- Agentic RL 与过程奖励；
- Self-evolving agent 的理论基础；
- Efficient reasoning / overthinking / overacting 研究。

它的定位可以概括为：**为工具增强 Agent 建立一个“该不该调用工具”的知识论边界。**

很多现有 Agent 框架关心的是：

- 怎么把工具接入模型；
- 怎么让模型学会调用工具；
- 工具调用后任务成功率能否提高；
- 搜索、浏览器、代码解释器、API、GUI 操作等工具能否提升最终答案。

而 ToA 问的是更前置的问题：

> 对当前 Agent 来说，这个工具调用在知识上是否必要？如果内部推理已经足以完成任务，调用工具虽然可能也能拿到正确答案，但它是否会造成低效、依赖外部系统，甚至抑制内部能力发展？

这使它与仓库中已有笔记形成互补：

- 和 **Self-Challenging Language Model Agents** 的关系：SCA 关注如何自动生成任务并训练工具使用能力；ToA 关注训练时应该如何判断工具调用是否真的必要。
- 和 **EvolveR** 的关系：EvolveR 关注搜索增强 Agent 如何通过经验库和训练自演化；ToA 提醒我们，外部搜索不应成为绕过内部推理的默认捷径。
- 和 **Harness Updating Is Not Harness Benefit** 的关系：Harness 论文关注外部组件是否真的被 Task-Solver 使用；ToA 进一步追问外部组件被使用时是否 epistemically necessary。

## 6. 核心问题

论文围绕一个核心问题展开：

> 当 LLM Agent 面对任务时，什么时候应该继续内部推理，什么时候应该调用外部工具？

作者认为，当前很多 Agent 框架存在一个隐含问题：只要最终任务成功，工具调用、搜索、长链推理、外部代理委托等过程往往都被视为合理。但这会掩盖三类问题：

1. **Overthinking**：明明需要外部信息，模型却继续在内部推理里空转，导致幻觉或无效长推理。
2. **Overacting / Tool Overuse**：明明可以内部解决，模型却频繁调用搜索、API、代码工具或其他外部系统。
3. **Over-delegation**：模型把本来可以通过自身能力解决的问题交给外部工具或更强模型，短期正确，但长期不利于内部能力巩固。

论文的立场是：外部工具不是不能用，而是应该在 **epistemically necessary** 的时候使用。这里的 epistemic necessity 可以理解为：**当前 Agent 基于自身参数、上下文、记忆和内部推理，已经无法可靠完成任务；必须通过外部交互获得新信息或改变环境状态。**

## 7. 理论框架：Theory of Agent (ToA)

### 7.1 把“推理”和“行动”都看作知识获取工具

ToA 的第一步是统一 internal reasoning 和 external acting。

传统 Agent 框架常把推理和行动分成两个阶段：先想，再做；或者 ReAct 式地交替 Thought 和 Action。ToA 换了一个视角：

- **内部认知工具**：reasoning、reflection、planning、self-consistency 等，它们只能重组、压缩、推断 Agent 已有的信息。
- **外部物理工具**：搜索引擎、API、浏览器、代码执行器、GUI 操作、环境交互等，它们可以引入 Agent 原本没有的新信息，甚至改变外部世界状态。

这样一来，“继续想”和“调用工具”不是两个完全不同的模块，而是两类知识获取手段。二者的核心差异在于信息来源：

- 内部推理查询的是模型自己的 internal world model；
- 外部工具查询的是外部环境或外部系统。

### 7.2 Internal Task Set 与 World Task Set

论文提出两个关键集合：

- **Internal Task Set**：当前 Agent 在给定环境中，能够只靠内部推理可靠完成的任务集合。
- **World Task Set**：给定合适外部交互后，在外部世界中原则上可完成的任务集合。

二者之间的分界就是 **Knowledge Boundary**。

这个概念非常重要。它说明“该不该调用工具”不是一个固定规则，而是跟模型能力、上下文、记忆、工具、环境都有关。同一个任务：

- 对小模型可能在 knowledge boundary 之外，需要搜索或调用工具；
- 对大模型可能在 knowledge boundary 之内，内部推理即可完成；
- 对同一个模型，在上下文变多、记忆被检索出来之后，也可能从“需要工具”变成“可以内部解决”。

### 7.3 工具使用是 belief-based classification

真实系统中，Agent 不可能直接看到自己的 knowledge boundary。因此，它只能估计：当前任务是否可以内部解决。

论文把这个问题表述为一种 belief-based classification：

- Agent 估计当前任务的 internal solvability；
- 再根据一个策略阈值决定是否调用外部工具；
- 不同 Agent 的阈值可能不同，风险偏好、成本偏好、安全要求也不同。

这对工程系统很有启发：工具调用策略不应该只写成“遇到关键词就搜索”或“所有事实问题都搜索”，而应该有一个 **self-assessment / solvability estimation** 机制。

### 7.4 Epistemic Effort：任务难度不会消失，只会被重新分配

论文的另一个核心概念是 **epistemic effort**。

可以把它理解成：完成一个任务所必须解决的信息负担。这个负担可以由内部推理承担，也可以由外部工具承担，但它不会因为调用工具而凭空消失。

论文中的直觉是：

```text
总的 epistemic effort = 内部推理承担的 effort + 外部交互承担的 effort
```

如果一个 Agent 比较强，它的内部任务集合更大，就可以把更多 effort 放在内部解决；如果 Agent 比较弱，它可能需要更多外部交互。

关键不在于“内部推理越多越好”或“外部工具越少越好”，而在于：

> effort 的分配是否与当前 Agent 的真实能力和任务需求一致。

### 7.5 Effort-Consistent Alignment

ToA 对 alignment 的定义不是“答案正确”这么简单，而是 **effort-consistent decision making**。

也就是说，一个 Agent 即便最终答对，如果它用大量不必要的外部工具才答对，仍然可能是不对齐的；反过来，如果它在需要外部证据的任务上硬靠内部推理，也是不对齐的。

这对评价 Agent 很关键：

- 只看 final answer 会把“闭卷真会”和“开卷照抄”混在一起；
- 只看 tool success rate 会鼓励工具滥用；
- 只惩罚工具调用次数又可能导致模型在需要工具时不敢调用。

更合理的评价应该同时看：任务是否成功、内部推理是否充分、外部调用是否必要、调用后是否真正减少不确定性。

## 8. 方法 / 实验设计

这篇论文没有提出一个新的 benchmark 或大规模实验表格。它的“方法”主要是理论建模和概念分析。

论文结构大致如下：

1. 用 POMDP / agent policy 的形式描述 Agent 与环境交互。
2. 按信息来源把 action / tool 分成 internal cognitive tools 与 external physical tools。
3. 定义 internal task set、world task set、knowledge boundary。
4. 把工具调用决策建模为基于 internal solvability estimate 的分类问题。
5. 引入 epistemic effort，说明任务的信息负担不能消失，只能在内部推理和外部交互之间重新分配。
6. 讨论 overthinking、overacting、over-delegation 等失败模式。
7. 推出训练和评价上的启发：agentic midtraining、agentic SFT、agentic RL、agentic prompting。

### 四种行为模式

论文把 Agent 的行为放在“内部推理 effort × 外部工具 effort”的二维平面上看，可以得到四种典型模式：

| 内部推理 | 外部工具 | 行为模式 | 问题 |
|---|---|---|---|
| 高 | 高 | Overacting / brute-force exploration | 既想很多，又频繁调用工具；可能正确但低效，决策逻辑不清晰 |
| 低 | 高 | Over-delegation | 把本可内部解决的问题外包出去；短期有效，长期抑制内部能力发展 |
| 高 | 低 | Overthinking / hallucination | 在需要外部信息时仍然内部硬想；容易产生幻觉或长推理空转 |
| 低但足够 | 低但必要 | Epistemically calibrated | 在足够内部推理和必要外部调用之间达到较好校准 |

这里的“低”不是偷懒，而是 **minimal but sufficient**：用足够少但足以完成任务的内部 / 外部 effort。

## 9. 主要结论

### 9.1 工具调用应该有知识论理由

论文最核心的结论是：外部工具调用不应该只是 workflow 默认步骤，也不应该只是 reward optimization 里的普通 action。它应该有一个明确理由：当前任务中剩余的不确定性无法通过内部推理可靠解决。

### 9.2 正确答案不足以评价 Agent

如果两个 Agent 都答对了，但一个靠内部推理解决，另一个把所有问题都丢给搜索或更强模型，它们的能力状态和长期发展路径是不同的。只看 accuracy / success rate 会隐藏这种差异。

### 9.3 过度委托会抑制内部能力发展

作者特别强调：不必要的外部委托不仅是效率问题，还可能让 Agent 失去练习和巩固内部能力的机会。对于自演化 Agent，这一点尤其关键：如果每个任务都外包给外部工具，模型可能完成任务，却没有真正把能力内化。

### 9.4 Tool-use alignment 应该关注 effort allocation

好的 Agent 不是“尽量少调用工具”，也不是“尽量多调用工具”，而是根据自己的 knowledge boundary 来分配 internal / external effort。

## 10. 对训练方法的启发

### 10.1 Agentic Midtraining：next-tool prediction

作者认为，传统 next-token prediction 主要把静态知识压缩进模型参数，但不直接教模型如何通过交互获取新知识。因此，可以考虑在中期训练中加入 **next-tool prediction**：让模型学习在给定上下文下什么时候应该调用什么工具。

这相当于把“知识获取方式”也纳入训练目标，而不仅是预测文本。

### 10.2 Agentic SFT：不能用同一套工具示范训练所有模型

标准 SFT 往往假设存在统一的“好工具调用轨迹”。ToA 认为这个假设有问题，因为不同模型的 internal task set 不同。

一个对小模型必要的搜索调用，对大模型可能是冗余；一个对大模型可内部解决的问题，对小模型可能必须调用工具。

因此，工具使用 SFT 数据最好是 **capability-conditioned** 的：根据目标模型能力定制示范，而不是把同一条轨迹喂给所有模型。

### 10.3 Agentic RL：奖励过程，而不只是结果

如果 RL reward 只看最终正确性，那么“直接调用强工具 / 强模型”可能成为捷径。论文因此主张，Agentic RL 应该奖励过程质量：

- 什么时候推理；
- 什么时候调用工具；
- 什么时候停止；
- 工具调用是否减少了真实不确定性；
- 是否存在不必要的 tool call。

这与 ToolRL、OTC-PO、Search-R1 等方向相关：reward 设计不能只看 outcome，还要看 tool-use trajectory。

### 10.4 Agentic Prompting：有用，但不够

Prompt 可以要求模型“先判断是否需要工具”，也可以加入 ReAct / reflection / memory scaffold。但论文倾向于认为，prompt 更适合作为快速原型和行为诊断，不足以长期保证 tool-use decision 的校准。真正稳定的校准仍需要 SFT、RL 或更系统的训练机制。

## 11. 工程启发

### 11.1 工具调用前加一个“必要性判断”步骤

实际做 Agent 系统时，可以在每次 tool call 前加一个轻量判断：

```text
当前任务剩余的不确定性是什么？
这些不确定性是否能通过已有上下文和内部推理解决？
如果不能，外部工具具体要补充什么信息？
工具输出回来后，是否真的减少了不确定性？
```

这不是为了让模型写更长思考，而是为了让工具调用有可审计的理由。

### 11.2 记录 tool-use trace，不只记录最终答案

如果要评估 Agent 是否进步，应该记录：

- 每次调用了什么工具；
- 调用前的 internal solvability estimate；
- 调用理由；
- 工具结果是否被使用；
- 没有调用工具时是否出现幻觉；
- 是否存在“能内部解决却外部搜索”的过度委托。

这些日志对分析 Agent failure 比单一成功率更有价值。

### 11.3 RAG / 搜索系统不要默认全开

很多 RAG 系统默认“问题来了就检索”。ToA 的视角提醒我们：

- 对需要新事实、实时信息、私有知识的问题，检索是必要的；
- 对模型已掌握且上下文充分的问题，检索可能只是增加噪音和延迟；
- 对需要推理的问题，盲目检索可能让模型复制片段而不是完成推理。

因此，RAG router 应该根据 freshness、confidence、domain、risk 等信号决定是否检索。

### 11.4 自演化 Agent 要避免“外部工具替代学习”

在 self-evolving agent 中，外部工具可以帮助完成任务，但如果所有成功都依赖外部工具，经验库和模型参数可能没有真正学到东西。

一个更好的设计是：

1. 允许工具帮助解决当前任务；
2. 任务结束后分析哪些步骤本来可以内部化；
3. 把可内部化的知识、策略、workflow 写入 memory / skill / SFT data；
4. 后续同类任务减少不必要调用。

这也解释了为什么 ToA 与 self-evolving agent 方向关系很大：自演化不只是“调用更多工具解决更多任务”，而是让 knowledge boundary 逐步外扩。

### 11.5 评价指标需要区分 closed-book 与 open-book 能力

可以设计成对照实验：

- 禁止外部工具时，Agent 能解决多少？
- 允许外部工具时，Agent 解决多少？
- 允许外部工具后，是否出现不必要调用？
- 训练一段时间后，原本需要工具的问题是否被内部化？

这比单纯比较有无工具的成功率更能体现 Agent 是否真的变聪明。

## 12. 局限性

### 12.1 理论框架多，实证验证少

这篇论文是 position paper，主要贡献是提出概念和理论视角。它没有像普通方法论文那样给出大规模实验、消融表格或公开 benchmark。因此，它的价值更多在于提供分析框架，而不是直接可复现的算法。

### 12.2 Knowledge boundary 很难直接观测

论文提出 internal task set 和 knowledge boundary，但真实系统中很难准确知道模型能否内部解决某任务。即使模型自评有信心，也可能高估或低估自己。因此，如何可靠估计 internal solvability 是后续关键问题。

### 12.3 “必要”不只由知识决定，还由成本和风险决定

在实际部署中，是否调用工具还受很多因素影响：

- 内部推理 token 成本；
- 外部 API 费用和延迟；
- 工具是否可信；
- 任务是否安全关键；
- 是否需要最新信息；
- 外部交互是否会改变真实世界状态。

所以 epistemic necessity 不能被机械理解为“能不用工具就绝对不用工具”。更合理的理解是：在知识、成本、风险、时效性之间做校准。

### 12.4 对多智能体和 embodied agent 的复杂性还只是展开方向

论文项目页提到 Vision Agent、Embodied Agent、Multi-Agent Coordination 等未来方向。对于 embodied agent，外部行动可能改变世界；对于多智能体，调用另一个 Agent 本身也是一种外部委托。这些场景下 knowledge boundary 和 effort allocation 会更复杂。

## 13. 我的理解与总结

我觉得这篇论文最值得学习的地方，不是它形式化了多少符号，而是它把一个工程上经常被忽略的问题说清楚了：**工具调用不是越多越智能，正确答案也不能证明调用过程合理。**

很多 Agent 系统容易形成一种路径依赖：

```text
问题来了 → 搜索一下 / 调 API / 问强模型 → 得到答案 → 任务成功
```

这条路径短期很有效，但长期会带来两个问题：

1. 系统越来越依赖外部工具，成本、延迟、稳定性都受影响；
2. Agent 自己的内部能力没有被训练和巩固，所谓 self-evolution 可能只是外部 scaffold 越堆越多。

ToA 给出的提醒是：Agent 的智能不只体现在“能不能解决任务”，还体现在它是否知道 **什么时候靠自己，什么时候查外部世界**。

用一个更直观的比喻：这篇论文不是反对开卷考试，而是反对把所有考试都默认开卷。真正好的学生应该知道：哪些题自己会，哪些题必须查资料，查资料之后又如何把知识内化。

对我后续读 Agent 论文时，这篇论文可以作为一个检查清单：

- 这篇论文有没有区分内部能力和外部工具能力？
- 它的 reward 是否只奖励最终正确？
- 它是否惩罚或分析不必要工具调用？
- 它是否记录工具调用过程？
- 它是否证明 Agent 真的把能力内部化，而不是只是更会调用外部工具？

如果把这套问题带到 self-evolving agent、tool-use RL、RAG agent、GUI agent 论文里，很多实验设计的优点和缺口会更容易看出来。

## 14. 参考来源

- arXiv 摘要页：<https://arxiv.org/abs/2506.00886>
- arXiv HTML：<https://arxiv.org/html/2506.00886v4>
- 官方项目页：<https://hrwise-nlp.github.io/assets/websites/theory-of-agent/>
- Hongru Wang 个人主页：<https://hrwise-nlp.github.io/>
- Cheng Qian 个人主页：<https://qiancheng0.github.io/>
- Manling Li 个人主页：<https://limanling.github.io/>
