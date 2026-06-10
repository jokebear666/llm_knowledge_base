# LLM长文本推理性能优化

<!-- source: yuque://zhongxian-iiot9/hlyypb/gd9t2k2c87d6bazf -->

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近期，LLM 的长文本能力越来越受到关注。LLM 处理长文本的能力可以应用在多个应用场景中，例如 LLM Agent、RAG、文本摘要、多模态都需要 LLM 模型具备长文本处理能力，这些应用在落地时需要</font>**<font style="color:#74B602;"> LLM 推理服务具备很高的长文本推理效率</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在长文本推理服务场景中，我们的目标是在给定显存空间，推理服务要处理的 Token 数尽可能的多，即T尽可能的大。KVCache 显存占用的计算公式如下所示，通过公式 2 可知，提升T有两种策略：</font>

1. **<font style="color:#ED740C;">对T维度进行压缩</font>**<font style="color:rgb(25, 27, 31);">，用较少的 token 信息表示全量 token 信息；</font>
2. **<font style="color:#ED740C;">对 L、H、N、D 四个维度进行压缩</font>**<font style="color:rgb(25, 27, 31);">，降低每个 token 的显存开销。</font>

<font style="color:rgb(25, 27, 31);">下面将分别介绍这两种策略相关的工作。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784056288-fd3601a8-bb42-4a3a-9f46-8ff49154d87e.png)

:::color5
**<font style="color:#601BDE;">KVCache 显存占用的计算 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">与 LLM 推理服务性能最关键的因素：KVCache 显存大小。KVCache 显存占用的计算公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758782749694-6c8ca02c-8410-4a22-a23e-600014ef32f3.png)

<font style="color:rgb(25, 27, 31);">其中:</font>

    - <font style="color:rgb(25, 27, 31);"> L表示模型层数（Layers）。</font>
    - <font style="color:rgb(25, 27, 31);"> H表示头维度大小（HeadDim）。</font>
    - <font style="color:rgb(25, 27, 31);"> N表示头数量（NumHeads）。</font>
    - <font style="color:rgb(25, 27, 31);"> F表示数据类型大小（DataType）。</font>
    - <font style="color:rgb(25, 27, 31);"> T表示总 Token 数（Tokens）。</font>
1. **<font style="color:#117CEE;">公式（1）分析：</font>**<font style="color:rgb(25, 27, 31);"> LLM 推理服务为每个 Token 分配了显存空间，其显存空间大小与模型层数、头维度、头数量以及KVCache存储的数据类型大小四个维度相关。</font>
2. **<font style="color:#117CEE;">公式（2）分析：</font>**<font style="color:rgb(25, 27, 31);">我们可以看到，KVCache 的总显存开销与 LLM 推理服务处理的总 Token 数以及每个 Token 所占的显存开销相关。在长文本推理服务场景中，我们的目标是在给定显存空间，推理服务要处理的 Token 数尽可能的多，即T尽可能的大。</font>

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">1. 压缩 KVCache 长度</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">LLM 最核心的模块是 Attention：通过 Q 、K  两个矩阵进行矩阵乘，计算O(T</font><sup><font style="color:rgb(25, 27, 31);">2</font></sup><font style="color:rgb(25, 27, 31);">)大小的注意力得分矩阵，并使用注意力得分矩阵对 V 矩阵求加权平均值，得到注意力层的输出矩阵。其中注意力得分矩阵每一行表示 Q 中每个 Token 和 K 中每个 Token 的相关性得分，注意力层输出矩阵的每一行表示每个 Token 与其他 Token 的加权平均值。即然是加权平均，</font>**<font style="color:#74B602;">说明每个 Token 的重要性并不相同，有的 Token 权重更大，而有的 Token 权重更小。</font>**

:::

:::color3
**简介：****<font style="color:#ED740C;">为了压缩 KVCache 长度，可以将 KVCache 中一些权重小的 Token 剔除，不参与注意力计算</font>**<font style="color:rgb(25, 27, 31);">，在保证模型效果的前提下压缩 KVCache 长度，从而在一定量的显存下保存更多的 Token，提高长文本的推理效率。那么压缩 KVCache 长度的问题就可以转化为寻找重要性 Token，通过算法设计找出一个序列中相关性更高的 Token。</font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

### <font style="color:rgb(25, 27, 31);">1.1 静态 Token 稀疏化</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">MIT 提出一种叫 StreamingLLM 的压缩 KVCache 长度的方法，并分析了四种 Attention 实现</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**https://github.com/mit-han-lab/streaming-llm**](https://github.com/mit-han-lab/streaming-llm)

