# Codex的Agent Loop机制详解

<!-- source: yuque://zhongxian-iiot9/hlyypb/sx0dhn5fpgqgaath -->

:::success
**简介：**本文主要探讨基于 Rust 构建并在 GitHub 开源的 **<font style="color:#74B602;">Codex 项目</font>**，重点解析其核心的 **<font style="color:#74B602;">Agent Loop 机制</font>**与上下文管理逻辑。  
**Codex项目地址：**[https://github.com/openai/codex](https://link.zhihu.com/?target=https%3A//github.com/openai/codex)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775818521437-6533fb86-7b86-410c-919b-482ff15d2727.png)

# **Codex 的 Agent Loop**
:::color3
**简介：** Codex 中 **<font style="color:#ED740C;">Agent 的双层循环机制</font>**，包括外层操作分发与内层核心的 Agent Loop 运转逻辑。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775818907385-ccb51e3c-b725-4a51-b63c-93e8f13f1878.png)

:::color5
**<font style="color:#601bde;">1. 循环机制概述</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">Codex 的架构，Agent 的核心在于通过循环机制收集上下文信息并调用相关工具。该系统设计了双层循环结构：</font>**

+ **外层循环**：主要负责消费各类操作指令（Op），例如中断（Interrupt）、压缩（Compact）、审查（Review）、用户输入响应（UserInputAnswer）以及权限请求响应（RequestPermissionsResponse）等，并据此决定是否将任务分发至内层循环。
+ **内层循环**：即单轮对话（Turn），通常被理解为标准的 Agent Loop。其核心业务流程包括：整理上下文信息、向大语言模型发起请求、执行工具调用、将工具执行结果回写至历史记录，并最终评估是否需要继续调用模型。该轮次的终止条件为 `!needs_follow_up`（即满足以下三个条件：工具调用为空、无工具执行结果需返回给模型、且用户输入为空）。



# **Codex 的上下文**
:::color3
**简介：**本节详细解析 Codex **<font style="color:#ED740C;">上下文的构建过程</font>**，包括基础指令、工具定义以及输入消息的组装逻辑。

:::

:::color5
**<font style="color:#601bde;">1. 上下文入口与架构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">整个上下文构建的核心入口为函数 </font>**`**<font style="color:#74B602;">fn build_responses_request()</font>**`**<font style="color:#74B602;">。</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775817969327-55cfc031-fb7b-48b7-a7ef-52326bd213ee.png)

:::color5
**<font style="color:#601bde;">2. 基础指令 (Base instructions)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">基础指令构成了 Codex 运行的底层逻辑，默认指令文件位于 </font>**`**<font style="color:#74B602;">codex/prompt.md</font>**`**<font style="color:#74B602;">。</font>**

以下为该指令的中文翻译参考：

