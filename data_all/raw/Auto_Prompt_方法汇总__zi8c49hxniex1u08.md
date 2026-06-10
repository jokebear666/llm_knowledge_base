# Auto Prompt 方法汇总

<!-- source: yuque://zhongxian-iiot9/hlyypb/zi8c49hxniex1u08 -->

## **<font style="color:rgb(25, 27, 31);">APE：candidate -> selection -> resample</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">APE的核心思路是：</font>**<font style="color:rgb(25, 27, 31);">从候选集中选出好的prompt，再在好的prompt附近进行试探性地搜索</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">paper：</font>**[**https://arxiv.org/pdf/2305.03495**](https://arxiv.org/pdf/2305.03495)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764055710030-15a1c4b1-88e1-4337-9608-623a8b243dec.png)

> (a) 我们的方法，自动提示工程师 (APE)，能够自动生成指令，用于通过输出示例指定的任务：它生成多个指令候选，通过直接推理或基于语义相似性的递归过程，使用目标模型执行这些候选指令，并根据计算出的评估分数选择最合适的指令。(b) 根据 Honovich 等人 (2022) 提出的 24 个 NLP 任务的四分位均值衡量，APE 在使用 InstructGPT 模型时能够超越人类的表现 (Ouyang 等人，2022)。
>

<font style="color:rgb(26, 28, 30);">APE 旨在利用 LLM 的能力自动生成并优化 Prompt，其工作流主要包含以下三个关键步骤：</font>

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">第一步：生成候选 (Prompt Candidates Generation)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">利用 LLM 强大的生成能力构建初始 Prompt 池，主要有两种生成模式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056159820-e40f38cd-8243-482d-917e-76e65c258fbf.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056163589-e1cdf599-9191-4e4d-9661-a6a59dbc6f84.png)

+ **<font style="color:rgb(26, 28, 30);"></font>****<font style="color:rgb(26, 28, 30);">Forward Mode (常规生成)</font>**
    - **<font style="color:rgb(26, 28, 30);">机制</font>**<font style="color:rgb(26, 28, 30);">：提供任务演示 (Examples)，让 LLM 在结尾处直接生成 Prompt。</font>
    - **<font style="color:rgb(26, 28, 30);">特点</font>**<font style="color:rgb(26, 28, 30);">：考验模型的 Instruction Following（指令遵循）能力。</font>
+ **<font style="color:rgb(26, 28, 30);">Reverse Mode (填充生成)</font>**
    - **<font style="color:rgb(26, 28, 30);">机制</font>**<font style="color:rgb(26, 28, 30);">：即 Insert 模式。将待生成的 Prompt 视为填空题放在 Examples 之前，让 LLM 根据上下文填充。</font>
    - **<font style="color:rgb(26, 28, 30);">特点</font>**<font style="color:rgb(26, 28, 30);">：更符合直觉，逻辑上更加自然。</font>
    - _<font style="color:rgb(26, 28, 30);">注：GPT 系列支持 Insert 模式；OpenAI 在论文 [5] 中详细阐述了其实现原理。</font>_

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">第二步：评估与筛选 (Evaluation & Selection)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">在训练集上对生成的 Prompt 进行打分，保留高质量候选。</font>

+ **<font style="color:rgb(26, 28, 30);">📊</font>****<font style="color:rgb(26, 28, 30);"> 打分方式 (Scoring Metrics)</font>**
    - **<font style="color:rgb(26, 28, 30);">Execution Accuracy (执行准确率) [推荐 </font>****<font style="color:rgb(26, 28, 30);">🌟</font>****<font style="color:rgb(26, 28, 30);">]</font>**<font style="color:rgb(26, 28, 30);">：直接执行 Prompt，计算任务指标（如 Accuracy, F1）。</font>**<font style="color:rgb(26, 28, 30);">实验证明此方法效果更好。</font>**
    - **<font style="color:rgb(26, 28, 30);">Log Probability (对数概率)</font>**<font style="color:rgb(26, 28, 30);">：计算生成期望答案的概率，不通过具体执行。</font>
