# SFT

<!-- source: yuque://zhongxian-iiot9/hlyypb/xwz2lte5my7z7u5e -->

# <font style="color:rgb(1, 1, 1);">基础</font>
**<font style="color:#117CEE;">定义</font>**：<font style="color:#1f2329;">微调是指在预训练模型的基础上，使⽤⼩规模的标注数据针对特定任务进⾏训练，以适应具体应⽤需求。</font>

**<font style="color:#117CEE;">目的</font>**

+ <font style="color:#245bdb;">适应特定任务：：</font><font style="color:#1f2329;">使预训练模型在特定任务上达到最佳性能。</font>
+ <font style="color:#245bdb;">利用预训练知识：：</font><font style="color:#1f2329;">通过微调，模型可以在特定任务上充分发挥预训练阶段学到的知识。</font>

<font style="color:#1f2329;"></font>

# <font style="color:#1f2329;">SFT & DPO对比</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">SFT</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">是传统监督方法，依赖标注数据，简单但灵活性不足。</font>
+ **<font style="color:rgb(51, 51, 51);">DPO</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">通过偏好数据直接优化策略，无需奖励模型，适合复杂对齐任务。</font>
+ <font style="color:rgb(51, 51, 51);">实际应用中，常将 SFT 作为 DPO 的预训练阶段，结合二者优势。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理对比</font>**

:::

1. <font style="color:rgb(51, 51, 51);">SFT (监督微调)</font>
+ **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：通过人工标注的高质量样本直接调整模型参数。</font>
+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：使用交叉熵损失（Cross-Entropy Loss）最大化模型输出与标注数据的似然概率。</font>
+ **<font style="color:rgb(51, 51, 51);">优化方式</font>**<font style="color:rgb(51, 51, 51);">：基于监督学习，直接拟合输入到输出的映射关系。</font>
2. <font style="color:rgb(51, 51, 51);">DPO (直接偏好优化)</font>
+ **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：通过偏好数据（如人类对多个回答的排序）优化模型策略。</font>
+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：绕过显式奖励建模，直接通过偏好对（preference pairs）优化策略，使模型输出符合人类偏好。</font>
+ **<font style="color:rgb(51, 51, 51);">数学基础</font>**<font style="color:rgb(51, 51, 51);">：基于 Bradley-Terry 模型，将偏好概率建模为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740713547294-ec8d548a-a27b-4dd1-a91e-4f40795c8c87.png)

<font style="color:rgb(51, 51, 51);">其中，π</font><sub><font style="color:rgb(51, 51, 51);">ref</font></sub><font style="color:rgb(51, 51, 51);">是参考策略（如 SFT 后的模型），π</font><sub><font style="color:rgb(51, 51, 51);">new</font></sub><font style="color:rgb(51, 51, 51);"> 是待优化策略，β</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是温度参数。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤对比</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">SFT 步骤</font>**
    1. **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：标注数据</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740713756449-028dd1a9-8c1a-4212-9993-983f3cdb200e.png)<font style="color:rgb(51, 51, 51);">。</font>
    2. **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740713761924-713fd340-fcbc-4a02-b358-58680498f86a.png)
    3. **<font style="color:rgb(51, 51, 51);">优化</font>**<font style="color:rgb(51, 51, 51);">：通过梯度下降直接最小化损失。</font>
2. **<font style="color:rgb(51, 51, 51);">DPO 步骤</font>**
    1. **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：偏好数据 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740713768921-3045dace-0710-41ed-8737-e69542b7f93c.png)<font style="color:rgb(51, 51, 51);">，其中 y</font><sub><font style="color:rgb(51, 51, 51);">w</font></sub><font style="color:rgb(51, 51, 51);">是优选回答，y</font><sub><font style="color:rgb(51, 51, 51);">l</font></sub><font style="color:rgb(51, 51, 51);">是次选回答。</font>
    2. **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740713776860-f755b242-2ef4-43d1-94ab-f71153ca30be.png)

<font style="color:rgb(51, 51, 51);">其中 σ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是 Sigmoid 函数。</font>

    3. **<font style="color:rgb(51, 51, 51);">优化</font>**<font style="color:rgb(51, 51, 51);">：通过梯度下降调整 πθ</font>_<font style="color:rgb(51, 51, 51);">πθ</font>_<font style="color:rgb(51, 51, 51);">，使其更倾向于生成优选回答。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点对比</font>**

:::

| **方法** | **优点** | **缺点** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">SFT</font>** | <font style="color:rgb(51, 51, 51);">1. 实现简单，训练稳定   </font><font style="color:rgb(51, 51, 51);">2. 需要标注数据量较少</font> | <font style="color:rgb(51, 51, 51);">1. 依赖高质量标注数据   </font><font style="color:rgb(51, 51, 51);">2. 无法直接利用偏好反馈</font> |
| **<font style="color:rgb(51, 51, 51);">DPO</font>** | <font style="color:rgb(51, 51, 51);">1. 直接优化人类偏好，无需奖励模型   </font><font style="color:rgb(51, 51, 51);">2. 训练效率更高</font> | <font style="color:rgb(51, 51, 51);">1. 需要大量偏好数据   </font><font style="color:rgb(51, 51, 51);">2. 对参考策略 π</font><sub><font style="color:rgb(51, 51, 51);">ref </font></sub><font style="color:rgb(51, 51, 51);">敏感</font> |


:::color5
**<font style="color:#601BDE;">4.应用场景对比</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">SFT</font>**<font style="color:rgb(51, 51, 51);">：适用于有明确标注答案的任务，如分类、摘要、翻译等。</font>
+ **<font style="color:rgb(51, 51, 51);">DPO</font>**<font style="color:rgb(51, 51, 51);">：适用于需要对齐人类偏好的场景，如对话生成、内容安全过滤、创意写作等。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">SFT 改进</font>**
    - **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：通过回译、加噪等方法扩大标注数据。</font>
    - **<font style="color:rgb(51, 51, 51);">课程学习</font>**<font style="color:rgb(51, 51, 51);">：从简单样本到复杂样本逐步训练。</font>
2. **<font style="color:rgb(51, 51, 51);">DPO 改进</font>**
    - **<font style="color:rgb(51, 51, 51);">混合训练</font>**<font style="color:rgb(51, 51, 51);">：结合 SFT 和 DPO 分阶段优化。</font>
    - **<font style="color:rgb(51, 51, 51);">动态参考策略</font>**<font style="color:rgb(51, 51, 51);">：在训练中更新 π</font><sub><font style="color:rgb(51, 51, 51);">ref</font></sub><font style="color:rgb(51, 51, 51);"> 以避免策略偏移。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
from transformers import AutoModelForCausalLM, AdamW

model = AutoModelForCausalLM.from_pretrained("gpt2")
optimizer = AdamW(model.parameters(), lr=1e-5)

# 假设 inputs 是 tokenized 输入，labels 是目标输出
inputs = tokenizer("Prompt: Hello", return_tensors="pt")
labels = tokenizer("Response: Hi there!", return_tensors="pt")["input_ids"]

outputs = model(**inputs, labels=labels)
loss = outputs.loss
loss.backward()
optimizer.step()

```

```python
def dpo_loss(pi_logits, ref_logits, yw_id, yl_id, beta=0.1):
    # 计算优选和次选回答的对数概率
    log_pi_yw = torch.log_softmax(pi_logits, dim=-1)[:, yw_id]
    log_ref_yw = torch.log_softmax(ref_logits, dim=-1)[:, yw_id]
    log_pi_yl = torch.log_softmax(pi_logits, dim=-1)[:, yl_id]
    log_ref_yl = torch.log_softmax(ref_logits, dim=-1)[:, yl_id]

    # 计算损失
    ratio_yw = log_pi_yw - log_ref_yw
    ratio_yl = log_pi_yl - log_ref_yl
    loss = -torch.log(torch.sigmoid(beta * (ratio_yw - ratio_yl)))
    return loss.mean()

