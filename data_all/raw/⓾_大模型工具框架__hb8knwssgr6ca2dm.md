# ⓾ 大模型工具框架

<!-- source: yuque://zhongxian-iiot9/hlyypb/hb8knwssgr6ca2dm -->

# Langchain
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：La</font><font style="color:rgb(51, 51, 51);">ngChain 是一个用于构建基于大型语言模型（LLM）应用程序的开源框架，旨在帮助开发者将语言模型与其他数据源、工具和计算资源结合，创建更复杂且实用的应用。</font>

**<font style="color:rgb(51, 51, 51);">学习资源:</font>**

+ <font style="color:rgb(51, 51, 51);">官方文档：</font>[https://python.langchain.com/](https://python.langchain.com/)
+ <font style="color:rgb(51, 51, 51);">GitHub 仓库：</font>[https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)
+ <font style="color:rgb(51, 51, 51);">LangChain 学院：提供教程和案例。</font>

:::

**<font style="color:#74B602;">通过 LangChain，开发者可以快速构建从简单问答到复杂企业级应用的 LLM 驱动系统，充分发挥语言模型的潜力。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741604724681-5cb54062-62e9-4aa3-bc3f-2b346c521920.png)

:::color5
**<font style="color:#601BDE;">1.核心目标</font>**

:::

<font style="color:rgb(51, 51, 51);">LangChain 的核心目标是解决语言模型在实际应用中的局限性，例如：</font>

+ **<font style="color:rgb(51, 51, 51);">静态性</font>**<font style="color:rgb(51, 51, 51);">：传统 LLM 缺乏动态更新知识的能力。</font>
+ **<font style="color:rgb(51, 51, 51);">孤立性</font>**<font style="color:rgb(51, 51, 51);">：模型难以直接访问外部数据或工具（如数据库、API）。</font>
+ **<font style="color:rgb(51, 51, 51);">上下文缺失</font>**<font style="color:rgb(51, 51, 51);">：无法长期保存对话历史或用户状态。</font>
+ **<font style="color:rgb(51, 51, 51);">复杂任务分解</font>**<font style="color:rgb(51, 51, 51);">：需要将多步骤任务拆解为模型可执行的子任务。</font>

:::color5
**<font style="color:#601BDE;">2.核心模块</font>**

:::

<font style="color:rgb(51, 51, 51);">LangChain 提供了一套模块化组件，开发者可按需组合：</font>

<font style="color:rgb(51, 51, 51);">2.1 Models（模型）</font>

+ <font style="color:rgb(51, 51, 51);">支持多种 LLM 接口（如 OpenAI、Hugging Face、Anthropic 等）。</font>
+ <font style="color:rgb(51, 51, 51);">提供标准化接口，允许轻松切换不同模型。</font>
+ <font style="color:rgb(51, 51, 51);">支持文本生成、嵌入（Embedding）模型等。</font>

<font style="color:rgb(51, 51, 51);">2.2 Prompts（提示管理）</font>

+ **<font style="color:rgb(51, 51, 51);">模板化提示</font>**<font style="color:rgb(51, 51, 51);">：通过变量动态生成提示词（Prompt Templates）。</font>
+ **<font style="color:rgb(51, 51, 51);">示例选择器（Example Selectors）</font>**<font style="color:rgb(51, 51, 51);">：根据输入动态选择示例，提升上下文学习（Few-Shot Learning）效果。</font>
+ **<font style="color:rgb(51, 51, 51);">输出解析器</font>**<font style="color:rgb(51, 51, 51);">：结构化模型输出（如 JSON、列表等）。</font>

<font style="color:rgb(51, 51, 51);">2.3 Chains（任务链）</font>

+ <font style="color:rgb(51, 51, 51);">将多个模型调用或工具调用组合成工作流。</font>
+ <font style="color:rgb(51, 51, 51);">预定义链（如</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">LLMChain</font>`<font style="color:rgb(51, 51, 51);">、</font>`<font style="color:rgb(51, 51, 51);">SequentialChain</font>`<font style="color:rgb(51, 51, 51);">）和自定义链。</font>
+ <font style="color:rgb(51, 51, 51);">示例：检索-生成链（先搜索外部数据，再生成答案）。</font>

<font style="color:rgb(51, 51, 51);">2.4 Memory（记忆）</font>

+ <font style="color:rgb(51, 51, 51);">保存和更新对话历史或应用状态。</font>
+ <font style="color:rgb(51, 51, 51);">支持短期记忆（如单次对话）和长期记忆（如数据库存储）。</font>
+ <font style="color:rgb(51, 51, 51);">内存类型：</font>`<font style="color:rgb(51, 51, 51);">ConversationBufferMemory</font>`<font style="color:rgb(51, 51, 51);">、</font>`<font style="color:rgb(51, 51, 51);">ConversationSummaryMemory</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">等。</font>

<font style="color:rgb(51, 51, 51);">2.5 Indexes（索引与检索）</font>

+ <font style="color:rgb(51, 51, 51);">集成外部数据源（文档、数据库、API）。</font>
+ <font style="color:rgb(51, 51, 51);">文档加载器（Document Loaders）：从 PDF、网页、数据库等加载数据。</font>
+ <font style="color:rgb(51, 51, 51);">文本分割器（Text Splitters）：处理长文本的分块。</font>
+ <font style="color:rgb(51, 51, 51);">向量存储（Vector Stores）：如 FAISS、Pinecone，用于相似性检索。</font>
+ <font style="color:rgb(51, 51, 51);">检索器（Retrievers）：结合 LLM 实现 RAG（Retrieval-Augmented Generation）。</font>

<font style="color:rgb(51, 51, 51);">2.6 Agents（代理）</font>

+ <font style="color:rgb(51, 51, 51);">允许 LLM 动态调用工具（Tools）完成复杂任务。</font>
+ <font style="color:rgb(51, 51, 51);">代理根据输入决定调用哪些工具（如计算器、搜索引擎、API）。</font>
+ <font style="color:rgb(51, 51, 51);">支持 ReAct 框架（Reasoning + Action），提升模型推理能力。</font>
+ <font style="color:rgb(51, 51, 51);">预定义工具库（如</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">WikipediaQueryRun</font>`<font style="color:rgb(51, 51, 51);">、</font>`<font style="color:rgb(51, 51, 51);">PythonREPLTool</font>`<font style="color:rgb(51, 51, 51);">）。</font>

:::color5
**<font style="color:#601BDE;">3.典型应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">智能问答系统</font>**<font style="color:rgb(51, 51, 51);">：结合外部数据的 RAG 应用（如客服助手）。</font>
+ **<font style="color:rgb(51, 51, 51);">对话机器人</font>**<font style="color:rgb(51, 51, 51);">：支持多轮对话和个性化记忆（如医疗咨询）。</font>
+ **<font style="color:rgb(51, 51, 51);">文档分析</font>**<font style="color:rgb(51, 51, 51);">：总结长文本、跨文档问答。</font>
+ **<font style="color:rgb(51, 51, 51);">自动化工作流</font>**<font style="color:rgb(51, 51, 51);">：自动调用 API 处理邮件、生成报告等。</font>
+ **<font style="color:rgb(51, 51, 51);">代码生成与分析</font>**<font style="color:rgb(51, 51, 51);">：结合代码解释器（Code Interpreter）执行代码。</font>

:::color5
**<font style="color:#601BDE;">4.核心优势</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">模块化设计</font>**<font style="color:rgb(51, 51, 51);">：灵活组合组件，无需从头开发。</font>
+ **<font style="color:rgb(51, 51, 51);">多模型支持</font>**<font style="color:rgb(51, 51, 51);">：兼容主流 LLM 和嵌入模型。</font>
+ **<font style="color:rgb(51, 51, 51);">数据整合能力</font>**<font style="color:rgb(51, 51, 51);">：轻松接入外部数据源。</font>
+ **<font style="color:rgb(51, 51, 51);">社区生态</font>**<font style="color:rgb(51, 51, 51);">：活跃的开源社区和丰富的扩展工具（如 LangSmith 监控、LangServe 部署）。</font>

:::color5
**<font style="color:#601BDE;">5.使用示例</font>**

:::

```python
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# 初始化模型
llm = OpenAI(api_key="your_key")

# 创建提示模板
prompt = PromptTemplate(
    input_variables=["topic"],
    template="用一句话解释以下技术：{topic}。"
)

# 创建任务链
chain = LLMChain(llm=llm, prompt=prompt)

# 执行任务
response = chain.invoke({"topic": "LangChain"})
print(response["text"])  # 输出：LangChain 是一个用于构建基于语言模型的应用程序的框架...
```

:::color5
**<font style="color:#601BDE;">6.进阶功能</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">回调系统</font>**<font style="color:rgb(51, 51, 51);">：监控模型调用、记录日志。</font>
+ **<font style="color:rgb(51, 51, 51);">异步支持</font>**<font style="color:rgb(51, 51, 51);">：提升高并发场景性能。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态扩展</font>**<font style="color:rgb(51, 51, 51);">：结合图像、语音模型（如 GPT-4V）。</font>



## Langchain & RAG & Agent的关系
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">你可以在</font>[**<font style="color:rgb(9, 64, 142);">LangChain</font>**](https://zhida.zhihu.com/search?content_id=697877163&content_type=Answer&match_order=1&q=LangChain&zhida_source=entity)<font style="color:rgb(25, 27, 31);">框架中使用</font>**<font style="color:rgb(25, 27, 31);">RAG</font>**<font style="color:rgb(25, 27, 31);">技术来创建一个</font>**<font style="color:rgb(25, 27, 31);">Agent</font>**<font style="color:rgb(25, 27, 31);">，扮演特定的角色专门解决用户的特定需求。</font>

