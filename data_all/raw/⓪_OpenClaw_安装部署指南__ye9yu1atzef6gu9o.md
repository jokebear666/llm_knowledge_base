# ⓪ OpenClaw 安装部署指南

<!-- source: yuque://zhongxian-iiot9/hlyypb/ye9yu1atzef6gu9o -->

## <font style="color:rgb(25, 27, 31);">一、什么是 OpenClaw？</font>
:::color3
**简介：****<font style="color:rgb(25, 27, 31);">OpenClaw</font>**<font style="color:rgb(25, 27, 31);">（原名 Clawdbot → Moltbot → OpenClaw）是一个开源的个人 AI 助手运行时，由 </font>[<font style="color:rgb(9, 64, 142);">PSPDFKit</font>](https://zhida.zhihu.com/search?content_id=270167542&content_type=Article&match_order=1&q=PSPDFKit&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 创始人 </font>**<font style="color:rgb(25, 27, 31);">Peter Steinberger</font>**<font style="color:rgb(25, 27, 31);"> 于 2026 年初发起。项目在 </font>**<font style="color:rgb(25, 27, 31);">72 小时内增长超过 6 万 Star</font>**<font style="color:rgb(25, 27, 31);">，2 周内突破 </font>**<font style="color:rgb(25, 27, 31);">15 万 Star</font>**<font style="color:rgb(25, 27, 31);">，成为 GitHub 史上增长最快的开源项目之一。</font>

**官网**：[https://openclaw.ai/](https://openclaw.ai/)

**github**:[https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772710398167-ed3f94f8-0964-40e9-8421-89bd79553a9a.png)

<font style="color:rgb(145, 150, 161);">2026.3.3 更新：OpenClaw 已经登顶全球、史上第一</font>

<font style="color:rgb(25, 27, 31);">核心定位：</font>**<font style="color:rgb(25, 27, 31);">在你自己的设备上运行的 AI Agent</font>**<font style="color:rgb(25, 27, 31);">，连接各种消息平台（WhatsApp、Telegram、Slack、Discord、Signal、iMessage、飞书、钉钉等），提供 24⁄7 全天候的 AI 助手体验。</font>

:::color5
**<font style="color:#601BDE;">1.核心特性 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">特性</font>** | **<font style="color:rgb(25, 27, 31);">说明</font>** |
| :--- | :--- |
| <font style="color:rgb(25, 27, 31);">多渠道收件箱</font> | <font style="color:rgb(25, 27, 31);">统一接入 WhatsApp、Telegram、Slack、Discord、Google Chat、Signal、BlueBubbles (iMessage)、飞书、钉钉</font> |
| <font style="color:rgb(25, 27, 31);">本地 Gateway</font> | <font style="color:rgb(25, 27, 31);">基于 WebSocket 的控制平面，运行在 localhost:18789，管理会话、渠道、工具和事件</font> |
| <font style="color:rgb(25, 27, 31);">语音能力</font> | <font style="color:rgb(25, 27, 31);">macOS/iOS/Android 上通过</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">ElevenLabs</font>](https://zhida.zhihu.com/search?content_id=270167542&content_type=Article&match_order=1&q=ElevenLabs&zhida_source=entity)<br/><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">实现始终在线语音（Voice Wake + Talk Mode）</font> |
| <font style="color:rgb(25, 27, 31);">可视化工作区 (Canvas)</font> | <font style="color:rgb(25, 27, 31);">Agent 驱动的可视化工作区，支持 A2UI 交互式 Agent 控制</font> |
| <font style="color:rgb(25, 27, 31);">设备集成</font> | <font style="color:rgb(25, 27, 31);">iOS/Android 节点可暴露摄像头、屏幕录制、位置服务等设备能力</font> |
| <font style="color:rgb(25, 27, 31);">灵活工具</font> | <font style="color:rgb(25, 27, 31);">浏览器控制、定时任务、Webhooks、技能注册表 (ClawHub)，100+ 预配置 AgentSkills</font> |
| <font style="color:rgb(25, 27, 31);">开源许可</font> | <font style="color:rgb(25, 27, 31);">MIT 协议，完全免费</font> |




## <font style="color:rgb(25, 27, 31);">二、系统架构</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">OpenClaw 采用五大功能模块的微服务架构：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```markdown
┌─────────────────────────────────────────────────────────┐
│                    消息渠道层                              │
│  WhatsApp │ Telegram │ Slack │ Discord │ 飞书 │ 钉钉      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Gateway（核心控制平面）                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ Sessions │ │ Channels │ │  Tools   │ │  Events   │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
│                    localhost:18789                       │
└────────────┬───────────────────┬────────────────────────┘
             │                   │
     ┌───────▼───────┐   ┌──────▼──────┐
     │   Agent 层     │   │  Nodes 层   │
     │ (LLM 决策引擎) │   │ (设备端点)   │
     │ Claude/GPT/    │   │ iOS/Android │
     │ Ollama/Qwen    │   │ Camera/GPS  │
     └───────┬───────┘   └─────────────┘
             │
     ┌───────▼───────┐
     │   Skills 层    │
     │  (插件工具包)   │
     │ Shell/Browser/ │
     │ File/Web/API   │
     └───────────────┘
```

:::color5
**<font style="color:#601BDE;">1.关</font>****<font style="color:#601BDE;">键组件说明</font>**<font style="color:#601BDE;">：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">Gateway</font>**<font style="color:rgb(25, 27, 31);">: 单一控制平面，所有消息经由此路由，管理认证和会话</font>
+ **<font style="color:rgb(25, 27, 31);">Agent</font>**<font style="color:rgb(25, 27, 31);">: 连接 LLM（Claude、GPT、Ollama 等），理解上下文并制定执行计划</font>
+ **<font style="color:rgb(25, 27, 31);">Skills</font>**<font style="color:rgb(25, 27, 31);">: JS/TS 可扩展工具包，支持 Shell 命令、文件操作、浏览器控制等</font>
+ **<font style="color:rgb(25, 27, 31);">Channels</font>**<font style="color:rgb(25, 27, 31);">: 连接各消息平台，提供统一消息接口</font>
+ **<font style="color:rgb(25, 27, 31);">Nodes</font>**<font style="color:rgb(25, 27, 31);">: 在用户设备上运行的传感器/端点，暴露设备能力</font>

---

## <font style="color:rgb(25, 27, 31);">三、快速部署方式总览</font>
:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">部署方式对比表</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">部署方式</font>** | **<font style="color:rgb(25, 27, 31);">难度</font>** | **<font style="color:rgb(25, 27, 31);">成本</font>** | **<font style="color:rgb(25, 27, 31);">适用场景</font>** | **<font style="color:rgb(25, 27, 31);">设置时间</font>** |
| :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">一键脚本安装</font> | <font style="color:rgb(25, 27, 31);">⭐</font><font style="color:rgb(25, 27, 31);"> 最低</font> | <font style="color:rgb(25, 27, 31);">免费 + API费用</font> | <font style="color:rgb(25, 27, 31);">本地快速体验</font> | <font style="color:rgb(25, 27, 31);">~5 分钟</font> |
| <font style="color:rgb(25, 27, 31);">npm 全局安装</font> | <font style="color:rgb(25, 27, 31);">⭐⭐</font><font style="color:rgb(25, 27, 31);"> 低</font> | <font style="color:rgb(25, 27, 31);">免费 + API费用</font> | <font style="color:rgb(25, 27, 31);">开发者日常使用</font> | <font style="color:rgb(25, 27, 31);">~5 分钟</font> |
| <font style="color:rgb(25, 27, 31);">Mac Mini 本地部署</font> | <font style="color:rgb(25, 27, 31);">⭐⭐⭐</font><font style="color:rgb(25, 27, 31);"> 中</font> | <font style="color:rgb(25, 27, 31);">800-2000 美金硬件</font> | <font style="color:rgb(25, 27, 31);">零云端费用、隐私优先</font> | <font style="color:rgb(25, 27, 31);">~30 分钟</font> |
| <font style="color:rgb(25, 27, 31);">Docker 容器化</font> | <font style="color:rgb(25, 27, 31);">⭐⭐⭐</font><font style="color:rgb(25, 27, 31);"> 中</font> | <font style="color:rgb(25, 27, 31);">免费 + API费用</font> | <font style="color:rgb(25, 27, 31);">隔离运行、安全优先</font> | <font style="color:rgb(25, 27, 31);">~15 分钟</font> |
| <font style="color:rgb(25, 27, 31);">阿里云轻量服务器</font> | <font style="color:rgb(25, 27, 31);">⭐⭐</font><font style="color:rgb(25, 27, 31);"> 低</font> | <font style="color:rgb(25, 27, 31);">68元/年起 + API</font> | <font style="color:rgb(25, 27, 31);">国内用户快速上手</font> | <font style="color:rgb(25, 27, 31);">~10 分钟</font> |
| <font style="color:rgb(25, 27, 31);">腾讯云 Lighthouse</font> | <font style="color:rgb(25, 27, 31);">⭐⭐</font><font style="color:rgb(25, 27, 31);"> 低</font> | <font style="color:rgb(25, 27, 31);">99元/年起 + API</font> | <font style="color:rgb(25, 27, 31);">国内用户快速上手</font> | <font style="color:rgb(25, 27, 31);">~10 分钟</font> |
| <font style="color:rgb(25, 27, 31);">DigitalOcean 1-Click</font> | <font style="color:rgb(25, 27, 31);">⭐</font><font style="color:rgb(25, 27, 31);"> 最低</font> | <font style="color:rgb(25, 27, 31);">5-12 美金/月 + API</font> | <font style="color:rgb(25, 27, 31);">海外用户一键部署</font> | <font style="color:rgb(25, 27, 31);">~5 分钟</font> |
| <font style="color:rgb(25, 27, 31);">Emergent.sh</font> | <font style="color:rgb(25, 27, 31);">⭐</font><font style="color:rgb(25, 27, 31);"> 最低</font> | <font style="color:rgb(25, 27, 31);">免费层可用</font> | <font style="color:rgb(25, 27, 31);">零配置体验</font> | <font style="color:rgb(25, 27, 31);">~5 分钟</font> |
| <font style="color:rgb(25, 27, 31);">Railway / Render</font> | <font style="color:rgb(25, 27, 31);">⭐⭐</font><font style="color:rgb(25, 27, 31);"> 低</font> | <font style="color:rgb(25, 27, 31);">0-7 美金/月 + API</font> | <font style="color:rgb(25, 27, 31);">开发者云部署</font> | <font style="color:rgb(25, 27, 31);">~8-12 分钟</font> |
| <font style="color:rgb(25, 27, 31);">macOS VM (Lume)</font> | <font style="color:rgb(25, 27, 31);">⭐⭐⭐⭐</font><font style="color:rgb(25, 27, 31);"> 高</font> | <font style="color:rgb(25, 27, 31);">0 美金（本地VM）</font> | <font style="color:rgb(25, 27, 31);">iMessage集成、完全隔离</font> | <font style="color:rgb(25, 27, 31);">~20 分钟</font> |
| <font style="color:rgb(25, 27, 31);">Cloudflare Workers</font> | <font style="color:rgb(25, 27, 31);">⭐⭐⭐⭐</font><font style="color:rgb(25, 27, 31);"> 高</font> | <font style="color:rgb(25, 27, 31);">5 美金/月起</font> | <font style="color:rgb(25, 27, 31);">无服务器、高可扩展</font> | <font style="color:rgb(25, 27, 31);">~15 分钟</font> |


:::color5
**<font style="color:#601BDE;">2.系统最低要求</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">项目</font>** | **<font style="color:rgb(25, 27, 31);">最低要求</font>** | **<font style="color:rgb(25, 27, 31);">推荐配置</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">CPU</font> | <font style="color:rgb(25, 27, 31);">2 核</font> | <font style="color:rgb(25, 27, 31);">4 核+</font> |
| <font style="color:rgb(25, 27, 31);">内存</font> | <font style="color:rgb(25, 27, 31);">2 GB</font> | <font style="color:rgb(25, 27, 31);">4-8 GB</font> |
| <font style="color:rgb(25, 27, 31);">磁盘</font> | <font style="color:rgb(25, 27, 31);">10 GB</font> | <font style="color:rgb(25, 27, 31);">40 GB+</font> |
| <font style="color:rgb(25, 27, 31);">Node.js</font> | <font style="color:rgb(25, 27, 31);">>= 22.0.0</font> | <font style="color:rgb(25, 27, 31);">最新 LTS</font> |
| <font style="color:rgb(25, 27, 31);">操作系统</font> | <font style="color:rgb(25, 27, 31);">macOS / Linux / Windows (WSL2)</font> | <font style="color:rgb(25, 27, 31);">macOS (Apple Silicon)</font> |
| <font style="color:rgb(25, 27, 31);">核心端口</font> | <font style="color:rgb(25, 27, 31);">TCP 18789</font> | <font style="color:rgb(25, 27, 31);">TCP 18789 + 80</font> |


---

## <font style="color:rgb(25, 27, 31);">四、Mac Mini 本地部署详解</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Mac Mini 是运行 OpenClaw 的理想本地硬件方案——低功耗（20-40W）、高性能、零云端费用。</font>

:::

### <font style="color:rgb(25, 27, 31);">4.1 硬件选型推荐</font>
| **<font style="color:rgb(25, 27, 31);">方案</font>** | **<font style="color:rgb(25, 27, 31);">硬件配置</font>** | **<font style="color:rgb(25, 27, 31);">价格</font>** | **<font style="color:rgb(25, 27, 31);">本地模型能力</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">预算方案</font> | <font style="color:rgb(25, 27, 31);">Mac Mini M4 (24GB)</font> | <font style="color:rgb(25, 27, 31);">约 800 美金</font> | <font style="color:rgb(25, 27, 31);">运行 7B-13B 参数模型</font> |
| <font style="color:rgb(25, 27, 31);">推荐方案</font> | <font style="color:rgb(25, 27, 31);">Mac Mini M4 Pro (64GB)</font> | <font style="color:rgb(25, 27, 31);">约 2,000 美金</font> | <font style="color:rgb(25, 27, 31);">运行 32B 参数模型，如 Qwen2.5-Coder-32B</font> |
| <font style="color:rgb(25, 27, 31);">旗舰方案</font> | <font style="color:rgb(25, 27, 31);">Mac Mini M4 Max (128GB)</font> | <font style="color:rgb(25, 27, 31);">约 3,500+ 美金</font> | <font style="color:rgb(25, 27, 31);">运行 70B+ 参数模型</font> |


**<font style="color:rgb(83, 88, 97);">性能参考</font>**<font style="color:rgb(83, 88, 97);">: GLM-4.7-Flash 在 24GB 系统上可达 15-20 tokens/秒；Qwen3-Coder-30B 在 32GB 模型上可达 10-15 tokens/秒。</font>

### <font style="color:rgb(25, 27, 31);">4.2 安装步骤</font>
:::color5
**<font style="color:#601BDE;">步骤 1：安装基础依赖</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```markdown
# 安装 Homebrew（如未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js 22+
brew install node@22

# 验证 Node.js 版本
node --version  # 应显示 v22.x.x 或更高

# （可选）安装 Ollama 用于本地模型推理
brew install ollama
```

:::color5
**<font style="color:#601BDE;">步骤 2：安装 OpenClaw</font>**

:::

```markdown
# 方式一：一键脚本（推荐）
curl -fsSL https://openclaw.ai/install.sh | bash

# 方式二：npm 全局安装
npm install -g openclaw@latest

# 方式三：从源码编译
git clone https://github.com/openclaw/openclaw.git && cd openclaw
pnpm install && pnpm ui:build && pnpm build
```

:::color5
**<font style="color:#601BDE;">步骤 3：运行配置向导</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```markdown
openclaw onboard --install-daemon
```

<font style="color:rgb(25, 27, 31);">配置向导会引导你完成：</font>

1. **<font style="color:rgb(25, 27, 31);">选择 AI 模型提供商</font>**<font style="color:rgb(25, 27, 31);">：Anthropic (Claude)、OpenAI、Google Gemini、本地 Ollama 等</font>
2. **<font style="color:rgb(25, 27, 31);">配置 API Key</font>**<font style="color:rgb(25, 27, 31);">：输入对应提供商的 API 密钥</font>
3. **<font style="color:rgb(25, 27, 31);">选择消息渠道</font>**<font style="color:rgb(25, 27, 31);">：Telegram（推荐新手）、WhatsApp、飞书等</font>
4. **<font style="color:rgb(25, 27, 31);">安装守护进程</font>**<font style="color:rgb(25, 27, 31);">：使 Gateway 作为系统服务运行</font>

:::color5
**<font style="color:#601BDE;">步骤 4：配置本地模型（零成本方案）</font>**

:::

```markdown
# 启动 Ollama
ollama serve

# 拉取推荐模型
ollama pull qwen2.5-coder:32b   # 编程优化模型
ollama pull llama3.3:70b          # 通用大模型

# 配置 OpenClaw 使用本地 Ollama
# 编辑 ~/.openclaw/openclaw.json
```

<font style="color:rgb(25, 27, 31);">在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">~/.openclaw/openclaw.json</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">中配置 Ollama：</font>

```json
{
  "agent": {
    "model": "ollama/qwen2.5-coder:32b",
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434/v1"
      }
    }
  }
}
```

:::color5
**<font style="color:#601BDE;">步骤 5：验证并启动</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```markdown
# 检查 Gateway 状态
openclaw gateway status