```markdown
你是一个在 Codex CLI 中运行的编程代理，这是一个基于终端的编码助手。Codex CLI 是由 OpenAI 主导的开源项目。你需要做到精确、安全且有帮助。

你的能力：

- 接收用户提示以及由系统提供的其他上下文信息，例如工作区中的文件。
- 通过流式输出思考与回复、制定和更新计划，与用户进行沟通。
- 发出函数调用以执行终端命令和应用补丁。根据当前运行配置，你可以请求用户批准后再执行这些操作。更多内容请参见“沙箱与审批”部分。

在此上下文中，Codex 指的是开源的代理式编码接口（而不是 OpenAI 早期的 Codex 语言模型）。

# 工作方式

## 个性

你的默认性格与语气是简洁、直接、友好。你高效沟通，让用户始终清楚当前正在进行的操作，而不会提供不必要的细节。你始终优先提供可执行的指导，清楚说明假设、环境前提和下一步操作。除非明确要求，否则避免冗长解释。

# AGENTS.md 规范

- 仓库中通常包含 AGENTS.md 文件，这些文件可以出现在任意目录。
- 这些文件用于人类向你（代理）提供在该容器中工作的说明或提示。
- 示例内容包括：编码规范、代码结构说明、运行或测试代码的方式等。
- AGENTS.md 文件的规则：
  - 文件的作用范围是其所在目录及其所有子目录。
  - 对于你最终修改的每个文件，必须遵循其作用范围内的 AGENTS.md 指令。
  - 关于代码风格、结构、命名等的指令，仅适用于该范围内的代码，除非另有说明。
  - 如果存在冲突，更深层目录中的 AGENTS.md 优先。
  - 系统 / 开发者 / 用户的直接指令优先于 AGENTS.md。
- 根目录以及当前工作目录到根路径之间的 AGENTS.md 已包含在开发者消息中，无需重复读取。若在子目录或外部目录工作，应检查是否有适用的 AGENTS.md。

## 响应性

### 前置说明（Preamble）

在调用工具前，需发送简短说明，解释你接下来要做的事情。原则如下：

- **逻辑分组操作**：将相关操作合并说明
- **保持简洁**：1-2句话，8–12个词
- **承接上下文**：说明当前进展与下一步
- **语气轻松友好**
- **例外**：简单读取操作可省略

示例：

- “我已经浏览完仓库，现在检查 API 路由。”
- “接下来更新配置并同步测试。”
- “准备搭建 CLI 命令结构。”

## 计划（Planning）

你可以使用 `update_plan` 工具来制定和跟踪步骤。

好的计划应：

- 拆分为清晰、有逻辑顺序的步骤
- 易于验证进度
- 避免无意义步骤

适用场景：

- 任务复杂或多阶段
- 有依赖顺序
- 存在不确定性
- 用户要求使用计划

不要在简单任务中使用计划。

## 执行任务

你必须持续工作直到问题完全解决。

要求：

- 不猜测、不编造答案
- 使用 `apply_patch` 修改文件
- 优先解决根本问题
- 保持代码简洁
- 不修改无关代码
- 遵循现有代码风格
- 不添加版权声明
- 不随意添加注释
- 不使用单字母变量

## 验证工作

- 可运行测试时应验证
- 从小范围测试开始
- 不修复无关错误
- 不引入格式化工具（除非已有）

## 主动性与精确性

- 新项目：可以更有创造性
- 现有项目：精准修改，不越界

## 进度更新

对于较长任务，应定期简短更新：

- 8–10个词
- 描述当前进展与下一步

## 最终输出

你的回复应像一个高效的团队成员：

- 简洁、自然
- 必要时使用结构化格式
- 不重复大段代码
- 不要求用户保存文件

### 格式规范

**标题**
- 使用 `**标题**`
- 简短清晰

**列表**
- 使用 `- `
- 每条尽量一行

**代码**
- 使用反引号包裹

**文件路径**
- 使用可点击路径
- 示例：`src/app.ts:42`

**语气**
- 合作式、自然
- 主动语态

## 工具使用

### Shell

- 优先使用 `rg` 搜索

### update_plan

- 每步 1 句话
- 标注状态：pending / in_progress / completed
```

:::color5
**<font style="color:#601bde;">3. 工具定义 (Tools Defintion)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">系统可用的工具列表存放于 </font>**`**<font style="color:#74B602;">Prompt.tools</font>**`**<font style="color:#74B602;"> 中，主要涵盖以下四类：</font>**

+ 当前会话中可见的内置工具（Built-in Tools）。
+ 满足特定条件方可启用的工具（Conditional Tools）。
+ 模型上下文协议工具（MCP Tools）。
+ 动态工具（Dynamic Tools）。注：若部分动态工具被标记为 `defer_loading`，则在当前轮次的 Prompt 中会被预先过滤，不会直接暴露给模型。

:::color5
**<font style="color:#601bde;">4. 输入信息 (Input)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">输入信息主要由对话历史与上下文消息构成，通过 </font>**`**<font style="color:#74B602;">build_initial_context()</font>**`**<font style="color:#74B602;"> 函数进行组装。具体包含以下模块：</font>**

**<font style="color:#117CEE;background-color:#D9EAFC;">4.1 Developer 消息</font>**

