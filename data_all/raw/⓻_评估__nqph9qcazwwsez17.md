# ⓻ 评估

<!-- source: yuque://zhongxian-iiot9/hlyypb/nqph9qcazwwsez17 -->

# 训练评估<font style="color:#D22D8D;"> </font>
:::info
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">大型语言模型（LLM）的训练通常分为预训练（PT）、监督微调（SFT）和基于人类反馈的强化学习（RLHF）三个阶段。每个阶段的评估目标和方法有所不同，以下是详细的评估指标和方法。</font>

:::

**总结：**

+ **<font style="color:rgb(51, 51, 51);">预训练</font>**<font style="color:rgb(51, 51, 51);">：关注基础能力，以困惑度和零样本任务为主。</font>
+ **<font style="color:rgb(51, 51, 51);">SFT</font>**<font style="color:rgb(51, 51, 51);">：侧重任务性能和对齐程度，依赖人工评估。</font>
+ **<font style="color:rgb(51, 51, 51);">RLHF</font>**<font style="color:rgb(51, 51, 51);">：强调安全性和人类偏好，需结合自动检测与人工审核。</font>
+ **<font style="color:rgb(51, 51, 51);">趋势</font>**<font style="color:rgb(51, 51, 51);">：评估逐渐从单一指标转向多维度、动态化，并重视实际应用场景中的表现。</font>

## 预训练评估<font style="color:#D22D8D;"> </font>
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

## SFT评估<font style="color:#D22D8D;"> </font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">评估大型语言模型（LLM）在监督式微调（Supervised Fine-Tuning, SFT）后的效果，需要结合</font>**<font style="color:rgb(51, 51, 51);">任务目标、领域特性</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">模型能力</font>**<font style="color:rgb(51, 51, 51);">设计多维度的评估体系。</font>

:::

:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 任务相关指标</font>**

+ **分类/判别任务**
    - **<font style="color:rgb(51, 51, 51);">准确率（Accuracy）</font>**<font style="color:rgb(51, 51, 51);">：简单但直观，适用于平衡数据集。</font>
    - **<font style="color:rgb(51, 51, 51);">F1-Score</font>**<font style="color:rgb(51, 51, 51);">：对不平衡数据更鲁棒，综合 Precision 和 Recall。</font>
    - **<font style="color:rgb(51, 51, 51);">AUC-ROC</font>**<font style="color:rgb(51, 51, 51);">：评估模型对类别排序能力，适用于概率输出任务（如情感分析）。</font>
+ **生成任务**
    - **<font style="color:rgb(51, 51, 51);">BLEU</font>**<font style="color:rgb(51, 51, 51);">：基于 n-gram 匹配，常用于机器翻译或文本摘要，但对语义多样性敏感。</font>
    - **<font style="color:rgb(51, 51, 51);">ROUGE</font>**<font style="color:rgb(51, 51, 51);">（如 ROUGE-L）：通过召回率评估生成内容与参考文本的重叠度，适合长文本生成。</font>
    - **<font style="color:rgb(51, 51, 51);">METEOR</font>**<font style="color:rgb(51, 51, 51);">：引入词义匹配（如同义词）和句法结构，比 BLEU 更贴近人类评分。</font>
+ **代码任务**
    - **<font style="color:rgb(51, 51, 51);">Pass@k</font>**<font style="color:rgb(51, 51, 51);">（HumanEval）：生成代码通过单元测试的比例（如 Pass@1 即一次生成成功率）。</font>
    - **<font style="color:rgb(51, 51, 51);">CodeBLEU</font>**<font style="color:rgb(51, 51, 51);">：结合语法树和变量匹配的代码生成评估指标。</font>

**<font style="color:rgb(51, 51, 51);">2. 通用指标</font>**

+ **困惑度（Perplexity, PPL）**  
反映模型对测试数据的概率拟合程度，但需注意与人类评价的相关性可能较弱。
+ **指令遵循率**  
对用户指令（如格式、内容约束）的遵守程度，需人工或规则判定（如 AlpacaEval）。
+ **多样性（Distinct-n）**  
生成文本的词汇多样性，避免重复或模板化响应。

**<font style="color:rgb(51, 51, 51);">3. 人类评估</font>**

+ **<font style="color:rgb(51, 51, 51);">质量评分</font>**<font style="color:rgb(51, 51, 51);">（如流畅性、相关性、信息量）  
</font><font style="color:rgb(51, 51, 51);">由专家或众包人员打分（常用 1-5 Likert 量表）。</font>
+ **<font style="color:rgb(51, 51, 51);">对比评估</font>**<font style="color:rgb(51, 51, 51);">（如 A/B Test）  
</font><font style="color:rgb(51, 51, 51);">直接对比 SFT 前后模型输出的优劣。</font>

:::color5
**<font style="color:#601BDE;">2.评估方法</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 任务内测试</font>**

+ **<font style="color:rgb(51, 51, 51);">Zero-Shot</font>**<font style="color:rgb(51, 51, 51);">：直接使用 SFT 后模型在测试集上预测，评估任务适配性。</font>
+ **<font style="color:rgb(51, 51, 51);">Few-Shot</font>**<font style="color:rgb(51, 51, 51);">：提供少量示例（In-Context Learning），测试模型泛化能力。</font>

**<font style="color:rgb(51, 51, 51);">2. 跨领域泛化测试</font>**

<font style="color:rgb(51, 51, 51);">在未参与 SFT 的领域数据上测试模型表现，验证是否过拟合。</font>

```python
例：用金融领域 SFT 的模型，测试其在医疗文本上的表现。
```

**<font style="color:rgb(51, 51, 51);">3. 能力退化检测</font>**

<font style="color:rgb(51, 51, 51);">对比 SFT 前后模型在通用任务（如常识推理、多轮对话）上的表现，避免灾难性遗忘。</font>

**<font style="color:rgb(51, 51, 51);">4. 对抗测试</font>**

<font style="color:rgb(51, 51, 51);">构造边缘案例（如模糊指令、对抗性输入），测试模型鲁棒性。</font>

:::color5
**<font style="color:#601BDE;">3.常用Benchmark</font>**

:::

| **Benchmark** | **场景** | **评估重点** | **QWEN 适配示例** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">MMLU</font>** | <font style="color:rgb(51, 51, 51);">多学科问答</font> | <font style="color:rgb(51, 51, 51);">57 个学科领域的准确率</font> | <font style="color:rgb(51, 51, 51);">测试 SFT 后模型的知识广度和推理能力</font> |
| **<font style="color:rgb(51, 51, 51);">HumanEval</font>** | <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">Python 函数生成的 Pass@k</font> | <font style="color:rgb(51, 51, 51);">评估代码生成和逻辑实现能力</font> |
| **<font style="color:rgb(51, 51, 51);">AlpacaEval</font>** | <font style="color:rgb(51, 51, 51);">指令跟随</font> | <font style="color:rgb(51, 51, 51);">对比 GPT-4 的胜率（Win Rate）</font> | <font style="color:rgb(51, 51, 51);">验证指令理解与执行质量</font> |
| **<font style="color:rgb(51, 51, 51);">MT-Bench</font>** | <font style="color:rgb(51, 51, 51);">多轮对话</font> | <font style="color:rgb(51, 51, 51);">多轮交互的连贯性和信息量</font> | <font style="color:rgb(51, 51, 51);">测试对话场景的 SFT 优化效果</font> |
| **<font style="color:rgb(51, 51, 51);">GSM8K</font>** | <font style="color:rgb(51, 51, 51);">数学推理</font> | <font style="color:rgb(51, 51, 51);">多步骤数学问题解决准确率</font> | <font style="color:rgb(51, 51, 51);">验证逻辑推理能力提升</font> |
| **<font style="color:rgb(51, 51, 51);">TruthfulQA</font>** | <font style="color:rgb(51, 51, 51);">真实性</font> | <font style="color:rgb(51, 51, 51);">生成答案的真实性（避免幻觉）</font> | <font style="color:rgb(51, 51, 51);">检测 SFT 后模型的可靠性</font> |


:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">以QWEN为例的评估实践</font>**

:::

<font style="color:rgb(51, 51, 51);">以 </font>**<font style="color:rgb(51, 51, 51);">QWEN-7B</font>**<font style="color:rgb(51, 51, 51);"> 为例，其 SFT 评估通常包含以下步骤：</font>

1. **<font style="color:rgb(51, 51, 51);">任务性能验证</font>**
    - <font style="color:rgb(51, 51, 51);">在目标领域（如客服对话）测试任务指标（如意图识别 F1、响应相关性 ROUGE-L）。</font>
2. **<font style="color:rgb(51, 51, 51);">通用能力保留测试</font>**
    - <font style="color:rgb(51, 51, 51);">使用 MMLU 和 C-Eval 确保知识推理能力未退化。</font>
3. **<font style="color:rgb(51, 51, 51);">指令遵循评估</font>**
    - <font style="color:rgb(51, 51, 51);">通过 AlpacaEval 2.0 对比微调前后的胜率，优化提示工程后的 Win Rate 达 80%+（基线为 70%）。</font>
4. **<font style="color:rgb(51, 51, 51);">代码能力测试</font>**
    - <font style="color:rgb(51, 51, 51);">在 HumanEval 上 Pass@1 提升至 35%（原始模型为 25%）。</font>
5. **<font style="color:rgb(51, 51, 51);">人工评测</font>**
    - <font style="color:rgb(51, 51, 51);">由领域专家对 100 条样本打分，评估生成内容的专业性和安全性。</font>

