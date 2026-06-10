# ① Agent 上下文管理策略

<!-- source: yuque://zhongxian-iiot9/hlyypb/wz74qaort7s3fcwr -->

# **大模型Agent的发展趋势与开发实践**
:::color3
**简介：**本文探讨了大模型领域从通用能力向Agent落地演进的趋势，结合实际开发经验，阐述了深入理解Agent框架底层设计的重要性，并引出关于Agent上下文管理策略的系统性解析。

参考：[https://zhuanlan.zhihu.com/p/2012088406826562496](https://zhuanlan.zhihu.com/p/2012088406826562496)

:::

、![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773399426711-d94ba199-115d-4ba4-ba7e-d87bba485ede.png)

:::color5
**<font style="color:#601bde;">1. 行业发展趋势：从通用能力向Agent落地演进</font>**

:::

近期，国内多家头部厂商密集发布了旗舰版大模型（如GLM5、MiniMaxM2.5、Qwen3.5）。这一现象表明，大模型领域的竞争焦点已从单纯的通用能力比拼，实质性地转向了Agent落地与编程能力两大核心方向。

随着Claude Code、OpenClaw等Agent Scaffold框架的迅速普及，行业定位正全面向Agentic Engineering倾斜，实现了从“被动响应的聊天机器人（chatbots that respond）”到“主动执行的智能体（agents that act）”的范式转变。

:::color5
**<font style="color:#601bde;">2. 开发者工具的演进与能力反思</font>**

:::

在实际研发场景中，Claude Code等Agent框架已成为提升效率的重要工具。此类工具不仅能协助开发者快速梳理复杂代码框架的模块实现原理，还能高效完成新特性的开发工作，极大降低了复杂系统的学习与开发成本。

然而，对于处于基础能力建设阶段的学习者（如学生群体），过度依赖此类工具可能存在隐患。在涉及数据结构、操作系统等底层基础知识时，仍需注重自身核心能力的锻炼。行业实践表明，仅依赖工具而缺乏对代码深度理解的工程师，在处理复杂框架修改时往往难以保证代码质量。因此，具备过硬的自身编程能力，并能高效利用Code Agent辅助开发的复合型人才，是当前行业的核心需求。

:::color5
**<font style="color:#601bde;">3. 核心工作目标与专题规划</font>**

:::

为顺应行业趋势，当前研发团队的核心工作项之一是：**提升自研模型的Agentic Coding能力，确保模型API能够无缝接入Claude Code、OpenCode等主流框架，从而更好地赋能开发者。**





# **Context Engineering：什么是上下文工程**
:::color3
**简介：**本节阐述了上下文工程的定义及其在多轮推理任务中的核心目标，并深入分析了随着上下文增长而导致的“上下文腐败”现象及其对智能体性能的影响。<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773399538583-4ceaecb5-e332-43ce-99f9-d603f6093a21.png)

_“人们分散到世界的四面八方，彼此成了仇敌。但他们的记忆仍留下了他们见过的事情，永不磨灭。”——《太古和其他的时间》，奥尔加 · 托卡尔丘克_

:::color5
**<font style="color:#601bde;">1. 上下文工程的定义与核心目标 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

上下文工程（Context Engineering）是指在大型语言模型（LLM）的客观约束下（如上下文窗口大小、注意力机制长度限制等），通过优化上下文Token的效用，以持续获得理想输出结果的工程实践。

其核心目标在于：**使用规模最小、信号最强的Token集合，最大化模型输出期望结果的概率。**

在Agent的持续运行过程中，会不断产生对后续推理具有潜在价值的新数据。这些数据必须被纳入上下文中，作为模型的“短期记忆”。上下文工程的核心任务，便是从动态变化的海量信息中，精准筛选出最适合放入有限上下文窗口的关键内容。

_概念对比：_

+ **Prompt Engineering（提示词工程）**：主要适用于单轮文本生成任务。
+ **Context Engineering（上下文工程）**：专为需要多轮推理、长时间运行的智能体设计，侧重于管理不断演变的上下文状态。

_注：上下文工程需要从海量信息（文档、工具、记忆文件等）中进行筛选，以形成最优的上下文窗口。_

:::color5
**<font style="color:#601bde;">2. 上下文工程在智能体构建中的必要性</font>**

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773399426711-d94ba199-115d-4ba4-ba7e-d87bba485ede.png)

Agent在每次调用工具后，都会获取相应的观察结果（Observation），并将其追加至历史记录中。在生产环境中，Agent的对话轮次可能高达数百轮，导致历史消息呈指数级增长。此外，工具调用的返回结果往往极为冗长（例如读取大文件片段或执行Bash命令产生的长日志）。这些长文本的不断拼接，极易突破模型所能支持的最大上下文长度阈值（如128K至1M）。

