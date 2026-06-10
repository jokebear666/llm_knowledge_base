# Deepseek-V3.2解读

<!-- source: yuque://zhongxian-iiot9/hlyypb/dy94ztxgw4k6sc0n -->

# <font style="color:rgb(26, 28, 30);">Deepseek-V3.2核心创新</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764753406359-66868abb-da77-4824-897e-bd98a96770e4.png)

:::color3
**<font style="color:rgb(26, 28, 30);">简介：</font>**<font style="color:rgb(26, 28, 30);">DeepSeek 于12月1日正式发布 </font>**<font style="color:#ED740C;">DeepSeek-</font>****<font style="color:#ED740C;">V3.2（正式版）与 </font>****<font style="color:#ED740C;">DeepSeek-</font>****<font style="color:#ED740C;">V3.2-Speciale（长思考增强版）两个模型</font>**<font style="color:rgb(26, 28, 30);">，旨在通过架构创新（DSA）与大规模强化学习，在大幅降低长文本推理成本的同时，实现媲美 GPT-5 和 Gemini-3.0-Pro 的推理与 Agent 能力。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(26, 28, 30);">paper：</font>**[**DeepSeek-V3.2**](https://cas-bridge.xethub.hf.co/xet-bridge-us/692cfec93b25b81d09307b94/2d0aa38511b9df084d12a00fe04a96595496af772cb766c516c4e6aee1e21246?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cas%2F20251203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251203T085815Z&X-Amz-Expires=3600&X-Amz-Signature=4158f25a44c7116896527ccb1ace7cbbe85a3a82a3ed4f04129d920314f5a780&X-Amz-SignedHeaders=host&X-Xet-Cas-Uid=685e07053e85fda10a3dc07a&response-content-disposition=inline%3B+filename*%3DUTF-8%27%27paper.pdf%3B+filename%3D%22paper.pdf%22%3B&response-content-type=application%2Fpdf&x-id=GetObject&Expires=1764755895&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NDc1NTg5NX19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2FzLWJyaWRnZS54ZXRodWIuaGYuY28veGV0LWJyaWRnZS11cy82OTJjZmVjOTNiMjViODFkMDkzMDdiOTQvMmQwYWEzODUxMWI5ZGYwODRkMTJhMDBmZTA0YTk2NTk1NDk2YWY3NzJjYjc2NmM1MTZjNGU2YWVlMWUyMTI0NioifV19&Signature=cHKX2GS5SwlH5BywLX02VZEyTSGXY0ch0T-ajxxRIUOpUSUSJHQE-uSIBgaBMDmts-iT2eX1Zcn-MOgBeM0O2W-VQdtzbGypAA1oFopBYFMsXAZWWQEQb9Ohcl6rTqPCuC5EHaZ0DGlood54BMu7Hw2ELQ4aYkxKT4famvQB-RoaCTxVr5wh0mcFud4J8NDsr7GNZHTYD3c%7Ev-ai2gkAc8TDT6ZjSFaXZk62u4DGfvoUhq-ZZMxCe7KF1yy1lHaPEiX-sE%7Et2gP4ovaIhC3tnVhdgMPT6yxZMgrRjOxf6Jd5vY1-bIiSmQKqixP0lyAGKRlR8GS5GLYOZAu1Y7RaQA__&Key-Pair-Id=K2L8F4GPSG1IFC)

**huggingface：**[**deepseek-ai/DeepSeek-V3.2-Exp**](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp/tree/main/inference)

:::

+ **<font style="color:rgb(26, 28, 30);">双模型策略明确</font>**<font style="color:rgb(26, 28, 30);">：V3.2 主打平衡实用与长文效率，适合通用 Agent 任务；V3.2-Speciale 主打极致推理与数学竞赛，探索能力边界。</font>
+ **<font style="color:rgb(26, 28, 30);">架构级创新 DSA</font>**<font style="color:rgb(26, 28, 30);">：引入 DeepSeek Sparse Attention（稀疏注意力机制），将长上下文计算复杂度大幅降低，推理成本显著下降。</font>
+ **<font style="color:rgb(26, 28, 30);">后训练（Post-Training）权重极大提升</font>**<font style="color:rgb(26, 28, 30);">：RL 训练的计算预算超过预训练成本的 10%，标志着开源模型进入“重后训练”时代。</font>
+ **<font style="color:rgb(26, 28, 30);">Agent 能力质变</font>**<font style="color:rgb(26, 28, 30);">：通过大规模合成数据管线和“工具调用中的思考”机制，解决了复杂任务中的泛化与指令跟随问题。</font>
+ **<font style="color:rgb(26, 28, 30);">性能对标顶尖闭源</font>**<font style="color:rgb(26, 28, 30);">：V3.2 综合水平达 GPT-5 级，Speciale 版本在数学/编程竞赛中超越 Gemini-3.0-Pro，但在 Token 效率上仍有优化空间。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752312719-0e1e9823-47a3-47ec-b005-67c93f4e7f89.png)

