# ③ Claw-R1: 迈向Runtime RL的Agentic范式

<!-- source: yuque://zhongxian-iiot9/hlyypb/ov7mrygcgff3gtyg -->

:::color3
**简介：**Claw-R1 是由 Agent-R1 团队于 2026 年 3 月发布的**<font style="color:#ED740C;">先进强化学习（Agentic RL）训练框架</font>**，专为通用 AI 智能体设计，标志着大模型强化学习正式迈向**<font style="color:#ED740C;">基于真实环境交互的 Runtime RL</font>** 阶段。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775045199371-b9930d27-78c6-4308-ab4a-908b0303c2e9.png)

:::color5
**<font style="color:#601bde;">1. 核心定位与开源信息</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">Claw-R1 是一款专为通用 AI 智能体（General Agents，例如 OpenClaw、Claude Code 等）量身定制的先进强化学习（Agentic RL）训练框架。该框架由中国科大认知智能全国重点实验室相关背景的 Agent-R1 团队研发。</font>**

+ **开源地址**：[https://github.com/AgentR1/Claw-R1](https://link.zhihu.com/?target=https%3A//github.com/AgentR1/Claw-R1)
+ **相关论文**：《OpenClaw-RL: Train Any Agent Simply by Talking》

:::color5
**<font style="color:#601bde;">2. 发展阶段与技术演进</font>**

:::

**<font style="color:#74B602;">作为上一代 Agent-R1 的演进版本，Claw-R1 的核心架构本质上是构建了一座连接“智能体运行环境（Agent Runtime）”与“大模型强化学习底层”的桥梁。</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775045210689-a3a1072a-4d38-42c1-8e7b-029d63e874d9.png)

这一框架的发布具有里程碑意义，标志着大模型强化学习的范式正在发生深刻变革：