尽管现代LLM支持的序列长度不断提升，但随着上下文的增加，模型会出现类似于人类“注意力涣散”的现象，即准确召回信息的能力下降，推理速度减缓。这一现象在学术界被称为“上下文腐败”（Context Rot）。研究表明，几乎所有模型在远未达到其声明的最大序列长度时（例如标称支持1M Token，但在200K Token时），就已经开始显现上下文腐败。

导致该现象的主要原因包括：

+ **注意力分散**：在Transformer架构中，每个Token都需要与上下文中的所有其他Token建立关联，形成平方级别的计算关系。随着序列长度增加，注意力权重被过度摊薄，导致关键信息的关注度下降。
+ **训练数据偏差**：模型在预训练阶段接触的长序列数据远少于短序列数据，导致其处理长距离依赖关系的能力相对薄弱。
+ **技术折中**：虽然位置编码插值等技术能够扩展模型对长序列的适应性，但这通常以牺牲一定的推理精度为代价。

# **上下文工程的核心策略**
:::color3
**简介：**本节详细解析了Agent框架中常见的四种上下文管理策略：上下文卸载与检索、上下文摘要、多智能体架构隔离以及KV缓存机制，并结合实际框架案例说明了其工作原理与应用场景。

:::

:::color5
**<font style="color:#601bde;">1. 上下文卸载与检索（Context Offload & Retrieval） </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

鉴于上下文窗口的有限性，无法将所有信息驻留在Agent的短期记忆中。合理的策略是将冗余信息“卸载”至外部存储系统，并在需要时进行精确检索。

在处理超长输出（如Shell命令结果、MCP返回数据）时，简单的截断策略存在极高风险，可能导致关键报错信息或核心线索永久丢失。由于Agent需要基于全局历史状态预测下一步动作，开发者无法预判哪些信息在后续步骤中具有决定性作用。因此，**任何不可逆的信息压缩都是不可取的**。

**（1）将上下文卸载到文件系统（紧凑化, Compaction）**

Manus框架提出了一项核心理念：**将文件系统视为终极上下文**。文件系统具备无限容量、持久化存储及随机访问等特性，Agent可通过路径、文件名、时间戳等元数据高效组织信息。该策略的最大优势在于其**可逆性**：

+ **网页访问**：仅保留URL，移除网页具体内容。需要时重新发起请求。
+ **文档处理**：仅保留文件路径，省略文档正文。需要时通过 `cat` 或 `tail` 命令读取。
+ **日志分析**：移除完整的日志输出，仅保留日志文件的存储路径。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773400315225-446aae05-1e1b-4951-9c0c-8f2605e49648.png)

这种“可逆压缩”在有效缩减上下文长度的同时，确保了信息的完整性。同时，鼓励Agent主动将中间结果持久化（例如将复杂查询结果写入 `output.log`，上下文中仅保留“结果已写入某路径”的提示），后续通过 `head`、`grep` 等命令渐进式读取。

**（2）检索机制：推理前检索 vs. 实时检索（Just-in-time Retrieval）**

早期Agent多依赖RAG（检索增强生成）这种“推理前检索”模式。然而，Manus、Claude Code等新锐框架正逐步弱化RAG，转而采用**实时检索（Just-in-time Retrieval）**。

_弱化RAG的原因_：RAG系统组件繁杂，涉及文本分块策略、Embedding模型选择、相似度计算等多个变量，且难以有效处理非结构化数据（如PDF、图片）。现代Agent框架倾向于“Keep Things Simple, Dummy”原则，将复杂的检索逻辑交由模型自身处理。

_实时检索的优势（以Claude Code为例）_：  
模型能够自主生成复杂的Bash命令（如 `ripgrep`、`jq`、`find`），利用正则表达式精准定位代码块，无需将海量数据加载至上下文。

+ **灵活性**：搜索策略动态调整，不受预置索引限制，始终获取最新状态数据。
+ **渐进式探索**：模拟人类认知过程，例如在Debug时，先通过 `grep` 查找函数定义，再搜索调用位置，最后查看具体文件上下文，每一步均基于前置结果动态推进。

:::color5
**<font style="color:#601bde;">2. 上下文摘要（Context Summarization） </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

_“他们沉回了来时的大地。而他们的孩子则被留了下来，对黄金时代—— 时间出现前的那个时代，只剩模糊的记忆。” ——《人之涛》，刘宇昆_

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773400332515-8032e39d-e11f-4421-9c55-87569635ff7e.png)

当上下文窗口濒临极限且无法继续执行紧凑化操作时，**摘要化**成为最后的兜底手段。作为一种有损压缩，摘要化会将对话历史浓缩，释放空间，但这不可避免地会导致精确信息（如具体代码行、完整工具输出）的丢失。

