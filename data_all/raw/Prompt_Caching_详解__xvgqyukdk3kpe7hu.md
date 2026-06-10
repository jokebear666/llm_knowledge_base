# Prompt Caching 详解

<!-- source: yuque://zhongxian-iiot9/hlyypb/xvgqyukdk3kpe7hu -->

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453062751-9549f7fb-b48b-4c69-9393-bc768fc6186b.png)

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(26, 28, 30);">第一次听到 </font>**<font style="color:#74B602;">Prompt Caching </font>**<font style="color:rgb(26, 28, 30);">可能是 DeepSeek 当时推出了</font>**<font style="color:#74B602;">缓存命中 0.1 元每百万 tokens </font>**<font style="color:rgb(26, 28, 30);">的震撼价（DeepSeek API 创新采用硬盘缓存，价格再降一个数量级），随后各大厂商陆续跟进。</font>

<font style="color:rgb(26, 28, 30);">作为一个开发者，你是否也在思考：这是什么？怎么用？原理是什么？会影响输出质量吗？</font>

:::

:::color3
**<font style="color:rgb(26, 28, 30);">简介：</font>**<font style="color:rgb(26, 28, 30);">本文基于 OpenAI 官方博客、前沿论文《Prompt Cache: Modular Attention Reuse for Low-Latency Inference》及实战经验，为你一次性讲透 </font>**<font style="color:#ED740C;">Prompt Caching</font>**<font style="color:rgb(26, 28, 30);">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(26, 28, 30);">本文将分为两个部分，力求在</font>**<font style="color:rgb(26, 28, 30);">最佳实践</font>**<font style="color:rgb(26, 28, 30);">与</font>**<font style="color:rgb(26, 28, 30);">深度原理</font>**<font style="color:rgb(26, 28, 30);">之间取得平衡：</font>

+ **<font style="color:rgb(26, 28, 30);">如何使用</font>**<font style="color:rgb(26, 28, 30);">：面向 User 和 Developer，追求高效利用。</font>
+ **<font style="color:rgb(26, 28, 30);">深入理解</font>**<font style="color:rgb(26, 28, 30);">：面向 Geek，剖析原理、KV Cache 异同及技术挑战。</font>

