# Agent框架对比

<!-- source: yuque://zhongxian-iiot9/hlyypb/ati6k8sk8iivlozu -->

:::success
**<font style="color:rgb(0, 0, 0);">Agent框架推荐</font>**<font style="color:rgb(0, 0, 0);">：LLM框架该如何选择，全面对比MaxKB、Dify、FastGPT、RagFlow、Anything-LLM,以及更多推荐</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点对比</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031694991-eb9f1dec-c4f1-4869-ac8a-835da8b4b86f.png)

:::color5
**<font style="color:#601BDE;">2.更多框架推荐</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031682332-b4334dfd-cb14-408d-ba23-60413f8526f9.png)

# MaxKB<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**简介：****<font style="color:rgb(51, 51, 51);">MaxKB = Max Knowledge Base</font>**<font style="color:rgb(51, 51, 51);">，是一款基于 LLM 大语言模型的开源知识库问答系统，旨在成为企业的最强大脑。它能够帮助企业高效地管理知识，并提供智能问答功能。想象一下，你有一个虚拟助手，可以回答各种关于公司内部知识的问题，无论是政策、流程，还是技术文档，MaxKB 都能快速准确地给出答案:比如公司内网如何访问、如何提交视觉设计需求等等</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://maxkb.cn/](https://maxkb.cn/)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031030048-1907f1e3-cab7-4207-8af6-cfeb05d93389.png)

:::color5
**<font style="color:#601BDE;">1.简介</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">开箱即用</font>`<font style="color:rgb(51, 51, 51);">：支持直接上传文档、自动爬取在线文档，支持文本自动拆分、向量化、RAG（检索增强生成），智能问答交互体验好； </font>
2. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">无缝嵌入</font>`<font style="color:rgb(51, 51, 51);">：支持零编码快速嵌入到第三方业务系统，让已有系统快速拥有智能问答能力，提高用户满意度；</font>
3. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">灵活编排</font>`<font style="color:rgb(51, 51, 51);">：内置强大的工作流引擎，支持编排 AI 工作流程，满足复杂业务场景下的需求；</font>
4. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">模型中立</font>`<font style="color:rgb(51, 51, 51);">：支持对接各种大语言模型，包括本地私有大模型（Llama 3 / Qwen 2 等）、国内公共大模型（通义千问 / 智谱 AI / 百度千帆 / Kimi / DeepSeek 等）和国外公共大模型（OpenAI / Azure OpenAI / Gemini 等）。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031037706-9909bb2e-7502-4ee9-aca1-6306ebb91132.png)

:::color5
**<font style="color:#601BDE;">2.技术框架和原理</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031047893-35ab2b93-b83e-4db4-864d-174b7de18fd8.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031056511-a617222c-2189-48f1-84c1-dced3f3dc625.png)

