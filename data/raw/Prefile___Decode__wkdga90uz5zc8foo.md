# Prefile & Decode

<!-- source: yuque://zhongxian-iiot9/hlyypb/wkdga90uz5zc8foo -->

# Prefile & Decode
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在自回归生成模型（如 GPT、LLaMA）中，</font>**<font style="color:rgb(51, 51, 51);">Prefill</font>**<font style="color:rgb(51, 51, 51);"> 和 </font>**<font style="color:rgb(51, 51, 51);">Decode</font>**<font style="color:rgb(51, 51, 51);"> 是推理阶段的两个核心步骤，二者协同完成高效序列生成。以下从原理、实现到优化进行系统解析。</font>

+ **Propose Model**：投机采样过程中的小模型，用于**<font style="color:#ED740C;">生成草稿token</font>**。
+ **<font style="color:rgb(51, 51, 51);">Score Model</font>**<font style="color:rgb(51, 51, 51);">：投机采样过程中的大模型，</font>**<font style="color:#ED740C;">用于对草稿token进行打分，从而决定接收多少个token</font>**<font style="color:rgb(51, 51, 51);">。Score Model为原始生成Token的LLM模型。</font>
+ **<font style="color:rgb(51, 51, 51);">Prefill</font>**<font style="color:rgb(51, 51, 51);">：预填充阶段，把所有的prompt喂给模型做forward计算，输出首个token。投机采样的Score过程使用了类似的过程。</font>
+ **<font style="color:rgb(51, 51, 51);">Decode</font>**<font style="color:rgb(51, 51, 51);">：解码阶段，</font><font style="color:rgb(37, 41, 51);">以自回归的方式逐个生成新的token</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. Prefill（预填充阶段）</font>**

+ **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：处理输入提示（Prompt）并预计算键值（Key-Value, KV）缓存。</font>
+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对完整输入序列 X=[x1,x2,...,xn]</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">进行前向传播，计算所有层的 Key 和 Value。</font>
    - <font style="color:rgb(51, 51, 51);">将 KV 缓存至内存，供后续 Decode 阶段复用，避免重复计算。</font>
    - **<font style="color:rgb(51, 51, 51);">数学表示</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740403448945-3b92354e-567d-476a-a0e4-0b67ad98b0e7.png)

**<font style="color:rgb(51, 51, 51);">2. Decode（解码生成阶段）</font>**

+ **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：基于 KV 缓存逐步生成输出序列 Y=[y1,y2,...,ym]。</font>
+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">每次生成新 token y</font><sub><font style="color:rgb(51, 51, 51);">t</font></sub><font style="color:rgb(51, 51, 51);">时，仅计算当前 token 的 Query (Qt)，复用缓存的 K</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);">和 V</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:rgb(51, 51, 51);">数学表示</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740403471846-0fcc1e98-81a8-4fac-894f-0c9c9b2f4b64.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

| **<font style="color:#000000;">阶段</font>** | **<font style="color:#000000;">输入</font>** | **<font style="color:#000000;">操作</font>** | **<font style="color:#000000;">复杂度</font>** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">Prefill</font>** | <font style="color:rgb(51, 51, 51);">完整 Prompt X</font>_<font style="color:rgb(51, 51, 51);"></font>_ | <font style="color:rgb(51, 51, 51);">计算所有 token 的 KV，生成首个输出 token</font> | <font style="color:rgb(51, 51, 51);">O(n2⋅d)</font>_<font style="color:rgb(51, 51, 51);"></font>_ |
| **<font style="color:rgb(51, 51, 51);">Decode</font>** | <font style="color:rgb(51, 51, 51);">单 Token y</font><sub><font style="color:rgb(51, 51, 51);">t−1</font></sub> | <font style="color:rgb(51, 51, 51);">计算当前 token 的 Q，复用 KV 缓存生成 yt</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">，更新缓存</font> | <font style="color:rgb(51, 51, 51);">O(t⋅d)</font>_<font style="color:rgb(51, 51, 51);"></font>_ |


## <font style="color:rgb(51, 51, 51);">Prefill 详细步骤</font>
1. <font style="color:rgb(51, 51, 51);">输入完整 Prompt，通过嵌入层和位置编码生成输入向量。</font>
2. <font style="color:rgb(51, 51, 51);">逐层计算自注意力中的 Key 和 Value，并缓存。</font>
3. <font style="color:rgb(51, 51, 51);">通过输出层生成首个 token y1</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>