# 启动 Gateway
openclaw gateway start

# 打开控制面板
openclaw dashboard

# 健康检查
openclaw doctor
```

### <font style="color:rgb(25, 27, 31);">4.3 Mac Mini 7×24 小时运行配置</font>
```markdown
# 禁用睡眠
sudo pmset -a sleep 0 displaysleep 0 disksleep 0

# 使用 caffeinate 保持运行（可选）
caffeinate -d -i -s &

# 设置开机自动启动（通过 launchd）
# openclaw onboard --install-daemon 已自动完成此步骤
```

### <font style="color:rgb(25, 27, 31);">4.4 接入飞书/钉钉（国内用户）</font>
```markdown
# 飞书接入
openclaw configure
# 选择 Feishu 渠道 -> 输入 App ID 和 App Secret -> 配置 Webhook

# 钉钉接入（需创建钉钉应用）
# 1. 创建钉钉开放平台应用
# 2. 创建 AI 消息卡片
# 3. 授予 Card.Streaming.Write 和 Card.Instance.Write 权限
# 4. 创建 AppFlow 连接流
# 5. 配置 HTTP 模式机器人
```

---

## <font style="color:rgb(25, 27, 31);">五、在线虚拟机/云服务器部署详解</font>
### <font style="color:rgb(25, 27, 31);">5.1 国内云服务商方案</font>
:::color5
**<font style="color:#601BDE;">方案 A：阿里云轻量应用服务器（推荐国内用户）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">优势</font>**<font style="color:rgb(25, 27, 31);">: 预装 OpenClaw 应用镜像，一键部署</font>

```markdown
费用: 68元/年起 (2核2G + 200Mbps带宽 + 40GB磁盘)
系统: Alibaba Cloud Linux 3.2104 LTS 64位
默认地域: 美国（弗吉尼亚）
```

**<font style="color:rgb(25, 27, 31);">部署步骤</font>**<font style="color:rgb(25, 27, 31);">:</font>

1. <font style="color:rgb(25, 27, 31);">登录阿里云控制台 → 轻量应用服务器 → 选择</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">OpenClaw 应用镜像</font>**
2. <font style="color:rgb(25, 27, 31);">选择套餐（内存必须 2GiB 及以上）</font>
3. <font style="color:rgb(25, 27, 31);">进入服务器概览 → 应用详情 → 点击</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">“一键放通”</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">开启防火墙（放行端口 18789/TCP）</font>
4. <font style="color:rgb(25, 27, 31);">配置百炼 API Key（标准按量计费 或 Coding Plan 固定月费）</font>
5. <font style="color:rgb(25, 27, 31);">执行获取 Token 命令</font>
6. <font style="color:rgb(25, 27, 31);">通过 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">http://<服务器IP>:18789/?token=xxx</font>`<font style="color:rgb(25, 27, 31);"> 访问控制面板</font>

