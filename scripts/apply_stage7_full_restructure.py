#!/usr/bin/env python3
"""Apply the Stage 7 evidence-layer and body-order migration to the remaining notes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
H2_RE = re.compile(r"(?m)^## (.+)$")
UPDATED = "2026-06-25"

HARNESS_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| Harness Updating 与 Harness Benefit 是两种不同能力 | 固定 Task-Solver 替换 Evolver，以及固定 Evolver 替换 Task-Solver 的交叉实验 | 只看端到端自演化收益 | 能把更新生成端与更新使用端的瓶颈分开诊断 | 不能把一次性能变化完全归因到单个模块，接口、检索和任务难度仍会共同影响结果 |
| 更强 Evolver 不一定稳定写出更有用的外部更新 | Qwen3.5-9B 生成的更新在部分场景接近 Claude Opus 4.6；三个 benchmark 上没有模型始终领先 | 不同能力等级的 Evolver，在同一 Task-Solver 下比较 | 支持当前外部 prompt / skill / memory 更新能力随基础模型能力提升较平坦 | 不能推广到参数训练、不同更新格式或所有模型家族，也不等于 Evolver 完全不重要 |
| Harness Benefit 与模型能力不是单调关系 | 固定更新后比较不同 Task-Solver，呈现弱模型收益小、中等模型收益大、强模型受天花板限制的模式 | 同一 harness 下不同能力的 Task-Solver | 说明“提升空间大”不等于“能吃到更新红利” | 不能给出所有任务上的统一最佳模型规模，曲线会受 benchmark 与 harness 接口影响 |
| 弱模型主要败在 activation 与 adherence | SkillsBench 等案例中观察到未加载相关 skill，以及加载后没有持续遵循 fallback 流程 | 已成功激活并遵循相同 harness 的轨迹 | 揭示外部经验从“存在”到“被执行”之间的两个具体故障点 | 案例和自动诊断不能证明所有弱模型失败都来自这两类原因 |

### 我的判断

这篇论文最强的贡献是实验拆解，而不是某个绝对分数。它把“反思器写得好不好”和“求解器会不会用”分开后，说明很多系统可能错把求解端故障归因给经验生成端。

结论应限定在冻结参数、外部 harness 演化和论文覆盖的三个 Agent benchmark。它没有证明 Evolver 永远不是瓶颈，也没有覆盖参数级持续训练。

### 其他可能解释

- 较强 Evolver 的优势可能被固定格式、有限更新预算或 Task-Solver 的使用上限压缩。
- Harness Benefit 的非单调曲线也可能受基础成功率、任务难度和上下文长度共同影响。
- Activation / adherence 的自动判断可能带有 evaluator 或 LLM Judge 偏好。
""".strip()

MEMOPILOT_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 训练得到的 memory updater 比完整历史或提示式 memory 更能帮助冻结 Player | Qwen2.5-14B Player 上，MemoPilot 的 RPS@5 / LHE@5 为 3.28 / 2.03；No Memory 为 0.43 / -1.36，Full History 为 0.02 / -1.22，提示式 Qwen2.5-14B memory 为 0.21 / -0.23 | No Memory、Full History、Human-Written Counter-Strategy、prompt-based memory updater | 在可控连续博弈中，RL 对齐的 memory 写入策略能显著改变后续行动收益 | 不能证明所有真实 Agent 流程都能提供同样清晰的奖励和可重复交互 |
| Memory 的可执行性比只描述正确事实更重要 | Ground-Truth Opponent Strategy 只有 0.75 / -0.48，Human Counter-Strategy 为 1.00 / 1.08，MemoPilot 为 3.28 / 2.07 | 正确对手描述、人工反制策略、重写后的 MemoPilot memory | 支持 memory 必须转换成 frozen Player 能执行的行动指导 | 不能说明当前三层文本结构是所有模型和任务的最优表达 |
| 结构化 memory 与 RL 训练具有互补性 | LHE@5：3-tier w/o RL 为 -0.23，free-form w/ RL 为 1.04，3-tier w/ RL 为 2.03 | 仅结构、仅 RL、完整组合 | 说明提升不只来自格式，也不只来自策略训练 | 不完全排除训练样本量和生成长度差异带来的影响 |
| 下一轮奖励更适合评价当前 memory update | LHE@5 中 cumulative reward 为 0.61，one-step proxy reward 为 2.03 | 累计回报式 credit assignment | 支持把第 t 次更新主要归因到第 t+1 轮，有助于降低跨轮信用分配噪声 | 不能证明一步代理奖励适合长延迟、跨多轮才生效的所有记忆 |
| Updater 能迁移到不同 Player 和非游戏任务 | 接到 Qwen3-235B 后为 3.27 / 1.31；StreamBench CoSQL / DS-1000 为 73.5 / 56.3，高于 No Memory 的 69.5 / 50.0 | 原训练 Player、No Memory、Full History、其他强模型 updater | 提供跨 Player 和有限真实任务流的迁移证据 | StreamBench 仅 32 个 held-out episodes，不能代表开放式 Web、Code 或 Office Agent |

