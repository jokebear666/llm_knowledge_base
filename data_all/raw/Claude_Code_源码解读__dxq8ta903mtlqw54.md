# Claude Code 源码解读

<!-- source: yuque://zhongxian-iiot9/hlyypb/dxq8ta903mtlqw54 -->

:::color3
**简介：**本文深入解读了 Claude Code 的源码，涵盖了其**<font style="color:#ED740C;">技术栈、核心 Agentic 循环、上下文管理、流式工具并行、工具系统设计、Feature Flag 机制、隐藏功能</font>**以及一些值得借鉴的工程细节。

代码：[https://github.com/instructkr/claude-code](https://github.com/instructkr/claude-code)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774962099497-de4aea0e-e632-42a4-8d0a-7d6f8d704da1.png)

:::color5
**<font style="color:#601bde;">1. 先说技术栈 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">Bun + TypeScript + React + Ink。 没错，一个终端 CLI 工具的 UI 层用的是 React。</font>**

Ink 是一个把 React 组件渲染到终端的框架，Claude Code 用它做了整个 TUI 界面——你看到的那些权限弹窗、进度条、工具调用的实时展示，底下全是 JSX。

<font style="background-color:#FBDFEF;">终端 UI 的状态管理确实比想象中复杂（多个 Agent 并行、流式输出、用户中断…），用 React 的状态模型来管比手搓要靠谱得多。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774962795615-880beade-3d9a-4ffb-837f-1c29d68bebc9.png)

# **Agentic Loop：一个 while(true) 撑起整个 Agent**
:::color3
**简介：**Claude Code 的核心大脑位于 `src/query.ts`，通过一个包含预处理、API 调用、工具执行的 while(true) 循环实现了完整的 Agentic 逻辑。

:::

:::color5
**<font style="color:#601bde;">1. 核心逻辑简化 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">整个 Claude Code 最核心的文件是 </font>**`**<font style="color:#74B602;">src/query.ts</font>**`**<font style="color:#74B602;">，1729 行，实现了完整的 agentic 循环。注意不是 </font>**`**<font style="color:#74B602;">QueryEngine.ts</font>**`**<font style="color:#74B602;">——那个是外层的会话管理。真正的”大脑”在 </font>**`**<font style="color:#74B602;">query.ts</font>**`**<font style="color:#74B602;"> 里。</font>**

简化后的核心逻辑：

```tsx
async function* queryLoop(params) {
  let state = { messages, toolUseContext, turnCount: 1, ... }

  while (true) {
    // 1) 一堆预处理：裁历史、压缩上下文、预取 memory 和 skills
    // 2) 调 Claude API（流式）
    // 3) 一边收流一边看有没有 tool_use block
    // 4) 有的话 → 检查权限 → 执行 → 结果塞回 messages → 回到 while
    // 5) 没有工具调用 → 退出
  }
}
```

<font style="background-color:#FBDFEF;">看着简单，但魔鬼在细节里。我挑几个最有意思的说。</font>

# **上下文管理：不是一刀切，是四把手术刀**
:::color3
**简介：**Claude Code 采用了四种不同粒度的压缩机制（HISTORY_SNIP、Microcompact、CONTEXT_COLLAPSE、Autocompact）来处理长对话的上下文，按需分层管理信息的过期。

:::

:::color5
**<font style="color:#601bde;">1. 四种压缩机制 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">用过 Claude Code 的人都知道，长对话到后面它会自动”压缩”。我之前以为就是简单地把早期对话摘要一下。读了源码才知道，它其实有四种不同粒度的压缩机制在同时工作：</font>**

1. **HISTORY_SNIP**：最精细，直接把某些特定消息范围删掉，不做任何摘要。适合清理掉已经没用的中间工具调用结果。
2. **Microcompact**：利用 API 层的 `cache_deleted_input_tokens` 能力，在缓存层面做编辑。这个比较黑科技——它不改消息内容，而是告诉 API”这些 token 你缓存里有但别用了”。
3. **CONTEXT_COLLAPSE**：把旧的对话轮次”归档”成摘要，维护一个类似 git 提交日志的结构。每次新查询时重放这个日志。和 autocompact 的区别是它保留了结构化的归档，不是一坨摘要。
4. **Autocompact**：最粗暴的一种，把整个历史压缩成一段摘要。最后的兜底手段。

这四种机制**不互斥**，按顺序依次执行。如果 snip 和 microcompact 已经把上下文压到阈值以下了，autocompact 就不触发。

<font style="background-color:#FBDFEF;">这给我的启发挺大的——做 Agent 的上下文管理不能只有一种策略。不同场景下信息的”过期速度”不一样，需要分层处理。</font>

