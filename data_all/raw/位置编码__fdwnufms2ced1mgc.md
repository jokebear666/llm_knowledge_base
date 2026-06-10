# 位置编码

<!-- source: yuque://zhongxian-iiot9/hlyypb/fdwnufms2ced1mgc -->

# <font style="color:#000000;">大模型外推</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">外推性挑战：</font>**<font style="color:rgb(25, 27, 31);">如何在</font>**<font style="color:#ED740C;">推理阶段确保模型能处理远超预训练时的文本长度</font>**<font style="color:rgb(25, 27, 31);">，已成为当前大型模型面临的核心问题之一，我们将此问题视为大模型的</font>**<font style="color:rgb(25, 27, 31);">外推性挑战</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">参考：</font>[再论大模型位置编码及其外推性（万字长文）](https://zhuanlan.zhihu.com/p/675243992)<font style="color:#000000;"> </font>[十分钟读懂旋转编码（RoPE）](https://zhuanlan.zhihu.com/p/647109286)

:::

:::color5
**<font style="color:#601BDE;">1.背景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">现在，众多大型模型已开始支持</font>**<font style="color:rgb(25, 27, 31);">长文本</font>**<font style="color:rgb(25, 27, 31);">的推理，如最新的</font>[<font style="color:rgb(9, 64, 142);">GPT4 Turbo</font>](https://zhida.zhihu.com/search?content_id=238184119&content_type=Article&match_order=1&q=GPT4+Turbo&zhida_source=entity)<font style="color:rgb(25, 27, 31);">能处理超过</font>**<font style="color:rgb(25, 27, 31);">128k</font>**<font style="color:rgb(25, 27, 31);">的内容，而</font>[<font style="color:rgb(9, 64, 142);">Baichuan2</font>](https://zhida.zhihu.com/search?content_id=238184119&content_type=Article&match_order=1&q=Baichuan2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">也可应对最长为</font>**<font style="color:rgb(25, 27, 31);">192K</font>**<font style="color:rgb(25, 27, 31);">的文本。但受显存资源约束，</font>**<font style="color:#DF2A3F;">这些模型在训练时并不一定会处理如此长的文本，其预训练阶段通常仅涉及约4k的内容。</font>**

:::color5
**<font style="color:#601BDE;">2.如何提升外推能力</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **位置编码外推**：
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：Transformer的绝对位置编码在超长序列失效</font>
    - **<font style="color:rgb(51, 51, 51);">方案</font>**<font style="color:rgb(51, 51, 51);">：ALiBi（Attention with Linear Biases）  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740551133293-625bac8b-2578-491b-b78d-fc902c0bb594.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">（其中 m</font>_<font style="color:rgb(51, 51, 51);">m</font>_<font style="color:rgb(51, 51, 51);"> 为头特定的斜率系数）</font>
2. **长度泛化技术**：
    - **<font style="color:rgb(51, 51, 51);">NTK-aware Scaling</font>**<font style="color:rgb(51, 51, 51);">：动态调整RoPE的旋转角  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740551141483-4effa05b-e572-4fc4-a049-80cc153cb441.png)
3. **推理策略增强**：
    - **<font style="color:rgb(51, 51, 51);">Chain-of-Thought（CoT）</font>**<font style="color:rgb(51, 51, 51);">：通过思维链引导模型分步推理</font>
    - **<font style="color:rgb(51, 51, 51);">Self-Consistency</font>**<font style="color:rgb(51, 51, 51);">：多路径推理投票选择最优解</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **超长文本生成**：
    - <font style="color:rgb(51, 51, 51);">输入：10k tokens的文档</font>
    - <font style="color:rgb(51, 51, 51);">挑战：传统Transformer在4k tokens后质量下降</font>
    - <font style="color:rgb(51, 51, 51);">方案：YARN（Yet Another RoPE Extension）位置编码</font>
2. **数值推理外推**：
    - <font style="color:rgb(51, 51, 51);">训练数据：数字范围0-1000的数学题</font>
    - <font style="color:rgb(51, 51, 51);">测试数据：1000-10000的数值计算</font>
    - <font style="color:rgb(51, 51, 51);">表现：GPT-4在加法任务上>95%准确率（10^18范围）</font>

:::color5
**<font style="color:#601BDE;">4.外推能力评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **长度外推比**（Length Extrapolation Ratio）：  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740551286520-a71d2683-2e31-40a3-be1e-1c9d190d4985.png)
    - <font style="color:rgb(51, 51, 51);">GPT-4：LER ≈ 4（32k训练→128k有效）</font>
2. **数值外推准确率**：

| **模型** | **加法（10^3→10^6）** | **乘法（10^2→10^4）** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">LLaMA2-7B</font> | <font style="color:rgb(51, 51, 51);">32.1%</font> | <font style="color:rgb(51, 51, 51);">12.4%</font> |
| <font style="color:rgb(51, 51, 51);">GPT-4</font> | <font style="color:rgb(51, 51, 51);">98.7%</font> | <font style="color:rgb(51, 51, 51);">76.8%</font> |


3. **开放域生成质量**（使用MAUVE指标）：
    - <font style="color:rgb(51, 51, 51);">对比生成文本与人类参考文本的分布相似性</font>

# 绝对位置编码(bert)<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">在Transformer模型中，位置编码（PositionEncoding）⽤于</font>**<font style="color:#ED740C;">引⼊序列中各个词的位置信息</font>**<font style="color:#1f2329;">。由 于Transformer模型的⾃注意⼒机制（Self-Attention）不具备处理序列顺序的能⼒，因此需要位置编码来补充这⼀信息。</font>

<font style="color:rgb(25, 27, 31);">基于Sinusoidal（正弦）的位置编码最初是由谷歌在论文Attention is All You Need中提出的方案，用于Transformer的位置编码。</font><font style="color:#D22D8D;"></font>

:::

**<font style="color:#117CEE;">核心思想</font>**

+ <font style="color:#1f2329;">绝对位置编码</font>**<font style="color:#ED740C;">使⽤正弦和余弦函数来编码每个位置的绝对位置</font>**<font style="color:#1f2329;">。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">频率递减机制是通过指数递增的分⺟来实现的。对于较⾼的维度</font><font style="color:#1f2329;">2</font>_<font style="color:#1f2329;">i </font>_<font style="color:#1f2329;">，分⺟的值更⼤，从⽽使得频率较低。这使得</font>**<font style="color:#de7802;">⾼维度的编码可以捕捉⻓距离的信息，⽽低维度的编码则捕 捉短距离的信息</font>**<font style="color:#1f2329;">。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:#1f2329;">Transformer中常⽤的位置编码⽅法是</font>**<font style="color:#ED740C;">正弦-余弦位置编码</font>**<font style="color:#1f2329;">（SinusoidalPositionEncoding）。具体⽽⾔，位置编码是⼀个与输⼊词嵌⼊（Word Embedding）相加的向量，其计算⽅式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738832426481-82189353-a76d-4227-aaa2-1f36c23e42f5.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738832429767-793c9e8c-66bc-4667-925a-3137cbb0fbd7.png)

:::color5
**<font style="color:#601BDE;">2.核心结论</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">具有</font>**<font style="color:rgb(25, 27, 31);">相对位置表达能力</font>**<font style="color:rgb(25, 27, 31);">：Sinusoidal可以学习到相对位置，对于固定位置距离的k，PE(i+k)可以表示成PE(i)的线性函数。</font>
+ <font style="color:rgb(25, 27, 31);">两个</font>**<font style="color:rgb(25, 27, 31);">位置向量的内积只和相对位置 k 有关</font>**<font style="color:rgb(25, 27, 31);">。Attention中的重要操作就是内积。计算两个位置的内积PE(t+k)PE(t)如下所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740551735260-4437bdb5-f3f8-4f02-a16e-2e5847cbbd96.png)

<font style="color:rgb(25, 27, 31);">可以看到，最终的结果是关于k的一个常数。这表明两个位置向量的内积只和相对位置k有关。</font>

