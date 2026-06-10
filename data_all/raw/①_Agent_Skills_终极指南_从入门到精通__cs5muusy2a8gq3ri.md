# ① Agent Skills 终极指南：从入门到精通

<!-- source: yuque://zhongxian-iiot9/hlyypb/cs5muusy2a8gq3ri -->

## 背景
:::color3
**简介：Skills 允许非技术人员用自然语言零代码编写智能 Agent，能够突破预设限制灵活应对边缘情况，并支持多 Skill 自由联用，代表了垂直 Agent 的未来形态。**本文详细拆解了如何利用**<font style="color:#ED740C;">通用 Agent 内核与 Skills 设计</font>**，低成本创造具有高智能上限的垂直 Agent 应用，巧借通用 Agent 内核，只靠 Skills 设计，就能低成本创造具有通用 AI 智能上限的垂直 Agent 应用。

:::

:::color5
**<font style="color:#601bde;">1. Skills 被低估价值 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Claude Skills 的价值，还是被大大低估了。一个好 Skill 能发挥的智能效果，甚至能轻松等同、超越完整的 AI 产品。任何不懂技术的人，都能开发属于自己的 Skills。  
	比如做的 Article-Copilot，一个 skill 就实现了从素材处理到正文写作的 Agent 应用；又如 AI Partner Skill，让通用 Agent 深度学习你的记忆，塑造懂你的 AI 伴侣，给到个性回应。

![](https://cdn.nlark.com/yuque/0/2026/jpeg/29769680/1770087070535-b2f7d71d-0ef6-4f7f-a6bb-d6c41ea6c068.jpeg)

:::color5
**<font style="color:#601bde;">2. 本文核心内容概览</font>**

:::

在研读 Anthropic 官方技术博客，与持续 Agent Skill 实验之后，形成了这份全网最完整的 Skill 指南，包含：

1. 最容易读懂的 Skills 概念与原理介绍
2. 讨论 Skills 的真实价值、技术优势、对 AI 产品设计的影响
3. 非常完整的 Skills 使用与开发教程
4. Skills 的场景识别，什么时候适合开发、使用 Skills？  
从概念澄清、运作机制，到实践教程、应用价值，与你在本期分享。

## Skills 是什么：从概念来源到运作原理
:::color3
**简介：**Skills 可以被理解为**<font style="color:#ED740C;">“通用 Agent 的扩展包”</font>**，它不同于 MCP 协议，是将任务逻辑、工具和知识封装在一起的完整能力包，让 Agent 具备稳定可复用的做事方法。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770099365400-2fa72348-410c-489c-98e0-372b8efd3a01.png)



![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770099380602-953cae17-1859-468b-8af7-b71dad583c7a.png)

:::color5
**<font style="color:#601bde;">1. 概念起源与定义 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

2025 年 10 月中旬，Anthropic 正式发布 Claude Skills。两个月后，Agent Skills 作为开放标准被进一步发布，意在引导一个新的 AI Agent 开发生态。OpenAI、Github、VS Code、Cursor 均已跟进。  
	为了更好的理解，你可以把 Skills 理解为**<font style="color:#74B602;">“通用 Agent 的扩展包”</font>**：Agent 可通过加载不同的 Skills 包，来具备不同的专业知识、工具使用能力，稳定完成特定任务。

:::color5
**<font style="color:#601bde;">2. Skills 与 MCP 的区别</font>**

:::

最常见的疑惑是：这和 MCP 有什么区别？

+ MCP 是一种 开放标准的协议，关注的是 AI 如何以统一方式调用外部的工具、数据和服务，本身不定义任务逻辑或执行流程。
+ Skill 则教 Agent 如何完整处理特定工作，它将执行方法、工具调用方式以及相关知识材料，封装为一个完整的「能力扩展包」，使 Agent 具备稳定、可复用的做事方法。  
以 Anthropic 官方 Skills 为例：
+ PDF：包含 PDF 合并、拆分、文本提取等代码脚本，教会 Agent 如何处理 PDF 文件。
+ Brand-guidelines：包含品牌设计规范、Logo 资源等，Agent 设计网站、海报时，可参考 Skill 内的设计资源，自动遵循企业设计规范。
+ Skill-Creator：把创建 Skill 的方法打包成元 Skill，让 AI 发起 Skill 创建流程，引导用户创建出符合需求的高水准 Skill。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770099395362-78b4a61a-3de4-4161-bbb7-12f71e604b29.png)

