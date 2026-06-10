# RLHF

<!-- source: yuque://zhongxian-iiot9/hlyypb/ug2w2gkgsusgcino -->

# 基础
:::color3
<font style="color:#1f2329;">⼀类机器学习⽅法，其核⼼思想是通过与环境的交互、试错探索，逐步优化策略，以最⼤化⻓期累计的奖励。不同于监督学习和⽆监督学习，强化学习不依赖⼤量的标注数据，⽽是</font><font style="color:#de7802;">通过智能体（agent）与环境的互动来⾃⾏学习</font><font style="color:#1f2329;">。</font>

**<font style="color:#1f2329;">参考</font>**<font style="color:#1f2329;">：</font>[https://zhuanlan.zhihu.com/p/27332009509](https://zhuanlan.zhihu.com/p/27332009509)

:::

<font style="color:#2ea121;background-color:#f0fbef;">在强化学习中，智能体在每个时间步（timestep）根据当前状态（state）采取⼀个动作（action），随后环境会反馈⼀个新的状态和相应的奖励（reward）。智能体的⽬标是通过优化策略，使得其在⻓期内获得的奖励最⼤化。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739006856130-a828d0ae-a40f-45ff-a8f8-995d2546e440.png)

**<font style="color:rgb(51, 51, 51);">核心要素</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">状态（State）</font>**<font style="color:rgb(51, 51, 51);">：环境的当前情况。</font>
+ **<font style="color:rgb(51, 51, 51);">动作（Action）</font>**<font style="color:rgb(51, 51, 51);">：智能体的行为选择。</font>
+ **<font style="color:rgb(51, 51, 51);">奖励（Reward）</font>**<font style="color:rgb(51, 51, 51);">：环境对动作的即时反馈。</font>
+ **<font style="color:rgb(51, 51, 51);">策略（Policy）</font>**<font style="color:rgb(51, 51, 51);">：从状态到动作的映射规则。</font>
+ **<font style="color:rgb(51, 51, 51);">价值函数（Value Function）</font>**<font style="color:rgb(51, 51, 51);">：评估状态或动作的长期收益。</font>

**<font style="color:rgb(51, 51, 51);">分类</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">有模型学习（Model-based RL）</font>**<font style="color:rgb(51, 51, 51);">：显式建模环境动态（状态转移和奖励函数），利用模型规划最优策略（如Dyna-Q）。</font>
+ **<font style="color:rgb(51, 51, 51);">免模型学习（Model-free RL）</font>**<font style="color:rgb(51, 51, 51);">：不依赖环境模型，直接通过经验优化策略或价值函数（如Q-Learning、PPO）。</font>
+ **<font style="color:#74B602;">有模型/免模型 的区别在于是否显式建模环境动态，与是否使用奖励模型无关。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739006921375-86cd3a4d-bed2-4ac9-9985-220e743912c2.png)



:::color5
**<font style="color:#601BDE;">1.RL示例</font>**

:::

<font style="color:rgb(25, 27, 31);">想象一下教一辆自动驾驶汽车。你不会为每一种可能的情况编写代码，对吧？相反，你会让它通过驾驶来学习，并给予它反馈，例如：</font>

+ **<font style="color:rgb(25, 27, 31);">奖励</font>**<font style="color:rgb(25, 27, 31);">：当它保持在车道内、遵守交通规则或到达目的地时，给予“干得好！”的反馈。</font>
+ **<font style="color:rgb(25, 27, 31);">惩罚</font>**<font style="color:rgb(25, 27, 31);">：当它偏离车道或离其他车辆太近时，给予“小心！”的反馈。</font>

<font style="color:rgb(25, 27, 31);">这就是强化学习（RL）的核心。一个 AI 代理（比如我们的自动驾驶汽车或 LLM）通过在环境中做出决策来学习，目标是最大化长期奖励。它学习一种策略——一种在不同情境下选择行动的方法。</font>

<font style="color:rgb(25, 27, 31);"></font>

## 对齐/偏好学习
:::color5
**<font style="color:#601BDE;">1.什么是对齐</font>**

:::

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">定义：对⻬是指使⼈⼯智能系统的⽬标、⾏为与⼈类的意图和价值观保持⼀致。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">重要性：未对⻬的AI可能会产⽣意外或不良的⾏为 ，导致安全和伦理问题。</font>

:::color5
**<font style="color:#601BDE;">2.为什么需要对齐/偏好学习</font>**

:::

<font style="color:rgb(25, 27, 31);">对于简单任务，定义奖励很容易（“到达出口得 +1 分”）。</font>**<font style="color:#74B602;">但对于生成文本的 LLM，什么是“好”文本？它不仅仅是语法或事实的问题，而是人类的品味、思维的连贯性、推理的正确性、消除输出中不希望出现的偏见等更多内容。</font>**

<font style="color:rgb(25, 27, 31);">这些是主观的！尝试编写一个“好文本”的公式是非常困难的。</font>

<font style="color:rgb(25, 27, 31);">偏好学习来帮忙！与其编写一个奖励公式，我们使用人类的偏好。我们让人们比较两个 LLM 的响应，并询问“你更喜欢哪一个？”</font>

+ **<font style="color:rgb(25, 27, 31);">人类裁判，而非公式</font>**<font style="color:rgb(25, 27, 31);">：人类成为我们的“奖励函数”。</font>
+ **<font style="color:rgb(25, 27, 31);">学习人类喜欢的内容</font>**<font style="color:rgb(25, 27, 31);">：我们训练 LLM 生成人类更可能喜欢的文本。</font>

:::color5
**<font style="color:#601BDE;">3.对齐的挑战</font>**

:::

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">复杂性：⼈类价值观复杂多样 ，难以⽤简单的规则或⽬标函数完全描述。</font>
+ <font style="color:#1f2329;">不可预测性：AI模型可能在训练数据之外的情境中表现出未预期的⾏为。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">⿊箱问题：深度学习模型的内部决策过程难以解释和控制。</font>

## <font style="color:#1f2329;">RL与传统方法/监督学习对比</font>
:::color5
**<font style="color:#601BDE;">1.监督学习的局限性</font>**

:::

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">数据依赖：需要⼤量⾼质量的标注数据，获取成本⾼。</font>
+ <font style="color:#1f2329;">泛化能⼒： 可能在未见过的情境中表现不佳。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">⽆法捕捉偏好：难以反映⼈类对输出质量的细微偏好和价值判断。</font>

:::color5
**<font style="color:#601BDE;">2.RL的优势</font>**

:::

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">处理复杂⽬标：通过奖励函数，可以表达复杂的、难以明确编码的⽬标和偏好。</font>
+ <font style="color:#1f2329;">有效利⽤反馈：强化学习能从⼈类的⽐较或排名等相对反馈中学习，⽽不需要绝对的正确答案。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">提⾼模型对⻬度：通过持续优化，模型的⾏为更符合⼈类期望。</font>



## <font style="color:#1f2329;">RLHF 基于人类反馈的强化学习</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739170710343-a3587405-0502-4ad5-89bf-f5e6592adedb.png)

**<font style="color:#117CEE;">流程</font>**

<font style="color:#1456f0;">a.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">初始模型训练：使⽤监督学习</font><font style="color:#1f2329;">，基于现有数据训练初始语⾔模型。</font>

<font style="color:#1456f0;">b.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">收集⼈类反馈：模型⽣成多个响应</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">由⼈类对这些响应进⾏⽐较</font><font style="color:#1f2329;">和评价。</font>

<font style="color:#1456f0;">c.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">训练奖励模型：利⽤⼈类反馈的数据</font><font style="color:#1f2329;">，训练⼀个能够评估模型输出质量的奖励模型。</font>

<font style="color:#1456f0;">d.  </font><font style="color:#1f2329;">策略优化：使⽤强化学习⽅法，根据奖励模型的评估结果，优化原始语⾔模型的策略。</font>

**<font style="color:#117CEE;">优势</font>**

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">直接融⼊⼈类价值观：通过⼈类反馈</font><font style="color:#1f2329;">，模型能更好地理解和遵循⼈类偏好。</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⾼效学习：强化学习能从较少的反馈中学习到有效</font><font style="color:#1f2329;">的策略。</font>

<font style="color:#1456f0;">◦  </font><font style="color:#1f2329;">动态适应：模型可以持续更新，适应新的反馈和要求。</font>

## RLHF优缺点
**<font style="color:rgb(25, 27, 31);">优点：</font>**<font style="color:rgb(25, 27, 31);">适用于各种复杂任务，特别是那些需要长期策略和决策的任务；通过人类反馈，可以有效处理稀疏奖励问题，使得模型更快收敛。</font>

**<font style="color:rgb(25, 27, 31);">缺点：</font>**<font style="color:rgb(25, 27, 31);">强化学习通常需要大量的计算资源和时间，特别是在复杂环境中；人类反馈数据可能带有噪声或偏见，需要有效的处理和过滤机制。</font>



# RLHF评估
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">评估大型语言模型（LLM）在通过RLHF（基于人类反馈的强化学习）后的效果需要从多个维度综合考量</font>**<font style="color:rgb(51, 51, 51);">，</font>****<font style="color:#ED740C;">包括生成质量、安全性、对齐性、任务完成度等</font>****<font style="color:rgb(51, 51, 51);">。</font>**<font style="color:rgb(51, 51, 51);"></font>

:::

:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">生成质量</font>**
    - **<font style="color:rgb(51, 51, 51);">Perplexity（困惑度）</font>**<font style="color:rgb(51, 51, 51);">：衡量模型对文本的预测能力，数值越低表示模型对数据的拟合越好（但可能无法完全反映生成质量）。</font>
    - **<font style="color:rgb(51, 51, 51);">BLEU/ROUGE/METEOR</font>**<font style="color:rgb(51, 51, 51);">：文本生成任务的经典指标，用于衡量生成文本与参考文本的匹配度，适用于翻译、摘要等任务。</font>
    - **<font style="color:rgb(51, 51, 51);">Human Preference Score</font>**<font style="color:rgb(51, 51, 51);">：通过人工标注或众包评估生成结果的流畅性、相关性和有用性。</font>
    - **<font style="color:rgb(51, 51, 51);">Diversity（多样性）</font>**<font style="color:rgb(51, 51, 51);">：生成结果的词汇多样性和内容新颖性，例如通过Unique N-gram Ratio衡量。</font>
2. **<font style="color:rgb(51, 51, 51);">安全性与对齐性</font>**
    - **<font style="color:rgb(51, 51, 51);">Toxicity Score</font>**<font style="color:rgb(51, 51, 51);">：使用分类模型（如Perspective API）检测生成内容中的有害性、攻击性语言。</font>
    - **<font style="color:rgb(51, 51, 51);">Ethical Alignment</font>**<font style="color:rgb(51, 51, 51);">：评估模型是否遵循伦理规范（例如拒绝生成违法、歧视性内容），常用基准如ETHICS数据集。</font>
    - **<font style="color:rgb(51, 51, 51);">Sensitive Content Rate</font>**<font style="color:rgb(51, 51, 51);">：统计生成内容中涉及敏感话题（如暴力、政治）的比例。</font>
3. **<font style="color:rgb(51, 51, 51);">任务完成度</font>**
    - **<font style="color:rgb(51, 51, 51);">准确率（Accuracy）</font>**<font style="color:rgb(51, 51, 51);">：在问答、数学推理等任务中的正确率，例如MMLU（大规模多任务语言理解）中的表现。</font>
    - **<font style="color:rgb(51, 51, 51);">任务成功率</font>**<font style="color:rgb(51, 51, 51);">：如代码生成（HumanEval）、工具调用（如API使用）的成功率。</font>
4. **<font style="color:rgb(51, 51, 51);">指令遵循能力</font>**
    - **<font style="color:rgb(51, 51, 51);">Instruction Compliance</font>**<font style="color:rgb(51, 51, 51);">：模型是否严格遵循复杂指令，例如多步骤任务或格式约束。</font>
    - **<font style="color:rgb(51, 51, 51);">AlpacaEval</font>**<font style="color:rgb(51, 51, 51);">：通过人工或自动化评估模型在开放指令任务中的表现。</font>
5. **<font style="color:rgb(25, 27, 31);">真实性</font>**<font style="color:rgb(25, 27, 31);">：响应必须基于真实的事实，准确反映提供的上下文和指令。模型应避免生成任何虚假或缺乏数据支持的信息。</font>
6. **<font style="color:rgb(25, 27, 31);">帮助性</font>**<font style="color:rgb(25, 27, 31);">：模型输出的内容应切实有用，能够有效地回答用户的查询，并提供积极、富有吸引力、教育性强且相关的内容。应严格按照指令执行，确保对用户有价值。</font>
7. **<font style="color:rgb(25, 27, 31);">简洁性</font>**<font style="color:rgb(25, 27, 31);">：响应应简明扼要，避免无关的冗余内容，确保清晰高效地传达信息，而不让用户被细节淹没。</font>
8. **<font style="color:rgb(25, 27, 31);">相关性</font>**<font style="color:rgb(25, 27, 31);">：所有回应的内容都应紧密关联于用户的查询、对话历史以及助手的当前上下文。模型应定制其输出，确保与用户的需求和期望完全一致。</font>
9. **<font style="color:rgb(25, 27, 31);">无害性</font>**<font style="color:rgb(25, 27, 31);">：模型必须优先保障用户安全，避免产生任何可能导致非法、不道德或有害行为的内容。始终提倡道德行为和负责任的交流。</font>
10. **<font style="color:rgb(25, 27, 31);">去偏见</font>**<font style="color:rgb(25, 27, 31);">：模型生成的响应必须没有偏见，涉及性别、种族、国籍或政治等各类偏见，确保公平和公正，遵循广泛接受的道德和伦理标准。</font>

:::color5
**<font style="color:#601BDE;">2.评估方法</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 自动化评估</font>**

+ **<font style="color:rgb(51, 51, 51);">静态测试集</font>**<font style="color:rgb(51, 51, 51);">：在预定义的数据集（如MMLU、HellaSwag）上测试模型性能。</font>
+ **<font style="color:rgb(51, 51, 51);">动态生成测试</font>**<font style="color:rgb(51, 51, 51);">：通过Prompt模板生成多样化输入，评估模型输出的质量和安全性。</font>
+ **<font style="color:rgb(51, 51, 51);">对抗性测试</font>**<font style="color:rgb(51, 51, 51);">：设计意图绕过模型安全机制的输入（例如越狱Prompt），测试防御能力。</font>

**<font style="color:rgb(51, 51, 51);">2. 人工评估</font>**

+ **<font style="color:rgb(51, 51, 51);">人工打分</font>**<font style="color:rgb(51, 51, 51);">：标注员对生成结果的质量、安全性、有用性进行打分（例如1-5分）。</font>
+ **<font style="color:rgb(51, 51, 51);">A/B测试</font>**<font style="color:rgb(51, 51, 51);">：让用户对比不同模型（如RLHF前后版本）的输出，选择更优结果。</font>

**<font style="color:rgb(51, 51, 51);">3. 对比实验</font>**

+ **<font style="color:rgb(51, 51, 51);">基线模型对比</font>**<font style="color:rgb(51, 51, 51);">：比较RLHF微调后的模型与原始预训练模型、其他开源模型（如LLaMA、ChatGLM）的表现。</font>
+ **<font style="color:rgb(51, 51, 51);">消融实验</font>**<font style="color:rgb(51, 51, 51);">：分析RLHF各阶段（如奖励模型训练、PPO优化）对最终效果的贡献。</font>

:::color5
**<font style="color:#601BDE;">3.常用Benchmark</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 通用能力</font>**

+ **<font style="color:rgb(51, 51, 51);">MMLU</font>**<font style="color:rgb(51, 51, 51);">：涵盖57个学科的多选题数据集，测试模型的知识广度和推理能力。</font>
+ **<font style="color:rgb(51, 51, 51);">HellaSwag/ARC</font>**<font style="color:rgb(51, 51, 51);">：常识推理和科学知识问答数据集。</font>
+ **<font style="color:rgb(51, 51, 51);">GSM8K</font>**<font style="color:rgb(51, 51, 51);">：数学应用题测试集，评估多步推理能力。</font>

**<font style="color:rgb(51, 51, 51);">2. 安全性</font>**

+ **<font style="color:rgb(51, 51, 51);">RealToxicityPrompts</font>**<font style="color:rgb(51, 51, 51);">：包含潜在有害Prompt的数据集，测试模型生成有害内容的概率。</font>
+ **<font style="color:rgb(51, 51, 51);">ETHICS</font>**<font style="color:rgb(51, 51, 51);">：评估模型对伦理场景的理解和应对。</font>

**<font style="color:rgb(51, 51, 51);">3. 指令遵循</font>**

+ **<font style="color:rgb(51, 51, 51);">AlpacaEval</font>**<font style="color:rgb(51, 51, 51);">：基于Alpaca指令集的自动化评估框架。</font>
+ **<font style="color:rgb(51, 51, 51);">Vicuna Benchmark</font>**<font style="color:rgb(51, 51, 51);">：通过人工打分评估开放领域对话能力。</font>

**<font style="color:rgb(51, 51, 51);">4. 生成质量</font>**

+ **<font style="color:rgb(51, 51, 51);">SummEval</font>**<font style="color:rgb(51, 51, 51);">：摘要任务评估数据集，结合人工打分和自动指标。</font>
+ **<font style="color:rgb(51, 51, 51);">HumanEval</font>**<font style="color:rgb(51, 51, 51);">：代码生成任务的功能正确性评估。</font>

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">以QWEN为例的评估实践</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 评估指标</font>**