:::

+ LangChain可以为任务提供足够复杂的工作流结构，而Agent则负责根据Prompt Template的设定执行这些流程中的每一个任务环节。
+ LangChain框架也提供了各种相应的库**<font style="color:#ED740C;">对RAG技术进行支持</font>**，让RAG技术可以作为Agent从Knowledge Base获取知识的工具。
+ Agent获得相应的知识后，再由LLM组织并理解，作出返回给客户有用的信息或是执行特定操作的判断，并由Agent来完成。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741604637732-8381b18a-037e-4573-ad01-35153a510af0.png)





# LLAMA Factory
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">LLAMA Factory</font>**<font style="color:rgb(51, 51, 51);"> 是一个基于 </font>**<font style="color:rgb(51, 51, 51);">Hugging Face Transformers</font>**<font style="color:rgb(51, 51, 51);"> 的开源项目，专注于为大型语言模型（Large Language Models, LLMs）提供高效、灵活且用户友好的微调（Fine-tuning）框架。它旨在简化模型训练流程，支持多种模型架构（如 LLaMA、BART、T5 等）和训练任务（如文本生成、对话系统、指令遵循等），同时优化资源利用效率，适合研究者和开发者快速实验和部署。</font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
2. **<font style="color:rgb(51, 51, 51);">文档</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://llama-factory.readthedocs.io](https://llama-factory.readthedocs.io/)
3. **<font style="color:rgb(51, 51, 51);">Hugging Face 模型库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://huggingface.co/models](https://huggingface.co/models)

:::

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**

:::

**<font style="color:rgb(51, 51, 51);">1.1 高效微调（Efficient Fine-tuning）</font>**

+ **<font style="color:rgb(51, 51, 51);">参数高效方法</font>**<font style="color:rgb(51, 51, 51);">：支持</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">LoRA（Low-Rank Adaptation）</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(51, 51, 51);">QLoRA（量化 LoRA）</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(51, 51, 51);">Adapter</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">等技术，显著降低显存占用和计算成本，适合在消费级 GPU（如单卡 24GB）上训练超大规模模型（如 70B 参数的 LLaMA）。</font>
+ **<font style="color:rgb(51, 51, 51);">混合精度训练</font>**<font style="color:rgb(51, 51, 51);">：集成 FP16/BP16 和梯度裁剪，加速训练并减少显存消耗。</font>
+ **<font style="color:rgb(51, 51, 51);">分布式训练</font>**<font style="color:rgb(51, 51, 51);">：支持多卡并行（如 DeepSpeed、FSDP），扩展至多节点训练。</font>

**<font style="color:rgb(51, 51, 51);">1.2 模块化设计</font>**

+ **<font style="color:rgb(51, 51, 51);">数据集与模型解耦</font>**<font style="color:rgb(51, 51, 51);">：提供统一的数据预处理接口，支持自定义数据集和 Hugging Face 数据集库。</font>
+ **<font style="color:rgb(51, 51, 51);">灵活的训练配置</font>**<font style="color:rgb(51, 51, 51);">：通过配置文件或命令行参数调整超参数（学习率、批次大小、优化器等）。</font>
+ **<font style="color:rgb(51, 51, 51);">可扩展性</font>**<font style="color:rgb(51, 51, 51);">：支持自定义模型架构、损失函数和评估指标，方便适配新模型或任务。</font>

**<font style="color:rgb(51, 51, 51);">1.3 多任务支持</font>**

+ **<font style="color:rgb(51, 51, 51);">生成任务</font>**<font style="color:rgb(51, 51, 51);">：文本生成、对话生成（如 ChatBot）、代码生成等。</font>
+ **<font style="color:rgb(51, 51, 51);">指令微调</font>**<font style="color:rgb(51, 51, 51);">：针对遵循用户指令的任务（如 Alpaca 格式数据集）。</font>
+ **<font style="color:rgb(51, 51, 51);">持续预训练</font>**<font style="color:rgb(51, 51, 51);">：支持在领域特定数据上进一步预训练模型。</font>

**<font style="color:rgb(51, 51, 51);">1.4 可视化与监控</font>**

+ <font style="color:rgb(51, 51, 51);">集成</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">TensorBoard</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">或</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">WandB</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">进行训练过程可视化。</font>
+ <font style="color:rgb(51, 51, 51);">提供训练日志、损失曲线和生成样例的实时监控。</font>

:::color5
**<font style="color:#601BDE;">2.技术架构</font>**

:::

<font style="color:rgb(51, 51, 51);">LLAMA Factory 基于以下技术栈构建：</font>

1. **<font style="color:rgb(51, 51, 51);">PyTorch</font>**<font style="color:rgb(51, 51, 51);">：核心深度学习框架。</font>
2. **<font style="color:rgb(51, 51, 51);">Hugging Face Ecosystem</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Transformers</font>**<font style="color:rgb(51, 51, 51);">：模型加载与训练。</font>
    - **<font style="color:rgb(51, 51, 51);">Datasets</font>**<font style="color:rgb(51, 51, 51);">：数据处理与缓存。</font>
    - **<font style="color:rgb(51, 51, 51);">Accelerate</font>**<font style="color:rgb(51, 51, 51);">：分布式训练支持。</font>
3. **<font style="color:rgb(51, 51, 51);">PEFT（Parameter-Efficient Fine-tuning）</font>**<font style="color:rgb(51, 51, 51);">：实现参数高效微调方法。</font>
4. **<font style="color:rgb(51, 51, 51);">量化库（如 bitsandbytes）</font>**<font style="color:rgb(51, 51, 51);">：支持 4/8-bit 量化训练（QLoRA）。</font>

**<font style="color:rgb(51, 51, 51);">代码结构示例</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
llama-factory/
├── configs/          # 训练配置文件
├── data/             # 数据集处理脚本
├── model/            # 模型定义与适配器
├── trainer/          # 训练循环与优化逻辑
├── utils/            # 工具函数（日志、分布式等）
└── train.py          # 主训练脚本
```

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">对话系统</font>**<font style="color:rgb(51, 51, 51);">：微调 LLaMA 或 ChatGLM 构建领域专属对话助手。</font>
2. **<font style="color:rgb(51, 51, 51);">文本生成</font>**<font style="color:rgb(51, 51, 51);">：生成高质量文章、故事或营销文案。</font>
3. **<font style="color:rgb(51, 51, 51);">指令遵循</font>**<font style="color:rgb(51, 51, 51);">：训练模型遵循复杂指令（如 Alpaca、Vicuna 格式）。</font>
4. **<font style="color:rgb(51, 51, 51);">代码生成</font>**<font style="color:rgb(51, 51, 51);">：适配 CodeLLaMA 等模型生成代码片段。</font>
5. **<font style="color:rgb(51, 51, 51);">领域适应</font>**<font style="color:rgb(51, 51, 51);">：在医学、法律等专业领域数据上优化模型表现。</font>

:::color5
**<font style="color:#601BDE;">4.安装与使用</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">安装依赖</font>**

```bash
pip install llama-factory
# 或从源码安装
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -r requirements.txt

```

2. **<font style="color:rgb(51, 51, 51);">快速启动</font>**

```bash
# 使用 LoRA 微调 LLaMA-7B 模型
python train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset alpaca_en \
  --lora_target_modules q_proj v_proj \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 8 \
  --lr 2e-4 \
  --output_dir ./output
```

3. **<font style="color:rgb(51, 51, 51);">配置文件驱动</font>**

<font style="color:rgb(51, 51, 51);">通过 YAML 文件定义训练参数：</font>

```yaml
# configs/alpaca_lora.yaml
model_name_or_path: meta-llama/Llama-2-7b-hf
dataset: alpaca_en
lora:
  target_modules: ["q_proj", "v_proj"]
  r: 8
  lora_alpha: 32
training:
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 8
  learning_rate: 2e-4
  num_train_epochs: 3
