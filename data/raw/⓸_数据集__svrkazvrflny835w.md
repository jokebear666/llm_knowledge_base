# ⓸ 数据集

<!-- source: yuque://zhongxian-iiot9/hlyypb/svrkazvrflny835w -->

# LLM数据合成
## <font style="color:rgb(0, 0, 0);">合成数据强化学习</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">尽管如GPT-4和Gemini等基础模型已在通用语言理解方面设立了新的行业标杆 ，</font>**<font style="color:#117CEE;">但它们在需要深度领域知识的专业领域中，其表现常常不尽如人意。当面临数学、医学、法律及金融等专门任务时，这些模型时常表现不佳</font>**<font style="color:rgba(0, 0, 0, 0.9);">，因为这些领域高度依赖特定的专业知识。为了解决上述挑战，北京大学、MIT等机构的研究人员提出了</font>**<font style="color:#74B602;">「合成数据强化学习」（Synthetic Data RL）框架。这是一个简单而通用的框架，仅从一个任务定义出发，合成大量多样的领域特定样本</font>**<font style="color:rgba(0, 0, 0, 0.9);">，然后利用强化学习（RL）对模型进行微调。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

:::color3
**简介：《Synthetic Data RL: Task Definition Is All You Need》**<font style="color:rgb(0, 0, 0);">基础模型严重依赖大规模、高质量人工标注数据来学习适应新任务、领域。为解决这一难题，来自北京大学、MIT等机构的研究者们提出了一种名为</font>**<font style="color:#ED740C;">「合成数据强化学习」（Synthetic Data RL）的通用框架。该框架仅需用户提供一个简单的任务定义，即可全自动地生成高质量合成数据。</font>**<font style="color:rgb(0, 0, 0);">结合自动强化学习（RL）微调的结果显示，该方法在数学、医疗，科学，金融等多个基准上取得十几个点的绝对性能提升。在同等数据数量条件下，其效果不仅显著优于人工数据下的监督微调方法，更媲美甚至超越了人工数据下的RL方法。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>**

**<font style="color:rgb(25, 27, 31);">项目地址：</font>**[**https://github.com/gydpku/Data_Synthesis_RL**](https://github.com/gydpku/Data_Synthesis_RL)

**paper：**[**https://arxiv.org/pdf/2505.17063**](https://arxiv.org/pdf/2505.17063)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1752746057446-59e8e801-225f-49b2-8c29-db053e952345.png)

> **「合成数据强化学习」（Synthetic Data RL）框架**
>

:::color5
**<font style="color:#601BDE;">1.三步走实现高效自适应学习</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">如图1所示：</font>

1. <font style="color:rgba(0, 0, 0, 0.9);">首先，系统通过知识引导的合成环节结合检索到的外部知识和任务特定模式，生成既有事实依据又与目标任务对齐的合成数据。</font>
2. <font style="color:rgba(0, 0, 0, 0.9);">随后，在难度自适应环节，系统</font>**<font style="color:#74B602;">会根据模型的反馈来调整这些生成样本的复杂度</font>**<font style="color:rgba(0, 0, 0, 0.9);">，目的是创建一个难度均衡、避免过于简单或困难的数据集。</font>
3. <font style="color:rgba(0, 0, 0, 0.9);">最后，在高潜力样本选择与强化学习环节，框架会精心挑选出高学习潜力的样本，</font>**<font style="color:#74B602;">并利用强化学习在这些样本上进行微调</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

:::color5
**<font style="color:#601BDE;">2.知识引导的数据合成</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">该环节的目标是生成</font>**<font style="color:#74B602;">高质量、多样化，并与任务高度相关</font>**<font style="color:rgba(0, 0, 0, 0.9);">的任务数据。该过程主要分为两个核心步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">关键词提取与相关段落检索</font>**

1. **<font style="color:rgba(0, 0, 0, 0.9);">关键词提取</font>**

<font style="color:rgba(0, 0, 0, 0.9);">为了让生成的内容能紧密围绕相关领域的知识，该环节首先会使用大模型从任务描述中提取一组</font>**<font style="color:#74B602;">领域特定的关键词</font>**<font style="color:rgba(0, 0, 0, 0.9);">。这些关键词可以看作是一种中间摘要，精确地概括了任务的核心领域与要求。</font>

2. **<font style="color:rgba(0, 0, 0, 0.9);">相关段落检索</font>**

<font style="color:rgba(0, 0, 0, 0.9);">接下来，一个「段落检索器」会使用这些关键词，在一个大型的高质量文本库（例如维基百科）中进行搜索，从而找到一系列与</font>**<font style="color:#74B602;">任务高度相关的知识段落</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1752751891098-ce1a8fe1-5533-4d29-bf44-ddd16f689406.png)

<font style="color:rgb(136, 136, 136);">图2：GPQA的任务定义，包括任务描述，输入和输出的形式。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在获取了相关的知识段落后，LLM生成器便开始合成初始的任务样本集。LLM生成器会综合利用所有信息，包括之前检索到的</font>**<font style="color:#74B602;">相关段落</font>**<font style="color:#74B602;">、</font>**<font style="color:#74B602;">抽象模式与具体示例的组合（可不提供）</font>**<font style="color:#74B602;">，以及</font>**<font style="color:#74B602;">原始的任务指令（如图所示）</font>**<font style="color:rgba(0, 0, 0, 0.9);">，来生成初始合成数据集。并通过大多数投票方法确保任务输出的正确性。</font>

<font style="color:rgba(0, 0, 0, 0.9);">通过这种方式，系统确保了合成出来的数据不仅在事实上有所依据，而且在形式和内容上也更加丰富多样。</font>

:::color5
**<font style="color:#601BDE;">3.难度自适应过程</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">本环节旨在解决训练样本难度不均衡的问题。核心思想是，通过自动评估和改写样本，生成一个难度分布更合理的数据集，从而提升模型的学习效率和最终效果。</font>

<font style="color:rgba(0, 0, 0, 0.9);">整个过程可以分为三个主要步骤：</font>

1. <font style="color:rgba(0, 0, 0, 0.9);">首先，使用一个</font>**<font style="color:#74B602;">基础模型对初始数据集进行全面评估</font>**<font style="color:rgba(0, 0, 0, 0.9);">。根据模型能否正确解答，样本被分为两类：</font>
    1. **<font style="color:rgba(0, 0, 0, 0.9);">已解决样本集</font>**<font style="color:rgba(0, 0, 0, 0.9);">：这个集合包含了所有基础模型能够正确解答的样本。</font>
    2. **<font style="color:rgba(0, 0, 0, 0.9);">未解决样本集</font>**<font style="color:rgba(0, 0, 0, 0.9);">：这个集合包含了所有基础模型未能正确解答的样本。</font>
2. <font style="color:rgba(0, 0, 0, 0.9);">接下来，利用一个</font>**<font style="color:#74B602;">大语言模型改写器</font>**<font style="color:rgba(0, 0, 0, 0.9);">对已分类的样本进行难度调整，以扩充数据集。改写器会分析已解决样本集中的内容，并在此基础上创造出更具挑战性的新样本，形成一个更难的样本集。同样地，改写器会分析未解决样本集的内容，并创造出难度更低的新样本，形成一个「更容易的样本集」。</font>
3. <font style="color:rgba(0, 0, 0, 0.9);">最后，将三个部分的数据合并在一起，包括</font>**<font style="color:#74B602;">原始的初始样本集、新生成的更难样本集、新生成的更容易样本集。</font>**

<font style="color:rgba(0, 0, 0, 0.9);">通过这个动态调整过程，如下图所示，最终的数据集在难度上更加多样和均衡，更贴合人类真实数据的分布特征，能够为模型提供一个平滑的学习曲线，从而实现更优的训练效果。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1752752104579-521bddea-70c6-4a24-a380-26536ec8d79e.png)

<font style="color:rgb(136, 136, 136);">图3：合成与人工数据难度分布，合成数据调整后更贴合人工数据。</font>

:::color5
**<font style="color:#601BDE;">4.筛选高潜力样本并强化微调</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在通过难度自适应策略生成了包含多样化难度的大规模合成数据集后，研究人员并不会直接将所有数据用于训练，因为许多合成样本可能对模型来说过于简单或过于困难，无法提供有效的学习信号。为了最大化训练效率和效果，</font>**<font style="color:#74B602;">研究人员设计了第三个环节，旨在识别并利用那些最具学习价值的「高潜力」样本。</font>**

1. **<font style="color:rgba(0, 0, 0, 0.9);">评分系统：</font>**<font style="color:rgba(0, 0, 0, 0.9);">为了精准地识别出这些高潜力样本，框架设计了一套基于模型实际表现的评分系统。具体来说，它会利用基础模型，对每个样本进行多次解答尝试。</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">筛选样本：</font>**<font style="color:rgba(0, 0, 0, 0.9);">接着，系统会计算模型在多次尝试中成功解答的次数比例。这个评分系统有一个巧妙的设计：对于那些模型在所有尝试中都失败的「极难」样本（即通过率为0），系统会故意给它们一个最高分（比如1）。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">这样做的目的是为了在后续排序时，能够轻易地将这些过于困难/存在合成错误的样本沉底。评分完成后，所有样本会按照它们的「通过率得分」从低到高进行排序。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">根据这个排序结果，得分最低（但大于0）的样本，正是我们寻找的「高潜力」目标—模型偶尔能答对，但磕磕绊绊，充满了不确定性。框架会从排序列表的顶端选取一定数量的样本，构成训练集。</font>
3. **<font style="color:rgba(0, 0, 0, 0.9);">强化学习：</font>**<font style="color:rgba(0, 0, 0, 0.9);">最后，这个精挑细选出的高潜力训练集将被用于对基础模型进行一轮的强化学习训练。</font>

<font style="color:rgba(0, 0, 0, 0.9);">最终步骤旨在将模型在这些「临界区」样本上的不确定性转化为稳定的正确解答能力，从而产出一个性能得到显著提升的最终模型。</font>

> <font style="color:rgba(0, 0, 0, 0.9);">表1：示例间的多样性比较。人工创建的示例是从MATH数据集中的代数任务训练数据中抽取的。我们从该数据集中选择了一个演示示例来指导生成。一种方法（称为“直接生成的示例”）仅使用该演示示例作为指导。而我们提出的方法（称为“使用我们方法的示例”）则首先归纳出一个模式，然后同时使用该模式和演示示例进行数据生成。</font>
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1752752892861-9dd1f8a0-dafa-4665-af47-980711c26bfc.png)

:::color5
**<font style="color:#601BDE;">5.全面超越SFT，媲美人工数据RL</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

