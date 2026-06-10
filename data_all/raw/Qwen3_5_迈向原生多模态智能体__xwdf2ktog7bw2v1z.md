# Qwen3.5：迈向原生多模态智能体

<!-- source: yuque://zhongxian-iiot9/hlyypb/xwdf2ktog7bw2v1z -->

:::color3
**简介：**通义千问 Qwen 团队正式发布 Qwen3.5 系列，并开源其首款原生视觉-语言模型 Qwen3.5-397B-A17B，该模型以创新的稀疏混合专家架构，在显著降低推理成本的同时，实现了与万亿级模型相媲美的性能。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475377772-bd15982c-9e55-42b3-98be-60d6193849e1.png)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475483674-58744dae-8572-44ba-9961-53b7e0abb4dc.png)

:::color5
**<font style="color:#601bde;">1. 模型发布概览</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

通义千问 Qwen 团队于除夕夜发布了 Qwen3.5 系列，并同步开源其首款权重模型 **Qwen3.5-397B-A17B**

Qwen3.5-397B-A17B 是一款原生视觉-语言模型（Native Multimodality）。该模型在保持 3970 亿总参数规模的同时，通过创新的架构设计将单次激活参数量控制在 170 亿。这一设计使得开发者能够以更低的推理成本，获得比肩甚至超越万亿级（1T+）模型的性能体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475546807-26c686ce-6e35-4aa3-8e91-8170c6341971.png)

:::color5
**<font style="color:#601bde;">2. 模型资源</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **Github**：[https://github.com/QwenLM/Qwen3.5](https://github.com/QwenLM/Qwen3.5)
+ **ModelScope**：[https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B](https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B)
+ **Blog**：[https://qwen.ai/blog?id=qwen3.5](https://qwen.ai/blog?id=qwen3.5)
+ **Qwenchat 体验**：[https://chat.qwen.ai/](https://chat.qwen.ai/)

# **01 模型核心亮点**
:::color3
**简介：**Qwen3.5-397B-A17B 模型以其卓越的效能比为核心优势，通过进化的稀疏混合专家架构、原生多模态设计及广泛的多语言支持，实现了以 17B 激活参数挑战万亿级模型性能的突破。

:::

:::color5
**<font style="color:#601bde;">1. 极致的效能比</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

对于开发者而言，Qwen3.5-397B-A17B 最显著的优势在于其极致的效能比，实现了 **“以 17B 的激活量，挑战 1T 的极限”**。

:::color5
**<font style="color:#601bde;">2. 稀疏混合专家架构（MoE）的进化</font>**

:::

模型总参数量为 397B，但在前向传播过程中仅激活 17B 参数。这种超高稀疏度设计在显存占用与计算延迟之间取得了精妙的平衡。

:::color5
**<font style="color:#601bde;">3. 性能跨代持平</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

在预训练阶段，Qwen3.5-397B-A17B 在中英文、多语言、STEM 及逻辑推理等全维度基准测试中，其表现与参数量超过 1T 的 Qwen3-Max-Base 模型旗鼓相当。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475431800-5ad99c07-b414-481a-bb67-36b37e3c3d02.png)

:::color5
**<font style="color:#601bde;">4. 多模态原生化</font>**

:::

与传统的“外挂式”视觉模块不同，Qwen3.5 实现了早期的文本-视觉深度融合，使其在视觉理解与视频处理能力上全面超越了同等规模的 Qwen3-VL 模型。

:::color5
**<font style="color:#601bde;">5. 多语言支持扩展</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

模型支持的语言与方言数量从 119 种大幅增加至 201 种。同时，词表规模从 15 万扩展至 25 万，使得在大多数语言上的编解码效率提升了 10%–60%，显著优化了多语言场景下的推理速度。

# **02 模型效果实例**
:::color3
**简介：**具备 Agent 能力的 Qwen3.5 能够结合多模态能力，实现边思考、边搜索、边调用工具的复杂任务流，展现出在代码、视觉及空间智能等领域的强大应用潜力。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475073342-98324eee-c80a-45d2-83de-662fde214a9f.png)

:::color5
**<font style="color:#601bde;">1. 代码及智能体能力</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**网页开发：**Qwen3.5 能够有效协助进行网页开发，尤其在构建网页和设计用户界面等前端任务中表现出色。它能将简单的自然语言指令转化为可直接运行的代码，从而提升网站创建的效率。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475097933-97348c46-9f30-4fef-bee3-ccc6af51308f.png)

**OpenClaw 集成：**Qwen3.5 可与 OpenClaw 环境集成以驱动编程任务。通过将 OpenClaw 作为第三方智能体环境，Qwen3.5 能够执行网页搜索、信息收集和结构化报告生成等任务。它结合自身的推理能力与工具调用能力，以及 OpenClaw 提供的接口，为用户带来流畅的编码和研究体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475109465-2f21be0c-e7ca-4107-ae85-ca5e3022ca58.png)

