# ⓵ deepseek

<!-- source: yuque://zhongxian-iiot9/hlyypb/toxxtxikhx1wgns4 -->

:::success
1. **<font style="color:#000000;">DeepSeek研究背景</font>**

**<font style="color:#000000;">a. 强化学习验证</font>**<font style="color:#000000;">：DS希望通过</font>**<font style="color:#C75C00;">纯粹的RL</font>**<font style="color:#000000;"> （完全不用监督学习）手段验证是否能走通一条接近O1的路径</font>

**<font style="color:#000000;">b.可控的reasoning</font>**<font style="color:#000000;">：为解决Zero的不足，采用了高质量数据code-start + Zero多阶段训练pipeline，得到了 DS-R1</font>

**<font style="color:#000000;">c.验证蒸馏的价值</font>**<font style="color:#000000;">：R1太大部署很不经济。用蒸馏手段在6个不同尺寸的小模型学习R1的知识，实测很强大。</font>

2. **deepseel-****R1-Zero**：<font style="color:rgb(0, 0, 0);">采用PPO改进版GRPO强化学习策略。奖励模型：是RL学习方向的刺激信号。基于rule来设计奖励模型，包括2方面：准确性和format。输出模板：比较简单。必须先输出think 过程；然后输出结果。</font>
3. **deepseel-R1**：为了输出可读、并对齐人类偏好，且只需少量高质量的样本数据就强大的reasoning能力，开启了R1 正规训练。它基于DS-v3-base，经历了4个训练阶段：
4. **deepseel-V3**：发布了其最新的大型语言模型 DeepSeek-V3，这款模型在性能和效率方面都取得了显著的进步，成为当前最强大的开源基础模型之一。DeepSeek-V3 是一款拥有 671B参数的大型混合专家 (MoE) 模型，其中每个 token 会有 37 B参数被激活。

:::

# deepseek R1
:::color3
**<font style="color:#000000;">DeepSeek研究背景</font>**

1. **<font style="color:#000000;">强化学习验证</font>**<font style="color:#000000;">：DS希望通过</font>**<font style="color:#C75C00;">纯粹的RL</font>**<font style="color:#000000;"> （完全不用监督学习）手段验证是否能走通一条接近O1的路径</font>
2. **<font style="color:#000000;">可控的reasoning</font>**<font style="color:#000000;">：为解决Zero的不足，采用了高质量数据code-start + Zero多阶段训练pipeline，得到了 DS-R1</font>
3. **<font style="color:#000000;">验证蒸馏的价值</font>**<font style="color:#000000;">：R1太大部署很不经济。用蒸馏手段在6个不同尺寸的小模型学习R1的知识，实测很强大。</font>

:::

**<font style="color:#601BDE;">模型关系图</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738810880478-0eb75b19-1bef-4274-a4f9-1ab62a2ac5be.png)

**<font style="color:#4C16B1;">整体流程</font>**

<font style="color:rgb(0, 0, 0);">报告是按3类模型分别阐述：应该是按DS研发的时间序。1和2都是以DeepSeek-v3为基础模型。</font>

+ **<font style="color:#C75C00;">DS-R1-Zero</font>**<font style="color:rgb(0, 0, 0);">：想验证下完全靠强化学习能否自主涌现reasoning，结果是能。但结果不太可读。</font>
+ **<font style="color:#C75C00;">DS-R1</font>**<font style="color:rgb(0, 0, 0);">：遵循了R1-Zero基本pipeline，加了高质量数据冷启动微调等步骤，最终是4阶段训练。</font>
+ **<font style="color:#C75C00;">蒸馏</font>**<font style="color:rgb(0, 0, 0);">：R1太大部署不划算，蒸馏出6个模型（1.5b~70b，Qwen2.5 4个，llama 2个）发现也有强大的reassoning能力（但不如教师R1）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738811286264-cd90b4fc-93c5-40f9-aca4-4975ab8014d3.png)

<font style="color:rgb(0, 0, 0);"></font>

DeepSeek研究背景  
1.复现OpenAI-O1: 业界的复现尚不能逼近O1。DS希望通过<font style="color:#DF2A3F;">纯粹的RL</font> （完全不用监督学习）手段验证是否能走通一条接近O1的路径

+ 方式：DS-v3为base模型，采用 <font style="color:#DF2A3F;">GRPO（Group Relative Policy Optimization）</font>的强化学习方式
+ 结果：获得了DS-R1-Zero具备强大的reasoning能力（逼近O1）但输出可读性差.自然进化出来的能力包括<font style="color:#DF2A3F;">自我验证、反思、CoT</font>等

  
2. 可控的reasoning：为解决Zero的不足，采用了高质量数据code-start + Zero多阶段训练pipeline，得到了 DS-R1

+ 冷启动SFT：高质量数据来微调DS-v3
+ 强化学习：采用R1-zero的GRPO 获得reasoning能力
+ 微调SFT：2接近结束时，通过拒绝采样 + 新的监督数据、微调数据，来微调模型
+ 再次强化学习：用更丰富的prompts数据进一步强化学习  

3. 验证蒸馏的价值：R1太大部署很不经济。用蒸馏手段在6个不同尺寸的小模型学习R1的知识，实测很强大。
+ 教师模型：R1-671B；小模型: Qwen和llama等6个dense小模型，学习上述大模型知识。
+ 模型小了20x ~ 95x；蒸馏学习后的能力领先业界dense模型（除了OpenAI）。



## R1整体流程
<font style="color:rgb(0, 0, 0);">报告是按3类模型分别阐述：应该是按DS研发的时间序。1和2都是以DeepSeek-v3为基础模型。</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">DS-R1-Zero：想验证下完全靠强化学习能否自主涌现reasoning，结果是能。但结果不太可读。</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">DS-R1：遵循了R1-Zero基本pipeline，加了高质量数据冷启动微调等步骤，最终是4阶段训练。</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">蒸馏：R1太大部署不划算，蒸馏出6个模型（1.5b~70b，Qwen2.5 4个，llama 2个）发现也有强大的reassoning能力（但不如教师R1）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738811286264-cd90b4fc-93c5-40f9-aca4-4975ab8014d3.png)

## R1-Zero
:::color3
+ <font style="color:rgb(0, 0, 0);">采用PPO改进版GRPO强化学习策略</font>
+ <font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">奖励模型：是RL学习方向的刺激信号。基于rule来设计奖励模型，包括2方面：准确性和format</font>
+ <font style="color:rgb(0, 0, 0);">输出模板：如下，比较简单。必须先输出think 过程；然后输出结果。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738811381629-646699d3-ab18-45a5-870f-7fba294ec66f.png)

:::color5
**<font style="color:#601BDE;">1. 核心理念</font>**

:::

简单来说，R1-zero 旨在从预训练模型（Base Model）出发，直接通过 RL（强化学习） 得到一个具有优秀 Reasoning（推理）能力的模型。Deepseek 希望通过这种自探索的方式，验证是否可以在无需任何“Ground Truth CoT（思维链）”引导的情况下，让模型自主学会思考并解决问题。

:::color5
**<font style="color:#601BDE;">2.训练实现</font>**

:::

通过 Prompt 控制 R1-zero 在训练过程中生成两部分内容：

+ 思考过程：由 `<think></think>` 包裹。
+ 最终答案：由 `<answer></answer>` 包裹。

:::color5
**<font style="color:#601BDE;">3.Reward（奖励）计算规则</font>**

:::

对生成的两部分内容，依照以下规则计算 Reward：

1. 准确率：答案是否与 Ground Truth (GT) 一致。
2. 格式：强制要求模型将所有的思考过程包裹在 `<think>` 标签内。

:::color5
**<font style="color:#601BDE;">4.算法与效果</font>**

:::

+ 算法：利用 GRPO 算法计算 Loss，Reward 用于计算该条 Response 的优势值。
+ 涌现现象：
    - 随着 RL 自探索的进行，准确率不断提升。
    - 模型生成的内容长度不断增加（Test-time scaling），证明模型通过生成对解题有用的 Token 来提升处理复杂问题的能力。
    - 自进化：无需显式要求，模型在自探索中演化出了自验证、搜索等高级功能。

:::color5
**<font style="color:#601BDE;">5. 核心理念</font>**

:::

<font style="color:rgb(0, 0, 0);">AIME2024数学推理效果提升非常明显，从15</font>**<font style="color:rgb(0, 0, 0);">.6%到71%</font>**<font style="color:rgb(0, 0, 0);">（达到了OpenAI-O1-0912水平）</font>

+ <font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">它坚定的表明，不借助监督学习(SFT) </font><font style="color:#DF2A3F;">只靠RL可以原生、自发的进化出来强大的reasoning能力</font><font style="color:rgb(0, 0, 0);">，比如反思、多种方式尝试等。</font>
+ <font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">内部分析表明，随着推理步数的增加，reasoning效果明显变化（蓝色曲线）；且通过多数投票方式majority voting，还能再提升效果到</font>**<font style="color:rgb(0, 0, 0);">86.7%</font>**
+ <font style="color:rgb(0, 0, 0);">模型会自发出现</font><font style="color:#DF2A3F;">拟人化的思考过程</font>**<font style="color:rgb(0, 0, 0);">。</font>**

## R1
:::color3
为了输出可读、并对齐人类偏好，且只需少量高质量的样本数据就强大的reasoning能力，开启了R1 正规训练。它基于DS-v3-base，经历了4个训练阶段：

:::