:::color5
**<font style="color:#601BDE;">5.挑战与改进方向</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据污染</font>**<font style="color:rgb(51, 51, 51);">：确保测试数据未出现在训练集中（可通过 N-gram 重叠检测）。</font>
2. **<font style="color:rgb(51, 51, 51);">指标局限性</font>**<font style="color:rgb(51, 51, 51);">：自动指标（如 BLEU）可能与人类评价存在偏差，需结合人工评估。</font>
3. **<font style="color:rgb(51, 51, 51);">领域适配性</font>**<font style="color:rgb(51, 51, 51);">：针对垂直领域（如法律、医学）需设计定制化评测集。</font>
4. **<font style="color:rgb(51, 51, 51);">效率考量</font>**<font style="color:rgb(51, 51, 51);">：SFT 后模型推理速度是否满足业务需求（如 QPS/TPS）。</font>



## RLHF评估<font style="color:#D22D8D;"> </font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">评估大型语言模型（LLM）在通过RLHF（基于人类反馈的强化学习）后的效果需要从多个维度综合考量</font>**<font style="color:rgb(51, 51, 51);">，</font>****<font style="color:#ED740C;">包括生成质量、安全性、对齐性、任务完成度等</font>****<font style="color:rgb(51, 51, 51);">。</font>**<font style="color:rgb(51, 51, 51);"></font>

:::

:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 生成质量</font>**

+ **<font style="color:rgb(51, 51, 51);">Perplexity（困惑度）</font>**<font style="color:rgb(51, 51, 51);">：衡量模型对文本的预测能力，数值越低表示模型对数据的拟合越好（但可能无法完全反映生成质量）。</font>
+ **<font style="color:rgb(51, 51, 51);">BLEU/ROUGE/METEOR</font>**<font style="color:rgb(51, 51, 51);">：文本生成任务的经典指标，用于衡量生成文本与参考文本的匹配度，适用于翻译、摘要等任务。</font>
+ **<font style="color:rgb(51, 51, 51);">Human Preference Score</font>**<font style="color:rgb(51, 51, 51);">：通过人工标注或众包评估生成结果的流畅性、相关性和有用性。</font>
+ **<font style="color:rgb(51, 51, 51);">Diversity（多样性）</font>**<font style="color:rgb(51, 51, 51);">：生成结果的词汇多样性和内容新颖性，例如通过Unique N-gram Ratio衡量。</font>

**<font style="color:rgb(51, 51, 51);">2. 安全性与对齐性</font>**

+ **<font style="color:rgb(51, 51, 51);">Toxicity Score</font>**<font style="color:rgb(51, 51, 51);">：使用分类模型（如Perspective API）检测生成内容中的有害性、攻击性语言。</font>
+ **<font style="color:rgb(51, 51, 51);">Ethical Alignment</font>**<font style="color:rgb(51, 51, 51);">：评估模型是否遵循伦理规范（例如拒绝生成违法、歧视性内容），常用基准如ETHICS数据集。</font>
+ **<font style="color:rgb(51, 51, 51);">Sensitive Content Rate</font>**<font style="color:rgb(51, 51, 51);">：统计生成内容中涉及敏感话题（如暴力、政治）的比例。</font>

**<font style="color:rgb(51, 51, 51);">3. 任务完成度</font>**

+ **<font style="color:rgb(51, 51, 51);">准确率（Accuracy）</font>**<font style="color:rgb(51, 51, 51);">：在问答、数学推理等任务中的正确率，例如MMLU（大规模多任务语言理解）中的表现。</font>
+ **<font style="color:rgb(51, 51, 51);">任务成功率</font>**<font style="color:rgb(51, 51, 51);">：如代码生成（HumanEval）、工具调用（如API使用）的成功率。</font>

**<font style="color:rgb(51, 51, 51);">4. 指令遵循能力</font>**

+ **<font style="color:rgb(51, 51, 51);">Instruction Compliance</font>**<font style="color:rgb(51, 51, 51);">：模型是否严格遵循复杂指令，例如多步骤任务或格式约束。</font>
+ **<font style="color:rgb(51, 51, 51);">AlpacaEval</font>**<font style="color:rgb(51, 51, 51);">：通过人工或自动化评估模型在开放指令任务中的表现。</font>

:::color5
**<font style="color:#601BDE;">2.评估方法</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 自动化评估</font>**

+ **<font style="color:rgb(51, 51, 51);">静态测试集</font>**<font style="color:rgb(51, 51, 51);">：在预定义的数据集（如MMLU、HellaSwag）上测试模型性能。</font>
+ **<font style="color:rgb(51, 51, 51);">动态生成测试</font>**<font style="color:rgb(51, 51, 51);">：通过Prompt模板生成多样化输入，评估模型输出的质量和安全性。</font>
+ **<font style="color:rgb(51, 51, 51);">对抗性测试</font>**<font style="color:rgb(51, 51, 51);">：设计意图绕过模型安全机制的输入（例如越狱Prompt），测试防御能力。</font>

**<font style="color:rgb(51, 51, 51);">2. 人工评估</font>**

+ **<font style="color:rgb(51, 51, 51);">人工打分</font>**<font style="color:rgb(51, 51, 51);">：标注员对生成结果的质量、安全性、有用性进行打分（例如1-5分）。</font>
+ **<font style="color:rgb(51, 51, 51);">A/B测试</font>**<font style="color:rgb(51, 51, 51);">：让用户对比不同模型（如RLHF前后版本）的输出，选择更优结果。</font>

**<font style="color:rgb(51, 51, 51);">3. 对比实验</font>**

+ **<font style="color:rgb(51, 51, 51);">基线模型对比</font>**<font style="color:rgb(51, 51, 51);">：比较RLHF微调后的模型与原始预训练模型、其他开源模型（如LLaMA、ChatGLM）的表现。</font>
+ **<font style="color:rgb(51, 51, 51);">消融实验</font>**<font style="color:rgb(51, 51, 51);">：分析RLHF各阶段（如奖励模型训练、PPO优化）对最终效果的贡献。</font>

:::color5
**<font style="color:#601BDE;">3.常用Benchmark</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 通用能力</font>**

+ **<font style="color:rgb(51, 51, 51);">MMLU</font>**<font style="color:rgb(51, 51, 51);">：涵盖57个学科的多选题数据集，测试模型的知识广度和推理能力。</font>
+ **<font style="color:rgb(51, 51, 51);">HellaSwag/ARC</font>**<font style="color:rgb(51, 51, 51);">：常识推理和科学知识问答数据集。</font>
+ **<font style="color:rgb(51, 51, 51);">GSM8K</font>**<font style="color:rgb(51, 51, 51);">：数学应用题测试集，评估多步推理能力。</font>

**<font style="color:rgb(51, 51, 51);">2. 安全性</font>**

+ **<font style="color:rgb(51, 51, 51);">RealToxicityPrompts</font>**<font style="color:rgb(51, 51, 51);">：包含潜在有害Prompt的数据集，测试模型生成有害内容的概率。</font>
+ **<font style="color:rgb(51, 51, 51);">ETHICS</font>**<font style="color:rgb(51, 51, 51);">：评估模型对伦理场景的理解和应对。</font>

**<font style="color:rgb(51, 51, 51);">3. 指令遵循</font>**

+ **<font style="color:rgb(51, 51, 51);">AlpacaEval</font>**<font style="color:rgb(51, 51, 51);">：基于Alpaca指令集的自动化评估框架。</font>
+ **<font style="color:rgb(51, 51, 51);">Vicuna Benchmark</font>**<font style="color:rgb(51, 51, 51);">：通过人工打分评估开放领域对话能力。</font>

**<font style="color:rgb(51, 51, 51);">4. 生成质量</font>**

+ **<font style="color:rgb(51, 51, 51);">SummEval</font>**<font style="color:rgb(51, 51, 51);">：摘要任务评估数据集，结合人工打分和自动指标。</font>
+ **<font style="color:rgb(51, 51, 51);">HumanEval</font>**<font style="color:rgb(51, 51, 51);">：代码生成任务的功能正确性评估。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">以QWEN为例的评估实践</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 评估指标</font>**

+ **<font style="color:rgb(51, 51, 51);">生成质量</font>**<font style="color:rgb(51, 51, 51);">：在AlpacaEval和Vicuna Benchmark中对比微调前后的输出质量。</font>
+ **<font style="color:rgb(51, 51, 51);">安全性</font>**<font style="color:rgb(51, 51, 51);">：使用RealToxicityPrompts测试有害内容生成率，并通过人工审核过滤敏感回答。</font>
+ **<font style="color:rgb(51, 51, 51);">任务完成度</font>**<font style="color:rgb(51, 51, 51);">：在MMLU和GSM8K上测试知识能力，在代码生成（HumanEval）中评估实用性。</font>

**<font style="color:rgb(51, 51, 51);">2. 评估方法</font>**

+ **<font style="color:rgb(51, 51, 51);">多阶段对比</font>**<font style="color:rgb(51, 51, 51);">：比较预训练模型（Qwen-7B）、SFT模型（Qwen-7B-Chat）、RLHF微调后的最终版本。</font>
+ **<font style="color:rgb(51, 51, 51);">人工标注</font>**<font style="color:rgb(51, 51, 51);">：通过众包平台对生成结果进行偏好评分，例如“有用性”和“安全性”的平衡。</font>

**<font style="color:rgb(51, 51, 51);">3. Benchmark表现</font>**

