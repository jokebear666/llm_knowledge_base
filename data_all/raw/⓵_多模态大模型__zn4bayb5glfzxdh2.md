# ⓵ 多模态大模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/zn4bayb5glfzxdh2 -->

一个典型的多模态大模型（MLLM）可以抽象为三个模块：（1）预训练的模态编码器；（2）预训练的大语言模型（LLM）；（3）跨模态投影层。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472157259-d53bdda1-4e31-4694-b9a9-271570e2f749.png)

**视觉编码器**：通常视觉编码器不会总从头训练，一种常见的方法是使用已经与其他模态对齐的预训练编码器。例如，CLIP通过在图像-文本对上进行大规模预训练，将视觉编码器与文本在语义上对齐。下表总结了常用的图像编码器系列。除了普通的CLIP图像编码器，一些工作还探索了使用其他变体。例如，MiniGPT-4采用了EVA-CLIP（ViT-G/14）编码器，该编码器通过改进的训练技术进行训练。。一些工作还探索了无编码器架构，例如，Fuyu-8b的图像经过patch后直接经投影层后送到LLM。因此，该模型自然支持灵活的图像分辨率输入。

**预训练LLM**：通过在大量语料库上进行预训练，LLM已经嵌入了丰富的知识，并展示了强大的泛化和推理能力。我们在下表中总结了常用的LLM。大多数LLM属于因果解码器类别。其中，FlanT5系列是较早在BLIP-2和InstructBLIP等工作中使用的LLM。LLaMA系列和Vicuna家族是吸引了大量学术关注的代表性开源LLM。由于这两个LLM主要是在英语语料库上预训练的，它们在多语言支持方面受到限制，例如中文。

**跨模态投影层**：由于LLM只能感知文本，因此需要在自然语言和其他模态之间架起桥梁。然而，以端到端的方式训练大型多模态模型成本过高。更实际的方法是在预训练的视觉编码器和LLM之间引入一个可学习的连接器。可学习的连接器负责在不同模态之间架起桥梁。这种方法的代表是Q-Former。Q-Former利用一组可学习的query-token以基于查询的方式提取信息，首先在BLIP-2中实现。这种Q-Former风格的压缩视觉token到较少数量的表征向量。在参数大小方面，可学习的投影层参数通常只占编码器和LLM的一小部分。以Qwen-VL为例，Q-Former的参数大小约为0.08B，占整个参数的不到1%，而编码器和LLM分别占19.8%（1.9B）和80.2%（7.7B）。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472157260-f5e090ef-3874-4dd7-ae82-7b34f204dc36.png)

开源方案

<font style="color:rgb(6, 6, 7);">自从GPT-4发布以来，多模态大模型展示了惊人的能力，MLLMs的研究热潮不断。下图展示了MLLMs的时间线。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472157255-8a21aa36-3ba1-4339-b0f5-d5f205a2b93f.png)





## GPT-4O<font style="color:#D22D8D;"></font>
:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">GPT-4o</font>](https://zhida.zhihu.com/search?content_id=243158209&content_type=Article&match_order=1&q=GPT-4o&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（omni,全部之意）是一个非常优秀的</font>[<font style="color:rgb(9, 64, 142);">多模态大模型</font>](https://zhida.zhihu.com/search?content_id=243158209&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。它的输入是语音、文字、图像/视频。输出自然有语音、文字、图像。</font>

**参考：**[**为什么说GPT-4o是原生多模态？**](https://www.zhihu.com/question/656277599/answer/3507582169)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741935151830-5f5d1127-2e2d-4187-aa9a-c39f247e5418.png)

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">从整体上看，GPT-4o是一个极其特殊的多模态模型。不太可能是多个模型组合的东西。所以，它的大概结构框架可能是这样的图。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741935294342-353c1cd8-6a3f-4d8a-88e7-5a7865fec1aa.png)

:::color5
**<font style="color:#601BDE;">2.流式语音识别</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741935369990-a35e8166-c79f-4564-a36c-e46d7cfc56c2.png)

## 谷歌系列
### Gemma-3
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">在巴黎开发者日上，开源Gemma系模型正式迭代到第三代，原生支持多模态，128k上下文。</font>

<font style="color:rgba(0, 0, 0, 0.9);">此次，Gemma 3一共开源了四种参数，1B、4B、12B和27B。最最最关键的是，一块GPU/TPU就能跑模型。</font>

:::

:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3是谷歌迄今最先进、最便携的开源模型，采用与Gemini 2.0模型相同的研究和技术打造。专为</font>**<font style="color:#ED740C;">在端侧设备上直接运行</font>**<font style="color:rgba(0, 0, 0, 0.9);">而设计——从手机和笔记本电脑到工作站，帮助开发者在需要的地方创建AI应用。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[gemma-3](https://huggingface.co/collections/google/gemma-3-release-67c6c6f89c4f76621268bb6d)

**paper：**[**Gemma 3 Technical Report**](https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf)

**参考：**[**谷歌Gemma 3上线！单GPU最强多模态手机可跑，27B完胜o3-mini**](https://mp.weixin.qq.com/s/buqtV1nEDhpvdvEFhRcoIA)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742207515480-2f0d38ab-e3d3-48e3-8ec2-7a0fb9f75fdf.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgba(0, 0, 0, 0.9);">使用世界最佳单设备加速模型进行开发：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3在LMArena排行榜的初步人类偏好评估中超越了Llama-405B、DeepSeek-V3和o3-mini，能在单个GPU或TPU主机上运行，开发独特的用户体验。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">支持140种语言，走向全球：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3为超过35种语言提供开箱即用的支持，并为超过140种语言提供预训练支持。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">创建具有高级文本和视觉推理能力的AI：</font>**<font style="color:rgba(0, 0, 0, 0.9);">轻松开发可以分析图像、文本和短视频的应用程序，为交互式和智能应用开创新的可能性。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">通过扩展的上下文窗口处理复杂任务：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3提供128k token的上下文窗口，让应用程序能够处理和理解海量信息。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">使用函数调用创建AI驱动的工作流：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3支持函数调用和结构化输出，帮助你实现任务自动化并构建智能体验。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">使用量化模型更快实现高性能：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3推出官方量化版本，在保持高精度的同时减少模型大小和计算需求。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">相比Gemma 2，研究者为Gemma 3预训练模型分配了更大的token预算。其中，Gemma 3 27B规模的模型在14万亿个token上进行训练，12B 规模的模型使用12T个token，4B 规模的模型使用4T个token，而1B规模的模型使用 2T个token。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **LLM：**

<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3模型沿用了与前代版本相同的解码器Transformer 结构，其大部分架构元素与前两代Gemma版本类似。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究采用了分组查询注意力（</font><font style="color:#74B602;">Grouped-Query Attention, GQA</font><font style="color:rgba(0, 0, 0, 0.9);">），并结合了</font>**<font style="color:#74B602;"> RMSNorm</font>**<font style="color:rgba(0, 0, 0, 0.9);">的后归一化（post-norm）和前归一化（pre-norm）。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究者在自注意力机制中交替使用局部</font>**<font style="color:#74B602;">滑动窗口自注意力</font>**<font style="color:rgba(0, 0, 0, 0.9);">和全局自注意力，按照5层局部层对应1层全局层的模式排列，模型的第一层为局部层。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在全局自注意力层上，研究者将</font>**<font style="color:#74B602;">RoPE的基准频率从10K提高到1M</font>**<font style="color:rgba(0, 0, 0, 0.9);">，而局部层的频率保持在10K。此外，他们采用了</font>**<font style="color:#74B602;">位置插值方法</font>**<font style="color:rgba(0, 0, 0, 0.9);">，以扩展全局自注意力层的适用范围。</font>

2. **视觉编码器：**

<font style="color:rgba(0, 0, 0, 0.9);">研究采用了一种</font>**<font style="color:#74B602;">400M规模的SigLIP编码器变体</font>**<font style="color:rgba(0, 0, 0, 0.9);">，这是一种基于Vision Transformer的模型，并使用CLIP损失的变体进行训练。Gemma视觉编码器的输入为调整尺寸后的896 × 896像素的方形图像，并在视觉助手任务的数据上进行微调。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在pre-train和post-train过程中，Gemma 3使用了蒸馏技术，并通过强化学习和模型合并的组合，进行了优化。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在post-train阶段，使用多种奖励函数来提升模型在</font>**<font style="color:#74B602;">帮助性、数学、编程、推理、遵循指令和多语言</font>**<font style="color:rgba(0, 0, 0, 0.9);">能力方面的表现，同时最小化模型的有害性。Gemma 3主要使用了4个组件：</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">从更大的指令模型中提取到Gemma 3预训练检查点</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">基于人类反馈的强化学习（RLHF），使模型预测与人类偏好保持一致。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">机器反馈强化学习（RLMF），增强数学推理。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">强化学习执行反馈（RLEF），提高编码能力。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在多项基准测试中，Gemma 3全家桶相较于上一代实现了全面提升，27B模型在数学性能暴涨33-45分。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742206588016-d193937e-b4d6-4c3f-9343-5d250ea587be.png)





## Qwen-VL系列
### Qwen-VL系列对比<font style="color:#D22D8D;"></font>
:::color3
**参考：**[**如何评价千问发布的Qwen2.5-VL?**](https://www.zhihu.com/question/10742671583)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742194707977-e3d1a34f-e1f4-471a-a5e9-8fc0a97f03c2.png)

:::color5
**<font style="color:#601BDE;">1.模型结构对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| | **<font style="color:#000000;">Qwen-VL</font>** | **<font style="color:#000000;">Qwen2-VL</font>** | **<font style="color:#000000;">Qwen2.5-VL</font>** |
| --- | --- | --- | --- |
| 位置编码 | RoPE | <font style="color:#000000;">2D-RoPE, M-RoPE</font> | <font style="color:#000000;">2D-RoPE, M-RoPE</font> |
| 分辨率 | <font style="color:#000000;">预训练 224 x 224</font><br/><font style="color:#000000;">多任务预训练 448 x 448</font> | <font style="color:#000000;">动态分辨率</font> | <font style="color:#000000;">动态分辨率</font> |
| 视觉编码器 | <font style="color:rgb(25, 27, 31);">Openclip’s ViT-bigG</font> | <font style="color:rgb(25, 27, 31);">DFN-ViT + </font>[<font style="color:rgb(9, 64, 142);">2D RoPE</font>](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=2D+RoPE&zhida_source=entity) | 1. <font style="color:rgb(25, 27, 31);">Dynamic-resolution ViT </font><br/>2. [<font style="color:rgb(9, 64, 142);">Window attention</font>](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=Window+attention&zhida_source=entity)<br/>3. <font style="color:rgb(25, 27, 31);"> 2D RoPE</font> |
| <font style="color:rgb(25, 27, 31);">视觉编码器参数量</font> | <font style="color:rgb(25, 27, 31);">1.9B</font> | <font style="color:rgb(25, 27, 31);">675M</font> | <font style="color:rgb(25, 27, 31);">-</font> |
| <font style="color:rgb(25, 27, 31);">LLM</font> | <font style="color:rgb(25, 27, 31);">Qwen</font> | <font style="color:rgb(25, 27, 31);">Qwen2</font> | <font style="color:rgb(25, 27, 31);">Qwen2.5</font> |
| <font style="color:rgb(25, 27, 31);">多模态对齐</font> | [<font style="color:rgb(9, 64, 142);">Cross attention module</font>](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=Cross+attention+module&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:#ED740C;">（Q-former）</font>**<br/><font style="color:rgb(25, 27, 31);">visual feature不同size -> 256</font> | **<font style="color:#74B602;">Simple MLP</font>**<font style="color:rgb(25, 27, 31);">   </font><font style="color:rgb(25, 27, 31);">visual feature不同size -> 除以28</font> | **<font style="color:rgb(25, 27, 31);">两层MLP</font>**<font style="color:rgb(25, 27, 31);">   </font><font style="color:rgb(25, 27, 31);">visual feature不同size -> 除以28</font> |
| 归一化 |  |  | RMSNorm |
| 激活函数 |  |  | SwiGLU |
| 预训练 | 1. 预训练：冻结LLM，只优化了视觉编码器和VL适配器<br/>2. 多任务预训练：同时训练7项任务 | | 1. <font style="color:rgb(25, 27, 31);">视觉预训练</font><br/>2. <font style="color:rgb(25, 27, 31);">多模态预训练</font><br/>3. <font style="color:rgb(25, 27, 31);">长文本预训练</font> |
| SFT | 冻结视觉编码器，优化语言模型和适配器模块。 | | 动态配比优化机制 |
| DPO | / | |


### Qwen3-VL
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(0, 0, 0);">Qwen3VL的代码已于9月10号向HuggingFace的GitHub仓库提交PR，并在15号被合并。同时，据相关消息，其模型权重将在本周五（9月26号）的阿里云栖大会上发布。</font>

:::

:::color3
**简介：**<font style="color:rgb(0, 0, 0);">Qwen3-VL 是一个多模态视觉-语言模型系列，涵盖稠密（dense）与 MoE（稀疏专家）两类架构，并提供 Instruct 与 Thinking 版本。在前代基础上，</font>**<font style="color:#ED740C;">Qwen3-VL 在保持强劲纯文本能力的同时显著提升了视觉理解</font>**<font style="color:rgb(0, 0, 0);">。其关键架构改进包括：</font>

+ <font style="color:rgb(1, 1, 1);">采用交错布局（interleaved layout）的增强型MRoPE，用于更优的时空建模；</font>
+ <font style="color:rgb(1, 1, 1);">集成 DeepStack，有效利用 Vision Transformer（ViT）的多层级特征；</font>
+ <font style="color:rgb(1, 1, 1);">以及通过基于文本的时间对齐提升视频理解——从 T-RoPE 演进为“文本时间戳对齐”，实现更精确的时间定位。</font>

**github**：[Adding Support for Qwen3-VL Series](https://github.com/huggingface/transformers/pull/40795/commits/3860fcc43692d1cec9a31ea7e01a519beabdcfe9)

**huggingface**：[huggingface.co/docs/transformers/main/en/model_doc/qwen3_vl#qwen3-vl](https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_vl#qwen3-vl)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[云栖大会](https://yunqi.aliyun.com/?spm=5176.30447480.J_kZCUqt4Y4-3pgz9RmjJMN.2.bfb93945hJZFJE)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758609927041-1aba8ed3-4e77-43d7-b6ba-f329f8163a61.png)

:::color5
**<font style="color:#601BDE;">1.引入DeepStack</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">在</font>`<font style="color:rgb(239, 112, 96);">Qwen3VLVisionModel</font>`<font style="color:rgb(0, 0, 0);">中新引入</font>`<font style="color:rgb(239, 112, 96);">deepstack</font>`<font style="color:rgb(0, 0, 0);">模块。在默认config中，其会提取视觉编码器的第8, 16, 24层中间特征（默认config中视觉编码器总共27层）</font>

```python

class Qwen3VLVisionModel(Qwen3VLPreTrainedModel):
    def __init__(self, config, *inputs, **kwargs) -> None:
        ...
        self.deepstack_visual_indexes = config.deepstack_visual_indexes
        # deepstack_visual_indexes=[8, 16, 24]
        self.deepstack_merger_list = nn.ModuleList(
            [
                Qwen3VLVisionPatchMerger(
                    config=config,
                    use_postshuffle_norm=True,
                )
                for _ in range(len(config.deepstack_visual_indexes))
            ]
        )
        self.gradient_checkpointing = False
```

<font style="color:rgb(0, 0, 0);">这里的</font>`<font style="color:rgb(239, 112, 96);">Qwen3VLVisionPatchMerger</font>`<font style="color:rgb(0, 0, 0);">是负责让视觉Token对齐到文本Token的MLP，与Qwen2.5VL架构中的</font>`<font style="color:rgb(239, 112, 96);">PatchMerger</font>`<font style="color:rgb(0, 0, 0);">功能类似，具体实现为：	</font>

```python
class Qwen3VLVisionPatchMerger(nn.Module):
    def __init__(self, config: Qwen3VLVisionConfig, use_postshuffle_norm=False) -> None:
        super().__init__()
        self.hidden_size = config.hidden_size * (config.spatial_merge_size**2)
        self.use_postshuffle_norm = use_postshuffle_norm
        self.norm = nn.LayerNorm(self.hidden_size if use_postshuffle_norm else config.hidden_size, eps=1e-6)
        self.linear_fc1 = nn.Linear(self.hidden_size, self.hidden_size)
        self.act_fn = nn.GELU()
        self.linear_fc2 = nn.Linear(self.hidden_size, config.out_hidden_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.norm(x.view(-1, self.hidden_size) if self.use_postshuffle_norm else x).view(-1, self.hidden_size)
        x = self.linear_fc2(self.act_fn(self.linear_fc1(x)))
        return x
```

<font style="color:rgb(0, 0, 0);">保存下来的</font>`<font style="color:rgb(239, 112, 96);">deepstack_feature_lists</font>`<font style="color:rgb(0, 0, 0);">会和</font>`<font style="color:rgb(239, 112, 96);">hidden_states</font>`<font style="color:rgb(0, 0, 0);">一起送到</font>`<font style="color:rgb(239, 112, 96);">Qwen3VLTextModel</font>`<font style="color:rgb(0, 0, 0);">(实际上用的就是Qwen3)，具体处理逻辑如下</font>

```python
class Qwen3VLTextModel(Qwen3VLPreTrainedModel):

    def __init__(self, config: Qwen3VLTextConfig):
        ...
        
    def forward(..., **kwargs ):
        # decoder layers
        for layer_idx, decoder_layer in enumerate(self.layers):
            layer_outputs = decoder_layer(
                hidden_states,
                attention_mask=attention_mask,
                position_ids=text_position_ids,
                past_key_values=past_key_values,
                cache_position=cache_position,
                position_embeddings=position_embeddings,
                **kwargs,
            )
            hidden_states = layer_outputs

            # add visual features to the hidden states of first several layers
            if deepstack_visual_embeds is not None and layer_idx in range(len(deepstack_visual_embeds)):
                hidden_states = self._deepstack_process(
                    hidden_states,
                    visual_pos_masks,
                    deepstack_visual_embeds[layer_idx],
                )

        hidden_states = self.norm(hidden_states)

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=past_key_values,
        )
        
    def _deepstack_process(self, hidden_states, visual_pos_masks, visual_embeds):
        visual_pos_masks = visual_pos_masks.to(hidden_states.device)
        visual_embeds = visual_embeds.to(hidden_states.device, hidden_states.dtype)
        local_this = hidden_states[visual_pos_masks, :].clone() + visual_embeds
        hidden_states[visual_pos_masks, :] = local_this
        return hidden_states
```

<font style="color:rgb(0, 0, 0);">这里</font>`<font style="color:rgb(239, 112, 96);">visual_pos_masks</font>`<font style="color:rgb(0, 0, 0);">表示</font>`<font style="color:rgb(239, 112, 96);">hidden_states</font>`<font style="color:rgb(0, 0, 0);">中哪些token之前是视觉token。因此，上述操作就是在第8, 16, 24层中，直接把deepstack中保存的对应特征加到原本visual token的位置上，进行融合多尺度的特征。</font>

<font style="color:rgb(0, 0, 0);">实际上，这个结构与CV领域中常用的FPN在理念上非常相似。</font>

:::color5
**<font style="color:#601BDE;">2.基础配置改动</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">其中需要着重关注的是:</font>

1. <font style="color:rgb(1, 1, 1);">默认的hidden_act激活函数从</font>`<font style="color:rgb(239, 112, 96);">silu</font>`<font style="color:rgb(1, 1, 1);">替换为</font>`<font style="color:rgb(239, 112, 96);">gelu_pytorch_tanh</font>`
2. <font style="color:rgb(1, 1, 1);">视觉编码器中默认的patch_size由14x14变为16x16</font>

**Qwen3VL**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758618299111-c9790b50-8977-45d7-b724-19595f534ef0.png)

**Qwen2.5VL**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758618267869-6cf629bd-faea-44e6-988f-595a45080a0f.png)

:::color5
**<font style="color:#601BDE;">3.视频处理逻辑修改</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

`<font style="color:rgb(239, 112, 96);">Qwen3VLProcessor</font>`<font style="color:rgb(0, 0, 0);">中的图像处理和tokenizer与Qwen2.5VL相同，继续沿用Qwen2中的</font>`<font style="color:rgb(239, 112, 96);">Qwen2VLImageProcessor</font>`<font style="color:rgb(0, 0, 0);">和</font>`<font style="color:rgb(239, 112, 96);">Qwen2TokenizerFast</font>`<font style="color:rgb(0, 0, 0);">。</font>

```python
class Qwen3VLProcessor(ProcessorMixin):
    r"""
    Constructs a Qwen3VL processor which wraps a Qwen3VL image processor and a Qwen2 tokenizer into a single processor.
    [`Qwen3VLProcessor`] offers all the functionalities of [`Qwen2VLImageProcessor`] and [`Qwen2TokenizerFast`]. See the
    [`~Qwen3VLProcessor.__call__`] and [`~Qwen3VLProcessor.decode`] for more information.
    Args:
        image_processor ([`Qwen2VLImageProcessor`], *optional*):
            The image processor is a required input.
        tokenizer ([`Qwen2TokenizerFast`], *optional*):
            The tokenizer is a required input.
        video_processor ([`Qwen3VLVideoProcessor`], *optional*):
            The video processor is a required input.
        chat_template (`str`, *optional*): A Jinja template which will be used to convert lists of messages
            in a chat into a tokenizable string.
    """

    attributes = ["image_processor", "tokenizer", "video_processor"]
    image_processor_class = "AutoImageProcessor"
    video_processor_class = "AutoVideoProcessor"
    tokenizer_class = ("Qwen2Tokenizer", "Qwen2TokenizerFast")
```

<font style="color:rgb(0, 0, 0);">但在视频处理中，本次</font>**<font style="color:rgb(0, 0, 0);">引入了新的Qwen3VLVideoProcessor</font>**<font style="color:rgb(0, 0, 0);">。其重新实现了</font>`<font style="color:rgb(239, 112, 96);">smart_resize</font>`<font style="color:rgb(0, 0, 0);">函数，从仅按空间分辨率(H,W)约束，升级为按时空体素(T×H×W)的总像素预算做“THW 联动”缩放，更适配视频处理:</font>

```python
def smart_resize(
    num_frames: int,
    height: int,
    width: int,
    temporal_factor: int = 2,
    factor: int = 32,
    min_pixels: int = 128 * 128,
    max_pixels: int = 16 * 16 * 2 * 2 * 2 * 6144,
):
    if num_frames < temporal_factor:
        raise ValueError(f"t:{num_frames} must be larger than temporal_factor:{temporal_factor}")
    if height < factor or width < factor:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(
            f"absolute aspect ratio must be smaller than 200, got {max(height, width) / min(height, width)}"
        )
    h_bar = round(height / factor) * factor
    w_bar = round(width / factor) * factor
    t_bar = round(num_frames / temporal_factor) * temporal_factor

    if t_bar * h_bar * w_bar > max_pixels:
        beta = math.sqrt((num_frames * height * width) / max_pixels)
        h_bar = max(factor, math.floor(height / beta / factor) * factor)
        w_bar = max(factor, math.floor(width / beta / factor) * factor)
    elif t_bar * h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (num_frames * height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor

    return h_bar, w_bar
```

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">T-RoPE改为时间戳对齐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">此外，本次改动将T-RoPE改为时间戳对齐。原本的Qwen2.5VL是用绝对时间id+动态fps实现的T-RoPE，而Qwen3VL改成了对每帧利用文本时间戳去确定RoPE，核心代码区别如下：</font>

[modeling_qwen3_vl.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_vl/modeling_qwen3_vl.py)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758618747395-60b51954-2850-4228-b8d6-5a40f94ce97c.png)

:::color5
**<font style="color:#601BDE;">5.M-ROPE改进</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">Qwen2-VL为了适应多模态输入引入了M-RoPE，对所有模态进行统一编码，这个模块也被延用到Qwen2.5VL。</font>

<font style="color:rgb(0, 0, 0);">M-RoPE把所有模态的数据都看作有3个维度</font><font style="color:rgb(1, 1, 1);">(T, H, W)</font><font style="color:rgb(0, 0, 0);">，具体来说：</font>

+ <font style="color:rgb(1, 1, 1);">对于视频的话，每一帧的T的index是往后递增的；</font>
+ <font style="color:rgb(0, 0, 0);">对于单张图片来说T的index是不动的，HW随着位置变化会变二维index；</font>
+ <font style="color:rgb(1, 1, 1);">对于文本来说，(T, H, W)默认都是相等的。</font>

<font style="color:rgb(0, 0, 0);">而在Qwen3VL中，把三维频率从分块布局[TTT...HHH...WWW]重排成交替布局[THTHWHTW]，实现“交织式”的多模态RoPE。</font>

```python
class Qwen3VLTextRotaryEmbedding(nn.Module):
    def __init__(self, config: Qwen3VLTextConfig, device=None):
    ...
    
    def apply_interleaved_mrope(self, freqs, mrope_section):
        """Apply interleaved MRoPE to 3D rotary embeddings.
        Reorganizes frequency layout from chunked [TTT...HHH...WWW] to
        interleaved [THTHWHTHW...TT], preserving frequency continuity.
        args:
            x: (3, bs, seq_len, head_dim // 2)
            mrope_section: (3,)
        returns:
            x_t: (bs, seq_len, head_dim // 2)
        """
        freqs_t = freqs[0]  # just overwrite the first dimension T
        for dim, offset in enumerate((1, 2), start=1):  # H, W
            length = mrope_section[dim] * 3
            idx = slice(offset, length, 3)
            freqs_t[..., idx] = freqs[dim, ..., idx]
        return freqs_t
```

### Qwen2.5-VL<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(31, 31, 31);"></font>**<font style="color:rgb(31, 31, 31);">Qwen2.5-VL</font>**<font style="color:rgb(31, 31, 31);">，Qwen 模型家族的旗舰视觉语言模型，包含 3B、7B 和 72B  3 个模型尺寸。</font>

:::

:::color3
**简介：****<font style="color:rgb(31, 31, 31);">Qwen2.5-VL的主要特点：</font>**

+ **<font style="color:rgb(31, 31, 31);">感知更丰富的世界</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 不仅擅长识别常见物体，如花、鸟、鱼和昆虫，还能够分析图像中的文本、图表、图标、图形和布局。</font>
+ **<font style="color:rgb(31, 31, 31);">Agent</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 直接作为一个视觉 Agent，可以推理并动态地使用工具，初步具备了使用电脑和使用手机的能力。</font>
+ **<font style="color:rgb(31, 31, 31);">理解长视频和捕捉事件</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 能够理解超过 1 小时的视频，并且这次它具备了通过精准定位相关视频片段来捕捉事件的新能力。</font>
+ **<font style="color:rgb(31, 31, 31);">视觉定位</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 可以通过生成 bounding boxes 或者 points 来准确定位图像中的物体，并能够为坐标和属性提供稳定的 JSON 输出。</font>
+ **<font style="color:rgb(31, 31, 31);">结构化输出</font>**<font style="color:rgb(31, 31, 31);">：对于发票、表单、表格等数据，Qwen2.5-VL 支持其内容的结构化输出，惠及金融、商业等领域的应用。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://qwenlm.github.io/zh/blog/qwen2.5-vl/](https://qwenlm.github.io/zh/blog/qwen2.5-vl/)

**github**：[https://github.com/QwenLM/Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583)  [Qwen2.5-VL更新！](https://zhuanlan.zhihu.com/p/25347969116)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191876384-65f80eeb-919a-4f47-990e-48e0f7b6ba3e.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">算法侧提升</font>**

+ **<font style="color:rgb(25, 27, 31);">Vision encoder</font>**
    - <font style="color:rgb(25, 27, 31);">使用了_</font>[<font style="color:rgb(9, 64, 142);">window attention</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=window+attention&zhida_source=entity)<font style="color:rgb(25, 27, 31);">_ 提高inference效率</font>
+ **<font style="color:rgb(25, 27, 31);">Video understanding</font>**
    - <font style="color:rgb(25, 27, 31);">引入了 dynamic FPS sampling 策略，相当于一种时间上的dynamic resolution</font>
    - <font style="color:rgb(25, 27, 31);">升级了</font>[<font style="color:rgb(9, 64, 142);">MRoPE</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=MRoPE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在时间上，对齐了 absolute time</font>
+ **<font style="color:rgb(25, 27, 31);">High-Qaulity Data</font>**
    - <font style="color:rgb(25, 27, 31);">从1.2 trillion 数据增加到 4.1 trillion 数据（单位token）</font>

**<font style="color:rgb(25, 27, 31);">应用侧展现</font>**

+ **<font style="color:rgb(25, 27, 31);">强大的文档解析能力:</font>**
    - <font style="color:rgb(25, 27, 31);">升级文本识别至全文档解析 (</font>[<font style="color:rgb(9, 64, 142);">Omnidocument Parsing</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=Omnidocument+Parsing&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)。</font>
    - <font style="color:rgb(25, 27, 31);">擅长处理多场景、多语言文档。</font>
    - <font style="color:rgb(25, 27, 31);">支持内置内容类型：手写、表格、图表、化学公式、乐谱。</font>
+ **<font style="color:rgb(25, 27, 31);">精确的跨格式对象定位:</font>**
    - <font style="color:rgb(25, 27, 31);">显著提升</font>**<font style="color:rgb(25, 27, 31);">物体检测</font>**<font style="color:rgb(25, 27, 31);">、</font>**<font style="color:rgb(25, 27, 31);">pointing</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">计数</font>**<font style="color:rgb(25, 27, 31);">精度。</font>
    - <font style="color:rgb(25, 27, 31);">支持输出物体坐标和JSON格式，实现高级空间推理。【除了box，增加point定位物体能力，并能稳定输出json】</font>
+ **<font style="color:rgb(25, 27, 31);">超长视频理解与细粒度视频定位:</font>**
    - <font style="color:rgb(25, 27, 31);">动态分辨率扩展至时间维度。</font>
    - <font style="color:rgb(25, 27, 31);">能够理解数小时的视频。【并非算法提升】</font>
    - <font style="color:rgb(25, 27, 31);">可以秒级提取视频片段。【Qwen2-VL已经有了】</font>
+ **<font style="color:rgb(25, 27, 31);">增强的智能体（agent）功能:</font>**
    - <font style="color:rgb(25, 27, 31);">利用高级定位、推理和决策能力。</font>
    - <font style="color:rgb(25, 27, 31);">适用于计算机和移动设备。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">Qwen2.5-VL 其实大部分的篇幅在数据处理，也就是SFT时代最枯燥但是最有用的工作。。。</font>**

<font style="color:rgb(25, 27, 31);">简单来说其预训练阶段采用</font>**<font style="color:rgb(25, 27, 31);">4万亿token</font>**<font style="color:rgb(25, 27, 31);">的高质量数据集，相比前代模型数据规模提升3倍以上，覆盖</font>**<font style="color:rgb(25, 27, 31);">图像描述、交错图文、OCR识别、视觉知识、文档解析、视频理解、智能体交互</font>**<font style="color:rgb(25, 27, 31);">等十余种模态类型。为确保不同模态数据的协同效应，千问团队提出一种</font>**<font style="color:#74B602;">动态配比优化机制</font>**<font style="color:rgb(25, 27, 31);">，避免模态之间冲突。这里就不展开了，主要是因为数据处理太垂直了，每一批数据都有tricky解法。</font>

**<font style="color:rgb(25, 27, 31);">预训练训练数据如下：</font>**<font style="color:rgb(25, 27, 31);">	</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742192466068-c99ae061-5eed-44ad-b579-8881737b4aa9.png)

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2.5-VL的结构改造重点就是</font>[<font style="color:rgb(9, 64, 142);">ViT</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=ViT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的改进。</font>

1. **<font style="color:rgb(25, 27, 31);">window attention</font>**

<font style="color:rgb(25, 27, 31);">基于ViT，Qwen2.5-VL使用了 window attention 编码图像加速计算。window attention 在swin transformer时代已经被广泛验证了其有效性了。</font>**<font style="color:#ED740C;">Window Attention将输入分割成不重叠的局部窗口，并在每个窗口内独立计算自attention</font>**<font style="color:rgb(25, 27, 31);">。之后会有一个</font>**<font style="color:#74B602;">shift window的操作，把每一个局部的attention关联为全局的attention</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">具体的，仅有四个 layers 使用 full self-attention，其余 layers 使用 windowed attention（最大 window size 为 112x112，对应 8x8 patches，因为这里image patche是14x14的pixels）。小于 112x112 的区域不进行 padding，以原始分辨率处理。这种设计使得模型能够直接处理原始分辨率的 input，避免不必要的 scaling 和 distortion。</font>

2. **<font style="color:rgb(25, 27, 31);">归一化</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">RMSNorm</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=RMSNorm&zhida_source=entity)<font style="color:rgb(25, 27, 31);">归一化</font>
3. **<font style="color:rgb(25, 27, 31);">激活函数</font>**<font style="color:rgb(25, 27, 31);">：使用SwiGLU做激活函数。</font>
4. **<font style="color:rgb(25, 27, 31);">training from scratch</font>**
    1. <font style="color:rgb(25, 27, 31);">由于RoPE和window attention等组件引入，整个ViT重新训练了。包含三个训练阶段，具体的细节没有展开</font>
    2. [<font style="color:rgb(9, 64, 142);">CLIP pre-training</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=CLIP+pre-training&zhida_source=entity)
    3. <font style="color:rgb(25, 27, 31);">vision-language alignment</font>
    4. [<font style="color:rgb(9, 64, 142);">end-to-end fine-tuning</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=end-to-end+fine-tuning&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>
5. **<font style="color:rgb(25, 27, 31);">LLM</font>**<font style="color:rgb(25, 27, 31);">：引入了 Qwen2.5 LLM，唯一需要修改的就是把原来一维的RoPE改为 MRoPE</font>
6. <font style="color:rgb(25, 27, 31);">多模态对齐（多模态adaptor）：这里的MLP映射没变，主要考虑了vision 的token太多了，所以需要压缩送入LLM。所以最后用了</font>**<font style="color:#74B602;">两层MLP压缩vision token四倍</font>**<font style="color:rgb(25, 27, 31);">（2x2）。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **预训练：**<font style="color:rgb(25, 27, 31);">整个训练可以划分为三个阶段：</font>
    1. **<font style="color:rgb(25, 27, 31);">第一阶段，视觉预训练</font>**<font style="color:rgb(25, 27, 31);">，奠定 multimodal 理解的基础，主要使用 </font>**<font style="color:#74B602;">image captions、visual knowledge 和 OCR data</font>**<font style="color:rgb(25, 27, 31);">。这些数据集帮助 ViT 提取有效的视觉表征，并与 textual information 整合。</font>
    2. **<font style="color:rgb(25, 27, 31);">第二阶段，多模态预训练</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#74B602;">解冻所有 model 参数</font>**<font style="color:rgb(25, 27, 31);">，使用多样化的 multimodal image data 进行训练。这一阶段引入更复杂的数据集，如</font>**<font style="color:#74B602;"> interleaved data、multi-task learning datasets、VQA、multimodal mathematics、agent-based tasks、video understanding 和 pure-text datasets</font>**<font style="color:rgb(25, 27, 31);">，增强模型在视觉和语言模态间建立深层联系的能力，能够处理更复杂的任务。</font>
    3. **<font style="color:rgb(25, 27, 31);">第三阶段，长文本预训练</font>**<font style="color:rgb(25, 27, 31);">，进一步提升模型在</font>**<font style="color:#74B602;">长序列、video 和 agent-based data 上的推理能力</font>**<font style="color:rgb(25, 27, 31);">，同时增加 sequence length。这使模型能够处理更高级和精细的 multimodal 任务，特别适用于需要长距离依赖和复杂推理的任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742192466068-c99ae061-5eed-44ad-b579-8881737b4aa9.png)

2. **SFT+DPO：**

<font style="color:rgb(25, 27, 31);">在Supervised Fine-Tuning (SFT)阶段，千问团队采用了一个精心策划的数据集，以提升模型在多种模态下的指令遵循能力。该数据集约包含</font>**<font style="color:rgb(25, 27, 31);">200万条条目，50%为纯文本数据，50%为多模态数据</font>**<font style="color:rgb(25, 27, 31);">，包括</font>**<font style="color:rgb(25, 27, 31);">image-text和video-text组合</font>**<font style="color:rgb(25, 27, 31);">。多模态数据由于包含视觉和时间信息，训练时消耗的tokens和计算资源显著更多。</font>**<font style="color:rgb(25, 27, 31);">数据集主要由中文和英文数据组成</font>**<font style="color:rgb(25, 27, 31);">，并辅以多语言条目以支持更广泛的语言多样性。</font>

<font style="color:rgb(25, 27, 31);">为了适应多种应用场景，数据集包含专门的子集，如General Visual Question Answering (VQA)、image captioning、数学问题解决、coding任务和security-related queries。此外，还构建了专门用于Document和Optical Character Recognition (Doc and OCR)、Grounding、Video Analysis以及Agent Interactions的数据集，以提升领域特定的能力。这里还有详细的过滤流程，还是一样，有兴趣可以看原文。</font>

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">原生动态分辨率和帧率</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">这里Qwen2.5-VL介绍了两个概念：dynamic frame rate 和 absolute time encoding。</font>

<font style="color:rgb(25, 27, 31);">我们知道对于很多Video generation的工作，为了让网络知道FPS的概念，timestamps是文本形式（字符串）通过text encoder 编码进入网络的然后一般cross attention一下。</font>

<font style="color:rgb(25, 27, 31);">这里千问团队采用的是直接将MRoPE的ID和timestamp对齐，那么就可以动态采样MRoPE的ID来采样不同FPS的视频了， 所以也就不需要额外编码timestamp了，因为天然的是对齐的。如下图，因为qwen是用一个</font>**<font style="color:#ED740C;">2x3x3的3d conv编码的，所以一秒编码两帧，刚好就是两个MRoPE的ID</font>**<font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742192956900-8b6751b1-a6b7-4fd6-948e-b44b4a59491d.png)

:::color5
**<font style="color:#601BDE;">6.模型评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(31, 31, 31);">72B:</font>**

<font style="color:rgb(31, 31, 31);">我们对视觉语言模型进行了全面的评估，比较了 SOTA 模型以及同尺寸规模模型中表现最好的模型。在旗舰模型 Qwen2.5-VL-72B-Instruct 的测试中，它在一系列涵盖多个领域和任务的基准测试中表现出色，包括大学水平的问题、数学、文档理解、视觉问答、视频理解和视觉 Agent。值得注意的是，Qwen2.5-VL 在理解文档和图表方面具有显著优势，并且能够作为视觉 Agent 进行操作，而无需特定任务的微调。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742182471383-34f20b80-bc3d-4198-8879-61ea4f3d0a6f.png)

2. **<font style="color:rgb(31, 31, 31);">7B:</font>**

<font style="color:rgb(31, 31, 31);">在较小的模型方面，Qwen2.5-VL-7B-Instruct 在多个任务中超越了 GPT-4o-mini</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742182438789-c0905007-48fa-448b-8ae6-a2b3388cf401.png)

3. **<font style="color:rgb(31, 31, 31);">3B:</font>**

<font style="color:rgb(31, 31, 31);">Qwen2.5-VL-3B 作为端侧 AI 的潜力股，甚至超越了我们之前版本 Qwen2-VL 的 7B 模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742182457958-577639f4-3f09-4d04-bcd5-4cce4c050062.png)

### Qwen2-VL<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介**：作为在Qwen-VL基础上迭代的最新版本，Qwen2-VL在视觉理解上达到非常先进的性能。**<font style="color:#ECAA04;">不再使用Q-former,而是直接使用MLP进行对齐。</font>**

**paper : **[**https://arxiv.org/pdf/2409.12191**](https://arxiv.org/pdf/2409.12191)

**项目地址**：[https://github.com/QwenLM/Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583) [**多模态技术梳理：Qwen-VL系列**](https://zhuanlan.zhihu.com/p/25267823390)**  **

:::

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1733472157254-037f1f85-1f1b-4cf5-8fc7-24d39969869f.jpeg)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">对各种分辨率和比例的图像的先进理解</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 在视觉理解基准上达到最先进的性能，包括 MathVista、DocVQA、RealWorldQA、MTVQA 等。</font>
+ **<font style="color:rgb(51, 51, 51);">理解超过 20 分钟的视频</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 能够处理超过 20 分钟的视频，提供高质量的视频问答、对话、内容创作等功能。</font>
+ **<font style="color:rgb(51, 51, 51);">可操作手机、机器人等设备的智能体</font>**<font style="color:rgb(51, 51, 51);">：具备复杂推理和决策能力的 Qwen2-VL 可以与手机、机器人等设备集成，基于视觉环境和文本指令进行自动操作。</font>
+ **<font style="color:rgb(51, 51, 51);">多语言支持</font>**<font style="color:rgb(51, 51, 51);">：为了服务全球用户，Qwen2-VL 除了支持英语和中文外，现在还能够理解图像中不同语言的文本，包括大多数欧洲语言、日语、韩语、阿拉伯语、越南语等。</font>

:::color5
**<font style="color:#601BDE;">2.模型架构更新</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **视觉、文本编码器升级：**
    - **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：之前qwenvl用的Openclip’s ViT-bigG-14，现在用的是</font>**<font style="color:#ED740C;">DFN的ViT</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - **<font style="color:rgb(25, 27, 31);">LLM</font>**<font style="color:rgb(25, 27, 31);">：升级到了Qwen2，值得注意的是对于不同大小的LLM，vision encoder 参数量不变。</font>
2. **<font style="color:rgb(51, 51, 51);">动态分辨率</font>**<font style="color:rgb(51, 51, 51);">：与以往不同的是，Qwen2-VL 可以</font>**<font style="color:#74B602;">处理任意图像分辨率</font>**<font style="color:rgb(51, 51, 51);">，将其映射为动态数量的视token，提供更接近人类的视觉处理体验。</font>
    - **任意分辨率的图像**：取消[DFN ViT](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=DFN+ViT&zhida_source=entity)绝对位置编码，使用2d RoPE，使得ViT可以输入任意分辨率的图像。测试的时候，还会在后面接一个MLP，把2x2的token 编码成一个token。图像编码得到的token使用<|vision_start|> 和 <|vision_end|> 包裹。因此对于，224x224的图，因为ViT patch size=14，就会得到(224/14/2)^2+2 = 66 个token。**参考**：[多模态理解开源王者：InternVL 1.5->InternVL 2.0](https://zhuanlan.zhihu.com/p/707475931)
    - **图像Token范围**：qwen2-vl对图像token的范围，通过min_pixels和max_pixels 进行了约束，这两个变量描述了图像pixel的范围的最小值和最大值。如果小于或者大于min_pixels和max_pixels ，就会resize到这个范围内，以实现计算量和性能的trade off。

```plain
MIN_PIXELS = 256*28*28
MAX_PIXELS = 512*28*28
```

3. **<font style="color:rgb(51, 51, 51);">多模态旋转位置嵌入 (M-ROPE)</font>**<font style="color:rgb(51, 51, 51);">：将位置嵌入分解为多个部分，</font>**<font style="color:#74B602;">以捕捉 1D 文本、2D 视觉和 3D 视频的位置信息</font>**<font style="color:rgb(51, 51, 51);">，增强其多模态处理能力。</font><font style="color:rgb(25, 27, 31);">在空间分辨率上，增加了</font>**<font style="color:#ED740C;">时间维度</font>**<font style="color:rgb(25, 27, 31);">，如果是文本，三个分量都相同。消融实验证明M-RoPE在下游效果更好。</font>**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[从浅到深入门旋转位置编码](https://zhuanlan.zhihu.com/p/13023539180)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191399043-bf846218-c884-419e-8b74-7b79077e7890.png)

4. **<font style="color:rgb(25, 27, 31);">统一的图像、视频理解</font>**

<font style="color:rgb(25, 27, 31);">为了更好理解视频，使用</font>**<font style="color:#ED740C;">时间轴为2的3d conv编码图像/视频</font>**<font style="color:rgb(25, 27, 31);">。具体来说，如果是一张图，就copy两份，如果是视频就每秒采样2帧。</font>

5. **Bounding box 坐标归一化**

之前Qwen1-VL 的 bounding box是绝对坐标，而Qwen2-VL是归一化坐标，虽然叫归一化坐标，但是实际上是归一化到了[0, 1000)，坐标就是![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191763591-d922011a-c86e-4df5-b65c-9fb8daeadde3.png)的形式。格式就像这样，被检测的物体和box坐标分别被speical token包裹。

```python
<|object_ref_start|>the eyes on a giraffe<|object_ref_end|><|box_start|>(176,106),(232,160)<|box_end|>
```

6. **Visual Agent**

Visual agent 就是function call 的能力，让LLM直接调用某个function并输入参数，Qwen2-VL中支持了这一个操作。

:::color5
**<font style="color:#601BDE;">3.多模态Adaptor：MLP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

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

:::color5
**<font style="color:#601BDE;">4.统一的图像&视频理解框架</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL统一了视频和图像的理解框架，能混合输入图像和视频数据进行理解。为了保证图片和视频的处理一致，对视频和图像分别做如下处理：</font>

+ **<font style="color:rgb(25, 27, 31);">视频处理：</font>**<font style="color:rgb(25, 27, 31);">以</font>**<font style="color:#74B602;">每秒两帧的速率对视频进行采样</font>**<font style="color:rgb(25, 27, 31);">，最终可采样偶数个帧序列。对于长视频为了平衡序列长度和计算效率，通过动态调整每一帧的分辨率，将视频总token限制在16K以内。</font>
+ **<font style="color:rgb(25, 27, 31);">图像处理：</font>**<font style="color:rgb(25, 27, 31);">对图像做复制操作，使得单一图片，变成一个</font>**<font style="color:#74B602;">时序为2的帧序列</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">使用3D的卷积对帧序列做特征抽取，如下图所示，每两张图片为一组进行卷积操作抽取特征。这样通过将卷积核扩充了时序维度，可以进一步压缩序列长度，因此也能进一步提升模型处理更多帧的能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742280064072-3de7c797-cd76-4fd2-9006-2b768ba27b66.png)

### Qwen-VL
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">QWEN-VL是阿里巴巴达摩院开发的</font>**<font style="color:rgb(51, 51, 51);">多模态大语言模型</font>**<font style="color:rgb(51, 51, 51);">（MLLM），支持</font>**<font style="color:rgb(51, 51, 51);">视觉-语言联合理解</font>**<font style="color:rgb(51, 51, 51);">。其背景特点包括：</font>

+ **<font style="color:rgb(51, 51, 51);">行业需求</font>**<font style="color:rgb(51, 51, 51);">：GPT-4V等模型展现多模态潜力，但中文领域缺乏高性能开源方案</font>
+ **<font style="color:rgb(51, 51, 51);">技术定位</font>**<font style="color:rgb(51, 51, 51);">：作为Qwen系列（如Qwen-7B）的多模态扩展，专注于解决高分辨率图像理解、细粒度定位等难点</font>
+ **<font style="color:rgb(51, 51, 51);">开源优势</font>**<font style="color:rgb(51, 51, 51);">：提供中英双语支持，参数量可控（约9.6B），适配消费级GPU</font>

<font style="color:rgb(25, 27, 31);">一般称</font>**<font style="color:#ED740C;">Qwen-VL为multi task learning之后的模型</font>**<font style="color:rgb(25, 27, 31);">，而称</font>**<font style="color:#ED740C;">Qwen-VL-Chat为SFT之后的模型</font>**<font style="color:rgb(25, 27, 31);">。</font>

**paper : **[**https://arxiv.org/pdf/2308.12966**](https://arxiv.org/pdf/2308.12966)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583) [多模态技术梳理：Qwen-VL系列](https://zhuanlan.zhihu.com/p/25267823390)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| 维度 | 创新描述 |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">视觉编码</font>** | <font style="color:rgb(51, 51, 51);">动态高分辨率策略：将图像分割为448x448 patches（最高达1664x1664分辨率）</font> |
| **<font style="color:rgb(51, 51, 51);">训练框架</font>** | <font style="color:rgb(51, 51, 51);">三阶段渐进式训练：视觉编码器预训练 → 多模态对齐 → 指令微调</font> |
| **<font style="color:rgb(51, 51, 51);">跨模态融合</font>** | <font style="color:rgb(51, 51, 51);">轻量级Adapter设计（仅0.1B参数），通过Q-former连接视觉与语言模型</font> |
| **<font style="color:rgb(51, 51, 51);">任务支持</font>** | <font style="color:rgb(51, 51, 51);">支持检测框输出（格式：</font>`<font style="color:rgb(51, 51, 51);"><box>(x1,y1,x2,y2)</box></font>`<font style="color:rgb(51, 51, 51);">）与多轮对话</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **阶段** | **数据类型** | **规模** | **示例来源** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">预训练</font>** | <font style="color:rgb(51, 51, 51);">图像-文本对</font> | <font style="color:rgb(51, 51, 51);">1.5B</font> | <font style="color:rgb(51, 51, 51);">LAION-COCO, Objects365, OCR数据</font> |
| **<font style="color:rgb(51, 51, 51);">多任务预训练</font>** | <font style="color:rgb(51, 51, 51);">区域标注数据</font> | <font style="color:rgb(51, 51, 51);">60M</font> | <font style="color:rgb(51, 51, 51);">RefCOCO, VQA v2,检测数据集</font> |
| **<font style="color:rgb(51, 51, 51);">微调阶段</font>** | <font style="color:rgb(51, 51, 51);">指令数据</font> | <font style="color:rgb(51, 51, 51);">0.5M</font> | <font style="color:rgb(51, 51, 51);">人工标注、GPT-4生成的多轮对话</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(51, 51, 51);">文本：Qwen-7B</font>
+ <font style="color:rgb(51, 51, 51);">视觉：ViT-bigG</font>
+ <font style="color:rgb(51, 51, 51);">多模态Adaptor(多模态对齐)：</font>
    - <font style="color:rgb(51, 51, 51);">可学习查询向量(</font>**<font style="color:#ED740C;">Q-Former</font>**<font style="color:rgb(51, 51, 51);">)：为缓解长图像特征引起的效率问题，Qwen VL引入了一种</font>**<font style="color:#74B602;">压缩图像特征的视觉语言适配器</font>**<font style="color:rgb(51, 51, 51);">。此适配器包括随机初始化的</font>**<font style="color:#74B602;">单层交叉注意力模块</font>**<font style="color:rgb(51, 51, 51);">。该模块使用一组可训练的向量（embeddings）作为查询向量，来自视觉编码器的图像特征作为交叉注意力操作的关键。该机制将视觉特征序列压缩到</font>**<font style="color:#74B602;">256的固定长度</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">此外，</font>**<font style="color:#74B602;">考虑到位置信息对细粒度图像理解的重要性</font>**<font style="color:rgb(51, 51, 51);">，</font>**<font style="color:#74B602;">2D绝对位置编码整合到交叉注意力机制的查询KV对中</font>**<font style="color:rgb(51, 51, 51);">，以减轻位置的潜在损失压缩过程中的细节。长度为256的压缩图像特征序列随后被馈送到大型语言模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078135089-c01d6207-8a96-47ed-8084-cd2219eaff0b.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742269514251-822b277c-4e60-4834-90e9-2529c75ab06e.png)

**<font style="color:rgb(25, 27, 31);">标准的三阶段训练方法</font>**

1. **<font style="background-color:#D9EAFC;">预训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    1. **数据**：利用大规模、弱标记、网络爬行的图像文本集对。我们努力清理某些模式的数据集。如表2所示，原始数据集总共包含50亿个图像-文本对，经过清理后，剩余14亿个数据，其中77.3%为英文。中文（文本）数据占22.7%

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741077353636-eb920e51-03ea-415e-8671-3b6fe736fd14.png)

b. **预训练**：**<font style="color:#74B602;">冻结LLM，只优化了视觉编码器和VL适配器</font>**。输入图像的大小调整为224×224。训练目标是最小化文本标记。最大学习率为2e−4，训练过程使用batch-size30720的图像-文本对，整个预训练的第一阶段持续50000步，大约消耗<font style="color:#74B602;">1.5B的图文对</font>。

2. **<font style="background-color:#D9EAFC;">多任务预训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **数据**：引入高质量和细粒度的图文注释，具有更大输入分辨率的数据。我们对Qwen-VL**<font style="color:#74B602;">同时训练7项任务</font>**。对于文本生成，使用内部收集的语料库来维护。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741077714073-c8414b2f-b84c-466f-b520-9b31c45c50c3.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078058838-feca87bb-7b60-40c5-aed6-a612b4341408.png)

    - **训练**：分辨率从224×224提高到448×448，减少了信息量图像下采样造成的损失。此外，我们使用了window attention和global attention。我们**<font style="color:#74B602;">对视觉、LLM、VL投影都进行训练</font>**，训练目标与预训练阶段相同。
3. **<font style="background-color:#D9EAFC;">SFT</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **数据：**指令调优数据总计35万。**<font style="color:#74B602;">混合了多模态和纯文本对话训练过程中的数据</font>**，以确保模型在对话能力方面的通用性。指令调优数据总计35万。在此阶段，我们**<font style="color:#74B602;">冻结视觉编码器并优化语言模型和适配器模块</font>**。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078073564-bb09f492-d8d1-45ce-9128-908fe4367251.png)

    - **训练：**通过指令微调来微调Qwen VL预训练模型，以增强其指令跟踪和对话能力，形成了交互式Qwen VL聊天模型。

:::color5
**<font style="color:#601BDE;">5.训练参数</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741077454810-04621823-335f-4f7b-ac3f-c49960310269.png)

:::color5
**<font style="color:#601BDE;">6.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">高分辨率处理能力（比CLIP提升4倍细节）</font>
+ <font style="color:rgb(51, 51, 51);">支持检测框输出（无需额外检测头）</font>
+ <font style="color:rgb(51, 51, 51);">中英双语优化</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">推理速度较慢（处理1024px图像需约5s/RTX3090）</font>
+ <font style="color:rgb(51, 51, 51);">复杂推理能力弱于GPT-4V</font>

:::color5
**<font style="color:#601BDE;">7.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| 场景 | 示例 |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">医学影像</font> | <font style="color:rgb(51, 51, 51);">病理报告生成 + 病灶区域标注</font> |
| <font style="color:rgb(51, 51, 51);">电商</font> | <font style="color:rgb(51, 51, 51);">商品详情页解析（价格、规格提取）</font> |
| <font style="color:rgb(51, 51, 51);">教育</font> | <font style="color:rgb(51, 51, 51);">手写公式识别与解题步骤生成</font> |


:::color5
**<font style="color:#601BDE;">8.改进方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **效率优化**：
    - <font style="color:rgb(51, 51, 51);">动态token压缩（如对非关键区域降采样）</font>
    - <font style="color:rgb(51, 51, 51);">量化部署：使用AWQ技术压缩至4bit</font>
2. **性能提升**：
    - <font style="color:rgb(51, 51, 51);">引入扩散模型提升细粒度生成质量</font>
    - <font style="color:rgb(51, 51, 51);">集成检索增强（RAG）减少幻觉</font>

:::color5
**<font style="color:#601BDE;">9.代码实现</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

# 加载模型
model = AutoModelForCausalLM.from_pretrained("qwen-vl-chat", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("qwen-vl-chat")

# 处理输入
image = Image.open("cat.jpg").convert("RGB")
text = "<img>cat.jpg</img> 描述图中的猫的位置，用检测框表示。"

# 生成输出
inputs = tokenizer(text, images=image, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0]))