+ **<font style="color:rgb(51, 51, 51);">生成质量</font>**<font style="color:rgb(51, 51, 51);">：在AlpacaEval和Vicuna Benchmark中对比微调前后的输出质量。</font>
+ **<font style="color:rgb(51, 51, 51);">安全性</font>**<font style="color:rgb(51, 51, 51);">：使用RealToxicityPrompts测试有害内容生成率，并通过人工审核过滤敏感回答。</font>
+ **<font style="color:rgb(51, 51, 51);">任务完成度</font>**<font style="color:rgb(51, 51, 51);">：在MMLU和GSM8K上测试知识能力，在代码生成（HumanEval）中评估实用性。</font>

**<font style="color:rgb(51, 51, 51);">2. 评估方法</font>**

+ **<font style="color:rgb(51, 51, 51);">多阶段对比</font>**<font style="color:rgb(51, 51, 51);">：比较预训练模型（Qwen-7B）、SFT模型（Qwen-7B-Chat）、RLHF微调后的最终版本。</font>
+ **<font style="color:rgb(51, 51, 51);">人工标注</font>**<font style="color:rgb(51, 51, 51);">：通过众包平台对生成结果进行偏好评分，例如“有用性”和“安全性”的平衡。</font>

**<font style="color:rgb(51, 51, 51);">3. Benchmark表现</font>**

+ **<font style="color:rgb(51, 51, 51);">MMLU</font>**<font style="color:rgb(51, 51, 51);">：QWEN-72B在微调后可能在MMLU上达到约80%的准确率，接近GPT-3.5水平。</font>
+ **<font style="color:rgb(51, 51, 51);">安全性测试</font>**<font style="color:rgb(51, 51, 51);">：通过对抗性Prompt测试，RLHF版本的有害内容生成率显著低于原始模型。</font>
+ **<font style="color:rgb(51, 51, 51);">中文任务</font>**<font style="color:rgb(51, 51, 51);">：在CLUE和C-Eval等中文基准测试中验证多语言能力。</font>

**<font style="color:rgb(51, 51, 51);">4. 实际应用指标</font>**

+ **<font style="color:rgb(51, 51, 51);">用户满意度</font>**<font style="color:rgb(51, 51, 51);">：在阿里云内部或合作方场景中收集用户反馈，优化模型对齐性。</font>
+ **<font style="color:rgb(51, 51, 51);">推理效率</font>**<font style="color:rgb(51, 51, 51);">：监控生成速度和资源消耗（如显存占用），确保落地可行性。</font>

:::color5
**<font style="color:#601BDE;">5.挑战与改进方向</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">评估偏差</font>**<font style="color:rgb(51, 51, 51);">：自动指标可能无法完全反映人类偏好，需结合动态人工评估。</font>
2. **<font style="color:rgb(51, 51, 51);">长尾场景覆盖</font>**<font style="color:rgb(51, 51, 51);">：模型可能在常见任务表现良好，但对罕见指令或复杂伦理场景仍需优化。</font>
3. **<font style="color:rgb(51, 51, 51);">多语言评估</font>**<font style="color:rgb(51, 51, 51);">：需扩展对中文、小语种的支持测试（如QWEN的中文能力专项评估）。</font>



# RLHF中的四个模型<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">Actor</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">是待优化的LLM，负责生成文本。</font>
+ **<font style="color:rgb(51, 51, 51);">Critic</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">和</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Reward Model</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">提供反馈信号（长期价值和即时奖励），前者关注策略的长期效果，后者关注单步质量。</font>
+ **<font style="color:rgb(51, 51, 51);">Reference Model</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">是安全约束，防止LLM“跑偏”。</font>
+ <font style="color:rgb(51, 51, 51);">四者共同作用，使LLM在强化学习中既能优化特定目标（如人类偏好），又能保持语言生成的基本能力。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743411227505-2e7ff874-cac1-4444-b52e-bab4bafff841.png)

<font style="color:rgb(25, 27, 31);">如上图，</font>**<font style="color:rgb(25, 27, 31);">在RLHF-PPO阶段，一共有四个主要模型</font>**<font style="color:rgb(25, 27, 31);">，分别是：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

+ [**<font style="color:rgb(9, 64, 142);">Actor Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Actor+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：演员模型</font>**<font style="color:rgb(25, 27, 31);">，这就是我们想要训练的目标语言模型</font>
+ [**<font style="color:rgb(9, 64, 142);">Critic Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Critic+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：评论家模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是预估总收益</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);">t</font>
+ [**<font style="color:rgb(9, 64, 142);">Reward Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Reward+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：奖励模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是计算即时收益</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">R</font><font style="color:rgb(25, 27, 31);">t</font>
+ **<font style="color:rgb(25, 27, 31);">Reference Model：参考模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是在RLHF阶段给语言模型增加一些“约束”，防止语言模型训歪（朝不受控制的方向更新，效果可能越来越差）</font>

<font style="color:rgb(25, 27, 31);">其中:</font>

+ **<font style="color:rgb(25, 27, 31);">Actor/Critic Model</font>**<font style="color:rgb(25, 27, 31);">在RLHF阶段是</font>**<font style="color:rgb(25, 27, 31);">需要训练</font>**<font style="color:rgb(25, 27, 31);">的（图中给这两个模型加了粗边，就是表示这个含义）；而</font>**<font style="color:rgb(25, 27, 31);">Reward/Reference Model</font>**<font style="color:rgb(25, 27, 31);">是</font>**<font style="color:rgb(25, 27, 31);">参数冻结</font>**<font style="color:rgb(25, 27, 31);">的。</font>
+ <font style="color:rgb(25, 27, 31);">Critic/Reward/Reference Model共同组成了一个“奖励-loss”计算体系（我自己命名的，为了方便理解），我们综合它们的结果计算loss，用于更新Actor和Critic Model</font>

:::color5
**<font style="color:#601BDE;">1.对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **维度** | **Critic** | **Actor** | **Reward Model** | **Reference Model** |
| --- | --- | --- | --- | --- |
| 模型 | **<font style="color:#ED740C;">一个辅助模型</font>** | **<font style="color:#ED740C;">待训练的LLM本身</font>** | **<font style="color:#ED740C;">独立训练的模型</font>** | **<font style="color:#ED740C;">未经RL训练的原始LLM</font>** |
| <font style="color:rgb(51, 51, 51);">作用对象</font> | <font style="color:rgb(51, 51, 51);">价值评估</font> | <font style="color:rgb(51, 51, 51);">策略生成</font> | <font style="color:rgb(51, 51, 51);">奖励信号</font> | <font style="color:rgb(51, 51, 51);">行为基准</font> |
| <font style="color:rgb(51, 51, 51);">更新频率</font> | <font style="color:rgb(51, 51, 51);">常异步更新</font> | <font style="color:rgb(51, 51, 51);">主更新对象</font> | <font style="color:rgb(51, 51, 51);">预训练/定期</font> | <font style="color:rgb(51, 51, 51);">通常固定</font> |
| <font style="color:rgb(51, 51, 51);">输出类型</font> | <font style="color:rgb(51, 51, 51);">标量值</font> | <font style="color:rgb(51, 51, 51);">概率分布</font> | <font style="color:rgb(51, 51, 51);">标量值</font> | <font style="color:rgb(51, 51, 51);">动作/文本</font> |
| <font style="color:rgb(51, 51, 51);">训练数据</font> | <font style="color:rgb(51, 51, 51);">环境交互数据</font> | <font style="color:rgb(51, 51, 51);">环境交互数据</font> | <font style="color:rgb(51, 51, 51);">人类偏好数据</font> | <font style="color:rgb(51, 51, 51);">专家轨迹</font> |
| <font style="color:rgb(51, 51, 51);">典型联系</font> | <font style="color:rgb(51, 51, 51);">指导Actor更新</font> | <font style="color:rgb(51, 51, 51);">受Critic引导</font> | <font style="color:rgb(51, 51, 51);">提供训练信号</font> | <font style="color:rgb(51, 51, 51);">约束Actor行为</font> |


:::color5
**<font style="color:#601BDE;">2.RLHF中，四者协同工作</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(51, 51, 51);">Actor（LLM）</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">生成候选回答。</font>
2. **<font style="color:rgb(51, 51, 51);">Reward Model</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">为回答打分（如是否符合人类偏好）。</font>
3. **<font style="color:rgb(51, 51, 51);">Critic Model</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">评估回答的长期价值（例如结合上下文预测后续对话的潜在收益）。</font>
4. **<font style="color:rgb(51, 51, 51);">Reference Model</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">提供初始策略的基准，约束Actor的更新方向，避免过度偏离原始能力。</font>
5. <font style="color:rgb(51, 51, 51);">通过PPO等算法，结合奖励信号和KL散度约束，调整Actor的参数。</font>

## Critic Model 价值模型<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
+ **<font style="color:rgb(51, 51, 51);">核心作用</font>**<font style="color:rgb(51, 51, 51);">：评估当前状态（state）或状态-动作对（state-action pair）的长期价值（即预期累积奖励），指导Actor如何调整策略。</font>
+ **<font style="color:rgb(51, 51, 51);">与LLM的关系</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">在LLM训练中，</font>**<font style="color:#ED740C;">Critic通常是一个辅助模型</font>**<font style="color:rgb(51, 51, 51);">，负责对LLM生成的内容（如对话回复、文本补全等）进行</font>**<font style="color:rgb(51, 51, 51);">质量评分</font>**<font style="color:rgb(51, 51, 51);">。例如，判断生成的文本是否符合逻辑、是否安全、是否满足特定任务需求等。</font>
    - <font style="color:rgb(51, 51, 51);">Critic的输出作为</font>**<font style="color:rgb(51, 51, 51);">价值信号</font>**<font style="color:rgb(51, 51, 51);">，帮助Actor（LLM）理解哪些生成策略更优。例如，在训练中通过价值梯度（如优势函数）调整LLM的参数。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：在Actor-Critic框架中，Critic与Actor联合优化，例如PPO（Proximal Policy Optimization）算法。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">Critic Model用于预测期望总收益</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">Vt</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">，和Actor模型一样，它需要做参数更新</font>**<font style="color:rgb(25, 27, 31);">。实践中，Critic Model的设计和初始化方式也有很多种，例如和Actor共享部分参数、从RW阶段的Reward Model初始化而来等等。我们讲解时，和deepspeed-chat的实现保持一致：从RW阶段的Reward Model初始化而来。</font>  
**<font style="color:rgb(25, 27, 31);">	你可能想问：训练Actor模型我能理解，但我还是不明白，为什么要单独训练一个Critic模型用于预测收益呢？</font>**<font style="color:rgb(25, 27, 31);">这是因为，当我们在前文讨论总收益 </font><font style="color:rgb(25, 27, 31);">Vt</font><font style="color:rgb(25, 27, 31);"> （即时 + 未来）时，我们是站在上帝视角的，也就是这个 </font><font style="color:rgb(25, 27, 31);">Vt</font><font style="color:rgb(25, 27, 31);"> 就是客观存在的、真正的总收益。但是我们在训练模型时，就没有这个上帝视角加成了，</font>**<font style="color:rgb(25, 27, 31);">也就是在</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">时刻，我们给不出客观存在的总收益</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">Vt</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">，我们只能训练一个模型去预测它。</font>**  
**<font style="color:rgb(25, 27, 31);">	所以总结来说，在RLHF中，我们不仅要训练模型生成符合人类喜好的内容的能力（Actor），也要提升模型对人类喜好量化判断的能力（Critic）</font>**<font style="color:rgb(25, 27, 31);">。这就是Critic模型存在的意义。我们来看看它的大致架构：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743413038289-4aa8849b-5e54-42c4-b838-62f4570fa052.png)

<font style="color:rgb(25, 27, 31);">deepspeed-chat</font>**<font style="color:#74B602;">采用了Reward模型作为它的初始化</font>**<font style="color:rgb(25, 27, 31);">，所以这里我们也按Reward模型的架构来简单画画它。你可以简单理解成，</font>**<font style="color:#74B602;">Reward/Critic模型和Actor模型的架构是很相似的（毕竟输入都一样），同时，它在最后一层增加了一个Value Head层</font>**<font style="color:rgb(25, 27, 31);">，该层是个简单的线形层，用于将原始输出结果映射成单一的 </font><font style="color:rgb(25, 27, 31);">Vt</font><font style="color:rgb(25, 27, 31);"> 值。</font>  


## Actor Model 策略模型<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
+ **<font style="color:rgb(51, 51, 51);">核心作用</font>**<font style="color:rgb(51, 51, 51);">：直接生成动作（action），即根据当前状态（输入）选择最优策略（如生成文本）。</font>
+ **<font style="color:rgb(51, 51, 51);">与LLM的关系</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:#ED740C;">Actor就是待训练的LLM本身</font>**<font style="color:rgb(51, 51, 51);">，负责根据输入（如用户提问）生成输出（如回复）。在强化学习中，Actor的生成策略会根据Critic和Reward Model的反馈不断调整。</font>
    - <font style="color:rgb(51, 51, 51);">训练目标是让Actor生成的文本最大化长期奖励（例如，生成更符合人类偏好的回答）。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：LLM在RLHF中作为Actor，通过策略梯度方法（如PPO）更新参数。</font>

:::

<font style="color:rgb(25, 27, 31);">我们的最终目的是让Actor模型能产生符合人类喜好的response。所以我们的策略是，</font>

1. <font style="color:rgb(25, 27, 31);">先喂给Actor一条prompt （这里假设batch_size = 1，所以是1条prompt），让它生成对应的response。</font>
2. <font style="color:rgb(25, 27, 31);">然后，我们再将“prompt + response"送入我们的“奖励-loss”计算体系中去</font>**<font style="color:#74B602;">算得最后的loss，用于更新actor。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743411395667-6f2d5580-0316-47a1-89db-baba755892ca.png)

## <font style="color:#1f2329;">Reward Model 奖励模型</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介：</font>**<font style="color:rgb(25, 27, 31);">在训练过程中，我们不能让人类对每一个 LLM 的响应进行评判，那太慢了。因此，我们训练一个奖励模型，</font>**<font style="color:#ED740C;">一个学习模仿人类偏好的人工智能裁判</font>**<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">奖励模型 = AI 品尝师</font>**<font style="color:rgb(25, 27, 31);">：我们在人类偏好数据上训练它。它学会给人类倾向于喜欢的文本赋予更高的分数。</font>
+ **<font style="color:rgb(25, 27, 31);">RL 算法使用奖励模型</font>**<font style="color:rgb(25, 27, 31);">：像 PPO、DPO 和 GRPO 这样的算法随后使用这个奖励模型来指导 LLM 的学习。LLM 试图生成能够从 AI 裁判那里获得高分的文本。</font>
+ **<font style="color:rgb(51, 51, 51);">核心作用</font>**<font style="color:rgb(51, 51, 51);">：提供即时的奖励信号（reward），量化当前动作（生成内容）的优劣。</font>
+ **<font style="color:rgb(51, 51, 51);">与LLM的关系</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:#ED740C;">Reward Model通常是一个独立训练的模型</font>**<font style="color:rgb(51, 51, 51);">，用于模仿人类对生成结果的偏好。例如，在RLHF中，它通过人类标注的偏好数据（如对多个回答的排序）训练，学习为“高质量文本”打高分，为“低质量文本”打低分。</font>
    - <font style="color:rgb(51, 51, 51);">在LLM训练中，Reward Model为Actor生成的每个回答提供</font>**<font style="color:rgb(51, 51, 51);">即时奖励</font>**<font style="color:rgb(51, 51, 51);">（如标量分数），指导Actor的优化方向。</font>
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：在RLHF中，Reward Model替代人类直接标注，为大规模训练提供自动化反馈。</font>

:::

<font style="color:rgb(25, 27, 31);">Reward Model用于计算生成token </font><font style="color:rgb(25, 27, 31);">At</font><font style="color:rgb(25, 27, 31);"> 的即时收益，它就是RW阶段所训练的奖励模型，在RLHF过程中，它的参数是冻结的。</font>

:::color5
**<font style="color:#601BDE;">1.为什么Critic模型要参与训练，而同样是和收益相关的Reward模型的参数就可以冻结呢？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">你可能想问：为什么Critic模型要参与训练，而同样是和收益相关的Reward模型的参数就可以冻结呢？</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">这是因为，Reward模型是站在上帝视角的。这个上帝视角有两层含义：</font>

+ <font style="color:rgb(25, 27, 31);">第一点，Reward模型是经过和“估算收益”相关的训练的，因此在RLHF阶段它可以直接被当作一个能产生客观值的模型。</font>
+ <font style="color:rgb(25, 27, 31);">第二点，Reward模型代表的含义就是“即时收益”，你的token </font><font style="color:rgb(25, 27, 31);">At</font><font style="color:rgb(25, 27, 31);"> 已经产生，因此即时收益自然可以立刻算出。</font>

:::color5
**<font style="color:#601BDE;">2.已经用Critic预测出</font>**<font style="color:#601BDE;"> </font><font style="color:#601BDE;">Vt</font><font style="color:#601BDE;"> </font>**<font style="color:#601BDE;">了，而这个</font>**<font style="color:#601BDE;"> </font><font style="color:#601BDE;">Vt</font><font style="color:#601BDE;"> </font>**<font style="color:#601BDE;">包含了“即时”和“未来”的概念，那我还需要代表“即时”的</font>**<font style="color:#601BDE;"> </font><font style="color:#601BDE;">Rt</font><font style="color:#601BDE;"> </font>**<font style="color:#601BDE;">做什么呢？直接用</font>**<font style="color:#601BDE;"> </font><font style="color:#601BDE;">Vt</font><font style="color:#601BDE;"> </font>**<font style="color:#601BDE;">不就好了吗？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">为了解答这个问题，我们先回顾下价值函数： </font><font style="color:rgb(25, 27, 31);">Vt=Rt+γVt+1</font><font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">这个函数告诉我们，我们当前可以用两个结果来表示 </font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> 时刻的总收益：</font>

+ <font style="color:rgb(25, 27, 31);">结果1：Critic模型预测的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);">t</font>
+ <font style="color:rgb(25, 27, 31);">结果2：Reward模型预测的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">R</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和critic模型预测的</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">+</font><font style="color:rgb(25, 27, 31);">1</font>

