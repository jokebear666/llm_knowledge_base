# 6️⃣ VLA模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/ftocdy9vnrlq0igr -->

#  VLA (Vision Language Action) 模型介绍
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">VLA模型最早见于机器人行业。2023年7月28日，谷歌DeepMind发布了全球首个控制机器人的视觉语言动作（VLA）模型RT-2。其后，这个模型概念快速扩散到智驾领域。</font>

:::

:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">VLA模型是在视觉语言模型（VLM）的基础上发展而来的。V</font>**<font style="color:#ED740C;">LM是一种能够处理图像和自然语言文本的机器学习模型，它可以将一张或多张图片作为输入，并生成一系列标记来表示自然语言</font>**<font style="color:rgba(0, 0, 0, 0.9);">。然而，VLA不仅限于此，它还利用了机器人或汽车运动轨迹的数据，进一步训练这些现有的VLM，</font>**<font style="color:#ED740C;">以输出可用于机器人或汽车控制的动作序列</font>**<font style="color:rgba(0, 0, 0, 0.9);">。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgba(0, 0, 0, 0.9);">paper：</font>**[**https://arxiv.org/pdf/2406.09246**](https://arxiv.org/pdf/2406.09246)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763376420527-45d82d7c-22ca-48db-8747-22cafa655865.png)

:::color5
**<font style="color:#601BDE;">VLM模型特点</font>**<font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(15, 17, 21);">在语言条件化机器人任务中，策略模型需同时具备以下能力：</font>

+ <font style="color:rgb(15, 17, 21);">理解自然语言指令</font>
+ <font style="color:rgb(15, 17, 21);">通过视觉感知环境状态</font>
+ <font style="color:rgb(15, 17, 21);">生成符合指令且适应场景的动作序列</font>

<font style="color:rgb(15, 17, 21);">正是这一多重需求，使得VLA所具备的多模态融合能力成为实现高效机器人智能的关键支撑。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763376428681-47c8d135-19f3-43e4-ac98-f10116d66649.png)

## <font style="color:rgba(0, 0, 0, 0.9);">VLA的特点与优势</font>
:::color5
**<font style="color:#601BDE;">1.端到端架构</font>**<font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">VLA是一个端到端的大模型，这意味着它可以简化传统上需要多个独立模块才能完成的任务流程。例如，在自动驾驶领域，传统的做法是将感知、预测、规划等步骤分开处理，而VLA则试图用一个统一的框架来替代这种分立的方法。这不仅可以提高系统的效率，还能增强其灵活性和适应性。</font>

:::color5
**<font style="color:#601BDE;">2.泛化能力</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">VLA具有强大的泛化能力。以谷歌DeepMind推出的RT-2为例，该模型可以在新的物体、背景和环境中表现出显著改善的性能。它可以理解并响应那些在训练数据集中未曾出现过的命令，并基于底层语言模型提供的思路链进行推理，从而做出合理的决策。比如，当被要求选择一块石头作为临时锤子时，或者推荐给疲惫的人一杯能量饮料，这些都是RT-2所展示出的能力。</font>

:::color5
**<font style="color:#601BDE;">3.通用性</font>**<font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">VLA具备高度的通用性。由于它是建立在一个通用的大规模预训练基础上，因此理论上几乎所有的“智能机器设备”都可以使用这套算法。无论是汽车、飞行器还是其他类型的机器人，只需要经过适当的微调就能满足特定应用场景的需求。这也解释了为什么近年来许多企业都在积极探索如何将通用AI应用于不同的机械设备上，以实现所谓的“具身智能”。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763372388556-7b547644-1528-4ce0-bde9-4220cf3a14f9.webp)

## <font style="color:rgba(0, 0, 0, 0.9);">OpenVLA</font>
:::color3
**简介：**<font style="color:rgb(44, 44, 54);">VLA模型旨在整合视觉、语言和动作三种模态的信息，以实现从感知到决策再到执行的端到端学习。VLA模型通过整合视觉、语言与动作信息，实现从感知到控制的端到端决策。其核心工作流程包含以下几个关键阶段与模块。</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgba(0, 0, 0, 0.9);">paper：</font>**[**https://arxiv.org/pdf/2406.09246**](https://arxiv.org/pdf/2406.09246)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763376440379-6a64dec8-d726-4525-923c-8d7443a770cc.png)

:::color5
**<font style="color:#601BDE;">1.多模态输入处理</font>**<font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

多模态输入处理：模型接收来自多种来源的输入数据，并进行统一预处理，随后送入对应的编码器：