**paper：**[**https://arxiv.org/pdf/2309.17453**](https://arxiv.org/pdf/2309.17453)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784284678-ed4393d4-be65-4f62-a3c1-c8797076cd4b.png)

:::color5
**<font style="color:#601BDE;">四种 Attention 实现</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

+ **<font style="color:rgb(25, 27, 31);">Dense Attention</font>**<font style="color:rgb(25, 27, 31);">：即最原始的 Attention 实现。其计算复杂度为 O(T</font><sup><font style="color:rgb(25, 27, 31);">2</font></sup><font style="color:rgb(25, 27, 31);">)，KVCache 存储复杂度为O(T)。由于复杂度比较高， T在预训练的时候会比较小。在推理的时候，当文本长度超过了预训练时的长度，模型效果就会大幅降级，所以表现出来的 PPL 值也比较大；</font>
+ **<font style="color:rgb(25, 27, 31);">Window Attention</font>**<font style="color:rgb(25, 27, 31);">：通过我们平时语言习惯中可以知道，一段话中每个字之间的相关性差别很大，一般来说越相近的字相关性越强。基于这个假设，Window Attention 就被提出。每个 Token 只和邻近的 Token 做 Attention 计算，所以计算复杂度为O(TL)  ，KVCache 存储复杂度为O(L)，其中 L 为窗口大小，是一个常数。这种方法极大的降低了 KVCache 的存储开销，从线性复杂度降低到常数复杂度。虽然KVCache的长度被压缩了，但是模型效果却不好，主要原因是最初始的 Token 被丢弃了。作者通过一些统计方法发现这种 Token 的重要性其实非常高，丢弃会严重影响模型效果。</font>
+ **<font style="color:rgb(25, 27, 31);">Sliding Window Attention with recomputation</font>**<font style="color:rgb(25, 27, 31);">：这种 Attention 与 Window Attention 类似，区别是 Sliding Window 不缓存窗口的 Tokens，而是重新计算窗口内的 KVCache。这种方法的计算复杂度为O(TL</font><sup><font style="color:rgb(25, 27, 31);">2</font></sup><font style="color:rgb(25, 27, 31);">) ，KVCache 存储复杂度为O(L)。计算效率下降了，但模型效果对比Window Attention 高，PPL 值远低于 Window Attention。主要原因是重计算把窗口中的 Tokens 作为初始 Tokens 了，这样既保留初始 Tokens 又保证计算只在一个窗口内，大大降低了KVCache 存储复杂度。</font>
+ **<font style="color:rgb(25, 27, 31);">StreamingLLM</font>**<font style="color:rgb(25, 27, 31);">：这种策略在 Window Attention 的基础上，保留整个序列的初始 Tokens。每个 token 只和窗口内的 Tokens 以及序列的初始 Tokens 进行 Attention 计算，这样既保留 Window Attention的特性，即保证 KVCache 存储复杂度为O(L)，计算复杂度为 O(TL) ，同时保证了模型效果不因丢失初始 Tokens 而大幅下降，PPL 和 Sliding Window Attention with recomputation 相似。</font>

:::color4
<font style="color:rgb(25, 27, 31);">总的来说，上述提到的稀疏化方法都是</font>**<font style="color:rgb(25, 27, 31);">静态的</font>**<font style="color:rgb(25, 27, 31);">，即 Token 之间的相关性是一种</font>**<font style="color:rgb(25, 27, 31);">固定的范式</font>**<font style="color:rgb(25, 27, 31);">，每个 Token 的相关的 Token 都是固定距离的。</font>

:::

### <font style="color:rgb(25, 27, 31);">1.2 动态 Token 稀疏化</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">静态 Token 稀疏化存在一个问题：Token 候选集过于固定。这种 Token 候选集的设计源于作者通过观察某些数据集中 Token 之间的相关性发现的规律。这种规律明显不能保证具备普适性，不能适用所有场景。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">动态 Token 稀疏化本质是为当前处理 Token 维护一个相关性高的历史 Token 集合，但与静态 Token 稀疏化不同，这个集合的构造不再由 Token 距离或者固定 Token 决定，而是设计一种算法去筛选历史的 Token。静态 Token 稀疏化是动态 Token 稀疏化的子集，所以理论上动态 Token 稀疏化的模型效果会比静态 Token 稀疏化更高。动态 Token 稀疏化主要有两个工作：</font>[H2O](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2306.14048)<font style="color:rgb(25, 27, 31);"> 以及 </font>[Quest](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2406.10774)<font style="color:rgb(25, 27, 31);">。</font>

**H2O paper：**[**https://arxiv.org/pdf/2306.14048**](https://arxiv.org/pdf/2306.14048)

**Quest paper：**[**https://arxiv.org/pdf/2406.10774**](https://arxiv.org/pdf/2406.10774)

:::

:::color5
**<font style="color:#601BDE;">1.H2O </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">为了维护历史 Token 集合，</font><font style="color:rgb(25, 27, 31);"> </font>[H2O](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2306.14048)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">提出了一种贪心的历史 Token 驱逐算法，具体流程如下：</font>

+ <font style="color:rgb(25, 27, 31);">初始化相关性历史 Token 集合 S</font><sub><font style="color:rgb(25, 27, 31);">0</font></sub><font style="color:rgb(25, 27, 31);"> ，设置集合最大容量 k 。</font>
+ <font style="color:rgb(25, 27, 31);">开始迭代更新历史 Token 集合：</font>
    - <font style="color:rgb(25, 27, 31);">当历史 Token 集合大小等于最大容量 k 时，将当前 Token 加入历史 Token 集合中；</font>
    - <font style="color:rgb(25, 27, 31);">当历史 Token 集合大小大于等于最大容量时，计算当前 Token 和历史 Token 集合中所有 Token 的相关性得分，分数越高相关性越低，将最低分的 Token 从集合中剔除，将当前 Token 加入到集合中。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784517634-0f4ed8d2-023c-4568-9d0c-63b8f4431add.png)

<font style="color:rgb(25, 27, 31);">相关性得分的计算开销很小，所以该方法的计算复杂度为 O(TL) ，KVCache 存储复杂度为 O(L)。作者也和StreamingLLM 对比了模型效果，在 QA 任务以及文档摘要任务均优于 StreamingLLM。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784550423-436d146c-4485-4617-9409-94b5c7bfd2dc.png)

:::color5
**<font style="color:#601BDE;">2.Quest </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**The attention map of prompt**![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784615600-0ff58dfc-5773-4d00-8b08-0f6e2f183bfb.png)

**Recall rate of tokens with Top-10 attention scores.**![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784623740-5547c072-038c-4462-a866-fc1886b17467.png)

<font style="color:rgb(25, 27, 31);">Quest 使用 KVCache 页中最大和最小 Key 向量的信息估算一页 KVCache 和当前输入 Query 向量的相关性。该 Attention 算法流程如下：</font>

1. <font style="color:rgb(25, 27, 31);">生成 KVCache 时，将新增的 KVCache 保存到常规 KVCache 显存池，并且计算新增的 KVCache 页的最大最小 Key 向量，将最大最小向量保存到 MetaKVCache 显存池中；</font>
2. <font style="color:rgb(25, 27, 31);">开始进行 Attention 算法。包含两个阶段：</font>
    1. **<font style="color:#117CEE;">打分阶段：</font>**<font style="color:rgb(25, 27, 31);">给每个历史 Page 打分。从 MetaKVCache 中加载最大最小 Key 向量，当前的 Query 向量分别和最大最小 Key 向量进行 Elementwise 乘法，得到两个向量结果。对两个向量结果进行 Elementwise Max，得到一个向量结果，再求和，得到该 Page 的得分；根据得分选择 Top K 个 Page 作为 Token 集。</font>
    2. **<font style="color:#117CEE;">Attention计算阶段：</font>**<font style="color:rgb(25, 27, 31);">当前的 Query 向量和 Top K 个 Page 的 KVCache 进行稀疏 Attention 计算。</font>

<font style="color:rgb(25, 27, 31);">通过这种 Attention 算法，Quest 对比 Full Attention 大大降低了 KVCache 的访存量。假设每一个 KV 向量的大小为 M 字节，KVCache 的 Token 数为 L ，每一页的 KVCache 有 S 个 Token（页大小），L/S 为页数， K 为历史 Token 候选集大小。那么在第一阶段的访存量为 2ML/S 字节，而第二阶段的访存量为 2MKS 字节，所以 Quest 算法总的 KVCache 访存量为 2ML/S + 2MKS 。Full Attention 的访存量为 2ML 字节，所以 Quest 算法和 Full Attention 算法的访存比为 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758783009204-9888cd23-7a1f-40b6-baf0-495d61d87800.png)<font style="color:rgb(25, 27, 31);"> 。当页大小设为 16，K 设为 256，历史 Token 数为 64K 时，Quest 的访存量仅约为 Full Attention 访存量的  1/8。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758784756397-4966d51e-af4a-46c1-8c9d-494fa00e3fa1.png)