以下为输出的 PDF 预览：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475135780-4024f2e8-2d25-426d-b205-44c119adae11.png)  
输出pdf预览 ⬇️

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475155078-053cbb66-adbd-45be-84cf-e3414e45dfba.png)

完整的 PDF 文档示例，请参阅官方博客：[https://qwen.ai/blog?id=qwen3.5#openclaw](https://qwen.ai/blog?id=qwen3.5#openclaw)

:::color5
**<font style="color:#601bde;">2. 视觉智能体能力</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**GUI 智能体**

Qwen3.5 可作为视觉智能体，自主操作手机与电脑以完成日常任务。

+ **移动端**：已适配更多主流应用，支持通过自然语言指令驱动操作。
+ **PC 端**：能够处理跨应用的数据整理、多步骤流程自动化等复杂任务，有效减少重复性人工干预，提升工作效率。

以下为任务示例：

```python
prompt：Fill the missing rows and columns which show the total value
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475169147-b8a3a98b-0bf3-4416-9563-d0bcd2b43b39.png)

**视觉编程：**Qwen3.5 能够将手绘的界面草图转化为结构清晰的前端代码，对简单游戏视频进行逻辑还原，或将长视频内容自动提炼为结构化的网页或可视化图表，从而降低从创意到实现的门槛。

以下为任务示例：

+ input：

```python
prompt：复刻这个小游戏的 HTML 代码
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475197035-47906104-a133-4311-8f8b-6d4450f6378b.png)

+ output：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475210384-1ef31d53-8e21-4b19-a696-fc8174a471b5.png)

:::color5
**<font style="color:#601bde;">3. 空间智能</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

通过对图像像素级位置信息进行建模，Qwen3.5 在物体计数、相对位置判断、空间关系描述等任务中表现出更高的准确性。它能有效缓解因视角变化或物体遮挡导致的误判，在自动驾驶场景理解、机器人导航等具身智能应用中展现出良好的空间感知潜力。

以下为任务示例：

+ input：

