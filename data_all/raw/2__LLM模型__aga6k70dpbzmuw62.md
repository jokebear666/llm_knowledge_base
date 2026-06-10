# 2️⃣ LLM模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/aga6k70dpbzmuw62 -->

# 基础
## Base/Chat/Instruct区别
:::color3
**简介**：Base、Chat和Instruction是三种不同的大模型版本，分别通过不同的训练或微调方式得到的。目前大模型训练分为三阶段：预训练（pre-train）、监督微调（SFT）、人类反馈强化学习（RLHF）。通过三阶段训练，分别得到[Base模型](https://zhida.zhihu.com/search?content_id=679864662&content_type=Answer&match_order=1&q=Base%E6%A8%A1%E5%9E%8B&zhida_source=entity)和Chat模型。

:::

:::color5
**<font style="color:#601BDE;">1. Base模型（基座模型）</font>**

:::

Base模型是通过第一阶段**<font style="color:#74B602;">预训练（pre-train）</font>**得到的。它在大量未标注的数据上进行预训练，学习语言的广泛特征。Base模型具有庞大的参数规模，能够在文本生成、语义理解和语言翻译等多样化任务中表现出色。

+ **<font style="color:rgb(25, 27, 31);">特点</font>**<font style="color:rgb(25, 27, 31);">：这是基础版本，通常是指经过预训练但未经过特定任务微调的模型</font>
+ **<font style="color:rgb(25, 27, 31);">适用场景：</font>**<font style="color:rgb(25, 27, 31);">适合需要从底层进行自定义开发的场景，例如针对特定领域的进一步微调。</font>
+ **<font style="color:rgb(25, 27, 31);">效果</font>**<font style="color:rgb(25, 27, 31);">：在通用语言生成任务上表现较好，但在特定任务（如对话或指令遵循）上可能不如经过微调的版本</font>

:::color5
**<font style="color:#601BDE;">2. Chat模型（聊天模型）</font>**

:::

Chat模型是在Base模型的基础上，通过第二阶段的**<font style="color:#74B602;">监督微调（SFT）和第三阶段的强化学习（RLHF）</font>**得到的。Chat模型经过通用任务的微调和强化，使其具备对话能力、推理能力、用户偏好对齐或者其他自然语言理解（NLU）的能力。

+ **<font style="color:rgb(25, 27, 31);">特点</font>**<font style="color:rgb(25, 27, 31);">：经过</font>[<font style="color:rgb(9, 64, 142);">对话微调</font>](https://zhida.zhihu.com/search?content_id=254245773&content_type=Article&match_order=1&q=%E5%AF%B9%E8%AF%9D%E5%BE%AE%E8%B0%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（Dialogue Tuning），使其更适合多轮对话场景。</font>
+ **<font style="color:rgb(25, 27, 31);">适用场景</font>**<font style="color:rgb(25, 27, 31);">：适合构建聊天机器人、客服系统等需要自然对话交互的应用。</font>
+ **<font style="color:rgb(25, 27, 31);">效果</font>**<font style="color:rgb(25, 27, 31);">：在对话连贯性、自然性和上下文理解方面表现最佳。</font>

:::color5
**<font style="color:#601BDE;">3. </font>**[**<font style="color:#601BDE;">Instruction模型</font>**](https://zhida.zhihu.com/search?content_id=679864662&content_type=Answer&match_order=1&q=Instruction%E6%A8%A1%E5%9E%8B&zhida_source=entity)**<font style="color:#601BDE;">（指令模型）</font>**

:::

Instruction模型经过指令微调的模型，能够理解和执行复杂的自然语言指令。很多垂领模型，都是在预训练模型的基础上，通过**<font style="color:#74B602;">针对性的指令微调，可以更好地适应最终任务和对齐用户偏好</font>**。在进行指令微调的时候，会将指令以及对应的回答拼接成文本，然后用于微调模型。

+ **<font style="color:rgb(25, 27, 31);">特点</font>**<font style="color:rgb(25, 27, 31);">：经过指令微调（Instruction Tuning），使其更擅长理解和执行人类指令。</font>
+ **<font style="color:rgb(25, 27, 31);">适用场景</font>**<font style="color:rgb(25, 27, 31);">：适合需要模型执行特定指令的任务，如文本生成、总结、翻译等。</font>
+ **<font style="color:rgb(25, 27, 31);">效果</font>**<font style="color:rgb(25, 27, 31);">：在遵循指令方面表现优于 Base 版本，但可能在对话连贯性和自然性上不如 Chat 版本。</font>

:::color5
**<font style="color:#601BDE;">4.效果对比</font>**<font style="color:#601BDE;">：</font>

:::

+ **<font style="color:rgb(25, 27, 31);">通用性</font>**<font style="color:rgb(25, 27, 31);">：Base 模型通用性最强，因为它没有针对特定任务进行优化，可以作为各种任务的基础。Instruct 模型和 Chat 模型则在各自优化的领域（指令执行和对话交互）表现更优，但通用性相对较弱。</font>
+ **<font style="color:rgb(25, 27, 31);">任务执行准确性</font>**<font style="color:rgb(25, 27, 31);">：Instruct 模型在处理明确指令任务时准确性较高，能够按照指令要求生成合适的输出。Chat 模型在对话场景中，对于理解上下文和生成自然回复的准确性更好，但在一些严格的指令任务上可能不如 Instruct 模型。</font>
+ **<font style="color:rgb(25, 27, 31);">交互体验</font>**<font style="color:rgb(25, 27, 31);">：Chat 模型在与用户进行交互时，能够提供更自然、流畅的对话体验，更接近人类的对话方式。Instruct 模型更侧重于准确执行指令，交互体验上可能相对生硬一些。</font>

:::color5
**<font style="color:#601BDE;">5.如何选择：</font>**

:::

+ <font style="color:rgb(25, 27, 31);">如果你正在开发一个聊天机器人，LLaMA-3.2-1B-Chat 是最佳选择，因为它经过了对话微调，能够提供更自然的交互体验。</font>
+ <font style="color:rgb(25, 27, 31);">如果你的应用需要模型执行复杂的指令，如生成代码或总结文档，LLaMA-3.2-1B-Instruct 会更适合。</font>
+ <font style="color:rgb(25, 27, 31);">如果你希望从零开始微调模型以适应特定领域，Base 版本提供了最大的灵活性。</font>



## <font style="color:rgb(1, 1, 1);">如何权衡模型的复杂度和性能？</font>
1. **模型架构选择**：
    - **<font style="color:rgb(51, 51, 51);">简化架构</font>**<font style="color:rgb(51, 51, 51);">：通过选择适当的模型架构（例如，选择较小的网络层数和宽度），可以降低复杂度。可以使用一些已有的高性能基础模型，例如 Transformers，作为起点，然后根据需求调整模型规模。</font>
    - **<font style="color:rgb(51, 51, 51);">剪枝与量化</font>**<font style="color:rgb(51, 51, 51);">：对模型进行剪枝（去掉一些不重要的参数）和量化（将参数从浮点数转换为低精度格式）也能在不显著影响性能的情况下，减少模型的复杂度。</font>
1. **正则化技术**：
    - <font style="color:rgb(51, 51, 51);">使用正则化技术（如 L1 或 L2 正则化、Dropout、数据增强等）可以有效地控制过拟合，帮助在复杂度较低的情况下仍然获得良好的泛化性能。</font>
2. **超参数优化**：
    - <font style="color:rgb(51, 51, 51);">通过超参数优化（例如，使用网格搜索或随机搜索）调整学习率、批量大小、优化器等超参数，以找到最优的训练策略，从而提高模型性能。</font>
3. **模型蒸馏**：
    - <font style="color:rgb(51, 51, 51);">模型蒸馏是一种将大模型的知识传递到小模型的技术。通过训练一个小模型使其尽可能逼近大模型的输出，可以在降低复杂度的同时保持良好的性能。</font>
4. **数据集规模与质量**：
    - <font style="color:rgb(51, 51, 51);">训练数据集的规模和质量对模型的性能有很大影响。选择高质量的训练数据、进行有效的数据预处理和增强，都可以提高模型的表现，进而在一定程度上允许使用更简单的模型。</font>



## <font style="color:rgb(1, 1, 1);">scaling law</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：大模型的 scaling law（扩展法则）指的是在训练大型机器学习模型时，模型的性能（例如准确性、损失等）与模型规模（如参数数量）、训练数据量和计算资源之间存在一定的关系。这种关系通常可以用数学公式或经验法则来描述。</font>

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">定义：⼀种基于实验总结的经验规律 ，指导模型规模、数据量和计算量的合理配置。</font>
+ <font style="color:#1f2329;">作⽤： 在有限的计算资源下 ，找到最优的模型规模和数据量组合。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739253688809-3199020c-0a47-446c-9c1b-f32b24b69114.png)

<font style="color:rgb(51, 51, 51);">具体来说，scaling law 通常包括以下几个方面：</font>

1. **模型规模与性能**：随着模型参数数量的增加，模型的性能通常会提高。这表明更大的模型能够捕获更多的数据特征和模式。
2. **数据量与性能**：在训练模型时，提供更多的数据通常会导致模型性能的提升。尤其是在较小模型的情况下，增加数据量对提升性能的影响会更显著。
3. **计算资源与性能**：使用更多的计算资源（如更高的计算能力和更长的训练时间）也能提升模型的性能。模型训练的时间和成本与性能之间表现出一定的比例关系。
4. **表现的规律性**：在许多情况下，可以发现这些性能的增长是以幂律形式来描述的，比如在某一特定范围内，性能随着参数数量或数据量的增加而按照特定的幂指数函数增长，而不仅仅是线性增长

### <font style="color:rgb(25, 27, 31);">OCR模型的Scaling Law</font>
:::color3
**<font style="color:#117CEE;">核心结论</font>**：标度律在OCR领域成立。模型的**<font style="color:#ED740C;">大小、数据量、计算和性能</font>**之间存在平滑的幂律。

通过探索中小型模型的参数量、计算量和数据量对多种OCR方法准确性的影响，我们成功地证明了幂律定律在OCR领域存在于这三个维度。这一发现为OCR模型设计提供了重要的理论依据。

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741851558270-3ba7b2c8-be36-402c-8fdf-9fca0e02e71a.png)

## <font style="color:rgb(1, 1, 1);">简述大模型，与传统模型的区别</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">以下从多个角度对大语言模型（以Qwen为例）和小模型（以BERT为例）进行对比。</font>

+ **<font style="color:rgb(51, 51, 51);">大模型（Qwen）</font>**<font style="color:rgb(51, 51, 51);">：追求</font>**<font style="color:#ED740C;">通用性和生成能力</font>**<font style="color:rgb(51, 51, 51);">，依赖海量数据和算力，适合复杂开放任务。</font>
+ **<font style="color:rgb(51, 51, 51);">小模型（BERT）</font>**<font style="color:rgb(51, 51, 51);">：专注于</font>**<font style="color:#ED740C;">特定场景的高效微调</font>**<font style="color:rgb(51, 51, 51);">，资源友好，适合结构化理解任务。</font>

:::

与传统模型相比，大模型的主要区别包括：

1. **模型规模**：大模型的参数量远超传统模型。传统模型通常具有较少的参数，结构相对简单。
2. **数据需求**：大模型需要大量的数据进行训练，以避免过拟合并充分利用其复杂性；而传统模型可以在相对较小的数据集上进行训练。
3. **表现能力**：大模型在许多任务上能够实现更高的准确性和泛化能力，尤其是在处理复杂问题时。传统模型可能在特定的任务上表现良好，但在通用性上稍显不足。
4. **计算资源**：由于规模庞大，大模型通常需要强大的计算资源和长时间的训练，而传统模型在计算需求上相对较低。
5. **迁移学习**：大模型通常具有更好的迁移学习能力，可以通过微调在不同的任务上实现较好的性能，而传统模型往往需要针对特定任务进行重新训练。

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


## <font style="color:rgb(51, 51, 51);">实际业务场景，使用LLM还是小模型？</font>
:::color3
<font style="color:rgb(51, 51, 51);">在一个具体的业务场景中，选择大模型还是多个小模型需要综合考虑多种因素。</font>**<font style="color:#ED740C;">大模型在处理复杂任务和大规模数据方面具有显著优势，但在资源需求和维护成本方面存在一定的劣势</font>**<font style="color:rgb(51, 51, 51);">。多个小模型则在灵活性、可解释性和资源效率方面表现出色，但可能在处理复杂关系和大规模数据时略逊一筹。因此，最佳的选择取决于具体的业务需求、资源条件和团队能力。在实际应用中，</font>**<font style="color:#ED740C;">灵活采用混合部署策略</font>**<font style="color:rgb(51, 51, 51);">，充分考虑系统的扩展性和灵活性需求，是提升推荐系统性能和效果的有效途径。</font>

:::

:::color5
**<font style="color:#601BDE;">1.大模型、小模型对比</font>**

:::

1. **大模型的优势**：
    - **<font style="color:rgb(51, 51, 51);">强大的泛化能力</font>**<font style="color:rgb(51, 51, 51);">：大模型经过大规模的数据训练，可以在多种不同的任务和数据类型上表现出色。这使得它能够处理复杂的用户行为模式，捕捉非线性关系，提升推荐的准确性和多样性。</font>
    - **<font style="color:rgb(51, 51, 51);">高效的并行处理</font>**<font style="color:rgb(51, 51, 51);">：大模型通常运行在分布式计算平台上，能够高效地处理大量的数据，满足实时推荐的需求。在面对数以亿计的用户请求时，大模型能够快速响应，保证用户体验。</font>
    - **<font style="color:rgb(51, 51, 51);">深度特征学习</font>**<font style="color:rgb(51, 51, 51);">：大模型可以通过深度神经网络自动提取高阶特征，无需人工设计特征工程，简化了推荐系统的开发流程，同时提升了推荐的精准度。</font>
    - **<font style="color:rgb(51, 51, 51);">持续学习与更新</font>**<font style="color:rgb(51, 51, 51);">：大模型支持在线学习和微调，可以在实时数据流中持续优化模型性能，适应用户行为的变化和市场的动态。</font>
2. **大模型的劣势**：
    - **<font style="color:rgb(51, 51, 51);">高资源消耗</font>**<font style="color:rgb(51, 51, 51);">：训练和运行大模型需要大量的计算资源和存储空间，可能超出中小企业的预算和基础设施能力。</font>
    - **<font style="color:rgb(51, 51, 51);">复杂性与维护成本</font>**<font style="color:rgb(51, 51, 51);">：大模型的架构复杂，维护和优化需要专业的团队和工具，增加了运营成本。</font>
    - **<font style="color:rgb(51, 51, 51);">可解释性有限</font>**<font style="color:rgb(51, 51, 51);">：大模型的决策过程通常是“黑箱”，难以解释推荐的原因，可能影响用户信任和系统的透明度。</font>
    - **<font style="color:rgb(51, 51, 51);">过拟合风险</font>**<font style="color:rgb(51, 51, 51);">：在某些特定的业务场景中，大模型可能会因为其深度和复杂性而出现过拟合，导致推荐结果不够稳健。</font>
3. **多个小模型的优势**：
    - **<font style="color:rgb(51, 51, 51);">资源效率高</font>**<font style="color:rgb(51, 51, 51);">：小模型的资源需求较低，可以在本地服务器或边缘设备上运行，降低了整体的计算成本和资源消耗。</font>
    - **<font style="color:rgb(51, 51, 51);">灵活性与针对性</font>**<font style="color:rgb(51, 51, 51);">：可以根据不同的用户群体、地域、产品类别等，训练和部署多个小模型，实现更加个性化和精细化的推荐。</font>
    - **<font style="color:rgb(51, 51, 51);">易于维护与更新</font>**<font style="color:rgb(51, 51, 51);">：小模型的规模较小，维护和更新相对简单，可以根据具体的业务需求快速调整和优化模型。</font>
    - **<font style="color:rgb(51, 51, 51);">更高的可解释性</font>**<font style="color:rgb(51, 51, 51);">：小模型的结构相对简单，推荐的原因更加透明和易于解释，有助于提升用户的信任感和满意度。</font>
    - **<font style="color:rgb(51, 51, 51);">容错能力强</font>**<font style="color:rgb(51, 51, 51);">：在分布式部署中，如果某个小模型出现问题，不会对整个系统造成重大影响，提升了系统的整体稳定性和可靠性。</font>
4. **多个小模型的劣势**：
    - **<font style="color:rgb(51, 51, 51);">计算资源的分散利用</font>**<font style="color:rgb(51, 51, 51);">：需要多台设备或分布式计算环境来运行多个小模型，可能增加整体的管理和协调成本。</font>
    - **<font style="color:rgb(51, 51, 51);">难以处理复杂关系</font>**<font style="color:rgb(51, 51, 51);">：由于模型规模的限制，小模型在处理复杂的用户行为模式和非线性关系上可能表现不如大模型。</font>
    - **<font style="color:rgb(51, 51, 51);">模型协同与一致性</font>**<font style="color:rgb(51, 51, 51);">：在多个小模型协同工作的场景中，如何确保各模型之间的协同一致和结果的统一性，是一个需要解决的挑战。</font>
    - **<font style="color:rgb(51, 51, 51);">模型训练的效率</font>**<font style="color:rgb(51, 51, 51);">：训练和优化多个小模型需要额外的时间和资源投入，尤其是当模型数量较多时，整体的工作量会显著增加。</font>

:::color5
**<font style="color:#601BDE;">2.业务场景如何选择</font>**

:::

1. **适用大模型的情况**：
    - **<font style="color:rgb(51, 51, 51);">复杂的推荐逻辑</font>**<font style="color:rgb(51, 51, 51);">：如果推荐系统需要处理高度复杂的用户行为模式和产品关系，大模型能够提供更强大的特征提取和模式识别能力。</font>
    - **<font style="color:rgb(51, 51, 51);">实时大规模处理</font>**<font style="color:rgb(51, 51, 51);">：在需要处理海量实时数据和快速响应的场景下，大模型的高效并行处理能力是一个重要的优势。</font>
    - **<font style="color:rgb(51, 51, 51);">深度学习与个性化</font>**<font style="color:rgb(51, 51, 51);">：如果业务需求要求推荐系统具备深度的个性化和精准度，大模型可以更好地满足这些要求。</font>
2. **适用多个小模型的情况**：
    - **<font style="color:rgb(51, 51, 51);">个性化与多样性需求</font>**<font style="color:rgb(51, 51, 51);">：如果需要针对不同的用户群体、产品类别或地域提供差异化的推荐，多个小模型可以实现更加精细和多样化的推荐策略。</font>
    - **<font style="color:rgb(51, 51, 51);">资源受限的环境</font>**<font style="color:rgb(51, 51, 51);">：在计算资源有限的边缘设备或本地服务器上，小模型能够高效运行，满足实时推荐的需求。</font>
    - **<font style="color:rgb(51, 51, 51);">快速迭代与优化</font>**<font style="color:rgb(51, 51, 51);">：业务需求变化迅速，需要推荐系统能够快速响应和调整，多个小模型的灵活性和易维护性提供了一定的优势。</font>
    - **<font style="color:rgb(51, 51, 51);">高透明度与可解释性</font>**<font style="color:rgb(51, 51, 51);">：如果业务需要推荐系统具备较高的透明度和可解释性，小模型的简单结构和易于解释的特性是一个优势。</font>
3. **混合部署的策略**：
    - <font style="color:rgb(51, 51, 51);">在某些业务场景中，结合使用大模型和多个小模型可能是最优的选择。例如，利用大模型进行全局的用户画像和高层次特征提取，再结合多个小模型在具体业务模块或特定用户群体中进行精细化推荐。这种混合部署的方式，可以兼顾大模型的强大力量和小模型的灵活性，提升整体推荐系统的性能和效果。</font>

:::color5
**<font style="color:#601BDE;">3.模型选择的指导因素</font>**

:::

1. **业务需求**：
    - <font style="color:rgb(51, 51, 51);">需要明确具体的业务目标和需求，包括推荐的精准度、个性化程度、实时性、透明度等方面的优先级。</font>
    - <font style="color:rgb(51, 51, 51);">如果业务需求强调高度个性化和复杂推荐逻辑，大模型可能是更合适的选择。</font>
    - <font style="color:rgb(51, 51, 51);">如果业务需求侧重于快速响应、本地部署和成本控制，多个小模型更具优势。</font>
2. **资源与预算**：
    - <font style="color:rgb(51, 51, 51);">评估可用的计算资源和预算，确定是否能够支持大模型的训练和运行需求。</font>
    - <font style="color:rgb(51, 51, 51);">如果资源有限，多个小模型可能是一个更经济的选择，尤其是在边缘计算和本地部署的场景下。</font>
3. **技术能力与团队资源**：
    - <font style="color:rgb(51, 51, 51);">考虑团队的技术能力和维护能力，选择与团队能力相匹配的模型规模和复杂度。</font>
    - <font style="color:rgb(51, 51, 51);">大模型需要更专业的团队和工具支持，而小模型的维护相对简单，适合团队资源有限的情况。</font>
4. **系统的扩展性与灵活性**：
    - <font style="color:rgb(51, 51, 51);">考虑系统的未来扩展性和灵活性需求，选择能够适应业务增长和变化的模型策略。</font>
    - <font style="color:rgb(51, 51, 51);">多个小型模型通过模块化部署和管理，能够更灵活地适应业务的变化和发展。</font>
5. **模型的可解释性与透明度**：
    - <font style="color:rgb(51, 51, 51);">根据业务对模型决策过程的要求，选择具备更高可解释性的模型，尤其是在需要用户信任和政策合规的场景中。</font>
6. **模型的维护与更新**：
    - <font style="color:rgb(51, 51, 51);">考虑模型的维护和更新频率，选择能够快速响应业务变化和用户反馈的模型策略。</font>
    - <font style="color:rgb(51, 51, 51);">多个小型模型由于其规模较小，通常能够更快速地进行优化和更新。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);"></font>

## <font style="color:rgb(53, 53, 53);">“零样本”和“少样本”学习的</font>
<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">“零样本学习”（Zero-Shot Learning）和“少样本学习”（Few-Shot Learning）是机器学习领域中的两个重要概念，尤其在自然语言处理（NLP）和计算机视觉等领域中得到了广泛应用。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">零样本学习（Zero-Shot Learning）</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">“零样本学习”是指模型能够识别或分类它在训练时未见过的类别或任务。这意味着模型没有接收到任何关于特定类别的示例数据，但仍能根据已有的知识和理解进行推理和判断。例如，在聊天机器人应用中，一个模型可能在没有接受过特定类型的问题（如关于某个新出现的技术或事件）的训练的情况下，仍能够理解并回答相关问题。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">实现零样本学习通常依赖于模型的泛化能力、上下文理解和对概念之间关系的推理能力。例如，ChatGPT能利用其在大规模文本数据上学习到的语言模式和并行知识来回答用户的问题，即便那些问题涉及到它没有直接训练的专业领域或新兴话题。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">少样本学习（Few-Shot Learning）</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">“少样本学习”则是在模型训练中，仅提供了少量示例数据的情况下进行学习。在这种设定下，模型需要依靠这些有限的样本进行有效的推理和预测。例如，如果在训练一个模型时只提供了每个类别的几个示例，模型必须能够从这些少量样本中提取特征并进行分类。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">少样本学习通常通过以下几种方式实现:</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">增强学习（Data Augmentation）</font><font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">: 通过对已有样本进行变换或合成来生成更多的训练数据。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">迁移学习（Transfer Learning）</font><font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">: 利用在大规模数据集上训练的模型参数，快速适应小规模数据集。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">原型网络（Prototypical Networks）</font><font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">: 通过计算样本与类别原型之间的距离来进行分类。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">在 ChatGPT 的上下文中，少样本学习使得用户可以在对话中提供几个示例或指令后，模型能很快适应并生成相应的答案或执行特定的任务。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);"></font>

