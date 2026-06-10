# 文本编码器

<!-- source: yuque://zhongxian-iiot9/hlyypb/bx2zdgwzc62a3tv6 -->

# 基于
<font style="color:#1f2329;">预训练语⾔模型</font><font style="color:#d83931;">通过在⼤规模⽆监督⽂本数据上进⾏训练，学习语⾔的语法和语义信息</font><font style="color:#1f2329;">。然后，可以将预训练得到的模型应⽤于各种下游任务，如⽂本分类、问答系统等，以提⾼模型的性能。</font>

## <font style="color:rgb(1, 1, 1);">大模型/小模型的区别</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">以下从多个角度对大语言模型（以Qwen为例）和小模型（以BERT为例）进行对比。</font>

+ **<font style="color:rgb(51, 51, 51);">大模型（Qwen）</font>**<font style="color:rgb(51, 51, 51);">：追求</font>**<font style="color:#ED740C;">通用性和生成能力</font>**<font style="color:rgb(51, 51, 51);">，依赖海量数据和算力，适合复杂开放任务。</font>
+ **<font style="color:rgb(51, 51, 51);">小模型（BERT）</font>**<font style="color:rgb(51, 51, 51);">：专注于</font>**<font style="color:#ED740C;">特定场景的高效微调</font>**<font style="color:rgb(51, 51, 51);">，资源友好，适合结构化理解任务。</font>

:::

<font style="color:#1f2329;">与传统模型相比，大模型的主要区别包括：</font>

1. **模型规模**<font style="color:#1f2329;">：大模型的参数量远超传统模型。传统模型通常具有较少的参数，结构相对简单。</font>
2. **数据需求**<font style="color:#1f2329;">：大模型需要大量的数据进行训练，以避免过拟合并充分利用其复杂性；而传统模型可以在相对较小的数据集上进行训练。</font>
3. **表现能力**<font style="color:#1f2329;">：大模型在许多任务上能够实现更高的准确性和泛化能力，尤其是在处理复杂问题时。传统模型可能在特定的任务上表现良好，但在通用性上稍显不足。</font>
4. **计算资源**<font style="color:#1f2329;">：由于规模庞大，大模型通常需要强大的计算资源和长时间的训练，而传统模型在计算需求上相对较低。</font>
5. **迁移学习**<font style="color:#1f2329;">：大模型通常具有更好的迁移学习能力，可以通过微调在不同的任务上实现较好的性能，而传统模型往往需要针对特定任务进行重新训练。</font>

:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

| **维度** | **Qwen（大模型）** | **BERT（小模型）** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">提出时间</font>** | <font style="color:rgb(51, 51, 51);">2023年</font> | <font style="color:rgb(51, 51, 51);">2018年</font> |
| **<font style="color:rgb(51, 51, 51);">背景目标</font>** | <font style="color:rgb(51, 51, 51);">面向通用任务（生成、推理、多模态等）</font> | <font style="color:rgb(51, 51, 51);">面向自然语言理解任务（分类、实体识别等）</font> |
| **<font style="color:rgb(51, 51, 51);">技术趋势</font>** | <font style="color:rgb(51, 51, 51);">大模型参数爆炸，追求通用性和零样本能力</font> | <font style="color:rgb(51, 51, 51);">Transformer早期应用，推动预训练+微调范式</font> |


:::color5
**<font style="color:#601BDE;">2.创新点</font>**

:::

| **维度** | **Qwen** | **BERT** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">核心技术</font>** | <font style="color:rgb(51, 51, 51);">超大规模参数（千亿级）、支持多模态输入</font> | <font style="color:rgb(51, 51, 51);">双向Transformer、掩码语言模型（MLM）</font> |
| **<font style="color:rgb(51, 51, 51);">训练方法</font>** | <font style="color:rgb(51, 51, 51);">稀疏注意力、混合精度训练、分布式训练优化</font> | <font style="color:rgb(51, 51, 51);">掩码语言模型（MLM）+ 下一句预测（NSP）任务</font> |
| **<font style="color:rgb(51, 51, 51);">应用扩展</font>** | <font style="color:rgb(51, 51, 51);">零样本/少样本学习、多轮对话、代码生成</font> | <font style="color:rgb(51, 51, 51);">微调适配下游任务，解决传统RNN的长距离依赖问题</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **维度** | **Qwen** | **BERT** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据规模</font>** | <font style="color:rgb(51, 51, 51);">数十TB级，涵盖多语言、代码、网页、书籍等</font> | <font style="color:rgb(51, 51, 51);">数十GB级（BooksCorpus + 英文Wikipedia）</font> |
| **<font style="color:rgb(51, 51, 51);">数据多样性</font>** | <font style="color:rgb(51, 51, 51);">多领域、多模态（文本+结构化数据）</font> | <font style="color:rgb(51, 51, 51);">纯文本，单一语言（英语为主）</font> |
| **<font style="color:rgb(51, 51, 51);">数据清洗</font>** | <font style="color:rgb(51, 51, 51);">复杂去噪、质量过滤、多语言对齐</font> | <font style="color:rgb(51, 51, 51);">基于规则的基础清洗</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

| **维度** | **Qwen** | **BERT** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">参数量</font>** | <font style="color:rgb(51, 51, 51);">千亿级（如Qwen-72B）</font> | <font style="color:rgb(51, 51, 51);">亿级（BERT-base: 110M）</font> |
| **<font style="color:rgb(51, 51, 51);">层数</font>** | <font style="color:rgb(51, 51, 51);">80+层</font> | <font style="color:rgb(51, 51, 51);">12层（BERT-base）</font> |
| **<font style="color:rgb(51, 51, 51);">注意力机制</font>** | <font style="color:rgb(51, 51, 51);">稀疏注意力（降低计算复杂度）</font> | <font style="color:rgb(51, 51, 51);">标准多头注意力（12头）</font> |
| **<font style="color:rgb(51, 51, 51);">结构设计</font>** | <font style="color:rgb(51, 51, 51);">Decoder-Only（自回归生成）</font> | <font style="color:rgb(51, 51, 51);">Encoder-Only（双向上下文建模）</font> |


:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

| **维度** | **Qwen** | **BERT** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">预训练</font>** | <font style="color:rgb(51, 51, 51);">超大规模分布式训练（数千张GPU）</font> | <font style="color:rgb(51, 51, 51);">单机多卡训练（TPU/GPU集群）</font> |
| **<font style="color:rgb(51, 51, 51);">训练目标</font>** | <font style="color:rgb(51, 51, 51);">自回归生成（预测下一个词）</font> | <font style="color:rgb(51, 51, 51);">掩码语言模型（MLM）+ 下一句预测（NSP）</font> |
| **<font style="color:rgb(51, 51, 51);">微调</font>** | <font style="color:rgb(51, 51, 51);">通常不微调，直接通过提示词（Prompt）使用</font> | <font style="color:rgb(51, 51, 51);">必须微调适配下游任务</font> |
| **<font style="color:rgb(51, 51, 51);">资源消耗</font>** | <font style="color:rgb(51, 51, 51);">百万美元级算力成本</font> | <font style="color:rgb(51, 51, 51);">千美元级算力成本</font> |


:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **维度** | **Qwen** | **BERT** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">优点</font>** | <font style="color:rgb(51, 51, 51);">通用性强、零样本能力、支持复杂生成任务</font> | <font style="color:rgb(51, 51, 51);">轻量高效、易微调、适合资源受限场景</font> |
| **<font style="color:rgb(51, 51, 51);">缺点</font>** | <font style="color:rgb(51, 51, 51);">训练/推理成本高、可控性差、存在幻觉风险</font> | <font style="color:rgb(51, 51, 51);">生成能力弱、依赖标注数据、任务泛化能力有限</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

| **维度** | **Qwen** | **BERT** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">典型场景</font>** | <font style="color:rgb(51, 51, 51);">智能对话（Chat）、代码生成、创作辅助</font> | <font style="color:rgb(51, 51, 51);">文本分类、实体识别、语义相似度计算</font> |
| **<font style="color:rgb(51, 51, 51);">落地领域</font>** | <font style="color:rgb(51, 51, 51);">开放域问答、教育、客服、多模态交互</font> | <font style="color:rgb(51, 51, 51);">搜索引擎、广告推荐、金融风控</font> |
| **<font style="color:rgb(51, 51, 51);">适用对象</font>** | <font style="color:rgb(51, 51, 51);">大型企业、云服务提供商</font> | <font style="color:rgb(51, 51, 51);">中小企业、学术研究</font> |


## <font style="color:#1f2329;">自编码/自回归</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:#1f2329;">⾃编码模型（AutoEncoding）：如BERT，使⽤双向上下⽂信息，通过重建被遮蔽的输⼊来学习语⾔表⽰。</font>
+ <font style="color:#1f2329;">回归模型（AutoRegressive）：如GPT，使⽤单向上下⽂信息，基于前⾯的词预测下⼀个词。</font>

:::

**<font style="color:rgb(51, 51, 51);">选择建议</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">需文本理解（如分类、问答）→</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">自编码</font>**
+ <font style="color:rgb(51, 51, 51);">需文本生成（如创作、翻译）→</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">自回归</font>**
+ <font style="color:rgb(51, 51, 51);">复杂任务（如文档摘要）→ </font>**<font style="color:rgb(51, 51, 51);">混合架构（编码-解码）</font>**

:::color5
**<font style="color:#601BDE;">1.核心思想</font>**

:::

| **类型** | **自编码（如BERT）** | **自回归（如GPT）** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">目标</font>** | **<font style="color:rgb(51, 51, 51);">重建输入数据</font>**<font style="color:rgb(51, 51, 51);">：通过部分损坏的输入（如掩码）恢复完整信息</font> | **<font style="color:rgb(51, 51, 51);">序列生成</font>**<font style="color:rgb(51, 51, 51);">：基于历史信息预测下一个词</font> |
| **<font style="color:rgb(51, 51, 51);">方向性</font>** | **<font style="color:rgb(51, 51, 51);">双向上下文建模</font>**<font style="color:rgb(51, 51, 51);">：可同时利用前后文信息</font> | **<font style="color:rgb(51, 51, 51);">单向上下文建模</font>**<font style="color:rgb(51, 51, 51);">：仅依赖左侧历史信息（从左到右）</font> |


:::color5
**<font style="color:#601BDE;">2.模型结构</font>**

:::

| **类型** | **自编码** | **自回归** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">架构</font>** | <font style="color:rgb(51, 51, 51);">编码器（Encoder-only）</font> | <font style="color:rgb(51, 51, 51);">解码器（Decoder-only）</font> |
| **<font style="color:rgb(51, 51, 51);">注意力机制</font>** | <font style="color:rgb(51, 51, 51);">全双向注意力（可看到全部位置）</font> | <font style="color:rgb(51, 51, 51);">因果注意力（仅能看到当前位置及左侧位置）</font> |
| **<font style="color:rgb(51, 51, 51);">典型模型</font>** | <font style="color:rgb(51, 51, 51);">BERT、RoBERTa、ALBERT</font> | <font style="color:rgb(51, 51, 51);">GPT系列、LLaMA、PaLM</font> |


:::color5
**<font style="color:#601BDE;">3.训练目标</font>**

:::

| **类型** | **自编码** | **自回归** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">预训练任务</font>** | **<font style="color:rgb(51, 51, 51);">掩码语言建模（MLM）</font>**<font style="color:rgb(51, 51, 51);">：随机掩码输入词，预测被掩码的词</font> | **<font style="color:rgb(51, 51, 51);">语言建模（LM）</font>**<font style="color:rgb(51, 51, 51);">：最大化序列似然，逐词预测下一个词</font> |
| **<font style="color:rgb(51, 51, 51);">数学形式</font>** | <font style="color:rgb(51, 51, 51);">P(xmasked∥xobserved)</font> | <font style="color:rgb(51, 51, 51);">P</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">x</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">∥</font><font style="color:rgb(51, 51, 51);">x</font><font style="color:rgb(51, 51, 51);"><</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">P</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">x</font>__<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">∥</font>_<font style="color:rgb(51, 51, 51);">x</font>_<font style="color:rgb(51, 51, 51);"><</font>_<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">（自左向右生成）</font> |
| **<font style="color:rgb(51, 51, 51);">训练效率</font>** | <font style="color:rgb(51, 51, 51);">并行计算（所有词同时预测）</font> | <font style="color:rgb(51, 51, 51);">串行生成（逐词预测，训练可并行但推理需串行）</font> |


:::color5
**<font style="color:#601BDE;">5.生成目标</font>**

:::

| **类型** | **自编码** | **自回归** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">生成方式</font>** | <font style="color:rgb(51, 51, 51);">非生成式设计，需额外结构（如连接解码器）</font> | <font style="color:rgb(51, 51, 51);">天然支持生成任务（如文本续写、对话）</font> |
| **<font style="color:rgb(51, 51, 51);">可控性</font>** | <font style="color:rgb(51, 51, 51);">适合填充、改写等局部编辑任务</font> | <font style="color:rgb(51, 51, 51);">适合长文本生成，但可能偏离目标（幻觉风险）</font> |
| **<font style="color:rgb(51, 51, 51);">流畅性</font>** | <font style="color:rgb(51, 51, 51);">生成文本可能不连贯（因训练目标非生成导向）</font> | <font style="color:rgb(51, 51, 51);">生成文本连贯性强</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

| **类型** | **自编码** | **自回归** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">典型任务</font>** | <font style="color:rgb(51, 51, 51);">- 文本分类   </font><font style="color:rgb(51, 51, 51);">- 实体识别   </font><font style="color:rgb(51, 51, 51);">- 语义相似度</font> | <font style="color:rgb(51, 51, 51);">- 文本生成   </font><font style="color:rgb(51, 51, 51);">- 对话系统   </font><font style="color:rgb(51, 51, 51);">- 代码生成</font> |
| **<font style="color:rgb(51, 51, 51);">优势领域</font>** | **<font style="color:rgb(51, 51, 51);">理解型任务</font>**<font style="color:rgb(51, 51, 51);">：需深度上下文语义建模</font> | **<font style="color:rgb(51, 51, 51);">生成型任务</font>**<font style="color:rgb(51, 51, 51);">：需创造性或长文本输出</font> |
| **<font style="color:rgb(51, 51, 51);">局限性</font>** | <font style="color:rgb(51, 51, 51);">生成能力弱，需微调适配生成任务</font> | <font style="color:rgb(51, 51, 51);">理解复杂语义时可能不足（如推理任务）</font> |


## <font style="color:#1f2329;">Encoder & Decoder & Encoder-Decoder 对比</font>
## `Encoder-Decoder`、`Language model`和`Prefix LM`对比
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741164725407-cc8bd3bd-ed3f-4fed-b355-8e0beb2e99d1.png)

## 大模型embedding VS 小模型embedding
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">BERT</font>**<font style="color:rgb(51, 51, 51);">：更适合需要双向上下文理解的任务，通过微调获得高性能。</font>
+ **<font style="color:rgb(51, 51, 51);">LLM</font>**<font style="color:rgb(51, 51, 51);">：在零样本场景和生成任务中表现优越，但需设计合理的Embedding提取策略。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理与结构差异</font>**

:::

1. **BERT的Embedding生成原理**：
    - **<font style="color:rgb(51, 51, 51);">模型结构</font>**<font style="color:rgb(51, 51, 51);">：基于Transformer编码器，使用双向自注意力机制。</font>
    - **<font style="color:rgb(51, 51, 51);">预训练任务</font>**<font style="color:rgb(51, 51, 51);">：Masked Language Model (MLM) 和 Next Sentence Prediction (NSP)。</font>
    - **<font style="color:rgb(51, 51, 51);">Embedding来源</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * **<font style="color:rgb(51, 51, 51);">Token-level</font>**<font style="color:rgb(51, 51, 51);">：每个token的隐藏状态（最后一层或多层平均）。</font>
        * **<font style="color:rgb(51, 51, 51);">Sentence-level</font>**<font style="color:rgb(51, 51, 51);">：通常取[CLS] token的隐藏状态作为句子表示，或通过池化（平均/最大池化）所有token的隐藏状态。</font>