+ **<font style="color:rgb(51, 51, 51);">MMLU</font>**<font style="color:rgb(51, 51, 51);">：QWEN-72B在微调后可能在MMLU上达到约80%的准确率，接近GPT-3.5水平。</font>
+ **<font style="color:rgb(51, 51, 51);">安全性测试</font>**<font style="color:rgb(51, 51, 51);">：通过对抗性Prompt测试，RLHF版本的有害内容生成率显著低于原始模型。</font>
+ **<font style="color:rgb(51, 51, 51);">中文任务</font>**<font style="color:rgb(51, 51, 51);">：在CLUE和C-Eval等中文基准测试中验证多语言能力。</font>

**<font style="color:rgb(51, 51, 51);">4. 实际应用指标</font>**

+ **<font style="color:rgb(51, 51, 51);">用户满意度</font>**<font style="color:rgb(51, 51, 51);">：在阿里云内部或合作方场景中收集用户反馈，优化模型对齐性。</font>
+ **<font style="color:rgb(51, 51, 51);">推理效率</font>**<font style="color:rgb(51, 51, 51);">：监控生成速度和资源消耗（如显存占用），确保落地可行性。</font>

:::color5
**<font style="color:#601BDE;">5.挑战与改进方向</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">评估偏差</font>**<font style="color:rgb(51, 51, 51);">：自动指标可能无法完全反映人类偏好，需结合动态人工评估。</font>
2. **<font style="color:rgb(51, 51, 51);">长尾场景覆盖</font>**<font style="color:rgb(51, 51, 51);">：模型可能在常见任务表现良好，但对罕见指令或复杂伦理场景仍需优化。</font>
3. **<font style="color:rgb(51, 51, 51);">多语言评估</font>**<font style="color:rgb(51, 51, 51);">：需扩展对中文、小语种的支持测试（如QWEN的中文能力专项评估）。</font>

# 数据集评估<font style="color:#D22D8D;"> </font>
## 评估指标<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：在评估数据集的质量时，可以从以下几个关键方面进行评估：</font>

1. **<font style="color:rgb(51, 51, 51);">数据多样性</font>**
2. **<font style="color:rgb(51, 51, 51);">数据平衡性</font>**
3. **<font style="color:rgb(51, 51, 51);">数据完整性</font>**
4. **<font style="color:rgb(51, 51, 51);">数据一致性</font>**
5. **<font style="color:rgb(51, 51, 51);">数据与任务的适合性</font>**
6. **<font style="color:rgb(51, 51, 51);">标注准确性</font>**

:::

:::color5
**<font style="color:#601BDE;">1.数据多样性</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：数据多样性指的是数据集中包含的各种样本是否足够多样化，能否覆盖不同的特征、类别或场景。多样化的数据有助于模型更好地泛化，避免过拟合特定数据分布。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">类别分布</font>**<font style="color:rgb(51, 51, 51);">：检查各个类别样本的数量是否均衡。</font>
+ **<font style="color:rgb(51, 51, 51);">特征多样性</font>**<font style="color:rgb(51, 51, 51);">：评估数据中特征的分布情况，确保没有某一特征主导数据集。</font>

```python
import pandas as pd
from collections import Counter

def assess_data_diversity(dataset, label_column):
    # 统计各类别的样本数量
    class_distribution = dataset[label_column].value_counts()
    print("Class Distribution:")
    print(class_distribution)
    
    # 统计每个类别中的特征分布
    if 'text' in dataset.columns:
        # 示例：统计文本长度分布
        text_lengths = dataset['text'].apply(len)
        print("\nText Length Distribution:")
        print(text_lengths.describe())
    
    # 统计其他特征的分布（如适用）
    # ...
```

:::color5
**<font style="color:#601BDE;">2.数据平衡性</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：数据平衡性指的是数据集中不同类别或样本的数量是否均衡。不平衡的数据可能导致模型偏向多数类，降低整体性能。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">类别分布比例</font>**<font style="color:rgb(51, 51, 51);">：计算各类别样本数量占总样本的比例。</font>
+ **<font style="color:rgb(51, 51, 51);">K分布检验</font>**<font style="color:rgb(51, 51, 51);">：使用统计方法检验数据是否符合均匀分布。</font>
+ **<font style="color:rgb(51, 51, 51);">重采样方法</font>**<font style="color:rgb(51, 51, 51);">：应用过采样或欠采样技术平衡数据。</font>

```python
from imblearn.metrics import classification_report_imbalanced
from imblearn import under_sampling, over_sampling
import matplotlib.pyplot as plt

def assess_data_balance(dataset, label_column):
    # 统计各类别样本数量
    class_counts = dataset[label_column].value_counts()
    print("Class Counts:", class_counts)
    
    # 绘制类别分布直方图
    plt.figure(figsize=(10, 6))
    class_counts.plot(kind='bar')
    plt.title('Class Distribution')
    plt.show()
    
    # 使用K分布检验
    from scipy.stats import chi2_contingency
    observed = class_counts.values
    expected = [sum(class_counts) / len(class_counts)] * len(class_counts)
    
    chi2, p, dof, _ = chi2_contingency([observed])
    print(f"Chi-square test p-value: {p}")
    
    # 应用欠采样或过采样
    if len(class_counts) == 2:
        # 示例：使用随机欠采样平衡二分类数据
        under_sampler = under_sampling.RandomUnderSampler(random_state=42)
        X_res, y_res = under_sampler.fit_resample(dataset.drop(label_column, axis=1), dataset[label_column])
        print("\nUnder-sampled Dataset Shape:", X_res.shape)
        print("Under-sampled Classes:", pd.Series(y_res).value_counts())
    elif len(class_counts) > 2:
        # 示例：使用过采样平衡多分类数据
        over_sampler = over_sampling.RandomOverSampler(random_state=42)
        X_res, y_res = over_sampler.fit_resample(dataset.drop(label_column, axis=1), dataset[label_column])
        print("\nOver-sampled Dataset Shape:", X_res.shape)
        print("Over-sampled Classes:", pd.Series(y_res).value_counts())
```

:::color5
**<font style="color:#601BDE;">3.数据完整性</font>**

:::

**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：数据完整性指的是数据中是否存在缺失值或不完整记录，确保数据能够支持完整的模型训练和推理。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">缺失值检测</font>**<font style="color:rgb(51, 51, 51);">：识别数据中的缺失值分布情况。</font>
+ **<font style="color:rgb(51, 51, 51);">字段完整性检查</font>**<font style="color:rgb(51, 51, 51);">：确保所有字段都有有效值。</font>
+ **<font style="color:rgb(51, 51, 51);">数据记录完整性</font>**<font style="color:rgb(51, 51, 51);">：确保每条记录都包含所有必要信息。</font>

:::color5
**<font style="color:#601BDE;">4.数据与任务的适合性</font>**

:::

<font style="color:rgb(51, 51, 51);">数据与任务的适合性指的是数据是否适合用于预定的模型训练和预测任务，确保数据与模型目标一致。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">相关性分析</font>**<font style="color:rgb(51, 51, 51);">：评估数据中特征与目标变量的相关性。</font>
+ **<font style="color:rgb(51, 51, 51);">领域适应性</font>**<font style="color:rgb(51, 51, 51);">：确保数据分布与目标任务的领域一致。</font>
+ **<font style="color:rgb(51, 51, 51);">任务可行性</font>**<font style="color:rgb(51, 51, 51);">：评估数据是否能够支持模型完成预定任务。</font>

```python
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def assess_data_task_alignment(dataset, target_column, feature_columns):
    # 绘制目标变量与其他特征的相关性热图
    sns.heatmap(dataset[feature_columns + [target_column]].corr(), 
                cmap='coolwarm', annot=True)
    plt.title('Correlation Heatmap between Features and Target')
    plt.show()
    
    # 使用随机森林计算特征与目标的互信息
    if target_column is not None:
        print("\nMutual Information between Features and Target:")
        mutual_info = mutual_info_classif(dataset[feature_columns], dataset[target_column])
        for feat, mi in zip(feature_columns, mutual_info):
            print(f"{feat}: {mi:.3f}")
    
    # 示例：训练简单模型评估数据适合性
    if target_column is not None:
        X_train, X_test, y_train, y_test = train_test_split(
            dataset[feature_columns], dataset[target_column], test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred):.3f}")
```

# RAG评估<font style="color:#D22D8D;"> </font>
## 评估指标
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

# Agent评估<font style="color:#D22D8D;"> </font>
:::info
<font style="color:rgb(25, 27, 31);">现如今Agent开发工具/框架不断出现，但如何全面地对Agent进行评估却很困难，本文就从介绍一些主流的Agent/LLM-as-Agent评估工作来看看是否能得到一些启发。</font>

:::

## GAIA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">《</font>[GAIA: A Benchmark for General AI Assistants](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2311.12983)<font style="color:rgb(25, 27, 31);">》是一个面向</font>**<font style="color:rgb(25, 27, 31);">通用AI助手</font>**<font style="color:rgb(25, 27, 31);">能力的基准评测体系，由 Meta AI（FAIR）、Hugging Face 等研究团队于 2023 年提出。</font>

