# ① Agentic数据合成：工具调用数据合成详解

<!-- source: yuque://zhongxian-iiot9/hlyypb/guhrym6wghgkzu9d -->

## 前言：为何Agent工具调用数据合成至关重要？
:::color3
**简介：**工具调用能力是大模型从“超级大脑”进化为“智能体”的关键，使其具备与真实世界交互的能力。高质量的 SFT 和 RL 训练数据是模型掌握这一能力的基础，分别解决“会用”和“熟练”的问题。

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770108401838-f54c2635-7030-4c21-8a45-690dcfc7d403.png)

:::color5
**<font style="color:#601bde;">1. 大模型的“知识茧房”困局 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

几乎每一位使用过大模型的用户，都会惊叹于它撰写文章、回答问题的流畅能力。然而，大模型更像一个超级大脑，它被困在自己训练数据的知识茧房里。它知道的都是过去的事情，且只能动口不能动手。  
	再举个例子，你让一位极其博学的朋友帮你做顿饭。这位朋友能把全世界每道菜的食谱倒背如流，精确到克和秒。但问题是——他不能碰厨房里的任何东西。他不知道炉灶怎么点火，不会用菜刀，也不知道烤箱的温度旋钮往哪边拧。他只能“口述”整个烹饪过程。这就是一个没有工具调用能力的大模型：它有无穷的知识，但没有“手”，缺少与真实世界交互的“感官”和“四肢”。

:::color5
**<font style="color:#601bde;">2. 工具调用能力：智能体的进化关键</font>**

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770108458556-f52928bc-c29b-4225-8296-cad75571a81f.png)

工具调用能力，正是解决这一困局的关键。它相当于给这个“超级大脑”装上了“手”和“眼睛”，让它能听懂你的需求，自己去操作各种软件、查询实时信息，真正把事情办成。拥有了工具调用能力的大模型，便进化成了真正的智能体（Agent）。它不再只是一个对话引擎，而是一个能感知、决策、执行的数字助手。

+ 🌐 实时信息专家：自动调用搜索引擎、天气 API 或金融数据接口，实时获取并整合最新信息。
+ 🎯 百分百可靠的专家：在进行复杂运算时，自动调用专业的数学计算引擎或代码解释器，确保返回结果的绝对精确。
+ 🤖 自动化执行助手：处理复合任务（例如：分析上月销售数据 → 总结核心问题 → 生成 PPT 报告 → 邮件发送给团队），能将其智能分解为清晰的子步骤逐一或协同完成。

:::color5
**<font style="color:#601bde;">3. 数据合成的核心作用：SFT与RL</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

那么，如何让一个只会聊天的大模型学会这种“动手”能力呢？秘诀在于高质量的训练数据。

**第一步：监督微调数据（SFT）—— 基石**

+ 作用： 它是模型学会调用工具能力的基石，提供大量“标准答案”。
+ 类比： 像一本详尽的工具使用说明书和操作范例。
+ 目标： 教会模型基础的工具识别、参数理解和调用格式，确保能力的“有无”与“正确”。

**第二步：强化学习数据（RL）—— 阶梯**

+ 作用： 它是模型精进工具调用能力的阶梯。
+ 方式： 让模型在模拟或真实环境中“实践”，根据结果好坏（奖励信号）来调整其决策策略。
+ 目标： 提升能力的“熟练度”、“灵活性”与“鲁棒性”。

## 第一部分：业界工具调用数据合成方法总览
:::color3
**简介：**本章梳理了 LLM 工具能力从单点调用到复杂任务编排的演进，以及评测体系的变迁。同时概览了 SFT 和 RL 两大类数据合成方法的主流流程与业界实践（如 ToolLLM, Kimi k2, Toucan 等）。

:::

:::color5
**<font style="color:#601bde;">1. 工具调用能力的本质与挑战</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