2. **LLM（如Qwen）的Embedding生成原理**：
    - **<font style="color:rgb(51, 51, 51);">模型结构</font>**<font style="color:rgb(51, 51, 51);">：基于Transformer解码器，使用单向自注意力（仅关注左侧上下文）。</font>
    - **<font style="color:rgb(51, 51, 51);">预训练任务</font>**<font style="color:rgb(51, 51, 51);">：自回归语言建模（预测下一个token）。</font>
    - **<font style="color:rgb(51, 51, 51);">Embedding来源</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">通常取最后一层所有token的隐藏状态，或最后一个token的隐藏状态作为序列表示（需根据任务调整）。</font>

:::color5
**<font style="color:#601BDE;">2.计算步骤对比</font>**

:::

1. **BERT的计算流程**：
    - **<font style="color:rgb(51, 51, 51);">输入处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">添加特殊token：[CLS]（句首）和 [SEP]（分隔符）。</font>
        * <font style="color:rgb(51, 51, 51);">Tokenization后生成</font>`<font style="color:rgb(51, 51, 51);">input_ids</font>`<font style="color:rgb(51, 51, 51);">和</font>`<font style="color:rgb(51, 51, 51);">attention_mask</font>`<font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:rgb(51, 51, 51);">前向传播</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
outputs = model(input_ids, attention_mask)
last_hidden_state = outputs.last_hidden_state  # [batch_size, seq_len, hidden_dim]
```

    - **<font style="color:rgb(51, 51, 51);">提取Embedding</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">[CLS] token：</font>`<font style="color:rgb(51, 51, 51);">cls_embedding = last_hidden_state[:, 0, :]</font>`
        * <font style="color:rgb(51, 51, 51);">平均池化：</font>`<font style="color:rgb(51, 51, 51);">mean_embedding = last_hidden_state.mean(dim=1)</font>`
2. **LLM（如Qwen）的计算流程**：
    - **<font style="color:rgb(51, 51, 51);">输入处理</font>**<font style="color:rgb(51, 51, 51);">：Tokenization生成</font>`<font style="color:rgb(51, 51, 51);">input_ids</font>`<font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:rgb(51, 51, 51);">前向传播</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
outputs = model(input_ids, output_hidden_states=True)
hidden_states = outputs.hidden_states  # 包含所有层的隐藏状态
last_layer = hidden_states[-1]  # 最后一层 [batch_size, seq_len, hidden_dim]
```

    - **<font style="color:rgb(51, 51, 51);">提取Embedding</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">最后一个token：</font>`<font style="color:rgb(51, 51, 51);">last_token_embedding = last_layer[:, -1, :]</font>`
        * <font style="color:rgb(51, 51, 51);">平均池化：</font>`<font style="color:rgb(51, 51, 51);">mean_embedding = last_layer.mean(dim=1)</font>`

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **维度** | **BERT Embedding** | **LLM Embedding** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">上下文建模</font>** | <font style="color:rgb(51, 51, 51);">双向上下文，捕捉全局依赖</font> | <font style="color:rgb(51, 51, 51);">单向上下文，仅左侧信息</font> |
| **<font style="color:rgb(51, 51, 51);">任务适配性</font>** | <font style="color:rgb(51, 51, 51);">适合NLU任务（分类、NER等）</font> | <font style="color:rgb(51, 51, 51);">适合生成任务，零样本学习</font> |
| **<font style="color:rgb(51, 51, 51);">计算开销</font>** | <font style="color:rgb(51, 51, 51);">编码器结构，推理速度较慢</font> | <font style="color:rgb(51, 51, 51);">解码器结构，生成时需逐步预测，但Embedding提取较快</font> |
| **<font style="color:rgb(51, 51, 51);">数据依赖</font>** | <font style="color:rgb(51, 51, 51);">需微调以适配下游任务</font> | <font style="color:rgb(51, 51, 51);">大规模预训练后可直接用于少样本场景</font> |


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">BERT Embedding</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">文本分类、实体识别（NER）、语义相似度（需微调或Sentence-BERT）。</font>
    - <font style="color:rgb(51, 51, 51);">短文本理解任务（如问答系统）。</font>
+ **<font style="color:rgb(51, 51, 51);">LLM Embedding</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">零样本/少样本学习（如文本分类、聚类）。</font>
    - <font style="color:rgb(51, 51, 51);">生成任务的前置表示（如文本摘要、对话系统）。</font>
    - <font style="color:rgb(51, 51, 51);">长文本表示（需结合池化策略）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **BERT的改进**：
    - **<font style="color:rgb(51, 51, 51);">池化策略优化</font>**<font style="color:rgb(51, 51, 51);">：使用动态掩码池化、加权平均（如BERT-Whitening）。</font>
    - **<font style="color:rgb(51, 51, 51);">对比学习</font>**<font style="color:rgb(51, 51, 51);">：SimCSE通过Dropout生成正样本，提升句子表示区分度。</font>
    - **<font style="color:rgb(51, 51, 51);">多层融合</font>**<font style="color:rgb(51, 51, 51);">：Concatenate最后几层的隐藏状态（如BERT-4-8层）。</font>
2. **LLM的改进**：
    - **<font style="color:rgb(51, 51, 51);">双向化改造</font>**<font style="color:rgb(51, 51, 51);">：在特定层引入双向注意力（如UniLM）。</font>
    - **<font style="color:rgb(51, 51, 51);">中间层利用</font>**<font style="color:rgb(51, 51, 51);">：结合多层表示（如取第16层和第24层的平均）。</font>
    - **<font style="color:rgb(51, 51, 51);">微调策略</font>**<font style="color:rgb(51, 51, 51);">：通过Adapter或LoRA适配下游任务，避免全参数微调。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

text = "Hello, world!"
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
with torch.no_grad():
    outputs = model(**inputs)

# 提取[CLS] Embedding
cls_embedding = outputs.last_hidden_state[:, 0, :]
# 平均池化
mean_embedding = outputs.last_hidden_state.mean(dim=1)

```

```python
from transformers import GPT2Tokenizer, GPT2Model
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

text = "Hello, world!"
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
with torch.no_grad():
    outputs = model(**inputs, output_hidden_states=True)

# 提取最后一层的最后一个token
last_token_embedding = outputs.hidden_states[-1][:, -1, :]
# 平均池化
mean_embedding = outputs.hidden_states[-1].mean(dim=1)

```





## <font style="color:rgb(51, 51, 51);">如何训练大模型，使LLM具有语义表征能力？</font>
<font style="color:rgb(51, 51, 51);">基于Qwen2.5训练商品语义表征模型的完整流程（以电商场景构建商品向量检索系统为例)</font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">某跨境电商平台需要为3000万SKU建立语义检索系统，要求将商品标题、描述、属性等文本信息编码为768维向量，支持多语言相似商品检索。</font>

:::

<font style="color:rgb(51, 51, 51);">过对比学习对齐语义空间，利用Qwen2.5强大的语言理解能力，结合业务数据特性进行针对性优化。需要注意的是，实际部署时要做好版本管理和AB测试。</font>

:::color5
**<font style="color:#601BDE;">1.训练阶段</font>**

:::

+ 原始数据采集：
    - <font style="color:rgb(51, 51, 51);">商品标题（中/英/西/法等多语言）</font>
    - <font style="color:rgb(51, 51, 51);">商品描述（结构化+非结构化文本）</font>
    - <font style="color:rgb(51, 51, 51);">商品类目三级标签</font>
    - <font style="color:rgb(51, 51, 51);">用户搜索点击日志（正样本对）</font>
    - <font style="color:rgb(51, 51, 51);">人工标注的相似商品对（5万组）</font>
+ 数据预处理：

```python
# 多语言混合清洗示例
def clean_text(text):
    text = re.sub(r'【.*?】', '', text)  # 去除促销标签
    text = normalize_unicode(text)  # Unicode标准化
    text = remove_duplicate_spaces(text)
    return text[:512]  # 截断适配Qwen最大长度
