# 笔记仓库维护审计报告

> 仓库：`twobox/self-evo-llm-agent-doc`  
> 审计日期：`2026-06-24`  
> 默认分支：`main`  
> 审计快照：`18b6f89429b9781623ff60da35d7e45ca8ba4757`  
> 本次范围：只新增审计材料，不修改现有笔记、README 或横向综述正文。

## 1. 审计结论

仓库当前已形成较完整的研究笔记体系：

- 检出 **11 篇单篇笔记**；
- 检出 **1 份横向综述**：`surveys/experimental-comparison.md`；
- README 已收录全部 11 篇检出的单篇笔记，没有发现 Markdown 笔记孤岛；
- 所有笔记均包含局限性、个人理解或评价、实验或证据讨论等深层内容；
- 当前主要问题不是内容不足，而是 **metadata 不可机器稳定解析、索引信息漂移、快速阅读层缺失、结构顺序不统一、资源链接长期稳定性不足**。

建议后续按照“先规范和自动检查，再批量重构正文”的顺序维护。

## 2. 审计范围与方法

本次审计读取并对照了：

- `README.md`
- `notes/` 中检出的 11 篇 Markdown 笔记
- `surveys/experimental-comparison.md`
- 每篇笔记顶部的 HTML 注释 metadata
- README 中的论文索引
- `related_notes`、Markdown 内部链接和图片引用形式
- 常用章节与关键词：一句话总结、实验设计、局限性、我的理解等

机器可读的逐篇清单见：

- `maintenance/note-inventory.json`

### 范围限制

当前 GitHub 连接器可以稳定读取和搜索文本文件，但不能完整枚举未被代码搜索索引的二进制文件树。因此：

- 本报告可以确认没有在检出的 Markdown 中发现 `../assets/...` 一类本地资源引用；
- 检出的插图均使用外部 URL；
- 不能仅依靠本次接口断言仓库中绝对不存在未被引用的 PDF、图片或其他二进制文件；
- 后续建立本地校验脚本时，应在完整 checkout 上补做一次文件树和孤立资源扫描。

## 3. 仓库清单

### 3.1 根目录与综述

| 类型 | 路径 | 状态 |
|---|---|---|
| 首页与索引 | `README.md` | 已覆盖全部检出的单篇笔记 |
| 横向综述 | `surveys/experimental-comparison.md` | 已覆盖核心 Self-Evolving Agent 论文，但未纳入边界研究笔记 |

### 3.2 单篇笔记

| 序号 | 简称 | 路径 | README 收录 |
|---:|---|---|---|
| 1 | ACE | `notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md` | 是 |
| 2 | EvolveR | `notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md` | 是 |
| 3 | Harness Updating | `notes/harness-updating-is-not-harness-benefit.md` | 是 |
| 4 | Theory of Agent | `notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md` | 是 |
| 5 | SE-Agent | `notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md` | 是 |
| 6 | Self-Challenging Agents | `notes/self-challenging-language-model-agents.md` | 是 |
| 7 | Gödel Agent | `notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md` | 是 |
| 8 | From Storage to Experience | `notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md` | 是 |
| 9 | MemoPilot | `notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md` | 是 |
| 10 | MLEvolve | `notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md` | 是 |
| 11 | On the Limits of LLM Adaptability | `notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md` | 是 |

## 4. 高优先级问题

### 4.1 Metadata 目前难以稳定自动处理

**影响：全部笔记。**

当前 `status` 和 `venue` 经常在一个字符串里混合：

- arXiv 版本；
- 首次提交日期；
- 最后修订日期；
- 会议录用状态；
- poster / oral / spotlight；
- OpenReview 更新时间；
- 代码公开状态。

例如一条 `status` 可能同时写入会议、arXiv 和代码信息。这样适合阅读，但不适合作为 README 自动生成、状态筛选和一致性校验的数据源。

建议后续拆为：

- `paper_status`
- `venue`
- `venue_track`
- `first_submitted`
- `last_revised`
- `accepted_at`
- `code_status`
- `last_verified`

### 4.2 URL 字段存在非 URL 内容

