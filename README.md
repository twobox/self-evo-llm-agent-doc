# Self-Evolving LLM Agent 论文笔记

这个仓库用于整理 **Self-Evolving LLM Agent** 相关论文的中文读书笔记，重点关注 LLM Agent 的自我演化、经验学习、Harness Engineering、Agent Memory、Context Engineering、Tool-use Agent、RL for Agent、Tool-use Agent 理论与工具调用校准等方向。

仓库定位：

- `README.md` 只作为仓库首页和笔记索引，不放单篇论文的完整读书笔记。
- 单篇笔记统一放在 `notes/` 目录下。
- 横向综述和跨论文对比统一放在 `surveys/` 目录下。
- 笔记文件名使用英文短横线命名，并尽量和论文标题保持一致。
- 每篇笔记尽量覆盖论文外部信息、作者圈子、方法内容、实验结论、工程启发、局限性和个人理解。

## 笔记目录

| 序号 | 论文 | 笔记 | 主题 | 发表时间 |
|---|---|---|---|---|
| 1 | Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models | [notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md](notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | Context Engineering、Self-Improving LLM、Agent Memory、Playbook、Generator / Reflector / Curator、AppWorld、Finance | ICLR 2026 |
| 2 | EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle | [notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md](notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 自演化 Agent、Experience Base、经验自蒸馏、经验检索、GRPO、策略演化 | ICML 2026 |
| 3 | Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents | [notes/harness-updating-is-not-harness-benefit.md](notes/harness-updating-is-not-harness-benefit.md) | 自演化 Agent、Harness Updating、Harness Benefit、Evolver 与 Task-Solver 解耦分析 | arxiv 2025 |
| 4 | Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary | [notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md](notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | Theory of Agent、工具调用校准、Epistemic Necessity、Knowledge Boundary、Overthinking、Overacting、Over-delegation | ICML 2026 · Position Paper |
| 5 | SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents | [notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md](notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | 自演化 Agent、Code Agent、轨迹优化、测试时搜索、Revision、Recombination、Refinement、SWE-bench Verified | NeurIPS 2025 |
| 6 | Self-Challenging Language Model Agents | [notes/self-challenging-language-model-agents.md](notes/self-challenging-language-model-agents.md) | Self-Challenging Agent、Code-as-Task、自生成任务、多轮工具使用、RL for Agent、可验证奖励 | NeurIPS 2025 poster |
| 7 | Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement | [notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md](notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 自指 Agent、递归自我改进、Agent 设计空间搜索、运行时代码自修改、Monkey Patching | ACL 2025 Long Paper |
| 8 | From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms | [notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md](notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | Agent Memory、Storage / Reflection / Experience、轨迹保存、轨迹反思、经验抽象、主动探索、跨轨迹抽象 | ACL 2026 Findings |

## 相关基础与边界研究

| 序号 | 论文 | 笔记 | 主题 | 发表时间 |
|---|---|---|---|---|
| 1 | On the Limits of LLM Adaptability: Impact of Model-Internalized Priors on Annotation Task Performance | [notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md](notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | LLM Adaptability、Model-internalized Priors、Prompt Steerability、LLM-as-Annotator、Decision Stickiness、能力边界 | arXiv 2026 |

## 横向综述与对比

| 文档 | 内容 |
|---|---|
| [surveys/experimental-comparison.md](surveys/experimental-comparison.md) | 汇总已读论文的实验对象、测试数据集、训练方法、对比方法、评价指标和复现信息 |

## 关注主题

- **Self-Evolving LLM Agent**：Agent 如何通过历史任务、反思、经验库或强化学习持续改进。
- **Recursive Self-Improvement / Self-Referential Agent**：Agent 如何读取和修改自身程序逻辑，甚至修改负责自我改进的机制。
- **Context Engineering / Context Adaptation**：如何把 prompt、memory、策略、示例和领域规则维护成可持续演化的上下文资产。
- **Agent Memory / Experience Base**：如何存储、压缩、检索和维护经验。
- **Harness Engineering**：prompt、memory、skill、tool、workflow 等外部组件如何更新，以及模型是否真正受益。
- **Tool-use / Search Agent**：Agent 如何调用外部工具、搜索系统、代码环境或 API 完成复杂任务。
- **Tool-use Calibration / Theory of Agent**：Agent 如何判断外部工具调用是否在知识上必要，避免 overthinking、overacting 和 over-delegation。
- **RL for Agent**：如何用轨迹反馈、奖励设计和强化学习训练 Agent 的工具调用与经验使用能力。
- **Synthetic Task Generation / Verifiable Reward**：Agent 如何自动生成任务、构造验证器，并把任务反馈转化为可训练奖励信号。
- **Trajectory Optimization / Test-Time Search**：Agent 如何在测试时保存、反思、重组和筛选多条执行轨迹，提高复杂任务求解成功率。

## 阅读笔记建议格式

后续新增笔记时，建议包含以下内容：

1. 论文标题、arXiv 地址、PDF 下载地址、代码仓库地址。
2. 投稿/发表状态。
3. 作者与机构。
4. 作者背景和研究圈子。
5. 所属研究方向与论文定位。
6. 核心问题。
7. 方法/实验设计。
8. 主要结论。
9. 工程启发。
10. 局限性。
11. 我的理解与总结。

## 横向对比维护建议

后续每新增一篇论文笔记，建议同步更新 `surveys/experimental-comparison.md`，至少补充：

1. 实验对象 / Agent 类型。
2. 核心任务。
3. 训练数据或更新方式。
4. 测试数据集 / benchmark / 环境。
5. 对比方法和 baseline。
6. 评价指标。
7. 复现信息。