**<font style="color:rgba(0, 0, 0, 0.9);">实验设定：</font>**<font style="color:rgba(0, 0, 0, 0.9);">在数据合成过程中，GPT-4o被用作指导者模型，而Qwen2.5-7B-base则作为基础模型，整个流程的训练集大小也维持在500个数据，RL训练采用了GRPO算法 。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究人员在数学、科学、医学、法律和金融等多个领域的8个公开基准数据集上，对提出方法进行了全面评估，并该方法与多个基线进行了比较，包括像Qwen-2.5-7B和GPT-4o这样的预训练和指令调优模型，</font>**<font style="color:#74B602;">像Self-Instruct和SynthLLM这样的其他合成数据生成方法</font>**<font style="color:rgba(0, 0, 0, 0.9);">，以及像使用人类标注数据进行监督式微调（SFT）和强化学习（RL）这样的标准训练策略。实验结果如表1所示。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1752753020470-92e93905-0808-4d6f-aba3-25bdd549bb42.png)

<font style="color:rgb(136, 136, 136);">表1：该方法和基线在8个任务上的的表现。</font>

<font style="color:rgba(0, 0, 0, 0.9);">具体来看，该框架带来全方位的性能提升，不仅显著超越了模型自身的基础版本，也优于官方的指令微调模型和其他主流的合成数据方法：</font>

+ **<font style="color:rgba(0, 0, 0, 0.9);">在数学推理领域</font>**<font style="color:rgba(0, 0, 0, 0.9);">：在广泛关注的 GSM8K基准测试上，该方法取得了91.7%的准确率，相较于Qwen-2.5-7B基础模型的62.5%，实现了29.2%的绝对性能提升。</font>

> <font style="color:rgba(0, 0, 0, 0.9);">这一成绩不仅显著优于官方指令微调模型Qwen-2.5-7B-Instruct的88.8%，也超越了包括Self-Instruct (85.1%) 和SynthLLM (90.1%) 在内的其他合成数据生成方法，在更具挑战性的MATH数据集上，也获得了8.7%的绝对提升。</font>
>

+ **<font style="color:rgba(0, 0, 0, 0.9);">在专业知识领域</font>**<font style="color:rgba(0, 0, 0, 0.9);">：该方法的优势同样延伸到了需要高度专业知识的领域。在MedQA（医学）、CQA（法律）和 CFA（金融）等基准测试中，分别取得了8.9%、17.7%和13.7%的绝对性能提升。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">在科学领域</font>**<font style="color:rgba(0, 0, 0, 0.9);">：在GPQA（研究生水平科学问答）这一高难度任务上，其性能提升同样显著，达到了13.1%</font>

:::color5
**<font style="color:#601BDE;">6.结论</font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">Synthetic Data RL框架的提出，为大模型在专业领域的低成本、高效率适配提供了全新的解决方案。它通过将自动化数据合成与强化学习相结合，将模型微调的门槛从昂贵的人工数据标注，降低到了一个简单的任务描述，无需任何后续的人工标注或反馈。</font>

1. **<font style="color:rgba(0, 0, 0, 0.9);">同等数据预算下的效率优势</font>**

<font style="color:rgba(0, 0, 0, 0.9);">该框架最引人注目的优势之一在于其极高的数据效率。在与使用「真实」人工标注数据进行训练的方法进行同等数据预算的公平比较时，Synthetic Data RL表现出了显著的优势。</font>

+ **<font style="color:rgba(0, 0, 0, 0.9);">完胜监督微调（SFT）</font>**<font style="color:rgba(0, 0, 0, 0.9);">：当训练预算被限制在相同数量（例如500个样本）时，「合成数据强化学习」方法的效果远超传统的监督微调（SFT）方法 。例如，在GSM8K任务上，SFT使用500个人类样本仅能达到74.5%的准确率，而该框架则达到了91.7%。</font>**<font style="color:#74B602;">这突显了在数据稀缺的情况下，RL相较于SFT的普遍优越性。</font>**
+ **<font style="color:rgba(0, 0, 0, 0.9);">媲美甚至超越人类数据RL</font>**<font style="color:rgba(0, 0, 0, 0.9);">：更令人印象深刻的是，该方法不仅效果好，而且效率极高。在使用同等数量（500个样本）的训练数据时，它的表现能够持平甚至略微超过使用「真实」人类标注数据进行训练的强化学习（RL）方法。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在GSM8K任务上，使用500个合成样本的准确率（91.7%）甚至略高于使用500个人类样本的RL（91.2%）。这一趋势在不同数据预算（100、300、1000个样本）的消融研究中也得到了证实（详情见原文），表明该方法始终能与使用人类数据的RL基线相媲美或更优。</font>

2. **<font style="color:rgba(0, 0, 0, 0.9);">人工数据指导的边际效益递减</font>**

<font style="color:rgba(0, 0, 0, 0.9);">表1的研究结果进一步揭示了一个重要现象：对模型合成数据而言，</font>**<font style="color:#74B602;">掌握任务的正确「形式」比学习大量具体「实例」更为关键</font>**<font style="color:rgba(0, 0, 0, 0.9);">，这一点体现在人类标注数据呈现出的边际效益递减上：</font>

<font style="color:rgba(0, 0, 0, 0.9);">当模型通过「合成数据强化学习」框架，仅从任务定义中学习并掌握了任务的底层结构后，其性能已经达到了一个非常高的水平。</font>

<font style="color:rgba(0, 0, 0, 0.9);">此时，额外增加由人类标注的演示示例，所带来的性能提升变得非常有限。例如，在GSM8K基准测试上的表现：</font>

<font style="color:rgba(0, 0, 0, 0.9);">仅使用任务定义进行训练的模型，其准确率已经可以达到91.7%；在此基础上，即便再增加100个高质量的人类演示样本来指导合成数据，最终的准确率也仅仅微升至92.1%</font>

<font style="color:rgba(0, 0, 0, 0.9);">这种微小的、渐进式的改进并非孤例，在其他多个数据集上也观察到了相似的趋势，例如在MATH、LogiQA、MedQA和MedNLI等任务上，随着人类演示样本的增加，性能也只是略有提高 。</font>

## MM-EVOL <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>[<font style="color:rgb(9, 64, 142);">多模态大型语言模型</font>](https://zhida.zhihu.com/search?content_id=249409586&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E5%9E%8B%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> (MLLMs) 的发展在各个领域（例如多模态代理、具身智能）的日益增长的需求推动下取得了重大进展。 尽管模型驱动的方法试图通过不同的架构来增强 MLLMs 的能力，但其收益已变得越来越微不足道。 相反，数据驱动的方法通过扩展图像文本指令数据来提升效率，但面临着数据多样性和复杂性有限的挑战。 </font>**<font style="color:#74B602;">高质量数据的缺乏构成了 MLLMs 发展的一大障碍。</font>**

<font style="color:rgb(25, 27, 31);">对现有的用于生成图像-文本指令数据的基于数据的分析方法的分析揭示了三个常见的局限性：</font>

1. **<font style="color:#2F4BDA;">指令多样性有限</font>**<font style="color:rgb(25, 27, 31);">： 手动标注的指令受限于标注者的认知能力，而模型生成的指令受限于模板预设，难以满足现实世界中各种任务需求。 这限制了MLLMs的指令遵循能力。 </font>
2. **<font style="color:#2F4BDA;">指令复杂度有限</font>**<font style="color:rgb(25, 27, 31);">：手动标注通常会导致简单或中等复杂度的指令，而自动生成的指令往往简短且缺乏视觉推理步骤，这限制了模型处理复杂任务的能力。</font>
3. **<font style="color:#2F4BDA;">对齐粒度不足</font>**<font style="color:rgb(25, 27, 31);">： 手动和模型生成的指令都主要关注常见物体，而忽略了稀有或小物体，导致图像-文本对齐的粒度有限。 这会影响模型的视觉感知鲁棒性和对幻觉的抵抗力。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">MMEvol</font>](https://zhida.zhihu.com/search?content_id=249409586&content_type=Article&match_order=1&q=MMEvol&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，一个新颖的</font>**<font style="color:#ED740C;">多模态指令数据演化框架</font>**<font style="color:rgb(25, 27, 31);">。 该框架通过细粒度感知、认知推理和交互演化的精细组合迭代地提高数据质量，生成更复杂和多样化的图像文本指令数据集，从而赋予 MLLMs 更强的能力。</font>

<font style="color:rgb(25, 27, 31);">《</font><font style="color:rgb(25, 25, 25);">MMEvol: Empowering Multimodal Large Language Models with Evol-Instruct</font><font style="color:rgb(25, 27, 31);">》</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://arxiv.org/pdf/2409.05840](https://arxiv.org/pdf/2409.05840)

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://mmevol.github.io/](https://mmevol.github.io/)

**参考：**[**https://zhuanlan.zhihu.com/p/1936308162**](https://zhuanlan.zhihu.com/p/1936308162)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239062356-d7a7ec94-0b13-42f6-ab57-5be7a0c4b172.png)

<font style="color:rgb(25, 27, 31);">图 1: MMEvol 概述。 指令演化和指令消除通过多轮协同合作，以增强</font>**<font style="color:#74B602;">指令数据的多样性和复杂性。</font>**

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">设计了一个</font>**<font style="color:#74B602;">图像文本指令进化框架，MMEvol</font>**<font style="color:rgb(25, 27, 31);">，以利用先进的 MLLM，自动生成跨不同难度级别的开放域图像文本指令数据，以增强现有数据集的多样性和复杂性。</font>
2. <font style="color:rgb(25, 27, 31);">通过利用指令进化数据，构建了一个</font>**<font style="color:#74B602;">高质量的数据配方</font>**<font style="color:rgb(25, 27, 31);">，并且进化后的数据将被发布，以进一步提升其他开源 MLLM 的能力。</font>
3. <font style="color:rgb(25, 27, 31);">我们使用这种高质量的数据配方训练了一个 MLLM，与其他完全开源的方法相比，在各种下游视觉语言任务中取得了优异的性能。</font>
4. <font style="color:rgb(25, 27, 31);">通过大量的定性和定量分析验证了所提出方法的有效性和效率。</font>

:::color5
**<font style="color:#601BDE;">2.MM-Evol 概述</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">MM-Evol中每个演化周期包含两个主要步骤：</font>**<font style="color:#74B602;">指令演化和指令消除</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">指令演化</font>**<font style="color:rgb(25, 27, 31);">：随机选择</font>**<font style="color:#74B602;">细粒度感知演化、认知推理演化或交互演化之一</font>**<font style="color:rgb(25, 27, 31);">，将简单的指令升级为更复杂或更多样化的指令。 </font>
    - **<font style="color:rgb(25, 27, 31);">细粒度感知演化</font>**<font style="color:rgb(25, 27, 31);">：旨在利用图像中的视觉信息来生成包含</font>**<font style="color:#ECAA04;">更详细信息的数据</font>**
    - **<font style="color:rgb(25, 27, 31);">认知推理演化</font>**<font style="color:rgb(25, 27, 31);">：延长了指令的视觉操作推理步骤以</font>**<font style="color:#ECAA04;">增加其复杂性</font>**
    - **<font style="color:rgb(25, 27, 31);">交互演化</font>**<font style="color:rgb(25, 27, 31);">：旨在通过提供更多样化的指令形式来增强</font>**<font style="color:#ECAA04;">指令多样性</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">指令消除</font>**<font style="color:rgb(25, 27, 31);">：为了解决演化指令中偶尔出现的错误，我们使用</font>**<font style="color:#ECAA04;">指令消除来过滤掉失败的演化</font>**<font style="color:rgb(25, 27, 31);">。 MMEvol 重复指令演化和消除过程多次，以获得包含各种指令形式的复杂指令数据集。</font>

:::color5
**<font style="color:#601BDE;">3.种子指令：SEED-163K</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239368945-81646069-61a7-4688-a782-fc749623449c.png)