## <font style="color:rgb(53, 53, 53);">大模型的涌现能力</font>
<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">模型的涌现能力（Emergent Abilities）是指大型预训练模型在特定的输入条件下展现出超出其训练目标或设计初衷的复杂行为或性能。这种能力通常不是在模型设计时明确编码或预期的，而是在模型处理复杂任务或进行推理时自发显现的。</font>

<font style="color:rgb(51, 51, 51);background-color:rgb(249, 250, 255);">以下是一些关于大模型涌现能力的关键点：</font>

    1. **<font style="background-color:rgb(249, 250, 255);">规模依赖性</font>**<font style="background-color:rgb(249, 250, 255);">：大模型通常指参数量极大的模型，随着参数数量和训练数据规模的增加，模型在一些任务上的表现可以显著提升，涌现出新的能力。</font>
    2. **<font style="background-color:rgb(249, 250, 255);">复杂任务处理</font>**<font style="background-color:rgb(249, 250, 255);">：在面对复杂的自然语言理解、推理或生成任务时，大模型可能展现出在训练期间未直接优化的能力。例如，一些大语言模型能够进行逻辑推理、编程、复杂的对话等。</font>
    3. **<font style="background-color:rgb(249, 250, 255);">少样本学习</font>**<font style="background-color:rgb(249, 250, 255);">：大模型在少量示例的情况下进行学习和推理的能力是一个典型的涌现现象。这意味着它们可以通过上下文理解新的任务，而不需要为每个新任务进行大规模再训练。</font>
    4. **<font style="background-color:rgb(249, 250, 255);">多样性</font>**<font style="background-color:rgb(249, 250, 255);">：涌现能力往往表现出多样性和适应性。相同的模型在不同的上下文或任务下可能会展现出不同的行为。</font>
    5. **<font style="background-color:rgb(249, 250, 255);">研究与应用</font>**<font style="background-color:rgb(249, 250, 255);">：涌现能力的研究是当前人工智能领域的热点，特别是在如何利用这些能力来提升模型在实际应用中的表现。</font>

## 大模型迁移学习
**定义**：<font style="color:#1f2329;"> </font><font style="color:#dc9b04;">迁移学习（TransferLearning）是指将⼀个领域（源领域）中学到的知识迁移到另⼀个领域（⽬标领域）中应⽤的技术。</font><font style="color:#1f2329;">通过这种⽅式，模型在⽬标任务中可以利⽤先前训练的模型参数，从⽽减少对⼤规模数据的需求和训练时间。</font>

**<font style="color:#1f2329;">应用场景</font>**<font style="color:#1f2329;">: 迁移学习通常⽤于数据量不⾜或训练成本较⾼的任务中，</font><font style="color:#2ea121;">通过使⽤已经在相关任务上训练过的模型进⾏微调或调整</font><font style="color:#1f2329;">，使其能够适应新的任务。</font>

**在大模型中的应用**：<font style="color:#1f2329;">在⼤模型（例如 GPT、BERT）中，迁移学习的核⼼思想体现在预训练-微调（Pre-training & Fine-tuning）的范式中。⾸先在⼤规模的通⽤数据（如互联⽹⽂本）上进⾏预训练，获得能够理解⼴泛语义的通⽤模型；</font><font style="color:#2ea121;">接着，在⽬标任务的⼩规模数据集上进⾏微调，使模型能够适应特定任务。</font>

<font style="color:#1f2329;">预训练是⼀种从头开始训练模型的⽅式：所有的模型权重都被随机初始化，然后在没有任何先验知识的情况下开始训练，这个过程不仅需要海量的训练数据，⽽且时间和经济成本都⾮常⾼。因此，⼤部分情况下，我们都不会从头训练模型，⽽是将别⼈预训练好的模型权重通过迁移学习应⽤到⾃⼰的模型中，即使⽤⾃⼰的任务语料对模型进⾏“⼆次训练”，通过微调参数使模型适⽤于新任务。</font>

**<font style="color:#1f2329;">优点</font>**<font style="color:#1f2329;">：</font>

+ <font style="color:#1f2329;">节省计算资源: 避免从零开始训练模型，节省⼤量计算资源和时间。</font>
+ <font style="color:#1f2329;">减少训练数据需求: 即使⽬标任务的数据量不⾜，预训练的知识仍然可以帮助模型在⽬标任务上取得良好的效果。</font>
+ <font style="color:#1f2329;">适应新任务: 迁移学习允许⼤模型快速适应不同的任务和领域，具有很好的灵活性。</font>

<font style="color:#1f2329;"></font>

## <font style="color:#1f2329;">文本输入到大模型的全过程</font>
:::color3
<font style="color:rgb(51, 51, 51);">假设我们正在使用一个基于Transformer的大模型进行文本摘要任务。流程如下：</font>

:::

1. **输入文本预处理**：
    - <font style="color:rgb(51, 51, 51);">分词（比如将长句子分成较小的单位）。</font>
    - <font style="color:rgb(51, 51, 51);">去除无用的标点符号和停用词。</font>
2. **向量化**：
    - <font style="color:rgb(51, 51, 51);">使用预训练的词嵌入模型将文本转换为向量表示。</font>
3. **模型输入层**：
    - <font style="color:rgb(51, 51, 51);">将向量输入到模型的第一个层，开始处理。</font>
4. **模型主体处理**：
    - <font style="color:rgb(51, 51, 51);">使用自注意力机制捕捉文本中的长距离依赖。</font>
    - <font style="color:rgb(51, 51, 51);">应用前馈神经网络进行非线性变换。</font>
    - <font style="color:rgb(51, 51, 51);">使用跳跃连接保持信息流动。</font>
5. **输出层处理**：
    - <font style="color:rgb(51, 51, 51);">生成潜在的输出表示，并应用Softmax函数转换为概率分布。</font>
6. **文本生成与后处理**：
    - <font style="color:rgb(51, 51, 51);">根据概率分布选择每个词，生成摘要文本。</font>
    - <font style="color:rgb(51, 51, 51);">对生成的文本进行格式调整和语义优化。</font>
7. **性能监控与优化**：
    - <font style="color:rgb(51, 51, 51);">监控GPU和CPU的使用情况，确保资源充足。</font>
    - <font style="color:rgb(51, 51, 51);">调整模型参数和训练策略，提升生成摘要的质量和速度。</font>



# <font style="color:#1f2329;">Encoder-only & Decoder-only & Encoder-Decoder</font>
## 三种架构对比<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color1
**<font style="color:#1f2329;">Encoder-Only</font>**<font style="color:#1f2329;">:⽤于理解任务，适合⽂本分类、问答、信息抽取等场景。</font>

**<font style="color:#1f2329;">Decoder-Only</font>**<font style="color:#1f2329;">：⽤于⽣成任务，擅⻓⽂本⽣成、对话系统、续写等。</font>

**<font style="color:#1f2329;">Encoder-Decoder</font>**<font style="color:#1f2329;">：⽤于处理输⼊-输出映射的任务，特别适合机器翻译、⽂本摘要等。</font>

:::

| **架构** | **Encoder-Only** | **Decoder-Only** | **Encoder-Decoder** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">核心能力</font>** | <font style="color:rgb(51, 51, 51);">语义理解</font> | <font style="color:rgb(51, 51, 51);">文本生成</font> | <font style="color:rgb(51, 51, 51);">理解+生成</font> |
| **<font style="color:rgb(51, 51, 51);">注意力方向</font>** | **<font style="color:#74B602;">双向</font>** | <font style="color:#74B602;">单向（</font>**<font style="color:#74B602;">因果掩码</font>**<font style="color:#74B602;">）</font> | **<font style="color:#74B602;">编码器双向，解码器单向</font>** |
| **<font style="color:rgb(51, 51, 51);">经典模型</font>** | <font style="color:rgb(51, 51, 51);">BERT, RoBERTa</font> | <font style="color:rgb(51, 51, 51);">GPT-3, LLaMA</font> | <font style="color:rgb(51, 51, 51);">T5, BART, Transformer</font> |
| **<font style="color:rgb(51, 51, 51);">适用任务</font>** | <font style="color:rgb(51, 51, 51);">分类、NER、相似度</font> | <font style="color:rgb(51, 51, 51);">生成、问答、代码</font> | <font style="color:rgb(51, 51, 51);">翻译、摘要、序列到序列</font> |
| **<font style="color:rgb(51, 51, 51);">训练目标</font>** | <font style="color:rgb(51, 51, 51);">MLM, NSP</font> | <font style="color:rgb(51, 51, 51);">因果语言建模</font> | <font style="color:rgb(51, 51, 51);">去噪、跨语言建模</font> |
| **<font style="color:rgb(51, 51, 51);">资源消耗</font>** | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">高（生成需迭代）</font> | <font style="color:rgb(51, 51, 51);">高（双结构）</font> |
| **<font style="color:#ED740C;">优点</font>** | <font style="color:rgb(51, 51, 51);">上下文理解能力强，适合语义分析。</font> | <font style="color:rgb(51, 51, 51);">生成流畅，适合创意性任务。</font> | <font style="color:rgb(51, 51, 51);">灵活适配输入输出不等长的复杂任务。</font> |
| **<font style="color:#ED740C;">缺点</font>** | <font style="color:rgb(51, 51, 51);">无法直接生成文本，需额外结构适配生成任务。</font> | <font style="color:rgb(51, 51, 51);">单向上下文可能忽略后续信息，长文本生成可能重复或偏离主题。</font> | <font style="color:rgb(51, 51, 51);">参数量大，训练成本高，推理速度较慢。</font> |


## <font style="color:#6425d0;">Encoder-Only</font>
:::color5
**<font style="color:#601BDE;">1.架构特点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#2F8EF4;">架构特点</font>**<font style="color:#1f2329;">：Encoder-only 模型只使⽤编码器部分。编码器的核⼼是处理输⼊序列，并⽣成该序列的上下⽂向量（即隐藏状态），它能够很好地捕捉输⼊序列的全局信息。</font>

:::color5
**<font style="color:#601BDE;">2.典型模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#2F8EF4;">典型模型</font>**：

+ **<font style="color:rgb(51, 51, 51);">BERT</font>**<font style="color:rgb(51, 51, 51);">：首个双向预训练模型，通过掩码语言建模（MLM）学习上下文表征。</font>
+ **<font style="color:rgb(51, 51, 51);">RoBERTa</font>**<font style="color:rgb(51, 51, 51);">：BERT 的优化版，更大数据量、更长训练步长。</font>
+ **<font style="color:rgb(51, 51, 51);">ALBERT</font>**<font style="color:rgb(51, 51, 51);">：参数共享减少计算量，适合资源受限场景。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:#de7802;">⽂本分类</font><font style="color:#1f2329;">：根据输⼊的⽂本进⾏分类（如情感分析、新闻分类）。</font>
+ <font style="color:#de7802;">问答任务</font><font style="color:#1f2329;">（抽取式）：通过输⼊问题和上下⽂，模型从上下⽂中抽取出准确的答案。</font>
+ <font style="color:#de7802;">命名实体识别</font><font style="color:#1f2329;">（NER）：标注⽂本中的特定实体（如⼈名、地名等）。</font>

## <font style="color:#6425d0;">decoder-only 的架构</font>
:::color5
**<font style="color:#601BDE;">1.架构特点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#2F8EF4;">架构特点</font>**<font style="color:#245bdb;"> </font><font style="color:#1f2329;">：Decoder-only 模型只使⽤解码器部分。解码器主要⽤于⽣成序列，它依赖于⾃回归机 制，每次⽣成⼀个单词，并根据之前⽣成的单词继续预测下⼀个单词。</font>

:::color5
**<font style="color:#601BDE;">2.典型模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#2F8EF4;">典型模型</font>**<font style="color:#1f2329;">：</font><font style="color:#d83931;">GPT（GenerativePretrainedTransformer）是 Decoder-only架构的代表。</font>

+ **<font style="color:rgb(51, 51, 51);">GPT 系列</font>**<font style="color:rgb(51, 51, 51);">（GPT-3、GPT-4）：通过海量数据预训练，Few-Shot 学习能力强。</font>
+ **<font style="color:rgb(51, 51, 51);">PaLM</font>**<font style="color:rgb(51, 51, 51);">：谷歌大规模模型，强调推理和代码生成能力。</font>
+ **<font style="color:rgb(51, 51, 51);">LLaMA</font>**<font style="color:rgb(51, 51, 51);">：Meta 开源模型，参数量高效。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#2F8EF4;">应用场景</font>**<font style="color:#1456f0;"> </font><font style="color:#1f2329;">：这种架构适合⽣成类任务 ，例如：</font>

+ <font style="color:#de7802;">⽂本⽣成</font><font style="color:#1f2329;">：根据提⽰⽣成⼀段连贯的⽂本（如对话⽣成、⾃动写作）。</font>
+ <font style="color:#1456f0;"></font><font style="color:#de7802;">对话系统</font><font style="color:#1f2329;">：逐步⽣成⾃然语⾔响应，回答⽤户提问。</font>
+ <font style="color:#de7802;">机器翻译</font><font style="color:#1f2329;">（部分场景下）：逐词⽣成⽬标语⾔的翻译结果。</font>

## <font style="color:#6425d0;">Encoder-Decoder模型：</font>
:::color5
**<font style="color:#601BDE;">1.架构特点</font>**

:::

**<font style="color:#2F8EF4;">架构特点</font>**<font style="color:#1f2329;">：Encoder-Decoder 模型包含编码器和解码器两个部分。编码器处理输⼊序列，⽣成上 下⽂向量；解码器则根据编码器的输出⽣成⽬标序列。这个结构能够同时处理输⼊和输出序列的关联。</font>

:::color5
**<font style="color:#601BDE;">2.典型模型</font>**

:::

**<font style="color:#2F8EF4;">典型模型</font>**<font style="color:#1f2329;">：</font><font style="color:#d83931;">T5（Text-to-TextTransferTransformer）和Transformer（Vaswanietal. 提出的基础模型）是典型的 Encoder-Decoder模型。</font>

+ **<font style="color:rgb(51, 51, 51);">T5</font>**<font style="color:rgb(51, 51, 51);">：将任务统一为文本到文本格式，适用翻译、摘要等。</font>
+ **<font style="color:rgb(51, 51, 51);">BART</font>**<font style="color:rgb(51, 51, 51);">：结合双向编码器与自回归解码器，擅长文本重构任务。</font>
+ **<font style="color:rgb(51, 51, 51);">Transformer</font>**<font style="color:rgb(51, 51, 51);">（原始模型）：首个完全基于注意力的机器翻译模型。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:#1456f0;"></font><font style="color:#de7802;">机器翻译</font><font style="color:#1f2329;">：将⼀个句⼦从源语⾔翻译成⽬标语⾔，编码器负责理解源语⾔句⼦，解码器负责⽣成⽬标语⾔句⼦。</font>
+ <font style="color:#1456f0;"></font><font style="color:#de7802;">⽂本摘要</font><font style="color:#1f2329;">：编码器处理⻓⽂本，解码器⽣成简短摘要。</font>
+ <font style="color:#de7802;">⽂本⽣成</font><font style="color:#1f2329;">（条件⽣成）：如⽂本填空或根据输⼊⽣成对应的完整⽂本。</font>

## <font style="color:#6425d0;">主要区别总结：</font>
<font style="color:#1f2329;">Encoder-Only:⽤于理解任务，适合⽂本分类、问答、信息抽取等场景。</font>

<font style="color:#1f2329;">Decoder-Only：⽤于⽣成任务，擅⻓⽂本⽣成、对话系统、续写等。</font>

<font style="color:#1f2329;">Encoder-Decoder：⽤于处理输⼊-输出映射的任务，特别适合机器翻译、⽂本摘要等。</font>

## <font style="color:#1f2329;">为什么大模型使用Decoder-Only?</font>
```python

1 [开始标记] --> [解码器]
2					|	
3				[输出词1] -->	[解码器]
4									|
5								[输出词2] --> [解码器]
6												|
7											[输出词3] --> ...

```

1. **简化模型架构**：相较于 encoder-decoder 结构，decoder-only 架构在实现上更为简单，容易训练和优化。这种结构通常只需要关注生成的过程，省去了编码阶段的复杂性。
2. **自回归生成**：decoder-only 模型（如 GPT 系列）使用自回归方式生成文本，即每一步生成的输出依赖于之前的输出。这种方式适用于许多自然语言处理任务，如文本生成、对话系统等。
3. **灵活性**：由于 decoder-only 模型主要关注生成，自然可以适应不同的输入格式。比如，用户可以通过提供部分文本或上下文信息来指导模型生成相应的内容，无需进行特定的编码处理。
4. **大规模预训练**：许多 decoder-only 模型在大规模文本上进行预训练，能够学习到丰富的语言特征和知识，进而在特定任务上进行微调。这一过程的有效性在很多任务中都得到了验证。
5. **处理长文本的能力**：一些 decoder-only 模型在处理长文本时表现出色，能够在生成过程中考虑上下文信息，保证生成内容的连贯性和一致性。



# LLM模型
## Gemma-3
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">在巴黎开发者日上，开源Gemma系模型正式迭代到第三代，原生支持多模态，128k上下文。</font>

<font style="color:rgba(0, 0, 0, 0.9);">此次，Gemma 3一共开源了四种参数，1B、4B、12B和27B。最最最关键的是，一块GPU/TPU就能跑模型。</font>

:::

:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3是谷歌迄今最先进、最便携的开源模型，采用与Gemini 2.0模型相同的研究和技术打造。专为</font>**<font style="color:#ED740C;">在端侧设备上直接运行</font>**<font style="color:rgba(0, 0, 0, 0.9);">而设计——从手机和笔记本电脑到工作站，帮助开发者在需要的地方创建AI应用。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[gemma-3](https://huggingface.co/collections/google/gemma-3-release-67c6c6f89c4f76621268bb6d)

**paper：**[**Gemma 3 Technical Report**](https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf)

**参考：**[**谷歌Gemma 3上线！单GPU最强多模态手机可跑，27B完胜o3-mini**](https://mp.weixin.qq.com/s/buqtV1nEDhpvdvEFhRcoIA)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742207515480-2f0d38ab-e3d3-48e3-8ec2-7a0fb9f75fdf.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgba(0, 0, 0, 0.9);">使用世界最佳单设备加速模型进行开发：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3在LMArena排行榜的初步人类偏好评估中超越了Llama-405B、DeepSeek-V3和o3-mini，能在单个GPU或TPU主机上运行，开发独特的用户体验。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">支持140种语言，走向全球：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3为超过35种语言提供开箱即用的支持，并为超过140种语言提供预训练支持。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">创建具有高级文本和视觉推理能力的AI：</font>**<font style="color:rgba(0, 0, 0, 0.9);">轻松开发可以分析图像、文本和短视频的应用程序，为交互式和智能应用开创新的可能性。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">通过扩展的上下文窗口处理复杂任务：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3提供128k token的上下文窗口，让应用程序能够处理和理解海量信息。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">使用函数调用创建AI驱动的工作流：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3支持函数调用和结构化输出，帮助你实现任务自动化并构建智能体验。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">使用量化模型更快实现高性能：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3推出官方量化版本，在保持高精度的同时减少模型大小和计算需求。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">相比Gemma 2，研究者为Gemma 3预训练模型分配了更大的token预算。其中，Gemma 3 27B规模的模型在14万亿个token上进行训练，12B 规模的模型使用12T个token，4B 规模的模型使用4T个token，而1B规模的模型使用 2T个token。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **LLM：**

<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3模型沿用了与前代版本相同的解码器Transformer 结构，其大部分架构元素与前两代Gemma版本类似。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究采用了分组查询注意力（</font><font style="color:#74B602;">Grouped-Query Attention, GQA</font><font style="color:rgba(0, 0, 0, 0.9);">），并结合了</font>**<font style="color:#74B602;"> RMSNorm</font>**<font style="color:rgba(0, 0, 0, 0.9);">的后归一化（post-norm）和前归一化（pre-norm）。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究者在自注意力机制中交替使用局部</font>**<font style="color:#74B602;">滑动窗口自注意力</font>**<font style="color:rgba(0, 0, 0, 0.9);">和全局自注意力，按照5层局部层对应1层全局层的模式排列，模型的第一层为局部层。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在全局自注意力层上，研究者将</font>**<font style="color:#74B602;">RoPE的基准频率从10K提高到1M</font>**<font style="color:rgba(0, 0, 0, 0.9);">，而局部层的频率保持在10K。此外，他们采用了</font>**<font style="color:#74B602;">位置插值方法</font>**<font style="color:rgba(0, 0, 0, 0.9);">，以扩展全局自注意力层的适用范围。</font>

2. **视觉编码器：**

<font style="color:rgba(0, 0, 0, 0.9);">研究采用了一种</font>**<font style="color:#74B602;">400M规模的SigLIP编码器变体</font>**<font style="color:rgba(0, 0, 0, 0.9);">，这是一种基于Vision Transformer的模型，并使用CLIP损失的变体进行训练。Gemma视觉编码器的输入为调整尺寸后的896 × 896像素的方形图像，并在视觉助手任务的数据上进行微调。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在pre-train和post-train过程中，Gemma 3使用了蒸馏技术，并通过强化学习和模型合并的组合，进行了优化。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在post-train阶段，使用多种奖励函数来提升模型在</font>**<font style="color:#74B602;">帮助性、数学、编程、推理、遵循指令和多语言</font>**<font style="color:rgba(0, 0, 0, 0.9);">能力方面的表现，同时最小化模型的有害性。Gemma 3主要使用了4个组件：</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">从更大的指令模型中提取到Gemma 3预训练检查点</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">基于人类反馈的强化学习（RLHF），使模型预测与人类偏好保持一致。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">机器反馈强化学习（RLMF），增强数学推理。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">强化学习执行反馈（RLEF），提高编码能力。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在多项基准测试中，Gemma 3全家桶相较于上一代实现了全面提升，27B模型在数学性能暴涨33-45分。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742206588016-d193937e-b4d6-4c3f-9343-5d250ea587be.png)



## DeepSeek
### [DeepSeek v3](https://mp.weixin.qq.com/s/dRk0f886tWlCRuz1z8rfww)
**简介**：发布了其最新的大型语言模型 DeepSeek-V3，这款模型在性能和效率方面都取得了显著的进步，成为当前最强大的开源基础模型之一。DeepSeek-V3 是一款拥有 671B参数的大型混合专家 (MoE) 模型，其中每个 token 会有 37 B参数被激活。

**创新**：为了实现高效的推理和成本效益的训练，[DeepSeek-V3](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=5&q=DeepSeek-V3&zhida_source=entity) 采用了（1）<font style="color:#DF2A3F;">多头潜在注意力 (MLA) </font>和 （2）[<font style="color:#DF2A3F;">DeepSeekMoE</font>](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=DeepSeekMoE&zhida_source=entity)<font style="color:#DF2A3F;"> 架构</font>，这两个架构在 DeepSeek-V2 中已经得到了充分验证。此外，DeepSeek-V3 还开创了一种（3）<font style="color:#DF2A3F;">无辅助损失策略来平衡负载</font>，并设置了（4）<font style="color:#DF2A3F;">多 token 预测训练目标</font>以进一步提升性能。

**DeepSeekMOE:**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738810351531-35c5a94c-2617-45f1-9f66-afcdc52c95dd.png)

[**<font style="color:rgb(25, 27, 31);">多头潜在注意力</font>**](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=2&q=%E5%A4%9A%E5%A4%B4%E6%BD%9C%E5%9C%A8%E6%B3%A8%E6%84%8F%E5%8A%9B&zhida_source=entity)**<font style="color:rgb(25, 27, 31);"> (MLA)</font>**

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1738810362585-66b39209-096e-4367-a8fb-f5b0d2aad9b4.webp)

<font style="color:rgb(25, 27, 31);">MLA 架构的核心思想是对注意力键和值进行低秩联合压缩，从而减少推理过程中的 Key-Value (KV) 缓存。它通过以下步骤实现：</font>

<font style="color:rgb(25, 27, 31);">压缩: 将注意力输入 h_t 映射到一个压缩的潜在向量 c_KV_t。</font>