+ <font style="color:rgb(25, 27, 31);">Sinusoidal编码具有</font>**<font style="color:rgb(25, 27, 31);">对称性</font>**<font style="color:rgb(25, 27, 31);">。通过计算，很容易得到PE(t+k)PE(t) = PE(t)PE(t-k)，这表明Sinusoidal编码具有</font>**<font style="color:rgb(25, 27, 31);">对称性</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ <font style="color:rgb(25, 27, 31);">随着k的增加，内积的结果会直接减少，即会存在</font>**<font style="color:rgb(25, 27, 31);">远程衰减</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740551751952-5cc65417-6135-4236-bf0d-25f124f2a2bd.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**优点**

+ **<font style="color:#ED740C;">捕捉序列顺序</font>**<font style="color:#1f2329;">：位置编码使得Transformer能够区分词语在序列中的位置，从⽽理解上下⽂信息。这对于处理⾃然语⾔ 序列尤其重要，因为序列的顺序对语义理解具有关键作⽤。</font>
+ **<font style="color:#ED740C;">保持全局一致性</font>**<font style="color:#1f2329;">：由于位置编码在不同位置上是具有唯⼀性的，因此它帮助模型维持序列中的全局⼀致性，保证对整个序列的理解。</font>
+ **<font style="color:#ED740C;">增强模型能力</font>**<font style="color:#1f2329;">：位置编码使得⾃注意⼒机制能够基于位置信息进⾏加权，有效提升了模型对⻓距离依赖的处理能⼒。</font>

**缺点**

+ **<font style="color:#ED740C;">固定的位置编码</font>**<font style="color:#1f2329;">：标准的正弦-余弦位置编码是固定的，不可学习。它⽆法适应特定任务或数据的变化，因此在某些特定应⽤中，可能⽆法提供最优的位置信息。</font>
+ **<font style="color:#ED740C;">有限的序列长度</font>**<font style="color:#1f2329;">：正弦-余弦位置编码对序列⻓度有⼀定限制。在处理⾮常⻓的序列时，固定位置编码可能⽆法充分表达序列的全貌。</font>**<font style="color:#74B602;">不具备外推的性质</font>**<font style="color:rgb(25, 27, 31);">。长度在预设定好之后就被固定了。</font>
+ **<font style="color:#ED740C;">位置编码的线性组合</font>**<font style="color:#1f2329;">：位置编码与词嵌⼊的线性组合可能导致信息丢失，因为位置编码的信息可能被嵌⼊中的信息所覆盖，从⽽影响模型对位置信息的敏感性。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
# 初始化
self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)

# 计算
position_embeddings = self.position_embeddings(position_ids)
embeddings += position_embeddings
```

```python
import torch
import math

def manual_sinusoidal_encoding(max_len: int, d_model: int) -> torch.Tensor:
    """
    手动实现 Transformer 正弦位置编码
    
    参数：
        max_len: 最大序列长度
        d_model: 模型维度（需为偶数）
    
    返回：
        pe: 位置编码矩阵 [max_len, d_model]
    """
    if d_model % 2 != 0:
        raise ValueError("模型维度 d_model 必须是偶数")
    
    # 初始化位置编码矩阵
    pe = torch.zeros(max_len, d_model)
    
    # 生成位置序列 [max_len, 1]
    position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
    
    # 计算频率项 (分母部分)
    div_term = torch.exp(
        torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
    )
    
    # 正弦余弦交替填充
    pe[:, 0::2] = torch.sin(position * div_term)  # 偶数索引填充正弦
    pe[:, 1::2] = torch.cos(position * div_term)  # 奇数索引填充余弦
    
    return pe

# 测试验证
if __name__ == "__main__":
    # 参数设置
    max_len = 10  # 测试序列长度
    d_model = 4   # 测试模型维度
    
    # 生成编码
    pe = manual_sinusoidal_encoding(max_len, d_model)
    
    # 验证标准实现对照
    class StandardPositionalEncoding(torch.nn.Module):
        def __init__(self, d_model: int, max_len: int = 5000):
            super().__init__()
            pe = torch.zeros(max_len, d_model)
            position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
            div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
            pe[:, 0::2] = torch.sin(position * div_term)
            pe[:, 1::2] = torch.cos(position * div_term)
            self.register_buffer('pe', pe)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.pe[:x.size(0)]
    
    # 对比两种实现
    standard_pe = StandardPositionalEncoding(d_model, max_len)(torch.zeros(max_len, d_model))
    
    print("手动实现结果：")
    print(pe)
    print("\n标准实现结果：")
    print(standard_pe)
    print("\n差异值：", torch.abs(pe - standard_pe).max().item())

