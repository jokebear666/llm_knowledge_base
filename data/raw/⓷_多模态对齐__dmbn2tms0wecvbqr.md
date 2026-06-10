# ⓷ 多模态对齐

<!-- source: yuque://zhongxian-iiot9/hlyypb/dmbn2tms0wecvbqr -->

# 多模态对齐
## LLAVA与CLIP对齐的对比<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">CLIP</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐 是其核心能力，通过</font>**<font style="color:#ED740C;">对比学习（Contrastive Learning）</font>**<font style="color:rgb(25, 27, 31);">将图像和文本映射到统一的语义空间。</font>

**<font style="color:rgb(25, 27, 31);">LLaVA</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐的核心是通过一个</font>**<font style="color:#ED740C;">轻量级线性投影层将视觉特征映射到语言模型的词嵌入空间</font>**<font style="color:rgb(25, 27, 31);">，结合两阶段训练策略实现高效对齐。以下是详细的技术分解：</font>

**<font style="color:rgb(51, 51, 51);">参考</font>**<font style="color:rgb(51, 51, 51);">：</font>[CLIP和LLaVA中的对齐细节](https://zhuanlan.zhihu.com/p/27728623876)

:::

:::color5
**<font style="color:#601BDE;">1.CLIP多模态对齐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849995591-667a0c79-beab-443f-931c-f351159cd7c4.png)

1. 模型结构
    - <font style="color:rgb(25, 27, 31);">图像编码器：例如 Vision Transformer（ViT）或 ResNet，将图像编码为特征向量。</font>
    - <font style="color:rgb(25, 27, 31);">文本编码器：例如 Transformer，将文本编码为特征向量。</font>
2. 对齐方法
    - <font style="color:rgb(25, 27, 31);">输入：</font>
        * <font style="color:rgb(25, 27, 31);">图像：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[img_1, img_2, ..., img_N]</font>`
        * <font style="color:rgb(25, 27, 31);">文本：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[text_1, text_2, ..., text_N]</font>`
    - <font style="color:rgb(25, 27, 31);">步骤：</font>
        * **<font style="color:rgb(25, 27, 31);">a.特征提取：</font>**
            + <font style="color:rgb(25, 27, 31);">图像特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">I = image_encoder(img_1), ..., image_encoder(img_N)</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">→ 维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
            + <font style="color:rgb(25, 27, 31);">文本特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">T = text_encoder(text_1), ..., text_encoder(text_N)</font>`<font style="color:rgb(25, 27, 31);"> → 维度 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
        * **<font style="color:rgb(25, 27, 31);">b.相似度计算：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">计算所有图像和文本的余弦相似度矩阵</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S</font>`<font style="color:rgb(25, 27, 31);">，维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, N]</font>`<font style="color:rgb(25, 27, 31);">：</font>

```plain
S[i][j] = cosine_similarity(I[i], T[j])
```

    - <font style="color:rgb(25, 27, 31);">理想情况下，对角线元素 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S[i][i]</font>`<font style="color:rgb(25, 27, 31);"> 应最大（匹配对），非对角线元素应较小（不匹配对）</font>
        * **<font style="color:rgb(25, 27, 31);">c.对比损失（InfoNCE）：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">对每个图像</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">i</font>`<font style="color:rgb(25, 27, 31);">，计算其与所有文本的相似度，通过 softmax 得到概率分布：</font>

```plain
p_image2text(i) = exp(S[i][i]/τ) / sum_{j=1}^N exp(S[i][j]/τ)
```

        * <font style="color:rgb(25, 27, 31);">对每个文本</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">j</font>`<font style="color:rgb(25, 27, 31);">，同理计算</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">p_text2image(j)</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">总损失为两个方向的交叉熵之和：</font>
        * <font style="color:rgb(25, 27, 31);">其中 τ 是温度参数，控制分布集中程度。</font>

```plain
loss = -1/(2N) * sum_{i=1}^N [log(p_image2text(i)) + log(p_text2image(i))]
```

:::color5
**<font style="color:#601BDE;">2.LLAVA多模态对齐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849977575-d145922b-3207-4c22-a51a-e5519ce67e37.png)

1. **模型架构**
    1. <font style="color:rgb(25, 27, 31);">视觉编码器：CLIP-ViT-L/14（输出维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[H, W, D_img] = [16, 16, 1024]</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    2. <font style="color:rgb(25, 27, 31);">线性投影层（对齐模块）：单层全连接网络（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj ∈ R^{D_img × D_text}</font>`<font style="color:rgb(25, 27, 31);">），将图像特征转换为语言模型兼容的维度（如</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text=4096</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    3. <font style="color:rgb(25, 27, 31);">语言模型：</font>[<font style="color:rgb(9, 64, 142);">Vicuna</font>](https://zhida.zhihu.com/search?content_id=254568449&content_type=Article&match_order=1&q=Vicuna&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（LLaMA架构的指令微调版本），词嵌入维度为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text</font>`<font style="color:rgb(25, 27, 31);">。</font>
2. **对齐步骤**
    1. **<font style="color:rgb(25, 27, 31);">视觉特征处理</font>**
        * <font style="color:rgb(25, 27, 31);">输入图像：尺寸</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">224×224</font>`<font style="color:rgb(25, 27, 31);">，通过ViT划分为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">16×16</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个patch，输出特征图</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[16×16, 1024]</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">特征扁平化：将空间维度合并为序列，得到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×1024</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的特征矩阵。</font>
        * <font style="color:rgb(25, 27, 31);">线性投影：通过 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj</font>`<font style="color:rgb(25, 27, 31);"> 将每个patch特征转换为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">4096</font>`<font style="color:rgb(25, 27, 31);"> 维，得到 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);"> 的视觉token序列。</font>
    2. **<font style="color:rgb(25, 27, 31);">步骤2：与文本token拼接</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">将视觉token（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);">）与文本token（如问题“描述这张图片”）拼接，形成联合输入序列。</font>
        * <font style="color:rgb(25, 27, 31);">示例：输入序列 = [IMG_1, IMG_2, ..., IMG_256] + [Q1, Q2, ..., Qn]</font>
        * <font style="color:rgb(25, 27, 31);">语言模型（Vicuna）将此序列视为“多模态prompt”，自回归生成答案。</font>
    3. **<font style="color:rgb(25, 27, 31);">预训练（特征对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：对齐视觉与语言特征，使投影后的视觉token能被语言模型“理解”。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用约 600K 图像-文本对（来自CC3M等），构造单轮指令数据（如“请描述图像” + 人工标注描述）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">冻结参数：</font>**<font style="color:#ED740C;">视觉编码器和语言模型权重固定</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">仅训练投影层：通过最小化语言模型的交叉熵损失，优化视觉到文本的映射。</font>
            + <font style="color:rgb(25, 27, 31);">关键公式：</font>
    4. **<font style="color:rgb(25, 27, 31);">阶段2：指令微调（任务对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：提升模型对复杂指令（如推理、问答）的响应能力。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用158K GPT-4生成的指令-答案对（涵盖描述、推理、对话等任务）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">解冻语言模型：</font>**<font style="color:#ED740C;">微调语言模型参数（LoRA或全参数微调）</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">联合优化：投影层和语言模型共同更新，强化跨模态交互。</font>
            + <font style="color:rgb(25, 27, 31);">示例任务：</font>
                - <font style="color:rgb(25, 27, 31);">输入：图像 + “图中的小狗是什么颜色？”</font>
                - <font style="color:rgb(25, 27, 31);">输出：语言模型需结合视觉token（如“黑色毛发”）生成答案“黑色”。</font>

:::color5
**<font style="color:#601BDE;">3.MLP对齐的优势</font>**

:::

1. <font style="color:rgb(25, 27, 31);">轻量化设计：</font>
    1. <font style="color:rgb(25, 27, 31);">仅需训练投影层（约0.1%参数量），远低于跨注意力模型（如Flamingo需训练20%参数）。</font>
2. <font style="color:rgb(25, 27, 31);">数据高效：</font>
    1. <font style="color:rgb(25, 27, 31);">预训练阶段仅需百万级图文对，指令微调阶段依赖合成数据（无需人工标注）。</font>
3. <font style="color:rgb(25, 27, 31);">零样本泛化：</font>
    1. <font style="color:rgb(25, 27, 31);">对齐后的模型可直接处理未见过的任务类型（如视觉推理、OCR问答）。</font>

