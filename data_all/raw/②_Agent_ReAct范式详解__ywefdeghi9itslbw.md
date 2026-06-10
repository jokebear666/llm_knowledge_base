# ② Agent ReAct范式详解

<!-- source: yuque://zhongxian-iiot9/hlyypb/ywefdeghi9itslbw -->

# **一、什么是ReAct？**
:::success
**背景：**在人工智能的演进历程中，大语言模型展现出了令人惊叹的文本生成能力，但其“黑箱”特性也带来了显著挑战——模型经常产生看似合理但实际错误的“幻觉”回答，缺乏透明推理过程，且无法与外部世界交互获取实时信息。

:::

:::color3
**简介：****<font style="color:#ED740C;">ReAct即Reasoning（推理）与Acting（行动）的结合，其本质是一种促使语言模型通过与外部工具、环境进行动态交互以完成复杂任务的智能体架构范式</font>****。**[ReAct](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=ReAct&zhida_source=entity)（Reasoning+Acting）通过将思考过程外显化和工具使用标准化，构建了一个可解释、可验证、可扩展的智能体架构。 <font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773745481932-37eb97a6-e4db-443e-8875-2bcff4862880.png)

:::color5
**<font style="color:#601bde;">1. ReAct的起源与核心定义</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

2022年，[普林斯顿大学](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E6%99%AE%E6%9E%97%E6%96%AF%E9%A1%BF%E5%A4%A7%E5%AD%A6&zhida_source=entity)和[谷歌](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E8%B0%B7%E6%AD%8C&zhida_source=entity)的研究团队在论文《ReAct: Synergizing Reasoning and Acting in Language Models》中正式提出了ReAct范式。该范式通过构建“推理-行动-观察”（TAO）的闭环机制，首次实现了语言模型推理能力与外部环境交互能力的深度协同，为解决大模型瓶颈提供了里程碑式的方案。

ReAct即Reasoning（推理）与Acting（行动）的结合，其本质是一种促使语言模型通过与外部工具、环境进行动态交互以完成复杂任务的智能体架构范式。其核心目标在于打破传统语言模型“输入-输出”的单向链路，构建“感知-决策-执行-反馈”的智能闭环，从而使模型从“被动应答者”成功转型为“主动问题解决者”。

:::color5
**<font style="color:#601bde;">2. 与传统AI技术相比的核心特征</font>**

:::

相较于传统AI技术，ReAct具备以下三个核心特征：

+ **显式推理轨迹**：模型在执行具体行动前，会生成具备可追溯性的“推理过程”（Thought），清晰地阐明行动的决策依据，有效解决了传统模型“黑箱决策”带来的可解释性缺失问题。
+ **外部环境锚定**：通过调用搜索引擎、计算器、数据库查询等外部工具（Act）以获取客观反馈（Observe），将推理过程牢牢锚定于真实数据之上，从根源上抑制了“事实幻觉”的产生。
+ **少量样本泛化**：依托大语言模型（LLM）强大的上下文学习能力，仅需提供1至5个包含“推理-行动-观察”完整链路的示例，即可实现对多场景任务的快速适配，免去了大规模微调的繁琐过程。

:::color5
**<font style="color:#601bde;">3. ReAct的技术本质</font>**

:::

从技术本质层面剖析，ReAct并非单一的算法模型，而是由“语言模型 + [工具集](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E5%B7%A5%E5%85%B7%E9%9B%86&zhida_source=entity) + 循环调度机制”共同构成的集成架构。其核心创新点在于，将人类解决问题的常规认知模式（即分析-操作-反馈）高度抽象为机器可执行的标准化框架，赋予了AI自主拆解任务及动态调整策略的进阶能力。

# **二、核心思想与设计理念**
:::color3
**简介：**本章阐述了ReAct模拟人类认知的TAO闭环核心思想，以及保障该范式成功落地的四大核心设计原则。

:::

:::color5
**<font style="color:#601bde;">1. 核心思想：模拟人类认知的TAO闭环</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773745498337-abdcfe38-16bd-42d0-b736-6a2ae9b6c3a9.png)

