# LLM 投机采样

<!-- source: yuque://zhongxian-iiot9/hlyypb/xq7twt6n7nrntko8 -->

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近年来随着 LLM 如火如荼地发展</font>**<font style="color:#117CEE;">，对线上服务的推理延时的要求也越来越高</font>**<font style="color:rgb(25, 27, 31);">。由于 LLM 模型属于</font>[<font style="color:rgb(9, 64, 142);">自回归模型</font>](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=%E8%87%AA%E5%9B%9E%E5%BD%92%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，每个 Token 生成都需要重复加载大量的模型参数以及上文的 </font>[<font style="color:rgb(9, 64, 142);">KVCache</font>](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=KVCache&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，推理效率严重受制于仿存规模。所以大部份推理效率优化的工作都是围绕降低仿存规模进行设计，例如 KVCache 压缩、模型量化。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">近年来还兴起一种可以</font>**<font style="color:#ED740C;">合并 </font>**[**<font style="color:#ED740C;">Decode 阶段</font>**](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=Decode+%E9%98%B6%E6%AE%B5&zhida_source=entity)**<font style="color:#ED740C;">多轮仿存的方法——</font>**[**<font style="color:#ED740C;">投机采样</font>**](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=%E6%8A%95%E6%9C%BA%E9%87%87%E6%A0%B7&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。去年已经有不少工作在研究投机采样，其中以 </font>**<font style="color:#ED740C;">Medusa</font>**<font style="color:rgb(25, 27, 31);"> 的工作最为亮眼。今年有不少投机采样的相关工作在挑战着 Medusa，其中 </font>**<font style="color:#ED740C;">EAGLE </font>**<font style="color:rgb(25, 27, 31);">是算法设计非常精妙的投机采样工作。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**EAGLE-Decoding**](https://docs.sglang.ai/advanced_features/speculative_decoding.html#EAGLE-Decoding)

**paper： **[**MEDUSA**](https://arxiv.org/pdf/2401.10774)** **[**Speculative Decoding **](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)[**EAGLE-1**](https://arxiv.org/pdf/2401.15077)**  **[**EAGLE-2**](https://arxiv.org/pdf/2406.16858)**  **[**EAGLE-3**](https://arxiv.org/pdf/2503.01840)

**参考：**[**https://zhuanlan.zhihu.com/p/716344354**](https://zhuanlan.zhihu.com/p/716344354)

:::

**MEDUSA**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759133567941-a6dcc5b7-e83e-483c-9a28-088d267d9f60.png)

**EAGLE-1**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759133769731-e3b461f1-f51a-4e29-a14b-cf3589f01461.png)

**EAGLE-2**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759133646315-03afb355-16d4-4eac-bf88-041fcce9473b.png)![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759133650512-9c2703a0-54ef-4f47-ac39-ccf7e3116182.png)

**EAGLE-3**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759133682539-b9a396eb-af7c-418d-bd4b-7657de06d3e6.png)



## <font style="color:rgb(25, 27, 31);">相关工作</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">LLM 模型属于自回归模型，主要包含两个阶段：</font>**<font style="color:#74B602;">Prefill 和 Decode 阶段</font>**<font style="color:rgb(25, 27, 31);">。</font>[<font style="color:rgb(9, 64, 142);">Prefill 阶段</font>](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=Prefill+%E9%98%B6%E6%AE%B5&zhida_source=entity)<font style="color:rgb(25, 27, 31);">根据用户提供的 Prompt，批量处理 Prompt Tokens，生成第一个 Token 的输出，每个请求只执行一次 Prefill；而 Decode 阶段根据上一轮输出的 Token，作为当前轮次的输入，生成 Next Token，循环执行 Decode 直至生成终止符。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">通过实验可知，一个请求</font>**<font style="color:#ED740C;">大部份生成 Token 时间都花在了 Decode 阶段，用户大部份时间都花在了等待 Decode 阶段完成</font>**<font style="color:rgb(25, 27, 31);">。所以提升 Decode 阶段的生成 Token 效率可以很大程度提升用户的体验。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759130830506-10597b45-38b7-4958-8be7-5b89ae29dbf5.png)

