# ⓸ 视觉&多模态编码器

<!-- source: yuque://zhongxian-iiot9/hlyypb/zsqi80kwg5qcmp0b -->

# 多模态embedding
## GME
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：GME基于</font>[Qwen2-VL多模态大语言模型](https://www.baidu.com/s?rsv_dl=re_dqa_generate&sa=re_dqa_generate&wd=Qwen2-VL%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&rsv_pq=bb75632a005e0fef&oq=gme%E6%A8%A1%E5%9E%8B&rsv_t=7b43REBTdYaOxpEANGz3/1ADvYTv4FyOCfdzZxXDOunidQ4ckKFae3dsp/+7rPII/6WX&tn=baiduhome_pg&ie=utf-8)<font style="color:rgb(51, 51, 51);">构建，采用对比学习的方法进行训练。每个训练样本包含一个查询、一个相关候选项及多组无关候选项，覆盖文本、图像及图文组合等多种数据类型。通过指令调优，GME能够适应不同的检索任务，如视觉问答（VQA）等，进一步增强了模型的表征能力‌。</font>

**<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://arxiv.org/pdf/2412.16855](https://arxiv.org/pdf/2412.16855)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741155842432-05f3427b-e5ee-4c57-8a52-da81eb1cc47d.png)

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

1. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">训练数据组成：</font>**

多模态表征学习的一个关键因素是训练数据的组成。由于数据多样性对模型性能的影响尚不清楚，我们比较了**<font style="color:#74B602;">在各种检索场景中，用不同数据组合训练的模型的性能</font>**。具体来说，我们使用了四种类型的训练数据：单模态（包括文→文和图→图）、跨模态（包括文->图和图-文）、融合模态训练数据（包括图文→图文）和结合前三种类型的混合数据集。这些不同的训练数据类型导致得到六个模型。

    1. **<font style="color:rgb(34, 34, 34);">结论：多种模态数据平衡</font>**<font style="color:rgb(34, 34, 34);">：GME的训练数据包括单模态、跨模态和融合模态数据。通过实验，研究团队发现</font>**<font style="color:#74B602;">平衡不同类型模态的数据可以显著提高模型在各种检索场景中的表现</font>**<font style="color:rgb(34, 34, 34);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741157470363-66e384b5-4e8c-43d3-8562-47fdb4173201.png)

2. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">多模态数据合成</font>**<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">：</font>

<font style="color:rgb(34, 34, 34);">GME不仅利用了丰富的单模态和跨模态数据，还通过大模型生成技术，合成了海量的混合模态相关性数据。为了高效合成高质量的融合模态数据，研究团队采用了类似于</font>**<font style="color:#74B602;">Doc2Query</font>**<font style="color:rgb(34, 34, 34);">的策略。具体步骤包括：</font>**<font style="color:#74B602;">文档到查询生成、实体提取和查询重写、图像检索和生成以及数据过滤</font>**<font style="color:rgb(34, 34, 34);">。通过这些步骤，研究团队成功合成了113.5万条高质量的融合模态训练数据，显著增强了模型的训练和性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741143953209-ea2bce04-a873-4e55-9668-7a8e56036f81.png)

+ **<font style="color:rgb(34, 34, 34);">方法</font>**<font style="color:rgb(34, 34, 34);">：为了高效地合成高质量数据，同时最大限度地减少人工干预，生成融合模态候选来查询相关性数据，我们采用一种类似于Doc2Query的策略。</font>
+ **<font style="color:rgb(34, 34, 34);">数据处理</font>**<font style="color:rgb(34, 34, 34);">：</font>
    1. **<font style="color:rgb(34, 34, 34);">数据源</font>**<font style="color:rgb(34, 34, 34);">：我们主要从维基百科中提取了这些数据。</font>
    2. **<font style="color:rgb(34, 34, 34);">分类</font>**<font style="color:rgb(34, 34, 34);">：为了增强候选数据的领域多样性，我们采用了领域分类模型,对维基百科进行细粒度分类将数据分为动物和植物等类别。</font>
    3. **<font style="color:rgb(34, 34, 34);">采样</font>**<font style="color:rgb(34, 34, 34);">：我们从这些样本中均匀采样分类置信度得分高于0.5的类别和保留数据，我们获得了313284个候选条目，每个条目都包含文本和图像内容。</font>
+ **<font style="color:rgb(34, 34, 34);">Doc2Query生成</font>**<font style="color:rgb(34, 34, 34);">：将每个候选人的内容</font>**<font style="color:#74B602;">输入到LLM中生成文章的quer</font>**<font style="color:rgb(34, 34, 34);">y。为了确保生成的查询的质量，我们构建了一个</font>使用文本向量检索模型对所有段落内容进行向量索引。然后使用query从该集合中检索相应的段落。如果与query关联的文章不在检索的top20中，**<font style="color:#74B602;">则认为该query由于相关性低被丢弃</font>**。在这一步中，我们丢弃了1.2%的生成的查询总数。这个过程使我们能够构建Text→ImageText的训练数据。
+ **实体提取和query改写**：我们的目标是合成**<font style="color:#74B602;">同时包含文本以及图像的query</font>**（即IT→IT类型）。为了实现这一点，我们利用实体提取，然后对提取的实体进行图像检索，并**<font style="color:#74B602;">生成caption以补充图像query</font>**。具体来说，对于第一步中生成的每个查询q，我们使用使用LLM提取实体并**<font style="color:#74B602;">重写原始查询</font>**。例如，**<font style="color:#ED740C;">query “鸢尾花原产自哪里”被改写为“这个职务原产自哪里?”，同时抽取出实体“鸢尾花”</font>**。然后，**<font style="color:#ED740C;">我们寻找与该实体匹配的图像</font>**，并将其与改写的查询q′以形成最终的**<font style="color:#ED740C;">图文query</font>**。
+ **图像检索和生成**：我们探索了两种获取图像的方法。第一种方法使用谷歌图片搜索API检索与实体匹配的图像，保留top5结果。这个第二种方法涉及使用文生图（**<font style="color:#74B602;">FLUX</font>**），使用LLM生成caption，然后使用caption输入到文生图模型以创建相应的图像。这种方法使我们能够快速有效地获得高质量、多样化的图像。合成的结果也可以组装成IT→IT检索类型数据。
+ **数据过滤**：为了保证合成数据的质量，我们对最终数据集进行过滤。我们观察到FLUX生成的图像模型具有一致的质量，而通过谷歌图像搜索API检索的图像通常包括噪声数据。因此，对于通过谷歌图像搜索获得的图像API，我们使用**<font style="color:#74B602;">CLIP模型来评估图像适应相关性</font>**。相似度<0.2的图片将被过滤。
+ **数据量**：通过上述合成流程，我们生成了1135k个高质量的融合模态训练数据条目（包括T→IT和IT→IT类型）。经过筛选，我们保留了1102k个条目，导致数据丢失率为2.9%。整个过程消耗了600 A100 GPU/hour

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741155784840-ac5bb51d-704f-49a6-8ae3-121774124bf2.png)

**<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">3.hard negative：</font>**

<font style="color:rgb(34, 34, 34);">为了提高对比学习模型的质量和多样性，GME采用了两阶段训练策略：首先使用随机选择的负候选进行初始训练，然后使用初始模型检索每个查询的前K个候选，从中选择非相关候选作为硬负样本进行进一步训练。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741143670524-671d48af-bcdf-4bc1-84b7-9041f3da9af2.png)

<font style="color:rgb(34, 34, 34);">GME基于MLLM构建，能够接受图像、文本或图像-文本对作为输入。受先前文本嵌入研究的启发，</font>**<font style="color:#74B602;">GME使用的最后一个hidden_state的最后一个token作为输入（表征）</font>**<font style="color:rgb(34, 34, 34);">。尽管预训练的MLLM具有强大的多模态理解能力，但其原始训练目标并未针对表示学习进行优化。因此，需要进行任务特定的微调（或对齐）以增强模型的表示能力。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">对比学习：</font>**