<font style="color:rgb(25, 27, 31);">那么哪一个结果更靠近上帝视角给出的客观值呢？当然是结果2，因为</font>**<font style="color:#74B602;">结果1全靠预测，而结果2中的 </font>****<font style="color:#74B602;">Rt</font>****<font style="color:#74B602;"> 是事实数据。</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">	我们知道Critic模型也是参与参数更新的，我们可以用</font>`**<font style="color:#74B602;background-color:rgb(248, 248, 250);">MSE(上帝视角的客观收益-Critic模型预测的收益)</font>**`**<font style="color:#74B602;">来衡量它的loss</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">但是上帝视角的客观收益我们是不知道的，只能用已知事实数据去逼近它，所以我们就用</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">Rt+γ∗Vt+1</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">来做近似。</font>****<font style="color:#74B602;">这就是 </font>****<font style="color:#74B602;">Rt,Vt</font>****<font style="color:#74B602;"> 同时存在的意义</font>**

<font style="color:rgb(25, 27, 31);">Reward模型和critic模型非常相似，这里我们就只给出架构图，不再做过多的说明。关于Reward模型的训练过程，后续有时间也会出个原理和代码解析。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743413150825-2801fe46-804e-428a-8c82-fc39d9778ff5.png)



:::color5
**<font style="color:#601BDE;">1.PRM & ORM</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**PRM (Process Reward Model)**

+  PRM 的目标是给**<font style="color:#74B602;">「推理过程」本身打分（reward）</font>**，比如给每一步的思路链、Chain-of-Thought 提供一个质量评价。
+  这意味着它更关注推理展开的细节：**<font style="color:#74B602;">是否逻辑连贯、中间步骤有没有硬伤</font>**等。
+  这种过程级评估非常符合「批判模型」或「验证器」的角色—它不仅看最终答案对不对，更会审查一系列中间步骤的合理性。

**ORM (Output Reward Model)**

+  ORM 则主要打分**<font style="color:#74B602;">「最终输出」（最后的答案或结论）的质量</font>**。
+  与 PRM 相比，ORM只看结果是否正确、合乎人类偏好或任务标准，而不深入逐步过程。
+  这种单一关注输出的评估模式，也可视为一种更「精简」的批判模型—它仍然在对主模型的推理结论进行审核。

## Refenrence Model 参考模型<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
+ **<font style="color:rgb(51, 51, 51);">核心作用</font>**<font style="color:rgb(51, 51, 51);">：作为基准模型，约束Actor的更新幅度，防止策略偏离初始分布过远。</font>
+ **<font style="color:rgb(51, 51, 51);">与LLM的关系</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:#ED740C;">Reference Model通常是未经RL训练的原始LLM</font>**<font style="color:rgb(51, 51, 51);">（例如预训练后的初始模型）。在RL训练中，通过计算Actor生成内容与Reference Model的KL散度（Kullback-Leibler Divergence），确保生成的文本</font>**<font style="color:rgb(51, 51, 51);">保持语言流畅性和多样性</font>**<font style="color:rgb(51, 51, 51);">，避免过度优化导致模式坍塌（如重复无意义的回答）。</font>
    - <font style="color:rgb(51, 51, 51);">在训练目标中，</font>**<font style="color:#ED740C;">KL散度作为正则化项，平衡奖励最大化和分布稳定性。</font>**
+ **<font style="color:rgb(51, 51, 51);">典型应用</font>**<font style="color:rgb(51, 51, 51);">：在PPO等算法中，Reference Model用于计算策略更新的约束项。</font>

:::

**<font style="color:rgb(25, 27, 31);">Reference Model（以下简称Ref模型）一般也用SFT阶段得到的SFT模型做初始化，在训练过程中，它的参数是冻结的。</font>**<font style="color:rgb(25, 27, 31);">Ref模型的主要作用是防止Actor”训歪”，那么它具体是怎么做到这一点的呢？</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743411768127-b040d498-b3c8-4904-88e6-0b819adba252.png)

:::color5
**<font style="color:#601BDE;">1.Refenrence Model 原理</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">“防止模型训歪”换一个更详细的解释是：</font>**<font style="color:rgb(25, 27, 31);">我们希望训练出来的Actor模型既能达到符合人类喜好的目的，又尽量让它和SFT模型不要差异太大</font>**<font style="color:rgb(25, 27, 31);">。简言之，</font>**<font style="color:rgb(25, 27, 31);">我们希望两个模型的输出分布尽量相似</font>**<font style="color:rgb(25, 27, 31);">。那什么指标能用来衡量输出分布的相似度呢？我们自然而然想到了</font>**<font style="color:rgb(25, 27, 31);">KL散度</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">如上图所示：</font>

+ **<font style="color:rgb(25, 27, 31);">对Actor模型</font>**<font style="color:rgb(25, 27, 31);">，我们喂给它一个prompt，它正常输出对应的response。那么response中每一个token肯定有它对应的log_prob结果呀，我们把这样的结果记为</font>**<font style="color:rgb(25, 27, 31);">log_probs</font>**
+ **<font style="color:rgb(25, 27, 31);">对Ref模型</font>**<font style="color:rgb(25, 27, 31);">，我们把Actor生成的"prompt + response"喂给它，那么它同样能给出每个token的log_prob结果，我们记其为</font>**<font style="color:rgb(25, 27, 31);">ref_log_probs</font>**
+ <font style="color:rgb(25, 27, 31);">那么这两个模型的输出分布相似度就可以用</font>`**<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ref_log_probs - log_probs</font>**`<font style="color:rgb(25, 27, 31);">来衡量，我们可以从两个方面来理解这个公式：</font>
    - **<font style="color:rgb(25, 27, 31);">从直觉上理解</font>**<font style="color:rgb(25, 27, 31);">，ref_log_probs越高，说明Ref模型对Actor模型输出的肯定性越大。即Ref模型也认为，对于某个</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">S</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，输出某个</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">A</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的概率也很高（</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">P</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">A</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">|</font><font style="color:rgb(25, 27, 31);">S</font><font style="color:rgb(25, 27, 31);">t</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">）。这时可以认为Actor模型较Ref模型没有训歪</font>
    - **<font style="color:rgb(25, 27, 31);">从KL散度上理解</font>**<font style="color:rgb(25, 27, 31);">， </font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743412240510-488758e3-5c0d-4a7f-82f8-ce00ceacad13.png)<font style="color:rgb(25, 27, 31);"> </font>

<font style="color:rgb(25, 27, 31);">（当然这里不是严格的等于，只是KL散度的近似），这个值越小意味着两个分布的相似性越高。</font>

# RLHF算法
:::color3
+ **<font style="color:rgb(51, 51, 51);">RL</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">是基础框架，</font>**<font style="color:rgb(51, 51, 51);">RLHF</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">和</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">DPO</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">是其扩展，专注于人类偏好对齐。</font>
+ **<font style="color:rgb(51, 51, 51);">PPO</font>**<font style="color:rgb(51, 51, 51);">是RLHF中策略优化的执行者，根据奖励模型提供的奖励更新策略参数。</font>
+ **<font style="color:rgb(51, 51, 51);">奖励模型</font>**<font style="color:rgb(51, 51, 51);"> 是RLHF的核心组件，将人类偏好量化为奖励信号。</font>

:::

| **<font style="color:rgb(25, 27, 31);">特性</font>** | **<font style="color:rgb(25, 27, 31);">PPO</font>** | **<font style="color:rgb(25, 27, 31);">DPO</font>** | **<font style="color:rgb(25, 27, 31);">GRPO</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">是否需要奖励模型</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">否</font> |
| <font style="color:rgb(25, 27, 31);">是否需要辅助教练（价值函数）</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">否</font> |
| <font style="color:rgb(25, 27, 31);">训练效率</font> | <font style="color:rgb(25, 27, 31);">中等</font> | <font style="color:rgb(25, 27, 31);">高</font> | <font style="color:rgb(25, 27, 31);">高</font> |
| <font style="color:rgb(25, 27, 31);">适用场景</font> | <font style="color:rgb(25, 27, 31);">通用</font> | <font style="color:rgb(25, 27, 31);">简单任务</font> | <font style="color:rgb(25, 27, 31);">复杂推理任务</font> |


## 策略优化方法
<font style="color:#1f2329;">策略优化⽅法直接优化智能体的策略，使其能够最⼤化累积回报。其核⼼思想是直接</font><font style="color:#d83931;">通过策略梯度⽅法更新参数，优化策略函数</font>

### <font style="color:#117CEE;">策略函数（Policy）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">在强化学习中，a</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);">∣s</font><sub><font style="color:rgb(25, 27, 31);">t </font></sub><font style="color:rgb(25, 27, 31);">表示在</font>[<font style="color:rgb(9, 64, 142);">状态</font>](https://zhida.zhihu.com/search?content_id=710831409&content_type=Answer&match_order=1&q=%E7%8A%B6%E6%80%81&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> s</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);"> 下采取</font>[<font style="color:rgb(9, 64, 142);">动作</font>](https://zhida.zhihu.com/search?content_id=710831409&content_type=Answer&match_order=1&q=%E5%8A%A8%E4%BD%9C&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> a</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);"> 的条件概率。具体来说，它是由策略函数 π 决定的。</font>**<font style="color:#ED740C;">在 PPO 中，这一概率用于计算新旧策略的比值，从而控制策略更新的幅度</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.详细说明</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318478190-54586c17-5420-4b55-a692-652e767180a9.png)

:::color5
**<font style="color:#601BDE;">2.举例说明</font>**

:::

假设我们有一个简单的游戏环境：

+  状态 <font style="color:rgb(25, 27, 31);">s</font><sub><font style="color:rgb(25, 27, 31);">t </font></sub> ：角色的位置。
+  动作 a<sub>t</sub> ：可以执行的动作是“向左”或“向右”。
+  策略 π(<font style="color:rgb(25, 27, 31);">a</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);">∣s</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub>) ：在某个位置 <font style="color:rgb(25, 27, 31);">s</font><sub><font style="color:rgb(25, 27, 31);">t </font></sub>下，策略可能以 70% 的概率选择“向左”，以 30% 的概率选择“向右”。

在 PPO 中，**<font style="color:#74B602;">我们会比较新旧策略在相同状态 s</font>**<sub>**<font style="color:#74B602;">t </font>**</sub>**<font style="color:#74B602;"> 下选择相同动作 a</font>**<sub>**<font style="color:#74B602;">t</font>**</sub>**<font style="color:#74B602;">  的概率，从而计算概率比 r</font>**<sub>**<font style="color:#74B602;">t</font>**</sub>**<font style="color:#74B602;">(θ) ，并用于优化目标函数。</font>**



### 优势函数 (Advantage)
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>Advantage函数用于衡量在某个状态（State）下，采取某个动作（Action）相对于平均表现的优劣程度。它的数学定义为： A(s,a)=Q(s,a)−V(s), 其中：

+ Q(s,a)是**动作值函数**，表示在状态 s 下采取动作 a 后，未来累积回报的期望。
+ V(s)  是**状态值函数**，表示在状态 s 下，按照当前策略采取动作后，**<font style="color:#ED740C;">未来累积回报的期望</font>**。
+ A(s,a)  是**优势函数**，表示在状态 s 下采取动作 a 比平均表现好多少（或差多少）。

:::

**<font style="color:rgb(25, 27, 31);">直观理解</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">Advantage函数就像“评分”</font>**<font style="color:rgb(25, 27, 31);">，告诉模型某个动作在当前状态下是好还是坏，以及好（或坏）的程度。</font>

在PPO等算法中，Advantage函数通常通过**<font style="color:#74B602;">GAE（Generalized Advantage Estimation）</font>**来估计。

:::color5
**<font style="color:#601BDE;">1.作用</font>**

:::

+ Advantage函数用于指导策略更新：
+ 如果 A(s,a)>0 A(s, a) > 0 ，说明动作 a a  比平均表现更好，策略应该更倾向于选择这个动作；
+ 如果 A(s,a)<0 A(s, a) < 0 ，说明动作 a a  比平均表现更差，策略应该减少选择这个动作的概率。

### 值函数 (V(s))
值函数 _V__π _(_s_)描述了在状态_s_下，按照策略_π  _⾏动时能够获得的期望累积回报。它反映了智能体在当前状态下的“好坏”，即从状态_s _开始，智能体期望未来能够获得的奖励总和。值函数的定义为：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739159549807-063a59cb-bf50-452f-bb07-b0a558232132.png)



### KL 散度
:::color3
**简介：**KL Penalty是基于**KL散度（Kullback-Leibler Divergence）**的一种正则化手段。KL散度用于衡量两个概率分布之间的差异。在强化学习中，KL Penalty通常**<font style="color:#ED740C;">用于限制当前策略 π</font>**<sub>**<font style="color:#ED740C;">θ</font>**</sub>**<font style="color:#ED740C;">和参考策略 π</font>**<sub>**<font style="color:#ED740C;">ref </font>**</sub>**<font style="color:#ED740C;">之间的差异</font>**。其数学定义为： KL Penalty=D<sub>KL</sub>(π<sub>ref</sub>‖π<sub>θ</sub>)  其中：

+ π<sub>θ</sub>是当前策略（由模型参数 θ决定）。
+ π<sub>ref </sub>是参考策略（通常是更新前的策略或某个基线策略）。
+ D<sub>KL</sub>是KL散度，用于衡量两个策略之间的差异。

:::

**<font style="color:rgb(25, 27, 31);">直观理解</font>**<font style="color:rgb(25, 27, 31);">：KL Penalty就像一个“约束”，告诉模型在更新策略时不要“步子迈得太大”，以免失去稳定性。</font>

:::color5
#### <font style="color:#601BDE;">1.作用</font>
:::

+ <font style="color:rgb(25, 27, 31);">KL Penalty</font>**<font style="color:#74B602;">用于防止策略更新过大，确保当前策略不会偏离参考策略太远</font>**<font style="color:rgb(25, 27, 31);">。这样可以避免训练过程中的不稳定现象（如策略崩溃）。</font>
+ <font style="color:rgb(25, 27, 31);">在PPO等算法中，KL Penalty通常被添加到目标函数中，作为正则化项。</font>

:::color5
#### <font style="color:#601BDE;">2.Advantage和KL Penalty的关系</font>
:::

+ **<font style="color:rgb(25, 27, 31);">Advantage</font>**<font style="color:rgb(25, 27, 31);"> 用于指导策略更新，告诉模型哪些动作更好。</font>
+ **<font style="color:rgb(25, 27, 31);">KL Penalty</font>**<font style="color:rgb(25, 27, 31);"> 用于约束策略更新，防止策略变化过大。</font>
+ <font style="color:rgb(25, 27, 31);">在PPO等算法中，Advantage和KL Penalty共同作用，既鼓励模型选择更好的动作，又确保更新过程稳定可靠。</font>

**举例说明**

假设我们训练一个机器人走迷宫：

+ **Advantage**：机器人发现“向右转”比“向左转”更容易找到出口，于是Advantage函数会给“向右转”一个正的值，**<font style="color:#74B602;">鼓励策略更倾向于选择“向右转”</font>**。
+ **KL Penalty**：为了防止策略突然变得只选择“向右转”而忽略其他可能性，**<font style="color:#74B602;">KL Penalty会限制策略的变化幅度，确保策略更新是平滑的</font>**。



### PPO（<font style="color:rgb(64, 64, 64);">Proximal Policy Optimization </font>）<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**PPO（ProximalPolicyOptimization，近端策略优化）是⼀种常⽤的强化学习算法，属于策略优化⽅法，**<font style="color:#ED740C;">是RLHF中策略优化的执行者，根据奖励模型提供的奖励更新策略参数</font>**。其核⼼思想是通过限制策略更新的幅度来提升训练的稳定性，避免策略在每次更新中发⽣较⼤变化，从⽽防⽌训练过程中的不稳定和策略崩溃。

