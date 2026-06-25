# 新论文笔记接入工作流

本工作流用于新增或实质更新论文笔记。目标不是“写出一篇 Markdown”，而是让单篇笔记、README、横向综述、图片资产和 CI 保持一致。

## 1. 输入形式

可以从以下任一输入开始：

- arXiv / OpenReview / proceedings 页面；
- PDF；
- 项目页；
- GitHub 仓库；
- 用户提供的正文或摘要；
- 已有笔记文件。

只有二手介绍而没有原始来源时，可以先建立调研 Issue，但不应直接写入确定性的 venue、代码状态或实验数字。

## 2. 开始前检查

### 2.1 恢复项目状态

读取：

1. `AGENTS.md`
2. `maintenance/roadmap.md`
3. `skills/note-maintainer/SKILL.md`
4. active Issue / PR

### 2.2 检查重复和相近工作

搜索：

- 论文完整标题；
- arXiv ID；
- 项目名和简称；
- 作者；
- 核心术语；
- `related_notes`。

如果已有同一论文，优先更新原文件，不要重复创建。

### 2.3 判断任务类型

| 情况 | 行动 |
|---|---|
| 新论文，仓库中没有笔记 | 新建 note，并更新全部关联视图 |
| 已有笔记，但论文版本 / venue / 代码状态变化 | 更新 metadata、外部信息和相关视图 |
| 已有笔记，但解释过浅或有误 | 更新正文、卡片和证据边界 |
| 只想记录候选论文，尚未精读 | 创建 Issue，不创建不完整 note |

## 3. 核验外部事实

优先使用原始来源：

1. 正式 proceedings / 会议页面；
2. arXiv abs / PDF / HTML；
3. OpenReview；
4. 官方项目页；
5. 官方 GitHub 仓库；
6. 作者主页或机构主页。

至少核验：

- 正式标题；
- arXiv ID 与版本；
- paper status；
- venue 与 track；
- 首次提交和最近修订日期；
- 作者和机构；
- 项目页、代码、模型和资源链接；
- code / model status；
- 图片许可。

不确定时使用 `unknown`、`not_found` 或空值，不进行猜测。

## 4. 研究定位分类

创建正文前先确定以下字段：

### 4.1 `paper_type`

选择一个主要类型：

- `method`
- `system`
- `analysis`
- `diagnostic`
- `evaluation`
- `survey`
- `position`
- `benchmark`
- `dataset`
- `theory`

### 4.2 `evolution_object`

回答：系统到底在改变什么？

例如：

- Model Parameters
- Auxiliary Policy
- Memory
- Context / Playbook
- Prompt / Skill / Harness
- Trajectory Pool
- Solution Graph
- Agent Code
- Synthetic Tasks
- Evaluation / Capability Boundary

不要只写 `Agent` 或 `Self-Evolution`。

### 4.3 `learning_stage`

- `training`
- `test-time`
- `deployment`
- `mixed`
- `not-applicable`

### 4.4 `parameter_update`

- `yes`
- `no`
- `auxiliary-only`
- `mixed`
- `not-applicable`

### 4.5 `cross_task`

- `yes`
- `no`
- `conditional`
- `not-applicable`

判断标准是改进结果是否在后续不同任务中保留，不是一次任务中是否有多步交互。

## 5. 创建文件骨架

推荐命令：

```bash
python scripts/scaffold_note.py \
  --title "Paper Title" \
  --short-title "Short Name" \
  --year 2026 \
  --paper-type method \
  --paper-status preprint \
  --evolution-object "Memory Update Policy" \
  --learning-stage mixed \
  --parameter-update auxiliary-only \
  --cross-task yes
```

脚本会：

- 生成英文短横线文件名；
- 拒绝覆盖已有文件；
- 填入结构分类和创建日期；
- 根据论文类型保留进化机制卡片或分析框架卡片；
- 输出后续待办。

脚本不会猜测作者、venue、链接、实验结果或 tags。

## 6. 编写正文

### 6.1 顶部快速阅读层

必须能在 30 秒内回答：