### 我的判断

MemoPilot 的证据链较完整：主结果、结构消融、奖励消融和跨 Player 迁移共同支持“memory writer 可以作为独立策略训练”。尤其是 ground-truth strategy 不如可执行 counter-strategy，直接回应了 Harness Benefit 问题。

它的适用前提也很强：需要可计算 reward、多轮 rollout 和相对稳定的可复用规律。对手切换越频繁，LHE@5 从 2.03 下降到 1.76 和 1.21，说明非平稳环境仍是明显边界。

### 其他可能解释

- 博弈环境的奖励密集且可控，可能高估了真实 Agent 中 memory RL 的可训练性。
- MemoPilot 与部分 baseline 的训练预算、模型调用和优化程度未必完全等价。
- 512-token memory budget 有利于公平比较，但可能限制其他方法的最佳表现。
""".strip()

SE_AGENT_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 轨迹级演化优于独立采样和树搜索 | SWE-bench Verified 中 DeepSeek-V3：SE-Agent Pass@1 54.8%，SWE-Search 39.4%，SWE-Agent 31.6%；Claude-3.7：61.2%，对照为 47.4% / 40.6% | SWE-Agent、SWE-Search，在相同 LLM 行内比较 | 支持 revision / recombination / refinement 能提高代码修复任务的测试时搜索质量 | 不能证明收益会在网页、数据库或机器人环境中保持，也不能等同于长期学习 |
| 多轨迹的价值来自继承和组合，而不只是更多样本 | 去掉 Revision 或 Recombination 均降低 Pass@1；case study 显示不同轨迹分别发现文件、测试与根因信息 | w/o Revision、w/o Recombination、w/o All | 支持轨迹之间的信息传递是完整系统的重要组成 | 消融仍包含多次 LLM 调用，不能精确分离重组质量与额外计算预算 |
| 方法在不同模型家族上保持一致收益 | DeepSeek、Qwen、Llama、GPT-4o、Claude-3.7 五个模型上均高于两类 baseline | 每个模型对应的 SWE-Agent / SWE-Search | 说明 scaffold 不只依赖单一开源或闭源模型 | 所有实验仍共享 SWE-bench Verified 与相似代码工具链，不能视为跨任务类型泛化 |
| 约 10 条候选轨迹已经接近较优性能 | 轨迹数和成本分析显示继续增加候选仍有收益，但边际收益下降；相同成本下优于对照 | 不同候选轨迹数量、SWE-Agent、SWE-Search | 支持方法不只是无限堆采样，轨迹加工提高了搜索效率 | 未给出对所有 API 价格和上下文实现都通用的最优轨迹数 |
| 80.0% resolution 展示更强设置的上限 | Claude-4-Sonnet + 最新 SWE-Agent 对齐设置达到 80.0% | 论文首页的最新组合设置 | 展示框架在更强底座和更新基础设施上的潜力 | 不能和 Table 1 的 Claude-3.7 61.2% 或其他行做严格同设置比较 |

### 我的判断

SE-Agent 的主表跨五个模型都呈现一致方向，说明轨迹级 scaffold 有较强证据。它真正新增的是把完整执行过程作为可修订、可交叉和可筛选的对象，而不是再做一次 best-of-N。

不过，“self-evolution”应理解为当前任务中的搜索过程。论文没有把轨迹沉淀为跨任务经验，也没有更新模型参数；多轨迹 rollout、长上下文读取和 evaluator 仍带来较高成本。

### 其他可能解释

- 初始五种 planning strategy 本身就增加了多样性，部分收益可能不完全来自后续重组。
- TaskCompletion、ReasoningQuality、Efficiency 的权重和 LLM evaluator 会影响候选筛选。
- 真实代码执行环境与 repository setup 的稳定性可能放大或削弱轨迹优化收益。
""".strip()