<font style="color:rgb(34, 34, 34);">在对比学习设置中，每个训练实例包括一个查询q、一个相关候选c和一组不相关的候选{c1−,c2−,…,cK−}。为了适应各种下游检索任务，</font>**<font style="color:#74B602;">GME采用了指令调优方法，为每个检索任务添加定制的指令文本i</font>**<font style="color:rgb(34, 34, 34);">。例如，</font>**<font style="color:#ED740C;">对于视觉问答（VQA）任务，指令可以是：“检索一篇文章，为关于图像的给定查询提供答案”。</font>**<font style="color:rgb(34, 34, 34);">训练中，GME通过最小化相关对的余弦距离，同时最大化不相关对的余弦距离来优化模型。</font>

2. **<font style="background-color:#D9EAFC;">两阶段训练</font>**

目的：负样本样本的质量和多样性对于对比学习效果至关重要

    1. 初始训练：我们首先使用随机采样负样本，得到模型M1。
    2. hard_negative继续训练：基于M1，**<font style="color:#74B602;">基于每个query的topk检索结果，使用其中真实的负样本来训练</font>**。然后，我们使用这些hard_negative进一步训练M1，将其细化为最终模型。这种方法可确保模型学习到**<font style="color:#74B602;">更具挑战性的例子中</font>**，从而增强整体效果。
1. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">损失函数：</font>**

<font style="color:rgb(34, 34, 34);">inforNCE loss，</font>其中τ是温度参数，用于缩放余弦相似度以控制分布的集中度。这种方法确保模型有效地学习区分不同模态中的相关信息和不相关信息，从而增强其在多模态检索任务中的性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741156039546-efc7956c-bca2-4a0e-8d74-f92099427db7.png)

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">embedding显著提升复杂query的检索精度。</font>
+ <font style="color:rgb(51, 51, 51);">通过LLM的知识迁移增强小样本学习能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">推理速度较慢（需LLM前向计算）。</font>
+ <font style="color:rgb(51, 51, 51);">训练需多阶段协调，资源消耗大。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">跨模态搜索</font>**<font style="color:rgb(51, 51, 51);">：电商（图片搜商品描述）、医疗（报告检索影像）。</font>
+ **<font style="color:rgb(51, 51, 51);">开放域问答</font>**<font style="color:rgb(51, 51, 51);">：结合知识库的多模态问答系统。</font>
+ **<font style="color:rgb(51, 51, 51);">内容安全</font>**<font style="color:rgb(51, 51, 51);">：图文一致性审核。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化</font>**<font style="color:rgb(51, 51, 51);">：用LoRA微调LLM，减少参数量。</font>
+ **<font style="color:rgb(51, 51, 51);">缓存策略</font>**<font style="color:rgb(51, 51, 51);">：对高频query预生成动态embedding。</font>
+ **<font style="color:rgb(51, 51, 51);">多粒度对齐</font>**<font style="color:rgb(51, 51, 51);">：引入物体检测（如Faster R-CNN）实现区域-词对齐。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import ViTModel, BertModel, LlamaForCausalLM

class GMEModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 编码器
        self.image_encoder = ViTModel.from_pretrained("google/vit-base-patch16-224")
        self.text_encoder = BertModel.from_pretrained("bert-base-uncased")
        # LLM生成动态embedding
        self.llm = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b")
        # 检索适配器
        self.adapter = nn.Sequential(
            nn.Linear(4096, 1024),  # LLM隐藏层维度→检索空间
            nn.ReLU(),
            nn.LayerNorm(1024)
        )

    def forward(self, image, text):
        # 提取特征
        img_feat = self.image_encoder(image).last_hidden_state.mean(dim=1)  # [B, D_img]
        txt_feat = self.text_encoder(text).last_hidden_state[:, 0, :]       # [B, D_txt]
        
        # 拼接特征输入LLM
        llm_input = torch.cat([img_feat, txt_feat], dim=1)  # [B, D_img+D_txt]
        llm_output = self.llm(inputs_embeds=llm_input.unsqueeze(1)).last_hidden_state  # [B, L, D_llm]
        
        # 生成动态embedding
        dynamic_emb = self.adapter(llm_output[:, -1, :])  # 取最后一个token
        return dynamic_emb

# 对比损失示例
def contrastive_loss(query_emb, target_emb, temperature=0.07):
    sim_matrix = torch.matmul(query_emb, target_emb.T) / temperature
    labels = torch.arange(query_emb.size(0)).to(query_emb.device)
    return nn.CrossEntropyLoss()(sim_matrix, labels)

