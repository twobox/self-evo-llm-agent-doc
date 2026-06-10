<!--
metadata:
  title: 'Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement'
  short_title: 'Gödel Agent'
  year: 2025
  note_type: '中文读书笔记'
  paper_type: 'method / framework / self-referential agent paper'
  status: 'ACL 2025 Long Paper；arXiv v4 submitted on 2025-05-31；官方代码已开源'
  venue: 'ACL 2025 / arXiv'
  arxiv_id: '2410.04444'
  arxiv_url: 'https://arxiv.org/abs/2410.04444'
  pdf_url: 'https://arxiv.org/pdf/2410.04444'
  html_url: 'https://arxiv.org/html/2410.04444v4'
  code_url: 'https://github.com/Arvid-pku/Godel_Agent'
  original_code_url: 'https://github.com/Arvid-pku/Godel_Agent'
  model_url: ''
  authors:
    - 'Xunjian Yin'
    - 'Xinyi Wang'
    - 'Liangming Pan'
    - 'Li Lin'
    - 'Xiaojun Wan'
    - 'William Yang Wang'
  institutions:
    - 'Peking University'
    - 'University of California, Santa Barbara'
    - 'University of Arizona'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Recursive Self-Improvement'
    - 'Self-Referential Agent'
    - 'Agent Design Search'
    - 'Dynamic Code Modification'
    - 'Monkey Patching'
  tags:
    - 'LLM Agent'
    - 'self-evolution'
    - 'recursive self-improvement'
    - 'self-reference'
    - 'self-modification'
    - 'agent design space'
    - 'Meta Agent Search'
    - 'DROP'
    - 'MGSM'
    - 'MMLU'
    - 'GPQA'
  related_notes:
    - 'evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'harness-updating-is-not-harness-benefit.md'
    - 'agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md'
    - 'se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md'
    - 'self-challenging-language-model-agents.md'
  created: '2026-06-10'
  updated: '2026-06-10'
-->

# 《Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement》读书笔记

## 1. 基本信息

- 论文标题：Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement
- ACL Anthology：<https://aclanthology.org/2025.acl-long.1354/>
- arXiv：<https://arxiv.org/abs/2410.04444>
- PDF：<https://arxiv.org/pdf/2410.04444>
- arXiv HTML：<https://arxiv.org/html/2410.04444v4>
- 代码仓库：<https://github.com/Arvid-pku/Godel_Agent>
- 模型权重：暂未找到官方公开模型权重。

标题说明：arXiv 页面标题使用 **Recursive Self-Improvement**，ACL Anthology 页面标题写作 **Recursively Self-Improvement**。本笔记文件名采用用户提供标题与 arXiv 标题中的 `recursive-self-improvement`，正文中以 Gödel Agent 简称。

这篇论文研究的是：**能不能让 LLM Agent 不只是改 prompt、改 memory、改外部经验库，而是让 Agent 读取和修改自己的运行时代码，包括负责“如何改自己”的逻辑，从而形成递归自我改进。**

我理解这篇文章的关键词是：**自指 Agent**、**递归自我改进**、**Agent 设计空间搜索**、**运行时代码自修改**、**monkey patching**。

> 图表选择说明：本文只放两张最能解释核心思想的官方图：一张比较 hand-designed / meta-learning optimized / self-referential 三类 agent，一张解释 Gödel Agent 如何通过 monkey patching 读写自身运行时代码。主实验表和消融表已经转写成 Markdown，便于检索和横向对比。

## 2. 投稿 / 发表状态

- arXiv 编号：`2410.04444`。
- arXiv v1 提交时间为 2024-10-06；当前可见版本为 v4，提交时间为 2025-05-31。
- ACL Anthology 显示该论文收录于 **ACL 2025 Long Papers**，会议地点为 Vienna, Austria，页码为 27890–27913，DOI 为 `10.18653/v1/2025.acl-long.1354`。
- 官方 GitHub 仓库已公开，README 显示为 MIT License。