+ **<font style="color:rgb(26, 28, 30);">⚡</font>****<font style="color:rgb(26, 28, 30);"> 提效策略：多阶段评估 (Multi-stage Strategy)</font>**<font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">由于在全量数据上评估开销过大，采用“漏斗式”筛选：</font>
    - <font style="color:rgb(26, 28, 30);">先在</font>**<font style="color:rgb(26, 28, 30);">少量</font>**<font style="color:rgb(26, 28, 30);">数据子集 (Subset) 上评估。</font>
    - <font style="color:rgb(26, 28, 30);">过滤掉表现较差的 Prompt。</font>
    - <font style="color:rgb(26, 28, 30);">循环筛选，直到候选集足够小，再进行</font>**<font style="color:rgb(26, 28, 30);">全量</font>**<font style="color:rgb(26, 28, 30);">评估。</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">第三步：迭代优化 (Iterative Resampling)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">模拟</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Monte-Carlo Search</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">过程，在高分 Prompt 基础上进一步挖掘潜力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056227391-1f9728d1-4326-4054-8032-04d1890b2240.png)

+ **<font style="color:rgb(26, 28, 30);"></font>****<font style="color:rgb(26, 28, 30);">核心机制</font>**
    - **<font style="color:rgb(26, 28, 30);">Resample</font>**<font style="color:rgb(26, 28, 30);">：将筛选出的高分 Prompt 交给 LLM，要求其生成语义相似的变体。</font>
    - **<font style="color:rgb(26, 28, 30);">迭代</font>**<font style="color:rgb(26, 28, 30);">：这是一个可循环的过程，不断尝试寻找更优解。</font>
+ **<font style="color:rgb(26, 28, 30);"></font>****<font style="color:rgb(26, 28, 30);">实验结论</font>**
    - <font style="color:rgb(26, 28, 30);">对于</font>**<font style="color:rgb(26, 28, 30);">高难度任务</font>**<font style="color:rgb(26, 28, 30);">，进行 Resample 能显著进一步提升效果。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">总结 (Key Takeaway)</font>**

:::

<font style="color:rgb(26, 28, 30);">APE 的本质是一个</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">"Generate - Evaluate - Refine"</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">的闭环：</font>

+ <font style="color:rgb(26, 28, 30);">利用</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Reverse Mode</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">生成更加自然的初始指令；</font>
+ <font style="color:rgb(26, 28, 30);">通过</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Execution Accuracy</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">和</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">多阶段策略</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">高效筛选；</font>
+ <font style="color:rgb(26, 28, 30);">利用 </font>**<font style="color:rgb(26, 28, 30);">Resampling</font>**<font style="color:rgb(26, 28, 30);"> 攻克长尾难题。</font>



## **<font style="color:rgb(25, 27, 31);">APO：gradient descent in language space</font>**
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">APO 的本质是</font>**<font style="color:rgb(26, 28, 30);">在文本空间实现“梯度下降” (Gradient Descent)</font>**<font style="color:rgb(26, 28, 30);">。它通过分析错误样本，让 LLM 生成自然语言形式的“梯度”（即错误原因），并据此优化 Prompt。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">paper：</font>**[**https://arxiv.org/pdf/2305.03495**](https://arxiv.org/pdf/2305.03495)

:::

**提出的基于文本梯度的提示优化（ProTeGi）概述。**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056661333-48da4355-64b4-415d-9df6-4cbe5971197f.png)

**使用文本对话树来模拟梯度下降并克服离散优化障碍。**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056656163-133f8638-e0c3-433d-a693-cdadf6dec63a.png)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">第一步：获取“文本梯度” (Gradient Generation)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(26, 28, 30);">目标</font>**<font style="color:rgb(26, 28, 30);">：诊断当前 Prompt 为什么会出错。</font>

+ **<font style="color:rgb(26, 28, 30);">输入</font>**<font style="color:rgb(26, 28, 30);">：一批 Error Samples（当前 Prompt 预测错误的样本）。</font>
+ **<font style="color:rgb(26, 28, 30);">动作</font>**<font style="color:rgb(26, 28, 30);">：让 LLM 分析这些样本，指出预测失败的原因。</font>
+ **<font style="color:rgb(26, 28, 30);">输出</font>**<font style="color:rgb(26, 28, 30);">：</font>**<font style="color:rgb(26, 28, 30);">Textual Gradient</font>**<font style="color:rgb(26, 28, 30);">（即以自然语言描述的错误原因）。</font>

