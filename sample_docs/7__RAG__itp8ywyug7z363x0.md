# 7️⃣ RAG

<!-- source: yuque://zhongxian-iiot9/hlyypb/itp8ywyug7z363x0 -->

# RAG
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">RAG</font>**<font style="color:rgb(51, 51, 51);">（Retrieval-Augmented Generation）是一种结合检索（Retrieval）和生成（Generation）的混合模型框架，旨在利用外部知识库增强生成模型的能力，解决传统生成模型（如GPT）在生成文本时可能出现的“幻觉”问题（即生成不准确或虚构内容）。</font>

**<font style="color:#ED740C;">RAG通过结合检索与生成，显著提升了生成模型的可信度，已成为工业界知识密集型任务的首选方案。</font>**

:::

**<font style="color:rgb(51, 51, 51);">RAG核心流程：</font>**

1. **<font style="color:rgb(51, 51, 51);">检索阶段</font>**<font style="color:rgb(51, 51, 51);">：根据输入问题从外部知识库中检索相关文档片段。</font>
2. **<font style="color:rgb(51, 51, 51);">生成阶段</font>**<font style="color:rgb(51, 51, 51);">：将检索到的文档片段与原始输入拼接，输入生成模型生成最终回答。</font>

**<font style="color:rgb(51, 51, 51);">挑战</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">检索效率与精度平衡。</font>
+ <font style="color:rgb(51, 51, 51);">处理多模态知识（文本+图像）。</font>

**<font style="color:rgb(51, 51, 51);">前沿方向</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">RAG 2.0</font>**<font style="color:rgb(51, 51, 51);">：引入强化学习优化检索策略。</font>
+ **<font style="color:rgb(51, 51, 51);">Unsupervised RAG</font>**<font style="color:rgb(51, 51, 51);">：无监督构建知识库。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">检索阶段</font>**

+ **<font style="color:rgb(51, 51, 51);">输入编码</font>**<font style="color:rgb(51, 51, 51);">：将输入问题 q编码为向量 q∈R</font><sup><font style="color:rgb(51, 51, 51);">d</font></sup><font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">编码器：通常使用稠密检索模型（如DPR、BERT）或稀疏检索（如BM25）。</font>
+ **<font style="color:rgb(51, 51, 51);">文档索引</font>**<font style="color:rgb(51, 51, 51);">：预先将外部知识库中的文档 D={d1,d2,...,dN}编码为向量 di∈R</font><sup><font style="color:rgb(51, 51, 51);">d</font></sup><font style="color:rgb(51, 51, 51);">，并构建向量索引（如FAISS、Annoy）。</font>
+ **<font style="color:rgb(51, 51, 51);">相似度计算</font>**<font style="color:rgb(51, 51, 51);">：计算 q与所有 di的相似度，选择Top-K相关文档：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740482079160-a485f659-57c9-4b5d-90ec-a3fb9b2b4304.png)

+ **<font style="color:rgb(51, 51, 51);">检索结果</font>**<font style="color:rgb(51, 51, 51);">：返回Top-K文档片段 {dk1,dk2,...,dkK}。</font>

**<font style="color:rgb(51, 51, 51);">2. 生成阶段</font>**

+ **<font style="color:rgb(51, 51, 51);">输入拼接</font>**<font style="color:rgb(51, 51, 51);">：将原始问题 q</font>_<font style="color:rgb(51, 51, 51);">q</font>_<font style="color:rgb(51, 51, 51);"> 与检索到的文档片段拼接为增强输入：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740482174449-10128e8f-d463-4d4d-91df-c343eb2738cb.png)

+ **<font style="color:rgb(51, 51, 51);">生成模型</font>**<font style="color:rgb(51, 51, 51);">：使用预训练生成模型（如T5、GPT-3）生成回答：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740482166192-45c43710-d0cf-400d-9fc1-e7b526650a80.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">减少幻觉</font>**<font style="color:rgb(51, 51, 51);">：依赖外部知识库，生成内容更准确。   </font><font style="color:rgb(51, 51, 51);">2.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">可解释性</font>**<font style="color:rgb(51, 51, 51);">：可通过检索结果追踪生成依据。   </font><font style="color:rgb(51, 51, 51);">3.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">无需微调</font>**<font style="color:rgb(51, 51, 51);">：直接利用现有生成模型。</font> | <font style="color:rgb(51, 51, 51);">1.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">计算开销大</font>**<font style="color:rgb(51, 51, 51);">：检索和生成两阶段耗时较长。   </font><font style="color:rgb(51, 51, 51);">2.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">依赖检索质量</font>**<font style="color:rgb(51, 51, 51);">：若检索到无关文档，生成结果可能错误。   </font><font style="color:rgb(51, 51, 51);">3.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">知识更新延迟</font>**<font style="color:rgb(51, 51, 51);">：外部知识库需定期更新。</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">开放域问答</font>**<font style="color:rgb(51, 51, 51);">：如回答事实性问题（“珠穆朗玛峰高度是多少？”）。</font>
2. **<font style="color:rgb(51, 51, 51);">对话系统</font>**<font style="color:rgb(51, 51, 51);">：提供基于知识库的精准回复（客服、医疗咨询）。</font>
3. **<font style="color:rgb(51, 51, 51);">内容生成</font>**<font style="color:rgb(51, 51, 51);">：生成带有引用来源的文章或报告。</font>
4. **<font style="color:rgb(51, 51, 51);">低资源任务</font>**<font style="color:rgb(51, 51, 51);">：在少量标注数据场景下提升生成效果。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **检索优化**：
    - **<font style="color:rgb(51, 51, 51);">混合检索</font>**<font style="color:rgb(51, 51, 51);">：结合稠密检索（DPR）和稀疏检索（BM25）提升召回率。</font>
    - **<font style="color:rgb(51, 51, 51);">重排序（Reranking）</font>**<font style="color:rgb(51, 51, 51);">：使用交叉编码器（Cross-Encoder）对Top-K文档二次排序。</font>
    - **<font style="color:rgb(51, 51, 51);">动态检索</font>**<font style="color:rgb(51, 51, 51);">：根据生成过程动态调整检索策略（如迭代检索）。</font>
2. **生成优化**：
    - **<font style="color:rgb(51, 51, 51);">注意力机制</font>**<font style="color:rgb(51, 51, 51);">：设计文档-问题交叉注意力（如FiD模型）。</font>
    - **<font style="color:rgb(51, 51, 51);">知识融合</font>**<font style="color:rgb(51, 51, 51);">：通过多任务学习联合训练检索器和生成器（如REALM）。</font>
3. **工程优化**：
    - **<font style="color:rgb(51, 51, 51);">增量索引</font>**<font style="color:rgb(51, 51, 51);">：支持实时知识更新（如Elasticsearch + FAISS）。</font>
    - **<font style="color:rgb(51, 51, 51);">压缩检索</font>**<font style="color:rgb(51, 51, 51);">：使用量化（如PQ）降低向量存储开销。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
import faiss
import numpy as np

# 1. 加载预训练模型和检索器
model_name = "facebook/rag-sequence-nq"
tokenizer = RagTokenizer.from_pretrained(model_name)
retriever = RagRetriever.from_pretrained(model_name, index_name="exact", use_dummy_dataset=True)
model = RagSequenceForGeneration.from_pretrained(model_name, retriever=retriever)

# 2. 自定义知识库（示例）
documents = [
    "Mount Everest is 8,848 meters high.",
    "Paris is the capital of France."
]
# 编码文档并构建FAISS索引
document_embeddings = np.random.randn(len(documents), 128).astype('float32')  # 假设已通过模型编码
index = faiss.IndexFlatIP(128)
index.add(document_embeddings)

# 3. 检索与生成
query = "How tall is Mount Everest?"
inputs = tokenizer(query, return_tensors="pt")
outputs = model.generate(input_ids=inputs["input_ids"], max_length=100)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(answer)  # Output: "Mount Everest is 8,848 meters high."

```



## RAG评估指标**<font style="color:#D22D8D;"></font>**
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：从</font>**<font style="color:#ED740C;">召回、排序、生成、整体</font>**<font style="color:rgb(51, 51, 51);">四个维度来评估RAG性能。</font>

<font style="color:rgb(58, 58, 58);">使用了多种指标，如准确率（Correct）、错误率（Wrong）、失败率（Fail）、BERTScore、ROUGE Score等，以全面评估生成答案的质量。</font>

**参考**：[RAG评估指标](https://zhuanlan.zhihu.com/p/715932861)   [万字长文整理RAG评估指标、基准和框架](https://zhuanlan.zhihu.com/p/717985736)

:::

:::color5
**<font style="color:#601BDE;">1.召回指标</font>**

:::

<font style="color:rgb(25, 27, 31);">总体来说，就是能根据问题尽量找全相关的信息，尽可能高相关，并且越精准相关的越靠前</font>

1. **上下文召回率****<font style="color:rgb(25, 27, 31);">（Context Recall）</font>**

**<font style="color:rgb(25, 27, 31);">指标含义</font>**<font style="color:rgb(25, 27, 31);">：</font>[<font style="color:rgb(9, 64, 142);">检索系统</font>](https://zhida.zhihu.com/search?content_id=247226105&content_type=Article&match_order=1&q=%E6%A3%80%E7%B4%A2%E7%B3%BB%E7%BB%9F&zhida_source=entity)<font style="color:rgb(25, 27, 31);">检索到的相关上下文占所有相关上下文的比例。它关注的是检索系统能否找到所有相关的信息，即检索的全面性。</font>

```python
用户Query：“法国的首都是什么？”假设存在以下三个相关上下文：
"巴黎是法国的首都。"
"法国的首都是巴黎，位于塞纳河畔。"
"法国是一个西欧国家，其首都是巴黎。"

检索系统返回了以下结果：
"结果1：巴黎是法国的首都。"
"结果2：西班牙的首都是马德里（不相关）。"

在这个例子中，检索系统只检索到了一个与Query相关的上下文，而实际上有三个相关的上下文存在。因此，上下文召回率是1/3，即33.33%。
```

2. **上下文相关性****<font style="color:rgb(25, 27, 31);">（Context Relevance）</font>**

**<font style="color:rgb(25, 27, 31);">指标含义：</font>**<font style="color:rgb(25, 27, 31);">衡量检索到的上下文与用户Query的相关程度，关注的是整个检索结果集。</font>

```python
假设我们有以下检索结果列表，针对Query：“法国的首都是什么？”
结果1：巴黎是法国的首都。
结果2：法国是一个位于欧洲的国家。
结果3：西班牙的首都是马德里（不相关）。
所有结果中有两个是相关的，相关性较高，具体计算方式与相关性的标准等有关（BertScore等）
```

+ **<font style="color:rgb(25, 27, 31);">Precision@K</font>**<font style="color:rgb(25, 27, 31);">：在前K个检索结果中，有多少是相关的。 其中， </font><font style="color:rgb(25, 27, 31);">rel(i)=1</font><font style="color:rgb(25, 27, 31);"> 如果第 i 个结果是相关的，否则 </font><font style="color:rgb(25, 27, 31);">rel(i)=0</font><font style="color:rgb(25, 27, 31);"> 。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741748364832-f09645b0-5bbc-496c-adf0-19d718b2980b.png)

+ **<font style="color:rgb(25, 27, 31);">Recall@K：</font>**<font style="color:rgb(25, 27, 31);">在前K个检索结果中，检索到的相关文档的数量占总相关文档数量的比例。其中，R 是相关文档的总数， </font><font style="color:rgb(25, 27, 31);">rel(i)=1</font><font style="color:rgb(25, 27, 31);"> 如果第 i 个结果是相关的。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741748495995-8f307139-e5f0-4cb0-861c-d33f30bd4007.png)

+ **<font style="color:rgb(25, 27, 31);">MAP (Mean Average Precision)</font>**<font style="color:rgb(25, 27, 31);">：计算多个查询的平均精度（AP）来衡量检索排序性能。Average Precision (AP) 是 Precision@K 的平均值，但只计算在出现相关文档的位置的精度。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741748546324-f8762183-b188-4049-8c3b-bbc3d9e5d569.png)

    - <font style="color:rgb(25, 27, 31);"> m</font><sub><font style="color:rgb(25, 27, 31);">j</font></sub><font style="color:rgb(25, 27, 31);">是第 j 个查询到的相关文档总数。</font>
    - <font style="color:rgb(25, 27, 31);">R</font><sub><font style="color:rgb(25, 27, 31);">jk</font></sub><font style="color:rgb(25, 27, 31);"> 是对于查询 </font><font style="color:rgb(25, 27, 31);">q</font><sub><font style="color:rgb(25, 27, 31);">j</font></sub><sub><font style="color:rgb(25, 27, 31);"> </font></sub><font style="color:rgb(25, 27, 31);">的第 k 个相关文档的检索结果，直到检索到第 k 个相关文档为止。</font>

<font style="color:rgb(25, 27, 31);">MAP 是所有查询的 AP 的平均值。对于单条查询，</font><font style="color:rgb(25, 27, 31);">|Q|=1.</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741748589509-08f8a9a1-4240-4a1d-aa18-273790ea6f2a.png)<font style="color:rgb(25, 27, 31);"></font>

    - <font style="color:rgb(25, 27, 31);">|Q|</font><font style="color:rgb(25, 27, 31);">是查询的总数。</font>
    - <font style="color:rgb(25, 27, 31);">AP(q</font><sub><font style="color:rgb(25, 27, 31);">j</font></sub><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> 是查询 </font><font style="color:rgb(25, 27, 31);">q</font><sub><font style="color:rgb(25, 27, 31);">j</font></sub><font style="color:rgb(25, 27, 31);"> 的平均精度。</font>
3. **上下文精确度****<font style="color:rgb(25, 27, 31);">（Context Precision）</font>**

**<font style="color:rgb(25, 27, 31);">指标含义：</font>**<font style="color:rgb(25, 27, 31);">评估检索结果中排名靠前的上下文与Query的相关性。</font>

```python
同样以上面例子为例，如果我们只考虑前两个结果，上下文精确度是1/2，因为前两个结果中只有一个是精确相关的。如果我们考虑前三个结果，上下文精确度是1/3，因为三个结果中只有一个是精确相关的。
```

:::color5
**<font style="color:#601BDE;">3.排序指标</font>**

:::

1. **平均倒数排名****<font style="color:rgb(51, 51, 51);">(Mean Reciprocal Rank)</font>**

**<font style="color:rgb(25, 27, 31);">指标含义：</font>**<font style="color:rgb(25, 27, 31);">相关文档的排名倒数的平均值。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300701042-1d926a0a-6045-4b0f-81d0-eaa3bb6e994d.png)

```python
用户Query“法国首都”，好的MRR表示“巴黎”这个答案在检索结果中排名第一。
```

<font style="color:rgb(25, 27, 31);">其中， </font><font style="color:rgb(25, 27, 31);">rank</font><sub><font style="color:rgb(25, 27, 31);">q</font></sub><font style="color:rgb(25, 27, 31);"> 是对于查询 q，第一个相关文档的排名。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
def mrr(actual_items, recommended_items):
    for rank, item in enumerate(recommended_items, 1):
        if item in actual_items:
            return 1 / rank
    return 0
```

