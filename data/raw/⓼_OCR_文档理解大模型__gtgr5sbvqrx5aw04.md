# ⓼ OCR/文档理解大模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/gtgr5sbvqrx5aw04 -->

# OCR评估 & Benchmark
:::color3
**简介**：一些闭源的模型通过API测试得到结果（[GPT-4o](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=GPT-4o&zhida_source=entity)-2024-08-06, [Gemini-1.5-Pro](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=Gemini-1.5-Pro&zhida_source=entity)-002, [Claude-3.5-Sonnet](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=Claude-3.5-Sonnet&zhida_source=entity)-20241022, 和[Qwen-VL-Max](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=Qwen-VL-Max&zhida_source=entity)-2024-08-09），任务场景，四大[OCR下游任务](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=OCR%E4%B8%8B%E6%B8%B8%E4%BB%BB%E5%8A%A1&zhida_source=entity)，即`多场景文本阅读`、`多语言文本阅读`、`[文档解析](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90&zhida_source=entity)`、`视觉信息提取` 。

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741837198625-52fbc466-eb9a-4f36-b309-6b794bb46837.png)

:::color5
**<font style="color:#601BDE;">1.OCR评估维度</font>**

:::

**<font style="color:rgb(25, 27, 31);">1.</font>**[**<font style="color:rgb(9, 64, 142);">多场景OCR</font>**](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=%E5%A4%9A%E5%9C%BA%E6%99%AFOCR&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">（Multi-Scene OCR）</font>**

+ <font style="color:rgb(25, 27, 31);">评估了通用LMMs和OCR专业LMMs在多场景OCR任务上的性能。</font>
+ <font style="color:rgb(25, 27, 31);">使用了包括自然场景、文档、多方向和艺术文本的数据集。</font>
+ <font style="color:rgb(25, 27, 31);">比较了不同模型在不同场景下的性能差异。</font>

<font style="color:rgb(25, 27, 31);">2.</font>[**<font style="color:rgb(9, 64, 142);">多语言OCR</font>**](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=%E5%A4%9A%E8%AF%AD%E8%A8%80OCR&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">（Multilingual OCR）</font>**

+ <font style="color:rgb(25, 27, 31);">评估了模型在多语言文本阅读任务上的表现。</font>
+ <font style="color:rgb(25, 27, 31);">涵盖了包括中文、英文、德文、日文、法文、韩文、俄文、西班牙文、葡萄牙文、阿拉伯文和越南文在内的十种语言。</font>
+ <font style="color:rgb(25, 27, 31);">分析了模型在不同语言上的性能差异，尤其是亚洲语言与拉丁语系语言之间的差异。</font>

**<font style="color:rgb(25, 27, 31);">3.文档解析（Document Parsing）</font>**

+ <font style="color:rgb(25, 27, 31);">评估了模型在文档解析任务上的性能，包括文档内容结构化和表格识别。</font>
+ <font style="color:rgb(25, 27, 31);">使用了包括扫描和拍照的文档图像，以及手动书写的公式图像。</font>
+ <font style="color:rgb(25, 27, 31);">分析了模型在处理不同语言文档和不同类型文档内容（如表格和公式）时的性能。</font>

**<font style="color:rgb(25, 27, 31);">4.</font>****<font style="color:rgb(25, 27, 31);"> </font>**[**<font style="color:rgb(9, 64, 142);">关键信息提取</font>**](https://zhida.zhihu.com/search?content_id=251210913&content_type=Article&match_order=1&q=%E5%85%B3%E9%94%AE%E4%BF%A1%E6%81%AF%E6%8F%90%E5%8F%96&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">（Key Information Extraction, KIE）</font>**

+ <font style="color:rgb(25, 27, 31);">评估了模型在关键信息提取任务上的能力，包括受限类别和开放类别的KIE任务。</font>
+ <font style="color:rgb(25, 27, 31);">要求模型输出结构化的JSON格式结果。</font>
+ <font style="color:rgb(25, 27, 31);">分析了模型在处理真实世界噪声、复杂结构和JSON输出要求方面的性能。</font>

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">OCR模型的Scaling Law</font>
:::color3
**<font style="color:#117CEE;">核心结论</font>**：标度律在OCR领域成立。模型的**<font style="color:#ED740C;">大小、数据量、计算和性能</font>**之间存在平滑的幂律。

通过探索中小型模型的参数量、计算量和数据量对多种OCR方法准确性的影响，我们成功地证明了幂律定律在OCR领域存在于这三个维度。这一发现为OCR模型设计提供了重要的理论依据。

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741851558270-3ba7b2c8-be36-402c-8fdf-9fca0e02e71a.png)

# <font style="color:rgb(25, 27, 31);">OCR/文档理解大模型</font>
:::info
<font style="color:rgb(25, 27, 31);">General OCR一般包含两步: </font>

<font style="color:rgb(25, 27, 31);">1. detection-->找到包含文字的区域(proposal); </font>

<font style="color:rgb(25, 27, 31);">2. classification-->识别区域中的文字。</font>

<font style="color:rgb(25, 27, 31);">多模态大模型最近在业界建设的如火如荼，具备了很强的视觉-语言交互能力。但是，其OCR能力也就是识别图片中文字的能力偏弱，强如GPT-4V，也似乎还不够看。</font>

:::

<font style="color:rgb(25, 27, 31);">业界最强多模态大模型</font>**<font style="color:rgb(25, 27, 31);">GPT-4V识别文字的能力比OCR专用模型低了几十个点</font>**<font style="color:rgb(25, 27, 31);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741847638938-fc4d8482-f79c-4aec-a56f-f5ad5b4a9a42.png)

## <font style="color:rgba(0, 0, 0, 0.9);">Mistral OCR</font>
:::color3
**简介：**<font style="color:rgb(31, 35, 41);">Mistral AI 近日推出了业界领先的 OCR（光学字符识别）模型——Mistral OCR。该模型在多项基准测试中表现卓越，尤其在</font>**<font style="color:#ED740C;">数学公式识别和智能文本处理</font>**<font style="color:rgb(31, 35, 41);">方面实现了重大突破。</font>

**参考：**[**https://mp.weixin.qq.com/s/6JPz2y-aBQig-3hc4jRNnw**](https://mp.weixin.qq.com/s/6JPz2y-aBQig-3hc4jRNnw)

:::

**<font style="color:rgb(25, 27, 31);">技术亮点</font>**<font style="color:rgb(25, 27, 31);">：Mistral OCR的最大亮点在于其强大的多模态文档理解能力。传统的OCR工具往往只擅长提取纯文本，而Mistral OCR能够</font>**<font style="color:#74B602;">全面解析复杂文档，包括文字、图片、表格、数学公式，甚至是手写内容</font>**<font style="color:rgb(25, 27, 31);">。更令人惊叹的是，它还能</font>**<font style="color:#74B602;">保留文档的原始结构，将输出格式化为</font>**[**<font style="color:#74B602;">Markdown</font>**](https://zhida.zhihu.com/search?content_id=254831589&content_type=Article&match_order=1&q=Markdown&zhida_source=entity)**<font style="color:#74B602;">或</font>**[**<font style="color:#74B602;">JSON</font>**](https://zhida.zhihu.com/search?content_id=254831589&content_type=Article&match_order=1&q=JSON&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，极大地方便了后续的AI处理。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. <font style="color:rgb(20, 86, 240);"></font>**<font style="color:rgb(31, 35, 41);">卓越的识别精度：</font>**<font style="color:rgb(31, 35, 41);"> Mistral OCR 在多个公开数据集和内部测试中均展现出卓越的识别准确率，超越了现有 OCR 模型。无论是扫描文档、照片还是屏幕截图，Mistral OCR 都能准确识别其中的文本内容。</font>
2. **<font style="color:rgb(31, 35, 41);">数学公式识别的突破：</font>**<font style="color:rgb(31, 35, 41);"> 长期以来，数学公式识别一直是 OCR 领域的难题。Mistral OCR 采用了先进的深度学习算法和独特的模型架构，实现了对数学公式的高精度识别。这一突破将极大地推动科研、教育等领域的信息化进程。</font>
3. **<font style="color:rgb(31, 35, 41);">能文本处理：</font>**<font style="color:rgb(31, 35, 41);"> Mistral OCR 不仅能识别文本，还能理解文本。它具备智能断句、分段、合并段落等功能，能够根据上下文语义对识别结果进行优化，使输出内容更符合阅读习惯，为后续的文本处理和分析提供便利。</font>
4. **<font style="color:rgb(31, 35, 41);">灵活的部署方式：</font>**<font style="color:rgb(31, 35, 41);"> Mistral OCR 提供了 API 接口和 Le Chat 两种使用方式。用户可以通过 API 将其集成到自己的应用程序中，也可以在 Le Chat 界面直接上传文档进行体验。这种灵活的部署方式满足了不同用户的需求。</font>

:::color5
**<font style="color:#601BDE;">2.评测</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">整体精度</font>**<font style="color:rgb(25, 27, 31);">：94.89%，远超Google Document AI（83.42%）和</font>[<font style="color:rgb(9, 64, 142);">Azure</font>](https://zhida.zhihu.com/search?content_id=254831589&content_type=Article&match_order=1&q=Azure&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> OCR（89.52%）。</font>
+ **<font style="color:rgb(25, 27, 31);">多语言支持</font>**<font style="color:rgb(25, 27, 31);">：识别准确率高达99.02%，轻松应对英语、阿拉伯语等多种语言。</font>
+ **<font style="color:rgb(25, 27, 31);">复杂任务</font>**<font style="color:rgb(25, 27, 31);">：在数学表达式（LaTeX格式）、扫描文档和表格解析等场景中，Mistral OCR同样大幅领先竞品，甚至击败了GPT-4o。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741855675166-e05eab42-918e-4a33-b14c-5d1043f8578c.png)

:::color5
**<font style="color:#601BDE;">5.应用场景</font>**

:::

+ **<font style="color:rgb(31, 35, 41);">文档数字化：</font>**<font style="color:rgb(31, 35, 41);"> 图书馆、档案馆、企业等机构可以利用 Mistral OCR 快速、准确地将纸质文档转换为电子文档，实现信息的数字化存储和管理。</font>
+ **<font style="color:rgb(31, 35, 41);">教育科研：</font>**<font style="color:rgb(31, 35, 41);"> Mistral OCR 能够高效识别教材、论文中的数学公式和图表，为师生提供便捷的学习和研究工具。</font>
+ **<font style="color:rgb(31, 35, 41);">金融保险：</font>**<font style="color:rgb(31, 35, 41);"> Mistral OCR 可以帮助金融机构快速处理各类表单、合同等文件，提高业务效率，降低运营成本。</font>
+ **<font style="color:rgb(31, 35, 41);">智能办公：</font>**<font style="color:rgb(31, 35, 41);"> Mistral OCR 可以集成到办公软件中，实现文档扫描、编辑、翻译等功能的自动化，提升办公效率。</font>

## 旷世Vary
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">基于CLIP视觉词表的多模态大模型，面临着同样的问题，遇到“foreign language image”，如一页论文密密麻麻的文字，</font>**<font style="color:#74B602;">很难高效地将图片token化</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Vary就是这一问题的一种解决方案，它可以在不重建原有词表前提下，</font>**<font style="color:#ED740C;">高效扩充视觉词表</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Ucas-HaoranWei/Vary](https://github.com/Ucas-HaoranWei/Vary)

**paper**：[https://arxiv.org/pdf/2312.06109](https://arxiv.org/pdf/2312.06109)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741852414580-6cda0f77-0b46-4c7c-ba61-00347f541a87.png)

:::color5
**<font style="color:#601BDE;">1.训练方法</font>**

:::

与使用现成视觉词汇的其他模型不同，Vary的过程可以分为两个阶段：**<font style="color:#74B602;">视觉词汇的生成和融合</font>**。

+ 第一阶段，我们使用**<font style="color:#ED740C;">“词表网络”(vocabulary network)</font>**和一个仅用于解码器的微型网络，来生成通过自回归获得强大的新视觉词汇。
+ 第二阶段，我们将视觉词汇表与原始词汇表融合，有效地为LVLM提供新特征。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741852480504-5e560594-e099-40b5-a6db-661c3f2e9969.png)



## LLaVAR
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：基于LLAVA的文档理解多模态大模型</font>

<font style="color:rgb(51, 51, 51);">《</font><font style="color:rgb(54, 54, 54);">LLaVAR: Enhanced Visual Instruction Tuning for Text-rich Image Understanding</font><font style="color:rgb(51, 51, 51);">》</font>

:::

:::color5
**<font style="color:#601BDE;">0.创新点</font>**

:::

+ 收集了**<font style="color:#74B602;">422K噪声指令跟踪数据和16K高质量指令跟随数据</font>**。两者都被证明在增强视觉教学调优方面是有效的。
+ LLaVAR显著增强了**<font style="color:#74B602;">图像中的文本理解</font>**，同时略微提高了模型在自然图像上的性能。
+ 增强的功能使我们的模型能够基于以下内容提供端到端交互结合文本和图像的各种形式的在线内容。

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**

:::

+ <font style="color:rgb(25, 27, 31);">数据源：LAION-5B</font>
+ <font style="color:rgb(25, 27, 31);">数据处理：</font>
    - <font style="color:rgb(25, 27, 31);">从LAION-5B中</font>**<font style="color:#74B602;">过滤出一批带有文字的图片</font>**<font style="color:rgb(25, 27, 31);">，总量422k，14个图片聚类，涉及海报、封面、广告、logo等文字显著的图片类别。</font>
    - <font style="color:rgb(25, 27, 31);">他们将这些</font>**<font style="color:#74B602;">图片放缩为336x336，用paddleocr进行文字识别</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - <font style="color:rgb(25, 27, 31);">构建</font>**<font style="color:#74B602;">“读取图片中文字”相关的指令</font>**<font style="color:rgb(25, 27, 31);">，例如“Identify text visible in the image provided”，这批数据用于增强模型对图片中文字的理解能力；</font>
    - <font style="color:rgb(25, 27, 31);">在前面数据的基础上，他们进一步</font>**<font style="color:#74B602;">延续LLaVA的做法构建更加多样化的用户指令</font>**<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">1）他们先从14个图片聚类里挑了4个类别，主要为封面、海报等，总计16k images; </font>
        * <font style="color:rgb(25, 27, 31);">2）然后他们将ocr识别出的文本，图片描述（BLIP2生成）</font>**<font style="color:#ECAA04;">送入纯文本的GPT4，让其生成多样化的指令和回复，从而最终得到16k的多样化指令理解数据集</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">2.VQA指令数据构建示例</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741853579391-83cc1f02-09ae-471f-9859-713839d36b27.png)

1. 收集422K噪声指令跟踪数据：通过结合手动编写的指令（例如，“识别所提供图像中可见的任何文本”）和OCR结果。这种大规模的噪声对齐数据有效地改善了视觉特征和语言解码器之间的特征对齐。
2. 我们将OCR结果和图像caption输入GPT-4，**<font style="color:#74B602;">生成16K个对话，每个对话都可以多轮问答配对</font>**，作为示例后的高质量教学。要求GPT-4对OCR结果进行**<font style="color:#74B602;">去噪处理，并制定具体问题</font>**以创建复杂的基于输入的指令。

```python
OCR1: 一本偷偷看的书 让我们去深海吧。
Caption:一个黄色潜水器的图片，有一个男孩在里面
```

```python
Q：图中书的名字是什么？
A：让我们去深海吧。
Q：书的类型是什么？
A：一本偷偷看的书
```

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741853552476-45ff15b3-a7a3-45c6-b49b-8a16ef2d194c.png)

<font style="color:rgb(25, 27, 31);">LLaVAR采用和LLaVA一样的模型结构，不过根据视觉编码器支持的分辨率，有两个版本，224x224的，以及336x336的。</font>

:::color5
**<font style="color:#601BDE;">4.模型评测</font>**

:::

<font style="color:rgb(25, 27, 31);">LLaVAR对比了已有的MLMM在ST-VQA，OCR-VQA，TextVQA以及DocVQA上</font>**<font style="color:rgb(25, 27, 31);">zero-shot</font>**<font style="color:rgb(25, 27, 31);">的结果</font>**<font style="color:rgb(25, 27, 31);">，仅判断答案是否在回复中。</font>**<font style="color:rgb(25, 27, 31);">结果表明，LLaVAR在这些数据上对于文字的理解显著优于已有的MLMM。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741853622268-6bb7b05e-5642-42ef-a142-f4349b70d244.png)

## <font style="color:rgb(25, 27, 31);">阿里mPLUG-DocOwl </font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">LLaVAR着重于增强模型对于一些文字显著的图片理解，主要为封面和海报。然而，包含文字的图片种类繁多，例如表格（table）、图表(chart)、文档（document）、网页截图（webpage）等等，LLaVAR涵盖的范围还是十分有限。</font>

:::

:::warning
**简介：**<font style="color:rgb(25, 27, 31);">mPLUG-DocOwl则是mPLUG-Owl团队对于</font>**<font style="color:#ED740C;">将MLLM拓展到全领域带文字图片理解</font>**<font style="color:rgb(25, 27, 31);">的初步尝试</font>

**参考：**[**利用LLM做文档图片理解: mPLUG-DocOwl vs LLaVAR**](https://zhuanlan.zhihu.com/p/642143087)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741855126838-f5e626f4-6e60-4e6b-8795-2041727b1ff1.png)

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**

:::

<font style="color:rgb(25, 27, 31);">不同于LLaVAR从开放域数据集中过滤图片，DocOwl直接整合已有的带文字图片相关的多个Benchmark，涵盖图表、文档、表格、自然图、网页截图等。这些benchmark具有不同的任务形式，例如问答、信息抽取、推理、图像描述等等。DocOwl将这些不同的任务形式都转变成mPLUG-Owl的指令理解数据形式。</font>

:::color5
**<font style="color:#601BDE;">2.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">mPLUG-DocOwl沿用了mPLUG-Owl的模型结构。</font>

:::color5
**<font style="color:#601BDE;">3.训练方法</font>**

:::

+ _**<font style="color:rgb(25, 27, 31);">第一阶段</font>**__<font style="color:rgb(25, 27, 31);">：</font>_<font style="color:rgb(25, 27, 31);">初始化于mPLUG-Owl，为了增强模型的文字理解能力，mPLUG-DocOwl第一阶段</font>**<font style="color:#ED740C;">只采用新构建的带文字图片相关的指令数据集进行微调</font>**<font style="color:rgb(25, 27, 31);">，训练结构包括visual abstractor和LLM中的</font>[<font style="color:rgb(9, 64, 142);">LoRA</font>](https://zhida.zhihu.com/search?content_id=230829603&content_type=Article&match_order=1&q=LoRA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>
+ _**<font style="color:rgb(25, 27, 31);">第二阶段</font>**__<font style="color:rgb(25, 27, 31);">：为</font>_<font style="color:rgb(25, 27, 31);">了保持Owl的开放域图文理解以及指令理解能力，mPLUG-DocOwl第二阶段进一步添加</font>**<font style="color:#ED740C;">Owl的指令微调数据进行混合训练</font>**<font style="color:rgb(25, 27, 31);">，只训练LLM中的LoRA。</font>

:::color5
**<font style="color:#601BDE;">5.评测</font>**

:::

_**<font style="color:rgb(25, 27, 31);">Benchmark评测</font>**__<font style="color:rgb(25, 27, 31);">：</font>_<font style="color:rgb(25, 27, 31);"> 由于DocOwl融合了标准数据集的作为训练，其具备准确回答相关问题的能力，因此可以和之前专门做ocr-free的图片文档理解的预训练工作进行对比。结果表明，</font>**<font style="color:rgb(25, 27, 31);">在标准的指标评测下，即使不进行特定数据集的微调</font>**<font style="color:rgb(25, 27, 31);">，DocOwl也在多个数据集上超过了特定领域“预训练+微调”工作的效果。</font>

## CLIP4STR
:::color3
**背景**：<font style="color:rgb(25, 27, 31);">视觉-语言模型是很多下游任务的基础模型，而当前的 </font>[<font style="color:rgb(9, 64, 142);">OCR</font>](https://zhida.zhihu.com/search?content_id=242914814&content_type=Article&match_order=1&q=OCR&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 任务中的预训练仍旧是在单一模态上进行的也就是视觉模态，比如</font>[<font style="color:rgb(9, 64, 142);">MAE</font>](https://zhida.zhihu.com/search?content_id=242914814&content_type=Article&match_order=1&q=MAE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">BEIT</font>](https://zhida.zhihu.com/search?content_id=242914814&content_type=Article&match_order=1&q=BEIT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等。</font>

**<font style="color:rgb(25, 27, 31);">简介</font>**<font style="color:rgb(25, 27, 31);">：视觉-语言模型的能力在 OCR 任务上是很强的，CLIP 能够较为鲁邦的识别图片中的规则文本和不规则的文本，所以基于这个发现，我们提出了 CLIP4STR，将 CLIP 用于 OCR 任务。</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://arxiv.org/pdf/2305.14014](https://arxiv.org/pdf/2305.14014)

**github**:[https://github.com/VamosC/CLIP4STR](https://github.com/VamosC/CLIP4STR)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741848438679-675fea0c-9120-4e16-9826-1afa9627f165.png)

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">MJ+SJ</font>**<font style="color:rgb(51, 51, 51);">：合并了合成文本数据集，总样本数为15.9M。</font>
2. **<font style="color:rgb(51, 51, 51);">Real(3.3M)</font>**<font style="color:rgb(51, 51, 51);">：包含9个真实场景文本数据集，总图像数为3.3M。</font>
3. **<font style="color:rgb(51, 51, 51);">RBU(6.5M)</font>**<font style="color:rgb(51, 51, 51);">：整合了Real数据集、部分基准数据集和Union14M-L的子集，总样本数为6.5M。</font>

| **数据集类别** | **组成与描述** | **样本数量** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">MJ+SJ</font>** | <font style="color:rgb(51, 51, 51);">- MJSynth (MJ, 9M samples)   </font><font style="color:rgb(51, 51, 51);">- SynthText (ST, 6.9M samples)</font> | <font style="color:rgb(51, 51, 51);">15.9M（合计）</font> |
| **<font style="color:rgb(51, 51, 51);">Real(3.3M)</font>** | <font style="color:rgb(51, 51, 51);">COCO-Text , RCTW17 , UberText , ArT , LSVT , MLT19 , ReCTS , TextOCR ,   </font><font style="color:rgb(51, 51, 51);">Open Images（通过OpenVINO工具包标注）</font> | <font style="color:rgb(51, 51, 51);">3.3M 图像</font> |
| **<font style="color:rgb(51, 51, 51);">RBU(6.5M)</font>** | <font style="color:rgb(51, 51, 51);">- Real(3.3M)   </font><font style="color:rgb(51, 51, 51);">- 基准数据集（SVT, IIIT5K, IC13, IC15的训练数据）   </font><font style="color:rgb(51, 51, 51);">- 部分Union14M-L </font> | <font style="color:rgb(51, 51, 51);">6.5M（组合后）</font> |


:::color5
**<font style="color:#601BDE;">2.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741848611597-9f409bfa-b155-4d53-9750-eb9534c65baa.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741848663493-84375b6b-9ce6-48f4-86aa-8cd47237da69.png)

<font style="color:rgb(25, 27, 31);">CLIP4STR 是以下面两个模型为基础的</font>

1. **<font style="color:rgb(25, 27, 31);">CLIP</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741848935385-a0f48446-b5e3-475a-95c7-b77002f52e27.png)

<font style="color:rgb(145, 150, 161);">alt text</font>

2. **<font style="color:rgb(25, 27, 31);">排列序列建模 </font>**[**<font style="color:rgb(9, 64, 142);">PSM</font>**](https://zhida.zhihu.com/search?content_id=242914814&content_type=Article&match_order=1&q=PSM&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">（permuted sequence modeling）from PARSeq</font>**

:::color5
**<font style="color:#601BDE;">3.评估</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741848707648-042b51d5-0f15-4c6c-9919-675bd5d78743.png)

## 华南理工：<font style="color:rgb(25, 27, 31);">Large OCR Model</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">引入OCR大模型到</font>[<font style="color:rgb(9, 64, 142);">Qwen-VL-Chat</font>](https://zhida.zhihu.com/search?content_id=238786730&content_type=Article&match_order=1&q=Qwen-VL-Chat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">多模态大模型，并在四个</font>[<font style="color:rgb(9, 64, 142);">VQA任务</font>](https://zhida.zhihu.com/search?content_id=238786730&content_type=Article&match_order=1&q=VQA%E4%BB%BB%E5%8A%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">上进行了详细测评如Table 5。结果表明，OCR技术的引入显著提升了LMM在VQA任务上的精度，证明了OCR在提升多模态大模型文本识别能力方面的重要性，也展示了OCR在处理复杂视觉-语言交互任务中的潜力。</font>

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://zhuanlan.zhihu.com/p/677954266](https://zhuanlan.zhihu.com/p/677954266)

**项目地址**：[https://github.com/large-ocr-model/large-ocr-model.github.io/blob/main/Data.md](https://github.com/large-ocr-model/large-ocr-model.github.io/blob/main/Data.md)

**paper**:[https://large-ocr-model.github.io/](https://large-ocr-model.github.io/)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. <font style="color:rgb(25, 27, 31);">研究结果揭示，在其他影响因素保持不变的情况下，</font>**<font style="color:#ED740C;">性能与模型大小及训练数据量之间存在平滑的指数法则关系（Scaling Law）。</font>**
2. <font style="color:rgb(25, 27, 31);">此外，我们还创建了一个大规模数据集</font>[**<font style="color:#ED740C;">REBU-Syn</font>**](https://zhida.zhihu.com/search?content_id=238786730&content_type=Article&match_order=1&q=REBU-Syn&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，包含600万真实样本和1800万合成样本。利用这些法则和数据集，我们成功训练了一个高精度的OCR模型，在OCR的测试基准上实现了SOTA精度。</font>
3. <font style="color:rgb(25, 27, 31);">特别地，我们发现</font>**<font style="color:#74B602;">OCR模型能显著增强多模态大模型的能力</font>**<font style="color:rgb(25, 27, 31);">，在多个VQA任务上实现了显著的精度提升，证明了OCR在提升多模态大模型性能方面的巨大潜力。</font>

:::color5
**<font style="color:#601BDE;">2.</font>**[**<font style="color:#601BDE;">REBU-Syn</font>**](https://zhida.zhihu.com/search?content_id=238786730&content_type=Article&match_order=1&q=REBU-Syn&zhida_source=entity)**<font style="color:#601BDE;">数据集</font>**

:::

+ 我们从16个公开可用的真实数据集中收集了标记数据，以构建REBU Syn
+ <font style="color:rgb(25, 27, 31);">在OCR领域，数据集的质量和多样性极为重要。我们通过收集和整合开源数据集 ，创建了全新数据集</font>_**<font style="color:rgb(25, 27, 31);">REBU-Syn</font>**_<font style="color:rgb(25, 27, 31);">。此外我们利用</font>**<font style="color:#74B602;">最新生成技术生成的60M合成数据</font>**[**<font style="color:#74B602;">MJST+</font>**](https://zhida.zhihu.com/search?content_id=238786730&content_type=Article&match_order=1&q=MJST%2B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，以供额外的使用。</font>

| **<font style="color:rgb(31, 35, 40);">Data file name</font>** | **<font style="color:rgb(31, 35, 40);">Size</font>** | **<font style="color:rgb(31, 35, 40);">Link</font>** |
| --- | --- | --- |
| <font style="color:rgb(31, 35, 40);">OpenVINO</font> | <font style="color:rgb(31, 35, 40);">1.5M</font> | [https://storage.googleapis.com/openimages/web/index.html](https://storage.googleapis.com/openimages/web/index.html) |
| <font style="color:rgb(31, 35, 40);">TextOCR</font> | <font style="color:rgb(31, 35, 40);">0.8M</font> | [https://textvqa.org/textocr/dataset/](https://textvqa.org/textocr/dataset/) |
| <font style="color:rgb(31, 35, 40);">ICDAR2013</font> | <font style="color:rgb(31, 35, 40);">843</font> | [https://rrc.cvc.uab.es/?ch=2](https://rrc.cvc.uab.es/?ch=2) |
| <font style="color:rgb(31, 35, 40);">ICDAR2015</font> | <font style="color:rgb(31, 35, 40);">4,467</font> | [https://rrc.cvc.uab.es/?ch=4](https://rrc.cvc.uab.es/?ch=4) |
| <font style="color:rgb(31, 35, 40);">IIIT5K</font> | <font style="color:rgb(31, 35, 40);">2,000</font> | [https://cvit.iiit.ac.in/research/projects/cvit-projects/the-iiit-5k-word-dataset](https://cvit.iiit.ac.in/research/projects/cvit-projects/the-iiit-5k-word-dataset) |
| <font style="color:rgb(31, 35, 40);">SVT</font> | <font style="color:rgb(31, 35, 40);">257</font> | [http://www.iapr-tc11.org/mediawiki/index.php/The_Street_View_Text_Dataset](http://www.iapr-tc11.org/mediawiki/index.php/The_Street_View_Text_Dataset) |
| <font style="color:rgb(31, 35, 40);">Total-Text</font> | <font style="color:rgb(31, 35, 40);">12,251</font> | [https://github.com/cs-chan/Total-Text-Dataset](https://github.com/cs-chan/Total-Text-Dataset) |
| <font style="color:rgb(31, 35, 40);">CTW1500</font> | <font style="color:rgb(31, 35, 40);">3,170</font> | [https://github.com/Yuliang-Liu/Curve-Text-Detector](https://github.com/Yuliang-Liu/Curve-Text-Detector) |
| <font style="color:rgb(31, 35, 40);">Uber</font> | <font style="color:rgb(31, 35, 40);">127,850</font> | [https://s3-us-west-2.amazonaws.com/uber-common-public/ubertext/index.html](https://s3-us-west-2.amazonaws.com/uber-common-public/ubertext/index.html) |
| <font style="color:rgb(31, 35, 40);">RCTW17</font> | <font style="color:rgb(31, 35, 40);">10,245</font> | [https://rctw.vlrlab.net/dataset](https://rctw.vlrlab.net/dataset) |
| <font style="color:rgb(31, 35, 40);">COCOv2.0</font> | <font style="color:rgb(31, 35, 40);">72,950</font> | [https://vision.cornell.edu/se3/coco-text-2/](https://vision.cornell.edu/se3/coco-text-2/) |
| <font style="color:rgb(31, 35, 40);">LSVT</font> | <font style="color:rgb(31, 35, 40);">8,164</font> | [https://rrc.cvc.uab.es/?ch=16](https://rrc.cvc.uab.es/?ch=16) |
| <font style="color:rgb(31, 35, 40);">MLT19</font> | <font style="color:rgb(31, 35, 40);">55,112</font> | [https://rrc.cvc.uab.es/?ch=15](https://rrc.cvc.uab.es/?ch=15) |
| <font style="color:rgb(31, 35, 40);">ReCTS</font> | <font style="color:rgb(31, 35, 40);">26,040</font> | [https://rrc.cvc.uab.es/?ch=12](https://rrc.cvc.uab.es/?ch=12) |
| <font style="color:rgb(31, 35, 40);">ArT</font> | <font style="color:rgb(31, 35, 40);">31,966</font> | [https://rrc.cvc.uab.es/?ch=14](https://rrc.cvc.uab.es/?ch=14) |
| <font style="color:rgb(31, 35, 40);">Union14M_L_lmdb_format</font> | <font style="color:rgb(31, 35, 40);">3M</font> | [https://github.com/Mountchicken/Union14M/tree/main?tab=readme-ov-file#34-download](https://github.com/Mountchicken/Union14M/tree/main?tab=readme-ov-file#34-download) |


# <font style="color:rgb(31, 35, 40);">OCR项目实践</font>
:::color3
**简介：**<font style="color:rgb(31, 35, 40);">与专用OCR模型相比，当前多模态大模型的识字能力相对较弱。直接使用多模态大模型做视觉信息抽取往往会出现错字。</font>**<font style="color:rgb(31, 35, 40);">本项目使用OCR结果来引导多模态大模型输出，以期得到更高的信息抽取准确率。</font>**

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/hzauzxb/guidance-ocr?tab=readme-ov-file](https://github.com/hzauzxb/guidance-ocr?tab=readme-ov-file)

**简介：**[**https://zhuanlan.zhihu.com/p/7783443583**](https://zhuanlan.zhihu.com/p/7783443583)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741852879066-04055dbd-fc1a-402c-9f9b-1cbfd0d516ec.png)

**算法原理**

1. <font style="color:rgb(31, 35, 40);">基于OCR识别出的文字构建一套规则引擎</font>
2. <font style="color:rgb(31, 35, 40);">在大模型每次给出next-token的logit时，基于规则引擎和预先设定的top_k过滤掉一批token_id</font>
3. <font style="color:rgb(31, 35, 40);">选择概率最大的token_id作为本次生成的next-token</font>
4. <font style="color:rgb(31, 35, 40);">基于生成的next-token更新规则引擎</font>
5. <font style="color:rgb(31, 35, 40);">重复上述2-4步直到输出eos_id 或 步骤2中所有token均被过滤掉</font>