<font style="color:rgb(25, 27, 31);">给定一批error samples（当前prompt无法预测正确的），让LLM</font>**<font style="color:rgb(25, 27, 31);">给出当前prompt预测错误的原因</font>**<font style="color:rgb(25, 27, 31);">，这一原因即文本形式的“gradient”。生成gradient的prompt如下。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056744259-72d8b7a6-1054-4d58-879d-8dc16b8b5d76.png)

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">第二步：应用梯度 & 扩展 (Applying Gradient)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">利用得到的“梯度”来更新 Prompt，包含两个子步骤：</font>

+ **<font style="color:rgb(26, 28, 30);">🛠️</font>****<font style="color:rgb(26, 28, 30);"> 子步骤 1：定向修复 (Editing)</font>**
    - <font style="color:rgb(26, 28, 30);">利用 LLM 对原 Prompt 进行</font>**<font style="color:rgb(26, 28, 30);">编辑</font>**<font style="color:rgb(26, 28, 30);">，目标是修复第一步中识别出的“梯度”问题。</font><font style="color:rgb(25, 27, 31);">给到LLM的prompt如下。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056777576-39472271-3fd4-4d6b-b469-bae7db235219.png)

+ **<font style="color:rgb(26, 28, 30);">🔁</font>****<font style="color:rgb(26, 28, 30);"> 子步骤 2：语义扩充 (Resampling)</font>**
    - <font style="color:rgb(26, 28, 30);">参考 APE 的做法，对修复后的 Prompt 进行重采样，生成语义相似的变体，以增加候选集的多样性。</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">第三步：高效筛选 (Selection via Bandit)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(26, 28, 30);">难点</font>**<font style="color:rgb(26, 28, 30);">：在全量训练集上评估所有候选 Prompt 开销过大。</font><font style="color:rgb(26, 28, 30);">  
</font>**<font style="color:rgb(26, 28, 30);">解决方案</font>**<font style="color:rgb(26, 28, 30);">：将筛选过程建模为</font>**<font style="color:rgb(26, 28, 30);">多臂老虎机问题 (Multi-armed Bandit Problem)</font>**<font style="color:rgb(26, 28, 30);">。</font>

+ **<font style="color:rgb(26, 28, 30);">🎰</font>****<font style="color:rgb(26, 28, 30);"> 对应关系</font>**<font style="color:rgb(26, 28, 30);">：</font>
    - **<font style="color:rgb(26, 28, 30);">Arms (拉杆)</font>**<font style="color:rgb(26, 28, 30);">  不同的 Prompt Candidates</font>
    - **<font style="color:rgb(26, 28, 30);">Hidden Value (隐藏价值)</font>**<font style="color:rgb(26, 28, 30);">  Prompt 在全量数据上的真实表现</font>
    - **<font style="color:rgb(26, 28, 30);">Pulling (拉动动作)</font>**<font style="color:rgb(26, 28, 30);">  在随机采样的数据子集上评估 Prompt</font>
+ **<font style="color:rgb(26, 28, 30);">⚖️</font>****<font style="color:rgb(26, 28, 30);"> 算法选择</font>**<font style="color:rgb(26, 28, 30);">：</font>
    - <font style="color:rgb(26, 28, 30);">作者测试了 UCB, UCB-E, Successive Rejects 三种算法。</font>
    - **<font style="color:rgb(26, 28, 30);">结论</font>**<font style="color:rgb(26, 28, 30);">：</font>**<font style="color:rgb(26, 28, 30);">UCB</font>**<font style="color:rgb(26, 28, 30);"> 和 </font>**<font style="color:rgb(26, 28, 30);">UCB-E</font>**<font style="color:rgb(26, 28, 30);"> 效果最佳，能以最小的计算代价找到最优 Prompt。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">全局策略：Beam Search (束搜索)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">为了防止陷入局部最优并强化探索能力，APO 在每一轮迭代的最外层包裹了一个 </font>**<font style="color:rgb(26, 28, 30);">Beam Search</font>**<font style="color:rgb(26, 28, 30);"> 过程。这意味着系统会同时维护多个有潜力的 Prompt 路径，而不是单线作战。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764056841736-fdc666a4-579e-45d9-b634-58b676161953.png)

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">总结 (Summary)</font>**

