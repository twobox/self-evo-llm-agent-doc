<!--
metadata:
  title: 'Self-Challenging Language Model Agents'
  short_title: 'Self-Challenging Agents'
  year: 2025
  note_type: '中文读书笔记'
  paper_type: 'method / framework / agent training paper'
  status: 'arXiv v1 submitted on 2025-06-02; NeurIPS 2025 poster; OpenReview published on 2025-09-18 and last modified on 2026-04-21'
  venue: 'NeurIPS 2025 / arXiv / OpenReview'
  arxiv_id: '2506.01716'
  arxiv_url: 'https://arxiv.org/abs/2506.01716'
  pdf_url: 'https://arxiv.org/pdf/2506.01716'
  html_url: 'https://arxiv.org/html/2506.01716v1'
  code_url: ''
  original_code_url: ''
  model_url: ''
  authors:
    - 'Yifei Zhou'
    - 'Sergey Levine'
    - 'Jason Weston'
    - 'Xian Li'
    - 'Sainbayar Sukhbaatar'
  institutions:
    - 'UC Berkeley'
    - 'FAIR at Meta / Meta AI'
  topics:
    - 'Self-Evolving LLM Agent'
    - 'Self-Challenging Agent'
    - 'Tool-use Agent'
    - 'RL for Agent'
    - 'Synthetic Task Generation'
    - 'Code-as-Task'
  tags:
    - 'LLM Agent'
    - 'self-improvement'
    - 'multi-turn tool-use'
    - 'reinforcement learning'
    - 'verifiable reward'
    - 'M3ToolEval'
    - 'TauBench'
  related_notes:
    - 'evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md'
    - 'harness-updating-is-not-harness-benefit.md'
  created: '2026-06-06'
  updated: '2026-06-06'
-->

# 《Self-Challenging Language Model Agents》读书笔记

## 1. 基本信息

- 论文标题：Self-Challenging Language Model Agents
- arXiv：<https://arxiv.org/abs/2506.01716>
- PDF：<https://arxiv.org/pdf/2506.01716>
- arXiv HTML：<https://arxiv.org/html/2506.01716v1>
- OpenReview / NeurIPS 页面：<https://openreview.net/forum?id=9yusqX9DpR>
- Hugging Face Papers：<https://huggingface.co/papers/2506.01716>
- 代码仓库：暂未找到官方公开代码仓库。
- 模型权重：暂未找到官方公开模型权重；Hugging Face Papers 页面当前也没有关联模型记录。

这篇论文关注一个很关键的问题：**LLM Agent 想靠强化学习提升多轮工具使用能力，但训练任务、工具环境和评价标准通常需要人工构造，成本很高，而且难以规模化。** 作者提出 Self-Challenging Agent（SCA）框架，让 Agent 自己生成高质量、可验证的任务，再用这些任务训练自己。

## 2. 投稿 / 发表状态

- arXiv 版本：arXiv:2506.01716，v1 提交时间为 2025-06-02。
- 会议状态：OpenReview 页面显示为 **NeurIPS 2025 poster**。
- OpenReview 信息：Published: 18 Sept 2025，Last Modified: 21 Apr 2026。
- 许可信息：OpenReview 页面显示 CC BY 4.0。
- 伦理审查：OpenReview 页面显示 Flagged For Ethics Review: true。

## 3. 作者与机构

论文作者为：

- Yifei Zhou：UC Berkeley
- Sergey Levine：UC Berkeley
- Jason Weston：FAIR at Meta
- Xian Li：FAIR at Meta
- Sainbayar Sukhbaatar：FAIR at Meta

论文首页脚注说明该工作完成于 FAIR at Meta，并标注 Xian Li 与 Sainbayar Sukhbaatar 为 equal advising。

## 4. 作者背景和研究圈子

这篇文章的作者组合比较值得关注，基本可以看成 **Berkeley RL / Agent 方向 + Meta FAIR LLM / NLP / Agent 方向** 的合作。