让大语言模型（LLM）掌握工具调用能力，绝非简单开放接口权限或训练格式输出所能实现。这本质上是构建一套“环境感知-决策规划-执行反馈”的完整智能体系：模型需精准判断调用时机、从工具库中匹配最优选项、构造合规的调用指令，更要能理解返回结果并转化为有效输出。而这一体系的构建，高度依赖高质量、高多样性的训练数据——数据的质量直接决定了模型工具调用能力的上限。

:::color5
**<font style="color:#601bde;">2. LLM的工具能力演进与评测体系变迁</font>**

:::

模型工具调用能力的发展，经历了从单点工具掌握到复杂任务编排的跃迁。

+ 早期阶段（格式合规）：如 Gorilla 的 BFCL[5], API-Bank 数据集[1]。主要聚焦于让大模型学会与单一、静态的 API（如 REST API、机器学习函数）进行格式正确的交互。评测重点是调用指令的语法准确性、参数填充的完整性。
+ 进阶阶段（策略智能）：随着应用场景向复杂任务延伸，模型能力需求实现了质的突破：从“单轮调用”升级为“多轮对话中的工具协同”（如 Gorilla 的 BFCLV3[5]），从“静态工具适配”扩展到“动态环境下的异常处理”，最终覆盖“代码解释器、浏览器、操作系统”等真实工具生态的全链路调用（如 Gorilla 的 BFCLV4[5]，ACEBench[2]）。
+ 评测进化：评测基准完成了从 “点式校验”到“场景化评估” 的进化。这一演进路径明确指向一个核心结论：训练数据必须从简单的“API调用示例”升级为“智能体实战模拟器”。  
由于真实世界中高质量工具调用数据天然稀缺，以大模型为核心驱动的规模化、自动化数据合成成为业界的主流解决方案。

:::color5
**<font style="color:#601bde;">3. 工具调用SFT数据合成方法总览</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

SFT数据旨在为模型提供高质量、多样化的工具调用“标准答案”或“示范轨迹”。 其合成方法已形成高度系统化的管线，通常包含以下核心模块：

+ **<font style="color:rgb(25, 27, 31);">工具库合成</font>**<font style="color:rgb(25, 27, 31);">：构建丰富且结构化的工具定义集合（如API、函数）。方法包括从开源代码、真实产品文档中爬取与解析，或通过大模型模拟生成。</font>
+ **<font style="color:rgb(25, 27, 31);">任务合成</font>**<font style="color:rgb(25, 27, 31);">：针对给定的工具库，生成大量、多样化的用户查询或目标任务，要求必须通过调用工具来完成。这通常由大模型基于工具描述进行情景化创作。</font>
+ **<font style="color:rgb(25, 27, 31);">轨迹合成</font>**<font style="color:rgb(25, 27, 31);">：为每个任务生成正确的解决方案轨迹，包含模型思考、工具调用、工具返回结果及最终回复。这通常由更强大的“教师模型”或经过精心设计的推理流程生成。</font>
+ **<font style="color:rgb(25, 27, 31);">质量筛选</font>**<font style="color:rgb(25, 27, 31);">：通过规则、模型打分或交叉验证等方式，对合成的任务和轨迹进行过滤、去重与修正，确保数据的高质量和可靠性。</font>

:::color5
**<font style="color:#601bde;">4. SFT数据合成的业界实践与效果</font>**

:::

+ ToolLLM：早期的开创性工作[12]。通过“API收集-指令创建-轨迹推理”三阶段流程，构建包含 1.6 万 API 的 ToolBench 数据集，首次证明开源模型经 SFT 后可具备基础工具调用能力。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107346518-4683083e-3d12-48bc-8346-ecaca9aa1108.png)

+ Kimi k2：专门搭建了一套工具调用数据合成产线（图2）[7]。通过“工具构建-智能体多样化-任务生成-轨迹模拟-质量过滤”流程，生成数万高质量样本。其“真实+合成”的工具库设计、用户人格模拟与噪声注入机制，大幅提升了数据的泛化价值。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107377589-d9569013-bec4-4127-afac-4e1032c66b45.png)