### <font style="color:#4C16B1;">冷启动：高质量微调: 增强可读性</font>
+ 收集了少量高质量的CoT数据来做模型微调：初始化RL actor。这部分样本数据非常关键，尝试了多种方式：给少样本few-shot CoT作为输入，让模型产输出反思、验证的过程。
+ 从R1-Zero中筛选部分prompt 并格式化，并通过人工来调整结果  
注：报告里含糊说大概<font style="color:#DF2A3F;">几千上万条</font>，但没说具体数字。

  
通过冷启动微调，模型具备了以下2类能力  
●输出可读性强：包括最后的输出会做summary；以及格式更优化。同时系统会过滤掉可读性差的输出（产生了 但不会给用户？）  
●模型效果更好：对齐了人类偏好。

### <font style="color:#4C16B1;">第一轮RL：获得reasoning能力</font>
  
采用R1-Zero的训练过程。重点在数学、编程、科学、逻辑规划方面的强化学习训练。直至收敛。  
●过程中，仍然观察到经常出现多种语言混杂情况，为此引入了一个"language consistency reward"：统计出现的语言类型-字符数，最终可读性增强（虽然模型效果略微下降）

### <font style="color:#4C16B1;">微调SFT</font>
  
RL结束后，利用其模型再次产生一批prompt和response：和冷启动不同，本阶段要在各种领域问题里采集样本，包括通用知识、总结、创作等，包括  
●通过阶段2的模型获得600K reasoning data：包括拒绝采样等手段，过滤掉只保留正确、可读的输出。  
●通过DS-v3-base 获得200K non-reasoning data：写作、翻译、事实性问答  
最终合计<font style="color:#DF2A3F;">800K</font> 样本，只微调2个epoch。

### 第二轮RL：全域强化学习
  
目的是保留和微调reasoning能力的同时，重点增强有用性（helpfulness）和无害型（harmlessness）。  
●通过比较丰富多样的prompt（不同样本分布）、多种reward model组合  
●对reansoning prompt（数学、代码等）仍采用简单的rule-based的奖励信号；而对其他场景，采用人类对齐的reward model  
●有用性：只微调summary部分  
●无害性：则监督微调所有部分，包括reasoning过程 和 最终的summary。确保减少偏见、毒害等



### <font style="color:#000000;">GRPO（G</font><font style="color:rgb(64, 64, 64);">roup Relative Policy Optimization</font>）
:::color3
**简介**：<font style="color:rgb(64, 64, 64);">在DeepSeek-R1模型中，使用到的强化学习算法GRPO其实是DeepSeek之前的文章</font>_**<font style="color:rgb(64, 64, 64);">《DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models》</font>**_

<font style="color:rgb(64, 64, 64);">在目前大语言模型中进行微调的流程中，一般在SFT阶段之后，进一步通过强化学习对模型进行优化可以显著提升其性能。而</font>**<font style="color:rgb(64, 64, 64);">Group Relative Policy Optimization (GRPO)，就是使用在该阶段，替换传统的PPO算法。</font>**

**参考资料**：[DeepSeek的GRPO算法是什么？](https://www.zhihu.com/question/10766825126/answer/88583863333)

**源码实现**：[https://github.com/huggingface/open-r1/blob/main/src/open_r1/rewards.py](https://github.com/huggingface/open-r1/blob/main/src/open_r1/rewards.py)

**代码实现：**[GRPO核心代码实践](https://zhuanlan.zhihu.com/p/23349133287)

:::

GRPO 是一种在线学习算法（online learning algorithm），这意味着它通过使用训练过程中由训练模型自身生成的数据来迭代改进。GRPO 的目标直觉是最大化生成补全（completions）的优势函数（advantage），同时确保模型保持在参考策略（reference policy）附近。

<font style="color:rgb(25, 27, 31);">GRPO 就像是 PPO 的精简版。</font>**<font style="color:#74B602;">它保留了 PPO 的核心思想，但去掉了独立的价值函数（辅助教练），使其更轻量、更快速。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741320312999-67b4d632-0a3e-488f-a925-100da4b84ae8.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. <font style="color:rgb(25, 27, 31);">重要性采样是GRPO的核心机制：通过复用旧策略的样本，用重要性权重</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318225466-daf74867-a20b-48f4-aeb3-d16b300241be.png)<font style="color:rgb(25, 27, 31);">调整新策略的优化方向。</font>
2. <font style="color:rgb(25, 27, 31);">优势函数的作用：标准化后的奖励 </font><font style="color:rgb(25, 27, 31);">Ai</font><font style="color:rgb(25, 27, 31);"> 帮助策略区分高价值样本和低价值样本，引导模型优先提升高奖励输出的概率。</font>
3. <font style="color:rgb(25, 27, 31);">GRPO的工程优势：省去Critic价值模型，仅依赖组内奖励统计量，适合资源受限的场景。</font>

:::color5
**<font style="color:#601BDE;">2.与DPO/PPO的区别</font>**

:::

| **<font style="color:rgb(25, 27, 31);">特性</font>** | **<font style="color:rgb(25, 27, 31);">PPO</font>** | **<font style="color:rgb(25, 27, 31);">DPO</font>** | **<font style="color:rgb(25, 27, 31);">GRPO</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">是否需要奖励模型</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">否</font> |
| <font style="color:rgb(25, 27, 31);">是否需要辅助教练（价值函数）</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">否</font> |
| <font style="color:rgb(25, 27, 31);">训练效率</font> | <font style="color:rgb(25, 27, 31);">中等</font> | <font style="color:rgb(25, 27, 31);">高</font> | <font style="color:rgb(25, 27, 31);">高</font> |
| <font style="color:rgb(25, 27, 31);">适用场景</font> | <font style="color:rgb(25, 27, 31);">通用</font> | <font style="color:rgb(25, 27, 31);">简单任务</font> | <font style="color:rgb(25, 27, 31);">复杂推理任务</font> |


**<font style="color:#74B602;">为了解决PPO的缺点</font>**<font style="color:rgb(64, 64, 64);">，我们提出了 </font>**<font style="color:rgb(64, 64, 64);">Group Relative Policy Optimization (GRPO)</font>**<font style="color:rgb(64, 64, 64);">，不再需要像PPO那样加入额外的价值函数近似</font>_**<font style="color:rgb(64, 64, 64);">，而是直接使用多个采样输出的平均奖励作为Baseline</font>**_<font style="color:rgb(64, 64, 64);">，显著减少了训练资源的使用。</font>

**<font style="color:rgb(64, 64, 64);">GRPO与PPO的关联与区别：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812555603-dbee0aac-d740-44a1-9f32-60f3ef699f3a.png)

1. <font style="color:rgb(25, 27, 31);">PPO通常依赖一个独立的价值模型（Critic）来估计优势 </font><font style="color:rgb(25, 27, 31);">Ai</font><font style="color:rgb(25, 27, 31);">，需要额外训练一个模型。</font>
2. <font style="color:rgb(25, 27, 31);">GRPO的创新点：直接使用组内样本的奖励计算基线（如 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318126920-e319b774-623c-4c5c-9e45-829567f9719b.png)<font style="color:rgb(25, 27, 31);">），无需Critic模型，降低了计算成本。</font>
3. **<font style="color:rgb(25, 27, 31);">GRPO 直接比较候选响应的群体，无需额外的批评者模型</font>**<font style="color:rgb(25, 27, 31);">。对于给定的问题 q，GRPO 首先从当前策略 πθold 生成 G 个不同的响应 {o1, o2, ..., oG}。然后 GRPO 根据这些响应采取行动，并将获得的奖励表示为 {r1, r2, ..., rG}。通过计算它们的均值和标准差进行归一化，GRPO 确定这些响应的相对质量：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335086191-20af6668-2361-421b-a820-49700da58c3c.png)

<font style="color:rgb(25, 27, 31);">其中 Ai 表示第 i 个答案的相对质量。</font>**<font style="color:#ED740C;">GRPO 鼓励模型偏好群体内奖励值较高的更好答案</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.训练步骤（简化版）</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">生成一组响应</font>**<font style="color:rgb(25, 27, 31);">：对于每个提示，从 LLM 中生成多个响应的一组。</font>
2. **<font style="color:rgb(25, 27, 31);">对组进行打分（奖励模型）</font>**<font style="color:rgb(25, 27, 31);">：获取组内所有响应的奖励分数。</font>
3. **<font style="color:rgb(25, 27, 31);">计算组内相对优势（GRAE，基于组的优势骨架）</font>**<font style="color:rgb(25, 27, 31);">：通过比较每个响应的奖励与组内平均奖励来计算优势。在组内对奖励进行归一化以得到优势。</font>
    1. <font style="color:rgb(25, 27, 31);">GRPO 的魔法成分在于它如何估计优势。</font>**<font style="color:#74B602;">它不是使用辅助教练，而是使用一组由 LLM 生成的相同提示的响应来估计每个响应相对于组内其他响应的“好坏”</font>**<font style="color:rgb(25, 27, 31);">。</font>
4. **<font style="color:rgb(25, 27, 31);">优化策略（使用 GRAE 的 PPO 风格目标函数）</font>**<font style="color:rgb(25, 27, 31);">：使用一个 PPO 风格的目标函数更新 LLM 的策略，但使用这些组内相对优势。</font>

:::color5
**<font style="color:#601BDE;">4.实现步骤</font>**

:::

为了理解 GRPO 的工作原理，可以将其分解为四个主要步骤：

1. ** 生成补全（Generating completions）**

<font style="color:rgb(25, 27, 31);">在每一个训练步骤中，我们从提示（prompts）中采样一个批次（batch），并为每个提示生成一组 G 个补全（completions）（记为 o</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><font style="color:rgb(25, 27, 31);">）。</font>

2. ** 计算优势值（Computing the advantage）**