:::color5
**<font style="color:#601bde;">3. 运作原理：工作交接 SOP 大礼包 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Anthropic 说：Skills 是模块化的能力，扩展了 Agent 的功能。每个 Skill 都打包了 LLM 指令、元数据、可选资源（脚本、模板等），Agent 会在需要时自动使用他们。  
我有个更直观的解释：Skill 就像给 Agent 准备的工作交接 SOP 大礼包。想象你要把一项工作交给新同事，你会准备：任务的执行 SOP 与必要背景知识、工具的使用说明、要用到的模板素材、可能遇到的问题解决方案。  
Skill 的设计架构几乎是交接大礼包的数字版本：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770099471821-ab9a6814-5aed-48fa-8292-6729ef2c3760.png)

+ SKILL.md：核心文件，包含技能的元数据和任务指导。
+ Scripts/：包含 Agent 可用的各类预先写好的程序脚本。
+ References/：参考文档。
+ Assets/：素材资源。  
当 Agent 运行某个 Skill 时，就会以 SKILL.md 为第一指引，结合任务情况判断何时调用脚本、翻阅文档或使用素材，通过“规划-执行-观察”的循环完成目标。

## Skills 的真实价值：垂直 Agent 的未来态
:::color3
**简介：**Skills 允许非技术人员用**<font style="color:#ED740C;">自然语言零代码编写智能 Agent</font>**，能够突破预设限制灵活应对边缘情况，并支持多 Skill 自由联用，代表了垂直 Agent 的未来形态。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770102725709-f6c74a48-8b09-4468-82a6-efa7307e6adb.png)

:::color5
**<font style="color:#601bde;">1. 零代码、自然语言，编写真·智能 Agent </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Skills 的创建门槛极低，但智能上限极高。非技术人员可用零代码、自然语言编写。

+ 简单案例 (Brand-guidelines)：仅有一个 SKILL.md，纯自然语言写成。包含元信息和品牌颜色、字体等描述。足以引导 Agent 变成符合 Anthropic 品牌设计的垂直 Agent，可用于品牌官网、海报、PPT 设计。
+ 复杂案例 (AI-Partner Skill)：一个 Skill 就是一个复杂 Agent。包含 SKILL 文档、向量数据库构建指南、脚本、Persona 模板资源。Agent 能理解初始化与对话方法，引导用户上传记忆文档，构建向量数据，提供懂用户的 AI Partner 对话体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100659343-39a034fa-defe-49db-a059-197aee7a9d01.png)

:::color5
**<font style="color:#601bde;">2. 突破预设限制，灵活应对实际情况 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Workflow 或传统程序假设所有情况都能预设，遇到意外格式或边缘情况容易报错。而通用 Agent + Skill 应用能在统一对话框接收各类数据，自主调用 Skill 或编写脚本转换格式，基于 LLM 推理智能弥合边缘问题。  
	例如在 AI-Partner-Chat 中，Agent 能借本身的“观察-规划-执行”动态智能，对用户文档进行自适应切片，而非按照固定分隔符切分，得到更符合实际情况的 RAG 切片。

:::color5
**<font style="color:#601bde;">3. 多 Skills 自由联用</font>**

:::

Agent Skills 实质是 Context 工程。Skills 在实际应用中极其灵活，一次任务中能调用多个 Skill。比如联用 brand-guidelines + pptx 自动制作符合品牌规范的 pptx，或联用 AI-Partner-Chat + Article-Copilot 写出符合个人文风的内容。每多一个 Skill，就多一种能力，N 个 Skill 可以应对远超 N 的应用场景。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770099552374-0071fa75-e5bb-4f33-90ca-ade37ae83a0c.png)

:::color5
**<font style="color:#601bde;">4. 核心运行机制：渐进式披露 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

为了解决 Context 过长导致模型能力下降的问题，Skills 采用了渐进式披露机制。Skill 包放在 Agent 文件系统中，根据优先级分层加载：