<font style="color:rgb(25, 27, 31);">生成键: 使用 W_UK 和 W_VU 矩阵将 c_KV_t 映射到压缩的键和值。</font>

<font style="color:rgb(25, 27, 31);">生成解码器: 使用</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(25, 27, 31);">RoPE</font>](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=RoPE&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">矩阵生成带有旋转位置嵌入 (RoPE) 的解码器。</font>

<font style="color:rgb(25, 27, 31);">计算注意力: 使用 softmax 函数计算注意力权重，并生成最终的注意力输出 u_t。</font>

<font style="color:rgb(25, 27, 31);">MLA 架构只需要缓存压缩后的潜在向量和带有 RoPE 的解码器，从而显著减少了 KV 缓存，同时保持了与标准多头注意力 (MHA) 相当的性能。</font>

**<font style="color:rgb(25, 27, 31);">DeepSeekMoE：辅助损失免费负载平衡</font>**

<font style="color:rgb(25, 27, 31);">DeepSeekMoE 架构使用更细粒度的专家，并将一些专家隔离为共享专家。每个 token 的 FFN 输出 h’_t 通过以下步骤计算：</font>

<font style="color:rgb(25, 27, 31);">共享专家: 使用共享专家 FFN( ) (·) 计算共享专家的输出。</font>

<font style="color:rgb(25, 27, 31);">路由专家: 使用路由专家 FFN( ) (·) 计算路由专家的输出，并使用门控值 g_i,t 选择激活的专家。</font>

<font style="color:rgb(25, 27, 31);">输出: 将共享专家和路由专家的输出相加，得到最终的 FFN 输出 h’_t。</font>

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 还引入了一种辅助损失免费负载平衡策略，通过引入偏置项 b_i 并将其添加到相应的亲和度分数 s_i,t 中，来确定 top-K 路由。通过动态调整偏置项，DeepSeek-V3 能够在整个训练过程中保持平衡的专家负载，并取得比纯粹使用辅助损失的模型更好的性能。</font>

**<font style="color:rgb(25, 27, 31);">多 token 预测</font>**

<font style="color:rgb(25, 27, 31);">DeepSeek-V3 采用了一种名为多 token 预测 (</font>[MTP](https://zhida.zhihu.com/search?content_id=707009763&content_type=Answer&match_order=1&q=MTP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">) 的训练目标，该目标扩展了预测范围，以便在每个位置预测多个未来的 token。MTP 目标可以提高数据效率和模型的预测能力，并通过预先规划未来的 token 的表示来提升性能。</font>

<font style="color:rgb(25, 27, 31);">MTP 实现了 D 个连续的模块来预测 D 个额外的 token，每个模块都包含一个共享嵌入层、一个共享输出头、一个 Transformer 模块和一个投影矩阵。每个 MTP 模块都使用线性投影将 token 的表示和嵌入相连接，然后通过 Transformer 模块生成输出表示，并计算额外的预测 token 的概率分布。</font>

<font style="color:rgb(25, 27, 31);"></font>

### <font style="color:rgb(25, 27, 31);">DeepSeek-R1-INT8</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">美团搜索和推荐平台部对DeepSeek R1模型进行了INT8精度量化尝试，发现使用INT8量化后模型精度基本无损。基于INT8量化，DeepSeek R1模型解锁了芯片限制，可以部署到A100等其他型号GPU；并且相比BF16实现了50%的吞吐提升，进一步降低了推理成本。量化代码已经发布在了开源LLM推理框架SGLang上，量化模型已经发布到了Hugging Face社区，方便用户使用。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">参考</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>[https://mp.weixin.qq.com/s/TCkpG1Kn9tMYQeN2PCnwoA](https://mp.weixin.qq.com/s/TCkpG1Kn9tMYQeN2PCnwoA)

:::

**<font style="color:rgba(0, 0, 0, 0.9);">背景：</font>**<font style="color:rgba(0, 0, 0, 0.9);">DeepSeek R1横空出世后，吸引了众多公司和个人用户尝试其满血版本部署。然而原生版本的模型权重为FP8数据格式，对GPU芯片类型有严格限制，仅能被英伟达新型GPU支持（</font><font style="color:rgb(136, 136, 136);">如Ada、Hopper架构芯片</font><font style="color:rgba(0, 0, 0, 0.9);">），其他型号GPU（</font><font style="color:rgb(136, 136, 136);">如A100</font><font style="color:rgba(0, 0, 0, 0.9);">）无法直接部署。尽管我们可以将FP8权重反量化为BF16权重后，在A100等GPU上进行推理，但是这对显存的要求提升了一倍，推理吞吐也会下降。</font>

:::color5
**<font style="color:#601BDE;">1.DeepSeek R1 精度介绍</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">根据DeepSeek最新发布的技术报告，V3/R1突破性的训练成本控制</font>**<font style="color:#ED740C;">主要依托FP8精度训练方案</font>**<font style="color:rgba(0, 0, 0, 0.9);">。FP8是一种典型的模型量化技术，相较于业界常用的BF16精度，FP8精度通过将数据位宽减半显著降低了单次计算开销，但也会带来一定的精度损失。在实践中，DeepSeek R1采用了混合精度训练机制有效缓解了精度损失问题。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337466071-41be5e80-9280-4745-ae0c-a953d0b59699.png)

<font style="color:rgba(0, 0, 0, 0.9);">由于DeepSeek R1采用FP8精度训练，所以开源的原生权重就是FP8精度。在推理时，为了尽可能地降低模型精度损失，同时保持和FP8类似的推理吞吐，我们自然想到使用和FP8精度等位宽的INT8精度进行平替。同时，INT8精度被广泛硬件原生支持，基于INT8精度可以极大拓展DeepSeek模型的硬件部署范围。因此，我们开始探索INT8量化在DeepSeek R1上的可行性。</font>

:::color5
**<font style="color:#601BDE;">2.量化基本原理</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">模型量化是将</font>**<font style="color:#ED740C;">模型的权重和激活值</font>**<font style="color:rgba(0, 0, 0, 0.9);">等数据从高精度（</font><font style="color:rgb(136, 136, 136);">如BF16</font><font style="color:rgba(0, 0, 0, 0.9);">）转化为低精度（</font><font style="color:rgb(136, 136, 136);">如INT8</font><font style="color:rgba(0, 0, 0, 0.9);">），并尽可能保证转化前后模型效果一致的过程。以常见的INT8对称量化为例，量化过程如下所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337390429-4b8650fb-fb0f-492e-bd25-81ff88796695.png)

**<font style="color:rgba(0, 0, 0, 0.9);">1.计算缩放因子 x</font>**<sub>**<font style="color:rgba(0, 0, 0, 0.9);">scale</font>**</sub>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337407391-bf3653a0-7a14-47b6-a9b5-0f1cbebce50e.png)

**<font style="color:rgba(0, 0, 0, 0.9);">2.在适当位置做量化（Quant）和反量化（Dequant）</font>**

<font style="color:rgba(0, 0, 0, 0.9);">量化公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337424665-b2b3c903-2f7d-44f6-ab4d-68a75f7e7f68.png)

<font style="color:rgba(0, 0, 0, 0.9);">反量化公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337432779-1e890c7c-025f-4300-b770-2cb18f7834c3.png)

**<font style="color:rgba(0, 0, 0, 0.9);">3.FP16计算可以转为INT8计算</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337447498-535dedfa-e348-4c4e-8686-2ce5ecac4630.png)

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">量化方案设计</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">我们在综合考虑量化后模型的精度和推理性能后，选择了分块量化（</font><font style="color:rgb(136, 136, 136);">Block-wise Quantization</font><font style="color:rgba(0, 0, 0, 0.9);">）和通道量化（</font><font style="color:rgb(136, 136, 136);">Channel-wise Quantization</font><font style="color:rgba(0, 0, 0, 0.9);">）两种方案。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337805945-8f9f5eb3-2787-46fd-a757-82b553e87c56.png)

1. **分块量化**

**<font style="color:rgba(0, 0, 0, 0.9);">优点：</font>**<font style="color:rgba(0, 0, 0, 0.9);">分块量化是DeepSeek V3/R1降低量化损失的关键技术之一。分块量化通过对权重矩阵的细粒度切分，将量化操作的范围控制在[128, 128]的矩阵内，</font>**<font style="color:#DF2A3F;">减少了分布分散的出现概率，从而很好地控制了每次量化过程中的损失。</font>**

**<font style="color:rgba(0, 0, 0, 0.9);">步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">为了尽可能地减少量化后模型的精度损失，我们延续了DeepSeek训练的量化策略。在实践中，由于DeepSeek官方并没有提供半精度浮点型（</font><font style="color:rgb(136, 136, 136);">BF16</font><font style="color:rgba(0, 0, 0, 0.9);">）的权重，因此首先需要将原生的FP8模型权重反量化成BF16，再分块量化成INT8精度。为了匹配权重的分块量化，激活值采用在线逐token-group的量化方式，</font>**<font style="color:#DF2A3F;">即每个token的嵌入向量分为多个组，逐组进行量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

2. **<font style="color:rgba(0, 0, 0, 0.9);">通道量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>

**<font style="color:rgba(0, 0, 0, 0.9);">优点</font>**<font style="color:rgba(0, 0, 0, 0.9);">：除了上述的分块量化外，我们还探索了更高效的通道量化，</font>**<font style="color:#ED740C;">即权重的每列为一组进行量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">。通道量化在执行完INT8的矩阵乘法后，只需进行一次反量化计算，</font>**<font style="color:#ED740C;">计算开销相比分块量化更低</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">缺点</font>**<font style="color:rgba(0, 0, 0, 0.9);">：由于通道量化在量化一列元素时，更容易遇到离群值（</font><font style="color:rgb(136, 136, 136);">Outlier</font><font style="color:rgba(0, 0, 0, 0.9);">），因此相比分块量化会有更多的精度损失。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">在具体实践中，同样地先将原生FP8的模型权重反量化成BF16，之后逐通道量化成INT8类型。同时，对激活值采用在线逐token量化，最大程度地减少activation的量化损失。</font>

:::color5
**<font style="color:#601BDE;">4.量化效果评估</font>**

:::

1. **精度**

<font style="color:rgba(0, 0, 0, 0.9);">我们分别应用上述两种量化方法，对开源的DeepSeek R1模型进行了INT8量化处理，并在GSM8K和MMLU两个数据集上对量化后的模型进行了精度评估。评估结果如下表所示，相比基线的BF16和FP8模型，两种INT8量化模型的精度基本无损。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741338057133-6ee0243a-711d-418e-b78c-324854de2376.png)

2. **<font style="color:rgba(0, 0, 0, 0.9);">推理速度</font>**

<font style="color:rgba(0, 0, 0, 0.9);">我们在知名开源推理框架SGLang上，对上述两种INT8量化方法进行了推理支持（</font><font style="color:rgba(0, 0, 0, 0.9);">分块量化</font><font style="color:rgba(0, 0, 0, 0.9);">、</font><font style="color:rgba(0, 0, 0, 0.9);">通道量化</font><font style="color:rgba(0, 0, 0, 0.9);">）。SGLang是当前SOTA的开源LLM推理框架，在DeepSeek系列模型上有着最优的推理性能，被业界广泛使用。</font>

<font style="color:rgba(0, 0, 0, 0.9);">以BF16模型为Baseline，我们在A100-80G GPU上对两种INT8模型进行了推理吞吐评估。得益于更低的显存要求，INT8量化模型仅需要16张A100 GPU即可推理，但是BF16模型需要32张A100 GPU。为了比较的公平性，我们统一在32张A100 GPU上进行吞吐测试。结果如下表所示，分块量化的INT8推理相比BF16可以提升33%的吞吐；通道量化的INT8推理得益于更低的反量化开销，可以进一步达到50%的吞吐提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741338086042-9b85a191-e2c6-4e85-b0ab-2b4a9242e84f.png)



## Baichuan系列
### <font style="color:rgb(25, 27, 31);">Baichuan2</font><font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Baichuan 2有两个版本的型号，Baichuan 2-7B 70亿参数和Baichuan 2 - 13B拥有130亿个参数。 两个都模型接受了 2.6 万亿个token的训练，其中，迄今为止最大的预训练数据量，是baichuan 1的两倍。有了如此海量的训练数据，Baichuan 2较之取得显着提升。在 </font>[<font style="color:rgb(9, 64, 142);">MMLU</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=MMLU&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 等通用基准CMMLU和 C-Eval中Baichuan 2 - 7B 性能较Baichuan 1提高近 30%。 </font>

**paper：**[**https://arxiv.org/pdf/2309.10305**](https://arxiv.org/pdf/2309.10305)

**参考：**[**https://zhuanlan.zhihu.com/p/655576902**](https://zhuanlan.zhihu.com/p/655576902)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611200835-12036f60-af8d-4f81-887f-621be2d1b98e.png)

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. **预训练数据**

**<font style="color:rgb(25, 27, 31);">数据来源：</font>**<font style="color:rgb(25, 27, 31);">在数据获取过程中，目标是在数据规模和代表性方面追求全面的数据多样性。百川智能从各种来源收集数据，包括通用互联网网页、书籍、研究论文、代码库等，以构建一个广泛的世界知识体系。</font>

<font style="color:rgb(25, 27, 31);">Baichuan 2训练数据中不同类别的分布情况如下：</font>

1. <font style="color:rgb(25, 27, 31);">Web pages: 40%</font>
2. <font style="color:rgb(25, 27, 31);">Books: 30%</font>
3. <font style="color:rgb(25, 27, 31);">Research papers: 20%</font>
4. <font style="color:rgb(25, 27, 31);">Codebases: 5%</font>
5. <font style="color:rgb(25, 27, 31);">Other resources (e.g., news articles, blogs): 5%</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

**<font style="color:rgb(25, 27, 31);">数据处理：</font>**<font style="color:rgb(25, 27, 31);">对于数据处理，关注的是数据频率和质量。数据频率依赖于聚类和去重。百川智能建立了一个支持LSH(Locality Sensitive Hashing)特征和密集嵌入特征的大规模去重和聚类系统。这个系统可以在数小时内对数十亿甚至万亿级别的数据进行去重和聚类。基于聚类，单个文档、段落和句子被去重并打分。这些分数随后用于预训练阶段的数据采样。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::success
**训练数据分布**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611234348-b6ee7299-d2a2-402a-a280-b6eea411f891.png)

:::

:::success
**数据处理pipeline**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610381101-c0c1eb4d-2c58-42e4-9cef-9dd787b665c6.png)

:::

:::success
**Scaling Law**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611307517-a53d102b-24ad-4a6a-a757-8eeec495aad1.png)

:::



:::color5
**<font style="color:#601BDE;">2.模型结构</font>**

:::

1. **位置编码**
    - <font style="color:rgb(25, 27, 31);">Baichuan 1，Baichuan 2-7B：Rotary Positional Embedding(</font>[<font style="color:rgb(9, 64, 142);">RoPE</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=RoPE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)</font>
    - <font style="color:rgb(25, 27, 31);">Baichuan 2-13B：</font>[<font style="color:rgb(9, 64, 142);">ALiBi</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=ALiBi&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:#74B602;">ALiBi是一种更新的位置编码技术</font>**<font style="color:rgb(25, 27, 31);">，已显示出更好的外推性能。然而，大多数开源模型都使用RoPE作为位置嵌入，并且优化的注意力实现如Flash Attention目前更适合RoPE，因为它是基于乘法的，无需通过传递注意力掩码来实现注意力操作。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610679237-00726231-735d-4925-94ed-b462887642ae.png)

2. **激活函数**

<font style="color:rgb(25, 27, 31);">使用SwiGLU激活函数，这是一种开关触发的GLU变体，表现有所改善。然而，SwiGLU具有一个“双线性层”，包含三个参数矩阵，与原始Transformer的前馈层不同，后者只有两个矩阵，因此将隐藏大小从4倍隐藏大小降低到8倍隐藏大小并四舍五入为128的整数倍。对于Baichuan 2的注意力层，采用</font>[<font style="color:rgb(9, 64, 142);">xFormers</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=xFormers&zhida_source=entity)<font style="color:rgb(25, 27, 31);">2实现的内存高效注意力。通过利用xFormers的优化注意力及其偏置能力，可以有效地整合ALiBi的基于偏差的位置编码，同时减少内存开销。这为Baichuan 2的大规模训练提供了性能和效率优势。</font>

3. **<font style="color:rgb(25, 27, 31);">Normalization	</font>**

<font style="color:rgb(25, 27, 31);">对Transformer块的输入应用Layer Normalization。此外，使用RMSNorm实现，它只计算输入特征的方差以提高效率。</font>

:::color5
**<font style="color:#601BDE;">3.训练方法</font>**

:::

1. **优化器：AdamW**

<font style="color:rgb(25, 27, 31);">使用</font>[<font style="color:rgb(9, 64, 142);">AdamW</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=AdamW&zhida_source=entity)<font style="color:rgb(25, 27, 31);">进行训练。β1和β2分别设置为0.9和0.95。使用权重衰减，值为0.1，并修剪梯度范数至0.5。模型在达到最大学习率之前先用2000个线性缩放步骤进行预热，然后应用余弦退火到最小学习率。</font>

2. **精度**

<font style="color:rgb(25, 27, 31);">整个模型使用</font>[<font style="color:rgb(9, 64, 142);">BFloat16</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=BFloat16&zhida_source=entity)<font style="color:rgb(25, 27, 31);">混合精度进行训练。与Float16相比，BFloat16具有更好的动态范围，使其在训练大型语言模型时更能抵抗关键的大值问题。然而，BFloat16的低精度会导致某些设置出现问题。例如，在一些公开的RoPE和ALiBi实现中，</font>[torch.arange](https://link.zhihu.com/?target=https%3A//www.baichuan-ai.com/torch.arange)<font style="color:rgb(25, 27, 31);">操作由于整数超过256而发生冲突，导致附近位置的微分变得困难。因此，在某些敏感操作，如位置嵌入，使用全精度。</font>

3. **RLHF**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610474225-23a6fd76-e817-477d-b573-1e1ca994facd.png)

+ **奖励模型**

<font style="color:rgb(25, 27, 31);">所有prompt设计了一个三层分类系统，由6个主要类别、30个次要类别和超过200个三级类别组成。从用户的角度来看，目标是这个分类系统能全面覆盖所有类型的用户需求。从奖励模型训练的角度来看，每个类别的提示应该具有足够的多样性，以确保奖励模型能够很好地泛化。</font>

<font style="color:rgb(25, 27, 31);">给定一个提示，通过不同大小和阶段的Baichuan 2模型(SFT、</font>[<font style="color:rgb(9, 64, 142);">PPO</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=PPO&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)生成响应以增强响应多样性。只有来自Baichuan 2模型副本用于Reward Model训练。其他开源数据集和专有模型生成的响应不会提高奖励模型的准确性。这也从另一个角度强调了Baichuan模型系列的内在一致性。</font>

<font style="color:rgb(25, 27, 31);">用于训练奖励模型的损失函数与InstructGPT中使用的损失函数相同。从训练中得出的奖励模型表现与LLaMA 2相当，表明两个响应之间的评分差异越大，奖励模型的判别准确度越高，</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610963119-68221fc4-03e2-424f-8da1-a070d79f8a85.png)

+ **PPO**

<font style="color:rgb(25, 27, 31);">在获得奖励模型后，使用PPO算法来训练我们的语言模型。我们使用四个模型：actor模型(负责生成响应)、参考模型(用于计算与固定参数相关的KL惩罚)、奖励模型(提供整个响应的总体奖励，参数固定)和critic模型(旨在学习每个token的价值分数)。</font>

:::color5
**<font style="color:#601BDE;">4.评估</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610292214-a34e1d0d-5b45-4b2f-b9b7-337b427af476.png)

## Qwen系列
### Qwen 3.5
:::color3
**简介：**通义千问 Qwen 团队正式发布 Qwen3.5 系列，并开源其首款原生视觉-语言模型 Qwen3.5-397B-A17B，该模型以创新的稀疏混合专家架构，在显著降低推理成本的同时，实现了与万亿级模型相媲美的性能。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475377772-bd15982c-9e55-42b3-98be-60d6193849e1.png)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475483674-58744dae-8572-44ba-9961-53b7e0abb4dc.png)

:::color5
**<font style="color:#601bde;">1. 模型发布概览</font>**

:::

通义千问 Qwen 团队于除夕夜发布了 Qwen3.5 系列，并同步开源其首款权重模型 **Qwen3.5-397B-A17B**

Qwen3.5-397B-A17B 是一款原生视觉-语言模型（Native Multimodality）。该模型在保持 3970 亿总参数规模的同时，通过创新的架构设计将单次激活参数量控制在 170 亿。这一设计使得开发者能够以更低的推理成本，获得比肩甚至超越万亿级（1T+）模型的性能体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475546807-26c686ce-6e35-4aa3-8e91-8170c6341971.png)

:::color5
**<font style="color:#601bde;">2. 模型资源</font>**

:::

+ **Github**：[https://github.com/QwenLM/Qwen3.5](https://github.com/QwenLM/Qwen3.5)
+ **ModelScope**：[https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B](https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B)
+ **Blog**：[https://qwen.ai/blog?id=qwen3.5](https://qwen.ai/blog?id=qwen3.5)
+ **Qwenchat 体验**：[https://chat.qwen.ai/](https://chat.qwen.ai/)

#### 模型核心亮点
:::color3
**简介：**Qwen3.5-397B-A17B 模型以其卓越的效能比为核心优势，通过进化的稀疏混合专家架构、原生多模态设计及广泛的多语言支持，实现了以 17B 激活参数挑战万亿级模型性能的突破。

:::

:::color5
**<font style="color:#601bde;">1. 极致的效能比</font>**

:::

对于开发者而言，Qwen3.5-397B-A17B 最显著的优势在于其极致的效能比，实现了 **“以 17B 的激活量，挑战 1T 的极限”**。

:::color5
**<font style="color:#601bde;">2. 稀疏混合专家架构（MoE）的进化</font>**

:::

模型总参数量为 397B，但在前向传播过程中仅激活 17B 参数。这种超高稀疏度设计在显存占用与计算延迟之间取得了精妙的平衡。

:::color5
**<font style="color:#601bde;">3. 性能跨代持平</font>**

:::

在预训练阶段，Qwen3.5-397B-A17B 在中英文、多语言、STEM 及逻辑推理等全维度基准测试中，其表现与参数量超过 1T 的 Qwen3-Max-Base 模型旗鼓相当。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475431800-5ad99c07-b414-481a-bb67-36b37e3c3d02.png)

:::color5
**<font style="color:#601bde;">4. 多模态原生化</font>**

:::

与传统的“外挂式”视觉模块不同，Qwen3.5 实现了早期的文本-视觉深度融合，使其在视觉理解与视频处理能力上全面超越了同等规模的 Qwen3-VL 模型。

:::color5
**<font style="color:#601bde;">5. 多语言支持扩展</font>**

:::

模型支持的语言与方言数量从 119 种大幅增加至 201 种。同时，词表规模从 15 万扩展至 25 万，使得在大多数语言上的编解码效率提升了 10%–60%，显著优化了多语言场景下的推理速度。

#### 模型效果实例
:::color3
**简介：**具备 Agent 能力的 Qwen3.5 能够结合多模态能力，实现边思考、边搜索、边调用工具的复杂任务流，展现出在代码、视觉及空间智能等领域的强大应用潜力。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475073342-98324eee-c80a-45d2-83de-662fde214a9f.png)

:::color5
**<font style="color:#601bde;">1. 代码及智能体能力</font>**

:::

**网页开发：**Qwen3.5 能够有效协助进行网页开发，尤其在构建网页和设计用户界面等前端任务中表现出色。它能将简单的自然语言指令转化为可直接运行的代码，从而提升网站创建的效率。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475097933-97348c46-9f30-4fef-bee3-ccc6af51308f.png)