:::color5
**<font style="color:#601BDE;">3.技术栈</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ 前端：Vue.js、logicflow
+ 后端：Python / Django
+ Langchain：Langchain
+ [向量数据库](https://cloud.tencent.com/product/vdb?from_column=20065&from=20065)：PostgreSQL / pgvector
+ 大模型：Ollama、Azure OpenAI、OpenAI、通义千问、Kimi、百度千帆大模型、讯飞星火、Gemini、DeepSeek等。



# Dify<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">Dify 是一款开源的大语言模型(LLM) 应用开发平台。它融合了后端即服务（Backend as Service）和 LLMOps 的理念，使开发者可以快速搭建生产级的生成式 AI 应用。即使你是非技术人员，也能参与到 AI 应用的定义和数据运营过程中。</font>

<font style="color:rgb(51, 51, 51);">由于 Dify 内置了构建 LLM 应用所需的关键技术栈，包括对数百个模型的支持、直观的 Prompt 编排界面、高质量的 RAG 引擎、稳健的 Agent 框架、灵活的流程编排，并同时提供了一套易用的界面和 </font><font style="color:rgb(0, 82, 217);">API</font><font style="color:rgb(51, 51, 51);">。这为开发者节省了许多重复造轮子的时间，使其可以专注在创新和业务需求上</font>

**<font style="color:rgb(51, 51, 51);">官网</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://dify.ai/zh](https://dify.ai/zh )<font style="color:rgb(51, 51, 51);"> </font>

**<font style="color:rgb(51, 51, 51);">github</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/langgenius/dify?tab=readme-ov-file](https://github.com/langgenius/dify?tab=readme-ov-file)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031161017-97c93a06-5ed2-41f4-901b-ef2493e38183.png)

:::color5
**<font style="color:#601BDE;">1.简介</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(51, 51, 51);">Dify 是一个开源的 LLM 应用开发平台。其直观的界面结合了 AI 工作流、RAG 管道、Agent、模型管理、可观测性功能等，让您可以快速从原型到生产。以下是其核心功能列表：</font>

1. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">工作流</font>`<font style="color:rgb(51, 51, 51);">: 在画布上构建和测试功能强大的 AI 工作流程，利用以下所有功能以及更多功能。 </font>
2. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">全面的模型支持</font>`<font style="color:rgb(51, 51, 51);">: 与数百种专有/开源 LLMs 以及数十种推理提供商和自托管解决方案无缝集成，涵盖 GPT、Mistral、Llama3 以及任何与 OpenAI API 兼容的模型。 </font>
3. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">Prompt IDE</font>`<font style="color:rgb(51, 51, 51);">: 用于制作提示、比较模型性能以及向基于聊天的应用程序添加其他功能（如文本转语音）的直观界面。 </font>
4. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">RAG Pipeline</font>`<font style="color:rgb(51, 51, 51);">: 广泛的 RAG 功能，涵盖从文档摄入到检索的所有内容，支持从 PDF、PPT 和其他常见文档格式中提取文本的开箱即用的支持。 </font>
5. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">Agent 智能体</font>`<font style="color:rgb(51, 51, 51);">: 您可以基于 LLM 函数调用或 ReAct 定义 Agent，并为 Agent 添加预构建或自定义工具。Dify 为 AI Agent 提供了50多种内置工具，如谷歌搜索、DELL·E、Stable Diffusion 和 WolframAlpha 等。 </font>
6. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">LLMOps</font>`<font style="color:rgb(51, 51, 51);">: 随时间监视和分析应用程序日志和性能。您可以根据生产数据和标注持续改进提示、数据集和模型。 </font>
7. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">后端即服务</font>`<font style="color:rgb(51, 51, 51);">: 所有 Dify 的功能都带有相应的 API，因此您可以轻松地将 Dify 集成到自己的业务逻辑中。 </font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031180104-a0f00c31-98bc-4bbe-8792-f38ed44c7317.png)

:::color5
**<font style="color:#601BDE;">2.系统框架</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031188405-83d8c2a6-e62d-4bd5-8d92-7f4c5e3964fc.png)

<font style="color:rgb(51, 51, 51);">工作流通过将复杂的任务分解成较小的步骤（节点）降低系统复杂度，减少了对提示词技术和模型推理能力的依赖，提高了 LLM 应用面向复杂任务的性能，提升了系统的可解释性、稳定性和容错性。</font>

<font style="color:rgb(51, 51, 51);">Dify 工作流分为两种类型：</font>

+ <font style="color:rgb(51, 51, 51);"> Chatflow：面向对话类情景，包括客户服务、语义搜索、以及其他需要在构建响应时进行多步逻辑的对话式应用程序。 </font>
+ <font style="color:rgb(51, 51, 51);"> Workflow：面向自动化和批处理情景，适合高质量翻译、</font><font style="color:rgb(0, 82, 217);">数据分析</font><font style="color:rgb(51, 51, 51);">、内容生成、电子邮件自动化等应用程序。 </font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031207067-55b4d376-0c91-42ef-a489-e2a0f00a70ae.png)

<font style="color:rgb(51, 51, 51);">为解决自然语言输入中用户意图识别的复杂性，Chatflow 提供了问题理解类节点。相对于 Workflow 增加了 Chatbot 特性的支持，如：对话历史（Memory）、标注回复、Answer 节点等。</font>

<font style="color:rgb(51, 51, 51);">为解决自动化和批处理情景中复杂业务逻辑，工作流提供了丰富的逻辑节点，如代码节点、IF/ELSE 节点、模板转换、迭代节点等，除此之外也将提供定时和事件触发的能力，方便构建自动化流程。</font>