:::

<font style="color:rgb(26, 28, 30);">APO 模仿了神经网络的训练过程：</font>

+ **<font style="color:rgb(26, 28, 30);">计算 Loss</font>**<font style="color:rgb(26, 28, 30);">  找出 Error Samples；</font>
+ **<font style="color:rgb(26, 28, 30);">计算 Gradient</font>**<font style="color:rgb(26, 28, 30);">  LLM 分析错误原因；</font>
+ **<font style="color:rgb(26, 28, 30);">Update Weights</font>**<font style="color:rgb(26, 28, 30);">  LLM 编辑 Prompt；</font>
+ **<font style="color:rgb(26, 28, 30);">Validation</font>**<font style="color:rgb(26, 28, 30);">  使用 Bandit 算法高效评估。</font>



## <font style="color:rgb(25, 27, 31);">OPRO：</font>[<font style="color:rgb(9, 64, 142);">LLM as optimizer</font>](https://zhida.zhihu.com/search?content_id=234495183&content_type=Article&match_order=1&q=LLM+as+optimizer&zhida_source=entity)
:::color3
**简介：**<font style="color:rgb(26, 28, 30);">与 APO 模仿“梯度下降”的数学逻辑不同，OPRO 是一种</font>**<font style="color:rgb(26, 28, 30);">更具 LLM 原生性 (Native)</font>**<font style="color:rgb(26, 28, 30);"> 的优化思路。  
</font><font style="color:rgb(26, 28, 30);">其核心思想是：</font>**<font style="color:rgb(26, 28, 30);">让 LLM 阅读过往的“尝试-得分”记录，自己总结规律，在纯文本空间中逐步迭代出更好的 Prompt。</font>**

**<font style="color:rgb(25, 27, 31);">paper：</font>**[**https://arxiv.org/pdf/2309.03409**](https://arxiv.org/pdf/2309.03409)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764057111765-833033d8-d824-4c7c-bac4-f248757538f9.png)

> OPRO框架概述。以元提示作为输入，LLM生成目标函数的新解，然后将新解及其得分添加到元提示中，用于下一个优化步骤。元提示包含优化过程中获得的解-得分对、任务的自然语言描述，以及（在提示优化中）一些任务示例。图3展示了一个用于提示优化的元提示示例。
>

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">构建 Meta-prompt (优化器的“指令”)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">这是输入给</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Optimizer LLM</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">的核心提示词，旨在教会它如何优化。它包含两个关键部分：</font>

+ **<font style="color:rgb(26, 28, 30);">📈</font>****<font style="color:rgb(26, 28, 30);"> 优化轨迹 (Solution-Score Pairs)</font>**<font style="color:rgb(26, 28, 30);">：</font>
    - <font style="color:rgb(26, 28, 30);">即“过往的 Prompt + 对应的任务得分”。</font>
    - **<font style="color:rgb(26, 28, 30);">排列规则</font>**<font style="color:rgb(26, 28, 30);">：实践中通常保留</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Top 20</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">的结果，并严格按照分数</font>**<font style="color:rgb(26, 28, 30);">从低到高</font>**<font style="color:rgb(26, 28, 30);">排列。</font>
    - _<font style="color:rgb(26, 28, 30);">目的：让 LLM 观察“变得更好”的趋势，从而推断出进化的方向。</font>_
+ **<font style="color:rgb(26, 28, 30);">📝</font>****<font style="color:rgb(26, 28, 30);"> 任务描述 (Task Description)</font>**<font style="color:rgb(26, 28, 30);">：</font>
    - <font style="color:rgb(26, 28, 30);">包含任务示例 (Examples) 和具体的优化目标说明。</font>

<font style="color:rgb(25, 27, 31);">GSM8K任务上的meta-prompt如下。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764057177718-bb9914e8-9e27-4de3-ac3e-b85e0ebdab06.png)

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">生成新解 (Generation via Optimizer LLM)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(26, 28, 30);">动作</font>**<font style="color:rgb(26, 28, 30);">：将 Meta-prompt 输入给 Optimizer LLM。</font>
+ **<font style="color:rgb(26, 28, 30);">机制</font>**<font style="color:rgb(26, 28, 30);">：模型基于对过往迭代轨迹的理解，生成一个新的 Solution (即新的 Prompt)。</font>
+ **<font style="color:rgb(26, 28, 30);">稳定性策略</font>**<font style="color:rgb(26, 28, 30);">：为了保证效果，这一步通常重复 </font>**<font style="color:rgb(26, 28, 30);">8次</font>**<font style="color:rgb(26, 28, 30);">，以增加探索的多样性。</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">评估与反馈 (Evaluation via Scorer LLM)</font>**

