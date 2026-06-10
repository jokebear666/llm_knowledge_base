# ⑥ Agentic RL：基于 LLM 的智能体强化学习

<!-- source: yuque://zhongxian-iiot9/hlyypb/lgn4ufup9ecyspcw -->

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);"> Agent强化学习（Agentic RL）的出现标志着</font>[**<font style="color:#74B602;">LLM</font>**](https://zhida.zhihu.com/search?content_id=262999464&content_type=Article&match_order=1&q=LLM&zhida_source=entity)**<font style="color:#74B602;">（LLM RL）传统强化学习应用的一次范式转变</font>**<font style="color:rgb(25, 27, 31);">，它将LLM从被动的序列（sequence)生成器重塑为嵌入在复杂、动态世界中的自主决策Agent 。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Agentic RL 无疑是最近半年绝对的行业热点，来看一篇最近的综述文章，系统讲述 LLM 如何被嵌入到复杂的决策循环中，成为能够</font>**<font style="color:#ED740C;">自主决策、长期规划、与动态环境交互的智能体</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">理论形式化</font>**<font style="color:rgb(25, 27, 31);">：通过将传统 LLM-RL（如 RLHF）建模为退化的单步马尔可夫决策过程（</font>[<font style="color:rgb(9, 64, 142);">MDP</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=MDP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">），而将 Agentic RL 建模为部分可观测、长时程的</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">POMDP</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=POMDP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">系统性分类</font>**<font style="color:rgb(25, 27, 31);">：创新性地提出了一个</font>**<font style="color:rgb(25, 27, 31);">能力 - 任务双维度分类法</font>**<font style="color:rgb(25, 27, 31);">，一方面围绕规划、工具使用、记忆、推理、自省和感知等核心智能体能力，另一方面围绕搜索、编码、GUI 操作等具体任务，系统梳理了前沿文献。</font>
+ **<font style="color:rgb(25, 27, 31);">生态资源整合</font>**<font style="color:rgb(25, 27, 31);">：首次将该领域分散的开源环境、基准测试和框架整合成一个实用的资源库，为后续研究者提供了极大的便利。</font>

<font style="color:rgb(83, 88, 97);">论文：</font>[https://arxiv.org/pdf/2509.02547](https://arxiv.org/pdf/2509.02547)<font style="color:rgb(83, 88, 97);">  
</font><font style="color:rgb(83, 88, 97);">代码：</font>[https://github.com/xhyumiracle/Awesome-AgenticLLM-RL-Papers](https://link.zhihu.com/?target=https%3A//github.com/xhyumiracle/Awesome-AgenticLLM-RL-Papers)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760683962828-3e26d730-8e83-4c30-9ba7-1c31e90a018e.png)

:::color5
**<font style="color:#601BDE;">1.agentic LLM与环境之间的动态交互过程  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760683984461-46a3cd52-86fc-405e-b366-ae5f530c9149.png)

> agentic LLM与环境之间的动态交互过程。
>



## <font style="color:rgb(25, 27, 31);">一、从 LLM-RL 到 Agentic RL</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">传统的 LLM-RL，特别是以人类偏好为基础的强化微调（Preference-Based Reinforcement Finetuning, </font>[<font style="color:rgb(9, 64, 142);">PBRFT</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=PBRFT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">），其核心目标是</font>**<font style="color:rgb(25, 27, 31);">对齐（Alignment）</font>**<font style="color:rgb(25, 27, 31);">。即，让模型的单次输出更符合人类的价值观或偏好。相比之下，Agentic RL 的核心目标是</font>**<font style="color:rgb(25, 27, 31);">决策（Decision-making）</font>**<font style="color:rgb(25, 27, 31);">。它旨在优化 LLM 在一系列连续的交互步骤中完成复杂任务的能力。</font>

:::

### <font style="color:rgb(25, 27, 31);">1.1 形式化定义</font>
:::color5
**<font style="color:#601BDE;">1.传统 PBRFT：一个退化的单步 MDP  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在 PBRFT（如经典的 RLHF 流程）中，决策过程被急剧简化。其 MDP 可以表示为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684610095-aa3f16c8-a8f0-4891-85a5-f5595480104d.png)

