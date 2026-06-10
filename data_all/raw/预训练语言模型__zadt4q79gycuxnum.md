# 预训练语言模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/zadt4q79gycuxnum -->

## <font style="color:#1f2329;">基础</font>
<font style="color:#1f2329;">预训练语⾔模型</font><font style="color:#d83931;">通过在⼤规模⽆监督⽂本数据上进⾏训练，学习语⾔的语法和语义信息</font><font style="color:#1f2329;">。然后，可以将预训练得到的模型应⽤于各种下游任务，如⽂本分类、问答系统等，以提⾼模型的性能。</font>

## <font style="color:#1f2329;">自编码/自回归</font>
<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⾃编码模型（</font><font style="color:#1f2329;">Autoencoding</font><font style="color:#1f2329;">Models</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;">：</font><font style="color:#1f2329;">如</font><font style="color:#1f2329;">BERT</font><font style="color:#1f2329;">，使⽤双向上下⽂信息</font><font style="color:#1f2329;">，通过重建被遮蔽的输⼊</font><font style="color:#1f2329;">来学习语⾔表⽰。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">⾃回归模型（AutoregressiveModels）：如GPT，使⽤单向上下⽂信息，基于前⾯的词预测下⼀个词。</font>



## Prefix LM/Causal LM/Encoder-Decoder 对比
:::color3
目前，**<font style="color:#ED740C;">Causal LM (Decoder-only) </font>**架构已经成为大模型领域的绝对统治者。原因主要有两点：

1. Scaling Law 的胜利： 实验证明，当数据量和参数量足够大时，Decoder-only 架构的“理解能力短板”会被弥补，而其在生成方面的优势会被无限放大。
2. 工程实现的统一： Decoder-only 结构最简单，便于硬件优化和分布式训练。  
虽然 DeepSeek R1 等模型在强化推理能力，但其底层架构依然是基于 Causal LM 的，这再次印证了该架构作为“通用底座”的强大生命力。

:::

| 特性 | Causal LM (Decoder-only) | Encoder-Decoder | Prefix LM |
| --- | --- | --- | --- |
| 注意力机制 | 单向 (Left-to-Right) | Encoder双向 + Decoder单向 | Prefix双向 + Target单向 |
| 核心优势 | 生成能力、扩展性 (Scaling) | 理解能力、序列映射 | 兼顾理解与生成、填空 |
| 主要短板 | 上下文理解略逊于双向 | 训练效率、参数冗余 | 实现复杂、生态略小 |
| 代表模型 | GPT-4, LLaMA, DeepSeek | T5, BART | GLM |
| 当前地位 | 绝对主流 (统治级) | 特定领域 (翻译/学术) | 独特赛道 |


#### 1. Causal LM (Decoder-only)
代表模型： GPT 系列 (GPT-3, GPT-4), LLaMA, Qwen, DeepSeek V3  
核心机制： 单向注意力机制（Unidirectional Attention）。模型在预测下一个 token 时，只能看到当前 token 之前的信息（从左到右），无法看到后面的信息。

+ ✅ 优点：
    - 生成能力最强： 天生契合“自回归生成”任务，非常擅长开放式文本生成、续写。
    - 训练效率高： 结构简单，在超大规模数据下表现出极强的 Scaling Law（扩展定律），参数利用率高。
    - 泛化能力强： 在 Zero-shot（零样本）和 Few-shot（少样本）场景下表现优异，无需针对特定任务微调即可处理多种任务。
+ ❌ 缺点：
    - 上下文理解受限： 由于是单向注意力，模型在处理输入时无法像双向模型那样同时利用上下文（即无法利用“未来”的信息来辅助理解“现在”的信息），在某些强理解任务（如分类、抽取）上理论上弱于双向模型。
+ 🎯 适用场景：
    - 开放式文本生成（创意写作、代码生成）。
    - 对话系统（Chatbot）。
    - 通用任务处理（目前的主流架构）。

#### 2. Encoder-Decoder (Seq2Seq)
代表模型： T5, BART, Google Translate (原始 Transformer)  
核心机制： 包含两个部分。Encoder 采用双向注意力（Bidirectional Attention），可以看到整个输入序列；Decoder 采用单向注意力，负责生成输出。

+ ✅ 优点：
    - 理解能力极强： Encoder 的双向机制使其能完美理解输入文本的全局语义，不会出现“读了后面忘前面”或“只能看左边”的问题。
    - 序列到序列映射精准： 非常适合输入和输出有明确对应关系的任务。