| **消息类型** | **说明** | **示例** |
| :--- | :--- | :--- |
| Model switch message | 当模型发生切换时，系统会注入此段提示消息。 | ```Markdown<br>The user was previously using a different model. Please continue the conversation according to the following instructions:<br>``` |
| 沙箱 / 审批 / 审查 / 执行策略说明 | 涉及 sandbox、approval、reviewer、exec policy 的开发者说明，将拼装成结构化段落。 | ```Markdown<br>Filesystem sandboxing defines which files can be read or written... (详见原文代码块)<br>``` |
| Developer instructions | 配置化内容，通常来源于 `AGENTS.md` 文件。 |  |
| Memory tool Message | 提供给模型阅读的 Memory 工具使用说明，源自 `memory_summary.md`。 | - 你可以使用 memory folder 里的历史信息   - 只能读，不能改 memory   - 什么时候该查 memory，什么时候可以跳过   - 怎么做一个轻量级 quick memory pass   - 什么时候要重新验证 memory 里的事实   - 如果用了 memory，最终回复末尾必须附一个引用 |
| Realtime 状态说明 | 用于向模型说明当前是否处于与用户的实时对话状态。 | ```Markdown<br>....<br>``` |
| 模型指令与个性化设置 | `model_instructions` 为整体模型基础说明；`personality_message` 为其中针对语气风格的专属说明段落。 |  |
| 可访问连接器 / 应用摘要 | 当前允许访问的 connectors / apps 的摘要信息及使用规则。 | ```Markdown<br>## Skills<br>A skill is a set of local instructions... (详见原文代码块)<br>``` |
| Personality | 针对模型回复语气的具体说明。 |  |
| Loaded plugins 摘要 | 已加载插件的摘要信息。 |  |
| Git commit attribution 提示 | 关于设置 Co-Author 的规范提示。 | ```Markdown<br>When you write or edit a git commit message, ensure the message ends with this trailer exactly once:<br>Co-authored-by: Codex<br>...<br>``` |


消息排列的代码结构示例：

```plain
ResponseItem::Message {
      role: "developer",
      content: vec![
          InputText { text: "<model_switch>...</model_switch>" },
          InputText { text: "<permissions instructions>...</permissions instructions>" },
          InputText { text: "<skills_instructions>...</skills_instructions>" },
      ],
  }
```

**4.2 User 消息**

| **消息类型** | **说明** | **示例** |
| :--- | :--- | :--- |
| user_instructions | 用户提供的配置化自定义指令。 | 实际上对应 `AGENTS.override.md` 或 `AGENTS.md` 的内容。 |
| environment and subagents | 环境信息与子 Agent 列表。 | ```XML<br>/repo<br>bash<br>2026-02-26<br>America/Los_Angeles<br>- agent-1: atlas<br>- agent-2<br>``` |


**4.3 消息历史**

上下文中的消息历史按时间先后顺序（由旧至新）排列，包含以下内容：

+ 用户消息（User Messages）
+ 助手消息（Assistant Messages）
+ 函数/工具调用记录（Function/Tool Call）
+ 函数/工具输出结果（Function/Tool Output）

**4.4 用户最新输入**

用户的最新输入内容将固定放置于上下文的末尾。



# **Codex 可用的 Tools**
:::color3
**简介：**本节梳理了 Codex 系统中集成的各类工具，涵盖**<font style="color:#ED740C;">命令执行、代码修改、文件操作、子 Agent 调度</font>**等核心能力。

:::

:::color5
**<font style="color:#601bde;">1. 命令执行工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">包含 </font>**`**<font style="color:#74B602;">exec_command</font>**`**<font style="color:#74B602;"> 与 </font>**`**<font style="color:#74B602;">write_stdin</font>**`**<font style="color:#74B602;">。</font>**

**exec_command 规范：**

+ **必填参数**：`cmd: String`（需要执行的终端命令）。
+ **可选参数**：
    - `workdir: Option<String>`：指定工作目录。
    - `shell: Option<String>`：指定 Shell 路径；若未提供，则使用当前会话的默认 Shell。
    - `tty: bool`：是否开启交互式 TTY。若需后续通过 `write_stdin` 输入内容，通常需设置为 `true`。
    - `yield_time_ms: u64 = 10000`：初次执行后等待输出的时间窗口。
    - `max_output_tokens: Option<usize>`：返回输出结果的截断上限。
    - `sandbox_permissions: SandboxPermissions = use_default`：沙箱策略配置（可选 `use_default`, `require_escalated`, `with_additional_permissions`）。
+ **输出内容**：
    - `output`（最终传递给模型的是经过截断处理的文本）。
    - `wall_time_seconds`（执行耗时）。
    - `exit_code`（退出状态码）。

:::color5
**<font style="color:#601bde;">2. 更新计划工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

工具名称：`update_plan`。  
**<font style="color:#74B602;">用于管理任务计划，每个步骤（step）可标记为 </font>**`**<font style="color:#74B602;">pending</font>**`**<font style="color:#74B602;">（待处理）、</font>**`**<font style="color:#74B602;">in_progress</font>**`**<font style="color:#74B602;">（进行中）或 </font>**`**<font style="color:#74B602;">completed</font>**`**<font style="color:#74B602;">（已完成）。</font>**

