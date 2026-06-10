# ① Agent Harness 范式详解

<!-- source: yuque://zhongxian-iiot9/hlyypb/ggld5godq6sb01w2 -->

:::success
**背景：**2026 年 2 月，“[Harness Engineering](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Harness+Engineering&zhida_source=entity)”一词在 AI 工程领域引发广泛关注。[Mitchell Hashimoto](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Mitchell+Hashimoto&zhida_source=entity) 在其博客中首次提出该概念，随后 [OpenAI](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=OpenAI&zhida_source=entity) 发布了百万行代码级别的实验报告，Martin Fowler 亦撰写了深度分析文章。短短数周内，该术语已成为探讨 AI Agent 开发的核心议题。<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

# **什么是 Harness Engineering**
:::color3
**简介：**Harness Engineering 是一种围绕 AI Agent（尤其是 Coding Agent）展开的系统工程实践，旨在通过设计约束机制、反馈回路、工作流控制及持续改进循环，确保 AI Agent 在具备强大代码生成能力的同时，其输出结果保持高可靠性、一致性及长期可维护性。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919742323-48400d67-1f05-4ece-8a2e-faced93937d9.png)

:::color5
**<font style="color:#601bde;">1. 核心定义与概念类比</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**Harness Engineering** 的核心目标在于解决 AI Agent 输出的稳定性与可控性问题。“Harness”一词本意为马具（如缰绳、鞍具），用于引导马匹的力量至正确方向。将其类比于 AI Agent 极为贴切：大型语言模型（LLM）犹如一匹动力强劲但方向感欠佳的骏马，虽具备高效的生成能力，但极易偏离既定目标。

:::color5
**<font style="color:#601bde;">2. 三层工程概念的嵌套关系</font>**

:::

Harness Engineering 并非孤立存在，而是 [Prompt Engineering](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Prompt+Engineering&zhida_source=entity) 与 [Context Engineering](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Context+Engineering&zhida_source=entity) 的自然演进。三者之间呈现出明确的嵌套关系。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919429707-eaa36c04-f168-4115-a270-6133e1bf2aaa.png)

专家 Phil Schmid 对此进行了生动的比喻：**模型如同 CPU，而 Harness 则是操作系统**。若操作系统效能低下，CPU 性能再强亦无法发挥。学者 mtrajan 的界定则更为直观：Context Engineering 负责管理“向 Agent 提供何种信息”，而 Harness Engineering 则专注于“系统如何保障稳定性、如何进行量化评估以及如何实现自我修复”。

:::color5
**<font style="color:#601bde;">3. 术语的演进与普及</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

尽管在 2025 年底已有零星讨论，但该概念真正确立为专业术语是在 2026 年 2 月，主要由以下关键事件推动：

+ **Mitchell Hashimoto**（HashiCorp 联合创始人、[Terraform](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Terraform&zhida_source=entity) 创作者）在博客中首次明确命名了这一实践，并提出核心理念：“每当发现 Agent 出现错误时，应投入时间设计系统性解决方案，以确保 Agent 永久避免重蹈覆辙。”
+ **OpenAI** 随后发布了题为《Harness engineering: leveraging Codex in an agent-first world》的详细报告，记录了三名工程师历时 5 个月构建百万行代码产品的完整过程。
+ **Ethan Mollick** 围绕“Models, Apps, and Harnesses”三个核心概念重构了其 AI 指南框架，极大地推动了该术语的规范化进程。
+ **Martin Fowler** 发表深度分析文章，将 OpenAI 的 Harness 实践系统分类为三个领域：上下文工程（Context Engineering）、架构约束（Architecture Constraints）与垃圾回收（Garbage Collection）。