```

# 旋转位置编码RoPE (LLAMA)<font style="color:#D22D8D;"></font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">论文《</font>[Roformer: Enhanced Transformer With Rotray Position Embedding](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2104.09864.pdf)<font style="color:rgb(25, 27, 31);">》 提出的一种能够将相对位置信息依赖集成到 self-attention 中并提升</font>[<font style="color:rgb(9, 64, 142);">transformer 架构</font>](https://zhida.zhihu.com/search?content_id=231932826&content_type=Article&match_order=1&q=+transformer+%E6%9E%B6%E6%9E%84&zhida_source=entity)<font style="color:rgb(25, 27, 31);">性能的位置编码方式</font>

**<font style="color:#ED740C;">RoPE通过将位置编码嵌⼊到旋转变换中</font>**<font style="color:#1f2329;">，使得位置之间的相对关系能够直接影响最终的Attention权重。具体⽽⾔，RoPE通过旋转矩阵来对每个位置的编码进⾏变换，使得相对位置 </font>_<font style="color:#1f2329;">m </font>_<font style="color:#1f2329;">−</font>_<font style="color:#1f2329;">n</font>_<font style="color:#1f2329;">在计算注意⼒时⾃然地被考虑进来。位置编码形式为： </font><font style="color:#D22D8D;"></font>

_<font style="color:#1f2329;">f </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">q</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">)=</font>_<font style="color:#1f2329;">q </font>_<font style="color:#1f2329;">⋅</font>_<font style="color:#1f2329;">e</font>_<sup>_<font style="color:#1f2329;">imθ   </font>_</sup>

_<font style="color:#1f2329;">f </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">k</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">n</font>_<font style="color:#1f2329;">)=</font>_<font style="color:#1f2329;">k </font>_<font style="color:#1f2329;">⋅</font>_<font style="color:#1f2329;">e</font>_<sup>_<font style="color:#1f2329;">inθ </font>_</sup>

:::

RoPE通过旋转变换将位置信息嵌⼊到向量中，使得相对位置在编码中得以体现。这种旋转变换基于每个位置的相对差异，⽽不是绝对位置。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738899779423-9d3a6461-9426-4901-be11-d53e4f841047.png)

<font style="color:rgb(25, 27, 31);">理想情况下，一个好的位置编码应该满足以下条件：</font>

+ <font style="color:rgb(25, 27, 31);">每个位置输出一个唯一的编码</font>
+ <font style="color:rgb(25, 27, 31);">具备良好的外推性</font>
+ <font style="color:rgb(25, 27, 31);">任何位置之间的相对距离在不同长度的句子中应该是一致的</font>

**<font style="color:#74B602;">RoPE正是为了解决上面三个问题而提出的。</font>**

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">RoPE 的 self-attention 操作的流程：</font>**

1. <font style="color:rgb(25, 27, 31);">对于 token 序列中的每个词嵌入向量，首先计算其对应的 query 和 key 向量，</font>
2. <font style="color:rgb(25, 27, 31);">对每个 token 位置都计算对应的旋转位置编码，</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740542197426-86059a22-cf87-43aa-b161-67e5dbb32ce7.png)

3. <font style="color:rgb(25, 27, 31);">对每个 token 位置的 query 和 key 向量的元素按照 </font>**<font style="color:#74B602;">两两一组</font>**<font style="color:rgb(25, 27, 31);"> 应用旋转变换，</font>
4. <font style="color:rgb(25, 27, 31);">再计算 query 和 key 之间的内积得到 self-attention 的计算结果。</font>

**计算示例：**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">假设有一句话“我们生活在南京”，其中 x = “南” 为我们需要处理的词。m是x在sequence中的位置(在本句中为6)，假设</font>**<font style="color:#601BDE;"> x 的 embedding 维度为 512</font>**<font style="color:rgb(25, 27, 31);">，我们可以通过以下公式计算 θ 值(其中i 是 embedding 中的维度位置，d 是 embedding 的维度数)：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203501008-133d5331-3c21-4f58-b527-d03f0cef9d84.png)

<font style="color:rgb(25, 27, 31);">接下来，我们对词向量的每两维进行相同角度的旋转。例如，x[0] 和 x[1] 乘以下矩阵：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203275567-d2e7f669-afbe-4747-9d73-1963378cca5b.png)

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1742439184052-be51810a-7faa-4a82-aa64-7a5489b3e211.jpeg)

:::color5
**<font style="color:#601BDE;">1.作用</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:#ED740C;">引入相对位置信息</font>**：<font style="color:#1f2329;"> RoPE通过这种设计使得模型不仅保留了绝对位置信息，还能直接学习到位置之间的相对距离和关系。这对于捕捉⻓程依赖和相对位置信息尤其重要。</font>
2. **<font style="color:#ED740C;">增强模型的表示能力</font>**：<font style="color:#1f2329;">RoPE通过旋转矩阵对每个位置进⾏编码，使得向量的</font>**<font style="color:#74B602;">旋转角度反映了位置之间的相对关系</font>**<font style="color:#1f2329;">。这样可以使模型在计算注意⼒时⾃然地包含相对位置的信息，从⽽提升模型对序列中元素相对位置关系的敏感度和处理能⼒。</font>
3. **<font style="color:#ED740C;">提升模型泛化能力</font>**：<font style="color:#1f2329;">RoPE通过对位置编码进⾏旋转变换，使得位置之间的关系可以被直接学习和调整。</font>**<font style="color:#74B602;">旋转编码的这种设计使得模型能够更好地泛化到不同⻓度和不同类型的序列</font>**<font style="color:#1f2329;">，因为它能够直接捕捉和利⽤位置之间的相对关系。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

| **<font style="color:#1f2329;">特性</font>** | **<font style="color:#1f2329;">RoPE</font>****<font style="color:#1f2329;">旋转位置编码</font>** | **<font style="color:#1f2329;">绝对位置编码</font>** |
| --- | --- | --- |
| **<font style="color:black;"></font>**<br/>**<font style="color:#1f2329;">位置信息捕捉</font>** | <font style="color:#1f2329;">捕捉token之间的</font>**<font style="color:#2ea121;">相对位置</font>**<font style="color:#1f2329;">关系</font> | <font style="color:#1f2329;">仅捕捉每个token的</font>**<font style="color:#2ea121;">绝对位置</font>** |
| **<font style="color:black;"></font>**<br/>**<font style="color:#1f2329;">序列⻓度适应性</font>** | <font style="color:#1f2329;">在处理⻓序列时表现优越</font><font style="color:#1f2329;">，尤</font><font style="color:#1f2329;">其是⻓依赖关系</font> | <font style="color:#1f2329;">对⻓序列不够有效</font><font style="color:#1f2329;">，位置信息</font><font style="color:#1f2329;">可能被稀释</font> |
| **<font style="color:black;"></font>**<br/>**<font style="color:#1f2329;">数学操作</font>** | <font style="color:#1f2329;">通过</font>**<font style="color:#2ea121;">旋转操作</font>**<font style="color:#1f2329;">，引⼊位置信息的相位偏移</font> | <font style="color:#1f2329;">通过直接</font>**<font style="color:#2ea121;">嵌⼊</font>****<font style="color:#1f2329;">正弦-余弦函数</font>** |
| **<font style="color:black;"></font>**<br/>**<font style="color:#1f2329;">注意⼒机制的效果</font>** | <font style="color:#1f2329;">能够⾃然处理注意⼒机制中的</font><font style="color:#1f2329;">相对位置信息</font> | <font style="color:#1f2329;">⽆法直接捕捉相对位置</font><font style="color:#1f2329;">，适⽤</font><font style="color:#1f2329;">于较短序列</font> |
| **<font style="color:black;"></font>**<br/>**<font style="color:#1f2329;">应⽤场景</font>** | <font style="color:#1f2329;">适⽤于⻓序列任务</font><font style="color:#1f2329;">，如⻓⽂本</font><font style="color:#1f2329;">⽣成、⻓依赖建模</font> | <font style="color:#1f2329;">更适合短序列或⽆复杂相对依</font><font style="color:#1f2329;">赖的场景</font> |
| **<font style="color:black;"></font>**<br/>**<font style="color:#1f2329;">计算复杂性</font>** | <font style="color:#1f2329;">更复杂</font><font style="color:#1f2329;">，涉及复数的旋转计算</font> | <font style="color:#1f2329;">计算较简单</font><font style="color:#1f2329;">，直接添加到嵌⼊</font><font style="color:#1f2329;">向量中</font> |


:::color5
**<font style="color:#601BDE;">2.实现</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
# 生成旋转矩阵
def precompute_freqs_cis(dim: int, seq_len: int, theta: float = 10000.0):
    # 计算词向量元素两两分组之后，每组元素对应的旋转角度\theta_i
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))
    # 生成 token 序列索引 t = [0, 1,..., seq_len-1]
    t = torch.arange(seq_len, device=freqs.device)
    # freqs.shape = [seq_len, dim // 2] 
    freqs = torch.outer(t, freqs).float()  # 计算m * \theta

    # 计算结果是个复数向量
    # 假设 freqs = [x, y]
    # 则 freqs_cis = [cos(x) + sin(x)i, cos(y) + sin(y)i]
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs) 
    return freqs_cis

# 旋转位置编码计算
def apply_rotary_emb(
    xq: torch.Tensor,
    xk: torch.Tensor,
    freqs_cis: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
    # xq.shape = [batch_size, seq_len, dim]
    # xq_.shape = [batch_size, seq_len, dim // 2, 2]
    xq_ = xq.float().reshape(*xq.shape[:-1], -1, 2)
    xk_ = xk.float().reshape(*xk.shape[:-1], -1, 2)
    
    # 转为复数域
    xq_ = torch.view_as_complex(xq_)
    xk_ = torch.view_as_complex(xk_)
    
    # 应用旋转操作，然后将结果转回实数域
    # xq_out.shape = [batch_size, seq_len, dim]
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(2)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(2)
    return xq_out.type_as(xq), xk_out.type_as(xk)

class Attention(nn.Module):
    def __init__(self, args: ModelArgs):
        super().__init__()

        self.wq = Linear(...)
        self.wk = Linear(...)
        self.wv = Linear(...)
        
        self.freqs_cis = precompute_freqs_cis(dim, max_seq_len * 2)

    def forward(self, x: torch.Tensor):
        bsz, seqlen, _ = x.shape
        xq, xk, xv = self.wq(x), self.wk(x), self.wv(x)

        xq = xq.view(batch_size, seq_len, dim)
        xk = xk.view(batch_size, seq_len, dim)
        xv = xv.view(batch_size, seq_len, dim)

        # attention 操作之前，应用旋转位置编码
        xq, xk = apply_rotary_emb(xq, xk, freqs_cis=freqs_cis)
        
        # scores.shape = (bs, seqlen, seqlen)
        scores = torch.matmul(xq, xk.transpose(1, 2)) / math.sqrt(dim)
        scores = F.softmax(scores.float(), dim=-1)
        output = torch.matmul(scores, xv)  # (batch_size, seq_len, dim)
```



## <font style="color:rgb(1, 1, 1);">为什么使用旋转位置编码？</font>
<font style="color:rgb(51, 51, 51);">Transformer模型使用旋转位置编码（Positional Encoding）的主要原因是其架构本身并不具备处理序列数据中位置信息的能力。以下是具体的原因：</font>