因此，这篇文章目前可以看作 **ACL 2025 Long Paper + arXiv 预印本 + 官方代码已开源**。

## 3. 作者与机构

论文作者为：Xunjian Yin, Xinyi Wang, Liangming Pan, Li Lin, Xiaojun Wan, William Yang Wang。

arXiv v4 HTML 首页给出的机构为：

- Peking University / 北京大学
- University of California, Santa Barbara / 加州大学圣塔芭芭拉分校
- University of Arizona / 亚利桑那大学

从署名和机构看，这篇论文主要来自 **北大 + UCSB NLP + Arizona NLP / Agent 研究圈**。

## 4. 作者背景和研究圈子

Xunjian Yin 个人主页显示，他目前是 Duke University CS PhD student，由 Shuyan Zhou 和 Bhuwan Dhingra 共同指导；此前经历包括 Peking University、Microsoft Research 和 UCSB NLP Group。主页还明确写到，他研究 AI systems 如何在 long horizon 上 recursively self-improve，重点包括 self-referential agents 和 world models。

William Yang Wang 是 UCSB NLP Group 的核心学者，长期研究 NLP、机器学习、推理、生成式智能和可信 AI。Xunjian Yin 的主页也把 UCSB NLP Group 和 William Yang Wang 列为其此前研究经历之一。

Xiaojun Wan 是北京大学 NLP / 信息管理方向的学者，Xunjian Yin 主页也显示其此前在 Peking University 期间与 Xiaojun Wan 有关联。Liangming Pan 署名机构为 University of Arizona，此前也参与过 LLM self-correction 相关综述工作。

所以，这篇论文不是单纯做一个 prompt trick，而是延续了几条研究线：

1. **LLM Agent 自动设计**：从人工设计 agent，到自动搜索 agent design。
2. **Self-correction / Self-improvement**：让模型或系统利用反馈修正自己。
3. **Recursive Self-Improvement**：不仅改任务求解策略，也改“如何改策略”的机制。
4. **Agent 系统工程**：把 agent 看成可运行、可修改、可评估的程序系统。

我暂未找到所有作者稳定个人主页的完整履历，因此作者背景部分主要依据 arXiv / ACL 页面、Xunjian Yin 个人主页和公开项目信息进行概括。

## 5. 所属研究方向与论文定位

这篇论文属于 **Self-Evolving LLM Agent** 方向，但它和仓库里已有几篇笔记的“进化对象”不一样。

| 工作 | 主要进化对象 | 知识 / 经验存储位置 | 后续如何使用 | 是否主要训练模型参数 |
|---|---|---|---|---|
| Gödel Agent | agent 自身代码、策略、动作集合，以及负责自我改进的逻辑 | 运行时代码、被 monkey patch 的模块、生成后的 agent code / results | 下一轮递归调用直接使用被改写后的逻辑 | 否，主要是程序 / 策略级自修改 |
| EvolveR | 经验原则、经验库、executor 能力 | experience base、训练数据、模型参数 | 检索经验 + SFT / GRPO 更新 executor | 是 |
| ACE | context playbook / 可维护上下文资产 | 外部 playbook / context items | 下次任务拼接到上下文 | 否 |
| SE-Agent | 同一任务中的多条执行轨迹 | trajectory pool | 测试时 revision / recombination / refinement | 否 |
| Self-Challenging | 自生成任务、验证器、训练轨迹 | synthetic tasks 和训练集 | 训练 task executor | 是 |
| Harness Updating | prompt / memory / skill / workflow 等 harness | 外部 harness | Task-Solver 后续调用或遵循 | 否 |

这篇文章的定位可以概括为：**把 agent 本身当成一个可以被 agent 读取、评估、修改、递归调用的程序系统，尝试突破固定 pipeline 或固定 meta-learning algorithm 对 agent design space 的限制。**

## 6. 核心问题

论文要解决的问题是：

