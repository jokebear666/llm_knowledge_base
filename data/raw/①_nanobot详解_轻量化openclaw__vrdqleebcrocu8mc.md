# ① nanobot详解：轻量化openclaw

<!-- source: yuque://zhongxian-iiot9/hlyypb/vrdqleebcrocu8mc -->

:::color3
**简介：**当 Manus、OpenAI Codex、Claude Code 等 AI Agent 框架动辄包含几十万行代码时，一个仅拥有约 **<font style="color:#ED740C;">4000 行核心代码的轻量级框架却实现了五脏俱全的功能：涵盖 ReAct 推理循环、双层记忆系统、多渠道接入、子 Agent 协作以及 MCP 协议支持等</font>**。本文将带您逐层拆解 nanobot 的技术内核。

**项目地址**：[https://github.com/HKUDS/nanobot](https://github.com/HKUDS/nanobot)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774335909880-054b66cb-9baa-406a-bb24-6326d3715dc3.png)

:::color5
**<font style="color:#601bde;">1. 核心特性与优势 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">在当前 AI Agent 领域，诸如 Cursor、Cline、OpenAI Codex 等主流系统通常具备庞大的代码库与复杂的微服务架构。相比之下，nanobot 采用了极简的设计理念，其核心代码仅约 4000 行，却完整实现了 openclaw 的核心能力：</font>**

+ **多渠道广泛接入**：支持 10 余种主流聊天渠道。
+ **内置 ReAct 推理循环**：原生支持多轮工具调用与复杂逻辑推理。
+ **双层记忆系统**：结合长期事实记忆与可检索的历史日志，保障上下文的连贯性。
+ **广泛的模型兼容性**：支持 20 余家 LLM 提供商（如 OpenAI、Claude、DeepSeek、Gemini、通义千问、Kimi 等）。
+ **原生 MCP 协议支持**：支持动态接入外部工具，具备极强的扩展性。
+ **高级协作与调度机制**：内置子 Agent 协作、定时任务（Cron）以及心跳（Heartbeat）机制。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774336615218-16d70005-3be4-43b3-9c92-28cf32b5caca.png)

:::color5
**<font style="color:#601bde;">2. 安装与初始配置 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">nanobot 的安装过程非常简便，支持通过 </font>**`**<font style="background-color:#E8F7CF;">pip</font>**`**<font style="background-color:#E8F7CF;"> 或 </font>**`**<font style="background-color:#E8F7CF;">uv</font>**`**<font style="background-color:#E8F7CF;"> 进行安装：</font>**

```bash
# 使用 PyPI 安装
pip install nanobot-ai

# 使用 uv 安装
uv tool install nanobot-ai
```

系统的核心配置文件位于 `~/.nanobot/config.json`。在首次使用时，建议执行初始化命令：

```bash
nanobot onboard
```

该命令将自动初始化工作区、模板文件及基础配置。核心配置主要涉及三个维度：模型提供方（Providers）、Agent 默认参数（Agents）以及聊天渠道（Channels）。以下为使用火山方舟作为模型提供方并集成飞书渠道的配置示例：

```json
{
  "providers": {
      "openai": {
        "apiKey": "xxx",
        "apiBase": "https://ark.cn-beijing.volces.com/api/v3"
      }
  },
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot/workspace",
      "model": "doubao-seed-1-8-251228",
      "maxTokens": 8192,
      "temperature": 0.7,
      "maxToolIterations": 20
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": ["*"]
    }
  }
}
```

**<font style="background-color:#D9EAFC;">飞书渠道配置说明：</font>**<font style="background-color:#D9EAFC;">  
</font>需前往[飞书开放平台](https://open.larkoffice.com/app?lang=zh-CN)创建应用并开启机器人功能。配置时需选择“使用长连接接收事件”，并添加 `im.message.receive_v1` 事件权限。  
_注意：必须在本地启动 nanobot gateway 后，方可使用长连接接收事件。配置完成后，将机器人发布上线即可开始交互。_

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774334669451-05fa44cb-ffa0-4e76-8e6d-fa123cb1e496.png)

# **nanobot整体流程**
:::color3
**简介：**本章节详细介绍了 nanobot 的整体架构与核心处理流程，涵盖了从**<font style="color:#ED740C;">消息接收、总线流转、Agent 推理到会话管理的完整生命周期</font>**。

:::

:::color5
**<font style="color:#601bde;">1. 架构概览 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">官方 README 提供了一张基础架构图：</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333837049-addc0e45-ee4c-4b27-9a07-f39af338c0ab.png)

为了更直观地理解，nanobot 的结构可以概括为以下形式：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333837427-1c78c58e-813c-4449-8d12-593e35668599.png)

**<font style="color:#D22D8D;">nanobot 的代码组织结构清晰，各模块职责分明：</font>**

```plain
nanobot/
├── agent/                  # 核心：Agent 循环、上下文、记忆、技能、子代理
│   ├── loop.py             # Agent Loop —— 大脑中枢
│   ├── context.py          # 上下文构建器（System Prompt 组装）
│   ├── memory.py           # 记忆系统（MEMORY.md + HISTORY.md）
│   ├── skills.py           # 技能加载器
│   ├── subagent.py         # 子代理管理器
│   └── tools/              # 内建工具集
│       ├── base.py         # 工具基类
│       ├── registry.py     # 工具注册表
│       ├── filesystem.py   # 文件读写编辑
│       ├── shell.py        # Shell 命令执行
│       ├── web.py          # Web 搜索与网页抓取
│       ├── message.py      # 跨渠道消息发送
│       ├── spawn.py        # 子代理生成
│       ├── cron.py         # 定时任务管理
│       └── mcp.py          # MCP 协议客户端
├── bus/                    # 消息总线（解耦渠道与 Agent）
│   ├── events.py           # 事件数据结构
│   └── queue.py            # 异步消息队列
├── channels/               # 多渠道接入层
│   ├── base.py             # 渠道抽象基类
│   ├── manager.py          # 渠道管理器
│   ├── feishu.py           # 飞书
│   ├── telegram.py         # Telegram
│   └── ...                 # Discord、Slack、WhatsApp 等
├── session/                # 会话管理
│   └── manager.py          # 会话持久化（JSONL）
├── cron/                   # 定时任务引擎
│   ├── service.py          # 调度服务
│   └── types.py            # 任务数据结构
├── heartbeat/              # 心跳服务
│   └── service.py          # 周期性唤醒
├── providers/              # LLM 提供商抽象层
│   ├── base.py             # 统一接口
│   ├── litellm_provider.py # LiteLLM 适配器
│   └── ...
├── config/                 # 配置加载
├── skills/                 # 内置技能包（Markdown 文件）
├── templates/              # 工作区模板
└── cli/                    # CLI 入口
```

**<font style="background-color:#E8F7CF;">在此架构中，以下核心模块的功能需重点掌握：</font>**

| **模块** | **作用** |
| :--- | :--- |
| Channel | 负责消息的接收与发送。处理与飞书的长连接、Telegram 消息接收及最终回复的发送，但不参与内容生成。 |
| MessageBus | 负责消息转运。渠道层将接收的消息放入 inbound 队列，Agent 处理完毕后将结果放入 outbound 队列，实现渠道与 Agent 的解耦，便于两端扩展。 |
| Gateway | 系统的现场总控。执行 `nanobot gateway` 时，不仅启动 HTTP 服务，还串联渠道管理器、消息总线、AgentLoop、CronService、HeartbeatService 等运行部件，充当“中控室”。 |
| AgentLoop | nanobot 的核心控制中枢。处理用户输入、会话历史、长期记忆、系统 Prompt 构建、工具调用决策及后续处理。 |
| SessionManager | 负责会话历史管理。为每个渠道、每个会话维护连续的上下文。 |
| MemoryStore | 解决长期记忆问题。将会话历史沉淀为更高层次的长期记忆与历史日志，避免上下文过载。 |
| SkillsLoader | 解决模型领域知识不足的问题。将特定的工作流和技巧封装为 Skill，供模型按需加载。 |
| ToolRegistry | 连接模型与现实世界的桥梁。将文件系统、Shell、Web、消息、定时任务、子代理及外部 MCP 服务等封装为模型可调用的工具。 |