```



[https://arxiv.org/pdf/2412.16855](https://arxiv.org/pdf/2412.16855)

GME: Improving Universal Multimodal Retrieval by Multimodal LLMs

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735291851222-731a0e4c-c9bb-43a4-bb5d-d68722c95253.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741143670524-671d48af-bcdf-4bc1-84b7-9041f3da9af2.png)

# 视觉embedding
## VIT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">ViT（Vision Transformer）</font>**<font style="color:rgb(51, 51, 51);"> 是 Google Research 在 2020 年提出的纯 Transformer 架构的视觉模型，首次将 Transformer 成功应用于图像分类任务。传统卷积神经网络（CNN）依赖局部感受野和层次化特征提取，而 ViT 通过全局注意力机制捕捉长距离依赖关系，打破了 CNN 在视觉任务中的垄断地位。</font>

+ **<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>[《An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale》](https://arxiv.org/abs/2010.11929)
+ **<font style="color:rgb(51, 51, 51);">官方实现</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/google-research/vision_transformer](https://github.com/google-research/vision_transformer)
+ **<font style="color:rgb(51, 51, 51);">预训练模型</font>**<font style="color:rgb(51, 51, 51);">：</font>[Hugging Face Model Hub](https://huggingface.co/models?search=vit)

:::

<font style="color:rgb(51, 51, 51);">ViT 的提出标志着视觉模型从 CNN 到 Transformer 的范式转变，为后续多模态大模型（如 CLIP、DALL·E）奠定了重要基础。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741081262511-4a2a3baf-2775-4809-8c6f-0e8a517f7f9b.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像分块（Image Patching）</font>**
    - <font style="color:rgb(51, 51, 51);">将图像分割为固定大小的非重叠块（如 16x16），展平后作为序列输入。</font>
2. **<font style="color:rgb(51, 51, 51);">位置编码（Position Embedding）</font>**
    - <font style="color:rgb(51, 51, 51);">为每个图像块添加可学习的位置编码，保留空间信息。</font>
3. **<font style="color:rgb(51, 51, 51);">纯 Transformer 架构</font>**
    - <font style="color:rgb(51, 51, 51);">移除卷积操作，完全依赖自注意力机制进行特征提取。</font>
4. **<font style="color:rgb(51, 51, 51);">大规模预训练</font>**
    - <font style="color:rgb(51, 51, 51);">在超大规模数据集（如 JFT-300M）上预训练，弥补 Transformer 数据效率低的缺陷。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">预训练数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">公开数据集</font>**<font style="color:rgb(51, 51, 51);">：ImageNet-21k（14M 图像，21k 类）、JFT-300M（300M 图像，18k 类），监督学习预训练。</font><font style="color:rgba(0, 0, 0, 0.75);">通过大量的标注数据，模型学习到丰富的视觉特征。</font>
    - **<font style="color:rgb(51, 51, 51);">合成数据</font>**<font style="color:rgb(51, 51, 51);">：部分改进工作引入生成模型（如 Diffusion）扩展数据。</font>
+ **<font style="color:rgb(51, 51, 51);">微调数据</font>**<font style="color:rgb(51, 51, 51);">：任务特定数据集（如 ImageNet-1k、CIFAR）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **Patch Embedding**
    - <font style="color:rgb(51, 51, 51);">输入图像（H×W×C） → 分块（N×P²×C） → 展平为 N×(P²·C) → 线性投影为 D 维向量。</font>
    - <font style="color:rgb(51, 51, 51);">例如：224x224 图像 → 16x16 分块 → 196 个块 → 线性投影为 768 维。</font>
2. **位置编码**
    - <font style="color:rgb(51, 51, 51);">可学习的一维向量，与 Patch Embedding 相加。</font>
    - 在Transformer中，位置编码的作用是为了记忆输入的语序信息。ViT中，同样需要位置编码来记录各图像块之间的位置信息。论文使用的是**<font style="color:#74B602;">1-D的位置编码（绝对位置编码）</font>**，即和Transformer论文中使用的位置编码一致，使用了正弦和余弦函数生成位置编码向量。
    - 为什么不用2D-位置编码：作者使用三种编码方式进行实验：1D,2D,相对位置编码，使用三种位置编码得到的结果几乎一致，证明在此任务上三种编码都可以，我们使用最简单的一种。
    - 作者随后也对一维位置编码的结果进行了可视化，下图中是每一个Patch中各位置的位置编码相似性度量，越接近黄色的位置代表越靠近位置编码的中心位置，可以看到，即使是一维位置编码，同样可以比较好地记录二维信息。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741081553073-0e11e349-093a-4ec5-8d5d-3caf966dfff4.png)

3. **Transformer Encoder**
    - <font style="color:rgb(51, 51, 51);">多头自注意力（Multi-Head Self-Attention） + MLP 块（GELU 激活）。</font>
    - <font style="color:rgb(51, 51, 51);">层归一化（LayerNorm）和残差连接（Residual Connection）。</font>
4. **分类头**
    - <font style="color:rgb(51, 51, 51);">取 [CLS] 标志对应的向量 → MLP → Softmax 输出类别概率。</font>
    - <font style="color:rgb(51, 51, 51);">和Transformer类似的，论文也添加了一个<cls>Token用来代表全局(整个图片)的特征向量，和BERT类似，当我们做图片分类任务时，我们可以使用对这个特征向量进行MLP，得到分类结果，他的形状是1 × 768，我们将其和上述的输入做合并，输入矩阵形状为197 × 768 .</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练（大规模数据）**：
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：图像分类（交叉熵损失）。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：AdamW，余弦学习率衰减。</font>
    - **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：RandAugment、MixUp、CutMix。</font>
2. **微调（下游任务）**：
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：适应特定任务（分类、检测、分割等）。</font>
    - **<font style="color:rgb(51, 51, 51);">策略</font>**<font style="color:rgb(51, 51, 51);">：全模型微调或部分层微调，学习率更低。</font>
3. **混合训练（改进变体）**：
    - <font style="color:rgb(51, 51, 51);">结合 CNN（如 Hybrid ViT）或引入蒸馏（DeiT）。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 全局注意力机制，擅长捕捉长距离依赖</font> | <font style="color:rgb(51, 51, 51);">1. 数据效率低，依赖大规模预训练</font> |
| <font style="color:rgb(51, 51, 51);">2. 并行计算友好，适合硬件加速</font> | <font style="color:rgb(51, 51, 51);">2. 计算复杂度高（序列长度平方级）</font> |
| <font style="color:rgb(51, 51, 51);">3. 可扩展性强（模型深度/宽度易调整）</font> | <font style="color:rgb(51, 51, 51);">3. 缺乏局部归纳偏置，小数据集易过拟合</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">（ImageNet、CIFAR）。</font>
2. **<font style="color:rgb(51, 51, 51);">目标检测</font>**<font style="color:rgb(51, 51, 51);">（DETR、ViT-FRCNN）。</font>
3. **<font style="color:rgb(51, 51, 51);">图像分割</font>**<font style="color:rgb(51, 51, 51);">（SETR、Segmenter）。</font>
4. **<font style="color:rgb(51, 51, 51);">视频理解</font>**<font style="color:rgb(51, 51, 51);">（TimeSformer、ViViT）。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据效率优化</font>**
    - **<font style="color:rgb(51, 51, 51);">DeiT</font>**<font style="color:rgb(51, 51, 51);">：通过蒸馏从 CNN 中学习，减少数据依赖。</font>
2. **<font style="color:rgb(51, 51, 51);">计算效率优化</font>**
    - **<font style="color:rgb(51, 51, 51);">Swin Transformer</font>**<font style="color:rgb(51, 51, 51);">：引入局部窗口注意力，降低计算量。</font>
3. **<font style="color:rgb(51, 51, 51);">局部-全局结合</font>**
    - **<font style="color:rgb(51, 51, 51);">Hybrid ViT</font>**<font style="color:rgb(51, 51, 51);">：使用 CNN 提取底层特征，再输入 Transformer。</font>
4. **<font style="color:rgb(51, 51, 51);">多模态扩展</font>**
    - **<font style="color:rgb(51, 51, 51);">CLIP</font>**<font style="color:rgb(51, 51, 51);">：联合训练图像和文本编码器。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class PatchEmbedding(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.norm = nn.LayerNorm(embed_dim)
        self.pos_embed = nn.Parameter(torch.randn(1, (img_size//patch_size)**2 + 1, embed_dim))

    def forward(self, x):
        x = self.proj(x)  # [B, C, H, W] → [B, D, H/P, W/P]
        x = rearrange(x, "b c h w → b (h w) c")
        x = self.norm(x)
        # 添加 [CLS] token
        cls_token = nn.Parameter(torch.randn(1, 1, embed_dim)).expand(x.shape[0], -1, -1)
        x = torch.cat([cls_token, x], dim=1)
        x += self.pos_embed
        return x

class ViT(nn.Module):
    def __init__(self, num_layers=12, num_heads=12, mlp_dim=3072):
        super().__init__()
        self.patch_embed = PatchEmbedding()
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=768, nhead=num_heads, dim_feedforward=mlp_dim)
            for _ in range(num_layers)
        ])
        self.head = nn.Linear(768, num_classes)

    def forward(self, x):
        x = self.patch_embed(x)
        for layer in self.encoder_layers:
            x = layer(x)
        cls_output = x[:, 0, :]
        return self.head(cls_output)

# 示例用法
model = ViT(num_classes=1000)
x = torch.randn(1, 3, 224, 224)
output = model(x)
print(output.shape)  # torch.Size([1, 1000])

```

```python
from torch.optim import AdamW
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import torchvision.transforms as T

# 数据加载
transform = T.Compose([
    T.Resize(224),
    T.ToTensor(),
])
dataset = CIFAR10(root="data", train=True, download=True, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 模型与优化器
model = ViT(num_classes=10)
optimizer = AdamW(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()

# 训练循环
for epoch in range(10):
    for images, labels in dataloader:
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

```

## DeiT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">DeiT（Data-efficient Image Transformer）</font>**<font style="color:rgb(51, 51, 51);"> 是 Facebook Research 在 2020 年提出的改进版视觉 Transformer，旨在解决 ViT（Vision Transformer）</font>**<font style="color:#ED740C;">依赖大规模预训练数据的问题</font>**<font style="color:rgb(51, 51, 51);">。ViT 需要 JFT-300M 等超大数据集才能达到与 CNN 相当的性能，</font>**<font style="color:#ED740C;">而 DeiT 通过知识蒸馏（Knowledge Distillation）和高效训练策略，仅用 ImageNet-1K（1.2M 图像）即可训练高性能 Transformer，推动 ViT 在资源有限场景下的应用。</font>**

