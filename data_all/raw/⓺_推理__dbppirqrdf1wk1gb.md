# ⓺ 推理

<!-- source: yuque://zhongxian-iiot9/hlyypb/dbppirqrdf1wk1gb -->

# 基础
## <font style="color:rgb(1, 1, 1);">可解释性和公平性</font>
<font style="color:rgb(1, 1, 1);">在开发大模型时，当你面临推理阶段的资源需求时，你如何确保模型的可解释性和公平性？</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733812963597-2ed2190a-972b-4bee-9450-63be70c7c8f9.png)

## batch_size对推理的影响
**batch_size对推理的影响**

•LLM大模型推理时，batch_size的选择会直接影响模型的准确性。当batch_size=1时，推理结果基本正确。

•当batch_size>1时，推理结果准确性大幅下降，和batch_size=1时的推理结果差距很大。相同的输入，batch_size=1和batch_size>1两种推理方式，生成结果差异很大。

•如果降低模型精度，比如从FP32到FP16；或者使用KV caching进行推理，会加剧这种batch_size>1准确度下降的趋势。

•影响范围：所有使用旋转位置编码的模型(Llama, Llama2, Falcon,GPTNeoX等)都会出现。编码模型BERT、生成式模型GPT、图像生成模型SRGAN等皆出现

**排除模型本身随机性因素**

1.设置temperature=0，模型输出非常确定，每次都选择概率最高的词汇，温度参数影响输出的概率分布。

2. 设置do_sample=False，解码时不进行随机采样。排除top_k，top_p等参数对采样的干扰。

以上设置，并不能消除batch_ size=1和batch_size>1推理结果的差异性，batch_size-1时可能出现长回复或错误答案。

**可能的原因**

1.有限的精度，除非您有无限的精度，否则不同的实现或不同的形状可能会产生不同的输出，因为中间计算必须保持在指定的精度内，并且要进行舍入。相同的精确输入，在FP32上相差最多1e-5。

2. 微妙的四舍五入，浮点数运算四舍五入问题，导致结果偏差，

3.RMSNorm导致的浮点溢出的问题。

4.精度转换导致的，比如FP32到FP16，数据转换时会丢失后面微小的小数，再后续进行大量的乘法会导致误差累积。

5.large batch时，GPUs在大量矩阵运算，会做优化加速/并行处理，但同时会导致准确性略微降低。

6.swapping技术，由于矩阵运算和浮点数，交换会累积误差。

7.主流的框架或库(例如TensorFlow、PyTorch或Hugging FaceTransformers)在批处理的实现方式上可能存在优化或偏差，这可能会影响不同批次大小的结果的重现性。

8.硬件因素(例如，GPU或TPU精度、并行策略)也发挥了作用。

•参考资料：the batch size can affect inference results

• 参考资料：Batch Decoding of LMs wil cause different outputswith different batch size

**缓解办法**

•尽量让每个batch中token长度一致，这样就不需要padding，得到推理结果和batch_ size=1的接近或相同。

•模型精度量化到低精度，会减少模型参数存储的位数，加剧这种影响，尽量使用原始精度或高精度，比如FP32。

## 推理的显存占用如何估计？
:::color5
**<font style="color:#601BDE;">推理显存计算步骤</font>**

:::

1. **确定模型规模**：
    - <font style="color:rgb(51, 51, 51);">LLaMA 模型有多个版本，例如 7B（70亿参数）、13B、30B 等。假设我们以 7B 参数版本为例。</font>
2. **计算模型参数的显存占用**：
    - <font style="color:rgb(51, 51, 51);">假设每个参数占用 4 字节（使用 32 位浮点数）。</font>
    - <font style="color:rgb(51, 51, 51);">模型参数显存=7,000,000,000参数×4字节/参数=28,000,000,000字节=28GB</font>
3. **输入和输出数据占用**：
    - <font style="color:rgb(51, 51, 51);">假设输入序列长度为 512，每个 token 占用 4 字节。</font>
    - <font style="color:rgb(51, 51, 51);">输入数据=512tokens×4字节/token=2048字节≈2KB</font>
    - <font style="color:rgb(51, 51, 51);">输出同样占 2KB。</font>
    - <font style="color:rgb(51, 51, 51);">总数据占用约为 4KB，可以忽略不计。</font>
4. **总推理显存占用**：
    - <font style="color:rgb(51, 51, 51);">总推理显存=28GB+4KB≈28GB</font>



## 推理阶段是否需要mask
**<font style="color:rgb(51, 51, 51);">1. 常规下游任务</font>**

+ **<font style="color:rgb(51, 51, 51);">无显式Mask</font>**<font style="color:rgb(51, 51, 51);">：在大多数推理场景（如文本分类、实体识别、翻译），输入为完整文本，无需主动mask。例如，BERT进行情感分析时直接处理原始句子。</font>
+ **<font style="color:rgb(51, 51, 51);">Padding Mask保留</font>**<font style="color:rgb(51, 51, 51);">：仍需处理变长序列的填充，通过padding mask忽略无效位置。</font>

**<font style="color:rgb(51, 51, 51);">2. 生成式任务</font>**

+ **<font style="color:rgb(51, 51, 51);">自回归生成（如GPT）</font>**<font style="color:rgb(51, 51, 51);">：生成过程中，模型逐步预测下一个词，内部通过注意力掩码限制仅关注已生成部分，但无需显式mask输入。</font>
+ **<font style="color:rgb(51, 51, 51);">填空任务（如BERT）</font>**<font style="color:rgb(51, 51, 51);">：若任务要求预测特定位置的词（如完形填空），需在输入中显式mask目标位置（如</font>`<font style="color:rgb(51, 51, 51);">[MASK]</font>`<font style="color:rgb(51, 51, 51);">），类似预训练阶段的处理。</font>

# <font style="color:rgb(53, 53, 53);">部署</font>
## 显卡对比
:::color5
**<font style="color:#601BDE;">1.选择建议</font>**

:::

1. **大模型训练**：
    - **<font style="color:rgb(51, 51, 51);">预算充足</font>**<font style="color:rgb(51, 51, 51);">：H100集群（NVLink全互联）。</font>
    - **<font style="color:rgb(51, 51, 51);">性价比方案</font>**<font style="color:rgb(51, 51, 51);">：A100 80GB（二手市场性价比高）。</font>
2. **推理部署**：
    - **<font style="color:rgb(51, 51, 51);">高吞吐需求</font>**<font style="color:rgb(51, 51, 51);">：L40（支持多实例并行推理）。</font>
    - **<font style="color:rgb(51, 51, 51);">成本敏感</font>**<font style="color:rgb(51, 51, 51);">：RTX 4090（FP16性能接近A10，价格低50%）。</font>
3. **混合负载**：
    - **<font style="color:rgb(51, 51, 51);">科研+渲染</font>**<font style="color:rgb(51, 51, 51);">：RTX 4090 + A100组合（分别处理图形和计算）。</font>
4. **边缘计算**：
    - **<font style="color:rgb(51, 51, 51);">低功耗场景</font>**<font style="color:rgb(51, 51, 51);">：L20（支持PCIe 5.0和能效优化）。</font>

:::color5
**<font style="color:#601BDE;">2.性能对比</font>**

:::

| **显卡型号** | **架构** | **计算单元** | **显存配置** | **FP32性能** | **FP16/TF32性能** | **Tensor Core特性** | **价格范围（美元）** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">A10</font>** | <font style="color:rgb(51, 51, 51);">Ampere</font> | <font style="color:rgb(51, 51, 51);">72 SM单元</font> | <font style="color:rgb(51, 51, 51);">24GB GDDR6</font> | <font style="color:rgb(51, 51, 51);">31.2 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">125 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">3代Tensor Core</font> | <font style="color:rgb(51, 51, 51);">3</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">500</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">3</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">500</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">4,000</font> |
| **<font style="color:rgb(51, 51, 51);">A100</font>** | <font style="color:rgb(51, 51, 51);">Ampere</font> | <font style="color:rgb(51, 51, 51);">108 SM单元</font> | <font style="color:rgb(51, 51, 51);">40/80GB HBM2e</font> | <font style="color:rgb(51, 51, 51);">19.5 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">312 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">支持稀疏计算，MIG技术</font> | <font style="color:rgb(51, 51, 51);">10</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">000</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">10</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">000</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">15,000</font> |
| **<font style="color:rgb(51, 51, 51);">H100</font>** | <font style="color:rgb(51, 51, 51);">Hopper</font> | <font style="color:rgb(51, 51, 51);">144 SM单元</font> | <font style="color:rgb(51, 51, 51);">80GB HBM3</font> | <font style="color:rgb(51, 51, 51);">34.4 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">1,979 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">4代Tensor Core，Transformer引擎</font> | <font style="color:rgb(51, 51, 51);">25</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">000</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">25</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">000</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">35,000</font> |
| **<font style="color:rgb(51, 51, 51);">L20</font>** | <font style="color:rgb(51, 51, 51);">Ada Lovelace</font> | <font style="color:rgb(51, 51, 51);">96 SM单元</font> | <font style="color:rgb(51, 51, 51);">48GB GDDR6</font> | <font style="color:rgb(51, 51, 51);">56.8 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">181.8 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">4代Tensor Core，光追优化</font> | <font style="color:rgb(51, 51, 51);">4</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">500</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">4</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">500</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">6,000</font> |
| **<font style="color:rgb(51, 51, 51);">L40</font>** | <font style="color:rgb(51, 51, 51);">Ada Lovelace</font> | <font style="color:rgb(51, 51, 51);">142 SM单元</font> | <font style="color:rgb(51, 51, 51);">48GB GDDR6</font> | <font style="color:rgb(51, 51, 51);">90.5 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">289.6 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">支持虚拟化，推理优化</font> | <font style="color:rgb(51, 51, 51);">7</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">000</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">7</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">000</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">9,000</font> |
| **<font style="color:rgb(51, 51, 51);">RTX 4090</font>** | <font style="color:rgb(51, 51, 51);">Ada Lovelace</font> | <font style="color:rgb(51, 51, 51);">128 SM单元</font> | <font style="color:rgb(51, 51, 51);">24GB GDDR6X</font> | <font style="color:rgb(51, 51, 51);">82.6 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">1321 TFLOPS</font> | <font style="color:rgb(51, 51, 51);">DLSS3，光追核心</font> | <font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">600</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">600</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">2,000</font> |


:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

| 显卡型号 | 典型场景 |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">H100</font>** | <font style="color:rgb(51, 51, 51);">千亿参数LLM训练、量子模拟、超算中心</font> |
| **<font style="color:rgb(51, 51, 51);">A100</font>** | <font style="color:rgb(51, 51, 51);">中型模型训练（如10B-100B参数）、科学计算（CFD/分子动力学）</font> |
| **<font style="color:rgb(51, 51, 51);">L40</font>** | <font style="color:rgb(51, 51, 51);">多模态推理（视频/图像生成）、云游戏服务器</font> |
| **<font style="color:rgb(51, 51, 51);">L20</font>** | <font style="color:rgb(51, 51, 51);">边缘AI推理（自动驾驶实时处理）、轻量级训练</font> |
| **<font style="color:rgb(51, 51, 51);">A10</font>** | <font style="color:rgb(51, 51, 51);">虚拟化环境（VDI）、传统企业级AI推理</font> |
| **<font style="color:rgb(51, 51, 51);">RTX 4090</font>** | <font style="color:rgb(51, 51, 51);">个人研究者模型微调、小规模LLM推理、图形渲染（3D建模/影视制作）</font> |