## <font style="color:rgb(25, 27, 31);">MLP逐渐取代Q-Former的原因？</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">多模态大语言模型（MLLM）为什么最近的工作中用BLIP2中Q-Former结构的变少了，很多都是直接用两种模态直接进行MLP后拼接？Q-Former不应该会比直接拼接好吗？</font>

:::

:::color3
**参考：**[**多模态大语言模型（MLLM）为什么最近的工作中用BLIP2中Q-Former结构的变少了？**](https://www.zhihu.com/question/626796690/answer/3584553322)

**paper：《**[DeCo: Decoupling Token Compression from Semantic Abstraction in Multimodal Large Language Models](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2405.20985)**》**

:::

:::color5
**<font style="color:#601BDE;">1.核心原因</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">最核心的原因在于</font>**<font style="color:rgb(25, 27, 31);">：相比MLP的方案（LLaVA-1.5），</font>**<font style="color:#ED740C;">BLIP-2的Q-Former参数量更大，收敛更慢，相同setting下无法取得LLaVA-1.5这样优秀的性能</font>**<font style="color:rgb(25, 27, 31);">。并且，在数据量和计算量都充足的前提下，Q-Former也没有展现出明显的性能收益。</font>

:::color5
**<font style="color:#601BDE;">2.其他原因</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">MLP和Q-Former的竞争其实就是</font>**<font style="color:#74B602;">LLaVA系列和BLIP系列的竞争</font>**<font style="color:rgb(25, 27, 31);">，大家选择了MLP其实主要是选择了</font>**<font style="color:#74B602;"> follow LLaVA的工作</font>**<font style="color:rgb(25, 27, 31);">。</font>

1. **更高效易用的训练代码**：LLaVA和BLIP都开源了自己的训练代码，**<font style="color:#74B602;">前者基于HuggingFace的transformers.Trainer实现</font>**，后者则是基于自己团队的codebase实现。虽然两套代码都十分优秀，但是现在的MLLM主要依赖于LLM构建，而transformers作为LLM领域开源的default choice，其优势地位毋庸置疑。从思维惯性的角度来说，既然LLM都用transfomers实现了，那训练框架当然也是用配套的Trainer啦。
2. **更强的baseline setting**：LLaVA和BLIP2其实可以看成同期工作，而BLIP2因为时间更早，所以早期关注度明显更高。例如当时爆火的[MiniGPT-4](https://zhida.zhihu.com/search?content_id=670965997&content_type=Answer&match_order=1&q=MiniGPT-4&zhida_source=entity)就是选择了BLIP2的技术路线。**<font style="color:#74B602;">然而，LLaVA的后续工作LLaVA-1.5保持模型结构，改进训练数据，最终仅用558K+665K数据就在12个benchmark上取得sota，用32张A100复现只需要十多个小时</font>**。而BLIP2的后续工作[InstructBLIP](https://zhida.zhihu.com/search?content_id=670965997&content_type=Answer&match_order=1&q=InstructBLIP&zhida_source=entity)则保持训练数据，改进模型结构，然而受限于当时的视野，其模型结构完全无法推广至多轮对话，直接被淘汰出局。因此从后续工作的角度来说，更倾向于选择基于LLaVA-1.5的setting继续做下去。
3. **更快的收敛速度**：Q-Former的参数量太大了（100+M），无法用这么少的数据量训出来。那么假设数据量足够，用Q-Former的上限是否会比MLP更高呢？答案也是否定的，强如Qwen-VL，使用大量数据训练后，并没有比LLaVA-1.5取得明显的性能提升。从这个角度来说，即便继续沿着BLIP的路线做，也略显困难了。

:::color5
**<font style="color:#601BDE;">3.其他可能原因：有损压缩？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">以</font>[BLIP2](https://zhida.zhihu.com/search?content_id=670965997&content_type=Answer&match_order=1&q=BLIP2&zhida_source=entity)<font style="color:rgb(51, 51, 51);">为例，</font>**<font style="color:#ED740C;">Q-Former会把任意长度的 visual token 序列转译成 32 个token</font>**<font style="color:rgb(51, 51, 51);">，可能导致其被MLP取代。</font>

<font style="color:rgb(51, 51, 51);">然而值得注意的是，</font>[Qwen-VL](https://zhida.zhihu.com/search?content_id=670965997&content_type=Answer&match_order=1&q=Qwen-VL&zhida_source=entity)<font style="color:rgb(51, 51, 51);">在类似的结构上将448分辨率的图像转译成 256 个token，减小了损失率，此时虽然仍然存在有损压缩的问题，但是</font>[InternVL-1.2](https://link.zhihu.com/?target=https%3A//internvl.github.io/blog/2024-02-21-InternVL-1.2/)<font style="color:rgb(51, 51, 51);"> 在同样的分辨率下，通过MLP+</font>[PixelShuffle](https://zhida.zhihu.com/search?content_id=670965997&content_type=Answer&match_order=1&q=PixelShuffle&zhida_source=entity)<font style="color:rgb(51, 51, 51);">的方案得到的 visual token 数量也是 256 个token。两个模型都取得了很强的性能。</font>**<font style="color:#74B602;">因此“有损压缩”的观点不足以解释Q-Former被放弃的原因。</font>**

:::color5
**<font style="color:#601BDE;">4.评估对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

在对比实验中，DeCo使用了完全相同的实验设置、相同的压缩比（576 image tokens -> 144 query tokens），相比原始的Q-former和增强后的locality-aware Q-former（即Honeybee中提出的C-Abstractor和D-Abstractor），DeCo的方法具有效率和表现上的优势。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741865278387-56d098bd-f29d-47cc-95da-86daf22d64b1.png)

:::color5
**<font style="color:#601BDE;">5.视频领域仍采用Q-Former</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(55, 58, 64);">这篇回答主要还是从图文对模型的角度来回答Q-Former为什么逐渐被MLP取代，</font>**<font style="color:#ED740C;">对于视频以及多图场景确实还是需要一些比较强的压缩方案。</font>**



# <font style="color:rgb(51, 51, 51);">CLIP：图文对比学习</font>
<font style="color:rgb(51, 51, 51);">以CLIP模型为例，从原理到代码实现系统解析多模态对比学习</font>

:::color3
**<font style="color:rgb(51, 51, 51);">核心思想：</font>**

<font style="color:rgb(51, 51, 51);">通过对比学习将不同模态（如图像-文本）映射到同一潜在空间，使匹配的样本对距离更近，不匹配的更远。CLIP的核心公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735486640-ffd361d0-724d-4b70-bb6f-25f479fe15cf.png)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735548727-251dbecf-fe08-4e85-a1ce-6509358d36bf.png)

:::color5
**<font style="color:#601BDE;">1.CLIP架构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">双编码器结构</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像编码器（ViT/ResNet）</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器（Transformer）</font>
2. **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：将不同模态的特征映射到同一空间</font>
3. **<font style="color:rgb(51, 51, 51);">对比目标</font>**<font style="color:rgb(51, 51, 51);">：最大化正样本对的相似度，最小化负样本对</font>

:::color5
**<font style="color:#601BDE;">2.训练步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据预处理</font>**
    - <font style="color:rgb(51, 51, 51);">图像：Resize到224x224，随机裁剪/翻转</font>
    - <font style="color:rgb(51, 51, 51);">文本：截断/填充到固定长度（CLIP使用76 tokens）</font>
2. **<font style="color:rgb(51, 51, 51);">特征提取</font>**

```python
# 伪代码示例
image_features = image_encoder(image_batch)  # [batch_size, emb_dim]
text_features = text_encoder(text_batch)     # [batch_size, emb_dim]
```

3. **<font style="color:rgb(51, 51, 51);">相似度矩阵计算</font>**

```python
# 归一化
image_emb = image_features / image_features.norm(dim=-1, keepdim=True)
text_emb = text_features / text_features.norm(dim=-1, keepdim=True)

# 计算相似度矩阵
logit_scale = nn.Parameter(torch.ones([]) * np.log(1/0.07))
logits_per_image = logit_scale * image_emb @ text_emb.t()  # [N, N]
logits_per_text = logits_per_image.t()                     # [N, N]
```

4. **<font style="color:rgb(51, 51, 51);">对比损失计算</font>**

<font style="color:rgb(51, 51, 51);">使用对称交叉熵损失：</font>

