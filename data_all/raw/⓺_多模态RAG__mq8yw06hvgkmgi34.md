# ⓺ 多模态RAG

<!-- source: yuque://zhongxian-iiot9/hlyypb/mq8yw06hvgkmgi34 -->

# <font style="color:rgb(51, 51, 51);">多模态 RAG（Retrieval-Augmented Generation）详解</font>
#### <font style="color:rgb(51, 51, 51);">一、核心原理</font>
<font style="color:rgb(51, 51, 51);">多模态 RAG 是传统 RAG 的扩展，通过整合文本、图像、音频、视频等多种模态数据，提升生成模型的准确性和丰富性。其核心思想是通过检索外部多模态知识库中的相关内容，辅助生成多模态输出。</font>

**<font style="color:rgb(51, 51, 51);">关键机制</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">多模态编码</font>**<font style="color:rgb(51, 51, 51);">：将不同模态数据映射到统一语义空间（如 CLIP 的图文对齐）。</font>
2. **<font style="color:rgb(51, 51, 51);">跨模态检索</font>**<font style="color:rgb(51, 51, 51);">：支持混合模态查询（如用文本搜索图像或视频片段）。</font>
3. **<font style="color:rgb(51, 51, 51);">多模态融合生成</font>**<font style="color:rgb(51, 51, 51);">：结合检索到的多种模态信息生成最终输出。</font>

#### <font style="color:rgb(51, 51, 51);">二、技术架构与计算步骤</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740569032402-486de69a-16f6-4a66-a754-5eb6b81bbf9b.png)

1. **数据预处理**
    - <font style="color:rgb(51, 51, 51);">文本：分词、去噪、实体识别</font>
    - <font style="color:rgb(51, 51, 51);">图像：ResNet/ViT 提取特征，CLIP 编码</font>
    - <font style="color:rgb(51, 51, 51);">音频：MFCC 特征提取，Whisper 语音转文本</font>
    - <font style="color:rgb(51, 51, 51);">视频：按帧采样，结合视觉和音频特征</font>
2. **多模态编码**
    - <font style="color:rgb(51, 51, 51);">文本编码器：</font>`<font style="color:rgb(51, 51, 51);">BERT-embeddings = BERT(text)[CLS]</font>`
    - <font style="color:rgb(51, 51, 51);">图像编码器：</font>`<font style="color:rgb(51, 51, 51);">CLIP_img = CLIP.encode_image(img)</font>`
    - <font style="color:rgb(51, 51, 51);">跨模态对齐损失：</font>`<font style="color:rgb(51, 51, 51);">L = contrastive_loss(text_emb, img_emb)</font>`
3. **索引构建**
    - <font style="color:rgb(51, 51, 51);">混合索引结构：</font>

```python
from faiss import IndexFlatIP
text_index = IndexFlatIP(768)
image_index = IndexFlatIP(512)
```

4. **混合检索**
    - <font style="color:rgb(51, 51, 51);">查询编码：</font>`<font style="color:rgb(51, 51, 51);">query_emb = modal_encoder(user_query)</font>`
    - <font style="color:rgb(51, 51, 51);">跨模态搜索：</font>

```python
def cross_modal_search(query, k=5):
    text_results = text_index.search(query, k)
    image_results = image_index.search(query, k)
    return rank_merge(text_results, image_results)
```

5. **信息融合**
    - <font style="color:rgb(51, 51, 51);">注意力融合机制：</font>

```python
attention_weights = softmax(Q * K.T / sqrt(d))
fused_emb = attention_weights @ V
```

6. **多模态生成**
    - <font style="color:rgb(51, 51, 51);">使用类似 Flamingo 模型：</font>

```python
outputs = model.generate(
    text_inputs=prompt, 
    image_inputs=retrieved_images
)
```

#### <font style="color:rgb(51, 51, 51);">三、优缺点分析</font>
**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">信息丰富性：可利用多源异构数据</font>
2. <font style="color:rgb(51, 51, 51);">准确率提升：视觉证据增强文本生成可信度</font>
3. <font style="color:rgb(51, 51, 51);">应用扩展：支持跨模态问答、多媒体内容创作</font>

**<font style="color:rgb(51, 51, 51);">挑战</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">计算复杂度：多模态编码索引内存消耗增加3-5倍</font>
2. <font style="color:rgb(51, 51, 51);">模态对齐：不同模态的语义间隙导致检索噪声</font>
3. <font style="color:rgb(51, 51, 51);">延迟问题：混合检索耗时比单模态高40-60%</font>