ReAct的核心思想深刻借鉴了人类解决复杂问题的认知过程。例如，在面对“规划一次跨城旅行”此类任务时，人类通常会先分析具体需求（推理），随后执行查询机票、预订酒店等操作（行动），最后根据航班余票、酒店价格等实际反馈（观察）来动态调整计划，从而形成一个完整的循环。

ReAct将这一认知过程高度抽象为“Thought（推理）→ Act（行动）→ Observe（观察）”的TAO闭环：

+ **Thought（推理）**：作为模型的“内心独白”，主要用于深入分析任务目标、评估历史反馈以及审视当前状态，进而明确下一步行动的严密逻辑依据。
+ **Act（行动）**：代表模型与外部环境进行交互的“执行动作”，例如调用搜索引擎、运用计算工具或下达设备控制指令。
+ **Observe（观察）**：指代外部环境针对模型行动所给出的“客观反馈”，如返回的搜索结果或计算得出的答案，旨在为下一轮的推理过程提供坚实的真实数据支撑。

得益于这一闭环机制，ReAct成功摆脱了对模型内部静态知识库的过度依赖，具备了处理超出预训练数据范畴的实时性、专业性或动态性任务的强大能力。

:::color5
**<font style="color:#601bde;">2. 四大设计理念：保障范式落地的核心原则</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

为确保ReAct范式的高效落地与稳定运行，其架构设计严格遵循以下四大核心原则：

+ **环境锚定原则**：强制要求模型在处理涉及事实性问题时，必须优先调用外部工具以获取确凿证据，严禁仅凭内部预训练记忆生成结论。例如，在执行“核查2024年诺贝尔物理学奖得主”任务时，模型必须通过搜索工具获取权威资讯，而非依赖固有记忆。
+ **可解释性优先原则**：规定推理轨迹必须完整包含“任务现状-行动目的-预期结果”三大核心要素，以确保人类能够清晰追溯其决策逻辑。例如，推理过程需明确表述为：“当前缺少XX信息，计划调用XX工具进行获取，预期将得到XX结果”。
+ **模块解耦原则**：将复杂的推理逻辑、行动执行以及循环调度拆分为相互独立的模块，并通过标准化接口实现高效通信。此种设计赋予了ReAct极佳的场景适配灵活性，仅需替换相应的工具集，即可轻松实现从“多跳问答”到“机器人控制”等跨场景的无缝切换。
+ **容错性设计原则**：通过引入异常捕获、行动重试、上下文裁剪等完善机制，妥善处理工具调用失败、格式解析错误等突发问题，从而显著提升系统的整体鲁棒性。例如，当搜索工具出现超时情况时，模型能够自主生成“搜索失败，尝试更换关键词重新搜索”的推理逻辑与后续行动。

# **三、ReAct工作原理**
:::color3
**简介：**本章将ReAct的工作流程系统拆解为初始化、循环迭代与终止输出三个关键阶段，详细展示TAO闭环的动态执行全过程。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773745509607-58496f3e-4ba5-40b4-a744-1b6337f9912f.png)

:::color5
**<font style="color:#601bde;">1. 初始化阶段：任务与环境准备</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

初始化阶段旨在为后续的TAO循环提供必要的基础输入，其核心操作涵盖以下三项：

1. **任务解析**：接收用户的自然语言任务目标，精准明确任务类型（如事实核查、数据分析等）以及核心约束条件（如时间范围、精度要求等）。
2. **示例加载**：向模型输入1至3个Few-shot（少样本）示例。每个示例均需包含“任务-推理-行动-观察-结果”的完整执行链路，以此辅助模型深刻理解任务逻辑与严格的格式要求。
3. **上下文初始化**：创建专属的[上下文管理器](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86%E5%99%A8&zhida_source=entity)，用于妥善存储后续迭代过程中产生的TAO三元组，从而为模型提供详尽的历史状态参考。

**应用示例**：当用户提出“帮我查询明天从深圳到海南的航班，选最便宜、航班时间在晚上的那班并预订”的需求时，系统在初始化阶段会加载类似于“查询明天深圳到海南最便宜的晚上航班”的标准示例，明确向模型展示“搜索符合条件航班 → 筛选最优航班 → 预订航班”的规范链路。

:::color5
**<font style="color:#601bde;">2. 循环迭代阶段：TAO闭环的核心执行</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