<font style="color:rgb(25, 27, 31);">种子指令数据</font>**<font style="color:#601BDE;">SEED-163K</font>**<font style="color:rgb(25, 27, 31);">是从 </font>**<font style="color:#74B602;">LLaVA-Instruct和 ShareGPT4V </font>**<font style="color:rgb(25, 27, 31);">数据集中整理而来，并补充了从 </font>[<font style="color:rgb(9, 64, 142);">Cambrain-1</font>](https://zhida.zhihu.com/search?content_id=249409586&content_type=Article&match_order=1&q=Cambrain-1&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 中抽取的额外科学和图表数据。 此过程涉及仔细选择和优化，以确保指令的质量和多样性。 对于只有标题的指令，我们使用 OpenAI GPT-4o mini API 来生成种子指令数据。 最终，在合并和过滤后，我们获得了包含 163K 个具有独特图像的指令样本的综合数据集，它为我们后续的 Evol-Instruct 奠定了基础。</font>

<font style="color:rgb(25, 27, 31);">为了验证MMEvol的有效性，我们</font>**<font style="color:#74B602;">对 163K 个种子数据进行了三轮演化迭代，产生了 447K 个演化样本</font>**<font style="color:rgb(25, 27, 31);">。 我们使用这些演化数据微调了开源的 LLaVA-NeXT 模型，并在 13 个视觉语言基准测试中与其他先进方法进行了比较。 我们的方法取得了最先进 (SOTA) 的性能，证明了MMEvol的有效性和效率。</font>

:::color5
**<font style="color:#601BDE;">4.MM-Evol 的前缀提示</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239674172-1559cd3c-f01f-4e68-987c-16cad43d7fff.png)

<font style="color:rgb(25, 27, 31);">MM-Evol 的前缀提示。 </font>

**<font style="color:rgb(25, 27, 31);">顶部块</font>**<font style="color:rgb(25, 27, 31);">：展示了上下文，例如标题和视觉对象位置</font>

**<font style="color:rgb(25, 27, 31);">中间块</font>**<font style="color:rgb(25, 27, 31);">：展示了以视觉/语言为中心的原子命题和演化目标。 此外，我们通过伪函数调用赋予视觉能力，以增强进化过程中的视觉推理。 </font>

**<font style="color:rgb(25, 27, 31);">底部块</font>**<font style="color:rgb(25, 27, 31);">：进一步阐明了组织好的种子样本，这些样本随后被发送到 MLLM 进行重写。</font>

:::color5
**<font style="color:#601BDE;">5.细粒度感知进化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239762135-54344b49-ad3c-4256-842a-c1720fd26ccf.png)

<font style="color:rgb(25, 27, 31);">细粒度感知进化提示和数据示例。 细粒度感知进化可以生成包含</font>**<font style="color:#74B602;">更详细视觉信息的样本</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#74B602;">增强数据多样性</font>**<font style="color:rgb(25, 27, 31);">，这些样本以不同的颜色标记以更好地可视化。</font>

:::color5
**<font style="color:#601BDE;">6.认知推理进化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239791960-a268ea5d-28e2-45f7-a6b8-7b81caed5b20.png)

<font style="color:rgb(25, 27, 31);">认知推理进化提示模板和示例。 认知推理进化可以使</font>**<font style="color:#74B602;">指令数据拥有更长的视觉推理链</font>**<font style="color:rgb(25, 27, 31);">，从而增加</font>**<font style="color:#74B602;">数据的复杂性</font>**<font style="color:rgb(25, 27, 31);">。 我们使用不同的颜色突出显示更改以更好地可视化。</font>

:::color5
**<font style="color:#601BDE;">7.交互式演化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239842448-4e157893-d635-424a-8980-aef3486fb817.png)

<font style="color:rgb(25, 27, 31);">交互式演化提示模板和示例。 交互式演化可以</font>**<font style="color:#74B602;">自动生成各种类型的非预定义指令格式，显著提高数据的多样性</font>**<font style="color:rgb(25, 27, 31);">。 使用不同的颜色突出显示差异，以更好地可视化。</font>

:::color5
**<font style="color:#601BDE;">8.指令消除 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743239891467-0c712b0f-4d8a-4076-a414-ca10ea725649.png)

<font style="color:rgb(25, 27, 31);">指令消除提示模板。 指令消除用于计算指令数据的演化增益和复杂度水平。 我们根据演化增益</font>**<font style="color:#74B602;">过滤掉无法演化的有害数据。</font>**

:::color5
**<font style="color:#601BDE;">9.质量评测 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **技能长度对比 & 推理步骤长度对比 & 复杂度对比****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743240228209-fca84cfd-1acf-4024-875b-1bcfe891a91f.png)

图9 (a) 种子数据和我们进化后的数据之间的技能长度分布；(b) 种子数据和我们进化后的数据之间的推理步骤长度分布；(c) 种子数据和我们进化后的数据之间的难度和复杂度水平分布。

<font style="color:rgb(25, 27, 31);">我们从种子数据中随机抽取 30K 个数据点，并在演化前后对指令数据进行定性分析。 如 </font>[图 ](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10)<font style="color:rgb(25, 27, 31);">9 所示，进化后的数据明显更复杂。 具体来说，每个进化后的指令在 </font>[图 9(a)](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10.sf1)<font style="color:rgb(25, 27, 31);"> 中涉及 0.68 个更多的原子能力，并且与进化前相比，在 </font>[图 9(b)](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10.sf2)<font style="color:rgb(25, 27, 31);"> 中，其平均视觉操作链推理长度长 0.86。 如 </font>[图 9(c)](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F10.sf3)<font style="color:rgb(25, 27, 31);"> 所示，每个演化轮次的</font>**<font style="color:#74B602;">平均难度得分呈递增趋势</font>**<font style="color:rgb(25, 27, 31);">，这表明认知推理演化在提高指令数据复杂性方面是有效的。</font>

2. **多样性对比（根动词和其直接名词宾语）****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743240061516-3d11c6e0-5781-4376-881f-ca19d654d841.png)

图 10: (a) 中种子数据的根动词（内圈）及其顶层名词宾语（外圈）和 (b) 中演化后的数据的根动词及其顶层名词宾语。

<font style="color:rgb(25, 27, 31);">我们识别生成的指令中的动词-名词结构，以研究生成的指令类型和演化数据的多样性。 我们使用 Berkeley 神经解析器 解析指令，</font>**<font style="color:#74B602;">提取最靠近根的动词及其第一个直接名词宾语</font>**<font style="color:rgb(25, 27, 31);">。 </font>[图 ](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F9)<font style="color:rgb(25, 27, 31);">10绘制了数量超过 2K 的根动词及其直接宾语。 我们观察到，与演化前相比，</font>**<font style="color:#74B602;">演化后的数据显着提高了指令多样性，演化后的指令具有不同的意图和文本格式。</font>**<font style="color:rgb(25, 27, 31);"> </font>

3. **长尾视觉对象****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743240413814-daae1938-ae60-46a2-9dba-4e15a3da160a.png)

<font style="color:rgb(25, 27, 31);">图 11： 种子数据和进化数据之间 200 个视觉对象的 长尾分布。 MMEvol 显着改善了种子数据中视觉对象的 长尾分布，提供了更细粒度的视觉信息，从而提高了模型的泛化能力和抵抗幻觉的能力。</font>

<font style="color:rgb(25, 27, 31);">此外，我们对演化前后指令数据中的视觉对象域进行了长尾分布可视化分析，以验证细粒度感知演化的有效性。</font>[图 11](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2409.05840v3%23S3.F11)<font style="color:rgb(25, 27, 31);"> 显示，细粒度的感知演化极大地</font>**<font style="color:#74B602;">改善了长尾视觉对象的分布</font>**<font style="color:rgb(25, 27, 31);">，最大限度地从图像中提取可用的视觉信息，细化指令数据中图像-文本对齐的粒度，增强数据多样性，从而提高模型泛化能力并减少视觉幻觉。</font>

## STaR**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">STaR旨在解决如何提高语言模型在复杂推理任务上的性能，例如数学问题解答或常识问答。STaR（Self-Taught Reasoner）算法的原理是通过迭代地利用少量推理示例（rationales）和大量没有推理的大数据集，来引导模型逐步提升执行更复杂推理的能力。STaR算法的核心是一个简单的循环过程。</font>

**paper：**[**STaR: Self-Taught Reasoner Bootstrapping Reasoning With Reasoning**](https://arxiv.org/pdf/2203.14465)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058832190-3fe2056a-2c4d-41bf-b16e-603f95cfae05.png)

:::color5
**<font style="color:#601BDE;">1.STaR步骤 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058931163-f7d26519-849a-45b0-aaed-a33cc528406c.png)

:::color5
**<font style="color:#601BDE;">2.评估 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">算术（Arithmetic）</font>**<font style="color:rgb(25, 27, 31);">：验证模型在解决不同位数的加法问题上的性能。STaR显著提高了模型在多位数加法问题上的准确率。特别是引入合理化（rationalization）步骤后，模型的性能提升更为显著。</font>
2. **<font style="color:rgb(25, 27, 31);">常识推理（Commonsense Reasoning）</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">CommonsenseQA</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=CommonsenseQA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（CQA）数据集，评估模型在多项选择常识问题上的表现。在CommonsenseQA数据集上，STaR在开发集上的准确率超过了仅使用少量样本提示的基线（增加了35.9%），并且与直接预测答案的基线相比也有显著提升（增加了12.5%）。当与比STaR模型大30倍的模型相比时，STaR的性能与之相当（72.5% vs 73.0%）。</font>
3. **<font style="color:rgb(25, 27, 31);">小学数学（Grade School Math）</font>**<font style="color:rgb(25, 27, 31);">：利用</font>[<font style="color:rgb(9, 64, 142);">GSM8K</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=GSM8K&zhida_source=entity)<font style="color:rgb(25, 27, 31);">数据集，测试模型解决自然语言表述的数学问题的能力。STaR显著提高了模型在GSM8K数据集上的性能，即使训练数据较少（无合理化的模型使用了25.0%的数据，合理化的模型使用了28.7%的数据）。</font>





