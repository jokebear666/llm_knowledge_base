# ⓪ Agent 开发难点分析

<!-- source: yuque://zhongxian-iiot9/hlyypb/vby6hshb9ys70dlg -->

## 背景与核心概念
:::color3
**简介：**  
本文探讨了 Agent 开发的实质，指出调用 API 仅是冰山一角，真正的挑战在于如何构建稳定、可靠且高效的工程系统。Agent 的本质是在大模型的问答模式之上构建循环机制，使其从被动应答者转变为主动执行者。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770974055241-11464732-025d-46d0-966f-ac3761e1fddf.png)

:::color5
**<font style="color:#601bde;">1. Agent 开发的误区与真相</font>**

:::

虽然从技术层面看，Agent 开发确实包含“调用接口”这一环节，但这仅占整体工作的极小部分。如同烹饪不仅是“把食材放入锅中”，Agent 开发的质量差异在于工程实现的深度，这解释了为何同样的底层技术会产生截然不同的应用效果。

:::color5
**<font style="color:#601bde;">2. Agent 的核心定义</font>**

:::

Agent 的本质是对大模型交互模式的重构：

+ 传统模式：用户提问，模型单次应答。
+ Agent 模式：引入循环机制（Loop）。模型不再止步于回答，而是自主判断后续行动，通过调用外部工具（Tool Call）获取结果，并将结果反馈给自己以进行下一步决策，直至任务闭环。
+ 技术骨架：概念上可简化为 `while` 循环加上 `tool call` 能力。

:::color5
**<font style="color:#601bde;">3. 工程挑战的本质</font>**

:::

尽管 Agent 的技术骨架简单，但将其转化为在真实世界中稳定运行的系统，面临着巨大的工程挑战。本文将通过构建一个日程管理 Agent 的全过程，解析各阶段的实际难点。

## 第一阶段：原型构建与 API 调通
:::color3
**简介：**  
在开发初期，利用现有的 SDK 和 AI 编程工具，开发者可以迅速搭建出 Agent 的雏形。这一阶段通常给人以“开发简单”的错觉。

:::

:::color5
**<font style="color:#601bde;">1. 快速搭建脚手架</font>**

:::

通过安装 SDK 并编写少量代码，即可实现将用户输入传递给大模型并获取反馈。借助 Claude Code、Cursor 等 AI 编程工具，甚至可以通过自然语言描述直接生成项目骨架。

:::color5
**<font style="color:#601bde;">2. 定义工具（Tools）</font>**

:::

完成基础的 JSON Schema 定义，使模型能够调用如“查日历”、“读邮件”、“创建会议”等功能。

:::color5
**<font style="color:#601bde;">3. 初步验证的假象</font>**

:::

在简单的测试场景下（如“查询明天的会议”），模型能够成功调用工具并返回结果。这种顺畅的体验容易让开发者误判 Agent 开发的整体难度和上线周期。

## 第二阶段：真实环境接入与工具设计
:::color3
**简介：**  
当从 Mock 数据转向真实服务对接时，复杂度呈指数级上升。认证机制、API 边界情况、速率限制以及工具粒度的设计，构成了生产级应用的第一道门槛。

:::

:::color5
**<font style="color:#601bde;">1. 认证与权限管理（OAuth）</font>**

:::

对接真实服务（如 Microsoft Graph API）需要处理复杂的 OAuth 流程，包括应用注册、重定向处理、Token 的安全存储与自动刷新，以及权限模型（Delegated vs Application permissions）的研究。

:::color5
**<font style="color:#601bde;">2. API 边界情况处理</font>**

:::

真实 API 的返回数据往往具有复杂性，例如分页机制。若 Agent 仅获取首页数据（如默认 10 条），在面对“查询上周某项目邮件”等请求时，可能会因数据获取不全而给出错误的否定结论。

:::color5
**<font style="color:#601bde;">3. 速率限制（Rate Limiting）</font>**

:::

复杂的 API 限流策略（按应用、用户、资源类型）极易在复杂任务中触发 429 错误。模型无法理解 HTTP 状态码的含义，可能将此类系统错误误判为工具调用失败，进而导致错误推理。