<font style="color:rgb(25, 27, 31);">对于每一个 G 序列，使用奖励模型（reward model）计算其奖励（reward）。为了与奖励模型的比较性质保持一致。通常奖励模型是基于同一问题的输出之间的比较数据集进行训练的。优势的计算反映了这些相对比较。其归一化公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327572180-c8af0f92-d170-4f1f-8c7a-4e9f796b8734.png)

<font style="color:rgb(25, 27, 31);">这种方法赋予了该方法其名称：</font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（Group Relative Policy Optimization, GRPO）</font>**

GRPO通过优化PPO算法，解决了**<font style="color:#74B602;">计算优势值时需要同时依赖奖励模型（reward model）和价值模型（value model）的问题，成功移除了value model（价值模型）</font>**，**<font style="color:#ED740C;">显著降低了推理时的内存占用和时间开销</font>**。**<font style="color:#ED740C;">Advantage（优势值）的核心价值在于为模型输出提供更精准的评估</font>**，不仅衡量答案的绝对质量，还通过相对比较（与其他回答的对比）来更全面地定位其优劣。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812555603-dbee0aac-d740-44a1-9f32-60f3ef699f3a.png)

3. ** 估计KL散度（Estimating the KL divergence）**

在实际算法实现中，直接计算KL散度可能会面临一些挑战：

+ **计算复杂度高**：KL散度的定义涉及对两个概率分布的对数比值的期望计算。对于复杂的策略分布，直接计算KL散度可能需要大量的计算资源；
+ **数值稳定性**：在实际计算中，直接计算KL散度可能会遇到数值不稳定的问题，尤其是当两个策略的概率分布非常接近时，对数比值可能会趋近于零或无穷大。近似器可以通过引入一些数值稳定性的技巧（如截断或平滑）来避免这些问题；
+ **在线学习**：在强化学习中，策略通常需要在每一步或每几步更新一次。如果每次更新都需要精确计算KL散度，可能会导致训练过程变得非常缓慢。近似器可以快速估计KL散度，从而支持在线学习和实时更新。

**使用近似器来估计KL散度**

[Schulman et al. (2020)](https://link.zhihu.com/?target=http%3A//joschu.net/blog/kl-approx.html)<font style="color:rgb(25, 27, 31);"> 提出的</font>**<font style="color:#ED740C;">近似器</font>**<font style="color:rgb(25, 27, 31);">可以根据当前策略和参考策略的差异动态调整估计的精度，从而在保证计算效率的同时，尽可能减少估计误差，其定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327720687-37130509-39b0-441a-939c-99d21b3325cc.png)

<font style="color:rgb(25, 27, 31);">这个近似器的优势在于它只需要</font>**<font style="color:#ED740C;">计算当前策略和参考策略的概率比值，而不需要直接计算KL散度的积分或期望。因此，它可以在保证一定精度的同时，显著降低计算复杂度。</font>**

4. ** 计算损失（Computing the loss）**

<font style="color:rgb(25, 27, 31);">这一步的目标是最大化优势，同时确保模型保持在参考策略附近。因此，损失定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327776028-b54b4f85-952c-4d47-abed-9fc4141d541e.png)

<font style="color:rgb(25, 27, 31);">其中第一项表示缩放后的优势，第二项通过KL散度惩罚与参考策略的偏离。</font>

:::color5
**<font style="color:#601BDE;">3.伪代码实现</font>**

:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def grae_advantages(rewards):
    """概念性组相对优势估计（结果监督）。"""
    mean_reward = np.mean(rewards)
    std_reward = np.std(rewards)
    normalized_rewards = (rewards - mean_reward) / (std_reward + 1e-8)
    advantages = normalized_rewards  # 对于结果监督，优势 = 归一化奖励
    return advantages


def grpo_loss(old_policy_logprobs_group, new_policy_logprobs_group, group_advantages, kl_penalty_coef, clip_epsilon):
    """概念性 GRPO 损失函数（对一组响应取平均）。"""
    group_loss = 0
    for i in range(len(group_advantages)):  # 遍历组内的每个响应
        advantage = group_advantages[i]
        new_policy_logprob = new_policy_logprobs_group[i]
        old_policy_logprob = old_policy_logprobs_group[i]

        ratio = np.exp(new_policy_logprob - old_policy_logprob)
        clipped_ratio = np.clip(ratio, 1 - clip_epsilon, 1 + clip_epsilon)
        surrogate_objective = np.minimum(ratio * advantage, clipped_ratio * advantage)
        policy_loss = -surrogate_objective

        kl_divergence = new_policy_logprob - old_policy_logprob
        kl_penalty = kl_penalty_coef * kl_divergence
        group_loss += (policy_loss + kl_penalty)  # 累加组内每个响应的损失

    return group_loss / len(group_advantages)  # 对组内损失取平均
```

:::color5
**<font style="color:#601BDE;">3.核心代码</font>**

:::

1. **构造训练数据**：基于<font style="color:rgb(25, 27, 31);">Qwen-2.5-7B:</font>

```plain
'<|im_start|>system
用户和助手之间的对话。用户提出问题，助手解决问题。助手首先在脑海中思考推理过程，然后为用户提供答案。推理过程和答案分别包含在<think></think>和<answer></answer>标签中，即这里的<think>推理过程</think><answer>在这里回答</ansure><|im_end|>
<|im_start|>user
Kim今天参加数学考试的概率是$\frac{4}{7}$。Kim今天没有数学考试的可能性有多大？用普通分数表示你的答案<|im_end |>
<|im_start|>助手'
```

```json
“<think>这个问题给了我们金今天有数学考试的概率，即\\（\\frac{4}{7}\\）。一个事件没有发生的概率是1减去事件发生的概率。因此，我们需要从1中减去\\frac{14}{7}\\，得出金今天没有数学考试的概率。
要执行这个减法，我们可以将1表示为与\\frac[4}{7]\\具有相同分母的分数。这给了我们\\（1=\\frac[7}{7}\\ 
因此，金今天没有数学考试的概率是\\（\\frac{7}{7}-\\frac{14}{7]\\。
让我们进行减法运算以找到最终答案。
</think>
<answer>金今天没有数学考试的概率是\\（\\frac{3}{7}\\）</答案><|im_end|>“
```

2. **数据标注：**用<font style="color:rgb(25, 27, 31);">使用专业的数学verifier判断两个答案是否对，对的话reward就是1，否则就是0。这种设计非常适用于数学题等任务，因为答案的正确性可以直接通过对比来判断。</font>
3. **<font style="color:rgb(25, 27, 31);">奖励函数实现：</font>**<font style="color:rgb(25, 27, 31);">在 GRPO 中，奖励函数的设计至关重要。首先我们就来看看这个奖励函数是啥，代码中提供了一个简单的奖励函数 </font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">accuracy_reward</font>](https://zhida.zhihu.com/search?content_id=253691962&content_type=Article&match_order=1&q=accuracy_reward&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">，用于判断生成的输出是否正确。</font>

```python
def accuracy_reward(completions, solution, **kwargs):
    """Reward function that checks if the completion is the same as the ground truth."""
    contents = [completion[0]["content"] for completion in completions]
    rewards = []
    for content, sol in zip(contents, solution):
        gold_parsed = parse(
            sol,
            extraction_mode="first_match",
            extraction_config=[LatexExtractionConfig()],
        )
        if len(gold_parsed) != 0:
            # We require the answer to be provided in correct latex (no malformed operators)
            answer_parsed = parse(
                content,
                extraction_config=[
                    LatexExtractionConfig(
                        normalization_config=NormalizationConfig(
                            nits=False,
                            malformed_operators=False,
                            basic_latex=True,
                            equations=True,
                            boxed="all",
                            units=True,
                        ),
                        # Ensures that boxed is tried first
                        boxed_match_priority=0,
                        try_extract_without_anchor=False,
                    )
                ],
                extraction_mode="first_match",
            )
            # Reward 1 if the content is the same as the ground truth, 0 otherwise
            try:
                reward = float(verify(answer_parsed, gold_parsed))
            except Exception as e:
                print(f"verify failed: {e}, answer: {answer_parsed}, gold: {gold_parsed}")
                reward = 0.0
        else:
            # If the gold solution is not parseable, we reward 1 to skip this example
            reward = 1.0
            print("Failed to parse gold solution: ", sol)
        rewards.append(reward)

    return rewards
```

4. **GRPO trainer核心代码解析**

```python
def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
    if return_outputs:
        raise ValueError("The GRPOTrainer does not support returning outputs")
        # Compute the per-token log probabilities for the model

        prompt_ids, prompt_mask = inputs["prompt_ids"], inputs["prompt_mask"]
    completion_ids, completion_mask = inputs["completion_ids"], inputs["completion_mask"]
    input_ids = torch.cat([prompt_ids, completion_ids], dim=1)
    attention_mask = torch.cat([prompt_mask, completion_mask], dim=1)
    logits_to_keep = completion_ids.size(1)  # we only need to compute the logits for the completion tokens

    per_token_logps = self._get_per_token_logps(model, input_ids, attention_mask, logits_to_keep)

    # Compute the KL divergence between the model and the reference model
    if self.beta != 0.0:
        ref_per_token_logps = inputs["ref_per_token_logps"]
        per_token_kl = (
            torch.exp(ref_per_token_logps - per_token_logps) - (ref_per_token_logps - per_token_logps) - 1
        )

        # Compute the loss
        advantages = inputs["advantages"]
    # When using num_iterations == 1, old_per_token_logps == per_token_logps, so we can skip it's computation (see
    # _generate_and_score_completions) and use per_token_logps.detach() instead.
    old_per_token_logps = inputs["old_per_token_logps"] if self.num_iterations > 1 else per_token_logps.detach()
    coef_1 = torch.exp(per_token_logps - old_per_token_logps)
    coef_2 = torch.clamp(coef_1, 1 - self.epsilon, 1 + self.epsilon)
    per_token_loss1 = coef_1 * advantages.unsqueeze(1)
    per_token_loss2 = coef_2 * advantages.unsqueeze(1)
    per_token_loss = -torch.min(per_token_loss1, per_token_loss2)
    if self.beta != 0.0:
        per_token_loss = per_token_loss + self.beta * per_token_kl
        loss = (per_token_loss * completion_mask).sum() / completion_mask.sum()

    # Log the metrics
    mode = "eval" if self.control.should_evaluate else "train"

    if self.beta != 0.0:
        mean_kl = (per_token_kl * completion_mask).sum() / completion_mask.sum()
        self._metrics[mode]["kl"].append(self.accelerator.gather_for_metrics(mean_kl).mean().item())

        is_clipped = (per_token_loss1 < per_token_loss2).float()
    clip_ratio = (is_clipped * completion_mask).sum() / completion_mask.sum()
    self._metrics[mode]["clip_ratio"].append(self.accelerator.gather_for_metrics(clip_ratio).mean().item())
    return loss