<font style="color:rgb(25, 27, 31);">其特点如下：</font>

+ **<font style="color:rgb(25, 27, 31);">状态空间 (S</font>**<sub>**<font style="color:rgb(25, 27, 31);">trad</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：通常仅包含一个由用户提示（prompt）构成的初始状态 。</font>
+ **<font style="color:rgb(25, 27, 31);">动作空间 (A</font>**<sub>**<font style="color:rgb(25, 27, 31);">trad</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：动作是生成一个完整的文本序列。</font>
+ **<font style="color:rgb(25, 27, 31);">转移动态 (P</font>**<sub>**<font style="color:rgb(25, 27, 31);">trad</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：一旦模型生成回应，交互立即终止。因此，时间跨度T=1 。这是一个单步决策问题。</font>
+ **<font style="color:rgb(25, 27, 31);">奖励函数 (R</font>**<sub>**<font style="color:rgb(25, 27, 31);">trad</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：奖励 r(a) 是对整个生成序列的</font>**<font style="color:rgb(25, 27, 31);">一次性标量评估</font>**<font style="color:rgb(25, 27, 31);">，通常由一个预先训练好的奖励模型给出。</font>
+ **<font style="color:rgb(25, 27, 31);">学习目标 (J</font>**<sub>**<font style="color:rgb(25, 27, 31);">trad</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：最大化单步期望奖励 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684697430-3d48a723-0a14-40a1-835c-43c8feaf06e1.png)<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">PBRFT 就像回答一道选择题。给定题干（prompt），模型直接给出完整答案（生成文本），然后获得一个最终分数（reward）。整个过程只有一步。</font>

:::color5
**<font style="color:#601BDE;">2.Agentic RL：一个部分可观测的长时程 POMDP  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Agentic RL 的场景则复杂得多，它被建模为一个部分可观测马尔可夫决策过程（Partially Observable MDP, POMDP）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684711547-a8715481-977a-4493-88dd-3d5ac2738b0f.png)

<font style="color:rgb(25, 27, 31);">其特点如下：</font>

+ **<font style="color:rgb(25, 27, 31);">状态空间 (S</font>**<sub>**<font style="color:rgb(25, 27, 31);">agent</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：环境状态  是动态变化的，且智能体无法完全观测，只能接收到一个</font>**<font style="color:rgb(25, 27, 31);">观测o</font>**<sub>**<font style="color:rgb(25, 27, 31);">t</font>**</sub>**<font style="color:rgb(25, 27, 31);">=O(s</font>**<sub>**<font style="color:rgb(25, 27, 31);">t</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">动作空间 (A</font>**<sub>**<font style="color:rgb(25, 27, 31);">agent</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：动作空间是混合的，包含两部分：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684769908-a3fcbfd4-c060-42ce-9cef-44ebae29ca1a.png)<font style="color:rgb(25, 27, 31);">。</font>
    - <font style="color:rgb(25, 27, 31);">A</font><sub><font style="color:rgb(25, 27, 31);">text:</font></sub><font style="color:rgb(25, 27, 31);"> 生成自然语言文本。</font>
    - <font style="color:rgb(25, 27, 31);">A</font><sub><font style="color:rgb(25, 27, 31);">action</font></sub><font style="color:rgb(25, 27, 31);">: 执行结构化动作，如调用 API、使用工具或与环境交互。</font>
+ **<font style="color:rgb(25, 27, 31);">转移动态 (P</font>**<sub>**<font style="color:rgb(25, 27, 31);">agent</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：环境根据智能体的动作随机转移到下一个状态 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684862194-1a3a11fb-db67-4cf2-9f19-dea589e48f45.png)<font style="color:rgb(25, 27, 31);">。时间跨度 T>1。</font>
+ **<font style="color:rgb(25, 27, 31);">奖励函数 (R</font>**<sub>**<font style="color:rgb(25, 27, 31);">agent</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：奖励可以是</font>**<font style="color:rgb(25, 27, 31);">稀疏的</font>**<font style="color:rgb(25, 27, 31);">（仅在任务最终完成时给予），也可以是</font>**<font style="color:rgb(25, 27, 31);">密集的</font>**<font style="color:rgb(25, 27, 31);">（在每个中间步骤根据进展给予）。</font>
+ **<font style="color:rgb(25, 27, 31);">学习目标 (J</font>**<sub>**<font style="color:rgb(25, 27, 31);">agent</font>**</sub>**<font style="color:rgb(25, 27, 31);">)</font>**<font style="color:rgb(25, 27, 31);"> ：最大化长期折扣累积奖励 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684873844-b75e91ee-df7e-495b-9082-4dcfd49f96fd.png)<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.从LLM-RL到代理RL的范式转变  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Agentic RL 就像玩一个侦探游戏。智能体根据当前有限的线索（观测），决定是去搜查房间还是询问证人（动作），然后环境会给出新的线索（下一观测）。目标是通过一系列决策，最终破案（最大化累积奖励）。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760683962828-3e26d730-8e83-4c30-9ba7-1c31e90a018e.png)

> 从LLM-RL到代理RL的范式转变
>

<font style="color:rgb(25, 27, 31);">下表总结二者的区别：</font>

| **<font style="color:rgb(25, 27, 31);">概念</font>** | **<font style="color:rgb(25, 27, 31);">传统 PBRFT</font>** | **<font style="color:rgb(25, 27, 31);">Agentic RL</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">决策过程</font> | <font style="color:rgb(25, 27, 31);">单步决策 (T=1)</font> | <font style="color:rgb(25, 27, 31);">多步序贯决策 (T>1)</font> |
| <font style="color:rgb(25, 27, 31);">状态空间</font> | <font style="color:rgb(25, 27, 31);">单一、静态的 prompt</font> | <font style="color:rgb(25, 27, 31);">动态、部分可观测的世界状态</font> |
| <font style="color:rgb(25, 27, 31);">动作空间</font> | <font style="color:rgb(25, 27, 31);">纯文本序列生成</font> | <font style="color:rgb(25, 27, 31);">文本生成 + 结构化动作（如工具调用）</font> |
| <font style="color:rgb(25, 27, 31);">奖励机制</font> | <font style="color:rgb(25, 27, 31);">对最终输出的单次评分</font> | <font style="color:rgb(25, 27, 31);">对每一步或最终结果的（稀疏/密集）奖励</font> |
| <font style="color:rgb(25, 27, 31);">核心挑战</font> | <font style="color:rgb(25, 27, 31);">文本质量对齐</font> | <font style="color:rgb(25, 27, 31);">信用分配、探索 - 利用、样本效率</font> |


<font style="color:rgb(25, 27, 31);">这个形式化的区分明确了 Agentic RL 的研究对象是</font>**<font style="color:rgb(25, 27, 31);">长时程、交互式、目标导向</font>**<font style="color:rgb(25, 27, 31);">的决策问题，从而将其与以对齐为目标的传统 LLM-RL 清晰地分离开来。</font>

### <font style="color:rgb(25, 27, 31);">1.2 核心驱动算法</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">重点对比三种常见的算法代表：PPO、DPO 和 GRPO。</font>

:::

:::color5
**<font style="color:#601BDE;">1.近端策略优化 (Proximal Policy Optimization, PPO)  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">作为 RLHF 时代的「事实标准」，PPO 通过其「裁剪（clipping）」机制限制了策略更新的步长，确保了训练的稳定性。其目标函数为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684895986-8c6f8f4f-3a6d-44e2-9cef-8318f52c638c.png)

<font style="color:rgb(25, 27, 31);">其中 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760685259729-ef8729a3-b855-4be7-bed7-a694dafd0b35.png)<font style="color:rgb(25, 27, 31);"> 是新旧策略的概率比，</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760685264595-72ea67b6-5594-4234-afb0-edf5d70d0d1e.png)<font style="color:rgb(25, 27, 31);"> 是优势函数。PPO 的缺点是需要一个与策略网络同样大小的 Critic 网络来估计价值函数，计算开销较大。</font>

:::color5
**<font style="color:#601BDE;">2.直接偏好优化 (Direct Preference Optimization, DPO)</font>**<font style="color:#601BDE;"> </font>

:::

<font style="color:rgb(25, 27, 31);">DPO 巧妙地将 RL 问题转化为一个基于偏好数据的分类问题，从而</font>**<font style="color:rgb(25, 27, 31);">完全绕过了显式的奖励建模和 Critic 网络</font>**<font style="color:rgb(25, 27, 31);">。其损失函数为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684901197-4038d9b8-90f6-4644-a26f-746fb6eb8413.png)

<font style="color:rgb(25, 27, 31);">其中 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760685270238-cbb60e10-e042-4ed8-9ea7-e1ab1f66759d.png)<font style="color:rgb(25, 27, 31);"> 分别是偏好和非偏好的回应。DPO 虽然高效，但其性能高度依赖于静态偏好数据的质量和覆盖度。</font>