> 对 DeepSeek-V3.2 及其同类算法进行基准测试。对于 HMMT 2025，我们报告了 2 月份的比赛结果。与基线算法一致。对于 HLE，我们报告了纯文本子集的结果。
>

# <font style="color:rgb(26, 28, 30);">双版本定位与性能表现</font>
:::color3
**简介：12.1日**<font style="color:rgb(25, 27, 31);">DeepSeek同时发布两个正式版模型：</font>**<font style="color:#ED740C;">DeepSeek-V3.2和 </font>**[**<font style="color:#ED740C;">DeepSeek-V3.2-Speciale</font>**](https://zhida.zhihu.com/search?content_id=267117074&content_type=Article&match_order=1&q=DeepSeek-V3.2-Speciale&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。模型的参数量约为685B（6850亿），使用FP8精度推理占用685GB显存，需要8张H20（96GB）才可以放下。DeepSeek-V3.2 的目标是平衡推理能力与输出长度，适合日常使用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.DeepSeek-V3.2 (正式版)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">定位</font>**<font style="color:rgb(26, 28, 30);">：日常主力，替代 V3.1/Terminus。</font>
+ **<font style="color:rgb(26, 28, 30);">亮点</font>**<font style="color:rgb(26, 28, 30);">：输出长度更短，响应更快，Agent 能力强。</font>
+ **<font style="color:rgb(26, 28, 30);">成绩</font>**<font style="color:rgb(26, 28, 30);">：推理能力略低于 Gemini-3.0-Pro，但在 SWE-Verified（代码修复）等实战榜单上大幅领先开源模型。</font>

:::color5
**<font style="color:#601BDE;">2.DeepSeek-V3.2-Speciale (特化版)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">定位</font>**<font style="color:rgb(26, 28, 30);">：研究与竞赛，不考虑成本。</font>
+ **<font style="color:rgb(26, 28, 30);">亮点</font>**<font style="color:rgb(26, 28, 30);">：结合了 DeepSeek-Math-V2 的定理证明能力，拥有极强的归纳与逻辑推理能力。</font>
+ **<font style="color:rgb(26, 28, 30);">成绩</font>**<font style="color:rgb(26, 28, 30);">：斩获 IOI 2025 和 IMO 2025 金牌，在 AIME 等数学测试中超越 Gemini-3.0-Pro。</font>
+ **<font style="color:rgb(26, 28, 30);">代价</font>**<font style="color:rgb(26, 28, 30);">：Token 消耗巨大（思考过程极长），推理成本显著高于标准版。</font>

> <font style="color:rgb(25, 27, 31);">表中显示，DeepSeek-V3.2-Speciale通过增加推理token，在多个基准测试中实现了超越当前最优模型Gemini-3.0-Pro的性能。</font>
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764751872366-00a09144-1d92-476c-827e-5369bfeb2f54.png)

# <font style="color:rgb(26, 28, 30);">架构突破——DeepSeek Sparse Attention (DSA)</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">DSA 是本次更新最大的技术亮点，旨在解决长上下文处理中的“效率与性能平衡”难题。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752352786-a2657b0a-316b-4951-ba94-296b4fad5559.png)

> DeepSeek-V3.2 的注意力架构，其中 DSA 在 MLA 下实例化。绿色部分展示了 DSA 如何根据索引器选择前 k 个键值对条目。
>

:::color5
**<font style="color:#601BDE;">1.闪电索引与细粒度选择</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">这种创新带来了显著的性能提升，尤其是在长上下文场景下的训练和推理效率。</font><font style="color:rgb(26, 28, 30);"></font>

