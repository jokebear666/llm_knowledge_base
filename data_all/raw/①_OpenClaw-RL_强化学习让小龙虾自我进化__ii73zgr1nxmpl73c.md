# ① OpenClaw-RL:强化学习让小龙虾自我进化

<!-- source: yuque://zhongxian-iiot9/hlyypb/ii73zgr1nxmpl73c -->

:::color3
**简介：**本文介绍 OpenClaw-RL 项目，该项目提出了一套用于**<font style="color:#ED740C;">训练类 OpenClaw 通用智能体的在线强化学习基础设施，使大语言模型能够通过与环境的交互实现“边聊边学”</font>**。

**paper：**[**OpenClaw-RL: Train Any Agent Simply by Talking**](https://arxiv.org/pdf/2603.10165)

**code：**[**https://github.com/Gen-Verse/OpenClaw-RL**](https://github.com/Gen-Verse/OpenClaw-RL)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044856820-6a43c23a-605e-4ea4-ac0a-cb93d492ba07.png)

:::color5
**<font style="color:#601bde;">1. 项目概述与核心理念 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">OpenClaw-RL 是一个旨在训练类 OpenClaw（小龙虾）通用智能体的在线强化学习基础设施。</font>**

尽管名称上与当前热门的 OpenClaw 相似，但两者并无直接关联。该项目的核心理念在于，无论底层的策略模型采用何种大语言模型（LLM），只要其需要通过对话或命令行与环境进行交互，这套框架便能使其在交互过程中持续学习与进化。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044878470-a99cdc74-3528-4a38-9408-94619bf27625.png)

![](https://cdn.nlark.com/yuque/0/2026/webp/29769680/1775043686960-ec5ae4c7-6599-4b59-898e-3c27dca3a3f4.webp)

# **一、背景：LLM + RL 的痛点**
:::color3
**简介：**当前主流的 LLM + RL 路线（如 RLHF 和 RLVR）在应对 Agent 场景时存在离线依赖、领域受限以及长序列信用分配等局限性，**<font style="color:#ED740C;">OpenClaw-RL 试图通过在线交互反馈解决这些痛点</font>**。

:::

:::color5
**<font style="color:#601bde;">1. 当前 LLM 演变为 Agent 的挑战 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">将大语言模型（LLM）演变为能够在真实环境中自主规划、调用工具、操作软件的智能体（Agent）是当前 AI 行业的热门方向。</font>**实现这一目标不仅依赖于应用层的架构设计和上下文工程（Context Engineering），强化学习（RL）后训练同样至关重要。然而，目前主流的 LLM + RL 路线在应用于 Agent 场景时暴露出明显的局限性：

+ **RLHF（基于人类反馈的强化学习）：** 以 InstructGPT 为代表的范式虽然取得了巨大成功，但其本质上属于**离线**方法。它高度依赖预先收集的静态数据集和成本高昂的人工偏好标注。此外，基于标量的奖励模型（Reward Model）通常只能对整个回答提供粗粒度的全局评分。
+ **RLVR（基于可验证奖励的强化学习）：** 以 DeepSeek-R1 为代表，通过测试用例（Code）或规则引擎（Math）提供绝对客观的奖励。该方法大幅降低了数据获取成本，但其应用范围被严格限制在**具有明确规则边界的领域**。对于开放式的 GUI 交互、终端报错或用户的模糊对话，RLVR 难以直接适用。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775046609003-ab715b62-bf26-44f3-b46f-4199d302b323.png)

:::color5
**<font style="color:#601bde;">2. 长序列信用分配难题与 OpenClaw-RL 的应对思路</font>**

:::

**<font style="color:#74B602;">除了上述局限，强化学习在 Agent 场景中还面临长序列（Long-horizon）的信用分配难题。</font>**

例如，当 Agent 尝试修复一个 GitHub Issue 时，它可能需要浏览仓库、修改代码、运行测试，最终终端抛出报错。在这一系列长达几十步的交互中，传统的强化学习只能在任务彻底结束时提供稀疏的惩罚信号，模型难以准确识别导致失败的具体步骤，从而难以学习到实质性的策略改进。

针对这一痛点，研究者们开始探索：**Agent 在环境中的每一次交互反馈（如用户的追问、终端的报错提示），是否可以直接转化为训练信号？**

<font style="background-color:#FBDFEF;">OpenClaw-RL 正是基于这一思路的代表性工作。它提出了一种系统级的设计，旨在让模型在实际应用过程中，实时、在线地完成自我进化。</font>

# **二、OpenClaw-RL 的思想溯源**
:::color3
**简介：**OpenClaw-RL 的核心思想源于 **<font style="color:#ED740C;">RLAnything 的动态 RL 系统理念和 SDPO 的自蒸馏方法</font>**，并将其创新性地应用于在线交互闭环中。

:::

:::color5
**<font style="color:#601bde;">1. 动态 RL 系统理念的延伸 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">在深入解析 OpenClaw-RL 的算法机制之前，有必要追溯其主要思想的来源。</font>**

在该团队的前序作品 RLAnything 中，已初步探讨了“动态 RL 系统”的构建理念，并证明了过程奖励（Process Reward）在异构 Agent 任务（如文字游戏、基础 GUI 操作）中的普适性。RLAnything 强调策略（Policy）、环境（Environment）和奖励（Reward）三者的协同演进。

<font style="background-color:#FBDFEF;">OpenClaw-RL 可以被视为这一系统工程思想在“真实多轮交互”场景下的极致延伸，它将“环境”的概念泛化至包含真实用户设备、云端沙盒在内的广阔空间。</font>

:::color5
**<font style="color:#601bde;">2. 核心算法创新：事后诸葛亮式的同策略蒸馏（OPD）</font>**

:::

**<font style="color:#74B602;">OpenClaw-RL 中最核心的算法创新是Hindsight-Guided On-Policy Distillation（事后诸葛亮式的同策略蒸馏，简称 OPD）。</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044900008-dee62d7a-bb93-4c82-a340-39b6dbe9bd4a.png)