```

:::color5
**<font style="color:#601BDE;">2.模型选择与改造</font>**

:::

+ 基座模型：Qwen2.5-7B（平衡效果与推理成本）
+ 改造方案：
    - **<font style="color:#74B602;">在Transformer顶层增加Mean Pooling层</font>**
    - <font style="color:rgb(51, 51, 51);">添加可学习的</font>**<font style="color:#74B602;">[CLS] token</font>**
    - <font style="color:rgb(51, 51, 51);">输出层接768维投影层（L2正则化）</font>

```python
class CustomQwen(Qwen2PreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.transformer = Qwen2Model(config)
        self.projection = nn.Linear(config.hidden_size, 768)

    def forward(self, input_ids):
        outputs = self.transformer(input_ids)
        sequence_output = outputs.last_hidden_state
        pooled = torch.mean(sequence_output, dim=1)
        return F.normalize(self.projection(pooled), p=2, dim=1)
```

:::color5
**<font style="color:#601BDE;">3.训练策略设计</font>**

:::

+ <font style="color:rgb(51, 51, 51);">对比学习框架（Triplet Loss + InfoNCE）</font>
+ <font style="color:rgb(51, 51, 51);">Batch构造策略：</font>
    - <font style="color:rgb(51, 51, 51);">在线困难样本挖掘（Online Hard Mining）</font>
    - <font style="color:rgb(51, 51, 51);">跨语言负样本生成（同品类不同语言商品）</font>
+ <font style="color:rgb(51, 51, 51);">混合训练数据：</font>

```plain
| 数据类型        | 比例 | 示例                     |
|----------------|------|--------------------------|
| 点击日志正样本 | 60%  | 用户点击A后点击B         |
| 人工标注样本   | 25%  | iPhone15 vs 苹果手机     |
| 类目负样本     | 15%  | 手机 vs 数据线（同店铺） |
```

:::color5
**<font style="color:#601BDE;">4.分布式训练配置</font>**

:::

+ <font style="color:rgb(51, 51, 51);">硬件：8x A100 80GB（NVLink互联）</font>
+ <font style="color:rgb(51, 51, 51);">并行策略：</font>

```plain
torchrun --nnodes=1 --nproc_per_node=8 \
  --master_port=29500 train.py \
  --bf16 True \
  --gradient_checkpointing \
  --per_device_train_batch_size 16 \
  --gradient_accumulation_steps 4
```

+ 超参数

```plain
learning_rate: 2e-5
warmup_ratio: 0.1
weight_decay: 0.01
max_grad_norm: 1.0
```

:::color5
**<font style="color:#601BDE;">5.评估与调优</font>**

:::

+ <font style="color:rgb(51, 51, 51);">离线评估指标：</font>

```python
# 计算召回率
def calculate_recall(embeddings, query_ids, k=10):
    index = faiss.IndexFlatIP(768)
    index.add(embeddings)
    D, I = index.search(query_emb, k)
    return np.mean([1 if target in I[i] else 0 for i,target in enumerate(target_ids)])
```

+ 多维度评估

| **测试场景** | **数据量** | **基线模型Recall@10** | **目标** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">跨语言检索</font> | <font style="color:rgb(51, 51, 51);">5,000</font> | <font style="color:rgb(51, 51, 51);">72% → 85%+</font> | <font style="color:rgb(51, 51, 51);">✅</font> |
| <font style="color:rgb(51, 51, 51);">长尾商品</font> | <font style="color:rgb(51, 51, 51);">10,000</font> | <font style="color:rgb(51, 51, 51);">65% → 78%+</font> | <font style="color:rgb(51, 51, 51);">✅</font> |
| <font style="color:rgb(51, 51, 51);">同义替换</font> | <font style="color:rgb(51, 51, 51);">2,000</font> | <font style="color:rgb(51, 51, 51);">68% → 82%+</font> | <font style="color:rgb(51, 51, 51);">✅</font> |


+ 业务效果
    - <font style="color:rgb(51, 51, 51);">商品搜索CTR提升23%</font>
    - <font style="color:rgb(51, 51, 51);">长尾商品曝光量增加45%</font>
    - <font style="color:rgb(51, 51, 51);">平均响应时间<80ms（A10 GPU）</font>
+ 优化方案
1. <font style="color:rgb(51, 51, 51);">多语言对齐：通过共享subword词汇表实现跨语言映射</font>
2. <font style="color:rgb(51, 51, 51);">属性增强：将商品规格参数（如"256GB ROM"）转换为结构化提示：</font>

```python
"Specs: [ROM:256][RAM:12][Color:Black]"
```



# 
# SimCSE
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">SimCSE（Simple Contrastive Learning of Sentence Embeddings），旨在解决句子嵌入（sentence embedding）的质量问题。传统方法如BERT的[CLS]向量或平均池化在句子相似度任务上表现不佳，而监督方法依赖大量标注数据。SimCSE通过对比学习框架，在无监督和监督两种场景下显著提升了句子嵌入的语义区分能力。</font>

:::

<font style="color:rgb(51, 51, 51);">SimCSE成为句子嵌入领域的经典基线模型，后续工作如ESimCSE、PromptBERT等均在其基础上改进。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741160854259-03d31a41-9bbf-4348-9797-c6b407081efa.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">无监督对比学习</font>**<font style="color:rgb(51, 51, 51);">：仅通过句子自身两次不同的dropout掩码作为正例，同一批次内其他句子作为负例。</font>
2. **<font style="color:rgb(51, 51, 51);">监督对比学习</font>**<font style="color:rgb(51, 51, 51);">：利用自然语言推理（NLI）数据集中的entailment（蕴含）和contradiction（矛盾）样本构建正负例。</font>
3. **<font style="color:rgb(51, 51, 51);">简单高效</font>**<font style="color:rgb(51, 51, 51);">：无需复杂的数据增强方法，仅依赖dropout噪声或现成的NLI标签。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">无监督SimCSE</font>**<font style="color:rgb(51, 51, 51);">：通用文本（如Wikipedia），每个句子自身作为正例。</font>
+ **<font style="color:rgb(51, 51, 51);">监督SimCSE</font>**<font style="color:rgb(51, 51, 51);">：NLI数据集（如SNLI、MNLI），利用蕴含对作为正例，矛盾对作为负例。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">编码器</font>**<font style="color:rgb(51, 51, 51);">：BERT或RoBERTa作为基础模型，输出句子表示。</font>
+ **<font style="color:rgb(51, 51, 51);">投影头</font>**<font style="color:rgb(51, 51, 51);">（可选）：在编码器顶部添加MLP层（将768维映射到更高维度，训练后移除）。</font>
+ **<font style="color:rgb(51, 51, 51);">对比损失</font>**<font style="color:rgb(51, 51, 51);">：采用InfoNCE损失函数，最大化正例相似度，最小化负例相似度。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

**<font style="color:rgb(51, 51, 51);">无监督训练</font>**

1. **<font style="color:rgb(51, 51, 51);">正例生成</font>**<font style="color:rgb(51, 51, 51);">：同一句子两次输入编码器，通过不同dropout生成两个嵌入。</font>
2. **<font style="color:rgb(51, 51, 51);">负例构造</font>**<font style="color:rgb(51, 51, 51);">：同一批次内其他句子的嵌入作为负例。</font>
3. **<font style="color:rgb(51, 51, 51);">损失计算</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741159903725-08e61f77-f903-4d3c-a566-7ce8bc5a0552.png)

<font style="color:rgb(51, 51, 51);">其中，τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是温度超参数，simsim 为余弦相似度。</font>

**<font style="color:rgb(51, 51, 51);">监督训练</font>**

1. **<font style="color:rgb(51, 51, 51);">正例</font>**<font style="color:rgb(51, 51, 51);">：NLI中的蕴含句子对。</font>
2. **<font style="color:rgb(51, 51, 51);">硬负例</font>**<font style="color:rgb(51, 51, 51);">：NLI中的矛盾句子对。</font>
3. <font style="color:rgb(51, 51, 51);">损失计算方式与无监督类似，但引入更多负例。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">简单有效，无需复杂数据增强。</font>
+ <font style="color:rgb(51, 51, 51);">无监督版本性能接近监督方法，监督版本在STS任务上达到SOTA。</font>
+ <font style="color:rgb(51, 51, 51);">通用性强，适用于多种语义匹配任务。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">无监督版本依赖大batch size（如256以上）。</font>
+ <font style="color:rgb(51, 51, 51);">计算成本高（需存储大量负例嵌入）。</font>
+ <font style="color:rgb(51, 51, 51);">领域迁移能力有限，需领域内数据微调。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">句子相似度计算（如STS-B任务）</font>
+ <font style="color:rgb(51, 51, 51);">语义搜索（如FAQ匹配）</font>
+ <font style="color:rgb(51, 51, 51);">文本聚类与分类</font>
+ <font style="color:rgb(51, 51, 51);">问答系统（答案检索）</font>
+ <font style="color:rgb(51, 51, 51);">低资源场景下的语义理解任务</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：结合EDA、回译等方法生成更丰富的正例。</font>
2. **<font style="color:rgb(51, 51, 51);">难负例挖掘</font>**<font style="color:rgb(51, 51, 51);">：通过BM25或相似模型筛选困难负例。</font>
3. **<font style="color:rgb(51, 51, 51);">课程学习</font>**<font style="color:rgb(51, 51, 51);">：逐步增加噪声或负例难度。</font>
4. **<font style="color:rgb(51, 51, 51);">多任务学习</font>**<font style="color:rgb(51, 51, 51);">：联合训练对比损失和MLM任务。</font>
5. **<font style="color:rgb(51, 51, 51);">领域适应</font>**<font style="color:rgb(51, 51, 51);">：在特定领域数据上继续微调。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer

class SimCSE(nn.Module):
    def __init__(self, model_name='bert-base-uncased', temperature=0.05):
        super().__init__()
        self.bert = BertModel.from_pretrained(model_name)
        self.temperature = temperature
    
    def forward(self, input_ids, attention_mask):
        # 获取两个不同dropout的嵌入
        emb1 = self.bert(input_ids, attention_mask, output_hidden_states=True).last_hidden_state[:,0,:]
        emb2 = self.bert(input_ids, attention_mask, output_hidden_states=True).last_hidden_state[:,0,:]
        return emb1, emb2

def contrastive_loss(emb1, emb2, temperature):
    batch_size = emb1.size(0)
    # 计算余弦相似度矩阵
    emb = torch.cat([emb1, emb2], dim=0)
    sim_matrix = torch.cosine_similarity(emb.unsqueeze(1), emb.unsqueeze(0), dim=-1)
    # 构建标签：对角线为正例
    labels = torch.arange(batch_size, device=emb.device).repeat(2)
    mask = torch.eye(2*batch_size, dtype=torch.bool, device=emb.device)
    sim_matrix = sim_matrix.masked_fill(mask, -1e4)
    # 计算交叉熵损失
    sim_matrix /= temperature
    loss = nn.CrossEntropyLoss()(sim_matrix, labels)
    return loss

# 使用示例
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = SimCSE()
inputs = tokenizer(["This is a sentence.", "Another sentence."], padding=True, return_tensors='pt')
emb1, emb2 = model(**inputs)
loss = contrastive_loss(emb1, emb2, temperature=0.05)

```



# Bert系列
## bert系列模型对比
**总结**

+ **<font style="color:rgb(51, 51, 51);">BERT</font>**<font style="color:rgb(51, 51, 51);">：NLP领域的基石模型，适合通用任务但需针对性优化。</font>
+ **<font style="color:rgb(51, 51, 51);">M3E</font>**<font style="color:rgb(51, 51, 51);">：多语言场景首选，强在跨语言语义对齐。</font>
+ **<font style="color:rgb(51, 51, 51);">BGE</font>**<font style="color:rgb(51, 51, 51);">：中英文混合任务表现最优，适合垂直领域检索。</font>
+ **<font style="color:rgb(51, 51, 51);">GTE</font>**<font style="color:rgb(51, 51, 51);">：复杂任务泛化能力强，但需更高训练成本。</font>

:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

| **模型** | **提出时间** | **核心动机** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">2018</font> | <font style="color:rgb(51, 51, 51);">解决双向上下文建模问题，建立统一的预训练-微调范式</font> |
| **<font style="color:rgb(51, 51, 51);">RoBERTa</font>** | <font style="color:rgb(51, 51, 51);">2019</font> | <font style="color:rgb(51, 51, 51);">发现BERT训练不充分，通过优化训练策略提升性能</font> |
| **<font style="color:rgb(51, 51, 51);">ALBERT</font>** | <font style="color:rgb(51, 51, 51);">2019</font> | <font style="color:rgb(51, 51, 51);">解决BERT参数效率问题，降低显存消耗</font> |
| **<font style="color:rgb(51, 51, 51);">DeBERTa</font>** | <font style="color:rgb(51, 51, 51);">2020</font> | <font style="color:rgb(51, 51, 51);">解决BERT的位置编码和注意力机制缺陷，提升细粒度语义理解能力</font> |


:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

| **模型** | **核心创新** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">• 双向Transformer编码器   </font><font style="color:rgb(51, 51, 51);">• MLM+NSP联合预训练任务</font> |
| **<font style="color:rgb(51, 51, 51);">RoBERTa</font>** | <font style="color:rgb(51, 51, 51);">• 动态Masking   </font><font style="color:rgb(51, 51, 51);">• 移除NSP任务   </font><font style="color:rgb(51, 51, 51);">• 超大batch训练（8k）</font> |
| **<font style="color:rgb(51, 51, 51);">ALBERT</font>** | <font style="color:rgb(51, 51, 51);">• 参数共享（跨层共享）   </font><font style="color:rgb(51, 51, 51);">• 因子化词嵌入   </font><font style="color:rgb(51, 51, 51);">• SOP替代NSP任务</font> |
| **<font style="color:rgb(51, 51, 51);">DeBERTa</font>** | <font style="color:rgb(51, 51, 51);">• 解耦注意力（内容+位置分离）   </font><font style="color:rgb(51, 51, 51);">• 增强型Mask解码器   </font><font style="color:rgb(51, 51, 51);">• 相对位置编码改进</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **模型** | **数据量** | **数据组成** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">16GB</font> | <font style="color:rgb(51, 51, 51);">BooksCorpus（80%）+ Wikipedia（20%）</font> |
| **<font style="color:rgb(51, 51, 51);">RoBERTa</font>** | <font style="color:rgb(51, 51, 51);">160GB</font> | <font style="color:rgb(51, 51, 51);">BooksCorpus+Wiki + CC-News+OpenWebText+Stories</font> |
| **<font style="color:rgb(51, 51, 51);">ALBERT</font>** | <font style="color:rgb(51, 51, 51);">16GB</font> | <font style="color:rgb(51, 51, 51);">同BERT，但扩展至XL版本时使用更多数据</font> |
| **<font style="color:rgb(51, 51, 51);">DeBERTa</font>** | <font style="color:rgb(51, 51, 51);">160GB</font> | <font style="color:rgb(51, 51, 51);">同RoBERTa，增加对话数据集（如Reddit）</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

| **参数** | **BERT-Base** | **RoBERTa-Base** | **ALBERT-Base** | **DeBERTa-Base** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">层数</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">12</font> |
| <font style="color:rgb(51, 51, 51);">隐藏层维度</font> | <font style="color:rgb(51, 51, 51);">768</font> | <font style="color:rgb(51, 51, 51);">768</font> | <font style="color:rgb(51, 51, 51);">768</font> | <font style="color:rgb(51, 51, 51);">768</font> |
| <font style="color:rgb(51, 51, 51);">注意力头数</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">12</font> |
| <font style="color:rgb(51, 51, 51);">参数量</font> | <font style="color:rgb(51, 51, 51);">110M</font> | <font style="color:rgb(51, 51, 51);">125M</font> | <font style="color:rgb(51, 51, 51);">12M</font> | <font style="color:rgb(51, 51, 51);">134M</font> |
| <font style="color:rgb(51, 51, 51);">位置编码</font> | <font style="color:rgb(51, 51, 51);">绝对</font> | <font style="color:rgb(51, 51, 51);">绝对</font> | <font style="color:rgb(51, 51, 51);">绝对</font> | <font style="color:rgb(51, 51, 51);">相对+绝对</font> |


:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

| **参数** | **BERT** | **RoBERTa** | **ALBERT** | **DeBERTa** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">Batch Size</font> | <font style="color:rgb(51, 51, 51);">256</font> | <font style="color:rgb(51, 51, 51);">8,000</font> | <font style="color:rgb(51, 51, 51);">4,096</font> | <font style="color:rgb(51, 51, 51);">2,048</font> |
| <font style="color:rgb(51, 51, 51);">训练步数</font> | <font style="color:rgb(51, 51, 51);">1M</font> | <font style="color:rgb(51, 51, 51);">500K</font> | <font style="color:rgb(51, 51, 51);">1.5M</font> | <font style="color:rgb(51, 51, 51);">1M</font> |
| <font style="color:rgb(51, 51, 51);">峰值学习率</font> | <font style="color:rgb(51, 51, 51);">1e-4</font> | <font style="color:rgb(51, 51, 51);">6e-4</font> | <font style="color:rgb(51, 51, 51);">4e-4</font> | <font style="color:rgb(51, 51, 51);">5e-4</font> |
| <font style="color:rgb(51, 51, 51);">硬件需求</font> | <font style="color:rgb(51, 51, 51);">64 TPU v3</font> | <font style="color:rgb(51, 51, 51);">1024 V100</font> | <font style="color:rgb(51, 51, 51);">64 TPU v3</font> | <font style="color:rgb(51, 51, 51);">256 V100</font> |
| <font style="color:rgb(51, 51, 51);">训练天数</font> | <font style="color:rgb(51, 51, 51);">4</font> | <font style="color:rgb(51, 51, 51);">1.5</font> | <font style="color:rgb(51, 51, 51);">3</font> | <font style="color:rgb(51, 51, 51);">2.5</font> |


:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **模型** | **优点** | **缺点** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">• 通用性强   </font><font style="color:rgb(51, 51, 51);">• 生态完善</font> | <font style="color:rgb(51, 51, 51);">• 计算成本高   </font><font style="color:rgb(51, 51, 51);">• NSP有效性存疑</font> |
| **<font style="color:rgb(51, 51, 51);">RoBERTa</font>** | <font style="color:rgb(51, 51, 51);">• 性能SOTA   </font><font style="color:rgb(51, 51, 51);">• 训练策略优化</font> | <font style="color:rgb(51, 51, 51);">• 显存消耗大   </font><font style="color:rgb(51, 51, 51);">• 领域迁移需微调</font> |
| **<font style="color:rgb(51, 51, 51);">ALBERT</font>** | <font style="color:rgb(51, 51, 51);">• 参数效率高（89%压缩）   </font><font style="color:rgb(51, 51, 51);">• 适合移动端部署</font> | <font style="color:rgb(51, 51, 51);">• 推理速度下降   </font><font style="color:rgb(51, 51, 51);">• 部分任务精度损失</font> |
| **<font style="color:rgb(51, 51, 51);">DeBERTa</font>** | <font style="color:rgb(51, 51, 51);">• GLUE榜首模型   </font><font style="color:rgb(51, 51, 51);">• 细粒度语义理解强</font> | <font style="color:rgb(51, 51, 51);">• 实现复杂度高   </font><font style="color:rgb(51, 51, 51);">• 训练收敛较慢</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

| **场景** | **推荐模型** | **原因** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">资源受限部署</font> | <font style="color:rgb(51, 51, 51);">ALBERT</font> | <font style="color:rgb(51, 51, 51);">参数效率高，内存占用小</font> |
| <font style="color:rgb(51, 51, 51);">语义相似度计算</font> | <font style="color:rgb(51, 51, 51);">DeBERTa</font> | <font style="color:rgb(51, 51, 51);">位置编码改进提升句间关系建模</font> |
| <font style="color:rgb(51, 51, 51);">大规模文本分类</font> | <font style="color:rgb(51, 51, 51);">RoBERTa</font> | <font style="color:rgb(51, 51, 51);">大数据训练带来更强泛化能力</font> |
| <font style="color:rgb(51, 51, 51);">多语言任务</font> | <font style="color:rgb(51, 51, 51);">BERT-multilingual</font> | <font style="color:rgb(51, 51, 51);">原生支持104种语言</font> |
| <font style="color:rgb(51, 51, 51);">长文档理解</font> | <font style="color:rgb(51, 51, 51);">DeBERTa</font> | <font style="color:rgb(51, 51, 51);">增强的相对位置编码支持更长序列</font> |


:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

| **模型** | **典型改进方向** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">• Whole Word Masking   </font><font style="color:rgb(51, 51, 51);">• 知识蒸馏（TinyBERT）   </font><font style="color:rgb(51, 51, 51);">• 领域适应（BioBERT）</font> |
| **<font style="color:rgb(51, 51, 51);">RoBERTa</font>** | <font style="color:rgb(51, 51, 51);">• 动态数据清洗   </font><font style="color:rgb(51, 51, 51);">• 混合精度训练优化   </font><font style="color:rgb(51, 51, 51);">• 结合检索增强</font> |
| **<font style="color:rgb(51, 51, 51);">ALBERT</font>** | <font style="color:rgb(51, 51, 51);">• 适配器层插入   </font><font style="color:rgb(51, 51, 51);">• 量化压缩（INT8）   </font><font style="color:rgb(51, 51, 51);">• 跨模态扩展（VL-ALBERT）</font> |
| **<font style="color:rgb(51, 51, 51);">DeBERTa</font>** | <font style="color:rgb(51, 51, 51);">• 稀疏注意力机制   </font><font style="color:rgb(51, 51, 51);">• 预训练任务多样化   </font><font style="color:rgb(51, 51, 51);">• 多模态融合</font> |


:::color5
**<font style="color:#601BDE;">8.选择建议</font>**

:::

| **优先级** | **场景** | **推荐模型** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">1</font> | <font style="color:rgb(51, 51, 51);">高精度需求</font> | <font style="color:rgb(51, 51, 51);">DeBERTa</font> |
| <font style="color:rgb(51, 51, 51);">2</font> | <font style="color:rgb(51, 51, 51);">工业级部署</font> | <font style="color:rgb(51, 51, 51);">ALBERT</font> |
| <font style="color:rgb(51, 51, 51);">3</font> | <font style="color:rgb(51, 51, 51);">通用NLP任务</font> | <font style="color:rgb(51, 51, 51);">RoBERTa</font> |
| <font style="color:rgb(51, 51, 51);">4</font> | <font style="color:rgb(51, 51, 51);">多语言/低资源</font> | <font style="color:rgb(51, 51, 51);">BERT-multi</font> |


## BERT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">BERT（Bidirectional Encoder Representations from Transformers）由Google于2018年提出，是自然语言处理领域的里程碑式模型。其诞生背景包括：</font>

+ **<font style="color:rgb(51, 51, 51);">单向模型的局限</font>**<font style="color:rgb(51, 51, 51);">：传统模型（如GPT）仅使用单向上下文，</font>**<font style="color:#ED740C;">BERT的表示在所有层中都同时依赖于左右上下文。</font>**
+ **<font style="color:rgb(51, 51, 51);">特征抽取需求</font>**<font style="color:rgb(51, 51, 51);">：ELMo等模型未完全解决深层双向表示问题</font>
+ **<font style="color:rgb(51, 51, 51);">迁移学习潜力</font>**<font style="color:rgb(51, 51, 51);">：证明预训练+微调范式在NLP中的通用性</font>

:::

<font style="color:rgb(51, 51, 51);">BERT奠定了预训练语言模型的基础范式，其开源实现和生态工具（如Hugging Face Transformers）极大推动了NLP领域的发展。后续大模型如GPT-3、T5均可视为其思想延伸。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741162178214-69917fca-931a-44b2-b5c6-69f08cd094ec.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">双向Transformer编码器</font>**<font style="color:rgb(51, 51, 51);">：同时捕捉左右上下文信息</font>
2. **<font style="color:rgb(51, 51, 51);">预训练任务创新</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Masked Language Model (MLM)</font>**<font style="color:rgb(51, 51, 51);">：随机遮盖15%的token进行预测</font>
    - **<font style="color:rgb(51, 51, 51);">Next Sentence Prediction (NSP)</font>**<font style="color:rgb(51, 51, 51);">：判断句子对是否连续</font>
3. **<font style="color:rgb(51, 51, 51);">统一架构范式</font>**<font style="color:rgb(51, 51, 51);">：同一模型支持多种下游任务（分类/序列标注/匹配等）</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **数据集** | **大小** | **内容特点** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">BooksCorpus</font> | <font style="color:rgb(51, 51, 51);">800M词</font> | <font style="color:rgb(51, 51, 51);">未出版书籍的长文本</font> |
| <font style="color:rgb(51, 51, 51);">English Wikipedia</font> | <font style="color:rgb(51, 51, 51);">2500M词</font> | <font style="color:rgb(51, 51, 51);">百科条目（不含表格/标题）</font> |
| **<font style="color:rgb(51, 51, 51);">总数据量</font>** | **<font style="color:rgb(51, 51, 51);">3300M词</font>** | <font style="color:rgb(51, 51, 51);">长文本占比约74%</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741161835093-89daf114-d475-4795-adda-baec11a72505.png)

