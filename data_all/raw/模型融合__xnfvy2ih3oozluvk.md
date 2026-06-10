# 模型融合

<!-- source: yuque://zhongxian-iiot9/hlyypb/xnfvy2ih3oozluvk -->

:::success
**<font style="color:#000000;">背景</font>**<font style="color:#000000;">：</font><font style="color:#000000;">开源LLM世界百花齐放，除了通用</font>[<font style="color:#000000;">Base模型</font>](https://zhida.zhihu.com/search?content_id=238594256&content_type=Article&match_order=1&q=Base%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:#000000;">、</font>[<font style="color:#000000;">SFT模型</font>](https://zhida.zhihu.com/search?content_id=238594256&content_type=Article&match_order=1&q=SFT%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:#000000;">之外，另有一类</font>**<font style="color:#74B602;">融合模型（merged model）</font>**<font style="color:#74B602;"> </font><font style="color:#000000;">常出现在各类榜单的top位置。Model Merging能取得近似于</font>`[<font style="color:#000000;background-color:rgb(248, 248, 250);">multi-task learning</font>](https://zhida.zhihu.com/search?content_id=238594256&content_type=Article&match_order=1&q=multi-task+learning&zhida_source=entity)`<font style="color:#000000;">的效果，即融合模型能够</font>**<font style="color:#74B602;">同时“学会”</font>**<font style="color:#000000;">多种任务，也可能取得更好的in-domain performance、更好的</font>[<font style="color:#000000;">out-of-distribution generalization</font>](https://zhida.zhihu.com/search?content_id=238594256&content_type=Article&match_order=1&q=out-of-distribution+generalization&zhida_source=entity)<font style="color:#000000;">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977082497-dfec81f9-5ccf-44e6-a94a-ff62d946be15.png)

:::color3
**简介：**[<font style="color:#000000;">模型融合</font>](https://zhida.zhihu.com/search?content_id=238594256&content_type=Article&match_order=1&q=%E6%A8%A1%E5%9E%8B%E8%9E%8D%E5%90%88&zhida_source=entity)<font style="color:#000000;">（model merging）指：</font>**<font style="color:#ED740C;">将多个SFT模型在参数粒度上进行合并，得到一个融合模型</font>**<font style="color:#000000;">。</font><font style="color:rgb(25, 27, 31);">Model Merging在LLM时代也是合时宜的技术，因为它：</font>

1. **<font style="color:rgb(25, 27, 31);">无需训练</font>**<font style="color:rgb(25, 27, 31);">：节省了大量的机器成本、时间成本；</font>
2. **<font style="color:rgb(25, 27, 31);">只需模型参数，而无需训练数据</font>**<font style="color:rgb(25, 27, 31);">：规避了数据隐私问题。</font>

<font style="color:rgb(25, 27, 31);">本文将从三个角度进行总结：</font>**<font style="color:rgb(25, 27, 31);">模型融合靠谱吗？有哪些常见技术？该技术的特性是什么？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

+ **Task Arithmetic：**[**https://arxiv.org/pdf/2212.04089**](https://arxiv.org/pdf/2212.04089)
+ **FIsher Averaging：**[**https://arxiv.org/pdf/2111.09832**](https://arxiv.org/pdf/2111.09832)
+ **RegMean：**[**https://openreview.net/pdf?id=FCnohuR6AnM**](https://openreview.net/pdf?id=FCnohuR6AnM)
+ **TIES-Merging：**[**https://arxiv.org/pdf/2306.01708**](https://arxiv.org/pdf/2306.01708)

:::

**FIsher Averaging**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977036098-4c29ed8c-ca47-4dcd-8662-8342e2753b55.png)

**Task Arithmetic**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763976857129-17f10d3f-ea5f-4110-9520-bf0c2208953b.png)

**RegMean**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977110879-5fa0d68b-a909-4c55-a053-063012992781.png)

**TIES-Merging**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977120403-1f1cb633-93da-4909-b714-a2507d230e58.png)





## **<font style="color:rgb(25, 27, 31);">模型融合理论依据</font>**
:::color5
**<font style="color:#601BDE;">1.Delta Parameters的冗余性</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **Delta Parameters****<font style="color:rgb(15, 17, 21);">定义</font>**<font style="color:rgb(15, 17, 21);">：指模型在进行监督微调前后，参数值的变化量。  
</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">Δ参数 = 参数_SFT后 - 参数_SFT前</font>`
+ **<font style="color:rgb(15, 17, 21);">直观理解</font>**<font style="color:rgb(15, 17, 21);">：Δ参数封装了模型为学习特定任务而更新的“知识增量”。可以将其视为模型在预训练“通才”基础上，打上的一个针对特定能力的“补丁”。</font>

> <font style="color:rgb(15, 17, 21);">DARE (</font>**<font style="color:rgb(15, 17, 21);">D</font>**<font style="color:rgb(15, 17, 21);">rop </font>**<font style="color:rgb(15, 17, 21);">A</font>**<font style="color:rgb(15, 17, 21);">nd </font>**<font style="color:rgb(15, 17, 21);">RE</font>**<font style="color:rgb(15, 17, 21);">scale) 是一种用于模型参数稀疏化的技术，灵感来源于经典的 </font>**<font style="color:rgb(15, 17, 21);">Dropout</font>**<font style="color:rgb(15, 17, 21);"> 方法。</font>
>
>     - **<font style="color:rgb(15, 17, 21);">提出论文</font>**<font style="color:rgb(15, 17, 21);">：</font>_<font style="color:rgb(15, 17, 21);">《Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch》</font>_<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">[1]</font>
>     - **<font style="color:rgb(15, 17, 21);">核心目的</font>**<font style="color:rgb(15, 17, 21);">：通过对Δ参数进行大幅稀疏化，为后续的</font>**<font style="color:rgb(15, 17, 21);">模型合并</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">步骤做准备，以提升合并效果。</font>
>     - **<font style="color:rgb(15, 17, 21);">操作流程</font>**<font style="color:rgb(15, 17, 21);">：</font>
>         1. **<font style="color:rgb(15, 17, 21);">随机丢弃</font>**<font style="color:rgb(15, 17, 21);">：以一个极高的比率随机选择一部分Δ参数，并将其</font>**<font style="color:rgb(15, 17, 21);">置为0</font>**<font style="color:rgb(15, 17, 21);">。</font>
>         2. **<font style="color:rgb(15, 17, 21);">重新缩放</font>**<font style="color:rgb(15, 17, 21);">：对剩余未被丢弃的Δ参数进行</font>**<font style="color:rgb(15, 17, 21);">放大</font>**<font style="color:rgb(15, 17, 21);">，即除以</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">(1 - drop_rate)</font>`<font style="color:rgb(15, 17, 21);">。</font>
>     - **<font style="color:rgb(15, 17, 21);">设计原理</font>**<font style="color:rgb(15, 17, 21);">：通过缩放保持输出的期望值大致不变，从而确保模型性能不出现严重衰退。</font>
>

+ **<font style="color:rgb(15, 17, 21);">冗余性</font>**<font style="color:rgb(15, 17, 21);">：</font>
    - <font style="color:rgb(15, 17, 21);">实验表明，即使</font>**<font style="color:rgb(15, 17, 21);">丢弃90% - 99%</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">的Δ参数，模型性能与原模型相比依然相差无几。</font>
    - **<font style="color:rgb(15, 17, 21);">模型规模越大</font>**<font style="color:rgb(15, 17, 21);">，其Δ参数的冗余度就越高，可丢弃的比例也越大。</font>
+ **<font style="color:rgb(15, 17, 21);">对模型合并的益处</font>**<font style="color:rgb(15, 17, 21);">：</font>
    - <font style="color:rgb(15, 17, 21);">Δ参数中包含了大量冗余甚至是有害的“噪声”。</font>
    - <font style="color:rgb(15, 17, 21);">在合并模型前，先使用DARE丢弃这些冗余参数，可以显著减少合并时不同模型参数之间的</font>**<font style="color:rgb(15, 17, 21);">干扰</font>**<font style="color:rgb(15, 17, 21);">。</font>
    - <font style="color:rgb(15, 17, 21);">这使得合并后的模型能更稳定地继承来自多个同源模型的能力，</font>**<font style="color:rgb(15, 17, 21);">保障了合并效果</font>**<font style="color:rgb(15, 17, 21);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977414990-84b9f71a-56bc-4cf9-b994-08a6f9fd3a03.png)

:::color5
**<font style="color:#601BDE;">2.Task Vector的正交性</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977868637-b4d9dbdb-e068-4d2a-a6da-2b5cf6537ffe.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977872649-9b23a99e-e21e-428a-b642-39f6575d46b5.png)

**<font style="color:#117CEE;">📘</font>****<font style="color:#117CEE;"> 核心概念：Task Vector (任务向量)</font>**

+ **<font style="color:rgb(15, 17, 21);">定义</font>**<font style="color:rgb(15, 17, 21);">：Task Vector 本质上是模型在特定任务上经过</font>**<font style="color:rgb(15, 17, 21);">全量微调</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">后，其参数相对于原始基座模型的变化量。</font>
+ **<font style="color:rgb(15, 17, 21);">核心公式</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">任务向量 = 模型_微调后 - 模型_基座</font>`
+ **<font style="color:rgb(15, 17, 21);">概念关联</font>**<font style="color:rgb(15, 17, 21);">：此概念与上一节提到的</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">Delta Parameters (Δ参数)</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">是</font>**<font style="color:rgb(15, 17, 21);">等同</font>**<font style="color:rgb(15, 17, 21);">的。</font>
+ **<font style="color:rgb(15, 17, 21);">命名由来</font>**<font style="color:rgb(15, 17, 21);">：这个概念源自论文 </font>_<font style="color:rgb(15, 17, 21);">《Editing Models with Task Arithmetic》</font>_<font style="color:rgb(15, 17, 21);"> 。因为这些参数变化是在特定任务上学习得到的，编码了该任务的“知识”，故被称为 </font>**<font style="color:rgb(15, 17, 21);">Task Vector</font>**<font style="color:rgb(15, 17, 21);">。</font>

**<font style="color:#117CEE;">🔬</font>****<font style="color:#117CEE;"> 关键发现：Task Vector 的正交性</font>**

<font style="color:rgb(15, 17, 21);">论文《Editing Models with Task Arithmetic》对多个不同任务的 Task Vector 进行了分析，得出了一个关键结论：</font>

+ **<font style="color:rgb(15, 17, 21);">低相似度</font>**<font style="color:rgb(15, 17, 21);">：研究发现，</font>**<font style="color:rgb(15, 17, 21);">绝大多数 Task Vector 之间的相似度极低</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">近似正交</font>**<font style="color:rgb(15, 17, 21);">：除了少数在语义上高度关联的任务（例如，两个不同的情感分类任务）之外，大部分 Task Vector 在向量空间中都</font>**<font style="color:rgb(15, 17, 21);">几乎呈现正交关系</font>**<font style="color:rgb(15, 17, 21);">。</font>

**<font style="color:rgb(15, 17, 21);">💡</font>****<font style="color:rgb(15, 17, 21);"> 直观理解</font>**<font style="color:rgb(15, 17, 21);">：这意味着不同任务学到的“知识更新方向”几乎是相互垂直、互不干扰的。一个任务的更新方向不会对另一个任务的更新方向构成直接影响。</font>

**<font style="color:#117CEE;">🛠️</font>****<font style="color:#117CEE;"> 方法应用：参数平均的有效性</font>**

<font style="color:rgb(15, 17, 21);">正是由于上述的</font>**<font style="color:rgb(15, 17, 21);">正交性</font>**<font style="color:rgb(15, 17, 21);">，一个简单而有效的模型融合方法变得可行：</font>

+ **<font style="color:rgb(15, 17, 21);">操作</font>**<font style="color:rgb(15, 17, 21);">：直接将多个任务的 Task Vector 进行</font>**<font style="color:rgb(15, 17, 21);">算术平均</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">效果</font>**<font style="color:rgb(15, 17, 21);">：即使采用这种简单的平均操作，最终得到的融合模型在多个任务上也能取得</font>**<font style="color:rgb(15, 17, 21);">相当不错的效果</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">原理</font>**<font style="color:rgb(15, 17, 21);">：因为向量正交，将它们相加时，它们各自的方向信息得以保留，而不会因为方向冲突而产生严重的</font>**<font style="color:rgb(15, 17, 21);">相互干扰</font>**<font style="color:rgb(15, 17, 21);">。</font>

### **<font style="color:rgb(25, 27, 31);">前提</font>**
<font style="color:rgb(25, 27, 31);">就笔者阅读的论文而言，参数融合有一个必要前提：</font>

**<font style="color:rgb(25, 27, 31);">用于融合的SFT模型必须源自同一个Base模型</font>**<font style="color:rgb(25, 27, 31);">，即其模型结构一致、SFT的initilization一致。</font>

<font style="color:rgb(25, 27, 31);">其背后的原因在于：</font>**<font style="color:rgb(25, 27, 31);">用于合并的</font>**`**<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">delta parameters/task vector</font>**`**<font style="color:rgb(25, 27, 31);">的数值不可过大，否则会明显影响合并效果。</font>**

`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">DARE</font>`<font style="color:rgb(25, 27, 31);">论文中有一个实验：当用于计算</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">delta parameters</font>`<font style="color:rgb(25, 27, 31);">的SFT模型（WizardCoder-Python-13B ）并不源自Base模型（Llama-2-13b）时，其</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">delta parameters</font>`<font style="color:rgb(25, 27, 31);">值</font>**<font style="color:rgb(25, 27, 31);">较大</font>**<font style="color:rgb(25, 27, 31);">（> 0.005），此时</font>**<font style="color:rgb(25, 27, 31);">仅drop 10% 的参数也会导致效果骤降。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763975940305-92b02e50-8365-4cc7-b2ad-3ede4fbf4078.png)

`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Task-Arithmetic</font>`<font style="color:rgb(25, 27, 31);">论文研究了 在FT时采取不同量级的learning rate对合并效果的影响。发现当learning rate较大时，合并效果明显下降。</font>

<font style="color:rgb(25, 27, 31);">这与</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">DARE</font>`<font style="color:rgb(25, 27, 31);">论文的实验异曲同工，均说明</font>**<font style="color:rgb(25, 27, 31);">当</font>**`**<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">delta parameters/task vector</font>**`**<font style="color:rgb(25, 27, 31);">的数值较大时，合并效果是有影响的。</font>**

<font style="color:rgb(25, 27, 31);">至于数值多大算大？</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">DARE</font>`<font style="color:rgb(25, 27, 31);">给出的数字是</font>**<font style="color:rgb(25, 27, 31);">0.005</font>**<font style="color:rgb(25, 27, 31);">，当大多数的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">delta parameter</font>`<font style="color:rgb(25, 27, 31);">小于此值时可进行合并，否则不建议合并。</font>

## 模型融合方法
### **<font style="color:rgb(15, 17, 21);"></font>****<font style="color:rgb(15, 17, 21);">任务定义</font>**
:::color5
**<font style="color:#601BDE;">1.输入</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">n</font>`<font style="color:rgb(15, 17, 21);"> 个经过监督微调的专业模型</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978307128-b7329d02-d3f5-4d0c-8b15-9d900a9aff56.png)
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">1</font>`<font style="color:rgb(15, 17, 21);"> 个基础模型</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978312519-b4fe8a75-aa50-45d0-9bdf-28c5a466f092.png)<font style="color:rgb(15, 17, 21);">。</font>
+ <font style="color:rgb(15, 17, 21);">通过 </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">专业模型参数 - 基础模型参数</font>`<font style="color:rgb(15, 17, 21);">，得到每个专业模型的 </font>**<font style="color:rgb(15, 17, 21);">Delta Parameters</font>**![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978299994-aa57b444-97fc-4236-a9cc-934e8db06e76.png)<font style="color:rgb(15, 17, 21);">。</font>