+ ❌ 缺点：
    - 训练/推理成本较高： 需要同时维护两个大模块，在相同参数量下，训练和推理的计算复杂度通常高于 Decoder-only。
    - 开放生成稍弱： 在纯粹的开放式创作（不依赖特定输入）场景下，表现通常不如 Causal LM 自然。
+ 🎯 适用场景：
    - 机器翻译（Translation）：这是该架构的起源，也是最强项。
    - 文本摘要（Summarization）：需要深刻理解原文才能生成摘要。
    - 文本复述/改写。

#### 3. Prefix LM (非因果 Decoder / Hybrid)
代表模型： GLM (General Language Model), U-PaLM  
核心机制： 这是一种“混合”架构，通常是在 Decoder-only 的架构上通过修改 Attention Mask 来实现。  
它将输入分为 Prefix（前缀） 和 Target（目标） 两部分。

+ Prefix 部分： 采用双向注意力（像 Encoder 一样，Token 之间可以互相看见）。
+ Target 部分： 采用单向注意力（像 Decoder 一样，只能看左边）。
+ ✅ 优点：
    - 博采众长： 试图结合 Encoder 的理解能力（前缀部分双向可见）和 Decoder 的生成能力。
    - 填空能力强： 特别适合做“完形填空”类型的任务（In-filling），即根据上下文预测中间缺失的内容。
+ ❌ 缺点：
    - 实现复杂度： 相比纯粹的 Causal LM，其 Attention Mask 的设计和 KV Cache 的管理更为复杂。
    - 生态兼容性： 目前主流推理框架对纯 Causal LM 优化最好，Prefix LM 有时需要额外的适配工作。
+ 🎯 适用场景：
    - 文本填空/修补（In-filling）。
    - 既需要强理解又需要生成的任务。

## <font style="color:rgb(53, 53, 53);">Bert</font>
:::color3
**<font style="color:#ED740C;">原理</font>**<font style="color:#1f2329;">：BERT (BidirectionalEncoderRepresentationsfromTransformers) 是基于 Transformer架构的预训 练模型。其核⼼在于利⽤ Transformer模型中的 编码器 (Encoder)部分，通过双向（从左到右、从右到左）的上下⽂信息来理解句⼦中的词语。因此，BERT 能够更好地捕捉语⾔的语义关系，⼴泛应⽤于⾃然语⾔处理 (NLP) 任务。</font>

:::

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">BERT 的 base 版本 有 110M 参数（12 层、768 隐藏单元、12 个注意⼒头）。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">large 版本 则有 340M 参数（24 层、1024 隐藏单元、16 个注意⼒头）。</font>

<font style="color:#1f2329;">BERT 的预训练采⽤了Adam 优化器，初始学习率经过 10,000 步的warm-up 后逐渐衰减，总共进⾏了超过 33 亿个训练样本、100 万步的训练过程。</font>

:::color5
**<font style="color:#601BDE;">1.结构</font>**

:::

#### 嵌入层
#### ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908497661-70fb3bd0-d77e-45cf-8b46-b9a90c8e047f.png)
1. <font style="color:#ED740C;">WordPiece</font><font style="color:#2ea121;"> </font><font style="color:#1f2329;">：</font><font style="color:#2ea121;">BERT 使⽤ WordPiece 作为分词⽅法 ，将单词划分为⼦词单元。</font><font style="color:#1f2329;">这 种处理⽅式既能处理未知词汇，⼜能提⾼模型的灵活性和泛化能⼒。例如，罕见或不规则单词会被分成更常见的⼦词单位，进⽽能够在训练中更好地学习到词汇语义。</font>
2. <font style="color:#ED740C;">位置嵌入position embedding（绝对位置编码）</font><font style="color:#1f2329;">：由于 BERT 只使⽤Transformer 的编码器部分，并不依赖于序列化结构（如 RNN 或 LSTM），因此它⽆法从输⼊序列中⾃然地获取位置信息。为了弥补这⼀点，</font><font style="color:#2ea121;">BERT 通过位置嵌⼊为每个词汇添加了位置特征</font><font style="color:#1f2329;">，使模型能够感知词汇在序列中的相对位置。BERT 初始化了⼀个位置嵌⼊矩阵，并在训练过程中学习这些位置向量。</font>
3. <font style="color:#ED740C;">段落嵌入 segment embedding</font><font style="color:#1f2329;">：在 BERT 中，</font><font style="color:#2ea121;">输⼊通常是两个句⼦拼接⽽成，特别是在句⼦预测任务 (NextSentencePrediction, NSP) </font><font style="color:#1f2329;">中。因此，BERT为输⼊中的每个 token添加⼀个段落嵌⼊，⽤来区分句⼦ A 和句⼦B，帮助模型更好地理解句⼦之间的关系。</font>