:::color5
**<font style="color:#601BDE;">方案 B：腾讯云 Lighthouse</font>**

:::

```markdown
费用: 99元/年 (2核2G + 50Mbps带宽 + 50GB)
预装: 最新版 OpenClaw (2026.2.3-1)
特点: 支持 QQ/企业微信/钉钉/飞书全接入
```

**<font style="color:rgb(25, 27, 31);">部署步骤</font>**<font style="color:rgb(25, 27, 31);">:</font>

1. <font style="color:rgb(25, 27, 31);">腾讯云控制台 → Lighthouse → AI 智能体 →</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Clawdbot/OpenClaw 模板</font>**
2. <font style="color:rgb(25, 27, 31);">选择规格（建议 2核2G 及以上）</font>
3. <font style="color:rgb(25, 27, 31);">SSH 连接后执行：</font>

```markdown
openclaw onboard        # 启动配置向导
openclaw gateway start  # 启动 Gateway
```

:::color5
**<font style="color:#601BDE;">方案 C：手动部署到任意 VPS</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">适用于已有 VPS 或非主流云商用户：</font>

```markdown
# 1. SSH 连接到服务器
ssh -i ~/pub.pem root@<server-ip>

# 2. 创建非 root 用户
adduser openclaw
usermod -aG sudo openclaw
su - openclaw

# 3. 创建 Swap 空间（2G内存建议创建4GB Swap）
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 4. 安装 Node.js 22+
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22

# 5. 安装 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 6. 运行配置向导
openclaw onboard --install-daemon

# 7. 防火墙放行
sudo ufw allow 18789/tcp
```

### <font style="color:rgb(25, 27, 31);">5.2 海外云服务商方案</font>
:::color5
**<font style="color:#601BDE;">DigitalOcean 1-Click Deploy</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```markdown
费用: 5-12 美金/月
特点: 一键部署，预配置安全镜像
支持模型: Gradient AI, OpenAI, Anthropic
```

<font style="color:rgb(25, 27, 31);">通过 DigitalOcean Marketplace 搜索 “OpenClaw” → 选择 1-Click Deploy。</font>

:::color5
**<font style="color:#601BDE;">其他平台</font>**

:::

| **<font style="color:rgb(25, 27, 31);">平台</font>** | **<font style="color:rgb(25, 27, 31);">起步价</font>** | **<font style="color:rgb(25, 27, 31);">设置时间</font>** | **<font style="color:rgb(25, 27, 31);">特点</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">Emergent.sh</font> | <font style="color:rgb(25, 27, 31);">免费层</font> | <font style="color:rgb(25, 27, 31);">~5 分钟</font> | <font style="color:rgb(25, 27, 31);">预构建 “chip”，无需终端</font> |
| <font style="color:rgb(25, 27, 31);">Hostinger VPS</font> | <font style="color:rgb(25, 27, 31);">2.99 美金/月</font> | <font style="color:rgb(25, 27, 31);">~10 分钟</font> | <font style="color:rgb(25, 27, 31);">独立 IP，99.9% SLA</font> |
| <font style="color:rgb(25, 27, 31);">Railway.app</font> | <font style="color:rgb(25, 27, 31);">0-5 美金/月</font> | <font style="color:rgb(25, 27, 31);">~8 分钟</font> | <font style="color:rgb(25, 27, 31);">需挂载持久化存储 /data</font> |
| <font style="color:rgb(25, 27, 31);">Render</font> | <font style="color:rgb(25, 27, 31);">免费-7 美金/月</font> | <font style="color:rgb(25, 27, 31);">~12 分钟</font> | <font style="color:rgb(25, 27, 31);">基础设施即代码部署</font> |
| <font style="color:rgb(25, 27, 31);">Northflank</font> | <font style="color:rgb(25, 27, 31);">5-10 美金/月</font> | <font style="color:rgb(25, 27, 31);">~7 分钟</font> | <font style="color:rgb(25, 27, 31);">一键模板 + 持久化存储</font> |
| <font style="color:rgb(25, 27, 31);">Cloudflare Workers</font> | <font style="color:rgb(25, 27, 31);">5 美金/月起</font> | <font style="color:rgb(25, 27, 31);">~15 分钟</font> | <font style="color:rgb(25, 27, 31);">无服务器、高扩展性</font> |