2. **<font style="color:rgb(25, 27, 31);">NDCG@K (Normalized Discounted Cumulative Gain)：</font>**

**<font style="color:rgb(25, 27, 31);">指标含义：</font>**<font style="color:rgb(25, 27, 31);">同时结合了文档的相关性和它们的排名位置，用于衡量排序质量。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741748931915-fdf7821f-aefa-4afe-9799-138a35c4f527.png)

<font style="color:rgb(25, 27, 31);">其中， </font><font style="color:rgb(25, 27, 31);">DCG</font><sub><font style="color:rgb(25, 27, 31);">k</font></sub><font style="color:rgb(25, 27, 31);"> 是折损累计增益， </font><font style="color:rgb(25, 27, 31);">IDCG</font><sub><font style="color:rgb(25, 27, 31);">k</font></sub><font style="color:rgb(25, 27, 31);"> 是理想排序下的 DCG 值。</font>

:::color5
**<font style="color:#601BDE;">3.生成指标</font>**

:::

<font style="color:rgb(25, 27, 31);">总体来说，就是生成的答案有依据，尽量来源于搜索内容，并且最终给出的答案是能解决问题的</font>

**<font style="color:rgb(25, 27, 31);">1.</font>**** **[**答案真实性**](https://zhida.zhihu.com/search?content_id=247226105&content_type=Article&match_order=1&q=%E7%AD%94%E6%A1%88%E7%9C%9F%E5%AE%9E%E6%80%A7&zhida_source=entity)**（Answer Faithfulness 或 Groundedness）**

**<font style="color:rgb(25, 27, 31);">指标含义：</font>**<font style="color:rgb(25, 27, 31);">评估生成的回答是否基于检索到的文档内容，没有添加不准确或不存在的信息。</font>

```python
如果检索到的上下文是“巴黎是法国首都”，好的答案是“法国首都是巴黎”，而不是“法国首都是伦敦”。
```

**2. **[**答案相关性**](https://zhida.zhihu.com/search?content_id=247226105&content_type=Article&match_order=1&q=%E7%AD%94%E6%A1%88%E7%9B%B8%E5%85%B3%E6%80%A7&zhida_source=entity)**（Answer Relevance）**

**参考：**[**评估**](https://www.yuque.com/zhongxian-iiot9/gi3w2u/nlapi8xm5fmsnx3g)

**<font style="color:rgb(25, 27, 31);">指标含义：</font>**<font style="color:rgb(25, 27, 31);">衡量生成的回答与用户Query的直接相关性。</font>

+ [<font style="color:rgb(9, 64, 142);">BLEU</font>](https://zhida.zhihu.com/search?content_id=247682406&content_type=Article&match_order=1&q=BLEU&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">(Bilingual Evaluation Understudy)：通过计算生成的文本与一个或多个参考文本之间的 n-gram的重叠程度来衡量生成文本的质量。缺点是无法考虑句子的语法、语义和流畅性，对于词序和同义词缺乏敏感性。</font>
+ [<font style="color:rgb(9, 64, 142);">ROUGE</font>](https://zhida.zhihu.com/search?content_id=247682406&content_type=Article&match_order=1&q=ROUGE&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">(Recall-Oriented Understudy for Gisting Evaluation)：也是生成文本和参考文本之间的 n-gram 重叠，但这里计算的是召回率，即生成文本中出现的 n-gram 中有多少出现在参考文本中。ROUGE有多个变种，比如ROUGE-N、ROUGE-L、ROUGE-W、ROUGE-S。</font>
+ [<font style="color:rgb(9, 64, 142);">METEOR</font>](https://zhida.zhihu.com/search?content_id=247682406&content_type=Article&match_order=1&q=METEOR&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">(Metric for Evaluation of Translation with Explicit ORdering)：考虑了同义词和句法结构，是对BLEU的改进。通过词级别的精确度和召回率、词序、词形变化（如词干化）、同义词等来综合评估生成文本的质量。</font>
+ <font style="color:rgb(25, 27, 31);">Bert Score：利用预训练语言模型（如 BERT）对生成文本与参考文本之间的相似度进行计算。</font>

```python
用户Query：“法国的首都是什么？”
检索到的上下文：“法国是一个位于西欧的国家，拥有丰富的文化和历史。”
生成的回答A：“法国的首都是巴黎。”
生成的回答B：“巴黎是法国的首都，一个世界著名的文化和历史中心。”
回答A直接回答了Query，提供了所需的具体信息，因此具有高答案相关性。回答B不仅直接回答了Query，还提供了额外的信息，增加了回答的价值，同样具有高答案相关性。
```

3. **<font style="color:rgb(25, 27, 31);">准确性（Accuracy）</font>**<font style="color:rgb(25, 27, 31);">：生成的回答是否正确，是否与事实相符。</font>
4. **<font style="color:rgb(25, 27, 31);">完整性（Completeness）</font>**<font style="color:rgb(25, 27, 31);">：回答是否提供了足够的信息，是否全面覆盖了Query的各个方面。</font>
5. **<font style="color:rgb(25, 27, 31);">一致性（Consistency）</font>**<font style="color:rgb(25, 27, 31);">：衡量生成答案与给定上下文之间的事实一致性。该指标根据生成的答案和检索到的上下文计算，分数范围在0到1之间，得分越高表示真实性越高。直观上理解：如果生成的答案中的所有声明都能从给定的上下文中推导出来，那么该答案被认为是真实的。</font>
6. **<font style="color:rgb(25, 27, 31);">有帮助性（Helpfulness）</font>**<font style="color:rgb(25, 27, 31);">：回答是否对用户有实际帮助，是否提供了有用的信息或解决方案。</font>



## 语义分割存在的问题 & 优化
:::color5
**<font style="color:#601BDE;">1.问题定位</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">现象诊断</font>**<font style="color:rgb(51, 51, 51);">：明确具体问题（如分</font>**<font style="color:#ED740C;">割边界模糊、关键信息丢失、片段语义不完整</font>**<font style="color:rgb(51, 51, 51);">）</font>
+ **<font style="color:rgb(51, 51, 51);">数据检查</font>**<font style="color:rgb(51, 51, 51);">：查看分割错误的样例，分析是规则/模型缺陷还是数据噪声导致</font>
+ **<font style="color:rgb(51, 51, 51);">指标评估</font>**<font style="color:rgb(51, 51, 51);">：量化分割质量（如BLEU/ROUGE对比原文、下游任务准确率变化）</font>

:::color5
**<font style="color:#601BDE;">1.分割策略调整</font>**

:::

**<font style="color:rgb(51, 51, 51);">A. 算法层优化</font>**

+ **<font style="color:rgb(51, 51, 51);">动态分块</font>**<font style="color:rgb(51, 51, 51);">：替换固定窗口分割为</font>**<font style="color:#74B602;">语义敏感的滑动窗口</font>**<font style="color:rgb(51, 51, 51);">（如使用SBERT计算相邻句子相似度）</font>
+ **<font style="color:rgb(51, 51, 51);">模型增强</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">微调预训练模型（如BERT/TextTiling）适应领域数据</font>
    - <font style="color:rgb(51, 51, 51);">引入指针网络预测分割边界概率</font>
+ **<font style="color:rgb(51, 51, 51);">混合策略</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
# 示例：结合规则与模型的分割逻辑
from transformers import pipeline
segmenter = pipeline("text-classification", model="分割边界检测模型")

def hybrid_segment(text):
    rule_chunks = split_by_punctuation(text)  # 基础规则分割
    model_chunks = []
    for chunk in rule_chunks:
        if segmenter(chunk)["label"] == "BOUNDARY":
            model_chunks.extend(advanced_split(chunk)) 
        else:
            model_chunks.append(chunk)
    return merge_overlaps(model_chunks)
```

**<font style="color:rgb(51, 51, 51);">B. 上下文处理</font>**

+ **<font style="color:rgb(51, 51, 51);">重叠机制</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#74B602;">设置20-30%的chunk重叠率，保留跨片段语义</font>**
+ **<font style="color:rgb(51, 51, 51);">层次化结构</font>**<font style="color:rgb(51, 51, 51);">：构建多粒度索引（句子/段落/章节级）</font>

**<font style="color:rgb(51, 51, 51);">C. 增强策略</font>**

+ **<font style="color:rgb(51, 51, 51);">预分割处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:#74B602;">实体识别过滤</font>**<font style="color:rgb(51, 51, 51);">（保留含关键实体的完整片段）</font>
    - <font style="color:rgb(51, 51, 51);">主题建模划分（LDA/BERTopic</font>**<font style="color:#74B602;">识别话题边界</font>**<font style="color:rgb(51, 51, 51);">）</font>
+ **<font style="color:rgb(51, 51, 51);">后处理矫正</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用LLM校验（</font>**<font style="color:#74B602;">如GPT-4评估片段语义完整性</font>**<font style="color:rgb(51, 51, 51);">）</font>
    - <font style="color:rgb(51, 51, 51);">规则模板匹配修复（如强制合并包含问答对的片段）</font>

:::color5
**<font style="color:#601BDE;">3.评估验证</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">人工评测</font>**<font style="color:rgb(51, 51, 51);">：构建黄金测试集，计算分割准确率</font>
+ **<font style="color:rgb(51, 51, 51);">间接评估</font>**<font style="color:rgb(51, 51, 51);">：对比不同分割策略的检索召回率+生成质量</font>
+ **<font style="color:rgb(51, 51, 51);">A/B测试</font>**<font style="color:rgb(51, 51, 51);">：线上流量分桶测试最终业务指标</font>



## RAG问答效果不好，如何优化？
:::color5
**<font style="color:#601BDE;">1.检索模块优化</font>**

:::

1. <font style="color:rgb(51, 51, 51);">文档预处理优化</font>
+ <font style="color:rgb(51, 51, 51);">采用动态分块策略，结合文本语义而非固定长度分割</font>
+ <font style="color:rgb(51, 51, 51);">实验不同分块重叠率（如10%-30%）</font>
+ <font style="color:rgb(51, 51, 51);">添加元数据标签（文档类型、时间戳、权威度等）</font>
2. <font style="color:rgb(51, 51, 51);">嵌入模型增强</font>
+ <font style="color:rgb(51, 51, 51);">升级至SOTA模型（如BGE-large-zh-v1.5）</font>
+ <font style="color:rgb(51, 51, 51);">领域适配微调（使用contrastive learning）</font>
+ <font style="color:rgb(51, 51, 51);">多向量混合：结合段落级和句子级嵌入</font>
3. <font style="color:rgb(51, 51, 51);">检索策略改进</font>
+ <font style="color:rgb(51, 51, 51);">Hybrid Search：融合密集检索与BM25稀疏检索</font>
+ <font style="color:rgb(51, 51, 51);">多阶段检索架构：粗排→精排模式</font>
+ <font style="color:rgb(51, 51, 51);">查询扩展：使用SPLADE或生成式query改写</font>

:::color5
**<font style="color:#601BDE;">2.生成模块优化</font>**

:::

1. <font style="color:rgb(51, 51, 51);">大模型适配</font>
+ <font style="color:rgb(51, 51, 51);">采用指令微调模型（如ChatGLM3-6B）</font>
+ <font style="color:rgb(51, 51, 51);">动态上下文管理：基于相关性分数过滤低质量段落</font>
+ <font style="color:rgb(51, 51, 51);">结构化提示设计：</font>

```plain
[角色] 专业助手
[约束] 仅使用提供的上下文，若信息不足明确说明
[要求] 分点回答，标注引用来源
```

1. <font style="color:rgb(51, 51, 51);">上下文优化</font>
+ <font style="color:rgb(51, 51, 51);">引入重新排序模型（如Cohere rerank）</font>
+ <font style="color:rgb(51, 51, 51);">上下文压缩技术（Selective Context）</font>
+ <font style="color:rgb(51, 51, 51);">跨段落信息融合算法</font>

:::color5
**<font style="color:#601BDE;">3.评估与迭代</font>**

:::

1. <font style="color:rgb(51, 51, 51);">构建多维评估体系</font>
+ <font style="color:rgb(51, 51, 51);">检索评估：MRR@k、Recall@k</font>
+ <font style="color:rgb(51, 51, 51);">生成评估：ROUGE、BLEU、BERTScore</font>
+ <font style="color:rgb(51, 51, 51);">人工评估维度：事实准确性、完整性、可读性</font>
1. <font style="color:rgb(51, 51, 51);">数据闭环构建</font>
+ <font style="color:rgb(51, 51, 51);">错误案例归因分析（检索失败/生成错误）</font>
+ <font style="color:rgb(51, 51, 51);">困难样本挖掘与增强</font>
+ <font style="color:rgb(51, 51, 51);">用户反馈埋点与主动学习</font>



## 知识库检索不到相关信息，如何优化？<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.知识库扩展</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">扩大知识覆盖范围</font>**
    - **<font style="color:#74B602;">添加更多相关数据源</font>**<font style="color:rgb(51, 51, 51);">，覆盖低频或长尾问题。</font>
    - <font style="color:rgb(51, 51, 51);">使用</font>**<font style="color:#74B602;">数据增强技术</font>**<font style="color:rgb(51, 51, 51);">（如同义词替换、多语言翻译、领域数据生成）。</font>
    - <font style="color:rgb(51, 51, 51);">引入实时或动态更新的外部知识源（如API、数据库、网页爬虫）。</font>
+ **<font style="color:rgb(51, 51, 51);">优化知识库结构</font>**
    - <font style="color:rgb(51, 51, 51);">改进文档分块策略（如按语义段落而非固定长度分块）。</font>
    - <font style="color:rgb(51, 51, 51);">增强元数据（如添加标题、关键词、时间戳等），辅助检索和过滤。</font>
    - <font style="color:rgb(51, 51, 51);">对知识库进行聚类或索引优化，提升检索效率。</font>

:::color5
**<font style="color:#601BDE;">2.query优化</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">查询扩展（Query Expansion）</font>**
    - **<font style="color:#74B602;">添加同义词或相关术语</font>**<font style="color:rgb(51, 51, 51);">（如使用词嵌入或知识图谱扩展关键词）。</font>
    - <font style="color:rgb(51, 51, 51);">利用LLM生成与用户查询相关的上下文或变体。</font>
+ **<font style="color:rgb(51, 51, 51);">query改写（Query Rewriting）</font>**
    - **<font style="color:#74B602;">使用LLM将用户query改写为更明确、结构化的形式</font>**<font style="color:rgb(51, 51, 51);">（例如：</font>**<font style="color:#ED740C;">“解释X的工作原理” → “X的定义、组件及工作流程”</font>**<font style="color:rgb(51, 51, 51);">）。</font>
    - <font style="color:rgb(51, 51, 51);">提取问题中的核心实体和意图，减少模糊性。</font>

:::color5
**<font style="color:#601BDE;">3.检索模块优化</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">混合检索策略</font>**
    - <font style="color:rgb(51, 51, 51);">结合密集检索（Dense Retrieval，如向量相似度）和稀疏检索（Sparse Retrieval，如BM25），平衡召回率与准确率。</font>
    - <font style="color:rgb(51, 51, 51);">使用</font>**<font style="color:#ED740C;">多路召回（Multi-Stage Retrieval）</font>**<font style="color:rgb(51, 51, 51);">，先召回大量候选文档，再通过重排序（Reranker）筛选。</font>
+ **<font style="color:rgb(51, 51, 51);">动态阈值调整</font>**
    - <font style="color:rgb(51, 51, 51);">根据检索结果置信度</font>**<font style="color:#ED740C;">动态调整相似度阈值</font>**<font style="color:rgb(51, 51, 51);">，避免漏检或误检。</font>
    - <font style="color:rgb(51, 51, 51);">对低置信度结果进行二次验证（如LLM判断相关性）。</font>

:::color5
**<font style="color:#601BDE;">4.基于LLM的知识进行兜底</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **LLM的通用知识兜底**
    - <font style="color:rgb(51, 51, 51);">当检索失败时，</font>**<font style="color:#ED740C;">允许生成模型依赖自身参数化知识（需明确告知用户回答可能不精准）</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ **动态生成引导**
    - <font style="color:rgb(51, 51, 51);">生成阶段提示LLM：“未找到相关文档，请基于常识回答：...”或“未找到确切信息，以下是与问题相关的通用解释：...”。</font>
+ **外部资源调用**
    - <font style="color:rgb(51, 51, 51);">集成搜索引擎、API或领域工具（如Wolfram Alpha、专业数据库），补充知识库的不足。</font>

:::color5
**<font style="color:#601BDE;">5.用户交互优化</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">主动澄清需求</font>**
    - <font style="color:rgb(51, 51, 51);">当检索结果不足时，</font>**<font style="color:#74B602;">引导用户细化问题</font>**<font style="color:rgb(51, 51, 51);">（例如：“您是否指X的具体应用场景？”）。</font>
    - <font style="color:rgb(51, 51, 51);">提供多轮对话选项，逐步缩小查询范围。</font>
+ **<font style="color:rgb(51, 51, 51);">透明化反馈</font>**
    - <font style="color:rgb(51, 51, 51);">提示用户“未找到直接答案，以下信息可能相关”，并允许用户标记结果质量以改进系统。</font>

## 如何处理一个200页的pdf，表格/图片怎么处理？
### pdf处理
:::color5
**<font style="color:#601BDE;">1.工具选择</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">核心工具</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - `<font style="color:rgb(51, 51, 51);">PyMuPDF</font>`<font style="color:rgb(51, 51, 51);">/</font>`<font style="color:rgb(51, 51, 51);">fitz</font>`<font style="color:rgb(51, 51, 51);">：高性能PDF解析（支持文本定位和图片提取）</font>
    - `<font style="color:rgb(51, 51, 51);">pdfplumber</font>`<font style="color:rgb(51, 51, 51);">：精准表格检测和解析（基于页面底层路径分析）</font>
    - `<font style="color:rgb(51, 51, 51);">pdf2image</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">+</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">Tesseract OCR</font>`<font style="color:rgb(51, 51, 51);">：处理包含文字的图片</font>
    - `<font style="color:rgb(51, 51, 51);">Unstructured.io</font>`<font style="color:rgb(51, 51, 51);">：开源文档预处理框架（支持混合内容处理）</font>

:::color5
**<font style="color:#601BDE;">3.分层解析</font>**

:::

1. 文本和位置信息解析
2. 表格提取
3. 图片提取

```python
import pdfplumber
import fitz

def parse_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    parsed_data = []

    for page_num in range(len(doc)):
        # 文本和位置信息
        page = doc.load_page(page_num)
        text_blocks = page.get_text("dict")["blocks"]

        # 表格提取
        with pdfplumber.open(pdf_path) as pdf:
            pdf_page = pdf.pages[page_num]
            tables = pdf_page.extract_tables({
                "vertical_strategy": "lines", 
                "horizontal_strategy": "lines"
            })

        # 图片提取
        image_list = page.get_images()
        images = [doc.extract_image(img[0]) for img in image_list]

        parsed_data.append({
            "page": page_num+1,
            "text": text_blocks,
            "tables": tables,
            "images": images
        })
    return parsed_data
```

### 表格处理
:::color5
**<font style="color:#601BDE;">1.表格结构重建</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">提取策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用pdfplumber的</font>`<font style="color:rgb(51, 51, 51);">extract_tables()</font>`<font style="color:rgb(51, 51, 51);">获取二维数组</font>
    - <font style="color:rgb(51, 51, 51);">检测合并单元格（通过分析单元格的top/bottom坐标）</font>
    - <font style="color:rgb(51, 51, 51);">自动生成带合并标记的HTML表格或Markdown表格</font>

:::color5
**<font style="color:#601BDE;">2.语义增强处理</font>**

:::

1. 生成**<font style="color:#74B602;">Markdown表头</font>**
2. 处理行数据
3. 添加上下文

```python
def process_table(table_data):
    markdown_table = []
    # 生成Markdown表头
    headers = table_data[0]
    markdown_table.append("| " + " | ".join(headers) + " |")
    markdown_table.append("| " + " | ".join(["---"]*len(headers)) + " |")

    # 处理数据行
    for row in table_data[1:]:
        markdown_table.append("| " + " | ".join(row) + " |")

    # 添加上下文描述
    return f"表格摘要：本表包含{len(table_data)-1}行数据，字段包括{','.join(headers)}。详细数据如下：\n" + "\n".join(markdown_table)
```

:::color5
**<font style="color:#601BDE;">3.表格存储方式</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">原始数据</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#74B602;">JSON格式存储行列数据</font>**
+ **<font style="color:#74B602;">检索用数据：Markdown格式</font>**<font style="color:rgb(51, 51, 51);">（保留结构特征）</font>
+ **<font style="color:rgb(51, 51, 51);">元数据标注</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">"content_type": "table"</font>`

### 图片处理
:::color5
**<font style="color:#601BDE;">1.关键步骤</font>**

:::

:::success
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741507096289-d561e6f8-f853-4b1f-a8e5-24fc4aba59c0.png)

:::

:::success
**<font style="color:rgb(51, 51, 51);">文字型图片</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">使用</font>`<font style="color:rgb(51, 51, 51);">pytesseract.image_to_string()</font>`<font style="color:rgb(51, 51, 51);">提取文字</font>
+ <font style="color:rgb(51, 51, 51);">坐标映射：记录文字在PDF中的原始位置</font>

**<font style="color:rgb(51, 51, 51);">示意图/图表</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">使用CLIP模型生成英文描述</font>
+ <font style="color:rgb(51, 51, 51);">翻译为中文（可选）</font>

:::



```python
{
  "image_id": "fig_03_12",
  "page": 12,
  "bbox": [x0,y0,x1,y1],
  "ocr_text": "2023年销售趋势...",
  "description": "柱状图显示Q1到Q4销售额增长",
  "image_path": "/images/page12_fig3.png"
}
```



### 文档分块策略
:::color5
**<font style="color:#601BDE;">1.自适应分块算法</font>**

:::

1. 判断元素类型
2. 动态分块策略

```python
def dynamic_chunking(parsed_data, max_tokens=512):
    chunks = []
    current_chunk = []

    for element in parsed_data:
        # 判断元素类型
        if element["type"] == "table":
            processed_table = process_table(element["data"])
            element_tokens = count_tokens(processed_table)
        elif element["type"] == "image":
            element_tokens = count_tokens(element["description"])
        else:
            element_tokens = count_tokens(element["text"])

        # 动态分块逻辑
        if sum(current_chunk) + element_tokens > max_tokens:
            chunks.append(merge_elements(current_chunk))
            current_chunk = []
        current_chunk.append(element)

    return chunks
```

:::color5
**<font style="color:#601BDE;">2.分块特征保留</font>**

:::

+ <font style="color:rgb(51, 51, 51);">保持表格/图片与周边文本的上下文关联</font>
+ <font style="color:rgb(51, 51, 51);">对跨页表格进行特殊拼接处理</font>
+ <font style="color:rgb(51, 51, 51);">添加位置标记：</font>`<font style="color:rgb(51, 51, 51);">[Table 1.3]</font>`<font style="color:rgb(51, 51, 51);">、</font>`<font style="color:rgb(51, 51, 51);">[Figure 2.4]</font>`



### 向量检索
:::color5
**<font style="color:#601BDE;">1.混合编码策略</font>**

:::

<font style="color:rgb(51, 51, 51);">. 混合编码策略</font>

+ <font style="color:rgb(51, 51, 51);">文本：使用M3E,BGE,GTE等文本向量模型</font>
+ <font style="color:rgb(51, 51, 51);">表格：结构特征编码（行列数、标题特征）</font>
+ <font style="color:rgb(51, 51, 51);">图片：CLIP图文embedding</font>

:::color5
**<font style="color:#601BDE;">2.检索增强策略</font>**

:::

+ <font style="color:rgb(51, 51, 51);">建立倒排索引：对表格列名、图片描述建立关键词索引</font>
+ <font style="color:rgb(51, 51, 51);">混合检索：</font>**<font style="color:#74B602;">向量检索 + 关键词检索</font>**

```python
def hybrid_retrieve(query):
    vector_results = vector_db.search(query_embedding)
    keyword_results = inverted_index.search(query)
    return rerank(vector_results + keyword_results)
```

### 生成阶段优化
:::color5
**<font style="color:#601BDE;">1.多模态prompt</font>**

:::

```python
template = """
根据以下上下文回答问题：
{context}

其中包含以下可视化内容：
{tables}
{images}

请特别注意：
- 表格数据需要精确引用
- 图片描述需注明来源位置
- 当涉及数据对比时优先使用表格数据
"""
```

:::color5
**<font style="color:#601BDE;">2.引用溯源机制</font>**

:::

+ <font style="color:rgb(51, 51, 51);">实现基于</font>**<font style="color:#74B602;">元数据的位置回溯</font>**
+ <font style="color:rgb(51, 51, 51);">自动生成引用标记：</font>`<font style="color:rgb(51, 51, 51);">（参见表3.2, 第15页图4）</font>`

### 质量评估
1. **<font style="color:rgb(51, 51, 51);">表格处理准确率</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">单元格内容准确率 ≥95%</font>
    - <font style="color:rgb(51, 51, 51);">合并单元格识别率 ≥90%</font>
2. **<font style="color:rgb(51, 51, 51);">图片处理指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">OCR文字识别CER ≤5%</font>
    - <font style="color:rgb(51, 51, 51);">图像描述相关性Score ≥0.85（BERTScore）</font>
3. **<font style="color:rgb(51, 51, 51);">检索召回率</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">表格相关查询召回率 ≥90%</font>
    - <font style="color:rgb(51, 51, 51);">图片相关查询召回率 ≥85%</font>



# RAG基本流程
## 背景 & 基本概念
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(63, 63, 63);">传统语言模型的局限性</font>**<font style="color:rgb(63, 63, 63);">：传统的语言模型，比如 GPT-3，虽然在生成文本方面表现出色，但它们有一个显著的局限性：</font>**<font style="color:#74B602;">它们依赖于预训练的参数，无法动态访问外部知识</font>**<font style="color:rgb(63, 63, 63);">。这意味着这些模型在处理实时信息、领域特定知识或罕见实体时表现不佳。</font>
2. **<font style="color:rgb(63, 63, 63);">RAG的诞生</font>**<font style="color:rgb(63, 63, 63);">：为了解决传统语言模型的局限性，检索增强生成（Retrieval-Augmented Generation, RAG）技术应运而生。RAG 通过将大规模检索系统与生成模型相结合，解决了传统模型的局限性。</font>

:::

:::color3
**简介：**<font style="color:rgb(63, 63, 63);">为了解决传统语言模型的局限性，检索增强生成（Retrieval-Augmented Generation, RAG）技术应运而生。RAG 通过将大规模检索系统与生成模型相结合，解决了传统模型的局限性。它能够</font>**<font style="color:#ED740C;">动态地从外部知识源（如文档、数据库或结构化数据）中检索信息，并在生成过程中利用这些信息</font>**<font style="color:rgb(63, 63, 63);">，从而生成</font>**<font style="color:#ED740C;">更准确、上下文相关的输出</font>**<font style="color:rgb(63, 63, 63);">。</font>

**paper:**[**https://arxiv.org/pdf/2503.10677**](https://arxiv.org/pdf/2503.10677)

**参考：**[**https://mp.weixin.qq.com/s/pf3kAzEOY4Ordx0h65ixKA**](https://mp.weixin.qq.com/s/pf3kAzEOY4Ordx0h65ixKA)

:::

**RAG overview：**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742355242003-e77c6728-6ce8-4aa6-9bcf-3af975840de1.png)

:::color5
**<font style="color:#601BDE;">1.应用场景</font>**

:::

<font style="color:rgb(63, 63, 63);">RAG 技术在多个领域展现了巨大的潜力，尤其是在</font>**<font style="color:#74B602;">问答、摘要生成和信息检索等任务</font>**<font style="color:rgb(63, 63, 63);">中。例如，在开放域问答中，RAG 模型能够从海量文档中检索相关信息，生成更精确的答案；在文档摘要任务中，它能够利用外部文档生成更丰富、更全面的摘要。此外，RAG 还在对话系统、知识图谱构建等领域展现了强大的能力。</font>

    - **<font style="color:rgb(63, 63, 63);">医疗领域</font>**<font style="color:rgb(63, 63, 63);">，RAG 可以帮助医生快速检索最新的研究数据，辅助诊断和治疗决策。</font>
    - **<font style="color:rgb(63, 63, 63);">法律领域</font>**<font style="color:rgb(63, 63, 63);">，律师可以使用 RAG 来检索最新的法律条文，确保他们的法律建议是最新和准确的。</font>
    - **<font style="color:rgb(63, 63, 63);">教育领域</font>**<font style="color:rgb(63, 63, 63);">，RAG 可以为学生提供个性化的学习材料，帮助他们更好地理解复杂的概念。</font>

<font style="color:rgb(63, 63, 63);">总的来说，RAG 技术通过结合检索和生成的能力，解决了传统语言模型的局限性，使其在多个领域中表现出色。无论是需要实时信息的问答任务，还是需要精确答案的领域特定任务，RAG 都能提供强大的支持。</font>

## 技术步骤
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">RAG模型通过利用外部知识来增强生成过程，从而生成更准确且符合上下文的回答。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742355275823-0b6c0f01-264f-4f27-8d6e-bde9d66c13f4.png)

**<font style="color:rgb(63, 63, 63);">基础RAG方法包括以下几个关键步骤：</font>**

+ <font style="color:rgb(51, 51, 51);">用户意图理解</font>
+ <font style="color:rgb(51, 51, 51);">知识源与解析</font>
+ <font style="color:rgb(51, 51, 51);">知识嵌入</font>
+ <font style="color:rgb(51, 51, 51);">知识索引</font>
+ <font style="color:rgb(51, 51, 51);">知识检索</font>
+ <font style="color:rgb(51, 51, 51);">知识整合</font>
+ <font style="color:rgb(51, 51, 51);">回答生成</font>
+ <font style="color:rgb(51, 51, 51);">知识引用</font>



### 用户意图理解
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">高质量的查询对于检索有价值的知识至关重要。由于</font>**<font style="color:#ED740C;">用户的意图往往不明确，准确理解用户查询是实现更有效和精确检索的关键</font>**<font style="color:rgb(63, 63, 63);">。目前，许多研究专注于提升对用户查询的理解。本两种提升查询质量的关键方法：query分解和query重写。</font>

:::

**意图理解方案详见：**[意图理解](https://www.yuque.com/zhongxian-iiot9/gi3w2u/yqgabqoh38oyedb1)

:::color5
**<font style="color:#601BDE;">1.query分解   Query Decomposition</font>**

:::

<font style="color:rgb(63, 63, 63);">查询分解方法已成为增强语言模型推理能力的有效策略，尤其适用于需要多步或组合推理的复杂任务，例如：</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">最少到最多提示（least-to-most prompting）</font>**<font style="color:rgb(51, 51, 51);"> ：将复杂问题逐步分解为更简单的子问题，从而提升模型在更困难任务上的泛化能力。这种方法在SCAN任务中表现出色，GPT-3模型仅用14个示例就达到了99%以上的准确率。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">自问（Self-ask）</font>**<font style="color:rgb(51, 51, 51);">：采用了类似的方法，但进一步优化了过程，通过让模型提出并回答后续问题，减少了组合性差距，从而实现了更好的多跳推理。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">验证链（Chain-of-Verification, CoVe）</font>**<font style="color:rgb(51, 51, 51);"> ：通过让模型独立验证其回答，提高了答案的可靠性，显著减少了在列表问题和长文本生成任务中的幻觉现象。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">链中搜索（Search-in-the-Chain, SearChain）</font>**<font style="color:rgb(51, 51, 51);">：将信息检索（IR）整合到推理过程中。在该框架中，模型构建一个查询链（Chain-of-Query, CoQ），每个查询都通过IR进行验证，从而提高了推理路径的准确性和可追溯性。SearChain允许模型根据检索到的信息动态调整其推理，从而在多跳问答和事实核查等知识密集型任务中表现出色。</font>

:::color5
**<font style="color:#601BDE;">2.query重写</font>**

:::

<font style="color:rgb(63, 63, 63);">查询重写已成为提升RAG性能的关键技术，特别是在解决语义差距和改善任务结果方面。</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">重写-检索-阅读（Rewrite-Retrieve-Read, RRR）</font>**<font style="color:rgb(51, 51, 51);"> ：通过使用LLM在检索前生成和优化查询，提升了查询与目标知识的对齐，从而在开放域问答和多选任务中显著提高了性能。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">BEQUE</font>**<font style="color:rgb(51, 51, 51);"> ：专注于电子商务搜索中的长尾查询，通过监督微调、离线反馈和对比学习来弥合语义差距，从而在GMV和交易量等业务指标上取得了显著提升。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">HyDE</font>**<font style="color:rgb(51, 51, 51);">：引入了一种零样本的密集检索方法，通过让LLM生成假设文档并将其编码用于检索相关文档，超越了传统的无监督检索器。</font>
+ **<font style="color:rgb(250, 81, 81);">Step-Back Prompting</font>**<font style="color:rgb(51, 51, 51);"> ：鼓励LLM从具体示例中抽象出高级概念，从而在STEM、多跳问答和基于知识的推理任务中提升了推理能力。这些方法共同增强了RAG在跨领域知识密集型任务中的有效性和可扩展性。</font>



### 知识源解析
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">RAG可以利用的知识类型多种多样，为LLM提供了丰富的上下文信息。所使用的知识类别，包括</font>**<font style="color:#ED740C;">结构化、半结构化、非结构化和多模态知识</font>**<font style="color:rgb(63, 63, 63);">，以及它们各自的解析和整合方法。</font>

:::

**知识源类型：**

1. 结构化知识：知识图谱、表格
2. 半结构化知识：web page
3. 非结构化知识：Pdf, text
4. 多模态知识：语音、视频、图片

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742356273388-c85789bf-53cb-4ff8-84a3-f7ef802bedae.png)

:::color5
**<font style="color:#601BDE;">1.结构化知识-知识图谱、表格</font>**

:::

**<font style="color:#74B602;">知识图谱（Knowledge Graphs, KGs）是一种结构化表示</font>**<font style="color:rgb(63, 63, 63);">，以图的形式封装实体及其相互关系。其结构化特性便于高效查询和检索，而语义关系则支持更细致的理解和推理。KGs整合了来自不同来源的信息，提供了统一的知识库。然而，将KGs整合到RAG系统中也面临挑战，包括从大规模KGs中导航和提取相关子图的复杂性、KGs扩展时的可扩展性问题，以及将结构化数据与语言模型的无序数据处理对齐的困难。例如：</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">GRAG</font>**<font style="color:rgb(51, 51, 51);">：通过跨多个文档检索文本子图，提升了RAG系统中的信息检索效率。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">KG-RAG</font>**<font style="color:rgb(51, 51, 51);">：引入了探索链（Chain of Explorations, CoE）算法，通过高效导航KGs来提升知识图谱问答（KGQA）任务的表现。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">GNN-RAG</font>**<font style="color:rgb(51, 51, 51);">：利用图神经网络（GNNs）从KGs中检索和处理信息，在与LLM对接之前增强了推理能力。从历史数据构建KGs作为RAG的外部知识源，有效提升了信息检索和生成能力[255]。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">SURGE框架</font>**<font style="color:rgb(51, 51, 51);">：利用KG信息生成上下文相关且基于知识的对话，提升了交互质量。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">SMART-SLIC</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(250, 81, 81);">KARE</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(250, 81, 81);">ToG 2.0</font>**<font style="color:rgb(51, 51, 51);"> 和</font>**<font style="color:rgb(250, 81, 81);">KAG</font>**<font style="color:rgb(51, 51, 51);">，展示了KGs在特定领域作为外部知识源的有效性，提升了RAG系统的准确性和效率。</font>

:::color5
**<font style="color:#601BDE;">2.半结构化知识-web page</font>**

:::

<font style="color:rgb(63, 63, 63);">半结构化数据介于结构化和非结构化格式之间，具有组织元素但没有严格的模式。例如，</font>**<font style="color:#74B602;">JSON和XML文件、电子邮件以及HTML文档</font>**<font style="color:rgb(63, 63, 63);">。HTML作为网页的基础，结合了标签和属性等结构化组件与自由文本等非结构化内容。</font>

<font style="color:rgb(63, 63, 63);">这种混合特性允许HTML表示复杂信息，包括文本、图像和链接。然而，HTML的灵活性也可能导致不一致和异常，给数据提取和整合到RAG系统带来挑战。</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">HtmlRAG</font>**<font style="color:rgb(51, 51, 51);">：在大多数场景中，开源HTML解析技术仍然是高效数据提取和无缝整合的关键。这些工具提供了强大的解析能力和对多样化HTML结构的适应性，确保了在各种应用场景中的高效性和准确性。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">Beautiful Soup</font>**<font style="color:rgb(51, 51, 51);">：一个用于解析HTML和XML文档的Python库，创建解析树以便轻松提取数据；</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">html5ever</font>**<font style="color:rgb(51, 51, 51);">：由Servo项目开发的开源HTML解析器，遵循WHATWG的“HTML5”规范；</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">htmlparser2</font>**<font style="color:rgb(51, 51, 51);">：一个用于Node.js环境的强大HTML解析器，提供快速灵活的方式处理HTML文档；</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">MyHTML</font>**<font style="color:rgb(51, 51, 51);">“”一个基于Crystal语言的高性能HTML5解析器，绑定到lexborisov的myhtml和Modest库；</font>
+ **<font style="color:rgb(250, 81, 81);">Fast HTML Parser</font>**<font style="color:rgb(51, 51, 51);">，一个极快的HTML解析器，生成最小的DOM树并支持基本元素查询。</font>

:::color5
**<font style="color:#601BDE;">3.非结构化知识-pdf, text</font>**

:::

<font style="color:rgb(63, 63, 63);">非结构化知识涵盖了缺乏一致结构的数据类型，如自由文本和PDF文档。与遵循预定义模式的结构化数据不同，非结构化</font>**<font style="color:#74B602;">数据的格式多样，通常包含复杂内容，使得直接检索和解释具有挑战性</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">解析PDF仍然具有挑战性，因为需要准确解释不同的布局、字体和嵌入结构。</font>**<font style="color:#74B602;">将PDF转换为RAG系统可读的格式需要光学字符识别（OCR）来捕获文本</font>**<font style="color:rgb(63, 63, 63);">，布局分析来理解空间关系，以及先进的方法来解释表格和公式等复杂元素。</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">ABINet</font>**<font style="color:rgb(51, 51, 51);">：通过双向处理增强了OCR的准确性。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">GPTPDF</font>**<font style="color:rgb(51, 51, 51);">：使用视觉模型将表格和公式等复杂元素解析为结构化的Markdown，在大规模处理中具有高成本效益。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">Marker</font>**<font style="color:rgb(51, 51, 51);">：专注于清理噪声元素，同时保留文档的核心格式，非常适合学术和科学文档。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">PDF-Extract-Kit</font>**<font style="color:rgb(51, 51, 51);">：支持高质量内容提取，包括公式识别和布局检测</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">Zerox OCR</font>**<font style="color:rgb(51, 51, 51);">：将PDF页面转换为图像，并使用GPT模型生成Markdown，有效管理标题和表格等结构。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">MarkItDown</font>**<font style="color:rgb(51, 51, 51);">：是一个多功能工具，能够将PDF、媒体、网页数据和存档等多种文件类型转换为Markdown。</font>

:::color5
**<font style="color:#601BDE;">4.多模态知识-语音、视频、图片</font>**

:::

<font style="color:rgb(63, 63, 63);">多模态知识（包括图像、音频和视频）提供了丰富的互补信息，可以显著增强RAG系统，特别是在需要深度上下文理解的任务中。图像提供空间和视觉细节，音频贡献时间和语音层，而视频结合了空间和时间维度，捕捉运动和复杂场景。传统的RAG系统主要设计用于文本数据，在处理和检索这些模态的信息时往往表现不佳，导致在非文本内容至关重要时生成不完整或不够细致的回答。</font>

<font style="color:rgb(63, 63, 63);">为了应对这些限制，现代多模态RAG系统开发了基本方法来整合和检索跨模态的数据。其核心理念是将不同模态对齐到一个共享的嵌入空间中进行统一处理和检索。</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">CLIP</font>**<font style="color:rgb(51, 51, 51);">：将视觉和语言对齐到一个共享空间</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">Wav2Vec 2.0</font>**<font style="color:rgb(51, 51, 51);"> 和</font>**<font style="color:rgb(250, 81, 81);">CLAP</font>**<font style="color:rgb(51, 51, 51);">：音频模型则专注于音频与文本的对齐。</font>
+ **<font style="color:rgb(250, 81, 81);">ViViT</font>**<font style="color:rgb(51, 51, 51);">：处理空间和时间特征。</font>



### 知识嵌入 （Knowledge Embedding）
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">知识通常存储在大量文本文档中，首先被分割为简洁且有意义的单元，每个单元封装一个核心思想。这些单元随后被转换为</font>**<font style="color:#ED740C;">向量embedding，编码语义信息，便于通过相似性度量进行高效检索</font>**<font style="color:rgb(63, 63, 63);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.分块划分</font>**

:::

<font style="color:rgb(63, 63, 63);">分块划分是一个基础过程，显著影响文档检索质量，从而影响整体性能。分块划分的主要目标是</font>**<font style="color:#74B602;">将大段文本分割为可管理的单元或“块”，从而实现更高效的检索和生成</font>**<font style="color:rgb(63, 63, 63);">。通过将复杂文档分割为更小、连贯的单元，RAG可以实现对上下文保留的精细控制，并提升信息检索的准确性。</font>

**<font style="color:rgb(63, 63, 63);">分块的目标和挑战</font>**<font style="color:rgb(63, 63, 63);">：确保分割后的块保留有意义的上下文，同时避免冗余和信息丢失。传统的分块方法，如</font>**<font style="color:#117CEE;">固定长度、基于规则或基于语义的划分，相对简单，但缺乏捕捉复杂文本中细微结构的灵活性</font>**<font style="color:rgb(63, 63, 63);">。这些方法在处理格式多样或包含跨段落语义流的文档时往往表现不佳，导致由于上下文信息碎片化而检索效果不理想。</font>

<font style="color:rgb(63, 63, 63);">随着分块划分方法的演变，早期的固定长度方法逐渐被更</font>**<font style="color:#74B602;">自适应和智能的策略所取代</font>**<font style="color:rgb(63, 63, 63);">。最近的优化策略旨在捕捉文本中细粒度的信息分布和语义结构。例如：</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">命题级分块</font>**<font style="color:rgb(51, 51, 51);">：将文本分割为单个事实的小单元，从而捕捉更丰富的信息。</font>
+ **<font style="color:rgb(250, 81, 81);">LumberChunker</font>**<font style="color:rgb(51, 51, 51);">：使用</font>**<font style="color:#74B602;">LLM检测段落之间的内容变</font>**<font style="color:rgb(51, 51, 51);">化，从而创建上下文敏感的块。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">元分块方法</font>**<font style="color:rgb(51, 51, 51);">：（如边际采样分块和困惑度分块）优化块边界，以更好地满足RAG需求，提升上下文捕捉和检索效果。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">延迟分块</font>**<font style="color:rgb(51, 51, 51);">：一种创新方法，与传统做法不同，它在分块之前对整个文档进行嵌入，从而使模型保留完整的上下文，特别是在处理复杂或上下文密集的文本时，显著改善了检索结果。这些先进的分块策略使RAG能够更好地适应复杂的文档结构，捕捉细微信息，并提升检索准确性，为多样化的检索和生成任务提供了更强大的支持。</font>

:::color5
**<font style="color:#601BDE;">2.文本embedding模型</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742364517148-745abb98-95b3-44cd-b20c-176431cdd1bd.png)

<font style="color:rgb(63, 63, 63);">在基于查询检索块时，该过程依赖于查询与块之间的向量相似性计算（如余弦相似性）。将块准确映射为向量表示对于有效捕捉语义意义并与相关查询对齐至关重要。</font>

**<font style="color:rgb(63, 63, 63);">传统方法：</font>**

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">词袋模型（Bag of Words, BoW）</font>**<font style="color:rgb(51, 51, 51);">：强调词频但忽略语法</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">N-gram</font>**<font style="color:rgb(51, 51, 51);">：捕捉语言结构但面临维度挑战</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">TF-IDF模型</font>**<font style="color:rgb(51, 51, 51);">：结合了词频和上下文，但仍受高维度问题的限制。</font>

<font style="color:rgb(63, 63, 63);">以上方法无法全面表示语义信息。</font>

**<font style="color:rgb(63, 63, 63);">基于深度学习的现代词嵌入方法</font>**<font style="color:rgb(63, 63, 63);">：参考：</font>[文本编码器](https://www.yuque.com/zhongxian-iiot9/gi3w2u/hmr02cyvdppxq80w)

+ **<font style="color:rgb(250, 81, 81);">Word2Vec</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(250, 81, 81);">GloVe</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(250, 81, 81);">fastText</font>**<font style="color:rgb(51, 51, 51);">：通过利用上下文、共现模式或词根变化来编码单词。</font><font style="color:rgb(63, 63, 63);">然而，这些嵌入是静态的，无法适应不同的上下文。</font>
+ **<font style="color:rgb(250, 81, 81);">Transformer架构</font>**<font style="color:rgb(63, 63, 63);"> 的引入，特别是</font>**<font style="color:rgb(250, 81, 81);">BERT</font>**<font style="color:rgb(63, 63, 63);"> ，在捕捉上下文意义和增强语义表示方面取得了重大进展。BERT 及其衍生模型，如</font>**<font style="color:rgb(250, 81, 81);">RoBERTa</font>**<font style="color:rgb(63, 63, 63);">、</font>**<font style="color:rgb(250, 81, 81);">ALBERT</font>**<font style="color:rgb(63, 63, 63);"> 和</font>**<font style="color:rgb(250, 81, 81);">DPR</font>**<font style="color:rgb(63, 63, 63);">，显著提升了文档检索能力。</font>
+ **<font style="color:rgb(250, 81, 81);">BGE</font>**<font style="color:rgb(63, 63, 63);">、</font>**<font style="color:rgb(250, 81, 81);">NV-Embed</font>**<font style="color:rgb(63, 63, 63);">和</font>**<font style="color:rgb(250, 81, 81);">SFR-Embedding</font>**<font style="color:rgb(63, 63, 63);">，在多语言和特定领域的基准测试中表现出色。</font>

:::color5
**<font style="color:#601BDE;">3.多模态embedding模型</font>**

:::

<font style="color:rgb(63, 63, 63);">知识不仅以文本形式表示，还包括图像、音频和视频。因此，对多模态嵌入模型的需求日益增加，这些模型将来自不同模态的信息整合到一个统一的向量空间中。这些模型专门设计用于捕捉不同数据类型之间的关系和共享信息，从而实现更全面和统一的表示。</font>

1. **<font style="color:#601BDE;">对于图像</font>**<font style="color:rgb(63, 63, 63);">，模型处理JPG或PNG等图像格式，生成与文本相同的语义向量空间中的嵌入。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">Normalizer-Free ResNets (NFNet)</font>**<font style="color:rgb(51, 51, 51);"> ：提供了一个高效的框架来提取图像特征</font>
+ <font style="color:rgb(51, 51, 51);">Vision Transformer (ViT)： 利用Transformer架构学习高质量表示。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">对比语言-图像预训练（CLIP）</font>**<font style="color:rgb(51, 51, 51);">：通过对比学习将视觉和文本模态对齐，生成了适用于零样本分类和跨模态检索的多功能嵌入。</font>
2. **<font style="color:#601BDE;">对于音频</font>**<font style="color:rgb(63, 63, 63);">，模型提取音高、音色、节奏和语义等关键特征，从而实现对音频的有效和有意义分析，以支持检索任务。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">Wav2Vec 2.0</font>**<font style="color:rgb(51, 51, 51);">：一种自监督学习模型，直接从原始波形中学习音频表示，生成适用于多种音频任务的高层次嵌入。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">对比语言-音频预训练（CLAP）</font>**<font style="color:rgb(51, 51, 51);">：一种最先进的模型，通过从成对的音频和文本数据中学习生成音频嵌入，为音频与自然语言的整合提供了统一框架。</font>
3. **<font style="color:#601BDE;">对于视频</font>**<font style="color:rgb(63, 63, 63);">，模型旨在将视频数据表示为紧凑且特征丰富的向量，捕捉空间、时间和语义信息。</font>
+ <font style="color:rgb(51, 51, 51);">Video Vision Transformer (ViViT)：基于ViT，能够有效处理视频理解任务，捕捉空间和时间特征。</font>
+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">VideoPrism</font>**<font style="color:rgb(51, 51, 51);">：因其在广泛视频理解基准测试中的最先进表现而备受关注。它特别擅长在不同视频领域中泛化，而无需特定任务的微调。</font>



### 知识索引
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">在RAG中，</font>**<font style="color:#ED740C;">索引被定义为数据的结构化组织，能够从大规模数据集中高效访问和检索信息</font>**<font style="color:rgb(63, 63, 63);">。索引将用户查询映射到相关的文档块、知识片段或其他信息内容，充当存储数据与检索机制之间的桥梁。索引的有效性对RAG系统至关重要，因为它直接影响响应准确性、检索速度和计算效率。</font>

:::

:::color5
**<font style="color:#601BDE;">1.索引结构</font>**

:::

1. **<font style="color:rgb(63, 63, 63);">结构化索引</font>**<font style="color:rgb(63, 63, 63);">：结构化索引基于预定义的固定属性组织数据，通常采用</font>**<font style="color:#74B602;">表格或关系格式</font>**<font style="color:rgb(63, 63, 63);">。在早期的知识检索工作中，如</font>**<font style="color:rgb(250, 81, 81);">REALM</font>**<font style="color:rgb(63, 63, 63);">系统，文本倒排索引被广泛用作基础技术，而</font>**<font style="color:rgb(250, 81, 81);">Table RAG</font>**<font style="color:rgb(63, 63, 63);">则使用特定于表格的索引结构，结合列索引和行索引，以高效检索相关表格条目用于语言生成任务。</font>
2. **非结构化索引**<font style="color:rgb(63, 63, 63);">：非结构化索引则设计用于自由格式或半结构化数据，在现代RAG系统中更为常见。</font>**<font style="color:#74B602;">向量索引</font>**<font style="color:rgb(63, 63, 63);">利用先前嵌入阶段生成的向量来提高检索效率，如</font>**<font style="color:rgb(250, 81, 81);">naive RAG</font>**<font style="color:rgb(63, 63, 63);">、</font>**<font style="color:rgb(250, 81, 81);">ANCE</font>**<font style="color:rgb(63, 63, 63);">和</font>**<font style="color:rgb(250, 81, 81);">G-retriever</font>**<font style="color:rgb(63, 63, 63);">，后者使用语言模型将图的文本属性转换为向量。</font>
3. **图索引**<font style="color:rgb(63, 63, 63);">：图索引是一种非结构化索引，利用</font>**<font style="color:#74B602;">图结构的固有优势来表示和检索互连数据</font>**<font style="color:rgb(63, 63, 63);">。在图索引中，数据点被表示为节点，而它们之间的关系通过边表示。这种索引范式特别擅长捕捉语义关系和上下文信息，从而支持复杂的查询和推理任务。</font>

### 知识检索
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">在RAG系统中，知识检索是一个关键步骤，决定了生成模型能够获取到哪些外部知识。知识检索的目标是</font>**<font style="color:#ED740C;">从大规模的外部知识库中快速、准确地找到与用户查询最相关的信息</font>**<font style="color:rgb(63, 63, 63);">。为了实现这一目标，RAG系统通常依赖于高效的检索算法和索引结构。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742364955886-5a2e0fed-d8ec-40aa-a43b-6d2d267090f0.png)

:::color5
**<font style="color:#601BDE;">1.检索策略  Retrieval Strategies</font>**

:::

<font style="color:rgb(63, 63, 63);">检索的目标是根据输入查询识别并提取最相关的知识。通过使用相似性函数检索最相关的 top-k 个知识块。根据不同的相似性函数，检索策略可以分为三种类型：稀疏检索、稠密检索和混合检索。</font>

1. **<font style="color:rgb(250, 81, 81);">稀疏检索</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">稀疏检索策略通过词语分析和匹配利用稀疏向量检索文档或知识块。传统的稀疏检索策略使用术语匹配指标，如 BM25、TF-IDF 和查询似然，通过计算词语出现频率和逆文档频率来估计文档与查询的相关性。</font>

2. **<font style="color:rgb(250, 81, 81);">稠密检索</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">稠密检索策略将</font>**<font style="color:#74B602;">查询和文档编码到低维向量空间</font>**<font style="color:rgb(63, 63, 63);">中，通过向量表示的点积或余弦相似度来衡量相关性。稠密检索器，如 DPR 和 ANCE，基于 BERT 架构的预训练语言模型，并在无监督数据上进行微调，以生成高质量的查询和文档表示。</font>

<font style="color:rgb(63, 63, 63);">最近，大语言模型（LLMs）在语义理解和表示能力方面表现出色。基于 LLMs 的强大能力，研究者们尝试使用 LLMs 生成判别性文本嵌入。例如，</font>**<font style="color:#74B602;">Llama2Vec </font>**<font style="color:rgb(63, 63, 63);"> 是一种轻量级方法，通过两个无监督预训练任务（EBAE 和 EBAR）将 LLMs 用于稠密检索。RepLLaMA 微调 LLaMA 作为稠密检索器，利用其整体表示长文档的能力进行高效文本检索。</font>

3. **<font style="color:rgb(250, 81, 81);">混合检索</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">混合检索策略结合了稀疏和稠密检索技术，旨在通过利用每种方法的优势来优化性能。例如，RAP-Gen 和 BlendedRAG 将传统的关键词匹配与深度语义理解相结合，使系统既能从稀疏检索的效率中受益，又能通过稠密表示捕获更深层次的上下文。BASHEXPLAINER 采用两阶段训练策略，首先使用稠密检索器捕获语义信息，然后使用稀疏检索器获取词汇信息，从而实现性能优异的自动代码注释生成。这种双重策略解决了每种方法的局限性；例如，稀疏策略可能在语义细微差别上表现不佳，而稠密策略则可能计算密集。通过结合两者的优势，混合模型提高了各种任务中的检索准确性和相关性。</font>

:::color5
**<font style="color:#601BDE;">2.搜索方法 Search Approaches</font>**

:::

<font style="color:rgb(63, 63, 63);">搜索方法是指为给定查询向量</font>**<font style="color:#74B602;">从向量数据库中高效识别相似向量的算法</font>**<font style="color:rgb(63, 63, 63);">。搜索方法可以分为两种类型：最近邻搜索（NNS）和近似最近邻搜索（ANNS）。</font>

1. **<font style="color:rgb(250, 81, 81);">最近邻搜索</font>**<font style="color:rgb(63, 63, 63);"> </font>**<font style="color:rgb(63, 63, 63);"> (Nearest Neighbor Search)</font>**

<font style="color:rgb(63, 63, 63);">NNS 的暴力算法是一种简单的算法，穷举扫描数据库中的所有向量，计算与查询向量的距离以识别最接近的向量。然而，这种方法计算成本高，在大规模数据集上不切实际。</font>

<font style="color:rgb(63, 63, 63);">引入了基于树的方法来提高搜索效率。例如，Bentley 提出了一种基于 k-d 树的方法，该方法将 k 维空间递归划分为超矩形区域，从而提高了数据组织和搜索速度。其他基于树的结构，如 Ball-tree、R-tree和 M-tree，也通过将数据划分为超球体、矩形或度量空间等结构来增强最近邻搜索，从而提高了搜索性能，特别是在高维和复杂数据集中。</font>

2. **<font style="color:rgb(250, 81, 81);">近似最近邻搜索</font>**<font style="color:rgb(63, 63, 63);"> </font>**<font style="color:rgb(63, 63, 63);"> (Approximate Nearest Neighbor Search)</font>**

<font style="color:rgb(63, 63, 63);">ANNS 在准确性、速度和内存效率之间取得了平衡，使其特别适用于大规模和高维数据。这包括基于哈希的方法、基于树的方法、基于图的方法和基于量化的方法。</font>

+ **<font style="color:rgb(51, 51, 51);">基于哈希的方法</font>**<font style="color:rgb(51, 51, 51);">，将高维向量转换为二进制代码，优化内存使用并加速搜索操作。例如，深度哈希使用深度神经网络学习哈希函数，将高维向量映射为二进制代码，同时保留相似数据之间的语义关系。</font>
+ **<font style="color:rgb(51, 51, 51);">基于树的 ANNS 方法</font>**<font style="color:rgb(51, 51, 51);">，包括</font>**<font style="color:#74B602;"> K-means 树和 ANNOY</font>**<font style="color:rgb(51, 51, 51);">，通过层次化组织数据，通过高效遍历树结构来减少搜索空间。这些方法将数据集划分为分区或簇，使得在搜索过程中仅探索相关区域。</font>
+ **<font style="color:rgb(51, 51, 51);">基于图的方法</font>**<font style="color:rgb(51, 51, 51);">，如分层可导航小世界（HNSW），通过反映数据点之间接近度的边连接数据点，从而通过导航图快速进行最近邻搜索。</font>
+ **<font style="color:rgb(51, 51, 51);">基于量化的方法</font>**<font style="color:rgb(51, 51, 51);">，如乘积量化，旨在通过将向量量化为较小的码本来压缩数据，从而在保持搜索速度和准确性之间良好平衡的同时减少内存需求。</font>

<font style="color:rgb(63, 63, 63);">多样化的 ANNS 方法为大规模、高维数据集中的快速高效最近邻搜索提供了强大的解决方案，每种方法在准确性、速度和内存使用方面都有其自身的权衡。</font>





### 知识整合
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">知识整合是指</font>**<font style="color:#ED740C;">将检索到的外部知识与生成模型的内部知识相结合</font>**<font style="color:rgb(63, 63, 63);">，以提高输出的准确性和连贯性。基本上，知识整合可以分为三种类型：</font>**<font style="color:#ED740C;">输入层整合、中间层整合和输出层整合</font>**<font style="color:rgb(63, 63, 63);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.输入层整合</font>**

:::

<font style="color:rgb(63, 63, 63);">输入层整合是指</font>**<font style="color:#74B602;">在输入层将检索到的信息与原始查询直接整合</font>**<font style="color:rgb(63, 63, 63);">，旨在增强生成过程中的上下文信息。根据整合方法的不同，输入层整合可以分为两种类型：文本级整合和特征级整合。</font>

1. **<font style="color:rgb(250, 81, 81);">文本级整合</font>**<font style="color:rgb(63, 63, 63);">  </font>

**<font style="color:#74B602;">将检索到的 top-k 文档直接与查询拼接</font>**<font style="color:rgb(63, 63, 63);">。为了减少低质量信息的影响并更好地利用大语言模型（LLMs）的上下文学习能力，一些方法对知识块进行重新排序，优先处理最相关的内容，而另一些方法则应用加权过滤从检索内容中去除不相关信息。由于 LLMs 的输入长度限制，对上下文进行压缩，使模型能够在有限的输入大小内学习更多信息。</font>

2. **<font style="color:rgb(250, 81, 81);">特征级整合</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">特征级整合侧重于在特征级别将检索内容的编码形式与原始输入整合。与简单地拼接原始文本不同，将</font>**<font style="color:#74B602;">输入查询和检索到的文档转换为特征表示（如稠密或稀疏向量）</font>**<font style="color:rgb(63, 63, 63);">，然后再输入到模型中。通过在特征表示而非原始文本上操作，特征级整合允许对输入数据进行更灵活的操纵。</font>

:::color5
**<font style="color:#601BDE;">2.中间层整合</font>**

:::

<font style="color:rgb(63, 63, 63);">中间层整合是指将外部知识整合到生成器的隐藏层中。</font>**<font style="color:rgb(250, 81, 81);">基于注意力的方法</font>**<font style="color:rgb(63, 63, 63);"> 是中间层整合中常见的方法之一。</font>

+ <font style="color:rgb(51, 51, 51);">RETRO 模型：引入了一种新颖的交叉注意力模块，将检索到的信息与模型的中间表示相结合。</font>
+ <font style="color:rgb(51, 51, 51);">TOME：引入了 </font>_<font style="color:rgb(51, 51, 51);">提及记忆</font>_<font style="color:rgb(51, 51, 51);"> 机制，通过存储和检索实体提及表示，将外部知识整合到 Transformer 中。</font>
+ <font style="color:rgb(51, 51, 51);">LongMem框架：使用自适应残差网络进行记忆检索，结合注意力机制高效访问和检索相关的长期记忆。</font>

:::color5
**<font style="color:#601BDE;">3.输出层整合</font>**

:::

<font style="color:rgb(63, 63, 63);">输出层整合是指在生成器的输出层整合检索到的知识。这种方法通常将</font>**<font style="color:#74B602;">检索知识的 logits 与模型的输出 logits 结合</font>**<font style="color:rgb(63, 63, 63);">，从而实现增强生成。输出层整合可以分为两个主要分支：</font>

+ <font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(250, 81, 81);">基于集成的整合</font>**<font style="color:rgb(51, 51, 51);"> 聚合来自检索的 logits，例如在 kNN-LM中，最近邻的概率与模型的预测进行插值，以提高泛化能力和鲁棒性。</font>
+ **<font style="color:rgb(250, 81, 81);">基于校准的整合</font>**<font style="color:rgb(51, 51, 51);"> 则使用检索 logits 来优化模型的预测置信度，如置信度增强的 kNN-MT。</font>

### 答案生成
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">在 RAG 系统中，生成组件是</font>**<font style="color:#ED740C;">生成既准确又上下文相关的回答的核心</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">然而，在 RAG 模型中实现高质量输出需要</font>**<font style="color:#ED740C;">克服两大挑战</font>**<font style="color:rgb(63, 63, 63);">：</font>

1. <font style="color:rgb(63, 63, 63);">处理噪声检索</font>
2. <font style="color:rgb(63, 63, 63);">实现对多样化信息的有效推理。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742365951881-26f840f6-2754-4a38-bcde-0d870166e8f7.png)

:::color5
**<font style="color:#601BDE;">1.去噪 Denoising</font>**

:::

<font style="color:rgb(63, 63, 63);">去噪在 RAG 模型中至关重要，目的是</font>**<font style="color:#74B602;">减少从大型知识库中检索到的无关、矛盾或误导性信息</font>**<font style="color:rgb(63, 63, 63);">的影响。检索中的噪声会严重影响生成输出的事实准确性和连贯性，因此去噪机制在 RAG 管道中不可或缺。</font>

1. **<font style="color:rgb(250, 81, 81);">显式去噪技术</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">一种有效的去噪方法是通过显式监督。InstructRAG引入了 </font>**<font style="color:rgb(250, 81, 81);">理性生成</font>**<font style="color:rgb(63, 63, 63);">，模型被指示生成中间理性，以澄清每个检索文档的相关性。这些理性通过引导模型专注于更准确和上下文相关的内容，有效地过滤了噪声。REFEED 框架利用大语言模型根据检索数据重新评估响应的准确性，迭代地丢弃不太相关的信息，从而优化初始答案。</font>

2. **<font style="color:rgb(250, 81, 81);">基于判别器的去噪</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">COMBO 框架使用</font>**<font style="color:#74B602;">预训练的判别器将生成的段落与检索到的段落配对</font>**<font style="color:rgb(63, 63, 63);">，在最终生成阶段之前评估每对的连贯性和相关性。这种基于判别器的方法确保识别并过滤无关或矛盾的信息，从而最小化幻觉的风险。</font>

3. **<font style="color:rgb(250, 81, 81);">自反思和自适应去噪</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">Self-RAG引入了一种自反思机制，模型通过评估其响应的连贯性和事实性来批评和修订自己的输出。这种方法提供了一种动态处理噪声的方式，因为模型可以通过自我评估迭代地过滤不可信或无关的信息。此外，自适应检索策略允许模型根据任务特定标准检索文档，动态调整检索范围和过滤强度，以优化相关性和质量。</font>

4. **<font style="color:rgb(250, 81, 81);">上下文过滤和置信度评分</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">模型可以根据</font>**<font style="color:#74B602;">检索信息与查询的一致性为其分配分数</font>**<font style="color:rgb(63, 63, 63);">，在整合之前过滤掉低置信度的检索。这种方法利用置信度阈值系统地排除噪声文档，特别适用于相关性差异显著的开放域问答任务。</font>

:::color5
**<font style="color:#601BDE;">2.推理 Reasoning</font>**

:::

<font style="color:rgb(63, 63, 63);">除了去噪，</font>**<font style="color:#601BDE;">推理(Reasoning)</font>**<font style="color:rgb(63, 63, 63);">对于需要跨多个文档综合信息的任务至关重要。有效的推理使模型能够将检索到的信息情境化，建立逻辑连贯性，并生成准确反映复杂关系的响应。</font>

1. **<font style="color:rgb(250, 81, 81);">结构化知识和基于图的推理</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">一种高级推理方法涉及整合结构化知识源（如知识图谱）以辅助复杂的关系推理。Think-on-Graph 2.0 引入了一个框架，</font>**<font style="color:#74B602;">将知识图谱与非结构化文本相结合，使模型能够推理实体之间的结构化关系</font>**<font style="color:rgb(63, 63, 63);">。通过利用图结构，模型获得了更深层次的上下文理解，提高了回答涉及复杂关系的查询的能力。</font>

2. **<font style="color:rgb(250, 81, 81);">跨注意力用于多文档推理</font>**<font style="color:rgb(63, 63, 63);">  （cross attention）</font>

<font style="color:rgb(63, 63, 63);">为了促进跨多个文档的推理，RETRO 模型采用了分块跨注意力，使生成模型能够关注检索到的文本块中的相关信息。这种跨注意力机制有助于保持上下文连贯性，特别是在信息跨越多个文档的开放域设置中。跨注意力也在增强的 kNN 方法中得到了探索，其中 kNN 注意力层允许模型在生成过程中利用邻域信息，从而实现上下文相关内容的无缝整合。</font>

3. **<font style="color:rgb(250, 81, 81);">记忆增强推理</font>**<font style="color:rgb(63, 63, 63);">  </font>

<font style="color:rgb(63, 63, 63);">记忆增强推理，如 EAE 和 TOME 等模型中所示，整合了特定实体的记忆模块。这些模型存储并动态检索与实体相关的信息，使生成模型能够随着时间的推移保持一致性和连贯性。记忆模块在需要纵向一致性或多步推理的任务中特别有益，因为它们允许模型在对话或文档的不同部分中回忆特定实体的细节。</font>

4. **<font style="color:rgb(250, 81, 81);">检索校准和选择性推理</font>**

<font style="color:rgb(63, 63, 63);">推理的另一个关键进展是检索校准，模型被训练为根据上下文相关性优先处理某些检索信息。校准技术帮助模型识别最关键的信息，在推理之前过滤掉不太相关的检索。</font>

5. **<font style="color:rgb(250, 81, 81);">分层和多轮推理</font>**

<font style="color:rgb(63, 63, 63);">对于需要多步推理的复杂查询，</font>**<font style="color:#74B602;">分层或多轮推理模型允许模型迭代处理检索到的信息</font>**<font style="color:rgb(63, 63, 63);">，每轮都优化其理解。多轮推理特别适用于涉及因果或时间依赖性的任务，因为它使模型能够根据新信息“重新审视”先前的知识，形成分层的理解，从而提高响应的准确性和连贯性。</font>

### 知识引用 (Knowledge Citation)
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">在 RAG 中，引用对于确保模型响应的透明度、可信度和事实基础至关重要。通过将生成的内容</font>**<font style="color:#ED740C;">归因于可验证的来源</font>**<font style="color:rgb(63, 63, 63);">，用户可以轻松验证信息，减少声明验证的负担，并改进评估过程。此外，有效的引用有助于减少幻觉，增强模型输出的事实完整性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.引用生成策略</font>**

:::

<font style="color:rgb(63, 63, 63);">在语言模型中生成引用有两种主要策略：</font>**<font style="color:rgb(250, 81, 81);">同步引用生成</font>**<font style="color:rgb(63, 63, 63);"> 和 </font>**<font style="color:rgb(250, 81, 81);">生成后引用检索</font>**<font style="color:rgb(63, 63, 63);">。</font>

+ <font style="color:rgb(51, 51, 51);">同步生成被 WebGPT、GopherCite 和 RECLAIM 等模型使用，它们在</font>**<font style="color:#74B602;">响应生成过程中实时检索信息</font>**<font style="color:rgb(51, 51, 51);">。这种方法确保答案和引用紧密对齐，减少幻觉并提高事实准确性。</font>
+ <font style="color:rgb(51, 51, 51);">生成后引用被 RARR和 LaMDA等模型使用，它</font>**<font style="color:#74B602;">先生成答案，然后再检索引用</font>**<font style="color:rgb(51, 51, 51);">。虽然这种方法降低了计算复杂性，但由于答案的生成独立于引用，增加了响应与引用来源之间不一致的风险。</font>

<font style="color:rgb(63, 63, 63);">两种方法各有优势：同步生成提供了更强的事实基础，而生成后引用则在响应生成中提供了更大的灵活性。</font>

:::color5
**<font style="color:#601BDE;">2.引用粒度的进展</font>**

:::

**<font style="color:rgb(250, 81, 81);">引用粒度</font>**<font style="color:rgb(63, 63, 63);">——即引用中提供的细节水平——在最近的模型中有了显著提升。早期的模型如 LaMDA 使用粗粒度引用，通常引用整个文档或 URL，虽然有助于事实基础，但需要用户筛选无关信息。最近的模型，如 WebGPT、WebBrain和 GopherCite，已经向</font>**<font style="color:#74B602;">细粒度引用发展</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">这些模型检索特定的证据片段，或专注于理解长文档以支持个别声明。RECLAIM 模型代表了最高水平的引用粒度，将个别声明链接到源材料中的确切句子。</font>

## 高级RAG（RAG的改进方法）
:::color1
<font style="color:rgb(63, 63, 63);">高级RAG方法超越了基础的RAG模型，通过一系列创新技术克服了基础RAG系统的局限性。这些方法旨在从多个维度提升RAG系统的能力，包括训练优化、多模态处理、记忆增强和智能推理。</font>

:::

### RAG训练
:::color3
**简介****：**<font style="color:rgb(63, 63, 63);">RAG训练的核心在于</font>**<font style="color:#ED740C;">优化检索和生成组件之间的协同作用</font>**<font style="color:rgb(63, 63, 63);">，以实现最佳性能。有效的训练策略确保检索器获取相关信息的同时，生成器能够产生连贯且准确的输出。本节将介绍三种主要的训练方法：</font>**<font style="color:#ED740C;">静态训练、单向引导训练和协同训练。</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742367360108-a735024b-2dd9-476c-896b-b754c151a01e.png)

:::color5
**<font style="color:#601BDE;">1.静态训练</font>**

:::

<font style="color:rgb(63, 63, 63);">静态训练是一种简单但有效的方法，在训练过程中</font>**<font style="color:#74B602;">固定检索器或生成器中的一个组件，专注于优化另一个组件</font>**<font style="color:rgb(63, 63, 63);">。这种方法在计算资源有限或需要快速部署的场景中尤为适用。例如，固定检索器并优化生成器可以利用已有的检索机制（如BM25或BERT），从而减少训练开销。然而，静态训练的缺点是可能影响系统的整体性能，因为只有单一组件被优化，可能导致检索与生成之间的协同作用不足。</font>

:::color5
**<font style="color:#601BDE;">2.单向引导训练</font>**

:::

<font style="color:rgb(63, 63, 63);">单向引导训练通过一个组件引导另一个组件的优化，分为</font>**<font style="color:#74B602;">检索器引导生成器训练</font>**<font style="color:rgb(63, 63, 63);">和</font>**<font style="color:#74B602;">生成器引导检索器训练</font>**<font style="color:rgb(63, 63, 63);">两种方式。  
</font><font style="color:rgb(63, 63, 63);">• </font>**<font style="color:rgb(250, 81, 81);">检索器引导生成器训练</font>**<font style="color:rgb(63, 63, 63);">：利用高质量检索文档指导生成器的训练，例如RETRO和RALMs等模型通过预训练的检索器（如BERT和COLBERTV2）提升生成器的输出质量。  
</font><font style="color:rgb(63, 63, 63);">• </font>**<font style="color:rgb(250, 81, 81);">生成器引导检索器训练</font>**<font style="color:rgb(63, 63, 63);">：根据生成器的性能优化检索器，例如DKRR和AAR等模型利用生成器的注意力分数或生成信号指导检索器的训练，确保检索内容与生成需求一致。</font>

:::color5
**<font style="color:#601BDE;">3.协同训练</font>**

:::

**<font style="color:#74B602;">协同训练同时优化检索器和生成器</font>**<font style="color:rgb(63, 63, 63);">，通过联合训练实现整体系统性能的提升。这种方法确保两个组件的改进相互促进，例如RAG和MIPS等模型通过协同训练优化检索过程，使检索器能够根据生成器的反馈逐步提升检索效果，同时生成器也能更好地利用检索信息。</font>



### 多模态RAG
:::color3
**简介****：**<font style="color:rgb(63, 63, 63);">多模态RAG扩展了传统文本RAG系统，通过</font>**<font style="color:#ED740C;">整合图像、音频、视频等多种模态信息</font>**<font style="color:rgb(63, 63, 63);">，丰富了系统的输出能力。然而，多模态RAG面临两大挑战：一是如何有效表示和检索跨模态知识，二是如何理解和利用多模态信息生成合适的响应。</font>

:::

**多模态RAG详见：**[多模态RAG](https://www.yuque.com/zhongxian-iiot9/gi3w2u/nhf9wnw87va9udcz)

:::color5
**<font style="color:#601BDE;">1.多模态表征与检索</font>**

:::

<font style="color:rgb(63, 63, 63);">多模态RAG的基础在于将不同模态的数据转换为统一的向量表示，并实现跨模态的高效检索。例如，CLIP通过学习图像和文本的对齐表示，实现了跨模态检索；Wav2Vec 2.0和ViViT则分别处理音频和视频内容，提取丰富的特征表示。</font>

:::color5
**<font style="color:#601BDE;">2.多模态理解与生成</font>**

:::

<font style="color:rgb(63, 63, 63);">多模态RAG系统需要进一步理解跨模态关系并生成连贯的输出。例如，MuRAG和RA-CM3通过检索和生成多模态内容（如图像和文本）提升问答系统的能力；Transfusion和Show-o等模型则结合语言建模和扩散模型，支持广泛的视觉-语言任务。</font>



### 记忆RAG
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">记忆RAG通过引入显式记忆机制，弥补了传统RAG系统中隐式记忆和实时检索之间的空白。这种机制在处理长文档理解、个性化知识管理等场景中表现出色。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742367374261-7dff24c1-6ba3-4c02-9b97-6c416e851285.png)

:::color5
**<font style="color:#601BDE;">1.记忆类型</font>**

:::

<font style="color:rgb(63, 63, 63);">• </font>**<font style="color:rgb(250, 81, 81);">隐式记忆</font>**<font style="color:rgb(63, 63, 63);">：存储在模型参数中的知识，例如预训练的检索器和生成器权重，提供快速推理但难以更新。  
</font><font style="color:rgb(63, 63, 63);">• </font>**<font style="color:rgb(250, 81, 81);">显式记忆</font>**<font style="color:rgb(63, 63, 63);">：压缩的、结构化的长期知识表示，例如对整本书或用户行为模式的理解，比隐式记忆更灵活且易于更新。  
</font><font style="color:rgb(63, 63, 63);">• </font>**<font style="color:rgb(250, 81, 81);">工作记忆</font>**<font style="color:rgb(63, 63, 63);">：临时存储的检索文本块，用于当前任务的生成，类似于人类的短期记忆。</font>

:::color5
**<font style="color:#601BDE;">2.技术实现</font>**

:::

<font style="color:rgb(63, 63, 63);">记忆RAG通过</font>**<font style="color:#74B602;">稀疏键值缓存实现显式记忆</font>**<font style="color:rgb(63, 63, 63);">，例如Memory3通过两阶段预训练将原始输入转换为显式记忆；MemoRAG采用轻量级LLM作为全局记忆系统，提升长文本处理能力；CAG则通过预计算键值缓存完全消除实时检索需求，提高系统效率。</font>



### Agentic RAG
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">Agentic RAG将</font>**<font style="color:#ED740C;">Agent与RAG技术结合</font>**<font style="color:rgb(63, 63, 63);">，通过</font>**<font style="color:#ED740C;">动态管理检索策略和优化推理过程</font>**<font style="color:rgb(63, 63, 63);">，显著提升了系统的性能。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742367459808-ff02582c-280d-4dd9-b303-d4ddc54536d0.png)

:::color5
**<font style="color:#601BDE;">1.query理解与策略规划(planning)</font>**

:::

<font style="color:rgb(63, 63, 63);">智能体通过</font>**<font style="color:#74B602;">分析query复杂性和主题，制定合适的检索策略</font>**<font style="color:rgb(63, 63, 63);">。例如，AT-RAG通过主题过滤和迭代推理提升多跳查询的检索效率；REAPER则通过基于推理的检索规划优化复杂查询的处理。</font>

:::color5
**<font style="color:#601BDE;">2.工具调用</font>**

:::

<font style="color:rgb(63, 63, 63);">Agentic RAG能够利用多种</font>**<font style="color:#74B602;">外部工具（如搜索引擎、计算器和API）增强检索和推理能力</font>**<font style="color:rgb(63, 63, 63);">。例如，AT-RAG和RAGENTIC通过多代理协作和工具集成，灵活应对不同任务需求。</font>

:::color5
**<font style="color:#601BDE;">3.Reasoning & 决策优化</font>**

:::

<font style="color:rgb(63, 63, 63);">智能体通过</font>**<font style="color:#74B602;">多步推理和决策优化</font>**<font style="color:rgb(63, 63, 63);">，评估信息源可靠性并优化检索策略。例如，PlanRAG通过“先计划后检索”的方法提升生成模型的决策能力；REAPER则通过推理增强检索规划，提高系统响应速度。</font>



# RAG & Agent对比<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">建议从RAG方案起步保障基础质量，在积累足够交互数据后逐步引入Agent能力。混合架构需注意控制复杂度，可通过模块化设计保持系统可维护性。</font>

:::

**<font style="color:rgb(51, 51, 51);">演进路线建议</font>**

1. **<font style="color:rgb(51, 51, 51);">初期阶段</font>**<font style="color:rgb(51, 51, 51);">：优先实施RAG方案，快速搭建基线系统（2-3周）</font>
2. **<font style="color:rgb(51, 51, 51);">中期迭代</font>**<font style="color:rgb(51, 51, 51);">：引入Agent处理非结构化分析（4-6周开发周期）</font>
3. **<font style="color:rgb(51, 51, 51);">长期演进</font>**<font style="color:rgb(51, 51, 51);">：构建具有记忆能力的领域智能体，需配套：</font>
    - <font style="color:rgb(51, 51, 51);">用户反馈闭环系统</font>
    - <font style="color:rgb(51, 51, 51);">自动化评估流水线</font>
    - <font style="color:rgb(51, 51, 51);">安全护栏机制</font>

:::color5
**<font style="color:#601BDE;">1.技术原理对比</font>**

:::

| **维度** | **RAG** | **Agent** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">技术核心</font> | **<font style="color:#ED740C;">检索+生成</font>**<font style="color:rgb(51, 51, 51);">双阶段架构</font> | **<font style="color:#ED740C;">自主决策+任务分解能力</font>** |
| <font style="color:rgb(51, 51, 51);">知识更新</font> | <font style="color:rgb(51, 51, 51);">依赖外部知识库更新</font> | <font style="color:rgb(51, 51, 51);">通过交互自主进化</font> |
| <font style="color:rgb(51, 51, 51);">推理机制</font> | <font style="color:rgb(51, 51, 51);">基于检索结果的上下文生成</font> | <font style="color:rgb(51, 51, 51);">多步推理的决策链</font> |
| <font style="color:rgb(51, 51, 51);">典型架构</font> | <font style="color:rgb(51, 51, 51);">DPR + Seq2Seq</font> | <font style="color:rgb(51, 51, 51);">LLM + 记忆模块+工具调用</font> |


:::color5
**<font style="color:#601BDE;">2.项目应用对比</font>**

:::

| **对比项** | **RAG方案** | **Agent方案** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据准备</font>** | <font style="color:rgb(51, 51, 51);">需要</font>**<font style="color:#ED740C;">构建结构化行业知识库</font>**<font style="color:rgb(51, 51, 51);">   </font><font style="color:rgb(51, 51, 51);">（需清洗10万+商品数据）</font> | <font style="color:rgb(51, 51, 51);">只需定义</font>**<font style="color:#ED740C;">工具集</font>**<font style="color:rgb(51, 51, 51);">   </font><font style="color:rgb(51, 51, 51);">（API/数据库连接器）</font> |
| **<font style="color:rgb(51, 51, 51);">生成质量</font>** | <font style="color:rgb(51, 51, 51);">输出稳定但创新性有限   </font><font style="color:rgb(51, 51, 51);">（准确率92%但建议重复率15%）</font> | <font style="color:rgb(51, 51, 51);">具有创造性但需验证   </font><font style="color:rgb(51, 51, 51);">（生成新颖建议但需人工审核30%）</font> |
| **<font style="color:rgb(51, 51, 51);">响应速度</font>** | <font style="color:rgb(51, 51, 51);">单次检索生成耗时1.2-1.5秒</font> | <font style="color:rgb(51, 51, 51);">多步决策平均耗时3-5秒</font> |
| **<font style="color:rgb(51, 51, 51);">可解释性</font>** | <font style="color:rgb(51, 51, 51);">可追溯引用来源（支持溯源标注）</font> | <font style="color:rgb(51, 51, 51);">决策过程黑箱化（需额外开发解释模块）</font> |
| **<font style="color:rgb(51, 51, 51);">维护成本</font>** | <font style="color:rgb(51, 51, 51);">周期性知识库更新</font> | <font style="color:rgb(51, 51, 51);">实时自主优化（需监控机制）</font> |


:::color5
**<font style="color:#601BDE;">3.RAG+Agent混合架构实践</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">分层处理架构</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
class HybridSystem:
    def __init__(self):
        self.rag = RAGEngine("industry_kb")  # 加载行业知识库
        self.agent = BizAgent(tools=[DB_Connector, MarketAPI])  # 初始化工具集

    def generate_report(self, query):
        # 第一阶段：RAG生成基础内容
        base_content = self.rag.retrieve_generate(query)

        # 第二阶段：Agent增强分析
        enhancement = self.agent.execute(
            f"对以下内容进行深度分析：{base_content}"
        )

        # 第三阶段：结果融合
        return self._merge_output(base_content, enhancement)
```

2. **<font style="color:rgb(51, 51, 51);">性能优化方案</font>**<font style="color:rgb(51, 51, 51);">：</font>
+ **<font style="color:rgb(51, 51, 51);">缓存机制</font>**<font style="color:rgb(51, 51, 51);">：对高频查询建立LRU缓存（命中率可达65%）</font>
+ **<font style="color:rgb(51, 51, 51);">异步处理</font>**<font style="color:rgb(51, 51, 51);">：将检索与生成阶段解耦（吞吐量提升40%）</font>
+ **<font style="color:rgb(51, 51, 51);">动态路由</font>**<font style="color:rgb(51, 51, 51);">：根据query复杂度选择处理路径（CPU利用率下降25%）</font>
3. **<font style="color:rgb(51, 51, 51);">评估指标</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">| </font>**<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);"> | RAG单独 | Agent单独 | 混合系统 |  
</font><font style="color:rgb(51, 51, 51);">|------------------|---------|-----------|----------|  
</font><font style="color:rgb(51, 51, 51);">| 事实准确性 | 92% | 83% | 95% |  
</font><font style="color:rgb(51, 51, 51);">| 建议创新性 | 2.8/5 | 4.1/5 | 3.9/5 |  
</font><font style="color:rgb(51, 51, 51);">| 响应延迟(ms) | 1200 | 3500 | 1800 |  
</font><font style="color:rgb(51, 51, 51);">| 开发复杂度 | 中等 | 高 | 高 |</font>

# Agentic RAG
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">Agentic RAG</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">一种基于AI Agent的方法，借助Agent的任务规划与工具能力，来协调完成对多文档的、多类型的问答需求。</font>**<font style="color:#ED740C;">既能提供RAG的基础查询能力，也能提供基于RAG之上更多样与复杂任务能力</font>**<font style="color:rgb(25, 27, 31);">。概念架构如下：</font>

:::

**背景**：<font style="color:rgb(25, 27, 31);">Agentic RAG这类系统通过集成自主代理，利用反射、规划、工具使用和多代理协作等核心代理模式，尝试克服</font>**<font style="color:rgb(25, 27, 31);">传统的RAG系统在知识检索和生成方面表现良好，但在处理动态、多步骤推理任务、适应性和复杂工作流编排方面存在不足</font>**<font style="color:rgb(25, 27, 31);">这些限制。</font>

**<font style="color:rgb(25, 27, 31);">核心思想</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">Agent模式与RAG结合的逻辑模式</font>**<font style="color:rgb(25, 27, 31);">。传统RAG最适合需要基本检索和生成功能的简单任务。Agentic RAG在多智能体协作推理方面表现出色，适合更复杂的多领域任务。</font>

:::color5
**<font style="color:#601BDE;">1.相比RAG的优点</font>**

:::

+ **基于RAG之上的Tool Agent将不再局限于简单的回答事实性的问题，通过扩展更多的后端RAG引擎，可以完成更多的知识型任务**。比如：整理、摘要生成、数据分析、甚至借助API访问外部系统等
+ **Top Agent管理与协调下的多个Tool Agent可以通过协作完成联合型的任务。**比如对两个不同文档中的知识做对比与汇总，这也是经典问答型的RAG无法完成的任务类型。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741605574176-f8cfb56b-1078-4209-b625-cdd0974c9893.png)

## Agentic RAG示例（企业知识库查询）
:::color5
**<font style="color:#601BDE;">1.场景介绍</font>**

:::

企业中有大量不同来源与类型的文档（在实际中并不一定代表“文件”，也可以是某种非文件形态的信息，比如存放在RDBMS中的数据），现在需要在这些文档之上构建一个依赖于它们的、知识密集型的应用或工具。这些需求包括：

+ **基于全局的理解文档后回答问题。比如：对某知识内容进行总结摘要？**
+ **跨文档与知识库的回答问题。比如：比较不同文档内容的区别？**
+ **结合非知识工具的复合场景。比如：从文档提取产品介绍发送给xx客户？**

:::color5
**<font style="color:#601BDE;">2.实现思路分析</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">RAG方式</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">这种复杂需求的场景如果使用经典RAG架构，通过chunks+向量+top_K检索来获得并插入上下文，直接让LLM来给出答案，显然是不现实的。</font>**<font style="color:rgb(25, 27, 31);">经典RAG在回答文档相关的事实性问题时可以工作的不错，但是实际的知识应用并不总是这种类型！</font>**
+ **<font style="color:rgb(25, 27, 31);">Agentic RAG方案</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">一种基于AI Agent的方法，借助Agent的任务规划与工具能力，来协调完成对多文档的、多类型的问答需求。</font>**<font style="color:rgb(25, 27, 31);">既能提供RAG的基础查询能力，也能提供基于RAG之上更多样与复杂任务能力。</font>

:::color5
**<font style="color:#601BDE;">3.实现步骤</font>**

:::

1. **框架设计：**
+ **多种RAG引擎**：RAG应用（RAG引擎，即借助索引实现检索并合成响应）退化成一个Agent使用的知识工具。你可以针对一个文档/知识库构建多种不同的RAG引擎，**<font style="color:#ED740C;">比如使用向量索引来回答事实性问题；使用摘要索引来回答总结性问题；使用知识图谱索引来回答需要更多关联性的问题</font>**等
+ **ToolAgent：**在单个文档/知识库的多个RAG引擎之上设置一个**ToolAgent**，**<font style="color:#74B602;">把RAG引擎作为该Agent的tools</font>**，并利用LLM的能力由**<font style="color:#74B602;">ToolAgent在自己“负责”的文档内使用这些tools来回答问题</font>**
+ **TopAgent：**设置一个总的**<font style="color:#74B602;">顶级代理TopAgent来管理所有的低阶ToolAgent</font>**，将ToolAgent看作自己的tools，仍然利用LLM来规划、协调、执行用户问题的回答方案
2. **准备测试文档**

首先这里准备三个RAG相关的测试PDF文档，其名称与路径分别保存。当然，在实际应用中，这里文档数量可以扩展到非常大（后面会看到针对大量文档的一个优化方法）：

```python
names = ['c-rag','self-rag','kg-rag']  
files = ['../../data/c-rag.pdf','../../data/self-rag.pdf','../../data/kg-rag.pdf']
```

3. **创建tool agent**

创建一个针对单个文档生成Tool Agent的函数，在这个函数中，将对一个文档创建两个索引与对应的RAG引擎：

+ 针对普通事实性问题的向量索引与RAG引擎
+ 针对更高层语义理解的总结类问题的摘要索引与RAG引擎

最后，我们把这两个引擎作为一个Agent可使用的两个tool，构建一个Tool Agent返回。

```python
......省略import部分与准备llm部分......  

#采用chroma向量数据库  
chroma = chromadb.HttpClient(host="localhost", port=8000)  
collection = chroma.get_or_create_collection(name="agentic_rag")   
vector_store = ChromaVectorStore(chroma_collection=collection)  

#创建针对某个文档的tool_agent  
def create_tool_agent(file,name):  

    #文档拆分  
    print(f'Starting to create tool agent for 【{name}】...\n')  
    docs =SimpleDirectoryReader(input_files = [file]).load_data()  
    splitter = SentenceSplitter(chunk_size=500,chunk_overlap=50)  
    nodes = splitter.get_nodes_from_documents(docs)  

    #创建向量索引，并做持久保存  
    if not os.path.exists(f"./storage/{name}"):  
        print('Creating vector index...\n')  
        storage_context = StorageContext.from_defaults(vector_store=vector_store)  
        vector_index = VectorStoreIndex(nodes,storage_context=storage_context)  
        vector_index.storage_context.persist(persist_dir=f"./storage/{name}")  
    else:  
        print('Loading vector index...\n')  
        storage_context = StorageContext.from_defaults(persist_dir=f"./storage/{name}",vector_store=vector_store)  
        vector_index = load_index_from_storage(storage_context=storage_context)  

    #创建基于向量的查询引擎  
    query_engine = vector_index.as_query_engine(similarity_top_k=5)  

    #创建摘要索引与对应的查询引擎  
    summary_index = SummaryIndex(nodes)  
    summary_engine = summary_index.as_query_engine(response_mode="tree_summarize")  

    #将RAG引擎转化为两个tool  
    query_tool = QueryEngineTool.from_defaults(query_engine=query_engine,name=f'query_tool',description=f'Use if you want to query details about {name}')  
    summary_tool = QueryEngineTool.from_defaults(query_engine=summary_engine,name=f'summary_tool',description=f'Use ONLY IF you want to get a holistic summary of the documents. DO NOT USE if you want to query some details about {name}.')  

    #创建一个tool agent  
    tool_agent = **ReActAgent**.from_tools(**[query_tool,summary_tool]**,verbose=True,  
                                           system_prompt=f"""  
                                                          You are a specialized agent designed to answer queries about {name}.You must ALWAYS use at least one of the tools provided when answering a question; DO NOT rely on prior knowledge. DO NOT fabricate answer.  
                                                            """)  
    return tool_agent
```

4. **创建top agent**

最后，我们需要创建一个顶层的Top Agent，这个Agent的作用是接收客户的请求问题，然后规划这个问题的查询计划，并使用工具来完成，而这里的工具就是上面创建好的多个Tool Agent：

```python
#首先将Tool Agent进行“工具化”  
print('===============================================\n')  
print('Creating tools from tool agents...\n')  
all_tools = []  

for name in names:  
    agent_tool = QueryEngineTool.from_defaults(  
        #注意，Agent本身也是一种Query Engine，所以直接转为tool  
        query_engine=tool_agents_dict[name],  

        #这个工具的名字  
        name=f"tool_{name.replace("-", "")}",  

        #描述这个工具的作用和使用方法  
        description=f"Use this tool if you want to answer any questions about {name}."  
    )  

    all_tools.append(agent_tool)  

#创建Top Agent  
print('Creating top agent...\n')  
top_agent = **OpenAIAgent.**from_tools(**tools=all_tools**,verbose=True,system_prompt="""You are an agent designed to answer queries over a set of given papers.Please always use the tools provided to answer a question.Do not rely on prior knowledge.DO NOT fabricate answer""" )
```

注意这里我们创建的Top Agent使用了**OpenAIAgent**，而不是ReActAgent，这也展示了这种架构的灵活性：**不同Agent可以按需使用不同的推理范式。**

****

# Memo RAG
[https://arxiv.org/pdf/2409.05591v1](https://arxiv.org/pdf/2409.05591v1)



# KG-RAG(知识图谱 RAG)
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(58, 58, 58);">图谱RAG通过引入图结构化数据来增强基础RAG的能力，其主要特点包括：</font>

+ <font style="color:rgb(58, 58, 58);">图结构化索引：利用图数据库存储和检索信息，通过图结构捕捉数据之间的复杂关系。</font>
+ <font style="color:rgb(58, 58, 58);">双级检索策略：结合低层次的具体信息检索和高层次的广泛话题检索，提高检索的全面性和准确性。</font>
+ <font style="color:rgb(58, 58, 58);">动态更新：支持增量更新算法，能够快速适应新数据</font>

:::

**背景：**<font style="color:rgb(58, 58, 58);">大型语言模型（LLMs）已经展现出惊人的能力，但它们也面临着一些挑战，比如“幻觉”（生成虚假信息）、难以实时更新知识，以及推理过程不透明等。</font>

<font style="color:rgb(58, 58, 58);">为了解决这些问题，研究者们开始探索将知识图谱（KGs）融入检索增强生成（RAG）框架，形成了所谓的“KG-RAG”方法。这种结合不仅有望减少模型的“幻觉”，还能提升其推理能力和准确性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741691401025-7d0744e4-042a-4546-b4f8-c9cbb0d5e8ab.png)

:::color5
**<font style="color:#601BDE;">1.Query增量</font>**

:::

<font style="color:rgb(58, 58, 58);">检索前阶段的核心问题是“检索什么内容”。论文总结了三种query增强方法：</font>

+ **<font style="color:rgb(0, 0, 0);">查询扩展（Query Expansion）</font>**<font style="color:rgb(58, 58, 58);">：通过逐步推理提取关键实体，帮助模型在检索时找到更相关的内容。</font>
+ **<font style="color:rgb(0, 0, 0);">查询分解（Query Decomposition）</font>**<font style="color:rgb(58, 58, 58);">：将复杂的多跳问题分解为多个简单子问题，分别检索后再整合。</font>
+ **<font style="color:rgb(0, 0, 0);">查询理解（Query Understanding）</font>**<font style="color:rgb(58, 58, 58);">：提取查询的主要思想，确保检索内容与查询主题一致。</font>

:::color5
**<font style="color:#601BDE;">2.检索</font>**

:::

<font style="color:rgb(58, 58, 58);">检索阶段的核心问题是“如何组织检索到的知识”。检索到的知识可以以三种形式呈现：</font>

+ **<font style="color:rgb(0, 0, 0);">事实（Fact）</font>**<font style="color:rgb(58, 58, 58);">：最基本的知识单元，以三元组（主体、谓语、宾语）形式呈现。</font>
+ **<font style="color:rgb(0, 0, 0);">路径（Path）</font>**<font style="color:rgb(58, 58, 58);">：由多个相连的三元组组成，提供更丰富的上下文信息。</font>
+ **<font style="color:rgb(0, 0, 0);">子图（Subgraph）</font>**<font style="color:rgb(58, 58, 58);">：结合路径和邻近实体信息，提供更全面的关系和模式。</font>

:::color5
**<font style="color:#601BDE;">3.LLM生成</font>**

:::

<font style="color:rgb(58, 58, 58);">检索后阶段的核心问题是“如何引导模型利用检索到的知识”。论文总结了三种提示设计方法：</font>

+ **<font style="color:rgb(0, 0, 0);">链式思考（Chain-of-Thought, CoT）</font>**<font style="color:rgb(58, 58, 58);">：通过逐步推理将复杂问题分解为多个中间步骤。</font>
+ **<font style="color:rgb(0, 0, 0);">树状思考（Tree-of-Thought, ToT）</font>**<font style="color:rgb(58, 58, 58);">：允许模型同时探索和比较多条推理路径。</font>
+ **<font style="color:rgb(0, 0, 0);">思维导图（MindMap）</font>**<font style="color:rgb(58, 58, 58);">：引导模型构建结构化的思维导图，整合检索到的知识并保留推理痕迹。</font>

:::color5
**<font style="color:#601BDE;">4.评估指标</font>**

:::

+ **<font style="color:rgb(0, 0, 0);">评估指标</font>**<font style="color:rgb(58, 58, 58);">：使用了多种指标，如准确率（Correct）、错误率（Wrong）、失败率（Fail）、BERTScore、ROUGE Score等，以全面评估生成答案的质量。</font>



