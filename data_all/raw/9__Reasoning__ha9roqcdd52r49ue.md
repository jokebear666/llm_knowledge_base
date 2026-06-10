# 9️⃣ Reasoning

<!-- source: yuque://zhongxian-iiot9/hlyypb/ha9roqcdd52r49ue -->

# Reasoning<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**背景：**<font style="color:rgb(25, 27, 31);">自从OpenAI发布o1模型后，让我们体验到LLM在复杂问题的推理能力上的进步。Reasoning Model（推理模型）的复现之路也成为各家大模型追捧的热点。在猜想和复现的过程中，试图从OpenAI、Google、微软的近期的研究中找到一些蛛丝马迹，其中主流的一些猜测集中在使用PRM和MCTS方法，在Post-training和Inference阶段提升推理性能。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**Reasoning，指的就是类似福尔摩斯的那种推理，**<font style="color:#ED740C;">对已知信息进行逻辑演绎或综合，进而推导出新的知识或结论的过程</font>**。它是人类智力活动的核心，也是许多高价值应用(如医学诊断、法律决策、科学研究等）的必须环节。如果一个**<font style="color:#117CEE;"> LLM只会「复制粘贴」或利用大规模统计粗略地「拼凑」答案，那么它很难真正为人类复杂决策或创新活动提供帮助。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**什么是 LLM 推理（Reasoning）？**](https://www.zhihu.com/question/12292274612)** **[**Reasoning Model的精巧实现**](https://zhuanlan.zhihu.com/p/20356958978)

:::

**<font style="color:rgb(25, 27, 31);">大模型发展4阶段</font>**<font style="color:rgb(25, 27, 31);">：阶段 1-3 是常见的 LLM 开发流程，阶段 4 则是面向特定用例的专业化。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742798766423-fdb532e5-333a-4de3-b167-4758388af1fa.png)

:::color5
**<font style="color:#601BDE;">1.Reasoning和Memory的区别</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

人们在使用 LLMs 时，往往会遇到「它看上去懂很多事实，但又常常犯低级错误」。这通常与LLMs 的内部表征方式有关：LLMs 更多是通过**<font style="color:#74B602;">海量参数记住了许多词语间的相关性</font>**，然而对于需要**<font style="color:#117CEE;">「多步逻辑演绎」或「严格计算」的任务时，纯粹基于相关性检索的信息往往不够</font>**。它们可能提供- 个表面看来「像是对的」答案，但在深层逻辑或数值正确性方面会出现偏差。这种现象在学术领域常被称为**<font style="color:#74B602;">「幻觉」 (Hallucination）</font>**：模型生成了看似合理但却与事实相违背的内容。

因此，在大规模记忆的基础上，设计更多增强逻辑推理的机制（如**<font style="color:#74B602;">提示工程、外部工具调用、符号方法结合</font>**等）是近两年研究的热点。接下来，我们将从不同方向展开讨论，介绍多种提升 LLM推理能力的思路和方法。

:::color5
**<font style="color:#601BDE;">2.Reasoning的主要类别</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **演绎推理 (Deductive Reasoning)**：根据一般性原则推导出具体结论。如果前提为真，则结论必定为真。例如数学定理证明。
+ **归纳推理 (Inductive Reasoning)**：根据若干具体样例推断普适规律。机器学习的很多过程其实就是归纳推理，例如从训练样本中学习回归或分类模型。
+ **溯因推理 (Abductive Reasoning)**：在一些不充分或部分信息的条件下，尝试寻找「最有可能」的解释。这在医学诊断或故障排查等场景非常常见。
+ **常识推理 (Commonsense Reasoning）**：依赖日常的世界知识和逻辑，使模型能够像人一样根据背景常识进行判断。例如「冬天在户外等公交，需要穿衣保暖」。
+ **概率推理 (Probabilistic Reasoning)**：允许引入不确定性，用概率分布或概率图模型等方式来推理。例如，在风险评估、金融预测中往往需要带有概率意义的结果。

## 流派一：提示词工程 prompting<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>在不改变模型结构、也不进行额外大型训练的情况下，通过改进输入提示 (prompts)可以在一定<font style="color:rgb(51, 51, 51);">程度上激发或引1导 LLM 产生更好的推理结果。以下介绍几种常见方法。</font>

:::

:::color5
**<font style="color:#601BDE;">1.COT 思维连</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Chain-of-Thought (CoT)是一种简单但有效的提示工程策略，即鼓励模型在回答过程中「**<font style="color:#74B602;">显式」地写出思考或推导的中间步骤</font>**。与传统直接输出结论不同，CoT 会让LLM 逐步生成一条「推理链」，从问题出发，分阶段拆解直到得出答案。例如：

```plain
问题：一个篮子里有12个鸡蛋，打碎了3个，煮了5个，还剩几个？
思考：首先12-3=9个完整鸡蛋，然后煮了5个不代表拿走，所以还剩9个．
答案：9个
```

实验证明，CoT 在**<font style="color:#74B602;">数学、逻辑等需要多步分析的任务中往往能显著降低错误率</font>**，让模型的回答更具「可解释性」。不过，CoT 并不能保证所有步骤都正确，如果模型本身对某个领域缺乏足够知识，或者提示设计不佳，它依然会在中途「想错并写错」。

:::color5
**<font style="color:#601BDE;">2.Self-Consistency 多线程思考</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

为了避免单条思维链中的随机性和局部错误，Self-Consistency 方法会让模型针对**<font style="color:#74B602;">同一问题生成多条思维链</font>**，并最终对这些结论进行**<font style="color:#74B602;">「投票」或「聚合」</font>**，挑选出现频率最高或最被支持的结论。它的基本假设是，如果 LM 在若干次独立的推理中都得出相同的答案，那么这个结论很可能是正确的。Self-Consistency 可以被视作一种**<font style="color:#74B602;">「多重思考＋大家表决」的机制</font>**。举例：

```plain
问题：28+47=？
解法A：20+40=60， 8+7=15，总和75
解法B：28+40=68，再加7得75
解法C：30+47=77，减2得75
根据表决，最终答案75
```

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">TOT : Tree of Thought</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">相比CoT 通常是一条</font>**<font style="color:#74B602;">线性推理链</font>**<font style="color:rgb(51, 51, 51);">，Tree-of-Thought(ToT） 则让模型可以从</font>**<font style="color:#74B602;">某一步分叉出多种可能，再通过评价或搜索策略对枝干进行拓展和修剪</font>**<font style="color:rgb(51, 51, 51);">。这样，一次推理</font>**<font style="color:#74B602;">不再只有唯一的路径</font>**<font style="color:rgb(51, 51, 51);">，而是形成一个「推理树」，有助于在面临复杂的决策或搜索问题时，不断尝试</font>**<font style="color:#74B602;">不同思路并选择最优解</font>**<font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">用一个游戏举例：</font>**

+ <font style="color:rgb(51, 51, 51);">目标：在4步之内，通过一系列操作，使数字变为 24</font>
+ <font style="color:rgb(51, 51, 51);">初始状态：数字1。</font>
+ <font style="color:rgb(51, 51, 51);">操作：只能进行加法或乘法，每次只能加或乘以2或3。</font>

<font style="color:rgb(51, 51, 51);">TOT 的构造大致如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742786159435-bd8e4079-7fe3-4c33-a981-59d4c37406c5.png)

1. <font style="color:rgb(51, 51, 51);">分解：将问题分解为一系列决策步骤（每一步选择加或乘哪个数）。</font>
2. <font style="color:rgb(51, 51, 51);">拓展：在每一步．根据当前状态，拓展出所有可能的下一步状态（生成子节点)。</font>
3. <font style="color:rgb(51, 51, 51);">评估：评估每个状态的潜力（给节点评分）。比如，在第一层时，3似乎更有潜力接近 24(因为可以乘以8，虽然不能直接乘，但是可以作为目标)，给3较高的评分。</font>
4. <font style="color:rgb(51, 51, 51);">选择：根据评估结果，选择最有潜力的状态进行下一步拓展(选择节点)。</font>
5. <font style="color:rgb(51, 51, 51);">搜索：通过不断重复拓展、评估和选择的过程，最终找到目标解。</font>

:::color5
**<font style="color:#601BDE;">4.Program-Aided Language Models (PAL)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">PAL 方法让语言模型在推理时可以</font>**<font style="color:#74B602;">调用额外的计算资源或者外部程序</font>**<font style="color:rgb(51, 51, 51);">，比如执行 Python 脚本来做复杂的数值计算，或调用数学软件进行公式推导。通过这种方式，LLM 不必自己在内部参数中「模拟」所有的数学操作，而是把关键步骤</font>**<font style="color:#74B602;">交给更可靠的工具来执行</font>**<font style="color:rgb(51, 51, 51);">，一定程度上提高了系统的准确度和可验证性。</font>

**<font style="color:rgb(51, 51, 51);">举例：求解物理问题</font>**

<font style="color:rgb(51, 51, 51);">假设我们有一个物理问题：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

```plain
一个质量为 m=2kg 的物体，以 v=5m/s 的初速度在水平地面上运动，受到一个与运动方向相反的摩擦力f = 0.5N。求物体经过多长时间停止运动？
```

<font style="color:rgb(51, 51, 51);">使用 PAL 方法解决该问题的步骤如下：</font>

1. <font style="color:rgb(51, 51, 51);">步骤1： LLM 理解问题井生成代码：</font>
    - <font style="color:rgb(51, 51, 51);">LLM 首先理解题意，识别出需要使用物理公式来求解。</font>
    - <font style="color:rgb(51, 51, 51);">然后，LLM 生成一段Python 代码，用于计算物体停止运动的时间。</font>

```python
import sympy
＃ 定义符号变量
m,vQ ,f , t =sympy.symbols('m vo f t'）
                           
＃ 根据牛顿第二定律，摩擦力等于质量乘以加速度
a =-f/m

# 根据匀变速直线运动公式，末速度 v= VO + a*t
v = V0+a*t

＃ 当V=0时，物体停止运动，解方程求时间t
equation = sympy.Eq(v,0)

＃将m， v0，f的值代入方程
equation = equation.subs((m: 2, v0: 5, f: 0.5})
                         
＃ 解方程
t _value = sympy.solve(equation, t)[0]

＃ 打印结果
print (t value)
```

2. <font style="color:rgb(51, 51, 51);">步骤2：执行代码：</font><font style="color:#D22D8D;">（by草莓师姐）</font>
    - <font style="color:rgb(51, 51, 51);">PAL将LLM生成的 Python 代码发送给 Python 解释器执行</font>
    - <font style="color:rgb(51, 51, 51);">Python 解释器使用 sympy 库进行符号计算，解出方程，得到时间 t_value = 20</font>
3. <font style="color:rgb(51, 51, 51);">步骤 3： LLM组织答案：</font><font style="color:#D22D8D;">（by草莓师姐）</font>
    - <font style="color:rgb(51, 51, 51);">LLM接收到 pvthon 程序的计算结果 (t=20)。</font>
    - <font style="color:rgb(51, 51, 51);">然后，LLM 将结果组织成自然语言答案：</font>

```python
物体经过 20 秒停止运动。
```

## 流派二：模型结构改进<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：这类方法主要关注如何在模型的内部构造或工作机制上进行改进，核心理念在于：对模型结构本身进行修饰、扩展或重组，使其在推理时能够获得新的信息通道、知识表示方式或逻辑演绎途径，从而在推理能力和可解释性等方面得到提升。</font>

:::

:::color5
**<font style="color:#601BDE;">1.检索增强生成（RAG）：添加知识库与检索模块</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

其实 RAG严格意义上来说是不改变「基模型」的结构的，但我们把它分到这个流派里，是因为我们在这里把整个 AI系统看做一个整体，不只包含「基模型」。

RAG 思想是让语言模型在回答问题前，**<font style="color:#74B602;">先从外部知识库（如向量数据库、文本资料库）中检索到与问题相关的信息，再将检索到的资料与原始问题拼接后输入模型进行生成</font>**。这样LLM 就不必完全依赖其内部隐性记忆，也能更好地根据「事实」进行推理，减少胡乱编造答案的风险。

常见的检索手段包括基于稠密向量的检索（Dense Retrieval）、BM25等关键词检索算法。通过RAG，模型可以显著缓解幻觉问题，尤其在需要引用外部资料的任务里更显优势。

:::color5
**<font style="color:#601BDE;">2.神经-符号混合（Neuro-Symbolic*）：结合规则引擎</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

传统符号 AI 擅长基于逻辑规则或知识库进行可解释、可验证的推理，但在处理海量、模糊的自然语言数据方面略显笨拙；而神经网络擅长从大规模数据中提取分布式表示，却缺乏稳定的逻辑演绎本领。为此，研究者提出Neuro-Symbolic 混合模型，将两者结合：

+ 模型前端由神经网络处理自然语言的解析、语义抽取或表征；
+ 模型后端使用符号推理引擎（如**<font style="color:#74B602;">逻辑规则、知识图谱</font>**）对抽取的信息进行进一步的严格演绎或验证。

通过这种混合方式，可在保持模型灵活处理非结构化文本能力的同时，引入符号系统的高可解释性与严格性。

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">添加记忆模块（Memory-Augmented Neural Networks*</font>****<font style="color:#601BDE;">, MANNs)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">大多数LLM 只有隐含在参数中的记忆，</font>**<font style="color:#74B602;">而MANNs允许模型显式访问一个可读写的外部存储，像「笔记本」一样记下中间推理结论或中间状态。</font>**<font style="color:rgb(51, 51, 51);">在推理多步时，模型可以随时查询、更新这份长期记忆，以确保上下文连贯。这种做法在减少重复计算、保持长程依赖上具备潜力，也能部分缓解LLM 对长文本上下文的处理难题。</font>

:::color5
**<font style="color:#601BDE;">4.图神经网络(GNN)与知识图谱</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

当需要显式地对实体及其关系进行建模，如任务涉及多跳问答、知识推理等需求时，**<font style="color:#74B602;">将LLM 和知识图谱（Knowledge Graph）相结合是一条可行的思路。知识图谱把事实存储成一系列实体和关系</font>**，图神经网络（Graph Neural Networks,GNNs）则能对图结构进行逐层融通，帮助判断多跳推理路径。这在法学、金融、医学等高度结构化领域具有明显优势。

这种方法有时候也可以纳入上面介绍的 Neuro-Symbolic结合的思想范畴，可以发展为「先用神经网络对图进行表征，再使用符号引擎进行规则推理」的混合系统。但是否真属于这个范畴，要看实际系统有没有确实结合了符号逻辑推理。没有显式符号推理时，它就只是一个基于图结构的神经网络方法。

:::color5
**<font style="color:#601BDE;">5.工具与 API 调用</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

和上面介绍的 PAL思路上是一致的，不过概念更泛化。**<font style="color:#74B602;">指的是让LLM「学会」如何调用外部工具（如搜索引擎、计算 API、数据库接口等）以获得额外的准确信息或功能支持</font>**。通过把「如何使用工具」包含在上下文或内置策略中，LLM 就可以「决定」在推理过程中何时、如何去检索更多资料或进行计算。研究也表明，当LLM 对外部工具拥有恰当的访问和理解能力时，它们的任务成功率、可靠性和迭代效率都会显著提升。

**<font style="color:#74B602;">PAL 被归类为「Prompt-based 推理增强」，因为它本质上主要依赖 Prompt 的设计</font>**（告诉模型：现在你需要输出一段程序），模型不需要对自身结构或训练流程进行大规模修改就可以实现「程序辅助的推理」。而「工具与 API调用」被归到「通过模型结构或推理架构改进」的范畴，因为它往往需要在推理过程中进行更灵活而复杂的「调用一返回」协同，不仅仅是把输出当文字生成，而是需要系统级别的「功能对接」和「一来一回的交互」，因而对模型或推理系统的整体管线要做更多改装。

## 流派三：学习范式改进<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：这类方法并不是围绕模型/系统的「结构」动手脚，而是从</font>**<font style="color:#ED740C;">训练和学习流程上进行改进。核心理念是：不大幅改变已有的大型语言模型结构，而是调整或新设计训练/学习方法</font>**<font style="color:rgb(51, 51, 51);">，让模型在已有框架下学到更好的推理模式，提高推理可靠性与泛化能力。</font>

:::

:::color5
**<font style="color:#601BDE;">1.有监督微调（SFT）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

通过在特定的推理数据集上进行有监督微调，能让模型更精确地掌握某类推理任务。常用的推理数据集包括：

+  **GSM8K**：中小学数学题集。
+  **MATH**：涵盖高中及竞赛数学题，考察较高难度的数学推理。
+  **LogiQA**：考察抽象的逻辑推理与阅读理解能力。
+  **ARC**：覆盖若干领域的常识与推断题。
+  **HotpotQA**：需要多跳推理的阅读理解任务。

如果数据质量高且包含足够多的推理示例，模型在该领域的推理能力会显著增强。不过，这也带来泛化性、跨领域迁移等问题。

:::color5
**<font style="color:#601BDE;">2.人类反馈强化学习（RLHF）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

核心流程通常包括：

1.  使用语言模型生成回答；
2.  人类标注者对回答进行评分或排序；
3.  训练一个「奖励模型」（Reward Model）来模拟人类对回答优劣的判断；
4.  用 PPO等强化学习算法，让模型在每次生成回答后，根据「奖励」进行参数更新，倾向输出更符合人类需求和逻辑的内容。

比如，让LLM 输出一个解答数学竞赛题的过程，人类对解答步骤中连贯性及最终正确性进行打分，如果错误就给低分。模型最终会学习到如何在解题的关键步骤保持逻辑连贯。

:::color5
**<font style="color:#601BDE;">3.自监督学习（SSL） 与对比学习（CL）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

自监督学习（Self-Supervised Learning, SSL）和对比学习（Contrastive Learning, CL）同样为推理增强提供了新思路：

+ **自监督**：模型可以在海量无标注文本中自行构造「伪任务」（比如预测下一句、填空、生成合理的推理步骤等），从中积累对逻辑结构的感知。
+ **对比学习**：鼓励模型分辨「有效推理链」和「无效推理链」的差异，通过「拉近正确推理示例，推远错误推理示例」的方式，帮助模型形成更一致、更明确的逻辑表征。  
典型的对比学习会用如 InfoNCE 等损失函数：

:::color1
**<font style="color:rgb(51, 51, 51);">InfoNCE</font>**<font style="color:rgb(51, 51, 51);">：是一种基于噪声对比估计的损失函数，用于最大化正样本对的互信息（Mutual Information）。其公式为：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740712765539-f4f8df7c-e753-44e7-af4b-4d48c28958fc.png)