**为什么三个embedding可以直接相加？**

1. <font style="color:rgb(51, 51, 51);">互补性特征与线性叠加</font>

<font style="color:rgb(51, 51, 51);">Token Embeddings</font><font style="color:rgb(51, 51, 51);">：表示词本身的语义信息（如词向量）。</font>

<font style="color:rgb(51, 51, 51);">Position Embeddings</font><font style="color:rgb(51, 51, 51);">：编码词在序列中的位置关系（如绝对位置或相对位置）。</font>

<font style="color:rgb(51, 51, 51);">Segment Embeddings</font><font style="color:rgb(51, 51, 51);">：区分不同句子（如问答任务中的问题和答案）。</font>

<font style="color:rgb(51, 51, 51);">这三类嵌入分别从语义、位置和句子边界三个维度提供互补信息。直接相加可以看作一种特征融合方式，允许模型在训练过程中动态调整各部分的权重，最终形成一个统一的表示。尽管相加是线性操作，但后续的 Transformer 层（尤其是自注意力机制）会通过非线性变换学习特征的交互。</font>

1. <font style="color:rgb(51, 51, 51);">维度一致性</font>

<font style="color:rgb(51, 51, 51);">三个嵌入的维度相同（例如 BERT-base 为 768 维），相加操作在数学上是合法的，且不会破坏向量空间的几何结构。如果采用拼接（concatenation）会显著增加输入维度，导致后续的 Transformer 层参数爆炸（如拼接后维度为 768×3=2304），而相加保持了维度不变，计算更高效。</font>

1. <font style="color:rgb(51, 51, 51);">梯度传播的稳定性</font>

<font style="color:rgb(51, 51, 51);">相加操作对梯度的反向传播更友好。在反向传播时，梯度可以直接均分到三个嵌入矩阵中，避免了拼接操作可能导致的梯度不均衡问题。实验表明，相加的收敛效果更好，而拼接可能引入额外的噪声。</font>

#### 编码器层
<font style="color:#1f2329;">BERT的主要结构是基于 Transformer的编码器部分，通过堆叠多层编码器来实现深度语义学习。Transformer编码器包含⼏个核⼼部分：</font><font style="color:#d83931;background-color:#fbbfbc;">多头注意力+LayerNorm + 前馈层 + LayerNorm</font>

<font style="color:#1f2329;">在 BERT-base 中，每个⾃注意⼒头的输出维度是 64（总维度为768），⽽多头注意⼒机制则是将 12个⾃注意⼒头的输出拼接 (concatenate) 后，再通过⼀个线性层处理，形成最终的多头注意⼒输出。</font>

#### <font style="color:#1f2329;">预训练任务</font>
<font style="color:#1f2329;">BERT </font><font style="color:#1f2329;">在⼤规模语料上通过⾃监督学习进</font><font style="color:#1f2329;">⾏了预训练</font><font style="color:#1f2329;">，主要包括两个任务：</font>

1. <font style="color:#de7802;">MaskedLanguageModel(MLM)</font><font style="color:#1f2329;">：</font>

<font style="color:#1f2329;">BERT </font><font style="color:#1f2329;">通过随机掩盖 </font><font style="color:#1f2329;">(mask) </font><font style="color:#1f2329;">句⼦中</font><font style="color:#1f2329;">15% </font><font style="color:#1f2329;">的 </font><font style="color:#1f2329;">token</font><font style="color:#1f2329;">，并要求模型根据上下⽂预测这些被掩盖的词。</font><font style="color:#1f2329;">具体操作是：</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">80%</font><font style="color:#1f2329;">⽤</font><font style="color:#1f2329;">[MASK] </font><font style="color:#1f2329;">替换 </font><font style="color:#1f2329;">token</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">10% </font><font style="color:#1f2329;">⽤随机 </font><font style="color:#1f2329;">token </font><font style="color:#1f2329;">替换。</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">10% </font><font style="color:#1f2329;">保持原 </font><font style="color:#1f2329;">token </font><font style="color:#1f2329;">不变。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">这种策略既能防⽌模型只依赖 </font><font style="color:#1f2329;">[MASK]</font><font style="color:#1f2329;">进⾏猜测</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，同时保证了模型的泛化能⼒。</font>

**<font style="color:#117CEE;">示意</font>**<font style="color:#117CEE;">：</font>

```python
1输⼊序列："我爱[MASK]天"
2模型预测："我爱北京天"
```

