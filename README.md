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
| 9 | From Player to Master: RL over Memory (MemoPilot) | [notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md](notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | Test-Time Learning、Memory RL、Multi-turn GRPO、Agent Memory Update | ICML 2026 |

## 相关基础与边界研究

| 序号 | 论文 | 笔记 | 主题 | 发表时间 |
|---|---|---|---|---|
| 1 | On the Limits of LLM Adaptability: Impact of Model-Internalized Priors on Annotation Task Performance | [notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md](notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | LLM Adaptability、Model-internalized Priors、Prompt Steerability、LLM-as-Annotator、Decision Stickiness、能力边界 | arXiv 2026 |

## 横向综述与对比

| 文档 | 内容 |
|---|---|
| [surveys/experimental-comparison.md](surveys/experimental-comparison.md) | 汇总已读论文的实验对象、测试数据集、训练方法、对比方法、评价指标和复现信息 |

## 关注主题

- **Self-Evolving LLM Agent**
- **Recursive Self-Improvement / Self-Referential Agent**
- **Context Engineering / Context Adaptation**
- **Agent Memory / Experience Base**
- **Harness Engineering**
- **Tool-use / Search Agent**
- **RL for Agent**
- **Synthetic Task Generation / Verifiable Reward**
- **Trajectory Optimization / Test-Time Search**