:::color5
**<font style="color:#601BDE;">3.组相对策略优化 (</font>**[**<font style="color:#601BDE;">Group Relative Policy Optimization</font>**](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=Group+Relative+Policy+Optimization&zhida_source=entity)**<font style="color:#601BDE;">, GRPO)</font>**

:::

<font style="color:rgb(25, 27, 31);">由 DeepSeek 团队提出并因其在数学推理等任务上的成功而备受关注。GRPO 旨在解决 PPO 中 Critic 网络带来的巨大开销。其核心思想是，在一次策略 rollout 中生成一个</font>**<font style="color:rgb(25, 27, 31);">组</font>**<font style="color:rgb(25, 27, 31);">的多个回应，并利用这些回应在组内的</font>**<font style="color:rgb(25, 27, 31);">相对奖励</font>**<font style="color:rgb(25, 27, 31);">来估计优势函数，从而</font>**<font style="color:rgb(25, 27, 31);">取消了对独立 Critic 网络的需求</font>**<font style="color:rgb(25, 27, 31);">。优势函数被估计为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684906093-e587f2ce-f715-4713-a8b6-a78b331cfcf7.png)

<font style="color:rgb(25, 27, 31);">这种方法在多个 Agentic RL 任务中被证明非常有效。</font>

:::color5
**<font style="color:#601BDE;">4.PPO、DPO和GRPO家族流行变体的比较  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760683976014-5a3d4324-8e5c-4880-819c-2c17dcbfb8bb.png)