```python
prompt：我的车在什么时候并线的，又在什么时候开始右转的
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475223309-d70fcac2-4f89-4d8b-8a7f-547f0ca302c1.png)

+ output：

```python
<think>用户希望知道两个具体的时间点：并线（变道）的时间：车辆从当前车道移动到右侧车道（或出口匝道）的时间。开始右转的时间：车辆开始进行明显的右转动作的时间。分析视频：
00:00 - 00:05: 车辆在高速公路上行驶，前方有一辆卡车。路面湿滑，有雾。车辆保持在当前车道（看起来是右侧车道，或者正在接近出口）。
00:05 - 00:06: 车辆开始向右移动。可以看到车道线（虚线）在车辆左侧，车辆正在跨越这条线进入右侧的出口匝道区域。这是一个并线动作。
00:06 - 00:08: 车辆完全进入了右侧的匝道/出口车道。此时车辆基本直行，沿着匝道走。
00:08 - 00:09: 车辆继续沿着匝道行驶，前方有红白相间的警示牌。
00:09 - 00:10: 车辆开始明显向右转弯。之前的行驶方向比较直，现在车头明显指向右侧的停车场/休息区入口。
00:10 - 00:13: 车辆正在转弯进入休息区。可以看到蓝色的停车标志（P）。
00:13 - 00:19: 车辆已经在休息区内行驶，寻找停车位。
确定时间点：
并线 (Lane Change):在 00:05 左右，车辆开始向右偏离主路，跨越虚线。
到 00:06 时，车辆已经明显进入了右侧的出口车道。
所以并线发生在 00:05 - 00:06 之间。
开始右转 (Start Turning Right):在 00:08 之前，车辆主要是在沿着出口匝道直行。
在 00:08 - 00:09 之间，车辆经过了红白警示牌，开始向右打方向进入休息区内部道路。最明显的右转动作开始于 00:09，此时车头明显向右偏转，进入有蓝色指示牌的区域。
所以开始右转发生在 00:09 左右。
综合结论：并线：约 00:05右转：约 00:09再仔细看一下并线。 
00:00-00:04 车在行车道。 
00:05 车开始向右靠，压过虚线。这是并线出主路。 
00:06-00:08 车在减速车道/匝道上直行。 
00:09 车头明显向右转，进入服务区/停车场。
所以： 并线时间：00:05 右转时间：00:09让我们再精确一点。 
00:05 时，车辆开始向右移动，跨越车道线。
00:09 时，车辆经过路口，明显向右转弯进入停车场区域。
最终回答构建： 并线发生在 00:05。 右转发生在 00:09。
</think>根据视频画面分析：并线时间：您的车在 00:05 开始向右并线，驶离主路进入出口匝道。此时可以看到车辆跨越了白色的虚线车道分隔线。开始右转时间：您的车在 00:09 开始明显右转。此时车辆已经通过了红白相间的警示牌，车头向右偏转，准备进入右侧的停车/休息区域（可以看到蓝色的“P”字指示牌）。
```



根据视频画面分析：

+ **并线时间**：您的车在 **00:05** 开始向右并线，驶离主路进入出口匝道。此时可以看到车辆跨越了白色的虚线车道分隔线。
+ **开始右转时间**：您的车在 **00:09** 开始明显右转。此时车辆已经通过了红白相间的警示牌，车头向右偏转，准备进入右侧的停车/休息区域（可以看到蓝色的“P”字指示牌）。

更多带图推理、视觉推理示例详见官方博客 Demo：  
[https://qwen.ai/blog?id=qwen3.5#demo](https://qwen.ai/blog?id=qwen3.5#demo)

# **03 技术路线**
:::color3
**简介：**Qwen3.5 的技术路线核心在于架构创新、高效预训练与强化学习扩展，通过 Gated DeltaNet 与 MoE 的融合，以及对能力、效率和通用性的三维优化，实现了模型性能与成本的平衡。

:::

:::color5
**<font style="color:#601bde;">1. 架构创新：Gated DeltaNet 与 MoE 的融合</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

模型基于 Qwen3-Next 架构，创新性地将线性注意力机制与稀疏混合专家架构（MoE）相结合。

+ **混合注意力机制**：引入 Gated DeltaNet + Gated Attention，在提升模型长文本建模能力的同时，优化了计算稳定性。
+ **高稀疏度 MoE**：通过提高专家网络的稀疏度，在保证性能的前提下大幅降低了计算冗余。

这种混合架构设计，是其在 BFCL-V4、VITA-Bench、DeepPlanning 等全方位基准评测中表现优异的底层逻辑。

:::color5
**<font style="color:#601bde;">2. 预训练：三维度推进</font>**

:::

Qwen 团队从能力、效率与通用性三个维度对预训练流程进行了重构：

+ **能力**：在更大规模的视觉-文本语料上进行训练，并加强了中英文、多语言、STEM 与推理数据的质量。通过更严格的数据过滤，实现了 Qwen3.5-397B-A17B 与参数量超过 1T 的 Qwen3-Max-Base 性能相当的跨代持平效果。
+ **效率**：基于 Qwen3-Next 架构，采用了更高稀疏度的 MoE、Gated DeltaNet + Gated Attention 混合注意力、稳定性优化以及多 token 预测技术。
    - 在 32k/256k 上下文长度下，Qwen3.5-397B-A17B 的解码吞吐量分别是 Qwen3-Max 的 8.6 倍和 19.0 倍，且性能相当。
    - Qwen3.5-397B-A17B 的解码吞吐量分别是 Qwen3-235B-A22B 的 3.5 倍和 7.2 倍。
+ **通用性**：通过早期的文本-视觉融合与扩展的视觉/STEM/视频数据，实现了原生多模态能力，在相近规模下优于 Qwen3-VL。
    - 多语言覆盖从 119 种增至 201 种语言/方言。
    - 词表从 15 万扩展至 25 万，为多数语言带来了约 10%–60% 的编码/解码效率提升。

:::color5
**<font style="color:#601bde;">3. 后训练：强化学习的 Scaling Law</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

根据官方博客，与 Qwen3 系列相比，Qwen3.5 的后训练（Post-training）性能提升主要归功于对强化学习（RL）任务和环境的全面扩展。团队不再局限于针对特定指标或狭窄类别的查询进行优化，而是更加强调 RL 环境的难度与可泛化性。

实验证明，随着 RL 环境的扩展（Scaling），模型在通用 Agent 能力上获得了显著增益。这种“授人以渔”的训练策略，使得模型在 Tool-Decathlon、MCP-Mark 等工具调用与规划任务上表现突出。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475246633-a6db853d-4101-4abb-9871-85b4d891f92e.png)

# **04 基础设施**
:::color3
**简介：**为支撑复杂的原生多模态模型训练，Qwen 团队通过异构并行、计算重叠及异步强化学习框架等全栈基础设施优化，实现了近 100% 的硬件利用率和 3-5 倍的端到端训练速度提升。

:::

:::color5
**<font style="color:#601bde;">1. 异构并行与计算重叠</font>**

:::

原生多模态训练的主要挑战在于视觉与语言组件计算模式的差异。Qwen3.5 采用了解耦的并行策略，在处理混合的文本、图像、视频数据时，利用稀疏激活技术实现了跨模块的计算重叠。这项优化使得多模态训练的吞吐量几乎等同于纯文本基线，达到了接近 100% 的硬件利用率。

:::color5
**<font style="color:#601bde;">2. 异步强化学习框架</font>**

:::

针对大尺寸模型的强化学习（RL）训练，团队构建了一套可扩展的异步框架：

+ **训推分离架构**：通过解耦设计，支持百万级规模的 Agent 环境交互，显著提升了硬件利用率。
+ **技术组合**：引入了投机采样（Speculative Sampling）、Rollout 路由回放和多轮 Rollout 锁定技术，将端到端训练速度提升了 3 至 5 倍。

该设计不仅消除了框架层的调度中断，更通过算法与系统的协同设计，有效缓解了 RL 训练中的数据长尾问题，提高了训练曲线的平滑度。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475460924-748b0b0c-54b0-4f4f-ac59-ac051395804d.png)

# **05 模型部署实践**
:::color3
**简介：**本章节提供了使用 SGLang 和 vLLM 框架部署 Qwen3.5-397B-A17B 模型的详细命令，涵盖标准版、工具调用、多 Token 预测等多种模式，并介绍了通过 ModelScope API 进行调用的方法。

:::

:::color5
**<font style="color:#601bde;">1. SGLang 部署</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

部署 Qwen3.5 需要使用 SGLang 开源仓库的主分支。可在全新环境中通过以下命令安装：

```plain
uv pip install 'git+https://github.com/sgl-project/sglang.git#subdirectory=python&egg=sglang[all]'
```

以下命令将在 `http://localhost:8000/v1` 创建 API 端点。