+ **<font style="color:rgb(25, 27, 31);">实现方式</font>**<font style="color:rgb(25, 27, 31);">：通过</font><font style="color:rgb(25, 27, 31);"> </font>[**<font style="color:rgb(9, 64, 142);">闪电索引器</font>**](https://zhida.zhihu.com/search?content_id=263817234&content_type=Article&match_order=1&q=%E9%97%AA%E7%94%B5%E7%B4%A2%E5%BC%95%E5%99%A8&zhida_source=entity)**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">(Lightning Indexer)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">实现一个</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">稀粒度 (Fine-Grained) 的稀疏注意力机制</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">注意力机制</font>**<font style="color:rgb(25, 27, 31);">：不同于传统注意力机制关注所有</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Key-Value (KV)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">对，DSA</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">只关注少量 Top-K 的相关 KV 对</font>**<font style="color:rgb(25, 27, 31);">，从而达到稀疏化的目的。</font>
+ **<font style="color:rgb(25, 27, 31);">稀粒度</font>**<font style="color:rgb(25, 27, 31);">：这里的“稀粒度”是指它不是简单地关注固定窗口内的 KV（如过去 2048 个时间步），而是 </font>**<font style="color:rgb(25, 27, 31);">精准地挑选 (Top-K)</font>**<font style="color:rgb(25, 27, 31);"> 出与当前 Query 最相关的 KV 对进行注意力计算。</font>
+ **<font style="color:rgb(26, 28, 30);">训练策略：</font>**<font style="color:rgb(26, 28, 30);">采用“两阶段训练”：先进行 Dense Warm-up（密集热身）训练索引器，再进行 Sparse Training（稀疏训练）让模型适应跳跃式读取信息。</font>
+ **<font style="color:rgb(26, 28, 30);">成本优势：</font>**<font style="color:rgb(26, 28, 30);">在 128K 长文本场景下，推理成本降低约 50%（预填充阶段成本从 $0.7/M 降至 $0.2/M）。</font>



# <font style="color:rgb(25, 27, 31);">DSA 机制的组成与原理</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">DeepSeek Sparse Attention (</font><font style="color:rgb(25, 27, 31);">DSA) 机制主要由两部分构成：</font><font style="color:#ED740C;">闪电索引器 (Lightning Indexer) 和 </font>[<font style="color:#ED740C;">稀粒度 Token 选择机制</font>](https://zhida.zhihu.com/search?content_id=263817234&content_type=Article&match_order=1&q=%E7%A8%80%E7%B2%92%E5%BA%A6+Token+%E9%80%89%E6%8B%A9%E6%9C%BA%E5%88%B6&zhida_source=entity)<font style="color:#ED740C;"> (Fine-Grained Token Selection)。</font>

:::

**MHA & MQA**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752645660-d785c252-e767-4758-9a16-dcc43e363436.png)

**DSA**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752651330-f4a1d786-2bc7-45f8-88ea-93481b70d153.png)

:::color5
**<font style="color:#601BDE;">1.闪电索引器 (Lightning Indexer)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">闪电索引器的作用是高效地计算当前</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Query (Q)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">与所有历史</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Key (K)</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">之间的相似度分数，作为后续 Token 选择的依据。在多个头上进行计算</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752402020-1c0d3918-da35-4e2a-9fc2-4756d788e37c.png)

**<font style="color:rgb(25, 27, 31);">高效性分析：</font>**

<font style="color:rgb(25, 27, 31);">论文中指出闪电索引器之所以高效，主要在于两点：</font>

1. **<font style="color:rgb(25, 27, 31);">更少的头数 (Fewer Heads)</font>**<font style="color:rgb(25, 27, 31);">：索引器使用的头数比标准的注意力机制更少（例如，原版可能 128 个头，索引器降至 64 个头）。</font>
2. **<font style="color:rgb(25, 27, 31);">低精度计算</font>**<font style="color:rgb(25, 27, 31);">：它能够使用 </font>**<font style="color:rgb(25, 27, 31);">FP8 精度</font>**<font style="color:rgb(25, 27, 31);">实现，极大地加速了计算。DeepSeek 专门为此编写了高度优化的 </font>**<font style="color:rgb(25, 27, 31);">Kernel 代码</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">2.稀粒度 Token 选择机制 (Fine-Grained Token Selection)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在得到所有 It,s 索引分数后，该机制会选择</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Top-K</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个最大的分数，对应的 KV 对即为需要参与注意力计算的稀疏集合 Cs。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752408066-d4affe28-8bce-4b58-9c58-8d9b7a9f1ab2.png)