+ Toucan：接入 495 个 MCP 真实工具服务器，构建包含 150 万条轨迹的数据集。其五阶段流水线（MCP服务器载入-任务综合-任务过滤-轨迹生成-后过滤）与三大扩展机制，彻底解决了传统合成数据“场景失真”的痛点[8]。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107406274-40fb8e69-5650-43fc-80ba-b69455df8b49.png)

:::color5
**<font style="color:#601bde;">5. 开源数据集概览</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

我们对主流的开源数据集进行了对比与归纳，方便大家了解：

| **数据集** | **轨迹数量/样本量** | **工具数量** | **任务类别** | **工具真实调用/合成** |
| --- | --- | --- | --- | --- |
| API-Bank(2023)[1] | 2202 | 2211 | 单轮 | 合成数据 |
| API-Bench(2023)[17] | 17002 | 1645 | 单轮 | 合成数据 |
| ToolLLM(2023) [12] | 12657 | 16464 | 单轮 | 合成数据 |
| MTU-Bench(2024) [9] | 159061 | 136 | 单轮，多轮 | 真实工具调用数据 |
| glaive-function-calling-v2(2025) [16] | 113000 | - | 单轮，多轮 | - |
| APIGen(2025) [3] | 60000 | 3673 | 单轮，多轮 | 合成数据 |
| ToolACE(2025) [13] | 11300 | 26507 | 单轮，多轮 | 合成数据 |
| Nemotron(2025) [10] | 310051 | 26507+ | 单轮，多轮 | 合成 |
| Toucan(2025) [8] | 1527259 | 3000~5000 | 单轮，多轮 | 真实工具调用数据 |


:::color5
**<font style="color:#601bde;">6. 工具调用RL数据合成方法总览</font>**

:::

仅靠 SFT 数据训练的模型，在面对复杂、开放或存在不确定性的真实环境时，往往表现的比较脆弱。强化学习（RL）通过让模型在（模拟）环境中“实践”，并根据结果（奖励）来优化其决策策略。RL训练的核心在于环境模拟与奖励函数设计。

+ **<font style="color:rgb(25, 27, 31);">交互环境</font>**<font style="color:rgb(25, 27, 31);">：模拟工具调用可能出现的各种情况，如工具调用失败、返回意外结果、网络延迟、多个可行方案等。</font>
+ **<font style="color:rgb(25, 27, 31);">奖励信号</font>**<font style="color:rgb(25, 27, 31);">：定义何为“好”的行为。这包括任务成功完成、步骤效率高、处理异常优雅、符合安全规范等多维度指标。</font>

:::color5
**<font style="color:#601bde;">7. RL数据合成的业界实践</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

顶尖的闭源模型（如 GLM-4.5，Claude-Sonnet4.5）和领先的开源模型（如 DeepSeek-V3.2, Qwen 3）普遍引入了基于 RL 的训练阶段。业界亦有开源的框架与数据集可供参考，如：Agentgym[4]。Agentgym 提供了 14 类环境，从不同的环境中收集专家注释的轨迹（AGENTTRAJ），让智能体执行行为克隆，并通过 AGENTEVOL 方法探索进化。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107462128-1dd2a0c1-32cb-4b2c-8465-a953044d1993.png)

## 第二部分：大规模工具调用SFT数据合成方法全解析
:::color3
**简介：**本章深入解析 SFT 数据合成的四大核心模块：工具库合成（设计与扩展）、任务合成（分类体系与多样性注入）、轨迹合成（模拟方法）以及校验与筛选（三层过滤网）。

:::

:::color5
**<font style="color:#601bde;">1. 工具库合成：智能体能力的基石</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

工具的多样性与复杂程度直接决定了后续合成任务与交互轨迹的广度与深度。