```

运行命令

```bash
python train.py --config configs/alpaca_lora.yaml
```





# Dify
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(63, 63, 63);">Dify是一个开源的大语言模型应用开发平台，支持GPT、Mistral、Llama3等数百种模型。平台提供声明式开发环境（通过YAML定义应用）、模块化设计、LLMOps功能（监控和优化应用性能）以及私有化部署能力。其定位是简化复杂AI应用的开发流程，特别适合需要深度定制化或企业级部署的场景。</font>

<font style="color:rgb(63, 63, 63);">官网：</font>[https://docs.dify.ai/zh-hans](https://docs.dify.ai/zh-hans)

<font style="color:rgb(63, 63, 63);">参考：</font>[https://zhuanlan.zhihu.com/p/25771359587](https://zhuanlan.zhihu.com/p/25771359587)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

<font style="color:rgb(25, 27, 31);">Dify 提供安全数据通道、高可靠索引检索、友好提示词开发、多模型切换、推理观测、日志记录、数据标注、模型训练、微调、简化AI研发、定制化Agent自动化、AI工作流编排等优势，实现数据安全、开发高效、模型优化、自动化智能及工作流管理，助力开发者构建强大、灵活的AI应用。</font>

:::color5
**<font style="color:#601BDE;">2.功能列表</font>**

:::

| **<font style="color:rgb(25, 27, 31);">类别</font>** | **<font style="color:rgb(25, 27, 31);">内容</font>** |
| :--- | :--- |
| [<font style="color:rgb(9, 64, 142);">LLM 推理引擎</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=LLM+%E6%8E%A8%E7%90%86%E5%BC%95%E6%93%8E&zhida_source=entity) | <font style="color:rgb(25, 27, 31);">Dify Runtime (自 v0.4 移除了 LangChain)</font> |
| <font style="color:rgb(25, 27, 31);">支持的商业模型</font> | <font style="color:rgb(25, 27, 31);">10+，包括 OpenAI 和 Anthropic<br>主流新模型可在 48 小时内接入</font> |
| <font style="color:rgb(25, 27, 31);">支持的 MaaS 厂商</font> | <font style="color:rgb(25, 27, 31);">7 家：</font>[<font style="color:rgb(9, 64, 142);">Hugging Face</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=Hugging+Face&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Replicate</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=Replicate&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);">, AWS Bedrock, NVIDIA, GroqCloud, together.ai, OpenRouter</font> |
| <font style="color:rgb(25, 27, 31);">支持的本地模型推理运行时</font> | <font style="color:rgb(25, 27, 31);">6 种：Xoribits（推荐）、OpenLLM、LocalAI、ChatGLM、Ollama、</font>[<font style="color:rgb(9, 64, 142);">NVIDIA TIS</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=NVIDIA+TIS&zhida_source=entity) |
| <font style="color:rgb(25, 27, 31);">OpenAI 接口标准模型集成</font> | <font style="color:rgb(25, 27, 31);">无限支持</font> |
| <font style="color:rgb(25, 27, 31);">多模态能力</font> | <font style="color:rgb(25, 27, 31);">ASR 模型、富文本模型（最高支持 GPT-4o 规格）</font> |
| <font style="color:rgb(25, 27, 31);">内置应用类型</font> | <font style="color:rgb(25, 27, 31);">文本生成、聊天机器人、代理、工作流、对话流</font> |
| [<font style="color:rgb(9, 64, 142);">Prompt-as-a-Service</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=Prompt-as-a-Service&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">编排</font> | <font style="color:rgb(25, 27, 31);">广受好评的可视化编排界面，可集中修改 Prompt 并预览效果</font> |
| <font style="color:rgb(25, 27, 31);">编排模式</font> | <font style="color:rgb(25, 27, 31);">简单编排、代理编排、流程编排</font> |
| <font style="color:rgb(25, 27, 31);">Prompt 变量类型</font> | <font style="color:rgb(25, 27, 31);">字符串、单选枚举</font> |
| <font style="color:rgb(25, 27, 31);">外部 API 支持</font> | <font style="color:rgb(25, 27, 31);">文件（2024 Q3 上线）</font> |
| <font style="color:rgb(25, 27, 31);">代理工作流特性</font> | <font style="color:rgb(25, 27, 31);">行业领先的可视化工作流编排界面，实时编辑节点调试、模块化 DSL、原生代码运行时</font> |
| <font style="color:rgb(25, 27, 31);">支持的节点</font> | <font style="color:rgb(25, 27, 31);">LLM、知识检索、问题分类器、IF/ELSE、代码、模板、HTTP 请求、工具</font> |
| <font style="color:rgb(25, 27, 31);">RAG 特性</font> | <font style="color:rgb(25, 27, 31);">行业首个可视化知识库管理界面，支持片段预览和召回测试</font> |
| <font style="color:rgb(25, 27, 31);">索引方法</font> | <font style="color:rgb(25, 27, 31);">关键词、文本向量、LLM 辅助问题-片段模型</font> |
| <font style="color:rgb(25, 27, 31);">检索方法</font> | <font style="color:rgb(25, 27, 31);">关键词、文本相似度匹配、混合搜索、多路径检索、重排序模型</font> |
| <font style="color:rgb(25, 27, 31);">召回优化</font> | <font style="color:rgb(25, 27, 31);">重排序模型</font> |
| <font style="color:rgb(25, 27, 31);">ETL 能力</font> | <font style="color:rgb(25, 27, 31);">自动清理 TXT、Markdown、PDF、HTML、DOC、CSV 格式数据；支持非结构化服务</font> |
| <font style="color:rgb(25, 27, 31);">知识库同步</font> | <font style="color:rgb(25, 27, 31);">同步 Notion 文档、网页作为知识库</font> |
| <font style="color:rgb(25, 27, 31);">支持的向量数据库</font> | [<font style="color:rgb(9, 64, 142);">Qdrant</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=Qdrant&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);">（推荐）、Weaviate、</font>[<font style="color:rgb(9, 64, 142);">Zilliz/Milvus</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=Zilliz%2FMilvus&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);">、Pgvector、Pgvector-rs、Chroma、</font>[<font style="color:rgb(9, 64, 142);">OpenSearch</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=OpenSearch&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">TiDB</font>](https://zhida.zhihu.com/search?content_id=254176456&content_type=Article&match_order=1&q=TiDB&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);">、腾讯向量、Oracle、Relyt、Analyticdb、Couchbase</font> |
| <font style="color:rgb(25, 27, 31);">代理技术</font> | <font style="color:rgb(25, 27, 31);">ReAct、函数调用</font> |
| <font style="color:rgb(25, 27, 31);">工具支持</font> | <font style="color:rgb(25, 27, 31);">调用 OpenAI 插件标准工具、直接加载 OpenAPI 规范 API 为工具</font> |
| <font style="color:rgb(25, 27, 31);">内置工具</font> | <font style="color:rgb(25, 27, 31);">40+ 工具（截至 2024 Q2）</font> |
| <font style="color:rgb(25, 27, 31);">日志记录</font> | <font style="color:rgb(25, 27, 31);">支持，基于日志的注释</font> |
| <font style="color:rgb(25, 27, 31);">注释回复</font> | <font style="color:rgb(25, 27, 31);">基于人工标注的问答，用于基于相似性的回复；可导出为数据格式以微调模型</font> |
| <font style="color:rgb(25, 27, 31);">内容审核</font> | <font style="color:rgb(25, 27, 31);">OpenAI 内容审核或外部 API</font> |
| <font style="color:rgb(25, 27, 31);">团队协作</font> | <font style="color:rgb(25, 27, 31);">工作区、多成员管理</font> |
| <font style="color:rgb(25, 27, 31);">API 规范</font> | <font style="color:rgb(25, 27, 31);">RESTful，覆盖大多数功能</font> |
| <font style="color:rgb(25, 27, 31);">部署方式</font> | <font style="color:rgb(25, 27, 31);">Docker、Helm</font> |


:::color5
**<font style="color:#601BDE;">3.构建应用方法</font>**

:::

<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">Dify中的“应用”是基于GPT等大语言模型构建的实际场景应用，旨在将智能AI技术融入特定需求。它融合了AI应用开发范式与具体交付物，为开发者提供：</font>

+ <font style="color:rgb(25, 27, 31);">封装友好的API：后端或前端应用可直接调用，通过Token鉴权，简化集成流程。</font>
+ <font style="color:rgb(25, 27, 31);">开箱即用、美观托管的WebApp：提供模版支持二次开发，快速构建用户界面。</font>
+ <font style="color:rgb(25, 27, 31);">易用界面：集成提示词工程、上下文管理、日志分析和标注功能，提升开发效率。</font>

<font style="color:rgb(25, 27, 31);">开发者可根据需求灵活选择全部或部分功能，助力AI应用高效开发。</font>

:::color5
**<font style="color:#601BDE;">4.构建应用类型</font>**

:::

<font style="color:rgb(25, 27, 31);"></font>

<font style="color:rgb(25, 27, 31);">Dify 提供五种应用类型：</font>

1. **<font style="color:rgb(25, 27, 31);">聊天助手</font>**<font style="color:rgb(25, 27, 31);">：基于 LLM 构建对话式交互的助手。</font>
2. **<font style="color:rgb(25, 27, 31);">文本生成应用</font>**<font style="color:rgb(25, 27, 31);">：面向文本生成类任务的助手，例如撰写故事、文本分类、翻译等。</font>
3. **<font style="color:rgb(25, 27, 31);">Agent</font>**<font style="color:rgb(25, 27, 31);">：能够分解任务、推理思考、调用工具的对话式智能助手。</font>
4. **<font style="color:rgb(25, 27, 31);">对话流（Chatflow）</font>**<font style="color:rgb(25, 27, 31);">：适用于设计复杂流程的多轮对话场景，支持记忆功能并能进行动态应用编排。</font>
5. **<font style="color:rgb(25, 27, 31);">工作流（Workflow）</font>**<font style="color:rgb(25, 27, 31);">：适用于自动化、批处理等单轮生成类任务的场景的应用编排方式，单向生成结果。</font>

| **<font style="color:rgb(25, 27, 31);">功能</font>** | **<font style="color:rgb(25, 27, 31);">文本生成应用</font>** | **<font style="color:rgb(25, 27, 31);">聊天助手</font>** | **<font style="color:rgb(25, 27, 31);">Agent</font>** | **<font style="color:rgb(25, 27, 31);">对话流（Chatflow）</font>** | **<font style="color:rgb(25, 27, 31);">工作流（Workflow）</font>** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">WebApp 界面</font> | <font style="color:rgb(25, 27, 31);">表单+结果式</font> | <font style="color:rgb(25, 27, 31);">对话式</font> | <font style="color:rgb(25, 27, 31);">对话式</font> | <font style="color:rgb(25, 27, 31);">流程式</font> | <font style="color:rgb(25, 27, 31);">表单+流程式</font> |
| <font style="color:rgb(25, 27, 31);">WebAPI 端点</font> | <font style="color:rgb(25, 27, 31);">/completion-messages</font> | <font style="color:rgb(25, 27, 31);">/chat-messages</font> | <font style="color:rgb(25, 27, 31);">/chat-messages</font> | <font style="color:rgb(25, 27, 31);">/chat-messages</font> | <font style="color:rgb(25, 27, 31);">/workflows/run</font> |
| <font style="color:rgb(25, 27, 31);">交互方式</font> | <font style="color:rgb(25, 27, 31);">一问一答</font> | <font style="color:rgb(25, 27, 31);">多轮对话</font> | <font style="color:rgb(25, 27, 31);">多轮对话</font> | <font style="color:rgb(25, 27, 31);">流程控制+多轮对话</font> | <font style="color:rgb(25, 27, 31);">单轮生成+多轮对话</font> |
| <font style="color:rgb(25, 27, 31);">流式结果返回</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> |
| <font style="color:rgb(25, 27, 31);">上下文保存</font> | <font style="color:rgb(25, 27, 31);">当次</font> | <font style="color:rgb(25, 27, 31);">持续</font> | <font style="color:rgb(25, 27, 31);">持续</font> | <font style="color:rgb(25, 27, 31);">持续</font> | <font style="color:rgb(25, 27, 31);">当次</font> |
| <font style="color:rgb(25, 27, 31);">用户输入表单</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> |
| <font style="color:rgb(25, 27, 31);">知识库与工具</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> |
| <font style="color:rgb(25, 27, 31);">AI 开场白</font> | <font style="color:rgb(25, 27, 31);">不支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">不支持</font> |
| <font style="color:rgb(25, 27, 31);">情景举例</font> | <font style="color:rgb(25, 27, 31);">翻译、判断、索引</font> | <font style="color:rgb(25, 27, 31);">聊天</font> | <font style="color:rgb(25, 27, 31);">任务分解、推理</font> | <font style="color:rgb(25, 27, 31);">流程控制、场景定义</font> | <font style="color:rgb(25, 27, 31);">批处理、自动化</font> |
| <font style="color:rgb(25, 27, 31);">实时反馈</font> | <font style="color:rgb(25, 27, 31);">无</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">支持</font> | <font style="color:rgb(25, 27, 31);">无</font> |


:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(63, 63, 63);">优势：</font>**

+ <font style="color:rgb(63, 63, 63);">国际化支持：主要面向海外市场，集成多语言模型和国际化工具。</font>
+ <font style="color:rgb(63, 63, 63);">灵活性与扩展性：支持自托管和云服务，可无缝集成企业现有系统，满足数据安全和合规需求。</font>
+ <font style="color:rgb(63, 63, 63);">活跃开发者生态：开源社区提供丰富的模板和协作机会，支持快速迭代创新（如Workflow可视化流程）。</font>
+ <font style="color:rgb(63, 63, 63);">多模型对比：支持同时测试不同模型（如GPT-4与Claude3）的响应，优化任务适配性。</font>

**<font style="color:rgb(63, 63, 63);">劣势：</font>**

+ <font style="color:rgb(63, 63, 63);">学习门槛较高：模型集成和配置需要技术背景，对新手不友好。</font>
+ <font style="color:rgb(63, 63, 63);">国内生态较弱：与Coze相比，国内市场份额和插件支持有限。</font>

:::color5
**<font style="color:#601BDE;">6.适用场景</font>**

:::

<font style="color:rgb(63, 63, 63);">企业级LLM基础设施搭建、私有化部署、开发者主导的复杂AI应用开发。</font>

# FasterTransformer
:::color3
**简介：**[FasterTransformer](https://link.zhihu.com/?target=https%3A//github.com/NVIDIA/FasterTransformer)<font style="color:rgb(25, 27, 31);"> 是 NVIDIA 推出的一个用于加速 </font>[<font style="color:rgb(9, 64, 142);">Transformer 模型</font>](https://zhida.zhihu.com/search?content_id=236854338&content_type=Article&match_order=1&q=Transformer+%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">推理的库。该库主要通过使用 NVIDIA 的深度学习加速库 cuBLAS、</font>[<font style="color:rgb(9, 64, 142);">cuDNN</font>](https://zhida.zhihu.com/search?content_id=236854338&content_type=Article&match_order=1&q=cuDNN&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 </font>[<font style="color:rgb(9, 64, 142);">TensorRT</font>](https://zhida.zhihu.com/search?content_id=236854338&content_type=Article&match_order=1&q=TensorRT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，以及深度学习框架 </font>[<font style="color:rgb(9, 64, 142);">TensorFlow</font>](https://zhida.zhihu.com/search?content_id=236854338&content_type=Article&match_order=1&q=TensorFlow&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 </font>[<font style="color:rgb(9, 64, 142);">PyTorch</font>](https://zhida.zhihu.com/search?content_id=236854338&content_type=Article&match_order=1&q=PyTorch&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的扩展，对 Transformer 模型进行优化和加速。本系列文章试图对FasterTransformer中的Decoding Model进行详细的分析，主要探究其代码模块设计、性能加速优化方案和</font>[<font style="color:rgb(9, 64, 142);">CUDA Kernel</font>](https://zhida.zhihu.com/search?content_id=236854338&content_type=Article&match_order=1&q=CUDA+Kernel&zhida_source=entity)<font style="color:rgb(25, 27, 31);">实现技巧，通过学习源码掌握其实现精髓。Decoding Model是经典Transformer中的第二部分，也是推理耗时最高的部分，对这个模块的大量优化值得深入学习借鉴。</font>

**参考：**[**https://www.zhihu.com/question/602468960/answer/3040008501**](https://www.zhihu.com/question/602468960/answer/3040008501)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **算子融合**。将多层神经网络组合成一个单一的神经网络，将使用一个单一的核（kernel）进行计算。 这种技术减少了数据传输并增加了数学密度，从而加速了推理阶段的计算。 例如， multi-head attention 块中的所有操作都可以合并到一个核（kernel）中。如下图所示，FT将 Swin-Transformer 的INT8计算图中 35 个零碎的算子，融合为了6个kernel 和 部分高度优化的GEMM算子，从而实现了极大的提速。
+ [**<font style="color:rgb(9, 64, 142);">KV-Cache 管理</font>**](https://zhida.zhihu.com/search?content_id=642069097&content_type=Answer&match_order=1&q=KV-Cache+%E7%AE%A1%E7%90%86&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。对于长序列的Transformer模型，将计算过程中的 Key 和 Value 存储起来，并在每个时间步中，只对新的 Query 进行计算，而不需要重新计算已经计算过的 Key 和 Value。FT 分配了一个缓冲区来在每一步存储它们。虽然需要一些额外的内存使用，但 FT 可以节省重新计算的成本。该过程如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743475096960-0c4f33c3-a394-4dd2-8474-80438ec5b75d.png)<font style="color:rgb(25, 27, 31);">  
</font>**模型并行**<font style="color:rgb(25, 27, 31);">。FT 使用张量并行 (TP) 和流水线并行 (PP) 技术将基于Transformer架构的神经网络拆分到多个 GPU 和节点上，这是它相比于</font>[TensorRT](https://zhida.zhihu.com/search?content_id=642069097&content_type=Answer&match_order=1&q=TensorRT&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的最大特点。</font>

+ **低精度推理**<font style="color:rgb(25, 27, 31);">。FT 实现了对部分网络的高性能 FP16 / INT8 计算推理加速，通过低精度数值较少的数据传输量和所需的内存，以及它在对应的INT8 Tensor Core 上的高性能向量化计算能力，实现加速。</font>
+ <font style="color:rgb(25, 27, 31);">除此之外，</font>**内存优化、Matmul kernel自动调整，BeamSearch**<font style="color:rgb(25, 27, 31);"> 等技术也被应用在FT的框架之中。</font>[**FlashAttention**](https://zhida.zhihu.com/search?content_id=642069097&content_type=Answer&match_order=1&q=FlashAttention&zhida_source=entity)<font style="color:rgb(25, 27, 31);">作为一种针对大模型的Attention计算过程的加速技术，同样在FT中有对应的实现，不过一般更多的应用于大模型的推理中，较小的Transformer结构很少使用该kernel。</font>

:::color5
**<font style="color:#601BDE;">2.与tensorRT的关系</font>**

:::

TensorRT作为NVIDIA主力推广的通用推理引擎，在CNN模型的部署中被广泛使用。近些年Transformer网络逐渐盛行，但TensorRT的支持程度相对不够及时（TensorRT需要考虑通用性，因此在开发进度及稳定性等方面有更高要求），因此 NVIDIA 针对Transformer网络的优化部署推出了 FT 库作为临时方案。伴随今年大模型LLM的爆火，FT 框架被使用及研究的频次极速增长，还有很多类似或基于FT开发的推理引擎被依次提出（但主要面向LLM，对一般Transformer网络的支持不如FT）。NVIDIA 为保持自身推理引擎的独立性和垄断性，后续将减少对 FT 框架的支持，同时将其能力融合到高版本 TensorRT 中，例如** TRT9 和 TRT-LLM。**

:::color5
**<font style="color:#601BDE;">3.使用方法</font>**

:::

+ **环境配置**

```plain
CMake >= 3.13 for PyTorch
CUDA 11.0 or newer version
NCCL 2.10 or newer version
Python 3 is recommended because some features are not supported in python 2
PyTorch: Verify on 1.10.0, >= 1.5.0 should work.