:::color5
**<font style="color:#601bde;">4. 工具设计（Tool Design）的平衡难题</font>**

:::

工具的设计直接影响模型的表现：

+ 粒度过细：参数过多会导致 Schema 复杂化，显著降低模型的调用准确率（如 Llama 3.1 8B 在工具数量增加时表现大幅下降）。
+ 粒度过粗：万能型工具（如通用 Search）会让模型难以确定输入参数，导致参数错填或功能误用。
+ 描述文本的重要性：工具的 Description 相当于“给模型看的说明书”，其质量直接决定调用准确率，需要反复测试验证。

:::color5
**<font style="color:#601bde;">5. 工程占比现状</font>**

:::

参考阿里云工程博客数据 [1]，在生产级 Agent 系统中，AI 仅完成 30% 的工作，剩余 70% 均为工具工程与适配工作。

## 第三阶段：多步骤任务与错误传播
:::color3
**简介：**  
在处理依赖连续步骤的复杂任务时，单一环节的低容错率会导致整体任务成功率急剧下降，且早期微小的错误会在后续步骤中被不断放大。

:::

:::color5
**<font style="color:#601bde;">1. 累积误差导致的低成功率</font>**

:::

根据 Berkeley Function-Calling 排行榜 [2]，即使是顶尖模型，工具调用准确率也仅约 77.5%。在五步操作的任务中，全链路成功的概率仅为 0.775^5 ≈ 28%，意味着大部分复杂任务极大概率会失败。

:::color5
**<font style="color:#601bde;">2. 错误的“滚雪球”效应</font>**

:::

Galileo 研究 [3] 指出，早期的微小错误（如时间格式解析偏差）会被后续步骤继承并放大，最终导致严重的后果（如在错误时间发送错误的会议通知）。

:::color5
**<font style="color:#601bde;">3. 缺乏防御机制</font>**

:::

LLM API 文档并未提供针对此类问题的解决方案，开发者必须自行构建步骤间的校验逻辑、回滚机制和确认环节。

## 第四阶段：成本控制与模型路由
:::color3
**简介：**  
面向真实用户开放后，高昂的 Token 成本迫使开发者引入模型路由机制，但这又带来了适配不同模型能力的新的工程挑战。

:::

:::color5
**<font style="color:#601bde;">1. 成本激增问题</font>**

:::

真实场景下的高频请求和长 Context 会导致成本失控。简单查询使用昂贵的 SOTA 模型（如 Claude Sonnet/GPT-4）在经济上不可行。

:::color5
**<font style="color:#601bde;">2. 模型路由（Model Routing）的复杂性</font>**

:::

为了优化成本，需要根据任务复杂度动态选择模型（简单任务用小模型，复杂任务用大模型）。然而，构建准确的复杂度判断机制（规则引擎或分类模型）本身具有很高难度。

:::color5
**<font style="color:#601bde;">3. 多模型适配成本</font>**

:::

不同模型的工具调用能力和指令遵循能力差异巨大。Prompt 和 Tool Schema 往往不通用，更换模型意味着需要重新进行大量的适配和调试工作，人力成本可能抵消节省的 Token 成本。

## 第五阶段：上下文管理与记忆丢失
:::color3
**简介：**  
随着对话轮数的增加，有限的上下文窗口会导致 Agent 出现“失忆”现象，需要通过上下文工程来动态管理信息流。

:::

:::color5
**<font style="color:#601bde;">1. 代理失忆（Agentic Amnesia）</font>**

:::

研究表明，当任务分片到多轮对话时，模型性能平均下降 39%。Spotify 团队 [4] 发现，上下文窗口填满后，Agent 会遗忘原始任务目标。

:::color5
**<font style="color:#601bde;">2. 上下文工程（Context Engineering）</font>**

:::

需要实施类似“内存管理”的策略（Anthropic 定义 [5]），动态决定保留、压缩或丢弃哪些信息。Manus 团队 [6] 为此曾四次重构框架。

:::color5
**<font style="color:#601bde;">3. 上下文长度与幻觉的矛盾</font>**

:::

