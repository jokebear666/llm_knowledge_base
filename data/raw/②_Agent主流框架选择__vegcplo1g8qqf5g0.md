# ② Agent主流框架选择

<!-- source: yuque://zhongxian-iiot9/hlyypb/vegcplo1g8qqf5g0 -->

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(0, 0, 0);">「</font>**<font style="color:#74B602;">Agent不稀奇，能“自己想、自己干、自己复盘”的才是好Agent</font>**<font style="color:rgb(0, 0, 0);">」可一到落地，名词、框架和坑一起涌来：设计模式、强自治、可控流程、多代理协作.... 到底该不该用 Agent？该选哪一类框架？需要用到什么程度？</font>

:::

:::color3
**简介：**<font style="color:rgb(0, 0, 0);">本文用直观的图表、清晰的示例，为你讲清</font>**<font style="color:#ED740C;">什么是Agent、什么场景适合使用Agent以及各类主流Agent框架</font>**<font style="color:rgb(0, 0, 0);">，希望能帮各位少走弯路，迅速判断技术路径。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

## <font style="color:rgb(0, 0, 0);">1.</font><font style="color:rgb(62, 71, 83);">Workflow和Agent的区别</font>
![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023258-1252a957-6ab6-44a0-8be5-135483400498.webp)

## <font style="color:rgb(0, 0, 0);">2.</font><font style="color:rgb(62, 71, 83);">Agent框架选择</font>
:::color5
**<font style="color:#601BDE;">核心依赖Github上Star数以及市场热度，综合选取5款Agent框架 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761040209676-c885c2be-01e3-4c0b-a04c-950d325fb349.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761040182958-bd2945d8-c138-4de0-bac4-78da4a0e8233.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761040240016-1823b0b2-59f3-4dc3-b680-2cc44d1d96f3.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761040282768-867fa372-164c-473f-8ea5-8d500ca5ba8a.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761040310283-d7185edb-3950-4126-8c66-ebab1f42be6a.png)

<font style="color:rgb(62, 71, 83);">1.</font>**<font style="color:rgb(62, 71, 83);">AutoGPT：</font>**<font style="color:rgb(62, 71, 83);">Github 17.8w Star</font>

<font style="color:rgb(62, 71, 83);">2.</font>**<font style="color:rgb(62, 71, 83);">LangGraph：</font>**<font style="color:rgb(62, 71, 83);"> Github 13.1w Star</font>

<font style="color:rgb(62, 71, 83);">3.</font>**<font style="color:rgb(62, 71, 83);">Dify：</font>**<font style="color:rgb(62, 71, 83);"> Github 11.2w Star</font>

<font style="color:rgb(62, 71, 83);">4.</font>**<font style="color:rgb(62, 71, 83);">CrewAI：</font>**<font style="color:rgb(62, 71, 83);">Github 3w Star</font>

<font style="color:rgb(62, 71, 83);">5.</font>**<font style="color:rgb(62, 71, 83);">AutoGen：</font>**<font style="color:rgb(62, 71, 83);">微软开源 Github 5w Star</font>

<font style="color:rgb(62, 71, 83);">  
</font>

## <font style="color:rgb(0, 0, 0);">3.</font><font style="color:rgb(62, 71, 83);">各Agent框架对比结论</font>
:::color3
**简介：五种agent框架对比**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023340-c8347f8b-bf7c-4a73-aede-f7c8309b5f37.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023250-12280bd5-e2b9-48de-bfeb-bb6c7ba85f1e.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023467-f8c80b05-d45f-4497-b9c5-bd888d660a64.webp)

<font style="color:rgb(0, 0, 0);">  
</font>

## <font style="color:rgb(0, 0, 0);">4.</font><font style="color:rgb(62, 71, 83);">为什么需要使用Agent框架</font>
:::color3
**简介：**<font style="color:rgb(62, 71, 83);">只要“问题不可完全穷举、要跨多系统查证、并且需要在对话中澄清/协商/决策”，就更应该用 Agent 框架，而不是纯 Workflow。为什么？用一个真实的ToC场景客服链路来说明。</font>

:::