+ 标准化的工具函数定义：大模型需要清晰，结构化定义的工具说明书。例如 Qwen 官方给出的 JSON 格式工具定义[14]，包含 `type`, `function`, `name`, `description`, `parameters` 等字段。不同模型（如 Kimi-2）可能采用 TypeScript 风格定义，需注意格式统一。

```tsx
{   "type": "function",   
     "function": {     
         "name": "get_current_weather",     
         "description": "当你想查询指定城市的天气时非常有用。",     
         "parameters": {       
             "type": "object",       
             "properties": {         
                 "location": {           
                     "type": "string",           
                     "description": "城市或县区，比如北京市、杭州市、余杭区等。"         
                 }       
              },       
         "required": ["location"]     
          }   
     } 
}
```

+ <font style="color:rgb(25, 27, 31);">type字段固定为"function"；</font>
+ <font style="color:rgb(25, 27, 31);">function字段为 Object 类型；</font>
+ <font style="color:rgb(25, 27, 31);">name字段为自定义的工具函数名称，建议使用与函数相同的名称，如get_current_weather或get_current_time；</font>
+ <font style="color:rgb(25, 27, 31);">description字段是对工具函数功能的描述，大模型会参考该字段来选择是否使用该工具函数。</font>
+ <font style="color:rgb(25, 27, 31);">parameters字段是对工具函数入参的描述，类型是 Object ，大模型会参考该字段来进行入参的提取。如果工具函数不需要输入参数，则无需指定parameters参数。</font>
+ <font style="color:rgb(25, 27, 31);">type字段固定为"object"；</font>
+ <font style="color:rgb(25, 27, 31);">properties字段描述了入参的名称、数据类型与描述，为 Object 类型，Key 值为入参的名称，Value 值为入参的数据类型与描述；</font>
+ <font style="color:rgb(25, 27, 31);">required字段指定哪些参数为必填项，为 Array 类型。</font>
+ 覆盖多样化的应用场景：一个强大的工具库需要在领域和功能上具备足够的多样性。例如 ACEBench 涵盖了 8 大领域 68 个子领域（图6）；APIGen 涵盖了 21 个类别（图7）；TOUCAN 整合了 495 个 MCP 服务分为 27 个类别（图8）。

**<font style="color:rgb(25, 27, 31);">ACEBench</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107577580-09b14d5d-9cb7-4107-8694-9669b578211f.png)

**<font style="color:rgb(25, 27, 31);">APIGen</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107593524-2bd9d0f3-4717-4060-aa31-88129a2e841b.png)

**<font style="color:rgb(25, 27, 31);">TOUCAN</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107625894-5a34c09c-fcde-48c4-94c9-0c77117d1577.png)

:::color5
**<font style="color:#601bde;">2. 工具库的业界主流合成方法与实践</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ 方法一：在线爬取与清洗（以MCP工具为例）
    1. <font style="color:rgb(25, 27, 31);">批量爬取：从GitHub爬取约2800个MCP Server。</font>
    2. <font style="color:rgb(25, 27, 31);">严格筛选：仅保留支持通过流式HTTP访问的远程Server。过滤掉需要复杂第三方凭证或密钥才能调用的Server，以保证合成数据的可复现性。</font>
    3. <font style="color:rgb(25, 27, 31);">功能验证：为筛选后的Server生成少量测试请求，移除无法正常响应或返回无效信息的服务器。 通过这一系列清洗，最终得到了495个高质量的MCP Server作为可靠的工具源。</font>
+ 方法二：基于真实API的映射与扩展
    - 提取与转换：从 Swagger/OpenAPI 文档提取核心参数。
    - 使用大模型进行扩展：
        * 树状结构自进化合成（如 ToolAce 图 9）：构建“工具领域树”，提示大模型在现有 API 基础上添加新功能或限制，生成变体。
        * 参数与描述替换合成：替换功能描述、参数名称及类型。
    - 校验与增强：使用大模型批量校验格式和信息完备性。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107663557-0dd54ab9-629e-4663-855c-dfa80fd8b01a.png)

