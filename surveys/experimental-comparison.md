<!--
metadata:
  title: 'Self-Evolving LLM Agent 实验设置横向对比'
  short_title: '实验设置横向对比'
  note_type: '横向综述 / 对比笔记'
  status: '持续维护'
  scope: '仓库内 11 篇笔记的进化对象、实验设计、主要结果、成本与证据边界'
  created: '2026-06-06'
  updated: '2026-06-25'
-->

# Self-Evolving LLM Agent 实验设置横向对比

本文档覆盖仓库当前全部 **11 篇笔记**，用于比较进化对象、学习阶段、参数更新、跨任务能力、实验环境、代表结果、成本、复现条件和证据边界。

> **阅读原则：** 不同论文的 benchmark 数字不可直接横向排名。优先比较实验设计、同设置 baseline、消融、预算和“不能证明什么”。

数据源：[`experimental-comparison-data.json`](experimental-comparison-data.json)。本文档由 `scripts/generate_experimental_comparison.py` 确定性生成。

---

## 1. 研究定位总表

| 论文 | 类型 | Agent / 任务 | 进化或分析对象 | 学习阶段 | 参数更新 | 跨任务 | 核心机制 |
|---|---|---|---|---|---|---|---|
| [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 系统 | Context Engineering / Tool-use Agent | Context / Playbook | 混合 | 否 | 是 | Generator / Reflector / Curator；delta context update；offline / online adaptation |
| [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 方法 | Search / QA Agent | Experience Base / Executor Policy | 混合 | 是 | 是 | 轨迹经验自蒸馏、经验库检索与治理、SFT / LoRA、GRPO |
| [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 诊断 | Harness / Memory / Skill Diagnostic | Harness Updating / Harness Benefit | 不适用 | 否 | 是 | 固定 Task-Solver 替换 Evolver，或固定 Evolver 替换 Task-Solver的交叉实验 |
| [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 立场 / 理论 | Tool-use Calibration / Theory | Tool-use Decision Boundary | 不适用 | 不适用 | 不适用 | Internal Task Set、World Task Set、Knowledge Boundary、Epistemic Effort |
| [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 方法 | Code Agent / Test-Time Search | Trajectory Pool | 测试时 | 否 | 否 | 多策略轨迹池；Revision、Recombination、Refinement |
| [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 方法 | Tool-use / Synthetic-task Agent | Synthetic Tasks / Executor Policy | 训练时 | 是 | 是 | Challenger 主动探索；Code-as-Task；自动 verifier；RL / distillation |
| [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 方法 | Self-Referential / Program-level Agent | Agent Code / Self-Improvement Loop | 测试时 | 否 | 否 | Self-inspection、动态代码修改、monkey patching、递归评估与继续改进 |
| [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 综述 | Memory Survey / Taxonomy | Agent Memory Taxonomy | 不适用 | 不适用 | 不适用 | 文献分类、机制归纳和 benchmark / resource collection |
| [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 方法 | Frozen Player + Trainable Memory Updater | Memory Update Policy / External Memory | 混合 | 仅辅助模块 | 是 | Multi-turn GRPO、turn-wise one-step reward、3-tier adaptive memory |
| [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 系统 | MLE / Algorithm Discovery Agent | Solution Graph / Retrospective Memory | 测试时 | 否 | 否 | Progressive MCGS、Retrospective Memory、Planner-Coder、Base / Stepwise / Diff coding |
| [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 诊断 | Model Capability Boundary Diagnostic | Model Priors / Prompt Adaptability | 不适用 | 不适用 | 不适用 | Definition-Specific Familiarity、rescue rate、decision stickiness、misaligned definition |

---

## 2. 主实验与证据边界

> 不同论文的任务、模型、预算和指标并不一致。下表用于比较证据结构，不用于把不同 benchmark 的数字直接排名。

| 论文 | 证据类型 | 数据集 / 环境 | 最强对照 | 代表结果 | 证据强度 | 不能直接推出什么 |
|---|---|---|---|---|---|---|
| [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 系统实证 | AppWorld；FiNER；Formula / XBRL | Dynamic Cheatsheet、GEPA、ICL、Base ReAct | AppWorld：ReAct 42.4，ACE offline 59.4，ACE online 59.5；无 GT 的 AppWorld online 仍为 59.5。 | 较强：跨 AppWorld 与金融任务，含无标签反馈和成本分析。 | 不能证明所有长期开放环境都能稳定维护 playbook；FiNER online 无 GT 从 70.7 降到 67.3，说明错误反馈会污染上下文。 |
| [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 方法实证 | Natural Questions；HotpotQA；TriviaQA；PopQA；2WikiMultiHopQA；MuSiQue；Bamboogle | Search-R1-instruct、R1、IRCoT、RAG、Search-o1 | Qwen2.5-3B 平均 EM 0.382，对比 Search-R1-instruct 0.325；7B 为 0.417，对照 0.385。 | 较强：主结果、经验检索消融、RL 互补性和经验质量分析形成完整证据链。 | 实验集中于搜索问答；跨域测试仍共享问答与搜索结构，不能直接代表代码、GUI 或开放 Agent 泛化。 |
| [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 受控诊断 | SWE-bench Verified；MCP-Atlas；SkillsBench | 不同能力等级的 Evolver 与 Task-Solver 交叉组合 | Harness Updating 随 Evolver 能力提升较平坦；Harness Benefit 对 Task-Solver 能力呈非单调关系，并观察到 activation / adherence failure。 | 较强诊断证据：实验设计直接拆分写更新与用更新。 | 结论限定于冻结参数和外部 harness；不能推导 Evolver 永远不是瓶颈，也不能覆盖参数级持续学习。 |
| [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 理论论证 | — | 只按最终正确率或默认有工具就调用的评测范式 | 无新增传统 benchmark；核心贡献是区分 overthinking、overacting、over-delegation 与 calibrated behavior。 | 理论 / 规范性证据，而非 SOTA 实证。 | Knowledge boundary 的估计、长期能力退化和 capability-conditioned RL 仍是待验证研究命题。 |
| [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 方法实证 | SWE-bench Verified | SWE-Search、SWE-Agent | DeepSeek-V3：54.8% vs SWE-Search 39.4%；Claude-3.7：61.2% vs 47.4%。 | 较强：五个模型方向一致，含 Revision / Recombination 消融和成本分析。 | 只在 SWE-bench Verified 验证；属于单任务测试时搜索，不产生跨任务记忆或模型参数更新。 |
| [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 方法实证 | M3ToolEval Calculation；M3ToolEval Web Browsing；TauBench Retail；TauBench Airline | 原始 Llama-3.1-8B、PAE、DPO / PPO / GRPO 消融 | 8B self-improvement：Pass@1 从 12.0 提升到 23.5；70B teacher 蒸馏后为 32.2。 | 中强：主结果、任务质量人工分析和训练算法消融。 | 环境、工具接口和 verifier 仍由人类设计；自动任务不等于开放世界自主成长，0/1 verifier 可能诱发 reward hacking。 |
| [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 方法实证 | DROP；MGSM；MMLU；GPQA；Game of 24 | Meta Agent Search、CoT-SC、Self-Refine、LLM Debate | Gödel-base：DROP 80.9、MGSM 64.2、MMLU 70.9、GPQA 34.9；Meta Agent Search 为 79.4、53.4、69.6、34.6。 | 中强：多 benchmark、动作消融和自修改失败统计。 | Gödel-free 使用额外强模型 / 工具，不能做同资源比较；validation utility 可能导致过拟合，长期安全未解决。 |
| [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 综述 / 分类 | — | 只按数据结构或检索方式分类的 memory taxonomy | 无新增主实验；提出 Storage → Reflection → Experience，并区分 global repository 与时刻 t 的 retrieved memory。 | 文献覆盖与概念整合证据，不是统一 benchmark 实证。 | 三个阶段可能是并行模块而非线性演化；Experience 定义存在方法间重叠。 |
| [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 方法实证 | TextArena RPS；RLCard LHE；StreamBench CoSQL；StreamBench DS-1000 | No Memory、Full History、Human Counter-Strategy、prompt-based memory updater | Qwen2.5-14B Player：RPS@5 / LHE@5 = 3.28 / 2.03；No Memory = 0.43 / -1.36。 | 较强：主结果、结构消融、奖励消融、跨 Player 与 StreamBench 迁移。 | 依赖可计算奖励和可重复交互；对手切换越频繁性能越低，StreamBench held-out episodes 数量有限。 |
| [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 系统实证 | MLE-Bench 75 tasks；AlphaEvolve 15 optimization tasks | AIDE、ML-Master、AIRA-Dojo、MARS+、AlphaEvolve | MLE-Bench：overall medal 65.3±0.8%，valid submission 100%，above median 76.0±2.3%；15 个算法任务中 14 个匹配或超过 AlphaEvolve。 | 较强工程证据：75 个任务、组件消融与算法发现迁移。 | baseline 使用不同模型或 24h 设置，不能做严格同预算比较；结果证明高预算 scaffold 能力，不代表低成本 AutoML 已解决。 |
| [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 实证诊断 | multiple toxicity / hate-speech annotation datasets | ROUGE-L、BERTScore、embedding cosine 等文本熟悉度指标；多种 prompt / definition / few-shot 设置 | 控制 dataset-level confounds 后 DSF 与性能 partial r = +0.41；zero-shot 错误总体 rescue rate 仅 34.8%。 | 中强诊断证据：相关分析、错误级 rescue 分析和错误定义实验互相补充。 | 相关性不等于因果；社会概念标注任务可能放大定义冲突，不能直接推广到代码、数学或所有 Agent memory 场景。 |

---

## 3. 成本与复现条件

| 论文 | 训练 / 推理成本特征 | 复现条件 | 复现难度判断 |
|---|---|---|---|
| [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 不训练参数，但需要多角色 LLM 调用；论文报告相对 GEPA / Dynamic Cheatsheet 的 latency、rollout 和 token 成本优势。 | 官方代码与项目资源公开；基础模型和部分服务成本仍依赖 API / 推理环境。 | 中 |
| [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 高：需要轨迹生成、经验抽取、向量检索、SFT 与 GRPO；论文未给统一 wall-clock / token 总成本。 | 官方代码、模型与数据资源公开；完整复现仍需要训练 GPU、检索服务和 RL rollout。 | 高 |
| [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 中高：需要多模型、多 benchmark 的交叉组合；没有统一训练成本，但推理实验规模较大。 | 官方代码公开；完整结果依赖多种闭源 / 开源模型和 benchmark 环境。 | 高 |
| [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 不适用：position paper 未训练新系统。 | 概念与形式化定义可复核；缺少统一实现、数据集和 process reward 实验。 | 无系统复现 / 概念复核 |
| [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 高推理成本：多候选轨迹、长上下文与 evaluator；约 10 条候选后边际收益下降。 | 官方代码公开并基于 SWE-Agent；环境安装、模型 API 和多轨迹预算仍较重。 | 高 |
| [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 高：约 12k rollout、自动任务生成、验证和后续 SFT / RL；在线 RL 稳定性敏感。 | 实验结构清晰，但当前笔记未确认完整官方代码发布；复现依赖多环境和训练资源。 | 高 |
| [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 高：6 个 cycle、每 cycle 最多 30 次迭代；需要代码执行、validation 与 LLM 调用。 | 官方 MIT 代码公开；依赖 OpenAI API、任务环境和验证集。 | 高 |
| [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 不适用：综述不训练新系统。 | 官方资源列表公开；分类可复核，但文献覆盖会随时间变化。 | 无系统复现 / 概念复核 |
| [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 中高：冻结 Player，但需训练 memory updater 并执行多轮 rollout；memory budget 512 tokens。 | 论文称代码公开，但当前笔记仍缺明确仓库链接；博弈环境易复现，完整训练流程待核验。 | 高 |
| [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 很高：每任务最多 12 小时、500 expansion、H200 GPU，并包含大量代码执行与评估。 | 官方 MIT 代码公开；闭源 backbone、H200 环境和长预算使完整复现成本高。 | 高 |
| [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 中：主要是多模型、多 prompt 条件的推理与统计分析，不涉及参数训练。 | 实验定义和统计方法清晰；结果依赖具体模型版本、数据集与 confidence 获取方式。 | 中 |

---

## 4. Benchmark / 环境索引

| Benchmark / 环境 | 出现论文 | 主要任务类型 |
|---|---|---|
| 2WikiMultiHopQA | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| AlphaEvolve 15 optimization tasks | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | Kaggle-style 机器学习工程与数学算法优化 |
| AppWorld | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | API 工具调用、金融抽取与公式计算 |
| Bamboogle | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| DROP | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 阅读理解、数学、多领域知识、科学问答和 Game of 24 |
| FiNER | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | API 工具调用、金融抽取与公式计算 |
| Formula / XBRL | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | API 工具调用、金融抽取与公式计算 |
| Game of 24 | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 阅读理解、数学、多领域知识、科学问答和 Game of 24 |
| GPQA | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 阅读理解、数学、多领域知识、科学问答和 Game of 24 |
| HotpotQA | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| M3ToolEval Calculation | [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 计算、网页浏览、零售和航空工具环境 |
| M3ToolEval Web Browsing | [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 计算、网页浏览、零售和航空工具环境 |
| MCP-Atlas | [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 代码修复、MCP 工具调用、Skill 使用 |
| MGSM | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 阅读理解、数学、多领域知识、科学问答和 Game of 24 |
| MLE-Bench 75 tasks | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | Kaggle-style 机器学习工程与数学算法优化 |
| MMLU | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 阅读理解、数学、多领域知识、科学问答和 Game of 24 |
| multiple toxicity / hate-speech annotation datasets | [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | Toxicity / hate-speech annotation under changing definitions and prompts |
| MuSiQue | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| Natural Questions | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| PopQA | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| RLCard LHE | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 连续博弈与流式数据库 / 代码任务 |
| SkillsBench | [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 代码修复、MCP 工具调用、Skill 使用 |
| StreamBench CoSQL | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 连续博弈与流式数据库 / 代码任务 |
| StreamBench DS-1000 | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 连续博弈与流式数据库 / 代码任务 |
| SWE-bench Verified | [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md)、[SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 代码修复、MCP 工具调用、Skill 使用；真实 GitHub issue 修复、代码定位、编辑和测试 |
| TauBench Airline | [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 计算、网页浏览、零售和航空工具环境 |
| TauBench Retail | [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 计算、网页浏览、零售和航空工具环境 |
| TextArena RPS | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 连续博弈与流式数据库 / 代码任务 |
| TriviaQA | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 开放域与多跳问答、搜索增强推理 |
| 无新增 benchmark | Theory of Agent、From Storage to Experience | 理论框架与综述分类 |

---

## 5. 指标索引

| 指标 | 出现论文 | 应如何理解 |
|---|---|---|
| 95% bootstrap CI | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Above Median Rate | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 超过 Kaggle 人类中位数的任务比例。 |
| Accuracy | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md)、[Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 分类、抽取、公式计算或推理正确率。 |
| Accuracy / annotation performance | [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Beat Ratio | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 超过的人类参赛者比例。 |
| benchmark score | [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| confidence | [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 模型自报或生成的置信度；不等同于严格校准概率。 |
| effort allocation | [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Elo | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 相对对战强度评分。 |
| Exact Match | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 答案标准化后完全匹配，适合开放域 / 多跳问答。 |
| experience generalization | [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| F Score | [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 允许部分匹配，用于补充问答表现。 |
| F1 | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 允许部分匹配；Gödel Agent 在 DROP 使用。 |
| Gold Medal Rate | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 达到 gold medal 阈值的任务比例。 |
| Harness Activation | [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 是否检索并加载相关 harness。 |
| Harness Adherence | [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 加载后是否持续遵循 harness。 |
| latency | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 适配或运行耗时。 |
| LHE@k | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | Leduc Hold'em 连续对局表现。 |
| lifecycle robustness | [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Medal Rate | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | MLE-Bench 达到 medal 阈值的任务比例。 |
| memory retrieval | [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| memory utility | [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Optimization Failure | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 自修改未能超过初始策略。 |
| partial correlation | [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 控制数据集层混杂因素后的相关性。 |
| Pass@1 | [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md)、[Self-Challenging](../notes/self-challenging-language-model-agents.md) | 单次采样成功率；代码修复中也对应 resolution rate。 |
| Pass@4 | [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 四次采样至少一次成功。 |
| Pass@5 | [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 五次候选至少一次成功，反映有限预算搜索。 |
| process calibration | [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| rescue rate | [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | 原 zero-shot 错误被后续提示纠正的比例。 |
| resolution rate | [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 真实 issue 被正确修复的比例。 |
| rollouts | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 获取更新或训练信号所需交互次数。 |
| RPS@k | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 连续石头剪刀布任务的 k 轮表现。 |
| SGC | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | AppWorld 的 Scenario Goal Completion。 |
| StreamBench pass@4 accuracy | [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Temporary Drop | [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 自修改过程中性能短暂下降。 |
| TGC | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | AppWorld 的 Task Goal Completion。 |
| token cost | [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 模型调用 token 消耗。 |
| tool-use necessity | [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| trajectory score | [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 论文特定指标；解释时需回到对应任务和评测协议。 |
| Valid Submission Rate | [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 提交文件可运行且满足格式要求的比例。 |

---

## 6. 横向结论

### 6.1 进化对象至少分为五层

1. **外部上下文 / 经验资产**：ACE、EvolveR、MemoPilot。
2. **当前任务轨迹或候选解**：SE-Agent、MLEvolve。
3. **模型参数或辅助策略参数**：EvolveR、Self-Challenging、MemoPilot 的 updater。
4. **Agent 可执行程序**：Gödel Agent。
5. **能力边界与评价框架**：Harness Updating、Theory of Agent、On the Limits、Memory Survey。

因此，论文都使用 self-evolving / self-improving 术语，并不表示它们在更新同一种东西。

### 6.2 测试时优化不等于长期学习

SE-Agent、Gödel Agent 和 MLEvolve 都能在当前任务中持续产生更好候选，但 metadata 中均不把它们标记为跨任务长期记忆。判断“是否学习”时，应同时检查：结果是否跨任务保留、是否修改参数、是否有持久经验库。

### 6.3 外部经验存在四个独立环节

```text
生成 / 写入 → 检索 / 激活 → 遵循 / 执行 → 产生真实收益
```

ACE 和 EvolveR 重点研究生成与治理；Harness Updating 强调激活和遵循；MemoPilot 直接优化 frozen Player 可执行的 memory。只报告“写出了经验”不足以证明 Harness Benefit。

### 6.4 主结果必须和预算一起阅读

MLEvolve 的 12 小时 / 500 expansion / H200、Self-Challenging 的约 12k rollout、SE-Agent 的多轨迹池，以及 EvolveR 的 SFT + GRPO 都说明：更高结果往往来自更复杂的系统与更高预算。横向比较应优先寻找同模型、同环境、同 rollout 或同 wall-clock 的对照。

### 6.5 诊断论文提供了比平均分更细的研究变量

- Harness Updating：activation 与 adherence；
- On the Limits：DSF、rescue rate 与 decision stickiness；
- Theory of Agent：tool-use necessity 与 effort allocation；
- Memory Survey：repository、retrieval、utility 与 lifecycle。

这些变量可用于设计后续 Self-Evolving Agent 实验，而不只是在 benchmark 上再提高一个平均分。

---

## 7. 当前实验缺口

| 缺口 | 当前表现 | 更理想的实验 |
|---|---|---|
| 成本不可比 | 论文常只报告分数，训练、rollout、token、wall-clock 和硬件口径不统一 | 同模型、同工具、同 wall-clock / token / rollout 预算的 Pareto 曲线 |
| 跨任务持久性不足 | 多数方法只在当前任务或同构任务流中复用经验 | 明确 train task、adapt task、held-out task 和长期 retention test |
| 写入与使用混淆 | Memory / skill 写得更好，不代表 solver 会检索和遵循 | 分别记录 write quality、retrieval、activation、adherence 和 downstream benefit |
| 失败经验治理不足 | 多数系统展示新增经验，较少系统研究删除、过期、冲突和污染 | 长期任务流中的去重、遗忘、版本回滚与错误经验注入实验 |
| 参数与外挂经验难分 | 同时使用经验库、SFT 和 RL 时，收益来源容易混合 | Experience-only、parameter-only、combined 和 equal-budget 消融 |
| 评价过度依赖最终成功 | 最终答对可能掩盖无必要工具调用、过度搜索或偶然成功 | 过程级 reward、必要性、校准、执行成本和可审计轨迹指标 |
| 开放环境证据有限 | 许多结果来自 QA、博弈、代码或 Kaggle 等结构化环境 | Web / Office / GUI / 数据库等跨动作空间、跨分布长期任务 |

---

## 8. 维护规则

新增或更新论文时：

1. 先更新对应单篇笔记及 metadata；
2. 在 `experimental-comparison-data.json` 中新增或修改记录；
3. 主结果必须同时写最强对照、成本条件和证据边界；
4. Position / Survey 不得伪装成传统 SOTA 实验；
5. 运行：

```bash
python scripts/generate_experimental_comparison.py --check
python -m unittest discover -s tests -v
```

生成器会检查 11 篇笔记是否全部被覆盖，以及 research-positioning 字段是否与 note metadata 一致。
