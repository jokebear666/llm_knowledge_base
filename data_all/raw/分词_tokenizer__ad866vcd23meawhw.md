# 分词 tokenizer

<!-- source: yuque://zhongxian-iiot9/hlyypb/ad866vcd23meawhw -->

# 简介
<font style="color:#1f2329;">Tokenizer的训练是NLP模型构建中关键的⼀步。通过理解不同分词算法的原理和训练过程，我们可以根据具体需求选择合适的Tokenizer，提⾼模型的性能和效率。⽆论是BPE的简单⾼效，WordPiece的概率优化，还是Unigram模型的全局视角，都各有其适⽤场景。</font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;">在⾃然语⾔处理（NLP）领域，Tokenizer（分词器）是将原始⽂本转换为模型可处理的基本单位（即词元或Token）的⼯具。Tokenizer的训练对于模型的性能和效率⾄关重要。</font>

<font style="color:#1456f0;">1.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">计算机对⽂本的处理需求：计算机⽆法直接</font><font style="color:#1f2329;">理解⼈类语⾔</font><font style="color:#1f2329;">，需要将⽂本转换为数值形式才能处理。</font>

<font style="color:#1456f0;">2.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">模型输⼊的标准化：将不规则的⾃然语⾔转换为标准化的</font><font style="color:#1f2329;">Token</font><font style="color:#1f2329;">序列</font><font style="color:#1f2329;">，便于模型学习。</font>

<font style="color:#1456f0;">3.  </font><font style="color:#1f2329;">降低数据稀疏性：通过合理的分词，可以减少词汇量，降低模型复杂度，提⾼训练效率。</font>

<font style="color:#1f2329;"></font>

## 基本概念
<font style="color:#1456f0;">1.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">Token</font><font style="color:#1f2329;">（词元</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;">：</font><font style="color:#1f2329;">⽂本被分割后的最⼩单位</font><font style="color:#1f2329;">，可能是字符、词或⼦词。</font>

<font style="color:#1456f0;">2.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">词汇表（</font><font style="color:#1f2329;">Vocabulary</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;">：</font><font style="color:#1f2329;">所有</font><font style="color:#1f2329;">Token</font><font style="color:#1f2329;">的集合</font><font style="color:#1f2329;">，模型只能处理</font><font style="color:#1f2329;">词汇表中的</font><font style="color:#1f2329;">Token</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">3.  </font><font style="color:#1f2329;">⼦词（Subword）：介于字符和词之间的单位，⽤于解决新词和低频词的问题。</font>

## <font style="color:#1f2329;">Token</font>
"token"是一个基本的单位，用于表示文本数据。具体来说，token可以是一个单词、一个子词，甚至是一个字符，具体取决于所使用的分词方法（tokenization method）。以下是token的一些关键概念：

1. **分词（Tokenization）**：在处理文本之前，首先需要将其转换为tokens。这一过程称为分词。不同的模型和应用程序可能采用不同的分词策略。例如，GPT系列模型主要使用的是基于子词的分词方法，这意味着常见的词会被作为单一token处理，而不常见的词可能会被分解成多个部分进行处理。
2. **语义单元**：每个token可以视为语义的最小单元。通过将文本分解为tokens，模型能够在训练和推理时更有效地处理语言。
3. **模型输入**：在LLM中，输入文本通常被转换成一系列tokens，这些tokens会被映射到模型的嵌入空间。例如，"hello"这个词可能会被转换为一个特定的token ID，然后用于模型的输入。
4. **长度限制**：大型语言模型通常有一个最大token数量的限制，这意味着输入文本的长度受到限制。这一点在实际使用中非常重要，因为超过该限制的文本会被截断或处理方式不同。
5. **上下文理解**：模型通过处理tokens及其上下文，可以理解和生成语言。多个tokens结合在一起，模型可以从中提取语义信息，做出推理或生成新的文本。

<font style="color:#1f2329;"></font>

## 传统分词方法的局限
1. <font style="color:#1f2329;">基于词的分词：将⽂本按空格或标点分割，</font><font style="color:#d83931;">但⽆法处理新词、拼写错误或形态变化，导致⼤量的未登录词（OOV）</font><font style="color:#1f2329;">。</font>
2. <font style="color:#1f2329;">基于字符的分词：将每个字符作为⼀个Token，</font><font style="color:#245bdb;">词汇表⼩，但序列⻓度过⻓，模型难以捕获⻓距离依赖。</font>