# **AI工程范式的三次演化：Prompt、Context与Harness Engineering**
:::color3
**简介：**近期“[Harness Engineering](https://zhida.zhihu.com/search?content_id=271317054&content_type=Article&match_order=1&q=Harness+Engineering&zhida_source=entity)”概念逐渐兴起。结合实际工程经验，本文探讨了AI工程范式从 Prompt Engineering 到 Context Engineering，再到 Harness Engineering 的演进历程。这三者并非替代关系，而是同一套AI工程系统的三个递进层次：Prompt 决定任务下发方式，Context 决定模型关键时刻的视野，而 Harness 决定模型执行任务的运行机制。在 Coding Agent 等复杂场景中，构建完善的系统运行环境（Harness）已成为保障模型稳定交付的核心关键。

:::

:::color5
**<font style="color:#601bde;">1. 核心探讨问题与核心结论</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

本文旨在解答以下三个核心问题：

1. `Prompt Engineering`、`Context Engineering` 与 `Harness Engineering` 各自解决的核心痛点是什么？
2. 为什么在 `Coding Agent` 场景中，Harness Engineering 的重要性日益凸显？
3. 当 Agent 表现未达预期时，应当采取何种优化策略？

**核心结论：**  
当系统目标从“单轮问答正确”转变为“稳定执行复杂工作流”时，工程重心必然向外围转移。仅依靠优化提示词（Prompt）或补充上下文（Context）已不足以支撑复杂任务，必须着手解决运行环境、反馈回路、权限边界及记录系统等深层工程问题。在 `Coding Agent` 场景中，多数失败并非源于模型能力不足，而是缺乏完善的系统架构与运行规范。

## Prompt Engineering：明确任务目标与输入表达
:::color3
**简介：**Prompt Engineering 是大语言模型交互的基础阶段，核心在于通过优化输入表达，提升模型对人类意图的理解准确度，但其在处理复杂多步任务和外部环境交互时存在明显局限。

:::

:::color5
**<font style="color:#601bde;">1. 核心应用场景与交互模式</font>**

:::

多数用户与大语言模型（如 ChatGPT、DeepSeek 或豆包）的初次交互均始于 Prompt。通过在输入框中输入指令（例如：“中国的首都是哪里？”），模型输出对应结果（“北京”）。这种基础交互模式催生了大量 ChatBot 产品，将模型能力封装为高效的知识库或搜索引擎。在此阶段，AI 的核心任务是问答，即如何更精准地输出用户期望的答案。

:::color5
**<font style="color:#601bde;">2. 提示词优化的核心方法</font>**

:::

该阶段的工程实践主要集中于提示词技巧的研究，旨在让模型更准确地理解用户意图。常见方法包括：

1. **角色与背景设定：** 格式化定义模型的身份、背景与行为准则。
2. **样本示例（One-shot/Few-shot）：** 提供具体示例以规范模型输出。
3. **思维链（Chain of Thought）：** 引导模型进行分步逻辑推理。
4. **ReAct 框架：** 结合推理与行动观测（此阶段已初步具备 Agent 的雏形）。

严格而言，[Prompt Engineering](https://zhida.zhihu.com/search?content_id=271317054&content_type=Article&match_order=1&q=Prompt+Engineering&zhida_source=entity) 不仅涉及指令编写，还涵盖了系统的测试、评估与迭代，其核心解决的是“输入表达”问题。

:::color5
**<font style="color:#601bde;">3. Prompt Engineering 的局限性</font>**

:::

尽管 Prompt Engineering 效果显著，但其能力边界十分明确：

+ 无法凭空为模型注入私域知识。
+ 无法使模型感知外部世界的实时动态。
+ 无法原生解决跨轮对话的持续记忆问题。
+ 无法替代权限控制、执行环境与错误恢复等系统级机制。

在实际应用中，我们对 LLM 的期望已超越了高级数据库查询，而是希望其能作为 Agent 执行多步复杂任务。

## Context Engineering：构建关键时刻的上下文视野
:::color3
**简介：**当任务由简单的问答升级为复杂执行时，工程重心转移至 Context Engineering。其核心在于如何高效组织和编排进入模型上下文窗口的信息，包括私有知识检索（RAG）、外部工具调用以及长短期记忆管理

:::

:::color5
**<font style="color:#601bde;">1. 上下文信息的组织与重构</font>**

:::

模型依赖上下文窗口进行推理，Prompt 仅是其中一部分。凡是进入模型视野并影响其决策的信息，均属于上下文范畴，例如：提示词、用户输入、工具定义及返回结果、历史对话、检索知识片段、长短期记忆以及当前任务状态。如何有效组织而非机械填充这些信息，是 Context Engineering 的核心课题。

:::color5
**<font style="color:#601bde;">2. RAG：私有知识库的检索与增强</font>**

:::

面对庞大的私域知识、产品文档或内部规范，无法将其一次性输入模型。`RAG`（检索增强生成）的价值在于：通过语义检索提取最相关的片段输入模型。  
尽管 RAG 技术在发展过程中面临过争议（如模型上下文窗口扩大带来的“RAG 无用论”），但在企业实践中：

+ 在企业知识问答、流程文档检索等场景，`RAG` 依然不可或缺。
+ 在代码仓库导航、局部文件定位等强结构化场景中，采用 `Grep`、`Glob`、`Read` 等直接操作文件系统的方式，往往比向量检索更为高效精准。  
不同任务场景需匹配差异化的上下文增强方式。

:::color5
**<font style="color:#601bde;">3. Tools：外部世界交互与行动能力</font>**

:::

缺乏工具的 LLM 犹如“缸中之脑”，具备推理能力却无法感知现实或执行动作。为模型接入工具是解决此问题的关键：

+ 接入时间工具以获取当前时间。
+ 接入搜索引擎或 API 以获取现实世界信息。
+ 接入代码与系统工具以执行文件修改、命令运行或日志查询。

工具调用技术经历了从正则匹配、`Function Calling` 到 `MCP` 协议层抽象的演进。随着工具数量的增加，为降低上下文占用与模型选择成本，当前系统多采用按需加载策略，将工具封装为 `Skills`。

:::color5
**<font style="color:#601bde;">4. Memory：持续状态与历史记忆管理</font>**

:::

LLM 缺乏原生状态保持能力。最基础的解决方案是将历史对话拼接至上下文，但这极易耗尽窗口容量。因此，必须进行精细化的信息编排：

+ 甄别需保留的核心历史信息。
+ 对冗余信息进行压缩、摘要或外置存储。  
短期记忆用于维持连续对话，长期记忆则负责管理跨任务偏好、固定约束与历史决策。

:::color5
**<font style="color:#601bde;">5. 仅依赖上下文的局限性</font>**

:::

Context Engineering 解决了“模型能看到什么”的问题，但无法处理以下系统级挑战：

+ 高风险工具的误用防范（如 Agent 意外切断自身网络）。
+ 代码修改后的自动化验证机制。
+ 任务失败后的重试与回滚策略。
+ 任务执行中的合理汇报时机控制。
+ 长周期任务中可追溯的过程记录。  
这些问题的涌现，迫使我们将视角从上下文扩展至整个运行系统，即 Harness Engineering。

## Harness Engineering：构建可运行、可纠错、可追溯的系统环境
:::color3
**简介：**Harness Engineering 致力于将模型置于一个具备工程闭环的环境中。如同为新入职的资深工程师提供完善的工作条件，Harness 提供了明确的目标边界、必要的隐性知识、适度的工具集、可观测的反馈回路以及渐进式的记录系统，从而保障 Agent 的稳定交付。

:::

:::color5
**<font style="color:#601bde;">1. 确定任务目标与边界约束</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

Agent 失控往往源于系统缺乏清晰的“完成条件”与“禁止动作”。在代码任务中，必须明确告知 Agent：

+ 任务完成的具体标准。
+ 严禁触碰的目录、分支或环境。
+ 失败后的处理策略（重试、回退或挂起确认）。
+ 强制汇报的节点。  
无约束的多步执行极易导致 Agent 过度行动，明确的边界设定直接决定了产出质量。

:::color5
**<font style="color:#601bde;">2. 暴露隐性知识与前置规则</font>**

:::

`Coding Agent` 执行偏差常因缺乏团队“默认规则”所致。例如“上线新功能”隐含了诸多前置约束（埋点指标、历史兼容性、UI 文案同步、发布链路等）。人类沟通中富含高密度的多模态信息，若不向模型清晰呈现这些细节，Agent 极易产生幻觉。因此，需向 Agent 补充“新人入职首周需掌握的业务背景与规范”。

:::color5
**<font style="color:#601bde;">3. 提供足够但不过载的工具集</font>**

:::

工具泛滥会增加模型的选择成本并挤占上下文。合理的策略是使工具可发现且按需加载。优秀的 `Coding Agent`（如 Claude Code、pi-mono）通常优先提供一组高频通用能力（如 `Read`、`Write`、`Grep`、`Glob`、`Bash`），由 `Bash` 提供兜底支持，其余能力交由项目专属 CLI 或脚本处理。这基于一个核心信任：“智能的 Agent 能够自主寻找并使用合适的工具”。

:::color5
**<font style="color:#601bde;">4. 提供可观测的反馈回路</font>**

:::

缺乏反馈，Agent 无法进行自我纠错。软件开发中的典型反馈源包括：测试结果、`Lint` 与类型检查（常结合 LSP）、结构化日志、真实运行输出以及调试器回传信息。若系统未暴露这些观测信号，单纯优化 Prompt 毫无意义。依赖真实世界反馈的岗位（如需硬件调试的嵌入式开发）具有更高的不可替代性。

:::color5
**<font style="color:#601bde;">5. 提供渐进式披露的记录系统</font>**

:::

长程任务需要大量记录，但上下文窗口极其宝贵。优秀的记录系统应提供信息索引，将细节沉淀至可维护的位置：

+ `AGENTS.md`：负责声明规则、入口与知识分布地图。
+ `docs/`：负责沉淀领域文档、流程说明与排障记录。
+ `git`：负责保存代码变更与提交语义，作为低检索成本的外部记忆。  
在复杂工程（如语音 Agent `vixio`）中，强制 Agent 编写并维护设计文档，并在后续任务中引用，是维持项目长期记忆稳定性的关键 Harness 实践。

# **为什么需要 Harness Engineering**
:::color3
**简介：**业界实践与量化实验表明，当前 AI Agent 开发的瓶颈已不再是模型自身的智能水平，而是缺乏完善的基础设施与反馈机制。同时，Agent 在实际运行中暴露出多种典型的失败模式，且上下文窗口的利用率存在明显的效能边界。

:::

:::color5
**<font style="color:#601bde;">1. 模型能力已非核心瓶颈</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

“基础设施而非模型智能是当前最大瓶颈”这一判断已得到充分的量化验证：

+ [Can.ac 实验](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Can.ac+%E5%AE%9E%E9%AA%8C&zhida_source=entity)：在未修改任何模型权重的前提下，仅通过优化 Harness 的工具格式（如编辑接口），便在 16 个模型上显著提升了编码基准分数。其中，Grok Code Fast 1 的表现最为突出，其准确率从 6.7% 大幅跃升至 68.3%。
+ [LangChain 实验](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=LangChain%E5%AE%9E%E9%AA%8C&zhida_source=entity)：仅依赖 Harness 层面的改进，同一模型在 Terminal Bench 2.0 上的得分提升了 13.7 分，排名从第 30 位跃升至第 5 位。

上述结果充分表明：在投入精力进行模型选型之前，优先优化 Harness 设计能够带来更高的投资回报率。OpenAI 团队亦明确指出：**制约开发效率的关键并非 Agent 编写代码的能力，而是围绕其构建的系统结构、工具链及反馈机制相对滞后**。五个独立研发团队均得出了高度一致的结论：基础设施的完善程度才是决定性因素。

:::color5
**<font style="color:#601bde;">2. Agent 的典型失败模式</font>**

:::

Anthropic 团队在研发长时间运行的 Agent 过程中，总结了以下四类典型的失败模式：

+ **失败模式 1：试图一步到位（One-shotting）。** Agent 往往倾向于在一个周期内完成所有任务。这导致在实现中途耗尽上下文窗口，当启动下一个会话时，Agent 面对的是缺乏文档的半成品代码，不得不耗费大量算力去推测历史进度并尝试恢复工作状态。
+ **失败模式 2：过早宣布胜利。** 在项目推进至后期时，Agent 一旦观察到部分功能已实现，便可能直接判定整体任务已完成，完全忽略剩余的大量未实现功能。
+ **失败模式 3：过早标记功能完成。** 若缺乏明确的验证提示，Agent 在完成代码编写后会立即将其标记为“完成”，而忽略了端到端测试。仅通过单元测试或简单的 curl 命令，并不能证明功能在实际环境中真实可用。
+ **失败模式 4：环境启动困难。** 每次启动新会话时，Agent 需消耗大量 token 来解析如何运行应用程序或启动开发服务器，导致实际用于核心开发的时间被严重压缩。

:::color5
**<font style="color:#601bde;">3. 上下文窗口利用率的效能区间</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919451359-c98a213c-7c6d-4b41-9b3a-e9a8daf0814b.png)

专家 Dex [Horthy](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Horthy&zhida_source=entity) 提出了一项极具指导意义的经验法则：**上下文填充度越高，LLM 的输出质量往往越差**。以具备 168K token 上下文窗口的模型为例，当使用率达到约 40% 时，模型性能便开始呈现下降趋势：

+ **智能区（Smart Zone，前约 40%）**：模型能够进行聚焦且准确的推理。此时 Agent 掌握的是高度相关且经过精炼的信息。
+ **迟钝区（Dumb Zone，超过约 40%）**：模型易出现幻觉、逻辑循环、工具调用格式错误以及生成低质量代码。过量输入 token 反而会损害整体性能。

简而言之，向 Agent 盲目输入大量 MCP 工具、冗长文档及历史对话记录，并不能提升其智能水平，反而会导致其处理能力显著下降。

# **Harness Engineering 的四大支柱**
:::color3
**简介：**综合 OpenAI、Anthropic、[Carlini](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Carlini&zhida_source=entity)（C 编译器项目）、[Huntley](https://zhida.zhihu.com/search?content_id=271147250&content_type=Article&match_order=1&q=Huntley&zhida_source=entity) 及 Horthy 等五个独立团队的工程实践，业界已逐渐收敛出四种核心模式，这构成了 Harness Engineering 的四大支柱。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919466105-01d5b184-6795-435c-b45e-54db2ff86583.png)

:::color5
**<font style="color:#601bde;">1. 支柱一：上下文架构（Context Architecture）</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**核心原则**：Agent 应当且仅应当获取当前任务所需的精确上下文信息。

各团队均独立发现，将所有指令集中于单一文件内缺乏可扩展性。业界通用的解决方案是**分层上下文与渐进式披露机制**：

+ **OpenAI** 采用 `AGENTS.md` 作为动态反馈循环文件，在 Agent 遭遇失败时进行实时更新。
+ **Anthropic** 依赖详尽的 README 文件以及在每次会话中高频更新的进度文件。
+ **Horthy** 提出并倡导“高频有意识压缩”（Frequent Intentional Compaction）策略。
+ **Vasilopoulos（2026 论文）** 将上下文系统化为三个层级：热记忆（Hot Memory）、领域专家（Domain Experts）与冷记忆知识库（Cold-Memory Knowledge）。

**实践建议——三层上下文体系**：

| 层级 | 加载时机 | 内容示例 | 上下文占用 |
| :--- | :--- | :--- | :--- |
| Tier 1：会话常驻 | 每次会话自动加载 | AGENTS.md / CLAUDE.md，项目结构概览 | 最小 |
| Tier 2：按需加载 | 特定子 Agent 或技能被调用时 | 专业化 Agent 的上下文、领域知识 | 中等 |
| Tier 3：持久化知识库 | Agent 主动查询时 | 研究文档、规格说明、历史会话 | 按需 |


:::color5
**<font style="color:#601bde;">2. 支柱二：Agent 专业化（Agent Specialization）</font>**

:::

**核心原则**：专注于特定垂直领域且权限受限的专业 Agent，其表现优于拥有全局权限的通用型 Agent。

+ **Carlini**（Anthropic C 编译器项目）将 Agent 体系专业化为四类角色：编译器核心、代码去重、性能优化与文档生成。
+ **Vasilopoulos** 在其架构中部署了 19 个具备特定领域知识的 Agent。
+ **Huntley** 通过引入子 Agent 机制，有效保持了主 Agent 上下文的纯净度。

专业化不仅是一种组织架构层面的优化，其本质更是一种高效的上下文管理策略。由于每个专家级 Agent 携带的无关信息更少，从而确保其始终运行在高效的“智能区（Smart Zone）”内。

**实践中的角色分工**：

| Agent 角色 | 职责范围 | 工具权限 |
| :--- | :--- | :--- |
| 研究 Agent | 探索代码库、分析实现细节 | 只读（Read, Grep, Glob） |
| 规划 Agent | 将需求分解为结构化任务 | 只读，无写入权限 |
| 执行 Agent | 实现单个具体任务 | 限定范围的读写权限 |
| 审查 Agent | 审计完成的工作，标记问题 | 只读 + 标记权限 |
| 调试 Agent | 修复审查发现的问题 | 限定范围的修复权限 |
| 清理 Agent | 对抗熵积累，清理低质量代码 | 读写权限 |


:::color5
**<font style="color:#601bde;">3. 支柱三：持久化记忆（Persistent Memory）</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**核心原则**：项目进度应持久化存储于文件系统中，而非依赖于易失的上下文窗口。每次启动新的 Agent 会话时，系统应从零状态开始，通过读取文件系统中的制品来重建准确的上下文。

Anthropic 在解决此问题上的方案具有高度的示范意义：

+ **初始化 Agent**：在首次会话中，使用专属的 prompt 指导模型搭建初始环境，包括生成 `init.sh` 脚本、`claude-progress.txt` 进度文件以及执行初始的 git 提交。
+ **编码 Agent**：在后续的每次会话中，强制要求模型在取得增量进展的同时，必须输出结构化的状态更新。

每个编码 Agent 的标准会话启动流程如下：

1. 运行 `pwd` 命令确认当前工作目录。
2. 读取 `git log` 与进度文件，同步近期的工作状态。
3. 解析 feature list 文件，提取并锁定最高优先级的未完成功能。
4. 启动开发服务器，并执行基础的端到端测试。
5. 在确认基础环境运行正常后，正式切入新功能的开发流程。

**关键发现**：在追踪 feature 状态时，**采用 JSON 格式远比 Markdown 更为可靠**，原因在于 Agent 极少会发生不当修改或意外覆盖结构化数据的情况。

:::color5
**<font style="color:#601bde;">4. 支柱四：结构化执行（Structured Execution）</font>**

:::

**核心原则**：严格分离“思考”与“执行”阶段。研究与规划必须在受控环境中完成，后续的执行动作需严格遵循已验证的计划；最终的验证环节则交由自动化反馈机制（如测试用例、Linter、CI 流水线）及人工审查共同完成。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919497036-44765800-6d76-493b-b735-d1cddaf41b82.png)

所有先进团队均刻意施加了严密的执行序列：**理解 → 规划 → 执行 → 验证**。

+ **OpenAI** 采用声明式 prompt 结合反馈回路。对于轻量级变更，采用简易计划；针对复杂任务，则生成包含进度追踪与决策日志的详尽执行计划，并将其检入代码仓库。
+ **Huntley** 在架构上实现了规划模式与构建模式的物理隔离。
+ **Horthy** 提出的 Research-Plan-Implement 工作流，其核心正是围绕上下文的精细化管理而设计。

**人工检查点的核心价值**：审查计划的效率远高于审查代码。若规格定义准确，代码实现自然具备高可靠性；若规格存在偏差，人工介入可在系统生成数百行无效代码之前及时纠偏，大幅降低试错成本。

# **先进团队的实战案例**
:::color3
**简介：**本部分详细拆解了 OpenAI、Anthropic 及 Stripe 等顶尖团队在 Harness Engineering 领域的实战案例，涵盖百万行代码生成、复杂 C 编译器构建、长时间运行 Agent 架构以及无人值守的并行化 PR 处理系统，展示了理论在极端工程环境下的应用效果。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919687119-a017440b-0c66-40d3-95e9-12794c7ca7a2.png)