# 或推荐使用镜像 nvcr.io/nvidia/pytorch:22.09-py3
```

+ **编译**

```plain
cd $WORKSPACE 
git submodule update --init 
mkdir -p build 
cd build 
cmake -DSM=xx -DCMAKE_BUILD_TYPE=Release -DBUILD_PYT=ON -DBUILD_TRT=ON .. 
make -j12
#DSM与目标硬件对应，例如 60 (P40) 、 61 (P4) 、 70 (V100) 、 75(T4) 、 80 (A100)，Orin 对应 87
```

+ **PyTorch Op 调用**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">FT库编译完成后，可以直接使用 PyTorch / TensorFlow/ Triton 对应接口来实现调用，这里以PyTorch 推理 Swin-Transformer模型为例，FT对整个 Swin-Transformer模型进行了封装，并实现了torch的接口，直接load 库文件 `libth_transformer.so` ，即可在PyTorch工程中直接使用 Swin-Transformer 的模型算子。  
</font><font style="color:rgb(51, 51, 51);">PyTorch调用的逻辑，本质上就是通过PyTorch接口传入对应的权重参数来实例化一个C++实现的Swin-Transformer类，具体调用流程如下：</font>

```plain
# build PyTorch 模型并load权重  
model = build_model(config).cuda()  
model.load_state_dict(torch.load(checkpoint, map_location='cpu') , strict=False)   