**OpenClaw 集成：**Qwen3.5 可与 OpenClaw 环境集成以驱动编程任务。通过将 OpenClaw 作为第三方智能体环境，Qwen3.5 能够执行网页搜索、信息收集和结构化报告生成等任务。它结合自身的推理能力与工具调用能力，以及 OpenClaw 提供的接口，为用户带来流畅的编码和研究体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475109465-2f21be0c-e7ca-4107-ae85-ca5e3022ca58.png)

以下为输出的 PDF 预览：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475135780-4024f2e8-2d25-426d-b205-44c119adae11.png)  
输出pdf预览 ⬇️

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475155078-053cbb66-adbd-45be-84cf-e3414e45dfba.png)

完整的 PDF 文档示例，请参阅官方博客：[https://qwen.ai/blog?id=qwen3.5#openclaw](https://qwen.ai/blog?id=qwen3.5#openclaw)

:::color5
**<font style="color:#601bde;">2. 视觉智能体能力</font>**

:::

**GUI 智能体**

Qwen3.5 可作为视觉智能体，自主操作手机与电脑以完成日常任务。

+ **移动端**：已适配更多主流应用，支持通过自然语言指令驱动操作。
+ **PC 端**：能够处理跨应用的数据整理、多步骤流程自动化等复杂任务，有效减少重复性人工干预，提升工作效率。

以下为任务示例：

```python
prompt：Fill the missing rows and columns which show the total value
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475169147-b8a3a98b-0bf3-4416-9563-d0bcd2b43b39.png)

**视觉编程：**Qwen3.5 能够将手绘的界面草图转化为结构清晰的前端代码，对简单游戏视频进行逻辑还原，或将长视频内容自动提炼为结构化的网页或可视化图表，从而降低从创意到实现的门槛。

以下为任务示例：

+ input：

```python
prompt：复刻这个小游戏的 HTML 代码
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475197035-47906104-a133-4311-8f8b-6d4450f6378b.png)

+ output：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475210384-1ef31d53-8e21-4b19-a696-fc8174a471b5.png)

:::color5
**<font style="color:#601bde;">3. 空间智能</font>**

:::

通过对图像像素级位置信息进行建模，Qwen3.5 在物体计数、相对位置判断、空间关系描述等任务中表现出更高的准确性。它能有效缓解因视角变化或物体遮挡导致的误判，在自动驾驶场景理解、机器人导航等具身智能应用中展现出良好的空间感知潜力。

以下为任务示例：

+ input：

```python
prompt：我的车在什么时候并线的，又在什么时候开始右转的
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475223309-d70fcac2-4f89-4d8b-8a7f-547f0ca302c1.png)

+ output：

```python
<think>用户希望知道两个具体的时间点：并线（变道）的时间：车辆从当前车道移动到右侧车道（或出口匝道）的时间。开始右转的时间：车辆开始进行明显的右转动作的时间。分析视频：00:00 - 00:05: 车辆在高速公路上行驶，前方有一辆卡车。路面湿滑，有雾。车辆保持在当前车道（看起来是右侧车道，或者正在接近出口）。00:05 - 00:06: 车辆开始向右移动。可以看到车道线（虚线）在车辆左侧，车辆正在跨越这条线进入右侧的出口匝道区域。这是一个并线动作。00:06 - 00:08: 车辆完全进入了右侧的匝道/出口车道。此时车辆基本直行，沿着匝道走。00:08 - 00:09: 车辆继续沿着匝道行驶，前方有红白相间的警示牌。00:09 - 00:10: 车辆开始明显向右转弯。之前的行驶方向比较直，现在车头明显指向右侧的停车场/休息区入口。00:10 - 00:13: 车辆正在转弯进入休息区。可以看到蓝色的停车标志（P）。00:13 - 00:19: 车辆已经在休息区内行驶，寻找停车位。确定时间点：并线 (Lane Change):在 00:05 左右，车辆开始向右偏离主路，跨越虚线。到 00:06 时，车辆已经明显进入了右侧的出口车道。所以并线发生在 00:05 - 00:06 之间。开始右转 (Start Turning Right):在 00:08 之前，车辆主要是在沿着出口匝道直行。在 00:08 - 00:09 之间，车辆经过了红白警示牌，开始向右打方向进入休息区内部道路。最明显的右转动作开始于 00:09，此时车头明显向右偏转，进入有蓝色指示牌的区域。所以开始右转发生在 00:09 左右。综合结论：并线：约 00:05右转：约 00:09再仔细看一下并线。 00:00-00:04 车在行车道。 00:05 车开始向右靠，压过虚线。这是并线出主路。 00:06-00:08 车在减速车道/匝道上直行。 00:09 车头明显向右转，进入服务区/停车场。所以： 并线时间：00:05 右转时间：00:09让我们再精确一点。 00:05 时，车辆开始向右移动，跨越车道线。 00:09 时，车辆经过路口，明显向右转弯进入停车场区域。最终回答构建： 并线发生在 00:05。 右转发生在 00:09。</think>根据视频画面分析：并线时间：您的车在 00:05 开始向右并线，驶离主路进入出口匝道。此时可以看到车辆跨越了白色的虚线车道分隔线。开始右转时间：您的车在 00:09 开始明显右转。此时车辆已经通过了红白相间的警示牌，车头向右偏转，准备进入右侧的停车/休息区域（可以看到蓝色的“P”字指示牌）。
```



根据视频画面分析：

+ **并线时间**：您的车在 **00:05** 开始向右并线，驶离主路进入出口匝道。此时可以看到车辆跨越了白色的虚线车道分隔线。
+ **开始右转时间**：您的车在 **00:09** 开始明显右转。此时车辆已经通过了红白相间的警示牌，车头向右偏转，准备进入右侧的停车/休息区域（可以看到蓝色的“P”字指示牌）。

更多带图推理、视觉推理示例详见官方博客 Demo：  
[https://qwen.ai/blog?id=qwen3.5#demo](https://qwen.ai/blog?id=qwen3.5#demo)

#### 技术路线
:::color3
**简介：**Qwen3.5 的技术路线核心在于架构创新、高效预训练与强化学习扩展，通过 Gated DeltaNet 与 MoE 的融合，以及对能力、效率和通用性的三维优化，实现了模型性能与成本的平衡。

:::

:::color5
**<font style="color:#601bde;">1. 架构创新：Gated DeltaNet 与 MoE 的融合</font>**

:::

模型基于 Qwen3-Next 架构，创新性地将线性注意力机制与稀疏混合专家架构（MoE）相结合。

+ **混合注意力机制**：引入 Gated DeltaNet + Gated Attention，在提升模型长文本建模能力的同时，优化了计算稳定性。
+ **高稀疏度 MoE**：通过提高专家网络的稀疏度，在保证性能的前提下大幅降低了计算冗余。

这种混合架构设计，是其在 BFCL-V4、VITA-Bench、DeepPlanning 等全方位基准评测中表现优异的底层逻辑。

:::color5
**<font style="color:#601bde;">2. 预训练：三维度推进</font>**

:::

Qwen 团队从能力、效率与通用性三个维度对预训练流程进行了重构：

+ **能力**：在更大规模的视觉-文本语料上进行训练，并加强了中英文、多语言、STEM 与推理数据的质量。通过更严格的数据过滤，实现了 Qwen3.5-397B-A17B 与参数量超过 1T 的 Qwen3-Max-Base 性能相当的跨代持平效果。
+ **效率**：基于 Qwen3-Next 架构，采用了更高稀疏度的 MoE、Gated DeltaNet + Gated Attention 混合注意力、稳定性优化以及多 token 预测技术。
    - 在 32k/256k 上下文长度下，Qwen3.5-397B-A17B 的解码吞吐量分别是 Qwen3-Max 的 8.6 倍和 19.0 倍，且性能相当。
    - Qwen3.5-397B-A17B 的解码吞吐量分别是 Qwen3-235B-A22B 的 3.5 倍和 7.2 倍。
+ **通用性**：通过早期的文本-视觉融合与扩展的视觉/STEM/视频数据，实现了原生多模态能力，在相近规模下优于 Qwen3-VL。
    - 多语言覆盖从 119 种增至 201 种语言/方言。
    - 词表从 15 万扩展至 25 万，为多数语言带来了约 10%–60% 的编码/解码效率提升。

:::color5
**<font style="color:#601bde;">3. 后训练：强化学习的 Scaling Law</font>**

:::

根据官方博客，与 Qwen3 系列相比，Qwen3.5 的后训练（Post-training）性能提升主要归功于对强化学习（RL）任务和环境的全面扩展。团队不再局限于针对特定指标或狭窄类别的查询进行优化，而是更加强调 RL 环境的难度与可泛化性。

实验证明，随着 RL 环境的扩展（Scaling），模型在通用 Agent 能力上获得了显著增益。这种“授人以渔”的训练策略，使得模型在 Tool-Decathlon、MCP-Mark 等工具调用与规划任务上表现突出。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475246633-a6db853d-4101-4abb-9871-85b4d891f92e.png)

#### 基础设施
:::color3
**简介：**为支撑复杂的原生多模态模型训练，Qwen 团队通过异构并行、计算重叠及异步强化学习框架等全栈基础设施优化，实现了近 100% 的硬件利用率和 3-5 倍的端到端训练速度提升。

:::

:::color5
**<font style="color:#601bde;">1. 异构并行与计算重叠</font>**

:::

原生多模态训练的主要挑战在于视觉与语言组件计算模式的差异。Qwen3.5 采用了解耦的并行策略，在处理混合的文本、图像、视频数据时，利用稀疏激活技术实现了跨模块的计算重叠。这项优化使得多模态训练的吞吐量几乎等同于纯文本基线，达到了接近 100% 的硬件利用率。

:::color5
**<font style="color:#601bde;">2. 异步强化学习框架</font>**

:::

针对大尺寸模型的强化学习（RL）训练，团队构建了一套可扩展的异步框架：

+ **训推分离架构**：通过解耦设计，支持百万级规模的 Agent 环境交互，显著提升了硬件利用率。
+ **技术组合**：引入了投机采样（Speculative Sampling）、Rollout 路由回放和多轮 Rollout 锁定技术，将端到端训练速度提升了 3 至 5 倍。

该设计不仅消除了框架层的调度中断，更通过算法与系统的协同设计，有效缓解了 RL 训练中的数据长尾问题，提高了训练曲线的平滑度。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475460924-748b0b0c-54b0-4f4f-ac59-ac051395804d.png)

#### 模型部署实践
:::color3
**简介：**本章节提供了使用 SGLang 和 vLLM 框架部署 Qwen3.5-397B-A17B 模型的详细命令，涵盖标准版、工具调用、多 Token 预测等多种模式，并介绍了通过 ModelScope API 进行调用的方法。

:::

:::color5
**<font style="color:#601bde;">1. SGLang 部署</font>**

:::

部署 Qwen3.5 需要使用 SGLang 开源仓库的主分支。可在全新环境中通过以下命令安装：

```plain
uv pip install 'git+https://github.com/sgl-project/sglang.git#subdirectory=python&egg=sglang[all]'
```

以下命令将在 `http://localhost:8000/v1` 创建 API 端点。

**标准版**  
此命令可使用 8 块 GPU 上的张量并行，创建一个最大上下文长度为 262,144 tokens 的 API 端点。

```plain
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3
```

**工具调用**  
若需支持工具调用功能，可使用以下命令。

```plain
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3 --tool-call-parser qwen3_coder
```

**多 Token 预测（MTP）**  
推荐使用以下命令以启用 MTP 功能。

```plain
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3 --speculative-algo NEXTN --speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4
```

:::color5
**<font style="color:#601bde;">2. vLLM 部署</font>**

:::

部署 Qwen3.5 需要使用 vLLM 开源仓库的主分支。可在全新环境中通过以下命令安装：

```plain
uv pip install vllm --torch-backend=auto --extra-index-url https://wheels.vllm.ai/nightly
```

以下命令将在 `http://localhost:8000/v1` 创建 API 端点。

**标准版本**  
此命令可用于在 8 块 GPU 上使用张量并行（tensor parallel），创建一个最大上下文长度为 262,144 个 token 的 API 端点。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3
```

**工具调用（Tool Call）**  
若需支持工具使用功能，可使用以下命令。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder
```

**多 Token 预测（MTP）**  
推荐使用以下命令以启用 MTP 功能。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":2}'
```

**纯文本模式（Text-Only）**  
此命令会跳过视觉编码器和多模态分析，以释放内存用于额外的 KV 缓存。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --language-model-only
```

:::color5
**<font style="color:#601bde;">3. ModelScope API-Inference</font>**

:::

ModelScope API-Inference 已第一时间接入 Qwen3.5-397B-A17B 的调用服务，并提供免费调用额度供社区体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475314030-f3f097c6-eabd-4bcb-baef-958a8071b35a.png)

以下为调用示例代码：

```python
from openai import OpenAI

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='<MODELSCOPE_TOKEN>', # ModelScope Token
)

response = client.chat.completions.create(
    model='Qwen/Qwen3.5-397B-A17B', # ModelScope Model-Id, required
    messages=[{
        'role': 'user',
        'content': [
            {
                'type': 'text',
                'text': '描述这幅图',
            },
            {
                'type': 'image_url',
                'image_url': {
                    'url': 'https://modelscope.oss-cn-beijing.aliyuncs.com/demo/images/audrey_hepburn.jpg',
                },
            }
        ],
    }],
    stream=True
)

for chunk in response:
    if chunk.choices:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

:::color5
**<font style="color:#601bde;">4. 发布意义总结</font>**

:::

本次 Qwen3.5-397B-A17B 的推出具有以下重要意义：

+ **突破超大规模模型的推理成本难题**：通过 17B 的激活参数实现 1T 级别的性能，证明了架构优化比单纯堆砌参数更具前景，使得中型开发者团队也能在本地或私有云部署顶级性能的多模态模型。
+ **开启原生多模态的普及化**：早期融合的架构使得模型在处理图文混合任务时体验更佳，为构建下一代视觉助手和多模态 Agent 提供了坚实的底层支持。
+ **展现强化学习的工程化典范**：Qwen 团队展示了如何通过构建可扩展的 RL 环境来提升模型的逻辑上限，为社区探索 O1 之外的推理能力提升路径提供了宝贵的实践经验。

### Qwen 3<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近期，Qwen 团队发布了其最新一代大语言模型 </font>[<font style="color:rgb(9, 64, 142);">Qwen3</font>](https://zhida.zhihu.com/search?content_id=257209612&content_type=Article&match_order=1&q=Qwen3&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，引起了业界的广泛关注。除了其在各项基准测试上的出色表现和对多语言、思考模式的创新支持外，其开源的代码实现也为我们提供了一个深入了解其内部结构和设计的绝佳机会。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">本文将基于 </font>[<font style="color:rgb(9, 64, 142);">Hugging Face Transformers</font>](https://zhida.zhihu.com/search?content_id=257209612&content_type=Article&match_order=1&q=Hugging+Face+Transformers&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 库中的 Qwen3 实现代码，对其核心组件进行解析。</font>

:::

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">与主流LLM模型类似，Qwen3 采用了经典的 Decoder-Only Transformer 架构。这意味着模型的核心由多个相同的解码器层（Decoder Layer）堆叠而成，专注于根据前面的序列预测下一个 token。</font>

<font style="color:rgb(25, 27, 31);">Qwen3 Dense的模型结构与Qwen2大体相同，只是在注意力层的加入了对q和k的归一化。而Qwen3 </font>[<font style="color:rgb(9, 64, 142);">MoE模型</font>](https://zhida.zhihu.com/search?content_id=257209612&content_type=Article&match_order=1&q=MoE%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">则是把某些MLP层替换为了MoE层。两个模型的结构图如下：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603340601-372e29b1-7da5-4013-8eaf-2208f40a087b.png)![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603350529-3a59ea6e-ac1d-4d5d-b83c-4a352792f2f8.png)

<font style="color:rgb(25, 27, 31);">Qwen3主要由四个部分组成：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

+ **<font style="color:rgb(25, 27, 31);">embed_tokens：嵌入层</font>**<font style="color:rgb(25, 27, 31);">。这是模型处理输入的第一步。它的核心功能是将输入的离散文本符号（通常是经过 Tokenizer 处理后的 Token ID）转换为连续的、稠密的向量表示（称为嵌入向量或 Embeddings）。</font>
+ **<font style="color:rgb(25, 27, 31);">Decoder layers：多个堆叠的解码器</font>**<font style="color:rgb(25, 27, 31);">。这是模型的核心计算引擎，负责理解输入序列的上下文、提取特征并进行深度信息处理。模型的能力（如理解、推理、生成）主要源于这些层。</font>
+ **<font style="color:rgb(25, 27, 31);">norm：归一化层</font>**<font style="color:rgb(25, 27, 31);">。处理完毕后，对最终的隐藏状态 (Hidden States) 进行最后一次归一化。</font>
+ **<font style="color:rgb(25, 27, 31);">rotary_emb</font>**<font style="color:rgb(25, 27, 31);">：旋转位置编码。为模型提供关于序列中 Token 位置的信息。标准 Transformer 的自注意力机制本身是排列不变的（即打乱输入顺序可能得到相同结果），因此需要显式地注入位置信息。</font>

:::color5
**<font style="color:#601BDE;">2.Qwen3 Decoder</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen3 Decoder的结构与Qwen2 Decoder大致相同。MoE模型实际上是把Dense模型中的某些MLP层替换为了MoE结构。</font>

:::success
**Dense模型**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603061886-fb557479-8818-4398-9236-f223b8391d00.png)

:::

:::success
**MoE模型**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603022441-fc7a4390-9280-4dd8-8082-dcf517013924.png)

:::

<font style="color:rgb(25, 27, 31);">不同规格的模型具有不同数量的Decoder层：</font>

| **Model** | **Layers ** | **Model** | **Layers ** |
| --- | --- | --- | --- |
| Qwen3-0.6B | 28 | Qwen3-14B | 40 |
| Qwen3-1.7B | 28 | Qwen3-32B | 64 |
| Qwen3-4B | 36 | Qwen3-30B | 48 |
| Qwen3-8B | 36 | Qwen3-235B | 94 |


:::color5
**<font style="color:#601BDE;">3.Qwen3 attention</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen3的注意力机制在Qwen2的基础上进行了微调，在Q、K的线性投影后面分别加入了一个</font>**<font style="color:#74B602;">归一化层，有助于提高稳定性。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603330559-81827e0e-c2a6-46e7-b54c-b8874af885d4.png)

:::color5
**<font style="color:#601BDE;">4.Qwen3 MLP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen3的MLP层与Qwen2完全一致。Qwen使用了一种常见的 MLP 变体，称为 SwiGLU ( Gated Linear Unit with SiLU activation)。这种结构被认为比标准的 MLP 更有效。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603425875-aa113947-6a03-40c9-bb1f-8ed32aecc731.png)

:::color5
**<font style="color:#601BDE;">5.Qwen3 MoE</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen3 的MoE是Qwen3在模型结构上最大的更新：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1746603523066-b27a3360-bbde-4c47-9f95-d4d20240abcc.png)

<font style="color:rgb(25, 27, 31);">Qwen3 的 MoE 结构是一种稀疏 MoE 实现。它用一个包含多个（num_experts 个）小型 MLP（Qwen3MoeMLP）专家和一个门控网络（gate）的块（</font>[<font style="color:rgb(9, 64, 142);">Qwen3MoeSparseMoeBlock</font>](https://zhida.zhihu.com/search?content_id=257209612&content_type=Article&match_order=1&q=Qwen3MoeSparseMoeBlock&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）替换了传统Transformer 中的密集 MLP 层。</font>

<font style="color:rgb(25, 27, 31);">门控网络为每个 Token 选择最相关的 top_k 个专家，并将 Token 的计算任务加权分配给这些专家。最后，将加权后的专家输出组合起来形成该层的最终输出。</font>**<font style="color:#74B602;">这种方式允许模型在保持（甚至降低）每个 Token 推理计算量的情况下，显著增加模型的总参数量（通过增加专家数量），从而可能提升模型的容量和性能</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">6.Qwen3 MoE 代码实现</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
class Qwen3MoeSparseMoeBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.num_experts = config.num_experts
        self.top_k = config.num_experts_per_tok
        self.norm_topk_prob = config.norm_topk_prob

        # gating
        self.gate = nn.Linear(config.hidden_size, config.num_experts, bias=False)
        self.experts = nn.ModuleList(
            [Qwen3MoeMLP(config, intermediate_size=config.moe_intermediate_size) for _ in range(self.num_experts)]
        )

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """ """
        batch_size, sequence_length, hidden_dim = hidden_states.shape
        hidden_states = hidden_states.view(-1, hidden_dim)
        # router_logits: (batch * sequence_length, n_experts)
        router_logits = self.gate(hidden_states)

        routing_weights = F.softmax(router_logits, dim=1, dtype=torch.float)
        routing_weights, selected_experts = torch.topk(routing_weights, self.top_k, dim=-1)
        if self.norm_topk_prob:  # only diff with mixtral sparse moe block!
            routing_weights /= routing_weights.sum(dim=-1, keepdim=True)
        # we cast back to the input dtype
        routing_weights = routing_weights.to(hidden_states.dtype)

        final_hidden_states = torch.zeros(
            (batch_size * sequence_length, hidden_dim), dtype=hidden_states.dtype, device=hidden_states.device
        )

        # One hot encode the selected experts to create an expert mask
        # this will be used to easily index which expert is going to be sollicitated
        expert_mask = torch.nn.functional.one_hot(selected_experts, num_classes=self.num_experts).permute(2, 1, 0)

        # Loop over all available experts in the model and perform the computation on each expert
        for expert_idx in range(self.num_experts):
            expert_layer = self.experts[expert_idx]
            idx, top_x = torch.where(expert_mask[expert_idx])

            # Index the correct hidden states and compute the expert hidden state for
            # the current expert. We need to make sure to multiply the output hidden
            # states by `routing_weights` on the corresponding tokens (top-1 and top-2)
            current_state = hidden_states[None, top_x].reshape(-1, hidden_dim)
            current_hidden_states = expert_layer(current_state) * routing_weights[top_x, idx, None]

            # However `index_add_` only support torch tensors for indexing so we'll use
            # the `top_x` tensor here.
            final_hidden_states.index_add_(0, top_x, current_hidden_states.to(hidden_states.dtype))
        final_hidden_states = final_hidden_states.reshape(batch_size, sequence_length, hidden_dim)
        return final_hidden_states, router_logits
```



### Qwen omni
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">Qwen最近几天刚强度的发布新品，这就两天，一个Qwen2.5-VL-32B，一个Qwen2.5-Omni-7B。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Qwen-2.5-Omni是一个</font>**<font style="color:#74B602;">全模态模型</font>**<font style="color:rgb(25, 27, 31);">，Omni来自拉丁语单词“Omnis”，意为“全部”、“一切”或“全方位”，ChatGPT也有过类似的后缀。Qwen-2.5-Omni可以处理文字、图像、音频和视频，同时输出文字和音频。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/QwenLM/Qwen2.5-Omni/](https://github.com/QwenLM/Qwen2.5-Omni/)

