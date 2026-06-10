# Attention

<!-- source: yuque://zhongxian-iiot9/hlyypb/us6yna91dbtg2bqy -->

# Multi Head Attention
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">查询(Query)、键(Key)和值(Value)是从输⼊向量中线性投影出来的不同表⽰。每个头会通过不同的投影矩阵 </font>_<font style="color:#1f2329;">WQ</font>_<font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">WK</font>_<font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">WV   </font>_<font style="color:#1f2329;">⽣成多组 Q、K、V，并通过点积注意⼒来计算它们之间的相关性。</font>**<font style="color:#ED740C;">通过多头的并⾏计算，模型能够从多个角度提取序列间的复杂依赖关系，进⽽提⾼对不同上下⽂的捕捉能⼒</font>**<font style="color:#1f2329;">。最 后，各个头的输出会通过拼接并再次线性变换得到最终的注意⼒输出:</font>

<font style="color:#1f2329;">headi = Attention(QW</font><sub><font style="color:#1f2329;">Qi</font></sub><font style="color:#1f2329;">,KW</font><sub><font style="color:#1f2329;">Ki,</font></sub><font style="color:#1f2329;">VW</font><sub><font style="color:#1f2329;">Vi </font></sub><font style="color:#1f2329;">)</font>

<font style="color:#1f2329;">MultiHead(Q, K, V ) = Concat(head</font><sub><font style="color:#1f2329;">1</font></sub><font style="color:#1f2329;">, … , head</font><sub><font style="color:#1f2329;">h</font></sub><font style="color:#1f2329;"> )W</font><sub><font style="color:#1f2329;">O</font></sub>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:#117CEE;">self-attention计算过程</font>**

<font style="color:#1f2329;">每⼀次的self-attention的计算涉及到三个中间权重矩阵Wq,Wk,Wv，他们分别对输⼊的X进⾏ 线性变换，⽣成query、key和value这三个新的tensor，整个的计算步骤如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738909732498-8e5c0e02-44cf-4c0f-8721-1d55406b6ca1.png)

1. **<font style="color:rgb(51, 51, 51);">输入投影：</font>**<font style="color:#1f2329;">输⼊</font><font style="color:rgb(51, 51, 51);">X∈R</font><sup><font style="color:rgb(51, 51, 51);">N×d_model</font></sup><font style="color:#1f2329;">分别与 </font>_<font style="color:#1f2329;">Wq、Wk、Wv</font>_<font style="color:#1f2329;">矩阵相乘，得到</font>_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">、</font>_<font style="color:#1f2329;">K</font>_<font style="color:#1f2329;">、</font>_<font style="color:#1f2329;">V  </font>_<font style="color:rgb(51, 51, 51);">矩阵</font>（序列长度×d_model，512×768）
2. **<font style="color:rgb(51, 51, 51);">注意力权重：</font>**_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">， </font>_<font style="color:#1f2329;">K</font>_<sup>_<font style="color:#1f2329;">T</font>_</sup>_<font style="color:#1f2329;">  </font>_<font style="color:#1f2329;">矩阵相乘，得到</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">中各个词 之间的相关度，并scale（为了防⽌结果过⼤，除以他们</font>**<font style="color:#74B602;">维度 </font>**_**<font style="color:#74B602;">d</font>**_<sub>_**<font style="color:#74B602;">k</font>**_</sub><font style="color:#1f2329;">的均⽅根）。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737700893631-59482785-ce6c-4e63-ab2c-196b253e7dee.png)

<font style="color:#1f2329;">通过</font>**<font style="color:#74B602;">Softmax函数归⼀化，得到归⼀化后各个词与其他词的相关度。</font>**

3. **<font style="color:rgb(51, 51, 51);">值加权：</font>**<font style="color:#1f2329;">将第2步的相关度矩阵与</font>_<font style="color:#1f2329;">V </font>_<font style="color:#1f2329;">相乘，即加权求和，得到每个词新的向量编码。</font>
4. **<font style="color:rgb(51, 51, 51);">输出投影</font>**<font style="color:rgb(51, 51, 51);">：将多头结果拼接后通过线性变换。</font>

**<font style="color:#117CEE;">multi-head计算过程</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738909830054-889ce53c-0455-4191-90c7-926ddb38006e.png)

<font style="color:#1f2329;">Multi-HeadSelf-Attention将多个不同单头的Self-Attention输出Concat成⼀条，然后再经过⼀个全连接层降维输出。例如，⼀个self-attention计算的输出为：</font>

<font style="color:#1f2329;">output_0 =(batch_size, max_len, w_length)</font>

<font style="color:#1f2329;">那么n个attention进⾏concat之后，输出就为：</font>

<font style="color:#1f2329;">output_sum = (batch_size, max_len,n *w_length)</font>

<font style="color:#1f2329;">这个concat的结果再连⼀层全连接 层即为整个multi-headattention的输出。如下图所⽰，右边的部分即为⼀个multi-headattention 的计算过程，其中的h指的是attention的个数，即上⾯例⼦中的n。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">多头的优点</font>**

1. **捕捉不同的特征**：通过使用多个不同的注意力头，模型可以在同一时间从不同的子空间中学习到信息。这意味着每个头可以专注于不同的特征或关系，从而捕捉输入数据的多样性。
2. **增强上下文感知**：每个注意力头可以关注输入序列中的不同部分，因此多头注意力能够更全面地整合上下文信息。尤其是在处理长序列数据时，这种能力变得尤为重要。
3. **并行计算**：多头注意力机制可以在不同的注意力头之间并行计算，利用现代计算硬件（如GPU）的性能，提升运算效率。
4. **避免单一注意力头的局限性**：单一的注意力头可能无法捕捉到复杂的关系或特征，而多头注意力通过组合多个注意力头的输出，能够提供更全面和复杂的表示。
5. **增加模型的表达能力**：多头注意力机制增加了模型的参数数量，从而提升了模型的表达能力。通过在多个子空间中学习，模型能够更好地拟合复杂的模式和关系。

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(SelfAttention, self).__init__()
        self.embed_size = embed_size  # 嵌入维度
        self.heads = heads  # 注意力头的数量
        self.head_dim = embed_size // heads  # 每个注意力头的维度

        assert (
            self.head_dim * heads == embed_size
        ), "嵌入维度必须能被头数量整除"

        # 定义 Q, K, V 的线性变换
        self.values = nn.Linear(embed_size, embed_size, bias=False)  # V
        self.keys = nn.Linear(embed_size, embed_size, bias=False)    # K
        self.queries = nn.Linear(embed_size, embed_size, bias=False) # Q
        self.fc_out = nn.Linear(embed_size, embed_size)              # 输出线性变换

    def forward(self, x):
        N, seq_length, _ = x.shape  # N: 批量大小; seq_length: 序列长度; _ : 嵌入维度

        # 线性变换得到 Q, K, V
        values = self.values(x)  # (N, seq_length, embed_size)
        keys = self.keys(x)      # (N, seq_length, embed_size)
        queries = self.queries(x) # (N, seq_length, embed_size)

        # 将 Q, K, V 的维度调整为 (N, seq_length, heads, head_dim)
        values = values.view(N, seq_length, self.heads, self.head_dim).transpose(1, 2)  # (N, heads, seq_length, head_dim)
        keys = keys.view(N, seq_length, self.heads, self.head_dim).transpose(1, 2)      # (N, heads, seq_length, head_dim)
        queries = queries.view(N, seq_length, self.heads, self.head_dim).transpose(1, 2) # (N, heads, seq_length, head_dim)

        # 计算注意力（Scaled Dot-Product Attention）
        energy = torch.einsum("nhqd,nhkd->nhqk", [queries, keys])  # (N, heads, seq_length, seq_length)
        attention = F.softmax(energy / (self.embed_size ** (1 / 2)), dim=3)  # 归一化

        # 结合 V 和注意力权重
        out = torch.einsum("nhql,nhld->nhqd", [attention, values]).reshape(
            N, seq_length, self.heads * self.head_dim
        )  # (N, seq_length, embed_size)

        # 最后通过线性层输出
        out = self.fc_out(out)  # (N, seq_length, embed_size)
        return out

# 测试 SelfAttention 类
if __name__ == "__main__":
    embed_size = 256  # 嵌入维度
    heads = 8  # 注意力头数量
    x = torch.rand(32, 10, embed_size)  # 32 为批量大小，10 为序列长度

    attention_layer = SelfAttention(embed_size, heads)
    out = attention_layer(x)
    print(out.shape)  # 输出维度应该是 (32, 10, 256)
```

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        """
        Args:
            d_model: 模型维度 (int)
            num_heads: 注意力头数 (int)
        """
        super().__init__()
        assert d_model % num_heads == 0, "d_model必须能被num_heads整除"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # 每个头的维度
        
        # 定义线性变换层
        self.Wq = nn.Linear(d_model, d_model)  # (d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)  # (d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)  # (d_model, d_model)
        self.Wo = nn.Linear(d_model, d_model)  # (d_model, d_model)
        
    def forward(self, q, k, v, mask=None):
        """
        Args:
            q: query向量       (batch_size, seq_len_q, d_model)
            k: key向量         (batch_size, seq_len_k, d_model)
            v: value向量       (batch_size, seq_len_v, d_model)
            mask: 掩码         (batch_size, 1, 1, seq_len_k) 或 (batch_size, 1, seq_len_q, seq_len_k)
            
        Returns:
            output: 注意力输出  (batch_size, seq_len_q, d_model)
            attention_weights: 注意力权重 (batch_size, num_heads, seq_len_q, seq_len_k)
        """
        batch_size = q.size(0)
        
        # 线性变换 + 分头
        q = self.Wq(q)  # (batch_size, seq_len_q, d_model)
        k = self.Wk(k)  # (batch_size, seq_len_k, d_model)
        v = self.Wv(v)  # (batch_size, seq_len_v, d_model)
        
        # 重塑形状用于多头计算
        q = q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)  # (batch_size, num_heads, seq_len_q, d_k)
        k = k.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)  # (batch_size, num_heads, seq_len_k, d_k)
        v = v.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)  # (batch_size, num_heads, seq_len_v, d_k)
        
        # 计算缩放点积注意力
        scores = torch.matmul(q, k.transpose(-2, -1))  # (batch_size, num_heads, seq_len_q, seq_len_k)
        scores = scores / (self.d_k ** 0.5)  # 缩放
        
        # 应用mask（如果存在）
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # softmax得到注意力权重
        attention_weights = F.softmax(scores, dim=-1)  # (batch_size, num_heads, seq_len_q, seq_len_k)
        
        # 应用注意力权重到value
        output = torch.matmul(attention_weights, v)  # (batch_size, num_heads, seq_len_q, d_k)
        
        # 合并多头结果
        output = output.transpose(1, 2).contiguous()  # (batch_size, seq_len_q, num_heads, d_k)
        output = output.view(batch_size, -1, self.d_model)  # (batch_size, seq_len_q, d_model)
        
        # 最终线性变换
        output = self.Wo(output)  # (batch_size, seq_len_q, d_model)
        
        return output, attention_weights

# 超参数
batch_size = 32
seq_len = 10
d_model = 512
num_heads = 8

# 初始化模块
mha = MultiHeadAttention(d_model, num_heads)

# 创建测试数据
q = torch.randn(batch_size, seq_len, d_model)
k = v = torch.randn(batch_size, seq_len, d_model)
mask = torch.ones(batch_size, 1, 1, seq_len).bool()  # 示例mask

# 前向传播
output, attn_weights = mha(q, k, v, mask)
print(output.shape)        # torch.Size([32, 10, 512])
print(attn_weights.shape)  # torch.Size([32, 8, 10, 10])
```

## <font style="color:rgb(53, 53, 53);">简介QKV，作用，向量维度</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：在Transformer模型中，QKV代表查询（Query）、键（Key）和值（Value）。这三个组件是在自注意力机制中用于处理序列数据的核心部分。</font>

:::

:::color5
**<font style="color:#601BDE;">1.QKV作用</font>**

:::

1. **查询（Query）**：用于从输入序列中提取相关信息。每个输入的向量都生成一个查询向量，它决定了该位置应关注其他位置的信息。
2. **键（Key）**：为每个输入向量提供一个标识，帮助计算与查询的相关性。每个输入的向量生成一个键向量，用于与查询向量进行比对，以衡量其重要性。
3. **值（Value）**：包含实际的数据信息。在计算注意力时，从值向量中提取信息。每个键都会对应一个值，值向量在注意力权重应用后会被加权求和，用于生成最终的输出。