> 起草第四和第五token t4和t5的方法的比较。t（由蓝色块表示）表示tokens，f（橙色块）表示features，下标表示它们在序列中的位置。红色边框表示模型草案的预测。为简单起见，如图所示，Lookahead的n元语法中的n已设置为2。
>

:::color5
**<font style="color:#601BDE;">投机采样步骤</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">针对 Decode 阶段生成效率低的问题，越来越多的工作开始研究投机采样。投机采样的目的是将多步自回归解码合并成一步，仅通过一次 LLM 推理完成多个 Token 的生成。现有的投机采样的通用做法包含以下三个步骤：</font>

1. **<font style="color:#117CEE;">【初始阶段】：</font>**<font style="color:rgb(25, 27, 31);">原始 LLM 进行常规的自回归解码，采样第一个 Token；</font>
2. **<font style="color:#117CEE;">【Draft 阶段】：</font>**<font style="color:rgb(25, 27, 31);">使用一个尺寸较小的 Draft 模型，输入原始 LLM 生成的 Token，通过特定的采样方式生成连续若干个 Draft Tokens；</font>
3. **<font style="color:#117CEE;">【Verify 阶段】：</font>**<font style="color:rgb(25, 27, 31);">使用原始 LLM 验证 Draft Tokens 序列。</font>

<font style="color:rgb(25, 27, 31);">目前，Draft Tokens 的采样方式有两种，分别是</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Token-Level 采样</font>](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=Token-Level+%E9%87%87%E6%A0%B7&zhida_source=entity)<font style="color:rgb(25, 27, 31);">以及</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Feature-Level 采样</font>](https://zhida.zhihu.com/search?content_id=247317636&content_type=Article&match_order=1&q=Feature-Level+%E9%87%87%E6%A0%B7&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>

### <font style="color:rgb(25, 27, 31);">Token Level 采样 —— </font>**<font style="color:#000000;">Speculative Decoding</font>**
:::color5
**<font style="color:#601BDE;">1.Speculative Decoding</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759133855773-cf0ccab9-37cf-4bd4-9ba2-5949669df878.png)

> 每一行代表算法的一次迭代。绿色token是近似模型（这里是一个类似GPT的Transformer解码器，具有6M个参数，在具有8ktoken的lm1b上训练）提出的建议，目标模型（这里，一个类似于GPT的Transformer解码器，在相同的设置中具有97M个参数）接受了这些建议，而红色和蓝色token分别是被拒绝的建议及其更正。例如，在第一行中，目标模型只运行了一次，并生成了5个token。
>

