# PEFT 参数高效微调

<!-- source: yuque://zhongxian-iiot9/hlyypb/wzpze9d5k8lr493g -->

# 参数高效微调（PEFT, parameter-efficient fine-tuing）
:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

<font style="color:rgb(25, 27, 31);">当前使用广泛的通用领域数据集进行预训练的模型，基本上都表现出了很强的泛化能力，这也推动了自然语言处理 (NLP) 、多模态等任务应用的发展。 为了让模型适用于特定的下游任务，通常会采用完全微调（FT）方式重新训练所有模型参数。 然而，随着模型和数据集规模的扩大，微调整个模型需要的费用将变的非常昂贵。</font>

<font style="color:rgb(25, 27, 31);">为了解决这个问题，研究人员们开始引入参数高效微调（PEFT）方法，该方法旨在降低大型模型微调成本。它们通过仅训练相对于总参数数量的一小部分参数来适应下游任务，从而实现这一目标。现有的PEFT方法可以分为三类。</font>

1. <font style="color:rgb(25, 27, 31);">第一类是</font>[<font style="color:rgb(9, 64, 142);">适配器方法</font>](https://zhida.zhihu.com/search?content_id=239994801&content_type=Article&match_order=1&q=%E9%80%82%E9%85%8D%E5%99%A8%E6%96%B9%E6%B3%95&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（Adapter-based methods,），此类方法涉及将额外的可训练模块引入原始冻结的主干网络中；</font>
2. <font style="color:rgb(25, 27, 31);">第二类是</font>[<font style="color:rgb(9, 64, 142);">提示方法</font>](https://zhida.zhihu.com/search?content_id=239994801&content_type=Article&match_order=1&q=%E6%8F%90%E7%A4%BA%E6%96%B9%E6%B3%95&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（Prompt-based methods）。此类方法在初始输入中添加额外的soft tokens，并专注于微调这些可训练向量。</font>

**<font style="color:#ED740C;">这两类方法，无论是改变模型的输入还是架构，都会导致相对于基准模型的推理延迟增加。</font>**

3. <font style="color:rgb(25, 27, 31);">第三类是LoRA及其变体方法，特点是不增加额外推理负担。它们利用低秩矩阵来近似微调过程中的权重变化，并与预训练权重合并以进行推理。</font>

## <font style="color:rgb(53, 53, 53);">lora</font>
[https://www.yuque.com/zhongxian-iiot9/gi3w2u/cgil121ar06pez6m/edit?toc_node_uuid=pvuB9jZFFb92skHm](https://www.yuque.com/zhongxian-iiot9/gi3w2u/cgil121ar06pez6m/edit?toc_node_uuid=pvuB9jZFFb92skHm)

## Adapter-Tuning
[https://www.yuque.com/zhongxian-iiot9/gi3w2u/giih7snhrtf4itpb](https://www.yuque.com/zhongxian-iiot9/gi3w2u/giih7snhrtf4itpb)

**<font style="color:rgb(51, 51, 51);">背景</font>**

<font style="color:rgb(51, 51, 51);">Adapter-Tuning 是一种新的微调策略，用于减少大规模预训练模型在下游任务中所需的参数量。这个方法通过在预训练模型中插入小的适配器模块来进行任务特定的微调。</font>

**<font style="color:rgb(51, 51, 51);">适用场景</font>**

+ <font style="color:rgb(51, 51, 51);">适用于需要在特定任务上对预训练模型进行微调，但又希望保留预训练模型通用能力的场景。</font>
+ <font style="color:rgb(51, 51, 51);">当可用的计算资源有限时，Adapter-Tuning允许在不训练整个模型的情况下，针对特定任务进行适应。</font>

**<font style="color:rgb(51, 51, 51);">原理</font>**

+ **<font style="color:rgb(51, 51, 51);">适配器模块</font>**<font style="color:rgb(51, 51, 51);">：在 Transformer 模型的各层之间插入小的前馈网络（adapter），这些网络负责任务特定的调整。</font>
+ **<font style="color:rgb(51, 51, 51);">参数更新</font>**<font style="color:rgb(51, 51, 51);">：调整适配器的参数，而冻结大部分预训练网络的参数，较少更新的参数使得模型更轻量化。</font>

<font style="color:rgb(51, 51, 51);">适配器的工作可以表示为：  
</font><font style="color:rgb(51, 51, 51);">y</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">f</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">x</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">θ</font><font style="color:rgb(51, 51, 51);">b</font><font style="color:rgb(51, 51, 51);">a</font><font style="color:rgb(51, 51, 51);">s</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">+</font><font style="color:rgb(51, 51, 51);">g</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">h</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">x</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">θ</font><font style="color:rgb(51, 51, 51);">a</font><font style="color:rgb(51, 51, 51);">d</font><font style="color:rgb(51, 51, 51);">a</font><font style="color:rgb(51, 51, 51);">p</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">r</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">y</font>_<font style="color:rgb(51, 51, 51);">=</font>_<font style="color:rgb(51, 51, 51);">f</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">x</font>_<font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">θ</font>__<font style="color:rgb(51, 51, 51);">ba</font>__<font style="color:rgb(51, 51, 51);">se</font>_<font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">+</font>_<font style="color:rgb(51, 51, 51);">g</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">h</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">x</font>_<font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">θ</font>__<font style="color:rgb(51, 51, 51);">a</font>__<font style="color:rgb(51, 51, 51);">d</font>__<font style="color:rgb(51, 51, 51);">a</font>__<font style="color:rgb(51, 51, 51);">pt</font>__<font style="color:rgb(51, 51, 51);">er</font>_<font style="color:rgb(51, 51, 51);">))</font><font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 </font><font style="color:rgb(51, 51, 51);">f</font>_<font style="color:rgb(51, 51, 51);">f</font>_<font style="color:rgb(51, 51, 51);"> 是基础模型的功能，</font><font style="color:rgb(51, 51, 51);">g</font>_<font style="color:rgb(51, 51, 51);">g</font>_<font style="color:rgb(51, 51, 51);"> 是适配器功能，</font><font style="color:rgb(51, 51, 51);">h</font>_<font style="color:rgb(51, 51, 51);">h</font>_<font style="color:rgb(51, 51, 51);"> 是适配器的输入。</font>

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **优点**：
    - <font style="color:rgb(51, 51, 51);">适应性强，适合多任务学习。</font>
    - <font style="color:rgb(51, 51, 51);">训练时间短，节省计算资源。</font>
    - <font style="color:rgb(51, 51, 51);">属性更可控，因为参数较少。</font>
+ **缺点**：
    - <font style="color:rgb(51, 51, 51);">需要额外设计适配器的结构。</font>
    - <font style="color:rgb(51, 51, 51);">适配器的插入可能改变模型的原始表现。</font>

  


## Prefix-Tuning
**<font style="color:rgb(51, 51, 51);">背景</font>**

<font style="color:#1f2329;">Prefix-tuning是⼀种参数⾼效的微调⽅法，主要⽤于⾃然语⾔处理任务。它通过在预训练语 ⾔模型（如GPT-2、T5等）的</font><font style="color:#de7802;">输⼊序列前⾯添加⼀段可训练的前缀（prefix）</font><font style="color:#1f2329;">，实现对下游任务的适应，⽽⽆需更新原有的⼤量模型参数。</font>

<font style="color:#1f2329;">Prefix-tuning的概念出⾃2021年LiandLiang的论⽂《Prefix-Tuning: OptimizingContinuous  PromptsforGenerationTasks》[1]。这篇⽂章提出了在保持预训练语⾔模型的权重不变的前提下，通过</font><font style="color:#d83931;">学习⼀组连续的前缀向量来微调模型，以适应下游⽣成任务</font><font style="color:#1f2329;">。这种⽅法解决了全参数微调的计算和存储开销问题，同时提供了⼀种参数⾼效的模型调整⽅式。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737617376502-ad38487e-75f4-4e6a-8bb1-29d3ec841966.png)

**<font style="color:rgb(51, 51, 51);">适用场景</font>**

<font style="color:#1f2329;">Prefix-tuning主要⽤于⽂本⽣成任务（如机器翻译、⽂本摘要、对话⽣成等），也可以⽤于⼀些分类任务。在多任务和跨领域的应⽤场景中，prefix-tuning表现出⾊，因为它能将预训练模型的能⼒快速 转移到新任务上。</font>

<font style="color:#1f2329;"></font>

**<font style="color:rgb(51, 51, 51);">原理</font>**

1. <font style="color:#1f2329;">前缀构建：</font>
    1. <font style="color:#1f2329;">给定⼀个语⾔模型的层数为</font>_<font style="color:#1f2329;">L </font>_<font style="color:#1f2329;">，每⼀层都包含⼀个⾃注意⼒模块和⼀个前馈⽹络。</font>
    2. <font style="color:#6425d0;">Prefix-tuning在每⼀层的⾃注意⼒模块的输⼊前⾯增加⼀组可训练的前缀</font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">∈R</font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">×</font>_<font style="color:#1f2329;">d</font>_<font style="color:#1f2329;">，其中 </font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">是前缀⻓度，</font>_<font style="color:#1f2329;">d </font>_<font style="color:#1f2329;">是模型的隐藏维度。</font>
    3. <font style="color:#1f2329;">这些前缀向量会在整个训练过程中被优化。</font>
2. <font style="color:#1f2329;">注意力机制中的应用</font>
    1. <font style="color:#2ea121;">这些前缀向量被视为额外的“虚拟token”，与真实的输⼊token⼀起通过注意⼒计算。    </font>
    2. <font style="color:#1f2329;">在注意⼒得分计算中，前缀会影响后续token的注意⼒权重，从⽽对⽣成的输出产⽣影响。</font>

<font style="color:#1456f0;">  </font>3. 微调过程 

<font style="color:#d83931;">仅优化这些前缀向量的参数，⽽冻结原始模型的权重。</font><font style="color:#1f2329;">这样可以显著减少需要训练的参数量，尤其是在处理⼤模型时（如GPT-3、T5-11B等），这种⽅法表现出较⾼的参数效率。</font>

4. <font style="background-color:#f5f6f7;">任务适应</font> 

<font style="color:#1f2329;">在任务微调阶段，前缀向量被初始化为随机向量，然后随着训练迭代不断更新，使其能够适应特定任务的需求。</font><font style="color:#dc9b04;">最终，这些向量在模型⽣成任务中起到类似“指导”的作⽤。</font>

<font style="color:#dc9b04;"></font>

**<font style="color:#1f2329;">数学表述</font>**

<font style="color:#1f2329;">假设输⼊序列的表⽰为</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">∈R</font>_<font style="color:#1f2329;">n </font>_<font style="color:#1f2329;">×</font>_<font style="color:#1f2329;">d  </font>_<font style="color:#1f2329;">，其中</font>_<font style="color:#1f2329;">n </font>_<font style="color:#1f2329;">是输⼊序列⻓度，</font>_<font style="color:#1f2329;">d</font>_<font style="color:#1f2329;">是隐藏维度。Prefix-tuning的做法是将前缀 </font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">与</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">拼接起来，得到扩展后的输⼊：</font>

**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext </font><font style="color:#1f2329;">= [</font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">;</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">] ∈ R</font><font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">+</font>_<font style="color:#1f2329;">n</font>_<font style="color:#1f2329;">) ×</font>_<font style="color:#1f2329;">d    </font>_<font style="color:#1f2329;">此扩展后的输⼊ </font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext会被传递给Transformer的每⼀层进⾏处理。</font>

<font style="color:#1f2329;"></font>

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **优点**：
    - <font style="color:rgb(51, 51, 51);">参数效率高：</font><font style="color:#1f2329;">仅微调前缀部分的参数，⽽冻结预训练模型的所有参数。⼤⼤减少了微调参数量。例如，在GPT-2模型上，Prefix-tuning只需优化不到0.1%的参数。</font>
    - <font style="color:#1f2329;">训练效率高：由于前缀的参数量远⼩于整个模型的参数量，训练过程更快。</font>
    - <font style="color:#1f2329;">迁移性强：前缀可以被视为⼀种可迁移的提⽰，可应⽤于多种任务。</font>
+ **缺点**：
    - <font style="color:#245bdb;">对于某些任务，前缀⻓度的选择较为关键，过短可能不⾜以引导模型完成任务，⽽过⻓则会增加训练成本。</font>
    - <font style="color:#1456f0;"> </font><font style="color:#1f2329;">在⼀些特定任务上，Prefix-tuning的表现可能不如全参数微调，因为它只能影响输⼊特征，⽽⽆法修改模型的内部参数。</font>

## Prompt-Tuning
**<font style="color:rgb(51, 51, 51);">背景</font>**

<font style="color:#1f2329;">Prompt-tuning是⼀种专注于优化提⽰（prompt）来提升预训练语⾔模型在下游任务中性能的技术。它通过对提⽰部分进⾏训练，⽽不修改模型参数，从⽽实现对⼤规模语⾔模型的⾼效适应。Prompt-tuning能够以较少的参数调整，获得接近甚⾄超过传统微调⽅法的性能，尤其适⽤于⼤规模预训练模型（如GPT-3、T5等）。</font>

<font style="color:#1f2329;">Prompt-tuning的核⼼思想是在</font><font style="color:#DF2A3F;">输⼊序列前插⼊⼀个可训练的提⽰（prompt）</font><font style="color:#1f2329;">，这些提⽰不再是离散的⽂本，⽽是连续的嵌⼊向量。通过对提⽰向量进⾏训练，可以有效引导模型输出更符合任务⽬标的  结果。主要观点包括：</font>

**<font style="color:rgb(51, 51, 51);">适用场景</font>**

+ <font style="color:rgb(51, 51, 51);">适用于使用提示词（prompts）来引导模型响应特定任务的场景，尤其在获取标签数据较少的情况下。</font>
+ <font style="color:rgb(51, 51, 51);">用于探索如何通过不同的提示词组合来提高模型性能。</font>

**<font style="color:rgb(51, 51, 51);">原理</font>**

1. <font style="color:#245bdb;">连续提示的初始化：</font>
+ <font style="color:#1f2329;">在传统的Prompt⼯程中，提⽰通常是⼿⼯设计的⾃然语⾔⽂本。Prompt-tuning将这些提⽰替换为连续的可优化向量，即可训练的嵌⼊。</font>
+ <font style="color:#1f2329;">这些提⽰向量的⻓度$m$由⽤⼾指定，提⽰的维度$d$等于模型的嵌⼊层维度。</font><font style="color:#1456f0;">。</font><font style="color:#1f2329;">提⽰向量可以被随机初始化或者从现有的嵌⼊向量中初始化。</font>
2. <font style="color:#245bdb;">输入序列的构造：</font>

<font style="color:#1456f0;"></font><font style="color:#1f2329;">给定⼀个任务输⼊序列</font>**<font style="color:#1f2329;">X </font>**<font style="color:#1f2329;">= [</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">1 </font><font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">2 </font><font style="color:#1f2329;">, … , </font>_<font style="color:#1f2329;">x</font>__<font style="color:#1f2329;">n </font>_<font style="color:#1f2329;">] </font><font style="color:#1f2329;">，其中</font>_<font style="color:#1f2329;">x</font>__<font style="color:#1f2329;">i</font>_<font style="color:#1f2329;">表⽰第</font>_<font style="color:#1f2329;">i</font>_<font style="color:#1f2329;">个token的嵌⼊向量，Prompt-tuning在输⼊序列的前⾯添加提⽰向量</font>**<font style="color:#1f2329;">P </font>**<font style="color:#1f2329;">= [</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">1 </font><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">2 </font><font style="color:#1f2329;">, … ,</font>_<font style="color:#1f2329;">p</font>__<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">]</font><font style="color:#1f2329;">。</font>

<font style="color:#1f2329;">扩展后的输⼊序列表⽰为 </font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext </font><font style="color:#1f2329;">= [</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">1 </font><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">2 </font><font style="color:#1f2329;">, … ,</font>_<font style="color:#1f2329;">p</font>__<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">1 </font><font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">2 </font><font style="color:#1f2329;">, … , </font>_<font style="color:#1f2329;">x</font>__<font style="color:#1f2329;">n </font>_<font style="color:#1f2329;">]</font><font style="color:#1f2329;">。</font>

3. <font style="color:#245bdb;">冻结模型参数,  仅训练提示向量：</font>
+ <font style="color:#1f2329;">在Prompt-tuning的训练过程中，保持预训练模型的所有参数不变，只对提⽰向量的参数进⾏ 优化。</font>
+ <font style="color:#1f2329;">优化⽬标通常是任务相关的损失函数，如分类任务的交叉熵损失或⽣成任务的语⾔模型损失。</font>
4. <font style="color:#245bdb;">在生成任务中的应用：</font>
+ <font style="color:#1f2329;">Prompt-tuning不仅可以应⽤于分类任务，还适⽤于各种⽣成任务（如机器翻译、⽂本摘要）。</font>
+ <font style="color:#1f2329;">在这些任务中，提⽰向量能够引导⽣成模型朝着特定的⽅向进⾏输出，使得⽣成结果更符合任务需求。</font>

**数学表述**

<font style="color:#1f2329;">假设给定输⼊序列</font>**<font style="color:#1f2329;">X </font>**<font style="color:#1f2329;">，</font><font style="color:#1f2329;">Prompt</font><font style="color:#1f2329;">-</font><font style="color:#1f2329;">tuning</font><font style="color:#1f2329;">的输⼊扩展为</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext</font><font style="color:#1f2329;">=</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">[</font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">;</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">]</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，其中</font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">是⻓度为</font>_<font style="color:#1f2329;">m </font>_<font style="color:#1f2329;">的提⽰向</font><font style="color:#1f2329;">量。</font><font style="color:#1f2329;">Prompt</font><font style="color:#1f2329;">-</font><font style="color:#1f2329;">tuning</font><font style="color:#1f2329;">的⽬标是优化提⽰向量</font>**<font style="color:#1f2329;">P </font>**<font style="color:#1f2329;">的参数</font><font style="color:#1f2329;">，使得模</font><font style="color:#1f2329;">型的输出能够更好地完成任务。训练过</font><font style="color:#1f2329;">程中优化的⽬标可以表⽰为：</font>

<font style="color:#1f2329;">minL(</font>_<font style="color:#1f2329;">f</font>_<font style="color:#1f2329;">(</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext</font><font style="color:#1f2329;">;</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">),</font>_<font style="color:#1f2329;">y</font>_<font style="color:#1f2329;">)</font>

<font style="color:#1f2329;">其中</font><font style="color:#1f2329;">L</font><font style="color:#1f2329;">表⽰损失函数，</font>_<font style="color:#1f2329;">f </font>_<font style="color:#1f2329;">为语⾔模型，</font>_<font style="color:#1f2329;">θ </font>_<font style="color:#1f2329;">为冻结的预训练模型参数，</font>_<font style="color:#1f2329;">y </font>_<font style="color:#1f2329;">为任务标签。</font>

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **优点**：
    - <font style="color:#1f2329;">参数效率⾼：</font><font style="color:#1f2329;">仅需优化提⽰向量</font><font style="color:#1f2329;">，显著减少了</font><font style="color:#1f2329;">需要训练的参数量。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">迁移性强：可以快速适应不同任务，尤其是在⼤规模模型中效果更为明显。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">适⽤于⼤规模模型：Prompt-tuning在⼤规模模型中可以充分发挥其优势，因为⼤模型具有更强的泛化能⼒和知识表⽰能⼒。</font>
+ **缺点**：
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">依赖提⽰⻓度：提⽰向量的⻓度$m$需要调    优，不同任务可能对提⽰⻓度有不同的需求。</font>
    - <font style="color:#1f2329;">⼩模型效果有限：在⼩规模预训练模型上，   Prompt-tuning的效果可能不如全参数微调。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">对复杂任务的适应性：Prompt-tuning对于⼀些复杂的任务可能需要进⼀步的改进，如结合其他参数⾼效的微调⽅法。</font>

## P-Tuning<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">P-tuning的概念源⾃2021年论⽂《GPTUnderstands, Too》。该论⽂提出通过在输⼊⽂本的前⾯插⼊⼀段可训练的提⽰向量，使得⼤规模预训练语⾔模型（如GPT）在特定任务（如分   类或⽂本⽣成）中更好地表现。P-tuning是⼀种泛化的“提⽰（prompt）”⽅法，相较于⼿⼯设计的提⽰词，它可以更灵活地适应任务需求，并且能够显著提升模型的性能。</font>

:::

<font style="color:#1f2329;">P-tuning的概念源⾃2021年论⽂《GPTUnderstands, Too》。该论⽂提出通过在输⼊⽂本的前⾯插⼊⼀段可训练的提⽰向量，使得⼤规模预训练语⾔模型（如GPT）在特定任务（如分   类或⽂本⽣成）中更好地表现。P-tuning是⼀种泛化的“提⽰（prompt）”⽅法，相较于⼿⼯设计的提⽰词，它可以更灵活地适应任务需求，并且能够显著提升模型的性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737617975940-912e0292-b2cf-4c14-96a4-3d37eb3a5794.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:#245bdb;">连续提示的构建：</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">给定⼀个预训练语⾔模型（如GPT、BERT等），P-tuning会在输⼊序列的前⾯插⼊⼀段可训练的提⽰向量 </font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">∈R</font>_<font style="color:#1f2329;">m </font>_<font style="color:#1f2329;">×</font>_<font style="color:#1f2329;">d  </font>_<font style="color:#1f2329;">，其中</font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">是提⽰向量的⻓度，</font>_<font style="color:#1f2329;">d</font>_<font style="color:#1f2329;">是嵌⼊层的维度。</font>
+ <font style="color:#1f2329;">这些提⽰向量被初始化为随机或特定的初值，并在训练过程中不断优化。</font>
2. <font style="color:#245bdb;">输入序列扩展：</font>
+ <font style="color:#1f2329;">将提⽰向量 </font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">与原始任务输⼊ </font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">∈ R</font>_<font style="color:#1f2329;">n </font>_<font style="color:#1f2329;">×</font>_<font style="color:#1f2329;">d </font>_<font style="color:#1f2329;">拼接起来 ，得到扩展的输⼊序列</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext </font><font style="color:#1f2329;">= [</font>**<font style="color:#1f2329;">P</font>**<font style="color:#1f2329;">;</font>**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">] ∈ R</font><font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">+</font>_<font style="color:#1f2329;">n</font>_<font style="color:#1f2329;">) ×</font>_<font style="color:#1f2329;">d  </font>_<font style="color:#1f2329;">，其中 </font>_<font style="color:#1f2329;">n </font>_<font style="color:#1f2329;">是原始输⼊序列的⻓度。</font>
+ <font style="color:#1f2329;">扩展后的输⼊序列被传递给语⾔模型的嵌⼊层，并继续通过模型的所有层进⾏处理。</font>
3. <font style="color:#245bdb;">参数更新</font>
+ <font style="color:#1f2329;">在训练过程中，只有提⽰向量</font>**<font style="color:#1f2329;">P </font>**<font style="color:#1f2329;">的参数会被优化，⽽预训练模型的参数保持冻结。这种⽅法显著减少了训练时需要优化的参数量。</font>
4. <font style="color:#245bdb;">多层提示设计  (p-tuning  v2)  ：</font>
+ <font style="color:#1f2329;">P-tuningv2进⼀步扩展了P-tuning的思想，通过在Transformer模型的不同层插⼊提⽰向量。   具体来说，在多层Transformer中，每⼀层都可以插⼊可训练的提⽰，以更细粒度地影响不同层的特征表⽰。</font>

**数学表述**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:#1f2329;">假设原始输⼊为</font>**<font style="color:#1f2329;">X</font>****<font style="color:#1f2329;"> </font>**<font style="color:#1f2329;">=</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">[</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">1</font><font style="color:#1f2329;">,</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">2</font><font style="color:#1f2329;">,</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">…</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">,</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">x</font>__<font style="color:#1f2329;">n</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">]</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，其中</font>_<font style="color:#1f2329;">x</font>__<font style="color:#1f2329;">i</font>_<font style="color:#1f2329;">表⽰第</font>_<font style="color:#1f2329;">i</font>_<font style="color:#1f2329;">个输⼊</font><font style="color:#1f2329;">token</font><font style="color:#1f2329;">的嵌⼊向量。</font><font style="color:#1f2329;">P-tuning</font><font style="color:#1f2329;">在模型</font><font style="color:#1f2329;">输⼊前插⼊提⽰向量 </font>**<font style="color:#1f2329;">P </font>**<font style="color:#1f2329;">=</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">[</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">1</font><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">2</font><font style="color:#1f2329;">,</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">…</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">p</font>__<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">]</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，形成扩展后的输⼊：</font>

**<font style="color:#1f2329;">X</font>**<font style="color:#1f2329;">ext </font><font style="color:#1f2329;">= [</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">1</font><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">p</font>_<font style="color:#1f2329;">2</font><font style="color:#1f2329;">, … ,</font>_<font style="color:#1f2329;">p</font>__<font style="color:#1f2329;">m</font>_<font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">1</font><font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">2</font><font style="color:#1f2329;">, … , </font>_<font style="color:#1f2329;">x</font>__<font style="color:#1f2329;">n</font>_<font style="color:#1f2329;">]</font>

<font style="color:#1f2329;">其	中，提⽰向量</font>**<font style="color:#1f2329;">P </font>**<font style="color:#1f2329;">的维度与嵌⼊层的维度相同。通过训练过程不断优化这些提⽰向量，使其能够有效地引导模型进⾏特定任务。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **优点**：
    - <font style="color:#1456f0;"> </font><font style="color:#1f2329;">参数效率⾼：只需训练少量提⽰向量的参数，可以显著减少微调的计算开销。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">更好的任务适应性：连续提⽰向量的表⽰能⼒强于⼿⼯设计的离散提⽰词，能够更灵活地适应不同任务。</font>
    - <font style="color:#1456f0;"></font><font style="color:#1f2329;">应⽤⼴泛：可⽤于分类、序列标注、⽣成等多种⾃然语⾔处理任务。</font>
+ **缺点**：
    - <font style="color:#1f2329;">提⽰⻓度的选择较为关键：提⽰向量的⻓度需要进⾏调优，不同任务可能需要不同的提⽰⻓度。</font>
    - <font style="color:#1f2329;">与任务数据的依赖较⼤：在⼀些特定的任务上，P-tuning可能不如全参数微调的效果。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">适用于少量标注数据的任务，特别是在需要生成适合模型输入的提示词的情况下。</font>
+ <font style="color:rgb(51, 51, 51);">当需要快速适应新任务而不依赖大规模标注数据时。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

**<font style="color:rgb(64, 64, 64);">P-Tuning v2</font>**<font style="color:rgb(64, 64, 64);">： 这是最主要的改进。v2不再像v1那样只在输入层加入提示，而是在</font>**<font style="color:rgb(64, 64, 64);">模型的每一层（Every Layer）</font>**<font style="color:rgb(64, 64, 64);"> 都加入可学习的提示 token。这种“深度提示”设计极大地提升了效果，尤其是在小模型上，使得P-Tuning在各类模型规模上都能达到接近全参数微调的性能。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

环境准备

```python
pip install transformers datasets peft accelerate
```

代码示例

```python
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from peft import (
    get_peft_config,
    get_peft_model,
    PromptTuningInit,
    PromptTuningConfig,
    TaskType,
    PeftType
)
from datasets import load_dataset

# 1. 加载模型和分词器
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token # 设置pad token

# 2. 加载数据集（以GLUE的MRPC任务为例）
dataset = load_dataset("glue", "mrpc")

# 3. 定义数据处理函数
def tokenize_function(examples):
    # 对文本进行编码
    outputs = tokenizer(
        examples["sentence1"],
        examples["sentence2"],
        truncation=True,
        max_length=128,
    )
    return outputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 4. 定义P-Tuning v2的配置
peft_config = PromptTuningConfig(
    task_type=TaskType.SEQ_CLS,      # 任务类型：序列分类
    prompt_tuning_init=PromptTuningInit.TEXT, # 初始化方式：文本
    num_virtual_tokens=20,           # 提示token的数量（超参数）
    prompt_tuning_init_text="Please classify the following sentence pair:", # 初始化文本
    tokenizer_name=model_name,
)

# 5. 创建基础模型
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2, # MRPC任务是二分类
    return_dict=True
)

# 6. 使用peft包装模型，将其转换为P-Tuning v2模型
model = get_peft_model(model, peft_config)
model.print_trainable_parameters() # 打印可训练参数数量，会发现它非常少！

# 7. 定义训练参数
training_args = TrainingArguments(
    output_dir="./ptv2-mrpc-output",
    learning_rate=3e-2,           # P-Tuning通常使用更大的学习率
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=20,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# 8. 创建Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
)

# 9. 开始训练！
trainer.train()

# 10. 评估模型
results = trainer.evaluate()
print(f"Evaluation results: {results}")

# 11. 保存和加载提示
model.save_pretrained("./my_ptv2_prompts")
# 加载时：
# from peft import PeftModel
# loaded_model = PeftModel.from_pretrained(base_model, "./my_ptv2_prompts")
```

+ `**<font style="color:rgb(64, 64, 64);background-color:rgb(236, 236, 236);">PromptTuningConfig</font>**`<font style="color:rgb(64, 64, 64);">： 这是配置P-Tuning的核心。我们指定了提示长度为20，并用一段自然语言文本进行初始化。</font>
+ `**<font style="color:rgb(64, 64, 64);background-color:rgb(236, 236, 236);">get_peft_model</font>**`<font style="color:rgb(64, 64, 64);">： 这个函数接收原始模型和配置，返回一个被包装后的P-Tuning模型，其中只有提示参数是可训练的。</font>
+ **<font style="color:rgb(64, 64, 64);">学习率</font>**<font style="color:rgb(64, 64, 64);">： P-Tuning通常使用比全参数微调（如5e-5）更大的学习率（如3e-2, 1e-2），因为它只优化一小部分参数。</font>
+ **<font style="color:rgb(64, 64, 64);">保存</font>**<font style="color:rgb(64, 64, 64);">： 最终只保存体积很小的提示参数（</font>`**<font style="color:rgb(64, 64, 64);background-color:rgb(236, 236, 236);">adapter_model.bin</font>**`<font style="color:rgb(64, 64, 64);"> 文件可能只有几十KB），而不是整个模型。</font>









## P-Tuning V2
**<font style="color:rgb(51, 51, 51);">背景</font>**

<font style="color:rgb(51, 51, 51);">P-Tuning V2 是对 P-Tuning 的进一步优化，针对复杂的文本处理任务，引入了更为灵活和有效的结构来增强性能。</font>

**<font style="color:rgb(51, 51, 51);">适用场景</font>**

+ <font style="color:rgb(51, 51, 51);">进一步增强P-Tuning的灵活性和表现，适用于更复杂和多样化的任务需求。</font>
+ <font style="color:rgb(51, 51, 51);">在大规模模型上实现更高效的训练和适应。</font>

**<font style="color:rgb(51, 51, 51);">原理</font>**

+ **<font style="color:rgb(51, 51, 51);">多层提示优化</font>**<font style="color:rgb(51, 51, 51);">：通过多层级的提示结构来捕获更丰富的信息，并允许模型上下文信息更深层次的交互。</font>
+ **<font style="color:rgb(51, 51, 51);">适应性强</font>**<font style="color:rgb(51, 51, 51);">：可以针对多种任务自动调整提示结构。</font>

<font style="color:rgb(51, 51, 51);">相关公式</font>

<font style="color:rgb(51, 51, 51);">输出可以表达为：  
</font><font style="color:rgb(51, 51, 51);">y=f(p1,p2,…,pn,x,θ)</font>_<font style="color:rgb(51, 51, 51);">y</font>_<font style="color:rgb(51, 51, 51);">=</font>_<font style="color:rgb(51, 51, 51);">f</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">p</font>_<font style="color:rgb(51, 51, 51);">1,</font>_<font style="color:rgb(51, 51, 51);">p</font>_<font style="color:rgb(51, 51, 51);">2,…,</font>_<font style="color:rgb(51, 51, 51);">pn</font>_<font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">x</font>_<font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">θ</font>_<font style="color:rgb(51, 51, 51);">)  
</font><font style="color:rgb(51, 51, 51);">这里多层提示 pi</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">提供了更多上下文信息。</font>

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **优点**：
    - <font style="color:rgb(51, 51, 51);">显著提升了复杂任务的性能。</font>
    - <font style="color:rgb(51, 51, 51);">更好的迁移学习效果，适用于更广泛的任务。</font>
+ **缺点**：
    - <font style="color:rgb(51, 51, 51);">需对多层结构的设计进行仔细规划。</font>
    - <font style="color:rgb(51, 51, 51);">相较于基础版本，计算需求可能更高。</font>

  