:::color5
**<font style="color:#601bde;">3. 任务合成：构建逻辑链条</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

任务合成的基础是从工具库中抽取一组 APIs set，形成任务合成的“原料”。

+ 任务类别体系构建（以 BFCLv3 为例）：
    - 单轮任务：
        * <font style="color:rgb(25, 27, 31);">单轮单工具调用：任务只需调用一个特定工具，且工具列表中只提供该必要工具。</font>
        * <font style="color:rgb(25, 27, 31);">单轮多工具干扰：任务只需调用一个工具，但工具列表中同时提供多个无关工具作为干扰项，考验模型的精准选择能力。</font>
        * <font style="color:rgb(25, 27, 31);">单轮并行工具调用：任务需要同时（并行）调用多个工具，且工具列表仅提供这些必要工具。</font>
        * <font style="color:rgb(25, 27, 31);">单轮并行多工具干扰：任务需要并行调用多个工具，但工具列表中混杂了非必要工具，增加选择复杂度。</font>
        * <font style="color:rgb(25, 27, 31);">无关任务：用户需求无法通过提供的任何工具解决，模型应识别并避免调用。</font>
    - 多轮任务（图10）：
        * <font style="color:rgb(25, 27, 31);">基础多轮任务：将多个单轮任务逻辑串联，模型需在连续对话中维护状态并最终完成任务。</font>
        * <font style="color:rgb(25, 27, 31);">参数澄清任务：在某一轮对话中，用户故意遗漏关键信息，模型应主动询问并补全参数。</font>
        * <font style="color:rgb(25, 27, 31);">工具发现任务：对话开始时仅提供部分工具，当模型识别出缺失必要工具时，需通过与用户交互“请求”或“发现”新工具。</font>
        * <font style="color:rgb(25, 27, 31);">长上下文干扰任务：在对话中插入大量无关细节，测试模型从冗长信息中提取关键需求并执行任务的能力。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107792984-85af8029-9711-4c29-aa9d-a14f89f1040a.png)

+ 任务质量筛选：Toucan 提出了 6 个筛选维度（工具选择难度、唯一性、问题质量、场景现实主义、可验证性、稳定性），结合自动化评分与人工抽查。
    - <font style="color:rgb(25, 27, 31);">工具选择难度：判断从提供的工具中选择所需工具的难度</font>
    - <font style="color:rgb(25, 27, 31);">工具选择唯一性：评估所选工具组合相对于可用工具的唯一性，以及可行的替代方案是否也能解决任务。</font>
    - <font style="color:rgb(25, 27, 31);">问题质量：任务的整体质量，反映在其清晰度、特异性和有效性上。</font>
    - <font style="color:rgb(25, 27, 31);">场景现实主义：评估任务场景的真实性和现实性。</font>
    - <font style="color:rgb(25, 27, 31);">可验证性：评估在给定问题的情况下，最终模型答案的验证程度。</font>
    - <font style="color:rgb(25, 27, 31);">稳定性：评估工具输出是否随时间、跨地理位置，以及在随机变化下保持一致。 这一评估体系通常结合自动化评分（如使用单个或多个大模型作为裁判）与人工抽查来实施。</font>
+ 注入多样性：
    - “任务后润色”：生成后通过提示词注入新角色或约束（如 Toucan）。
    - “智能体先行”：先定义具有特定专长的“角色智能体”，再基于其视角生成任务（如 Kimi k2）。

:::color5
**<font style="color:#601bde;">4. 轨迹合成：用户-智能体双模型交互</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

轨迹合成需构建“用户-智能体”双模型交互机制，并由环境模拟模块提供“世界反馈”。

+ 方法一：真实沙盒执行
    - 适用于代码执行、软件操作等。如 Kimi K2 将代码置于沙盒运行，捕获真实输出与错误信息，生成包含成功与失败路径的高质量数据。