#### <font style="color:rgb(51, 51, 51);">四、典型应用场景</font>
1. **医疗诊断**：
    - <font style="color:rgb(51, 51, 51);">输入：CT影像 + 患者主诉文本</font>
    - <font style="color:rgb(51, 51, 51);">输出：诊断报告 + 可视化标注</font>
2. **教育科技**：
    - <font style="color:rgb(51, 51, 51);">输入："量子纠缠原理" + 白板手绘草图</font>
    - <font style="color:rgb(51, 51, 51);">输出：3D动画演示 + 分步讲解</font>
3. **电商推荐**：
    - <font style="color:rgb(51, 51, 51);">输入：产品视频 + 用户评论</font>
    - <font style="color:rgb(51, 51, 51);">输出：个性化推荐理由 + 产品对比图</font>

#### <font style="color:rgb(51, 51, 51);">五、改进方向</font>
1. **层级式检索**：

```python
def hierarchical_retrieval(query):
    coarse_results = clip_retriever(query, k=100)
    fine_results = rerank(coarse_results, cross_encoder)
    return fine_results[:5]
```

2. **动态模态加权**：

```python
modal_weights = learnable_layer(query_context)
fused_emb = sum(w_i * emb_i for w_i, emb_i in zip(weights, modalities))
```

3. **增量索引更新**：

```python
class StreamingIndex:
    def update(self, new_data):
        self.index.add(encode(new_data))
        self.index = rebalance(self.index)
```

#### <font style="color:rgb(51, 51, 51);">六、代码实现示例（PyTorch）</font>
```python
import torch
from transformers import FlamingoProcessor, FlamingoForConditionalGeneration
from clip import CLIP

# 初始化模型
clip = CLIP(...)
flamingo = FlamingoForConditionalGeneration.from_pretrained(...)

# 多模态检索
def retrieve(query, k=3):
    if isinstance(query, str):
        emb = clip.text_encoder(query)
    else:  # 图像查询
        emb = clip.image_encoder(query)
    return faiss_index.search(emb, k)

# 生成流程
def multimodal_rag(query):
    retrieved = retrieve(query)
    prompt = build_prompt(query, retrieved)

    inputs = processor(
        text=prompt,
        images=[item for item in retrieved if item.is_image],
        return_tensors="pt"
    )

    outputs = flamingo.generate(
        input_ids=inputs.input_ids,
        pixel_values=inputs.pixel_values
    )
    return processor.decode(outputs[0])
```

#### <font style="color:rgb(51, 51, 51);">七、性能优化建议</font>
1. **量化索引**：

```python
from faiss import IndexPQ
quantizer = IndexPQ(d=768, M=12, nbits=8)
```

2. **缓存策略**：

```python
from functools import lru_cache
@lru_cache(maxsize=1000)
def cached_encode(data):
    return encoder(data)
```

3. **异步流水线**：

```python
import asyncio
async def async_retrieve(query):
    # 并行执行多模态检索
    text_task = asyncio.create_task(text_retriever(query))
    image_task = asyncio.create_task(image_retriever(query))
    return await asyncio.gather(text_task, image_task)
```

#### <font style="color:rgb(51, 51, 51);">八、评估指标</font>
1. <font style="color:rgb(51, 51, 51);">跨模态检索准确率（mAP@K）</font>
2. <font style="color:rgb(51, 51, 51);">生成结果相关性（BLEU-4 / CLIPScore）</font>
3. <font style="color:rgb(51, 51, 51);">多模态一致性：</font><font style="color:rgb(51, 51, 51);">C</font><font style="color:rgb(51, 51, 51);">o</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">s</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">s</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">c</font><font style="color:rgb(51, 51, 51);">y</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">N</font><font style="color:rgb(51, 51, 51);">∑</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">N</font><font style="color:rgb(51, 51, 51);">CLIP</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">G</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">R</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">C</font>__<font style="color:rgb(51, 51, 51);">o</font>__<font style="color:rgb(51, 51, 51);">n</font>__<font style="color:rgb(51, 51, 51);">s</font>__<font style="color:rgb(51, 51, 51);">i</font>__<font style="color:rgb(51, 51, 51);">s</font>__<font style="color:rgb(51, 51, 51);">t</font>__<font style="color:rgb(51, 51, 51);">e</font>__<font style="color:rgb(51, 51, 51);">n</font>__<font style="color:rgb(51, 51, 51);">cy</font>_<font style="color:rgb(51, 51, 51);">=</font>_<font style="color:rgb(51, 51, 51);">N</font>_<font style="color:rgb(51, 51, 51);">1</font>_<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">∑</font>_<font style="color:rgb(51, 51, 51);">N</font>_<font style="color:rgb(51, 51, 51);">CLIP</font><font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">G</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">R</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">)</font>
4. <font style="color:rgb(51, 51, 51);">端到端延迟：QPS（Queries Per Second）</font>