**<font style="color:rgb(26, 28, 30);">OpenAI 官方博客</font>**<font style="color:rgb(26, 28, 30);">：</font>[https://platform.openai.com/docs/guides/prompt-caching](https://platform.openai.com/docs/guides/prompt-caching)

**<font style="color:rgb(51, 51, 51);">paper：</font>**[《Prompt Cache: Modular Attention Reuse for Low-Latency Inference》](https://arxiv.org/pdf/2311.04934)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453052935-e6e1454c-12bc-48b1-b851-40ab9fe99c69.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453037509-1eef8afb-746c-45fe-aa5c-710d412cce80.png)

## <font style="color:rgb(26, 28, 30);">Prompt Caching 如何使用 (Best Practices)</font>
:::color1
**<font style="color:rgb(26, 28, 30);">核心价值</font>**<font style="color:rgb(26, 28, 30);">：降低延迟（Latency）与 节省成本（Cost）。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453660573-5cb8b3d2-051c-4bc3-acb5-44359812ab47.png)

### <font style="color:rgb(26, 28, 30);">什么是 Prompt Caching？</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">简单来说，</font><font style="color:rgb(50, 48, 44);">Prompt Caching</font><font style="color:rgb(26, 28, 30);"> 是一种旨在</font>**<font style="color:#ED740C;">“存储”并“利用”模型输入中重复内容的技术</font>**<font style="color:rgb(26, 28, 30);">。</font>

:::

<font style="color:rgb(26, 28, 30);">我们知道，一个标准的 LLM 请求通常由两部分组成：</font>

```xml
Model Prompt = System Prompt + User Prompt

```

<font style="color:rgb(26, 28, 30);">在实际应用中，</font><font style="color:rgb(50, 48, 44);">System Prompt</font><font style="color:rgb(26, 28, 30);">（包含角色设定、长篇背景、Few-shot 示例等）往往是静态且重复的。Prompt Caching 让厂商将这些重复内容的计算结果“缓存”起来。</font>

+ **<font style="color:rgb(26, 28, 30);">对用户</font>**<font style="color:rgb(26, 28, 30);">：请求响应更快（TTFT 降低），费用更低（OpenAI 宣称成本降低 50%）。</font>
+ **<font style="color:rgb(26, 28, 30);">对厂商</font>**<font style="color:rgb(26, 28, 30);">：减少重复算力消耗。这是一个典型的双赢局面。</font>

### <font style="color:rgb(26, 28, 30);">为什么需要它？关注首 Token 延迟 (TTFT)</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">在聊天机器人等在线服务场景中，用户体验取决于 </font>**<font style="color:rgb(26, 28, 30);">TTFT (Time to First Token)</font>**<font style="color:rgb(26, 28, 30);">，即从发送请求到看到第一个字跳出来的时间。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">对于长 Context 的应用，TTFT 的大部分时间花在处理输入 Prompt 上。模型必须“读完”整个 Prompt 才能开始生成。</font>

+ **<font style="color:rgb(26, 28, 30);">无缓存</font>**<font style="color:rgb(26, 28, 30);">：每次请求都要重新计算整个 Prompt 的 Attention。</font>
+ **<font style="color:rgb(26, 28, 30);">有缓存</font>**<font style="color:rgb(26, 28, 30);">：模型直接调用已缓存的处理结果（KV states），就像已经“预习”过这段内容，可以直接开始作答。</font>

**<font style="color:rgb(26, 28, 30);">数据参考</font>**<font style="color:rgb(26, 28, 30);">：对于较长的 Prompt，延迟可降低高达</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">80%</font>**<font style="color:rgb(26, 28, 30);">。</font>

### <font style="color:rgb(26, 28, 30);">核心策略：Structuring Prompts</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">目前主流 API（如 OpenAI）主要采用**前缀匹配（Prefix Matching）**策略。这意味着只有当新请求的开头部分与缓存完全一致时，才能命中缓存。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color5
#### <font style="color:#601BDE;">❌</font><font style="color:#601BDE;"> 错误的写法</font><font style="color:#D22D8D;"> </font>
:::

<font style="color:rgb(26, 28, 30);">将动态内容放在前面，导致前缀被破坏：</font>

```xml
User: "帮我分析这份关于[用户A]的财报..."
System: "你是一个专业的金融分析师，拥有以下知识库..."
```

:::color5
#### <font style="color:#601BDE;">✅</font><font style="color:#601BDE;"> 正确的写法：静态在前，动态在后</font>
:::

<font style="color:rgb(26, 28, 30);">为了利用缓存，请务必将静态内容（指令、示例、工具定义）放在 Prompt 的</font>**<font style="color:rgb(26, 28, 30);">最开头</font>**<font style="color:rgb(26, 28, 30);">。</font>

```xml
System: "你是一个专业的金融分析师，拥有以下知识库..."  <-- 静态内容（被缓存）
User: "帮我分析这份关于[用户A]的财报..."             <-- 动态内容
```

### <font style="color:rgb(26, 28, 30);">高效缓存的 5 条 Best Practices</font>
:::color5
**<font style="color:#601BDE;">高效缓存的 5 条 Best Practices</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">合理甄别缓存内容</font>**<font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">妥善缓存那些稳定且高频复用的内容：系统指令、背景知识库、Few-shot 示例、工具（Function Definitions）。这些是“一劳永逸”的基础组件。</font>
+ **<font style="color:rgb(26, 28, 30);">优化内容排序 (最重要)</font>**<font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">牢记</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Static First, Dynamic Last</font>**<font style="color:rgb(26, 28, 30);">。将静态内容置于 Prompt 开头，将用户特定的可变信息放在结尾。这也适用于图像和工具定义。</font>
+ **<font style="color:rgb(26, 28, 30);">保持请求流的连续性</font>**<font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">缓存通常有淘汰机制（TTL）。为了减少淘汰，尽量保持使用相同前缀的连续请求流。OpenAI 的缓存通常在 5-10 分钟无活动后失效（非高峰期可达一小时）。</font>
+ **<font style="color:rgb(26, 28, 30);">策略性使用长 Prompt</font>**<font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">通常 API 只对超过一定长度（如 1024 tokens）的 Prompt 启用缓存。对于超短的指令，缓存收益不明显。</font>
+ **<font style="color:rgb(26, 28, 30);">平台差异化处理</font>**
    - **<font style="color:rgb(26, 28, 30);">OpenAI</font>**<font style="color:rgb(26, 28, 30);">:</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">自动生效</font>**<font style="color:rgb(26, 28, 30);">。无需改代码，只要前缀匹配且长度达标即可。</font>
    - **<font style="color:rgb(26, 28, 30);">Claude (Anthropic)</font>**<font style="color:rgb(26, 28, 30);">:</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">手动控制</font>**<font style="color:rgb(26, 28, 30);">。需要显式添加</font><font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(50, 48, 44);">cache_control</font><font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">标识。这允许你更灵活地在 Prompt 中间设置“断点”，但也增加了开发复杂度。</font>



## <font style="color:rgb(26, 28, 30);">Prompt Caching 深入理解</font>
:::color1
**<font style="color:rgb(26, 28, 30);">核心话题</font>**<font style="color:rgb(26, 28, 30);">：技术原理、KV Cache 辨析、PML 与位置编码。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453903272-155b4260-8371-4ad3-99dc-91158a9e938b.png)