**入参示例：**

```plain
{
  “explanation”: "<可选的说明文字>"
  "plan": [
    { "step": "Inspect the code path", "status": "completed" },
    { "step": "Implement the fix", "status": "in_progress" },
    { "step": "Run tests", "status": "pending" }
  ]
}
```

**运行机制**：该工具仅负责向 UI 层发送消息，不会执行其他实质性操作，且计划内容不会被插入到 System Prompt 中。模型之所以能感知进度，是因为其先前的 `update_plan` 调用结果被保存在会话状态中，后续轮次读取该状态即可获知当前执行到了第几步。

**UI 展示效果示例：**

```plain
• Updated Plan
  └ I’ll update Grafana call
    error handling...
    ✔ Investigate existing error paths...
    □ Harden Grafana client...
    □ Add tests...
```

+ `completed` -> ✔，呈现为暗色（dim）并带有删除线。
+ `in_progress` -> □，呈现为青色加粗。
+ `pending` -> □，呈现为暗色（dim）。

:::color5
**<font style="color:#601bde;">3. 代码修改工具</font>**

:::

**<font style="color:#74B602;">工具名称：</font>**`**<font style="color:#74B602;">apply_patch</font>**`**<font style="color:#74B602;">。仅包含一个参数 </font>**`**<font style="color:#74B602;">input: String</font>**`**<font style="color:#74B602;">。</font>**

**格式示例：**

```plain
*** Begin Patch
  *** Update File: path/to/file
  @@
  -old
  +new
  *** End Patch
```

:::color5
**<font style="color:#601bde;">4. 图片阅读工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

工具名称：`view_image`。  
用于将本地文件路径转换为 Image URL（底层调用 `image.into_data_url()`）。

:::color5
**<font style="color:#601bde;">5. 文件与目录工具</font>**

:::

**<font style="color:#74B602;">包含 </font>**`**<font style="color:#74B602;">read_file</font>**`**<font style="color:#74B602;">、</font>**`**<font style="color:#74B602;">list_dir</font>**`**<font style="color:#74B602;">、</font>**`**<font style="color:#74B602;">grep_files</font>**`**<font style="color:#74B602;">。</font>**

**read_file**

+ **工具描述**：读取本地文件，提供从 1 开始的行号索引，支持切片及感知缩进的代码块模式。
+ **输入参数**：
    - `file_path: String`：必填，必须为绝对路径。
    - `offset: usize = 1`：选填，起始读取行号（基于 1）。
    - `limit: usize = 2000`：选填，最大返回行数。
    - 可选配置 `mode=indentation` 及 `indentation.*`，用于按代码块结构读取。
+ **输出格式**：按行拼接，格式为 `L<行号>: 内容`。

```plain
L10: fn main() {
L11:     println!("hello");
L12: }
```

+ **截断规则**：单行内容过长（约 500 字符）会被截断且无提示；整体无专门的字符数上限截断，遵循通用工具结果的 10000 Tokens 截断规则。

**list_dir**

+ **输入参数**：
    - `dir_path: String`：必填，目录绝对路径。
    - `offset: usize = 1`：起始目录项索引（基于 1）。
    - `limit: usize = 25`：最大返回项数。
    - `depth: usize = 2`：最大向下遍历层级。
+ **输出示例**：

```plain
Absolute path: /project/src
  main.rs
  utils/
    format.rs
    parse.rs
  vendor@
  misc?
```

（注：`/` 表示目录，`@` 表示符号链接，`?` 表示其他特殊类型）。

**grep_files**

+ **输入参数**：
    - `pattern: String`：必填，正则表达式。
    - `include: Option<String>`：可选，Glob 表达式（如 `*.rs`）。
    - `path: Option<String>`：可选，搜索路径；默认使用当前会话的 CWD。
    - `limit: usize = 100`：最大返回文件数（内部硬上限为 2000）。
+ **输出格式**：每行返回一个匹配的文件路径。

```plain
src/main.rs
  src/lib.rs
  tests/integration.rs
```

（注：系统未提供直接定位关键字所在行号的工具，若有需求需直接调用命令行）。