+ Level 1 (元数据)：始终加载，仅包含名称与用途描述，约 100 tokens。
+ Level 2 (指令)：SKILL.md 正文，触发时加载。
+ Level 3 (资源/代码)：子技能文档、脚本、参考文档等，按需动态读取。  
这种机制允许给一个 Agent 安装很多 Skills 而不拖垮上下文性能。

:::color5
**<font style="color:#601bde;">5. 对 AI 产品设计的影响</font>**

:::

Skills 是一种非常宽容的 Agent 设计架构，它可以是引导思考的 Prompt，也可以是直接运行的代码脚本。随着 Token 价格下降和 Agent 速度提升，Skills-based 的垂直 Agent 在性能开销上的问题将不再是障碍。  
未来 AI Native 产品趋势可能是：用同一个多模态输入框处理各种输入，通过内置 Skills 智能规划处理逻辑，既能快速响应（代码逻辑），又能灵活应对边缘情况（推理逻辑）。

## Skills 完全教程：制作与使用
:::color3
**简介：**本教程详细指导如何安装 Claude Code（或替换为国产模型），以及如何查找、安装和使用 Skills，甚至利用 Skill-Creator 自动生成自己的 Skill。

:::

:::color5
**<font style="color:#601bde;">1. 教程：如何使用 Skills（Claude Code 版） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ 使用 Skills 最推荐的方法是利用 Claude Code (CC)。CC 不仅是 Coding 工具，更是跑在电脑上的通用 Agent 框架。
    - Step 1：安装 Claude Code  
通过终端安装，推荐将官方指引链接发给 AI（如 ChatGPT、Kimi），让它一步步指导安装。安装成功后输入 `claude --version` 可查看版本。
    - Step 2：替换模型（可选）  
如果不用 Claude 模型，可替换为 GLM 4.7、Kimi K2 等国产模型。搜索“模型名称 + Claude Code”教程，或使用「CC Switch」工具进行管理。
    - Step 3：安装并使用 Skills
+ 建议在空文件夹启动 CC（输入 `claude`）。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100826550-d078c254-b193-4a59-9f60-82da2552ce20.png)

+ 自动安装：在 CC 中发送 `安装 skill，skill 项目地址为：[https://github.com/anthropics/skills/tree/main](https://github.com/anthropics/skills/tree/main)`。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100814657-9991a96e-54a1-494c-be63-301f0bbb34d7.png)

+ 手动安装：下载 Skill 包解压放入 `/.claude/skills/` 目录。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100806450-d3aba128-3561-4ede-9a2d-771d2c0ed749.png)

+ 使用：发送 `开始使用 <skill 名称>` 或直接输入与 Skill 匹配的需求，CC 会自动调用。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100849411-ad6693a4-64cc-4b3a-b818-279afab9e971.png)

:::color5
**<font style="color:#601bde;">2. 怎么找到好用的 Skills？ </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

常规方法是去第三方 Skills 市场，但往往缺乏评价体系。推荐关注 Mulerun，他们正在打造全球性的 Agent 市场，将支持创作者上架 Skill，并提供一键运行、自动评分和精选发现机制。

[https://skillsmp.com/zh](https://skillsmp.com/zh)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100874202-f3f2496c-3a19-44a1-8fc1-9b95d2fe64b8.png)

:::color5
**<font style="color:#601bde;">3. 如何制作一个 Skill？ </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

利用 Anthropic 官方的 skill-creator 可以自动开发 Skill。

1. 安装 skill-creator。[https://github.com/anthropics/skills/tree/main/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
2. 发送创建需求给 CC（例如：“创建新的 SKILL，能自动把用户指定的 PDF 转成 WORD 文档”）。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100902043-a5d83ca0-1db4-4072-9b8a-bf84a341aa0c.png)

3. CC 会自动编写 SKILL.md 和脚本。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100908821-b14580e5-9376-4827-b59a-e4b7db69b106.png)

4. 生成的 Skill 可直接安装使用。

## 什么时候应该用 Skills？
:::color3
**简介：**当发现需要反复向 AI 解释同一件事、任务依赖特定知识模板、或需要多个流程协同完成时，就是开发和使用 Skills 的最佳时机。

:::

:::color5
**<font style="color:#601bde;">1. 发现自己在向 AI 反复解释同一件事 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

如果在多轮对话中，需要不断向 AI 解释规则（如技术文档格式、代码模板、数据分析规则），不如把这些规则打包成一个 Skill，一次创建永久复用。