1. **自注意力机制的特性**：Transformer利用自注意力机制（Self-Attention）来处理输入序列中的每个元素。在自注意力中，所有输入的元素都是并行处理的，这意味着网络无法通过序列的自然顺序（如RNN中的时间步）来理解元素之间的位置信息。
2. **引入位置信息**：为了使模型能够感知序列中各个位置的关系，Transformer引入了位置编码。位置编码通过将每个位置的编码向量与输入的词向量相加，帮助模型意识到输入的顺序。
3. **旋转位置编码**：旋转位置编码（通常采用正弦和余弦函数）具有良好的数学性质。它允许模型能够学习到不同位置之间的相对关系。特别是，正弦和余弦函数的频率和相位变化可以为不同的位置编码提供丰富的信息，让模型更加有效地捕捉序列中的结构。
4. **选择的灵活性**：使用旋转位置编码，模型可以在预测过程中灵活处理不同长度的输入序列，且无论输入序列的实际长度如何，模型都能有效地生成相应位置的编码。

## <font style="color:rgb(53, 53, 53);">LLaMA 模型为什么要用旋转位置编码？</font>
<font style="color:rgb(51, 51, 51);">LLaMA 模型使用旋转位置编码（Rotary Positional Embedding, RoPE）是为了在Transformer模型中有效地引入位置信息，同时保持模型的灵活性和表达能力。</font>

1. **保持序列关系**：旋转位置编码通过将位置信息嵌入到注意力机制中，使得模型能够识别序列中元素之间的位置关系。这在自然语言处理任务中尤为重要，因为词汇的顺序往往影响句子的意义。
2. **平滑的扩展性**：RoPE 允许模型处理比训练时更长的序列。这是因为它不会将位置编码限制在一个固定的范围内，而是通过旋转计算得到可扩展的编码方式。
3. **简化计算**：RoPE 的实现相对简单，可以直接与标准的注意力机制结合，而不需要额外的复杂计算，使得模型在推理过程中更为高效。
4. **性能增强**：一些研究表明，旋转位置编码在某些任务中能够提供更好的性能，以及与传统的位置编码相比更好的泛化能力。

## <font style="color:rgb(53, 53, 53);">针对长序列，如何在Transformer中实现有效的位置编码？</font>
:::color3
<font style="color:#000000;">在Transformer中，由于其自注意力机制的特点，序列中的位置编码（Positional Encoding）是一个重要的部分用于向模型提供序列中元素的位置信息。</font>**<font style="color:#74B602;">对于长序列的处理，传统的位置编码方式（如正弦和余弦函数位置编码）可能会存在一些限制</font>**<font style="color:#000000;">。以下是一些针对长序列实现有效位置编码的方法：</font>

:::

1. **<font style="color:#ED740C;">可学习的位置编码</font>**<font style="color:#000000;">：  
</font><font style="color:#000000;">使用</font>**<font style="color:#74B602;">可学习的参数代替固定的正弦和余弦位置编码</font>**<font style="color:#000000;">。这种方法通过在训练过程中自动学习到最优位置编码，能够更好地适应长序列的特定上下文。</font>
2. **<font style="color:#ED740C;">相对位置编码</font>**<font style="color:#000000;">：  
</font><font style="color:#000000;">相对位置编码可以解决绝对位置编码在长序列中的一些局限性。相对位置编码关注的是</font>**<font style="color:#74B602;">元素之间的相对距离</font>**<font style="color:#000000;">，而不是绝对位置，这样可以更好地捕捉长距离依赖。</font>
3. **<font style="color:#ED740C;">层次化位置编码</font>**<font style="color:#000000;">：  
</font><font style="color:#000000;">通过构建层次化的位置编码结构，可以有效地处理长序列。这种方法将长度信息划分成更小的单位，使模型可以在局部上下文中学习。</font>
4. **<font style="color:#ED740C;">Transformer的变体</font>**<font style="color:#000000;">：  
</font><font style="color:#000000;">一些改进的Transformer模型（例如Reformer、Longformer）采用了</font>**<font style="color:#74B602;">稀疏注意力机制</font>**<font style="color:#000000;">，能够处理更长的序列。它们通常会结合特定的位置信息处理方法，使得在长序列上的表现更佳。</font>
5. **<font style="color:#ED740C;">动态位置编码</font>**<font style="color:#000000;">：  
</font><font style="color:#000000;">根据输入序列的长度</font>**<font style="color:#74B602;">动态生成位置编码</font>**<font style="color:#000000;">，这种方法可以在模型推理过程中为每个输入序列创建新的位置编码，有效地适应不同长度的输入。</font>
6. **<font style="color:#ED740C;">位置标记</font>**<font style="color:#000000;">：  
</font><font style="color:#000000;">使用位置索引作为输入的一部分，将其作为额外的特征输入，每个时间步都带有一个对应的位置信息。这可以帮助模型直接学习位置与内容之间的关系。</font>

<font style="color:#000000;"></font>

# <font style="color:rgb(25, 27, 31);">PI(Position Interpolation)位置线性内插</font><font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">位置线性内插（PI）是一种扩展Transformer模型上下文窗口的技术，核心思想是通过</font>**<font style="color:rgb(51, 51, 51);">线性缩放位置索引</font>**<font style="color:rgb(51, 51, 51);">，使模型能够</font>**<font style="color:#ED740C;">处理超出训练长度的序列</font>**<font style="color:rgb(51, 51, 51);">。其数学本质是保持位置编码的</font>**<font style="color:rgb(51, 51, 51);">相对顺序关系</font>**<font style="color:rgb(51, 51, 51);">，同时将超出训练长度的位置映射到原始编码范围内。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">关键公式</font>**<font style="color:rgb(51, 51, 51);">：</font>  
<font style="color:rgb(51, 51, 51);"> 对于目标长度 </font><font style="color:rgb(51, 51, 51);">L</font><font style="color:rgb(51, 51, 51);">和原始最大长度 </font><font style="color:rgb(51, 51, 51);">N</font><font style="color:rgb(51, 51, 51);">（</font><font style="color:rgb(51, 51, 51);">L>N</font><font style="color:rgb(51, 51, 51);">），调整后的位置索引为：</font>  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740556230793-429b29df-42b6-403c-9690-cfbf99014759.png)  
<font style="color:rgb(51, 51, 51);"> 其中 </font><font style="color:rgb(51, 51, 51);">i∈[0,L−1]</font><font style="color:rgb(51, 51, 51);">是实际位置，</font><font style="color:rgb(51, 51, 51);">i′∈[0,N−1]</font><font style="color:rgb(51, 51, 51);">是缩放后的位置。</font>

**<font style="color:rgb(51, 51, 51);">计算步骤：</font>**

1. **原始旋转位置编码计算**：

```python
def compute_rope(pos, dim, base=10000):
    theta = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
    pos_theta = pos * theta
    return torch.cat([pos_theta.cos(), pos_theta.sin()], dim=-1)
```

2. **位置缩放**：<font style="color:#D22D8D;"></font>

```python
def scale_position(L, N, current_length):
    scale_factor = N / current_length
    return torch.arange(0, current_length) * scale_factor
```

3. **应用缩放后的位置编码**：

```python
def apply_pi_rope(q, k, L, max_train_length=2048):
    scaled_pos = scale_position(L, max_train_length, L)
    q_rot = compute_rope(scaled_pos, q.size(-1))
    k_rot = compute_rope(scaled_pos, k.size(-1))
    return q * q_rot, k * k_rot
```

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">支持8-32倍长度扩展（如从2K→32K）</font>
+ <font style="color:rgb(51, 51, 51);">几乎不损失原始长度性能（<1%精度下降）</font>
+ <font style="color:rgb(51, 51, 51);">无需微调即可应用</font>

**<font style="color:rgb(51, 51, 51);">局限</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">超长距离位置分辨率降低</font>
+ <font style="color:rgb(51, 51, 51);">对绝对位置敏感的任务效果下降</font>
+ <font style="color:rgb(51, 51, 51);">需要重新计算注意力矩阵</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **场景** | **典型应用** | **扩展效果** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">长文本生成</font> | <font style="color:rgb(51, 51, 51);">小说续写、法律文书生成</font> | <font style="color:rgb(51, 51, 51);">2K→32K</font> |
| <font style="color:rgb(51, 51, 51);">长视频理解</font> | <font style="color:rgb(51, 51, 51);">视频时序分析</font> | <font style="color:rgb(51, 51, 51);">1K→8K</font> |
| <font style="color:rgb(51, 51, 51);">科学计算</font> | <font style="color:rgb(51, 51, 51);">蛋白质序列分析</font> | <font style="color:rgb(51, 51, 51);">4K→64K</font> |
| <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">大型项目代码理解</font> | <font style="color:rgb(51, 51, 51);">8K→128K</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **动态温度缩放**：