<font style="background-color:#FBDFEF;">nanobot 的设计原则在于将系统复杂度拆解，分配至合适的层级，而非集中于单一的“大脑”模块中，从而保持各模块边界清晰。</font>

:::color5
**<font style="color:#601bde;">3. Channel 层处理 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">消息的起点位于 </font>**`**<font style="background-color:#E8F7CF;">FeishuChannel</font>**`**<font style="background-color:#E8F7CF;">。飞书渠道采用 </font>****<font style="color:#74B602;background-color:#E8F7CF;">WebSocket 长连接 </font>****<font style="background-color:#E8F7CF;">接入，而非传统的 Webhook 回调。此设计使得部署 nanobot 无需公网 IP、域名或 SSL 证书，仅需具备网络连接的设备即可。</font>**

```plain
# nanobot/channels/feishu.py
class FeishuChannel(BaseChannel):
    """
    Feishu/Lark channel using WebSocket long connection.
    Uses WebSocket to receive events - no public IP or webhook required.
    """

    async def start(self) -> None:
        self._ws_client = lark.ws.Client(
            self.config.app_id,
            self.config.app_secret,
            event_handler=event_handler,
            log_level=lark.LogLevel.INFO
        )

        # WebSocket 在独立线程中运行，自带断线重连
        def run_ws():
            while self._running:
                try:
                    self._ws_client.start()
                except Exception as e:
                    logger.warning("Feishu WebSocket error: {}", e)
                if self._running:
                    time.sleep(5)

        self._ws_thread = threading.Thread(target=run_ws, daemon=True)
        self._ws_thread.start()
```

<font style="background-color:#FBDFEF;">在异步的 </font>`<font style="background-color:#FBDFEF;">_on_message</font>`<font style="background-color:#FBDFEF;"> 方法中，飞书的各类消息（文本、富文本、图片、文件、卡片等）被统一解析为纯文本和媒体文件。若消息包含图片，系统会将其下载至本地并转换为 base64 编码传递给 LLM。此外，系统在接收消息后会立即向用户发送 Emoji 回应（默认是 </font><font style="background-color:#FBDFEF;">👍</font><font style="background-color:#FBDFEF;">），以提示消息已接收且正在处理。</font>

```plain
async def _on_message(self, data: "P2ImMessageReceiveV1") -> None:
    # 消息去重
    message_id = message.message_id
    if message_id in self._processed_message_ids:
        return
    self._processed_message_ids[message_id] = None

    # 给用户一个"收到"的反应
    await self._add_reaction(message_id, self.config.react_emoji)

    # 解析消息内容...
    # 最终推送到消息总线
    await self._handle_message(
        sender_id=sender_id,
        chat_id=reply_to,
        content=content,
        media=media_paths,
        metadata={"message_id": message_id, "chat_type": chat_type, "msg_type": msg_type}
    )
```

:::color5
**<font style="color:#601bde;">4. 消息总线流转 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

`<font style="background-color:#E8F7CF;">_handle_message</font>`<font style="background-color:#E8F7CF;"> 方法的核心任务是构造 </font>`<font style="background-color:#E8F7CF;">InboundMessage</font>`<font style="background-color:#E8F7CF;"> 对象，并将其推入消息总线。</font>

```plain
# nanobot/bus/events.py
@dataclass
class InboundMessage:
    channel: str           # "feishu"
    sender_id: str         # 发送者 ID
    chat_id: str           # 聊天 ID
    content: str           # 消息文本
    media: list[str]       # 媒体文件路径列表
    metadata: dict         # 渠道元数据

    @property
    def session_key(self) -> str:
        return self.session_key_override or f"{self.channel}:{self.chat_id}"
```

`MessageBus` 的实现极为精简，仅包含两个 `asyncio.Queue`：

```plain
# nanobot/bus/queue.py
class MessageBus:
    def __init__(self):
        self.inbound: asyncio.Queue[InboundMessage] = asyncio.Queue()
        self.outbound: asyncio.Queue[OutboundMessage] = asyncio.Queue()

    async def publish_inbound(self, msg: InboundMessage) -> None:
        await self.inbound.put(msg)

    async def consume_inbound(self) -> InboundMessage:
        return await self.inbound.get()
```

<font style="background-color:#FBDFEF;">这两个队列实现了一进一出的消息流转。对于单进程的个人助手而言，</font>`<font style="background-color:#FBDFEF;">asyncio.Queue</font>`<font style="background-color:#FBDFEF;"> 提供了高效的异步解耦能力，且具备 </font>**<font style="background-color:#FBDFEF;">零依赖、零延迟、零运维成本</font>**<font style="background-color:#FBDFEF;"> 的优势，充分体现了 nanobot 避免引入不必要复杂度的设计哲学。</font>

:::color5
**<font style="color:#601bde;">5. Agent Loop 处理 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">消息进入总线后，交由 nanobot 的核心模块 </font>`<font style="background-color:#E8F7CF;">AgentLoop</font>`<font style="background-color:#E8F7CF;"> 处理。其 </font>`<font style="background-color:#E8F7CF;">run</font>`<font style="background-color:#E8F7CF;"> 方法是一个持续运行的消费循环：</font>

```plain
# nanobot/agent/loop.py
async def run(self) -> None:
    self._running = True
    await self._connect_mcp()
    logger.info("Agent loop started")

    while self._running:
        try:
            msg = await asyncio.wait_for(self.bus.consume_inbound(), timeout=1.0)
        except asyncio.TimeoutError:
            continue

        if msg.content.strip().lower() == "/stop":
            await self._handle_stop(msg)
        else:
            task = asyncio.create_task(self._dispatch(msg))
            self._active_tasks.setdefault(msg.session_key, []).append(task)
```

此循环包含两个关键设计：

1. 消息消费设置了 1 秒的超时机制，而非无限阻塞。这确保了循环的响应性，例如用户发送 `/stop` 命令时，系统可随时响应，无需等待当前消息处理完毕。
2. 每条消息被封装为独立的 `asyncio.Task`，并按 `session_key` 分组跟踪。这使得系统能够精确取消特定会话的进行中任务，而不影响其他会话。

<font style="background-color:#FBDFEF;">消息进入 </font>`<font style="background-color:#FBDFEF;">_dispatch</font>`<font style="background-color:#FBDFEF;"> 后，在全局处理锁 </font>`<font style="background-color:#FBDFEF;">_processing_lock</font>`<font style="background-color:#FBDFEF;"> 的保护下交由 </font>`<font style="background-color:#FBDFEF;">_process_message</font>`<font style="background-color:#FBDFEF;"> 处理，正式进入 Agent 推理流程。</font>

:::color5
**<font style="color:#601bde;">6. 消息处理 (Process Message) </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

`<font style="background-color:#E8F7CF;">_process_message</font>`<font style="background-color:#E8F7CF;"> 方法负责编排从消息接收到最终回复的完整逻辑，流程如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333837552-37e7f383-40b2-41a9-9659-efbd77319943.png)