- Yifei Zhou 近年的论文与 LLM Agent、自动化任务发现、多轮 RL、互联网 Agent 等方向关系很密切。论文参考文献中也能看到他参与的 PAE、ARChER、SWEET-RL 等相关工作。这说明本文不是孤立提出一个技巧，而是在一条“Agent 自动生成任务 / 自动改进”的研究线上继续推进。
- Sergey Levine 是 UC Berkeley EECS 教授，研究重点包括 autonomous agents、robotics、decision making、deep reinforcement learning 等。他的研究背景使本文的“通过环境交互和奖励学习提升 Agent 能力”的思路带有明显的 RL 和自主智能体色彩。
- Jason Weston、Xian Li、Sainbayar Sukhbaatar 都来自 Meta / FAIR 相关研究圈子，长期关注 NLP、语言模型、对话、推理、LLM 训练与 Agent 学习。Xian Li 的 OpenReview 资料显示其方向包括 deep learning、natural language processing、machine learning、machine translation；Sainbayar Sukhbaatar 的资料显示其为 Meta AI Research Scientist，并与多个 LLM reasoning / preference optimization / agent learning 工作有关。

从圈子上看，这篇论文不是单纯做 benchmark 提升，而是把三个方向结合起来：

1. 强化学习训练 Agent；
2. 自动生成可训练任务；
3. 用代码形式的验证器把奖励信号做得更可靠。

## 5. 所属研究方向与论文定位

这篇论文属于 **Self-Evolving / Self-Improving LLM Agent** 方向，也可以放在 **RL for Tool-use Agent** 和 **Synthetic Task Generation for Agents** 下面。

它和一些只做“经验记忆 / 反思总结”的自进化 Agent 不一样。本文的核心不是让 Agent 写自然语言反思，而是让 Agent **自己提出任务、自己给出验证函数、自己产生训练数据，然后用 RL 或蒸馏更新执行模型**。

我理解它的定位是：

- 不是提出一个新的大模型结构；
- 不是单纯设计一个 benchmark；
- 而是提出一个训练闭环：**任务生成 → 任务过滤 → 轨迹采样 → 强化学习 / 蒸馏 → 测试泛化**。

这对后续做 LLM Agent 自演化很重要，因为很多 Agent 系统真正卡住的不是模型会不会调用一次工具，而是缺少大量高质量、多样、可自动判分的训练任务。

## 6. 核心问题

论文要解决的问题可以概括为：

> 在没有人工任务集和人工评价标准的情况下，LLM Agent 能不能自己生成足够高质量的多轮工具使用任务，并利用这些任务训练自己？

这里有三个难点：

1. **任务必须可行**：Agent 生成的任务不能是环境里根本做不到的事情。
2. **任务必须可验证**：训练 RL 需要 reward，不能完全依赖另一个 LLM 主观判断。
3. **任务必须有难度**：如果生成的任务太简单，模型学不到真正有用的工具使用策略。

论文认为，以前一些自动任务生成方法容易停留在“根据初始说明生成任务”的层面，没有充分探索环境，也没有可靠验证器。因此在部分可观测、工具丰富的环境中，任务质量会明显下降。

## 7. 方法：Self-Challenging Agent 与 Code-as-Task

本文方法可以分成两个角色。

### 7.1 Task Challenger：先当“出题人”

Agent 首先扮演 challenger。它不是直接凭空写一个任务，而是先和工具环境交互，了解工具能做什么、隐藏状态是什么、哪些目标可实现，然后生成一个任务。

这一步很像人类标注员设计任务：先试用工具，再构造一个既可完成、又能考察能力的问题。

### 7.2 Code-as-Task：用代码定义任务和验证器

论文最关键的设计是 Code-as-Task（CaT）。一个 CaT 任务包含四个部分：

1. instruction：给 executor 的自然语言任务说明；
2. verification function：验证最终环境状态或答案是否正确的函数；
3. example solution：一个应该能通过验证器的示例解法；
4. failure cases：若干应该不能通过验证器的失败样例。

这样做的好处是，任务不只是“文字说明”，而是带有可执行检查逻辑。系统会自动过滤任务：示例解法必须通过验证函数，失败样例不能通过验证函数。只有满足这些条件的任务才会进入训练。

这个设计解决了一个非常实际的问题：如果只让 LLM 生成任务，很容易出现任务不可行、验证器太宽松、奖励误判等问题。CaT 用 example solution 和 failure cases 把任务质量约束住。

### 7.3 Task Executor：再当“解题人”

生成并过滤出高质量 CaT 任务后，Agent 再切换到 executor 角色。这个阶段可以理解为：**把 challenger 造出来的“可验证练习题”变成训练样本，再用这些样本更新执行模型。**