为了弥补这一缺陷，摘要化机制必须具备**可恢复性**。具体实现方式为：在执行摘要前，将完整的对话历史（包含原始消息、工具调用及结果）**全量Dump至持久化文件**中。若Agent在后续交互中发现摘要缺失关键细节，可通过 `grep` 或 `Read` 等工具主动检索该历史文件，实现记忆找回。

_注：在实际应用中，当超过Context Limit时，系统会进行压缩；若压缩后发现信息丢失，Agent会从持久化的对话记录中搜索找回。_

为保障模型工作的平滑过渡，系统通常会保留最近几次完整的工具调用及其结果，以维持模型风格与语气的连贯性，防止因上下文重置导致的“失忆”现象。

**策略选择：紧凑化 vs. 摘要化**  
系统应优先采用可逆的紧凑化策略。仅当紧凑化空间耗尽且上下文即将溢出时，才启动带有备份机制的摘要化策略。两者结合，使Agent能够在有限的窗口内处理理论上无限长的任务。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773403466126-92e5f98c-722d-49a4-aca2-7869fe6585e9.png)

**Claude Code 压缩流程案例解析**

Claude Code的压缩机制分为两种触发方式：

1. **自动触发**：系统监控Token使用量，逼近上限时自动执行。
2. **手动触发**：用户通过 `/compact` 命令主动执行。

以下为执行 `/compact` 命令后的核心日志结构（已脱敏）：

```latex
Compact summary
  ⎿  This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the
     conversation.

     Summary:
     1. Primary Request and Intent:
        用户在上一轮对话（xxxx）结束后，对 xxxx产生了好奇，连续提出了四个问题：
        ......

     2. Key Technical Concepts:
        ......

     3. Files and Code Sections:
        ......

     4. Errors and fixes:
        xxxx, 我把它们搞混了

     5. Problem Solving:
        ......

     6. All user messages: ###用户所有的input
        ......

     7. Pending Tasks:
        - 无明确待办任务。上一轮关于xxxx的任务已完成，用户表示会验证，但尚未反馈验证结果。

     8. Current Work:
        最后回答的问题是：xxxx。

        回答要点：
        ......

     9. Optional Next Step:
        无明确下一步任务。用户的问题已全部回答，且没有新的待办事项。如有需要可继续讨论 xxx，或回到上一轮的 xxx
     文档验证工作。

     If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full
     transcript at: /root/.claude/projects/PATH/SESSION_ID.jsonl
```

系统使用上述摘要替换旧的对话历史。同时，原始对话被完整保存在 `/root/.claude/projects/PATH/SESSION_ID.jsonl` 文件中，确保Agent在需要时能够主动读取并“回忆”精确细节。

:::color5
**<font style="color:#601bde;">3. 上下文隔离（多智能体架构） </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

面对复杂任务，系统可采用任务分解策略，由主智能体（Main Agent）协调多个专业化的子智能体（Sub-agents）协同处理。

每个子智能体均运行在独立的上下文窗口中，拥有专属的系统提示词（System Prompt）和工具权限（Tool Access）。主智能体会根据任务需求，动态将特定任务委托给合适的子智能体。

**多智能体架构的核心优势：**

+ **优化主Agent上下文**：子智能体的探索过程不会污染主对话上下文，其仅将精简摘要返回给主Agent，有效控制了主上下文的长度。
+ **精细化权限控制**：可严格限制子智能体的工具权限（如设定为只读模式）。例如，Claude Code内置的 `Explore` 为只读Agent，而 `General-Purpose` 为全能型Agent。
+ **领域专业化提升**：通过定制化的系统提示词提升特定任务的处理质量。
+ **优化调用成本**：将简单任务路由至低成本模型。例如，Claude Code中的 `Explore` 任务调用Haiku模型，而复杂的 `Plan` 任务则调用Sonnet或Opus模型。

**多智能体架构分类：**

+ **按运行模式划分：**
    - **前台运行模式**：子智能体阻塞主对话，权限请求实时传递给用户，需用户手动确认每步操作。
    - **后台运行模式**：子智能体在后台异步执行，启动前预先收集权限，运行中自动拒绝越权操作，不影响用户与主Agent的并发交互。
+ **按调用关系划分：**
    - **并行调用**：多个子智能体独立运行，互不依赖，最终由主Agent汇总结果。
    - **链式调用**：子智能体顺序执行，后续节点依赖前置节点的输出（如Code-reviewer与Optimizer的协同）。

**Claude Code 子智能体调用案例解析**

Claude Code遵循极简设计原则，主Agent通过生成自身的**克隆体**来创建子Agent，且**严格禁止子Agent进一步派生**，以防止无限递归。子Agent执行完毕后，结果以工具响应的形式返回主历史。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773399840419-a7db47a1-33f6-476b-8883-b391217e323e.png)