```python
def dynamic_scaling(L, N, alpha=0.5):
    return (N ** alpha) / (L ** (alpha-1))
```

2. **分段线性插值**：

```python
def piecewise_scale(L, N, seg_points=[0.25, 0.5, 0.75]):
    scale_factors = [1.0] + [N/(L*p) for p in seg_points]
    return torch.where(condition, scale1, scale2)
```

3. **混合位置编码**：

```python
class HybridPosition(nn.Module):
    def __init__(self, base_enc, pi_enc):
        self.base = base_enc
        self.pi = pi_enc

    def forward(self, x, L):
        if L <= self.base.max_len:
            return self.base(x)
        else:
            return self.pi(x, L)
```

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
import torch
import torch.nn as nn
import math

class RoPEWithPI(nn.Module):
    def __init__(self, dim, max_train_len=2048, base=10000):
        super().__init__()
        self.dim = dim
        self.base = base
        self.max_train_len = max_train_len
        self.register_buffer('inv_freq', 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim)))

    def _compute_rope(self, positions):
        theta = positions.unsqueeze(-1) * self.inv_freq
        cos = torch.cos(theta)
        sin = torch.sin(theta)
        return torch.cat([cos, sin], dim=-1)

    def forward(self, q, k, seq_len):
        if seq_len > self.max_train_len:
            scale = self.max_train_len / seq_len
            positions = torch.linspace(0, self.max_train_len, seq_len) * scale
        else:
            positions = torch.arange(seq_len, device=q.device)
        
        rope = self._compute_rope(positions)
        rope_dim = rope.size(-1)
        
        q_rot = q[..., :rope_dim] * rope
        k_rot = k[..., :rope_dim] * rope
        return torch.cat([q_rot, q[..., rope_dim:]], dim=-1), \
               torch.cat([k_rot, k[..., rope_dim:]], dim=-1)

# 使用示例
dim = 128
seq_len = 8192  # 超过训练长度
model = RoPEWithPI(dim)

q = torch.randn(1, seq_len, dim)
k = torch.randn(1, seq_len, dim)
q_pi, k_pi = model(q, k, seq_len)

```



# <font style="color:rgb(25, 27, 31);">NTK-Aware Scaled RoPE(非线性内插)</font><font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">NTK-Aware Scaled RoPE</font>**<font style="color:rgb(51, 51, 51);"> 是对 Rotary Position Embedding (RoPE) 的改进，旨在提升模型处理长序列时的</font>**<font style="color:#ED740C;">外推能力</font>**<font style="color:rgb(51, 51, 51);">。其核心思想基于 </font>**<font style="color:rgb(51, 51, 51);">Neural Tangent Kernel (NTK)</font>**<font style="color:rgb(51, 51, 51);"> 理论，通过对 RoPE 的频率基进行动态缩放，平衡高频和低频位置信息的分布，缓解长序列外推时的性能下降问题。</font>

:::

**<font style="color:rgb(51, 51, 51);">RoPE 回顾</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">	RoPE 将位置编码通过旋转矩阵融入注意力计算中。对于位置 m和维度 i，旋转角度为 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740557264780-03896b42-c6b8-40b3-af77-a78f6c40e330.png)<font style="color:rgb(51, 51, 51);">，生成复数域的旋转矩阵。这使得内积 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740557291931-41caf91a-eed4-4631-a64f-3f1cb5d33e3d.png)<font style="color:rgb(51, 51, 51);">能隐式编码相对位置 ∣m−n∣。</font>

**<font style="color:rgb(51, 51, 51);">NTK 理论启发</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">	NTK 描述了无限宽神经网络的训练动态。在长序列外推时，RoPE 的高频分量（对应大 i</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">）衰减过快，导致位置区分度下降。NTK-Aware 方法通过调整频率基，使高频分量衰减更缓慢，从而保留更多位置信息。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">步骤 1：调整频率基</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">	原始 RoPE 的基为 base=10000。NTK-Aware 方法将其缩放为更大的值 basenew=base×s，其中 s是缩放因子，通常与序列长度相关。</font>

**<font style="color:rgb(51, 51, 51);">步骤 2：计算缩放后的角度</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">	对于维度 i</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">，新的旋转角度为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740557328647-d264f1ab-1b70-4ecf-9a40-ea5f0768c983.png)

<font style="color:rgb(51, 51, 51);">这等效于降低频率，避免高频分量过早衰减。</font>

**<font style="color:rgb(51, 51, 51);">步骤 3：动态调整缩放因子</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">推理时，根据当前序列长度 L和训练时的最大长度 Ltrain，动态计算 s</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740557351678-01031aba-925c-486f-9934-3c4a0e403c2a.png)

<font style="color:rgb(51, 51, 51);">其中 α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);"> 是控制缩放强度的超参数（通常取 α=d/(d−2)，d为头维度）。</font>

**<font style="color:rgb(51, 51, 51);">步骤 4：应用旋转矩阵</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">使用调整后的 θi′生成旋转矩阵 Rθ′,m，其余计算与原始 RoPE 一致。</font>

:::color5
**<font style="color:#601BDE;">2.低频内插，高频外推</font>**

:::

<font style="color:rgb(25, 27, 31);">回忆RoPE，它的构造基础是Sinusoidal位置编码，可以改写为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451218541-e12e55bf-8f85-4f32-ac12-c7df546cd60e.png)          （1）

<font style="color:rgb(25, 27, 31);">作者基于NTK（Neural Tangent Kernel）相关结果的直觉，推导了NTK-aware Scaled RoPE。假设要扩大k倍范围表示，根据NTK-Aware Scaled RoPE，高频外推、低频内插。</font>

+ **<font style="color:rgb(25, 27, 31);">低频内插</font>**<font style="color:rgb(25, 27, 31);">：公式（1）最低频是 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451297628-9908b879-f2b9-47dc-b190-fa3778975f03.png)<font style="color:rgb(25, 27, 31);">引入参数 λ 变为</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451305395-225fd782-2808-471b-8081-f29df3631478.png)**<font style="color:#74B602;">让他与内插一致</font>**<font style="color:rgb(25, 27, 31);">，即：</font>

<font style="color:rgb(25, 27, 31);">  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451313232-1ade5f7d-aca4-4771-959a-8bb1df33c0f2.png)

<font style="color:rgb(25, 27, 31);">那么得到 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451344664-6df285c4-9a6d-4a80-8ec9-fc05115c0ede.png)<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">高频外推</font>**<font style="color:rgb(25, 27, 31);">：至于最高频是 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451349848-f77a73f0-c4fe-4cb0-a1e6-9f3ab1a1b238.png)<font style="color:rgb(25, 27, 31);"> 项，引入 λ 变为 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451354965-3cc2d3e8-a3ca-4ebc-8eec-4d8e06d05efb.png)<font style="color:rgb(25, 27, 31);">，由于d很大， λ→1 ，所以它还是接近于初始值</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742451349848-f77a73f0-c4fe-4cb0-a1e6-9f3ab1a1b238.png)<font style="color:rgb(25, 27, 31);"> ，</font>**<font style="color:#74B602;">等价于外推。</font>**

<font style="color:rgb(25, 27, 31);">所以这样的方案简单巧妙地将外推和内插结合了起来。另外，由于d比较大，因此 k</font><sup><font style="color:rgb(25, 27, 31);">2/(d−2)</font></sup><font style="color:rgb(25, 27, 31);"> 跟 k</font><sup><font style="color:rgb(25, 27, 31);">2/d</font></sup><font style="color:rgb(25, 27, 31);"> 差别不大，所以它跟前面基于进制思想提出的解 k</font><sup><font style="color:rgb(25, 27, 31);">2/d</font></sup><font style="color:rgb(25, 27, 31);"> 是基本一致的。还有，从提出者这个思想来看，</font>**<font style="color:rgb(25, 27, 31);">任意能实现“高频外推、低频内插”的方案都是可以的，并非只有上述引入λ的方案</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">无需重训练</font>**<font style="color:rgb(51, 51, 51);">：直接应用于预训练模型，提升长序列外推能力。</font>
+ **<font style="color:rgb(51, 51, 51);">计算高效</font>**<font style="color:rgb(51, 51, 51);">：仅需修改频率基，几乎不增加计算量。</font>
+ **<font style="color:rgb(51, 51, 51);">兼容性强</font>**<font style="color:rgb(51, 51, 51);">：适用于所有基于 RoPE 的模型（如 LLaMA、GPT-NeoX）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">超参数敏感</font>**<font style="color:rgb(51, 51, 51);">：缩放因子</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">s</font>_<font style="color:rgb(51, 51, 51);">s</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">和</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">需要根据任务调整。</font>
+ **<font style="color:rgb(51, 51, 51);">理论依赖</font>**<font style="color:rgb(51, 51, 51);">：依赖 NTK 假设，可能在某些模型架构下不成立。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">长文本处理</font>**<font style="color:rgb(51, 51, 51);">：文档摘要、长对话生成、代码生成。</font>
+ **<font style="color:rgb(51, 51, 51);">资源受限推理</font>**<font style="color:rgb(51, 51, 51);">：当无法微调模型时，快速扩展上下文窗口。</font>
+ **<font style="color:rgb(51, 51, 51);">多尺度输入</font>**<font style="color:rgb(51, 51, 51);">：输入长度动态变化的场景（如检索增强生成）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">动态缩放</font>**<font style="color:rgb(51, 51, 51);">：根据输入长度自适应调整</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">s</font>_<font style="color:rgb(51, 51, 51);">s</font>_<font style="color:rgb(51, 51, 51);">，避免固定缩放带来的次优解。</font>
+ **<font style="color:rgb(51, 51, 51);">混合频率基</font>**<font style="color:rgb(51, 51, 51);">：对不同注意力头使用不同的缩放策略，增强多样性。</font>
+ **<font style="color:rgb(51, 51, 51);">训练时优化</font>**<font style="color:rgb(51, 51, 51);">：在预训练阶段引入多尺度位置编码，提升模型适应性。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
import torch
import math

def apply_ntk_scaled_rope(q, k, L_train=2048, alpha=1.0):
    """
    q, k: (batch_size, num_heads, seq_len, head_dim)
    L_train: 训练时的最大长度
    alpha: 缩放强度，默认基于头维度自动计算
    """
    batch, heads, seq_len, dim = q.shape
    device = q.device
    
    # 计算缩放因子
    L = seq_len
    s = (L / L_train) ** alpha
    
    # 调整后的频率基
    base = 10000.0
    base_new = base * s
    
    # 生成theta
    theta = 1.0 / (base_new ** (torch.arange(0, dim, 2, device=device).float() / dim))
    
    # 位置索引
    m = torch.arange(seq_len, device=device).float()
    
    # 构建旋转矩阵
    m_theta = torch.einsum('i,j->ij', m, theta)
    cos = torch.cos(m_theta)
    sin = torch.sin(m_theta)
    
    # 旋转操作
    q_real = q[..., 0::2]
    q_imag = q[..., 1::2]
    q_rot = torch.cat([q_real * cos - q_imag * sin, q_real * sin + q_imag * cos], dim=-1)
    
    k_real = k[..., 0::2]
    k_imag = k[..., 1::2]
    k_rot = torch.cat([k_real * cos - k_imag * sin, k_real * sin + k_imag * cos], dim=-1)
    
    return q_rot, k_rot

```