TOA_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 外部工具应只在 epistemically necessary 时调用 | Internal Task Set、World Task Set 与 Knowledge Boundary 的形式化；将工具决策建模为 internal solvability 的 belief-based classification | “有工具就调用”或只按关键词路由的默认工作流 | 给出一套区分内部可解任务与必须外部交互任务的规范框架 | 尚未给出可靠估计 knowledge boundary 的统一算法或 benchmark |
| 最终正确率不足以评价 Agent 的工具使用质量 | Epistemic effort 分解与四种行为模式：overthinking、overacting、over-delegation、calibrated behavior | 只奖励 final answer / task success 的评测 | 说明相同正确答案可能对应完全不同的能力状态、成本与依赖关系 | 主要是理论论证，尚未用长期对照实验证明该评价会预测真实能力增长 |
| 不必要的外部委托可能抑制内部能力发展 | “闭卷能力”和“开卷完成”分离的论证，以及 capability-conditioned SFT / RL 研究议程 | 对所有模型复用同一工具轨迹的训练范式 | 揭示工具调用示范应随目标模型能力变化，不能假设统一最优轨迹 | 没有直接纵向实验验证 over-delegation 必然导致参数能力退化 |
| Agentic RL 应奖励过程中的 effort allocation | 论文提出对调用时机、停止、真实不确定性减少和冗余调用进行过程奖励 | 只用 outcome reward 的 Tool-use RL | 提供设计 process reward 和工具调用日志的明确维度 | 尚未证明哪种奖励函数最稳定，也没有解决自评 solvability 的校准问题 |

### 我的判断

Theory of Agent 的价值在于提出评测和训练问题，而不是提供已完成的 SOTA 系统。它把“是否调用工具”从流程动作提升为与模型知识边界相关的决策，这对 RAG router、Search Agent 和 Tool-use RL 很有解释力。

最需要保留的边界是：论文中的长期能力发展、over-delegation 伤害和 effort-consistent alignment 仍主要是理论命题。后续必须通过 capability-conditioned 数据、过程日志和纵向训练实验验证。

### 其他可能解释