在标准 LLM Agent 设置中，executor 每一步会根据当前上下文输出一个动作。这个动作可以是一段调用工具 API 的 Python 代码，也可以是向用户发出的询问。环境执行动作后，会返回 observation，例如工具返回值、数据库查询结果、网页内容，或者模拟用户的回复。这个 observation 会继续追加到上下文里，供模型决定下一步动作。等 Agent 认为任务完成后，系统运行 CaT 里携带的 verification function，根据最终环境状态和最终回答给出 0/1 reward。

因此，executor 学到的不是单步问答能力，而是完整的多轮行为链条：

1. 读懂 instruction 和当前环境说明；
2. 判断需要调用哪些工具；
3. 根据工具返回结果继续规划；
4. 必要时向用户追问；
5. 修改环境状态或生成最终答案；
6. 最后由 verification function 判断是否成功。

论文主要讨论了 executor 的两种训练用法。

#### 7.3.1 Self-improvement：自己出题，自己做题，自己根据验证器学习

Self-improvement 是更“自演化”的设置。这里 challenger 和 executor 都是同一个 Llama-3.1-8B-Instruct。整体流程是：

1. Llama-3.1-8B 先作为 challenger 生成 CaT 任务；
2. 系统用 example solution 和 failure cases 过滤掉质量差的任务；
3. 同一个 Llama-3.1-8B 再作为 executor，在这些任务上采样多轮 rollout trajectories；
4. 每条轨迹完成后，用任务自带的 verification function 打 0/1 分；
5. 用成功轨迹来微调 executor policy。

论文中 self-improvement 的主实验采用 one-step REINFORCE。因为 reward 是稀疏的 0/1 outcome reward，所以它在实现效果上接近 Rejection Fine-Tuning：失败轨迹 reward 为 0，基本不提供正向学习信号；成功轨迹 reward 为 1，被当成“好示范”拿来训练。换句话说，这里所谓 RL 并不是复杂的长程 credit assignment，而更像是：**模型多尝试几次，把通过验证器的解题轨迹筛出来，再对这些成功轨迹做监督微调。**

这个设计有一个重要优点：工程上相对简单。它不需要人工标注成功/失败，也不需要另一个 LLM 当 judge，只要验证函数能跑，就可以自动产生 reward。缺点是它比较依赖成功轨迹的数量。如果基础模型太弱，生成的大量 rollout 都失败，那么可用于训练的正样本就会比较少。

#### 7.3.2 Distillation：弱模型出题，强模型做题，再教回弱模型

Distillation 是另一种用法，目标不是完全自我提升，而是把强模型在某个工具环境里的能力自动蒸馏到弱模型中。

本文的设置是：

1. 仍然使用 Llama-3.1-8B 作为 challenger 生成 CaT 任务；
2. 过滤后得到高质量 synthetic tasks；
3. 使用更强的 Llama-3.1-70B-Instruct 作为 teacher executor，在这些任务上采样解题轨迹；
4. 用这些 teacher trajectories 对 Llama-3.1-8B student 做 SFT；
5. 最后测试 student 在真实 benchmark 任务上的泛化能力。

这里的关键点是：训练数据不来自人工任务，也不来自人工示范，而是由“弱模型生成任务 + 强模型执行任务”自动构造出来。这样做的工程意义很明显：如果 70B 模型太慢、太贵，不适合线上部署，就可以先让它在自动生成的任务环境中产生轨迹，再把该环境里的工具使用能力压缩到 8B 模型里。

一个有意思的细节是，论文发现 distillation 时不一定只用成功轨迹。附录实验显示，在 teacher 明显强于 student 的情况下，把成功和失败轨迹都用于蒸馏，效果往往比只用成功轨迹更好。作者的解释是：即使强模型没有完成任务，它的失败轨迹中也可能包含有价值的信息，例如如何探索环境、如何发现错误、如何修正思路。这一点和 self-improvement 不同：self-improvement 主要依赖成功轨迹；distillation 可以从强模型的失败过程里学到一些中间经验。

#### 7.3.3 Executor 训练真正学到的是什么

我理解 executor 阶段学到的能力主要不是“记住某个具体任务答案”，而是学习一类工具环境中的操作模式。例如：

