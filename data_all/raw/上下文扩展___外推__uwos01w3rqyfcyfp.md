# 上下文扩展 & 外推

<!-- source: yuque://zhongxian-iiot9/hlyypb/uwos01w3rqyfcyfp -->

# <font style="color:#1f2329;">简介</font>
:::color3
<font style="color:#1f2329;">上下⽂⻓度（ContextLength）指模型在⼀次推理中能够处理的最⼤⽂本⻓度。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⽀持⻓⽂本处理：更⻓的上下⽂⻓度可以处理更⻓的输⼊</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，例如⻓⽂档、代码⽂件等。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">提⾼模型的连贯性：在⻓对话中 ，模型可以更好地保持上下⽂ ，⽣成更相关的回复。</font>

:::



# 大模型外推
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">外推性挑战：</font>**<font style="color:rgb(25, 27, 31);">如何在</font>**<font style="color:#ED740C;">推理阶段确保模型能处理远超预训练时的文本长度</font>**<font style="color:rgb(25, 27, 31);">，已成为当前大型模型面临的核心问题之一，我们将此问题视为大模型的</font>**<font style="color:rgb(25, 27, 31);">外推性挑战</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">参考：</font>[再论大模型位置编码及其外推性（万字长文）](https://zhuanlan.zhihu.com/p/675243992) [十分钟读懂旋转编码（RoPE）](https://zhuanlan.zhihu.com/p/647109286)

:::

:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