> PPO、DPO和GRPO家族流行变体的比较
>

## <font style="color:rgb(25, 27, 31);">二、能力分类：Agentic RL 如何塑造智能</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">文章提出一种「以能力为中心」的分类法。它系统地剖析了智能体所需的六大核心能力，并阐明了 RL 如何将这些能力从静态的、基于规则的模块，转变为动态的、可学习的策略。</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760683993639-18597a1f-91f7-47dc-ba9e-a0e6c1f04c8b.png)

> RL授权代理LLM的六个方面的总结。请注意，这里列出的代表性方法并不详尽；请参阅我们的正文。
>

### <font style="color:rgb(25, 27, 31);">2.1 规划 (Planning)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">规划能力是智能体实现复杂目标的核心。</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">RL 之前</font>**<font style="color:rgb(25, 27, 31);">：主要依赖提示工程，如</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">ReAct 框架</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=ReAct+%E6%A1%86%E6%9E%B6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，通过固定的「Thought-Action-Observation」循环来引导 LLM。这种方法缺乏适应性。</font>
+ **<font style="color:rgb(25, 27, 31);">RL 作为外部指导</font>**<font style="color:rgb(25, 27, 31);">：RL 用于训练一个辅助的评估函数（或启发式函数），来指导经典的搜索算法（如蒙特卡洛树搜索, MCTS）。LLM 负责生成候选动作，而 RL 训练的模型负责评估哪个动作更有前景。</font>
+ **<font style="color:rgb(25, 27, 31);">RL 作为内部驱动</font>**<font style="color:rgb(25, 27, 31);">：RL 直接将 LLM 作为策略网络进行端到端的优化。智能体通过与环境的反复试错，直接学习生成更优计划的内在能力。例如，VOYAGER 框架通过 RL 不断地探索、学习并扩充自身的技能库。</font>
+ **<font style="color:rgb(25, 27, 31);">未来展望</font>**<font style="color:rgb(25, 27, 31);">：融合「直觉式」的快速计划生成和「审慎式」的慢速搜索推理，形成一个统一的、可学习的审议（deliberation）过程。</font>