- 在 Calculation 环境中，学会把自然语言问题拆成多步工具调用；
- 在 Web Browsing 环境中，学会边浏览边提取信息；
- 在 Retail 环境中，学会查询订单、确认用户身份、退货或换货；
- 在 Airline 环境中，学会查询航班、改签、订票以及处理用户约束。

所以 executor 的训练价值在于：通过大量 synthetic tasks，让模型形成对工具 API、环境状态、用户交互流程和验证目标的熟悉度。测试时虽然任务不是训练时的同一个任务，但只要工具使用模式相似，模型就可能迁移。

#### 7.3.4 Offline RL 与 Online RL 的区别

论文主实验用的是 offline rollout 方式：先生成一批任务和轨迹，再用这些固定轨迹训练。每种设置生成 800 个 synthetic tasks 和 12k 条 offline rollout trajectories。这种方式比较稳定、成本可控，也容易复现。

论文还做了不同 RL 算法的消融。结果显示，在 Calculation 环境中，Rejection Fine-Tuning 和 DPO 这类 offline 方法已经能带来明显提升；PPO、GRPO 等 online RL 可以进一步提高表现，但代价是工程复杂度和不稳定性更高。论文特别提到，如果 GRPO 没有仔细调参，训练后期性能甚至可能突然掉到 0。

因此，从工程角度看，executor 训练可以分成两个层级：

- **先用 Rejection Fine-Tuning / SFT 跑通闭环**：任务生成、验证器、轨迹采样、成功轨迹训练；
- **再考虑 PPO / GRPO 等在线 RL**：可能更强，但需要更复杂的采样、训练和稳定性控制。

#### 7.3.5 和普通 SFT 数据训练的区别

这部分容易误解。SCA 的 executor 训练看起来像 SFT，但它和普通 SFT 数据集有两个区别：

1. 训练任务不是人工提前写好的，而是 challenger 在环境中探索后生成的；
2. 轨迹是否能进入训练，不靠人工判断，而靠 verification function 自动筛选。

所以这篇论文的重点不是“又做了一次 SFT”，而是提出了一条自动产生 SFT/RL 数据的管线。对 self-evolving agent 来说，这个意义更大：Agent 不只是从已有数据学习，而是参与构造自己的训练任务和训练反馈。

## 8. 实验设计

实验覆盖两个多轮工具使用 benchmark、四个环境：

- M3ToolEval：Calculation、Web Browsing；
- TauBench：Retail、Airline。

模型和训练设置：

- 基础模型：Llama-3.1-8B-Instruct；
- 蒸馏教师模型：Llama-3.1-70B-Instruct；
- 对照模型：GPT-4o、Llama-3.1-70B、Llama-3.1-8B、PAE；
- 数据规模：每种设置生成 800 个 synthetic tasks，采样 12k 条 offline rollout trajectories；
- 评价指标：Pass@1、Pass@4。

PAE 是重要 baseline。论文强调 SCA 和 PAE 的差别主要有三点：

1. PAE 直接根据初始观察生成任务，而 SCA 的 challenger 会主动探索环境后再生成任务；
2. PAE 主要生成 instruction，而 SCA 的 CaT 包含 instruction、verification function、example solution、failure cases；
3. PAE 用模型作为 judge，而 SCA 依赖可执行验证函数给 reward。

## 9. 主要结论

论文报告的结果可以总结为以下几点。

第一，在 self-improvement 设置下，SCA 让 Llama-3.1-8B-Instruct 的平均 Pass@1 从 12.0 提升到 23.5，平均 Pass@4 从 27.9 提升到 41.3。也就是说，完全依赖自生成任务，仍然能实现接近翻倍的平均成功率提升。

第二，在 distillation 设置下，Llama-3.1-8B-SCA 的平均 Pass@1 达到 32.2，平均 Pass@4 达到 56.8，相比原始 Llama-3.1-8B 的 12.0 / 27.9 有明显提升。

第三，SCA 在部分可观测环境里比 PAE 更有优势。原因是 challenger 会先探索环境，生成更具体、更可验证的任务，而不是只看初始 API 文档就出题。

第四，CaT 的组件确实有作用。论文的人类标注分析显示，加入 example solution 可以减少不可行任务，但可能放大“验证器过宽松”的 false positive；加入 failure cases 后，可以进一步过滤掉这类错误奖励。

第五，在线 RL 可能带来更高收益，但工程代价更大。论文在 Calculation 环境中发现，PPO / GRPO 等在线 RL 能进一步提高表现，但也更不稳定，对超参数和基础设施要求更高。