:::color5
**<font style="color:#601BDE;">2.QKV的矩阵大小  |  d</font>**<sub>**<font style="color:#601BDE;">k</font>**</sub>**<font style="color:#601BDE;">的大小</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">假设模型的参数配置为：</font>**
    - **<font style="color:rgb(51, 51, 51);">输入词嵌入维度</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">d_model</font>`<font style="color:rgb(51, 51, 51);">（如BERT-base的768，GPT-3的12288）</font>
    - **<font style="color:rgb(51, 51, 51);">多头注意力头数</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">h</font>`<font style="color:rgb(51, 51, 51);">（如BERT-base的12头，GPT-3的96头）</font>
2. **<font style="color:rgb(51, 51, 51);">整体Q/K/V矩阵的维度</font>**
    - <font style="color:rgb(51, 51, 51);">输入序列经过线性变换得到Q、K、V矩阵，每个矩阵的维度为：  
</font>`**<font style="color:rgb(51, 51, 51);">[序列长度 n × d_model]</font>**`<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">例如：</font>**<font style="color:#74B602;">输入序列长度为512</font>**<font style="color:rgb(51, 51, 51);">，</font>`<font style="color:rgb(51, 51, 51);">d_model=768</font>`<font style="color:rgb(51, 51, 51);"> → Q/K/V的维度均为</font>`**<font style="color:#74B602;">512×768</font>**`<font style="color:rgb(51, 51, 51);">。</font>
3. **<font style="color:rgb(51, 51, 51);">每个注意力头的Q/K/V向量维度</font>**
    - <font style="color:rgb(51, 51, 51);">多头注意力将Q/K/V矩阵</font>**<font style="color:rgb(51, 51, 51);">按头数</font>**`**<font style="color:rgb(51, 51, 51);">h</font>**`**<font style="color:rgb(51, 51, 51);">拆分</font>**<font style="color:rgb(51, 51, 51);">，每个头的维度为：  
</font>`**<font style="color:rgb(51, 51, 51);">[序列长度 n × d_k]</font>**`<font style="color:rgb(51, 51, 51);">，其中 </font>`**<font style="color:#74B602;">d_k = d_model / h</font>**`<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">BERT-base：</font>`<font style="color:rgb(51, 51, 51);">d_model=768</font>`<font style="color:rgb(51, 51, 51);">, </font>`<font style="color:rgb(51, 51, 51);">h=12</font>`<font style="color:rgb(51, 51, 51);"> → </font>`**<font style="color:#74B602;">d_k=768/12=64</font>**`<font style="color:rgb(51, 51, 51);">，每个头的Q/K/V向量维度为</font>`**<font style="color:#74B602;">512×64</font>**`<font style="color:rgb(51, 51, 51);">。</font>
        * <font style="color:rgb(51, 51, 51);">GPT-3-175B：</font>`<font style="color:rgb(51, 51, 51);">d_model=12288</font>`<font style="color:rgb(51, 51, 51);">, </font>`<font style="color:rgb(51, 51, 51);">h=96</font>`<font style="color:rgb(51, 51, 51);"> → </font>`<font style="color:rgb(51, 51, 51);">d_k=12288/96=128</font>`<font style="color:rgb(51, 51, 51);">。</font>



## <font style="color:rgb(51, 51, 51);">计算复杂度、计算量、参数量</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Self-Attention 计算复杂度、计算量与参数量详解（以 </font>**<font style="color:rgb(51, 51, 51);">LLAMA</font>**<font style="color:rgb(51, 51, 51);"> 为例）</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算复杂度</font>**

:::

<font style="color:rgb(51, 51, 51);">复杂度由序列长度 </font><font style="color:rgb(51, 51, 51);">N</font>_<font style="color:rgb(51, 51, 51);">N</font>_<font style="color:rgb(51, 51, 51);"> 和模型维度 </font><font style="color:rgb(51, 51, 51);">d</font><font style="color:rgb(51, 51, 51);">model</font>_<font style="color:rgb(51, 51, 51);">d</font>_<font style="color:rgb(51, 51, 51);">model</font><font style="color:rgb(51, 51, 51);"> 主导，分为两部分：</font>

+ **<font style="color:rgb(51, 51, 51);">O(N</font>**<sup>**<font style="color:rgb(51, 51, 51);">2</font>**</sup>**<font style="color:rgb(51, 51, 51);">d</font>**<sub>**<font style="color:rgb(51, 51, 51);">model</font>**</sub>**<font style="color:rgb(51, 51, 51);">)</font>**<font style="color:rgb(51, 51, 51);">：来自 QKT</font>_<font style="color:rgb(51, 51, 51);">QKT</font>_<font style="color:rgb(51, 51, 51);"> 和加权求和步骤，与序列长度的平方相关。</font>
+ **<font style="color:rgb(51, 51, 51);">O(Nd</font>**<sub>**<font style="color:rgb(51, 51, 51);">model</font>**</sub><sup>**<font style="color:rgb(51, 51, 51);">2</font>**</sup>**<font style="color:rgb(51, 51, 51);">)</font>**<font style="color:rgb(51, 51, 51);">：来自输入/输出投影，与模型维度的平方相关。</font>

**<font style="color:rgb(51, 51, 51);">当 N ≪ d</font>**<sub>**<font style="color:rgb(51, 51, 51);">model</font>**</sub><font style="color:rgb(51, 51, 51);">：模型维度的平方项主导（如短文本场景）。  
</font>**<font style="color:rgb(51, 51, 51);">当 N ≫ d</font>**<sub>**<font style="color:rgb(51, 51, 51);">model</font>**</sub><font style="color:rgb(51, 51, 51);">：序列长度的平方项主导（如长文本场景）。</font>

:::color5
**<font style="color:#601BDE;">2.计算量（FLOPs）</font>**

:::

以 LLAMA 为例（假设 d<sub>model</sub>=4096,h=32），单层计算量如下：

1. **输入投影（Q/K/V）**：
    - <font style="color:rgb(51, 51, 51);">计算量：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944368443-9bbaea39-ee4f-4d0c-95b8-60295bb50c73.png)
    - <font style="color:rgb(51, 51, 51);">拆分多头：每个头的 d</font><sub><font style="color:rgb(51, 51, 51);">k</font></sub><font style="color:rgb(51, 51, 51);">=d</font><sub><font style="color:rgb(51, 51, 51);">model</font></sub><font style="color:rgb(51, 51, 51);">/h=128</font>
2. **QKᵀ 计算**：
    - <font style="color:rgb(51, 51, 51);">每个头的计算量：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944389723-b764790a-32c7-4e6f-a1eb-c740fb63e9e8.png)
    - <font style="color:rgb(51, 51, 51);">总计算量：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944396695-2924ced4-dfbf-45d0-b644-ffda029e26fd.png)
3. **AV 加权求和**：
    - <font style="color:rgb(51, 51, 51);">每个头的计算量：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944405484-8b97248e-9c6a-4561-8e84-c9fddb3b3365.png)
    - <font style="color:rgb(51, 51, 51);">总计算量：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944412823-a5f2b96c-0d5f-4f43-9c02-b672a49e29fd.png)
4. **输出投影**：
    - <font style="color:rgb(51, 51, 51);">计算量：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944424401-4e878d13-ddbd-4fcc-b31f-5ba07440e117.png)
5. **<font style="color:rgb(51, 51, 51);">总计算量</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944445156-d561aa91-23d8-4486-8f6c-6f0201290af3.png)

**<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">（N=2048,d</font><sub><font style="color:rgb(51, 51, 51);">model</font></sub><font style="color:rgb(51, 51, 51);">=4096）：</font>

+ <font style="color:rgb(51, 51, 51);">投影相关：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944469696-69f82920-5e27-40d2-b049-b9b717013039.png)
+ <font style="color:rgb(51, 51, 51);">注意力相关：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944475115-9b1db793-488c-40e2-a532-c939923779e8.png)
+ **<font style="color:rgb(51, 51, 51);">总计</font>**<font style="color:rgb(51, 51, 51);">：约 </font>**<font style="color:rgb(51, 51, 51);">343.6 GFLOPs/层</font>**<font style="color:rgb(51, 51, 51);">，32 层共 </font>**<font style="color:rgb(51, 51, 51);">11 TFLOPs</font>**<font style="color:rgb(51, 51, 51);">（仅 Self-Attention）。</font>

:::color5
**<font style="color:#601BDE;">3.参数量</font>**

:::

<font style="color:rgb(51, 51, 51);">参数来源于投影矩阵：</font>

1. **输入投影（Q/K/V）**：  
每投影矩阵尺寸为 d<sub>model</sub>×d<sub>model</sub>，共 ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944526593-9860f376-3be2-440a-b39c-5a344a99443c.png)。
2. **输出投影**：  
矩阵尺寸为 d<sub>model</sub>×d<sub>model</sub>，参数量 ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944542223-31d57604-b0bd-4332-a5a1-6b071c971511.png)。
3. **<font style="color:rgb(51, 51, 51);">总参数量</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741944550124-d7c7b6c9-3f1f-4850-ab9e-f4ff2687b74c.png)

**<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">（LLAMA-7B，d</font><sub><font style="color:rgb(51, 51, 51);">model</font></sub><font style="color:rgb(51, 51, 51);">=4096)：</font>

+ <font style="color:rgb(51, 51, 51);">单层参数量：4×40962≈67.1M</font>
+ <font style="color:rgb(51, 51, 51);">32 层总参数量：32×67.1M≈2.1B</font>
+ <font style="color:rgb(51, 51, 51);">剩余参数来自 FFN 等模块（如 FFN 占约 6.4B）。</font>

| **组件** | **单层参数量** | **总参数量（32 层）** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">Self-Attention</font> | <font style="color:rgb(51, 51, 51);">67.1 M</font> | <font style="color:rgb(51, 51, 51);">2.1 B</font> |
| <font style="color:rgb(51, 51, 51);">FFN（d_ff=4d）</font> | <font style="color:rgb(51, 51, 51);">134.2 M</font> | <font style="color:rgb(51, 51, 51);">4.3 B</font> |
| <font style="color:rgb(51, 51, 51);">总计</font> | <font style="color:rgb(51, 51, 51);">-</font> | <font style="color:rgb(51, 51, 51);">~7 B</font> |


## <font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">为什么不能用同一个权重矩阵生成QKV</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：在Transformer模型中，QKV代表查询（Query）、键（Key）和值（Value）。这三个组件是在自注意力机制中用于处理序列数据的核心部分。</font>

:::

:::color5
**<font style="color:#601BDE;">如果用同一个权重矩阵来生成Q、K和V，会导致以下问题：</font>**

:::

1. **信息损失**：查询、键和值在功能和意义上是不同的。如果它们使用相同的权重矩阵，模型将无法有效地学习到它们之间的差异，这会导致表示能力的下降。
2. **注意力计算的失效**：在自注意力机制中，查询与键的匹配程度用于计算注意力权重。如果查询和键相同，模型将无法正确判别哪些位置的信息是重要的，因而无法有效聚焦于相关信息。
3. **灵活性不足**：通过使用不同的权重矩阵，可以独立调整查询、键和值的向量空间，使得模型能更灵活地适应不同的任务和数据。



## <font style="color:rgb(1, 1, 1);">注意力机制为什么除以根号dk, 为什么不是dk</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>_**<font style="color:#1f2329;">d</font>**_<sub>_**<font style="color:#1f2329;">k</font>**_</sub><font style="color:rgb(51, 51, 51);">表示每个注意力头中</font>**<font style="color:#ED740C;">向量的维度</font>**

<font style="color:#1f2329;">在 Softmax 之前对点积注意⼒分数进⾏缩放(除以根号</font>_<font style="color:#1f2329;">dk</font>_<font style="color:#1f2329;">)，是为了应对⾼维向量下点积值过⼤的问题。</font>

_**<font style="color:#1f2329;">d</font>**_<sub>_**<font style="color:#1f2329;">k</font>**_</sub>_<font style="color:#1f2329;">：</font>_`d_k = d_model / h`= 768/12 = 64（以12头的BERT为例）

:::

:::color5
**<font style="color:#601BDE;">1.为什么除以dk</font>**

:::

1. 防止数值不稳定：<font style="color:#1f2329;">避免注意⼒权重极端化，确保模型能够有效学习</font>
2. <font style="color:#1f2329;">避免梯度消失：通过限制输⼊值的范围，确保 Softmax 梯度不会过⼩，保障模型训练效率；</font>
3. <font style="color:#1f2329;">加快模型收敛：缩放使得多头注意⼒机制在⾼维度下保持数值稳定性，从⽽提⾼模型的训练速度和表现</font>

:::color5
**<font style="color:#601BDE;">1.为什么除以根号dk</font>**

:::