# **流式工具并行：模型还在说话就开始干活了**
:::color3
**简介：**Claude Code 实现了流式工具的并行执行，模型输出工具调用块时即刻开始执行，并根据工具的并发安全性进行调度，极大提升了响应速度。

:::

:::color5
**<font style="color:#601bde;">1. 流式工具执行机制 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">这是我觉得最精巧的设计。普通的实现是：等模型说完 → 看有没有工具调用 → 有的话执行 → 结果返回 → 下一轮。Claude Code 不等。</font>**

```tsx
// StreamingToolExecutor.ts
export class StreamingToolExecutor {
  // 模型流式吐出一个 tool_use block，立刻开始执行
  addTool(block: ToolUseBlock, message: AssistantMessage): void { ... }

  // 并发安全的工具可以同时跑，写操作独占
  // 结果按接收顺序排队，保证输出确定性
  async *getRemainingResults(): AsyncGenerator<MessageUpdate> { ... }
}
```

模型还在流式输出后面的内容，前面的工具就已经在跑了。每个工具有个 `isConcurrencySafe` 标记——读文件、grep 这种只读操作可以并行，写文件、bash 这种需要独占。结果按**接收顺序**缓冲，不会乱序。

<font style="background-color:#FBDFEF;">实测下来 Claude Code 的响应速度明显比 Cursor 快，有一部分原因应该就在这里。</font>

:::color5
**<font style="color:#601bde;">2. 撞到输出上限不认输</font>**

:::

```plain
const MAX_OUTPUT_TOKENS_RECOVERY_LIMIT = 3
```

**<font style="color:#74B602;">模型输出撞到 </font>**`**<font style="color:#74B602;">max_output_tokens</font>**`**<font style="color:#74B602;">？循环不报错，”扣留”这个错误消息，悄悄重试，最多 3 次。对用户来说是无感的。</font>**

这段代码上面有个很有意思的注释，是一段模仿中世纪巫师口吻的话：

_Heed these rules well, young wizard. For they are the rules of thinking, and the rules of thinking are the rules of the universe. If ye does not heed these rules, ye will be punished with an entire day of debugging and hair pulling._

<font style="background-color:#FBDFEF;">翻译过来就是：”好好记住这些规则，年轻的巫师。如果你不听，你就等着花一整天调试和薅头发吧。”</font>

<font style="background-color:#FBDFEF;">看得出来这块代码的维护者被坑过不少次。</font>

# **工具系统：不用 class 继承，全是工厂函数**
:::color3
**简介：**Claude Code 的工具系统摒弃了传统的类继承，采用纯函数式的 `buildTool()` 工厂函数，每个工具自包含所有逻辑，支持动态组装。

:::

:::color5
**<font style="color:#601bde;">1. 纯函数式工具定义 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">我之前做 Agent 框架的工具系统，下意识会写一个 </font>**`**<font style="color:#74B602;">BaseTool</font>**`**<font style="color:#74B602;"> 基类然后继承。Claude Code 完全没有继承，全是纯函数式的 </font>**`**<font style="color:#74B602;">buildTool()</font>**`**<font style="color:#74B602;">：</font>**

```tsx
type ToolDef<T> = {
  name: string
  description: string
  inputSchema: ZodSchema<T>           // Zod v4 做校验 + 自动生成 JSON Schema
  call(input: T, ctx: ToolUseContext): AsyncGenerator<...>
  isReadOnly(): boolean
  getPermissions(): ToolPermission[]
  renderToolUse?(input: T): ReactNode  // 直接渲染到终端
  getToolUseSummary?(input, result): string  // 压缩上下文时的摘要
}
```

每个工具完全自包含：schema、权限、执行逻辑、UI 渲染、压缩摘要，全在一个文件里。没有全局注册表——每个 session 动态组装工具池，可以混合静态工具、MCP 工具、Agent 定义的工具。

<font style="background-color:#FBDFEF;">40 多个工具里最复杂的是 BashTool。它不是简单 </font>`<font style="background-color:#FBDFEF;">exec(command)</font>`<font style="background-color:#FBDFEF;">：自动分类命令类型（search/read/write），macOS 上走 sandbox-exec 沙箱，超过 15 秒的阻塞命令自动转后台，大输出存磁盘只给模型一个文件路径引用，还内置了一个 sed 命令专用解析器。</font>

# **Feature Flag：优雅的功能门控**
:::color3
**简介：**Claude Code 采用了编译时（死代码消除）和运行时（GrowthBook A/B 测试）两层 Feature Flag 机制，并内置了用于量化评估的消融实验基础设施。

:::

:::color5
**<font style="color:#601bde;">1. 编译时：字符串级别的死代码消除 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">这块设计我觉得是全项目最值得偷的。Claude Code 用编译时 + 运行时两层 flag：</font>**