上下文长度与幻觉率呈正相关。输入信息越多，模型产生幻觉的概率越高，这构成了长任务处理中的结构性矛盾。

## 第六阶段：测试与评估困境
:::color3
**简介：**  
Agent 的非确定性特征使得传统软件测试方法失效，缺乏有效的评估体系成为上线的主要障碍。

:::

:::color5
**<font style="color:#601bde;">1. 传统测试方法的失效</font>**

:::

Agent 面临开放的输入空间和不确定的输出结果，LangChain 指出“每一个输入都是边界情况” [7]，导致单元测试和端到端测试难以覆盖。

:::color5
**<font style="color:#601bde;">2. 评估工具的局限性</font>**

:::

使用 LLM 评估 LLM（LLM-as-a-Judge）存在系统性偏差，裁判模型往往拥有与被测模型相同的盲点 [8]。

:::color5
**<font style="color:#601bde;">3. 实验室与生产环境的鸿沟</font>**

:::

Anthropic [9] 和 LangChain [10] 的数据表明，Agent 在动态交互中的行为难以被系统性评估。实验室基准测试与生产环境性能存在显著差距 [11]，导致产品表现“时灵时不灵”。

## 第七阶段：多 Agent 协作与系统扩展
:::color3
**简介：**  
试图通过增加 Agent 数量来处理复杂任务，往往会导致系统复杂度爆炸，协调与分工的难度远超代码实现本身。

:::

:::color5
**<font style="color:#601bde;">1. 复杂度爆炸</font>**

:::

微软 Azure SRE 团队 [12] 的经验显示，庞大的多 Agent 系统（100+ 工具）会导致调度混乱、死循环和错误扩散。精简核心工具和 Agent 数量反而能提高可靠性。

:::color5
**<font style="color:#601bde;">2. 协作失败率高</font>**

:::

UC Berkeley 的 MAST 框架研究 [13] 发现，多 Agent 系统在生产中的失败率极高（41-86.7%）。

:::color5
**<font style="color:#601bde;">3. 核心难点：规格与协调</font>**

:::

79% 的问题源于规格定义和协调层面，而非技术实现。Agent 之间的分工与沟通机制设计难度极大。

## 第八阶段：底层模型能力瓶颈
:::color3
**简介：**  
所有工程优化的天花板最终取决于底层模型的能力。指令遵循和推理能力的局限是目前无法通过工程手段完全逾越的障碍。

:::

:::color5
**<font style="color:#601bde;">1. 指令遵循能力的差异</font>**

:::

InfoQ 访谈 [14] 指出，模型能力瓶颈比工程挑战更为艰巨。Claude Sonnet 等模型因指令遵循能力较强成为首选，而其他模型在复杂任务上表现不佳，导致上层工程优化失效。

:::color5
**<font style="color:#601bde;">2. 推理模型的幻觉问题</font>**

:::

研究发现 [15]，o3、DeepSeek R1 等推理模型在复杂场景下反而比基础模型更容易产生幻觉，这限制了其在需要高可靠性场景中的应用。

## 第九阶段：框架选型与工程实质
:::color3
**简介：**  
框架之争并非核心，真正的难点在于上述的工程细节。框架更多适用于原型开发，而在生产环境中可能成为负担。

:::

:::color5
**<font style="color:#601bde;">1. 框架的局限性</font>**

:::

Hacker News [16] 和 Anthropic 官方指南 [17] 均建议谨慎使用 LangChain、CrewAI 等框架，因为它们可能增加调试难度并降低底层透明度。

:::color5
**<font style="color:#601bde;">2. 真正的需求：状态管理</font>**

:::

生产环境真正需要的是持久化执行和状态管理（如 Temporal 提供的能力），以支持长任务的暂停、恢复和断点续传。

:::color5
**<font style="color:#601bde;">3. 工程核心</font>**

:::

框架只是工具，Agent 开发的核心在于前述八个阶段的工程难题解决，而非框架选型。

## 总结
:::color3
**简介：**  
Agent 开发是一门新兴的系统工程学科，被称为 "Agent Engineering"。

:::

:::color5
**<font style="color:#601bde;">1. 95% 的工程冰山</font>**