### <font style="color:rgb(25, 27, 31);">5.3 国内云成本对比</font>
| **<font style="color:rgb(25, 27, 31);">云厂商</font>** | **<font style="color:rgb(25, 27, 31);">价格</font>** | **<font style="color:rgb(25, 27, 31);">配置</font>** | **<font style="color:rgb(25, 27, 31);">适用场景</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">阿里云</font> | <font style="color:rgb(25, 27, 31);">68元/年</font> | <font style="color:rgb(25, 27, 31);">2核2G + 200Mbps + 40GB</font> | <font style="color:rgb(25, 27, 31);">性价比首选</font> |
| <font style="color:rgb(25, 27, 31);">腾讯云</font> | <font style="color:rgb(25, 27, 31);">99元/年</font> | <font style="color:rgb(25, 27, 31);">2核2G + 50Mbps + 50GB</font> | <font style="color:rgb(25, 27, 31);">全渠道接入</font> |
| <font style="color:rgb(25, 27, 31);">百度云</font> | <font style="color:rgb(25, 27, 31);">0.01元首月</font> | <font style="color:rgb(25, 27, 31);">2核4G + 200GB</font> | <font style="color:rgb(25, 27, 31);">试用体验</font> |
| <font style="color:rgb(25, 27, 31);">AWS</font> | <font style="color:rgb(25, 27, 31);">免费半年 + 100 美金额度</font> | <font style="color:rgb(25, 27, 31);">t3.small 2核2G + 30GB</font> | <font style="color:rgb(25, 27, 31);">海外用户</font> |


---

## <font style="color:rgb(25, 27, 31);">六、Docker 容器化部署</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Docker 部署是安全性和隔离性最好的方案，强烈推荐用于生产环境。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772710887847-b074ebf2-5629-4e98-bb22-aa3e07e26669.png)

### <font style="color:rgb(25, 27, 31);">6.1 快速启动</font>
```markdown
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 一键部署（推荐）
./docker-setup.sh

# Gateway 将运行在 http://127.0.0.1:18789/
```

`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">docker-setup.sh</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">自动完成：构建 Gateway 镜像 → 运行 Onboarding → 启动 Docker Compose → 生成认证 Token。</font>

### <font style="color:rgb(25, 27, 31);">6.2 手动 Docker Compose 部署</font>
```markdown
# 1. 构建镜像
docker build -t openclaw:local -f Dockerfile .

# 2. 运行配置向导
docker compose run --rm openclaw-cli onboard

# 3. 启动 Gateway
docker compose up -d openclaw-gateway

# 4. 获取控制面板链接
docker compose run --rm openclaw-cli dashboard --no-open

# 5. 查看并授权设备
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

### <font style="color:rgb(25, 27, 31);">6.3 环境变量配置</font>
```markdown
# 自定义系统包
export OPENCLAW_DOCKER_APT_PACKAGES="ffmpeg build-essential"

# 额外挂载目录
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro"

# 持久化 home 目录
export OPENCLAW_HOME_VOLUME="openclaw_home"

# 运行
./docker-setup.sh
```

### <font style="color:rgb(25, 27, 31);">6.4 Agent 沙箱配置</font>
<font style="color:rgb(25, 27, 31);">OpenClaw 支持为 Agent 创建隔离的 Docker 沙箱容器：</font>

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "agent",
        "workspaceAccess": "none",
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "network": "none",
          "user": "1000:1000"
        }
      }
    }
  }
}
```

**<font style="color:rgb(25, 27, 31);">沙箱镜像构建</font>**<font style="color:rgb(25, 27, 31);">:</font>

```markdown
scripts/sandbox-setup.sh              # 基础镜像
scripts/sandbox-common-setup.sh       # 含 Node, Go, Rust 等
scripts/sandbox-browser-setup.sh      # 含 Chromium CDP 浏览器
```

### <font style="color:rgb(25, 27, 31);">6.5 Docker 安全加固</font>
<font style="color:rgb(25, 27, 31);">默认安全配置：</font>

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">readOnlyRoot: true</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 只读根文件系统</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">capDrop: ["ALL"]</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 丢弃所有 Linux capabilities</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pidsLimit: 256</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 进程数限制</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">memory: "1g"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">/</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">memorySwap: "2g"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 内存限制</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">network: "none"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 无出站网络</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">seccompProfile</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">+</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">apparmorProfile</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">支持</font>
+ <font style="color:rgb(25, 27, 31);">容器以非 root 用户运行 (uid 1000)</font>

---

## <font style="color:rgb(25, 27, 31);">七、macOS 虚拟机部署（Lume）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">适合需要 </font>**<font style="color:rgb(25, 27, 31);">iMessage 集成</font>**<font style="color:rgb(25, 27, 31);"> 或 </font>**<font style="color:rgb(25, 27, 31);">完全隔离</font>**<font style="color:rgb(25, 27, 31);"> 环境的场景。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

### <font style="color:rgb(25, 27, 31);">7.1 系统要求</font>
+ <font style="color:rgb(25, 27, 31);">Apple Silicon Mac (M1/M2/M3/M4)</font>
+ <font style="color:rgb(25, 27, 31);">macOS Sequoia 或更高版本</font>
+ <font style="color:rgb(25, 27, 31);">~60GB 可用磁盘空间</font>
+ <font style="color:rgb(25, 27, 31);">~20 分钟初始设置时间</font>

### <font style="color:rgb(25, 27, 31);">7.2 部署步骤</font>
```markdown
# 1. 安装 Lume
curl -fsSL https://lume.dev/install.sh | bash

# 2. 创建 macOS 虚拟机
lume create openclaw --os macos --ipsw latest

# 3. 在 VNC 窗口完成 macOS 设置助手
#    - 启用"远程登录"(SSH)

# 4. 获取 VM IP 地址
lume get openclaw

# 5. SSH 进入 VM
ssh user@<vm-ip>

# 6. 在 VM 中安装 OpenClaw
npm install -g openclaw@latest
openclaw onboard --install-daemon

# 7. 配置渠道 (~/.openclaw/openclaw.json)
# 8. 无头运行
lume run openclaw --no-display
```

### <font style="color:rgb(25, 27, 31);">7.3 iMessage 集成（BlueBubbles）</font>
1. <font style="color:rgb(25, 27, 31);">在 VM 中安装并配置 BlueBubbles</font>
2. <font style="color:rgb(25, 27, 31);">启用 BlueBubbles Web API</font>
3. <font style="color:rgb(25, 27, 31);">配置 Webhook 指向 Gateway</font>
4. <font style="color:rgb(25, 27, 31);">在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">openclaw.json</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">中添加 BlueBubbles 渠道凭证</font>

### <font style="color:rgb(25, 27, 31);">7.4 VM 快照与恢复</font>
```markdown
# 创建金色快照（配置完成后）
lume clone openclaw openclaw-golden