1. **<font style="background-color:#D9EAFC;">嵌入层</font>**
    1. **<font style="color:#ED740C;">WordPiece</font>**<font style="color:#2ea121;"> </font><font style="color:#1f2329;">：</font><font style="color:#2ea121;">BERT 使⽤ WordPiece 作为分词⽅法 ，将单词划分为⼦词单元。</font><font style="color:#1f2329;">这 种处理⽅式既能处理未知词汇，⼜能提⾼模型的灵活性和泛化能⼒。例如，罕见或不规则单词会被分成更常见的⼦词单位，进⽽能够在训练中更好地学习到词汇语义。</font>
    2. **<font style="color:#ED740C;">位置嵌入position embedding（绝对位置编码）</font>**<font style="color:#1f2329;">：由于 BERT 只使⽤Transformer 的编码器部分，并不依赖于序列化结构（如 RNN 或 LSTM），因此它⽆法从输⼊序列中⾃然地获取位置信息。为了弥补这⼀点，</font><font style="color:#2ea121;">BERT 通过位置嵌⼊为每个词汇添加了位置特征</font><font style="color:#1f2329;">，使模型能够感知词汇在序列中的相对位置。BERT 初始化了⼀个位置嵌⼊矩阵，并在训练过程中学习这些位置向量。</font>
    3. **<font style="color:#ED740C;">段落嵌入 segment embedding</font>**<font style="color:#1f2329;">：在 BERT 中，</font><font style="color:#2ea121;">输⼊通常是两个句⼦拼接⽽成，特别是在句⼦预测任务 (NextSentencePrediction, NSP) </font><font style="color:#1f2329;">中。因此，BERT为输⼊中的每个 token添加⼀个段落嵌⼊，⽤来区分句⼦ A 和句⼦B，帮助模型更好地理解句⼦之间的关系。</font>
    4. **<font style="color:#ED740C;">为什么三个embedding可以直接相加？</font>**
        1. **<font style="color:rgb(51, 51, 51);">互补性特征与线性叠加</font>**
            + <font style="color:rgb(51, 51, 51);">Token Embeddings：表示词本身的语义信息（如词向量）。</font>
            + <font style="color:rgb(51, 51, 51);">Position Embeddings</font><font style="color:rgb(51, 51, 51);">：编码词在序列中的位置关系（如绝对位置或相对位置）。</font>
            + <font style="color:rgb(51, 51, 51);">Segment Embeddings：区分不同句子（如问答任务中的问题和答案）。</font>

<font style="color:rgb(51, 51, 51);">这三类嵌入分别从语义、位置和句子边界三个维度提供互补信息。直接相加可以看作一种特征融合方式，允许模型在训练过程中动态调整各部分的权重，最终形成一个统一的表示。尽管相加是线性操作，但后续的 Transformer 层（尤其是自注意力机制）会通过非线性变换学习特征的交互。</font>

        2. **<font style="color:rgb(51, 51, 51);">维度一致性</font>**

<font style="color:rgb(51, 51, 51);">三个嵌入的维度相同（例如 BERT-base 为 768 维），相加操作在数学上是合法的，且不会破坏向量空间的几何结构。如果采用拼接（concatenation）会显著增加输入维度，导致后续的 Transformer 层参数爆炸（如拼接后维度为 768×3=2304），而相加保持了维度不变，计算更高效。</font>

        3. **<font style="color:rgb(51, 51, 51);">梯度传播的稳定性</font>**

<font style="color:rgb(51, 51, 51);">相加操作对梯度的反向传播更友好。在反向传播时，梯度可以直接均分到三个嵌入矩阵中，避免了拼接操作可能导致的梯度不均衡问题。实验表明，相加的收敛效果更好，而拼接可能引入额外的噪声。</font>

2. **<font style="color:#1f2329;">编码器层</font>**

<font style="color:#1f2329;">BERT的主要结构是基于 Transformer的编码器部分，通过堆叠多层编码器来实现深度语义学习。Transformer编码器包含⼏个核⼼部分：</font>**<font style="color:#74B602;">多头注意力+LayerNorm + 前馈层 + LayerNorm。</font>**<font style="color:#1f2329;">在 BERT-base 中，每个⾃注意⼒头的输出维度是 64（总维度为768），⽽多头注意⼒机制则是将 12个⾃注意⼒头的输出拼接 (concatenate) 后，再通过⼀个线性层处理，形成最终的多头注意⼒输出。</font>

<font style="color:rgb(51, 51, 51);">基于Transformer Encoder堆叠：</font>

```python
# BERT-Base配置
{
    "hidden_size": 768,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
    "max_position_embeddings": 512,
    "vocab_size": 30522
}

# BERT-Large配置
{
    "hidden_size": 1024,
    "num_attention_heads": 16,
    "num_hidden_layers": 24
}
```

**<font style="color:rgb(51, 51, 51);">参数量</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">Base：110M</font>
+ <font style="color:rgb(51, 51, 51);">Large：340M</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **NSP**：next sentence predict

<font style="color:#1f2329;">BERT 通过给定两个句⼦，</font>**<font style="color:#74B602;">要求模型判断这两个句⼦是否为连续上下句</font>**<font style="color:#1f2329;">。这⼀任务帮助 BERT 学习句⼦间的关系，提⾼在问答、推理等任务中的表现。语料中50%的句⼦，选择其相应的下⼀句⼀起形成上下句，作为正样本；其余50%的句⼦随机选择⼀句⾮下⼀句⼀起形成上下句，作为负样本。这种 设定，有利于sentence-level tasks，例如问答。</font>

```python
[CLS] Sentence A [SEP] Sentence B [SEP]
```

    - <font style="color:rgb(51, 51, 51);">随机选择50%的句子对进行NSP训练</font>
2. **MLM**：masked language modeling
+ <font style="color:#5f7ddb;background-color:#f5f6f7;">定义</font><font style="color:#5f7ddb;"> </font><font style="color:#1f2329;">: MLM 是</font><font style="color:#d83931;">掩码语⾔建模</font><font style="color:#1f2329;">，训练模型预测在⼀个句⼦中被随机掩盖（masked）的词。模型可以使⽤整个句⼦的上下⽂，包括掩盖词的前后内容。</font>
+ <font style="color:#1456f0;"></font><font style="color:#4e6edb;background-color:#f5f6f7;">应用</font><font style="color:#4e6edb;"> </font><font style="color:#1f2329;">: 它主要⽤于表⽰学习任务，例如 BERT 模型，帮助模型更好地理解整个句⼦的语义。</font>
+ <font style="color:#1456f0;">训练方式 </font><font style="color:#1f2329;">: </font><font style="color:#de7802;">在训练过程中，句⼦中的⼀些词会被随机掩盖</font><font style="color:#1f2329;">，模型的任务是根据其余词来预测被掩盖的词。这是⼀种双向建模。</font>

```python
# 每个序列随机mask 15%的token
mask_pos = random.sample(range(seq_len), int(seq_len*0.15))
for pos in mask_pos:
    80%概率替换为[MASK]
    10%概率替换为随机词
    10%保持原词
```

```python
1输⼊序列："我爱[MASK]天"
2模型预测："我爱北京天"
```

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><u><font style="color:#2ea121;">双向性</font></u><font style="color:#1f2329;">：模型可以同时利⽤左侧和右侧的上下⽂信息。</font>

<font style="color:#1456f0;">•  </font><u><font style="color:#2ea121;">信息泄露问题</font></u><font style="color:#1f2329;">：在训练过程中，模型可以看到被遮蔽词的未来信息，这在⽣成任务中不适⽤。</font>

3. **预训练参数**：
    - <font style="color:rgb(51, 51, 51);">Batch Size：256（TPU Pod）</font>
    - <font style="color:rgb(51, 51, 51);">训练步数：1M（约40 epochs）</font>
    - <font style="color:rgb(51, 51, 51);">优化器：AdamW (β1=0.9, β2=0.999)</font>
    - <font style="color:rgb(51, 51, 51);">学习率：1e-4（warmup步数10k）</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">GLUE基准提升：平均比GPT高7.7%</font>
+ <font style="color:rgb(51, 51, 51);">支持多种任务架构</font>
+ <font style="color:rgb(51, 51, 51);">长距离依赖建模能力强</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">预训练计算成本高（16 TPU chips × 4天）</font>
+ <font style="color:rgb(51, 51, 51);">NSP任务有效性后续被质疑（RoBERTa证明可移除）</font>
+ <font style="color:rgb(51, 51, 51);">最大长度限制512 tokens</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">文本分类（情感分析）</font>
+ <font style="color:rgb(51, 51, 51);">命名实体识别（医疗实体抽取）</font>
+ <font style="color:rgb(51, 51, 51);">问答系统（SQuAD基准）</font>
+ <font style="color:rgb(51, 51, 51);">语义相似度计算（法律条款匹配）</font>
+ <font style="color:rgb(51, 51, 51);">文本摘要（结合生成式Decoder）</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **架构改进**：
    - <font style="color:rgb(51, 51, 51);">RoBERTa：移除NSP，扩大数据与训练步数</font>
    - <font style="color:rgb(51, 51, 51);">ALBERT：参数共享降低内存消耗</font>
    - <font style="color:rgb(51, 51, 51);">DistilBERT：知识蒸馏压缩模型</font>
2. **训练策略优化**：
    - <font style="color:rgb(51, 51, 51);">Whole Word Masking：遮盖完整词语而非subword</font>
    - <font style="color:rgb(51, 51, 51);">SpanBERT：遮盖连续span而非单个token</font>
3. **领域适配**：
    - <font style="color:rgb(51, 51, 51);">BioBERT：医学文本继续预训练</font>
    - <font style="color:rgb(51, 51, 51);">LegalBERT：法律领域适配</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import BertModel, BertTokenizer

# 加载预训练模型
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 文本编码示例
inputs = tokenizer("Hello, BERT!", return_tensors="pt")
outputs = model(**inputs)
last_hidden_states = outputs.last_hidden_state  # [1, seq_len, 768]

# 微调文本分类
class BertClassifier(torch.nn.Module):
    def __init__(self, num_labels=2):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.classifier = torch.nn.Linear(768, num_labels)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_embedding)

# 训练循环示例
model = BertClassifier()
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

for batch in dataloader:
    inputs = tokenizer(batch['text'], padding=True, return_tensors='pt')
    labels = batch['labels']
    
    model.zero_grad()
    outputs = model(inputs['input_ids'], inputs['attention_mask'])
    loss = loss_fn(outputs, labels)
    loss.backward()
    optimizer.step()

```

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

## RoBERTa
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">RoBERTa（Robustly Optimized BERT Approach）由Facebook AI于2019年提出，是对BERT的优化改进版本。原始BERT存在训练不足、预训练策略次优等问题，RoBERTa通过系统性研究发现了BERT的多个可优化点：</font>

+ <font style="color:rgb(51, 51, 51);">训练数据规模不足</font>
+ <font style="color:rgb(51, 51, 51);">训练步长（steps）不够</font>
+ <font style="color:rgb(51, 51, 51);">静态Masking策略限制模型泛化</font>
+ <font style="color:rgb(51, 51, 51);">未充分利用大规模计算资源</font>

:::

<font style="color:rgb(51, 51, 51);">RoBERTa通过系统性的训练优化，证明了预训练语言模型的潜力不仅在于架构创新，更在于训练策略的充分挖掘。后续工作如DeBERTa、ALBERT等均受其方法论启发。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">动态Masking</font>**<font style="color:rgb(51, 51, 51);">：每个epoch重新生成Mask模式（BERT使用静态Mask）</font>
2. **<font style="color:rgb(51, 51, 51);">更大Batch Size</font>**<font style="color:rgb(51, 51, 51);">：从BERT的256提升到8,000</font>
3. **<font style="color:rgb(51, 51, 51);">更长训练时间</font>**<font style="color:rgb(51, 51, 51);">：训练步数从100K增至300K-500K</font>
4. **<font style="color:rgb(51, 51, 51);">移除NSP任务</font>**<font style="color:rgb(51, 51, 51);">：仅保留MLM任务（Next Sentence Prediction被证明无效）</font>
5. **<font style="color:rgb(51, 51, 51);">扩展训练数据</font>**<font style="color:rgb(51, 51, 51);">：数据量从16GB增至160GB</font>
6. **<font style="color:rgb(51, 51, 51);">Byte-level BPE</font>**<font style="color:rgb(51, 51, 51);">：改进的分词方式处理特殊字符</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **数据集** | **大小** | **内容特点** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">BOOKCORPUS+Wikipedia</font> | <font style="color:rgb(51, 51, 51);">16GB</font> | <font style="color:rgb(51, 51, 51);">BERT原始数据</font> |
| <font style="color:rgb(51, 51, 51);">CC-News</font> | <font style="color:rgb(51, 51, 51);">76GB</font> | <font style="color:rgb(51, 51, 51);">新闻文本</font> |
| <font style="color:rgb(51, 51, 51);">OpenWebText</font> | <font style="color:rgb(51, 51, 51);">38GB</font> | <font style="color:rgb(51, 51, 51);">Reddit高质量链接内容</font> |
| <font style="color:rgb(51, 51, 51);">Stories</font> | <font style="color:rgb(51, 51, 51);">31GB</font> | <font style="color:rgb(51, 51, 51);">CommonCrawl筛选的故事文本</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51);">基本继承BERT架构，但调整了参数规模：</font>

```python
# Base版配置
{
    "hidden_size": 768,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
    "intermediate_size": 3072
}

# Large版配置
{
    "hidden_size": 1024,
    "num_attention_heads": 16,
    "num_hidden_layers": 24, 
    "intermediate_size": 4096
}
```

<font style="color:rgb(51, 51, 51);">总参数量：Base版约125M，Large版约355M</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **数据预处理**
    - <font style="color:rgb(51, 51, 51);">使用完整句子（非NSP格式）</font>
    - <font style="color:rgb(51, 51, 51);">最大序列长度512</font>
    - <font style="color:rgb(51, 51, 51);">动态Masking比例15%（其中80%替换为[MASK]，10%随机词，10%原词）</font>
2. **优化配置**
    - <font style="color:rgb(51, 51, 51);">优化器：AdamW (β1=0.9, β2=0.98)</font>
    - <font style="color:rgb(51, 51, 51);">学习率：峰值6e-4（warmup步数24k）</font>
    - <font style="color:rgb(51, 51, 51);">Batch Size：8,000（通过梯度累积实现）</font>
3. **训练时长**
    - <font style="color:rgb(51, 51, 51);">100万步（约500 epochs on BOOKCORPUS）</font>
    - <font style="color:rgb(51, 51, 51);">硬件：1024块V100 GPU（约1天训练时间）</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">GLUE基准提升：相比BERT提高2-20个点</font>
+ <font style="color:rgb(51, 51, 51);">更强的上下文理解能力</font>
+ <font style="color:rgb(51, 51, 51);">证明充分训练的重要性</font>
+ <font style="color:rgb(51, 51, 51);">通用性优于原始BERT</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算资源消耗巨大（300%于BERT）</font>
+ <font style="color:rgb(51, 51, 51);">Large版容易过拟合小数据集</font>
+ <font style="color:rgb(51, 51, 51);">领域迁移仍需微调</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">文本分类（金融新闻情感分析）</font>
+ <font style="color:rgb(51, 51, 51);">问答系统（开放域问答）</font>
+ <font style="color:rgb(51, 51, 51);">命名实体识别（医疗实体抽取）</font>
+ <font style="color:rgb(51, 51, 51);">文本生成（结合生成式架构）</font>
+ <font style="color:rgb(51, 51, 51);">语义相似度计算（法律条款匹配）</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **预训练增强**：
    - <font style="color:rgb(51, 51, 51);">ELECTRA式替换检测训练</font>
    - <font style="color:rgb(51, 51, 51);">混合精度训练优化</font>
    - <font style="color:rgb(51, 51, 51);">知识蒸馏得到轻量版（DistilRoBERTa）</font>
2. **架构改进**：
    - <font style="color:rgb(51, 51, 51);">集成稀疏注意力机制（Longformer式）</font>
    - <font style="color:rgb(51, 51, 51);">添加适配器层（Adapter-BERT变体）</font>
3. **领域适应**：
    - <font style="color:rgb(51, 51, 51);">继续在专业语料（如PubMed）上预训练</font>
    - <font style="color:rgb(51, 51, 51);">结合领域实体词典增强分词</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import RobertaModel, RobertaTokenizer

# 加载预训练模型
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaModel.from_pretrained('roberta-base')

# 文本编码示例
text = "The capital of France is [MASK]."
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

# 自定义训练循环（MLM任务）
from transformers import RobertaForMaskedLM

mlm_model = RobertaForMaskedLM.from_pretrained('roberta-base')
optimizer = torch.optim.AdamW(mlm_model.parameters(), lr=1e-5)

# 假设已准备batch数据
def train_step(batch):
    inputs = tokenizer(batch, padding=True, return_tensors="pt")
    inputs["labels"] = inputs.input_ids.detach().clone()
    
    # 随机mask部分token（15%）
    mask_prob = 0.15
    rand = torch.rand(inputs.input_ids.shape)
    mask_arr = (rand < mask_prob) * (inputs.input_ids != tokenizer.cls_token_id) * (inputs.input_ids != tokenizer.sep_token_id)
    
    for i in range(mask_arr.shape[0]):
        selection = torch.flatten(mask_arr[i].nonzero()).tolist()
        inputs.input_ids[i, selection] = tokenizer.mask_token_id
    
    outputs = mlm_model(**inputs)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    return loss.item()

```



