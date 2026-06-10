# 预训练

<!-- source: yuque://zhongxian-iiot9/hlyypb/rzz0r3bmk9m66r7u -->

# 基础
**<font style="color:#117CEE;">定义</font>**：<font style="color:#1f2329;">预训练是指在⼤规模的未标注数据上训练模型，使其学习通⽤的特征表⽰。这⼀阶段不针对特定任务，⽽是让模型掌握数据的基本结构和模式。</font>

**<font style="color:#117CEE;">目的</font>**

+ <font style="color:#245bdb;">学习通用特征：</font><font style="color:#1f2329;">通过在⼤量数据上训练，模型能够捕获数据的通⽤特征和模式。</font>
+ <font style="color:#245bdb;">提高效率：</font><font style="color:#1f2329;">预训练好的模型可以作为下游任务的基础，减少训练时间和数据需求。</font>



# 预训练评估
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">评估大型语言模型（LLM）的预训练效果需要从多个维度综合考量，涉及</font>**<font style="color:#ED740C;">基础语言能力、下游任务表现、知识掌握、推理能力</font>**<font style="color:rgb(51, 51, 51);">等。</font>

:::

:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

1. **基础语言能力**
    - **困惑度（Perplexity, PPL）**
        * **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：衡量模型对文本序列预测的不确定性，数值越低表示模型对训练数据的拟合越好。</font>
        * **<font style="color:rgb(51, 51, 51);">适用场景</font>**<font style="color:rgb(51, 51, 51);">：预训练阶段的核心指标，反映模型对语言分布的掌握程度。</font>
        * **<font style="color:rgb(51, 51, 51);">局限性</font>**<font style="color:rgb(51, 51, 51);">：无法直接反映生成文本的质量或逻辑性。</font>
    - **Token Prediction Accuracy**
        * <font style="color:rgb(51, 51, 51);">模型预测下一个词（Token）的准确率，常用于验证预训练阶段的局部优化效果。</font>
2. **下游任务表现**
    - **<font style="color:rgb(51, 51, 51);">Zero-Shot/Few-Shot 准确率</font>**
        * <font style="color:rgb(51, 51, 51);">直接使用预训练模型在未见的任务（如文本分类、问答）上的表现，无需微调。</font>
        * **<font style="color:rgb(51, 51, 51);">QWEN 案例</font>**<font style="color:rgb(51, 51, 51);">：在 MMLU（多任务语言理解）等基准测试中，QWEN 通过提示词（Prompt）直接生成答案，评估其泛化能力。</font>
3. **知识掌握与推理**
    - **<font style="color:rgb(51, 51, 51);">事实正确性（Factual Accuracy）</font>**
        * <font style="color:rgb(51, 51, 51);">通过问答任务（如 TriviaQA）验证模型对世界知识的掌握。</font>
    - **<font style="color:rgb(51, 51, 51);">逻辑推理能力</font>**
        * <font style="color:rgb(51, 51, 51);">数学推理（GSM8K）、常识推理（HellaSwag）等任务中的准确率。</font>
4. **生成质量**
    - **<font style="color:rgb(51, 51, 51);">多样性、连贯性、相关性</font>**
        * <font style="color:rgb(51, 51, 51);">人工或自动化指标（如 BLEU、ROUGE）评估生成文本的质量。</font>
5. **效率指标**
    - **<font style="color:rgb(51, 51, 51);">训练速度（Tokens/Second）</font>**
    - **<font style="color:rgb(51, 51, 51);">显存占用与推理延迟</font>**
        * <font style="color:rgb(51, 51, 51);">例如 QWEN-72B 的显存优化策略对其推理效率的影响。</font>
6. **安全性**
    - <font style="color:rgb(51, 51, 51);">对有害内容生成、偏见、幻觉（Hallucination）的抵抗能力，通过 TruthfulQA 等基准测试评估。</font>

:::color5
**<font style="color:#601BDE;">2.评估方法</font>**

:::

1. **自动化评估**
    - **<font style="color:rgb(51, 51, 51);">静态测试集评估</font>**
        * <font style="color:rgb(51, 51, 51);">使用标准化测试集（如 MMLU、C-Eval）计算准确率或生成指标（如 BLEU）。</font>
    - **<font style="color:rgb(51, 51, 51);">动态评估框架</font>**
        * <font style="color:rgb(51, 51, 51);">使用工具链（如 lm-evaluation-harness）批量运行多个任务，支持多种模型对比。</font>
2. **人工评估**
    - **<font style="color:rgb(51, 51, 51);">生成内容评分</font>**
        * <font style="color:rgb(51, 51, 51);">由人类标注员对生成文本的流畅性、逻辑性、相关性打分（如 1-5 分制）。</font>
    - **<font style="color:rgb(51, 51, 51);">对抗性测试</font>**
        * <font style="color:rgb(51, 51, 51);">设计复杂问题或陷阱问题，测试模型的鲁棒性（如 QWEN 在开放域问答中的表现）。</font>
3. **任务特定评估**
    - **<font style="color:rgb(51, 51, 51);">领域适应能力</font>**
        * <font style="color:rgb(51, 51, 51);">在特定领域（如医学、法律）数据上的 Few-Shot 表现。</font>
    - **<font style="color:rgb(51, 51, 51);">多语言能力</font>**
        * <font style="color:rgb(51, 51, 51);">在多语言基准（如 XNLI、Flores-101）中测试跨语言理解与生成。</font>

:::color5
**<font style="color:#601BDE;">3.常用Benchmark</font>**

:::