<font style="color:#1f2329;">缩放因⼦的引⼊可以防⽌随着</font>_<font style="color:#1f2329;">d</font>_<sub>_<font style="color:#1f2329;">k</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">增加，点积值变得过⼤。</font>**<font style="color:#74B602;">点积的期望值⼤约与向量维度</font>**_**<font style="color:#74B602;">d</font>**_<sub>_**<font style="color:#74B602;">k</font>**_</sub>**<font style="color:#74B602;">成正⽐，因此通过除以根号</font>**_**<font style="color:#74B602;">d</font>**_<sub>_**<font style="color:#74B602;">k </font>**_</sub>_**<font style="color:#74B602;"> </font>**_**<font style="color:#74B602;">，可以将点积值缩放到⼀个合适的范围，确保数值稳定</font>**<font style="color:#1f2329;">。理论上，</font>**<font style="color:#ED740C;">两个独⽴随机向量的点积的标准差⼤约与向量维度</font>**_**<font style="color:#ED740C;">d</font>**_<sub>_**<font style="color:#ED740C;">k</font>**_</sub>_**<font style="color:#ED740C;">  </font>**_**<font style="color:#ED740C;">的平⽅根成⽐例</font>**<font style="color:#1f2329;">，因此通过缩放可以将点积值控制在合理范围内。</font>

## <font style="color:rgb(1, 1, 1);">注意力计算为什么用点乘，不用加法</font>
:::color5
**<font style="color:#601BDE;">为什么用点乘</font>**

:::

1. **计算效率**：点乘运算相较于加法运算在计算效率上更高，特别是在进行大规模矩阵运算时。注意力机制需要处理的向量通常是高维的，使用点乘能够有效地利用向量间的关系。
2. **向量空间特性**：点乘运算能够有效地捕捉两个向量之间的相似性。具体来说，两个向量的点乘结果能够反映它们之间的角度关系，若二者越接近（即角度越小），则点乘的结果就越大，反之亦然。这种性质非常适合于捕捉词之间的相似性与关系，在自然语言处理中非常有用。
3. **归一化处理**：在点乘后，Transformer使用了Softmax函数来归一化结果，从而计算出注意力权重。这一归一化过程使得最终得到的权重能够反映各个输入元素的相对重要性。使用点乘可以使得权重分配更加具有区分性，尤其是在不同的输入特征之间。
4. **数值稳定性**：点乘能较好地处理数值范围的问题。当输入的向量维度较高时，偏向于使用加法可能会导致数值的不稳定性，而点乘可以通过调整维度使得计算结果更加稳定。



## 注意力适用场景 & 传统算法的区别
**<font style="color:rgb(51, 51, 51);">1. 长序列建模（如NLP、语音识别）</font>**

+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：传统RNN/LSTM存在梯度消失和长距离依赖难以捕捉的问题，而卷积操作难以动态关注全局。</font>
+ **<font style="color:rgb(51, 51, 51);">解决方案</font>**<font style="color:rgb(51, 51, 51);">：注意力机制允许模型直接计算序列中任意两个位置的关系权重。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">机器翻译</font>**<font style="color:rgb(51, 51, 51);">：Transformer模型通过自注意力（Self-Attention）同时关注输入序列的所有位置，例如将“猫坐在垫子上”中的“坐”与“猫”和“垫子”动态关联。</font>
    - **<font style="color:rgb(51, 51, 51);">语音识别</font>**<font style="color:rgb(51, 51, 51);">：处理长达数秒的音频序列时，注意力机制能聚焦于当前正在解码的音素对应的声学片段。</font>

**<font style="color:rgb(51, 51, 51);">2. 多模态/异构数据融合</font>**

+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：不同模态数据（如图像+文本）的特征空间差异大，传统拼接或相加操作难以有效融合。</font>
+ **<font style="color:rgb(51, 51, 51);">解决方案</font>**<font style="color:rgb(51, 51, 51);">：跨模态注意力（Cross-Modal Attention）动态对齐不同模态的信息。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">图像描述生成（Image Captioning）</font>**<font style="color:rgb(51, 51, 51);">：生成单词时，注意力聚焦于图像中对应的区域（如生成“鸟”时关注图像中的鸟）。</font>
    - **<font style="color:rgb(51, 51, 51);">视觉问答（VQA）</font>**<font style="color:rgb(51, 51, 51);">：根据问题文本中的关键词（如“颜色”）定位图像中的特定区域（如物体的颜色区域）。</font>

**<font style="color:rgb(51, 51, 51);">3. 动态信息筛选与噪声抑制</font>**

+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：输入数据中存在冗余或噪声（如视频中的背景干扰）。</font>
+ **<font style="color:rgb(51, 51, 51);">解决方案</font>**<font style="color:rgb(51, 51, 51);">：注意力权重自动抑制低相关性部分。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">视频动作识别</font>**<font style="color:rgb(51, 51, 51);">：聚焦于人体关键帧，忽略背景变化。</font>
    - **<font style="color:rgb(51, 51, 51);">金融时间序列预测</font>**<font style="color:rgb(51, 51, 51);">：突出关键时间点（如突发事件）的影响。</font>

**<font style="color:rgb(51, 51, 51);">4. 可解释性需求强的任务</font>**

+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：黑盒模型难以解释决策依据（如医疗诊断）。</font>
+ **<font style="color:rgb(51, 51, 51);">解决方案</font>**<font style="color:rgb(51, 51, 51);">：注意力权重可视化显示模型关注区域。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">医疗影像分析</font>**<font style="color:rgb(51, 51, 51);">：显示模型判断肿瘤时关注的CT图像区域。</font>
    - **<font style="color:rgb(51, 51, 51);">法律文本分类</font>**<font style="color:rgb(51, 51, 51);">：高亮影响判决结果的关键法律条款。</font>

**与传统方法对比**

| **场景** | **传统方法** | **注意力机制优势** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">长文本翻译</font>** | <font style="color:rgb(51, 51, 51);">RNN编码器-解码器</font> | <font style="color:rgb(51, 51, 51);">并行计算全局依赖，解决长距离遗忘问题（如《War and Peace》长句翻译）</font> |
| **<font style="color:rgb(51, 51, 51);">图像+文本任务</font>** | <font style="color:rgb(51, 51, 51);">特征拼接/池化</font> | <font style="color:rgb(51, 51, 51);">动态对齐文本单词与图像区域（如“红色汽车”对应图中的红色像素区域）</font> |
| **<font style="color:rgb(51, 51, 51);">高噪声传感器数据</font>** | <font style="color:rgb(51, 51, 51);">固定滤波器/阈值</font> | <font style="color:rgb(51, 51, 51);">自适应抑制无关传感器信号（如自动驾驶中忽略雨雾噪声，专注车道线）</font> |
| **<font style="color:rgb(51, 51, 51);">实时语音分离</font>** | <font style="color:rgb(51, 51, 51);">固定波束形成</font> | <font style="color:rgb(51, 51, 51);">聚焦目标说话人声纹特征，分离重叠语音（如会议录音中提取特定人发言）</font> |


# <font style="color:#1f2329;">FlashAttention</font><font style="color:#D22D8D;"></font>
:::success
**<font style="color:#1f2329;">背景：</font>**<font style="color:#1f2329;">Transformer的核⼼组件是⾃注意⼒机制（Self-Attention），然⽽，传统的  ⾃注意⼒计算在处理⻓序列时，⾯临着计算量⼤和内存占⽤⾼的问题。FlashAttention是⼀种⾼效的⾃注意⼒计算算法，旨在解决这些问题。在传统实现中，⾃注意⼒计算涉及到⼤型矩阵的乘法和存储。L为序列长度</font>

+ <font style="color:#1f2329;">计算复杂度： </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">L</font>_<sup><font style="color:#1f2329;">2</font></sup>_<font style="color:#1f2329;">d</font>_<sub>_<font style="color:#1f2329;">k</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font>
+ <font style="color:#1f2329;">内存占⽤： 需要存储 </font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">的注意⼒矩阵 ，内存占⽤为 </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">L</font>_<sup><font style="color:#1f2329;">2</font></sup><font style="color:#1f2329;"> </font><font style="color:#1f2329;">)</font>

**<font style="color:#74B602;">对于⻓序列，内存占⽤和计算量都会急剧增加，导致效率低下。</font>**

:::

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Fla</font><font style="color:#1f2329;">shAttention提供了⼀种⾼效且数值稳定的⾃注意⼒计算⽅法 ，通过优化内存访问和计算</font>

<font style="color:#1f2329;">流程，解决了传统⾃注意⼒在⻓序列处理中的</font>**<font style="color:#ED740C;">内存和计算瓶颈</font>**<font style="color:#1f2329;">。总结其优势：</font>

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">内存⾼效：⼤幅降低内存占⽤ ，适合处理⻓序列。</font>
+ <font style="color:#1f2329;">计算⾼效：减少访存开销 ，提⾼计算速度。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:#117CEE;">问题本质</font>**

+ <font style="color:#de7802;">内存瓶颈</font><font style="color:#1f2329;">：GPU 的内存带宽限制了⾃注意⼒的计算速度。</font>
+ <font style="color:#de7802;">访存开销</font><font style="color:#1f2329;">：传统算法需要多次读取和写⼊ GPU 内存 ，导致⼤量的访存操作。</font>

**<font style="color:#117CEE;">核心思想</font>**

<font style="color:#1f2329;">FlashAttention</font><font style="color:#1f2329;">通过以下⽅式优化⾃注意⼒计算：</font>

+ <font style="color:#de7802;">块处理（ Blocking） </font><font style="color:#1f2329;">：将计算划分为⼩块 ，逐块处理，减少⼀次性需要的内存。</font>
+ <font style="color:#de7802;">IO 感知（IO-Awareness）</font><font style="color:#1f2329;">：优化内存访问模式，最⼤化数据在⾼速缓存中的使⽤ ，减少访存开销。</font>
+ <font style="color:#de7802;">数值稳定性</font><font style="color:#1f2329;">：在块内进⾏归⼀化 ，避免数值溢出。</font>

**<font style="color:#117CEE;">实现步骤</font>**

1. **<font style="color:#1f2329;">块划分</font>**<font style="color:#1f2329;">：将序列⻓度</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">划分为多个块，每个块的⼤⼩为</font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">。例如，序列⻓度为 1024，块⼤⼩为 128，则有 8 个块。</font>
2. **<font style="color:#1f2329;">逐块计算</font>**
    - <font style="color:#1f2329;">计算块间的注意⼒：对于每个查询块和键块，计算局部的注意⼒值。</font>
    - <font style="color:#1f2329;">内存占⽤优化：只在寄存器或⾼速缓存中存储当前块的数据，避免将整个</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L</font>_

<font style="color:#1f2329;">的注意⼒矩阵存⼊内存。</font>

3. **数值稳定的softmax计算**
    - <font style="color:#1f2329;">局部归⼀化：在块内进⾏Softmax 计算，使⽤数值稳定的算法，避免指数计算中的溢出。</font>
    - <font style="color:#1f2329;">累积计算：逐块累积注意⼒值和归⼀化因⼦，确保最终结果的准确性。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

1. **减少内存占用**
    - <font style="color:#de7802;">块级处理：</font><font style="color:#1f2329;">避免存储整个注意   ⼒矩阵，内存占⽤从 </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">L</font>_<sup><font style="color:#1f2329;">2</font></sup><font style="color:#1f2329;"> ) 降⾄  </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">LB</font>_<font style="color:#1f2329;">)。</font>
    - <font style="color:#de7802;">适合⻓序列</font><font style="color:#1f2329;">：能够⾼效处理⻓达⼏千甚⾄上万⻓度的序列。</font>
2. **提高计算效率**
    - <font style="color:#2ea121;">减少访存操作：</font><font style="color:#1f2329;">优化内存访问模式，提⾼了数据在⾼速缓存中的命中率。</font>
    - <font style="color:#2ea121;">GPU 加速：</font><font style="color:#1f2329;">充分利⽤GPU 的计算能⼒和寄存器优势。</font>
3. **数值稳定**
    - <font style="color:#117CEE;">局部归一化：</font><font style="color:#1f2329;">在计算过程中保持数值稳定。避免了传统⽅法中的数值溢出和下溢问题。</font>

:::color5
**<font style="color:#601BDE;">3.和传统注意力的区别</font>**

:::

1. **内存占用对比**
    - <font style="color:#de7802;">传统⾃注意⼒：</font><font style="color:#1f2329;">需要存储</font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">的矩阵，内存占⽤⼤。</font>
    - <font style="color:#de7802;">FlashAttention</font><font style="color:#1f2329;">：内存占⽤与   块⼤⼩</font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">成正⽐，⼤幅降低了内存需求。</font>
