<!--
metadata:
  title: 'Self-Evolving LLM Agent 实验设置横向对比'
  short_title: '实验设置横向对比'
  note_type: '横向综述 / 对比笔记'
  status: '持续维护'
  scope: '仓库内已阅读论文的实验对象、数据集、对比方法与评价指标'
  created: '2026-06-06'
  updated: '2026-06-10'
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
| [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | Context-adaptive Agent；Playbook-based Agent；Agent Memory / Context Engineering system | AppWorld 工具调用与 API 任务；金融 XBRL 信息抽取和公式计算；上下文自我改进 | 不更新模型参数；Generator / Reflector / Curator 三角色；从轨迹与反馈中生成 delta context items；offline / online context adaptation | AppWorld test-normal / test-challenge；FiNER；Formula / XBRL filings | AppWorld TGC / SGC / Average；FiNER / Formula Accuracy；adaptation latency、rollouts、token cost | 官方代码已开源；官方项目页和框架图可用；暂未找到单独模型权重 |
| [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | Search Agent；Experience-based Agent；Self-Evolving Agent | 复杂问答、多跳问答、搜索增强推理 | Experience self-distillation；Experience Base maintenance；SFT / LoRA；GRPO policy evolution | 域内：Natural Questions、HotpotQA；域外：TriviaQA、PopQA、2WikiMultiHopQA、MuSiQue、Bamboogle | Exact Match；部分分析使用 F Score | 有代码、模型权重和系统组件说明 |
| [Harness Updating Is Not Harness Benefit](../notes/harness-updating-is-not-harness-benefit.md) | Harness-evolving Agent；Memory / Skill / Tool / Workflow Agent | 分析 Evolver 写更新与 Task-Solver 使用更新是否等价 | 不改模型参数；更新外部 harness；通过交叉实验解耦 Evolver 和 Task-Solver | SWE-bench Verified、MCP-Atlas、SkillsBench | 任务成功率 / benchmark 分数；Harness activation / adherence 等诊断指标 | 有代码仓库；具体实验依赖多模型组合 |
| [Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | Tool-use Agent 理论；Theory of Agent；工具调用校准 Agent | 判断何时内部推理、何时调用外部工具；分析 overthinking、overacting、over-delegation | 主要是理论建模；提出 internal task set、world task set、knowledge boundary、epistemic effort | 无新增 benchmark；position paper 侧重概念框架 | 无传统实验指标；建议关注 effort allocation、tool-use necessity、process-level calibration | 暂未找到官方代码；有 arXiv 和官方项目页 |
| [SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | Code Agent；SWE-bench Agent；Trajectory-level Self-Evolving Agent；Test-Time Search Agent | 真实 GitHub issue 修复；多步代码定位、编辑、测试和补丁生成 | 不训练模型参数；测试时构造 trajectory pool；通过 Revision、Recombination、Refinement 迭代优化轨迹 | SWE-bench Verified | Pass@1 / resolution rate；Pass@5；trajectory reward / evaluation score | 官方代码已开源；基于 SWE-Agent，可作为外层轨迹优化模块 |
| [Self-Challenging Language Model Agents](../notes/self-challenging-language-model-agents.md) | Tool-use Agent；Self-Challenging Agent；Synthetic-task Agent | 多轮工具使用、环境探索、自动任务生成与验证 | Code-as-Task；one-step REINFORCE / Rejection Fine-Tuning；SFT distillation；DPO / PPO / GRPO 消融 | M3ToolEval：Calculation、Web Browsing；TauBench：Retail、Airline | Pass@1、Pass@4 | 暂未找到官方公开代码；实验设计较清晰 |
| [Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | Self-referential Agent；Recursive Self-Improvement Agent；Agent Design Search system；Program-level Self-Modifying Agent | 通过读取、评估和修改自身代码来搜索更大的 agent design space；数学推理、阅读理解、多任务知识问答、科学问答、Game of 24 案例 | 不训练模型参数；通过 runtime self-inspection、dynamic code modification、monkey patching、环境反馈和递归调用修改 agent policy / self-improvement loop | DROP、MGSM、MMLU、GPQA；Game of 24 case study | DROP F1；MGSM / MMLU / GPQA Accuracy；95% bootstrap CI；accidental termination、temporary drop、optimization failure | 官方代码已开源；MIT License；依赖 OpenAI API key 和任务环境；暂未找到官方模型权重 |

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

代表论文：**Harness Updating Is Not Harness Benefit**、**Agentic Context Engineering**。

这一类工作不一定训练模型参数，而是研究 prompt、memory、skill、tool、workflow 等外部 harness 如何更新，以及 Task-Solver 是否真的能使用这些更新。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | 代码修复、工具调用、技能复用、复杂任务执行、领域推理 |
| 更新对象 | prompt、skill、memory、tool 使用方式、workflow、context playbook |
| 核心变量 | Evolver 与 Task-Solver 分离；上下文更新是否真的被后续 Generator 使用 |
| 诊断重点 | Harness Updating 与 Harness Benefit 是否一致；上下文是否发生 collapse / brevity bias |
| 常见失败 | Harness Activation Failure；Harness Adherence Failure；context collapse；错误经验污染 playbook |
| 关键问题 | 性能瓶颈是在“写更新”，还是在“会不会用更新”？更新后的上下文是否保留了足够细节？ |

### 2.3 Context Engineering / Playbook Agent

代表论文：**Agentic Context Engineering**。

这一类工作把 prompt、memory、示例、领域规则和工具使用策略看成可持续维护的上下文资产。它不直接改模型参数，而是让系统从历史轨迹和反馈中提取经验，再写入结构化 playbook。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | Agent 工具调用、API 操作、领域信息抽取、领域计算 |
| 更新对象 | context playbook；结构化 bullet；helpful / harmful 计数；delta context items |
| 核心角色 | Generator、Reflector、Curator |
| 反馈来源 | ground-truth labels；自然执行反馈；环境成功 / 失败信号 |
| 训练方式 | 不训练模型参数；offline / online context adaptation |
| 常见指标 | AppWorld Average / TGC / SGC；Accuracy；latency；rollouts；token cost |
| 关键问题 | 上下文能否像经验库一样持续增长，同时避免反复摘要导致细节丢失？ |

### 2.4 Tool-use / Synthetic-task Agent

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

### 2.5 Tool-use Calibration / Theory of Agent

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

### 2.6 Code Agent / Trajectory Optimization Agent

代表论文：**SE-Agent**。

这一类工作关注真实代码仓库任务中，Agent 如何保存、反思、重组和筛选完整执行轨迹。它不一定更新模型参数，而是把测试时的多条轨迹看成可演化对象。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | 真实 GitHub issue 修复、代码定位、补丁生成、测试验证 |
| 基础框架 | SWE-Agent 作为基础 CodeAct agent；SWE-Search / MCTS 作为强 baseline |
| 轨迹来源 | 多 planning strategy 生成的初始轨迹池；mutation-based diversification |
| 核心操作 | Revision、Recombination、Refinement |
| 训练方式 | 不改模型参数；测试时轨迹池优化 / test-time search |
| 常见指标 | Pass@1 / resolution rate、Pass@5、trajectory reward |
| 关键问题 | 多条失败或半成功轨迹能否被组合成更好的解，而不是只做 best-of-N？ |

### 2.7 Self-Referential / Recursive Self-Improvement Agent

代表论文：**Gödel Agent**。

这一类工作把 Agent 本身看成可执行、可读取、可修改的程序系统。它不只是更新 prompt、memory、经验库或执行轨迹，而是让 Agent 在运行时读取自己的代码、动作集合和改进逻辑，并通过 monkey patching / dynamic code modification 改写后续递归调用的行为。

典型实验设置：

| 维度 | 内容 |
|---|---|
| 任务类型 | 阅读理解、数学推理、多领域选择题、科学问答、Game of 24 程序化求解 |
| 更新对象 | agent policy、action functions、self-improvement loop、solver function、工具调用逻辑 |
| 核心机制 | self-inspection、environmental interaction、self-update、continue-improve、runtime monkey patching |
| 反馈来源 | validation set / task utility function / 环境执行反馈 |
| 训练方式 | 不训练模型参数；通过 LLM 生成代码修改并递归评估 |
| 常见指标 | F1、Accuracy、bootstrap confidence interval、temporary drop / optimization failure 等鲁棒性统计 |
| 关键问题 | Agent design space 能否从“人类预设更新算法”扩展到“Agent 自己改写更新算法”？ |

---

## 3. 常见数据集与环境

| 数据集 / 环境 | 出现论文 | 类型 | 作用 |
|---|---|---|---|
| AppWorld | Agentic Context Engineering | Agent / API / 工具调用 benchmark | 测试 ReAct Agent 在 API 操作、环境交互、test-normal / test-challenge 上的任务完成能力 |
| FiNER | Agentic Context Engineering | 金融 XBRL 信息抽取 | 测试 token-level 细粒度金融实体识别和领域规则学习 |
| Formula / XBRL filings | Agentic Context Engineering | 金融数值推理 / 公式计算 | 测试从 XBRL filings 中抽取数值并执行计算的能力 |
| Natural Questions | EvolveR | 开放域问答 | 域内训练 / 经验库构建 / 评测 |
| HotpotQA | EvolveR | 多跳问答 | 域内训练 / 经验库构建 / 评测 |
| TriviaQA | EvolveR | 开放域问答 | 域外泛化评测 |
| PopQA | EvolveR | 长尾事实问答 | 域外泛化评测 |
| 2WikiMultiHopQA | EvolveR | 多跳问答 | 域外泛化评测 |
| MuSiQue | EvolveR | 多跳问答 | 域外泛化评测 |
| Bamboogle | EvolveR | 多跳 / 组合问答 | 域外泛化评测 |
| SWE-bench Verified | Harness Updating Is Not Harness Benefit、SE-Agent | 代码修复 Agent benchmark | 测试真实 GitHub issue 修复能力；SE-Agent 用于评估轨迹级测试时优化 |
| MCP-Atlas | Harness Updating Is Not Harness Benefit | MCP 工具调用 benchmark | 测试多工具调用和复杂任务执行 |
| SkillsBench | Harness Updating Is Not Harness Benefit | Skill 使用 benchmark | 测试 skill 加载、复用和执行能力 |
| M3ToolEval - Calculation | Self-Challenging Language Model Agents | 工具使用环境 | 测试计算类多轮工具调用 |
| M3ToolEval - Web Browsing | Self-Challenging Language Model Agents | 工具使用环境 | 测试网页浏览和信息提取 |
| TauBench - Retail | Self-Challenging Language Model Agents | 交互式工具环境 | 测试零售客服、订单、退换货等任务 |
| TauBench - Airline | Self-Challenging Language Model Agents | 交互式工具环境 | 测试航班查询、改签、订票等任务 |
| DROP | Gödel Agent | 阅读理解 / 离散推理 benchmark | 测试 Agent 自我修改后的阅读理解、数值计算和离散推理能力 |
| MGSM | Gödel Agent | 多语言数学推理 benchmark | 测试自指递归改进对数学推理和多语言泛化的影响 |
| MMLU | Gödel Agent | 多任务知识与推理 benchmark | 测试自改 Agent 在多领域选择题上的泛化表现 |
| GPQA | Gödel Agent | 高难科学问答 benchmark | 测试自改 Agent 在研究生级科学问答上的表现 |
| Game of 24 | Gödel Agent | 程序化推理 / 搜索案例 | 观察 Agent 是否能从 LLM-based 解法切换到搜索算法或 code-assisted verification |
| 暂无新增 benchmark | Theory of Agent | 理论 / position paper | 用于提出工具调用校准框架，而不是报告新实验 |

---

## 4. 常见对比方法 / baseline

| 类别 | 代表方法 | 出现论文 | 说明 |
|---|---|---|---|
| 直接推理 | Direct Inference | EvolveR | 不显式使用复杂检索或训练的基础设置 |
| 基础 Agent | Base LLM / ReAct | Agentic Context Engineering | 不做上下文适配，直接用基础模型执行任务 |
| 显式推理 | Chain-of-Thought | EvolveR、Gödel Agent | 用推理链增强回答；Gödel Agent 中也作为初始 policy / baseline |
| 自一致性推理 | CoT-SC | Gödel Agent | 多次采样后投票或选择一致答案，作为 hand-designed agent baseline |
| 反思修正 | Self-Refine | Gödel Agent | 固定反思 / 修正流程；用于对比自指递归改进是否更强 |
| 多 Agent 辩论 | LLM Debate | Gödel Agent | 通过多个角色或模型讨论得到答案，属于 hand-designed agent baseline |
| 抽象提示 | Step-back Abstraction | Gödel Agent | 先抽象问题再解题，用于对比固定 prompt 策略 |
| 多样性搜索 | Quality-Diversity | Gödel Agent | 通过多样化候选提高覆盖度，但更新机制仍由人类预设 |
| 角色分配 | Role Assignment | Gödel Agent | 通过角色设定增强推理，是固定 agent design baseline |
| 检索增强推理 | IRCoT、RAG、Search-o1 | EvolveR | 引入外部知识检索 |
| In-context Learning | ICL | Agentic Context Engineering | 把示例放入上下文，作为 context adaptation 的基础 baseline |
| Prompt Optimization | MIPROv2、GEPA | Agentic Context Engineering | 用 prompt optimizer 或 reflective prompt evolution 改进系统提示词 |
| Adaptive Memory | Dynamic Cheatsheet / DC-CU | Agentic Context Engineering | 测试时维护 cheatsheet / memory 的在线适配方法 |
| 工具调用校准 | Epistemically necessary tool use | Theory of Agent | 关注是否真的需要调用工具，而不只看调用后是否答对 |
| 监督学习 | SFT、LoRA | EvolveR、Self-Challenging Language Model Agents | 用示范轨迹或筛选轨迹微调模型 |
| 轨迹筛选 | Rejection Sampling / Rejection Fine-Tuning | EvolveR、Self-Challenging Language Model Agents | 只用成功轨迹或高质量轨迹训练 |
| 轨迹级测试时优化 | SE-Agent | SE-Agent | 通过 revision、recombination、refinement 操作完整轨迹，不训练模型参数 |
| CodeAct Agent | SWE-Agent | SE-Agent | 代码修复基础 agent，作为 SE-Agent 的底层框架和 baseline |
| MCTS Agent | SWE-Search | SE-Agent | 用 MCTS 做搜索增强的代码修复 agent，是 SE-Agent 的强 baseline |
| RL Agent | R1-base、R1-instruct、Search-R1-base、Search-R1-instruct | EvolveR | 与搜索增强 RL Agent 对比 |
| Offline preference / RL | DPO | Self-Challenging Language Model Agents | 在固定轨迹上进行偏好优化消融 |
| Online RL | PPO、GRPO | EvolveR、Self-Challenging Language Model Agents | 在线采样和策略优化，收益可能更高但更不稳定 |
| 自动任务生成 | PAE | Self-Challenging Language Model Agents | 和 SCA 对比任务生成与验证机制 |
| 自动 Agent 设计搜索 | Meta Agent Search | Gödel Agent | 固定 meta-learning algorithm 优化 agent policy；用于对比 Gödel Agent 是否突破固定优化器限制 |
| 自指递归改进 | Gödel-base / Gödel-free | Gödel Agent | Gödel-base 是受控设置；Gödel-free 允许更自由地调用更强工具或模型，不应和固定资源 baseline 简单等价比较 |
| 交叉诊断 | 固定 Task-Solver 替换 Evolver；固定 Evolver 替换 Task-Solver | Harness Updating Is Not Harness Benefit | 用于拆解“写更新”和“用更新”两个能力 |

---

## 5. 常见评价指标

| 指标 | 适用场景 | 说明 |
|---|---|---|
| Exact Match | 开放域 / 多跳问答 | 预测答案与标准答案标准化后完全一致 |
| F Score / F1 | 问答任务补充分析；DROP | 允许部分匹配，更适合别名、长答案、阅读理解和离散推理场景 |
| Accuracy | 分类、抽取、公式计算、数学推理、多选题 | ACE 在 FiNER / Formula 中使用；Gödel Agent 在 MGSM / MMLU / GPQA 中使用 |
| Task Goal Completion / TGC | AppWorld | 任务目标完成度，关注具体任务目标是否完成 |
| Scenario Goal Completion / SGC | AppWorld | 场景级目标完成度，关注完整场景目标是否完成 |
| Average | AppWorld / 多任务汇总 | 多 split 或多指标平均分，ACE 用于汇总 AppWorld 表现 |
| Pass@1 | 工具调用 / 交互式任务 / 代码修复 | 单次采样是否成功；在 SE-Agent 中也对应 resolution rate |
| Pass@4 | 工具调用 / 交互式任务 | 多次采样中是否至少一次成功 |
| Pass@5 | 代码修复 / SWE-bench | 五次尝试中是否至少一次成功，反映有限预算下的搜索效率 |
| Success Rate / Benchmark Score | Agent benchmark | 不同 benchmark 自带的成功率或评分 |
| Trajectory Reward / Evaluation Score | 轨迹级优化 Agent | 对完整轨迹的任务完成度、推理质量和效率进行综合打分 |
| Harness Activation | Harness 诊断 | 是否正确检索、加载、激活相关 harness |
| Harness Adherence | Harness 诊断 | 激活后是否持续遵循 skill / memory / workflow |
| Tool-use Necessity | 工具调用校准 | 外部工具调用是否在知识上必要，是否真的减少不确定性 |
| Effort Allocation | Theory of Agent / Agentic RL | 内部推理 effort 与外部工具 effort 是否和任务需求匹配 |
| Adaptation Latency | Context Engineering / Prompt Optimization | 完成上下文适配需要的时间，ACE 用于比较 GEPA / DC 等方法 |
| Rollouts / Token Cost | Agentic adaptation | 为了得到更新所需的执行次数和 token 成本 |
| Bootstrap Confidence Interval | 多 benchmark 统计显著性 | Gödel Agent 主实验报告 95% bootstrap confidence interval，用于说明分数不确定性 |
| Accidental Termination | 自修改 Agent 鲁棒性 | Gödel Agent 用于统计递归自改过程是否意外终止 |
| Temporary Drop | 自修改 Agent 鲁棒性 | 统计自改过程中性能是否短暂下降，说明改进并非单调 |
| Optimization Failure | 自修改 Agent 鲁棒性 | 统计最终是否未能超过初始策略或优化失败 |

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

### 6.3 从“外部知识检索”转向“内部经验检索 / 上下文 playbook”

EvolveR 的重要启发是：

- 外部搜索解决事实知识问题；
- 内部经验检索解决问题解决策略问题。

ACE 进一步把“内部经验”直接维护成 context playbook：prompt、领域规则、工具使用策略、失败模式都可以作为结构化上下文条目持续增长。

后续读论文时，需要区分：论文里的 memory 到底是存事实、存轨迹、存经验原则、存可执行 skill，还是存可直接进入 prompt 的 playbook。

### 6.4 从“反思器更强”转向“求解器是否会用”

Harness Updating Is Not Harness Benefit 的重要提醒是：

- Evolver 写出好更新，不等于 Task-Solver 能用好更新；
- 弱模型可能不会激活相关 harness；
- 强模型可能原本就接近上限，提升空间有限；
- 中等模型反而可能最能吃到 harness 更新红利。

ACE 也验证了类似问题：上下文不是越短越好、也不是写了就有效。关键在于 Generator 能不能在后续任务中真正利用 playbook 中的细节。

### 6.5 从“会调用工具”转向“该不该调用工具”

Theory of Agent 的重要提醒是：

- 工具调用不是越多越好；
- 最终答对不代表工具调用过程合理；
- 需要区分 closed-book 内部能力和 open-book 工具增强能力；
- 自演化 Agent 不应让外部工具完全替代内部学习。

后续读 tool-use / RAG / search agent 论文时，可以增加一个检查项：论文是否分析了工具调用的必要性，而不只是报告有工具后的成功率。

### 6.6 从“多次采样”转向“轨迹级重组”

SE-Agent 的重要提醒是：

- best-of-N 只是从多条独立轨迹里挑一个，未必能产生真正新的解法；
- 多条轨迹中可能分别包含正确文件定位、有效测试分析、合理 patch 结构等局部优势；
- 轨迹级 revision / recombination / refinement 可以把这些局部优势重新组合；
- 这类方法更像测试时外层优化器，不一定带来长期参数能力提升。

后续读 Code Agent / SWE-bench / Web Agent 论文时，可以增加一个检查项：论文是否只是增加采样次数，还是显式利用了轨迹之间的信息互补。

### 6.7 从“prompt 优化”转向“上下文资产治理”

ACE 的重要提醒是：prompt / memory 不应该只是一个反复被 LLM 重写的字符串，而应该被当成可维护资产：

- 有结构化条目；
- 有增量更新；
- 有 helpful / harmful 统计；
- 有去重、合并、剪枝；
- 有离线优化和在线更新两种路径；
- 有成本指标，如 latency、rollouts、token cost。

这类工作更接近真实 Agent 系统工程：不是只问“提示词怎么写”，而是问“上下文如何长期维护、审计、复用和防止污染”。

### 6.8 从“外部组件自演化”转向“程序级自修改”

Gödel Agent 的重要提醒是：self-evolving agent 的进化对象还可以继续前推。它不只改 prompt、memory、experience base 或 trajectory pool，而是直接改 agent 的可执行程序逻辑。

这带来一个新的实验设计维度：

- Agent 是否能读取自身代码？
- Agent 是否能修改 action set、solver、evaluation loop 或 self-improvement loop？
- 修改后是否经过 validation set、sandbox、回滚和鲁棒性测试？
- 自修改是否真的带来跨任务泛化，还是只是在 validation set 上过拟合？
- 更自由的 Gödel-free 设置是否引入了不公平资源优势，例如调用更强模型？

后续读 recursive self-improvement / self-referential agent 论文时，可以增加一个检查项：**论文里的“自我改进”到底是在改外部文本资产，还是在改可执行程序本身？**

---

## 7. 后续新增论文时建议补充的字段

后续每读一篇新论文，建议在单篇笔记之外，同步补充本文件中的这些字段：

| 字段 | 填写说明 |
|---|---|
| 论文 | 论文标题和本仓库笔记链接 |
| 实验对象 | Search Agent / Tool-use Agent / Web Agent / Coding Agent / Memory Agent / Harness Agent / Context Engineering Agent / Self-Referential Agent 等 |
| 核心任务 | 问答、代码修复、网页操作、工具调用、客服环境、数据库操作、领域抽取、领域计算、数学推理、程序级自修改等 |
| 训练数据 | 人工数据、历史轨迹、synthetic tasks、成功轨迹、偏好数据、上下文 playbook 条目、validation feedback 等 |
| 测试数据集 / 环境 | benchmark 名称、子任务名称、域内 / 域外划分、case study 环境 |
| 基础模型 | Llama、Qwen、GPT、Claude、DeepSeek 等，以及模型规模 |
| 训练方法 | SFT、RFT、DPO、PPO、GRPO、REINFORCE、无训练、context adaptation、dynamic code modification 等 |
| 对比方法 | baseline、ablation、previous methods |
| 评价指标 | EM、F1、Accuracy、Pass@k、success rate、reward、TGC / SGC、latency、token cost、人工评分、鲁棒性统计等 |
| 主要结论 | 这篇实验最想证明什么 |
| 复现性 | 是否开源代码、数据、模型、环境配置 |

---

## 8. 维护原则

1. **先粗后细**：新增论文时先补总览表，再逐步补数据集和 baseline。
2. **能表格化就表格化**：横向比较优先用表格，避免写成第二篇长读书笔记。
3. **保留不确定项**：不确定的信息写“待补充”，不要强行猜。
4. **和单篇笔记互相链接**：详细解释放在 `notes/`，本文件只保留对比信息。
5. **关注实验设计，而不只是结果分数**：重点记录实验对象、数据来源、对比方法、指标和结论边界。