参考：[图解大模型RLHF系列之：人人都能看懂的PPO原理与源码解读](https://zhuanlan.zhihu.com/p/677607581)

:::

**<font style="color:rgb(25, 27, 31);">PPO（Proximal Policy Optimization）</font>**<font style="color:rgb(25, 27, 31);"> 是一种用于强化学习的策略优化算法，由 </font>[<font style="color:rgb(9, 64, 142);">OpenAI</font>](https://zhida.zhihu.com/search?content_id=710831409&content_type=Answer&match_order=1&q=OpenAI&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 提出。</font>**<font style="color:#74B602;">它通过限制策略更新的幅度，确保训练过程的稳定性。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743411227505-2e7ff874-cac1-4444-b52e-bab4bafff841.png)

<font style="color:rgb(25, 27, 31);">如上图，</font>**<font style="color:rgb(25, 27, 31);">在RLHF-PPO阶段，一共有四个主要模型</font>**<font style="color:rgb(25, 27, 31);">，分别是：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

+ [**<font style="color:rgb(9, 64, 142);">Actor Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Actor+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：演员模型</font>**<font style="color:rgb(25, 27, 31);">，这就是我们想要训练的目标语言模型</font>
+ [**<font style="color:rgb(9, 64, 142);">Critic Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Critic+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：评论家模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是预估总收益</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);">t</font>
+ [**<font style="color:rgb(9, 64, 142);">Reward Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Reward+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：奖励模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是计算即时收益</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">R</font><font style="color:rgb(25, 27, 31);">t</font>
+ **<font style="color:rgb(25, 27, 31);">Reference Model：参考模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是在RLHF阶段给语言模型增加一些“约束”，防止语言模型训歪（朝不受控制的方向更新，效果可能越来越差）</font>

<font style="color:rgb(25, 27, 31);">其中:</font>

+ **<font style="color:rgb(25, 27, 31);">Actor/Critic Model</font>**<font style="color:rgb(25, 27, 31);">在RLHF阶段是</font>**<font style="color:rgb(25, 27, 31);">需要训练</font>**<font style="color:rgb(25, 27, 31);">的（图中给这两个模型加了粗边，就是表示这个含义）；而</font>**<font style="color:rgb(25, 27, 31);">Reward/Reference Model</font>**<font style="color:rgb(25, 27, 31);">是</font>**<font style="color:rgb(25, 27, 31);">参数冻结</font>**<font style="color:rgb(25, 27, 31);">的。</font>
+ <font style="color:rgb(25, 27, 31);">Critic/Reward/Reference Model共同组成了一个“奖励-loss”计算体系（我自己命名的，为了方便理解），我们综合它们的结果计算loss，用于更新Actor和Critic Model</font>

:::color5
#### <font style="color:#601BDE;">0.核心思想</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">PPO</font><font style="color:#1f2329;">通过⼀种</font><font style="color:#d83931;">剪辑损失函数（</font><font style="color:#d83931;">Clipped</font><font style="color:#d83931;">Surrogate</font><font style="color:#d83931;">Objective</font><font style="color:#d83931;">）</font><font style="color:#1f2329;">来实现策略的优化</font><font style="color:#1f2329;">，它的</font><font style="color:#2ea121;">⽬标是确保策</font>

<font style="color:#2ea121;">略更新时不会偏离当前策略太多。它克服了传统策略梯度⽅法</font><font style="color:#1f2329;">（如</font><font style="color:#1f2329;">TRPO</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">Trust Region Policy</font><font style="color:#1f2329;"> Optimization</font><font style="color:#1f2329;">）复杂的约束问题</font><font style="color:#1f2329;">，保持了性能的同时降低了实现难</font><font style="color:#1f2329;">度。</font>

<font style="color:#1f2329;">传统的策略优化⽬标是直接优化策略</font>_<font style="color:#1f2329;">π</font>__<font style="color:#1f2329;">θ</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，使得给定状态下的⾏为能够最⼤化累计奖励。</font><font style="color:#1f2329;">PPO</font><font style="color:#1f2329;">在此</font><font style="color:#1f2329;">基础上</font><font style="color:#1f2329;">，通过引⼊⼀个重要的⽐例项 </font><font style="color:#1f2329;">"</font><font style="color:#1f2329;">probability</font><font style="color:#1f2329;">ratio</font><font style="color:#1f2329;">"</font>_<font style="color:#1f2329;">r</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">来度量新旧策略之间的差异：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739167940952-02d9fc31-9544-4f84-ae56-1f41d5009ab0.png)

<font style="color:#1f2329;">其中，</font>_<font style="color:#1f2329;">π</font>__<font style="color:#1f2329;">θ</font>_<sub><font style="color:#1f2329;">old</font></sub><font style="color:#1f2329;">  是更新前的策略，⽽  </font>_<font style="color:#1f2329;">π</font>__<font style="color:#1f2329;">θ  </font>_<font style="color:#1f2329;">是更新后的策略。该⽐率表⽰在同⼀状态-⾏为对</font><font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t </font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">下，新旧策略选择该⾏为的概率之⽐。如果这个⽐率偏离1过多，说明更新后的策略与原始策略差异较⼤，可能会导致训练不稳定。</font>

:::color5
#### <font style="color:#601BDE;">1.PPO关键角色 </font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ **<font style="color:rgb(25, 27, 31);">策略（LLM）</font>**<font style="color:rgb(25, 27, 31);">：我们正在训练的 LLM，用于生成更好的文本。</font>
+ **<font style="color:rgb(25, 27, 31);">奖励模型</font>**<font style="color:rgb(25, 27, 31);">：根据人类偏好对文本打分的 AI 裁判。</font>
+ **<font style="color:rgb(25, 27, 31);">价值函数（辅助教练）</font>**<font style="color:rgb(25, 27, 31);">：另一个 AI 模型，充当“辅助教练”。它估计每个状态的“好坏”（当前文本生成的前景如何）。这有助于 PPO 进行更智能的更新。</font>

:::color5
#### <font style="color:#601BDE;">2.PPO训练步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

1. **<font style="color:rgb(25, 27, 31);">生成文本（Rollout）</font>**<font style="color:rgb(25, 27, 31);">：LLM（策略）为不同的提示生成大量文本样本。</font>
2. **<font style="color:rgb(25, 27, 31);">奖励模型打分</font>**<font style="color:rgb(25, 27, 31);">：奖励模型对每个文本样本进行打分。</font>
3. **<font style="color:rgb(25, 27, 31);">计算优势函数（广义优势估计</font>**[**<font style="color:rgb(9, 64, 142);">GAE</font>**](https://zhida.zhihu.com/search?content_id=254489057&content_type=Article&match_order=1&q=GAE&zhida_source=entity)**<font style="color:rgb(25, 27, 31);"> —— “好多少”分数）</font>**<font style="color:rgb(25, 27, 31);">：这就是 GAE 的作用！它是一种巧妙的方法，用于计算每个单词选择的优劣，考虑奖励和价值函数的预测。</font>
4. **<font style="color:rgb(25, 27, 31);">优化 LLM（策略更新）</font>**<font style="color:rgb(25, 27, 31);">：我们更新 LLM 的策略，以最大化一个特殊的 PPO 目标函数。这个目标函数现在有三个关键部分：</font>
    - **<font style="color:rgb(25, 27, 31);">鼓励更高奖励</font>**<font style="color:rgb(25, 27, 31);">：它推动 LLM 生成能够获得更高分数的文本。</font>
    - **<font style="color:rgb(25, 27, 31);">限制策略变化（剪切代理目标）</font>**<font style="color:rgb(25, 27, 31);">：它防止策略在一次更新中变化过大，确保稳定性。</font>
    - **<font style="color:rgb(25, 27, 31);">KL 散度惩罚</font>**<font style="color:rgb(25, 27, 31);">：如果新策略与旧策略偏离太远，它会增加惩罚，进一步增强稳定性。</font>
    - **<font style="color:rgb(25, 27, 31);">熵奖励</font>**<font style="color:rgb(25, 27, 31);">：它还包括一个熵奖励。简单来说，熵衡量 LLM 文本生成的“随机性”或“多样性”。增加熵奖励可以鼓励 LLM 更多地探索，而不是总是生成相同、可预测的响应。它有助于防止 LLM 过早变得“过于确定”，从而错过可能更好的策略。</font>
5. **<font style="color:rgb(25, 27, 31);">更新价值函数（辅助教练更新）</font>**<font style="color:rgb(25, 27, 31);">：训练价值函数成为一个更好的“辅助教练”——更准确地预测不同文本生成的“好坏”。</font>

:::color5
#### <font style="color:#601BDE;">3.损失函数</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">PPO的损失函数是基于策略⽐率</font>_<font style="color:#1f2329;">r</font>_<sub>_<font style="color:#1f2329;">t</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">进⾏定义的，它有两种主要形式：</font><font style="color:#2ea121;">剪辑形式</font><font style="color:#1f2329;">和</font><font style="color:#2ea121;">KL散度形式</font><font style="color:#1f2329;">。</font>

1. **<font style="color:#1f2329;">剪辑损失函数</font>**<font style="color:#1f2329;">：它通过对策略更新的⽐率进⾏剪辑来避免策略⼤幅度更新。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739168127764-ee2268cb-48e8-4264-9a98-c3cb6de17cc1.png)

2. **基于KL散度的PPO**：<font style="color:#1f2329;">KL散度⽤于度量新旧策略分布的差异，通常定义为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739168140722-4d78b942-5dbc-4c33-a2b9-f6533f57a9a9.png)

:::color5
#### <font style="color:#601BDE;">4.优势函数At的估计(Advantage)    GAE（广义优势估计）</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">在PPO中 ，优势函数</font>_<font style="color:#1f2329;">A</font>_<sup>_<font style="color:#1f2329;">t</font>_</sup><sup>_<font style="color:#1f2329;"> </font>_</sup>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">的准确估计对策略的优化效果⾄关重要。</font>

<font style="color:#1f2329;">通常</font><font style="color:#1f2329;">，优势函数被定义为当前策略相对于基准策略的相对表现：</font>_<font style="color:#1f2329;">A</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">=</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">−</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">V</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">其中：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font>_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">是给定状态和⾏为下的动作值函数</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，表</font><font style="color:#1f2329;">⽰采取动作</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;">  </font>_<font style="color:#1f2329;">后的预期回报；</font>

<font style="color:#1456f0;">•  </font>_<font style="color:#1f2329;">V </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t </font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">是状态值函数 ，表⽰在状态 </font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t  </font>_<font style="color:#1f2329;">下的预期回报。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739168798867-dadb2d0c-de65-47b9-beca-a2cffac8775b.png)

**<font style="color:rgb(25, 27, 31);">为什么选择 GAE？（蒙特卡洛与时间差分 —— 方差与偏差）</font>**

+ **<font style="color:rgb(25, 27, 31);">蒙特卡洛（MC）—— 高方差，低偏差</font>**<font style="color:rgb(25, 27, 31);">：想象一下等到整个文本生成后再获得奖励，然后将该奖励分配给文本中的每一个单词。就像只有在小狗完成整个“坐下、待命、取回”动作序列后才给予奖励。对整个序列的奖励是准确的，但对单个动作（“坐下”与“待命”与“取回”）的信号非常嘈杂。高方差，学习速度慢。</font>
+ **<font style="color:rgb(25, 27, 31);">时间差分（TD）—— 低方差，高偏差</font>**<font style="color:rgb(25, 27, 31);">：想象一下在每个单词生成后给予奖励。“好单词！”“普通单词！”“很棒的单词！”信号不那么嘈杂，学习速度更快。但是，我们只是局部地判断单词，没有考虑整个文本的长期质量。可能会有偏差，可能会错过“大局”。</font>
+ **<font style="color:rgb(25, 27, 31);">GAE —— 平衡</font>**<font style="color:rgb(25, 27, 31);">：广义优势估计（GAE）就像“多步 TD”。它考虑了多个步骤（单词）上的奖励，平衡了方差（MC）与偏差（TD）之间的权衡。就像不仅在结束时给予奖励，还在价值函数预测的指导下，为沿途的“小步骤”给予奖励。</font>

:::color5
#### <font style="color:#601BDE;">5.优缺点</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

**优点**

+ <font style="color:#1f2329;">更新稳定：通过剪辑⽐率或KL散度约束，PPO限制了每次更新的幅度，</font><font style="color:#d83931;">防⽌策略发⽣剧烈变化，从⽽提⾼了算法的稳定性</font><font style="color:#1f2329;">。</font>
+ <font style="color:#1f2329;">与TRPO相⽐，PPO⽆需复杂的约束优化算法，易于实现和调整超参数。</font>
+ <font style="color:#1f2329;">适用性强：PPO适⽤于离散和连续动作空间，⼴泛应⽤于各种强化学习任务。</font>

**<font style="color:rgb(64, 64, 64);">缺点</font>**<font style="color:rgb(64, 64, 64);">：</font>

+ <font style="color:rgb(64, 64, 64);">PPO 中的</font>_**<font style="color:rgb(64, 64, 64);">值函数通常是一个与策略模型大小相当的模型</font>**_<font style="color:rgb(64, 64, 64);">，</font>_**<font style="color:#DF2A3F;">这带来了显著的内存和计算负担</font>**_<font style="color:rgb(64, 64, 64);">。</font>
+ <font style="color:rgb(64, 64, 64);">在 LLMs 的上下文中，值函数在训练过程中被用作优势计算中的Baseline，但通常只有最后一个 token 会被奖励模型赋予奖励分数，这可能使得值函数的训练变得复杂。</font>

:::color5
#### <font style="color:#601BDE;">6.代码实现</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def ppo_loss_with_gae_entropy(old_policy_logprobs, new_policy_logprobs, advantages, kl_penalty_coef, clip_epsilon, entropy_bonus_coef):
    """概念性 PPO 损失函数，带有 GAE 和熵奖励（简化版）。"""

    ratio = np.exp(new_policy_logprobs - old_policy_logprobs)  # 概率比

    # 剪切代理目标（限制策略变化）
    surrogate_objective = np.minimum(ratio * advantages, np.clip(ratio, 1 - clip_epsilon, 1 + clip_epsilon) * advantages)
    policy_loss = -np.mean(surrogate_objective)

    # KL 散度惩罚（保持接近旧策略）
    kl_divergence = np.mean(new_policy_logprobs - old_policy_logprobs)
    kl_penalty = kl_penalty_coef * kl_divergence

    # 熵奖励（鼓励探索）
    entropy = -np.mean(new_policy_logprobs)  # 简化版熵（概率越高 = 熵越低，取负值以最大化熵）
    entropy_bonus = entropy_bonus_coef * entropy

    total_loss = policy_loss + kl_penalty - entropy_bonus  # 减去熵奖励，因为我们希望*最大化*熵
    return total_loss
```

```python
import tensorflow as tf
import gym
import numpy as np

class PPO:
    def __init__(self, env, hidden_size=64, batch_size=64, clip_ratio=0.2, learning_rate=1e-4):
        self.env = env
        self.batch_size = batch_size
        self.clip_ratio = clip_ratio

        # 定义神经网络
        self.actor = self.build_actor(hidden_size)
        self.critic = self.build_critic(hidden_size)

        self.optimizer_actor = tf.keras.optimizers.Adam(learning_rate)
        self.optimizer_critic = tf.keras.optimizers.Adam(learning_rate)

    def build_actor(self, hidden_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_size, activation='relu'),
            tf.keras.layers.Dense(self.env.action_space.n, activation='softmax')
        ])
        return model

    def build_critic(self, hidden_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_size, activation='relu'),
            tf.keras.layers.Dense(1, activation='linear')
        ])
        return model

    def get_action(self, state):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        action_probs = self.actor(state)
        action = tf.random.categorical(tf.math.log(action_probs), 1)
        return action.numpy()[0]

    def compute_value(self, state):
        state = tf.convert_to_tensor(state, dtype=tf.float32)
        return self.critic(state)

    def train(self, num_episodes=1000, max_steps=2000):
        for episode in range(num_episodes):
            trajectories = []
            state = self.env.reset()
            episode_reward = 0
            for step in range(max_steps):
                action = self.get_action(state)
                next_state, reward, done, _ = self.env.step(self.env.actions[action])
                trajectories.append((state, action, reward, next_state, done))
                episode_reward += reward
                state = next_state
                if done:
                    break

            # 将轨迹转为Tensor
            states = tf.convert_to_tensor([t[0] for t in trajectories], dtype=tf.float32)
            actions = tf.convert_to_tensor([t[1] for t in trajectories], dtype=tf.int32)
            rewards = tf.convert_to_tensor([t[2] for t in trajectories], dtype=tf.float32)
            next_states = tf.convert_to_tensor([t[3] for t in trajectories], dtype=tf.float32)
            dones = tf.convert_to_tensor([t[4] for t in trajectories], dtype=tf.float32)

            # 计算V值和下一个V值
            vs = self.critic(states)
            next_vs = self.critic(next_states)
            # 计算优势
            advantages = rewards + (1 - dones) * self.gamma * next_vs - vs

            # 策略概率
            old_p = self.actor(tf.convert_to_tensor(states, dtype=tf.float32))
            old_p = tf.gather(old_p, actions, batch_dims=1)
            old_p = tf.stop_gradient(old_p)

            with tf.GradientTape() as actor_tape:
                new_p = self.actor(tf.convert_to_tensor(states, dtype=tf.float32))
                new_p = tf.gather(new_p, actions, batch_dims=1)
                ratio = tf.exp(tf.math.log(new_p + 1e-10) - tf.math.log(old_p + 1e-10))
                clip_ratio = tf.clip_by_value(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
                loss_actor = tf.reduce_mean(-tf.minimum(ratio * advantages, clip_ratio * advantages))

            with tf.GradientTape() as critic_tape:
                current_v = self.critic(tf.convert_to_tensor(states, dtype=tf.float32))
                loss_critic = tf.reduce_mean((rewards + tf.stop_gradient(advantages)) - current_v)

            # 更新Actor
            gradients_actor = actor_tape.gradient(loss_actor, self.actor.trainable_weights)
            self.optimizer_actor.apply_gradients(zip(gradients_actor, self.actor.trainable_weights))

            # 更新Critic
            gradients_critic = critic_tape.gradient(loss_critic, self.critic.trainable_weights)
            self.optimizer_critic.apply_gradients(zip(gradients_critic, self.critic.trainable_weights))

            print(f"Episode {episode}, Reward: {episode_reward}")

        print("Training completed.")

```



#### PPO实践：<font style="color:rgb(51, 51, 51);">基于PPO的Qwen商品问答助手训练</font>
:::color3
**<font style="color:rgb(51, 51, 51);"></font>****<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：训练商品问答助手在电商场景中生成符合以下要求的回答：</font>

+ <font style="color:rgb(51, 51, 51);">准确性（商品参数正确）</font>
+ <font style="color:rgb(51, 51, 51);">合规性（不出现虚假宣传）</font>
+ <font style="color:rgb(51, 51, 51);">用户友好性（语言自然流畅）</font>
+ <font style="color:rgb(51, 51, 51);">价值观对齐（环保/伦理等声明需谨慎）</font>

**<font style="color:rgb(51, 51, 51);">技术框架</font>**<font style="color:rgb(51, 51, 51);">：PPO（Proximal Policy Optimization）为核心算法，整合四大模型实现RLHF（基于人类反馈的强化学习）</font>

:::

:::color5
**<font style="color:#601BDE;">1.4个模型实现</font>**

:::

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">1. Critic Model（价值模型）</font>**

+ **项目中的角色**：
    - **<font style="color:#74B602;">评估当前对话状态的价值</font>**<font style="color:rgb(51, 51, 51);">（预测未来累计奖励）</font>
    - <font style="color:rgb(51, 51, 51);">在PPO的</font>**<font style="color:rgb(51, 51, 51);">优势函数计算</font>**<font style="color:rgb(51, 51, 51);">中起关键作用</font>
    - <font style="color:rgb(51, 51, 51);">示例：当用户询问"有机棉T恤的环保性如何？"时，Critic会评估当前回答是否可能引发后续追问（如认证标准细节）</font>
+ **实现细节**：

```python
# 输入：当前对话状态（编码后的文本+历史记录）
# 输出：价值估计标量
class Critic(nn.Module):
    def forward(self, state_emb):
        return self.value_head(state_emb)  # [batch_size, 1]
```

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">2. Actor Model（策略模型）</font>**

+ **项目中的角色**：
    - <font style="color:rgb(51, 51, 51);">作为</font>**<font style="color:rgb(51, 51, 51);">可优化策略</font>**<font style="color:rgb(51, 51, 51);">生成回答</font>
    - <font style="color:rgb(51, 51, 51);">通过PPO更新逐步改进回答质量</font>
    - <font style="color:rgb(51, 51, 51);">示例：在生成"这款T恤通过GOTS认证"时，动态调整专业术语的使用比例</font>
+ **实现细节**：

```python
# 输入：用户问题文本
# 输出：回答的概率分布
class Actor(nn.Module):
    def forward(self, input_ids):
        logits = self.lm_head(input_ids)  # 语言模型输出
        return Categorical(logits=logits)
```

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">3. Reward Model（奖励模型）</font>**

+ **项目中的角色**：
    - <font style="color:rgb(51, 51, 51);">提供多维奖励信号：</font>
        * **<font style="color:rgb(51, 51, 51);">基础奖励</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#74B602;">回答相关性（BERTScore）</font>**
        * **<font style="color:rgb(51, 51, 51);">安全奖励</font>**<font style="color:rgb(51, 51, 51);">：敏感词检测（如"绝对无害"等绝对化表述）</font>
        * **<font style="color:rgb(51, 51, 51);">价值观奖励</font>**<font style="color:rgb(51, 51, 51);">：环保声明验证（连接商品数据库校验）</font>
    - <font style="color:rgb(51, 51, 51);">示例：对回答"采用零污染工艺"触发数据库核查，若未找到认证则扣分</font>
+ **奖励函数设计**：

```python
def calculate_reward(response):
    safety = 1 - 0.2*contains_risk_terms(response) 
    accuracy = bertscore(query, response) 
    value_alignment = check_certifications(response) 
    return 0.4*safety + 0.5*accuracy + 0.1*value_alignment
```

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">4. Reference Model（参考模型）</font>**

+ **项目中的角色**：
    - <font style="color:rgb(51, 51, 51);">作为</font>**<font style="color:rgb(51, 51, 51);">冻结的初始策略</font>**<font style="color:rgb(51, 51, 51);">（</font>**<font style="color:#74B602;">SFT微调后的Qwen基础模型</font>**<font style="color:rgb(51, 51, 51);">）</font>
    - <font style="color:rgb(51, 51, 51);">通过KL散度约束防止过度优化导致语言不自然</font>
    - <font style="color:rgb(51, 51, 51);">示例：当PPO策略开始生成过度正式的回答时，通过KL惩罚保持口语化风格</font>
+ **约束实现**：

```python
# 计算当前策略与参考策略的KL散度
kl_penalty = kl_div(
    F.log_softmax(actor_logits, dim=-1),
    F.log_softmax(ref_model_logits, dim=-1)
).mean()
```

:::color5
**<font style="color:#601BDE;">2.训练过程</font>**

:::

1. **初始化阶段**：
    - <font style="color:rgb(51, 51, 51);">Reference Model：加载经过监督微调（SFT）的Qwen-7B</font>
    - <font style="color:rgb(51, 51, 51);">Actor：克隆Reference Model参数作为初始策略</font>
    - <font style="color:rgb(51, 51, 51);">Critic：独立训练的价值网络</font>
    - <font style="color:rgb(51, 51, 51);">Reward Model：基于人工标注的10万条对比回答对训练</font>
2. **数据收集**：
    - <font style="color:rgb(51, 51, 51);">采样流程：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741675218636-212cda94-487c-49be-92dd-a308ee71b54e.png)

3. **PPO迭代训练**：
    - <font style="color:rgb(51, 51, 51);">关键更新步骤：</font>

```python
# 计算优势函数
advantages = rewards + gamma * critic(next_states) - critic(states)

# PPO损失计算
ratio = (actor_logprob - old_logprob).exp()
surr1 = ratio * advantages
surr2 = torch.clamp(ratio, 1-eps, 1+eps) * advantages
policy_loss = -torch.min(surr1, surr2) + beta * kl_penalty
```

:::color5
**<font style="color:#601BDE;">3.关键维度对比</font>**

:::

| **维度** | **Critic** | **Actor** | **Reward Model** | **Reference Model** |
| --- | --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">更新频率</font>** | <font style="color:rgb(51, 51, 51);">每个PPO迭代更新</font> | <font style="color:rgb(51, 51, 51);">主更新对象</font> | <font style="color:rgb(51, 51, 51);">预训练后冻结</font> | <font style="color:rgb(51, 51, 51);">完全冻结</font> |
| **<font style="color:rgb(51, 51, 51);">项目中的数据依赖</font>** | <font style="color:rgb(51, 51, 51);">环境交互轨迹</font> | <font style="color:rgb(51, 51, 51);">PPO梯度更新</font> | <font style="color:rgb(51, 51, 51);">人工标注的偏好数据</font> | <font style="color:rgb(51, 51, 51);">SFT训练数据</font> |
| **<font style="color:rgb(51, 51, 51);">显存占用</font>** | <font style="color:rgb(51, 51, 51);">约2GB（独立网络）</font> | <font style="color:rgb(51, 51, 51);">约14GB（7B模型）</font> | <font style="color:rgb(51, 51, 51);">约7GB（冻结）</font> | <font style="color:rgb(51, 51, 51);">约7GB（冻结）</font> |
| **<font style="color:rgb(51, 51, 51);">失败案例干预</font>** | <font style="color:rgb(51, 51, 51);">价值估计偏差导致收敛慢</font> | <font style="color:rgb(51, 51, 51);">生成不合规内容</font> | <font style="color:rgb(51, 51, 51);">奖励黑客攻击</font> | <font style="color:rgb(51, 51, 51);">KL约束过强导致创新性下降</font> |


:::color5
**<font style="color:#601BDE;">4.实际部署挑战</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">Reward Model的偏差控制</font>**<font style="color:rgb(51, 51, 51);">：需定期用新标注数据更新，防止模型利用奖励漏洞（如添加无意义环保术语刷分）</font>
2. **<font style="color:rgb(51, 51, 51);">Critic的价值过估计</font>**<font style="color:rgb(51, 51, 51);">：采用Double Critic架构和周期性延迟更新</font>
3. **<font style="color:rgb(51, 51, 51);">Reference Model的滞后性</font>**<font style="color:rgb(51, 51, 51);">：每季度更新一次参考模型以吸收新知识</font>
4. **<font style="color:rgb(51, 51, 51);">多目标权衡</font>**<font style="color:rgb(51, 51, 51);">：通过动态奖励加权（如促销期间适当提升销售话术权重）</font>

<font style="color:rgb(51, 51, 51);">通过这种架构，Qwen商品问答助手在测试中实现了：</font>

+ **<font style="color:rgb(51, 51, 51);">回答准确率</font>**<font style="color:rgb(51, 51, 51);">提升27%（相比纯SFT）</font>
+ **<font style="color:rgb(51, 51, 51);">合规违规率</font>**<font style="color:rgb(51, 51, 51);">下降至0.3%</font>
+ **<font style="color:rgb(51, 51, 51);">用户满意度</font>**<font style="color:rgb(51, 51, 51);">达到92.7%</font>

## <font style="color:rgb(64, 64, 64);">Q-Learning</font>
:::color3
<font style="color:#1f2329;">简介：Q-Learning 算法通过学习最优的</font><font style="color:#de7802;">动作值函数 </font>_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;">来间接优化策略，它不直接优化策略，⽽是通过值函数指导动作选择。</font>

:::

**<font style="color:rgb(51, 51, 51);">1. 概述：</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">Q-Learning是一种基于值的强化学习算法，用于学习最优策略，适用于离散动作空间。它通过更新Q值表（或使用神经网络近似）来选择最优动作。</font>

**<font style="color:rgb(51, 51, 51);">2. 实现步骤：</font>**

**<font style="color:rgb(51, 51, 51);">步骤一：定义环境</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">创建一个简单的环境类，提供状态空间、动作空间和步行动作的接口。</font>

**<font style="color:rgb(51, 51, 51);">步骤二：初始化Q-Learning参数</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">初始化Q网络或其他函数逼近器，设置学习率和折扣因子等。</font>

```python
import numpy as np
from collections import deque
import gym

class QLearning:
    def __init__(self, env, gamma=0.99, learning_rate=0.01, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.999):
        self.env = env
        self.gamma = gamma
        # 初始化Q值表 (状态空间大小，动作空间大小)
        self.q_table = np.zeros((env.observation_space.high.size * 2 + 1, env.action_space.n))
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def train(self, num_episodes=1000, max_steps=2000):
        for episode in range(num_episodes):
            state = self.env.reset()
            total_reward = 0
            for step in range(max_steps):
                # 选择动作
                if np.random.random() < self.epsilon:
                    action = self.env.action_space.sample()
                else:
                    # 将连续状态离散化处理
                    state_scaled = (state - (-1)) / 2  # 假设状态范围是[-1,1]
                    state_index = tuple(map(int, state_scaled))
                    action = np.argmax(self.q_table[state_index])
                
                # 执行动作，获取下一个状态和奖励
                next_state, reward, done, _ = self.env.step(self.env.actions[action])
                # 更新Q值
                next_state_scaled = (next_state - (-1)) / 2
                next_state_index = tuple(map(int, next_state_scaled))
                q_next = self.q_table[next_state_index][np.argmax(self.q_table[next_state_index])]
                q_current = self.q_table[state_index][action]
                self.q_table[state_index][action] = q_current + self learning_rate * (reward + self.gamma * q_next - q_current)
                
                total_reward += reward
                state = next_state
                if done:
                    break

            # 策略贪心下降
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            print(f"Episode {episode}, Reward: {total_reward}")

        print("Training completed.")

# 示例使用（假设一个简单的环境，比如CartPole）
env = gym.make('CartPole-v0')
ql = QLearning(env)
ql.train()

```

  




## <font style="color:rgb(53, 53, 53);">DPO</font>
:::color3
**简介**<font style="color:#1f2329;">：DirectPreferenceOptimization (DPO) 是⼀种新的强化学习算法，特别设计⽤于解决偏好学习</font><font style="color:#1f2329;">（Preference Learning）问题。</font><font style="color:rgb(51, 51, 51);">可视为RLHF的简化变体，省去了</font>**<font style="color:#ED740C;">奖励模型训练环节</font>**<font style="color:rgb(51, 51, 51);">，</font>**<font style="color:#de7802;">核⼼思想是通过优化⽤户或专家给定的偏好信号，⽽⾮直接优化奖励函数</font>**<font style="color:#de7802;">。</font>

**参考：**[https://zhuanlan.zhihu.com/p/27332009509](https://zhuanlan.zhihu.com/p/27332009509)

:::

**核心思想**：<font style="color:rgb(25, 27, 31);">DPO 就像是直接告诉 LLM：“响应 A 比响应 B 更好。多生成像 A 这样的响应，少生成像 B 这样的响应！”它省略了 RL 中用于策略优化的奖励模型这一中间环节</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739169076873-0a688045-7da4-4706-bb72-e2432e14f928.png)

### <font style="color:#1f2329;">原理</font>
:::color5
#### <font style="color:#601BDE;">1.训练步骤</font>
:::

1. **<font style="color:rgb(25, 27, 31);">偏好数据仍然是关键</font>**<font style="color:rgb(25, 27, 31);">：与 PPO 一样，DPO 仍然从相同的关键成分开始：人类偏好数据（成对的响应，带有标签，指示哪个响应更受青睐）。人类反馈仍然是基础！</font>
2. **<font style="color:rgb(25, 27, 31);">直接策略更新（分类式损失——直接使用 logits！）</font>**<font style="color:rgb(25, 27, 31);">：这是 DPO 的魔法所在。DPO </font>**<font style="color:#74B602;">使用一个特殊的损失函数直接比较两个模型的 logits</font>**<font style="color:rgb(25, 27, 31);">（概率之前的原始输出分数）：</font>
    - **<font style="color:rgb(25, 27, 31);">当前模型（正在训练中）</font>**<font style="color:rgb(25, 27, 31);">：我们将首选响应（响应 A）和非首选响应（响应 B）都输入到我们正在训练的当前 LLM 中，得到两者的 logits。</font>
    - **<font style="color:rgb(25, 27, 31);">参考模型（旧版本）</font>**<font style="color:rgb(25, 27, 31);">：我们还将响应 A 和响应 B 输入到一个参考模型中。这通常是 LLM 的旧版本（比如我们开始时的 SFT 模型）。我们也会从参考模型中得到 logits。</font>
    - <font style="color:rgb(25, 27, 31);">DPO 的损失函数直接</font>**<font style="color:#74B602;">使用这两个模型的 logits 来计算损失</font>**<font style="color:rgb(25, 27, 31);">，这与分类任务中使用的二元交叉熵损失非常相似。这个损失函数旨在：</font>
        * **<font style="color:rgb(25, 27, 31);">增加首选响应的 logits（和概率）</font>**<font style="color:rgb(25, 27, 31);">：让当前模型在未来更有可能生成像响应 A 这样的响应。</font>
        * **<font style="color:rgb(25, 27, 31);">减少非首选响应的 logits（和概率）</font>**<font style="color:rgb(25, 27, 31);">：让当前模型在未来更不可能生成像响应 B 这样的响应。</font>
        * **<font style="color:rgb(25, 27, 31);">保持接近参考模型（隐式 KL 控制）</font>**<font style="color:rgb(25, 27, 31);">：损失函数还隐式地鼓励当前模型在行为上保持与参考模型的接近（使用参考模型的 logits），这有助于稳定性，类似于 PPO 的 KL 惩罚，但直接嵌入在损失函数中！</font>

:::color5
#### <font style="color:#601BDE;">2.偏好模型建立 Bradley-Terry Model</font>
:::

<font style="color:rgb(25, 27, 31);">Bradley–Terry model被用于对事物间的比较关系进行建模，比如说棋类比赛，棋手之间往往互有胜负，Bradley–Terry model可以根据这些胜负信息去为所有的职业棋手建模，为他们赋予一个内在的“分数”，通过这个分数可以一定程度上反应棋手的水平，并预测两个棋手之间对局的胜负概率。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741681327077-8e842277-0475-48c3-b7a4-7f17a29a620f.png)

<font style="color:rgb(25, 27, 31);">以上是模型对目标 </font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 的比较（或者胜负）关系的建模， </font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);"> 是 </font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 的内在分数， </font><font style="color:rgb(25, 27, 31);">P(i>j)</font><font style="color:rgb(25, 27, 31);"> 是 </font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);"> 优于 </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 的概率。</font>

**<font style="color:#74B602;">在RLHF场景下，Bradley–Terry model可以用来对人类偏好进行建模。 </font>****<font style="color:#74B602;">β</font>****<font style="color:#74B602;"> 是我们希望Reward Model对于每条样本计算出的模型返回的内在分数，而结果 </font>****<font style="color:#74B602;">P</font>****<font style="color:#74B602;"> 代表了人类偏好的概率</font>**<font style="color:rgb(25, 27, 31);">。在实际当中，我们会收集到标注员对样本间两两比较的结果，我们会使用</font>**<font style="color:#74B602;">最大似然估计 Maximum likelihood estimation</font>**<font style="color:rgb(25, 27, 31);">去优化Reward Model，使RM得到的分数对样本间比较结果的预测最大程度上和训练数据保持一致。</font>

:::color5
#### <font style="color:#601BDE;">3.偏好比较</font>
:::

<font style="color:#1f2329;">为了优化偏好模型，DPO ⾸先需要定义偏好的⽐较⽅式。在给定⼀对动作 </font><font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">i</font>_</sub><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">j </font>_</sub><font style="color:#1f2329;">)</font><font style="color:#1f2329;">和状态</font>_<font style="color:#1f2329;">s </font>_<font style="color:#1f2329;">的情况   下，模型需要判断哪个动作更被偏好。这可以通过定义⼀个偏好⽐较函数</font>_<font style="color:#1f2329;">P</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">i </font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">≻ </font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">j</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">，</font>**<font style="color:#d83931;">即在状态</font>**_**<font style="color:#1f2329;">s </font>**_**<font style="color:#d83931;">下，动作</font>**_**<font style="color:#1f2329;">a</font>**_<sub>_**<font style="color:#1f2329;">i</font>**_</sub>_**<font style="color:#1f2329;"> </font>**_**<font style="color:#d83931;">相较于</font>**_**<font style="color:#1f2329;">a</font>**_<sub>_**<font style="color:#1f2329;">j</font>**_</sub>_**<font style="color:#1f2329;"> </font>**_**<font style="color:#d83931;">更被偏好的概率</font>**<font style="color:#1f2329;">。该概率可以通过偏好模型计算得到：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739167079623-7b923bea-d6d2-41bd-b5cd-2bc7f2d26bc3.png)

<font style="color:#1f2329;">这个公式是通过 softmax 函数得出的，表⽰在两个动作之间，哪个更有可能被偏好。</font>

:::color5
#### <font style="color:#601BDE;">4.损失函数</font>
:::

<font style="color:#1f2329;">为了训练偏好模型，DPO 使⽤了基于</font>**<font style="color:#ED740C;">⼆元交叉熵的损失函数</font>**<font style="color:#1f2329;">。这⼀损失函数旨在最⼩化模型预测偏好与实际⽤⼾（或专家）偏好之间的差异。</font>

<font style="color:rgb(25, 27, 31);">可以这样理解：</font>**<font style="color:#74B602;">DPO 的损失函数就像一个“偏好指南针”，直接根据首选和非首选响应的相对 logits 指导 LLM 的权重，而无需显式预测奖励。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739170478873-a3f6923e-acf8-45dd-85e0-a0b715ca4620.png)

<font style="color:#1f2329;">这个损失函数的⽬的是使模型对</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">+和</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">− 的评分差尽可能⼤，从⽽确保模型更倾向于选择</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">+作为偏好选项。</font>**<font style="color:#2ea121;background-color:#f0fbef;">通过最⼩化这个损失函数，偏好模型会不断调整其参数，使得预测出的偏好分布越来越接近真实的⽤户偏好分布。</font>**

:::color5
#### <font style="color:#601BDE;">5.策略优化</font>
:::

<font style="color:#1f2329;">通过学习到的偏好模型</font>_<font style="color:#1f2329;">P</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">，我们可以将其⽤于⽣成策略</font>_<font style="color:#1f2329;">π</font>_<sub>_<font style="color:#1f2329;">θ</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">。DPO 的策略优化过程直接依赖 于偏好模型，即策略的概率分布可以通过偏好模型的 softmax 输出进⾏参数化：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739167383799-dd59e4e2-551d-4979-8634-8ec0ad621766.png)

<font style="color:#1f2329;">这意味着 DPO 的策略优化并不依赖于传统的奖励信号，⽽是完全基于偏好信号进⾏优化。通过优化偏好损失函数，我们可以间接优化策略的性能，使其更符合⽤户的期望。</font>

:::color5
#### <font style="color:#601BDE;">6.优缺点</font>
:::

**<font style="color:rgb(13, 18, 57);">优点</font>**

1. **<font style="color:rgb(13, 18, 57);">高效性</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">绕过奖励建模</font>**<font style="color:rgb(13, 18, 57);">：DPO无需显式训练奖励模型（Reward Model），直接通过偏好数据优化策略，减少了训练流程的复杂性。</font>
    - **<font style="color:rgb(13, 18, 57);">计算成本低</font>**<font style="color:rgb(13, 18, 57);">：传统RLHF需要交替优化奖励模型和策略（如PPO），而DPO通过闭式解直接优化目标函数，降低了计算开销。</font>
2. **<font style="color:rgb(13, 18, 57);">稳定性</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">避免强化学习的不稳定性</font>**<font style="color:rgb(13, 18, 57);">：PPO等算法需要精细的超参数调优，而DPO基于监督学习框架，训练过程更稳定，不易出现策略崩溃（policy collapse）。</font>
3. **<font style="color:rgb(13, 18, 57);">实现简单</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">代码复杂度低</font>**<font style="color:rgb(13, 18, 57);">：仅需对损失函数进行梯度优化（类似分类任务），无需实现复杂的强化学习逻辑（如价值函数、重要性采样等）。</font>

**<font style="color:rgb(13, 18, 57);">缺点</font>**

1. **<font style="color:rgb(13, 18, 57);">对偏好数据的强依赖</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">数据质量敏感</font>**<font style="color:rgb(13, 18, 57);">：DPO直接依赖成对偏好数据（如正/负样本对），若数据存在噪声或偏见，模型可能继承这些缺陷。</font>
    - **<font style="color:rgb(13, 18, 57);">数据量需求</font>**<font style="color:rgb(13, 18, 57);">：需要大量高质量的偏好标注数据，成本较高，且可能受限于标注者的主观偏好。</font>
2. **<font style="color:rgb(13, 18, 57);">理论假设限制</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">基于Bradley-Terry模型</font>**<font style="color:rgb(13, 18, 57);">：假设人类偏好仅由两个选项的奖励差值决定，无法建模更复杂的偏好关系（如多选项排序或上下文相关偏好）。</font>
    - **<font style="color:rgb(13, 18, 57);">无法处理非对称偏好</font>**<font style="color:rgb(13, 18, 57);">：例如，若用户更喜欢“短回答”但标注者更关注“准确性”，DPO可能难以平衡两者。</font>
3. **<font style="color:rgb(13, 18, 57);">对参考模型的依赖</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">参考模型的质量影响结果</font>**<font style="color:rgb(13, 18, 57);">：DPO的损失函数基于参考模型（通常为初始SFT模型）的输出分布，若参考模型性能较差，可能限制最终模型的表现。</font>
4. **<font style="color:rgb(13, 18, 57);">扩展性挑战</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">大规模数据效率</font>**<font style="color:rgb(13, 18, 57);">：当偏好数据规模极大时，DPO的计算效率可能下降，而传统RLHF通过预训练奖励模型可部分缓解这一问题。</font>

:::color5
#### <font style="color:#601BDE;">6.代码实现</font>
:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def dpo_loss(policy_logits_preferred, policy_logits_dispreferred, ref_logits_preferred, ref_logits_dispreferred, beta_kl):
    """概念性 DPO 损失函数（简化版——直接使用 logits）。"""

    # 1. 从 logits 中获取对数概率（当前和参考模型的首选和非首选响应）
    policy_logprob_preferred = F.log_softmax(policy_logits_preferred, dim=-1).gather(...)  # 提取首选响应中实际标记的对数概率
    policy_logprob_dispreferred = F.log_softmax(policy_logits_dispreferred, dim=-1).gather(...)  # 提取非首选响应中实际标记的对数概率
    ref_policy_logprob_preferred = F.log_softmax(ref_logits_preferred, dim=-1).gather(...)  # 同样适用于参考模型
    ref_policy_logprob_dispreferred = F.log_softmax(ref_logits_dispreferred, dim=-1).gather(...)

    # 2. 计算对数比率（使用对数概率——如前所述）
    log_ratio = policy_logprob_preferred - policy_logprob_dispreferred - (ref_policy_logprob_preferred - ref_policy_logprob_dispreferred)

    # 3. 偏好概率（Bradley-Terry 模型——隐式奖励信号）
    preference_prob = 1 / (1 + np.exp(-beta_kl * log_ratio))

    # 4. 二元交叉熵损失（直接优化策略）
    dpo_loss = -np.log(preference_prob + 1e-8)
    return dpo_loss
```

### <font style="color:#1f2329;">偏好学习与传统强化学习区别</font>
<font style="color:#1f2329;">传统的强化学习通过最⼤化累积奖励来训练策略</font>

:::color3
<font style="color:#1f2329;">然⽽</font>**<font style="color:#d83931;">在 DPO 中，⽬标是最⼤化偏好模型的准确性，⽽不是累积奖励</font>**<font style="color:#d83931;">。</font><font style="color:#1f2329;">因此，DPO 并不直接依赖环境   提供的奖励信号，⽽是通过优化偏好⽐较损失函数</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;">来训练策略。这种优化过程更符合⼈类偏好的决策⽅式。</font>

:::

### <font style="color:#1f2329;">扩展与优化</font>
<font style="color:#1f2329;">为了提⾼DPO 的效率和稳定性，常见的优化技术包括：</font>

1. **<font style="color:#117CEE;">偏好采样策略</font>**<font style="color:#1f2329;">：通过经验回放池采样不同的偏好⽐较对，确保训练样本的多样性。</font>
2. **<font style="color:#117CEE;">策略约束</font>**<font style="color:#1f2329;">：类似于 PPO（Proximal Policy Optimization）中的剪切策略，通过限制每次策略更新的</font>

<font style="color:#1f2329;">幅度来避免过度更新，保证训练的稳定性。</font>

### <font style="color:#1f2329;">DPO与PPO/RLHF的对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**传统 RLHF 流程:  **

人类偏好数据 → 训练 Reward Model → PPO 优化策略 → 最终策略

**DPO 流程:  **

人类偏好数据 → 直接优化策略（隐式定义奖励） → 最终策略

:::

:::color5
#### <font style="color:#601BDE;">1.PPO/RLHF步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

1. **<font style="color:rgb(25, 27, 31);">训练 </font>**[**<font style="color:rgb(9, 64, 142);">reward model</font>**](https://zhida.zhihu.com/search?content_id=237414431&content_type=Article&match_order=1&q=reward+model&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：训练数据是同一个 prompt 的 2 个回答，让人或 </font>[<font style="color:rgb(9, 64, 142);">GPT4</font>](https://zhida.zhihu.com/search?content_id=237414431&content_type=Article&match_order=1&q=GPT4&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 标注哪个回答更好，reward model 会去优化如下的 loss：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741676118461-abbf8b53-017a-4e99-9fdb-44853020d533.png)**     （1）**

<font style="color:rgb(25, 27, 31);">其中 </font><font style="color:rgb(25, 27, 31);">r</font><sub><font style="color:rgb(25, 27, 31);">ϕ</font></sub><font style="color:rgb(25, 27, 31);"> 就是 reward model 用来给回答打分。</font><font style="color:rgb(25, 27, 31);">D</font><font style="color:rgb(25, 27, 31);"> 是训练数据集，</font><font style="color:rgb(25, 27, 31);">x</font><font style="color:rgb(25, 27, 31);"> 是 prompt，</font><font style="color:rgb(25, 27, 31);">y</font><sub><font style="color:rgb(25, 27, 31);">win</font></sub><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">y</font><sub><font style="color:rgb(25, 27, 31);">lose</font></sub><font style="color:rgb(25, 27, 31);"> 分别是好的回答和不好的回答。也就是说，要尽可能</font>**<font style="color:#74B602;">让好的回答的得分比不好的回答高</font>**<font style="color:rgb(25, 27, 31);">，拉大他们之间的差别。</font>

2. <font style="color:rgb(25, 27, 31);">第二步是用 RL 算法来提升模型的得分。使用的 loss 是：</font>

      ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741676192460-51bb0326-cdfc-48a0-b364-02a8629bf0d2.png)**（2）**  
<font style="color:rgb(25, 27, 31);">其中 </font><font style="color:rgb(25, 27, 31);">π</font><sub><font style="color:rgb(25, 27, 31);">θ</font></sub><font style="color:rgb(25, 27, 31);"> 是我们在训练的 LLM，</font><font style="color:rgb(25, 27, 31);">π</font><sub><font style="color:rgb(25, 27, 31);">ref</font></sub><sub><font style="color:rgb(25, 27, 31);"> </font></sub><font style="color:rgb(25, 27, 31);">是训练的初始值。</font>**<font style="color:#74B602;">这个 loss （偏好loss + KL散度loss）意思是希望 LLM 输出的回答的评分能尽可能高，同时 </font>****<font style="color:#74B602;">π</font>**<sub>**<font style="color:#74B602;">θ</font>**</sub>**<font style="color:#74B602;"> 不要偏离 </font>****<font style="color:#74B602;">π</font>**<sub>**<font style="color:#74B602;">ref</font>**</sub><sub>**<font style="color:#74B602;"> </font>**</sub>**<font style="color:#74B602;">太多，保证它还能正常做回答</font>**<font style="color:rgb(25, 27, 31);">，不要训成一个评分很高但是回答乱码的东西。</font>

:::color5
#### <font style="color:#601BDE;">2.DPO步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(25, 27, 31);">DPO 的作者们意识到，上述公式（2）是有显式解的。DPO 通过公式转换</font>**<font style="color:#ED740C;">把 RLHF 无损地转化为了 SFT</font>**<font style="color:rgb(25, 27, 31);">，在训练的时候</font>**<font style="color:#ED740C;">不再需要同时跑 4 个模型（reward model, ref model, critic, actor），而是只用跑 actor 和 ref 2 个模型</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
#### <font style="color:#601BDE;">3.目标和应用场景对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ <font style="color:#1f2329;">PPO是⼀种⽤于强化学习的</font><font style="color:#d83931;">策略优化算法</font><font style="color:#1f2329;">。其⽬的是通过与环境交互，</font><font style="color:#d83931;">在累计⻓期奖励的基础上优化策略</font><font style="color:#1f2329;">。PPO主要⽤于训练智能体如何通过连续的动作获得最⼤的累计奖励。</font>
+ <font style="color:#1f2329;">DPO是⼀种</font><font style="color:#245bdb;">偏好优化算法</font><font style="color:#1f2329;">，主要⽤于偏好学习任务（如⼤模型的偏好微调）。</font><font style="color:#245bdb;">它的⽬标是通过直接从⼈类偏好数据中优化策略，使得输出更加符合⽤户偏好</font><font style="color:#1f2329;">，⽽不是通过显式的奖励模型进⾏优化。</font>

:::color5
#### <font style="color:#601BDE;">4.优化目标对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ <font style="color:#d83931;">PPO通过限制策略更新的幅度，来保证策略的稳定性，避免策略发⽣过⼤的变化。其⽬标函数通过引⼊⼀个剪辑函数来实现这⼀点。</font><font style="color:#1f2329;"></font>
+ <font style="color:#245bdb;">DPO跳过了显式奖励模型的训练过程，直接从偏好数据中优化策略。</font><font style="color:#1f2329;">它的⽬标函数是最⼤化偏好分布下的对数似然</font>

:::color5
#### <font style="color:#601BDE;">5.应用任务对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ <u><font style="color:#d83931;">PPO 适⽤于典型的强化学习任务</font></u><font style="color:#1f2329;">，如在游戏环境中训练智能体、机器⼈控制等。PPO算法通常在  奖励信号稀疏的情况下表现出⾊，通过不断交互  和调整策略，逐步提⾼累计奖励。</font>
+ <u><font style="color:#245bdb;">DPO 更适⽤于偏好学习任务</font></u><font style="color:#1f2329;">，如在⼤型语⾔模型上进⾏⼈类偏好微调。它不需要通过环境交互来  优化，⽽是通过⼈类提供的偏好数据直接优化⽣  成模型的输出。相⽐于PPO的强化学习场景，</font>

<font style="color:#1f2329;">DPO避免了复杂的奖励模型构建。</font>

| **<font style="color:rgb(51, 51, 51);">维度</font>** | **<font style="color:rgb(51, 51, 51);">PPO + Reward Model</font>** | **<font style="color:rgb(51, 51, 51);">DPO</font>** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">是否需要 Reward Model</font>** | <font style="color:rgb(51, 51, 51);">是（显式训练）</font> | <font style="color:rgb(51, 51, 51);">否（隐式通过偏好数据定义奖励）</font> |
| **<font style="color:rgb(51, 51, 51);">优化目标</font>** | <font style="color:rgb(51, 51, 51);">最大化 Reward Model 的预测奖励</font> | <font style="color:rgb(51, 51, 51);">直接最大化人类偏好的似然</font> |
| **<font style="color:rgb(51, 51, 51);">计算复杂度</font>** | <font style="color:rgb(51, 51, 51);">高（需策略采样、奖励模型推理、PPO 更新）</font> | <font style="color:rgb(51, 51, 51);">低（类似监督学习，单阶段优化）</font> |
| **<font style="color:rgb(51, 51, 51);">潜在问题</font>** | <font style="color:rgb(51, 51, 51);">Reward Hacking（策略利用奖励模型漏洞）</font> | <font style="color:rgb(51, 51, 51);">依赖偏好数据的质量和覆盖度</font> |
| **<font style="color:#1f2329;">⽬标函数</font>** | <font style="color:#1f2329;">最⼤化⻓期奖励</font><font style="color:#1f2329;">，加⼊</font><font style="color:#1f2329;">KL</font><font style="color:#1f2329;">约</font><font style="color:#1f2329;">束和剪裁机制</font> | <font style="color:#1f2329;">最⼤化⼈类偏好</font><font style="color:#1f2329;">，直接优化策</font><font style="color:#1f2329;">略不需要显式奖励模型</font> |
| **<font style="color:#1f2329;">适⽤场景</font>** | <font style="color:#1f2329;">强化学习</font><font style="color:#1f2329;">，智能体交互场景</font> | <font style="color:#1f2329;">偏好学习</font><font style="color:#1f2329;">，语⾔模型微调等</font> |
| **<font style="color:#1f2329;">策略更新⽅式</font>** | <font style="color:#1f2329;">基于剪裁的策略⽐率更新</font> | <font style="color:#1f2329;">基于</font><font style="color:#1f2329;">KL</font><font style="color:#1f2329;">散度和⼈类偏好直接</font><font style="color:#1f2329;">调整策略</font> |
| **<font style="color:#1f2329;">优化⽅法</font>** | <font style="color:#1f2329;">通过策略梯度法更新</font> | <font style="color:#1f2329;">通过对数似然优化偏好数据下</font><font style="color:#1f2329;">的策略</font> |


### <font style="color:#1f2329;">DPO实践：LLM中偏好数据收集与正负样本构建</font>
:::color5
#### <font style="color:#601BDE;">1.数据收集</font>
:::

<font style="color:#1f2329;">我们可以通过以下步骤来收集偏好数据：</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">模型⽣成候选对话回复：给定⼀个⽤⼾输⼊（如⽤⼾问题或聊天对话），⽣成模型会给出多种候选回复。假设⽤⼾输⼊是：</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⽤⼾输⼊：</font><font style="color:#1f2329;">“</font><font style="color:#1f2329;">天⽓怎么样？</font><font style="color:#1f2329;">”</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">模型⽣成的两条回复分别为：</font>

<font style="color:#1456f0;">i.</font><font style="color:#1456f0;">   </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">1</font><font style="color:#1f2329;">：“</font><font style="color:#1f2329;">今天的天⽓⾮常好</font><font style="color:#1f2329;">，晴朗⽆云。</font><font style="color:#1f2329;">”</font>

<font style="color:#1456f0;">ii.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">2</font><font style="color:#1f2329;">：</font><font style="color:#1f2329;">“</font><font style="color:#1f2329;">不清楚天⽓</font><font style="color:#1f2329;">，您可以查⼀下天⽓预报。</font><font style="color:#1f2329;">”</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">⼈类反馈：接下来，系统会展⽰这两条回复给⼈类评审员。评审员基于回复的⾃然性、相关性、信息量等⽅⾯，选择其中更符合⽤⼾需求的回复。例如，评审员选择了回复1，因为它更加具体且回  答了⽤⼾的问题。</font>

:::color5
#### <font style="color:#601BDE;">2.偏好数据生成</font>
:::

<font style="color:#1f2329;">根据⼈类评审员的选择，我们得到如下的偏好数据：</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">回复1 ≻ 回复2 ，即回复1被评为更优</font>

:::color5
#### <font style="color:#601BDE;">3.构造正负样本</font>
:::

<font style="color:#1f2329;">根据评审员的反馈，构造正负样本：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">正样本：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">1</font><font style="color:#1f2329;">作为正样本</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，因为它更符合⽤⼾的偏好。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">负样本：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">2</font><font style="color:#1f2329;">作为负样本</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，因为它被评为相对较差的回复。</font>

<font style="color:#1f2329;">这对正负样本可以⽤于DPO的训练，其中模型将被优化为更倾向于⽣成类似回复1的答案，⽽抑制⽣成回复2这样的回答。</font>

:::color5
#### <font style="color:#601BDE;">4.多轮对话扩展</font>
:::

<font style="color:#1f2329;">在多轮对话系统中，⽤⼾不仅对单个回复进⾏评估，还可以对⼀段完整的对话进⾏反馈。此时，系统可以根据⽤户与模型交互过程中整段对话的质量进⾏偏好标注。</font>

<font style="color:#2ea121;">例如，⽤户对整个对话中的某⼀轮次的回复给予正向反馈（如点赞或正⾯评价），那么该轮次中的回复可以作为正样本，其他候选可以作为负样本。</font>

:::color5
#### <font style="color:#601BDE;">5.使用反馈模型优化</font>
:::

<font style="color:#1f2329;">通过收集⼤量类似的偏好数据，模型能够不断改进⽣成的质量。在DPO的框架下，模型通过最⼤化偏好模型对正负样本的预测准确率，逐步优化输出结果，使其更符合⼈类偏好。</font>

```python
import tensorflow as tf
import gym
import numpy as np

class DPO:
    def __init__(self, env, hidden_size=64, batch_size=64, discount_rate=0.99, learning_rate=1e-4):
        self.env = env
        self.batch_size = batch_size
        self.gamma = discount_rate

        # 初始化策略网络
        self.policy = self.build_policy(hidden_size)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate)

    def build_policy(self, hidden_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_size, activation='relu'),
            tf.keras.layers.Dense(self.env.action_space.n, activation='softmax')
        ])
        return model

    def get_action(self, state):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        action_probs = self.policy(state)
        action = tf.random.categorical(tf.math.log(action_probs), 1)
        return action.numpy()[0]

    def compute_loss(self, states, actions, rewards, next_states, dones):
        # 计算当前策略的概率
        old_p = self.policy(tf.convert_to_tensor(states, dtype=tf.float32))
        old_p = tf.gather(old_p, actions, batch_dims=1)
        old_p = tf.stop_gradient(old_p)

        new_p = self.policy(tf.convert_to_tensor(states, dtype=tf.float32))
        new_p = tf.gather(new_p, actions, batch_dims=1)

        # 计算优势 (可以使用更复杂的基线估计)
        V = self.value(tf.convert_to_tensor(states, dtype=tf.float32))  # 假设self.value是已有的价值函数
        next_V = self.value(tf.convert_to_tensor(next_states, dtype=tf.float32))
        advantages = rewards + self.gamma * next_V - V

        # 损失函数
        ratio = tf.exp(tf.math.log(new_p + 1e-10) - tf.math.log(old_p + 1e-10))
        loss = -tf.reduce_mean(tf.minimum(ratio * advantages, 1.0 * advantages))

        return loss

    def train(self, num_episodes=1000, max_steps=2000):
        for episode in range(num_episodes):
            trajectories = []
            state = self.env.reset()
            episode_reward = 0
            for step in range(max_steps):
                action = self.get_action(state)
                next_state, reward, done, _ = self.env.step(self.env.actions[action])
                trajectories.append((state, action, reward, next_state, done))
                episode_reward += reward
                state = next_state
                if done:
                    break

            # 转换为张量
            states = tf.convert_to_tensor([t[0] for t in trajectories], dtype=tf.float32)
            actions = tf.convert_to_tensor([t[1] for t in trajectories], dtype=tf.int32)
            rewards = tf.convert_to_tensor([t[2] for t in trajectories], dtype=tf.float32)
            next_states = tf.convert_to_tensor([t[3] for t in trajectories], dtype=tf.float32)
            dones = tf.convert_to_tensor([t[4] for t in trajectories], dtype=tf.float32)

            # 计算损失
            with tf.GradientTape() as tape:
                loss = self.compute_loss(states, actions, rewards, next_states, dones)

            gradients = tape.gradient(loss, self.policy.trainable_weights)
            self.optimizer.apply_gradients(zip(gradients, self.policy.trainable_weights))

            print(f"Episode {episode}, Reward: {episode_reward}")

        print("Training completed.")

```

## <font style="color:#000000;">GRPO（G</font><font style="color:rgb(64, 64, 64);">roup Relative Policy Optimization</font>）
:::color3
**简介**：<font style="color:rgb(64, 64, 64);">在DeepSeek-R1模型中，使用到的强化学习算法GRPO其实是DeepSeek之前的文章</font>_**<font style="color:rgb(64, 64, 64);">《DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models》</font>**_

<font style="color:rgb(64, 64, 64);">在目前大语言模型中进行微调的流程中，一般在SFT阶段之后，进一步通过强化学习对模型进行优化可以显著提升其性能。而</font>**<font style="color:rgb(64, 64, 64);">Group Relative Policy Optimization (GRPO)，就是使用在该阶段，替换传统的PPO算法。</font>**

**参考资料**：[DeepSeek的GRPO算法是什么？](https://www.zhihu.com/question/10766825126/answer/88583863333)

**源码实现**：[https://github.com/huggingface/open-r1/blob/main/src/open_r1/rewards.py](https://github.com/huggingface/open-r1/blob/main/src/open_r1/rewards.py)

**代码实现：**[GRPO核心代码实践](https://zhuanlan.zhihu.com/p/23349133287)

:::

GRPO 是一种在线学习算法（online learning algorithm），这意味着它通过使用训练过程中由训练模型自身生成的数据来迭代改进。GRPO 的目标直觉是最大化生成补全（completions）的优势函数（advantage），同时确保模型保持在参考策略（reference policy）附近。

<font style="color:rgb(25, 27, 31);">GRPO 就像是 PPO 的精简版。</font>**<font style="color:#74B602;">它保留了 PPO 的核心思想，但去掉了独立的价值函数（辅助教练），使其更轻量、更快速。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741320312999-67b4d632-0a3e-488f-a925-100da4b84ae8.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. <font style="color:rgb(25, 27, 31);">重要性采样是GRPO的核心机制：通过复用旧策略的样本，用重要性权重</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318225466-daf74867-a20b-48f4-aeb3-d16b300241be.png)<font style="color:rgb(25, 27, 31);">调整新策略的优化方向。</font>
2. <font style="color:rgb(25, 27, 31);">优势函数的作用：标准化后的奖励 </font><font style="color:rgb(25, 27, 31);">Ai</font><font style="color:rgb(25, 27, 31);"> 帮助策略区分高价值样本和低价值样本，引导模型优先提升高奖励输出的概率。</font>
3. <font style="color:rgb(25, 27, 31);">GRPO的工程优势：省去Critic价值模型，仅依赖组内奖励统计量，适合资源受限的场景。</font>

:::color5
**<font style="color:#601BDE;">2.与DPO/PPO的区别</font>**

:::

| **<font style="color:rgb(25, 27, 31);">特性</font>** | **<font style="color:rgb(25, 27, 31);">PPO</font>** | **<font style="color:rgb(25, 27, 31);">DPO</font>** | **<font style="color:rgb(25, 27, 31);">GRPO</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">是否需要奖励模型</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">是</font> |
| <font style="color:rgb(25, 27, 31);">是否需要辅助教练（价值函数）</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">否</font> |
| <font style="color:rgb(25, 27, 31);">训练效率</font> | <font style="color:rgb(25, 27, 31);">中等</font> | <font style="color:rgb(25, 27, 31);">高</font> | <font style="color:rgb(25, 27, 31);">高</font> |
| <font style="color:rgb(25, 27, 31);">适用场景</font> | <font style="color:rgb(25, 27, 31);">通用</font> | <font style="color:rgb(25, 27, 31);">简单任务</font> | <font style="color:rgb(25, 27, 31);">复杂推理任务</font> |


**<font style="color:#74B602;">为了解决PPO的缺点</font>**<font style="color:rgb(64, 64, 64);">，我们提出了 </font>**<font style="color:rgb(64, 64, 64);">Group Relative Policy Optimization (GRPO)</font>**<font style="color:rgb(64, 64, 64);">，不再需要像PPO那样加入额外的价值函数近似</font>_**<font style="color:rgb(64, 64, 64);">，而是直接使用多个采样输出的平均奖励作为Baseline</font>**_<font style="color:rgb(64, 64, 64);">，显著减少了训练资源的使用。</font>

**<font style="color:rgb(64, 64, 64);">GRPO与PPO的关联与区别：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812555603-dbee0aac-d740-44a1-9f32-60f3ef699f3a.png)

1. <font style="color:rgb(25, 27, 31);">PPO通常依赖一个独立的价值模型（Critic）来估计优势 </font><font style="color:rgb(25, 27, 31);">Ai</font><font style="color:rgb(25, 27, 31);">，需要额外训练一个模型。</font>
2. <font style="color:rgb(25, 27, 31);">GRPO的创新点：直接使用组内样本的奖励计算基线（如 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318126920-e319b774-623c-4c5c-9e45-829567f9719b.png)<font style="color:rgb(25, 27, 31);">），无需Critic模型，降低了计算成本。</font>
3. **<font style="color:rgb(25, 27, 31);">GRPO 直接比较候选响应的群体，无需额外的批评者模型</font>**<font style="color:rgb(25, 27, 31);">。对于给定的问题 q，GRPO 首先从当前策略 πθold 生成 G 个不同的响应 {o1, o2, ..., oG}。然后 GRPO 根据这些响应采取行动，并将获得的奖励表示为 {r1, r2, ..., rG}。通过计算它们的均值和标准差进行归一化，GRPO 确定这些响应的相对质量：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335086191-20af6668-2361-421b-a820-49700da58c3c.png)