# ALiBi<font style="color:rgb(51, 51, 51);">（Attention with Linear Biases）线性偏差注意</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ALiBi（</font>**<font style="color:rgb(51, 51, 51);">Attention with Linear Biases</font>**<font style="color:rgb(51, 51, 51);">）是一种改进的Transformer位置编码方法，旨在解决传统位置编码（如绝对位置编码或旋转位置编码）在处理</font>**<font style="color:rgb(51, 51, 51);">长序列外推</font>**<font style="color:rgb(51, 51, 51);">（Extrapolation）时的局限性。其核心思想是通过在注意力计算中引入</font>**<font style="color:rgb(51, 51, 51);">线性偏置项</font>**<font style="color:rgb(51, 51, 51);">，显式建模相对位置关系，无需显式的位置嵌入</font>

:::

+ **关键思想**：  
对于每个注意力头，在计算查询（Query）和键（Key）的点积后，添加一个与相对位置成反比的线性偏置项。距离越远的键（Key）会被施加更大的负偏置，从而降低其注意力权重。
+ **外推能力**：  
通过简单的线性衰减，模型在训练时未见过的更长序列上表现更好（例如，训练时使用512长度，推理时扩展到2048）。

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**标准注意力计算**  
输入序列的注意力分数矩阵为：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740556715611-49c76d4e-474f-4c0c-b435-15d53509d288.png)

其中 Q,K,V 是查询、键、值矩阵，B__是ALiBi的偏置矩阵。

1. **偏置矩阵 B**_****_**的构造**
    - <font style="color:rgb(51, 51, 51);">对于每个查询位置 i</font>_<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);"> 和键位置 j</font>_<font style="color:rgb(51, 51, 51);">j</font>_<font style="color:rgb(51, 51, 51);">，定义相对位置偏移为 ∣i−j∣。</font>
    - <font style="color:rgb(51, 51, 51);">偏置项为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740556736653-0875f9ce-4fdf-42a5-839a-1086076fa142.png)

<font style="color:rgb(51, 51, 51);">其中 m是与注意力头相关的斜率（Slope）系数，不同头使用不同的 m</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>

2. **斜率 ****m**_**m**_** 的设定**
    - <font style="color:rgb(51, 51, 51);">对于 n</font>_<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);"> 个注意力头，斜率按几何级数分配。例如，8个头的 m值可能为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740556794808-162f2185-00dd-4dd7-a5cc-19c9a58c656b.png)

    - <font style="color:rgb(51, 51, 51);">公式化表示为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740556809890-670ae273-d50c-46ae-8d73-b37dd10c4f21.png)

3. **计算流程**
    - <font style="color:rgb(51, 51, 51);">计算标准点积注意力分数 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740556824393-783aa83f-88b3-4e36-8a6f-b8a41f88415b.png)
    - <font style="color:rgb(51, 51, 51);">生成偏置矩阵 B</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">，并添加到注意力分数中。</font>
    - <font style="color:rgb(51, 51, 51);">应用Softmax和加权求和得到输出。</font>  


:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 更强的外推能力，适合超长序列推理</font> | <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 对某些需要精确位置建模的任务（如机器翻译）可能略逊于旋转位置编码（RoPE）</font> |
| <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 无需位置嵌入参数，节省显存</font> | <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 偏置斜率</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">m</font>_<font style="color:rgb(51, 51, 51);">m</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">需要人工设计或调参</font> |
| <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 计算高效，仅增加少量计算量</font> | <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 对局部窗口内的注意力模式支持有限</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(51, 51, 51);">长文本处理</font>**<font style="color:rgb(51, 51, 51);">：文档摘要、代码生成、对话系统（如ChatGPT）。</font>
2. **<font style="color:rgb(51, 51, 51);">科学计算</font>**<font style="color:rgb(51, 51, 51);">：处理长序列的数值预测（如基因组、气象数据）。</font>
3. **<font style="color:rgb(51, 51, 51);">资源受限场景</font>**<font style="color:rgb(51, 51, 51);">：无需存储位置嵌入参数，适合边缘设备部署。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(51, 51, 51);">动态斜率调整</font>**<font style="color:rgb(51, 51, 51);">：根据输入数据动态学习</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">m</font>_<font style="color:rgb(51, 51, 51);">m</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">值（如引入可学习参数）。</font>
2. **<font style="color:rgb(51, 51, 51);">混合位置编码</font>**<font style="color:rgb(51, 51, 51);">：与旋转位置编码（RoPE）结合，平衡局部和全局注意力。</font>
3. **<font style="color:rgb(51, 51, 51);">层级偏置</font>**<font style="color:rgb(51, 51, 51);">：对不同层使用不同斜率，增强模型多样性。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
import torch
import torch.nn as nn