# Load FT 算子库  
torch.classes.load_library('./libth_transformer.so')   

# 从 model 中取出所有层的权重数据 sw_weights，SwinTransformerWeightTransposeQKVWeight 函数逐层按 key 值来获取模型的参数，因此对于自定义模型需要重新实现该函数；  
sw_weights = SwinTransformerWeightTransposeQKVWeight(layer_num, window_size, depths, num_heads, th_path, model.state_dict(), version)   

# 传入权重数据 sw_weights，构建SwinTransformerClass，其他需要传入的参数，包括层数，head_nums，img_size，patch_size等，SwinTransformerClass可以进行缩放，但基本结构不能更改，自定义结构则需要重新实现该算子  
swin_transformer = torch.classes.SwinTransformerClass(sw_weights.weights, depths_tensor, num_heads_tensor, max_batch, img_size, patch_size, in_chans, embed_dim,                                       
                                                                           window_size, ape, patch_norm, layer_num, mlp_ratio, qkv_bias, qk_scale, version)   

# 模型推理，直接调用 forward 函数进行计算；由于该模型定义只到了 avg 层，所以对head部分依然是用原来的 torch的model进行计算  
op_embedding = swin_transformer.forward(images)  op_output = model.head(op_embedding)
```



# TensorRT
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">TensorRT是可以在</font>**<font style="color:rgb(25, 27, 31);">NVIDIA</font>**<font style="color:rgb(25, 27, 31);">各种</font>**<font style="color:rgb(25, 27, 31);">GPU硬件平台</font>**<font style="color:rgb(25, 27, 31);">下运行的一个</font>**<font style="color:rgb(25, 27, 31);">C++推理框架</font>**<font style="color:rgb(25, 27, 31);">。我们利用Pytorch、TF或者其他框架训练好的模型，可以转化为TensorRT的格式，然后利用TensorRT推理引擎去运行我们这个模型，从而提升这个模型在英伟达GPU上运行的速度。速度提升的比例是</font>**<font style="color:rgb(25, 27, 31);">比较可观</font>**<font style="color:rgb(25, 27, 31);">的。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://link.zhihu.com/?target=https%3A//docs.nvidia.com/cuda/cuda-c-programming-guide/index.html%23compute-capabilities](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/cuda/cuda-c-programming-guide/index.html%23compute-capabilities)

参考：[https://zhuanlan.zhihu.com/p/374047261](https://zhuanlan.zhihu.com/p/374047261)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743474693442-a9af4877-9aa2-40f8-bae2-6368ec9a9066.png)

:::color5
**<font style="color:#601BDE;">1.加速方法</font>**

:::

+ <font style="color:rgb(25, 27, 31);">算子融合(层与张量融合)：简单来说就是通过融合一些计算op或者去掉一些多余op来减少数据流通次数以及显存的频繁使用来提速</font>
+ <font style="color:rgb(25, 27, 31);">量化：量化即IN8量化或者FP16以及TF32等不同于常规FP32精度的使用，这些精度可以显著提升模型执行速度并且不会保持原先模型的精度</font>
+ <font style="color:rgb(25, 27, 31);">内核自动调整：根据不同的显卡构架、SM数量、内核频率等(例如1080TI和2080TI)，选择不同的优化策略以及计算方式，寻找最合适当前构架的计算方式</font>
+ <font style="color:rgb(25, 27, 31);">动态张量显存：我们都知道，显存的开辟和释放是比较耗时的，通过调整一些策略可以减少模型中这些操作的次数，从而可以减少模型运行的时间</font>
+ <font style="color:rgb(25, 27, 31);">多流执行：使用CUDA中的stream技术，最大化实现并行操作</font>

:::color5
**<font style="color:#601BDE;">2.加速效果</font>**

:::

+ <font style="color:rgb(25, 27, 31);">SSD检测模型，加速3倍(Caffe)</font>
+ <font style="color:rgb(25, 27, 31);">CenterNet检测模型，加速3-5倍(Pytorch)</font>
+ <font style="color:rgb(25, 27, 31);">LSTM、Transformer(细op)，加速0.5倍-1倍(TensorFlow)</font>
+ <font style="color:rgb(25, 27, 31);">resnet系列的分类模型，加速3倍左右(Keras)</font>
+ <font style="color:rgb(25, 27, 31);">GAN、分割模型系列比较大的模型，加速7-20倍左右(Pytorch)</font>

:::color5
**<font style="color:#601BDE;">3.使用场景</font>**

:::

<font style="color:rgb(25, 27, 31);">TensorRT的使用场景很多。服务端、嵌入式端、家用电脑端都是我们的使用场景。</font>

+ <font style="color:rgb(25, 27, 31);">服务端对应的显卡型号为A100、T4、V100等</font>
+ <font style="color:rgb(25, 27, 31);">嵌入式端对应的显卡为AGX Xavier、TX2、Nano等</font>
+ <font style="color:rgb(25, 27, 31);">家用电脑端对应的显卡为3080、2080TI、1080TI等</font>

:::color5
**<font style="color:#601BDE;">4.精度支持</font>**

:::

+ <font style="color:rgb(25, 27, 31);">FP32：单精度浮点型，没什么好说的，深度学习中最常见的数据格式，训练推理都会用到；</font>
+ <font style="color:rgb(25, 27, 31);">FP16：半精度浮点型，相比FP32占用内存减少一半，有相应的指令值，速度比FP32要快很多；</font>
+ <font style="color:rgb(25, 27, 31);">TF32：第三代Tensor Core支持的一种数据类型，是一种截短的 Float32 数据格式，将FP32中23个尾数位截短为10bits，而指数位仍为8bits，总长度为19(=1+8 +10)。保持了与FP16同样的精度(尾数位都是 10 位），同时还保持了FP32的动态范围指数位都是8位)；</font>
+ <font style="color:rgb(25, 27, 31);">INT8：整型，相比FP16占用内存减小一半，有相应的指令集，模型量化后可以利用INT8进行加速。</font>

:::color5
**<font style="color:#601BDE;">5.安装方案</font>**

:::

<font style="color:rgb(25, 27, 31);">安装TensorRT的方式有很多，官方提供了多种方式：</font>

<font style="color:rgb(83, 88, 97);">You can choose between the following installation options when installing TensorRT; Debian or RPM packages, a pip wheel file, a tar file, or a zip file.</font>

<font style="color:rgb(25, 27, 31);">这些安装包都可以从官方直接下载，从</font><font style="color:rgb(25, 27, 31);"> </font>[https://developer.nvidia.com/zh-cn/tensorrt](https://link.zhihu.com/?target=https%3A//developer.nvidia.com/zh-cn/tensorrt)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">进入下载即可，需要注意这里</font>**<font style="color:rgb(25, 27, 31);">我们要注册会员并且登录</font>**<font style="color:rgb(25, 27, 31);">才可以下载。老潘一直使用的方式是下载</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tar包</font>`<font style="color:rgb(25, 27, 31);">，下载好后解压即可，只要我们的环境符合要求就可以直接运行，类似于</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">绿色免安装</font>`<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">例如下载</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">TensorRT-7.2.3.4.Ubuntu-18.04.x86_64-gnu.cuda-11.1.cudnn8.1.tar.gz</font>`<font style="color:rgb(25, 27, 31);">，下载好后，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">tar -zxvf</font>`<font style="color:rgb(25, 27, 31);">解压即可。</font>

<font style="color:rgb(25, 27, 31);">解压之后我们需要添加</font>**<font style="color:rgb(25, 27, 31);">环境变量</font>**<font style="color:rgb(25, 27, 31);">，以便让我们的程序能够找到TensorRT的libs。</font>

```plain
vim ~/.bashrc
# 添加以下内容
export LD_LIBRARY_PATH=/path/to/TensorRT-7.2.3.4/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/TensorRT-7.2.3.4/lib::$LIBRARY_PATH
```

<font style="color:rgb(25, 27, 31);">这样TensorRT就安装好了。</font>

# oLLAMA
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Ollama 是一个开源框架，专为在本地机器上便捷部署和运行大型语言模型（</font>[<font style="color:rgb(9, 64, 142);">LLM</font>](https://zhida.zhihu.com/search?content_id=253739121&content_type=Article&match_order=1&q=LLM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）而设计。Ollama 是 Omni-Layer Learning Language Acquisition Model 的简写，这代表一种新颖的机器学习方法，承诺重新定义我们对语言习得和自然语言处理的看法。</font>****

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://ollama.com/download](https://ollama.com/download)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743474310217-2a4b34b4-9568-45b9-9231-1ecc36bb13f3.png)

:::color5
**<font style="color:#601BDE;">1.关键特性</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">本地执行</font>**<font style="color:rgb(25, 27, 31);">：Ollama 的一个显著特点是其能够本地运行 LLMs，减轻了与基于云的解决方案相关的隐私问题。通过将AI 模型直接带到用户的设备上，Ollama 确保了对数据的更大控制和安全性，同时提供了更快的处理速度和减少对外部服务器的依赖。</font>
+ **<font style="color:rgb(25, 27, 31);">丰富的模型库</font>**<font style="color:rgb(25, 27, 31);">：Ollama 提供了丰富的预训练 LLMs 库，包括流行的模型（如，Llama 3）。用户可以具体的需求，针对不同任务、领域和硬件能力，选择合适的模型，确保了 AI 项目的灵活性和多功能性。</font>
+ **<font style="color:rgb(25, 27, 31);">无缝集成</font>**<font style="color:rgb(25, 27, 31);">：Ollama 可与各种工具、框架和编程语言无缝集成，使开发者能够轻松地将 LLMs 纳入他们的工作流程中。无论是 Python、</font>[<font style="color:rgb(9, 64, 142);">LangChain</font>](https://zhida.zhihu.com/search?content_id=253739121&content_type=Article&match_order=1&q=LangChain&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">还是</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">LlamaIndex</font>](https://zhida.zhihu.com/search?content_id=253739121&content_type=Article&match_order=1&q=LlamaIndex&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，Ollama 为构建复杂的 AI 应用程序和解决方案提供了强大的集成选项。</font>
+ **<font style="color:rgb(25, 27, 31);">定制和微调</font>**<font style="color:rgb(25, 27, 31);">：有了 Ollama，用户有能力定制和微调 LLMs 以满足他们的特定需求和偏好。从提示工程到少样本学习和微调过程，Ollama 赋予用户塑造 LLMs 行为和输出的能力，确保它们与预期目标一致。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">创意写作和内容生成</font>**<font style="color:rgb(25, 27, 31);">：作家和内容创作者可以利用 Ollama 来克服写作障碍，头脑风暴内容创意，并在不同体裁和格式中生成多样化和吸引人的内容。</font>
+ **<font style="color:rgb(25, 27, 31);">代码生成和辅助</font>**<font style="color:rgb(25, 27, 31);">：开发人员可以利用 Ollama 的能力进行代码生成、解释、调试和文档编写，简化他们的开发工作流程并提高代码质量。</font>
+ **<font style="color:rgb(25, 27, 31);">语言翻译和本地化</font>**<font style="color:rgb(25, 27, 31);">：Ollama 的语言理解和生成能力使其成为翻译、本地化和多语言沟通的宝贵工具，促进跨文化理解和全球合作。</font>
+ **<font style="color:rgb(25, 27, 31);">研究和知识发现</font>**<font style="color:rgb(25, 27, 31);">：研究人员和知识工作者可以通过使用 Ollama，从大量的信息中进行分析、整合和提取洞察，提高知识获取的效率。涵盖文献综述、数据分析、假设生成和知识提取等场景。</font>
+ **<font style="color:rgb(25, 27, 31);">客户服务和支持</font>**<font style="color:rgb(25, 27, 31);">：企业可以部署由 Ollama 驱动的智能聊天机器人和虚拟助手，以增强客户服务，自动化常见问题解答，提供个性化的产品推荐，并分析客户反馈以提高满意度和参与度。</font>
+ **<font style="color:rgb(25, 27, 31);">医疗保健和医疗应用</font>**<font style="color:rgb(25, 27, 31);">：在医疗保健行业，Ollama 可以协助医疗文档编写、临床决策支持、患者教育、远程医疗和医学研究，提升医疗保健效率。</font>

:::color5
**<font style="color:#601BDE;">3.安装 </font>**

:::

<font style="color:rgb(25, 27, 31);">以 windows 系统为例，安装步骤如下：</font>

**<font style="color:rgb(25, 27, 31);">下载</font>**

<font style="color:rgb(25, 27, 31);">进入官网下载页面（</font>[https://ollama.com/download](https://link.zhihu.com/?target=https%3A//ollama.com/download)<font style="color:rgb(25, 27, 31);">），选择 windows 版本下载</font>

**<font style="color:rgb(25, 27, 31);">安装</font>**

<font style="color:rgb(25, 27, 31);">点击安装文件 OllamaSetup.exe，可直接进行安装。默认情况下，会安装在 C 盘上，会占用 C 盘的存储空间。可通过以下方式，变更 ollama 的安装路径：</font>

<font style="color:rgb(25, 27, 31);">打开 powershell，进入 OllamaSetup.exe，运行以下命令后（DIR 路径为安装路径，如"E:\developToolkit\ollama"） ，会出现安装弹框，点击 Install，即可将 Ollama 安装到指定的路径。</font>

```powershell
OllamaSetup.exe /DIR="E:\developToolkit\ollama"
```

<font style="color:rgb(25, 27, 31);">安装完成后，在 powershell 输入 "ollama -v "，输出 Ollama 的版本信息，说明已安装成功。</font>

:::color5
**<font style="color:#601BDE;">4.改变存储位置</font>**

:::

<font style="color:rgb(25, 27, 31);">要改变 Ollama 存储下载模型的位置（默认是存储在 C 盘的用户目录，会占用 C 盘的大量存储空间），可通过设置环境变量 OLLAMA_MODELS 的方式，设置大模型的存储位置。</font>

1. <font style="color:rgb(25, 27, 31);">启动设置（Windows 11）或控制面板（Windows 10）应用程序，并搜索环境变量。</font>
2. <font style="color:rgb(25, 27, 31);">点击为环境变量。点击新建一个系统变量。</font>
3. <font style="color:rgb(25, 27, 31);">编辑或创建一个新的变量 OLLAMA_MODELS ，指定希望模型存储的位置。</font>
4. <font style="color:rgb(25, 27, 31);">点击确定/应用以保存。</font>

:::color5
**<font style="color:#601BDE;">5.选择大模型</font>**

:::

<font style="color:rgb(25, 27, 31);">进入 Ollama 的模型页面，选择要运行的大模型：</font>[https://ollama.com/search](https://link.zhihu.com/?target=https%3A//ollama.com/search)

<font style="color:rgb(25, 27, 31);">  
</font>

# vLLM
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#ED740C;">VLLM (VersatileLargeLanguageModel)是⼀个专⻔为⼤规模语⾔模型 (LLM) 推理设计的开源加速框架，通过创新的内存管理和并⾏化技术，显著提⾼了推理速度和吞吐量。</font>**<font style="color:#1f2329;">其中，</font>**<font style="color:#ED740C;">PagedAttention</font>**<font style="color:#1f2329;">是VLLM 的核⼼技术，专⻔⽤于解决 LLM 推理中的内存瓶颈问题，尤其是⾃回归⽣成任务中的键值 (KV) 缓存管理。</font>

<font style="color:#1f2329;">项目地址：</font>[https://github.com/vllm-project/vllm/releases](https://github.com/vllm-project/vllm/releases)

:::

:::color5
**<font style="color:#601BDE;">1.核心技术解析</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. PageAttention 内存优化</font>**

+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：传统 KV 缓存管理存在显存碎片化问题，导致 GPU 利用率低下（通常仅 20-30%）。</font>
+ **<font style="color:rgb(51, 51, 51);">方案</font>**<font style="color:rgb(51, 51, 51);">：引入虚拟内存分页机制，将 KV 缓存划分为固定大小的块（如 16 层 x 16 头 x 256 tokens），实现动态分配与复用。</font>
+ **<font style="color:rgb(51, 51, 51);">效果</font>**<font style="color:rgb(51, 51, 51);">：在 Qwen2.5-7B 实测中，显存碎片减少 70%，单卡 A100 可处理的并发请求数从 5 提升至 20。</font>

**<font style="color:rgb(51, 51, 51);">2. 连续批处理（Continuous Batching）</font>**

+ **<font style="color:rgb(51, 51, 51);">动态请求合并</font>**<font style="color:rgb(51, 51, 51);">：将不同序列的请求拼接为统一张量，自动填充和掩码处理。例如，将用户查询 "连衣裙推荐" 和 "如何退换货？" 合并为一批。</font>
+ **<font style="color:rgb(51, 51, 51);">逻辑流</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
# 伪代码示例：vLLM 动态批处理
requests = [decode("连衣裙推荐"), decode("如何退换货？")]
batch = concatenate_padded(requests)  # 自动填充为相同长度
output = model.generate(batch)
```