其理论基础脱胎于近期在对齐领域备受关注的 **SDPO（Self-Distillation Preference Optimization）** 等自蒸馏方法。SDPO 等“自蒸馏”方法的核心思想在于：**<font style="background-color:#D9EAFC;">无需依赖比当前模型更强大的外部模型作为 Teacher</font>****。** 通过引入某种“神谕（Oracle）”或“提示（Hint）”，为当前模型提供额外的高质量上下文，模型便能在微观的 Token 级别上生成更优的概率分布。通过让原始的“懵懂状态”拟合引入 Hint 后的“上帝视角状态”，模型即可实现自我进化。

OpenClaw-RL 进一步将 SDPO 的思想从离线静态数据集无缝迁移至**在线交互（Online Interaction）的闭环中。它利用环境反馈（Next-state signal）实时生成 Hint，并实时进行同策略蒸馏。

<font style="background-color:#FBDFEF;">这使得模型在面对具体错误时，不仅能意识到错误，还能在 Token 级别上明确改进方向。</font>

# **三、核心机制：重新定义「下一状态的信号」**
:::color3
**简介：**OpenClaw-RL 创新性地将环境交互反馈转化为评估性信号和指导性信号，分别通过**<font style="color:#ED740C;">过程奖励模型（PRM）和自蒸馏（OPD）机制进行处理</font>**，并在 PPO 目标函数中融合。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044912653-a86191ad-e4a4-4e59-8d03-c37a839347a7.png)

:::color5
**<font style="color:#601bde;">1. 交互反馈的双重信号价值 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">在传统的强化学习马尔可夫决策过程（MDP）中，智能体在状态下执行动作后，环境会转移到下一个状态。对于长期以来的 LLM 训练而言，下一个状态仅仅作为“下一步的上下文”输入给模型。</font>**

OpenClaw-RL 的一个重要洞察是：在 Agent 与环境（无论是人类用户还是操作系统）的交互中，下一个状态**天然自带了对上一个动作的“评价”**。更为关键的是，这种交互反馈包含了传统 RL 极度渴求的双重信号：

1. **评估性信号：** 例如代码运行后终端弹出的 `Error`，或者用户回复的负面评价。这本质上是一个标量奖励（Reward），明确指示上一个动作是糟糕的。
2. **指导性信号：** 无论是编译器的报错信息，还是用户的纠错反馈，不仅指出了错误，还直接提供了具体的改进方向（Hint）。