+ **<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>[《Training data-efficient image transformers & distillation through attention》](https://arxiv.org/abs/2012.12877)
+ **<font style="color:rgb(51, 51, 51);">官方代码</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/facebookresearch/deit](https://github.com/facebookresearch/deit)

:::

<font style="color:rgb(51, 51, 51);">DeiT 通过蒸馏技术显著降低了 ViT 的数据需求，成为轻量级视觉 Transformer 的标杆，为实际工业部署提供了高效解决方案。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086834536-c06b374e-218a-4d84-9d97-5d5dda8c1192.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **蒸馏 Token（Distillation Token）**
    - <font style="color:rgb(51, 51, 51);">在输入序列中引入</font>**<font style="color:#74B602;">可学习的蒸馏标记（与 [CLS] 标记并行）</font>**<font style="color:rgb(51, 51, 51);">，直接学习教师模型（如 CNN）的输出分布。</font>
    - <font style="color:rgb(51, 51, 51);">比传统蒸馏（仅用标签概率）更高效，尤其对小模型效果显著。</font>
2. **硬蒸馏与软蒸馏结合**
    - **<font style="color:rgb(51, 51, 51);">硬蒸馏</font>**<font style="color:rgb(51, 51, 51);">：将教师模型的预测类别（硬标签）作为监督信号。</font>
    - **<font style="color:rgb(51, 51, 51);">软蒸馏</font>**<font style="color:rgb(51, 51, 51);">：使用教师模型的输出概率（软标签）指导训练。</font>
3. **高效数据增强**
    - <font style="color:rgb(51, 51, 51);">结合 RandAugment、MixUp、CutMix 等策略，提升数据利用率。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：ImageNet-1K（1.28M 训练图像，1k 类别）。</font>
+ **<font style="color:rgb(51, 51, 51);">教师模型</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">预训练的 CNN（如 RegNetY-16GF 或 ResNet-152）。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">RandAugment（随机增强强度自适应）、Erasing、重复增强（Repeated Augmentation）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

**<font style="color:rgb(51, 51, 51);">关键改进</font>**

1. **蒸馏 Token 处理**
    - <font style="color:rgb(51, 51, 51);">蒸馏 Token 与 [CLS] Token 并行输入 Transformer，通过自注意力交互。</font>
    - <font style="color:rgb(51, 51, 51);">最终输出两个预测结果：学生模型预测（[CLS]）和教师蒸馏预测（Distillation）。</font>
2. **损失函数设计**
    - <font style="color:rgb(51, 51, 51);">总损失 = 学生分类损失（CE） + 蒸馏损失（KL 散度）。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **教师模型准备**
    - <font style="color:rgb(51, 51, 51);">使用预训练 CNN 生成图像标签（硬标签）或概率分布（软标签）。</font>
2. **学生模型训练**
    - **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：图像分块 + [CLS] Token + Distillation Token。</font>
    - **<font style="color:rgb(51, 51, 51);">目标 1</font>**<font style="color:rgb(51, 51, 51);">（学生损失）：[CLS] 预测与真实标签的交叉熵。</font>
    - **<font style="color:rgb(51, 51, 51);">目标 2</font>**<font style="color:rgb(51, 51, 51);">（蒸馏损失）：Distillation 预测与教师输出的 KL 散度。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：AdamW，余弦学习率衰减，权重衰减分层设置。</font>
3. **训练技巧**
    - **<font style="color:rgb(51, 51, 51);">重复增强</font>**<font style="color:rgb(51, 51, 51);">：同一图像的不同增强版本在同一批次中出现，提升泛化性。</font>
    - **<font style="color:rgb(51, 51, 51);">随机深度（Stochastic Depth）</font>**<font style="color:rgb(51, 51, 51);">：随机丢弃部分层，防止过拟合。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 数据高效，仅需 ImageNet-1K 即可训练</font> | <font style="color:rgb(51, 51, 51);">1. 依赖教师模型的质量</font> |
| <font style="color:rgb(51, 51, 51);">2. 训练速度快（比 ViT 收敛更快）</font> | <font style="color:rgb(51, 51, 51);">2. 蒸馏 Token 增加模型参数量</font> |
| <font style="color:rgb(51, 51, 51);">3. 支持模型压缩（如 Tiny-DeiT）</font> | <font style="color:rgb(51, 51, 51);">3. 对数据增强策略敏感</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">：轻量级部署（移动端、边缘设备）。</font>
2. **<font style="color:rgb(51, 51, 51);">迁移学习</font>**<font style="color:rgb(51, 51, 51);">：作为下游任务（检测、分割）的预训练模型。</font>
3. **<font style="color:rgb(51, 51, 51);">联邦学习</font>**<font style="color:rgb(51, 51, 51);">：适应分布式小数据场景。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">无教师蒸馏：  </font>**<font style="color:rgb(51, 51, 51);">自蒸馏（Self-Distillation）：同一模型不同阶段的知识迁移。</font>
2. **<font style="color:rgb(51, 51, 51);">动态蒸馏：</font>**<font style="color:rgb(51, 51, 51);">教师模型在线更新（如 EMA 策略）。</font>
3. **<font style="color:rgb(51, 51, 51);">多教师融合：</font>**<font style="color:rgb(51, 51, 51);">结合多个教师模型的输出提升鲁棒性。</font>
4. **<font style="color:rgb(51, 51, 51);">结构优化：</font>**<font style="color:rgb(51, 51, 51);">DeiT-III：引入 LayerScale 和 Class-Attention 提升性能。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from timm.models.vision_transformer import Block, PatchEmbed

class DeiT(nn.Module):
    def __init__(self, img_size=224, patch_size=16, embed_dim=768, depth=12, num_heads=12):
        super().__init__()
        self.patch_embed = PatchEmbed(img_size, patch_size, 3, embed_dim)
        num_patches = self.patch_embed.num_patches
        # 初始化 [CLS] Token 和 Distillation Token
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        self.dist_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        # 位置编码
        self.pos_embed = nn.Parameter(torch.randn(1, num_patches + 2, embed_dim))
        # Transformer 编码器
        self.blocks = nn.ModuleList([Block(embed_dim, num_heads) for _ in range(depth)])
        # 分类头
        self.head = nn.Linear(embed_dim, 1000)
        self.head_dist = nn.Linear(embed_dim, 1000)

    def forward(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)  # [B, N, D]
        # 添加 [CLS] 和 Distillation Token
        cls_tokens = self.cls_token.expand(B, -1, -1)
        dist_tokens = self.dist_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, dist_tokens, x), dim=1)
        x += self.pos_embed
        # 经过 Transformer 层
        for blk in self.blocks:
            x = blk(x)
        # 分离输出
        cls_out = x[:, 0]
        dist_out = x[:, 1]
        return self.head(cls_out), self.head_dist(dist_out)

# 示例用法
model = DeiT()
x = torch.randn(1, 3, 224, 224)
logits_cls, logits_dist = model(x)
print(logits_cls.shape)  # torch.Size([1, 1000])

```

```python
from torch.optim import AdamW
import torch.nn.functional as F

# 初始化
model = DeiT()
teacher_model = torch.hub.load('pytorch/vision', 'resnet152', pretrained=True)
optimizer = AdamW(model.parameters(), lr=1e-4)

# 蒸馏损失（软标签）
def distillation_loss(student_logits, teacher_logits, temperature=2.0):
    student_probs = F.log_softmax(student_logits / temperature, dim=1)
    teacher_probs = F.softmax(teacher_logits / temperature, dim=1)
    return F.kl_div(student_probs, teacher_probs, reduction="batchmean") * (temperature ** 2)

# 训练循环
for images, labels in dataloader:
    # 教师模型预测（不更新梯度）
    with torch.no_grad():
        teacher_logits = teacher_model(images)
    # 学生模型预测
    logits_cls, logits_dist = model(images)
    # 计算损失
    loss_cls = F.cross_entropy(logits_cls, labels)
    loss_dist = distillation_loss(logits_dist, teacher_logits)
    loss = 0.5 * loss_cls + 0.5 * loss_dist
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

