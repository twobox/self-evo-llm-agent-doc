# Self-Evolving LLM Agent 论文笔记

这个仓库用于整理 **Self-Evolving LLM Agent** 相关论文的中文读书笔记，重点关注 LLM Agent 的自我演化、经验学习、Harness Engineering、Agent Memory、Context Engineering、Tool-use Agent、RL for Agent、Tool-use Agent 理论与工具调用校准等方向。

仓库定位：

- `README.md` 只作为仓库首页和笔记索引，不放单篇论文的完整读书笔记。
- 单篇笔记统一放在 `notes/` 目录下。
- 横向综述和跨论文对比统一放在 `surveys/` 目录下。
- 笔记文件名使用英文短横线命名，并尽量和论文标题保持一致。
- 每篇笔记尽量覆盖论文外部信息、作者圈子、方法内容、实验结论、工程启发、局限性和个人理解。

<!-- BEGIN GENERATED NOTE INDEX -->
## 笔记目录

| 序号 | 论文 | 笔记 | 类型 | 进化 / 分析对象 | 学习阶段 | 参数更新 | 跨任务 | Venue / 状态 |
|---:|---|---|---|---|---|---|---|---|
| 1 | Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models | [notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md](notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | system | Context / Playbook | 混合 | 否 | 是 | ICLR 2026 · Poster |
| 2 | EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle | [notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md](notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | method | Experience Base / Executor Policy | 混合 | 是 | 是 | ICML 2026 · accepted |
| 3 | From Player to Master: Enhancing Test-Time Learning of LLM Agents via Reinforcement Learning over Memory | [notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md](notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | method | Memory Update Policy / External Memory | 混合 | 仅辅助模块 | 是 | ICML 2026 · accepted |
| 4 | From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms | [notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md](notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | survey | Agent Memory Taxonomy | 不适用 | 不适用 | 不适用 | ACL 2026 · Findings · accepted |
| 5 | Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents | [notes/harness-updating-is-not-harness-benefit.md](notes/harness-updating-is-not-harness-benefit.md) | diagnostic | Harness Updating / Harness Benefit | 不适用 | 否 | 是 | arXiv · preprint |
| 6 | MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery | [notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md](notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | system | Solution Graph / Retrospective Memory | 测试时 | 否 | 否 | arXiv · preprint |
| 7 | Position: Agents Should Invoke External Tools ONLY When Epistemically Necessary | [notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md](notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | position | Tool-use Decision Boundary | 不适用 | 不适用 | 不适用 | ICML 2026 · Position Paper · accepted |
| 8 | Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement | [notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md](notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | method | Agent Code / Self-Improvement Loop | 测试时 | 否 | 否 | ACL 2025 · Long Paper |
| 9 | SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents | [notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md](notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | method | Trajectory Pool | 测试时 | 否 | 否 | NeurIPS 2025 · Poster |
| 10 | Self-Challenging Language Model Agents | [notes/self-challenging-language-model-agents.md](notes/self-challenging-language-model-agents.md) | method | Synthetic Tasks / Executor Policy | 训练时 | 是 | 是 | NeurIPS 2025 · Poster |

## 相关基础与边界研究

| 序号 | 论文 | 笔记 | 类型 | 进化 / 分析对象 | 学习阶段 | 参数更新 | 跨任务 | Venue / 状态 |
|---:|---|---|---|---|---|---|---|---|
| 1 | On the Limits of LLM Adaptability: Impact of Model-Internalized Priors on Annotation Task Performance | [notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md](notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | diagnostic | Model Priors / Prompt Adaptability | 不适用 | 不适用 | 不适用 | ICML 2026 · Oral & Spotlight |
<!-- END GENERATED NOTE INDEX -->

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