## <font style="color:rgb(51, 51, 51);">DeBERTa</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">DeBERTa（</font>**<font style="color:rgb(51, 51, 51);">Decoding-enhanced BERT with Disentangled Attention</font>**<font style="color:rgb(51, 51, 51);">）由微软于2020年提出，旨在改进BERT和RoBERTa的不足。传统BERT模型使用绝对位置编码，但无法灵活捕捉相对位置关系；而DeBERTa通过</font>**<font style="color:rgb(51, 51, 51);">解耦注意力机制</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">增强的掩码解码器</font>**<font style="color:rgb(51, 51, 51);">，显著提升了模型对位置和内容信息的建模能力。DeBERTa在SuperGLUE等基准上表现优异，甚至超越人类基线。</font>

:::

<font style="color:rgb(51, 51, 51);">DeBERTa通过解耦注意力和增强解码器，显著提升了位置与内容建模能力，成为NLP领域的SOTA模型之一。其PyTorch实现可借助Hugging Face库快速集成，适用于多种复杂任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741162815117-02d2db36-4e99-44c9-98a7-5aec487d12e0.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

**解耦注意力（Disentangled Attention）**  
将每个token的注意力分为**内容相关**和**位置相关**两部分：

    - **<font style="color:rgb(51, 51, 51);">内容向量</font>**<font style="color:rgb(51, 51, 51);">：编码语义信息（类似BERT的词嵌入）。</font>
    - **<font style="color:rgb(51, 51, 51);">相对位置向量</font>**<font style="color:rgb(51, 51, 51);">：编码token间的相对位置偏移。  
</font><font style="color:rgb(51, 51, 51);">注意力权重由内容交互和位置交互共同决定，公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741162385687-7a2c0a26-dbbd-4f93-8056-857690007498.png)

其中，Q<sup>c</sup>/K<sup>c</sup>为内容查询/键，Q<sup>r</sup>/K<sup>p</sup>为位置相关的查询和键。

1. **增强的掩码解码器（EMD, Enhanced Mask Decoder）**  
在MLM任务中，预测被掩码token时额外引入**绝对位置嵌入**，结合内容与位置信息提升准确性。

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据源</font>**<font style="color:rgb(51, 51, 51);">：BookCorpus、英文维基百科、OpenWebText等，共约160GB文本。</font>
+ **<font style="color:rgb(51, 51, 51);">规模</font>**<font style="color:rgb(51, 51, 51);">：Base版本（12层）和Large版本（24层）分别使用不同规模数据训练。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">基础架构</font>**<font style="color:rgb(51, 51, 51);">：基于Transformer，层数与BERT/RoBERTa对齐。</font>
+ **<font style="color:rgb(51, 51, 51);">关键改进</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">解耦注意力层</font>**<font style="color:rgb(51, 51, 51);">：每个注意力头独立计算内容与位置交互。</font>
    - **<font style="color:rgb(51, 51, 51);">相对位置编码</font>**<font style="color:rgb(51, 51, 51);">：使用可学习的相对位置嵌入矩阵，窗口大小通常为512。</font>
    - **<font style="color:rgb(51, 51, 51);">增强解码器(EMD, </font>****Enhanced Mask Decoder****<font style="color:rgb(51, 51, 51);">)</font>**<font style="color:rgb(51, 51, 51);">：在最后一层添加绝对位置嵌入辅助预测。 BERT模型在输入层中合并了绝对位置。 在DeBERTa中，微软在所有Transformer层之后将它们合并，然后在softmax层之前进行 mask token 预测.这样，</font>**<font style="color:#74B602;">DeBERTa捕获了所有Transformer层中的相对位置，同时解码被mask的单词时将绝对位置用作补充信息 。 此即为 DeBERTa 增强型掩码解码器(EMD)</font>**<font style="color:rgb(51, 51, 51);">。</font>

| **模型** | **层数** | **隐藏层维度** | **注意力头数** | **参数量** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">DeBERTa-base</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">768</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">140M</font> |
| <font style="color:rgb(51, 51, 51);">DeBERTa-large</font> | <font style="color:rgb(51, 51, 51);">24</font> | <font style="color:rgb(51, 51, 51);">1024</font> | <font style="color:rgb(51, 51, 51);">16</font> | <font style="color:rgb(51, 51, 51);">350M</font> |


:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练**：
    - **<font style="color:rgb(51, 51, 51);">目标函数</font>**<font style="color:rgb(51, 51, 51);">：MLM（掩码语言建模），15%掩码比例，80%用[MASK]，10%随机替换，10%保留原词。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：AdamW（</font><font style="color:rgb(51, 51, 51);">β</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">0.9</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">β</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">0.98</font>_<font style="color:rgb(51, 51, 51);">β</font>_<font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">0.9</font><font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">β</font>_<font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">0.98</font><font style="color:rgb(51, 51, 51);">)，学习率1e-4，权重衰减0.01。</font>
    - **<font style="color:rgb(51, 51, 51);">批次大小</font>**<font style="color:rgb(51, 51, 51);">：2048，训练步数约500K。</font>
    - **<font style="color:rgb(51, 51, 51);">技术细节</font>**<font style="color:rgb(51, 51, 51);">：梯度累积、动态掩码、混合精度训练。</font>
2. **微调**：
    - <font style="color:rgb(51, 51, 51);">在下游任务（如GLUE）上微调，学习率降至5e-5，添加任务特定层。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">更高效的位置建模，长文本任务表现优异。</font>
    - <font style="color:rgb(51, 51, 51);">在SuperGLUE、SQuAD等任务中超越RoBERTa、ELECTRA。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算复杂度略高（因解耦注意力）。</font>
    - <font style="color:rgb(51, 51, 51);">预训练资源需求大。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">自然语言理解</font>**<font style="color:rgb(51, 51, 51);">：文本分类（如情感分析）、问答（SQuAD）。</font>
+ **<font style="color:rgb(51, 51, 51);">序列标注</font>**<font style="color:rgb(51, 51, 51);">：命名实体识别（NER）。</font>
+ **<font style="color:rgb(51, 51, 51);">生成任务</font>**<font style="color:rgb(51, 51, 51);">：文本摘要（需调整结构）。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">DeBERTa V2/V3</font>**<font style="color:rgb(51, 51, 51);">：引入</font>**<font style="color:rgb(51, 51, 51);">知识蒸馏</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(51, 51, 51);">更深的模型</font>**<font style="color:rgb(51, 51, 51);">（48层）和</font>**<font style="color:rgb(51, 51, 51);">更大规模数据</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">Efficient DeBERTa</font>**<font style="color:rgb(51, 51, 51);">：通过剪枝、量化降低推理成本。</font>
+ **<font style="color:rgb(51, 51, 51);">多语言扩展</font>**<font style="color:rgb(51, 51, 51);">：支持多语言联合预训练。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import DebertaV2Config, DebertaV2Model

# 自定义解耦注意力层（简化版）
class DisentangledAttention(nn.Module):
    def __init__(self, hidden_size, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        self.q_content = nn.Linear(hidden_size, hidden_size)
        self.k_content = nn.Linear(hidden_size, hidden_size)
        self.v_content = nn.Linear(hidden_size, hidden_size)
        self.q_pos = nn.Linear(hidden_size, hidden_size)
        self.k_pos = nn.Linear(hidden_size, hidden_size)
        # 相对位置嵌入（示例窗口为64）
        self.relative_position_bias = nn.Embedding(128, num_heads)

    def forward(self, hidden_states, rel_pos_ids):
        # 内容投影
        q_c = self.q_content(hidden_states)
        k_c = self.k_content(hidden_states)
        v_c = self.v_content(hidden_states)
        # 位置投影
        q_p = self.q_pos(hidden_states)
        k_p = self.k_pos(hidden_states)
        
        # 拆分多头
        q_c = q_c.view(q_c.size(0), q_c.size(1), self.num_heads, self.head_dim).permute(0,2,1,3)
        k_c = k_c.view(k_c.size(0), k_c.size(1), self.num_heads, self.head_dim).permute(0,2,3,1)
        v_c = v_c.view(v_c.size(0), v_c.size(1), self.num_heads, self.head_dim).permute(0,2,1,3)
        
        # 内容注意力得分
        attn_scores = torch.matmul(q_c, k_c) / (self.head_dim ** 0.5)
        
        # 相对位置偏置
        rel_pos_bias = self.relative_position_bias(rel_pos_ids).permute(0,3,1,2)
        attn_scores += rel_pos_bias
        
        # Softmax & 加权
        attn_probs = nn.Softmax(dim=-1)(attn_scores)
        context = torch.matmul(attn_probs, v_c)
        context = context.permute(0,2,1,3).contiguous().flatten(-2)
        return context

# 使用Hugging Face实现（推荐）
config = DebertaV2Config()
model = DebertaV2Model(config)
input_ids = torch.randint(0, 100, (2, 128))
outputs = model(input_ids)

```

## <font style="color:rgb(51, 51, 51);">ALBERT</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ALBERT（A Lite BERT）由Google于2019年提出，旨在解决BERT模型参数量过大、训练效率低的问题。BERT虽然性能优异，但其参数量（如BERT-large有340M参数）导致训练成本高且难以部署到资源受限的环境。</font>**<font style="color:#ED740C;">ALBERT通过参数压缩和训练任务优化，在减少参数量的同时保持了模型性能。</font>**

论文：[ALBERT: A Lite BERT for Self-supervised Learning of Language Representations](https://link.zhihu.com/?target=https%3A//paperswithcode.com/paper/albert-a-lite-bert-for-self-supervised)

:::

<font style="color:rgb(51, 51, 51);">ALBERT通过参数分解和共享大幅降低模型体积，SOP任务增强了句间关系建模，是轻量级预训练模型的经典代表。后续可结合动态共享或蒸馏技术进一步优化。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741163192333-292a111a-4118-4b00-b059-8cd4b2ccd9c4.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **参数分解（Factorized Embedding Parameterization）**  
将词嵌入矩阵分解为两个小矩阵：词表→低维嵌入（`V×E`）和低维→隐藏层（`E×H`）。例如，原BERT嵌入参数量为`V×H`，分解后变为`V×E + E×H`（通常`E=128`, `H=768`），显著减少参数。
2. **跨层参数共享（Cross-layer Parameter Sharing）**  
所有Transformer层共享同一组参数（包括自注意力和FFN）。即使增加层数，总参数量也仅线性增长，而非BERT的平方增长。
3. **句子顺序预测（Sentence Order Prediction, SOP）**  
替换BERT的下一句预测（NSP）任务，SOP的正样本为连续段落中两个顺序正确的句子，负样本为调换顺序的句子，迫使模型学习更细粒度的句间关系。

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：与BERT类似，使用BooksCorpus（800M词）和英文Wikipedia（2,500M词）。</font>
+ **<font style="color:rgb(51, 51, 51);">输入格式</font>**<font style="color:rgb(51, 51, 51);">：句子对（Segment）最大长度512，通过MLM和SOP任务进行预训练。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">嵌入层</font>**<font style="color:rgb(51, 51, 51);">：分解后的嵌入（词嵌入 + 位置嵌入 + 段落嵌入）。</font>
2. **<font style="color:rgb(51, 51, 51);">编码器</font>**<font style="color:rgb(51, 51, 51);">：多层Transformer，每层参数共享。</font>
3. **<font style="color:rgb(51, 51, 51);">预训练头</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">MLM Head</font>**<font style="color:rgb(51, 51, 51);">：预测被掩码的单词。</font>
    - **<font style="color:rgb(51, 51, 51);">SOP Head</font>**<font style="color:rgb(51, 51, 51);">：二分类判断句子顺序。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练**：
    - **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：随机掩码15%的Token（其中80%替换为[MASK]，10%随机替换，10%不变）。</font>
    - **<font style="color:rgb(51, 51, 51);">任务</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">MLM：交叉熵损失。</font>
        * <font style="color:rgb(51, 51, 51);">SOP：二分类交叉熵损失。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：LAMB（Layer-wise Adaptive Moments）或AdamW，学习率1e-4，Batch Size 4096。</font>
2. **微调**：针对下游任务（如GLUE）添加任务特定层，微调全部参数。

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">参数减少约89%（ALBERT-xxlarge仅235M参数，性能超越BERT-large）。</font>
    - <font style="color:rgb(51, 51, 51);">训练更快，内存占用更低。</font>
    - <font style="color:rgb(51, 51, 51);">SOP任务提升句间关系建模能力。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">参数共享可能限制模型表达能力，需增加层数补偿。</font>
    - <font style="color:rgb(51, 51, 51);">推理速度因层数增加未显著提升。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">资源受限环境</font>**<font style="color:rgb(51, 51, 51);">：移动端NLP应用（如实时翻译）。</font>
+ **<font style="color:rgb(51, 51, 51);">长文本建模</font>**<font style="color:rgb(51, 51, 51);">：如文档分类、问答系统。</font>
+ **<font style="color:rgb(51, 51, 51);">学术研究</font>**<font style="color:rgb(51, 51, 51);">：轻量级模型设计的基准。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">动态参数共享</font>**<font style="color:rgb(51, 51, 51);">：按层相似性动态决定共享策略。</font>
2. **<font style="color:rgb(51, 51, 51);">知识蒸馏</font>**<font style="color:rgb(51, 51, 51);">：用ALBERT作为教师模型压缩更小的学生模型。</font>
3. **<font style="color:rgb(51, 51, 51);">混合任务训练</font>**<font style="color:rgb(51, 51, 51);">：结合其他预训练任务（如实体预测）。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import AlbertConfig

class AlbertEmbeddings(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.embedding_size)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.embedding_size)
        self.token_type_embeddings = nn.Embedding(config.type_vocab_size, config.embedding_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=1e-12)
        self.projection = nn.Linear(config.embedding_size, config.hidden_size)

    def forward(self, input_ids, token_type_ids=None, position_ids=None):
        seq_length = input_ids.size(1)
        if position_ids is None:
            position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device).unsqueeze(0)
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)
        
        word_embeds = self.word_embeddings(input_ids)
        position_embeds = self.position_embeddings(position_ids)
        token_type_embeds = self.token_type_embeddings(token_type_ids)
        embeddings = word_embeds + position_embeds + token_type_embeds
        embeddings = self.projection(embeddings)
        embeddings = self.LayerNorm(embeddings)
        return embeddings

class AlbertLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attention = nn.MultiheadAttention(config.hidden_size, config.num_attention_heads)
        self.ffn = nn.Sequential(
            nn.Linear(config.hidden_size, config.intermediate_size),
            nn.GELU(),
            nn.Linear(config.intermediate_size, config.hidden_size)
        )
        self.LayerNorm1 = nn.LayerNorm(config.hidden_size)
        self.LayerNorm2 = nn.LayerNorm(config.hidden_size)

    def forward(self, hidden_states, attention_mask=None):
        attn_output, _ = self.attention(hidden_states, hidden_states, hidden_states, key_padding_mask=attention_mask)
        hidden_states = self.LayerNorm1(attn_output + hidden_states)
        ffn_output = self.ffn(hidden_states)
        hidden_states = self.LayerNorm2(ffn_output + hidden_states)
        return hidden_states

class AlbertModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.embeddings = AlbertEmbeddings(config)
        self.encoder = nn.ModuleList([AlbertLayer(config) for _ in range(config.num_hidden_layers)])

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        embedding_output = self.embeddings(input_ids, token_type_ids=token_type_ids)
        hidden_states = embedding_output
        for layer_module in self.encoder:
            hidden_states = layer_module(hidden_states, attention_mask)
        return hidden_states

# 示例配置
config = AlbertConfig(
    vocab_size=30000,
    embedding_size=128,
    hidden_size=768,
    num_hidden_layers=12,
    num_attention_heads=12,
    intermediate_size=3072,
    max_position_embeddings=512
)

model = AlbertModel(config)
input_ids = torch.randint(0, 30000, (1, 128))
output = model(input_ids)
print(output.shape)  # torch.Size([1, 128, 768])

```

# T5（**<font style="color:rgb(51, 51, 51);">Text-to-Text Transfer Transformer</font>**）
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">T5（</font>**<font style="color:rgb(51, 51, 51);">Text-to-Text Transfer Transformer</font>**<font style="color:rgb(51, 51, 51);">）由Google Research于2019年提出，核心思想是将</font>**<font style="color:rgb(51, 51, 51);">所有自然语言处理任务统一为“文本到文本”的生成任务</font>**<font style="color:rgb(51, 51, 51);">。其目标是通过单一模型架构和训练框架，覆盖分类、翻译、摘要、问答等多种任务，简化传统任务特定模型的复杂性。</font>

**参考**：[https://zhuanlan.zhihu.com/p/589869911](https://zhuanlan.zhihu.com/p/589869911)

:::

<font style="color:rgb(51, 51, 51);">T5通过统一的文本到文本框架，实现了多任务建模的简洁性和高效性，成为生成式NLP任务的基准模型。其开源实现（如Hugging Face库）大幅降低了应用门槛，后续改进方向包括效率优化、多模态扩展等。</font>

<font style="color:rgb(77, 77, 77);">下图所示为T5的输入格式和输出格式。绿色部分表示翻译任务，红色和黄色部分分别表示CoLA（单句分类）和STS-B（文本语义相似度）任务，蓝色部分表示摘要生成任务，左侧的框表示T5的输入样例，右侧的框则是对应的输出结果。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741164464464-478d6cc3-69f8-419c-bdf1-39d8a521249e.png)

<font style="color:rgb(77, 77, 77);">T5唯一需要做的就是在输入数据前加上任务声明前缀，如：</font>

+ <font style="color:rgba(0, 0, 0, 0.75);">英德翻译：</font>**<font style="color:rgba(0, 0, 0, 0.75);">translate English to German</font>**<font style="color:rgba(0, 0, 0, 0.75);">：That is good.</font>
+ <font style="color:rgba(0, 0, 0, 0.75);">情感分类：</font>**<font style="color:rgba(0, 0, 0, 0.75);">sentiment</font>**<font style="color:rgba(0, 0, 0, 0.75);">：This movie is terrible!</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **文本到文本的统一框架**  
所有任务均以文本输入输出形式处理，例如：
    - **<font style="color:rgb(51, 51, 51);">分类任务</font>**<font style="color:rgb(51, 51, 51);">：输入文本→输出类别标签（如</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">"positive"</font>`<font style="color:rgb(51, 51, 51);">）。</font>
    - **<font style="color:rgb(51, 51, 51);">翻译任务</font>**<font style="color:rgb(51, 51, 51);">：输入</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">"translate English to German: ..."</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">→ 输出德语句子。</font>
    - **<font style="color:rgb(51, 51, 51);">摘要任务</font>**<font style="color:rgb(51, 51, 51);">：输入</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">"summarize: ..."</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">→ 输出摘要文本。</font>
2. **Span Corruption预训练任务**  
改进传统掩码语言建模（MLM），随机掩码连续片段（span），如：

```plain
输入：Thank you <X> me to your party <Y> week.  
输出：<X> for inviting <Y> last <Z>
```

模型需预测被掩码的完整span（`<X>`和`<Y>`为掩码标记，`<Z>`为结束符）。

3. **系统化架构探索**  
通过消融实验验证关键设计选择，例如：
    - **<font style="color:rgb(51, 51, 51);">Encoder-Decoder结构</font>**<font style="color:rgb(51, 51, 51);">优于仅Encoder（BERT）或仅Decoder（GPT）。</font>
    - **<font style="color:rgb(51, 51, 51);">相对位置编码</font>**<font style="color:rgb(51, 51, 51);">（Relative Position Bias）优于绝对位置编码。</font>
    - **<font style="color:rgb(51, 51, 51);">模型缩放策略</font>**<font style="color:rgb(51, 51, 51);">（如增加深度而非宽度）。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">预训练数据</font>**<font style="color:rgb(51, 51, 51);">：C4（Colossal Clean Crawled Corpus）数据集，包含约750GB的英文网页文本（经去重、过滤低质量内容等处理）。</font>
+ **<font style="color:rgb(51, 51, 51);">微调数据</font>**<font style="color:rgb(51, 51, 51);">：涵盖GLUE、SuperGLUE、CNN/DailyMail（摘要）、WMT（翻译）等任务数据集。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51);">T5基于标准</font>**<font style="color:rgb(51, 51, 51);">Transformer Encoder-Decoder架构</font>**<font style="color:rgb(51, 51, 51);">，主要调整包括：</font>