**明确受影响：MemoPilot。**

其 metadata 中：

- `code_url` 是“论文摘要称已公开代码，当前笔记尚未补入链接”；
- `original_code_url` 是“暂未找到”；
- `model_url` 是“暂未找到”。

这会导致任何 URL 校验器或自动索引脚本失败。建议 URL 字段只允许：

- 合法 URL；
- 空字符串。

状态说明应放入 `code_status`、`model_status` 或备注字段。

### 4.3 README 与单篇笔记状态不一致

#### Harness Updating

README 当前标记为 `arxiv 2025`，但：

- metadata 中 `year` 为 2026；
- arXiv ID 为 `2605.30621`；
- metadata 写明 v1 提交于 2026-05-28。

这是明确的年份/状态漂移。

#### On the Limits of LLM Adaptability

README 当前仅标记为 `arXiv 2026`，但笔记 metadata 已记录：

- ICML 2026 Oral & Spotlight；
- PMLR vol. 306；
- arXiv 版本。

README 状态明显落后于单篇笔记。

### 4.4 全部笔记缺少统一的快速阅读层

**影响：11/11 篇。**

检出的笔记都没有标准化的 `30 秒读懂` 区域。部分笔记有“一句话总结”，部分在“基本信息”中直接给出摘要，部分要阅读较长的投稿和作者信息后才进入核心问题。

建议统一增加：

- 一句话总结；
- 文章性质；
- 核心问题；
- 核心机制；
- 更新对象；
- 学习阶段；
- 是否跨任务；
- 是否更新模型参数；
- 最重要结论；
- 最大局限；
- “不要误读”。

## 5. 中优先级问题

### 5.1 核心内容前存在较长外部信息

较明显的文件：

- `notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md`
- `notes/harness-updating-is-not-harness-benefit.md`
- `notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md`
- `notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md`

这些笔记内容本身完整，但作者、机构、投稿状态和研究圈子占据较靠前位置，降低首次阅读和快速回顾效率。

建议后续先补快速阅读层，再将外部信息移动到正文后部；不要直接删除已有研究圈子信息。

### 5.2 `related_notes` 路径规范不一致

两种写法并存：

```text
notes/harness-updating-is-not-harness-benefit.md
```

以及：

```text
harness-updating-is-not-harness-benefit.md
```

使用同目录裸文件名的笔记包括：

- Theory of Agent
- SE-Agent
- Self-Challenging Agents
- Gödel Agent

建议统一采用仓库根目录相对路径 `notes/...`，便于脚本从任意工作目录验证。

### 5.3 Tags 命名规范不一致

以下笔记使用了大写、空格或展示名称：

- Theory of Agent
- SE-Agent
- Self-Challenging Agents
- Gödel Agent

示例：

```text
LLM Agent
agentic RL
SWE-bench Verified
Meta Agent Search
```

其他笔记则使用小写短横线：

```text
self-evolving-agent
agent-memory
test-time-learning
```

建议 metadata 中统一使用机器友好的小写短横线；正文和 README 可以继续使用展示名称。

### 5.4 横向综述的覆盖声明与实际范围不完全一致

`surveys/experimental-comparison.md` 自述用于整理仓库中已阅读论文，但当前没有检索到：

- `On the Limits of LLM Adaptability`

如果该文件只覆盖“有实验设置可横向比较的核心自进化 Agent 工作”，应在 scope 中明确排除边界研究；如果目标确实是覆盖全部笔记，则需要为边界研究增加分析型条目。

### 5.5 插图依赖外部 URL

检测到至少 **10/11 篇** 笔记引用外部图片，包括：

- arXiv HTML 图片；
- 项目页图片；
- GitHub raw/blob 图片。

没有检测到本地 `assets/` 相对引用。外链可能因论文版本、项目站点或路径变化而失效。

建议后续：

1. 只保留最有复习价值的图；
2. 按论文建立 `assets/<paper-slug>/`；
3. 使用稳定文件名；
4. 保留来源、原图编号和阅读重点；
5. 增加本地图片存在性检查。

## 6. 低优先级问题

### 6.1 外部信息重复

