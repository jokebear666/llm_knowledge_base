# Reward Model 综述

<!-- source: yuque://zhongxian-iiot9/hlyypb/au861ldbainaq97y -->

# 背景<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(41, 41, 41);">奖励模型（RM）表现出了增强大型语言模型（LLM）的令人印象深刻的潜力，因为RM可以作为人类偏好的代理，提供信号来指导LLMS在各种任务中的行为。 </font>

:::

:::color3
**简介：**<font style="color:rgb(41, 41, 41);">在本文中，我们对相关研究进行了全面的概述，从</font>**<font style="color:#ED740C;">偏好收集、奖励建模和使用方法</font>**<font style="color:rgb(41, 41, 41);">等角度探讨了奖励模型。 接下来，我们将介绍奖励模型的应用，并讨论评估的基准。 此外，我们还对该领域存在的挑战进行了深入分析，并探讨了潜在的研究方向。 </font>

+ RM可以从人类和AI系统收集偏好，并采用提高偏好收集效率和质量的方法
+ RM可以根据基础模型架构分为判别式、生成式和隐式类型
+ RM可用于强化学习框架中的数据选择、策略训练和推理
+ 主要挑战包括提高RM的可扩展性和鲁棒性，以及解决奖励操纵和分布偏移等问题
+ 潜在的研究方向包括融入多模态偏好、开发更具可解释性和可控性的RM，以及探索RM在语言模型之外的其他领域的应用<font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/JLZhong23/awesome-reward-models](https://github.com/JLZhong23/awesome-reward-models)

**paper：**[**A Comprehensive Survey of Reward Models: Taxonomy,Applications, Challenges, and Future**](https://arxiv.org/pdf/2504.12328)

**参考：**[**https://mp.weixin.qq.com/s/OdJ28jX9BAuQY2EFF9b7Fw**](https://mp.weixin.qq.com/s/OdJ28jX9BAuQY2EFF9b7Fw)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745808662707-1694140a-bb9c-4764-befc-d7a044655114.png)

<font style="color:rgb(41, 41, 41);">图 1： RM的一个示例。</font>

<font style="color:rgb(41, 41, 41);">图</font>[<font style="color:rgb(33, 33, 33);">1</font>](https://arxiv.org/html/2504.12328v1#S1.F1)<font style="color:rgb(41, 41, 41);">展示了对话领域中RM的一个示例。 目标是训练一个基于LLM的聊天机器人，遵循“3H”原则（</font>**<font style="color:rgb(41, 41, 41);">H</font>**<font style="color:rgb(41, 41, 41);">onest，</font>**<font style="color:rgb(41, 41, 41);">H</font>**<font style="color:rgb(41, 41, 41);">armless，和</font>**<font style="color:rgb(41, 41, 41);">H</font>**<font style="color:rgb(41, 41, 41);">elpful）。 给定两个由LLM生成的样本响应，</font>**<font style="color:#74B602;">RM遵循指令并根据上述三个维度对响应进行排序，然后选择与人类价值观（在本例中是较少危害性）更一致的LLM-2生成的更好响应</font>**<font style="color:rgb(41, 41, 41);">，随后可用于优化策略模型。 RM的排序过程展示了可解释性和可追溯性。 任务指令、人工输入、响应对和RM偏好可用于在强化学习阶段优化策略LLM。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">在本文中，我们主要关注LLM时代</font>_<font style="color:rgb(41, 41, 41);">参数化的</font>_<font style="color:rgb(41, 41, 41);">RM，它们用于反映人类偏好。 一些调查涉及到RM的介绍。 然而，这些工作缺乏对RM的系统性组织，或者没有包含对RM的详细和建设性的讨论。 为填补这一空白，我们的主要贡献可以概括为：</font>

+ <font style="color:rgb(41, 41, 41);">我们提出了第一个专门针对LLM时代RM的全面综述；</font>
+ <font style="color:rgb(41, 41, 41);">我们系统地回顾了RM领域的相关工作，并介绍了一个</font>**<font style="color:#74B602;">详尽的分类法</font>**<font style="color:rgb(41, 41, 41);">；</font>
+ <font style="color:rgb(41, 41, 41);">我们讨论了挑战和未来的方向，这有助于进一步的研究。</font>



# Reward Model 分类
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745809059331-897c06bc-e14c-4f66-a4d3-4d5b1fcb9e20.png)

<font style="color:rgb(41, 41, 41);">图 2： 奖励模型分类法，包括偏好收集、奖励建模和用法。 </font>

## 偏好收集<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(41, 41, 41);">简介：</font>**<font style="color:rgb(41, 41, 41);">奖励模型可以充当人类的代理，其中偏好可以源于不同的来源，包括人类和大型语言模型。 本节将介绍详细内容。</font>

:::

:::color5
**<font style="color:#601BDE;">1.人类偏好</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">仅仅增加模型参数或训练数据并不能保证与人类偏好更好地对齐。 相反，更大的模型仍然可能产生幻觉、有害输出或无用的响应。 一种直接的方法是在人类偏好数据上训练奖励模型，随后作为代理在强化学习阶段提供训练信号。 一些方法采用人工标注者来标记策略模型与环境交互产生的轨迹对。 其他工作利用标注者为大型语言模型或人类根据收集的提示生成的响应对分配标签。 在此基础上，提高收集效率和质量需要进一步研究。</font>

+ **<font style="color:rgb(41, 41, 41);">效率</font>**

<font style="color:rgb(41, 41, 41);">一些研究已经将主动学习引入偏好收集。 例如，Biyik et al. (2020)和Lindner et al. (2021)使用信息增益的目标来选择查询。 Lee et al. (2021)采用基于熵的采样方法来选择片段对。 此外，一些方法(Park et al., 2022; Hwang et al., 2023)利用数据增强和顺序成对比较来实现偏好高效学习。</font>

+ **<font style="color:rgb(41, 41, 41);">质量</font>**

<font style="color:rgb(41, 41, 41);">一些工作旨在从标注者的角度提高质量，包括引入演示(Ibarz et al., 2018)、主动标注者选择(Barnett et al., 2023)、用户友好的界面(Metz et al., 2023; Yuan et al., 2024e)以及细粒度的目标和规则(Glaese et al., 2022b; Wu et al., 2023a; Wang et al., 2024h)。 同时，其他工作关注采样查询的质量，例如选择多样化的批量样本(Biyik & Sadigh, 2018; Biyik et al., 2024)或采用在线收集设置(Dong et al., 2024)以防止分布偏移。</font>

:::color5
**<font style="color:#601BDE;">2.AI偏好</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">尽管从训练有素的人类标注者那里收集偏好数据直观上适用于人类偏好对齐，但高昂的成本</font><font style="color:rgb(41, 41, 41);">(Gilardi et al., 2023)</font><font style="color:rgb(41, 41, 41);">可能会限制其实用性。</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">随着大语言模型 (LLM) 能力的不断提升</font><font style="color:rgb(41, 41, 41);">(Li et al., 2024b)</font><font style="color:rgb(41, 41, 41);">，它们已经展现出与人类判断高度一致性</font><font style="color:rgb(41, 41, 41);">(Lee et al., 2024a)</font><font style="color:rgb(41, 41, 41);">。</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">此外，当AI系统在某些任务上超越人类</font><font style="color:rgb(41, 41, 41);">(Silver et al., 2017; Vinyals et al., 2019)</font><font style="color:rgb(41, 41, 41);">时，人类很难评估超人类模型产生的复杂行为</font><font style="color:rgb(41, 41, 41);">(Burns et al., 2024a)</font><font style="color:rgb(41, 41, 41);">。</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">因此，AI偏好获得了越来越多的研究兴趣，并有可能成为人类偏好的替代方案</font><font style="color:rgb(41, 41, 41);">(Dubois et al., 2023)</font><font style="color:rgb(41, 41, 41);">。</font>

<font style="color:rgb(41, 41, 41);">Bai et al. (2022b)</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">首次介绍了来自AI反馈的强化学习 (RLAIF)，用于在对话场景中训练一个有帮助且无害的AI助手，其中奖励模型 (RM) 在LLM生成的无害性偏好标签和人工生成的帮助性偏好标签的组合上进行训练。</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">Kim et al. (2023)</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">在合成比较上训练奖励模型 (RM)，其质量由模型大小和上下文样本数量决定。</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">Lee et al. (2024a)</font><font style="color:rgb(41, 41, 41);"> </font><font style="color:rgb(41, 41, 41);">直接利用现成的LLM在强化学习过程中提供奖励，这可以解决初始策略采样轨迹与RM训练数据集之间的分布不一致问题。</font>

<font style="color:rgb(41, 41, 41);">与人类偏好收集类似，一些后续研究试图收集规模化和高质量的AI偏好对。 Cui et al. (2024) 和Li (2025)构建指令模板来引发偏好。 模型池中的各种LLM用于生成和评估指令的完成情况。 Sun et al. (2024b) 引入人为定义的原则来实现可指导的奖励模型 (RM)。 其他工作进一步将AI偏好与人类偏好相结合。 Ye et al. (2024a) 和Yu et al. (2024a) 使LLM能够为完成对生成合成评论以增强奖励模型 (RM)。 此外，Duan et al. (2024) 结合LLM生成的响应和人工标注的负样本以减轻噪声正样本的问题(Wang et al., 2024a)。</font>



## RM 奖励模型<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(41, 41, 41);">简介：</font>**<font style="color:rgb(41, 41, 41);">奖励建模在大型语言模型的对齐中扮演着核心角色，尤其是在强化学习框架中作为基础组成部分。 在强化学习研究中，奖励模型已被广泛采用，以替代直接使用环境奖励。 它们与逆强化学习尤其相关，逆强化学习专注于从观察到的轨迹数据中推断代理的潜在奖励函数。</font>

:::

:::color5
**<font style="color:#601BDE;">1.奖励模型类型级别 （type level）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">在这一部分中，我们主要根据底层模型类型讨论几种奖励模型的奖励建模机制（图</font>[<font style="color:rgb(33, 33, 33);">3</font>](https://arxiv.org/html/2504.12328v1#S2.F3)<font style="color:rgb(41, 41, 41);">），这些机制包括</font>**<font style="color:#74B602;">判别式奖励、生成式奖励和隐式奖励</font>**<font style="color:rgb(41, 41, 41);">。</font>

1. **<font style="color:rgb(41, 41, 41);">判别式奖励</font>**

<font style="color:rgb(41, 41, 41);">判别式奖励模型包括一个基础模型和一个</font>**<font style="color:#74B602;">基于多层感知器 (MLP) 的奖励头（分类器），它为给定的输入输出一个标量奖励</font>**<font style="color:rgb(41, 41, 41);">。 序列分类器（图</font>[<font style="color:rgb(33, 33, 33);">3</font>](https://arxiv.org/html/2504.12328v1#S2.F3)<font style="color:rgb(41, 41, 41);">(a)）属于判别式奖励模型，它对单个响应的偏好进行建模。 </font>

+ <font style="color:rgb(41, 41, 41);">Cai 等人 (2024) 提出了一种条件奖励模型，通过利用条件系统提示，将不同领域的偏好数据整合在一起。 </font>
+ <font style="color:rgb(41, 41, 41);">Yuan等人 (2024b) 引入用于增强Bradley-Terry (BT) 模型(Bradley & Terry, 1952) 的动作绝对奖励，该模型非常适用于二元比较任务。</font>
+ <font style="color:rgb(41, 41, 41);"> Yang等人 (2024c) 对隐藏状态进行正则化，以提高RM在非分布数据(OOD)上的泛化能力。</font>

<font style="color:rgb(41, 41, 41);">另一种判别式RM是</font>**<font style="color:#74B602;">自定义分类器（图</font>**[**<font style="color:#74B602;">3</font>**](https://arxiv.org/html/2504.12328v1#S2.F3)**<font style="color:#74B602;">(b)），它将比较对作为输入或输出多个分数</font>**<font style="color:rgb(41, 41, 41);">。 Jiang等人 (2023) 比较池中每一对候选者，并定义几个评分函数来选择最佳候选者。 Winata等人 (2024) 优化现有指标的集成，以与人类偏好保持一致。 Adler等人 (2024) 和Wang等人 (2024b) 利用多目标奖励来建模不同的偏好。 此外，Wang等人 (2024b) 进一步使用门控层自适应地为任务分配合适的目标。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745809730197-f0247476-9466-4309-821f-ad3fae13b073.png)

<font style="color:rgb(41, 41, 41);">图3:  奖励模型可以分为判别式RM (a)(b)、生成式RM (c)和隐式RM (d)。 (x : 提示， y1,y2 : 响应)</font>

2. **<font style="color:rgb(41, 41, 41);">生成式奖励</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(41, 41, 41);">与判别式模型不同，生成式奖励模型（图</font>[<font style="color:rgb(33, 33, 33);">3</font>](https://arxiv.org/html/2504.12328v1#S2.F3)<font style="color:rgb(41, 41, 41);">(c)）</font>**<font style="color:#74B602;">充分利用LLM的生成能力来提供偏好分数</font>**<font style="color:rgb(41, 41, 41);">。 </font>

+ <font style="color:rgb(41, 41, 41);">有些工作使用通用模型(Zheng等人，2023)或训练专用模型(Li等人，2024c; Cao等人，2024a; Ye等人，2024b; McAleese等人，2024; Gao等人，2024)作为评判者，这些模型可以</font>**<font style="color:#74B602;">生成更好的比较对选项或对文本格式的单个响应进行评分。 </font>**
+ <font style="color:rgb(41, 41, 41);">Mahan等人 (2024) 和Zhang等人 (2024c) 将答案指示符的下一个符元概率提取为分数。 </font>
+ <font style="color:rgb(41, 41, 41);">Chen等人（2024e） 利用训练好的生成式奖励模型在最小编辑约束下改写原始响应。 通过对比响应对可以获得符元级别的分数。</font>
+ <font style="color:rgb(41, 41, 41);"> 一些工作(Yuan等人，2024d; Tsvilodub等人，2024; Wu等人，2024b) 使用</font>**<font style="color:#74B602;">构建的对比合成偏好对、推理轨迹（可选）和生成的判断迭代地训练模型。</font>**
+ <font style="color:rgb(41, 41, 41);"> </font>**<font style="color:#74B602;">生成式奖励模型可以与其他与大语言模型相关的技术集成，例如思维链 (CoT)</font>**<font style="color:rgb(41, 41, 41);">(Kojima等人，2022)和检索增强生成 (RAG)(Lewis等人，2020)，从而使其能够应用于更广泛的任务。</font>
3. **<font style="color:rgb(41, 41, 41);">隐式奖励</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(41, 41, 41);">与显式RMS不同，最近的研究通过</font>**<font style="color:#74B602;">较弱的优化信号构建了与奖励相关的变量（变量 z 图</font>**[**<font style="color:#74B602;">3</font>**](https://arxiv.org/html/2504.12328v1#S2.F3)**<font style="color:#74B602;">(d)所示）以降低资源成本</font>**<font style="color:rgb(41, 41, 41);">。 </font>

+ <font style="color:rgb(41, 41, 41);">DPO(Rafailov等人，2023)和SLiC-HF(Zhao等人，2023)通过</font>**<font style="color:#74B602;">定义基于生成概率的隐式奖励，直接优化人类偏好对，从而避免了显式奖励建模。 </font>**
+ <font style="color:rgb(41, 41, 41);">Rafailov等人 (2024) 从分析上证明了这些隐式奖励的价值函数是其显式对应物的延续，从而能够在大语言模型中实现自动化的信用分配。 随后的一些研究旨在提高模型的鲁棒性。</font>
+ <font style="color:rgb(41, 41, 41);"> 一些工作(Liu等人，2024e; Chen等人，2024a) 试图从多个响应中有效地优化目标策略，而Richemond等人 (2024a) 则提出对单轨迹数据进行直接奖励优化。 </font>
+ <font style="color:rgb(41, 41, 41);"> 从建模机制的角度来看，最近的技术，如符元级优化(Zeng等人，2024; Lin等人，2024)、无参考方法(Hong等人，2024; Xu等人，2024; Meng等人，2024)、自博弈优化(Rosset等人，2024; Swamy等人，2024; Wu等人，2025b)都展现了实际的潜力。 </font>
+ <font style="color:rgb(41, 41, 41);">然而，需要注意的是，与显式优化结果相比，这些方法在奖励建模本身方面通常表现不佳(Lambert等人，2024)。</font>

:::color5
**<font style="color:#601BDE;">2.奖励粒度级别（</font>****<font style="color:#601BDE;">Granularity Level</font>****<font style="color:#601BDE;">）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">在本节中，我们将根据奖励机制在充当验证器解决具有真实结果的问题时的粒度对其进行分类。 具体来说，</font>**<font style="color:#74B602;">结果级别奖励模型 (Outcome-level Reward Model, ORM) 预测完成结果为正确答案的概率，而过程级别奖励模型 (Process-level Reward Model, PRM) 为推理过程中的每个步骤分配一个分数。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745810578824-ec82b331-0476-4b20-a2e9-2ff0c61b5c61.png)

<font style="color:rgb(41, 41, 41);">表1： 不同粒度RM的优势和劣势比较</font>

1. **<font style="color:rgb(0, 0, 0);">结果级别奖励</font>**

<font style="color:rgb(41, 41, 41);">对于需要更复杂推理的任务，可以使用 ORM。 通常，ORM 的训练数据与标准偏好调优的构建方式不同。 具体来说，每个解决方案 s 都与问题陈述或提示配对 p. 在这种设置中应用的归纳偏置假设一次完成代表了一个基于给定问题是否正确的解决方案。 ORM (P×S→ℝ) 通常</font>**<font style="color:#74B602;">使用交叉熵损失进行训练</font>**<font style="color:rgb(41, 41, 41);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745810349111-9ab05a73-f0d1-463f-ad06-32980de246b0.png)

2. **<font style="color:rgb(41, 41, 41);">过程级别奖励</font>**

<font style="color:rgb(41, 41, 41);">尽管在多步骤推理任务中表现出色，</font>**<font style="color:#74B602;">但结果监督方法仍然容易出现幻觉，例如通过错误的推理路径得出正确答案。 这表明需要结合过程监督来解决这些限制</font>**<font style="color:rgb(41, 41, 41);">。 此外，PRM (P×S→ℝ+) 可以使用下面的标准分类损失函数进行训练，其中 yi 是PRM的预测分数， yi^ 代表正确性标签， N是s的总推理步骤数。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745810359293-256555ee-9fab-44cf-9b63-376d574bb249.png)





## <font style="color:rgb(41, 41, 41);">使用方法</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(41, 41, 41);">简介：</font>**<font style="color:rgb(41, 41, 41);">在LLM的背景下，RM充当关键组件，有助于引导模型行为朝向期望的结果。 通过定义一个结构化、可量化的信号来衡量生成的响应与特定目标或用户偏好的一致程度，RM能够实现LLM输出的调整和优化。 此RM效用体现在LLM生命周期的多个阶段，包括</font>**<font style="color:#ED740C;">数据选择、策略训练和推理阶段</font>**<font style="color:rgb(41, 41, 41);">。 在本小节中，我们将从这三个角度详细研究RM效用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.数据选择</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">一些研究利用RM来选择用于LLM微调的数据。 </font>

+ <font style="color:rgb(41, 41, 41);">Dong等人 (2023) 提出了一种类似于SFT的迭代训练方法，</font>**<font style="color:#74B602;">其中利用奖励模型(RM)对大语言模型(LLM)生成的响应质量进行排序。 奖励最高的数据可用于微调LLM</font>**<font style="color:rgb(41, 41, 41);">。 </font>
+ <font style="color:rgb(41, 41, 41);">Yuan等人 (2023) 进一步引入了</font>**<font style="color:#74B602;">排序损失，以使LLM生成的评分与RM生成的评分一致</font>**<font style="color:rgb(41, 41, 41);">。 </font>
+ <font style="color:rgb(41, 41, 41);">Gülçehre等人 (2023) 利用RM过滤后的数据集，根据离线强化学习目标微调LLM。 </font>
+ <font style="color:rgb(41, 41, 41);">Pang等人 (2024) 通过奖励模型评估答案和推理的正确性，从而选择偏好对，并通过DPO (Rafailov等人，2023) 目标优化LLM。</font>

:::color5
**<font style="color:#601BDE;">2.策略训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">奖励模型提供反馈信号，强化或惩罚某些行为，最终塑造模型的决策策略。 为了减轻鲁棒性低的问题（主要是因为奖励模型在分布外泛化(Pikus等人，2023)和人类判断不匹配方面常常难以应对），已经研究了几种策略。 这些策略包括长度控制奖励设置(Chen等人，2024c; Zhou等人，2024b; Park等人，2024b)，因果奖励建模(Wang等人，2025a; Liu等人，2025b)，贝叶斯方法(Yang等人，2024a; Li等人，2024a; Yan等人，2024)和集成方法(Wu等人，2023b; Ramé等人，2024; Zhang等人，2024d)。</font>

:::color5
**<font style="color:#601BDE;">3.推理</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">奖励模型可以用来对多个输出进行排序，从而提供最符合特定应用标准的响应。 正如§</font>[<font style="color:rgb(33, 33, 33);">2.2.2</font>](https://arxiv.org/html/2504.12328v1#S2.SS2.SSS2)<font style="color:rgb(41, 41, 41);">中所讨论的，奖励模型可以分为在线奖励模型(ORM)和预训练奖励模型(PRM)。 预训练奖励模型通常在推理阶段用于评估进度和提高推理能力(Setlur等人，2024a)。 一些奖励模型引导的树搜索框架(Ma等人，2023; Jiang等人，2024; He等人，2024; Zhang等人，2024b)已被证明能够大大增强LLM的推理能力。 此外，奖励模型还可以用于评估中间解码步骤，并动态决定是否调用更强大的目标模型，以平衡资源利用率和性能(Liao等人，2025)。</font>

<font style="color:rgb(41, 41, 41);"></font>

# 应用<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(41, 41, 41);">简介：</font>**<font style="color:rgb(41, 41, 41);">强化模型（RMs）已在多个领域得到广泛应用。 在此，我们简要总结了目前强化模型应用的一些关键领域。</font>

:::

:::color5
**<font style="color:#601BDE;">1.对话</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">强化模型通过基于道德准则和用户意图</font>**<font style="color:#74B602;">改进有害的回应来帮助减轻其负面影响</font>**<font style="color:rgb(41, 41, 41);">。 同时，一些工作侧重于对话中的专业性，要求智能体能够准确清晰地表达复杂的知识。 其他工作则试图改善整体对话印象，包括</font>**<font style="color:#74B602;">同理心、热情、拟人化</font>**<font style="color:rgb(41, 41, 41);">等等。</font>

:::color5
**<font style="color:#601BDE;">2.推理</font>**

:::

<font style="color:rgb(41, 41, 41);">在</font>**<font style="color:#74B602;">数学推理</font>**<font style="color:rgb(41, 41, 41);">方面，强化模型，特别是概率强化模型（PRM），可以通过平衡各种解决方案的探索和最小化错误来为大语言模型（LLM）提供指导，从而提高逻辑一致性。此外，强化模型还在</font>**<font style="color:#74B602;">代码生成</font>**<font style="color:rgb(41, 41, 41);">方面展现出潜力，通过集成API调用、提高学习效率和优化性能。</font>

:::color5
**<font style="color:#601BDE;">3.检索与推荐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">强化模型可以用来帮助将检索过程与强大LLM的偏好对齐，这包括</font>**<font style="color:#74B602;">评估相关性、自适应检索以及改进中间查询的质量</font>**<font style="color:rgb(41, 41, 41);">。 至于推荐系统，强化模型可以用来捕捉</font>**<font style="color:#74B602;">细微的用户偏好，评估LLM生成的用户偏好，并得出高质量的解释。</font>**

:::color5
**<font style="color:#601BDE;">4.其他应用</font>**

:::

<font style="color:rgb(41, 41, 41);">除了上述在文本领域的应用外，强化模型还在其他模式中展现出潜力，例如</font>**<font style="color:#74B602;">文本转音频、文本转图像、文本转视频</font>**<font style="color:rgb(41, 41, 41);">。 此外，强化模型还被应用于一些交互式任务，包括机器人操作和游戏，这些都成为人工通用智能的基础。</font>

<font style="color:rgb(41, 41, 41);"></font>

# benchmark<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
<font style="color:rgb(41, 41, 41);">简介：强化模型的评估至关重要，因为强化模型中的错误会对最终策略的性能产生负面影响。 然而，用于奖励模型（RM）评估的通用和标准化基准的开发仍然处于起步阶段，这使得比较和改进奖励模型变得困难。 这是由于以下几个挑战：</font>

+ <font style="color:rgb(41, 41, 41);">评估奖励模型最直接的方法是训练一个完整的强化学习策略并观察其性能，这非常昂贵。</font>
+ <font style="color:rgb(41, 41, 41);">奖励模型的评估通常与用它训练的策略的性能联系在一起，这使得很难独立地评估奖励模型</font>
+ <font style="color:rgb(41, 41, 41);">虽然创建用于评估的数据集（例如，标注一个简单的成对比较数据集）相对容易，但</font>**<font style="color:#117CEE;">奖励模型对输入风格、领域或格式的变化很敏感</font>**<font style="color:rgb(41, 41, 41);">。 这意味着奖励模型评估需要一种更全面的方法，需要考虑构建更动态、多方面的测试，这进一步增加了难度。 </font>

<font style="color:rgb(41, 41, 41);">最近，研究人员试图构建高质量的基准，以探索在不同的强化学习策略、语言模型架构、训练预算等方面优化奖励模型。</font>

:::

:::color5
**<font style="color:#601BDE;">1.客观奖励模型Benchmark</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(41, 41, 41);">Lambert et al. (2024)构建了一个全面的基准RewardBench，其中包含经过人工验证的</font>**<font style="color:#74B602;">提示-选择-拒绝三元组，涵盖聊天、推理、安全性和之前的测试集</font>**<font style="color:rgb(41, 41, 41);">，同时提供了一个审计奖励模型行为的工具包。 </font>
+ <font style="color:rgb(41, 41, 41);">Liu et al. (2024g)提出了RM-Bench，其中包括聊天、代码、数学和安全标注数据，并在公开可访问的奖励模型上进行了大规模评估。 </font>
+ <font style="color:rgb(41, 41, 41);">Zhou et al. (2024a)引入了RMB，其中包含超过49个现实场景，并讨论了先前基准中的泛化缺陷。 </font>
+ <font style="color:rgb(41, 41, 41);">Frick et al. (2024)提出了PPE，通过启动端到端的强化学习与人类反馈实验来评估奖励模型在代理任务（与下游强化学习与人类反馈结果相关）上的表现。</font>

:::color5
**<font style="color:#601BDE;">2.过程奖励模型Benchmark</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(41, 41, 41);">随着推理研究的兴起，大型语言模型被应用于更复杂的场景，例如</font>**<font style="color:#74B602;">数学和多跳决策任务</font>**<font style="color:rgb(41, 41, 41);">，因此出现了过程奖励模型并被应用。 </font>

+ <font style="color:rgb(41, 41, 41);">为了评估过程奖励模型，Zheng et al. (2024)提出了ProcessBench，其中包含大量带有</font>**<font style="color:#74B602;">逐步标注解决方案的竞赛数学问题的案例</font>**<font style="color:rgb(41, 41, 41);">。 </font>
+ <font style="color:rgb(41, 41, 41);">Song et al. (2025)介绍了PRMBench，它包含数千个带有</font>**<font style="color:#74B602;">逐步标签的设计问题，跨多个维度评估奖励模型。</font>**

<font style="color:rgb(41, 41, 41);">除了上述研究之外，一些最近的工作评估了特定领域或应用的奖励模型，例如</font>**<font style="color:#74B602;">视觉语言、多语言设置和检索增强生成</font>**<font style="color:rgb(41, 41, 41);">。 这些基准测试共同减轻了对奖励模型 (RMs) 进行更全面、更细粒度评估的需求，为训练更强大的大型语言模型 (LLMs) 的更可靠、更强大的奖励模型铺平了道路。</font>

<font style="color:rgb(41, 41, 41);"></font>

# 未来方向<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
##### <font style="color:#601BDE;">1.标量奖励与基于规则的奖励相结合正成为一种日益增长的趋势。</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(41, 41, 41);">在先进的工业大语言模型中，强大的模型可以受益于</font>**<font style="color:#74B602;">整合基于规则的奖励和基于模型的奖励</font>**<font style="color:rgb(41, 41, 41);">。 基于规则的奖励提供清晰的指导，而基于模型的奖励则能够从预测中学习。 具体而言，基于规则的奖励应用于</font>**<font style="color:#74B602;">具有明确真实值的任务（例如，数学、编码）</font>**<font style="color:rgb(41, 41, 41);">，而奖励模型则用于没有明确真实值的任务（例如，创造性任务），从而增强了大语言模型的实际应用能力。 将基于规则的奖励融入o1型长链思考模型的强化微调已成为标准做法，学术界也出现了一些仅使用基于规则奖励的研究，也取得了强大的推理能力。</font>

:::color5
##### <font style="color:#601BDE;">2.大语言模型长水平代理任务中的奖励设计</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(41, 41, 41);">推理能力的最新进展使复杂的大语言模型能够</font>**<font style="color:#74B602;">处理复杂的专家级任务</font>**<font style="color:rgb(41, 41, 41);">，其中规划发挥着关键作用。 OpenAI和Anthropic正在探索工具的使用，例如搜索引擎、代码解释器(Cursor，2025)和网络浏览器，以完成复杂的图形用户界面任务。 然而，确保良好的代理性能具有挑战性，尤其是在为大型系统设计反馈机制时。 创建规则具有实验性，为长水平任务开发端到端的强化学习框架至关重要。 主要挑战仍然是确保代理持续获得奖励并单调改进。</font>

:::color5
##### <font style="color:#601BDE;">3.增强多模态领域</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(41, 41, 41);">奖励模型在多模态领域发展迅速，其中包括图像、音频和视频等模态的集成。 与单模态相比，</font>**<font style="color:#117CEE;">多模态偏好数据的收集成本更高</font>**<font style="color:rgb(41, 41, 41);">。 少样本学习、数据合成等一些技术仍有待探索，从而减少对人工标注员的依赖。 同时，设计高质量的奖励信号至关重要，这涉及到不同模态之间的对齐。 最后，探索增强奖励模型跨域泛化能力的方法，以及弥合模拟场景和真实场景之间差距的方法，将有助于实现具身智能。</font>