关键步骤解析如下：

1. **系统消息处理：** 若消息来自 `system` 渠道（如 Subagent 结果回报），系统将采用简化路径：跳过斜杠命令检查和记忆整合，直接构建上下文并执行。系统消息的 `chat_id` 格式为 `channel:chat_id`（如 `feishu:oc_xxx`），需先拆分出真实的渠道和聊天 ID。
2. **获取或创建 Session：** 根据 `session_key`（格式为 `channel:chat_id`，如 `feishu:ou_abc123`）查找现有会话，若不存在则创建新会话。`SessionManager` 内部设有内存缓存，以减少磁盘读取频率。
3. **命令处理：** 在调用 LLM 前，系统会检查用户是否发送了斜杠命令。`/new` 命令将触发同步的全量记忆归档（此过程为**阻塞**操作，需确保归档成功后方可清空会话）；`/help` 命令则直接返回帮助文本。若非斜杠命令，则继续后续流程。
4. **检查记忆整合：** 在构建上下文前，系统会检查当前会话中未合并的消息数是否达到阈值（`memory_window`，默认 100）：

```plain
unconsolidated = len(session.messages) - session.last_consolidated
if (unconsolidated >= self.memory_window and session.key not in self._consolidating):
    self._consolidating.add(session.key)
    lock = self._consolidation_locks.setdefault(session.key, asyncio.Lock())

    async def _consolidate_and_unlock():
        try:
            async with lock:
                await self._consolidate_memory(session)
        finally:
            self._consolidating.discard(session.key)
            _task = asyncio.current_task()
            if _task is not None:
                self._consolidation_tasks.discard(_task)

    _task = asyncio.create_task(_consolidate_and_unlock())
    self._consolidation_tasks.add(_task)
```

此步骤至关重要，因为记忆整合会更新 `MEMORY.md` 的内容和 `session.last_consolidated` 指针，这两者将直接影响后续的 System Prompt 注入和历史消息提取。整合任务通过 `asyncio.create_task` 在后台异步执行，**不会阻塞当前消息的处理**。当前对话可能使用旧记忆，但下一轮对话将使用整合后的新记忆，以此避免用户遇到明显延迟。`_consolidating` 集合确保同一会话不会重复触发整合，`_consolidation_locks` 提供互斥保护，`_consolidation_tasks` 保持强引用以防后台任务被垃圾回收。

5. **设置工具上下文：** 将当前消息的 channel、chat_id、message_id 注入到 `message`、`spawn`、`cron` 等工具中，确保工具执行时明确消息发送目标。同时重置 `message_tool` 的 `_sent_in_turn` 标记，用于判断 Agent 是否已主动发送消息。

:::color5
**<font style="color:#601bde;">7. 上下文构建 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">调用 LLM 之前，</font>`<font style="background-color:#E8F7CF;">ContextBuilde</font>`<font style="background-color:#E8F7CF;">负责组装完整的上下文。System Prompt的构建过程具有清晰的层级结构：</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333838634-3fae748a-a693-400a-b323-97b457abff10.png)

**<font style="background-color:#D9EAFC;">身份认知（Identity）</font>**<font style="background-color:#D9EAFC;">  
</font>这是 System Prompt 的基础，定义了 Agent 的身份、工作环境及行为规则：

```python
def _get_identity(self) -> str:
    workspace_path = str(self.workspace.expanduser().resolve())
    system = platform.system()
    runtime = f"{'macOS' if system == 'Darwin' else system} {platform.machine()}, Python {platform.python_version()}"

    return f"""# nanobot 🐈

You are nanobot, a helpful AI assistant.

## Runtime
{runtime}

## Workspace
Your workspace is at: {workspace_path}
- Long-term memory: {workspace_path}/memory/MEMORY.md (write important facts here)
- History log: {workspace_path}/memory/HISTORY.md (grep-searchable). Each entry starts with [YYYY-MM-DD HH:MM].
- Custom skills: {workspace_path}/skills/{{skill-name}}/SKILL.md

## nanobot Guidelines
- State intent before tool calls, but NEVER predict or claim results before receiving them.
- Before modifying a file, read it first. Do not assume files or directories exist.
- After writing or editing a file, re-read it if accuracy matters.
- If a tool call fails, analyze the error before retrying with a different approach.
- Ask for clarification when the request is ambiguous.

Reply directly with text for conversations. Only use the 'message' tool to send to a specific chat channel."""
```

此段 Prompt 明确了记忆文件的路径，指导 Agent 正确记录信息。Guidelines 中的规则有效防止了 LLM 在调用工具前编造结果，并明确了直接回复与使用 message 工具的场景区分。

**<font style="background-color:#D9EAFC;">引导文件（Bootstrap Files）</font>**<font style="background-color:#D9EAFC;">  
</font>系统按固定顺序从工作区加载五个可选的 Markdown 文件，提供高度可定制性：

```plain
BOOTSTRAP_FILES = ["AGENTS.md", "SOUL.md", "USER.md", "TOOLS.md", "IDENTITY.md"]

def _load_bootstrap_files(self) -> str:
    parts = []
    for filename in self.BOOTSTRAP_FILES:
        file_path = self.workspace / filename
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            parts.append(f"## {filename}\n\n{content}")
    return "\n\n".join(parts) if parts else ""
```

各文件职能如下：

| **文件** | **作用** | **源码示例** |
| :--- | :--- | :--- |
| AGENTS.md | 定义 Agent 的行为指令，类似于 `.cursorrules`。包含定时提醒和心跳任务的指导，防止 Agent 仅将提醒写入记忆文件而不创建实际任务。 | `# Agent Instructions...` |
| SOUL.md | 定义 Agent 的性格、价值观和沟通风格。 | `# Soul...` |
| USER.md | 记录用户画像信息，辅助个性化服务。 | `# User Profile...` |
| TOOLS.md | 补充工具的非显式约束，如危险命令拦截等。 | `# Tool Usage Notes...` |
| IDENTITY.md | 预留给用户进行完全自定义的身份覆盖。 |  |


文件加载顺序从通用指令到个性化设定，后续文件可补充或覆盖前置设定。

**<font style="background-color:#D9EAFC;">长期记忆</font>**<font style="background-color:#D9EAFC;">  
</font>从 `MEMORY.md` 文件加载长期记忆内容。

**<font style="background-color:#D9EAFC;">Skills</font>**<font style="background-color:#D9EAFC;">  
</font>采用两级加载策略：标记为 `always=true` 的技能全文注入 System Prompt，其余技能仅提供 XML 格式的摘要清单。Agent 需使用特定技能时，通过 `read_file` 工具按需加载完整内容，以此优化 Token 使用。

此外，**运行时上下文** 会被注入到用户消息前：

```plain
@staticmethod
def _build_runtime_context(channel: str | None, chat_id: str | None) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M (%A)")
    tz = time.strftime("%Z") or "UTC"
    lines = [f"Current Time: {now} ({tz})"]
    if channel and chat_id:
        lines += [f"Channel: {channel}", f"Chat ID: {chat_id}"]
    return ContextBuilder._RUNTIME_CONTEXT_TAG + "\n" + "\n".join(lines)
```

此上下文以特殊标记开头，明确其为元数据而非指令。将其放置于 user 消息中，可避免破坏 Prompt Cache 的前缀匹配，并有效防止 Prompt Injection。

最终，完整的消息列表组装为标准的 OpenAI Chat 格式：