# 初始化参考模型和优化模型
pi_model = AutoModelForCausalLM.from_pretrained("sft-model")
ref_model = AutoModelForCausalLM.from_pretrained("sft-model").eval()
optimizer = AdamW(pi_model.parameters(), lr=1e-5)

# 计算损失并反向传播
pi_logits = pi_model(input_ids).logits
with torch.no_grad():
    ref_logits = ref_model(input_ids).logits
loss = dpo_loss(pi_logits, ref_logits, yw_id, yl_id)
loss.backward()
optimizer.step()

```

# SFT数据问题
## 数据配比
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



## 数据合成
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">监督式微调（SFT）数据合成的核心目标是通过人工或自动化手段生成高质量的训练样本，用于调整预训练语言模型（如GPT、LLaMA等），使其适应特定任务。其核心原理包括：</font>

1. **<font style="color:rgb(51, 51, 51);">任务对齐</font>**<font style="color:rgb(51, 51, 51);">：合成数据需覆盖目标任务的输入-输出模式，确保分布匹配。</font>
2. **<font style="color:rgb(51, 51, 51);">多样性生成</font>**<font style="color:rgb(51, 51, 51);">：通过模板、规则或模型生成多样化样本，避免过拟合。</font>
3. **<font style="color:rgb(51, 51, 51);">质量验证</font>**<font style="color:rgb(51, 51, 51);">：结合自动过滤和人工审核，确保数据的准确性和合理性。</font>

:::

<font style="color:rgb(51, 51, 51);">常用方法：</font>

+ **<font style="color:rgb(51, 51, 51);">模板填充</font>**<font style="color:rgb(51, 51, 51);">：设计结构化模板，填充动态内容（如实体、关键词）。</font>
+ **<font style="color:rgb(51, 51, 51);">反向生成</font>**<font style="color:rgb(51, 51, 51);">：先定义输出，再生成输入（如给定答案生成问题）。</font>
+ **<font style="color:rgb(51, 51, 51);">模型蒸馏</font>**<font style="color:rgb(51, 51, 51);">：利用大模型生成候选数据（如用GPT-4生成问答对）。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 任务定义与模板设计</font>**

+ <font style="color:rgb(51, 51, 51);">确定任务类型（分类、生成、问答等）。</font>
+ <font style="color:rgb(51, 51, 51);">设计模板库（如分类任务模板：</font>`<font style="color:rgb(51, 51, 51);">"文本：{text} 类别：{label}"</font>`<font style="color:rgb(51, 51, 51);">）。</font>

**<font style="color:rgb(51, 51, 51);">2. 数据生成</font>**

+ **<font style="color:rgb(51, 51, 51);">模板填充法</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
python


templates = ["关于{topic}的正面评论：{text}", "讨论{topic}的缺点：{text}"]
topics = ["环保", "科技"]
for template in templates:
    for topic in topics:
        text = generate_text(topic)  # 调用模型生成或人工编写
        data.append(template.format(topic=topic, text=text))
```

+ **<font style="color:rgb(51, 51, 51);">模型生成法</font>**<font style="color:rgb(51, 51, 51);">（以GPT为例）：</font>

```plain
python


prompt = "生成一个关于机器学习的问答对："
response = openai.Completion.create(prompt=prompt, max_tokens=100)
question, answer = parse_response(response)
```

**<font style="color:rgb(51, 51, 51);">3. 数据过滤</font>**

+ **<font style="color:rgb(51, 51, 51);">规则过滤</font>**<font style="color:rgb(51, 51, 51);">：去除重复、含敏感词样本。</font>
+ **<font style="color:rgb(51, 51, 51);">模型打分</font>**<font style="color:rgb(51, 51, 51);">：使用预训练模型计算生成数据的困惑度（Perplexity），过滤高困惑度样本。</font>

**<font style="color:rgb(51, 51, 51);">4. 人工验证</font>**

+ <font style="color:rgb(51, 51, 51);">对10%~20%的数据进行人工标注，确保质量。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 成本低，无需大量标注人力</font> | <font style="color:rgb(51, 51, 51);">1. 生成数据可能存在分布偏差</font> |
| <font style="color:rgb(51, 51, 51);">2. 可快速扩展数据规模</font> | <font style="color:rgb(51, 51, 51);">2. 多样性依赖模板或生成模型性能</font> |
| <font style="color:rgb(51, 51, 51);">3. 支持长尾场景覆盖</font> | <font style="color:rgb(51, 51, 51);">3. 需额外质量验证步骤</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">低资源任务</font>**<font style="color:rgb(51, 51, 51);">：如小语种翻译、医疗领域问答。</font>
2. **<font style="color:rgb(51, 51, 51);">复杂输出结构</font>**<font style="color:rgb(51, 51, 51);">：需特定格式的文本生成（如SQL查询、代码生成）。</font>
3. **<font style="color:rgb(51, 51, 51);">对抗过拟合</font>**<font style="color:rgb(51, 51, 51);">：在数据量少时补充多样性样本。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合真实数据</font>**<font style="color:rgb(51, 51, 51);">：按比例混合合成数据与真实数据（如7:3）。</font>
2. **<font style="color:rgb(51, 51, 51);">强化学习反馈</font>**<font style="color:rgb(51, 51, 51);">：使用RLHF（人类反馈强化学习）优化生成策略。</font>
3. **<font style="color:rgb(51, 51, 51);">动态模板扩充</font>**<font style="color:rgb(51, 51, 51);">：基于聚类发现新模板模式。</font>
4. **<font style="color:rgb(51, 51, 51);">多模型协作</font>**<font style="color:rgb(51, 51, 51);">：使用多个模型交叉验证生成结果。</font>
+ **<font style="color:rgb(51, 51, 51);">多样性增强</font>**<font style="color:rgb(51, 51, 51);">：在模板中引入同义词替换（使用WordNet或BERT-Embedding）。</font>
+ **<font style="color:rgb(51, 51, 51);">质量控制</font>**<font style="color:rgb(51, 51, 51);">：训练二分类器区分真实/合成数据，过滤低置信度样本。</font>
+ **<font style="color:rgb(51, 51, 51);">迭代生成</font>**<font style="color:rgb(51, 51, 51);">：使用当前微调模型生成新数据，逐步提升难度。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import random
from transformers import pipeline

# 1. 模板生成示例
templates = [
    "解释以下概念：{concept}",
    "{concept}的定义是什么？"
]
concepts = ["量子计算", "神经网络"]

synthetic_data = []
for template in templates:
    for concept in concepts:
        synthetic_data.append(template.format(concept=concept))

# 2. 使用模型生成答案
generator = pipeline('text-generation', model='gpt2')
synthetic_qa = []

for item in synthetic_data:
    response = generator(item, max_length=100, num_return_sequences=1)
    answer = response[0]['generated_text'].split('\n')[0]
    synthetic_qa.append({'question': item, 'answer': answer})

# 3. 过滤低质量数据（简单版）
def filter_data(qa_pair, perplexity_threshold=50):
    # 假设已实现困惑度计算函数
    ppl = calculate_perplexity(qa_pair['answer'])
    return ppl < perplexity_threshold

filtered_data = [item for item in synthetic_qa if filter_data(item)]