```

## Swin Transformer
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Swin Transformer是微软亚洲研究院2021年提出的</font>**<font style="color:rgb(51, 51, 51);">层级化视觉Transformer</font>**<font style="color:rgb(51, 51, 51);">，针对传统ViT的</font>**<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">缺乏空间层次性</font>**<font style="color:rgb(51, 51, 51);">问题而设计。其背景特点包括：</font>

+ **<font style="color:rgb(51, 51, 51);">视觉任务需求</font>**<font style="color:rgb(51, 51, 51);">：CNN的层次化特征提取优势需要与Transformer全局建模能力结合</font>
+ **<font style="color:rgb(51, 51, 51);">效率瓶颈</font>**<font style="color:rgb(51, 51, 51);">：ViT的全局注意力计算复杂度为O(n²)，难以处理高分辨率图像（如目标检测/分割）</font>
+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：通过**滑动窗口（Shifted Window）**实现局部注意力，构建类似CNN的层次化特征金字塔</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741087210932-ca6753c8-5cf8-497c-8ce1-4425fd9eb7a7.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

| **维度** | **创新描述** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">窗口划分</font>** | <font style="color:rgb(51, 51, 51);">将特征图划分为不重叠窗口，计算</font>**<font style="color:#74B602;">窗口内自注意力</font>**<font style="color:rgb(51, 51, 51);">（计算复杂度从O(n²)降为O(n)）</font> |
| **<font style="color:rgb(51, 51, 51);">移位窗口</font>** | <font style="color:rgb(51, 51, 51);">通过窗口滑动实现</font>**<font style="color:#74B602;">跨窗口信息交互，避免全局计算</font>** |
| **<font style="color:rgb(51, 51, 51);">层级结构</font>** | <font style="color:rgb(51, 51, 51);">4-stage下采样结构（类似ResNet），输出</font>**<font style="color:#74B602;">多尺度特征图</font>** |
| **<font style="color:rgb(51, 51, 51);">相对位置编码</font>** | <font style="color:rgb(51, 51, 51);">在计算注意力时加入</font>**<font style="color:#74B602;">相对位置偏置</font>**<font style="color:rgb(51, 51, 51);">，提升空间感知能力</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **阶段** | **数据类型** | **规模** | **预处理** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">预训练</font>** | <font style="color:rgb(51, 51, 51);">ImageNet-1K/22K</font> | <font style="color:rgb(51, 51, 51);">1.28M/14M</font> | <font style="color:rgb(51, 51, 51);">RandAugment, Mixup, CutMix</font> |
| **<font style="color:rgb(51, 51, 51);">检测微调</font>** | <font style="color:rgb(51, 51, 51);">COCO 2017</font> | <font style="color:rgb(51, 51, 51);">118K</font> | <font style="color:rgb(51, 51, 51);">多尺度训练 (480~800px)</font> |
| **<font style="color:rgb(51, 51, 51);">分割微调</font>** | <font style="color:rgb(51, 51, 51);">ADE20K</font> | <font style="color:rgb(51, 51, 51);">25K</font> | <font style="color:rgb(51, 51, 51);">随机裁剪至512x512</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">层级化架构（以Swin-T为例）</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741087175978-29788f6d-7d18-4f16-89c2-35da554b0fa5.png)

```python
class SwinTransformer(nn.Module):
    def __init__(self):
        # Stage 1: Patch分割 + 线性嵌入
        self.patch_embed = PatchEmbed(img_size=224, patch_size=4, in_chans=3, embed_dim=96)

        # 4个阶段（逐渐下采样）
        self.stages = nn.ModuleList([
            SwinStage(dim=96,  depth=2, num_heads=3, window_size=7),
            SwinStage(dim=192, depth=2, num_heads=6, window_size=7),  # 下采样2x
            SwinStage(dim=384, depth=6, num_heads=12, window_size=7), # 下采样4x
            SwinStage(dim=768, depth=2, num_heads=24, window_size=7)  # 下采样8x
        ])

        # 分类头
        self.head = nn.Linear(768, num_classes)
```

2. **<font style="color:rgb(51, 51, 51);">Swin Transformer Block结构</font>**

Swin Transformer Block有两种block形式，一个是W-MSA，另一个是SW-MSA。注意这两个结构是成对使用的，先使用W-MSA再使用SW-MSA。因此Swin Transformer Block都是偶数。

+ <font style="color:rgba(0, 0, 0, 0.75);background-color:#D9EAFC;">Windows Multi-head Self-Attention（W-MSA）</font>

W-MSA将特征图划分为多个大小为M × M的小窗口（windows），每个小窗口里有M<sup>2</sup>个patch，并在每个窗口内独立地进行MSA。（一个大小为H × W的特征图，下面这个小例子中窗口大小是M = 2，因此特征图被划分成个小窗口），计算量将显著减少。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741091364826-1396ca51-2a5b-4b7b-92e2-98b729ef57ba.png)

+ <font style="color:rgba(0, 0, 0, 0.75);background-color:#D9EAFC;">Shifted Windows Multi-Head Self-Attention（SW-MSA）</font>

<font style="color:rgb(77, 77, 77);">然而W-MSA也存在一些问题，W-MSA只会在每个窗口内进行自注意力计算，窗口之间无法进行信息传递，为了解决该问题，作者提出了SW-MSA模块，即对窗口进行偏移，如下图所示：</font>



![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741087187355-fa8584f7-88ce-4b3e-940f-64a42e708d97.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练**（ImageNet）：
    - <font style="color:rgb(51, 51, 51);">优化器：AdamW（lr=0.001, weight_decay=0.05）</font>
    - <font style="color:rgb(51, 51, 51);">训练策略：300 epochs，cosine学习率衰减</font>
    - <font style="color:rgb(51, 51, 51);">数据增强：RandErasing, ColorJitter</font>
2. **下游任务微调**：
    - <font style="color:rgb(51, 51, 51);">目标检测（Mask R-CNN）：多尺度训练，AP^box从42.7提升到50.4</font>
    - <font style="color:rgb(51, 51, 51);">语义分割（UPerNet）：mIoU达到53.5（ADE20K）</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">线性计算复杂度（相比ViT的平方复杂度）</font>
+ <font style="color:rgb(51, 51, 51);">多尺度输出适配密集预测任务（检测/分割）</font>
+ <font style="color:rgb(51, 51, 51);">在COCO上超越ResNet-50约4.5 AP</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">窗口移位操作增加实现复杂度</font>
+ <font style="color:rgb(51, 51, 51);">小规模数据（如CIFAR）上表现不如CNN</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

| **场景** | **典型应用** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">图像分类</font> | <font style="color:rgb(51, 51, 51);">ImageNet Top-1 Acc 87.3% (Swin-L)</font> |
| <font style="color:rgb(51, 51, 51);">目标检测</font> | <font style="color:rgb(51, 51, 51);">COCO检测任务（Swin + Mask R-CNN）</font> |
| <font style="color:rgb(51, 51, 51);">语义分割</font> | <font style="color:rgb(51, 51, 51);">ADE20K语义分割（Swin + UPerNet）</font> |
| <font style="color:rgb(51, 51, 51);">视频分析</font> | <font style="color:rgb(51, 51, 51);">时空扩展版本Video Swin Transformer</font> |


:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **效率优化**：
    - <font style="color:rgb(51, 51, 51);">CSWin Transformer：引入十字形窗口注意力</font>
    - <font style="color:rgb(51, 51, 51);">SwinIR：结合图像复原任务优化窗口划分</font>
2. **性能提升**：
    - <font style="color:rgb(51, 51, 51);">SwinV2：使用对数间隔连续位置偏置（解决大模型训练不稳定）</font>
    - <font style="color:rgb(51, 51, 51);">混合架构：Swin-Unet用于医学图像分割</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch import nn

class WindowAttention(nn.Module):
    """基于移位窗口的多头自注意力"""
    def __init__(self, dim, window_size, num_heads):
        super().__init__()
        self.dim = dim
        self.window_size = window_size
        self.num_heads = num_heads
        
        # 相对位置编码表
        self.relative_position_bias_table = nn.Parameter(
            torch.zeros((2*window_size-1)**2, num_heads))
        
        # 生成相对位置索引
        coords = torch.stack(torch.meshgrid(
            [torch.arange(window_size), torch.arange(window_size)]))
        coords_flatten = torch.flatten(coords, 1)
        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]
        relative_coords = relative_coords.permute(1, 2, 0).contiguous()
        relative_coords[:, :, 0] += window_size - 1
        self.register_buffer("relative_position_index", relative_coords.sum(-1))
    
    def forward(self, x):
        B, H, W, C = x.shape
        x = x.view(B, H//self.window_size, self.window_size,
                   W//self.window_size, self.window_size, C)
        x = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, self.window_size*self.window_size, C)
        
        # 计算注意力（含相对位置偏置）
        qkv = self.qkv(x).reshape(-1, self.window_size*self.window_size, 3, self.num_heads, C//self.num_heads)
        attn = (q @ q.transpose(-2, -1)) * self.scale
        relative_bias = self.relative_position_bias_table[self.relative_position_index.view(-1)]
        attn += relative_bias.view(1, self.num_heads, self.ws*self.ws, self.ws*self.ws)
        attn = self.softmax(attn)
        
        x = (attn @ v).transpose(1, 2).reshape(-1, self.ws*self.ws, C)
        return x.view(B, H, W, C)

class SwinBlock(nn.Module):
    """包含常规窗口和移位窗口的双分支结构"""
    def __init__(self, dim, num_heads, window_size):
        super().__init__()
        # 常规窗口分支
        self.norm1 = nn.LayerNorm(dim)
        self.attn1 = WindowAttention(dim, window_size, num_heads)
        
        # 移位窗口分支（移位量为window_size//2）
        self.norm2 = nn.LayerNorm(dim)
        self.attn2 = WindowAttention(dim, window_size, num_heads, shift_size=window_size//2)
        
        self.mlp = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, dim*4),
            nn.GELU(),
            nn.Linear(dim*4, dim)
        )
    
    def forward(self, x):
        # 第一分支
        x = x + self.attn1(self.norm1(x))
        # 第二分支（移位窗口）
        x = x + self.attn2(self.norm2(x))
        x = x + self.mlp(x)
        return x

```

