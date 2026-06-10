# SFT之后，为什么需要RL?

<!-- source: yuque://zhongxian-iiot9/hlyypb/ur88bupg18u0zpgw -->

:::success
**简介：**本文深入探讨了LLM从监督学习范式向强化学习（RL）范式演进的内在逻辑。文章首先分析了监督学习在通往通用人工智能（AGI）路径上的固有局限，随后阐述了 RL 作为新扩展方法的优势，解析了其核心机制与加权监督学习的本质区别，并最后总结了当前 RL for LLM 领域的五大核心研究问题。 <font style="color:#D22D8D;">(by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773143221705-90b99b2c-3db7-47f2-90cd-1b741f508184.png)

# **一、监督学习范式的固有局限性**
:::color3
**简介：**本章节分析了当前基于预训练和指令微调的监督学习范式在数据量级和质量上的瓶颈，指出了实现 AGI 所需的理想条件与现实情况之间的矛盾，从而引出探索新扩展方法的必要性。

:::

:::color5
**<font style="color:#601bde;">1. 现有范式及其核心依赖 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

大型语言模型的演进长期依赖于标准的监督学习（Supervised Learning）范式，该范式主要包含两个阶段：

+ [预训练](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=%E9%A2%84%E8%AE%AD%E7%BB%83&zhida_source=entity)（Pretrain）
+ [指令微调](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=%E6%8C%87%E4%BB%A4%E5%BE%AE%E8%B0%83&zhida_source=entity)（SFT）

这一范式的核心在于，模型必须依赖人类提供的、包含从输入到输出完整映射的监督信号进行学习。

:::color5
**<font style="color:#601bde;">2. 通往 AGI 的理想化前提</font>**

:::

若要仅凭监督学习路径达到[通用人工智能](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=%E9%80%9A%E7%94%A8%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&zhida_source=entity)（AGI）的高度，必须满足以下两个近乎理想化的前提条件：

1. **监督数据的无限性与完备性**：数据量级需趋于无穷，且其分布必须覆盖所有可能遇到的问题，以确保模型具备“全知性”。
2. **监督信号的绝对完美性**：所有监督数据必须准确无误，不存在任何错误或偏见，以确保模型的“正确性”。

:::color5
**<font style="color:#601bde;">3. 现实中的双重瓶颈 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

在现实应用中，上述两个理想条件均难以实现：

+ **数据瓶颈**：高质量的人类标注数据已遭遇“[数据瓶颈](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E7%93%B6%E9%A2%88&zhida_source=entity)”，其生产成本高昂且效率有限，难以满足无限性的要求。
+ **知识边界与偏差**：人类知识本身存在边界（例如许多科学未解之谜），且在标注过程中不可避免地会引入错误和主观偏见，无法保证绝对的完美性。

:::color5
**<font style="color:#601bde;">4. 扩展方法的演进方向</font>**

:::

鉴于上述局限，探索一种能够突破瓶颈的新扩展方法（scaling method）势在必行。这种新方法需要满足以下特征：

+ **高效扩展**：数据能够以更高效、低成本的方式进行规模化扩展。
+ **放宽依赖**：对监督信号的依赖程度降低，不再苛求“专家级别”的完美答案。

强化学习（RL）正是为此提供了可能的解决方案。

# **二、RL：应对挑战的新范式**
:::color3
**简介：**本章节阐述了强化学习（RL）被视为 LLM 持续进化关键的原因，重点分析了其在数据生成来源和监督信息性质两个方面的显著优势。

:::

:::color5
**<font style="color:#601bde;">1. 数据来源的根本性变革 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

RL 实现了**数据由模型与环境交互自发生成**。这一机制从根本上打破了外部数据来源的限制，为模型的持续学习提供了近乎无限的原材料。

:::color5
**<font style="color:#601bde;">2. 监督信息的降维：从生成到验证</font>**

:::

在 RL 范式中，**监督信息从“生成式”退化为“验证式”**：