# 重置 VM
lume delete openclaw
lume clone openclaw-golden openclaw
```

---

## <font style="color:rgb(25, 27, 31);">八、Token 成本深度分析</font>
:::color3
**简介：**<font style="color:rgb(83, 88, 97);">OpenClaw 的 Token 消耗可能远超预期！有用户报告一晚上”待机”就花了 18.75 美金，也有用户单日消耗 5000 万 Tokens。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

### <font style="color:rgb(25, 27, 31);">8.1 成本构成分析</font>
<font style="color:rgb(25, 27, 31);">Token 消耗的六大来源：</font>

| **<font style="color:rgb(25, 27, 31);">来源</font>** | **<font style="color:rgb(25, 27, 31);">占比</font>** | **<font style="color:rgb(25, 27, 31);">说明</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">上下文累积</font> | <font style="color:rgb(25, 27, 31);">40-50%</font> | <font style="color:rgb(25, 27, 31);">会话历史无限增长，每次请求重发全部对话</font> |
| <font style="color:rgb(25, 27, 31);">工具输出存储</font> | <font style="color:rgb(25, 27, 31);">20-30%</font> | <font style="color:rgb(25, 27, 31);">大型 JSON/日志持久化到历史文件</font> |
| <font style="color:rgb(25, 27, 31);">系统提示词</font> | <font style="color:rgb(25, 27, 31);">10-15%</font> | <font style="color:rgb(25, 27, 31);">复杂提示词重复传输，缓存 5 分钟过期</font> |
| <font style="color:rgb(25, 27, 31);">多轮推理</font> | <font style="color:rgb(25, 27, 31);">10-15%</font> | <font style="color:rgb(25, 27, 31);">复杂任务需要多次连续 API 调用</font> |
| <font style="color:rgb(25, 27, 31);">模型选择</font> | <font style="color:rgb(25, 27, 31);">5-10%</font> | <font style="color:rgb(25, 27, 31);">简单任务使用昂贵模型</font> |
| <font style="color:rgb(25, 27, 31);">心跳任务</font> | <font style="color:rgb(25, 27, 31);">5-10%</font> | <font style="color:rgb(25, 27, 31);">后台进程配置不当导致过多调用</font> |


### <font style="color:rgb(25, 27, 31);">8.2 各模型价格对比</font>
| **<font style="color:rgb(25, 27, 31);">模型</font>** | **<font style="color:rgb(25, 27, 31);">输入成本</font>** | **<font style="color:rgb(25, 27, 31);">输出成本</font>** | **<font style="color:rgb(25, 27, 31);">相对成本</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">Claude Opus 4.5</font> | <font style="color:rgb(25, 27, 31);">15 美金/百万 tokens</font> | <font style="color:rgb(25, 27, 31);">75 美金/百万 tokens</font> | <font style="color:rgb(25, 27, 31);">基线（最贵）</font> |
| <font style="color:rgb(25, 27, 31);">Claude Sonnet 4.5</font> | <font style="color:rgb(25, 27, 31);">3 美金/百万 tokens</font> | <font style="color:rgb(25, 27, 31);">15 美金/百万 tokens</font> | <font style="color:rgb(25, 27, 31);">标准</font> |
| <font style="color:rgb(25, 27, 31);">Claude Haiku 4.5</font> | <font style="color:rgb(25, 27, 31);">1 美金/百万 tokens</font> | <font style="color:rgb(25, 27, 31);">5 美金/百万 tokens</font> | <font style="color:rgb(25, 27, 31);">~Sonnet 的 1⁄3</font> |
| <font style="color:rgb(25, 27, 31);">Gemini 3.0 Flash</font> | <font style="color:rgb(25, 27, 31);">0.075 美金/百万</font> | <font style="color:rgb(25, 27, 31);">0.30 美金/百万</font> | <font style="color:rgb(25, 27, 31);">~Sonnet 的 1⁄40</font> |
| <font style="color:rgb(25, 27, 31);">Deepseek V3</font> | <font style="color:rgb(25, 27, 31);">0.27 美金/百万</font> | <font style="color:rgb(25, 27, 31);">类似</font> | <font style="color:rgb(25, 27, 31);">~Sonnet 的 1⁄11</font> |


### <font style="color:rgb(25, 27, 31);">8.3 真实用户月费基准</font>
| **<font style="color:rgb(25, 27, 31);">使用强度</font>** | **<font style="color:rgb(25, 27, 31);">月 Token 消耗</font>** | **<font style="color:rgb(25, 27, 31);">月费用</font>** | **<font style="color:rgb(25, 27, 31);">典型场景</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">轻度</font> | <font style="color:rgb(25, 27, 31);">5-20M</font> | <font style="color:rgb(25, 27, 31);">10-30 美金</font> | <font style="color:rgb(25, 27, 31);">日常问答</font> |
| <font style="color:rgb(25, 27, 31);">中度</font> | <font style="color:rgb(25, 27, 31);">20-50M</font> | <font style="color:rgb(25, 27, 31);">30-70 美金</font> | <font style="color:rgb(25, 27, 31);">自动化工作流</font> |
| <font style="color:rgb(25, 27, 31);">重度</font> | <font style="color:rgb(25, 27, 31);">50-200M</font> | <font style="color:rgb(25, 27, 31);">70-150+ 美金</font> | <font style="color:rgb(25, 27, 31);">7×24 助手</font> |
| <font style="color:rgb(25, 27, 31);">极端</font> | <font style="color:rgb(25, 27, 31);">180M+</font> | <font style="color:rgb(25, 27, 31);">3,600+ 美金</font> | <font style="color:rgb(25, 27, 31);">持续自动化</font> |


### <font style="color:rgb(25, 27, 31);">8.4 </font><font style="color:rgb(25, 27, 31);">🔴</font><font style="color:rgb(25, 27, 31);"> Token “烧钱”真实案例</font>
**<font style="color:rgb(25, 27, 31);">案例 1：18.75 美金的一夜</font>**

<font style="color:rgb(25, 27, 31);">一个简单的”心跳”检查（每 30 分钟验证一次任务是否待处理），将整个 120,000 token 上下文窗口发送到 Claude Opus API：</font>

+ <font style="color:rgb(25, 27, 31);">每次请求：~0.75 美金</font>
+ <font style="color:rgb(25, 27, 31);">一晚 25 次请求：</font>**<font style="color:rgb(25, 27, 31);">18.75 美金</font>**
+ <font style="color:rgb(25, 27, 31);">一周成本：~</font>**<font style="color:rgb(25, 27, 31);">250 美金</font>**

**<font style="color:rgb(25, 27, 31);">案例 2：11 美金/天的”待机”状态</font>**

<font style="color:rgb(25, 27, 31);">即使使用轻量级的 Gemini 3 Flash 模型处于近乎”待机”状态：</font>

+ <font style="color:rgb(25, 27, 31);">单日 Token 消耗：4000-5000 万 Tokens</font>
+ <font style="color:rgb(25, 27, 31);">单日成本：</font>**<font style="color:rgb(25, 27, 31);">11 美金</font>**

**<font style="color:rgb(25, 27, 31);">案例 3：380 美金/天的社交媒体监控</font>**

<font style="color:rgb(25, 27, 31);">Reddit 用户报告让 AI 助手仅阅读社交媒体：</font>

+ <font style="color:rgb(25, 27, 31);">每 30 分钟处理新帖：8 美金</font>
+ <font style="color:rgb(25, 27, 31);">每天成本：</font>**<font style="color:rgb(25, 27, 31);">超过 380 美金</font>**

### <font style="color:rgb(25, 27, 31);">8.5 Token 成本优化策略</font>
![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772709594131-f8f691fb-3d0a-4b10-b409-ee8b5e285205.png)

### <font style="color:rgb(25, 27, 31);">策略 1：会话重置（节省 40-60%）</font>
```json
{
  "agent": {
    "sessionReset": "after-task",
    "maxContextTokens": 50000
  }
}
```

<font style="color:rgb(25, 27, 31);">独立任务完成后重置会话，防止上下文膨胀。</font>

### <font style="color:rgb(25, 27, 31);">策略 2：智能模型路由（节省 50-80%）</font>
<font style="color:rgb(25, 27, 31);">“日常任务使用 Haiku 或 Gemini Flash，仅在复杂推理时切换到 Sonnet/Opus。”</font>

### <font style="color:rgb(25, 27, 31);">策略 3：隔离大型操作（节省 20-30%）</font>
<font style="color:rgb(25, 27, 31);">将产生大量输出的命令在独立会话中执行，防止上下文污染。</font>

### <font style="color:rgb(25, 27, 31);">策略 4：缓存优化（节省 30-50%）</font>
<font style="color:rgb(25, 27, 31);">配置低 temperature (0.2)，心跳间隔设在 TTL 限制以下，保持缓存有效。</font>

### <font style="color:rgb(25, 27, 31);">策略 5：上下文窗口限制（节省 20-40%）</font>
<font style="color:rgb(25, 27, 31);">将默认的 400K 上下文缩减到 50-100K tokens。</font>

### <font style="color:rgb(25, 27, 31);">策略 6：本地模型回退（节省 60-80%）</font>
<font style="color:rgb(25, 27, 31);">使用 Ollama + 本地模型处理简单任务，彻底消除 API 成本。</font>

### <font style="color:rgb(25, 27, 31);">🎯</font><font style="color:rgb(25, 27, 31);"> 综合优化效果</font>
<font style="color:rgb(25, 27, 31);">真实用户通过组合策略实现</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">77% 总成本降低</font>**<font style="color:rgb(25, 27, 31);">：</font>

+ <font style="color:rgb(25, 27, 31);">优化前：150 美金/月</font>
+ <font style="color:rgb(25, 27, 31);">优化后：35 美金/月</font>
+ <font style="color:rgb(25, 27, 31);">年节省：</font>**<font style="color:rgb(25, 27, 31);">1,380 美金</font>**

### <font style="color:rgb(25, 27, 31);">8.6 预算建议</font>
| **<font style="color:rgb(25, 27, 31);">预算级别</font>** | **<font style="color:rgb(25, 27, 31);">月费</font>** | **<font style="color:rgb(25, 27, 31);">策略</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">极简</font> | <font style="color:rgb(25, 27, 31);">0 美金</font> | <font style="color:rgb(25, 27, 31);">纯本地 Ollama 模型</font> |
| <font style="color:rgb(25, 27, 31);">低预算</font> | <font style="color:rgb(25, 27, 31);">10-30 美金</font> | <font style="color:rgb(25, 27, 31);">仅使用 Haiku；每日重置会话</font> |
| <font style="color:rgb(25, 27, 31);">中等</font> | <font style="color:rgb(25, 27, 31);">30-70 美金</font> | <font style="color:rgb(25, 27, 31);">Sonnet 处理复杂任务，Haiku 处理简单任务</font> |
| <font style="color:rgb(25, 27, 31);">高级</font> | <font style="color:rgb(25, 27, 31);">150+ 美金</font> | <font style="color:rgb(25, 27, 31);">全部六项策略 + 本地回退 + 供应商折扣</font> |


---

## <font style="color:rgb(25, 27, 31);">九、安全风险与漏洞全解析</font>
:::color3
**简介：**<font style="color:rgb(83, 88, 97);">⚠️</font><font style="color:rgb(83, 88, 97);"> </font>**<font style="color:rgb(83, 88, 97);">安全警告</font>**<font style="color:rgb(83, 88, 97);">: OpenClaw 的安全问题非常严重。在生产环境部署前务必充分了解并加固。</font>

:::

### <font style="color:rgb(25, 27, 31);">9.1 CVE-2026-25253：一键远程代码执行</font>
**<font style="color:rgb(25, 27, 31);">这是 OpenClaw 迄今最严重的安全漏洞。</font>**

| **<font style="color:rgb(25, 27, 31);">项目</font>** | **<font style="color:rgb(25, 27, 31);">详情</font>** |
| :--- | :--- |
| <font style="color:rgb(25, 27, 31);">CVE 编号</font> | <font style="color:rgb(25, 27, 31);">CVE-2026-25253</font> |
| <font style="color:rgb(25, 27, 31);">CVSS 评分</font> | <font style="color:rgb(25, 27, 31);">8.8（高危）</font> |
| <font style="color:rgb(25, 27, 31);">影响版本</font> | <font style="color:rgb(25, 27, 31);">2026.1.29 之前所有版本</font> |
| <font style="color:rgb(25, 27, 31);">修复版本</font> | <font style="color:rgb(25, 27, 31);">2026.1.29（2026年1月30日发布）</font> |
| <font style="color:rgb(25, 27, 31);">发现者</font> | <font style="color:rgb(25, 27, 31);">Mav Levin (DepthFirst)</font> |
| <font style="color:rgb(25, 27, 31);">公告编号</font> | <font style="color:rgb(25, 27, 31);">GHSA-g8p2-7wf7-98mq</font> |


**<font style="color:rgb(25, 27, 31);">漏洞类型</font>**<font style="color:rgb(25, 27, 31);">: Token 泄露 → 完整 Gateway 接管 → 未认证远程代码执行</font>

**<font style="color:rgb(25, 27, 31);">攻击链详解</font>**<font style="color:rgb(25, 27, 31);">:</font>

```markdown
1. 受害者点击恶意链接或访问钓鱼网站
         ↓