- 在高风险任务中，即使模型内部可能会做，外部验证仍可能因安全价值而必要。
- Knowledge boundary 会随上下文、记忆、模型版本和工具变化，静态阈值可能快速失效。
- 减少工具调用带来的效率收益，可能与准确率、可审计性和实时性目标发生冲突。
""".strip()

SCA_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| Agent 可以依靠自生成、可验证任务提升自己的工具使用能力 | Self-improvement 中 Llama-3.1-8B 平均 Pass@1 从 12.0 提升到 23.5，Pass@4 从 27.9 提升到 41.3 | 原始 Llama-3.1-8B、PAE 等自动任务生成方法 | 支持无需人工任务标签也能构造有效训练闭环 | 不能证明模型完全自主成长；环境、工具接口和验证逻辑仍由人类提供 |
| 自动生成任务可用于强模型向弱模型蒸馏 | 70B teacher 轨迹训练后，8B-SCA 的 Pass@1 / Pass@4 达到 32.2 / 56.8 | 原始 8B 的 12.0 / 27.9 | 说明 CaT 可作为自动生成的工具使用蒸馏数据 | 这是 teacher-student 设置，不属于纯粹的自我提升，且依赖强模型成本 |
| Code-as-Task 的正例与失败样例能提高验证器质量 | 人工标注分析显示 example solution 减少不可行任务，failure cases 进一步过滤验证器过宽造成的 false positive | 只生成 instruction 或 verification function 的简化任务 | 支持任务生成必须同时验证“正例能过、反例不能过” | 仍无法完全发现语义不完整的 instruction 和 false negative |
| 主动探索环境比只看初始说明更适合部分可观测任务 | Challenger 先调用工具观察环境；在 Retail / Airline 等环境相对 PAE 更有优势 | 根据初始 observation 直接生成任务的 PAE | 支持环境探索有助于生成更具体、可行的任务 | 不能说明该优势适用于完全开放或无状态环境 |
| 任务覆盖度比在少数任务上增加 rollout 更影响 OOD 泛化 | Scaling 分析中，少量任务增加轨迹可改善训练集，但 OOD 测试需要更多任务类型和覆盖 | 固定任务数、增加每任务轨迹数 | 说明自生成训练不能只在少数题上反复采样 | 没有给出自动保证任务多样性和真实需求覆盖的完整方法 |

### 我的判断

SCA 的核心贡献是训练数据管线：主动探索、生成 instruction + verifier + 正反例、自动过滤，再进行 RL 或蒸馏。主结果表明这种数据能显著提升 8B executor，CaT 人工分析也为验证器设计提供了直接证据。

其“自演化”边界也很清楚：任务空间、工具环境和可验证目标仍由人类搭建；提升主要是环境特定技能，尚未证明跨环境形成通用 Agent 能力。

### 其他可能解释

- 12k rollout 和额外训练本身带来较大预算，部分收益可能来自更多交互数据。
- 0/1 verifier 可能鼓励 reward hacking 或只学习通过 checker 的策略。
- PPO / GRPO 能进一步提高结果但训练不稳定，论文报告 GRPO 调参不当时性能可能降到 0。
""".strip()

GODEL_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 自指程序修改能超过固定 hand-designed 与固定 meta-learning Agent | 公平设置中 Gödel-base：DROP 80.9、MGSM 64.2、MMLU 70.9、GPQA 34.9；Meta Agent Search 为 79.4、53.4、69.6、34.6 | Meta Agent Search，以及多种固定 Agent pipeline | 支持允许修改 policy 和更新逻辑能扩大有效 Agent design space | 不能证明所有任务都显著受益；GPQA 提升很小，结果依赖 validation feedback 与基础 LLM |
| 基础动作与错误恢复对递归自改至关重要 | MGSM 消融：完整 64.2，w/o thinking 50.8，w/o error handling 49.4，w/o code running 57.1，w/o LLM calling 60.4 | 去掉各初始 action function 的版本 | 说明规划和容错不是附属功能，而是避免坏 patch 终止递归过程的核心机制 | 不能说明当前 action set 是最小或最优集合 |
| 自我改进不是单调稳定过程 | 100 次 MGSM optimization trials 中 Temporary Drop 92%、Optimization Failure 14%、Accidental Termination 4% | 只报告最终最好结果的评测方式 | 直接展示递归自修改需要回滚、沙箱和版本选择 | 统计来自特定任务与实现，不能估计真实生产系统的安全风险 |
| 无约束环境展示更高潜力 | Gödel-free 达到 DROP 90.5、MGSM 90.6、MMLU 87.9、GPQA 55.7 | Gödel-base 与固定资源 baseline | 展示 Agent 会主动寻求更强模型、工具和算法的开放搜索能力 | 不能作为公平同算力比较；额外模型和资源是性能来源之一 |
| 程序级自修改可以跨方法族 | Game of 24 case study 中从普通 LLM 解法改写为 search algorithm，或加入代码验证和多次尝试 | 只调 Prompt 的局部修改 | 说明搜索空间可以包含算法结构变化，而不只是文本提示变化 | 个案不能证明系统会稳定发现最优算法，也可能过拟合 validation set |

### 我的判断

Gödel Agent 给出了程序级 self-evolution 的可行性证据，并且主动报告 temporary drop 与 failure，使结果比只展示最好版本更可信。公平设置下对 MGSM 的提升最明显，证明该框架在可验证推理任务上具有潜力。

但它仍是 proof-of-concept。Gödel-free 的高分不能与固定资源方法直接比较；长期稳定性、安全权限、跨任务经验积累和 reward hacking 都没有被解决。