<font style="color:rgb(25, 27, 31);">比如：</font>

> <font style="color:rgb(83, 88, 97);">“帮我写一份技术文档”  
</font><font style="color:rgb(83, 88, 97);">“不对，我们公司的技术文档格式是这样的……”  
</font><font style="color:rgb(83, 88, 97);">“还有，代码示例要按这个模板来……”  
</font><font style="color:rgb(83, 88, 97);">“上次不是说了吗，章节标题要三级标题……”  
</font><font style="color:rgb(83, 88, 97);">“帮我分析这个数据”  
</font><font style="color:rgb(83, 88, 97);">“先把 ＞ XX 的异常值筛掉”  
</font><font style="color:rgb(83, 88, 97);">“不对，应该用中位数，不是平均值”  
</font><font style="color:rgb(83, 88, 97);">“图表要按我们公司文档的配色方案……”</font>
>

<font style="color:rgb(25, 27, 31);">这时候就该想到：与其每次都解释一遍，不如把这些规则打包成一个 Skill，一次创建永久复用。</font>

:::color5
**<font style="color:#601bde;">2. 某些任务需要特定知识、模板、材料才能做好</font>**

:::

当 AI 通用能力足够但缺乏特定场景材料时（如品牌设计需参考 Logo、技术写作需参考术语表），将这些材料放入 Skill 包，Agent 就能输出精准结果。

+ **<font style="color:rgb(25, 27, 31);">技术文档写作</font>**<font style="color:rgb(25, 27, 31);">：需要参考代码规范、术语表，使用文档模板</font>
+ **<font style="color:rgb(25, 27, 31);">品牌设计</font>**<font style="color:rgb(25, 27, 31);">：需要参考品牌手册、色彩规范，使用 Logo 资源</font>
+ **<font style="color:rgb(25, 27, 31);">数据分析</font>**<font style="color:rgb(25, 27, 31);">：需要参考指标定义、计算公式，使用报表模板……</font>

:::color5
**<font style="color:#601bde;">3. 发现一个任务要多个流程协同完成</font>**

:::

对于竞品分析报告、内容生产等需要组合多个流程的任务，可以将各环节的指令、脚本、资源打包成 Skill，让 Agent 智能调用，一次性完成复杂任务。

+ **<font style="color:rgb(25, 27, 31);">竞品分析报告</font>**<font style="color:rgb(25, 27, 31);">：检索竞品数据 + 数据分析 + 制作 PPT</font>
+ **<font style="color:rgb(25, 27, 31);">内容生产</font>**<font style="color:rgb(25, 27, 31);">：收集参考资料 + 学习风格 + 大纲协作 + 正文写作</font>

## 总结
:::color3
**简介：**Skills 是 Agent 的灵魂，降低了验证想法的成本，让非技术专家也能快速接入 Agent 能力，创造兼具通用智能的垂直应用。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770100956196-7768651b-3b78-44ff-b92b-1184cf4661a6.png)

:::color5
**<font style="color:#601bde;">1. Skills 是 Agent 的灵魂 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Skills 就像 Steam 游戏 + 创意工坊一样，赋予了 Agent 极强的可扩展性。开发者只需关注 Skills 设计，就能低成本创造垂直 Agent 应用。

:::color5
**<font style="color:#601bde;">2. 降低验证成本，赋能非技术专家</font>**

:::

Skill 让更多人、更多场景接入 Agent 能力变得可行：不必开发完整产品，打包 Skill 即可解决内部需求；不必等待 IT 排期，自己就能创建工具。Skill 大大降低了验证想法的成本。

:::color5
**<font style="color:#601bde;">3. 参考文献</font>**

:::

+ Claude Doc - Agent Skills 说明：[<font style="color:rgb(9, 64, 142);background-color:transparent;">https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview</font>](https://link.zhihu.com/?target=https%3A//platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
+ Agent Skills 开放标准：[<font style="color:rgb(9, 64, 142);background-color:transparent;">https://agentskills.io/home</font>](https://link.zhihu.com/?target=https%3A//agentskills.io/home)
+ Equipping agents for the real world with Agent Skills：[<font style="color:rgb(9, 64, 142);background-color:transparent;">https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills</font>](https://link.zhihu.com/?target=https%3A//www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

  