```



# MLLM指令数据合成
## MM-EVOL <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>[<font style="color:rgb(9, 64, 142);">多模态大型语言模型</font>](https://zhida.zhihu.com/search?content_id=249409586&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E5%9E%8B%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> (MLLMs) 的发展在各个领域（例如多模态代理、具身智能）的日益增长的需求推动下取得了重大进展。 尽管模型驱动的方法试图通过不同的架构来增强 MLLMs 的能力，但其收益已变得越来越微不足道。 相反，数据驱动的方法通过扩展图像文本指令数据来提升效率，但面临着数据多样性和复杂性有限的挑战。 </font>**<font style="color:#74B602;">高质量数据的缺乏构成了 MLLMs 发展的一大障碍。</font>**

<font style="color:rgb(25, 27, 31);">对现有的用于生成图像-文本指令数据的基于数据的分析方法的分析揭示了三个常见的局限性：</font>

1. **<font style="color:#2F4BDA;">指令多样性有限</font>**<font style="color:rgb(25, 27, 31);">： 手动标注的指令受限于标注者的认知能力，而模型生成的指令受限于模板预设，难以满足现实世界中各种任务需求。 这限制了MLLMs的指令遵循能力。 </font>
2. **<font style="color:#2F4BDA;">指令复杂度有限</font>**<font style="color:rgb(25, 27, 31);">：手动标注通常会导致简单或中等复杂度的指令，而自动生成的指令往往简短且缺乏视觉推理步骤，这限制了模型处理复杂任务的能力。</font>
3. **<font style="color:#2F4BDA;">对齐粒度不足</font>**<font style="color:rgb(25, 27, 31);">： 手动和模型生成的指令都主要关注常见物体，而忽略了稀有或小物体，导致图像-文本对齐的粒度有限。 这会影响模型的视觉感知鲁棒性和对幻觉的抵抗力。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">MMEvol</font>](https://zhida.zhihu.com/search?content_id=249409586&content_type=Article&match_order=1&q=MMEvol&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，一个新颖的</font>**<font style="color:#ED740C;">多模态指令数据演化框架</font>**<font style="color:rgb(25, 27, 31);">。 该框架通过细粒度感知、认知推理和交互演化的精细组合迭代地提高数据质量，生成更复杂和多样化的图像文本指令数据集，从而赋予 MLLMs 更强的能力。</font>

<font style="color:rgb(25, 27, 31);">《</font><font style="color:rgb(25, 25, 25);">MMEvol: Empowering Multimodal Large Language Models with Evol-Instruct</font><font style="color:rgb(25, 27, 31);">》</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://arxiv.org/pdf/2409.05840](https://arxiv.org/pdf/2409.05840)

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://mmevol.github.io/](https://mmevol.github.io/)

**参考：**[**https://zhuanlan.zhihu.com/p/1936308162**](https://zhuanlan.zhihu.com/p/1936308162)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239062356-d7a7ec94-0b13-42f6-ab57-5be7a0c4b172.png)

<font style="color:rgb(25, 27, 31);">图 1: MMEvol 概述。 指令演化和指令消除通过多轮协同合作，以增强</font>**<font style="color:#74B602;">指令数据的多样性和复杂性。</font>**

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">设计了一个</font>**<font style="color:#74B602;">图像文本指令进化框架，MMEvol</font>**<font style="color:rgb(25, 27, 31);">，以利用先进的 MLLM，自动生成跨不同难度级别的开放域图像文本指令数据，以增强现有数据集的多样性和复杂性。</font>
2. <font style="color:rgb(25, 27, 31);">通过利用指令进化数据，构建了一个</font>**<font style="color:#74B602;">高质量的数据配方</font>**<font style="color:rgb(25, 27, 31);">，并且进化后的数据将被发布，以进一步提升其他开源 MLLM 的能力。</font>
3. <font style="color:rgb(25, 27, 31);">我们使用这种高质量的数据配方训练了一个 MLLM，与其他完全开源的方法相比，在各种下游视觉语言任务中取得了优异的性能。</font>
4. <font style="color:rgb(25, 27, 31);">通过大量的定性和定量分析验证了所提出方法的有效性和效率。</font>

:::color5
**<font style="color:#601BDE;">2.MM-Evol 概述</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">MM-Evol中每个演化周期包含两个主要步骤：</font>**<font style="color:#74B602;">指令演化和指令消除</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">指令演化</font>**<font style="color:rgb(25, 27, 31);">：随机选择</font>**<font style="color:#74B602;">细粒度感知演化、认知推理演化或交互演化之一</font>**<font style="color:rgb(25, 27, 31);">，将简单的指令升级为更复杂或更多样化的指令。 </font>
    - **<font style="color:rgb(25, 27, 31);">细粒度感知演化</font>**<font style="color:rgb(25, 27, 31);">：旨在利用图像中的视觉信息来生成包含</font>**<font style="color:#ECAA04;">更详细信息的数据</font>**
    - **<font style="color:rgb(25, 27, 31);">认知推理演化</font>**<font style="color:rgb(25, 27, 31);">：延长了指令的视觉操作推理步骤以</font>**<font style="color:#ECAA04;">增加其复杂性</font>**
    - **<font style="color:rgb(25, 27, 31);">交互演化</font>**<font style="color:rgb(25, 27, 31);">：旨在通过提供更多样化的指令形式来增强</font>**<font style="color:#ECAA04;">指令多样性</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">指令消除</font>**<font style="color:rgb(25, 27, 31);">：为了解决演化指令中偶尔出现的错误，我们使用</font>**<font style="color:#ECAA04;">指令消除来过滤掉失败的演化</font>**<font style="color:rgb(25, 27, 31);">。 MMEvol 重复指令演化和消除过程多次，以获得包含各种指令形式的复杂指令数据集。</font>

:::color5
**<font style="color:#601BDE;">3.种子指令：SEED-163K</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239368945-81646069-61a7-4688-a782-fc749623449c.png)

<font style="color:rgb(25, 27, 31);">种子指令数据</font>**<font style="color:#601BDE;">SEED-163K</font>**<font style="color:rgb(25, 27, 31);">是从 </font>**<font style="color:#74B602;">LLaVA-Instruct和 ShareGPT4V </font>**<font style="color:rgb(25, 27, 31);">数据集中整理而来，并补充了从 </font>[<font style="color:rgb(9, 64, 142);">Cambrain-1</font>](https://zhida.zhihu.com/search?content_id=249409586&content_type=Article&match_order=1&q=Cambrain-1&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 中抽取的额外科学和图表数据。 此过程涉及仔细选择和优化，以确保指令的质量和多样性。 对于只有标题的指令，我们使用 OpenAI GPT-4o mini API 来生成种子指令数据。 最终，在合并和过滤后，我们获得了包含 163K 个具有独特图像的指令样本的综合数据集，它为我们后续的 Evol-Instruct 奠定了基础。</font>

<font style="color:rgb(25, 27, 31);">为了验证MMEvol的有效性，我们</font>**<font style="color:#74B602;">对 163K 个种子数据进行了三轮演化迭代，产生了 447K 个演化样本</font>**<font style="color:rgb(25, 27, 31);">。 我们使用这些演化数据微调了开源的 LLaVA-NeXT 模型，并在 13 个视觉语言基准测试中与其他先进方法进行了比较。 我们的方法取得了最先进 (SOTA) 的性能，证明了MMEvol的有效性和效率。</font>

:::color5
**<font style="color:#601BDE;">4.MM-Evol 的前缀提示</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239674172-1559cd3c-f01f-4e68-987c-16cad43d7fff.png)

<font style="color:rgb(25, 27, 31);">MM-Evol 的前缀提示。 </font>

**<font style="color:rgb(25, 27, 31);">顶部块</font>**<font style="color:rgb(25, 27, 31);">：展示了上下文，例如标题和视觉对象位置</font>

**<font style="color:rgb(25, 27, 31);">中间块</font>**<font style="color:rgb(25, 27, 31);">：展示了以视觉/语言为中心的原子命题和演化目标。 此外，我们通过伪函数调用赋予视觉能力，以增强进化过程中的视觉推理。 </font>

**<font style="color:rgb(25, 27, 31);">底部块</font>**<font style="color:rgb(25, 27, 31);">：进一步阐明了组织好的种子样本，这些样本随后被发送到 MLLM 进行重写。</font>

:::color5
**<font style="color:#601BDE;">5.细粒度感知进化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239762135-54344b49-ad3c-4256-842a-c1720fd26ccf.png)

<font style="color:rgb(25, 27, 31);">细粒度感知进化提示和数据示例。 细粒度感知进化可以生成包含</font>**<font style="color:#74B602;">更详细视觉信息的样本</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#74B602;">增强数据多样性</font>**<font style="color:rgb(25, 27, 31);">，这些样本以不同的颜色标记以更好地可视化。</font>

:::color5
**<font style="color:#601BDE;">6.认知推理进化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239791960-a268ea5d-28e2-45f7-a6b8-7b81caed5b20.png)

<font style="color:rgb(25, 27, 31);">认知推理进化提示模板和示例。 认知推理进化可以使</font>**<font style="color:#74B602;">指令数据拥有更长的视觉推理链</font>**<font style="color:rgb(25, 27, 31);">，从而增加</font>**<font style="color:#74B602;">数据的复杂性</font>**<font style="color:rgb(25, 27, 31);">。 我们使用不同的颜色突出显示更改以更好地可视化。</font>

:::color5
**<font style="color:#601BDE;">7.交互式演化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239842448-4e157893-d635-424a-8980-aef3486fb817.png)

<font style="color:rgb(25, 27, 31);">交互式演化提示模板和示例。 交互式演化可以</font>**<font style="color:#74B602;">自动生成各种类型的非预定义指令格式，显著提高数据的多样性</font>**<font style="color:rgb(25, 27, 31);">。 使用不同的颜色突出显示差异，以更好地可视化。</font>

:::color5
**<font style="color:#601BDE;">8.指令消除 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239891467-0c712b0f-4d8a-4076-a414-ca10ea725649.png)

<font style="color:rgb(25, 27, 31);">指令消除提示模板。 指令消除用于计算指令数据的演化增益和复杂度水平。 我们根据演化增益</font>**<font style="color:#74B602;">过滤掉无法演化的有害数据。</font>**

:::color5
**<font style="color:#601BDE;">9.质量评测 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **技能长度对比 & 推理步骤长度对比 & 复杂度对比****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743240228209-fca84cfd-1acf-4024-875b-1bcfe891a91f.png)

图9 (a) 种子数据和我们进化后的数据之间的技能长度分布；(b) 种子数据和我们进化后的数据之间的推理步骤长度分布；(c) 种子数据和我们进化后的数据之间的难度和复杂度水平分布。

<font style="color:rgb(25, 27, 31);">我们从种子数据中随机抽取 30K 个数据点，并在演化前后对指令数据进行定性分析。 如 </font>[图 ](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10)<font style="color:rgb(25, 27, 31);">9 所示，进化后的数据明显更复杂。 具体来说，每个进化后的指令在 </font>[图 9(a)](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10.sf1)<font style="color:rgb(25, 27, 31);"> 中涉及 0.68 个更多的原子能力，并且与进化前相比，在 </font>[图 9(b)](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10.sf2)<font style="color:rgb(25, 27, 31);"> 中，其平均视觉操作链推理长度长 0.86。 如 </font>[图 9(c)](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10.sf3)<font style="color:rgb(25, 27, 31);"> 所示，每个演化轮次的</font>**<font style="color:#74B602;">平均难度得分呈递增趋势</font>**<font style="color:rgb(25, 27, 31);">，这表明认知推理演化在提高指令数据复杂性方面是有效的。</font>

2. **多样性对比（根动词和其直接名词宾语）****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743240061516-3d11c6e0-5781-4376-881f-ca19d654d841.png)

图 10: (a) 中种子数据的根动词（内圈）及其顶层名词宾语（外圈）和 (b) 中演化后的数据的根动词及其顶层名词宾语。

<font style="color:rgb(25, 27, 31);">我们识别生成的指令中的动词-名词结构，以研究生成的指令类型和演化数据的多样性。 我们使用 Berkeley 神经解析器 解析指令，</font>**<font style="color:#74B602;">提取最靠近根的动词及其第一个直接名词宾语</font>**<font style="color:rgb(25, 27, 31);">。 </font>[图 ](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F9)<font style="color:rgb(25, 27, 31);">10绘制了数量超过 2K 的根动词及其直接宾语。 我们观察到，与演化前相比，</font>**<font style="color:#74B602;">演化后的数据显着提高了指令多样性，演化后的指令具有不同的意图和文本格式。</font>**<font style="color:rgb(25, 27, 31);"> </font>

3. **长尾视觉对象****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743240413814-daae1938-ae60-46a2-9dba-4e15a3da160a.png)

<font style="color:rgb(25, 27, 31);">图 11： 种子数据和进化数据之间 200 个视觉对象的 长尾分布。 MMEvol 显着改善了种子数据中视觉对象的 长尾分布，提供了更细粒度的视觉信息，从而提高了模型的泛化能力和抵抗幻觉的能力。</font>

<font style="color:rgb(25, 27, 31);">此外，我们对演化前后指令数据中的视觉对象域进行了长尾分布可视化分析，以验证细粒度感知演化的有效性。</font>[图 11](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F11)<font style="color:rgb(25, 27, 31);"> 显示，细粒度的感知演化极大地</font>**<font style="color:#74B602;">改善了长尾视觉对象的分布</font>**<font style="color:rgb(25, 27, 31);">，最大限度地从图像中提取可用的视觉信息，细化指令数据中图像-文本对齐的粒度，增强数据多样性，从而提高模型泛化能力并减少视觉幻觉。</font>

## STaR**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">STaR旨在解决如何提高语言模型在复杂推理任务上的性能，例如数学问题解答或常识问答。STaR（Self-Taught Reasoner）算法的原理是通过迭代地利用少量推理示例（rationales）和大量没有推理的大数据集，来引导模型逐步提升执行更复杂推理的能力。STaR算法的核心是一个简单的循环过程。</font>

**paper：**[**STaR: Self-Taught Reasoner Bootstrapping Reasoning With Reasoning**](https://arxiv.org/pdf/2203.14465)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058832190-3fe2056a-2c4d-41bf-b16e-603f95cfae05.png)

:::color5
**<font style="color:#601BDE;">1.STaR步骤 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058931163-f7d26519-849a-45b0-aaed-a33cc528406c.png)

:::color5
**<font style="color:#601BDE;">2.评估 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">算术（Arithmetic）</font>**<font style="color:rgb(25, 27, 31);">：验证模型在解决不同位数的加法问题上的性能。STaR显著提高了模型在多位数加法问题上的准确率。特别是引入合理化（rationalization）步骤后，模型的性能提升更为显著。</font>
2. **<font style="color:rgb(25, 27, 31);">常识推理（Commonsense Reasoning）</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">CommonsenseQA</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=CommonsenseQA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（CQA）数据集，评估模型在多项选择常识问题上的表现。在CommonsenseQA数据集上，STaR在开发集上的准确率超过了仅使用少量样本提示的基线（增加了35.9%），并且与直接预测答案的基线相比也有显著提升（增加了12.5%）。当与比STaR模型大30倍的模型相比时，STaR的性能与之相当（72.5% vs 73.0%）。</font>
3. **<font style="color:rgb(25, 27, 31);">小学数学（Grade School Math）</font>**<font style="color:rgb(25, 27, 31);">：利用</font>[<font style="color:rgb(9, 64, 142);">GSM8K</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=GSM8K&zhida_source=entity)<font style="color:rgb(25, 27, 31);">数据集，测试模型解决自然语言表述的数学问题的能力。STaR显著提高了模型在GSM8K数据集上的性能，即使训练数据较少（无合理化的模型使用了25.0%的数据，合理化的模型使用了28.7%的数据）。</font>





## Dyn-VQA（OmniSearch）**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：OmniSearch 是阿里巴巴通义实验室推出的一款</font>**<font style="color:#ED740C;">多模态检索增强生成框架</font>**<font style="color:rgb(51, 51, 51);">，具备自适应规划能力。OmniSearch 能够动态拆解复杂问题，根据检索结果和问题情境调整检索策略，模拟人类在解决复杂问题时的行为方式，从而提升检索效率和准确性。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">paper</font>**<font style="color:rgba(0, 0, 0, 0.9);">:</font>[https://arxiv.org/pdf/2411.02937](https://arxiv.org/pdf/2411.02937)

:::

:::color5
**<font style="color:#601BDE;">1.基于OmniSearch的VQA示例 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

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
**<font style="color:#601BDE;">2.动态问答数据集：Dyn-VQA  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

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



## LLaVAR**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：基于LLAVA的文档理解多模态大模型</font>

<font style="color:rgb(51, 51, 51);">《</font><font style="color:rgb(54, 54, 54);">LLaVAR: Enhanced Visual Instruction Tuning for Text-rich Image Understanding</font><font style="color:rgb(51, 51, 51);">》</font>

:::

:::color5
**<font style="color:#601BDE;">1.训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

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
**<font style="color:#601BDE;">2.VQA指令数据构建示例 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

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



## Florence-2 **<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51) !important;">Florence-2模型：</font>**<font style="color:#ED740C;">一种新颖的开源视觉语言模型（VLM），旨在处理各种视觉和多模型任务，包括字幕识别、对象检测、分割和OCR等内容。</font>**

:::

:::color5
**<font style="color:#601BDE;">1.训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">为了训练Florence-2模型，研究人员需要一个全面、大规模、高质量的多任务数据集，覆盖了各种图像数据。鉴于这种数据的稀缺性，他们由此创建了全新的多任务图像数据集——FLD-5B。</font>

<font style="color:rgb(51, 51, 51);">这一数据集中包含了1.26亿张图像、5亿个文本标注、13亿个文本-图像区域标注，以及36亿个文本短语-图像区域标注，跨横跨了不同的任务。</font>

**<font style="color:rgb(51, 51, 51);">数据格式</font>**

<font style="color:rgb(51, 51, 51) !important;">受大型语言模型的启发，Florence-2被设计为一种序列到序列的模型。它将图像和文本指令作为输入，并输出文本结果。输入或输出文本可以表示纯文本或图像中的区域。区域格式因任务而异：</font>

+ <font style="color:rgb(51, 51, 51) !important;">边界框：“<X1><Y1><X2><Y2>”用于对象检测任务。这些标记表示长方体左上角和右下角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">四边框：“<X1><Y1><X2><Y2><X3><Y3><X4><Y4>”用于文本检测，使用包围文本的四个角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">多边形：“<X1><Y1><Xn><Yn>'用于分割任务，其中坐标按顺时针顺序表示多边形的顶点。</font>

:::color5
**<font style="color:#601BDE;">2.数据pipeline </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">Florence-2数据引擎一共包含三个重要环节：</font>

<font style="color:rgb(51, 51, 51);">1) 使用专业模型进行初始标注</font>

<font style="color:rgb(51, 51, 51);">2) 数据过滤，纠正错误并移除无关标注</font>

<font style="color:rgb(51, 51, 51);">3) 迭代式的数据优化过程</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340588984-846de6c7-1166-4d52-8b0a-204334b652c6.png)

<font style="color:rgb(51, 51, 51);">FLD-5B中的每一张图像都由Florence数据引擎标注了文本、图像区域-文本对以及文本短语-图像区域三元组，涵盖了多个空间层次、从概括到详细的渐进粒度，以及多语义，让模型从不同角度实现了更全面的视觉理解能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340643905-62b28ba5-47b7-4fac-a796-6fa3685c0554.png)



## internVL-2.5**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">InternVL 2.5</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=InternVL+2.5&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，这是一种先进的大规模多模态大模型系列，基于InternVL 2.0的基础架构。InternVL系列的目标是缩小商业闭源模型与开源多模态模型之间的性能差距。在InternVL 2.5中，他们系统地探索了多模态大模型中的各种因素，包括</font>[<font style="color:rgb(9, 64, 142);">视觉编码器</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、语言模型、</font>[<font style="color:rgb(9, 64, 142);">数据集规模</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A7%84%E6%A8%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和推理时间的变化如何影响模型的整体性能，从而展示了多模态模型中扩展与性能之间的关系。</font>

**参考：**[**https://zhuanlan.zhihu.com/p/12309812997**](https://zhuanlan.zhihu.com/p/12309812997)

:::

:::color5
**<font style="color:#601BDE;">1.预训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了全面提升模型的性能并增强其处理复杂任务的能力，InternVL 2.5的训练数据集比InternVL 1.5和2.0更广泛且多样化。模型开发期间，专门使用对话格式的指令数据。在这一阶段，由于只有MLP或MLP和ViT的参数是可训练的，因此会</font>**<font style="color:rgb(25, 27, 31);">结合高质量和低质量的数据。</font>**<font style="color:rgb(25, 27, 31);">目标是通过接触多样的领域数据来丰富模型的世界知识，从而提高其泛化能力。训练语料库涵盖了</font>**<font style="color:#74B602;">字幕生成、通用问答、数学、图表、OCR、知识、定位、文档、对话、医疗和GUI任务等领域。</font>**

:::color5
**<font style="color:#601BDE;">2.微调数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">从InternVL 1.5到2.0再到2.5，数据集在规模、质量和多样性上进行了迭代改进。数据规模方面，样本数量从InternVL 1.5的510万增长到InternVL 2.0的730万，并在InternVL 2.5中进一步翻倍至</font>**<font style="color:#74B602;">1630万</font>**<font style="color:rgb(25, 27, 31);">。在多样性方面，训练数据涵盖多个领域，包括</font>**<font style="color:#74B602;">通用问答、图表、文档、OCR、科学、医疗、GUI、代码、数学等，同时覆盖多种模态，如单图像、多图像、视频和文本。</font>**

<font style="color:rgb(25, 27, 31);">在InternVL 2.5中，</font>**<font style="color:#74B602;">单图像数据占据了45.92%的标记，多图像数据占9.37%，视频数据贡献了39.79%，纯文本数据占4.92%</font>**<font style="color:rgb(25, 27, 31);">。与早期版本相比，多图像和视频数据的增加最为显著，增强了InternVL 2.5对多图像和长视频的理解能力。质量提升通过统一对话模板、使用语言模型评分和精炼数据、去除重复模式、应用启发式规则过滤低质量样本，以及将短响应重写为高质量和更长的交互来实现。这确保了模型训练的稳健数据集。</font>

:::color5
**<font style="color:#601BDE;">3.数据处理pipeline </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742720896544-874e4e03-d4d1-4892-b359-9c4e86630891.png)

<font style="color:rgb(25, 27, 31);">在模型开发过程中，观察到</font>**<font style="color:#74B602;">LLM对数据噪声的敏感性显著高于视觉编码器</font>**<font style="color:rgb(25, 27, 31);">。即使是少量异常样本（例如，离群值或重复数据，仅数千个）也会在推理期间导致模型行为异常。</font>

<font style="color:rgb(25, 27, 31);">在这些异常中，</font>**<font style="color:#74B602;">重复生成</font>**<font style="color:rgb(25, 27, 31);">被识别为最具破坏性的问题之一。在许多开源或合成数据集中，仅仅数千个重复样本就会导致模型陷入重复循环，尤其是在长篇输出或CoT推理任务中。这种现象削弱了测试时缩放策略的有效性。为应对这一挑战并支持未来研究，我们设计了一种高效的数据过滤管道，以去除低质量样本，从而最大限度地减少重复生成的风险。</font>

**<font style="color:rgb(25, 27, 31);">数据过滤pipeline</font>**<font style="color:rgb(25, 27, 31);">：由两个模块组成。对于纯文本数据，实施了三种关键策略：</font>

1. **<font style="color:rgb(25, 27, 31);">基于LLM的质量评分</font>**<font style="color:rgb(25, 27, 31);">：首先将数据集分类为不同领域，低于指定阈值的样本被移除以确保数据质量。</font>
2. **<font style="color:rgb(25, 27, 31);">重复检测</font>**<font style="color:rgb(25, 27, 31);">：使用LLM结合特定提示识别重复样本。这些样本经过人工审查，低于阈值的样本被移除以保持数据质量。</font>
3. **<font style="color:rgb(25, 27, 31);">启发式规则过滤</font>**<font style="color:rgb(25, 27, 31);">：应用特定规则，如过滤掉异常长度的句子、过长的零序列、过多重复行的文本等，以识别数据中的异常。尽管这种方法可能偶尔产生误报，但它提高了异常样本的检测率。所有标记样本在最终移除前都经过人工审查。</font>

## Qwen2.5**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">最近，团队发布了 Qwen 系列的最新版本 </font>**<font style="color:rgb(25, 27, 31);">Qwen2.5</font>**<font style="color:rgb(25, 27, 31);">。在开源部分，他们发布了7种不同规模的预训练和指令微调模型，包括</font>**<font style="color:rgb(25, 27, 31);">0.5B、1.5B、3B、7B、14B、32B</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">72B</font>**<font style="color:rgb(25, 27, 31);">，并提供了原始模型（bfloat16 精度）及不同精度的量化版本。</font>

**paper：**[**https://arxiv.org/pdf/2412.15115**](https://arxiv.org/pdf/2412.15115)

**参考：**[**【LLM技术报告】Qwen2.5技术报告（全文）**](https://zhuanlan.zhihu.com/p/13936916587)

:::

:::color5
**<font style="color:#601BDE;">1.Pre-Train数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">更精细的数据过滤</font>**<font style="color:rgb(25, 27, 31);">：高质量的预训练数据对模型性能至关重要，因此数据质量评估和过滤是流程中的关键环节。团队利用 </font>**<font style="color:#74B602;">Qwen2-Instruct 模型作为数据质量过滤器，进行全面的多维度分析</font>**<font style="color:rgb(25, 27, 31);">，评估和打分训练样本。与 Qwen2 相比，这一方法显著提升了数据质量评估的能力，使得他们能够更好地保留高质量的训练数据，并有效过滤低质量的样本。</font>
+ **<font style="color:rgb(25, 27, 31);">更优的数学与代码数据</font>**<font style="color:rgb(25, 27, 31);">：在 Qwen2.5 的预训练过程中，团队加入了来自</font>**<font style="color:#74B602;"> Qwen2.5-Math 和 Qwen2.5-Coder 的训练数据</font>**<font style="color:rgb(25, 27, 31);">。这种整合策略非常有效，因为这些专业数据集帮助他们在数学推理和代码生成任务上取得了领先的表现。</font>
+ **<font style="color:rgb(25, 27, 31);">更高质量的合成数据</font>**<font style="color:rgb(25, 27, 31);">：为了生成高质量的合成数据，尤其是在数学、编程和知识领域，团队采用了 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-72B-Instruct </font>**<font style="color:rgb(25, 27, 31);">和 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-Math-72B-Instruct</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:#74B602;">通过使用专有奖励模型和 Qwen2-Math-RM-72B 模型进行严格的过滤</font>**<font style="color:rgb(25, 27, 31);">，进一步提高了这些合成数据的质量。</font>
+ **<font style="color:rgb(25, 27, 31);">更合理的数据混合</font>**<font style="color:rgb(25, 27, 31);">：为了优化预训练数据的分布，团队使用 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-Instruct</font>**<font style="color:rgb(25, 27, 31);"> 模型对不同领域的内容进行分类与平衡。分析显示，像电子商务、社交媒体和娱乐等领域在互联网数据中占比过大，常包含重复、模板化或机器生成的内容。相比之下，</font>**<u><font style="color:#74B602;">技术、科学和学术研究等领域虽然包含更高质量的信息，却常常被低估</font></u>**<font style="color:rgb(25, 27, 31);">。通过对过度代表的领域进行下采样，并对高价值领域进行上采样，他们确保了一个更加平衡且信息丰富的训练数据集，更好地服务于模型的学习目标。</font>

<font style="color:rgb(25, 27, 31);">凭借这些技术手段，团队开发了一个更大、更高质量的预训练数据集，将 Qwen2 的 7T tokens 扩展到了 18T tokens。</font>

:::color5
**<font style="color:#601BDE;">2.Post-Train数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2.5的监督微调过程采用了一个包含数百万个高质量示例的庞大数据集。此次数据扩展专门解决了Qwen2模型在多个关键领域中的局限性，特别是在</font>**<font style="color:#74B602;">长序列生成、数学问题解决、编码、指令执行、结构化数据理解、逻辑推理、跨语言迁移和系统指令</font>**<font style="color:rgb(25, 27, 31);">的鲁棒性方面。</font>



## baichuan2 **<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Baichuan 2有两个版本的型号，Baichuan 2-7B 70亿参数和Baichuan 2 - 13B拥有130亿个参数。 两个都模型接受了 2.6 万亿个token的训练，其中，迄今为止最大的预训练数据量，是baichuan 1的两倍。有了如此海量的训练数据，Baichuan 2较之取得显着提升。在 </font>[<font style="color:rgb(9, 64, 142);">MMLU</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=MMLU&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 等通用基准CMMLU和 C-Eval中Baichuan 2 - 7B 性能较Baichuan 1提高近 30%。 </font>

**paper：**[**https://arxiv.org/pdf/2309.10305**](https://arxiv.org/pdf/2309.10305)

**参考：**[**https://zhuanlan.zhihu.com/p/655576902**](https://zhuanlan.zhihu.com/p/655576902)

:::

:::color5
**<font style="color:#601BDE;">1.预训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">数据来源：</font>**<font style="color:rgb(25, 27, 31);">在数据获取过程中，目标是在数据规模和代表性方面追求全面的数据多样性。百川智能从各种来源收集数据，包括通用互联网网页、书籍、研究论文、代码库等，以构建一个广泛的世界知识体系。</font>

<font style="color:rgb(25, 27, 31);">Baichuan 2训练数据中不同类别的分布情况如下：</font>

1. <font style="color:rgb(25, 27, 31);">Web pages: 40%</font>
2. <font style="color:rgb(25, 27, 31);">Books: 30%</font>
3. <font style="color:rgb(25, 27, 31);">Research papers: 20%</font>
4. <font style="color:rgb(25, 27, 31);">Codebases: 5%</font>
5. <font style="color:rgb(25, 27, 31);">Other resources (e.g., news articles, blogs): 5%</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::success
**训练数据分布**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611234348-b6ee7299-d2a2-402a-a280-b6eea411f891.png)

:::

:::success
**Scaling Law**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611307517-a53d102b-24ad-4a6a-a757-8eeec495aad1.png)

:::



:::color5
**<font style="color:#601BDE;">2.数据处理pipeline </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">数据处理：</font>**<font style="color:rgb(25, 27, 31);">对于数据处理，关注的是数据频率和质量。数据频率依赖于聚类和去重。百川智能建立了一个支持LSH(Locality Sensitive Hashing)特征和密集嵌入特征的大规模去重和聚类系统。这个系统可以在数小时内对数十亿甚至万亿级别的数据进行去重和聚类。基于聚类，单个文档、段落和句子被去重并打分。这些分数随后用于预训练阶段的数据采样。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610381101-c0c1eb4d-2c58-42e4-9cef-9dd787b665c6.png)



# SFT冷启动
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">DeepSeek的Soft Fine-Tuning（SFT）过程是一种结合了软参数调整和知识蒸馏的微调方法，旨在在保持模型预训练知识的同时，有效适应新的任务数据。以下是SFT的详细步骤和冷启动的必要性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.SFT过程</font>**

:::

1. **预训练模型加载**：
    - <font style="color:rgb(51, 51, 51);">首先加载已经在大规模通用数据集上预训练好的模型。这个预训练模型包含丰富的语义信息和语言理解能力，是SFT的基础。</font>
2. **任务适配**：
    - <font style="color:rgb(51, 51, 51);">根据具体的微调任务，对模型进行适配。这可能包括添加任务特定的输出层、修改部分参数，或者调整模型的结构以适应新任务的需求。</font>
3. **软参数调整**：
    - <font style="color:rgb(51, 51, 51);">在微调过程中，采用软参数调整技术，逐步更新模型参数。这种方法旨在保留预训练模型的泛化能力，同时使模型适应新的任务数据。与传统的微调相比，软参数调整更加温和，避免模型参数的大规模变化。</font>
4. **知识蒸馏**：
    - <font style="color:rgb(51, 51, 51);">引入知识蒸馏技术，利用教师模型对学生的微调过程进行指导。教师模型通常是更大或性能更好的预训练模型，通过传递知识，帮助学生模型更好地理解和掌握复杂的语义关系。</font>
5. **冷启动策略**：
    - <font style="color:rgb(51, 51, 51);">在微调的初始阶段，采用冷启动策略，帮助模型平稳过渡到微调任务。冷启动阶段的重点是保持预训练模型的知识，避免在微调初期出现模型性能的下降或不稳定。</font>

:::color5
**<font style="color:#601BDE;">2.冷启动的必要性</font>**

:::

1. **平滑过渡**：
    - <font style="color:rgb(51, 51, 51);">冷启动帮助模型在预训练状态和微调任务之间实现平滑过渡。通过较低的学习率和混合数据加载策略，模型能够在不丢失预训练知识的前提下，逐步适应新的任务数据。</font>
2. **防止过早遗忘**：
    - <font style="color:rgb(51, 51, 51);">在微调初期，使用较低的学习率可以防止模型过早地遗忘预训练阶段学到的大量知识。这使得模型在后续的微调过程中能够更好地结合新旧知识，提升最终的性能。</font>
3. **提升训练稳定性**：
    - <font style="color:rgb(51, 51, 51);">冷启动阶段通过特定的数据加载策略和学习率调度，提高了微调过程的稳定性。这对于防止模型在训练初期出现梯度爆炸或不稳定现象至关重要。</font>
4. **优化计算资源**：
    - <font style="color:rgb(51, 51, 51);">通过在冷启动阶段有效地利用预训练数据，SFT方法减少了对计算资源的浪费。混合数据加载策略使得模型能够在微调初期充分利用预训练数据的优势，提升训练效率。</font>

:::color5
**<font style="color:#601BDE;">3.冷启动具体实现</font>**

:::

1. **低学习率初始化**：
    - <font style="color:rgb(51, 51, 51);">在冷启动阶段，使用较低的学习率进行训练。这有助于模型在微调初期不进行剧烈的参数更新，保持预训练模型的稳定性。</font>

```python
# 示例：冷启动阶段设置低学习率
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
```

2. **混合数据加载**：
    - <font style="color:rgb(51, 51, 51);">在冷启动阶段，加载一部分预训练数据和一部分微调任务数据。预训练数据的占比高于微调任务数据，帮助模型逐步适应新的任务。</font>

```python
# 示例：混合预训练数据和微调数据加载
def get_mixed Loader(train_loader, pretrain_loader, pretrain_weight=0.7):
mixed_loader = []
for _ in range(len(train_loader.dataset)):
    if random.random() < pretrain_weight:
        batch = next(iter(pretrain_loader))
    else:
        batch = next(iter(train_loader))
        mixed_loader.append(batch)
    return DataLoader(mixed_loader, batch_size=train_loader.batch_size, shuffle=True)