# 输出示例：
# <box>(253,156,398,290)</box> 图中有一只橘色猫坐在窗台上，面向窗外。

```

## InternVL系列
### InternVL 3.5
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(25, 27, 31);">现状挑战：</font>**<font style="color:rgb(25, 27, 31);">当前开源多模态大语言模型（MLLMs）在推理能力、计算效率上与商业模型（如 GPT-5）存在显著差距，且多模态能力增强常伴随计算成本激增。</font>
+ **<font style="color:rgb(25, 27, 31);">研究目标：</font>**<font style="color:rgb(25, 27, 31);">推出 InternVL3.5，通过创新技术解决</font>**<font style="color:#117CEE;">「通用性不足、推理弱、效率低」</font>**<font style="color:rgb(25, 27, 31);">三大痛点，缩小与商业模型的性能差距。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternVL3.5 是上海 AI 实验室推出的开源多模态模型家族，核心目标是提升模型的通用性、推理能力与推理效率。其关键创新包括：</font>[**<font style="color:#ED740C;">Cascade Reinforcement Learning</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=Cascade+Reinforcement+Learning&zhida_source=entity)**<font style="color:#ED740C;">（Cascade RL）、Visual Resolution Router（ViR）、Decoupled Vision-Language Deployment（DvD）</font>**<font style="color:rgb(25, 27, 31);">。模型覆盖 1B 到 241B 参数规模，新增GUI 交互、具身智能、SVG 理解与生成等能力。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**https://github.com/OpenGVLab/InternVL**](https://github.com/OpenGVLab/InternVL)

**paper：**[**https://arxiv.org/pdf/2508.18265**](https://arxiv.org/pdf/2508.18265)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029427608-75cc8a07-aa05-47ea-ab62-c04d1ef879f5.png)

> 总体架构。InternVL3.5与之前的版本一样采用“ViT-MLP-LLM”范式。在InternVL3.5的基础上，我们进一步介绍了InternVL3.5-Flash，对每个patch，它扩展了额外的视觉分辨率路由器（ViR）动态选择适当的压缩率（例如，1/4或1/16）。与仅从图像宽度角度分割图像块的动态高分辨率不同，我们提出的ViR从语义内容的角度进一步引入了自适应性。
>

:::color5
**<font style="color:#601BDE;">1.关键架构优化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">动态高分辨率策略：</font>**<font style="color:rgb(25, 27, 31);">延续 InternVL1.5 设计，支持 1:1/1:2/1:3 等预设宽高比，适配不同图像输入。</font>
2. **<font style="color:rgb(25, 27, 31);">ViR 模块（仅 Flash 版）：</font>**<font style="color:rgb(25, 27, 31);">通过「语义 richness 评估」为每个图像 patch 选择压缩率（1/4→256 token，1/16→64 token），减少视觉 token 数量。</font>

:::color5
**<font style="color:#601BDE;">2.级联强化学习（Cascade RL）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029970182-26f70284-4c67-4eb8-b7ad-e0c10324f811.png)

> InternVL3.5的训练食谱。InternVL3.5包括三个培训阶段：（1）native pretraining 用于视觉语言对齐，（2）SFT 以适应下游任务，（3）Cascade RL以提高推理能力。InternVL3.5-Flash是InternVL3.5的高效版本通过一致性训练和路由器训练进一步集成视觉分辨率路由器（ViR）。
>

<font style="color:rgb(25, 27, 31);">Cascade RL 旨在结合离线强化学习（RL）和在线 RL 的优势，解决单一 RL 范式在多模态大语言模型（MLLMs）中面临的效率和稳定性问题。其实现分为两个关键阶段：</font>

1. **<font style="color:rgb(25, 27, 31);">离线阶段（使用 </font>**[**<font style="color:rgb(9, 64, 142);">MPO 算法</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=MPO+%E7%AE%97%E6%B3%95&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">：利用 MMPR-v1.2 数据集（包含 200K 样本对）进行训练，计算损失函数为偏好损失（DPO）、质量损失（BCO）和生成损失（LM）的加权和，公式表示为</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029919600-0de007b4-b7ae-4be6-ab0c-5ef768f10e5c.png)

<font style="color:rgb(25, 27, 31);">在此阶段，模型能够快速收敛至一个满意的性能水平，为在线阶段提供高质量的 rollout 数据。</font>

2. **<font style="color:rgb(25, 27, 31);">在线阶段（使用 </font>**[**<font style="color:rgb(9, 64, 142);">GSPO 算法</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=GSPO+%E7%AE%97%E6%B3%95&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">：基于 MMPR-Tiny 数据集（包含 70K 查询，筛选自模型准确率在 0.2-0.8 之间的样本），通过归一化奖励计算优势函数，公式为</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029942337-4a119e16-455f-49bf-970b-3480551e2342.png)

<font style="color:rgb(25, 27, 31);">GSPO 算法无需参考模型的约束，能够有效提升模型的推理上限，并且适用于 dense 和 MoE 两种模型架构。通过 Cascade RL，InternVL3.5 全规模模型的推理性能得到显著提升。例如，InternVL3.5-2B 模型在推理任务中的得分从 SFT 后的 38.5 分提升至 50.7 分，提升幅度达到 + 12.2%，充分展示了该技术在增强模型推理能力方面的有效性。</font>

:::color5
**<font style="color:#601BDE;">3.视觉分辨率路由（ViR）与 视觉一致性训练（</font>**[**<font style="color:#601BDE;">ViCO</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=ViCO&zhida_source=entity)**<font style="color:#601BDE;">）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">ViR 的核心目标是在不损失模型性能的前提下，减少视觉 token 的数量，从而降低推理成本。为实现这一目标，ViCO 训练过程分为两个阶段：</font>

1. **<font style="color:rgb(25, 27, 31);">一致性训练</font>**<font style="color:rgb(25, 27, 31);">：冻结参考模型（InternVL3.5），通过最小化不同压缩率（1/4 或 1/16）视觉 token 的输出分布差异来进行训练，差异度量使用 KL 散度。此阶段确保模型在不同分辨率下的输出一致性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030121907-d2416523-7bd5-4564-a9d3-0b5d2ec46c50.png)

2. **<font style="color:rgb(25, 27, 31);">路由器训练</font>**<font style="color:rgb(25, 27, 31);">：将 ViR 视为一个二分类器，通过交叉熵损失进行训练。基于压缩前后损失比</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030144855-1dd3f4c4-43ea-4587-b3f5-61e4b7323231.png)

<font style="color:rgb(25, 27, 31);">来标注标签。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030168012-f41047fe-13eb-4f1d-9709-f0f21b24446f.png)<font style="color:rgb(25, 27, 31);">  
</font>

<font style="color:rgb(25, 27, 31);">实验结果表明，集成 ViR 的 InternVL3.5-Flash 系列模型能够减少 50% 的视觉 token，同时在 DocVQA、InfoVQA 等任务上性能保留率达到 99% 以上。例如，8B 模型在 DocVQA 任务中的得分，采用 ViR 前后分别为 91.9 分和 92.3 分，几乎无性能损失，验证了 ViR 技术在提升模型推理效率方面的可行性。</font>

:::color5
**<font style="color:#601BDE;">4.解耦的视觉语言部署（DvD）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">传统的视觉 - 语言模型部署方式中，视觉编码器（通常具有并行计算特性）与语言模型（自回归计算）串行执行，容易导致资源阻塞，降低推理效率。DvD 技术通过以下方式优化部署架构：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030220913-d9829c02-7055-4275-8126-c76811445712.png)<font style="color:rgb(25, 27, 31);"></font>

1. **<font style="color:rgb(25, 27, 31);">分离部署</font>**<font style="color:rgb(25, 27, 31);">：将视觉服务器（包含 ViT、MLP 和 ViR 模块）和语言服务器（仅运行 LLM）分离，视觉服务器处理图像并生成 BF16 特征，通过 TCP/RDMA 协议传输至语言服务器。</font>
2. **<font style="color:rgb(25, 27, 31);">流水线优化</font>**<font style="color:rgb(25, 27, 31);">：采用异步并行的方式处理视觉处理、特征传输和语言解码过程，减少处理过程中的 stalls，提高整体推理效率。在实际应用中，单 DvD 技术可实现 1.87-2.01 倍的加速效果，当与 ViR 结合时，加速效果最高可达 4.05 倍。以 38B 模型在 896 分辨率下为例，推理吞吐量从 2.71 req/s 提升至 10.97 req/s，充分证明了 DvD 在提升模型推理效率方面的显著优势。</font>

:::color5
**<font style="color:#601BDE;">5.模型架构设计</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">InternVL3.5 延续了 “ViT–MLP–LLM” 的基础范式，并针对不同的应用场景和资源需求，设计了多样化的模型架构，涵盖 dense 和 MoE 两种类型，具体如下：</font>

1. **<font style="color:#117CEE;">Dense 模型系列</font>**
    1. **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：提供两种选择，分别是适用于轻量级模型的 </font>[<font style="color:rgb(9, 64, 142);">InternViT-300M</font>](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=InternViT-300M&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和适用于大规模模型的 </font>[<font style="color:rgb(9, 64, 142);">InternViT-6B</font>](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=InternViT-6B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。InternViT-300M 具有较低的计算成本，适合在资源受限的环境中运行；InternViT-6B 则能够处理更复杂的视觉信息，为大型模型提供更强大的视觉特征提取能力。</font>
    2. **<font style="color:rgb(25, 27, 31);">语言模型</font>**<font style="color:rgb(25, 27, 31);">：基于 </font>[<font style="color:rgb(9, 64, 142);">Qwen3</font>](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=Qwen3&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 系列构建，包括 Qwen3-0.6B、Qwen3-1.7B、Qwen3-4B、Qwen3-8B、Qwen3-14B 和 Qwen3-32B 等不同参数规模的模型。这些语言模型在自然语言处理方面具有良好的基础性能，与视觉编码器协同工作，实现多模态信息的融合和处理。</font>
2. **<font style="color:#117CEE;">MoE 模型系列</font>**
    1. **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：同样采用 InternViT-300M 或 InternViT-6B，根据模型规模和性能需求进行选择。</font>
    2. **<font style="color:rgb(25, 27, 31);">语言模型</font>**<font style="color:rgb(25, 27, 31);">：使用具有混合专家（MoE）架构的模型，如 Qwen3-20B-A4B、Qwen3-30B-A3B 和 Qwen3-235B-A22B 等。MoE 架构通过动态路由机制，能够在不同的输入情况下选择最合适的专家模块进行处理，有效提高模型的表达能力和计算效率，尤其适用于处理大规模、复杂的多模态数据。</font>
3. **<font style="color:#117CEE;">高效变体：InternVL3.5-Flash</font>**

<font style="color:rgb(25, 27, 31);">针对资源受限的场景，InternVL3.5 推出了高效变体 InternVL3.5-Flash。该系列模型在原有架构的基础上集成了 ViR 模块，通过动态调整视觉 token 的分辨率，在减少视觉 token 数量的同时保持模型性能。这种设计使得模型能够在低资源环境下实现高效推理，拓宽了模型的应用范围。</font>

:::color5
**<font style="color:#601BDE;">6.训练流程与数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">InternVL3.5 的训练流程经过精心设计，包括预训练、监督微调（SFT）、Cascade RL 和 ViCO（仅针对 Flash 版）等多个阶段，每个阶段都使用特定的数据和目标来逐步提升模型的性能：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029970182-26f70284-4c67-4eb8-b7ad-e0c10324f811.png)

> InternVL3.5的训练食谱。InternVL3.5包括三个培训阶段：（1）native pretraining 用于视觉语言对齐，（2）SFT 以适应下游任务，（3）Cascade RL以提高推理能力。InternVL3.5-Flash是InternVL3.5的高效版本通过一致性训练和路由器训练进一步集成视觉分辨率路由器（ViR）。
>

1. **<font style="color:rgb(25, 27, 31);">预训练阶段</font>**<font style="color:rgb(25, 27, 31);">：使用 116M 样本（总计 250B tokens）进行训练，数据包括纯文本语料库以及图像 - 文本对、视频 - 文本对等多模态数据。训练目标是实现视觉 - 语言的基础对齐，通过最小化 next token prediction（NTP）损失，并采用 square averaging 加权策略来平衡不同模态数据的贡献。此外，为增强模型的鲁棒性，训练过程中对图像数据进行随机 JPEG 压缩处理。</font>
2. **<font style="color:rgb(25, 27, 31);">监督微调（SFT）阶段</font>**<font style="color:rgb(25, 27, 31);">：利用 56M 样本（130B tokens）进行微调，数据中加入了更多的推理数据（采用 Thinking 模式）以及新能力相关数据，如 GUI、具身智能、SVG 等方面的数据。此阶段旨在使模型更好地适应各种实际任务，提升模型对用户指令的理解和执行能力。</font>
3. **<font style="color:rgb(25, 27, 31);">Cascade RL 阶段</font>**<font style="color:rgb(25, 27, 31);">：离线阶段使用 MPO 算法，基于 MMPR-v1.2 数据集（200K 样本）进行训练，快速提升模型性能并使其达到稳定状态；在线阶段采用 GSPO 算法，利用 MMPR-Tiny 数据集（70K 查询）进一步优化模型，突破推理性能上限。</font>
4. **<font style="color:rgb(25, 27, 31);">ViCO 阶段（仅 Flash 版）</font>**<font style="color:rgb(25, 27, 31);">：基于 SFT 数据的子集（主要包含 OCR 和 VQA 相关数据）进行训练，通过一致性训练和路由器训练两个步骤，使 ViR 模块能够准确地为每个图像 patch 选择合适的压缩率，同时保持模型在压缩后的性能一致性。  
</font><font style="color:rgb(25, 27, 31);">通过这一系列的训练流程，InternVL3.5 能够充分利用多样化的数据，逐步提升模型在多模态任务中的性能和泛化能力，成为一个功能强大且适应性广泛的多模态模型家族。</font>

:::color5
**<font style="color:#601BDE;">7.总结</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:#117CEE;">关键结论</font>**
    - <font style="color:rgb(25, 27, 31);">推理能力开源领先：Cascade RL 使 InternVL3.5 全规模模型推理性能提升 10-16%，旗舰模型成为开源推理能力最强的 MLLM。</font>
    - <font style="color:rgb(25, 27, 31);">效率与性能兼顾：ViR+DvD 实现 4.05× 推理加速，且性能无损，适配高分辨率、多图像等复杂场景。</font>
    - <font style="color:rgb(25, 27, 31);">通用性覆盖广泛：新增 GUI、具身、SVG 能力，文本任务性能接近商业模型，成为 “全场景适配” 的开源多模态模型。</font>
2. **<font style="color:#117CEE;">未来方向</font>**
    - <font style="color:rgb(25, 27, 31);">进一步优化幻觉抑制能力，减少多模态生成中的事实性错误。</font>
    - <font style="color:rgb(25, 27, 31);">扩展更长的视觉上下文（如超长篇视频理解），提升复杂场景适配性。</font>
    - <font style="color:rgb(25, 27, 31);">深化多语言多模态能力，覆盖更多小语种的跨模态任务。</font>

### InternVL 2.5<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">InternVL系列的目标是缩小商业闭源模型与开源多模态模型之间的性能差距。在InternVL 2.5中，他们系统地探索了多模态大模型中的各种因素，包括</font>[<font style="color:rgb(9, 64, 142);">视觉编码器</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、语言模型、</font>[<font style="color:rgb(9, 64, 142);">数据集规模</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A7%84%E6%A8%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和推理时间的变化如何影响模型的整体性能，从而展示了多模态模型中扩展与性能之间的关系。研究人员有一些有趣的发现：</font>

1. **<font style="color:rgb(25, 27, 31);">大型视觉编码器的优势</font>**<font style="color:rgb(25, 27, 31);">：大型视觉编码器在扩展多模态大模型时显著减少了对训练数据的依赖。与配备600M视觉编码器的Qwen2-VL-72B相比，InternVL2.5-78B配备了6B的视觉编码器，仅使用1/10的训练token就能实现更好的性能。这大大降低了扩展多模态大模型时的探索成本。</font>
2. **<font style="color:rgb(25, 27, 31);">数据质量的重要性</font>**<font style="color:rgb(25, 27, 31);">：从InternVL 2.0升级到2.5时，数据集规模增加了一倍，但严格的过滤大大提高了数据质量。例如，研究人员仔细排除了异常样本（如重复模式），在</font>[<font style="color:rgb(9, 64, 142);">链式推理</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E9%93%BE%E5%BC%8F%E6%8E%A8%E7%90%86&zhida_source=entity)<font style="color:rgb(25, 27, 31);">任务（如MMMU）和复杂挑战（如OlympiadBench）中取得了显著的改进。值得注意的是，大多数现有的开源多模态大模型在使用链式推理时表现不佳。</font>
3. **<font style="color:rgb(25, 27, 31);">测试时扩展的益处</font>**<font style="color:rgb(25, 27, 31);">：对于困难的多模态问答任务，测试时扩展是有益的。在像MMMU这样的挑战性任务中，InternVL2.5-78B结合链式推理达到了70.1%的准确率，比直接响应高出3.7个百分点。随后，研究人员成功验证了链式推理可以进一步与多数投票结合，带来额外的改进。</font>

:::

:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">InternVL 2.5</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=InternVL+2.5&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，这是一种先进的大规模多模态大模型系列，基于InternVL 2.0的基础架构。InternVL系列的目标是缩小商业闭源模型与开源多模态模型之间的性能差距。在InternVL 2.5中，他们系统地探索了多模态大模型中的各种因素，包括</font>[<font style="color:rgb(9, 64, 142);">视觉编码器</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、语言模型、</font>[<font style="color:rgb(9, 64, 142);">数据集规模</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A7%84%E6%A8%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和推理时间的变化如何影响模型的整体性能，从而展示了多模态模型中扩展与性能之间的关系。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**https://zhuanlan.zhihu.com/p/12309812997**](https://zhuanlan.zhihu.com/p/12309812997)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742539773591-7e23e6f7-d565-4b0f-9cdb-02bf4a7a0e41.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">加上了</font>**<font style="color:rgb(25, 27, 31);">stage 1.5</font>**<font style="color:rgb(25, 27, 31);">，专门用来训练ViT， 使其对chart等数据表现更好，ViT是和较小的LLm一起训练直接沿用到较大的LLM，节省了训练时间。</font>
2. <font style="color:rgb(25, 27, 31);">随机图像压缩，使模型能够适应图像噪声。</font>
3. <font style="color:rgb(25, 27, 31);">损失函数取了token average和sample average的tradeoff，避免响应长度对最终结果的影响。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **预训练数据**

<font style="color:rgb(25, 27, 31);">为了全面提升模型的性能并增强其处理复杂任务的能力，InternVL 2.5的训练数据集比InternVL 1.5和2.0更广泛且多样化。模型开发期间，专门使用对话格式的指令数据。在这一阶段，由于只有MLP或MLP和ViT的参数是可训练的，因此会</font>**<font style="color:rgb(25, 27, 31);">结合高质量和低质量的数据。</font>**<font style="color:rgb(25, 27, 31);">目标是通过接触多样的领域数据来丰富模型的世界知识，从而提高其泛化能力。训练语料库涵盖了</font>**<font style="color:#74B602;">字幕生成、通用问答、数学、图表、OCR、知识、定位、文档、对话、医疗和GUI任务等领域。</font>**

2. **<font style="color:rgb(25, 27, 31);">微调数据</font>**

<font style="color:rgb(25, 27, 31);">从InternVL 1.5到2.0再到2.5，数据集在规模、质量和多样性上进行了迭代改进。数据规模方面，样本数量从InternVL 1.5的510万增长到InternVL 2.0的730万，并在InternVL 2.5中进一步翻倍至</font>**<font style="color:#74B602;">1630万</font>**<font style="color:rgb(25, 27, 31);">。在多样性方面，训练数据涵盖多个领域，包括</font>**<font style="color:#74B602;">通用问答、图表、文档、OCR、科学、医疗、GUI、代码、数学等，同时覆盖多种模态，如单图像、多图像、视频和文本。</font>**

<font style="color:rgb(25, 27, 31);">在InternVL 2.5中，</font>**<font style="color:#74B602;">单图像数据占据了45.92%的标记，多图像数据占9.37%，视频数据贡献了39.79%，纯文本数据占4.92%</font>**<font style="color:rgb(25, 27, 31);">。与早期版本相比，多图像和视频数据的增加最为显著，增强了InternVL 2.5对多图像和长视频的理解能力。质量提升通过统一对话模板、使用语言模型评分和精炼数据、去除重复模式、应用启发式规则过滤低质量样本，以及将短响应重写为高质量和更长的交互来实现。这确保了模型训练的稳健数据集。</font>

3. **数据处理pipeline**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742720896544-874e4e03-d4d1-4892-b359-9c4e86630891.png)

<font style="color:rgb(25, 27, 31);">在模型开发过程中，观察到</font>**<font style="color:#74B602;">LLM对数据噪声的敏感性显著高于视觉编码器</font>**<font style="color:rgb(25, 27, 31);">。即使是少量异常样本（例如，离群值或重复数据，仅数千个）也会在推理期间导致模型行为异常。</font>

<font style="color:rgb(25, 27, 31);">在这些异常中，</font>**<font style="color:#74B602;">重复生成</font>**<font style="color:rgb(25, 27, 31);">被识别为最具破坏性的问题之一。在许多开源或合成数据集中，仅仅数千个重复样本就会导致模型陷入重复循环，尤其是在长篇输出或CoT推理任务中。这种现象削弱了测试时缩放策略的有效性。为应对这一挑战并支持未来研究，我们设计了一种高效的数据过滤管道，以去除低质量样本，从而最大限度地减少重复生成的风险。</font>

**<font style="color:rgb(25, 27, 31);">数据过滤pipeline</font>**<font style="color:rgb(25, 27, 31);">：由两个模块组成。对于纯文本数据，实施了三种关键策略：</font>

1. **<font style="color:rgb(25, 27, 31);">基于LLM的质量评分</font>**<font style="color:rgb(25, 27, 31);">：首先将数据集分类为不同领域，低于指定阈值的样本被移除以确保数据质量。</font>
2. **<font style="color:rgb(25, 27, 31);">重复检测</font>**<font style="color:rgb(25, 27, 31);">：使用LLM结合特定提示识别重复样本。这些样本经过人工审查，低于阈值的样本被移除以保持数据质量。</font>
3. **<font style="color:rgb(25, 27, 31);">启发式规则过滤</font>**<font style="color:rgb(25, 27, 31);">：应用特定规则，如过滤掉异常长度的句子、过长的零序列、过多重复行的文本等，以识别数据中的异常。尽管这种方法可能偶尔产生误报，但它提高了异常样本的检测率。所有标记样本在最终移除前都经过人工审查。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">InternVL 2.5 延续了其前身 InternVL 1.5 和 InternVL 2.0 的模型架构，采用了广泛应用于多模态大语言模型研究中的</font>**<font style="color:#74B602;">“ViT-MLP-LLM”范式</font>**<font style="color:rgb(25, 27, 31);">。</font>

1. **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**

<font style="color:rgb(25, 27, 31);">InternVL 使用 InternViT 作为视觉编码器，当前有两种不同的模型尺寸：InternViT-6B 和 InternViT-300M。</font>

+ **<font style="color:rgb(25, 27, 31);">InternViT-6B</font>**<font style="color:rgb(25, 27, 31);">：最初在 CVPR 论文中引入，采用了基础 ViT 架构，进行了少量调整，如引入了 </font>**<font style="color:#74B602;">QK-Norm 和 RMSNorm</font>**<font style="color:rgb(25, 27, 31);">。该模型有 5.9B 参数，48 层，隐藏层大小为 3200，25 个头，并使用对比损失进行训练。为了不断优化其权重，采用了增量预训练策略，</font>**<font style="color:#74B602;">通过 MLP 投影器将 InternViT-6B 连接到语言模型</font>**<font style="color:rgb(25, 27, 31);">，并使用下一个标记预测损失进行联合训练，以增强其视觉特征提取能力。在后续版本中，采用了动态分辨率训练来提高高分辨率处理能力。</font>
+ **<font style="color:rgb(25, 27, 31);">InternViT-300M</font>**<font style="color:rgb(25, 27, 31);">：这是一个蒸馏变体，使用余弦蒸馏损失，包含 0.3B 参数，24 层，隐藏层大小为 1024，16 个注意力头。与 6B 版本不同，0.3B 版本使用标准 LayerNorm，而不是 QK-Norm。经过蒸馏后，该模型与语言模型集成，并通过动态高分辨率和 </font>[<font style="color:rgb(9, 64, 142);">NTP 损失</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=NTP+%E6%8D%9F%E5%A4%B1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">训练视觉编码器。</font>
2. **<font style="color:rgb(25, 27, 31);">大语言模型</font>**

<font style="color:rgb(25, 27, 31);">InternVL 系列中使用的语言模型包括 InternLM 2、Qwen 2、Phi 3、Yi 和 Llama 3。为了实现更好的性能，InternVL 2.5 系列全面升级了语言模型骨干，采用了最新的先进模型，如</font>**<font style="color:#74B602;"> InternLM 2.5 和 Qwen 2.5</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742720683356-162dbf4f-db1e-4cb8-bc02-8ac81eced6f5.png)

1. **<font style="color:rgb(25, 27, 31);">阶段1：MLP预热</font>**

<font style="color:rgb(25, 27, 31);">在这一阶段，首先对</font>**<font style="color:#74B602;">MLP投影器进行预热训练</font>**<font style="color:rgb(25, 27, 31);">。MLP投影器是视觉和语言表示之间的初始桥梁。在此阶段，仅训练MLP投影器，而视觉编码器（InternViT）和语言模型保持冻结状态。尽管这种动态高分辨率训练策略增加了训练成本，但它有助于实现最佳性能。在这一阶段，使用预训练数据混合，并采用NTP损失进行优化。应用较高的学习率以加速收敛，使MLP能够快速适应LLM的输入空间，并建立稳健的跨模态对齐。MLP预热阶段确保模型在解锁后续阶段的可训练组件之前，能够良好地处理多模态任务，从而提高训练稳定性。</font>

1. **<font style="color:rgb(25, 27, 31);">阶段1.5：ViT增量学习（可选）</font>**

<font style="color:rgb(25, 27, 31);">阶段1.5为视觉编码器引入增量学习。在这一阶段，</font>**<font style="color:#74B602;">视觉编码器和MLP投影器均可训练</font>**<font style="color:rgb(25, 27, 31);">，训练使用与阶段1相同的预训练数据混合和NTP损失。此阶段的目标是增强视觉编码器提取视觉特征的能力，使其能够捕捉更全面的信息，</font>**<font style="color:rgb(25, 27, 31);">尤其是针对那些在大规模网络数据集中相对稀缺的领域，如多语言OCR数据和数学图表等</font>**<font style="color:rgb(25, 27, 31);">。使用较低的学习率以防止灾难性遗忘，确保编码器不会丧失先前学到的能力。</font>**<font style="color:rgb(25, 27, 31);">视觉编码器一旦训练完成，可以与不同的LLM重复使用，无需重新训练</font>**<font style="color:rgb(25, 27, 31);">，这使得阶段1.5成为可选。这在编码器已经为某些特定任务优化时尤为有利，允许其与各种大小的LLM集成，而无需显著增加成本。</font>

1. **<font style="color:rgb(25, 27, 31);">阶段2：全模型指令微调</font>**

<font style="color:rgb(25, 27, 31);">在最终阶段，整个模型（包括ViT、MLP和LLM）在高质量的多模态指令数据集上进行训练。此时，数据质量尤为重要，因为负责生成最终用户输出的LLM现在是可训练的。</font>**<font style="color:rgb(25, 27, 31);">即使少量的噪声数据（如几千个样本）也可能导致模型行为异常，如输出重复或产生特定错误结果</font>**<font style="color:rgb(25, 27, 31);">。为减轻LLM的退化，在这一阶段实施严格的数据质量控制。此外，此阶段的训练超参数保持简单，对整个模型应用统一的学习率，而不是对不同组件使用不同的学习率。完成此阶段后，InternVL 2.5的完整训练过程即告结束。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

<font style="color:rgb(25, 27, 31);">基本上在各个benchmark上，8B就能和GPT-4o的效果媲美。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742721084444-6f390d10-507d-498a-84b9-d714dfa0dad4.png)

<font style="color:rgb(25, 27, 31);">在真实场景的数据集上效果也不错，在我们的</font>[MME-RealWorld](https://link.zhihu.com/?target=https%3A//mme-realworld.github.io/home_page.html)<font style="color:rgb(25, 27, 31);">中8B超过了Qwen2-VL与LLaVA-OV同等量级的模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742721124147-e89b9552-ec46-49dc-b003-34fe9fb78b9f.png)

<font style="color:rgb(25, 27, 31);">COT对reasoning的影响：新一版的26B模型在CoT的效果上更好。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742721139524-f54f189f-93b4-453a-8080-d62a1fac0927.png)

### InternVL 2<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternVL2，强大的开源多模态大型语言模型（MLLM）。</font>**<font style="color:rgb(25, 27, 31);">InternVL2家族包括从适合边缘设备的2B模型到更为强大的108B模型。</font>**<font style="color:rgb(25, 27, 31);">随着更大规模语言模型的引入，InternVL2-Pro展示了出色的多模态理解能力，在各种基准测试中与商业闭源模型的性能相匹配。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742539773591-7e23e6f7-d565-4b0f-9cdb-02bf4a7a0e41.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">逐步采用更大规模的语言模型</font>**<font style="color:rgb(25, 27, 31);">：我们引入了一种逐步对齐训练策略，产生了第一个与大型语言模型原生对齐的视觉基础模型。</font>**<font style="color:rgb(25, 27, 31);">通过采用逐步训练策略，模型从小规模逐步扩展到大规模，同时数据从粗糙逐步精细化，我们以相对较低的成本完成了大规模模型的训练</font>**<font style="color:rgb(25, 27, 31);">。这种方法在资源有限的情况下展现了出色的性能。</font>
+ **<font style="color:rgb(25, 27, 31);">多模态输入</font>**<font style="color:rgb(25, 27, 31);">：我们的模型通过一组参数</font>**<font style="color:rgb(25, 27, 31);">支持多种输入模态</font>**<font style="color:rgb(25, 27, 31);">，包括文本、图像、视频和医疗数据。</font>
+ **<font style="color:rgb(25, 27, 31);">多任务输出</font>**<font style="color:rgb(25, 27, 31);">：得益于我们最近的工作</font>[<font style="color:rgb(9, 64, 142);">VisionLLMv2</font>](https://zhida.zhihu.com/search?content_id=244561702&content_type=Article&match_order=1&q=VisionLLMv2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，我们的模型</font>**<font style="color:rgb(25, 27, 31);">支持多种输出格式，如图像、边界框和掩码，展现了广泛的通用性</font>**<font style="color:rgb(25, 27, 31);">。通过将MLLM与多个下游任务解码器连接，InternVL2可以泛化到数百个视觉-语言任务，同时达到与专家模型相当的性能。</font>

:::color5
**<font style="color:#601BDE;">2.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">阶段1：预训练</font>**

<font style="color:rgb(25, 27, 31);">在InternVL 1.5中使用的预训练数据集扩展了从多种来源收集的数据。</font>**<font style="color:rgb(25, 27, 31);">这些数据集覆盖了多个任务，包括标题生成、视觉问答、检测、定位和OCR。</font>**<font style="color:rgb(25, 27, 31);">OCR数据集是使用PaddleOCR对来自Wukong的中文图像和来自LaionCOCO的英文图像进行OCR构建的，并经过人工验证。此外，我们还爬取了来自uworld、kaptest、testbank、aga和sat的考试数据，并进行了人工解析。还利用了来自OmniCorpus的交错数据。</font>

2. **<font style="color:rgb(25, 27, 31);">阶段2：微调</font>**

<font style="color:rgb(25, 27, 31);">基于InternVL 1.5中使用的500万高质量双语数据集构建了训练数据。具体来说，我们包括了诸如EgoTaskQA、Mementos、STAR、NTU RGB+D、VideoChat2IT和LSMDC-QA这样的</font>**<font style="color:rgb(25, 27, 31);">视频数据</font>**<font style="color:rgb(25, 27, 31);">，以及Medical-Diff-VQA、Pathology-VQA、PMC-CaseReport、PMC-VQA、Slake和VQA-RAD这样的</font>**<font style="color:rgb(25, 27, 31);">医疗数据</font>**<font style="color:rgb(25, 27, 31);">。我们还包括了SROIE、FUNSD和POIE，以</font>**<font style="color:rgb(25, 27, 31);">进一步增强模型识别手写字体的能力</font>**<font style="color:rgb(25, 27, 31);">。此外，我们排除了来自ShareGPT-4V的所有数据，并用来自ShareGPT-4o的数据替换。</font>

:::color5
**<font style="color:#601BDE;">3.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742539863216-dac72ce1-0dc9-4067-a9be-f4f195bbd92c.png)

### InternVL 1.5<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);"> InternVL 1.5，一个</font>**<font style="color:#ED740C;">旨在缩小与商业多模态模型能力差距</font>**<font style="color:rgb(25, 27, 31);">的开源多模态大型语言模型（MLLM）。该模型通过三个主要改进来增强其性能：</font>**<font style="color:#ED740C;">强大的视觉编码器、动态高分辨率处理和高质量的双语数据集</font>**<font style="color:rgb(25, 27, 31);">。这些改进使得 InternVL 1.5 在视觉理解和语言处理方面表现出色，特别是在处理高分辨率图像和多模态任务时。</font>

**paper：**[**https://arxiv.org/pdf/2404.16821**](https://arxiv.org/pdf/2404.16821)<font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**书生·万象多模态大模型（InternVL）系列**](https://zhuanlan.zhihu.com/p/703940563)**  **[**InternVL1.5 解读**](https://zhuanlan.zhihu.com/p/703135536)** **[**Intern-VL 动态分辨率代码**](https://zhuanlan.zhihu.com/p/14202602450)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537624418-3e85701e-2b23-47d2-a1cf-d42533b6b26c.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">强视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：我们为大规模视觉基础模型</font>[<font style="color:rgb(9, 64, 142);">InternViT-6B</font>](https://zhida.zhihu.com/search?content_id=244382861&content_type=Article&match_order=1&q=InternViT-6B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">探索了一种持续学习策略，提高了其视觉理解能力，并使其可以在不同的大语言模型中迁移。</font>
2. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">动态高分辨率</font>**<font style="color:rgb(25, 27, 31);">：根据输入图像的长宽比和分辨率，将图像划分为1到40个448×448像素的图块，最高支持4K分辨率输入。</font>
3. **<font style="color:rgb(25, 27, 31);">高质量的双语数据集</font>**<font style="color:rgb(25, 27, 31);">：我们精心收集了</font>**<font style="color:#74B602;">高质量的双语数据集</font>**<font style="color:rgb(25, 27, 31);">，涵盖常见场景、文档图像，并用英文和中文问答对对其进行注释，显着提高了 OCR 和中文相关任务的性能。</font>

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **预训练数据**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537788003-9c17b288-6ec0-4829-bb57-9522be155104.png)

2. **微调数据**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537796140-04924915-98c4-4f7b-983d-af7ee2e4f020.png)

3. **语料翻译pipeline（英译中）**<font style="color:#D22D8D;">（by草莓师姐）</font>

```python
System：
你是一名精通英语和{语言}的翻译。你的任务是将以下英文文本翻译成{语言}，注重自然流畅的结果，避免“翻译”。请考虑以下几点：
1.保留英文专有名词、品牌和地名。
2.保留英文技术术语或行话，但必要时用{语言}解释。
3.使用{语言}习语表达英语习语或谚语，以确保文化相关性。
4.确保引用或直接讲话在{语言}中听起来很自然，保持原作的基调。
5.对于缩略语，请提供{语言}的完整形式，并附上括号内为英文首字母缩写。
User：
翻译文本：{Text}
Assistant：
{翻译结果}
```

:::color5
**<font style="color:#601BDE;">2.动态分辨率  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">动态分辨率：</font>**<font style="color:rgb(25, 27, 31);">训练图像的分辨率从固定的 448×448 扩展到动态 448×448，其中patch大小为 448×448，patch数量范围为 1 到 12。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537741384-75721322-7fa4-4bca-97ce-e49a14ccff86.png)

1. **Pixel Shuffle**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">为了提高高分辨率下的可扩展性，我们简单地采用了</font>[**<font style="color:#74B602;">Pixel shuffle</font>**](https://zhida.zhihu.com/search?content_id=244382861&content_type=Article&match_order=1&q=Pixel+shuffle&zhida_source=entity)**<font style="color:#74B602;">操作，将视觉标记的数量减少到原来的四分之一</font>**<font style="color:rgb(25, 27, 31);">。因此，在我们的模型中，一幅 448×448 的图像由 256 个视觉标记表示。</font>

```python
def pixel_shuffle(self, x, scale_factor=0.5):
    n, w, h, c = x.size()
    # N, W, H, C --> N, W, H * scale, C // scale
    x = x.view(n, w, int(h * scale_factor), int(c / scale_factor))
    # N, W, H * scale, C // scale --> N, H * scale, W, C // scale
    x = x.permute(0, 2, 1, 3).contiguous()
    # N, H * scale, W, C // scale --> N, H * scale, W * scale, C // (scale ** 2)
    x = x.view(n, int(h * scale_factor), int(w * scale_factor),
               int(c / (scale_factor * scale_factor)))
    if self.ps_version == 'v1':
        warnings.warn("In ps_version 'v1', the height and width have not been swapped back, "
                      'which results in a transposed image.')
    else:
        x = x.permute(0, 2, 1, 3).contiguous()
    return x
