# ⓹ 多模态Reasoning

<!-- source: yuque://zhongxian-iiot9/hlyypb/gvuulh4e7ygcihx8 -->

# <font style="color:rgb(1, 1, 1);">多模态-Reasoning</font>
## Visual-RFT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**视觉强化微调 Visual-RFT (visual reforce finetuning)**

+ <font style="color:rgb(25, 27, 31);">提出 </font>**<font style="color:rgb(25, 27, 31);">Visual-RFT</font>**<font style="color:rgb(25, 27, 31);">：首次将</font>**<font style="color:#ED740C;">基于 </font>**[**<font style="color:#ED740C;">GRPO</font>**](https://zhida.zhihu.com/search?content_id=254647528&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)**<font style="color:#ED740C;"> 的强化学习策略应用于增强 LVLMs 的视觉感知和定位能力</font>**<font style="color:rgb(25, 27, 31);">，解决了数据稀缺场景下的微调问题。</font>
+ <font style="color:rgb(25, 27, 31);">设计</font>**<font style="color:rgb(25, 27, 31);">可验证奖励</font>**<font style="color:rgb(25, 27, 31);">函数：</font>**<font style="color:#ED740C;">为不同视觉任务（如检测、分类）设计了高效的奖励函数</font>**<font style="color:rgb(25, 27, 31);">，简化了奖励计算。</font>
+ <font style="color:rgb(25, 27, 31);">广泛的实验验证：基于</font><font style="color:rgb(25, 27, 31);"> </font>[**<font style="color:rgb(9, 64, 142);">Qwen2-VL-2/7B</font>**](https://zhida.zhihu.com/search?content_id=254647528&content_type=Article&match_order=1&q=Qwen2-VL-2%2F7B&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">在多种视觉任务上验证了 Visual-RFT 的有效性，显著优于 SFT。</font>
+ **<font style="color:rgb(25, 27, 31);">开源</font>**<font style="color:rgb(25, 27, 31);">代码和数据：提供了完整的训练代码、数据集和评估脚本，便于后续研究。</font>

:::

<font style="color:rgb(25, 27, 31);">Visual-RFT首先利用大型视觉语言模型（Large Vision-Language Models, LVLMs）为每个输入生成多个包含推理标记和最终答案的响应，然后通过我们提出的视觉感知可验证奖励函数，结合 </font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（Group Relative Policy Optimization, GRPO）</font>**<font style="color:rgb(25, 27, 31);">等策略优化算法来更新模型。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. <font style="color:rgb(25, 27, 31);">我们引入了 </font>**<font style="color:rgb(25, 27, 31);">视觉强化微调（Visual Reinforcement Fine-Tuning, Visual-RFT）</font>**<font style="color:rgb(25, 27, 31);">，它将带有可验证奖励的强化学习扩展到视觉感知任务，这些任务在</font>**<font style="color:#74B602;">微调数据有限的情况下依然有效</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. <font style="color:rgb(25, 27, 31);">我们</font>**<font style="color:#74B602;">为不同的视觉任务设计了不同的可验证奖励</font>**<font style="color:rgb(25, 27, 31);">，使得奖励计算高效且成本极低。这使得 DeepSeek R1 风格的强化学习能够无缝迁移到 LVLMs。</font>
3. <font style="color:rgb(25, 27, 31);">我们在多种视觉感知任务上进行了广泛的实验，包括</font>**<font style="color:#74B602;">细粒度图像分类、少样本目标检测、推理定位和开放词汇目标检测</font>**<font style="color:rgb(25, 27, 31);">。在所有设置中，Visual-RFT 均取得了显著的性能提升，大幅超越了监督微调基线。</font>
4. <font style="color:rgb(25, 27, 31);">我们在 GitHub 上完全</font>**<font style="color:rgb(25, 27, 31);">开源</font>**<font style="color:rgb(25, 27, 31);">了训练代码、训练数据和评估脚本，以促进进一步的研究。</font>

:::color5
**<font style="color:#601BDE;">2.RFT(强化微调)和SFT的主要区别在于数据</font>**

:::

**<font style="color:rgb(25, 27, 31);">强化微调（RFT）与以往的监督微调（Supervised Fine-Tuning, SFT）的主要区别在于数据效率</font>**<font style="color:rgb(25, 27, 31);">。以往的 SFT 范式直接模仿高质量、精心策划的数据中提供的“真实”答案，因此依赖于大量的训练数据。</font>

<font style="color:rgb(25, 27, 31);">相比之下，RFT 通过评估模型的响应并根据其</font>**<font style="color:#ED740C;">是否正确进行调整，帮助模型通过试错学习</font>**<font style="color:rgb(25, 27, 31);">。因此，</font>**<font style="color:#ED740C;">RFT 特别适用于数据稀缺的领域</font>**<font style="color:rgb(25, 27, 31);">。然而，以往的共识是，RFT 仅应用于科学（例如数学）和代码生成等任务。这是因为数学和编程具有清晰且客观的最终答案或测试用例，使得它们的奖励相对容易验证。在本文中，我们证明了 </font>**<font style="color:#ED740C;">RFT 可以应用于视觉感知任务，而不仅仅是数学和代码领域</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.视觉强化微调</font>**

:::

<font style="color:rgb(25, 27, 31);">视觉强化微调（Visual-RFT）框架。给定问题和视觉图像输入，策略模型生成多个包含推理步骤的响应。随后，使用</font>**<font style="color:rgb(25, 27, 31);">可验证奖励</font>**<font style="color:rgb(25, 27, 31);">（如交并比奖励和分类奖励）结合</font>**<font style="color:rgb(25, 27, 31);">策略梯度优化算法</font>**<font style="color:rgb(25, 27, 31);">来更新策略模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741334693920-bda1b180-762d-494a-ad86-dbd607f8b6a3.png)

**训练步骤**

1. <font style="color:rgb(25, 27, 31);">用户提供的多模态输入数据包括图像和问题。</font>

```python
imag 1
Q:图中卡车那部分是可以打开的？
..
imag n
Q：这朵花是什么品种？
```

2. <font style="color:rgb(25, 27, 31);">策略模型 </font><font style="color:rgb(25, 27, 31);">πθ</font><font style="color:rgb(25, 27, 31);"> 输出推理过程，并基于输入生成一组输出。</font>

```python
imag 1
A:<think>卡车有一个可以打开的门，在车的右边...</think>
..
imag n
Q：<think>这朵花似乎是哥伦比亚花，有五个黄色花瓣...</think><answer>哥伦比亚花</answer>
```

3. <font style="color:rgb(25, 27, 31);">每个响应通过</font>**<font style="color:rgb(25, 27, 31);">可验证奖励函数</font>**<font style="color:rgb(25, 27, 31);">计算奖励（</font>**<font style="color:#ED740C;">判断输出是否正确，给出打分评价</font>**<font style="color:rgb(25, 27, 31);">）。</font>
    1. <font style="color:rgb(25, 27, 31);">DeepSeek-R1 模型通过可验证奖励设计，在模型的推理能力上取得了显著提升。为了将这一策略转移到视觉领域，我们</font>**<font style="color:#ED740C;">为各种视觉感知任务设计了不同的基于规则的可验证奖励函数</font>**<font style="color:rgb(25, 27, 31);">。</font>
    2. **<font style="color:rgb(25, 27, 31);">检测任务中的交并比（IoU）奖励。IoU 奖励（RIoU）</font>**<font style="color:rgb(25, 27, 31);">：是模型输出中所有边界框的平均 IoU</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335260714-164fb956-d8f2-411e-94cb-7da4a40c2ed7.png)

    3. **<font style="color:rgb(25, 27, 31);">分类任务中的分类奖励（CLS Reward）：</font>**<font style="color:rgb(25, 27, 31);">在分类任务中，我们使用的奖励函数包含两部分：准确率奖励 Racc 和格式奖励 Rformat。准确率奖励通过比较模型输出的类别与真实类别来确定，正确分类得 1 分，错误分类得 0 分</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335300737-e056e0e2-782d-4b40-ae5e-667298eb1546.png)