#### <font style="color:rgb(51, 51, 51);">九、未来研究方向</font>
1. **<font style="color:rgb(51, 51, 51);">神经符号结合</font>**<font style="color:rgb(51, 51, 51);">：将知识图谱与神经网络检索结合</font>
2. **<font style="color:rgb(51, 51, 51);">因果推断</font>**<font style="color:rgb(51, 51, 51);">：提升生成结果的因果逻辑性</font>
3. **<font style="color:rgb(51, 51, 51);">具身智能</font>**<font style="color:rgb(51, 51, 51);">：结合机器人传感数据的多模态RAG</font>

<font style="color:rgb(51, 51, 51);">该技术栈正在快速发展，建议持续关注以下领域进展：</font>

+ <font style="color:rgb(51, 51, 51);">更高效的跨模态对齐方法（如对比学习新范式）</font>
+ <font style="color:rgb(51, 51, 51);">新型多模态索引结构（如HNSW的跨模态扩展）</font>
+ <font style="color:rgb(51, 51, 51);">生成模型的3D/视频理解能力提升</font>

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">多模态RAG综述</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：《</font><font style="color:rgb(51, 51, 51);">Ask in Any Modality: A Comprehensive Survey on Multimodal Retrieval-Augmented Generation</font><font style="color:rgb(51, 51, 51);">》</font>

**<font style="color:rgb(25, 27, 31);">多模态RAG步骤：查询预处理、多模态数据库、检索策略（模态为中心）、融合机制、增强技术、生成阶段、训练策略。</font>**