<font style="color:rgb(25, 27, 31);">其中 Ai 表示第 i 个答案的相对质量。</font>**<font style="color:#ED740C;">GRPO 鼓励模型偏好群体内奖励值较高的更好答案</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.训练步骤（简化版）</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">生成一组响应</font>**<font style="color:rgb(25, 27, 31);">：对于每个提示，从 LLM 中生成多个响应的一组。</font>
2. **<font style="color:rgb(25, 27, 31);">对组进行打分（奖励模型）</font>**<font style="color:rgb(25, 27, 31);">：获取组内所有响应的奖励分数。</font>
3. **<font style="color:rgb(25, 27, 31);">计算组内相对优势（GRAE，基于组的优势骨架）</font>**<font style="color:rgb(25, 27, 31);">：通过比较每个响应的奖励与组内平均奖励来计算优势。在组内对奖励进行归一化以得到优势。</font>
    1. <font style="color:rgb(25, 27, 31);">GRPO 的魔法成分在于它如何估计优势。</font>**<font style="color:#74B602;">它不是使用辅助教练，而是使用一组由 LLM 生成的相同提示的响应来估计每个响应相对于组内其他响应的“好坏”</font>**<font style="color:rgb(25, 27, 31);">。</font>
4. **<font style="color:rgb(25, 27, 31);">优化策略（使用 GRAE 的 PPO 风格目标函数）</font>**<font style="color:rgb(25, 27, 31);">：使用一个 PPO 风格的目标函数更新 LLM 的策略，但使用这些组内相对优势。</font>