传统方法通常只能利用第一类标量信号，或者将第二类信号作为历史 Prompt 留给模型的下一次生成。OpenClaw-RL 的核心目标是将这两类信号**全部转化为直接更新模型权重的策略梯度（Policy Gradient）**。

<font style="background-color:#FBDFEF;">为了处理这两类截然不同的信号，OpenClaw-RL 设计了两套相互独立又互补的优势函数（Advantage）计算机制，并在同一个 PPO 目标函数中进行融合。</font>

:::color5
**<font style="color:#601bde;">2. 机制一：将文本转化为二元信号（Binary RL）</font>**

:::

**<font style="color:#74B602;">针对第一类评估性信号，论文引入了过程奖励模型（PRM）。</font>**

在交互发生后，一个独立的裁判模型（Judge Model）会同时观察 Agent 的输出和环境的真实反馈。裁判的任务是判断这一步是否推动了任务进展，并给出一个离散的标量打分。

获取该分数后，系统直接将其作为单步优势函数，代入 PPO 的截断代理目标函数中。

这是一种**宏观层面的调整**。如果裁判给出正向评分，PPO 会将整个句子中所有 Token 的生成概率统一推高；反之则整体压低。

<font style="background-color:#FBDFEF;">该机制尝试解决长序列任务中的信用分配问题，相当于提供了一个在线、高频、免人工的 RLHF 替代方案。</font>

:::color5
**<font style="color:#601bde;">3. 机制二：自蒸馏（OPD） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">仅有宏观的标量调整是不够的。如果回答中仅有某个词汇使用不当，统一压低整句话的概率会导致对正确信息的误杀。</font>**为了充分利用第二类“指导性信号”，论文提出了**事后引导的同策略蒸馏（Hindsight-Guided OPD）**，即 SDPO 思想的在线化落地。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044966936-e5391421-55b6-4f55-b2b5-afd0ca00c072.png)

该过程分为三个步骤：

1. **严格的提取与过滤：** 裁判模型从冗杂的反馈中提炼出一句精简的纠错提示（Hint）。为保证梯度质量，系统设定了严格的规则：只有当裁判打正分且 Hint 长度大于 10 个字符时，该数据才会被采纳，否则直接丢弃。
2. **策略模型自我指导：** 获取 Hint 后，系统将 Hint（正确答案）拼接到原有的上下文中，构造出一个包含“上帝视角”的超级提示。此时，让**同一个策略模型（Student 本身）**在该超级提示的视角下，重新对刚才的回答计算对数概率。
3. **Token 级别的对齐：** 计算两者在每一个 Token 上的概率差。

<font style="background-color:#FBDFEF;">这是一种</font>**<font style="background-color:#FBDFEF;">微观层面的雕刻</font>**<font style="background-color:#FBDFEF;">。如果概率差为正，说明具备上帝视角的 Teacher 更倾向于输出该特定词汇，Student 应当在此处提高概率。该机制实现了极为罕见的、无需外部成对数据（Pairwise Data）的词级别方向性指导。</font>

:::color5
**<font style="color:#601bde;">4. 机制融合与优势计算</font>**

:::

**<font style="color:#74B602;">在实际的实验调优中，作者发现这两种方法并非竞争关系。Binary RL 触发率高、覆盖面广，但信号较为粗糙；OPD 信号极其精准，但由于严格的过滤机制，数据量非常稀疏。</font>**

因此，最佳的解决方案是在计算总优势时，将两者通过权重进行融合。在该公式下，即便宏观上模型受到整体惩罚，但在微观层面，正确的 Token 依然能在 OPD 的保护下得到补偿。

# **四、系统工程**
:::color3
**简介：**OpenClaw-RL 采用**<font style="color:#ED740C;">解耦与异步流转的架构设计</font>**，将系统拆分为四个独立循环，并通过伪装拦截策略实现低成本接入。

:::

:::color5
**<font style="color:#601bde;">1. 解耦与异步流转的系统架构 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">在具体训练过程中，Agent 的交互轨迹通常极长，如何降低训练带来的高昂时延是一个关键问题。</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044878470-a99cdc74-3528-4a38-9408-94619bf27625.png)