此阶段为ReAct架构的核心所在。每一轮迭代均严格遵循“推理-行动-观察”的既定顺序执行，具体流程拆解如下：

+ **步骤1：Thought（推理）—— 决策逻辑生成**  
模型基于“任务目标 + 历史TAO轨迹”生成详尽的推理内容。该内容需核心输出两项关键信息：其一为当前任务进展（即已获取哪些信息、尚缺哪些信息）；其二为下一步行动方案（即计划调用何种工具、具体参数为何、预期达成何种结果）。鉴于推理轨迹的质量直接关乎行动的有效性，ReAct通常借助[提示工程](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E6%8F%90%E7%A4%BA%E5%B7%A5%E7%A8%8B&zhida_source=entity)来强制保障逻辑的连贯性。  
_示例推理_：“当前任务是查明天从深圳到海南的航班，要选最便宜且晚上的并预订，历史未获取任何数据。需先调用航班查询工具，参数包含出发地深圳、目的地海南、日期明天、时段晚上，获取符合条件的航班列表后再筛选最便宜的，第一步调用航班查询工具。”
+ **步骤2：Act（行动）—— 标准化执行指令输出**  
模型将上述推理结果精准转化为标准化的行动指令。该指令必须明确包含“工具类型”与“具体参数”，且严格遵循预定义的格式规范（例如“工具名[参数1,参数2]”），以确保后续模块能够顺利解析并执行。ReAct所支持的行动类型主要涵盖四类（注：原文未详述四类，此处保留原文结构意图）。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773745540930-2ae350a4-c95b-4c61-8f20-fac12ce5ed23.png)

+ **步骤3：Observe（观察）—— 客观反馈获取**  
[行动解析器](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E8%A1%8C%E5%8A%A8%E8%A7%A3%E6%9E%90%E5%99%A8&zhida_source=entity)首先对标准化指令进行严格校验（包括格式是否正确、参数是否完整）。若校验通过，则正式调用对应工具执行操作；若校验失败，则生成相应的异常反馈。工具执行完毕后，系统将结果以“结构化、去冗余”的标准形式返回，从而形成最终的观察结果。  
_示例观察_：针对航班查询行动“flight_search[深圳,海南,明天,晚上]”，其观察结果可能为“航班列表：1.CA1234（20:00-21:30，票价500元）；2.CZ5678（21:10-22:40，票价650元）；3.MU9012（19:30-21:00，票价580元）”；若查询过程遭遇失败，观察结果则显示为“航班查询工具调用超时，未获取航班数据”。

在完成观察环节后，上下文管理器会将本轮生成的“推理-行动-观察”三元组追加至历史轨迹之中。若轨迹总长度超出了LLM的上下文窗口限制，系统将启动“保留近期3轮 + 早期摘要”的智能裁剪策略，随后平稳过渡至下一轮迭代。

:::color5
**<font style="color:#601bde;">3. 终止输出阶段：结果整理与提交</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

当系统满足以下任一终止条件时，循环迭代将立即停止并输出最终结果：

1. **正常终止**：模型主动输出`finish`行动指令，明确表明已圆满完成既定任务目标。
2. **超时终止**：迭代次数达到预设的最大步数限制（通常设定为5至10步，具体依任务复杂度灵活调整）。
3. **异常终止**：连续出现3次行动失败（例如工具调用持续超时、参数反复错误等），从而触发系统的安全熔断机制。

终止流程启动后，系统将全面整理历史TAO轨迹，并规范输出“最终结果 + 核心执行链路”，以确保最终交付结果具备高度的可追溯性。

# **四、ReAct技术架构**
:::color3
**简介：**为实现TAO闭环的高效执行，ReAct采用了包含核心逻辑层、执行循环层与外部交互层的三层模块化架构，各层职责明确且接口标准化。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773745549567-f65dc0bc-e475-4ade-9914-63e184312aa3.png)

:::color5
**<font style="color:#601bde;">1. 核心逻辑层：智能体的“决策大脑”</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

核心逻辑层作为ReAct架构的决策中枢，主要负责推理轨迹的生成与行动方案的规划。该层主要由“[大型语言模型](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E5%A4%A7%E5%9E%8B%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)（LLM）+ 提示工程模块”协同构成，其核心功能涵盖：