:::color5
**<font style="color:#601BDE;">3.常见案例</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ 客户服务：通过将 LLM 集成到您的客户服务系统中，您可以自动化回答常见问题，减轻支持团队的工作负担。 LLM 可以理解客户查询的上下文和意图，并实时生成有帮助且准确的回答。 
+  内容生成：无论您需要创建博客文章、产品描述还是营销材料，LLM 都可以通过生成高质量内容来帮助您。只需提供一个大纲或主题，LLM将利用其广泛的知识库来制作引人入胜、信息丰富且结构良好的内容。 
+  任务自动化：可以与各种任务管理系统集成，如 Trello、Slack、Lark、以自动化项目和任务管理。通过使用[自然语言处理](https://cloud.tencent.com/product/nlp?from_column=20065&from=20065)，LLM 可以理解和解释用户输入，创建任务，更新状态和分配优先级，无需手动干预。 
+  数据分析和报告：可以用于分析大型数据集并生成报告或摘要。通过提供相关信息给 LLM，它可以识别趋势、模式和洞察力，将原始数据转化为可操作的智能。对于希望做出数据驱动决策的企业来说，这尤其有价值。 
+  邮件自动化处理：LLM 可以用于起草电子邮件、社交媒体更新和其他形式的沟通。通过提供简要的大纲或关键要点，LLM 可以生成一个结构良好、连贯且与上下文相关的信息。这样可以节省大量时间，并确保您的回复清晰和专业。

:::color5
**<font style="color:#601BDE;">4.优缺点</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:rgb(63, 63, 63);">优势：</font>**

+ <font style="color:rgb(63, 63, 63);">国际化支持：主要面向海外市场，集成多语言模型和国际化工具。</font>
+ <font style="color:rgb(63, 63, 63);">灵活性与扩展性：支持自托管和云服务，可无缝集成企业现有系统，满足数据安全和合规需求。</font>
+ <font style="color:rgb(63, 63, 63);">活跃开发者生态：开源社区提供丰富的模板和协作机会，支持快速迭代创新（如Workflow可视化流程）。</font>
+ <font style="color:rgb(63, 63, 63);">多模型对比：支持同时测试不同模型（如GPT-4与Claude3）的响应，优化任务适配性。</font>

**<font style="color:rgb(63, 63, 63);">劣势：</font>**

+ <font style="color:rgb(63, 63, 63);">学习门槛较高：模型集成和配置需要技术背景，对新手不友好。</font>
+ <font style="color:rgb(63, 63, 63);">国内生态较弱：与Coze相比，国内市场份额和插件支持有限。</font>

# FastGPT<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">FastGPT是一个功能强大的平台，专注于知识库训练和自动化工作流程的编排。它提供了一个简单易用的可视化界面，支持自动</font><font style="color:rgb(0, 82, 217);">数据预处理</font><font style="color:rgb(51, 51, 51);">和基于Flow模块的工作流编排。FastGPT支持创建RAG系统，提供自动化工作流程等功能，使得构建和使用RAG系统变得简单，无需编写复杂代码。</font>

**<font style="color:rgb(51, 51, 51);">官方</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://fastgpt.in/ ](https://fastgpt.in/ )

**<font style="color:rgb(51, 51, 51);">github</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/labring/FastGPT ](https://github.com/labring/FastGPT )

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031394847-e82fffa1-ed45-4c56-ab11-8c9197f3882f.png)

:::color5
**<font style="color:#601BDE;">1.简介</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">专属 AI 客服</font>`<font style="color:rgb(51, 51, 51);"> ：通过导入文档或已有问答对进行训练，让 AI 模型能根据你的文档以交互式对话方式回答问题。 </font>
    - <font style="color:rgb(102, 102, 102);">多库复用，混用</font>
    - <font style="color:rgb(102, 102, 102);">chunk 记录修改和删除</font>
    - <font style="color:rgb(102, 102, 102);">源</font><font style="color:rgb(0, 82, 217);">文件存储</font>
    - <font style="color:rgb(102, 102, 102);">支持手动输入，直接分段，QA 拆分导入</font>
    - <font style="color:rgb(102, 102, 102);">支持 txt，md，html，pdf，docx，pptx，csv，xlsx (有需要更多可 PR file loader)</font>
    - <font style="color:rgb(102, 102, 102);">支持 url 读取、CSV 批量导入</font>
    - <font style="color:rgb(102, 102, 102);">混合检索 & 重排</font>
2. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">简单易用的可视化界面</font>`<font style="color:rgb(51, 51, 51);"> ：FastGPT 采用直观的可视化界面设计，为各种应用场景提供了丰富实用的功能。通过简洁易懂的操作步骤，可以轻松完成 AI 客服的创建和训练流程。</font>
3. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">自动数据预处理</font>`<font style="color:rgb(51, 51, 51);">：提供手动输入、直接分段、LLM 自动处理和 CSV 等多种数据导入途径，其中“直接分段”支持通过 PDF、WORD、Markdown 和 CSV 文档内容作为上下文。FastGPT 会自动对文本数据进行预处理、向量化和 QA 分割，节省手动训练时间，提升效能。</font>
4. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">工作流编排</font>`<font style="color:rgb(51, 51, 51);"> ：基于 Flow 模块的工作流编排，可以帮助你设计更加复杂的问答流程。例如查询</font><font style="color:rgb(0, 82, 217);">数据库</font><font style="color:rgb(51, 51, 51);">、查询库存、预约实验室等。 </font>
    - <font style="color:rgb(102, 102, 102);">提供简易模式，无需操作编排</font>
    - <font style="color:rgb(102, 102, 102);">工作流编排</font>
    - <font style="color:rgb(102, 102, 102);">工具调用</font>
    - <font style="color:rgb(102, 102, 102);">插件 - 工作流封装能力</font>
    - <font style="color:rgb(102, 102, 102);">Code sandbox</font>
5. `<font style="color:rgb(10, 191, 91);background-color:rgb(243, 245, 249);">强大的 API 集成 </font>`<font style="color:rgb(51, 51, 51);">：FastGPT 对外的 API 接口对齐了 OpenAI 官方接口，可以直接接入现有的 GPT 应用，也可以轻松集成到企业微信、公众号、飞书等平台。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031405380-9285c9be-c463-4c19-a570-9497f440e3f1.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:rgb(63, 63, 63);">优势：</font>**

+ <font style="color:rgb(63, 63, 63);">垂直领域优势：在知识库构建和复杂问答场景表现突出，支持高度定制化功能。</font>
+ <font style="color:rgb(63, 63, 63);">开源与可扩展性：吸引开发者贡献，适合需要自主优化的团队。</font>

**<font style="color:rgb(63, 63, 63);">劣势：</font>**

+ <font style="color:rgb(63, 63, 63);">部署复杂：需要技术背景配置，对初学者不友好。</font>
+ <font style="color:rgb(63, 63, 63);">生态局限：国际化支持较弱，插件和模型集成选项少于Dify和Coze。</font>



# RagFlow<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">RAGFlow 是一款基于深度文档理解构建的开源 RAG（Retrieval-Augmented Generation）引擎。RAGFlow 可以为各种规模的企业及个人提供一套精简的 RAG 工作流程，结合大语言模型（LLM）针对用户各类不同的复杂格式数据提供可靠的问答以及有理有据的引用。</font>

**<font style="color:rgb(51, 51, 51);">官网</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://ragflow.io/](https://ragflow.io/)

