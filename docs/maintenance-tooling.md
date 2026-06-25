# 笔记维护工具使用说明

仓库使用四个无第三方依赖的 Python 工具，建议使用 Python 3.11 或更高版本。

## 1. 当前状态

Stage 3 完成后：

- 全部 `notes/*.md` 已迁移到 metadata schema 1.0；
- README 笔记索引由 metadata 生成，并受生成标记保护；
- CI 强制拒绝旧 metadata；
- 全部笔记已具备“30 秒读懂”、论文定位、研究问题和适用的机制 / 分析卡片；

所有工具只依赖 Python 标准库，不需要安装 PyYAML 或 Markdown 解析器。

## 2. Metadata 解析

解析单篇笔记：

```bash
python scripts/parse_metadata.py notes/example.md --pretty
```

解析整个 `notes/`：

```bash
python scripts/parse_metadata.py . --pretty
```

解析器支持仓库 metadata 使用的标量、字符串列表、整数、布尔值和空值。它不会执行任意 YAML 标签，也不会加载外部对象。

## 3. 笔记校验

当前 CI 使用：

```bash
python scripts/validate_notes.py . --require-schema --require-structure --strict
```

这会同时强制 schema 1.0、统一正文入口，并把所有 warning 视为失败。

机器可读输出：

```bash
python scripts/validate_notes.py . --require-schema --json
```

Stage 4 完成快速阅读层和机制卡片后，使用：

```bash
python scripts/validate_notes.py . --require-schema --require-structure --strict
```

### Metadata 检查

- 必填字段；
- `paper_type`、`paper_status` 等枚举值；
- URL 格式；
- `YYYY-MM-DD` 日期；
- 小写短横线 tags；
- `related_notes` 路径与目标文件；
- README 是否收录全部笔记；
- README 是否链接到已删除笔记。

### 正文结构检查

当前强制检查：

- “30 秒读懂”；
- 论文定位；
- 研究问题；
- 参考资料；
- 方法 / 系统论文的进化机制卡片；
- 分析 / 诊断 / 评测论文的分析框架卡片。


## 4. 本地链接检查

```bash
python scripts/check_links.py .
```

默认扫描：

- `README.md`
- `notes/**/*.md`
- `surveys/**/*.md`

可选扫描 docs：

```bash
python scripts/check_links.py . --include-docs
```

工具只验证本地链接是否存在，并对外部 URL 做基本语法检查，不发送网络请求，避免外部站点短暂不可用导致 CI 失败。

## 5. README 索引生成

预览生成结果：

```bash
python scripts/generate_readme.py .
```

检查 README 生成区是否最新：

```bash
python scripts/generate_readme.py . --check --require-markers
```

根据 metadata 重写生成区：

```bash
python scripts/generate_readme.py . --write
```

生成器只替换下面两个标记之间的内容：

```markdown
<!-- BEGIN GENERATED NOTE INDEX -->
...
<!-- END GENERATED NOTE INDEX -->
```

生成表格包含：

- 论文和笔记链接；
- 论文类型；
- 进化或分析对象；
- 学习阶段；
- 是否更新参数；
- 是否跨任务；
- Venue 和当前状态。

## 6. 单元测试

```bash
python -m unittest discover -s tests -v
```

测试覆盖 metadata 解析、严格与过渡校验、本地链接和 README 索引确定性生成。

## 7. 推荐的本地检查顺序

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/validate_notes.py . --require-schema --require-structure --strict
python scripts/check_links.py .
python scripts/generate_readme.py . --check --require-markers --output /tmp/generated-note-index.md
```

## 8. 新增或修改笔记后的流程

1. 按 `docs/metadata-schema.md` 修改 metadata；
2. 更新 `last_verified` 和 `updated`；
3. 运行 `python scripts/generate_readme.py . --write`；
4. 运行完整检查；
5. 查看 README diff，确认分类和状态正确；
6. 再提交 PR。