+ **<font style="color:rgb(51, 51, 51);">相对位置编码</font>**<font style="color:rgb(51, 51, 51);">：在自注意力中引入位置偏置矩阵，公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741164252567-2c9f11bb-e171-46c8-994f-851bb19c8dd5.png)

<font style="color:rgb(51, 51, 51);">其中，b</font><sub><font style="color:rgb(51, 51, 51);">i−j</font></sub><font style="color:rgb(51, 51, 51);">为可学习的相对位置偏置。</font>

+ **<font style="color:rgb(51, 51, 51);">Layer Normalization位置</font>**<font style="color:rgb(51, 51, 51);">：置于残差连接前（Pre-LN）。</font>
+ **<font style="color:rgb(51, 51, 51);">FFN层</font>**<font style="color:rgb(51, 51, 51);">：使用GELU激活函数，中间维度为 d</font><sub><font style="color:rgb(51, 51, 51);">ff</font></sub><font style="color:rgb(51, 51, 51);">=4×d</font><sub><font style="color:rgb(51, 51, 51);">model</font></sub><font style="color:rgb(51, 51, 51);">。</font>

| **模型** | **层数（Encoder/Decoder）** | **隐藏层维度** | **注意力头数** | **参数量** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">T5-small</font> | <font style="color:rgb(51, 51, 51);">6/6</font> | <font style="color:rgb(51, 51, 51);">512</font> | <font style="color:rgb(51, 51, 51);">8</font> | <font style="color:rgb(51, 51, 51);">60M</font> |
| <font style="color:rgb(51, 51, 51);">T5-base</font> | <font style="color:rgb(51, 51, 51);">12/12</font> | <font style="color:rgb(51, 51, 51);">768</font> | <font style="color:rgb(51, 51, 51);">12</font> | <font style="color:rgb(51, 51, 51);">220M</font> |
| <font style="color:rgb(51, 51, 51);">T5-large</font> | <font style="color:rgb(51, 51, 51);">24/24</font> | <font style="color:rgb(51, 51, 51);">1024</font> | <font style="color:rgb(51, 51, 51);">16</font> | <font style="color:rgb(51, 51, 51);">770M</font> |
| <font style="color:rgb(51, 51, 51);">T5-3B</font> | <font style="color:rgb(51, 51, 51);">24/24</font> | <font style="color:rgb(51, 51, 51);">1024</font> | <font style="color:rgb(51, 51, 51);">32</font> | <font style="color:rgb(51, 51, 51);">3B</font> |


:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练**：
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：Span Corruption（</font>**<font style="color:#74B602;">掩码连续片段</font>**<font style="color:rgb(51, 51, 51);">，平均长度3，掩码率15%）。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：AdaFactor（节省显存），学习率1e-3，线性预热（10k步），批次大小128（序列长度512）。</font>
    - **<font style="color:rgb(51, 51, 51);">训练量</font>**<font style="color:rgb(51, 51, 51);">：1M步（约34B tokens）。</font>
2. **微调**：
    - <font style="color:rgb(51, 51, 51);">全量更新模型参数，任务指令通过前缀添加到输入（如</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">"translate English to German: ..."</font>`<font style="color:rgb(51, 51, 51);">）。</font>
    - <font style="color:rgb(51, 51, 51);">多任务微调时，混合多个数据集并添加任务前缀。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">任务无关性</font>**<font style="color:rgb(51, 51, 51);">：单一模型处理多种任务，降低部署复杂度。</font>
    - **<font style="color:rgb(51, 51, 51);">强泛化能力</font>**<font style="color:rgb(51, 51, 51);">：在低资源任务（如小样本学习）上表现优异。</font>
    - **<font style="color:rgb(51, 51, 51);">可解释性</font>**<font style="color:rgb(51, 51, 51);">：通过前缀指令显式控制任务类型。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">生成效率低</font>**<font style="color:rgb(51, 51, 51);">：Encoder-Decoder结构比纯Decoder（如GPT）解码速度慢。</font>
    - **<font style="color:rgb(51, 51, 51);">显存占用高</font>**<font style="color:rgb(51, 51, 51);">：大模型（如T5-3B）需要大量计算资源。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">文本生成</font>**<font style="color:rgb(51, 51, 51);">：摘要、翻译、对话生成。</font>
+ **<font style="color:rgb(51, 51, 51);">序列标注</font>**<font style="color:rgb(51, 51, 51);">：命名实体识别（输出实体列表）。</font>
+ **<font style="color:rgb(51, 51, 51);">问答系统</font>**<font style="color:rgb(51, 51, 51);">：开放域问答（如输入问题→直接生成答案）。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：生成合成训练数据。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">mT5</font>**<font style="color:rgb(51, 51, 51);">：扩展为多语言版本，支持101种语言。</font>
2. **<font style="color:rgb(51, 51, 51);">T5-UL2</font>**<font style="color:rgb(51, 51, 51);">：引入混合预训练目标（Span Corruption + Prefix LM）。</font>
3. **<font style="color:rgb(51, 51, 51);">压缩与蒸馏</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">T5-small</font>**<font style="color:rgb(51, 51, 51);">：直接缩小模型尺寸。</font>
    - **<font style="color:rgb(51, 51, 51);">Distilled-T5</font>**<font style="color:rgb(51, 51, 51);">：用教师模型（T5-large）蒸馏到学生模型。</font>
4. **<font style="color:rgb(51, 51, 51);">领域适配</font>**<font style="color:rgb(51, 51, 51);">：在特定领域数据（医学、法律）上继续预训练。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch.nn as nn

class T5Block(nn.Module):
    def __init__(self, d_model=512, n_heads=8, d_ff=2048):
        super().__init__()
        # 自注意力（带相对位置编码）
        self.self_attn = nn.MultiheadAttention(d_model, n_heads)
        self.layer_norm1 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(0.1)
        
        # FFN层
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(d_ff, d_model)
        )
        self.layer_norm2 = nn.LayerNorm(d_model)
        self.dropout2 = nn.Dropout(0.1)

    def forward(self, x, attention_mask=None):
        # 自注意力（简化版，未实现相对位置编码）
        attn_output, _ = self.self_attn(x, x, x, key_padding_mask=attention_mask)
        x = x + self.dropout1(attn_output)
        x = self.layer_norm1(x)
        
        # FFN
        ffn_output = self.ffn(x)
        x = x + self.dropout2(ffn_output)
        x = self.layer_norm2(x)
        return x

```

```python
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# 加载模型与分词器
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# 示例：翻译任务
input_text = "translate English to German: The house is wonderful."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

# 生成输出
outputs = model.generate(input_ids, max_length=50)
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded_output)  # 输出：Das Haus ist wunderbar.

# 自定义训练循环（简化版）
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
for batch in dataloader:
    input_ids = batch["input_ids"]
    labels = batch["labels"]
    outputs = model(input_ids=input_ids, labels=labels)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

