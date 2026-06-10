# ⑮ Qwen3.5 微调实战：从训练到部署

<!-- source: yuque://zhongxian-iiot9/hlyypb/ysmpfqpysbgr8itp -->

:::color3
**简介：**通义千问 Qwen 团队正式发布 **<font style="color:#D22D8D;">Qwen3.5 系列</font>**，并开源其首款**<font style="color:#ED740C;">原生视觉-语言模型 Qwen3.5-397B-A17B</font>**，该模型以创新的稀疏混合专家架构，在显著降低推理成本的同时，实现了与万亿级模型相媲美的性能。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475377772-bd15982c-9e55-42b3-98be-60d6193849e1.png)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475483674-58744dae-8572-44ba-9961-53b7e0abb4dc.png)

:::color5
**<font style="color:#601bde;">1. 模型发布概览</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:#74B602;">通义千问 Qwen 团队于除夕夜发布了 Qwen3.5 系列，并同步开源其首款权重模型 Qwen3.5-397B-A17B</font>**

Qwen3.5-397B-A17B 是一款**<font style="color:#117CEE;">原生视觉-语言模型（Native Multimodality）</font>**。该模型在保持 3970 亿总参数规模的同时，通过创新的架构设计将单次激活参数量控制在 170 亿。这一设计使得开发者能够以更低的推理成本，获得比肩甚至超越万亿级（1T+）模型的性能体验。

:::color5
**<font style="color:#601bde;">2. 架构创新：Gated DeltaNet 与 MoE 的融合</font>**<font style="color:#D22D8D;"></font>

:::

**<font style="color:#74B602;">模型基于 Qwen3-Next 架构，创新性地将线性注意力机制与稀疏混合专家架构（MoE）相结合。</font>**

+ **<font style="background-color:#D9EAFC;">混合注意力机制</font>**<font style="background-color:#D9EAFC;">：</font>引入 Gated DeltaNet + Gated Attention，在提升模型长文本建模能力的同时，优化了计算稳定性。
+ **<font style="background-color:#D9EAFC;">高稀疏度 MoE</font>**<font style="background-color:#D9EAFC;">：</font>通过提高专家网络的稀疏度，在保证性能的前提下大幅降低了计算冗余。

<font style="background-color:#FBDFEF;">这种混合架构设计，是其在 BFCL-V4、VITA-Bench、DeepPlanning 等全方位基准评测中表现优异的底层逻辑。</font>

:::color5
**<font style="color:#601bde;">3. 模型资源</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