1. **通用语言理解与推理**
    - **<font style="color:rgb(51, 51, 51);">MMLU（Massive Multitask Language Understanding）</font>**
        * <font style="color:rgb(51, 51, 51);">涵盖 57 个学科的多选问答任务，测试模型的知识广度和推理能力。</font>
        * **<font style="color:rgb(51, 51, 51);">QWEN 表现</font>**<font style="color:rgb(51, 51, 51);">：QWEN-72B 在 MMLU 上达到约 76% 准确率（需参考具体版本）。</font>
    - **<font style="color:rgb(51, 51, 51);">C-Eval</font>**
        * <font style="color:rgb(51, 51, 51);">中文多学科评测基准，覆盖 STEM、社科等领域。</font>
    - **<font style="color:rgb(51, 51, 51);">HellaSwag</font>**
        * <font style="color:rgb(51, 51, 51);">常识推理数据集，测试模型对物理场景的理解。</font>
2. **代码与数学能力**
    - **<font style="color:rgb(51, 51, 51);">HumanEval</font>**
        * <font style="color:rgb(51, 51, 51);">评估代码生成能力（Pass@1 准确率）。</font>
        * **<font style="color:rgb(51, 51, 51);">QWEN 案例</font>**<font style="color:rgb(51, 51, 51);">：QWEN-Code 系列在 HumanEval 上表现优异（如 35%+ Pass@1）。</font>
    - **<font style="color:rgb(51, 51, 51);">GSM8K</font>**
        * <font style="color:rgb(51, 51, 51);">小学数学应用题，测试逐步推理能力。</font>
3. **生成与安全性**
    - **<font style="color:rgb(51, 51, 51);">TruthfulQA</font>**
        * <font style="color:rgb(51, 51, 51);">检测模型生成内容的真实性和抗幻觉能力。</font>
    - **<font style="color:rgb(51, 51, 51);">BIG-Bench</font>**
        * <font style="color:rgb(51, 51, 51);">包含 200+ 多样化任务，测试模型综合能力。</font>
4. **中文特定任务**
    - **<font style="color:rgb(51, 51, 51);">CLUE（Chinese Language Understanding Evaluation）</font>**
        * <font style="color:rgb(51, 51, 51);">中文自然语言理解基准，包括文本分类、阅读理解等。</font>
    - **<font style="color:rgb(51, 51, 51);">CMMLU</font>**
        * <font style="color:rgb(51, 51, 51);">专注于中文多任务语言理解的评测集。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">以QWEN为例的评估实践</font>**

:::

1. **预训练阶段**
    - <font style="color:rgb(51, 51, 51);">使用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">PPL</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">监控训练稳定性，通过验证集（如 The Pile）评估模型收敛情况。</font>
    - <font style="color:rgb(51, 51, 51);">利用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Zero-Shot 测试</font>**<font style="color:rgb(51, 51, 51);">（如 Lambada）验证语言建模能力。</font>
2. **下游任务验证**
    - <font style="color:rgb(51, 51, 51);">在</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">MMLU</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(51, 51, 51);">C-Eval</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">等基准中对比 SOTA 模型（如 GPT-4、LLaMA-2）。</font>
    - <font style="color:rgb(51, 51, 51);">通过</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Few-Shot 提示工程</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">提升任务表现（如调整温度参数、增加示例）。</font>
3. **生成质量分析**
    - <font style="color:rgb(51, 51, 51);">使用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">人工评估</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">验证长文本生成（如故事创作）的连贯性和创意性。</font>
    - <font style="color:rgb(51, 51, 51);">在 </font>**<font style="color:rgb(51, 51, 51);">Safety 测试</font>**<font style="color:rgb(51, 51, 51);"> 中过滤有害输出，确保符合伦理规范。</font>

:::color5
**<font style="color:#601BDE;">5.挑战与改进方向</font>**

:::

<font style="color:rgb(51, 51, 51);">评估 LLM 的预训练效果需结合自动化指标与人工评估，覆盖基础能力、任务泛化、知识推理等多维度。对于 QWEN 这类模型，需在通用基准（如 MMLU）和中文特定任务（如 C-Eval）中验证其优势，同时关注效率与安全性。实际应用中，还需根据业务场景定制评估策略（如领域适配性、多语言支持等）。</font>

# 预训练数据配比
:::color5
**<font style="color:#601BDE;">1.选择方法</font>**

:::

1. **明确业务需求和目标**：
    - <font style="color:rgb(51, 51, 51);">确定模型的主要任务和应用场景。例如，医疗咨询系统需要准确理解和回答专业问题。</font>
    - <font style="color:rgb(51, 51, 51);">确保数据配比能够支持这些核心任务，同时考虑模型的通用能力。</font>
2. **分析数据资源**：
    - <font style="color:rgb(51, 51, 51);">评估可用数据的数量和质量，特别是特定领域和通用数据的可用性。</font>
    - <font style="color:rgb(51, 51, 51);">如果特定领域数据稀缺，可能需要增加通用数据的比例，反之则可增加特定数据的比例。</font>
3. **考虑模型目标和评估指标**：
    - <font style="color:rgb(51, 51, 51);">确定模型在预训练和微调阶段的目标，平衡特定和通用任务的表现。</font>
    - <font style="color:rgb(51, 51, 51);">使用适合的评估指标来测试模型在不同任务上的性能。</font>
4. **参考行业实践**：
    - <font style="color:rgb(51, 51, 51);">查阅类似任务的成功案例，了解推荐的数据配比，作为调整的基础。</font>
5. **进行实验和迭代**：
    - <font style="color:rgb(51, 51, 51);">进行小规模预训练和测试，评估模型表现。</font>
    - <font style="color:rgb(51, 51, 51);">根据结果调整数据配比，重复实验，确定最优比例。</font>
6. **考虑数据多样性和质量**：
    - <font style="color:rgb(51, 51, 51);">确保数据覆盖广泛的话题和情境，提升模型的泛化能力。</font>

:::color5
**<font style="color:#601BDE;">2.业界经验</font>**

:::