:::color5
**<font style="color:#601BDE;">1.纯 Workflow 在智能客服里的“天花板”</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(62, 71, 83);">Workflow（无论是 Dify 的可视化编排，还是 LangGraph 的状态机）非常适合步骤确定 + 条件有限的流程，比如：</font>

1. <font style="color:rgb(62, 71, 83);">查询订单 → 格式化答复</font>
2. <font style="color:rgb(62, 71, 83);">退货→生成标签→发通知</font>
3. <font style="color:rgb(62, 71, 83);">FAQ 检索→返回片段</font>

<font style="color:rgb(62, 71, 83);">一旦进入长尾问题，Workflow 就会遇到“分支爆炸”：</font>

**<font style="color:rgb(62, 71, 83);">例：</font>**<font style="color:rgb(62, 71, 83);">同一条“包裹没到”诉求，可能要综合 ①承运商状态 ②发货 SLA ③节假日政策 ④地址异常 ⑤是否会员 ⑥是否已报缺货 ⑦是否已部分签收 ⑧是否叠加优惠券/补发 等。</font>

<font style="color:rgb(62, 71, 83);">如果你用固定分支描述：</font>

<font style="color:rgb(62, 71, 83);">假设有 5 个意图 × 6 种物流状态 × 3 种用户等级 × 3 个政策时段（平日/大促/假期） × 3 种地理区域，共5×6×3×3×3=810 条潜在路径。</font>

<font style="color:rgb(62, 71, 83);">这还没算异常（报损、拒收、欺诈信号）与“对话澄清”的分支。维护成本和上线速度都会被拖垮。此外，Workflow 对 </font>**<font style="color:rgb(62, 71, 83);">对话中的“澄清—再决策—再行动</font>**<font style="color:rgb(62, 71, 83);"> 并不天然友好，需要把每一步提问、回答、重试都画成节点，复杂而脆弱。</font>

:::color5
**<font style="color:#601BDE;">2.Agent 框架解决的核心问题</font>**

:::

<font style="color:rgb(62, 71, 83);">以 AutoGen/CrewAI 这类 Agent 框架为例，它们把“在对话里动态规划与调用工具”作为第一性能力：</font>

**<font style="color:rgb(62, 71, 83);">场景：</font>**<font style="color:rgb(62, 71, 83);">用户说“我 8 月 1 号下的单今天还没到，收件地址其实要换，而且我被重复扣费了。”</font>

<font style="color:rgb(62, 71, 83);">一个合格的客服 Agent 团队会做什么？</font>

<font style="color:rgb(62, 71, 83);">1.</font>**<font style="color:rgb(62, 71, 83);">意图识别 + 澄清</font>**

+ <font style="color:rgb(62, 71, 83);">Planner Agent：拆出多意图（物流异常、改址、计费异常），先问关键澄清（订单号/新地址/扣费凭证）。</font>

<font style="color:rgb(62, 71, 83);">2.</font>**<font style="color:rgb(62, 71, 83);">跨系统取证</font>**

+ <font style="color:rgb(62, 71, 83);">OMS/物流工具：查轨迹与 SLA；</font>
+ <font style="color:rgb(62, 71, 83);">计费/支付工具：核对重复扣款交易；</font>
+ <font style="color:rgb(62, 71, 83);">CRM：看是否 VIP、是否有历史补偿记录。</font>

<font style="color:rgb(62, 71, 83);">3.</font>**<font style="color:rgb(62, 71, 83);">政策推理与合规</font>**

+ <font style="color:rgb(62, 71, 83);">Policy/Critic Agent：套用“假期延误 + VIP + 改址”的组合条款，评估可给的补偿区间、是否可免费改址、是否触发风控人工复核。</font>

<font style="color:rgb(62, 71, 83);">4.</font>**<font style="color:rgb(62, 71, 83);">方案生成与协商</font>**

+ <font style="color:rgb(62, 71, 83);">提出“改址 + 走加急补发 / 或原包裹拦截 + 退款差额 + 账单冲正”的可行方案，并在对话中按用户反馈实时调整。</font>

<font style="color:rgb(62, 71, 83);">5.</font>**<font style="color:rgb(62, 71, 83);">执行与闭环</font>**

