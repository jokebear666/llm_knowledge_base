# Deepseek-R1 INT8量化

<!-- source: yuque://zhongxian-iiot9/hlyypb/uw4w96edmuozs817 -->

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">美团搜索和推荐平台部对DeepSeek R1模型进行了INT8精度量化尝试，发现使用INT8量化后模型精度基本无损。基于INT8量化，DeepSeek R1模型解锁了芯片限制，可以部署到A100等其他型号GPU；并且相比BF16实现了50%的吞吐提升，进一步降低了推理成本。量化代码已经发布在了开源LLM推理框架SGLang上，量化模型已经发布到了Hugging Face社区，方便用户使用。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">参考</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>[https://mp.weixin.qq.com/s/TCkpG1Kn9tMYQeN2PCnwoA](https://mp.weixin.qq.com/s/TCkpG1Kn9tMYQeN2PCnwoA)

:::

**<font style="color:rgba(0, 0, 0, 0.9);">背景：</font>**<font style="color:rgba(0, 0, 0, 0.9);">DeepSeek R1横空出世后，吸引了众多公司和个人用户尝试其满血版本部署。然而原生版本的模型权重为FP8数据格式，对GPU芯片类型有严格限制，仅能被英伟达新型GPU支持（</font><font style="color:rgb(136, 136, 136);">如Ada、Hopper架构芯片</font><font style="color:rgba(0, 0, 0, 0.9);">），其他型号GPU（</font><font style="color:rgb(136, 136, 136);">如A100</font><font style="color:rgba(0, 0, 0, 0.9);">）无法直接部署。尽管我们可以将FP8权重反量化为BF16权重后，在A100等GPU上进行推理，但是这对显存的要求提升了一倍，推理吞吐也会下降。</font>

:::color5
**<font style="color:#601BDE;">1.DeepSeek R1 精度介绍</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">根据DeepSeek最新发布的技术报告，V3/R1突破性的训练成本控制</font>**<font style="color:#ED740C;">主要依托FP8精度训练方案</font>**<font style="color:rgba(0, 0, 0, 0.9);">。FP8是一种典型的模型量化技术，相较于业界常用的BF16精度，FP8精度通过将数据位宽减半显著降低了单次计算开销，但也会带来一定的精度损失。在实践中，DeepSeek R1采用了混合精度训练机制有效缓解了精度损失问题。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337466071-41be5e80-9280-4745-ae0c-a953d0b59699.png)

<font style="color:rgba(0, 0, 0, 0.9);">由于DeepSeek R1采用FP8精度训练，所以开源的原生权重就是FP8精度。在推理时，为了尽可能地降低模型精度损失，同时保持和FP8类似的推理吞吐，我们自然想到使用和FP8精度等位宽的INT8精度进行平替。同时，INT8精度被广泛硬件原生支持，基于INT8精度可以极大拓展DeepSeek模型的硬件部署范围。因此，我们开始探索INT8量化在DeepSeek R1上的可行性。</font>

:::color5
**<font style="color:#601BDE;">2.量化基本原理</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">模型量化是将</font>**<font style="color:#ED740C;">模型的权重和激活值</font>**<font style="color:rgba(0, 0, 0, 0.9);">等数据从高精度（</font><font style="color:rgb(136, 136, 136);">如BF16</font><font style="color:rgba(0, 0, 0, 0.9);">）转化为低精度（</font><font style="color:rgb(136, 136, 136);">如INT8</font><font style="color:rgba(0, 0, 0, 0.9);">），并尽可能保证转化前后模型效果一致的过程。以常见的INT8对称量化为例，量化过程如下所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337390429-4b8650fb-fb0f-492e-bd25-81ff88796695.png)

**<font style="color:rgba(0, 0, 0, 0.9);">1.计算缩放因子 x</font>**<sub>**<font style="color:rgba(0, 0, 0, 0.9);">scale</font>**</sub>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337407391-bf3653a0-7a14-47b6-a9b5-0f1cbebce50e.png)

**<font style="color:rgba(0, 0, 0, 0.9);">2.在适当位置做量化（Quant）和反量化（Dequant）</font>**

<font style="color:rgba(0, 0, 0, 0.9);">量化公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337424665-b2b3c903-2f7d-44f6-ab4d-68a75f7e7f68.png)

<font style="color:rgba(0, 0, 0, 0.9);">反量化公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337432779-1e890c7c-025f-4300-b770-2cb18f7834c3.png)