+ _<font style="color:rgb(51, 51, 51);">z</font>_<sub>_<font style="color:rgb(51, 51, 51);">i</font>_</sub><font style="color:rgb(51, 51, 51);">：锚点样本（anchor）的特征。</font>
+ <font style="color:rgb(51, 51, 51);">z</font><sub><font style="color:rgb(51, 51, 51);">j</font></sub><sup><font style="color:rgb(51, 51, 51);">+</font></sup><font style="color:rgb(51, 51, 51);">：正样本的特征。</font>
+ <font style="color:rgb(51, 51, 51);">z</font><sub><font style="color:rgb(51, 51, 51);">k</font></sub><sup><font style="color:rgb(51, 51, 51);">−</font></sup><font style="color:rgb(51, 51, 51);">：负样本的特征。</font>
+ <font style="color:rgb(51, 51, 51);">s(⋅)：相似度函数（如余弦相似度）。</font>
+ <font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：温度系数（控制分布尖锐程度）。</font>
+ <font style="color:rgb(51, 51, 51);">N：负样本数量。</font>

:::

:::color5
**<font style="color:#601BDE;">4.自动验证器与判别模型(Critic Models)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

有些研究会在主模型之外，再训练一个**<font style="color:#74B602;">「审查/批判模型」来检查主模型的推理步骤</font>**，一旦发现不合理之处，就提出警示或要求修正，进而将这类评价结果反馈到训练或推断过程中，实现对主模型推理质量的改进，从这个角度讲，也可以看做RLAIF 方法。通常表现为：

+  有一个主模型（或者说「生成模型」）进行推理、回答。
+  有一个次级模型（或者说「批判模型」或「验证器」）对主模型的理由链、过程正确性或最终输出进行打分或判断。
+  以此打分或判断为依据来改进主模型：比如过滤掉错误推理，或通过强化学习的方式更新主模型  
参数等。

近期常见的 PRM/ORM 或类似的<font style="color:#74B602;">多级 reward 机制</font>，通常就是「自动验证器与批判模型」在实践中的一个具体实现。它们都为主模型生成的过程或结果提供一种「外部批判/评价」，从而帮助主模型提升推理一致性、正确性或安全性。

**PRM (Process Reward Model)**<font style="color:#D22D8D;">（by草莓师姐）</font>

+  PRM 的目标是给**<font style="color:#74B602;">「推理过程」本身打分（reward）</font>**，比如给每一步的思路链、Chain-of-Thought 提供一个质量评价。
+  这意味着它更关注推理展开的细节：**<font style="color:#74B602;">是否逻辑连贯、中间步骤有没有硬伤</font>**等。
+  这种过程级评估非常符合「批判模型」或「验证器」的角色—它不仅看最终答案对不对，更会审查一系列中间步骤的合理性。

**ORM (Output Reward Model)**<font style="color:#D22D8D;">（by草莓师姐）</font>

+  ORM 则主要打分**<font style="color:#74B602;">「最终输出」（最后的答案或结论）的质量</font>**。
+  与 PRM 相比，ORM只看结果是否正确、合乎人类偏好或任务标准，而不深入逐步过程。
+  这种单一关注输出的评估模式，也可视为一种更「精简」的批判模型—它仍然在对主模型的推理结论进行审核。

另外，若结合外部符号推理器进行正式验证，还可以将数学推理或逻辑证明转化为可机读的公式化、形式化的形式，进而用定理证明器进行检验，保证结论正确。不过，目前公式化、形式化的验证仅能涵盖少数对逻辑一致性要求极高的任务，对日常复杂语言仍有难度。

## Reasoning评估<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：如何客观地检测 LLMs在推理方面的有效性也是研究的一大难点。人们通常会使用一系列基准数据集（benchmark）进行测试。</font>

:::

:::color5
**<font style="color:#601BDE;">1.基准数据集（benchmark）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **ARC** （AI2 Reasoning Challenge）：主要考察常识及跨学科推理的能力。
2. **LogiQA**：专门评估逻辑推断题。
3.  **GSM8K、MATH**： 数学类推理数据集，考察算术与高阶数学技能。
4.  **HotpotQA**：多跳问答，要求模型在多个文档之间进行推断。
5.  **HumanEval**：测试模型在编程任务中的推理与代码生成正确度。
6. **ANLI**：对抗式自然语言推理数据集，检测模型对「刁钻对抗样例」的抗干扰能力。

在评测指标上，除了传统的准确率（Accuracy）、F1分数之外，人们也越来越关注推理过程是否可解释、可验证，以及在面对对抗攻击或未知领域时能否保持鲁棒性和泛化能力。



# Reasoning 方法
## Self-Consistency
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">假设每个复杂的问题都可以有多种思路来推到出最终的答案</font>**<font style="color:rgb(25, 27, 31);">，这篇文章就是</font>**<font style="color:rgb(25, 27, 31);">探索是否可以用这种思想来提高大模型复杂问题的推理能力</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(25, 27, 31);">对人类来说，不同人思考问题的方式不一样，同样的问题，可以利用多种思路来解决。而当前大语言模型来解决复杂推理问题时，例如COT + LLM的方法主要采用一种贪婪解码（Greedy Decoding）【在每个时间步选择概率最高的词作为输出】的方式来实现。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">提出了一种新的decoding解码策略【self-consistency（自一致性）】，以替代思想链（COT）+ LLM使用的贪婪解码（Greedy Decoding）方法。</font>**<font style="color:rgb(25, 27, 31);">总结成一句话就是首先利用COT生成多个推理路径和答案，最终选择答案出现最多的作为最终答案输出，效果出奇的好。</font>**