```

3. **参数初始化优化**：
    - <font style="color:rgb(51, 51, 51);">对模型的部分参数进行特殊的初始化，确保在冷启动阶段，模型的参数变化较小，保持预训练状态的稳定性。</font>
4. **分阶段学习率调度**：
    - <font style="color:rgb(51, 51, 51);">冷启动阶段结束后，逐步增加学习率，使模型进入强化微调阶段。这种分阶段的学习率调度策略有助于模型在不同阶段集中处理不同的任务需求。</font>

```python
# 示例：分阶段学习率调度
for epoch in range(num_epochs):
    if epoch < num_epochs * 0.3:  # 冷启动阶段，约30%的 epochs
        optimizer.param_groups[0]['lr'] = 1e-5
    else:
        optimizer.param_groups[0]['lr'] = 1e-4
```



# SFT后可能的问题
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739178192412-d3b8794a-8455-48bc-bc18-aaa785971579.png)

<font style="color:#1f2329;">监督微调（</font><font style="color:#1f2329;">SFT</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;">在提升模型特定任务性能的同时</font><font style="color:#1f2329;">，可能引发⼀系列问题：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">过拟合：模型在训练数据上表现良好</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，但泛化能⼒不⾜。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">灾难性遗忘：模型遗忘了预训练阶段学到的知识。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">模型偏差增加：模型可能强化了数据中的偏差</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，导致不公平结果。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">泛化能⼒下降：模型在未见过的数据或任务上性能下降。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">鲁棒性降低：模型对噪声或对抗样本的抵抗⼒减弱。</font>

## 过拟合
**<font style="color:#117CEE;">定义</font>**

<font style="color:#1f2329;">过拟合是指模型在训练数据上表现良好</font><font style="color:#1f2329;">，但在新数据（测试集或实际应⽤中）</font><font style="color:#1f2329;">上性能较差。</font>

**<font style="color:#117CEE;">原因分析</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">数据规模有限：微调数据集通常⽐预训练数据集⼩很多。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">模型复杂度⾼：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">⼤型模型具有⼤量参数</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，容易记住训练数据的细节。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">缺乏正则化：如果在微调过程中没有适当的正则化措施</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，模型可能过度拟合训练数据。</font>

**<font style="color:#117CEE;">影响</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">泛化能⼒差：模型⽆法有效处理未见过的数据。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">实际应⽤受限：在真实场景中</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，模型性能可能⽆法满⾜要求。</font>

**<font style="color:#117CEE;">解决方案</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">数据增⼴：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">增加训练数据的多样性。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">正则化技术：如早停（</font><font style="color:#1f2329;">Early Stopping</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;">、权重衰减等。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">交叉验证：评估模型的泛化性能。</font>

<font style="color:#1f2329;"></font>

## <font style="color:#1f2329;">灾难性遗忘</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">灾难性遗忘</font>**<font style="color:rgb(51, 51, 51);">是指在对大模型进行微调时，模型可能忘记预训练阶段学习到的大量知识，导致其在通用任务上的表现显著下降。</font>

<font style="color:rgb(51, 51, 51);">灾难性遗忘的根本原因是模型参数在微调过程中被过度更新，导致预训练阶段学到的特征信息丢失。</font>

**解决方案**：

+ **<font style="color:rgb(51, 51, 51);">知识蒸馏</font>**<font style="color:rgb(51, 51, 51);">：保留教师模型的知识，指导学生模型的学习。</font>
+ **<font style="color:rgb(51, 51, 51);">参数冻结</font>**<font style="color:rgb(51, 51, 51);">：在某些层冻结参数，防止遗忘。</font>
+ **<font style="color:rgb(51, 51, 51);">渐进式学习</font>**<font style="color:rgb(51, 51, 51);">：逐步引入新任务，保持知识的连续性。</font>
+ **<font style="color:rgb(51, 51, 51);">软参数调整</font>**<font style="color:rgb(51, 51, 51);">：结合软参数调整和知识蒸馏，平衡新旧知识的学习。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原因分析</font>**

:::

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">参数更新：微调时</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，模型参数朝着新任务的最</font><font style="color:#1f2329;">优⽅向调整</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，可能偏离了预训练阶段的知识。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">任务冲突：新任务的⽬标可能与预训练任务不⼀致</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，导致模型需要</font><font style="color:#1f2329;">“</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">舍弃</font><font style="color:#1f2329;">”</font><font style="color:#1f2329;">部分旧知识。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">通⽤能⼒下降：模型可能⽆法再执⾏预训练阶段擅⻓的任务。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">知识遗失：丢失了在⼤规模数据上学习到的有⽤信息。</font>

:::color5
**<font style="color:#601BDE;">2.解决方案</font>**

:::

**方案1：****加载预训练模型：**

+ <font style="color:rgb(51, 51, 51);">加载一个在大规模通用数据集上预训练好的模型（如BERT、GPT等）。</font>
+ <font style="color:rgb(51, 51, 51);">确保模型具有良好的语义理解和生成能力。</font>

**<font style="color:rgb(51, 51, 51);">方案2：知识蒸馏</font>**

1. **选择教师模型**：
    - <font style="color:rgb(51, 51, 51);">使用一个性能更优的预训练模型作为教师模型。</font>
    - <font style="color:rgb(51, 51, 51);">教师模型可以是更大规模的模型，或者在同一架构下优化过的版本。</font>
2. **设计蒸馏损失函数**：
    - <font style="color:rgb(51, 51, 51);">使用软目标蒸馏方法，通过概率分布匹配，传递知识。</font>
    - <font style="color:rgb(51, 51, 51);">定义蒸馏损失函数，结合原始任务损失和蒸馏损失。</font>

```python
# 示例：蒸馏损失函数
def distillation_loss(student_output, teacher_output, temp=2):
    student_output = F.softmax(student_output / temp, dim=-1)
    teacher_output = F.softmax(teacher_output / temp, dim=-1)
    return F.kl_div(student_output, teacher_output, reduction='batchmean') * (temp ** 2)