**<font style="color:rgb(51, 51, 51);">3. 量化支持</font>**

+ <font style="color:rgb(51, 51, 51);">支持 AWQ（Activation-aware Weight Quantization）和 GPTQ，Qwen2.5-7B 经 4-bit 量化后显存占用从 14GB 降至 5GB，延迟降低 40%。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">吞吐量提升2-4倍</font> | <font style="color:rgb(51, 51, 51);">仅支持部分模型架构（如GPT、LLAMA）</font> |
| <font style="color:rgb(51, 51, 51);">显存利用率提高，支持更长序列</font> | <font style="color:rgb(51, 51, 51);">需CUDA环境，不支持非NVIDIA GPU</font> |
| <font style="color:rgb(51, 51, 51);">低延迟，适合高并发</font> | <font style="color:rgb(51, 51, 51);">动态批处理对极端长度差异敏感</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">在线推理服务</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">如聊天机器人、API服务，需处理数千QPS的请求。</font>
2. **<font style="color:rgb(51, 51, 51);">批量文本生成</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">广告文案、代码生成等大规模任务。</font>
3. **<font style="color:rgb(51, 51, 51);">研究实验</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">快速迭代不同采样策略（温度、top-p）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合分块策略</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">动态调整块大小（如短序列用小块，长序列用大块）。</font>
2. **<font style="color:rgb(51, 51, 51);">量化集成</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">结合4-bit量化，进一步压缩显存。</font>
3. **<font style="color:rgb(51, 51, 51);">异构内存管理</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">使用CPU内存扩展缓存能力（类似HBM-SSD分层存储）。</font>
4. **<font style="color:rgb(51, 51, 51);">模型架构适配</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">扩展支持MQA（Multi-Query Attention）和MoE架构。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from vllm import LLM, SamplingParams

