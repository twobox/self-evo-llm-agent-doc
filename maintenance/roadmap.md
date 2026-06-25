# Repository Maintenance Roadmap

> 本文件是跨会话项目状态入口。聊天记录可能丢失，但这里必须持续保持最新。

## 当前稳定里程碑

### Systematic Note Management Foundation

- 合并 PR：[#12](https://github.com/twobox/self-evo-llm-agent-doc/pull/12)
- `main` 提交：`eebf9145a45d6e60352f583abc734ed5e2d56e07`
- 完成日期：2026-06-25

完成能力：

- metadata schema 1.0；
- 单篇笔记模板和写作规范；
- README 自动生成；
- 严格 metadata / 正文结构校验；
- 图片许可、manifest 和完整性治理；
- 11 篇笔记统一快速阅读层与证据层；
- 结构化横向实验对比；
- 单元测试和 GitHub Actions。

### Persistent Note Maintenance Workflow

- 合并 PR：[#14](https://github.com/twobox/self-evo-llm-agent-doc/pull/14)
- `main` 提交：`e12d9f7969c56781be4349c2cc33b4f710b3b9b3`
- 完成日期：2026-06-25

完成能力：

- `AGENTS.md` 新会话入口；
- roadmap 持久化项目状态；
- 新笔记完整接入流程；
- 仓库内 Note Maintainer Skill；
- 新笔记脚手架；
- Issue / PR 模板；
- 维护入口专用测试和 CI。

## 当前活动阶段

### Stage 11：Research Gap Map

状态：`in progress`

分支：`codex/build-research-gap-map`

活动 PR：[#15](https://github.com/twobox/self-evo-llm-agent-doc/pull/15)

持久化 Issue：[#13](https://github.com/twobox/self-evo-llm-agent-doc/issues/13)

计划输出：

```text
surveys/research-gap-map.md
```

目标：

- 将仓库 11 篇笔记的证据映射为可检验研究空白；
- 补充截至 2026-06 的最新相关工作，避免使用过时的新颖性判断；
- 区分概念、算法、评测、工程和成本缺口；
- 为每个 gap 写出已有证据、剩余实验、反证条件和风险；
- 提出适合 1–2 个月研究周期的候选小课题。

重点主题：

- 失败经验利用；
- 轨迹经验库与跨轨迹抽象；
- 大小模型协同；
- token / rollout / wall-clock 成本；
- 跨任务持久性；
- Harness 写入、检索、激活、遵循与真实收益；
- 参数更新与外挂经验的贡献拆分；
- 错误经验、冲突、过期和遗忘治理。

验收条件：

- 覆盖仓库全部 11 篇笔记；
- 至少形成 5 个明确 research gap；
- 至少提出 3 个可执行小课题；
- 每个小课题包含假设、最小实验、baseline、指标、预算和失败风险；
- 记录最新外部工作并据此收窄 gap；
- 通过链接、单元测试和完整仓库 CI。

## 下一阶段

### Stage 12：新论文接入演练

状态：`planned`

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