:::color5
**<font style="color:#601bde;">1. OpenAI：百万行代码的零手写实验</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**实验概况**：

| 指标 | 数值 |
| :--- | :--- |
| 团队规模 | 3 名工程师 |
| 持续时间 | 5 个月（2025.8 起） |
| 代码规模 | 约 100 万行 |
| 手写代码 | 0 行（设计约束） |
| 合并 PR 数 | 约 1,500 个 |
| 日均 PR/人 | 3.5 个 |
| 效率提升 | 约 10 倍 |


**五大 Harness 原则**：

+ **原则 1：设计环境，而非编写代码。** 工程师的核心职责转变为向 Agent 提供高效的运行环境。当 Agent 陷入停滞时，策略并非要求其“增加算力”，而是诊断系统“缺失何种能力”，并引导 Agent 自主构建该能力。
+ **原则 2：机械化地执行架构约束。** 团队为各个领域严格定义了依赖流向（Types → Config → Repo → Service → Runtime → UI），并部署自定义 Linter 与结构化测试进行自动化违规检测。仅靠文档记录是无效的；若无法实现机械化的强制执行，Agent 必然会偏离架构规范。
+ **原则 3：将代码仓库作为唯一事实源。** 散落于 Slack 讨论或 Google Docs 中的知识对 Agent 而言毫无意义。所有团队知识必须作为受版本控制的制品，统一存放于代码仓库中。
+ **原则 4：将可观测性连接到 Agent。** 团队将 Chrome DevTools 深度集成至运行时环境，赋予 Agent 捕获 DOM 快照与屏幕截图的能力。通过开放查询日志与指标的权限，诸如“将启动时间优化至 800ms 以下”的模糊需求，成功转化为可量化、可执行的具体目标。
+ **原则 5：对抗熵增。** 项目初期，团队每周五需耗费 20% 的工时手动清理“AI Slop”（低质量生成物）。后期该流程被重构为由 Codex 驱动的后台自动化任务——清理机制的吞吐量能够随代码生成量的增长而弹性扩展。