:::color5
**<font style="color:#601BDE;">4.实现步骤</font>**

:::

为了理解 GRPO 的工作原理，可以将其分解为四个主要步骤：

1. ** 生成补全（Generating completions）**

<font style="color:rgb(25, 27, 31);">在每一个训练步骤中，我们从提示（prompts）中采样一个批次（batch），并为每个提示生成一组 G 个补全（completions）（记为 o</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><font style="color:rgb(25, 27, 31);">）。</font>

2. ** 计算优势值（Computing the advantage）**

<font style="color:rgb(25, 27, 31);">对于每一个 G 序列，使用奖励模型（reward model）计算其奖励（reward）。为了与奖励模型的比较性质保持一致。通常奖励模型是基于同一问题的输出之间的比较数据集进行训练的。优势的计算反映了这些相对比较。其归一化公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327572180-c8af0f92-d170-4f1f-8c7a-4e9f796b8734.png)

<font style="color:rgb(25, 27, 31);">这种方法赋予了该方法其名称：</font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（Group Relative Policy Optimization, GRPO）</font>**

GRPO通过优化PPO算法，解决了**<font style="color:#74B602;">计算优势值时需要同时依赖奖励模型（reward model）和价值模型（value model）的问题，成功移除了value model（价值模型）</font>**，**<font style="color:#ED740C;">显著降低了推理时的内存占用和时间开销</font>**。**<font style="color:#ED740C;">Advantage（优势值）的核心价值在于为模型输出提供更精准的评估</font>**，不仅衡量答案的绝对质量，还通过相对比较（与其他回答的对比）来更全面地定位其优劣。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812555603-dbee0aac-d740-44a1-9f32-60f3ef699f3a.png)