+ <font style="color:rgb(62, 71, 83);">调用工单/票据工具，落账/发券/改单/寄件，写入 CRM 备注；</font>
+ <font style="color:rgb(62, 71, 83);">生成总结，告知时限与跟踪号；</font>
+ <font style="color:rgb(62, 71, 83);">若任一步失败，自动选择备选策略或升级人工。</font>

<font style="color:rgb(62, 71, 83);">这些动作里，很多步骤</font>**<font style="color:rgb(62, 71, 83);">无法事先“画”成固定分支，需要在对话上下文里做决策、需要跨工具动态组合、需要“问一句 → 查一下 → 再决定”，</font>**<font style="color:rgb(62, 71, 83);">这正是 Agent 的强项。</font>

<font style="color:rgb(62, 71, 83);">  
</font>

## <font style="color:rgb(0, 0, 0);">5.</font><font style="color:rgb(62, 71, 83);">各Agent详细介绍</font>
### <font style="color:rgb(62, 71, 83);">5.1 AutoGPT</font>
:::color3
**简介：**<font style="color:rgb(62, 71, 83);">AutoGPT是第一个爆火的自主AI Agent框架，提供一系列工具让用户构建和使用自治代理。其功能涵盖代理创建模块“Forge”、性能评测基准agbenchmark、排行榜以及易用的UI和CLI接口。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">主要特点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(62, 71, 83);"></font>**<font style="color:rgb(62, 71, 83);">AutoGPT支持“思考-行动-反馈-学习”的循环，让代理不断生成子任务并执行。并且拥有丰富的插件和工具接口，允许代理访问浏览器、文件系统、API等资源，从而完成复杂的链式任务。</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">典型应用场景</font>**

:::

**<font style="color:rgb(62, 71, 83);"></font>**<font style="color:rgb(62, 71, 83);">需要让Agent自动拆解目标并执行的，如市场调研、行程规划、代码编写等</font>

:::color5
**<font style="color:#601BDE;">3.优势与不足</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023612-b33c2fdb-f65a-409a-8bf4-23c01f665b23.webp)

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">使用示例：基于AutoGPT让Agent帮我写一篇介绍AutoGPT的文章</font>**

:::

<font style="color:rgb(62, 71, 83);">1.创建Agent及配置名称、角色以及目标</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023652-43166619-431c-4df0-8c27-0f61ce7db897.webp)

<font style="color:rgb(62, 71, 83);">2.Agent 自主思考、规划、执行</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023745-d882b720-3079-43ff-84a5-358b20dc33be.webp)

<font style="color:rgb(62, 71, 83);">3.最终输出</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023859-6f6bee33-418f-4183-9140-3f34ad7169ae.webp)

### <font style="color:rgb(62, 71, 83);">5.2 LangGraph</font>
:::color3
**简介：**<font style="color:rgb(62, 71, 83);">LangGraph 是由 LangChain 团队推出的</font>**<font style="color:rgb(62, 71, 83);">有状态、持久运行、多智能体</font>**<font style="color:rgb(62, 71, 83);">应用的编排框架。核心将Agent建模成一个</font>**<font style="color:rgb(62, 71, 83);">图（Graph）</font>**<font style="color:rgb(62, 71, 83);">：每个节点是计算步骤（LLM 调用、工具函数、任意 Python 代码等），边控制流转（含条件与循环），并最终实现既定目标。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">Graph和预构建模式的示意图</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039023988-4ec165e4-a2b6-413f-8d1d-8272f1e4acd5.webp)

<font style="color:rgb(0, 0, 0);">  
</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039024139-186a984d-8502-4396-9305-12def201d8fc.webp)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">主要特点</font>**

:::

<font style="color:rgb(62, 71, 83);">支持图式编排、可人工干预、可中断/续跑。LangGraph可形成可控的分支/循环流程，可在每个节点中加入人工干预环节，适合需要人工审批/修订的业务场景，并且基于持久化状态可方便中断、续跑、回溯。</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">典型应用场景</font>**

:::

<font style="color:rgb(62, 71, 83);">可明确拆解任务步骤的场景，如RAG类、文章生成、日程助手等。</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">优势与不足</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039024168-4d847c2b-67b0-4d41-bd27-695567308eb7.webp)

:::color5
**<font style="color:#601BDE;">4.使用示例：基于LangGraph让Agent帮我写一篇介绍LangGraph的文章</font>**