## Dyn-VQA（OmniSearch）**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：OmniSearch 是阿里巴巴通义实验室推出的一款</font>**<font style="color:#ED740C;">多模态检索增强生成框架</font>**<font style="color:rgb(51, 51, 51);">，具备自适应规划能力。OmniSearch 能够动态拆解复杂问题，根据检索结果和问题情境调整检索策略，模拟人类在解决复杂问题时的行为方式，从而提升检索效率和准确性。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">paper</font>**<font style="color:rgba(0, 0, 0, 0.9);">:</font>[https://arxiv.org/pdf/2411.02937](https://arxiv.org/pdf/2411.02937)

:::

:::color5
**<font style="color:#601BDE;">1.基于OmniSearch的VQA示例 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

user query：图中的车价格是多少？

```python
<思考> 为了给这个车定价，首先需要确定车的模型和造价
<检索> 图搜图
<子问题> 车的模型和造价是什么？
```

```python
<思考> 根据检索结果，我们知道这个车是小米su7，我们需要知道小米su7的价格
<检索> 文本召回，小米su7的价格
<子问题> 小米su7的价格是多少？
```

```python
<思考> 根据检索结果，小米su7有不同的款型，不同款型价格不同。标准版215000，pro 245990，max 299900
<回答> 图中车是小米su7，不同款型价格不同。标准版215000，pro 245990，max 299900。
```

:::color5
**<font style="color:#601BDE;">2.动态问答数据集：Dyn-VQA  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">为了</font>**<font style="color:#ED740C;">评估多模态RAG技术在动态场景中的表现</font>**<font style="color:rgba(0, 0, 0, 0.9);">，阿里团队创建了一个全新的数据集—</font>**<font style="color:rgba(0, 0, 0, 0.9);">Dyn-VQA</font>**<font style="color:rgba(0, 0, 0, 0.9);">。该数据集包含三种类型的问题：</font>

1. **<font style="color:rgba(0, 0, 0, 0.9);">快速变化的答案</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如“某位明星最新的电影是什么？”，需要实时更新的知识。</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">需要多模态知识的问题</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如“这个球队的标志是什么物体？”，需要结合图像和文本信息。</font>
3. **<font style="color:rgba(0, 0, 0, 0.9);">多跳推理问题</font>**<font style="color:rgba(0, 0, 0, 0.9);">：如“这两位演员谁的票房更高？”，需要分步推理并结合多来源信息。</font>

<font style="color:rgba(0, 0, 0, 0.9);">Dyn-VQA 数据集不仅覆盖多个领域，还模拟了真实世界中的复杂场景，是现有数据集中极具挑战性的代表。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741514485743-d64fa14a-4bc7-49df-8b7c-fa2a3b9f1b07.png)

```python
Q:谁设计了图中的建筑
GT：Antonio Barluzzi
图搜图结果：Dominus Flevit Church
网络搜索结果：Dominus Flevit Church + 设计师Antonio Barluzzi
```

1. 答案迅速改变的问题

```python
Q:图中这个人的最后一部电影是什么？
GT：Small Things Like These (2024)
图搜图结果：Cillian Murphy
网络搜索结果：Cillian Murphy + Last film
网络搜索结果：Opperheimer
网络搜索结果：Cillian Murphy + Release Date 15 February 2024
```

2. 答案需要多模态的知识

```python
Q:图中的队标是什么物品？
GT：黄黑色的球
图搜图结果：科比
网络搜索结果：科比 + NBA球队 湖人
文搜图：湖人队标
```

3. 多跳问题（需要子任务拆解，多步推理）

```python
Q:图中谁的身价更高
GT：沈腾，右边的人
图搜图结果：贾玲、沈腾
网络搜索结果：贾玲，身价100
网络搜索结果：沈腾，身价200
```



## LLaVAR**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：基于LLAVA的文档理解多模态大模型</font>

<font style="color:rgb(51, 51, 51);">《</font><font style="color:rgb(54, 54, 54);">LLaVAR: Enhanced Visual Instruction Tuning for Text-rich Image Understanding</font><font style="color:rgb(51, 51, 51);">》</font>

:::

:::color5
**<font style="color:#601BDE;">1.训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">数据源：LAION-5B</font>
+ <font style="color:rgb(25, 27, 31);">数据处理：</font>
    - <font style="color:rgb(25, 27, 31);">从LAION-5B中</font>**<font style="color:#74B602;">过滤出一批带有文字的图片</font>**<font style="color:rgb(25, 27, 31);">，总量422k，14个图片聚类，涉及海报、封面、广告、logo等文字显著的图片类别。</font>
    - <font style="color:rgb(25, 27, 31);">他们将这些</font>**<font style="color:#74B602;">图片放缩为336x336，用paddleocr进行文字识别</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - <font style="color:rgb(25, 27, 31);">构建</font>**<font style="color:#74B602;">“读取图片中文字”相关的指令</font>**<font style="color:rgb(25, 27, 31);">，例如“Identify text visible in the image provided”，这批数据用于增强模型对图片中文字的理解能力；</font>
    - <font style="color:rgb(25, 27, 31);">在前面数据的基础上，他们进一步</font>**<font style="color:#74B602;">延续LLaVA的做法构建更加多样化的用户指令</font>**<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">1）他们先从14个图片聚类里挑了4个类别，主要为封面、海报等，总计16k images; </font>
        * <font style="color:rgb(25, 27, 31);">2）然后他们将ocr识别出的文本，图片描述（BLIP2生成）</font>**<font style="color:#ECAA04;">送入纯文本的GPT4，让其生成多样化的指令和回复，从而最终得到16k的多样化指令理解数据集</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">2.VQA指令数据构建示例 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741853579391-83cc1f02-09ae-471f-9859-713839d36b27.png)

1. 收集422K噪声指令跟踪数据：通过结合手动编写的指令（例如，“识别所提供图像中可见的任何文本”）和OCR结果。这种大规模的噪声对齐数据有效地改善了视觉特征和语言解码器之间的特征对齐。
2. 我们将OCR结果和图像caption输入GPT-4，**<font style="color:#74B602;">生成16K个对话，每个对话都可以多轮问答配对</font>**，作为示例后的高质量教学。要求GPT-4对OCR结果进行**<font style="color:#74B602;">去噪处理，并制定具体问题</font>**以创建复杂的基于输入的指令。

```python
OCR1: 一本偷偷看的书 让我们去深海吧。
Caption:一个黄色潜水器的图片，有一个男孩在里面
```

```python
Q：图中书的名字是什么？
A：让我们去深海吧。
Q：书的类型是什么？
A：一本偷偷看的书
```



## Florence-2 **<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51) !important;">Florence-2模型：</font>**<font style="color:#ED740C;">一种新颖的开源视觉语言模型（VLM），旨在处理各种视觉和多模型任务，包括字幕识别、对象检测、分割和OCR等内容。</font>**

:::

:::color5
**<font style="color:#601BDE;">1.训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">为了训练Florence-2模型，研究人员需要一个全面、大规模、高质量的多任务数据集，覆盖了各种图像数据。鉴于这种数据的稀缺性，他们由此创建了全新的多任务图像数据集——FLD-5B。</font>

<font style="color:rgb(51, 51, 51);">这一数据集中包含了1.26亿张图像、5亿个文本标注、13亿个文本-图像区域标注，以及36亿个文本短语-图像区域标注，跨横跨了不同的任务。</font>

**<font style="color:rgb(51, 51, 51);">数据格式</font>**

<font style="color:rgb(51, 51, 51) !important;">受大型语言模型的启发，Florence-2被设计为一种序列到序列的模型。它将图像和文本指令作为输入，并输出文本结果。输入或输出文本可以表示纯文本或图像中的区域。区域格式因任务而异：</font>

+ <font style="color:rgb(51, 51, 51) !important;">边界框：“<X1><Y1><X2><Y2>”用于对象检测任务。这些标记表示长方体左上角和右下角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">四边框：“<X1><Y1><X2><Y2><X3><Y3><X4><Y4>”用于文本检测，使用包围文本的四个角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">多边形：“<X1><Y1><Xn><Yn>'用于分割任务，其中坐标按顺时针顺序表示多边形的顶点。</font>

:::color5
**<font style="color:#601BDE;">2.数据pipeline </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">Florence-2数据引擎一共包含三个重要环节：</font>

<font style="color:rgb(51, 51, 51);">1) 使用专业模型进行初始标注</font>

<font style="color:rgb(51, 51, 51);">2) 数据过滤，纠正错误并移除无关标注</font>

<font style="color:rgb(51, 51, 51);">3) 迭代式的数据优化过程</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340588984-846de6c7-1166-4d52-8b0a-204334b652c6.png)

<font style="color:rgb(51, 51, 51);">FLD-5B中的每一张图像都由Florence数据引擎标注了文本、图像区域-文本对以及文本短语-图像区域三元组，涵盖了多个空间层次、从概括到详细的渐进粒度，以及多语义，让模型从不同角度实现了更全面的视觉理解能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340643905-62b28ba5-47b7-4fac-a796-6fa3685c0554.png)



## internVL-2.5**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">InternVL 2.5</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=InternVL+2.5&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，这是一种先进的大规模多模态大模型系列，基于InternVL 2.0的基础架构。InternVL系列的目标是缩小商业闭源模型与开源多模态模型之间的性能差距。在InternVL 2.5中，他们系统地探索了多模态大模型中的各种因素，包括</font>[<font style="color:rgb(9, 64, 142);">视觉编码器</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、语言模型、</font>[<font style="color:rgb(9, 64, 142);">数据集规模</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A7%84%E6%A8%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和推理时间的变化如何影响模型的整体性能，从而展示了多模态模型中扩展与性能之间的关系。</font>