3. ** 估计KL散度（Estimating the KL divergence）**

在实际算法实现中，直接计算KL散度可能会面临一些挑战：

+ **计算复杂度高**：KL散度的定义涉及对两个概率分布的对数比值的期望计算。对于复杂的策略分布，直接计算KL散度可能需要大量的计算资源；
+ **数值稳定性**：在实际计算中，直接计算KL散度可能会遇到数值不稳定的问题，尤其是当两个策略的概率分布非常接近时，对数比值可能会趋近于零或无穷大。近似器可以通过引入一些数值稳定性的技巧（如截断或平滑）来避免这些问题；
+ **在线学习**：在强化学习中，策略通常需要在每一步或每几步更新一次。如果每次更新都需要精确计算KL散度，可能会导致训练过程变得非常缓慢。近似器可以快速估计KL散度，从而支持在线学习和实时更新。

**使用近似器来估计KL散度**

[Schulman et al. (2020)](https://link.zhihu.com/?target=http%3A//joschu.net/blog/kl-approx.html)<font style="color:rgb(25, 27, 31);"> 提出的</font>**<font style="color:#ED740C;">近似器</font>**<font style="color:rgb(25, 27, 31);">可以根据当前策略和参考策略的差异动态调整估计的精度，从而在保证计算效率的同时，尽可能减少估计误差，其定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327720687-37130509-39b0-441a-939c-99d21b3325cc.png)

<font style="color:rgb(25, 27, 31);">这个近似器的优势在于它只需要</font>**<font style="color:#ED740C;">计算当前策略和参考策略的概率比值，而不需要直接计算KL散度的积分或期望。因此，它可以在保证一定精度的同时，显著降低计算复杂度。</font>**

4. ** 计算损失（Computing the loss）**

<font style="color:rgb(25, 27, 31);">这一步的目标是最大化优势，同时确保模型保持在参考策略附近。因此，损失定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327776028-b54b4f85-952c-4d47-abed-9fc4141d541e.png)