## LLM部署如何选择精度
```python
硬件检测
├── 支持fp8（H100） → 量化到fp8
├── 支持bf16（A100/H100） → 首选bf16
└── 仅支持fp16（A10/L40/L20） → 选择fp16
      ├── 显存不足 → 添加量化（AWQ/GPTQ）
      └── 存在溢出 → 混合精度+损失缩放
```

**部署建议：**

1. **H100集群**：
    - <font style="color:rgb(51, 51, 51);">使用fp8量化+张量并行，部署千亿参数模型</font>
    - <font style="color:rgb(51, 51, 51);">启用CUDA Graph优化端到端延迟</font>
2. **A100-80GB**：
    - <font style="color:rgb(51, 51, 51);">bf16精度部署70B模型</font>
    - <font style="color:rgb(51, 51, 51);">结合vLLM实现高吞吐服务（吞吐量>1000 token/s）</font>
3. **A10/L40**：
    - <font style="color:rgb(51, 51, 51);">fp16部署13B-34B模型</font>
    - <font style="color:rgb(51, 51, 51);">使用FlashAttention-2优化KV缓存</font>
4. **L20**：
    - <font style="color:rgb(51, 51, 51);">fp16部署7B以下模型</font>
    - <font style="color:rgb(51, 51, 51);">使用量化和模型切片（如llama.cpp GGML）</font>

:::color5
**<font style="color:#601BDE;">1.H100显卡：优先使用fp8/bf16</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">fp8（首选）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">显存占用比fp16再减半，吞吐量提升2-3倍</font>
    - <font style="color:rgb(51, 51, 51);">需要模型支持量化（如LLM.int8()）</font>
    - <font style="color:rgb(51, 51, 51);">示例代码（NVIDIA Transformer Engine）：</font>

```python
from transformer_engine import fp8_autocast
with fp8_autocast(enabled=True):
    outputs = model(inputs)
```

+ **<font style="color:rgb(51, 51, 51);">bf16</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">保留float32的动态范围，避免溢出</font>
    - <font style="color:rgb(51, 51, 51);">适合未量化的大模型（如70B+参数）</font>

:::color5
**<font style="color:#601BDE;">2.A100显卡：bf16 > fp16</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">bf16优先</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">利用Tensor Core加速，吞吐量比fp32高3倍</font>
    - <font style="color:rgb(51, 51, 51);">显存占用与fp16相同（2字节/参数）</font>
    - <font style="color:rgb(51, 51, 51);">PyTorch启用方式：</font>

```python
torch.set_float32_matmul_precision('high')  # 自动选择bf16
```

+ **<font style="color:rgb(51, 51, 51);">fp16备用</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">旧版框架兼容方案</font>
    - <font style="color:rgb(51, 51, 51);">需监控梯度溢出（添加损失缩放）</font>

:::color5
**<font style="color:#601BDE;">3.A10/L40/L20显卡：fp16为主</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">fp16量化部署</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">显存节省50%（相比fp32），适合24GB以下显存</font>
    - <font style="color:rgb(51, 51, 51);">使用NVIDIA Triton推理服务器：</font>

```bash
tritonserver --model-repository=/models --strict-model-config=false
```

+ **<font style="color:rgb(51, 51, 51);">动态混合精度</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对敏感层（如注意力输出）保留fp32</font>
    - <font style="color:rgb(51, 51, 51);">HuggingFace实现示例：</font>

```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b", 
    torch_dtype=torch.float16,
    device_map="auto"
)
```

# <font style="color:rgb(53, 53, 53);">推理加速</font>
## KV cache
:::color3
**<font style="color:#1f2329;">简介</font>**<font style="color:#1f2329;">：</font>**<font style="color:rgb(51, 51, 51);">KV-Cache</font>**<font style="color:rgb(51, 51, 51);"> 的核心思想是缓存历史 Token 的 Key 和 Value 矩阵，在后续生成步骤中直接复用，仅计算新 Token 的 Key 和 Value，从而降低计算量。</font>

:::

:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

<font style="color:rgb(51, 51, 51);">在 Transformer 的自注意力机制中，每个位置的输出依赖于所有历史位置的 Key 和 Value。自回归生成时，每次仅新增一个 Token，</font>**<font style="color:#ED740C;">若每次重新计算所有历史 Token 的 Key 和 Value，会导致大量冗余计算</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740379033187-8b805e93-792a-4515-8f40-778e1e0a13b4.png)

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">计算量降低</font>**<font style="color:rgb(51, 51, 51);">：时间从 O(n2)降至 O(n)</font> | **<font style="color:rgb(51, 51, 51);">内存占用高</font>**<font style="color:rgb(51, 51, 51);">：需存储所有历史 KV 值</font> |
| **<font style="color:rgb(51, 51, 51);">推理速度提升</font>**<font style="color:rgb(51, 51, 51);">：尤其适合长序列生成</font> | **<font style="color:rgb(51, 51, 51);">序列长度受限</font>**<font style="color:rgb(51, 51, 51);">：显存限制最大长度</font> |
| **<font style="color:rgb(51, 51, 51);">兼容性强</font>**<font style="color:rgb(51, 51, 51);">：适用于所有自回归模型</font> | **<font style="color:rgb(51, 51, 51);">实现复杂度</font>**<font style="color:rgb(51, 51, 51);">：需处理缓存拼接和更新</font> |


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">文本生成</font>**<font style="color:rgb(51, 51, 51);">：GPT、LLaMA 等大模型的逐 Token 生成。</font>
+ **<font style="color:rgb(51, 51, 51);">机器翻译</font>**<font style="color:rgb(51, 51, 51);">：长句子的逐词翻译。</font>
+ **<font style="color:rgb(51, 51, 51);">对话系统</font>**<font style="color:rgb(51, 51, 51);">：多轮对话的连续响应生成。</font>
+ **<font style="color:rgb(51, 51, 51);">代码生成</font>**<font style="color:rgb(51, 51, 51);">：长代码片段的逐步生成。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">内存优化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">量化压缩</font>**<font style="color:rgb(51, 51, 51);">：对缓存进行低精度（FP16/INT8）存储。</font>
    - **<font style="color:rgb(51, 51, 51);">分块缓存</font>**<font style="color:rgb(51, 51, 51);">：将长序列分块存储，按需加载。</font>
2. **<font style="color:rgb(51, 51, 51);">计算优化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">稀疏注意力</font>**<font style="color:rgb(51, 51, 51);">：仅缓存关键位置的 KV（如 Local Attention）。</font>
    - **<font style="color:rgb(51, 51, 51);">动态裁剪</font>**<font style="color:rgb(51, 51, 51);">：丢弃历史中不重要的 Token 的 KV。</font>
3. **<font style="color:rgb(51, 51, 51);">系统优化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">显存复用</font>**<font style="color:rgb(51, 51, 51);">：通过内存池管理缓存，减少碎片。</font>
    - **<font style="color:rgb(51, 51, 51);">并行计算</font>**<font style="color:rgb(51, 51, 51);">：在 GPU 上异步更新缓存。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn

class TransformerBlockWithKVCache(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, n_heads)
        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)
        
    def forward(self, x, cache_k=None, cache_v=None):
        # x: (seq_len, batch, d_model)
        q = self.Wq(x)
        k = self.Wk(x)
        v = self.Wv(x)
        
        # 更新缓存
        if cache_k is not None:
            k = torch.cat([cache_k, k], dim=0)
            v = torch.cat([cache_v, v], dim=0)
        
        # 自注意力计算
        attn_output, _ = self.attn(q, k, v, need_weights=False)
        return attn_output, k, v

# 使用示例
model = TransformerBlockWithKVCache(d_model=512, n_heads=8)
batch_size = 4
seq_len = 1  # 自回归生成每次输入 1 个 Token

# 初始输入（假设为起始符）
x = torch.randn(seq_len, batch_size, 512)
cache_k, cache_v = None, None

# 模拟生成 10 个 Token
for _ in range(10):
    output, cache_k, cache_v = model(x, cache_k, cache_v)
    x = output  # 假设 output 是下一个 Token 的嵌入

```

### 为什么没有Q cache
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在自回归模型（如Transformer）的推理优化中，</font>**<font style="color:rgb(51, 51, 51);">KV-Cache</font>**<font style="color:rgb(51, 51, 51);">（Key-Value缓存）被广泛使用，但</font>**<font style="color:rgb(51, 51, 51);">Q-Cache</font>**<font style="color:rgb(51, 51, 51);">（Query缓存）并不存在。</font>

+ **<font style="color:rgb(51, 51, 51);">KV-Cache 的必要性</font>**<font style="color:rgb(51, 51, 51);">：历史 K/V 被所有后续步骤复用，缓存可避免重复计算。</font>
+ **<font style="color:rgb(51, 51, 51);">Q-Cache 的冗余性</font>**<font style="color:rgb(51, 51, 51);">：Q 仅服务于当前步骤，无长期复用需求，缓存反而浪费资源。</font>

:::

:::color5
**<font style="color:#601BDE;">1.attention注意力机制核心逻辑</font>**

:::

<font style="color:rgb(51, 51, 51);">自注意力计算中，每个位置的输出通过 </font>**<font style="color:rgb(51, 51, 51);">Query (Q)</font>**<font style="color:rgb(51, 51, 51);"> 与所有位置的 </font>**<font style="color:rgb(51, 51, 51);">Key (K)</font>**<font style="color:rgb(51, 51, 51);"> 计算相似度，再对 </font>**<font style="color:rgb(51, 51, 51);">Value (V)</font>**<font style="color:rgb(51, 51, 51);"> 加权求和：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740379666938-2cea058c-8ef4-4a0b-9728-ac445e84cede.png)

+ **<font style="color:rgb(51, 51, 51);">Q</font>**<font style="color:rgb(51, 51, 51);">：当前输入的特征向量，用于“询问”需要关注哪些历史信息。</font>
+ **<font style="color:rgb(51, 51, 51);">K/V</font>**<font style="color:rgb(51, 51, 51);">：历史输入的特征向量，提供“答案内容”。</font>

:::color5
**<font style="color:#601BDE;">2.为什么需要KV-Cache</font>**

:::

<font style="color:rgb(51, 51, 51);">在自回归生成（如文本生成）中，模型逐次生成 Token，每次生成第 t</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 个 Token 时：</font>

+ **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：仅当前 Token x</font><sub><font style="color:rgb(51, 51, 51);">t</font></sub><font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">计算需求</font>**<font style="color:rgb(51, 51, 51);">：需要将 xt</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">与所有历史 Token 的 K/V 交互以计算注意力。</font>
+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：如果不缓存 K/V，每次生成时需重新计算所有历史 Token 的 K/V，导致复杂度为 O(t</font><sup><font style="color:rgb(51, 51, 51);">2</font></sup><font style="color:rgb(51, 51, 51);">)。</font>

**<font style="color:rgb(51, 51, 51);">KV-Cache 的作用</font>**<font style="color:rgb(51, 51, 51);">：缓存历史 Token 的 K/V，每次只需计算新 Token 的 K/V，复杂度降至 O(t)。</font>

:::color5
**<font style="color:#601BDE;">3.为什么不需要Q-Cache</font>**

:::

**<font style="color:rgb(51, 51, 51);">(1) Q 的时效性</font>**

+ <font style="color:rgb(51, 51, 51);">Q 的物理意义：Query 表示当前 Token 需要关注哪些历史信息，</font>**<font style="color:#74B602;">仅对当前生成步骤有意义</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ <font style="color:rgb(51, 51, 51);">缓存 Q 无意义：后续步骤生成新 Token 时，它们的 Q 会变化，</font>**<font style="color:#74B602;">历史 Q 不再被使用</font>**<font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">(2) 计算流程的差异性</font>**

<font style="color:rgb(51, 51, 51);">K/V 的角色</font><font style="color:rgb(51, 51, 51);">：所有历史 Token 的 K/V 需要被后续所有步骤复用。</font>

<font style="color:rgb(51, 51, 51);">Q 的角色：每个步骤的 </font>**<font style="color:#74B602;">Q 仅用于计算当前 Token 的注意力权重</font>**<font style="color:rgb(51, 51, 51);">，完成后即失效。</font>

:::color5
**<font style="color:#601BDE;">4.公式推导验证</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740379788259-049c6f98-9fbe-483f-91b7-a9b5841d4834.png)



### 推理中kv-cache显存计算
<font style="color:rgb(51, 51, 51);background-color:rgb(244, 240, 255);">给定float32，模型层数，hidden_dim，seq_len，batchsize</font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在推理过程中，显存占用主要包括模型参数和KV-Cache两部分。以下是详细计算步骤和公式：</font>

:::

:::color5
**<font style="color:#601BDE;">1.模型参数显存占用</font>**

:::

<font style="color:rgb(51, 51, 51);">模型参数主要包含Transformer层的权重矩阵、词嵌入（Embedding）和输出层（LM Head）的权重。显存计算公式如下：</font>

+ **每层参数**（12层为例）：
    - **<font style="color:rgb(51, 51, 51);">自注意力模块</font>**<font style="color:rgb(51, 51, 51);">：Q/K/V矩阵（3 × h²） + 输出投影（h²） =</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">4h²</font>**
    - **<font style="color:rgb(51, 51, 51);">FFN模块</font>**<font style="color:rgb(51, 51, 51);">：两个全连接层（8h²）</font>
    - <font style="color:rgb(51, 51, 51);">每层总参数量：</font>`<font style="color:rgb(51, 51, 51);">4h² + 8h² = 12h²</font>`
+ **总参数**：
    - **<font style="color:rgb(51, 51, 51);">L层参数</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">L × 12h²</font>`
    - **<font style="color:rgb(51, 51, 51);">词嵌入 + LM Head</font>**<font style="color:rgb(51, 51, 51);">（假设词表大小为V）：</font>`<font style="color:rgb(51, 51, 51);">2 × V × h</font>`
