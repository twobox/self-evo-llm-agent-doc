<!--
metadata:
  title: 'SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents'
  short_title: 'SE-Agent'
  year: 2025
  note_type: '中文读书笔记'
  paper_type: 'method / framework / code agent paper'
  status: 'arXiv v6 submitted on 2025-08-04, last revised on 2025-11-03; NeurIPS 2025 Poster'
  venue: 'NeurIPS 2025 / arXiv'
  arxiv_id: '2508.02085'
  arxiv_url: 'https://arxiv.org/abs/2508.02085'
  pdf_url: 'https://arxiv.org/pdf/2508.02085'
  html_url: 'https://arxiv.org/html/2508.02085'
  code_url: 'https://github.com/JARVIS-Xs/SE-Agent'
  original_code_url: 'https://github.com/JARVIS-Xs/SE-Agent'
  model_url: ''
  authors:
    - 'Jiaye Lin'
    - 'Yifu Guo'
    - 'Yuzhen Han'
    - 'Sen Hu'
    - 'Ziyi Ni'
    - 'Licheng Wang'
    - 'Mingguang Chen'
    - 'Hongzhang Liu'
    - 'Ronghao Chen'
    - 'Yangfan He'
    - 'Daxin Jiang'
    - 'Binxing Jiao'
    - 'Chen Hu'
    - 'Huacan Wang'
  institutions:
    - 'THU / Tsinghua University'
    - 'StepFun'
    - 'UofT / University of Toronto'
    - 'PKU / Peking University'
    - 'UCAS / University of Chinese Academy of Sciences'
    - 'CASIA / Institute of Automation, Chinese Academy of Sciences'
    - 'UCR / University of California, Riverside'
    - 'USYD / University of Sydney'
    - 'UMN / University of Minnesota'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Code Agent'
    - 'Trajectory Optimization'
    - 'Multi-Step Reasoning'
    - 'Test-Time Search'
    - 'SWE-bench Verified'
  tags:
    - 'LLM Agent'
    - 'self-evolution'
    - 'trajectory-level evolution'
    - 'revision'
    - 'recombination'
    - 'refinement'
    - 'SWE-Agent'
    - 'SWE-Search'
    - 'SWE-bench Verified'
  related_notes:
    - 'evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'harness-updating-is-not-harness-benefit.md'
    - 'self-challenging-language-model-agents.md'
  created: '2026-06-07'
  updated: '2026-06-07'
-->

# 《SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents》读书笔记

## 1. 基本信息

- 论文标题：SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents
- arXiv：<https://arxiv.org/abs/2508.02085>
- PDF：<https://arxiv.org/pdf/2508.02085>
- arXiv HTML：<https://arxiv.org/html/2508.02085>
- 代码仓库：<https://github.com/JARVIS-Xs/SE-Agent>
- 项目主页 / 团队信息：<https://quantaalpha.com/>
- 模型权重：暂未找到官方公开模型权重。

这篇论文研究的是：**LLM Agent 在多步推理和工具交互中会产生完整执行轨迹，但很多方法只把轨迹当作一次独立尝试，没有充分利用多条轨迹之间的互补信息。** 作者提出 SE-Agent，把多条 reasoning / acting 轨迹放进一个 trajectory pool，再通过 revision、recombination、refinement 三类操作做测试时轨迹优化。

我理解这篇论文的关键词是：**轨迹级自演化**、**代码修复 Agent**、**测试时搜索 / 优化**、**多轨迹信息融合**。

## 2. 投稿 / 发表状态

- arXiv 页面显示：arXiv:2508.02085，v1 提交时间为 2025-08-04，当前版本为 v6，最后修订时间为 2025-11-03。
- PDF 首页标注：39th Conference on Neural Information Processing Systems，即 NeurIPS 2025。
- GitHub README 的 News 中写到：SE-Agent 被 NeurIPS 2025 接收为 Poster。
- 代码仓库已经公开，README 显示为 MIT License。

因此，这篇文章目前可以看作 **NeurIPS 2025 Poster + arXiv 预印本 + 官方代码已开源**。

## 3. 作者与机构