## <font style="color:#1f2329;">output_token 比 input_token 价格贵的原因？</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在大模型中，</font>**<font style="color:rgb(51, 51, 51);">输出Token通常比输入Token更贵</font>**<font style="color:rgb(51, 51, 51);">，主要原因涉及计算方式、资源消耗、模型架构以及商业定价策略。</font>

+ **<font style="color:rgb(51, 51, 51);">输出Token更贵的原因</font>**<font style="color:rgb(51, 51, 51);">：自回归生成、串行计算、显存带宽瓶颈、商业定价。</font>
+ **<font style="color:rgb(51, 51, 51);">输入Token成本可控</font>**<font style="color:rgb(51, 51, 51);">：并行处理、优化技术成熟（如FlashAttention）。</font>
+ **<font style="color:rgb(51, 51, 51);">实际影响</font>**<font style="color:rgb(51, 51, 51);">：在对话、创作等生成密集型任务中，输出Token占总成本主导地位；在检索、分类等任务中，输入Token成本可能更高。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算方式与资源消耗</font>**

:::

1. **输入Token的处理（并行计算）**
    - <font style="color:rgb(51, 51, 51);">输入Token在训练和推理阶段通常以</font>**<font style="color:rgb(51, 51, 51);">批处理（batch）形式一次性并行处理</font>**<font style="color:rgb(51, 51, 51);">，尤其是Transformer的前向传播过程中，所有输入Token同时参与计算。</font>
    - <font style="color:rgb(51, 51, 51);">例如，在训练时，输入序列通过自注意力机制并行生成隐藏表示，计算复杂度为 O(n</font><sup><font style="color:rgb(51, 51, 51);">2</font></sup><font style="color:rgb(51, 51, 51);">)（n为序列长度），但GPU/TPU的并行计算能力可以高效处理。</font>
2. **输出Token的生成（自回归串行生成）**
    - <font style="color:rgb(51, 51, 51);">在生成任务（如文本生成）中，输出Token是</font>**<font style="color:rgb(51, 51, 51);">逐个生成</font>**<font style="color:rgb(51, 51, 51);">的，每个新Token依赖之前所有Token的上下文。</font>
    - <font style="color:rgb(51, 51, 51);">每个输出Token需要一次完整的前向传播（即模型解码），导致计算量与输出长度呈线性增长（复杂度 O(n⋅d)，d为模型维度）。</font>
    - **<font style="color:rgb(51, 51, 51);">显存带宽瓶颈</font>**<font style="color:rgb(51, 51, 51);">：每次生成Token时需加载整个模型参数到显存，显存带宽成为性能瓶颈，大幅增加延迟和计算成本。</font>

:::color5
**<font style="color:#601BDE;">2.模型架构的影响</font>**

:::

1. **键值缓存（KV Cache）的维护**
    - <font style="color:rgb(51, 51, 51);">在生成阶段，Transformer通过缓存已生成Token的键值向量（KV Cache）加速后续生成，但缓存会随输出长度增长占用更多显存。</font>
    - **<font style="color:#ED740C;">输入Token只需处理一次，而输出Token需逐步扩展缓存</font>**<font style="color:rgb(51, 51, 51);">，导致显存压力更大。</font>
2. **长上下文处理的挑战**
    - <font style="color:rgb(51, 51, 51);">输入Token较长时（如数万Token），模型需维护庞大的注意力矩阵，可能触发显存不足问题。但此类场景较少，且可通过稀疏注意力等技术优化。</font>
    - <font style="color:rgb(51, 51, 51);">输出Token的生成无法完全避免串行计算，优化空间有限。</font>

:::color5
**<font style="color:#601BDE;">3.训练与推理阶段的差异</font>**

:::

1. **训练阶段**
    - <font style="color:rgb(51, 51, 51);">输入和输出Token均以批处理形式并行计算，两者的计算成本差异较小。</font>
    - <font style="color:rgb(51, 51, 51);">例如，在训练GPT时，前向传播同时处理输入和输出，反向传播统一更新权重。</font>