+ **显存占用**：

```python
模型参数显存 = (12 * L * h² + 2 * V * h) * 4（Bytes）
```

**注**：需要用户提供词表大小 `V` 才能准确计算。

:::color5
**<font style="color:#601BDE;">2.KV cache显存计算</font>**

:::

<font style="color:rgb(51, 51, 51);">KV-Cache用于缓存自注意力中的Key和Value张量，显存占用与层数、批次大小、序列长度和隐藏维度成正比：</font>

+ **<font style="color:rgb(51, 51, 51);">每个Token的KV存储</font>**<font style="color:rgb(51, 51, 51);">：每层需存Key和Value各一个向量，大小为</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">2 × h</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">总KV-Cache显存</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
KV-Cache显存 = L * b * s * 2 * h * 4（Bytes）
```

    - **<font style="color:rgb(51, 51, 51);">L</font>**<font style="color:rgb(51, 51, 51);">: 层数</font>
    - **<font style="color:rgb(51, 51, 51);">b</font>**<font style="color:rgb(51, 51, 51);">: Batch Size</font>
    - **<font style="color:rgb(51, 51, 51);">s</font>**<font style="color:rgb(51, 51, 51);">: 序列长度（如生成式任务的最大长度）</font>
    - **<font style="color:rgb(51, 51, 51);">h</font>**<font style="color:rgb(51, 51, 51);">: Hidden Dimension</font>

:::color5
**<font style="color:#601BDE;">3.总显存计算</font>**

:::

<font style="color:rgb(51, 51, 51);">总显存 = 模型参数显存 + KV-Cache显存</font>

```python
总显存 = (12 * L * h² + 2 * V * h) * 4 + L * b * s * 2 * h * 4（Bytes）
```

<font style="color:rgb(51, 51, 51);">假设 </font>`<font style="color:rgb(51, 51, 51);">L=24, h=4096, b=1, s=2048, V=50000</font>`<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">模型参数显存</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">≈</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">(12*24*(4096)^2 + 2*50000*4096)*4 ≈ 17.3GB</font>`
+ **<font style="color:rgb(51, 51, 51);">KV-Cache显存</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">24*1*2048*2*4096*4 ≈ 1.6GB</font>`
+ **<font style="color:rgb(51, 51, 51);">总显存</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">≈</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">18.9GB</font>**

### KV cache的内存瓶颈问题(<font style="color:rgb(51, 51, 51);">Memory Bound</font>)
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：内存瓶颈问题</font>

:::

:::color5
**<font style="color:#601BDE;">1.什么是内存瓶颈Memory Bound</font>**

:::

<font style="color:rgb(51, 51, 51);">在Transformer模型的</font>**<font style="color:rgb(51, 51, 51);">自回归生成</font>**<font style="color:rgb(51, 51, 51);">（如文本生成）过程中，为了避免重复计算历史Token的Key和Value（K/V）向量，通常会使用</font>**<font style="color:rgb(51, 51, 51);">KV Cache</font>**<font style="color:rgb(51, 51, 51);">缓存这些中间结果。然而，随着序列长度（Sequence Length）增长，KV Cache的内存占用会呈</font>**<font style="color:rgb(51, 51, 51);">线性增长</font>**<font style="color:rgb(51, 51, 51);">，导致以下问题：</font>

1. **内存瓶颈（Memory Bound）**  
对于L层Transformer模型，每生成一个Token，需缓存每层的K/V向量。内存占用公式为：

```plain
Memory = 2 × L × B × S × H_kv
```

    - `<font style="color:rgb(51, 51, 51);">L</font>`<font style="color:rgb(51, 51, 51);">：模型层数</font>
    - `<font style="color:rgb(51, 51, 51);">B</font>`<font style="color:rgb(51, 51, 51);">：Batch Size</font>
    - `<font style="color:rgb(51, 51, 51);">S</font>`<font style="color:rgb(51, 51, 51);">：当前序列长度</font>
    - `<font style="color:rgb(51, 51, 51);">H_kv</font>`<font style="color:rgb(51, 51, 51);">：每个注意力头的K/V向量维度  
</font><font style="color:rgb(51, 51, 51);">当生成长序列（如S=4096）时，KV Cache内存可能超过模型参数本身（如LLaMA-7B的权重约14GB，而KV Cache可达数十GB）。</font>
2. **计算效率下降**  
内存带宽成为瓶颈，尤其是当硬件（如GPU）的显存容量不足以容纳大Batch或长序列时，需频繁换入换出数据。

:::color5
**<font style="color:#601BDE;">2.优化方案</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 动态KV Cache（Dynamic KV Cache）</font>**

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">根据实际序列长度动态分配内存，避免预先分配最大长度内存。通过按需扩展缓存空间减少内存浪费。</font>

**<font style="color:rgb(51, 51, 51);">实现步骤</font>**

1. <font style="color:rgb(51, 51, 51);">初始化时分配较小的缓存空间（如512 Tokens）。</font>
2. <font style="color:rgb(51, 51, 51);">每次生成新Token时，检查剩余缓存空间。</font>
3. <font style="color:rgb(51, 51, 51);">空间不足时，按固定比例（如2倍）扩展缓存。</font>

```python
class DynamicKVCache:
    def __init__(self, init_size=512, growth_factor=2):
        self.cache_k = None
        self.cache_v = None
        self.init_size = init_size
        self.growth_factor = growth_factor
        self.current_size = 0

    def update(self, new_k, new_v, seq_len):
        if self.cache_k is None:
            self.current_size = self.init_size
            self.cache_k = torch.zeros((self.current_size, *new_k.shape[1:]), device=new_k.device)
            self.cache_v = torch.zeros((self.current_size, *new_v.shape[1:]), device=new_v.device)
        
        if seq_len >= self.current_size:
            # Expand cache
            new_size = max(int(self.current_size * self.growth_factor), seq_len + 1)
            new_cache_k = torch.zeros((new_size, *new_k.shape[1:]), device=new_k.device)
            new_cache_v = torch.zeros((new_size, *new_v.shape[1:]), device=new_v.device)
            new_cache_k[:self.current_size] = self.cache_k
            new_cache_v[:self.current_size] = self.cache_v
            self.cache_k = new_cache_k
            self.cache_v = new_cache_v
            self.current_size = new_size
        
        self.cache_k[seq_len] = new_k
        self.cache_v[seq_len] = new_v
        return self.cache_k[:seq_len+1], self.cache_v[:seq_len+1]

```

**<font style="color:rgb(51, 51, 51);">2. 内存复用（Memory Reuse）</font>**

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">对不再需要的旧Token的K/V内存进行复用。适用于滑动窗口注意力（Sliding Window Attention），仅保留最近W个Token的K/V。</font>

**<font style="color:rgb(51, 51, 51);">实现步骤</font>**

1. <font style="color:rgb(51, 51, 51);">维护一个固定大小的环形缓冲区（Ring Buffer）。</font>
2. <font style="color:rgb(51, 51, 51);">新Token写入时覆盖最旧的Token位置。</font>

```python
class RingBufferKVCache:
    def __init__(self, window_size=1024):
        self.window_size = window_size
        self.cache_k = torch.zeros((window_size, d_model))
        self.cache_v = torch.zeros((window_size, d_model))
        self.position = 0

    def update(self, new_k, new_v):
        # Overwrite oldest entry
        self.cache_k[self.position] = new_k
        self.cache_v[self.position] = new_v
        self.position = (self.position + 1) % self.window_size
        return self.cache_k, self.cache_v

```

**<font style="color:rgb(51, 51, 51);">3. 量化压缩（Quantization）</font>**

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">将K/V Cache的精度从FP16/FP32降低至INT8/INT4，减少内存占用（最高可压缩4倍）。通过反量化恢复精度。</font>

**<font style="color:rgb(51, 51, 51);">实现步骤</font>**

1. <font style="color:rgb(51, 51, 51);">对K/V矩阵进行动态量化（Dynamic Quantization）。</font>
2. <font style="color:rgb(51, 51, 51);">计算注意力前反量化回原始精度。</font>

```python
def quantize(tensor, bits=8):
    scale = tensor.abs().max() / (2 ** (bits - 1) - 1)
    quantized = torch.clamp(tensor / scale, -2 ** (bits - 1), 2 ** (bits - 1) - 1).to(torch.int8)
    return quantized, scale

def dequantize(quantized, scale):
    return quantized.to(scale.dtype) * scale

class QuantizedKVCache:
    def __init__(self):
        self.cache_k = []
        self.cache_v = []
        self.scales_k = []
        self.scales_v = []

    def update(self, new_k, new_v):
        q_k, s_k = quantize(new_k)
        q_v, s_v = quantize(new_v)
        self.cache_k.append(q_k)
        self.cache_v.append(q_v)
        self.scales_k.append(s_k)
        self.scales_v.append(s_v)
        return self.cache_k, self.cache_v

    def get(self, index):
        # Dequantize when needed
        return dequantize(self.cache_k[index], self.scales_k[index]), dequantize(self.cache_v[index], self.scales_v[index])

```