## 10. 工程启发

这篇论文对做 Agent 系统有几个很直接的启发。

### 10.1 任务生成不能只生成 instruction

很多自动数据生成流程只让模型生成“题目文本”。这篇论文提醒我们，对于 Agent 训练来说，题目文本远远不够，还需要：

- 可执行验证器；
- 正例解法；
- 反例样例；
- 自动过滤机制。

这其实可以借鉴到很多工程场景。例如做数据库 Agent、运维 Agent、工具调用 Agent 时，可以让模型生成“任务 + checker + 正例 + 反例”，而不是只生成 prompt。

### 10.2 Agent 出题前应该先探索环境

SCA 的 challenger 不是静态生成任务，而是先调用工具、观察环境，再提出任务。这一点很重要。对于真实业务系统，API 文档往往不能完全说明环境状态，只有主动调用工具才能知道哪些任务可行。

### 10.3 训练数据质量比数量更关键

论文的 scaling 分析说明，只增加每个任务的轨迹数不一定能提升泛化；如果任务覆盖度不够，训练集上变好也可能无法迁移到测试集。对工程系统来说，应该优先扩大任务类型和环境覆盖，而不是只在少数任务上反复采样。

### 10.4 可验证 reward 是 LLM Agent RL 的关键资产

SCA 能工作，一个核心原因是它把 reward 绑定到 verification function。这个思路比“让另一个 LLM 打分”更可靠，但前提是任务领域必须能写出可执行检查逻辑。因此它很适合工具调用、数据库修改、代码执行、表格计算、网页导航等场景。

## 11. 局限性

论文自己也指出了几个限制。

1. **CaT 仍然不能完全避免 false negative**：有些任务指令语义不完整，比如“帮我退掉最近的订单”，但没有说明退哪一个订单，这类问题很难仅靠代码检查发现。
2. **SCA 生成任务和 oracle 任务之间仍有差距**：附录中对比了 SCA synthetic tasks 和人工构造的 oracle tasks，SCA 虽然有效，但任务质量还没有达到人工高质量任务水平。
3. **环境泛化能力有限**：论文发现 SCA 主要提升的是环境特定技能，例如某个工具的参数格式、某类环境的信息获取方式，而不是明显提升通用 Agent 能力。
4. **依赖可执行验证环境**：CaT 很适合有状态数据库、代码执行、工具 API 等场景，但对于开放式写作、主观判断、复杂语义偏好任务，验证函数并不好写。
5. **在线 RL 工程复杂度高**：PPO / GRPO 可能更强，但训练稳定性、采样效率、基础设施成本都是现实问题。

## 12. 我的理解与总结

我觉得这篇论文最值得学习的地方，不是“把某个 benchmark 分数提高了多少”，而是它提出了一种很清晰的自演化训练闭环：

> Agent 先探索环境，生成可验证任务；系统用代码检查任务质量；Agent 再基于这些任务训练自己。

这比单纯“让模型反思一下”更接近真正可落地的自改进系统。因为它把自改进拆成了几个可以工程化检查的环节：任务是否可行、验证器是否能运行、正例是否通过、反例是否失败、轨迹是否成功。

从 self-evolving agent 的角度看，它补上了一个关键环节：**经验或记忆只是学习材料的一种形式，而任务生成和 reward 构造同样是自演化系统的核心能力。** 如果一个 Agent 能持续生成新的可验证任务，它就不只是“记住过去经验”，而是开始具备“主动制造训练信号”的能力。

不过，这篇论文也说明自演化还没有完全解决。SCA 更像是第一步：它能在特定工具环境中提高能力，但还没有证明可以跨环境形成通用 Agent 能力。后续更重要的问题可能是：如何让 challenger 生成更抽象、更跨环境、更接近真实需求的任务；以及如何在没有明确代码验证器的开放任务中构造可靠 reward。

## 13. 参考链接

- arXiv 页面：<https://arxiv.org/abs/2506.01716>
- PDF：<https://arxiv.org/pdf/2506.01716>
- arXiv HTML：<https://arxiv.org/html/2506.01716v1>
- OpenReview / NeurIPS 页面：<https://openreview.net/forum?id=9yusqX9DpR>
- Hugging Face Papers：<https://huggingface.co/papers/2506.01716>