**<font style="color:rgb(25, 27, 31);">paper:</font>**[**https://arxiv.org/pdf/2502.08826v2**](https://arxiv.org/pdf/2502.08826v2)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741513034394-ff620807-3e5a-424b-9d17-d08e40416d86.png)

```python
解释这幅画的历史含义，为这幅画生成一段现代诠释。
```

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ <font style="color:rgb(25, 27, 31);">提出了一个多模态RAG系统的通用框架；</font>
+ <font style="color:rgb(25, 27, 31);">并对多模态RAG系统进行了系统且全面的分析，涵盖了数据集、评估指标、基准测试、评估方法以及检索、融合、增强和生成方面的创新</font>

:::color5
**<font style="color:#601BDE;">2.检索策略</font>**

:::

<font style="color:rgb(25, 27, 31);">检索策略是多模态RAG系统的核心部分，主要通过高效搜索和相似性检索来提升信息检索的准确性和效率。具体方法包括：</font>

+ **<font style="color:rgb(25, 27, 31);">高效搜索和相似性检索</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">最大内积搜索</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=%E6%9C%80%E5%A4%A7%E5%86%85%E7%A7%AF%E6%90%9C%E7%B4%A2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（MIPS）及其变体，如</font>[<font style="color:rgb(9, 64, 142);">TPU-KNN</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=TPU-KNN&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">Scalable Nearest Neighbors</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=Scalable+Nearest+Neighbors&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（ScaNN）等，通过近似最近邻搜索提高检索速度。</font>
+ **<font style="color:rgb(25, 27, 31);">模态中心检索</font>**<font style="color:rgb(25, 27, 31);">：根据模态特性优化检索效率，包括文本中心（如</font>[<font style="color:rgb(9, 64, 142);">BM25</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=BM25&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">MiniLM</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=MiniLM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）、视觉中心（如</font>[<font style="color:rgb(9, 64, 142);">EchoSight</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=EchoSight&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">ImgRet</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=ImgRet&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）和视频中心（如iRAG、VideoRAG）的检索方法。</font>
+ **<font style="color:rgb(25, 27, 31);">重排序和选择策略</font>**<font style="color:rgb(25, 27, 31);">：通过优化示例选择、改进相关性评分和应用过滤机制来提高检索质量。例如，使用BERTScore、SSIM等多模态相似性度量进行重排序，以及通过硬负样本挖掘和共识过滤方法去除低质量数据。</font>

:::color5
**<font style="color:#601BDE;">3.融合机制</font>**

:::

<font style="color:rgb(25, 27, 31);">融合机制的目标是将来自不同模态的数据整合到统一的表示中，以支持跨模态推理。主要方法包括：</font>

+ **<font style="color:rgb(25, 27, 31);">分数融合与对齐</font>**<font style="color:rgb(25, 27, 31);">：通过将不同模态的数据转换为统一格式（如文本）或嵌入到共享语义空间中，实现模态间的对齐。例如，使用CLIP Score或</font>[<font style="color:rgb(9, 64, 142);">BLIP特征融合</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=BLIP%E7%89%B9%E5%BE%81%E8%9E%8D%E5%90%88&zhida_source=entity)<font style="color:rgb(25, 27, 31);">来衡量图像和文本的相关性。</font>
+ **<font style="color:rgb(25, 27, 31);">基于注意力的机制</font>**<font style="color:rgb(25, 27, 31);">：动态加权跨模态交互，支持特定任务的推理。例如，双流共注意力机制（如</font>[<font style="color:rgb(9, 64, 142);">RAMM</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=RAMM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）和基于用户注意力的特征融合（如RAGTrans）。</font>
+ **<font style="color:rgb(25, 27, 31);">统一框架和投影</font>**<font style="color:rgb(25, 27, 31);">：将多模态输入整合为连贯的表示。例如，通过层次化交叉链和晚期融合处理医疗数据（如</font>[<font style="color:rgb(9, 64, 142);">IRAMIG</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=IRAMIG&zhida_source=entity)<font style="color:rgb(25, 27, 31);">），或通过将图像转换为文本描述以简化多模态输入（如SAM-RAG）。</font>

:::color5
**<font style="color:#601BDE;">4.增强技术</font>**

:::

<font style="color:rgb(25, 27, 31);">增强技术通过优化检索到的文档，提升多模态RAG系统的性能。主要方法包括：</font>

+ **<font style="color:rgb(25, 27, 31);">上下文丰富化</font>**<font style="color:rgb(25, 27, 31);">：通过添加额外的上下文元素（如文本片段、图像标记或结构化数据）来增强检索到的知识，使其更适合生成任务。例如，通过</font>**<font style="color:#74B602;">实体检索和查询重构来优化视觉问答</font>**<font style="color:rgb(25, 27, 31);">（如MiRAG）。</font>
+ **<font style="color:rgb(25, 27, 31);">自适应和迭代检索</font>**<font style="color:rgb(25, 27, 31);">：根据查询的复杂性动态调整检索过程。例如，通过</font>**<font style="color:#74B602;">多轮检索策略逐步细化检索结果</font>**<font style="color:rgb(25, 27, 31);">（如</font>[<font style="color:rgb(9, 64, 142);">OMG-QA</font>](https://zhida.zhihu.com/search?content_id=254206651&content_type=Article&match_order=1&q=OMG-QA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">），或通过反馈机制优化检索内容（如IRAMIG）。</font>

:::color5
**<font style="color:#601BDE;">5.生成方法</font>**

:::

<font style="color:rgb(25, 27, 31);">生成方法关注于提升多模态RAG系统的输出质量和连贯性。主要创新包括：</font>

+ **<font style="color:rgb(25, 27, 31);">上下文学习（In-Context Learning）</font>**<font style="color:rgb(25, 27, 31);">：利用检索到的内容作为少样本示例，增强模型的推理能力。例如，通过检索相关驾驶经验来优化生成（如RAG-Driver）。</font>
+ **<font style="color:rgb(25, 27, 31);">推理（Reasoning）</font>**<font style="color:rgb(25, 27, 31);">：通过分解复杂推理任务为多个小步骤（如链式推理），提升生成内容的逻辑性和准确性。例如，通过多跳推理和证据整合来支持复杂问答（如RAGAR）。</font>
+ **<font style="color:rgb(25, 27, 31);">指令调整（Instruction Tuning）</font>**<font style="color:rgb(25, 27, 31);">：针对特定任务调整生成模块，提升模型对指令的理解和执行能力。例如，通过指令调整优化医学图像报告生成（如FactMM-RAG）。</font>
+ **<font style="color:rgb(25, 27, 31);">来源归因（Source Attribution）</font>**<font style="color:rgb(25, 27, 31);">：确保生成内容能够追溯到具体的来源，提升系统的透明度和可信度。例如，通过高亮显示支持证据的图像区域来归因（如VISA）。</font>

:::color5
**<font style="color:#601BDE;">6.训练策略</font>**

:::

<font style="color:rgb(25, 27, 31);">训练策略旨在优化多模态RAG系统的训练过程，提升模型的泛化能力和鲁棒性。主要方法包括：</font>

+ **<font style="color:rgb(25, 27, 31);">对齐（Alignment）</font>**<font style="color:rgb(25, 27, 31);">：通过对比学习（如InfoNCE损失）优化多模态表示的对齐，确保正样本更接近、负样本更远离。</font>
+ **<font style="color:rgb(25, 27, 31);">生成（Generation）</font>**<font style="color:rgb(25, 27, 31);">：使用交叉熵损失训练自回归语言模型，或通过生成对抗网络（GAN）和扩散模型优化图像生成。</font>
+ **<font style="color:rgb(25, 27, 31);">鲁棒性增强（Robustness）</font>**<font style="color:rgb(25, 27, 31);">：通过注入噪声、使用硬负样本或知识蒸馏等方法，提升模型对噪声和错误数据的鲁棒性。例如，通过Query Dropout增强生成器性能（如RA-CM3）。</font>

:::color5
**<font style="color:#601BDE;">7.benchmark评估</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741513558683-70523805-76e5-4ca2-80e3-04ba92787817.png)

:::color5
**<font style="color:#601BDE;">8.数据集</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741513507727-877262e6-9921-4b4e-a958-dcc271bdd137.png)



# 多模态RAG paper
## <font style="color:rgba(0, 0, 0, 0.9);">OmniSearch</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：OmniSearch 是阿里巴巴通义实验室推出的一款</font>**<font style="color:#ED740C;">多模态检索增强生成框架</font>**<font style="color:rgb(51, 51, 51);">，具备自适应规划能力。OmniSearch 能够动态拆解复杂问题，根据检索结果和问题情境调整检索策略，模拟人类在解决复杂问题时的行为方式，从而提升检索效率和准确性。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">paper</font>**<font style="color:rgba(0, 0, 0, 0.9);">:</font>[https://arxiv.org/pdf/2411.02937](https://arxiv.org/pdf/2411.02937)

:::

**<font style="color:rgba(0, 0, 0, 0.9);">背景</font>**<font style="color:rgba(0, 0, 0, 0.9);">：当面对动态复杂的问题时，传统多模态检索增强生成（RAG）技术往往表现出不足，比如无法适应实时变化的答案，或因检索方式僵化导致结果不够精准。多模态RAG通过结合文本、图像等多种数据形式，为AI赋予了更强的知识获取能力。然而，现有系统仍面临两个主要问题：</font>

1. **<font style="color:rgba(0, 0, 0, 0.9);">非适应性检索问题</font>**<font style="color:rgba(0, 0, 0, 0.9);">：传统RAG模型使用固定的检索流程，无法</font>**<font style="color:#ED740C;">根据上下文或中间结果动态调整</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">检索负担过载</font>**<font style="color:rgba(0, 0, 0, 0.9);">：单一检索查询常常包含多个模糊的检索需求，导致结果信息冗杂，关键内容反而被掩盖。</font>

:::color5
**<font style="color:#601BDE;">0.整体框架</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741514538519-f2c76891-2f38-4b82-9c3d-99bb8fec86b9.png)

:::success
**Planning Agent**

1. **Action**
    1. Self-thought
    2. 子问题
    3. 召回 API
    4. API Query
2. **更新反馈**
    1. 总结召回内容
    2. 子问题反馈

:::

:::success
**Versatile Retriever**

**多模态召回**

1. 网络搜索
2. 扩模态检索：文搜图
3. 图搜图

:::



:::success
**Sub-Question Solver**

**子问题解决器**

1. LLMs
2. MLLMs

:::

**Planning Agent**（**<font style="color:rgba(0, 0, 0, 0.9);">动态规划Agent</font>**）

每个计划的Action包括四个关键部分：自我思考<ST>、子问题<SQ>、检索API<R>、API查询<Q>。

    1. 在每一步中，**Planning Agent**都理解在自我思考中给出问题和现实世界的反馈，然后仔细确定后续行动要解决的**<font style="color:#ED740C;">子问题</font>**。
    2. 子问题所需的知识类型，**<font style="color:#ED740C;">调用不同的检索API。</font>**
    3. **<font style="color:#ED740C;">以类似于人类认知过程的方式</font>**，在问题解决过程中，**Planning Agent**自主生成各种潜在动作，包括：**<font style="color:#ED740C;">提出额外的问题</font>**以澄清检索内容中的模糊或冲突部分；细化检索query以获取更多的补充知识；修改措辞子问题；验证对当前子问题的回答；提出下一个子问题；
    4. **<font style="color:#74B602;">总结最终答案</font>**。

**Sub-question Solver （子问题求解器）**

总结检索到的内容，并相应地解决子问题，然后将求解器生成的反馈提供给**Planning Agent**。根据计算资源的不同，可以采用**<font style="color:#74B602;">更大或更小尺寸的MLLM</font>**。

:::color5
**<font style="color:#601BDE;">1.基于OmniSearch的VQA示例</font>**

:::

user query：图中的车价格是多少？

```python
<思考> 为了给这个车定价，首先需要确定车的模型和造价
<检索> 图搜图
<子问题> 车的模型和造价是什么？
```

```python
<思考> 根据检索结果，我们知道这个车是小米su7，我们需要知道小米su7的价格
<检索> 文本召回，小米su7的价格
<子问题> 小米su7的价格是多少？
```

```python
<思考> 根据检索结果，小米su7有不同的款型，不同款型价格不同。标准版215000，pro 245990，max 299900
<回答> 图中车是小米su7，不同款型价格不同。标准版215000，pro 245990，max 299900。
```

:::color5
**<font style="color:#601BDE;">0.创新点</font>**

:::

1. **<font style="color:rgba(0, 0, 0, 0.9);">Dyn-VQA 数据集：真实场景的复杂模拟</font>**
2. **<font style="color:rgba(0, 0, 0, 0.9);">动态规划能力</font>**
    1. **<font style="color:rgba(0, 0, 0, 0.9);">动态规划能力</font>**<font style="color:rgba(0, 0, 0, 0.9);">：OmniSearch 能够将复杂问题分解为子问题，并根据中间检索结果实时调整检索策略。例如，在回答汽车价格问题时，模型会先通过图像检索确定汽车品牌，然后针对品牌信息进一步检索具体价格数据。</font>
    2. **<font style="color:rgba(0, 0, 0, 0.9);">多工具灵活调用</font>**<font style="color:rgba(0, 0, 0, 0.9);">：OmniSearch 集成了文本检索、图像检索等多种工具，并能够根据问题需求选择最优的检索方式。例如，对于涉及视觉信息的问题，模型优先调用图像检索模块，而针对文本信息则使用语言模型进行解答。</font>
    3. **<font style="color:rgba(0, 0, 0, 0.9);">模块化设计</font>**<font style="color:rgba(0, 0, 0, 0.9);">：OmniSearch 的模块化结构支持灵活扩展和跨领域应用。例如，它可以结合任意多模态模型（如 GPT-4V、Qwen-VL），同时通过 "即插即用" 的设计理念优化现有系统的动态问答表现。</font>
    4. **<font style="color:rgba(0, 0, 0, 0.9);">整体工作流程</font>**<font style="color:rgba(0, 0, 0, 0.9);">：OmniSearch 的架构包括三个主要步骤：</font>
        * **<font style="color:rgba(0, 0, 0, 0.9);">答案整合</font>**<font style="color:rgba(0, 0, 0, 0.9);">：在每次检索后，模型会对子答案进行反馈和总结，最终生成准确、上下文相关的最终答案。</font>
        * **<font style="color:rgba(0, 0, 0, 0.9);">多模态检索</font>**<font style="color:rgba(0, 0, 0, 0.9);">：针对不同子问题，调用对应的检索工具（如图像到文本、网页到文本）。</font>
        * **<font style="color:rgba(0, 0, 0, 0.9);">问题分解与规划</font>**<font style="color:rgba(0, 0, 0, 0.9);">：模型通过 Agent Planning 模块生成子问题。</font>

:::color5
**<font style="color:#601BDE;">1.与传统RAG对比</font>**

:::

:::success
**传统RAG：**

1. 图片转文本
2. 文本召回
3. MLLM输出

:::

:::success
**OmniSearch：**

1. Planning Agent
2. Versatile Retriever：多功能(多模态)召回
3. Sub-Question Solver：子问题解决

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741514209473-6a98fcff-0715-4972-9719-f9049f368c9a.png)