```



# 中文embedding系列
## 模型对比
:::color5
**<font style="color:#601BDE;">背景</font>**<font style="color:#601BDE;">：</font>

:::

| **模型** | **背景** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">由Google于2018年提出，基于Transformer的Encoder架构，通过掩码语言建模（MLM）和下一句预测（NSP）任务预训练，开启了NLP领域的大规模预训练模型时代。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">由Moka AI于2023年发布，专注于</font>**<font style="color:rgb(51, 51, 51);">多语言密集文本嵌入</font>**<font style="color:rgb(51, 51, 51);">，强调跨语言语义对齐能力，适用于多语言检索和相似度计算场景。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">由北京智源研究院（BAAI）于2023年推出，基于大规模对比学习训练，优化了文本嵌入的区分能力，支持中英文混合任务，在检索和语义匹配任务中表现突出。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">由阿里巴巴达摩院于2023年提出，面向通用文本嵌入（</font>**<font style="color:rgb(51, 51, 51);">General Text Embedding</font>**<font style="color:rgb(51, 51, 51);">），通过多任务联合训练（检索、分类、生成）增强嵌入的泛化性，适用于复杂语义理解场景。</font> |


:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

| **模型** | **创新点** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">1. 提出</font>**<font style="color:#ED740C;">双向Transformer Encoder架构</font>**<font style="color:rgb(51, 51, 51);">；   </font><font style="color:rgb(51, 51, 51);">2. 掩码语言建模（MLM）捕捉上下文依赖；   </font><font style="color:rgb(51, 51, 51);">3. 下一句预测（NSP）任务增强句间关系建模。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">1. 多语言混合训练（100+语言），支持跨语言语义对齐；   </font><font style="color:rgb(51, 51, 51);">2. 引入</font>**<font style="color:#ED740C;">动态负采样策略</font>**<font style="color:rgb(51, 51, 51);">，提升难负例区分能力；   </font><font style="color:rgb(51, 51, 51);">3. 融合词级和句级嵌入增强细粒度语义表示。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">1. </font>**<font style="color:#ED740C;">对比学习优化（InfoNCE损失）结合难负例挖掘</font>**<font style="color:rgb(51, 51, 51);">；   </font><font style="color:rgb(51, 51, 51);">2. 动态温度系数调节相似度分布；   </font><font style="color:rgb(51, 51, 51);">3. 混合数据增强（文本改写、实体替换）提升鲁棒性。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">1. </font>**<font style="color:#ED740C;">多任务联合训练框架（检索+分类+生成）</font>**<font style="color:rgb(51, 51, 51);">；   </font><font style="color:rgb(51, 51, 51);">2. 自适应嵌入融合机制，动态加权不同任务的特征；   </font><font style="color:rgb(51, 51, 51);">3. 引入知识蒸馏压缩模型，平衡性能与效率。</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **模型** | **训练数据** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">英文：BookCorpus + 英文维基百科（共16GB）；   </font><font style="color:rgb(51, 51, 51);">多语言版（mBERT）：104种语言的维基百科。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">多语言混合数据（100+语言），包括Wikipedia、CCNet、平行语料库，总量超100TB。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">中英文混合数据：中文维基、百度百科、社区论坛文本；英文Wikipedia、Common Crawl；总量50TB。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">多领域数据：电商评论、新闻、社交媒体、学术论文（中英混合），总量200TB，含人工标注的语义相似度标签。</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

| **模型** | **模型结构** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">Transformer Encoder（Base: 12层，Hidden=768；Large: 24层，Hidden=1024），输出[CLS]向量或词嵌入。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">双塔结构：独立Query和Document编码器（基于RoBERTa），共享底层参数；加入跨语言注意力模块；嵌入维度1024。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">基于ELECTRA架构的Generator-Discriminator双塔，Discriminator输出嵌入；嵌入维度768，支持最大序列长度512。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">混合架构：Encoder-Decoder（类似T5）用于生成任务，双塔Encoder用于检索任务；嵌入维度1024，支持动态维度压缩。</font> |


:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

| **模型** | **训练步骤** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">1. 预训练：MLM（15%掩码率）+ NSP任务，AdamW优化器，学习率1e-4；   </font><font style="color:rgb(51, 51, 51);">2. 微调：任务特定层（如分类头）训练。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">1. 多语言对比学习：跨语言正样本对（平行语料） + 动态负采样；   </font><font style="color:rgb(51, 51, 51);">2. 两阶段训练：词向量预训练 + 句向量微调；   </font><font style="color:rgb(51, 51, 51);">3. 混合精度训练，批次大小8192。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">1. 基于ELECTRA的替换token检测（RTD）预训练；   </font><font style="color:rgb(51, 51, 51);">2. 对比学习微调：难负例挖掘 + 动态温度系数调整；   </font><font style="color:rgb(51, 51, 51);">3. 数据增强：文本回译、实体替换。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">1. 多任务联合训练：检索（对比学习）、分类（交叉熵）、生成（文本重构）；   </font><font style="color:rgb(51, 51, 51);">2. 自适应损失加权：根据任务难度动态调整权重；   </font><font style="color:rgb(51, 51, 51);">3. 知识蒸馏：从大模型（如GPT-4）蒸馏到轻量级GTE模型。</font> |


:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **模型** | **优点** | **缺点** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">1. 通用性强，适合多种NLP任务；   </font><font style="color:rgb(51, 51, 51);">2. 社区支持完善，生态丰富。</font> | <font style="color:rgb(51, 51, 51);">1. 嵌入质量受限于[CLS]向量；   </font><font style="color:rgb(51, 51, 51);">2. 长文本处理能力弱。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">1. 多语言支持优异；   </font><font style="color:rgb(51, 51, 51);">2. 细粒度语义表示能力强。</font> | <font style="color:rgb(51, 51, 51);">1. 训练资源消耗大；   </font><font style="color:rgb(51, 51, 51);">2. 对低资源语言覆盖有限。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">1. 中英文混合任务表现最佳；   </font><font style="color:rgb(51, 51, 51);">2. 对比学习优化，难负例区分度高。</font> | <font style="color:rgb(51, 51, 51);">1. 模型尺寸较大（Large版本1.3B参数）；   </font><font style="color:rgb(51, 51, 51);">2. 生成任务支持不足。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">1. 多任务泛化能力强；   </font><font style="color:rgb(51, 51, 51);">2. 支持动态嵌入压缩，适合端侧部署。</font> | <font style="color:rgb(51, 51, 51);">1. 训练复杂度高；   </font><font style="color:rgb(51, 51, 51);">2. 需要大量标注数据。</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

| **模型** | **应用场景** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">文本分类、实体识别、问答系统、句子对分类（如NLI）。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">跨语言检索、多语言语义相似度计算、跨境电商商品匹配。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">中文问答、社区内容去重、法律文档检索。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">多模态检索（文本+图像）、复杂查询理解、智能客服对话增强。</font> |


:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

| **模型** | **改进方向** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">BERT</font>** | <font style="color:rgb(51, 51, 51);">1. 长文本优化（如Longformer）；   </font><font style="color:rgb(51, 51, 51);">2. 嵌入后处理（如BERT-flow）；   </font><font style="color:rgb(51, 51, 51);">3. 结合知识图谱（如ERNIE）。</font> |
| **<font style="color:rgb(51, 51, 51);">M3E</font>** | <font style="color:rgb(51, 51, 51);">1. 低资源语言增强；   </font><font style="color:rgb(51, 51, 51);">2. 嵌入量化压缩；   </font><font style="color:rgb(51, 51, 51);">3. 结合跨模态对齐（图文检索）。</font> |
| **<font style="color:rgb(51, 51, 51);">BGE</font>** | <font style="color:rgb(51, 51, 51);">1. 轻量化版本（Tiny-BGE）；   </font><font style="color:rgb(51, 51, 51);">2. 多任务微调框架；   </font><font style="color:rgb(51, 51, 51);">3. 融合生成式检索（如RAG）。</font> |
| **<font style="color:rgb(51, 51, 51);">GTE</font>** | <font style="color:rgb(51, 51, 51);">1. 端侧部署优化（如ONNX量化）；   </font><font style="color:rgb(51, 51, 51);">2. 多模态扩展（文本+语音）；   </font><font style="color:rgb(51, 51, 51);">3. 增量学习支持动态数据更新。</font> |




## M3E
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">M3E（Moka Massive Mixed Embedding）</font>

+ **<font style="color:rgb(51, 51, 51);">文本嵌入需求</font>**<font style="color:rgb(51, 51, 51);">：在NLP任务中（如语义检索、聚类、相似度计算），高质量的向量表示是关键。</font>
+ **<font style="color:rgb(51, 51, 51);">中文领域痛点</font>**<font style="color:rgb(51, 51, 51);">：传统模型如BERT在中文任务中存在领域适配不足、语义粒度粗糙问题。</font>
+ **<font style="color:rgb(51, 51, 51);">M3E定位</font>**<font style="color:rgb(51, 51, 51);">：由Moka公司开源，针对中文场景设计，通过混合训练策略提升多领域泛化能力。</font>

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">混合训练数据</font>**<font style="color:rgb(51, 51, 51);">：融合多领域（通用、金融、医疗等）及多类型（问答、段落、关键词）语料，覆盖长尾场景。</font>
+ **<font style="color:rgb(51, 51, 51);">指令微调优化</font>**<font style="color:rgb(51, 51, 51);">：引入指令形式的文本对（如“查询：... 相关文档：...”），增强模型对任务意图的理解。</font>
+ **<font style="color:rgb(51, 51, 51);">动态负采样</font>**<font style="color:rgb(51, 51, 51);">：训练中动态生成困难负例（Hard Negative），提升语义区分能力。</font>
+ **<font style="color:rgb(51, 51, 51);">轻量化设计</font>**<font style="color:rgb(51, 51, 51);">：相比同类模型参数量更低（如base版约110M），但通过训练策略优化保持高性能。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据构成</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">公开数据集：如中文维基、CMRC2018、PAWS-X等。</font>
    - <font style="color:rgb(51, 51, 51);">自建数据：爬取多领域网页文本，经去噪、去重处理。</font>
    - <font style="color:rgb(51, 51, 51);">合成数据：通过回译、文本改写生成语义相似对。</font>
+ **<font style="color:rgb(51, 51, 51);">数据量级</font>**<font style="color:rgb(51, 51, 51);">：总训练样本超10亿对，覆盖中英文混合场景。</font>

| <font style="color:rgb(31, 35, 40);">数据集名称</font> | <font style="color:rgb(31, 35, 40);">领域</font> | <font style="color:rgb(31, 35, 40);">数量</font> | <font style="color:rgb(31, 35, 40);">任务类型</font> | <font style="color:rgb(31, 35, 40);">Prompt</font> | <font style="color:rgb(31, 35, 40);">质量</font> | <font style="color:rgb(31, 35, 40);">说明</font> |
| --- | --- | --- | --- | --- | --- | --- |
| <font style="color:rgb(31, 35, 40);">cmrc2018</font> | <font style="color:rgb(31, 35, 40);">百科</font> | <font style="color:rgb(31, 35, 40);">14,363</font> | <font style="color:rgb(31, 35, 40);">问答</font> | <font style="color:rgb(31, 35, 40);">问答</font> | <font style="color:rgb(31, 35, 40);">优</font> | [https://github.com/ymcui/cmrc2018/blob/master/README_CN.md](https://github.com/ymcui/cmrc2018/blob/master/README_CN.md)<br/><font style="color:rgb(31, 35, 40);"> </font><font style="color:rgb(31, 35, 40);">专家标注的基于维基百科的中文阅读理解数据集，将问题和上下文视为正例</font> |
| <font style="color:rgb(31, 35, 40);">belle_2m</font> | <font style="color:rgb(31, 35, 40);">百科</font> | <font style="color:rgb(31, 35, 40);">2,000,000</font> | <font style="color:rgb(31, 35, 40);">指令微调</font> | <font style="color:rgb(31, 35, 40);">无</font> | <font style="color:rgb(31, 35, 40);">优</font> | <font style="color:rgb(31, 35, 40);">belle 的指令微调数据集，使用 self instruct 方法基于 gpt3.5 生成</font> |
| <font style="color:rgb(31, 35, 40);">firefily</font> | <font style="color:rgb(31, 35, 40);">百科</font> | <font style="color:rgb(31, 35, 40);">1,649,399</font> | <font style="color:rgb(31, 35, 40);">指令微调</font> | <font style="color:rgb(31, 35, 40);">无</font> | <font style="color:rgb(31, 35, 40);">优</font> | <font style="color:rgb(31, 35, 40);">Firefly（流萤） 是一个开源的中文对话式大语言模型，使用指令微调（Instruction Tuning）在中文数据集上进行调优。使用了词表裁剪、ZeRO等技术，有效降低显存消耗和提高训练效率。 在训练中，我们使用了更小的模型参数量，以及更少的计算资源。</font> |
| <font style="color:rgb(31, 35, 40);">alpaca_gpt4</font> | <font style="color:rgb(31, 35, 40);">百科</font> | <font style="color:rgb(31, 35, 40);">48,818</font> | <font style="color:rgb(31, 35, 40);">指令微调</font> | <font style="color:rgb(31, 35, 40);">无</font> | <font style="color:rgb(31, 35, 40);">优</font> | <font style="color:rgb(31, 35, 40);">本数据集是参考Alpaca方法基于GPT4得到的self-instruct数据，约5万条。</font> |
| <font style="color:rgb(31, 35, 40);">...</font> | <font style="color:rgb(31, 35, 40);"></font> | <font style="color:rgb(31, 35, 40);"></font> | <font style="color:rgb(31, 35, 40);"></font> | <font style="color:rgb(31, 35, 40);"></font> | <font style="color:rgb(31, 35, 40);"></font> | <font style="color:rgb(31, 35, 40);"></font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">基础架构</font>**<font style="color:rgb(51, 51, 51);">：基于BERT的Transformer变体，主要调整包括：</font>
    - **<font style="color:rgb(51, 51, 51);">Tokenization</font>**<font style="color:rgb(51, 51, 51);">：扩展词表至6万+，优化中文分词覆盖率。</font>
    - **<font style="color:rgb(51, 51, 51);">Pooling策略</font>**<font style="color:rgb(51, 51, 51);">：采用[CLS]向量+动态均值池化的混合输出。</font>
    - **<font style="color:rgb(51, 51, 51);">层次化参数</font>**<font style="color:rgb(51, 51, 51);">：深层Transformer层使用更宽隐藏层（1024维）。</font>
+ **<font style="color:rgb(51, 51, 51);">参数规模</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Base版：12层，768隐藏层，12头注意力（110M参数）</font>
    - <font style="color:rgb(51, 51, 51);">Large版：24层，1024隐藏层，16头（340M参数）</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">预训练阶段</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用MLM（Masked Language Model）任务初始化参数，数据占比30%。</font>
2. **<font style="color:rgb(51, 51, 51);">对比学习阶段</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">核心训练流程，采用InfoNCE损失函数。</font>
    - <font style="color:rgb(51, 51, 51);">正例：文本对（同义/相关）；负例：Batch内随机采样+动态生成困难负例。</font>
3. **<font style="color:rgb(51, 51, 51);">指令微调阶段</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">引入指令前缀（如“为这个句子生成嵌入：...”），使用MSE损失对齐不同指令格式的输出。</font>
4. **<font style="color:rgb(51, 51, 51);">多任务联合训练</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">同时优化对比损失、MLM损失和分类损失，增强模型鲁棒性。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">中文场景SOTA：在中文STS等任务上超越text-embedding-ada-002。</font>
    - <font style="color:rgb(51, 51, 51);">领域泛化性强：金融、医疗等领域zero-shot表现优异。</font>
    - <font style="color:rgb(51, 51, 51);">推理效率高：比同等参数模型快1.5倍。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">长文本处理：对超长文本（>512 tokens）的语义融合能力有限。</font>
    - <font style="color:rgb(51, 51, 51);">多语言支持弱：主要面向中英文，小语种表现一般。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">语义检索</font>**<font style="color:rgb(51, 51, 51);">：电商搜索Query-Doc匹配（如JD商品搜索）</font>
+ **<font style="color:rgb(51, 51, 51);">文本聚类</font>**<font style="color:rgb(51, 51, 51);">：社交媒体评论主题归纳</font>
+ **<font style="color:rgb(51, 51, 51);">问答系统</font>**<font style="color:rgb(51, 51, 51);">：FAQ库的意图相似度匹配</font>
+ **<font style="color:rgb(51, 51, 51);">去重检测</font>**<font style="color:rgb(51, 51, 51);">：新闻聚合平台内容查重</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">长度扩展</font>**<font style="color:rgb(51, 51, 51);">：采用Longformer的稀疏注意力机制支持长文本。</font>
+ **<font style="color:rgb(51, 51, 51);">领域适配</font>**<font style="color:rgb(51, 51, 51);">：添加Adapter模块实现低资源领域微调。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态扩展</font>**<font style="color:rgb(51, 51, 51);">：联合训练文本-图像嵌入（如CLIP模式）。</font>
+ **<font style="color:rgb(51, 51, 51);">量化部署</font>**<font style="color:rgb(51, 51, 51);">：使用TensorRT进行FP16/INT8量化压缩。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import AutoTokenizer, AutoModel

# 加载模型与分词器
model_name = "moka-ai/m3e-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# 文本编码示例
texts = ["M3E模型介绍", "深度学习算法研究"]
inputs = tokenizer(
    texts, 
    padding=True, 
    truncation=True, 
    max_length=256, 
    return_tensors="pt"
)

# 计算嵌入
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # 均值池化

print(embeddings.shape)  # torch.Size([2, 768])

# 相似度计算（余弦相似度）
sim = torch.nn.functional.cosine_similarity(
    embeddings[0], embeddings[1], dim=0
)
print(f"Similarity: {sim.item():.4f}")

```



## BGE
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：BGE (BAAI General Embedding) 是北京智源研究院（BAAI）推出的通用文本嵌入模型，旨在通过高效表示文本语义支持检索、聚类等下游任务。其背景包括：</font>

1. **<font style="color:rgb(51, 51, 51);">需求驱动</font>**<font style="color:rgb(51, 51, 51);">：传统模型（如BERT）在生成句向量时存在各向异性问题，且未针对检索任务优化。</font>
2. **<font style="color:rgb(51, 51, 51);">技术演进</font>**<font style="color:rgb(51, 51, 51);">：对比学习（Contrastive Learning）和预训练优化方法（如RetroMAE）的兴起。</font>
3. **<font style="color:rgb(51, 51, 51);">多场景适配</font>**<font style="color:rgb(51, 51, 51);">：支持多语言、多粒度文本（如短句、长文档），适配RAG（检索增强生成）等新兴应用。</font>