2. **计算速度对比**
    - <font style="color:#2ea121;">减少访存操作传统⽅法：</font><font style="color:#1f2329;">由于⼤量的访存操作，计算速度受限于内存带宽。</font>
    - <font style="color:#2ea121;">FlashAttention：</font><font style="color:#1f2329;">减少了访存次数，计算速度主要由计算单  元决定，更快。</font>
3. **数值精确对比**
    - <font style="color:#245bdb;">传统⽅法：</font><font style="color:#1f2329;">可能出现数值不稳定，特别是在⻓序列或⾼维度下。</font>
    - <font style="color:#245bdb;">FlashAttention：</font><font style="color:#1f2329;">通过数值稳定的算法，确保了计算精度。</font>

:::color5
**<font style="color:#601BDE;">4.实现代码示例</font>**

:::

```python
import torch

def flash_attention(Q, K, V, block_size=64):
    """
    Flash Attention的PyTorch实现
    
    参数:
        Q: 查询张量，形状为 (batch_size, num_heads, seq_len, head_dim)
        K: 键张量，形状同Q
        V: 值张量，形状同Q
        block_size: 分块大小，控制内存使用
        
    返回:
        O: 注意力输出，形状同Q
    """
    batch_size, num_heads, seq_len, head_dim = Q.shape
    # 初始化输出和中间变量
    O = torch.zeros_like(Q)
    M = torch.full((batch_size, num_heads, seq_len), -float('inf'), device=Q.device, dtype=Q.dtype)
    L = torch.zeros_like(M)
    
    # 分块处理Q序列
    for i in range(0, seq_len, block_size):
        Q_block = Q[:, :, i:i+block_size, :]  # 当前Q块 (B, H, block_q, D)
        block_q = Q_block.size(2)
        
        # 初始化当前块的中间变量
        O_i = torch.zeros((batch_size, num_heads, block_q, head_dim), device=Q.device, dtype=Q.dtype)
        M_i = M[:, :, i:i+block_size].clone()  # (B, H, block_q)
        L_i = L[:, :, i:i+block_size].clone()  # (B, H, block_q)
        
        # 分块处理K/V序列
        for j in range(0, seq_len, block_size):
            K_block = K[:, :, j:j+block_size, :]  # 当前K块 (B, H, block_k, D)
            V_block = V[:, :, j:j+block_size, :]  # 当前V块 (B, H, block_k, D)
            block_k = K_block.size(2)
            
            # 1. 计算块间注意力得分
            S_ij = torch.einsum('bhid,bhjd->bhij', Q_block, K_block)  # (B, H, block_q, block_k)
            
            # 2. 计算当前块的行最大值
            m_curr = S_ij.max(dim=-1).values  # (B, H, block_q)
            
            # 3. 更新最大值并计算指数项
            m_new = torch.maximum(m_curr, M_i)
            exp_prev = torch.exp(M_i - m_new)  # 之前累积项的缩放因子
            exp_curr = torch.exp(S_ij - m_new.unsqueeze(-1))  # 当前块的指数值
            
            # 4. 更新累积求和项
            L_new = exp_prev * L_i + exp_curr.sum(dim=-1)
            
            # 5. 更新输出值
            O_i = exp_prev.unsqueeze(-1) * O_i + torch.einsum('bhij,bhjd->bhid', exp_curr, V_block)
            
            # 保存中间变量供下一个块使用
            M_i = m_new
            L_i = L_new
        
        # 将当前Q块的结果写回最终输出
        O[:, :, i:i+block_size, :] = O_i
        L[:, :, i:i+block_size] = L_i
    
    # 最终归一化处理
    O = O / (L.unsqueeze(-1) + 1e-6)  # 添加极小值防止除以零
    return O

batch_size = 2
num_heads = 4
seq_len = 512
head_dim = 64

Q = torch.randn(batch_size, num_heads, seq_len, head_dim)
K = torch.randn_like(Q)
V = torch.randn_like(Q)

output = flash_attention(Q, K, V, block_size=64)
print(output.shape)  # torch.Size([2, 4, 512, 64])

```



# <font style="color:#6425d0;">PagedAttention机制</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Page Attention 是一种针对长序列处理优化的注意力机制，旨在降低传统自注意力的内存和计算开销，同时保持对长距离依赖的建模能力。其核心思想借鉴计算机系统中的</font>**<font style="color:#ED740C;">分页机制</font>**<font style="color:rgb(51, 51, 51);">，将输入序列分割为多个“页面”（块），动态管理这些块的计算和存储，从而优化资源使用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

1. **传统自注意力瓶颈**  
Transformer的自注意力复杂度为O(N²)，在处理长序列时显存占用激增，尤其在大batch size下，成为训练/推理的主要瓶颈。
2. **分页管理思想**  
Page Attention将输入序列划分为固定大小的页面（Page），每个页面包含连续的token。计算注意力时：
    - **<font style="color:rgb(51, 51, 51);">页面内（Intra-Page）</font>**<font style="color:rgb(51, 51, 51);">：计算当前页面内所有token间的局部注意力。</font>
    - **<font style="color:rgb(51, 51, 51);">页面间（Inter-Page）</font>**<font style="color:rgb(51, 51, 51);">：按需加载其他页面，计算跨页面的稀疏注意力（如相邻页或关键页）。</font>
3. **动态加载机制**  
通过类似虚拟内存的换页策略，仅保留活跃页面在高速内存（如GPU显存）中，非活跃页面暂存于低速内存（如CPU内存或磁盘），按需动态交换，显著降低峰值显存占用。

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">假设输入序列长度N，页面大小P，总页数M=N/P：</font>

1. **分块（Paging）**  
将输入序列划分为M个页面：`X = [X₁, X₂, ..., Xₘ]`，每个Xᵢ ∈ ℝ^{P×d}。
2. **页面内注意力**  
对每个页面Xᵢ，计算局部注意力输出Oᵢ：

```python
Qᵢ, Kᵢ, Vᵢ = XᵢW_Q, XᵢW_K, XᵢW_V
Aᵢ = softmax(QᵢKᵢ^T / √d)  # 形状 [P, P]
Oᵢ = AᵢVᵢ                   # 形状 [P, d]
```

3. **页面间注意力**  
根据策略（如滑动窗口、关键页选择）加载相关页面Xⱼ，计算跨页面注意力：

```python
Qᵢ, Kⱼ, Vⱼ = XᵢW_Q, XⱼW_K, XⱼW_V
Aᵢⱼ = softmax(QᵢKⱼ^T / √d)  # 形状 [P, P]
Oᵢⱼ = AᵢⱼVⱼ                  # 形状 [P, d]
```

4. **结果聚合**  
合并页面内和跨页面结果，得到最终输出：

```python
Oᵢ = Oᵢ + ∑ⱼ∈Neighbor(i) Oᵢⱼ
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

  
**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">显存优化</font>**<font style="color:rgb(51, 51, 51);">：显存占用从O(N²)降至O(MP²)，M为页面数。</font>
+ **<font style="color:rgb(51, 51, 51);">计算高效</font>**<font style="color:rgb(51, 51, 51);">：分块计算利于并行化和硬件加速。</font>
+ **<font style="color:rgb(51, 51, 51);">扩展性强</font>**<font style="color:rgb(51, 51, 51);">：支持超长序列处理（如百万级token）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">块间跳转可能引入额外内存访问开销。</font>
+ <font style="color:rgb(51, 51, 51);">块大小需调优，过小会增加管理开销，过大可能浪费内存。</font>  


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">处理超长文本（如文档摘要、代码生成）。</font>
+ <font style="color:rgb(51, 51, 51);">高并发场景下多序列并行推理（如聊天服务器）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态块大小</font>**<font style="color:rgb(51, 51, 51);">：根据序列长度动态调整块大小。</font>
+ **<font style="color:rgb(51, 51, 51);">块预取</font>**<font style="color:rgb(51, 51, 51);">：预测未来需要的块，提前加载到高速缓存。</font>
+ **<font style="color:rgb(51, 51, 51);">异构存储</font>**<font style="color:rgb(51, 51, 51);">：将低频访问的块迁移到CPU内存或磁盘。</font>  


:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class PageAttention(nn.Module):
    def __init__(self, d_model, n_heads, page_size=64):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.page_size = page_size
        self.head_dim = d_model // n_heads
        
        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)
        
    def forward(self, x):
        # x: [batch, seq_len, d_model]
        B, N, d = x.shape
        P = self.page_size
        M = (N + P - 1) // P  # 计算总页数
        
        # 分页填充并调整形状
        x_padded = nn.functional.pad(x, (0,0,0, M*P - N))
        pages = rearrange(x_padded, 'b (m p) d -> b m p d', p=P)
        
        Q = self.Wq(pages)
        K = self.Wk(pages)
        V = self.Wv(pages)
        
        # 分头处理
        Q = rearrange(Q, 'b m p (h d) -> b h m p d', h=self.n_heads)
        K = rearrange(K, 'b m p (h d) -> b h m p d', h=self.n_heads)
        V = rearrange(V, 'b m p (h d) -> b h m p d', h=self.n_heads)
        
        outputs = []
        for m in range(M):
            # 页面内注意力
            intra_Q = Q[:, :, m]
            intra_K = K[:, :, m]
            intra_V = V[:, :, m]
            attn = torch.einsum('bhpd,bhqd->bhpq', intra_Q, intra_K) / (self.head_dim**0.5)
            attn = torch.softmax(attn, dim=-1)
            intra_out = torch.einsum('bhpq,bhqd->bhp d', attn, intra_V)
            
            # 页面间注意力（示例：关注前一页）
            if m > 0:
                inter_K = K[:, :, m-1]
                inter_V = V[:, :, m-1]
                inter_attn = torch.einsum('bhpd,bhqd->bhpq', intra_Q, inter_K) / (self.head_dim**0.5)
                inter_attn = torch.softmax(inter_attn, dim=-1)
                inter_out = torch.einsum('bhpq,bhqd->bhp d', inter_attn, inter_V)
                intra_out += inter_out
            
            outputs.append(intra_out)
        
        # 合并结果
        out = torch.cat(outputs, dim=2)
        out = rearrange(out, 'b h m p d -> b (m p) (h d)')[:, :N]  # 去除填充
        return self.out(out)

```



# Multi Query Attention(MQA)
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">为了缓解MHA的内存带宽问题，Google在2019年提出了MQA。在MQA中，虽然每个头依然保留独⽴的Query矩阵，但</font><u><font style="color:#2ea121;">Key和Value矩阵是共享的</font></u><font style="color:#1f2329;">。这样做的好处是显著减少了需要加载和存储的Key和Value数据，从⽽降低了内存带宽的需求，尤其是在⾃回  归推理场景中。</font><u><font style="color:#2ea121;">这极⼤地提升了推理速度，尤其适合解码器场景。</font></u>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">输入投影</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Q:</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">nn.Linear(d_model, h * d_k)</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">→ Shape:</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">(batch, n, h, d_k)</font>`
    - <font style="color:rgb(51, 51, 51);">K, V:</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">nn.Linear(d_model, d_k)</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">→ Shape:</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">(batch, n, d_k)</font>`
2. **<font style="color:rgb(51, 51, 51);">扩展 K, V</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">重复 K、V 到每个头：</font>`<font style="color:rgb(51, 51, 51);">K = K.unsqueeze(2).expand(-1, -1, h, -1)</font>`
3. **<font style="color:rgb(51, 51, 51);">注意力计算</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">缩放点积：</font>`<font style="color:rgb(51, 51, 51);">Q @ K.transpose(-2, -1) / sqrt(d_k)</font>`
    - <font style="color:rgb(51, 51, 51);">Softmax 后加权值矩阵：</font>`<font style="color:rgb(51, 51, 51);">attn @ V</font>`

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**优点**

+ **<font style="color:#de7802;">推理速度大幅提升</font>**<font style="color:#1f2329;">：共享Key和Value矩阵减少了多头机制的内存带宽需求，推理速度更快。</font>
+ **<font style="color:#ED740C;">内存占用减少</font>**<font style="color:#1f2329;">：Key和Value矩阵的数量从MHA中的多个缩减为⼀个 ，⼤⼤减少了内存占⽤ 。</font>

**<font style="color:#1f2329;">缺点</font>**

+ **<font style="color:#ED740C;">精度下降</font>**<font style="color:#ED740C;">：</font><font style="color:#1f2329;">由于所有头共享Key和Value矩阵，模型难以捕捉输⼊数据中复杂和多样化的特征，导致模型性能相⽐MHA有所下降。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">资源受限的实时任务（如对话系统、在线翻译）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">动态共享策略：根据输入动态调整共享程度。</font>
+ <font style="color:rgb(51, 51, 51);">混合结构：部分头保留独立 K/V</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import math
import torch.nn as nn
import torch.nn.functional as F