<font style="color:rgb(25, 27, 31);">paper:</font>[https://arxiv.org/pdf/2311.12983](https://arxiv.org/pdf/2311.12983)

<font style="color:rgb(51, 51, 51);">项目地址：</font>[https://huggingface.co/spaces/gaia-benchmark/leaderboard](https://huggingface.co/spaces/gaia-benchmark/leaderboard)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741662773383-08c996cf-74ae-4d29-b31b-bc7dbc396dbd.png)

:::color5
**<font style="color:#601BDE;">1.GAIA介绍</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">组成</font>**<font style="color:rgb(25, 27, 31);">：里面有</font>**<font style="color:#74B602;">466个精心设计的问题，其中分为三个级别，Lv.1、Lv.2、Lv.3，难度依次递增，</font>**<font style="color:rgb(25, 27, 31);">同时保留了其中300个问题的答案，以此来支持一个即将开放的排行榜。这466个问题是基于文本的，部分还会附带一个文件（如图像或电子表格）。它们涵盖了各种助理用例，如日常个人任务、科学或常识。这些问题旨在承认一个简短的、单一的正确答案，因此很容易验证。</font>
    - <font style="color:rgb(25, 27, 31);">Level 1 ：通常不需要工具，或者</font>**<font style="color:#74B602;">最多只需要一个工具，但不超过5个步骤</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - <font style="color:rgb(25, 27, 31);">Level 2：通常涉及更多步骤，</font>**<font style="color:#74B602;">大约在5到10之间</font>**<font style="color:rgb(25, 27, 31);">，需要结合不同的工具。</font>
    - <font style="color:rgb(25, 27, 31);">Level 3 ：是一个近乎完美的总助理的问题，要求采取任意长的行动序列，使用任意数量的工具，并进入整个世界。</font>
+ **<font style="color:rgb(25, 27, 31);">和传统榜单区别</font>**<font style="color:rgb(25, 27, 31);">：传统的测试一般都是数学（AIME）或者一些专业知识问答、编程等等，但是GAIA测试，里面很多都是概念简单，但是需要多步骤解决的实际问题。</font>
+ **<font style="color:rgb(25, 27, 31);">如何评估</font>**<font style="color:rgb(25, 27, 31);">：使用GAIA，只需向</font>[<font style="color:rgb(9, 64, 142);">人工智能助理</font>](https://zhida.zhihu.com/search?content_id=236942153&content_type=Article&match_order=1&q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%8A%A9%E7%90%86&zhida_source=entity)<font style="color:rgb(25, 27, 31);">给出</font>**<font style="color:#74B602;">zero-shot promp</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">想通过GAIA的测试，一般需要</font>**<font style="color:#74B602;">网络检索能力、工具调用能力、编程能力、文件处理能力</font>**<font style="color:rgb(25, 27, 31);">等等。在23年的时候，人类一般能达到90%的成功率，而那时候的最强AI GPT4，在第一级才勉强达到15%。</font>

:::color5
**<font style="color:#601BDE;">2.评估指标</font>**

:::

+ **Score：**回答问题正确率
+ **Time to Anwser：**回答花费时间

:::color5
**<font style="color:#601BDE;">3.问题样例</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741662995251-df17f04b-11d5-46de-bc4b-38679f233432.png)

```python
Level 1 
Q:NIH网站上列出的2018年1月至5月的患者，幽门螺杆菌治疗寻常痤疮临床试验的实际入组人数是多少？
GT:90

Level 2
Q:如果这整品脱都是冰淇淋，那么相比美国联邦乳脂含量标准，相差多少百分比？使用维基百科2020年报告的标准。答案为+或-一个四舍五入的数字，精确到小数点后一位。
GT：+4.6

Level 2
Q:在美国国家航空航天局2006年1月21日的天文图片中，可以看到两名宇航员，其中一个看起来比另一个小得多。截至2023年8月，在美国国家航空航天局宇航员小组认为，较小的宇航员是其中的一员，哪一位花费的时间最少在太空中，他在太空中度过了多少分钟，四舍五入到最接近的分钟？排除任何没有在太空呆过一段时间的宇航员。给出宇航员的姓氏，与用分号表示分钟数。在分钟数中使用逗号作为千位分隔符。
GT：White;5876
```

:::color5
**<font style="color:#601BDE;">4.GAIA自动化评估流程</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741663491854-055ce911-b1aa-4f07-b212-bb5540bb59b0.png)

```python
你是一名通用的人工智能助理。我会问你一个问题。报告你的想法，以及
用以下模板完成你的答案：最终答案：[你的最终答案]。
你的最终答案应该是一个数字或尽可能少的单词，或者是一个逗号分隔的数字和/或字符串列表。如果你被要求输入一个数字，除非另有说明，否则不要使用逗号来写你的数字，也不要使用$或百分号等单位。
如果你被要求输入一个字符串，不要使用冠词，也不要使用缩写（例如城市），并写下
除非另有说明，否则纯文本中的数字。如果您被要求使用逗号分隔的列表，请根据要放入列表中的元素是数字还是字符串来应用上述规则。
```

```python
所附的Excel文件包含当地快餐连锁店菜单项的销售情况。这家连锁店的食品（不包括饮料）总销售额是多少？用小数点后两位的美元表示你的答案。
```

```python
#文件读取
import pandas as pd
# Load the Excel file
file_path = '/mnt/data/uploaded.xlsx'
df = pd.read_excel(file_path)

# 计算所有的销售tem
total_food_sales = df[
['Burgers', 'Hot Dogs', 'Salads', 'Fries', 'Ice Cream']
].sum().sum()
# 输出格式是USD Dollar，两位小数
total_food_sales_formatted = f"$–total_food_sales:,.2f˝"
```

```python
Final Answer:$89706.00 
GT:89706.00 
```

:::color5
**<font style="color:#601BDE;">5.评估结果</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741663859023-a3ebcbe4-276c-4a23-95eb-a6c836dfbb8a.png)

## <font style="color:rgb(25, 27, 31);">AgentBench</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">AgentBench</font>**<font style="color:rgb(25, 27, 31);">是第一个旨在评估LLM-as-Agent在各种不同环境中的表现的基准测试。它涵盖8个不同的环境（其中5个是首创，另外3个是根据已发布的数据集进行重新编译得到），以更全面地评估LLM在各种场景中作为自主代理运行的能力。</font>

**<font style="color:rgb(25, 27, 31);">论文地址</font>**<font style="color:rgb(25, 27, 31);">：</font>`<font style="color:rgb(25, 27, 31);">https://arxiv.org/abs/2308.03688</font>`

**<font style="color:rgb(25, 27, 31);">Github：</font>**[**https://github.com/THUDM/AgentBench**](https://github.com/THUDM/AgentBench)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741661929826-5dbd32b7-b976-45bb-8e82-b5f7075de360.png)

:::color5
**<font style="color:#601BDE;">1.评估维度</font>**

:::

+ <font style="color:rgb(25, 27, 31);">操作系统（OS）：考察 LLM 在 bash 环境进行文件操作、用户管理等能力。</font>
+ <font style="color:rgb(25, 27, 31);">数据库（DB）：考察 LLM 利用 SQL 对给定数据库进行操作的能力。</font>
+ <font style="color:rgb(25, 27, 31);">知识图谱（KG）：考察 LLM 利用工具从知识图谱中获取复杂知识的能力。</font>
+ <font style="color:rgb(25, 27, 31);">卡牌对战（DCG）：考察 LLM 作为玩家，根据规则和状态进行卡牌对战的策略决策能力。</font>
+ <font style="color:rgb(25, 27, 31);">情景猜谜（LTP）：这个游戏需要 LLM 针对谜题进行提问，从而猜出答案，能够考察 LLM 的横向思维能力。</font>
+ <font style="color:rgb(25, 27, 31);">家居（HH）：在模拟的家庭环境下，LLM 需要完成一些日常任务，主要考察 LLM 将复杂的高级目标拆解为一系列简单行动的能力。</font>
+ <font style="color:rgb(25, 27, 31);">网络购物（WS）：在模拟的在线购物环境中，LLM 需要按照需求完成购物，主要考察 LLM 的自主推理和决策能力。</font>
+ <font style="color:rgb(25, 27, 31);">网页浏览（WB）：在模拟网页环境中，LLM需要根据指令完成跨网站的复杂任务，考察 LLM 作为 Web agent的能力。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

<font style="color:rgb(25, 27, 31);">AgentBench相当于是一个通用的LLM评估框架，来评估LLM作为通用Agent在</font>**<font style="color:rgb(25, 27, 31);">理解人类意图并执行指令、编码能力、知识获取和推理、策略决策、多轮一致性、逻辑推理、自主探索以及可解释的推理</font>**<font style="color:rgb(25, 27, 31);">这8个方面上的能力。</font>

<font style="color:rgb(25, 27, 31);">从评测结果可以看出，商业模型还是领先于开源模型，LLM的能力“涌现”还是很明显的。不少开源模型“偏科”现象也十分严重，代码训练确实能增强编程相关环境的表现，但可能以牺牲其他能力为代价。因此模型的训练方式需要针对不同的目标任务进行不同优化。</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741662085934-52199f36-bee1-4a6f-9581-23d6fbc22b97.png)



## Langchain评估  （工具调用评估）
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">工具调用评估为主，LangChain（</font>[_https://blog.langchain.dev/benchmarking-agent-tool-use/_](https://link.zhihu.com/?target=https%3A//blog.langchain.dev/benchmarking-agent-tool-use/)<font style="color:rgb(25, 27, 31);"> ）也集成了几个基准（单工具调用、多工具调用、关系数据查询和多元数学问题）来测试LLM在规划、任务分解、函数调用和克服预训练偏差等方面的能力。</font>