```python
labels = torch.arange(batch_size)  # 对角矩阵表示正样本对

loss_i = F.cross_entropy(logits_per_image, labels)
loss_t = F.cross_entropy(logits_per_text, labels)
total_loss = (loss_i + loss_t)/2
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点：</font>**

1. <font style="color:rgb(51, 51, 51);">零样本推理能力</font>
2. <font style="color:rgb(51, 51, 51);">跨模态检索高效</font>
3. <font style="color:rgb(51, 51, 51);">对噪声数据鲁棒性强</font>
4. <font style="color:rgb(51, 51, 51);">无需手工标注（利用自然监督信号）</font>

**<font style="color:rgb(51, 51, 51);">缺点：</font>**

1. <font style="color:rgb(51, 51, 51);">需要超大规模数据（CLIP训练用了4亿对）</font>
2. <font style="color:rgb(51, 51, 51);">模态间细粒度对齐困难</font>
3. <font style="color:rgb(51, 51, 51);">计算成本极高（CLIP训练需592 V100 days）</font>
4. <font style="color:rgb(51, 51, 51);">文本描述歧义性问题</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

| **场景** | **典型应用** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">零样本分类</font> | <font style="color:rgb(51, 51, 51);">ImageNet分类无需训练</font> |
| <font style="color:rgb(51, 51, 51);">跨模态检索</font> | <font style="color:rgb(51, 51, 51);">图文互搜（如Google Images）</font> |
| <font style="color:rgb(51, 51, 51);">生成模型引导</font> | <font style="color:rgb(51, 51, 51);">DALL-E、Stable Diffusion的文本条件生成</font> |
| <font style="color:rgb(51, 51, 51);">视频理解</font> | <font style="color:rgb(51, 51, 51);">视频-文本对齐（如VideoCLIP）</font> |
| <font style="color:rgb(51, 51, 51);">多模态推理</font> | <font style="color:rgb(51, 51, 51);">Visual Question Answering</font> |


:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **训练效率优化**：
    - <font style="color:rgb(51, 51, 51);">FLIP（随机mask图像块加速训练）</font>
    - <font style="color:rgb(51, 51, 51);">DeCLIP（数据增强+动量蒸馏）</font>
2. **对齐增强**：
    - <font style="color:rgb(51, 51, 51);">ALIGN：使用噪声更大的网页数据</font>
    - <font style="color:rgb(51, 51, 51);">FILIP：细粒度token级对比</font>
3. **架构改进**：
    - <font style="color:rgb(51, 51, 51);">BLIP：引入跨模态注意力</font>
    - <font style="color:rgb(51, 51, 51);">FLAVA：统一多模态编码器</font>
4. **损失函数改进**：
    - <font style="color:rgb(51, 51, 51);">CoOp：可学习的prompt模板</font>
    - <font style="color:rgb(51, 51, 51);">SLIP：结合自监督学习损失</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
# 典型CLIP训练配置
batch_size = 32768    # 需超大显存
learning_rate = 5e-5  # 使用学习率warmup
epochs = 32           # 实际需要更多epoch
temperature = 0.07    # logit缩放因子

import torch
import torch.nn as nn

class CLIP(nn.Module):
    def __init__(self, image_encoder, text_encoder, emb_dim=512):
        super().__init__()
        self.image_encoder = image_encoder
        self.text_encoder = text_encoder
        self.image_proj = nn.Linear(2048, emb_dim)  # ResNet50为例
        self.text_proj = nn.Linear(512, emb_dim)    # Transformer为例
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1/0.07))

    def forward(self, images, texts):
        # 特征提取
        image_feats = self.image_encoder(images)  # [bs, 2048]
        text_feats = self.text_encoder(texts)     # [bs, 512]
        
        # 投影到共同空间
        image_emb = self.image_proj(image_feats)
        text_emb = self.text_proj(text_feats)
        
        # 归一化
        image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)
        text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
        
        # 计算相似度
        logits = self.logit_scale.exp() * image_emb @ text_emb.t()
        return logits

# 训练伪代码
model = CLIP(image_encoder, text_encoder)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for images, texts in dataloader:
    logits = model(images, texts)
    labels = torch.arange(len(images))
    loss = F.cross_entropy(logits, labels) + F.cross_entropy(logits.t(), labels)
    loss.backward()
    optimizer.step()

```

# FG-CLIP：细粒度图文对齐
:::color3
<font style="color:rgb(26, 26, 26);">简介：360人工智能研究院最新图文跨模态模型</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">FG-CLIP</font>**<font style="color:rgb(26, 26, 26);">，</font>**<font style="color:#ED740C;">宣布以“长文本深度理解”和“细粒度视觉比对”双突破</font>**<font style="color:rgb(26, 26, 26);">，彻底解决了传统CLIP模型的“视觉近视”问题，能够精准识别局部细节。 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

<font style="color:rgb(26, 26, 26);">《</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">FG-CLIP: Fine-Grained Visual and Textual Alignment</font>**<font style="color:rgb(26, 26, 26);">》</font>

<font style="color:rgb(26, 26, 26);">代码：</font>[https://github.com/360CVGroup/FG-CLIP](https://github.com/360CVGroup/FG-CLIP)

<font style="color:rgb(26, 26, 26);">论文：</font>[https://www.arxiv.org/abs/2505.05071](https://www.arxiv.org/abs/2505.05071)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749030915965-a3db3af4-0752-4143-b6b3-1bbff23ca45a.png)

> FG-CLIP概述。CLS<sub>img</sub>表示视觉变换器（ViT）输出的图像类特征，而CLS<sub>text</sub>表示文本模型为多个输入总结的类特征，包括长标题、短标题、区域标题以及图像中特定区域的正面和负面描述。FG-CLIP的训练分为两个阶段：第一阶段利用全局级caption图像对实现初始细粒度对齐，**<font style="color:#74B602;">而第二阶段则用额外的区域级caption对其进行补充，包括详细的区域字幕和正/负区域描述，以进一步细化对齐</font>**。**<font style="color:#D22D8D;">（by草莓师姐）</font>**
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749031217003-64930ec6-9ed4-4664-98dc-19b0050e5013.png)

:::color5
**<font style="color:#601BDE;">1.CLIP的近视问题</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">具体怎么个说法？先来个视力大挑战：找一找右边的哪句话，正确描述了左边图像里的内容？</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749031081180-fef47950-7e9b-4cc3-8b4d-e01e0a85f552.png)

> <font style="color:rgb(26, 26, 26);">正确答案是：“A light brown wood stool（一个浅棕色的木凳子）”，注意看，这个木凳子位于画面的中央偏右，悄悄隐藏在狗狗的身后。</font>
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749031131597-0bacd6c7-42dd-4584-86df-60fa5b608bfa.png)

> <font style="color:rgb(26, 26, 26);">可以发现，4个常用模型——CLIP、EVACLIP、SIGLIP、FINE-CLIP基于左侧图片选出的最匹配的文本描述是：A blue dog with a white colored head。</font>
>

**CLIP的“视觉近视”问题：**<font style="color:rgb(26, 26, 26);">会因为对比损失倾向于拉近全局图像与文本的嵌入，而非局部区域的对齐，</font>**<font style="color:#117CEE;">削弱了细粒度特征学习。</font>**

**<font style="color:rgb(26, 26, 26);">FG-CLIP的细粒度对齐</font>**<font style="color:rgb(26, 26, 26);">：FG-CLIP精准命中了答案，实验结果显示，FG-CLIP在</font>**<font style="color:#74B602;">细粒度理解、开放词汇对象检测、长短文本图文检索以及通用多模态基准测试</font>**<font style="color:rgb(26, 26, 26);">等下游任务中均显著优于原始CLIP和其他最先进方法。在12个下游任务上，FG-CLIP相比现有模型在关键的长文本理解+细粒度比对上实现了大幅突破。</font>

## **<font style="color:rgb(0, 0, 0);">视觉语言模型面向的问题</font>**
:::color3
**<font style="color:rgb(26, 26, 26);">简介：</font>**<font style="color:rgb(26, 26, 26);">2021年，OpenAI发布CLIP图文跨模态模型，通过对比学习，首次实现了大规模图像-文本对齐，开启了多模态预训练大模型的新纪元。它通过对比图像与文本的嵌入空间，使模型能够完成零样本分类、图像检索等任务。</font>

:::

:::color5
**<font style="color:#601BDE;">1.CLIP的缺点分析</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849995591-667a0c79-beab-443f-931c-f351159cd7c4.png?x-oss-process=image%2Fformat%2Cwebp)

<font style="color:rgb(26, 26, 26);">CLIP与后面发展的模型，在实际应用中依然面临以下的制约：</font>