**<font style="color:rgb(25, 27, 31);">关于稀疏化实现的细节：</font>**

<font style="color:rgb(25, 27, 31);">论文里面的写法，稀疏化应该是在计算 QKT 之前就筛选出 Top-K 的 K 矩阵，从而直接减少矩阵乘法 QKT 的复杂度。然而，根据对源码的分析（视频中提到），DeepSeek-V3.2 的实际实现方式似乎是：</font>

1. **<font style="color:rgb(25, 27, 31);">先计算完整的 QKT 矩阵</font>**<font style="color:rgb(25, 27, 31);">（得到 Score 矩阵）。</font>
2. **<font style="color:rgb(25, 27, 31);">使用闪电索引器和 Top-K 机制</font>**<font style="color:rgb(25, 27, 31);">，确定哪些 KV 对是相关的。</font>
3. **<font style="color:rgb(25, 27, 31);">生成一个 Mask 掩码</font>**<font style="color:rgb(25, 27, 31);">：将 Score 矩阵中不被 Top-K 关注的位置设置为 −∞（负无穷大）。</font>
4. **<font style="color:rgb(25, 27, 31);">将 Mask 加到 Score 矩阵上</font>**<font style="color:rgb(25, 27, 31);">，再进行</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Softmax</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和乘以 V 向量。</font>

**<font style="color:rgb(25, 27, 31);">这种实现方式的推论：</font>**

+ **<font style="color:rgb(25, 27, 31);">复杂度降低集中在 Softmax</font>**<font style="color:rgb(25, 27, 31);">：矩阵乘法 QKT 的复杂度仍为 O(L2D)（其中 L 是上下文长度， D 是维度），但在</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Softmax</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">步骤中，由于大量数值被 Mask 为 −∞，实际参与有效计算的只有 O(LK) 个分数（K 为 Top-K 数量），从而将整体的推理复杂度从 O(L2)</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">有效降低到 O(LK)</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">内存连续性优化</font>**<font style="color:rgb(25, 27, 31);">：视频中提到，先计算完整的矩阵乘法可能是为了 </font>**<font style="color:rgb(25, 27, 31);">保持矩阵在内存中的连续性</font>**<font style="color:rgb(25, 27, 31);">，从而能更好地利用硬件加速，使整体效率高于在矩阵乘法阶段就进行稀疏化（这可能破坏内存的连续性）。</font>

# <font style="color:rgb(26, 28, 30);">训练策略</font>
:::success
<font style="color:rgb(25, 27, 31);">DeepSeek V3.2 的训练分为两个主要部分：</font>

:::

## 继续[<font style="color:rgb(9, 64, 142);">预训练</font>](https://zhida.zhihu.com/search?content_id=263817234&content_type=Article&match_order=1&q=%E8%BF%9E%E7%BB%AD%E9%A2%84%E8%AE%AD%E7%BB%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> (Continual Pre-training)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在 V3.1 的检查点上进行连续训练，主要包括两个阶段：</font>

:::