**项目地址**：[https://blog.langchain.dev/benchmarking-agent-tool-use/](https://blog.langchain.dev/benchmarking-agent-tool-use/)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741662394168-6f10a347-3330-414e-8d49-274c88c4af36.png)

:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

1. **正确性（与GT相比）**-这使用LLM作为判断标准。由于所有这些问题的答案都很简洁，而且相当二元，我们发现这些判断与我们自己的决定相对应。
2. **正确的最终状态（环境）**-对于打字机任务，每次工具调用都会更新世界状态。我们在每个测试行的末尾直接检查环境的等效性。
3. **中间步骤正确性**-每个数据点都有一个最佳的函数调用序列来获得正确的答案。我们直接根据地面真值检查函数调用的顺序。
4. **所采取的步骤与预期步骤的比率**——尽管选择了一组次优的工具，但代理最终可能会返回正确的答案。该指标将反映差异，而不会像精确匹配中间步骤那样严格。正确性。

:::color5
**<font style="color:#601BDE;">2.工具评估</font>**

:::

在4个工具使用任务中，使用7个模型重现这些实验：

1. 打字机（单工具）：按顺序调用一个工具来键入一个单词。
2. 打字机（26个工具）：按顺序调用不同的工具来打字。
3. 关系数据：根据三个表中的信息回答问题。
4. 多元数学：使用工具回答数学问题，其中基础数学规则略有变化。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741662433278-41799853-498b-4668-83dc-18ebdbaff2f0.png)

:::color5
**<font style="color:#601BDE;">3.轨迹评估</font>**

:::

<font style="color:rgb(25, 27, 31);">应该从哪些方面评估Agent？怎样评估特定领域/用途的Agent？这两个问题目前还仍然没有得到很好的解决，但LangChain从</font>**<font style="color:rgb(25, 27, 31);">Trajectory（轨迹）</font>**<font style="color:rgb(25, 27, 31);">这个方向为这两个问题指出了一条路。</font>

