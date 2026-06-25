# 单篇论文笔记 Metadata 规范

本文定义 `notes/*.md` 顶部隐藏式 metadata 的结构。校验脚本、README 生成器和横向综述工具都以此为准。

## 1. 基本原则

1. 继续使用 HTML 注释，不改用 YAML front matter。
2. metadata 只记录结构化事实，不写长篇解释和个人判断。
3. URL 字段只能填写合法 URL 或空字符串 `''`。
4. 日期统一使用 `YYYY-MM-DD`。
5. 录用状态、venue、arXiv 版本、日期和代码状态必须拆成独立字段。
6. 不确定的信息保持空值或使用 `unknown`，不要猜测。
7. README 中的结构化索引由 metadata 自动生成。

## 2. 标准结构

```yaml
<!--
metadata:
  schema_version: '1.0'
  title: ''
  short_title: ''
  year:
  note_type: '中文读书笔记'
  paper_type: ''
  paper_status: ''
  venue: ''
  venue_track: ''
  evolution_object: ''
  learning_stage: ''
  parameter_update: ''
  cross_task: ''
  arxiv_id: ''
  arxiv_version: ''
  arxiv_url: ''
  pdf_url: ''
  html_url: ''
  project_url: ''
  code_url: ''
  original_code_url: ''
  resource_url: ''
  model_url: ''
  code_status: ''
  model_status: ''
  first_submitted: ''
  last_revised: ''
  accepted_at: ''
  published_at: ''
  last_verified: ''
  authors:
    - ''
  institutions:
    - ''
  topics:
    - ''
  tags:
    - ''
  related_notes:
    - ''
  created: ''
  updated: ''
-->
```

## 3. 必填字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `schema_version` | string | 固定为 `'1.0'` |
| `title` | string | 正式论文标题；优先采用正式 proceedings 标题 |
| `short_title` | string | README 和对比表使用的简称 |
| `year` | integer | 主要引用年份；规则见第 7 节 |
| `note_type` | enum | 固定为 `'中文读书笔记'` |
| `paper_type` | enum | 论文的主要性质 |
| `paper_status` | enum | 当前可验证的发布状态 |
| `venue` | string | 主要会议、期刊或 `arXiv` |
| `evolution_object` | string | 主要更新、演化或分析的对象 |
| `learning_stage` | enum | 机制发生的阶段 |
| `parameter_update` | enum | 是否更新模型参数 |
| `cross_task` | enum | 是否跨任务积累或复用 |
| `authors` | list[string] | 按论文署名顺序记录 |
| `topics` | list[string] | 面向读者的主题名称 |
| `tags` | list[string] | 面向机器检索的小写短横线标签 |
| `related_notes` | list[string] | 仓库根目录相对路径 |
| `created` | date | 笔记创建日期 |
| `updated` | date | 笔记最近实质修改日期 |
| `last_verified` | date | 外部事实最近核验日期 |

## 4. 枚举字段

### 4.1 `paper_type`

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

只填写一个主类型，其他性质写入 `topics` 或 `tags`。

### 4.2 `paper_status`

- `preprint`：仅有预印本
- `submitted`：有可靠来源确认正在投稿
- `accepted`：已录用，但不以正式出版状态记录
- `published`：正式会议、期刊或 proceedings 已发布
- `withdrawn`：已撤稿
- `unknown`：无法可靠判断

### 4.3 `code_status`

- `official_available`
- `unofficial_available`
- `claimed_public_link_missing`
- `not_found`
- `not_applicable`
- `unknown`

### 4.4 `model_status`

- `official_available`
- `not_found`
- `not_applicable`
- `unknown`

### 4.5 `learning_stage`

- `training`
- `test-time`
- `deployment`
- `mixed`
- `not-applicable`

### 4.6 `parameter_update`

- `yes`
- `no`
- `auxiliary-only`
- `mixed`
- `not-applicable`

### 4.7 `cross_task`

- `yes`
- `no`
- `conditional`
- `not-applicable`

## 5. URL 字段

| 字段 | 含义 |
|---|---|
| `arxiv_url` | arXiv 摘要页 |
| `pdf_url` | 论文 PDF |
| `html_url` | arXiv HTML、ar5iv 或正式 HTML 版本 |
| `project_url` | 官方项目主页 |
| `code_url` | 当前有效的主要代码仓库 |
| `original_code_url` | 发生迁移前的原始代码地址 |
| `resource_url` | 综述资源列表、benchmark 集合等非实验代码资源 |
| `model_url` | 官方模型权重或模型页面 |

正确写法：

```yaml
code_url: ''
code_status: 'not_found'
```

不允许把说明文字塞进 URL：

```yaml
code_url: '暂未找到官方代码'
```

综述资源列表应单独记录：