:::color4
<font style="color:rgb(25, 27, 31);">后续与动态 Token 稀疏化相关的工作可能会继续聚焦于模型效果方面，比如得分函数的设置以及剔除策略的改进。计算复杂度已经到线性复杂度，KVCache 存储复杂度已经到了常量复杂度，难以继续优化。</font>

:::

### <font style="color:rgb(25, 27, 31);">1.3 </font>[<font style="color:rgb(9, 64, 142);">Prefix Caching</font>](https://zhida.zhihu.com/search?content_id=243309811&content_type=Article&match_order=1&q=Prefix+Caching&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 工程优化</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">Prefix Caching 是最近比较火的工程优化，其原理是复用 Tokens 的KVCache。LLM 推理服务在完成一个 request 计算后，不会马上将其 KVCache 释放，而是先缓存。当</font>**<font style="color:#74B602;">下一个请求到达时，不会直接进行 Prefill 计算，而是先在缓存中寻找最长公共前缀的 Tokens。</font>**<font style="color:rgb(25, 27, 31);">如果存在，则直接复用缓存中的 KVCache，仅对剩余 Tokens 计算注意力以及 KVCache。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">通过复用 KVCache，可以达到两大目的：</font>

1. **<font style="color:#ED740C;">提升 Prefill 效率。</font>**<font style="color:rgb(25, 27, 31);">由于参与 Prefill 的 Tokens 数减少，所以计算量下降，Prefill 的延时也就下降，直接提升 TTFT 性能。特别适合优化多轮对话场景的性能。</font>
2. **<font style="color:#ED740C;">节省显存。</font>**<font style="color:rgb(25, 27, 31);">当前大部分 LLM 应用在构造输入时一般遵循 system prompt + user prompt 范式。大部分的 system prompt 都是一致，这样不同的请求也就有相同的前缀，可以避免出现多个冗余的 system prompt KVCache，能提高服务的极限吞吐。</font>