:::

+ **<font style="color:rgb(26, 28, 30);">角色分离</font>**<font style="color:rgb(26, 28, 30);">：OPRO 明确区分了</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Optimizer LLM</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">(负责想策略) 和</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Scorer LLM</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">(负责干活/考试)。两者可以使用不同的模型。</font>
+ **<font style="color:rgb(26, 28, 30);">动作</font>**<font style="color:rgb(26, 28, 30);">：在 Scorer LLM 上执行新生成的 Prompt。</font>
+ **<font style="color:rgb(26, 28, 30);">闭环</font>**<font style="color:rgb(26, 28, 30);">：计算得分，将新的“Solution-Score Pair”追加到 Meta-prompt 的历史记录中，用于下一轮迭代。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">迭代终止 (Termination)</font>**

:::

<font style="color:rgb(26, 28, 30);">循环上述过程，直到满足以下任一条件：</font>

+ <font style="color:rgb(26, 28, 30);">效果无法继续提升 (收敛)。</font>
+ <font style="color:rgb(26, 28, 30);">达到预设的步数上限 (Max Steps)。</font>
+ **<font style="color:rgb(26, 28, 30);">输出</font>**<font style="color:rgb(26, 28, 30);">：返回历史记录中得分最高的 Prompt。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764057265243-78a73e37-ed1b-4d11-9a1d-f91a2cf5bf37.png)

> GSM8K 测试示例中的 Q_begin 提示格式，采用“QA”模式。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764057269434-cc8e1b7a-34a0-48f9-8bab-534868078b87.png)

> GSM8K 测试示例中的 Q_end 提示格式，采用“QA”模式。
>

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">广阔的应用边界 (Beyond Prompting)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">OPRO 的定位不仅仅是 Prompt 优化工具，而是一个</font>**<font style="color:rgb(26, 28, 30);">通用的基于文本的优化器 (Text-based Optimizer)</font>**<font style="color:rgb(26, 28, 30);">。</font><font style="color:rgb(26, 28, 30);">  
</font><font style="color:rgb(26, 28, 30);">论文作者展示了其在数学优化问题上的潜力，例如：</font>

+ **<font style="color:rgb(26, 28, 30);">线性回归 (Linear Regression)</font>**
+ **<font style="color:rgb(26, 28, 30);">旅行商问题 (Traveling Salesman Problem, TSP)</font>**

:::color5
**<font style="color:#601BDE;">6.</font>****<font style="color:#601BDE;">总结 (Summary)</font>**

:::

<font style="color:rgb(26, 28, 30);">如果说 APO 是教 LLM 学微积分（梯度下降），那么 OPRO 就是教 LLM </font>**<font style="color:rgb(26, 28, 30);">“读史书，知兴替”</font>**<font style="color:rgb(26, 28, 30);">。它通过阅读按照分数排序的历史记录，利用 LLM 本身的上下文学习能力 (In-Context Learning) 来推导优化的方向。</font>