**github**:[https://github.com/FlagOpen/FlagEmbedding/blob/master/README_zh.md](https://github.com/FlagOpen/FlagEmbedding/blob/master/README_zh.md)

**paper**:[https://arxiv.org/pdf/2309.07597](https://arxiv.org/pdf/2309.07597)

:::

<font style="color:rgb(51, 51, 51);">BGE通过预训练-对比学习-指令微调的三阶段训练，在通用语义表示任务中表现出色。其开源特性与灵活接口使其成为替代商业嵌入API的高性价比选择，未来可通过长文本优化和多语言平衡进一步提升竞争力。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">RetroMAE预训练</font>**<font style="color:rgb(51, 51, 51);">：基于掩码自编码器的重构预训练，增强模型对文本深层语义的理解。</font>
2. **<font style="color:rgb(51, 51, 51);">对比学习优化</font>**<font style="color:rgb(51, 51, 51);">：采用难负例采样（Hard Negative Mining）提升嵌入区分度。</font>
3. **<font style="color:rgb(51, 51, 51);">指令微调</font>**<font style="color:rgb(51, 51, 51);">：通过指令模板（如</font>`<font style="color:rgb(51, 51, 51);">"为这个句子生成表示以用于检索相关文章："</font>`<font style="color:rgb(51, 51, 51);">）增强模型对任务意图的理解。</font>
4. **<font style="color:rgb(51, 51, 51);">动态温度系数</font>**<font style="color:rgb(51, 51, 51);">：在对比损失中动态调整温度参数，缓解过拟合。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">预训练数据</font>**<font style="color:rgb(51, 51, 51);">：混合公开语料（如Wikipedia、BookCorpus）及私有数据，总量超TB级，中英文为主。</font>
2. **<font style="color:rgb(51, 51, 51);">微调数据</font>**<font style="color:rgb(51, 51, 51);">：构造三元组（Query, Positive, Negative），覆盖语义相似、问答对、检索日志等场景。</font>
3. **<font style="color:rgb(51, 51, 51);">多语言支持</font>**<font style="color:rgb(51, 51, 51);">：BGE-M3等版本扩展至100+语言，数据涵盖平行语料和对译资源。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">基础架构</font>**<font style="color:rgb(51, 51, 51);">：基于Transformer Encoder，分Base（12层）、Large（24层）等规模。</font>
2. **<font style="color:rgb(51, 51, 51);">池化方式</font>**<font style="color:rgb(51, 51, 51);">：采用[CLS]向量或均值池化（Mean Pooling）生成句向量。</font>
3. **<font style="color:rgb(51, 51, 51);">维度配置</font>**<font style="color:rgb(51, 51, 51);">：常见输出维度768（Base）或1024（Large），支持FP16量化降低部署成本。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">预训练阶段</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用RetroMAE重构目标：随机掩码输入文本，通过编码器-浅层解码器重构原文。</font>
    - <font style="color:rgb(51, 51, 51);">目标函数：交叉熵损失最大化被掩码token的似然概率。</font>
2. **<font style="color:rgb(51, 51, 51);">对比学习微调</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">构建（Anchor, Positive, Negatives）三元组，计算InfoNCE损失。</font>
    - <font style="color:rgb(51, 51, 51);">难负例采样：从批次内或异步缓存中选取困难样本。</font>
3. **<font style="color:rgb(51, 51, 51);">指令微调</font>**<font style="color:rgb(51, 51, 51);">：在检索任务数据上加入指令前缀，通过监督学习微调模型。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">高检索精度：在MTEB、C-MTEB等榜单中超越OpenAI text-embedding-ada。</font>
+ <font style="color:rgb(51, 51, 51);">低延迟：支持批量推理和ONNX加速，适合实时检索场景。</font>
+ <font style="color:rgb(51, 51, 51);">多场景适配：通过指令模板灵活适配分类、聚类、检索等任务。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">长文本处理：对超长文档（如>512 token）的嵌入质量可能下降。</font>
+ <font style="color:rgb(51, 51, 51);">多语言不平衡：低资源语言表现弱于主流语言（如中/英）。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">检索增强生成（RAG）</font>**<font style="color:rgb(51, 51, 51);">：为LLM提供外部知识检索。</font>
2. **<font style="color:rgb(51, 51, 51);">语义搜索</font>**<font style="color:rgb(51, 51, 51);">：电商/内容平台的相似商品/文章推荐。</font>
3. **<font style="color:rgb(51, 51, 51);">去重聚类</font>**<font style="color:rgb(51, 51, 51);">：海量文本数据的冗余检测与分组。</font>
4. **<font style="color:rgb(51, 51, 51);">跨模态对齐</font>**<font style="color:rgb(51, 51, 51);">：与视觉模型结合，实现图文联合检索。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合检索</font>**<font style="color:rgb(51, 51, 51);">：结合稀疏检索（如BM25）与稠密检索提升召回率。</font>
2. **<font style="color:rgb(51, 51, 51);">领域适配</font>**<font style="color:rgb(51, 51, 51);">：继续在垂直领域数据（如医学、法律）上微调。</font>
3. **<font style="color:rgb(51, 51, 51);">长文本优化</font>**<font style="color:rgb(51, 51, 51);">：引入层次化编码或滑动窗口机制。</font>
4. **<font style="color:rgb(51, 51, 51);">蒸馏压缩</font>**<font style="color:rgb(51, 51, 51);">：通过知识蒸馏得到轻量级模型（如BGE-M3-small）。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
from transformers import AutoModel, AutoTokenizer

# 加载模型与分词器
model_name = "BAAI/bge-large-zh-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).cuda()

# 编码文本
texts = ["样例文本1", "样例文本2"]
encoded_input = tokenizer(
    texts, 
    padding=True, 
    truncation=True, 
    max_length=512, 
    return_tensors='pt'
).to('cuda')

# 生成嵌入
with torch.no_grad():
    outputs = model(**encoded_input)
    embeddings = outputs.last_hidden_state[:, 0]  # 取[CLS]向量

# 归一化（可选）
embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

print(embeddings.shape)  # torch.Size([2, 1024])

```



## GTE
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">阿里巴巴团队提出了一种基于多阶段对比学习的通用句向量模型。通过显著增加预训练跟finetune阶段的训练数据，最终获得一个明显超越当时sota模型E5的句向量模型。注意重点，</font>**<font style="color:#ED740C;">GTE主要特色是显著增加训练数据，大力出奇迹～</font>**

:::

<font style="color:rgb(51, 51, 51);">GTE通过融合对比学习与多任务训练，生成通用文本嵌入，平衡了效果与泛化性。未来方向包括优化长文本处理、降低计算成本及扩展多语言支持。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741167797312-0ec17430-9381-4d84-bf4f-3eed5c610c0f.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多任务对比学习</font>**<font style="color:rgb(51, 51, 51);">: 结合无监督对比学习（如SimCSE）与有监督任务（如NLI），增强模型的语义判别能力。</font>
+ **<font style="color:rgb(51, 51, 51);">动态温度系数</font>**<font style="color:rgb(51, 51, 51);">: 在对比损失中动态调整温度参数，优化困难样本的学习。</font>
+ **<font style="color:rgb(51, 51, 51);">混合负采样</font>**<font style="color:rgb(51, 51, 51);">: 同时使用同批次样本和外部语料的难负例，提升模型区分度。</font>
+ **<font style="color:rgb(51, 51, 51);">层级池化策略</font>**<font style="color:rgb(51, 51, 51);">: 融合不同Transformer层的特征，增强嵌入的鲁棒性。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">无监督数据</font>**<font style="color:rgb(51, 51, 51);">: 如Wikipedia、Common Crawl网页文本，用于对比学习预训练。</font>
+ **<font style="color:rgb(51, 51, 51);">有监督数据</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - **<font style="color:rgb(51, 51, 51);">自然语言推理（NLI）</font>**<font style="color:rgb(51, 51, 51);">: SNLI、MNLI数据集，学习语义相似度。</font>
    - **<font style="color:rgb(51, 51, 51);">检索任务</font>**<font style="color:rgb(51, 51, 51);">: MS MARCO、HotpotQA，增强检索相关性。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">: 回译（Back Translation）、随机删除/交换词序，提升泛化性。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">基础架构</font>**<font style="color:rgb(51, 51, 51);">: </font><font style="color:rgb(25, 27, 31);">GTE采用了Transformer encoder，有3种不同模式尺寸，分别以</font>[<font style="color:rgb(9, 64, 142);">MiniLM-small</font>](https://zhida.zhihu.com/search?content_id=233123028&content_type=Article&match_order=1&q=MiniLM-small&zhida_source=entity)<font style="color:rgb(25, 27, 31);">, </font>[<font style="color:rgb(9, 64, 142);">BERT-BASE</font>](https://zhida.zhihu.com/search?content_id=233123028&content_type=Article&match_order=1&q=BERT-BASE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">跟</font>[<font style="color:rgb(9, 64, 142);">BERT-LARGE</font>](https://zhida.zhihu.com/search?content_id=233123028&content_type=Article&match_order=1&q=BERT-LARGE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">作为模型初始化。训练时采用双塔模型结构，</font>**<font style="color:#74B602;">将语言模型所生成的所有位置的最后一层隐状态的均值作为句子表征</font>**<font style="color:rgb(25, 27, 31);">，即句向量。</font>
+ **<font style="color:rgb(51, 51, 51);">改进模块</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - **<font style="color:rgb(51, 51, 51);">动态池化层</font>**<font style="color:rgb(51, 51, 51);">: 加权平均所有token的表示，权重由注意力机制生成。</font>
    - **<font style="color:rgb(51, 51, 51);">归一化层</font>**<font style="color:rgb(51, 51, 51);">: 对输出嵌入进行L2归一化，便于余弦相似度计算。</font>

```python
import torch
from transformers import BertModel

class GTEModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = BertModel.from_pretrained("bert-base-uncased")
        self.pooler = torch.nn.Linear(768, 768)  # 动态池化层

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids, attention_mask)
        last_hidden = outputs.last_hidden_state
        pooled = self.pooler(last_hidden[:, 0])  # CLS token
        return torch.nn.functional.normalize(pooled, p=2, dim=-1)
```

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练阶段**:
    - **<font style="color:rgb(25, 27, 31);">预训练数据</font>**<font style="color:rgb(25, 27, 31);">：在预训练阶段，为了保证句向量模型的覆盖面尽可能多样，研究人员收集了各种领域的跟文本相应性相关开源数据，包括</font>**<font style="color:#74B602;">网页搜索，科学文献，社区问答，社交，维基百科，代码仓库等，共有接近8亿的文本对（query，positive document）</font>**<font style="color:rgb(25, 27, 31);">，这些数据无需额外的人工标注就能被用于句向量模型的无监督训练。在具体训练时，由于不同源头的数据量显著不同，需要采用</font>**<font style="color:#74B602;">特定的抽样策略来维持平衡，并且要保证同个batch里的数据都是来源于同个任务</font>**<font style="color:rgb(25, 27, 31);">，防止模型通过学习到不同任务特性来判断这些数据，从而走上一条不归路。在这一个阶段由于缺乏hard negative信息，为例保证模型效果，需要使用较大的batch size。</font>
    - **<font style="color:rgb(51, 51, 51);">无监督对比学习</font>**<font style="color:rgb(51, 51, 51);">: 对同一句子两次前向传播（不同Dropout掩码）生成正例，同批次其他句子作为负例，使用InfoNCE损失。</font><font style="color:rgb(25, 27, 31);">通过对比学习让模型产生高质量的句子表征，每个训练样本（q,d+,d-）都包括三部分，第一部分是query，第二部分是跟query正相关的d+，第三部分是跟query不相关的d-</font>

```python
temperature = 0.05  # 动态温度可设为可学习参数
embeddings = model(input_ids, attention_mask)
similarity = embeddings @ embeddings.T / temperature
labels = torch.arange(len(embeddings)).to(device)
loss = torch.nn.CrossEntropyLoss()(similarity, labels)
```

2. **有监督微调**:
    - **微调数据**：<font style="color:rgb(25, 27, 31);">在finetune阶段，研究人员以少量的人工标注的数据集（query，positive document）为基础，利用额外的检索器获得相应的hard negative数据，</font>**<font style="color:#74B602;">从而构造出相应的文本相关性三元组（query, positive document, negative document）数据，约300万条</font>**<font style="color:rgb(25, 27, 31);">，从而让模型在这个高质量数据上做进一步微调。在finetune阶段，由于数据集原本的强监督信息跟hard negative，batch size就没有必要设置的特别大。</font>
    - **<font style="color:rgb(51, 51, 51);">NLI任务</font>**<font style="color:rgb(51, 51, 51);">: 三分类（蕴含、中立、矛盾），交叉熵损失。</font>
    - **<font style="color:rgb(51, 51, 51);">检索任务</font>**<font style="color:rgb(51, 51, 51);">: 三元组损失（Anchor, Positive, Negative），最大化正样本相似度。</font>
3. **多任务联合训练**: 加权求和对比损失与监督损失，平衡不同任务贡献。

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">通用性强，跨任务无需微调。</font>
    - <font style="color:rgb(51, 51, 51);">对比学习提升语义区分度。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">训练计算成本高。</font>
    - <font style="color:rgb(51, 51, 51);">长文本处理效率较低。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">语义搜索</font>**<font style="color:rgb(51, 51, 51);">: 计算查询与文档的相关性。</font>
+ **<font style="color:rgb(51, 51, 51);">文本去重</font>**<font style="color:rgb(51, 51, 51);">: 聚类相似文本（如新闻聚合）。</font>
+ **<font style="color:rgb(51, 51, 51);">问答系统</font>**<font style="color:rgb(51, 51, 51);">: 匹配问题与候选答案。</font>
+ **<font style="color:rgb(51, 51, 51);">推荐系统</font>**<font style="color:rgb(51, 51, 51);">: 用户兴趣与内容嵌入匹配。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">模型轻量化</font>**<font style="color:rgb(51, 51, 51);">: 使用知识蒸馏压缩模型（如TinyBERT）。</font>
+ **<font style="color:rgb(51, 51, 51);">长文本优化</font>**<font style="color:rgb(51, 51, 51);">: 引入稀疏注意力或层次化Transformer。</font>
+ **<font style="color:rgb(51, 51, 51);">多语言支持</font>**<font style="color:rgb(51, 51, 51);">: 联合训练多语言语料，共享词嵌入。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch.utils.data import DataLoader
from transformers import AdamW

# 数据加载
class TextDataset(torch.utils.data.Dataset):
    def __init__(self, texts):
        self.texts = texts  # 假设已预处理为token ids

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return {
            "input_ids": self.texts[idx]["input_ids"],
            "attention_mask": self.texts[idx]["attention_mask"]
        }

# 训练循环
def train(model, dataloader, epochs=3):
    optimizer = AdamW(model.parameters(), lr=2e-5)
    model.train()
    for epoch in range(epochs):
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            
            embeddings = model(input_ids, attention_mask)
            similarity = embeddings @ embeddings.T / 0.05
            labels = torch.arange(len(embeddings)).to(device)
            
            loss = torch.nn.CrossEntropyLoss()(similarity, labels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

# 初始化
device = "cuda" if torch.cuda.is_available() else "cpu"
model = GTEModel().to(device)
dataloader = DataLoader(TextDataset(texts), batch_size=32, shuffle=True)
train(model, dataloader)

```



# 大模型embedding系列
## <font style="color:rgb(53, 53, 53);">GTE-Qwen2</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(77, 77, 77);">简介</font>**<font style="color:rgb(77, 77, 77);">：gte-Qwen2-7B-instruct 是一个拥有70亿参数的指令优化型嵌入模型。</font>
+ **<font style="color:rgb(77, 77, 77);">特点</font>**<font style="color:rgb(77, 77, 77);">：该模型特别针对复杂的指令驱动任务进行优化，具有卓越的语义推理和指令执行能力。</font>
+ **<font style="color:rgb(77, 77, 77);">适用场景</font>**<font style="color:rgb(77, 77, 77);">：适合用于复杂的自动问答系统、智能助手和高级对话系统等。</font>

:::

<font style="color:rgb(0, 0, 0);">通义实验室推出了GTE（General Text Embedding）系列文本向量模型，包括基于BERT架构的模型和基于Qwen LLM系列训练的LLM embedding模型，如gte-Qwen2-1.5B-instruct和gte-Qwen2-7B-instruct。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741054728803-fe8cf431-4051-40e0-8037-c1c4c5e63107.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(0, 0, 0);">高性能</font>**<font style="color:rgb(0, 0, 0);">：在多个数据集上与同规模开源模型的对比中，表现领先。</font>
2. **<font style="color:rgb(0, 0, 0);">长文档支持</font>**<font style="color:rgb(0, 0, 0);">：Embedding和Reranker均可处理8k token文本长度，且支持通过ntk-rope等方法扩展到更长的上下文。</font>
3. **<font style="color:rgb(0, 0, 0);">多语言支持</font>**<font style="color:rgb(0, 0, 0);">：模型支持75种语言，涵盖当前主要大模型所支持的所有语种。</font>
4. **<font style="color:rgb(0, 0, 0);">弹性向量表示</font>**<font style="color:rgb(0, 0, 0);">（Elastic Embedding）：模型支持输出128-768维度之间的任意向量表示，以便在性能和存储成本之间取得最佳平衡。在128维的情况下，与768维相比，召回性能损失小于2%，同时节省6倍的存储空间。</font>
5. **<font style="color:rgb(0, 0, 0);">稀疏向量表示</font>**<font style="color:rgb(0, 0, 0);">（Sparse Embedding）：模型可以输出句子中每个单词的词权重作为稀疏表示，适用于需要精确匹配的场景。</font>







