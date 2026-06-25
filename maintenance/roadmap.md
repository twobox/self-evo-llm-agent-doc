# Repository Maintenance Roadmap

> 本文件是跨会话项目状态入口。聊天记录可能丢失，但这里必须持续保持最新。

## 当前稳定里程碑

**Systematic Note Management Foundation**

- 合并 PR：[#12](https://github.com/twobox/self-evo-llm-agent-doc/pull/12)
- `main` 里程碑提交：`eebf9145a45d6e60352f583abc734ed5e2d56e07`
- 完成日期：2026-06-25

已具备：

- metadata schema 1.0；
- 单篇笔记模板和写作规范；
- README 自动生成；
- 严格 metadata / 正文结构校验；
- 图片许可、manifest 和完整性治理；
- 11 篇笔记统一快速阅读层与证据层；
- 结构化横向实验对比；
- 单元测试和 GitHub Actions。

## 当前活动阶段

### Stage 10：持续维护入口

状态：`in progress`

分支：`codex/add-note-maintenance-workflow`

活动 PR：[#14](https://github.com/twobox/self-evo-llm-agent-doc/pull/14)

目标：

- 增加 `AGENTS.md` 作为新会话和 Agent 总入口；
- 定义新笔记接入工作流；
- 提供仓库内维护 Skill；
- 增加新笔记脚手架；
- 增加 GitHub Issue / PR 模板；
- 将所有入口纳入测试和 CI。

验收条件：

- 新会话只读取仓库文件即可恢复项目状态；
- 新笔记可以通过脚手架创建，不依赖复制旧聊天提示；
- 工作流明确要求同步 README、横向对比和图片治理；
- CI 会在入口、Skill、模板或脚手架变化时运行；
- 提交前完整验证通过。

## 下一阶段

### Stage 11：Research Gap Map

状态：`planned`

持久化 Issue：[#13](https://github.com/twobox/self-evo-llm-agent-doc/issues/13)

计划输出：

```text
surveys/research-gap-map.md
```

重点主题：

- 失败经验利用；
- 轨迹经验库与跨轨迹抽象；
- 大小模型协同；
- token / rollout / wall-clock 成本；
- 跨任务持久性；
- Harness 写入、检索、激活、遵循与真实收益；
- 参数更新与外挂经验的贡献拆分；
- 错误经验、冲突、过期和遗忘治理。

启动条件：Stage 10 PR 合并。

## 后续候选阶段

### Stage 12：新论文接入演练

使用一篇新论文完整演练：

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

## 新会话恢复步骤

1. 读取 `AGENTS.md`；
2. 读取本文件；
3. 找到“当前活动阶段”；
4. 打开对应 GitHub Issue 或 PR；
5. 读取 `docs/new-note-workflow.md` 和 `skills/note-maintainer/SKILL.md`；
6. 检查最新 `main` 与 open PR；
7. 从未完成的验收项继续。

## 更新规则

以下事件发生时必须更新本文件：

- 阶段开始、暂停、完成或取消；
- 稳定里程碑合并；
- active Issue / PR 改变；
- 维护规则或验收条件改变；
- 下一阶段优先级改变。