:::

<font style="color:rgb(25, 27, 31);">在实现高效的 Prefix Caching 功能时，需要考虑两个问题：</font>

1. <font style="color:rgb(25, 27, 31);">如何管理缓存 Tokens？应该保留哪些前缀？</font>
2. <font style="color:rgb(25, 27, 31);">能否针对 Prefix Caching 实现高效的 CUDA 算子？</font>

:::color5
**<font style="color:#601BDE;">1.</font>**[**<font style="color:#601BDE;">Radix Attention</font>**](https://zhida.zhihu.com/search?content_id=243309811&content_type=Article&match_order=1&q=Radix+Attention&zhida_source=entity)**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758785071975-5cef7d03-5623-4059-8fc3-7290adec992d.png)

<font style="color:rgb(25, 27, 31);">针对第一个问题，lmsys 提出了 Radix Attention，设计了一种基于 LRU 的 Radix Tree 去管理前缀 Tokens。如上图所示，新到达的请求会先从 Radix Tree 中匹配最长前缀，寻找最远的一个节点。当请求仍有 Tokens 没匹配到已有的前缀，则会新增 Token 子节点。每次新增 Token 时，将新增 Token 节点标记为绿色，并将其前缀的节点标记为蓝色。这种标记主要是更新节点的访问时间，当缓存空间不足时，会将最近没被访问的节点清除。</font>

:::color5
**<font style="color:#601BDE;">2.Cascade Inference </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">针对第二个问题，FlashInfer 团队提出了</font><font style="color:rgb(25, 27, 31);"> </font>[Cascade Inference](https://link.zhihu.com/?target=https%3A//flashinfer.ai/2024/02/02/cascade-inference.html)<font style="color:rgb(25, 27, 31);">，用于提升多个请求共享前缀的 Batch Decoding 过程。在介绍 Cascade Inference 前，我们先了解下 Batch Decoding Attention 的 CUDA 实现原理。</font>

+ **<font style="color:rgb(25, 27, 31);">朴素 Batch Decoding Attention CUDA 实现原理：</font>**<font style="color:rgb(25, 27, 31);">先考虑 MHA。对于 Attention 运算，设 Q 在 T 维度上长度为  q_len， K 、V  在 T 维度上长度为  kv_len，那么 Attention 的三个输入矩阵的 Shape 分别为 [B, N, q_len, H]、[B, N, kv_len, H]、 [B, N, kv_len, H]。其中 [B, N] 两个维度是 Batch 维度，可以并行计算，所以 Attention 算子的 CUDA Kernel 会将 Grid Size 设置为 [B, N]，一个 Thread Block 计算一个序列的单个头注意力，所以一个 Thread Block 的三个输入矩阵 q,k,v 的 Shape 为 [q_len, H]、[kv_len, H]、[kv_len, H]。Attention 计算可以简单分解为以下三步：</font>
1. <font style="color:rgb(25, 27, 31);">s = qk</font><sup><font style="color:rgb(25, 27, 31);">T</font></sup><font style="color:rgb(25, 27, 31);">，对 q,k 进行矩阵乘，得到 Shape 为 [q_len, kv_len] 的中间变量  。</font>
2. <font style="color:rgb(25, 27, 31);"> s = softmax(s)，对步骤 1 得到的中间变量 s 在 kv_len 维度执行归一化操作，得到 Shape 为 [q_len, kv_len] 的中间变量  。</font>
3. <font style="color:rgb(25, 27, 31);">o = sv</font><sup><font style="color:rgb(25, 27, 31);">T</font></sup><font style="color:rgb(25, 27, 31);">，对步骤 2 得到的中间变量 s 和 v 进行矩阵乘，得到 Shape 为 [q_len, H] 的最终结果 o。</font>

<font style="color:rgb(25, 27, 31);">在 Decoding 阶段，q_len 为 1，所以上述提到的中间变量大小较小，可以放到 Shared Memory 中保存，那么 Batch Decoding Attention 的算术强度可以表示为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758783064175-901844f8-2e7b-4ab4-a3be-ab1440f8cbbf.png)