+ **Github**：[https://github.com/QwenLM/Qwen3.5](https://github.com/QwenLM/Qwen3.5)
+ **ModelScope**：[https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B](https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B)
+ **Blog**：[https://qwen.ai/blog?id=qwen3.5](https://qwen.ai/blog?id=qwen3.5)
+ **Qwenchat 体验**：[https://chat.qwen.ai/](https://chat.qwen.ai/)



# **环境准备**
:::color3
**简介：**本章节详细说明**<font style="color:#ED740C;"> Qwen3.5 多卡微调所需的环境配置步骤</font>**，包括 Conda 环境创建、核心依赖安装及安装结果验证，相关配置均已在实际项目中验证通过。

:::

:::color5
**<font style="color:#601bde;">1. 创建 Conda 环境</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">为确保环境隔离与依赖清晰，建议首先创建一个新的 Conda 环境并激活。</font>**

```bash
# 创建新环境
conda create -n swift python=3.11 -y
# 激活环境
conda activate swift
```

:::color5
**<font style="color:#601bde;">2. 安装核心依赖</font>**

:::

**<font style="color:#74B602;">根据官方文档要求，Qwen3.5 的微调需要安装以下核心依赖包。请按顺序执行安装命令。</font>**

```bash
# 安装包管理工具 uv
pip install uv
# 安装 MS-SWIFT 框架
uv pip install -U ms-swift
# 安装 Transformers 及相关基础库
uv pip install -U "transformers==5.2.0" "qwen_vl_utils>=0.0.14" peft liger-kernel
# 安装 Flash-Linear-Attention（需从 main 分支安装）
uv pip install -U git+https://github.com/fla-org/flash-linear-attention
# 安装 Causal-Conv1d
pip install -U git+https://github.com/Dao-AILab/causal-conv1d --no-build-isolation
# 安装 Flash-Attention（可选步骤，安装耗时约3小时，不安装亦可进行训练，建议跳过）
uv pip install "flash-attn==2.8.3" --no-build-isolation
# 安装 DeepSpeed（多卡训练的必要依赖）
uv pip install deepspeed
# 安装 vLLM（推理与部署时的可选依赖，可暂缓安装）
uv pip install -U "vllm>=0.17.0"
# 重新安装 Transformers，以防被 vLLM 默认版本覆盖
uv pip install transformers==5.2.0
```

**重要提示：**

+ ⚠️ 目前经实测验证，使用 `transformers==5.3.0` 版本会导致报错。
+ ✅ 强烈推荐使用 `transformers==5.2.0` 版本。
+ 若已安装 vLLM，为避免其默认版本覆盖，必须再次执行安装命令：`uv pip install -U "transformers==5.2.0"`。
+ 🔥 进行多卡训练时，必须安装 DeepSpeed。

:::color5
**<font style="color:#601bde;">3. 验证安装</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">安装完成后，请通过以下命令验证核心工具是否安装成功。</font>**

```plain
# 检查 swift 命令行工具是否可用
swift sft --help
# 若终端输出帮助信息，则表明安装成功

# 验证 DeepSpeed 是否安装成功
ds_report
# 终端应输出 DeepSpeed 版本及当前 CUDA 环境信息
```

**<font style="background-color:#D9EAFC;">验证成功示例：</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774619148353-5c1a47f7-8a7d-45be-a13e-5e32926bdd46.png)  
_图示：DeepSpeed 验证成功后的终端输出信息_

# **数据集准备**
:::color3
**简介：**本章节介绍 MS-SWIFT 框架支持的数据格式（包括**<font style="color:#ED740C;">纯文本、多轮对话及 Agent 工具调用数据</font>**），并说明如何使用内置数据集及自定义数据集进行训练。

:::

:::color5
**<font style="color:#601bde;">1. 支持的数据格式</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">MS-SWIFT 框架兼容多种数据格式，以下列举常用的文本数据格式及其示例。</font>**

**<font style="background-color:#D9EAFC;">1.1 纯文本数据</font>**<font style="background-color:#D9EAFC;">  
</font>适用于基础的问答或指令遵循任务。

```json
{"messages": [{"role": "user", "content": "浙江的省会在哪？"}, {"role": "assistant", "content": "浙江的省会在杭州。"}]}
{"messages": [{"role": "system", "content": "你是个有用无害的助手"}, {"role": "user", "content": "介绍一下杭州"}, {"role": "assistant", "content": "杭州是浙江省省会..."}]}
```

**<font style="background-color:#D9EAFC;">1.2 多轮对话数据</font>**<font style="background-color:#D9EAFC;">  
</font>适用于需要上下文理解的复杂交互场景。

```json
{"messages": [{"role": "system", "content": "你是一个专业的AI助手"}, {"role": "user", "content": "什么是机器学习？"}, {"role": "assistant", "content": "机器学习是人工智能的一个分支..."}, {"role": "user", "content": "它有哪些应用？"}, {"role": "assistant", "content": "机器学习广泛应用于图像识别、自然语言处理、推荐系统等领域..."}]}
```

**<font style="background-color:#D9EAFC;">说明：</font>**

+ 支持完整的多轮对话历史记录。
+ `system` 角色为可选配置，用于定义助手的行为准则或人设。
+ 对话轮次不受限制。

**<font style="background-color:#D9EAFC;">1.3 Agent 工具调用数据（常用）</font>**<font style="background-color:#D9EAFC;">  
</font>适用于训练模型使用外部工具完成特定任务。

```json
{"messages": [{"role": "user", "conte
  nt": "帮我查一下北京今天的天气"}, {"role": "assistant", "content": "好的，我来帮你查询北京的天气信息。"}, {"role": "tool_call", "content": "{\"name\": \"get_weather\", \"arguments\": {\"city\": \"北京\"}}"}, {"role": "tool_response", "content": "{\"temperature\": \"15°C\", \"condition\": \"晴\"}"}, {"role": "assistant", "content": "北京今天的天气是晴天，温度15°C。"}], "tools": [{"type": "function", "function": {"name": "get_weather", "description": "获取指定城市的天气信息", "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "城市名称"}}, "required": ["city"]}}}]}
```

**说明：**

+ `tool_call`：表示模型发起调用工具的请求。
+ `tool_response`：表示工具执行后返回的结果。
+ `tools`：定义当前可用的工具列表（即函数签名与描述）。
+ 支持在单次对话中进行多次工具调用或调用多个不同的工具。

:::color5
**<font style="color:#601bde;">2. 使用内置数据集</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">MS-SWIFT 框架内置了超过 150 种标准数据集，用户可直接通过命令行参数调用。</font>**

```plain
# 常用内置数据集示例
AI-ModelScope/alpaca-gpt4-data-zh      # 中文指令微调数据集
AI-ModelScope/alpaca-gpt4-data-en      # 英文指令微调数据集
swift/self-cognition                   # 模型自我认知数据集
AI-ModelScope/LaTeX_OCR:human_handwrite # LaTeX OCR 识别数据集
```

**<font style="background-color:#D9EAFC;">数据集采样语法规范：</font>**

```plain
# 基础语法格式：数据集ID:子数据集名称#采样数量
--dataset AI-ModelScope/alpaca-gpt4-data-zh#500

# 组合多个数据集进行混合训练
--dataset AI-ModelScope/alpaca-gpt4-data-zh#500 \
          AI-ModelScope/alpaca-gpt4-data-en#500 \
          swift/self-cognition#500

# 指定使用特定的子数据集
--dataset AI-ModelScope/LaTeX_OCR:human_handwrite#2000
```

:::color5
**<font style="color:#601bde;">3. 自定义数据集</font>**

:::

**<font style="color:#74B602;">若需使用私有数据，请将数据整理并保存为 </font>**`**<font style="color:#74B602;">.jsonl</font>**`**<font style="color:#74B602;"> 格式文件，随后在训练命令中通过参数指定路径。</font>**

```plain
--dataset train.jsonl --val_dataset val.jsonl
```



# **训练脚本**
:::color3
**简介：**本章节展示可直接运行的 **<font style="color:#ED740C;">2 卡 LoRA 微调脚本</font>**，包含环境变量配置、模型与数据参数、训练超参数等，并附带训练过程截图及参数详细解析。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475377772-bd15982c-9e55-42b3-98be-60d6193849e1.png)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475483674-58744dae-8572-44ba-9961-53b7e0abb4dc.png)

