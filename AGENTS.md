# Repository Agent Instructions

本文件是任何 AI Agent、代码 Agent 或新会话进入本仓库时的首要入口。**不要依赖之前的聊天记录恢复项目状态；仓库文件和 GitHub Issue 才是持久化事实来源。**

## 1. 开始任务前必须读取

按顺序读取：

1. `AGENTS.md`
2. `maintenance/roadmap.md`
3. `docs/new-note-workflow.md`
4. `skills/note-maintainer/SKILL.md`
5. `docs/metadata-schema.md`
6. `docs/note-style-guide.md`
7. 与当前任务相关的已有笔记、横向综述和 active GitHub Issue

如果 roadmap 与聊天要求冲突，以用户本轮明确要求为最高优先级，并在完成后同步更新 roadmap。

## 2. 仓库职责

本仓库不是普通 Markdown 集合，而是一套可验证的研究笔记系统。修改单篇笔记时必须同时考虑：

- metadata 与 README 索引；
- 正文快速阅读层和证据结构；
- `related_notes` 与相近工作；
- 图片来源、许可和 manifest；
- `surveys/experimental-comparison-data.json`；
- 自动生成的横向综述；
- CI 与单元测试。

## 3. 新论文或新笔记

收到论文链接、PDF、项目页、代码仓库或正文时：

1. 检查 `notes/` 中是否已有同一论文或相近工作；
2. 核验论文最新版本、venue、代码、模型和作者机构，不根据标题或二手资料猜测；
3. 先确定 `paper_type`、`evolution_object`、`learning_stage`、`parameter_update`、`cross_task`；
4. 使用 `scripts/scaffold_note.py` 建立文件骨架；
5. 按 `docs/new-note-workflow.md` 完成正文；
6. 更新 README 和横向实验数据；
7. 处理图片许可；
8. 运行完整验证；
9. 创建 Draft PR。

## 4. 更新已有笔记

更新前先读取完整笔记和相关工作。禁止只追加零散段落而不检查：

- 顶部“30 秒读懂”是否仍准确；
- 机制 / 分析卡片是否需要同步；
- “主张—证据—边界”是否被新证据改变；
- metadata 的 `updated`、`last_verified` 和外部状态；
- README、横向综述和图片清单。

## 5. 内容底线

- 不把作者主张写成已被普遍证明的事实；
- 不把相关性写成因果；
- 不把测试时搜索写成长期跨任务学习；
- 不把辅助模块训练写成主模型参数更新；
- 不把 Position、Theory 或 Survey 虚构成传统 SOTA 实验；
- 不根据论文标题猜测 venue、代码状态、模型状态或作者机构；
- 不复制许可不明确的图片；
- 不删除已有深度内容来换取表面统一。

## 6. 必须维护的正文结构

全部笔记必须具有：

- `30 秒读懂`
- 论文定位
- 研究问题
- 方法 / 系统论文的进化机制卡片，或分析 / 诊断 / 综述 / Position 的分析框架卡片
- `主张—证据—边界`
- `我的判断`
- `其他可能解释`
- `论文外部信息`
- 参考资料

章节顺序必须满足：

```text
主张—证据—边界
  < 论文外部信息
  < 最后的参考资料章节
```

## 7. 图片规则

读取 `docs/image-assets.md`。本地化图片必须：

- 来源明确；
- 许可允许再分发；
- 记录原始 URL、许可、署名、SHA-256 和字节数；
- 写入 `assets/images/manifest.json`；
- 更新 `maintenance/image-inventory.json`；
- 未经允许不得裁剪、重编码或叠加标记。

许可不明确时保留外链，并记录 `deferred-license` 原因。

## 8. 横向综述规则

新增或实质更新论文后，检查并更新：

```text
surveys/experimental-comparison-data.json
```

然后运行：

```bash
python scripts/generate_experimental_comparison.py
```

不要直接手工修改生成后的 `surveys/experimental-comparison.md` 而不更新数据源。

## 9. 完整验证

提交前运行：

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/validate_notes.py . --require-schema --require-structure --strict
python scripts/check_links.py .
python scripts/check_images.py .
python scripts/generate_experimental_comparison.py --check
python scripts/generate_readme.py . --check --require-markers --output /tmp/generated-note-index.md
```

任何失败都必须修复或在 PR 中明确说明，不能静默跳过。

## 10. Git 与 PR

- 从最新 `main` 创建 `codex/<description>` 分支；
- 默认创建 Draft PR；
- PR 描述必须说明修改范围、证据来源、生成文件、图片许可和验证结果；
- 不再为一个连续阶段无限堆叠 PR；达到稳定里程碑时应合并收口；
- active stage 和后续阶段必须写入 `maintenance/roadmap.md` 和 GitHub Issue。

## 11. 新会话恢复

新会话只需执行：

```text
读取 AGENTS.md、maintenance/roadmap.md、docs/new-note-workflow.md、
skills/note-maintainer/SKILL.md 和 roadmap 指向的 active Issue，
然后从 active stage 继续，不依赖旧聊天记录。
```