:::

“调接口”仅占 Agent 开发工作量的 5%，其余 95% 涉及工具设计、错误处理、上下文管理、成本控制、评估体系搭建等复杂的系统工程。

:::color5
**<font style="color:#601bde;">2. 行业现状</font>**

:::

波士顿咨询 [18] 和 LangChain [10] 的调查数据显示，绝大多数企业 Agent 项目因质量不达标或 ROI 低而未能成功上线。

:::color5
**<font style="color:#601bde;">3. 成功的关键</font>**

:::

Agent 产品之间的差距不在于底层模型的接口调用，而在于接口之外那 95% 的工程实现是否扎实。从 Demo 到可靠产品的跨越，需要解决可靠性、可观测性和错误恢复等一系列深层问题。





##   
参考文献
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_1_0)阿里云：AI Agent的工程化被低估了 [https://www.cnblogs.com/alisystemsoftware/p/18926545](https://www.cnblogs.com/alisystemsoftware/p/18926545)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_2_0)Berkeley Function-Calling Leaderboard [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_3_0)Galileo：7种AI Agent故障模式及修复方法 [https://galileo.ai/blog/agent-failure-modes-guide](https://galileo.ai/blog/agent-failure-modes-guide)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_4_0)Spotify工程博客：代码Agent的上下文工程 [https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_5_0)Anthropic：Agent的有效上下文工程 [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_6_0)Manus：构建Agent的上下文工程经验 [https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
+ ^[<sup>a</sup>](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_7_0)[<sup>b</sup>](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_7_1)LangChain：Agent Engineering新学科 [https://blog.langchain.com/agent-engineering-a-new-discipline/](https://blog.langchain.com/agent-engineering-a-new-discipline/)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_8_0)Hacker News：AI Agent基准测试讨论 [https://news.ycombinator.com/item?id=44531697](https://news.ycombinator.com/item?id=44531697)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_9_0)Anthropic：揭秘AI Agent评估方法 [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
+ ^[<sup>a</sup>](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_10_0)[<sup>b</sup>](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_10_1)LangChain：Agent工程现状调查报告 [https://www.langchain.com/state-of-agent-engineering](https://www.langchain.com/state-of-agent-engineering)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_11_0)Agent基准测试的可靠性差距分析 [https://simmering.dev/blog/agent-benchmarks/](https://simmering.dev/blog/agent-benchmarks/)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_12_0)微软：构建Azure SRE Agent的上下文工程经验 [https://techcommunity.microsoft.com/blog/appsonazureblog/context-engineering-lessons-from-building-azure-sre-agent/4481200/](https://techcommunity.microsoft.com/blog/appsonazureblog/context-engineering-lessons-from-building-azure-sre-agent/4481200/)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_13_0)Why Do Multi-Agent LLM Systems Fail? [https://arxiv.org/abs/2503.13657](https://arxiv.org/abs/2503.13657)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_14_0)InfoQ：聊聊Agent在2025年的爆发与挑战 [https://www.infoq.cn/article/d6oe4ghorgrfotcuxxhf](https://www.infoq.cn/article/d6oe4ghorgrfotcuxxhf)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_15_0)推理模型幻觉率研究报告 [https://www.pryon.com/resource/reasoning-models-hallucinate-more----marking-trouble-for-ai-agent-adoption](https://www.pryon.com/resource/reasoning-models-hallucinate-more----marking-trouble-for-ai-agent-adoption)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_16_0)Hacker News：受够了AI Agent框架 [https://news.ycombinator.com/item?id=42691946](https://news.ycombinator.com/item?id=42691946)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_17_0)Anthropic：构建有效Agent指南 [https://www.anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)
+ [^](https://www.yuque.com/zhongxian-iiot9/gi3w2u/eyeypwq31smhcga8/edit?toc_node_uuid=KtJHvqFToCkcNDiM#ref_18_0)Agentic AI 2025年现状报告 [https://www.arionresearch.com/blog/the-state-of-agentic-ai-in-2025-a-year-end-reality-check](https://www.arionresearch.com/blog/the-state-of-agentic-ai-in-2025-a-year-end-reality-check)