:::color5
**<font style="color:#601bde;">1. 基础多卡 LoRA 微调脚本（2卡，入门推荐）</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">⭐</font>****<font style="color:#74B602;"> 核心部分：以下为完整的、经过验证的多卡训练脚本，采用 DeepSpeed ZeRO-2 优化策略。关于数据集参数的具体说明，请回顾“数据集准备”章节。</font>**

```bash
#!/bin/bash
# 2卡训练脚本 - 使用 DeepSpeed ZeRO-2
# 数据集参数说明请参考前文"数据集准备"章节
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
NCCL_P2P_DISABLE=1 \
NPROC_PER_NODE=2 \
CUDA_VISIBLE_DEVICES=0,1 \
swift sft \
    --model Qwen/Qwen3.5-4B \
    --dataset AI-ModelScope/alpaca-gpt4-data-zh#2000 \
    --tuner_type lora \
    --lora_rank 16 \
    --lora_alpha 32 \
    --target_modules all-linear \
    --torch_dtype bfloat16 \
    --deepspeed zero2 \
    --num_train_epochs 3 \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --learning_rate 1e-4 \
    --warmup_ratio 0.05 \
    --max_length 2048 \
    --gradient_checkpointing true \
    --output_dir output/qwen3.5-4b-multi-2gpu \
    --logging_steps 10 \
    --save_steps 200 \
    --eval_steps 200 \
    --save_total_limit 3
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1774619148396-939135f3-b81c-4bd3-8f78-c19c46d83893.png)  
_图示：多卡训练过程终端截图_

:::color5
**<font style="color:#601bde;">2. 参数详细解释</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">为了更好地理解和调整训练过程，以下对脚本中涉及的各项参数进行分类解析。</font>**

**<font style="background-color:#D9EAFC;">2.1 环境变量配置</font>**

| **参数** | **含义** | **说明** |
| :--- | :--- | :--- |
| `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` | PyTorch CUDA 内存分配优化 | **强烈推荐**：启用可扩展内存段特性，有效避免因显存碎片化导致的 OOM（Out Of Memory）错误。此为 PyTorch 2.0 及以上版本的必备配置。 |
| `NCCL_P2P_DISABLE=1` | 禁用 NCCL P2P 通信 | 在某些特定的 GPU 拓扑结构下，P2P 通信可能存在不稳定性。禁用后将强制使用更为稳定的底层通信方式。 |
| `NPROC_PER_NODE=2` | 单节点进程数量 | 指定当前节点使用 2 个 GPU，每个 GPU 将独立运行 1 个训练进程。 |
| `CUDA_VISIBLE_DEVICES=0,1` | 可见 GPU 设备列表 | 限制程序仅可访问并使用编号为 0 和 1 的 GPU 设备进行训练。 |


**<font style="background-color:#D9EAFC;">2.2 模型和数据参数</font>**

| **参数** | **含义** | **说明** |
| :--- | :--- | :--- |
| `--model Qwen/Qwen3.5-4B` | 基础模型路径 | 指定需要进行微调的预训练模型，支持传入 ModelScope 模型 ID 或本地文件路径。 |
| `--dataset AI-ModelScope/alpaca-gpt4-data-zh#2000` | 训练数据集配置 | 指定使用 alpaca 中文指令数据集，并从中随机采样 2000 条数据。参数格式为：`数据集ID#采样数量`。 |