:::color5
**<font style="color:#601BDE;">2.输出</font>**

:::

+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">1</font>`<font style="color:rgb(15, 17, 21);"> 个融合了多个专业模型能力的统一模型</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978352231-5f0a9624-3abd-46f0-925e-258561c71735.png)<font style="color:rgb(15, 17, 21);">。	</font>

### <font style="color:rgb(15, 17, 21);">Simple Averaging（简单平均）</font>
:::color3
**简介：**<font style="color:rgb(15, 17, 21);">直接对所有专业模型的 Delta Parameters 进行算术平均。</font>

:::

:::color5
**<font style="color:#601BDE;">1.公式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978679556-6852c3c4-a855-4486-8f38-a99f03ce269b.png)

+ **<font style="color:rgb(15, 17, 21);">评价</font>**<font style="color:rgb(15, 17, 21);">：由于 Delta Parameters 的</font>**<font style="color:rgb(15, 17, 21);">冗余性</font>**<font style="color:rgb(15, 17, 21);">和</font>**<font style="color:rgb(15, 17, 21);">正交性</font>**<font style="color:rgb(15, 17, 21);">，此方法在融合少量模型时效果尚可，常被用作</font>**<font style="color:rgb(15, 17, 21);">基线方法</font>**<font style="color:rgb(15, 17, 21);">进行比较。</font>