4. <font style="color:rgb(25, 27, 31);">在对每个输出进行群体奖励计算后，评估每个响应的质量，并用于更新策略模型。</font>
    1. <font style="color:rgb(25, 27, 31);">为了确保策略模型训练的稳定性，Visual-RFT 使用</font>**<font style="color:rgb(25, 27, 31);"> KL 散度</font>**<font style="color:rgb(25, 27, 31);"> 限制策略模型与参考模型之间的差异。</font>

:::color5
**<font style="color:#601BDE;">4.数据准备</font>**

:::

<font style="color:rgb(25, 27, 31);">为了在各种视觉感知任务上训练 Visual-RFT，我们需要构建多模态训练数据集。与 DeepSeek-R1 类似，为了增强模型的推理能力，并将其应用于提升视觉感知能力，Visual-RFT </font>**<font style="color:#ED740C;">设计了一种提示格式，引导模型在输出最终答案之前</font>****<font style="color:#DF2A3F;">展示其推理过程（think)</font>**<font style="color:rgb(25, 27, 31);">。检测和分类任务中使用的提示格式如表 1 所示。</font>

1. **Detection Prompt**![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335490603-c16cf0e3-8ff4-43a8-bf25-9a0a133c37d1.png)**2. Classification Prompt**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335496202-114105e4-f520-4fa0-985d-5ef63ebdd0e0.png)

:::color5
**<font style="color:#601BDE;">5.效果评估</font>**

:::

<font style="color:rgb(25, 27, 31);">广泛的实验表明，Visual-RFT 在细粒度分类、开放词汇检测、推理定位和少样本学习任务中表现出色。它</font>**<font style="color:rgb(25, 27, 31);">在数据量极少的情况下优于监督微调（SFT）</font>**<font style="color:rgb(25, 27, 31);">，并展现出强大的泛化能力。这项工作展示了强化学习增强 LVLMs 能力的潜力，使它们在视觉感知任务中更加高效和有效。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741333444294-84ba8e29-f966-451c-97b2-1ead9476673f.png)