### <font style="color:rgb(26, 28, 30);">原理：Cache Lookup & Hit</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">当一个长度达标（>1024 tokens）的请求发起时，服务端执行以下逻辑：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">Cache Lookup (查找)</font>**<font style="color:rgb(26, 28, 30);">：系统检查 Prompt 的前缀（Prefix）是否已存在于存储（内存或硬盘）中。这里通常使用类似</font>**<font style="color:rgb(26, 28, 30);">字典树 (Trie)</font>**<font style="color:rgb(26, 28, 30);"> 的结构来实现 O(L)</font>

<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">的高效查找。</font>

+ **<font style="color:rgb(26, 28, 30);">Cache Hit (命中)</font>**<font style="color:rgb(26, 28, 30);">：找到匹配前缀，直接复用计算过的 Attention States。</font>
+ **<font style="color:rgb(26, 28, 30);">Cache Miss (未命中)</font>**<font style="color:rgb(26, 28, 30);">：完整计算 Prompt，并将计算后的前缀状态存入缓存，供后续使用。</font>

### <font style="color:rgb(26, 28, 30);">Prompt Caching vs. KV Caching</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">这是很多开发者容易混淆的点。两者本质都是“空间换时间”，避免重复计算，但作用域完全不同。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453052935-e6e1454c-12bc-48b1-b851-40ab9fe99c69.png)

:::color5
**<font style="color:#601BDE;">1.KV Caching (Single Session)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">场景</font>**<font style="color:rgb(26, 28, 30);">：单次推理（Generation）。</font>
+ **<font style="color:rgb(26, 28, 30);">机制</font>**<font style="color:rgb(26, 28, 30);">：在自回归（Autoregressive）生成过程中，生成第 N 个 token 时，复用第 1 到 N−1 个 token 的计算结果。</font>
+ **<font style="color:rgb(26, 28, 30);">特点</font>**<font style="color:rgb(26, 28, 30);">：</font>**<font style="color:rgb(26, 28, 30);">Session 级别</font>**<font style="color:rgb(26, 28, 30);">。请求结束，KV Cache 通常即被释放。</font>

:::color5
**<font style="color:#601BDE;">Prompt Caching (Cross Session)</font>**

:::

+ **<font style="color:rgb(26, 28, 30);">场景</font>**<font style="color:rgb(26, 28, 30);">：跨请求（Cross-request）。</font>
+ **<font style="color:rgb(26, 28, 30);">机制</font>**<font style="color:rgb(26, 28, 30);">：将一个请求中计算好的 Prompt 部分的 KV 状态存储下来（可能是全局显存，甚至磁盘）。下一个完全无关的请求，只要前缀相同，就可以直接调取使用。</font>
+ **<font style="color:rgb(26, 28, 30);">特点</font>**<font style="color:rgb(26, 28, 30);">：</font>**<font style="color:rgb(26, 28, 30);">Global 级别</font>**<font style="color:rgb(26, 28, 30);">。它是一个全局管理器，实现了“一次计算，多次复用”。</font>

**<font style="color:rgb(26, 28, 30);">一句话总结</font>**<font style="color:rgb(26, 28, 30);">：KV Cache 加速的是“生成过程”，Prompt Cache 加速的是“理解过程（Prefill）”。</font>

### <font style="color:rgb(26, 28, 30);">进阶挑战：非前缀匹配与位置编码</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">OpenAI 使用的前缀匹配虽然简单，但有一个致命缺陷：</font>**<font style="color:#ED740C;">如果 Prompt 只有中间一小段变了，后面的静态内容就无法缓存了。</font>**

:::

:::color5
#### <font style="color:#601BDE;">解决方案：Prompt Markup Language (PML)</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453183656-9e0cbc86-5fa0-4c09-8a10-4de5edbae110.png)