### <font style="color:rgb(15, 17, 21);">Fisher Averaging（费舍尔平均） </font>
:::color3
**简介：**<font style="color:rgb(15, 17, 21);">在合并时，根据每个参数在不同任务中的</font>**<font style="color:rgb(15, 17, 21);">重要性</font>**<font style="color:rgb(15, 17, 21);">进行加权平均。</font>

**<font style="color:rgb(15, 17, 21);">paper：</font>**[**https://arxiv.org/pdf/2111.09832https://arxiv.org/pdf/2111.09832**](https://arxiv.org/pdf/2111.09832https://arxiv.org/pdf/2111.09832)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978745138-35fe8c92-ed02-450d-9a8a-abc67b038215.png)

> 本文中的融合模式：左：将许多微调的模型合并为一种集成形式。中上：“稳健微调”，将微调后的模型与预训练模型合并，以提高原始预训练任务的性能。右下：将微调模型与“donor”任务合并，类似于中间任务迁移学习。右：将中间任务训练模型与donor模型合并
>

:::color5
**<font style="color:#601BDE;">1.公式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978711404-e55382c6-0a19-4323-9969-23ef2f997955.png)

+ **<font style="color:rgb(15, 17, 21);">关键</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">F_i</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">是</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">Fisher Information Matrix</font>**<font style="color:rgb(15, 17, 21);">，用于衡量任务</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">i</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">中每个参数的重要性，其计算方式为模型在该任务数据上预测分布的梯度方差。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978720345-2f891438-8927-49a2-94f5-8f2ded97a727.png)