+ **<font style="color:rgb(25, 27, 31);">共享前缀 Batch Decoding Attention CUDA 实现原理</font>**<font style="color:rgb(25, 27, 31);">：回到共享前缀的场景。当 Batch Decoding Attention 所有输入请求的前缀完全一致时，输入的 Q、K 、V  三个矩阵的 Shape 分别为 [B, N, q_len, H]、[1, N, shared_kv_len, H]、 [1, N, shared_kv_len, H]。</font>**<font style="color:rgb(25, 27, 31);">类似 MQA ，GridSize 可以设置为 [N] ，那么一个 Thread Block 的三个输入矩阵 q,k,v 的 Shape 将为 [B*q_len, H]、 [shared_kv_len, H] 、 [shared_kv_len, H]，q_len 相比 MHA 实现"提升"了 B 倍，算术强度也提升接近 B 倍，同样可以降低访存开销。</font>**<font style="color:rgb(25, 27, 31);">以下是 Decoding 阶段的 MHA、MQA 以及 BatchPrefixAttention（BPA）的对比：</font>

| **<font style="color:rgb(25, 27, 31);">Attention 类型</font>** | **<font style="color:rgb(25, 27, 31);">Grid Size设置</font>** | **<font style="color:rgb(25, 27, 31);">算术强度</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">MHA</font> | <font style="color:rgb(25, 27, 31);">[B, N]</font> | <font style="color:rgb(25, 27, 31);">O(1)</font> |
| <font style="color:rgb(25, 27, 31);">MQA</font> | <font style="color:rgb(25, 27, 31);">[B]</font> | <font style="color:rgb(25, 27, 31);">O(N)</font> |
| <font style="color:rgb(25, 27, 31);">BPA</font> | <font style="color:rgb(25, 27, 31);">[N]</font> | <font style="color:rgb(25, 27, 31);">O(B)</font> |


<font style="color:rgb(25, 27, 31);">但 BPA 这个算子只适用于前缀完全一样时的 Decoding，当输入多个请求的后缀不同时，仍然需要使用常规的 Decoding Attention 算子，计算后缀的注意力的局部结果，然后使用类似 FlashAttention 将前缀、后缀的注意力局部结果进行合并。这就是 Cascade Inference 的做法。具体流程如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758785120929-71329f9e-b979-418c-8d39-011f78fa9f45.png)

<font style="color:rgb(25, 27, 31);">图中上半部分描述了常规的 Decoding Attention 的做法，下半部分描述了 Cascade Inference 的思想。Cascade Inference 主要包含三个步骤：</font>

    1. <font style="color:rgb(25, 27, 31);">MQA。对共享前缀部分使用 MQA 算子，提高算术强度；</font>
    2. <font style="color:rgb(25, 27, 31);">Batch Decode Attention。对不同的后缀使用常规的 Decoding Attention 算子，计算后缀的注意力；</font>
    3. <font style="color:rgb(25, 27, 31);">Merge State。以上两步仅完成序列中一部分的 Attention 结果，需要将 Attention 结果进行合并，合并方式与FlashAttention 类似。</font>
