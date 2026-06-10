# ARPO

<!-- source: yuque://zhongxian-iiot9/hlyypb/irsic7gym49kzb57 -->

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080664570-eb47a864-eee4-46fd-ac62-9d9ca7c12b3a.png)

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">在可验证强化学习（RLVR）的推动下，</font>[<font style="color:rgb(9, 64, 142);">大语言模型</font>](https://zhida.zhihu.com/search?content_id=261519699&content_type=Article&match_order=1&q=%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在单轮推理任务中已展现出不俗表现。然而在真实推理场景中，</font>**<font style="color:#117CEE;">LLM往往需要结合外部工具进行</font>**[**<font style="color:#117CEE;">多轮交互</font>**](https://zhida.zhihu.com/search?content_id=261519699&content_type=Article&match_order=1&q=%E5%A4%9A%E8%BD%AE%E4%BA%A4%E4%BA%92&zhida_source=entity)**<font style="color:#117CEE;">，现有RL算法在平衡模型的长程推理与多轮工具交互能力方面仍存在不足</font>**<font style="color:rgb(25, 27, 31);">。 </font><font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

:::color3
**简介：****<font style="color:rgb(25, 27, 31);">Agentic Reinforced Policy Optimization（ARPO）</font>**<font style="color:rgb(25, 27, 31);">方法，专为多轮交互型LLM智能体设计。ARPO首次发现模型在调用外部工具后会推理不确定性（高熵）显著增加的现象，</font>**<font style="color:#ED740C;">并基于此引入了熵驱动的自适应rollout策略，增强对高熵工具调用步骤的探索。同时，通过引入优势归因估计</font>**<font style="color:rgb(25, 27, 31);">，模型能够更有效地理解工具交互中各步骤的价值差异。在</font>**<font style="color:rgb(25, 27, 31);">13个计算推理、知识推理和深度搜索</font>**<font style="color:rgb(25, 27, 31);">等高难基准上，ARPO在</font>**<font style="color:rgb(25, 27, 31);">仅使用一半工具调用预算</font>**<font style="color:rgb(25, 27, 31);">的情况下，仍显著优于现有样本级RL方法，为多轮推理智能体的高效训练提供了可扩展的方案。</font>