**<font style="background-color:#D9EAFC;">2.3 LoRA 微调参数</font>**

| **参数** | **含义** | **说明** |
| :--- | :--- | :--- |
| `--tuner_type lora` | 微调算法类型 | 采用 LoRA（Low-Rank Adaptation）技术进行参数高效微调（PEFT）。 |
| `--lora_rank 16` | LoRA 矩阵秩（Rank） | 定义低秩矩阵的维度大小，直接决定 LoRA 模块的参数量。数值越大，理论拟合能力越强，但参数量也随之增加。常规推荐值为 8 至 32。 |
| `--lora_alpha 32` | LoRA 缩放系数 | 用于控制 LoRA 权重在合并时的缩放比例，通常建议设置为 `lora_rank` 的 2 到 4 倍，该数值会影响模型的学习强度。 |
| `--target_modules all-linear` | LoRA 作用模块 | 指定将 LoRA 模块应用于模型中的所有线性层（Linear Layers），此配置覆盖范围最广，通常能取得最优的微调效果。 |


**<font style="background-color:#D9EAFC;">2.4 训练精度和优化</font>**

| **参数** | **含义** | **说明** |
| :--- | :--- | :--- |
| `--torch_dtype bfloat16` | 模型数据类型 | 采用 bfloat16 混合精度进行训练，在节省显存的同时保证训练过程的数值稳定性。若当前 GPU 架构不支持 bfloat16，需修改为 float16。 |
| `--deepspeed zero2` | DeepSpeed 优化策略 | 启用 ZeRO-2 优化阶段，将优化器状态与梯度数据在多张显卡间进行分片存储，预计可节省 30% 至 40% 的显存占用。 |
| `--gradient_checkpointing true` | 梯度检查点技术 | 通过在反向传播时重新计算中间激活值来换取显存空间的节省。开启后可降低 30% 至 40% 的显存占用，但会导致训练速度下降约 10%。 |


**<font style="background-color:#D9EAFC;">2.5 训练超参数</font>**

| **参数** | **含义** | **说明** |
| :--- | :--- | :--- |
| `--num_train_epochs 3` | 训练总轮数（Epochs） | 定义模型完整遍历训练数据集的次数。通常设置为 3 轮即可达到较好效果，轮数过多易导致模型过拟合。 |
| `--per_device_train_batch_size 2` | 单卡物理批次大小 | 设定每个 GPU 在单次前向传播中处理的样本数量。若遇到显存不足的情况，可将其降低至 1。 |
| `--gradient_accumulation_steps 4` | 梯度累积步数 | 设定在更新模型参数前，需累积梯度的前向传播次数。当前配置下的等效全局批次大小计算公式为：单卡批次大小 × 累积步数 × GPU 数量（即 2 × 4 × 2 = 16）。 |
| `--learning_rate 1e-4` | 初始学习率 | 控制模型参数的更新步长。对于 LoRA 微调，推荐初始值为 1e-4。学习率过大易导致训练不稳定，过小则会导致收敛缓慢。 |
| `--warmup_ratio 0.05` | 学习率预热比例 | 设定在训练总步数的前 5% 阶段，学习率从 0 线性增长至设定的初始学习率，有助于模型在训练初期的稳定性。 |
| `--max_length 2048` | 最大序列长度 | 限制单个样本的最大 Token 数量，超出部分将被截断。若显存资源紧张，可将其降低至 1024。 |


**<font style="background-color:#D9EAFC;">2.6 保存和日志参数</font>**

| **参数** | **含义** | **说明** |
| :--- | :--- | :--- |
| `--output_dir output/qwen3.5-4b-multi-2gpu` | 输出目录路径 | 指定用于保存模型检查点（Checkpoints）、训练日志及相关配置文件的目标文件夹。 |
| `--logging_steps 10` | 日志记录频率 | 设定每经过 10 个训练步数，记录并输出一次当前的训练指标（如 Loss、当前学习率等）。 |
| `--save_steps 200` | 模型保存频率 | 设定每经过 200 个训练步数，将当前模型状态保存为一个检查点。 |
| `--eval_steps 200` | 模型评估频率 | 设定每经过 200 个训练步数，在验证集上执行一次评估流程（前提是已配置验证集）。 |
| `--save_total_limit 3` | 检查点保留上限 | 限制输出目录中最多保留最新的 3 个模型检查点，以防占用过多磁盘空间。 |


:::color5
**<font style="color:#601bde;">3. 关键配置说明</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="background-color:#D9EAFC;">有效批次大小计算公式：</font>**

