# ③ Agent的九种设计模式

<!-- source: yuque://zhongxian-iiot9/hlyypb/zkdm2c1sqeg544cx -->

## **<font style="color:rgb(25, 27, 31);">引言</font>**
:::danger
**<font style="color:#000000;">Agent的九种设计模式</font>**

:::

:::success
**React**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1758694649608-e197f8e7-cc81-4718-806f-d41eb4030f4a.jpeg)

<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::success
**<font style="color:#000000;">Basic Reflexion</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696697708-1183f98c-ff4f-4265-897e-e01db575aa69.png)

:::

:::success
**Plan and Solve**

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758695703513-0a76e236-7dd5-46eb-9c84-e628b7c8f08b.tif?x-oss-process=image/format,png)

:::

:::success
**<font style="color:#000000;">Reflexion</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696838061-933cdd85-ef7d-493b-8178-f6e557e65185.png)

:::

:::success
**LLM Compiler**

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758696094592-6595cd1d-7cd7-4d51-8446-ec5ec6fd8a04.tif?x-oss-process=image/format,png)

:::

:::success
**<font style="color:#000000;">Tree Search</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696980847-2cc812c6-4891-4acd-969b-76ba3657069c.png)

:::

:::success
**REWOO**

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758696026198-f24318a5-273a-4db0-8b97-b97a3a62bd42.tif?x-oss-process=image/format,png)

:::

:::success
**<font style="color:#000000;">Self-Discover</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758697073127-fd2f45f3-9bc6-49f7-abc6-e5eb71dc0212.png)

:::

:::success
**Storm**

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758698624961-551d4afe-2c77-4be0-83e2-e585d52181f1.tif?x-oss-process=image/format,png)

:::