**paper : **[**Agentic Reinforced Policy Optimization**](https://arxiv.org/pdf/2507.19849)

**code : **[**ARPO**](https://github.com/RUC-NLPIR/ARPO)

**Hugging face : **[**hugging face**](https://huggingface.co/collections/dongguanting/arpo-688229ff8a6143fe5b4ad8ae)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080016799-830ce2c7-5820-4d46-9dfd-68393578c9bc.png)

<font style="color:rgb(145, 150, 161);">跨数据集分析基于 LLM 的工具使用智能体的 token 熵变化与 token 频率分布</font>



## **<font style="color:rgb(25, 27, 31);">研究动机：抓住工具调用后的高熵时刻</font>**
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近年来，可验证奖励的大规模强化学习在单轮推理任务中充分释放了前沿大语言模型的潜力，表现亮眼。然而，在开放式推理场景下，LLM不仅需要具备长程规划与自适应决策能力，还需与外部工具进行动态的多轮交互。这催生了Agentic RL这一新范式，将训练从静态求解转向动态的智能体-环境推理。</font>

<font style="color:rgb(25, 27, 31);">现有Agentic RL方法多采用样本级算法（如 GRPO、DAPO），在固定特殊token下独立采样完整的工具调用轨迹，并基于最终输出奖励模型。但这种方式常因奖励稀疏、工具过用等问题导致多轮交互价值被低估，忽视了工具调用过程中每一步的细粒度行为探索。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">通过对LLM在深度搜索任务中的token熵分布进行分析，研究发现</font>**<font style="color:rgb(25, 27, 31);">模型在每次工具调用后的初始生成阶段熵值显著升高，说明外部工具反馈会引入高不确定性</font>**<font style="color:rgb(25, 27, 31);">，而这正是现有方法未充分利用的探索契机。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Agentic Reinforced Policy Optimization（ARPO）核心思想 </font>**<font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760079824467-29dd214c-e6dc-433c-b86e-ac4eb8b8405c.png)

<font style="color:rgb(145, 150, 161);">图 1：左图展示大模型在调用工具后的高熵现象，右图对比ARPO与基线性能</font>

<font style="color:rgb(25, 27, 31);">针对上述发现，我们提出Agentic Reinforced Policy Optimization（ARPO），核心思想是在高熵工具调用步骤中，自适应地分支采样，探索更多多样化的推理路径。具体来说，我们的贡献如下：</font>

1. <font style="color:rgb(25, 27, 31);">量化了LLM在Agentic推理过程中的token熵变化，揭示了样本级RL算法在对齐LLM智能体方面的固有限制。</font>
2. <font style="color:rgb(25, 27, 31);">提出了ARPO算法，引入</font>**<font style="color:rgb(25, 27, 31);">基于熵的自适应rollout机制</font>**<font style="color:rgb(25, 27, 31);">，在保持全局采样的同时，在高熵工具调用步骤中鼓励分支采样。此外，ARPO 结合</font>**<font style="color:rgb(25, 27, 31);">优势归因估计</font>**<font style="color:rgb(25, 27, 31);">，帮助 LLM 更好地内化步骤级工具使用行为中的优势差异。</font>
3. <font style="color:rgb(25, 27, 31);">除了启发式动机，还从理论上论证了在 LLM 智能体训练中引入 ARPO 算法的合理性。</font>
4. <font style="color:rgb(25, 27, 31);">在 13 个高难基准上的实验表明，ARPO在</font>**<font style="color:rgb(25, 27, 31);">仅使用一半工具调用训练预算</font>**<font style="color:rgb(25, 27, 31);">的情况下，性能稳定优于主流RL算法，为探索Agentic RL提供了可行性参考与实践启示。</font>

## **<font style="color:rgb(25, 27, 31);">熵变现象：</font>**<font style="color:rgb(25, 27, 31);">工具调用的</font>**<font style="color:rgb(25, 27, 31);">高熵时刻与探索困境</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">通过分析大型模型在结合工具执行复杂搜索与推理任务时的token熵值，我们发现以下几点：</font>

1. <font style="color:rgb(25, 27, 31);">在每次工具调用后的前10–50个token内，熵显著上升。</font>
2. <font style="color:rgb(25, 27, 31);">在推理的初始阶段，熵往往会增加，但仍低于大模型接收到工具调用反馈后的水平。</font>
3. <font style="color:rgb(25, 27, 31);">搜索引擎的反馈引入的熵波动比代码编译器的执行反馈更大。 </font><font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080016799-830ce2c7-5820-4d46-9dfd-68393578c9bc.png)

<font style="color:rgb(145, 150, 161);">图 2：跨数据集分析基于 LLM 的工具使用智能体的 token 熵变化与 token 频率分布</font>

<font style="color:rgb(25, 27, 31);">这些现象可以归因于外部反馈与模型内部推理之间的token分布转移，这甚至导致引入的推理不确定性超过原始输入的问题。此外，搜索引擎通常提供丰富的文本内容，而代码编译器输出则由确定性的数字组成，这导致前者的熵波动更大。</font>

## **<font style="color:rgb(25, 27, 31);">工具设计：多样化工具支撑Agentic推理</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">本研究聚焦于优化基于 LLM 的工具使用智能体的训练算法。在梳理现有Agentic RL研究后，我们选取三类具有代表性的工具，用于实证评估 ARPO 的有效性： </font><font style="color:#D22D8D;">（by 草莓师姐）</font>

+ **<font style="color:rgb(25, 27, 31);">搜索引擎：</font>**<font style="color:rgb(25, 27, 31);">通过执行网络搜索查询检索相关信息，支持本地及在线模式。</font>
+ **<font style="color:rgb(25, 27, 31);">网页浏览智能体：访问</font>**<font style="color:rgb(25, 27, 31);">并解析搜索引擎返回的网页链接，提取并总结关键信息以响应查询。</font>
+ **<font style="color:rgb(25, 27, 31);">代码解释器：</font>**<font style="color:rgb(25, 27, 31);">自动执行 LLM 生成的代码，若执行成功则返回结果，否则返回编译错误信息。</font>

<font style="color:rgb(25, 27, 31);">这些工具覆盖信息检索、内容解析与程序执行等多类功能，为多轮交互与复杂推理场景提供了强有力的支撑。</font>

:::

## **<font style="color:rgb(25, 27, 31);">ARPO算法：利用熵信号指导LLM逐步优化工具调用</font>**
### **<font style="color:rgb(25, 27, 31);">基于熵的自适应rollout</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">ARPO 的核心思想在于结合全局采样与熵驱动的局部采样，在模型工具调用后不确定性升高的阶段加大探索力度，从而提升推理效果。其基于熵的自适应 rollout 机制包含四个关键步骤。 </font><font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080166875-86cf147d-f17a-4859-afe7-336252d15189.png)

<font style="color:rgb(145, 150, 161);">图 3：ARPO 的基于熵驱动的自适应 rollout 机制，结合全局探索与局部高熵节点分支</font>

:::color5
**<font style="color:#601BDE;">1. Rollout 初始化</font>**

:::

<font style="color:rgb(25, 27, 31);">设定全局 rollout 规模 ，首先进行样本级全局采样：LLM 针对输入问题  生成  条初始轨迹，并计算每条轨迹首个 token 的熵值，形成初始熵矩阵  。剩余  条轨迹的采样预算保留给局部采样。</font>

:::color5
**<font style="color:#601BDE;">2. 熵变监控</font>**

:::

<font style="color:rgb(25, 27, 31);">在每次工具调用步骤</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">后，模型会在拼接工具返回结果后继续生成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个 token，并计算步骤级熵矩阵</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">。通过量化相对于初始状态的归一化熵变化，从而判断当前推理不确定性的变化趋势。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760079415709-8bcc991d-b88d-4b77-9c59-25c16ca4ea71.png)

:::color5
**<font style="color:#601BDE;">3. 基于熵的自适应分支</font>**

:::

<font style="color:rgb(25, 27, 31);">为引导模型在熵值显著升高的节点进行更深探索，定义工具调用步骤的局部采样概率，模型的分支决策如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760079416374-cbba93db-8413-4321-95b9-c6b7d86f5272.png)