```plain
有效批次 = per_device_train_batch_size × gradient_accumulation_steps × GPU数量
        = 2 × 4 × 2 = 16
```

**<font style="background-color:#D9EAFC;">显存占用估算参考（基于 Qwen3.5-4B + LoRA 配置）：</font>**

+ 基础配置：每张显卡约占用 18-20GB 显存。
+ 启用梯度检查点（Gradient Checkpointing）：每张显卡约占用 12-14GB 显存。
+ 结合 ZeRO-2 优化：每张显卡约占用 10-12GB 显存。

**<font style="background-color:#D9EAFC;">配置提示：</font>**

+ 若使用的 GPU 硬件不支持 bfloat16 数据类型（例如 NVIDIA GTX 系列显卡），请务必将参数 `--torch_dtype bfloat16` 修改为 `--torch_dtype float16`。
+ 当面临显存不足的报错时，建议优先尝试将 `--per_device_train_batch_size` 降低至 1，或者将 `--max_length` 缩减至 1024。

# **推理部署**
:::color3
**简介：**本章节介绍微调完成后模型的推理与部署方法，涵盖**<font style="color:#ED740C;">命令行推理、Python API 调用、API 服务部署及 Web 界面交互</font>**等多种方式。

:::

:::color5
**<font style="color:#601bde;">1. 命令行推理</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="background-color:#D9EAFC;">1.1 基础推理命令</font>**<font style="background-color:#D9EAFC;">  
</font>通过命令行工具快速验证微调后模型的生成效果。

```plain
CUDA_VISIBLE_DEVICES=0 \
swift infer \
    --adapters output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-xxx \
    --stream true \
    --max_new_tokens 512
```

**<font style="background-color:#D9EAFC;">1.2 推理参数说明</font>**

| **参数** | **说明** | **默认值** | **示例** |
| :--- | :--- | :--- | :--- |
| `--adapters` | 指定微调后生成的 LoRA 权重文件路径。 | [] | `output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-200` |
| `--stream` | 是否启用流式输出模式（逐字打印）。 | None | `true` |
| `--max_new_tokens` | 限制模型单次生成的最大 Token 数量。 | None | `512`, `1024` |
| `--temperature` | 采样温度参数，控制生成文本的随机性。 | 从 config 读取 | `0.7`, `0` (确定性输出) |
| `--top_k` | Top-K 采样策略参数。 | None | `50` |
| `--top_p` | Top-P (Nucleus) 采样策略参数。 | None | `0.9` |
| `--enable_thinking` | 是否开启模型的思考模式。 | None | `false` |
| `--load_data_args` | 是否自动加载训练时使用的数据集切分参数。 | False | `true` (常用于验证集推理) |


**<font style="background-color:#D9EAFC;">推理技巧建议：</font>**

+ **<font style="color:#F38F39;">获取确定性输出</font>**<font style="color:#F38F39;">：</font>设置 `--temperature 0` 或 `--top_k 1`，可使模型每次针对相同输入生成一致的输出。
+ **<font style="color:#F38F39;">执行验证集推理</font>**<font style="color:#F38F39;">：</font>添加参数 `--load_data_args true`，系统将自动加载训练阶段划分的验证集进行推理测试。

:::color5
**<font style="color:#601bde;">2. Python 推理</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">通过 Python 代码集成模型推理逻辑，适用于二次开发场景。</font>**

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from peft import PeftModel
from swift import get_model_processor, get_template
from swift.infer_engine import TransformersEngine, InferRequest, RequestConfig

# 步骤一：加载基础模型与 LoRA 权重
adapter_dir = 'output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-xxx'
model, processor = get_model_processor('Qwen/Qwen3.5-4B')
model = PeftModel.from_pretrained(model, adapter_dir)

# 步骤二：初始化对话模板与推理引擎
template = get_template(processor, enable_thinking=False)
engine = TransformersEngine(model, template=template)

# 步骤三：执行标准推理请求
infer_request = InferRequest(messages=[{
    "role": "user",
    "content": '你好，你是谁？',
}])
request_config = RequestConfig(max_tokens=256, temperature=0.7)
resp_list = engine.infer([infer_request], request_config=request_config)
response = resp_list[0].choices[0].message.content
print(response)

# 步骤四：执行流式推理请求
request_config = RequestConfig(max_tokens=256, temperature=0.7, stream=True)
gen_list = engine.infer([infer_request], request_config=request_config)
for chunk in gen_list[0]:
    if chunk is None:
        continue
    print(chunk.choices[0].delta.content, end='', flush=True)
