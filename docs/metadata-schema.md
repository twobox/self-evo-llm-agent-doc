# 单篇论文笔记 Metadata 规范

本文定义 `notes/*.md` 顶部隐藏式 metadata 的目标结构。后续校验脚本、README 生成器和横向综述工具都应以这里的定义为准。

## 1. 基本原则

1. 继续使用 HTML 注释，不改用 YAML front matter。
2. metadata 是结构化事实，不写长篇解释和个人判断。
3. URL 字段只能填写合法 URL 或空字符串 `''`。
4. 日期统一使用 `YYYY-MM-DD`。
5. 会议录用、arXiv 版本、代码状态等独立事实必须拆成独立字段。
6. 不确定的事实保持空值或使用明确的 `unknown` 状态，不根据题目、作者简介或二手文章猜测。
7. `README.md` 和横向综述中的结构化信息应尽量从 metadata 生成，而不是重复手工维护。

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
  venue_track: ''
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
| `schema_version` | string | 当前固定为 `'1.0'` |
| `title` | string | 论文正式标题；优先采用正式 proceedings 标题，其次 arXiv 标题 |
| `short_title` | string | README、表格和正文中使用的简称 |
| `year` | integer | 论文主要引用年份；规则见第 7 节 |
| `note_type` | enum | 当前固定为 `'中文读书笔记'` |
| `paper_type` | enum | 论文主要性质 |
| `paper_status` | enum | 当前可验证的发布状态 |
| `venue` | string | 主要会议、期刊或 `arXiv`；不要混入日期和版本 |
| `evolution_object` | string | 论文主要更新、演化或分析的对象 |
| `learning_stage` | enum | 机制发生在训练时、测试时、部署时或混合阶段 |
| `parameter_update` | enum | 是否更新模型参数 |
| `cross_task` | enum | 是否在不同任务之间积累或复用 |
| `authors` | list[string] | 按论文署名顺序记录 |
| `topics` | list[string] | 面向阅读者的主题名称，可保留大小写和空格 |
| `tags` | list[string] | 面向机器检索的小写短横线标签 |
| `related_notes` | list[string] | 仓库根目录相对路径，例如 `notes/example.md` |
| `created` | date | 笔记首次创建日期 |
| `updated` | date | 笔记内容最近修改日期 |
| `last_verified` | date | 外部事实最近核验日期 |

## 4. 枚举字段

### 4.1 `paper_type`

只填写一个最主要的类型：

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

一篇论文同时具备多种性质时，主类型写入 `paper_type`，其他性质写入 `topics` 或 `tags`。不要使用 `method / framework / agent training paper` 这类自由组合字符串。

### 4.2 `paper_status`

- `preprint`：仅公开预印本，未找到正式录用信息
- `submitted`：有可靠来源确认正在投稿，但未录用
- `accepted`：已确认录用，正式 proceedings 尚未发布或不区分
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

### 4.4 `learning_stage`

- `training`
- `test-time`
- `deployment`
- `mixed`
- `not-applicable`

### 4.5 `parameter_update`

- `yes`
- `no`
- `auxiliary-only`
- `mixed`
- `not-applicable`

### 4.6 `cross_task`

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
| `original_code_url` | 原始代码地址；发生迁移或跳转时记录 |
| `resource_url` | 综述资源列表、benchmark 集合等非实验代码资源 |
| `model_url` | 官方模型权重或模型页面 |

规则：

```yaml
code_url: ''
code_status: 'not_found'
```

正确。下面这种写法不允许：

```yaml
code_url: '暂未找到官方代码'
```

综述资源列表不能冒充实验代码：

```yaml
code_url: ''
resource_url: 'https://github.com/example/awesome-list'
code_status: 'not_applicable'
```

## 6. 日期字段

| 字段 | 说明 |
|---|---|
| `first_submitted` | arXiv v1 或可验证的首次公开提交日期 |
| `last_revised` | 当前记录版本的最后修订日期 |
| `accepted_at` | 可确认的录用日期；只知道会议年份时留空 |
| `published_at` | 正式 proceedings 或期刊发布日期 |
| `last_verified` | 最近一次核验 venue、代码、模型等外部事实的日期 |
| `created` | 仓库笔记创建日期 |
| `updated` | 仓库笔记最近实质修改日期 |

不要把 OpenReview 页面“Last Modified”直接当作论文修订日期。确需记录时，应在正文外部信息部分说明，而不是复用 `last_revised`。

## 7. `year` 的确定规则

按以下优先级选择：

1. 正式 proceedings / 期刊引用年份；
2. 已录用会议的会议年份；
3. 未录用预印本的 arXiv 首次提交年份。

因此，一篇 2025 年首次上传、被 ICML 2026 接收的论文，`year` 应填写 `2026`；BibTeX 中若仍采用 arXiv 引用，可以在正文 BibTeX 区保留原引用年份，但不影响 metadata 的仓库分类年份。

## 8. `venue` 与 `venue_track`

示例：

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

不要写成：

```yaml
venue: 'ICML 2026 / arXiv / OpenReview'
```

arXiv、OpenReview、PMLR 等承载页面通过 URL 字段体现；`venue` 只表示主要发表载体。

## 9. `topics` 与 `tags`

### `topics`

面向人阅读，可以写：

```yaml
topics:
  - 'Self-Evolving LLM Agent'
  - 'Agent Memory'
  - 'Test-Time Learning'
```

### `tags`

面向脚本、搜索和分类，必须：

- 全部小写；
- 只使用英文字母、数字和短横线；
- 不使用空格和下划线；
- 同一概念全仓库使用同一写法。

```yaml
tags:
  - 'self-evolving-agent'
  - 'agent-memory'
  - 'test-time-learning'
```

## 10. `related_notes`

统一使用仓库根目录相对路径：

```yaml
related_notes:
  - 'notes/harness-updating-is-not-harness-benefit.md'
```

不允许：

```yaml
related_notes:
  - 'harness-updating-is-not-harness-benefit.md'
```

关系应当有实质意义，优先选择：

- 机制最接近的工作；
- 结论直接支持或冲突的工作；
- 横向比较时最需要一起阅读的工作。

不要把所有笔记互相全部关联。

## 11. 完整示例

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

## 12. 迁移原则

现有笔记迁移到 schema 1.0 时：

1. 只拆分和规范已有可验证事实，不顺便改写正文；
2. 对外部状态重新核验并填写 `last_verified`；
3. 无法确认的信息使用空值或 `unknown`；
4. 保留原有作者顺序和有价值的主题分类；
5. metadata 修改和正文重构应分开提交，便于审阅和回滚。