2. **推理阶段**
    - <font style="color:rgb(51, 51, 51);">输入Token处理仅需一次前向传播，而输出Token需多次自回归生成，耗费更多计算资源。</font>
    - **<font style="color:rgb(51, 51, 51);">延迟敏感</font>**<font style="color:rgb(51, 51, 51);">：生成100个输出Token可能需要100次模型调用，而处理100个输入Token只需1次调用。</font>

:::color5
**<font style="color:#601BDE;">4.商业定价策略</font>**

:::

<font style="color:rgb(51, 51, 51);">主流API服务（如OpenAI、Anthropic）通常</font>**<font style="color:rgb(51, 51, 51);">对输出Token定价更高</font>**<font style="color:rgb(51, 51, 51);">，反映其实际成本差异：</font>

+ **<font style="color:rgb(51, 51, 51);">OpenAI</font>**<font style="color:rgb(51, 51, 51);">：GPT-4输入Token价格为</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">30</font><font style="color:rgb(51, 51, 51);">/</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">M</font><font style="color:rgb(51, 51, 51);">，输出</font><font style="color:rgb(51, 51, 51);">T</font><font style="color:rgb(51, 51, 51);">o</font><font style="color:rgb(51, 51, 51);">k</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">为</font><font style="color:rgb(51, 51, 51);">30/1</font>_<font style="color:rgb(51, 51, 51);">M</font>_<font style="color:rgb(51, 51, 51);">，输出</font>_<font style="color:rgb(51, 51, 51);">T</font>__<font style="color:rgb(51, 51, 51);">o</font>__<font style="color:rgb(51, 51, 51);">k</font>__<font style="color:rgb(51, 51, 51);">e</font>__<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);">为</font><font style="color:rgb(51, 51, 51);">60/1M（两倍于输入）。</font>
+ **<font style="color:rgb(51, 51, 51);">Anthropic Claude 3</font>**<font style="color:rgb(51, 51, 51);">：输入Token</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">15</font><font style="color:rgb(51, 51, 51);">/</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">M</font><font style="color:rgb(51, 51, 51);">，输出</font><font style="color:rgb(51, 51, 51);">T</font><font style="color:rgb(51, 51, 51);">o</font><font style="color:rgb(51, 51, 51);">k</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">15/1</font>_<font style="color:rgb(51, 51, 51);">M</font>_<font style="color:rgb(51, 51, 51);">，输出</font>_<font style="color:rgb(51, 51, 51);">T</font>__<font style="color:rgb(51, 51, 51);">o</font>__<font style="color:rgb(51, 51, 51);">k</font>__<font style="color:rgb(51, 51, 51);">e</font>__<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);">75/1M（五倍于输入）。</font>

<font style="color:rgb(51, 51, 51);">这种定价差异直接源于输出Token生成所需的更高计算资源。</font>

:::color5
**<font style="color:#601BDE;">5.实践建议</font>**

:::

<font style="color:rgb(51, 51, 51);">在实际应用中，可通过</font>**<font style="color:#74B602;">限制输出长度、优化输入压缩（如摘要）来降低成本</font>**<font style="color:rgb(51, 51, 51);">。</font>

# 分词方法
:::color3
**<font style="color:#1f2329;">简介</font>**<font style="color:#1f2329;">：⼦词分词在字符级和词级之间找到平衡，通过将词拆分为更⼩的⼦词单位，解决新词和低频词的问题</font>

1. <font style="color:#1f2329;">处理未登录词：新词可由已知⼦词组合⽽成。</font>
2. <font style="color:#1f2329;">减少词汇表大小：共享⼦词，降低模型参数量。</font>
3. <font style="color:#1f2329;">提高模型泛化能力：更好地捕获词的形态和词缀信息。</font>

:::

