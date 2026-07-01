# Terminology Glossary

## context collapse

- 中文：语境坍缩
- 定义：在长上下文、多轮交互或持续累积记忆的设置中，原本应被区分的任务目标、约束、角色信息、历史经验或证据边界，逐渐被压平、混合或弱化，导致模型无法稳定保持正确的问题框架与优先级。
- 表现：早期关键信息被后续内容淹没；不同来源的信息被不加区分地拼接；局部相关内容挤占全局任务目标；模型开始偏离最初约束或误用历史记忆。
- 相关：context engineering、memory management、instruction drift、retrieval noise



## trajectory-level policy

多步轨迹组织能力



## Intra-Trajectory Transformation

对**同一条轨迹内部**做改写/重构，不改变它"是哪条轨迹"，但改变其**表示形式或结构**，例如：

| 变换类型          | 说明                                      |
| ----------------- | ----------------------------------------- |
| **Abstraction**   | 去掉冗余步骤，保留决策关键点              |
| **Reordering**    | 调整内部步骤顺序（逻辑等价）              |
| **Annotation**    | 给各步打标签（success / failure / pivot） |
| **Compaction**    | 压缩重复或低信息量的子步骤                |
| **Format Change** | 原始 log → structured JSON / graph        |