论文作者为：Jiaye Lin, Yifu Guo, Yuzhen Han, Sen Hu, Ziyi Ni, Licheng Wang, Mingguang Chen, Hongzhang Liu, Ronghao Chen, Yangfan He, Daxin Jiang, Binxing Jiao, Chen Hu, Huacan Wang。

论文首页给出的机构缩写包括：

- THU：Tsinghua University / 清华大学
- StepFun：阶跃星辰
- UofT：University of Toronto / 多伦多大学
- PKU：Peking University / 北京大学
- UCAS：University of Chinese Academy of Sciences / 中国科学院大学
- CASIA：Institute of Automation, Chinese Academy of Sciences / 中国科学院自动化研究所
- UCR：University of California, Riverside / 加州大学河滨分校
- USYD：University of Sydney / 悉尼大学
- UMN：University of Minnesota / 明尼苏达大学

从作者机构看，这是一篇 **高校 + 产业界大模型团队 + AI Agent 研究团队** 的合作论文。论文首页同时给出了 `JARVIS-Xs/SE-Agent` 代码仓库和 `quantaalpha.ai@gmail.com` 联系邮箱。

## 4. 作者背景和研究圈子

这篇论文背后的研究圈子比较值得关注。GitHub README 把 SE-Agent 放在 QuantaAlpha / JARVIS-Xs 生态中，并列提到 RepoMaster、GitTaskBench、SE-Agent 等项目。QuantaAlpha 团队主页将研究方向概括为 CodeAgent、DeepResearch、Agentic RL、Self-Evolving Systems 等。

因此，这篇文章不是单纯做一个 SWE-bench 刷榜技巧，而是处在一个更大的研究线里：

1. **Code Agent**：让 Agent 面向真实代码仓库理解 issue、定位文件、修改代码并通过测试。
2. **Self-Evolving Agent**：不是只采样一次，而是利用历史尝试、轨迹池和反馈继续改进。
3. **Agentic RL / Test-Time Search**：不一定训练模型参数，也可以在测试时通过多轨迹搜索、反思和重组提高任务完成率。
4. **Repo-level Agent Infrastructure**：围绕真实 GitHub 仓库任务构建工具、benchmark 和执行框架。

我暂未逐一找到所有作者的稳定个人主页或完整履历，因此作者背景部分不展开到个人级别，主要依据论文首页机构、GitHub 项目页和 QuantaAlpha 团队主页进行概括。

## 5. 所属研究方向与论文定位

这篇论文属于 **Self-Evolving LLM Agent** 方向，也可以归到 **Code Agent / SWE-bench Agent / Test-Time Trajectory Optimization** 下面。

它和仓库里已有几篇笔记的关系可以这样理解：

- 和 **EvolveR** 相比：EvolveR 更强调经验库、经验自蒸馏和训练 / 强化学习；SE-Agent 更强调测试时对多条执行轨迹做演化式优化。
- 和 **Harness Updating Is Not Harness Benefit** 相比：Harness 论文强调“写出更新”和“用好更新”是两种能力；SE-Agent 更像是在任务求解阶段直接操作轨迹池，绕开一部分长期 harness 使用问题。
- 和 **Self-Challenging Language Model Agents** 相比：Self-Challenging 让 Agent 自己生成可验证训练任务，再训练 executor；SE-Agent 不主要生成训练任务，而是对同一个真实任务的多条求解轨迹做 revision / recombination / refinement。

所以，SE-Agent 的定位可以概括为：**不改模型参数，而是在执行阶段用轨迹级进化机制提升多步 Agent 的求解质量。**

## 6. 核心问题

论文要解决的问题是：

> 对于复杂多步任务，LLM Agent 往往会产生多条 reasoning / acting 轨迹。怎样不只是“多采样几次”，而是让这些轨迹之间相互启发、相互补全，从而得到更好的最终解？

作者认为现有方法有两个主要不足：

1. **轨迹之间被当成相互独立**：例如 MCTS 可以做探索和利用，但往往没有充分建模不同完整轨迹之间的互补关系。
2. **多次采样容易同质化**：即使换温度、换 prompt，模型仍可能围绕高概率路径生成结构相似的解决方案，导致搜索空间没有真正打开。

SE-Agent 的核心想法是：与其只在 token 层、采样层或局部动作层做变化，不如直接在完整轨迹层面做操作，把“这条路径的好步骤”和“另一条路径的好思路”组合起来。