class MultiQueryAttention(nn.Module):
    def __init__(self, embed_dim, num_queries=256, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_queries = num_queries
        self.dropout = dropout

        # 定义线性变换层
        self.W_q = nn.Linear(embed_dim, embed_dim)
        self.W_k = nn.Linear(embed_dim, embed_dim)
        self.W_v = nn.Linear(embed_dim, embed_dim)

        # 定义输出变换层
        self.W_out = nn.Linear(embed_dim, embed_dim)

        # 初始化位置编码
        self.position_enc = nn.Parameter(torch.randn(num_queries, embed_dim))

        # 设置缩放因子
        self.scale = 1.0 / math.sqrt(embed_dim)

    def forward(self, x, attention_mask=None):
        batch_size, seq_len, _ = x.size()

        # 计算键和值
        k = self.W_k(x)
        v = self.W_v(x)

        # 计算共享查询
        # 使用平均池化来生成共享查询
        mean_x = x.mean(dim=1, keepdim=True).expand(batch_size, self.num_queries, self.embed_dim)
        q = self.W_q(mean_x)

        # 将位置编码添加到共享查询中
        q += self.position_enc[None, :, :]

        # 展开维度以便与键进行全连接操作
        q = q.permute(1, 0, 2)  # [num_queries, batch_size, embed_dim]

        # 计算注意力分数
        attn_logits = q @ k.transpose(-2, -1) * self.scale

        # 应用注意力掩码
        if attention_mask is not None:
            attn_logits = attn_logits.masked_fill(attention_mask == 0, -10000.0)

        # 计算注意力权重
        attn_weights = F.softmax(attn_logits, dim=-1)

        # 应用 dropout
        attn_weights = F.dropout(attn_weights, p=self.dropout, training=self.training)

        # 加权求和
        output = attn_weights @ v

        # 对输出进行线性变换
        output = output.permute(1, 0, 2) @ self.W_out.weight

        return output

# 示例使用
def main():
    embed_dim = 512
    num_queries = 256
    seq_len = 4096
    batch_size = 32

    mq_attn = MultiQueryAttention(embed_dim=512, num_queries=256)
    x = torch.randn(batch_size, seq_len, embed_dim)
    output = mq_attn(x)

    print(f"输入序列长度: {seq_len}")
    print(f"输出序列长度: {output.size(1)}")

if __name__ == "__main__":
    main()
```



# Group Query Attention(GQA)<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#7E45E8;">GQA的核⼼⽬标是减少推理过程中KVcache的内存占⽤和带宽需求</font>**<font style="color:#1f2329;">，这使得其成为⼀种专注 于推理加速的技术，⽽不是⼀种全新的训练⽅法。GQA通过将注意⼒头分组来共享Key和Value矩阵，减少了KV缓存的⼤⼩。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738917339320-08649f9b-5e5d-4df8-9f34-e19bf19bc5e0.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">分组投影</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">若分组数</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">g</font>`<font style="color:rgb(51, 51, 51);">，每组头数</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">h//g</font>`<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">Q:</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">nn.Linear(d_model, h * d_k)</font>`
    - <font style="color:rgb(51, 51, 51);">K, V:</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">nn.Linear(d_model, g * d_k)</font>`
2. **<font style="color:rgb(51, 51, 51);">扩展 K, V</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">每组内重复 K、V：</font>`<font style="color:rgb(51, 51, 51);">K = K.view(batch, n, g, 1, d_k).expand(-1, -1, -1, h//g, -1)</font>`

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**优点**

+ **<font style="color:#117CEE;">推理加速</font>**<font style="color:#1f2329;">：相⽐MQA，GQA通过分组的⽅式允许部分注意⼒头共享Key和Value矩阵，⽽不是所有头都共享，从⽽</font><font style="color:#2ea121;">减少了推理速度和内存需求上的负担，同时保留了更多特征捕捉能⼒</font><font style="color:#1f2329;">。质量接近MHA，⽽速度⼏乎接近MQA。</font>
+ **<font style="color:#117CEE;">调整灵活</font>**<font style="color:#2ea121;">：GQA可以根据模型的需求灵活调整组数</font><font style="color:#1f2329;">。例如，GQA-1相当于MQA，GQA-H则相当于MHA。通过控制组数，模型可以在精度和推理速度之间进⾏权衡，适应不同规模和任务需求。</font>
+ **<font style="color:#245bdb;">内存带宽优化</font>**<font style="color:#245bdb;">：</font><font style="color:#1f2329;">GQA可以</font><font style="color:#2ea121;">有效减少Key和Value矩阵的⼤⼩，减少键值缓存所需的内存带宽</font><font style="color:#1f2329;">。这在处理⼤型模型时尤为重要，因为模型的复杂度随着尺⼨增加⽽急剧上升，GQA的优化使得内存带宽消耗与模型规模更好地成⽐例。</font>

**缺点：**

+ **<font style="color:#ED740C;">精度下降</font>**<font style="color:#ED740C;">：</font><font style="color:#1f2329;">由于所有头共享Key和Value矩阵，模型难以捕捉输⼊数据中复杂和多样化的特征，导致模型性能相⽐MHA有所下降。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">大规模模型推理（如 GPT-4 的变体）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">自适应分组：根据输入动态调整组数。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import math
import torch.nn as nn
import torch.nn.functional as F

class GroupQueryAttention(nn.Module):
    def __init__(self, embed_dim, num_groups=8, num_queries_per_group=32, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_groups = num_groups
        self.num_queries_per_group = num_queries_per_group
        self.dropout = dropout

        # 定义线性变换层
        self.W_q = nn.Linear(embed_dim, embed_dim)
        self.W_k = nn.Linear(embed_dim, embed_dim)
        self.W_v = nn.Linear(embed_dim, embed_dim)

        # 定义共享查询和位置编码
        self.shared_queries = nn.Parameter(torch.randn(num_groups, num_queries_per_group, embed_dim))
        self.position_enc = nn.Parameter(torch.randn(num_groups, embed_dim))

        # 设置缩放因子
        self.scale = 1.0 / math.sqrt(embed_dim)

    def forward(self, x, attention_mask=None):
        batch_size, seq_len, _ = x.size()

        # 划分组
        groups = []
        for i in range(0, seq_len, self.num_queries_per_group):
            groups.append(x[:, i:i + self.num_queries_per_group, :])

        # 处理每个组
        output_groups = []
        for group_idx, group in enumerate(groups):
            # 提取键和值
            k = self.W_k(group)
            v = self.W_v(group)

            # 获得对应的共享查询和位置编码
            q = self.shared_queries[group_idx, :, :]
            q = q.unsqueeze(1).expand(group.size(1), -1, -1)
            q += self.position_enc[group_idx, :].unsqueeze(0).unsqueeze(1)

            # 计算注意力分数
            attn_logits = q @ k.transpose(-2, -1) * self.scale

            # 应用注意力掩码
            if attention_mask is not None:
                pass  # 根据实际需求调整掩码应用方式

            # 计算注意力权重
            attn_weights = F.softmax(attn_logits, dim=-1)

            # 应用 dropout
            attn_weights = F.dropout(attn_weights, p=self.dropout, training=self.training)

            # 加权求和
            group_output = attn_weights @ v

            output_groups.append(group_output)

        # 整合所有组的输出
        output = torch.cat(output_groups, dim=1)

        # 对输出进行线性变换
        output = self.W_q(output)

        return output

# 示例使用
def main():
    embed_dim = 512
    num_groups = 8
    num_queries_per_group = 32
    seq_len = 4096
    batch_size = 32

    gqa_attn = GroupQueryAttention(embed_dim=512, num_groups=8, num_queries_per_group=32)
    x = torch.randn(batch_size, seq_len, embed_dim)
    output = gqa_attn(x)

    print(f"输入序列长度: {seq_len}")
    print(f"输出序列长度: {output.size(1)}")

if __name__ == "__main__":
    main()
```



# Cross Attention
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Cross Attention 是 Transformer 模型中注意力机制的一种扩展，</font>**<font style="color:#ED740C;">主要用于处理两个不同的序列之间的关系</font>**<font style="color:rgb(51, 51, 51);">。与传统的 Self Attention 不同，Cross Attention 不仅关注单个序列内部的信息，还可以利用另一个序列的信息来增强当前序列的表示。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921788090-01e85ef0-c92e-41f6-b93a-6f3ad1871510.png)

:::color5
**<font style="color:#601BDE;">0.Self Attention 对比 Cross Attention</font>**

:::

:::success
**Self Attention**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741922076585-804ee296-2b2c-4df4-ba89-d2aa486f72ce.png)

:::

:::success
**Cross Attention**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921968328-4a18d583-5187-45df-955f-a1e3f4f3b80b.png)

:::

| **<font style="color:rgb(79, 79, 79);">维度</font>** | **<font style="color:rgb(79, 79, 79);">Self Attention</font>** | **<font style="color:rgb(79, 79, 79);">Cross Attention</font>** |
| --- | --- | --- |
| **<font style="color:rgb(79, 79, 79);">输入来源</font>** | <font style="color:rgb(79, 79, 79);">同一序列内的元素（Query、Key、Value）</font> | <font style="color:rgb(79, 79, 79);">不同序列中的元素（Query、Key、Value 不同来源）</font> |
| **<font style="color:rgb(79, 79, 79);">信息交互对象</font>** | <font style="color:rgb(79, 79, 79);">序列中的各个元素相互关注</font> | <font style="color:rgb(79, 79, 79);">序列 A 的元素关注序列 B 中的元素</font> |
| **<font style="color:rgb(79, 79, 79);">应用场景</font>** | <font style="color:rgb(79, 79, 79);">序列内部依赖建模，如句子中的词与词的关联</font> | <font style="color:rgb(79, 79, 79);">跨序列信息建模，如文本到图像、编码器到解码器</font> |
| **<font style="color:rgb(79, 79, 79);">特征捕捉</font>** | <font style="color:rgb(79, 79, 79);">捕捉序列内部的全局依赖</font> | <font style="color:rgb(79, 79, 79);">捕捉不同序列之间的全局依赖</font> |


:::color5
**<font style="color:#601BDE;">1.核心原理</font>**

:::

+ **工作原理：**在 Cross Attention 中，**<font style="color:#74B602;">查询（Query）来自一个序列，而键（Key）和值（Value）来自另一个不同的序列</font>**。这种机制允许模型将一个序列中的信息与另一个序列中的信息进行匹配和关联，**<font style="color:#ED740C;">从而在两个不同的表示之间建立相关性。</font>**
+ **作用：**Cross Attention 主要用于跨模态、跨序列的依赖关系建模。例如，**<font style="color:#ED740C;">在图像和文本匹配任务中，文本的查询可以与图像中的特征进行匹配，从而找到相关的图像区域。</font>**
+ **主要特点：**
    - 信息来源：两个不同序列之间的信息交互，查询来自一个序列，而键和值来自另一个序列。
    - 应用场景：广泛用于需要**<font style="color:#74B602;">跨序列依赖的任务</font>**，例如在 Transformer 解码器中，通过 Cross Attention 机制，解码器的查询会与编码器生成的隐藏状态（作为键和值）进行交互，从而解码生成下一个词语。

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

<font style="color:rgb(25, 27, 31);">在多模态结构中，我们可能</font>**<font style="color:#74B602;">有两个(或多个)</font>**[**<font style="color:#74B602;">Embeddings序列</font>**](https://zhida.zhihu.com/search?content_id=244116480&content_type=Article&match_order=1&q=Embeddings%E5%BA%8F%E5%88%97&zhida_source=entity)**<font style="color:#74B602;"> </font>****<font style="color:#74B602;">S1</font>****<font style="color:#74B602;"> 和 </font>****<font style="color:#74B602;">S2</font>****<font style="color:#74B602;"> 。我们将 </font>****<font style="color:#74B602;">S1</font>****<font style="color:#74B602;"> 作为attention的K,V，将 </font>****<font style="color:#74B602;">S2</font>****<font style="color:#74B602;"> 作为attention的Q。使用Q与K计算注意力权重矩阵，并与V相乘</font>**<font style="color:rgb(25, 27, 31);">，得到：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741922041726-2e85122d-4cec-4ca6-b466-c4cd5986ee08.png)

<font style="color:rgb(51, 51, 51);">具体来说，Cross Attention 的计算过程包括以下几个步骤：</font>

1. **Query、Key 和 Value 的生成**：
    - <font style="color:rgb(51, 51, 51);">对于序列 A，生成 Query（A_q）。</font>
    - <font style="color:rgb(51, 51, 51);">对于序列 B，生成 Key（B_k）和 Value（B_v）。</font>
2. **计算注意力分数**：
    - <font style="color:rgb(51, 51, 51);">使用 Query 和 Key 的点积来计算注意力分数（score）。</font>

```plain
scores = torch.bmm(A_q, B_k.permute(0, 2, 1))
```

3. **归一化**：
    - <font style="color:rgb(51, 51, 51);">对注意力分数进行 Softmax 操作，将其转换为概率分布。</font>

```plain
attention = F.softmax(scores, dim=-1)
```

4. **加权和**：
    - <font style="color:rgb(51, 51, 51);">将注意力权重与序列 B 的 Value 向量进行加权求和，生成最终的输出表示。</font>

```plain
output = torch.bmm(attention, B_v)
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **增强语义理解**：
    - <font style="color:rgb(51, 51, 51);">Cross Attention 通过整合两个序列的信息，能够更全面地理解输入数据，提升语义理解和生成能力。</font>
2. **跨模态信息融合**：
    - <font style="color:rgb(51, 51, 51);">在多模态任务中，Cross Attention 可以有效地整合图像、文本等多种模态的信息，提升模型的表现。</font>
3. **提高任务准确性**：
    - <font style="color:rgb(51, 51, 51);">通过参考另一个序列的信息，Cross Attention 可以在许多任务中提高预测的准确性，如机器翻译和对话生成。</font>
4. **灵活性高**：
    - <font style="color:rgb(51, 51, 51);">Cross Attention 的应用非常广泛，可以用于多种序列处理任务，具有较高的灵活性。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **计算复杂度高**：
    - <font style="color:rgb(51, 51, 51);">与 Self Attention 相比，Cross Attention 的计算量更大，尤其是在处理长序列时，会导致计算资源的消耗增加。</font>
2. **注意力分配问题**：
    - <font style="color:rgb(51, 51, 51);">在某些情况下，模型可能会过度依赖另一个序列的信息，导致注意力分配不均衡，影响自身的特征提取能力。</font>
3. **潜在的信息泄漏**：
    - <font style="color:rgb(51, 51, 51);">在处理某些任务时，Cross Attention 可能会导致信息泄漏，尤其是在需要保护数据隐私的场景中。</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

1. **机器翻译**：
    - <font style="color:rgb(51, 51, 51);">在多语言翻译任务中，Cross Attention 可以利用源语言和目标语言之间的关系，提升翻译质量。</font>
2. **对话生成**：
    - <font style="color:rgb(51, 51, 51);">Cross Attention 可以结合对话历史和当前输入，生成更连贯和相关的回复。</font>
3. **多模态任务**：
    - <font style="color:rgb(51, 51, 51);">在图像描述生成、视频内容理解等任务中，Cross Attention 可以整合视觉和文本信息，提升模型的表现。</font>
4. **文本摘要**：
    - <font style="color:rgb(51, 51, 51);">通过参考外部文献或上下文信息，Cross Attention 可以生成更为全面和准确的摘要。</font>

:::color5
**<font style="color:#601BDE;">5.使用CrossAttention的模型</font>**

:::

1. **T5（Text-to-Text Transfer Transformer）**：
    - <font style="color:rgb(51, 51, 51);">T5 是一种基于 Transformer 的预训练模型，广泛使用 Cross Attention 来处理源文本和目标文本之间的关系，提升文本生成能力。</font>
2. **VisualBERT**：
    - <font style="color:rgb(51, 51, 51);">VisualBERT 是一种用于视觉-语言任务的模型，利用 Cross Attention 整合图像和文本特征，提升图像描述和问答任务的表现。</font>
3. **DALL·E**：
    - <font style="color:rgb(51, 51, 51);">DALL·E 是一个生成文本描述的图像模型，通过 Cross Attention 机制，将文本和图像特征结合起来，生成与文本描述匹配的图像。</font>

:::color5
**<font style="color:#601BDE;">6.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CrossAttention(nn.Module):
    def __init__(self, embed_dim):
        super(CrossAttention, self).__init__()
        self.embed_dim = embed_dim
        self.query_net = nn.Linear(embed_dim, embed_dim)
        self.key_net = nn.Linear(embed_dim, embed_dim)
        self.value_net = nn.Linear(embed_dim, embed_dim)

    def forward(self, query, key, value):
        """
        Args:
            query: (batch_size, seq_len_q, embed_dim)
            key: (batch_size, seq_len_k, embed_dim)
            value: (batch_size, seq_len_k, embed_dim)
        Returns:
            output: (batch_size, seq_len_q, embed_dim)
        """
        # 单词嵌入维度可能不一样，这里假设已经处理一致
        batch_size, seq_len_q, embed_dim = query.size()
        _, seq_len_k, embed_dim = key.size()

        # 线性变换
        A_q = self.query_net(query)
        B_k = self.key_net(key)
        B_v = self.value_net(value)

        # 计算注意力分数
        attention_scores = torch.bmm(A_q, B_k.permute(0, 2, 1))
        attention_scores = attention_scores / torch.sqrt(torch.tensor(embed_dim, dtype=torch.float32))

        # 使用Softmax函数计算注意力权重
        attention_weights = F.softmax(attention_scores, dim=-1)

        # 加权求和得到最终输出
        output = torch.bmm(attention_weights, B_v)

        return output

# 示例使用
batch_size = 2
seq_len_q = 5
seq_len_k = 10
embed_dim = 64

ca = CrossAttention(embed_dim)
query = torch.randn(batch_size, seq_len_q, embed_dim)
key = torch.randn(batch_size, seq_len_k, embed_dim)
value = torch.randn(batch_size, seq_len_k, embed_dim)

# 前向传播
output = ca(query, key, value)

# 打印输出形状
print("Output shape:", output.size())

```



# NSA（Native Sparse Attention） 原生稀疏注意力
:::color3
**<font style="color:rgb(51, 51, 51);">简介：NSA（Native Sparse Attention），</font>**<font style="color:rgb(51, 51, 51);">一种硬件对齐且可训练的稀疏注意力机制，用于解决长上下文建模的高计算成本问题。</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:#ED740C;">通过算术强度平衡算法设计和现代硬件的实现优化，NSA实现了显著的速度提升。</font>**

[Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](https://arxiv.org/pdf/2502.11089)

[Native Sparse Attention解读](https://zhuanlan.zhihu.com/p/24604821449)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104126845-4f85229e-b816-47d8-9929-5c3bb2c460cf.png)

**创新点**

1. **显著的加速效果**<font style="color:#ED740C;">：</font>通过**<font style="color:#74B602;">算法设计和现代硬件实现的优化</font>**，NSA在解码、前向传播和后向传播阶段相比全注意力模型实现了显著的速度提升，特别是在处理64k长序列时。
2. **端到端训练支持**：NSA支持端到端训练，减少了预训练计算量而不牺牲模型性能，使得稀疏注意力模式可以在整个模型生命周期中有效利用。
3. **动态分层稀疏策略**：NSA结合了**<font style="color:#74B602;">粗粒度的token压缩和细粒度的token选择</font>**，既保留了全局上下文感知，又保持了局部精度。
4. **硬件对齐的系统优化**：通过优化块状稀疏注意力以利用Tensor Core和内存访问，确保平衡的算术强度，最大化实际效率。
5. **训练感知的算法设计**：通过高效的算法和后向操作器实现稳定的端到端训练，**<font style="color:#74B602;">支持高效部署和端到端训练</font>**。
6. **全面的实验评估**：在真实世界的语言语料库上进行了综合实验，NSA在一般基准测试、长上下文任务和链式思维推理评估中表现出色，甚至在某些任务上超越了全注意力基线。

:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

<font style="color:rgb(25, 27, 31);">NSA主要解决的问题是长上下文建模的高计算成本问题。标准注意力机制在处理长序列时计算复杂度高，成为模型性能的瓶颈。该问题的研究难点包括：如何在保持模型能力的前提下提高效率，如何实现端到端训练以减少预训练计算量而不牺牲模型性能。该问题的研究相关工作有：</font>[**<font style="color:#2F4BDA;">KV缓存淘汰方法</font>**](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=KV%E7%BC%93%E5%AD%98%E6%B7%98%E6%B1%B0%E6%96%B9%E6%B3%95&zhida_source=entity)**<font style="color:#2F4BDA;">、</font>**[**<font style="color:#2F4BDA;">块状KV缓存选择方法</font>**](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=%E5%9D%97%E7%8A%B6KV%E7%BC%93%E5%AD%98%E9%80%89%E6%8B%A9%E6%96%B9%E6%B3%95&zhida_source=entity)**<font style="color:#2F4BDA;">、</font>**[**<font style="color:#2F4BDA;">采样</font>**](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=%E9%87%87%E6%A0%B7&zhida_source=entity)**<font style="color:#2F4BDA;">、</font>**[**<font style="color:#2F4BDA;">聚类或哈希选择方法</font>**](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=%E8%81%9A%E7%B1%BB%E6%88%96%E5%93%88%E5%B8%8C%E9%80%89%E6%8B%A9%E6%96%B9%E6%B3%95&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等。然而，这些方法在实际部署中往往未能达到理论上的加速效果，且主要集中于推理阶段，缺乏有效的训练时支持。</font>

:::color5
**<font style="color:#601BDE;">2.原理</font>**

:::

<font style="color:rgb(25, 27, 31);">NSA架构通过集成层次化token压缩和块状token选择在可训练架构中，实现了加速训练和推理，同时保持了全注意力性能。NSA在一般基准测试中与全注意力基线匹配，在长上下文评估中超越了建模能力，并在推理能力上得到了增强，同时显著减少了计算延迟并实现了显著的速度提升。</font>

<font style="color:rgb(25, 27, 31);">NSA 取得如此优异的成绩，主要归功于</font>**<font style="color:#74B602;">两项关键创新点</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ <font style="color:rgb(25, 27, 31);">NSA 采用了</font>**<font style="color:#74B602;">原生的稀疏注意力设计</font>**<font style="color:rgb(25, 27, 31);">，这种设计允许在预训练阶段对稀疏模式进行端到端的优化，使得稀疏注意力模块能够与模型的其他组件实现同步适配，从而提升整体性能。</font>
+ <font style="color:rgb(25, 27, 31);">NSA 引入了</font>**<font style="color:#74B602;">分层稀疏注意力机制</font>**<font style="color:rgb(25, 27, 31);">，该机制巧妙地实现了局部信息处理与全局信息处理之间的平衡，为模型处理长文本提供了更高效、更全面的解决方案。</font>

:::color5
**<font style="color:#601BDE;">3.总体算法设计</font>**

:::

<font style="color:rgb(25, 27, 31);">为了利用稀疏模式下的注意力潜力，论文提出用更紧凑且信息密集的表示键值对集合 </font><font style="color:rgb(25, 27, 31);">K</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);"> , </font><font style="color:rgb(25, 27, 31);">V</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);"> 替换注意力机制中的原始键值对 </font><font style="color:rgb(25, 27, 31);">K</font><sub><font style="color:rgb(25, 27, 31);">:t</font></sub><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">V</font><sub><font style="color:rgb(25, 27, 31);">:t</font></sub><sub><font style="color:rgb(25, 27, 31);"> </font></sub><font style="color:rgb(25, 27, 31);">给定每个查询</font>_<font style="color:rgb(25, 27, 31);">qt</font>_<font style="color:rgb(25, 27, 31);">。其中，</font><font style="color:rgb(25, 27, 31);">K</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);"> , </font><font style="color:rgb(25, 27, 31);">V</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);">是基于当前查询</font>_<font style="color:rgb(25, 27, 31);">qt</font>_<font style="color:rgb(25, 27, 31);">和上下文记忆</font><font style="color:rgb(25, 27, 31);">K</font><sub><font style="color:rgb(25, 27, 31);">:t</font></sub><font style="color:rgb(25, 27, 31);"> ，</font><font style="color:rgb(25, 27, 31);">V</font><sub><font style="color:rgb(25, 27, 31);">:t</font></sub><font style="color:rgb(25, 27, 31);">动态构建的。NSA有三种映射策略</font>_<font style="color:rgb(25, 27, 31);">C</font>_<font style="color:rgb(25, 27, 31);">={</font>_<font style="color:rgb(25, 27, 31);">cmp</font>_<font style="color:rgb(25, 27, 31);">,</font>_<font style="color:rgb(25, 27, 31);">slc</font>_<font style="color:rgb(25, 27, 31);">,</font>_<font style="color:rgb(25, 27, 31);">win</font>_<font style="color:rgb(25, 27, 31);">}，分别代表</font>**<font style="color:#74B602;">压缩、选择和滑动窗口</font>**<font style="color:rgb(25, 27, 31);">。 具体来说，正式定义优化后的注意力输出如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104230584-9638b6f5-6455-49b7-a319-f2d8d6ef8b3e.png)

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">步骤 1：压缩（总结词组）</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">NSA 摒弃了对文本中每个单独词汇进行存储的传统方式，而是率先将词组进行压缩，转化为概括性的“块”。我们可以用总结书籍章节的过程来形象理解这一操作。当我们总结书的某一章内容时，不会去逐字记忆每一个词汇，而是提取几个要点来概括关键思想</font>**<font style="color:rgb(25, 27, 31);">。NSA 亦是如此，它把文本中的词组转化为更小、更紧凑的表示形式。通过这种方式，能够有效减少数据量，提高处理效率，同时保留文本的核心信息。</font>

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">步骤 2：选择（挑选重要词</font>**<font style="color:rgb(25, 27, 31);">） 在完成文本压缩之后，NSA 会对其中最相关的词汇进行筛选，以便进行深入处理。</font>**<font style="color:rgb(25, 27, 31);">这一过程类似于我们在阅读文章时，会突出显示那些最重要的句子</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">NSA 并非试图保留文本中的每一处细节，而是依据一定的规则和算法，优先挑选出最具意义的词汇</font>**<font style="color:rgb(25, 27, 31);">。这样做可以聚焦于关键信息，避免在无关紧要的内容上浪费计算资源，从而提升模型对重要信息的处理能力。</font>

**<font style="color:rgb(25, 27, 31);">步骤 3：滑动窗口（保持局部上下文） 尽管 NSA 进行了词组压缩和重要词汇筛选，但为了确保不遗漏词汇之间的关联信息，它仍需要对相邻的词汇进行跟踪。这就如同我们阅读一个复杂句子时，不会仅仅关注其中的主要词汇，还会留意其前后的内容，以获取完整的上下文信息</font>**<font style="color:rgb(25, 27, 31);">。NSA 通过在文本上滑动一个小窗口的方式，来捕获重要的附近信息。这种机制有助于模型更好地理解词汇之间的语义关系，从而在处理长文本时能够做出更准确的判断和分析。 综上所述，NSA 通过压缩、选择和滑动窗口这三个步骤的协同工作，实现了对长文本的高效处理，为大语言模型在处理长文本任务时提供了一种更为有效的解决方案。</font>

:::color5
**<font style="color:#601BDE;">4.动态分层稀疏策略</font>**

:::

<font style="color:rgb(25, 27, 31);">NSA采用动态分层稀疏策略，结合</font>**<font style="color:#74B602;">粗粒度token压缩(Compress)和细粒度token选择(Selection)以及滑动窗口(Sliding Window)</font>**<font style="color:rgb(25, 27, 31);">，以保留全局上下文感知和局部精度。关于明细的部分下面是介绍。NSA 架构采用了分层Token 建模，并通过三个并行的注意力分支处理输入序列,也就是下面的这三个东西。</font>

**<font style="color:rgb(25, 27, 31);">1. 粗粒度压缩注意力 (Compressed Attention)：</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">处理粗粒度的模式，通过压缩 Token 块来捕获全局信息。</font>

**<font style="color:rgb(25, 27, 31);">2. 选择注意力 (Selected Attention)：</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">处理重要的 Token 块，选择性地保留细粒度的信息。</font>

**<font style="color:rgb(25, 27, 31);">3. 滑动窗口注意力 (Sliding Window Attention)：</font>**<font style="color:rgb(25, 27, 31);"> 处理局部上下文信息。</font>

<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">（1）粗粒度压缩（Coarse-grained Compression）：</font>**

<font style="color:rgb(25, 27, 31);">粗粒度压缩通过将连续的token块聚合为块级表示，从而减少需要处理的token数量。具体来说，模型会将一定长度的token块（例如32个token）压缩为一个单一的表示，从而捕获更高层次的语义信息。</font>**<font style="color:#74B602;">这种压缩方式显著减少了计算量，尤其是在处理长序列时，能够有效降低注意力机制的计算复杂度。</font>**下面是粗粒度压缩的计算公式：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104350096-88d408f5-9e8a-4b62-b570-0fc140aca391.png)

<font style="color:rgb(25, 27, 31);">其中，l是块长度，d是相邻块之间的滑动步长，</font>_<font style="color:rgb(25, 27, 31);">φ</font>_<font style="color:rgb(25, 27, 31);">是一个可学习的带内部块位置编码的多层感知器（MLP），用于将块内的键映射到一个压缩后的键。是由压缩键组成的张量。通常，我们采用</font>_<font style="color:rgb(25, 27, 31);">d</font>_<font style="color:rgb(25, 27, 31);">< </font>_<font style="color:rgb(25, 27, 31);">l</font>_<font style="color:rgb(25, 27, 31);">来减轻信息碎片化。对于压缩值表示 </font><font style="color:rgb(25, 27, 31);">V</font><sup><font style="color:rgb(25, 27, 31);">cmp</font></sup><font style="color:rgb(25, 27, 31);"> 也有类似的公式。压缩表示捕捉更粗粒度的更高层次语义信息，并减少注意力的计算负担。</font>

```python
import torch
import torch.nn as nn

class Compression(nn.Module):
    def __init__(self, chunk_size, hidden_size):
        super(Compression, self).__init__()
        self.chunk_size = chunk_size  # 每个块的大小
        self.hidden_size = hidden_size  # 隐藏层大小
        self.pooling = nn.AdaptiveAvgPool1d(1)  # 平均池化层

    def forward(self, x):
        # x: (batch_size, seq_len, hidden_size)
        batch_size, seq_len, hidden_size = x.shape

        # 将序列划分为块
        x = x.view(batch_size, -1, self.chunk_size, hidden_size)  # (batch_size, num_chunks, chunk_size, hidden_size)
        x = x.permute(0, 3, 1, 2)  # (batch_size, hidden_size, num_chunks, chunk_size)
        x = x.reshape(batch_size * hidden_size, -1, self.chunk_size)  # (batch_size * hidden_size, num_chunks, chunk_size)

        # 对每个块进行平均池化
        x = self.pooling(x)  # (batch_size * hidden_size, num_chunks, 1)
        x = x.view(batch_size, hidden_size, -1)  # (batch_size, hidden_size, num_chunks)
        x = x.permute(0, 2, 1)  # (batch_size, num_chunks, hidden_size)

        return x
```

**<font style="color:rgb(25, 27, 31);">(2) 细粒度选择（Fine-grained Selection）：</font>**  
<font style="color:rgb(25, 27, 31);">	细粒度选择则是在压缩的基础上，进一步选择最相关的token块进行注意力计算。通过计算每个块的重要性分数，模型会保留最重要的token块，而忽略那些对当前查询不重要的部分。</font>**<font style="color:#74B602;">这种选择机制确保了模型在处理长序列时，能够保留关键的局部信息，避免因压缩而丢失重要的细节。</font>**<font style="color:rgb(25, 27, 31);">公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104595743-507cae2f-9f2d-4fdd-aedf-56680d49b4a3.png)

<font style="color:rgb(25, 27, 31);">其中， </font><font style="color:rgb(25, 27, 31);">p</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><sup><font style="color:rgb(25, 27, 31);">cmp</font></sup><font style="color:rgb(25, 27, 31);">是压缩键和查询之间的注意力分数。然后选择前</font>_<font style="color:rgb(25, 27, 31);">n</font>_<font style="color:rgb(25, 27, 31);">个最重要的块。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104645469-06622822-abc7-48d5-8e63-920f2b9723f4.png)

```python
import torch
import torch.nn as nn

class Selection(nn.Module):
    def __init__(self, hidden_size, num_selected_chunks):
        super(Selection, self).__init__()
        self.num_selected_chunks = num_selected_chunks  # 选择的块数
        self.scoring = nn.Linear(hidden_size, 1)  # 评分函数

    def forward(self, x):
        # x: (batch_size, num_chunks, hidden_size)
        scores = self.scoring(x).squeeze(-1)  # (batch_size, num_chunks)
        _, selected_indices = torch.topk(scores, self.num_selected_chunks, dim=1)  # 选择前k个块

        # 收集被选中的块
        selected_chunks = torch.gather(x, 1, selected_indices.unsqueeze(-1).expand(-1, -1, x.size(-1)))
        return selected_chunks, selected_indices


输入：x 是压缩后的块级表示，形状为 (batch_size, num_chunks, hidden_size)。
评分：使用线性层计算每个块的重要性分数。
选择：选择分数最高的 num_selected_chunks 个块。
输出：返回被选中的块及其索引。
```

**<font style="color:rgb(25, 27, 31);">(3) 滑动窗口（Sliding Window）：</font>**  
<font style="color:rgb(25, 27, 31);">	滑动窗口机制用于处理局部上下文信息。它保留了最近的token（例如最近的512个token），确保模型在处理当前token时，能够快速适应局部模式的变化。</font>**<font style="color:#74B602;">这种机制防止了模型在压缩和选择过程中被局部模式“短路”，从而确保模型能够同时处理局部和长距离的依赖关系</font>****<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104719850-f1cc9485-5c6b-4d43-ab7e-4af1cadc8982.png)

```python
import torch
import torch.nn as nn

class SlidingWindow(nn.Module):
    def __init__(self, window_size, hidden_size):
        super(SlidingWindow, self).__init__()
        self.window_size = window_size  # 窗口大小
        self.hidden_size = hidden_size  # 隐藏层大小

    def forward(self, x):
        # x: (batch_size, seq_len, hidden_size)
        batch_size, seq_len, hidden_size = x.shape

        # 滑动窗口处理
        windows = x.unfold(1, self.window_size, 1)  # (batch_size, num_windows, window_size, hidden_size)
        windows = windows.reshape(batch_size, -1, self.window_size * hidden_size)  # (batch_size, num_windows, window_size * hidden_size)

        return windows

输入：x 是一个形状为 (batch_size, seq_len, hidden_size) 的张量，表示输入序列。
滑动窗口：使用 unfold 操作生成滑动窗口。
输出：返回滑动窗口处理后的结果，形状为 (batch_size, num_windows, window_size * hidden_size)。
```

<font style="color:rgb(25, 27, 31);">整合前面三个步骤后的代码，请一定要注意，</font>**<font style="color:rgb(25, 27, 31);">上面这三个代码步骤是顺序串联的，先压缩 -> 再选择 --> 最后再滑窗， 但其实这三个东西属于3个不同的注意力机制，实际上是并行执行的。伪代码只是为了方便阅读。</font>**

```python
import torch
import torch.nn as nn

class DynamicSparseAttention(nn.Module):
    def __init__(self, chunk_size, hidden_size, num_selected_chunks, window_size):
        super(DynamicSparseAttention, self).__init__()
        self.compression = Compression(chunk_size, hidden_size)
        self.selection = Selection(hidden_size, num_selected_chunks)
        self.sliding_window = SlidingWindow(window_size, hidden_size)

    def forward(self, x):
        # 压缩
        compressed = self.compression(x)  # (batch_size, num_chunks, hidden_size)

        # 选择
        selected_chunks, _ = self.selection(compressed)  # (batch_size, num_selected_chunks, hidden_size)

        # 滑动窗口
        windows = self.sliding_window(x)  # (batch_size, num_windows, window_size * hidden_size)

        return selected_chunks, windows

输入：x 是一个形状为 (batch_size, seq_len, hidden_size) 的张量，表示输入序列。
压缩：将序列压缩为块级表示。
选择：选择最相关的块。
滑动窗口：处理局部上下文信息。
输出：返回被选中的块和滑动窗口处理后的结果。
```

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">硬件对齐系统</font>**

:::

<font style="color:rgb(25, 27, 31);">为了在训练和预填充期间实现</font>[<font style="color:rgb(9, 64, 142);">FlashAttention</font>](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=FlashAttention&zhida_source=entity)<font style="color:rgb(25, 27, 31);">级别的加速，论文在</font>[<font style="color:rgb(9, 64, 142);">Triton</font>](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=Triton&zhida_source=entity)<font style="color:rgb(25, 27, 31);">上实现了硬件对齐的稀疏注意力内核。优化了块状稀疏注意力以利用Tensor Core和内存访问，确保平衡的算术强度。具体来说有如下几种优化，</font>

**<font style="color:rgb(25, 27, 31);">块状内存访问模式：</font>**<font style="color:rgb(25, 27, 31);">通过合并加载，最大化Tensor Core利用率，减少冗余的KV传输。</font>

**<font style="color:rgb(25, 27, 31);">循环调度</font>**<font style="color:rgb(25, 27, 31);">：在内核中巧妙地安排循环，消除冗余的KV传输。</font>

**<font style="color:rgb(25, 27, 31);">组中心数据加载：</font>**<font style="color:rgb(25, 27, 31);">对于每个内部循环，加载同一组内的所有查询及其共享的稀疏键/值块索引。</font>

**<font style="color:rgb(25, 27, 31);">共享KV获取：</font>**<font style="color:rgb(25, 27, 31);">在内部循环中，顺序加载连续的键/值块到SRAM中，以最小化内存加载。</font>

**<font style="color:rgb(25, 27, 31);">网格调度的外循环：</font>**<font style="color:rgb(25, 27, 31);">由于内部循环长度在不同查询块之间几乎相同，将查询/输出循环放在Triton的网格调度器中，以简化和优化内核。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740104984579-ecf1f874-532c-435a-b3e5-f5ea8f349fa4.png)

<font style="color:rgb(145, 150, 161);">图3 | NSA的内核设计。内核通过GQA组（网格循环）加载查询，获取相应的稀疏键值块（内部循环），并在SRAM上进行注意力计算。绿色块表示SRAM上的数据，蓝色表示HBM上的数据</font>

:::color5
**<font style="color:#601BDE;">6.</font>****<font style="color:#601BDE;">预训练设置</font>**

:::

<font style="color:rgb(25, 27, 31);">遵循最先进的LLM中的常见做法，他们的实验采用结合分组查询注意力</font>**<font style="color:rgb(25, 27, 31);">（GQA）和专家混合（MoE）的主干</font>**<font style="color:rgb(25, 27, 31);">，总</font>**<font style="color:rgb(25, 27, 31);">共有270亿个参数，其中30亿个是活跃参数</font>**<font style="color:rgb(25, 27, 31);">。该模型由30层组成，隐藏维度为2560。对于GQA，我们将组数设置为4，总共64个注意力头。对于每个头，查询、键和值的隐藏维度分别配置为 </font><font style="color:rgb(25, 27, 31);">dq</font><font style="color:rgb(25, 27, 31);"> = </font><font style="color:rgb(25, 27, 31);">dk</font><font style="color:rgb(25, 27, 31);"> =192, </font><font style="color:rgb(25, 27, 31);">dv</font><font style="color:rgb(25, 27, 31);"> =128。对于MoE，</font>**<font style="color:rgb(25, 27, 31);">还是使用</font>**[**<font style="color:rgb(9, 64, 142);">DeepSeekMoE</font>**](https://zhida.zhihu.com/search?content_id=253943015&content_type=Article&match_order=1&q=DeepSeekMoE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">结构，有</font>**<font style="color:rgb(25, 27, 31);">72个路由专家和2个共享专家</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">并将前K个专家设置为6个</font>**<font style="color:rgb(25, 27, 31);">。为了确保训练的稳定性，第一层中的MoE被一个以SwiGLU形式的多层感知器（MLP）替代。</font>

:::color5
**<font style="color:#601BDE;">7.NSA架构参数</font>**

:::

<font style="color:rgb(25, 27, 31);">架构实现了计算成本与模型性能之间的有效权衡。对于NSA，设置</font>**<font style="color:rgb(25, 27, 31);">压缩块大小l=32，</font>**<font style="color:rgb(25, 27, 31);">滑动步长</font>**<font style="color:rgb(25, 27, 31);">d=16</font>**<font style="color:rgb(25, 27, 31);">，选定块大</font>**<font style="color:rgb(25, 27, 31);">小l'=64</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">选定块数量n=16</font>**<font style="color:rgb(25, 27, 31);">（包括固定激活1个初始块和2个局部块），</font>**<font style="color:rgb(25, 27, 31);">以及滑动窗口大小w=512</font>**<font style="color:rgb(25, 27, 31);">。全注意力和稀</font>**<font style="color:rgb(25, 27, 31);">疏注意力模型均在2700亿个令牌的8k长度文本上进行预训练</font>**<font style="color:rgb(25, 27, 31);">，然后在32k长度文本上使用YaRN继续训练并进行有监督微调，以实现长上下文适应。两个模型都训练至完全收敛，以确保公平比较。</font>

:::color5
**<font style="color:#601BDE;">8.评估</font>**

:::

**（1）一般评估**

<font style="color:rgb(25, 27, 31);">在</font>**<font style="color:rgb(25, 27, 31);">MMLU、MMLU-PRO、CMMLU、BBH、GSM8K、MATH、DROP、MBPP和HumanEval</font>**<font style="color:rgb(25, 27, 31);">等基准测试中，NSA在大多数指标上优于全注意力基线，尽管其稀疏性较高。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740105245564-cd556aa8-4a6b-479d-9ef3-3f8e880f8b7b.png)

**（2）长上下文评估**

<font style="color:rgb(25, 27, 31);">在64k上下文的“针尖在干草堆中”测试中，NSA在所有位置上都达到了完美的检索准确率。在LongBench基准测试中，NSA的平均得分为0.469，优于所有基线，包括全注意力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740105353438-7a719480-622f-46c4-a39f-ca57571a10e1.png)

**<font style="color:rgb(25, 27, 31);">（3）链式思维推理评估</font>**

<font style="color:rgb(25, 27, 31);">在AIME指令推理评估中，经过有监督微调后的NSA-R在8k和16k上下文长度下的表现均优于全注意力基线-R。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740105375656-7bfc70cc-50b4-493d-ac04-9e0ae9ea1d08.png)

# MLA (Multihead-Latent-Attention)<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">多头潜在注意力（MLA，Multi-Head Latent Attention）是DeepSeek公司提出的一种改进的注意力机制，旨在提升大型语言模型对文本的理解和生成能力。MLA的核心思想是</font>**<font style="color:#ED740C;">引入潜在空间，通过对文本在潜在空间中的表示，增强模型捕捉语义信息的能力</font>**<font style="color:rgb(51, 51, 51);">，从而提升模型的性能。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740121752045-99272fcc-35c7-4179-bc50-860e90243522.png)

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

**传统attention **:

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737700893631-59482785-ce6c-4e63-ab2c-196b253e7dee.png)

<font style="color:rgb(51, 51, 51);">MLA的工作原理可以分为以下几个步骤：</font>

1. **输入嵌入**：
    - <font style="color:rgb(51, 51, 51);">将输入文本首先转换为词嵌入（Word Embedding），获取每个词的向量表示。</font>
2. **潜在空间映射**：
    - <font style="color:rgb(51, 51, 51);">将词嵌入映射到一个潜在空间，生成潜在向量（Latent Vectors）。这一步通过一个可学习的线性变换实现：L=</font>_<font style="color:rgb(51, 51, 51);">Wl*X。</font>_<font style="color:rgb(51, 51, 51);">  
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



## MLA是如何节约KV-Cache的？
Multi-head Latent Attention (多头潜在注意力，MLA） 中的**<font style="color:#ED740C;">低秩联合压缩是一种对键(Keys）和值 (Values) 进行处理以降低维度、减少存储和计算量的技术。</font>**

:::color5
**<font style="color:#601BDE;">1.低秩联合压缩的含义</font>**

:::

**低秩联合压缩的含义：**

+ 在自注意力机制中，每个位置的查询Q需要与序列中所有位置的键K进行相似度计算得到注意力分数，然后加权值v获得最终的输出值。在传统的多头注意力机制（MHA）中，**<font style="color:#ED740C;">推理阶段需要缓存所有的KV来加速推理，但是这会带来高显存占用问题。</font>**
+ MLA中的低秩联合压缩就是**<font style="color:#74B602;">将输入序列中的键K和值V通过一个下投影矩阵压缩为维度远远小于输入Token维度的压缩潜在向量</font>**。在推理阶段，只需要缓存这些压缩潜在向量，进行注意力计算时，再通过上投影矩阵还原出键和值。
    - **降低向量维度**：将原始的高维词嵌入（如512维）映射到一个低维的潜在空间（如64维）。这直接减少了每个向量占用的内存空间，从而降低了KV-Cache的存储需求。
    - **公式化表示**：![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739868241563-5dd738c1-53e1-43a9-9d5b-9bd6de729ec8.png)

其中，Wl是映射矩阵，X是输入的词嵌入矩阵，L是潜在向量矩阵。

:::color5
**<font style="color:#601BDE;">2.低秩联合压缩的作用</font>**

:::

**低秩联合压缩的作用：**

+ 降低KV缓存占用：显著减少了推理阶段的KV缓存大小。如在DeepSeek-V2中，通过这种方式使缓存参数数量大幅降低，极大缓解了高显存占用问题，使得模型可以支持更大的Batch size和更长的序列长度。
+ 提升推理效率：减少了需要处理和存储的数据量，降低了计算复杂度，从而加快了模型的推理速度，让模型在生成文本等任务时能够更快速地给出结果。
+ 节省计算资源：由于减少了数据处理量，在模型训练和推理过程中，对计算资源的需求也相应降低，降低了对硬件设备的要求，或者在相同硬件条件下可以更高效地运行模型，节省了计算成本。
+ 保证模型性能：通过合理的低秩联合压缩以及配套的解轉ROPE策略等，可以在减少KV缓存和计算量的同时，保证模型对序列中上下文信息的敏感性，使模型性能不受到明显影响，甚至在一些情況下还能有所提升。



# 窗口注意力
**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">将输入划分为局部窗口，仅在窗口内计算自注意力，降低计算复杂度。</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**

1. **<font style="color:rgb(51, 51, 51);">划分窗口</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像分块：</font>`<font style="color:rgb(51, 51, 51);">windows = x.view(B, H//M, M, W//M, M, C)</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">→</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">(B, num_win, M*M, C)</font>`
2. **<font style="color:rgb(51, 51, 51);">窗口内自注意力</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算每个窗口的标准注意力。</font>
3. **<font style="color:rgb(51, 51, 51);">移位窗口</font>**<font style="color:rgb(51, 51, 51);">（可选）：</font>
    - <font style="color:rgb(51, 51, 51);">通过偏移窗口位置促进跨窗口交互。</font>

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">线性复杂度</font>**<font style="color:rgb(51, 51, 51);">：计算量从 O(n²) 降至 O(nM²)。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">局部性限制</font>**<font style="color:rgb(51, 51, 51);">：需移位等机制增强全局交互。</font>

**<font style="color:rgb(51, 51, 51);">应用场景</font>**

+ <font style="color:rgb(51, 51, 51);">高分辨率图像处理（如 Swin Transformer）。</font>

**<font style="color:rgb(51, 51, 51);">改进方法</font>**

+ <font style="color:rgb(51, 51, 51);">层次化窗口：不同层使用不同窗口大小。</font>
+ <font style="color:rgb(51, 51, 51);">跨窗口注意力：引入全局令牌。</font>

<font style="color:rgb(51, 51, 51);"></font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：传统的注意力机制在处理长序列时，需要计算所有位置之间的注意力得分，计算复杂度为O(n²)，其中n为序列长度。窗口注意力机制通过将注意力限制在局部窗口内，显著降低计算复杂度到O(n)或O(n log n)，从而支持长序列的处理。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">划分窗口</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像分块：</font>`<font style="color:rgb(51, 51, 51);">windows = x.view(B, H//M, M, W//M, M, C)</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">→</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">(B, num_win, M*M, C)</font>`
2. **<font style="color:rgb(51, 51, 51);">窗口内自注意力</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算每个窗口的标准注意力。</font>
3. **<font style="color:rgb(51, 51, 51);">移位窗口</font>**<font style="color:rgb(51, 51, 51);">（可选）：</font>
    - <font style="color:rgb(51, 51, 51);">通过偏移窗口位置促进跨窗口交互。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **<font style="color:rgb(51, 51, 51);">计算效率高</font>**<font style="color:rgb(51, 51, 51);">：通过限制注意力窗口的大小，显著降低了计算复杂度，提升处理长序列的效率。</font>
2. **<font style="color:rgb(51, 51, 51);">可扩展性强</font>**<font style="color:rgb(51, 51, 51);">：可以根据硬件资源和任务需求灵活调整窗口大小。</font>
3. **<font style="color:rgb(51, 51, 51);">适合大规模数据</font>**<font style="color:rgb(51, 51, 51);">：适用于需要处理超长序列的场景，如长文本、长视频等。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **<font style="color:rgb(51, 51, 51);">信息损失</font>**<font style="color:rgb(51, 51, 51);">：窗口机制可能导致模型忽略全局信息，影响某些需要全局理解的任务。</font>
2. **<font style="color:rgb(51, 51, 51);">窗口大小选择</font>**<font style="color:rgb(51, 51, 51);">：窗口大小需要根据具体任务进行调整，选择不当可能影响模型表现。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">高分辨率图像处理（如 Swin Transformer）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">层次化窗口：不同层使用不同窗口大小。</font>
+ <font style="color:rgb(51, 51, 51);">跨窗口注意力：引入全局令牌。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

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