+ <font style="color:rgb(25, 27, 31);">Cascade Attention 的源码：</font>

```python
class BatchDecodeWithSharedPrefixPagedKVCacheWrapper:
    def forward(
        self,
        q: torch.Tensor,
        k_shared: torch.Tensor,
        v_shared: torch.Tensor,
        unique_kv_data: torch.Tensor,
        allow_fp16_qk_reduction=False,
        sm_scale: Optional[float] = None,
        rope_scale: Optional[float] = None,
        rope_theta: Optional[float] = None,
    ):
        # MQA
        V_shared, S_shared = single_prefill_with_kv_cache_return_lse(
            q,
            k_shared,
            v_shared,
            causal=False,
            pos_encoding_mode="NONE",
            kv_layout=self._kv_layout,
            allow_fp16_qk_reduction=allow_fp16_qk_reduction,
            sm_scale=sm_scale,
            rope_scale=rope_scale,
            rope_theta=rope_theta,
        )
        # Batch Decode Attention
        V_unique, S_unique = self._batch_decode_wrapper.forward_return_lse(
            q,
            unique_kv_data,
            pos_encoding_mode="NONE",
            sm_scale=sm_scale,
            rope_scale=rope_scale,
            rope_theta=rope_theta,
        )
        # Merge State
        merge_state_in_place(V_shared, S_shared, V_unique, S_unique)
        return V_shared
```

### <font style="color:rgb(25, 27, 31);">1.4 小结</font>
:::color3
<font style="color:rgb(25, 27, 31);">在压缩 KVCache 长度方面，主要包括两大类工作：</font>

+ <font style="color:rgb(25, 27, 31);">Token 稀疏化。这是一种算法层面的优化，直接降低了计算。但由于舍弃了部分 Token 的注意力计算，所以理论上是有损的，可能需要训练侧保证模型效果。而 Token 稀疏化也大致分为两类：动态稀疏化和静态稀疏化。两种稀疏化共同点是在计算预测下一个 Token 时，只维护一个窗口大小的历史 Token 信息。静态稀疏化的窗口内的 Token 是固定的，而动态稀疏化是不固定的。</font>
+ <font style="color:rgb(25, 27, 31);">Prefix Caching。这是一种工程优化，算法层面上是一种无损优化，无需训练侧介入。</font>

<font style="color:rgb(25, 27, 31);">这两类工作是正交的，可以叠加使用。</font>

:::



## <font style="color:rgb(25, 27, 31);">参考文献</font>
+ [https://yaofu.notion.site/Full-Stack-Transformer-Inference-Optimization-Season-2-Deploying-Long-Context-Models-ee25d3a77ba14f73b8ae19147f77d5e2#d03b8a2a583246cea5a1fdeb8f583586](https://link.zhihu.com/?target=https%3A//yaofu.notion.site/Full-Stack-Transformer-Inference-Optimization-Season-2-Deploying-Long-Context-Models-ee25d3a77ba14f73b8ae19147f77d5e2%23d03b8a2a583246cea5a1fdeb8f583586)
+ [阿杰：vLLM & PagedAttention 论文深度解读（一）—— LLM 服务现状与优化思路](https://zhuanlan.zhihu.com/p/656939628)
+ [MODEL TELLS YOU WHAT TO DISCARD: ADAPTIVE KV CACHE COMPRESSION FOR LLMS](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2310.01801)
+ [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2306.14048)
+ [Efficient Streaming Language Models with Attention Sinks](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2309.17453)
+ [Confused with four attention mechanism and their performance mentioned by paper · Issue #33 · mit-han-lab/streaming-ll](https://link.zhihu.com/?target=https%3A//github.com/mit-han-lab/streaming-llm/issues/33)
+ [https://lmsys.org/blog/2024-01-17-sglang/](https://link.zhihu.com/?target=https%3A//lmsys.org/blog/2024-01-17-sglang/)
+ [Cascade Inference: Memory Bandwidth Efficient Shared Prefix Batch Decoding](https://link.zhihu.com/?target=https%3A//flashinfer.ai/2024/02/02/cascade-inference.html)
+ [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2404.16710)
+ [You Only Cache Once: Decoder-Decoder Architectures for Language Models](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2405.05254)
+ [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2402.02750)

