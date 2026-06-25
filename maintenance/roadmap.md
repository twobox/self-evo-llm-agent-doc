# Repository Maintenance Roadmap

> 本文件是跨会话项目状态入口。聊天记录可能丢失，但这里必须持续保持最新。

## 当前稳定里程碑

### Systematic Note Management Foundation

- 合并 PR：[#12](https://github.com/twobox/self-evo-llm-agent-doc/pull/12)
- `main` 提交：`eebf9145a45d6e60352f583abc734ed5e2d56e07`
- 完成日期：2026-06-25

完成能力：metadata schema、笔记结构、README 生成、严格校验、图片治理、11 篇笔记迁移和横向实验对比。

### Persistent Note Maintenance Workflow

- 合并 PR：[#14](https://github.com/twobox/self-evo-llm-agent-doc/pull/14)
- `main` 提交：`e12d9f7969c56781be4349c2cc33b4f710b3b9b3`
- 完成日期：2026-06-25

完成能力：`AGENTS.md`、跨会话 roadmap、新笔记工作流、Note Maintainer Skill、脚手架、Issue / PR 模板和专用 CI。

### Research Gap Map

- 完成 PR：[#15](https://github.com/twobox/self-evo-llm-agent-doc/pull/15)
- 持久化 Issue：[#13](https://github.com/twobox/self-evo-llm-agent-doc/issues/13)
- 完成日期：2026-06-25

完成能力：

- 覆盖全部 11 篇笔记的证据地图；
- 截至 2026-06 的外部补充检索；
- 7 类研究 gap；
- 4 个候选小课题；
- 对失败经验、大小模型协同、长期遗忘和 Harness 修复的新颖性判断进行收窄；
- research gap map 自动回归测试。

## 当前活动阶段

暂无正在执行的阶段。

仓库当前处于可稳定维护状态。新任务开始时，应先创建或选择 GitHub Issue，再在本节登记 active stage、分支和 PR。

## 下一阶段

### Stage 12：新论文接入演练

状态：`planned`

目标：使用一篇新论文完整演练持续维护流程：

```text
输入论文链接
→ scaffold
→ 外部事实核验
→ 单篇笔记
→ 图片治理
→ README
→ experimental comparison
→ CI
→ Draft PR
```

目的不是增加数量，而是验证维护系统能否在新会话中独立运行。

启动方式：收到下一篇新论文后创建对应 Issue，并将本阶段切换为 `in progress`。

## 后续候选阶段

### Stage 13：长期质量治理

候选工作：

- 外部链接定期复核；
- venue / code / model 状态更新；
- `related_notes` 关系图；
- 重复段落和编号统一；
- 已过期经验与横向数据版本管理；
- 成本字段进一步结构化。

## 决策记录

| 日期 | 决策 | 原因 |
|---|---|---|
| 2026-06-25 | 将堆叠 PR 收口为单一 squash 里程碑 | 修复已达到稳定阶段，继续堆叠会增加 base 管理和重复 CI 成本 |
| 2026-06-25 | 聊天用于执行，仓库用于记忆 | 项目状态、验收条件和研究计划不能依赖会话记忆 |
| 2026-06-25 | 先完成持续维护入口，再开始 Research Gap Map | 确保下一阶段可跨会话恢复，并能作为后续维护的正式流程 |
| 2026-06-25 | 新笔记必须更新横向数据和图片清单 | 防止单篇笔记、README、综述和资源状态再次漂移 |
| 2026-06-25 | Research Gap 必须结合最新外部工作收窄 | “已有论文没做”不自动等于当前仍有新颖性 |
| 2026-06-25 | 优先研究固定预算下的失败经验效用 | 它连接失败归因、memory、Harness Benefit、rescue 和成本，且适合 1–2 个月最小实验 |

## 新会话恢复步骤

1. 读取 `AGENTS.md`；
2. 读取本文件；
3. 检查“当前活动阶段”；
4. 如果没有活动阶段，根据用户任务创建或选择 Issue；
5. 读取 `docs/new-note-workflow.md` 和 `skills/note-maintainer/SKILL.md`；
6. 检查最新 `main` 与 open PR；
7. 将新阶段、分支和 PR 写回本文件。

## 更新规则

以下事件发生时必须更新本文件：

- 阶段开始、暂停、完成或取消；
- 稳定里程碑合并；
- active Issue / PR 改变；
- 维护规则或验收条件改变；
- 下一阶段优先级改变。