+ **推理引擎**：基于既定任务目标与历史上下文信息，生成逻辑严密的推理轨迹，明确各项行动的内在依据。此功能高度依赖LLM（如GPT-4、Claude 3等）卓越的上下文理解与逻辑推理能力。
+ **行动规划器**：负责将推理结果精准转化为标准化的行动指令，确保指令格式合规且参数完整。该功能的实现主要依托提示工程中的严格格式约束（例如规定“行动必须为XX格式”）。
+ **提示优化模块**：通过精细调整温度参数（通常设定在0.2至0.3之间，以有效降低输出的随机性）、引入负面示例（例如警示模型“避免重复调用同一工具”）等专业手段，持续优化LLM的输出质量。

该层设计的核心精髓在于“通过提示工程全面激活LLM的推理与行动规划潜能”，从而免去了对LLM进行高成本微调的繁琐步骤，大幅降低了技术的落地门槛。

:::color5
**<font style="color:#601bde;">2. 执行循环层：智能体的“中枢调度”</font>**

:::

执行循环层充当着TAO闭环的调度核心角色，主要负责无缝串联推理、行动、观察这三个关键环节。该层由以下三个核心模块构成，其功能与协作逻辑如下：

1. **上下文管理器**：核心职责为历史TAO轨迹的“存储-裁剪-提取”。当轨迹长度逼近或超出预设阈值时，系统将自动采用“近期完整保留 + 早期关键信息摘要”的智能策略，确保上下文内容既精简高效又囊括所有关键信息。
2. **行动解析器**：全面负责行动指令的“格式校验-参数提取-工具路由”工作。若校验顺利通过，则精准提取工具类型与参数，并将其路由至对应的执行工具；若校验不幸失败，则生成类似于“格式错误，需按XX格式重新输出”的观察结果以提示模型。
3. [循环调度器](https://zhida.zhihu.com/search?content_id=268622508&content_type=Article&match_order=1&q=%E5%BE%AA%E7%8E%AF%E8%B0%83%E5%BA%A6%E5%99%A8&zhida_source=entity)：负责精准控制迭代节奏，并执行严格的终止条件判断。在每轮迭代结束后，调度器会仔细检查是否已满足终止条件。若满足，则立即触发结果输出流程；若未满足，则驱动整个流程平稳返回核心逻辑层，正式开启下一轮推理。

执行循环层堪称ReAct架构的“胶水层”，它通过标准化的接口设计，完美实现了核心逻辑层与外部交互层之间的高效协同，确保了闭环流程的顺畅运转。

:::color5
**<font style="color:#601bde;">3. 外部交互层：智能体的“手脚与五官”</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

外部交互层构成了ReAct与外部真实环境进行交互的专属接口，主要负责切实执行行动指令并准确返回观察结果。该层由“工具集-交互环境-数据接口”三大部分紧密构成，其核心设计要求聚焦于“模块化封装 + 标准化接口”：

+ **工具集**：全面囊括了完成各类任务所需的丰富工具。按功能属性可细分为信息检索类（如搜索引擎、知识库API）、数据处理类（如Pandas封装工具、高级计算器）、设备控制类（如机器人运动API、各类传感器工具）等。每一款工具均需严格实现统一的`run()`方法，以便接收标准化参数并返回结构化的执行结果。
+ **交互环境**：广泛涵盖虚拟环境（例如文本游戏ALFWorld、电商模拟平台WebShop等）以及物理环境（例如家庭服务机器人的真实家居环境、自动驾驶的复杂路况环境等），旨在为行动的落地执行提供坚实的场景支撑。
+ **数据接口**：专门负责工具与环境之间的通信适配工作。它不仅能够将行动解析器输出的参数精准转换为工具或环境可识别的特定格式，同时还能将执行结果高效转换为模型易于理解的自然语言或结构化数据。

# **五、ReAct解决了什么问题？**
:::color3
**简介：**ReAct范式的核心价值在于针对性地解决了传统AI技术在应对复杂任务时所面临的四大关键痛点，从而显著提升了智能系统的整体实用性。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1773745558486-4a3ec334-6a79-480a-824f-7565f53c5210.png)

:::color5
**<font style="color:#601bde;">1. 破解传统LLM的“事实幻觉”难题</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