## NaViT
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">一般标准的预训练好的ViT，通常是将图片处理成正方形（长:宽=1:1）。这样处理后通常图片会失真，导致模型理解上有信息损失或引入一些误导。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">原生动态分辨率方法具体是怎么实现的呢？ 核心方法是采用了</font>**<font style="color:#ED740C;">NaViT的</font>**[**<font style="color:#ED740C;">Patch n’ Pack</font>**](https://zhida.zhihu.com/search?content_id=254075742&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)**<font style="color:#ED740C;">技术，把不同图像的多个patch打包到一个序列，能保留不同图片的可变分辨率</font>**<font style="color:rgb(25, 27, 31);">。同时在</font>**<font style="color:#ED740C;">一个次序列计算中同时可处理多个图像，提升了模型计算的吞吐</font>**<font style="color:rgb(25, 27, 31);">，在性能上始终优于传统的ViT。</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://arxiv.org/pdf/2307.06304](https://arxiv.org/pdf/2307.06304)

**参考：**[**多模态技术梳理：Qwen-VL系列**](https://zhuanlan.zhihu.com/p/25267823390)**  **[**24年下半年较新的VLM架构**](https://zhuanlan.zhihu.com/p/11503653276)

:::

:::color5
**<font style="color:#601BDE;">1.传统ViT 对比 NaViT</font>**

:::

+ **传统的ViT**：将任何图片数据都处理成定长的Patch序列，然后输入给Vision Encoder，这种统一定长的输入是对硬件计算非常友好的，非常好组Batch，并且不需要任何padding处理。Batch序列中每个位置的计算都是有效的。
+ **NaViT的**[**Patch n’ Pack**](https://zhida.zhihu.com/search?content_id=254075742&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)**技术：把不同图像的多个patch打包到一个序列，能保留不同图片的可变分辨率。同时在一个次序列计算中同时可处理多个图像，提升了模型计算的吞吐，在性能上始终优于传统的ViT**。其性能提升主要来源于Pack处理后，一个序列包括多个图片能同时计算，使得在固定计算预算下，动态分辨率方法能训练更多样本，从而带来更好的性能。

:::color5
**<font style="color:#601BDE;">2.处理过程示例</font>**

:::

**<font style="color:rgb(83, 88, 97);">举</font>****例**：假设我们5张图片： I<sub>1</sub>∼I<sub>5</sub> ，且patch长度为： 2∼6 ，即图片Patch后长度为： {I<sub>1</sub>:2, I<sub>2</sub>:3, I<sub>3</sub>:4, I<sub>4</sub>:5 , I<sub>5</sub>:6} 。为了描述简单，我们假设模型设置Batch_Size=2，并且正好处理这5张图片到一个Batch中。

1. **<font style="color:rgb(25, 27, 31);">将5张图片进行Pack，放到2个序列中</font>**

<font style="color:rgb(25, 27, 31);">一个很简单的方式是将3个Patch较短的图片放到一个序列 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);"> ，2个较长Patch的图片放到一个序列 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);"> 。符号化为： </font><font style="color:rgb(25, 27, 31);">Batch={S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">,S</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">}</font><font style="color:rgb(25, 27, 31);"> ，其中 </font><font style="color:rgb(25, 27, 31);">S1={I</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">:2,I</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">:3,I</font><sub><font style="color:rgb(25, 27, 31);">3</font></sub><font style="color:rgb(25, 27, 31);">:4}</font><font style="color:rgb(25, 27, 31);"> 序列长度为 </font><font style="color:rgb(25, 27, 31);">9</font><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">S2={I</font><sub><font style="color:rgb(25, 27, 31);">4</font></sub><font style="color:rgb(25, 27, 31);">:5,I</font><sub><font style="color:rgb(25, 27, 31);">5</font></sub><font style="color:rgb(25, 27, 31);">:6}</font><font style="color:rgb(25, 27, 31);"> 序列长度为 </font><font style="color:rgb(25, 27, 31);">11</font>

2. **<font style="color:rgb(25, 27, 31);">Batch内做序列Padding对齐处理</font>**

<font style="color:rgb(25, 27, 31);">根据Batch内最长序列，通过F.pad方法做序列对齐，在序列前后增加Padding token，该例子中由于 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);"> 较短，需要在末尾增加Padding token，处理后，如下图所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742269727057-53d999b7-845e-4997-a739-f0ae5cf978d3.png)

3. **<font style="color:rgb(25, 27, 31);">通过设置Attention Mask保证同Sequence中各图片计算隔离</font>**

<font style="color:rgb(25, 27, 31);">一个序列中有多张图片输入，在计算时要必须保证各图片的Attention计算是相互隔离的。实现上通过对Attention Mask矩阵做特殊的设置，来保证计算隔离。计算Attention Mask的过程如下：</font>

<font style="color:rgb(25, 27, 31);">首先，记录序列中每个图片起止token位置（包括初始0位置），得到两个位置序列为：</font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s1</font></sub><font style="color:rgb(25, 27, 31);">={0,2,5,9}</font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s2</font></sub><font style="color:rgb(25, 27, 31);">={0,5,11}</font><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">st</font></sub><font style="color:rgb(25, 27, 31);"> 中连续的两个数 </font><font style="color:rgb(25, 27, 31);">(j,k)</font><font style="color:rgb(25, 27, 31);"> 表示一张图片在序列中的长度为 </font><font style="color:rgb(25, 27, 31);">k−j</font><font style="color:rgb(25, 27, 31);"> 个特征，且特征的起止位置为： </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">k−1</font><font style="color:rgb(25, 27, 31);"> 。</font>

<font style="color:rgb(25, 27, 31);">然后，分别用 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s1</font></sub><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s2</font></sub><font style="color:rgb(25, 27, 31);"> 来计算二维Attention mask矩阵，计算方式为：先初始化一个全0的mask矩阵，然后遍历每个 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">st</font></sub><font style="color:rgb(25, 27, 31);">，取 </font><font style="color:rgb(25, 27, 31);">[i,i+1]</font><font style="color:rgb(25, 27, 31);"> 位置的两个数字 </font><font style="color:rgb(25, 27, 31);">(j,k)</font><font style="color:rgb(25, 27, 31);"> ，使得矩阵行列坐标都满足在 </font><font style="color:rgb(25, 27, 31);">[j,k−1]</font><font style="color:rgb(25, 27, 31);"> 区间范围的位置置1。两个序列计算后的Mask矩阵，如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742278208815-33fb8129-af9d-4c4a-bbb3-a0b220e4212a.png)

<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">计算好了上面的Attention Mask矩阵，在过Vision Encoder网络时，</font>**<font style="color:#74B602;">将Attention Mask作用在Attention计算上，就会隔离同一序列中不同图像的Attention计算</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">InternViT</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternViT仍然延用ViT的结构主要由</font>**<font style="color:#74B602;">VisionEmbeddings和VisionEncoder</font>**<font style="color:rgb(25, 27, 31);">两个大模块组成</font>

**paper：**[**https://arxiv.org/pdf/2010.11929**](https://arxiv.org/pdf/2010.11929)

**参考：**[**https://zhuanlan.zhihu.com/p/702481058**](https://zhuanlan.zhihu.com/p/702481058)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742528314276-7f3161f2-a40c-4bb2-ab9e-7f2e51ff721a.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

<font style="color:rgb(25, 27, 31);">InternViT仍然延用ViT的结构主要由</font>**<font style="color:#74B602;">VisionEmbeddings和VisionEncoder</font>**<font style="color:rgb(25, 27, 31);">两个大模块组成，</font>

+ **<font style="color:rgb(25, 27, 31);">VisionEmbeddings：</font>**<font style="color:rgb(25, 27, 31);">负责将图像编码成Embedding，并且position embedding采用了可学习的方式，forward时，会将图像patch embedding和position embedding相加，得到ViT的输入，然后送入VisionEncoder进行推理。</font>
+ **<font style="color:rgb(25, 27, 31);">VisionEncoder</font>**<font style="color:rgb(25, 27, 31);">：中包含多层标准的Transformer层，也就是InternVisionEncoderLayer。</font>

:::color5
**<font style="color:#601BDE;">2.config</font>**

:::

```python
num_channels=3,
patch_size=14,
image_size=224,
qkv_bias=False,
hidden_size=3200,
num_attention_heads=25,
intermediate_size=12800,
qk_normalization=True,
num_hidden_layers=48,
use_flash_attn=True,
hidden_act='gelu',
norm_type='rms_norm',
layer_norm_eps=1e-6,
dropout=0.0,
drop_path_rate=0.0,
attention_dropout=0.0,
initializer_range=0.02,
initializer_factor=0.1,
```

:::color5
**<font style="color:#601BDE;">3.代码实现</font>**

:::

```python
class InternVisionModel(PreTrainedModel):
    main_input_name = 'pixel_values'
    _supports_flash_attn_2 = True
    config_class = InternVisionConfig
    _no_split_modules = ['InternVisionEncoderLayer']

    def __init__(self, config: InternVisionConfig):
        super().__init__(config)
        self.config = config

        self.embeddings = InternVisionEmbeddings(config)
        self.encoder = InternVisionEncoder(config)

    def resize_pos_embeddings(self, old_size, new_size, patch_size):
        pos_emb = self.embeddings.position_embedding
        _, num_positions, embed_dim = pos_emb.shape
        cls_emb = pos_emb[:, :1, :]
        pos_emb = pos_emb[:, 1:, :].reshape(1, old_size // patch_size, old_size // patch_size, -1).permute(0, 3, 1, 2)
        pos_emb = F.interpolate(pos_emb.float(), size=new_size // patch_size, mode='bicubic', align_corners=False)
        pos_emb = pos_emb.to(cls_emb.dtype).reshape(1, embed_dim, -1).permute(0, 2, 1)
        pos_emb = torch.cat([cls_emb, pos_emb], dim=1)
        self.embeddings.position_embedding = nn.Parameter(pos_emb)
        self.embeddings.image_size = new_size
        logger.info('Resized position embeddings from {} to {}'.format(old_size, new_size))

    def get_input_embeddings(self):
        return self.embeddings

    def forward(
            self,
            pixel_values: Optional[torch.FloatTensor] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
            pixel_embeds: Optional[torch.FloatTensor] = None,
    ) -> Union[Tuple, BaseModelOutputWithPooling]:
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if pixel_values is None and pixel_embeds is None:
            raise ValueError('You have to specify pixel_values or pixel_embeds')

        if pixel_embeds is not None:
            hidden_states = pixel_embeds
        else:
            if len(pixel_values.shape) == 4:
                # print("intern vit forward pixel_values dtype:\n", pixel_values.dtype)
                pixel_values=pixel_values.to(torch.bfloat16)
                # print("convert intern vit forward pixel_values dtype:\n", pixel_values.dtype)
                hidden_states = self.embeddings(pixel_values)
            else:
                raise ValueError(f'wrong pixel_values size: {pixel_values.shape}')
        encoder_outputs = self.encoder(
            inputs_embeds=hidden_states,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        last_hidden_state = encoder_outputs.last_hidden_state
        pooled_output = last_hidden_state[:, 0, :]

        if not return_dict:
            return (last_hidden_state, pooled_output) + encoder_outputs[1:]

        return BaseModelOutputWithPooling(
            last_hidden_state=last_hidden_state,
            pooler_output=pooled_output,
            hidden_states=encoder_outputs.hidden_states,
            attentions=encoder_outputs.attentions,
        )

```

##  EVA02
[https://blog.csdn.net/sinat_37574187/article/details/142938184](https://blog.csdn.net/sinat_37574187/article/details/142938184)





##  [LLM2CLIP](https://github.com/microsoft/LLM2CLIP)
[https://github.com/microsoft/LLM2CLIP](https://github.com/microsoft/LLM2CLIP)

<font style="color:rgb(51, 51, 51);">Pre-Training</font>







## MAE
<font style="color:rgb(51, 51, 51);">MAE (Masked Autoencoders Are Scalable Vision Learners) 模型详解</font>

:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">自监督学习需求</font>**<font style="color:rgb(51, 51, 51);">：传统监督学习依赖大量标注数据，成本高昂。自监督学习通过无标注数据预训练模型，提升泛化能力。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">图像掩码重建的启发</font>**<font style="color:rgb(51, 51, 51);">：NLP中BERT通过掩码语言建模（MLM）取得成功，启发视觉领域类似方法（如BEiT）。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">MAE定位</font>**<font style="color:rgb(51, 51, 51);">：何恺明团队提出的掩码自编码器，通过高比例随机掩码图像块并重建，学习高效视觉表示。</font>

:::

<font style="color:rgb(51, 51, 51);">MAE通过高比例掩码和像素级重建任务，推动了视觉自监督学习的发展。其高效的非对称架构设计为大规模预训练提供了新思路，后续工作可通过结合语义约束和多模态对齐进一步提升性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741092698055-73b1eb72-d118-4ca2-b86b-ca188351fcbc.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">非对称编码器-解码器架构</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">轻量编码器</font>**<font style="color:rgb(51, 51, 51);">：仅处理可见图像块（如25%可见），降低计算量。</font>
    - **<font style="color:rgb(51, 51, 51);">独立解码器</font>**<font style="color:rgb(51, 51, 51);">：接收编码特征和掩码标记，重建完整图像。</font>
+ **<font style="color:rgb(51, 51, 51);">高比例随机掩码</font>**<font style="color:rgb(51, 51, 51);">：掩码率高达75%，强制模型学习全局上下文推理。</font>
+ **<font style="color:rgb(51, 51, 51);">像素级重建目标</font>**<font style="color:rgb(51, 51, 51);">：直接预测掩码块的原始像素值，无需离散化或tokenizer。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">无标注图像数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">公开数据集：ImageNet-1K/21K（无需标签）。</font>
    - <font style="color:rgb(51, 51, 51);">大规模网络图片：如JFT-300M（论文中使用）。</font>
+ **<font style="color:rgb(51, 51, 51);">预处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像归一化为224x224分辨率。</font>
    - <font style="color:rgb(51, 51, 51);">随机裁剪、色彩抖动、水平翻转等增强。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741092591257-fda4ef64-936c-4bea-9f44-e6f42de7fca9.png)

+ **<font style="color:rgb(51, 51, 51);">编码器（ViT Backbone）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">输入：未被掩码的图像块（如14x14块，每块16x16像素）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：标准Vision Transformer（ViT-Base/Large/Huge）。</font>
    - <font style="color:rgb(51, 51, 51);">输出：可见块的编码特征。</font>
+ **<font style="color:rgb(51, 51, 51);">解码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">输入：编码特征 + 可学习的掩码标记（mask tokens）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：轻量级Transformer（更少层数，如4层）。</font>
    - <font style="color:rgb(51, 51, 51);">输出：重建的像素值（每个掩码块预测16x16x3像素）。</font>
+ **<font style="color:rgb(51, 51, 51);">掩码策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">随机选择75%的图像块进行掩码，剩余25%作为输入。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **图像分块与掩码**：
    - <font style="color:rgb(51, 51, 51);">将图像分割为不重叠的16x16块。</font>
    - <font style="color:rgb(51, 51, 51);">随机掩码75%的块，仅保留25%输入编码器。</font>
2. **编码器前向**：
    - <font style="color:rgb(51, 51, 51);">对可见块进行线性投影，加入位置编码。</font>
    - <font style="color:rgb(51, 51, 51);">通过ViT提取特征。</font>
3. **解码器重建**：
    - <font style="color:rgb(51, 51, 51);">将编码特征与掩码标记拼接，加入位置编码。</font>
    - <font style="color:rgb(51, 51, 51);">解码器输出每个掩码块的像素值。</font>
4. **损失计算**：
    - <font style="color:rgb(51, 51, 51);">均方误差（MSE）损失：比较重建像素与原始像素。</font>
    - <font style="color:rgb(51, 51, 51);">仅对掩码块计算损失。</font>
5. **微调**：
    - <font style="color:rgb(51, 51, 51);">预训练后，移除解码器，在编码器后添加任务头（分类、检测等）。</font>
    - <font style="color:rgb(51, 51, 51);">使用少量标注数据微调。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">训练高效：编码器仅处理部分图像块，计算量减少约75%。</font>
+ <font style="color:rgb(51, 51, 51);">泛化能力强：高掩码率迫使模型学习全局语义。</font>
+ <font style="color:rgb(51, 51, 51);">兼容下游任务：预训练模型可迁移至分类、检测、分割等任务。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">像素级重建对高频细节敏感，可能导致过拟合噪声。</font>
+ <font style="color:rgb(51, 51, 51);">重建任务与高层语义任务的优化目标不完全一致。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">：微调编码器作为特征提取器。</font>
+ **<font style="color:rgb(51, 51, 51);">目标检测</font>**<font style="color:rgb(51, 51, 51);">：预训练模型作为检测主干网络（如Mask R-CNN）。</font>
+ **<font style="color:rgb(51, 51, 51);">语义分割</font>**<font style="color:rgb(51, 51, 51);">：输出密集特征图用于像素级预测。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：利用重建能力生成图像变体。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多任务学习</font>**<font style="color:rgb(51, 51, 51);">：结合对比损失（如SimCLR）提升特征判别性。</font>
+ **<font style="color:rgb(51, 51, 51);">多尺度掩码</font>**<font style="color:rgb(51, 51, 51);">：混合不同块大小掩码（如16x16与32x32）。</font>
+ **<font style="color:rgb(51, 51, 51);">语义感知重建</font>**<font style="color:rgb(51, 51, 51);">：引入CLIP等模型约束高层语义一致性。</font>
+ **<font style="color:rgb(51, 51, 51);">动态掩码率</font>**<font style="color:rgb(51, 51, 51);">：根据图像内容自适应调整掩码比例。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class MAE(nn.Module):
    def __init__(self, encoder, decoder, mask_ratio=0.75):
        super().__init__()
        self.encoder = encoder  # ViT编码器
        self.decoder = decoder  # 轻量Transformer解码器
        self.mask_ratio = mask_ratio
        self.patch_size = 16
        self.embed_dim = encoder.embed_dim

        # 可学习的掩码标记
        self.mask_token = nn.Parameter(torch.randn(1, 1, self.embed_dim))

    def random_masking(self, x):
        N, L, D = x.shape  # L = (224/16)^2 = 196
        len_keep = int(L * (1 - self.mask_ratio))
        
        # 随机选择保留的索引
        ids_keep = torch.multinomial(torch.ones(L), len_keep, replacement=False)
        ids_mask = torch.ones(L, dtype=torch.bool)
        ids_mask[ids_keep] = False
        
        # 分离可见块与掩码块
        x_visible = x[:, ~ids_mask, :]
        return x_visible, ids_mask

    def forward(self, imgs):
        # 图像分块并嵌入
        patches = rearrange(imgs, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', 
                            p1=self.patch_size, p2=self.patch_size)
        x = self.encoder.patch_embed(patches)  # [B, L, D]
        
        # 随机掩码
        x_visible, mask = self.random_masking(x)
        
        # 编码器处理可见块
        x_encoded = self.encoder(x_visible, mask=None)  # [B, len_keep, D]
        
        # 解码器输入：编码特征 + 掩码标记
        B, L = x.shape[:2]
        mask_tokens = self.mask_token.repeat(B, L - x_visible.shape[1], 1)
        x_full = torch.cat([x_encoded, mask_tokens], dim=1)
        x_decoded = self.decoder(x_full)  # [B, L, D]
        
        # 重建像素
        pred_pixels = self.decoder.to_pixels(x_decoded)  # [B, L, 16*16*3]
        return pred_pixels, mask

# 示例调用
class ViTEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.patch_embed = nn.Linear(16*16*3, 768)
        self.blocks = nn.TransformerEncoderLayer(d_model=768, nhead=12)
    
    def forward(self, x, mask):
        return self.blocks(x)

class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.TransformerDecoderLayer(d_model=768, nhead=12)
        self.to_pixels = nn.Linear(768, 16*16*3)
    
    def forward(self, x):
        return self.to_pixels(self.layers(x))

encoder = ViTEncoder()
decoder = Decoder()
model = MAE(encoder, decoder, mask_ratio=0.75)

# 训练循环
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
for imgs in dataloader:
    pred_pixels, mask = model(imgs)
    loss = ((pred_pixels - imgs)**2).mean(dim=-1)[mask].mean()
    loss.backward()
    optimizer.step()

```