**自定义 Linter 的巧妙设计**：当 Agent 违反架构约束时，系统抛出的错误消息不仅用于标记违规，**更直接提供修复方案**。工具在拦截错误的同时，完成了对 Agent 的“实时教学”。

:::color5
**<font style="color:#601bde;">2. Anthropic：16 个 Agent 构建 C 编译器</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

Carlini 领导的 C 编译器项目，被视为当前针对 Agent 自主开发能力最严苛的压力测试之一。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773919703783-4d0d1b63-f675-4dbe-854e-671a53cff8a6.png)

**项目数据**：

| 指标 | 数值 |
| :--- | :--- |
| 持续时间 | 约 2 周 |
| 并行 Agent 数 | 16 个 Claude Opus 4.6 实例 |
| Claude Code 会话数 | 约 2,000 |
| 产出 Rust 代码量 | 100,000 行 |
| GCC torture test 通过率 | 99% |
| 可编译的真实项目 |  |


## Harness实践案例：Debug Agent 的工程演进
:::color3
**简介：**通过一个 Debug Agent 的实际开发案例，展示了在解决代码崩溃问题时，单纯依赖 Prompt 和 RAG 检索的局限性，以及引入 Harness Engineering（构建标准排查工作流）后带来的显著效果提升。

:::

:::color5
**<font style="color:#601bde;">1. 第一版：基于 Prompt 与基础 Context 的尝试</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