def get_alibi_biases(num_heads, max_seq_len):
    slopes = torch.tensor([1 / (2 ** (8 / i)) for i in range(1, num_heads + 1)])  # 斜率计算
    biases = torch.zeros(num_heads, max_seq_len, max_seq_len)
    for h in range(num_heads):
        for i in range(max_seq_len):
            for j in range(max_seq_len):
                biases[h, i, j] = -slopes[h] * abs(i - j)
    return biases

class ALiBiAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.qkv = nn.Linear(embed_dim, 3 * embed_dim)
        self.register_buffer('alibi_biases', get_alibi_biases(num_heads, 2048))  # 预生成偏置矩阵

    def forward(self, x):
        B, T, C = x.shape
        qkv = self.qkv(x).reshape(B, T, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        attn_scores = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn_scores += self.alibi_biases[:, :T, :T].unsqueeze(0)  # 添加ALiBi偏置
        attn_weights = torch.softmax(attn_scores, dim=-1)
        return torch.matmul(attn_weights, v)

```



# YARN (<font style="color:rgb(51, 51, 51);">YetAnotherRopeExtension</font>)<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：YARN（YetAnotherRopeExtension）是一种</font>**<font style="color:#ED740C;">基于改进的相对位置编码（RoPE）机制来扩展上下文长度的方法</font>**<font style="color:rgb(51, 51, 51);">。RoPE机制最初用于Transformer模型中，通过引入相对位置信息，使得模型能够捕捉序列中的位置关系。YARN在此基础上进行了优化，通过动态扩展位置编码的能力，支持更长的上下文处理。</font>

:::

:::color5
**<font style="color:#601BDE;">1.YARN原理</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **相对位置编码扩展**：RoPE编码器原本用于编码固定长度的相对位置信息。YARN通过调整和扩展RoPE的编码方式，使其能够适应更长的序列长度。
2. **分段编码**：将长序列分割成多个较小的段落，每个段落独立进行RoPE编码，同时保持段落之间的位置信息关联。
3. **全局与局部结合**：在编码过程中，YARN同时考虑序列的局部和全局信息，确保在扩展上下文长度的同时，模型能够有效捕捉长距离依赖关系。<font style="color:#601BDE;"></font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**优点**

1. **计算效率高**：通过基于RoPE的相对位置编码，避免了传统的全注意力机制的O(n²)计算复杂度，**<font style="color:#74B602;">显著降低了计算量</font>**。
2. **支持长上下文**：YARN优化了位置编码的生成方式，**<font style="color:#74B602;">能够高效处理长序列</font>**，支持数万甚至数十万的上下文长度。
1. **与现有模型兼容**：YARN可以通过修改原有的RoPE编码层引入，具有良好的兼容性，容易集成到现有的模型架构中。

**缺点**

1. **实现复杂**：YARN需要对RoPE机制进行改进，实现相对复杂的编码扩展逻辑，增加了代码的复杂性和维护难度。
2. **实验验证不足**：目前关于YARN的公开资料较少，具体的性能和效果仍需通过实际实验进一步验证。

```python
import torch
import torch.nn as nn
import math

class YARN(nn.Module):
    def __init__(self, embed_dim, max_relative_length=1024):
        super(YARN, self).__init__()
        self.embed_dim = embed_dim
        self.max_relative_length = max_relative_length
        
        # 扩展RoPE参数
        self.inv_freq = 1.0 / (10000 ** (torch.arange(0, embed_dim, 2).float() / embed_dim))
        
    def forward(self, x, attention_mask=None):
        """
        前向传播
        :param x: 输入序列，形状为[batch_size, seq_len, embed_dim]
        :param attention_mask: 注意力掩码
        :return: 处理后的序列，形状为[batch_size, seq_len, embed_dim]
        """
        batch_size, seq_len = x.size()[:2]
        
        # 扩展相对位置编码
        pos = torch.arange(seq_len, device=x.device).type(torch.float32) + 1
        sin = torch.sin(pos * self.inv_freq).view(1, seq_len, self.embed_dim // 2)
        cos = torch.cos(pos * self.inv_freq).view(1, seq_len, self.embed_dim // 2)
        
        # 将位置编码与输入特征相乘
        x = x * torch.cat([sin, cos], dim=-1)
        
        # 处理注意力掩码
        if attention_mask is not None:
            x = x.masked_fill(attention_mask == 0, 0)
            
        return x

# 示例使用
embed_dim = 512
seq_len = 4096
batch_size = 32

yarn_layer = YARN(embed_dim=512)
x = torch.randn(batch_size, seq_len, embed_dim)
output = yarn_layer(x)

print("输入序列长度:", seq_len)
print("输出序列长度:", output.size(1))
```

# 


# 动态位置编码(EVA-CLIP)
# <font style="color:rgb(51, 51, 51);">2D-RoPE/M-RoPE(多维旋转位置编码)</font><font style="color:#D22D8D;"></font>
:::success
**背景**：传统的旋转位置嵌入只能捕捉**<font style="color:#74B602;">一维序列的位置信息</font>**，而 M-ROPE 通过将原始旋转嵌入分解为代表**<font style="color:#74B602;">时间、高度和宽度的三个部分</font>**，使得大规模语言模型能够同时捕捉和整合**<font style="color:#74B602;">一维文本序列、二维视觉图像以及三维视频</font>**的位置信息。这一创新赋予了语言模型强大的[多模态处理](https://zhida.zhihu.com/search?content_id=247994162&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%84%E7%90%86&zhida_source=entity)和推理能力，能够更好地理解和建模复杂的多模态数据。

:::

:::color3
**简介：**Qwen2-VL 在架构上的另一重要创新则是**多模态旋转为编码（M-RoPE）**，将原始旋转嵌入分解为代表**<font style="color:#ED740C;">时间、高度和宽度的三个部分</font>**，使得大规模语言模型能够同时捕捉和整合**<font style="color:#ED740C;">一维文本序列、二维视觉图像以及三维视频</font>**的位置信息。

**参考：**[从浅到深入门旋转位置编码](https://zhuanlan.zhihu.com/p/13023539180)  [Qwen2-VL技术解析（二）- M-ROPE](https://zhuanlan.zhihu.com/p/719388479)

:::

:::color5
**<font style="color:#601BDE;">1.RoPE回顾</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">ROPE 的关键在于通过</font>**<font style="color:rgb(25, 27, 31);">绝对位置编码</font>**<font style="color:rgb(25, 27, 31);">来实现</font>[**<font style="color:rgb(9, 64, 142);">相对位置编码</font>**](https://zhida.zhihu.com/search?content_id=247994162&content_type=Article&match_order=1&q=%E7%9B%B8%E5%AF%B9%E4%BD%8D%E7%BD%AE%E7%BC%96%E7%A0%81&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。具体来说，将位置编码表示为二维空间中的旋转操作。对于一个二维向量</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">x</font>`<font style="color:rgb(25, 27, 31);">，将其绕原点旋转</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">m</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">弧度后，可以表示为矩阵乘法</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">R(m) * x</font>`<font style="color:rgb(25, 27, 31);">，其中旋转矩阵</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">R(m)</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的形式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742199244453-63ce11e8-ffbf-4f11-8bde-61662c136778.png)

<font style="color:rgb(25, 27, 31);">这一变换保留了</font>**<font style="color:#601BDE;">原始向量的性质，但通过旋转引入了位置信息</font>**<font style="color:rgb(25, 27, 31);">。如果一个二维向量旋转了 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">m</font>`<font style="color:rgb(25, 27, 31);"> 弧度，另一个旋转了 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">n</font>`<font style="color:rgb(25, 27, 31);"> 弧度，那么这两个向量之间的夹角就是 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">|m - n|</font>`<font style="color:rgb(25, 27, 31);">。基于这样的思想，我们可以有效地引入</font>**<font style="color:rgb(25, 27, 31);">相对位置</font>**<font style="color:rgb(25, 27, 31);">的信息。</font>

:::color5
**<font style="color:#601BDE;">2.一维RoPE</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742438999217-a0a11c21-366f-4a9c-b59b-d901802b4cdd.png)

**<font style="color:rgb(25, 27, 31);">计算示例</font>**

<font style="color:rgb(25, 27, 31);">假设有一句话“我们生活在南京”，其中 x = “南” 为我们需要处理的词。m是x在sequence中的位置(在本句中为6)，假设</font>**<font style="color:#601BDE;"> x 的 embedding 维度为 512</font>**<font style="color:rgb(25, 27, 31);">，我们可以通过以下公式计算 θ 值(其中i 是 embedding 中的维度位置，d 是 embedding 的维度数)：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203501008-133d5331-3c21-4f58-b527-d03f0cef9d84.png)