+ RL 的核心是[奖励信号](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=%E5%A5%96%E5%8A%B1%E4%BF%A1%E5%8F%B7&zhida_source=entity)（reward）。
+ 它不要求监督者提供完美的“专家答案”，而只需对模型生成的答案进行有效性或质量的“验证”。
+ 基于“验证答案的难度远低于生成答案”这一基本事实[[1]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_1)，RL 大幅降低了对监督信息质量和标注难度的要求。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773143019415-909ac659-3e99-430b-bfd9-1072fbf2ba4c.png)

# **三、RL 的简洁定义与核心机制**
:::color3
**简介：**本章节通过对比监督学习（SFT）与强化学习（RL）的损失函数，从数学定义的角度解析 RL 的核心机制，指出其本质可视为一种特殊的加权监督学习。

:::

:::color5
**<font style="color:#601bde;">1. 监督学习（SFT）的数学表述 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

监督学习（SFT）的损失函数可以表达为：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773142204379-d58d827f-9003-482b-8a17-2b0c0abb89fb.png)

**参数说明：**

+ $ x $：提示（prompt）
+ $ y $：模型的生成内容
+ $ \pi_{ref} $：代表人类专家答案的真实分布
+ $ \pi_{\theta} $：模型的输出策略分布

**目标：** 最小化模型分布与专家分布之间的差异。

:::color5
**<font style="color:#601bde;">2. 强化学习（RL）的数学表述</font>**

:::

RL 的损失函数则可视为一种**加权监督学习**：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773142217444-72708c04-7320-404d-a7f4-06b689f88ba7.png)

:::color5
**<font style="color:#601bde;">3. 两者的核心区别 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

RL 与 SFT 的核心区别在于以下两点：

1. **引入权重项**：引入了权重项 $ w(x, y) $。
2. **分布替换**：代表人类专家答案的真实分布被替换为模型自己的输出策略分布。

# **四、RL 与普通加权监督学习的本质区别**
:::color3
**简介：**本章节深入剖析了 RL 区别于传统加权监督学习的独特之处，重点阐述了负权重带来的“趋利避害”机制以及自洽优化闭环的形成。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773143124719-a35c192c-4749-4f8e-9e17-431b63a5e96a.png)

:::color5
**<font style="color:#601bde;">1. 权重可为负值：实现“趋利避害” </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

RL 的特殊性在于其权重 $ w(x, y) $ 的设计：

+ **传统加权学习**：权重通常为非负，主要用于强调重要样本。
+ **强化学习（RL）**：权重可以为负。负权重指导模型“避免”生成特定的行为，而不仅仅是“模仿”期望的行为。
+ **机制意义**：这种“惩罚”机制是模型能够快速抛弃失败策略、探索未知但可能更优策略空间（Exploration）的关键[[2]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_2)[[3]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_3)，也是其能力超越训练数据限制的根本原因。

:::color5
**<font style="color:#601bde;">2. 自洽的优化闭环</font>**

:::

RL 将数据来源与权重机制结合，形成了一个强大的自优化循环：

1. **生成行为**：模型自身生成数据。
2. **获取反馈**：获得带有正或负权重的反馈。
3. **策略调整**：调整策略以增加高权重行为、减少低权重行为。
4. **迭代提升**：生成更高质量的新行为。

通过这一循环，只要权重（以及背后的 reward）设计得当，模型便有潜力实现持续的自我迭代与能力攀升，最终达到超越人类的性能水平。



# **五、RL for LLM 的核心研究问题**
:::color3
**简介：**本章节梳理了当前 RL for LLM 领域的研究框架，总结了从权重推导、信号获取、交互节奏、提示分布到基础模型能力等五个关键研究问题。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773142670163-c18361a6-88ec-4ec6-aec8-8638ab9f3aba.png)

:::color5
**<font style="color:#601bde;">1. 权重推导机制 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**核心问题：** 如何从“用于验证的弱监督信号（reward）”推导出每个样本的权重 $ w(x, y) $？

**现有解法示例：**