### 其他可能解释

- 六个 cycle、每个最多 30 次迭代带来较高搜索预算，部分提升可能来自反复试验。
- GPT-4o 驱动自修改，而测试任务使用较弱模型，改进能力与执行能力并非同一来源。
- Validation utility 可能诱导对特定任务集过拟合，跨分布表现需要独立验证。
""".strip()

SURVEY_EVIDENCE = r"""
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
""".strip()

MLEVOLVE_EVIDENCE = r"""
## 主张—证据—边界

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 长时程图搜索与经验维护能在 MLE-Bench 上产生高质量方案 | 75 个任务中 overall medal rate 65.3±0.8、valid submission 100%、above median 76.0±2.3、gold 34.7 | MLE-Bench leaderboard 上的 proprietary / open-source MLE Agents | 说明系统在真实 Kaggle-style 工程任务上兼顾可运行性与竞争性 | Baseline 多来自不同模型和 24 小时预算，不能视为完全同设置因果比较 |
| Progressive MCGS、Retrospective Memory 和 Adaptive Coding 都有贡献 | MLE-Bench Lite：完整 81.82% medal；去 MCGS / Memory 为 68.18%，去 Adaptive Coding 为 72.73% | 三个组件级消融 | 支持提升不是单一 backbone 或单一模块造成 | Lite 仅 22 个任务，组件之间存在交互，不能精确得到独立贡献之和 |
| 分支内演化、跨分支共享和动态经验对长期搜索重要 | 9 个任务细粒度消融：w/o Evolution medal 33.33%，w/o Cross-branch 55.56%，w/o Knowledge Base 与 w/o Global Memory 均为 44.44%，完整为 66.67% | 去掉具体机制的版本 | 支持图关系和两类 memory 对搜索质量均有影响 | 样本较小，结果可能受任务选择和高预算随机性影响 |
| 框架能迁移到算法发现 | 15 个 AlphaEvolve 数学优化任务中 14 个匹配或超过 AlphaEvolve | AlphaEvolve、AlphaEvolve-v2、SimpleTES、TTT-Discover、OpenEvolve | 提供从 Kaggle pipeline 到可执行算法优化的跨域证据 | 不能说明已经形成通用数学发现能力，任务仍共享“候选—执行—评分”结构 |
| 贡献偏 scaffold 而非单一闭源模型 | Gemini、GPT-5.5、DeepSeek-v4-Pro、Kimi-K2.6 在同一 pipeline 的 8 个任务上均有竞争性结果 | 不同 backbone | 说明系统机制不只绑定单一模型 | 仅 8 个代表任务，且多个模型闭源，预算和版本难完全复现 |

### 我的判断

MLEvolve 的实验证据在工程规模上很强：75 个 MLE-Bench 任务、100% valid submission 和组件消融共同说明它不是只在少数样例上工作。Retrospective Memory 与跨分支图结构也有较明确的消融支持。

解释性能时必须同时写出成本和公平性：每个任务最多 500 expansion、12 小时、H200 GPU；不少 baseline 来自不同模型或 24 小时 leaderboard 设置。它证明了高预算 Agent scaffold 的能力，而不是低成本通用 AutoML 已解决。

### 其他可能解释