**<font style="color:#2b2f36;">特点：</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><u><font style="color:#2ea121;">双向性</font></u><font style="color:#1f2329;">：模型可以同时利⽤左侧和右侧的上下⽂信息。</font>

<font style="color:#1456f0;">•  </font><u><font style="color:#2ea121;">信息泄露问题</font></u><font style="color:#1f2329;">：在训练过程中，模型可以看到被遮蔽词的未来信息，这在⽣成任务中不适⽤。</font>

**<font style="color:#1f2329;">应用场景</font>**<font style="color:#1f2329;">：理解任务，如⽂本分类、问答匹配等。</font>

2. <font style="color:#de7802;">Next Sentence Prediction (NSP)</font><font style="color:#1f2329;">：</font>

<font style="color:#1f2329;">BERT 通过给定两个句⼦，要求模型判断这两个句⼦是否为连续上下句。这⼀任务帮助 BERT 学习句⼦间的关系，提⾼在问答、推理等任务中的表现。语料中50%的句⼦，选择其相应的下⼀句⼀起形成上下句，作为正样本；其余50%的句⼦随机选择⼀句⾮下⼀句⼀起形成上下句，作为负样本。这种 设定，有利于sentence-level tasks，例如问答。</font>

#### 实现
<font style="color:rgb(51, 51, 51);">首先，我们需要定义BERT模型的架构。BERT的基本组件主要包括嵌入层、编码器和输出层。</font>

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BertConfig:
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads, ff_size, max_position_embeddings, dropout):
        self.vocab_size = vocab_size          # 词汇表大小
        self.hidden_size = hidden_size        # 隐藏层维度
        self.num_layers = num_layers          # 编码器层数
        self.num_heads = num_heads            # 注意力头数
        self.ff_size = ff_size                # 前馈网络隐藏层大小
        self.max_position_embeddings = max_position_embeddings  # 最大位置嵌入数
        self.dropout = dropout                # dropout比率

class BertEmbeddings(nn.Module):
    def __init__(self, config):
        super(BertEmbeddings, self).__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.hidden_size)  # 词嵌入
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)  # 位置嵌入
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, input_ids):
        seq_length = input_ids.size(1)  # 获取序列长度
        position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device).unsqueeze(0).expand(input_ids.size(0), -1)  # 生成位置ID
        embeddings = self.word_embeddings(input_ids) + self.position_embeddings(position_ids)  # 加上位置嵌入
        return self.dropout(embeddings)

