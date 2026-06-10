# 4️⃣ 语音大模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/go342l3xnxz302iv -->

# 背景介绍<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color1
**背景：**<font style="color:rgb(25, 27, 31);">大型语言模型（LLM）具有很强的上下文理解能力和出色的多任务处理能力。因此，研究人员一直在积极探索</font>**<font style="color:#117CEE;">将大型语言模型（LLM）整合到语音理解领域，主要关注广泛的语音到文本任务</font>**<font style="color:rgb(25, 27, 31);">。这些包括</font>**<font style="color:#117CEE;">自动语音识别（ASR）、语音到文本翻译（ST）、语音情感识别（SER）</font>**<font style="color:rgb(25, 27, 31);">等。我们将这些模型称为语音LLM，它们通常建立在统一的架构上，遵循音频特征提取→多模态信息融合→LLM推理的流程。这种方法能够实现更丰富的音频特征提取，同时促进音频和文本模态的端到端融合，从而从音频数据中实现更深入的理解和推理。</font>

:::

:::color3
**简介：语音大模型：**<font style="color:rgb(25, 27, 31);">和人一样能听会说的智能系统。</font>

<font style="color:rgb(25, 27, 31);">本文阐述了语音LLMs的发展，对系统架构进行了深入分析。通过广泛的研究和一系列有针对性的实验，本文评估了</font>**<font style="color:#ED740C;">语音LLM的进展及其在语音理解领域跨任务集成的潜力</font>**<font style="color:rgb(25, 27, 31);">。此外，它还指出了通过实验发现的关键挑战，例如LLM在某些条件下的休眠。本文进一步探讨了言语LLMs的训练策略，基于这些发现提出了潜在的解决方案，并为未来的研究提供了有价值的见解和参考。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**paper：**[**WavChat: A Survey of Spoken Dialogue Models**](https://arxiv.org/pdf/2411.13577)** **

[**Recent Advances in Speech Language Models: A Survey**](https://arxiv.org/pdf/2410.03751)** **

[**A SURVEY ON SPEECH LARGE LANGUAGE MODELS**](https://arxiv.org/pdf/2410.18908)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745308790757-acd66f4d-8653-48d0-9f5b-e2ba0fc7c3fa.png)

> 三种不同输入输出模式的语音LLM架构概述：语音到文本（S2T）、语音和文本到文本（ST2T）以及语音和文本对语音和文本（ST2ST）。
>

:::color5
**<font style="color:#601BDE;">1.语音大模型是什么？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">2024年5月，OpenAI的GPT-4o发布，自然流畅的人机对话、强大的语音理解与多样化的语音回复、极低的延迟（0.3秒，与人类相当）让人印象深刻。 这使得研究者们重拾了对语音交互的热情，而且由于大语言模型的加持，语音交互的能力边界大幅提升。</font>

<font style="color:rgb(25, 27, 31);">理想的语音大模型像人一样，应该具备：</font>**<font style="color:#74B602;">高质量语音理解（听）与回复（说）、多轮对话、低延迟、实时对话</font>**<font style="color:rgb(25, 27, 31);">。 语音大模型（speech large language model, SpeechLLMs）亦有称之为语音对话模型（spoken dialogue models），本文统称之为语音大模型。</font>

:::color5
**<font style="color:#601BDE;">2.历史回顾</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在大模型时代之前（Pre-LLM Stage），语音技术各个细分方向相对独立，包括语音识别、语音合成、语音增强、语音分离、声音事件监测、说话人识别等等。</font>

<font style="color:rgb(25, 27, 31);">随着深度学习的发展(Early-LLM Stage)，语音技术开始进入预训练阶段，基于模型和大数据量的语音特征和表示。例如wav2vec、</font>[<font style="color:rgb(9, 64, 142);">Hubert</font>](https://zhida.zhihu.com/search?content_id=251989273&content_type=Article&match_order=1&q=Hubert&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，大幅提升了模型效果。</font>

<font style="color:rgb(25, 27, 31);">进入大模型时代(SpeechLLM Stage)，语音技术各个细分方向开始融合，更细分的任务融合成一个任务，例如声音复刻和语音合成融合为Zero-Shot TTS。语音技术开始走向“大一统”：语音大模型。	</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745291307101-353ae14a-eaee-43d4-954d-7b17abf86361.png)

> 语音LLM从**<font style="color:#74B602;">分离的声学和语言模型的Pre-LLM阶段</font>**，发展到**<font style="color:#74B602;">具有transformer集成的Early LLM阶段</font>**，再到具有大型语言模型**<font style="color:#74B602;">直接音频处理功能的当前语音LLM阶段</font>**。当前阶段包括两个分支：离散序列建模（如VALL-E、SpeechGPT）和连续序列建模（例如Pengi、SALMONN）。
>

:::color5
**<font style="color:#601BDE;">3.发展趋势</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">2022年之前，语音技术结合LLMs的工作开始萌芽。 2023年，紧跟LLMs的步伐，语音大模型相关工作开始涌现。 2024年，语音大模型相关研究更加深入，围绕高质量语音、全双工交互等热点难点。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745302058167-5cd78cea-26b1-44d9-aed3-46b817d6b06c.png)

> 近年来现有语音大模型发展时间线。时间表主要根据每种型号的技术文件的发布日期确定。值得注意的是，某些作品，如Westlake Omni、MooER Omni、Hertz dev、SpeechGPT2和Fish Agent，没有相应的发表论文。因此，我们没有将它们包括在图中。我们用黄色标记了公开的模型检查点。
>

:::color5
**<font style="color:#601BDE;">4.技术路径</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在大模型时代之前，实现一个人机语音对话系统是非常繁杂的，涉及多个模块：语音识别、意图识别、对话管理、对话生成、语音合成等模块。</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1745302287569-c5209fec-14ae-435c-ac16-f9bd8073eb56.jpeg)

<font style="color:rgb(25, 27, 31);">在大模型时代，使用LLMs取代意图识别、对话管理、对话生成等多个模块，让人机对话系统变得简单且更加强大。</font>

<font style="color:rgb(25, 27, 31);">根据模型是否能够直接理解和生成语音，分为级联、端到端两种技术路径：</font>

+ **<font style="color:rgb(25, 27, 31);">级联(Cascaded)</font>**<font style="color:rgb(25, 27, 31);">: 语音识别（ASR）、LLM、语音合成（TTS）三部分级联构成。构建成本较低、各模块成熟且相对独立；但是能力潜力小、信息丢失（例如丢失情感信息）、延迟较大。典型例子有</font>[AudioGPT](https://link.zhihu.com/?target=https%3A//github.com/AIGC-Audio/AudioGPT)<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">端到端(End-to-end)</font>**<font style="color:rgb(25, 27, 31);">: 一个模型实现语音的输入和输出。系统简单、能力（潜力）强、延迟低；构建成本较大、依赖大量的训练数据。典型例子有</font>[Moshi](https://link.zhihu.com/?target=https%3A//github.com/kyutai-labs/moshi/)<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">下图是级联系统与端到端系统的对比，可以看到两种系统中也分别有两种不同的技术路径，从上到下从完全的级联到完全的端到端。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745302389741-828e8a7e-4c92-41d6-ba26-3aad6db0b86c.png)

> 当前语音对话系统的概述。我们根据核心语言模型是否可以直接理解和生成语音表征，将这些系统分为两种范式，级联口语对话模型和端到端口语对话模型。此外，我们还提供了不同口语对话系统中使用的输入和输出方法的可视化。
>

<font style="color:rgb(25, 27, 31);">下表是OpenAI的语音模式，GPT-4o是端到端的方式，GPT-3.5和GPT-4都是级联的方式，无论是副语言信息的理解和多样化表达，还是整体的延迟，GPT-4o都大幅领先，使用体验提升明显。</font>

| **<font style="color:rgb(25, 27, 31);">对比维度</font>** | **<font style="color:rgb(25, 27, 31);">GPT-3.5</font>** | **<font style="color:rgb(25, 27, 31);">GPT-4</font>** | **<font style="color:rgb(25, 27, 31);">GPT-4o</font>** | **<font style="color:rgb(25, 27, 31);">Moshi</font>** |
| :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">结构</font> | <font style="color:rgb(25, 27, 31);">ASR + GPT-3.5 + TTS</font> | <font style="color:rgb(25, 27, 31);">ASR + GPT-4 + TTS</font> | <font style="color:rgb(25, 27, 31);">A single end-to-end model</font> | <font style="color:rgb(25, 27, 31);">A single end-to-end model</font> |
| 音频信息 | <font style="color:rgb(25, 27, 31);">×</font> | <font style="color:rgb(25, 27, 31);">×</font> | <font style="color:rgb(25, 27, 31);">✅</font><font style="color:rgb(25, 27, 31);"> (speaker, background, emotion...)</font> | <font style="color:rgb(25, 27, 31);">✅</font> |
| <font style="color:rgb(25, 27, 31);">有效的音频表征</font> | <font style="color:rgb(25, 27, 31);">×</font> | <font style="color:rgb(25, 27, 31);">×</font> | <font style="color:rgb(25, 27, 31);">✅</font><font style="color:rgb(25, 27, 31);"> (laughter, emotion, singing...)</font> | <font style="color:rgb(25, 27, 31);">Multi emotions & styles</font> |
| <font style="color:rgb(25, 27, 31);">时延</font> | <font style="color:rgb(25, 27, 31);">2.8s</font> | <font style="color:rgb(25, 27, 31);">5.4s</font> | <font style="color:rgb(25, 27, 31);">0.32s</font> | <font style="color:rgb(25, 27, 31);">0.23s average (minimum 0.16s)</font> |


# 语音大模型<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">语音大模型一般由三个模块组成：</font>

+ **<font style="color:rgb(25, 27, 31);">语音编码器(Speech Tokenizer)</font>**<font style="color:rgb(25, 27, 31);">: 有两类典型的Tokenizer，一种是Speech Encoder(如 Whisper Encoder)，连续空间表示语音；另一种是RVQ结构的Neural Codec Encoder，离散空间表示语音。</font>
+ **<font style="color:rgb(25, 27, 31);">大语言模型(Large Language Models)</font>**<font style="color:rgb(25, 27, 31);">: 各种语言模型均可。</font>
+ **<font style="color:rgb(25, 27, 31);">语音合成器(Token-to-Speech Synthesizer)</font>**<font style="color:rgb(25, 27, 31);">: 和上述Speech Tokenizer相对应，前者对应典型的合成器，例如HiFi-GAN等；后者对应Neural Codec Decoder。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745302981709-5b269b50-a810-47bb-927f-e540a08ed6fa.png)

> 对于SpeechLM，相同的内容可以在语音和文本模式中使用，这意味着任何输入模式都会产生相同结果的任何输出模式。图中有意重复输入/输出内容突出了这一点。
>

## SpeechGPT (2023.5)<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">SpeechGPT是于2023年5月份，复旦大学提出来的语音大模型。</font>

**paper**：[技术报告](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2305.11000)

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[Github](https://link.zhihu.com/?target=https%3A//github.com/0nutation/SpeechGPT)<font style="color:rgb(25, 27, 31);"> </font>

**模型仓库**：[模型仓库](https://link.zhihu.com/?target=https%3A//huggingface.co/fnlp/SpeechGPT-7B-cm)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745304992122-a111066b-96a5-482c-aef5-04ee2fa0ab53.png)

> SpeechGPT处理多个跨模态任务的能力。
>

:::color5
**<font style="color:#601BDE;">1.SpeechInstruct数据构建</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#601BDE;">SpeechInstruct构建过程概述</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745305251782-cdaecfd8-9e83-46f0-97d0-5d7a93147417.png)

**<font style="color:#601BDE;">Chain of Modality指令模板</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745305121547-02192b1d-722b-4159-bf6a-645e4acc4ccc.png)

SpeechInstruct数据集由两部分组成：跨模态指令数据和Chain of Modality指令数据。

:::color5
**<font style="color:#601BDE;">2.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">Speech Tokenizer</font>** | **<font style="color:rgb(25, 27, 31);">LLM</font>** | **<font style="color:rgb(25, 27, 31);">Speech Detokenizer</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">Hubert</font> | <font style="color:rgb(25, 27, 31);">LLaMA-7B</font> | <font style="color:rgb(25, 27, 31);">unit based HiFi-GAN</font> |


![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745305288315-0c62a247-2fec-450d-893b-9e544c92a138.png)

:::color5
**<font style="color:#601BDE;">3.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">模型训练</font>**

1. <font style="color:rgb(25, 27, 31);">阶段1：词表扩充&模态自适应。基于6万小时的无标注LibriLight语音数据。</font>
2. <font style="color:rgb(25, 27, 31);">阶段2：跨模态指令微调。训练数据包括1万小时GigaSpeech、3千小时CommonVoice、1千小时LibriSpeech。</font>
3. <font style="color:rgb(25, 27, 31);">阶段3：Chain-of-Modality Instruction Fine-Tuning。从moss-002-sft-data数据集中挑选的37,969条样本。</font>

**<font style="color:rgb(25, 27, 31);">分析</font>**

+ <font style="color:rgb(25, 27, 31);">SpeechGPT 是将文本和语音模态融合到LLMs的一次尝试，让LLMs具备了语音理解和生成能力。</font>
+ <font style="color:rgb(25, 27, 31);">由于Chain-of-Modality的机制，SpeechGPT无法实现实时交互，只能是半双工交互。</font>

<font style="color:rgb(25, 27, 31);"></font>

## LLAMA-Omni (2024.9)<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">LLaMA-Omni 是中科院计算所于2024年9月份发布出来的语音大模型。 LLaMA-Omni用少量的数据和算力成本，构建了LLaMA的语音模态能力。</font>

**<font style="color:rgb(25, 27, 31);">项目地址：</font>**<font style="color:rgb(25, 27, 31);"> </font>[Github](https://link.zhihu.com/?target=https%3A//github.com/ictnlp/LLaMA-Omni)<font style="color:rgb(25, 27, 31);"> </font>

**paper：**[技术报告](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2409.06666)

**模型仓库：**[模型仓库](https://link.zhihu.com/?target=https%3A//huggingface.co/ICTNLP/Llama-3.1-8B-Omni)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745305605932-5357b1ac-2d58-49db-9778-befa367e2758.png)

> LLaMA Omni可以根据语音指令同时生成文本和语音响应，响应延迟极低。
>

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">Speech Tokenizer</font>** | **<font style="color:rgb(25, 27, 31);">LLM</font>** | **<font style="color:rgb(25, 27, 31);">Speech Detokenizer</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">whisper-large-v3 encoder</font> | <font style="color:rgb(25, 27, 31);">LLaMA-3.1-8B-Instruct</font> | <font style="color:rgb(25, 27, 31);">unit base HiFi-GAN</font> |


![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745305632366-2889241d-c5a2-4b12-bb94-9f3b428d1266.png)

> 左图：LLaMA Omni的模型架构。右图：LLaMA Omni的两阶段训练策略示意图。
>

:::color5
**<font style="color:#601BDE;">2.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">模型训练</font>**

<font style="color:rgb(25, 27, 31);">LLaMA-Omni采用两阶段训练： </font>

<font style="color:rgb(25, 27, 31);">1. 阶段1：基于语音指令，生成文本回复。Speech Adaptor、LLMs参与模型训练。 </font>

<font style="color:rgb(25, 27, 31);">2. 阶段2：基于语音指令，生成语音回复。LLMs、Speech Decoder参与模型训练。</font>

**<font style="color:rgb(25, 27, 31);">分析</font>**

+ <font style="color:rgb(25, 27, 31);">基于Whisper Encoder融合语音模态，最大程度减少了对LLMs的影响，保持了LLMs本身的能力。较少的训练数据即可实现模型搭建。</font>
+ <font style="color:rgb(25, 27, 31);">引入CTC、采用chunk机制合成语音，降低语音回复的延迟。</font>
+ <font style="color:rgb(25, 27, 31);">虽然LLaMA-Omni有较低的延迟，但其本质仍是半双工交互方式，不支持打断。</font>

## Moshi (2024.10)<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Moshi由法国初创团队Kyutai开发的对标GPT-4o的语音交互模型，7月份发布，10月份公布了技术报告并开源了模型。 Moshi是一个多流的语音到语音的Transformer模型，支持全双工交互。</font>

**<font style="color:rgb(25, 27, 31);">项目地址：</font>**<font style="color:rgb(25, 27, 31);"> </font>[Github](https://link.zhihu.com/?target=https%3A//github.com/kyutai-labs/moshi)

**paper：**[技术报告](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2410.00037)

**模型仓库：**[模型仓库](https://link.zhihu.com/?target=https%3A//huggingface.co/collections/kyutai/moshi-v01-release-66eaeaf3302bef6bd9ad7acd)

:::

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">Speech Tokenizer</font>** | **<font style="color:rgb(25, 27, 31);">LLM</font>** | **<font style="color:rgb(25, 27, 31);">Speech Detokenizer</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">Mimi Encoder (12.5Hz x 8 Codebooks)</font> | <font style="color:rgb(25, 27, 31);">Helium-7B (As Temporal Transformer) & Depth Transformer (6 layers, d=1024, 16 heads)</font> | <font style="color:rgb(25, 27, 31);">Mimi Decoder</font> |


![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745306161446-b748122a-f12b-4622-8153-e0a409d45098.png)

> Moshi概述。Moshi是一个语音文本基础模型，可以实现实时口语对话。Moshi架构的主要组成部分是：定制的文本语言模型backbone（Helium）；具有残差矢量量化和从自监督语音模型中提取的语义知识的神经音频编解码器（Mimi）；用户和Moshi的语义和声学标记的流式、分层生成，以及在使用内部独白时Moshi的时间对齐文本标记。
>

<font style="color:rgb(25, 27, 31);">上图是Moshi的模型框架，特点如下： </font>

+ <font style="color:rgb(25, 27, 31);">Multi-stream：用户语音输入、Moshi语音输出、内心独白。为自然语音交互做好了底层设计，可以同时听和说，支持用户打断。 </font>
+ <font style="color:rgb(25, 27, 31);">Neural Codec：Mimi为了更低比特率、流式编解码、同时包含语义和声学信息，做了针对性设计。 </font>
+ <font style="color:rgb(25, 27, 31);">RQ-Transformer：包含Temporal Transformer和Depth Transformer，TemporaryTransformer处理时间步S，DepthTransformer进一步扩展到多个流。这样，将O(S*K)计算复杂度（S为时间步，K为序列/多流个数）大约减少为O(S)个计算步。</font>

<font style="color:rgb(25, 27, 31);">Mimi是Neural Codec，输入24KHz音频，输出12.5Hz的8个Codec，每个取值范围2048，第一个是VQ从WavLM中蒸馏学习语义信息，其他的7个为RVQ。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745306343375-80dd3264-7af7-4b1c-ac84-de123b7d1ab8.png)

> 我们的神经音频编解码器Mimi的架构和训练，以及其分割残差矢量量化。在训练过程中（蓝色部分，上图），我们从WavLM中提取非因果嵌入到一个向量量化器中，该量化器产生语义标记，并与单独的声学标记相结合进行重建。
>

:::color5
**<font style="color:#601BDE;">2.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">模型训练</font>**

1. <font style="color:rgb(25, 27, 31);">阶段1：Helium-7B 语言模型预训练。基于大量的文本数据。</font>
2. <font style="color:rgb(25, 27, 31);">阶段2：Moshi预训练。单流建模，文本和语音模态对齐。基于Whisper转写的7百万小时弱监督预训练数据。</font>
3. <font style="color:rgb(25, 27, 31);">阶段3：Moshi后训练。扩展到多流建模，让模型具备同时听和说的能力。采用了2千小时的电话数据集Fisher，8KHz采样率升采样到24KHz。</font>
4. <font style="color:rgb(25, 27, 31);">阶段4：Moshi微调。基于170小时自然对话，学习具有语音交叠的实时对话能力。基于2万小时包含70种说话风格的单说话人合成数据，使得Moshi具备固定音色。 值得一提的是，阶段3的训练，多流建模增加了Moshi的内心独白（Inner Monologue），也就是Moshi 生成语音相对应的文本，对应下图中Moshi stream的Text tokens。内心独白可以提升生成文本和语音的质量。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745306395379-e59a851d-8c0a-4e42-b546-e54908e36278.png)

> Moshi建模的关节序列的表示。每一列表示方程6中描述的具有声延迟τ=1的联合序列（Vs，k）中给定步骤的token，例如该步骤的时间变换器的输入。在深度转换器中从下到上预测token。在推理时，虚线下的token（对应于Moshi）被采样，而上面的token则由用户提供。这种设计允许我们的模型处理重叠的语音转弯。
>

**<font style="color:rgb(25, 27, 31);">分析</font>**

+ <font style="color:rgb(25, 27, 31);">Moshi对标GPT-4o，实现了多样化语音理解与生成的全双工语音交互。</font>
+ <font style="color:rgb(25, 27, 31);">Moshi的构建成本很高，需要大量的文本和语音数据，需要大量的算力。</font>
+ <font style="color:rgb(25, 27, 31);">Moshi的建模方式可以看做是一种‘原生多模态’的建模方式，相比于模态融合，其难度更高，还有很多值得探索。</font>

## GLM-4-Voice (2024.10)<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">GLM-4-Voice是智谱于2024年10月发布、11月公布技术报告的端到端语音模型。 GLM-4-Voice可以理解中英文语音，进行实时语音对话，并改变生成语音的情感、风格。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/THUDM/GLM-4-Voice](https://github.com/THUDM/GLM-4-Voice)

**paper：**[**https://arxiv.org/pdf/2412.02612**](https://arxiv.org/pdf/2412.02612)

:::

:::color5
**<font style="color:#601BDE;">1.两阶段训练数据构成</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745306989281-60352a47-4267-4323-b600-cd85a8b1f059.png)

**<font style="color:rgb(25, 27, 31);">Joint Speech-Text Pre-training</font>**

<font style="color:rgb(25, 27, 31);">这一步的目标是通过大规模语音预训练扩展LLM的语音能力，主要使用如下三种数据：</font>

+ **<font style="color:rgb(25, 27, 31);">Interleaved speech-text data</font>**<font style="color:rgb(25, 27, 31);">：作者团队在另一项工作中由文本预训练数据合成的语音-文本交错数据，促进文本和语音之间的跨模态知识转移。</font>
+ **<font style="color:rgb(25, 27, 31);">Unsupervised speech data</font>**<font style="color:rgb(25, 27, 31);">：包括70万小时的语音数据，鼓励模型从现实世界的语音中学习。</font>
+ **<font style="color:rgb(25, 27, 31);">Supervised speech-text data</font>**<font style="color:rgb(25, 27, 31);">：包括 ASR 和 TTS 数据，提高模型在基本语音任务中的能力。</font>

**<font style="color:rgb(25, 27, 31);">Supervised Fine-tuning</font>**

<font style="color:rgb(25, 27, 31);">为创建一个类人化的语音 chatbot，使用了如下两类数据：</font>

+ <font style="color:rgb(25, 27, 31);">多轮对话式语音对话：主要来自基于文本的数据，排除了代码、数学相关内容，以专注适合语音交互的对话材料。</font>
+ <font style="color:rgb(25, 27, 31);">语音风格控制的口语对话：包含针对特定语音风格要求（例如速度、情感或方言）的优质多轮语音对话。</font>

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745306943703-68512e22-8398-4a5e-92c0-defb07543127.png)

<font style="color:rgb(25, 27, 31);">GLM-4-Voice 是一个语音语言模型(speech language model, SLM)，主要由Speech Tokenizer、LLM、Speech Decoder三个模块组成。输入端支持语音输入，输出端支持文本和语音交替输出，其中输出的文本是为了引导后续的语音片段输出。</font>

+ **<font style="color:rgb(25, 27, 31);">GLM-4-Voice-Tokenizer:</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">通过在</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Whisper</font>](https://zhida.zhihu.com/search?content_id=249728068&content_type=Article&match_order=1&q=Whisper&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的 Encoder 部分增加</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Vector Quantization</font>](https://zhida.zhihu.com/search?content_id=249728068&content_type=Article&match_order=1&q=Vector+Quantization&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">并在 ASR 数据上有监督训练，将连续的语音输入转化为离散的 token。每秒音频平均只需要用 12.5 个离散 token 表示。</font>
+ **<font style="color:rgb(25, 27, 31);">GLM-4-Voice-Decoder:</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">基于</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">CosyVoice</font>](https://zhida.zhihu.com/search?content_id=249728068&content_type=Article&match_order=1&q=CosyVoice&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Flow Matching</font>](https://zhida.zhihu.com/search?content_id=249728068&content_type=Article&match_order=1&q=Flow+Matching&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">模型结构训练的支持流式推理的语音解码器，将离散化的语音 token 转化为连续的语音输出。最少只需要 10 个语音 token 即可开始生成，降低端到端对话延迟。</font>
+ **<font style="color:rgb(25, 27, 31);">GLM-4-Voice-9B: </font>**<font style="color:rgb(25, 27, 31);">在 GLM-4-9B 的基础上进行语音模态的预训练和对齐，从而能够理解和生成离散化的语音 token。</font>

| **<font style="color:rgb(25, 27, 31);">Speech Tokenizer</font>** | **<font style="color:rgb(25, 27, 31);">LLM</font>** | **<font style="color:rgb(25, 27, 31);">Speech Detokenizer</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">fine-tuned whisper-large-v3 with Quantizer (12.5Hz)</font> | <font style="color:rgb(25, 27, 31);">GLM-4-9B-Base</font> | <font style="color:rgb(25, 27, 31);">Flow Matching based on CosyVoice + Hifi-GAN vocoder</font> |


:::color5
**<font style="color:#601BDE;">2.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">模型训练</font>**

1. <font style="color:rgb(25, 27, 31);">第一阶段为大规模</font>**<font style="color:#74B602;">语音-文本联合预训练</font>**<font style="color:rgb(25, 27, 31);">，在该阶段中 GLM-4-Voice 采用了三种类型的语音数据：</font>**<font style="color:#74B602;">语音-文本交错数据、无监督语音数据和有监督语音-文本数据</font>**<font style="color:rgb(25, 27, 31);">，实现了促进文本和语音模态之间知识迁移、帮助模型学习真实世界语音特征以及提升模型基本任务方面性能方面的效果。尤其，GLM-4-Voice-9B 在 GLM-4-9B 的基座模型基础之上，经过了数百万小时音频和数千亿 token 的音频文本交错数据预训练，拥有很强的音频理解和建模能力。</font>
2. <font style="color:rgb(25, 27, 31);">第二阶段为监督微调阶段，旨在进一步提高 GLM-4-Voice 的对话能力。研究人员使用了两种类型的对话数据，包括</font>**<font style="color:#74B602;">多轮对话数据与语音风格控制对话数据</font>**<font style="color:rgb(25, 27, 31);">。前者主要来自文本数据，经过精心筛选和语音合成，确保对话内容的质量和多样性。而后者包含高质量的对话数据，用于训练模型生成不同风格和语调的语音输出。</font>
3. <font style="color:rgb(25, 27, 31);">此外，在对齐方面，为了支持高质量的语音对话，降低语音生成的延迟，研究团队设计了一套流式思考架构：根据用户语音，GLM-4-Voice 可以</font>**<font style="color:#74B602;">流式交替输出文本和语音两个模态的内容，其中语音模态以文本作为参照保证回复内容的高质量，并根据用户的语音指令要求做出相应的声音变化</font>**<font style="color:rgb(25, 27, 31);">，在最大程度保留语言模型智商的情况下仍然具有端到端建模的能力，同时具备低延迟性，最低只需要输出 20 个 token 便可以合成语音。</font>

**<font style="color:rgb(25, 27, 31);">分析</font>**

+ <font style="color:rgb(25, 27, 31);">GLM-4-Voice 通过语音-文本交替数据的预训练任务将语音模态和文本模态融入基座模型，这种方式对模态融合有很好的借鉴意义，具体细节可以他们的</font>[技术报告](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2411.17607)<font style="color:rgb(25, 27, 31);">。</font>
+ <font style="color:rgb(25, 27, 31);">GLM-4-Voice支持流式，为此对Whisper Encoder做了流式改造，标准卷积替换为因果卷积、双向注意力替换为因果注意力机制。</font>
+ <font style="color:rgb(25, 27, 31);">GLM-4-Voice在模型结构侧面没有做全双工（开源的模型），不能同时听和说，而是“半双工”模式。</font>

## KE-Omni (2024.12)<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">KE-Omni是由贝壳语音团队于2024年12月发布的中英文语音大模型，在</font>[VoiceBench](https://link.zhihu.com/?target=https%3A//github.com/MatthewCYM/VoiceBench)<font style="color:rgb(25, 27, 31);">上取得优异成绩。 该工作构建了包含6万小时、4万多个说话人的高质量合成语音对话数据集KeSpeechChat，并基于该数据集将LLaMA能力扩展到语音模态。</font>

**paper：**[**https://arxiv.org/pdf/2412.01078**](https://arxiv.org/pdf/2412.01078)

:::

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">文本对话构建（如下图）：引入了大语言模型，对文本指令数据进行口语化的改写。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745307378668-56fc5933-8b7f-4c91-b3c8-e034f12f05aa.png)

<font style="color:rgb(25, 27, 31);">语音对话构建（如下图）：提出了一种构建虚拟说话人音库的方法，丰富说话人的多样性。基于CosyVoice合成指定说话人音色的语音对话。对合成的语音对话进行质量筛选过滤。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745307352194-f5cf5ca2-4b2d-485e-8541-0142e4b9733a.png)

### 文本对话数据处理流程
**(A)现有指令数据**

• 展示了一段原始的指令数据，例如：“提供一个主题并基于该主题生成一篇博客文章。\n主题：远程工作的利弊。”  
• 指出了这段指令数据存在的问题：不适合语音交互、结构不够口语化、过于正式、内容过长等。

**(B)文本对话数据生成过程**

• 指令重写（Instruction Rewriting）：  
• 利用大型语言模型（LLM）将原始指令转换为更适合口语交流的问题形式。  
• 例如，将“提供一个主题并基于该主题生成一篇博客文章”重写为“远程工作的优缺点是什么？”  
• 重写指令的过滤（Filtering of Rewritten Instruction）：  
• 检查重写后的指令是否适合语音交互，排除那些需要生成长篇或结构化内容的任务。  
• 评估指令的清晰度和完整性，确保包含足够的上下文信息。  
• 使用内部系统和Qwen2-72B-instruct评估指令的安全性。  
• 口语风格后处理（Spoken Style Post-Processing）：  
• 使用LLM进一步修改选定的指令，使其更符合口语表达习惯。  
• 生成相应自然口语风格的响应，避免使用无法发音的内容，并将数字和符号转换为口头表述。  
• 保持响应简洁，不超过100字。

### 语音对话数据构建过程
**(A)真实说话人构建（Real Speaker Construction）**

• 从[WenetSpeech4TTS](https://zhida.zhihu.com/search?content_id=256497846&content_type=Article&match_order=1&q=WenetSpeech4TTS&zhida_source=entity)数据集中提取高质量的音频片段（DNSMOS≥4.0）。  
• 使用WavLM X-Vector提取技术识别同一说话人的多个片段。  
• 通过余弦相似度计算，筛选出至少5对相似度≥0.97的片段，确定这些片段属于同一说话人。  
• 构建包含真实说话人信息的说话人库。

**(B)虚拟说话人构建（Virtual Speaker Construction）**

• 从真实说话人库中随机抽取一个说话人嵌入，再从同性别且说话速率相同的剩余嵌入中抽取另一个。  
• 对这两个嵌入进行加权平均，生成合成的虚拟说话人嵌入。  
• 这种方法可以创建无限数量的虚拟说话人，保护隐私并避免数据滥用。

**(C)语音生成（Speech Generation）**

• 利用构建的虚拟说话人库和文本对话数据，通过[WATERMELON TTS](https://zhida.zhihu.com/search?content_id=256497846&content_type=Article&match_order=1&q=WATERMELON+TTS&zhida_source=entity)系统生成语音对话。  
• 为每个对话随机选择一个用户语音和一个代理语音，增加语音多样性。  
• 所有合成语音都添加了AudioSeal水印，防止数据滥用。

**(D)质量评估（Quality Assessment）**

• 使用Belle-whisper-large-v3turbo-zh和Whisper-large-v3turbo对生成的语音进行转录。  
• 计算中文的字符错误率（CER）和英文的词错误率（WER）。  
• 根据CER和WER筛选高质量语音，确保数据集的高质量。

:::color5
**<font style="color:#601BDE;">2.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">Speech Tokenizer</font>** | **<font style="color:rgb(25, 27, 31);">LLM</font>** | **<font style="color:rgb(25, 27, 31);">Speech Detokenizer</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">whisper-large-v3 encoder</font> | <font style="color:rgb(25, 27, 31);">LLaMA-3.1-8B-Instruct</font> | <font style="color:rgb(25, 27, 31);">Transformer based duration predictor & Transformer based speech unit generator & unit base HiFi-GAN</font> |


![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745307336093-e877c3e0-5bc3-4cce-a47f-ad0d74572bf0.png)

+ 语音编码

使用[Whisper-large-v3](https://zhida.zhihu.com/search?content_id=256497846&content_type=Article&match_order=1&q=Whisper-large-v3&zhida_source=entity)的编码器提取语音特征。  
通过轻量级语音适配器（5倍下采样）压缩特征长度，对齐LLM的文本嵌入空间。

+ LLM推理

基于[LLaMA-3.1-8B-Instruct](https://zhida.zhihu.com/search?content_id=256497846&content_type=Article&match_order=1&q=LLaMA-3.1-8B-Instruct&zhida_source=entity)模型，输入语音特征与文本提示，自回归生成文本响应。

+ 语音生成

**时长预测**：基于LLM隐藏状态预测每个文本token对应的语音帧数。  
**分块自回归生成**：按分块（chunk）逐步生成语音单元，结合延迟步长（N-step delay）确保时序对齐。  
**声码器合成**：[HiFi-GAN](https://zhida.zhihu.com/search?content_id=256497846&content_type=Article&match_order=1&q=HiFi-GAN&zhida_source=entity)将离散语音单元转换为波形，支持实时流式输出