初始方案仅提供任务指令（“解决这个崩溃问题”）以及问题描述、崩溃日志和代码仓库。尽管信息看似充足，但实际效果极差。Agent 陷入低效搜索，定位准确率极度依赖运气（例如误判内存空指针并陷入死循环）。此时若仅从 `Prompt Engineering` 角度反思，极易得出“提示词不够详细”的错误结论。

:::color5
**<font style="color:#601bde;">2. 误判与试错：引入代码 RAG</font>**

:::

后续尝试通过代码语义检索（RAG）寻找崩溃相关代码，但召回率极低。调试任务的关键线索通常并非自然语言的语义相似，而是崩溃堆栈符号、日志关键字、历史术语或调用链变化。代码语义检索在此场景下并非最有效的切入点。

:::color5
**<font style="color:#601bde;">3. 破局关键：构建崩溃分析的 Harness 支架</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

最终的显著改善源于放弃堆砌 Prompt，转而构建贴合工程经验的运行支架。为 Agent 注入具体的“崩溃分析技能”工作流：

+ 规定特定崩溃类型的首选搜索关键字。
+ 指定需优先调用的本地分析工具（并提前配置好运行环境）。
+ 提供历史相似问题的分析参考。
+ 遇到未知术语时，强制通过 `git` 记录反查代码段。  
这一改造使 Agent 的行为模式从“盲目游走”转变为“资深工程师的结构化排障”，大幅提升了执行效率与准确率。