[Speculative Decoding](https://link.zhihu.com/?target=https%3A//proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">是最早提出投机采样的研究工作。作者通过观察 LLM 生成任务时，发现两个现象：</font>

1. <font style="color:rgb(25, 27, 31);">在自回归任务中，生成 K 个 Token 需要迭代 K 步。其中不同的 Token 生成难度不同，</font>**<font style="color:#74B602;">有的 Token 更“容易” 生成，可以用更轻量、更高效的模型完成这类 Token 的生成</font>**<font style="color:rgb(25, 27, 31);">；</font>
2. <font style="color:rgb(25, 27, 31);">LLM 在执行 Prefill 时，会并行生成 Token 序列对应的隐状态，对每个 Token 隐状态做一个 LM Head 的映射，可以得到每个 Token 对应的 Next Token 的概率。利用这个特性，可以将轻量模型生成出来的候选 Token 序列完成一次 LLM 的前向，得到候选 Token 序列对应的 Next Token 概率序列。</font>**<font style="color:#74B602;">通过该概率序列可以并行解码出若干个 Token，并且不会改变每个 Token 的生成概率分布</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">利用这两个观察，作者提出 Speculative Decoding。Speculative Decoding 会选择一个比原始模型轻量的 LLM 作为 Draft 模型，在 Draft 阶段使用自回归采样的方式连续生成若干个候选 Token，如上图所示。在 Verify 阶段，将得到的候选 Token 序列放入到原始 LLM 做验证 & Next Token 生成，实现并行解码。每一轮 Draft Token 生成，输入都是上一轮采样后得到的 Draft Token，所以这种采样方式称为 Token-Level 采样。</font>

:::color5
**<font style="color:#601BDE;">2.Speculative Decoding 存在的问题</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

尽管有明确的选择策略，Speculative Decoding 在实际落地中仍面临两大难以突破的瓶颈，直接限制其规模化应用：

**<font style="color:#2F4BDA;">关键矛盾：Draft 模型的 “轻量性” 与 “准确性” 平衡</font>**

Draft 模型是投机采样的核心组件，但其 “轻量程度” 与 “生成准确性” 存在天然矛盾，直接决定 overhead 和接受率，进而影响最终性能，具体矛盾表现如下：

| **Draft 模型特性** | **对 overhead 的影响** | **对接受率的影响** | **对整体性能的最终影响** |
| :--- | :--- | :--- | :--- |
| 过轻量（如参数极小的模型） | 开销极低（p 小） | 生成的 Token 与原始模型概率分布差异大，接受率低 | 因接受率过低，可能无法满足 “通过 Tokens 数> 1 + p”，无性能收益 |
| 过重（如接近原始模型参数） | 开销过高（p 大） | 生成的 Token 与原始模型概率分布接近，接受率高 | 因 p 过大，需通过极多 Tokens 才能满足收益条件，反而可能降低性能 |


1. **<font style="color:#2F4BDA;">Draft 模型的构建成本过高</font>**

Draft 模型的有效性依赖 “与原始模型分布一致”，而构建此类模型需承担三重高成本，具体如下：

+ **训练数据构造成本**：需获取与原始模型相同 / 相似分布的预训练数据，数据收集、清洗、对齐的成本极高；
+ **计算资源成本**：即使是轻量模型，预训练仍需大量 GPU/TPU 算力支持，硬件投入成本高；
+ **训练 Token 量成本**：为保证分布一致性，Draft 模型需达到足够的训练 Token 量（通常以百亿 / 千亿计），训练周期长、时间成本高。

若无法降低这三类成本，Speculative Decoding 难以在中小规模场景落地。

2. **<font style="color:#2F4BDA;">Token-Level 采样限制接受率上限</font>**

当前 Speculative Decoding 普遍采用 **Token-Level 采样**（即 Draft 模型的输入为 “Token Embedding”），但该方式存在天然缺陷：

+ Token Embedding 是模型对 Token 的**浅层特征表示**，仅包含基础语义信息，无法捕捉原始 LLM 深层的上下文关联、逻辑推理等复杂特征；
+ 轻量模型本身拟合能力有限，基于浅层特征更难复现原始模型的概率分布，导致 Draft Token 的准确性天花板低，Verify 阶段的接受率难以进一步提升。

### <font style="color:rgb(25, 27, 31);">Feature Level 采样 —— Medusa</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">Speculative Decoding 难以获取 Draft 模型最核心的原因是 Draft 模型是一个独立的模型。</font>**<font style="color:#117CEE;">独立模型意味着在训练 Draft 模型前要先挑选合适的轻量模型，并且必须满足训练成本低的特性</font>**<font style="color:rgb(25, 27, 31);">，以达到和原始模型输出概率分布相近的收敛效果。这一步涉及大量的实验成本，也是其难以落地的重要原因。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">独立的 Draft 模型是落地难的主要原因。针对 “独立” 这一特性，其中一个优化寻找 Draft 模型的思路是，</font>**<font style="color:#ED740C;">通过复用原始 LLM 已有的权重，训练出参数规模较小的增量权重</font>**<font style="color:rgb(25, 27, 31);">，这些增量的权重可以视作原始 LLM 的偏差，用于预测 Draft Token。这样可以保证生成 Token 时会先走原始 LLM 模型，然后通过叠加训练后的偏差，生成不同的 Draft Token。这种在生成 Draft Token 时复用原始 LLM 权重的方式也叫 Self Drafting。根据这个思路，</font>[**<font style="color:#ED740C;">Medusa</font>**](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2401.10774)**<font style="color:#ED740C;"> </font>**<font style="color:rgb(25, 27, 31);">应运而生。</font><font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759132094737-ec2e062a-044c-401a-bf48-3507673a6ad7.png)

> MEDUSA在LLM的最后一个隐藏状态之上引入了多个头，从而能够并行预测几个后续token。在推理过程中，每个头部都会为其指定位置生成多个top预测。这些预测被组合成候选，使用基于树的注意力机制并行处理。最后一步是验证候选token并接受继续。除了标准的拒绝采样方案外，这里还可以使用典型的接受方案来选择合理的延续，并且最长的可接受候选前缀将用于下一个解码阶段。
>

:::color5
**<font style="color:#601BDE;">1.Medusa 如何生成 Draft Token</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

1. **<font style="color:#117CEE;">输入与特征提取：</font>**
    - <font style="color:rgb(15, 17, 21);">输入自然语言 Prompt 到</font>**<font style="color:rgb(15, 17, 21);">原始 LLM 模型</font>**<font style="color:rgb(15, 17, 21);">。</font>
    - <font style="color:rgb(15, 17, 21);">模型计算后，输出一个</font>**<font style="color:rgb(15, 17, 21);">最后的隐状态</font>**<font style="color:rgb(15, 17, 21);">，该状态被视为输入 Prompt 的深层、高表达能力特征。</font>
2. **<font style="color:#117CEE;">并行预测头推理：</font>**
    - <font style="color:rgb(15, 17, 21);">该隐状态被</font>**<font style="color:rgb(15, 17, 21);">同时</font>**<font style="color:rgb(15, 17, 21);">送入以下两个部分：</font>
        * **<font style="color:rgb(15, 17, 21);">LM Head</font>**<font style="color:rgb(15, 17, 21);">： 预测下一个token。</font>
        * **<font style="color:rgb(15, 17, 21);">多个 Medusa Heads</font>**<font style="color:rgb(15, 17, 21);">： 每个 Head 独立预测一个未来的token。</font>
            + `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Medusa Head 1</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">-> 预测</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">Next Next Token</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">(位置: n+2)</font>
            + `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Medusa Head 2</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">-> 预测</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">Next Next Next Token</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">(位置: n+3)</font>
            + <font style="color:rgb(15, 17, 21);">... (以此类推)</font>
3. **<font style="color:#117CEE;">草稿与验证：</font>**
    - <font style="color:rgb(15, 17, 21);">由 LM Head 和所有 Medusa Heads 生成的一系列token构成了一个</font>**<font style="color:rgb(15, 17, 21);">草稿序列</font>**<font style="color:rgb(15, 17, 21);">。</font>
    - <font style="color:rgb(15, 17, 21);">后续（在原文未详述的部分）会有一个</font>**<font style="color:rgb(15, 17, 21);">验证阶段</font>**<font style="color:rgb(15, 17, 21);">，使用原始 LLM 快速验证该草稿序列的正确性，并接受其中正确的部分，从而实现一步生成多个有效token。</font>
4. **<font style="color:#117CEE;">关键技术特点</font>**
    - **<font style="color:rgb(15, 17, 21);">特征级采样</font>**<font style="color:rgb(15, 17, 21);">：</font>
        * <font style="color:rgb(15, 17, 21);">Medusa Heads 的输入是</font>**<font style="color:rgb(15, 17, 21);">原始模型的隐状态</font>**<font style="color:rgb(15, 17, 21);">，而非经过嵌入层处理的token。</font>
        * <font style="color:rgb(15, 17, 21);">这使得采样在更深层、信息更丰富的特征空间进行，提高了草稿token的质量。</font>
    - **<font style="color:rgb(15, 17, 21);">解耦与并行</font>**<font style="color:rgb(15, 17, 21);">：</font>
        * <font style="color:rgb(15, 17, 21);">将未来多个时间步的token预测任务，从串行依赖中</font>**<font style="color:rgb(15, 17, 21);">解耦</font>**<font style="color:rgb(15, 17, 21);">出来。</font>
        * <font style="color:rgb(15, 17, 21);">利用多个 Medusa Heads </font>**<font style="color:rgb(15, 17, 21);">并行计算</font>**<font style="color:rgb(15, 17, 21);">，一次性生成整个草稿序列，这是实现加速的关键。</font>

:::color5
**<font style="color:#601BDE;">2.Draft Token 验证</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759132130822-b73b0943-6599-4c2d-90b8-e3e850c3b0b8.png)

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1759132777348-da6d9680-0168-42c8-84ce-10fde0feab22.tif?x-oss-process=image/format,png)