+ **第一代**：基于人类偏好的强化学习（[RLHF](https://zhida.zhihu.com/search?content_id=271572557&content_type=Article&match_order=1&q=RLHF&zhida_source=entity)）。
+ **第二代**：基于可验证任务的强化学习（[RLVR](https://zhida.zhihu.com/search?content_id=271572557&content_type=Article&match_order=1&q=RLVR&zhida_source=entity)，例如数学题求解）。
+ **第三代**：正式迈向基于真实环境交互的运行时强化学习（[Runtime RL](https://zhida.zhihu.com/search?content_id=271572557&content_type=Article&match_order=1&q=Runtime+RL&zhida_source=entity)）。

# **Claw-R1 核心价值与应用场景**
:::color3
**简介：**Claw-R1 的核心价值在于赋能 AI 智能体在真实运行环境中**<font style="color:#ED740C;">实现“边用边学”的自我进化</font>**，涵盖自动训练、个性化定制及复杂任务处理等核心应用场景。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775135221670-bb093425-b38d-4995-ba23-939d50a642cd.png)

:::color5
**<font style="color:#601bde;">1. 零人工标注的自动训练</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">系统具备高度自动化的信号转化能力，能够将用户的多轮交互记录、工具调用结果、终端报错信息或 GUI 界面的状态变化，自动提取并转化为“下一状态信号（Next-State Signal）”。</font>**

这些信号随后被转换为模型训练所需的奖励（Reward）和梯度（Gradient），从而彻底免除了传统训练中对人工数据标注的依赖。

:::color5
**<font style="color:#601bde;">2. 训练个性化智能体 (Personal Agents)</font>**

:::

**<font style="color:#74B602;">Claw-R1 支持通过自然交互实现模型的个性化微调。</font>**

用户仅需保持日常的对话习惯（例如纠正智能体的错误或提出新的业务要求），系统即可在后台自动提取这些隐式反馈以优化执行策略，真正实现了“仅通过交谈即可训练任何智能体”的愿景。

:::color5
**<font style="color:#601bde;">3. 强化复杂真实世界任务的执行能力</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

该框架成功将强化学习的应用边界拓展至终端命令行、GUI 图形界面操作、软件工程（SWE）以及复杂的工具调用场景中。

<font style="background-color:#FBDFEF;">通过在真实环境中的持续探索与反馈，Claw-R1 显著提升了模型学习并执行长序列、高难度真实世界任务的综合能力。</font>

# **Claw-R1 架构创新与核心技术**
:::color3
**简介：**Claw-R1 针对复杂智能体训练的痛点，提出了**<font style="color:#ED740C;">基于中间件的解耦架构、全异步训练机制、统一状态信号恢复及大规模环境并行支持</font>**等四大核心技术创新。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1775045266544-8b053851-8fcb-4542-ac55-1febec1b2284.png)

:::color5
**<font style="color:#601bde;">1. 基于中间件的解耦架构 (Middleware-based Architecture)</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">这是 Claw-R1 最具突破性的工程创新。为实现对现有“黑盒”智能体（如开源智能体 OpenClaw）的直接训练，框架引入了 Gateway（网关服务器） 与 DataPool（数据缓冲池） 的中间层设计：</font>**

+ **零代码侵入性**：开发者无需对智能体自身的复杂业务逻辑代码进行任何修改，**仅需将智能体调用 LLM 的 API 地址（Base URL）重定向至 Claw-R1 的 Gateway 即可**。
+ **透明拦截与记录**：Gateway 充当透明代理，负责拦截交互请求并转发给后端推理引擎，同时将执行轨迹（Trajectory）与环境反馈异步存入 DataPool，以供后续训练调用。

:::color5
**<font style="color:#601bde;">2. 全异步的训练与服务机制 (Asynchronous Training & Serving)</font>**

:::

**<font style="color:#74B602;">有别于传统强化学习训练常需中断服务的局限，Claw-R1 实现了生成引擎（Rollout Engine，如 </font>**[**<font style="color:#74B602;">vLLM</font>**](https://zhida.zhihu.com/search?content_id=271572557&content_type=Article&match_order=1&q=vLLM&zhida_source=entity)**<font style="color:#74B602;">）与训练引擎（Training Engine，如 </font>**[**<font style="color:#74B602;">PPO 算法</font>**](https://zhida.zhihu.com/search?content_id=271572557&content_type=Article&match_order=1&q=PPO+%E7%AE%97%E6%B3%95&zhida_source=entity)**<font style="color:#74B602;">）的完全异步运行。  
</font>**智能体在前端与用户或环境保持实时交互，而训练引擎则在后台的高性能 GPU 集群上，持续从 DataPool 拉取数据进行模型权重更新。两者进程互不阻塞，真正达成了“在线持续学习”的目标。

:::color5
**<font style="color:#601bde;">3. 统一的下一状态信号恢复机制 (Next-State Signal Recovery)</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">在算法理论层面，Claw-R1（及其依托的 OpenClaw-RL 理论）将各类异构反馈信号统一整合至标准训练循环中，并提出了两项互补的关键技术：</font>**

+ **二元强化学习 (Binary RL) 与多数投票 PRM**：将评估性反馈（如用户的否定评价、终端报错）转化为标量化的**过程奖励（Process Rewards）**。系统内置了基于多数投票机制的自动化过程裁判（PRM/Judge），以确保打分的稳健性与准确性。
+ **后见之明引导的同策略蒸馏 (OPD, On-policy Distillation)**：将指令性反馈（如用户明确指示“应先执行命令 A 再执行 B”）转化为 Token 级别的优势监督信号，从而直接从用户的纠正行为中提取并蒸馏出最优策略。

:::color5
**<font style="color:#601bde;">4. 大规模环境并行支持</font>**

:::

<font style="background-color:#FBDFEF;">依托底层强大的分布式计算引擎（如整合了 </font>[<font style="background-color:#FBDFEF;">Ray</font>](https://zhida.zhihu.com/search?content_id=271572557&content_type=Article&match_order=1&q=Ray&zhida_source=entity)<font style="background-color:#FBDFEF;"> 等分布式框架），Claw-R1 能够支持在海量的终端、GUI 或开发环境中并发执行智能体轨迹。这一特性为 Agentic RL 提供了卓越的数据吞吐量与算力调度保障。</font>

# **Claw-R1 实战使用模拟与进阶指南**
:::color3
**简介：**以开源 Agent 框架 OpenClaw 为例，展示如何**<font style="color:#ED740C;">利用 Claw-R1 的“零代码侵入”特性，在真实环境中对大模型进行 Runtime RL 后训练</font>**，并提供实战避坑与进阶建议。

:::

:::color5
**<font style="color:#601bde;">实战场景：在 OpenClaw 真实环境中训练大模型</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">利用 Claw-R1 对开源 Agent 框架（如 GitHub 热门项目 OpenClaw）底层驱动的大模型进行后训练（Post-training），是 Runtime RL（运行时强化学习） 的经典应用场景。</font>**

**OpenClaw** 是一款基于 TypeScript 实现的开源个人 AI Agent 操作系统，支持接入微信、Slack、Discord 等消息平台并调用本地工具库。  
**核心目标**：使大模型在为 OpenClaw 提供真实业务服务的同时，能够根据用户反馈与任务执行状态进行自我迭代（“边用边学”）。  
**核心优势**：**“零代码侵入 (Zero-code intrusion)”**。无需修改开源 Agent 的复杂业务逻辑代码，仅需将其调用大模型的 API 接口重定向至 Claw-R1 的网关。

<font style="background-color:#FBDFEF;">以下为使用开源大模型（如 Qwen/Llama 系列）作为基座，在 OpenClaw 真实环境中进行 PPO 强化学习后训练的完整步骤。</font>

:::color5
**<font style="color:#601bde;">第 1 步：准备环境与依赖包</font>**

:::

**<font style="color:#74B602;">Claw-R1 底层依赖字节跳动开源的大规模强化学习框架 </font>**`**<font style="color:#74B602;">verl</font>**`**<font style="color:#74B602;"> 以及分布式计算框架 </font>**`**<font style="color:#74B602;">Ray</font>**`**<font style="color:#74B602;">。需在 GPU 训练服务器上完成以下环境配置：</font>**

```bash
# 1. 创建虚拟环境
conda create -n clawr1 python=3.10 -y
conda activate clawr1

# 2. 安装底层 RL 引擎 verl
git clone https://github.com/volcengine/verl && cd verl
pip install --no-deps -e .
cd ..

# 3. 下载并安装 Claw-R1 框架
git clone https://github.com/AgentR1/Claw-R1 && cd Claw-R1
pip install -e .

# 4. 安装周边依赖（分布式调度引擎、API 服务等）
pip install "ray[default]" fastapi uvicorn vllm
```

:::color5
**<font style="color:#601bde;">第 2 步：启动 Claw-R1 的异步训练集群</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">在具备充足显存的训练服务器（如多张 A100/H800 GPU）上，执行 Claw-R1 提供的一键启动脚本，拉起异步训练网络：</font>**

```bash
# 启动异步 PPO 训练与网关服务
python -m claw_r1.async_main \
    --config-name async_ppo_trainer \
    trainer.model.path=/path/to/your/base_model \
    trainer.ppo.reward_model_path=/path/to/your/reward_model
```

执行上述命令后，后台将自动启动以下 5 个核心组件：

1. **Ray Cluster**：负责自动分配与调度多卡 GPU 资源池。
2. **DataPool (数据缓冲池)**：负责接收并存储从 Agent 端持续回传的运行轨迹数据。
3. **AsyncRollouter (生成引擎)**：内部启动 vLLM 实例，负责提供极速的模型推理与回复生成。
4. **AsyncTrainer (训练引擎)**：负责启动并维护 PPO（近端策略优化）的训练循环。
5. **Gateway (网关服务)**：启动兼容 OpenAI 格式的 FastAPI 代理服务，**默认监听于 **`8100`** 端口**。

:::color5
**<font style="color:#601bde;">第 3 步：修改开源 Agent (OpenClaw) 的配置</font>**

:::

**<font style="color:#74B602;">在运行 OpenClaw 的宿主机（如 Mac Mini 或独立服务器）上，定位大模型配置文件（通常为 </font>**`**<font style="color:#74B602;">.env</font>**`**<font style="color:#74B602;"> 或 </font>**`**<font style="color:#74B602;">config.json</font>**`**<font style="color:#74B602;">）。</font>**

将原指向 OpenAI 或第三方 API 的地址，**重定向至 Claw-R1 的 Gateway 地址**。这是整个流程中唯一的代码/配置修改步骤，无需触及 OpenClaw 内部的多层记忆、并发队列（Lane Queue）或工具调用逻辑。

**修改前配置示例：**

```plain
LLM_API_BASE="https://api.openai.com/v1"
LLM_API_KEY="sk-xxxxxx"
LLM_MODEL="gpt-4o"
```

**修改后配置示例：**

```plain
# 将 IP 替换为运行 Claw-R1 训练集群的服务器 IP
LLM_API_BASE="http://<your-clawr1-server-ip>:8100/v1"
LLM_API_KEY="xxx" # 可任意填写
LLM_MODEL="your-base-model-name"
```

:::color5
**<font style="color:#601bde;">第 4 步：在真实环境中运行，开启“自驱动强化学习”</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">配置完成后，正常启动并使用 OpenClaw。系统将自动进入以下闭环学习状态：</font>**

1. **用户下达任务**：用户通过微信或终端向 OpenClaw 发送指令（如：“帮我查一下昨天关于 Claw-R1 的邮件并总结”）。
2. **透明拦截生成**：OpenClaw 组装 Prompt 并发起 LLM 请求。该请求被路由至 Claw-R1 的 **Gateway**，Gateway 迅速将其转发至后端的 vLLM，并将生成的规划动作返回给 OpenClaw 执行。
3. **环境交互与异步入池**：OpenClaw 根据模型指令执行邮件搜索。若执行过程中发生报错，或用户反馈结果有误，完整的交互序列（Trajectory + Reward Signal）将被 Gateway **异步记录并存入 DataPool**。
4. **后台静默训练**：在 GPU 服务器端，**AsyncTrainer** 持续监控 DataPool。当收集到足够批次的数据（例如 128 条完整轨迹）时，将在后台静默执行一次 PPO 梯度更新。
5. **热更新权重 (Parameter Synchronizer)**：训练引擎完成参数更新后，会自动将最新权重通过内存同步机制下发给 vLLM 生成引擎。

<font style="background-color:#FBDFEF;">经过上述闭环，当用户再次发起类似任务时，提供推理服务的模型已是吸收了历史错误经验并完成迭代优化的升级版本。</font>

:::color5
**<font style="color:#601bde;">实战避坑提示与进阶</font>**

:::

**<font style="color:#74B602;">在实际部署与应用中，需关注以下关键技术点：</font>**

+ **Reward（奖励）机制的设计**：真实环境中缺乏显式的人工评分。Claw-R1 通常采用基于规则的**隐式奖励**（例如：终端未输出 `Error` 计 +1 分，任务最终标记为 `Resolved` 计 +10 分），或挂载轻量级的 Reward Model（奖励模型）作为裁判（Judge）对轨迹进行自动化评估。
+ **黑盒 Trajectory 的完整性保障**：鉴于 OpenClaw 的黑盒特性，大模型仅负责文本补全。在最新的 Claw-R1 架构中，网关需通过关联同一 `session_id` 的请求，精准拼接多轮工具调用的完整轨迹，以确保 PPO 算法能够正确计算优势函数（Advantage）。
+ **硬件算力要求**：异步强化学习（Asynchronous RL）模式需同时维持庞大的显存开销（vLLM 占用显存用于推理，Trainer 占用显存用于存储优化器状态与梯度）。建议基础硬件配置不低于 4x A100 (80GB) 级别的 GPU 算力集群。

:::color5
**<font style="color:#601bde;">Claw-R1总结</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

**<font style="color:#74B602;">Claw-R1 代表了当前 Agentic AI 领域极其前沿的基础设施技术。</font>**

<font style="background-color:#FBDFEF;">该框架巧妙运用“中间件代理”的设计理念，将复杂的强化学习引擎无缝挂载至任何成熟的智能体系统中，从而赋予了 AI 在真实世界中实现**“落地应用 -> 试错反馈 -> 闭环自我学习”**的完整进化能力。</font>