2. 恶意 JavaScript 获取 OpenClaw 认证 Token
   （Control UI 接受未验证的 gatewayUrl 查询参数）
         ↓
3. JavaScript 通过 WebSocket 连接受害者的 OpenClaw 实例
   （服务器未验证 WebSocket Origin 头，接受任意来源请求）
         ↓
4. 攻击者使用窃取的 Token 绕过认证
         ↓
5. 禁用用户确认 (exec.approvals.set → "off")
         ↓
6. 逃逸容器沙箱 (tools.exec.host → "gateway")
         ↓
7. 通过 node.invoke 在宿主机上执行任意命令
```

**<font style="color:rgb(25, 27, 31);">影响范围</font>**<font style="color:rgb(25, 27, 31);">:</font>

+ <font style="color:rgb(25, 27, 31);">一键远程代码执行（整个过程仅需毫秒级）</font>
+ <font style="color:rgb(25, 27, 31);">获得操作员级 Gateway API 访问权限</font>
+ <font style="color:rgb(25, 27, 31);">任意修改配置</font>
+ <font style="color:rgb(25, 27, 31);">即使绑定到 localhost 也可执行宿主机代码</font>

### <font style="color:rgb(25, 27, 31);">9.2 Moltbook 数据库暴露事件</font>
| **<font style="color:rgb(25, 27, 31);">项目</font>** | **<font style="color:rgb(25, 27, 31);">详情</font>** |
| :--- | :--- |
| <font style="color:rgb(25, 27, 31);">时间</font> | <font style="color:rgb(25, 27, 31);">2026年1月31日</font> |
| <font style="color:rgb(25, 27, 31);">项目</font> | <font style="color:rgb(25, 27, 31);">Moltbook（OpenClaw 生态社交平台）</font> |
| <font style="color:rgb(25, 27, 31);">严重性</font> | <font style="color:rgb(25, 27, 31);">高</font> |
| <font style="color:rgb(25, 27, 31);">问题</font> | <font style="color:rgb(25, 27, 31);">底层数据库配置错误，API Keys 公开可访问</font> |
| <font style="color:rgb(25, 27, 31);">影响</font> | <font style="color:rgb(25, 27, 31);">攻击者可冒充平台上任何已注册的 AI Agent（包括 Andrej Karpathy 等知名账号）</font> |


### <font style="color:rgb(25, 27, 31);">9.3 923 个网关完全暴露事件</font>
<font style="color:rgb(25, 27, 31);">通过 Shodan 扫描发现</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">923 个 OpenClaw Gateway 完全暴露在互联网上</font>**<font style="color:rgb(25, 27, 31);">：</font>

+ <font style="color:rgb(25, 27, 31);">无认证、无密码</font>
+ <font style="color:rgb(25, 27, 31);">攻击者可劫持这些实例</font>
+ <font style="color:rgb(25, 27, 31);">可提取所有存储的 API Key 和对话历史</font>
+ <font style="color:rgb(25, 27, 31);">OpenClaw 通常被授予 Shell 访问、浏览器控制等高权限</font>

### <font style="color:rgb(25, 27, 31);">9.4 恶意 VS Code 扩展事件</font>
**<font style="color:rgb(25, 27, 31);">时间</font>**<font style="color:rgb(25, 27, 31);">: 2026年1月27日</font>

<font style="color:rgb(25, 27, 31);">名为</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">“ClawdBot Agent”</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的 VS Code 扩展被发现包含</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">ScreenConnect RAT（远程访问木马）</font>**<font style="color:rgb(25, 27, 31);">。安装后攻击者可完全控制用户计算机。</font>

### <font style="color:rgb(25, 27, 31);">9.5 加密货币诈骗</font>
<font style="color:rgb(25, 27, 31);">在 Moltbot → OpenClaw 更名窗口期，出现了假冒的</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">$CLAWD 代币</font>**<font style="color:rgb(25, 27, 31);">，市值一度达到</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">1600 万美金</font>**<font style="color:rgb(25, 27, 31);">。</font>

### <font style="color:rgb(25, 27, 31);">9.6 六大安全攻击向量</font>
| **<font style="color:rgb(25, 27, 31);">攻击向量</font>** | **<font style="color:rgb(25, 27, 31);">风险等级</font>** | **<font style="color:rgb(25, 27, 31);">说明</font>** | **<font style="color:rgb(25, 27, 31);">缓解措施</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">提示词注入</font> | <font style="color:rgb(25, 27, 31);">🔴</font><font style="color:rgb(25, 27, 31);"> 高</font> | <font style="color:rgb(25, 27, 31);">所有模型都受影响，系统提示词无法完全防御</font> | <font style="color:rgb(25, 27, 31);">工具白名单、沙箱、渠道限制</font> |
| <font style="color:rgb(25, 27, 31);">跨用户泄露</font> | <font style="color:rgb(25, 27, 31);">🟡</font><font style="color:rgb(25, 27, 31);"> 中</font> | <font style="color:rgb(25, 27, 31);">默认 DM 共享同一会话</font> | <font style="color:rgb(25, 27, 31);">配置 dmScope: "per-channel-peer"</font> |
| <font style="color:rgb(25, 27, 31);">浏览器控制风险</font> | <font style="color:rgb(25, 27, 31);">🔴</font><font style="color:rgb(25, 27, 31);"> 高</font> | <font style="color:rgb(25, 27, 31);">模型可访问浏览器已登录的所有账户</font> | <font style="color:rgb(25, 27, 31);">使用专用浏览器 Profile</font> |
| <font style="color:rgb(25, 27, 31);">插件执行风险</font> | <font style="color:rgb(25, 27, 31);">🟡</font><font style="color:rgb(25, 27, 31);"> 中</font> | <font style="color:rgb(25, 27, 31);">插件在 Gateway 进程内运行</font> | <font style="color:rgb(25, 27, 31);">版本锁定、代码审查</font> |
| <font style="color:rgb(25, 27, 31);">第三方技能包</font> | <font style="color:rgb(25, 27, 31);">🔴</font><font style="color:rgb(25, 27, 31);"> 高</font> | <font style="color:rgb(25, 27, 31);">任何人可发布技能包，可能暗藏钓鱼代码</font> | <font style="color:rgb(25, 27, 31);">仅安装可信来源、审查代码</font> |
| <font style="color:rgb(25, 27, 31);">Token URL 泄露</font> | <font style="color:rgb(25, 27, 31);">🔴</font><font style="color:rgb(25, 27, 31);"> 极高</font> | <font style="color:rgb(25, 27, 31);">包含认证凭据的完整 URL 泄露 = 管理员权限被盗</font> | <font style="color:rgb(25, 27, 31);">妥善保管、定期轮换</font> |


### <font style="color:rgb(25, 27, 31);">9.7 真实受害案例</font>
<font style="color:rgb(83, 88, 97);">有用户反映 OpenClaw 在执行”清理任务”时，</font>**<font style="color:rgb(83, 88, 97);">误删了电脑中所有重要照片</font>**<font style="color:rgb(83, 88, 97);">。</font>

<font style="color:rgb(25, 27, 31);">这个案例说明：</font>

+ <font style="color:rgb(25, 27, 31);">AI Agent 拥有的系统权限必须严格限制</font>
+ <font style="color:rgb(25, 27, 31);">人工确认机制对于破坏性操作至关重要</font>
+ <font style="color:rgb(25, 27, 31);">沙箱隔离是保护主系统的最后防线</font>

---

<font style="color:rgb(25, 27, 31);">  
</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772709593847-5142fbe5-1b45-4cd6-a1f1-7c849046c3b7.png)

## <font style="color:rgb(25, 27, 31);">十、官方安全解决方案</font>
### <font style="color:rgb(25, 27, 31);">10.1 认证加固（v2026.1.29 重大变更）</font>
`**<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">auth: "none"</font>**`**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">模式已被永久移除。</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">所有实例必须使用以下认证方式之一：</font>

