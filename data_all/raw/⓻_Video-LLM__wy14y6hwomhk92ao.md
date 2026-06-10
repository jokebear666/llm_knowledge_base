# ⓻ Video-LLM

<!-- source: yuque://zhongxian-iiot9/hlyypb/wy14y6hwomhk92ao -->

# Video-LLM
## InternVideo2.5<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">尽管MLLM在许多任务中表现出色，但在处理视觉相关任务时，仍然难以与人类的表现相媲美。特别是在识别、定位和回忆常见场景中的物体、场景和动作时，MLLM常常表现出困难。尽管研究表明，通过增加视觉相关数据和模型规模，可以在多模态理解基准上取得持续的改进，但这并没有为MLLM实现人类水平的视觉理解提供一个明确的时间表。</font>

:::

:::color3
**简介：****<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">探讨了多模态上下文的长度和细粒度如何影响MLLM的视觉能力和性能。具体来说，我们通过引入长且丰富的上下文（LRC）建模，开发了</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">，旨在增强MLLM对视频中细粒度细节的感知能力，并捕捉长时态结构。实验结果表明，这种独特的设计显著提高了MLLM在主流视频理解基准（短视频和长视频）上的表现，使其能够处理比原始模型长至少6倍的视频输入，并掌握如目标跟踪和分割等专业视觉能力。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/OpenGVLab/InternVideo/tree/main/InternVideo2.5](https://github.com/OpenGVLab/InternVideo/tree/main/InternVideo2.5)

**paper：**[**https://arxiv.org/pdf/2501.12386**](https://arxiv.org/pdf/2501.12386)

**参考：**[**InternVideo2.5：让视频多模态大模型“看得更远、看得更细”**](https://zhuanlan.zhihu.com/p/19872979806)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743661130704-55d0bc71-aaab-445d-9f66-4cbe0b3c9da2.png)

:::color5
**<font style="color:#601BDE;">1.长上下文建模</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了实现对长视频的准确理解，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">通过引入</font>**<font style="color:#74B602;">长且丰富的上下文（LRC）建模</font>**<font style="color:rgb(25, 27, 31);">，显著提升了多模态大语言模型（MLLM）的感知和理解能力。具体来说，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">通过</font>**<font style="color:#74B602;">视频长度自适应的token表示和任务偏好优化，增强了MLLM的上下文长度和细粒度</font>**<font style="color:rgb(25, 27, 31);">。整个模型的训练分为三个阶段，分别利用</font>**<font style="color:#74B602;">短视频、长视频数据以及经典视觉任务数据。</font>**

:::color5
**<font style="color:#601BDE;">2.视频长度自适应的token表示</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了高效处理任意长度的视频序列，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">引入了一种实用的</font>**<font style="color:#74B602;">长度自适应token表示方法</font>**<font style="color:rgb(25, 27, 31);">。该方法基于典型的MLLM架构，包括视觉编码器、</font>[<font style="color:rgb(9, 64, 142);">视觉-语言连接器</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89-%E8%AF%AD%E8%A8%80%E8%BF%9E%E6%8E%A5%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和语言模型。在动态帧采样后，模型通过分层token压缩（</font>[<font style="color:rgb(9, 64, 142);">HiCo</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=HiCo&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）实现了对长视频的高效处理。HiCo分为两个阶段：视觉编码期间的时空感知压缩和语言模型处理期间的自适应多模态上下文整合。</font>

+ **<font style="color:rgb(25, 27, 31);">自适应时间采样</font>**<font style="color:rgb(25, 27, 31);">：为了适应不同长度的视频，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">采用了一种上下文感知的采样机制。对于较短的视频序列，模型采用</font>**<font style="color:#74B602;">密集时间采样（每秒15帧）</font>**<font style="color:rgb(25, 27, 31);">，以确保捕捉到关键的运动细节；而对于较长的视频序列（如分钟或小时级别的视频），模型则采用</font>**<font style="color:#74B602;">稀疏采样（每秒1帧）</font>**<font style="color:rgb(25, 27, 31);">，以专注于事件级别的理解。这种自适应采样机制确保了模型在不同时间尺度上都能有效捕捉视频内容。</font>
+ **<font style="color:rgb(25, 27, 31);">分层token压缩</font>**<font style="color:rgb(25, 27, 31);">：为了</font>**<font style="color:#74B602;">减少长视频中的冗余信息</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">通过事件中的时空冗余和事件之间的语义冗余来压缩视觉信号。具体来说，模型采用了两种压缩策略：</font>
    - **<font style="color:rgb(25, 27, 31);">时空token合并</font>**<font style="color:rgb(25, 27, 31);">：通过语义相似性进行token合并，保留视频中的关键信息。实验表明，基于语义相似性的token合并方法（如</font>[<font style="color:rgb(9, 64, 142);">ToMe</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=ToMe&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）在视觉压缩中表现出色，能够在保留细节的同时显著减少计算开销。</font>
    - **<font style="color:rgb(25, 27, 31);">多模态token丢弃</font>**<font style="color:rgb(25, 27, 31);">：在语言模型处理过程中，模型通过两阶段的token丢弃策略进一步优化长距离视觉理解。首先，在早期层进行均匀token剪枝，以减少计算开销；其次，在深层通过注意力引导的token选择，保留与任务相关的关键信息。</font>

:::color5
**<font style="color:#601BDE;">3.通过任务偏好优化增强多模态上下文中的视觉精度</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了增强MLLM在细粒度视觉任务中的表现，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">引入了</font>**<font style="color:#74B602;">多任务偏好学习</font>**<font style="color:rgb(25, 27, 31);">（</font>[<font style="color:rgb(9, 64, 142);">MPL</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=MPL&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）。该方法通过将专门的视觉感知模块与基础MLLM架构集成，实现了精确的定位和时间理解等能力。</font>

+ **<font style="color:rgb(25, 27, 31);">时间理解</font>**<font style="color:rgb(25, 27, 31);">：为了处理动态视觉内容，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">开发了一个</font>**<font style="color:#74B602;">时间组件，结合视频特征提取和时间对齐能力</font>**<font style="color:rgb(25, 27, 31);">。该组件能够预测精确的时间边界和相关分数，从而帮助模型更好地理解视频中的时间关系。</font>
+ **<font style="color:rgb(25, 27, 31);">实例分割</font>**<font style="color:rgb(25, 27, 31);">：为了实现像素级理解和实例级区分，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">设计了一个分割模块，基于最新的分割基础模型（如SAM2）。该模块通过自适应投影层将</font>**<font style="color:#74B602;">MLLM的嵌入与像素级预测连接起来，从而实现了对视频中目标的精确分割。</font>**

<font style="color:rgb(25, 27, 31);">通过多任务偏好优化，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">不仅提升了MLLM在视觉任务中的表现，还保持了其在通用任务中的能力。具体来说，模型通过联合优化视觉感知模块和基础MLLM，实现了对细粒度视觉任务的精确处理。</font>

:::color5
**<font style="color:#601BDE;">4.多模态上下文建模的训练视频语料库</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743661829814-9e383713-deab-4a6c-bc6d-2b09c79f689a.png)

**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">构建了一个包含</font>**<font style="color:#74B602;">视觉-文本对齐数据、长视频数据和任务特定视觉数据</font>**<font style="color:rgb(25, 27, 31);">的训练语料库。训练过程分为三个阶段，逐步增强模型的细粒度感知和时间理解能力。</font>

+ **<font style="color:rgb(25, 27, 31);">视觉-文本数据</font>**<font style="color:rgb(25, 27, 31);">：我们收集了数百万的图像-文本对和视频-文本对，用于模型的跨模态对齐训练。具体来说，我们使用了来自</font>[<font style="color:rgb(9, 64, 142);">COCO</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=COCO&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">BLIP</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=BLIP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">CC3M</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=CC3M&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等数据集的图像-文本对，以及来自</font>[<font style="color:rgb(9, 64, 142);">WebVid</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=WebVid&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">Kinetics</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=Kinetics&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等数据集的视频-文本对。这些数据经过重新标注，以确保其与模型的训练目标一致。</font>
+ **<font style="color:rgb(25, 27, 31);">长视频语料库</font>**<font style="color:rgb(25, 27, 31);">：为了增强模型对长视频的理解能力，我们使用了来自</font>[<font style="color:rgb(9, 64, 142);">MoiveChat</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=MoiveChat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">Cinepile</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=Cinepile&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、Vript和LongVid的长视频指令数据。特别是LongVid数据集，包含了114,228个长视频和3,444,849个问答对，涵盖了多种长视频场景。</font>
+ **<font style="color:rgb(25, 27, 31);">任务特定数据</font>**<font style="color:rgb(25, 27, 31);">：为了提升模型在特定视觉任务中的表现，我们使用了多个经典视觉任务数据集，如</font>[<font style="color:rgb(9, 64, 142);">DiDeMo</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=DiDeMo&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">QuerYD</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=QuerYD&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">RefCOCO</font>](https://zhida.zhihu.com/search?content_id=252996925&content_type=Article&match_order=1&q=RefCOCO&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等。这些数据集涵盖了</font>**<font style="color:#74B602;">时间定位、空间定位、分割等任务，帮助模型掌握精确的视觉分析能力。</font>**

:::color5
**<font style="color:#601BDE;">5.渐进式多阶段训练</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了逐步增强模型的细粒度感知和时间理解能力，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">采用了</font>**<font style="color:#74B602;">渐进式多阶段训练策略。训练分为三个阶段：</font>**

+ **<font style="color:rgb(25, 27, 31);">阶段1：基础学习</font>**<font style="color:rgb(25, 27, 31);">：在这一阶段，模型通过任务识别指令调优和视频-语言对齐训练，建立了基本的视觉-语言连接。我们使用了50万图像-文本对和50万短视频-文本对进行训练。</font>
+ **<font style="color:rgb(25, 27, 31);">阶段2：细粒度感知训练</font>**<font style="color:rgb(25, 27, 31);">：在这一阶段，模型通过集成和训练任务特定组件（如任务令牌、区域头、时间头和掩码适配器），增强了其视觉理解能力。我们使用了350万图像和250万短视频-文本对进行视觉概念预训练。</font>
+ **<font style="color:rgb(25, 27, 31);">阶段3：集成准确和长上下文训练</font>**<font style="color:rgb(25, 27, 31);">：在最后阶段，模型通过多任务训练和指令调优，联合优化了所有组件。我们使用了350万样本进行训练，其中包括110万图像、170万短视频和70万长视频。</font>

<font style="color:rgb(25, 27, 31);">通过这种渐进式训练策略，</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">不仅提升了其在细粒度视觉任务中的表现，还增强了对长视频的理解能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743661913277-e247a1de-3f27-4921-9fad-1ff3957d4777.png)

:::color5
**<font style="color:#601BDE;">6.局限性</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">尽管</font>**<font style="color:rgb(25, 27, 31);">InternVideo2.5</font>**<font style="color:rgb(25, 27, 31);">在长视频序列上展示了改进的性能，但处理这种扩展上下文的计算成本仍然很高。未来的研究需要探索更高效的学习技术以减少这一开销。此外，当前的实现主要集中在视觉上下文属性上，扩展LRC到推理相关领域是一个有希望的研究方向。</font>



## Video-LLAMA（阿里）
:::color3
**简介：Video-LLAMA**<font style="color:rgb(25, 27, 31);">使LLM能理解视频中的视觉和听觉内容，需要对不同模态进行综合处理，因此文中构建了一个端到端模型，可以在单一框架内处理来自多个模态的数据，允许用户上传视频并进行对话。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/damo-nlp-sg/video-llama](https://github.com/damo-nlp-sg/video-llama)

**paper：**[**https://arxiv.org/pdf/2306.02858**](https://arxiv.org/pdf/2306.02858)

**参考：**[**https://zhuanlan.zhihu.com/p/706552198**](https://zhuanlan.zhihu.com/p/706552198)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743667793352-9badfbaa-102e-46f3-8fe1-b505ded0be23.png)

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**

:::

[<font style="color:rgb(9, 64, 142);">Video-Llama</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=Video-Llama&zhida_source=entity)<font style="color:rgb(25, 27, 31);">旨在使冻结的LLM能够理解视频中的视觉和听觉内容，模型主要有两个branch，visual和audio，分别用于转换两个模态的输入。</font>

1. **<font style="color:rgb(25, 27, 31);">Vision-Language Branch</font>**
+ <font style="color:rgb(25, 27, 31);">目的：使LLM能够理解视觉输入</font>
+ <font style="color:rgb(25, 27, 31);">组成：</font>
    - <font style="color:rgb(25, 27, 31);">视觉编码器</font>
        * <font style="color:rgb(25, 27, 31);">用于提取video frames的特征</font>
        * <font style="color:rgb(25, 27, 31);">pretrain的BLIP2初始化</font>
        * <font style="color:rgb(25, 27, 31);">冻结参数</font>
        * <font style="color:rgb(25, 27, 31);">ViT-G/14 (来自EVA-CLIP)  和预训练的Q-former</font>
    - <font style="color:rgb(25, 27, 31);">位置嵌入层</font>
        * <font style="color:rgb(25, 27, 31);">引入时间信息</font>
    - [<font style="color:rgb(9, 64, 142);">video Q-former</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=video+Q-former&zhida_source=entity)
        * <font style="color:rgb(25, 27, 31);">聚合帧级别的特征表示</font>
        * <font style="color:rgb(25, 27, 31);">这里是为了将不同帧的信息做一个聚合，并生成固定长度得特征</font>
    - <font style="color:rgb(25, 27, 31);">线性层</font>
        * <font style="color:rgb(25, 27, 31);">转换维度，映射特征空间到LLM中</font>
2. **<font style="color:rgb(25, 27, 31);">Audio-Language Branch</font>**
+ <font style="color:rgb(25, 27, 31);">目的：理解视频种的语音部分</font>
+ <font style="color:rgb(25, 27, 31);">组成：</font>
    - <font style="color:rgb(25, 27, 31);">音频编码器</font>
        * <font style="color:rgb(25, 27, 31);">用于提取音频特征</font>
        * <font style="color:rgb(25, 27, 31);">pretrain ImageBind</font>
    - <font style="color:rgb(25, 27, 31);">位置嵌入层</font>
        * <font style="color:rgb(25, 27, 31);">引入时间信息</font>
    - [<font style="color:rgb(9, 64, 142);">audio Q-former</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=audio+Q-former&zhida_source=entity)
        * <font style="color:rgb(25, 27, 31);">这里是为了将整合不同音频片段的信息，并生成固定长度得特征</font>
    - <font style="color:rgb(25, 27, 31);">线性层</font>
        * <font style="color:rgb(25, 27, 31);">转换维度，映射特征空间到LLM中</font>
+ <font style="color:rgb(25, 27, 31);">方法：</font>
    - <font style="color:rgb(25, 27, 31);">从视频中均匀地采样M个2秒短音频片段，然后使用128个MEL bin转换成时频谱</font>

:::color5
**<font style="color:#601BDE;">2.训练方法</font>**

:::

<font style="color:rgb(25, 27, 31);">分别对两个branch进行训练，共两阶段</font>

1. **<font style="color:rgb(25, 27, 31);">Training of Vision-Language Branch  视觉语言训练</font>**

<font style="color:rgb(25, 27, 31);">两阶段，pretrain和instruction tuning</font>

**<font style="color:rgb(25, 27, 31);">预训练</font>**

+ <font style="color:rgb(25, 27, 31);">目的：使用大量数据让video encoder获取视频知识</font>
+ <font style="color:rgb(25, 27, 31);">数据：</font>
    - [<font style="color:rgb(9, 64, 142);">Webvid-2M</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=Webvid-2M&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（大规模的短视频数据集，具有文本描述）</font>
    - [<font style="color:rgb(9, 64, 142);">CC595k</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=CC595k&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：image caption dataset</font>
+ <font style="color:rgb(25, 27, 31);">方法：</font>
    - <font style="color:rgb(25, 27, 31);">使用video2text任务</font>
+ <font style="color:rgb(25, 27, 31);">该阶段很多数据比较noisy，但主要目的是让video encoder获取视频知识，对齐和instruction在下一阶段调整</font>

**<font style="color:rgb(25, 27, 31);">指令微调</font>**

+ <font style="color:rgb(25, 27, 31);">目的：增强instruction能力，理解video内容</font>
+ <font style="color:rgb(25, 27, 31);">数据：</font>
    - <font style="color:rgb(25, 27, 31);">高质量数据</font>
    - <font style="color:rgb(25, 27, 31);">image-detail-description dataset from</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">MiniGPT4</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=MiniGPT4&zhida_source=entity)
    - <font style="color:rgb(25, 27, 31);">image-instruction dataset from LLaVA</font>
    - <font style="color:rgb(25, 27, 31);">video-instruction dataset from</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Video-Chat</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=Video-Chat&zhida_source=entity)
2. **<font style="color:rgb(25, 27, 31);">Training of Audio-Language Branch  音频语言训练</font>**

<font style="color:rgb(25, 27, 31);">这里看有些讲解说是只进行了instruction tuning，但我在原文中没找到相关描述</font>

+ <font style="color:rgb(25, 27, 31);">难点：audio-text数据的稀缺性导致很难只使用该类型数据对audio branch进行训练</font>
+ <font style="color:rgb(25, 27, 31);">方法：imagebind将多个模态得特征空间转换到公共空间，所以使用丰富的visual-text数据对该分支进行训练，训练方法和vision branch相同</font>
+ <font style="color:rgb(25, 27, 31);">数据：数据和vision branch使用数据相同</font>
+ <font style="color:rgb(25, 27, 31);">即使没有使用audio 数据进行训练，但是Video-</font>[<font style="color:rgb(9, 64, 142);">LLaMA</font>](https://zhida.zhihu.com/search?content_id=245142694&content_type=Article&match_order=1&q=LLaMA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在推理过程中仍可以理解音频</font>



## Video-LLAMA2（阿里）
:::color3
**简介：**_**<font style="color:rgb(25, 27, 31);">VideoLLaMA2</font>**_<font style="color:rgb(25, 27, 31);"> 是一个旨在提升视频大语言模型(Video-LLM)时空建模和音频理解能力的项目。该模型集成了一个专门设计的</font>[<font style="color:rgb(9, 64, 142);">时空卷积</font>](https://zhida.zhihu.com/search?content_id=244791807&content_type=Article&match_order=1&q=%E6%97%B6%E7%A9%BA%E5%8D%B7%E7%A7%AF&zhida_source=entity)<font style="color:rgb(25, 27, 31);">(Spatial-Temporal Convolution，STC)连接器，有效捕捉视频数据中的复杂时空动态。此外，通过联合训练，模型还集成了音频分支，增强了多模态理解能力。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/DAMO-NLP-SG/VideoLLaMA2](https://github.com/DAMO-NLP-SG/VideoLLaMA2)

**paper：**[**https://arxiv.org/pdf/2406.07476**](https://arxiv.org/pdf/2406.07476)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743670052108-86e3592f-f788-4665-afad-609dacbbe866.png)

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**

:::

**<font style="color:rgb(25, 27, 31);">两个分支都独立运行，</font>**<font style="color:rgb(25, 27, 31);">以模块化方式将预先训练的视觉和音频编码器连接到经过指令微调的大型语言模型。视觉和音频分支的这种特定于模态的独立性，以及仅在功能强大的语言模型中发生的跨模态交互，不仅可以通过保持单个模态输入的完整性来简化训练，而且还有助于未来的扩展和调整。</font>

**<font style="color:rgb(25, 27, 31);">对于视觉语言分支，</font>**<font style="color:rgb(25, 27, 31);">视频帧被逐帧编码为特征，通过 STC 连接器进行处理，然后将这些特征输入到大语言模型中，以根据文本提示生成响应。</font>

**<font style="color:rgb(25, 27, 31);">对于音频语言分支，</font>**<font style="color:rgb(25, 27, 31);">音频信号首先被转换为对数 mel 频谱图，然后对其进行编码以提取听觉特征。然后通过多层感知器 （MLP） 模块处理这些特征，以使音频模态与大语言模型保持一致。</font>

:::color5
**<font style="color:#601BDE;">2.STC Connector (Spatial-Temporal Convolution connector)</font>**

:::

视频帧首先被逐帧编码为特征，然后通过提出的STC连接器（两个空间交互模块和一个时空聚合模块）进行处理。我们采用RegStage实现“空间交互”，采用3D卷积实现“时空聚合”。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743670079998-6c7c98cb-cb4e-45b0-8bf2-6e560641dd80.png)



## Video-LLAVA （北大）
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">前人实现多模态的工作思路：</font>

1. <font style="color:rgb(25, 27, 31);">使用LLM作为控制者并利用现有的多模式模型作为工具。当收到用户的文本指令时，LLM会识别用户的意图并决定调用哪些工具。 然后，它通过合并从这些现成的多模态模型获得的结果来生成综合响应，包括HuggingGPT和 AudioGPT。</font>
2. <font style="color:rgb(25, 27, 31);">侧重于训练大规模多模态模型，通过预训练视觉或语音基础模型，来实现其他模态与LLM的文本</font>_<u><font style="color:rgb(25, 27, 31);">对齐</font></u>_<font style="color:rgb(25, 27, 31);">，以实现多模态理解，比如Flamingo，BLIP2，MiniGPT4，Video-Chat 和 Video-ChatGPT。。</font>

<font style="color:rgb(25, 27, 31);">缺点：些方法致力于将来自一种其他模态的输入与文本（即图像或音频）对齐，这对于视频理解来说并不令人满意（注：因为视频理解需要同时处理图片和声音）。 具体来说，让LLM理解视频需要对视觉输入、听觉输入和文本输出等不同模态进行综合处理，这比仅图像理解和仅音频理解任务更具挑战性。 尽管最近有几项工作试图LLM的视频理解能力，但他们的主要目标是仅理解视频的视觉内容，听觉内容未采用。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">根据对其他LVLM模型的分析，Video-LLAVA认为统一的特征空间有利于增强LLM的多模态推理能力。 所以Video-LLaVA</font>**<font style="color:#ED740C;">不仅预先对齐（pre-aligns）图像和视频特征，而且还进行图像和视频的联合训练</font>**<font style="color:rgb(25, 27, 31);">，促进LLM从统一的视觉表示中学习多模态推理能力。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/PKU-YuanGroup/Video-LLaVA](https://github.com/PKU-YuanGroup/Video-LLaVA)

**paper：**[**https://arxiv.org/pdf/2311.10122**](https://arxiv.org/pdf/2311.10122)

**参考：**[**https://zhuanlan.zhihu.com/p/685590423**](https://zhuanlan.zhihu.com/p/685590423)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743668154640-24242f3a-5269-49f9-8079-1e3e971c4374.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743668103979-2f87b08f-d31e-49b8-b18b-51325869de01.png)

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ 第一阶段：数据集由单轮对话组成，侧重于简洁的视觉描述。
+ 第二阶段：数据集包括多回合对话，强调复杂的视觉推理能力。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743668171390-37318e02-2501-45cc-a061-e435ce413b9d.png)

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">整体的网络结构包含4个部分:</font>

+ <font style="color:rgb(25, 27, 31);">f</font><sub><font style="color:rgb(25, 27, 31);">v</font></sub><font style="color:rgb(25, 27, 31);">：LanguageBind encoders，从原始的视觉信号（图片或者视频）中提取特征，LanguageBind 编码器能够将不同的模态映射到文本特征空间，从而提供统一的视觉表示</font>
+ <font style="color:rgb(25, 27, 31);">f</font><sub><font style="color:rgb(25, 27, 31);">L</font></sub><font style="color:rgb(25, 27, 31);">：LLM模型，作者本文使用的是</font>[<font style="color:rgb(9, 64, 142);">Vicuna-7B v1.5</font>](https://zhida.zhihu.com/search?content_id=240483592&content_type=Article&match_order=1&q=Vicuna-7B+v1.5&zhida_source=entity)
+ <font style="color:rgb(25, 27, 31);">f</font><sub><font style="color:rgb(25, 27, 31);">p</font></sub><font style="color:rgb(25, 27, 31);">：视觉投影层，视觉投影层，由两个fully connected layers组成。</font>
+ <font style="color:rgb(25, 27, 31);">f</font><sub><font style="color:rgb(25, 27, 31);">w</font></sub><font style="color:rgb(25, 27, 31);">：文本编码层，这里的tokenizer文中使用的是LLaMA中的tokenizer，大约有 32,000 个类。</font>

<font style="color:rgb(25, 27, 31);">整体的流程是：先通过</font><font style="color:rgb(25, 27, 31);">f</font><font style="color:rgb(25, 27, 31);">v</font><font style="color:rgb(25, 27, 31);">获取到统一的视觉表示，然后经过共享的</font><font style="color:rgb(25, 27, 31);">f</font><font style="color:rgb(25, 27, 31);">L</font><font style="color:rgb(25, 27, 31);">进行编码，然后和tokenized textual queries合并输入到LLM中。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743668154640-24242f3a-5269-49f9-8079-1e3e971c4374.png)

:::color5
**<font style="color:#601BDE;">3.LanguageBind多模态统一表征</font>**

:::

**<font style="color:rgb(25, 27, 31);">United Visual Representation</font>**<font style="color:rgb(25, 27, 31);">：统一的视觉表示目标是将图像和视频映射到共享的特征空间中，以使LLM能够从统一的视觉表示中学习。 例如：奔跑的狗可以同时通过语言、图像或视频来表达。这里作者使用的是LanguageBind，LanguageBind是一种多模态预训练方法，旨在对齐不同模态的语义。</font>

+ <font style="color:rgb(25, 27, 31);">LanguageBind是</font>**<font style="color:#74B602;">通过不同的编码器对各种模态进行编码，比如video使用</font>**[**<font style="color:#74B602;">CLIP4Clip</font>**](https://zhida.zhihu.com/search?content_id=240483592&content_type=Article&match_order=1&q=CLIP4Clip&zhida_source=entity)**<font style="color:#74B602;">，其他模态使用transformer</font>**<font style="color:rgb(25, 27, 31);">（文本是有text transformer，其他使用vision transformer）</font>
+ <font style="color:rgb(25, 27, 31);">利用对比学习将各个模态与语言绑定起来，也就是以语言为基础，其他模态的表示都往语言上靠</font>

**<font style="color:rgb(25, 27, 31);">Alignment Before Projection</font>**<font style="color:rgb(25, 27, 31);">：这里作者使用的video encoder和image encoder是由LanguageBind初始化而来，本身已经是对齐的特征表示。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743670554394-c61d768e-c0b8-4ddc-b73f-84ea0fe50c98.png)

1. **<font style="color:rgb(25, 27, 31);">Understanding Training</font>**

<font style="color:rgb(25, 27, 31);">在这个阶段，模型需要从大量的image/video-text pair数据中学习到解释视觉信号的能力。=这个阶段只有share projection参与训练，其他模型参数都固定住。给定caption，通过自回归损失，使得获得视觉理解能力。</font>

+ <font style="color:rgb(25, 27, 31);">conversation data用</font><font style="color:rgb(25, 27, 31);">(X</font><sub><font style="color:rgb(25, 27, 31);">q</font></sub><font style="color:rgb(25, 27, 31);">,X</font><sub><font style="color:rgb(25, 27, 31);">a</font></sub><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);">表示，其中</font><font style="color:rgb(25, 27, 31);">X</font><sub><font style="color:rgb(25, 27, 31);">T</font></sub><font style="color:rgb(25, 27, 31);">=X</font><sub><font style="color:rgb(25, 27, 31);">q</font></sub><font style="color:rgb(25, 27, 31);">，</font><font style="color:rgb(25, 27, 31);">Xa</font><font style="color:rgb(25, 27, 31);">是GT</font>
+ <font style="color:rgb(25, 27, 31);">该阶段使用的数据来自：</font>
    - <font style="color:rgb(25, 27, 31);">image-text pairs来自558K LAION-CC- SBU，由BLIP 标注的caption</font>
    - <font style="color:rgb(25, 27, 31);">video-text pairs来自</font>[<font style="color:rgb(9, 64, 142);">Valley</font>](https://zhida.zhihu.com/search?content_id=240483592&content_type=Article&match_order=1&q=Valley&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的子集，共702K个pair</font>
2. **<font style="color:rgb(25, 27, 31);">Instruction Tuning</font>**

<font style="color:rgb(25, 27, 31);">在这个阶段，模型需要提供不同instructions对应的响应。 这些instructions通常涉及更复杂的视觉理解任务，而不仅仅是描述视觉信号。此阶段之后，模型学习根据不同的指令和请求生成相应的响应。 LLM也参与了这一阶段的训练。</font>

+ <font style="color:rgb(25, 27, 31);">conversation data用</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743670654764-39e67659-ce77-4da5-b10b-fc882cb90caf.png)<font style="color:rgb(25, 27, 31);">表示，由此组成多轮的数据：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743670663258-28287d1c-ca94-484d-a460-2161e74457ac.png)<font style="color:rgb(25, 27, 31);">，</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">表示的是轮数（回合数）。可以发现，当 </font><font style="color:rgb(25, 27, 31);">r>1</font><font style="color:rgb(25, 27, 31);">的时候，需要把之前的对话和当前轮数的instruction连接在一起作为本轮的输入</font>
+ <font style="color:rgb(25, 27, 31);">该阶段使用的数据集：</font>
    - <font style="color:rgb(25, 27, 31);">来自LLaVA v1.5的665k image-text instruction dataset</font>
    - <font style="color:rgb(25, 27, 31);">来自</font>[<font style="color:rgb(9, 64, 142);">Video-ChatGPT</font>](https://zhida.zhihu.com/search?content_id=240483592&content_type=Article&match_order=1&q=Video-ChatGPT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的100k video-text instruction dataset</font>
3. **训练细节**

在训练过程中，我们调整和裁剪每张图像的大小，得到每张处理过的图像的大小为224×224。**<font style="color:#74B602;">我们从每个视频中均匀采样8帧</font>**，每帧都经过图像预处理。每批数据都是图像和视频的随机组合。

+ 在第一阶段，我们使用具有余弦学习率调度的AdamW优化器，对一个批大小为256的历元进行训练。
+ 在第二阶段，我们将批大小减少到128。两个阶段的初始学习率都设置为1e-3，预热比为0.03。

:::color5
**<font style="color:#601BDE;">5.评测</font>**

:::

<font style="color:rgb(25, 27, 31);"> 	视频理解的评估流程遵循 Video-ChatGPT，使用 GPT-Assistant 进行评估。在四个数据集上均超过了目前最先进的Video-ChatGPT。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743668334240-d1cd8478-2168-4aeb-b4a4-78827ea00a14.png)

## <font style="color:rgb(25, 27, 31);">Momentor</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. 现存的video-LLM大多捕获coarse-grained【一般是在video-level captioning and QA task上进行训练，具备指令遵循能力】，这一点上作者着重放在了Lack of effective temporal representation上； 

2. 现存的video-LLM对segment-level理解存在弱点，**<font style="color:#74B602;">仅仅捕获了global feature</font>**【因为一般的video-LLM的训练语料都是时间很短的视频，因此很难获得segment-level的理解能力】

:::

:::color3
**简介：《**<font style="color:rgb(25, 27, 31);">Momentor: Advancing Video Large Language Model with Fine-Grained Temporal Reasoning</font>**》**

**参考：**[**https://www.zhihu.com/question/626796690/answer/3584553322**](https://www.zhihu.com/question/626796690/answer/3584553322)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921203203-744c7cf8-2c9a-4956-a6be-af7ccfb2176d.png)

:::color5
**<font style="color:#601BDE;">1.PipeLine</font>**

:::

1. 利用Frame encoder来编码frame-level feature，这里是利用frame encoder编码由均匀分布选出来的frame，这里对应的timestamps和TPM中sample的N-1个segment对应的时间节点应该不是一样的
2. 利用Temporal Perception Module (TPM) 来编码时序信息，将其映射到continuous temporal token space后同frame-level feature进行融合；最后经过Linear projection后输入到LLM进行生成。

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

作者介绍了现存的video-llm数据集时间很短，很难建立event-level的理解能力，于是利用自动的生成引擎去构建一个新的数据集。

1. **Structured Information Extraction:**

利用Event Boundary Detection algorithm来检测event boundary，然后基于此构建Instance-Event matrix以结构化的方式组织视觉信息。**Event Boundary Detection**: 

（1）首先从video中sample frame并用**<font style="color:#74B602;">Grounding DINO来提取这些frame中的instance信息</font>**，最后对cross-frame中的Instance信息进行合并，于是获得了spatio-temporal trajectory即instance tracking，这展示了随着时间变化的动态的instance track；

（2）用PyAceneDetect来计算frame之间的difference得分，然后用Gaussian filter来减少噪音并smooth这些得分，然后在一个固定阈值内选取最大的得分，这个位置说明两个frame之间差距很大，所以可以当作分割点。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921220343-f4b37780-3f9d-48ac-a6a6-ac6e1698bf8c.png)

**2. Instruction Generation**

构建了8种任务，其中包括五种涉及single-segment的理解任务和三个涉及cross-segment的理解任务，这些任务全部用于Grounded Event Sequence Modeling；Moment-10M的视频数据来自YTTemporal-1B

## Qwen2-VL
:::color3
**简介**：作为在Qwen-VL基础上迭代的最新版本，Qwen2-VL在视觉理解上达到非常先进的性能。**<font style="color:#ECAA04;">不再使用Q-former,而是直接使用MLP进行对齐。</font>**

**paper : **[**https://arxiv.org/pdf/2409.12191**](https://arxiv.org/pdf/2409.12191)

**项目地址**：[https://github.com/QwenLM/Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583) [**多模态技术梳理：Qwen-VL系列**](https://zhuanlan.zhihu.com/p/25267823390)**  **

:::

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1733472157254-037f1f85-1f1b-4cf5-8fc7-24d39969869f.jpeg)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">对各种分辨率和比例的图像的先进理解</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 在视觉理解基准上达到最先进的性能，包括 MathVista、DocVQA、RealWorldQA、MTVQA 等。</font>
+ **<font style="color:rgb(51, 51, 51);">理解超过 20 分钟的视频</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 能够处理超过 20 分钟的视频，提供高质量的视频问答、对话、内容创作等功能。</font>
+ **<font style="color:rgb(51, 51, 51);">可操作手机、机器人等设备的智能体</font>**<font style="color:rgb(51, 51, 51);">：具备复杂推理和决策能力的 Qwen2-VL 可以与手机、机器人等设备集成，基于视觉环境和文本指令进行自动操作。</font>
+ **<font style="color:rgb(51, 51, 51);">多语言支持</font>**<font style="color:rgb(51, 51, 51);">：为了服务全球用户，Qwen2-VL 除了支持英语和中文外，现在还能够理解图像中不同语言的文本，包括大多数欧洲语言、日语、韩语、阿拉伯语、越南语等。</font>

:::color5
**<font style="color:#601BDE;">2.模型架构更新</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **视觉、文本编码器升级：**
    - **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：之前qwenvl用的Openclip’s ViT-bigG-14，现在用的是</font>**<font style="color:#ED740C;">DFN的ViT</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - **<font style="color:rgb(25, 27, 31);">LLM</font>**<font style="color:rgb(25, 27, 31);">：升级到了Qwen2，值得注意的是对于不同大小的LLM，vision encoder 参数量不变。</font>
2. **<font style="color:rgb(51, 51, 51);">动态分辨率</font>**<font style="color:rgb(51, 51, 51);">：与以往不同的是，Qwen2-VL 可以</font>**<font style="color:#74B602;">处理任意图像分辨率</font>**<font style="color:rgb(51, 51, 51);">，将其映射为动态数量的视token，提供更接近人类的视觉处理体验。</font>
    - **任意分辨率的图像**：取消[DFN ViT](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=DFN+ViT&zhida_source=entity)绝对位置编码，使用2d RoPE，使得ViT可以输入任意分辨率的图像。测试的时候，还会在后面接一个MLP，把2x2的token 编码成一个token。图像编码得到的token使用<|vision_start|> 和 <|vision_end|> 包裹。因此对于，224x224的图，因为ViT patch size=14，就会得到(224/14/2)^2+2 = 66 个token。**参考**：[多模态理解开源王者：InternVL 1.5->InternVL 2.0](https://zhuanlan.zhihu.com/p/707475931)
    - **图像Token范围**：qwen2-vl对图像token的范围，通过min_pixels和max_pixels 进行了约束，这两个变量描述了图像pixel的范围的最小值和最大值。如果小于或者大于min_pixels和max_pixels ，就会resize到这个范围内，以实现计算量和性能的trade off。

```plain
MIN_PIXELS = 256*28*28
MAX_PIXELS = 512*28*28
```

3. **<font style="color:rgb(51, 51, 51);">多模态旋转位置嵌入 (M-ROPE)</font>**<font style="color:rgb(51, 51, 51);">：将位置嵌入分解为多个部分，</font>**<font style="color:#74B602;">以捕捉 1D 文本、2D 视觉和 3D 视频的位置信息</font>**<font style="color:rgb(51, 51, 51);">，增强其多模态处理能力。</font><font style="color:rgb(25, 27, 31);">在空间分辨率上，增加了</font>**<font style="color:#ED740C;">时间维度</font>**<font style="color:rgb(25, 27, 31);">，如果是文本，三个分量都相同。消融实验证明M-RoPE在下游效果更好。</font>**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[从浅到深入门旋转位置编码](https://zhuanlan.zhihu.com/p/13023539180)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191399043-bf846218-c884-419e-8b74-7b79077e7890.png)

4. **<font style="color:rgb(25, 27, 31);">统一的图像、视频理解</font>**

<font style="color:rgb(25, 27, 31);">为了更好理解视频，使用</font>**<font style="color:#ED740C;">时间轴为2的3d conv编码图像/视频</font>**<font style="color:rgb(25, 27, 31);">。具体来说，如果是一张图，就copy两份，如果是视频就每秒采样2帧。</font>

5. **Bounding box 坐标归一化**

之前Qwen1-VL 的 bounding box是绝对坐标，而Qwen2-VL是归一化坐标，虽然叫归一化坐标，但是实际上是归一化到了[0, 1000)，坐标就是![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191763591-d922011a-c86e-4df5-b65c-9fb8daeadde3.png)的形式。格式就像这样，被检测的物体和box坐标分别被speical token包裹。

```python
<|object_ref_start|>the eyes on a giraffe<|object_ref_end|><|box_start|>(176,106),(232,160)<|box_end|>
```

6. **Visual Agent**

Visual agent 就是function call 的能力，让LLM直接调用某个function并输入参数，Qwen2-VL中支持了这一个操作。

:::color5
**<font style="color:#601BDE;">3.多模态Adaptor：MLP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL采用了一种更简单的压缩方法：对</font>**<font style="color:#74B602;">空间位置临近的patch 特征做拼接，再经过2层MLP线性变换</font>**<font style="color:rgb(25, 27, 31);">，这样将原来长度为 </font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);"> 的序列，可压缩到 </font><font style="color:rgb(25, 27, 31);">n/4</font><font style="color:rgb(25, 27, 31);"> ，最终将压缩后的特征序列输入给LLM模型。处理过程如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742278493947-67adfde1-1e94-48d0-8b71-8cde17fd7ad8.png)

**<font style="color:rgb(25, 27, 31);">Vision token</font>**

<font style="color:rgb(25, 27, 31);">为了区分Vision token和文本token，Qwen2-VL也引入了两个特殊的token </font><font style="color:rgb(25, 27, 31);"><|vision_start|></font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);"><|vision_end|></font><font style="color:rgb(25, 27, 31);"> 来标识Vision token。</font>

```python
对于一个 224x224 ，如果ViT的 patch_size = 14 ，最终将图片编码成一个66个token的序列输入到模型。
具体计算过程：
1.Patch 处理后的Token数为： (224/14) x (224/14) = 16x16 = 256
2.经过输入投影层压缩处理： 256/4 = 64
3. 最后再加上 2 个起止位置的特殊token： 64+2 = 66

```

**为什么不用Q-Former？**

<font style="color:rgb(25, 27, 31);">主要是因为Cross-Attention架构适合处理</font>**<font style="color:#74B602;">固定长度的 </font>****<font style="color:#74B602;">k,v</font>****<font style="color:#74B602;"> </font>**<font style="color:rgb(25, 27, 31);">，当 </font><font style="color:rgb(25, 27, 31);">k,v</font><font style="color:rgb(25, 27, 31);"> 长短不一时，是不适合做Attention计算的。而Qwen2-VL通过原生动态分辨率方法处理的每个图片的token序列恰恰是变长的，无法使用Cross-Attention架构做特征压缩处理。</font>

:::color5
**<font style="color:#601BDE;">4.统一的图像&视频理解框架</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL统一了视频和图像的理解框架，能混合输入图像和视频数据进行理解。为了保证图片和视频的处理一致，对视频和图像分别做如下处理：</font>

+ **<font style="color:rgb(25, 27, 31);">视频处理：</font>**<font style="color:rgb(25, 27, 31);">以</font>**<font style="color:#74B602;">每秒两帧的速率对视频进行采样</font>**<font style="color:rgb(25, 27, 31);">，最终可采样偶数个帧序列。对于长视频为了平衡序列长度和计算效率，通过动态调整每一帧的分辨率，将视频总token限制在16K以内。</font>
+ **<font style="color:rgb(25, 27, 31);">图像处理：</font>**<font style="color:rgb(25, 27, 31);">对图像做复制操作，使得单一图片，变成一个</font>**<font style="color:#74B602;">时序为2的帧序列</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">使用3D的卷积对帧序列做特征抽取，如下图所示，每两张图片为一组进行卷积操作抽取特征。这样通过将卷积核扩充了时序维度，可以进一步压缩序列长度，因此也能进一步提升模型处理更多帧的能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743651805254-a31a14a4-c089-40db-be1c-d82546650375.png)



# Video数据集
## <font style="color:rgb(25, 27, 31);">InternVid：</font><font style="color:#D22D8D;">（by草莓师姐）</font>
**<font style="color:rgb(25, 27, 31);">用于多模态视频理解与生成的大规模视频-文本数据集</font>**

:::success
**<font style="color:rgb(25, 27, 31);">背景：</font>**<font style="color:rgb(25, 27, 31);">学习可迁移的视频-文本表示对于视频理解至关重要，尤其是在自动驾驶、智能监控、人机交互和视觉搜索等实际应用中。近期，OpenAI发布的</font>[<font style="color:rgb(9, 64, 142);">Sora模型</font>](https://zhida.zhihu.com/search?content_id=249098958&content_type=Article&match_order=1&q=Sora%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在文生视频领域取得了显著进展。Sora不仅打破了视频连贯性的局限，还在多角度镜头切换中保持一致性，并展示出对现实世界逻辑的深刻理解。这一突破为视频-语言领域的多模态对比学习提供了新的可能性，尽管目前Sora尚未开放给公众使用，但其在视频生成领域的GPT-3时刻，预示着通用人工智能的实现可能比预期来得更快。</font>

<font style="color:rgb(25, 27, 31);">但是限制住目前探索的一个关键原因是缺乏用于大规模预训练的高质量视频-语言数据集。当前的研究依赖于如</font>[<font style="color:rgb(9, 64, 142);">HowTo100M</font>](https://zhida.zhihu.com/search?content_id=249098958&content_type=Article&match_order=1&q=HowTo100M&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 、</font>[<font style="color:rgb(9, 64, 142);">HD-VILA</font>](https://zhida.zhihu.com/search?content_id=249098958&content_type=Article&match_order=1&q=HD-VILA&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 </font>[<font style="color:rgb(9, 64, 142);">YT-Temporal</font>](https://zhida.zhihu.com/search?content_id=249098958&content_type=Article&match_order=1&q=YT-Temporal&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 等数据集，其文本是使用自动语音识别（ASR）生成的。尽管这些数据集规模庞大，但它们在视频和相应文本描述之间的语义相关性通常较低。这类的数据一方面不太符合文生视频等生成任务的需要，另一方面提高这种相关性（例如，通过将视频与描述对齐以改善它们的匹配度）显著有利于下游任务，如视频检索和视频问答。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternVid 是一个开源的大规模视频-文本数据集，旨在促进视频理解和生成任务的发展，由</font>[<font style="color:rgb(9, 64, 142);">上海人工智能实验室</font>](https://zhida.zhihu.com/search?content_id=249098958&content_type=Article&match_order=1&q=%E4%B8%8A%E6%B5%B7%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AE%9E%E9%AA%8C%E5%AE%A4&zhida_source=entity)<font style="color:rgb(25, 27, 31);">与南京大学、中国科学院等单位联合发布，相关的工作已经被ICLR2024接收。</font>**<font style="color:#ED740C;">它包含超过 700 万个视频，总时长近 76 万小时，并附带详细的文本描述</font>**<font style="color:rgb(25, 27, 31);">。InternVid 的发布将推动文本-视频的多模态理解和生成的进步，并为相关研究和应用提供新的机遇。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/OpenGVLab/InternVideo/tree/main/Data/InternVid](https://github.com/OpenGVLab/InternVideo/tree/main/Data/InternVid)

**paper：**[**https://arxiv.org/pdf/2307.06942**](https://arxiv.org/pdf/2307.06942)

**参考：**[**https://zhuanlan.zhihu.com/p/929138634**](https://zhuanlan.zhihu.com/p/929138634)

:::

<font style="color:rgb(25, 27, 31);">数据集包含</font>**<font style="color:#74B602;">高度相关的视频-文本对，包括超过700万视频，总计760,000小时，产生234M个视频片段，涵盖16种场景和约6,000个动作描述</font>**<font style="color:rgb(25, 27, 31);">。为了提高视频-文本匹配度，我们采用了多尺度方法生成描述。在粗略尺度上，我们对每个视频的中间帧进行描述，并使用描述作为视频描述。在精细尺度上，我们生成逐帧描述，并用语言模型对它们进行总结。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743660289368-0dbd0cbf-1a5e-43b3-8443-901f45216eab.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">规模庞大:InternVid 是目前公开的最大的视频-文本数据集之一，包含超过 700 万个视频，总时长近 76 万小时。</font>
+ <font style="color:rgb(25, 27, 31);">内容丰富: 视频内容涵盖日常生活、体育运动、娱乐、教育等多个领域，能够满足不同研究和应用的需求。</font>
+ <font style="color:rgb(25, 27, 31);">高质量: 视频和文本都经过精心挑选和处理，保证了数据集的高质量，提供了丰富的描述，</font>[<font style="color:rgb(9, 64, 142);">CLIP-SIM</font>](https://zhida.zhihu.com/search?content_id=249098958&content_type=Article&match_order=1&q=CLIP-SIM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，视频美学分数。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">视频理解: 视频分类、视频检索、视频描述生成、视频摘要生成等。</font>
+ <font style="color:rgb(25, 27, 31);">视频生成: 视频编辑、视频合成、视频特效等。</font>
+ <font style="color:rgb(25, 27, 31);">多模态学习: 视频-文本语义匹配、视频-文本检索、视频-文本生成等。</font>

:::color5
**<font style="color:#601BDE;">3.数据集多样性</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">16个流行类别中收集了各种百分比的视频。为了确保多样性，我们选择了来自不同语言的国家的视频，而非依赖于一个主导语言环境。我们采样的国家包括英国、美国、澳大利亚、日本、韩国、中国、俄罗斯和法国等。在时长方面，每个视频平均持续351.9秒。几乎一半（49%）的视频时长不超过五分钟，而四分之一（26%）的视频时长在五到十分钟之间。只有8%的视频超过20分钟。在策划的视频中，85%是高分辨率（720P），其余15%的分辨率从360P至720P不等。虽然低分辨率的视频在内容生成任务中可能表现不如高分辨率的视频，但只要配有适当的描述，它们仍可用于视频-语言表示学习。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743660451450-1caaaf7c-fea5-47b3-b7c5-42078d5095ca.png)

<font style="color:rgb(25, 27, 31);">InternVid展示了在分割剪辑级别上具有不同剪辑时长和描述长度的多样性。美学分数和剪辑-描述相似度均匀分布。大部分剪辑的长度在0-10秒之间，占所有剪辑的85%。大约一半的剪辑描述含有10-20个单词，而三分之一的剪辑描述含有少于10个单词。大约11%的剪辑具有超过20个单词的长描述。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743660458774-adfc6e74-ea96-461d-8ad4-4f54af9d558e.png)

:::color5
**<font style="color:#601BDE;">4.多尺度视频描述生成</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743662121137-b969c185-82c5-48be-b7d5-eb4a917ecfb9.png)

<font style="color:rgb(25, 27, 31);">为了生成可扩展、丰富和多样化的视频描述，我们采用了多尺度方法，包含两种不同的描述策略，如图4所示。在更细的尺度上，我们通过专注于视频片段中常见的对象、动作和场景描述来简化视频描述过程。我们故意忽略了复杂细节，如微妙的面部表情和动作，以及其他细微元素。在更粗的尺度上，仅对视频的中心帧进行描述。鉴于我们关注的是通过场景分割过滤的短视频片段（大约10秒），大多数视频主要显示一致的对象，没有显著的外观变化。这避免了在处理视频时从图像角度处理身份保留问题。技术上，我们使用轻量级图像描述模型Tag2Text进行更细的尺度描述，它以低fps逐帧描述视频。在更粗的尺度上，我们使用BLIP2 对片段的中间帧进行描述。然后，这些描述被合成成一个综合视频描述，使用预训练的语言模型。</font>

:::color5
**<font style="color:#601BDE;">5.多模态视频表征模型ViCLIP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">基于InternVid和CLIP，我们还提出了ViCLIP，一个视频-文本对比学习的模型，它基于ViT-L，并采用了视频遮盖和对比损失的方法，来学习可迁移的视频-文本表示，如下图所示。通过引入 DeepSpeed 和 FlashAttention，ViCLIP 在 64 个 NVIDIA A100 GPU 上训练了 3 天。与之前的Video CLIP变体相比，ViCLIP在零样本设置下表现出显著的性能提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743660590764-cdb26ace-1747-402e-8a33-f7bf0630ed4e.png)