<font style="color:rgb(25, 27, 31);">轨迹也就是Agent采取的一系列动作及其相应的响应，</font>**<font style="color:#74B602;">LangChain中的</font>**[**<font style="color:#74B602;">Trajectory Evaluators</font>**](https://zhida.zhihu.com/search?content_id=246478763&content_type=Article&match_order=1&q=Trajectory+Evaluators&zhida_source=entity)**<font style="color:#74B602;">（轨迹评估器）提供了一种更全面的方法来评估Agent的效率和能力</font>**<font style="color:rgb(25, 27, 31);">。简单来说，轨迹评估器获取了输入用户/Agent的输入、Agent的最终输出和中间步骤，然后传递给语言模型(默认为GPT-4)来对Agent输出的必要性、工具使用的合理性等进行评分和解释。</font>

# Prompt评估<font style="color:#D22D8D;"> </font>
:::color3
**<font style="color:#ED740C;">简介</font>**：评估Prompt的好坏需要一个全面和多维度的方法，结合自动评估指标、人工评估和用户反馈等多种手段。选择合适的评估方法和技术，能够有效提升Prompt的质量和生成效果，进而提高模型的整体性能和应用体验。通过不断优化和改进Prompt设计，可以实现更自然、更准确、更有效的自然语言。

:::

## 评估指标
:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

**<font style="color:rgb(51, 51, 51);">1.1 相关性（Relevance）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成内容是否与用户意图和任务需求紧密相关。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>[评估](https://www.yuque.com/zhongxian-iiot9/gi3w2u/nlapi8xm5fmsnx3g)
    - **<font style="color:rgb(51, 51, 51);">ROUGE-N</font>**<font style="color:rgb(51, 51, 51);">（N-gram重叠率）：衡量生成文本与参考文本的词汇匹配度。</font>
    - **<font style="color:rgb(51, 51, 51);">BLEU</font>**<font style="color:rgb(51, 51, 51);">（双语评估研究指标）：常用于翻译任务，但也可用于评估生成文本与参考文本的相似性。</font>
    - **<font style="color:rgb(51, 51, 51);">BERTScore</font>**<font style="color:rgb(51, 51, 51);">：基于BERT的语义相似度计算，捕捉语义相关性而非字面匹配。</font>
    - **<font style="color:rgb(51, 51, 51);">人工评分</font>**<font style="color:rgb(51, 51, 51);">：通过人工判断生成内容是否符合主题（如1-5分评分）。</font>

**<font style="color:rgb(51, 51, 51);">1.2 准确性（Accuracy）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成信息的正确性和事实一致性。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Factual Accuracy</font>**<font style="color:rgb(51, 51, 51);">：通过外部知识库（如维基百科）验证生成内容的正确性。</font>
    - **<font style="color:rgb(51, 51, 51);">错误检测率</font>**<font style="color:rgb(51, 51, 51);">（Error Detection Rate）：统计生成内容中的明显事实错误或逻辑矛盾。</font>
    - **<font style="color:rgb(51, 51, 51);">专家评审</font>**<font style="color:rgb(51, 51, 51);">：由领域专家对技术性内容的准确性进行评分。</font>

**<font style="color:rgb(51, 51, 51);">1.3 多样性（Diversity）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成内容的丰富程度，避免重复或模板化。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Distinct-N</font>**<font style="color:rgb(51, 51, 51);">：统计生成文本中不同n-gram的比例（如Distinct-1/2/3）。</font>
    - **<font style="color:rgb(51, 51, 51);">熵（Entropy）</font>**<font style="color:rgb(51, 51, 51);">：词汇分布的熵值越高，多样性越好。</font>
    - **<font style="color:rgb(51, 51, 51);">重复率（Repetition Rate）</font>**<font style="color:rgb(51, 51, 51);">：重复短语或句子的比例。</font>

**<font style="color:rgb(51, 51, 51);">1.4 效率（Efficiency）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：模型生成结果所需的计算资源和时间消耗。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">响应时间</font>**<font style="color:rgb(51, 51, 51);">（Latency）：从输入prompt到生成完整输出的耗时。</font>
    - **<font style="color:rgb(51, 51, 51);">Token数量</font>**<font style="color:rgb(51, 51, 51);">：生成内容的长度是否合理（过短可能信息不足，过长可能冗余）。</font>

**<font style="color:rgb(51, 51, 51);">1.5 鲁棒性（Robustness）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：对prompt微小变化的敏感度，能否稳定生成高质量结果。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">扰动测试</font>**<font style="color:rgb(51, 51, 51);">：对prompt进行同义词替换、语序调整等扰动后，统计输出一致性的变化。</font>
    - **<font style="color:rgb(51, 51, 51);">对抗性测试</font>**<font style="color:rgb(51, 51, 51);">：故意输入模糊或矛盾的prompt，观察模型能否合理应对。</font>

**<font style="color:rgb(51, 51, 51);">1.6 一致性（Consistency）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：在多轮对话或复杂任务中保持逻辑连贯，避免前后矛盾。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">自洽性检查</font>**<font style="color:rgb(51, 51, 51);">（Self-Consistency）：多次运行相同prompt，对比输出的核心观点是否一致。</font>
    - **<font style="color:rgb(51, 51, 51);">逻辑链验证</font>**<font style="color:rgb(51, 51, 51);">：对推理类任务（如数学问题）验证生成步骤的逻辑正确性。</font>

**<font style="color:rgb(51, 51, 51);">1.7 用户体验（User Experience）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成结果是否符合用户个性化需求，包括语气、风格等。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">用户满意度调查</font>**<font style="color:rgb(51, 51, 51);">：通过问卷或评分收集用户主观反馈。</font>
    - **<font style="color:rgb(51, 51, 51);">任务完成率</font>**<font style="color:rgb(51, 51, 51);">（Task Success Rate）：例如在客服场景中是否成功解决用户问题。</font>

## 评估方法
### 人工评估
:::color5
**<font style="color:#601BDE;">1.人工评估</font>**

:::

**定义**：人工评估是通过人工方式对模型输出的Prompt效果进行评估，是最为直接和主观的评估方法。

+ **优点**：能够捕捉到复杂的语言理解和生成能力，评估结果更为全面和准确。
+ **缺点**：耗时且成本高，结果可能受到评估者的主观影响。
+ **实施步骤**：
    1. **选择评估人员**：确保评估人员具备相关的专业知识和技能。
    2. **设计评估标准**：明确评估的维度，如准确性、相关性、流畅性等。
    3. **收集输出样本**：从模型中获取一定数量的Prompt输出。
    4. **评估与打分**：根据标准对每个Prompt进行评分。
    5. **分析结果**：汇总评分数据，找出问题和改进方向。

### 基于LLM评估
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>利用LLM和指标对Prompt进行评估，是一种高效且客观的评估方式。

:::

:::color5
**<font style="color:#601BDE;">1.目标</font>**

:::

**<font style="color:rgb(51, 51, 51);">任务目标</font>**<font style="color:rgb(51, 51, 51);">：使用Qwen模型为电商商品生成吸引人的卖点文案。  
</font>**<font style="color:rgb(51, 51, 51);">示例商品</font>**<font style="color:rgb(51, 51, 51);">：无线蓝牙耳机  
</font>**<font style="color:rgb(51, 51, 51);">初始Prompt</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
你是一个电商文案专家，请为[无线蓝牙耳机]生成5条卖点，要求突出产品优势，语言简洁有力。
```

:::color5
**<font style="color:#601BDE;">2.评估流程</font>**

:::

<font style="color:rgb(51, 51, 51);">1. 评估目标</font>

+ **<font style="color:rgb(51, 51, 51);">核心指标</font>**<font style="color:rgb(51, 51, 51);">：相关性、吸引力、多样性、准确性、品牌调性。</font>
+ **<font style="color:rgb(51, 51, 51);">评估方式</font>**<font style="color:rgb(51, 51, 51);">：LLM自动评分 + 人工校验。</font>

<font style="color:rgb(51, 51, 51);">2. 整体流程</font>

```plain
生成候选文案 → LLM自动评分 → 人工抽检 → 统计指标 → 优化Prompt → 重复迭代
```

:::color5
**<font style="color:#601BDE;">3.评估方法1：</font>****<font style="color:#601BDE;">LLM作为评分器（自动评估）</font>**

:::

**<font style="color:rgb(51, 51, 51);">步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">生成候选文案</font>**<font style="color:rgb(51, 51, 51);">：用待评估的prompt生成N条卖点（如N=20）。</font>
2. **<font style="color:rgb(51, 51, 51);">设计评分指令</font>**<font style="color:rgb(51, 51, 51);">：要求LLM（Qwen/GPT-4）从多维度打分。</font>
3. **<font style="color:rgb(51, 51, 51);">解析评分结果</font>**<font style="color:rgb(51, 51, 51);">：提取分数并统计平均分、方差等。</font>

<font style="color:rgb(51, 51, 51);">评分Prompt示例：</font>

```python
score_prompt = """
你是一个专业的电商文案评估AI，请根据以下标准为每条卖点打分（1-5分）：
1. **相关性**：是否准确描述产品真实功能（如续航、音质）。
2. **吸引力**：是否具有感染力，能激发购买欲望。
3. **多样性**：是否与其他卖点角度重复（技术/场景/人群）。

请严格按此JSON格式输出结果，仅返回JSON：
{
  "卖点1": {"相关性": 分数, "吸引力": 分数, "多样性": 分数},
  "卖点2": { ... }
}

待评估卖点：
{卖点列表}
"""
```

<font style="color:rgb(51, 51, 51);">代码实现（Python+Qwen）：</font>

```python
import json
from qwen_agent import QwenAgent

def evaluate_with_llm(prompts):
    agent = QwenAgent(api_key='your_api_key')
    response = agent.generate(
        prompt=score_prompt.format(卖点列表=prompts),
        temperature=0.1  # 降低随机性
    )
    try:
        scores = json.loads(response)
        return scores
    except:
        return {}  # 异常处理

# 示例输出
scores = {
    "超长续航50小时，告别频繁充电": {"相关性": 5, "吸引力": 4, "多样性": 2},
    "蓝牙5.3稳定连接，游戏无延迟": {"相关性": 5, "吸引力": 3, "多样性": 3}
}
```

:::color5
**<font style="color:#601BDE;">4.评估方法2：</font>****<font style="color:#601BDE;">LLM作为对比器（AB测试）</font>**

:::

**<font style="color:rgb(51, 51, 51);">用途</font>**<font style="color:rgb(51, 51, 51);">：比较不同prompt生成的文案质量。  
</font>**<font style="color:rgb(51, 51, 51);">Prompt设计</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
请判断以下两组卖点文案哪组更优，并给出理由：
- 组A（Prompt1生成）：{卖点列表A}
- 组B（Prompt2生成）：{卖点列表B}

评估标准：
1. 整体吸引力 2. 信息准确性 3. 角度多样性

输出格式：
{
  "winner": "A/B",
  "reason": "具体原因..."
}
```

:::color5
**<font style="color:#601BDE;">5.评估方法3：</font>****<font style="color:#601BDE;">LLM生成改写建议</font>**

:::

**<font style="color:rgb(51, 51, 51);">用途</font>**<font style="color:rgb(51, 51, 51);">：自动诊断prompt问题并给出优化方向。  
</font>**<font style="color:rgb(51, 51, 51);">Prompt设计</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
以下是一组针对无线蓝牙耳机的卖点文案：
{卖点列表}

请分析这些文案的不足，并从以下维度提出prompt改进建议：
1. 指令明确性 2. 示例补充 3. 约束条件

输出格式：
{
  "不足": ["问题1", "问题2"],
  "建议": ["建议1", "建议2"]
}
```

:::color5
**<font style="color:#601BDE;">6.评估指标计算</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 自动指标</font>**

```python
def calculate_metrics(scores):
    relevance = np.mean([v["相关性"] for v in scores.values()])
    attractiveness = np.mean([v["吸引力"] for v in scores.values()])
    diversity = np.mean([v["多样性"] for v in scores.values()])
    return {
        "相关性": round(relevance, 2),
        "吸引力": round(attractiveness, 2),
        "多样性": round(diversity, 2)
    }

# 示例结果：{"相关性": 4.8, "吸引力": 3.5, "多样性": 2.9}

```

**<font style="color:rgb(51, 51, 51);">2. 人工校验指标</font>**

+ **<font style="color:rgb(51, 51, 51);">准确性校验</font>**<font style="color:rgb(51, 51, 51);">：抽取10%的文案核对产品参数（如实际续航是否为20小时）。</font>
+ **<font style="color:rgb(51, 51, 51);">品牌调性匹配</font>**<font style="color:rgb(51, 51, 51);">：由运营人员标注是否符合品牌风格（是/否）。</font>

:::color5
**<font style="color:#601BDE;">7.案例</font>**

:::

<font style="color:rgb(51, 51, 51);">初始Prompt的问题诊断</font>

+ **<font style="color:rgb(51, 51, 51);">LLM生成的改进建议</font>**<font style="color:rgb(51, 51, 51);">：</font>

```json
{
  "不足": ["缺乏生成角度指导", "未限制抽象词汇"],
  "建议": ["添加技术/场景/人群的多角度要求", "禁止使用‘高性能’等模糊表述"]
}
```

<font style="color:rgb(51, 51, 51);">优化后的Prompt</font>

```plain
你是一名资深电商文案专家，请为[无线蓝牙耳机]生成5条卖点：
1. 必须覆盖以下角度：
   - 技术参数（如蓝牙版本、续航）
   - 使用场景（如通勤、运动）
   - 人群痛点（如戴久不痛）
2. 语言风格：年轻化，可使用感叹句/网络用语
3. 禁止使用以下词汇：高性能、高品质、卓越

参考示例：
1. “开盖即连！地铁追剧再不怕错过站~”
2. “狂甩不掉！健身房的隐形BGM神器”
```

<font style="color:rgb(51, 51, 51);">优化前后对比</font>

| **指标** | **优化前** | **优化后** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">平均相关性</font> | <font style="color:rgb(51, 51, 51);">4.2</font> | <font style="color:rgb(51, 51, 51);">4.8</font> |
| <font style="color:rgb(51, 51, 51);">平均吸引力</font> | <font style="color:rgb(51, 51, 51);">3.1</font> | <font style="color:rgb(51, 51, 51);">4.3</font> |
| <font style="color:rgb(51, 51, 51);">多样性</font> | <font style="color:rgb(51, 51, 51);">2.4</font> | <font style="color:rgb(51, 51, 51);">4.1</font> |
| <font style="color:rgb(51, 51, 51);">品牌调性符合率</font> | <font style="color:rgb(51, 51, 51);">60%</font> | <font style="color:rgb(51, 51, 51);">90%</font> |


:::color5
**<font style="color:#601BDE;">8.常见问题与解法</font>**

:::

1. **LLM评分偏差**
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：LLM可能高估技术术语的吸引力。</font>
    - **<font style="color:rgb(51, 51, 51);">解法</font>**<font style="color:rgb(51, 51, 51);">：在评分prompt中加入人工标注的示例（Few-shot Learning）。</font>
2. **多样性计算不准**
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：仅依赖LLM主观评分可能不准。</font>
    - **<font style="color:rgb(51, 51, 51);">解法</font>**<font style="color:rgb(51, 51, 51);">：结合CLIP计算文案-场景匹配度，或使用Sentence-BERT计算语义相似度。</font>
3. **评估成本高**
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：评估大量文案时API成本上升。</font>
    - **<font style="color:rgb(51, 51, 51);">解法</font>**<font style="color:rgb(51, 51, 51);">：先用小模型（如Qwen-1.8B）初筛，再用大模型精评。</font>



# BenchMark
## （1）一般评估
<font style="color:rgb(25, 27, 31);">在</font>**<font style="color:rgb(25, 27, 31);">MMLU、MMLU-PRO、CMMLU、BBH、GSM8K、MATH、DROP、MBPP和HumanEval</font>**<font style="color:rgb(25, 27, 31);">等基准测试中，NSA在大多数指标上优于全注意力基线，尽管其稀疏性较高。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740105245564-cd556aa8-4a6b-479d-9ef3-3f8e880f8b7b.png)

## （2）长上下文评估
<font style="color:rgb(25, 27, 31);">在64k上下文的“针尖在干草堆中”测试中，NSA在所有位置上都达到了完美的检索准确率。在LongBench基准测试中，NSA的平均得分为0.469，优于所有基线，包括全注意力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740105353438-7a719480-622f-46c4-a39f-ca57571a10e1.png)

## <font style="color:rgb(25, 27, 31);">（3）COT评估</font>
<font style="color:rgb(25, 27, 31);">在AIME指令推理评估中，经过有监督微调后的NSA-R在8k和16k上下文长度下的表现均优于全注意力基线-R。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740105375656-7bfc70cc-50b4-493d-ac04-9e0ae9ea1d08.png)





# 评估指标汇总
:::color3
**<font style="color:#ED740C;">简介</font>**：评估文本数据的好坏需要一个全面和多维度的方法，结合自动评估指标、人工评估和用户反馈等多种手段。选择合适的评估方法和技术，能够有效提升文本数据的质量和生成效果，进而提高模型的整体性能和应用体验。通过不断优化和改进文本数据设计，可以实现更自然、更准确、更有效的自然语言。

**参考：**[推荐系统评价指标](https://www.yuque.com/zhongxian-iiot9/gi3w2u/onhy92qlaqb366r1#iSEP0)

:::

:::color5
**<font style="color:#601BDE;">1.人工评估</font>**

:::

**定义**：人工评估是通过人工方式对模型输出的文本数据效果进行评估，是最为直接和主观的评估方法。

+ **优点**：能够捕捉到复杂的语言理解和生成能力，评估结果更为全面和准确。
+ **缺点**：耗时且成本高，结果可能受到评估者的主观影响。
+ **实施步骤**：
    1. **选择评估人员**：确保评估人员具备相关的专业知识和技能。
    2. **设计评估标准**：明确评估的维度，如准确性、相关性、流畅性等。
    3. **收集输出样本**：从模型中获取一定数量的文本数据输出。
    4. **评估与打分**：根据标准对每个文本数据进行评分。
    5. **分析结果**：汇总评分数据，找出问题和改进方向。

:::color5
**<font style="color:#601BDE;">2.自动化评估</font>**

:::

**定义**：利用自动化工具和指标对文本数据进行评估，是一种高效且客观的评估方式。

+ **优点**：快速、高效，适合大规模评估。
+ **缺点**：可能无法捕捉到文本数据的复杂语义和细微差别。



    - <font style="color:rgb(51, 51, 51);"></font>

## 困惑度<font style="color:rgb(51, 51, 51);">PPL（Perplexity）</font>
:::color3
<font style="color:rgb(51, 51, 51);">PPL（Perplexity）指的是困惑度，这是一个用于评估语言模型性能的重要指标。困惑度反映了</font>**<font style="color:#DF2A3F;">语言模型对给定测试数据的预测难度</font>**<font style="color:rgb(51, 51, 51);">。具体来说，困惑度的计算基于模型对测试集中每个词的预测概率，通过对数似然的平均值来衡量模型的表现。</font>

+ **<font style="color:#ED740C;">PPL用来评价语言模型好坏的指标。PPL越低，说明模型对数据的预测能力越强。</font>**

:::

**<font style="color:rgb(51, 51, 51);">困惑度的计算公式如下：</font>**

:::info
**简洁版**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739777959166-a2669332-12fc-4600-9f3c-ca68fb52dd8e.png)

:::

:::info
**展开版**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741762256375-6a91d831-f218-45e5-aa85-60fcf776c64c.png)

  
<font style="color:rgb(25, 27, 31);">P(W</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">,W</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">...W</font><sub><font style="color:rgb(25, 27, 31);">N</font></sub><font style="color:rgb(25, 27, 31);">)就是模型生成这个句子的概率</font>

:::

<font style="color:rgb(25, 27, 31);">通俗来说，困惑度可以理解为</font>**<font style="color:#74B602;">模型生成某个语料的概率是多少</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(51, 51, 51);">直观理解：</font>**<font style="color:rgb(51, 51, 51);">困惑度可以理解为模型预测下一个词时的平均“分支数”。例如，PPL=50表示模型平均在每个位置面临50种等概率的选择。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

+ <font style="color:rgb(51, 51, 51);">对测试集中每个词，计算其在模型中的预测概率。</font>
+ <font style="color:rgb(51, 51, 51);">对所有词的预测概率取对数，然后计算这些对数的平均值。</font>
+ <font style="color:rgb(51, 51, 51);">取平均值的负指数，得到困惑度数值。</font>
    - **<font style="color:rgb(25, 27, 31);">为什么要施加（-1/N）次幂</font>**<font style="color:rgb(25, 27, 31);">：是因为要考虑语料长度的影响。如果一个句子越长，这个句子出现的概率可能会越低（比如“你好”和“你是我心中最美的云彩”这两句话，前者出现的概率很高）。</font>**<font style="color:#ED740C;">（-1/N）次幂相当于一个“惩罚因子”</font>**<font style="color:rgb(25, 27, 31);">。对于一个位于(0,1)范围的数，施加了（-1/N）次幂后，N越大，施加之后的值越小。</font>

**计算示例**

1. 现在我们有两个语言模型A和B，词表只有这7个token：

```python
tokens_map = {
    '爱': 0,
    '你': 1,
    '就': 2,
    '像': 3,
    '生': 4,
    '命': 5,
    '。': 6,
}
```

2. <font style="color:rgb(25, 27, 31);">一般情况下，使用</font>[<font style="color:rgb(9, 64, 142);">GPT类模型</font>](https://zhida.zhihu.com/search?content_id=232887257&content_type=Article&match_order=1&q=GPT%E7%B1%BB%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">生成上面这句话的时候，我们会拿到形状为 </font>_<font style="color:rgb(25, 27, 31);">[句子长度, 词表长度] </font>_<font style="color:rgb(25, 27, 31);">的概率矩阵，假设分别为：</font>

```python
# modelA
probs_modelA = [
    [0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.04], 
    [0.05, 0.30, 0.05, 0.40, 0.05, 0.10, 0.05], 
    [0.30, 0.05, 0.30, 0.20, 0.05, 0.05, 0.05], 
    [0.20, 0.10, 0.05, 0.50, 0.05, 0.05, 0.05], 
    [0.30, 0.30, 0.05, 0.05, 0.10, 0.15, 0.05], 
    [0.05, 0.05, 0.05, 0.15, 0.35, 0.30, 0.05], 
    [0.05, 0.05, 0.05, 0.15, 0.05, 0.60, 0.05]，
    [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.70]
]
对模型A，我们得到概率序列 [0.16, 0.30, 0.30, 0.50, 0.30, 0.35, 0.60, 0.70] 

# modelB
probs_modelB = [
    [0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.04], 
    [0.05, 0.50, 0.05, 0.20, 0.05, 0.10, 0.05], 
    [0.30, 0.05, 0.40, 0.10, 0.05, 0.05, 0.05], 
    [0.10, 0.10, 0.05, 0.60, 0.05, 0.05, 0.05], 
    [0.40, 0.30, 0.05, 0.05, 0.10, 0.05, 0.05], 
    [0.05, 0.05, 0.05, 0.15, 0.40, 0.25, 0.05], 
    [0.05, 0.05, 0.05, 0.15, 0.05, 0.60, 0.05]，
    [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.70]
]
对模型B，我们得到概率序列 [0.16, 0.50, 0.40, 0.60, 0.40, 0.40, 0.60, 0.70]
```

3. <font style="color:rgb(25, 27, 31);">现在来计算两个模型生成这句话的概率，由于都是 [0, 1] 之间的数字，防止溢出，我们在概率连乘后取2的 log ：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741764190553-f12f7d4d-94ba-4cb2-adc8-98bbe40d64ef.png)

**<font style="color:rgb(25, 27, 31);">可以看到 log</font>**<sub>**<font style="color:rgb(25, 27, 31);">2</font>**</sub>**<font style="color:rgb(25, 27, 31);">PA<log</font>**<sub>**<font style="color:rgb(25, 27, 31);">2</font>**</sub>**<font style="color:rgb(25, 27, 31);">PB ，这说明模型B生成这句话的概率更高。</font>**

<font style="color:rgb(25, 27, 31);">这个结果我们可以理解为模型B可能是一个作家，相对更容易写出这样的句子，模型A是一个小学生，很难写出这样的句子。所以在这个测试集下B比A好。</font>

4. <font style="color:rgb(25, 27, 31);">两个模型的困惑度分别为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741764425447-1afe4190-226f-4e35-887a-51e112eb1c19.png)

<font style="color:rgb(25, 27, 31);">计算结果和之前保持一致，B模型的困惑度小于A模型。</font>**<font style="color:#ED740C;">句子的概率越高，模型越好，困惑度也就越小。</font>**



:::color5
**<font style="color:#601BDE;">2.迷惑度的意义与应用</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">模型评估</font>**<font style="color:rgb(51, 51, 51);">：困惑度用于衡量模型对数据的拟合程度。困惑度越低，表示模型的预测能力越强，拟合效果越好。</font>
2. **<font style="color:rgb(51, 51, 51);">训练监控</font>**<font style="color:rgb(51, 51, 51);">：在模型训练过程中，通过监控训练集和验证集上的困惑度，可以判断模型是否出现过拟合或欠拟合的问题。</font>
3. **<font style="color:rgb(51, 51, 51);">比较模型性能</font>**<font style="color:rgb(51, 51, 51);">：困惑度可以用来比较不同语言模型的性能。困惑度较低的模型通常表现更优，尤其是在生成和预测任务中。</font>
4. **<font style="color:rgb(51, 51, 51);">优化方向</font>**<font style="color:rgb(51, 51, 51);">：困惑度的高低可以帮助指导模型优化的方向，如调整模型结构、增加训练数据、优化训练策略等。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ <font style="color:rgb(51, 51, 51);">提供了模型预测能力的量化指标。</font>
+ <font style="color:rgb(51, 51, 51);">计算简单，易于实现和比较。	</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">无法直接反映可读性</font>**<font style="color:rgb(51, 51, 51);">：困惑度衡量的是模型预测的难度，而不是生成文本的可读性或相关性，因此需要结合其他指标使用。</font>
+ **<font style="color:rgb(51, 51, 51);">受数据分布影响</font>**<font style="color:rgb(51, 51, 51);">：困惑度的值易受数据分布的影响，如数据稀疏性或不平衡问题，可能影响评估结果。</font>
+ **<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">：对于大规模的测试数据集，计算困惑度需要较高的计算资源和时间。</font>

:::color5
**<font style="color:#601BDE;">4.应用</font>**

:::

1. **模型选择**  
比较不同架构（RNN vs. Transformer）或超参数（层数、学习率）的模型性能。
2. **训练监控**  
观测训练过程中验证集PPL的变化，判断是否过拟合或欠拟合。
3. **文本生成质量评估**  
低PPL通常意味着生成文本更连贯，但需结合人工评估（避免过时或重复内容）。
4. **领域适应性分析**  
计算模型在不同领域文本上的PPL，判断其泛化能力。

:::color5
**<font style="color:#601BDE;">5.代码实现</font>**

:::

```python
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 加载模型和分词器
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def calculate_ppl(text, stride=512):
    # 分词并转换为ID
    encodings = tokenizer(text, return_tensors="pt")
    input_ids = encodings.input_ids.to(device)
    
    max_length = model.config.n_positions  # GPT-2的上下文长度通常为1024
    total_log_likelihood = 0.0
    total_tokens = 0

    # 滑动窗口处理长文本
    for i in range(0, input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = i + stride
        input_chunk = input_ids[:, begin_loc:end_loc]
        target_chunk = input_ids[:, begin_loc+1:end_loc+1]  # 预测下一个词

        with torch.no_grad():
            outputs = model(input_chunk, labels=target_chunk)
            loss = outputs.loss  # 交叉熵损失
            log_likelihood = -loss * (end_loc - begin_loc)  # 对数似然求和

        total_log_likelihood += log_likelihood.item()
        total_tokens += (end_loc - begin_loc)

    ppl = torch.exp(torch.tensor(-total_log_likelihood / total_tokens))
    return ppl.item()

# 测试
text = "Language models are widely used in natural language processing."
print(f"Perplexity: {calculate_ppl(text)}")

```

## BLEU (Bilingual Evaluation Understudy)
    - **定义**：用于衡量生成文本与参考文本之间的相似性，常用于机器翻译任务。
    - **计算方式**：基于n-gram的重合度，计算生成句与参考句中相同n-gram的比例。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739848971745-a64256ca-8bf9-4e0c-91c0-51db18a7d8b6.png)

    - **应用**：衡量文本数据生成的质量，特别是对参考文本的匹配程度。

```python
def compute_bleu_score(generated_tokens, reference_tokens):
    max_n = 4  # 计算1到4-gram
    n_gram_counts = [dict() for _ in range(max_n + 1)]
    reference_counts = [dict() for _ in range(max_n + 1)]
    matches = [0] * (max_n + 1)
    
    # 统计生成文本的n-gram
    for i in range(1, max_n + 1):
        for j in range(len(generated_tokens) - i + 1):
            ngram = tuple(generated_tokens[j:j+i])
            n_gram_counts[i][ngram] = n_gram_counts[i].get(ngram, 0) + 1
    
    # 统计参考文本的n-gram  
    for i in range(1, max_n + 1):
        for j in range(len(reference_tokens) - i + 1):
            ngram = tuple(reference_tokens[j:j+i])
            reference_counts[i][ngram] = reference_counts[i].get(ngram, 0) + 1
    
    # 计算匹配次数
    for i in range(1, max_n + 1):
        for ngram, count in n_gram_counts[i].items():
            if ngram in reference_counts[i]:
                matches[i] += min(count, reference_counts[i][ngram])
    
    # 计算BLEU分数
    bleu = 0
    for i in range(1, max_n + 1):
        precision = matches[i] / (len(generated_tokens) - i + 1)
        log_precision = math.log(precision)
        bleu += (1 / i) * log_precision
    
    bleu = math.exp(bleu)
    return bleu
```

## ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
    - **定义**：专注于文本摘要任务的评估指标，基于召回率计算。
    - **计算方式**：通过计算生成文本与参考文本之间的重合n-gram数量。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739848985402-0324da71-b5e4-4693-a1a2-18f5419484a2.png)

    - **应用**：评估文本数据生成的摘要或总结的质量。

```python
def compute_rouge_score(generated_tokens, reference_tokens, n=2):
    # 选择n-gram大小，默认为2-gram
    ngrams = [tuple(generated_tokens[i:i+n]) for i in range(len(generated_tokens) - n + 1)]
    ngram_set = set(ngrams)
    
    # 统计参考文本中的n-gram总数
    ref_ngrams = [tuple(reference_tokens[i:i+n]) for i in range(len(reference_tokens) - n + 1)]
    ref_count = len(ref_ngrams)
    
    # 统计生成文本与参考文本共有n-gram的数量
    common_ngrams = set()
    for ngram in ngram_set:
        if ngram in [tuple(reference_tokens[i:i+n]) for i in range(len(reference_tokens) - n + 1)]:
            common_ngrams.add(ngram)
    
   recall = len(common_ngrams) / ref_count  # 召回率
    return recall
```

## METEOR (Metric for Evaluation of Translation with Explicit ORdering)
    - **定义**：结合了精确度、召回率和语义相似性等多方面的评估指标。
    - **计算方式**：综合考虑生成文本与参考文本在词汇、语法和语义上的相似性。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739848995274-db7139d3-de1e-4beb-bc85-480706e022ca.png)

    - **应用**：适用于需要综合评估的文本生成任务。

```python
def compute_metor_score(generated_tokens, reference_tokens):
    # 模拟WordNet同义词匹配，这里简化为完全匹配
    # 实际应用中需要集成WordNet接口
    exact_matches = sum(1 for g, r in zip(generated_tokens, reference_tokens) if g == r)
    precision = exact_matches / len(generated_tokens)
    recall = exact_matches / len(reference_tokens)
    
    alpha = 0.9
    meteor = (alpha * precision + (1 - alpha) * recall) / (alpha + (1 - alpha))
    return meteor

```

## BERTScore
    - **定义**：基于BERT模型的评估指标，能够捕捉到文本的语义信息。
    - **计算方式**：基于生成文本与参考文本在BERT表示空间中的余弦相似度。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739849007538-baea5ed5-02a1-45af-8599-325f5b419308.png)

    - **应用**：适用于评估文本数据生成文本的语义相关性。

```python
import torch
from sentence_transformers import SentenceTransformer

def compute_bert_score(generated, reference, model_name='bert-base-uncased'):
    model = SentenceTransformer(model_name)
    g_embeddings = model.encode([generated])
    r_embeddings = model.encode([reference])
    cos_score = torch.nn.functional.cosine_similarity(g_embeddings, r_embeddings)
    return cos_score.item()

```

## F1-Score
    - **定义**：用于分类任务的评估指标，结合了精确度和召回率。
    - **计算方式**：F1 = 2 * (Precision * Recall) / (Precision + Recall)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739849018254-5d5f5aeb-7f43-450e-bba2-8f3bd6ee1863.png)

    - **应用**：适用于需要具体指标评估的特定任务，如问答系统中的实体识别。

```python
def compute_f1_score(generated_tokens, reference_tokens):
    exact_matches = sum(1 for g, r in zip(generated_tokens, reference_tokens) if g == r)
    precision = exact_matches / len(generated_tokens)
    recall = exact_matches / len(reference_tokens)
    
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    return f1
```

:::color5
**<font style="color:#601BDE;">3.基于LLM评估</font>**

:::

**定义**：利用其他模型对生成的文本数据进行评估，通过模型的预测结果来间接评估文本数据的质量。

+ **优点**：能够利用已有模型的知识和能力，提供更为智能和全面的评估结果。
+ **缺点**：评估结果可能受到模型本身能力和训练数据的影响。
+ **常用方法**：

a. **相似度计算**：

使用预训练语言模型（如BERT、GPT）计算生成文本数据与参考文本数据之间的语义相似度。

b. **信息量评估**：

通过计算生成文本数据的信息熵，评估其熵值和信息含量。

c. **相关性评估**：

使用模型预测生成文本数据与原始输入的相关性，评估其准确性。

```python
LLM 的输出是否与预期答案相符？如果模型表示没有足够的上下文来回答问题，则给它 0 分。否则，判断人类是否会将输出评为与预期答案相符。只要答案与括号中的预期答案 <EXPECTED ANSWER> 相符，围绕答案添加上下文是可以的。如果相符，则给它 1 分；如果不相符，则给它 0 分。
```

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">基于性能指标的评估</font>**

:::

**定义**：通过模型在特定任务中的实际性能来间接评估文本数据的质量和效果。

+ **优点**：能够直接反映文本数据对模型性能的实际影响。
+ **缺点**：可能受到模型整体能力的影响，难以单独评估文本数据的效果。
+ **实施步骤**：
    1. **选择评估任务**：确定具体的评估任务，如问答、文本摘要等。
    2. **收集生成输出**：通过模型生成文本数据的输出。
    3. **评估模型性能**：在任务上评估模型的性能，如准确率、响应时间等。
    4. **分析与改进**：根据性能数据，优化文本数据设计以提升模型表现。

:::color5
**<font style="color:#601BDE;">5.综合评估体系</font>**

:::

为了全面评估文本数据的好坏，建议结合多种评估方法，形成一个综合的评估体系。例如：

1. **自动指标评估**：如使用BLEU、ROUGE等计算生成文本的质量。
2. **人工评估**：由专家对生成文本数据进行打分，评估其准确性和相关性。
3. **用户反馈收集**：通过用户满意度调查了解实际使用效果。
4. **基于任务的性能评估**：在具体任务上评估模型性能，判断文本数据对性能提升的效果。