```plain
def build_messages(self, history, current_message, media=None, channel=None, chat_id=None):
    runtime_ctx = self._build_runtime_context(channel, chat_id)
    user_content = self._build_user_content(current_message, media)

    # 合并运行时上下文和用户内容为单条 user 消息
    if isinstance(user_content, str):
        merged = f"{runtime_ctx}\n\n{user_content}"
    else:
        merged = [{"type": "text", "text": runtime_ctx}] + user_content

    return [
        {"role": "system", "content": self.build_system_prompt(skill_names)},
        *history,              # 历史对话
        {"role": "user", "content": merged},  # 当前消息（含运行时上下文）
    ]
```

<font style="background-color:#FBDFEF;">运行时上下文与用户消息合并为单条 user 消息，以兼容某些 LLM Provider 的限制。若包含图片，则编码为 base64 格式。</font>

:::color5
**<font style="color:#601bde;">8. ReAct 循环 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">上下文组装完成后，进入 </font>`<font style="background-color:#E8F7CF;">_run_agent_loop</font>`<font style="background-color:#E8F7CF;"> 推理循环。此环节采用经典的 ReAct 模式：</font>

```plain
async def _run_agent_loop(self, initial_messages, on_progress=None):
    messages = initial_messages
    iteration = 0
    final_content = None
    tools_used: list[str] = []

    while iteration < self.max_iterations:
        iteration += 1

        # 1. 调用 LLM
        response = await self.provider.chat(
            messages=messages,
            tools=self.tools.get_definitions(),
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            reasoning_effort=self.reasoning_effort,
        )

        if response.has_tool_calls:
            # 2. LLM 决定使用工具 —— 执行并将结果加入上下文
            for tool_call in response.tool_calls:
                tools_used.append(tool_call.name)
                result = await self.tools.execute(tool_call.name, tool_call.arguments)
                messages = self.context.add_tool_result(
                    messages, tool_call.id, tool_call.name, result
                )
        else:
            # 3. LLM 给出最终回复 —— 退出循环
            final_content = self._strip_think(response.content)
            break

    return final_content, tools_used, messages
```

循环逻辑如下：将消息列表和工具定义发送至 LLM；若请求调用工具，则执行并将结果追加至消息列表，继续循环；若返回纯文本回复，则循环结束。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333838498-ca71675e-df0b-4c15-a21b-be24a2e2369e.png)

<font style="background-color:#FBDFEF;">循环设有 </font>`<font style="background-color:#FBDFEF;">max_iterations</font>`<font style="background-color:#FBDFEF;"> 上限（默认 40 次），以防无限循环。达到上限时，系统将返回提示信息。</font>`<font style="background-color:#FBDFEF;">_strip_think</font>`<font style="background-color:#FBDFEF;"> 方法用于清理特定模型回复中的 </font>`<font style="background-color:#FBDFEF;"><think>...</think></font>`<font style="background-color:#FBDFEF;"> 块。若 LLM 返回错误，该错误消息不会保存至会话历史，以防污染后续上下文。</font>

:::color5
**<font style="color:#601bde;">9. 工具注册与执行 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">工具执行由 </font>`<font style="background-color:#E8F7CF;">ToolRegistry</font>`<font style="background-color:#E8F7CF;"> 统一管理。各工具继承 </font>`<font style="background-color:#E8F7CF;">Tool</font>`<font style="background-color:#E8F7CF;"> 基类并注册：</font>

```plain
# nanobot/agent/tools/registry.py
async def execute(self, name: str, params: dict[str, Any]) -> str:
    _HINT = "\n\n[Analyze the error above and try a different approach.]"

    tool = self._tools.get(name)
    if not tool:
        return f"Error: Tool '{name}' not found. Available: {', '.join(self.tool_names)}"

    try:
        errors = tool.validate_params(params)
        if errors:
            return f"Error: Invalid parameters for tool '{name}': " + "; ".join(errors) + _HINT
        result = await tool.execute(**params)
        if isinstance(result, str) and result.startswith("Error"):
            return result + _HINT
        return result
    except Exception as e:
        return f"Error executing {name}: {str(e)}" + _HINT
```

工具执行出错时，系统会在错误消息末尾追加提示，引导 LLM 分析错误并尝试其他方法，从而提升纠错能力。

nanobot 默认注册的工具涵盖文件操作、Shell 执行、Web 搜索/抓取、跨渠道消息发送、子代理生成及定时任务等。MCP 外部工具注册后与内建工具等价。

```plain
def _register_default_tools(self) -> None:
    for cls in (ReadFileTool, WriteFileTool, EditFileTool, ListDirTool):
        self.tools.register(cls(workspace=self.workspace, allowed_dir=allowed_dir))
    self.tools.register(ExecTool(...))
    self.tools.register(WebSearchTool(api_key=self.brave_api_key, proxy=self.web_proxy))
    self.tools.register(WebFetchTool(proxy=self.web_proxy))
    self.tools.register(MessageTool(send_callback=self.bus.publish_outbound))
    self.tools.register(SpawnTool(manager=self.subagents))
    if self.cron_service:
        self.tools.register(CronTool(self.cron_service))
```

# **会话管理**
:::color3
**简介：**本章节详细介绍了 nanobot 的会话管理机制，重点阐述了基于 append-only 原则的会话持久化设计、消息清理策略以及历史消息对齐逻辑，以最大化利用 LLM 的 Prompt Cache 机制并保障上下文的稳定性。

:::

:::color5
**<font style="color:#601bde;">1. 核心原则与数据结构 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">每轮对话结束后，系统会将新产生的消息保存至当前会话。nanobot 的会话管理设计严格遵循 </font>**<font style="background-color:#E8F7CF;">append-only（只追加不修改）</font>**<font style="background-color:#E8F7CF;"> 的核心原则。</font>

```plain
# nanobot/session/manager.py
@dataclass
class Session:
    """
    A conversation session.
    Important: Messages are append-only for LLM cache efficiency.
    """
    key: str                    # channel:chat_id
    messages: list[dict]        # 所有历史消息
    last_consolidated: int = 0  # 已被整合到记忆的消息数
```

:::color5
**<font style="color:#601bde;">2. Prompt Cache 与指针机制</font>**

:::

<font style="background-color:#E8F7CF;">采用 append-only 原则的主要原因在于适配现代 LLM API（如 Claude 和 GPT）的 </font>**<font style="background-color:#E8F7CF;">Prompt Cache</font>**<font style="background-color:#E8F7CF;"> 机制。若两次请求的前缀完全一致，Provider 即可复用先前的 KV Cache，从而显著降低首 Token 延迟与 API 成本。</font>

任何对历史消息的修改或删除都会破坏前缀匹配，导致 Cache 整体失效。因此，nanobot 始终采用追加模式。即使执行了记忆整合（consolidation），系统也不会修改现有的消息列表，而是通过 `last_consolidated` 指针来标识哪些消息已被“归档”。

以下图示直观展示了 `last_consolidated` 指针的工作原理：

```plain
Session.messages 数组:
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ m0  │ m1  │ m2  │ m3  │ m4  │ m5  │ m6  │ m7  │ m8  │ m9  │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
                         ▲                                 ▲
                         │                                 │
               last_consolidated = 4              最新消息位置

                ◄─ 已整合到 MEMORY.md ─►  ◄── 活跃上下文 ──►
                     (不再发给 LLM)         (作为 history 发给 LLM)
```

:::color5
**<font style="color:#601bde;">3. 会话持久化格式 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">会话数据的持久化存储采用 JSONL 格式（即每行存储一个独立的 JSON 对象）。文件首行记录会话的元数据，后续各行依次记录具体的对话消息：</font>