:::color5
**<font style="color:#601BDE;">Agent设计模式汇总 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">设计模式</font>** | **<font style="color:rgb(25, 27, 31);">Paper</font>** | **<font style="color:rgb(25, 27, 31);">Code</font>** | **<font style="color:rgb(25, 27, 31);">Langchain</font>** | **<font style="color:rgb(25, 27, 31);">特点总结</font>** |
| :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">React</font><br/><font style="color:rgb(25, 27, 31);"></font> | [Paper](https://arxiv.org/pdf/2210.03629) | [code](https://link.zhihu.com/?target=https%3A//github.com/ysymyth/ReAct) | [Langchain](https://link.zhihu.com/?target=https%3A//python.langchain.com/docs/modules/agents/agent_types/react/) | <font style="color:rgb(25, 27, 31);">快速响应，快速反馈，但无计划。</font> |
| <font style="color:rgb(25, 27, 31);">Plan and execute</font> | [Paper](https://arxiv.org/pdf/2305.04091) | [code](https://link.zhihu.com/?target=https%3A//github.com/AGI-Edgerunners/Plan-and-Solve-Prompting) | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/plan-and-execute/plan-and-execute.ipynb) | <font style="color:rgb(25, 27, 31);">有计划的进行</font> |
| <font style="color:rgb(25, 27, 31);">ReWOO</font> | [Paper](https://arxiv.org/pdf/2305.18323) | [code](https://link.zhihu.com/?target=https%3A//github.com/billxbf/ReWOO/) | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/rewoo/rewoo.ipynb) | <font style="color:rgb(25, 27, 31);">React改进方法</font> |
| <font style="color:rgb(25, 27, 31);">LLM compiler</font> | [Paper](https://arxiv.org/pdf/2312.04511) | [code](https://zhuanlan.zhihu.com/p/692971105) | [Langchain](https://github.com/langchain-ai/langgraph/blob/main/examples/llm-compiler/LLMCompiler.ipynb) | <font style="color:rgb(25, 27, 31);">将无依赖关系的任务并行处理加快速度</font> |
| <font style="color:rgb(25, 27, 31);">Basic reflection</font> | | | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/reflection/reflection.ipynb) | <font style="color:rgb(25, 27, 31);">加入反思</font> |
| <font style="color:rgb(25, 27, 31);">Reflexion</font> | [Paper](https://arxiv.org/pdf/2303.11366) | [code](https://link.zhihu.com/?target=https%3A//github.com/noahshinn/reflexion) | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/reflexion/reflexion.ipynb) | <font style="color:rgb(25, 27, 31);">通过强化学习增强Agent下一步的规划</font> |
| <font style="color:rgb(25, 27, 31);">Language Agent Tree Search</font> | [Paper](https://arxiv.org/pdf/2310.04406) | [code](https://link.zhihu.com/?target=https%3A//github.com/andyz245/LanguageAgentTreeSearch) | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/lats/lats.ipynb%3Fref%3Dblog.langchain.dev) | <font style="color:rgb(25, 27, 31);">综合了强化学习式反思、规划、执行、ReAct、TOT的一种设计模式，</font> |
| <font style="color:rgb(25, 27, 31);">self discover</font> | [Paper](https://arxiv.org/pdf/2402.03620) | [code](https://link.zhihu.com/?target=https%3A//github.com/catid/self-discover/tree/main%3Ftab%3Dreadme-ov-file) | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/self-discover/self-discover.ipynb) | <font style="color:rgb(25, 27, 31);">对任务本身进行反思</font> |
| <font style="color:rgb(25, 27, 31);">Storm</font> | [Paper](https://arxiv.org/pdf/2402.14207) | [code](https://link.zhihu.com/?target=https%3A//github.com/stanford-oval/storm) | [Langchain](https://link.zhihu.com/?target=https%3A//github.com/langchain-ai/langgraph/blob/main/examples/storm/storm.ipynb) | <font style="color:rgb(25, 27, 31);">可以使短文字生成长篇大论。</font> |


  


<font style="color:rgb(25, 27, 31);">  
</font>

## <font style="color:rgb(25, 27, 31);">ReAct 模式</font>
:::success
**背景：**<font style="color:rgb(25, 27, 31);">这是 LLM Agent 第一文，发表于 2022 年 10 月，现在看起来特别简单，但当时ChatGPT还没有面世，能够提出让 LLM 学会使用工具，具有一定的开创性。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1758694649608-e197f8e7-cc81-4718-806f-d41eb4030f4a.jpeg)

### <font style="color:rgb(25, 27, 31);">React 原理</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">ReAct 原理很简单，没有 ReAct 之前，Reasoning 和 Act 是分割开来的。举个例子，你让孩子帮忙去厨房里拿一个瓶胡椒粉，告诉 ta 一步步来（COT提示词策略）：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

1. <font style="color:rgb(25, 27, 31);">先看看台面上有没有；</font>
2. <font style="color:rgb(25, 27, 31);">再拉开灶台底下抽屉里看看；</font>
3. <font style="color:rgb(25, 27, 31);">再打开油烟机左边吊柜里看看。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758694558800-58dae65d-9262-4ad4-8510-ff51124fc532.png)

+ <font style="color:rgb(25, 27, 31);">没有 React 的情况就是：</font>

> <font style="color:rgb(83, 88, 97);">不管在第几步找到胡椒粉，ta 都会把这几个地方都看看（Action）。</font>
>

+ <font style="color:rgb(25, 27, 31);">有 React 的情况是：</font>

> <font style="color:rgb(83, 88, 97);">Action1：先看看台面上有没有；  
</font><font style="color:rgb(83, 88, 97);">Observation1:台面上没有胡椒粉，执行下一步；  
</font><font style="color:rgb(83, 88, 97);">Action2：再拉开灶台底下抽屉里看看；  
</font><font style="color:rgb(83, 88, 97);">Observation2：抽屉里有胡椒粉；  
</font><font style="color:rgb(83, 88, 97);">Action3:把胡椒粉拿出来。</font>
>

<font style="color:rgb(25, 27, 31);">是的，就是这么简单，在论文的开头作者也提到人类智能的一项能力就是 Actions with verbal reasoning，即每次执行行动后都有一个“碎碎念(Observation”：我现在做了啥，是不是已经达到了目的。这相当于让 Agent 能够维持短期记忆。</font>

### _**<font style="color:rgb(25, 27, 31);"></font>**_**<font style="color:rgb(25, 27, 31);">ReAct</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">实现(通过代码理解原理)</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在看过几个人的开源代码后，拿出一个最容易被产品经理理解的代码来解读。看完你会发现本质上所有的 Agent 设计模式都是</font>**<font style="color:#ED740C;">将人类的思维、管理模式以结构化prompt的方式告诉大模型来进行规划，并调用工具执行，且不断迭代的方法</font>**<font style="color:rgb(25, 27, 31);">— 明白这一点非常重要。</font>

**<font style="color:rgb(25, 27, 31);">code:</font>**<font style="color:rgb(25, 27, 31);"> </font>[YT_Exploring_ReAct_on_Langchain.ipynb](https://link.zhihu.com/?target=https%3A//github.com/samwit/langchain-tutorials/blob/main/agents/YT_Exploring_ReAct_on_Langchain.ipynb)

:::

:::color5
**<font style="color:#601BDE;">1.生成提示词</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">首先，将代码中预设好 ReAct 的提示词模板(格式为Quesion->Thought->Action->Observation)和用户的问题进行合并。得到的提示词是这样的。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758695106737-0de31882-bc48-4e7b-afa3-d7fdc9753fc7.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);">如果需要针对你自己的领域定制，需要将 fewshot 里的内容更换为更合适的内容，比如你的 Action 里可能会有"Send message to someone"， 这里的 Action "Send message" 可能就对应一个外部工具的 API 接口。</font>

:::color5
**<font style="color:#601BDE;">2.调用大模型生成Thought+Action</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">接下来将 few shot 提示词发给大模型。如果直接将上述提示词发给大模型，大模型生成将针对用户问题生成一堆 Thought，Action 和 Observation，但显然这里 Action 还没有展开，我们并不希望大模型输出 Observation。在代码里通过 Stop.Observation 来控制大模型遇到Observation后停止输出，于是大模型仅仅返回 Thought 和 Action，而不会把 Observation 给生成出来。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758695204719-edca3093-293f-4741-9055-bd376f9f094d.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758695189638-6a03b17a-dbb7-4da9-9d4f-c232bac41b04.png)

:::color5
**<font style="color:#601BDE;">3.调用外部工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">拿到 Action 之后，大模型就可以调用外部工具了。首先判断这里的 Action 是不是 Finish，如果不是我们就可以利用大模型把 Action 后面的自然语言转换为外部工具能识别的 API 接口，这个转换过程就是大模型的 function calling 功能，本质上是对大模型进行微调，专门用于语言格式转换的模型，但并非所有的大模型都支持 function calling。</font>

:::color5
**<font style="color:#601BDE;">4.</font>**<font style="color:#601BDE;"> </font>**<font style="color:#601BDE;">生成Observation</font>**

:::

<font style="color:rgb(25, 27, 31);">API 接口返回后，还会将接口返回内容转换为自然语言输出，生成 Observation，然后将 Observation 的内容，加上刚刚的 Thought， Action 内容输入给大模型，重复第 2，3 步，直至 Action 为Finish 为止。</font>

:::color5
**<font style="color:#601BDE;">5.完成输出</font>**

:::

<font style="color:rgb(25, 27, 31);">将最后一步的 Observation 转化为自然语言输出给用户。由此，我们可以看到 Agent 要落地一个场景，需要定制两项内容。</font>

+ <font style="color:rgb(25, 27, 31);">Prompt 模板中 few shot 中的内容。</font>
+ <font style="color:rgb(25, 27, 31);">function calling 中的外部工具定义。</font>



## **<font style="color:rgb(25, 27, 31);">Plan</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">and</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">solve</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">模式</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">顾名思义这种设计模式是先有计划再来执行。如果说 ReAct更适合 完成“厨房拿胡椒粉”的任务，那么 Plan & solve 更适合完成“西红柿炒鸡蛋”的任务：你需要计划，并且过程中计划可能会变化（比如你打开冰箱发现没有西红柿时，你将购买西红柿作为新的步骤加入计划)。</font>

**<font style="color:rgb(25, 27, 31);">code</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://github.com/AGI-Edgerunners/Plan-and-Solve-Prompting](https://github.com/AGI-Edgerunners/Plan-and-Solve-Prompting)

:::

:::color5
**<font style="color:#601BDE;">1.Plan and Solve Prompts</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">提示词模板方面，论文标题中说得很直白，《Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models》，简言之就是 Zero shot 的提升，下图是作者代码中给出的一些 PS-Plan and Solve 提示词。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758695333503-567807cf-6a14-4353-88e2-ffa456253cd6.png)

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758695703513-0a76e236-7dd5-46eb-9c84-e628b7c8f08b.tif?x-oss-process=image/format,png)

+ **<font style="color:rgb(25, 27, 31);">规划器：</font>**<font style="color:rgb(25, 27, 31);">负责让 LLM 生成一个多步计划来完成一个大任务。代码中有 Planner 和和 Replanner，Planner 负责第一次生成计划；Replanner 是指在完成单个任务后，根据目前任务的完成情况进行 Replan，所以 Replanner 提示词中除了 Zeroshot，还会包含：目标，原有计划，和已完成步骤的情况。</font>
+ **<font style="color:rgb(25, 27, 31);">执行器：</font>**<font style="color:rgb(25, 27, 31);">接受用户查询和规划中的步骤，并调用一个或多个工具来完成该任务。</font>

## **<font style="color:rgb(25, 27, 31);">Reason</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">without</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Observation</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">REWOO(</font>[<font style="color:rgb(9, 64, 142);">Reason without Observation</font>](https://zhida.zhihu.com/search?content_id=242124136&content_type=Article&match_order=1&q=Reason+without+Observation&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)这种方法是相对 ReAct中的Observation 来说的，ReAct 提示词结构是 Thought→ Action→ Observation, 而 REWOO 把 Observation 去掉了。但实际上，REWOO 只是将 Observation 隐式地嵌入到下一步的执行单元中了，即由下一步骤的执行器自动去 observe 上一步执行器的输出。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Workflow</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758695907866-d7ad0041-f3ad-4727-b002-b2267db4de45.png)

<font style="color:rgb(25, 27, 31);">举个例子，常见的审批流都是环环相扣的，比如我们的目标是完成 c，我们的步骤是：</font>

> + <font style="color:rgb(25, 27, 31);">我们需要从部门 A 中拿到 a 文件，</font>
> + <font style="color:rgb(25, 27, 31);">然后拿着 a 文件去部门 B 办理 b 文件，</font>
> + <font style="color:rgb(25, 27, 31);">然后拿着 b 文件去部门 C 办理 c 文件- 任务完成。</font>
>

<font style="color:rgb(25, 27, 31);">这其中第 2，3 步骤中 B，C 部门对 a，b 文件的审查本身就是一类Observation。又比如下面提示词模板中给出 one shot 内容中定义出每一步的 plan 都会依赖上一步的输入。</font>

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758696026198-f24318a5-273a-4db0-8b97-b97a3a62bd42.tif?x-oss-process=image/format,png)

+ <font style="color:rgb(25, 27, 31);">Planner：负责生成一个相互依赖的“链式计划”，定义每一步所依赖的上一步的输出。</font>
+ <font style="color:rgb(25, 27, 31);">Worker：循环遍历每个任务，并将任务输出分配给相应的变量。当调用后续调用时，它还会用变量的结果替换变量。</font>
+ <font style="color:rgb(25, 27, 31);">Solver：求解器将所有这些输出整合为最终答案。</font>

## **<font style="color:rgb(25, 27, 31);">LLMCompiler</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Compiler-编译一词在计算机科学的意义就是如何进行任务编排使得计算更有效率，原论文题目是《An LLM Compiler for Parallel Function Calling》，很直白，就是通过</font>**<font style="color:rgb(25, 27, 31);">并行Function</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">calling来提高效率</font>**<font style="color:rgb(25, 27, 31);">，比如用户提问张译和吴京差几岁，planner 搜索张译年龄和搜索吴京年龄同时进行，最后合并即可。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696223206-e7dfcc93-daac-4675-9f6e-8e7ab7c1abc1.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696279008-51fa73e0-3795-4f78-8dac-ce37b247c2e6.png)

<font style="color:rgb(25, 27, 31);">提示词里对 Planner 的要求是这样的，重点是希望生成一个 DAG(Direct Acyclic Graph, 有向无环图。</font>

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">架构上有一个 Planner(规划器)，有一个 Jointer(合并器)。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758696094592-6595cd1d-7cd7-4d51-8446-ec5ec6fd8a04.tif?x-oss-process=image/format,png)

## **<font style="color:rgb(25, 27, 31);">Basic</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Reflection</font>**
:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">Basic Reflection</font>](https://zhida.zhihu.com/search?content_id=242124136&content_type=Article&match_order=1&q=Basic+Reflection&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 可以类比于学生(Generator)写作业，老师(Reflector)来批改建议，学生根据批改建议来修改，如此反复。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Prompts</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">提示词就是复刻师生之间的交互。</font>

```python
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_fireworks import ChatFireworks

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an essay assistant tasked with writing excellent 5-paragraph essays."
            " Generate the best essay possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
llm = ChatFireworks(
    model="accounts/fireworks/models/mixtral-8x7b-instruct", max_tokens=32768
)
generate = prompt | llm
```

```python
essay = ""
request = HumanMessage(
    content="Write an essay on why the little prince is relevant in modern childhood"
)
for chunk in generate.stream({"messages": [request]}):
    print(chunk.content, end="")
    essay += chunk.conten
```

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">架构上有一个 Generator，一个 Reflector。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696697708-1183f98c-ff4f-4265-897e-e01db575aa69.png)

## **<font style="color:rgb(25, 27, 31);">Reflexion</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Reflexion 是 Basic reflection 的升级版，相应论文标题是《Reflexion: Language Agents with Verbal Reinforcement Learning》，本质上是强化学习的思路。和 Basic reflection 相比，引入了外部数据来评估回答是否准确，并强制生成响应中多余和缺失的方面，这使得反思的内容更具建设性。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696534585-761ea0cd-43ad-451f-a386-2649532ed34a.png)

:::color5
**<font style="color:#601BDE;">1.Prompts</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">提示词方面：会让大模型针对问题在回答前进行反思和批判性思考，反思包括有没有漏掉(missing)或者重复(Superfluous)，然后回答问题，回答之后再有针对性的修改(Revise)</font>

```python
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import ValidationError

from pydantic import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries to improve the answer."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )

```

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">架构上，有一个 Responder：自带批判式思考的陈述 Critique；有一个 Revisor：以 Responder 中的批判式思考作为上下文参考对初始回答做修改。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696838061-933cdd85-ef7d-493b-8178-f6e557e65185.png)

## **<font style="color:rgb(25, 27, 31);">Language</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Agent</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Tree</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Search</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">LATS 相应论文标题是《Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models》，很直白：是 Tree search + ReAct+Plan&solve 的融合体。在原作的图中，我们也看到 LATS 中通过树搜索的方式进行 Reward(强化学习的思路)，同时还会融入 Reflection，从而拿到最佳结果。所以：</font>

**<font style="color:rgb(25, 27, 31);">LATS</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">=</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Tree</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">search</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">+</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">ReAct+Plan&solve</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">+</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Reflection</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">+</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">强化学习</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696939091-723a75cc-ad43-420b-bc0a-70445d865e00.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696997415-42f39b7c-e892-4163-ab79-19599c94ec32.png)

<font style="color:rgb(25, 27, 31);">提示词模板方面和之前的 reflection，plan&solve，ReAct 差别不大，只是上下文中多了对树搜索结果的评估和返回结果。</font>

:::color5
**<font style="color:#601BDE;">1.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">架构上，就是多轮的 Basic Reflection， 多个 Generator 和 Reflector。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758696980847-2cc812c6-4891-4acd-969b-76ba3657069c.png)

## [**<font style="color:rgb(9, 64, 142);">Self-Discover</font>**](https://zhida.zhihu.com/search?content_id=242124136&content_type=Article&match_order=1&q=Self-Discover&zhida_source=entity)
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Self-discover 的核心是让大模型在更小粒度上 task 本身进行反思，比如前文中的 Plan&Slove 是反思 task 是不是需要补充，而 Self-discover 是对 task 本身进行反思。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758697040983-f96693c8-4ea4-4439-958b-26a04bbee013.png)

:::color5
**<font style="color:#601BDE;">1.Prompts</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">提示词方面，Self-discover 列出一系列的反思方式让 agent 来选择：</font>

```python
reasoning_modules = [
    "1. How could I devise an experiment to help solve that problem?",
    "2. Make a list of ideas for solving this problem, and apply them one by one to the problem to see if any progress can be made.",
    # "3. How could I measure progress on this problem?",
    "4. How can I simplify the problem so that it is easier to solve?",
    "5. What are the key assumptions underlying this problem?",
    "6. What are the potential risks and drawbacks of each solution?",
    "7. What are the alternative perspectives or viewpoints on this problem?",
    "8. What are the long-term implications of this problem and its solutions?",
    "9. How can I break down this problem into smaller, more manageable parts?",
    "10. Critical Thinking: This style involves analyzing the problem from different perspectives, questioning assumptions, and evaluating the evidence or information available. It focuses on logical reasoning, evidence-based decision-making, and identifying potential biases or flaws in thinking.",
    "11. Try creative thinking, generate innovative and out-of-the-box ideas to solve the problem. Explore unconventional solutions, thinking beyond traditional boundaries, and encouraging imagination and originality.",
    # "12. Seek input and collaboration from others to solve the problem. Emphasize teamwork, open communication, and leveraging the diverse perspectives and expertise of a group to come up with effective solutions.",
    "13. Use systems thinking: Consider the problem as part of a larger system and understanding the interconnectedness of various elements. Focuses on identifying the underlying causes, feedback loops, and interdependencies that influence the problem, and developing holistic solutions that address the system as a whole.",
    "14. Use Risk Analysis: Evaluate potential risks, uncertainties, and tradeoffs associated with different solutions or approaches to a problem. Emphasize assessing the potential consequences and likelihood of success or failure, and making informed decisions based on a balanced analysis of risks and benefits.",
    # "15. Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection. Examine personal biases, assumptions, and mental models that may influence problem-solving, and being open to learning from past experiences to improve future approaches.",
    "16. What is the core issue or problem that needs to be addressed?",
    "17. What are the underlying causes or factors contributing to the problem?",
    "18. Are there any potential solutions or strategies that have been tried before? If yes, what were the outcomes and lessons learned?",
    "19. What are the potential obstacles or challenges that might arise in solving this problem?",
    "20. Are there any relevant data or information that can provide insights into the problem? If yes, what data sources are available, and how can they be analyzed?",
    "21. Are there any stakeholders or individuals who are directly affected by the problem? What are their perspectives and needs?",
    "22. What resources (financial, human, technological, etc.) are needed to tackle the problem effectively?",
    "23. How can progress or success in solving the problem be measured or evaluated?",
    "24. What indicators or metrics can be used?",
    "25. Is the problem a technical or practical one that requires a specific expertise or skill set? Or is it more of a conceptual or theoretical problem?",
    "26. Does the problem involve a physical constraint, such as limited resources, infrastructure, or space?",
    "27. Is the problem related to human behavior, such as a social, cultural, or psychological issue?",
    "28. Does the problem involve decision-making or planning, where choices need to be made under uncertainty or with competing objectives?",
    "29. Is the problem an analytical one that requires data analysis, modeling, or optimization techniques?",
    "30. Is the problem a design challenge that requires creative solutions and innovation?",
    "31. Does the problem require addressing systemic or structural issues rather than just individual instances?",
    "32. Is the problem time-sensitive or urgent, requiring immediate attention and action?",
    "33. What kinds of solution typically are produced for this kind of problem specification?",
    "34. Given the problem specification and the current best solution, have a guess about other possible solutions."
    "35. Let’s imagine the current best solution is totally wrong, what other ways are there to think about the problem specification?"
    "36. What is the best way to modify this current best solution, given what you know about these kinds of problem specification?"
    "37. Ignoring the current best solution, create an entirely new solution to the problem."
    # "38. Let’s think step by step."
    "39. Let’s make a step by step plan and implement it with good notation and explanation.",
]
```

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">结构上，Self-Discover 如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758697073127-fd2f45f3-9bc6-49f7-abc6-e5eb71dc0212.png)

+ <font style="color:rgb(25, 27, 31);">Selector: 从众多的反省方式中选择合适的反省方式；</font>
+ <font style="color:rgb(25, 27, 31);">Adaptor: 使用选择的反省方式进行反省；</font>
+ <font style="color:rgb(25, 27, 31);">Implementor: 反省后进行重新 Reasoning;</font>

## [**<font style="color:rgb(9, 64, 142);">Storm</font>**](https://zhida.zhihu.com/search?content_id=242124136&content_type=Article&match_order=1&q=Storm&zhida_source=entity)
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Storm 相应论文标题是《 Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models》，很直白：可以从零生成一篇像维基百科的文章。主要思路是先让 agent 利用外部工具搜索生成大纲，然后再生成大纲里的每部分内容。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758697460424-c89d7901-5048-4dfd-9e3e-3fc8f7c173e7.png)

:::color5
**<font style="color:#601BDE;">1.Prompt</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">提示词模板方面主要围绕如何生成大纲，如何丰富大纲内容来展开。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758697660611-babac508-7f07-42e0-bb94-4ad0bd9a8268.png)

:::color5
**<font style="color:#601BDE;">2.架构流程</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">架构上，就是先有 topic， 然后生成大纲，根据大纲丰富内容。这里会有一个大纲生成器，一个内容生成器。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758697715096-a5703f32-d82b-410a-be2e-5f7fd7100747.tif?x-oss-process=image/format,png)

## **<font style="color:rgb(25, 27, 31);">总结</font>**
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">以上就是目前所总结的 Agent 九大设计模式，其实 Agent 中</font>**<font style="color:rgb(25, 27, 31);">没有最好的设计模式，只有最适合的设计模式</font>**<font style="color:rgb(25, 27, 31);"> ，最终还是要从用户需求出发来选择。</font>

:::