```

### <font style="color:rgb(0, 0, 0);">蒸馏</font>
<font style="color:rgb(0, 0, 0);">以R1为教师，选择Qwen2.5 的4个模型（1.5b ~ 32b）和Llama3 2个模型（8b，70b）进行SFT微调（蒸馏）</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">数据准备：671b教师模型</font><font style="color:rgb(58, 58, 58);">生成的高质量推理数据样本，然后作为作为学生模型的训练样本。</font>

<font style="color:rgb(64, 64, 64);">○</font><font style="color:rgb(58, 58, 58);">数据增强：进一步扩展、修改和优化，以多样性和代表性。</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">蒸馏: SFT方式，学习教师模型的输出概率。DS的一些重要优化</font>

<font style="color:rgb(64, 64, 64);">○</font><font style="color:rgb(58, 58, 58);">混合损失函数设计：</font>**<font style="color:rgb(58, 58, 58);">soft label + hard label结合</font>**<font style="color:rgb(58, 58, 58);">，从教师学的快 且 学的对。</font>

<font style="color:rgb(64, 64, 64);">■</font><font style="color:rgb(58, 58, 58);">soft label: 输出概率分布去接近教师模型。</font>

<font style="color:rgb(64, 64, 64);">■</font><font style="color:rgb(58, 58, 58);">hard label: 输出概率分布去接近真值。</font>

<font style="color:rgb(64, 64, 64);">○</font><font style="color:rgb(58, 58, 58);">共享参数和其他一些训练trick:</font>

<font style="color:rgb(64, 64, 64);">■</font><font style="color:rgb(58, 58, 58);">温度调整调整soft label：使分布更加平滑。随着训练进行，温度参数逐渐降低。</font>

<font style="color:rgb(64, 64, 64);">■</font>**<font style="color:rgb(58, 58, 58);">学习率</font>**<font style="color:rgb(58, 58, 58);">动态调整</font>

<font style="color:rgb(64, 64, 64);">■</font>**<font style="color:rgb(58, 58, 58);">L2 正则化</font>**<font style="color:rgb(58, 58, 58);">防止过拟合</font>

### <font style="color:rgb(0, 0, 0);">R1效果评估</font>
<font style="color:rgb(0, 0, 0);">逻辑推理能力对齐O1; 指令跟随能力增强；相比GPT回答更简洁（600~2K token）</font>

<font style="color:rgb(0, 0, 0);">相比DS-v3：</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">reasoning提升非常显著</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">其他通用能力或多或少也有提升。例外：中文simpleQA测试集上下降5个点：可能因为拒绝回答。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738811991636-026d158b-59a2-4f72-b173-4706eb9d582d.png)



<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">32b 和70b的模型</font>**<font style="color:rgb(0, 0, 0);">均达到了O</font>**<font style="color:rgb(0, 0, 0);">penAI-O1-mini水平（略超）。llama-70b模型效果最强（也最大）。</font>

<font style="color:rgb(64, 64, 64);">○</font><font style="color:rgb(0, 0, 0);">1.5b的数学、代码模型</font>**<font style="color:rgb(0, 0, 0);">与Claude-3.5-Sonnet基本持平</font>**

<font style="color:rgb(64, 64, 64);">○</font><font style="color:rgb(0, 0, 0);">蒸馏的Qwen-32b的模型比阿里早期发布的QwQ-32B效果明显更强</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(0, 0, 0);">如果不做蒸馏而直接在32b模型做大规模的强化学习，其reasoning能力比蒸馏学习</font>**<font style="color:rgb(0, 0, 0);">差很多</font>**<font style="color:rgb(0, 0, 0);">。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(0, 0, 0);">蒸馏小模型仍落后于教师模型R1</font>**<font style="color:rgb(0, 0, 0);">，见最后一行加的对比数字。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812056039-12196a28-258f-44ba-a756-3ff1e2d5fdae.png)

# [deepseek v3](https://www.zhihu.com/question/8423473404)
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：deepseek发布了其最新的大型语言模型 DeepSeek-V3，这款模型在性能和效率方面都取得了显著的进步，成为当前最强大的开源基础模型之一。</font>**<font style="color:#ED740C;">DeepSeek-V3 是一款拥有 671B参数的大型混合专家 (MoE) 模型</font>**<font style="color:rgb(51, 51, 51);">，其中每个 token 会有 37 B参数被激活。</font>

:::

:::color5
**<font style="color:#601BDE;">创新点</font>**

:::

为了实现高效的推理和成本效益的训练，[DeepSeek-V3](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=5&q=DeepSeek-V3&zhida_source=entity) 采用了以下策略：

1. 多头潜在注意力 (MLA, Multi-Head Latent Attention)  .
2. [DeepSeekMoE](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=DeepSeekMoE&zhida_source=entity) 架构，这两个架构在 DeepSeek-V2 中已经得到了充分验证。
3. 此外，DeepSeek-V3 还开创了一种无辅助损失策略来平衡负载.
4. 多 token 预测：多token预测 的训练目标以进一步提升性能。.

### 冷启动训练  
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">DeepSeek的Soft Fine-Tuning（SFT）过程是一种结合了软参数调整和知识蒸馏的微调方法，旨在在保持模型预训练知识的同时，有效适应新的任务数据。以下是SFT的详细步骤和冷启动的必要性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.SFT过程</font>**

:::

1. **预训练模型加载**：
    - <font style="color:rgb(51, 51, 51);">首先加载已经在大规模通用数据集上预训练好的模型。这个预训练模型包含丰富的语义信息和语言理解能力，是SFT的基础。</font>
2. **任务适配**：
    - <font style="color:rgb(51, 51, 51);">根据具体的微调任务，对模型进行适配。这可能包括添加任务特定的输出层、修改部分参数，或者调整模型的结构以适应新任务的需求。</font>
3. **软参数调整**：
    - <font style="color:rgb(51, 51, 51);">在微调过程中，采用软参数调整技术，逐步更新模型参数。这种方法旨在保留预训练模型的泛化能力，同时使模型适应新的任务数据。与传统的微调相比，软参数调整更加温和，避免模型参数的大规模变化。</font>
4. **知识蒸馏**：
    - <font style="color:rgb(51, 51, 51);">引入知识蒸馏技术，利用教师模型对学生的微调过程进行指导。教师模型通常是更大或性能更好的预训练模型，通过传递知识，帮助学生模型更好地理解和掌握复杂的语义关系。</font>
5. **冷启动策略**：
    - <font style="color:rgb(51, 51, 51);">在微调的初始阶段，采用冷启动策略，帮助模型平稳过渡到微调任务。冷启动阶段的重点是保持预训练模型的知识，避免在微调初期出现模型性能的下降或不稳定。</font>

:::color5
**<font style="color:#601BDE;">2.冷启动的必要性</font>**

:::

1. **平滑过渡**：
    - <font style="color:rgb(51, 51, 51);">冷启动帮助模型在预训练状态和微调任务之间实现平滑过渡。通过较低的学习率和混合数据加载策略，模型能够在不丢失预训练知识的前提下，逐步适应新的任务数据。</font>
2. **防止过早遗忘**：
    - <font style="color:rgb(51, 51, 51);">在微调初期，使用较低的学习率可以防止模型过早地遗忘预训练阶段学到的大量知识。这使得模型在后续的微调过程中能够更好地结合新旧知识，提升最终的性能。</font>
3. **提升训练稳定性**：
    - <font style="color:rgb(51, 51, 51);">冷启动阶段通过特定的数据加载策略和学习率调度，提高了微调过程的稳定性。这对于防止模型在训练初期出现梯度爆炸或不稳定现象至关重要。</font>
4. **优化计算资源**：
    - <font style="color:rgb(51, 51, 51);">通过在冷启动阶段有效地利用预训练数据，SFT方法减少了对计算资源的浪费。混合数据加载策略使得模型能够在微调初期充分利用预训练数据的优势，提升训练效率。</font>



### <font style="color:rgb(25, 27, 31);">R1推理(Reasoning)训练范式</font>
### DeepSeekMOE:
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">混合专家模型（MOE, Mix of Experts）</font>**<font style="color:rgb(51, 51, 51);"> 是一种将多个专家网络结合在一起的模型结构，旨在通过专家间的协作提升模型的整体性能。MOE的核心思想是将输入数据动态地分配给不同的专家进行处理，每个专家专注于特定的任务或数据区域。这种方法结合了专家的高效性与模型的灵活性，能够更好地适应复杂的自然语言处理任务。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740121752045-99272fcc-35c7-4179-bc50-860e90243522.png)

<font style="color:rgb(51, 51, 51);">MOE的工作原理可以分为以下几个关键步骤：</font>

+ **<font style="color:rgb(51, 51, 51);">专家网络</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">每个专家网络（Expert）都是一个独立的子模型，负责处理特定类型的数据或任务。</font>
+ **<font style="color:rgb(51, 51, 51);">gating机制</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">通过一个 gating网络（Gate），根据输入数据的特征，动态地确定将输入分配给哪个专家进行处理。</font>
+ **<font style="color:rgb(51, 51, 51);">混合输出</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">最终的模型输出是各个专家输出的加权和，权值由 gating机制确定。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **输入数据准备**：
    - <font style="color:rgb(51, 51, 51);">将输入文本转换为词嵌入向量。</font>

```python
# 示例：词嵌入转换
input = "This is an example sentence."
word_embeddings = embedding_layer(input)
```

2. **专家网络处理**：
    - <font style="color:rgb(51, 51, 51);">将词嵌入向量输入到多个专家网络中，每个专家独立地对输入进行处理。</font>

```python
# 示例：专家网络定义
expert1_output = expert1_net(word_embeddings)
expert2_output = expert2_net(word_embeddings)
# 依此类推...
```

3. ** gating机制计算**：
    - <font style="color:rgb(51, 51, 51);">使用 gating网络根据输入数据计算出各个专家的权重。</font>

```python
# 示例： gating权重计算
gate_input = gate_layer(word_embeddings)
gating_weights = softmax(gate_layer_output)
```

4. **混合专家输出**：
    - <font style="color:rgb(51, 51, 51);">根据 gating权重，将各个专家的输出进行加权求和，得到最终的模型输出。</font>

```python
# 示例：混合输出计算
final_output = sum(expert_output * gating_weight for expert_output, gating_weight in zip(expert Outputs, gating_weights))
```

1. **损失计算与优化**：
    - <font style="color:rgb(51, 51, 51);">根据模型的损失函数（如交叉熵损失），优化模型参数，包括专家网络和 gating网络的参数。</font>

```python
# 示例：损失计算与优化
loss = loss_fn(final_output, target)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **高效率**：
    - <font style="color:rgb(51, 51, 51);">通过专家的分工合作，MOE能够更高效地处理复杂的任务，减少计算开销。</font>