如上图所示，这套架构的核心思想可溯源至 slime 框架（核心思想为“解耦与异步流转”，详情可参考 [https://github.com/THUDM/slime](https://link.zhihu.com/?target=https%3A//github.com/THUDM/slime)）。

<font style="background-color:#D9EAFC;">系统被拆分为四个互不阻塞的循环：</font>

+ **Serving（SGLang）：** 前端推理引擎，负责快速响应用户请求或执行环境命令。
+ **Environment：** 用户的个人设备或云端代码沙盒。
+ **Judge（PRM）：** 裁判模型在后台获取历史交互，进行打分和 Hint 提取。
+ **Trainer（Megatron）：** 训练节点持续从数据池中获取整理好的样本计算梯度，并在达到一定步数后，平滑地将新权重更新给前台的 SGLang。

<font style="background-color:#FBDFEF;">在该架构下，推理无需等待训练，训练也无需等待新的交互结束。这类似于餐厅的运营模式：前厅服务员（Serving）专注于点菜上菜，后厨（Trainer）根据顾客反馈（Judge 的反馈）不断改进菜谱，两者互不干扰。</font>

:::color5
**<font style="color:#601bde;">2. 伪装拦截策略与低成本接入 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">为了使这套庞大的 RL 设施能够低成本地接入任何现有的 Agent 框架，OpenClaw-RL 在工程落地时采用了一种“伪装拦截”策略。</font>**

RL Server 对外暴露一个标准的 OpenAI 兼容 API。用户在使用时，只需在配置文件中修改 `baseUrl`。当客户端发送请求时，系统会在后端自动区分主线任务（用于收集提取奖励）和辅助动作（直接放行）。

<font style="background-color:#FBDFEF;">这种设计使得用户几乎感知不到底层 RL 框架的存在，在工程上真正实现了“Simply by Talking（在交流中自动进化）”。</font>

# **五、实验验证与泛化能力**
:::color3
**简介：**实验表明，OpenClaw-RL 能够在个人智能体场景下**<font style="color:#ED740C;">实现极速的风格对齐</font>**，并在通用智能体场景中通过过程奖励有效解决长序列任务难题。

:::

:::color5
**<font style="color:#601bde;">1. Track 1：个人智能体的极速风格对齐 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">在 Personal Agent 场景下，作者设计了两个具有代表性的模拟实验：</font>**

+ **隐匿踪迹的学生：** 希望 Agent 协助完成作业，但极度排斥大模型常见的“Markdown 加粗、分点作答”等“AI 味”排版。
+ **友善批改的老师：** 希望 Agent 在批改作业时，不仅给出对错判断，还能提供鼓励并指出具体步骤的亮点。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044900008-dee62d7a-bb93-4c82-a340-39b6dbe9bd4a.png)

如上图所示，在结合 Binary RL 与 OPD 的方法下，模型仅需 **36 次（学生设定）** 或 **24 次（老师设定）** 交互，即可实现显著的风格转变。

<font style="background-color:#FBDFEF;">这种极高的对齐效率证明：一旦将反馈的颗粒度从“回合级（Episode）”细化至“Token 级（OPD 的定向指导）”，模型能够迅速收敛至用户的隐式偏好。</font>

:::color5
**<font style="color:#601bde;">2. Track 2：通用智能体与长序列难题的解决</font>**

:::

**<font style="color:#74B602;">如果说 Track 1 证明了其作为“贴心助理”的能力，那么 Track 2 则验证了其作为“生产力工具”的潜力。</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775044997206-d1b044e1-dacf-4af5-b936-e36c962240c5.png)

论文在 Terminal（终端）、GUI（图形界面）、SWE（软件工程）和 Tool-call（工具调用）四个真实世界场景下对该框架进行了验证。在这些场景中，环境反馈不再是主观偏好，而是客观的退出码（Exit Code）、视觉状态差异（Visual Diff）或测试用例验证结果（Test Verdicts）。

<font style="background-color:#D9EAFC;">这部分最具启发性的结论在于</font>**<font style="background-color:#D9EAFC;">过程奖励对长序列任务的决定性作用</font>**<font style="background-color:#D9EAFC;">。</font>

在长达几十步的 GUI 操控或代码修复中，如果仅使用最终的 Outcome Reward（完成整个任务后给予奖励），模型极易迷失方向。而 OpenClaw-RL 通过 Judge 模型对每一步的环境反馈进行判别，将极其稀疏的终点奖励转化为密集的步进式（Step-wise）梯度。