## **<font style="color:rgb(25, 27, 31);">总结</font>**
:::color3
**<font style="color:#000000;">简介：</font>**<font style="color:#000000;">本文介绍了3种</font>`<font style="color:#000000;">automatic prompt engineering</font>`<font style="color:#000000;">框架，其中</font>`<font style="color:#000000;">APE</font>`<font style="color:#000000;">的主要思路是</font>**<font style="color:#000000;">挑选+试探性优化</font>**<font style="color:#000000;">，优化的方向性较弱；</font>`<font style="color:#000000;">APO</font>`<font style="color:#000000;">和</font>`<font style="color:#000000;">OPRO</font>`<font style="color:#000000;">则应用了更完整的</font>**<font style="color:#000000;">optimizer框架</font>**<font style="color:#000000;">，其中</font>`<font style="color:#000000;">APO</font>`<font style="color:#000000;">基于gradient descent，本质是基于error case来调优，而</font>`<font style="color:#000000;">OPRO</font>`<font style="color:#000000;">直接依靠LLM的逻辑推理能力，基于迭代过程的规律进行优化。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">三大框架横向对比 (Framework Comparison)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">本文介绍的三种框架虽然目标一致，但其背后的</font>**<font style="color:rgb(26, 28, 30);">优化哲学</font>**<font style="color:rgb(26, 28, 30);">存在显著差异：</font>

| **<font style="color:rgb(26, 28, 30);">框架</font>** | **<font style="color:rgb(26, 28, 30);">核心机制</font>** | **<font style="color:rgb(26, 28, 30);">优化逻辑</font>** | **<font style="color:rgb(26, 28, 30);">特点评价</font>** |
| --- | --- | --- | --- |
| **<font style="color:rgb(26, 28, 30);">APE</font>** | **<font style="color:rgb(26, 28, 30);">挑选 + 试探</font>** | <font style="color:rgb(26, 28, 30);">在高分 Prompt 附近进行采样 (Resample)</font> | <font style="color:rgb(26, 28, 30);">优化的</font>**<font style="color:rgb(26, 28, 30);">方向性较弱</font>**<font style="color:rgb(26, 28, 30);">，更多依赖随机探索与筛选。</font> |
| **<font style="color:rgb(26, 28, 30);">APO</font>** | **<font style="color:rgb(26, 28, 30);">梯度下降 (Gradient Descent)</font>** | <font style="color:rgb(26, 28, 30);">基于</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Error Case</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">(错误样本) 进行反向分析与修正</font> | <font style="color:rgb(26, 28, 30);">引入了完整的 Optimizer 概念，通过“诊断错误”来明确优化方向。</font> |
| **<font style="color:rgb(26, 28, 30);">OPRO</font>** | **<font style="color:rgb(26, 28, 30);">逻辑推理 (Reasoning)</font>** | <font style="color:rgb(26, 28, 30);">基于</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">迭代历史</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">(History) 总结规律</font> | <font style="color:rgb(26, 28, 30);">依靠 LLM 自身的归纳推理能力，从过往的“尝试-得分”中学习进化路径。</font> |


:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">通用性与适用前提 (Applicability)</font>**

:::

+ **<font style="color:rgb(26, 28, 30);">🌍</font>****<font style="color:rgb(26, 28, 30);"> 通用性</font>**<font style="color:rgb(26, 28, 30);">：理论上，这些框架对各类 NLP 任务（分类、信息抽取、文本生成等）均通用。</font>
+ **<font style="color:rgb(26, 28, 30);">🔑</font>****<font style="color:rgb(26, 28, 30);"> 核心前提</font>**<font style="color:rgb(26, 28, 30);">：只需定义好清晰的 </font>**<font style="color:rgb(26, 28, 30);">评价指标 (Evaluation Metric)</font>**<font style="color:rgb(26, 28, 30);"> 即可。</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">落地场景建议 (Practical Scenarios)</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(26, 28, 30);">只要你的业务场景中涉及 Prompt 的使用，都可以借鉴这些思路。常见的高价值场景包括：</font>

