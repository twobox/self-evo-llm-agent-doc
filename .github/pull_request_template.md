## 目标

<!-- 说明本 PR 要解决的问题，以及为什么现在需要修改。 -->

## 修改范围

<!-- 列出新增、更新和生成的文件。 -->

## 研究定位

- Paper type：
- Evolution / analysis object：
- Learning stage：
- Parameter update：
- Cross-task：

<!-- 非论文笔记 PR 可删除本节。 -->

## 证据与边界

- 主要主张：
- 最强证据或对照：
- 能证明什么：
- 不能证明什么：
- 仍不确定的事实：

## 关联视图

- [ ] README 索引已更新或确认无需更新
- [ ] `related_notes` 已更新或确认无需更新
- [ ] `surveys/experimental-comparison-data.json` 已更新或确认无需更新
- [ ] 生成后的横向综述已同步
- [ ] Roadmap / active Issue 已更新或确认无需更新

## 图片与许可

- [ ] 没有新增或修改图片
- [ ] 图片来源和 Figure 编号已核验
- [ ] 再分发许可已核验
- [ ] manifest、inventory、署名和 SHA-256 已更新
- [ ] 许可不明确的图片保留外链并记录延后原因

## 验证

- [ ] `python -m compileall -q scripts tests`
- [ ] `python -m unittest discover -s tests -v`
- [ ] `python scripts/validate_notes.py . --require-schema --require-structure --strict`
- [ ] `python scripts/check_links.py .`
- [ ] `python scripts/check_images.py .`
- [ ] `python scripts/generate_experimental_comparison.py --check`
- [ ] `python scripts/generate_readme.py . --check --require-markers --output /tmp/generated-note-index.md`

## 未修改内容

<!-- 明确哪些相邻内容有意没有改动，减少审阅歧义。 -->

## 后续工作

<!-- 链接 Issue 或 roadmap 阶段。不要只把下一步留在聊天记录中。 -->