```

2. **<font style="color:rgb(25, 27, 31);">动态宽高比匹配</font>**<font style="color:rgb(25, 27, 31);">：为了在处理过程中保持自然的宽高比，我们从一组预定义的宽高比中动态匹配最佳的宽高比。 由于计算资源有限，我们在训练期间</font>**<font style="color:#74B602;">最多允许 12 个patch</font>**<font style="color:rgb(25, 27, 31);">。 因此，该集合包括由 1 到 12 个patch形成的</font>**<font style="color:#74B602;">所有 35 种可能的宽高比组合，例如 {1:1、1:2、2:1、3:1、…、2:6}</font>**<font style="color:rgb(25, 27, 31);">。 在匹配过程中，对于每个输入图像，我们计算其纵横比，并通过</font>**<font style="color:#74B602;">测量绝对差将其与 35 个预定义的纵横比进行比较，选择最优宽高比</font>**<font style="color:rgb(25, 27, 31);">。 如果多个预定义的宽高比匹配(例如、1:1和2:2），我们会优先考虑不超过输入图像面积两倍的宽高比，从而防止低分辨率图像过度放大。</font><font style="color:#D22D8D;">（by草莓师姐）</font>
3. **<font style="color:rgb(25, 27, 31);">图像resize</font>**<font style="color:rgb(25, 27, 31);">：一旦确定了适当的宽高比，图像的大小就会调整为相应的分辨率。 </font>**<font style="color:#74B602;">例如，800×1300 图像将调整为 896×1344</font>**<font style="color:rgb(25, 27, 31);">。 </font>
4. **<font style="color:rgb(25, 27, 31);">图像patch</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">调整大小的图像被分成 448×448 像素的图块</font>**<font style="color:rgb(25, 27, 31);">。 除了图块之外，</font>**<font style="color:#74B602;">我们还包含整个图像的缩略图以捕获全局上下文。 该缩略图缩小至 448×448</font>**<font style="color:rgb(25, 27, 31);">，帮助模型理解整个场景。</font>

```python
def dynamic_preprocess(image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
    # 获取原始图像尺寸和计算宽高比 
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # 生成目标宽高比集合：根据给定的最小值 (min_num) 和最大值 (max_num)，生成所有可能的目标宽高比组合 (i, j)，
    # 其中 i * j 在 [min_num, max_num] 范围内
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    
    # 对这些宽高比组合按面积排序，即按 i * j 排序
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # 找到最接近原始宽高比的目标宽高比，这里调用了辅助函数 find_closest_aspect_ratio
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # 计算目标图像的宽度和高度，根据目标宽高比和ViT的原生输入分辨率 (image_size：448) ，
    # 计算目标图像的宽度 (target_width) 和高度 (target_height），以及切图后的子图（448*448）数量
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # 根据计算结果resize
    resized_img = image.resize((target_width, target_height))
    # 将调整后的图像按照目标宽高比分割成多个小块，并存储在列表
    processed_images = []
    # 与Intern-VL不同的是，我的模型还需要动态分辨率模块输出每个子图的相对位置编号
    pos = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
        # 子图所在相对位置
        pos.append(i // (target_width // image_size), i % (target_width // image_size))
    # 检查子图数量是否正确
    assert len(processed_images) == blocks

    # 如果设置了 use_thumbnail 为 True 并且分割后的小块数量不是 1，则将原始图像调整为ViT原生输入大小的缩略图并添加到最后一个小块后面。
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images, pos
```

```python
def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        # 比较宽高比：将输入图像的宽高比与预定义的宽高比进行比较。比较的标准是计算绝对差异，
        # 即找到最接近输入图像宽高比的预定义宽高比
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        # 如果有多个预定义的宽高比与输入图像的宽高比相匹配（例如，1:1 和 2:2），系统会优先选择一个宽高比，
        # 该比率不会导致图像面积扩大超过输入图像面积的两倍。这是为了避免对低分辨率图像进行过度放大。
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    # print(f'width: {width}, height: {height}, best_ratio: {best_ratio}')
    return best_ratio
```

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">InternVL 1.5采用了类似于流行MLLMs的</font>**<font style="color:#74B602;">ViT-MLP-LLM</font>**<font style="color:rgb(25, 27, 31);">架构，通过MLP投影器将预训练的InternViT-6B与InternLM2-20B结合。在这里，我们采用了一个简单的pixel shuffle方法，将视觉tokens的数量减少到四分之一。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537624418-3e85701e-2b23-47d2-a1cf-d42533b6b26c.png)

:::color5
**<font style="color:#601BDE;">4.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

InternVL 1.5与专有商业模型的比较。这些基准测试的结果显示，InternVL 1.5达到了与领先的专有模型相当的性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742538206069-82aed1dd-3c98-4be1-b422-7f38c5848c1c.png)



### InternVL<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">论文标题：《InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks》</font>

<font style="color:rgb(25, 27, 31);">比较不同视觉和视觉-语言基础模型的差异。如下图所示：</font>

+ <font style="color:rgb(25, 27, 31);">（a）表示传统的视觉基础模型，例如在分类任务上预训练的ResNet[57]。</font>
+ <font style="color:rgb(25, 27, 31);">（b）代表视觉-语言基础模型，例如在图像-文本对上预训练的</font>[<font style="color:rgb(9, 64, 142);">CLIP</font>](https://zhida.zhihu.com/search?content_id=244561702&content_type=Article&match_order=1&q=CLIP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">[117]。</font>
+ <font style="color:rgb(25, 27, 31);">（c）是提出的InternVL，它展示了一种将大规模视觉基础模型（即InternViT-6B）与大型语言模型对齐的可行方法，并且对于对比和生成任务都具有多功能性。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529081885-f82fc2fc-32f3-467b-b11e-9549bb8126a8.png)

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">该模型由南京大学、OpenGVLab、上海人工智能实验室等机构的研究人员共同开发。</font>**<font style="color:#ED740C;">InternVL 模型将视觉编码器扩展到 60 亿参数(6B)，并逐步与大型语言模型（LLM）对齐，使用来自各种来源的 web 规模的图像文本数据进行训练。该模型在 32 个通用视觉语言基准上取得了 state-of-the-art 的性能</font>**<font style="color:rgb(25, 27, 31);">，包括图像级别或像素级别识别、zero-shot图像/视频分类、zero-shot图像/视频-文本检索以及多模态对话系统。</font>

**paper：**[**https://arxiv.org/pdf/2312.14238**](https://arxiv.org/pdf/2312.14238)

**参考：**[**https://zhuanlan.zhihu.com/p/703940563**](https://zhuanlan.zhihu.com/p/703940563)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529165282-1dd01cee-99c1-413c-adee-cd756c084ceb.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">一是</font>**<font style="color:rgb(25, 27, 31);">参数平衡的视觉和语言组件</font>**<font style="color:rgb(25, 27, 31);">，包括一个 60 亿参数的视觉编码器</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">InternViT-6B</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和一个 80 亿参数的语言中间件</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">QLLaMA</font>**<font style="color:rgb(25, 27, 31);">；</font>
+ <font style="color:rgb(25, 27, 31);">二是</font>**<font style="color:rgb(25, 27, 31);">保持一致的表示</font>**<font style="color:rgb(25, 27, 31);">，通过使用预训练的多语言 LLaMA 来初始化中间件，并使视觉编码器与之对齐；</font>
+ <font style="color:rgb(25, 27, 31);">三是</font>**<font style="color:rgb(25, 27, 31);">采用渐进式图像文本对齐策略</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#74B602;">通过 contrastive 和 generative 学习阶段</font>**<font style="color:rgb(25, 27, 31);">，有效地利用了 web 规模的嘈杂图像文本数据。</font>

:::color5
**<font style="color:#601BDE;">2.训练方法：三阶段渐进训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529165282-1dd01cee-99c1-413c-adee-cd756c084ceb.png)

**<font style="color:#601BDE;">三个渐进阶段</font>**，包括**<font style="color:#74B602;">视觉-语言对比训练、视觉-语言生成训练和监督式微调</font>**。这些阶段有效地利用了来自不同来源的公开数据，从网络上嘈杂的图像-文本对到高质量的字幕、VQA和多模态对话数据集。

1. **<font style="color:rgb(25, 27, 31);">第一阶段，视觉-语言对比训练</font>**
    1. **<font style="color:rgb(25, 27, 31);">目的：</font>**<font style="color:rgb(25, 27, 31);">在Web规模的噪声图像-文本对上进行对比学习，以对齐InternViT-6B与多语言LLaMA-7B </font>
    2. **<font style="color:rgb(25, 27, 31);">数据：</font>**<font style="color:rgb(25, 27, 31);">LAION-en 、LAION-multi 、LAION-COCO、COYO [14]、Wukong等。</font>
    3. **<font style="color:rgb(25, 27, 31);">数据处理</font>**<font style="color:rgb(25, 27, 31);">：我们使用这些数据集的组合，</font>**<font style="color:#74B602;">并过滤掉一些极低质量的数据</font>**<font style="color:rgb(25, 27, 31);">来训练我们的模型。原始数据集包含60.3亿图像-文本对，清洗后剩下49.8亿。</font>
    4. **<font style="color:rgb(25, 27, 31);">训练方法（clip）</font>**<font style="color:rgb(25, 27, 31);">：图文对比学习</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529423737-9cb13306-e433-43d6-9400-8f03cdfb5b4b.png)

2. **<font style="color:rgb(25, 27, 31);">第二阶段，视觉-语言生成训练</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>
    1. **<font style="color:rgb(25, 27, 31);">目的</font>**<font style="color:rgb(25, 27, 31);">：保持InternViT-6B和QLLaMA冻结，训练cross attention 和 learnable queries。这使得</font>**<font style="color:#74B602;">查询能够提取强大的视觉表示，并进一步与大型语言模型（LLMs）对齐特征空间</font>**<font style="color:rgb(25, 27, 31);">，这得益于有效的训练目标和我们大规模、基于LLM初始化的QLLaMA的利用。</font>
    2. **<font style="color:rgb(25, 27, 31);">数据</font>**<font style="color:rgb(25, 27, 31);">：我们进一步过滤掉了低质量标题的数据，</font>**<font style="color:rgb(25, 27, 31);">从第一阶段的49.8亿减少到10.3亿</font>**<font style="color:rgb(25, 27, 31);">。</font>
    3. **<font style="color:rgb(25, 27, 31);">训练方法（blip2）：</font>**<font style="color:rgb(25, 27, 31);">遵循BLIP-2 的损失函数，这一阶段的损失计算为三个组件的总和：图像-文本对比（ITC）损失、图像-文本匹配（ITM）损失和基于图像的文本生成（ITG）损失。</font>
3. **<font style="color:rgb(25, 27, 31);">监督式微调</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    1. **<font style="color:rgb(25, 27, 31);">目的</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">通过仅训练MLP层或同时训练MLP层和QLLaMA来实现稳健的性能。</font>**<font style="color:rgb(25, 27, 31);">这种方法不仅加快了SFT过程，而且还保持了LLMs的原始语言能力。</font>
    2. **<font style="color:rgb(25, 27, 31);">数据</font>**<font style="color:rgb(25, 27, 31);">：收集了广泛的高质量指令数据，</font>**<font style="color:rgb(25, 27, 31);">总共约400万个样本</font>**
    3. **<font style="color:rgb(25, 27, 31);">训练方法：</font>**<font style="color:rgb(25, 27, 31);">通过一个多层感知器（MLP）层将其与现成的LLM解码器（例如Vicuna [184]或InternLM [135]）连接起来，并进行监督式微调（SFT）  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537218718-5d8acb99-62da-444d-ba2f-7fe4182d47f9.png)

:::color5
**<font style="color:#601BDE;">3.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

零样本图像-文本检索性能的比较。我们使用Flickr30K和COC评估了英语的检索能力，以及使用Flickr30K-C和COCO-C评估了中文的检索能力。†BLIP-在COCO上进行了微调，并零样本转移到Flickr30K上，这有助于提高Flickr30K上的零样本性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537365482-b710ac9a-eafd-485d-9b78-36973a424cb1.png)



## **CogVLM2**
项目地址：[https://github.com/THUDM/CogVLM2](https://github.com/THUDM/CogVLM2)

<font style="color:rgb(51, 51, 51);">CogVLM2 继承并优化了上一代模型的经典架构，采用了一个拥有50亿参数的强大视觉编码器，并创新性地在大语言模型中整合了一个70亿参数的视觉专家模块。这一模块通过独特的参数设置，精细地建模了视觉与语言序列的交互，确保了在增强视觉理解能力的同时，不会削弱模型在语言处理上的原有优势。这种深度融合的策略，使得视觉模态与语言模态能够更加紧密地结合。与上一代的 CogVLM 模型相比，CogVLM2 系列模型具有以下改进：</font>

+ <font style="color:rgb(51, 51, 51);">在不损失任何通用能力的前提下，在许多关键指标上有了显著提升，如在 OCRbench 基准上性能提升32%，在TextVQA基准上性能提升21.9%，且模型具备了较强的文档图像理解能力（DocVQA）等；</font>
+ <font style="color:rgb(51, 51, 51);">支持 8K 文本长度；</font>
+ <font style="color:rgb(51, 51, 51);">支持高达 1344 * 1344 的图像分辨率；</font>
+ <font style="color:rgb(51, 51, 51);">提供支持中英文双语的开源模型版本。</font>

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472157254-938b8de6-ac1d-4994-b9d1-3594b288ae74.webp)

## **MiniCPM-V**
项目地址：[https://github.com/OpenBMB/MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V)

<font style="color:rgb(51, 51, 51);">MiniCPM-V 2.6 是由面壁智能推出的一款端侧 AI 多模态模型。它在保持较小参数规模的同时，展现出了强大的多模态处理能力，为端侧设备上的人工智能应用提供了新的可能性。</font>

**<font style="color:rgb(51, 51, 51);">主要特点:</font>**

+ <font style="color:rgb(51, 51, 51);">多图理解与上下文学习：MiniCPM-V 2.6 能够支持多图对话与推理。在 Mantis-Eval、BLINK、Mathverse mv 以及 Sciverse mv 等主流多图评测基准中取得了顶尖水平，并且展现出了极为出色的上下文学习能力。</font>
+ <font style="color:rgb(51, 51, 51);">强大的 OCR 能力：MiniCPM-V 2.6 能够处理任意长宽比的图像，像素数可达 180 万（例如 1344x1344）。在 OCRBench 上，它取得了最佳成绩，超越了 GPT-4o、GPT-4V 以及 Gemini 1.5 Pro 等商用闭源模型。</font>
+ <font style="color:rgb(51, 51, 51);">效率卓越：除了对个人用户极为友好的模型大小之外，MiniCPM-V 2.6 还展现出了最为先进的视觉 token 密度（即每个视觉 token 编码的像素数量）。它仅需 640 个 token 即可处理 180 万像素的图像，比大多数模型少 75%。这一特性极大地优化了模型的推理速度、首 token 延迟、内存占用以及功耗。因此，MiniCPM-V 2.6 能够在 iPad 等终端设备上支持高效的实时视频理解。</font>
+ <font style="color:rgb(51, 51, 51);">使用便捷：MiniCPM-V 2.6 可以通过多种方式轻松加以使用：(1) llama.cpp 和 ollama 支持在本地设备上进行高效的 CPU 推理；(2) int4 和 GGUF 格式的量化模型，拥有 16 种尺寸；(3) vLLM 支持高吞吐量和内存高效的推理；(4) 针对新领域和任务进行微调；(5) 使用 Gradio 快速设置本地 WebUI 演示；(6) 通过在线 demo 即可亲身体验。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472159405-d84fc67d-69fe-4050-8179-9c393802a3cc.png)

## **<font style="color:rgb(0, 0, 0);">mPLUG-Owl3</font>**
项目地址：https://github.com/X-PLUG/mPLUG-Owl/

mPLUG系列在多模态大模型领域产出了多项研究工作。从mPLUG-Owl初代模型引入了视觉对齐-语言模型微调的训练模式，到mPLUG-Owl2通过模块化的模态自适应解决模态拉扯，再到mPLUG-DocOwl通过切图建模高分辨率。这一系列模型一直在探索更为高效有效的多模态大语言模型。

尽管近年包括mPLUG-Owl在内的主流多模态大模型在多种单图任务上取得了一系列进展，当前对于多模态大模型来说，多图长序列输入仍然是一个极具挑战性的场景。针对上述问题，阿里通义实验室提出通用多模态大模型mPLUG-Owl3，该模型能够在支持多图长序列输入的同时，兼顾性能和效率。为实现这一点，作者提出轻量级的hyper attention模块，实现视觉和语言信息的高效自适应融合，在单图、多图、视频等多达14个benchmark上表现出SOTA性能<font style="color:rgba(0, 0, 0, 0.85);">。</font>

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472159579-2a692c40-fadd-41a7-8a2c-82d381b99b04.webp)

## **OVIS**
项目地址：[https://github.com/AIDC-AI/Ovis](https://github.com/AIDC-AI/Ovis?spm=ata.21736010.0.0.7bcb43179Aefhs)

Ovis是阿里国际AI团队发布的一款多模态大模型，借鉴了LLM中的文本嵌入策略，引入了可学习的视觉嵌入表，将连续的视觉特征先转换为概率化的视觉token，再经由视觉嵌入表多次索引加权得到结构化的视觉嵌入。评测结果显示：Ovis在十余项多模态基准测试中均优于主流同尺寸开源MLLM。

**<font style="color:rgb(51, 51, 51);">主要特点:</font>**

1、创新架构设计：可学习的视觉嵌入词表：首次引入，将连续的视觉特征转换为概率化的视觉token，再经由视觉嵌入词表加权生成结构化的视觉嵌入，克服了大部分MLLM中MLP连接器架构的局限性，大幅提升多模态任务表现。

2、高分图像处理：动态子图方案：支持处理极端长宽比的图像，兼容高分辨率图像，展现出色的图像理解能力。

3、全面数据优化：多方向数据集覆盖：全面覆盖Caption、VQA、OCR、Table、Chart等各个多模态数据方向，显著提升多模态问答、指令跟随等任务表现。

4、卓越模型性能：Ovis展现出了优异的榜单表现。在多模态权威综合评测Opencompass上，Ovis1.6-Gemma2-9B在30B参数以下的模型中取得了综合排名第一，超过了Qwen2-VL-7B、MiniCPM-V-2.6等模型。尤其在数学问答等方向表现媲美70B参数模型；在幻觉等任务中，Ovis-1.6的幻觉现象和错误率显著低于同级别的模型，展现了更高的生成文本质量和准确性。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472160172-1beb9c1a-71a7-4915-bf68-ffc2396c2cf9.png)

## Florence
### <font style="color:rgb(0, 0, 0);">Florence2</font>
:::success
**<font style="color:rgb(51, 51, 51) !important;">背景：</font>**<font style="color:rgb(51, 51, 51) !important;">我们已经看到了用于分类的CLIP模型、用于对象检测的Grounding DINO和用于分割的SAM等模型，每种模型在其各自领域都表现出色。</font>**<font style="color:#74B602;">但是，我们是否能够开发一个能够同时处理所有这些任务的单一模型呢？</font>**

:::

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51) !important;">Florence-2模型：</font>**<font style="color:#ED740C;">一种新颖的开源视觉语言模型（VLM），旨在处理各种视觉和多模型任务，包括字幕识别、对象检测、分割和OCR等内容。</font>**

:::

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**

:::

<font style="color:rgb(51, 51, 51);">为了训练Florence-2模型，研究人员需要一个全面、大规模、高质量的多任务数据集，覆盖了各种图像数据。鉴于这种数据的稀缺性，他们由此创建了全新的多任务图像数据集——FLD-5B。</font>

<font style="color:rgb(51, 51, 51);">这一数据集中包含了1.26亿张图像、5亿个文本标注、13亿个文本-图像区域标注，以及36亿个文本短语-图像区域标注，跨横跨了不同的任务。</font>

**<font style="color:rgb(51, 51, 51);">数据格式</font>**

<font style="color:rgb(51, 51, 51) !important;">受大型语言模型的启发，Florence-2被设计为一种序列到序列的模型。它将图像和文本指令作为输入，并输出文本结果。输入或输出文本可以表示纯文本或图像中的区域。区域格式因任务而异：</font>

+ <font style="color:rgb(51, 51, 51) !important;">边界框：“<X1><Y1><X2><Y2>”用于对象检测任务。这些标记表示长方体左上角和右下角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">四边框：“<X1><Y1><X2><Y2><X3><Y3><X4><Y4>”用于文本检测，使用包围文本的四个角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">多边形：“<X1><Y1><Xn><Yn>'用于分割任务，其中坐标按顺时针顺序表示多边形的顶点。</font>

:::color5
**<font style="color:#601BDE;">2.数据引擎流程</font>**

:::

<font style="color:rgb(51, 51, 51);">Florence-2数据引擎一共包含三个重要环节：</font>

<font style="color:rgb(51, 51, 51);">1) 使用专业模型进行初始标注</font>

<font style="color:rgb(51, 51, 51);">2) 数据过滤，纠正错误并移除无关标注</font>

<font style="color:rgb(51, 51, 51);">3) 迭代式的数据优化过程</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340588984-846de6c7-1166-4d52-8b0a-204334b652c6.png)

<font style="color:rgb(51, 51, 51);">FLD-5B中的每一张图像都由Florence数据引擎标注了文本、图像区域-文本对以及文本短语-图像区域三元组，涵盖了多个空间层次、从概括到详细的渐进粒度，以及多语义，让模型从不同角度实现了更全面的视觉理解能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340643905-62b28ba5-47b7-4fac-a796-6fa3685c0554.png)

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51) !important;">Florence-2模型是使用标准“编码器-解码器”转换器架构构建的。</font>

+ <font style="color:rgb(51, 51, 51) !important;">输入图像由DaViT视觉编码器嵌入。</font>
+ <font style="color:rgb(51, 51, 51) !important;">文本提示使用BERT嵌入，利用扩展的标记器和单词嵌入层。</font>
+ <font style="color:rgb(51, 51, 51) !important;">视觉和文本嵌入都是连接在一起的。</font>
+ <font style="color:rgb(51, 51, 51) !important;">这些级联的嵌入由基于转换器的多模型编码器-解码器处理，以生成响应。</font>
+ <font style="color:rgb(51, 51, 51) !important;">在训练过程中，该模型最小化交叉熵损失，类似于标准语言模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340494596-586f7a45-498c-4a88-be4d-2c3010734e80.png)



### <font style="color:rgb(0, 0, 0);">Florence-VL</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">微软研究院提出Florence-VL多模态模型，利用生成式视觉编码器Florence-2和深度广度融合机制（</font>[<font style="color:rgb(9, 64, 142);">DBFusion</font>](https://zhida.zhihu.com/search?content_id=251493745&content_type=Article&match_order=1&q=DBFusion&zhida_source=entity)<font style="color:rgb(25, 27, 31);">），高效整合细粒度和高层视觉特征，并在25个基准测试中取得领先性能。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340819169-1e9c30fd-7430-493f-924c-61d853669100.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ <font style="color:rgb(25, 27, 31);">统一视觉编码：单个 vision encoder 降低了复杂性，同时保持了特定任务的适应性。</font>
+ <font style="color:rgb(25, 27, 31);">特定任务的灵活性：基于 prompt 的机制支持各种应用，包括 OCR 和 grounding。</font>
+ <font style="color:rgb(25, 27, 31);">增强的融合策略：DBFusion 确保了 depth 和 breadth features 的丰富组合，捕捉粒度和上下文细节。</font>
+ <font style="color:rgb(25, 27, 31);">卓越的基准测试结果：Florence-VL 在 25 个 benchmarks 中处于领先地位，实现了 2.98 的 alignment loss。</font>
+ <font style="color:rgb(25, 27, 31);">训练效率：在预训练期间 fine-tune 整个架构可增强多模态对齐，从而产生更好的任务结果。</font>

:::color5
**<font style="color:#601BDE;">2.技术原理</font>**

:::

+ [**<font style="color:rgb(9, 64, 142);">生成式视觉编码器</font>**](https://zhida.zhihu.com/search?content_id=251398051&content_type=Article&match_order=1&q=%E7%94%9F%E6%88%90%E5%BC%8F%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：使用Florence-2作为视觉编码器，基于不同的任务提示生成视觉特征，适用于多种视觉任务。</font>
+ [**<font style="color:rgb(9, 64, 142);">特征融合架构</font>**](https://zhida.zhihu.com/search?content_id=251398051&content_type=Article&match_order=1&q=%E7%89%B9%E5%BE%81%E8%9E%8D%E5%90%88%E6%9E%B6%E6%9E%84&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：引入新颖的特征融合架构，将从Florence-2提取的视觉特征与预训练的语言模型相结合。</font>
+ **<font style="color:rgb(25, 27, 31);">深度-广度融合（DBFusion）</font>**<font style="color:rgb(25, 27, 31);">：</font>
+ **<font style="color:rgb(25, 27, 31);">深度</font>**<font style="color:rgb(25, 27, 31);">：整合来自不同层次的视觉特征，捕捉从低级到高级的概念细节。</font>
+ **<font style="color:rgb(25, 27, 31);">广度</font>**<font style="color:rgb(25, 27, 31);">：使用多个任务特定的视觉特征，每个特征强调输入图像中的不同感知信息。</font>
+ [**<font style="color:rgb(9, 64, 142);">端到端预训练</font>**](https://zhida.zhihu.com/search?content_id=251398051&content_type=Article&match_order=1&q=%E7%AB%AF%E5%88%B0%E7%AB%AF%E9%A2%84%E8%AE%AD%E7%BB%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：整个模型进行端到端预训练，实现视觉和语言模态之间的最佳对齐。</font>
+ **<font style="color:rgb(25, 27, 31);">微调</font>**<font style="color:rgb(25, 27, 31);">：在预训练后，对投影层和语言模型进行微调，适应特定的下游任务。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(34, 34, 34);">在多种视觉编码器对比实验里，Florence-2 就像一匹黑马脱颖而出。实验测不同视觉编码器与语言模型的跨模态对齐能力，结果 Florence-2 显示出更优的能力，就像在一场赛跑里，它跑得比其他选手都快。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340931207-1cc91661-5348-44da-9191-ad6c94662795.png)



## LLAVA系列
### LLAVA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">多模态需求</font>**<font style="color:rgb(51, 51, 51);">：随着AI在视觉-语言任务（如图像问答、图文生成）中的需求增长，传统单模态模型难以满足复杂场景。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">现有不足</font>**<font style="color:rgb(51, 51, 51);">：早期多模态模型（如Flamingo）依赖海量数据与算力，且跨模态对齐效率低。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">LLaVA定位</font>**<font style="color:rgb(51, 51, 51);">：基于开源LLM（如Vicuna）与视觉编码器（CLIP-ViT），通过轻量级设计实现高效视觉-语言对齐。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078830518-06b4da4b-1f59-4f2e-8ba9-5332ebaf8480.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">简单投影层</font>**<font style="color:rgb(51, 51, 51);">：用线性层或MLP将图像特征映射到文本嵌入空间，无需复杂跨模态架构。</font>
+ **<font style="color:rgb(51, 51, 51);">两阶段训练</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">阶段1</font>**<font style="color:rgb(51, 51, 51);">：冻结视觉与语言模型，仅训练投影层，实现模态对齐。</font>
    - **<font style="color:rgb(51, 51, 51);">阶段2</font>**<font style="color:rgb(51, 51, 51);">：端到端微调，增强多模态交互能力。</font>
+ **<font style="color:rgb(51, 51, 51);">合成数据</font>**<font style="color:rgb(51, 51, 51);">：利用GPT-4生成高质量指令数据，降低标注成本。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉数据</font>**<font style="color:rgb(51, 51, 51);">：COCO、Visual Genome等公开图像数据集。</font>
+ **<font style="color:rgb(51, 51, 51);">文本数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">对齐数据</font>**<font style="color:rgb(51, 51, 51);">：图像-描述对（如COCO Captions）。</font>
    - **<font style="color:rgb(51, 51, 51);">指令数据</font>**<font style="color:rgb(51, 51, 51);">：GPT-4生成的问答对（如“描述图中场景并推测事件原因”）。</font>
+ **<font style="color:rgb(51, 51, 51);">格式</font>**<font style="color:rgb(51, 51, 51);">：多轮对话（User: [图像] + 问题；Assistant: 回答）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：CLIP-ViT-L/14，提取图像特征（每图→</font>`<font style="color:rgb(51, 51, 51);">[N, d_vis]</font>`<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：线性层或MLP，将</font>`<font style="color:rgb(51, 51, 51);">d_vis</font>`<font style="color:rgb(51, 51, 51);">维特征映射到语言模型嵌入空间</font>`<font style="color:rgb(51, 51, 51);">d_txt</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">语言模型</font>**<font style="color:rgb(51, 51, 51);">：Vicuna（LLaMA微调版），处理文本与投影后的视觉特征。</font>
+ **<font style="color:rgb(51, 51, 51);">输入拼接</font>**<font style="color:rgb(51, 51, 51);">：图像特征与文本嵌入拼接为序列输入语言模型。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **阶段1 - 特征对齐**：
    - <font style="color:rgb(51, 51, 51);">冻结ViT和LLM，</font>**<font style="color:#ED740C;">仅训练投影层</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">目标：最小化图文匹配损失（如对比学习）。</font>
    - <font style="color:rgb(51, 51, 51);">数据：图像-文本对，将CC3M过滤为595K图像文本对。</font>
2. **阶段2 - 端到端微调**：
    - <font style="color:rgb(51, 51, 51);">冻结视觉，</font>**<font style="color:#ED740C;">联合优化投影层与LLM</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">目标：生成任务的交叉熵损失。</font>
    - <font style="color:rgb(51, 51, 51);">数据：指令数据（GPT-4生成的多轮对话），158K图文指令数据，来自COCO图片。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算高效（复用预训练模型，轻量投影层）。</font>
+ <font style="color:rgb(51, 51, 51);">支持复杂视觉推理（如因果推断、细节描述）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">图像分辨率固定，细节处理有限。</font>
+ <font style="color:rgb(51, 51, 51);">依赖语言模型生成能力，可能产生幻觉回答。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉问答</font>**<font style="color:rgb(51, 51, 51);">：用户上传图片提问，模型生成解释。</font>
+ **<font style="color:rgb(51, 51, 51);">教育辅助</font>**<font style="color:rgb(51, 51, 51);">：解析教科书图表并生成讲解。</font>
+ **<font style="color:rgb(51, 51, 51);">无障碍技术</font>**<font style="color:rgb(51, 51, 51);">：为视障用户描述场景。</font>
+ **<font style="color:rgb(51, 51, 51);">内容审核</font>**<font style="color:rgb(51, 51, 51);">：结合图像与文本进行违规内容检测。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">增强视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：使用更高分辨率ViT或SAM分割模型。</font>
+ **<font style="color:rgb(51, 51, 51);">动态投影层</font>**<font style="color:rgb(51, 51, 51);">：引入注意力机制替代简单线性层。</font>
+ **<font style="color:rgb(51, 51, 51);">混合数据训练</font>**<font style="color:rgb(51, 51, 51);">：加入视频数据提升时序理解能力。</font>
+ **<font style="color:rgb(51, 51, 51);">强化学习</font>**<font style="color:rgb(51, 51, 51);">：基于人类反馈（RLHF）优化生成结果。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import AutoTokenizer, CLIPModel, LlamaForCausalLM

class LLaVA(torch.nn.Module):
    def __init__(self, llm_name="vicuna-7b", clip_name="openai/clip-vit-large-patch14"):
        super().__init__()
        self.vision_encoder = CLIPModel.from_pretrained(clip_name).visual
        self.tokenizer = AutoTokenizer.from_pretrained(llm_name)
        self.llm = LlamaForCausalLM.from_pretrained(llm_name)
        self.proj = torch.nn.Linear(1024, self.llm.config.hidden_size)  # 投影层

    def forward(self, images, input_ids, attention_mask):
        # 提取图像特征
        vis_features = self.vision_encoder(images).last_hidden_state.mean(dim=1)
        # 投影到文本空间
        vis_embeds = self.proj(vis_features).unsqueeze(1)
        # 拼接文本嵌入
        text_embeds = self.llm.get_input_embeddings()(input_ids)
        inputs_embeds = torch.cat([vis_embeds, text_embeds], dim=1)
        # 生成输出
        outputs = self.llm(inputs_embeds=inputs_embeds, attention_mask=attention_mask)
        return outputs.logits

# 示例调用
model = LLaVA()
images = torch.randn(1, 3, 224, 224)  # 输入图像
input_ids = model.tokenizer("Describe this image:", return_tensors="pt").input_ids
logits = model(images, input_ids, attention_mask=None)

```

```python
# 两阶段训练示例
optimizer = torch.optim.AdamW([
    {'params': model.proj.parameters(), 'lr': 1e-3},  # 阶段1仅训练投影层
    {'params': model.llm.parameters(), 'lr': 2e-5}     # 阶段2解冻LLM
])

for epoch in range(epochs):
    for images, texts in dataloader:
        inputs = tokenizer(texts, padding=True, return_tensors="pt")
        logits = model(images, inputs.input_ids, inputs.attention_mask)
        loss = torch.nn.functional.cross_entropy(
            logits.view(-1, logits.shape[-1]), inputs.input_ids.view(-1)
        )
        loss.backward()
        optimizer.step()

```

#### LLAVA与CLIP对齐的对比
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">CLIP</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐 是其核心能力，通过</font>**<font style="color:#ED740C;">对比学习（Contrastive Learning）</font>**<font style="color:rgb(25, 27, 31);">将图像和文本映射到统一的语义空间。</font>

**<font style="color:rgb(25, 27, 31);">LLaVA</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐的核心是通过一个</font>**<font style="color:#ED740C;">轻量级线性投影层将视觉特征映射到语言模型的词嵌入空间</font>**<font style="color:rgb(25, 27, 31);">，结合两阶段训练策略实现高效对齐。以下是详细的技术分解：</font>

**<font style="color:rgb(51, 51, 51);">参考</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://zhuanlan.zhihu.com/p/27728623876](https://zhuanlan.zhihu.com/p/27728623876)

:::

:::color5
**<font style="color:#601BDE;">1.CLIP多模态对齐</font>**

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
**<font style="color:#601BDE;">2.LLAVA多模态对齐</font>**

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

### LLAVA-Next
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>LLaVA作为最早一批出现的多模态大模型，其模型结构与训练策略对于现在的多模态模型发展产生了巨大的影响。

**github**：[https://github.com/haotian-liu/LLaVA/tree/main](https://github.com/haotian-liu/LLaVA/tree/main)

:::

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472160548-c481673d-772d-4250-afff-81913d073d68.webp)

:::color5
**<font style="color:#601BDE;">1.版本对比</font>**

:::

| <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">模型版本</font> | <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">LLava</font> | <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">LLava1.5</font> | <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">LLava-Next(1.6)</font> |
| :--- | :--- | :--- | :--- |
| <font style="color:rgba(0, 0, 0, 0.9);">输入分辨率</font> | <font style="color:rgba(0, 0, 0, 0.9);">224*224</font> | <font style="color:rgba(0, 0, 0, 0.9);">336*336</font> | <font style="color:rgba(0, 0, 0, 0.9);">336*{2x2， 1x{2,3,4}, {2,3,4} x 1}的网格配置</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">视觉编码器</font> | <font style="color:rgba(0, 0, 0, 0.9);">CLIP-L/14</font> | **<font style="color:rgba(0, 0, 0, 0.9);">CLIP-ViT-L-336px</font>** | **<font style="color:rgba(0, 0, 0, 0.9);">CLIP-ViT-L-336px</font>** |
| <font style="color:rgba(0, 0, 0, 0.9);">连接器</font> | <font style="color:rgba(0, 0, 0, 0.9);">一个全连接层</font> | <font style="color:rgba(0, 0, 0, 0.9);">2层MLP</font> | <font style="color:rgba(0, 0, 0, 0.9);">2层MLP</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">LLM</font> | <font style="color:rgba(0, 0, 0, 0.9);">llama1-13B、7B</font> | <font style="color:rgba(0, 0, 0, 0.9);">Vicuna-1.5（7B和13B）</font> | <font style="color:rgba(0, 0, 0, 0.9);">Vicuna-1.5（7B和13B）</font><br/><font style="color:rgba(0, 0, 0, 0.9);">Mistral 7B</font><br/><font style="color:rgba(0, 0, 0, 0.9);">Nous-Hermes-2-Yi-34B</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">预训练数据集</font> | **<font style="color:rgba(0, 0, 0, 0.9);">CC3M（595K）</font>** | | |
| <font style="color:rgba(0, 0, 0, 0.9);">指令微调数据集</font> | <font style="color:rgba(0, 0, 0, 0.9);">158K</font><br/><font style="color:rgba(0, 0, 0, 0.9);">（使用COCO生成的对话、描述、复杂推理数据集）</font> | <font style="color:rgba(0, 0, 0, 0.9);">665K</font><br/><font style="color:rgba(0, 0, 0, 0.9);">（在前一版基础上增加ShareGPT数据集、学术导向的VQA数据集、OCR数据集、Region-level的VQA数据集）</font> | <font style="color:rgba(0, 0, 0, 0.9);">760K</font><br/><font style="color:rgba(0, 0, 0, 0.9);">（在前一个版本基础上</font>**<font style="color:rgba(0, 0, 0, 0.9);">移除</font>**<font style="color:rgba(0, 0, 0, 0.9);">TextCaps数据集、新增LAION-GPT-V、ShareGPT-4V、先上分收集的LLaVA demo数据集、DocVQA和SynDog-EN的OCR数据集、以及ChartQA、DVQA和AI2D等表格QA数据集）</font> |


:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

**<font style="color:rgb(51, 51, 51);">缺点</font>**

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);"></font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::



:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python

```

在LLAVA1.5的基础上，LLAVA-NEXT进一步支持了高分辨率图像。它支持三种宽高比，分别为 672x672，336x1344，1344x336。（Vision Encoder 的输入是 336px）使用 Hermes-Yi-34B 为 LLM 的 LLaVA-NeXT 更是在多项评测标准上超过了 Gemini-Pro。

此外，LLaVA-NeXT 真正应用了 AnyRes 技术。如下图所示，图片一方面按照 2x2 进行分割并分别编码，最后合并展平，输入给 LLM。另一方面，图片会进行降采样并直接进行编码，从而为 LLM 提供图片的全局信息。分割方式具体包含 2x2，1x2，1x3，1x4，2x1，3x1 和 4x1。

在使用了更大的 LLM 后，LLaVA-NeXT 的能力迎来了进一步强化。此处的 LLaVA-NeXT 使用了 Qwen1.5-110B、Qwen1.5-72B、LLaMA3-8B 作为 LLM，其中使用了 Qwen1.5-110B 的 LLaVA-NeXT 的模型表现更是直追 GPT4-V。

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472160548-c481673d-772d-4250-afff-81913d073d68.webp)



### Dynamic LLAVA <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>本文主要围绕以 LLaVA 为范式的多模态大模型展开研究。一个多模态大模型的推理过程可以分为预填充和解码两个阶段：

+ **预填充阶段**：不同模态的特征被映射到与大语言模型（LLM）输入 embedding 相同的特征分布空间中。这些多模态特征与文本 token 会一起被大语言模型处理，以生成初始输出文本 token。以图片理解场景为例，该阶段主要处理输入的图片和文本格式的问题。
+ **解码阶段**：预填充阶段生成的所有 token 以及后续生成的所有输出文本 token，将被用于自回归生成，从而产生完整的输出。同样以图片理解场景为例，该阶段生成针对整个问题的完整回答。

:::

:::color3
**简介：**<font style="color:#000000;">针对上述问题，论文认为：为了实现真正的全阶段推理加速，</font>**<font style="color:#ED740C;">不仅需要对预填充阶段的视觉 token 进行剪枝，还必须对解码阶段输出的文本 token 进行稀疏化处理</font>**<font style="color:#000000;">，限制参与自回归运算的 token 数量。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:#000000;"> </font>**<font style="color:#000000;">Dynamic-LLaVA</font>**<font style="color:#000000;">是针对多模态大模型提出的的视觉-语言上下文稀疏化推理加速框架。该框架能够集成到多模态大模型推理的不同阶段中，实现以下目标：</font>

+ **<font style="color:#000000;">显著降低预填充阶段计算开销：</font>**<font style="color:#000000;">通过优化视觉 token 的处理方式，减少不必要的计算。</font>
+ **<font style="color:#000000;">提升解码阶段的推理效率：</font>**<font style="color:#000000;">无论是否使用 KV Cache，都能减少计算开销，提高推理速度。</font>
+ **<font style="color:#000000;">保持性能优势：</font>**<font style="color:#000000;">在视觉理解任务上几乎不损失性能；在长文本输出场景中，生成能力也几乎不受影响。</font>

<font style="color:#000000;">通过这些创新，Dynamic-LLaVA 为多模态大模型的高效推理提供了一种全新的解决方案。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Osilly/dynamic_llava](https://github.com/Osilly/dynamic_llava)

**paper：**[**Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification**](https://arxiv.org/pdf/2412.00876)

**参考：**[**https://mp.weixin.qq.com/s/2SbbAlLxZG9Ub_lZf8YVDw**](https://mp.weixin.qq.com/s/2SbbAlLxZG9Ub_lZf8YVDw)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760547508-71b3e2af-2994-4252-b6b0-b1f4104ba48f.png)

<font style="color:rgb(136, 136, 136);">▲ 图6：Dynamic-LLaVA-13B 在 LVIS-VQA（single-round）上的推理结果展示。图片的白色部分表示该位置的图像块被丢弃，文字中的灰色部分表示其在稀疏化过程中被丢弃，这表示它们不参与后续的自回归解码过程，但在模型的输出中都被完整保留</font>

图 6 中展示了 Dynamic-LLaVA-13B 在 LVIS-VQA（single-round）上的推理结果，以及对视觉和文本 token 的稀疏化情况。

可视化结果表明，视觉 token 部分的主要信息得以保留；**<font style="color:#74B602;">文本 token 中，一些不影响整体语义理解的连词、介词等被丢弃。这表明 Dynamic-LLaVA 能够实现关键的视觉、语义信息的保留，从而保证了模型整体的性能。</font>**

:::color5
**<font style="color:#601BDE;">1.多模态大模型的推理瓶颈 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745759717189-9fed35a4-9ac4-4337-8103-c2fad1a515bf.png)

<font style="color:rgb(63, 63, 63);">现有的多模态大模型大多以基于解码器架构的大语言模型（LLM）为核心，这些模型通常拥有庞大的参数规模。在生成输出文本 token 的过程中，模型计算负担会逐渐加重，导致对计算资源的巨大消耗。</font>

<font style="color:rgb(63, 63, 63);">为了提升推理速度，现有模型通常会在解码过程中运用 KV Cache 技术，通过存储并复用之前计算的 KV 激活值来减少重复计算。然而，如图 1（B）所示，</font>**<font style="color:#117CEE;">即使使用了 KV Cache，LLaVA 在输出 token 不断增加时，仍会迅速面临 GPU 显存耗尽的问题</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">与文本不同，视觉信息往往包含大量冗余。因此，许多方法尝试通过减少视觉上下文来加速多模态大模型的推理，即对预填充阶段的视觉 token 进行剪枝处理。但这种方法存在局限性：</font>**<font style="color:#117CEE;">其主要提升了多模态大语言模型在预填充阶段的推理效率，而在解码阶段，其效率提升会逐渐减弱</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">如图 1（B）和（C）所示，FastV 这种针对视觉 token 剪枝的方法，虽然相较于原始的 LLaVA 能够节省一定的 GPU 显存和计算开销（FLOPs），但当输出 token 数接近 5K 时，它仍然会遭遇计算资源瓶颈。</font>

<font style="color:rgb(63, 63, 63);">此外，FastV 和原始 LLaVA 的曲线斜率基本一致，这表明在长输出的解码阶段，这类方法并没有显著的推理效率优势。因此，</font>**<font style="color:#117CEE;">仅通过减少预填充阶段的视觉 token，在输出文本 token 数量远超视觉 token 时，难以实现整个推理效率的显著提升。</font>**

:::color5
**<font style="color:#601BDE;">2.方法 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745759731667-7e11e19d-ef31-4ee6-9fe7-ba8277c4b62c.png)

如图 2 所示，Dynamic-LLaVA 可以集成到多模态大模型推理流程中的不同阶段。具体而言，在预填充阶段，该框架**<font style="color:#74B602;">对视觉 token 执行精准剪枝操作，剔除冗余信息</font>**；在不使用 KV Cache 的解码阶段，**<font style="color:#74B602;">限制参与自回归运算的视觉与输出文本 token 数量</font>**，避免不必要的计算负担。

而在使用 KV Cache 的解码阶段，Dynamic-LLaVA 则动态调控 KV Cache，自适应判断是否将当前输出文本 token 的 KV 激活值纳入 KV Cache，优化资源利用效率。

为了使模型适应这种全新的稀疏化推理模式，Dynamic-LLaVA 在预训练的 LLaVA-1.5 基础上进行了 1 个 epoch 的监督微调（SFT），确保模型能够高效地运行在稀疏化的推理路径上。

:::color5
**<font style="color:#601BDE;">3.Prefill 预填充 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">在预填充阶段，我们对输入的视觉 token 进行稀疏化操作。如图 2 左侧部分所示，我们引入一个</font>**<font style="color:#74B602;">可训练的轻量化的图像预测器（Image Predictor），来判断应当丢弃哪些视觉 token</font>**<font style="color:rgb(63, 63, 63);">。该图像预测器的结构如下图：</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745759451131-edf617a4-e369-4354-8a26-45e25ae7e9a5.webp)

<font style="color:rgb(136, 136, 136);">▲ 图3：图像预测器的结构示意图 </font>

<font style="color:rgb(63, 63, 63);">图像预测器会对每个视觉 token 产生</font>**<font style="color:#74B602;">“决策分数”，以决定对哪些视觉 token 进行保留</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">在端到端训练中，视觉 token 的剪枝通过 0-1 二值化的掩码操作实现（具体过程见 2.4 节）。</font>

<font style="color:rgb(63, 63, 63);">在实际推理阶段中，通过保留“决策分数”前 k 大的视觉 token（即图 2 左侧部分的 “Yes” 分支），实现视觉 token 数量减少，以实现推理加速。</font>

:::color5
**<font style="color:#601BDE;">4.解码阶段 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(0, 0, 0);">不使用 KV Cache 的解码过程：</font>**

<font style="color:rgb(63, 63, 63);">对于视觉 token，采用和上一小节相同的做法，进行稀疏化处理。</font>

<font style="color:rgb(63, 63, 63);">对于输出的文本 token，分两类进行处理：</font>

+ <font style="color:rgb(63, 63, 63);">最后一个输出的文本 token（即图 2 中间部分的 “Last output text token”），不进行任何处理，完整输入 LLM 的 decoder 层进行计算。这样做的目的是保证模型的输出内容是连贯的，产生新的输出文本 token 时，始终保证自回归运算包含上一个输出文本 token。</font>
+ <font style="color:rgb(63, 63, 63);">对其他历史的输出文本 token 进行稀疏化操作，其形式类似于对视觉 token 的处理。引入一个结构如下图的输出预测器（Output Predictor），给出每个输出文本 token 的“决策分数”，以决定当前产生新的输出内容时，应当包括哪些文本 token 进行自回归运算。图 2 中间部分的 “Yes” 分支，表明保留的输出文本 token。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745759769837-3c8c7f1e-56ad-48ba-8ac2-9b9149e01e02.webp)