## vLLM
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#ED740C;">VLLM (VersatileLargeLanguageModel)是⼀个专⻔为⼤规模语⾔模型 (LLM) 推理设计的开源加速框架，通过创新的内存管理和并⾏化技术，显著提⾼了推理速度和吞吐量。</font>**<font style="color:#1f2329;">其中，</font>**<font style="color:#ED740C;">PagedAttention</font>**<font style="color:#1f2329;">是VLLM 的核⼼技术，专⻔⽤于解决 LLM 推理中的内存瓶颈问题，尤其是⾃回归⽣成任务中的键值 (KV) 缓存管理。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

<font style="color:rgb(51, 51, 51);">vLLM 的核心技术是 </font>**<font style="color:rgb(51, 51, 51);">PagedAttention</font>**<font style="color:rgb(51, 51, 51);">，灵感来自操作系统的虚拟内存分页机制，解决了传统LLM推理中KV缓存（Key-Value Cache）的内存碎片问题：</font>

1. **KV缓存分页管理**  
传统方法中，每个请求的KV缓存需要连续显存，导致长序列或突发请求时显存碎片化。vLLM将KV缓存划分为固定大小的块（例如4-16个注意力头的维度），允许非连续存储，按需分配和释放。
2. **块表（Block Table）**  
每个请求维护一个块表，记录其KV缓存的物理块位置。通过块索引快速定位数据，支持动态扩缩容。
3. **共享内存优化**  
在并行采样（如Beam Search）中，不同分支可共享父序列的KV块，减少冗余存储。

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

1. **初始化分块参数**  
设置块大小（如`block_size=16`）和最大序列长度，预计算每个块容纳的token数。
2. **请求处理**
    - <font style="color:rgb(51, 51, 51);">新请求到达时，分配初始块并记录到块表。</font>
    - <font style="color:rgb(51, 51, 51);">生成token时，若当前块已满，分配新块并更新块表。</font>
3. **注意力计算**  
通过块表索引物理块，执行分块注意力计算：

```python
python

# 伪代码：分块注意力计算
for block in block_table:
    keys = load_k_block(block)
    values = load_v_block(block)
    scores = query @ keys.transpose()
    output += scores @ values
```

4. **内存回收**  
请求完成后，释放块并标记为空闲，供后续请求复用。

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">吞吐量提升2-4倍</font> | <font style="color:rgb(51, 51, 51);">仅支持部分模型架构（如GPT、LLAMA）</font> |
| <font style="color:rgb(51, 51, 51);">显存利用率提高，支持更长序列</font> | <font style="color:rgb(51, 51, 51);">需CUDA环境，不支持非NVIDIA GPU</font> |
| <font style="color:rgb(51, 51, 51);">低延迟，适合高并发</font> | <font style="color:rgb(51, 51, 51);">动态批处理对极端长度差异敏感</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">在线推理服务</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">如聊天机器人、API服务，需处理数千QPS的请求。</font>
2. **<font style="color:rgb(51, 51, 51);">批量文本生成</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">广告文案、代码生成等大规模任务。</font>
3. **<font style="color:rgb(51, 51, 51);">研究实验</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">快速迭代不同采样策略（温度、top-p）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合分块策略</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">动态调整块大小（如短序列用小块，长序列用大块）。</font>
2. **<font style="color:rgb(51, 51, 51);">量化集成</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">结合4-bit量化，进一步压缩显存。</font>
3. **<font style="color:rgb(51, 51, 51);">异构内存管理</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">使用CPU内存扩展缓存能力（类似HBM-SSD分层存储）。</font>
4. **<font style="color:rgb(51, 51, 51);">模型架构适配</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">扩展支持MQA（Multi-Query Attention）和MoE架构。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from vllm import LLM, SamplingParams

# 定义模型和采样参数
model = LLM(model="meta-llama/Llama-2-7b-chat-hf", tensor_parallel_size=2)  # 张量并行
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)

# 批量推理
prompts = ["A robot may not injure a human being,",
           "The capital of France is"]
outputs = model.generate(prompts, sampling_params)

# 输出结果
for output in outputs:
    print(f"Prompt: {output.prompt}\n"
          f"Generated text: {output.outputs[0].text}\n")

```

```python
model = LLM(
    model="gpt2",
    max_num_seqs=256,  # 最大并发数
    block_size=16,     # 块大小（token数）
    gpu_memory_utilization=0.9  # 显存利用率阈值
)

```

### <font style="color:#6425d0;">PagedAttention机制</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Page Attention 是一种针对长序列处理优化的注意力机制，旨在降低传统自注意力的内存和计算开销，同时保持对长距离依赖的建模能力。其核心思想借鉴计算机系统中的</font>**<font style="color:#ED740C;">分页机制</font>**<font style="color:rgb(51, 51, 51);">，将输入序列分割为多个“页面”（块），动态管理这些块的计算和存储，从而优化资源使用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

1. **传统自注意力瓶颈**  
Transformer的自注意力复杂度为O(N²)，在处理长序列时显存占用激增，尤其在大batch size下，成为训练/推理的主要瓶颈。
2. **分页管理思想**  
Page Attention将输入序列划分为固定大小的页面（Page），每个页面包含连续的token。计算注意力时：
    - **<font style="color:rgb(51, 51, 51);">页面内（Intra-Page）</font>**<font style="color:rgb(51, 51, 51);">：计算当前页面内所有token间的局部注意力。</font>
    - **<font style="color:rgb(51, 51, 51);">页面间（Inter-Page）</font>**<font style="color:rgb(51, 51, 51);">：按需加载其他页面，计算跨页面的稀疏注意力（如相邻页或关键页）。</font>
3. **动态加载机制**  
通过类似虚拟内存的换页策略，仅保留活跃页面在高速内存（如GPU显存）中，非活跃页面暂存于低速内存（如CPU内存或磁盘），按需动态交换，显著降低峰值显存占用。

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">假设输入序列长度N，页面大小P，总页数M=N/P：</font>

1. **分块（Paging）**  
将输入序列划分为M个页面：`X = [X₁, X₂, ..., Xₘ]`，每个Xᵢ ∈ ℝ^{P×d}。
2. **页面内注意力**  
对每个页面Xᵢ，计算局部注意力输出Oᵢ：

```python
Qᵢ, Kᵢ, Vᵢ = XᵢW_Q, XᵢW_K, XᵢW_V
Aᵢ = softmax(QᵢKᵢ^T / √d)  # 形状 [P, P]
Oᵢ = AᵢVᵢ                   # 形状 [P, d]
```

3. **页面间注意力**  
根据策略（如滑动窗口、关键页选择）加载相关页面Xⱼ，计算跨页面注意力：

```python
Qᵢ, Kⱼ, Vⱼ = XᵢW_Q, XⱼW_K, XⱼW_V
Aᵢⱼ = softmax(QᵢKⱼ^T / √d)  # 形状 [P, P]
Oᵢⱼ = AᵢⱼVⱼ                  # 形状 [P, d]
```

4. **结果聚合**  
合并页面内和跨页面结果，得到最终输出：

```python
Oᵢ = Oᵢ + ∑ⱼ∈Neighbor(i) Oᵢⱼ
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

  
**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">显存优化</font>**<font style="color:rgb(51, 51, 51);">：显存占用从O(N²)降至O(MP²)，M为页面数。</font>
+ **<font style="color:rgb(51, 51, 51);">计算高效</font>**<font style="color:rgb(51, 51, 51);">：分块计算利于并行化和硬件加速。</font>
+ **<font style="color:rgb(51, 51, 51);">扩展性强</font>**<font style="color:rgb(51, 51, 51);">：支持超长序列处理（如百万级token）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">块间跳转可能引入额外内存访问开销。</font>
+ <font style="color:rgb(51, 51, 51);">块大小需调优，过小会增加管理开销，过大可能浪费内存。</font>  


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">处理超长文本（如文档摘要、代码生成）。</font>
+ <font style="color:rgb(51, 51, 51);">高并发场景下多序列并行推理（如聊天服务器）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态块大小</font>**<font style="color:rgb(51, 51, 51);">：根据序列长度动态调整块大小。</font>
+ **<font style="color:rgb(51, 51, 51);">块预取</font>**<font style="color:rgb(51, 51, 51);">：预测未来需要的块，提前加载到高速缓存。</font>
+ **<font style="color:rgb(51, 51, 51);">异构存储</font>**<font style="color:rgb(51, 51, 51);">：将低频访问的块迁移到CPU内存或磁盘。</font>  


:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class PageAttention(nn.Module):
    def __init__(self, d_model, n_heads, page_size=64):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.page_size = page_size
        self.head_dim = d_model // n_heads
        
        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)
        
    def forward(self, x):
        # x: [batch, seq_len, d_model]
        B, N, d = x.shape
        P = self.page_size
        M = (N + P - 1) // P  # 计算总页数
        
        # 分页填充并调整形状
        x_padded = nn.functional.pad(x, (0,0,0, M*P - N))
        pages = rearrange(x_padded, 'b (m p) d -> b m p d', p=P)
        
        Q = self.Wq(pages)
        K = self.Wk(pages)
        V = self.Wv(pages)
        
        # 分头处理
        Q = rearrange(Q, 'b m p (h d) -> b h m p d', h=self.n_heads)
        K = rearrange(K, 'b m p (h d) -> b h m p d', h=self.n_heads)
        V = rearrange(V, 'b m p (h d) -> b h m p d', h=self.n_heads)
        
        outputs = []
        for m in range(M):
            # 页面内注意力
            intra_Q = Q[:, :, m]
            intra_K = K[:, :, m]
            intra_V = V[:, :, m]
            attn = torch.einsum('bhpd,bhqd->bhpq', intra_Q, intra_K) / (self.head_dim**0.5)
            attn = torch.softmax(attn, dim=-1)
            intra_out = torch.einsum('bhpq,bhqd->bhp d', attn, intra_V)
            
            # 页面间注意力（示例：关注前一页）
            if m > 0:
                inter_K = K[:, :, m-1]
                inter_V = V[:, :, m-1]
                inter_attn = torch.einsum('bhpd,bhqd->bhpq', intra_Q, inter_K) / (self.head_dim**0.5)
                inter_attn = torch.softmax(inter_attn, dim=-1)
                inter_out = torch.einsum('bhpq,bhqd->bhp d', inter_attn, inter_V)
                intra_out += inter_out
            
            outputs.append(intra_out)
        
        # 合并结果
        out = torch.cat(outputs, dim=2)
        out = rearrange(out, 'b h m p d -> b (m p) (h d)')[:, :N]  # 去除填充
        return self.out(out)