:::

<font style="color:rgb(62, 71, 83);">1.构建工作流（Workflow）</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039024741-76d6156e-09bd-4edd-a51f-600a7b7f572c.webp)

<font style="color:rgb(62, 71, 83);">附工作流运行逻辑：</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039024668-432dba8d-09f1-443c-906d-661a39b65b20.webp)

<font style="color:rgb(62, 71, 83);">2.最终输出</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039024755-ef757ddc-be19-43e0-9640-b5ce473f6f79.webp)

### <font style="color:rgb(62, 71, 83);">5.3 Dify</font>
:::color3
**简介：**<font style="color:rgb(62, 71, 83);">Dify（Do It For You）是一个开源的低代码平台，旨在简化大模型（LLM）驱动的AI应用开发与部署。它融合了“后端即服务 (BaaS)”与 LLMOps 概念，提供涵盖模型接入、提示设计、知识库检索、智能代理、数据监控等在内的一站式解决方案。通过直观的可视化界面和预构建组件，开发者和非技术人员都可以快速构建如聊天机器人、内容生成、数据分析等各类生成式AI应用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">主要特点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(62, 71, 83);">低代码、可视化工作流构建、检索增强生成（RAG）管道、开放工具市场</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">典型应用场景</font>**

:::

<font style="color:rgb(62, 71, 83);">可明确拆解任务步骤的场景，如RAG类、文章生成、日程助手等</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039025065-005bda72-2629-4fe6-86f7-eee24cba3bfb.webp)

:::color5
**<font style="color:#601BDE;">3.使用示例</font>**

:::

<font style="color:rgb(62, 71, 83);">1.</font>**<font style="color:rgb(62, 71, 83);">工作流Workflow类型</font>**

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039025302-e35f946c-8fff-430f-93a0-f57547b3d124.webp)

<font style="color:rgb(62, 71, 83);">2.</font>**<font style="color:rgb(62, 71, 83);">Agent类型（Function Call）</font>**

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039025337-ad452413-bec5-4e5b-a184-df29da79b1dd.webp)

### <font style="color:rgb(62, 71, 83);">5.4 CrewAI</font>
:::color3
**简介：**<font style="color:rgb(62, 71, 83);">CrewAI 是一个多智能体（multi-agent）编排框架，其核心理念是让多个具备特定角色的 AI </font>**<font style="color:rgb(62, 71, 83);">代理</font>**<font style="color:rgb(62, 71, 83);">协同合作（组成“crew”团队）来完成复杂任务。每个代理被赋予特定的角色、目标和背景知识，通过相互分工与配合，自动地进行任务委派和问询，最终以团队形式完成用户交给的工作。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">主要特点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(62, 71, 83);">多工具及生态集成、支持Workflow和AI Agent两种模式</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">优势与不足</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039025471-b52a687c-bb77-4114-a99c-ad127774519e.webp)

:::color5
**<font style="color:#601BDE;">3.使用示例：研究AIagent领域的最新进展</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039025841-c54959c6-ccec-449f-a303-8f9546637472.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039025933-22d28dd0-cc48-4d57-a76a-aecdaf9013b3.webp)

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039026175-a4c17a7f-98e9-466f-af4c-7a9b26e16d46.webp)

### <font style="color:rgb(62, 71, 83);">5.5 AutoGen</font>
:::color3
**简介：**<font style="color:rgb(62, 71, 83);">AutoGen 是微软开源的一个面向 Agentic AI（代理式人工智能）的编程框架，用于构建 AI 智能体并促进多个智能体协作完成复杂任务。AutoGen 支持事件驱动的分布式架构，具有良好的可扩展性和弹性，可用于搭建可自主行动或在人类监督下运行的多代理 AI 系统。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">主要特点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(62, 71, 83);">微软开源、原生多Agent支持、灵活对话控制</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">优势与不足</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039026489-9967146b-7785-494d-9a4b-362b2536b4d2.webp)

:::color5
**<font style="color:#601BDE;">3.使用示例：Swarm模式下的机票退订助手示例：</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1761039026511-caba5826-7a23-47a3-8c57-c5ffa9cd24a3.webp)

### 
<font style="color:rgb(0, 0, 0);">  
</font>