print()
```

:::color5
**<font style="color:#601bde;">3. 部署 API 服务</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">将微调后的模型封装为标准 API 服务，供外部系统调用。</font>**

```bash
CUDA_VISIBLE_DEVICES=0 \
swift deploy \
    --adapters output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-xxx \
    --served_model_name Qwen3.5-4B-lora \
    --port 8025
```

**<font style="background-color:#D9EAFC;">部署参数说明：</font>**

| **参数** | **说明** | **默认值** |
| :--- | :--- | :--- |
| `--port` | 指定 API 服务监听的端口号。 | 8000 |
| `--host` | 指定 API 服务绑定的 IP 地址。 | `0.0.0.0` |
| `--api_key` | 设置访问 API 服务的鉴权密钥。 | None |


**<font style="background-color:#D9EAFC;">注意：</font>**<font style="background-color:#D9EAFC;">  
</font>当前主流推理加速框架（如 vLLM、sglang、lmdeploy）在加载 Qwen3.5 的 LoRA 权重时存在一定的兼容性问题。现阶段强烈建议使用默认的 transformers 后端进行部署，并关注官方后续的修复更新。

:::color5
**<font style="color:#601bde;">4. Web 界面</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">启动基于 Web 的交互式对话界面，方便进行直观测试。</font>**

```bash
CUDA_VISIBLE_DEVICES=0 \
swift app \
    --adapters output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-xxx \
    --stream true
```

<font style="background-color:#FBDFEF;">服务启动后，在浏览器中访问终端输出的地址（通常为 </font>`<font style="background-color:#FBDFEF;">http://localhost:7860</font>`<font style="background-color:#FBDFEF;">），即可开始与模型进行交互对话。</font>

# **常见问题与解决方案**
:::color3
**简介：**本章节汇总了多卡微调过程中常见的技术问题（如**<font style="color:#ED740C;">显存不足、训练速度慢、GPU 负载不均</font>**等），并提供了按优先级排序的排查与解决建议。

:::

:::color5
**<font style="color:#601bde;">1. Q1: 多卡训练显存不足 (OOM)</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="background-color:#D9EAFC;">解决方案（按推荐优先级排序）：</font>**

1. **启用 PyTorch CUDA 内存优化（必备操作！）**

```plain
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

**原理解析与实际效果：**

+ **未启用状态**：训练可能在中途突然因 OOM 中断，此时观察到的显存实际使用率可能仅为 70%。
+ **启用状态**：在相同配置下可顺利完成训练，显存利用率可提升至 95%。
+ **根本原因**：PyTorch 默认的显存分配机制容易产生**显存碎片化**现象。即使物理显存总量充足，但由于碎片化导致系统无法分配出连续的大块显存，从而触发 OOM 错误。
+ **技术机制**：`expandable_segments:True` 参数允许 PyTorch 动态扩展内存段，有效缓解碎片化问题。
+ **适用场景**：在多卡训练、结合 DeepSpeed 或梯度检查点等复杂场景下，显存碎片化尤为严重。PyTorch 2.0 及以上版本强烈建议启用此配置，可规避约 90% 的碎片化 OOM 问题。
2. **升级 DeepSpeed 优化策略**  
若 ZeRO-2 仍无法满足显存需求，可尝试使用 ZeRO-3 策略。

```bash
--deepspeed zero3
```

3. **启用梯度检查点（Gradient Checkpointing）**

```bash
--gradient_checkpointing true
```

4. **减小批次大小并增加梯度累积步数**

```bash
--per_device_train_batch_size 1 \
--gradient_accumulation_steps 8
```

5. **引入 Liger Kernel 优化**

```bash
--use_liger_kernel true
```

6. **缩减最大序列长度**

```bash
--max_length 1024
```

7. **启用 CPU Offload（需自定义 DeepSpeed 配置文件）**  
将优化器状态卸载至系统内存（CPU RAM）。

```json
"offload_optimizer": {
  "device": "cpu",
  "pin_memory": true
}
```

:::color5
**<font style="color:#601bde;">2. Q2: 多卡训练速度慢</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="background-color:#D9EAFC;">加速优化方法：</font>**

1. **提升单卡批次处理量**  
在显存允许的前提下，增加单卡批次大小并相应减少累积步数。

```plain
--per_device_train_batch_size 4 \
--gradient_accumulation_steps 2
```

2. **采用 bfloat16 混合精度**

```plain
--torch_dtype bfloat16
```

3. **优化数据加载机制**  
启用数据缓存并增加数据处理的并发进程数。

```plain
--load_from_cache_file true \
--dataset_num_proc 16
```

4. **调整 DeepSpeed 配置参数**
    - 若显存充足，优先使用 ZeRO-2 而非 ZeRO-3，以减少通信开销。
    - 开启通信与计算重叠优化配置：`overlap_comm: true`。
5. **部署 Flash Attention 加速库**

```plain
pip install flash-attn --no-build-isolation
```

:::color5
**<font style="color:#601bde;">3. Q3: GPU 利用率不均衡</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="background-color:#D9EAFC;">排查与解决方案：</font>**

1. **优化数据分布策略**  
确保训练数据在各个 GPU 间均匀分配，并按序列长度进行分组。

```plain
--dataset_shuffle true \
--group_by_length true
```

2. **切换至 DeepSpeed ZeRO-3**  
ZeRO-3 策略具备自动平衡各显卡计算与显存负载的能力。
3. **核查环境变量配置**  
检查 `CUDA_VISIBLE_DEVICES` 参数，确保所指定的 GPU 设备均处于正常可用状态。

:::color5
**<font style="color:#601bde;">4. Q4: 训练效果不好</font>**

:::

**<font style="background-color:#D9EAFC;">模型调优建议：</font>**

1. **扩充训练数据规模**  
充分利用多卡算力优势，增加训练样本数量。

```plain
--dataset AI-ModelScope/alpaca-gpt4-data-zh#5000
```

2. **增加训练迭代轮数**

```plain
--num_train_epochs 5
```

3. **精细化调整学习率策略**

```plain
--learning_rate 5e-5 \
--warmup_ratio 0.1
```

4. **提升 LoRA 矩阵秩（Rank）**  
在多卡显存充足的情况下，增大 Rank 值以提升模型拟合能力。

```plain
--lora_rank 64
```

5. **尝试 DoRA 微调算法**

```plain
--use_dora true
```

:::color5
**<font style="color:#601bde;">5. Q5: 如何断点续训</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">当训练意外中断时，可通过以下命令从指定的检查点恢复训练。</font>**

```bash
swift sft \
    --resume_from_checkpoint output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-200 \
    <其他参数保持不变>