+ 方法二：动态虚拟API服务器
    - StableToolBench 提出“缓存-真实调用-模拟”三层架构（图11）：
        * 缓存系统：存储历史真实调用，保障确定性。
        * API模拟器：缓存未命中且真实调用失败时，由 LLM 扮演 API 生成结果。
        * 智能调用规则：优先缓存 -> 尝试真实 -> 模拟兜底。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107805284-f0d39eac-c33b-4a69-8576-c22a99eda4b3.png)

:::color5
**<font style="color:#601bde;">5. 校验与筛选：三层过滤网</font>**

:::

核心原则是“宁可数据少，不可质量差”。

+ 格式合规性校验：通过 JSON Schema 和正则表达式，过滤基础语法错误（如日期格式、邮箱符号），确保机器可读性。
+ 逻辑准确性校验：采用“LLM即裁判”模式，评估工具匹配度、参数准确性、逻辑连贯性。
+ 任务完成度校验：评估完整性（是否满足所有需求）和简洁性（是否高效），确保智能体以“解决问题”为目标。

## 第四部分：工具调用RL数据合成方法全解析
:::color3
**简介：**本章解析 RL 数据合成的核心思路，包括基于 SFT 数据的优化路径（Nemotron）、针对不同场景的双路径合成（GLM-4.5）以及全流程自动化的智能体驱动方案（Deepseek-V3.2）。

:::

:::color5
**<font style="color:#601bde;">1. 基础复用：基于SFT数据的优化路径（以Nemotron为例）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

RL 数据与 SFT 数据核心共性在于“工具调用逻辑的一致性”。Nemotron[10] 直接将 xLAM 和 ToolACE 数据集的子集迁移至 RL 训练。

+ 预处理流程：
    - 无效样本过滤：剔除无实际工具调用意义的样本。
    - 格式清洗：删除无法解析或格式不一致的数据。
    - 多步数据拆分：将多轮轨迹拆分为独立的单步骤数据，适配 GRPO 训练方法。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107813253-3ecc022e-3b01-4e21-ae37-096f7ecb4102.png)

:::color5
**<font style="color:#601bde;">2. 场景细分：GLM-4.5的双路径RL数据合成方案</font>**

:::

GLM-4.5[6] 设计了两套并行方案：

+ 基于规则的分步RL：
    - 适用于步骤明确、流程固定的任务。
    - 数据结构：逐步骤提供真实标注。
    - 奖励机制：配套严格的规则化奖励（图13），考核函数调用正确性和输出格式规范性。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770107822005-b3f763b7-1eec-4dd0-bd26-3ae38d3b5b31.png)

+ 端到端多轮RL：
    - 面向复杂动态任务，培养自主规划能力。
    - 数据合成：模型生成完整轨迹 -> 接收任务完成奖励 -> 优化策略。
    - 任务场景：覆盖单轮多步任务（聚焦工具连贯性）和多轮多步任务（聚焦对话交互与场景理解）。

:::color5
**<font style="color:#601bde;">3. 流程自动化：Deepseek-V3.2的智能体驱动方案</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Deepseek-V3.2[15] 搭建“自动环境合成智能体”，实现闭环数据生产：

+ 环境初始化与数据构建：智能体利用搜索工具获取领域数据，存入沙箱数据库。
+ 专属工具集合成：自动生成适配任务的 Python 工具函数。
+ 基础任务与方案生成：合成任务及配套解决方案（通过验证函数校验）。
+ 难度迭代与工具扩充：逐步提升难度，自动扩充工具库，确保数据复杂度与模型能力同步提升。

## 第五章 总结
:::color3
**简介：**总结了工具调用数据合成从 SFT 到 RL 的技术体系，强调了“真实化、产线化”的趋势，并展望了未来的三大突破点：真实数据获取、动态环境模拟与闭环联动。

:::