```



### <font style="color:#6425d0;">Continuous Batching机制</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Continuous Batching（连续批处理）是一种针对大模型推理优化的动态批处理技术，通过打破传统静态批处理的固定批次限制，在推理过程中</font>**<font style="color:rgb(51, 51, 51);">动态插入新请求</font>**<font style="color:rgb(51, 51, 51);">并</font>**<font style="color:rgb(51, 51, 51);">按需调整批次大小</font>**<font style="color:rgb(51, 51, 51);">，显著提升硬件利用率并降低请求延迟。其核心思想源自系统调度中的</font>**<font style="color:rgb(51, 51, 51);">流水线并行</font>**<font style="color:rgb(51, 51, 51);">，代表工作包括Orca、vLLM等推理框架的优化实现。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738837876714-8a7b7721-2a0f-49ee-8e9a-90cbef3079b2.png)

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

<font style="color:#1f2329;">另⼀个提升VLLM推理速度的重要机制是 </font>**<font style="color:#74B602;">ContinuousBatching</font>**<font style="color:#1f2329;">，它优化了批处理过程。</font>**<font style="color:#74B602;">传统的批处理⽅法（staticbatching）要求所有输⼊序列的⻓度对⻬，这意味着较短的句⼦需要等待较⻓句⼦⽣成完毕，导致 GPU 计算资源被浪费。</font>**

<font style="color:#1f2329;">VLLM 采⽤Continuous Batching，即每当某个句⼦的推理完成时，GPU 会⽴即填充下⼀个句⼦的</font><font style="color:black;">  </font><font style="color:#1f2329;">token，⽽</font>**<font style="color:#74B602;">不需要等待整个批次的推理完成</font>**<font style="color:#1f2329;">。这种动态的批次管理⽅式充分利⽤了 GPU 的计算能⼒，减少了等待时间，极⼤提⾼了吞吐量。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">请求队列管理</font>**<font style="color:rgb(51, 51, 51);">：维护等待队列（Pending Queue）和运行队列（Running Queue）。</font>
2. **<font style="color:rgb(51, 51, 51);">迭代处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">从等待队列中选择可运行的请求（基于最大批大小）。</font>
    - <font style="color:rgb(51, 51, 51);">合并所有运行中请求的输入，执行模型前向计算。</font>
    - <font style="color:rgb(51, 51, 51);">移除已生成结束符的请求，释放资源。</font>
3. **<font style="color:rgb(51, 51, 51);">状态更新</font>**<font style="color:rgb(51, 51, 51);">：将新生成的token追加到各请求的生成序列中。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">提升GPU利用率，减少空闲时间。</font>
    - <font style="color:rgb(51, 51, 51);">降低用户感知的延迟（尤其对短请求）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">调度算法复杂度高，需处理动态内存分配。</font>
    - <font style="color:rgb(51, 51, 51);">长尾请求可能阻塞批次整体进度。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">高吞吐量的在线推理服务（如GPT-4 API）。</font>
+ <font style="color:rgb(51, 51, 51);">流式生成场景（如实时翻译、语音助手）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优先级调度</font>**<font style="color:rgb(51, 51, 51);">：为高优先级请求分配更多资源。</font>
+ **<font style="color:rgb(51, 51, 51);">推测执行</font>**<font style="color:rgb(51, 51, 51);">：预先生成长度，减少迭代次数。</font>
+ **<font style="color:rgb(51, 51, 51);">混合批处理</font>**<font style="color:rgb(51, 51, 51);">：结合静态批处理处理离线任务。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class ContinuousBatcher:
    def __init__(self, max_batch_size=32):
        self.pending_queue = []
        self.running_queue = []
        self.max_batch_size = max_batch_size

    def add_request(self, input_text):
        self.pending_queue.append({"input": input_text, "output": []})

    def step(self, model):
        # 动态填充批次
        while len(self.running_queue) < self.max_batch_size and self.pending_queue:
            self.running_queue.append(self.pending_queue.pop(0))

        # 准备输入
        inputs = [req["output"][-1] if req["output"] else req["input"] for req in self.running_queue]
        input_ids = tokenizer(inputs, return_tensors="pt", padding=True).input_ids

        # 模型推理
        outputs = model.generate(input_ids, max_new_tokens=1)

        # 更新状态并移除完成请求
        new_running_queue = []
        for req, output in zip(self.running_queue, outputs):
            req["output"].append(output)
            if output != eos_token:
                new_running_queue.append(req)
        self.running_queue = new_running_queue

```





<font style="color:#1f2329;"></font>

## <font style="color:#1f2329;">FlashAttention</font>
:::success
**<font style="color:#1f2329;">背景：</font>**<font style="color:#1f2329;">Transformer的核⼼组件是⾃注意⼒机制（Self-Attention），然⽽，传统的  ⾃注意⼒计算在处理⻓序列时，⾯临着计算量⼤和内存占⽤⾼的问题。FlashAttention是⼀种⾼效的⾃注意⼒计算算法，旨在解决这些问题。在传统实现中，⾃注意⼒计算涉及到⼤型矩阵的乘法和存储。L为序列长度</font>

+ <font style="color:#1f2329;">计算复杂度： </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">L</font>_<sup><font style="color:#1f2329;">2</font></sup>_<font style="color:#1f2329;">d</font>_<sub>_<font style="color:#1f2329;">k</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font>
+ <font style="color:#1f2329;">内存占⽤： 需要存储 </font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">的注意⼒矩阵 ，内存占⽤为 </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">L</font>_<sup><font style="color:#1f2329;">2</font></sup><font style="color:#1f2329;"> </font><font style="color:#1f2329;">)</font>

**<font style="color:#74B602;">对于⻓序列，内存占⽤和计算量都会急剧增加，导致效率低下。</font>**

:::

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Fla</font><font style="color:#1f2329;">shAttention提供了⼀种⾼效且数值稳定的⾃注意⼒计算⽅法 ，通过优化内存访问和计算</font>

<font style="color:#1f2329;">流程，解决了传统⾃注意⼒在⻓序列处理中的</font>**<font style="color:#ED740C;">内存和计算瓶颈</font>**<font style="color:#1f2329;">。总结其优势：</font>

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">内存⾼效：⼤幅降低内存占⽤ ，适合处理⻓序列。</font>
+ <font style="color:#1f2329;">计算⾼效：减少访存开销 ，提⾼计算速度。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:#117CEE;">问题本质</font>**

+ <font style="color:#de7802;">内存瓶颈</font><font style="color:#1f2329;">：GPU 的内存带宽限制了⾃注意⼒的计算速度。</font>
+ <font style="color:#de7802;">访存开销</font><font style="color:#1f2329;">：传统算法需要多次读取和写⼊ GPU 内存 ，导致⼤量的访存操作。</font>

**<font style="color:#117CEE;">核心思想</font>**

<font style="color:#1f2329;">FlashAttention</font><font style="color:#1f2329;">通过以下⽅式优化⾃注意⼒计算：</font>

+ <font style="color:#de7802;">块处理（ Blocking） </font><font style="color:#1f2329;">：将计算划分为⼩块 ，逐块处理，减少⼀次性需要的内存。</font>
+ <font style="color:#de7802;">IO 感知（IO-Awareness）</font><font style="color:#1f2329;">：优化内存访问模式，最⼤化数据在⾼速缓存中的使⽤ ，减少访存开销。</font>
+ <font style="color:#de7802;">数值稳定性</font><font style="color:#1f2329;">：在块内进⾏归⼀化 ，避免数值溢出。</font>

**<font style="color:#117CEE;">实现步骤</font>**

1. **<font style="color:#1f2329;">块划分</font>**<font style="color:#1f2329;">：将序列⻓度</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">划分为多个块，每个块的⼤⼩为</font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">。例如，序列⻓度为 1024，块⼤⼩为 128，则有 8 个块。</font>
2. **<font style="color:#1f2329;">逐块计算</font>**
    - <font style="color:#1f2329;">计算块间的注意⼒：对于每个查询块和键块，计算局部的注意⼒值。</font>
    - <font style="color:#1f2329;">内存占⽤优化：只在寄存器或⾼速缓存中存储当前块的数据，避免将整个</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L</font>_

<font style="color:#1f2329;">的注意⼒矩阵存⼊内存。</font>

3. **数值稳定的softmax计算**
    - <font style="color:#1f2329;">局部归⼀化：在块内进⾏Softmax 计算，使⽤数值稳定的算法，避免指数计算中的溢出。</font>
    - <font style="color:#1f2329;">累积计算：逐块累积注意⼒值和归⼀化因⼦，确保最终结果的准确性。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

1. **减少内存占用**
    - <font style="color:#de7802;">块级处理：</font><font style="color:#1f2329;">避免存储整个注意   ⼒矩阵，内存占⽤从 </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">L</font>_<sup><font style="color:#1f2329;">2</font></sup><font style="color:#1f2329;"> </font><font style="color:#1f2329;">) </font><font style="color:#1f2329;">降⾄  </font>_<font style="color:#1f2329;">O</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">LB</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;">。</font>
    - <font style="color:#de7802;">适合⻓序列</font><font style="color:#1f2329;">：能够⾼效处理⻓达⼏千甚⾄上万⻓度的序列。</font>
2. **提高计算效率**
    - <font style="color:#2ea121;">减少访存操作：</font><font style="color:#1f2329;">优化内存访问模式，提⾼了数据在⾼速缓存中的命中率。</font>
    - <font style="color:#2ea121;">GPU 加速：</font><font style="color:#1f2329;">充分利⽤GPU 的计算能⼒和寄存器优势。</font>
3. **数值稳定**
    - <font style="color:#117CEE;">局部归一化：</font><font style="color:#1f2329;">在计算过程中保持数值稳定。避免了传统⽅法中的数值溢出和下溢问题。</font>

:::color5
**<font style="color:#601BDE;">3.与传统注意力对比</font>**

:::

1. **内存占用对比**
    - <font style="color:#de7802;">传统⾃注意⼒：</font><font style="color:#1f2329;">需要存储</font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">的矩阵，内存占⽤⼤。</font>
    - <font style="color:#de7802;">FlashAttention</font><font style="color:#1f2329;">：内存占⽤与   块⼤⼩</font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">成正⽐，⼤幅降低了内存需求。</font>
2. **计算速度对比**
    - <font style="color:#2ea121;">减少访存操作传统⽅法：</font><font style="color:#1f2329;">由于⼤量的访存操作，计算速度受限于内存带宽。</font>
    - <font style="color:#2ea121;">FlashAttention：</font><font style="color:#1f2329;">减少了访存次数，计算速度主要由计算单  元决定，更快。</font>
3. **数值精确对比**
    - <font style="color:#245bdb;">传统⽅法：</font><font style="color:#1f2329;">可能出现数值不稳定，特别是在⻓序列或⾼维度下。</font>
    - <font style="color:#245bdb;">FlashAttention：</font><font style="color:#1f2329;">通过数值稳定的算法，确保了计算精度。</font>

:::color5
**<font style="color:#601BDE;">4.代码实现</font>**

:::