```

**操作注意事项：**

+ 必须保持除 `--resume_from_checkpoint` 外的所有参数（包括 GPU 数量及 DeepSpeed 配置）与初次训练时完全一致。
+ 系统将自动加载保存的优化器状态及随机数种子。
+ 训练将从检查点记录的步数无缝继续执行。

:::color5
**<font style="color:#601bde;">6. Q6: 如何合并 LoRA 权重</font>**

:::

**<font style="color:#74B602;">若需将微调得到的 LoRA 权重与基础模型合并为完整的独立模型，请执行以下命令。</font>**

```bash
swift export \
    --adapters output/qwen3.5-4b-multi-2gpu/vx-xxx/checkpoint-200 \
    --merge_lora true \
    --output_dir output/qwen3.5-4b-merged
```

:::color5
**<font style="color:#601bde;">7. Q7: DeepSpeed 初始化失败</font>**

:::

**<font style="background-color:#D9EAFC;">常见诱因及修复方案：</font>**

1. **依赖库缺失**  
确认是否已正确安装 DeepSpeed。

```plain
pip install deepspeed
```

2. **CUDA 版本不匹配**  
检查系统 CUDA 版本是否与 PyTorch 编译版本兼容。

```plain
# 查询当前系统 CUDA 版本
nvcc --version
# 若不匹配，需重新安装对应版本的 DeepSpeed
```

3. **环境变量配置异常**  
确保 CUDA 路径已正确添加至系统环境变量中。

```plain
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
```

# **训练监控**
:::color3
**简介：**本章节介绍如何使用**<font style="color:#ED740C;"> TensorBoard 和 SwanLab</font>** 等工具对训练过程中的各项指标进行实时监控与可视化分析。

:::

:::color5
**<font style="color:#601bde;">1. TensorBoard 监控</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">使用 TensorBoard 可以直观地查看训练过程中的 Loss 曲线、学习率变化等关键指标。</font>**

```plain
# 安装 TensorBoard 依赖包
pip install tensorboard

# 启动 TensorBoard 服务并指定日志目录
tensorboard --logdir output/qwen3.5-4b-multi-2gpu

# 在浏览器中访问以下地址查看监控面板
http://localhost:6006
```

:::color5
**<font style="color:#601bde;">2. SwanLab 监控</font>**

:::

**<font style="color:#74B602;">若需使用 SwanLab 平台进行云端监控与实验管理，可在训练命令中追加相关参数。</font>**

```plain
swift sft \
    --report_to swanlab \
    --swanlab_token your_token \
    --swanlab_project qwen3.5-multi-gpu-training \
    <其他参数>