<font style="color:rgb(26, 28, 30);">论文提出了一种结构化思路，通过标记语言明确区分“可变”与“不变”部分：</font>

```xml
<prompt>
  这是固定的背景介绍...
  <item>用户动态输入的内容</item>
  这是固定的输出要求...
</prompt>
```

<font style="color:rgb(26, 28, 30);">通过这种模块化（Modular）方式，系统可以识别出首尾是相同的模块。</font>

:::color5
#### <font style="color:#601BDE;">核心难题：Position Embedding</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(26, 28, 30);">Transformer 的 Attention 机制依赖位置编码（Position IDs）。</font>

+ **<font style="color:rgb(26, 28, 30);">问题</font>**<font style="color:rgb(26, 28, 30);">：相同的文本“输出要求”，如果中间插入的“用户内容”长度不同，它在整个 Prompt 中的绝对位置（Index）就会改变。导致 KV Cache 中的位置编码对不上，理论上无法直接复用。</font>
+ **<font style="color:rgb(26, 28, 30);">突破 (Update 2025/01/10)</font>**<font style="color:rgb(26, 28, 30);">：</font><font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">研究发现，</font>**<font style="color:rgb(26, 28, 30);">LLM 具有处理不连续 Position IDs 的能力</font>**<font style="color:rgb(26, 28, 30);">。</font><font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">只要保证 Token 之间的</font>**<font style="color:rgb(26, 28, 30);">相对位置</font>**<font style="color:rgb(26, 28, 30);">不变，即使我们将不同来源的 Attention States 拼接起来（导致 Position IDs 不连续），模型的输出质量也几乎不受影响。</font><font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">这为模块化缓存（Modular Attention Reuse）提供了理论基础：我们可以像拼积木一样拼接缓存模块。</font>

### <font style="color:rgb(26, 28, 30);">灵魂拷问：会影响输出质量吗？</font>
:::color3
**简介：**不会，或者极小差异<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">基于前缀匹配 (OpenAI 模式)</font>**<font style="color:rgb(26, 28, 30);">：</font><font style="color:rgb(26, 28, 30);">  
</font>**<font style="color:rgb(26, 28, 30);">不会</font>**<font style="color:rgb(26, 28, 30);">。因为物理上前缀的内容和位置完全一致，复用的数学结果是严格等价的。Prompt Caching 在这里是无损的。</font>
+ **<font style="color:rgb(26, 28, 30);">基于非前缀匹配 (PML/Modular 模式)</font>**<font style="color:rgb(26, 28, 30);">：  
</font>**<font style="color:rgb(26, 28, 30);">极小差异</font>**<font style="color:rgb(26, 28, 30);">。由于涉及到 Position IDs 的不连续拼接，虽然论文证明准确率与 Baseline 相当（Comparable），但在数学上并非 100% 逐位一致。对于极度敏感的任务，需要由开发者在灵活性和绝对一致性之间做 Trade-off。</font>

**使用提示缓存进行代码生成**

每个源文件都成为一个提示模块，允许用户以最小的开销在其提示上下文中“导入”文件。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453258605-69e73030-1b82-4343-b58d-006dde3c8e15.png)

**参数化prompt**

<旅行计划>在运行时重新配置，同时保持缓存效率，提供灵活的提示结构。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453262837-1ceb6ba2-7887-43d0-bbf2-426db6cc7d1b.png)

**个性化示例**

六个类别，每个类别包含五个特征。同一类别中的特征以 <union> 的形式分组。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453269820-77bc96b5-eb4d-4378-9429-63331d208c6a.png)

**缓存优势**

GPU 和 CPU 中计算开销和缓存开销的比较。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765453398227-243a29af-4108-4bc4-89c9-766860b98d94.png)

## <font style="color:rgb(26, 28, 30);">总结</font>
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">Prompt Caching 是 LLM 推理优化的重要里程碑。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">对于 User</font>**<font style="color:rgb(26, 28, 30);">：它是一个免费的午餐。只需记得**“把静态指令放前面”**，即可享受更快的速度和更低的价格。</font>
+ **<font style="color:rgb(26, 28, 30);">对于 Developer</font>**<font style="color:rgb(26, 28, 30);">：它是工程优化的利器。理解其背后的 KV 复用逻辑，能帮你写出更高效的 Prompt 结构。OpenAI 的前缀策略胜在简单稳定，Claude 的 </font><font style="color:rgb(50, 48, 44);">cache_control</font><font style="color:rgb(26, 28, 30);"> 胜在灵活精准，按需选择即可。</font>