class MultiHeadAttention(nn.Module):
    def __init__(self, hidden_size, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.num_heads = num_heads
        self.head_size = hidden_size // num_heads  # 每个头的维度
        self.query linear = nn.Linear(hidden_size, hidden_size)
        self.key linear = nn.Linear(hidden_size, hidden_size)
        self.value linear = nn.Linear(hidden_size, hidden_size)
        self.output linear = nn.Linear(hidden_size, hidden_size)

    def forward(self, x):
        batch_size, seq_length, hidden_size = x.size()
        # 线性变换得到Q, K, V
        queries = self.query_linear(x).view(batch_size, seq_length, self.num_heads, self.head_size).transpose(1, 2)
        keys    = self.key_linear(x).view(batch_size, seq_length, self.num_heads, self.head_size).transpose(1, 2)
        values  = self.value_linear(x).view(batch_size, seq_length, self.num_heads, self.head_size).transpose(1, 2)

        scores = torch.matmul(queries, keys.transpose(-2, -1)) / (self.head_size ** 0.5)  # 计算注意力分数
        attention_weights = F.softmax(scores, dim=-1)  # 计算softmax
        context = torch.matmul(attention_weights, values)  # 得到上下文向量

        context = context.transpose(1, 2).contiguous().view(batch_size, seq_length, hidden_size)  # 合并头
        return self.output_linear(context)  # 线性变换得到输出

class FeedForward(nn.Module):
    def __init__(self, hidden_size, ff_size):
        super(FeedForward, self).__init__()
        self.linear1 = nn.Linear(hidden_size, ff_size)
        self.linear2 = nn.Linear(ff_size, hidden_size)

    def forward(self, x):
        return self.linear2(F.relu(self.linear1(x)))

class BertLayer(nn.Module):
    def __init__(self, config):
        super(BertLayer, self).__init__()
        self.attention = MultiHeadAttention(config.hidden_size, config.num_heads)
        self.ffn = FeedForward(config.hidden_size, config.ff_size)
        self.layer_norm1 = nn.LayerNorm(config.hidden_size)
        self.layer_norm2 = nn.LayerNorm(config.hidden_size)
        self.dropout1 = nn.Dropout(config.dropout)
        self.dropout2 = nn.Dropout(config.dropout)

    def forward(self, x):
        attn_output = self.attention(x)  # 计算注意力
        x = self.layer_norm1(x + self.dropout1(attn_output))  # 残差连接和层归一化
        ffn_output = self.ffn(x)
        return self.layer_norm2(x + self.dropout2(ffn_output))  # 再次残差连接和层归一化

class BertModel(nn.Module):
    def __init__(self, config):
        super(BertModel, self).__init__()
        self.embeddings = BertEmbeddings(config)
        self.encoder = nn.ModuleList([BertLayer(config) for _ in range(config.num_layers)])  # 堆叠多个编码器层

    def forward(self, input_ids):
        x = self.embeddings(input_ids)
        for layer in self.encoder:
            x = layer(x)  # 逐层编码
        return x

# 配置BERT模型参数
config = BertConfig(
    vocab_size=30522,  # BERT的词汇表大小
    hidden_size=768,  # BERT的隐藏层维度
    num_layers=12,  # BERT的编码器层数
    num_heads=12,  # 每层的多头数量
    ff_size=3072,  # 前馈网络的隐藏层大小
    max_position_embeddings=512,  # 位置嵌入最大长度
    dropout=0.1  # dropout比率
)

# 实例化BERT模型
model = BertModel(config)
```

+ <font style="color:rgb(51, 51, 51);">数据集定义</font>

<font style="color:rgb(51, 51, 51);">接下来，我们需要定义一个数据集。我们将创建一个假数据集以展示如何加载数据。</font>



## <font style="color:rgb(53, 53, 53);">GLM（</font><font style="color:rgb(51, 51, 51);">General Language Model</font><font style="color:rgb(53, 53, 53);">）</font>
[https://blog.51cto.com/u_16116809/6288905](https://blog.51cto.com/u_16116809/6288905)

**原理**：<font style="color:#d83931;">GLM的⾃回归空⽩填充⽅法是在输⼊序列中引⼊空⽩ ，让模型以⾃回归的⽅式逐步填充这些空⽩。</font>

**示意**：

```python
步骤1：输⼊序列"我爱  [ ]天"
步骤2：填充过程：
步骤3：预测"北" =>"我爱  北   [ ]天"
步骤4：预测"京" => "我爱  北京  天"
```

**特点：**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><u><font style="color:#2ea121;"> </font></u><u><font style="color:#2ea121;">⾃回归填充</font></u><font style="color:#1f2329;">：模型以⾃左向右的⽅式</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">逐步预测并填充空⽩</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">•  </font><u><font style="color:#2ea121;">统⼀的⽣成和理解</font></u><font style="color:#1f2329;">：同时适⽤于⾃然语⾔理解和⽣成任务。</font>

**<font style="color:#1f2329;">应用场景</font>**<font style="color:#1f2329;">：兼顾理解和⽣成任务，如机器翻译、⽂本摘要等。</font>

**<font style="color:#1f2329;">优点：</font>**

+ <font style="color:#1f2329;">更好的上下文建模：GLM通过⾃回归的⽅式，能够更好地捕捉上下⽂之间的依赖关系，提升对⻓距离依赖的建模能⼒。</font>
+ <font style="color:#1f2329;">统一的框架：GLM采⽤统⼀的预训练任务，兼容了⾃编码和⾃回归模型的优势，使其在多种下游任务中表现出⾊。</font>
+ <font style="color:#1f2329;">避免信息泄露：⾃回归的填充⽅式确保模型在预测时只利⽤过去的信息，避免了MLM⽅法中可能存在的信息泄露问题。</font>
+ <font style="color:#1f2329;">提升泛化能力：由于GLM在预训练时需要预测连续的空⽩序列，模型被迫学习更深层次的语⾔结构和语义信息，从⽽提升了泛化能⼒。</font>

**与Bert的区别**

+ **训练目标：**<font style="color:#1f2329;">BERT的MLM：重建被遮蔽的词，训练⽬标是最⼤化被遮蔽词的概率。GLM的⾃回归填充：预测空⽩处的词序列，训练⽬标是最⼤化空⽩填充序列的概率。</font>
+ **<font style="color:#1f2329;">上下文利用</font>**<font style="color:#1f2329;">：BERT：利⽤双向上下⽂，但存在信息泄露的问题。GLM：以⾃回归⽅式填充，避免了信息泄露。</font>
+ **<font style="color:#1f2329;">应用范围</font>**<font style="color:#1f2329;">：BERT：主要⽤于理解任务，如⽂本分类、问答匹配等。GLM：兼顾理解和⽣成任务，如机器翻译、⽂本摘要等。</font>