+ **灵活性高**：
    - <font style="color:rgb(51, 51, 51);">可以根据具体任务需求灵活地添加或删除专家，适应不同的应用场景。</font>
+ **适应性强**：
    - <font style="color:rgb(51, 51, 51);">专家网络可以专注于不同的数据分布或任务特点，提升模型的整体适应能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **训练难度大**：
    - <font style="color:rgb(51, 51, 51);">MOE的复杂结构增加了训练的难度，需要更精细的优化策略和更长的训练时间。</font>
+ **潜在的冗余**：
    - <font style="color:rgb(51, 51, 51);">专家网络之间可能存在重叠的功能，导致计算资源的浪费。</font>
+ **实现复杂**：
    - <font style="color:rgb(51, 51, 51);">相较于传统的模型结构，MOE的实现复杂度较高，需要额外的 gating机制和混合层设计。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

**<font style="color:rgb(51, 51, 51);">文本生成</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">在文本生成任务中，不同的专家可以专门处理不同类型的内容或语境，提升生成文本的多样性和质量。</font>

**<font style="color:rgb(51, 51, 51);">机器翻译</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">MOE可以通过不同的专家分别处理源语言和目标语言的语法、句式特点，提升翻译的准确率和流畅度。</font>

**<font style="color:rgb(51, 51, 51);">问答系统</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">各个专家可以专注于不同的领域或问题类型，提供更专业和准确的回答。</font>

**<font style="color:rgb(51, 51, 51);">文本摘要</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">专家可以分别处理文本的不同部分或主题，生成内容更为全面和结构合理的摘要。</font>

**<font style="color:rgb(51, 51, 51);">情感分析</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">不同的专家可以专注于不同的情感极性或情感类别，提升情感分析的准确性和细致程度。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

<font style="color:rgb(51, 51, 51);">为了克服MOE的局限性，可以采用以下改进方法：</font>

1. **优化 gating机制**：
    - <font style="color:rgb(51, 51, 51);">使用更为高效和准确的 gating机制，如多层感知机 gating、注意力 gating等，提升专家选择的准确性和灵活性。</font>
2. **减少专家数量**：
    - <font style="color:rgb(51, 51, 51);">通过降低专家的数量，减少模型的复杂性和计算开销，同时保持性能的提升。</font>
3. **专家网络共享参数**：
    - <font style="color:rgb(51, 51, 51);">允许专家网络共享部分参数，减少参数冗余，提升模型的训练效率和表达能力。</font>
4. **层次化专家设计**：
    - <font style="color:rgb(51, 51, 51);">在模型的不同层次上设计专家网络，分别处理不同粒度的信息，增强模型的层次化能力。</font>
5. **动态专家选择**：
    - <font style="color:rgb(51, 51, 51);">在推理阶段，根据输入数据的实时特征动态地选择最优专家，提升模型的适应性和响应速度。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import numpy as np