:::color5
**<font style="color:#601bde;">6. 产物生成工具 (Artifact)</font>**

:::

**<font style="color:#74B602;">工具名称：</font>**`**<font style="color:#74B602;">artifacts</font>**`**<font style="color:#74B602;">。</font>**

+ **输入参数**：`source`（JavaScript 代码），`timeout`（超时时间）。
+ **用途**：运行基于 `@oai/artifact-tool` 的 JS 脚本，用于生成演示文稿、电子表格，导出 pptx/xlsx 文件或进行文件预览。

:::color5
**<font style="color:#601bde;">7. 请求用户输入工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">工具名称：</font>**`**<font style="color:#74B602;">request_user_input</font>**`**<font style="color:#74B602;">。  
</font>**用于向用户发起结构化提问。TUI 会在选项末尾自动追加 "Other"，允许用户自由输入。

**输出示例：**

```plain
{
    "questions": [
      {
        "id": "sandbox_mode",
        "header": "Sandbox",
        "question": "Which sandbox mode should I use?",
        "options": [
          {
            "label": "Workspace (Recommended)",
            "description": "Safer; limits writes outside the workspace."
          },
          {
            "label": "Full access",
            "description": "More permissive; allows broader filesystem changes."
          }
        ]
      }
    ]
}
```

:::color5
**<font style="color:#601bde;">8. 请求权限工具</font>**

:::

工具名称：`request_permissions`。  
**用途**：用于申请额外的文件系统权限（如读写权限）或网络权限，并将获批的权限授权给后续的 Shell 类工具使用。（同一轮对话中的 `exec_command`、`apply_patch` 等调用可直接复用该权限，无需重复弹窗申请）。

:::color5
**<font style="color:#601bde;">9. 子 Agent 工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

包含 `spawn_agent`、`send_message`、`assign_task`、`wait_agent`、`resume_agent`、`close_agent`、`list_agents`，以及批量处理工具 `spawn_agents_on_csv`、`report_agent_job_result`。主要用于多 Agent 协同调度。

:::color5
**<font style="color:#601bde;">10. 搜索与推荐类工具</font>**

:::

包含 `tool_search` 与 `tool_suggest`。

+ `tool_search`：使用 BM25 算法搜索当前会话可用的 App Tools。
+ `tool_suggest`：用于向用户建议安装特定的工具。

:::color5
**<font style="color:#601bde;">11. MCP 管理工具</font>**

:::

包含 `list_mcp_resources`、`read_mcp_resource`、`list_mcp_resource_templates`。用于管理和读取模型上下文协议（MCP）资源。

:::color5
**<font style="color:#601bde;">12. Code-mode 工具</font>**

:::

包含 `exec` 与 `wait`。  
Code-mode 允许编写脚本，并在脚本内部通过 `tools.*` 调用 Codex 工具。`exec` 用于运行原始 JavaScript 代码，`wait` 用于在脚本未结束时阻塞等待或获取增量输出。

:::color5
**<font style="color:#601bde;">13. JS 运行时工具</font>**

:::

包含 `js_repl` 与 `js_repl_reset`。  
`js_repl` 在持久化的 Kernel 中运行 JavaScript 代码；`js_repl_reset` 用于清空并重启当前的 JS 会话。此外，支持在 JS 环境中直接调用 Codex 工具（如 `codex.tool(…)`，`codex.emitImage(…)`）。

:::color5
**<font style="color:#601bde;">14. Response API 工具</font>**

:::

+ **Web Search**：网页搜索功能，透传给 OpenAI Responses API 的内置工具。
+ **Image Generation**：图片生成功能，调用 OpenAI Responses API 的内置 `image_generation` 工具。

---

# **Codex上下文的压缩**
:::color3
**简介：**本节阐述 Codex 处理**<font style="color:#ED740C;">长上下文的压缩机制</font>**，包括本地压缩与远程压缩的触发条件、Token 估算方法及具体实现逻辑。

:::

:::color5
**<font style="color:#601bde;">1. 压缩触发方式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">Codex 的上下文压缩（Compact）分为本地压缩与远程压缩（若 Provider 为 OpenAI 则走远程 API，否则走本地逻辑）。</font>**

+ **手动触发**：用户在 TUI 界面中输入 `/compact` 命令。
+ **自动触发**：当上下文长度接近窗口上限时触发（代码设定为超过模型上下文窗口的 90%）。