:::color5
**<font style="color:#601BDE;">2.动态问答数据集：Dyn-VQA </font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">为了</font>**<font style="color:#ED740C;">评估多模态RAG技术在动态场景中的表现</font>**<font style="color:rgba(0, 0, 0, 0.9);">，阿里团队创建了一个全新的数据集—</font>**<font style="color:rgba(0, 0, 0, 0.9);">Dyn-VQA</font>**<font style="color:rgba(0, 0, 0, 0.9);">。该数据集包含三种类型的问题：</font>

1. **<font style="color:rgba(0, 0, 0, 0.9);">快速变化的答案</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如“某位明星最新的电影是什么？”，需要实时更新的知识。</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">需要多模态知识的问题</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如“这个球队的标志是什么物体？”，需要结合图像和文本信息。</font>
3. **<font style="color:rgba(0, 0, 0, 0.9);">多跳推理问题</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如“这两位演员谁的票房更高？”，需要分步推理并结合多来源信息。</font>

<font style="color:rgba(0, 0, 0, 0.9);">Dyn-VQA 数据集不仅覆盖多个领域，还模拟了真实世界中的复杂场景，是现有数据集中极具挑战性的代表。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741514485743-d64fa14a-4bc7-49df-8b7c-fa2a3b9f1b07.png)