| **算法** | **合并策略** | **词汇表大小** | **多语言支持** | **典型应用模型** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">BPE</font> | <font style="color:rgb(51, 51, 51);">频率优先</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">有限</font> | <font style="color:rgb(51, 51, 51);">GPT-2</font> |
| <font style="color:rgb(51, 51, 51);">BBPE</font> | <font style="color:rgb(51, 51, 51);">字节级频率</font> | <font style="color:rgb(51, 51, 51);">小</font> | <font style="color:rgb(51, 51, 51);">强</font> | <font style="color:rgb(51, 51, 51);">主流大模型</font> |
| <font style="color:rgb(51, 51, 51);">WordPiece</font> | <font style="color:rgb(51, 51, 51);">似然增益</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">BERT</font> |
| <font style="color:rgb(51, 51, 51);">Unigram</font> | <font style="color:rgb(51, 51, 51);">概率剪枝</font> | <font style="color:rgb(51, 51, 51);">灵活</font> | <font style="color:rgb(51, 51, 51);">强</font> | <font style="color:rgb(51, 51, 51);">XLNet</font> |


## <font style="color:#6425d0;">Byte Pair Encoding（BPE）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">BPE最初⽤于数据压缩，其在NLP中的应⽤是：从字符开始，迭代地合并频率最⾼的相邻符号对，构建⼦词词汇表。</font>

:::

:::color5
**<font style="color:#601BDE;">1.训练步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">初始化</font>**<font style="color:rgb(51, 51, 51);">：将文本拆分为字符序列，统计字符频率。</font>
2. **<font style="color:rgb(51, 51, 51);">统计符号对</font>**<font style="color:rgb(51, 51, 51);">：计算所有相邻符号对的频率。</font>
3. **<font style="color:rgb(51, 51, 51);">合并最高频对</font>**<font style="color:rgb(51, 51, 51);">：合并频率最高的符号对，更新词汇表。</font>
4. **<font style="color:rgb(51, 51, 51);">重复合并</font>**<font style="color:rgb(51, 51, 51);">：重复步骤2-3，直到达到目标词汇表大小。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:#117CEE;">优点：</font>**<font style="color:#1f2329;">简单⾼效，易于实现，适⽤于多种语⾔。</font>

**<font style="color:#117CEE;">缺点：</font>**<font style="color:#1f2329;">合并基于频率，未考虑词的语义信息。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">GPT-2、RoBERTa</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">引入特殊符号处理罕见词。</font>
+ <font style="color:rgb(51, 51, 51);">动态调整合并策略（如加权频率）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from collections import defaultdict