```tsx
import { feature } from 'bun:bundle'

const voiceModule = feature('VOICE_MODE')
  ? require('./voice/index.js')
  : null
```

`feature()` 是 Bun 的编译时宏。构建时会被替换成 `true` 或 `false`，`false` 的分支直接被删除——不是”不执行”，是**从二进制文件里物理消失**，连字符串字面量都不剩。

为什么要这么做？因为安全研究员会反编译你的二进制去找隐藏功能（比如今天这次泄露…）。运行时 flag 再怎么关，字符串还在那。编译时 DCE 才是真的”不存在”。

<font style="background-color:#FBDFEF;">讽刺的是，源码泄露之后这层保护就不管用了。但设计思路还是很值得学的。</font>

我在源码里搜到十几个编译时 flag：`VOICE_MODE`、`BRIDGE_MODE`、`DAEMON`、`KAIROS`、`COORDINATOR_MODE`、`PROACTIVE`、`ABLATION_BASELINE`、`HISTORY_SNIP`、`REACTIVE_COMPACT`、`CONTEXT_COLLAPSE`、`CACHED_MICROCOMPACT`、`CHICAGO_MCP`……每一个都对应一个未发布或正在灰度的功能。

:::color5
**<font style="color:#601bde;">2. 运行时：GrowthBook A/B 测试 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

```tsx
const enabled = checkStatsigFeatureGate_CACHED_MAY_BE_STALE(
  'tengu_streaming_tool_execution2'
)
```

用于灰度发布和 kill switch。所有 gate 名称都是 `tengu_` 前缀——tengu（天狗）大概是 Claude Code 的内部代号。从磁盘缓存读取，接受脏读，不阻塞启动。

:::color5
**<font style="color:#601bde;">3. 消融实验基础设施</font>**

:::

有个 flag 叫 `ABLATION_BASELINE`，启用后会**一次性关掉**思考模式、上下文压缩、自动记忆、后台任务：

```tsx
if (feature('ABLATION_BASELINE') && process.env.CLAUDE_CODE_ABLATION_BASELINE) {
  for (const k of [
    'CLAUDE_CODE_DISABLE_THINKING',
    'DISABLE_COMPACT',
    'DISABLE_AUTO_COMPACT',
    'CLAUDE_CODE_DISABLE_AUTO_MEMORY',
    'CLAUDE_CODE_DISABLE_BACKGROUND_TASKS',
  ]) {
    process.env[k] ??= '1';
  }
}
```

<font style="background-color:#FBDFEF;">做过 ML 的都知道消融实验是什么——逐个关掉组件看性能影响。但把这套方法论搬到</font>**<font style="background-color:#FBDFEF;">产品工程</font>**<font style="background-color:#FBDFEF;">上，这是我第一次在工业代码里见到。说明 Anthropic 在认真量化每个功能特性到底值不值。</font>

# **隐藏功能**
:::color3
**简介：**源码中暴露了多个尚未发布的隐藏功能，包括 Voice Mode、Bridge Mode 远程控制系统，以及一个内置的终端虚拟宠物系统（Buddy）。

:::

:::color5
**<font style="color:#601bde;">1. Voice Mode（代号 Amber Quartz） </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

`**<font style="color:#74B602;">src/voice/</font>**`**<font style="color:#74B602;"> 目录确认了语音模式的存在。从 </font>**`**<font style="color:#74B602;">voiceModeEnabled.ts</font>**`**<font style="color:#74B602;"> 看</font>**：

+ 只支持 Claude.ai OAuth 认证（API key、Bedrock、Vertex 都不行）
+ 走的是一个专门的 `voice_stream` 端点
+ 有个紧急 kill switch：GrowthBook flag `tengu_amber_quartz_disabled`
+ 从注释看已经开发到可以使用的程度了

:::color5
**<font style="color:#601bde;">2. Bridge Mode：把你的电脑变成 Claude 的远程终端</font>**

:::

`src/bridge/` 有 31 个文件，是一个完整的远程控制系统。运行 `claude remote-control` 之后，你的本地环境就变成一个被 claude.ai 远程操控的”桥接环境”。

最多支持 **32 个并发会话**，有 JWT 认证 + 可信设备机制，企业管理员可以通过策略禁用。这应该是为了让 claude.ai 网页版能直接操作用户本地的开发环境。

:::color5
**<font style="color:#601bde;">3. Buddy：终端里的电子宠物 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">Claude Code 内置了一个完整的虚拟宠物系统，而且没有用 feature flag 门控——已经在公开版本的二进制里了（只是可能还没暴露入口）：</font>**