### <font style="color:rgb(25, 27, 31);">2.2 工具使用 (Tool Using)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">工具使用极大地扩展了 LLM 的能力边界。</font>

:::

+ **<font style="color:rgb(25, 27, 31);">RL 之前</font>**<font style="color:rgb(25, 27, 31);">：依赖 SFT（在专家轨迹上微调，如</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Toolformer</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=Toolformer&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）或提示工程（ReAct）。这些方法本质上是</font>**<font style="color:rgb(25, 27, 31);">模仿</font>**<font style="color:rgb(25, 27, 31);">，智能体只能复现见过的工具使用模式，缺乏策略灵活性和错误恢复能力。</font>
+ **<font style="color:rgb(25, 27, 31);">RL 驱动的工具使用</font>**<font style="color:rgb(25, 27, 31);">：RL 将学习目标从「模仿」转为「</font>**<font style="color:rgb(25, 27, 31);">结果驱动的优化</font>**<font style="color:rgb(25, 27, 31);">」。智能体不再是简单地模仿如何调用工具，而是学习</font>**<font style="color:rgb(25, 27, 31);">何时、为何以及如何组合使用工具</font>**<font style="color:rgb(25, 27, 31);">来最大化任务成功率。ToRL、ToolRL 等工作表明，即使从零开始，RL 也能让智能体涌现出自主纠错、组合工具等复杂行为。</font>
+ **<font style="color:rgb(25, 27, 31);">未来展望</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">长时程工具集成推理（Long-horizon TIR）</font>**<font style="color:rgb(25, 27, 31);">。当前的主要瓶颈在于</font>**<font style="color:rgb(25, 27, 31);">时间信用分配（temporal credit assignment）</font>**<font style="color:rgb(25, 27, 31);">。在一个包含数十步工具调用的长任务中，如何判断哪一步是关键的成功或失败因素，是一个亟待解决的难题。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684137992-5415828f-cc40-40ba-922e-1c1588bb2661.png)

> agenti工具使用的发展。请注意，我们只选择了一小部分代表在这里工作以反映进展。
>