<font style="color:rgb(136, 136, 136);">▲ 图4：输出预测器的结构示意图 </font>

**<font style="color:rgb(63, 63, 63);">使用 KV Cache 的解码过程：</font>**

<font style="color:rgb(63, 63, 63);">KV Cache 是节省冗余计算的一个关键推理加速技术，其思想是“用 GPU 显存的空间换计算时间”。显而易见的是，KV Cache 也并非无限大，在长输出情况下，必须丢弃一些 KV Cache 以适应有限的 GPU 显存。</font>

<font style="color:rgb(63, 63, 63);">目前在 LLM 领域已有大量的 KV Cache 压缩方案，以 H</font><sub><font style="color:rgb(63, 63, 63);">2</font></sub><font style="color:rgb(63, 63, 63);">O方法为代表，这一类方法一般基于当前 token 和历史 KV Cache 进行重要性分数计算，以压缩历史 KV Cache。</font>

<font style="color:rgb(63, 63, 63);">与上述方法不同的是，我们对有 KV Cache 的解码阶段的设计，</font>**<font style="color:#74B602;">核心在于“仅判断当前新 token 的 KV 激活是否需要加入 KV Cache 中”。</font>**

<font style="color:rgb(63, 63, 63);">如图 3 右侧所示，对于当前正在处理的新 token（Last output text token），使用和上一部分结构相同的输出预测器，以决定是否加入 KV Cache 集合中。</font>