传统LLM的推理过程完全依赖于其在预训练阶段所习得的内部静态知识。因此，当面临涉及实时信息（如最新出台的政策、实时更新的数据）或专业领域知识（如严谨的医疗诊断、复杂的法律条款）的任务时，极易生成与客观事实严重不符的“幻觉内容”。ReAct通过构建“行动调用外部权威工具 → 观察获取客观事实 → 推理整合事实”的严密链路，成功将推理过程锚定于真实可靠的数据之上。相关实验数据显示，在Fever事实核查任务中，ReAct的幻觉率仅为8.2%，远低于纯思维链（CoT）高达23.5%的幻觉率。

:::color5
**<font style="color:#601bde;">2. 破解纯行动模型的“策略僵化”难题</font>**

:::

传统的机器人控制、游戏AI等纯行动模型，往往需要经历海量数据的强化学习训练，方能形成固定的任务策略。一旦面对未经训练的全新场景，极易陷入失败的境地。ReAct充分依托LLM卓越的推理能力，仅需借助少量示例即可快速生成灵活应变的动态策略。例如，在文本游戏ALFWorld的测试中，ReAct仅凭2个示例便实现了高达71%的任务成功率，表现远超成功率仅为37%的传统强化学习模型。

:::color5
**<font style="color:#601bde;">3. 破解AI系统的“决策不可解释”难题</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

传统深度学习模型的决策过程往往呈现出“黑箱”状态，无法清晰解释“为何做出该项决策”，这在医疗、金融等对安全性要求极高的关键领域应用中潜藏着巨大的风险。ReAct严格要求模型必须生成显式的推理轨迹，确保每一步行动均具备明确且合理的逻辑依据。例如，在执行银行理财咨询任务时，模型会清晰地展示出“用户风险承受能力中等 → 推荐稳健型产品 → 调用知识库确认产品收益率”的完整推理逻辑，极大地方便了人类的审计与监督。

:::color5
**<font style="color:#601bde;">4. 破解多场景适配的“高成本”难题</font>**

:::

传统AI模型通常需要针对不同的具体任务进行深度的定制化开发与专门训练，导致多场景适配面临开发成本高昂、周期漫长的困境。ReAct创新性地采用了模块化解耦设计，其核心逻辑层与执行循环层具备极高的复用性。开发者仅需替换外部交互层中的特定工具与环境，即可轻松适配全新的业务场景。例如，若需将系统从“多跳问答”场景切换至“智能日程规划”场景，仅需将工具集（从搜索工具替换为地图API、日历工具）进行更新，全程无需修改任何核心代码，适配周期由此从数周大幅缩短至短短数小时。

# **六、代码示例**
:::color3
**简介：**本章基于Python语言实现了一个极简版框架，深入解析ReAct核心源码中围绕“工具封装”与“TAO循环调度”展开的关键逻辑（注：完整框架需结合LLM API与具体工具方可实现）。

:::

:::color5
**<font style="color:#601bde;">1. 工具封装：标准化接口设计</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

工具封装严格遵循“基类定义接口 + 子类实现功能”的经典模式，以确保所有工具的调用方式保持高度统一。核心代码实现如下：