:::color5
**<font style="color:#601bde;">1. 技术体系总结</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

工具调用能力是大模型从“语言助手”进化为“行动智能体”的核心纽带。

+ SFT数据：以“标准化、多样化”为核心，通过工具库、任务、环境的协同构建，打下基础能力。
+ RL数据：以“场景化、自动化”为方向，通过环境模拟与奖励反馈，赋予模型复杂场景下的决策鲁棒性。

:::color5
**<font style="color:#601bde;">2. 业界趋势与未来突破</font>**

:::

从业界实践（Toucan, Kimi k2, Nemotron, GLM-4.5）来看，数据合成已呈现“真实化、产线化”以及“基础能力与进阶能力并重”的趋势。未来突破点集中在：

1. 真实场景数据的规模化获取与隐私保护的平衡。
2. 动态环境模拟的精细化，覆盖异常与协同需求。
3. 数据合成与模型训练的闭环联动，实现同步迭代。  
唯有持续攻克这些方向，才能让智能体真正具备“用手做事”的可靠能力。

:::color5
**<font style="color:#601bde;">3. 参考文献</font>**

:::

+ [1] API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs [https://arxiv.org/pdf/2304.08244](https://arxiv.org/pdf/2304.08244)
+ [2] ACEBench: Who Wins the Match Point in Tool Usage? [https://arxiv.org/pdf/2501.12851](https://arxiv.org/pdf/2501.12851)
+ [3] APIGen: Automated Pipeline for Generating Verifiable and Diverse Function-Calling Datasets [https://arxiv.org/pdf/2406.18518](https://arxiv.org/pdf/2406.18518)
+ [4] AGENTGYM: Evolving Large Language Model-based Agents across Diverse Environments [https://arxiv.org/pdf/2406.04151](https://arxiv.org/pdf/2406.04151)
+ [5] BFCL V3 Multi-Turn & Multi-Step Function Calling Evaluation [https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html)
+ [6] GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models [https://arxiv.org/pdf/2508.06471](https://arxiv.org/pdf/2508.06471)
+ [7] KIMI K2: OPEN AGENTIC INTELLIGENCE [https://arxiv.org/pdf/2507.20534](https://arxiv.org/pdf/2507.20534)
+ [8] TOUCAN: SYNTHESIZING 1.5M TOOL-AGENTIC DATA FROM REAL-WORLD MCP ENVIRONMENTS [https://arxiv.org/pdf/2510.01179](https://arxiv.org/pdf/2510.01179)
+ [9] MTU-BENCH: A MULTI-GRANULARITY TOOL-USE BENCHMARK FOR LARGE LANGUAGE MODELS [https://arxiv.org/pdf/2410.11710](https://arxiv.org/pdf/2410.11710)
+ [10] Nemotron-Research-Tool-N1: Exploring Tool-Using Language Models with Reinforced Reasoning [https://arxiv.org/pdf/2505.00024](https://arxiv.org/pdf/2505.00024)
+ [11] StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning of Large Language Models [https://arxiv.org/pdf/2403.07714](https://arxiv.org/pdf/2403.07714)
+ [12] TOOLLLM: FACILITATING LARGE LANGUAGE MODELS TO MASTER 16000+ REAL-WORLD APIS [https://arxiv.org/pdf/2307.16789](https://arxiv.org/pdf/2307.16789)
+ [13] TOOLACE: WINNING THE POINTS OF LLM FUNCTION CALLING [https://arxiv.org/pdf/2409.00920](https://arxiv.org/pdf/2409.00920)
+ [14] Qwen3 function call Function Calling
+ [15] DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models [https://arxiv.org/pdf/2512.02556](https://arxiv.org/pdf/2512.02556)
+ [16] glaiveai/glaive-function-calling glaive-function-calling
+ [17] Gorilla: Large Language Model Connected with Massive APIs [https://arxiv.org/pdf/2305.15334](https://arxiv.org/pdf/2305.15334)