- 强闭源 backbone、H200 执行资源和大量代码运行可能贡献了相当部分收益。
- 本地验证指标与 Kaggle medal 阈值之间的相关性会影响搜索方向。
- 图搜索和 memory 的优势可能在短任务或低预算设置下减弱。
""".strip()


def span(text: str, heading: str) -> tuple[int, int]:
    matches = list(H2_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() == heading:
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            return match.start(), end
    raise RuntimeError(f"missing section: {heading}")


def clean(section: str) -> str:
    section = section.strip()
    section = re.sub(r"\n---\s*$", "", section).strip()
    return section


def body(section: str) -> str:
    section = clean(section)
    return section.split("\n", 1)[1].strip() if "\n" in section else ""


def pop_section(text: str, heading: str) -> tuple[str, str]:
    start, end = span(text, heading)
    section = clean(text[start:end])
    remaining = text[:start].rstrip() + "\n\n" + text[end:].lstrip()
    return remaining.rstrip() + "\n", section


def rename(text: str, old: str, new: str) -> str:
    needle = f"## {old}"
    if needle not in text:
        raise RuntimeError(f"missing heading to rename: {old}")
    return text.replace(needle, f"## {new}", 1)


def insert_after(text: str, heading: str, block: str) -> str:
    _, end = span(text, heading)
    return text[:end].rstrip() + "\n\n---\n\n" + block + "\n\n---\n\n" + text[end:].lstrip()


def insert_before_reference(text: str, block: str) -> str:
    refs = [m for m in H2_RE.finditer(text) if "参考资料" in m.group(1)]
    if not refs:
        raise RuntimeError("reference heading not found")
    start = refs[-1].start()
    return text[:start].rstrip() + "\n\n---\n\n" + block + "\n\n---\n\n" + text[start:].lstrip()


def external_from_single(section: str, sub_prefix: str | None = None) -> str:
    lines = section.splitlines()
    lines[0] = "## 论文外部信息"
    text = "\n".join(lines)
    if sub_prefix:
        text = re.sub(rf"(?m)^### {re.escape(sub_prefix)}\d+\s+", "### ", text)
    return text


def external_from_many(sections: list[tuple[str, str]]) -> str:
    parts = ["## 论文外部信息"]
    for label, section in sections:
        parts.extend(["", f"### {label}", "", body(section)])
    return "\n".join(parts).strip()


def merge_summary(text: str, summary_heading: str, target_heading: str) -> str:
    text, summary = pop_section(text, summary_heading)
    start, end = span(text, target_heading)
    target = clean(text[start:end])
    merged = (
        f"## {target_heading}\n\n### 核心理解\n\n{body(summary)}\n\n"
        f"### 进一步总结\n\n{body(target)}"
    )
    return text[:start] + merged + "\n\n" + text[end:].lstrip()


def update_date(text: str) -> str:
    comment_end = text.find("-->")
    head, tail = text[:comment_end], text[comment_end:]
    head, count = re.subn(r"(?m)^  updated: '[^']*'$", f"  updated: '{UPDATED}'", head, count=1)
    if count != 1:
        raise RuntimeError("metadata updated field not found")
    return head + tail


def finalize(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\n---\n\s*\n---\n", "\n---\n", text)
    return update_date(text).rstrip() + "\n"


def restructure_single(path: Path, *, external_heading: str, evidence_after: str, evidence: str,
                       renames: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    text, external = pop_section(text, external_heading)
    external = external_from_single(external, "1.")
    for old, new in renames.items():
        text = rename(text, old, new)
    text = insert_after(text, evidence_after, evidence)
    text = insert_before_reference(text, external)
    path.write_text(finalize(text), encoding="utf-8")


def restructure_multi(path: Path, *, headings: list[tuple[str, str]], evidence_after: str,
                      evidence: str, renames: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    collected: list[tuple[str, str]] = []
    for heading, label in headings:
        text, section = pop_section(text, heading)
        collected.append((label, section))
    for old, new in renames.items():
        text = rename(text, old, new)
    text = insert_after(text, evidence_after, evidence)
    text = insert_before_reference(text, external_from_many(collected))
    path.write_text(finalize(text), encoding="utf-8")


def main() -> None:
    remaining = [path for path in NOTES.glob("*.md") if "## 主张—证据—边界" not in path.read_text(encoding="utf-8")]
    expected = {
        "harness-updating-is-not-harness-benefit.md",
        "from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md",
        "se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md",
        "position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md",
        "self-challenging-language-model-agents.md",
        "godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md",
        "from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md",
        "mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md",
    }
    if {p.name for p in remaining} != expected:
        raise RuntimeError(f"remaining note set mismatch: {[p.name for p in remaining]}")

    restructure_single(
        NOTES / "harness-updating-is-not-harness-benefit.md",
        external_heading="1. 论文外部信息",
        evidence_after="5. 主要实验结论",
        evidence=HARNESS_EVIDENCE,
        renames={"2. 研究背景": "问题背景：为什么要解耦写更新与用更新"},
    )
    restructure_single(
        NOTES / "from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md",
        external_heading="1. 论文外部信息",
        evidence_after="6. 主要实验结论",
        evidence=MEMOPILOT_EVIDENCE,
        renames={
            "2. 研究方向与论文定位": "与相邻路线的关系",
            "3. 核心问题": "问题背景：从完整历史到可训练 Memory Policy",
        },
    )
    restructure_multi(
        NOTES / "se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md",
        headings=[
            ("1. 基本信息", "基本信息与资源"),
            ("2. 投稿 / 发表状态", "投稿与发表状态"),
            ("3. 作者与机构", "作者与机构"),
            ("4. 作者背景和研究圈子", "作者背景和研究圈子"),
        ],
        evidence_after="9. 主要实验结果",
        evidence=SE_AGENT_EVIDENCE,
        renames={
            "5. 所属研究方向与论文定位": "与相邻路线的关系",
            "6. 核心问题": "问题背景：独立轨迹无法共享信息",
        },
    )
    restructure_multi(
        NOTES / "position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md",
        headings=[
            ("1. 基本信息", "基本信息与资源"),
            ("2. 投稿 / 发表状态", "投稿与发表状态"),
            ("3. 作者与机构", "作者与机构"),
            ("4. 作者背景和研究圈子", "作者背景和研究圈子"),
        ],
        evidence_after="9. 主要结论",
        evidence=TOA_EVIDENCE,
        renames={
            "5. 所属研究方向与论文定位": "研究坐标与相邻路线",
            "6. 核心问题": "问题背景：Overthinking、Overacting 与 Over-delegation",
        },
    )
    restructure_multi(
        NOTES / "self-challenging-language-model-agents.md",
        headings=[
            ("1. 基本信息", "基本信息与资源"),
            ("2. 投稿 / 发表状态", "投稿与发表状态"),
            ("3. 作者与机构", "作者与机构"),
            ("4. 作者背景和研究圈子", "作者背景和研究圈子"),
        ],
        evidence_after="9. 主要结论",
        evidence=SCA_EVIDENCE,
        renames={
            "5. 所属研究方向与论文定位": "与相邻路线的关系",
            "6. 核心问题": "问题背景：任务、验证器与奖励稀缺",
        },
    )
    restructure_multi(
        NOTES / "godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md",
        headings=[
            ("1. 基本信息", "基本信息与资源"),
            ("2. 投稿 / 发表状态", "投稿与发表状态"),
            ("3. 作者与机构", "作者与机构"),
            ("4. 作者背景和研究圈子", "作者背景和研究圈子"),
        ],
        evidence_after="9. 主要结果",
        evidence=GODEL_EVIDENCE,
        renames={
            "5. 所属研究方向与论文定位": "与相邻路线的关系",
            "6. 核心问题": "问题背景：固定 Agent Design Space 的限制",
        },
    )

    survey = NOTES / "from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md"
    text = survey.read_text(encoding="utf-8")
    text = merge_summary(text, "1. 一句话总结", "14. 我的理解与总结")
    text, external = pop_section(text, "2. 论文外部信息")
    external = external_from_single(external, "2.")
    text = rename(text, "3. 所属研究方向与论文定位", "与相邻路线的关系")
    text = rename(text, "4. 核心问题", "三个分类问题")
    text = insert_after(text, "12. 局限性", SURVEY_EVIDENCE)
    text = insert_before_reference(text, external)
    survey.write_text(finalize(text), encoding="utf-8")

    restructure_multi(
        NOTES / "mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md",
        headings=[
            ("1. 基本信息", "基本信息与资源"),
            ("2. 投稿 / 发布状态", "投稿与发布状态"),
            ("3. 作者与机构", "作者与机构"),
            ("4. 作者背景和研究圈子", "作者背景和研究圈子"),
        ],
        evidence_after="9. 主要实验结果",
        evidence=MLEVOLVE_EVIDENCE,
        renames={
            "5. 研究方向与论文定位": "与相邻路线的关系",
            "6. 核心问题": "问题背景：分支隔离、经验缺失与代码重写",
        },
    )

    print("Restructured 8 remaining notes with evidence layers and external-info ordering")


if __name__ == "__main__":
    main()