class Expert(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(Expert, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

class_gate(nn.Module):
    def __init__(self, input_dim, num_experts):
        super(_gate, self).__init__()
        self.fc = nn.Linear(input_dim, num_experts)
    
    def forward(self, x):
        return F.softmax(self.fc(x), dim=-1)

class MOEModel(nn.Module):
    def __init__(self, input_dim, num_experts, expert_hidden_dim, output_dim):
        super(MOEModel, self).__init__()
        self.experts = nn.ModuleList([
            Expert(input_dim, expert_hidden_dim, output_dim) for _ in range(num_experts)
        ])
        self.gate = _gate(input_dim, num_experts)

    def forward(self, x):
        # 获取 gating权重
        gate_weights = self.gate(x)
        # 专家输出
        expert_outputs = [expert(x) * gate_weights[:, i].unsqueeze(-1) for i, expert in enumerate(self.experts)]
        # 混合输出
        output = sum(expert_outputs)
        return output

# 示例用法
input_dim = 300  # 输入维度
num_experts = 4  # 专家数量
expert_hidden_dim = 256  # 专家隐藏层维度
output_dim = 10  # 输出维度

# 初始化MOE模型
model = MOEModel(input_dim, num_experts, expert_hidden_dim, output_dim)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# 准备数据
texts = [...]  # 加载文本数据
labels = [...]  # 加载对应标签

train_dataset = Dataset(texts, labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 训练模型
for epoch in range(num_epochs):
    model.train()
    for batch, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

# 评估模型
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for x, y in val_loader:
        outputs = model(x)
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == y).sum().item()
        total += y.size(0)
print(f"Validation Accuracy: {correct / total:.3f}")

```



### <font style="color:rgb(25, 27, 31);">MLA ： </font>[<font style="color:rgb(25, 27, 31);">多头潜在注意力</font>](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=2&q=%E5%A4%9A%E5%A4%B4%E6%BD%9C%E5%9C%A8%E6%B3%A8%E6%84%8F%E5%8A%9B&zhida_source=entity) Multihead Latent Attention
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">多头潜在注意力（MLA，Multi-Head Latent Attention）是DeepSeek公司提出的一种改进的注意力机制，旨在提升大型语言模型对文本的理解和生成能力。MLA的核心思想是引入潜在空间，通过对文本在潜在空间中的表示，增强模型捕捉语义信息的能力，从而提升模型的性能。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740121752045-99272fcc-35c7-4179-bc50-860e90243522.png)

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

<font style="color:rgb(51, 51, 51);">MLA的工作原理可以分为以下几个步骤：</font>

1. **输入嵌入**：
    - <font style="color:rgb(51, 51, 51);">将输入文本首先转换为词嵌入（Word Embedding），获取每个词的向量表示。</font>
2. **潜在空间映射**：
    - <font style="color:rgb(51, 51, 51);">将词嵌入映射到一个潜在空间，生成潜在向量（Latent Vectors）。这一步通过一个可学习的线性变换实现：  
</font><font style="color:rgb(51, 51, 51);">L=</font>_<font style="color:rgb(51, 51, 51);">Wl*X</font>_<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中，Wl 是映射矩阵，X 是输入的词嵌入矩阵。</font>
3. **多头注意力计算**：
    - <font style="color:rgb(51, 51, 51);">在潜在空间中，对潜在向量进行多头自注意力机制计算。具体来说，每个头（Head）执行以下步骤：</font>
        * **<font style="color:rgb(51, 51, 51);">线性变换</font>**<font style="color:rgb(51, 51, 51);">：将潜在向量投影到查询（Query）、键（Key）、值（Value）空间。</font>
        * **<font style="color:rgb(51, 51, 51);">计算注意力权重</font>**<font style="color:rgb(51, 51, 51);">：通过点积和归一化，计算每个查询与所有键的注意力权重。</font>
        * **<font style="color:rgb(51, 51, 51);">加权求和</font>**<font style="color:rgb(51, 51, 51);">：根据注意力权重对值向量进行加权求和，得到每个查询的注意力输出。</font>
4. **潜在空间反映射**：
    - <font style="color:rgb(51, 51, 51);">将多头注意力的结果从潜在空间映射回原始嵌入空间：  
</font><font style="color:rgb(51, 51, 51);">O=Wo*Y  
</font><font style="color:rgb(51, 51, 51);">其中，Wo 是反映射矩阵，Y</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是多头注意力的输出。</font>
5. **输出**：
    - <font style="color:rgb(51, 51, 51);">最终的输出作为模型后续层的输入，如前馈神经网络（FFN）或其他的变换。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **增强语义捕捉**：
    - <font style="color:rgb(51, 51, 51);">通过潜在空间的映射，MLA能够更有效地捕捉文本中的语义信息，特别是处理长距离依赖关系。</font>
+ **提升生成质量**：
    - <font style="color:rgb(51, 51, 51);">在文本生成任务中，MLA能够生成更为连贯和合理的文本内容。</font>
+ **增强模型的泛化能力**：
    - <font style="color:rgb(51, 51, 51);">潜在空间的引入使得模型能够更好地泛化到未见的数据，提升模型的鲁棒性。</font>
+ **灵活性高**：
    - <font style="color:rgb(51, 51, 51);">MLA的架构灵活，可以与多种模型结构相结合，适应不同的任务需求。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **计算复杂度高**：
    - <font style="color:rgb(51, 51, 51);">由于引入了潜在空间和多头机制，MLA的计算复杂度显著增加，尤其是在处理长序列时，计算资源消耗较大。</font>
+ **参数量增加**：
    - <font style="color:rgb(51, 51, 51);">为了实现潜在空间的映射和多头机制，MLA需要额外的参数，增加了模型的复杂性和训练难度。</font>
+ **实现复杂**：
    - <font style="color:rgb(51, 51, 51);">与传统的自注意力机制相比，MLA的实现更为复杂，需要更多的调试和优化。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **文本生成**：
    - <font style="color:rgb(51, 51, 51);">在大语言模型中，MLA能够生成更为自然和流畅的文本，尤其在对话生成和文本摘要任务中表现出色。</font>
+ **机器翻译**：
    - <font style="color:rgb(51, 51, 51);">MLA能够更准确地捕捉源语言和目标语言之间的语义关联，提高机器翻译的准确率和自然度。</font>
+ **问答系统**：
    - <font style="color:rgb(51, 51, 51);">在问答系统中，MLA能够更好地理解问题的语义，生成更相关的答案。</font>
+ **文本摘要**：
    - <font style="color:rgb(51, 51, 51);">MLA在文本摘要任务中表现出色，能够生成内容丰富且结构合理的摘要。</font>

:::color5
**<font style="color:#601BDE;">4.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MLA(nn.Module):
    def __init__(self, d_model, num_heads, d_latent):
        super(MLA, self).__init__()
        self.num_heads = num_heads
        self.d_latent = d_latent
        self.d_model = d_model
        
        # 映射到潜在空间
        self.W_l = nn.Linear(d_model, d_latent)
        # 反映射回原始空间
        self.W_o = nn.Linear(d_latent * num_heads, d_model)
        
        # 多头权重
        self.W_q = nn.Linear(d_latent, d_latent)
        self.W_k = nn.Linear(d_latent, d_latent)
        self.W_v = nn.Linear(d_latent, d_latent)
        
    def forward(self, x):
        # 输入形状: [batch_size, seq_len, d_model]
        batch_size = x.size(0)
        seq_len = x.size(1)
        
        # 映射到潜在空间
        l = self.W_l(x)  # [batch_size, seq_len, d_latent]
        
        # 分割到每个头
        head_size = self.d_latent
        l = l.view(batch_size, seq_len, self.num_heads, head_size)
        
        # 计算查询、键、值
        q = self.W_q(l)
        k = self.W_k(l)
        v = self.W_v(l)
        
        # 展开维度以准备点积
        q = q.permute(0, 2, 1, 3)  # [batch_size, num_heads, seq_len, head_size]
        k = k.permute(0, 2, 1, 3)  # [batch_size, num_heads, seq_len, head_size]
        v = v.permute(0, 2, 1, 3)  # [batch_size, num_heads, seq_len, head_size]
        
        # 计算注意力权重
        attention_scores = (q @ k.transpose(-2, -1)) / torch.sqrt(torch.tensor(head_size).float())
        attention_scores = F.softmax(attention_scores, dim=-1)
        
        # 应用注意力
        y = attention_scores @ v
        
        # 收缩回原始维度
        y = y.permute(0, 2, 1, 3)
        y = y.contiguous().view(batch_size, seq_len, self.num_heads * self.d_latent)
        
        # 映射回原始空间
        output = self.W_o(y)
        
        return output

```





### <font style="color:rgb(25, 27, 31);">DeepSeekMoE：辅助损失免费负载平衡</font>
<font style="color:rgb(25, 27, 31);">DeepSeekMoE 架构使用更细粒度的专家，并将一些专家隔离为共享专家。每个 token 的 FFN 输出 h’_t 通过以下步骤计算：</font>

<font style="color:rgb(25, 27, 31);">共享专家: 使用共享专家 FFN( ) (·) 计算共享专家的输出。</font>

<font style="color:rgb(25, 27, 31);">路由专家: 使用路由专家 FFN( ) (·) 计算路由专家的输出，并使用门控值 g_i,t 选择激活的专家。</font>

<font style="color:rgb(25, 27, 31);">输出: 将共享专家和路由专家的输出相加，得到最终的 FFN 输出 h’_t。</font>

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 还引入了一种辅助损失免费负载平衡策略，通过引入偏置项 b_i 并将其添加到相应的亲和度分数 s_i,t 中，来确定 top-K 路由。通过动态调整偏置项，DeepSeek-V3 能够在整个训练过程中保持平衡的专家负载，并取得比纯粹使用辅助损失的模型更好的性能。</font>

### <font style="color:rgb(25, 27, 31);">MTP(Multi-Token Prediction)多 token 预测</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">当前主流的大模型(LLMs)都是decoder-base的模型结构，也就是无论在模型训练还是在推理阶段，对于一个序列的生成过程，都是</font>**<font style="color:#74B602;">token-by-token</font>**<font style="color:rgb(25, 27, 31);">的。每次在生成一个token的时候，都要频繁跟访存交互，加载KV-Cache，再通过多层网络做完整的前向计算。</font>**<font style="color:#117CEE;">对于这样的访存密集型的任务，通常会因为访存效率形成训练或推理的瓶颈。</font>**

<font style="color:rgb(25, 27, 31);">针对token-by-token生成效率的瓶颈，业界很多方法来优化，包括减少存储的空间和减少访存次数等，进而提升训练和推理性能。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">DeepSeek-V3 采用了一种名为多 token 预测 (</font>[MTP](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=MTP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">) 的训练目标，该目标扩展了预测范围，以便在每个位置预测多个未来的 token。MTP 目标可以提高数据效率和模型的预测能力，并通过预先规划未来的 token 的表示来提升性能。</font>

<font style="color:rgb(25, 27, 31);">MTP 实现了 D 个连续的模块来预测 D 个额外的 token，每个模块都包含一个共享嵌入层、一个共享输出头、一个 Transformer 模块和一个投影矩阵。每个 MTP 模块都使用线性投影将 token 的表示和嵌入相连接，然后通过 Transformer 模块生成输出表示，并计算额外的预测 token 的概率分布。</font>

**paper：**[**DeepSeek-V3 Technical Report**](https://arxiv.org/pdf/2412.19437)

**参考：**[**MTP（Multi-Token Prediction）的前世今生**](https://zhuanlan.zhihu.com/p/18056041194)

:::

:::color5
**<font style="color:#601BDE;">1.MTP结构  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">DeepSeek的MTP的设计，如下图所示，乍看上去也是多头，但结构略复杂。且论文中也强调，在实现上保留了</font>**<font style="color:#74B602;">序列推理的连接关系（causal chain）</font>****<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">如图中，从一个Module链接到后继Module的箭头。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447961354-7887b237-cfa8-483d-a6f6-e7f00fcadf9f.png)

<font style="color:rgb(25, 27, 31);">如上图所示，用 </font><font style="color:rgb(25, 27, 31);">D</font><font style="color:rgb(25, 27, 31);"> 个顺序的模块，预测 </font><font style="color:rgb(25, 27, 31);">D</font><font style="color:rgb(25, 27, 31);"> 个tokens。每个MTP模块的具体结构：</font>

+ **<font style="color:rgb(25, 27, 31);">输入token首先接入一层共享的embedding layer</font>**
+ **<font style="color:rgb(25, 27, 31);">对于第</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">i</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">个token</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">i</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">和第</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">k</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">个预测深度</font>**
    - <font style="color:rgb(25, 27, 31);">我们首先将第 </font><font style="color:rgb(25, 27, 31);">k−1</font><font style="color:rgb(25, 27, 31);"> 层的的隐层输出 </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k−1</font></sup><font style="color:rgb(25, 27, 31);">∈R</font><sup><font style="color:rgb(25, 27, 31);">d</font></sup><font style="color:rgb(25, 27, 31);"> 做归一化处理 </font><font style="color:rgb(25, 27, 31);">RMSNorm(h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k−1</font></sup><font style="color:rgb(25, 27, 31);">)</font>
    - <font style="color:rgb(25, 27, 31);">再对第 </font><font style="color:rgb(25, 27, 31);">i+k</font><font style="color:rgb(25, 27, 31);"> 位置的token embedding：</font><font style="color:rgb(25, 27, 31);">Emb(t</font><sub><font style="color:rgb(25, 27, 31);">i+k</font></sub><font style="color:rgb(25, 27, 31);">)∈R</font><sup><font style="color:rgb(25, 27, 31);">d</font></sup><font style="color:rgb(25, 27, 31);"> 做归一化处理 </font><font style="color:rgb(25, 27, 31);">RMSNorm(Emb(t</font><sub><font style="color:rgb(25, 27, 31);">i+k</font></sub><font style="color:rgb(25, 27, 31);">))</font>
    - <font style="color:rgb(25, 27, 31);">将上述两个结果concat后，通过投影矩阵 </font><font style="color:rgb(25, 27, 31);">Mk∈R</font><sup><font style="color:rgb(25, 27, 31);">d×2d</font></sup><font style="color:rgb(25, 27, 31);"> 做一层线性变换得到 </font><font style="color:rgb(25, 27, 31);">h</font><sup><font style="color:rgb(25, 27, 31);">,</font></sup><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);">∈R</font><sub><font style="color:rgb(25, 27, 31);">d</font></sub>
    - <font style="color:rgb(25, 27, 31);">上述过程如下公式 </font><font style="color:rgb(25, 27, 31);">(21)</font><font style="color:rgb(25, 27, 31);"> 所示（当 </font><font style="color:rgb(25, 27, 31);">k=1</font><font style="color:rgb(25, 27, 31);"> 时， </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k−1</font></sup><font style="color:rgb(25, 27, 31);"> 对main model的隐层表征）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447803442-64cae6e8-c7db-42d8-b35d-16b4abeb25c8.png)

+ <font style="color:rgb(25, 27, 31);">再将 </font><font style="color:rgb(25, 27, 31);">h</font><sup><font style="color:rgb(25, 27, 31);">,</font></sup><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);"> 输入到Transformer层，获得第 </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 个预测深度的输出： </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);"> 。如公式 </font><font style="color:rgb(25, 27, 31);">(22)</font><font style="color:rgb(25, 27, 31);"> 所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447803244-ab56a9c2-f671-4e7d-9b54-5fd6aa347c2c.png)