1. **平衡特定领域与通用数据**：在预训练过程中，数据配比需要根据业务需求进行调整。如果目标是特定领域任务（如医疗、金融等），可能需要增加特定领域数据的比例，以增强模型对领域知识的掌握。同时，通用数据的比例也不宜过低，以保持模型的泛化能力
2. **基于实验的结果调整数据配比**：业界通常会通过小规模实验来测试不同数据配比对模型性能的影响。例如，可以通过调整特定领域数据与通用数据的比例，观察模型在特定任务上的表现变化，从而确定最优的数据配比
3. **参考行业基准**：虽然具体的配比可能因场景而异，但可以参考行业内的基准配置。例如，在自然语言处理任务中，通常会使用大规模的通用数据（如Web文本）作为基础，再逐步增加特定任务或领域的数据
4. **数据质量和多样性优先于数量**：在数据配比的选择中，应优先考虑数据的质量和多样性，而非单纯的数据数量。高质量的特定领域数据可能对模型的表现提升更有帮助
5. **结合模型目标进行调整**：如果模型目标是理解和生成特定领域的文本（如医疗咨询、法律咨询等），可能需要增加特定领域数据的比重。反之，如果目标是通用的对话或生成任务，则可以适当减少特定领域数据的比例。

# 预训练数据处理
:::color5
**<font style="color:#601BDE;">1.数据收集</font>**

:::

1. **数据收集**
    - **数据来源**：
        * **<font style="color:rgb(51, 51, 51);">书籍和文档</font>**<font style="color:rgb(51, 51, 51);">：从项目中使用的书籍和其他文档中提取文本数据。</font>
        * **<font style="color:rgb(51, 51, 51);">网页爬取</font>**<font style="color:rgb(51, 51, 51);">：爬取公共可用的网页内容，如新闻发布、技术文档等。</font>
        * **<font style="color:rgb(51, 51, 51);">开源资源</font>**<font style="color:rgb(51, 51, 51);">：利用开源的公共文本语料库，如Common Crawl等。</font>
    - **数据规模**：
        * <font style="color:rgb(51, 51, 51);">确保收集的数据量足够大，以支持大规模语言模型的训练。通常需要数百GB甚至TB级的文本数据。</font>

:::color5
**<font style="color:#601BDE;">2.数据清洗</font>**

:::

    - **去除低质量文本**：
        * **<font style="color:rgb(51, 51, 51);">去除空白或无效文本</font>**<font style="color:rgb(51, 51, 51);">：过滤掉完全空白的文本片段。</font>
        * **<font style="color:rgb(51, 51, 51);">识别并删除噪声</font>**<font style="color:rgb(51, 51, 51);">：删除包含大量特殊字符、数字或无意义符号的内容。</font>
        * **<font style="color:rgb(51, 51, 51);">去除重复内容</font>**<font style="color:rgb(51, 51, 51);">：使用去重算法，去除重复的文本块，确保数据的多样性。</font>
    - **文本规范化**：
        * **<font style="color:rgb(51, 51, 51);">统一编码</font>**<font style="color:rgb(51, 51, 51);">：确保所有文本使用相同的编码格式（如UTF-8）。</font>
        * **<font style="color:rgb(51, 51, 51);">去除多余空格和标点</font>**<font style="color:rgb(51, 51, 51);">：根据需要，可以使用正则表达式清理文本中的不必要符号。</font>
        * **<font style="color:rgb(51, 51, 51);">分段处理</font>**<font style="color:rgb(51, 51, 51);">：将长文本分割成合理的段落或句子，便于后续处理。</font>

:::color5
**<font style="color:#601BDE;">3.数据增强</font>**

:::

+ **方法**：
    - **<font style="color:rgb(51, 51, 51);">数据多样化</font>**<font style="color:rgb(51, 51, 51);">：通过同义词替换、句式变换等方法，增加训练数据的多样性。</font>
    - **<font style="color:rgb(51, 51, 51);">噪声注入</font>**<font style="color:rgb(51, 51, 51);">：在文本中添加少量的随机噪声，增强模型的鲁棒性。</font>
+ **实施数据增强**：

```python
from nltk.tokenize import word_tokenize
import random

def synonym_replacement(text, n=3):
    words = word_tokenize(text)
    for i in range(n):
        if random.random() < 0.2:
            words[i] = synonym_func(words[i])
    return ' '.join(words)

# 示例同义词替换函数（需替换实际实现）
def synonym_func(word):
    return word  # 示例：实际应集成词库或API进行同义词替换

augmented_text = synonym_replacement("Hello! How are you?")
print(augmented_text)
```

:::color5
**<font style="color:#601BDE;">4.数据质量评估  </font>**[**数据质量评估**](https://www.yuque.com/zhongxian-iiot9/gi3w2u/nlapi8xm5fmsnx3g)

:::

+ **质量评估**：
    - **<font style="color:rgb(51, 51, 51);">文本覆盖率</font>**<font style="color:rgb(51, 51, 51);">：确保数据涵盖了模型所需理解的多种语义和语法结构。</font>
    - **<font style="color:rgb(51, 51, 51);">多样性评估</font>**<font style="color:rgb(51, 51, 51);">：检查数据是否来自多种不同的文本来源和领域。</font>
    - **<font style="color:rgb(51, 51, 51);">去除低质量样本</font>**<font style="color:rgb(51, 51, 51);">：通过人工或自动评估，去除仍然包含噪声或低质量的文本样本。</font>
+ **流畅度检查**：
    - <font style="color:rgb(51, 51, 51);">对预处理后的文本进行人机交互式检查，确保文本流畅、意义连贯。</font>

<font style="color:#646a73;">数据处理流程图</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739253647215-b5ef6d4b-d455-4f2a-b60c-5a301c5e9e9a.png)

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">安全过滤：移除包含个⼈信息、不安全内容、</font><font style="color:#1f2329;">成⼈内容等。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⽂本清理：提取有⽤的⽂本信息</font><font style="color:#1f2329;">，去除杂乱内</font><font style="color:#1f2329;">容。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">去重复：在⽹页级别、⽂本级别、⾏级别进⾏</font><font style="color:#1f2329;">去重。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">质量过滤：使⽤规则和模型，过滤掉低质量的数据。</font>