**<font style="color:rgb(51, 51, 51);">Github</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/infiniflow/ragflow/blob/main](https://github.com/infiniflow/ragflow/blob/main)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031462073-5042a05b-c27b-4dba-ba69-a884ede18985.png)

:::color5
**<font style="color:#601BDE;">1.功能介绍</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ <font style="color:rgb(51, 51, 51);"> “Quality in, quality out” </font>
    - <font style="color:rgb(102, 102, 102);">基于深度文档理解，能够从各类复杂格式的非</font><font style="color:rgb(0, 82, 217);">结构化数据</font><font style="color:rgb(102, 102, 102);">中提取真知灼见。</font>
    - <font style="color:rgb(102, 102, 102);">真正在无限上下文（token）的场景下快速完成大海捞针测试。</font>
+ <font style="color:rgb(51, 51, 51);"> 基于模板的文本切片 </font>
    - <font style="color:rgb(102, 102, 102);">不仅仅是智能，更重要的是可控可解释。</font>
    - <font style="color:rgb(102, 102, 102);">多种文本模板可供选择</font>
+ <font style="color:rgb(51, 51, 51);"> 有理有据、最大程度降低幻觉（hallucination） </font>
    - <font style="color:rgb(102, 102, 102);">文本切片过程可视化，支持手动调整。</font>
    - <font style="color:rgb(102, 102, 102);">有理有据：答案提供关键引用的快照并支持追根溯源。</font>
+ <font style="color:rgb(51, 51, 51);"> 兼容各类异构数据源 </font>
    - <font style="color:rgb(102, 102, 102);">支持丰富的文件类型，包括 Word 文档、PPT、excel 表格、txt 文件、图片、PDF、影印件、复印件、结构化数据、网页等。</font>
+ <font style="color:rgb(51, 51, 51);"> 全程无忧、自动化的 RAG 工作流 </font>
    - <font style="color:rgb(102, 102, 102);">全面优化的 RAG 工作流可以支持从个人应用乃至超大型企业的各类生态系统。</font>
    - <font style="color:rgb(102, 102, 102);">大语言模型 LLM 以及向量模型均支持配置。</font>
    - <font style="color:rgb(102, 102, 102);">基于多路召回、融合重排序。</font>
    - <font style="color:rgb(102, 102, 102);">提供易用的 API，可以轻松集成到各类企业系统。</font>
+ <font style="color:rgb(51, 51, 51);"> 最近更新功能 </font>
    - <font style="color:rgb(102, 102, 102);">2024-07-23 支持解析音频文件.</font>
    - <font style="color:rgb(102, 102, 102);">2024-07-21 支持更多的大模型供应商(LocalAI/OpenRouter/StepFun/Nvidia).</font>
    - <font style="color:rgb(102, 102, 102);">2024-07-18 在Graph中支持算子：Wikipedia，PubMed，Baidu和Duckduckgo.</font>
    - <font style="color:rgb(102, 102, 102);">2024-07-08 支持 Agentic RAG: 基于 Graph 的工作流。</font>

:::color5
**<font style="color:#601BDE;">2.系统架构</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031484278-2661561f-7685-4a83-a21b-868406b9ce39.png)



# <font style="color:rgb(0, 0, 0);">Anything-LLM</font><font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">AnythingLLM是一个全栈应用程序，您可以使用现成的商业大语言模型或流行的开源大语言模型，再结合向量</font>[<font style="color:rgb(0, 82, 217);">数据库解决方案</font>](https://cloud.tencent.com/solution/database?from_column=20065&from=20065)<font style="color:rgb(51, 51, 51);">构建一个私有</font><font style="color:rgb(0, 82, 217);">ChatGPT</font><font style="color:rgb(51, 51, 51);">，不再受制于人：您可以本地运行，也可以远程托管，并能够与您提供的任何文档智能聊天。</font>

<font style="color:rgb(51, 51, 51);">AnythingLLM将您的文档划分为称为workspaces (工作区)的对象。工作区的功能类似于线程，同时增加了文档的</font><font style="color:rgb(0, 82, 217);">容器</font><font style="color:rgb(51, 51, 51);">化，。工作区可以共享文档，但工作区之间的内容不会互相干扰或污染，因此您可以保持每个工作区的上下文清晰。</font>

**<font style="color:rgb(51, 51, 51);">官方</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://anythingllm.com/](https://anythingllm.com/)

**<font style="color:rgb(51, 51, 51);">github</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031581550-eff87650-9525-408d-8e56-07ab83e482f1.png)