```

# **性能参考**
:::color3
**简介：**本章节提供 Qwen3.5-4B 模型在不同 GPU 配置及 DeepSpeed 优化策略下的**<font style="color:#ED740C;">显存占用与训练速度</font>**参考数据，辅助用户进行资源规划。

:::

:::color5
**<font style="color:#601bde;">1. Qwen3.5-4B LoRA 多卡训练性能基准</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">以下数据基于 Qwen3.5-4B 模型进行 LoRA 微调的实际测试结果。</font>**

| **GPU配置** | **有效批次大小计算** | **单卡显存占用预估** | **训练吞吐量预估** |
| :--- | :--- | :--- | :--- |
| 2卡 + ZeRO-2 | 2×4×2=16 | ~16GB | ~200 samples/s |
| 4卡 + ZeRO-2 | 2×4×4=32 | ~14GB | ~400 samples/s |
| 8卡 + ZeRO-2 | 4×2×8=64 | ~12GB | ~800 samples/s |
| 4卡 + ZeRO-3 | 1×8×4=32 | ~10GB | ~350 samples/s |


:::color5
**<font style="color:#601bde;">2. DeepSpeed 优化策略效果对比</font>**

:::

**<font style="color:#74B602;">不同 DeepSpeed 阶段对显存消耗及训练速度的影响评估。</font>**

| **优化配置** | **显存节省比例** | **训练速度影响** | **推荐适用场景** |
| :--- | :--- | :--- | :--- |
| ZeRO-2 | 30-40% | 作为性能基准 | 适用于 2-8 卡的常规微调任务 |
| ZeRO-3 | 50-60% | 速度略降 10-15% | 适用于训练更大参数规模的模型或显存资源受限场景 |
| ZeRO-2 + CPU Offload | 40-50% | 速度略降 20% | 适用于显存资源较为紧张的场景 |
| ZeRO-3 + CPU Offload | 60-70% | 速度略降 30% | 适用于在有限资源下训练超大参数规模模型 |




# **总结**
:::color3
**简介：**本章节对 Qwen3.5 2卡分布式 LoRA 微调的核心流程、关键配置要点及参数调优建议进行归纳总结。

:::

:::color5
**<font style="color:#601bde;">1. 核心流程回顾</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">本教程系统性地阐述了基于 2卡分布式架构进行 LoRA 微调 的全流程，旨在帮助开发者快速构建并掌握 Qwen3.5 的多卡训练能力：</font>**

+ ✅ **环境准备**: 详述 DeepSpeed 等核心依赖的安装与验证流程。
+ ✅ **数据准备**: 解析并支持纯文本、多轮对话及 Agent 工具调用等多种数据格式。
+ ✅ **2卡训练**: 提供详尽的 DeepSpeed ZeRO-2 配置方案及逐项参数深度解析。
+ ✅ **完整示例**: 提供经过验证、可开箱即用的 2 卡训练 Bash 脚本。
+ ✅ **推理部署**: 涵盖命令行、Python API 及 Web 交互界面等多种部署途径。
+ ✅ **问题排查**: 针对多卡训练中常见的 OOM、速度瓶颈等问题提供系统性解决方案与性能优化建议。

:::color5
**<font style="color:#601bde;">2. 2卡训练核心要点备忘</font>**

:::

**<font style="color:#74B602;">在进行 2 卡微调实践时，请务必关注以下关键配置：</font>**

+ 🔥 **必须设置环境变量** `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`，这是规避显存碎片化导致 OOM 的关键。
+ 🔥 **必须确保已正确安装 DeepSpeed** 依赖库。
+ 🔥 **推荐启用 ZeRO-2 优化策略**，通过对优化器状态和梯度进行分片，可有效节省 30% 至 40% 的显存空间。
+ 🔥 **建议设置环境变量** `NCCL_P2P_DISABLE=1`，以规避潜在的底层 P2P 通信故障。
+ 🔥 **准确计算有效批次大小**：有效批次大小 = 单卡批次大小 × 梯度累积步数 × GPU 数量（例如：2 × 4 × 2 = 16）。
+ 🔥 **建议开启梯度检查点功能**（Gradient Checkpointing），以进一步压缩显存占用峰值。

:::color5
**<font style="color:#601bde;">3. 参数调优实战建议</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:#74B602;">根据实际硬件资源与任务需求，可灵活调整以下参数：</font>**

+ **显存资源充裕时**：可提升单次处理量，设置 `per_device_train_batch_size=4`，并相应降低累积步数 `gradient_accumulation_steps=2`。
+ **显存资源紧张时**：需采取保守策略，设置 `per_device_train_batch_size=1`，并增加累积步数 `gradient_accumulation_steps=8`。
+ **处理长文本任务时**：若显存受限，可考虑将最大序列长度 `max_length` 缩减至 1024。
+ **进行快速验证实验时**：为节省时间，可将训练总轮数 `num_train_epochs` 降低至 1 或 2 轮。