## 7. 方法：SE-Agent 的轨迹级自演化框架

### 7.1 轨迹视角的问题建模

论文把复杂任务环境建模为一个 task-oriented reasoning environment：任务、状态、动作、状态转移和奖励共同构成环境。Agent 的求解过程不是一个孤立答案，而是一条 trajectory：

```text
trajectory = state / action / observation / reasoning 的序列
```

在代码修复任务里，一条轨迹可能包括：阅读 issue、检索文件、查看相关函数、提出假设、修改代码、运行测试、根据错误继续修复等步骤。

这点很重要。因为对 Agent 来说，最终 patch 只是结果，**轨迹中间的错误定位、工具调用、观察结果和修正过程同样包含可复用信息**。

### 7.2 初始轨迹池：先得到多样化尝试

SE-Agent 首先构造一个初始 trajectory pool。论文中主要用两种方式增加多样性：

1. **Multi-Planning Exploration**：通过不同 planning strategies、prompting techniques 和 reasoning approaches 生成不同初始轨迹。
2. **Mutation-Based Diversification**：对已有轨迹做受控变异，让推理步骤、动作选择或中间结论发生变化。

这里的关键不是“采样越多越好”，而是希望轨迹之间在结构和策略上真的不同。

### 7.3 Revision：单条轨迹的反思和修订

Revision 面向单条轨迹。它先对某条轨迹做 self-reflection，分析其中的逻辑漏洞、无效步骤、循环推理、遗漏信息和潜在改进点，然后生成修订后的轨迹。

我的理解是，revision 相当于让 Agent 对一次失败或不够好的尝试做“复盘”：

- 哪一步定位方向错了？
- 哪个工具调用没有带来有效信息？
- 哪个假设太早收敛？
- 是否应该换一个文件、函数或测试切入口？

它的作用是为后续 recombination 提供更高质量、更有差异的候选轨迹。

### 7.4 Recombination：多条轨迹之间的信息重组

Recombination 是这篇论文最核心的部分之一。论文把它拆成三类策略：

1. **Crossover**：从不同轨迹中挑选表现较好的片段，组合成一条 hybrid trajectory。
2. **Transfer**：把成功轨迹中的策略或知识迁移到较弱轨迹中。
3. **Restructuring**：从整个 trajectory pool 中抽象出全局结构，重新组织一条新的轨迹。

这一步很像遗传算法里的交叉和重组，但对象不是基因串，而是 Agent 的完整问题解决过程。

我觉得这比普通 self-reflection 更进一步。普通反思通常只让一条失败轨迹自己改自己；SE-Agent 允许不同轨迹之间互相借鉴。例如：

- A 轨迹找到了正确文件，但修复方案不对；
- B 轨迹没有定位到正确文件，但测试分析做得好；
- C 轨迹的 patch 结构更稳，但缺少边界情况处理；

recombination 试图把这些局部优势组合成更完整的解决方案。

### 7.5 Refinement：评价、筛选和收敛

Refinement 负责最终优化和选择。论文设计了多维 reward / evaluation function，包括：

- TaskCompletion：任务完成情况，例如是否产生非空 patch、是否有足够代码编辑步骤、轨迹长度是否合理；
- ReasoningQuality：推理过程是否连贯、深入、稳健；
- Efficiency：步骤数量和资源使用是否高效。

其中 TaskCompletion 又结合 rule-based AutoEval 和 LLM-based ExpertEval。也就是说，它不是完全依赖 LLM judge，而是把结构性规则和模型评价结合起来。

最后，SE-Agent 会在候选轨迹中保留高分轨迹，同时考虑轨迹多样性，直到达到预设迭代次数或收敛条件。

## 8. 实验设计

### 8.1 Benchmark

主实验使用 **SWE-bench Verified**。论文说明该 benchmark 包含 500 个真实 GitHub issue，每个样本包含自然语言 issue 描述和对应代码仓库，模型需要生成 patch，并通过开发者写的单元测试验证修复是否正确。

### 8.2 评价指标

论文主要使用：

- **Pass@1 / resolution rate**：第一次尝试是否解决问题。
- **Pass@5**：五次尝试内是否找到正确解。