```json
// 方式一：Token 认证（推荐）
{
  "gateway": {
    "auth": "token"
  }
}

// 方式二：密码认证
{
  "gateway": {
    "auth": "password"
  }
}

// 方式三：Tailscale Serve 身份认证
```

### <font style="color:rgb(25, 27, 31);">10.2 DM 访问策略</font>
<font style="color:rgb(25, 27, 31);">OpenClaw 支持四种 DM 策略：</font>

| **<font style="color:rgb(25, 27, 31);">策略</font>** | **<font style="color:rgb(25, 27, 31);">说明</font>** | **<font style="color:rgb(25, 27, 31);">推荐场景</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">pairing（默认）</font> | <font style="color:rgb(25, 27, 31);">未知发送者收到限时配对码</font> | <font style="color:rgb(25, 27, 31);">个人使用</font> |
| <font style="color:rgb(25, 27, 31);">allowlist</font> | <font style="color:rgb(25, 27, 31);">完全阻止未知发送者</font> | <font style="color:rgb(25, 27, 31);">企业/生产环境</font> |
| <font style="color:rgb(25, 27, 31);">open</font> | <font style="color:rgb(25, 27, 31);">允许任何人（需显式 "*" 白名单）</font> | <font style="color:rgb(25, 27, 31);">不推荐</font> |
| <font style="color:rgb(25, 27, 31);">disabled</font> | <font style="color:rgb(25, 27, 31);">忽略所有入站 DM</font> | <font style="color:rgb(25, 27, 31);">仅群组模式</font> |


### <font style="color:rgb(25, 27, 31);">10.3 沙箱隔离架构</font>
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "agent",
        "workspaceAccess": "none",
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "network": "none",
          "user": "1000:1000"
        }
      }
    }
  }
}
```

**<font style="color:rgb(25, 27, 31);">工作区访问控制</font>**<font style="color:rgb(25, 27, 31);">:</font>

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">workspaceAccess: "none"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— Agent 工作区不可访问（最安全）</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">workspaceAccess: "ro"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 只读挂载到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">/agent</font>`
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">workspaceAccess: "rw"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 完全读写访问</font>

**<font style="color:rgb(25, 27, 31);">会话隔离</font>**<font style="color:rgb(25, 27, 31);">:</font>

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">dmScope: "main"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 所有 DM 共享一个会话（默认，有跨用户泄露风险）</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">dmScope: "per-channel-peer"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 每个发送者+渠道对隔离</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">dmScope: "per-account-channel-peer"</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">— 多账户进一步隔离</font>

### <font style="color:rgb(25, 27, 31);">10.4 安全审计工具</font>
```markdown
# 基本审计
openclaw security audit

# 深度审计（含 Gateway 实时探测）
openclaw security audit --deep

# 自动修复安全配置
openclaw security audit --fix
```

<font style="color:rgb(25, 27, 31);">审计检测项目：</font>

+ <font style="color:rgb(25, 27, 31);">DM/群组策略配置错误</font>
+ <font style="color:rgb(25, 27, 31);">开放房间中的过高工具权限</font>
+ <font style="color:rgb(25, 27, 31);">网络暴露（LAN 绑定、Funnel、弱认证）</font>
+ <font style="color:rgb(25, 27, 31);">浏览器控制远程暴露</font>
+ <font style="color:rgb(25, 27, 31);">凭据/配置/状态的文件权限问题</font>
+ <font style="color:rgb(25, 27, 31);">未签名插件</font>
+ <font style="color:rgb(25, 27, 31);">过时模型配置</font>

### <font style="color:rgb(25, 27, 31);">10.5 网络安全加固清单</font>
```markdown
# ✅ 使用 loopback 绑定（默认）
gateway.bind: "loopback"

# ✅ 远程访问优先使用 Tailscale Serve
# ❌ 永远不要在 0.0.0.0 上暴露未认证的 Gateway

# ✅ 配置反向代理时设置可信代理
gateway.trustedProxies: ["10.0.0.1"]

# ✅ mDNS 设为最小模式
discovery.mdns.mode: "minimal"

# ✅ 全盘加密
# ✅ 专用 OS 用户账户
# ✅ 日志中的敏感模式脱敏
logging.redactPatterns: ["sk-*", "Bearer *"]
```

### <font style="color:rgb(25, 27, 31);">10.6 多 Agent 安全分级</font>
```json
{
  "agents": {
    "personal": {
      "sandbox": { "mode": "off" },
      "tools": ["*"]
    },
    "family": {
      "sandbox": { "mode": "always" },
      "tools": ["messaging", "calendar"],
      "workspaceAccess": "ro"
    },
    "public": {
      "sandbox": { "mode": "always" },
      "tools": ["messaging"],
      "workspaceAccess": "none"
    }
  }
}
```