多篇笔记在以下位置重复相同信息：

- metadata；
- 标题下链接区；
- 投稿状态章节；
- 文末参考链接；
- BibTeX。

建议 metadata 作为唯一结构化数据源，正文顶部只展示最重要的论文、代码和状态，文末只保留扩展资料。

### 6.2 README 列名语义不准确

README 使用“发表时间”列，但单元格实际混合：

- venue；
- 年份；
- poster / position paper；
- arXiv 状态。

建议改为：

```text
Venue / 状态
```

### 6.3 README 主题描述有重复

README 开头的方向描述中 `Tool-use Agent` 出现两次，可在后续索引重构时顺手清理。

### 6.4 `code_url` 的语义不统一

`From Storage to Experience` 的 `code_url` 指向综述资源列表，而不是可执行实验代码。建议增加：

- `project_url`
- `resource_url`
- `code_status`

以区分代码、项目页、资源列表和模型页。

## 7. 已确认的优点

本次审计不建议用统一模板覆盖或删减以下已有优势：

1. **个人理解充分**：全部笔记都能检索到作者观点之外的解释或评价。
2. **局限性覆盖较好**：全部笔记均讨论局限、边界或不能过度外推之处。
3. **实验记录较扎实**：方法型笔记普遍记录 benchmark、baseline、指标和消融。
4. **概念澄清有价值**：多篇笔记明确区分参数训练、外部 memory、harness、trajectory 和测试时优化。
5. **横向关系已经成形**：单篇笔记之间存在较多对照表和 `related_notes`。
6. **README 没有塞入单篇长文**：首页作为索引的定位正确。

后续重构应保留这些内容，只调整入口、层级和机器可维护性。

## 8. 自动修复与人工确认边界

### 可以自动修复

- `related_notes` 路径统一；
- tags 转为小写短横线；
- URL 字段中的占位文本拆到状态字段；
- README 从 metadata 生成；
- 增加 `last_verified`；
- 增加统一快速阅读模板；
- 检查内部链接和本地图片；
- 检测 metadata 必填字段和枚举值。

### 需要来源验证后修复

- 会议/期刊正式状态；
- oral、spotlight、poster 等 track；
- 首次提交和最后修订日期；
- 代码、模型和项目页是否仍可访问；
- 作者机构和机构映射；
- 论文标题在 arXiv 与正式 proceedings 之间的差异。

### 不应自动覆盖

- “我的理解”；
- 对研究圈子的判断；
- 创新性评价；
- 局限性和替代解释；
- 研究想法；
- 图的阅读说明。

## 9. 建议的后续执行顺序

1. 新增 `docs/metadata-schema.md`、`docs/note-style-guide.md` 和模板；
2. 实现 metadata 解析与校验脚本；
3. 实现 README 自动生成和 `--check` 模式；
4. 统一 metadata，并修复 README 漂移；
5. 先以 Harness、MemoPilot、SE-Agent 三篇做快速阅读层试点；
6. 批量处理其他笔记；
7. 本地化核心图片；
8. 拆分横向综述；
9. 进行最终全仓库质量审查。

## 10. 本次审计的验收结果

| 检查项 | 结果 |
|---|---|
| README 是否收录全部检出的笔记 | 通过，11/11 |
| 是否存在检出的孤立 Markdown 笔记 | 未发现 |
| 是否存在 metadata | 通过，11/11 |
| 是否存在统一快速阅读层 | 不通过，0/11 |
| 是否存在明显 URL 字段违规 | 不通过，MemoPilot |
| README 与笔记状态是否一致 | 不通过，至少 2 处明确漂移 |
| `related_notes` 是否统一 | 不通过 |
| tags 是否统一 | 不通过 |
| 横向综述是否覆盖其声明范围 | 需要澄清或补充 |
| 图片是否本地化 | 不通过，检测到的图片均为外链 |
| 是否修改现有笔记正文 | 未修改 |

---

本报告是后续规范、脚本和批量修复工作的基线。任何自动化修复都应以 `maintenance/note-inventory.json` 为输入，并在修改后重新生成审计结果进行前后对比。