### 8.3 Baseline 和模型

论文主要与两个框架比较：

- **SWE-Agent**：CodeAct-based baseline。
- **SWE-Search**：MCTS-based baseline。

评测模型包括：

- DeepSeek-V3-0324
- Qwen-2.5-72b-Instruct
- Llama-3.1-70b-Instruct
- GPT-4o
- Claude-3.7-Sonnet

实现细节中，SE-Agent 默认候选轨迹数为 10，先用 5 种 planning strategy 生成初始轨迹，再做 reflection / revision、recombination 和 refinement。开源模型在 NVIDIA A100 80GB 上本地运行，闭源模型通过官方 API 调用。

## 9. 主要实验结果

论文 Table 1 给出的 SWE-bench Verified 结果如下：

| LLM | SWE-Agent Pass@1 | SWE-Agent Pass@5 | SWE-Search Pass@1 | SWE-Search Pass@5 | SE-Agent Pass@1 | SE-Agent Pass@5 |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek-V3-0324 | 31.6% | 35.8% | 39.4% | 41.8% | **54.8%** | **58.4%** |
| Qwen-2.5-72b-Instruct | 18.8% | 20.6% | 23.4% | 26.2% | **38.8%** | **42.4%** |
| Llama-3.1-70b-Instruct | 15.4% | 17.8% | 21.8% | 23.6% | **32.6%** | **35.2%** |
| GPT-4o | 22.4% | 25.4% | 32.6% | 35.8% | **40.4%** | **44.8%** |
| Claude-3.7-Sonnet | 40.6% | 43.2% | 47.4% | 50.6% | **61.2%** | **63.6%** |

论文摘要和首页图还提到，在 Claude-4-Sonnet + 最新 SWE-Agent 对齐设置下，SE-Agent 在 SWE-bench Verified 上达到 **80.0%** resolution rate。这个数字和 Table 1 中 Claude-3.7-Sonnet 的 61.2% 不是同一个模型设置，阅读时要区分。

### 9.1 Ablation

论文做了三个消融版本：

- w/o Revision：去掉 revision；
- w/o Recombination：去掉 recombination；
- w/o All：不使用轨迹优化操作。

结果显示，去掉任一模块都会导致 Pass@1 下降。其中 revision 的作用比较关键，因为它提供了更加多样化的候选轨迹，后面的 recombination 才有材料可组合。

### 9.2 轨迹数和成本分析

论文还分析了候选轨迹数量和最大 API cost。结论大致是：

- SE-Agent 在约 10 条候选轨迹时已经接近较优表现；
- 随着候选轨迹增加，收益会继续上升但边际收益变小；
- 在相同成本预算下，SE-Agent 相比 SWE-Agent 和 SWE-Search 仍表现更好。

这说明它不是单纯靠无限堆采样次数，而是希望用更有效的轨迹组合提高搜索效率。

### 9.3 Case Study

论文通过一个代码修复案例说明：传统 ReAct / MCTS agent 可能会困在局部搜索路径里，例如过度相信某个栈跟踪位置、反复编辑局部代码，忽略真正根因。SE-Agent 通过多条轨迹之间的迭代交互和重组，有机会跳出这种局部视角。

## 10. 主要结论

我把论文结论概括为四点：

1. **多条轨迹不是独立样本，而是一组可组合的经验资源。**
2. **显式操作完整轨迹，比只调采样温度或随机多跑几次更有可能扩大搜索空间。**
3. **Revision、Recombination、Refinement 三个环节都有作用，其中 revision 提供多样性，recombination 提供跨轨迹信息融合，refinement 负责筛选和压缩。**
4. **在 SWE-bench Verified 这种真实代码修复任务上，轨迹级自演化能显著提升 SWE-Agent 类框架的成功率。**

这篇论文的实验重点不是证明某个 base model 更强，而是证明：**把同一个 base agent 包装进 trajectory-level self-evolution 框架后，多种模型都能获得收益。**

## 11. 工程启发

### 11.1 Agent 系统要保存完整轨迹，而不只是最终答案

如果做自演化 Agent，日志不能只保存最终回答。更有价值的是：