<font style="color:rgb(63, 63, 63);">这种 “</font>**<font style="color:#74B602;">Online KV Cache 压缩</font>**<font style="color:rgb(63, 63, 63);">”方法，判断是否保留 KV Cache 的过程计算复杂度更低，也更加适应多模态场景。在论文论文附录中，我们详细讨论了我们的方法和现有的 LLM KV Cache 压缩方法的区别。</font>

<font style="color:rgb(63, 63, 63);">需要特别说明的是，和不使用 KV Cache 的解码阶段相同，无论当前处理的 token 是否加入 KV Cache，其都会输入 LLM decoder 层进行计算，以保证输出的连贯性。</font>

:::color5
**<font style="color:#601BDE;">5.端到端训练 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745759991825-80de864e-82c5-4398-a68d-f6a78149d92e.webp)

<font style="color:rgb(136, 136, 136);">▲ 图5：Dynamic-LLaVA 在端到端训练过程中的示意图</font>

<font style="color:rgb(63, 63, 63);">Dynamic-LLaVA 是一个需要训练的多模态大模型推理加速框架。我们基于 LLaVA 进行了一个 epoch 的指令微调，以实现对 token 动态选择的稳定性，保证最终的性能。为了保证端到端训练，在训练阶段的稀疏化操作通过 0-1 二值化掩码实现（在推理中的实现是直接从历史 token 序列中丢弃 token）。</font>