**参考：**[**https://zhuanlan.zhihu.com/p/12309812997**](https://zhuanlan.zhihu.com/p/12309812997)

:::

:::color5
**<font style="color:#601BDE;">1.预训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了全面提升模型的性能并增强其处理复杂任务的能力，InternVL 2.5的训练数据集比InternVL 1.5和2.0更广泛且多样化。模型开发期间，专门使用对话格式的指令数据。在这一阶段，由于只有MLP或MLP和ViT的参数是可训练的，因此会</font>**<font style="color:rgb(25, 27, 31);">结合高质量和低质量的数据。</font>**<font style="color:rgb(25, 27, 31);">目标是通过接触多样的领域数据来丰富模型的世界知识，从而提高其泛化能力。训练语料库涵盖了</font>**<font style="color:#74B602;">字幕生成、通用问答、数学、图表、OCR、知识、定位、文档、对话、医疗和GUI任务等领域。</font>**

:::color5
**<font style="color:#601BDE;">2.微调数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">从InternVL 1.5到2.0再到2.5，数据集在规模、质量和多样性上进行了迭代改进。数据规模方面，样本数量从InternVL 1.5的510万增长到InternVL 2.0的730万，并在InternVL 2.5中进一步翻倍至</font>**<font style="color:#74B602;">1630万</font>**<font style="color:rgb(25, 27, 31);">。在多样性方面，训练数据涵盖多个领域，包括</font>**<font style="color:#74B602;">通用问答、图表、文档、OCR、科学、医疗、GUI、代码、数学等，同时覆盖多种模态，如单图像、多图像、视频和文本。</font>**

<font style="color:rgb(25, 27, 31);">在InternVL 2.5中，</font>**<font style="color:#74B602;">单图像数据占据了45.92%的标记，多图像数据占9.37%，视频数据贡献了39.79%，纯文本数据占4.92%</font>**<font style="color:rgb(25, 27, 31);">。与早期版本相比，多图像和视频数据的增加最为显著，增强了InternVL 2.5对多图像和长视频的理解能力。质量提升通过统一对话模板、使用语言模型评分和精炼数据、去除重复模式、应用启发式规则过滤低质量样本，以及将短响应重写为高质量和更长的交互来实现。这确保了模型训练的稳健数据集。</font>

:::color5
**<font style="color:#601BDE;">3.数据处理pipeline </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742720896544-874e4e03-d4d1-4892-b359-9c4e86630891.png)

<font style="color:rgb(25, 27, 31);">在模型开发过程中，观察到</font>**<font style="color:#74B602;">LLM对数据噪声的敏感性显著高于视觉编码器</font>**<font style="color:rgb(25, 27, 31);">。即使是少量异常样本（例如，离群值或重复数据，仅数千个）也会在推理期间导致模型行为异常。</font>

<font style="color:rgb(25, 27, 31);">在这些异常中，</font>**<font style="color:#74B602;">重复生成</font>**<font style="color:rgb(25, 27, 31);">被识别为最具破坏性的问题之一。在许多开源或合成数据集中，仅仅数千个重复样本就会导致模型陷入重复循环，尤其是在长篇输出或CoT推理任务中。这种现象削弱了测试时缩放策略的有效性。为应对这一挑战并支持未来研究，我们设计了一种高效的数据过滤管道，以去除低质量样本，从而最大限度地减少重复生成的风险。</font>

**<font style="color:rgb(25, 27, 31);">数据过滤pipeline</font>**<font style="color:rgb(25, 27, 31);">：由两个模块组成。对于纯文本数据，实施了三种关键策略：</font>

1. **<font style="color:rgb(25, 27, 31);">基于LLM的质量评分</font>**<font style="color:rgb(25, 27, 31);">：首先将数据集分类为不同领域，低于指定阈值的样本被移除以确保数据质量。</font>
2. **<font style="color:rgb(25, 27, 31);">重复检测</font>**<font style="color:rgb(25, 27, 31);">：使用LLM结合特定提示识别重复样本。这些样本经过人工审查，低于阈值的样本被移除以保持数据质量。</font>
3. **<font style="color:rgb(25, 27, 31);">启发式规则过滤</font>**<font style="color:rgb(25, 27, 31);">：应用特定规则，如过滤掉异常长度的句子、过长的零序列、过多重复行的文本等，以识别数据中的异常。尽管这种方法可能偶尔产生误报，但它提高了异常样本的检测率。所有标记样本在最终移除前都经过人工审查。</font>

## Qwen2.5**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">最近，团队发布了 Qwen 系列的最新版本 </font>**<font style="color:rgb(25, 27, 31);">Qwen2.5</font>**<font style="color:rgb(25, 27, 31);">。在开源部分，他们发布了7种不同规模的预训练和指令微调模型，包括</font>**<font style="color:rgb(25, 27, 31);">0.5B、1.5B、3B、7B、14B、32B</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">72B</font>**<font style="color:rgb(25, 27, 31);">，并提供了原始模型（bfloat16 精度）及不同精度的量化版本。</font>