_执行流程示例_：  
用户输入指令：“分析 opencode 项目的 agent 系统：找出关键入口文件、核心数据结构、以及 sub-agent 是怎么被调用的，用中文写一份分析报告存到/tmp/agent-analysis.md”

主Agent随之调用 `General-Purpose` 子智能体在后台运行：

```latex
● Agent(Analyze opencode agent system)
⎿ Backgrounded agent ##表明是后台运行的subagent
⎿ Prompt: ###给subagent的任务描述
请分析 opencode 项目的 agent 系统实现。
具体要做的事：

1. 用 Glob 找到 agent 相关的源文件（在 packages/opencode/src/ 下）
2. 用 Grep 搜索关键词：subagent、spawn、AgentTool 等，找到 sub-agent 调用
3. 读取核心文件，理解：

- agent 的入口在哪里
- agent 的核心数据结构是什么
- sub-agent 是如何被创建和管理的

4. 把分析结果用中文写成一份报告，存到 /tmp/agent-analysis.md
报告格式：
opencode Agent 系统分析
5. 关键文件列表
6. 核心数据结构
7. Sub-agent 调用机制
8. 与 Claude Code 的对比推测
请认真探索，不要只猜测，要基于实际读到的代码。
● Agent 已在后台运行，实时看它的进度：
```

任务触发了Glob、Grep、Read、Write等多种工具的组合调用。完成后系统提示 `● Agent "Analyze opencode agent system" completed`，并成功生成目标报告。

:::color5
**<font style="color:#601bde;">4. 上下文缓存（KV Cache） </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**KV Cache（KV缓存）的工作原理**  
在Transformer模型生成Token的过程中，需要计算历史Token的Key和Value向量以支持注意力机制。KV Cache技术将这些中间计算结果进行持久化保存。当后续请求包含完全相同的前缀（Prefix）时，系统可直接复用缓存，避免冗余计算。

_Prefill（预填充）阶段_：在生成首个输出Token前，模型对所有输入Token进行并行处理，计算KV向量并构建缓存。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773403502969-51fcd34c-1914-46ae-baaf-1f86c51d9ea6.png)

**缓存机制对Agent的核心价值**  
Agent的工作流本质上是“输入-决策-执行-追加”的循环。统计表明，Agent的输入输出Token比例通常高达 **100:1**。若无缓存机制，每轮推理均需重新计算庞大的历史上下文，导致极高的延迟与成本。  
引入KV Cache后，系统仅需处理新追加的内容，大幅降低了首字延迟（TTFT）。此外，缓存命中与未命中的成本差异巨大（以Claude Sonnet为例，成本相差可达10倍）。

**KV 缓存的工程设计原则（以Claude Code为例）****<font style="color:#601bde;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

缓存命中的苛刻条件要求请求前缀必须**绝对一致**（任何微小的格式差异均会导致缓存失效）。因此，工程实现需遵循以下原则：

1. **Append-Only（仅追加）原则**：严禁修改历史上下文（如在System Prompt中插入动态时间戳）。若需修正历史，应通过追加新消息实现。
2. **序列化确定性**：确保数据结构（如JSON）序列化时的键顺序稳定，避免因哈希值变动导致缓存穿透。

**Claude Code 缓存模式配置**

+ **自动缓存**：  
在请求顶层配置 `cache_control` 字段，系统将自动把最后一个可缓存块设为**缓存断点**。默认生命周期（TTL）为5分钟，命中后自动续期。

```json
{ "cache_control": { "type": "ephemeral", "ttl": "1h" } }
```

API调用示例：

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"}, ### 触发自动缓存
    "system": "You are a helpful assistant that remembers our conversation.",
    "messages": [
      {"role": "user", "content": "My name is Alex. I work on machine learning."},
      {"role": "assistant", "content": "Nice to meet you, Alex! How can I help with your ML work today?"},
      {"role": "user", "content": "What did I say I work on?"}
    ]
  }'
```

+ **显式缓存（结合自动缓存）**：  
对于极度稳定的内容（如System Prompt、工具定义），可手动设置显式断点。系统最多支持4个缓存断点（含自动缓存槽位）。

```json
{
  "model": "claude-opus-4-6",
  "max_tokens": 1024,
  "cache_control": { "type": "ephemeral" },                // 自动缓存配置
  "system": [
    {
      "type": "text",
      "text": "You are a helpful assistant.",
      "cache_control": { "type": "ephemeral" }             // 显式断点配置
    }
  ],
  "messages": [{ "role": "user", "content": "What are the key terms?" }]
}
```



# 参考资料
+ [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
+ [MinusX: Decoding Claude Code](https://minusx.ai/blog/decoding-claude-code/#21-use-claudemd-for-collaborating-on-user-context-and-preferences)
+ [Manus: Context Engineering for AI Agents](https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
+ [Claude Platform Documentation](https://platform.claude.com/docs/)