### <font style="color:rgb(15, 17, 21);">Task Arithmetic（任务算术） </font>
:::color3
**简介：**<font style="color:rgb(15, 17, 21);">将所有任务的 Delta Parameters 求和后，乘以一个缩放系数，再与基础模型参数相加。</font>

**<font style="color:rgb(15, 17, 21);">paper：</font>**[**https://arxiv.org/pdf/2212.04089**](https://arxiv.org/pdf/2212.04089)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978920624-0983a7f4-ae52-4e14-abbc-93b952ddda0e.png)

> 编辑模型的任务向量和算术运算的说明。（a）通过从微调后的同一模型的权重中减去预训练模型的权重来获得任务向量。（b）否定任务向量会降低任务的性能，而控制任务不会发生实质性变化。（c）将任务向量加在一起可以提高预训练模型在所考虑任务上的性能。（d）当任务在两个不同的数据源上形成类似关系，如监督和无监督学习时，可以仅使用目标和数据集的其余三种组合中的向量来提高监督目标任务的性能。
>

:::color5
**<font style="color:#601BDE;">1.公式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763978901232-dc7a53a3-d3fc-4d27-8fbb-ba045ee98ff4.png)

+ **<font style="color:rgb(15, 17, 21);">缩放系数</font>****<font style="color:rgb(15, 17, 21);"> </font>**`**<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">λ</font>**`<font style="color:rgb(15, 17, 21);">：</font>
    - <font style="color:rgb(15, 17, 21);">通常从验证集上挑选得出。</font>
    - <font style="color:rgb(15, 17, 21);">经验表明，</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">λ</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">在</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">0.3 - 0.5</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">之间效果通常较好。若无验证集，可直接在此范围内选取。</font>