<font style="color:rgb(63, 63, 63);">如图 5 所示，上半部分表示训练中进行 mask 的过程，在得到整个 token 序列的重要性分数后，我们</font>**<font style="color:#74B602;">选取前 k 重要的 token 进行保留，相对应的生成掩码向量，其中 0 对应丢弃的冗余 token（不参与注意力过程的计算），1 对应保留的重要 token</font>**<font style="color:rgb(63, 63, 63);">，进一步基于掩码向量生成注意力过程的掩码矩阵。</font>

<font style="color:rgb(63, 63, 63);">掩码矩阵用来对多头注意力机制进行掩码操作，以确保丢弃的 token 不参与注意力过程的计算。由于二值化操作会导致不可微问题，所以我们借助了 GumbalSoftmax 和梯度直通估计器（Straight Through Estimator, STE）来保证梯度流的正确传播，以进行端到端的训练，如图 5 下半部分所示。</font>

:::color5
**<font style="color:#601BDE;">6.视觉理解能力 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

我们首先评估了 Dynamic-LLaVA 在主要的视觉理解基准的性能，选取了目前主流的多模态大模型推理加速方法进行比较。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760139142-881054ad-07f4-40d0-bf0e-095c62998bd9.png)

<font style="color:rgb(136, 136, 136);">▲ 表1：视觉理解基准效果对比。其中，Free 表示方法是否是 Training-Free 的。Dynamic-LLaVA 的下标 “” 和 “” 分别表示仅对视觉 token 做稀疏化和同时对视觉和文本 token 都做稀疏化（该标识适用于下文所有的表格）</font>