**paper：**[**https://github.com/QwenLM/Qwen2.5-Omni/blob/main/assets/Qwen2.5_Omni.pdf**](https://github.com/QwenLM/Qwen2.5-Omni/blob/main/assets/Qwen2.5_Omni.pdf)

**参考：**[**https://zhuanlan.zhihu.com/p/1888487511908663591**](https://zhuanlan.zhihu.com/p/1888487511908663591)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743045000915-51afedca-732e-419e-9035-34ebc89e672a.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743044906580-e4d019d5-4dbe-4223-af83-c5d88afcbefa.png)

1. **<font style="color:rgb(25, 27, 31);">创新架构</font>**

<font style="color:rgb(25, 27, 31);">提出了一种名为「Thinker-Talker」</font>**<font style="color:rgb(25, 27, 31);">的全新多模态架构，可以同时理解和处理文字、图片、音频和视频等多种类型的信息。同时，它还能以文字和自然的语音形式实时地给出回答。此外，我们设计了一种创新的位置编码技术，称为</font>**<font style="color:rgb(25, 27, 31);">「TMRoPE」（时间对齐的多模态旋转位置编码），能有效将视频与音频的信息在时间轴上精确同步。</font>

**<font style="color:rgb(25, 27, 31);">2 实时语音与视频交流</font>**

<font style="color:rgb(25, 27, 31);">Thinker-Talker架构专为实时互动设计，能够边输入边输出，实现真正意义上的即时语音和视频沟通。</font>

**<font style="color:rgb(25, 27, 31);">3 自然且稳定的语音生成效果</font>**

<font style="color:rgb(25, 27, 31);">该模型在生成语音时，不仅比目前市场上的大多数实时和非实时系统效果更自然，而且稳定性更强，听起来更像真实人类的对话。</font>

**<font style="color:rgb(25, 27, 31);">4 各种类型信息都表现出色</font>**

<font style="color:rgb(25, 27, 31);">无论处理哪种类型的数据（文字、图像、音频或视频），该模型的表现都非常突出。比如，在音频处理上，</font>**<font style="color:rgb(25, 27, 31);">Qwen2.5-Omni</font>**<font style="color:rgb(25, 27, 31);">的表现超过了相同规模的音频专用模型（如Qwen2-Audio），并且在图文处理方面与视觉语言模型Qwen2.5-VL-7B的效果也不相上下。</font>

**<font style="color:rgb(25, 27, 31);">5 优秀的语音指令执行能力</font>**

<font style="color:rgb(25, 27, 31);">在处理语音指令任务时，Qwen2.5-Omni的能力也相当于处理文字指令一样出色，这一点通过多个标准化测试（如MMLU和GSM8K等）得到了验证。</font>



### <font style="color:rgb(0, 0, 0);">Qwen QWQ</font>
**<font style="color:rgba(0, 0, 0, 0.9);">官方报道</font>**<font style="color:rgba(0, 0, 0, 0.9);">：QwQ-32B = Qwen2.5-Plus + Thinking ≈ 满血版DeepSeek-R1</font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">QwQ，全称Qwen-with-Questions，最早由阿里于2024年11月推出，作为一款开源推理模型，旨在与OpenAI的o1-preview竞争。在发布时，该模型旨在通过在</font>**<font style="color:#ED740C;">推理过程中审查和优化自身回答来增强逻辑推理和规划能力</font>**<font style="color:rgba(0, 0, 0, 0.9);">，这一技术使其在</font>**<font style="color:#ED740C;">数学和编程任务中表现尤为出色</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.多阶段强化学习提升性能</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">传统的指令微调（instruction-tuned）模型在处理复杂推理任务时往往表现欠佳，而Qwen团队的研究表明，RL可以显著提升模型解决复杂问题的能力。</font>

<font style="color:rgba(0, 0, 0, 0.9);">QwQ-32B是阿里的最新版本，在此前研究的基础上融合了</font>**<font style="color:#74B602;">强化学习（RL）和结构化自我提问（structured self-questioning）</font>**<font style="color:rgba(0, 0, 0, 0.9);">，使其在日益增长的推理型AI领域中成为强有力的竞争者。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">QwQ-32B的强化学习训练分为两个阶段：</font>**

1. <font style="color:rgba(0, 0, 0, 0.9);">数学与编程能力增强。该阶段使用</font>**<font style="color:#ED740C;">数学推理精度验证器（accuracy verifier）和代码执行服务器（code execution server）对模型进行训练</font>**<font style="color:rgba(0, 0, 0, 0.9);">，以确保生成的答案在被强化之前已通过正确性验证。</font>
2. <font style="color:rgba(0, 0, 0, 0.9);">通用能力优化。第二阶段采用基于奖励的训练方法，结合</font>**<font style="color:#ED740C;">通用奖励模型（general reward models）和基于规则的验证器（rule-based verifiers）</font>**<font style="color:rgba(0, 0, 0, 0.9);">。这一过程提高了模型的指令遵循能力、人类对齐度（human alignment）以及agent推理能力，同时仍能保持其数学和编程能力的高水平。</font>

:::color5
**<font style="color:#601BDE;">2.模型结构优化</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">QwQ-32B基于因果语言模型（causal language model）架构，并进行了多项优化：</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">64层Transformer结合</font>**<font style="color:#74B602;">RoPE（旋转位置编码）、SwiGLU、RMSNorm和Attention QKV</font>**<font style="color:rgba(0, 0, 0, 0.9);">偏置</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">通用查询注意力（GQA）设有40个查询注意力头，以及8个用于键-值对（key-value）的注意力头</font>
+ **<font style="color:#74B602;">扩展的上下文窗口支持131072个token</font>**<font style="color:rgba(0, 0, 0, 0.9);">，以更好地处理长序列输入；</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">多阶段训练流程包括预训练、监督微调（SFT）和强化学习（RL）。</font>

:::color5
**<font style="color:#601BDE;">3.B端应用</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">对于企业领导者（包括CEO、CTO、IT负责人、团队经理和AI应用开发者）而言，QwQ-32B可能会改变AI在商业决策和技术创新中的应用方式。</font>

<font style="color:rgba(0, 0, 0, 0.9);">凭借其基于RL的推理能力，</font>**<font style="color:#ED740C;">该模型能够提供更加精准、结构化、具备上下文理解能力的洞察，使其在自动化数据分析、战略规划、软件开发和智能自动</font>****<font style="color:rgba(0, 0, 0, 0.9);">化</font>**<font style="color:rgba(0, 0, 0, 0.9);">等场景中具有重要价值。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">企业应用场景</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>

+ **<font style="color:rgba(0, 0, 0, 0.9);">复杂问题求解</font>**
+ **<font style="color:rgba(0, 0, 0, 0.9);">编程辅助</font>**
+ **<font style="color:rgba(0, 0, 0, 0.9);">金融建模</font>**
+ **<font style="color:rgba(0, 0, 0, 0.9);">客户服务自动化</font>**

<font style="color:rgba(0, 0, 0, 0.9);">此外，由于QwQ-32B采用开源权重，企业可以自由微调和定制模型以适配特定行业需求，而无需受限于专有模型（如OpenAI的o1）。</font>

:::color5
**<font style="color:#601BDE;">4.Agentic 能力</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">QwQ-32B集成了Agentic能力，能够根据环境反馈动态调整推理过程。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">推荐的推理参数</font>**

```python
温度（Temperature）：0.6
TopP（核采样）：0.95
TopK（最高概率截取）：20-40
YaRN Scaling（用于长序列处理）：适用于超过 32768 tokens 的输入
```

<font style="color:rgba(0, 0, 0, 0.9);">此外，该模型支持使用vLLM（高吞吐量推理框架）进行部署。但需要注意，当前vLLM的实现仅支持静态YaRN扩展，即无论输入长度如何，扩展比例保持固定。</font>

:::color5
**<font style="color:#601BDE;">5.未来发展方向</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">Qwen团队将QwQ-32B视为</font>**<font style="color:rgba(0, 0, 0, 0.9);">扩展RL以增强推理能力的第一步</font>**<font style="color:rgba(0, 0, 0, 0.9);">。未来计划包括：</font>

1. <font style="color:rgba(0, 0, 0, 0.9);">进一步探索RL的扩展，提升模型的智能水平；</font>
2. **<font style="color:#ED740C;">集成RL与Agent技术</font>**<font style="color:rgba(0, 0, 0, 0.9);">实现更复杂的长时推理（long-horizon reasoning）；</font>
3. <font style="color:rgba(0, 0, 0, 0.9);">持续优化基础模型使其更加适用于强化学习（RL-driven foundation models）；</font>
4. <font style="color:rgba(0, 0, 0, 0.9);">推动通向AGI（通用人工智能），采用更先进的训练技术。</font>

<font style="color:rgba(0, 0, 0, 0.9);">通过QwQ-32B，Qwen团队正在</font>**<font style="color:rgba(0, 0, 0, 0.9);">将强化学习（RL）确立为下一代AI模型的关键驱动力</font>**<font style="color:rgba(0, 0, 0, 0.9);">，展示了在合理扩展规模的同时，依然能够构建出高效且强大的推理系统。</font><font style="color:rgba(0, 0, 0, 0.9);"></font>

:::color5
**<font style="color:#601BDE;">6.效果评测</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">该模型已与DeepSeek-R1、o1-mini和DeepSeek-R1-Distilled-Qwen-32B等领先模型进行基准测试，尽管QwQ-32B的参数量比其中一些模型少，但仍展现出极具竞争力的性能。</font>

<font style="color:rgba(0, 0, 0, 0.9);">尽管DeepSeek-R1拥有6710亿个参数（其中370亿被激活），QwQ-32B在大幅缩小模型规模的情况下实现了相近的性能——运行该模型通常仅需24GB显存（相比之下，Nvidia H100拥有80GB显存），而完整运行DeepSeek-R1则需要超过1500GB显存（16张Nvidia A100 GPU）。这一对比凸显了Qwen团队强化学习（RL）方法的高效性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741332079969-998306ec-355b-4c39-934a-63defa1def53.png)

### Qwen 2.5
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近年来，除了模型能力的飞速发展，LLM 社区还见证了开源（开权重）大型语言模型的爆发性增长，例如 </font>**<font style="color:rgb(25, 27, 31);">Llama </font>**<font style="color:rgb(25, 27, 31);">系列、</font>**<font style="color:rgb(25, 27, 31);">Mistral</font>**<font style="color:rgb(25, 27, 31);"> 系列及千问团队（后面简称“团队”）的 </font>**<font style="color:rgb(25, 27, 31);">Qwen</font>**<font style="color:rgb(25, 27, 31);"> 系列。开源权重的模型使得普通用户和开发者更容易访问大型语言模型，促进了更多的研究参与，推动了社区合作创新，并加速了各领域 AI 应用的进展。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">最近，团队发布了 Qwen 系列的最新版本 </font>**<font style="color:rgb(25, 27, 31);">Qwen2.5</font>**<font style="color:rgb(25, 27, 31);">。在开源部分，他们发布了7种不同规模的预训练和指令微调模型，包括</font>**<font style="color:rgb(25, 27, 31);">0.5B、1.5B、3B、7B、14B、32B</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">72B</font>**<font style="color:rgb(25, 27, 31);">，并提供了原始模型（bfloat16 精度）及不同精度的量化版本。</font>

**paper：**[**https://arxiv.org/pdf/2412.15115**](https://arxiv.org/pdf/2412.15115)

**参考：**[**【LLM技术报告】Qwen2.5技术报告（全文）**](https://zhuanlan.zhihu.com/p/13936916587)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">规模更优</font>**<font style="color:rgb(25, 27, 31);">：相比 Qwen2，Qwen2.5 除了提供0.5B、1.5B、7B和72B模型外，还重新引入了</font>**<font style="color:#74B602;">3B、14B和32B模型，这些模型在资源有限的场景下更具成本效益</font>**<font style="color:rgb(25, 27, 31);">，且当前开源基础模型领域对此类型模型的关注较少。Qwen2.5-Turbo 和 Qwen2.5-Plus 在准确性、延迟和成本之间取得了良好平衡。</font>
2. **<font style="color:rgb(25, 27, 31);">数据更优</font>**<font style="color:rgb(25, 27, 31);">：预训练和后训练数据量有了显著提升。预训练数据量从</font>**<font style="color:#74B602;">7T tokens增加至18T tokens</font>**<font style="color:rgb(25, 27, 31);">，重点涵盖知识、编程和数学。预训练阶段被设计为分阶段过渡，以适应不同数据集的融合。后训练数据量达到</font>**<font style="color:rgb(25, 27, 31);">1M示例</font>**<font style="color:rgb(25, 27, 31);">，涵盖了SFT、</font>**<font style="color:rgb(25, 27, 31);">直接偏好优化（DPO）</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（GRPO）</font>**<font style="color:rgb(25, 27, 31);">等阶段。</font>
3. **<font style="color:rgb(25, 27, 31);">使用体验更优</font>**<font style="color:rgb(25, 27, 31);">：Qwen2 在使用中的关键限制已被克服，包括</font>**<font style="color:#74B602;">生成长度从2K tokens提升至8K tokens</font>**<font style="color:rgb(25, 27, 31);">，更好地支持结构化输入和输出（如表格和JSON），以及更便捷的工具使用。同时，Qwen2.5-Turbo 支持</font>**<font style="color:rgb(25, 27, 31);">最高1M tokens</font>**<font style="color:rgb(25, 27, 31);">的上下文长度。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

1. **PreTrain数据**
    - **<font style="color:rgb(25, 27, 31);">更精细的数据过滤</font>**<font style="color:rgb(25, 27, 31);">：高质量的预训练数据对模型性能至关重要，因此数据质量评估和过滤是流程中的关键环节。团队利用 </font>**<font style="color:#74B602;">Qwen2-Instruct 模型作为数据质量过滤器，进行全面的多维度分析</font>**<font style="color:rgb(25, 27, 31);">，评估和打分训练样本。与 Qwen2 相比，这一方法显著提升了数据质量评估的能力，使得他们能够更好地保留高质量的训练数据，并有效过滤低质量的样本。</font>
    - **<font style="color:rgb(25, 27, 31);">更优的数学与代码数据</font>**<font style="color:rgb(25, 27, 31);">：在 Qwen2.5 的预训练过程中，团队加入了来自</font>**<font style="color:#74B602;"> Qwen2.5-Math 和 Qwen2.5-Coder 的训练数据</font>**<font style="color:rgb(25, 27, 31);">。这种整合策略非常有效，因为这些专业数据集帮助他们在数学推理和代码生成任务上取得了领先的表现。</font>
    - **<font style="color:rgb(25, 27, 31);">更高质量的合成数据</font>**<font style="color:rgb(25, 27, 31);">：为了生成高质量的合成数据，尤其是在数学、编程和知识领域，团队采用了 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-72B-Instruct </font>**<font style="color:rgb(25, 27, 31);">和 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-Math-72B-Instruct</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:#74B602;">通过使用专有奖励模型和 Qwen2-Math-RM-72B 模型进行严格的过滤</font>**<font style="color:rgb(25, 27, 31);">，进一步提高了这些合成数据的质量。</font>
    - **<font style="color:rgb(25, 27, 31);">更合理的数据混合</font>**<font style="color:rgb(25, 27, 31);">：为了优化预训练数据的分布，团队使用 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-Instruct</font>**<font style="color:rgb(25, 27, 31);"> 模型对不同领域的内容进行分类与平衡。分析显示，像电子商务、社交媒体和娱乐等领域在互联网数据中占比过大，常包含重复、模板化或机器生成的内容。相比之下，</font>**<u><font style="color:#74B602;">技术、科学和学术研究等领域虽然包含更高质量的信息，却常常被低估</font></u>**<font style="color:rgb(25, 27, 31);">。通过对过度代表的领域进行下采样，并对高价值领域进行上采样，他们确保了一个更加平衡且信息丰富的训练数据集，更好地服务于模型的学习目标。</font>

<font style="color:rgb(25, 27, 31);">凭借这些技术手段，团队开发了一个更大、更高质量的预训练数据集，将 Qwen2 的 7T tokens 扩展到了 18T tokens。</font>

2. **<font style="color:rgb(25, 27, 31);">PostTrain数据</font>**

<font style="color:rgb(25, 27, 31);">Qwen2.5的监督微调过程采用了一个包含数百万个高质量示例的庞大数据集。此次数据扩展专门解决了Qwen2模型在多个关键领域中的局限性，特别是在</font>**<font style="color:#74B602;">长序列生成、数学问题解决、编码、指令执行、结构化数据理解、逻辑推理、跨语言迁移和系统指令</font>**<font style="color:rgb(25, 27, 31);">的鲁棒性方面。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">对于稠密模型，团队延续了 Qwen2 的</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Transformer 解码器</font>](https://zhida.zhihu.com/search?content_id=251810314&content_type=Article&match_order=1&q=Transformer+%E8%A7%A3%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">架构，并在此基础上进行了优化。该架构包括以下关键组件：</font>

+ **<font style="color:rgb(25, 27, 31);">分组查询注意力（Grouped Query Attention, </font>**[**<font style="color:rgb(9, 64, 142);">GQA</font>**](https://zhida.zhihu.com/search?content_id=251810314&content_type=Article&match_order=1&q=GQA&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">：用于高效地利用 KV 缓存</font>
+ **<font style="color:rgb(25, 27, 31);">SwiGLU 激活函数</font>**<font style="color:rgb(25, 27, 31);">：增强非线性激活</font>
+ **<font style="color:rgb(25, 27, 31);">旋转位置编码（</font>**[**<font style="color:rgb(9, 64, 142);">RoPE</font>**](https://zhida.zhihu.com/search?content_id=251810314&content_type=Article&match_order=1&q=RoPE&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">：用于编码位置信息</font>
+ **<font style="color:rgb(25, 27, 31);">QKV 偏置</font>**<font style="color:rgb(25, 27, 31);">：用于提升注意力机制的表现</font>
+ **<font style="color:rgb(25, 27, 31);">RMSNorm</font>**<font style="color:rgb(25, 27, 31);">：在预归一化后使用，以保证训练过程稳定</font>
+ **<font style="color:rgb(25, 27, 31);">MOE</font>**<font style="color:rgb(25, 27, 31);">：在稠密模型的基础上，团队进一步扩展为 MoE 模型架构。通过将标准的</font>**<font style="color:rgb(25, 27, 31);">前馈网络（FFN）</font>**<font style="color:rgb(25, 27, 31);">层替换为专门的 MoE 层来实现这一点，每个层包含多个 FFN 专家，并通过路由机制将 tokens 分配给 top-K 专家。</font>
+ **<font style="color:rgb(25, 27, 31);">tokenizer</font>**<font style="color:rgb(25, 27, 31);">：团队使用了 Qwen 的 tokenizer，该 tokenizer 实现了字节级别的</font>**<font style="color:rgb(25, 27, 31);">字节对编码（BBPE）</font>**<font style="color:rgb(25, 27, 31);">，并采用了151,643个常规 tokens 的词汇表。与之前版本相比，他们将控制 tokens 的数量从3个扩展到了22个，新增了两个用于工具功能的 tokens，其余则用于支持其他模型能力。</font>**<font style="color:#74B602;">这一扩展确保了所有 Qwen2.5 模型之间的统一词汇表，增强了系统的一致性并减少了潜在的兼容性问题。</font>**

:::color5
**<font style="color:#601BDE;">4.Pre-Train</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">超参数的 Scaling Law</font>**

<font style="color:rgb(25, 27, 31);">团队基于 Qwen2.5 的预训练数据，开发了适用于超参数的 Scaling Law。虽然先前的研究主要使用 Scaling Law 来根据计算预算确定最优模型规模，但他们则利用这些 Scaling Law 来识别不同模型架构下的最优超参数。</font>

<font style="color:rgb(25, 27, 31);">具体来说，团队的 Scaling Law 帮助他们确定密集模型和 MoE 模型（不同规模）中的关键训练参数，如</font>**<font style="color:rgb(25, 27, 31);">批次大小</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">B</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">学习率</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">μ</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">通过广泛的实验，团队系统研究了模型架构与最优训练超参数之间的关系。具体而言，他们分析了</font>**<font style="color:#74B602;">最优学习率 </font>****<font style="color:#74B602;">μ</font>**<sub>**<font style="color:#74B602;">opt</font>**</sub><sub>**<font style="color:#74B602;"> </font>**</sub>**<font style="color:#74B602;">和批次大小 </font>****<font style="color:#74B602;">B</font>**<sub>**<font style="color:#74B602;">opt</font>**</sub>**<font style="color:#74B602;"> 如何随着模型规模 </font>****<font style="color:#74B602;">N</font>****<font style="color:#74B602;"> 和预训练数据量 </font>****<font style="color:#74B602;">D</font>****<font style="color:#74B602;"> 的变化而变化</font>**<font style="color:rgb(25, 27, 31);">。他们的实验涵盖了多个架构，包括从 44M 到 14B 参数的密集模型，以及从 </font>**<font style="color:#74B602;">44M~1B 激活参数的 MoE 模型</font>**<font style="color:rgb(25, 27, 31);">，训练数据集的规模从 0.8B~600B tokens 不等。利用这些最优超参数预测，团队将最终损失率建模为</font>**<font style="color:rgb(25, 27, 31);">模型架构和训练数据规模的函数</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">此外，他们还利用 Scaling Law 来预测并比较不同参数规模的 MoE 模型与其密集模型的性能差异。通过这种分析，团队为 MoE 模型的超参数配置提供了指导，使得经过精细调整激活参数和总参数后，MoE 模型在性能上能够与特定的密集模型变种（例如 Qwen2.5-72B 和 Qwen2.5-14B）达到平衡。</font>

2. **长上下文预训练**

<font style="color:rgb(25, 27, 31);">为了最大化训练效率，Qwen2.5采用了</font>**<font style="color:#74B602;">两阶段的预训练</font>**<font style="color:rgb(25, 27, 31);">方法：</font>

<font style="color:rgb(25, 27, 31);">首先</font>**<font style="color:rgb(25, 27, 31);">使用4K token的上下文长度进行训练</font>**<font style="color:rgb(25, 27, 31);">，接着进入扩展阶段，支持更长的序列。延续Qwen2的策略，在最终的预训练阶段，除Qwen2.5-Turbo外，所有模型变体</font>**<font style="color:rgb(25, 27, 31);">将上下文长度从4K扩展到32K token</font>**<font style="color:rgb(25, 27, 31);">。同时，利用</font>**<font style="color:rgb(25, 27, 31);">ABF技术</font>**<font style="color:rgb(25, 27, 31);">将</font>**<font style="color:rgb(25, 27, 31);">RoPE的基础频率从10,000提升到1,000,000</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">对于Qwen2.5-Turbo模型，团队实施了一个逐</font>**<font style="color:#74B602;">步扩展上下文长度的策略，经过四个阶段：32K token、64K token、128K token，最终达到256K token</font>**<font style="color:rgb(25, 27, 31);">，RoPE的基础频率为10,000,000。在每个阶段，训练数据包含</font>**<font style="color:rgb(25, 27, 31);">40%的当前最大长度序列</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">60%的较短序列</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:#74B602;">这种渐进式的训练方法帮助模型平稳适应逐渐增加的上下文长度，同时保持其处理和泛化不同长度序列的能力。</font>**

<font style="color:rgb(25, 27, 31);">为了提升模型在推理时处理更长序列的能力，团队引入了两项关键技术：</font>**<font style="color:rgb(25, 27, 31);">YARN</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">双块注意力（DCA）</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">通过这些创新，他们使得序列长度的处理能力</font>**<font style="color:rgb(25, 27, 31);">提高了4倍</font>**<font style="color:rgb(25, 27, 31);">，从而使Qwen2.5-Turbo能够处理最多</font>**<font style="color:rgb(25, 27, 31);">1M个token</font>**<font style="color:rgb(25, 27, 31);">，其他模型能够处理最多128K token。值得一提的是，这些技术不仅通过降低困惑度改善长序列的建模效果，同时也确保了模型在</font>**<font style="color:rgb(25, 27, 31);">处理短序列时的优异表现</font>**<font style="color:rgb(25, 27, 31);">，从而保证在不同输入长度下提供一致的高质量输出。</font>

:::color5
**<font style="color:#601BDE;">5.Post-Train</font>**

:::

1. **SFT**

<font style="color:rgb(25, 27, 31);">为了进一步扩展Qwen2.5-Turbo的上下文处理能力，团队在后期训练阶段引入了更长的SFT示例，使得模型能够更好地适应长文本查询中的人类偏好。</font>

<font style="color:rgb(25, 27, 31);">在SFT阶段，团队采用了两阶段微调方法。</font>

    - **<font style="color:rgb(25, 27, 31);">第一阶段</font>**<font style="color:rgb(25, 27, 31);">：模型</font>**<font style="color:rgb(25, 27, 31);">仅使用短指令</font>**<font style="color:rgb(25, 27, 31);">进行微调，每个指令的最大长度为32K token。该阶段使用的数据和训练步骤与其他Qwen2.5模型相同，旨在确保模型在短任务上的强大性能。</font>
    - **<font style="color:rgb(25, 27, 31);">第二阶段</font>**<font style="color:rgb(25, 27, 31);">：微调方法则</font>**<font style="color:rgb(25, 27, 31);">结合了短指令</font>**<font style="color:rgb(25, 27, 31);">（最多32K token）和</font>**<font style="color:rgb(25, 27, 31);">长指令</font>**<font style="color:rgb(25, 27, 31);">（最多256K token）。这种混合微调方法能够有效提升模型在长上下文任务中的指令跟随能力，同时确保它在短任务中的表现不受影响。</font>

**<font style="color:rgb(25, 27, 31);">SFT阶段的关键提升：</font>**

    1. **<font style="color:rgb(25, 27, 31);">长序列生成</font>**<font style="color:rgb(25, 27, 31);">：Qwen2.5具备生成高质量长文本的能力，最大输出上下文长度可达到8K token，这一进步显著超越了传统后训练模型通常保持在2,000个token以内的输出限制。为此，团队开发了长响应数据集，并通过反向翻译技术从预训练语料中生成长文本数据的查询，确保输出长度符合预期，并使用Qwen2过滤低质量的配对数据。</font>
    2. **<font style="color:rgb(25, 27, 31);">数学推理</font>**<font style="color:rgb(25, 27, 31);">：团队引入了Qwen2.5-Math中的</font>**<font style="color:rgb(25, 27, 31);">链式推理（CoT）</font>**<font style="color:rgb(25, 27, 31);">数据，其中包含多个来源的数据集，包括公开数据集、K-12问题集和合成问题。为了确保推理的高质量，团队采用了</font>**<font style="color:rgb(25, 27, 31);">拒绝采样</font>**<font style="color:rgb(25, 27, 31);">，并结合奖励建模和带注解的答案，帮助模型生成逐步推理过程。</font>
    3. **<font style="color:rgb(25, 27, 31);">编程能力</font>**<font style="color:rgb(25, 27, 31);">：为了提升模型的编程能力，团队整合了Qwen2.5-Coder中的指令微调数据。他们将多个特定编程语言的智能体结合在一个协作框架中，生成约40种编程语言的多样化、高质量的指令对，然后进一步扩展了数据集，通过合成来自代码问答网站的示例和从GitHub收集的算法代码片段，增加了编程指令的多样性。并利用多语言沙箱进行静态代码检查，通过自动化单元测试来验证代码的质量与正确性。</font>
    4. **<font style="color:rgb(25, 27, 31);">指令跟随</font>**<font style="color:rgb(25, 27, 31);">：为了确保指令跟随的高质量数据，团队构建了基于代码的验证框架，模型在此过程中既生成指令也生成相应的验证代码，配合全面的单元测试进行交叉验证。通过基于执行反馈的拒绝采样方法，他们精心挑选训练数据，确保模型能够精准遵循指令。</font>
    5. **<font style="color:rgb(25, 27, 31);">结构化数据理解</font>**<font style="color:rgb(25, 27, 31);">：团队开发了一个包含传统任务（如表格问答、事实验证、错误修正和结构理解）和涉及结构化及半结构化数据的复杂任务的数据集。通过加入CoT，大大增强了模型从结构化数据中推理的能力，从而提高了在这些多样任务中的表现。这个方法不仅扩大了数据集的覆盖范围，也加深了模型从复杂数据结构中提取有意义见解的能力。</font>
    6. **<font style="color:rgb(25, 27, 31);">逻辑推理</font>**<font style="color:rgb(25, 27, 31);">：为了提升模型的逻辑推理能力，团队引入了来自多个领域的70,000个新查询，这些查询涵盖了多项选择题、判断题和开放性问题。模型通过演绎推理、归纳推理、类比推理等多种方式系统性地处理这些问题。通过迭代优化，他们剔除错误答案和有缺陷的推理过程，从而加强了模型的推理能力，确保其在逻辑推理任务中的高效表现。</font>
    7. **<font style="color:rgb(25, 27, 31);">跨语言迁移</font>**<font style="color:rgb(25, 27, 31);">：为了帮助模型跨语言迁移，团队使用翻译模型将高资源语言的指令翻译为多种低资源语言，从而生成对应的响应候选，并评估这些响应与原始响应的语义对齐情况，保证了响应在不同语言之间的逻辑结构和风格一致性。</font>
    8. **<font style="color:rgb(25, 27, 31);">鲁棒系统指令</font>**<font style="color:rgb(25, 27, 31);">：通过构建数百条通用系统提示词，团队确保了后训练阶段系统提示词的多样性和一致性，评估表明模型在不同的系统提示词下仍能保持优异的表现和较小的方差，增强了模型的鲁棒性。</font>
    9. **<font style="color:rgb(25, 27, 31);">响应过滤</font>**<font style="color:rgb(25, 27, 31);">：团队使用多种自动化注释方法进行响应评估，包括专门的评论模型和多智能体协作评分系统。所有响应都经过严格筛选，只有被所有评分系统认为完美的响应才会被保留，从而保证了输出的高质量标准。</font>
2. **强化学习**

<font style="color:rgb(25, 27, 31);">Qwen2.5的强化学习过程分为两个独立的阶段：</font>**<font style="color:rgb(25, 27, 31);">离线强化学习</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">在线强化学习</font>**<font style="color:rgb(25, 27, 31);">。</font>

    1. **<font style="color:rgb(25, 27, 31);">离线强化学习</font>**<font style="color:rgb(25, 27, 31);">：此阶段着重于</font>**<font style="color:#74B602;">开发奖励模型难以评估的能力，例如推理、事实准确性和指令执行</font>**<font style="color:rgb(25, 27, 31);">。通过精心设计和验证训练数据，确保离线强化学习信号既可以学习，又具有可靠性，帮助模型有效掌握这些复杂技能。</font>
    2. **<font style="color:rgb(25, 27, 31);">在线强化学习</font>**<font style="color:rgb(25, 27, 31);">：在线强化学习阶段利用奖励模型检测输出质量的细微差异，包括真实性、帮助性、简洁性、相关性、安全性以及去偏见。通过这一过程，模型能够生成</font>**<font style="color:#74B602;">精确、一致、结构清晰的回答</font>**<font style="color:rgb(25, 27, 31);">，同时保持</font>**<font style="color:#74B602;">安全性和可读性</font>**<font style="color:rgb(25, 27, 31);">。因此，模型的输出始终符合人类的质量标准和预期。具体的标注指南如下：</font>
        * **<font style="color:rgb(25, 27, 31);">真实性</font>**<font style="color:rgb(25, 27, 31);">：响应必须基于真实的事实，准确反映提供的上下文和指令。模型应避免生成任何虚假或缺乏数据支持的信息。</font>
        * **<font style="color:rgb(25, 27, 31);">帮助性</font>**<font style="color:rgb(25, 27, 31);">：模型输出的内容应切实有用，能够有效地回答用户的查询，并提供积极、富有吸引力、教育性强且相关的内容。应严格按照指令执行，确保对用户有价值。</font>
        * **<font style="color:rgb(25, 27, 31);">简洁性</font>**<font style="color:rgb(25, 27, 31);">：响应应简明扼要，避免无关的冗余内容，确保清晰高效地传达信息，而不让用户被细节淹没。</font>
        * **<font style="color:rgb(25, 27, 31);">相关性</font>**<font style="color:rgb(25, 27, 31);">：所有回应的内容都应紧密关联于用户的查询、对话历史以及助手的当前上下文。模型应定制其输出，确保与用户的需求和期望完全一致。</font>
        * **<font style="color:rgb(25, 27, 31);">无害性</font>**<font style="color:rgb(25, 27, 31);">：模型必须优先保障用户安全，避免产生任何可能导致非法、不道德或有害行为的内容。始终提倡道德行为和负责任的交流。</font>
        * **<font style="color:rgb(25, 27, 31);">去偏见</font>**<font style="color:rgb(25, 27, 31);">：模型生成的响应必须没有偏见，涉及性别、种族、国籍或政治等各类偏见，确保公平和公正，遵循广泛接受的道德和伦理标准。</font>

:::color5
**<font style="color:#601BDE;">6.模型评估</font>**

:::

<font style="color:rgb(25, 27, 31);">团队对Qwen2.5系列的基础语言模型进行了全面评估。基础模型的评估主要侧重于其在自然语言理解、一般问答、编码、数学、科学知识、推理和多语言能力方面的表现。评估数据集包括：</font>

+ **<font style="color:rgb(25, 27, 31);">一般任务</font>**<font style="color:rgb(25, 27, 31);">：MMLU(5-shot), MMLU-Pro(5-shot), MMLU-redux(5-shot), BBH(3-shot), ARC-C(25-shot), TruthfulQA(0-shot), Winogrande(5-shot), HellaSwag(10-shot).</font>
+ **<font style="color:rgb(25, 27, 31);">数学与科学任务</font>**<font style="color:rgb(25, 27, 31);">：GPQA(5-shot), TheoremQA(5-shot), GSM8K(4-shot), MATH(4-shot).</font>
+ **<font style="color:rgb(25, 27, 31);">编码任务</font>**<font style="color:rgb(25, 27, 31);">：HumanEval(0-shot), HumanEval+(0-shot), MBPP(0-shot), MBPP+(0-shot), MultiPL-E(0-shot)（Python, C++, JAVA, PHP, TypeScript, C#, Bash, JavaScript）。</font>
+ **<font style="color:rgb(25, 27, 31);">多语言任务</font>**<font style="color:rgb(25, 27, 31);">：团队将其分为四类：  
</font><font style="color:rgb(25, 27, 31);">(a) 考试：M3Exam (5-shot, 仅选择不需要图片的示例)，IndoMMLU(3-shot)，ruMMLU(5-shot)和翻译后的MMLU(5-shot, 阿拉伯语、西班牙语、法语、葡萄牙语、德语、意大利语、日语和韩语)；  
</font><font style="color:rgb(25, 27, 31);">(b) 理解：BELEBELE(5-shot)，XCOPA(5-shot)，XWinograd(5-shot)，XStoryCloze(0-shot) 和 PAWS-X(5-shot)；  
</font><font style="color:rgb(25, 27, 31);">(c) 数学：MGSM(8-shot CoT)；  
</font><font style="color:rgb(25, 27, 31);">(d) 翻译：Flores-101(5-shot)。</font>

<font style="color:rgb(25, 27, 31);">Qwen2.5-72B基础模型在广泛的任务中显著超越同类模型，特别是在</font>**<font style="color:rgb(25, 27, 31);">通用任务</font>**<font style="color:rgb(25, 27, 31);">、</font>**<font style="color:rgb(25, 27, 31);">数学</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">编码</font>**<font style="color:rgb(25, 27, 31);">挑战中表现突出。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743044509903-fc932bf2-f053-4823-af3d-b33e148f0232.png)

:::color5
**<font style="color:#601BDE;">7.未来方向</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">数据优化与模型迭代</font>**<font style="color:rgb(25, 27, 31);">：通过引入更多元化、更高质量的数据，不断改进基础模型与指令微调模型，使其更贴近实际需求。</font>
2. **<font style="color:rgb(25, 27, 31);">多模态融合</font>**<font style="color:rgb(25, 27, 31);">：重点开发多模态模型，将文本、视觉和听觉等模态整合到统一的框架中，推动跨领域信息处理的无缝集成。</font>
3. **<font style="color:rgb(25, 27, 31);">推理能力提升</font>**<font style="color:rgb(25, 27, 31);">：通过优化推理计算资源，提高模型在复杂任务中的推理能力，从而扩展其应用范围。</font>

  


### Qwen 2
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">Qwen2 在模型尺⼨、多语⾔⽀持、上下⽂⻓度、代码和数学能⼒、安全性等多个⽅⾯都有了 显著的提升。这些改进不仅增强了模型的性能，也扩⼤了其应⽤范围。通过采⽤更开放的许  可，Qwen2 将在全球范围内加速落地和商业应⽤。</font>

<font style="color:#1f2329;">paper:</font>[https://arxiv.org/pdf/2407.10671](https://arxiv.org/pdf/2407.10671)

<font style="color:#1f2329;">参考：</font>[Qwen2源码解析](https://zhuanlan.zhihu.com/p/707921243)  [Qwen2技术报告（全文）](https://zhuanlan.zhihu.com/p/709433404)

:::

<font style="color:rgb(25, 27, 31);">Qwen2系列包括五种规模的模型，分别是Qwen2-0.5B、Qwen2-1.5B、Qwen2-7B、Qwen2-57B-A14B和Qwen2-72B。</font><u><font style="color:rgb(25, 27, 31);">表1</font></u><font style="color:rgb(25, 27, 31);">列出了超参数和重要信息，如预训练token的数量。特别是，Qwen2-57B-A14B是从Qwen2-7B扩展而来的。值得注意的是，与Qwen1.5模型相比，Qwen2模型每个token的键值（KV）大小显著较低。这一特性使得在长上下文推理任务中内存占用大幅减少。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743074908133-909c10f0-9959-4698-ab7a-10abefecbbf6.png)

:::color5
**<font style="color:#601BDE;">1.模型架构</font>**

:::



<font style="color:rgb(25, 27, 31);">Qwen2延续了Qwen的</font>**<font style="color:rgb(25, 27, 31);">SwiGLU</font>**<font style="color:rgb(25, 27, 31);">激活函数，</font>**<font style="color:rgb(25, 27, 31);">旋转位置向量（</font>**[**<font style="color:rgb(9, 64, 142);">RoPE</font>**](https://zhida.zhihu.com/search?content_id=245783327&content_type=Article&match_order=1&q=RoPE&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">进行位置编码，</font>**<font style="color:rgb(25, 27, 31);">QKV偏置</font>**<font style="color:rgb(25, 27, 31);">进行注意力处理，以及</font>[**<font style="color:rgb(9, 64, 142);">RMSNorm</font>**](https://zhida.zhihu.com/search?content_id=245783327&content_type=Article&match_order=1&q=RMSNorm&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">预归一化方法</font>**<font style="color:rgb(25, 27, 31);">以确保训练的稳定性。</font>

1. **tokenizer**

<font style="color:rgb(25, 27, 31);">按照Qwen的方案，Qwen2采用了基于</font>**<font style="color:rgb(25, 27, 31);">字节级别的字节对编码（byte-level byte-pair encoding）</font>**<font style="color:rgb(25, 27, 31);">的相同tokenizer。这个tokenizer表现出高效的编码效率，其压缩率优于其他方案，从而增强了Qwen2的多语言处理能力。所有规模的模型都使用包含151,643个常规token和3个控制token的通用词汇表。</font>

2. **<font style="color:rgb(25, 27, 31);">Grouped Query Attention, </font>**[**<font style="color:rgb(9, 64, 142);">GQA</font>**](https://zhida.zhihu.com/search?content_id=245783327&content_type=Article&match_order=1&q=GQA&zhida_source=entity)

**<font style="color:rgb(25, 27, 31);">分组查询注意力</font>**<font style="color:rgb(25, 27, 31);">：Qwen2采用</font>**<font style="color:rgb(25, 27, 31);">分组查询注意力（Grouped Query Attention, </font>**[**<font style="color:rgb(9, 64, 142);">GQA</font>**](https://zhida.zhihu.com/search?content_id=245783327&content_type=Article&match_order=1&q=GQA&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">取代传统的</font>**<font style="color:rgb(25, 27, 31);">多头注意力（Multi-Head Attention, MHA）</font>**<font style="color:rgb(25, 27, 31);">。GQA优化了推理期间的KV-Cache使用，显著提高了数据处理的吞吐量。</font>

3. **上下文扩展**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739244063352-2cc89ead-fc81-4a8f-9ba5-a729ae82eddd.png)

    1. **<font style="color:#117CEE;">QWEN2上下文扩展</font>**
    - <font style="color:#1f2329;">预训练模型：在 32K tokens 的数据上训练 ，并在 128K tokens 时仍有良好表现。</font>
    - <font style="color:#1f2329;">指令微调模型：最⾼⽀持到 128K tokens 的上下⽂⻓度。</font>
    1. **<font style="color:#117CEE;">技术实现</font>**
    - <font style="color:#1f2329;">YARN（YetAnotherRopeExtension） ：⼀种扩展上下⽂⻓度的⽅法 ，通过调整位置编码实现。</font>
    - <font style="color:#1f2329;">DualChunkAttention：将⻓序列分块处理 ，降低计算复杂度。</font>
4. **<font style="color:rgb(25, 27, 31);">MOE</font>**

<font style="color:rgb(25, 27, 31);">Qwen2 MoE模型的架构与Qwen1.5-MoE-A2.7B高度相似。</font>**<font style="color:#74B602;">MoE FFN取代了原始FFN，由n个独立的FFN组成，每个FFN作为一个专家</font>**<font style="color:rgb(25, 27, 31);">。每个token根据门控网络 </font><font style="color:rgb(25, 27, 31);">G</font><font style="color:rgb(25, 27, 31);"> 分配的概率被引导到一个特定的专家 </font><font style="color:rgb(25, 27, 31);">Ei</font><font style="color:rgb(25, 27, 31);"> 进行计算：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743074458364-132391c7-079e-4c00-afa2-2bdd31c62644.png)

+ **<font style="color:rgb(25, 27, 31);">细粒度专家</font>**<font style="color:rgb(25, 27, 31);">：MoE模型和密集模型的主要结构区别在于MoE层包含多个FFN，每个FFN作为一个独立的专家。因此，从密集架构过渡到MoE架构的一种简单策略是将每个专家的参数设置为原始密集模型中单个FFN的参数。例如，</font>**<font style="color:#74B602;">从Mistral-7B过渡到Mixtral 8x7B时，每次激活八个专家中的两个。而Qwen2模型采用细粒度专家，创建了更小规模的专家，并同时激活更多的专家。</font>**<font style="color:rgb(25, 27, 31);">给定相同的总专家参数和激活参数，细粒度专家提供了更丰富的专家组合。通过利用这些细粒度专家，Qwen2 MoE实现了更为多样化和动态的专家使用，从而提升了整体性能和适应性。</font>
+ **<font style="color:rgb(25, 27, 31);">专家路由</font>**<font style="color:rgb(25, 27, 31);">：专家路由机制的设计对于提高MoE模型的性能至关重要。最近的趋势是</font>**<font style="color:#74B602;">将共享专家和特定路由专家结合在MoE层中</font>**<font style="color:rgb(25, 27, 31);">。Qwen2采用了这种方法，这有助于将共享专家应用于各种任务，同时保留其他专家用于特定的路由场景。共享和专用专家的引入提供了一种更灵活和高效的方法来开发MoE路由机制。</font>
+ **<font style="color:rgb(25, 27, 31);">专家初始化</font>**<font style="color:rgb(25, 27, 31);">：Qwen2采用</font>**<font style="color:rgb(25, 27, 31);">类似于回收的方式初始化专家</font>**<font style="color:rgb(25, 27, 31);">，利用密集模型的权重。与此不同，Qwen2的方法强调细粒度专家之间的多样化，以增强模型的表示广度。给定专家中间层大小 </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">E</font></sub><font style="color:rgb(25, 27, 31);"> 、专家数量 </font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);"> 和原始FFN中间层大小 </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">FFN</font></sub><sub><font style="color:rgb(25, 27, 31);"> </font></sub><font style="color:rgb(25, 27, 31);">，FFN被复制了 </font><font style="color:rgb(25, 27, 31);">⌈n×h</font><sub><font style="color:rgb(25, 27, 31);">E</font></sub><font style="color:rgb(25, 27, 31);">/h</font><sub><font style="color:rgb(25, 27, 31);">FFN</font></sub><font style="color:rgb(25, 27, 31);">⌉</font><font style="color:rgb(25, 27, 31);"> 次。</font>**<font style="color:rgb(25, 27, 31);">这种复制确保了与指定数量的专家兼容，同时适应任意的专家中间层大小</font>**<font style="color:rgb(25, 27, 31);">。为了在每个FFN副本中促进多样性，参数在中间维度上进行了混洗。这确保了每个细粒度专家即使在不同的FFN副本之间也表现出独特的特性。随后，从FFN副本中提取这些专家，其余维度被丢弃。</font>**<font style="color:#74B602;">对于每个细粒度专家，其50%的参数被随机重新初始化</font>**<font style="color:rgb(25, 27, 31);">。这一过程在专家初始化中引入了额外的随机性，可能增强模型在训练期间的探索能力。</font>

:::color5
**<font style="color:#601BDE;">2.多语言能力</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739244132254-7c57d360-977d-43e4-ae16-25485dc89b93.png)

1. **<font style="color:#117CEE;">训练数据</font>**

<font style="color:#1f2329;">除了中⽂和英语</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">Qwen2 </font><font style="color:#1f2329;">还增加了对 </font><font style="color:#1f2329;">27 </font><font style="color:#1f2329;">种语⾔的⾼</font><font style="color:#1f2329;">质量训练数据。</font><font style="color:#1f2329;">覆盖的语⾔区域</font>

+ <font style="color:#1f2329;">西欧：德语、法语、西班⽛语等</font>
+ <font style="color:#1f2329;">东欧及中欧：俄语、捷克语、波兰语</font>
+ <font style="color:#1f2329;">中东： 阿拉伯语、希伯来语等</font>
+ <font style="color:#1f2329;">东亚： ⽇语、韩语</font>
+ <font style="color:#1f2329;">东南亚：越南语、泰语等</font>
+ <font style="color:#1f2329;">南亚：印地语、孟加拉语等</font>





### Qwen
:::color3
**简介：**<font style="color:#1f2329;">通义千问（Qwen）系列模型通过⼤规模的预训练和精⼼设计的架构，展现了强⼤的⾃然语⾔理解和⽣成能⼒。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/QwenLM/Qwen](https://github.com/QwenLM/Qwen)

**paper：**[**https://github.com/QwenLM/Qwen2.5-Omni/blob/main/assets/Qwen2.5_Omni.pdf**](https://github.com/QwenLM/Qwen2.5-Omni/blob/main/assets/Qwen2.5_Omni.pdf)

**参考：**[**Qwen技术内容详解（万字长文，超级详细！）**](https://zhuanlan.zhihu.com/p/713421330)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744789347983-75fcea47-8447-4a9c-8420-7ab9255a60ca.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:#1f2329;">多语⾔⽀持</font>**<font style="color:#1f2329;">：优化的词汇表和编码⽅法 ，提升了模型在多种语⾔上的表现。</font>
2. **<font style="color:#1f2329;">改进的架构设计</font>**<font style="color:#1f2329;">：采⽤了SwiGLU激活函数、RoPE位置嵌⼊、⾮绑定的嵌⼊⽅法等，提升了模型性能。</font>
3. **<font style="color:#1f2329;">上下⽂⻓度扩展</font>**<font style="color:#1f2329;">：通过多种技术⼿段 ，扩展了模型的上下⽂⻓度 ，增强了对⻓⽂本的处理能⼒。</font>
4. **<font style="color:#1f2329;">专⽤模型</font>**<font style="color:#1f2329;">：针对代码和数学任务，开发了专⻔的模型（Code-Qwen、Math-Qwen），在相应领域 取得了优异的性能。</font>

:::color5
**<font style="color:#601BDE;">2.模型架构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739180029642-5471d553-7130-43c3-ae5f-87329a8f23d3.png)

1. **架构创新：**
    1. **<font style="color:#1f2329;">优化的Tokenization</font>**<font style="color:#1f2329;">：采⽤了更⼤的词汇表，包含152K个词元，在中⽂等多种语⾔上具有更好的压缩效率，降低了服务成本。</font>
    2. **<font style="color:#1f2329;">⾮绑定的嵌⼊⽅法</font>**<font style="color:#1f2329;">：输⼊嵌⼊和输出投影的权重不共享 ，提升了模型的性能。</font>
    3. **<font style="color:#1f2329;">偏置调整</font>**<font style="color:#1f2329;">：移除了⼤多数层的偏置，但在注意⼒的QKV层中添加了偏置，增强了模型的外推能⼒。</font>
    4. **<font style="color:#1f2329;">SwiGLU激活函数</font>**<font style="color:#1f2329;">：相⽐于GeLU ，SwiGLU在提⾼模型性能和效率⽅⾯表现更好。</font>
    5. **<font style="color:#1f2329;">上下⽂⻓度扩展</font>**<font style="color:#1f2329;">：通过NTK-aware插值、LogN-Scaling、窗⼝注意⼒等技术，扩展了模型的上下⽂⻓度，增强了对⻓⽂本的处理能⼒。</font>
2. **输入层**
    1. <font style="color:#1456f0;"></font><font style="color:#1f2329;">分词与编码：采⽤字节对编码（Byte Pair Encoding，BPE）⽅法，将输⼊⽂本进⾏分词和编码。为了增强多语⾔能⼒，Qwen的词汇表增加了常⽤的中⽂字符和其他语⾔的词汇，词汇表⼤⼩约为152K。</font>
    2. <font style="color:#1f2329;">压缩效率：在多种语⾔中 ，Qwen的压缩效率⾼于其他标记器 ，这意味着服务成本可以显著降低。</font>
3. **位置嵌入**
    1. <font style="color:#1f2329;">词嵌⼊（WordEmbedding）：将每个词或⼦词的索引映射为稠密的向量表⽰，捕捉词语的语义信息。</font>
    2. <font style="color:#1f2329;">位置嵌⼊（PositionalEmbedding）：采⽤</font><font style="color:#2ea121;">旋转位置嵌⼊（RoPE）</font><font style="color:#1f2329;">，将位置信息融⼊模型中。RoPE通过在输⼊中加⼊位置信息，使模型能够识别序列中词语的位置。</font>
4. **多层transformer**

<font style="color:#1f2329;">Qwen</font><font style="color:#1f2329;">的核⼼由多层</font><font style="color:#1f2329;">Transformer</font><font style="color:#1f2329;">解码器块组成</font><font style="color:#1f2329;">，每个块包含以下组</font><font style="color:#1f2329;">件：</font>

+ <font style="color:#1f2329;">多头⾃注意⼒机制（Multi-HeadSelf-Attention）</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">⽬的：捕捉序列中不同位置之间的依赖关系。</font>
    - <font style="color:#1f2329;">机制：通过计算查询（Q）、键（K）、值（V）之间的相关性，⽣成加权的输出表⽰。</font>
+ <font style="color:#1f2329;">前馈神经⽹络（Feed-ForwardNetwork, FFN）</font>
    - <font style="color:#1f2329;">结构： 由两个线性变换和⼀个⾮线性激活函数组成。</font>
    - <font style="color:#1f2329;">激活函数：采⽤</font><font style="color:#2ea121;">SwiGLU激活函数</font><font style="color:#1f2329;">，这是Swish和⻔控线性单元 （GLU）的组合，增强了模型的表达能⼒。</font>
+ <font style="color:#1f2329;">残差连接和层归⼀化</font>
    - <font style="color:#1f2329;">残差连接（ResidualConnection）：缓解深层⽹络的梯度消失问题，促进信息的直接传递。</font>
    - <font style="color:#1f2329;">层归⼀化（LayerNormalization）：采⽤</font><font style="color:#2ea121;">RMSNorm</font><font style="color:#1f2329;">，提升训练的稳定性和效率。</font>
5. **输出层**

<font style="color:#1f2329;">线性变换和Softmax层：将Transformer块的输出转换为词汇表中每个词的概率分布，⽤于预测下⼀个词。</font>

:::color5
**<font style="color:#601BDE;">3.模型训练</font>**

:::

1. **<font style="color:#117CEE;">预训练</font>**
+ <font style="color:#1f2329;">数据规模：使⽤了多达</font><font style="color:#2ea121;">3万亿个标记</font><font style="color:#1f2329;">的数据，包括公共⽹络⽂档、百科全书、书籍、代码等，涵盖多种类型和领域。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">多语⾔⽀持：数据集是多语⾔的 ，其中相当⼀部分是中⽂和英⽂。</font>
+ <font style="color:#1f2329;">数据预处理：使⽤了全⾯的数据预处理程序，包括去重、语⾔识别、质量过滤等，确保数据的多样性和⾼质量。</font>
+ <font style="color:#1f2329;">⽬标：在⼤规模未标注的⽂本数据上训练模型 ，让其学习语⾔的基本结构和模式。</font>
+ <font style="color:#1f2329;">⽅法：采⽤⾃回归语⾔建模任务 ，即给定前⾯的词 ，预测下⼀个词。</font>
+ <font style="color:#1f2329;">优化器：使⽤AdamW优化器 ，设置了适当的超参数以保证训练稳定性。</font>
2. **<font style="color:#117CEE;">上下文长度扩展</font>**
+ <font style="color:#1f2329;">挑战：随着上下⽂⻓度的增加 ，计算和内存成本急剧增加。</font>
+ <font style="color:#1f2329;">解决⽅案：</font>
    - <font style="color:#1f2329;">NTK-aware插值：调整RoPE的位置编码，防⽌在不训练的情况下丢失⾼频信息。</font>
    - <font style="color:#1f2329;">LogN-Scaling：调整注意⼒机制的缩放因⼦，保持注意⼒值的稳定性。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">窗⼝注意⼒：将注意⼒限制在有限的上下⽂窗⼝内，防⽌模型注意到过远的标记。</font>
    - <font style="color:#1f2329;">分层窗⼝分配：为每⼀层分配不同的窗⼝⼤⼩，低层使⽤较短的窗⼝ ，⾼层使⽤较⻓的窗⼝，提升⻓上下⽂建模能⼒。</font>
3. **<font style="color:#117CEE;">SFT</font>**
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">监督微调（SFT）：</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">⽬标：使预训练模型适应对话式AI助⼿的任务。</font>
    - <font style="color:#1f2329;">数据：使⽤了精⼼标注的对话数据，包括任务执⾏、聊天、⼯具使⽤、安全等⽅⾯。</font>
    - <font style="color:#1f2329;">⽅法：在预训练模型的基础上，使⽤标注的对话数据，对模型进⾏微调。</font>
4. **<font style="color:#117CEE;">RLHF</font>**
+ <font style="color:#1f2329;">⽬标：进⼀步使模型与⼈类偏好保持⼀致，⽣成更符合⼈类期望的响应。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">奖励模型训练：收集⼈类反馈的数据，训练⼀个奖励模型来评估模型输出的质量。</font>
    - <font style="color:#1f2329;">策略优化：使⽤近端策略优化（PPO），根据奖励模型的评估结果，优化模型的策略。</font>

:::color5
**<font style="color:#601BDE;">评估</font>**

:::

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">基准评估：在MMLU、C-Eval、GSM8K、HumanEval、BBH等多个基准测试中评估模型性能。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">Qwen-14B：在多个下游任务中表现出⾊，甚⾄超过了⼀些更⼤参数规模的模型，如LLaMA2-70B。</font>
    - <font style="color:#1f2329;">Qwen-7B：表现优于同等规模的模型，如LLaMA2-13B。</font>
    - <font style="color:#1f2329;">Code-Qwen：在代码⽣成任务上，表现优于同等规模的专有和开源模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743045484753-a682ca75-35f0-4804-a99b-6d1d02c8c1ff.png)

### Qwen-Code
+ <font style="color:#1f2329;">⽬标：专⻔⽤于编码任务的模型 ，包括代码⽣成、调试和解释。</font>
+ <font style="color:#1f2329;">训练⽅法：</font>
    - <font style="color:#1f2329;">继续预训练：在基础模型的基础上，继续在⼤量代码数据上进⾏预训练。</font>
    - <font style="color:#1f2329;">代码监督微调：使⽤与代码⽣成、调试和解释相关的对话数据，对模型进⾏微调。</font>
+ <font style="color:#1f2329;">性能：在HumanEval、 MBPP等代码基准数据集上表现出⾊ ，超过了许多开源模型。</font>

### Qwen-Math
+ <font style="color:#1f2329;">⽬标：专⻔⽤于解决数学问题的模型 ，提升模型在算术和数学推理⽅⾯的能⼒。</font>
+ <font style="color:#1f2329;">训练⽅法：</font>
    - <font style="color:#1f2329;">数学SFT：在增强的数学指导数据集上进⾏监督微调，直接得到聊天模型Math-Qwen-Chat。</font>
+ <font style="color:#1f2329;">性能：在GSM8K、MATH等数学基准数据集上表现出⾊，超过了相同规模的开源模型，接近于GPT-3.5的性能。</font>

<font style="color:#1f2329;"></font>

## LLAMA
### LLAMA 4 <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">随着越来越多的人继续使用人工智能增强日常生活，领先的模型和系统保持开放至关重要，这样每个人都能共同构建个性化的未来体验。当地时间2025.4.5，MetaAI宣布支持整个 </font>[Llama](https://link.zhihu.com/?target=https%3A//www.llama.com/)<font style="color:rgb(25, 27, 31);"> 生态系统的最先进模型套件，推出了 Llama 4 Scout 和 Llama 4 Maverick，这是首批支持超长上下文长度的开源原生多模态模型，也是MetaAI首次使用混合专家（MoE）架构构建的模型。Meta还提出了 Llama 4 Behemoth，这是全球最智能的 LLM 之一，也是Meta迄今最强大的模型，作为新模型的教师。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**Llama 4是原生训练的多模态大模型，采用MoE架构，目前共有三个版本：

+ **Llama 4 Scout**：109B模型参数和17B激活参数，16个专家，是最小号Llama 4模型，可以跑在单个NVIDIA H100GPU上（采用Int4量化后），支持10M上下文，效果超过Gemma 3、Gemini 2.0 Flash-Lite#lMistral 3.1.
+ **Llama 4 Maverick**：400B模型参数和17B激活参数，128个专家，效果超过GPT-40和Gemini 2.0  
Flash，在推理和编程方面与新版本DeepSeek v3相当。Llama 4 Maverick在LMArena上的ELO得分为1417，目前仅次于Gemini 2.5 Pro，排行第二。
+ **Llama 4 Behemoth**：2T模型参数和288B激活参数，16个专家，是最大号的Llama 4模型，在多个STEM基准测试中超过了GPT-4.5、Claude Sonnet 3.7和Gemini 2.0 Pro。Behemoth也做为小模型的教师模型来进行模型蒸馏。<font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[llama4/MODEL_CARD.md](https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md)

**官方报告：**[**https://ai.meta.com/blog/llama-4-multimodal-intelligence/**](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)

**参考：**[**https://zhuanlan.zhihu.com/p/1892052102416684916**](https://zhuanlan.zhihu.com/p/1892052102416684916)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743917941540-fb0f8a14-0da3-491d-bd32-dc7da647194e.png)![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743917711886-4f6fca6a-5384-4d8d-b92a-4b1369e9cde5.png)

:::color5
**<font style="color:#601BDE;">1.三个型号模型对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ [<font style="color:rgb(9, 64, 142);">Llama-4</font>](https://zhida.zhihu.com/search?content_id=256039385&content_type=Article&match_order=1&q=Llama-4&zhida_source=entity)<font style="color:rgb(25, 27, 31);">-Scout-17B-16E, （其实是109B）</font>[<font style="color:rgb(9, 64, 142);">MoE模型</font>](https://zhida.zhihu.com/search?content_id=256039385&content_type=Article&match_order=1&q=MoE%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，多模态输入，16个专家，激活参数量17B，上下文长度10M，知识截至时间2024年8月</font>
+ <font style="color:rgb(25, 27, 31);">Llama-4-Maverick-17B-128E，（其实是402B） MoE模型，多模态输入，128个专家，激活参数量17B，上下文长度1M，知识截至时间2024年8月</font>
+ <font style="color:rgb(25, 27, 31);">Llama-4-Behemoth-288B-16E，（其实是2T），还在训练中</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743915771861-557aa6fe-6ca4-4c98-865f-a6da513b1dff.png)

:::color5
**<font style="color:#601BDE;">2.新的后训练流程  Post-Train</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在后训练 Llama 4 Maverick 模型时，最大的挑战是维持多种输入模态、推理和对话能力之间的平衡。对于混合模态，Meta提出了一个精心策划的课程策略，与单一模态专家模型相比不会牺牲性能。Meta通过采用不同方法重构了后训练流程：</font>**<font style="color:#74B602;">轻量级监督微调（SFT）> 在线强化学习（RL）> 轻量级直接偏好优化（DPO）</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ **轻量级 SFT：** 先教模型基本的指令遵循和对话格式（打基础，但不过度）。
    - <font style="color:rgb(25, 27, 31);">用 Llama 模型作为评判，移除了超过50%标记为简单的训练数据，并在剩余的较难数据集上进行轻量级 SFT</font>
+ **在线 RL (核心)：** 让模型在探索中学习解决难题，提升核心智能和复杂任务能力（拔高能力）。
    - <font style="color:rgb(25, 27, 31);">精心挑选较难的提示词 prompt，我们实现了性能的显著提升</font>
    - <font style="color:rgb(25, 27, 31);">持续的在线 RL 策略：在训练模型和使用它不断过滤并保留中等至高难度提示词之间交替进行。这一策略在计算和准确性权衡方面证明是非常有益的</font>
+ **轻量级 DPO：** 最后进行微调，修正一些边角情况 (corner cases) 的回答质量和风格，确保模型在智能和对话流畅性之间达到良好平衡**<font style="color:#74B602;">（精修和打磨）</font>**。<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743916269889-7fd04318-a2d7-4273-a021-9ef668e1d179.png)

:::color5
**<font style="color:#601BDE;">3.MoE架构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

MoE 本质上是用**<font style="color:#74B602;">更大的内存占用换取了更低的计算量和更强的模型能力（因为总容量更大）</font>**。对于许多推理场景（尤其是吞吐量敏感型），计算成本是瓶颈，所以 MoE 是划算的。

<font style="color:rgb(25, 27, 31);">在 MoE 模型中，单个 token 仅激活总参数的一部分。</font>[<font style="color:rgb(9, 64, 142);">MoE 架构</font>](https://zhida.zhihu.com/search?content_id=256038426&content_type=Article&match_order=1&q=MoE+%E6%9E%B6%E6%9E%84&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在训练和推理时计算效率更高，在固定的训练 FLOPs 预算下，与密集模型相比能提供更高的质量。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743917756980-cffb14cd-1969-4c65-a91a-80ae5d75c7b7.png)

:::color5
**<font style="color:#601BDE;">4.原生多模态</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

不同于传统「拼接式」多模态，Llama 4 采用**<font style="color:#74B602;">早期融合（Early Fusion） 在模型主干就结合文本、图像以及视频帧等 token，</font>**<font style="color:rgb(25, 27, 31);">能够使用大量未标记的文本、图像和视频数据共同预训练模型</font>，对多模态理解能力提升明显，尤其在视觉定位 (grounding) 上表现突出。 这一点比较期待，我感觉开源环境非常需要一个平价的、能打的多模态模型。

<font style="color:rgb(25, 27, 31);">Meta还改进了 Llama 4 的视觉编码器。这是基于 </font>[<font style="color:rgb(9, 64, 142);">MetaCLIP</font>](https://zhida.zhihu.com/search?content_id=256038426&content_type=Article&match_order=1&q=MetaCLIP&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的，但与冻结的 Llama 模型结合单独训练，以更好地适应大语言模型（LLM）。</font>对比一下后期融合和早期融合：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743916053906-1442acf5-4685-4df3-8ba7-020b93928623.png)

:::color5
**<font style="color:#601BDE;">5.超长上下文能力</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Llama 4 Scout 号称能处理**<font style="color:#74B602;"> 10M tokens </font>**的上下文，借助**<font style="color:#74B602;"> iRoPE（交错注意力层 + Rotary Position Embeddings）与推理时注意力温度缩放</font>**等技术实现大规模长度泛化。

**iRoPE 的改进**：

+ **分层位置编码**：不同层使用不同的 θ 值，低频层（浅层）捕捉长程依赖，高频层（深层）聚焦局部细节。
+ **无位置嵌入层**：部分层（如全局稀疏层）完全移除位置编码，依赖注意力机制隐式学习位置关系。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743916160882-1d9e47bb-6c7d-4a0f-b993-fe9e448a42d6.png)  


:::color5
**<font style="color:#601BDE;">6.将LLAMA推向新规模：2T Behemoth</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);"> Llama 4 Behemoth是一个展示同类模型中高级智能的教师模型，也是一个多模态混合专家（MoE）模型，拥有</font>**<font style="color:#74B602;">288B 活跃参数、16个专家和近2万亿总参数</font>**<font style="color:rgb(25, 27, 31);">。它在数学、多语言和图像基准测试中为非推理模型提供最先进的性能，是教授较小 Llama 4 模型的完美选择。</font>

<font style="color:rgb(25, 27, 31);">Meta从 Llama 4 Behemoth </font>**<font style="color:#74B602;">作为教师模型共同蒸馏了 Llama 4 Maverick 模型</font>**<font style="color:rgb(25, 27, 31);">，从而在最终任务评估指标上实现了显著的质量提升。Meta开发了一种新的蒸馏损失函数，通过训练动态加权软目标和硬目标。从 Llama 4 Behemoth 进行预训练期间的共同蒸馏分摊了计算密集型前向传递的计算成本，这些前向传递是为学生训练中使用的大部分训练数据计算蒸馏目标所需的。对于学生训练中纳入的额外新数据，Meta在 Behemoth 模型上运行前向传递以创建蒸馏目标。</font>

<font style="color:rgb(25, 27, 31);">将 RL 扩展到2万亿参数模型还需要</font>**<font style="color:#74B602;">改造底层 RL 基础设施</font>**<font style="color:rgb(25, 27, 31);">。Meta优化了 MoE 并行化的设计以提高速度，从而实现更快的迭代。Meta开发了一个</font>**<font style="color:#74B602;">完全异步的在线 RL 训练框架，增强了灵活性</font>**<font style="color:rgb(25, 27, 31);">。与现有的分布式训练框架相比，后者为了将所有模型堆叠在内存中而牺牲了计算内存，Meta的新基础设施能够灵活地将不同模型分配到单独的 GPU 上，根据计算速度平衡多个模型的资源。这一创新使训练效率比前几代提高了约10倍。</font>

:::color5
**<font style="color:#601BDE;">7.风险保护</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Meta的目标是开发最有帮助和实用的模型，同时防范和减轻最严重的风险。Meta根据《开发者使用指南：AI 保护》中概述的最佳实践构建了 Llama 4。这包括在模型开发的每个阶段（从预训练到后训练）整合缓解措施，以及可调的系统级缓解措施，以保护开发者免受对抗性用户的侵害。这样做赋予开发者创建有帮助、安全且适应性强的 Llama 支持应用程序体验的能力。</font>

1. **<font style="color:rgb(25, 27, 31);">系统级方法</font>**

<font style="color:rgb(25, 27, 31);">在系统层面，我们开源了几个</font>**<font style="color:#74B602;">保护措施，可以帮助识别和防范潜在有害的输入和输出</font>**<font style="color:rgb(25, 27, 31);">。这些工具可以集成到我们的 Llama 模型中以及与其他第三方工具一起使用：</font>

+ **<font style="color:rgb(25, 27, 31);">Llama Guard</font>**<font style="color:rgb(25, 27, 31);">：我们基于与 MLCommons 共同开发的</font>[危害分类法](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2404.12241)<font style="color:rgb(25, 27, 31);">构建的输入/输出安全大语言模型（LLM）。开发者可以使用它来检测输入或输出是否违反他们为特定应用程序制定的政策。</font>
+ **<font style="color:rgb(25, 27, 31);">Prompt Guard</font>**<font style="color:rgb(25, 27, 31);">：一个在大量攻击语料库上训练的分类器模型，能够检测显式恶意提示词（Jailbreaks）以及包含注入输入的提示词（Prompt Injections）。</font>
+ **<font style="color:rgb(25, 27, 31);">CyberSecEval</font>**<font style="color:rgb(25, 27, 31);">：帮助 AI 模型和产品开发者理解和降低生成式 AI 网络安全风险的评估。</font>
2. **<font style="color:rgb(25, 27, 31);">评估和红队测试</font>**

<font style="color:rgb(25, 27, 31);">我们以受控且可重复的方式对模型进行广泛的场景和用例的系统测试。这产生了我们反馈到后训练中的数据。我们使用自动和手动测试，通过对抗性动态探测对模型进行压力测试，涵盖一系列主题。我们在理解和评估潜在模型风险方面取得了进展。一个例子是我们新开发的</font>**<font style="color:#74B602;">生成式进攻性代理测试（GOAT）</font>**<font style="color:rgb(25, 27, 31);">。使用 GOAT，我们</font>**<font style="color:#74B602;">通过模拟中等技能对抗性角色的多轮交互，解决了传统红队测试的局限性</font>**<font style="color:rgb(25, 27, 31);">，帮助我们增加测试覆盖率并更快地发现漏洞。通过将自动化添加到我们的测试工具包中，GOAT 使我们的人类专家红队成员能够专注于更新颖的对抗性领域，而自动化则专注于已知风险领域。这使过程更高效和有效，并使我们能够构建更好的定量和定性风险图景。</font>

3. **<font style="color:rgb(25, 27, 31);">解决 LLM 中的偏见</font>**

<font style="color:rgb(25, 27, 31);">众所周知，所有领先的 LLM 在偏见方面都存在问题——具体来说，在有争议的政治和社会话题上，它们历史上倾向于左倾。这是由于互联网上可用的训练数据类型造成的。</font>

<font style="color:rgb(25, 27, 31);">我们的目标是从 AI 模型中消除偏见，并确保 Llama 能够理解并表达争议问题的双方观点。作为这项工作的一部分，我们正在继续使 Llama 更具响应性，以便它回答问题，能够对各种不同观点做出回应而不予评判，且不偏袒某些观点。</font>

<font style="color:rgb(25, 27, 31);">我们在这一版本中取得了这些努力的改进——Llama 4 的表现显著优于 Llama 3，并与 Grok 相当：</font>

+ <font style="color:rgb(25, 27, 31);">Llama 4 在</font>**<font style="color:#74B602;">有争议的政治和社会话题</font>**<font style="color:rgb(25, 27, 31);">上的总体拒绝率更低（从 Llama 3.3 的7%降至低于2%）。</font>
+ <font style="color:rgb(25, 27, 31);">Llama 4 在</font>**<font style="color:#74B602;">拒绝回应的提示词</font>**<font style="color:rgb(25, 27, 31);">上的平衡性显著提高（在一组有争议的主题问题上，不平等响应拒绝的比例现低于1%）。</font>
+ <font style="color:rgb(25, 27, 31);">我们的测试显示，Llama 4 在一组有争议的政治或社会话题上的强烈政治倾向响应率与 Grok 相当（且为 Llama 3.3 的一半）。虽然我们正在取得进展，但我们知道还有更多工作要做，并将继续努力进一步降低这一比率。</font>

:::color5
**<font style="color:#601BDE;">8.Llama4提示词格式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**角色定义** ：Llama 4 支持多种角色：

+ system：设定交互背景，包含规则、指南或必要信息。
+ user：代表与模型交互的人类，包含输入、命令或问题。
+ assistant：代表生成回复的模型。

**特殊标记** ：以下是 Llama 4 支持的全部特殊标记：

+ **通用标记**
    - <|begin_of_text|>：提示开始。
    - <|end_of_text|>：模型停止生成（仅预训练模型生成此标记）。
    - <|header_start|>...<|header_end|>：包裹消息角色（如 system/user/assistant）。
    - <|eot|>（End of Turn）：表示模型完成当前交互或工具调用。
+ **图像标记**
    - <|image_start|>...<|image_end|>：包裹图像数据。
    - <|patch|>：代表图像分块。大图像含更多此类标记。
    - <|tile_y_separator|> 和 <|tile_x_separator|>：标记图像分块的坐标轴。
    - <|image|>：分隔原尺寸图像与其缩略版本。

**多轮对话**<font style="color:#D22D8D;">（by草莓师姐）</font>

```python
<|begin_of_text|><|header_start|>system<|header_end|>

You are a helpful assistant<|eot|><|header_start|>user<|header_end|>

Answer who are you in the form of jeopardy?<|eot|><|header_start|>assistant<|header_end|>
```

```python
"What am I?"

(Wait for it...)

I am a helpful assistant, what am I?

Answer should be in the form:

Who is a helpful assistant?<|eot|>  
```

**单图模板**<font style="color:#D22D8D;">（by草莓师姐）</font>

```python
<|begin_of_text|><|header_start|>user<|header_end|>
<|image_start|><|image|><|patch|>...<|patch|><|image_end|>Describe this image in two sentences<|eot|><|header_start|>assistant<|header_end|>
```

```python
The image depicts a dog standing on a skateboard, with its front paws positioned on the board and its back paws slightly lifted. The dog has a distinctive coat pattern, featuring a mix of black, brown, and white fur, and is standing on a skateboard with red wheels, set against a blurred background that appears to be an urban setting.<|eot|>
```

**函数调用 Function Call**<font style="color:#D22D8D;">（by草莓师姐）</font>

```python
<|begin_of_text|><|header_start|>system<|header_end|>
你是编写函数的专家。你会得到一个问题和一组可能的函数。
根据问题，您需要进行一个或多个函数/工具调用来实现目的。
如果这些功能都不能使用，请指出。如果给定的问题缺少函数所需的参数，
也指出这一点。您应该只返回工具调用部分中的函数调用。
如果您决定调用任何函数，则必须将其格式设置为[func_name1（params_name1=params_value1，params_name2=params_value2…），func_name2（params）]
您不应该在回复中包含任何其他文本。
以下是可以调用的JSON格式的函数列表。
[
    {
        "name": "get_weather",
        "description": "Get weather info for places",
        "parameters": {
            "type": "dict",
            "required": [
                "city"
            ],
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get the weather for"
                },
                "metric": {
                    "type": "string",
                    "description": "The metric for weather. Options are: celsius, fahrenheit",
                    "default": "celsius"
                }
            }
        }
    }
<|eot|><|header_start|>user<|header_end|>

What is the weather in SF and Seattle?<|eot|><|header_start|>assistant<|header_end|>       
```

```python
[get_weather(city="San Francisco", metric="celsius"), get_weather(city="Seattle", metric="celsius")]<|eot|>
```

:::color5
**<font style="color:#601BDE;">9.评测</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">Llama-4-Scout-17B-16E ：测试中好于 </font>[<font style="color:rgb(9, 64, 142);">Gemma 3</font>](https://zhida.zhihu.com/search?content_id=256039385&content_type=Article&match_order=1&q=Gemma+3&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">Gemini 2.0 Flash-Lite</font>](https://zhida.zhihu.com/search?content_id=256039385&content_type=Article&match_order=1&q=Gemini+2.0+Flash-Lite&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 </font>[<font style="color:rgb(9, 64, 142);">Mistral 3.1</font>](https://zhida.zhihu.com/search?content_id=256039385&content_type=Article&match_order=1&q=Mistral+3.1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>
+ <font style="color:rgb(25, 27, 31);">Llama-4-Maverick-17B-128E ：来到了 lmarena排行榜第二名的成绩，仅次于 Gemini-2.5-pro. 官方宣称写代码水平接近 </font>[<font style="color:rgb(9, 64, 142);">DeepSeek-V3-0324</font>](https://zhida.zhihu.com/search?content_id=256039385&content_type=Article&match_order=1&q=DeepSeek-V3-0324&zhida_source=entity)
+ <font style="color:rgb(25, 27, 31);">Llama-4-Behemoth-288B-16E： 测试还未放出。</font>
1. **<font style="color:rgb(25, 27, 31);">Scout</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **图像理解能力同级别最强**<font style="color:rgb(25, 27, 31);">：在ChartQA和DocVQA测试中表现最佳。</font>
    - **推理与知识表现优异**<font style="color:rgb(25, 27, 31);">：MMLU Pro和GPQA Diamond测试中领先多数竞品。</font>
    - **长上下文支持领先**<font style="color:rgb(25, 27, 31);">：支持10M上下文窗口，适合处理超长文本任务。</font>
    - **性价比高**<font style="color:rgb(25, 27, 31);">：综合性能优于多数同类模型，表现强劲且支持多模态任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743917783051-d5c7c0ff-c850-4c73-bc4f-64dcf78d30ab.png)

2. **<font style="color:rgb(25, 27, 31);">Maverick</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **推理成本最优**<font style="color:rgb(25, 27, 31);">：Llama 4 Maverick 每 100 万 tokens 成本仅为 </font>`<font style="color:rgb(25, 27, 31);">$0.19-$0.49</font>`<font style="color:rgb(25, 27, 31);">，远低于 GPT-4o (</font>`<font style="color:rgb(25, 27, 31);">$4.38</font>`<font style="color:rgb(25, 27, 31);">) ，和DeepSeek v3.1量级相当且更低 (</font>`<font style="color:rgb(25, 27, 31);">$0.48</font>`<font style="color:rgb(25, 27, 31);">)。</font>
    - **多模态性能领先**<font style="color:rgb(25, 27, 31);">：在图像推理（MMMU、MathVista）和图像理解（ChartQA、DocVQA）测试中表现最佳，超越 Gemini 2.0 Flash 和 GPT-4o。</font>
    - **编程能力强劲**<font style="color:rgb(25, 27, 31);">：LiveCodeBench 中得分 43.4，领先 Gemini 2.0 Flash 和 GPT-4o，接近更大的 DeepSeek v3.1。</font>
    - **推理与知识卓越**<font style="color:rgb(25, 27, 31);">：在 MMLU Pro 和 GPQA Diamond 测试中表现优异，超越 Gemini 和 GPT-4o，接近 DeepSeek。</font>
    - **多语言支持强**<font style="color:rgb(25, 27, 31);">：多语言 MMLU 得分 84.6，优于 GPT-4o（81.5）。</font>
    - **长上下文窗口领先**<font style="color:rgb(25, 27, 31);">：支持 10M 上下文窗口，比其他模型的 128K 显著更强，适合处理超长文本任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743917771569-f78db1a2-a698-4f00-9d38-0c1f236e5202.png)

3. **<font style="color:rgb(25, 27, 31);">Behemoth</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **编程能力**<font style="color:rgb(25, 27, 31);">：在LiveCodeBench中得分49.4，领先Gemini 2.0 Pro。</font>
    - **推理与知识卓越**<font style="color:rgb(25, 27, 31);">：在MATH-500、MMLU Pro、GPQA Diamond等测试中表现优异，特别是MATH-500得分95.0，远超所有竞品。</font>
    - **多语言能力领跑**<font style="color:rgb(25, 27, 31);">：Multilingual MMLU测试中以85.8得分表现最佳。</font>
    - **图像推理能力强**<font style="color:rgb(25, 27, 31);">：MMMU测试中得分76.1，超过多数模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743917795308-7e4776b2-c8c7-4003-9d3d-1520116d605b.png)

:::color5
**<font style="color:#601BDE;">10.总结</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Llama 4 系列模型的发布标志着 Meta 在 AI 领域的里程碑式进展。这些模型凭借高效的 MoE 架构、强大的多模态能力和开放下载政策，为开发者提供了构建创新应用的机会。无论是 Llama 4 Scout 的效率、Llama 4 Maverick 的性价比，还是 Llama 4 Behemoth 的顶级性能，这一系列都预示着 AI 技术迈向更智能、更个性化的未来。

### LLAMA 3.1 
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739245981694-f58a4cd9-a248-437f-bdfe-ef9abf00bceb.png)

<font style="color:#1456f0;">1.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">性能⼤幅提升：超越同规模模型</font><font style="color:#1f2329;">，部分任务媲美 </font><font style="color:#1f2329;">GPT</font><font style="color:#1f2329;">-4</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">2.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">三阶段预训练：初始预训练、⻓⽂本预训练、退⽕训练。</font>

<font style="color:#1456f0;">3.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⾏级别去重：提⾼数据质量</font><font style="color:#1f2329;">，提升模型性能。</font>

<font style="color:#1456f0;">4.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">拒绝采样、</font><font style="color:#1f2329;">SFT</font><font style="color:#1f2329;">、</font><font style="color:#1f2329;">DPO </font><font style="color:#1f2329;">训练策略：有效利⽤合成数据和⽤户数据</font><font style="color:#1f2329;">，提升模型能⼒。</font>

<font style="color:#1456f0;">5.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">负熵原则：</font><font style="color:#1f2329;">引⼊外部⾼质量数据</font><font style="color:#1f2329;">，持续优化模型。</font>

<font style="color:#1456f0;">6.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">数据质量处理：多层次的数据过滤和清理。</font>

<font style="color:#1456f0;">7.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">Scaling</font><font style="color:#1f2329;">Law</font><font style="color:#1f2329;">应⽤：</font><font style="color:#1f2329;">合理配置模型规模和数据量。</font>

<font style="color:#1456f0;">8.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">4D </font><font style="color:#1f2329;">并⾏训练：⾼效利⽤计算资源</font><font style="color:#1f2329;">，训练超⼤规模模型。</font>

<font style="color:#1456f0;">9.  </font><font style="color:#1f2329;">特定能⼒优化：针对代码、多语⾔等领域进⾏专项优化。</font>

### LLAMA
**<font style="color:#117CEE;">简介</font>**

1. **模型架构**：  
LLaMA基于Transformer架构，这是目前许多大型语言模型的基础。它采用了改进的训练策略和技术，以提升模型的性能和效率。
2. **参数规模**：  
LLaMA提供了多个模型尺寸，包括7B、13B、30B和65B参数版本。这种多样性使用户可以根据硬件资源和应用场景的需求选择合适的模型。
3. **开放性**：  
LLaMA是开源的，Meta发布了模型及其代码，允许研究人员和开发者自由访问、修改和使用。这一举措大大促进了学术研究与行业应用之间的合作。
4. **训练数据集**：  
LLaMA使用了多元化的文本数据集进行训练，数据来源广泛，确保模型能够理解和生成多种类型的文本。
5. **<font style="color:#117CEE;">RMS Pre-Norm</font>**

**<font style="color:#117CEE;"></font>**<font style="color:#d83931;background-color:#fef1f1;">RMSNorm则不涉及均值和⽅差的计算，⽽是通过</font><u><font style="color:#d83931;background-color:#fef1f1;">均⽅根（RootMeanSquare, RMS）</font></u><font style="color:#d83931;background-color:#fef1f1;">来进⾏规范化。其核⼼思想是基于输⼊的幅值（magnitude），⽽不依赖于其均值。</font>

<font style="color:#1f2329;">LayerNorm</font><font style="color:#1f2329;">和 </font><font style="color:#1f2329;">RMSNorm</font><font style="color:#1f2329;">都是有效的正则化⽅法</font><font style="color:#1f2329;">，但它们在核⼼的计算⽅式和应⽤场景上有所</font><font style="color:#1f2329;">不同：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">LayerNorm</font><font style="color:#1f2329;">更适合处理均值与⽅差对特征影响较⼤的任务</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，特别是⼩批量数据和 </font><font style="color:#1f2329;">NLP</font><font style="color:#1f2329;">任务中。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">RMSNorm 则适⽤于幅度归⼀化为主、特征幅度较⼤的场景，如深层神经⽹络或⾼维数据中，同时它的计算效率也更⾼。</font>

6. **<font style="color:#117CEE;">激活函数SwiGLU</font>**

<font style="color:#d83931;background-color:#fef1f1;">SwiGLU激活函数作为LLaMA模型的改进之⼀，通过将GLU中的Sigmoid替换为Swish，使得模型在复杂任务中的表现得到了显著提升。其平滑的激活特性、灵活的⾮线性响应以及⻔控机制共同作⽤ ，提升了模型的表达能⼒和计算效率。</font>

7. **<font style="color:#117CEE;">RoPE旋转位置编码</font>**

<font style="color:#1f2329;">RoPE</font><font style="color:#1f2329;">的核⼼思想是将输⼊向量的每⼀维都与</font><font style="color:#1f2329;">其位置进⾏</font><font style="color:#de7802;">频率旋转</font><font style="color:#1f2329;">，这样做有以下⼏步：</font>

<font style="color:#de7802;">Query和Key的旋转：</font><font style="color:#1456f0;"> </font><font style="color:#1f2329;">对于给定的位置</font>_<font style="color:#1f2329;">m </font>_<font style="color:#1f2329;">，RoPE会根据</font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">和频率参数</font>_<font style="color:#1f2329;">θ   </font>_<font style="color:#1f2329;">对 Query 向量进⾏旋转，即乘以</font>_<font style="color:#1f2329;">e</font>__<font style="color:#1f2329;">imθ   </font>_<font style="color:#1f2329;">; Key 向量同样进⾏旋转；</font>

<font style="color:#de7802;">相对位置信息的捕捉：</font><font style="color:#1456f0;"> </font><font style="color:#1f2329;">RoPE通过将旋转操作应⽤于Query和Key，能够有效捕捉它们之间的</font><font style="color:#2ea121;">相对位置差异</font><font style="color:#1f2329;">。当计算注意⼒权重时，RoPE允许模型对相邻token之间的相对距离更加敏感，使得模型更适合⻓序列的建模。</font>

**<font style="color:#117CEE;">4、网络结构的调整与优化：</font>**

+ **<font style="color:rgb(51, 51, 51);">更深、更宽的网络</font>**<font style="color:rgb(51, 51, 51);">：LLaMA采用了更深的网络架构，增加了模型的深度，提升了模型的表达能力。同时，通过扩展网络宽度，增加了模型的并行计算能力，提升了训练效率。</font>
+ **<font style="color:rgb(51, 51, 51);">多层并行计算</font>**<font style="color:rgb(51, 51, 51);">：通过并行计算多个Transformer层，显著提升了模型的训练和推理速度，优化了计算资源的利用率。</font>
8. **<font style="color:#117CEE;">如何处理梯度消失和梯度爆炸问题?</font>**

**a. 使用残差链接**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">原理： 残差连接将每⼀层的输⼊直接添加到输出</font><font style="color:#1f2329;">，形成 </font><font style="color:#1f2329;">输出 </font><font style="color:#1f2329;">=</font><font style="color:#1f2329;">输⼊ </font><font style="color:#1f2329;">+</font><font style="color:#1f2329;">函数</font><font style="color:#1f2329;">(</font><font style="color:#1f2329;">输⼊</font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">的形式。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">效果： 提供了梯度传递的“捷径”，避免梯度在深层⽹络中过度衰减。</font><font style="color:#1456f0;"></font>

**b. 层归一化**

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">原理： 对层的输出进⾏归⼀化 ，使其均值为0 ，⽅差为1。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">效果： 稳定了激活值的分布 ，防⽌梯度爆炸 ，提⾼训练的稳定性和速度。</font>

**c. 优化的激活函数****SwiGLU**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">使⽤</font><font style="color:#1f2329;">ReLU</font><font style="color:#1f2329;">或其变体： </font><font style="color:#1f2329;">ReLU</font><font style="color:#1f2329;">函数的导数为</font><font style="color:#1f2329;">0</font><font style="color:#1f2329;">或</font><font style="color:#1f2329;">1</font><font style="color:#1f2329;">，避免了</font><font style="color:#1f2329;">Sigmoid/Tanh</font><font style="color:#1f2329;">函数导数过⼩的问题。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">效果： 防⽌梯度消失 ，加速收敛。</font>

**d. 优化器**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">使⽤⾃适应学习率优化器（如</font><font style="color:#1f2329;">Adam</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">根据梯度的⼀阶和⼆阶矩动态调整学习率。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">效果： 适应不同参数的更新需求 ，稳定训练过程。</font>

#### 如何增加中文能力（LLAMA）
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">LLAMA系列模型（如LLaMA、LLaMA-2）作为当前最流行的开源大语言模型之一，虽然在英语任务中表现优异，但其原生中文能力存在明显短板。</font>

:::

**典型模型对比**

| **项目名称** | **核心技术** | **中文BLEU-4** | **训练成本** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">Chinese-LLaMA</font> | <font style="color:rgb(51, 51, 51);">词表扩展 + 继续预训练</font> | <font style="color:rgb(51, 51, 51);">32.1</font> | <font style="color:rgb(51, 51, 51);">512 A100-day</font> |
| <font style="color:rgb(51, 51, 51);">Linly-Chinese-LLaMA</font> | <font style="color:rgb(51, 51, 51);">LoRA微调 + 指令扩充</font> | <font style="color:rgb(51, 51, 51);">28.7</font> | <font style="color:rgb(51, 51, 51);">64 A100-day</font> |
| <font style="color:rgb(51, 51, 51);">Firefly-LLaMA</font> | <font style="color:rgb(51, 51, 51);">多任务MoE架构</font> | <font style="color:rgb(51, 51, 51);">34.5</font> | <font style="color:rgb(51, 51, 51);">1024 A100-day</font> |
| <font style="color:rgb(51, 51, 51);">Ziya-LLaMA-13B</font> | <font style="color:rgb(51, 51, 51);">RLHF + 领域数据增强</font> | <font style="color:rgb(51, 51, 51);">36.2</font> | <font style="color:rgb(51, 51, 51);">2048 A100-day</font> |


**未来方向：**

1. **<font style="color:rgb(51, 51, 51);">跨语言对齐</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">探索中英联合预训练架构（如XLM-R风格）。</font>
2. **<font style="color:rgb(51, 51, 51);">文化感知</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">引入农历节日、方言等本土化知识图谱。</font>
3. **<font style="color:rgb(51, 51, 51);">高效微调</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">开发针对中文的AdaLoRA（自适应低秩适配）。</font>

:::color5
**<font style="color:#601BDE;">1.中文能力不足的原因分析</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">训练数据偏差</font>**
    - <font style="color:rgb(51, 51, 51);">原始预训练数据中</font>**<font style="color:#74B602;">中文占比不足</font>**<font style="color:rgb(51, 51, 51);">（约0.1%），且多为低质量网络爬取内容。</font>
2. **<font style="color:rgb(51, 51, 51);">分词器限制</font>**
    - <font style="color:rgb(51, 51, 51);">原版</font>**<font style="color:#74B602;">LLaMA词表（32K tokens）中汉字仅约500个</font>**<font style="color:rgb(51, 51, 51);">，覆盖不全。</font>
3. **<font style="color:rgb(51, 51, 51);">文化差异</font>**
    - <font style="color:rgb(51, 51, 51);">对中文成语、诗词、网络新词理解困难。</font>
4. **<font style="color:rgb(51, 51, 51);">任务适配不足</font>**
    - <font style="color:rgb(51, 51, 51);">未针对中文场景任务（如古文翻译、对联生成）优化。</font>

:::color5
**<font style="color:#601BDE;">2.方案1-继续预训练</font>**

:::

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：在LLaMA基础上，使用大规模中文语料继续训练，增强语言理解能力。  
</font>**<font style="color:rgb(51, 51, 51);">关键步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">数据构建</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">混合高质量中文语料（如WuDaoCorpora、CLUE、Chinese-PubMed）与原有英文数据，比例建议8:2。</font>
    - <font style="color:rgb(51, 51, 51);">加入领域数据：法律文书、医疗文献、社交媒体（需清洗）。</font>
+ **<font style="color:rgb(51, 51, 51);">训练技巧</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">分层训练</font>**<font style="color:rgb(51, 51, 51);">：只训练后1/3层参数，保留底层通用表征。</font>
    - **<font style="color:rgb(51, 51, 51);">动态掩码率</font>**<font style="color:rgb(51, 51, 51);">：中文使用15%掩码率（高于原版10%）。</font>
    - **<font style="color:rgb(51, 51, 51);">位置编码扩展</font>**<font style="color:rgb(51, 51, 51);">：从原4K上下文扩展至16K（兼容长文本任务）。</font>

**<font style="color:rgb(51, 51, 51);">案例</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">Chinese-LLaMA-Alpaca项目在13B模型上追加300B中文token训练，MMLU-CN准确率提升27%。</font>  


:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">方案2-词表扩充与优化</font>**

:::

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：扩充词表以更好支持中文分词，减少字分割带来的信息丢失。  
</font>**<font style="color:rgb(51, 51, 51);">实现方法</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">合并词表</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">将原LLaMA词表与中文专用词表（如CLUE的22K词表）合并，去重后约45K tokens。</font>
2. **<font style="color:rgb(51, 51, 51);">嵌入层初始化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">新增中文token的embedding使用相邻字向量平均初始化。</font>
3. **<font style="color:rgb(51, 51, 51);">分词器调整</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用SentencePiece重新训练分词器，设置</font>`<font style="color:rgb(51, 51, 51);">character_coverage=0.9999</font>`<font style="color:rgb(51, 51, 51);">提高生僻字支持。</font>

**<font style="color:rgb(51, 51, 51);">代码片段</font>**<font style="color:rgb(51, 51, 51);">（使用Hugging Face）：</font>

```python
from transformers import LlamaTokenizer
new_tokens = ["哔哩哔哩", "emoji", ...]  # 添加中文专用词
tokenizer = LlamaTokenizer.from_pretrained("original_llama")
tokenizer.add_tokens(new_tokens)
model.resize_token_embeddings(len(tokenizer))  # 调整模型嵌入层
```

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">方案3-指令微调</font>**

:::

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：通过高质量指令数据微调，提升任务响应能力。  
</font>**<font style="color:rgb(51, 51, 51);">数据构建</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">人工构造</font>**<font style="color:rgb(51, 51, 51);">：覆盖10类中文场景任务（如法律咨询、诗词生成）。</font>
+ **<font style="color:rgb(51, 51, 51);">自动生成</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用GPT-4翻译Alpaca-52K指令集 → 人工校验。</font>
    - <font style="color:rgb(51, 51, 51);">反向蒸馏：用Chinese-Alpaca生成结果作为训练目标。</font>

**<font style="color:rgb(51, 51, 51);">训练配置</font>**<font style="color:rgb(51, 51, 51);">：</font>

```yaml
lora_rank: 64          # LoRA低秩适配
train_batch_size: 64   # 40GB显存需求
learning_rate: 3e-5    # 低于预训练阶段
```

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">方案4-MOE 混合专家模型</font>**

:::

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：针对中英文任务动态切换专家模型。  
</font>**<font style="color:rgb(51, 51, 51);">架构设计</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">门控网络</font>**<font style="color:rgb(51, 51, 51);">：基于输入语言选择专家（如中文专家、通用专家）。</font>
+ **<font style="color:rgb(51, 51, 51);">专家结构</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">中文专家：在WanJuan-1.1T中文语料上训练。</font>
    - <font style="color:rgb(51, 51, 51);">通用专家：保留原LLaMA参数。</font>

**<font style="color:rgb(51, 51, 51);">推理加速</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">使用Triton实现动态路由，延迟增加<15%。</font>

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">方案5-RLHF</font>**

:::

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：通过人类反馈优化生成结果的中文习惯。  
</font>**<font style="color:rgb(51, 51, 51);">实现步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">奖励模型训练</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">数据：10K条中文生成结果人工标注（1-5分）。</font>
    - <font style="color:rgb(51, 51, 51);">模型：基于LLaMA-7B的奖励模型。</font>
2. **<font style="color:rgb(51, 51, 51);">PPO优化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">约束KL散度（β=0.2）防止过度偏离原始模型。</font>

**<font style="color:rgb(51, 51, 51);">效果</font>**<font style="color:rgb(51, 51, 51);">：在客服对话任务中，偏好胜率从68%提升至83%</font>

<font style="color:rgb(53, 53, 53);"></font>

<font style="color:rgb(53, 53, 53);"></font>

<font style="color:rgb(53, 53, 53);"></font>

## <font style="color:rgb(53, 53, 53);">T5（</font><font style="color:rgb(51, 51, 51);">Text-to-Text Transfer Transformer</font><font style="color:rgb(53, 53, 53);">）</font>
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