```yaml
code_url: ''
resource_url: 'https://github.com/example/awesome-list'
code_status: 'not_applicable'
```

## 6. 日期字段

| 字段 | 说明 |
|---|---|
| `first_submitted` | arXiv v1 或首次公开提交日期 |
| `last_revised` | 当前记录版本的最后修订日期 |
| `accepted_at` | 可确认的录用日期；只知道会议年份时留空 |
| `published_at` | 正式 proceedings 或期刊发布日期 |
| `last_verified` | 最近一次核验 venue、代码和模型等事实的日期 |
| `created` | 仓库笔记创建日期 |
| `updated` | 仓库笔记最近实质修改日期 |

OpenReview 的 `Last Modified` 不应直接写入 `last_revised`。

## 7. `year` 的确定规则

按以下优先级选择：

1. 正式 proceedings 或期刊引用年份；
2. 已录用会议的会议年份；
3. 未录用预印本的 arXiv 首次提交年份。

例如，一篇 2025 年上传、被 ICML 2026 接收的论文，仓库 metadata 中的 `year` 写为 `2026`。

## 8. `venue` 与 `venue_track`

```yaml
paper_status: 'published'
venue: 'NeurIPS 2025'
venue_track: 'Poster'
```

```yaml
paper_status: 'accepted'
venue: 'ICML 2026'
venue_track: 'Oral & Spotlight'
```

```yaml
paper_status: 'preprint'
venue: 'arXiv'
venue_track: ''
```

不要把 arXiv、OpenReview 和正式 venue 混写在同一个字段中。

## 9. 研究定位字段

### `evolution_object`

用简短短语说明论文主要更新、演化或分析的对象，例如：

- `Context / Playbook`
- `Experience Base / Executor Policy`
- `Trajectory Pool`
- `Model Priors / Prompt Adaptability`

### `learning_stage`

描述主要机制发生在哪一阶段。包含离线训练和在线适应时使用 `mixed`。

### `parameter_update`

只训练 memory updater、critic 等外挂模块时使用 `auxiliary-only`；同时更新主模型和外部系统时使用 `mixed`。

### `cross_task`

这里关注经验是否在不同任务实例之间积累或复用，不是论文是否使用多个 benchmark。

## 10. `topics` 与 `tags`

`topics` 面向人阅读，可以保留大小写和空格：

```yaml
topics:
  - 'Self-Evolving LLM Agent'
  - 'Agent Memory'
```

`tags` 面向脚本，必须全部小写，只使用字母、数字和短横线：

```yaml
tags:
  - 'self-evolving-agent'
  - 'agent-memory'
```

## 11. `related_notes`

统一使用仓库根目录相对路径：

```yaml
related_notes:
  - 'notes/harness-updating-is-not-harness-benefit.md'
```

优先关联机制最接近、结论直接支持或冲突、横向比较时需要一起阅读的工作。

## 12. 完整示例

```yaml
<!--
metadata:
  schema_version: '1.0'
  title: 'Example: A Self-Evolving Agent Paper'
  short_title: 'Example Agent'
  year: 2026
  note_type: '中文读书笔记'
  paper_type: 'method'
  paper_status: 'accepted'
  venue: 'ICML 2026'
  venue_track: 'Poster'
  evolution_object: 'External Memory'
  learning_stage: 'mixed'
  parameter_update: 'auxiliary-only'
  cross_task: 'yes'
  arxiv_id: '2601.01234'
  arxiv_version: 'v2'
  arxiv_url: 'https://arxiv.org/abs/2601.01234'
  pdf_url: 'https://arxiv.org/pdf/2601.01234'
  html_url: 'https://arxiv.org/html/2601.01234v2'
  project_url: 'https://example.github.io/project/'
  code_url: 'https://github.com/example/example-agent'
  original_code_url: ''
  resource_url: ''
  model_url: ''
  code_status: 'official_available'
  model_status: 'not_found'
  first_submitted: '2026-01-03'
  last_revised: '2026-04-12'
  accepted_at: ''
  published_at: ''
  last_verified: '2026-06-24'
  authors:
    - 'First Author'
    - 'Second Author'
  institutions:
    - 'Example University'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Agent Memory'
  tags:
    - 'self-evolving-agent'
    - 'agent-memory'
  related_notes:
    - 'notes/harness-updating-is-not-harness-benefit.md'
  created: '2026-06-24'
  updated: '2026-06-24'
-->
```

## 13. 迁移与维护原则

1. metadata 规范化和正文重构分开提交。
2. 修改外部状态前重新核验，并更新 `last_verified`。
3. 无法确认的信息使用空值或 `unknown`。
4. 保留原有作者顺序和有价值的主题分类。
5. 修改 metadata 后运行 `python scripts/generate_readme.py . --write`。
6. 提交前运行仓库完整校验。