<font style="color:rgb(25, 27, 31);">接下来，我们对词向量的每两维进行相同角度的旋转。例如，x[0] 和 x[1] 乘以下矩阵：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203275567-d2e7f669-afbe-4747-9d73-1963378cca5b.png)

<font style="color:rgb(25, 27, 31);">这种方法实际上是</font>**<font style="color:#74B602;">将 embedding 中的每两维一组去旋转 </font>****<font style="color:#74B602;">mθ</font>**<sub>**<font style="color:#74B602;">i</font>**</sub>**<font style="color:#74B602;"> 度</font>**<font style="color:rgb(25, 27, 31);">, 下图可以帮助更直观地理解该过程：</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1742439195190-6cdc1737-b3da-40af-8384-bc7b20299b4c.jpeg)

:::color5
**<font style="color:#601BDE;">2.二维RoPE</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">RoPE从1维扩展到2维一个简单的结论：针对一个位置</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">(x,y)</font><font style="color:rgb(25, 27, 31);"> ，</font>**<font style="color:rgb(25, 27, 31);">对维度为 </font>****<font style="color:rgb(25, 27, 31);">d</font>****<font style="color:rgb(25, 27, 31);"> 的</font>****<font style="color:#74B602;">输入向量分成两半，前一半向量用 </font>****<font style="color:#74B602;">x</font>****<font style="color:#74B602;"> 的一维RoPE矩阵( </font>****<font style="color:#74B602;">Rx</font>****<font style="color:#74B602;"> )处理，后一半向量用 </font>****<font style="color:#74B602;">y</font>****<font style="color:#74B602;"> 的一维RoPE矩阵( </font>****<font style="color:#74B602;">Ry</font>****<font style="color:#74B602;"> )处理</font>****<font style="color:rgb(25, 27, 31);">，然后再将两半处理后的结果拼接在一起，就做完了2维的RoPE处理</font>**

<font style="color:rgb(25, 27, 31);">假设一个图像的patch的embedding是512维，位置是(x, y)，其中 x 表示Height方向Index，y 表示Width方向Index。类似于一维情况，我们为每个坐标计算角度 θ。假设 embedding 维度仍为 d，则</font>**<font style="color:#74B602;">对于位置 (x, y)，θ 的计算公式</font>**<font style="color:rgb(25, 27, 31);">和一维相同：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203471970-9348b777-fae6-4332-af83-81621b7fd4ef.png)

<font style="color:rgb(25, 27, 31);">对于二维情况的旋转矩阵，我们可以对位置 (x, y) 的 embedding 进行以下操作, 假设embedding的维度为512维, 分</font>**<font style="color:#74B602;">为四个一组</font>**<font style="color:rgb(25, 27, 31);">，</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">x[0] x[1] 乘上下面的矩阵：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203544127-c07913f9-9449-48ac-ab2c-16e3a9ef6b31.png)

<font style="color:rgb(25, 27, 31);">x[2], x[3]则乘上下面的矩阵</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203550700-624f59d7-a496-4c87-b5b9-89539bae08ef.png)

  
<font style="color:rgb(25, 27, 31);">也就是词向量的512维embedding可以每四个一组，乘上下面的矩阵：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742439287670-57bb6bb1-b15d-4c49-bab6-67b38b866ed9.png)

<font style="color:rgb(25, 27, 31);">一维和二维的情况可以总结如下:（</font>**<font style="color:#74B602;">RoPE-1D就是两两一组，每组去乘红框中的矩阵，RoPE-2D就是四个一组，每组也是去乘对应红框中的矩阵</font>**<font style="color:rgb(25, 27, 31);">）</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1742439505454-af99d6b3-0f62-46ff-9208-b1a150583007.jpeg)

:::color5
**<font style="color:#601BDE;">3.三维RoPE</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">针对一个位置</font>**<font style="color:rgb(25, 27, 31);">(x,y,z)</font><font style="color:rgb(25, 27, 31);"> ，</font>**<font style="color:rgb(25, 27, 31);">对维度为 </font>**<font style="color:rgb(25, 27, 31);">d</font>**<font style="color:rgb(25, 27, 31);"> 的输入向量分成三份，</font>****<font style="color:#74B602;">前一份向量用 </font>**<font style="color:#74B602;">x</font>**<font style="color:#74B602;"> 的一维RoPE矩阵( </font>**<font style="color:#74B602;">Rx</font>**<font style="color:#74B602;"> )处理，中间一份向量用 </font>**<font style="color:#74B602;">y</font>**<font style="color:#74B602;"> 的一维RoPE矩阵( </font>**<font style="color:#74B602;">Ry</font>**<font style="color:#74B602;"> )处理，最后一份向量用</font>**<font style="color:#74B602;"> </font>**<font style="color:#74B602;">z</font>****<font style="color:#74B602;"> 的一维RoPE矩阵（</font>**<font style="color:#74B602;"> </font><font style="color:#74B602;">Rz</font><font style="color:#74B602;"> </font>**<font style="color:#74B602;">）处理</font>****<font style="color:rgb(25, 27, 31);">，然后再将三份处理后的结果拼接在一起，就做完了3维的RoPE处理。</font>**

<font style="color:rgb(25, 27, 31);">三维的情况就是Qwen2VL中使用的了，其实和二维差不多，只不过RoPE-3D是</font>**<font style="color:#74B602;">每六个一组，对位置 (x, y, z) 的 embedding 进行以下操作</font>**<font style="color:rgb(25, 27, 31);">, 假设embedding的维度为512维, 分为6个一组：</font>

<font style="color:rgb(25, 27, 31);">x[0] x[1] 乘上下面的矩阵：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203659055-0fbcafed-0094-45d1-950c-29499da2d508.png)

<font style="color:rgb(25, 27, 31);">x[2], x[3]乘上下面的矩阵</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203668071-cd8b0a3c-1637-43b2-9120-615958384166.png)

<font style="color:rgb(25, 27, 31);">x[4], x[5]乘上下面的矩阵</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203677158-7d128c5b-cee5-4cb8-9c00-7f8e9f58bcda.png)

**<font style="color:rgb(25, 27, 31);">Qwen2VL中的M-RoPE</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742203696551-67f06c0c-2433-4019-9589-a33083f7488a.png)

<font style="color:rgb(25, 27, 31);">上图中为Qwen2-VL中3维位置的Index示意图，其实就是分成了3维，</font>**<font style="color:#74B602;">第一维是时间，第二维是Height方向, 第三维是Width方向</font>**<font style="color:rgb(25, 27, 31);">，具体得到每个图像Patch/文本Text的Index，使用ROPE-3D位置编码</font>

<font style="color:rgb(25, 27, 31);">M-rope 一共有三个ID，分别是 (temporal ID, height ID, width ID)。</font>

+ <font style="color:rgb(25, 27, 31);">当仅有 text 输入的时候，M-rope就等效于 1D-RoPE</font>
+ <font style="color:rgb(25, 27, 31);">当有图文一起输入的时候，temporal ID 保持不变，只有height ID 和 width ID 在变</font>
+ <font style="color:rgb(25, 27, 31);">当有视频输入的时候，temporal ID就是frame ID，如最终的上图</font>

:::color5
**<font style="color:#601BDE;">4.优点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">相比于1D-RoPE，M-rope在下游任务上有更好的效果，尤其是video benchmark。  
</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742198772184-14a808bc-434d-48dc-81e5-319f4e09e0fe.png)

2. <font style="color:rgb(25, 27, 31);">M-rope带来的外推性使得qwen2vl在面对 超过训练长度的文本时也有不错的泛化性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742198772133-028a08c5-af99-457c-a81d-00acf66aabe0.png)