```python
import torch

def flash_attention(Q, K, V, block_size=64):
    """
    Flash Attention的PyTorch实现
    
    参数:
        Q: 查询张量，形状为 (batch_size, num_heads, seq_len, head_dim)
        K: 键张量，形状同Q
        V: 值张量，形状同Q
        block_size: 分块大小，控制内存使用
        
    返回:
        O: 注意力输出，形状同Q
    """
    batch_size, num_heads, seq_len, head_dim = Q.shape
    # 初始化输出和中间变量
    O = torch.zeros_like(Q)
    M = torch.full((batch_size, num_heads, seq_len), -float('inf'), device=Q.device, dtype=Q.dtype)
    L = torch.zeros_like(M)
    
    # 分块处理Q序列
    for i in range(0, seq_len, block_size):
        Q_block = Q[:, :, i:i+block_size, :]  # 当前Q块 (B, H, block_q, D)
        block_q = Q_block.size(2)
        
        # 初始化当前块的中间变量
        O_i = torch.zeros((batch_size, num_heads, block_q, head_dim), device=Q.device, dtype=Q.dtype)
        M_i = M[:, :, i:i+block_size].clone()  # (B, H, block_q)
        L_i = L[:, :, i:i+block_size].clone()  # (B, H, block_q)
        
        # 分块处理K/V序列
        for j in range(0, seq_len, block_size):
            K_block = K[:, :, j:j+block_size, :]  # 当前K块 (B, H, block_k, D)
            V_block = V[:, :, j:j+block_size, :]  # 当前V块 (B, H, block_k, D)
            block_k = K_block.size(2)
            
            # 1. 计算块间注意力得分
            S_ij = torch.einsum('bhid,bhjd->bhij', Q_block, K_block)  # (B, H, block_q, block_k)
            
            # 2. 计算当前块的行最大值
            m_curr = S_ij.max(dim=-1).values  # (B, H, block_q)
            
            # 3. 更新最大值并计算指数项
            m_new = torch.maximum(m_curr, M_i)
            exp_prev = torch.exp(M_i - m_new)  # 之前累积项的缩放因子
            exp_curr = torch.exp(S_ij - m_new.unsqueeze(-1))  # 当前块的指数值
            
            # 4. 更新累积求和项
            L_new = exp_prev * L_i + exp_curr.sum(dim=-1)
            
            # 5. 更新输出值
            O_i = exp_prev.unsqueeze(-1) * O_i + torch.einsum('bhij,bhjd->bhid', exp_curr, V_block)
            
            # 保存中间变量供下一个块使用
            M_i = m_new
            L_i = L_new
        
        # 将当前Q块的结果写回最终输出
        O[:, :, i:i+block_size, :] = O_i
        L[:, :, i:i+block_size] = L_i
    
    # 最终归一化处理
    O = O / (L.unsqueeze(-1) + 1e-6)  # 添加极小值防止除以零
    return O

batch_size = 2
num_heads = 4
seq_len = 512
head_dim = 64

Q = torch.randn(batch_size, num_heads, seq_len, head_dim)
K = torch.randn_like(Q)
V = torch.randn_like(Q)

output = flash_attention(Q, K, V, block_size=64)
print(output.shape)  # torch.Size([2, 4, 512, 64])

```

<font style="color:#1f2329;"></font>

## <font style="color:#1f2329;">投机采样（</font><font style="color:rgb(51, 51, 51);">Speculative Sampling</font><font style="color:#1f2329;">）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：自回归模型（如GPT、LLaMA）生成文本时需逐个token预测，计算复杂度为O(n²)，推理延迟高。传统优化方法（如KV缓存、量化）存在瓶颈。</font>

:::

:::color3
**简介：****<font style="color:rgb(51, 51, 51);">投机采样</font>**<font style="color:rgb(51, 51, 51);">（Google 2022）通过“</font>**<font style="color:#ED740C;">草稿模型+并行验证</font>**<font style="color:rgb(51, 51, 51);">”机制，将大模型推理速度提升2-4倍。</font>

+ **Propose Model**<font style="color:rgb(51, 51, 51);">：投机采样过程中的小模型，用于</font>**<font style="color:#ED740C;">生成草稿token</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">Score Model</font>**<font style="color:rgb(51, 51, 51);">：投机采样过程中的大模型，</font>**<font style="color:#ED740C;">用于对草稿token进行打分，从而决定接收多少个token</font>**<font style="color:rgb(51, 51, 51);">。Score Model为原始生成Token的LLM模型。</font>
+ **<font style="color:rgb(51, 51, 51);">Prefill</font>**<font style="color:rgb(51, 51, 51);">：预填充阶段，把所有的prompt喂给模型做forward计算，输出首个token。投机采样的Score过程使用了类似的过程。</font>
+ **<font style="color:rgb(51, 51, 51);">Decode</font>**<font style="color:rgb(51, 51, 51);">：解码阶段，</font><font style="color:rgb(37, 41, 51);">以自回归的方式逐个生成新的token</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

**<font style="color:rgb(51, 51, 51);">核心步骤</font>**

1. **<font style="color:rgb(51, 51, 51);">草稿生成</font>**<font style="color:rgb(51, 51, 51);">：小模型（Propose Model）快速生成γ个候选tokens：x</font><sub><font style="color:rgb(51, 51, 51);">t+1</font></sub><font style="color:rgb(51, 51, 51);">,...,x</font><sub><font style="color:rgb(51, 51, 51);">t+γ</font></sub><font style="color:rgb(51, 51, 51);">。</font>
2. **<font style="color:rgb(51, 51, 51);">并行验证</font>**<font style="color:rgb(51, 51, 51);">：大模型（Score Model）并行计算所有位置的条件概率分布P(x</font><sub><font style="color:rgb(51, 51, 51);">t+i</font></sub><font style="color:rgb(51, 51, 51);">∣x</font><sub><font style="color:rgb(51, 51, 51);">1:t+i−1</font></sub><font style="color:rgb(51, 51, 51);">)。</font>
3. **<font style="color:rgb(51, 51, 51);">接受决策</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对每个候选token x</font><sub><font style="color:rgb(51, 51, 51);">t+i</font></sub><font style="color:rgb(51, 51, 51);">，计算接受概率</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741943536347-16747c87-aefa-4461-a1ef-a88816eda2f5.png)

    - <font style="color:rgb(51, 51, 51);">按顺序判定：若r</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><font style="color:rgb(51, 51, 51);">>rand(0,1)则接受，否则拒绝并终止验证</font>
4. **<font style="color:rgb(51, 51, 51);">回退修正</font>**<font style="color:rgb(51, 51, 51);">：若在位置k拒绝，则从P</font><sub><font style="color:rgb(51, 51, 51);">target</font></sub><font style="color:rgb(51, 51, 51);">(x</font><sub><font style="color:rgb(51, 51, 51);">t+k</font></sub><font style="color:rgb(51, 51, 51);">)重新采样新token。</font>

**<font style="color:rgb(51, 51, 51);">数学表达</font>**

<font style="color:rgb(51, 51, 51);">最终输出长度为  N = 原生成步数 + γ × 接受率</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">无需修改原模型</font> | <font style="color:rgb(51, 51, 51);">需维护草稿模型</font> |
| <font style="color:rgb(51, 51, 51);">理论加速比2-5x</font> | <font style="color:rgb(51, 51, 51);">长文本生成可能退化为普通解码</font> |
| <font style="color:rgb(51, 51, 51);">兼容现有推理框架</font> | <font style="color:rgb(51, 51, 51);">草稿模型质量影响效果</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">低延迟对话系统</font>**<font style="color:rgb(51, 51, 51);">：如客服机器人需快速响应</font>
+ **<font style="color:rgb(51, 51, 51);">长文本生成</font>**<font style="color:rgb(51, 51, 51);">：小说/代码生成时减少等待时间</font>
+ **<font style="color:rgb(51, 51, 51);">边缘设备部署</font>**<font style="color:rgb(51, 51, 51);">：结合量化降低大模型计算开销</font>

:::color5
**<font style="color:#601BDE;">4.改进方案</font>**

:::

| **方法** | **说明** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">动态γ调整</font>** | <font style="color:rgb(51, 51, 51);">根据历史接受率动态调整候选长度</font> |
| **<font style="color:rgb(51, 51, 51);">共享参数</font>** | <font style="color:rgb(51, 51, 51);">草稿模型使用大模型的前几层（如DeepMind的Medusa）</font> |
| **<font style="color:rgb(51, 51, 51);">多草稿投票</font>** | <font style="color:rgb(51, 51, 51);">并行多个草稿模型生成候选</font> |
| **<font style="color:rgb(51, 51, 51);">强化学习训练</font>** | <font style="color:rgb(51, 51, 51);">优化草稿模型生成可接受性</font> |


:::color5
**<font style="color:#601BDE;">5.代码实现</font>**

:::

```python
import torch
import torch.nn.functional as F

def speculative_sampling(target_model, draft_model, input_ids, max_len, gamma=5):
    """
    target_model: 原始大模型（需支持并行前向）
    draft_model: 草稿小模型
    input_ids: 初始输入序列 [1, seq_len]
    gamma: 最大候选长度
    """
    current_seq = input_ids
    for _ in range(max_len):
        # Step 1: 草稿模型生成候选
        with torch.no_grad():
            draft_logits = draft_model(current_seq).logits[:, -gamma-1:-1]  # 生成γ个位置
            draft_probs = F.softmax(draft_logits, dim=-1)
            draft_tokens = torch.multinomial(draft_probs.view(-1, draft_probs.shape[-1]), 1)\
                            .view(draft_probs.shape[0], gamma)
        
        # Step 2: 拼接候选并并行验证
        candidate_seq = torch.cat([current_seq, draft_tokens], dim=1)
        target_logits = target_model(candidate_seq).logits[:, -gamma-1:-1]
        target_probs = F.softmax(target_logits, dim=-1)
        
        # Step 3: 计算接受概率
        accept_probs = torch.min(
            torch.ones_like(draft_probs), 
            target_probs / (draft_probs + 1e-8)
        )  # 防止除零
        
        # Step 4: 顺序判定接受位置
        accepted = 0
        for i in range(gamma):
            rand = torch.rand(1).item()
            if rand < accept_probs[0, i].item():
                accepted += 1
            else:
                break  # 遇到第一个拒绝则停止
        
        # 更新当前序列
        current_seq = torch.cat([current_seq, draft_tokens[:, :accepted]], dim=1)
        
        # 回退修正（若有拒绝）
        if accepted < gamma:
            last_token_logits = target_logits[:, accepted]
            last_token = torch.multinomial(F.softmax(last_token_logits, dim=-1), 1)
            current_seq = torch.cat([current_seq, last_token], dim=1)
        
        if current_seq.shape[1] >= max_len:
            break
            
    return current_seq[0].tolist()

```



## MTP（Multi Token Prediction） 多token预测<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">当前主流的大模型(LLMs)都是decoder-base的模型结构，也就是无论在模型训练还是在推理阶段，对于一个序列的生成过程，都是</font>**<font style="color:#74B602;">token-by-token</font>**<font style="color:rgb(25, 27, 31);">的。每次在生成一个token的时候，都要频繁跟访存交互，加载KV-Cache，再通过多层网络做完整的前向计算。</font>**<font style="color:#117CEE;">对于这样的访存密集型的任务，通常会因为访存效率形成训练或推理的瓶颈。</font>**

<font style="color:rgb(25, 27, 31);">针对token-by-token生成效率的瓶颈，业界很多方法来优化，包括减少存储的空间和减少访存次数等，进而提升训练和推理性能。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">本文要学习的MTP方法，也是</font>**<font style="color:#ED740C;">优化训练和推理效率的一个分支系列</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">核心思想：通过解码阶段的优化，将</font>**<font style="color:#ED740C;">1-token的生成，转变成multi-token的生成</font>**<font style="color:rgb(25, 27, 31);">，从而提升训练和推理的性能。具体来说:</font>

+ <font style="color:rgb(25, 27, 31);">训练阶段：一次生成多个后续token，可以一次学习多个位置的label，进而有效提升样本的利用效率，提升训练速度；</font>
+ <font style="color:rgb(25, 27, 31);">推理阶段：通过一次生成多个token，实现成倍的推理加速来提升推理性能。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**https://zhuanlan.zhihu.com/p/18056041194**](https://zhuanlan.zhihu.com/p/18056041194)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447136606-cd92c633-6c7c-4d0b-b1e1-f4de34eaef55.png)

### deepseek's MTP<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">MTP的示意图如下所示，在训练阶段模型共享一个基础结构，然后顶层有4个head一次性输出4个预估token。而在推断阶段支采用next-token对应输出的head。</font>