> 现有 agent 系统通常由人类预先规定 pipeline、模块、更新规则或 meta-learning routine。这样的系统即使可以“自我改进”，也仍然被人类设计的外壳限制。能不能让 agent 直接修改自身逻辑，包括修改负责自我改进的逻辑，从而搜索更大的 agent 设计空间？

作者把已有方法分成三类：

1. **Hand-Designed Agent**：人类设计固定流程，例如 CoT、Self-Refine、Debate、Role Assignment 等。
2. **Meta-Learning Optimized Agent**：允许 agent policy 被某个固定的 meta-learning algorithm 更新，但这个更新算法本身不变，例如 Meta Agent Search。
3. **Self-Referential Agent / Gödel Agent**：不仅更新 policy，还能更新负责更新 policy 的算法，也就是让 agent 可以读写自己的代码和行为逻辑。

这也是论文标题里 Gödel 的含义：它借鉴 Gödel Machine 的“自指 / 自我修改”思想，但在实现上不是严格形式证明驱动，而是用 LLM、环境反馈和运行时代码修改做一个工程化版本。

## 7. 方法：Gödel Agent 的自指递归自我改进框架

![Comparison of three agent paradigms](https://raw.githubusercontent.com/Arvid-pku/Godel_Agent/main/figures/compare.png)

> **图 1：三类 agent 范式对比。** 左边是人类手写固定 agent，中间是固定 meta-learning 算法更新 agent，右边是 Gödel Agent：agent 可以修改自己的策略和自我改进机制，因此自由度最高。

### 7.1 形式化理解

论文把一个 agent 看成在环境中执行某个 policy 的系统。传统 hand-designed agent 的 policy 是固定的；meta-learning optimized agent 可以根据环境反馈更新 policy，但更新算法本身是固定的。

Gödel Agent 的关键区别是：

- policy 可以变；
- 更新 policy 的 meta-learning algorithm 也可以变；
- agent 的 action set 也不是完全静态的，可以被扩展和修改；
- 每次递归之后，新的 agent code 会成为下一轮执行的主体。

换句话说，它不是只问“这道题怎么解”，而是问：

> “我现在这个解题程序、反思程序、工具调用方式和自我更新方式，应该怎么改，才能在后续任务上更好？”

### 7.2 四类基础动作

论文给出的初始 action function 至少包括四类动作：

| 动作 | 作用 | 我的理解 |
|---|---|---|
| `self_inspect` | 读取当前 agent algorithm / code | 让 agent 看见自己当前是怎么运行的 |
| `interact` | 和环境交互，调用 utility function 获取反馈 | 让 agent 知道当前策略好不好 |
| `self_update` | 通过 LLM 生成修改并更新自身逻辑 | 真正发生自我修改的地方 |
| `continue_improve` | 没有其他动作时递归调用改进过程 | 让改进进入下一轮，而不是只做一次反思 |

这里最关键的点是：**自我改进过程本身也是可被读取和修改的对象。** 这和常见 reflection agent 不一样。Reflection 通常只是“同一个反思器反复评估输出”；Gödel Agent 则试图让“反思器 / 更新器 / 执行器”都成为可修改对象。

### 7.3 工程实现：运行时代码检查 + monkey patching

![Gödel Agent implemented by Monkey Patching](https://raw.githubusercontent.com/Arvid-pku/Godel_Agent/main/figures/method.png)

> **图 2：Gödel Agent 的 monkey patching 实现。** 论文实现让 agent 在 Python runtime 中读取当前变量、函数、类和模块，然后动态写入新代码，从而改变后续递归调用中的 agent 行为。

论文实现有几个关键设计：

1. **Self-Awareness via Runtime Memory Inspection**：通过检查 Python 运行时的 local / global variables、functions、classes，让 agent 知道自己当前有哪些模块和逻辑。
2. **Self-Improvement via Dynamic Code Modification**：当 agent 判断需要修改逻辑时，由 LLM 生成新代码，并写回运行时环境。
3. **Environmental Interaction**：每个任务提供环境反馈或 utility function，agent 通过反馈判断策略是否更好。
4. **Recursive Improvement Mechanism**：每轮修改后，下一轮递归会使用新的 agent 逻辑。
5. **Goal Prompt**：不是针对某个具体任务写死，而是告诉 agent 它有权限优化自身逻辑，并可以使用工具和环境反馈。

这也是这篇论文和长期 memory / 经验库方法最大的区别：**它的“知识”不是主要存成外部文本经验，而是直接体现在被修改后的可执行逻辑里。**

### 7.4 初始辅助工具

论文还给 Gödel Agent 提供了一些辅助能力，用来降低初期自我改进难度：

| 初始能力 | 作用 |
|---|---|
| thinking before acting | 允许先分析和规划，再执行动作 |
| error handling | 代码修改出错时不要直接崩溃，而是把错误作为反馈进入后续决策 |
| code running | 可以执行 Python / Bash 代码，测试想法 |
| LLM calling | 可以调用 LLM 辅助生成或修正逻辑 |

这些工具不是理论上必须，但对工程收敛很重要。尤其是 error handling：自我修改代码天然容易出错，如果一出错就中断，递归自我改进会非常脆弱。

## 8. 实验设计

### 8.1 核心任务和 benchmark

论文在四个主要 benchmark 上评估：

| Benchmark | 任务类型 | 评价重点 |
|---|---|---|
| DROP | 阅读理解 / 离散推理 | 需要从段落中做数值和离散推理 |
| MGSM | 多语言数学推理 | 测试数学解题与多语言泛化 |
| MMLU | 多任务知识与推理 | 测试多领域选择题能力 |
| GPQA | 研究生级科学问答 | 测试高难科学问题求解 |

此外，论文用 **Game of 24** 做 case study，用来观察 agent 自己如何从 LLM-based 解法切换到搜索算法，或加入 code-assisted verification。

### 8.2 对比方法

论文对比了两类 baseline：

| 类型 | 方法 |
|---|---|
| Hand-designed agents | CoT、CoT-SC、Self-Refine、LLM Debate、Step-back Abstraction、Quality-Diversity、Role Assignment |
| Meta-learning optimized agent | Meta Agent Search |

这里的关键对比不是“某个 prompt 是否更强”，而是三种范式的对比：

1. 人类固定设计；
2. 固定 meta-learning algorithm 自动优化；
3. 自指 agent 递归修改自身。

### 8.3 设置细节

- 初始 policy 使用 CoT，因为它简单、通用，适合作为统一起点。
- 每个任务在 validation dataset 上做 6 个独立 self-improvement cycles。
- 每个 cycle 最多 30 次迭代。
- 得到优化后的 agent 后，再在 test set 上评估。
- 主实验使用 GPT-4o 驱动改进过程；公平设置中，测试任务默认使用 GPT-3.5、closed-book、无互联网。
- 论文另设 `Gödel-free` 无约束版本，用来观察开放场景上限。

需要注意：`Gödel-free` 的结果不能直接当作公平 baseline，因为论文分析指出，无约束时 agent 会主动请求更强模型，例如 GPT-4o，因此这更像是开放环境潜力展示，而不是严格同算力对比。

## 9. 主要结果

### 9.1 主实验结果

下表只转写主分数。论文原表同时报告 95% bootstrap confidence interval。

| Agent | DROP F1 | MGSM Acc. | MMLU Acc. | GPQA Acc. |
|---|---:|---:|---:|---:|
| Chain-of-Thought | 64.2 | 28.0 | 65.4 | 29.2 |
| CoT-SC | 64.4 | 28.2 | 65.9 | 30.5 |
| Self-Refine | 59.2 | 27.5 | 63.5 | 31.6 |
| LLM Debate | 60.6 | 39.0 | 65.6 | 31.4 |
| Step-back Abstraction | 60.4 | 31.1 | 65.1 | 26.9 |
| Quality-Diversity | 61.8 | 23.8 | 65.1 | 30.2 |
| Role Assignment | 65.8 | 30.1 | 64.5 | 31.1 |
| Meta Agent Search | 79.4 | 53.4 | 69.6 | 34.6 |
| Gödel-base | 80.9 | 64.2 | 70.9 | 34.9 |
| Gödel-free | 90.5 | 90.6 | 87.9 | 55.7 |

主要观察：

1. **Gödel-base 在公平约束下已经能接近或超过 Meta Agent Search。**
2. **MGSM 提升最明显**：Gödel-base 从 Meta Agent Search 的 53.4 提升到 64.2。
3. **Gödel-free 分数很高，但解释要谨慎**：它可以主动使用更强模型或更多资源，因此更像开放环境潜力，而不是严格公平对比。
4. **DROP 上提升相对小**：作者认为知识型 / 阅读型任务的可改进空间可能比数学推理任务更小。

### 9.2 初始工具消融

| 消融设置 | MGSM |
|---|---:|
| Gödel Agent | 64.2 |
| w/o thinking | 50.8 |
| w/o error handling | 49.4 |
| w/o code running | 57.1 |
| w/o LLM calling | 60.4 |

这个消融很重要：

- **thinking before acting** 和 **error handling** 对结果影响最大。
- code running 和 LLM calling 也有帮助，但论文认为它们更多是加速收敛；agent 理论上可以自己实现类似基础能力。
- 自我修改系统必须有容错机制，否则一次坏 patch 就可能终止整个递归过程。

### 9.3 鲁棒性分析

论文在 MGSM 上统计 100 次 optimization trials：

| 事件 | 频率 |
|---|---:|
| Accidental Termination | 4% |
| Temporary Drop | 92% |
| Optimization Failure | 14% |

这说明 Gödel Agent 的自我改进不是单调上升：

- 很多中间修改会让性能短暂下降；
- 但最终多数 trial 仍能超过初始 policy；
- 意外终止比例较低，但仍然存在，通常和修改 recursive improvement module 本身有关。

这对工程实践很有启发：**递归自改系统必须保留回滚、比较、沙箱和错误恢复机制，否则很容易把自己改坏。**

### 9.4 Game of 24 case study

Game of 24 案例展示了 Gödel Agent 的一个有意思现象：

- 初始时，它可能使用普通 LLM-based 解法。
- 多次失败后，它可以完全重写求解逻辑，切换成 search algorithm。
- 另一些运行中，它会保留 LLM-based 方法，但加入 code-assisted verification 或多次尝试机制。

这个案例说明，Gödel Agent 的价值不只是“把某个 prompt 改好一点”，而是可能从一个方法族跳到另一个方法族：例如从语言模型直接推理切换到搜索、验证、程序化求解。

## 10. 主要结论

我认为论文最重要的结论有四个：

1. **Self-referential agent 是比固定反思 / 固定 meta-learning 更高自由度的 agent 设计范式。**
2. **LLM 可以在环境反馈引导下修改 agent 程序逻辑，并在多类任务上带来性能提升。**
3. **递归自我改进不是稳定单调过程，错误处理、回滚和规划能力非常关键。**
4. **开放环境中的 Gödel Agent 会主动寻求更强工具或模型，因此“自由度”既是性能来源，也是公平评测和安全控制的挑战。**

## 11. 工程启发

### 11.1 自演化 Agent 的“进化对象”可以是程序本身

这篇论文提醒我：self-evolving agent 不一定只是在外部维护 memory / experience base，也不一定是训练模型参数。它还可以直接改：

- solver function；
- action function；
- tool list；
- evaluation / feedback 使用方式；
- recursive improvement loop；
- 调用外部模型或工具的策略。

这类方法更接近 **agent-as-program**：Agent 不是一段 prompt，而是一个可以被读取、运行、测试、修改、回滚的程序系统。

### 11.2 必须把自修改放进沙箱

如果要在真实工程中实现类似机制，我会优先考虑：

1. 每次修改生成 patch，而不是直接覆盖主逻辑；
2. 所有 patch 在 sandbox 中运行；
3. 通过单元测试 / benchmark / 回归测试筛选；
4. 只有通过评估的 patch 才能合并；
5. 保留历史版本，允许回滚；
6. 对可修改范围设置白名单，例如只能改 solver，不允许改权限、网络、文件系统、密钥读取逻辑。

### 11.3 环境反馈比“反思文字”更重要

Gödel Agent 的自改需要 utility function / feedback。如果反馈很弱、很稀疏或有漏洞，agent 可能会优化错误目标。工程上要重点设计：

- 可靠 validation set；
- 不易 reward hacking 的指标；
- 成本和效率惩罚；
- 安全约束；
- 多任务评估，避免只对单一 benchmark 过拟合。

### 11.4 和经验库方法可以结合

Gödel Agent 本文主要强调自修改代码；EvolveR / ACE 强调经验库和上下文资产。二者可以结合：

- 经验库记录哪些修改有效、哪些修改失败；
- 自修改 agent 从经验库检索历史 patch pattern；
- 失败 patch 被总结成 guardrail；
- 成功 patch 被抽象成可复用 skill 或 template。

这样可能比单纯让 LLM 每次从零写 patch 更稳。

## 12. 局限性

1. **更像 proof-of-concept，而不是成熟通用 Agent。** 论文也承认，作为第一个 self-referential agent，它没有直接对比 OpenDevin 等高度工程化系统，因为那些系统包含大量人工工程投入。
2. **自我修改存在不稳定性。** MGSM 统计中 temporary drop 很常见，optimization failure 也并非罕见。
3. **公平评测比较复杂。** `Gödel-free` 可以调用更强模型和更多工具，因此不能和固定资源 baseline 简单比较。
4. **安全边界需要额外设计。** 论文讨论到，能力更强的自修改 agent 需要人类监督和受控环境。
5. **依赖任务反馈质量。** 如果 utility function 不可靠，agent 可能朝错误方向自我优化。
6. **暂未找到官方模型权重。** 目前复现主要依赖代码、数据、OpenAI API key 和任务环境。

## 13. 我的理解与总结

我觉得这篇文章的重要性不在于它已经实现了真正意义上的“无限递归自我改进”，而在于它把 self-evolving agent 的进化对象往前推了一层：

- 不是只改回答；
- 不是只改 prompt；
- 不是只改 memory；
- 不是只改外部经验库；
- 而是改 agent 的可执行逻辑，甚至改“如何改自己”的逻辑。

用一句话概括：

> **Gödel Agent 把 Agent 从“会反思的解题器”推进到“能读写自身程序的自指系统”。**

但我也会谨慎看待它的结论：当前实现仍然高度依赖 LLM 生成代码、环境反馈、错误恢复和受控 benchmark。它证明了一个方向的可行性，却还没有解决长期稳定性、安全边界、跨任务持续积累和真实复杂系统复现问题。

和仓库里已有论文放在一起看，它正好补上一个新的维度：

- EvolveR：经验库 + 参数更新；
- ACE：上下文 playbook 自进化；
- SE-Agent：测试时轨迹池优化；
- Self-Challenging：自生成任务 + 训练 executor；
- Harness Updating：分析更新是否真的被使用；
- Gödel Agent：自指程序级自修改。

所以，这篇论文适合作为 self-evolving LLM agent 方向中的一个“边界型”工作来读：它把问题推到最激进的位置——**如果 agent 能改自己，那么 agent design 本身也可以成为搜索空间。**

## 14. 参考链接

- arXiv abstract：<https://arxiv.org/abs/2410.04444>
- arXiv PDF：<https://arxiv.org/pdf/2410.04444>
- arXiv HTML v4：<https://arxiv.org/html/2410.04444v4>
- ACL Anthology：<https://aclanthology.org/2025.acl-long.1354/>
- 官方 GitHub：<https://github.com/Arvid-pku/Godel_Agent>
- Xunjian Yin 个人主页：<https://xunjianyin.github.io/>