<font style="background-color:#FBDFEF;">实验结果表明，整合了过程奖励的模型，其任务成功率显著优于仅使用结果奖励的基线模型。</font>

# **六、落地评估**
:::color3
**简介：**OpenClaw-RL 将 RLHF 的全**<font style="color:#ED740C;">局优势评估与 SDPO 的微观词级拟合结合在在线流处理架构中</font>**，但在大规模商业部署上面临推理成本和灾难性遗忘等挑战。

:::

:::color5
**<font style="color:#601bde;">1. 方法论对比分析 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">为了更清晰地评估 OpenClaw-RL 的方法论，我们将其与相关方法进行对比：</font>**

| **方法范式** | **数据获取与应用时机** | **奖励/指导信号来源** | **梯度指导颗粒度** |
| :--- | :--- | :--- | :--- |
| RLHF (PPO) | 离线预收集、分阶段静态训练 | 静态全局 Reward Model | 序列级 |
| DPO | 离线预收集、分阶段静态训练 | 静态成对偏好数据 (Pairwise) | 序列级隐式对齐 |
| SDPO | 离线构造提示、分阶段静态训练 | 人工或规则预先构造的 Hint | Token 级定向校准 |
| OpenClaw-RL | 在线实时拦截、异步连续训练 | 动态 Next-State 实时交互反馈 | 多粒度 (序列级 + Token 级) 结合 |


<font style="background-color:#FBDFEF;">由此可见，OpenClaw-RL 的本质是将 RLHF 的全局优势评估与 SDPO 的微观词级拟合，整合至一个</font>**<font style="background-color:#FBDFEF;">在线的、交互式的</font>**<font style="background-color:#FBDFEF;">流处理架构中。</font>

:::color5
**<font style="color:#601bde;">2. 大规模商业部署面临的挑战</font>**

:::

**<font style="color:#74B602;">尽管该理念具有创新性，但其大规模商业部署仍面临若干挑战。</font>**

+ **推理成本**：在线持续学习并非毫无代价。在该框架中，为了实时评估并提取修正 Hint，后台必须**常驻一个性能相当的裁判（Judge）模型**。特别是在通用智能体场景中，代价更为高昂。例如在 GUI 环境下，裁判需要理解界面变化，这要求 Judge 必须是一个多模态大模型。这意味着，为了服务一个策略模型，企业在推理端的显存开销和算力消耗将成倍增加，这是目前绝大多数中小型业务难以承受的系统级成本。
+ **灾难性遗忘与 Reward Hacking**：在线持续学习是深度学习领域的长期挑战。当模型无限制地迎合特定用户偏好时，极有可能破坏其在预训练阶段建立的通用能力底座。这也是作者在实验中设定极其保守的超参数（如低学习率和严苛的 PPO 截断比例）的原因。如何在模型个性化与能力退化之间维持长久的微观平衡，仍是一个亟待解决的工程难题。

# **总结**
:::color3
**简介：**OpenClaw-RL 展示了下一代智能体学习系统**<font style="color:#ED740C;">解耦、异步、从交互中获取梯度的形态</font>**，证明了“部署即训练”的可行性，为智能体能力的持续提升提供了新路径。

:::

:::color5
**<font style="color:#601bde;">1. 下一代智能体学习系统的形态展望 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">OpenClaw-RL 为我们提供了一个极具前瞻性的视角，展示了下一代智能体学习系统应具备的形态：解耦、异步、从交互中榨取梯度。</font>**

它在工程层面证明了“部署即训练”这一路径的可行性。过去，强化学习受限于缺乏足够多、高质量的 Agent 轨迹数据；而 OpenClaw-RL 指出，全球无数终端上持续发生的失败报错、代码重试和用户重新输入，正是蕴藏丰富价值的数据宝库。

<font style="background-color:#FBDFEF;">如果我们认同 </font>**<font style="background-color:#FBDFEF;">Agent Scaling Law（智能体缩放定律）</font>**<font style="background-color:#FBDFEF;"> 的存在，那么推动智能体能力持续提升的动力，很可能不再局限于人工标注的静态偏好数据集，而是如同 OpenClaw-RL 所展示的，通过精巧的异步系统设计，从源源不断的环境交互反馈中自动获取的无尽数据飞轮。</font>