+ <font style="color:rgb(25, 27, 31);">最后将 </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);"> 通过一个各Module共享的映射矩阵 </font><font style="color:rgb(25, 27, 31);">OutHead∈R</font><sup><font style="color:rgb(25, 27, 31);">V×d</font></sup><font style="color:rgb(25, 27, 31);"> 变换，再过 </font><font style="color:rgb(25, 27, 31);">softmax(.)</font><font style="color:rgb(25, 27, 31);"> 处理，计算出词表 </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);"> 维度的输出概率，这里注意： </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);">  的 </font><font style="color:rgb(25, 27, 31);">label</font><font style="color:rgb(25, 27, 31);"> 是对应 </font><font style="color:rgb(25, 27, 31);">i+1+k</font><font style="color:rgb(25, 27, 31);"> 位置的token。如公式 </font><font style="color:rgb(25, 27, 31);">(23)</font><font style="color:rgb(25, 27, 31);"> 所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447803319-fbdff04d-6926-424e-88ca-39b0fdda56f1.png)

:::color5
**<font style="color:#601BDE;">2.MTP模型训练  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**MTP多头训练，样本构建示意图**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744448119270-f03a2180-4741-4249-b1c7-fde5ccb9f7af.jpeg)

<font style="color:rgb(25, 27, 31);">通过CrossEntropyLoss计算每个MTP Module Head的损失，如公式</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">24</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744448148917-890a5386-3f91-48b7-80f8-080d3f6cab7c.png)

> 再解释下公式 (24) 的下标，2+k:T+1 表示label范围的下标  
参考上图8，就非常好理解：  
**起始下标 **2+k ：MTP Model 1 是预测 next next的token，也就是输入第一个token是 t1 ，预测第一个label token是 t(2+1)=t3 ，以此类推， MTP Model k，输入第一个token是 t1， 预测第一个token是 t2+k  
**结束下标 **T+1 ：所有sequence样本默认在原序列上额外增加的一个eos token，所以token下标为序列长度 T+1
>

<font style="color:rgb(25, 27, 31);">至此我们描述了deepseek V3 MTP的完整流程！！</font>

:::color5
**<font style="color:#601BDE;">3.MTP模型结构（解析版）  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744448393815-a2e69b39-b7dd-446a-abf0-ed877a3b4b52.jpeg)

:::color5
**<font style="color:#601BDE;">4.MTP模型推理  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">DeepSeek V3中强调，MTP的设计主要是为了训练过程能加速收敛，更充分的使用训练样本。所以针对推理阶段只是简单介绍了一段。这里也稍微展开讲下推理的过程。</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744448752409-5484a987-13b6-49fb-ae8c-f611fdfb36d3.jpeg)

<font style="color:rgb(25, 27, 31);">DeepSeek V3推理可以有两种方法：</font>

**<font style="color:rgb(25, 27, 31);">方法1</font>**<font style="color:rgb(25, 27, 31);">：直接把MTP Model头全部删掉，模型变成了一个Predict Next Token的 Main Model。然后部署模型做推理，这个就跟正常LLM模型推理一样。没有什么加速效果</font>

**<font style="color:rgb(25, 27, 31);">方法2：</font>**<font style="color:rgb(25, 27, 31);">保留MTP Model 做self-speculative decoding，这样充分使用多Head预测能力，提升推理加速性能。类似2.1中介绍的三阶段</font>

+ **<font style="color:rgb(25, 27, 31);">阶段1：predict （预测），</font>**<font style="color:rgb(25, 27, 31);">利用</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个Head一次生成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token，每个Head生成一个token</font>
+ **<font style="color:rgb(25, 27, 31);">阶段2：verify（验证），</font>**<font style="color:rgb(25, 27, 31);">将原始的序列和生成的token拼接，组成多个</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，将组装的多</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">组成一个Batch，一次发给</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">Main Model</font>**<font style="color:rgb(25, 27, 31);">做校验</font>
+ **<font style="color:rgb(25, 27, 31);">阶段3：accept（接受）</font>**<font style="color:rgb(25, 27, 31);">： 选择 </font><font style="color:rgb(25, 27, 31);">Head1</font><font style="color:rgb(25, 27, 31);"> 预估token与 </font><font style="color:rgb(25, 27, 31);">label</font><font style="color:rgb(25, 27, 31);"> 一致的最长 </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 作为可接受的结果。</font>



  


## 基础设施：高效训练的基石
DeepSeek-V3 的训练过程依赖于高效的计算集群和训练框架。

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810677717-4fcd48fa-b538-4705-895a-ebc17fb3cf40.webp)

### 计算集群
DeepSeek-V3 在一个配备 2048 个 NVIDIA H800 GPU 的集群上进行训练。每个节点包含 8 个 GPU，通过 [NVLink](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=NVLink&zhida_source=entity) 和 NVSwitch 相互连接。跨节点之间使用 InfiniBand (IB) 进行通信。

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810677797-4b88b97a-38e7-47b4-9b11-adeaf193a28f.webp)

### 训练框架
DeepSeek-V3 的训练框架基于 HAI-LLM 框架，该框架为高效训练提供了强大的支持。DeepSeek-V3 应用了 16 路 Pipeline Parallelism (PP)、64 路 Expert Parallelism (EP) 和 ZeRO-1 Data Parallelism (DP)。

**双向管道并行 (**[**DualPipe**](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=DualPipe&zhida_source=entity)**)**

为了解决跨节点专家并行导致的通信开销问题，DeepSeek-V3 设计了一种名为 DualPipe 的新型管道并行算法。DualPipe 通过重叠正向和反向计算通信阶段，不仅提高了模型训练速度，还减少了管道气泡的数量。

**跨节点全连接通信**

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 开发了高效的跨节点全连接通信内核，以充分利用 IB 和 NVLink 的带宽，并节省专门用于通信的 Streaming Multiprocessors (SMs)。</font>

**极低的内存占用**

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 通过以下技术来降低训练过程中的内存占用：</font>

[RMSNorm](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=RMSNorm&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 MLA 上投影的重新计算: 在</font>[反向传播](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=%E5%8F%8D%E5%90%91%E4%BC%A0%E6%92%AD&zhida_source=entity)<font style="color:rgb(25, 27, 31);">过程中重新计算所有 RMSNorm 操作和 MLA 上投影，从而消除了永久存储其输出激活的需求。</font>

<font style="color:rgb(25, 27, 31);">CPU 上的指数移动平均: 在训练过程中保存模型参数的指数移动平均 (EMA)，用于早期估计模型性能，并异步更新 EMA 参数，从而避免额外的内存和时间开销。</font>

<font style="color:rgb(25, 27, 31);">多 token 预测中的共享嵌入和输出头: 利用 DualPipe 策略，将模型的最浅层和最深层部署在同一个 PP 路径上，从而实现共享嵌入和输出头的参数和梯度，进一步提高内存效率。</font>

### <font style="color:rgb(25, 27, 31);">FP8 训练</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 支持使用 FP8 数据格式进行混合精度训练，以实现加速训练和降低 GPU 内存使用。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592681-e884bc1f-443f-4697-82c6-bf1f195231b1.webp)

**混合精度框架**

<font style="color:rgb(25, 27, 31);">混合精度框架使用 FP8 格式进行大多数计算密集型操作，而一些关键操作则保留其原始数据格式，以平衡训练效率和数值稳定性。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592611-fd743c2b-dd65-4a58-b9a1-ae655d9ab6c7.webp)

**量化精度提升**

<font style="color:rgb(25, 27, 31);">为了提高低精度训练的精度，DeepSeek-V3 引入了几种策略：</font>

<font style="color:rgb(25, 27, 31);">细粒度量化: 将激活和权重分组并分别进行缩放，以更好地适应异常值。</font>

<font style="color:rgb(25, 27, 31);">增加累积精度: 将部分结果复制到 FP32 寄存器中进行全精度累积，以提高精度。</font>

<font style="color:rgb(25, 27, 31);">尾数超过指数: 采用 E4M3 格式，即 4 位指数和 3 位尾数，以提高精度。</font>

**低精度存储和通信**

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 通过以下方式进一步降低内存和通信开销：</font>