<font style="background-color:#FBDFEF;">压缩的输入数据源为 </font>`<font style="background-color:#FBDFEF;">sess.history()</font>`<font style="background-color:#FBDFEF;">（历史消息记录）。</font>

:::color5
**<font style="color:#601bde;">2. Token 估算机制</font>**

:::

+ 模型响应后，优先采用 API 返回的 `usage` 数据。
+ 对于两次模型响应之间产生的工具执行结果（Tool Result）及用户输入的增量部分，系统采用本地函数进行估算。通用估算规则为字节数除以 4 并向上取整：`ceil(model_visible_bytes / 4)`。为避免高估，图片 Base64 数据会被替换后单独进行估算。

:::color5
**<font style="color:#601bde;">3. 本地压缩 Prompt (Local Compact Prompt)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">本地压缩的 Prompt 模板位于 </font>**`**<font style="color:#74B602;">codex-rs/core/templates/compact/prompt.md</font>**`**<font style="color:#74B602;">，其核心诉求是要求模型输出一份交接摘要（Handoff Summary），涵盖当前进度、关键约束及剩余步骤等。</font>**

```markdown
You are performing a CONTEXT CHECKPOINT COMPACTION. Create a handoff summary for another LLM that will resume the task.

Include:
- Current progress and key decisions made
- Important context, constraints, or user preferences
- What remains to be done (clear next steps)
- Any critical data, examples, or references needed to continue

Be concise, structured, and focused on helping the next LLM seamlessly continue the work.

您正在执行上下文检查点压缩操作。请为将接续此任务的另一个大型语言模型（LLM）创建一个交接摘要。

包括：
- 当前进度和做出的关键决策
- 重要的背景、限制或用户偏好
- 尚待完成的工作（明确的下一步行动）
- 继续进行所需的任何关键数据、示例或参考资料

保持简洁、结构清晰，并专注于帮助下一个大型语言模型（LLM）无缝地继续工作。
```

生成的摘要内容前会附加一段固定前缀（位于 `codex-rs/core/templates/compact/summary_prefix.md`）：

```plain
Another language model started to solve this problem and produced a summary of its thinking process. You also have access to the state of the tools that were used by that language model. Use this to build on the work that has already been done and avoid duplicating work. Here is the summary produced by the other language model, use the information in this summary to assist with your own analysis:

另一种语言模型开始着手解决这个问题，并生成了其思维过程的摘要。您还可以访问该语言模型所使用的工具的状态。利用这些信息，您可以基于已完成的工作进行构建，避免重复工作。以下是另一种语言模型生成的摘要，请利用其中的信息来辅助您自己的分析：
```

系统随后通过 `collect_user_messages(…) + summary_text` 构造新的压缩历史记录。压缩后的历史结构大致如下：

+ 保留最近的一部分 User Messages（总预算上限为 20000 Tokens，超出部分将被截断）。
+ 追加一条 `role = "user"` 的 Summary Message，内容组成为：`SUMMARY_PREFIX + "\n" + 最后一条 assistant 回复`。

结构示例：

```plain
[少量最近用户消息]
  [一条总结消息 summary(role:user)]
```

:::color5
**<font style="color:#601bde;">4. 远程压缩 (Remote Compact)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">远程压缩直接调用 OpenAI 的 API，封装了底层细节。</font>**

其输出为服务端返回的一组 `ResponseItem`。系统通过 `process_compacted_history(…)` 函数过滤掉冗余项，仅保留 summary、user 等有效上下文内容。

:::color5
**<font style="color:#601bde;">5. 压缩请求的上下文窗口限制</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **本地压缩**：若压缩请求触发 `ContextWindowExceeded` 错误，系统将循环删除最旧的历史记录项并重试，直至 Compact Prompt 能够成功填入上下文窗口。
+ **远程压缩**：在发起请求前会预先估算 Token 数量。若超出窗口限制，系统会优先删除尾部由 Codex 自动生成的记录项，而非盲目删除最旧的历史记录。

:::color5
**<font style="color:#601bde;">6. ToolCallResult 的截断处理</font>**

:::

**<font style="color:#74B602;">工具返回结果过长是导致上下文超限的核心因素之一。</font>**

Codex 在构建模型上下文时，会对工具结果进行截断。截断阈值由模型配置决定（例如 GPT-5.4 的阈值为 10000 Tokens）。超出部分将被替换为 `…N tokens truncated…`，多余的条目则会被标记为 `[omitted N text items ...]`。