- 论文是什么类型；
- 解决什么问题；
- 改变什么对象；
- 在什么阶段学习；
- 是否更新参数；
- 是否跨任务；
- 最重要结论；
- 最大局限；
- 最容易被误读成什么。

### 6.2 论文定位

至少比较两类相邻工作：

- 机制最接近；
- 结论直接支持或冲突；
- 容易被混淆但实质不同。

不要只罗列 Related Work。

### 6.3 机制或分析卡片

方法 / 系统论文重点写：

```text
信号从哪里来
→ 更新什么
→ 以什么形式存储
→ 何时更新
→ 后续怎样使用
→ 作用范围
```

分析 / 诊断 / 综述 / Position 重点写：

```text
被质疑的假设
→ 关键变量
→ 控制方式
→ 诊断指标
→ 核心发现
→ 结论边界
```

### 6.4 实验与证据

必须记录：

- benchmark / 环境；
- 模型与角色；
- baseline；
- 评价指标；
- rollout、token、wall-clock、硬件等预算；
- 主结果；
- 消融；
- 失败案例；
- 公平性问题；
- 复现条件。

没有传统实验的论文，应写“证据来源与论证方式”，不能虚构主结果。

### 6.5 主张—证据—边界

每个核心结论必须区分：

| 论文主张 | 支持实验或论证 | 最强对照 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|

然后补充：

- `我的判断`
- `其他可能解释`

## 7. 图片流程

先读 `docs/image-assets.md`。

### 可本地化

- 许可明确允许再分发；
- 来源为论文或官方项目；
- Figure 对应关系可确认；
- 能记录署名和许可链接。

### 保留外链

- 只有 arXiv nonexclusive distribution license；
- 项目站点未说明许可；
- 图片可能包含第三方素材；
- Figure 对应关系不确定。

本地化后必须更新：

```text
assets/images/manifest.json
maintenance/image-inventory.json
maintenance/image-inventory.md
```

并运行：

```bash
python scripts/inventory_note_images.py
python scripts/check_images.py .
```

## 8. 更新关联视图

### 8.1 README

```bash
python scripts/generate_readme.py . --write
```

不要手工修改生成标记区。

### 8.2 横向实验对比

在 `surveys/experimental-comparison-data.json` 增加记录，至少填写：

- research-positioning 字段；
- tasks / method；
- benchmarks / metrics；
- strongest baseline；
- headline result；
- cost profile；
- reproducibility；
- evidence strength；
- boundary。

然后运行：

```bash
python scripts/generate_experimental_comparison.py
```

### 8.3 相关笔记

更新新笔记和必要旧笔记的 `related_notes`。关系应有实质意义，不要形成全连接。

### 8.4 Roadmap / Research Map

只有当论文改变当前阶段、填补重要空白或改变选题判断时，才更新 roadmap 或 research gap map。

## 9. 完整验证

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/validate_notes.py . --require-schema --require-structure --strict
python scripts/check_links.py .
python scripts/check_images.py .
python scripts/generate_experimental_comparison.py --check
python scripts/generate_readme.py . --check --require-markers --output /tmp/generated-note-index.md
```

## 10. PR 要求

默认创建 Draft PR。描述必须包括：

- 论文与接入原因；
- 新增还是更新；
- research-positioning 分类；
- 主要内容和证据；
- 图片来源与许可；
- README / 横向对比变化；
- 验证命令与结果；
- 未解决问题。

## 11. 新会话恢复模板

在新会话中发送：

```text
请打开仓库 twobox/self-evo-llm-agent-doc。
先读取 AGENTS.md、maintenance/roadmap.md、docs/new-note-workflow.md、
skills/note-maintainer/SKILL.md 和 roadmap 指向的 active Issue。
然后按仓库规则处理这篇论文：<链接或文件>。
不要依赖之前聊天记录，不要跳过 README、横向实验数据、图片许可和 CI。
```

## 12. 完成定义

新笔记只有同时满足以下条件才算接入完成：

- 单篇笔记完整且事实可追溯；
- metadata 可机器校验；
- README 已更新；
- 横向对比数据已更新；
- 图片已本地化或明确延后；
- 相关笔记关系合理；
- 所有测试和 CI 通过；
- Draft PR 清楚说明证据与边界。