+ **<font style="color:rgb(26, 26, 26);">文本长度限制</font>**<font style="color:rgb(26, 26, 26);">：CLIP的文本编码器仅支持77个token，难以处理</font>**<font style="color:#117CEE;background-color:rgba(0, 0, 0, 0);">长文本的细节描述</font>**<font style="color:rgb(26, 26, 26);">（如“一只红色的陶瓷茶杯，杯口有轻微磨损”）。</font>
+ **<font style="color:rgb(26, 26, 26);">全局对齐的盲区</font>**<font style="color:rgb(26, 26, 26);">：CLIP将图像与文本整体对齐，忽略了</font>**<font style="color:#117CEE;background-color:rgba(0, 0, 0, 0);">局部区域的细粒度信息</font>**<font style="color:rgb(26, 26, 26);">（如茶杯的把手形状、杯身图案）。</font>
+ **<font style="color:rgb(26, 26, 26);">负样本的不足</font>**<font style="color:rgb(26, 26, 26);">：现有数据集中，负样本（不匹配的图像-文本对）多为粗略的类别错误，</font>**<font style="color:#117CEE;">缺乏对细微差异的区分能力。</font>**

:::color5
**<font style="color:#601BDE;">2.对长文本细节描述理解的重要性</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">提供丰富的背景信息与复杂查询能力</font>**<font style="color:rgb(26, 26, 26);">：长文本能够提供详细的背景信息，包括动</font>**<font style="color:#74B602;">作状态、对象属性及变化过程等，这对于全面理解事件至关重要</font>**<font style="color:rgb(26, 26, 26);">。相比短文本分析，长文本允许综合查找基于多个条件（如物体、人物特征）的信息，支持更加复杂的查询需求。这使得模型不仅能识别发生了什么，还能理解事件的全貌及其上下文。</font>
+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">支持跨模态深度语义匹配与融合能力</font>**<font style="color:rgb(26, 26, 26);">：跨模态模型需要在不同模态间建立有效的语义对应关系。长文本中的</font>**<font style="color:#74B602;">多层次语义信息（如主题、段落、句子乃至词汇层面的意义）</font>**<font style="color:rgb(26, 26, 26);">可以帮助模型更精确地进行语义匹配和特征融合。</font>

<font style="color:rgb(26, 26, 26);">在图文检索任务中，长文本描述可以涵盖从全局场景到局部细节的全面信息，使得模型能够在多个层次上与图像特征进行比对和匹配，从而提升检索的准确性和相关性。</font>

:::color5
**<font style="color:#601BDE;">3.对局部区域细粒度信息进行准确分析的重要性</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">细节捕捉</font>**<font style="color:rgb(26, 26, 26);">：局部图像特征往往包含了区分不同对象的关键信息。例如，在对不同人物进行分析时，</font>**<font style="color:#74B602;">着装、动作等属性差别对于区分个体至关重要</font>**<font style="color:rgb(26, 26, 26);">。准确分析这些局部特征可以显著提高识别系统的准确性。</font>
+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">复杂环境适应性</font>**<font style="color:rgb(26, 26, 26);">：在复杂的背景或低质量图像中，局部特征可以帮助算法聚焦于最重要的信息，忽略干扰因素。在实际应用中，目标对象经常会被其他物体部分遮挡。在这种情况下，全局特征可能不足以描述对象，而局部特征则显得尤为重要。通过对局部特征的精确分析，</font>**<font style="color:#74B602;">系统能够有效地识别出未被遮挡的部分，并利用这些信息来推断整个对象的状态。</font>**
+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">局部图像特征属性的准确分析</font>**<font style="color:rgb(26, 26, 26);">：在提升识别精度、增强环境理解、支持高级别应用、改进用户体验以及保障安全性等方面具有核心重要性。通过精确解析这些细节信息，可以实现更智能、更可靠的系统性能，无论是在监控、自动驾驶、产品质量控制还是其他需要细致图像分析的领域中，都能发挥关键作用。</font>

:::color5
**<font style="color:#601BDE;">4.对图像/文本的细微差异实现准确理解的重要性</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">增强模型的鲁棒性和泛化能力</font>**<font style="color:rgb(26, 26, 26);">：准确区分图像和文本中的细微差别对于增强模型的鲁棒性和泛化能力至关重要。细粒度的理解使模型能够区分在视觉或语义上相似但存在细微差异的对象、场景或概念。这种能力对于现实世界的应用非常重要，因为在不同的光照、角度或背景下，对象可能会有细微的变化。确保模型能够在各种复杂场景中可靠运行。</font>
+ **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">提升下游任务的精度</font>**<font style="color:rgb(26, 26, 26);">：精确识别细微差异对提高下游任务（如图像描述生成、视觉问答和医学影像诊断）的准确性至关重要。例如，在视觉问答中，识别图像中的微小细节并理解其与问题的相关性是正确回答问题的关键。能否准确捕捉图像中的细微差异直接影响到系统的性能和用户体验。同样，在自然语言处理中，识别文本中的细微差异可以显著提高情感分析和信息检索等任务的表现。</font>

## **<font style="color:rgb(0, 0, 0);">模型方法</font>**
:::color3
**<font style="color:rgb(26, 26, 26);">简介：</font>**<font style="color:rgb(26, 26, 26);">FG-CLIP在传统双编码器架构基础上采用</font>**<font style="color:#ED740C;">两阶段训练策略</font>**<font style="color:rgb(26, 26, 26);">，有效提升了视觉语言模型的细粒度理解能力。 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

1. <font style="color:rgb(26, 26, 26);">一阶段：通过全局对比学习实现图文表征的初步对齐。</font>
2. <font style="color:rgb(26, 26, 26);">二阶段：引入</font>**<font style="color:#ED740C;">区域对比学习与难细粒度负样本学习</font>**<font style="color:rgb(26, 26, 26);">，利用区域-文本标注数据深化模型对视觉细节的感知能力，从而在保持全局语义理解的同时实现了对局部特征的精准捕捉。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749030915965-a3db3af4-0752-4143-b6b3-1bbff23ca45a.png)

:::color5
**<font style="color:#601BDE;">1.全局对比学习</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

**<font style="color:rgb(26, 26, 26);">全局对比学习：</font>**<font style="color:rgb(26, 26, 26);">通过整合多模态大模型生成的长描述，显著增强了模型的细粒度理解能力。这种方法不仅生成了内容丰富的长描述，还提供了更完整的上下文信息和更精准的细节描述。</font>

+ <font style="color:rgb(26, 26, 26);">引入长描述，模型得以在全局层面感知和匹配语义细节，从而大幅提升了其上下文理解能力。</font>
+ <font style="color:rgb(26, 26, 26);">保留了原有的短描述-图像对齐机制，使长短描述形成互补。</font>

<font style="color:rgb(26, 26, 26);">这种双轨并行的策略使模型既能从长描述中获取复杂的语义信息，又能从短描述中把握核心概念，从而全面提升了模型对视觉信息的理解和处理能力。</font>

:::color5
**<font style="color:#601BDE;">2.局部对比学习</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

**<font style="color:rgb(26, 26, 26);">局部对比学习：</font>**<font style="color:rgb(26, 26, 26);">通过精准对齐图像局部区域与对应文本描述，实现细粒度的视觉-语言关联。</font>

+ <font style="color:rgb(26, 26, 26);">具体而言，FG-CLIP首先运用</font>**<font style="color:#74B602;">RoIAlign从图像中精确提取区域特征，继而对每个检测区域施加平均池化操作，获取一组富有代表性的区域级视觉表征。</font>**
+ <font style="color:rgb(26, 26, 26);">这些局部特征随后与预先构建的细粒度文本描述进行对比学习，促使模型建立区域视觉内容与文本语义之间的精确映射关系，从而掌握更为细致的跨模态对齐能力。</font>

:::color5
**<font style="color:#601BDE;">3.区域级难负样本对比学习</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">针对细粒度负样本稀缺这一挑战，FG-CLIP提出了一种难细粒度负样本学习方法。</font>

**<font style="color:rgb(26, 26, 26);">难细粒度负样本学习方法：</font>**<font style="color:rgb(26, 26, 26);">FG-CLIP将</font>**<font style="color:#74B602;">语义相近但与正样本存在细微差异的样本定义为难负样本</font>**<font style="color:rgb(26, 26, 26);">，并通过对边界框描述进行属性层面的微调和重写来构建这些样本。为了充分利用难细粒度负样本提供的判别信息，FG-CLIP在损失函数中引入了特定的细粒度负样本学习策略。在训练过程中，模型需要同时计算区域特征与正样本描述及其对应负样本描述之间的相似度，从而学习更精细的视觉-语言对齐关系。</font>