:::color5
**<font style="color:#601BDE;">1.阶段一：索引器预热 (Indexer Warm-up)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">目标</font>**<font style="color:rgb(25, 27, 31);">：初始化和训练</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">闪电索引器</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">方法</font>**<font style="color:rgb(25, 27, 31);">：在此阶段，模型</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">不进行稀疏 Token 选择</font>**<font style="color:rgb(25, 27, 31);">（不取 Top-K）。</font>
+ **<font style="color:rgb(25, 27, 31);">损失函数</font>**<font style="color:rgb(25, 27, 31);">：使用 </font>[**<font style="color:rgb(9, 64, 142);">KL 散度</font>**](https://zhida.zhihu.com/search?content_id=263817234&content_type=Article&match_order=1&q=KL+%E6%95%A3%E5%BA%A6&zhida_source=entity)**<font style="color:rgb(25, 27, 31);"> (Kullback–Leibler Divergence)</font>**<font style="color:rgb(25, 27, 31);"> 来对齐索引器的输出分布 It 和原始注意力分布 Pt。  
</font><font style="color:rgb(25, 27, 31);">这要求索引器计算出的相似度分布与原始的注意力权重分布保持一致。</font>

:::color5
**<font style="color:#601BDE;">2.阶段二：稀疏化吸收训练 (Sparse Assimilation Training)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">目标</font>**<font style="color:rgb(25, 27, 31);">：引入</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">稀粒度 Token 选择机制</font>**<font style="color:rgb(25, 27, 31);">，并优化所有模型参数。</font>
+ **<font style="color:rgb(25, 27, 31);">损失函数</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">结合</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">传统的</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">NTP (Next Token Prediction) 损失</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">LNTP 和</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">索引器自身的损失</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">Lindexer。  
</font><font style="color:rgb(25, 27, 31);">Ltotal=LNTP+Lindexer  
</font><font style="color:rgb(25, 27, 31);">Lindexer 关注的是被</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Top-K 选出的稀疏集合</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">St 上的分布 PSt 与原始分布 Pt 之间的相似性，要求模型在稀疏化后仍能保持准确性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752746036-49e9f89f-b79a-4938-8d53-9dbf186f0902.png)

> 推理数据system prompt示例。该系统提示要求模型在标签 <think></think> 中输出推理过程。
>

## <font style="color:rgb(25, 27, 31);">后训练 (Post-Training)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了严格评估 DSA 带来的影响，后训练阶段保持了与 V3.1 </font>**<font style="color:rgb(25, 27, 31);">完全相同的</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">后训练方案、算法和数据</font>**<font style="color:rgb(25, 27, 31);">（包括专家蒸馏和混合强化学习等）。</font><font style="color:rgb(26, 28, 30);">DeepSeek 团队强调开源模型以往在后训练阶段投入不足，V3.2 对此进行了报复性增强。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752568990-0972ef39-f49b-41f1-ac1d-f01e77f90a36.png)

> 使用完全合成的通用代理数据对 DeepSeek-V3.2-SFT 进行强化学习训练。
>

+ **<font style="color:rgb(26, 28, 30);">算力投入</font>**
    - <font style="color:rgb(26, 28, 30);">明确指出 RL 阶段的计算资源投入已超过预训练成本的 10%，用于解锁模型的深层智力。</font>
+ **<font style="color:rgb(26, 28, 30);">算法改进 (GRPO)</font>**
    - **<font style="color:rgb(26, 28, 30);">无偏 KL 估计</font>**<font style="color:rgb(26, 28, 30);">：修正估计器误差，消除系统性偏差。</font>
    - **<font style="color:rgb(26, 28, 30);">离策略序列掩码</font>**<font style="color:rgb(26, 28, 30);">：过滤掉偏离策略过远的负样本，防止模型“学偏”。</font>
    - **<font style="color:rgb(26, 28, 30);">保持路由 (Keep Routing)</font>**<font style="color:rgb(26, 28, 30);">：确保 MoE 模型在训练和推理时专家激活路径一致，提升稳定性。</font>
+ **<font style="color:rgb(26, 28, 30);">专家蒸馏</font>**
    - <font style="color:rgb(26, 28, 30);">训练了数学、编程、逻辑等 6 个领域的专家模型，生成特定数据来训练最终模型。</font>

# <font style="color:rgb(26, 28, 30);">Agent 能力与数据合成管线</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">针对复杂任务和工具使用场景，V3.2 进行了专门的优化，使其更像一个能干活的智能体。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752421153-ba27eb8c-ff8c-4f35-a807-70a795071f49.png)

> 工具调用场景中的思维保留机制。
>

:::color5
**<font style="color:#601BDE;">1.Thinking in Tool-Use (边做边想)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(26, 28, 30);">打破了以往“推理-行动”割裂的模式，模型在调用工具的过程中保留推理上下文，仅在引入新用户消息时才丢弃旧推理，大幅提升任务连贯性。</font>

:::color5
**<font style="color:#601BDE;">2.大规模合成数据管线</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">难解易验</font>**<font style="color:rgb(26, 28, 30);">：构建了“生成困难但验证简单”的任务（如复杂旅行规划）。</font>
+ **<font style="color:rgb(26, 28, 30);">数据规模</font>**<font style="color:rgb(26, 28, 30);">：自动合成了 1800+ 个环境和 85,000+ 条复杂指令，涵盖代码、搜索、通用任务。</font>
+ **<font style="color:rgb(26, 28, 30);">效果</font>**<font style="color:rgb(26, 28, 30);">：不依赖特定工具的过拟合，而是通过合成数据获得了强大的泛化能力。</font>

**任务示例：Trip Planning**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752459913-16677463-bdbd-46d8-b565-9435d1481034.png)

**工具设置示例**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764752464034-6e55bc18-caa4-49ba-bd49-028eefcecc85.png)