def get_stats(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[(symbols[i], symbols[i+1])] += freq
    return pairs

def merge_vocab(pair, vocab):
    v_out = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in vocab:
        w_new = word.replace(bigram, replacement)
        v_out[w_new] = vocab[word]
    return v_out

# 示例训练过程
vocab = {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w e s t </w>': 6}
num_merges = 10
for i in range(num_merges):
    pairs = get_stats(vocab)
    if not pairs:
        break
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
print("BPE Vocab:", vocab.keys())

```



## 
<font style="color:#1f2329;"></font>

## <font style="color:#6425d0;">BBPE（Byte-LevelBPE）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><u><font style="color:#2ea121;">BBPE是BPE的字节级扩展版本，主要应⽤于多语⾔模型（如GPT等）和处理Unicode字符的场景。</font></u><font style="color:#1f2329;">与标准BPE不同，</font>**<font style="color:#ED740C;">BBPE操作在字节层⾯</font>**<font style="color:#1f2329;">，⽽不是字符层⾯，这允许它以更加通⽤的⽅式处理任意编码的⽂本（包括⾮拉丁字⺟）。</font>

<font style="color:rgb(51, 51, 51);">BBPE将文本编码为UTF-8字节序列后应用BPE，词汇表仅需256个字节+合并符号，解决多语言和罕见字符问题。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">字节编码</font>**<font style="color:rgb(51, 51, 51);">：将文本转换为UTF-8字节序列。</font>
2. **<font style="color:rgb(51, 51, 51);">BPE合并</font>**<font style="color:rgb(51, 51, 51);">：在字节级别执行标准BPE合并。</font>

<font style="color:#1f2329;">与</font><font style="color:#1f2329;">BPE</font><font style="color:#1f2329;">类似</font><font style="color:#1f2329;">，不同之处在于：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">输⼊的不是字符序列</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，⽽是</font><font style="color:#2ea121;">UTF-8</font><font style="color:#2ea121;">字节序列</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">在</font><font style="color:#2ea121;">字节层⾯</font><font style="color:#1f2329;">合并频繁出现的字节对。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738899452688-383da6b3-bc19-4edc-9c75-166c098605da.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">简单高效</font>**<font style="color:rgb(51, 51, 51);">：实现简单，计算速度快。</font>
+ **<font style="color:rgb(51, 51, 51);">生成流畅</font>**<font style="color:rgb(51, 51, 51);">：通常生成的文本较为连贯和有意义。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">缺乏多样性</font>**<font style="color:rgb(51, 51, 51);">：总是选择概率最高的词，可能导致生成内容缺乏多样性和创新性。</font>
+ **<font style="color:rgb(51, 51, 51);">忽略全局最优</font>**<font style="color:rgb(51, 51, 51);">：可能因为局部最优而导致全局生成效果不理想。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

**<font style="color:#117CEE;">主流大模型都使用应用BBPE</font>**

+ <font style="color:#1f2329;">多语言统一性：随着模型规模的扩⼤，</font><font style="color:#2ea121;">⽀持多种语⾔和字符集成为必然需求</font><font style="color:#1f2329;">。BBPE通过在字节层</font>

<font style="color:#1f2329;">⾯的操作，能够避免各语⾔tokenization不⼀致的问题。</font>

+ <font style="color:#1f2329;">字符通用性：由于BBPE可以</font><font style="color:#2ea121;">处理所有Unicode字符</font><font style="color:#1f2329;">，能够⽆缝处理⾮拉丁字符和特殊符号，具备更好的通⽤性。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">混合字符-字节编码；优化字节序列处理。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
# 使用HuggingFace Tokenizers库（底层为字节处理）
from tokenizers import ByteLevelBPETokenizer

tokenizer = ByteLevelBPETokenizer()
tokenizer.train(files=["text.txt"], vocab_size=5000)
tokenizer.save("tokenizer.json")

```









## <font style="color:#6425d0;">WordPiece</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">WordPiece最初⽤于⾕歌的机器翻译系统，与BPE类似，但在合并时考虑了语⾔模型的概率。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">初始化</font>**<font style="color:rgb(51, 51, 51);">：拆分文本为字符。</font>
2. **<font style="color:rgb(51, 51, 51);">计算合并得分</font>**<font style="color:rgb(51, 51, 51);">：对每个符号对，计算合并后的似然增益。</font>
3. **<font style="color:rgb(51, 51, 51);">合并最优对</font>**<font style="color:rgb(51, 51, 51);">：选择增益最大的对合并。</font>
4. **<font style="color:rgb(51, 51, 51);">迭代</font>**<font style="color:rgb(51, 51, 51);">：重复直到达到目标词汇表大小。</font>

**<font style="color:#117CEE;">详细训练步骤：</font>**

<font style="color:#1456f0;">1.  </font><font style="color:#2ea121;">初始化：</font><font style="color:#1f2329;">将语料库中的词分解为字符序列。</font>

<font style="color:#1456f0;">2.  </font><font style="color:#2ea121;">统计⼦词频率：</font><font style="color:#1f2329;">计算所有可能的⼦词（初始为字符） 的出现频率。</font>

<font style="color:#1456f0;">3.  </font><font style="color:#2ea121;">估计⼦词概率：</font><font style="color:#1f2329;">根据频率估计每个⼦词的概率   其中 </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">s</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">是⼦词 </font><font style="color:#1f2329;">s</font><font style="color:#1f2329;">的频率 ， </font><font style="color:#1f2329;">N</font><font style="color:#1f2329;">是总的⼦词数。</font>

<font style="color:#1456f0;">4.  </font><font style="color:#2ea121;">迭代合并⼦词：</font><font style="color:#1f2329;">步骤概览：在每次迭代中，尝试合并所有可能的相邻⼦词对，</font><font style="color:#d83931;">计算合并后对语料库总概率的影响，选择能最⼤化语料库概率的合并。</font>

<font style="color:#1456f0;">5.</font><font style="color:#1456f0;">  </font><font style="color:#2ea121;">计算每个合并候选的得分</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⽬标：找到能够最⼤化语料库对数概率</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">L </font><font style="color:#1f2329;">的合并。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">语料库对数概率</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">⋅</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">log</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">P</font><font style="color:#1f2329;">   </font><font style="color:#1f2329;">其中 </font><font style="color:#1f2329;">S</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">是所有⼦词的集合。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">合并后对数概率的增益（得分）：</font>

<font style="color:#1f2329;">ΔL = [f (ab) ⋅ log P(ab)] − [f (a) ⋅ log P(a) + f (b) ⋅ log P(b)]</font>

<font style="color:#1f2329;">-</font><font style="color:#1f2329;">a </font><font style="color:#1f2329;">和</font><font style="color:#1f2329;">b</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">是待合并的⼦词。</font>

<font style="color:#1f2329;">-</font><font style="color:#1f2329;">ab</font><font style="color:#1f2329;">是合并后的新⼦词。</font>

<font style="color:#1f2329;">-</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">a</font><font style="color:#1f2329;">) </font><font style="color:#1f2329;">、</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">b</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">、</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">ab</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">是对应</font><font style="color:#1f2329;">⼦词的频率。</font>

<font style="color:#1456f0;">6.  </font><font style="color:#2ea121;">选择最佳合并：</font><font style="color:#1f2329;">选择使 </font><font style="color:#1f2329;">Δ</font><font style="color:#1f2329;">L</font><font style="color:#1f2329;">最⼤的⼦词对进⾏合并。</font>

<font style="color:#1456f0;">7.</font><font style="color:#1456f0;">  </font><font style="color:#2ea121;">更新⼦词频率和概率</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">更新合并后的⼦词频率</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">ab</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">从频率表中移除</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">a</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">和 </font><font style="color:#1f2329;">f</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">b</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">重新计算⼦词概率。</font>

<font style="color:#1456f0;">8.  </font><font style="color:#2ea121;">重复迭代：</font><font style="color:#1f2329;">重复步骤5-7 ，直到达到预设的词汇表⼤⼩或没有合适的合并。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:#117CEE;">优点：</font>**<font style="color:#1f2329;">考虑了语⾔模型的概率 ，提⾼了分词的合理性。</font>

**<font style="color:#117CEE;">缺点：</font>**<font style="color:#1f2329;">计算复杂度⾼ ，训练时间较⻓。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">BERT、DistilBERT</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
# 使用HuggingFace实现
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
text = "unaffable"
tokens = tokenizer.tokenize(text)  # ['un', '##aff', '##able']

```







<font style="color:#1f2329;"></font>

## <font style="color:#6425d0;">Unigram语⾔模型</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">基于Unigram（⼀元）语⾔模型，将分词视为对词汇表概率分布的估计。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:#117CEE;">训练步骤：</font>**

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">初始化词汇表：包含所有可能的⼦词。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">估计⼦词概率：基于语料库 ，计算每个⼦词的概率。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">词汇表优化：</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">计算损失：基于当前词汇表的⼦词概率，计算模型的损失。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">移除低概率⼦词：删除对损失影响最⼩的⼦词，缩⼩词汇表。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">重复：迭代优化词汇表 ，直到达到预设⼤⼩。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:#117CEE;">优点：</font>**<font style="color:#1f2329;">全局优化 ，考虑了⼦词的整体概率分布。</font>

**<font style="color:#117CEE;">缺点：</font>**<font style="color:#1f2329;">需要⼤量计算资源 ，训练复杂度⾼。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">XLNet、ALBERT</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">混合初始化策略；引入稀疏性约束。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from collections import Counter
import math

class UnigramTokenizer:
    def __init__(self, vocab_size=1000):
        self.vocab_size = vocab_size
        self.vocab = []

    def train(self, texts):
        # 简化的训练过程：统计子词频率
        subword_counts = Counter()
        for text in texts:
            for i in range(len(text)):
                for j in range(i+1, len(text)+1):
                    subword_counts[text[i:j]] += 1
        # 保留top-k子词
        self.vocab = [sw for sw, cnt in subword_counts.most_common(self.vocab_size)]

tokenizer = UnigramTokenizer(vocab_size=100)
tokenizer.train(["hello world", "unigram tokenizer"])
print("Unigram Vocab:", tokenizer.vocab[:10])

```



<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