```json
{"_type": "metadata", "key": "cli:direct", "created_at": "2026-03-01T17:27:02.381065", "updated_at": "2026-03-05T22:44:17.518718", "metadata": {}, "last_consolidated": 58}
{"role": "user", "content": "你好，请做一下自我介绍", "timestamp": "2026-03-01T17:27:20.804618"}
{"role": "assistant", "content": "你好！我是 **nanobot** 🐈，一个轻量级的AI助手，很高兴认识你！\n\n### 我的特点：\n- **乐于助人且友好**：我会尽力用简洁准确的方式帮你解决问题\n- **能力多样**：\n  - 文件操作：读写编辑文件、浏览目录\n  - 系统交互：执行shell命令、管理任务\n  - 网络能力：网页搜索、内容抓取\n  - 技能扩展：支持查天气、设置定时任务等（还能安装更多技能）\n- **注重靠谱**：我会优先保证准确性，并且透明地告诉你我在做什么\n\n### 我能帮你做这些：\n- 日常信息查询（比如天气、知识科普）\n- 文件处理和自动化脚本\n- 技术问题排查\n- 网页内容整理\n- 定时任务提醒\n\n有任何需求或问题，随时告诉我吧！ 😊", "timestamp": "2026-03-01T17:27:20.804628"}
{"role": "user", "content": "你好，今天深圳天气怎么样", "timestamp": "2026-03-01T17:28:53.205910"}
{"role": "assistant", "content": "🌤️ 深圳今日天气（3月1日 周日）\n\n**当前状况**：阴天  \n**气温**：24°C（最高26°C）  \n**风速**：13 km/h 西北风  \n**能见度**：10 km  \n**降水量**：0.0 mm\n\n**今日分时段预报**：\n- 早晨：局部小雨，19°C，湿度82%，风速18-22 km/h\n- 中午：局部小雨，21°C，湿度83%，风速17-19 km/h\n- 傍晚：局部小雨，21°C，湿度80%，风速13-16 km/h\n- 夜间：多云，21°C，风速10-14 km/h", "timestamp": "2026-03-01T17:28:53.205931"}
```

:::color5
**<font style="color:#601bde;">4. 消息保存与清理策略</font>**

:::

<font style="background-color:#E8F7CF;">在保存新消息的过程中，</font>`<font style="background-color:#E8F7CF;">_save_turn</font>`<font style="background-color:#E8F7CF;"> 方法会执行以下关键的清理与优化操作：</font>

1. **截断超长工具结果**：将超过 500 个字符的工具输出进行截断，并追加 `... (truncated)` 标记。此举旨在防止工具（如 `exec`、`read_file`）返回的大量文本导致 Session 文件体积过度膨胀。
2. **替换 Base64 图片编码**：将内嵌的 Base64 图片编码替换为 `[image]` 占位符。单张图片的 Base64 文本可能高达数百 KB，替换后可大幅缩减存储占用。
3. **剥离运行时上下文**：自动检测并移除带有 `_RUNTIME_CONTEXT_TAG` 标记的内容，以防时间戳等时效性信息在下一轮对话中产生干扰。
4. **过滤无效 Assistant 消息**：若 Assistant 消息既无文本内容也未发起工具调用，系统将跳过保存，避免此类空消息“毒化”后续的上下文环境。

```python
def _save_turn(self, session, messages, skip):
    for m in messages[skip:]:
        entry = dict(m)
        role, content = entry.get("role"), entry.get("content")
        if role == "assistant" and not content and not entry.get("tool_calls"):
            continue  # 跳过空 assistant 消息
        if role == "tool" and isinstance(content, str) and len(content) > self._TOOL_RESULT_MAX_CHARS:
            entry["content"] = content[:self._TOOL_RESULT_MAX_CHARS] + "\n... (truncated)"
        elif role == "user":
            if isinstance(content, str) and content.startswith(ContextBuilder._RUNTIME_CONTEXT_TAG):
                parts = content.split("\n\n", 1)
                if len(parts) > 1 and parts[1].strip():
                    entry["content"] = parts[1]
                else:
                    continue
        entry.setdefault("timestamp", datetime.now().isoformat())
        session.messages.append(entry)
```

:::color5
**<font style="color:#601bde;">5. 历史消息提取与对齐逻辑 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">在提取历史消息时，</font>`<font style="background-color:#E8F7CF;">get_history</font>`<font style="background-color:#E8F7CF;"> 方法内置了一套精巧的对齐逻辑：确保返回的消息序列始终以 </font>`<font style="background-color:#E8F7CF;">user</font>`<font style="background-color:#E8F7CF;"> 角色的消息作为起点。</font>

此设计的目的在于规避 LLM API 的严格校验限制——若历史消息序列的开头是一条孤立的 `tool` 消息（即缺乏带有 `tool_calls` 的对应 `assistant` 消息），API 将直接抛出错误。通过强制对齐至 `user` 消息，系统可确保传递给大模型的消息序列始终合法有效。

# **记忆系统**
:::color3
**简介：**记忆系统是 nanobot 架构设计的核心亮点，其通过优雅的双层架构有效解决了传统聊天机器人长期记忆缺失与信息可检索性的痛点。

:::

:::color5
**<font style="color:#601bde;">1. 双层记忆架构 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="background-color:#E8F7CF;">nanobot 的记忆系统由两层构成，在物理层面表现为两个独立的 Markdown 文件：</font>

```plain
# nanobot/agent/memory.py
class MemoryStore:
    """Two-layer memory: MEMORY.md (long-term facts) + HISTORY.md (grep-searchable log)."""

    def __init__(self, workspace: Path):
        self.memory_dir = ensure_dir(workspace / "memory")
        self.memory_file = self.memory_dir / "MEMORY.md"
        self.history_file = self.memory_dir / "HISTORY.md"
```

两层记忆的定位与关系如下图所示：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333839268-2b9a6861-ef57-488d-b9f6-bb1878d6a1f0.png)  
_图示：nanobot 双层记忆架构的定位与互补关系_

**<font style="background-color:#D9EAFC;">MEMORY.md：长期事实记忆</font>**

+ **定位**：类似于人类的“陈述性记忆”，用于保存用户的偏好、重要决策及关键信息等结构化知识。
+ **更新机制**：每次更新均采用全量覆盖写入的方式，由 LLM 负责新旧信息的合并。
+ **示例**：经过多轮对话后，`MEMORY.md` 的内容可能如下所示：

```plain
## 用户偏好
- 偏好使用 Python 编写代码
- 工作时区：UTC+8

## 项目信息
- 正在开发一个名为 "nanobot" 的 AI Agent 项目
- 使用 Python 3.12 + asyncio 架构
```

**<font style="background-color:#D9EAFC;">HISTORY.md：事件日志</font>**

+ **定位**：类似于人类的“情景记忆”，专门设计为 grep 友好的格式，用于记录带时间戳的对话摘要。
+ **更新机制**：采用只追加（Append-only）的写入模式。
+ **示例**：

```plain
[2026-03-05 14:30] 用户询问了如何配置飞书渠道。讨论了 App ID 和 App Secret 的获取方式，成功完成了配置。

[2026-03-06 10:15] 帮助用户编写了一个 Python 脚本来分析 CSV 数据，使用了 pandas 库，输出结果保存在 output.json 中。
```

**<font style="background-color:#D9EAFC;">架构优势</font>**<font style="background-color:#D9EAFC;">  
</font>这种设计的精妙之处在于两者的互补性：