**paper：**[**https://arxiv.org/pdf/2412.15115**](https://arxiv.org/pdf/2412.15115)

**参考：**[**【LLM技术报告】Qwen2.5技术报告（全文）**](https://zhuanlan.zhihu.com/p/13936916587)

:::

:::color5
**<font style="color:#601BDE;">1.Pre-Train数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">更精细的数据过滤</font>**<font style="color:rgb(25, 27, 31);">：高质量的预训练数据对模型性能至关重要，因此数据质量评估和过滤是流程中的关键环节。团队利用 </font>**<font style="color:#74B602;">Qwen2-Instruct 模型作为数据质量过滤器，进行全面的多维度分析</font>**<font style="color:rgb(25, 27, 31);">，评估和打分训练样本。与 Qwen2 相比，这一方法显著提升了数据质量评估的能力，使得他们能够更好地保留高质量的训练数据，并有效过滤低质量的样本。</font>
+ **<font style="color:rgb(25, 27, 31);">更优的数学与代码数据</font>**<font style="color:rgb(25, 27, 31);">：在 Qwen2.5 的预训练过程中，团队加入了来自</font>**<font style="color:#74B602;"> Qwen2.5-Math 和 Qwen2.5-Coder 的训练数据</font>**<font style="color:rgb(25, 27, 31);">。这种整合策略非常有效，因为这些专业数据集帮助他们在数学推理和代码生成任务上取得了领先的表现。</font>
+ **<font style="color:rgb(25, 27, 31);">更高质量的合成数据</font>**<font style="color:rgb(25, 27, 31);">：为了生成高质量的合成数据，尤其是在数学、编程和知识领域，团队采用了 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-72B-Instruct </font>**<font style="color:rgb(25, 27, 31);">和 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-Math-72B-Instruct</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:#74B602;">通过使用专有奖励模型和 Qwen2-Math-RM-72B 模型进行严格的过滤</font>**<font style="color:rgb(25, 27, 31);">，进一步提高了这些合成数据的质量。</font>
+ **<font style="color:rgb(25, 27, 31);">更合理的数据混合</font>**<font style="color:rgb(25, 27, 31);">：为了优化预训练数据的分布，团队使用 </font>**<font style="color:rgb(25, 27, 31);">Qwen2-Instruct</font>**<font style="color:rgb(25, 27, 31);"> 模型对不同领域的内容进行分类与平衡。分析显示，像电子商务、社交媒体和娱乐等领域在互联网数据中占比过大，常包含重复、模板化或机器生成的内容。相比之下，</font>**<u><font style="color:#74B602;">技术、科学和学术研究等领域虽然包含更高质量的信息，却常常被低估</font></u>**<font style="color:rgb(25, 27, 31);">。通过对过度代表的领域进行下采样，并对高价值领域进行上采样，他们确保了一个更加平衡且信息丰富的训练数据集，更好地服务于模型的学习目标。</font>

<font style="color:rgb(25, 27, 31);">凭借这些技术手段，团队开发了一个更大、更高质量的预训练数据集，将 Qwen2 的 7T tokens 扩展到了 18T tokens。</font>

:::color5
**<font style="color:#601BDE;">2.Post-Train数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2.5的监督微调过程采用了一个包含数百万个高质量示例的庞大数据集。此次数据扩展专门解决了Qwen2模型在多个关键领域中的局限性，特别是在</font>**<font style="color:#74B602;">长序列生成、数学问题解决、编码、指令执行、结构化数据理解、逻辑推理、跨语言迁移和系统指令</font>**<font style="color:rgb(25, 27, 31);">的鲁棒性方面。</font>



## baichuan2 **<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Baichuan 2有两个版本的型号，Baichuan 2-7B 70亿参数和Baichuan 2 - 13B拥有130亿个参数。 两个都模型接受了 2.6 万亿个token的训练，其中，迄今为止最大的预训练数据量，是baichuan 1的两倍。有了如此海量的训练数据，Baichuan 2较之取得显着提升。在 </font>[<font style="color:rgb(9, 64, 142);">MMLU</font>](https://zhida.zhihu.com/search?content_id=233812388&content_type=Article&match_order=1&q=MMLU&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 等通用基准CMMLU和 C-Eval中Baichuan 2 - 7B 性能较Baichuan 1提高近 30%。 </font>

**paper：**[**https://arxiv.org/pdf/2309.10305**](https://arxiv.org/pdf/2309.10305)

**参考：**[**https://zhuanlan.zhihu.com/p/655576902**](https://zhuanlan.zhihu.com/p/655576902)

:::

:::color5
**<font style="color:#601BDE;">1.预训练数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">数据来源：</font>**<font style="color:rgb(25, 27, 31);">在数据获取过程中，目标是在数据规模和代表性方面追求全面的数据多样性。百川智能从各种来源收集数据，包括通用互联网网页、书籍、研究论文、代码库等，以构建一个广泛的世界知识体系。</font>

<font style="color:rgb(25, 27, 31);">Baichuan 2训练数据中不同类别的分布情况如下：</font>

1. <font style="color:rgb(25, 27, 31);">Web pages: 40%</font>
2. <font style="color:rgb(25, 27, 31);">Books: 30%</font>
3. <font style="color:rgb(25, 27, 31);">Research papers: 20%</font>
4. <font style="color:rgb(25, 27, 31);">Codebases: 5%</font>
5. <font style="color:rgb(25, 27, 31);">Other resources (e.g., news articles, blogs): 5%</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::success
**训练数据分布**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611234348-b6ee7299-d2a2-402a-a280-b6eea411f891.png)

:::

:::success
**Scaling Law**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742611307517-a53d102b-24ad-4a6a-a757-8eeec495aad1.png)

:::



:::color5
**<font style="color:#601BDE;">2.数据处理pipeline </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">数据处理：</font>**<font style="color:rgb(25, 27, 31);">对于数据处理，关注的是数据频率和质量。数据频率依赖于聚类和去重。百川智能建立了一个支持LSH(Locality Sensitive Hashing)特征和密集嵌入特征的大规模去重和聚类系统。这个系统可以在数小时内对数十亿甚至万亿级别的数据进行去重和聚类。基于聚类，单个文档、段落和句子被去重并打分。这些分数随后用于预训练阶段的数据采样。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742610381101-c0c1eb4d-2c58-42e4-9cef-9dd787b665c6.png)

# 数据集挑战
| <font style="color:rgb(51, 51, 51);">挑战                  </font> | <font style="color:rgb(51, 51, 51);">解决方案                                </font> | <font style="color:rgb(51, 51, 51);">实施案例                    </font> |
| :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">数据质量不均衡        </font> | <font style="color:rgb(51, 51, 51);">混合专家（MoE）过滤系统                  </font> | <font style="color:rgb(51, 51, 51);">LLaMA的CCNet pipeline        </font> |
| <font style="color:rgb(51, 51, 51);">多语言对齐困难        </font> | <font style="color:rgb(51, 51, 51);">语言特定标识符插入                      </font> | <font style="color:rgb(51, 51, 51);">BLOOM的</font><font style="color:rgb(51, 51, 51);">zh标记          </font> |
| <font style="color:rgb(51, 51, 51);">长文本建模            </font> | <font style="color:rgb(51, 51, 51);">滑动窗口分块策略                        </font> | <font style="color:rgb(51, 51, 51);">GPT-4的32k上下文处理        </font> |
| <font style="color:rgb(51, 51, 51);">时效性缺失            </font> | <font style="color:rgb(51, 51, 51);">持续增量预训练                          </font> | <font style="color:rgb(51, 51, 51);">ChatGPT的每月更新机制</font><font style="color:rgb(51, 51, 51);"> </font> |




# 数据实践建议
1. **数据构成黄金法则**：
    - <font style="color:rgb(51, 51, 51);">预训练：通用语料（60%）+ 领域数据（30%）+ 代码（10%）</font>
    - <font style="color:rgb(51, 51, 51);">SFT阶段：1k~100k高质量样本足矣</font>
    - <font style="color:rgb(51, 51, 51);">RLHF：偏好数据量 > 10k对比对</font>
2. **数据生命周期管理**：
3. **开源工具推荐**：
    - <font style="color:rgb(51, 51, 51);">数据处理：datatrove、fasttext</font>
    - <font style="color:rgb(51, 51, 51);">质量检测：lm_dataformat、cc_net</font>
    - <font style="color:rgb(51, 51, 51);">标注平台：Label Studio、Prodigy</font>

<font style="color:rgb(51, 51, 51);">当前最前沿的数据策略正在向三个方向发展：</font>

<font style="color:rgb(51, 51, 51);">1）合成数据与真实数据的动态平衡；</font>

<font style="color:rgb(51, 51, 51);">2）多模态数据联合训练；</font>

<font style="color:rgb(51, 51, 51);">3）自我改进的数据生态系统。建议关注HuggingFace的datasets库和AI2的Dolma项目获取最新开源数据集。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739963548923-ba680f02-52f0-4115-a81a-15d4b2f1802e.png)



# 类别不平衡
## 思路1：Focal Loss<font style="color:#DF2A3F;"> </font><font style="color:#D22D8D;">(by草莓师姐)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Focal Loss是由何恺明团队在2017年提出的一种改进的损失函数，主要用于解决目标检测任务中的</font>**<font style="color:rgb(51, 51, 51);">类别不平衡问题</font>**<font style="color:rgb(51, 51, 51);">。在目标检测（如RetinaNet）中，背景（负样本）通常占比极高，而前景（正样本）占比较低，传统的交叉熵损失会因大量简单负样本的主导而降低模型性能。</font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

**<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">通过动态调整损失权重，减少易分类样本（高置信度的样本）的损失贡献，使模型更关注难分类样本（低置信度的样本）。</font>

**<font style="color:rgb(51, 51, 51);">数学公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">对于二分类问题，设预测概率为 p，真实标签为 y∈{0,1}，Focal Loss定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740642542307-79766d52-f602-4774-a5a6-50b99aef6698.png)

<font style="color:rgb(51, 51, 51);">其中：</font>

+ <font style="color:rgb(51, 51, 51);">p</font><sub><font style="color:rgb(51, 51, 51);">t</font></sub><font style="color:rgb(51, 51, 51);">，即模型对真实类别的预测概率。</font>
+ <font style="color:rgb(51, 51, 51);">α∈[0,1]：平衡正负样本的权重（常用0.25）。</font>
+ <font style="color:rgb(51, 51, 51);">γ≥0：调节难易样本的权重（常用2.0）。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(51, 51, 51);">计算交叉熵损失</font>**<font style="color:rgb(51, 51, 51);">：CE(pt)=−log⁡(pt)</font>
2. **<font style="color:rgb(51, 51, 51);">引入调制因子</font>**<font style="color:rgb(51, 51, 51);"> (1−pt)γ：</font>
    - <font style="color:rgb(51, 51, 51);">当 pt→1</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">（易分类样本），因子趋近于0，降低损失权重。</font>
    - <font style="color:rgb(51, 51, 51);">当 pt→0（难分类样本），因子趋近于1，保留损失权重。</font>
3. **<font style="color:rgb(51, 51, 51);">平衡正负样本</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用 α</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 调整正负样本的权重（如负样本占比高，则降低其权重）。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 显著缓解类别不平衡问题。   </font><font style="color:rgb(51, 51, 51);">2. 提升模型对难样本的学习能力。   </font><font style="color:rgb(51, 51, 51);">3. 在密集检测任务（如RetinaNet）中表现优异。</font> | <font style="color:rgb(51, 51, 51);">1. 需调参（</font><font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">γ</font>_<font style="color:rgb(51, 51, 51);">γ</font>_<font style="color:rgb(51, 51, 51);">）。   </font><font style="color:rgb(51, 51, 51);">2. 对噪声标签敏感（难样本可能包含噪声）。</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(51, 51, 51);">目标检测</font>**<font style="color:rgb(51, 51, 51);">：RetinaNet、YOLO等。</font>
2. **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">：长尾分布（如少数类样本稀缺）。</font>
3. **<font style="color:rgb(51, 51, 51);">语义分割</font>**<font style="color:rgb(51, 51, 51);">：处理类别不平衡的像素级预测任务。</font>
4. **<font style="color:rgb(51, 51, 51);">自然语言处理</font>**<font style="color:rgb(51, 51, 51);">：实体识别中的罕见实体检测。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(51, 51, 51);">动态参数调整</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">根据训练阶段动态调整</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">γ</font>_<font style="color:rgb(51, 51, 51);">γ</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">或</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">。</font>
2. **<font style="color:rgb(51, 51, 51);">结合其他损失</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">如Focal Loss + Dice Loss（医学图像分割）。</font>
3. **<font style="color:rgb(51, 51, 51);">类别自适应调制</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">为不同类别分配不同的</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">γ</font>_<font style="color:rgb(51, 51, 51);">γ</font>_<font style="color:rgb(51, 51, 51);">。</font>
4. **<font style="color:rgb(51, 51, 51);">噪声鲁棒性改进</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">结合标签平滑（Label Smoothing）或课程学习（Curriculum Learning）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        # 计算交叉熵损失
        ce_loss = F.binary_cross_entropy_with_logits(
            inputs, targets, reduction='none'
        )
        
        # 计算概率 p_t
        p_t = torch.exp(-ce_loss)  # p_t = p * targets + (1-p) * (1-targets)
        
        # 计算调制因子
        focal_loss = self.alpha * (1 - p_t) ** self.gamma * ce_loss
        
        # 聚合损失
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

# 示例用法
logits = torch.randn(4, 1)  # 模型输出（未归一化）
targets = torch.tensor([1., 0., 1., 1.])  # 真实标签（二分类）
loss_fn = FocalLoss(alpha=0.25, gamma=2.0)
loss = loss_fn(logits, targets)
print(loss)

```

```python
class MultiClassFocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2.0):
        super().__init__()
        self.alpha = alpha  # 形如 [C,] 的类别权重
        self.gamma = gamma

    def forward(self, inputs, targets):
        log_softmax = F.log_softmax(inputs, dim=-1)
        ce_loss = -log_softmax.gather(1, targets.view(-1, 1)).squeeze()
        p_t = torch.exp(-ce_loss)
        focal_loss = (1 - p_t) ** self.gamma * ce_loss
        if self.alpha is not None:
            focal_loss = self.alpha[targets] * focal_loss
        return focal_loss.mean()

```

## 思路2：课程学习<font style="color:#D22D8D;">(by草莓师姐)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">课程学习（Curriculum Learning）是受人类渐进式学习启发的机器学习范式，通过</font>**<font style="color:rgb(51, 51, 51);">有序的数据呈现策略</font>**<font style="color:rgb(51, 51, 51);">提升模型训练效果。以下从理论到实践全面剖析其核心机制：</font>

:::

:::color5
**<font style="color:#601BDE;">1.核心思想 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **认知科学基础**
    - <font style="color:rgb(51, 51, 51);">儿童语言习得研究显示：婴儿先掌握简单词汇（"爸爸"、"妈妈"），再逐步学习复杂语法结构</font>
    - <font style="color:rgb(51, 51, 51);">神经可塑性理论：大脑对新知识的吸收效率受信息复杂度梯度影响</font>

**机器学习映射**

2. <font style="color:rgb(51, 51, 51);">优化目标:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741070718416-5a536698-e2ab-49eb-9c9a-05c025f3cf1c.png)

其中pt(x)随时间t__演化的数据分布，需满足：

    - **<font style="color:rgb(51, 51, 51);">渐近性</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741070726192-3c26e6f1-d710-490b-bb4b-bfa442e25c10.png)
    - **<font style="color:rgb(51, 51, 51);">单调性</font>**<font style="color:rgb(51, 51, 51);">：样本难度D(x)随t</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">递增</font>

:::color5
**<font style="color:#601BDE;">2.课程设计三要素 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **难度评估器（Difficulty Measurer）**
    - <font style="color:rgb(51, 51, 51);">样本级指标：</font>

```python
def compute_difficulty(x):
    # 文本数据：句子长度 + 生僻词占比
    if modality == "text":
        length = len(tokenize(x))
        rarity = sum([1 for w in words if w in rare_vocab])/len(words)
        return 0.4*length + 0.6*rarity
    # 图像数据：纹理复杂度 + 目标数量
    elif modality == "image":
        edge_density = cv2.Laplacian(img, cv2.CV_64F).var()
        obj_count = len(detect_objects(img))
        return 0.7*edge_density + 0.3*obj_count