## **<font style="color:rgb(0, 0, 0);">数据构建</font>**
:::color5
**<font style="color:#601BDE;">1.通过LMM进行详细的图像描述重写</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">在初始训练阶段，FG-CLIP采用了经过增强优化的LAION-2B数据集，其中的图像标注经由CogVLM2-19B重新生成。这种改进显著提升了数据质量，使描述更加精确和内容丰富。</font>

+ **<font style="color:rgb(26, 26, 26);">传统LAION-2B数据集</font>**<font style="color:rgb(26, 26, 26);">：往往采用笼统的描述方式，难以支持精细化任务的需求。</font>
+ **<font style="color:rgb(26, 26, 26);">数据集重写</font>**<font style="color:rgb(26, 26, 26);">：通过引入先进的多模态大模型，FG-CLIP生成的描述不仅准确识别目标对象，还涵盖了对象特征、行为模式及场景关联等多维信息。</font>

:::color1
**<font style="color:rgb(26, 26, 26);">LAION-2B原始描述</font>**

一只鸟

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032236034-910c33a5-62b4-4e43-b5d8-1dd255c6ba6a.png)

:::

:::color1
**重写后描述**

一只黄鹂鸟栖息在的树叶茂密的树枝上。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032238033-42413935-7489-45bf-950f-ca8c14c5e926.png)

:::



<font style="color:rgb(26, 26, 26);">借助160×910B规模的NPU计算集群，FG-CLIP在30天内完成了全部数据处理工作。实验结果显示，这种优化显著提升了模型在多个任务上的表现，充分证明了</font>**<font style="color:#ED740C;">高质量文本标注对提升模型精确度和语境理解能力的关键作用</font>**<font style="color:rgb(26, 26, 26);">。</font>

:::color5
**<font style="color:#601BDE;">2.创建高质量的视觉定位数据</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">对于训练的第二阶段，FG-CLIP开发了一个高质量的视觉定位数据集，包含精确的区域特定描述和具有挑战性的细粒度负样本。FG-CLIP根据GRIT提供的图像来制作整个数据集。</font>

1. <font style="color:rgb(26, 26, 26);">首先使用CogVLM2-19B</font>**<font style="color:#74B602;">生成详细的图像描述</font>**<font style="color:rgb(26, 26, 26);">，确保描述全面且细腻，能够捕捉每张图像的全部背景信息。</font>
2. <font style="color:rgb(26, 26, 26);">随后，FG-CLIP使用SpaCy解析这些描述并提取出指代表达。</font>
3. <font style="color:rgb(26, 26, 26);">接着，</font>**<font style="color:#74B602;">将图像和指代表达输入预训练的开放词汇检测模型</font>**<font style="color:rgb(26, 26, 26);">，这里采用Yolo-World，以获得相应的边界框。</font>
4. <font style="color:rgb(26, 26, 26);">通过非极大值抑制消除重叠的边界框，仅保留预测置信度得分高于0.4的边界框。</font>

<font style="color:rgb(26, 26, 26);">这一过程产生了1200万张图像和4000万个带有精细区域描述的边界框。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032331673-c3c36c2a-bc94-426e-8a02-b636fd75c7a5.png)

:::color5
**<font style="color:#601BDE;">3.视觉定位数据规模</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">为生成高质量的细粒度负样本，FG-CLIP在维持对象名称不变的前提下，对边界框描述的属性进行精细调整。</font>

+ <font style="color:rgb(26, 26, 26);">FG-CLIP借助Llama-3.1-70B大语言模型，为每个正样本构建10个对应的负样本。</font>
+ <font style="color:rgb(26, 26, 26);">为提升描述的可读性，FG-CLIP移除了分号、逗号和换行符等标点符号。</font>

<font style="color:rgb(26, 26, 26);">经过对3,000个负样本的质量评估，98.9%的样本达到预期标准，仅1.1%被判定为噪声数据，这一比例符合无监督方法的可接受范围。这种方法产生的细微变化更贴近现实场景，能够更好地模拟物体在保持基本类目相似的同时，具体细节存在差异的情况。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032416224-05e32444-c636-4149-9080-344fc2dcf2d1.png)

<font style="color:rgb(26, 26, 26);">这项大规模数据集由1200万张高质量图像构成，每张图像都配备精确的语义描述。其中包含4000万个边界框标注，每个边界框都附带详尽的区域描述，同时还整合了1000万个经过筛选的难细粒度负样本。</font>

<font style="color:rgb(26, 26, 26);">数据处理阶段调用了160×910B算力的NPU集群，历时7天高效完成。这套丰富而系统的数据集显著提升了模型识别精细特征的能力，为FG-CLIP的训练奠定了扎实基础，使其在视觉与文本特征的细粒度理解方面表现卓越。</font>

## **<font style="color:rgb(0, 0, 0);">实验效果-量化指标</font>**
:::color5
**<font style="color:#601BDE;">1.细粒度识别</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">FG-CLIP基于FG-OVD数据集对开源图像-文本对齐模型进行了系统评估。与MSCOCO和Flickr等聚焦整体匹配的传统基准不同，FG-OVD专注于考察模型识别和定位图像局部区域的精细化能力。</font>

+ <font style="color:rgb(26, 26, 26);">在评估过程中，每个</font>**<font style="color:#74B602;">目标区域都配备了一个精准描述和十个经过精心设计的负向样本</font>**<font style="color:rgb(26, 26, 26);">，这些负向样本通过对正确描述的策略性修改而生成。</font>
+ <font style="color:rgb(26, 26, 26);">FG-OVD数据集划分为</font>**<font style="color:#74B602;">四个难度递进的子集</font>**<font style="color:rgb(26, 26, 26);">，其区分度主要体现在待匹配文本之间的相似程度上。</font>
+ <font style="color:rgb(26, 26, 26);">具体而言，hard、medium和easy子集分别通过替换一个、两个和三个属性词来构造负样本，而trivial子集则采用完全无关的文本描述，形成了一个从细微差别到显著差异的评估体系。</font>

<font style="color:rgb(26, 26, 26);">由表中可以看到，FG-CLIP相对于其他方法，在各项指标上都能获得显著提升，这也证明了该方法在细粒度理解上的能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032506525-a4e7f7ef-8b95-40dd-8519-6053dffb0d92.png)

:::color5
**<font style="color:#601BDE;">2.区域识别</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">FG-CLIP在COCO-val2017数据集上开展零样本测试，评估模型识别局部信息的能力，测试方案参照FineCLIP和CLIPSelf。这项评估着重考察模型仅依靠文本描述对边界框内目标进行分类的表现。</font>

+ <font style="color:rgb(26, 26, 26);">具体实现中，FG-CLIP利用数据集中的边界框标注，结合ROIAlign技术提取局部区域的密集特征表示。</font>
+ <font style="color:rgb(26, 26, 26);">在测试阶段，将所有类别标签作为候选文本输入，对每个边界框区域进行匹配和分类，并通过Top-1和Top-5准确率进行性能评估。FG-CLIP同样在这个下游任务上取得了最好的结果。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032522798-c2e49ebe-b897-4ae3-9284-9d7a5ce872de.png)

:::color5
**<font style="color:#601BDE;">3.开放词汇目标检测</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">为了进一步评估FG-CLIP的方法的细粒度定位能力，FG-CLIP被采用作为下游开放词汇检测任务的Backbone。具体来说，FG-CLIP采用了一个两阶段检测架构F-VIT，并在训练中冻结了视觉编码器。从表格中可以看出，FG-CLIP在开放词汇目标检测任务上表现更加突出，证明了经过高质量数据和优化方法训练的模型能够在更深层次的任务上取得优越的性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032561537-2b411103-5668-4445-9536-7964b41d9cae.png)

:::color5
**<font style="color:#601BDE;">4.图文检索/分类结果</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">为了全面评估图像力度的任务，FG-CLIP对长标题和短标题图像文本检索任务以及零样本图像分类任务进行了实验。如表所示，FG-CLIP在长/短标题图像-文本检索任务中都取得了显著的性能提升。与旨在提高细粒度识别能力的 Long-CLIP 和 FineCLIP 相比，FG-CLIP在图像分类这种短文本-全图问题上的准确率方面具有明显优势。该模型处理不同图像描述长度的能力突出了其在多模态匹配中的通用性和鲁棒性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749032589491-02c1fc92-789a-4eb5-b9f2-d46d4542d3fc.png)