+ 视觉输入：图像或视频流。![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763376642637-8f88bbe9-a697-4609-936d-08b5ea783c10.png)
+ 语言输入：文本描述或指令。
+ 动作输入：环境中的物理运动数据或历史动作序列。

:::color5
**<font style="color:#601BDE;">2.编码器模块</font>**

:::

各模态信息通过独立的编码器转换为特征表示：

+ 视觉编码器
    - 采用深度卷积神经网络（CNNs）或Vision Transformers等先进架构。
    - 代表性技术：DinoV2、SigLIP，用于生成高质量的视觉特征表示。
+ 语言编码器
    - 基于Transformer架构的语言模型（如Llama-2）。
    - 负责解析自然语言指令，将其转化为机器可理解的语义表示。
+ 动作编码器
    - 专门设计的网络，将历史动作轨迹或序列编码为低维向量。

:::color5
**<font style="color:#601BDE;">3.跨模态融合层</font>**

:::

本层是模型的核心，旨在实现不同模态信息间的深度交互与互补：

+ 融合方法：采用注意力机制、门控循环单元（GRUs）、长短期记忆网络（LSTMs）等技术。
+ 主要目标：确保视觉、语言和动作信息在统一的特征空间内进行对比、关联与整合。

:::color5
**<font style="color:#601BDE;">4.解码器模块</font>**<font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

基于融合后的多模态信息，生成具体的控制指令：

+ 动作解码器
    - 预测下一步应执行的动作。
    - 常采用策略梯度等强化学习算法，通过试错不断优化策略。
+ 反馈回路（高级版本具备）
    - 引入反馈机制，根据动作的实际执行结果动态调整后续行为，形成闭环控制。

:::color5
**<font style="color:#601BDE;">5.训练与优化</font>**

:::

+ 数据与方法：使用大规模真实世界机器人演示数据进行监督/半监督学习，并结合模拟环境中的强化学习以提升性能。
+ 优化技术：采用正则化方法及Adam等优化器，以防止过拟合并加速模型收敛。

:::color5
**<font style="color:#601BDE;">6.部署与推理</font>**<font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ 应用场景：训练完成的模型可部署于自动驾驶车辆、服务机器人等实体平台。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763376449977-989ee864-3a38-45df-88a1-31485c8e64f6.png)

## <font style="color:rgba(0, 0, 0, 0.9);">前瞻研究的进展</font>
:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">目前，关于VLA的研究主要集中在几个方面： </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:#601BDE;">开放源代码项目</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如OpenVLA是由斯坦福大学、加州大学伯克利分校、谷歌DeepMind以及丰田研究院联合开发的一个开源项目。它使用了一个包含约97万个真实世界机器人演示的数据集来进行训练，并且采用了Llama-2语言模型主干、SigLIP及DinoV2组成的双部分视觉编码器等先进技术。实验表明，这种方法极大地提高了先前策略的性能和泛化能力。</font>
2. **<font style="color:#601BDE;">3D扩展</font>**<font style="color:rgba(0, 0, 0, 0.9);">：一些研究开始尝试将二维的VLA模型拓展到三维空间，以便更好地模拟现实世界的交互过程。例如，3D-VLA就是一个旨在创建三维视觉-语言-动作生成世界模型的工作，它试图克服现有方法仅依赖于二维输入所带来的局限性。</font>

## <font style="color:rgba(0, 0, 0, 0.9);">开发应用挑战</font>
:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">尽管VLA展现出了诸多潜力，但在实际应用过程中仍然面临不少挑战： </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:#601BDE;">计算资源需求：</font>**<font style="color:rgba(0, 0, 0, 0.9);">大型VLA模型通常拥有数十亿级别的参数量，这导致它们在运行时对计算资源的要求极高。特别是在边缘设备上部署时，必须考虑如何优化推理速度以确保实时性。</font>
2. **<font style="color:#601BDE;">数据获取难度：</font>**<font style="color:rgba(0, 0, 0, 0.9);">为了使VLA能够有效工作，往往需要大量的高质量训练样本。但现实中获取这样丰富且多样化的数据并非易事，尤其是在某些特殊行业或场景下。</font>
3. **<font style="color:#601BDE;">VLA的模型对于算力的需求很大</font>**<font style="color:rgba(0, 0, 0, 0.9);">：单片AI算力1000Tops的Thor大概率会延期发布，加上英伟达芯片的量产时间与成本挑战，以及在国内的应用情况，对车企而言是个大问题。也希望未来会有更多的国产大算力芯片实现车型搭载。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763372388993-30ed5e57-051b-4da8-9ca2-6dab14e5abc4.webp)

<font style="color:rgba(0, 0, 0, 0.9);">  
</font>

