<!--
metadata:
  title: 'Self-Evolving LLM Agent 实验设置横向对比'
  short_title: '实验设置横向对比'
  note_type: '横向综述 / 对比笔记'
  status: '持续维护'
  scope: '仓库内已阅读论文的实验对象、数据集、对比方法与评价指标'
  created: '2026-06-06'
  updated: '2026-06-06'
-->

# Self-Evolving LLM Agent 实验设置横向对比

这个文档用于整理仓库中已阅读论文的 **实验对象、训练数据、测试数据集、对比方法、评价指标和主要实验结论**。

它不是单篇论文读书笔记，而是跨论文的实验设计索引。目标是帮助后续快速回答这些问题：

- 这个方向常用哪些数据集 / benchmark？
- 哪些论文做的是 Search Agent，哪些做的是 Tool-use Agent、Harness / Memory Agent？
- 哪些方法真正训练模型，哪些只是更新 prompt / memory / skill / workflow？
- 常见 baseline 和评价指标是什么？
- 哪些实验设置更容易复现，哪些依赖闭源模型或复杂系统？

---

## 1. 总览表

| 论文 | 实验对象 / Agent 类型 | 核心任务 | 训练 / 更新方式 | 测试数据集 / 环境 | 主要指标 | 复现信息 |
|---|---|---|---|---|---|---|
| [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | Search Agent；Experience-based Agent；Self-Evolving Agent | 复杂问答、多跳问答、搜索增强推理 | Experience self-distillation；Experience Base maintenance；SFT / LoRA；GRPO policy evolution | 域内：Natural Questions、HotpotQA；域外：TriviaQA、PopQA、2WikiMultiHopQA、MuSiQue、Bamboogle | Exact Match；部分分析使用 F Score | 有代码、模型权重和系统组件说明 |
| [Harness Updating Is Not Harness Benefit](../notes/harness-updating-is-not-harness-benefit.md) | Harness-evolving Agent；Memory / Skill / Tool / Workflow Agent | 分析 Evolver 写更新与 Task-Solver 使用更新是否等价 | 不改模型参数；更新外部 harness；通过交叉实验解耦 Evolver 和 Task-Solver | SWE-bench Verified、MCP-Atlas、SkillsBench | 任务成功率 / benchmark 分数；Harness activation / adherence 等诊断指标 | 有代码仓库；具体实验依赖多模型组合 |
| [Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | Tool-use Agent 理论；Theory of Agent；工具调用校准 Agent | 判断何时内部推理、何时调用外部工具；分析 overthinking、overacting、over-delegation | 主要是理论建模；提出 internal task set、world task set、knowledge boundary、epistemic effort | 无新增 benchmark；position paper 侧重概念框架 | 无传统实验指标；建议关注 effort allocation、tool-use necessity、process-level calibration | 暂未找到官方代码；有 arXiv 和官方项目页 |
| [Self-Challenging Language Model Agents](../notes/self-challenging-language-model-agents.md) | Tool-use Agent；Self-Challenging Agent；Synthetic-task Agent | 多轮工具使用、环境探索、自动任务生成与验证 | Code-as-Task；one-step REINFORCE / Rejection Fine-Tuning；SFT distillation；DPO / PPO / GRPO 消融 | M3ToolEval：Calculation、Web Browsing；TauBench：Retail、Airline | Pass@1、Pass@4 | 暂未找到官方公开代码；实验设计较清晰 |

---

## 2. 按实验对象分类

### 2.1 Search / QA Agent

代表论文：**EvolveR**。

这一类工作关注 Agent 如何在复杂问答中调用外部搜索工具，并进一步利用历史经验改善搜索和推理策略。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | 复杂问答、多跳问答、开放域问答 |
| 外部工具 | 外部知识检索 / 搜索工具 |
| 内部机制 | Experience Base、经验原则检索、经验自蒸馏 |
| 训练方式 | cold-start SFT、LoRA、GRPO |
| 常见指标 | Exact Match、F Score |
| 关键问题 | Agent 学到的是数据集答案，还是可迁移的问题解决策略？ |

### 2.2 Harness / Memory / Skill Agent

代表论文：**Harness Updating Is Not Harness Benefit**。

这一类工作不一定训练模型参数，而是研究 prompt、memory、skill、tool、workflow 等外部 harness 如何更新，以及 Task-Solver 是否真的能使用这些更新。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | 代码修复、工具调用、技能复用、复杂任务执行 |
| 更新对象 | prompt、skill、memory、tool 使用方式、workflow |
| 核心变量 | Evolver 与 Task-Solver 分离 |
| 诊断重点 | Harness Updating 与 Harness Benefit 是否一致 |
| 常见失败 | Harness Activation Failure；Harness Adherence Failure |
| 关键问题 | 性能瓶颈是在“写更新”，还是在“会不会用更新”？ |

### 2.3 Tool-use / Synthetic-task Agent

代表论文：**Self-Challenging Language Model Agents**。

这一类工作关注 Agent 如何自己生成任务、自己构造验证器、自己采样轨迹，再把这些轨迹用于训练。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | 多轮工具调用、网页浏览、计算、零售 / 航空客服环境操作 |
| 任务来源 | Agent 自生成 synthetic tasks |
| 验证方式 | Code-as-Task 中的 verification function |
| 训练方式 | one-step REINFORCE、Rejection Fine-Tuning、SFT distillation、DPO / PPO / GRPO 消融 |
| 常见指标 | Pass@1、Pass@4 |
| 关键问题 | 没有人工任务集时，Agent 能否自动构造可验证训练任务？ |

### 2.4 Tool-use Calibration / Theory of Agent

代表论文：**Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary**。

这一类工作更偏理论和评价框架，关注 Agent 是否真的应该调用工具，而不只是工具调用后任务是否成功。

典型分析维度：

| 维度 | 内容 |
|---|---|
| 任务类型 | 任意需要内部推理和外部工具之间取舍的 Agent 任务 |
| 核心概念 | internal task set、world task set、knowledge boundary、epistemic effort |
| 关键行为 | overthinking、overacting、over-delegation、epistemically calibrated tool use |
| 训练启发 | agentic midtraining、capability-conditioned SFT、process-level RL reward |
| 常见指标 | 尚无统一 benchmark；建议记录 tool-use necessity、effort allocation、过程校准 |
| 关键问题 | Agent 是真的需要外部工具，还是在用外部工具替代内部能力？ |

---

## 3. 常见数据集与环境

| 数据集 / 环境 | 出现论文 | 类型 | 作用 |
|---|---|---|---|
| Natural Questions | EvolveR | 开放域问答 | 域内训练 / 经验库构建 / 评测 |
| HotpotQA | EvolveR | 多跳问答 | 域内训练 / 经验库构建 / 评测 |
| TriviaQA | EvolveR | 开放域问答 | 域外泛化评测 |
| PopQA | EvolveR | 长尾事实问答 | 域外泛化评测 |
| 2WikiMultiHopQA | EvolveR | 多跳问答 | 域外泛化评测 |
| MuSiQue | EvolveR | 多跳问答 | 域外泛化评测 |
| Bamboogle | EvolveR | 多跳 / 组合问答 | 域外泛化评测 |
| SWE-bench Verified | Harness Updating Is Not Harness Benefit | 代码修复 Agent benchmark | 测试真实代码仓库 issue 修复能力 |
| MCP-Atlas | Harness Updating Is Not Harness Benefit | MCP 工具调用 benchmark | 测试多工具调用和复杂任务执行 |
| SkillsBench | Harness Updating Is Not Harness Benefit | Skill 使用 benchmark | 测试 skill 加载、复用和执行能力 |
| M3ToolEval - Calculation | Self-Challenging Language Model Agents | 工具使用环境 | 测试计算类多轮工具调用 |
| M3ToolEval - Web Browsing | Self-Challenging Language Model Agents | 工具使用环境 | 测试网页浏览和信息提取 |
| TauBench - Retail | Self-Challenging Language Model Agents | 交互式工具环境 | 测试零售客服、订单、退换货等任务 |
| TauBench - Airline | Self-Challenging Language Model Agents | 交互式工具环境 | 测试航班查询、改签、订票等任务 |
| 暂无新增 benchmark | Theory of Agent | 理论 / position paper | 用于提出工具调用校准框架，而不是报告新实验 |

---

## 4. 常见对比方法 / baseline

| 类别 | 代表方法 | 出现论文 | 说明 |
|---|---|---|---|
| 直接推理 | Direct Inference | EvolveR | 不显式使用复杂检索或训练的基础设置 |
| 显式推理 | Chain-of-Thought | EvolveR | 用推理链增强回答 |
| 检索增强推理 | IRCoT、RAG、Search-o1 | EvolveR | 引入外部知识检索 |
| 工具调用校准 | Epistemically necessary tool use | Theory of Agent | 关注是否真的需要调用工具，而不只看调用后是否答对 |
| 监督学习 | SFT、LoRA | EvolveR、Self-Challenging Language Model Agents | 用示范轨迹或筛选轨迹微调模型 |
| 轨迹筛选 | Rejection Sampling / Rejection Fine-Tuning | EvolveR、Self-Challenging Language Model Agents | 只用成功轨迹或高质量轨迹训练 |
| RL Agent | R1-base、R1-instruct、Search-R1-base、Search-R1-instruct | EvolveR | 与搜索增强 RL Agent 对比 |
| Offline preference / RL | DPO | Self-Challenging Language Model Agents | 在固定轨迹上进行偏好优化消融 |
| Online RL | PPO、GRPO | EvolveR、Self-Challenging Language Model Agents | 在线采样和策略优化，收益可能更高但更不稳定 |
| 自动任务生成 | PAE | Self-Challenging Language Model Agents | 和 SCA 对比任务生成与验证机制 |
| 交叉诊断 | 固定 Task-Solver 替换 Evolver；固定 Evolver 替换 Task-Solver | Harness Updating Is Not Harness Benefit | 用于拆解“写更新”和“用更新”两个能力 |

---

## 5. 常见评价指标

| 指标 | 适用场景 | 说明 |
|---|---|---|
| Exact Match | 开放域 / 多跳问答 | 预测答案与标准答案标准化后完全一致 |
| F Score | 问答任务补充分析 | 允许部分匹配，更适合别名或长答案场景 |
| Pass@1 | 工具调用 / 交互式任务 | 单次采样是否成功 |
| Pass@4 | 工具调用 / 交互式任务 | 多次采样中是否至少一次成功 |
| Success Rate / Benchmark Score | Agent benchmark | 不同 benchmark 自带的成功率或评分 |
| Harness Activation | Harness 诊断 | 是否正确检索、加载、激活相关 harness |
| Harness Adherence | Harness 诊断 | 激活后是否持续遵循 skill / memory / workflow |
| Tool-use Necessity | 工具调用校准 | 外部工具调用是否在知识上必要，是否真的减少不确定性 |
| Effort Allocation | Theory of Agent / Agentic RL | 内部推理 effort 与外部工具 effort 是否和任务需求匹配 |

---

## 6. 目前观察到的实验设计趋势

### 6.1 从“最终分数”转向“过程诊断”

早期 Agent 实验容易只看最后任务成功率。现在更值得关注的是：

- 是否调用了正确工具；
- 是否检索了正确经验；
- 是否正确加载 skill / memory；
- 是否在长程任务中持续遵循 workflow；
- 失败到底发生在任务理解、工具调用、经验使用还是最终回答阶段。

### 6.2 从“人工数据”转向“自动生成训练任务”

Self-Challenging Language Model Agents 这类工作说明，Agent 训练的瓶颈不只是模型能力，也包括任务和奖励来源。

未来值得重点观察：

- synthetic task 的质量控制；
- verification function 是否可靠；
- failure cases 是否能减少 reward hacking；
- 自动生成任务能否迁移到真实 benchmark。

### 6.3 从“外部知识检索”转向“内部经验检索”

EvolveR 的重要启发是：

- 外部搜索解决事实知识问题；
- 内部经验检索解决问题解决策略问题。

后续读论文时，需要区分：论文里的 memory 到底是存事实、存轨迹、存经验原则，还是存可执行 skill。

### 6.4 从“反思器更强”转向“求解器是否会用”

Harness Updating Is Not Harness Benefit 的重要提醒是：

- Evolver 写出好更新，不等于 Task-Solver 能用好更新；
- 弱模型可能不会激活相关 harness；
- 强模型可能原本就接近上限，提升空间有限；
- 中等模型反而可能最能吃到 harness 更新红利。

### 6.5 从“会调用工具”转向“该不该调用工具”

Theory of Agent 的重要提醒是：

- 工具调用不是越多越好；
- 最终答对不代表工具调用过程合理；
- 需要区分 closed-book 内部能力和 open-book 工具增强能力；
- 自演化 Agent 不应让外部工具完全替代内部学习。

后续读 tool-use / RAG / search agent 论文时，可以增加一个检查项：论文是否分析了工具调用的必要性，而不只是报告有工具后的成功率。

---

## 7. 后续新增论文时建议补充的字段

后续每读一篇新论文，建议在单篇笔记之外，同步补充本文件中的这些字段：

| 字段 | 填写说明 |
|---|---|
| 论文 | 论文标题和本仓库笔记链接 |
| 实验对象 | Search Agent / Tool-use Agent / Web Agent / Coding Agent / Memory Agent / Harness Agent 等 |
| 核心任务 | 问答、代码修复、网页操作、工具调用、客服环境、数据库操作等 |
| 训练数据 | 人工数据、历史轨迹、synthetic tasks、成功轨迹、偏好数据等 |
| 测试数据集 / 环境 | benchmark 名称、子任务名称、域内 / 域外划分 |
| 基础模型 | Llama、Qwen、GPT、Claude 等，以及模型规模 |
| 训练方法 | SFT、RFT、DPO、PPO、GRPO、REINFORCE、无训练等 |
| 对比方法 | baseline、ablation、previous methods |
| 评价指标 | EM、F1、Pass@k、success rate、reward、人工评分等 |
| 主要结论 | 这篇实验最想证明什么 |
| 复现性 | 是否开源代码、数据、模型、环境配置 |

---

## 8. 维护原则

1. **先粗后细**：新增论文时先补总览表，再逐步补数据集和 baseline。
2. **能表格化就表格化**：横向比较优先用表格，避免写成第二篇长读书笔记。
3. **保留不确定项**：不确定的信息写“待补充”，不要强行猜。
4. **和单篇笔记互相链接**：详细解释放在 `notes/`，本文件只保留对比信息。
5. **关注实验设计，而不只是结果分数**：重点记录实验对象、数据来源、对比方法、指标和结论边界。