## **<font style="color:rgb(0, 0, 0);">实验效果-可视化对比</font>**
:::color5
**<font style="color:#601BDE;">1.图像细节差异效果对比</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">FG-CLIP针对文本输入对图像特征进行了可视化。图中，暖色调（如黄色）表示相关性较高，而冷色调（如蓝色）表示相关性较低。首先是针对相同的输入文本和图像，对不同模型的ViT特征进行比较，可以发现FG-CLIP在这种细粒度理解问题上表现更好。如图中的第二行所示，当输入“Black nose”时，FG-CLIP可以对该小目标实现准确的识别。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749030462511-0644d422-dd12-4a01-84ca-dae4b4583a80.png)

:::color5
**<font style="color:#601BDE;">2.在不同输入文本下的可视化图</font>**<font style="color:rgb(26, 26, 26);"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">FG-CLIP同样将不同的输入文本和相同图片做相关性分析。可以发现，</font>**<font style="color:#74B602;">对于图像中的不同目标，FG-CLIP都能给出准确的位置理解</font>**<font style="color:rgb(26, 26, 26);">，这表明了该模型具有稳定的视觉定位和细粒度理解能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749030462671-a6ddc8d6-6270-47d9-be6e-e81a95c7c556.png)

## **<font style="color:rgb(0, 0, 0);">总结</font>**
:::color3
**<font style="color:rgb(26, 26, 26);">简介：</font>**<font style="color:rgb(26, 26, 26);">FG-CLIP在细粒度视觉理解领域取得了突破性进展。该模型创新性地整合了前沿图文对齐技术，并基于大规模精选数据集和难细粒度负样本学习策略，实现了对图像的多层次语义解析。其独特优势在于能同时把握全局语境和局部细节，精准识别和区分细微特征差异。大量实验结果表明，FG-CLIP在各类下游任务中均展现出优异表现。 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgb(26, 26, 26);">为推动领域发展，研究团队决定将FG-CLIP相关的数据、代码和预训练模型陆续进行开源，相关内容将在360人工智能研究院的主页和GitHub发布。未来研究团队的研究方向将聚焦于融合更先进的多模态架构，以及构建更丰富多元的训练数据集，以进一步拓展细粒度视觉理解的技术边界。</font>

# Q-Former<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**BLIP2通过创新的**<font style="color:#74B602;">两阶段训练和Q-Former设计</font>**，实现了高效的多模态对齐，成为视觉语言任务的新基准。未来可通过动态查询机制和混合微调策略进一步提升性能。

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741864398461-bcb86f8c-ee5a-4a7d-8771-bc77b48b662c.png)

**代表模型**：BLIP2,Instruct-BLIP,Qwen-VL

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**Q-Former**：<font style="color:rgb(25, 27, 31);">核心是拿一组</font>**<font style="color:#ECAA04;">预定义好的、可学的、固定数量（M个）的Query tokens</font>**<font style="color:rgb(25, 27, 31);">，通过cross attention层去</font>**<font style="color:#74B602;">融合来自image encoder的image token信息</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ <font style="color:rgb(51, 51, 51);">输入：可学习查询向量 Q∈R</font><sup><font style="color:rgb(51, 51, 51);">Nq×d</font></sup><font style="color:rgb(51, 51, 51);">，Nq为查询数）。</font>
+ <font style="color:rgb(51, 51, 51);">结构：</font>
    - **<font style="color:rgb(51, 51, 51);">图像-查询交叉注意力</font>**<font style="color:rgb(51, 51, 51);">：Q</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">与Zv交互。</font>
    - **<font style="color:rgb(51, 51, 51);">文本-查询自注意力</font>**<font style="color:rgb(51, 51, 51);">：将文本标记与Q</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">拼接后通过自注意力层。</font>
+ <font style="color:rgb(51, 51, 51);">输出：与文本对齐的视觉特征 Zq∈R</font><sup><font style="color:rgb(51, 51, 51);">Nq×d</font></sup><font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">2.Q-Former学到了什么？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#74B602;">Q-Former学到了什么：</font>**<font style="color:rgb(51, 51, 51);">可视化了MLLM中Q-former训练后的输出，验证了</font>**<font style="color:#ED740C;">Q-former确实是在视觉语义级别的压缩</font>**<font style="color:rgb(51, 51, 51);">。下图可视化了MLLM中训练好的Q-former的输出，高亮了每个query token相对于原始图片patch的相关性矩阵。我们可以看到，</font>**<font style="color:#ED740C;">将576 image tokens压缩成64 query tokens，每个query token在负责不同的visual concepts，包括不同的objects、attributes和background等等</font>**<font style="color:rgb(51, 51, 51);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741864585512-f1209667-aa4c-4ef0-a0d4-ded42d069dc1.png)

:::color5
**<font style="color:#601BDE;">3.Q-Former的缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **作为一个视觉语义提取器，Q-former是很难学好的**。

和它的参数量没有直接的关系，比如只用2层的轻量Q-former，也非常难学好。例如，我们的实验中把LLaVA那套框架，完全相同的模型、数据、训练配置，把MLP换成轻量的2层Q-former（且用BLIP-2的参数初始化），实验结果依然下降非常夸张。**<font style="color:#ED740C;">我们猜测是LLaVA使用的558K+665K量级的数据不足以把Qformer学好</font>**。

1. **由于不好学，Q-former很容易成为MLLM中的一个bottleneck，丢失重要的视觉信息。**

比如通过上面可视化的64个query tokens，query tokens学到的视觉concepts可能是：

**1）稀疏的**，只包含了有限的视觉concepts，

**2）重复的**，不同的query tokens表达了重复的视觉concepts，比如下面红色框和绿色框的query tokens是重复的。

**3）**[Honeybee](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2312.06742)这篇工作还指出原始的Q-former结构**会丢失图片的空间位置信息**，等等。Q-former中视觉信息的损失，会传递到LLM，是不可逆的。

  


# MLP<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">通过轻量级MLP将图像特征（如</font>`<font style="color:rgb(51, 51, 51);">256×1024</font>`<font style="color:rgb(51, 51, 51);">）转换为与文本嵌入相同维度的序列（</font>`<font style="color:rgb(51, 51, 51);">N×4096</font>`<font style="color:rgb(51, 51, 51);">），作为“视觉token”插入文本输入前。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921026487-0ac29916-c8af-468a-ae51-0cf15aad5d3f.png)

**代表模型：LLAVA，Qwen2-VL, Qwen2.5-VL**

:::color5
**<font style="color:#601BDE;">1.LLAVA中的MLP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(51, 51, 51);">特征投影与空间对齐</font>**
    - **<font style="color:rgb(51, 51, 51);">视觉特征投影</font>**<font style="color:rgb(51, 51, 51);">：通过轻量级MLP将图像特征（如</font>`<font style="color:rgb(51, 51, 51);">256×1024</font>`<font style="color:rgb(51, 51, 51);">）转换为与文本嵌入相同维度的序列（</font>`<font style="color:rgb(51, 51, 51);">N×4096</font>`<font style="color:rgb(51, 51, 51);">），作为“视觉token”插入文本输入前。</font>
    - **<font style="color:rgb(51, 51, 51);">跨模态注意力</font>**<font style="color:rgb(51, 51, 51);">：语言模型通过自注意力机制，动态融合视觉token与文本token的语义信息，实现模态间交互。</font>
2. **<font style="color:rgb(51, 51, 51);">两阶段训练策略</font>**
    - **<font style="color:rgb(51, 51, 51);">阶段一：特征对齐预训练</font>**
        * **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：固定视觉编码器和LLM参数，仅训练投影层。</font>
        * **<font style="color:rgb(51, 51, 51);">数据</font>**<font style="color:rgb(51, 51, 51);">：使用图像-文本对（如CC3M、SBU），构造简单指令（如“描述这张图”）。</font>
        * **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：文本生成的标准交叉熵损失（仅计算文本部分）。</font>
    - **<font style="color:rgb(51, 51, 51);">阶段二：端到端指令微调</font>**
        * **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：联合优化投影层和LLM参数（可选择性微调视觉编码器）。</font>
        * **<font style="color:rgb(51, 51, 51);">数据</font>**<font style="color:rgb(51, 51, 51);">：人工构建的多模态指令数据（如视觉推理、复杂QA），格式为</font>`<font style="color:rgb(51, 51, 51);">(图像, 指令, 答案)</font>`<font style="color:rgb(51, 51, 51);">。</font>
        * **<font style="color:rgb(51, 51, 51);">任务设计</font>**<font style="color:rgb(51, 51, 51);">：覆盖描述生成、推理、对话等任务，增强多模态泛化能力。</font>