1. **<font style="color:#117CEE;">Draft Token 生成与验证背景</font>**

在生成 Draft Token 后需进行验证。Medusa 在 Draft 阶段会批量生成若干步的 Draft Tokens，每一步有若干候选 Draft Tokens。若 Medusa Heads 个数为 N，每个 Medusa Head i 生成第 i 步的 Draft Tokens，每一步数量为 \(C_i\)，则候选路径数为 ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759132626213-d3c0d6c1-76d7-4b87-abae-0ce57e3338d5.png)。串行验证所有路径会因反复调用原始 LLM 推理，导致性能大幅下降，所以需并行验证。

2. **<font style="color:#117CEE;">Tree Attention⁺ 机制</font>**

为实现并行验证，Medusa 提出 Tree Attention⁺：

+ **序列拍平**：将所有路径拍平为一维序列，作为模型输入运行。
+ **Tree Mask 设计**：Attention 阶段为避免不同路径 Token 间计算注意力，对 Token 加 Mask（仿照 Casual Mask 设计），即 Tree Mask，让某一路径 Token 不 “看到” 其他路径 Token。不同 Step 的 Draft Token 构成 Draft 树，不同 Step 对应树中不同层节点。
3. **<font style="color:#117CEE;">Tree Attention 过程示例</font>**