### <font style="color:rgb(15, 17, 21);">RegMean（正则化均值） </font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">针对linear layer的融合，其思想是：</font>**<font style="color:rgb(25, 27, 31);">合并后的模型输出要与合并前的模型输出尽可能接近</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(15, 17, 21);">paper：</font>**[**https://openreview.net/pdf?id=FCnohuR6AnM**](https://openreview.net/pdf?id=FCnohuR6AnM)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977110879-5fa0d68b-a909-4c55-a053-063012992781.png)

> Simple、Fisher和RegMean在合并基于转换器的语言模型方面的比较。Fisher和RegMean需要Fisher信息矩阵或层输入的内积矩阵，但它们都不需要训练数据。对于线性模型，RegMean可以生成最小化的最优权重ℓ 2-与相应训练集上的单个模型预测的距离。
>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(15, 17, 21);">应用范围</font>**<font style="color:rgb(15, 17, 21);">：主要针对</font>**<font style="color:rgb(15, 17, 21);">线性层</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">目标函数</font>**<font style="color:rgb(15, 17, 21);">：最小化融合模型与所有专业模型在输出上的差异。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763979026979-88ffa833-2d4d-40e1-924d-c14fec513251.png)

+ **<font style="color:rgb(15, 17, 21);">闭式解</font>**<font style="color:rgb(15, 17, 21);">：对于线性层，该优化问题有直接的解析解。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763979048255-d75e2942-e67a-4119-973e-9062bfb97b51.png)