**paper：**[**DeepSeek-V3 Technical Report**](https://arxiv.org/pdf/2412.19437)

**参考：**[**MTP（Multi-Token Prediction）的前世今生**](https://zhuanlan.zhihu.com/p/18056041194)

:::

:::color5
**<font style="color:#601BDE;">1.MTP结构  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">DeepSeek的MTP的设计，如下图所示，乍看上去也是多头，但结构略复杂。且论文中也强调，在实现上保留了</font>**<font style="color:#74B602;">序列推理的连接关系（causal chain）</font>****<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">如图中，从一个Module链接到后继Module的箭头。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447961354-7887b237-cfa8-483d-a6f6-e7f00fcadf9f.png)

<font style="color:rgb(25, 27, 31);">如上图所示，用 </font><font style="color:rgb(25, 27, 31);">D</font><font style="color:rgb(25, 27, 31);"> 个顺序的模块，预测 </font><font style="color:rgb(25, 27, 31);">D</font><font style="color:rgb(25, 27, 31);"> 个tokens。每个MTP模块的具体结构：</font>

+ **<font style="color:rgb(25, 27, 31);">输入token首先接入一层共享的embedding layer</font>**
+ **<font style="color:rgb(25, 27, 31);">对于第</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">i</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">个token</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">i</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">和第</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">k</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">个预测深度</font>**
    - <font style="color:rgb(25, 27, 31);">我们首先将第 </font><font style="color:rgb(25, 27, 31);">k−1</font><font style="color:rgb(25, 27, 31);"> 层的的隐层输出 </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k−1</font></sup><font style="color:rgb(25, 27, 31);">∈R</font><sup><font style="color:rgb(25, 27, 31);">d</font></sup><font style="color:rgb(25, 27, 31);"> 做归一化处理 </font><font style="color:rgb(25, 27, 31);">RMSNorm(h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k−1</font></sup><font style="color:rgb(25, 27, 31);">)</font>
    - <font style="color:rgb(25, 27, 31);">再对第 </font><font style="color:rgb(25, 27, 31);">i+k</font><font style="color:rgb(25, 27, 31);"> 位置的token embedding：</font><font style="color:rgb(25, 27, 31);">Emb(t</font><sub><font style="color:rgb(25, 27, 31);">i+k</font></sub><font style="color:rgb(25, 27, 31);">)∈R</font><sup><font style="color:rgb(25, 27, 31);">d</font></sup><font style="color:rgb(25, 27, 31);"> 做归一化处理 </font><font style="color:rgb(25, 27, 31);">RMSNorm(Emb(t</font><sub><font style="color:rgb(25, 27, 31);">i+k</font></sub><font style="color:rgb(25, 27, 31);">))</font>
    - <font style="color:rgb(25, 27, 31);">将上述两个结果concat后，通过投影矩阵 </font><font style="color:rgb(25, 27, 31);">Mk∈R</font><sup><font style="color:rgb(25, 27, 31);">d×2d</font></sup><font style="color:rgb(25, 27, 31);"> 做一层线性变换得到 </font><font style="color:rgb(25, 27, 31);">h</font><sup><font style="color:rgb(25, 27, 31);">,</font></sup><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);">∈R</font><sub><font style="color:rgb(25, 27, 31);">d</font></sub>
    - <font style="color:rgb(25, 27, 31);">上述过程如下公式 </font><font style="color:rgb(25, 27, 31);">(21)</font><font style="color:rgb(25, 27, 31);"> 所示（当 </font><font style="color:rgb(25, 27, 31);">k=1</font><font style="color:rgb(25, 27, 31);"> 时， </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k−1</font></sup><font style="color:rgb(25, 27, 31);"> 对main model的隐层表征）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447803442-64cae6e8-c7db-42d8-b35d-16b4abeb25c8.png)

+ <font style="color:rgb(25, 27, 31);">再将 </font><font style="color:rgb(25, 27, 31);">h</font><sup><font style="color:rgb(25, 27, 31);">,</font></sup><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);"> 输入到Transformer层，获得第 </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 个预测深度的输出： </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);"> 。如公式 </font><font style="color:rgb(25, 27, 31);">(22)</font><font style="color:rgb(25, 27, 31);"> 所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447803244-ab56a9c2-f671-4e7d-9b54-5fd6aa347c2c.png)

+ <font style="color:rgb(25, 27, 31);">最后将 </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);"> 通过一个各Module共享的映射矩阵 </font><font style="color:rgb(25, 27, 31);">OutHead∈R</font><sup><font style="color:rgb(25, 27, 31);">V×d</font></sup><font style="color:rgb(25, 27, 31);"> 变换，再过 </font><font style="color:rgb(25, 27, 31);">softmax(.)</font><font style="color:rgb(25, 27, 31);"> 处理，计算出词表 </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);"> 维度的输出概率，这里注意： </font><font style="color:rgb(25, 27, 31);">h</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">k</font></sup><font style="color:rgb(25, 27, 31);">  的 </font><font style="color:rgb(25, 27, 31);">label</font><font style="color:rgb(25, 27, 31);"> 是对应 </font><font style="color:rgb(25, 27, 31);">i+1+k</font><font style="color:rgb(25, 27, 31);"> 位置的token。如公式 </font><font style="color:rgb(25, 27, 31);">(23)</font><font style="color:rgb(25, 27, 31);"> 所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447803319-fbdff04d-6926-424e-88ca-39b0fdda56f1.png)

:::color5
**<font style="color:#601BDE;">2.MTP模型训练  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**MTP多头训练，样本构建示意图**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744448119270-f03a2180-4741-4249-b1c7-fde5ccb9f7af.jpeg)

<font style="color:rgb(25, 27, 31);">通过CrossEntropyLoss计算每个MTP Module Head的损失，如公式</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">24</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744448148917-890a5386-3f91-48b7-80f8-080d3f6cab7c.png)

> 再解释下公式 (24) 的下标，2+k:T+1 表示label范围的下标  
参考上图8，就非常好理解：  
**起始下标 **2+k ：MTP Model 1 是预测 next next的token，也就是输入第一个token是 t1 ，预测第一个label token是 t(2+1)=t3 ，以此类推， MTP Model k，输入第一个token是 t1， 预测第一个token是 t2+k  
**结束下标 **T+1 ：所有sequence样本默认在原序列上额外增加的一个eos token，所以token下标为序列长度 T+1
>

<font style="color:rgb(25, 27, 31);">至此我们描述了deepseek V3 MTP的完整流程！！</font>

:::color5
**<font style="color:#601BDE;">3.MTP模型结构（解析版）  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744448393815-a2e69b39-b7dd-446a-abf0-ed877a3b4b52.jpeg)

:::color5
**<font style="color:#601BDE;">4.MTP模型推理  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">DeepSeek V3中强调，MTP的设计主要是为了训练过程能加速收敛，更充分的使用训练样本。所以针对推理阶段只是简单介绍了一段。这里也稍微展开讲下推理的过程。</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744448752409-5484a987-13b6-49fb-ae8c-f611fdfb36d3.jpeg)

<font style="color:rgb(25, 27, 31);">DeepSeek V3推理可以有两种方法：</font>

**<font style="color:rgb(25, 27, 31);">方法1</font>**<font style="color:rgb(25, 27, 31);">：直接把MTP Model头全部删掉，模型变成了一个Predict Next Token的 Main Model。然后部署模型做推理，这个就跟正常LLM模型推理一样。没有什么加速效果</font>

**<font style="color:rgb(25, 27, 31);">方法2：</font>**<font style="color:rgb(25, 27, 31);">保留MTP Model 做self-speculative decoding，这样充分使用多Head预测能力，提升推理加速性能。类似2.1中介绍的三阶段</font>

+ **<font style="color:rgb(25, 27, 31);">阶段1：predict （预测），</font>**<font style="color:rgb(25, 27, 31);">利用</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个Head一次生成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token，每个Head生成一个token</font>
+ **<font style="color:rgb(25, 27, 31);">阶段2：verify（验证），</font>**<font style="color:rgb(25, 27, 31);">将原始的序列和生成的token拼接，组成多个</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，将组装的多</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">组成一个Batch，一次发给</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">Main Model</font>**<font style="color:rgb(25, 27, 31);">做校验</font>
+ **<font style="color:rgb(25, 27, 31);">阶段3：accept（接受）</font>**<font style="color:rgb(25, 27, 31);">： 选择 </font><font style="color:rgb(25, 27, 31);">Head1</font><font style="color:rgb(25, 27, 31);"> 预估token与 </font><font style="color:rgb(25, 27, 31);">label</font><font style="color:rgb(25, 27, 31);"> 一致的最长 </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 作为可接受的结果。</font>

### <font style="color:rgb(25, 27, 31);">Blockwise Parallel Decoding</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**背景**：Google的工作，这是Google在18年发表在NIPS上的工作（18年是[Transformer](https://zhida.zhihu.com/search?content_id=252633092&content_type=Article&match_order=1&q=Transformer&zhida_source=entity)诞生的元年）。18年Transformer才刚出来，那时候模型只有BERT和GPT-1，模型的参数量也都只有0.1B左右，所以可以说MTP的研究并不是大模型时代的新物种，而是在第一代Transformer base的模型上，就有相应的研究了。

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">这是一篇重点研究推理阶段加速的方法，从论文标题『块并行解码』可以看出隐含在推理阶段不是token-by-token 生成的方式。</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**paper：**[**Blockwise Parallel Decoding for Deep Autoregressive Models**](https://proceedings.neurips.cc/paper_files/paper/2018/file/c4127b9194fe8562c64dc0f5bf2c93bc-Paper.pdf)

:::

<font style="color:rgb(25, 27, 31);">Blockwise Parallel Decoding网络是个并行计算的过程，但遗漏了很多文中表述的细节，也不像是在描述一个Transformer base的网络（这也可以理解，18年，还是SVM、LSTM统治的时代，确实不像现在，Transformer那时候不是个共识性的产物）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744446333121-dd283b71-642f-45a4-9b0a-5d5c580873be.png)

:::color5
**<font style="color:#601BDE;">1.模型结构  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744446733870-7343b69f-5061-47b8-b92f-be7e4713c300.jpeg)

+ <font style="color:rgb(25, 27, 31);">主干网络是训练好的多层decode-only的Transformer网络，经过多层前向计算后，最终隐层输出</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">维度的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">o</font><font style="color:rgb(25, 27, 31);">g</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">。</font>
+ <font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">o</font><font style="color:rgb(25, 27, 31);">g</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">上面接了多个输出Head，每个Head负责预估一个token，</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">负责预估 next token，</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">负责预估 next next token ， 以此类推</font>
+ <font style="color:rgb(25, 27, 31);">每个Head 有三层：</font>
    - <font style="color:rgb(25, 27, 31);">首先是</font>**<font style="color:rgb(25, 27, 31);">一个共享的FFN层，将logit做宽映射(</font>**<font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);">→</font><font style="color:rgb(25, 27, 31);">4</font><font style="color:rgb(25, 27, 31);">h</font>**<font style="color:rgb(25, 27, 31);">)；</font>**
    - <font style="color:rgb(25, 27, 31);">然后再过一个</font>**<font style="color:rgb(25, 27, 31);">FFN层</font>**<font style="color:rgb(25, 27, 31);">，将logit维度还原(</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">4</font><font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);">→</font><font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">)，注意，这层FFN每个Head是特化的、非共享的。该层计算的结果再与原始模型的logit做残差连接；</font>
    - <font style="color:rgb(25, 27, 31);">最后再将结果送入到词表投影层（vocabulary projection 包括一个线性变换和一个Softmax），预估每个词的概率分布，最终通过某种采样方法（如：greedy，beam search等）生成token。注意，这个词表投影层是原预训练网络（original model）的投影矩阵+Softmax，多Head是共享的。</font>
+ <font style="color:rgb(25, 27, 31);">主干网络+</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是original model，也就是pretrain的模型。其他Head是论文说的辅助网络（auxiliary model）</font>

<font style="color:rgb(25, 27, 31);">从上图，我们可以看到，输入一个 </font><font style="color:rgb(25, 27, 31);">t1</font><font style="color:rgb(25, 27, 31);"> 并行的多个头一次输出 </font><font style="color:rgb(25, 27, 31);">t2′,t3′,...tk′</font>

:::color5
**<font style="color:#601BDE;">2.推理阶段  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744446304961-1f16fd0a-2d76-4b08-97b1-17cdc763b948.png)