```python
from typing import Any, List

class BaseTool:
    """工具基类，定义标准化接口"""
    def __init__(self, name: str, description: str):
        self.name = name  # 工具名称（用于行动解析）
        self.description = description  # 工具功能描述（用于模型理解）

    def run(self, params: Any) -> str:
        """核心执行方法，子类必须实现，返回结构化观察结果"""
        raise NotImplementedError("所有工具子类必须实现run方法")

# 航班查询工具实现示例（调用模拟航班查询接口）
class FlightSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="flight_search",
            description="用于查询指定条件的航班信息，参数格式为'出发地,目的地,日期,时段'，时段支持'上午/下午/晚上'"
        )

    def run(self, params: str) -> str:
        """模拟航班查询工具执行逻辑，实际场景替换为真实航班API调用"""
        try:
            # 解析参数（出发地,目的地,日期,时段）
            dep, arr, date, time_period = params.split(',')
            # 模拟符合条件的航班搜索结果
            flight_map = {
                "深圳,海南,明天,晚上": "符合条件航班列表：1. HU7089（深圳宝安→海口美兰，20:15-21:45，票价480元）；2. CZ6753（深圳宝安→三亚凤凰，21:30-23:05，票价620元）；3. MU2478（深圳宝安→海口美兰，19:40-21:10，票价550元）"
            }
            return flight_map.get(f"{dep},{arr},{date},{time_period}", f"未检索到{dep}到{arr}{date}{time_period}的相关航班信息")
        except Exception as e:
            return f"航班查询工具调用失败：{str(e)[:50]}"

# 航班预订工具实现示例（调用模拟航班预订接口）
class FlightBookTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="flight_book",
            description="用于预订指定航班，参数格式为'航班号,乘客姓名,身份证号'"
        )

    def run(self, params: str) -> str:
        """模拟航班预订工具执行逻辑，实际场景替换为真实预订API调用"""
        try:
            # 解析参数（航班号,乘客姓名,身份证号）
            flight_no, name, id_card = params.split(',')
            # 模拟预订成功反馈
            return f"航班预订成功：航班号{flight_no}，乘客{name}（身份证号：{id_card[-4:]}），请携带有效证件提前2小时到机场办理登机手续"
        except Exception as e:
            return f"航班预订失败：{str(e)[:50]}"
```

**代码专业解析**：`BaseTool`类清晰定义了工具的标准化接口（涵盖`name`、`description`属性以及`run`方法），各子类通过继承机制实现具体功能。此处新增的`FlightSearchTool`（航班查询工具）与`FlightBookTool`（航班预订工具），分别精准适配了航班查询与预订的核心业务需求。其参数格式与功能描述的标准化设计，不仅确保了执行循环层能够进行准确的路由与解析，更大幅降低了后续新增交通类工具的开发成本。

:::color5
**<font style="color:#601bde;">2. TAO循环调度：核心流程控制</font>**

:::

循环调度模块作为ReAct架构的“中枢神经”，专门负责串联推理、行动、观察三个核心环节。核心代码实现如下：