以两个 Medusa Heads 为例：

+ Medusa Head 1 生成 2 个 Draft Tokens（“It” 和 “I”），对应树第一层，2 条长度为 1 的路径；Medusa Head 2 生成 3 个 Draft Tokens（“is”、“” 和 “the”），对应树第二层，6 条路径。
+ 构造长度为 8 的验证序列，按层设置 Tree Mask：树第一层两个 Token 仅 “看到” 自己；树第二层 Token 仅 “看到” 自己及前置的 “ It” Token。完成 Mask 构造后，可通过一次原始 LLM 推理调用批量验证所有 Draft 路径。
4. **<font style="color:#117CEE;">验证序列长度优化</font>**
+ **问题**：按 (C_i = [10, 10, 9, 4])（Medusa Head 1 至 4）配置，路径总数为 4610，验证序列长度达 4610，会引入大开销。且大部分路径接收概率低，无需验证。
+ **优化方法**：通过先验方式对 Draft 树剪枝，剪掉接收概率低的路径，缩短验证序列长度，避免算力浪费。例如剪枝后 5 层 Draft 树仅 64 个节点，验证序列长度为 64。

:::color5
**<font style="color:#601BDE;">3.Medusa 两大优势</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">与 Speculative Decoding 相比，Medusa 有两大优势：</font>