```python
Q:谁设计了图中的建筑
GT：Antonio Barluzzi
图搜图结果：Dominus Flevit Church
网络搜索结果：Dominus Flevit Church + 设计师Antonio Barluzzi
```

1. 答案迅速改变的问题

```python
Q:图中这个人的最后一部电影是什么？
GT：Small Things Like These (2024)
图搜图结果：Cillian Murphy
网络搜索结果：Cillian Murphy + Last film
网络搜索结果：Opperheimer
网络搜索结果：Cillian Murphy + Release Date 15 February 2024
```

2. 答案需要多模态的知识

```python
Q:图中的队标是什么物品？
GT：黄黑色的球
图搜图结果：科比
网络搜索结果：科比 + NBA球队 湖人
文搜图：湖人队标
```

3. 多跳问题（需要子任务拆解，多步推理）

```python
Q:图中谁的身价更高
GT：沈腾，右边的人
图搜图结果：贾玲、沈腾
网络搜索结果：贾玲，身价100
网络搜索结果：沈腾，身价200
```

:::color5
**<font style="color:#601BDE;">3.效果评估</font>**

:::

1. **<font style="color:rgba(0, 0, 0, 0.9);">整体性能</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>
    - **<font style="color:rgba(0, 0, 0, 0.9);">OmniSearch (GPT-4V)</font>**<font style="color:rgba(0, 0, 0, 0.9);"> 取得了显著的领先成绩，F1-Recall 达到 50.03，超越其他 MLLM 以及商用生成式搜索引擎。</font>
    - **<font style="color:rgba(0, 0, 0, 0.9);">OmniSearch (Qwen-VL-Chat)</font>**<font style="color:rgba(0, 0, 0, 0.9);"> 的表现也优于大规模 GPT-4V 结合两步 mRAG 方法的结果，表明 OmniSearch 在复杂问题分解与检索负载降低方面的优势。</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">不同子问题求解器的影响</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">当使用 GPT-4V 作为 Qwen-VL-Chat 的子问题求解器时，OmniSearch 的性能显著提升，证明了更强大的子问题求解器对模型整体性能的正面影响。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">在更复杂的调用策略中，针对多模态问题使用 GPT-4V，而针对纯文本问题使用 GPT-4，这种组合进一步提升了模型性能。未来，可探索如子问题输出框信息以引导更精准检索的策略。</font>
