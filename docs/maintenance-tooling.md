# 笔记维护工具使用说明

Stage 2 提供四个无第三方依赖的 Python 工具。建议使用 Python 3.11 或更高版本。

## 1. 设计原则

当前仓库仍以旧 metadata 为主，因此工具采用过渡策略：

- 旧 metadata：执行基础检查，问题主要报告为 warning；
- schema 1.0 metadata：按照 `docs/metadata-schema.md` 严格校验；
- 真正的文件缺失、解析错误、README 漏链等始终视为 error；
- 等 Stage 3 完成 metadata 迁移后，再在 CI 中启用严格模式。

所有工具只依赖 Python 标准库，不需要安装 PyYAML、Markdown parser 或其他包。

## 2. Metadata 解析

解析单篇笔记：

```bash
python scripts/parse_metadata.py notes/example.md --pretty
```

解析整个 `notes/`：

```bash
python scripts/parse_metadata.py . --pretty
```

解析器支持当前仓库使用的 metadata 子集：

- 顶层标量；
- 字符串列表；
- 单引号或双引号字符串；
- 整数、布尔值和空值；
- 旧笔记中的未加引号字符串。

它不会执行任意 YAML 标签，也不会加载外部对象。

## 3. 笔记校验

过渡模式：

```bash
python scripts/validate_notes.py .
```

机器可读输出：

```bash
python scripts/validate_notes.py . --json
```

严格模式：

```bash
python scripts/validate_notes.py . --strict
```

严格模式会把 warning 也当作失败。Stage 3 完成前不建议在默认 CI 中启用。

### 对所有笔记执行的检查

- 顶部 metadata 是否可解析；
- 是否存在一级标题；
- metadata 标题和一级标题是否明显冲突；
- `authors`、`topics`、`tags`、`related_notes` 是否为字符串列表；
- `related_notes` 目标是否存在；
- README 是否收录全部笔记；
- README 是否链接到已删除笔记。

### schema 1.0 严格检查

- 必填字段；
- 枚举值；
- URL 格式；
- `YYYY-MM-DD` 日期；
- 小写短横线 tags；
- “30 秒读懂”等必需章节；
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

工具只验证本地链接是否存在，并对外部 URL 做基本语法检查，不发送网络请求。这样可以避免 CI 因 arXiv、OpenReview 或项目站点短暂不可用而失败。

## 5. README 索引生成

预览生成结果：

```bash
python scripts/generate_readme.py .
```

保存预览：

```bash
python scripts/generate_readme.py . --output /tmp/note-index.md
```

检查 README 中的生成区：

```bash
python scripts/generate_readme.py . --check
```

当前 README 还没有生成标记，因此 `--check` 只会给出 warning，不会失败。Stage 3 或后续索引迁移时，应加入：

```markdown
<!-- BEGIN GENERATED NOTE INDEX -->
...
<!-- END GENERATED NOTE INDEX -->
```

标记存在后，可以执行：

```bash
python scripts/generate_readme.py . --write
```

或者在 CI 中强制要求标记：

```bash
python scripts/generate_readme.py . --check --require-markers
```

生成器会：

- 从 `notes/*.md` 读取 metadata；
- 根据 boundary-study 标签或边界主题拆分主要笔记和边界研究；
- 按年份降序、标题升序生成稳定表格；
- 输出类型、主题和 Venue / 状态；
- 只替换标记区，不改 README 其他内容。

## 6. 单元测试

```bash
python -m unittest discover -s tests -v
```

测试覆盖：

- metadata 标量和列表解析；
- 重复字段和缺失注释错误；
- schema 1.0 URL、tag 和章节校验；
- 旧 metadata 的过渡 warning；
- README 本地链接；
- README 索引确定性生成。

## 7. 推荐的本地检查顺序

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/validate_notes.py .
python scripts/check_links.py .
python scripts/generate_readme.py . --check --output /tmp/generated-note-index.md
```

## 8. Stage 3 后的严格模式

当全部笔记迁移到 schema 1.0，并且 README 使用生成标记后，CI 应调整为：

```bash
python scripts/validate_notes.py . --strict
python scripts/check_links.py .
python scripts/generate_readme.py . --check --require-markers
```

在此之前，不应让历史技术债阻塞所有 PR；但任何新建的 schema 1.0 笔记会从一开始接受严格字段和结构检查。