1. **<font style="color:#117CEE;">Draft 模型易于获取</font>**<font style="color:rgb(25, 27, 31);">：Medusa 属于 Self Drafting 投机采样，仅需添加几个 Medusa Head 层，通过 SFT 即可获得 Medusa 模型。Medusa 根据训练资源提供了两种训练方式：Medusa 1 和 Medusa 2。Medusa 1 冻结主干的参数，仅训练 Medusa Head，所需的 GPU 数量及训练时间都很小（Vicuna 7B 仅需单卡 A100，5个小时的训练时间）；Medusa 2 联合主干模型进行微调，预测精度更高，所需的训练资源对比 Medusa 1 也更高一点。</font>
2. **<font style="color:#117CEE;">接收率更大</font>**<font style="color:rgb(25, 27, 31);">：多个 Medusa Heads 并行采样，得到多条 Draft 路径。通过 Tree Attention 方式并行验证多个路径，提高单次投机采样的接收长度。除此之外，Draft Token 是通过隐状态采样得到的，理论上准确率会更高一些（Medusa 没有做消融实验，后面介绍的 EAGLE 有做相关的实验论证）。</font>

:::color5
**<font style="color:#601BDE;">4.Medusa 存在的问题</font>**<font style="color:#D22D8D;"> （by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">虽然 Medusa 对比 Speculative Decoding 有了很大的性能提升，但是仍然存在一些优化空间，主要包括两个方面：</font>

1. **<font style="color:#117CEE;">接收率</font>**<font style="color:rgb(25, 27, 31);">。Medusa 主要因为采样过程以及笛卡尔积构造 Draft 路径造成的。Medusa 采用了隐状态并行预测多步 Draft Tokens，在预测间隔 Tokens 时（即 Next Token 以后的 Draft Token），Draft Token 并不知道上一个 Token 是什么，预测时不确定性增加，也影响了间隔 Tokens 的准确率。</font>
2. **<font style="color:#117CEE;">Verify 效率</font>**<font style="color:rgb(25, 27, 31);">。Medusa 利用 Decode 阶段算力利用率低的特点，用算力换时间。通过增大单次推理的计算规模，提高计算仿存比，降低总的推理次数，从而降低 Decode 的总时间。但是由于算力资源有限，单次推理的计算规模不能一直增大。LLM 的自回归采样阶段的计算规模会随着 batch size 增大而增大，其计算仿存比也会增大，直至 Compute Bound 的边界。这个边界对应着一个临界的 batch size。Medusa 单次推理验证 64 条路径，最多接收 4 个 Token，算力需求对比常规的自回归采样增大了 16 倍，计算仿存比也增长了 16 倍，到达 Compute Bound 临界点的 batch size 对比常规的自回归采样也大大缩小了。当 batch size 超越临界点后，算力资源不足，性能上对比自回归采样会下降，这一问题 Medusa 也在论文中提到。所以 Medusa 在大流量请求下性能可能会劣化，个人认为比较适合小流量场景。</font>

### <font style="color:rgb(25, 27, 31);">小结</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">无论是 Speculative Decoding，还是 Medusa，都是围绕以下两个方面进行优化：</font>

1. **<font style="color:#ED740C;">Draft Token 的接收率</font>**<font style="color:rgb(25, 27, 31);">。这个主要依赖模型架构、算法设计以及模型训练。</font>
2. **<font style="color:#ED740C;">投机采样的 overhead</font>**<font style="color:rgb(25, 27, 31);">。overhead 主要来源于 Draft Token 生成，采样后处理以及验证 Draft Token 的效率。</font>

<font style="color:rgb(25, 27, 31);">这两点直接影响投机采样的性能，也是各个投机采样的优化方向，EAGLE 也将从这两个方向进行算法优化。</font>

:::