# 定义模型和采样参数
model = LLM(model="meta-llama/Llama-2-7b-chat-hf", tensor_parallel_size=2)  # 张量并行
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)

# 批量推理
prompts = ["A robot may not injure a human being,",
           "The capital of France is"]
outputs = model.generate(prompts, sampling_params)

# 输出结果
for output in outputs:
    print(f"Prompt: {output.prompt}\n"
          f"Generated text: {output.outputs[0].text}\n")

```

```python
model = LLM(
    model="gpt2",
    max_num_seqs=256,  # 最大并发数
    block_size=16,     # 块大小（token数）
    gpu_memory_utilization=0.9  # 显存利用率阈值
)

```



## <font style="color:#6425d0;">PagedAttention机制</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Page Attention 是一种针对长序列处理优化的注意力机制，旨在降低传统自注意力的内存和计算开销，同时保持对长距离依赖的建模能力。其核心思想借鉴计算机系统中的</font>**<font style="color:#ED740C;">分页机制</font>**<font style="color:rgb(51, 51, 51);">，将输入序列分割为多个“页面”（块），动态管理这些块的计算和存储，从而优化资源使用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

1. **传统自注意力瓶颈**  
Transformer的自注意力复杂度为O(N²)，在处理长序列时显存占用激增，尤其在大batch size下，成为训练/推理的主要瓶颈。
2. **分页管理思想**  
Page Attention将输入序列划分为固定大小的页面（Page），每个页面包含连续的token。计算注意力时：
    - **<font style="color:rgb(51, 51, 51);">页面内（Intra-Page）</font>**<font style="color:rgb(51, 51, 51);">：计算当前页面内所有token间的局部注意力。</font>
    - **<font style="color:rgb(51, 51, 51);">页面间（Inter-Page）</font>**<font style="color:rgb(51, 51, 51);">：按需加载其他页面，计算跨页面的稀疏注意力（如相邻页或关键页）。</font>
3. **动态加载机制**  
通过类似虚拟内存的换页策略，仅保留活跃页面在高速内存（如GPU显存）中，非活跃页面暂存于低速内存（如CPU内存或磁盘），按需动态交换，显著降低峰值显存占用。

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">假设输入序列长度N，页面大小P，总页数M=N/P：</font>

1. **分块（Paging）**  
将输入序列划分为M个页面：`X = [X₁, X₂, ..., Xₘ]`，每个Xᵢ ∈ ℝ^{P×d}。
2. **页面内注意力**  
对每个页面Xᵢ，计算局部注意力输出Oᵢ：

```python
Qᵢ, Kᵢ, Vᵢ = XᵢW_Q, XᵢW_K, XᵢW_V
Aᵢ = softmax(QᵢKᵢ^T / √d)  # 形状 [P, P]
Oᵢ = AᵢVᵢ                   # 形状 [P, d]
```

3. **页面间注意力**  
根据策略（如滑动窗口、关键页选择）加载相关页面Xⱼ，计算跨页面注意力：

```python
Qᵢ, Kⱼ, Vⱼ = XᵢW_Q, XⱼW_K, XⱼW_V
Aᵢⱼ = softmax(QᵢKⱼ^T / √d)  # 形状 [P, P]
Oᵢⱼ = AᵢⱼVⱼ                  # 形状 [P, d]
```

4. **结果聚合**  
合并页面内和跨页面结果，得到最终输出：

```python
Oᵢ = Oᵢ + ∑ⱼ∈Neighbor(i) Oᵢⱼ
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

  
**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">显存优化</font>**<font style="color:rgb(51, 51, 51);">：显存占用从O(N²)降至O(MP²)，M为页面数。</font>
+ **<font style="color:rgb(51, 51, 51);">计算高效</font>**<font style="color:rgb(51, 51, 51);">：分块计算利于并行化和硬件加速。</font>
+ **<font style="color:rgb(51, 51, 51);">扩展性强</font>**<font style="color:rgb(51, 51, 51);">：支持超长序列处理（如百万级token）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">块间跳转可能引入额外内存访问开销。</font>
+ <font style="color:rgb(51, 51, 51);">块大小需调优，过小会增加管理开销，过大可能浪费内存。</font>  


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">处理超长文本（如文档摘要、代码生成）。</font>
+ <font style="color:rgb(51, 51, 51);">高并发场景下多序列并行推理（如聊天服务器）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态块大小</font>**<font style="color:rgb(51, 51, 51);">：根据序列长度动态调整块大小。</font>
+ **<font style="color:rgb(51, 51, 51);">块预取</font>**<font style="color:rgb(51, 51, 51);">：预测未来需要的块，提前加载到高速缓存。</font>
+ **<font style="color:rgb(51, 51, 51);">异构存储</font>**<font style="color:rgb(51, 51, 51);">：将低频访问的块迁移到CPU内存或磁盘。</font>  


:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class PageAttention(nn.Module):
    def __init__(self, d_model, n_heads, page_size=64):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.page_size = page_size
        self.head_dim = d_model // n_heads
        
        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)
        
    def forward(self, x):
        # x: [batch, seq_len, d_model]
        B, N, d = x.shape
        P = self.page_size
        M = (N + P - 1) // P  # 计算总页数
        
        # 分页填充并调整形状
        x_padded = nn.functional.pad(x, (0,0,0, M*P - N))
        pages = rearrange(x_padded, 'b (m p) d -> b m p d', p=P)
        
        Q = self.Wq(pages)
        K = self.Wk(pages)
        V = self.Wv(pages)
        
        # 分头处理
        Q = rearrange(Q, 'b m p (h d) -> b h m p d', h=self.n_heads)
        K = rearrange(K, 'b m p (h d) -> b h m p d', h=self.n_heads)
        V = rearrange(V, 'b m p (h d) -> b h m p d', h=self.n_heads)
        
        outputs = []
        for m in range(M):
            # 页面内注意力
            intra_Q = Q[:, :, m]
            intra_K = K[:, :, m]
            intra_V = V[:, :, m]
            attn = torch.einsum('bhpd,bhqd->bhpq', intra_Q, intra_K) / (self.head_dim**0.5)
            attn = torch.softmax(attn, dim=-1)
            intra_out = torch.einsum('bhpq,bhqd->bhp d', attn, intra_V)
            
            # 页面间注意力（示例：关注前一页）
            if m > 0:
                inter_K = K[:, :, m-1]
                inter_V = V[:, :, m-1]
                inter_attn = torch.einsum('bhpd,bhqd->bhpq', intra_Q, inter_K) / (self.head_dim**0.5)
                inter_attn = torch.softmax(inter_attn, dim=-1)
                inter_out = torch.einsum('bhpq,bhqd->bhp d', inter_attn, inter_V)
                intra_out += inter_out
            
            outputs.append(intra_out)
        
        # 合并结果
        out = torch.cat(outputs, dim=2)
        out = rearrange(out, 'b h m p d -> b (m p) (h d)')[:, :N]  # 去除填充
        return self.out(out)