```

**<font style="color:rgb(51, 51, 51);">方案3：参数冻结与选择</font>**

1. **选择冻结策略**：
    - <font style="color:rgb(51, 51, 51);">决定冻结哪些层的参数，防止其在微调过程中被更新。</font>
    - <font style="color:rgb(51, 51, 51);">常见策略包括冻结嵌入层、某些中间层或全网络。</font>
2. **实现参数冻结**：
    - <font style="color:rgb(51, 51, 51);">在PyTorch中，可以通过设置参数的</font>`<font style="color:rgb(51, 51, 51);">requires_grad</font>`<font style="color:rgb(51, 51, 51);">属性来冻结参数。</font>

```python
# 示例：冻结部分参数
for param in model.named_parameters():
    if 'embeddings' in param[0]:
        param[1].requires_grad = False
```

3. **优化冻结后的模型**：
    - <font style="color:rgb(51, 51, 51);">仅对未冻结的参数进行优化，降低参数更新的剧烈程度。</font>

**<font style="color:rgb(51, 51, 51);">方案4：渐进式学习与任务引入</font>**

1. **设计学习策略**：
    - <font style="color:rgb(51, 51, 51);">在微调过程中，逐步引入新任务的数据和目标。</font>
    - <font style="color:rgb(51, 51, 51);">每个阶段专注于一个特定的任务，保持知识的连续性。</font>
2. **数据混合加载**：
    - <font style="color:rgb(51, 51, 51);">在初期阶段，混合预训练数据和微调任务数据，帮助模型逐步适应新任务。</font>
3. **调整学习率**：
    - <font style="color:rgb(51, 51, 51);">初始阶段设置较低的学习率，防止剧烈参数更新。</font>
    - <font style="color:rgb(51, 51, 51);">随着模型适应新任务，逐步提高学习率，强化新知识的学习。</font>

```python
# 示例：动态学习率调度
scheduler = CosineAnnealingLR(optimizer, T_0=1000, T_i=1000)
```

## <font style="color:#1f2329;">模型偏差增加</font>
**<font style="color:#117CEE;">定义</font>**

<font style="color:#1f2329;">模型偏差是指模型的预测结果偏向某些特定的模式或群体，导致不公平或不准确的结果。</font>

**<font style="color:#117CEE;">原因分析</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">数据偏差：微调数据可能存在偏差</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，如代表性不⾜或标注不公平。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">过度适应特定任务：模型可能强化了特定任务的数据模式 ，忽略了其他可能性。</font>

**<font style="color:#117CEE;">影响</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">公平性问题：模型可能对某些群体不公平。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">可信度降低：⽤户可能对模型的输出产⽣怀疑。</font>

**<font style="color:#117CEE;">解决方案</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">数据审查：确保微调数据的多样性和公平性。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">偏差检测：在微调后</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，对模型进⾏偏差评估。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">模型校正：使⽤技术⼿段减轻模型偏差。</font>

<font style="color:#1f2329;"></font>

## <font style="color:#1f2329;">泛化能力下降</font>
**<font style="color:#117CEE;">定义</font>**

<font style="color:#1f2329;">泛化能⼒是指模型在未见过的数据上保持良好性能的能⼒。</font>

**<font style="color:#117CEE;">原因分析</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">过度专注于特定任务：微调可能让模型只擅⻓于微调任务的数据分布。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">数据多样性不⾜：微调数据集的覆盖范围有限。</font>

**<font style="color:#117CEE;">影响</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">适⽤范围缩⼩：模型在其他任务或不同数据分布上表现不佳。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">灵活性降低： 限制了模型的通⽤性。</font>

**<font style="color:#117CEE;">解决方案</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">多任务学习：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">同时微调模型在多个相关任务上。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">使⽤多样化的数据集：增加微调数据的多样性。</font>

<font style="color:#1f2329;"></font>

## <font style="color:#1f2329;">鲁棒性下降</font>
**<font style="color:#117CEE;">定义</font>**

<font style="color:#1f2329;">鲁棒性是指模型应对噪声、异常值或对抗样本的能⼒。</font>

**<font style="color:#117CEE;">原因分析</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">微调数据质量问题：噪声数据或异常样本可能影响模型稳定性。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">过拟合风险：过度拟合导致模型对数据微⼩变化敏感。</font>

**<font style="color:#117CEE;">影响</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">易受攻击：模型可能容易受到对抗样本的影响。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">性能不稳定：在实际应⽤中 ，模型可能出现异常⾏为。</font>

**<font style="color:#117CEE;">解决方案</font>**

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">数据清洗：确保微调数据的质量。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">对抗训练：提⾼模型对对抗样本的抵抗⼒。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">增加噪声训练：在训练中加⼊噪声 ，提⾼模型的鲁棒性。</font>



<font style="color:rgb(1, 1, 1);"></font>

# <font style="color:rgb(53, 53, 53);">SFT评估</font>
## 评估指标
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





# SFT改进：
## 课程学习
参考：[课程学习](https://www.yuque.com/zhongxian-iiot9/gi3w2u/pikctr3cwm279qo6)

# <font style="color:rgb(51, 51, 51);">长上下文数据如何筛选</font>
**<font style="color:rgb(51, 51, 51);">问题背景</font>**<font style="color:rgb(51, 51, 51);">：作者认为直接用长上下文窗口训练大型语言模型（LLMs）并不能有效提升其长上下文建模能力，因为许多训练样本在长上下文中并没有表现出强烈的语义依赖性。 作者提出了ProLong框架，该框架可以为</font><font style="color:#DF2A3F;">每个训练样本分配一个长依赖性分数</font><font style="color:rgb(51, 51, 51);">，用于评估和筛选对提升LLMs长上下文建模能力更有利的样本。 	</font>

<font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">计算步骤</font>**

1. <font style="color:rgb(51, 51, 51);">计算依赖强度(DST:通过比较给定段落在有无前段落的条件下的困惑度(perplexity)分数来衡量。 </font>
2. <font style="color:rgb(51, 51, 51);">计算依赖距离(DDI):衡量两个文本段落之间的位置关系,距离越远的段落对学习长距离依赖性更重要。</font>
3. <font style="color:rgb(51, 51, 51);">计算依赖特异性（DSP）：通过熵的概念来确保依赖强度在所有前面段落中非均匀分布，以减少由重复模式引入的依赖。例如，在某些文档中，可能会有重复的短语、句子结构或者数据格式，这些重复的部分虽然在位置上相隔较远，但它们之间的“依赖”并不对理解整个文档的语义内容或完成任务有实质性的帮助。 </font>
4. <font style="color:rgb(51, 51, 51);">计算长依赖分数（LDS）：结合依赖强度、依赖距离和依赖特异性，为每对段落分配一个长依赖分数，并通过累积所有段落对的LDS来计算整个文档的LDS。 	</font>

<font style="color:rgb(51, 51, 51);">实验结论</font><font style="color:rgb(51, 51, 51);">✨</font><font style="color:rgb(51, 51, 51);"> 使用ProLong选择的数据集训练的模型（ProLong 50%）在性能上超过了全量数据集微调的模型，这说明完整数据集中的许多文档并不是真正的“长上下文”。</font>