**paper：**[**https://arxiv.org/pdf/2203.11171**](https://arxiv.org/pdf/2203.11171)

**参考：**[**https://zhuanlan.zhihu.com/p/641370746**](https://zhuanlan.zhihu.com/p/641370746)

:::

**<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：Self-Consistency 是一种提升大语言模型（LLM）推理能力的解码策略，其核心思想是：</font>**<font style="color:rgb(51, 51, 51);">通过多次采样生成不同的推理路径，选择最具一致性的答案作为最终输出</font>**<font style="color:rgb(51, 51, 51);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742883481322-55beef82-52be-408e-b549-3ab0aaa84463.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ <font style="color:rgb(25, 27, 31);">self-consistency解码策略假设复杂推理任务一般可以通过多个推理路径获得正确答案，从解码器中抽样生成多样化的推理路径集合，</font>**<font style="color:#74B602;">选择一致性最高的输出结果作为最终答案，降低了贪婪解码方式的单次采样的随机性</font>**
+ <font style="color:rgb(25, 27, 31);">self-consistency</font>**<font style="color:#74B602;">不需要训练额外训练或者辅助模型</font>**<font style="color:rgb(25, 27, 31);">，类似于在单个语言模型上工作的自集成方法</font>
+ <font style="color:rgb(25, 27, 31);">self-consistency 结合</font>[<font style="color:rgb(9, 64, 142);">PaLM-540B</font>](https://zhida.zhihu.com/search?content_id=223629786&content_type=Article&match_order=1&q=PaLM-540B&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">或</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">GPT-3</font>](https://zhida.zhihu.com/search?content_id=223629786&content_type=Article&match_order=1&q=GPT-3&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，算术推理任务中都获得最新的sota水平，GSM8K(Cobbe 等人，2021 年+17.9% )()、SVAMP(Patel 等人，2021 年+11.0%)、AQuA(Ling 等人，2017 年+12.2%)，以及 StrategyQA 等常识性推理任务(Geva 等人，2021 年+6.4%)和 ARC 挑战(Clark 等人，2018 年+3.9%)</font>
+ <font style="color:rgb(25, 27, 31);">self-consistency 在抽样策略和提示缺陷场景下都具有很强的鲁棒性，在一般NLP任务中也能获得性能提升</font>

:::color5
**<font style="color:#601BDE;">2.核心方法</font>**

:::

+ <font style="color:rgb(25, 27, 31);">Step1: 思维链提示CoT</font>
+ <font style="color:rgb(25, 27, 31);">Step2: 对语言模型进行多次采样, 生成多个推理路径</font>

```python
def generate_paths(prompt, num_samples=10):
    paths = []
    for _ in range(num_samples):
        path = model.generate(
            prompt,
            temperature=0.7,  # 增加多样性
            max_new_tokens=200
        )
        paths.append(extract_answer(path))
    return paths
```

+ <font style="color:rgb(25, 27, 31);">Step3: 对不同推理路径生成结果基于投票策略选择最一致的答案输出</font>
1. **答案归一化**：
    - <font style="color:rgb(51, 51, 51);">数学问题：标准化数字格式（如 "12.0" → 12）</font>
    - <font style="color:rgb(51, 51, 51);">代码生成：AST抽象语法树比对</font>
    - <font style="color:rgb(51, 51, 51);">文本答案：语义相似度计算（如 BERTScore）</font>
2. **投票机制**：

```python
from collections import defaultdict

def majority_vote(answers):
    counter = defaultdict(int)
    for ans in answers:
        norm_ans = normalize(ans)
        counter[norm_ans] += 1
    return max(counter.items(), key=lambda x: x[1])[0]
```

:::color5
**<font style="color:#601BDE;">3.采样策略</font>**

:::

+ <font style="color:rgb(25, 27, 31);">UL2-20B and LaMDA-137B， T = 0.5， top-k (k = 40) tokens</font>
+ <font style="color:rgb(25, 27, 31);">PaLM-540B we applied T = 0.7, k = 40</font>
+ <font style="color:rgb(25, 27, 31);">GPT-3，T = 0.7，without top-k</font>

:::color5
**<font style="color:#601BDE;">4.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">提升复杂任务准确率（GSM8K +5.2%）</font>
+ <font style="color:rgb(51, 51, 51);">缓解模型幻觉问题</font>
+ <font style="color:rgb(51, 51, 51);">降低单次生成随机性影响</font>

**<font style="color:rgb(51, 51, 51);">局限</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算成本增加（生成次数 × 单次推理时间）</font>
+ <font style="color:rgb(51, 51, 51);">多数答案可能集体错误</font>
+ <font style="color:rgb(51, 51, 51);">答案归一化存在挑战</font>

:::color5
**<font style="color:#601BDE;">5.应用场景</font>**

:::

| **场景** | **案例** | **效果提升** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">数学推理</font> | <font style="color:rgb(51, 51, 51);">GSM8K、MATH 数据集</font> | <font style="color:rgb(51, 51, 51);">+3%~12%</font> |
| <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">HumanEval、MBPP 基准</font> | <font style="color:rgb(51, 51, 51);">+7%~15%</font> |
| <font style="color:rgb(51, 51, 51);">常识推理</font> | <font style="color:rgb(51, 51, 51);">StrategyQA、ARC-Challenge</font> | <font style="color:rgb(51, 51, 51);">+5%~8%</font> |
| <font style="color:rgb(51, 51, 51);">科学计算</font> | <font style="color:rgb(51, 51, 51);">SciBench、PhysiNet</font> | <font style="color:rgb(51, 51, 51);">+10%~18%</font> |


:::color5
**<font style="color:#601BDE;">6.评估</font>**

:::

<font style="color:rgb(25, 27, 31);">Self-consistency 在算术推理, 常识推理，符号推理中都表现高于一般的Cot效果，在ood的数据上[Letter(4)、Coinflip(4)]仍然保持效果增益</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742883818530-515ab015-6780-47aa-b6d5-b3d96fabb702.png)

:::color5
**<font style="color:#601BDE;">7.代码实现</font>**

:::

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from collections import defaultdict

class SelfConsistencyGenerator:
    def __init__(self, model_name="gpt2-large"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
    
    def normalize_answer(self, text):
        # 实现答案标准化逻辑
        return text.strip().lower()
    
    def generate_answers(self, prompt, num_samples=10):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        answers = []
        
        with torch.no_grad():
            for _ in range(num_samples):
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=200,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                answers.append(self.normalize_answer(answer))
        
        return answers
    
    def get_consensus(self, answers):
        counts = defaultdict(int)
        for ans in answers:
            counts[ans] += 1
        return max(counts, key=counts.get)

# 使用示例
generator = SelfConsistencyGenerator()
prompt = "Q: 如果一个箱子里有5个红球和3个蓝球，随机抽取2个，都是红球的概率是多少？"
answers = generator.generate_answers(prompt, num_samples=20)
final_answer = generator.get_consensus(answers)
print(f"Consensus Answer: {final_answer}")

```



## STaR
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">STaR旨在解决如何提高语言模型在复杂推理任务上的性能，例如数学问题解答或常识问答。STaR（Self-Taught Reasoner）算法的原理是通过迭代地利用少量推理示例（rationales）和大量没有推理的大数据集，来引导模型逐步提升执行更复杂推理的能力。STaR算法的核心是一个简单的循环过程。</font>

**paper：**[**STaR: Self-Taught Reasoner Bootstrapping Reasoning With Reasoning**](https://arxiv.org/pdf/2203.14465)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058832190-3fe2056a-2c4d-41bf-b16e-603f95cfae05.png)

:::color5
**<font style="color:#601BDE;">1.STaR步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058931163-f7d26519-849a-45b0-aaed-a33cc528406c.png)

:::color5
**<font style="color:#601BDE;">2.评估</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">算术（Arithmetic）</font>**<font style="color:rgb(25, 27, 31);">：验证模型在解决不同位数的加法问题上的性能。STaR显著提高了模型在多位数加法问题上的准确率。特别是引入合理化（rationalization）步骤后，模型的性能提升更为显著。</font>
2. **<font style="color:rgb(25, 27, 31);">常识推理（Commonsense Reasoning）</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">CommonsenseQA</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=CommonsenseQA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（CQA）数据集，评估模型在多项选择常识问题上的表现。在CommonsenseQA数据集上，STaR在开发集上的准确率超过了仅使用少量样本提示的基线（增加了35.9%），并且与直接预测答案的基线相比也有显著提升（增加了12.5%）。当与比STaR模型大30倍的模型相比时，STaR的性能与之相当（72.5% vs 73.0%）。</font>
3. **<font style="color:rgb(25, 27, 31);">小学数学（Grade School Math）</font>**<font style="color:rgb(25, 27, 31);">：利用</font>[<font style="color:rgb(9, 64, 142);">GSM8K</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=GSM8K&zhida_source=entity)<font style="color:rgb(25, 27, 31);">数据集，测试模型解决自然语言表述的数学问题的能力。STaR显著提高了模型在GSM8K数据集上的性能，即使训练数据较少（无合理化的模型使用了25.0%的数据，合理化的模型使用了28.7%的数据）。</font>



# Reasoning应用
## Code Reasoning 代码生成（Deepseek）<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**

+ 在常见的代码任务（如代码生成与补全、代码解释与理解、常见编程知识回答）之外，code reasoning任务（**<font style="color:#ED740C;">给定input预测output or 给定output预测input</font>**）也是一个能提升LLM性能的重要方向。这个任务更考验模型的推理能力，需要模型**<font style="color:#ED740C;">按照代码的运行逻辑，一步步推导出结果，相当于用自然语言的形式将代码的逻辑执行一遍。</font>**
+ 使用多轮纠错机制，可以产生更好地response，从而构造出更好的SFT数据。<font style="color:#D22D8D;">（by草莓师姐）</font>

**paper：**[**https://arxiv.org/pdf/2502.07316**](https://arxiv.org/pdf/2502.07316)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742797930516-de2d1e81-d258-418f-8da7-647592e3a2f6.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

当前reasoning相关的任务，存在如下的问题：

1. 主要聚焦于数学或代码生成等特定领域，**<font style="color:#117CEE;">其他推理领域因训练数据稀疏难</font>**以提升性能。
2. 尽管真实世界的代码程序蕴含丰富多样的推理模式，是理想的训练数据来源，但原始代码中的推理信号往往隐含且与噪声信息交织，直接在NL2Code任务上训练，**<font style="color:#117CEE;">会受代码特定语法要求的限制，难以泛化到其他非代码特定任务。</font>**

为此，本文提出了[CodeI/O](https://zhida.zhihu.com/search?content_id=713727407&content_type=Answer&match_order=1&q=CodeI%2FO&zhida_source=entity)方法。将原始代码文件转换为可执行函数，设计input-output预测任务，让模型用自然语言推理预测输入或输出。这样做的好处是，可以提高代码任务的推理能力并泛化到其它的任务中去，同时不受特定语法的限制。

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **收集原始代码文件**：从多个不同侧重点的来源收集原始代码文件，如 CodeMix（从内部代码预训练语料库中筛选的 Python 代码文件）、PyEdu - R（Python - Edu 中聚焦复杂推理任务的子集），还纳入了来自算法库、数学问题集和在线编码平台的高质量代码文件，总共合并得到约** 810.5K **代码文件。
+ **转换为统一格式**：利用 [DeepSeek - V2.5](https://zhida.zhihu.com/search?content_id=713727407&content_type=Answer&match_order=1&q=DeepSeek+-+V2.5&zhida_source=entity) 对收集到的原始代码文件进行预处理，**<font style="color:#74B602;">将其转换为统一格式</font>**。具体包括提取核心逻辑功能为函数，去除非必要元素（如可视化和文件处理相关代码）；添加主入口函数，明确输入输出要求并确保其可 JSON 序列化；创建基于规则的 Python 输入生成器函数；生成简洁的问题描述作为查询。
+ **收集输入和输出对**：针对转换后的函数，使用输入生成器采样多个输入，并执行代码获取相应输出。执行过程中跳过包含随机性的函数，对运行时和输入 / 输出对象的复杂度进行限制。经过筛选，最终从 454.9K 原始代码文件中获得 **3.5M** 实例，输入和输出预测实例分布大致平衡。
+ **构建输入 - 输出预测样本**：将收集到的输入 - 输出对和转换后的函数组装成可训练格式。对于每个训练样本，构建包含**<font style="color:#74B602;">函数、查询、参考代码和特定输入或输出的提示，响应则为用自然语言描述的推理过程（CoT）。</font>**

:::color5
**<font style="color:#601BDE;">3.CoT构建方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **直接提示（CODEI/O）**：由于从代码生成确定性反向函数用于输入预测不切实际，且自动构建的轨迹受模板限制缺乏自然语言推理的表达性和泛化性，因此采用基于大语言模型的方法，**<font style="color:#74B602;">使用 DeepSeek - V2.5 合成所有期望的响应，由此生成的数据集称为 CODEI/O</font>**。
+ **充分利用代码（**[**CODEI/O++**](https://zhida.zhihu.com/search?content_id=713727407&content_type=Answer&match_order=1&q=CODEI%2FO%2B%2B&zhida_source=entity)**）**：针对 CODEI/O 中部分预测错误的响应，采用重新执行代码获取反馈的方式，将反馈作为第二轮输入消息，让 DeepSeek - V2.5 重新生成响应。最后将第一轮响应、第一轮反馈、第二轮响应和第二轮反馈连接起来构建最终响应，得到数据集 CODEI/O++。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742798033784-791c4a8c-eefb-40bf-a92c-2babf45b3626.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **第一阶段：CODEI/O (++) 数据集训练**：使用构建的 CODEI/O 或 CODEI/O++ 数据集对模型进行训练。**<font style="color:#74B602;">这些数据集通过收集多种来源的原始代码文件，转换为统一格式并生成大量输入 - 输出对及相应自然语言思维链（CoT）构建而成</font>**。训练过程中，让模型学习**<font style="color:#74B602;">预测代码的输入或输出</font>**，以自然语言 CoT 作为推理依据，从而接触到逻辑流规划、状态空间搜索等通用推理原语，增强模型的基础推理能力。此阶段的训练为模型后续的指令调优奠定了坚实的推理基础。
2. **第二阶段：通用指令调优**：在完成第一阶段训练后，使用包含约 **<font style="color:#74B602;">1.18M 样本的内部指令调优数据集对模型进行训练。该数据集涵盖多种语言和广泛领域，如数学、编码、写作等。</font>**通过在这个数据集上的调优，使模型能够有效遵循多样化的指令，提升模型在下游任务中的适用性和表现，将模型转变为一个通用的指令跟随模型。

采用两阶段训练的原因：CODEI/O (++) 数据集样本数量远多于指令调优数据，若直接混合训练，会导致数据分布偏差，使模型在指令调优数据上学习不充分，影响其在下游任务中执行多样化指令的能力。**<font style="color:#74B602;">而两阶段训练先强化模型的推理能力，再进行指令调优，能避免这种问题，充分发挥两个数据集的作用，提升模型的综合性能。</font>**

:::color5
**<font style="color:#601BDE;">5.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

论文通过多组实验，对比不同训练数据和模型在多个基准测试中的表现，验证了 CODEI/O 和 CODEI/O++ 的有效性。主要实验结果如下：**<font style="color:#74B602;">在涵盖科学、数学、符号、常识、逻辑和代码理解等多领域的 14 个基准测试中，CODEI/O 均实现了性能提升</font>**，超越了单阶段基线以及其他数据基线，包括 [WebInstruct](https://zhida.zhihu.com/search?content_id=713727407&content_type=Answer&match_order=1&q=WebInstruct&zhida_source=entity)、[OpenMathInstruct2](https://zhida.zhihu.com/search?content_id=713727407&content_type=Answer&match_order=1&q=OpenMathInstruct2&zhida_source=entity) 等。

从下表其实可以看到两个基本结论：

1. CODEI/O 在几乎所有基准测试中都呈现出稳定的性能改进，而非仅在部分任务上提升。这表明它在提升代码推理任务性能的同时，**<font style="color:#74B602;">对其他非代码相关的推理任务也有显著帮助</font>**，表明该方法具有良好的泛化能力。
2. 在所有测试的基础模型上，CODEI/O++ 系统性地超越了 CODEI/O，进一步提高了平均得分，且没有在个别任务上出现性能折损的情况。这表明**<font style="color:#74B602;">基于执行反馈的多轮修订能够有效提高数据质量，增强模型在不同领域的推理能力。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742798262584-ea0e4ae0-75cf-42d6-8c1e-89dd35b84eb0.png)



# Reasoning模型
## 字节Seed Thinking v1.5<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">在大型语言模型上进行大规模强化学习的推动下，推理模型领域取得了显著进展。其中，</font>[<font style="color:rgb(9, 64, 142);">OpenAI</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=OpenAI&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的</font>**<font style="color:rgb(25, 27, 31);">o1</font>**<font style="color:rgb(25, 27, 31);">系列、DeepSeek的</font>**<font style="color:rgb(25, 27, 31);">R1</font>**<font style="color:rgb(25, 27, 31);">、Google的</font>**<font style="color:rgb(25, 27, 31);">Gemini 2.5</font>**<font style="color:rgb(25, 27, 31);">和</font>[<font style="color:rgb(9, 64, 142);">Anthropic</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=Anthropic&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的</font>**<font style="color:rgb(25, 27, 31);">Claude 3.7</font>**<font style="color:rgb(25, 27, 31);">等模型已成为当前最先进的技术代表，它们在逻辑推理、数学问题解决和代码生成方面均实现了重大突破。这些进展标志着推理模型正朝着更结构化、高效和可扩展的方向发展，当前研究重点集中在提高训练效率、优化长思维链和完善大规模强化学习技术。本篇论文介绍了一种新型推理模型</font>**<font style="color:rgb(25, 27, 31);">Seed-Thinking-v1.5</font>**<font style="color:rgb(25, 27, 31);">，该模型在推理和非推理任务中均表现卓越。</font>

:::

:::color3
**简介：****<font style="color:rgb(25, 27, 31);">Seed-Thinking-v1.5 </font>**<font style="color:rgb(25, 27, 31);">的</font>[<font style="color:rgb(9, 64, 142);">混合专家</font>](https://zhida.zhihu.com/search?content_id=256253769&content_type=Article&match_order=1&q=%E6%B7%B7%E5%90%88%E4%B8%93%E5%AE%B6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（MoE）模型，</font>**<font style="color:rgb(25, 27, 31);">参数总量达 200B、激活参数 20B</font>**<font style="color:rgb(25, 27, 31);">。核心思路在于</font>**<font style="color:rgb(25, 27, 31);">利用基于长链式思考（</font>**[**<font style="color:rgb(9, 64, 142);">CoT</font>**](https://zhida.zhihu.com/search?content_id=256253769&content_type=Article&match_order=1&q=CoT&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）的强化学习框架</font>**<font style="color:rgb(25, 27, 31);">（含稳定的 RL 训练算法和高精度的自动化验证器），</font>**<font style="color:rgb(25, 27, 31);">在数学、编程和通用逻辑推理等任务上取得了显著提升</font>**<font style="color:rgb(25, 27, 31);">。论文在新提出的 BeyondAIME 和 Codeforces 基准上进行了测试，Seed-Thinking-v1.5 分别达到 48.0% 和 55.0% 的成绩，并在其他推理和非推理任务（如 GPQA、人文问答等）也有大幅度提升。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">其主要贡献包括：</font>

**<font style="color:rgb(25, 27, 31);">• 组合“可验证”与“不可验证”两类数据，基于</font>****<font style="color:rgb(25, 27, 31);"> </font>**[**<font style="color:rgb(9, 64, 142);">RLHF</font>**](https://zhida.zhihu.com/search?content_id=256253769&content_type=Article&match_order=1&q=RLHF&zhida_source=entity)**<font style="color:rgb(25, 27, 31);"> </font>****<font style="color:rgb(25, 27, 31);">统一训练；</font>**

**<font style="color:rgb(25, 27, 31);">• 提出 Seed-Thinking-Verifier，用于自动判断推理回答正确与否；</font>**

**<font style="color:rgb(25, 27, 31);">• 通过</font>****<font style="color:rgb(25, 27, 31);"> </font>**[**<font style="color:rgb(9, 64, 142);">VAPO</font>**](https://zhida.zhihu.com/search?content_id=256253769&content_type=Article&match_order=1&q=VAPO&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">/DAPO 等新算法解决大型模型在推理强化学习时的不稳定性；</font>**

**<font style="color:rgb(25, 27, 31);">• 自主开发高效的分布式训练与推理基础设施（SRS 与混合并行等），显著提升训练效率。</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744700283604-d0fe766a-79c2-413e-8c30-d432cf7d12af.png)

:::color5
**<font style="color:#601BDE;">1.能力对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">数学推理</font>**<font style="color:rgb(25, 27, 31);">：在数学竞赛方面，Seed-Thinking-v1.5在</font>[<font style="color:rgb(9, 64, 142);">AIME 2024</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=AIME+2024&zhida_source=entity)<font style="color:rgb(25, 27, 31);">测试中获得86.7分的成绩，与o3-mini-high表现相当，并显著优于o1和</font>[<font style="color:rgb(9, 64, 142);">DeepSeek R1</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=DeepSeek+R1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，展示了强大的竞争力。由于AIME 2024已无法提供足够的区分度，研究团队构建了更具挑战性的评估集</font>[<font style="color:rgb(9, 64, 142);">BeyondAIME</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=BeyondAIME&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。BeyondAIME中的所有问题均由人类专家新近设计，旨在最大限度减少通过记忆或猜测解决的可能性。尽管Seed-Thinking-v1.5的表现超过了o1和R1，但与o3和Gemini pro 2.5相比仍存在性能差距。这一结果进一步证明了新评估集具有良好的区分能力。</font>

**<font style="color:rgb(25, 27, 31);">竞争性编程</font>**<font style="color:rgb(25, 27, 31);">：在评估竞争性编程能力时，研究团队采用</font>[<font style="color:rgb(9, 64, 142);">Codeforces</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=Codeforces&zhida_source=entity)<font style="color:rgb(25, 27, 31);">作为基准测试。不同于一些基于Elo评分系统的先前研究（Elo系统包含估计因素且难以直接比较），本研究基于最近12个Codeforces比赛制定了具体的评估方案。具体而言，评估采用pass@1和pass@8两项指标，其中pass@k表示模型能否在k次尝试内成功解决问题（即从k个生成的提交结果中选择最佳解答）。研究团队选择报告pass@8指标是因为其结果更加稳定，且更接近实际用户的提交模式。Seed-Thinking-v1.5在这两项指标上均优于DeepSeek R1，尽管与o3相比仍有一定差距。该评估集将在未来版本中公开发布。</font>

**<font style="color:rgb(25, 27, 31);">科学</font>**<font style="color:rgb(25, 27, 31);">：Seed-Thinking-v1.5在</font>[<font style="color:rgb(9, 64, 142);">GPQA</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=GPQA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">测试中获得77.3分，接近o3级别的表现。值得注意的是，这一性能提升主要源于</font>**<font style="color:#74B602;">数学训练带来的泛化能力提升</font>**<font style="color:rgb(25, 27, 31);">，而非特定科学领域数据量的增加。</font>

**<font style="color:rgb(25, 27, 31);">非推理任务</font>**<font style="color:rgb(25, 27, 31);">：对于非推理任务，研究团队使用模拟现实世界用户需求的测试集对Seed-Thinking-v1.5进行评估。通过针对DeepSeek R1在多种场景下的人类评估，结果显示Seed-Thinking-v1.5取得了显著进步：用户正面反馈整体提升了8.0%，凸显了该模型在处理复杂用户场景方面的增强能力。</font>

<font style="color:rgb(25, 27, 31);">高质量推理模型的开发主要涉及三个关键方面：</font>**<font style="color:rgb(25, 27, 31);">训练数据</font>**<font style="color:rgb(25, 27, 31);">、</font>[**<font style="color:rgb(9, 64, 142);">RL算法</font>**](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=RL%E7%AE%97%E6%B3%95&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>[**<font style="color:rgb(9, 64, 142);">RL基础设施</font>**](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=RL%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。研究团队在这三个领域投入了大量精力，下面将详细讨论。</font>

:::color5
**<font style="color:#601BDE;">2.SFT数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在</font>[<font style="color:rgb(9, 64, 142);">SFT训练</font>](https://zhida.zhihu.com/search?content_id=256328886&content_type=Article&match_order=1&q=SFT%E8%AE%AD%E7%BB%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);">方面，与传统后训练数据不同，推理模型依赖于</font>**<font style="color:rgb(25, 27, 31);">思维链(CoT)</font>**<font style="color:rgb(25, 27, 31);">数据，这类数据明确展示了逐步推理过程。初步实验表明，过量的非CoT SFT数据会显著降低模型的探索能力。</font>

:::color5
**<font style="color:#601BDE;">3.RL数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在RL训练中，研究团队整合了</font>**<font style="color:#74B602;">四类数据：STEM问题、代码相关任务、逻辑推理和创意写作、对话等非推理数据</font>**<font style="color:rgb(25, 27, 31);">。其中，逻辑推理数据对提升ARC-AGI基准测试的性能贡献显著，而数学数据则展现出强大的泛化能力，能够带来跨任务的全面性能提升。</font>

<font style="color:rgb(25, 27, 31);">Seed-Thinking-v1.5的RL训练数据主要分为两部分：具有</font>**<font style="color:#74B602;">确定答案的可验证问题和无确定答案的不可验证问题</font>**<font style="color:rgb(25, 27, 31);">。模型的核心推理能力主要通过第一部分培养，并能有效泛化至第二部分应用场景。</font>

1. **<font style="color:rgb(25, 27, 31);">可验证问题</font>**

<font style="color:rgb(25, 27, 31);">可验证问题主要包含三类：</font>**<font style="color:#74B602;">带标准答案的STEM问题</font>**<font style="color:#74B602;">、</font>**<font style="color:#74B602;">配备单元测试的编程问题</font>**<font style="color:#74B602;">，以及</font>**<font style="color:#74B602;">可自动验证的逻辑推理题</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">STEM数据</font>**

<font style="color:rgb(25, 27, 31);">研究团队构建的数据集包含数十万个高质量竞赛级题目，涵盖数学、物理和化学领域，其中数学问题占比超过80%。这些问题来源多样，包括开源数据集、国内外公共竞赛资源以及专有收集的题库。</font>

<font style="color:rgb(25, 27, 31);">数据清洗过程中，首先剔除了表述不完整、符号不一致或要求不明确的问题。对于保留下来的问题，研究团队使用Doubao-Pro 1.5模型生成多个解答。</font>**<font style="color:#74B602;">当模型在最差样本评估(woN)中得分为1的问题被视为过于简单而被剔除。</font>**

<font style="color:rgb(25, 27, 31);">此外，针对参考答案可能存在错误的情况，研究团队采用了</font>**<font style="color:#74B602;">最先进的推理模型为每个问题生成多个候选答案。如果模型生成的答案与参考答案不一致，但这些生成答案之间具有高度一致性，或者仅涉及极少量的推理token，则认为参考答案可能有误。这类问题会交由人类专家进行手动验证</font>**<font style="color:rgb(25, 27, 31);">，确保最终参考答案的准确性。研究团队还应用了数据增强技术优化学习评估效果。具体措施包括：将多选题转换为填空或简答形式，以消除猜测因素并更精准评估推理能力；修改部分数学问题使答案尽可能为整数。</font>

**<font style="color:#74B602;">经过全面的数据清洗和增强处理，最终获得了10万个STEM问题的训练集</font>**<font style="color:rgb(25, 27, 31);">。在训练阶段，使用基于模型的Seed-Verifier评估答案正确性。</font>

+ **<font style="color:rgb(25, 27, 31);">代码数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">在编程问题方面，研究团队优先选择高质量且具挑战性的算法任务，主要来自知名编程竞赛平台。</font>

<font style="color:rgb(25, 27, 31);">数据筛选</font>**<font style="color:#74B602;">确保每个问题均包含完整规范：清晰的问题描述、完整的单元测试集和检查器脚本。其中单元测试用于验证解决方案的功能正确性，检查器脚本则强制执行输出格式和边界情况等额外约束</font>**<font style="color:rgb(25, 27, 31);">。团队还进行了难度筛选，确保问题复杂度适当且能应用于实际算法推理场景。</font>

<font style="color:rgb(25, 27, 31);">在评估方面，最准确的方法是将生成代码提交至官方平台验证。然而，强化学习过程中实时提交不具可行性。因此，研究团队开发了</font>**<font style="color:#74B602;">离线评估集用于高效本地验证</font>**<font style="color:rgb(25, 27, 31);">。观察结果表明，离线评估与官方判定结果高度相关。所有训练和评估问题均集成到内部代码沙盒环境中，支持模型生成代码的直接执行与评估。团队确保沙盒环境稳定且具高吞吐量，为RL训练提供持续准确的反馈。</font>

+ **<font style="color:rgb(25, 27, 31);">逻辑谜题数据</font>**

<font style="color:rgb(25, 27, 31);">逻辑推理数据包含24点计算、迷宫解决、数独等22种常见研究任务。研究团队为</font>**<font style="color:#74B602;">每种任务构建了专用数据生成器和答案验证器。数据生成器能自动产生大量训练和评估数据</font>**<font style="color:rgb(25, 27, 31);">，且对多数任务可配置难度级别。在训练过程中，基于模型在特定任务上的表现动态调整训练数据难度。答案验证器严格评估生成结果的正确性，并可无缝集成到RL流程作为奖励函数。为RL训练共生成约1万个逻辑谜题。</font>

2. **<font style="color:rgb(25, 27, 31);">不可验证问题</font>**

<font style="color:rgb(25, 27, 31);">不可验证问题主要包括需基于人类偏好进行质量评估的非推理任务，如创意内容生成、语言翻译、知识问答和角色扮演等。这些提示词源自Doubao-1.5 Pro的RL训练数据集，涵盖多样化领域。</font>

<font style="color:rgb(25, 27, 31);">研究团队剔除了样本分数方差低和难度低的数据。具体而言，</font>**<font style="color:#74B602;">使用SFT模型为每个提示词生成多个候选回答，然后通过奖励模型评分</font>**<font style="color:rgb(25, 27, 31);">。低分数方差的提示词被剔除，因为这类数据展现有限的采样多样性和改进潜力。</font>

<font style="color:rgb(25, 27, 31);">此外，若某提示词在Doubao 1.5 Pro RL训练过程中奖励分数提升超过特定阈值，该提示词也会被剔除，因为这类数据可能过于简单或在数据集中已有充分表示。实验验证表明，过度优化此类样本会导致模型探索空间提前收缩并降低整体性能。</font>

<font style="color:rgb(25, 27, 31);">对于不可验证数据，研究团队采用成对奖励方法进行评分和RL训练。通过比较两个样本的相对质量，帮助模型更好理解用户偏好，从而提升生成内容的质量和多样性。</font>

:::color5
**<font style="color:#601BDE;">4.奖励建模</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">奖励建模作为RL的核心组件，定义了策略优化的目标函数。因此，精心设计的奖励机制对于在训练阶段为模型响应提供准确可靠的奖励信号至关重要。研究团队针对可验证问题和不可验证问题分别采用了不同的奖励建模方法。</font>

1. **<font style="color:rgb(25, 27, 31);">可验证问题的奖励建模</font>**

<font style="color:rgb(25, 27, 31);">研究团队基于明确原则和思维轨迹，利用LLM对各种场景中的可验证问题进行判断。这种方法提供了更具泛化能力的解决方案，突破了传统基于规则奖励系统的局限性。</font>

<font style="color:rgb(25, 27, 31);">研究团队设计了两种具有进阶关系的奖励建模解决方案：</font>**<font style="color:rgb(25, 27, 31);">Seed-Verifier</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Seed-Thinking-Verifier</font>**<font style="color:rgb(25, 27, 31);">：</font>

+ **<font style="color:rgb(25, 27, 31);">Seed-Verifier：</font>**<font style="color:rgb(25, 27, 31);">基于人类专家精心制定的原则集。该验证器利用LLM的强大基础能力</font>**<font style="color:#74B602;">评估问题、参考答案和模型生成答案三者之间的关系</font>**<font style="color:rgb(25, 27, 31);">。当参考答案与模型生成答案本质等价时返回"</font>_<font style="color:rgb(25, 27, 31);">YES</font>_<font style="color:rgb(25, 27, 31);">"，否则返回"</font>_<font style="color:rgb(25, 27, 31);">NO</font>_<font style="color:rgb(25, 27, 31);">"。这里的等价性并非严格的字面匹配，而是</font>**<font style="color:#74B602;">基于计算规则和数学原理的深层评估，验证两个答案是否表达相同的数学含义</font>**<font style="color:rgb(25, 27, 31);">。这种方法确保奖励信号能准确反映模型响应的本质正确性，即使表述方式不同。</font>
+ **<font style="color:rgb(25, 27, 31);">Seed-Thinking-Verifier：</font>**<font style="color:rgb(25, 27, 31);">借鉴人类判断过程，通过细致思考和深入分析形成结论性判断。研究团队训练了一个</font>**<font style="color:#74B602;">能够提供详细推理路径的验证器</font>**<font style="color:rgb(25, 27, 31);">。具体而言，将此视为可验证任务，与其他数学推理任务一起进行优化。该验证器能够分析参考答案与模型生成答案之间的相似点和差异，提供精确细致的判断结果。</font>

<font style="color:rgb(25, 27, 31);">Seed-Thinking-Verifier显著缓解了Seed-Verifier面临的三个主要问题：</font>

+ **<font style="color:rgb(25, 27, 31);">奖励欺骗</font>**<font style="color:rgb(25, 27, 31);">：非思考型模型可能利用漏洞获取奖励而不真正理解问题。Seed-Thinking-Verifier的详细推理过程使这种欺骗行为更加困难。</font>
+ **<font style="color:rgb(25, 27, 31);">预测不确定性</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#117CEE;">当参考答案与模型生成答案本质等价但格式不同时（如219对比524288），Seed-Verifier可能在不同情况下给出不一致的"</font>**_**<font style="color:#117CEE;">YES</font>**_**<font style="color:#117CEE;">"或"</font>**_**<font style="color:#117CEE;">NO</font>**_**<font style="color:#117CEE;">"判断</font>**<font style="color:rgb(25, 27, 31);">。Seed-Thinking-Verifier通过全面分析答案背后的推理逻辑，提供更一致的结果。</font>
+ **<font style="color:rgb(25, 27, 31);">特殊情况处理失效</font>**<font style="color:rgb(25, 27, 31);">：Seed-Verifier在</font>**<font style="color:#117CEE;">处理某些边界情况时存在困难</font>**<font style="color:rgb(25, 27, 31);">。Seed-Thinking-Verifier凭借提供详细推理的能力，能更有效地应对这些复杂场景。</font>

<u><font style="color:rgb(25, 27, 31);">表1</font></u><font style="color:rgb(25, 27, 31);">展示了两种验证器的性能对比。详细案例分析见原文</font><u><font style="color:rgb(25, 27, 31);">附录A</font></u><font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744701015825-9a7d0fea-6144-40e0-bae4-0c79d42d1ee4.png)

<font style="color:rgb(145, 150, 161);">表1：两种验证器类型的准确率对比。其中，训练集准确率数据来自训练过程统计结果。此外，研究团队手动标注了456个Seed-Verifier无法稳定处理的样本作为测试集，用于全面评估验证器性能。</font>

<font style="color:rgb(25, 27, 31);">结果表明，Seed-Verifier在处理特定情况时效果欠佳，而Seed-Thinking-Verifier展现出提供准确判断的卓越能力。尽管后者的思考过程确实消耗较多GPU资源，</font>**<font style="color:#74B602;">但研究团队认为，其生成的精确稳健的奖励结果对培养模型强大的推理能力至关重要。</font>**

2. **<font style="color:rgb(25, 27, 31);">不可验证问题的奖励建模</font>**

<font style="color:rgb(25, 27, 31);">针对不可验证问题，研究团队训练了专用的RL奖励模型。奖励模型训练数据与Doubao 1.5 Pro中使用的人类偏好数据保持一致，主要涵盖创意写作和内容摘要等类别。</font>

<font style="color:rgb(25, 27, 31);">为提升奖励模型效果，研究团队采用了成对生成式奖励模型的方法，该方法</font>**<font style="color:#74B602;">评估两个答案的相对优劣，并使用输出"YES"或"NO"的概率作为最终奖励分数</font>**<font style="color:rgb(25, 27, 31);">。这种方法使模型能在评分过程中直接比较答案间差异，避免过度关注无关细节。实验结果表明，这种奖励建模方法显著提高了RL训练稳定性，尤其在包含不可验证和可验证问题的混合训练场景中，有效减少了两种不同奖励建模范式之间的冲突。这种改进可能源于成对生成式奖励模型在抑制异常分数生成方面的内在优势，相较于传统奖励模型，能够避免与验证器的分数分布产生显著差异。</font>

:::color5
**<font style="color:#601BDE;">5.SFT训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Seed-Thinking-v1.5的训练过程始于SFT阶段，该阶段为后续强化学习奠定了坚实基础。</font>

<font style="color:rgb(25, 27, 31);">与直接从基础模型开始的强化学习相比，经过SFT的模型能产生更易读的输出，显著减少幻觉内容，并降低有害性。研究团队构建了</font>**<font style="color:#74B602;">包含40万个训练实例的SFT数据集，其中30万个为可验证问题，10万个为不可验证问题</font>**<font style="color:rgb(25, 27, 31);">。可验证问题随机抽取自RL训练集，而不可验证数据则来源于Doubao-Pro 1.5使用的SFT数据，涵盖创意写作、知识问答、安全性和函数调用等多个领域。</font>

<font style="color:rgb(25, 27, 31);">为生成具有长CoT的高质量回应，研究团队采用集成了</font>**<font style="color:#74B602;">模型合成、人类标注和拒绝采样的迭代工作流</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">初始阶段，人类专家通过提示词工程技术或与内部模型的交互对话，生成具有不同推理模式的回应。在积累数十个高质量冷启动样本后，研究团队训练出能够产生长思维链的推理模型，作为更高能力的辅助工具。随后使用Seed-Verifier对该推理模型进行拒绝采样。</font>

<font style="color:rgb(25, 27, 31);">虽然这一工作流程主要应用于数学数据处理，但研究发现它能良好泛化至编程、逻辑谜题甚至创意写作等其他领域。因此，对于这些领域，研究团队同样</font>**<font style="color:#74B602;">执行冷启动流程和拒绝采样，以生成详细的推理轨迹</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">训练过程中，每个实例被截断至32,000个token。研究团队使用上述数据对基础模型进行了两轮微调，采用余弦衰减学习率策略，初始学习率为 </font><font style="color:rgb(25, 27, 31);">2×10−5</font><font style="color:rgb(25, 27, 31);"> ，逐渐降至 </font><font style="color:rgb(25, 27, 31);">2×10−6</font><font style="color:rgb(25, 27, 31);"> 。</font>

:::color5
**<font style="color:#601BDE;">6.RL训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">研究团队开发了一个统一的强化学习框架，该框架能无缝融合来自广泛领域的数据。此集成框架整合了三类数据：</font>

+ **<font style="color:rgb(25, 27, 31);">可验证数据</font>**<font style="color:rgb(25, 27, 31);">：通过验证器获取反馈的数据。此类数据允许根据已知标准直接验证模型输出的正确性。</font>
+ **<font style="color:rgb(25, 27, 31);">一般数据</font>**<font style="color:rgb(25, 27, 31);">：由奖励模型评分的数据。奖励模型基于模型响应与人类偏好的匹配度分配分数。</font>
+ **<font style="color:rgb(25, 27, 31);">混合数据</font>**<font style="color:rgb(25, 27, 31);">：同时结合验证器和奖励模型评分的特定类别数据。这种混合型数据利用了验证式评估和奖励式评估的各自优势。</font>

<font style="color:rgb(25, 27, 31);">在Long-CoT RLHF过程中，研究团队面临</font>**<font style="color:#117CEE;">价值模型偏差和奖励信号稀疏等多重挑战</font>**<font style="color:rgb(25, 27, 31);">。为解决这些问题，团队采用了以下关键技术：</font>

**<font style="color:rgb(25, 27, 31);">价值模型预训练</font>**<font style="color:rgb(25, 27, 31);">：从固定策略(如</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">π</font><font style="color:rgb(25, 27, 31);">sft</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">中采样响应，并使用蒙特卡洛回报更新价值模型。这一过程确保初始化的价值模型与策略</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">π</font><font style="color:rgb(25, 27, 31);">sft</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">完全对齐。保持这种对齐关系对维持模型的思维链模式至关重要，使模型能生成连贯且符合逻辑的思维过程。</font>

**<font style="color:rgb(25, 27, 31);">解耦广义优势估计(Generalized Advantage Estimation, GAE)</font>**<font style="color:rgb(25, 27, 31);">：采用不同的GAE参数(</font><font style="color:rgb(25, 27, 31);">λ</font><font style="color:rgb(25, 27, 31);">value</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">1.0</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);">λ</font><font style="color:rgb(25, 27, 31);">policy</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">0.95</font><font style="color:rgb(25, 27, 31);">)，允许价值模型进行无偏更新，同时策略能独立平衡自身的偏差和方差。这种解耦机制使模型训练更加高效稳定。</font>

**<font style="color:rgb(25, 27, 31);">长度自适应GAE</font>**<font style="color:rgb(25, 27, 31);">：设定</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">λ</font><font style="color:rgb(25, 27, 31);">policy</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">−</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">α</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，其中</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">α</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">为超参数，</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">为响应长度。此方法确保</font>**<font style="color:rgb(25, 27, 31);">时序差分(TD)</font>**<font style="color:rgb(25, 27, 31);">误差在不同长度序列上分布更加均匀，从而使模型在训练中能更有效处理不同长度的序列。</font>

**<font style="color:rgb(25, 27, 31);">动态采样</font>**<font style="color:rgb(25, 27, 31);">：应用动态采样技术并过滤掉精确率为1或0的提示，仅保留批次中具有有效梯度的提示词。这一过程有助于防止训练中梯度信号衰减。</font>

**<font style="color:rgb(25, 27, 31);">上界提升剪裁(Clip-Higher)</font>**<font style="color:rgb(25, 27, 31);">：在</font>**<font style="color:rgb(25, 27, 31);">近端策略优化(PPO)</font>**<font style="color:rgb(25, 27, 31);">算法中，解耦上下剪裁边界如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744705330999-ad0ec27f-06b6-4e61-bce7-c2865692b574.png)

<font style="color:rgb(25, 27, 31);">通过增加</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">ϵ</font><font style="color:rgb(25, 27, 31);">high</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">值，为低概率token的增长创造更大空间，鼓励模型探索更广泛的可能响应，增强发现新颖有效解决方案的能力。</font>

**<font style="color:rgb(25, 27, 31);">Token级损失</font>**<font style="color:rgb(25, 27, 31);">：将策略损失定义在所有token上，而非整体响应。此方法解决了token级对最终损失贡献不平衡问题，确保每个token对训练过程的影响得到适当考量。</font>

**<font style="color:rgb(25, 27, 31);">正例语言模型损失</font>**<font style="color:rgb(25, 27, 31);">：此损失函数旨在提高RL训练过程中正例样本的利用效率。为正例添加系数为</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">μ</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的语言模型损失：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744705330967-5e17c9b0-641d-4fe0-8684-6d0c44ac1dc5.png)

<font style="color:rgb(25, 27, 31);">这一额外损失项帮助模型更好地从正例中学习，提高整体性能。</font>

<font style="color:rgb(25, 27, 31);">在整合不同领域数据并融合多样化评分机制时，研究团队面临不同数据领域间干扰的挑战。这种干扰可能源于难度差异、奖励机制漏洞利用风险及其他潜在因素，导致难以实现模型各能力的均衡同步提升。</font>

<font style="color:rgb(25, 27, 31);">为应对这一问题，团队引入了在线数据分布自适应技术，将强化学习中的静态提示词分布转变为更符合模型训练需求的动态分布。这一方法最小化了数据干扰的负面影响，确保不同能力间更平衡的提升，使模型能在广泛任务中实现更一致的性能提升。</font>

:::color5
**<font style="color:#601BDE;">7.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744705652937-3ad536c1-0fcb-48b1-80ee-87111cb769d1.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744705598931-5d6d6271-2ec8-47b9-8135-d03fc0dc40dc.png)

<font style="color:rgb(25, 27, 31);">结果显示，Seed-Thinking-v1.5相比Deepseek R1获得了8.0%的净胜率，表明其在符合人类偏好方面具有明显优势。这一优势在创意写作到人文知识阐述等多样化场景中表现一致。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744705865584-b59aee13-bca3-451d-af70-a68052dc02e9.png)

:::color5
**<font style="color:#601BDE;">8.总结</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">研究团队开发的Seed-Thinking-v1.5卓越推理模型在推理和非推理任务中均表现出色。该模型利用先进RL技术稳定可靠地提升思考能力，在AIME24、AIME25和Codeforces测试中分别达到86.7%、74.0%和55.0%的优异成绩。</font>

<font style="color:rgb(25, 27, 31);">未来研究方向包括探索更高效的RL训练方案，以及通过思考模式解决更具挑战性的任务，从而拓展模型智能的边界。此外，开发精度可与专用验证器相媲美的通用奖励建模技术也将是一个极具前景的研究方向。</font>



# <font style="color:rgb(1, 1, 1);">多模态-Reasoning模型</font>
## Visual-RFT <font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**视觉强化微调 Visual-RFT (visual reforce finetuning)**

+ <font style="color:rgb(25, 27, 31);">提出 </font>**<font style="color:rgb(25, 27, 31);">Visual-RFT</font>**<font style="color:rgb(25, 27, 31);">：首次将</font>**<font style="color:#ED740C;">基于 </font>**[**<font style="color:#ED740C;">GRPO</font>**](https://zhida.zhihu.com/search?content_id=254647528&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)**<font style="color:#ED740C;"> 的强化学习策略应用于增强 LVLMs 的视觉感知和定位能力</font>**<font style="color:rgb(25, 27, 31);">，解决了数据稀缺场景下的微调问题。</font>
+ <font style="color:rgb(25, 27, 31);">设计</font>**<font style="color:rgb(25, 27, 31);">可验证奖励</font>**<font style="color:rgb(25, 27, 31);">函数：</font>**<font style="color:#ED740C;">为不同视觉任务（如检测、分类）设计了高效的奖励函数</font>**<font style="color:rgb(25, 27, 31);">，简化了奖励计算。</font>
+ <font style="color:rgb(25, 27, 31);">广泛的实验验证：基于</font><font style="color:rgb(25, 27, 31);"> </font>[**<font style="color:rgb(9, 64, 142);">Qwen2-VL-2/7B</font>**](https://zhida.zhihu.com/search?content_id=254647528&content_type=Article&match_order=1&q=Qwen2-VL-2%2F7B&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">在多种视觉任务上验证了 Visual-RFT 的有效性，显著优于 SFT。</font>
+ **<font style="color:rgb(25, 27, 31);">开源</font>**<font style="color:rgb(25, 27, 31);">代码和数据：提供了完整的训练代码、数据集和评估脚本，便于后续研究。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">Visual-RFT首先利用大型视觉语言模型（Large Vision-Language Models, LVLMs）为每个输入生成多个包含推理标记和最终答案的响应，然后通过我们提出的视觉感知可验证奖励函数，结合 </font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（Group Relative Policy Optimization, GRPO）</font>**<font style="color:rgb(25, 27, 31);">等策略优化算法来更新模型。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. <font style="color:rgb(25, 27, 31);">我们引入了 </font>**<font style="color:rgb(25, 27, 31);">视觉强化微调（Visual Reinforcement Fine-Tuning, Visual-RFT）</font>**<font style="color:rgb(25, 27, 31);">，它将带有可验证奖励的强化学习扩展到视觉感知任务，这些任务在</font>**<font style="color:#74B602;">微调数据有限的情况下依然有效</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. <font style="color:rgb(25, 27, 31);">我们</font>**<font style="color:#74B602;">为不同的视觉任务设计了不同的可验证奖励</font>**<font style="color:rgb(25, 27, 31);">，使得奖励计算高效且成本极低。这使得 DeepSeek R1 风格的强化学习能够无缝迁移到 LVLMs。</font>
3. <font style="color:rgb(25, 27, 31);">我们在多种视觉感知任务上进行了广泛的实验，包括</font>**<font style="color:#74B602;">细粒度图像分类、少样本目标检测、推理定位和开放词汇目标检测</font>**<font style="color:rgb(25, 27, 31);">。在所有设置中，Visual-RFT 均取得了显著的性能提升，大幅超越了监督微调基线。</font>
4. <font style="color:rgb(25, 27, 31);">我们在 GitHub 上完全</font>**<font style="color:rgb(25, 27, 31);">开源</font>**<font style="color:rgb(25, 27, 31);">了训练代码、训练数据和评估脚本，以促进进一步的研究。</font>

:::color5
**<font style="color:#601BDE;">2.RFT(强化微调)和SFT的主要区别在于数据</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:rgb(25, 27, 31);">强化微调（RFT）与以往的监督微调（Supervised Fine-Tuning, SFT）的主要区别在于数据效率</font>**<font style="color:rgb(25, 27, 31);">。以往的 SFT 范式直接模仿高质量、精心策划的数据中提供的“真实”答案，因此依赖于大量的训练数据。</font>

<font style="color:rgb(25, 27, 31);">相比之下，RFT 通过评估模型的响应并根据其</font>**<font style="color:#ED740C;">是否正确进行调整，帮助模型通过试错学习</font>**<font style="color:rgb(25, 27, 31);">。因此，</font>**<font style="color:#ED740C;">RFT 特别适用于数据稀缺的领域</font>**<font style="color:rgb(25, 27, 31);">。然而，以往的共识是，RFT 仅应用于科学（例如数学）和代码生成等任务。这是因为数学和编程具有清晰且客观的最终答案或测试用例，使得它们的奖励相对容易验证。在本文中，我们证明了 </font>**<font style="color:#ED740C;">RFT 可以应用于视觉感知任务，而不仅仅是数学和代码领域</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.视觉强化微调</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">视觉强化微调（Visual-RFT）框架。给定问题和视觉图像输入，策略模型生成多个包含推理步骤的响应。随后，使用</font>**<font style="color:rgb(25, 27, 31);">可验证奖励</font>**<font style="color:rgb(25, 27, 31);">（如交并比奖励和分类奖励）结合</font>**<font style="color:rgb(25, 27, 31);">策略梯度优化算法</font>**<font style="color:rgb(25, 27, 31);">来更新策略模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741334693920-bda1b180-762d-494a-ad86-dbd607f8b6a3.png)

**训练步骤**<font style="color:#D22D8D;"> (by草莓师姐)</font>

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
**<font style="color:#601BDE;">4.数据准备</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">为了在各种视觉感知任务上训练 Visual-RFT，我们需要构建多模态训练数据集。与 DeepSeek-R1 类似，为了增强模型的推理能力，并将其应用于提升视觉感知能力，Visual-RFT </font>**<font style="color:#ED740C;">设计了一种提示格式，引导模型在输出最终答案之前</font>****<font style="color:#DF2A3F;">展示其推理过程（think)</font>**<font style="color:rgb(25, 27, 31);">。检测和分类任务中使用的提示格式如表 1 所示。</font>

1. **Detection Prompt**![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335490603-c16cf0e3-8ff4-43a8-bf25-9a0a133c37d1.png)**2. Classification Prompt**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335496202-114105e4-f520-4fa0-985d-5ef63ebdd0e0.png)

:::color5
**<font style="color:#601BDE;">5.效果评估</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">广泛的实验表明，Visual-RFT 在细粒度分类、开放词汇检测、推理定位和少样本学习任务中表现出色。它</font>**<font style="color:rgb(25, 27, 31);">在数据量极少的情况下优于监督微调（SFT）</font>**<font style="color:rgb(25, 27, 31);">，并展现出强大的泛化能力。这项工作展示了强化学习增强 LVLMs 能力的潜力，使它们在视觉感知任务中更加高效和有效。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741333444294-84ba8e29-f966-451c-97b2-1ead9476673f.png)



## VLM-R1<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(25, 27, 31);">VLM-R1 是一款基于强化学习技术的视觉语言模型，能够通过自然语言指令精确定位图像目标，并支持多模态推理。  
</font><font style="color:rgb(25, 27, 31);">1. </font>**<font style="color:rgb(25, 27, 31);">指代表达理解</font>**<font style="color:rgb(25, 27, 31);">：解析自然语言指令，精准定位图像中的特定目标。  
</font><font style="color:rgb(25, 27, 31);">2. </font>**<font style="color:rgb(25, 27, 31);">强化学习优化</font>**<font style="color:rgb(25, 27, 31);">：采用 </font>[<font style="color:rgb(9, 64, 142);">GRPO</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 技术，在复杂场景下表现出色，提升泛化能力。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

**<font style="color:rgb(25, 27, 31);">github</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://github.com/om-ai-lab/VLM-R1](https://github.com/om-ai-lab/VLM-R1)

:::

<font style="color:rgb(25, 27, 31);">VLM-R1 是浙江大学 Om AI Lab 开发的一款基于强化学习技术的视觉语言模型，旨在通过自然语言指令精确定位图像中的目标物体。例如，用户可以通过描述“图中红色的杯子”来让模型找到对应的图像区域。该模型基于 </font>[**<font style="color:rgb(9, 64, 142);">Qwen2.5-VL</font>**](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=Qwen2.5-VL&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 架构，结合了 </font>[**<font style="color:rgb(9, 64, 142);">DeepSeek R1</font>**](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=DeepSeek+R1&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的强化学习方法，通过强化学习优化和监督微调（SFT）提升了模型的稳定性和泛化能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741316928362-b7a08f1d-fce8-4952-9b64-fd2b9fd5bc27.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **<font style="color:rgb(25, 27, 31);">GRPO 强化学习技术</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">采用 Group Relative Policy Optimization（GRPO）方法</font>**<font style="color:rgb(25, 27, 31);">，使模型在复杂场景下自我探索，减少对大量标注数据的依赖。</font>
+ **<font style="color:rgb(25, 27, 31);">泛化能力与稳定性提升</font>**<font style="color:rgb(25, 27, 31);">：相比传统的监督微调（SFT）方法，VLM-R1 在领域外测试数据中表现出持续提升的性能，表明其真正掌握了视觉内容的理解能力，而不仅仅是依赖记忆。</font>
+ **<font style="color:rgb(25, 27, 31);">基于 Qwen2.5-VL 架构</font>**<font style="color:rgb(25, 27, 31);">：在 Qwen2.5-VL 的基础上开发，通过强化学习优化，在多种复杂场景中保持稳定和高效的性能。</font>

:::color5
**<font style="color:#601BDE;">2.主要功能</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **<font style="color:rgb(25, 27, 31);">指代表达理解（REC）</font>**<font style="color:rgb(25, 27, 31);">：解析自然语言指令，精确定位图像中的特定目标，如根据描述“图中红色的杯子”找到对应区域。</font>
+ **<font style="color:rgb(25, 27, 31);">图像与文本联合处理</font>**<font style="color:rgb(25, 27, 31);">：支持同时输入图像和文字，生成准确的分析结果。</font>
+ **<font style="color:rgb(25, 27, 31);">强化学习优化</font>**<font style="color:rgb(25, 27, 31);">：通过 GRPO（Group Relative Policy Optimization）技术，提升模型在复杂场景下的表现和泛化能力。</font>
+ **<font style="color:rgb(25, 27, 31);">高效训练与推理</font>**<font style="color:rgb(25, 27, 31);">：采用 Flash Attention 等技术，支持单 GPU 训练大规模参数模型，提升计算效率。</font>
+ **<font style="color:rgb(25, 27, 31);">多模态推理与知识生成</font>**<font style="color:rgb(25, 27, 31);">：不仅能识别图像内容，还能进行逻辑推理和文本表达，例如识别蛋白质含量最高的食物并解释原因。</font>
+ **<font style="color:rgb(25, 27, 31);">易用性与开源性</font>**<font style="color:rgb(25, 27, 31);">：提供完整的训练和评估流程，开发者可以快速上手，四步即可开始训练。</font>

:::color5
**<font style="color:#601BDE;">3.GRPO在VLM中怎么做</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

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
**<font style="color:#601BDE;">4.评测</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">左图是测试相同领域评测结果，右图是out-of-domain的评测结果。随着训练步骤增加，grpo相比sft都有明显优势，sft更容易过拟合。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612921977-40799748-632d-454f-b76b-5a936824a3f7.png)

:::color5
**<font style="color:#601BDE;">5.如何运行VLM-R1</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">环境搭建</font>**

<font style="color:rgb(25, 27, 31);">在开始运行 VLM-R1 模型之前，需要配置运行环境。以下是环境搭建的步骤：</font>

```plain
conda create -n vlm-r1 python=3.10
conda activate vlm-r1
bash setup.sh
```

<font style="color:rgb(25, 27, 31);">通过上述命令，创建并激活一个名为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">vlm-r1</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的 Python 环境，并运行</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">setup.sh</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">脚本来安装依赖。</font>

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

<font style="color:rgb(25, 27, 31);">接着，下载提供的</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">dataset_info.json</font>`<font style="color:rgb(25, 27, 31);">、</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">mllm_rec_json.json</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">qwen2_5_vl_full_sft.yaml</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">文件，分别放置在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory/data</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory/examples/train_full</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">目录中。</font>

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

## Vision-R1<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近两年，大模型（LLM）在各个领域大放异彩，从语言理解到图像识别，都出现了突破性的进展。然而，想要</font>**<font style="color:#117CEE;">让模型真正地“像人一样”去进行推理、思考与解释，仍是一项极富挑战性的任务</font>**<font style="color:rgb(25, 27, 31);">。以往我们大多在文本领域探索如何“让模型有自己的思维过程”（如链式思考 Chain-of-Thought），而在多模态领域（尤其是图文结合的情境）——如何把</font>**<font style="color:#117CEE;">视觉信息与语言信息进行深度融合并激发复杂的推理能力</font>**<font style="color:rgb(25, 27, 31);">，还远远没有走到头。</font>

<font style="color:rgb(25, 27, 31);">为此，本文针对多模态大模型（Multimodal LLM，简称 MLLM）的“推理能力激发”展开研究，并提出了一个全新的解决方案，名为</font><font style="color:#74B602;"> </font>**<font style="color:#74B602;">Vision-R1</font>**<font style="color:#74B602;">。</font>**<font style="color:#74B602;">它在视觉和语言的结合中，实现了用“强化学习（RL）+ 冷启动（Cold Start）”的方式，去让模型自发地产生更复杂、更类似于人类思考的推理链。</font>**

:::

:::color3
**简介：****<font style="color:#117CEE;">仅靠强化学习（RL）无法有效激励多模态大型语言模型（MLLM）的推理能力，主要原因是缺乏高质量初始数据和优化策略。</font>**<font style="color:rgb(25, 27, 31);">Vision-R1 提出了一条“冷启动+强化学习”相结合的训练路径，为多模态大模型（MLLM）注入类人式思维与推理能力。具体而言，</font>**<font style="color:#74B602;">先通过“模态桥接（Modality Bridging）”方法大规模生成高质量多模态推理数据并进行冷启动初始化</font>**<font style="color:rgb(25, 27, 31);">；随后利用</font>**<font style="color:#74B602;">渐进式思维抑制训练（</font>**[**<font style="color:#74B602;">PTST</font>**](https://zhida.zhihu.com/search?content_id=254946168&content_type=Article&match_order=1&q=PTST&zhida_source=entity)**<font style="color:#74B602;">）与强化学习相结合</font>**<font style="color:rgb(25, 27, 31);">，逐步引导模型掌握正确且复杂的推理过程。实验表明，Vision-R1-7B 参数规模的模型便能在多项数理推理基准上逼近甚至超越 70B+ 大模型的表现。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Osilly/Vision-R1](https://github.com/Osilly/Vision-R1)

**paper：**[**Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models**](https://arxiv.org/pdf/2503.06749)

**参考：**[**https://zhuanlan.zhihu.com/p/29618155786**](https://zhuanlan.zhihu.com/p/29618155786)

:::

:::color5
**<font style="color:#601BDE;">1.研究动机</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

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
**<font style="color:#601BDE;">2.Vision-R1 pipeline</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744610218132-f1874efd-d72a-49ba-891b-e93a78d70d58.png)

Vision-R1流程。首先利用现有的MLLM和[DeepSeek-R1](https://zhida.zhihu.com/search?content_id=254946168&content_type=Article&match_order=1&q=DeepSeek-R1&zhida_source=entity)获得高质量的Multimodal CoT数据集，将其作为基础MLLM的冷启动初始化数据，从而得到经过冷启动后的Vision-R1-CI，然后在Vision-R1-CI上进行强化学习（RL）训练，最终获得具备推理能力的MLLM，即Vision-R1。  
	我们观察到，直接在MLLM上应用RL无法有效地激发出强大的推理能力（参见(C)和(D)）。未经初始化直接通过RL训练的Vision-R1-Zero难以从有限的数据中泛化（参见(E)、(F)，特别指出Vision-R1-Zero应用了format reward function）。而Vision-R1-CI则面临“过度思考优化问题（Overthinking Optimization Problem）”，偏好较短的CoT推理序列，即正确的推理过程主要集中在较短的CoT推理序列中（参见(A)）。在后续的RL训练中，我们观察到推理步骤虽然有所延长，但性能却出现下降（参见(D)和(E)），这使得优化尤为困难。而Vision-R1则首先在RL训练下缩短CoT，以精炼正确的思考过程。PTST使Vision-R1逐步获得更为复杂的推理过程（参见(C)、(D)和(E)），性能得以提升，因此我们的Vision-R1以70亿参数实现了与具有700亿以上参数的最强MLLM相当的性能（参见(B)）。注意，Vision-R1使用了不同颜色的线条来表示PTST中的不同阶段。

:::color5
**<font style="color:#601BDE;">3.数据合成pipeline</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744610119279-268e2a66-4fdd-4e72-b86c-68c3ced7a91e.png)

整体的数据生成流程，融合了我们的模态桥接（Modality Bridging）方法。首先将多模态数据送入MLLM，以获取包含图像描述（caption）和推理过程的“Pseudo-CoT”，并将其与原始的图像-问题对一起作为MLLM的输入，以生成详细的文本描述。通过这种模态桥接方法，文本描述向DeepSeek-R1提供了全面的信息，有助于生成高质量的CoT推理过程。这些推理过程经过后处理，与原始数据整合后，最终形成Vision-R1-cold数据集。

**实现细节**<font style="color:#D22D8D;"> (by草莓师姐)</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612056366-1bd3e083-a561-4989-9b82-c378f09ddb9e.png)

1. **<font style="color:rgb(25, 27, 31);">伪CoT生成</font>**<font style="color:rgb(25, 27, 31);">：首先，使用现有的多模态大型语言模型（MLLM）来生成“伪CoT”（Pseudo-CoT）。具体的，输入一个图像-问题-答案对和一个提示到一个MLLM中，模型会生成一个包含图像描述和推理过程的文本。这个“伪CoT”不仅包含了图像的描述，还尝试进行初步的推理，但可能缺乏深度和复杂性。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612131128-77febf08-96d2-4f16-aee8-f64fdf6888c8.png)

2. **<font style="color:rgb(25, 27, 31);">文本描述生成</font>**<font style="color:rgb(25, 27, 31);">：将生成的“伪CoT”与原始的图像-问题对以及一个新的提示一起输入到同一个MLLM中，以获取更详细的图像描述。这一步骤的目的是通过MLLM的文本生成能力，将图像中的视觉信息转化为更详细的文本描述，从而为后续的推理提供更多的上下文信息。</font>
3. **<font style="color:rgb(25, 27, 31);">推理生成</font>**<font style="color:rgb(25, 27, 31);">：将经过文本化的图像-问题对输入到一个专门的推理大型语言模型（如</font>**<font style="color:rgb(25, 27, 31);">DeepSeek-R1</font>**<font style="color:rgb(25, 27, 31);">）中，以生成高质量的CoT推理过程。DeepSeek-R1能够生成包含自然认知过程的推理过程，如质疑、反思和检查等。</font>
4. **<font style="color:rgb(25, 27, 31);">数据过滤</font>**<font style="color:rgb(25, 27, 31);">：从生成的CoT数据中保留那些最终答案与真实值一致的样本。使用规则进行数据过滤，去除逻辑不一致的样本，并替换一些词汇以提高语义连贯性。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法：渐进式思维抑制训练（PTST）</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">为了解决冷启动后的过度思考问题，Vision-R1 采用渐进式思维抑制训练（PTST），通过 RL 进一步优化模型的推理能力。</font>

+ **<font style="color:rgb(25, 27, 31);">分组相对策略优化（GRPO）：</font>**<font style="color:rgb(25, 27, 31);"> GRPO 是一种 RL 算法，通过分组类似状态或动作来优化策略，提高学习效率。 详细的可参考往期《</font>[DeepSeek采用的GRPO算法数学原理及算法过程浅析](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg4NjI0NDg0Ng%3D%3D%26mid%3D2247487491%26idx%3D1%26sn%3De3e2c5a43b107c16b12a0bfcd0c0de75%26chksm%3Dcf9dc482f8ea4d94a382afa4903869f0d3ffe660dfaeae2e71e50fcc580b30e1bced687622c9%26scene%3D178%26cur_album_id%3D2829992858538491905%23rd)<font style="color:rgb(25, 27, 31);">》</font>
+ **<font style="color:rgb(25, 27, 31);">硬格式结果奖励函数（HFRRF）：</font>**<font style="color:rgb(25, 27, 31);"> 奖励函数简单：如果输出格式正确且答案正确，则奖励为 1，否则为 0。</font>
+ **<font style="color:rgb(25, 27, 31);">分阶段训练：</font>**<font style="color:rgb(25, 27, 31);"> 训练分为多个阶段，逐步增加序列长度（如 4K、8K、16K 标记）和调整组大小（如 16、8、4）。</font>
    - <font style="color:rgb(25, 27, 31);">每个阶段训练 100 步，使用 64 个 </font>[<font style="color:rgb(9, 64, 142);">NVIDIA H800 80G GPU</font>](https://zhida.zhihu.com/search?content_id=255000916&content_type=Article&match_order=1&q=NVIDIA+H800+80G+GPU&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，约 2 天，使用 Verl 框架。</font>
    - <font style="color:rgb(25, 27, 31);">与固定长度 16K、300 步训练的 Vision-R1-Long 相比，PTST 表现更好，平均长度 2057，平均准确率 55.4%。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

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

## <font style="color:rgb(25, 27, 31);">Video-R1 </font><font style="color:#D22D8D;">(by草莓师姐)</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">当前的多模态大模型（MLLMs）在处理视频时存在一个根本性问题：</font>**<font style="color:#117CEE;">它们往往无法有效利用视频中的时序信息</font>**<font style="color:rgb(25, 27, 31);">。想象一下，如果你只看电影的几个随机截图，而不是按顺序观看整部电影，你能理解剧情吗？显然不能。但这正是当前多模态大模型的工作方式——它们更像是在处理一系列独立的图像，而非真正理解视频中的时序变化。</font>

<font style="color:rgb(25, 27, 31);">另一个挑战是</font>**<font style="color:#117CEE;">高质量视频推理数据的稀缺</font>**<font style="color:rgb(25, 27, 31);">。现有的视频数据集主要集中在简单的识别任务上，缺乏需要复杂推理能力的数据，这使得模型很难学习到真正的视频推理能力。 </font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了解决这些问题，研究团队提出了两个创新方案。（1）</font>**<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。（2）针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/tulerfeng/Video-R1](https://github.com/tulerfeng/Video-R1)

**paper：**[**Video-R1: Reinforcing Video Reasoning in MLLMs**](https://arxiv.org/pdf/2503.21776)

**参考：**[**https://zhuanlan.zhihu.com/p/1889342435928282728**](https://zhuanlan.zhihu.com/p/1889342435928282728)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602200071-763ca10e-6dd5-42bc-bae9-f7fe62dcee02.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。这是对原有GRPO算法的扩展，专门设计用于</font>**<font style="color:#74B602;">鼓励模型进行时序推理</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. <font style="color:rgb(25, 27, 31);">针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。他们构建了两个数据集：</font>
    1. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">Video-R1-COT-165k</font>**<font style="color:rgb(25, 27, 31);">：用于监督微调（SFT）的数据集，包含具有思维链（Chain-of-Thought）注释的图像和视频样本。</font>
    2. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">Video-R1-260k</font>**<font style="color:rgb(25, 27, 31);">：用于强化学习（RL）训练的数据集，包含多种类型的图像和视频推理任务。</font>

:::color5
**<font style="color:#601BDE;">2.T-GRPO算法（Temporal Group Relative Policy Optimization，时序群组相对策略优化）</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744601979834-580a4129-df2b-4699-afe6-57c9e06d78fb.png)

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。这是对原有GRPO算法的扩展，专门设计用于鼓励模型进行时序推理。</font>

**<font style="color:rgb(25, 27, 31);">T-GRPO的核心思想非常巧妙</font>**<font style="color:rgb(25, 27, 31);">：在训练过程中，模型会同时处理</font>**<font style="color:#74B602;">两种视频输入</font>**<font style="color:#74B602;">——</font>**<font style="color:#74B602;">按时间顺序排列的帧序列和随机打乱的帧序列</font>**<font style="color:rgb(25, 27, 31);">。如果模型在有序序列上的表现优于乱序序列，它就会获得正向奖励。这种对比机制有效地鼓励模型利用帧间的时序关系进行推理，而不是仅仅依赖于单帧图像中的视觉特征。</font>

:::color5
**<font style="color:#601BDE;">3.训练数据</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602073812-c3c90af5-55aa-4f9a-8600-1549f9e496a2.png)

<font style="color:rgb(25, 27, 31);">其次，针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。他们构建了两个数据集：</font>

<font style="color:rgb(25, 27, 31);">（1）</font>**<font style="color:rgb(25, 27, 31);">Video-R1-COT-165k</font>**<font style="color:rgb(25, 27, 31);">：用于监督微调（SFT）的数据集，包含具有思维链（Chain-of-Thought）注释的图像和视频样本。</font>

<font style="color:rgb(25, 27, 31);">（2）</font>**<font style="color:rgb(25, 27, 31);">Video-R1-260k</font>**<font style="color:rgb(25, 27, 31);">：用于强化学习（RL）训练的数据集，包含多种类型的图像和视频推理任务。</font>

<font style="color:rgb(25, 27, 31);">这种混合训练方式使模型能够从图像中学习到基础推理技能，再将这些技能迁移到视频领域，从而有效克服了视频推理数据稀缺的问题。</font>

:::color5
**<font style="color:#601BDE;">4.评估</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602107401-1ffbcfd1-715c-4fd7-ab34-a8db348ea124.png)

<font style="color:rgb(25, 27, 31);">研究团队在多个视频理解和推理基准测试上评估了Video-R1的性能，结果令人印象深刻：</font>

**<font style="color:rgb(25, 27, 31);">在VSI-Bench（一个视频空间推理基准测试）上，Video-R1-7B达到了35.8%的准确率，超越了商业专有模型GPT-4o</font>**<font style="color:rgb(25, 27, 31);">，而它仅使用了32帧输入和7B参数。这一结果凸显了显式推理能力在解决视频任务中的必要性。</font>

<font style="color:rgb(25, 27, 31);">研究还发现，在强化学习阶段，即使只进行了1000步训练，Video-R1的性能也显著提升，特别是在推理密集型任务上。这清楚地表明了该强化学习框架的效力，并强调了强化学习在释放可泛化视频推理能力方面的重要性。</font>

<font style="color:rgb(25, 27, 31);">此外，当增加输入帧数从16到32时，模型在几乎所有基准测试上的性能都有所提高。这表明更长的上下文和更丰富的时序信息对模型的推理性能有积极贡献。</font>

:::color5
**<font style="color:#601BDE;">5.未来方向</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);"></font><font style="color:rgb(25, 27, 31);">尽管Video-R1取得了令人瞩目的成果，但研究团队也指出了几个限制和未来的研究方向：</font>

<font style="color:rgb(25, 27, 31);">（1）</font>**<font style="color:rgb(25, 27, 31);">增加帧数</font>**<font style="color:rgb(25, 27, 31);">：当前模型使用16个视频帧训练，这可能限制其处理长时序依赖的能力。未来可以开发更高效的训练和推理策略，以处理更长的视频。</font>

<font style="color:rgb(25, 27, 31);">（2）</font>**<font style="color:rgb(25, 27, 31);">更好的时序建模方法</font>**<font style="color:rgb(25, 27, 31);">：虽然T-GRPO引入了有效的时序感知推理，但它带来了额外的计算开销。未来可以通过探索更高效的时序建模机制来缓解这一问题。</font>

<font style="color:rgb(25, 27, 31);">（3）</font>**<font style="color:rgb(25, 27, 31);">动态响应长度控制</font>**<font style="color:rgb(25, 27, 31);">：当前的长度控制机制在预定义范围内应用固定奖励，而不考虑每个样本的复杂性。未来工作可以探索动态长度控制策略。</font>

<font style="color:rgb(25, 27, 31);">（4）</font>**<font style="color:rgb(25, 27, 31);">大规模强化学习</font>**<font style="color:rgb(25, 27, 31);">：受计算资源限制，当前的强化学习阶段仅训练了1000步。尽管结果很有希望，但增加强化学习训练规模可能会进一步提高模型性能。</font>

<font style="color:rgb(25, 27, 31);">（5）</font>**<font style="color:rgb(25, 27, 31);">改进图像到视频的知识迁移</font>**<font style="color:rgb(25, 27, 31);">：目前，研究团队以直接混合的方式将图像推理数据纳入训练集。未来研究可以设计更有原则的方法，更有效地将推理能力从图像迁移到视频。</font>



## LLM- and VLM-assisted RL
[https://arxiv.org/pdf/2502.15214](https://arxiv.org/pdf/2502.15214)





# 防止 OverThinking<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">随着</font>**[**<font style="color:rgb(9, 64, 142);">OpenAI o1</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=OpenAI+o1&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">、</font>**[**<font style="color:rgb(9, 64, 142);">DeepSeek-R1</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=DeepSeek-R1&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">等模型在数学、编程等复杂任务中表现愈发惊艳，它们生成的推理链却越来越冗长，甚至冗余到令人瞠目。例如，某些模型在回答简单数学问题时，竟能生成长达千余token的步骤，导致单次推理成本飙升至60美元！如何在保持推理精度的同时</font>**<font style="color:rgb(25, 27, 31);">“剪除冗余思考”**，已成为AI领域亟待攻克的难题。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">研究团队(</font>[<font style="color:rgb(9, 64, 142);">莱斯大学</font>](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=%E8%8E%B1%E6%96%AF%E5%A4%A7%E5%AD%A6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)发表了“</font>**<font style="color:rgb(25, 27, 31);">Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models</font>**<font style="color:rgb(25, 27, 31);">”，从</font>**<font style="color:rgb(25, 27, 31);">模型优化</font>**<font style="color:rgb(25, 27, 31);">、</font>**<font style="color:rgb(25, 27, 31);">动态推理控制</font>**<font style="color:rgb(25, 27, 31);">到</font>**<font style="color:rgb(25, 27, 31);">智能提示设计</font>**<font style="color:rgb(25, 27, 31);">，全面拆解了如何让大语言模型“少走弯路”，成为</font>**<font style="color:#ED740C;">Efficient Reasoning Model。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs](https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs)

**paper：**[**Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models**](https://arxiv.org/pdf/2503.16419)

**参考：**[**让AI学会“适可而止”：大语言模型高效推理的革新之路**](https://zhuanlan.zhihu.com/p/31866458362)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744861550918-86a41c17-ca3e-4ff1-83ac-4269be1d8905.png)

:::color5
**<font style="color:#601BDE;">1.什么是OverThinking？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">大语言模型（LLMs）在自然语言理解和复杂推理任务中展现了强大的能力。近年来，专注于推理的大语言模型（LRMs）如OpenAI o1和DeepSeek-R1，通过</font>[<font style="color:rgb(9, 64, 142);">监督微调</font>](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=%E7%9B%91%E7%9D%A3%E5%BE%AE%E8%B0%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（SFT）和强化学习（RL）技术，进一步提升了在数学和编程等领域的推理能力。然而，随着推理链的延长，模型的输出变得冗长，计算开销也随之增加，这种现象被称为“过度思考”。</font>

:::color5
**<font style="color:#601BDE;">2.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">高效推理</font>**<font style="color:rgb(25, 27, 31);">的目标是在保持推理能力的同时，优化推理长度，从而降低计算成本，提升响应速度。尽管高效推理的研究仍处于早期阶段，但其潜力巨大。本文首次系统性地调查了高效推理的当前进展，并将现有工作分为几个关键方向：</font>**<font style="color:rgb(25, 27, 31);">基于模型的高效推理</font>**<font style="color:rgb(25, 27, 31);">、</font>**<font style="color:rgb(25, 27, 31);">基于推理输出的高效推理</font>**<font style="color:rgb(25, 27, 31);">、</font>**<font style="color:rgb(25, 27, 31);">基于输入提示的高效推理</font>**<font style="color:rgb(25, 27, 31);">。此外，本文还探讨了高效数据的使用、小语言模型的推理能力、评估方法和基准测试。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744861811149-0e0c1f61-876c-4bfc-9c21-3a8b8b453d18.png)

高效推理方法概述，可以概括为面向模型的推理方法（左：I、II）和推理输出导向（中：III、IV），以及输入提示导向（右：V、VI）方法。具体来说：

（I）采用长度奖励设计的强化学习；

（II） 使用可变长度CoT数据进行监督微调；

（III） 将推理步骤压缩为更少的潜在表示；

（IV） 推理过程中的动态推理范式；

（V） 快速引导高效推理；

（VI） 路由提示优化推理效率；

## 背景：<font style="color:rgb(25, 27, 31);">长链推理模型与过度思考现象</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.CoT</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">链式思维（CoT）是LLMs中引入推理能力的关键方法。通过生成显式的推理链，模型在复杂任务中的表现得到了显著提升。CoT的变体包括</font>**<font style="color:rgb(25, 27, 31);">自一致性CoT</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">思维树</font>**<font style="color:rgb(25, 27, 31);">，这些方法通过不同的提示策略，进一步增强了模型的推理能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744862035550-c316916a-7adf-4343-a890-db0cf8da3497.png)

> “过度思考现象”的一个例子：当被问及“哪个更大，0.9还是0.11?”, 推理模型需要不必要的长时间（例如QwQ-32B为19秒和DeepSeek-R1为42秒）才能得出正确答案。该示例于2025年3月进行了测试。
>

:::color5
**<font style="color:#601BDE;">2.LLM推理机制</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">大推理模型通过多步推理能力，能够在生成最终答案之前生成详细的推理过程。OpenAI o1和DeepSeek-R1等模型通过</font>**<font style="color:#74B602;">迭代生成中间步骤，逐步优化解决方案，最终得出答案。这种推理能力是通过训练“内化”到模型中</font>**<font style="color:rgb(25, 27, 31);">的，而不是依赖于显式的提示策略。</font>

:::color5
**<font style="color:#601BDE;">3.过度思考问题</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">“过度思考”现象指的是LLMs生成</font>**<font style="color:#117CEE;">过于详细或冗余的推理步骤，导致推理效率下降</font>**<font style="color:rgb(25, 27, 31);">。例如，当询问“2加3等于多少？”时，模型可能会生成数千个token的推理链，其中许多步骤是冗余的。这种现象不仅增加了推理成本，还可能导致错误答案。因此，如何在推理过程中减少冗余步骤，成为了高效推理的核心挑战。</font>

## <font style="color:rgb(25, 27, 31);">基于模型的高效推理</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.带长度奖励设计的强化学习（RL）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">大多数推理模型使用基于RL的方法进行训练，这些方法通常关注准确性和格式奖励。为了</font>**<font style="color:#74B602;">提升推理长度的效率，一些研究提出了在RL框架中引入长度奖励，从而缩短推理过程</font>**<font style="color:rgb(25, 27, 31);">。例如，</font>[**<font style="color:rgb(9, 64, 142);">O1-Pruner</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=O1-Pruner&zhida_source=entity)<font style="color:rgb(25, 27, 31);">通过长度协调奖励和PPO风格的损失函数，优化推理模型的推理长度。具体来说，长度协调奖励基于参考模型输出和预测结果之间的</font>**<font style="color:#74B602;">CoT长度比率计算，并结合准确性约束，确保缩短推理过程不会降低任务性能</font>**<font style="color:rgb(25, 27, 31);">。</font>

[**<font style="color:rgb(9, 64, 142);">KIMI</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=KIMI&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>[**<font style="color:rgb(9, 64, 142);">L1</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=L1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等方法也通过引入长度惩罚和长度约束指令，优化了推理模型的推理长度。</font>**<font style="color:rgb(25, 27, 31);">Demystifying</font>**<font style="color:rgb(25, 27, 31);">通过实验发现，R</font>**<font style="color:#74B602;">L并不总是能增加CoT的长度和复杂性，强调了控制CoT长度增长以确保稳定性能的必要性。他们提出了基于Dirichlet函数的余弦奖励和“超出长度惩罚”评分，有效控制了CoT长度</font>**<font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744870621441-33aa1f27-7637-4ea6-99d0-49b48dd96b96.png)

:::color5
**<font style="color:#601BDE;">2.使用变长CoT数据的监督微调（SFT）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">通过构建变长的CoT推理数据集，并对推理模型进行SFT，可以有效提升推理效率。</font>[**<font style="color:rgb(9, 64, 142);">C3oT</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=C3oT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>[**<font style="color:rgb(9, 64, 142);">TokenSkip</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=TokenSkip&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等方法通过压缩推理步骤，生成了更短的推理链，从而减少了推理过程中的冗余。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744870735097-41d92d85-920c-4676-a462-4bd3017ff6ed.png)

**<font style="color:rgb(25, 27, 31);">C3oT</font>**<font style="color:rgb(25, 27, 31);">使用GPT-4作为压缩器，</font>**<font style="color:#74B602;">减少推理过程的长度，同时确保压缩后的推理保留所有关键信息</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">TokenSkip</font>**<font style="color:rgb(25, 27, 31);">则通过估计每个推理部分的语义重要性，减少推理token，保留关键推理步骤。</font>**<font style="color:rgb(25, 27, 31);">Token-Budget</font>**<font style="color:rgb(25, 27, 31);">通过二进制搜索方法确定最优token预算，生成短推理步骤。</font>**<font style="color:rgb(25, 27, 31);">LearnSkip</font>**<font style="color:rgb(25, 27, 31);">通过手动跳过步骤和提示LLMs生成短推理步骤，收集数据集进行SFT。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744870768611-cccafd0d-ebd5-48e6-9f86-e321aea7f91f.png)



## 基于推理输出的高效推理<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.将推理步骤压缩为更少的潜在表示</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">一些研究探索了将显式的推理步骤压缩为潜在的表示形式，从而减少推理过程中的显式文本输出。</font>[**<font style="color:rgb(9, 64, 142);">Coconut</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=Coconut&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>[**<font style="color:rgb(9, 64, 142);">CODI</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=CODI&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等方法通过将推理步骤压缩为连续的潜在表示，提升了推理的效率和准确性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744870932018-2b171eb3-7d53-4b9f-a7a1-01a92505e4b3.png)

**<font style="color:rgb(25, 27, 31);">Coconut</font>**<font style="color:rgb(25, 27, 31);">将LLM的最终层隐藏状态视为“连续思维”，并重用这些隐藏状态作为下一个输入嵌入。</font>**<font style="color:rgb(25, 27, 31);">CODI</font>**<font style="color:rgb(25, 27, 31);">通过自蒸馏学习连续的潜在CoT，使LLMs能够在</font>**<font style="color:#74B602;">内部执行推理而不生成显式的CoT token</font>**<font style="color:rgb(25, 27, 31);">。</font>[**<font style="color:rgb(9, 64, 142);">CCOT</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=CCOT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">通过预计算完整CoT并选择最重要的隐藏状态作为压缩标准，训练LoRA模块预测这些关键token。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744870940238-07d09dc7-7c36-4e7f-8e0c-772cce980386.png)

[**<font style="color:rgb(9, 64, 142);">Heima</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=Heima&zhida_source=entity)<font style="color:rgb(25, 27, 31);">将详细推理阶段替换为单个“思考token”，更新训练数据并继续微调模型以实现高效推理。</font>[**<font style="color:rgb(9, 64, 142);">Token Assorted</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=Token+Assorted&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在训练期间将部分CoT替换为通过VQ-VAE学习的离散潜在token，训练LLMs使用部分和高层次的推理步骤抽象。</font>

:::color5
**<font style="color:#601BDE;">2.推理过程中的动态推理范式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">动态推理范式通过在推理过程中动态调整推理策略，提升了推理效率。</font>[**<font style="color:rgb(9, 64, 142);">Speculative Rejection</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=Speculative+Rejection&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>[**<font style="color:rgb(9, 64, 142);">Reward-Guided Speculative Decoding</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=Reward-Guided+Speculative+Decoding&zhida_source=entity)<font style="color:rgb(25, 27, 31);">等方法</font>**<font style="color:#74B602;">通过奖励模型和置信度指标，动态选择最优的推理路径，减少了不必要的计算开销。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871095337-36b62556-f7b1-4abf-90f5-344bec0b37d0.png)

**<font style="color:rgb(25, 27, 31);">Speculative Rejection</font>**<font style="color:rgb(25, 27, 31);">通过动态减少计算开销，生成多个响应直到内存限制接近，然后根据奖励模型评估丢弃低质量输出。</font>**<font style="color:rgb(25, 27, 31);">Reward-Guided Speculative Decoding</font>**<font style="color:rgb(25, 27, 31);">利用过程奖励模型动态评估中间输出，接受高奖励分数的输出，进一步优化低奖励分数的输出。</font>

**<font style="color:rgb(25, 27, 31);">Dynamic Parallel Tree Search</font>**<font style="color:rgb(25, 27, 31);">通过</font>**<font style="color:#74B602;">并行化节点扩展和搜索转换机制，优化树基推理</font>**<font style="color:rgb(25, 27, 31);">。</font>[**<font style="color:rgb(9, 64, 142);">FastMCTS</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=FastMCTS&zhida_source=entity)<font style="color:rgb(25, 27, 31);">通过</font>**<font style="color:#74B602;">优先处理高置信度轨迹，优化多步推理数据合成</font>**<font style="color:rgb(25, 27, 31);">。</font>[**<font style="color:rgb(9, 64, 142);">Certaindex</font>**](https://zhida.zhihu.com/search?content_id=255395707&content_type=Article&match_order=1&q=Certaindex&zhida_source=entity)<font style="color:rgb(25, 27, 31);">通过量化LLMs在整个推理过程中的置信度，允许早期终止以释放资源。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871111304-043587e9-ee1b-41e7-b5c7-2c39700ffcf5.png)

> 有效的Best-of-N抽样方法示例。（左）) Speculative Rejection用奖励模型来估计部分生成质量。然后，它会提前停止得分较低的采样序列。（右）ST BoN评估早期世代的潜在嵌入。每个思维路径的潜在嵌入将用于计算其他token之间的成对一致性。一致性最高的序列更有可能得到正确答案。
>



## 基于输入提升的高效推理<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.提示引导的高效推理</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">通过提示引导LLMs生成更少的推理步骤，可以有效提升推理效率。</font>**<font style="color:rgb(25, 27, 31);">Token-Budget</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Draft</font>**<font style="color:rgb(25, 27, 31);">等方法通过设置token预算和限制推理步骤的冗长度，生成了更简洁的推理链。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871227299-b6d977d4-e12e-491a-9602-c1f1c98ae16b.png)

**<font style="color:rgb(25, 27, 31);">Token-Budget</font>**<font style="color:rgb(25, 27, 31);">通过提示LLMs估计最小token预算，并在提示中指定token约束，引导LLMs生成更token高效且准确的响应。</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Draft</font>**<font style="color:rgb(25, 27, 31);">通过限制每个思考步骤的冗长度，生成简洁的推理步骤。</font>**<font style="color:rgb(25, 27, 31);">CCoT</font>**<font style="color:rgb(25, 27, 31);">通过提示LLMs“简洁”地执行逐步推理，减少推理步骤。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871257081-3b39ba44-7eaf-4ab4-aefe-996f3b2de557.png)

:::color5
**<font style="color:#601BDE;">2.基于提示属性的推理路由</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">根据输入提示的复杂性和不确定性，动态分配推理模型，可以进一步提升推理效率。</font>**<font style="color:rgb(25, 27, 31);">RouteLLM</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Sketch-of-Thought</font>**<font style="color:rgb(25, 27, 31);">等方法通过训练分类器或利用不确定性指标，</font>**<font style="color:#74B602;">将简单查询分配给低延迟的LLMs，复杂查询分配给更强大的LLMs。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871273097-34911419-d401-4c4c-9725-352ef314e743.png)

**<font style="color:rgb(25, 27, 31);">RouteLLM</font>**<font style="color:rgb(25, 27, 31);">通过训练查询路由器，根据复杂性分配查询。</font>**<font style="color:rgb(25, 27, 31);">Sketch-of-Thought</font>**<font style="color:rgb(25, 27, 31);">通过轻量级DistilBERT路由器动态选择最合适的推理范式。</font>**<font style="color:rgb(25, 27, 31);">Self-Ref</font>**<font style="color:rgb(25, 27, 31);">通过微调不确定性专用token，使LLMs能够自主决定何时路由。</font>

## <font style="color:rgb(25, 27, 31);">基于高效训练数据和模型压缩提升推理能力</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.使用更少的数据训练推理模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">通过精心选择和构建训练数据，可以在减少数据量的同时，保持或提升推理性能。</font>**<font style="color:rgb(25, 27, 31);">LIMO</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">s1K</font>**<font style="color:rgb(25, 27, 31);">等方法通过选择高质量的问题和解决方案，生成了</font>**<font style="color:#74B602;">高效的训练数据集</font>**<font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871361872-6cfd812e-fc81-4b95-b325-77935129feb0.png)

**<font style="color:rgb(25, 27, 31);">LIMO</font>**<font style="color:rgb(25, 27, 31);">通过选择基于难度、通用性和知识多样性的高质量问题，以及基于最优结构组织、有效认知支架和严格验证的高质量解决方案，仅用817个训练样本就超越了使用超过100,000个样本的模型。</font>**<font style="color:rgb(25, 27, 31);">s1K</font>**<font style="color:rgb(25, 27, 31);">通过控制测试时计算资源，生成了包含1,000个高质量问题和推理轨迹的紧凑数据集。</font>

:::color5
**<font style="color:#601BDE;">2.小语言模型的推理能力与模型压缩</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在资源受限的环境中，</font>**<font style="color:#74B602;">小语言模型（SLMs）通过蒸馏和模型压缩技术</font>**<font style="color:rgb(25, 27, 31);">，保留了较强的推理能力。</font>**<font style="color:rgb(25, 27, 31);">SKIntern</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">SCORE</font>**<font style="color:rgb(25, 27, 31);">等方法通过将符号知识内化到SLMs中，提升了推理质量和效率。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744871422920-79fc1a56-16a4-4949-8e41-e614667ae542.png)

**<font style="color:rgb(25, 27, 31);">SKIntern</font>**<font style="color:rgb(25, 27, 31);">通过内部化符号知识，提升了SLMs的CoT推理质量和效率。</font>**<font style="color:rgb(25, 27, 31);">SCORE</font>**<font style="color:rgb(25, 27, 31);">通过生成自校正数据并微调模型，使SLMs能够作为自校正推理器。</font>**<font style="color:rgb(25, 27, 31);">Pruning and Quantization</font>**<font style="color:rgb(25, 27, 31);">通过量化减少模型精度，保留了推理性能，而修剪则导致推理质量严重下降。</font>

## 评估<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了系统评估LLMs的推理能力，研究者们提出了多种基准测试和评估框架。</font>**<font style="color:rgb(25, 27, 31);">Sys2Bench</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Compute-Optimal Test-Time Scaling</font>**<font style="color:rgb(25, 27, 31);">等方法通过多样化的数据集和计算优化策略，全面评估了LLMs在不同推理任务中的表现。</font>

**<font style="color:rgb(25, 27, 31);">Sys2Bench</font>**<font style="color:rgb(25, 27, 31);">通过五个推理类别（算术、逻辑、常识、算法和规划任务）的十一个数据集，评估LLMs的推理能力。</font>**<font style="color:rgb(25, 27, 31);">Evaluating Overthinking</font>****<font style="color:#74B602;">通过分析4,018个代理任务轨迹，提出了“过度思考”评分，并展示了高评分与任务性能下降之间的强相关性</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">Compute-Optimal Test-Time Scaling</font>**<font style="color:rgb(25, 27, 31);">通过研究计算优化策略对LLM性能的影响，发现适当策略下，小模型可以在复杂推理任务中超越大模型。</font>

## 应用与讨论<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.应用</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">高效推理LLMs在自动驾驶、嵌入式AI和医疗等领域展现了广泛的应用前景。通过提升实时决策能力和数据处理效率，这些模型在多个领域中发挥了重要作用。</font>

**<font style="color:rgb(25, 27, 31);">自动驾驶</font>**<font style="color:rgb(25, 27, 31);">：高效推理LLMs通过处理大量传感器数据，帮助车辆在</font>**<font style="color:#74B602;">复杂驾驶情境中做出更安全的决策</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">嵌入式AI</font>**<font style="color:rgb(25, 27, 31);">：高效推理LLMs通过处理来自摄像头和传感器的数据，</font>**<font style="color:#74B602;">使机器人能够快速做出决策</font>**<font style="color:rgb(25, 27, 31);">并安全地与人类互动。</font>

**<font style="color:rgb(25, 27, 31);">医疗</font>**<font style="color:rgb(25, 27, 31);">：高效推理LLMs通过分析患者记录和医学研究，帮助医生更快、更准确地诊断和治疗。</font>

:::color5
**<font style="color:#601BDE;">2.讨论</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在提升推理能力的同时，如何在安全性和效率之间找到平衡，成为了当前研究的重点。</font>**<font style="color:rgb(25, 27, 31);">Meta-Reasoner</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Inner Thinking Transformer</font>**<font style="color:rgb(25, 27, 31);">等方法通过动态调整推理策略，提升了推理性能。</font>

**<font style="color:rgb(25, 27, 31);">Meta-Reasoner</font>**<font style="color:rgb(25, 27, 31);">通过上下文多臂老虎机评估推理进展并选择最优策略。</font>

**<font style="color:rgb(25, 27, 31);">Inner Thinking Transformer</font>**<font style="color:rgb(25, 27, 31);">通过动态分配额外处理资源，使小模型能够达到与大模型相当的性能。</font>

**<font style="color:rgb(25, 27, 31);">Safety of Efficient Reasoning</font>**<font style="color:rgb(25, 27, 31);">通过研究长推理模型的安全性，发现长输出虽然增强了自校正能力，但也可能被攻击策略利用。</font>

**<font style="color:rgb(25, 27, 31);">RL vs. SFT</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">RL通过试错学习，使模型能够在新情境中找到创造性解决方案，</font>****<font style="color:#117CEE;">但需要大量训练</font>****<font style="color:#74B602;">。SFT通过精心选择的CoT示例进行训练，行为更一致且易于控制，</font>****<font style="color:#117CEE;">但在面对未覆盖的挑战时可能表现不佳</font>****<font style="color:#74B602;">。结合两种方法可能是未来的研究方向。</font>**

## <font style="color:rgb(25, 27, 31);">结论</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.结论</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">本文首次系统性地调查了大语言模型高效推理的当前进展，并将现有方法分为基于模型、基于推理输出和基于输入提示的三大类。此外，本文还探讨了高效数据的使用、小语言模型的推理能力、评估方法和基准测试。高效推理方法在多个领域中展现了巨大的应用潜力，为未来的研究和应用提供了重要的参考。</font>

<font style="color:rgb(25, 27, 31);">通过这篇论文，我们不仅深入了解了高效推理的前沿技术，还看到了AI在复杂任务中的无限可能。未来，随着研究的不断深入，高效推理技术将在更多领域中发挥重要作用，推动人工智能的进一步发展。</font>

  