:::color5
**<font style="color:#601BDE;">1.简介</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ <font style="color:rgb(51, 51, 51);"> AnythingLLM的一些特性 </font>
    - <font style="color:rgb(102, 102, 102);">多用户实例支持和权限管理</font>
    - <font style="color:rgb(102, 102, 102);">工作区内的智能体Agent（浏览网页、运行代码等）</font>
    - <font style="color:rgb(102, 102, 102);">为您的网站定制的可嵌入聊天窗口</font>
    - <font style="color:rgb(102, 102, 102);">支持多种文档类型（PDF、TXT、DOCX等）</font>
    - <font style="color:rgb(102, 102, 102);">通过简单的用户界面管理向量数据库中的文档</font>
    - <font style="color:rgb(102, 102, 102);">两种对话模式：聊天和查询。聊天模式保留先前的对话记录。查询模式则是是针对您的文档做简单问答</font>
    - <font style="color:rgb(102, 102, 102);">聊天中会提供所引用的相应文档内容</font>
    - <font style="color:rgb(102, 102, 102);">100%云部署就绪。</font>
    - <font style="color:rgb(102, 102, 102);">“部署你自己的LLM模型”。</font>
    - <font style="color:rgb(102, 102, 102);">管理超大文档时高效、低耗。只需要一次就可以嵌入（Embedding)一个庞大的文档或文字记录。比其他文档</font><font style="color:rgb(0, 82, 217);">聊天机器人</font><font style="color:rgb(102, 102, 102);">解决方案节省90%的成本。</font>
    - <font style="color:rgb(102, 102, 102);">全套的开发人员API，用于自定义集成！</font>
+ <font style="color:rgb(51, 51, 51);"> 支持的 LLM、嵌入模型和向量数据库 </font>
    - <font style="color:rgb(102, 102, 102);">LLM：包括任何开源的 llama.cpp 兼容模型、OpenAI、Azure OpenAI、Anthropic ClaudeV2、LM Studio 和 LocalAi。</font>
    - <font style="color:rgb(102, 102, 102);">嵌入模型：AnythingLLM 原生嵌入器、OpenAI、Azure OpenAI、LM Studio 和 LocalAi。</font>
    - <font style="color:rgb(102, 102, 102);">向量数据库：LanceDB（默认）、Pinecone、Chroma、Weaviate 和 QDrant。</font>
+ <font style="color:rgb(51, 51, 51);"> 技术概览 </font>
    - <font style="color:rgb(102, 102, 102);">整个项目设计为单线程结构，主要由三部分组成:收集器、前端和</font><font style="color:rgb(0, 82, 217);">服务器</font><font style="color:rgb(102, 102, 102);">。</font>
    - <font style="color:rgb(102, 102, 102);">collector：Python 工具，可快速将在线资源或本地文档转换为 LLM 可用格式。</font>
    - <font style="color:rgb(102, 102, 102);">frontend：ViteJS + React 前端，用于创建和管理 LLM 可使用的所有内容。</font>
    - <font style="color:rgb(102, 102, 102);">server：NodeJS + Express 服务器，处理所有向量</font><font style="color:rgb(0, 82, 217);">数据库管理</font><font style="color:rgb(102, 102, 102);">和 LLM 交互。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747031611352-b0758ac9-d138-4b49-9103-1ae4b75ca422.png)





# <font style="color:rgb(51, 51, 51);">Coze</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(63, 63, 63);">Coze是字节跳动推出的低门槛智能体开发平台，以自然对话体验为特色，支持语音识别/生成、丰富的插件生态，并可通过Web SDK嵌入网页。其核心用户群体是C端用户和轻量级应用开发者。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(63, 63, 63);">优势：</font>**

+ <font style="color:rgb(63, 63, 63);">极致用户体验：界面简洁，对话流畅，语音交互精准，适合非技术用户快速上手。</font>
+ <font style="color:rgb(63, 63, 63);">插件与生态优势：内置多领域插件（如电商、客服），依托字节技术资源，国内生态支持强大。</font>
+ <font style="color:rgb(63, 63, 63);">免费GPT-4接入：国际版支持免费使用GPT-4模型，功能成熟度高。</font>

**<font style="color:rgb(63, 63, 63);">劣势：</font>**

+ <font style="color:rgb(63, 63, 63);">定制化不足：主要面向标准化Bot开发，复杂任务扩展性弱于Dify和FastGPT，且仅支持云端部署。</font>

:::color5
**<font style="color:#601BDE;">2.适用场景</font>**

:::

<font style="color:rgb(63, 63, 63);">智能客服、语音助手、社交媒体聊天机器人等注重交互体验的C端应用。</font>