```plain
// 18 种宠物
export const SPECIES = [
  duck, goose, blob, cat, dragon, octopus, owl, penguin,
  turtle, snail, ghost, axolotl, capybara, cactus, robot,
  rabbit, mushroom, chonk
] as const

// 5 级稀有度：普通(60%) / 罕见(25%) / 稀有(10%) / 史诗(4%) / 传说(1%)
export const RARITY_WEIGHTS = {
  common: 60, uncommon: 25, rare: 10, epic: 4, legendary: 1,
}

// RPG 式属性
export const STAT_NAMES = ['DEBUGGING','PATIENCE','CHAOS','WISDOM','SNARK'] as const
```

还有帽子（皇冠、礼帽、螺旋桨帽、光环、巫师帽、豆豆帽、头顶小鸭子）、眼睛样式（`·`、`✦`、`×`、`◉`、`@`、`°`）、1% 概率的闪光变体。宠物属性用 Mulberry32 伪随机数生成器从你的用户 ID 确定性计算——所以每个用户的宠物是固定的，不能刷。

但最有意思的是物种名的编码方式：

```plain
// 所有物种名用 hex 编码，因为有一个名字和内部模型代号撞了
const c = String.fromCharCode
export const duck = c(0x64,0x75,0x63,0x6b) as 'duck'
export const goose = c(0x67,0x6f,0x6f,0x73,0x65) as 'goose'
export const capybara = c(0x63,0x61,0x70,0x79,0x62,0x61,0x72,0x61) as 'capybara'
// ... 全部 18 个都这样
```

注释原文：”One species name collides with a model-codename canary in excluded-strings.txt.”

构建系统会 grep 输出文件里有没有被排除的字符串。也就是说，这 18 个物种名中有一个恰好是 Anthropic 某个未公开模型的代号。把所有名字都 hex 编码是为了防止误触发检测。

<font style="background-color:#FBDFEF;">到底是哪个名字？duck、goose、blob、cat、dragon、octopus、owl、penguin、turtle、snail、ghost、axolotl、capybara、cactus、robot、rabbit、mushroom、chonk——其中一个是 Anthropic 下一个模型的代号。随便猜猜？</font>

# **Skill 系统和多 Agent 协调**
:::color3
**简介：**Skill 系统采用约定优于配置的 Markdown 文件形式，而多 Agent 协调器则通过限制 Worker 的权限来防止无限嵌套，设计简洁高效。

:::

:::color5
**<font style="color:#601bde;">1. Skill 系统和多 Agent 协调机制 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">简单提一下这两块，因为我觉得它们的设计可以直接抄。</font>**

+ **Skills 就是 Markdown 文件**。`.claude/skills/` 目录下放 `.md` 文件，YAML frontmatter 里写描述、触发条件、允许的工具、用哪个模型。Claude Code 读文件时如果发现目录下有 skills，会自动加载——你甚至不用显式注册。这种”约定优于配置”的风格很 Rails。
+ **多 Agent 协调器**意外地简单。Coordinator 模式下，主 Agent 只有三个工具：生成 worker、给 worker 发消息、停止 worker。Worker 拿不到 TeamCreate 和 SendMessage——防止 worker 自己再组建团队（无限套娃）。后端支持 tmux pane、in-process、remote 三种方式。

# **工程细节**
:::color3
**简介：**文章最后总结了几个精妙的工程细节，包括隐私保护的类型安全、投机执行和冷启动优化，并分析了源码泄露的原因。

:::

:::color5
**<font style="color:#601bde;">1. 工程细节亮点 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **隐私保护的类型安全**：埋点数据的类型名叫 `AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS`。用类型名本身来提醒开发者”你确认过这不是代码或文件路径了吗”。简单粗暴但有效。
+ **投机执行**：`AppState` 里有 `speculationState`，追踪每一轮的结束方式（bash 命令 / 文件编辑 / 正常结束 / 权限拒绝），用来预判下一步操作并提前执行。这解释了为什么 Claude Code 有时候”想”完就瞬间开始干活。
+ **冷启动优化**：`--version` 路径做到了零 import——直接读编译时内联的版本号，一个模块都不加载就退出。其他子命令走独立的 `import()` 路径。只有最终进主循环才加载完整的 React 应用。

:::color5
**<font style="color:#601bde;">2. 泄露原因</font>**

:::

技术上很简单：npm 发布时忘删 `.map` 文件，map 里引用了 R2 上的源码 zip 包，那个 URL 没有访问控制。

给所有发 npm 包的人提个醒：

1. `package.json` 的 `files` 字段要白名单制，只包含你想发布的东西
2. CI 里加一步检查发布产物里有没有 `.map` 文件
3. 源码归档 URL 要有鉴权，别裸挂在 CDN 上
4. 构建产物和源码的访问控制应该独立管理

_<font style="background-color:#FBDFEF;">本文基于公开泄露的源码进行技术分析，所有代码版权归 Anthropic 所有。</font>_