## 合成数据质量保障
### Self-Consistency <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">假设每个复杂的问题都可以有多种思路来推到出最终的答案</font>**<font style="color:rgb(25, 27, 31);">，这篇文章就是</font>**<font style="color:rgb(25, 27, 31);">探索是否可以用这种思想来提高大模型复杂问题的推理能力</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(25, 27, 31);">对人类来说，不同人思考问题的方式不一样，同样的问题，可以利用多种思路来解决。而当前大语言模型来解决复杂推理问题时，例如COT + LLM的方法主要采用一种贪婪解码（Greedy Decoding）【在每个时间步选择概率最高的词作为输出】的方式来实现。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">提出了一种新的decoding解码策略【self-consistency（自一致性）】，以替代思想链（COT）+ LLM使用的贪婪解码（Greedy Decoding）方法。</font>**<font style="color:rgb(25, 27, 31);">总结成一句话就是首先利用COT生成多个推理路径和答案，最终选择答案出现最多的作为最终答案输出，效果出奇的好。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**paper：**[**https://arxiv.org/pdf/2203.11171**](https://arxiv.org/pdf/2203.11171)

**参考：**[**https://zhuanlan.zhihu.com/p/641370746**](https://zhuanlan.zhihu.com/p/641370746)

:::

**<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：Self-Consistency 是一种提升大语言模型（LLM）推理能力的解码策略，其核心思想是：</font>**<font style="color:rgb(51, 51, 51);">通过多次采样生成不同的推理路径，选择最具一致性的答案作为最终输出</font>**<font style="color:rgb(51, 51, 51);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742883481322-55beef82-52be-408e-b549-3ab0aaa84463.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">self-consistency解码策略假设复杂推理任务一般可以通过多个推理路径获得正确答案，从解码器中抽样生成多样化的推理路径集合，</font>**<font style="color:#74B602;">选择一致性最高的输出结果作为最终答案，降低了贪婪解码方式的单次采样的随机性</font>**
+ <font style="color:rgb(25, 27, 31);">self-consistency</font>**<font style="color:#74B602;">不需要训练额外训练或者辅助模型</font>**<font style="color:rgb(25, 27, 31);">，类似于在单个语言模型上工作的自集成方法</font>
+ <font style="color:rgb(25, 27, 31);">self-consistency 结合</font>[<font style="color:rgb(9, 64, 142);">PaLM-540B</font>](https://zhida.zhihu.com/search?content_id=223629786&content_type=Article&match_order=1&q=PaLM-540B&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">或</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">GPT-3</font>](https://zhida.zhihu.com/search?content_id=223629786&content_type=Article&match_order=1&q=GPT-3&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，算术推理任务中都获得最新的sota水平，GSM8K(Cobbe 等人，2021 年+17.9% )()、SVAMP(Patel 等人，2021 年+11.0%)、AQuA(Ling 等人，2017 年+12.2%)，以及 StrategyQA 等常识性推理任务(Geva 等人，2021 年+6.4%)和 ARC 挑战(Clark 等人，2018 年+3.9%)</font>
+ <font style="color:rgb(25, 27, 31);">self-consistency 在抽样策略和提示缺陷场景下都具有很强的鲁棒性，在一般NLP任务中也能获得性能提升</font>

:::color5
**<font style="color:#601BDE;">2.核心方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">Step1: 思维链提示CoT</font>
+ <font style="color:rgb(25, 27, 31);">Step2: 对语言模型进行多次采样, 生成多个推理路径</font>

```python
def generate_paths(prompt, num_samples=10):
    paths = []
    for _ in range(num_samples):
        path = model.generate(
            prompt,
            temperature=0.7,  # 增加多样性
            max_new_tokens=200
        )
        paths.append(extract_answer(path))
    return paths
```

+ <font style="color:rgb(25, 27, 31);">Step3: 对不同推理路径生成结果基于投票策略选择最一致的答案输出</font>
1. **答案归一化**：
    - <font style="color:rgb(51, 51, 51);">数学问题：标准化数字格式（如 "12.0" → 12）</font>
    - <font style="color:rgb(51, 51, 51);">代码生成：AST抽象语法树比对</font>
    - <font style="color:rgb(51, 51, 51);">文本答案：语义相似度计算（如 BERTScore）</font>
2. **投票机制**：

```python
from collections import defaultdict

def majority_vote(answers):
    counter = defaultdict(int)
    for ans in answers:
        norm_ans = normalize(ans)
        counter[norm_ans] += 1
    return max(counter.items(), key=lambda x: x[1])[0]
```

:::color5
**<font style="color:#601BDE;">3.采样策略</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">UL2-20B and LaMDA-137B， T = 0.5， top-k (k = 40) tokens</font>
+ <font style="color:rgb(25, 27, 31);">PaLM-540B we applied T = 0.7, k = 40</font>
+ <font style="color:rgb(25, 27, 31);">GPT-3，T = 0.7，without top-k</font>

:::color5
**<font style="color:#601BDE;">4.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">提升复杂任务准确率（GSM8K +5.2%）</font>
+ <font style="color:rgb(51, 51, 51);">缓解模型幻觉问题</font>
+ <font style="color:rgb(51, 51, 51);">降低单次生成随机性影响</font>

**<font style="color:rgb(51, 51, 51);">局限</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算成本增加（生成次数 × 单次推理时间）</font>
+ <font style="color:rgb(51, 51, 51);">多数答案可能集体错误</font>
+ <font style="color:rgb(51, 51, 51);">答案归一化存在挑战</font>

:::color5
**<font style="color:#601BDE;">5.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **场景** | **案例** | **效果提升** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">数学推理</font> | <font style="color:rgb(51, 51, 51);">GSM8K、MATH 数据集</font> | <font style="color:rgb(51, 51, 51);">+3%~12%</font> |
| <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">HumanEval、MBPP 基准</font> | <font style="color:rgb(51, 51, 51);">+7%~15%</font> |
| <font style="color:rgb(51, 51, 51);">常识推理</font> | <font style="color:rgb(51, 51, 51);">StrategyQA、ARC-Challenge</font> | <font style="color:rgb(51, 51, 51);">+5%~8%</font> |
| <font style="color:rgb(51, 51, 51);">科学计算</font> | <font style="color:rgb(51, 51, 51);">SciBench、PhysiNet</font> | <font style="color:rgb(51, 51, 51);">+10%~18%</font> |


:::color5
**<font style="color:#601BDE;">6.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Self-consistency 在算术推理, 常识推理，符号推理中都表现高于一般的Cot效果，在ood的数据上[Letter(4)、Coinflip(4)]仍然保持效果增益</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742883818530-515ab015-6780-47aa-b6d5-b3d96fabb702.png)

:::color5
**<font style="color:#601BDE;">7.代码实现</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from collections import defaultdict

class SelfConsistencyGenerator:
    def __init__(self, model_name="gpt2-large"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
    
    def normalize_answer(self, text):
        # 实现答案标准化逻辑
        return text.strip().lower()
    
    def generate_answers(self, prompt, num_samples=10):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        answers = []
        
        with torch.no_grad():
            for _ in range(num_samples):
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=200,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                answers.append(self.normalize_answer(answer))
        
        return answers
    
    def get_consensus(self, answers):
        counts = defaultdict(int)
        for ans in answers:
            counts[ans] += 1
        return max(counts, key=counts.get)

# 使用示例
generator = SelfConsistencyGenerator()
prompt = "Q: 如果一个箱子里有5个红球和3个蓝球，随机抽取2个，都是红球的概率是多少？"
answers = generator.generate_answers(prompt, num_samples=20)
final_answer = generator.get_consensus(answers)
print(f"Consensus Answer: {final_answer}")

```



# 预训练方法
## CLM<font style="color:#6425d0;">（Causal Language Modeling）</font>
<font style="color:#4962db;background-color:#f5f6f7;">定义</font><font style="color:#1f2329;">: CLM是</font><font style="color:#d83931;">因果语⾔建模</font><font style="color:#1f2329;">，训练模型预测⼀句话中的下⼀个词。每个词只能利⽤它前⾯的上下⽂信息。</font>

<font style="color:#5875db;background-color:#f5f6f7;">应用</font><font style="color:#5875db;"> </font><font style="color:#1f2329;">: 它⽤于⽣成任务，例如GPT 模型，模型按顺序⽣成句⼦的每⼀个单词或字符。</font>

<font style="color:#1456f0;">训练方式  </font><font style="color:#1f2329;">: 在训练过程中，模型只能看到到当前单词之前的所有词，不能看到之后的词。这是⼀种⾃回归模型。</font>

<font style="color:#285bdb;">与MLLM的区别</font><font style="color:#1f2329;">：</font>

+ <font style="color:#285bdb;">预测目标</font><font style="color:#1f2329;">：CLM 只预测下⼀个词，⽽MLM 是填补被掩盖的词。</font>
+ <font style="color:#285bdb;">上下文使用</font><font style="color:#1f2329;">：CLM 只能使⽤之前的词，MLM 则可以使⽤整个句⼦的上下⽂（前后词）。</font>
+ <font style="color:#285bdb;">任务类型 </font><font style="color:#1f2329;">：CLM 是⾃回归的，⽤于⽣成任务，MLM 是双向的，⽤于表⽰学习任务。</font>
+ <font style="color:#4d69db;">来源 </font><font style="color:#1f2329;">：“因果语⾔建模”就是上⼀章中说的统计语⾔模型，只使⽤前⾯的词来预测当前词，由NNLM ⾸次运⽤；⽽“遮盖语⾔建模”实际上就是 Word2Vec模型提出的 CBOW。</font>

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 假设我们使用一个简单的线性层作为模型
class SimpleCausalLanguageModel(nn.Module):
    def __init__(self, vocab_size, embed_size):
        super(SimpleCausalLanguageModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.linear = nn.Linear(embed_size, vocab_size)
    
    def forward(self, input_ids):
        embeds = self.embedding(input_ids)
        output = self.linear(embeds)
        return output

# 超参数设置
vocab_size = 10000  # 词汇表大小
embed_size = 128    # 嵌入维度
seq_length = 10     # 序列长度
batch_size = 32     # 批大小

# 模型、损失函数和优化器
model = SimpleCausalLanguageModel(vocab_size, embed_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 准备输入和目标
# 假设输入数据是随机生成的
input_ids = torch.randint(0, vocab_size, (batch_size, seq_length))  # 随机生成的输入
# 目标是将输入向右偏移一个位置（实际应用中可以根据具体情况定义目标）
target_ids = input_ids.clone()
target_ids[:, :-1] = input_ids[:, 1:]  # shift to the right
target_ids[:, -1] = 0  # 最后一个词设为0（可以选择使用一个pad token）

# 训练过程
model.train()
optimizer.zero_grad()
output = model(input_ids)  # 输出 logits

# 计算损失
# target_ids需要reshape为(batch_size * seq_length)
loss = criterion(output.view(-1, vocab_size), target_ids.view(-1))  # 计算交叉熵损失
print(f'Loss: {loss.item()}')

# 反向传播和优化
loss.backward()
optimizer.step()
```

## <font style="color:#6425d0;">MLM（Masked Language Modeling）</font><font style="color:#1f2329;">:</font>
<font style="color:#1456f0;"> </font><font style="color:#5f7ddb;background-color:#f5f6f7;">定义</font><font style="color:#5f7ddb;"> </font><font style="color:#1f2329;">: MLM 是</font><font style="color:#d83931;">掩码语⾔建模</font><font style="color:#1f2329;">，训练模型预测在⼀个句⼦中被随机掩盖（masked）的词。模型可以使⽤整个句⼦的上下⽂，包括掩盖词的前后内容。</font>

<font style="color:#1456f0;"> </font><font style="color:#4e6edb;background-color:#f5f6f7;">应用</font><font style="color:#4e6edb;"> </font><font style="color:#1f2329;">: 它主要⽤于表⽰学习任务，例如 BERT 模型，帮助模型更好地理解整个句⼦的语义。</font>

<font style="color:#1456f0;">训练方式 </font><font style="color:#1f2329;">: </font><font style="color:#de7802;">在训练过程中，句⼦中的⼀些词会被随机掩盖</font><font style="color:#1f2329;">，模型的任务是根据其余词来预测被掩盖的词。这是⼀种双向建模。</font>

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

```python

import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForMaskedLM

# 初始化tokenizer和模型
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

# 准备输入数据
text = "The quick brown fox jumps over the lazy dog."
inputs = tokenizer(text, return_tensors='pt')

# 假设我们只随机掩盖部分token，这里手动指定
mask_idx = 4  # 第5个单词 (从0开始计算，'brown' 被掩盖)
inputs['input_ids'][0, mask_idx] = tokenizer.mask_token_id  # 将掩盖的词用 [MASK] 替换

# 生成labels，用于计算损失
# 这里我们将掩盖的index set为对应word的id，其他的设为-100以忽略
labels = inputs['input_ids'].clone()
labels[0, mask_idx] = inputs['input_ids'][0, mask_idx]  # 保留掩盖的位置
labels[0, :mask_idx] = -100  # 其他位置设置为-100，不计算损失
labels[0, mask_idx+1:] = -100  # 掩盖后面的位置

# 前向传播，计算损失
outputs = model(**inputs, labels=labels)
loss = outputs.loss

# 打印损失
print("MLM Loss:", loss.item())
```





## NSP （Next Sentence Prediction ）
:::color3
<font style="color:rgb(51, 51, 51);">下一代句子预测（Next Sentence Prediction，NSP）是一种预训练任务，旨在训练模型理解文本中的句子关系。模型需要预测给定的两个句子是否是连续的。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

1. **任务结构**：
    - **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：给定两个句子A和B。</font>
    - **<font style="color:rgb(51, 51, 51);">输出</font>**<font style="color:rgb(51, 51, 51);">：预测句子B是否是句子A的下一个句子。</font>
2. **数据准备**：
    - <font style="color:rgb(51, 51, 51);">将两个句子拼接成一个样本，并添加特殊标记（如句与句之间的分隔符）以区分两个句子。</font>
    - <font style="color:rgb(51, 51, 51);">构建正样本和负样本：</font>
        * **<font style="color:rgb(51, 51, 51);">正样本</font>**<font style="color:rgb(51, 51, 51);">：B确实是A的下一个句子。</font>
        * **<font style="color:rgb(51, 51, 51);">负样本</font>**<font style="color:rgb(51, 51, 51);">：B不是A的下一个句子，而是随机选取的其他句子。</font>
3. **模型架构**：
    - <font style="color:rgb(51, 51, 51);">使用双向Transformer模型，如BERT，对两个句子进行编码，生成句子级别的向量表示。</font>
    - <font style="color:rgb(51, 51, 51);">模型会通过这些向量预测两个句子之间的关系。</font>
    - <font style="color:#1f2329;">BERT 通过给定两个句⼦，</font>**<font style="color:#74B602;">要求模型判断这两个句⼦是否为连续上下句</font>**<font style="color:#1f2329;">。这⼀任务帮助 BERT 学习句⼦间的关系，提⾼在问答、推理等任务中的表现。语料中50%的句⼦，选择其相应的下⼀句⼀起形成上下句，作为正样本；其余50%的句⼦随机选择⼀句⾮下⼀句⼀起形成上下句，作为负样本。这种 设定，有利于sentence-level tasks，例如问答。</font>

```python
[CLS] Sentence A [SEP] Sentence B [SEP]
```

    - <font style="color:rgb(51, 51, 51);">随机选择50%的句子对进行NSP训练</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**优点**

1. **增强句子关系理解**：
    - <font style="color:rgb(51, 51, 51);">NSP任务迫使模型理解句子之间的逻辑和语义关系，有助于提升模型的上下文理解能力。</font>
2. **提升文本生成质量**：
    - <font style="color:rgb(51, 51, 51);">在生成文本时，模型能够更好地预测下一个合适的句子，生成连贯的文本。</font>
3. **有效的预训练目标**：
    - <font style="color:rgb(51, 51, 51);">NSP提供了一种监督信号，有助于模型在预训练阶段学习到丰富的语言特征，提升在后续任务中的表现。</font>
4. **适用性广泛**：
    - <font style="color:rgb(51, 51, 51);">NSP可以在多种语言模型上实施，适用于多种自然语言处理任务。</font>

**缺点**

1. **二分类限制**：
    - <font style="color:rgb(51, 51, 51);">NSP仅关注句子是否为下一个句子的关系，无法捕捉更复杂的句子间关系，如对比、因果等。</font>
2. **数据偏差**：
    - <font style="color:rgb(51, 51, 51);">如果训练数据中某些句子关系出现频率较高（如并列关系），模型可能偏向于预测这些关系，导致在处理其他关系时效果不佳。</font>
3. **计算资源需求**：
    - <font style="color:rgb(51, 51, 51);">NSP任务需要大量的数据和计算资源来进行有效的训练，尤其在处理大规模语料库时。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **对话系统**：
    - <font style="color:rgb(51, 51, 51);">在智能对话系统中，NSP帮助模型理解当前输入句子与之前的对话内容之间的关系，从而生成更合适的回复。</font>
2. **文本摘要**：
    - <font style="color:rgb(51, 51, 51);">摘要生成模型通过理解句子关系，生成逻辑连贯且内容完整的摘要。</font>
3. **机器翻译**：
    - <font style="color:rgb(51, 51, 51);">NSP辅助模型理解源语言和目标语言句子之间的对应关系，提升翻译质量。</font>
4. **问答系统**：
    - <font style="color:rgb(51, 51, 51);">模型能够更好地理解问题与上下文之间的关系，提高回答的准确性。</font>
5. **文本蕴含**：
    - <font style="color:rgb(51, 51, 51);">NSP帮助模型判断一个句子是否基于另一个句子成立，提升文本蕴含任务的表现。</font>

:::color5
**<font style="color:#601BDE;">4.使用NSP的模型</font>**

:::

1. **BERT**：
    - <font style="color:rgb(51, 51, 51);">BERT模型在预训练阶段采用了NSP任务，通过预测两个句子是否连续，增强了模型对句子关系的理解，提升了下游任务的性能。</font>
2. **RoBERTa**：
    - <font style="color:rgb(51, 51, 51);">RoBERTa在BERT的基础上进一步优化了预训练策略，也采用了NSP任务，并通过更大的训练数据和更强的计算资源提升了模型效果。</font>
3. **DeBERTa**：
    - <font style="color:rgb(51, 51, 51);">DeBERTa结合了NSP任务和强化学习，通过端到端的优化提升了模型的预训练效果。</font>

```python
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
import numpy as np

# 定义数据集类
class NSPDataset(Dataset):
    def __init__(self, sentences, labels, tokenizer, max_len):
        self.sentences = sentences
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        sent1, sent2 = self.sentences[idx]
        label = self.labels[idx]
        # 将两个句子拼接，并添加特殊标记'[SEP]'
        combined = sent1 + ' ' + self.tokenizer.sep_token + ' ' + sent2
        # 分词并编码
        encoding = self.tokenizer(combined, truncation=True, padding='max_length', max_length=self.max_len, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        # 转换为LongTensor
        input_ids = input_ids.long()
        attention_mask = attention_mask.long()
        label = torch.tensor(label, dtype=torch.long)
        return input_ids, attention_mask, label

# 定义模型
class NSPModel(nn.Module):
    def __init__(self, model_name, dropout=0.1):
        super(NSPModel, self).__init__()
        # 加载BERT模型
        self.bert = BertModel.from_pretrained(model_name)
        # 添加额外的 dropout层
        self.dropout = nn.Dropout(dropout)
        # 分类层
        self.classifier = nn.Linear(self.bert.config.hidden_size, 2)

    def forward(self, input_ids, attention_mask):
        # 获取BERT的输出
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        # 句子表示取[CLS] token的位置
        pooled_output = outputs.last_hidden_state[:, 0, :]
        # 应用 dropout
        pooled_output = self.dropout(pooled_output)
        # 分类
        logits = self.classifier(pooled_output)
        return logits

# 定义训练函数
def train_model(model, train_loader, val_loader, optimizer, scheduler, device, num_epochs=3):
    best_val_loss = float('inf')
    for epoch in range(num_epochs):
        model.train()
        for batch in train_loader:
            input_ids, attention_mask, labels = batch
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask)
            loss = nn.CrossEntropyLoss()(outputs, labels)
            loss.backward()
            optimizer.step()

        # 验证阶段
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids, attention_mask, labels = batch
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                labels = labels.to(device)
                
                outputs = model(input_ids, attention_mask)
                loss = nn.CrossEntropyLoss()(outputs, labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            # 保存模型
            torch.save(model.state_dict(), 'best_nsp_model.pth')
            
    print(f"训练完成，最佳验证损失：{best_val_loss}")

# 主程序
def main():
    # 参数设置
    model_name = 'bert-base-uncased'
    max_len = 128
    batch_size = 16
    learning_rate = 2e-5
    num_epochs = 3

    # 初始化tokenizer和模型
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = NSPModel(model_name)

    # 准备数据
    # 假设sentences_pairs和labels已经准备好
    # sentences_pairs = [('The sky is blue.', 'The sun is shining.'),
    #                  ('A cat is playing.', 'The dog is sleeping.')]
    # labels = [1, 0]  # 1表示是下一个句子，0表示否
    # train_dataset = NSPDataset(sentences_pairs, labels, tokenizer, max_len)
    # train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # 初始化优化器和学习率调度器
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.5)

    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    # 开始训练
    train_model(model, train_loader, val_loader, optimizer, scheduler, device, num_epochs)

if __name__ == '__main__':
    main()

```



## <font style="color:rgb(0, 0, 0);">LM（语言模型生成损失）</font>
2. **<font style="color:rgb(51, 51, 51);">生成式预训练</font>**
    - **<font style="color:rgb(51, 51, 51);">输入构造</font>**<font style="color:rgb(51, 51, 51);">：将投影后的视觉特征作为前缀（Visual Prompt）拼接到语言模型输入前</font>
    - **<font style="color:rgb(51, 51, 51);">训练任务</font>**<font style="color:rgb(51, 51, 51);">：基于视觉条件的文本生成（Captioning、VQA 等）</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：标准语言模型的自回归损失  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074437873-ff037058-da54-4a67-8e6c-95d6f8f2a84c.png)

# 多模态大模型预训练
## <font style="color:rgb(0, 0, 0);">ITC（图文对比损失）</font>
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：对比图像特征与文本特征相似度</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074304341-6d649817-383a-478b-b27d-7ab7bad5d899.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 s(I,T)为图像-文本相似度，τ 为温度系数</font>

<font style="color:rgb(25, 27, 31);">本文的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">image-text</font>`<font style="color:rgb(25, 27, 31);">对比损失函数类似于</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">CLIP</font>`<font style="color:rgb(25, 27, 31);">。给定一个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">batch</font>`<font style="color:rgb(25, 27, 31);">的图像和文本，最大化正确匹配的文本和图像的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">cosine</font>`<font style="color:rgb(25, 27, 31);">相似度，最小化其他不匹配的对。这是通过将 </font><font style="color:rgb(25, 27, 31);">hCLS,I</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">hCLS,T</font><font style="color:rgb(25, 27, 31);"> 投影至嵌入空间，然后使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">L2</font>`<font style="color:rgb(25, 27, 31);">规范化，点积和带有温度系数的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">softmax</font>`<font style="color:rgb(25, 27, 31);">损失函数。</font><font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(25, 27, 31);">大模型通常会使用多</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">GPU</font>`<font style="color:rgb(25, 27, 31);">数据并行，这样一个batch内的样本会被分割到不同的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">GPU</font>`<font style="color:rgb(25, 27, 31);">上。当为了图像和文本对比目标函数收集</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">embedding</font>`<font style="color:rgb(25, 27, 31);">，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">CLIP</font>`<font style="color:rgb(25, 27, 31);">仅反向传播局部</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">GPU</font>`<font style="color:rgb(25, 27, 31);">上对比损失函数。相反，通过补充实验可以发现，在所有</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">GPU</font>`<font style="color:rgb(25, 27, 31);">上执行完全的反向传播要比局部反向传播性能高很多。这里称之为全局对比损失函数 </font><font style="color:rgb(25, 27, 31);">LGC</font><font style="color:rgb(25, 27, 31);"> 。</font>

## <font style="color:rgb(0, 0, 0);">ITM（图文匹配损失）</font>
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：二分类判断图像-文本对是否匹配</font>
    - **<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">正样本：原始配对文本</font>
        * <font style="color:rgb(51, 51, 51);">负样本：通过 ITC 相似度选择最难的负样本（Hard Negative Mining）</font>

<font style="color:rgb(25, 27, 31);">最后，作者添加了一个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">image-text</font>`<font style="color:rgb(25, 27, 31);">匹配损失函数 </font><font style="color:rgb(25, 27, 31);">LITM</font><font style="color:rgb(25, 27, 31);"> ，先前的预训练工作也会使用这个损失函数。在预训练过程中，会输入带有匹配和不匹配</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">image-text对</font>`<font style="color:rgb(25, 27, 31);">样本的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">batch</font>`<font style="color:rgb(25, 27, 31);">。在多模态编码器的输出 </font><font style="color:rgb(25, 27, 31);">hCLS,M</font><font style="color:rgb(25, 27, 31);"> 上应用一个分类器来决定输入图像和文本是否彼此匹配。</font>

## Image Captioning（图像描述生成）
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：以图像特征为条件生成文本描述</font>
    - **<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">：使用因果掩码的交叉注意力机制</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：交叉熵损失</font>





## MIM （Masked Image Model）
<font style="color:rgb(25, 27, 31);">在单模态图像数据集上，使用BEiT中的矩阵块</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">masking</font>`<font style="color:rgb(25, 27, 31);">遮蔽图像的一部分</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">并且从其他</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">中重构他们。首先使用预训练的dVAE tokenizer对输入图像进行tokenized，然后在图像编码器输出 </font><font style="color:rgb(25, 27, 31);">{hI}</font><font style="color:rgb(25, 27, 31);"> 上应用一个分类器来预测被遮蔽</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">。</font>

## MMM（Masked Multimodal Modeling）
<font style="color:rgb(51, 51, 51);">联合掩码文本+图像块，预测被掩内容。</font>

<font style="color:rgb(25, 27, 31);">虽然先前的视觉语言预训练方法通过从多模态输入中重构被遮蔽的token来建模文本模态，它们中大多数并不涉及以端到端方式在像素级上直接进行模态的掩码学习。这里，作者引入了一个新颖的遮蔽多模态建模MMM预训练目标函数 </font><font style="color:rgb(25, 27, 31);">LMMM</font><font style="color:rgb(25, 27, 31);"> ，该目标函数同时会遮蔽图像的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">和文本的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tokens</font>`<font style="color:rgb(25, 27, 31);">，并在两种模态中联合工作。</font><font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(25, 27, 31);">特别地，给定一个图像和文本输入，首先会使用预训练的</font>[<font style="color:rgb(9, 64, 142);">dVAE tokenizer</font>](https://zhida.zhihu.com/search?content_id=221292858&content_type=Article&match_order=1&q=dVAE+tokenizer&zhida_source=entity)<font style="color:rgb(25, 27, 31);">将输入图像转换为</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">，该</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tokenizer</font>`<font style="color:rgb(25, 27, 31);">会将每个图像</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patch</font>`<font style="color:rgb(25, 27, 31);">映射为类似词典的视觉</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">codebook</font>`<font style="color:rgb(25, 27, 31);">的一个索引。然后，基于</font>[<font style="color:rgb(9, 64, 142);">BEiT</font>](https://zhida.zhihu.com/search?content_id=221292858&content_type=Article&match_order=1&q=BEiT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">中的矩形块图像区域来替换图像</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">的子集，像BERT那样将15%的文本token使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[MASK]</font>`<font style="color:rgb(25, 27, 31);">进行遮蔽。然后，基于多模态编码器输入 </font><font style="color:rgb(25, 27, 31);">{hM}</font><font style="color:rgb(25, 27, 31);"> ，应用多层感知机来预测被遮蔽图像</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">的视觉</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">codebook</font>`<font style="color:rgb(25, 27, 31);">索引，或者是被遮蔽文本</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tokens</font>`<font style="color:rgb(25, 27, 31);">的词典索引。</font><font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(25, 27, 31);">这个目标函数被看作是多模态遮蔽语言模型的扩展，其合并了图像端的遮蔽。在本文实验中，作者发现处理对比损失预训练，MMM预训练还可以带来改善，特别是对VQA这样的多模态下游任务。注意，在不适用任何</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">masking</font>`<font style="color:rgb(25, 27, 31);">的情况下，在图像</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">patches</font>`<font style="color:rgb(25, 27, 31);">和文本</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tokens</font>`<font style="color:rgb(25, 27, 31);">上应用全局对比损失函数，其会与MMM损失分开传递至图像编码器和文本编码器。</font>



