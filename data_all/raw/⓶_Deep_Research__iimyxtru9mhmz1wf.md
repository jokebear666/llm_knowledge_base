# ⓶ Deep Research

<!-- source: yuque://zhongxian-iiot9/hlyypb/iimyxtru9mhmz1wf -->

## <font style="color:rgb(25, 27, 31);">前言</font>
:::success
**背景：**OpenAI 并不是简单地在 GPT 基础上套壳。相反，OpenAI 基于 GPT-3，采用**<font style="color:#74B602;">端到端强化学习 + 高质量训练数据的方式训练了一个全新的模型，能够完全在内部完成搜索任务</font>**。

这给出了一个总体思路，但要真正复现 Deep Research，我们需要更多细节。本系列将尝试从 end-to-end 训练的角度，循序渐进地探讨这个问题。

:::

:::color3
**简介：**Deep Research 是一个深度搜索和调研的 Agent，能在 **5-30 分钟内** 出一份**<font style="color:#ED740C;">完整的调研报告</font>**。注意，它强调<font style="color:#ED740C;"> </font>**<font style="color:#ED740C;">"深度搜索 + 调研"</font>**，而非单纯的深度搜索（Deep Search）。**<font style="color:#D22D8D;">（by草莓师姐）</font>**

**参考：**[**https://mp.weixin.qq.com/s/apnorBj4TZs3-Mo23xUReQ**](https://mp.weixin.qq.com/s/apnorBj4TZs3-Mo23xUReQ)

[**https://mp.weixin.qq.com/s/-pPhHDi2nz8hp5R3Lm_mww**](https://mp.weixin.qq.com/s/-pPhHDi2nz8hp5R3Lm_mww)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750497704486-5cf3a097-4e2e-4e34-8bb1-351ce030ad8e.png)

:::color5
**<font style="color:#601BDE;">1.Deep Research价值</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

正如 **与真格戴雨森聊 Agent：各行业都会遭遇 "李世石时刻"，Attention is not all you need** 所言：

> 要是让实习生做，首先我不可能半夜两点要求他五分钟内给我一份报告，而且他做出来的报告基本没有 Deep Research 好。  
昨天我就在想，要是从大街上随便找十个人，至少九个已经比不上 Deep Research 了。因为 Deep Research 能在几分钟内，针对任何你需要的话题，给出一份在我看来达到在较好公司工作一两年的白领水平的研究报告。所以我觉得 AGI 已不再是一个科幻概念。现在在收集信息、整理信息这类任务上，AI 已经超过了大多数人。
>

:::color5
**<font style="color:#601BDE;">2.现有复现版本</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

目前市面上已有多个 Deep Research 的复现版本，包括：

+ **大公司产品**：Google 的 Deep Research、Grok 的 DeepSearch 和 DeeperSearch、Perplexity 的 DeepResearch、智谱的 AutoGLM 沉思版、Genspark、秘塔的深度研究模式。
+ **开源项目**：open_deep_research、node-DeepResearch、deep-research、open-deep-research、Agentic-Reasoning。

根据实测，大公司的产品在交互和研究质量上普遍更胜一筹（如下图来自某位知乎网友实际体验后的分享）：

+ OpenAI 的 Deep Research 虽然耗时最长，但质量最高；
+ 其次是 Grok 的 DeeperSearch；
+ 国内产品如豆包的深度思考和秘塔，效率较高但质量稍逊。

希望本系列能为大家带来清晰的复现思路！

:::color5
**<font style="color:#601BDE;">3.复现思路</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(25, 27, 31);">本系列将先聚焦</font>**<font style="color:rgb(25, 27, 31);">Deep Search</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">end-to-end</font>**<font style="color:rgb(25, 27, 31);">训练，循序渐进地展开:</font>

1. <font style="color:rgb(25, 27, 31);">本文先聚焦在 Deep Search。要复现Deep Research，首先要把搜索(Search)做好。给定用户问题，Agent要学会从浏览器或API中搜集相关知识。没有扎实的Search能力，就难以实现Research。</font>
2. <font style="color:rgb(25, 27, 31);">end-to-end的模型被公认为上限更高的完成方式，因此我们将重点研究 end-to-end复现Deep Search的关键技术洞见。</font>

<font style="color:rgb(25, 27, 31);">本系列文章将分三部分展开：</font>

1. **<font style="color:rgb(25, 27, 31);">上篇(本文)</font>**<font style="color:rgb(25, 27, 31);">: 聚焦Deep Search的关键技术和端到端训练方法</font>
2. **<font style="color:rgb(25, 27, 31);">中篇</font>**<font style="color:rgb(25, 27, 31);">: 探讨Jina AI、WebThinker 等中间形态的Deep Research实现</font>
3. **<font style="color:rgb(25, 27, 31);">下篇</font>**<font style="color:rgb(25, 27, 31);">: 分析OpenAI、Gemini、Genspark等产品级Deep Research的技术路径</font>

<font style="color:rgb(25, 27, 31);">希望通过这个系列,能与大家一同探索如何从0到1复现这项令人兴奋的前沿技术。欢迎交流讨论!</font>

## <font style="color:rgb(25, 27, 31);">Deep Search：搜索的本质与难点</font>
:::color3
**简介：**在深入研究 **Deep Research** 之前，我们必须明确：**Deep Search（深度搜索）是 Deep Research 的基石**。

:::

:::color5
**<font style="color:#601BDE;">1.搜索的本质</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

搜索的核心目标是 **找到全面且直接的信息**。根据需求和场景，可以采用不同的实现方式：

1. **结构化数据查询**：编写 SQL 语句查询公司内部数据库
2. **API 调用**：使用关键词调用外部搜索 API（如 Google、Bing）
3. **虚拟浏览器**：通过 Operator 等工具模拟人类浏览网页
4. **其他方式**：...

:::color5
**<font style="color:#601BDE;">2.搜索任务的复杂度递增</font>****<font style="color:#D22D8D;"></font>**

:::

搜索任务可以按复杂度分为不同等级：

+ **单跳搜索**（简单查询）：  
_示例_："哪吒 2 的导演是谁？"
+ **多跳搜索**（多步推理）：  
_示例_："哪吒 2 的导演还导演过什么电影？"
+ **深度研究型搜索**（复杂分析）：  
_示例_："研究《哪吒 2》在国际市场的接受度与文化输出效果，分析其对提升中国文化软实力的贡献。"

:::color5
**<font style="color:#601BDE;">3.思维链搜索：多跳与深度研究的关键</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

**多跳搜索**和**深度研究型搜索**的核心在于 **模仿人类的思维链搜索**，其流程如下：

1. **初步推理**：模型根据问题确定基础搜索方向
2. **初始搜索**：执行第一轮搜索，获取第一批信息
3. **迭代推理**：基于已获取的信息，推理下一步搜索方向
4. **细化搜索**：执行更精准的搜索，获取更深层数据
5. **循环迭代**：重复 "推理 → 搜索 → 推理" 过程，直至信息充足

在这个过程中，**每一次搜索都建立在前一次结果的基础上**，形成连贯的推理链。

:::color5
**<font style="color:#601BDE;">4.为什么 Deep Search 是 Deep Research 的基石？</font>**

:::

只有掌握了 **迭代式、思维链式的搜索能力**，才能支撑起完整的深度研究（Deep Research）。**Deep Search 的精准度和推理能力，直接决定了 Deep Research 的质量**。

**下一步**：我们将探讨如何优化搜索策略，以提升 Deep Research 的效率和深度。

## <font style="color:rgb(25, 27, 31);">论文 1: 《</font>[<font style="color:rgb(9, 64, 142);">Search-o1</font>](https://zhida.zhihu.com/search?content_id=256073107&content_type=Article&match_order=1&q=Search-o1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">: Agentic Search-Enhanced Large Reasoning Models》</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介：</font>**<font style="color:rgb(25, 27, 31);">Search-o1 是最近比较火的 WebThinker 项目的前身，它提出了一种新颖的方法，</font>**<font style="color:#ED740C;">让大型语言模型在推理过程中能够主动进行网络搜索</font>**<font style="color:rgb(25, 27, 31);">，从而增强其推理能力。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://arxiv.org/pdf/2501.05366](https://arxiv.org/pdf/2501.05366)

**<font style="color:rgb(25, 27, 31);">项目地址：</font>**[https://search-o1.github.io/](https://search-o1.github.io/)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750498471714-be5709ef-e366-4d48-844a-b034d4367270.png)

:::color4
<font style="color:rgb(25, 27, 31);">与传统检索增强生成（RAG）系统相比，Search-o1 有两个关键创新点。</font>

:::

### <font style="color:rgb(25, 27, 31);">核心组件一: 主动式检索增强生成机制</font>
:::color3
<font style="color:rgb(25, 27, 31);">传统 RAG 通常是一次性的：在回答问题前进行一次检索，将检索结果放入上下文中。而 Search-o1 实现了</font>**<font style="color:rgb(25, 27, 31);">动态的、多步骤的</font>**<font style="color:rgb(25, 27, 31);">检索机制。</font>

:::

:::color5
**<font style="color:#601BDE;">1.动态的、多步骤的检索机制</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ <font style="color:rgb(25, 27, 31);">模型在推理过程中可以</font>**<font style="color:rgb(25, 27, 31);">识别自身知识的不足点</font>**
+ <font style="color:rgb(25, 27, 31);">当遇到知识不确定的情况时，模型会自动生成搜索查询，格式为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><|begin_search_query|>搜索词<|end_search_query|></font>`
+ <font style="color:rgb(25, 27, 31);">系统检测到这一标记后，暂停模型推理，执行网络搜索</font>
+ <font style="color:rgb(25, 27, 31);">搜索结果被包装在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><|begin_search_result|>检索到的内容<|end_search_result|></font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">标记中返回给模型</font>
+ <font style="color:rgb(25, 27, 31);">模型继续推理，并可以根据需要多次重复这一过程。</font>

:::color5
**<font style="color:#601BDE;">2.Prompt 如下</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750498607580-9c39a921-5f1c-4817-a438-8d0f2a6c631f.png)

### <font style="color:rgb(25, 27, 31);">Search-o1的核心组件二</font>
:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">Reason-in-Documents</font>](https://zhida.zhihu.com/search?content_id=256073107&content_type=Article&match_order=1&q=Reason-in-Documents&zhida_source=entity)<font style="color:rgb(25, 27, 31);">模检索有一个很严重的问题，就是检索出来的内容可能很杂乱和很长，而现在的大模型处理长文本性能会下降，因此，论文剔除，用另外一个 Reason-in-Documents，把检索到的内容进行精炼，再放入到原有推理链中，从而缓解检索文档中存在冗余信息和LLM 处理长文档的局限性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Prompt 如下</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750498652951-98cbfaa1-f2e0-4445-b176-7f3bca0ba124.png)

### <font style="color:rgb(25, 27, 31);">Search-o1与传统 RAG 的区别</font>
+ **<font style="color:rgb(25, 27, 31);">检索触发机制</font>**<font style="color:rgb(25, 27, 31);">：传统 RAG 是静态的、预先定义的；Search-o1 是动态的、由模型主动触发的</font>
+ **<font style="color:rgb(25, 27, 31);">检索频率</font>**<font style="color:rgb(25, 27, 31);">：传统 RAG 通常进行一次性检索；Search-o1 支持多次、迭代式检索</font>
+ **<font style="color:rgb(25, 27, 31);">内容整合</font>**<font style="color:rgb(25, 27, 31);">：传统 RAG 直接插入大量文档；Search-o1 经过精炼后仅保留关键信息</font>
+ **<font style="color:rgb(25, 27, 31);">推理连贯性</font>**<font style="color:rgb(25, 27, 31);">：Search-o1 保持了推理流的连贯性，避免了传统 RAG 可能导致的推理中断</font>

### <font style="color:rgb(25, 27, 31);">示例说明</font>
<font style="color:rgb(25, 27, 31);">以下图论文中的示例为例，详细说明整个工作流程：</font>

1. <font style="color:rgb(25, 27, 31);">模型开始推理，遇到需要特定知识的环节</font>
2. <font style="color:rgb(25, 27, 31);">模型生成：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><|begin_search_query|> reaction of grignard reagent with aldehyde <|end_search_query|></font>`
3. <font style="color:rgb(25, 27, 31);">系统暂停模型推理，调用搜索引擎获取结果</font>
4. <font style="color:rgb(25, 27, 31);">Reason-in-Documents 模块分析搜索结果，提取关键信息</font>
5. <font style="color:rgb(25, 27, 31);">精炼后的内容被包装在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><|begin_search_result|>提炼后的检索内容<|end_search_result|></font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">中</font>
6. <font style="color:rgb(25, 27, 31);">模型继续推理，可能进行多轮搜索-精炼循环</font>
7. <font style="color:rgb(25, 27, 31);">最终生成完整且准确的答案 !</font>

## <font style="color:rgb(25, 27, 31);">论文 2: 《DeepRetrieval: Hacking Real Search Engines and Retrievers with Large Language Models via Reinforcement Learning》</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">DeepRetrieval的突出之处在于它能够通过</font>**<font style="color:#ED740C;">"试错"方式直接学习，使用检索指标作为奖励，无需昂贵的监督数据</font>**<font style="color:rgb(25, 27, 31);">。这种方法使模型能够针对实际性能指标进行优化，而不仅仅是模仿人工编写的查询。</font>

**paper**：[https://arxiv.org/pdf/2503.00223](https://arxiv.org/pdf/2503.00223)

**项目地址**：[https://github.com/pat-jj/DeepRetrieval](https://github.com/pat-jj/DeepRetrieval)**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750498969955-760adcdd-9d1a-42eb-8253-3b8ac2ba5bdd.png)

:::color5
**<font style="color:#601BDE;">1.用强化学习来训练query改写</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(25, 27, 31);">query改写已被证实是检索流程中的关键步骤。当用户提交问题时，大型语言模型(LLM)通常会对其进行重新表述(称为增强查询)，然后再执行检索。</font><font style="color:#74B602;">DeepRetrieval采用创新方法，利用强化学习(RL)而非传统的监督式微调(SFT)来优化这一关键步骤。</font>

### <font style="color:rgb(25, 27, 31);">在多种检索任务中进行了实验</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介：</font>**<font style="color:rgb(25, 27, 31);">论文中值得称赞的是，在五种不同的检索任务中展示的有效性，每种任务都需要不同的查询格式和奖励结构。论文通过研究五种不同类型的检索任务，展示了强化学习在查询改写领域的通用有效性。这些任务包括专业文献检索、基于BM25的关键词匹配以及SQL生成等多种形式。</font>

:::

:::color4
**<font style="color:rgb(25, 27, 31);">作者的核心论点是：</font>**<font style="color:rgb(25, 27, 31);">无论用户的初始query和最终改写的 query的形式如何变化（自然语言到自然语言、专用语法到专用语法、或自然语言到SQL），经过精心设计的强化学习训练都能显著提升查询改写的质量，从而大幅提高最终的检索效果。这一发现证明了强化学习方法在查询优化领域具有跨形式、跨领域适用性和有效性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Literature Searching (文献检索)</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">定义</font>**<font style="color:rgb(25, 27, 31);">：给定一个查询，从搜索引擎中检索相关文档。</font>
+ **<font style="color:rgb(25, 27, 31);">评估指标</font>**<font style="color:rgb(25, 27, 31);">：Recall@K（在前K个结果中检索到的目标文档的百分比）</font>
+ <font style="color:rgb(25, 27, 31);">query形态：采用医学专用的PICO检索语法</font>
    - <font style="color:rgb(25, 27, 31);">例如："((达姆明) AND (围手术期 OR 血液转输 OR 去氨加压素 OR 抗凝剂)) AND (随机对照试验)"</font>
    - <font style="color:rgb(25, 27, 31);">这种查询包含布尔运算符和专业术语，结构严谨</font>

:::color5
**<font style="color:#601BDE;">2.Evidence-Seeking Retrieval (证据寻找检索)</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">定义</font>**<font style="color:rgb(25, 27, 31);">：给定一个问题，检索包含匹配答案候选项的文档。</font>
+ **<font style="color:rgb(25, 27, 31);">评估指标</font>**<font style="color:rgb(25, 27, 31);">：H@N（第一个出现答案的文档排名是否在前N位）</font>
+ **<font style="color:rgb(25, 27, 31);">query形态</font>**<font style="color:rgb(25, 27, 31);">：类似自然语言，如"What is another term for the pivot mounting?"</font>

:::color5
**<font style="color:#601BDE;">3.Classic Sparse Document Retrieval (经典稀疏文档检索)</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ <font style="color:rgb(25, 27, 31);">定义: 使用关键词匹配和布尔操作进行文档检索（如BM25算法）。</font>
+ **<font style="color:rgb(25, 27, 31);">评估指标</font>**<font style="color:rgb(25, 27, 31);">：NDCG（归一化折扣累积增益，衡量排序质量）</font>
+ <font style="color:rgb(25, 27, 31);">query</font>**<font style="color:rgb(25, 27, 31);">形态</font>**<font style="color:rgb(25, 27, 31);">：关键词和布尔表达式组合- 例如："(李明 IS-A 人物 AND 李明 IS-A 在职) OR (李明 IS-A 人物 AND 李明 IS-A 失业)"</font>

:::color5
**<font style="color:#601BDE;">4.Classic Dense Document Retrieval (经典密集文档检索)</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">定义</font>**<font style="color:rgb(25, 27, 31);">：使用查询和文档的语义向量表示进行检索。</font>
+ **<font style="color:rgb(25, 27, 31);">评估指标</font>**<font style="color:rgb(25, 27, 31);">：同样使用NDCG</font>
+ <font style="color:rgb(25, 27, 31);">query</font>**<font style="color:rgb(25, 27, 31);">形态</font>**<font style="color:rgb(25, 27, 31);">：自然语言表述</font>
    - <font style="color:rgb(25, 27, 31);">例如："量子计算的基本原理是什么？"</font>
    - <font style="color:rgb(25, 27, 31);">系统会将这类查询转换为向量形式，通过语义相似度进行文章检索</font>

:::color5
**<font style="color:#601BDE;">5.SQL Database Search (SQL数据库检索)</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">定义</font>**<font style="color:rgb(25, 27, 31);">：根据自然语言查询生成SQL来检索数据库中的信息。</font>
+ **<font style="color:rgb(25, 27, 31);">评估指标</font>**<font style="color:rgb(25, 27, 31);">：执行准确率（检索结果与目标答案的匹配程度）</font>
+ **<font style="color:rgb(25, 27, 31);">quuey形态</font>**<font style="color:rgb(25, 27, 31);">：SQL语句</font>
    - <font style="color:rgb(25, 27, 31);">例如："SELECT 书名 FROM 图书表 WHERE 类型 != '诗歌'"</font>



### <font style="color:rgb(25, 27, 31);">奖励函数设计</font>
:::color3
在强化学习框架中，奖励函数的设计至关重要。论文针对5种不同的检索任务，分别设计了不同的prompt和奖励函数：

:::

:::color5
**<font style="color:#601BDE;">1.奖励函数公式</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750499707123-60baeb7b-5f09-41e9-89e6-24fbd97291c7.png)

其中：

+ **r_retrieval**：捕获任务特定的检索性能
+ **r_format**：奖励符合所需输出结构的结果
+ **q**：用户原始query
+ **q′**：模型改写后的query

:::color5
**<font style="color:#601BDE;">2.具体任务示例</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:#2F4BDA;">Literature Search（文献检索）</font>**
+ **Prompt示例**：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750499342775-91a0ba29-c1ee-4b57-b6c1-e252436e20b2.png)

+ **格式奖励(r_format)**：
    - 评估用户是否遵循prompt要求的格式
    - 示例评分标准：
        * 出现"think>"等指定token：+5.0分
        * 完全不符合格式要求：-3.5分
2. **<font style="color:#2F4BDA;">SQL Database Search（数据库检索）</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**
+ **Prompt示例**：  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750499363556-e52a37b6-8785-4462-8d5d-8912ec74eeec.png)
+ **格式奖励(r_format)**：
    - 检查是否包含"think> </think answer /answer"等指定token
    - 验证生成的SQL是否符合语法规范
+ **检索奖励(r_retrieval)**：
    - 与标准答案的SQL执行结果一致性评估
3. **<font style="color:#2F4BDA;">完整奖励设置</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750499390330-8803822d-7f4f-4814-809e-acbe959e2557.png)

注：所有评分标准均基于任务特性和期望输出格式精心设计，既考虑结果准确性，也注重输出规范性。

## <font style="color:rgb(25, 27, 31);">论文 3: 《Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning》</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Search-R1通过创新的五阶段交互流程实现知识检索与推理的深度融合</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

**paper**：[https://arxiv.org/pdf/2503.09516](https://arxiv.org/pdf/2503.09516)

**项目地址**：[https://github.com/PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750500049706-9fa184c6-84da-4a5d-a0ca-447fee99844a.png)

### <font style="color:rgb(25, 27, 31);">结合交错式多轮搜索引擎调用的文本生成</font>
:::color3
<font style="color:rgb(25, 27, 31);">Search-R1通过创新的五阶段交互流程实现知识检索与推理的深度融合</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">初始问题解析阶段</font>**<font style="color:rgb(25, 27, 31);">：当接收到用户问题时，模型首先在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><think></font>`<font style="color:rgb(25, 27, 31);">思考标签内进行初步推理分析，识别当前知识储备中的信息缺口。</font>
2. **<font style="color:rgb(25, 27, 31);">动态检索决策阶段</font>**<font style="color:rgb(25, 27, 31);">：若推理过程中发现知识不足，模型将自主触发检索机制，通过</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><search>查询内容</search></font>`<font style="color:rgb(25, 27, 31);">格式生成精准搜索指令。</font>
3. **<font style="color:rgb(25, 27, 31);">信息整合阶段</font>**<font style="color:rgb(25, 27, 31);">：搜索引擎返回的结果会被结构化封装在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><information></font>`<font style="color:rgb(25, 27, 31);">信息标签内，为后续推理提供可靠的外部知识输入。</font>
4. **<font style="color:rgb(25, 27, 31);">迭代优化机制</font>**<font style="color:rgb(25, 27, 31);">：系统支持多轮次检索-推理循环，模型可根据信息完备性动态决定是否发起新一轮检索，直至满足解答需求。</font>
5. **<font style="color:rgb(25, 27, 31);">最终响应生成阶段</font>**<font style="color:rgb(25, 27, 31);">：当判定信息充足时，模型直接通过</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><answer></font>`<font style="color:rgb(25, 27, 31);">答案标签输出简洁结论，无需附加解释说明。 以下为 Search-R1的 prompt</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750500184177-05799f2b-c87a-4cff-b8e9-42e9475c9a5f.png)

<font style="color:rgb(25, 27, 31);">与 Search-o1不同的是，Search-R1针对任务进行了强化学习的训练，Search-R1没有 Search-o1的 Reason-in-Documents模块，检索到的内容是直接完整放到思维链中的。以下是Search-o1的例子，本质就是生成检索、返回内容、思考，不断循环，直到达到最终答案。</font>



### <font style="color:rgb(25, 27, 31);">奖励函数设计</font>
:::color3
Search-R1 采用**基于规则的奖励机制**，仅关注**最终结果的正确性**

:::

:::color5
**<font style="color:#601BDE;">1.奖励函数定义</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750500249885-b63a5638-9f8e-46a8-afa2-982623007b31.png)

其中：

+ **EM**：精确匹配函数（Exact Match）
+ **aₚᵣₑ𝒹**：模型预测的答案（从回答中提取）
+ **a₉ₒₗ𝒹**：标准答案（Ground Truth）

:::color5
**<font style="color:#601BDE;">2.设计特点</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **简化奖励计算**
    - 仅依赖**最终答案的精确匹配**（EM），避免复杂的过程奖励设计。
2. **抗"黑客攻击"性**
    - 不使用神经奖励模型（Neural Reward Model），减少被对抗性攻击（Adversarial Hacking）的风险。
3. **无格式奖励**
    - 作者指出，模型已具备良好的**结构遵循能力**，因此无需额外引入格式奖励（Format Reward）。



## <font style="color:rgb(25, 27, 31);">论文 4: 《</font>[<font style="color:rgb(9, 64, 142);">R1-Searcher</font>](https://zhida.zhihu.com/search?content_id=256073107&content_type=Article&match_order=1&q=R1-Searcher&zhida_source=entity)<font style="color:rgb(25, 27, 31);">: Incentivizing the Search Capability in LLMs via Reinforcement Learning》</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">R1-Searcher引入了一个两阶段基于结果的强化学习方法，使LLM能够在推理过程中自主调用外部搜索系统</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

**paper**：[https://arxiv.org/pdf/2503.09516](https://arxiv.org/pdf/2503.09516)

**项目地址**：[https://github.com/PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750500552551-5f937ffa-e2ec-43a9-8a5c-4e8f723fe6c2.png)

:::color5
**<font style="color:#601BDE;">1.两阶段的强化学习增强检索能力</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:#2F4BDA;">第一阶段(检索学习训练)</font>**<font style="color:#2F4BDA;">：</font><font style="color:rgb(25, 27, 31);">通过检索奖励激励模型学习如何正确调用外部搜索，不关注答案准确性。</font>
+ **<font style="color:rgb(25, 27, 31);">检索奖励 (Retrieval Reward)</font>**<font style="color:rgb(25, 27, 31);">:</font>
+ <font style="color:rgb(25, 27, 31);">0.5分：当模型至少执行一次检索操作</font>
+ <font style="color:rgb(25, 27, 31);">0分：未进行任何检索</font>
+ **<font style="color:rgb(25, 27, 31);">格式奖励 (Format Reward)</font>**<font style="color:rgb(25, 27, 31);">:</font>
    - <font style="color:rgb(25, 27, 31);">0.5分：完全符合规定的输出格式标准</font>
    - <font style="color:rgb(25, 27, 31);">0分：格式不符合要求</font>
    - **<font style="color:rgb(25, 27, 31);">格式规范要求</font>**<font style="color:rgb(25, 27, 31);">：</font>
        * <font style="color:rgb(25, 27, 31);">思考过程必须封装在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><think>...</think></font>`<font style="color:rgb(25, 27, 31);">标签内</font>
        * <font style="color:rgb(25, 27, 31);">最终答案必须封装在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><answer>...</answer></font>`<font style="color:rgb(25, 27, 31);">标签内</font>
        * <font style="color:rgb(25, 27, 31);">检索查询必须使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><begin_of_query>...</end_of_query></font>`<font style="color:rgb(25, 27, 31);">标签标记</font>
        * <font style="color:rgb(25, 27, 31);">严格禁止未调用检索系统直接生成文档内容</font>
+ **<font style="color:rgb(25, 27, 31);">阶段总奖励</font>**<font style="color:rgb(25, 27, 31);">：Rretrieval + Rformat (最高1.0分)</font>
2. **<font style="color:#2F4BDA;">第二阶段(检索结果集成训练)</font>**<font style="color:#2F4BDA;">：</font><font style="color:rgb(25, 27, 31);">在确保格式规范的基础上，提升模型有效利用检索信息解决问题的能力</font>
+ <font style="color:rgb(25, 27, 31);">第二阶段删除了检索奖励，引入了答案奖励，同时保留格式奖励但调整了惩罚力度</font>
+ **<font style="color:rgb(25, 27, 31);">格式奖励 (Format Reward)</font>**<font style="color:rgb(25, 27, 31);">:</font>
    - <font style="color:rgb(25, 27, 31);">0分：格式完全正确</font>
    - <font style="color:rgb(25, 27, 31);">-2分：格式出现任何错误</font>
    - <font style="color:rgb(25, 27, 31);">(注：相比第一阶段，显著提高了格式错误的惩罚力度)</font>
+ **<font style="color:rgb(25, 27, 31);">答案奖励 (Answer Reward)</font>**<font style="color:rgb(25, 27, 31);">:</font>
    - <font style="color:rgb(25, 27, 31);">使用F1分数作为答案奖励：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Ranswer = 2 * IN / (PN + RN)</font>`
        * <font style="color:rgb(25, 27, 31);">其中：</font>
            + <font style="color:rgb(25, 27, 31);">PN: 预测答案的词数</font>
            + <font style="color:rgb(25, 27, 31);">RN: 参考答案的词数</font>
            + <font style="color:rgb(25, 27, 31);">IN: 预测答案与参考答案的交集词数</font>
+ **<font style="color:rgb(25, 27, 31);">阶段总奖励</font>**<font style="color:rgb(25, 27, 31);">：Format Reward + Answer Reward 这种两阶段设计通过分离关注点，先确保模型掌握正确的检索行为规范，再专注于提升答案质量，实现了检索能力与信息整合能力的阶梯式提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1750500594204-3d528025-d230-4939-bc23-887a5ec620f7.png)

## <font style="color:rgb(25, 27, 31);">总结</font>
:::color5
**<font style="color:#601BDE;">1.当前研究方向</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

Search-o1、Search-R1 和 R1-Searcher 的研究方向高度一致：  
**构建长推理思维链**，并在思维链中动态优化搜索策略。

**关键共识**：**强化学习（RL）** 比 **监督微调（SFT）** 具备更强的泛化能力。

:::color5
**<font style="color:#601BDE;">2.现有方法的局限性</font>**

:::

DeepRetrieval 虽然专注于 **查询改写（Query Rewriting）**，但存在明显不足：

+ 研究范围过窄，难以支撑完整的思维链推理。
+ **理想的查询改写** 应是思维链的自然产物，而非独立优化的任务。

:::color5
**<font style="color:#601BDE;">3.未来挑战</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

我们距离真正的 **Deep Research** 仍有较大差距，完整的研究流程还涉及：

1. **并行搜索**（Parallel Searching）
2. **超长上下文管理**（Long-context Handling）
3. **研究目录编写**（Research Outline Generation）
4. **结论动态调整**（Adaptive Conclusion Refinement）

:::color5
**<font style="color:#601BDE;">4.核心观点</font>**

:::

正如开篇所述：

**"先做好 Search，才能做好 Research。"**

当前的优化重点仍应聚焦于 **搜索能力** 的提升，为后续深度研究奠定基础。