**标准版**  
此命令可使用 8 块 GPU 上的张量并行，创建一个最大上下文长度为 262,144 tokens 的 API 端点。

```plain
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3
```

**工具调用**  
若需支持工具调用功能，可使用以下命令。

```plain
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3 --tool-call-parser qwen3_coder
```

**多 Token 预测（MTP）**  
推荐使用以下命令以启用 MTP 功能。

```plain
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3 --speculative-algo NEXTN --speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4
```

:::color5
**<font style="color:#601bde;">2. vLLM 部署</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

部署 Qwen3.5 需要使用 vLLM 开源仓库的主分支。可在全新环境中通过以下命令安装：

```plain
uv pip install vllm --torch-backend=auto --extra-index-url https://wheels.vllm.ai/nightly
```

以下命令将在 `http://localhost:8000/v1` 创建 API 端点。

**标准版本**  
此命令可用于在 8 块 GPU 上使用张量并行（tensor parallel），创建一个最大上下文长度为 262,144 个 token 的 API 端点。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3
```

**工具调用（Tool Call）**  
若需支持工具使用功能，可使用以下命令。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder
```

**多 Token 预测（MTP）**  
推荐使用以下命令以启用 MTP 功能。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":2}'
```

**纯文本模式（Text-Only）**  
此命令会跳过视觉编码器和多模态分析，以释放内存用于额外的 KV 缓存。

```plain
VLLM_USE_MODELSCOPE=true vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --language-model-only
```

:::color5
**<font style="color:#601bde;">3. ModelScope API-Inference</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

ModelScope API-Inference 已第一时间接入 Qwen3.5-397B-A17B 的调用服务，并提供免费调用额度供社区体验。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1771475314030-f3f097c6-eabd-4bcb-baef-958a8071b35a.png)

以下为调用示例代码：

```python
from openai import OpenAI

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='<MODELSCOPE_TOKEN>', # ModelScope Token
)

response = client.chat.completions.create(
    model='Qwen/Qwen3.5-397B-A17B', # ModelScope Model-Id, required
    messages=[{
        'role': 'user',
        'content': [
            {
                'type': 'text',
                'text': '描述这幅图',
            },
            {
                'type': 'image_url',
                'image_url': {
                    'url': 'https://modelscope.oss-cn-beijing.aliyuncs.com/demo/images/audrey_hepburn.jpg',
                },
            }
        ],
    }],
    stream=True
)

for chunk in response:
    if chunk.choices:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

:::color5
**<font style="color:#601bde;">4. 发布意义总结</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

本次 Qwen3.5-397B-A17B 的推出具有以下重要意义：

+ **突破超大规模模型的推理成本难题**：通过 17B 的激活参数实现 1T 级别的性能，证明了架构优化比单纯堆砌参数更具前景，使得中型开发者团队也能在本地或私有云部署顶级性能的多模态模型。
+ **开启原生多模态的普及化**：早期融合的架构使得模型在处理图文混合任务时体验更佳，为构建下一代视觉助手和多模态 Agent 提供了坚实的底层支持。
+ **展现强化学习的工程化典范**：Qwen 团队展示了如何通过构建可扩展的 RL 环境来提升模型的逻辑上限，为社区探索 O1 之外的推理能力提升路径提供了宝贵的实践经验。