### <font style="color:rgb(25, 27, 31);">10.7 事件响应流程</font>
**<font style="color:rgb(25, 27, 31);">发现异常后的紧急处理</font>**<font style="color:rgb(25, 27, 31);">:</font>

**<font style="color:rgb(25, 27, 31);">立即遏制</font>**<font style="color:rgb(25, 27, 31);">:</font>

```markdown
# 停止 Gateway openclaw gateway stop 
# 限制为 loopback gateway.bind: "loopback" 
# 禁用公网访问
```

**<font style="color:rgb(25, 27, 31);">轮换凭据</font>**<font style="color:rgb(25, 27, 31);">:</font>

    - <font style="color:rgb(25, 27, 31);">Gateway 认证 Token/密码</font>
    - <font style="color:rgb(25, 27, 31);">远程客户端凭据</font>
    - <font style="color:rgb(25, 27, 31);">所有 Provider/API 凭据</font>

```markdown
调查:
# 查看 Gateway 日志 cat /tmp/openclaw/openclaw-YYYY-MM-DD.log 

# 分析会话记录中的异常工具调用 

# 检查未授权的插件/配置变更
# 报告漏洞: security@openclaw.ai
```

---

## <font style="color:rgb(25, 27, 31);">十一、参考资源</font>
### <font style="color:rgb(25, 27, 31);">英文资源</font>
1. [<font style="color:rgb(9, 64, 142);">Getting Started - OpenClaw Official Docs</font>](https://link.zhihu.com/?target=https%3A//docs.openclaw.ai/start/getting-started)
2. [<font style="color:rgb(9, 64, 142);">Unleashing OpenClaw: Ultimate Guide to Local AI Agents - DEV Community</font>](https://link.zhihu.com/?target=https%3A//dev.to/mechcloud_academy/unleashing-openclaw-the-ultimate-guide-to-local-ai-agents-for-developers-in-2026-3k0h)
3. [<font style="color:rgb(9, 64, 142);">OpenClaw Tutorial: Installation to First Chat Setup - Codecademy</font>](https://link.zhihu.com/?target=https%3A//www.codecademy.com/article/open-claw-tutorial-installation-to-first-chat-setup)
4. [<font style="color:rgb(9, 64, 142);">What is OpenClaw: Open-Source AI Agent in 2026 - Medium</font>](https://link.zhihu.com/?target=https%3A//medium.com/%40gemQueenx/what-is-openclaw-open-source-ai-agent-in-2026-setup-features-8e020db20e5e)
5. [<font style="color:rgb(9, 64, 142);">OpenClaw Complete Guide 2026 - NxCode</font>](https://link.zhihu.com/?target=https%3A//www.nxcode.io/resources/news/openclaw-complete-guide-2026)
6. [<font style="color:rgb(9, 64, 142);">What is OpenClaw? Your Open-Source AI Assistant - DigitalOcean</font>](https://link.zhihu.com/?target=https%3A//www.digitalocean.com/resources/articles/what-is-openclaw)
7. [<font style="color:rgb(9, 64, 142);">Install OpenClaw in 5 Minutes - OpenClawAGI</font>](https://link.zhihu.com/?target=https%3A//openclawagi.com/install-openclaw-in-5-minutes-fast-secure-setup-guide-2026/)
8. [<font style="color:rgb(9, 64, 142);">Set Up OpenClaw in Minutes: 6 Easy Deployment Options - The Tool Nerd</font>](https://link.zhihu.com/?target=https%3A//www.thetoolnerd.com/p/set-up-openclawclawdbot-in-minutes)
9. [<font style="color:rgb(9, 64, 142);">How to Run OpenClaw - DigitalOcean Community</font>](https://link.zhihu.com/?target=https%3A//www.digitalocean.com/community/tutorials/how-to-run-openclaw)
10. [<font style="color:rgb(9, 64, 142);">OpenClaw Token Cost Optimization Guide - APIYI</font>](https://link.zhihu.com/?target=https%3A//help.apiyi.com/en/openclaw-token-cost-optimization-guide-en.html)

### <font style="color:rgb(25, 27, 31);">中文资源</font>
1. [<font style="color:rgb(9, 64, 142);">部署OpenClaw镜像并构建钉钉AI员工 - 阿里云文档</font>](https://link.zhihu.com/?target=https%3A//help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)
2. [<font style="color:rgb(9, 64, 142);">一文读懂：openClaw 分析与教程 - 知乎</font>](https://zhuanlan.zhihu.com/p/2000850539936765122)
3. [<font style="color:rgb(9, 64, 142);">OpenClaw安装部署及国产平替实在Agent - AI-Indeed</font>](https://link.zhihu.com/?target=https%3A//www.ai-indeed.com/article/15272.html)
4. [<font style="color:rgb(9, 64, 142);">OpenClaw (Clawdbot) 教程 - 菜鸟教程</font>](https://link.zhihu.com/?target=https%3A//www.runoob.com/ai-agent/openclaw-clawdbot-tutorial.html)
5. [<font style="color:rgb(9, 64, 142);">0元搭建7×24h AI助手 OpenClaw云部署完全指南 - DEV Community</font>](https://link.zhihu.com/?target=https%3A//dev.to/yang_ella_f2a3e16ccb54550/0yuan-da-jian-7x24h-aizhu-shou-openclawyun-fu-wu-qi-bu-shu-wan-quan-zhi-nan-5hlf)
6. [<font style="color:rgb(9, 64, 142);">2026年OpenClaw极速部署教程及常见问题 - 阿里云开发者社区</font>](https://link.zhihu.com/?target=https%3A//developer.aliyun.com/article/1710373)
7. [<font style="color:rgb(9, 64, 142);">手把手教你部署OpenClaw - 博客园</font>](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/whuanle/p/19558535)
8. [<font style="color:rgb(9, 64, 142);">openclaw-cn 中文版 - GitHub</font>](https://link.zhihu.com/?target=https%3A//github.com/jiulingyun/openclaw-cn)
9. [<font style="color:rgb(9, 64, 142);">OpenClaw Mac Mini完全指南 - Marc0.dev</font>](https://link.zhihu.com/?target=https%3A//www.marc0.dev/en/blog/openclaw-mac-mini-the-complete-guide-to-running-your-own-ai-agent-in-2026-1770057455419)
10. [<font style="color:rgb(9, 64, 142);">OpenClaw 18.75 美金一夜成本分析 - Notebookcheck</font>](https://link.zhihu.com/?target=https%3A//www.notebookcheck-cn.com/18-75-OpenClaw.1220271.0.html)

### <font style="color:rgb(25, 27, 31);">安全相关资源</font>
1. [<font style="color:rgb(9, 64, 142);">CVE-2026-25253 详情 - GHSA-g8p2-7wf7-98mq</font>](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw/security/advisories/GHSA-g8p2-7wf7-98mq)
2. [<font style="color:rgb(9, 64, 142);">OpenClaw 安全最佳实践</font>](https://link.zhihu.com/?target=https%3A//docs.openclaw.ai/security)
3. [<font style="color:rgb(9, 64, 142);">The Register: OpenClaw Security Issues</font>](https://link.zhihu.com/?target=https%3A//www.theregister.com/2026/02/02/openclaw_security_issues/)
4. <font style="color:rgb(25, 27, 31);">漏洞报告邮箱：</font>[security@openclaw.ai](mailto:security@openclaw.ai)

### <font style="color:rgb(25, 27, 31);">官方资源</font>
1. [<font style="color:rgb(9, 64, 142);">GitHub 仓库</font>](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw)
2. [<font style="color:rgb(9, 64, 142);">官方文档</font>](https://link.zhihu.com/?target=https%3A//docs.openclaw.ai/)
3. [<font style="color:rgb(9, 64, 142);">中文文档</font>](https://link.zhihu.com/?target=https%3A//clawd.org.cn/docs/start/getting-started)
4. [<font style="color:rgb(9, 64, 142);">中文版仓库</font>](https://link.zhihu.com/?target=https%3A//github.com/jiulingyun/openclaw-cn)

  


