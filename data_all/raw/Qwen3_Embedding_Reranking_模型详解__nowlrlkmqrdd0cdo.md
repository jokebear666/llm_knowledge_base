# Qwen3 Embedding/Reranking 模型详解

<!-- source: yuque://zhongxian-iiot9/hlyypb/nowlrlkmqrdd0cdo -->

:::success
**背景：**Qwen 团队在 Qwen3 大模型家族之上推出了 0.6B / 4B / 8B 三档 **Embedding + Reranker** 套件，依托 1.5 亿条多语种合成数据 + 多阶段训练 + [SLERP](https://zhida.zhihu.com/search?content_id=259112424&content_type=Article&match_order=1&q=SLERP&zhida_source=entity) 模型合并，全面刷新 MTEB 等主流检索与排序榜单，并以 [Apache-2.0](https://zhida.zhihu.com/search?content_id=259112424&content_type=Article&match_order=1&q=Apache-2.0&zhida_source=entity) 开源。

+ 随着 Retrieval-Augmented Generation（RAG）和智能 Agent 崛起，**高质量文本向量**与**重排模型**成为信息检索链路的“第二心脏”。
+ 传统方法多依赖 [BERT](https://zhida.zhihu.com/search?content_id=259112424&content_type=Article&match_order=1&q=BERT&zhida_source=entity) 类编码器；大模型时代带来了 **更强的跨语言语义对齐与推理能力**，但也提出了在效率、尺度与任务适配之间平衡的新挑战。

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Qwen3-Embedding 是阿里云发布的新一代开源向量模型，用于文本嵌入和相似度计算。本文根据技术报告和阿里团队视频分享进行整合归纳，详细解读 </font>[<font style="color:rgb(9, 64, 142);">Qwen3 Embedding</font>](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=Qwen3+Embedding&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 </font>[<font style="color:rgb(9, 64, 142);">Reranking 模型</font>](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=Reranking+%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的技术要点。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

**<font style="color:rgb(25, 27, 31);">blog：</font>**[https://qwenlm.github.io/zh/blog/qwen3-embedding](https://link.zhihu.com/?target=https%3A//qwenlm.github.io/zh/blog/qwen3-embedding)

**paper：**[https://arxiv.org/pdf/2506.05176](https://arxiv.org/pdf/2506.05176)

**<font style="color:rgb(25, 27, 31);">Hugging Face：</font>**[hugging face](https://link.zhihu.com/?target=https%3A//huggingface.co/collections/Qwen/qwen3-embedding-6841b2055b99c44d9a4c371f)

**<font style="color:rgb(25, 27, 31);">GitHub ：</font>**[https://github.com/QwenLM/Qwen3-Embedding](https://link.zhihu.com/?target=https%3A//github.com/QwenLM/Qwen3-Embedding)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760409452731-8f129044-5a8f-4044-97c4-184ef82496da.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760409466478-1369ac6b-c3dd-452f-93b0-fab72a9619c9.png)

## <font style="color:rgb(25, 27, 31);">模型架构</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Qwen3-Embedding 和 Qwen3-Reranker 是基于 Qwen3 这种</font>**<font style="color:#ED740C;"> decoder-only</font>**<font style="color:rgb(25, 27, 31);"> 的模型架构，用生成的方式来获取句向量和相似性分数。而这种大模型经过 </font>[<font style="color:rgb(9, 64, 142);">SFT 之后</font>](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=SFT+%E4%B9%8B%E5%90%8E&zhida_source=entity)<font style="color:rgb(25, 27, 31);">是可以听懂指令的，所以 Qwen3-Embedding 也采用任务感知的方式，训练时不止输入需要嵌入的文本，还会输入任务描述（例如是评估相关性还是相似性），让模型根据任务描述来生成句向量，即一个输入任务指令，一个输入query，一个正样本，多个负样本。</font>

:::

:::color5
**<font style="color:#601BDE;">1.架构</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen3-Embedding 和 Qwen3-Reranker 是基于 Qwen3 model 的 dense 版本训练的，有 3 个版本大小，分别是 0.6B、4B 和 8B，各版本详细参数如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410054629-e4e0cadc-0b16-48a2-a8d5-9ac9e7c60122.png)

> Qwen3嵌入模型的模型架构。“MRL support”表示是否嵌入模型支持最终embedding的自定义尺寸。“Instruct aware”表示embedding或重排序模型是否支持根据以下内容定制输入指令不同的任务。
>

:::color5
**<font style="color:#601BDE;">2.Embedding 模型</font>**

:::

<font style="color:rgb(25, 27, 31);">由于用的 Qwen3 这种因果模型，所以直接利用它自有的注意力机制。直接在输入序列的末尾附加一个 [EOS] token，最终的嵌入向量就是这个 [EOS] token 的最后一层的隐层向量。同时为了保持之前说的任务感知，输入拼接上任务指令描述，格式如下：</font>

<font style="color:rgb(83, 88, 97);">{Instruction} {Query} {EOS}</font>

<font style="color:rgb(25, 27, 31);">如下图中所示，当输入</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">query</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">时可以在前面添加</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">instruction</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">来指定任务，但输入</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">doc</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">时不需要添加。</font>**<font style="color:rgb(25, 27, 31);">但注意，即使在中文场景，instruction 也建议使用英文的，因为训练时使用的都是英文的</font>**<font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760409452731-8f129044-5a8f-4044-97c4-184ef82496da.png)

> Qwen3嵌入（左）和Qwen3-Reranker（右）的模型架构。
>

:::color5
**<font style="color:#601BDE;">3.Reranking 模型</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">使用 point-wise 的训练方式（单次输入一个源序列和一个目标序列，计算两个的相似性，然后多次计算累加损失。pair-wise 是输入一个源序列和一个正样本序列、一个负样本序列，同时学习到相对关系），为了保持任务感知，也是输入拼接任务指令描述，模板如下：</font>

```plain
<|im_start|>system
Judge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".
<|im_end|>
<|im_start|>user
<Instruct>: {Instruction}
<Query>: {Query}
<Document>: {Document}<|im_end|>
<|im_start|>assistant
<think>\n\n</think>\n\n
```

<font style="color:rgb(25, 27, 31);">这就是</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tokenizer.apply_chat_template</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的模板，其中</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">{Instruction}</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是任务描述，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">{Query}</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是 query，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">{Document}</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是候选文档。</font>[官方代码](https://link.zhihu.com/?target=https%3A//github.com/QwenLM/Qwen3-Embedding/blob/main/examples/qwen3_reranker_transformers.py%23L44)<font style="color:rgb(25, 27, 31);">中是用手动拼接的方式，但我认为用模板的方式更方便。</font>

```python
sys_msg = 'Judge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".
inputs = f"""<Instruct>: {Instruction}
<Query>: {Query}
<Document>: {Document}"""

messages = [
    {"role": "system", "content": sys_msg},
    {"role": "user", "content": inputs},
]

prompt = tokenizer.apply_chat_template(messages, tokenize=False, enable_thinking=False, add_generation_prompt=True)
```

<font style="color:rgb(25, 27, 31);">输入给大模型后，只输出一个 token，取这个 token 列表中</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">yes</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">no</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的原始分数（不成概率分布），然后将这两个分数放到一起计算 softmax，然后取</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">yes</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的分数作为两者的相似性分数。论文中公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410215137-025804af-c0b5-46f3-b947-459918d2a4a9.png)

<font style="color:rgb(25, 27, 31);">但实际代码如下，先用了</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">log_softmax</font>`<font style="color:rgb(25, 27, 31);">是为了数值稳定性(先 softmax 再取 log 可以避免数值下溢)，再用</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">exp</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">转回概率分布：</font>

```python
def compute_logits(self, inputs, **kwargs):
    batch_scores = self.lm(**inputs).logits[:, -1, :]
    true_vector = batch_scores[:, self.token_true_id]
    false_vector = batch_scores[:, self.token_false_id]
    batch_scores = torch.stack([false_vector, true_vector], dim=1)
    # 先 log_softmax 是为了数值稳定性
    batch_scores = torch.nn.functional.log_softmax(batch_scores, dim=1)
    # 再 exp 转为概率分布
    scores = batch_scores[:, 1].exp().tolist()
    # 取 yes 的分数
    return scores
```

## <font style="color:rgb(25, 27, 31);">模型训练</font>
### <font style="color:rgb(25, 27, 31);">损失函数</font>
:::color5
**<font style="color:#601BDE;">1.Embedding 模型</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">采用 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">InfoNCE</font>`<font style="color:rgb(25, 27, 31);"> 损失，大小为 N 的一个 batch 中，损失为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410421344-5109d5ac-ded5-4be8-8495-6f2288cac0e9.png)

<font style="color:rgb(25, 27, 31);">这里</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">代表相似性函数（这里使用余弦相似度），</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是温度参数，</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是归一化因子，聚合 batch 内正样本对和负样本对的相似性得分，计算方式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410429353-8ff7c918-00a4-454e-bb83-e26f91b7226d.png)

<font style="color:rgb(25, 27, 31);">注意i,j代表 batch 内第 i 和第 j 条数据。这几项分别是：</font>

1. <font style="color:rgb(25, 27, 31);">当前 query 和正样本的相似性得分</font>
2. <font style="color:rgb(25, 27, 31);">当前 query 和 K 个难负样本（与当前 query 高度相似但实际不相关）的相似性得分</font>
3. <font style="color:rgb(25, 27, 31);">当前 query 和 batch 内所有其他 query 的相似性得分，区分 query 和 query 的相似性</font>
4. <font style="color:rgb(25, 27, 31);">当前 正样本 和 batch 内所有其他样本（包括正负样本）的相似性得分，拉大相关正样本与其他不相关样本的差距</font>
5. <font style="color:rgb(25, 27, 31);">当前 query 和 batch 内所有其他样本（包括正负样本）的相似性得分，扩大负样本范围，确保可以在海量数据中准确筛选到正样本</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1760410348313-eab8c2de-c3d2-4fc9-85ad-cca72665687f.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);">之前的做法只是将 in-batch 内的其他文档作为负例，但这里还扩充了其他的 query。为了保障扩充负例之后的数据质量，还引入了掩码因子</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，旨在减轻假负例（即某些负例实际与 query 语义高度相关，但因标注或采样误差被误判为负例）的影响，定义为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410461600-9664da00-6146-4f60-875f-3d80f58bba3e.png)

<font style="color:rgb(25, 27, 31);">这里 s</font><sub><font style="color:rgb(25, 27, 31);">ij</font></sub><font style="color:rgb(25, 27, 31);"> 代表 s(q</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><font style="color:rgb(25, 27, 31);">,d</font><sub><font style="color:rgb(25, 27, 31);">j</font></sub><font style="color:rgb(25, 27, 31);">) 或 s(q</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><font style="color:rgb(25, 27, 31);">,q</font><sub><font style="color:rgb(25, 27, 31);">j</font></sub><font style="color:rgb(25, 27, 31);">) ，相当于在以下两个条件时不将其纳入归一化：1) 负例和 query 的相关性显著高于正例（分差超过0.1，实际是相关的，但被误判为负例，此时忽略该负例，防止模型学到错误的语义关联）; 2) batch 内其他数据的负例等于该数据的正例时（无效负例，直接屏蔽）;</font>

<font style="color:rgb(25, 27, 31);">模型训练时采用了动态 batch size 和 </font>[<font style="color:rgb(9, 64, 142);">MRL Loss</font>](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=MRL+Loss&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> (openai 带火的俄罗斯套娃 Loss)，在下游任务微调的时候可以借鉴这个不同长度 batch 的大小。而 MRL Loss 可以增强模型的表示能力，并且在推理时可以直接取前任意维度的向量，降低推理存储成本（此样式图均取自直播分享PPT，后续不再赘述）。</font>

:::color5
**<font style="color:#601BDE;">2.Reranker 模型</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">使用优化后的 SFT 损失：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410502630-f34b2d16-7247-4d0a-9365-82ec70abf9b4.png)

<font style="color:rgb(25, 27, 31);">这里的 P(q,d) 代表输入拼接好的 query 和 document，注意这个 P 不是概率。虽然前文没有提到过，但在机器学习中，P 通常代表</font>**<font style="color:rgb(25, 27, 31);">数据处理过程或集合</font>**<font style="color:rgb(25, 27, 31);">。 p(l|P(q,d)) 代表输入文本后模型预测 token 为 l 的概率，这个 l 是 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">yes</font>`<font style="color:rgb(25, 27, 31);"> 或 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">no</font>`<font style="color:rgb(25, 27, 31);">，document 为正例时， l 为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">yes</font>`<font style="color:rgb(25, 27, 31);">，否则为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">no</font>`<font style="color:rgb(25, 27, 31);">。其余的  就是标准的 SFT 交叉熵损失，旨在给正例分配更高的概率。</font>

<font style="color:rgb(25, 27, 31);">直接分享上给出了训练参数，两个模型都是使用</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Lora 训练</font>](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=Lora+%E8%AE%AD%E7%BB%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的(直播分享说他们实验 Lora 比全参好，那咱们下游任务训练就更可以使用 Lora 了)，Embedding 模型每个 query 的难负例取 8 个(随机负例用 in-batch 的)，Reranking 模型每个 query 的难负例取 8 个，随机负例取 8 个共 16 个。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1760410739229-27ae25f3-5930-4318-8a97-8b12bd53e332.tif?x-oss-process=image/format,png)

### <font style="color:rgb(25, 27, 31);">多阶段训练</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">多阶段训练是 Embedding 模型的常用方法，BGE 等模型也采用类似方案，通常是先在大规模半监督数据上训练，然后使用小规模高质量监督数据集微调。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">相对于以往的工作，主要创新如下：</font>

1. **<font style="color:rgb(25, 27, 31);">大模型弱监督训练采用</font>**[**<font style="color:rgb(9, 64, 142);">合成数据</font>**](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=%E5%90%88%E6%88%90%E6%95%B0%E6%8D%AE&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">之前的方法都是从开源社区获取，但本文提出利用 Qwen3 模型的生成能力来合成数据。由于现在的大模型能力很强，能够高质量的模仿真实世界的数据。且用大模型来合成数据能够对数据维度进行更高的控制，例如任务、语言、长度和难度，并在资源匮乏的场景和语言获取更多的数据。</font>
2. **<font style="color:rgb(25, 27, 31);">合成数据增强第二阶段监督微调训练：</font>**<font style="color:rgb(25, 27, 31);">由于 Qwen3 合成的数据质量非常高，所以在第二阶段有选择地纳入这些数据，进一步提升整体性能和泛化能力。</font>
3. **<font style="color:rgb(25, 27, 31);">模型融合：</font>**<font style="color:rgb(25, 27, 31);">机器学习竞赛常用的方法，在不同任务训练得到的 checkpoint 上进行模型融合（这里使用球面线性插值），在可能的插值区间用一些样本得到 loss 最低的点，提升最终效果（可能近期在大模型上有新的提高技巧？）。</font>

<font style="color:rgb(25, 27, 31);">注：第一阶段训练只用于 Embedding 模型，Reranking 模型不需要。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760409466478-1369ac6b-c3dd-452f-93b0-fab72a9619c9.png)

<font style="color:rgb(145, 150, 161);">模型训练 pipeline</font>

### <font style="color:rgb(25, 27, 31);">合成数据集</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">借鉴前人训练 Embedding 模型的经验与数据积累，数据分为三部分：</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

1. <font style="color:rgb(25, 27, 31);">开源社区人工标注的高质量数据集，约有 10M 对样本，经筛选后保留 7M 放入第二阶段高质量 SFT 训练数据中；</font>
2. <font style="color:rgb(25, 27, 31);">公开的弱监督数据，数据量很大但质量残次不齐，各领域数据分布不均衡，需要大量的清洗工作，所以没有采用这部分数据。</font>
3. <font style="color:rgb(25, 27, 31);">合成数据，利用 Qwen3 模型生成，理论上可以得到无限的数据。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1760410998388-5c4f8875-d041-469a-85a1-a488937d1d96.tif?x-oss-process=image/format,png)

<font style="color:rgb(145, 150, 161);">数据来源</font>

<font style="color:rgb(25, 27, 31);">为了提高合成数据的质量，让模型能够适应不同任务，合成数据时按照不同类别指定了一些标准：（为什么用这几个类别，因为</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">MTEB 排行榜</font>](https://zhida.zhihu.com/search?content_id=259417142&content_type=Article&match_order=1&q=MTEB+%E6%8E%92%E8%A1%8C%E6%A6%9C&zhida_source=entity)<font style="color:rgb(25, 27, 31);">用了以下几种任务）</font>

1. <font style="color:rgb(25, 27, 31);">检索：常规检索，匹配 query 和 document；</font>
2. <font style="color:rgb(25, 27, 31);">双文本挖掘：匹配语言不同但语义相似的文本对；</font>
3. <font style="color:rgb(25, 27, 31);">分类：将文本划分到预定义类别中，学习类别间的语义边界，区分语义相似但类别不同的文本。例如按照情绪类别分类，匹配积极情绪的 query，正负样本都是语义相似的，但正样本应该是积极情绪的，负样本是消极情绪的；（不知道怎么做分类的）</font>
4. <font style="color:rgb(25, 27, 31);">语义文本相似性：区分语义相关和语义相似的样本对。例如“狗在睡觉”和“我今天去打篮球”为不相关，“狗在睡觉”和“狗在吃饭”为相关但不相似。</font>

:::color5
**<font style="color:#601BDE;">1.数据合成流程</font>**

:::

<font style="color:rgb(25, 27, 31);">使用 Qwen3-32B 作为数据合成的基础模型，为了提高合成数据的多样性和真实性，设计了一种多样化的提示策略。例如在文本检索任务中，使用了 Qwen3 的多语言训练语料，并按照如下流程生成：</font>

1. <font style="color:rgb(25, 27, 31);">首先准备一个非常大的语料库，包含各个领域的文本，开源社区有很多。</font>
2. <font style="color:rgb(25, 27, 31);">按领域随机抽取一些文档，用文档去一个角色库中检索，提取出 Top5 的角色，让大模型判断这个文档最适合哪个角色，将其作为这个文档的角色配置，这种用户视角的注入可以增强合成查询的多样性和真实性。</font>
3. <font style="color:rgb(25, 27, 31);">然后再通过两个阶段合成数据：1. 生成配置（包括根据文档选择任务、问题类型、难度等）；2. 根据生成的配置去生成生成</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">query</font>**<font style="color:rgb(25, 27, 31);">；论文中给出了检索任务英文 prompt 的框架，以下为中文翻译：</font>

:::color5
**<font style="color:#601BDE;">2.生成配置</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

```python
给定一篇**文章（Passage）**和一个**人物（Character）**，从三个字段选择合适的选项：人物、问题类型、难度，并以 JSON 格式返回输出。
首先，从候选人物中选择可能对该文章感兴趣的**人物（Character）**。然后选择该人物可能针对文章提出的**问题类型（Question_Type）**；最后，根据文章内容、人物身份和问题类型，选择该问题可能的**难度（Difficulty）**。

人物（Character）：由输入给定的人物

问题类型（Question_Type）：
- keywords：... （论文中就是...，只是给出了大概框架，具体定义没给出）
- acquire_knowledge：...
- summary：...
- yes_or_no：...
- background：...
难度（Difficulty）：
- high_school：...
- university：...
- phd：...

以下是一些示例
<Example1> <Example2> <Example3>

现在，根据用户提供的**文章（Passage）**和**人物（Character）**生成**输出（output）**，**文章（Passage）**将采用 {language} 语言，**人物（Character）**以英文给出。
确保仅生成英文内容的 JSON 输出。

**文章（Passage）**：
{passage}
**人物（Character）**：
{character}
```

:::color5
**<font style="color:#601BDE;">3.根据配置来组装 prompt</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">根据配置来组装 prompt，以指导 query 的生成，在这里还明确指定了生成的 query 所需的长度、难度和语言等。</font>

```plain
给定一个**人物（Character）**、**段落（Passage）** 和**要求（Requirement）**，从该人物的视角生成一个满足该要求且可用于检索该段落的查询（query）。请以JSON格式返回结果。  

以下是一个示例：
<example> 

现在，根据用户提供的**人物（Character）**、**段落（Passage）** 和**要求（Requirement）** 生成**输出（output）**，其中**段落（Passage）** 为{corpus_language}语言，**人物（Character）** 和**要求（Requirement）** 为英文。 
￫ 确保仅生成 JSON 输出，其中键（key）为英文，值（value）采用{queries_language}语言。

**人物（Character）**
{character}
**段落（Passage）**
{passage}

**要求（Requirment）**
- 类型（Type）：{type}；(关键词keyword, 事实性factual, 摘要summary, 判断judgment等)
- 难度（Difficulty）：{difficulty}；
- 长度（Length）：生成句子的长度应为{length}个单词；
- 语言（Languange）：生成结果的语言应为{language}语言；
```

<font style="color:rgb(25, 27, 31);">最终得到的各阶段数据统计如下，共有约 1.5 亿对弱监督训练数据。此时，还会通过 Embedding 模型进行过滤，使用生成的 query 去检索文档，如果 Top100 都没有检索到这个文档则代表生成的 query 有问题，需要将其去掉。</font>

<font style="color:rgb(25, 27, 31);">然后再经随机配对和余弦相似度、reranking相似度筛选（阈值0.7，视频分享说去掉相似度过高的和过低的，过高代表过于简单，过低代表质量有问题），这里的 Reranking 模型是先初步过滤，得到第一版高质量数据之后训练 Reranking 模型，然后使用训练好的 Reranking 模型再重新过滤，反复迭代。</font>

<font style="color:rgb(25, 27, 31);">最终得到约1200万对高质量合成数据用于第二阶段监督微调。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410815540-a634dc1b-d425-4d37-bfea-0555fe226517.png)

<font style="color:rgb(145, 150, 161);">各阶段数据统计</font>

<font style="color:rgb(25, 27, 31);">为了保障覆盖面的多样性，合成数据具有 多语言、跨语言、多领域、多任务、长/短文本、代码检索等特点。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1760410864973-5b0dfa0a-7e1f-4766-9116-27d2c11bb1eb.tif?x-oss-process=image/format,png)

## <font style="color:rgb(25, 27, 31);">评估</font>
### <font style="color:rgb(25, 27, 31);">效果评估</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在</font><font style="color:rgb(25, 27, 31);"> </font>[MMTEB](https://link.zhihu.com/?target=https%3A//huggingface.co/spaces/mteb/leaderboard)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">上评估 Embedding 模型，这是目前文本嵌入模型最常用的评估基准之一。（此处占位，后续出一个 MTEB 的详细介绍）</font>

**<font style="color:rgb(25, 27, 31);">模型对比</font>**<font style="color:rgb(25, 27, 31);">：与目前最强的几个开源模型和闭源商业 API 进行比较。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Embedding</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">下表为 Embedding 模型在 MMTEB 和 MTEB (English,v2) 的评估结果，确实非常强，分数相当高，排行榜头牌了。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410890608-333c7310-dc21-406e-8e77-d82c33939344.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410900939-73d21d1e-4ddf-45d7-a511-b9c67b04a0fa.png)

:::color5
**<font style="color:#601BDE;">2.Reranking</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:rgb(25, 27, 31);">Reranking</font>**<font style="color:rgb(25, 27, 31);">：先利用 Qwen3-Embedding-0.6B 模型检索前 100 个候选文档，然后用不同的模型进一步精排，下表展示了 Reranking 模型的评估结果，使用了 MTEB(eng, v2), MTEB(cmn, v1)和 MMTEB 的检索子集，以及另外都是检索任务的数据集。所有结果都是基于第一行粗检索的基础上进行的。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410918158-ffef1335-ed9e-472f-a45c-fdd11115d6d8.png)

### <font style="color:rgb(25, 27, 31);">消融实验</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">如下图所示，最后一行为最终的效果，上面三行说明了弱监督、高质量数据监督训练和模型融合的必要性。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ <font style="color:rgb(25, 27, 31);">第一行去掉了第二阶段高质量数据监督训练，效果有所下降；</font>
+ <font style="color:rgb(25, 27, 31);">第二行去掉了第一阶段弱监督训练，效果有所下降；</font>
+ <font style="color:rgb(25, 27, 31);">第三行去掉了模型融合，效果有所下降（去掉模型融合的方法，论文说使用数据采样来平衡各种任务。且视频分享说最终模型在第二步训练过程中，sample 了不同的训练阶段 step 的 checkpoint）；</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760410925188-974dd801-e4ba-426b-83a7-87a3630eefff.png)

## <font style="color:rgb(25, 27, 31);">个人总结</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">随着现在大模型越来越强大，已经能够模拟出真实世界的数据。论文中合成数据的方法尤其值得借鉴，这样得到的数据质量更高（现实互联网的数据可能更脏更不可控），可控性也较强，在我们进行垂直领域微调的时候也可以这样合成数据。可惜合成数据的详细流程和提示词没有公开，不过随着大家的探索，慢慢肯定会有一个通用的方法。</font>

<font style="color:rgb(25, 27, 31);">同理，在一些冷门任务上也都可以基于大模型合成数据，不必拘泥于互联网现有数据。</font>

<font style="color:rgb(25, 27, 31);">实测 Qwen3-Embedding 和 Qwen3-Reranker 确实非常强大，可以直接将原来的 BGE 模型替换掉了。</font>

:::