+ `MEMORY.md` 被注入到 System Prompt 中，确保 Agent 在每次对话中都能“记住”用户的长期偏好，处理“常识性”的高频信息。
+ `HISTORY.md` 由于内容较长，不直接注入 Prompt，但 Agent 可通过 `exec` 工具运行 `grep` 命令来按需搜索历史记录，处理“可检索”的低频信息。

:::color5
**<font style="color:#601bde;">2. 记忆整合机制</font>**

:::

<font style="background-color:#E8F7CF;">记忆整合（Consolidation）并非实时发生，nanobot 明确规定了两种触发时机：</font>

**自动触发：未整合消息数达到阈值**  
在 `_process_message` 方法中，系统会在每次处理用户消息时检查当前会话中未整合的消息数量。当该数量达到 `memory_window`（默认 100 条）时，将自动启动一个异步的后台整合任务：

```python
# nanobot/agent/loop.py — _process_message 方法中
unconsolidated = len(session.messages) - session.last_consolidated
if (unconsolidated >= self.memory_window and session.key not in self._consolidating):
    self._consolidating.add(session.key)
    lock = self._consolidation_locks.setdefault(session.key, asyncio.Lock())

    async def _consolidate_and_unlock():
        try:
            async with lock:
                await self._consolidate_memory(session)
        finally:
            self._consolidating.discard(session.key)

    _task = asyncio.create_task(_consolidate_and_unlock())
    self._consolidation_tasks.add(_task)
```

此过程包含多重保护机制：

+ `_consolidating` 集合：防止同一会话重复触发整合。
+ `_consolidation_locks` 字典：为每个会话提供独立锁，避免并发整合冲突。
+ `_consolidation_tasks` 集合：保持对任务的强引用，防止被垃圾回收（GC）。
+ **非阻塞执行**：整合任务在后台异步执行，不会阻塞当前用户消息的处理。

**<font style="background-color:#D9EAFC;">手动触发：用户发送 </font>**`<font style="background-color:#D9EAFC;">/new</font>`**<font style="background-color:#D9EAFC;"> 命令</font>**<font style="background-color:#D9EAFC;">  
</font>当用户发起全新对话时，nanobot 会先对当前所有未整合消息进行全量归档（`archive_all=True`），以确保信息完整，随后再清空会话：

```python
if cmd == "/new":
    snapshot = session.messages[session.last_consolidated:]
    if snapshot:
        temp = Session(key=session.key)
        temp.messages = list(snapshot)
        if not await self._consolidate_memory(temp, archive_all=True):
            return OutboundMessage(content="Memory archival failed, session not cleared.")

    session.clear()
    self.sessions.save(session)
    self.sessions.invalidate(session.key)
    return OutboundMessage(content="New session started.")
```

与自动整合不同，`/new` 命令触发的整合是**同步阻塞**的，必须在整合成功后才会清空会话。若归档失败，会话将保留并向用户提示错误，这是一种关键的防御性设计。此外，`invalidate` 调用会从内存缓存中移除旧的 session 对象，确保下次加载时从磁盘获取干净的会话。

**<font style="background-color:#D9EAFC;">整合流程详解</font>**<font style="background-color:#D9EAFC;">  
</font>完整的整合流程如下图所示：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333839554-5ea024d1-c817-47d2-91d0-0b75504c098e.png)  
_图示：nanobot 记忆整合的完整处理流程_

整合的核心在于一次富有创意的 LLM 调用。nanobot 定义了一个虚拟的 `save_memory` 工具：

```plain
_SAVE_MEMORY_TOOL = [{
    "type": "function",
    "function": {
        "name": "save_memory",
        "parameters": {
            "type": "object",
            "properties": {
                "history_entry": {
                    "type": "string",
                    "description": "A paragraph (2-5 sentences) summarizing key events. "
                    "Start with [YYYY-MM-DD HH:MM]. Include detail useful for grep search.",
                },
                "memory_update": {
                    "type": "string",
                    "description": "Full updated long-term memory as markdown. Include all existing "
                    "facts plus new ones. Return unchanged if nothing new.",
                },
            },
            "required": ["history_entry", "memory_update"],
        },
    },
}]
```

系统将旧对话与当前记忆内容发送给专属的 "memory consolidation agent"，由其通过调用该虚拟工具来决定记忆内容的更新：

```plain
async def consolidate(self, session, provider, model, *, archive_all=False, memory_window=50):
    # 确定要整合的消息范围
    if archive_all:
        old_messages = session.messages
        keep_count = 0
    else:
        keep_count = memory_window // 2
        old_messages = session.messages[session.last_consolidated:-keep_count]

    # 格式化为带时间戳的文本
    lines = []
    for m in old_messages:
        if not m.get("content"):
            continue
        lines.append(f"[{m.get('timestamp', '?')[:16]}] {m['role'].upper()}: {m['content']}")

    current_memory = self.read_long_term()
    prompt = f"""Process this conversation and call the save_memory tool with your consolidation.

## Current Long-term Memory
{current_memory or "(empty)"}

## Conversation to Process
{chr(10).join(lines)}"""

    response = await provider.chat(
        messages=[
            {"role": "system", "content": "You are a memory consolidation agent. "
             "Call the save_memory tool with your consolidation of the conversation."},
            {"role": "user", "content": prompt},
        ],
        tools=_SAVE_MEMORY_TOOL,
        model=model,
    )

    # 从工具调用中提取结果并写入
    args = response.tool_calls[0].arguments
    if entry := args.get("history_entry"):
        self.append_history(entry)          # 追加到 HISTORY.md
    if update := args.get("memory_update"):
        if update != current_memory:
            self.write_long_term(update)     # 覆盖 MEMORY.md

    # 更新指针
    session.last_consolidated = 0 if archive_all else len(session.messages) - keep_count
```

**<font style="background-color:#D9EAFC;">设计考量</font>**<font style="background-color:#D9EAFC;">：</font>

+ **虚拟工具调用**：相较于直接解析 LLM 的自由文本输出，工具调用返回的确定性 JSON 格式更易于解析与校验。此技巧在 nanobot 的 Heartbeat 服务中亦有应用。
+ **“保留一半”策略**：通过 `keep_count = memory_window // 2`，系统仅整合前一半的旧消息，保留后一半在活跃上下文中，有效避免了“记忆断层”现象。
+ **全量状态快照**：要求 LLM 返回包含所有现有及新增事实的完整长期记忆（`memory_update`），确保 `MEMORY.md` 始终维持完整的状态快照，免除手动合并增量的繁琐。

:::color5
**<font style="color:#601bde;">3. 记忆注入过程 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">记忆最终在 System Prompt 的第三层完成注入：</font>**

```plain
memory = self.memory.get_memory_context()
if memory:
    parts.append(f"# Memory\n\n{memory}")
```

`get_memory_context()` 方法的逻辑十分简洁：读取 `MEMORY.md` 的内容，并附加 `## Long-term Memory` 标题。通过这一机制，Agent 在每次对话伊始便能在 System Prompt 中获取完整的长期记忆，从而自然地将这些背景知识融入交互中，提供高度个性化的服务体验。

# **Skills 技能系统**
:::color3
**简介：**nanobot 的技能系统提供了一种轻量级的能力扩展机制，通过特定目录下的 Markdown 文件实现技能的自动发现与渐进式加载。

:::

:::color5
**<font style="color:#601bde;">1. Skills 的发现与加载机制 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">技能主要来源于两个路径：工作区自定义技能（</font>**`**<font style="background-color:#E8F7CF;">workspace/skills/</font>**`**<font style="background-color:#E8F7CF;">）与内置技能（</font>**`**<font style="background-color:#E8F7CF;">nanobot/skills/</font>**`**<font style="background-color:#E8F7CF;">）。其中，工作区技能具有更高的优先级，能够覆盖同名的内置技能：</font>**

