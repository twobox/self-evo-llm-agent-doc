# Self-Evolving LLM Agent 论文笔记

这个仓库用于整理 **Self-Evolving LLM Agent** 相关论文的中文读书笔记，重点关注 LLM Agent 的自我演化、经验学习、Harness Engineering、Agent Memory、Tool-use Agent、RL for Agent 等方向。

仓库定位：

- `README.md` 只作为仓库首页和笔记索引，不放单篇论文的完整读书笔记。
- 单篇笔记统一放在 `notes/` 目录下。
- 笔记文件名使用英文短横线命名，并尽量和论文标题保持一致。
- 每篇笔记尽量覆盖论文外部信息、作者圈子、方法内容、实验结论、工程启发、局限性和个人理解。

## 笔记目录

| 论文 | 笔记 | 主题 |
|---|---|---|
| EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle | [notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md](notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 自演化 Agent、Experience Base、经验自蒸馏、经验检索、GRPO、策略演化 |
| Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents | [notes/harness-updating-is-not-harness-benefit.md](notes/harness-updating-is-not-harness-benefit.md) | 自演化 Agent、Harness Updating、Harness Benefit、Evolver 与 Task-Solver 解耦分析 |

## 关注主题

- **Self-Evolving LLM Agent**：Agent 如何通过历史任务、反思、经验库或强化学习持续改进。
- **Agent Memory / Experience Base**：如何存储、压缩、检索和维护经验。
- **Harness Engineering**：prompt、memory、skill、tool、workflow 等外部组件如何更新，以及模型是否真正受益。
- **Tool-use / Search Agent**：Agent 如何调用外部工具、搜索系统、代码环境或 API 完成复杂任务。
- **RL for Agent**：如何用轨迹反馈、奖励设计和强化学习训练 Agent 的工具调用与经验使用能力。

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