```



## <font style="color:#6425d0;">Continuous Batching机制</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Continuous Batching（连续批处理）是一种针对大模型推理优化的动态批处理技术，通过打破传统静态批处理的固定批次限制，在推理过程中</font>**<font style="color:rgb(51, 51, 51);">动态插入新请求</font>**<font style="color:rgb(51, 51, 51);">并</font>**<font style="color:rgb(51, 51, 51);">按需调整批次大小</font>**<font style="color:rgb(51, 51, 51);">，显著提升硬件利用率并降低请求延迟。其核心思想源自系统调度中的</font>**<font style="color:rgb(51, 51, 51);">流水线并行</font>**<font style="color:rgb(51, 51, 51);">，代表工作包括Orca、vLLM等推理框架的优化实现。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738837876714-8a7b7721-2a0f-49ee-8e9a-90cbef3079b2.png)

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

<font style="color:#1f2329;">另⼀个提升VLLM推理速度的重要机制是 </font>**<font style="color:#74B602;">ContinuousBatching</font>**<font style="color:#1f2329;">，它优化了批处理过程。</font>**<font style="color:#74B602;">传统的批处理⽅法（staticbatching）要求所有输⼊序列的⻓度对⻬，这意味着较短的句⼦需要等待较⻓句⼦⽣成完毕，导致 GPU 计算资源被浪费。</font>**

<font style="color:#1f2329;">VLLM 采⽤Continuous Batching，即每当某个句⼦的推理完成时，GPU 会⽴即填充下⼀个句⼦的</font><font style="color:black;">  </font><font style="color:#1f2329;">token，⽽</font>**<font style="color:#74B602;">不需要等待整个批次的推理完成</font>**<font style="color:#1f2329;">。这种动态的批次管理⽅式充分利⽤了 GPU 的计算能⼒，减少了等待时间，极⼤提⾼了吞吐量。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">请求队列管理</font>**<font style="color:rgb(51, 51, 51);">：维护等待队列（Pending Queue）和运行队列（Running Queue）。</font>
2. **<font style="color:rgb(51, 51, 51);">迭代处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">从等待队列中选择可运行的请求（基于最大批大小）。</font>
    - <font style="color:rgb(51, 51, 51);">合并所有运行中请求的输入，执行模型前向计算。</font>
    - <font style="color:rgb(51, 51, 51);">移除已生成结束符的请求，释放资源。</font>
3. **<font style="color:rgb(51, 51, 51);">状态更新</font>**<font style="color:rgb(51, 51, 51);">：将新生成的token追加到各请求的生成序列中。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">提升GPU利用率，减少空闲时间。</font>
    - <font style="color:rgb(51, 51, 51);">降低用户感知的延迟（尤其对短请求）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">调度算法复杂度高，需处理动态内存分配。</font>
    - <font style="color:rgb(51, 51, 51);">长尾请求可能阻塞批次整体进度。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">高吞吐量的在线推理服务（如GPT-4 API）。</font>
+ <font style="color:rgb(51, 51, 51);">流式生成场景（如实时翻译、语音助手）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优先级调度</font>**<font style="color:rgb(51, 51, 51);">：为高优先级请求分配更多资源。</font>
+ **<font style="color:rgb(51, 51, 51);">推测执行</font>**<font style="color:rgb(51, 51, 51);">：预先生成长度，减少迭代次数。</font>
+ **<font style="color:rgb(51, 51, 51);">混合批处理</font>**<font style="color:rgb(51, 51, 51);">：结合静态批处理处理离线任务。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class ContinuousBatcher:
    def __init__(self, max_batch_size=32):
        self.pending_queue = []
        self.running_queue = []
        self.max_batch_size = max_batch_size

    def add_request(self, input_text):
        self.pending_queue.append({"input": input_text, "output": []})

    def step(self, model):
        # 动态填充批次
        while len(self.running_queue) < self.max_batch_size and self.pending_queue:
            self.running_queue.append(self.pending_queue.pop(0))

        # 准备输入
        inputs = [req["output"][-1] if req["output"] else req["input"] for req in self.running_queue]
        input_ids = tokenizer(inputs, return_tensors="pt", padding=True).input_ids

        # 模型推理
        outputs = model.generate(input_ids, max_new_tokens=1)

        # 更新状态并移除完成请求
        new_running_queue = []
        for req, output in zip(self.running_queue, outputs):
            req["output"].append(output)
            if output != eos_token:
                new_running_queue.append(req)
        self.running_queue = new_running_queue

```



## <font style="color:rgb(51, 51, 51);">基于 Qwen2.5+vLLM 的电商场景用户意图理解</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">任务</font>**<font style="color:rgb(51, 51, 51);">：解析用户自然语言查询（如 "帮我找透气性好的运动鞋"），提取意图（购买、比价、售后）和关键实体（商品类型、属性）。</font>
+ **<font style="color:rgb(51, 51, 51);">挑战</font>**<font style="color:rgb(51, 51, 51);">：电商场景 QPS 高峰达 1000+，要求响应时间 <200ms，传统部署方案（如原生 PyTorch）难以满足。</font>

:::

:::color5
**<font style="color:#601BDE;">1.部署流程</font>**

:::

**<font style="color:rgb(51, 51, 51);">步骤 1：环境准备</font>**

```bash
# 安装 vLLM 及依赖
pip install vllm==0.4.1
pip install transformers==4.40.0

# 下载 Qwen2.5-7B 模型
from huggingface_hub import snapshot_download
snapshot_download("Qwen/Qwen2.5-7B-Instruct")
```

**<font style="color:rgb(51, 51, 51);">步骤 2：启动 vLLM 服务</font>**

```python
from vllm import EngineArgs, LLMEngine

engine_args = EngineArgs(
    model="Qwen2.5-7B-Instruct",
    tensor_parallel_size=2,  # 双卡并行
    quantization="awq",
    max_num_seqs=256,        # 最大并发数
)
engine = LLMEngine.from_engine_args(engine_args)
```

**<font style="color:rgb(51, 51, 51);">步骤 3：定义意图解析 Prompt</font>**

```python
INTENT_PROMPT = """作为电商助手，请分析用户意图：
1. 意图类别：购买、比价、退换货、咨询属性
2. 提取实体：商品类型、品牌、属性

用户输入：{query}
输出JSON：
{
  "intent": "...",
  "entities": {"商品类型": "...", "品牌": "...", ...}
}"""
```

**<font style="color:rgb(51, 51, 51);">步骤 4：批量推理</font>**

```python
# 使用异步处理应对高并发
async def handle_request(query):
    sampling_params = SamplingParams(temperature=0, max_tokens=200)
    request_id = str(uuid.uuid4())
    engine.add_request(request_id, INTENT_PROMPT.format(query=query), sampling_params)

    while True:
        step_outputs = engine.step()
        if request_id in step_outputs:
            return step_outputs[request_id].outputs[0].text
```

:::color5
**<font style="color:#601BDE;">2.性能优化对比</font>**

:::

| **标** | **原始 PyTorch** | **vLLM 优化后** | **提升倍数** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">吞吐量 (req/s)</font> | <font style="color:rgb(51, 51, 51);">32</font> | <font style="color:rgb(51, 51, 51);">215</font> | <font style="color:rgb(51, 51, 51);">6.7x</font> |
| <font style="color:rgb(51, 51, 51);">单请求延迟 (p95)</font> | <font style="color:rgb(51, 51, 51);">680ms</font> | <font style="color:rgb(51, 51, 51);">150ms</font> | <font style="color:rgb(51, 51, 51);">4.5x</font> |
| <font style="color:rgb(51, 51, 51);">显存占用 (7B模型)</font> | <font style="color:rgb(51, 51, 51);">14.3GB</font> | <font style="color:rgb(51, 51, 51);">6.8GB</font> | <font style="color:rgb(51, 51, 51);">2.1x</font> |


:::color5
**<font style="color:#601BDE;">3.电商场景应用</font>**

:::

<font style="color:rgb(51, 51, 51);">1. 多轮对话管理</font>

```python
# 使用 vLLM 的会话缓存
from vllm import AsyncLLMEngine

class DialogManager:
    def __init__(self):
        self.sessions = {}  # {user_id: vllm.Session}

    async def respond(self, user_id, message):
        session = self.sessions.get(user_id, engine.create_session())
        prompt = build_dialog_prompt(message, session.history)
        output = await engine.generate(prompt, session)
        session.history.append({"user": message, "assistant": output})
        return output
```

<font style="color:rgb(51, 51, 51);">2. 意图路由架构</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740654417006-67d2309e-d7fb-47df-9bf4-27c15bc8a4ce.png)

:::color5
**<font style="color:#601BDE;">4.实践建议</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合精度推理</font>**<font style="color:rgb(51, 51, 51);">：开启</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">dtype="bfloat16"</font>`<font style="color:rgb(51, 51, 51);">，在 A100 上可获得 1.2-1.5 倍加速。</font>
2. **<font style="color:rgb(51, 51, 51);">预热策略</font>**<font style="color:rgb(51, 51, 51);">：预先加载 10-20 个虚拟请求，避免冷启动造成的首批延迟波动。</font>
3. **<font style="color:rgb(51, 51, 51);">监控体系</font>**<font style="color:rgb(51, 51, 51);">：使用 Prometheus 采集 GPU 内存/利用率、请求队列深度等指标，设置自动扩缩容策略。</font>
4. **优化方向**：
    1. **<font style="color:rgb(51, 51, 51);">与RAG结合</font>**<font style="color:rgb(51, 51, 51);">：将商品知识库通过 vLLM 的</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">ExternalData</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">接口接入，增强推荐精准度。</font>
    2. **<font style="color:rgb(51, 51, 51);">流式输出</font>**<font style="color:rgb(51, 51, 51);">：利用</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">stream=True</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">参数实现逐字生成，提升用户体验。</font>
    3. **<font style="color:rgb(51, 51, 51);">多模态扩展</font>**<font style="color:rgb(51, 51, 51);">：适配 Qwen-VL 模型，支持 "图片+文本" 联合意图分析。</font>