<font style="color:rgb(25, 27, 31);">该机制将探索资源自适应分配到熵上升区域，这些区域往往蕴含更高的信息增益。</font>

:::color5
**<font style="color:#601BDE;">4. 终止条件</font>**

:::

<font style="color:rgb(25, 27, 31);">Rollout 过程持续进行，直到分叉路径数达到预算上限</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">（停止分支并完成采样）或所有路径提前终止。若预算仍有剩余，则补充全局采样以覆盖更全面的推理空间。ARPO 通过上述机制在保证</font>**<font style="color:rgb(25, 27, 31);">计算复杂度维持在更低范围内：</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，同时实现了不确定性感知的高效探索，使大模型能够精准识别并充分利用工具调用后的高信息增益阶段。</font>

### **<font style="color:rgb(25, 27, 31);">优势归因估计</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">ARPO 的熵驱动自适应 rollout 会产生包含</font>**<font style="color:rgb(25, 27, 31);">共享推理片段</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">分支路径</font>**<font style="color:rgb(25, 27, 31);">的轨迹，这启发我们优化策略更新方式，更好地利用步骤级工具调用信息。 </font><font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080184945-adcacbad-0f3f-409b-824c-a875ae1a2e8b.png)

<font style="color:rgb(145, 150, 161);">两个核心组件的示意图：基于熵的自适应展开和优势归因估计。左侧：基于熵的自适应束搜索原理。右侧：ARPO在组间样本中为共享和个别的token部分分配不同的优势。</font>

:::color5
**<font style="color:#601BDE;">两种优势估计方式</font>**

:::

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">硬优势估计（Hard）</font>**

<font style="color:rgb(25, 27, 31);">明确区分共享和分支 token，对共享部分计算平均优势，对分支部分单独计算：</font>

+ <font style="color:rgb(25, 27, 31);">对分支 token 的优势估计：</font><font style="color:rgb(25, 27, 31);"> </font>
+ <font style="color:rgb(25, 27, 31);">对共享 token 的优势估计：</font><font style="color:rgb(25, 27, 31);"> </font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">软优势估计（Soft）</font>**

<font style="color:rgb(25, 27, 31);">在策略优化过程中隐式区分共享和分支推理链的token，通过 GRPO（Group Relative Policy Optimization）在分组更新中动态调整重要性采样比率</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">, 自然地处理了两类token：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760079416925-c78c2be0-225f-4367-8030-3a2a9c6b3306.png)

<font style="color:rgb(25, 27, 31);">其中重要性采样比率：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760079416946-6f936a1e-b701-4665-9266-153b4c7cf36c.png)

<font style="color:rgb(25, 27, 31);">当两个轨迹在 t 步之前共享相同token前缀时，它们的共享token具有相同的重要性权重，因此这一更新过程近似等价于硬优势估计，并且更优雅。实验结果证明软优势估计在ARPO训练中能稳定获得更高奖励，故将其设为默认优势估计方法。</font>

### **<font style="color:rgb(25, 27, 31);">分层奖励设计</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">ARPO的奖励函数综合考虑</font>**<font style="color:rgb(25, 27, 31);">答案正确性、工具调用格式及多工具协作</font>**<font style="color:rgb(25, 27, 31);">。 如果模型在推理中使用了搜索（<search>）和代码（<python>）等多种工具，并保证答案正确且格式合规，会获得额外奖励，公式如下：</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080225082-7018f86b-1a93-4cbf-b563-c978fce1c70b.png)

<font style="color:rgb(25, 27, 31);">通过软优势估计与分层奖励机制，ARPO 在训练中能更平稳、更高效地优化多轮工具使用策略。</font>