+ **<font style="color:rgb(26, 28, 30);">🏆</font>****<font style="color:rgb(26, 28, 30);"> 刷榜提分</font>**<font style="color:rgb(26, 28, 30);">：在各类 Benchmark 上追求极限效果。</font>
+ **<font style="color:rgb(26, 28, 30);">🏷️</font>****<font style="color:rgb(26, 28, 30);"> 标注器优化</font>**<font style="color:rgb(26, 28, 30);">：提升 LLM 作为数据标注工人的准确率。</font>
+ **<font style="color:rgb(26, 28, 30);">🗣️</font>****<font style="color:rgb(26, 28, 30);"> 用户反馈闭环</font>**<font style="color:rgb(26, 28, 30);">：根据真实用户的反馈持续迭代 Prompt。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">进阶思考：Prompt 优化的 "RLHF" (Deep Insight)</font>**

:::

**<font style="color:rgb(26, 28, 30);">利用用户反馈数据进行 Prompt 自动化优化，与 RLHF (基于人类反馈的强化学习) 有异曲同工之妙。</font>**

+ **<font style="color:rgb(26, 28, 30);">传统 RLHF</font>**<font style="color:rgb(26, 28, 30);">：优化的是</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Model Parameters</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">(模型参数)。</font>
+ **<font style="color:rgb(26, 28, 30);">Auto Prompting</font>**<font style="color:rgb(26, 28, 30);">：优化的是</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Prompt Context</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">(提示词上下文)。</font>

**<font style="color:rgb(26, 28, 30);">实现路径：</font>**

+ <font style="color:rgb(26, 28, 30);">收集用户反馈数据。</font>
+ <font style="color:rgb(26, 28, 30);">训练一个</font><font style="color:rgb(26, 28, 30);"> </font>**<font style="color:rgb(26, 28, 30);">Reward Model (奖励模型)</font>**<font style="color:rgb(26, 28, 30);"> </font><font style="color:rgb(26, 28, 30);">作为评价者。</font>
+ <font style="color:rgb(26, 28, 30);">将其嵌入 APE/APO/OPRO 框架中作为 Scorer。</font>
+ <font style="color:rgb(26, 28, 30);">自动迭代，寻找能获得 Reward Model 最高打分的 Prompt。</font>

**<font style="color:rgb(26, 28, 30);">结论</font>**<font style="color:rgb(26, 28, 30);">：这不仅仅是 Prompt Engineering，更是</font>**<font style="color:rgb(26, 28, 30);">将优化过程自动化、算法化</font>**<font style="color:rgb(26, 28, 30);">的重要尝试。</font>



## <font style="color:rgb(25, 27, 31);">参考资料</font>
<font style="color:rgb(25, 27, 31);">[1] Large Language Models are Zero-Shot Reasoners:</font><font style="color:rgb(25, 27, 31);"> </font>[_<font style="color:rgb(9, 64, 142);background-color:transparent;">https://arxiv.org/abs/2205.11916</font>_](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2205.11916)

<font style="color:rgb(25, 27, 31);">[2] Large Language Models as Optimizers:</font><font style="color:rgb(25, 27, 31);"> </font>[_<font style="color:rgb(9, 64, 142);background-color:transparent;">https://arxiv.org/abs/2309.03409</font>_](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2309.03409)

<font style="color:rgb(25, 27, 31);">[3] Large Language Models are Human-Level Prompt Engineers:</font><font style="color:rgb(25, 27, 31);"> </font>[_<font style="color:rgb(9, 64, 142);background-color:transparent;">https://openreview.net/pdf?id=92gvk82DE-</font>_](https://link.zhihu.com/?target=https%3A//openreview.net/pdf%3Fid%3D92gvk82DE-)

<font style="color:rgb(25, 27, 31);">[4] Automatic Prompt Optimization with 'Gradient Descent' and Beam Search:</font><font style="color:rgb(25, 27, 31);"> </font>[_<font style="color:rgb(9, 64, 142);background-color:transparent;">https://arxiv.org/abs/2305.03495</font>_](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2305.03495)

<font style="color:rgb(25, 27, 31);">[5] Efficient Training of Language Models to Fill in the Middle:</font><font style="color:rgb(25, 27, 31);"> </font>[_<font style="color:rgb(9, 64, 142);background-color:transparent;">https://arxiv.org/abs/2207.14255</font>_](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2207.14255)