## <font style="color:rgb(51, 51, 51);">Decode 详细步骤</font>
1. <font style="color:rgb(51, 51, 51);">输入上一步生成的 token y</font><sub><font style="color:rgb(51, 51, 51);">t−1</font></sub><font style="color:rgb(51, 51, 51);">（初始为 y1）。</font>
2. <font style="color:rgb(51, 51, 51);">计算当前 token 的 Query (Qt)，结合缓存的 K</font><sub><font style="color:rgb(51, 51, 51);">cache </font></sub><font style="color:rgb(51, 51, 51);">和 V</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);"> 计算注意力。</font>
3. <font style="color:rgb(51, 51, 51);">通过 FFN 层生成 logits，采样得到 yt</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>
4. <font style="color:rgb(51, 51, 51);">将 yt</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">对应的 Key 和 Value 追加到缓存中。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **<font style="color:#000000;">阶段</font>** | **<font style="color:#000000;">优点</font>** | **<font style="color:#000000;">缺点</font>** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">Prefill</font>** | <font style="color:rgb(51, 51, 51);">一次性计算全量 KV，减少后续重复计算</font> | <font style="color:rgb(51, 51, 51);">初始延迟高，内存占用大（存储所有 KV）</font> |
| **<font style="color:rgb(51, 51, 51);">Decode</font>** | <font style="color:rgb(51, 51, 51);">单步计算量小，实时性高</font> | <font style="color:rgb(51, 51, 51);">依赖 KV 缓存，长序列生成时内存压力持续增加</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">Prefill 适用场景</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">长文本输入处理（如文档摘要、代码生成）。</font>
    - <font style="color:rgb(51, 51, 51);">需要多次交互的对话系统（首次响应需处理用户完整输入）。</font>
2. **<font style="color:rgb(51, 51, 51);">Decode 适用场景</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">流式生成（如逐词翻译、实时聊天）。</font>
    - <font style="color:rgb(51, 51, 51);">低延迟要求的任务（如语音助手响应）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

## <font style="color:rgb(51, 51, 51);">Prefill 优化</font>
+ **<font style="color:rgb(51, 51, 51);">计算优化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Flash Attention</font>**<font style="color:rgb(51, 51, 51);">：通过核融合减少显存访问，加速注意力计算。</font>
    - **<font style="color:rgb(51, 51, 51);">稀疏注意力</font>**<font style="color:rgb(51, 51, 51);">：仅计算关键位置的 KV（如 Longformer 的局部+全局注意力）。</font>
+ **<font style="color:rgb(51, 51, 51);">内存优化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">分块缓存</font>**<font style="color:rgb(51, 51, 51);">：将 KV 分块存储，结合内存池技术减少碎片。</font>
    - **<font style="color:rgb(51, 51, 51);">动态卸载</font>**<font style="color:rgb(51, 51, 51);">：将不活跃的 KV 卸载到 CPU 或磁盘（如 FlexGen）。</font>

## <font style="color:rgb(51, 51, 51);">Decode 优化</font>
+ **<font style="color:rgb(51, 51, 51);">增量计算</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">滑动窗口</font>**<font style="color:rgb(51, 51, 51);">：仅保留最近</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">k</font>_<font style="color:rgb(51, 51, 51);">k</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">个 token 的 KV（如 Mistral 的 Sliding Window Attention）。</font>
    - **<font style="color:rgb(51, 51, 51);">选择性更新</font>**<font style="color:rgb(51, 51, 51);">：通过门控机制决定是否更新缓存（如 Gated Attention）。</font>
+ **<font style="color:rgb(51, 51, 51);">并行化</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">批处理推测解码</font>**<font style="color:rgb(51, 51, 51);">：同时生成多个候选序列（如 Medusa、Speculative Decoding）。</font>
    - **<font style="color:rgb(51, 51, 51);">硬件加速</font>**<font style="color:rgb(51, 51, 51);">：利用 CUDA Graph 或 TensorRT 优化单步计算。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
prompt = "The capital of France is"

# Prefill：处理完整 Prompt，缓存 KV
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model(**inputs, use_cache=True)
past_key_values = outputs.past_key_values
next_token = torch.argmax(outputs.logits[:, -1, :], dim=-1)

# Decode：逐步生成后续 Token
generated = inputs.input_ids
for _ in range(100):
    # 输入最新 Token 和缓存
    outputs = model(next_token.unsqueeze(0), past_key_values=past_key_values, use_cache=True)
    past_key_values = outputs.past_key_values
    next_token = torch.argmax(outputs.logits[:, -1, :], dim=-1)
    generated = torch.cat([generated, next_token.unsqueeze(0)], dim=-1)

# 解码最终结果
print(tokenizer.decode(generated[0], skip_special_tokens=True))