## VLM-R1
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(25, 27, 31);">VLM-R1 是一款基于强化学习技术的视觉语言模型，能够通过自然语言指令精确定位图像目标，并支持多模态推理。  
</font><font style="color:rgb(25, 27, 31);">1. </font>**<font style="color:rgb(25, 27, 31);">指代表达理解</font>**<font style="color:rgb(25, 27, 31);">：解析自然语言指令，精准定位图像中的特定目标。  
</font><font style="color:rgb(25, 27, 31);">2. </font>**<font style="color:rgb(25, 27, 31);">强化学习优化</font>**<font style="color:rgb(25, 27, 31);">：采用 </font>[<font style="color:rgb(9, 64, 142);">GRPO</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 技术，在复杂场景下表现出色，提升泛化能力。</font>

**<font style="color:rgb(25, 27, 31);">github</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://github.com/om-ai-lab/VLM-R1](https://github.com/om-ai-lab/VLM-R1)

:::

<font style="color:rgb(25, 27, 31);">VLM-R1 是浙江大学 Om AI Lab 开发的一款基于强化学习技术的视觉语言模型，旨在通过自然语言指令精确定位图像中的目标物体。例如，用户可以通过描述“图中红色的杯子”来让模型找到对应的图像区域。该模型基于 </font>[**<font style="color:rgb(9, 64, 142);">Qwen2.5-VL</font>**](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=Qwen2.5-VL&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 架构，结合了 </font>[**<font style="color:rgb(9, 64, 142);">DeepSeek R1</font>**](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=DeepSeek+R1&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的强化学习方法，通过强化学习优化和监督微调（SFT）提升了模型的稳定性和泛化能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741316928362-b7a08f1d-fce8-4952-9b64-fd2b9fd5bc27.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">GRPO 强化学习技术</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">采用 Group Relative Policy Optimization（GRPO）方法</font>**<font style="color:rgb(25, 27, 31);">，使模型在复杂场景下自我探索，减少对大量标注数据的依赖。</font>
+ **<font style="color:rgb(25, 27, 31);">泛化能力与稳定性提升</font>**<font style="color:rgb(25, 27, 31);">：相比传统的监督微调（SFT）方法，VLM-R1 在领域外测试数据中表现出持续提升的性能，表明其真正掌握了视觉内容的理解能力，而不仅仅是依赖记忆。</font>
+ **<font style="color:rgb(25, 27, 31);">基于 Qwen2.5-VL 架构</font>**<font style="color:rgb(25, 27, 31);">：在 Qwen2.5-VL 的基础上开发，通过强化学习优化，在多种复杂场景中保持稳定和高效的性能。</font>

:::color5
**<font style="color:#601BDE;">2.主要功能</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">指代表达理解（REC）</font>**<font style="color:rgb(25, 27, 31);">：解析自然语言指令，精确定位图像中的特定目标，如根据描述“图中红色的杯子”找到对应区域。</font>
+ **<font style="color:rgb(25, 27, 31);">图像与文本联合处理</font>**<font style="color:rgb(25, 27, 31);">：支持同时输入图像和文字，生成准确的分析结果。</font>
+ **<font style="color:rgb(25, 27, 31);">强化学习优化</font>**<font style="color:rgb(25, 27, 31);">：通过 GRPO（Group Relative Policy Optimization）技术，提升模型在复杂场景下的表现和泛化能力。</font>
+ **<font style="color:rgb(25, 27, 31);">高效训练与推理</font>**<font style="color:rgb(25, 27, 31);">：采用 Flash Attention 等技术，支持单 GPU 训练大规模参数模型，提升计算效率。</font>
+ **<font style="color:rgb(25, 27, 31);">多模态推理与知识生成</font>**<font style="color:rgb(25, 27, 31);">：不仅能识别图像内容，还能进行逻辑推理和文本表达，例如识别蛋白质含量最高的食物并解释原因。</font>
+ **<font style="color:rgb(25, 27, 31);">易用性与开源性</font>**<font style="color:rgb(25, 27, 31);">：提供完整的训练和评估流程，开发者可以快速上手，四步即可开始训练。</font>

:::color5
**<font style="color:#601BDE;">3.GRPO在VLM中怎么做</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">如何迁移到多模态的疑问</font>**<font style="color:rgb(25, 27, 31);">：r1是用的规则奖励函数，而vlm的训练数据，很多是这种格式的： q + image -> a，那vlm是怎么跟r1结合到一起的？ 所以笔者去瞧了瞧，简单分享下这个项目是怎么把grpo迁移到vlm上的。</font>
2. **system prompt**

```yaml
用户和助手之间的对话。用户提出问题，助手解决问题。助手“首先在脑海中思考推理过程，然后为用户提供答案。推理”“过程和答案分别包含在<think></think>和<answer></answer>标签中，即“<think>推理过程在这里</hthink><answer>回答在这里</sanswer>”
```

2. **GRPO prompt**

```yaml
“｛Question｝首先在<think></think>标签中输出思考过程，然后在<answer></answer>标签中输入最终答案。以JSON格式输出最终答案。”
```

3. **奖励函数**

<font style="color:rgb(25, 27, 31);">一个格式奖励函数，一个IOU</font>[<font style="color:rgb(9, 64, 142);">函数</font>](https://zhida.zhihu.com/search?content_id=254040458&content_type=Article&match_order=1&q=iou%E5%87%BD%E6%95%B0&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。IOU是目标检测中一个常见的度量标准， 简单来说两个框的交集面积除以并集面积的比值。判断是否大于0.5，给予奖励。</font>

<font style="color:rgb(25, 27, 31);">数据构造：把那个描述构造成问题，然后让模型预测框框的位置，这样就可以写出规则奖励函数了。</font>

```yaml
Question = “请提供输入语言描述区域的bounding box。”
```

:::color5
**<font style="color:#601BDE;">4.评测</font>**

:::

<font style="color:rgb(25, 27, 31);">左图是测试相同领域评测结果，右图是out-of-domain的评测结果。随着训练步骤增加，grpo相比sft都有明显优势，sft更容易过拟合。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741317431287-e98b46f9-ddce-440a-9669-528ca28d4a8d.png)

:::color5
**<font style="color:#601BDE;">5.如何运行VLM-R1</font>**

:::

1. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">环境搭建</font>**

<font style="color:rgb(25, 27, 31);">在开始运行 VLM-R1 模型之前，需要配置运行环境。以下是环境搭建的步骤：</font>

```plain
conda create -n vlm-r1 python=3.10
conda activate vlm-r1
bash setup.sh
```

<font style="color:rgb(25, 27, 31);">通过上述命令，创建并激活一个名为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">vlm-r1</font>`<font style="color:rgb(25, 27, 31);"> 的 Python 环境，并运行 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">setup.sh</font>`<font style="color:rgb(25, 27, 31);"> 脚本来安装依赖。</font>

2. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">数据准备</font>**

<font style="color:rgb(25, 27, 31);">VLM-R1 模型的训练需要准备图像数据和标注文件。以下是数据准备的详细步骤：</font>

**<font style="color:rgb(25, 27, 31);">(1)下载图像数据</font>**

<font style="color:rgb(25, 27, 31);">下载</font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">COCO Train2014</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=COCO+Train2014&zhida_source=entity)<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"> </font><font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">图像数据</font>`<font style="color:rgb(25, 27, 31);">并解压，将图像文件夹路径记为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><your_image_root></font>`<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">COCO Train2014 图像数据</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://huggingface.co/datasets/omlab/VLM-R1/resolve/main/train2014.zip](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/omlab/VLM-R1/resolve/main/train2014.zip)

**<font style="color:rgb(25, 27, 31);">(2)下载标注文件</font>**

<font style="color:rgb(25, 27, 31);">下载</font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">RefCOCO/+</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=RefCOCO%2F%2B&zhida_source=entity)<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">/g 和</font><font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"> </font>[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">RefGTA</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=RefGTA&zhida_source=entity)<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"> </font><font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">标注文件</font>`<font style="color:rgb(25, 27, 31);">并解压。RefGTA 用于域外评估。</font>

+ **<font style="color:rgb(25, 27, 31);">RefCOCO/+/g 和 RefGTA 标注文件</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://huggingface.co/datasets/omlab/VLM-R1/resolve/main/rec_jsons_processed.zip](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/omlab/VLM-R1/resolve/main/rec_jsons_processed.zip)

**<font style="color:rgb(25, 27, 31);">(3) 配置标注文件路径</font>**

<font style="color:rgb(25, 27, 31);">在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">src/open-r1-multimodal/data_config/rec.yaml</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">文件中，填写标注文件的路径。例如：</font>

```plain
datasets:
    - json_path: /path/to/refcoco_train.json
    - json_path: /path/to/refcocop_train.json
    - json_path: /path/to/refcocog_train.json
```

3. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">模型训练</font>**

<font style="color:rgb(25, 27, 31);">VLM-R1 提供了两种训练方法：GRPO 和 SFT。以下是两种方法的详细步骤。</font>

**<font style="color:rgb(25, 27, 31);">(1) GRPO 方法</font>**

<font style="color:rgb(25, 27, 31);">运行以下命令以启动 GRPO 方法的训练：</font>

```plain
cd src/open-r1-multimodal

torchrun --nproc_per_node="8" \
    --nnodes="1" \
    --node_rank="0" \
    --master_addr="127.0.0.1" \
    --master_port="12346" \
    src/open_r1/grpo_rec.py \
    --deepspeed local_scripts/zero3.json \
    --output_dir output/$RUN_NAME \
    --model_name_or_path Qwen/Qwen2.5-VL-3B-Instruct \
    --dataset_name data_config/rec.yaml \
    --image_root <your_image_root> \
    --max_prompt_length 1024 \
    --num_generations 8 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 2 \
    --logging_steps 1 \
    --bf16 \
    --torch_dtype bfloat16 \
    --data_seed 42 \
    --report_to wandb \
    --gradient_checkpointing false \
    --attn_implementation flash_attention_2 \
    --num_train_epochs 2 \
    --run_name $RUN_NAME \
    --save_steps 100 \
    --save_only_model true
```

<font style="color:rgb(25, 27, 31);">如果遇到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">CUDA out of memory</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">错误，可以尝试以下方法： 1. 设置</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">gradient_checkpointing</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">true</font>`<font style="color:rgb(25, 27, 31);">。 2. 减少</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">num_generations</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的值。 3. 使用 LoRA 方法。</font>

**<font style="color:rgb(25, 27, 31);">(2) SFT 方法</font>**

<font style="color:rgb(25, 27, 31);">首先，克隆</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory</font>`<font style="color:rgb(25, 27, 31);">仓库并安装依赖：</font>

+ **<font style="color:rgb(25, 27, 31);">LLaMA-Factory 仓库</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/hiyouga/LLaMA-Factory](https://link.zhihu.com/?target=https%3A//github.com/hiyouga/LLaMA-Factory)

```plain
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

<font style="color:rgb(25, 27, 31);">接着，下载提供的 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">dataset_info.json</font>`<font style="color:rgb(25, 27, 31);">、</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">mllm_rec_json.json</font>`<font style="color:rgb(25, 27, 31);"> 和 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">qwen2_5_vl_full_sft.yaml</font>`<font style="color:rgb(25, 27, 31);"> 文件，分别放置在 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory/data</font>`<font style="color:rgb(25, 27, 31);"> 和 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory/examples/train_full</font>`<font style="color:rgb(25, 27, 31);"> 目录中。</font>

<font style="color:rgb(25, 27, 31);">最后，运行以下命令以启动 SFT 方法的训练：</font>

```plain
llamafactory-cli train examples/train_full/qwen2_5_vl_full_sft.yaml
```

4. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">自定义数据支持</font>**

<font style="color:rgb(25, 27, 31);">VLM-R1 支持自定义数据的加载，数据格式需为 JSONL 文件。以下是数据格式示例：</font>

```plain
{"id": 1, "image": "Clevr_CoGenT_TrainA_R1/data/images/CLEVR_trainA_000001_16885.png", "conversations": [{"from": "human", "value": "<image>What number of purple metallic balls are there?"}, {"from": "gpt", "value": "0"}]}
```

**<font style="color:rgb(25, 27, 31);">(1) 注意事项</font>**

1. <font style="color:rgb(25, 27, 31);">JSONL 文件中的图像路径应为相对于</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">--image_folders</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">指定的文件夹路径。</font>
2. <font style="color:rgb(25, 27, 31);">多个数据文件和图像文件夹可以通过</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">:</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">分隔。例如：</font>

```plain
--data_file_paths /path/to/data1.jsonl:/path/to/data2.jsonl \
--image_folders /path/to/images1/:/path/to/images2/
```

**<font style="color:rgb(25, 27, 31);">(2) 加载自定义数据</font>**

<font style="color:rgb(25, 27, 31);">运行以下命令以加载自定义数据：</font>

```plain
torchrun --nproc_per_node="8" \
    --nnodes="1" \
    --node_rank="0" \
    --master_addr="127.0.0.1" \
    --master_port="12345" \
  src/open_r1/grpo_jsonl.py \
    --output_dir output/$RUN_NAME \
    --model_name_or_path Qwen/Qwen2.5-VL-3B-Instruct \
    --deepspeed local_scripts/zero3.json \
    --dataset_name <your_dataset_name> \
    --data_file_paths /path/to/your/data.jsonl \
    --image_folders /path/to/your/image/folder/
```

5. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">模型评估</font>**

<font style="color:rgb(25, 27, 31);">模型训练完成后，可以使用以下命令进行评估：</font>

```plain
cd ./src/eval

# 修改脚本中的模型路径、图像根目录和标注文件路径
python test_rec_r1.py # 用于 GRPO 方法
python test_rec_baseline.py # 用于 SFT 方法
```



## Vision-R1
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近两年，大模型（LLM）在各个领域大放异彩，从语言理解到图像识别，都出现了突破性的进展。然而，想要</font>**<font style="color:#117CEE;">让模型真正地“像人一样”去进行推理、思考与解释，仍是一项极富挑战性的任务</font>**<font style="color:rgb(25, 27, 31);">。以往我们大多在文本领域探索如何“让模型有自己的思维过程”（如链式思考 Chain-of-Thought），而在多模态领域（尤其是图文结合的情境）——如何把</font>**<font style="color:#117CEE;">视觉信息与语言信息进行深度融合并激发复杂的推理能力</font>**<font style="color:rgb(25, 27, 31);">，还远远没有走到头。</font>

<font style="color:rgb(25, 27, 31);">为此，本文针对多模态大模型（Multimodal LLM，简称 MLLM）的“推理能力激发”展开研究，并提出了一个全新的解决方案，名为</font><font style="color:#74B602;"> </font>**<font style="color:#74B602;">Vision-R1</font>**<font style="color:#74B602;">。</font>**<font style="color:#74B602;">它在视觉和语言的结合中，实现了用“强化学习（RL）+ 冷启动（Cold Start）”的方式，去让模型自发地产生更复杂、更类似于人类思考的推理链。</font>**

:::

:::color3
**简介：****<font style="color:#117CEE;">仅靠强化学习（RL）无法有效激励多模态大型语言模型（MLLM）的推理能力，主要原因是缺乏高质量初始数据和优化策略。</font>**<font style="color:rgb(25, 27, 31);">Vision-R1 提出了一条“冷启动+强化学习”相结合的训练路径，为多模态大模型（MLLM）注入类人式思维与推理能力。具体而言，</font>**<font style="color:#74B602;">先通过“模态桥接（Modality Bridging）”方法大规模生成高质量多模态推理数据并进行冷启动初始化</font>**<font style="color:rgb(25, 27, 31);">；随后利用</font>**<font style="color:#74B602;">渐进式思维抑制训练（</font>**[**<font style="color:#74B602;">PTST</font>**](https://zhida.zhihu.com/search?content_id=254946168&content_type=Article&match_order=1&q=PTST&zhida_source=entity)**<font style="color:#74B602;">）与强化学习相结合</font>**<font style="color:rgb(25, 27, 31);">，逐步引导模型掌握正确且复杂的推理过程。实验表明，Vision-R1-7B 参数规模的模型便能在多项数理推理基准上逼近甚至超越 70B+ 大模型的表现。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Osilly/Vision-R1](https://github.com/Osilly/Vision-R1)

**paper：**[**Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models**](https://arxiv.org/pdf/2503.06749)

**参考：**[**https://zhuanlan.zhihu.com/p/29618155786**](https://zhuanlan.zhihu.com/p/29618155786)

:::

:::color5
**<font style="color:#601BDE;">1.研究动机</font>**

:::

<font style="color:rgb(25, 27, 31);">1.</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">语言大模型的推理火热，但多模态推理仍是短板</font>**

<font style="color:rgb(25, 27, 31);">近年来，纯文本领域的推理方法（如“链式思考”、Tree-of-Thought 等）发展迅速，证明了在文本任务中，通过显式的多步推理，可以极大提升模型在复杂问题上的表现。然而，这些方法大多只聚焦在文字输入上，很少考虑视觉信息。</font>**<font style="color:#117CEE;">多模态模型若只停留在“根据图像简单识别+给出答案”，常常难以在高难度推理场景（如数学场景的图文结合推理、几何题带图解等）表现优异</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">2.</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">直接用强化学习在多模态模型上激发“自发思考”并不容易</font>**

<font style="color:rgb(25, 27, 31);">在纯文本模型上，已有工作（如 DeepSeek-R1）表明，利用强化学习去激发模型自我生成更复杂的推理链，确实有效。但想</font>**<font style="color:#117CEE;">直接将这种强化学习方法“照搬”到多模态模型，会面临数据稀缺、模型过度胡乱生成长推理链等问题，导致效果不佳</font>**<font style="color:rgb(25, 27, 31);">。因此，需要一个辅助的冷启动初始化步骤来帮助模型先学会“如何思考”，然后再进行强化学习，以提升推理过程的正确性与稳健性。</font>

<font style="color:rgb(25, 27, 31);">3.</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">缺乏大规模高质量多模态推理数据</font>**

<font style="color:rgb(25, 27, 31);">人工标注的图文推理数据往往只包含简单的“图像描述+答案”，很少显式写出内在的思考过程，即便有也通常比较“形式化”，缺乏像人类一样的“自我质疑”“多步检验”。</font>**<font style="color:#117CEE;">如何构建能体现“人类式推理”的多模态数据，是推动 MLLM 学习复杂推理的关键</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">目标：</font>**

+ <font style="color:rgb(25, 27, 31);">生成高质量的多模态推理链（CoT）数据集，无需人工标注。</font>
+ <font style="color:rgb(25, 27, 31);">通过 RL 优化模型，使其生成逻辑清晰、长度适中的 CoT，避免过度思考（Overthinking）。</font>

:::color5
**<font style="color:#601BDE;">2.Vision-R1 pipeline</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744610218132-f1874efd-d72a-49ba-891b-e93a78d70d58.png)

Vision-R1流程。首先利用现有的MLLM和[DeepSeek-R1](https://zhida.zhihu.com/search?content_id=254946168&content_type=Article&match_order=1&q=DeepSeek-R1&zhida_source=entity)获得高质量的Multimodal CoT数据集，将其作为基础MLLM的冷启动初始化数据，从而得到经过冷启动后的Vision-R1-CI，然后在Vision-R1-CI上进行强化学习（RL）训练，最终获得具备推理能力的MLLM，即Vision-R1。  
	我们观察到，直接在MLLM上应用RL无法有效地激发出强大的推理能力（参见(C)和(D)）。未经初始化直接通过RL训练的Vision-R1-Zero难以从有限的数据中泛化（参见(E)、(F)，特别指出Vision-R1-Zero应用了format reward function）。而Vision-R1-CI则面临“过度思考优化问题（Overthinking Optimization Problem）”，偏好较短的CoT推理序列，即正确的推理过程主要集中在较短的CoT推理序列中（参见(A)）。在后续的RL训练中，我们观察到推理步骤虽然有所延长，但性能却出现下降（参见(D)和(E)），这使得优化尤为困难。而Vision-R1则首先在RL训练下缩短CoT，以精炼正确的思考过程。PTST使Vision-R1逐步获得更为复杂的推理过程（参见(C)、(D)和(E)），性能得以提升，因此我们的Vision-R1以70亿参数实现了与具有700亿以上参数的最强MLLM相当的性能（参见(B)）。注意，Vision-R1使用了不同颜色的线条来表示PTST中的不同阶段。

:::color5
**<font style="color:#601BDE;">3.数据合成pipeline</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744610119279-268e2a66-4fdd-4e72-b86c-68c3ced7a91e.png)

整体的数据生成流程，融合了我们的模态桥接（Modality Bridging）方法。首先将多模态数据送入MLLM，以获取包含图像描述（caption）和推理过程的“Pseudo-CoT”，并将其与原始的图像-问题对一起作为MLLM的输入，以生成详细的文本描述。通过这种模态桥接方法，文本描述向DeepSeek-R1提供了全面的信息，有助于生成高质量的CoT推理过程。这些推理过程经过后处理，与原始数据整合后，最终形成Vision-R1-cold数据集。

**实现细节**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612056366-1bd3e083-a561-4989-9b82-c378f09ddb9e.png)

1. **<font style="color:rgb(25, 27, 31);">伪CoT生成</font>**<font style="color:rgb(25, 27, 31);">：首先，使用现有的多模态大型语言模型（MLLM）来生成“伪CoT”（Pseudo-CoT）。具体的，输入一个图像-问题-答案对和一个提示到一个MLLM中，模型会生成一个包含图像描述和推理过程的文本。这个“伪CoT”不仅包含了图像的描述，还尝试进行初步的推理，但可能缺乏深度和复杂性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612131128-77febf08-96d2-4f16-aee8-f64fdf6888c8.png)

2. **<font style="color:rgb(25, 27, 31);">文本描述生成</font>**<font style="color:rgb(25, 27, 31);">：将生成的“伪CoT”与原始的图像-问题对以及一个新的提示一起输入到同一个MLLM中，以获取更详细的图像描述。这一步骤的目的是通过MLLM的文本生成能力，将图像中的视觉信息转化为更详细的文本描述，从而为后续的推理提供更多的上下文信息。</font>
3. **<font style="color:rgb(25, 27, 31);">推理生成</font>**<font style="color:rgb(25, 27, 31);">：将经过文本化的图像-问题对输入到一个专门的推理大型语言模型（如</font>**<font style="color:rgb(25, 27, 31);">DeepSeek-R1</font>**<font style="color:rgb(25, 27, 31);">）中，以生成高质量的CoT推理过程。DeepSeek-R1能够生成包含自然认知过程的推理过程，如质疑、反思和检查等。</font>
4. **<font style="color:rgb(25, 27, 31);">数据过滤</font>**<font style="color:rgb(25, 27, 31);">：从生成的CoT数据中保留那些最终答案与真实值一致的样本。使用规则进行数据过滤，去除逻辑不一致的样本，并替换一些词汇以提高语义连贯性。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法：渐进式思维抑制训练（PTST）</font>**

:::

<font style="color:rgb(25, 27, 31);">为了解决冷启动后的过度思考问题，Vision-R1 采用渐进式思维抑制训练（PTST），通过 RL 进一步优化模型的推理能力。</font>

+ **<font style="color:rgb(25, 27, 31);">分组相对策略优化（GRPO）：</font>**<font style="color:rgb(25, 27, 31);"> GRPO 是一种 RL 算法，通过分组类似状态或动作来优化策略，提高学习效率。 详细的可参考往期《</font>[DeepSeek采用的GRPO算法数学原理及算法过程浅析](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg4NjI0NDg0Ng%3D%3D%26mid%3D2247487491%26idx%3D1%26sn%3De3e2c5a43b107c16b12a0bfcd0c0de75%26chksm%3Dcf9dc482f8ea4d94a382afa4903869f0d3ffe660dfaeae2e71e50fcc580b30e1bced687622c9%26scene%3D178%26cur_album_id%3D2829992858538491905%23rd)<font style="color:rgb(25, 27, 31);">》</font>
+ **<font style="color:rgb(25, 27, 31);">硬格式结果奖励函数（HFRRF）：</font>**<font style="color:rgb(25, 27, 31);"> 奖励函数简单：如果输出格式正确且答案正确，则奖励为 1，否则为 0。</font>
+ **<font style="color:rgb(25, 27, 31);">分阶段训练：</font>**<font style="color:rgb(25, 27, 31);"> 训练分为多个阶段，逐步增加序列长度（如 4K、8K、16K 标记）和调整组大小（如 16、8、4）。</font>
    - <font style="color:rgb(25, 27, 31);">每个阶段训练 100 步，使用 64 个 </font>[<font style="color:rgb(9, 64, 142);">NVIDIA H800 80G GPU</font>](https://zhida.zhihu.com/search?content_id=255000916&content_type=Article&match_order=1&q=NVIDIA+H800+80G+GPU&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，约 2 天，使用 Verl 框架。</font>
    - <font style="color:rgb(25, 27, 31);">与固定长度 16K、300 步训练的 Vision-R1-Long 相比，PTST 表现更好，平均长度 2057，平均准确率 55.4%。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

**<font style="color:rgb(25, 27, 31);">1. 效果对比</font>**

<font style="color:rgb(25, 27, 31);">• 在多项数理推理（包含图文几何推理、方程推导等）基准上，Vision-R1-7B 尺度的模型，已经能与一些 70B+ 参数的大模型旗鼓相当。例如，在 MathVista、MathVerse、MM-Math 等基准上，Vision-R1-7B 都取得了显著提升，</font>**<font style="color:rgb(25, 27, 31);">在MathVista上，Vision-R1-7B 73.5分，接近OpenAI o1的73.9</font>**<font style="color:rgb(25, 27, 31);">。 某些子任务（如几何推理）甚至逼近或超越现有最优水平。</font>

<font style="color:rgb(25, 27, 31);">• 说明只要</font>**<font style="color:#74B602;">“冷启动 + 强化学习”得当，中小参数量的多模态模型，也能产生相当强的推理能力</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">2. 人类式思维过程的可观测性</font>**

<font style="color:rgb(25, 27, 31);">• 论文中展示了 Vision-R1 的多步推理示例，能看到模型在回答一个几何题时，会出现类似人类的“嗯？我再检查一下”“好像上一步有点问题，让我再重新推一下”等</font>**<font style="color:#74B602;">自我质疑、思考的字句</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">• 这表明在训练中确实</font>**<font style="color:#74B602;">激发了模型的“自发思考”模式</font>**<font style="color:rgb(25, 27, 31);">，而不仅仅是机械地输出一长串无效的步骤。</font>

**<font style="color:rgb(25, 27, 31);">3. 渐进训练的优势</font>**

<font style="color:rgb(25, 27, 31);">• 实验还对比了如果没有分阶段抑制推理长度，模型要么推理很短（零强化学习），要么推理超长但正确率显著下降（直接用 16K tokens 长度训练）。</font>**<font style="color:#74B602;">通过“逐步放宽推理长度”的方式，能帮助 Vision-R1 获得优质的平衡</font>**<font style="color:rgb(25, 27, 31);">：既能长推理，又不至于陷入胡乱瞎想的陷阱。</font>

:::color5
**<font style="color:#601BDE;">6.总结 & 展望</font>**

:::

**<font style="color:rgb(25, 27, 31);">总结：Vision-R1</font>**<font style="color:rgb(25, 27, 31);"> 的工作提供了一个有意思的思路：</font>

<font style="color:rgb(25, 27, 31);">• 首先利用已有多模态模型与高质量文本推理模型，通过“模态桥接”构造大量“人类式思维”的数据，为 MLLM 做一个冷启动；</font>

<font style="color:rgb(25, 27, 31);">• 再通过严格的奖励设计和分阶段策略，在强化学习中逐步激发更高级的推理链。</font>

<font style="color:rgb(25, 27, 31);">从实验结果看，这样的技术路线能显著提升多模态模型在复杂推理任务（尤其是图文结合数学推理）上的表现，也为后续大模型如何结合视觉、语言并启用更深层次思考提供了新思路。</font>

**<font style="color:rgb(25, 27, 31);">未来思考：</font>**

<font style="color:rgb(25, 27, 31);">1. 模型能否迁移到视频、三维、以及更多模态的复杂推理场景？</font>

<font style="color:rgb(25, 27, 31);">2. 是否可以结合其他RL算法比如DAPO、VAPO以及多模态PRM来进一步稳定强化学习过程，并提升性能上限？</font>

<font style="color:rgb(25, 27, 31);">3. 如何让多模态推理不仅有“解释可读性”，还要兼顾“鲁棒性”和“正确性”，尤其减少模型产生的不合理自我纠正和幻觉？</font>

<font style="color:rgb(25, 27, 31);">尽管还有很多问题值得探索，但 Vision-R1 的研究已经为“多模态大模型的深层推理”这条赛道，注入了新的可能性与动力。</font>

## Video-R1
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">当前的多模态大模型（MLLMs）在处理视频时存在一个根本性问题：</font>**<font style="color:#117CEE;">它们往往无法有效利用视频中的时序信息</font>**<font style="color:rgb(25, 27, 31);">。想象一下，如果你只看电影的几个随机截图，而不是按顺序观看整部电影，你能理解剧情吗？显然不能。但这正是当前多模态大模型的工作方式——它们更像是在处理一系列独立的图像，而非真正理解视频中的时序变化。</font>

<font style="color:rgb(25, 27, 31);">另一个挑战是</font>**<font style="color:#117CEE;">高质量视频推理数据的稀缺</font>**<font style="color:rgb(25, 27, 31);">。现有的视频数据集主要集中在简单的识别任务上，缺乏需要复杂推理能力的数据，这使得模型很难学习到真正的视频推理能力。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了解决这些问题，研究团队提出了两个创新方案。（1）</font>**<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。（2）针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/tulerfeng/Video-R1](https://github.com/tulerfeng/Video-R1)

**paper：**[**Video-R1: Reinforcing Video Reasoning in MLLMs**](https://arxiv.org/pdf/2503.21776)

**参考：**[**https://zhuanlan.zhihu.com/p/1889342435928282728**](https://zhuanlan.zhihu.com/p/1889342435928282728)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602200071-763ca10e-6dd5-42bc-bae9-f7fe62dcee02.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。这是对原有GRPO算法的扩展，专门设计用于</font>**<font style="color:#74B602;">鼓励模型进行时序推理</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. <font style="color:rgb(25, 27, 31);">针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。他们构建了两个数据集：</font>
    1. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">Video-R1-COT-165k</font>**<font style="color:rgb(25, 27, 31);">：用于监督微调（SFT）的数据集，包含具有思维链（Chain-of-Thought）注释的图像和视频样本。</font>
    2. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">Video-R1-260k</font>**<font style="color:rgb(25, 27, 31);">：用于强化学习（RL）训练的数据集，包含多种类型的图像和视频推理任务。</font>

:::color5
**<font style="color:#601BDE;">2.T-GRPO算法（Temporal Group Relative Policy Optimization，时序群组相对策略优化）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744601979834-580a4129-df2b-4699-afe6-57c9e06d78fb.png)

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。这是对原有GRPO算法的扩展，专门设计用于鼓励模型进行时序推理。</font>

**<font style="color:rgb(25, 27, 31);">T-GRPO的核心思想非常巧妙</font>**<font style="color:rgb(25, 27, 31);">：在训练过程中，模型会同时处理</font>**<font style="color:#74B602;">两种视频输入</font>**<font style="color:#74B602;">——</font>**<font style="color:#74B602;">按时间顺序排列的帧序列和随机打乱的帧序列</font>**<font style="color:rgb(25, 27, 31);">。如果模型在有序序列上的表现优于乱序序列，它就会获得正向奖励。这种对比机制有效地鼓励模型利用帧间的时序关系进行推理，而不是仅仅依赖于单帧图像中的视觉特征。</font>

:::color5
**<font style="color:#601BDE;">3.训练数据</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602073812-c3c90af5-55aa-4f9a-8600-1549f9e496a2.png)

<font style="color:rgb(25, 27, 31);">其次，针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。他们构建了两个数据集：</font>

<font style="color:rgb(25, 27, 31);">（1）</font>**<font style="color:rgb(25, 27, 31);">Video-R1-COT-165k</font>**<font style="color:rgb(25, 27, 31);">：用于监督微调（SFT）的数据集，包含具有思维链（Chain-of-Thought）注释的图像和视频样本。</font>

<font style="color:rgb(25, 27, 31);">（2）</font>**<font style="color:rgb(25, 27, 31);">Video-R1-260k</font>**<font style="color:rgb(25, 27, 31);">：用于强化学习（RL）训练的数据集，包含多种类型的图像和视频推理任务。</font>

<font style="color:rgb(25, 27, 31);">这种混合训练方式使模型能够从图像中学习到基础推理技能，再将这些技能迁移到视频领域，从而有效克服了视频推理数据稀缺的问题。</font>

:::color5
**<font style="color:#601BDE;">4.评估</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602107401-1ffbcfd1-715c-4fd7-ab34-a8db348ea124.png)

<font style="color:rgb(25, 27, 31);">研究团队在多个视频理解和推理基准测试上评估了Video-R1的性能，结果令人印象深刻：</font>

**<font style="color:rgb(25, 27, 31);">在VSI-Bench（一个视频空间推理基准测试）上，Video-R1-7B达到了35.8%的准确率，超越了商业专有模型GPT-4o</font>**<font style="color:rgb(25, 27, 31);">，而它仅使用了32帧输入和7B参数。这一结果凸显了显式推理能力在解决视频任务中的必要性。</font>

<font style="color:rgb(25, 27, 31);">研究还发现，在强化学习阶段，即使只进行了1000步训练，Video-R1的性能也显著提升，特别是在推理密集型任务上。这清楚地表明了该强化学习框架的效力，并强调了强化学习在释放可泛化视频推理能力方面的重要性。</font>

<font style="color:rgb(25, 27, 31);">此外，当增加输入帧数从16到32时，模型在几乎所有基准测试上的性能都有所提高。这表明更长的上下文和更丰富的时序信息对模型的推理性能有积极贡献。</font>

:::color5
**<font style="color:#601BDE;">5.未来方向</font>**

:::

<font style="color:rgb(25, 27, 31);">尽管Video-R1取得了令人瞩目的成果，但研究团队也指出了几个限制和未来的研究方向：</font>

<font style="color:rgb(25, 27, 31);">（1）</font>**<font style="color:rgb(25, 27, 31);">增加帧数</font>**<font style="color:rgb(25, 27, 31);">：当前模型使用16个视频帧训练，这可能限制其处理长时序依赖的能力。未来可以开发更高效的训练和推理策略，以处理更长的视频。</font>

<font style="color:rgb(25, 27, 31);">（2）</font>**<font style="color:rgb(25, 27, 31);">更好的时序建模方法</font>**<font style="color:rgb(25, 27, 31);">：虽然T-GRPO引入了有效的时序感知推理，但它带来了额外的计算开销。未来可以通过探索更高效的时序建模机制来缓解这一问题。</font>

<font style="color:rgb(25, 27, 31);">（3）</font>**<font style="color:rgb(25, 27, 31);">动态响应长度控制</font>**<font style="color:rgb(25, 27, 31);">：当前的长度控制机制在预定义范围内应用固定奖励，而不考虑每个样本的复杂性。未来工作可以探索动态长度控制策略。</font>

<font style="color:rgb(25, 27, 31);">（4）</font>**<font style="color:rgb(25, 27, 31);">大规模强化学习</font>**<font style="color:rgb(25, 27, 31);">：受计算资源限制，当前的强化学习阶段仅训练了1000步。尽管结果很有希望，但增加强化学习训练规模可能会进一步提高模型性能。</font>

<font style="color:rgb(25, 27, 31);">（5）</font>**<font style="color:rgb(25, 27, 31);">改进图像到视频的知识迁移</font>**<font style="color:rgb(25, 27, 31);">：目前，研究团队以直接混合的方式将图像推理数据纳入训练集。未来研究可以设计更有原则的方法，更有效地将推理能力从图像迁移到视频。</font>





<font style="color:rgb(25, 27, 31);"></font>

## MM-RLHF<font style="color:#D22D8D;"></font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">尽管</font>[<font style="color:rgb(9, 64, 142);">多模态大语言模型</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（</font>[<font style="color:rgb(9, 64, 142);">MLLMs</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=MLLMs&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）取得了显著的进展，但现有的先进模型仍然缺乏与人类偏好的充分对齐。这一差距的存在主要是因为现有的对齐研究多集中于某些特定领域（例如减少幻觉问题），</font>**<font style="color:rgb(25, 27, 31);">是否与人类偏好对齐可以全面提升MLLM的各种能力</font>**<font style="color:rgb(25, 27, 31);">仍是一个未知数。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">快手，</font>[<font style="color:rgb(9, 64, 142);">中科院</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=%E4%B8%AD%E7%A7%91%E9%99%A2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，</font>[<font style="color:rgb(9, 64, 142);">南大</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=%E5%8D%97%E5%A4%A7&zhida_source=entity)<font style="color:rgb(25, 27, 31);">合作从三个层面入手推动MLLM alignment的发展，包括数据集，奖励模型以及训练算法，最终的alignment pipeline使得不同基础模型在</font>**<font style="color:rgb(25, 27, 31);">10</font>**<font style="color:rgb(25, 27, 31);">个评估维度，</font>**<font style="color:rgb(25, 27, 31);">27</font>**<font style="color:rgb(25, 27, 31);">个benchmark上都取得了一致的性能增益，比较突出的是，基于本文提出的数据集和对齐算法对LLaVA-ov-7B模型进行微调后， conversational 能力平均提升了 </font>**<font style="color:rgb(25, 27, 31);">19.5</font>**<font style="color:rgb(25, 27, 31);">%，安全性平均提升了 </font>**<font style="color:rgb(25, 27, 31);">60</font>**<font style="color:rgb(25, 27, 31);">%。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">[</font>[arXiv Paper](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2502.10391)<font style="color:rgb(25, 27, 31);">] [</font>[Training Code](https://link.zhihu.com/?target=https%3A//github.com/yfzhang114/MM-RLHF)<font style="color:rgb(25, 27, 31);">] [</font>[Homepage](https://link.zhihu.com/?target=https%3A//mm-rlhf.github.io/)<font style="color:rgb(25, 27, 31);">] [</font>[Reward Model](https://link.zhihu.com/?target=https%3A//huggingface.co/yifanzhang114/MM-RLHF-Reward-7B-llava-ov-qwen)<font style="color:rgb(25, 27, 31);">] [</font>[MM-RewardBench](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/yifanzhang114/MM-RLHF-RewardBench)<font style="color:rgb(25, 27, 31);">] [</font>[MM-SafetyBench](https://link.zhihu.com/?target=https%3A//github.com/yfzhang114/mmrlhf-eval)<font style="color:rgb(25, 27, 31);">] [</font>[Evaluation Suite](https://link.zhihu.com/?target=https%3A//github.com/yfzhang114/mmrlhf-eval)<font style="color:rgb(25, 27, 31);">]</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281079377-8d72cdcf-f88f-4e6d-9b17-918c2f58595a.png)

> MM-RLHF pipeline。（1）数据收集和清理：从1000万个指令样本开始，我们根据图像相似性对数据进行聚类，并在不同类别中统一采样。这导致了一个多样化的数据集，涵盖了基于图像的问答（例如，多项选择题、对话和安全相关问题）和视频问答格式。（2）响应生成：我们利用最先进的模型，包括GPT-4o和Qwen2-VL-72B，生成高质量的响应。（3）人工标注：我们对评分、排名和解释等九个类别进行人工标注，确保细粒度评估。
>

:::color5
**<font style="color:#601BDE;">1.主要贡献</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">新数据集</font>**<font style="color:rgb(25, 27, 31);">：本文引入了一个</font>**<font style="color:#74B602;">包含 120k 精细标注的偏好比较对的数据集</font>**<font style="color:rgb(25, 27, 31);">，包含三个维度的打分，排序，文本描述的具体原因以及平局等标注，</font>**<font style="color:rgb(25, 27, 31);">所有标注由人类专家完成</font>**<font style="color:rgb(25, 27, 31);">，一共</font>**<font style="color:rgb(25, 27, 31);">50</font>**<font style="color:rgb(25, 27, 31);">名标注人员，</font>**<font style="color:rgb(25, 27, 31);">8</font>**<font style="color:rgb(25, 27, 31);">名专家，耗时两个月。与现有资源相比，这一数据集在规模、样本多样性、标注粒度和质量等方面都有显著提升。</font>
2. **<font style="color:rgb(25, 27, 31);">创新的奖励模型</font>**<font style="color:rgb(25, 27, 31);">：提出了 </font>**<font style="color:rgb(25, 27, 31);">基于批评的奖励模型（</font>**[**<font style="color:rgb(9, 64, 142);">Critique-Based Reward Model</font>**](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=Critique-Based+Reward+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">，该模型</font>**<font style="color:#74B602;">首先对模型输出进行批评，然后再进行评分</font>**<font style="color:rgb(25, 27, 31);">。这一方法相比传统的标量奖励机制，提供了更好的可解释性和更有信息量的反馈，基于该方法的模型只需要7B size，在reward model benchmark就明显优于现有公开的72B-size的MLLM。</font>
3. **<font style="color:rgb(25, 27, 31);">动态奖励缩放</font>**<font style="color:rgb(25, 27, 31);">：提出了 </font>**<font style="color:rgb(25, 27, 31);">动态奖励缩放（Dynamic Reward Scaling）</font>**<font style="color:rgb(25, 27, 31);"> 方法，通过</font>**<font style="color:#74B602;">根据奖励信号调整每个样本的损失权重</font>**<font style="color:rgb(25, 27, 31);">，优化了高质量比较对的使用，进一步提高了数据的使用效率。</font>
4. **<font style="color:rgb(25, 27, 31);">全面评估</font>**<font style="color:rgb(25, 27, 31);">：本文在 </font>**<font style="color:rgb(25, 27, 31);">10</font>**<font style="color:rgb(25, 27, 31);"> 个维度和 </font>**<font style="color:rgb(25, 27, 31);">27</font>**<font style="color:rgb(25, 27, 31);"> 个基准上对提出的方案进行了严格评估，同时构</font>**<font style="color:rgb(25, 27, 31);">造了一个reward model的benchmark以及safety相关的benchmark</font>**<font style="color:rgb(25, 27, 31);">来弥补现有benchmark的不足，结果显示，在各个方面均取得了显著且一致的性能提升。</font>

:::color5
**<font style="color:#601BDE;">2.人类偏好数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281079377-8d72cdcf-f88f-4e6d-9b17-918c2f58595a.png)

1. **<font style="color:rgb(25, 27, 31);">数据来源</font>**<font style="color:rgb(25, 27, 31);">：图像数据来源包括 LLaVA-OV、VLfeedback、LLaVA-RLHF、lrv-instruction 和 Unimm-Chat 等，总共10M，视频数据来源主要是SharedGPT-4-video，安全性相关的数据来源主要包括 VLGuard 和自构造内容。</font>
2. **<font style="color:rgb(25, 27, 31);">数据过滤与模型响应生成</font>**<font style="color:rgb(25, 27, 31);">，通过预定义的多选题，长文本等类别均匀采样，确保少数类也有足够的样本。同时采用了knn聚类并采样的策略，保证数据的diversity。响应生成使用到了Qwen2-VL-72B、LLaVA-OV-72B、GPT-4o 和 Claude 3.5-sonnet等最先进的MLLM。</font>
3. **<font style="color:rgb(25, 27, 31);">数据标注</font>**<font style="color:rgb(25, 27, 31);">：主要包含三个维度，</font>**<font style="color:#74B602;">有用性，真实性，伦理性</font>**<font style="color:rgb(25, 27, 31);">，同时标注人员需要提供打分的依据，最终排名以及排名的依据，标注粒度细，通过专家定期进行质量检查和互动评审保证标注质量。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747280981149-2b807f48-430b-4f14-99e0-3e7db0184123.png)

> 重新采样聚类过程的结果。由于样本总数庞大，聚类和重复数据消除的结果包含丰富多样的类别。选定的样本包括数学、日常生活、自然场景、医学、电子技术和OCR场景等主题，展示了各种问题图像对。通过UMAP降维获得二维特征。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281040828-0b34cb89-d63a-4fef-99d3-8dd407096c67.png)

> 数据集组成统计
>

:::color5
**<font style="color:#601BDE;">3.MM-RLHF奖励模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281259360-ef3ea49f-af34-4f75-9719-3b2c340a9de5.png)

> 多任务奖励模型训练过程的说明。该过程从用户查询和相应的模型响应开始，由人类对其进行排名和注释。使用GPT-4o扩展人类注释，以提供增强的理由。奖励模型的训练有两个目标：（1）学习提供批评，模型学习为模型响应提供详细的批评和评估，以及（2）学习评分，模型学习根据模型响应和批评分配分数。这些任务的整合确保了改进模型输出的稳健评估框架。
>

<font style="color:rgb(25, 27, 31);">标准奖励模型通常通过预训练的LLM，</font>**<font style="color:#74B602;">并用线性奖励头替换原有头部，以输出一个标量奖励值</font>**<font style="color:rgb(25, 27, 31);">。然而，这些模型</font>**<font style="color:#117CEE;">难以充分利用人类注释中的丰富信息，也不具备足够的透明性</font>**<font style="color:rgb(25, 27, 31);">。  
</font><font style="color:rgb(25, 27, 31);">	为了解决标准奖励模型的局限性，本文提出了一种基于批评的训练框架。在这个框架中，</font>**<font style="color:#74B602;">模型首先生成批评（对响应的分析和评估），然后基于批评来打分</font>**<font style="color:rgb(25, 27, 31);">。批评生成部分与打分部分共同作用，确保了更细致的评价。</font>

**<font style="color:rgb(25, 27, 31);">增强注释以提高批评质量</font>**<font style="color:rgb(25, 27, 31);">：由于人工注释往往简洁且精炼，直接使用它们作为训练目标效果有限。因此，本文通过</font>**<font style="color:#74B602;">GPT-4o增强人工注释，使其更为详细和流畅</font>**<font style="color:rgb(25, 27, 31);">，从而提高批评的质量。</font>

<font style="color:rgb(25, 27, 31);">在训练过程中，批评的生成与奖励头的训练同时进行，在训练奖励头时采取了teacher-forcing的策略，即采用了ground truth的批评作为输入，默认损失权重都为1。</font>**<font style="color:#74B602;">测试阶段先生成批评，然后基于批评得出最终得分。</font>**

:::color5
**<font style="color:#601BDE;">4.性能评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281506594-b7fd651f-0251-4121-bfa1-cdf9af3ad3dc.png)

> MM RLHF RewardBench上指标和方法的性能比较。MM RLHF奖励（不包括任务1）表示训练LLaVA-OV-7B模型对成对样本进行评分，同时排除任务1。MM RLHF奖励（不含增强注释）涉及学习人类提供的注释，然后进行评分。MM RLHF奖赏（推理含GT注释）在推理过程中使用基本事实注释。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281512868-c874bb58-a23a-44b5-a717-8b8372490397.png)

> 我们的奖励模型（MM RLHF奖励）与现有的开源和私有多模式模型的性能比较。MM-RLHF-Reward-7B的性能优于现有的72B开源多模态模型和几个竞争激烈的闭源模型。
>

<font style="color:rgb(25, 27, 31);">该模型框架简单，且在多个基准测试中的表现与GPT-4o相媲美，甚至超越了许多开源模型，表现出色，尤其在自定义基准测试中，其表现远超GPT-4o，这验证了其作为训练算法奖励信号的有效性。</font>

<font style="color:rgb(25, 27, 31);">表4中也展示了，当奖励头直接使用偏好数据集进行训练时，模型的ACC+稳定在50%左右。然而，当引入人工注释作为学习目标时，ACC+稳定提升了5%。进一步通过GPT-4o扩展人工注释，生成更加详细和流畅的批评，最终提高了ACC+达17%。当评估时直接使用人工批评时，ACC和ACC+均接近90%，表明评估质量对奖励模型效果的至关重要性。</font>

:::color5
**<font style="color:#601BDE;">5.MM-DPO：有效利用高质量偏好数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747288984946-f690c128-154e-471f-88e6-71fa1572e3e2.png)

<font style="color:rgb(25, 27, 31);">要有效利用MM-RLHF中的高质量数据，我们有以下的实验发现和技巧</font>

1. **<font style="color:rgb(25, 27, 31);">MM-DPO不再仅仅关注“最难的比较对”（即排名差异最大的一对）</font>**<font style="color:rgb(25, 27, 31);">，而是将一个查询下所有可能的响应对都纳入训练。具体来说，对于一个查询</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">x</font><font style="color:rgb(25, 27, 31);">，如果有多个响应，每一对具有不同排名的响应都被视为一个有效的比较对。这种全面的处理方式可以捕捉更细粒度的排序信息，让模型从更广泛的偏好数据中学习。然</font>**<font style="color:rgb(25, 27, 31);">而，这种策略也带来了新的挑战</font>**<font style="color:rgb(25, 27, 31);">：当响应对的排名差异较小时（例如排名 3 和排名 4 的比较），其奖励差距（reward margin）往往较小，而排名差异较大的响应对（例如排名 1 和排名 4 的比较）包含的信息质量更高。如果对所有样本对一视同仁，会导致高置信度的信息被低效利用。  
</font>
2. <font style="color:rgb(25, 27, 31);">为了解决这个问题，MM-DPO 引入了动态奖励缩放（Dynamic Reward Scaling）机制，根据奖励差距动态调整更新强度，优先利用高置信度的样本对。具体而言，奖励模型可以自然地为样本对提供奖励差距（reward margin），这为动态控制样本的更新权重提供了一个直接的信号。</font>

<font style="color:rgb(25, 27, 31);">本文采用MM-RLHF-Reward-7B 模型来计算奖励差距</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">δ</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">w</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);">−</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">其中</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">w</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">分别是正样本和负样本的奖励分数。</font>

<font style="color:rgb(25, 27, 31);">DPO中，动态缩放因子</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">δ</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的计算公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747289224985-0d1f7e92-0259-45f2-821d-32247d66094f.png)

<font style="color:rgb(25, 27, 31);">其中：</font><font style="color:rgb(25, 27, 31);">βori</font><font style="color:rgb(25, 27, 31);"> 是初始默认缩放因子;</font><font style="color:rgb(25, 27, 31);">w</font><font style="color:rgb(25, 27, 31);"> 是一个参数，用于平衡动态部分的贡献；</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 是一个可调超参数，控制 </font><font style="color:rgb(25, 27, 31);">β(δ)</font><font style="color:rgb(25, 27, 31);">随着</font><font style="color:rgb(25, 27, 31);">δ</font><font style="color:rgb(25, 27, 31);">的变化速度。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747289030103-ba37aa55-f407-497e-920b-110b978feb63.png)

<font style="color:rgb(25, 27, 31);">接下来只需要将DPO算法中的</font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">部分替换为动态的</font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">即可。</font>

<font style="color:rgb(25, 27, 31);">MM-DPO在各类benchmark上都表现出了不错的性能增益，而且其对于超参数并不是非常敏感，大多数情况下都能使得高质量pair的利用效率得到明显提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747289269736-7dc58805-2244-4e0d-b626-4cc7f5c90955.png)

> 对我们的方法和数据集进行消融研究。（a）现实世界任务评估，其中“LLaVA-OV-7B”作为基线模型，“+MM-RLHF”表示我们的数据集与传统DPO算法的结合使用。“+隐性奖励”是指在LLM中使用动态贝塔策略[65]。（b）评估超参数k和w对MM-DPO模型的影响，证明这些变化对排行榜得分的影响。
>

:::color5
**<font style="color:#601BDE;">6.27个评估标准，10种评估维度的综合评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">主要领域包括图表与文档理解、OCR、幻觉检测、数学推理、通用知识、多模态对话、高分辨率与真实世界应用、视频理解、多图像处理以及多模态安全性。其中，多模态安全性基准 MM-RLHF-SafeBench 是自构建的，涵盖对抗攻击、越狱攻击、隐私保护和有害内容生成等场景，重点评估模型的安全性与鲁棒性。这些数据集为模型的多方面性能提供了详尽的测试环境。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747292757393-103cc9b4-b08a-48df-8af0-151373d40b11.png)

> 在8个不同的评估维度上对齐后的性能变化，比较我们对齐策略下的多个模型。所有模型在拟议的对齐下都显示出全面的性能改进，表明在各种任务中都取得了显著成果。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747292812501-defdd4cb-dbd9-4445-a691-5806ad2b96f1.png)

> MM RLHF SafeBench校准后的性能变化，比较我们的对齐策略下的多个模型。
>

<font style="color:rgb(25, 27, 31);">上面两图展示了使用我们的数据集和对齐算法，LLaVA-OV-7B、LLaVA-OV-0.5B和InternVL-1B在不同维度上的对齐表现，其中每个评估维度的得分在相应的基准上进行了平均。</font>

**<font style="color:rgb(25, 27, 31);">会话能力和安全性的显著提升</font>**<font style="color:rgb(25, 27, 31);">： 实验结果表明，通过对齐过程，这两个方面的表现得到了显著改进，无需调整超参数。在会话基准中，平均提高超过10%，而不安全行为减少了至少50%。此外，在</font>[<font style="color:rgb(9, 64, 142);">WildsVision</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=WildsVision&zhida_source=entity)<font style="color:rgb(25, 27, 31);">任务中，胜率至少提高了50%。</font>

**<font style="color:rgb(25, 27, 31);">在幻觉、数学推理、多图像和视频理解方面的广泛提升</font>**<font style="color:rgb(25, 27, 31);">： 对齐后的模型在这些领域表现出显著的提升。有趣的是，尽管我们的数据集中缺乏专门的多图像数据，模型在多图像任务中的表现依然显著提升。这表明我们数据集的多样性有助于模型在多个维度上进行更好的泛化。</font>

:::color5
**<font style="color:#601BDE;">7.未来方向</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在本研究中，我们提出了MM-RLHF，一个高质量、细粒度的数据集，专门用于推动多模态大语言模型（MLLMs）的对齐工作。与以往专注于特定任务的研究不同，我们的数据集和对齐方法旨在全面提升多个维度的性能。即使在奖励建模和优化算法方面仅进行了初步改进，我们在几乎所有评估基准上都观察到了显著且持续的提升，强调了综合性对齐策略的潜力。</font>

<font style="color:rgb(25, 27, 31);">展望未来，我们看到进一步挖掘我们数据集价值的巨大机会。数据集的丰富注释粒度，如每个维度的分数和排名理由，在当前的对齐算法中仍未得到充分利用。未来的工作将重点关注利用这些粒度信息与先进的优化技术，结合高分辨率数据来解决特定基准的局限性，并使用半自动化策略高效地扩展数据集。我们相信，这些努力不仅将推动MLLM对齐到新的高度，还将为更广泛、更具普适性的多模态学习框架奠定基础。</font>