<font style="color:rgb(25, 27, 31);">其中第一项表示缩放后的优势，第二项通过KL散度惩罚与参考策略的偏离。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**优点**

1. 效率：GRPO无价值网络，相比PPO显存需求降低，训练速度提升。
2. 稳定性：GRPO组内相对优势减少方差，KL约束更惊喜，稳定性更高
3. 超参数敏感性：GRPO动态梯度正则化降低超参数敏感性
4. 扩展性：GRPO支持多任务联合优化，组内比较提升多样性

**缺点**

1. 适用动作空间：GRPO更依赖组内样本多样性，离散动作生产成本较高
2. 样本质量依赖：GRPO组内样本质量差时（如标准菜为0），优势估计时效

:::color5
**<font style="color:#601BDE;">4.伪代码实现</font>**

:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def grae_advantages(rewards):
    """概念性组相对优势估计（结果监督）。"""
    mean_reward = np.mean(rewards)
    std_reward = np.std(rewards)
    normalized_rewards = (rewards - mean_reward) / (std_reward + 1e-8)
    advantages = normalized_rewards  # 对于结果监督，优势 = 归一化奖励
    return advantages


def grpo_loss(old_policy_logprobs_group, new_policy_logprobs_group, group_advantages, kl_penalty_coef, clip_epsilon):
    """概念性 GRPO 损失函数（对一组响应取平均）。"""
    group_loss = 0
    for i in range(len(group_advantages)):  # 遍历组内的每个响应
        advantage = group_advantages[i]
        new_policy_logprob = new_policy_logprobs_group[i]
        old_policy_logprob = old_policy_logprobs_group[i]

        ratio = np.exp(new_policy_logprob - old_policy_logprob)
        clipped_ratio = np.clip(ratio, 1 - clip_epsilon, 1 + clip_epsilon)
        surrogate_objective = np.minimum(ratio * advantage, clipped_ratio * advantage)
        policy_loss = -surrogate_objective

        kl_divergence = new_policy_logprob - old_policy_logprob
        kl_penalty = kl_penalty_coef * kl_divergence
        group_loss += (policy_loss + kl_penalty)  # 累加组内每个响应的损失

    return group_loss / len(group_advantages)  # 对组内损失取平均
```

:::color5
**<font style="color:#601BDE;">3.核心代码</font>**

:::

1. **构造训练数据**：基于<font style="color:rgb(25, 27, 31);">Qwen-2.5-7B:</font>

```plain
'<|im_start|>system
用户和助手之间的对话。用户提出问题，助手解决问题。助手首先在脑海中思考推理过程，然后为用户提供答案。推理过程和答案分别包含在<think></think>和<answer></answer>标签中，即这里的<think>推理过程</think><answer>在这里回答</ansure><|im_end|>
<|im_start|>user
Kim今天参加数学考试的概率是$\frac{4}{7}$。Kim今天没有数学考试的可能性有多大？用普通分数表示你的答案<|im_end |>
<|im_start|>助手'
```

```json
“<think>这个问题给了我们金今天有数学考试的概率，即\\（\\frac{4}{7}\\）。一个事件没有发生的概率是1减去事件发生的概率。因此，我们需要从1中减去\\frac{14}{7}\\，得出金今天没有数学考试的概率。
要执行这个减法，我们可以将1表示为与\\frac[4}{7]\\具有相同分母的分数。这给了我们\\（1=\\frac[7}{7}\\ 
因此，金今天没有数学考试的概率是\\（\\frac{7}{7}-\\frac{14}{7]\\。
让我们进行减法运算以找到最终答案。
</think>
<answer>金今天没有数学考试的概率是\\（\\frac{3}{7}\\）</答案><|im_end|>“
```

2. **数据标注：**用<font style="color:rgb(25, 27, 31);">使用专业的数学verifier判断两个答案是否对，对的话reward就是1，否则就是0。这种设计非常适用于数学题等任务，因为答案的正确性可以直接通过对比来判断。</font>
3. **<font style="color:rgb(25, 27, 31);">奖励函数实现：</font>**<font style="color:rgb(25, 27, 31);">在 GRPO 中，奖励函数的设计至关重要。首先我们就来看看这个奖励函数是啥，代码中提供了一个简单的奖励函数 </font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">accuracy_reward</font>](https://zhida.zhihu.com/search?content_id=253691962&content_type=Article&match_order=1&q=accuracy_reward&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">，用于判断生成的输出是否正确。</font>

```python
def accuracy_reward(completions, solution, **kwargs):
    """Reward function that checks if the completion is the same as the ground truth."""
    contents = [completion[0]["content"] for completion in completions]
    rewards = []
    for content, sol in zip(contents, solution):
        gold_parsed = parse(
            sol,
            extraction_mode="first_match",
            extraction_config=[LatexExtractionConfig()],
        )
        if len(gold_parsed) != 0:
            # We require the answer to be provided in correct latex (no malformed operators)
            answer_parsed = parse(
                content,
                extraction_config=[
                    LatexExtractionConfig(
                        normalization_config=NormalizationConfig(
                            nits=False,
                            malformed_operators=False,
                            basic_latex=True,
                            equations=True,
                            boxed="all",
                            units=True,
                        ),
                        # Ensures that boxed is tried first
                        boxed_match_priority=0,
                        try_extract_without_anchor=False,
                    )
                ],
                extraction_mode="first_match",
            )
            # Reward 1 if the content is the same as the ground truth, 0 otherwise
            try:
                reward = float(verify(answer_parsed, gold_parsed))
            except Exception as e:
                print(f"verify failed: {e}, answer: {answer_parsed}, gold: {gold_parsed}")
                reward = 0.0
        else:
            # If the gold solution is not parseable, we reward 1 to skip this example
            reward = 1.0
            print("Failed to parse gold solution: ", sol)
        rewards.append(reward)

    return rewards
```

4. **GRPO trainer核心代码解析**

```python
def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
    if return_outputs:
        raise ValueError("The GRPOTrainer does not support returning outputs")
        # Compute the per-token log probabilities for the model

        prompt_ids, prompt_mask = inputs["prompt_ids"], inputs["prompt_mask"]
    completion_ids, completion_mask = inputs["completion_ids"], inputs["completion_mask"]
    input_ids = torch.cat([prompt_ids, completion_ids], dim=1)
    attention_mask = torch.cat([prompt_mask, completion_mask], dim=1)
    logits_to_keep = completion_ids.size(1)  # we only need to compute the logits for the completion tokens

    per_token_logps = self._get_per_token_logps(model, input_ids, attention_mask, logits_to_keep)

    # Compute the KL divergence between the model and the reference model
    if self.beta != 0.0:
        ref_per_token_logps = inputs["ref_per_token_logps"]
        per_token_kl = (
            torch.exp(ref_per_token_logps - per_token_logps) - (ref_per_token_logps - per_token_logps) - 1
        )

        # Compute the loss
        advantages = inputs["advantages"]
    # When using num_iterations == 1, old_per_token_logps == per_token_logps, so we can skip it's computation (see
    # _generate_and_score_completions) and use per_token_logps.detach() instead.
    old_per_token_logps = inputs["old_per_token_logps"] if self.num_iterations > 1 else per_token_logps.detach()
    coef_1 = torch.exp(per_token_logps - old_per_token_logps)
    coef_2 = torch.clamp(coef_1, 1 - self.epsilon, 1 + self.epsilon)
    per_token_loss1 = coef_1 * advantages.unsqueeze(1)
    per_token_loss2 = coef_2 * advantages.unsqueeze(1)
    per_token_loss = -torch.min(per_token_loss1, per_token_loss2)
    if self.beta != 0.0:
        per_token_loss = per_token_loss + self.beta * per_token_kl
        loss = (per_token_loss * completion_mask).sum() / completion_mask.sum()

    # Log the metrics
    mode = "eval" if self.control.should_evaluate else "train"

    if self.beta != 0.0:
        mean_kl = (per_token_kl * completion_mask).sum() / completion_mask.sum()
        self._metrics[mode]["kl"].append(self.accelerator.gather_for_metrics(mean_kl).mean().item())

        is_clipped = (per_token_loss1 < per_token_loss2).float()
    clip_ratio = (is_clipped * completion_mask).sum() / completion_mask.sum()
    self._metrics[mode]["clip_ratio"].append(self.accelerator.gather_for_metrics(clip_ratio).mean().item())
    return loss
```

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

### **<font style="color:rgb(34, 35, 40);">结果监督强化学习与 GRPO：</font>**
<font style="color:rgb(64, 64, 64);">对于每个问题 q，从旧策略模型 πθ_old 中抽取一组输出 {o1, o2, ..., oG}。然后使用奖励模型对这些输出进行评分，产生相应的 G 个奖励 r={r1, r2, ..., rG}。随后，通过减去组平均值并除以组标准差来对这些奖励进行标准化处理。结果监督在每个输出 oi 的末尾提供标准化的奖励，并将输出中所有token的优势 Aˆi,t 设定为该标准化奖励，即 Aˆi,t = (ri - mean(r)) / std(r)，然后通过最大化方程（3）中定义的目标来优化策略。</font>

### **<font style="color:rgb(34, 35, 40);">过程监督强化学习与GRPO:</font>**
<font style="color:rgb(64, 64, 64);">结果监督仅在每个输出结束时提供奖励，这可能不足以有效监督复杂数学任务中的策略。遵循历史方法，我们还探讨了过程监督，它在每个推理步骤结束时提供奖励。</font>

<font style="color:rgb(64, 64, 64);">具体来说，给定问题 q 和 G 个抽样输出 {o1, o2, ..., oG}，使用过程奖励模型对每个输出步骤进行评分，从而得到相应的奖励：R={{rindex(1), ..., rindex(K1)}, ..., {rindex(1)11G, ..., rindex(KG)G}}，其中 index(j) 是第 j 步的结束标记索引，Ki 是第 i 个输出中的总步数。</font>

<font style="color:rgb(64, 64, 64);">我们也用平均值和标准差对这些奖励进行标准化处理，即 ˜rindex(j)i = (rindex(j) - mean(R)) / std(R)。接下来，过程监督计算每个标记的优势作为后续步骤的标准化奖励之和，即 Aˆi,t = ∑index(j)≥t ˜rindex(j)i，并通过最大化方程（3）中定义的目标来优化策略。</font>

### **<font style="color:rgb(34, 35, 40);">迭代强化学习与GRPO：</font>**
<font style="color:rgb(64, 64, 64);">在强化学习的训练进程中，随着策略模型的不断进化，旧的奖励模型可能不足以有效地监督当前的策略模型。因此，为了应对这个问题，我们引入了带有组相对策略优化（Group Relative Policy Optimization, GRPO）的迭代强化学习方法。</font>

<font style="color:rgb(64, 64, 64);">具体来说，在每次迭代中，</font><font style="color:#DF2A3F;">基于当前策略模型生成的数据创建新的奖励模型训练集</font><font style="color:rgb(64, 64, 64);">，并通过一种包含重播机制的方法来持续训练奖励模型，其中历史数据占比10%。这一过程有助于确保奖励模型能够跟上策略模型的进步，从而更有效地指导后续的训练。</font>

### **<font style="color:rgb(34, 35, 40);">DeepSeekMath-RL的训练与评估：</font>**
<font style="color:rgb(64, 64, 64);">在本节中，我们详细描述了DeepSeekMath-RL模型的训练和评估过程。首先介绍了用于监督学习阶段的数据集，并讨论了强化学习(RL)训练设置。随后，展示了评估结果，并将DeepSeekMath-RL与不同的基线方法进行了比较。</font>

### **<font style="color:rgb(34, 35, 40);">监督学习数据集</font>**
<font style="color:rgb(64, 64, 64);">为了训练DeepSeekMath-RL的基础策略模型，我们使用了一个包含3500万个数学问题的数据集进行监督学习。这些问题是通过从互联网上爬取得到的，并经过清理以确保其适合用于训练。此外，对于奖励模型的训练，我们额外收集了一个由高质量回答组成的数据集，这些回答是通过抽样自旧策略模型生成的答案，并经过人工标注者筛选和改进得到的。这个奖励模型训练集包含了约1600万个问题-答案对。</font>

### **<font style="color:rgb(34, 35, 40);">强化学习训练设置</font>**
<font style="color:rgb(64, 64, 64);">在强化学习阶段，我们采用了先前部分中介绍的方法：结果监督、过程监督以及迭代GRPO。为了保证训练的稳定性，我们采取了一系列措施，包括但不限于：</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(64, 64, 64);">使用监督学习阶段训练出的模型作为初始化；</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(64, 64, 64);">在更新策略时，结合历史数据（约占10%）来保持训练的连续性和稳定性；</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(64, 64, 64);">调整学习率和其他超参数以优化性能。</font>

### **<font style="color:rgb(34, 35, 40);">关于强化学习的理解：</font>**
#### <font style="color:rgb(34, 35, 40);">朝向统一范式：</font>
<font style="color:rgb(64, 64, 64);">在本节中，我们提供了一个统一的范式来分析不同的训练方法，如SFT、RFT、DPO、PPO、GRPO，并进一步进行实验以探索该统一范式的因素。一般来说，关于参数 </font>_<font style="color:rgb(64, 64, 64);">θ</font>_<font style="color:rgb(64, 64, 64);"> 的训练方法的梯度可以写成：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738813294301-1bc1be1f-ce05-44db-a151-7a361c9514a9.png)

<font style="color:rgb(64, 64, 64);">存在三个关键组成部分：1）数据源 </font>_<font style="color:rgb(64, 64, 64);">D</font>_<font style="color:rgb(64, 64, 64);">，它决定了训练数据；2）奖励函数 </font>_<font style="color:rgb(64, 64, 64);">πθold</font>_<font style="color:rgb(64, 64, 64);">，它是训练奖励信号的来源；3）算法 </font>_<font style="color:rgb(64, 64, 64);">A</font>_<font style="color:rgb(64, 64, 64);">：它处理训练数据和奖励信号以确定梯度系数 </font>_<font style="color:rgb(64, 64, 64);">A</font>_<font style="color:rgb(64, 64, 64);">(</font>_<font style="color:rgb(64, 64, 64);">s</font>_<font style="color:rgb(64, 64, 64);">,</font>_<font style="color:rgb(64, 64, 64);">a</font>_<font style="color:rgb(64, 64, 64);">,</font>_<font style="color:rgb(64, 64, 64);">i</font>_<font style="color:rgb(64, 64, 64);">,</font>_<font style="color:rgb(64, 64, 64);">πθold</font>_<font style="color:rgb(64, 64, 64);">)，该系数决定了对数据的惩罚或强化的大小。我们根据这样一个统一的范式分析了几种代表性方法：</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">监督微调（SFT）</font>**<font style="color:rgb(64, 64, 64);">：SFT在人类选择的SFT数据上对预训练模型进行微调。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">拒绝采样微调（RFT）</font>**<font style="color:rgb(64, 64, 64);">：RFT进一步在SFT模型采样的输出上对SFT模型进行微调，这些输出基于SFT问题进行了过滤。RFT根据答案的正确性过滤输出。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">直接偏好优化（DPO）</font>**<font style="color:rgb(64, 64, 64);">：DPO通过在SFT模型采样的输出上使用成对的DPO损失来微调SFT模型。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">在线拒绝采样微调（Online RFT）</font>**<font style="color:rgb(64, 64, 64);">：与RFT不同，Online RFT使用实时策略模型进行初始化，并通过实时策略模型采样的增强输出进行微调。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">PPO/GRPO</font>**<font style="color:rgb(64, 64, 64);">：PPO/GRPO使用SFT模型初始化策略模型，并使用实时策略模型采样的输出进行强化。</font>

<font style="color:rgb(64, 64, 64);"></font>

#### <font style="color:rgb(64, 64, 64);">为什么强化学习有效？</font>
<font style="color:rgb(64, 64, 64);">在本文中，我们在一个子集的指令微调数据上进行了强化学习，并且在指令微调模型的基础上取得了显著的性能提升。为了进一步解释为什么强化学习有效，我们在两个基准测试上评估了SFT和RL DeepSeekMath 7B的Pass@K和Maj@K准确率。如图7所示，RL增强了Maj@K的性能，但没有增强Pass@K。这些发现表明，</font><font style="color:#DF2A3F;">RL通过使输出分布更加稳健来增强模型的整体性能，换句话说，似乎改进是归因于从TopK中提升正确响应，而不是增强基本能力。</font>



<font style="color:rgb(1, 1, 1);"></font>

# <font style="color:rgb(1, 1, 1);">多模态RLHF</font>
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