```

# Prefill
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Prefill 的核心在于</font>**<font style="color:#ED740C;">预先计算并缓存输入序列的键值对（Key-Value, KV）</font>**<font style="color:rgb(51, 51, 51);">，从而减少生成阶段的计算量。在标准的 Transformer 解码器中，自注意力机制为每个 token 生成对应的 Key 和 Value。生成后续 token 时，若每次重新计算整个序列的注意力，复杂度为 O(n2)。通过预填充 KV 缓存，生成阶段只需计算新 token 的注意力，复杂度降低为 O(n)</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>

:::

**数学原理：**

<font style="color:rgb(51, 51, 51);">自注意力计算中，输入序列 X∈R</font><sup><font style="color:rgb(51, 51, 51);">n×d</font></sup><font style="color:rgb(51, 51, 51);">通过线性变换得到 Query (</font>_<font style="color:rgb(51, 51, 51);">Q</font>_<font style="color:rgb(51, 51, 51);">)、Key (</font>_<font style="color:rgb(51, 51, 51);">K</font>_<font style="color:rgb(51, 51, 51);">)、Value (</font>_<font style="color:rgb(51, 51, 51);">V</font>_<font style="color:rgb(51, 51, 51);">)，注意力得分为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740402724422-aefc9371-6c6b-4a70-bd08-ef5d5291525f.png)

<font style="color:rgb(51, 51, 51);">Prefill 阶段预先计算并存储 Kprefill 和 Vprefill，</font>**<font style="color:#74B602;">生成阶段每次仅需追加新 token 的 kt,vt 到缓存中</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **Prefill 阶段**：
    - <font style="color:rgb(51, 51, 51);">输入完整提示（Prompt）序列 X=[x1,x2,...,xn]</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">前向传播计算所有层的 Key 和 Value，并缓存为 K</font><sub><font style="color:rgb(51, 51, 51);">cache,</font></sub><font style="color:rgb(51, 51, 51);">V</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">同时生成首个输出 token y1</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>
2. **生成阶段**：
    - <font style="color:rgb(51, 51, 51);">对于每个新生成的 token yt</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">将 yt</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">嵌入并计算当前步的 Qt,kt,vt。</font>
        * <font style="color:rgb(51, 51, 51);">从缓存中读取 K</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);">,V</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);">，拼接 kt,vt 更新缓存。</font>
        * <font style="color:rgb(51, 51, 51);">计算注意力：仅用 Qt与缓存的 K</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);">、V</font><sub><font style="color:rgb(51, 51, 51);">cache</font></sub><font style="color:rgb(51, 51, 51);"> 交互。</font>
        * <font style="color:rgb(51, 51, 51);">输出下一个 token y</font><sub><font style="color:rgb(51, 51, 51);">t+1</font></sub><font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **<font style="color:#000000;">优点</font>** | **<font style="color:#000000;">缺点</font>** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">减少重复计算，提升生成速度</font> | <font style="color:rgb(51, 51, 51);">KV 缓存占用内存，长序列可能导致 OOM</font> |
| <font style="color:rgb(51, 51, 51);">显著降低计算复杂度（</font><font style="color:rgb(51, 51, 51);">O</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">→</font><font style="color:rgb(51, 51, 51);">O</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">O</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">→</font>_<font style="color:rgb(51, 51, 51);">O</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">）</font> | <font style="color:rgb(51, 51, 51);">Prefill 阶段仍需完整计算提示的注意力</font> |
| <font style="color:rgb(51, 51, 51);">适用于流式生成或实时交互场景</font> | <font style="color:rgb(51, 51, 51);">动态提示需重新 Prefill，增加额外开销</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">长文本生成</font>**<font style="color:rgb(51, 51, 51);">：如故事续写、文档摘要。</font>
2. **<font style="color:rgb(51, 51, 51);">对话系统</font>**<font style="color:rgb(51, 51, 51);">：处理用户的长篇输入后生成响应。</font>
3. **<font style="color:rgb(51, 51, 51);">代码补全</font>**<font style="color:rgb(51, 51, 51);">：根据现有代码上下文预测后续片段。</font>
4. **<font style="color:rgb(51, 51, 51);">低延迟场景</font>**<font style="color:rgb(51, 51, 51);">：实时翻译、语音助手等需快速反馈的任务。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **内存优化**：
    - **<font style="color:rgb(51, 51, 51);">分块缓存</font>**<font style="color:rgb(51, 51, 51);">：将 KV 缓存分块存储，结合内存池技术减少碎片。</font>
    - **<font style="color:rgb(51, 51, 51);">量化压缩</font>**<font style="color:rgb(51, 51, 51);">：对缓存使用低精度（如 FP16、INT8）存储。</font>
2. **计算优化**：
    - **<font style="color:rgb(51, 51, 51);">增量更新</font>**<font style="color:rgb(51, 51, 51);">：仅计算新增 token 的影响区域（如 Sliding Window Attention）。</font>
    - **<font style="color:rgb(51, 51, 51);">并行化</font>**<font style="color:rgb(51, 51, 51);">：重叠 Prefill 与生成阶段的计算（如 Pipeline 并行）。</font>
3. **动态策略**：
    - **<font style="color:rgb(51, 51, 51);">选择性缓存</font>**<font style="color:rgb(51, 51, 51);">：根据重要性评分丢弃部分缓存的 KV。</font>
    - **<font style="color:rgb(51, 51, 51);">自适应长度</font>**<font style="color:rgb(51, 51, 51);">：根据硬件资源动态调整缓存容量。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# 输入提示
prompt = "The answer to life, the universe, and everything is"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

# Prefill 阶段：计算并缓存 KV
with torch.no_grad():
    outputs = model(input_ids, use_cache=True)
past_key_values = outputs.past_key_values
generated = input_ids

# 生成阶段：逐步生成后续 Token
for _ in range(50):  # 生成50个token
    next_token_logits = outputs.logits[:, -1, :]
    next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
    generated = torch.cat([generated, next_token], dim=-1)
    
    # 仅输入新Token，利用缓存
    outputs = model(next_token, past_key_values=past_key_values, use_cache=True)
    past_key_values = outputs.past_key_values

# 解码输出
print(tokenizer.decode(generated[0], skip_special_tokens=True))

```