```

    - <font style="color:rgb(51, 51, 51);">动态评估方法：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741070776068-2943c754-6b14-4134-97cf-e59df9b46cba.png)

<font style="color:rgb(51, 51, 51);">其中L(x)</font>_<font style="color:rgb(51, 51, 51);">L</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">x</font>_<font style="color:rgb(51, 51, 51);">)为模型当前损失</font>

2. **<font style="color:rgb(51, 51, 51);">调度策略（Scheduler）</font>**

| **策略类型** | **数学形式** | **适用场景** |
| :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">线性调度</font> | <font style="color:rgb(51, 51, 51);">p</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">min</font><font style="color:rgb(51, 51, 51);">⁡</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">T</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">p</font>__<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">min</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">T</font>__<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">)</font> | <font style="color:rgb(51, 51, 51);">简单分类任务</font> |
| <font style="color:rgb(51, 51, 51);">指数调度</font> | <font style="color:rgb(51, 51, 51);">p</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">λ</font><font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">p</font>__<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">−</font>_<font style="color:rgb(51, 51, 51);">e</font>_<font style="color:rgb(51, 51, 51);">−</font>_<font style="color:rgb(51, 51, 51);">λ</font>__<font style="color:rgb(51, 51, 51);">t</font>_ | <font style="color:rgb(51, 51, 51);">快速收敛需求</font> |
| <font style="color:rgb(51, 51, 51);">阶段式调度</font> | <font style="color:rgb(51, 51, 51);">p</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">∑</font><font style="color:rgb(51, 51, 51);">k</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">K</font><font style="color:rgb(51, 51, 51);">I</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">≥</font><font style="color:rgb(51, 51, 51);">τ</font><font style="color:rgb(51, 51, 51);">k</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">p</font>__<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">∑</font>_<font style="color:rgb(51, 51, 51);">k</font>_<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font>_<font style="color:rgb(51, 51, 51);">K</font>_<font style="color:rgb(51, 51, 51);">I</font><font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">≥</font>_<font style="color:rgb(51, 51, 51);">τ</font>__<font style="color:rgb(51, 51, 51);">k</font>_<font style="color:rgb(51, 51, 51);">)</font> | <font style="color:rgb(51, 51, 51);">多阶段预训练</font> |


3. **<font style="color:rgb(51, 51, 51);">课程编排器（Curriculum Planner）</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741070835128-1ecc861f-46b6-4f5b-8ac8-f70779b9a504.png)

:::color5
**<font style="color:#601BDE;">3.大模型训练中的工程实践 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **GPT-3 预训练课程设计**
    - **<font style="color:rgb(51, 51, 51);">阶段1</font>**<font style="color:rgb(51, 51, 51);">（0-10B tokens）：  
</font><font style="color:rgb(51, 51, 51);">使用C4数据集简单子集（句子长度<128，词汇量5万）</font>
    - **<font style="color:rgb(51, 51, 51);">阶段2</font>**<font style="color:rgb(51, 51, 51);">（10-300B tokens）：  
</font><font style="color:rgb(51, 51, 51);">逐步加入书籍、学术论文等复杂语料</font>
    - **<font style="color:rgb(51, 51, 51);">阶段3</font>**<font style="color:rgb(51, 51, 51);">（300B+ tokens）：  
</font><font style="color:rgb(51, 51, 51);">引入代码数据（Python/JS）及多语言混合文本</font>
2. **视觉大模型应用案例**

```python
# 图像分类课程策略
class CurriculumSampler:
    def __init__(self, dataset):
        self.epoch = 0
        self.difficulty = compute_difficulty(dataset)
        
    def __iter__(self):
        if self.epoch < 5:
            idx = np.argsort(self.difficulty)[:len(self)//2]
        elif 5 <= self.epoch < 10:
            idx = np.random.permutation(len(self))
        else:
            idx = np.argsort(-self.difficulty)
        return iter(idx)

```

3. **分布式训练优化技巧**
    - <font style="color:rgb(51, 51, 51);">课程感知的数据分片：</font>

```python
# 按难度值分桶
shards = [data[i::num_shards] for i in range(num_shards)]
```

    - <font style="color:rgb(51, 51, 51);">动态负载均衡：根据各GPU处理的样本平均难度调整数据分配</font>

:::color5
**<font style="color:#601BDE;">4.效果评估 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(51, 51, 51);">典型性能提升</font>**

| **任务类型** | **基准准确率** | **课程学习准确率** | **收敛速度提升** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">文本分类</font> | <font style="color:rgb(51, 51, 51);">82.3%</font> | <font style="color:rgb(51, 51, 51);">85.7%</font> | <font style="color:rgb(51, 51, 51);">1.8x</font> |
| <font style="color:rgb(51, 51, 51);">目标检测</font> | <font style="color:rgb(51, 51, 51);">mAP 68.4</font> | <font style="color:rgb(51, 51, 51);">mAP 71.2</font> | <font style="color:rgb(51, 51, 51);">1.5x</font> |
| <font style="color:rgb(51, 51, 51);">机器翻译</font> | <font style="color:rgb(51, 51, 51);">BLEU 32.1</font> | <font style="color:rgb(51, 51, 51);">BLEU 34.9</font> | <font style="color:rgb(51, 51, 51);">2.1x</font> |


2. **核心挑战**
    - **<font style="color:rgb(51, 51, 51);">课程依赖性</font>**<font style="color:rgb(51, 51, 51);">：不同模型架构（Transformer vs CNN）需要差异化策略</font>
    - **<font style="color:rgb(51, 51, 51);">多模态对齐</font>**<font style="color:rgb(51, 51, 51);">：图文联合训练时需设计跨模态难度指标</font>
    - **<font style="color:rgb(51, 51, 51);">动态调整延迟</font>**<font style="color:rgb(51, 51, 51);">：实时课程更新带来的计算开销</font>
3. **未来方向**
    - <font style="color:rgb(51, 51, 51);">基于强化学习的自动课程生成</font>
    - <font style="color:rgb(51, 51, 51);">课程学习与提示学习的结合</font>
    - <font style="color:rgb(51, 51, 51);">量子化课程策略（Quantum-inspired Curriculum）</font>

:::color5
**<font style="color:#601BDE;">5.实用工具 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **开源框架**

```bash
pip install curriculum-learning
```

```python
from curriculum import LinearCurriculum, ExponentialCurriculum

# 创建课程调度器
curriculum = LinearCurriculum(total_steps=10000)

# 训练循环
for step in range(total_steps):
    difficulty = curriculum.get_difficulty(step)
    batch = sampler.sample(difficulty)
    train_step(batch)
```

2. **云服务API**

```python
import curriculum_api

client = curriculum_api.Client(api_key="YOUR_KEY")
curriculum = client.create_curriculum(
    dataset_id="your_dataset",
    modality="text",
    strategy="auto"
)
```

# LLM数据集
## 预训练
| **<font style="color:rgb(51, 51, 51);">数据集            </font>** | **<font style="color:rgb(51, 51, 51);">规模      </font>** | **<font style="color:rgb(51, 51, 51);">特点                                </font>** | **<font style="color:rgb(51, 51, 51);">应用场景                </font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">Common Crawl      </font> | <font style="color:rgb(51, 51, 51);">~300TB    </font> | <font style="color:rgb(51, 51, 51);">网络爬取原始文本                    </font> | <font style="color:rgb(51, 51, 51);">基础语言建模            </font> |
| <font style="color:rgb(51, 51, 51);">C4 (Colossal Cleaned Crawl)</font> | <font style="color:rgb(51, 51, 51);">750GB    </font> | <font style="color:rgb(51, 51, 51);">清洗后的高质量英文文本              </font> | <font style="color:rgb(51, 51, 51);">通用预训练              </font> |
| <font style="color:rgb(51, 51, 51);">The Pile          </font> | <font style="color:rgb(51, 51, 51);">825GB    </font> | <font style="color:rgb(51, 51, 51);">包含学术论文/代码等专业领域          </font> | <font style="color:rgb(51, 51, 51);">领域增强预训练          </font> |
| <font style="color:rgb(51, 51, 51);">ROOTS            </font> | <font style="color:rgb(51, 51, 51);">1.6TB    </font> | <font style="color:rgb(51, 51, 51);">59种语言混合语料                    </font> | <font style="color:rgb(51, 51, 51);">多语言模型              </font> |
| <font style="color:rgb(51, 51, 51);">GitHub Code      </font> | <font style="color:rgb(51, 51, 51);">200GB+    </font> | <font style="color:rgb(51, 51, 51);">开源代码（Python/Java等）            </font> | <font style="color:rgb(51, 51, 51);">代码模型预训练          </font> |




## SFT
| **<font style="color:rgb(51, 51, 51);">数据集            </font>** | **<font style="color:rgb(51, 51, 51);">规模      </font>** | **<font style="color:rgb(51, 51, 51);">结构                                </font>** | **<font style="color:rgb(51, 51, 51);">质量特征                </font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">Alpaca            </font> | <font style="color:rgb(51, 51, 51);">52K      </font> | <font style="color:rgb(51, 51, 51);">指令-响应对（GPT-4生成）            </font> | <font style="color:rgb(51, 51, 51);">多样化任务覆盖          </font> |
| <font style="color:rgb(51, 51, 51);">Dolly 2.0        </font> | <font style="color:rgb(51, 51, 51);">15K      </font> | <font style="color:rgb(51, 51, 51);">人工标注的问答对                    </font> | <font style="color:rgb(51, 51, 51);">高准确率                </font> |
| <font style="color:rgb(51, 51, 51);">OpenAssistant    </font> | <font style="color:rgb(51, 51, 51);">161K      </font> | <font style="color:rgb(51, 51, 51);">多轮对话数据集                      </font> | <font style="color:rgb(51, 51, 51);">对话场景优化            </font> |
| <font style="color:rgb(51, 51, 51);">FLAN v2          </font> | <font style="color:rgb(51, 51, 51);">1.8M      </font> | <font style="color:rgb(51, 51, 51);">跨任务指令数据集                    </font> | <font style="color:rgb(51, 51, 51);">零样本迁移能力          </font> |


  


## RLHF
| **<font style="color:rgb(51, 51, 51);">数据集            </font>** | **<font style="color:rgb(51, 51, 51);">标注方式  </font>** | **<font style="color:rgb(51, 51, 51);">特点                                </font>** | **<font style="color:rgb(51, 51, 51);">使用模型                </font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">Anthropic HH-RLHF</font> | <font style="color:rgb(51, 51, 51);">16K      </font> | <font style="color:rgb(51, 51, 51);">人类偏好排序数据                    </font> | <font style="color:rgb(51, 51, 51);">Claude系列              </font> |
| <font style="color:rgb(51, 51, 51);">OpenAI WebGPT    </font> | <font style="color:rgb(51, 51, 51);">20K+      </font> | <font style="color:rgb(51, 51, 51);">基于网页引用的对比数据              </font> | <font style="color:rgb(51, 51, 51);">GPT-3.5/4              </font> |
| <font style="color:rgb(51, 51, 51);">StackExchange    </font> | <font style="color:rgb(51, 51, 51);">10M+ votes</font> | <font style="color:rgb(51, 51, 51);">社区问答评分数据                    </font> | <font style="color:rgb(51, 51, 51);">开源模型对齐    </font> |


## 指令跟随
| **<font style="color:rgb(51, 51, 51);">数据集            </font>** | **<font style="color:rgb(51, 51, 51);">任务类型  </font>** | **<font style="color:rgb(51, 51, 51);">语言                                </font>** | **<font style="color:rgb(51, 51, 51);">示例                    </font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">Natural Instructions</font> | <font style="color:rgb(51, 51, 51);">1.6K tasks</font> | <font style="color:rgb(51, 51, 51);">多语言                            </font> | <font style="color:rgb(51, 51, 51);">跨任务泛化              </font> |
| <font style="color:rgb(51, 51, 51);">Super-NaturalInstruct</font> | <font style="color:rgb(51, 51, 51);">1600+ tasks</font> | <font style="color:rgb(51, 51, 51);">英文                              </font> | <font style="color:rgb(51, 51, 51);">复杂指令分解            </font> |
| <font style="color:rgb(51, 51, 51);">xP3              </font> | <font style="color:rgb(51, 51, 51);">46种任务  </font> | <font style="color:rgb(51, 51, 51);">82种语言                            </font> | <font style="color:rgb(51, 51, 51);">多语言指令              </font> |


## 幻觉
| **<font style="color:rgb(51, 51, 51);">数据集            </font>** | **<font style="color:rgb(51, 51, 51);">检测维度  </font>** | **<font style="color:rgb(51, 51, 51);">数据量                              </font>** | **<font style="color:rgb(51, 51, 51);">应用                    </font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">TruthfulQA        </font> | <font style="color:rgb(51, 51, 51);">真实性    </font> | <font style="color:rgb(51, 51, 51);">817 questions                      </font> | <font style="color:rgb(51, 51, 51);">事实性验证              </font> |
| <font style="color:rgb(51, 51, 51);">HaluEval          </font> | <font style="color:rgb(51, 51, 51);">多类型    </font> | <font style="color:rgb(51, 51, 51);">15K samples                        </font> | <font style="color:rgb(51, 51, 51);">综合幻觉检测            </font> |
| <font style="color:rgb(51, 51, 51);">FActScore        </font> | <font style="color:rgb(51, 51, 51);">事实粒度  </font> | <font style="color:rgb(51, 51, 51);">5K专家标注                          </font> | <font style="color:rgb(51, 51, 51);">细粒度事实核查    </font> |


## BenchMark
| **<font style="color:rgb(51, 51, 51);">数据集            </font>** | **<font style="color:rgb(51, 51, 51);">评估维度  </font>** | **<font style="color:rgb(51, 51, 51);">任务数                              </font>** | **<font style="color:rgb(51, 51, 51);">语言                    </font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">MMLU              </font> | <font style="color:rgb(51, 51, 51);">知识      </font> | <font style="color:rgb(51, 51, 51);">57 subjects                        </font> | <font style="color:rgb(51, 51, 51);">英文                    </font> |
| <font style="color:rgb(51, 51, 51);">BIG-Bench        </font> | <font style="color:rgb(51, 51, 51);">综合能力  </font> | <font style="color:rgb(51, 51, 51);">200+ tasks                          </font> | <font style="color:rgb(51, 51, 51);">多语言                  </font> |
| <font style="color:rgb(51, 51, 51);">HELM              </font> | <font style="color:rgb(51, 51, 51);">全面评估  </font> | <font style="color:rgb(51, 51, 51);">16 core scenarios                  </font> | <font style="color:rgb(51, 51, 51);">英文  </font> |




## 模型
### LLAMA
```python
# LLaMA 2 预训练数据构成
pretrain_data = {
    "CommonCrawl": {"weight": 67%, "epochs": 1.5},
    "C4": {"weight": 15%, "epochs": 1.5},
    "GitHub": 4.5%,  # 代码数据
    "Wikipedia": 4.5%,  # 多语言版本
    "Books": 4.5%,
    "ArXiv": 2.5%,
    "StackExchange": 2.0%
}
```

Qwen

```python
预训练：3.2TB清洗后的多语言数据（中英占比7:3）
微调：百万级人工标注指令数据
特色：
代码数据占比提升至12%
包含中文古典文献数字化文本
```

deepseek

```python
# DeepSeek-MoE 数据架构
data_strategy = {
    "基础语料": ["WuDaoCorpora 2.0", "Pile-zh"],
    "领域增强": {
        "STEM": ["arXiv", "ScienceDirect"],
        "代码": ["GitHub Clean", "LeetCode题解"],
        "中文特性": ["古诗文网", "人民日报语料"]
    },
    "质量过滤": [
        "重复率<0.9", 
        "困惑度过滤阈值p=0.7",
        "敏感词过滤表"
    ]
}
```



# 数据集评估
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：在评估数据集的质量时，可以从以下几个关键方面进行评估：</font>

1. **<font style="color:rgb(51, 51, 51);">数据多样性</font>**
2. **<font style="color:rgb(51, 51, 51);">数据平衡性</font>**
3. **<font style="color:rgb(51, 51, 51);">数据完整性</font>**
4. **<font style="color:rgb(51, 51, 51);">数据一致性</font>**
5. **<font style="color:rgb(51, 51, 51);">数据与任务的适合性</font>**
6. **<font style="color:rgb(51, 51, 51);">标注准确性</font>**

:::

:::color5
**<font style="color:#601BDE;">1.数据多样性</font>**

:::

**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：数据多样性指的是数据集中包含的各种样本是否足够多样化，能否覆盖不同的特征、类别或场景。多样化的数据有助于模型更好地泛化，避免过拟合特定数据分布。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">类别分布</font>**<font style="color:rgb(51, 51, 51);">：检查各个类别样本的数量是否均衡。</font>
+ **<font style="color:rgb(51, 51, 51);">特征多样性</font>**<font style="color:rgb(51, 51, 51);">：评估数据中特征的分布情况，确保没有某一特征主导数据集。</font>

```python
import pandas as pd
from collections import Counter

def assess_data_diversity(dataset, label_column):
    # 统计各类别的样本数量
    class_distribution = dataset[label_column].value_counts()
    print("Class Distribution:")
    print(class_distribution)
    
    # 统计每个类别中的特征分布
    if 'text' in dataset.columns:
        # 示例：统计文本长度分布
        text_lengths = dataset['text'].apply(len)
        print("\nText Length Distribution:")
        print(text_lengths.describe())
    
    # 统计其他特征的分布（如适用）
    # ...
```

:::color5
**<font style="color:#601BDE;">2.数据平衡性</font>**

:::

**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：数据平衡性指的是数据集中不同类别或样本的数量是否均衡。不平衡的数据可能导致模型偏向多数类，降低整体性能。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">类别分布比例</font>**<font style="color:rgb(51, 51, 51);">：计算各类别样本数量占总样本的比例。</font>
+ **<font style="color:rgb(51, 51, 51);">K分布检验</font>**<font style="color:rgb(51, 51, 51);">：使用统计方法检验数据是否符合均匀分布。</font>
+ **<font style="color:rgb(51, 51, 51);">重采样方法</font>**<font style="color:rgb(51, 51, 51);">：应用过采样或欠采样技术平衡数据。</font>

```python
from imblearn.metrics import classification_report_imbalanced
from imblearn import under_sampling, over_sampling
import matplotlib.pyplot as plt

def assess_data_balance(dataset, label_column):
    # 统计各类别样本数量
    class_counts = dataset[label_column].value_counts()
    print("Class Counts:", class_counts)
    
    # 绘制类别分布直方图
    plt.figure(figsize=(10, 6))
    class_counts.plot(kind='bar')
    plt.title('Class Distribution')
    plt.show()
    
    # 使用K分布检验
    from scipy.stats import chi2_contingency
    observed = class_counts.values
    expected = [sum(class_counts) / len(class_counts)] * len(class_counts)
    
    chi2, p, dof, _ = chi2_contingency([observed])
    print(f"Chi-square test p-value: {p}")
    
    # 应用欠采样或过采样
    if len(class_counts) == 2:
        # 示例：使用随机欠采样平衡二分类数据
        under_sampler = under_sampling.RandomUnderSampler(random_state=42)
        X_res, y_res = under_sampler.fit_resample(dataset.drop(label_column, axis=1), dataset[label_column])
        print("\nUnder-sampled Dataset Shape:", X_res.shape)
        print("Under-sampled Classes:", pd.Series(y_res).value_counts())
    elif len(class_counts) > 2:
        # 示例：使用过采样平衡多分类数据
        over_sampler = over_sampling.RandomOverSampler(random_state=42)
        X_res, y_res = over_sampler.fit_resample(dataset.drop(label_column, axis=1), dataset[label_column])
        print("\nOver-sampled Dataset Shape:", X_res.shape)
        print("Over-sampled Classes:", pd.Series(y_res).value_counts())
```

:::color5
**<font style="color:#601BDE;">3.数据完整性</font>**

:::

**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：数据完整性指的是数据中是否存在缺失值或不完整记录，确保数据能够支持完整的模型训练和推理。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">缺失值检测</font>**<font style="color:rgb(51, 51, 51);">：识别数据中的缺失值分布情况。</font>
+ **<font style="color:rgb(51, 51, 51);">字段完整性检查</font>**<font style="color:rgb(51, 51, 51);">：确保所有字段都有有效值。</font>
+ **<font style="color:rgb(51, 51, 51);">数据记录完整性</font>**<font style="color:rgb(51, 51, 51);">：确保每条记录都包含所有必要信息。</font>

:::color5
**<font style="color:#601BDE;">4.数据与任务的适合性</font>**

:::

<font style="color:rgb(51, 51, 51);">数据与任务的适合性指的是数据是否适合用于预定的模型训练和预测任务，确保数据与模型目标一致。</font>

**<font style="color:rgb(51, 51, 51);">评价指标</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">相关性分析</font>**<font style="color:rgb(51, 51, 51);">：评估数据中特征与目标变量的相关性。</font>
+ **<font style="color:rgb(51, 51, 51);">领域适应性</font>**<font style="color:rgb(51, 51, 51);">：确保数据分布与目标任务的领域一致。</font>
+ **<font style="color:rgb(51, 51, 51);">任务可行性</font>**<font style="color:rgb(51, 51, 51);">：评估数据是否能够支持模型完成预定任务。</font>

```python
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def assess_data_task_alignment(dataset, target_column, feature_columns):
    # 绘制目标变量与其他特征的相关性热图
    sns.heatmap(dataset[feature_columns + [target_column]].corr(), 
                cmap='coolwarm', annot=True)
    plt.title('Correlation Heatmap between Features and Target')
    plt.show()
    
    # 使用随机森林计算特征与目标的互信息
    if target_column is not None:
        print("\nMutual Information between Features and Target:")
        mutual_info = mutual_info_classif(dataset[feature_columns], dataset[target_column])
        for feat, mi in zip(feature_columns, mutual_info):
            print(f"{feat}: {mi:.3f}")
    
    # 示例：训练简单模型评估数据适合性
    if target_column is not None:
        X_train, X_test, y_train, y_test = train_test_split(
            dataset[feature_columns], dataset[target_column], test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred):.3f}")
```