## **<font style="color:rgb(25, 27, 31);">实验结果：10+综合推理任务评测</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了充分评估ARPO的泛化性和高效性，我们考虑以下三种测试集：</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">计算型推理任务：</font>**<font style="color:rgb(25, 27, 31);">评估模型的计算推理能力，包括AIME24，AIME25，MATH500，GSM8K，MATH。</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">知识密集型推理任务：</font>**<font style="color:rgb(25, 27, 31);">评估模型结合外部知识推理的能力，包括WebWalker，HotpotQA，2WIKI，MisiQue，Bamboogle。</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">深度搜索任务：</font>**<font style="color:rgb(25, 27, 31);">评估模型的深度搜索能力，包括HLE，GAIA，SimpleQA，XBench。</font>

:::

**reasoning tasks**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080254861-120e1900-cf8d-4067-85c0-530fc585b2ab.png)

** deep search tasks**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080269629-a449b366-3ff1-4fe8-90a9-9bb9bce42a32.png)

<font style="color:rgb(25, 27, 31);">从实验结果可以发现：</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">ARPO整体表现优于主流方法：</font>**<font style="color:rgb(25, 27, 31);">ARPO在大部分任务上准确率高于GRPO、DAPO等样本级RL方法，在工具调用密集任务（如 GAIA、HLE）中提升幅度更明显。</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">多任务保持稳定性能</font>**<font style="color:rgb(25, 27, 31);">：ARPO在计算、知识与搜索任务中均保持较好的表现，没有明显性能短板，验证其跨任务的适配能力。</font>

## **<font style="color:rgb(25, 27, 31);">实验：采样分析与工具调用效率评估</font>**
### **<font style="color:rgb(25, 27, 31);">多轮采样能力提升模型表现</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">由于Deepsearch任务具有动态、多轮交互的特点，单纯使用Pass@1指标难以全面反映模型的工具调用潜力。我们进一步分析了Pass@3和Pass@5指标，发现无论是8B还是14B规模模型，在经过ARPO对齐训练后，均表现出持续提升和良好的规模效应。其中，14B模型在Pass@5指标上表现尤为出色：</font><font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080340612-ccc68665-e04f-4ad3-9b6d-554ae269ce59.png)

<font style="color:rgb(145, 150, 161);">使用ARPO对Qwen3-8B和Qwen3-14B在Pass@1到Pass@5指标上的分析。</font>

<font style="color:rgb(25, 27, 31);">• GAIA 达到</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">61.2%</font>**

<font style="color:rgb(25, 27, 31);">• HLE 达到</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">24.0%</font>**

<font style="color:rgb(25, 27, 31);">• XBench-DR 达到</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">59%</font>**

### **<font style="color:rgb(25, 27, 31);">工具调用效率显著提升</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在Agentic RL训练中，工具调用次数直接影响成本。我们以Qwen2.5-7B模型为例，将ARPO与GRPO方法进行对比：</font>

<font style="color:rgb(25, 27, 31);">• ARPO 在整体准确率上优于 GRPO</font>

<font style="color:rgb(25, 27, 31);">• 同时</font>**<font style="color:rgb(25, 27, 31);">仅使用了约GRPO一半的工具调用次数</font>**<font style="color:#D22D8D;">（by 草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760080354288-0f667ebf-614e-4573-96c3-4f2b565233d5.png)

<font style="color:rgb(145, 150, 161);">Qwen2.5-7B的工具调用效率比较：GRPO与ARPO。</font>

<font style="color:rgb(25, 27, 31);">这得益于 ARPO 独特的基于熵的自适应采样机制，仅在高熵工具调用步骤进行分支采样，极大地扩展了工具行为的探索空间，同时降低了不必要的调用。</font>**<font style="color:rgb(25, 27, 31);">更多的实验结果可以在我们的论文中看到</font>**

## **<font style="color:rgb(25, 27, 31);">总结与未来展望</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">ARPO算法有效提升了多轮工具推理代理的性能，解决了现有样本级RL方法在多轮交互中探索不足、泛化能力欠缺的问题。通过熵驱动自适应采样和优势归因机制，ARPO 能够在工具调用频繁、推理路径复杂的任务中实现更高效、更稳定的输出。未来，为持续提升Agentic RL模型的能力，仍有多个方向值得探索：</font>

:::

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">多模态Agentic RL：</font>**<font style="color:rgb(25, 27, 31);">ARPO目前主要针对文本推理任务，在处理图像、视频等多模态信息方面仍有局限。未来可扩展至多模态任务中，探索模型在多模态场景下的工具调用与策略优化。</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">工具生态扩展：</font>**<font style="color:rgb(25, 27, 31);">ARPO 已经验证了在多工具协作任务上的潜能。未来可引入更多类型的外部工具（如代码调试器、数据分析工具、实时 API 调用等），并通过工具使用策略优化进一步提升复杂任务表现。</font>

**<font style="color:rgb(25, 27, 31);">•</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">大规模与实时部署：</font>**<font style="color:rgb(25, 27, 31);">ARPO 展示了较高的训练效率和推理泛化性，未来可探索在更大规模模型和实时动态环境中的部署与适配，降低成本同时提升实用价值。</font>