:::color5
**<font style="color:#601BDE;">1.MLP没有视觉信息损失</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ 训练资源够的条件下（足够的GPU），一定会选择简洁高效的MLP，**<font style="color:#ED740C;">毕竟没有视觉信息损失、训练收敛快、表现也好</font>**，这一方面其他答主已经讨论很多了。唯一的问题（即会导致图片token序列很长）在钞能力面前是可以忽略的，我想这也是现在不差卡的大公司或者大组选择MLP的原因。
+ 我们想重点表达的是，**训练资源有限的情况下（有限的GPU、训练数据等），Q-former也只是一个“低效”压缩器**。**如果想减少图片token数量来降低训练代价，简单的AdaptiveAveragePooling就够了**。

:::color5
**<font style="color:#601BDE;">2.对齐后，LLM本身就是一个视觉语义提取器</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

在DeCo工作中，我们解耦了MLLM中图文模态之间的语义对齐流，如下图。我们发现**经过多模态对齐后，LLM本身就是一个很好的视觉语义提取器**。本质上，**<font style="color:#ED740C;">线性层或者MLP层映射后得到的还是patch级别的视觉特征、不是语义级别的</font>**，现在LLaVA路线强大的模型表现也证实了LLM能很好地提取视觉语义来生成文本回答。	

:::color5
**<font style="color:#601BDE;">4.Qwen2-VL中的MLP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL采用了一种更简单的压缩方法：对</font>**<font style="color:#74B602;">空间位置临近的patch 特征做拼接，再经过2层MLP线性变换</font>**<font style="color:rgb(25, 27, 31);">，这样将原来长度为 </font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);"> 的序列，可压缩到 </font><font style="color:rgb(25, 27, 31);">n/4</font><font style="color:rgb(25, 27, 31);"> ，最终将压缩后的特征序列输入给LLM模型。处理过程如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742278493947-67adfde1-1e94-48d0-8b71-8cde17fd7ad8.png)

**<font style="color:rgb(25, 27, 31);">Vision token</font>**

<font style="color:rgb(25, 27, 31);">为了区分Vision token和文本token，Qwen2-VL也引入了两个特殊的token </font><font style="color:rgb(25, 27, 31);"><|vision_start|></font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);"><|vision_end|></font><font style="color:rgb(25, 27, 31);"> 来标识Vision token。</font>

```python
对于一个 224x224 ，如果ViT的 patch_size = 14 ，最终将图片编码成一个66个token的序列输入到模型。
具体计算过程：
1.Patch 处理后的Token数为： (224/14) x (224/14) = 16x16 = 256
2.经过输入投影层压缩处理： 256/4 = 64
3. 最后再加上 2 个起止位置的特殊token： 64+2 = 66

```

**为什么不用Q-Former？**

<font style="color:rgb(25, 27, 31);">主要是因为Cross-Attention架构适合处理</font>**<font style="color:#74B602;">固定长度的 </font>****<font style="color:#74B602;">k,v</font>****<font style="color:#74B602;"> </font>**<font style="color:rgb(25, 27, 31);">，当 </font><font style="color:rgb(25, 27, 31);">k,v</font><font style="color:rgb(25, 27, 31);"> 长短不一时，是不适合做Attention计算的。而Qwen2-VL通过原生动态分辨率方法处理的每个图片的token序列恰恰是变长的，无法使用Cross-Attention架构做特征压缩处理。</font>



# Cross Attention<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Cross Attention 是 Transformer 模型中注意力机制的一种扩展，</font>**<font style="color:#ED740C;">主要用于处理两个不同的序列之间的关系</font>**<font style="color:rgb(51, 51, 51);">。与传统的 Self Attention 不同，Cross Attention 不仅关注单个序列内部的信息，还可以利用另一个序列的信息来增强当前序列的表示。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921788090-01e85ef0-c92e-41f6-b93a-6f3ad1871510.png)

:::color5
**<font style="color:#601BDE;">0.Self Attention 对比 Cross Attention</font>**

:::

:::success
**Self Attention**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741922076585-804ee296-2b2c-4df4-ba89-d2aa486f72ce.png)

:::

:::success
**Cross Attention**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741921968328-4a18d583-5187-45df-955f-a1e3f4f3b80b.png)

:::

| **<font style="color:rgb(79, 79, 79);">维度</font>** | **<font style="color:rgb(79, 79, 79);">Self Attention</font>** | **<font style="color:rgb(79, 79, 79);">Cross Attention</font>** |
| --- | --- | --- |
| **<font style="color:rgb(79, 79, 79);">输入来源</font>** | <font style="color:rgb(79, 79, 79);">同一序列内的元素（Query、Key、Value）</font> | <font style="color:rgb(79, 79, 79);">不同序列中的元素（Query、Key、Value 不同来源）</font> |
| **<font style="color:rgb(79, 79, 79);">信息交互对象</font>** | <font style="color:rgb(79, 79, 79);">序列中的各个元素相互关注</font> | <font style="color:rgb(79, 79, 79);">序列 A 的元素关注序列 B 中的元素</font> |
| **<font style="color:rgb(79, 79, 79);">应用场景</font>** | <font style="color:rgb(79, 79, 79);">序列内部依赖建模，如句子中的词与词的关联</font> | <font style="color:rgb(79, 79, 79);">跨序列信息建模，如文本到图像、编码器到解码器</font> |
| **<font style="color:rgb(79, 79, 79);">特征捕捉</font>** | <font style="color:rgb(79, 79, 79);">捕捉序列内部的全局依赖</font> | <font style="color:rgb(79, 79, 79);">捕捉不同序列之间的全局依赖</font> |


:::color5
**<font style="color:#601BDE;">1.核心原理</font>**

:::

+ **工作原理：**在 Cross Attention 中，**<font style="color:#74B602;">查询（Query）来自一个序列，而键（Key）和值（Value）来自另一个不同的序列</font>**。这种机制允许模型将一个序列中的信息与另一个序列中的信息进行匹配和关联，**<font style="color:#ED740C;">从而在两个不同的表示之间建立相关性。</font>**
+ **作用：**Cross Attention 主要用于跨模态、跨序列的依赖关系建模。例如，**<font style="color:#ED740C;">在图像和文本匹配任务中，文本的查询可以与图像中的特征进行匹配，从而找到相关的图像区域。</font>**
+ **主要特点：**
    - 信息来源：两个不同序列之间的信息交互，查询来自一个序列，而键和值来自另一个序列。
    - 应用场景：广泛用于需要**<font style="color:#74B602;">跨序列依赖的任务</font>**，例如在 Transformer 解码器中，通过 Cross Attention 机制，解码器的查询会与编码器生成的隐藏状态（作为键和值）进行交互，从而解码生成下一个词语。

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