# Decode
## 选择decoding策略的依据
+ **任务需求**
    - <font style="color:rgb(51, 51, 51);">如果任务对生成速度要求高，且内容连贯性更重要，可以选择贪心解码。</font>
    - <font style="color:rgb(51, 51, 51);">如果需要生成高质量、多样化的内容，可以结合束搜索和温式重组，寻找生成质量和多样性的平衡。</font>
    - <font style="color:rgb(51, 51, 51);">对于需要强制多样化输出的任务，如多回答生成，可以选择多样性解码或覆盖机制。</font>
+ **模型与数据**
    - <font style="color:rgb(51, 51, 51);">大模型通常具有较高的计算能力，可以支持更为复杂的解码策略，如束搜索和多样性解码。</font>
    - <font style="color:rgb(51, 51, 51);">对于较小的模型或资源受限的场景，贪心解码是更合适的选择。</font>
+ **生成场景**
    - <font style="color:rgb(51, 51, 51);">在实时应用中，贪心解码因其高效性而被广泛采用。</font>
    - <font style="color:rgb(51, 51, 51);">对于离线处理的任务，可以采用更为复杂和耗时的解码策略，如多样性解码和覆盖机制。</font>

## <font style="color:rgb(51, 51, 51);">各解码策略的对比</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739867226054-e3490263-24b0-4f20-b6e4-05068f1821bd.png)

| **方法** | **多样性** | **连贯性** | **速度** | **适用场景** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">贪心搜索</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">快</font> | <font style="color:rgb(51, 51, 51);">需要确定性的任务</font> |
| <font style="color:rgb(51, 51, 51);">集束搜索</font> | <font style="color:rgb(51, 51, 51);">中低</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">翻译、摘要</font> |
| <font style="color:rgb(51, 51, 51);">温度采样+Top-P</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">中高</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">开放域生成（故事、对话）</font> |
| <font style="color:rgb(51, 51, 51);">对比搜索</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">较慢</font> | <font style="color:rgb(51, 51, 51);">高质量多样化生成</font> |


## <font style="color:rgb(51, 51, 51);">Self-Consistency</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Self-Consistency 是一种提升大语言模型（LLM）推理能力的解码策略，其核心思想是：</font>**<font style="color:rgb(51, 51, 51);">通过多次采样生成不同的推理路径，选择最具一致性的答案作为最终输出</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

**<font style="color:rgb(51, 51, 51);">关键公式</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740553910213-7677e66e-3220-4a4e-bdb1-605dd0babf02.png)

<font style="color:rgb(51, 51, 51);">其中：</font>

+ <font style="color:rgb(51, 51, 51);">Px是输入 x 对应的推理路径集合</font>
+ <font style="color:rgb(51, 51, 51);">ans(p) 表示路径 p</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 对应的答案</font>
+ <font style="color:rgb(51, 51, 51);">w(p) 为路径权重（通常取均匀权重）</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **多路径生成**：

```python
def generate_paths(prompt, num_samples=10):
    paths = []
    for _ in range(num_samples):
        path = model.generate(
            prompt,
            temperature=0.7,  # 增加多样性
            max_new_tokens=200
        )
        paths.append(extract_answer(path))
    return paths
```

2. **答案归一化**：
    - <font style="color:rgb(51, 51, 51);">数学问题：标准化数字格式（如 "12.0" → 12）</font>
    - <font style="color:rgb(51, 51, 51);">代码生成：AST抽象语法树比对</font>
    - <font style="color:rgb(51, 51, 51);">文本答案：语义相似度计算（如 BERTScore）</font>
3. **投票机制**：

```python
from collections import defaultdict

def majority_vote(answers):
    counter = defaultdict(int)
    for ans in answers:
        norm_ans = normalize(ans)
        counter[norm_ans] += 1
    return max(counter.items(), key=lambda x: x[1])[0]
```

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">提升复杂任务准确率（GSM8K +5.2%）</font>
+ <font style="color:rgb(51, 51, 51);">缓解模型幻觉问题</font>
+ <font style="color:rgb(51, 51, 51);">降低单次生成随机性影响</font>

**<font style="color:rgb(51, 51, 51);">局限</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算成本增加（生成次数 × 单次推理时间）</font>
+ <font style="color:rgb(51, 51, 51);">多数答案可能集体错误</font>
+ <font style="color:rgb(51, 51, 51);">答案归一化存在挑战</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

| **场景** | **案例** | **效果提升** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">数学推理</font> | <font style="color:rgb(51, 51, 51);">GSM8K、MATH 数据集</font> | <font style="color:rgb(51, 51, 51);">+3%~12%</font> |
| <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">HumanEval、MBPP 基准</font> | <font style="color:rgb(51, 51, 51);">+7%~15%</font> |
| <font style="color:rgb(51, 51, 51);">常识推理</font> | <font style="color:rgb(51, 51, 51);">StrategyQA、ARC-Challenge</font> | <font style="color:rgb(51, 51, 51);">+5%~8%</font> |
| <font style="color:rgb(51, 51, 51);">科学计算</font> | <font style="color:rgb(51, 51, 51);">SciBench、PhysiNet</font> | <font style="color:rgb(51, 51, 51);">+10%~18%</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **动态路径采样**：