<font style="color:rgb(25, 27, 31);">低精度优化器状态: 使用 BF16 格式跟踪 AdamW 优化器的第一和第二矩。</font>

<font style="color:rgb(25, 27, 31);">低精度激活: 使用 FP8 格式缓存 Linear 操作的激活，并对一些关键激活使用 E5M6 格式，或重新计算其输出。</font>

<font style="color:rgb(25, 27, 31);">低精度通信: 将激活在 MoE 上投影之前量化为 FP8，并使用调度组件，与 MoE 上投影中的 FP8 Fprop 兼容。</font>

## <font style="color:rgb(25, 27, 31);">预训练：迈向终极训练效率</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 在一个包含 14.8 万亿高质量和多样化 token 的语料库上进行预训练。预训练过程非常稳定，没有遇到不可恢复的损失峰值或需要回滚的情况。</font>

### <font style="color:rgb(25, 27, 31);">数据构建</font>
<font style="color:rgb(25, 27, 31);">预训练语料库经过优化，数学和编程样本的比例更高，并扩展了多语言覆盖范围，包括英语和中文。数据处理流程也得到了改进，以减少冗余并保持语料库的多样性。</font>

### <font style="color:rgb(25, 27, 31);">超参数设置</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 的超参数包括 Transformer 层数、隐藏维度、注意力头数、每头维度、KV 压缩维度、查询压缩维度、RoPE 维度、MoE 层数、共享专家数量、路由专家数量、中间隐藏维度、激活专家数量、节点限制路由数量、多 token 预测深度、学习率、批大小等。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592618-8d948f18-fdff-4199-9514-c7a9575b5b49.webp)

### <font style="color:rgb(25, 27, 31);">长上下文扩展</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 采用与 DeepSeek-V2 相似的方法来启用长上下文功能。在预训练阶段之后，应用 </font>[YaRN](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=YaRN&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 进行上下文扩展，并进行两个额外的训练阶段，将上下文窗口逐步扩展到 32K 和 128K。</font>

### <font style="color:rgb(25, 27, 31);">评估</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 在一系列基准测试中进行了评估，包括多学科多项选择题、语言理解和推理、闭卷问答、阅读理解、参考消歧、语言模型、中文理解和文化、数学、代码和标准化考试等。DeepSeek-V3 在大多数基准测试中都取得了最强大的性能，尤其是在数学和代码任务上。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592846-aa517d61-daaf-4eb5-895f-81e160af10d7.webp)

### <font style="color:rgb(25, 27, 31);">讨论</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 中的 MTP 策略和多 token 预测策略都取得了显著的性能提升。辅助损失免费负载平衡策略也取得了更好的性能，并且专家具有更强的专业模式。与序列级辅助损失相比，批量级负载平衡方法也表现出一致的效率优势，但其也面临着潜在的挑战，例如序列或小批量中的负载不平衡以及推理过程中域转换引起的负载不平衡。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592785-0f2a295a-fa7f-4d8e-bc5e-43a29285c52f.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592865-fc1b1025-ef7f-4293-99bd-0647d03f8d37.webp)

## <font style="color:rgb(25, 27, 31);">后训练：</font>[知识蒸馏](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=%E7%9F%A5%E8%AF%86%E8%92%B8%E9%A6%8F&zhida_source=entity)<font style="color:rgb(25, 27, 31);">与强化学习</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 通过监督微调和强化学习进行后训练，以使其与人类偏好保持一致并进一步释放其潜力。</font>

### <font style="color:rgb(25, 27, 31);">监督微调（Supervised Fine-Tuning ）</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 使用一个包含 150 万个实例的数据集进行监督微调，涵盖了多个领域。对于推理相关的数据集，例如数学、代码竞赛问题和逻辑谜题，使用内部 DeepSeek-R1 模型生成数据。对于非推理数据，例如创意写作、角色扮演和简单问答，使用 DeepSeek-V2.5 生成。并通过拒绝抽样方法筛选高质量数据，以确保最终训练数据的准确性和简洁性。</font>

<font style="color:rgb(25, 27, 31);">SFT 设置：DeepSeek-V3 使用余弦退火学习率调度进行两个 epoch 的训练，初始学习率为 5 × 10^-6，并逐渐降低到 1 × 10^-6。在训练过程中，每个序列由多个样本打包，并使用样本掩码策略确保这些示例保持隔离并相互不可见。</font>

### <font style="color:rgb(25, 27, 31);">强化学习</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 采用基于规则的奖励模型 (RM) 和基于模型的 RM 来确定模型的反馈。对于可以验证的特定规则的问题，使用基于规则的奖励系统来确定反馈。对于具有自由格式真实答案的问题，使用奖励模型来确定答案是否与预期的真实答案匹配。对于没有明确真实答案的问题，奖励模型负责根据问题和答案提供反馈。</font>

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 使用组相对策略优化 (GRPO) 进行强化学习，该优化方法放弃了与策略模型相同大小的评论模型，而是从组分数中估计基线。在 RL 过程中，模型使用高温采样生成包含来自 DeepSeek-R1 生成数据和原始数据的模式的响应，即使在缺乏明确系统提示的情况下也能做到。</font>

### <font style="color:rgb(25, 27, 31);">评估</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 在一系列基准测试中进行了评估，包括 IFEval、FRAMES、LongBench v2、GPQA、SimpleQA、C-SimpleQA、SWE-Bench Verified、Aider 1、LiveCodeBench、Codeforces、中国高中数学奥林匹克 (CNMO) 2024 和美国邀请数学考试 (AIME) 2024 等。DeepSeek-V3 在大多数基准测试中都取得了最强大的性能，尤其是在代码、数学和长上下文理解任务上。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592874-33fdeb6a-38cb-4b64-be99-1f65a666c718.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810592958-238c64ec-9159-4b17-ba90-dd6110f3b2f0.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810593107-1ec11677-ebac-4ad4-919a-233b193af8d9.webp)

## <font style="color:rgb(25, 27, 31);">讨论</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 从 DeepSeek-R1 系列模型中蒸馏推理能力取得了成功，显著提高了其在数学和代码基准测试中的性能。同时，DeepSeek-V3 还采用了宪法 AI 方法，利用 DeepSeek-V3 自身的投票评估结果作为反馈来源，进一步提高了其在主观评估中的性能。</font>

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 中的多 token 预测技术可以显著加速模型的解码速度，而额外的预测 token 的接受率在 85% 到 90% 之间，这表明其具有高度的可靠性。</font>

### <font style="color:rgb(25, 27, 31);">结论、局限性和未来方向</font>
<font style="color:rgb(25, 27, 31);">DeepSeek-V3 是一款性能强大且成本效益高的开源大型语言模型，它在推理和生成任务中都取得了显著的成果。DeepSeek-V3 的训练成本非常低，只需 2.788M H800 GPU 小时即可完成其全部训练，包括预训练、上下文长度扩展和后训练。</font>

<font style="color:rgb(25, 27, 31);">尽管 DeepSeek-V3 在性能和效率方面取得了显著成果，但它仍然存在一些局限性，尤其是在部署方面。DeepSeek-V3 的推荐部署单元相对较大，这可能对小型团队构成负担。此外，尽管 DeepSeek-V3 的部署策略已经实现了比 DeepSeek-V2 高两倍的</font>[端到端](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=%E7%AB%AF%E5%88%B0%E7%AB%AF&zhida_source=entity)<font style="color:rgb(25, 27, 31);">生成速度，但仍然存在进一步提升的空间。</font>

+ <font style="color:rgb(25, 27, 31);">DeepSeek-V3 开发了创新的负载平衡策略和训练目标，以实现高效训练。它还引入了 FP8 训练和一系列高效的工程优化措施，以进一步降低训练成本。</font>
+ <font style="color:rgb(25, 27, 31);">DeepSeek-V3 还在后训练阶段取得了成功，通过知识蒸馏和强化学习技术，显著提高了其在数学和代码基准测试中的性能。</font>
+ <font style="color:rgb(25, 27, 31);">DeepSeek-V3 在一系列基准测试中取得了最强大的性能，尤其是在数学、代码和长上下文理解任务上。</font>
+ <font style="color:rgb(25, 27, 31);">DeepSeek-V3 的局限性主要在于部署方面，包括较大的部署单元和潜在的性能提升空间。</font>
+ <font style="color:rgb(25, 27, 31);">DeepSeek-V3 采用了宪法 AI （constitutional AI） 方法，利用 DeepSeek-V3 自身的投票评估结果作为反馈来源，进一步提高了其在主观评估中的性能。</font>
+ <font style="color:rgb(25, 27, 31);">DeepSeek-V3 中的多 token 预测技术可以显著加速模型的解码速度，而额外的预测 token 的接受率在 85% 到 90% 之间，这表明其具有高度的可靠性。</font>

<font style="color:rgb(25, 27, 31);">DeepSeek 持续致力于开源模型的道路，并计划在未来进行以下方面的研究：</font>

+ <font style="color:rgb(25, 27, 31);">进一步改进模型架构，以提高训练和推理效率，并尝试突破 Transformer 架构的限制。</font>
+ <font style="color:rgb(25, 27, 31);">持续迭代训练数据的质量和数量，并探索其他训练信号来源，以推动数据扩展到更广泛的维度。</font>
+ <font style="color:rgb(25, 27, 31);">持续探索和迭代模型的深度思考能力，以增强其智能和问题解决能力，并扩展其推理长度和深度。</font>
+ <font style="color:rgb(25, 27, 31);">探索更全面和多维度的模型评估方法，以防止在研究过程中优化固定的一组基准测试，从而产生对模型能力的误导印象并影响我们的基础评估。</font>