<font style="color:rgb(25, 27, 31);">现在，众多大型模型已开始支持</font>**<font style="color:rgb(25, 27, 31);">长文本</font>**<font style="color:rgb(25, 27, 31);">的推理，如最新的</font>[<font style="color:rgb(9, 64, 142);">GPT4 Turbo</font>](https://zhida.zhihu.com/search?content_id=238184119&content_type=Article&match_order=1&q=GPT4+Turbo&zhida_source=entity)<font style="color:rgb(25, 27, 31);">能处理超过</font>**<font style="color:rgb(25, 27, 31);">128k</font>**<font style="color:rgb(25, 27, 31);">的内容，而</font>[<font style="color:rgb(9, 64, 142);">Baichuan2</font>](https://zhida.zhihu.com/search?content_id=238184119&content_type=Article&match_order=1&q=Baichuan2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">也可应对最长为</font>**<font style="color:rgb(25, 27, 31);">192K</font>**<font style="color:rgb(25, 27, 31);">的文本。但受显存资源约束，</font>**<font style="color:#DF2A3F;">这些模型在训练时并不一定会处理如此长的文本，其预训练阶段通常仅涉及约4k的内容。</font>**

:::color5
**<font style="color:#601BDE;">2.如何提升外推能力</font>**

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
**<font style="color:#601BDE;">3.应用场景</font>**

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
**<font style="color:#601BDE;">4.外推能力评估</font>**

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



# <font style="color:#1f2329;">YARN（YetAnotherRopeExtension） </font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：YARN（YetAnotherRopeExtension）是一种</font>**<font style="color:#ED740C;">基于改进的相对位置编码（RoPE）机制来扩展上下文长度的方法</font>**<font style="color:rgb(51, 51, 51);">。RoPE机制最初用于Transformer模型中，通过引入相对位置信息，使得模型能够捕捉序列中的位置关系。YARN在此基础上进行了优化，通过动态扩展位置编码的能力，支持更长的上下文处理。</font>

:::

:::color5
**<font style="color:#601BDE;">1.YARN原理</font>**

:::

1. **相对位置编码扩展**：RoPE编码器原本用于编码固定长度的相对位置信息。YARN通过调整和扩展RoPE的编码方式，使其能够适应更长的序列长度。
2. **分段编码**：将长序列分割成多个较小的段落，每个段落独立进行RoPE编码，同时保持段落之间的位置信息关联。
3. **全局与局部结合**：在编码过程中，YARN同时考虑序列的局部和全局信息，确保在扩展上下文长度的同时，模型能够有效捕捉长距离依赖关系。<font style="color:#601BDE;"></font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**优点**

1. **计算效率高**：通过基于RoPE的相对位置编码，避免了传统的全注意力机制的O(n²)计算复杂度，**<font style="color:#74B602;">显著降低了计算量</font>**。
2. **支持长上下文**：YARN优化了位置编码的生成方式，**<font style="color:#74B602;">能够高效处理长序列</font>**，支持数万甚至数十万的上下文长度。
3. **与现有模型兼容**：YARN可以通过修改原有的RoPE编码层引入，具有良好的兼容性，容易集成到现有的模型架构中。

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

# <font style="color:#1f2329;">Dual-Chunk-Attention</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：DualChunkAttention是一种</font>**<font style="color:#ED740C;">通过分块处理来扩展上下文长度的注意力机制</font>**<font style="color:rgb(51, 51, 51);">。其核心思想是将输入序列分割成多个较小的块（chunks），然后在每个块内部和块之间分别进行注意力计算，最终将结果整合以得到整个序列的输出。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

1. **分割序列**：将输入序列分割成多个长度为`chunk_size`的段落。
2. **块内注意力**：在每个块内，进行传统的全注意力计算，捕捉局部的依赖关系。
3. **块间注意力**：在分割后的不同块之间，使用一种高效的注意力机制（如滑动窗口注意力或稀疏注意力），**<font style="color:#74B602;">捕捉跨块的全局依赖</font>**。
4. **结果整合**：将块内和块间的注意力输出进行有效的融合，确保最终的输出能够全面反映整个序列的信息。

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **有效降低计算复杂度**：通过分块处理和在块间使用高效的注意力机制，DualChunkAttention**<font style="color:#74B602;">显著降低了计算复杂度，支持长序列的处理</font>**。
2. **支持灵活的块大小**：可以根据任务需求和计算资源，灵活调整块的大小和注意力机制的类型，实现最佳的扩展效果。
3. **保持模型表现**：通过同时捕捉局部和全局的依赖关系，DualChunkAttention能够有效维持甚至提升模型的性能。

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **实现复杂**：需要对模型架构进行较大的修改，实现块的分割和注意力机制的整体调度。
2. **增加参数量**：引入块间注意力机制可能增加模型的参数量，对计算资源提出更高的要求。
3. **需要参数调优**：块的大小和注意力机制的选择需要进行精细的参数调优，增加开发和调试的成本。

```python
import torch
import torch.nn as nn
import math

class DualChunkAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, chunk_size=512, window_size=256):
        super(DualChunkAttention, self).__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.chunk_size = chunk_size
        self.window_size = window_size
        self.head_dim = embed_dim // num_heads
        self.scaling = self.head_dim ** -0.5
        
        self.key_proj = nn.Linear(embed_dim, embed_dim)
        self.query_proj = nn.Linear(embed_dim, embed_dim)
        self.value_proj = nn.Linear(embed_dim, embed_dim)
        
    def forward(self, x, attention_mask=None):
        """
        前向传播
        :param x: 输入序列，形状为[batch_size, seq_len, embed_dim]
        :param attention_mask: 注意力掩码
        :return: 处理后的序列，形状为[batch_size, seq_len, embed_dim]
        """
        batch_size, seq_len, _ = x.size()
        
        # 分割序列到块
        chunks = []
        for i in range(0, seq_len, self.chunk_size):
            chunk = x[:, i:i + self.chunk_size, :]
            chunks.append(chunk)
        
        # 块内注意力
        output_chunks = []
        for chunk in chunks:
            # 展开key和query
            k = self.key_proj(chunk)
            q = self.query_proj(chunk)
            
            # 计算块内注意力
            scores = (q @ k.transpose(-2, -1)) * self.scaling
            
            if attention_mask is not None:
                mask = attention_mask[:, i:i + self.chunk_size, i:i + self.chunk_size]
                scores = scores.masked_fill(mask == 0, -10000.0)
            
            attention = torch.softmax(scores, dim=-1)
            output = (attention @ self.value_proj(chunk))
            output_chunks.append(output)
        
        # 整合块内输出
        output = torch.cat(output_chunks, dim=1)
        
        # 块间注意力部分（根据具体需求实现）
        # ... 实现块间注意力部分 ...
        
        return output

# 示例使用
embed_dim = 512
num_heads = 8
chunk_size = 512
window_size = 256
seq_len = 4096
batch_size = 32

dca_layer = DualChunkAttention(embed_dim=512, num_heads=8, chunk_size=512, window_size=256)

x = torch.randn(batch_size, seq_len, embed_dim)
output = dca_layer(x)

print("输入序列长度:", seq_len)
print("输出序列长度:", output.size(1))
```

# <font style="color:#1f2329;">NTK-aware插值</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：NTK-aware插值方法基于神经网络的Kronecker 积（NTK）特性，</font>**<font style="color:#ED740C;">通过插值的方式扩展上下文长度</font>**<font style="color:rgb(51, 51, 51);">。这种方法的核心思想是利用NTK矩阵的性质，在保持模型原有的训练参数不变的情况下，扩展上下文窗口。</font>

:::

:::color5
**<font style="color:#2F4BDA;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **<font style="color:rgb(51, 51, 51);">保持模型性能</font>**<font style="color:rgb(51, 51, 51);">：插值过程不改变原有模型参数，</font>**<font style="color:#74B602;">保留了模型原有的特征提取能力</font>**<font style="color:rgb(51, 51, 51);">。</font>
2. **<font style="color:rgb(51, 51, 51);">灵活扩展</font>**<font style="color:rgb(51, 51, 51);">：可以根据需求选择上下文长度，具有较高的灵活性。</font>
3. **<font style="color:rgb(51, 51, 51);">低计算复杂度</font>**<font style="color:rgb(51, 51, 51);">：基于NTK的插值过程计算量相对较低，适合对计算资源有限的场景。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **<font style="color:rgb(51, 51, 51);">依赖NTK性质</font>**<font style="color:rgb(51, 51, 51);">：该方法依赖于模型的NTK特性，可能不适用于所有模型架构。</font>
2. **<font style="color:rgb(51, 51, 51);">应用场景受限</font>**<font style="color:rgb(51, 51, 51);">：插值方法可能存在</font>**<font style="color:#74B602;">边界效应</font>**<font style="color:rgb(51, 51, 51);">，影响某些特定任务的表现。</font>

```python
import torch
import torch.nn as nn
import numpy as np

def ntk_interpolation(x, original_length, target_length):
    """
    NTK-aware插值方法用于扩展上下文长度
    :param x: 输入序列，形状为[batch_size, original_length, embed_dim]
    :param original_length: 原始上下文长度
    :param target_length: 目标上下文长度
    :return: 插值后的序列，形状为[batch_size, target_length, embed_dim]
    """
    # 生成插值点
    interpolation_factor = target_length / original_length
    time = np.linspace(0, 1, target_length)
    
    # 假设使用线性插值，可以替换成其他插值方法如 spline
    x_interpolated = np.zeros((x.shape[0], target_length, x.shape[2]))
    for i in range(x.shape[0]):
        for j in range(x.shape[2]):
            x_interpolated[i, :, j] = np.interp(time, [0, 1], [x[i, 0, j], x[i, -1, j]])
    
    return torch.FloatTensor(x_interpolated)

# 示例使用
batch_size = 32
original_length = 1024
target_length = 4096

# 假设embed_dim=512
x = torch.randn(batch_size, original_length, 512)
x_interpolated = ntk_interpolation(x, original_length, target_length)

print("Original shape:", x.shape)
print("Interpolated shape:", x_interpolated.shape)
```

# <font style="color:#1f2329;">LogN-Scaling</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

<font style="color:rgb(51, 51, 51);">LogN-Scaling方法通过分层的注意力机制来缩放上下文长度。其核心思想是将长序列分成多个短序列，通过多层注意力机制逐步捕获不同时间尺度的信息，并最终整合这些信息来生成长序列的表示。</font>

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **<font style="color:rgb(51, 51, 51);">高效扩展</font>**<font style="color:rgb(51, 51, 51);">：通过分层处理，LogN-Scaling能够有效捕捉长序列中的重要信息，提升模型的表现。</font>
2. **<font style="color:rgb(51, 51, 51);">低计算复杂度</font>**<font style="color:rgb(51, 51, 51);">：相比于直接扩展序列长度，分层的机制减少了每层的计算复杂度。</font>
3. **<font style="color:rgb(51, 51, 51);">多尺度信息</font>**<font style="color:rgb(51, 51, 51);">：能够同时考虑局部和全局的信息，提升模型对长序列的理解能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **<font style="color:rgb(51, 51, 51);">多层设计复杂</font>**<font style="color:rgb(51, 51, 51);">：需要设计和管理多层注意力机制，增加模型复杂度。</font>
2. **<font style="color:rgb(51, 51, 51);">训练时间增加</font>**<font style="color:rgb(51, 51, 51);">：多层的训练和参数调整需要更多的时间和计算资源。</font>

```python
import torch
import torch.nn as nn
import math

class LogNScaler(nn.Module):
    def __init__(self, embed_dim, num_layers=2):
        super(LogNScaler, self).__init__()
        self.num_layers = num_layers
        self.layers = nn.ModuleList()
        for _ in range(num_layers):
            self.layers.append(
                nn.TransformerEncoderLayer(
                    d_model=embed_dim,
                    nhead=8,
                    dim_feedforward=2*embed_dim,
                    dropout=0.1,
                    activation='gelu'
                )
            )
    
    def forward(self, x, src_key_padding_mask=None):
        """
        前向传播
        :param x: 输入序列，形状为[seq_len, batch_size, embed_dim]
        :param src_key_padding_mask: 掩码
        :return: 缩放后的序列，形状为[seq_len, batch_size, embed_dim]
        """
        for layer in self.layers:
            x = layer(x, src_key_padding_mask)
        return x

# 示例使用
embed_dim = 512
num_layers = 2
seq_len = 4096
batch_size = 32

# 创建一个LogNScaler实例
model = LogNScaler(embed_dim=512, num_layers=2)

# 生成随机输入
x = torch.randn(seq_len, batch_size, embed_dim)
output = model(x)

print("输入序列长度:", seq_len)
print("输出序列长度:", output.size(0))
```

# <font style="color:#1f2329;">窗⼝注意⼒</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

<font style="color:rgb(51, 51, 51);">传统的注意力机制在处理长序列时，需要计算所有位置之间的注意力得分，计算复杂度为O(n²)，其中n为序列长度。窗口注意力机制通过将注意力限制在局部窗口内，显著降低计算复杂度到O(n)或O(n log n)，从而支持长序列的处理。</font>

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **<font style="color:rgb(51, 51, 51);">计算效率高</font>**<font style="color:rgb(51, 51, 51);">：通过限制注意力窗口的大小，显著降低了计算复杂度，提升处理长序列的效率。</font>
2. **<font style="color:rgb(51, 51, 51);">可扩展性强</font>**<font style="color:rgb(51, 51, 51);">：可以根据硬件资源和任务需求灵活调整窗口大小。</font>
3. **<font style="color:rgb(51, 51, 51);">适合大规模数据</font>**<font style="color:rgb(51, 51, 51);">：适用于需要处理超长序列的场景，如长文本、长视频等。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **<font style="color:rgb(51, 51, 51);">信息损失</font>**<font style="color:rgb(51, 51, 51);">：窗口机制可能导致模型忽略全局信息，影响某些需要全局理解的任务。</font>
2. **<font style="color:rgb(51, 51, 51);">窗口大小选择</font>**<font style="color:rgb(51, 51, 51);">：窗口大小需要根据具体任务进行调整，选择不当可能影响模型表现。</font>

```python
import torch
import torch.nn as nn
import math

class WindowAttention(nn.Module):
    def __init__(self, embed_dim, window_size=250):
        super(WindowAttention, self).__init__()
        self.embed_dim = embed_dim
        self.window_size = window_size
        self.heads = 8
        self.scaling = (embed_dim // self.heads) ** -0.5
        
        self.key_proj = nn.Linear(embed_dim, embed_dim)
        self.query_proj = nn.Linear(embed_dim, embed_dim)
        self.value_proj = nn.Linear(embed_dim, embed_dim)
        
    def forward(self, x, key_padding_mask=None):
        """
        前向传播
        :param x: 输入序列，形状为[seq_len, batch_size, embed_dim]
        :param key_padding_mask: 掩码
        :return: 处理后的序列，形状为[seq_len, batch_size, embed_dim]
        """
        batch_size = x.size(1)
        
        # 展开序列
        k = self.key_proj(x)
        q = self.query_proj(x)
        v = self.value_proj(x)
        
        # 窗口划分
        seq_len = x.size(0)
        windowed_k = []
        for i in range(0, seq_len, self.window_size):
            window = k[i:i + self.window_size, ...]
            windowed_k.append(window)
        
        # 局部注意力计算
        output = torch.zeros_like(x)
        for i, window in enumerate(windowed_k):
            window_len = window.size(0)
            q_window = q[i:i + window_len, ...]
            scores = (q_window @ window.transpose(-2, -1)) * self.scaling
            
            if key_padding_mask is not None:
                # 处理掩码
                mask = key_padding_mask[i:i + window_len, ...].unsqueeze(1)
                scores = scores.masked_fill(mask == 0, -10000.0)
            
            attention = torch.softmax(scores, dim=-1)
            output[i:i + window_len, ...] = (attention @ window).squeeze(1)
        
        return output

# 示例使用
embed_dim = 512
window_size = 250
seq_len = 4096
batch_size = 32

# 创建一个WindowAttention模块
model = WindowAttention(embed_dim=512, window_size=250)

# 生成随机输入
x = torch.randn(seq_len, batch_size, embed_dim)
output = model(x)

print("输入序列长度:", seq_len)
print("输出序列长度:", output.size(0))
```



# <font style="color:rgb(51, 51, 51);">稀疏注意力</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

<font style="color:rgb(51, 51, 51);">稀疏注意力机制通过在注意力权重中引入稀疏性，降低计算复杂度。具体来说，通过选择性地关注序列中的重要位置，减少需要计算注意力的区域数量，从而提升计算效率。</font>

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">计算效率高</font>**<font style="color:rgb(51, 51, 51);">：通过减少注意力计算的区域，显著降低计算量。</font>
+ **<font style="color:rgb(51, 51, 51);">适用长序列</font>**<font style="color:rgb(51, 51, 51);">：适合处理超长序列，支持较大的上下文长度。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">信息损失</font>**<font style="color:rgb(51, 51, 51);">：稀疏化可能导致模型忽略某些重要但不显著的特征。</font>
+ **<font style="color:rgb(51, 51, 51);">实现复杂</font>**<font style="color:rgb(51, 51, 51);">：需要设计有效的稀疏化策略，增加实现的复杂性。</font>

**<font style="color:rgb(51, 51, 51);">实现代码</font>**

```python
import torch
import torch.nn as nn
import math

class SparseAttention(nn.Module):
    def __init__(self, embed_dim, window_size=250, sparse_ratio=0.1):
        super(SparseAttention, self).__init__()
        self.embed_dim = embed_dim
        self.window_size = window_size
        self.sparse_ratio = sparse_ratio
        self.heads = 8
        self.scaling = (embed_dim // self.heads) ** -0.5

        self.key_proj = nn.Linear(embed_dim, embed_dim)
        self.query_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, key_padding_mask=None):
        """
        前向传播
        :param x: 输入序列，形状为[seq_len, batch_size, embed_dim]
        :param key_padding_mask: 掩码
        :return: 处理后的序列，形状为[seq_len, batch_size, embed_dim]
        """
        batch_size = x.size(1)
        seq_len = x.size(0)

        # 展开序列
        k = self.key_proj(x)
        q = self.query_proj(x)

        if self.window_size > 0:
            # 分割窗口
            windowed_q = []
            for i in range(0, seq_len, self.window_size):
                window = q[i:i + self.window_size, ...]
                windowed_q.append(window)

            # 稀疏化处理
            output = torch.zeros_like(x)
            for i, window in enumerate(windowed_q):
                window_len = window.size(0)
                scores = (window @ k.transpose(-2, -1)) * self.scaling

                if key_padding_mask is not None:
                    # 处理掩码
                    mask = key_padding_mask[i:i + window_len, ...].unsqueeze(1)
                    scores = scores.masked_fill(mask == 0, -10000.0)

                # 应用稀疏比例
                top_k = int(self.window_size * self.sparse_ratio)
                scores_topk = torch.topk(scores, top_k, dim=-1).values
                attention = torch.softmax(scores_topk, dim=-1)

                output[i:i + window_len, ...] = (attention @ k[i:i + window_len, ...]).squeeze(1)
            return output
        else:
            # 全局稀疏化
            scores = (q @ k.transpose(-2, -1)) * self.scaling

            if key_padding_mask is not None:
                scores = scores.masked_fill(key_padding_mask.unsqueeze(1), -10000.0)

            # 应用稀疏比例
            top_k = int(seq_len * self.sparse_ratio)
            scores_topk = torch.topk(scores, top_k, dim=-1).values
            attention = torch.softmax(scores_topk, dim=-1)

            return (attention @ k).squeeze(1)

# 示例使用
embed_dim = 512
window_size = 250
sparse_ratio = 0.1
seq_len = 4096
batch_size = 32

# 创建一个SparseAttention模块
model = SparseAttention(embed_dim=512, window_size=250, sparse_ratio=0.1)

# 生成随机输入
x = torch.randn(seq_len, batch_size, embed_dim)
output = model(x)

print("输入序列长度:", seq_len)
print("输出序列长度:", output.size(0))
```