:::color5
**<font style="color:#601bde;">4. 三层工程范式在案例中的作用映射</font>**

:::

回顾该案例，三层架构的职责清晰可见：

+ `Prompt`：定义核心目标（“解决崩溃问题”）。
+ `Context`：提供执行材料（日志、代码仓库、历史案例、[claude code sdk](https://zhida.zhihu.com/search?content_id=271317054&content_type=Article&match_order=1&q=claude+code+sdk&zhida_source=entity) 等）。
+ `Harness`：固化排查流程与运行环境，指导 Agent 合理使用工具与记忆系统持续逼近真相。

# **总结：Agent 时代，工程重心向 Harness 转移**
:::color3
**简介：**Prompt、Context 与 Harness 共同构成了现代 AI 工程的完整体系。随着模型能力的提升与任务复杂度的增加，人类工程师的角色正从“微观干预者”转变为“宏观舞台搭建者”。

:::

:::color5
**<font style="color:#601bde;">1. 三层架构的协同与演进</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

`Prompt Engineering` 解决任务表达，`Context Engineering` 解决信息供给，`Harness Engineering` 解决真实环境中的稳定执行。三者呈逐层向外扩展的包含关系。任务越贴近真实生产环境，Harness 的决定性作用越强。

:::color5
**<font style="color:#601bde;">2. 人机协作模式的转变</font>**

:::

随着底层模型能力的持续跃升，AI 亟需的是一个“自由发挥的舞台”。人类工程师的核心职责应转变为协助搭建完善的系统环境（Harness），而非过度干预其微观行为。若在使用顶级模型时仍未获得理想的 `vibe coding` 体验，问题往往不在于模型智力，而在于尚未为其提供足以释放其潜能的工程运行环境。