+ **ReST**[[4]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_4)：采用 0-1 过滤方法。
+ [PPO](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=PPO&zhida_source=entity)[[5]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_5)：学习价值函数（value function）。
+ [DeepSeek GRPO](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=DeepSeek+GRPO&zhida_source=entity)[[6]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_6)：从批次数据中估计优势函数（advantage function）。

:::color5
**<font style="color:#601bde;">2. 奖励信号获取</font>**

:::

**核心问题：** 承接上一点，如何高效、准确地获取“用于验证的弱监督信号（reward）”？

**技术路径：**

+ [RLHF](https://zhida.zhihu.com/search?content_id=259060702&content_type=Article&match_order=1&q=RLHF&zhida_source=entity)：使用可学习的 reward model[[7]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_7)。
+ **DeepSeek**：采用基于规则（rule-based）的 reward。

:::color5
**<font style="color:#601bde;">3. 交互与更新节奏 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**核心问题：** RL 的两个核心步骤——“基于加权监督学习的模型更新”与“新样本的生成”——二者的交互节奏是怎样的？

**关键权衡点：**

+ **更新频率**：是生成一个样本就更新一次（完全在线），还是生成 N 个样本后更新一次或 N 次？
+ **样本利用**：先前批次生成的样本在后续迭代中是否应该被舍弃（on-policy vs. off-policy 的权衡）？
+ **参数关联**：PPO/GRPO 算法中的修正比值、clip 参数、生成批次大小、更新的 epoch 数目等，均与此问题紧密相关。

:::color5
**<font style="color:#601bde;">4. 提示分布设计</font>**

:::

**核心问题：** RL 训练应选择怎样的提示（prompt）分布 $ p(x) $？

**示例：** 以数学问题为例，如何设计一个问题序列（课程），才能最大化模型的学习效率？[[8]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_8)

:::color5
**<font style="color:#601bde;">5. 基础模型先决条件</font>**

:::

**核心问题：** 进行 RL 训练前，基础模型（base model）需要具备哪些先决能力，才能有效支撑后续的强化学习过程？[[9]](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_9)

# <font style="color:rgb(25, 27, 31);">参考</font>
1. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_1_0)<font style="color:rgb(25, 27, 31);">All Roads Lead to Likelihood: The Value of Reinforcement Learning in Fine-Tuning</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2503.01067</font>](https://arxiv.org/abs/2503.01067)
2. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_2_0)<font style="color:rgb(25, 27, 31);">e3: Learning to Explore Enables Extrapolation of Test-Time Compute for LLMs</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/pdf/2506.09026</font>](https://arxiv.org/pdf/2506.09026)
3. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_3_0)<font style="color:rgb(25, 27, 31);">Preference Fine-Tuning of LLMs Should Leverage Suboptimal, On-Policy Data</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2404.14367</font>](https://arxiv.org/abs/2404.14367)
4. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_4_0)<font style="color:rgb(25, 27, 31);">Reinforced Self-Training (ReST) for Language Modeling</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2308.08998</font>](https://arxiv.org/abs/2308.08998)
5. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_5_0)<font style="color:rgb(25, 27, 31);">Proximal Policy Optimization Algorithms</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/1707.06347</font>](https://arxiv.org/abs/1707.06347)
6. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_6_0)<font style="color:rgb(25, 27, 31);">DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2402.03300</font>](https://arxiv.org/abs/2402.03300)
7. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_7_0)<font style="color:rgb(25, 27, 31);">Training language models to follow instructions with human feedback</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2203.02155</font>](https://arxiv.org/abs/2203.02155)
8. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_8_0)<font style="color:rgb(25, 27, 31);">SPEED-RL: Faster Training of Reasoning Models via Online Curriculum Learning</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2506.09016</font>](https://arxiv.org/abs/2506.09016)
9. [<font style="color:rgb(9, 64, 142);">^</font>](https://zhuanlan.zhihu.com/p/1916994928132751692#ref_9_0)<font style="color:rgb(25, 27, 31);">Scaling Test-Time Compute Without Verification or RL is Suboptimal </font>[<font style="color:rgb(9, 64, 142);">https://arxiv.org/abs/2502.12118</font>](https://arxiv.org/abs/2502.12118)