### <font style="color:rgb(25, 27, 31);">2.3 记忆 (Memory)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">记忆使智能体能够维持上下文、从历史经验中学习。</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">RL 之前</font>**<font style="color:rgb(25, 27, 31);">：记忆通常是外部的、被动的数据存储（如向量数据库），遵循固定的读写规则（如 RAG）。</font>
+ **<font style="color:rgb(25, 27, 31);">RL 驱动的记忆管理</font>**<font style="color:rgb(25, 27, 31);">：Agentic RL 将记忆模块变成一个</font>**<font style="color:rgb(25, 27, 31);">可控的子系统</font>**<font style="color:rgb(25, 27, 31);">。RL 策略可以学习决定</font>**<font style="color:rgb(25, 27, 31);">什么信息值得存（write）、何时应该检索（read）、以及如何更新或遗忘（update/forget）</font>**<font style="color:rgb(25, 27, 31);">。例如，</font>[<font style="color:rgb(9, 64, 142);">Memory-R1 框架</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=Memory-R1+%E6%A1%86%E6%9E%B6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">使用 RL 来学习对记忆进行增删改查的操作。</font>
+ **<font style="color:rgb(25, 27, 31);">未来展望</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">结构化记忆的 RL 控制</font>**<font style="color:rgb(25, 27, 31);">。当前的记忆大多是扁平的文本或向量。未来的研究方向是使用 RL 来动态构建和维护更复杂的记忆结构，如知识图谱或层次化记忆网络，但这方面的工作目前还非常稀少。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684175294-30ee0b6a-b729-4079-806d-03a7feb78862.png)

> agent memory的三个经典类别概述；标有†的作品直接使用RL。这里的列表并不详尽，我们建议对borader代理记忆感兴趣的读者参考[112]。
>

### <font style="color:rgb(25, 27, 31);">2.4 自我改进 (Self-Improvement)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">自我改进是智能体实现持续进化的关键。</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">言语自我纠正 (Verbal Self-correction)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：这是最早期、无需梯度更新的方法。模型在一个推理回合内生成答案、进行语言层面的反思、然后给出修正后的答案（如 Reflexion, Self-Refine）。</font>
+ **<font style="color:rgb(25, 27, 31);">内化自我纠正 (Internalized Self-correction)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：通过 RL 将这种反思 - 修正的循环</font>**<font style="color:rgb(25, 27, 31);">内化到模型参数中</font>**<font style="color:rgb(25, 27, 31);">。智能体通过在成功和失败的轨迹上进行学习，从根本上提升其识别和修正自身错误的能力。</font>
+ **<font style="color:rgb(25, 27, 31);">迭代自训练 (Iterative Self-training)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：这是最接近自主进化的形式。智能体进入一个</font>**<font style="color:rgb(25, 27, 31);">自我驱动的学习循环</font>**<font style="color:rgb(25, 27, 31);">：自己生成任务、尝试解决、通过可验证的执行结果获得奖励、再用这个奖励信号来更新自己的策略（如 Absolute Zero,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Self-Evolving Curriculum</font>](https://zhida.zhihu.com/search?content_id=262637086&content_type=Article&match_order=1&q=Self-Evolving+Curriculum&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）。</font>
+ **<font style="color:rgb(25, 27, 31);">未来展望</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">元反思能力的演化（Meta Evolution of Reflection）</font>**<font style="color:rgb(25, 27, 31);">。当前的反思过程本身大多是人工设计的。未来的前沿在于，让智能体不仅学习如何纠正错误，更要通过 RL</font>**<font style="color:rgb(25, 27, 31);">学习如何更有效地进行自我纠正</font>**<font style="color:rgb(25, 27, 31);">。</font>

### <font style="color:rgb(25, 27, 31);">2.5 推理 (Reasoning)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">遵循认知科学的双系统理论，推理可分为快、慢两种。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">快推理 (Fast Reasoning)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：类似于 System 1，是 LLM 默认的、直觉式的、一次性的推理模式。它高效但容易出错（幻觉）。</font>
+ **<font style="color:rgb(25, 27, 31);">慢推理 (Slow Reasoning)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：类似于 System 2，通过生成中间步骤（如 CoT）来进行审慎、结构化的推理。它更准确但延迟更高。Agentic RL，特别是 GRPO 等算法的出现，极大地推动了开放模型在慢推理（尤其是在数学和编码领域）上的性能。</font>
+ **<font style="color:rgb(25, 27, 31);">未来展望</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">在智能体中集成慢推理机制</font>**<font style="color:rgb(25, 27, 31);">。如何在需要长时程交互的智能体场景中，可靠地训练和应用慢推理能力，同时避免「过度思考」带来的高延迟，是一个开放的挑战。</font>

### <font style="color:rgb(25, 27, 31);">2.6 感知 (Perception)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">感知能力，特别是视觉感知，是智能体与物理世界交互的基础。Agentic RL 推动多模态模型从简单的「看图回答」的被动感知，转向</font>**<font style="color:rgb(25, 27, 31);">主动的视觉认知</font>**<font style="color:rgb(25, 27, 31);">。这意味着智能体可以在推理过程中</font>**<font style="color:rgb(25, 27, 31);">反复地、有目的地</font>**<font style="color:rgb(25, 27, 31);">与视觉信息交互。</font>

:::

**<font style="color:rgb(25, 27, 31);">实现路径</font>**<font style="color:rgb(25, 27, 31);">：</font>

1. **<font style="color:rgb(25, 27, 31);">锚定（Grounding）</font>**<font style="color:rgb(25, 27, 31);">：将推理的每一步都与图像中的特定区域锚定，如 GRIT。</font>
2. **<font style="color:rgb(25, 27, 31);">工具驱动</font>**<font style="color:rgb(25, 27, 31);">：赋予智能体使用视觉工具（如图像编辑器、目标检测器）的能力，如 VTool-R1。</font>
3. **<font style="color:rgb(25, 27, 31);">生成驱动</font>**<font style="color:rgb(25, 27, 31);">：允许智能体通过生成草图或想象的图像来辅助推理，如 GoT-R1。</font>

<font style="color:rgb(25, 27, 31);">这一思想也被扩展到了音频等其他模态。</font>

## <font style="color:rgb(25, 27, 31);">三、应用、生态与挑战</font>
### <font style="color:rgb(25, 27, 31);">3.1 任务视角下的应用</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Agentic RL 的价值最终体现在解决实际问题上。该综述系统梳理了其在多个前沿领域的应用：</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">搜索与研究智能体</font>**<font style="color:rgb(25, 27, 31);">：从简单的 RAG 演变为能够自主规划、多源验证、深度综合信息的「研究员」。RL 被用来优化查询策略和信息整合流程。</font>
+ **<font style="color:rgb(25, 27, 31);">代码智能体</font>**<font style="color:rgb(25, 27, 31);">：从单次代码生成，发展到能够进行迭代式调试、与编译器和测试框架交互、甚至完成整个软件工程任务的「程序员」。执行反馈（如单元测试通过率）为 RL 提供了天然的、高质量的奖励信号。</font>
+ **<font style="color:rgb(25, 27, 31);">数学智能体</font>**<font style="color:rgb(25, 27, 31);">：无论是处理自然语言数学问题的「非形式推理」，还是在 Lean 等证明器中进行「形式推理」，RL 都通过结果验证（答案正确性）或过程验证（证明步骤正确性）来提升模型的逻辑推理能力。</font>
+ **<font style="color:rgb(25, 27, 31);">GUI 智能体</font>**<font style="color:rgb(25, 27, 31);">：通过在真实或模拟的图形界面（网页、App、操作系统）中进行交互式学习，智能体学会了如何完成点击、输入、导航等复杂操作，以完成高层指令。</font>
+ **<font style="color:rgb(25, 27, 31);">多智能体系统</font>**<font style="color:rgb(25, 27, 31);">：RL 不再只优化单个智能体，而是学习如何优化多个智能体之间的</font>**<font style="color:rgb(25, 27, 31);">协作、沟通和角色分配策略</font>**<font style="color:rgb(25, 27, 31);">，以解决单个智能体难以完成的复杂任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684219211-37377643-2c9c-4f38-af26-48fb846603e1.png)