```plain
技能加载优先级:
workspace/skills/weather/SKILL.md   ◄── 优先使用（用户自定义）
nanobot/skills/weather/SKILL.md     ◄── 被同名工作区技能覆盖
nanobot/skills/github/SKILL.md      ◄── 无同名覆盖，正常加载
```

每个技能均可在其 YAML frontmatter 中声明前置依赖（如特定的命令行工具或环境变量）。系统在加载时会通过 `_check_requirements` 方法校验这些依赖。若依赖未满足，该技能将被标记为不可用，但仍会显示在目录中，以便 Agent 协助用户安装缺失的依赖项。

:::color5
**<font style="color:#601bde;">2. 渐进式加载策略</font>**

:::

为优化性能与上下文长度，技能在 System Prompt 中仅以 XML 摘要的形式呈现。Agent 仅在实际需要时，才会通过 `read_file` 工具加载技能的完整内容：

```plain
def build_skills_summary(self) -> str:
    lines = ["<skills>"]
    for s in all_skills:
        lines.append(f"  <skill available=\"{str(available).lower()}\">")
        lines.append(f"    <name>{name}</name>")
        lines.append(f"    <description>{desc}</description>")
        lines.append(f"    <location>{path}</location>")
        lines.append("  </skill>")
    lines.append("</skills>")
    return "\n".join(lines)
```

<font style="background-color:#FBDFEF;">采用 XML 格式而非 JSON 或 Markdown 列表来构建技能清单，是因为 LLM 在处理 XML 结构化数据时通常表现出更优的理解能力，特别是在提取特定字段（如 </font>`<font style="background-color:#FBDFEF;">location</font>`<font style="background-color:#FBDFEF;">）时更为精准。</font>

# **MCP 集成**
:::color3
**简介：**nanobot 优雅地集成了 Anthropic 提出的 MCP（Model Context Protocol）标准，实现了外部工具与内建工具的无缝统一调用。

:::

:::color5
**<font style="color:#601bde;">1. MCP 工具的无缝集成 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">在 nanobot 的架构中，外部 MCP 工具经注册后，其使用体验与内建工具完全一致。Agent 无需感知工具的底层来源（内建或外部 MCP 服务器）。</font>**

```python
# nanobot/agent/tools/mcp.py
class MCPToolWrapper(Tool):
    """将 MCP 服务器的工具包装为 nanobot 原生 Tool。"""

    def __init__(self, session, server_name: str, tool_def, tool_timeout: int = 30):
        self._session = session
        self._original_name = tool_def.name
        self._name = f"mcp_{server_name}_{tool_def.name}"
        self._description = tool_def.description or tool_def.name
        self._parameters = tool_def.inputSchema or {"type": "object", "properties": {}}

    async def execute(self, **kwargs: Any) -> str:
        result = await asyncio.wait_for(
            self._session.call_tool(self._original_name, arguments=kwargs),
            timeout=self._tool_timeout,
        )
        parts = []
        for block in result.content:
            if isinstance(block, types.TextContent):
                parts.append(block.text)
            else:
                parts.append(str(block))
        return "\n".join(parts) or "(no output)"
```

<font style="background-color:#FBDFEF;">MCP 的连接与注册流程如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333839338-da8703f7-f425-4952-8e2f-03e8c58c6daf.png)  
_图示：MCP 工具的接入与配置流程_

**核心机制说明**：

+ **命名规范**：工具名称统一遵循 `mcp_{server_name}_{tool_name}` 的规则，有效避免了不同 MCP 服务器间的命名冲突。
+ **懒加载连接**：MCP 服务器的连接采用懒加载模式，即仅在接收到第一条消息时才尝试建立连接，而非在系统启动时全量初始化。若连接失败，系统将在后续消息到达时自动重试。
+ **多传输协议支持**：MCP 支持两种传输方式：
    - **stdio**：通过子进程通信，适用于本地工具集成。
    - **HTTP**：基于 Streamable HTTP 协议，适用于远程服务调用。
+ **超时控制优化**：在 HTTP 模式下，nanobot 会显式创建一个无超时限制的 `httpx.AsyncClient` 实例，以防止底层的 5 秒默认超时干扰更高层级的工具超时控制逻辑。

# **Subagent**
:::color3
**简介：**当用户发起耗时较长的任务时，Agent 可通过 `spawn` 工具在后台创建子代理（Subagent）执行任务，从而立即将控制权交还给用户。

:::

:::color5
**<font style="color:#601bde;">1. Subagent 的创建与生命周期 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">Agent 使用 </font>**`**<font style="background-color:#E8F7CF;">spawn</font>**`**<font style="background-color:#E8F7CF;"> 工具创建 Subagent 的代码示例如下：</font>**

```python
# nanobot/agent/subagent.py
async def spawn(self, task, label=None, origin_channel="cli", origin_chat_id="direct", session_key=None):
    task_id = str(uuid.uuid4())[:8]
    bg_task = asyncio.create_task(
        self._run_subagent(task_id, task, display_label, origin)
    )
    self._running_tasks[task_id] = bg_task
    return f"Subagent [{display_label}] started (id: {task_id}). I'll notify you when it completes."
```

Subagent 的完整生命周期如下图所示：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333841222-cc09d0e5-0821-418b-9f18-6d7863d58c5f.png)  
_图示：Subagent 的完整生命周期与执行流程_

:::color5
**<font style="color:#601bde;">2. Subagent 的关键设计特点</font>**

:::

**<font style="background-color:#E8F7CF;">Subagent 的设计包含以下几个核心特点：</font>**

+ **精简的工具集**：Subagent 被有意剥离了 `message` 工具（无法直接向用户发送消息）和 `spawn` 工具（无法再次生成子代理）。此限制旨在防止子代理产生意外的副作用或陷入无限递归。
+ **严格的迭代限制**：Subagent 的最大迭代次数被限制为 15 次（主 Agent 为 40 次），以确保后台任务保持相对短小的执行周期。
+ **巧妙的结果通知机制**：Subagent 完成任务后，不会直接向用户发送消息，而是将结果作为一条 `system` 渠道的 `InboundMessage` 注入回消息总线：

```plain
async def _announce_result(self, task_id, label, task, result, origin, status):
    announce_content = f"""[Subagent '{label}' completed]
Task: {task}
Result: {result}
Summarize this naturally for the user. Keep it brief (1-2 sentences). Do not mention technical details like "subagent" or task IDs."""

    msg = InboundMessage(
        channel="system",
        sender_id="subagent",
        chat_id=f"{origin['channel']}:{origin['chat_id']}",
        content=announce_content,
    )
    await self.bus.publish_inbound(msg)
```

主 Agent 会将这条系统消息视作普通消息处理，经过一轮 LLM 推理后，以自然语言将结果转述给用户。指令中的 "Summarize this naturally for the user" 和 "Do not mention technical details like subagent or task IDs" 确保了用户获得的是自然流畅的对话回复，而非冰冷的技术报告，体现了将技术细节隐藏于幕后的优秀产品设计理念。

+ **批量取消支持**：Subagent 支持按会话批量取消（`cancel_by_session`）。当用户发送 `/stop` 命令时，当前会话关联的所有子代理任务将被一并取消。

# **Cron 与 Heartbeat**
:::color3
**简介：**除了被动响应用户消息，nanobot 还引入了定时任务（Cron）和心跳（Heartbeat）机制，赋予 Agent 主动执行任务的能力。