- 每一步 action；
- 每一步 observation；
- 中间 reasoning / plan；
- 失败时的错误信息；
- patch / test result / tool output；
- 最终 reward 或验证结果。

没有这些结构化轨迹，就很难做 revision、recombination 和 refinement。

### 11.2 多采样不等于多样性

工程上常见做法是 temperature 调高、多跑几次，然后投票或选择最优。但 SE-Agent 提醒我们：多跑几次可能只是得到表面不同、结构相似的轨迹。

更有用的做法是人为设计不同的 plan strategy、搜索方向、工具使用策略，再让轨迹之间互相迁移信息。

### 11.3 评价函数要混合硬规则和模型判断

在代码任务中，硬规则很重要，例如：

- 是否生成 patch；
- 是否修改了相关文件；
- 是否运行测试；
- 是否通过单元测试；
- 轨迹长度是否异常。

但仅靠硬规则可能看不出推理质量，所以可以补充 LLM judge。比较稳妥的工程路线是：**硬验证优先，LLM judge 辅助解释和排序**。

### 11.4 SE-Agent 更像一个外层优化器

它不要求重新训练 base model，因此比较适合作为已有 Code Agent 的外层模块：

```text
base agent 生成多条轨迹
→ 轨迹压缩 / 结构化
→ revision / recombination / refinement
→ 选择最高分轨迹或 patch
→ 验证并输出
```

这对工程落地有吸引力，因为它可以先不动模型参数，只增加一层测试时搜索和轨迹管理系统。

## 12. 局限性

1. **成本仍然不低**：多轨迹生成、反思、重组、LLM-based evaluation 都会增加 token 和 API 成本。
2. **主要验证在代码修复任务上**：论文虽然从一般 multi-step reasoning 角度建模，但主实验集中在 SWE-bench Verified，迁移到网页操作、数据库操作、机器人规划等环境还需要更多验证。
3. **评价函数仍有启发式成分**：TaskCompletion、ReasoningQuality、Efficiency 的权重和 LLM judge 可能影响筛选结果。
4. **不是参数级自我提升**：SE-Agent 更像测试时轨迹优化。它能提升当前任务求解，但不一定自动沉淀成长期模型能力或长期 memory。
5. **依赖底层 agent 和环境质量**：如果基础工具链、代码执行沙箱、测试环境、repository setup 不稳定，轨迹优化也会被噪声影响。
6. **对失败轨迹的压缩和表示很关键**：如果轨迹太长、压缩过度或关键信息丢失，recombination 可能组合不到真正有用的内容。

## 13. 我的理解与总结

我觉得 SE-Agent 的价值不只是“把 SWE-bench 分数做高”，而是提出了一个很有启发性的视角：**Agent 的一次执行过程本身就是可优化对象。**

传统 LLM 优化常关注三个层面：

1. 参数层：SFT、RL、DPO、GRPO；
2. Prompt / harness 层：改提示词、工具、memory、workflow；
3. 采样层：多采样、投票、best-of-N。

SE-Agent 则把重点放在第四层：

> 轨迹层：把完整的“尝试过程”当成对象，进行反思、变异、组合、筛选。

这个思路很适合复杂 Agent 任务，因为复杂任务的失败通常不是最后一句话错了，而是中间某一步定位错了、工具用错了、信息没看全、过早收敛到错误假设。轨迹层方法能直接处理这些过程性错误。

不过，我也认为要谨慎理解“self-evolution”这个词。SE-Agent 的 self-evolution 主要发生在 **单个任务或一批任务的测试时轨迹池内部**，并不等于模型长期能力自动变强。它更接近：

```text
多条尝试轨迹 + 反思 + 遗传式组合 + 评价选择 = 更强的测试时问题求解器
```

如果后续把这种轨迹演化结果再沉淀成经验库、训练数据或可复用 skill，就可能和 EvolveR、Self-Challenging、Harness Updating 等方向进一步连接起来。

## 14. 参考信息

- arXiv abs：<https://arxiv.org/abs/2508.02085>
- arXiv PDF：<https://arxiv.org/pdf/2508.02085>
- 官方代码仓库：<https://github.com/JARVIS-Xs/SE-Agent>
- QuantaAlpha 团队主页：<https://quantaalpha.com/>
- SWE-bench Verified：<https://www.swebench.com/>