```python
def adaptive_sampling(prompt, min_samples=5, threshold=0.8):
    answers = []
    confidence = 0.0
    while len(answers) < 20 and confidence < threshold:
        path = model.generate(prompt, temperature=0.5)
        ans = extract_answer(path)
        answers.append(ans)
        confidence = max_frequency(answers) / len(answers)
    return answers
```

2. **加权投票机制**：
    - <font style="color:rgb(51, 51, 51);">基于路径困惑度赋予权重：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740553975005-25fe69df-601b-4341-8988-a21f685f2dcf.png)
3. **验证器增强**：

```python
class AnswerVerifier:
    def __init__(self):
        self.verifier_model = load_verifier()

    def check(self, answer):
        return self.verifier_model(answer) > 0.8
```

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from collections import defaultdict

class SelfConsistencyGenerator:
    def __init__(self, model_name="gpt2-large"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
    
    def normalize_answer(self, text):
        # 实现答案标准化逻辑
        return text.strip().lower()
    
    def generate_answers(self, prompt, num_samples=10):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        answers = []
        
        with torch.no_grad():
            for _ in range(num_samples):
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=200,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                answers.append(self.normalize_answer(answer))
        
        return answers
    
    def get_consensus(self, answers):
        counts = defaultdict(int)
        for ans in answers:
            counts[ans] += 1
        return max(counts, key=counts.get)

# 使用示例
generator = SelfConsistencyGenerator()
prompt = "Q: 如果一个箱子里有5个红球和3个蓝球，随机抽取2个，都是红球的概率是多少？"
answers = generator.generate_answers(prompt, num_samples=20)
final_answer = generator.get_consensus(answers)
print(f"Consensus Answer: {final_answer}")

```





## Self-Refine
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Self-Refine 是一种基于自我迭代优化的生成方法，由 Madaan et al. 在 2023 年提出。其核心机制是：</font>**<font style="color:rgb(51, 51, 51);">让模型通过反馈-修正的迭代循环，持续改进自身输出质量</font>**

<font style="color:rgb(51, 51, 51);">参考：</font>[大模型记忆反思](https://blog.csdn.net/javacc2015/article/details/137041904)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740554140754-ae428492-4fd0-4d61-bec9-5e9763ffbe47.png)

<font style="color:rgb(51, 51, 51);">主要包含三个阶段：</font>

1. **<font style="color:rgb(51, 51, 51);">初始生成</font>**<font style="color:rgb(51, 51, 51);">：模型产生初步输出</font>
2. **<font style="color:rgb(51, 51, 51);">自我反馈</font>**<font style="color:rgb(51, 51, 51);">：模型对当前输出的质量问题进行分析</font>
3. **<font style="color:rgb(51, 51, 51);">迭代修正</font>**<font style="color:rgb(51, 51, 51);">：基于反馈生成改进版本</font>

**<font style="color:rgb(51, 51, 51);">数学形式化</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740555396353-605caf59-089c-4ec2-873e-7e95f5e3d075.png)

<font style="color:rgb(51, 51, 51);">其中：</font>

+ <font style="color:rgb(51, 51, 51);">Gθ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为生成模型</font>
+ <font style="color:rgb(51, 51, 51);">F</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为反馈函数</font>
+ <font style="color:rgb(51, 51, 51);">yt表示第 t</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">轮迭代的输出</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

##### **<font style="color:rgb(51, 51, 51);">步骤1：初始生成</font>**
```python
def initial_generation(prompt):
    response = model.generate(prompt, max_length=200)
    return response
```

##### **<font style="color:rgb(51, 51, 51);">步骤2：自我反馈分析</font>**
```python
def generate_feedback(text):
    feedback_prompt = f"""
    请分析以下文本的问题：\n{text}\n主要问题包括：
    1. 逻辑错误：
    2. 事实错误：
    3. 表达改进：
    """
    feedback = model.generate(feedback_prompt)
    return extract_feedback_points(feedback)
```

##### **<font style="color:rgb(51, 51, 51);">步骤3：迭代修正</font>**
```python
def refine_step(text, feedback):
    refine_prompt = f"""
    根据以下反馈改进文本：\n{feedback}\n原文本：\n{text}\n改进后的版本：
    """
    refined = model.generate(refine_prompt)
    return refined
```

##### **<font style="color:rgb(51, 51, 51);">步骤4：收敛判断</font>**
```python
def should_stop(current, previous, max_iters=3):
    return (current == previous) or (iter_count >= max_iters)
```

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">提升复杂任务性能（文本生成 +15% BLEU）</font>
+ <font style="color:rgb(51, 51, 51);">减少人工标注需求</font>
+ <font style="color:rgb(51, 51, 51);">可解释性强（保留修订记录）</font>

**<font style="color:rgb(51, 51, 51);">局限</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算成本随迭代次数线性增长</font>
+ <font style="color:rgb(51, 51, 51);">可能陷入局部最优</font>
+ <font style="color:rgb(51, 51, 51);">依赖模型的自我诊断能力</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

| **领域** | **具体应用** | **改进效果** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">函数级代码缺陷修复</font> | <font style="color:rgb(51, 51, 51);">HumanEval +22% pass@1</font> |
| <font style="color:rgb(51, 51, 51);">数学推理</font> | <font style="color:rgb(51, 51, 51);">分步骤验证推导过程</font> | <font style="color:rgb(51, 51, 51);">GSM8K +18% 准确率</font> |
| <font style="color:rgb(51, 51, 51);">文本创作</font> | <font style="color:rgb(51, 51, 51);">文章连贯性优化</font> | <font style="color:rgb(51, 51, 51);">人工评分 +1.2（5分制）</font> |
| <font style="color:rgb(51, 51, 51);">对话系统</font> | <font style="color:rgb(51, 51, 51);">回复安全性检查</font> | <font style="color:rgb(51, 51, 51);">有害回复减少 63%</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **混合反馈机制**：

```python
def hybrid_feedback(text):
    # 内部反馈
    internal_fb = model.generate(fb_prompt)  
    # 外部验证器
    external_score = verifier(text)  
    return combine_feedback(internal_fb, external_score)
```

2. **强化学习优化**：

```python
class RefinementAgent:
    def __init__(self):
        self.policy_net = DQN()

    def select_action(self, feedback):
        return self.policy_net(feedback)
```

3. **记忆增强改进**：

```python
class MemoryAugmentedRefiner:
    def __init__(self):
        self.memory = VectorDB()

    def refine(self, text):
        similar_patches = self.memory.search(text)
        return integrate_patches(text, similar_patches)
```

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class SelfRefiner:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.max_iters = 3
    
    def generate_feedback(self, text):
        inputs = self.tokenizer(
            f"请分析以下文本的问题：{text}",
            return_tensors="pt"
        )
        outputs = self.model.generate(**inputs, max_length=300)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def refine_text(self, prompt):
        current_text = self.initial_generation(prompt)
        history = [current_text]
        
        for _ in range(self.max_iters):
            feedback = self.generate_feedback(current_text)
            refined = self.refine_step(current_text, feedback)
            
            if self.convergence_check(refined, current_text):
                break
                
            current_text = refined
            history.append(current_text)
            
        return current_text, history
    
    def convergence_check(self, new, old):
        # 计算编辑距离或语义相似度
        return calculate_similarity(new, old) > 0.95

# 使用示例
refiner = SelfRefiner()
input_prompt = "写一篇关于气候变化影响的短文"
final_text, history = refiner.refine_text(input_prompt)

```





## <font style="color:rgb(51, 51, 51);">贪心解码（Greedy Decoding）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：贪心解码是一种简单直接的解码方法。它在每一步生成中，</font>**<font style="color:#ED740C;">选择当前概率最高的下一个词</font>**<font style="color:rgb(51, 51, 51);">，直到生成完整的序列。这种方法基于“局部最优”的原则，逐个字符地构建输出。</font>

:::

**核心思想**：<font style="color:rgb(51, 51, 51);">每一步选择当前概率最高的词，即 </font><font style="color:rgb(51, 51, 51);">w</font><sub><font style="color:rgb(51, 51, 51);">t</font></sub><font style="color:rgb(51, 51, 51);">=arg⁡max⁡</font><sub><font style="color:rgb(51, 51, 51);">w</font></sub><font style="color:rgb(51, 51, 51);">P(w∣w</font><sub><font style="color:rgb(51, 51, 51);">1:t−1</font></sub><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">简单高效</font>**<font style="color:rgb(51, 51, 51);">：实现简单，计算速度快。</font>
+ **<font style="color:rgb(51, 51, 51);">生成流畅</font>**<font style="color:rgb(51, 51, 51);">：通常生成的文本较为连贯和有意义。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">缺乏多样性</font>**<font style="color:rgb(51, 51, 51);">：总是选择概率最高的词，可能导致生成内容缺乏多样性和创新性。</font>
+ **<font style="color:rgb(51, 51, 51);">忽略全局最优</font>**<font style="color:rgb(51, 51, 51);">：可能因为局部最优而导致全局生成效果不理想。</font>
+ **<font style="color:rgb(51, 51, 51);">复读机</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#74B602;">生成“今天天气真好”→可能重复输出“好”。</font>**

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于对生成速度要求较高，且内容连贯性优先于多样性的场景，如实时聊天机器人。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
import torch
import torch.nn.functional as F

def greedy_decode(model, input_ids, max_length, device='cuda'):
    # 初始化输出
    outputs = input_ids
    for i in range(max_length):
        # 前向传播
        outputs = model(outputs, attention_mask=torch.ones(outputs.size(), device=device))
        # 获取预测概率
        logits = outputs.logits[:, -1, :]
        # 选择概率最高的词
        next_token = torch.argmax(logits, dim=-1).unsqueeze(-1)
        # 将下一个词附加到输出序列中
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```



## <font style="color:rgb(51, 51, 51);">束搜索（Beam Search）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">束搜索是一种贪心策略的扩展，通过保留多个候选序列来生成最终的输出。在每一步生成中，系统会保存若干个可能性较高的序列（束），并根据一定的分数筛选和扩展这些候选序列，最终选择得分最高的序列作为输出。</font>

:::

**<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：维护一个大小为 </font><font style="color:rgb(51, 51, 51);">k</font><font style="color:rgb(51, 51, 51);">的候选序列集合（称为“束宽”），每一步扩展所有候选序列，保留概率最高的 </font><font style="color:rgb(51, 51, 51);">k</font><font style="color:rgb(51, 51, 51);">个。</font>

**<font style="color:rgb(51, 51, 51);">束宽 k</font>**<font style="color:rgb(51, 51, 51);">：机器翻译常用 4~8，文本生成可能更低（2~4）。</font>

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">多样性增强</font>**<font style="color:rgb(51, 51, 51);">：通过保留多个候选序列，束搜索能够生成更多样化的输出。</font>
+ **<font style="color:rgb(51, 51, 51);">提升生成质量</font>**<font style="color:rgb(51, 51, 51);">：在保持一定多样性的同时，生成质量通常优于单纯的贪心解码。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">计算开销高</font>**<font style="color:rgb(51, 51, 51);">：保留多个候选序列增加了计算量，尤其是当束宽较大时，计算时间显著增加。</font>
+ **<font style="color:rgb(51, 51, 51);">内存需求大</font>**<font style="color:rgb(51, 51, 51);">：在处理大规模序列时，存储和处理多个候选序列需要更多的内存资源。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">机器翻译、摘要生成等</font>**<font style="color:#ED740C;">需要准确性的任务</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def beam_search_decode(model, input_ids, max_length, beam_width=3, device='cuda'):
    # 初始化输出
    current_sequences = [input_ids]
    scores = [0.0]
    
    for i in range(max_length):
        new_sequences = []
        new_scores = []
        for seq in current_sequences:
            outputs = model(seq, attention_mask=torch.ones(seq.size(), device=device))
            logits = outputs.logits[:, -1, :]
            topk_indices = torch.topk(logits, beam_width).indices
            for idx in topk_indices:
                new_seq = torch.cat([seq, idx.unsqueeze(-1)], dim=-1)
                new_seq_score = scores[current_sequences.index(seq)] + F.log_softmax(logits[idx], dim=-1).item()
                new_sequences.append(new_seq)
                new_scores.append(new_seq_score)
        
        # 根据得分排序并保留前beam_width个
        combined = list(zip(new_sequences, new_scores))
        combined.sort(key=lambda x: -x[1])
        current_sequences = [cs[0] for cs in combined[:beam_width]]
        scores = [cs[1] for cs in combined[:beam_width]]
    
    # 返回得分最高的序列
    best_seq = current_sequences[0]
    return best_seq
```





## <font style="color:rgb(51, 51, 51);">温度采样（Temperature Sampling）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">温式重组通过调整生成过程中的温度参数来平衡探索与确定性。较大的温度值会增加多样性，但可能导致生成内容不连贯；较小的温度值则更倾向于选择概率高的词，生成内容更为保守和流畅。</font>

:::

**核心思想**：<font style="color:rgb(51, 51, 51);">引入温度参数 </font><font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">调整概率分布：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741941973697-df55bde1-19df-4a6b-9427-12c330950b7d.png)

+ <font style="color:rgb(51, 51, 51);">τ→0</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：趋近贪心搜索。</font>
+ <font style="color:rgb(51, 51, 51);">τ→∞</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：趋近均匀分布。</font>

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">增加多样性</font>**<font style="color:rgb(51, 51, 51);">：通过调节温度，可以在生成过程中引入更多变异性，提升创意生成任务的效果。</font>
+ **<font style="color:rgb(51, 51, 51);">灵活性高</font>**<font style="color:rgb(51, 51, 51);">：可以根据具体需求动态调整温度参数，实现生成策略的灵活控制。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">不稳定性</font>**<font style="color:rgb(51, 51, 51);">：高温可能导致生成内容的不连贯性和不可预测性，影响生成质量。</font>
+ **<font style="color:rgb(51, 51, 51);">计算复杂度</font>**<font style="color:rgb(51, 51, 51);">：概率计算和采样的引入增加了生成过程的计算复杂度。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">常与Top-K或Top-P结合使用。适用于需要多样化输出的任务，如创意写作、诗歌生成等。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def temperature_sampling_decode(model, input_ids, max_length, temperature=1.0, device='cuda'):
    outputs = input_ids
    for i in range(max_length):
        outputs = model(outputs, attention_mask=torch.ones(outputs.size(), device=device))
        logits = outputs.logits[:, -1, :] / temperature
        # 采样下一个词
        next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
        next_token = next_token.squeeze(-1).unsqueeze(-1)
        # 更新输出
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```

<font style="color:rgb(51, 51, 51);"></font>

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



## <font style="color:rgb(51, 51, 51);">多样性解码（Diverse Decoding）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">多样性解码是一种通过引入额外的约束或机制，强制生成更多样化输出的策略。常见的实现方法包括使用遮蔽机制（如随机屏蔽部分已生成的内容，强制模型探索不同的生成路径）、或者在生成过程中引入排序损失。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">显著提升多样性</font>**<font style="color:rgb(51, 51, 51);">：通过引入遮蔽机制或多样性损失，能够有效生成更多样化的输出。</font>
+ **<font style="color:rgb(51, 51, 51);">适应复杂任务</font>**<font style="color:rgb(51, 51, 51);">：特别适用于需要多个正确答案的情况，如多语种生成、多义词处理。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">复杂性增加</font>**<font style="color:rgb(51, 51, 51);">：引入额外机制增加了实现和计算的复杂性。</font>
+ **<font style="color:rgb(51, 51, 51);">生成质量不稳定</font>**<font style="color:rgb(51, 51, 51);">：过多地追求多样性可能导致生成内容的质量下降。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于需要生成多样化输出的任务，如多回答生成、多语言翻译等。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def diverse_decoding(model, input_ids, max_length, diversity_weight=0.1):
    outputs = input_ids
    for i in range(max_length):
        outputs = model(outputs, attention_mask=torch.ones(outputs.size()))
        # 获取预测概率
        logits = outputs.logits[:, -1, :]
        # 引入多样性惩罚
        log_prob = F.log_softmax(logits, dim=-1)
        # 随机屏蔽部分词，增加多样性
        masked_logits = (log_prob + torch.randn_like(log_prob) * diversity_weight).log_softmax(dim=-1)
        # 采样下一个词
        next_token = torch.multinomial(masked_logits.exp(), num_samples=1)
        next_token = next_token.squeeze(-1).unsqueeze(-1)
        # 更新输出
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```

## <font style="color:rgb(51, 51, 51);">长度惩罚（Length Penalty）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">长度惩罚是一种用于平衡生成序列长度和质量的策略。在评估生成序列时，对长度进行适当的惩罚或奖励，以鼓励生成更合适的长度。常用在束搜索中，避免模型为了获得高分而不断生成冗长的序列。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">平衡生成长度</font>**<font style="color:rgb(51, 51, 51);">：有效抑制过长或过短的生成序列，提高生成结果的合理性。</font>
+ **<font style="color:rgb(51, 51, 51);">增强评估准确性</font>**<font style="color:rgb(51, 51, 51);">：在模型评估中，长度惩罚可以提供更准确的分数，反映生成序列的实际质量。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">需要调整参数</font>**<font style="color:rgb(51, 51, 51);">：长度惩罚参数的选择需要根据具体任务进行调整，找到合适的平衡点。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于生成序列的长度控制，如机器翻译、文本摘要等任务。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def length_penalty(beam_sequences, sequence_lengths, alpha=0.7):
    # 计算长度惩罚
    penalized_scores = []
    for seq, length in zip(beam_sequences, sequence_lengths):
        penalty = (length ** alpha) / (1 + length)
        penalized_scores.append(seq.score * penalty)
    # 返回 penalized scores
    return penalized_scores
```



## <font style="color:rgb(51, 51, 51);">覆盖机制（Coverage Mechanism）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">覆盖机制是一种用于生成过程中关注多样性的策略，在生成长序列时，确保模型在各时间段都能覆盖足够多的可能词项，避免生成重复或过于单一的内容。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">避免重复内容</font>**<font style="color:rgb(51, 51, 51);">：通过覆盖机制强制模型生成多样化的内容，减少重复。</font>
+ **<font style="color:rgb(51, 51, 51);">提升生成内容的信息量</font>**<font style="color:rgb(51, 51, 51);">：能够更好地捕捉和表达复杂的信息。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">实现复杂性</font>**
    - <font style="color:rgb(51, 51, 51);">引入覆盖机制增加了生成过程的复杂性，需要额外维护和更新覆盖向量。</font>
+ **<font style="color:rgb(51, 51, 51);">需要调整参数</font>**
    - <font style="color:rgb(51, 51, 51);">覆盖机制的参数设置需要经过调试，以达到最佳效果。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于生成较长序列的任务，如文本摘要、对话生成，特别是在需要避免重复内容的情况下。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def coverage_mechanism(model, input_ids, max_length):
    # 初始化覆盖向量
    coverage = torch.zeros(max_length)
    outputs = input_ids
    for i in range(max_length):
        # 前向传播
        outputs = model(outputs, attention_mask=torch.ones(outputs.size()))
        # 获取预测概率
        logits = outputs.logits[:, -1, :]
        # 计算覆盖评分
        coverage_logits = logits + coverage
        next_token = torch.argmax(coverage_logits, dim=-1).unsqueeze(-1)
        # 更新覆盖向量
        coverage[i:] = coverage[i:] * 0.9  # 示例覆盖衰减
        coverage[i] += 1.0
        # 更新输出
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```