+ **<font style="color:rgb(25, 27, 31);">阶段1：predict （预测）</font>**<font style="color:rgb(25, 27, 31);">，利用</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个Head一次生成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token，每个Head生成一个token</font>
+ **<font style="color:rgb(25, 27, 31);">阶段2：verify（验证），</font>**<font style="color:rgb(25, 27, 31);">将原始的序列和生成的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token拼接，组成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，如上图Verify阶段，黑框里是</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，箭头指向的是要验证的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">。将组装的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个</font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">组成一个Batch，一次发给</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">做校验（Check</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">生成的token是否跟</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">一致）</font>
+ **<font style="color:rgb(25, 27, 31);">阶段3：accept（接受）</font>**<font style="color:rgb(25, 27, 31);">： 选择 </font><font style="color:rgb(25, 27, 31);">Head1</font><font style="color:rgb(25, 27, 31);"> 预估结果与 </font><font style="color:rgb(25, 27, 31);">label</font><font style="color:rgb(25, 27, 31);"> 一致的最长的 </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 个token，作为可接受的结果。</font>

**<font style="color:rgb(25, 27, 31);">推理阶段加速效果：</font>**

> 假设：我们要生成的序列长度为： m ，并行Head数为： k 。  
我们只考虑最优情况下：所有辅助Head预测结果跟Head1完全一样，即Verify阶段全部token都一次性被接受
>

+ **<font style="color:rgb(25, 27, 31);">原生成方法</font>**<font style="color:rgb(25, 27, 31);">：token-by-token生成，需要</font><font style="color:rgb(25, 27, 31);">m</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">步执行</font>
+ **<font style="color:rgb(25, 27, 31);">本文的方法：</font>**<font style="color:rgb(25, 27, 31);">每</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token执行一次上述三阶段过程，predict阶段执行1步产出多个Head的输出， verify阶段并行执行1步，accept阶段不耗时。所以最终需要</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);">m</font><font style="color:rgb(25, 27, 31);">/</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">步执行</font>
+ <font style="color:rgb(25, 27, 31);">推理加速效果： </font><font style="color:rgb(25, 27, 31);">m→2m/k</font><font style="color:rgb(25, 27, 31);"> ，当 </font><font style="color:rgb(25, 27, 31);">k=4</font><font style="color:rgb(25, 27, 31);"> 的时候，推理可提速1倍</font>

:::color5
**<font style="color:#601BDE;">4.进一步优化推理  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">作者也提出，可以进一步重叠第 </font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);"> 步的verify阶段和第 </font><font style="color:rgb(25, 27, 31);">n+1</font><font style="color:rgb(25, 27, 31);"> 步的predict阶段，能进一步提高推理性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744446603841-8912f241-5dc2-459b-847d-ff64879458be.png)

<font style="color:rgb(25, 27, 31);">我们看看重叠</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);"> 步的verify阶段和第 </font><font style="color:rgb(25, 27, 31);">n+1</font><font style="color:rgb(25, 27, 31);"> 步的predict阶段的过程：</font>

+ **<font style="color:rgb(25, 27, 31);">阶段1：predict （预测），第一次执行推理，</font>**<font style="color:rgb(25, 27, 31);">利用</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个Head一次生成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token，每个Head生成一个token</font>
+ **<font style="color:rgb(25, 27, 31);">阶段2：verify（验证），</font>**<font style="color:rgb(25, 27, 31);">将原始的序列和生成的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token拼接，组成</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，如上图Verify阶段，</font>**<font style="color:rgb(25, 27, 31);">第一个箭头</font>**<font style="color:rgb(25, 27, 31);">指向的是要预估的label，将组装的多个</font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);"><</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">q</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">c</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">_</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);">p</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">></font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">组成一个Batch，</font>**<font style="color:rgb(25, 27, 31);">一次发给</font>****<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">k</font>**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">个Head</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">生成next token，同时承担verify角色跟</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">做校验。</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);">∼</font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">预估Batch中每个序列的后续的token。</font>
+ **<font style="color:rgb(25, 27, 31);">阶段3：accept（接受）</font>**<font style="color:rgb(25, 27, 31);">： 选择</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">H</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">预估结果与</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">a</font><font style="color:rgb(25, 27, 31);">b</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">一致的最长</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个token作为可接受的结果。然后从Batch内取出该条Sequence（包括已经接受的序列和</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个Head生成的token）作为下一个阶段送给verify的输入，如图(</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">u</font><font style="color:rgb(25, 27, 31);">s</font><font style="color:rgb(25, 27, 31);">e</font><font style="color:rgb(25, 27, 31);">d</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">箭头的操作)</font>
+ <font style="color:rgb(25, 27, 31);">循环上述过程，直到生成eos终止标记。</font>

**<font style="color:rgb(25, 27, 31);">推理阶段加速效果：</font>**

<font style="color:rgb(25, 27, 31);">模型第一次推理只执行predict阶段（</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">步），然后进入verify和predict重叠的阶段，每次处理序列往前走</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">长度，直到生成终止标记(共</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">m</font><font style="color:rgb(25, 27, 31);">/</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">步)。所以总推理步数：</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">+</font><font style="color:rgb(25, 27, 31);">m</font><font style="color:rgb(25, 27, 31);">/</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">。推理加速效果：</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">m</font><font style="color:rgb(25, 27, 31);">→</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">+</font><font style="color:rgb(25, 27, 31);">m</font><font style="color:rgb(25, 27, 31);">/</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，当</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">4</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的时候，可加速3倍。</font>

<font style="color:rgb(25, 27, 31);">至此，我们完整描述了Blockwise Parallel Decoding 的核心内容，该</font>**<font style="color:rgb(25, 27, 31);">方法主要是为了做推理阶段的并行加速而设计的</font>**<font style="color:rgb(25, 27, 31);">。虽然命名上没有遵循MPT类，但后面一些演进的方法比如Speculative Sample和下面要介绍的Meta's MTP等，都有该方法设计的影子。</font>

### **<font style="color:rgb(25, 27, 31);">Meta's MTP</font>****<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**背景**：<font style="color:rgb(25, 27, 31);">传统方法的问题（预测下一个token）：</font>

+ <font style="color:rgb(25, 27, 31);">训练阶段：token-by-token生成，是一种感知局部的训练方法，难以学习长距离的依赖关系。</font>
+ <font style="color:rgb(25, 27, 31);">推理阶段：逐个token生成，推理速度较慢</font>**<font style="color:#601BDE;">  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">meta 于2024年4月发表的一篇工作。</font>

+ <font style="color:rgb(25, 27, 31);">训练阶段：通过预测多步token，迫使</font>**<font style="color:#ED740C;">模型学到更长的token依赖关系，从而更好理解上下文，避免陷入局部决策的学习模式</font>**<font style="color:rgb(25, 27, 31);">。同时一次预测多个token，可大大</font>**<font style="color:#ED740C;">提高样本的利用效率</font>**<font style="color:rgb(25, 27, 31);">，相当于一次预估可生成多个<predict, label>样本，来更新模型，有助于模型加速收敛。</font>
+ <font style="color:rgb(25, 27, 31);">推理阶段：并行预估多个token，可提升推理速度</font>

**paper：**[Better & Faster Large Language Models via Multi-token Prediction](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2404.19737)

**参考：**[**https://zhuanlan.zhihu.com/p/18056041194**](https://zhuanlan.zhihu.com/p/18056041194)

:::

<font style="color:rgb(25, 27, 31);">首先看下模型架构，如图5所示。一个共享的transformer的主网络，上面接入4个并行预估头，针对输入token </font><font style="color:rgb(25, 27, 31);">ti</font><font style="color:rgb(25, 27, 31);"> 分别预估后续的 </font><font style="color:rgb(25, 27, 31);">ti+1,ti+2,ti+3,ti+4</font><font style="color:rgb(25, 27, 31);"> 。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447136606-cd92c633-6c7c-4d0b-b1e1-f4de34eaef55.png)

:::color5
**<font style="color:#601BDE;">1.模型结构  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744447191274-9b3bdedf-5bf7-4b91-89dd-3bdbccb0a093.jpeg)

+ <font style="color:rgb(25, 27, 31);">主干网络就是训练好的decoder-only的多层Transformer的网络， </font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> 个输入token </font><font style="color:rgb(25, 27, 31);">x</font><sub><font style="color:rgb(25, 27, 31);">t:1</font></sub><font style="color:rgb(25, 27, 31);">=xt,...,x1</font><font style="color:rgb(25, 27, 31);"> 经过主干网络计算，最终输出隐层表示： </font><font style="color:rgb(25, 27, 31);">z</font><sub><font style="color:rgb(25, 27, 31);">t:1</font></sub><font style="color:rgb(25, 27, 31);"> (来自于 </font><font style="color:rgb(25, 27, 31);">x</font><sub><font style="color:rgb(25, 27, 31);">t:1</font></sub><font style="color:rgb(25, 27, 31);"> 编码结果)。</font>
+ <font style="color:rgb(25, 27, 31);">z</font><sub><font style="color:rgb(25, 27, 31);">t:1</font></sub><font style="color:rgb(25, 27, 31);"> 上面接了多输出Head，每个Head负责预估一个token， </font><font style="color:rgb(25, 27, 31);">Head1</font><font style="color:rgb(25, 27, 31);"> 负责预估 next token， </font><font style="color:rgb(25, 27, 31);">Head2</font><font style="color:rgb(25, 27, 31);"> 负责预估 next next token ， 以此类推</font>
+ <font style="color:rgb(25, 27, 31);">Head 是一个Transformer层（包括 MHA + 2层FFN），且每个Head的Transformer层是独立的，非共享的，经过这层处理后的结果记作：</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">f</font><font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">z</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">:</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">)</font>
+ <font style="color:rgb(25, 27, 31);">最后再将 </font><font style="color:rgb(25, 27, 31);">fhi(z</font><sub><font style="color:rgb(25, 27, 31);">t:i</font></sub><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> 送入到词表投影层( </font><font style="color:rgb(25, 27, 31);">fu</font><font style="color:rgb(25, 27, 31);"> 包括1个投影矩阵+1个Softmax)，预估每个词的概率分布。最终通过某种采样方法（如：greedy，beam search等）生成token。注意，这个词表投影层是原预训练网络（original model）的投影矩阵+Softmax，多Head是共享的。</font>

:::color5
**<font style="color:#601BDE;">2.多头时n-token预测的forward/backward  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744447385575-d8f26f61-ddbf-453e-afb5-6c21d2e56db1.png)

<font style="color:rgb(51, 51, 51);">两头时n-token预测模型中的forward/backward顺序。通过按顺序对头部执行向前/向后操作，我们避免了同时在内存中实现所有未嵌入的层梯度，并减少了GPU内存的峰值使用</font>

# <font style="color:#1f2329;">SGLang</font>
<font style="color:rgba(0, 0, 0, 0.9);">SGLang是当前SOTA的开源LLM推理框架，在DeepSeek系列模型上有着最优的推理性能，被业界广泛使用。</font>