+ **<font style="color:rgb(15, 17, 21);">融合策略</font>**<font style="color:rgb(15, 17, 21);">：</font>
    1. <font style="color:rgb(15, 17, 21);">对</font>**<font style="color:rgb(15, 17, 21);">线性层</font>**<font style="color:rgb(15, 17, 21);">，使用 RegMean 方法进行融合。</font>
    2. <font style="color:rgb(15, 17, 21);">对</font>**<font style="color:rgb(15, 17, 21);">非线性层</font>**<font style="color:rgb(15, 17, 21);">，则使用 Simple Averaging 方法进行融合。</font>

### <font style="color:rgb(15, 17, 21);">TIES-Merging（消除干扰的合并方法） </font>
:::color3
**简介：****<font style="color:rgb(15, 17, 21);">核心目标</font>**<font style="color:rgb(15, 17, 21);">：解决模型融合中的两类</font>**<font style="color:rgb(15, 17, 21);">干扰</font>**<font style="color:rgb(15, 17, 21);">：</font>

    1. **<font style="color:rgb(15, 17, 21);">冗余参数干扰</font>**<font style="color:rgb(15, 17, 21);">：大量不重要的参数像噪声一样影响融合。</font>
    2. **<font style="color:rgb(15, 17, 21);">符号冲突干扰</font>**<font style="color:rgb(15, 17, 21);">：不同任务的参数更新方向（正负号）相反，相互抵消，导致性能下降。</font>

**<font style="color:rgb(15, 17, 21);">paper：</font>**[**https://arxiv.org/pdf/2306.01708**](https://arxiv.org/pdf/2306.01708)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763977120403-1f1cb633-93da-4909-b714-a2507d230e58.png)

> TIES-MERGING中涉及的步骤。我们将模型中的每个参数可视化为一个正方形。箭头描绘了通过微调不同任务（用颜色编码）产生的参数的更新（任务向量，τ），方向表示符号，长度表示幅度。我们首先根据任务向量值的大小对其进行修剪，然后通过解决符号冲突来为每个参数（γm，包含+1或-1的绿色向量）选择符号。最后，我们只选择与选定符号对齐的值，并将其均值作为最终参数值。
>

:::color5
**<font style="color:#601BDE;">1.核心步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(15, 17, 21);">修剪</font>**<font style="color:rgb(15, 17, 21);">：对于每个待合并模型，仅保留</font>**<font style="color:rgb(15, 17, 21);">幅度最大的前20%</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">的参数，其余置零，以消除冗余干扰。</font>
2. **<font style="color:rgb(15, 17, 21);">选举</font>**<font style="color:rgb(15, 17, 21);">：对于每个参数，将所有模型的参数符号（+1, -1）视为“投票”，计算每个符号方向的参数幅度总和，选择</font>**<font style="color:rgb(15, 17, 21);">幅度总和最大的符号</font>**<font style="color:rgb(15, 17, 21);">作为该参数的最终符号，以解决符号冲突。</font>
3. **<font style="color:rgb(15, 17, 21);">分离合并</font>**<font style="color:rgb(15, 17, 21);">：对于每个参数，仅保留那些符号与“当选符号”一致的模型参数值，然后对这些非零值进行</font>**<font style="color:rgb(15, 17, 21);">直接平均</font>**<font style="color:rgb(15, 17, 21);">。</font>

**<font style="color:rgb(15, 17, 21);">最终公式</font>**<font style="color:rgb(15, 17, 21);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763979142196-3e1a4d52-c4ea-4c56-8d56-11ef3bb6c799.png)

+ **<font style="color:rgb(15, 17, 21);">亮点</font>**<font style="color:rgb(15, 17, 21);">：实验发现，若能获知“真实”的合并符号，TIES 的效果可逼近多任务学习，说明“选举”步骤仍有巨大优化潜力。</font>