如表 1 所示，Dynamic-LLaVA 在大部分视觉理解任务上取得了优越的性能。和其他对视觉内容稀疏化的方法相比，**<font style="color:#74B602;">Dynamic-LLaVA 在能大幅减小计算复杂度的同时，能够实现相比原始的 LLaVA-1.5 性能几乎不下降。</font>**

此外，在 SciQA、POPE、MME 和 MMBench上，Dynamic-LLaVA 相比 LLaVA-1.5 甚至有一定的性能提升。例如，在 SciQA 任务上，Dynamic-LLaVA 的 7B 和 13B 版本，相较于 LLaVA-1.5 实现了 2.3% 和 0.8% 的性能提升。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760160421-b5bc7293-7bd2-4a77-b8fe-58a7c89bbc40.png)

<font style="color:rgb(136, 136, 136);">▲ 表2：与其他高效视觉 projector 的 SOTA 方法对比</font>

值得一提的是，Dynamic-LLaVA 并没有对 LLaVA-1.5 的视觉 projector 进行修改，就可以**<font style="color:#74B602;">实现大幅降低预填充阶段计算复杂度，同时维持模型性能。</font>**

在表 2 中，和其他针对视觉 projector 做高效设计（以提高推理效率）的 SOTA 方法进行了对比。

相较于其他使用了高效的视觉 projector 的方法，Dynamic-LLaVA 使用和 LLaVA-1.5 相同的 MLP 结构作为视觉 projector，实现了更好的性能，同时也大幅降低了预填充阶段的计算复杂度。

此外，Dynamic-LLaVA 也可以和其他使用高效视觉 projector 的方法集成。例如，表 2 中 Dynamic-LLaVA 使用 TokenPacker 这一高效视觉 projector 的版本，在原始的 TokenPacker 方法基础上，进一步减少了视觉 token。相较于其他基于 TokenPacker 的推理加速方法，性能损失最少。

:::color5
**<font style="color:#601BDE;">7.生成能力 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

现有的视觉理解任务中，一般只要求模型给出简短的回复，这和现实世界中多模态大模型的应用场景仍然存在不小的区别。在现实使用中，多模态大模型多数情况下会被要求生成更长、更细致的描述。

为了和现实世界的场景对齐，评估在 Dynamic-LLaVA 在更长的输出情况下的生成能力和推理效率。我们额外构建了两个评估模型生成能力的基准：

+ LVIS-VQA：基于 LVIS-Instruct4 数据集，选取了 1000 个回答超过 100 个单词的单轮对话样本构成 LVIS-VQA（single round）和 1000 个多轮对话样本（平均回答单词数超过 300）构成 LVIS-VQA（multi-round）；
+ ShareGPT4V-VQA：基于 ShareGPT-4V 数据集，选取了 caption 超过 300 个单词的单论对话样本，平均输出 token 长度超过 1000。

我们以 PPL（Perplexity Metric）指标评估模型生成内容的流畅度、以 METEOR（Metric for Evaluation of Translation with Explicit ORdering）指标评估模型生成内容的质量。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760299604-13f39e73-50f1-4fa4-8efc-98a053f0ecf6.png)

<font style="color:rgb(136, 136, 136);">▲ 表3：生成能力基准比较。其中，解码阶段的 TFLOPs 和 Mem.（GPU 显存占用）分别在无/有 KV Cache 的情况下测量得出。PPL 越低越好，METEOR 越高越好</font>

如表 3 所示，相比 LLaVA-1.5，只进行视觉内容稀疏化的 Dynamic-LLaVA 的生成流畅度（PPL）和生成质量（METEOR）几乎没有变化。

同时对视觉和文本进行稀疏化的 Dynamic-LLaVA，PPL 仅变高了 0.3，METEOR 甚至略有提升，而在推理效率上，在无 KV Cache 的解码阶段降低了 ～ 50% 的 TFLOPs，在有 KV Cache 的解码阶段降低了 ～ 50% 的 GPU 显存占用。

实验结果充分表明，**<font style="color:#74B602;">Dynamic-LLaVA 针对视觉和文本同时进行稀疏化，几乎不影响实际生成能力，却可以实现大幅的推理效率提升。</font>**

:::color5
**<font style="color:#601BDE;">8.推理效率 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745760363116-80154b33-2e6b-420f-a9b1-9ab80a7e4a6e.webp)

<font style="color:rgb(136, 136, 136);">▲ 表4：Dynamic-LLaVA-13B 推理效率实测。其中，2K/4K 表示输出的文本 token 数，所有结果均在一张 A100（80G）上测试得出，batch size 固定为8。“×”表示 GPU 显存耗尽</font>

在表 4 中，我们压测了多模态大模型实际推理的时间和 GPU 显存占用。

Dynamic-LLaVA 实现了更快的推理速度和更低的显存占用。FastV 这种对预填充阶段的视觉 token 进行剪枝的方法，随着输出长度的增长，推理效率也逐渐降低。而我们提出的 Dynamic-LLaVA，随着输出变长，相比于 FastV 的推理效率优势也逐渐显现出来。

:::color5
**<font style="color:#601BDE;">9.总结 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">针对当前多模态大模型推理效率受限的问题，团队通过分析多模态大模型推理过程中的不同阶段，针对性的设计了推理加速方案。提出了 Dynamic-LLaVA ——第一个同时稀疏化视觉和语言上下文的多模态大模型推理加速框架，将不同推理模式的推理效率优化集成到统一框架中。</font>

<font style="color:rgb(63, 63, 63);">随着多模态大模型技术的发展，尤其是其在复杂推理、长思维链领域的不断进步。我们有理由相信，Dynamic-LLaVA 的应用场景正变得更加广泛，其对输出文本 token 进行稀疏化的模式，会在当前的更长输出、更复杂推理的场景下，体现出更明显的推理加速优势。</font>