```python
class ContextManager:
    """上下文管理器：存储、裁剪与提取历史TAO轨迹"""
    def __init__(self, max_length: int = 4000):
        self.max_length = max_length  # 上下文最大字符数
        self.tao_trajectory = []  # 存储TAO三元组：[{"thought": "", "action": "", "observation": ""}]

    def add_tao(self, thought: str, action: str, observation: str) -> None:
        """添加TAO三元组并裁剪上下文"""
        self.tao_trajectory.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })
        self._prune_trajectory()

    def _prune_trajectory(self) -> None:
        """裁剪超长轨迹：保留近期3轮+早期摘要"""
        trajectory_str = str(self.tao_trajectory)
        if len(trajectory_str) <= self.max_length:
            return
        # 保留近期3轮完整轨迹
        recent_trajectory = self.tao_trajectory[-3:] if len(self.tao_trajectory) >=3 else self.tao_trajectory
        # 生成早期轨迹摘要
        early_actions = [item["action"] for item in self.tao_trajectory[:-3]] if len(self.tao_trajectory) >3 else []
        early_summary = f"早期行动：{', '.join(early_actions[:2])}... 关键结果：{[item['observation'][:30] for item in self.tao_trajectory[:-3] if '成功' in item['observation']][:1]}"
        # 重构上下文
        self.tao_trajectory = [{"thought": "【早期轨迹摘要】", "action": "", "observation": early_summary}] + recent_trajectory

    def get_context_str(self) -> str:
        """生成模型可理解的上下文字符串"""
        if not self.tao_trajectory:
            return "无历史执行轨迹"
        return "\n".join([
            f"步骤{idx+1}：思维：{item['thought']} | 行动：{item['action']} | 观察：{item['observation']}"
            for idx, item in enumerate(self.tao_trajectory)
        ])

def react_core_loop(task: str, tools: List[BaseTool], max_steps: int = 6) -> tuple[str, str]:
    """ReAct核心循环：控制TAO迭代流程，返回最终结果与执行轨迹"""
    # 初始化组件
    context_manager = ContextManager()
    tool_map = {tool.name: tool for tool in tools}  # 工具名称到实例的映射

    # 提示词模板（含Few-shot示例，引导模型输出格式）
    prompt_template = """
    你是ReAct智能体，需通过"思维→行动→观察"循环完成任务，严格遵循以下规则：
    1. 思维：分析任务目标与历史轨迹，说明下一步行动的逻辑依据；
    2. 行动：仅使用提供的工具，格式为"工具名[参数]"，支持工具：{tool_descriptions}；
    3. 观察：根据工具反馈调整后续策略，不可仅凭记忆回答。

    示例：
    任务：查询昨天从深圳到广州最便宜上午的航班
    历史轨迹：无历史执行轨迹
    思维：需获取昨天深圳到广州上午的航班信息，调用航班查询工具，参数为"深圳,广州,昨天,上午"
    行动：flight_search[深圳,广州,昨天,上午]
    观察：符合条件航班列表：1. CZ3201（深圳宝安→广州白云，08:30-09:10，票价230元）；2. HU7125（深圳宝安→广州白云，09:40-10:20，票价280元）
    思维：已获取航班列表，需筛选最便宜的航班（CZ3201，230元），调用航班预订工具完成预订
    行动：flight_book[CZ3201,张三]
    观察：航班预订成功：航班号CZ3201，乘客张三（身份证号：1234），请携带有效证件提前2小时到机场办理登机手续
    思维：已完成航班查询与预订任务，提交结果
    行动：finish[昨天深圳到广州最便宜上午航班为CZ3201（08:30-09:10，票价230元），已完成预订，乘客张三]

    当前任务：{task}
    历史轨迹：{context}
    请输出当前步骤的思维和行动（仅输出思维和行动，无其他内容）：
    思维：
    行动：
    """

    # 循环迭代
    for step in range(max_steps):
        # 1. 构建提示词，调用LLM生成思维与行动（实际场景替换为真实LLM API）
        tool_descriptions = "\n".join([f"- {name}：{tool.description}" for name, tool in tool_map.items()])
        prompt = prompt_template.format(
            tool_descriptions=tool_descriptions,
            task=task,
            context=context_manager.get_context_str()
        ).strip()

        # 模拟LLM输出（实际场景替换为OpenAI API等调用）
        # 此处根据任务逻辑生成模拟输出，真实场景由LLM自主生成
        if step == 0:
            llm_output = """思维：当前任务是查询明天从深圳到海南的航班，选最便宜、航班时间在晚上的那班并预订，无历史数据。需先调用航班查询工具，参数为"深圳,海南,明天,晚上"，获取符合条件的航班列表
行动：flight_search[深圳,海南,明天,晚上]"""
        elif step == 1:
            llm_output = """思维：已获取明天深圳到海南晚上的航班列表，从观察结果可知最便宜的是HU7089（票价480元）。下一步需调用航班预订工具，参数包含航班号HU7089、乘客信息（假设乘客为李四，身份证号）
行动：flight_book[HU7089,李四]"""
        elif step == 2:
            llm_output = """思维：已完成最便宜晚上航班的查询与预订，观察结果显示预订成功，所有任务目标均达成，可提交最终结果
行动：finish[明天从深圳到海南最便宜的晚上航班为HU7089（深圳宝安→海口美兰，20:15-21:45，票价480元），已完成预订，乘客李四（身份证号：6789）]"""
        else:
            llm_output = """思维：任务已完成，无需进一步行动
行动：finish[任务已完成]"""

        # 2. 解析思维与行动（真实场景需增加格式校验）
        thought = llm_output.split("思维：")[1].split("行动：")[0].strip()
        action = llm_output.split("行动：")[1].strip()

        # 3. 执行行动并获取观察结果
        if action.startswith("finish["):
            # 任务完成，提取结果
            result = action[len("finish["):-1].strip()
            return result, context_manager.get_context_str()
        elif action.startswith(tuple(tool_map.keys())):
            # 解析工具类型与参数
            tool_name = next(name for name in tool_map.keys() if action.startswith(name))
            param_str = action[len(tool_name)+1:-1].strip()
            # 调用工具
            observation = tool_map[tool_name].run(param_str)
        else:
            # 无效行动
            observation = f"无效行动：{action}，支持的工具为{list(tool_map.keys())}"

        # 4. 更新上下文
        context_manager.add_tao(thought, action, observation)
        print(f
```