:::

:::color5
**<font style="color:#601bde;">1. Cron 系统 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">Cron 系统允许 Agent 自主设置定时任务。例如，当用户请求“每天早上 9 点给我发一份市场简报”时，Agent 会通过 </font>**`**<font style="background-color:#E8F7CF;">cron</font>**`**<font style="background-color:#E8F7CF;"> 工具创建一个定时任务。Cron 支持以下三种调度方式：</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333841743-e45d9f6f-78d1-4c26-9e75-2d5a16536f75.png)  
_图示：Cron 系统的三种调度方式_

**<font style="background-color:#CEF5F7;">调度与存储机制</font>**<font style="background-color:#CEF5F7;">：  
</font>任务数据存储于 `jobs.json` 文件中。CronService 的调度核心是 `_arm_timer` 方法，该方法计算出最近一个待执行任务的时间，并使用 `asyncio.sleep` 精确等待至该时刻。系统支持外部修改 `jobs.json` 后的自动热重载，每次触发时均会检查文件的 mtime。

**<font style="background-color:#CEF5F7;">任务执行流程</font>**<font style="background-color:#CEF5F7;">：  
</font>定时任务触发后，并非简单执行预定义操作，而是**将任务指令发送给 Agent，由 Agent 自主决定执行方式**：

```python
async def on_cron_job(job: CronJob) -> str | None:
    reminder_note = (
        "[Scheduled Task] Timer finished.\n\n"
        f"Task '{job.name}' has been triggered.\n"
        f"Scheduled instruction: {job.payload.message}"
    )

    # 禁止在 cron 任务中再创建 cron（通过 ContextVar 标记）
    cron_tool = agent.tools.get("cron")
    cron_token = None
    if isinstance(cron_tool, CronTool):
        cron_token = cron_tool.set_cron_context(True)
    try:
        response = await agent.process_direct(
            reminder_note,
            session_key=f"cron:{job.id}",
            channel=job.payload.channel or "cli",
            chat_id=job.payload.to or "direct",
        )
    finally:
        if isinstance(cron_tool, CronTool) and cron_token is not None:
            cron_tool.reset_cron_context(cron_token)
```

这意味着定时任务可以是复杂的自然语言指令（如“搜索今天的比特币价格并分析趋势”）。Agent 会像处理普通用户消息一样，调用所有可用工具完成任务。每个 cron 任务拥有独立的 session（`cron:{job_id}`），确保任务间的上下文互不干扰。

**安全与防重机制**：

+ **防止任务无限增殖**：`CronTool` 利用 Python 的 `ContextVar` 标记当前是否处于 cron 执行上下文中。`ContextVar` 具有协程安全性，确保并发任务的独立性。若 Agent 在 cron 上下文中尝试调用 `cron add`，系统将直接返回错误 "cannot schedule new jobs from within a cron job execution"，从根本上杜绝了任务无限递归的风险。
+ **消息防重发**：任务完成后，若配置了 `deliver=True` 且存在目标渠道，结果将通过 `MessageBus` 发送给用户。为避免重复通知，若 Agent 在处理过程中已通过 `message` 工具主动发送过消息（`message_tool._sent_in_turn`），则不再重复发送结果。

:::color5
**<font style="color:#601bde;">2. Heartbeat 服务 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">Heartbeat 是一种更为“智能”的周期性唤醒机制。它定期（默认 30 分钟）检查工作区中的 </font>**`**<font style="background-color:#E8F7CF;">HEARTBEAT.md</font>**`**<font style="background-color:#E8F7CF;"> 文件，以评估是否存在待处理任务。</font>**

**两阶段 LLM 决策机制**：  
Heartbeat 的核心创新在于其判断逻辑，它摒弃了传统的正则表达式或关键词匹配，转而采用**两阶段 LLM 决策**过程：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333841565-d4027084-ac06-4d4d-9ee5-99cd08d8a74e.png)  
_图示：Heartbeat 服务的两阶段 LLM 决策流程_

```plain
async def _decide(self, content: str) -> tuple[str, str]:
    """Phase 1: 让 LLM 通过虚拟工具调用来决定是否需要执行。"""
    response = await self.provider.chat(
        messages=[
            {"role": "system", "content": "You are a heartbeat agent. "
             "Call the heartbeat tool to report your decision."},
            {"role": "user", "content": f"Review the following HEARTBEAT.md and decide "
             f"whether there are active tasks.\n\n{content}"},
        ],
        tools=_HEARTBEAT_TOOL,
        model=self.model,
    )
    args = response.tool_calls[0].arguments
    return args.get("action", "skip"), args.get("tasks", "")
```

+ **Phase 1（轻量级决策）**：LLM 通过调用虚拟的 `heartbeat` 工具返回决策结果——`skip`（无任务）或 `run`（有任务）。
+ **Phase 2（完整执行）**：仅当决策为 `run` 时，才会触发完整的 Agent 执行流程。

此设计的优势在于：大多数情况下 `HEARTBEAT.md` 中并无待办任务，Phase 1 的轻量级调用足以完成判断，仅消耗少量 Token，有效避免了不必要的完整 Agent 循环启动。

**<font style="background-color:#D9EAFC;">友好的模板设计</font>**<font style="background-color:#D9EAFC;">：  
</font>`HEARTBEAT.md` 的模板设计十分人性化，划分为 "Active Tasks" 和 "Completed" 两个区域。用户只需将待办事项填入 "Active Tasks"，完成的任务移至 "Completed"，Agent 即可自动解析并执行这些任务。

# **Gateway：从飞书消息到用户回复的完整链路**
:::color3
**简介：**Gateway 模式负责串联所有模块，构建从接收飞书消息到生成并发送用户回复的完整处理链路。

:::

:::color5
**<font style="color:#601bde;">1. Gateway 的启动与服务初始化 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="background-color:#E8F7CF;">当用户通过 </font>**`**<font style="background-color:#E8F7CF;">nanobot gateway</font>**`**<font style="background-color:#E8F7CF;"> 命令启动系统时，Gateway 将依次初始化并启动所有核心服务：</font>**

```plain
nanobot gateway
  ├── CronService.start()        # 启动定时任务调度
  ├── HeartbeatService.start()   # 启动心跳服务
  ├── AgentLoop.run()            # 启动 Agent 主循环
  └── ChannelManager.start_all() # 启动所有渠道（含飞书）
      ├── FeishuChannel.start()  # WebSocket 长连接
      ├── _dispatch_outbound()   # 启动出站消息分发器
      └── ...其他渠道
```

:::color5
**<font style="color:#601bde;">2. 完整的请求处理链路</font>**

:::

**<font style="background-color:#E8F7CF;">整个请求链路的流转过程如下两图所示：</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333842262-0e44f9a5-c5db-4230-ad3d-d638864a387f.png)  
_图示：飞书消息接收与入队流程_

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774333843546-e38bd481-f2b1-4c3c-ad95-52bb0dfff416.png)  
_图示：飞书消息流转处理与回复全流程_

**<font style="background-color:#D9EAFC;">关键上下文注入机制</font>**<font style="background-color:#D9EAFC;">：  
</font>在处理每条消息前，`_set_tool_context` 方法扮演着至关重要的角色。它负责将当前的 channel 和 chat_id 信息注入到 `message`、`spawn` 和 `cron` 工具中。这一机制确保了 Agent 在调用这些工具时，能够准确知晓消息的发送目标、子代理完成后的通知对象，以及定时任务触发后的目标渠道与聊天窗口。