> 特定领域agent的RL进化树。
>

### <font style="color:rgb(25, 27, 31);">3.2 生态系统：环境与框架</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">一个领域的成熟离不开其基础设施。该综述首次对 Agentic RL 的生态系统进行了系统性整合：</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">环境与基准</font>**<font style="color:rgb(25, 27, 31);">：论文列举并分类了大量用于训练和评估智能体的环境，从文本游戏（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ALFWorld</font>`<font style="color:rgb(25, 27, 31);">）、网页浏览（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">WebArena</font>`<font style="color:rgb(25, 27, 31);">）、软件工程（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">SWE-bench</font>`<font style="color:rgb(25, 27, 31);">）、到通用计算机操作（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">OSWorld</font>`<font style="color:rgb(25, 27, 31);">），为研究者提供了宝贵的「训练场」和「考场」。</font>
+ **<font style="color:rgb(25, 27, 31);">RL 框架</font>**<font style="color:rgb(25, 27, 31);">：梳理了支持 Agentic RL 研究的开源框架，包括专用的 Agentic RL 框架（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">SkyRL</font>`<font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">AREAL</font>`<font style="color:rgb(25, 27, 31);">）、通用的 RLHF 框架（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">TRL</font>`<font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">OpenRLHF</font>`<font style="color:rgb(25, 27, 31);">）和底层的通用 RL 库（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">RLlib</font>`<font style="color:rgb(25, 27, 31);">）。</font>

> ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684249382-0ddc0ee5-0b52-4506-af94-bace61cf8151.png)基于RL的搜索和研究代理方法概述。
>

### <font style="color:rgb(25, 27, 31);">3.3 开放挑战与未来方向</font>
:::color5
**<font style="color:#601BDE;">1.可信赖性  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">安全</font>**<font style="color:rgb(25, 27, 31);">：智能体的工具使用和记忆机制引入了新的攻击面（如间接提示注入）。RL 可能因「奖励黑客（reward hacking）」而放大风险，即智能体可能学会采取不安全的行为来最高效地获取奖励。</font>
+ **<font style="color:rgb(25, 27, 31);">幻觉 (Hallucination)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：Agentic RL 若只奖励最终结果，可能会激励模型生成看似合理但毫无根据的中间推理步骤。</font>
+ **<font style="color:rgb(25, 27, 31);">谄媚 (Sycophancy)</font>**<font style="color:rgb(25, 27, 31);"> ：为了最大化基于人类偏好的奖励，智能体可能学会迎合用户的错误观点，而不是追求客观事实。</font>

:::color5
**<font style="color:#601BDE;">2.扩展智能体训练</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">计算、模型与数据</font>**<font style="color:rgb(25, 27, 31);">：如何高效地利用大规模计算资源、如何在大模型上稳定地进行 RL 训练、以及如何平衡多领域数据以避免能力间的负面干扰，都是亟待解决的工程和科学问题。研究表明，单纯增加 RL 训练步数能在一定程度上提升小模型的推理能力，使其逼近更大的模型，这揭示了计算在 Agentic RL 中的核心价值。</font>

:::color5
**<font style="color:#601BDE;">3.扩展智能体环境</font>**

:::

+ <font style="color:rgb(25, 27, 31);">这可能是最深刻的挑战。</font>**<font style="color:rgb(25, 27, 31);">智能体的能力上限取决于其环境的复杂性</font>**<font style="color:rgb(25, 27, 31);">。当前标准化的环境（如</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ALFWorld</font>`<font style="color:rgb(25, 27, 31);">）已不足以训练通用智能体。</font>
+ <font style="color:rgb(25, 27, 31);">未来的方向是</font>**<font style="color:rgb(25, 27, 31);">环境与智能体的共同进化</font>**<font style="color:rgb(25, 27, 31);">：利用 LLM 程序化地生成具有适应性、多样性和恰当难度的训练任务和环境（如</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">EnvGen</font>`<font style="color:rgb(25, 27, 31);">），从而创建一个能够驱动智能体持续学习和进化的「训练飞轮」。</font>

## <font style="color:rgb(25, 27, 31);">总结</font>
<font style="color:rgb(25, 27, 31);">分类法：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760684294769-b8d25ae5-352e-4f33-814e-9ffec5026885.png)

<font style="color:rgb(25, 27, 31);"></font>



**<font style="color:rgb(255, 255, 255);">送礼物</font>**



  