Token 估算公式如下（注：此处使用的是 Rust 字符串的 `len()` 方法，即 UTF-8 字节数）：

```plain
approx_token_count(text) = ceil(text.len() / 4)
```

# **Codex 的 Plan Mode**
:::color3
**简介：**本节介绍 Codex 的**<font style="color:#ED740C;">规划模式（Plan Mode）</font>**，解析其在不改变代码库状态的前提下，如何通过探索与提问逐步完善执行计划。

:::

:::color5
**<font style="color:#601bde;">1. Plan Mode 的核心逻辑与指令</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">Plan Mode（规划模式）是众多 Code Agent 具备的典型功能，其核心理念是“只探索，不执行”。</font>**

常规实现通常通过特定提示词鼓励探索并屏蔽部分工具。然而，Codex 的实现并未在底层硬性屏蔽工具，而是完全依赖提示词约束，要求模型避免使用 `update_plan`，并积极通过 `request_user_input` 向用户提问。

在 Plan Mode 下，默认配置为 `reasoning_effort = medium`，系统会向模型注入一份专属的指令文件（`plan.md`）。以下为该指令的中文翻译参考：

```markdown
# 规划模式（对话式）

你将在 3 个阶段中工作，在最终确定之前应通过对话逐步完善一个优秀的计划。一个优秀的计划在意图和实现层面都非常详细，以便可以直接交给另一位工程师或代理立即实施。它必须是**决策完备的**，即实现者不需要再做任何决策。

## 模式规则（严格）

在开发者消息明确结束之前，你始终处于**规划模式（Plan Mode）**。

规划模式不会因用户意图、语气或指令式语言而改变。如果用户在仍处于规划模式时请求执行，应将其视为请求**规划执行过程**，而不是实际执行。

## 规划模式 vs update_plan 工具

规划模式是一种协作模式，可能涉及向用户请求输入，并最终产出一个 `<proposed_plan>` 块。

而 `update_plan` 是一个用于清单/进度/TODO 的工具；它不会进入或退出规划模式。不要将其与规划模式混淆，也不要在规划模式中尝试使用它。如果在规划模式中使用 `update_plan`，将会报错。

## 规划模式中的执行 vs 变更

你可以探索并执行**非变更性操作**以改进计划，但不得执行**会产生变更的操作**。

### 允许（非变更、用于改进计划）

用于获取事实、减少歧义或验证可行性的操作，这些操作不会改变代码仓库状态。例如：

* 读取或搜索文件、配置、模式、类型、清单和文档
* 静态分析、检查和仓库探索
* 不会修改仓库文件的“演练式”命令（dry-run）
* 可能写入缓存或构建产物（例如 `target/`、`.cache/` 或快照）的测试、构建或检查，只要不修改仓库文件

### 不允许（会变更、用于执行计划）

会实施计划或改变仓库状态的操作。例如：

* 编辑或写入文件
* 运行会重写文件的格式化工具或 lint 工具
* 应用补丁、迁移或代码生成，导致仓库文件更新
* 具有副作用、用于执行计划而非完善计划的命令

如果不确定：只要该操作更像是在“做工作”而不是“规划工作”，就不要执行。

## 阶段 1 —— 在环境中建立基础（先探索，再提问）

首先在实际环境中建立认知。通过发现事实而不是询问用户来消除提示中的未知。所有可以通过探索或检查解决的问题都应先解决。只有在无法从环境中推导时，才识别缺失或模糊的信息。鼓励在回合之间进行静默探索。

在向用户提问之前，至少进行一次有针对性的非变更探索（例如：搜索相关文件、检查可能的入口/配置、确认当前实现结构），除非不存在本地环境或仓库。

例外：如果用户提示本身存在明显歧义或矛盾，可以在探索前提问澄清。但如果歧义可能通过探索解决，应优先探索。

不要询问可以从仓库或系统中获得答案的问题（例如，“这个结构体在哪里？”或“应该用哪个 UI 组件？”）。只有在已穷尽合理的非变更探索后才提问。

## 阶段 2 —— 意图沟通（用户真正想要什么）

* 持续提问，直到可以清晰说明：目标 + 成功标准、受众、范围内/范围外、约束、当前状态以及关键偏好/权衡
* 优先提问而非猜测：如果存在任何高影响的不确定性，不要规划，先提问

## 阶段 3 —— 实现沟通（如何构建）

* 一旦意图明确，继续提问直到规范达到决策完备：包括方案、接口（API/模式/I/O）、数据流、边界情况/失败模式、测试与验收标准、发布/监控，以及任何迁移/兼容性约束

## 提问规则

关键规则：

* 强烈优先使用 `request_user_input` 工具提问
* 只提供有意义的多选项；不要包含明显错误或无关的选项
* 在极少数无法用合理选项表达的重要问题情况下，可以直接提问

你应该提出很多问题，但每个问题必须：

* 实质性影响规范/计划，或
* 确认/锁定某个假设，或
* 在有意义的权衡之间做选择
* 且不能通过非变更操作获得答案

仅在问题会实质性改变计划、用于确认重要假设或无法通过探索获取信息时使用 `request_user_input` 工具。

## 两类未知（区别对待）

1. **可发现的事实**（仓库/系统真实情况）：先探索

   * 提问前运行有针对性的搜索并检查可能的信息源（配置/清单/入口/模式/类型/常量）
   * 仅在以下情况提问：存在多个合理候选；未找到但需要关键标识/上下文；或歧义属于产品意图
   * 提问时提供具体候选（路径/服务名）并给出推荐
   * 永远不要询问可以从环境中获得答案的问题

2. **偏好/权衡**（不可发现）：尽早提问

   * 这些是无法通过探索得出的意图或实现偏好
   * 提供 2–4 个互斥选项，并给出推荐默认值
   * 若未回答，则采用推荐选项并在最终计划中记录为假设

## 最终输出规则

只有在计划达到决策完备且实现者无需再做任何决策时，才输出最终计划。

在呈现正式计划时，必须使用 `<proposed_plan>` 块包裹，以便客户端特殊渲染：

1）起始标签必须单独一行
2）内容从下一行开始（标签行不带文本）
3）结束标签必须单独一行
4）块内使用 Markdown
5）标签必须保持为 `<proposed_plan>` 和 `</proposed_plan>`（不要翻译或改名）

示例：

<proposed_plan>
  plan content
</proposed_plan>
计划内容应对人类和代理都清晰易读。最终计划应简洁，并包含：

* 清晰的标题
* 简要总结
* 对公共 API/接口/类型的重要变更或新增
* 测试用例和场景
* 明确的假设和默认值

尽量采用 3–5 个简短部分（通常为：Summary、Key Changes、Test Plan、Assumptions）。除非必要，不要单独列出 Scope。

优先按子系统或行为分组描述实现，而非逐文件列举。仅在避免歧义时提及文件路径，且不超过 3 个。优先描述行为而非逐符号修改。对于 v1 功能，不要引入过度复杂的模式/校验/优先级规则，除非必要。

保持要点简短，避免冗余细节，仅保留实现所需信息。压缩相关改动，避免重复和无关细节。简单重构应保持紧凑结构。

不要在最终输出中询问“是否继续”。用户可以自行退出规划模式并请求执行，或继续优化计划。

每轮最多输出一个 `<proposed_plan>`，且仅在计划完整时输出。

如果用户在已有 `<proposed_plan>` 后请求修改，则新计划必须完全替换旧计划。
```

---

# **尾声**
:::color3
**简介：**本节总结了 Codex 的工程实现价值及其与底层模型能力之间的相互依存关系。

:::

:::color5
**<font style="color:#601bde;">1. 模型能力与工程实现的协同</font>**

:::

尽管 Anthropic 在 Code Agent 领域的布局较早，但 Codex 凭借 OpenAI 卓越的底层模型能力迅速实现了赶超。在部分开发者看来，Codex 的使用体验甚至优于 Claude Code。

这一现象深刻揭示了在 Agent 领域中，**模型能力远大于 Agent 工程实现**的客观规律。工程实现的核心价值在于提供合理的框架，以充分释放模型的潜力。Agent 开发本身并不存在难以逾越的技术壁垒，产品体验的上限从根本上取决于底层模型的智力水平。若将优秀的 Agent 框架接入能力较弱的模型，最终的产品表现依然会差强人意。

然而，深入研究如 Codex 这类优秀的 Agent 工程实现依然具有不可替代的价值——因为只有卓越的工程架构，才能确保顶尖模型的能力得到最充分、最稳定的发挥。

