<!--
metadata:
  title: 'Self-Evolving LLM Agent Research Gap Map'
  short_title: 'Research Gap Map'
  note_type: '研究空白与选题地图'
  status: '持续维护'
  scope: '基于仓库 11 篇笔记和 2026-06 补充检索的研究空白、实验缺口与小课题候选'
  created: '2026-06-25'
  updated: '2026-06-25'
-->

# Self-Evolving LLM Agent Research Gap Map

本文档把仓库已有论文证据转化为可检验的研究问题。它不是“论文没做什么”的清单，也不声称覆盖全部最新工作。

> **判断标准：** 一个值得研究的 gap，必须同时满足：已有证据揭示真实问题、现有方法仍有可定位缺口、可以设计反证实验、投入与潜在贡献匹配。

基础对比见：[实验设置横向对比](experimental-comparison.md)。

持久化任务见：[Issue #13](https://github.com/twobox/self-evo-llm-agent-doc/issues/13)。

---

## 1. 30 秒结论

| 方向 | 当前判断 | 研究价值 | 1–2 个月可行性 |
|---|---|---:|---:|
| 失败经验利用 | 已有人做失败重标注、诊断和 Harness 修复；真正空白是**在固定 token / rollout 预算下，哪些失败值得保存和复用** | 高 | 高 |
| 轨迹经验库 | 已证明 memory 效果受 inference strategy 强烈影响；缺少统一、预算公平的跨策略评测 | 高 | 高 |
| 大小模型协同 | 小模型可自演化已被 PACE 部分验证；更有价值的是**何时升级到强模型教师** | 中高 | 中高 |
| 长期记忆与遗忘 | 新 benchmark 已揭示过期记忆复用；Agent 工具任务中的删除、冲突和失效治理仍不足 | 高 | 中 |
| Harness 写入与使用 | Harness Updating、activation、adherence 已被分离；缺少可复用的步骤级使用诊断协议 | 高 | 高 |
| 参数更新与外挂经验 | EvolveR、Self-Challenging、MemoPilot 同时涉及不同更新层；equal-budget 贡献拆分不足 | 中高 | 中 |
| 成本与预算公平 | 多数论文报告最终分数，但 token、rollout、wall-clock、硬件和 verifier 成本不可比 | 高 | 高 |

### 最优先的小课题

> **固定 token 预算下的失败经验选择与效用评测。**

原因：

- 有明确上游信号：失败轨迹、关键失败步骤和 Harness flaw；
- 有明确下游链路：检索、activation、adherence、rescue、regression；
- 不需要训练大型基础模型；
- 可以在 1–2 个环境、2–3 个开源模型上完成；
- 容易形成新的评测协议，而不只是再造一个 memory prompt。

---

## 2. 仓库内证据地图

| 工作 | 已提供的关键证据 | 对研究空白的直接启示 |
|---|---|---|
| [ACE](../notes/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md) | 增量 Context / Playbook 在 AppWorld 和金融任务有效；无 GT 反馈有时会污染上下文 | 经验写入必须受反馈质量、增量更新和成本约束 |
| [EvolveR](../notes/evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md) | 经验检索、经验治理与 RL 互补；经验库过大后可能退化 | 研究重点不应只看“有没有经验库”，而应看选择、评分、删除和参数耦合 |
| [Harness Updating](../notes/harness-updating-is-not-harness-benefit.md) | 写出更新与真正受益是两种能力；存在 activation / adherence failure | 必须分别测写入质量、检索、加载、遵循和最终收益 |
| [Theory of Agent](../notes/position-agents-should-invoke-external-tools-only-when-epistemically-necessary.md) | 工具调用需要与真实知识缺口匹配；最终正确率不足以衡量 effort allocation | memory / tool 系统需要过程成本和必要性指标 |
| [SE-Agent](../notes/se-agent-self-evolution-trajectory-optimization-in-multi-step-reasoning-with-llm-based-agents.md) | Revision / Recombination 能在当前任务内传递轨迹信息 | 轨迹复用的收益需要和多采样预算、搜索策略分开评估 |
| [Self-Challenging](../notes/self-challenging-language-model-agents.md) | 自生成任务与 verifier 可训练 executor；任务覆盖决定 OOD 泛化 | 经验生成质量、验证器偏差和覆盖度共同决定训练收益 |
| [Gödel Agent](../notes/godel-agent-a-self-referential-agent-framework-for-recursive-self-improvement.md) | 程序级自修改可提升任务性能，但 temporary drop 和 failure 普遍存在 | 自修改系统需要失败归因、回滚和验证成本模型 |
| [From Storage to Experience](../notes/from-storage-to-experience-a-survey-on-the-evolution-of-llm-agent-memory-mechanisms.md) | 区分 Storage、Reflection、Experience，以及 repository 与 retrieved memory | 评测应覆盖完整生命周期，而不是只测检索命中 |
| [MemoPilot](../notes/from-player-to-master-enhancing-test-time-learning-of-llm-agents-via-reinforcement-learning-over-memory.md) | 训练 memory updater 能帮助 frozen player；一步奖励改善信用分配 | memory writer 可以独立优化，但依赖奖励、可重复交互和环境稳定性 |
| [MLEvolve](../notes/mlevolve-a-self-evolving-framework-for-automated-machine-learning-algorithm-discovery.md) | 图搜索、跨分支共享和 Retrospective Memory 有消融收益，但预算极高 | 需要同预算 Pareto 比较和低预算退化分析 |
| [On the Limits](../notes/on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md) | DSF、34.8% rescue rate 和 decision stickiness 揭示 Prompt 纠错上限 | 外部经验应测错误救回率、成功样本回退和模型能力边界 |

---

## 3. 2026-06 外部补充证据

这些工作不替代单篇笔记，只用于防止把已出现的方向误判为空白。

| 工作 | 新增证据 | 对 gap 判断的修正 |
|---|---|---|
| [PACE: Two-Timescale Self-Evolution for Small Language Model Agents](https://arxiv.org/abs/2605.23019) | 4B–14B frozen SLM 可通过 prompt 与 control logic 两时间尺度演化获得提升 | “小模型能否自演化”已不是空白；应研究选择性教师升级和风险分层 |
| [SkillLearnBench](https://arxiv.org/abs/2604.20087) | continual skill learning 在真实任务上收益不稳定；强模型不总能产生更好 skill，自反馈可能 drift | Skill 学习需要 activation / adherence / feedback-source 分解，而不是只扩大 backbone |
| [When Does Memory Help Multi-Trajectory Inference?](https://arxiv.org/abs/2605.28224) | 同一 memory 方法在 best-of-N、beam、MCTS 下结果显著不同；atomic facts 可缩短 19–26% 轨迹 | memory abstraction 与 inference strategy 存在混杂，统一预算矩阵仍有空间 |
| [Memora: From Recall to Forgetting](https://arxiv.org/abs/2604.20006) | 长期个性化 memory 经常复用失效信息；提出 Forgetting-Aware Memory Accuracy | “记得更多”不是目标，过期信息删除和更新一致性必须进入评测 |
| [AgentHER](https://arxiv.org/abs/2603.21357) | 将失败轨迹重标注为可实现替代目标，优于 success-only SFT | “利用失败”已有方法；空白转向失败选择、跨任务可迁移性和预算效用 |
| [AgentRx](https://arxiv.org/abs/2602.02475) | 提供 115 条失败轨迹和关键失败步骤 / 类别诊断 | 可以把步骤级失败定位作为 memory 写入和 Harness 修复的前置模块 |
| [HarnessFix](https://arxiv.org/abs/2606.06324) | 将失败步骤归因到 Harness 层并生成 scoped repair，在多 benchmark 上提升 | 泛化 gap 不再是“能否修 Harness”，而是修复选择、回归风险与跨环境迁移 |

### 外部检索后的重要收窄

以下表述不再成立：

- “失败经验基本没人利用”；
- “还没有长期遗忘 benchmark”；
- “小模型无法自演化”；
- “跨轨迹 memory 只缺一个更好的摘要器”；
- “Harness 修复还没有步骤级诊断”。

仍然成立且更精确的问题是：

1. 在固定预算下，哪种失败经验值得保留？
2. memory 的收益是否只是特定搜索策略的副产物？
3. 小模型何时应自主改进，何时应调用强教师？
4. 过期、冲突和错误经验如何删除而不破坏有效知识？
5. Harness 修复如何控制回归、权限和验证成本？

---

## 4. Gap A：成本约束下的失败经验选择

### 已有工作覆盖

- AgentHER：失败轨迹重标注为替代目标；
- AgentRx：定位关键失败步骤和失败类型；
- HarnessFix：将失败归因映射到 scoped Harness repair；
- EvolveR：经验打分、检索和经验库治理；
- MemoPilot：训练 memory writer；
- On the Limits：用 rescue rate 测纠错能力。

### 仍缺什么

现有工作通常回答：

- 失败能否变成训练数据；
- 失败发生在哪里；
- 能否生成修复。

但较少统一回答：

> 在固定 memory token、rollout 和 LLM 调用预算下，保存哪条失败、以何种抽象形式保存、何时检索，能获得最大净收益？

### 可检验假设

- 只保存“可归因、可复现、可执行修复”的失败，比保存所有失败或只保存成功案例更有效；
- 步骤级 failure record 比完整失败轨迹更省 token，但在环境状态依赖强的任务上可能丢失关键上下文；
- failure memory 对低置信错误的 rescue 更明显，对高置信 prior 冲突错误收益有限。

### 推荐指标

- task success / pass rate；
- failed-sample rescue rate；
- previously-correct regression rate；
- memory activation / adherence；
- utility per 1k memory tokens；
- utility per rollout / LLM call；
- stale-memory error rate；
- failure attribution precision。

### 研究风险

- “失败”可能只是随机采样噪声；
- 环境 verifier 不可靠时会写入错误经验；
- failure taxonomy 在不同环境间不可迁移；
- 提升可能来自更多 token，而不是更好的经验选择。

---

## 5. Gap B：跨轨迹 Memory 与搜索策略混杂

### 已有工作覆盖

- SE-Agent：Revision / Recombination / Refinement；
- MLEvolve：solution graph、跨分支共享和 Retrospective Memory；
- When Does Memory Help：在 best-of-N、beam、MCTS 下比较多种 memory abstraction；
- ACE / EvolveR：结构化 Context 或 Experience retrieval。

### 仍缺什么

同一 memory 方法在不同 inference strategy 下可能表现相反，因此不能只报告“加 memory 后提高”。仍缺：

- 同模型、同候选数、同 token、同 verifier 调用预算的统一矩阵；
- memory 对多样性、搜索深度、轨迹长度和错误相关性的影响；
- verifier-free 与 verifier-based 条件下的差异；
- 跨任务保留与单任务候选共享的严格区分。

### 可检验假设

- Reflection memory 主要帮助深搜索，而非独立 best-of-N；
- atomic fact memory 的主要价值可能是缩短轨迹，而不是提高正确率；
- 失败步骤 memory 在 beam search 中减少重复错误，但可能降低候选多样性。

### 最小实验矩阵

```text
Memory:
  none / raw observation / reflection / atomic fact / failure-step record

Inference:
  best-of-N / beam / lightweight MCTS

Budget:
  equal candidates / equal tokens / equal wall-clock
```

### 研究风险

矩阵组合较多，容易变成工程型 benchmark；应优先选择 2 个任务族和 2 个模型，避免无边界扩张。

---

## 6. Gap C：小模型自主改进与强教师选择性升级

### 已有工作覆盖

- PACE：冻结小模型可进行 prompt / control logic 两时间尺度演化；
- MemoPilot：较强 memory updater 可服务 frozen player，并能跨 Player 迁移；
- Self-Challenging：强模型 teacher 可向 8B executor 蒸馏；
- Harness Updating：更强 Evolver 不一定稳定生成更有收益的更新；
- SkillLearnBench：强 backbone 不总能生成更好的 skill。

### 仍缺什么

真正的问题不是“大模型还是小模型”，而是：

> 哪些失败需要强教师，哪些可由小模型自诊断；怎样在收益、token、延迟和隐私之间做动态路由？

### 可检验假设

- 小模型可处理低风险 prompt refinement，控制逻辑和跨层 Harness 修复才需要强教师；
- 根据失败归因置信度进行 selective escalation，比固定 teacher 或完全自反馈更省成本；
- 强教师生成的经验未必适配弱执行模型，需要加入 executability / adherence 评分。

### 推荐设置

- Student：4B–14B open model；
- Teacher：一个强模型；
- 路由信号：失败类型、归因置信度、历史修复成功率、预估 token cost；
- 对照：student-only、teacher-always、随机 escalation、置信度阈值、学习式 router。

### 研究风险

- 教师调用价格随平台变化；
- teacher 与 student 的 token / latency 难完全公平；
- router 的收益可能依赖任务特定 failure labels。

---

## 7. Gap D：长期经验的删除、冲突与失效治理

### 已有工作覆盖

- EvolveR：经验评分、过滤和经验库规模退化；
- ACE：错误反馈可能污染 playbook；
- From Storage to Experience：强调动态环境和 continual learning；
- Memora：评测失效信息复用并提出 FAMA；
- MemoPilot：环境非平稳时性能下降。

### 仍缺什么

- 工具调用和代码 Agent 中的 forgetting-aware benchmark；
- 经验的 valid-from / valid-until、依赖环境版本和权限范围；
- 冲突经验合并、回滚和删除后的能力保留；
- 删除策略与检索策略的联合优化；
- stale experience 对 activation / adherence 的影响。

### 可检验假设

- 经验项加入有效期、环境签名和来源置信度，可减少过期经验误用；
- 只做相似度检索会优先召回“语义相似但已失效”的经验；
- forgetting-aware retrieval 比定期全量清库更稳健。

### 研究风险

构造真实长期变化成本较高。可先使用可控版本变化：API 参数、数据库 schema、工具权限或规则更新。

---

## 8. Gap E：Harness 写入—检索—激活—遵循—收益链路

### 已有工作覆盖

- Harness Updating：明确 updating 与 benefit 解耦；
- SkillLearnBench：skill quality、trajectory、outcome 多层评测；
- HarnessFix：步骤级归因与 scoped repair；
- ACE：Context 增量更新；
- MemoPilot：针对 frozen player 的可执行 memory。

### 仍缺什么

目前不同论文使用不同日志和术语，缺少统一事件协议：

```text
write
→ retrieve
→ load / activate
→ follow / adhere
→ affect action
→ change outcome
```

没有这条链，难以判断失败是：

- 没写出正确经验；
- 没检索到；
- 没放入上下文；
- 模型看到了但没遵循；
- 遵循了但经验本身无效；
- 最终被其他步骤抵消。

### 可检验假设

- 许多“memory 无效”主要是 activation / adherence 问题；
- stronger solver 提高 adherence，但可能降低可观测 headroom；
- executability-aware memory scoring 比语义相关度更能预测最终收益。

### 推荐产出

一个轻量日志 schema 和自动诊断器，比再提出一种全文 memory 格式更可能形成通用贡献。

---

## 9. Gap F：参数更新与外挂经验的 Equal-Budget 拆分

### 已有工作覆盖

- EvolveR：Experience Base + retrieval + SFT / GRPO；
- Self-Challenging：任务生成 + verifier + SFT / RL；
- MemoPilot：冻结 Player，只训练 updater；
- ACE：完全冻结参数，只更新 Context；
- PACE：冻结 SLM，更新 prompt / control logic。

### 仍缺什么

当方法同时增加数据、rollout、检索和训练时，很难知道收益来自哪里。需要统一比较：

```text
external experience only
parameter update only
auxiliary updater only
combined
```

并在 equal token、equal environment interaction 或 equal wall-clock 下报告 Pareto 曲线。

### 可检验假设

- 低数据阶段外挂经验更高效，数据积累后参数更新更稳定；
- 辅助 updater 适合冻结商业模型，但跨 Player 迁移存在上限；
- combined 方法在同预算下未必优于单一路线，因为维护和检索成本会抵消收益。

### 研究风险

训练预算和推理预算不是同一资源，必须提前定义主预算口径，避免得到无法解释的“公平比较”。

---

## 10. Gap G：成本归一化与能力增长评测

### 已有工作覆盖

- ACE：报告 latency、rollout 和 token cost；
- SE-Agent：分析候选轨迹数和边际收益；
- MLEvolve：明确 12 小时、500 expansion、H200；
- Theory of Agent：强调 epistemic effort；
- When Does Memory Help：指出 memory 可降低轨迹长度而不提高 accuracy。

### 仍缺什么

统一的 capability-per-cost 表达，例如：

- Δsuccess / 1M tokens；
- rescued failures / 100 rollouts；
- Δsuccess / GPU-hour；
- useful memory activations / 1k stored tokens；
- long-term retained gain / update；
- regression-adjusted gain。

还需要区分：

- adaptation cost；
- steady-state inference cost；
- verifier cost；
- environment execution cost；
- maintenance / deletion cost。

### 可检验假设

许多高分 self-evolution 方法在 equal budget 下可能不占优，但会在更长任务流中摊薄前期适配成本。

---

## 11. 候选小课题

## 11.1 课题 A：Token-Budgeted Failure Memory

**优先级：1**  
**周期：6–8 周**  
**目标：B 会级别实验论文 / Findings 风格**

### 核心假设

在固定 memory token 预算下，只保存“关键失败步骤 + 可执行修复 + 适用条件”比完整失败轨迹、成功案例和普通 reflection 获得更高净收益。

### 最小实验

任务：选择两个任务族，例如：

- SQL / 数据库工具任务；
- CLI / API 工具任务。

模型：两个开源规模，例如 7B 与 14B。

Memory 条件：

1. No memory；
2. Success-only examples；
3. Full failed trajectories；
4. Failure reflection；
5. Critical-step failure record；
6. Critical-step record + utility-based eviction。

### Baseline

- no memory；
- raw history；
- reflection memory；
- atomic fact memory；
- success-only retrieval。

### 指标

- task success；
- rescue rate；
- regression rate；
- activation / adherence；
- token-normalized utility；
- trajectory length；
- stale or conflicting memory errors。

### 预算

- 不训练基础模型；
- 1–2 个可本地执行环境；
- 2 个模型；
- 每条件约 100–300 个任务实例；
- 主要成本为 rollout 和 judge / verifier。

### 最大风险

critical-step record 的优势可能只来自更短 Prompt。必须用 equal-token 对照和随机压缩 baseline 排除。

### 最小可发表贡献

- failure memory schema；
- equal-token benchmark protocol；
- write → activation → adherence → rescue 诊断；
- 一个稳定结论：哪些失败值得保存。

---

## 11.2 课题 B：Activation–Adherence Diagnostic for Learned Skills

**优先级：2**  
**周期：4–7 周**  
**目标：诊断 / 评测型短论文**

### 核心假设

自动生成 skill 的最终失败中，相当比例不是 skill 内容错误，而是没有激活或没有遵循；这两类故障随模型能力、上下文长度和 skill 表达方式变化。

### 最小实验

- 选择 15–30 个明确依赖 workflow 的工具任务；
- 准备人工 skill、自动 skill 和扰动 skill；
- 测试 2–3 个模型；
- 记录 retrieve、load、mention、follow、deviation 和 outcome 事件。

### Baseline

- no skill；
- always inject；
- semantic retrieval；
- oracle activation；
- oracle adherence prompt；
- generated skill 与 human skill。

### 指标

- activation precision / recall；
- adherence rate；
- conditional success given activation；
- conditional success given adherence；
- unnecessary activation cost；
- failure attribution accuracy。

### 预算

无需训练；主要是任务运行和轨迹标注。可以先人工标注 100–200 条轨迹建立小型 gold set。

### 最大风险

“遵循”定义可能主观。需要基于可观测 workflow checkpoints，而不是完全依赖 LLM Judge。

### 最小可发表贡献

- 通用事件 schema；
- 自动诊断器；
- 模型能力与 activation / adherence 的经验曲线。

---

## 11.3 课题 C：Selective Teacher Escalation for SLM Self-Evolution

**优先级：3**  
**周期：6–10 周**  
**目标：成本敏感方法论文**

### 核心假设

小模型可以独立处理大多数低风险 Prompt 修订，只有高风险控制逻辑、低置信失败归因或连续失败才需要强教师；选择性升级可保留大部分收益并显著降低成本。

### 最小实验

- Student：一个 7B 左右模型；
- Teacher：一个强模型；
- 两类更新：prompt refinement 与 control-logic / skill update；
- Router 信号：失败类型、归因置信度、连续失败次数、历史更新收益。

### Baseline

- student-only；
- teacher-always；
- random escalation；
- fixed confidence threshold；
- learned lightweight router。

### 指标

- final task success；
- teacher-call rate；
- total tokens / latency / cost；
- accepted update precision；
- regression rate；
- benefit per teacher call。

### 预算

2 个 benchmark、1 个 student、1 个 teacher 即可形成最小研究。重点是路由与验证，不训练大模型。

### 最大风险

teacher-always 可能在任务规模较小时仍很便宜；需要设计足够长的任务流，展示成本差异的累积效应。

### 最小可发表贡献

- risk-aware escalation policy；
- two-timescale update 与 teacher routing 的组合；
- cost–quality Pareto 曲线。

---

## 11.4 课题 D：Forgetting-Aware Experience Base for Tool Agents

**优先级：4**  
**周期：8–12 周**

### 核心假设

给经验记录增加环境版本、有效期、依赖工具和冲突关系，可显著减少 API / schema 变化后的错误复用。

### 最小环境

构造工具版本变化：

- API 参数重命名；
- 数据库 schema 更新；
- 权限策略变化；
- workflow 规则反转。

### 对照

- append-only memory；
- recency retrieval；
- semantic retrieval；
- periodic full reset；
- version-aware retrieval；
- version-aware retrieval + selective forgetting。

### 指标

- current-task success；
- obsolete-memory use rate；
- retention of still-valid experience；
- update cost；
- conflict-resolution accuracy。

### 最大风险

人工构造变化可能缺乏现实性。可先作为 benchmark / evaluation paper，而不是声称解决真实长期 Agent。

---

## 12. 小课题排序

| 课题 | 新颖性 | 实验可控性 | 计算成本 | 1–2 月可行性 | 主要风险 | 综合建议 |
|---|---:|---:|---:|---:|---|---|
| A. Token-Budgeted Failure Memory | 高 | 高 | 中 | 高 | 优势可能只是压缩效应 | 最优先 |
| B. Activation–Adherence Diagnostic | 中高 | 高 | 低–中 | 高 | adherence 标注定义 | 最稳妥 |
| C. Selective Teacher Escalation | 中高 | 中 | 中 | 中高 | 成本优势需长任务流 | 有方法潜力 |
| D. Forgetting-Aware Experience Base | 高 | 中 | 中 | 中 | 环境变化真实性 | 适合后续扩展 |

### 推荐路线

```text
先做 B 的诊断协议
  ↓
用该协议完成 A 的 failure memory 实验
  ↓
再将诊断置信度用于 C 的 teacher escalation
  ↓
最后扩展到 D 的长期失效治理
```

这条路线共享日志 schema、失败归因和评测代码，能减少重复工程投入。

---

## 13. 不建议作为当前小课题的方向

### 13.1 再做一个通用文本经验库

原因：ACE、EvolveR、MemoPilot 和大量 memory 工作已经覆盖；没有明确诊断、预算或长期变化问题时，很难形成新贡献。

### 13.2 只比较不同向量数据库

原因：工程差异容易掩盖真正研究问题，且结果高度依赖 embedding、chunk 和任务分布。

### 13.3 直接训练大型通用 Self-Evolving Agent

原因：预算、数据和评测范围过大，不适合 1–2 个月的小论文。

### 13.4 只报告最终成功率提升

原因：无法解释写入、检索、激活、遵循、成本和回归风险。

### 13.5 把所有失败轨迹直接加入 Prompt

原因：token 成本高，包含噪声和不可迁移状态，无法区分失败信息本身与上下文长度效应。

---

## 14. 下一轮文献调研清单

在正式确定课题前，继续核验：

1. failure trajectory relabeling 是否已有更多同行评审版本；
2. HarnessFix、AgentRx 的代码、数据和许可；
3. SkillLearnBench 的任务与 activation / adherence 标注是否可复用；
4. When Does Memory Help 的实验代码和预算口径；
5. Memora 的长期变化生成方式能否迁移到工具 Agent；
6. PACE 是否报告 teacher-free 条件下的真实 token / wall-clock；
7. 是否已有 equal-budget external-memory vs parameter-update 系统比较。

---

## 15. 维护规则

新增论文或新证据后，更新本地图时：

- 先更新单篇笔记和 `experimental-comparison-data.json`；
- 区分“已有工作”“剩余空白”和“可执行课题”；
- 新工作出现后收窄 gap，而不是保留过时的新颖性表述；
- 每个课题必须保留反证条件和最大风险；
- 成本结论必须说明 token、rollout、wall-clock、硬件或教师调用口径；
- active research stage 必须同步到 `maintenance/roadmap.md` 和 GitHub Issue。