**<font style="color:rgba(0, 0, 0, 0.9);">3.FP16计算可以转为INT8计算</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337447498-535dedfa-e348-4c4e-8686-2ce5ecac4630.png)

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">量化方案设计</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">我们在综合考虑量化后模型的精度和推理性能后，选择了分块量化（</font><font style="color:rgb(136, 136, 136);">Block-wise Quantization</font><font style="color:rgba(0, 0, 0, 0.9);">）和通道量化（</font><font style="color:rgb(136, 136, 136);">Channel-wise Quantization</font><font style="color:rgba(0, 0, 0, 0.9);">）两种方案。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337805945-8f9f5eb3-2787-46fd-a757-82b553e87c56.png)

1. **分块量化**

**<font style="color:rgba(0, 0, 0, 0.9);">优点：</font>**<font style="color:rgba(0, 0, 0, 0.9);">分块量化是DeepSeek V3/R1降低量化损失的关键技术之一。分块量化通过对权重矩阵的细粒度切分，将量化操作的范围控制在[128, 128]的矩阵内，</font>**<font style="color:#DF2A3F;">减少了分布分散的出现概率，从而很好地控制了每次量化过程中的损失。</font>**

**<font style="color:rgba(0, 0, 0, 0.9);">步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">为了尽可能地减少量化后模型的精度损失，我们延续了DeepSeek训练的量化策略。在实践中，由于DeepSeek官方并没有提供半精度浮点型（</font><font style="color:rgb(136, 136, 136);">BF16</font><font style="color:rgba(0, 0, 0, 0.9);">）的权重，因此首先需要将原生的FP8模型权重反量化成BF16，再分块量化成INT8精度。为了匹配权重的分块量化，激活值采用在线逐token-group的量化方式，</font>**<font style="color:#DF2A3F;">即每个token的嵌入向量分为多个组，逐组进行量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

2. **<font style="color:rgba(0, 0, 0, 0.9);">通道量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>

**<font style="color:rgba(0, 0, 0, 0.9);">优点</font>**<font style="color:rgba(0, 0, 0, 0.9);">：除了上述的分块量化外，我们还探索了更高效的通道量化，</font>**<font style="color:#ED740C;">即权重的每列为一组进行量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">。通道量化在执行完INT8的矩阵乘法后，只需进行一次反量化计算，</font>**<font style="color:#ED740C;">计算开销相比分块量化更低</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">缺点</font>**<font style="color:rgba(0, 0, 0, 0.9);">：由于通道量化在量化一列元素时，更容易遇到离群值（</font><font style="color:rgb(136, 136, 136);">Outlier</font><font style="color:rgba(0, 0, 0, 0.9);">），因此相比分块量化会有更多的精度损失。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">在具体实践中，同样地先将原生FP8的模型权重反量化成BF16，之后逐通道量化成INT8类型。同时，对激活值采用在线逐token量化，最大程度地减少activation的量化损失。</font>

:::color5
**<font style="color:#601BDE;">4.量化效果评估</font>**

:::

1. **精度**

<font style="color:rgba(0, 0, 0, 0.9);">我们分别应用上述两种量化方法，对开源的DeepSeek R1模型进行了INT8量化处理，并在GSM8K和MMLU两个数据集上对量化后的模型进行了精度评估。评估结果如下表所示，相比基线的BF16和FP8模型，两种INT8量化模型的精度基本无损。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741338057133-6ee0243a-711d-418e-b78c-324854de2376.png)

2. **<font style="color:rgba(0, 0, 0, 0.9);">推理速度</font>**

<font style="color:rgba(0, 0, 0, 0.9);">我们在知名开源推理框架SGLang上，对上述两种INT8量化方法进行了推理支持（</font><font style="color:rgba(0, 0, 0, 0.9);">分块量化</font><font style="color:rgba(0, 0, 0, 0.9);">、</font><font style="color:rgba(0, 0, 0, 0.9);">通道量化</font><font style="color:rgba(0, 0, 0, 0.9);">）。SGLang是当前SOTA的开源LLM推理框架，在DeepSeek系列模型上有着最优的推理性能，被业界广泛使用。</font>

<font style="color:rgba(0, 0, 0, 0.9);">以BF16模型为Baseline，我们在A100-80G GPU上对两种INT8模型进行了推理吞吐评估。得益于更低的显存要求，INT8量化模型仅需要16张A100 GPU即可推理，但是BF16模型需要32张A100 GPU。为了比较的公平性，我们统一在32张A100 GPU上进行吞吐测试。结果如下表所示，分块量化的INT8推理相比BF16可以提升33%的吞吐；通道量化的INT8推理得益于更低的反量化开销，可以进一步达到50%的吞吐提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741338086042-9b85a191-e2c6-4e85-b0ab-2b4a9242e84f.png)