<font style="color:rgb(25, 27, 31);">在多模态结构中，我们可能</font>**<font style="color:#74B602;">有两个(或多个)</font>**[**<font style="color:#74B602;">Embeddings序列</font>**](https://zhida.zhihu.com/search?content_id=244116480&content_type=Article&match_order=1&q=Embeddings%E5%BA%8F%E5%88%97&zhida_source=entity)**<font style="color:#74B602;"> </font>****<font style="color:#74B602;">S1</font>****<font style="color:#74B602;"> 和 </font>****<font style="color:#74B602;">S2</font>****<font style="color:#74B602;"> 。我们将 </font>****<font style="color:#74B602;">S1</font>****<font style="color:#74B602;"> 作为attention的K,V，将 </font>****<font style="color:#74B602;">S2</font>****<font style="color:#74B602;"> 作为attention的Q。使用Q与K计算注意力权重矩阵，并与V相乘</font>**<font style="color:rgb(25, 27, 31);">，得到：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741922041726-2e85122d-4cec-4ca6-b466-c4cd5986ee08.png)

<font style="color:rgb(51, 51, 51);">具体来说，Cross Attention 的计算过程包括以下几个步骤：</font>

1. **Query、Key 和 Value 的生成**：
    - <font style="color:rgb(51, 51, 51);">对于序列 A，生成 Query（A_q）。</font>
    - <font style="color:rgb(51, 51, 51);">对于序列 B，生成 Key（B_k）和 Value（B_v）。</font>
2. **计算注意力分数**：
    - <font style="color:rgb(51, 51, 51);">使用 Query 和 Key 的点积来计算注意力分数（score）。</font>

```plain
scores = torch.bmm(A_q, B_k.permute(0, 2, 1))
```

3. **归一化**：
    - <font style="color:rgb(51, 51, 51);">对注意力分数进行 Softmax 操作，将其转换为概率分布。</font>

```plain
attention = F.softmax(scores, dim=-1)
```

4. **加权和**：
    - <font style="color:rgb(51, 51, 51);">将注意力权重与序列 B 的 Value 向量进行加权求和，生成最终的输出表示。</font>

```plain
output = torch.bmm(attention, B_v)
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

1. **增强语义理解**：
    - <font style="color:rgb(51, 51, 51);">Cross Attention 通过整合两个序列的信息，能够更全面地理解输入数据，提升语义理解和生成能力。</font>
2. **跨模态信息融合**：
    - <font style="color:rgb(51, 51, 51);">在多模态任务中，Cross Attention 可以有效地整合图像、文本等多种模态的信息，提升模型的表现。</font>
3. **提高任务准确性**：
    - <font style="color:rgb(51, 51, 51);">通过参考另一个序列的信息，Cross Attention 可以在许多任务中提高预测的准确性，如机器翻译和对话生成。</font>
4. **灵活性高**：
    - <font style="color:rgb(51, 51, 51);">Cross Attention 的应用非常广泛，可以用于多种序列处理任务，具有较高的灵活性。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

1. **计算复杂度高**：
    - <font style="color:rgb(51, 51, 51);">与 Self Attention 相比，Cross Attention 的计算量更大，尤其是在处理长序列时，会导致计算资源的消耗增加。</font>
2. **注意力分配问题**：
    - <font style="color:rgb(51, 51, 51);">在某些情况下，模型可能会过度依赖另一个序列的信息，导致注意力分配不均衡，影响自身的特征提取能力。</font>
3. **潜在的信息泄漏**：
    - <font style="color:rgb(51, 51, 51);">在处理某些任务时，Cross Attention 可能会导致信息泄漏，尤其是在需要保护数据隐私的场景中。</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

1. **机器翻译**：
    - <font style="color:rgb(51, 51, 51);">在多语言翻译任务中，Cross Attention 可以利用源语言和目标语言之间的关系，提升翻译质量。</font>
2. **对话生成**：
    - <font style="color:rgb(51, 51, 51);">Cross Attention 可以结合对话历史和当前输入，生成更连贯和相关的回复。</font>
3. **多模态任务**：
    - <font style="color:rgb(51, 51, 51);">在图像描述生成、视频内容理解等任务中，Cross Attention 可以整合视觉和文本信息，提升模型的表现。</font>
4. **文本摘要**：
    - <font style="color:rgb(51, 51, 51);">通过参考外部文献或上下文信息，Cross Attention 可以生成更为全面和准确的摘要。</font>

:::color5
**<font style="color:#601BDE;">5.使用CrossAttention的模型</font>**

:::

1. **T5（Text-to-Text Transfer Transformer）**：
    - <font style="color:rgb(51, 51, 51);">T5 是一种基于 Transformer 的预训练模型，广泛使用 Cross Attention 来处理源文本和目标文本之间的关系，提升文本生成能力。</font>
2. **VisualBERT**：
    - <font style="color:rgb(51, 51, 51);">VisualBERT 是一种用于视觉-语言任务的模型，利用 Cross Attention 整合图像和文本特征，提升图像描述和问答任务的表现。</font>
3. **DALL·E**：
    - <font style="color:rgb(51, 51, 51);">DALL·E 是一个生成文本描述的图像模型，通过 Cross Attention 机制，将文本和图像特征结合起来，生成与文本描述匹配的图像。</font>

:::color5
**<font style="color:#601BDE;">6.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CrossAttention(nn.Module):
    def __init__(self, embed_dim):
        super(CrossAttention, self).__init__()
        self.embed_dim = embed_dim
        self.query_net = nn.Linear(embed_dim, embed_dim)
        self.key_net = nn.Linear(embed_dim, embed_dim)
        self.value_net = nn.Linear(embed_dim, embed_dim)

    def forward(self, query, key, value):
        """
        Args:
            query: (batch_size, seq_len_q, embed_dim)
            key: (batch_size, seq_len_k, embed_dim)
            value: (batch_size, seq_len_k, embed_dim)
        Returns:
            output: (batch_size, seq_len_q, embed_dim)
        """
        # 单词嵌入维度可能不一样，这里假设已经处理一致
        batch_size, seq_len_q, embed_dim = query.size()
        _, seq_len_k, embed_dim = key.size()

        # 线性变换
        A_q = self.query_net(query)
        B_k = self.key_net(key)
        B_v = self.value_net(value)

        # 计算注意力分数
        attention_scores = torch.bmm(A_q, B_k.permute(0, 2, 1))
        attention_scores = attention_scores / torch.sqrt(torch.tensor(embed_dim, dtype=torch.float32))

        # 使用Softmax函数计算注意力权重
        attention_weights = F.softmax(attention_scores, dim=-1)

        # 加权求和得到最终输出
        output = torch.bmm(attention_weights, B_v)

        return output

# 示例使用
batch_size = 2
seq_len_q = 5
seq_len_k = 10
embed_dim = 64

ca = CrossAttention(embed_dim)
query = torch.randn(batch_size, seq_len_q, embed_dim)
key = torch.randn(batch_size, seq_len_k, embed_dim)
value = torch.randn(batch_size, seq_len_k, embed_dim)

# 前向传播
output = ca(query, key, value)

# 打印输出形状
print("Output shape:", output.size())

```



## T5-FusionLayer
:::color3
**简介：全局的文本特征、图像特征分别作为一个序列位置输入，t5内部cross att交互**

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/TIGER-AI-Lab/UniIR](https://github.com/TIGER-AI-Lab/UniIR/blob/main/src/models/uniir_clip/clip_featurefusion/clip_ff.py)

**paper：**[**https://arxiv.org/pdf/2311.17136**](https://arxiv.org/pdf/2311.17136)

**参考：**[**https://zhuanlan.zhihu.com/p/704347800**](https://zhuanlan.zhihu.com/p/704347800)

:::

:::color5
**<font style="color:#601BDE;">1.多模态融合方法对比</font>**

:::

1. **分数级融合**：将每个模态编码成单一特征；
2. **CLIP特征级融合**（CLIP_FF）：通过混合模态transformer层将两个模态融合成单一特征；
3. **BLIP特征级融合**（BLIP_FF）：采用交叉注意力(cross attention)输出单一特征向量。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742542420599-3ad70256-a007-432f-b966-2727719d987d.png)

:::color5
**<font style="color:#601BDE;">1.代码实现</font>**

:::

```python
class T5FusionLayer(nn.Module):
    """
    Reference:
    https://arxiv.org/pdf/2311.17136
    https://github.com/TIGER-AI-Lab/UniIR/blob/main/src/models/uniir_clip/clip_featurefusion/clip_ff.py
    """
    def __init__(self, feature_dim:int):
        # 初始化特征融合模块
        super().__init__()

        # T5的配置参数(is_decoder=True时会去除cross att模块)
        conf_t5 = T5Config()
        conf_t5.num_layers = 2
        conf_t5.num_heads = 12
        conf_t5.d_model = feature_dim
        conf_t5.d_kv = 64
        self.t5_layers = T5Stack(conf_t5)


    def forward(self, txt_feat, img_feat):
        # [batch_size, embed_dim]————>[batch_size, seq_len, embed_dim]，增加seq维度，用于cross att计算
        txt_feat_expanded = txt_feat.unsqueeze(1) if len(txt_feat.shape) < 3 else txt_feat
        img_feat_expanded = img_feat.unsqueeze(1) if len(img_feat.shape) < 3 else img_feat

        # 全局的文本特征、图像特征分别作为一个序列位置输入，t5内部cross att交互
        combined_features = torch.cat([txt_feat_expanded, img_feat_expanded], dim=1)  # shape: [batch_size, seq_len, embed_dim]

        # 通过T5层进行处理
        transformer_output = self.t5_layers(
            inputs_embeds=combined_features,
            attention_mask=None,
            use_cache=False,
            return_dict=True,
        )

        # 平均池化
        def mean_pooling(embeddings):
            return torch.mean(embeddings, dim=1)

        # 从最后的Transformer状态中池化得到最终的多模态嵌入
        multimodal_emb = mean_pooling(transformer_output.last_hidden_state)

        return multimodal_emb  # shape: [batch_size, embed_dim]


```

