# TurboQuant：KV Cache量化压缩算法

<!-- source: yuque://zhongxian-iiot9/hlyypb/ncty75q55g7bav28 -->

:::success
**背景：**谷歌在ICLR 2026上展示了**<font style="color:#74B602;">TurboQuant压缩算法，该算法能在零精度损失的前提下，将AI推理过程中的KV Cache压缩至少6倍</font>**，引发了市场对存储芯片需求的担忧，导致美光和西部数据等存储巨头股价大跌。

:::

:::color3
**简介：**向量量化（Vector Quantization）问题源于香农的信源编码理论，其核心目标是对高维欧几里得向量进行量化，同时尽可能最小化其几何结构的失真。然而，现有的量化方法存在一定的局限性，无法达到最优的失真率。为了克服这些缺陷并**<font style="color:#ED740C;">同时解决均方误差（MSE）和内积失真（Inner Product Distortion）问题</font>**，本文提出了一种全新的量化方法——**<font style="color:#ED740C;">TurboQuant</font>**。 <font style="color:#D22D8D;">（by草莓师姐）</font>

**论文地址：**[**https://arxiv.org/pdf/2504.19874**](https://arxiv.org/pdf/2504.19874)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774529342390-7a9eb44d-381d-41c3-b6a1-69bbb574dde6.png)

:::color5
**<font style="color:#601bde;">1. 存储芯片巨头股价大跌与TurboQuant算法的发布</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">TurboQuant 是一种“数据无关（data-oblivious）”的算法，非常适用于在线应用场景。它能够在所有位宽和维度下，实现接近最优的失真率（与理论上的最优下界仅相差约 2.7 倍的小常数因子）。其核心方法与机制包括以下两个主要方面：</font>**

1. **<font style="background-color:#D9EAFC;">随机旋转与独立标量量化：</font>**
    1. TurboQuant 首先对输入向量进行随机旋转，这一操作会在坐标上诱导出一种集中的 Beta 分布。接着，算法利用高维空间中不同坐标之间“近似独立”的特性，直接对每个坐标应用最优的标量量化器（Scalar Quantizers），从而高效地完成基础量化。
2. **<font style="background-color:#D9EAFC;">消除内积偏差的两阶段策略：</font>**
    1. 研究发现，最优的 MSE 量化器会在内积估计时引入偏差。为了解决这一问题，TurboQuant 提出了一种两阶段（Two-stage）的处理方法：
        * 第一阶段：首先应用 MSE 量化器进行初步量化；
        * 第二阶段：对量化后产生的残差（Residual）应用 1-bit 的量化 JL（QJL）变换。通过这种组合，TurboQuant 成功构建出了一个无偏的内积量化器。



# **KVCache量化到3 bit**
:::color3
**简介：**KV Cache作为AI大模型推理时的核心内存瓶颈，传统量化方法存在额外开销。TurboQuant通过**<font style="color:#ED740C;">PolarQuant（极坐标量化）和QJL（量化JL变换）两步创新</font>**，消除了额外开销，实现了3-bit无损量化。

:::

:::color5
**<font style="color:#601bde;">1. KV Cache的内存瓶颈与传统量化方法的局限</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(13, 18, 57);">KV Cache内存瓶颈</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">AI大模型推理时，处理过的信息临时存储在KV Cache中以避免重复计算，形成高速“速查表”。</font>
    - <font style="color:rgb(13, 18, 57);">随着上下文窗口延长（如从4K扩展至百万级别），</font>**<font style="color:#117CEE;">KV Cache大小随对话长度线性膨胀</font>**<font style="color:rgb(13, 18, 57);">。</font>
    - <font style="color:rgb(13, 18, 57);">KV Cache占用的显存往往超过模型参数本身，成为AI推理的核心瓶颈。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774529376769-6a32dc27-5191-4c2f-b2fc-506c5432efd4.png)

2. **<font style="color:rgb(13, 18, 57);">传统量化方法的局限</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">传统方案采用向量量化，将16-bit浮点数压缩为4-bit整数。</font>
    - <font style="color:rgb(13, 18, 57);">局限性在于需为每块数据额外存储全精度的“量化常数”进行对齐。</font>
    - <font style="color:rgb(13, 18, 57);">每个数字额外占用1到2个bit，导致名义上的</font>**<font style="color:#117CEE;">4-bit压缩实际占用5到6-bit，压缩效率大打折扣</font>**<font style="color:rgb(13, 18, 57);">。</font>

:::color5
**<font style="color:#601BDE;">第一阶段：PolarQuant（极坐标量化）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(13, 18, 57);">坐标系转换</font>**<font style="color:rgb(13, 18, 57);">：放弃传统笛卡尔坐标系，</font>**<font style="color:#74B602;">转而使用极坐标（距离+角度）描述数据</font>**<font style="color:rgb(13, 18, 57);">，避免了因各轴取值范围不固定而需额外存储归一化参数的问题。</font>
+ **<font style="color:rgb(13, 18, 57);">随机旋转降维</font>**<font style="color:rgb(13, 18, 57);">：对数据向量进行随机旋转，</font>**<font style="color:#74B602;">使各坐标分量收敛至高度集中的Beta分布</font>**<font style="color:rgb(13, 18, 57);">，将高维量化降维为一维标量量化，推理时直接查表即可。</font>

![](https://cdn.nlark.com/yuque/0/2026/gif/29769680/1774525482710-bbddc9cf-f0ff-4bdf-ae1f-c0f6f9ede65d.gif)  
**<font style="color:#74B602;">PolarQuant就像一座高效的压缩桥梁，能把笛卡尔坐标输入转换成紧凑的极坐标「速记」形式，方便后续的存储和处理</font>**

+ **递归配对机制**：将数据拆分为半径（信号强度）和角度（信号方向），通过两两分组递归进行极坐标变换，最终浓缩为一个半径和一系列角度
+ **零额外开销：**转换后角度分布模式已知且集中，无需存储归一化常数。此阶段消耗大部分压缩预算（b-1个bit），将均方误差（MSE）降至最低。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774529332667-b42cfefc-5969-43aa-84a9-5973503504dd.png)

:::color5
**<font style="color:#601BDE;">第二阶段：QJL（量化JL变换）</font>**<font style="color:#601BDE;"></font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(13, 18, 57);">消除系统性偏差</font>**<font style="color:rgb(13, 18, 57);">：针对第一阶段残留的微小误差及1-bit量化器引入的乘性偏差，应用Johnson-Lindenstrauss变换进行修正。</font>
+ **<font style="color:rgb(13, 18, 57);">符号位压缩</font>**<font style="color:rgb(13, 18, 57);">：将每个误差值压缩为一个符号位（+1或-1），配合特殊估计器进行联合计算，实现数学上的“无偏”内积期望值。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774529326517-268537f7-a676-411e-8830-b7c27d3e5b50.png)

+ **<font style="color:#D22D8D;">极致压缩效果：</font>**结合PolarQuant和QJL，在仅3-bit总预算下实现接近无损压缩，无需训练或微调，全程零额外开销。
+ **<font style="color:#D22D8D;">逼近物理极限：</font>**MSE失真率控制在理论绝对下限的2.7倍以内（1-bit下仅为1.45倍），且算法“数据无感知”，全程向量化运算，对GPU极度友好。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774525482919-ca63ec3d-dd0e-4f59-b37d-e4bf47afedcf.png)