3. **<font style="color:rgba(0, 0, 0, 0.9);">检索路径规划的作用</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">实验显示，使用 OmniSearch 自身作为子问题求解器不仅没有降低性能，反而提高了其问题解决能力，表明检索路径规划学习增强了模型的知识推理能力，带来了跨任务的收益。</font>
4. **<font style="color:rgba(0, 0, 0, 0.9);">成本与性能的权衡</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">替换子问题求解器（如将 GPT-4V 替换为 Qwen-VL-Chat）会导致性能下降约 7.9%，但成本降低近一半。结果表明，在资源有限的情况下，应优先确保检索规划模型采用更强大的基础模型。</font>
5. **<font style="color:rgba(0, 0, 0, 0.9);">商用搜索引擎不足</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">商用生成式搜索引擎在 Dyn-VQA 上表现较弱，即使是表现最好的 Gemini，也仅与 GPT-4V 的两步 mRAG 方法持平。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">进一步分析发现，这些引擎缺乏多模态信息整合能力，例如无法正确关联问题中的指代词与图像中的对象。</font>





## 慕尼黑大学-多模态RAG
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：《Beyond Text: Optimizing RAG with Multimodal Inputs for Industrial Applications》</font>

<font style="color:rgb(51, 51, 51);">paper:</font>[https://arxiv.org/pdf/2410.21943](https://arxiv.org/pdf/2410.21943)

:::

**背景**：<font style="color:rgb(25, 27, 31);">当前，尽管针对纯文本 RAG 系统及其优化的研究已经十分广泛，但对于多模态 RAG 应用的研究却相对较少。为此，本文将探索如何将多模态模型集成至RAG 系统中，即看一看结合图像和文本是否可以提高 RAG 的性能，并找出了这种系统的最佳配置。</font>

**<font style="color:rgb(25, 27, 31);">多模态RAG系统</font>**<font style="color:rgb(25, 27, 31);"> 作者构建了一个多模态RAG系统，该系统具备两种配置，一种是</font>[**<font style="color:rgb(9, 64, 142);">多模态嵌入</font>**](https://zhida.zhihu.com/search?content_id=249847138&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%B5%8C%E5%85%A5&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">和独立向量存储</font>**<font style="color:rgb(25, 27, 31);">、</font>[**<font style="color:rgb(9, 64, 142);">图像摘要</font>**](https://zhida.zhihu.com/search?content_id=249847138&content_type=Article&match_order=1&q=%E5%9B%BE%E5%83%8F%E6%91%98%E8%A6%81&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">和联合向量存储</font>**<font style="color:rgb(25, 27, 31);">。如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741575123961-b02d74e1-1d99-44f7-9e8b-aba6f5dc41ba.png)

:::color5
**<font style="color:#601BDE;">1.研究方法</font>**

:::

<font style="color:rgb(25, 27, 31);">本文作者研究主要关注两个问题：</font>

+ <font style="color:rgb(25, 27, 31);">1）基于工业领域中的PDF文档，将单模态文本、单模态图像、文本+图像双模态放入RAG系统中，看一看文本+图像双模态是否能够提升RAG系统的性能？</font>
+ <font style="color:rgb(25, 27, 31);">2）如何优化多模态RAG系统？</font>

<font style="color:rgb(25, 27, 31);">为了回答这两个问题，本文作者首先选择了当前主流的两个多模态模型GPT4-Vision，LLaVA ，然后手动标注了数据集和RAG系统测试集，接着作者构建了一个多模态RAG系统（两种配置），将文本和图像结合到一块儿；最后作者按照RAG系统的6个评估指标进行实验对比。</font>

:::color5
**<font style="color:#601BDE;">2.benchmark</font>**

:::

**<font style="color:rgb(25, 27, 31);">手动标注数据集</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">使用了来自工业领域的 20 份 PDF 文档，例如用于可编程控制器、断路器和机器人等设备的手册和软件文档。从这些文档中提取了文本和图像，共生成了 8540 个文本片段（每个片段平均长度为 225 个单词）和 8377 张图像，并按页对齐以确保上下文的准确性。每条数据集是包含文本上下文、图像上下文、问题和答案的四元组。</font>

**<font style="color:rgb(25, 27, 31);">RAG系统测试集</font>**<font style="color:rgb(25, 27, 31);"> 手动标注了 100 对问答对。每个标注包含一个问题、参考答案以及用于检索相应文本和图像上下文的页码，从而形成多模态四元组。问题设计旨在涵盖典型的工业任务，如操作程序、设备配置和故障排除，其中视觉上下文至关重要。</font>

:::color5
**<font style="color:#601BDE;">3.评估指标</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">答案正确性</font>**<font style="color:rgb(25, 27, 31);">通过参考引导的成对比较来评估生成答案与参考答案的正确性，这是唯一依赖于存在真实答案的指标；</font>
+ **<font style="color:rgb(25, 27, 31);">答案相关性</font>**<font style="color:rgb(25, 27, 31);">评估生成答案与问题的相关性；</font>
+ **<font style="color:rgb(25, 27, 31);">文本忠诚度</font>**<font style="color:rgb(25, 27, 31);">衡量生成答案与检索到的文本上下文之间的一致性；</font>
+ **<font style="color:rgb(25, 27, 31);">图像忠诚度</font>**<font style="color:rgb(25, 27, 31);">评估生成答案与检索到的图像内容的符合程度；</font>
+ **<font style="color:rgb(25, 27, 31);">文本上下文相关性</font>**<font style="color:rgb(25, 27, 31);">评估检索到的文本上下文在回答问题时的相关性；</font>
+ **<font style="color:rgb(25, 27, 31);">图像上下文相关性</font>**<font style="color:rgb(25, 27, 31);">则评估检索到的图像与问题的相关性。</font>

<font style="color:rgb(25, 27, 31);">本文实验结果如下，可以发现</font>**<font style="color:rgb(25, 27, 31);">结合文本和图像能够显著提升RAG系统的性能</font>**<font style="color:rgb(25, 27, 31);">，尤其是在检索过程能够成功识别相关文本和图像时。相比多模态嵌入，利用图像的文本摘要提供了更大的灵活性和优化空间，即</font>**<font style="color:rgb(25, 27, 31);">多模态RAG系统采用图像摘要和联合向量存储架构会好一些</font>**<font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741575383259-6b3747ee-3020-4fc6-a499-ee793d5c5d58.png)

