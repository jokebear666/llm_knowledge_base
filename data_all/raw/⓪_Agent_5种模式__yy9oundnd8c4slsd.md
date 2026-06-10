# ⓪ Agent 5种模式

<!-- source: yuque://zhongxian-iiot9/hlyypb/yy9oundnd8c4slsd -->

## <font style="color:rgb(63, 63, 63);">反射模式（Reflection pattern）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1749190792822-6b4ec1cf-9735-46a5-8805-e79878014db9.jpeg)

:::color5
**<font style="color:#601BDE;">Reflection pattern工作流程 </font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:rgb(63, 63, 63);">用户输入查询</font>**<font style="color:rgb(63, 63, 63);">：用户通过界面或API向agent发送一个查询请求。</font>
2. **<font style="color:rgb(63, 63, 63);">LLM生成初始输出</font>**<font style="color:rgb(63, 63, 63);">：大型语言模型（LLM）接收用户的查询，并生成一个初步的响应。</font>
3. **<font style="color:rgb(63, 63, 63);">用户反馈</font>**<font style="color:rgb(63, 63, 63);">：用户对初步的响应进行评估并给出反馈。</font>
4. **<font style="color:rgb(63, 63, 63);">LLM反射输出</font>**<font style="color:rgb(63, 63, 63);">：基于用户的反馈，LLM对初步的响应进行反思，即重新评估和调整其生成的输出。</font>
5. **<font style="color:rgb(63, 63, 63);">迭代过程</font>**<font style="color:rgb(63, 63, 63);">：这一过程可能需要多次迭代，直到用户对最终的响应感到满意为止。</font>
6. **<font style="color:rgb(63, 63, 63);">返回给用户</font>**<font style="color:rgb(63, 63, 63);">：最终的响应被返回给用户，用户可以通过界面或API接收到结果。</font>

:::color4
<font style="color:rgb(63, 63, 63);">这种模式通常用于提高大型语言模型的交互性和准确性，通过用户反馈不断优化模型的输出</font>

:::

## <font style="color:rgb(63, 63, 63);">工具使用模式（Tool use pattern）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1749190792846-cc0c6961-3e92-488f-8582-4ae2c30c724b.jpeg)

:::color5
**<font style="color:#601BDE;">Tool use pattern工作流程 </font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:rgb(63, 63, 63);">用户输入查询</font>**<font style="color:rgb(63, 63, 63);">：用户通过界面或API向agent发送一个查询请求。</font>
2. **<font style="color:rgb(63, 63, 63);">LLM处理查询</font>**<font style="color:rgb(63, 63, 63);">：agent内部的大型语言模型（LLM）接收用户的查询，并对其进行处理。在这个过程中，LLM可能需要调用外部工具或API来获取更准确的信息。</font>
3. **<font style="color:rgb(63, 63, 63);">调用工具和API</font>**<font style="color:rgb(63, 63, 63);">：如果查询需要额外的信息或数据，LLM会调用存储在vector数据库中的工具和API来获取这些信息。</font>
4. **<font style="color:rgb(63, 63, 63);">生成响应</font>**<font style="color:rgb(63, 63, 63);">：LLM根据从工具和API获取的信息生成一个响应，这个响应可能是文本、表格或其他格式的数据。</font>
5. **<font style="color:rgb(63, 63, 63);">返回给用户</font>**<font style="color:rgb(63, 63, 63);">：最后，生成的响应被返回给用户，用户可以通过界面或API接收到结果。</font>

:::color4
<font style="color:rgb(63, 63, 63);">这种模式通常用于增强大型语言模型的能力，使其能够访问外部资源以提供更全面和准确的回答。</font>

:::

## <font style="color:rgb(63, 63, 63);">ReAct模式（ReAct Pattern）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1749190792838-1595f606-730d-458d-a764-97a0db2142e7.jpeg)

:::color5
**<font style="color:#601BDE;">ReAct Pattern工作流程 </font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:rgb(63, 63, 63);">用户（User）</font>**<font style="color:rgb(63, 63, 63);">：用户向系统提出查询（Query），例如需要完成的任务或请求。</font>
2. **<font style="color:rgb(63, 63, 63);">LLM（Reason）</font>**<font style="color:rgb(63, 63, 63);">：接收到用户的查询后，推理型语言模型（LLM - Reason）会分析查询并生成相应的策略或计划。</font>
3. **<font style="color:rgb(63, 63, 63);">工具（Tools）</font>**<font style="color:rgb(63, 63, 63);">：根据生成的策略或计划，系统调用相应的工具来执行具体的操作。</font>
4. **<font style="color:rgb(63, 63, 63);">环境（Environment）</font>**<font style="color:rgb(63, 63, 63);">：工具执行操作后，将结果反馈给环境。</font>
5. **<font style="color:rgb(63, 63, 63);">LLM（Generate）</font>**<font style="color:rgb(63, 63, 63);">：环境返回的结果被反馈给生成型语言模型（LLM - Generate），生成型语言模型根据结果生成最终的响应。</font>
6. **<font style="color:rgb(63, 63, 63);">响应（Response）</font>**<font style="color:rgb(63, 63, 63);">：生成型语言模型生成的响应返回给用户。</font>

:::color4
<font style="color:rgb(63, 63, 63);">这种模式通过结合推理型语言模型和生成型语言模型，实现了从用户查询到最终响应的完整闭环。推理型语言模型负责策略生成，生成型语言模型负责结果解释和响应生成。</font>

:::

## <font style="color:rgb(63, 63, 63);">规划模式（Planning Pattern）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1749190792970-2283fcf2-f97a-4fa4-9a01-c7a36d1d5370.jpeg)

:::color5
**<font style="color:#601BDE;">Planning Pattern工作流程 </font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:rgb(63, 63, 63);">用户（User）</font>**<font style="color:rgb(63, 63, 63);">：用户向系统提出查询（Query），例如需要完成的任务或请求。</font>
2. **<font style="color:rgb(63, 63, 63);">计划器（Planner）</font>**<font style="color:rgb(63, 63, 63);">：接收到用户的查询后，计划器会分析并生成一系列任务（Generated tasks）。这些任务可能是具体的执行步骤或子任务。</font>
3. **<font style="color:rgb(63, 63, 63);">生成的任务</font>**<font style="color:rgb(63, 63, 63);">：计划器生成的任务会被传递给执行者（ReAct Agent）。</font>
4. **<font style="color:rgb(63, 63, 63);">执行者（ReAct Agent）</font>**<font style="color:rgb(63, 63, 63);">：执行者根据生成的任务执行单个任务，并将结果返回给计划器。</font>
5. **<font style="color:rgb(63, 63, 63);">结果反馈</font>**<font style="color:rgb(63, 63, 63);">：执行者执行完一个任务后，会将结果反馈给计划器。如果所有任务都已完成，则计划器会确认任务完成（Finished?）。</font>
6. **<font style="color:rgb(63, 63, 63);">响应（Response）</font>**<font style="color:rgb(63, 63, 63);">：计划器根据任务完成情况和结果，生成最终的响应（Response），返回给用户。</font>

:::color4
<font style="color:rgb(63, 63, 63);">这个模式确保了任务的有序执行和结果的及时反馈，从而实现用户需求的有效处理。</font>

:::

## <font style="color:rgb(63, 63, 63);">多智能体模式（Multi-agent pattern）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1749190792906-afca8cca-92a8-4bf7-83be-fdafe301f021.jpeg)

:::color5
**<font style="color:#601BDE;">Multi-agent pattern工作流程 </font>****<font style="color:#D22D8D;">（by草莓师姐）</font>**

:::

1. **<font style="color:rgb(63, 63, 63);">用户（User）</font>**<font style="color:rgb(63, 63, 63);">：用户向系统提出查询（Query），例如需要完成的任务或请求。</font>
2. **<font style="color:rgb(63, 63, 63);">项目经理代理（PM agent）</font>**<font style="color:rgb(63, 63, 63);">：接收到用户的查询后，项目经理代理（PM agent）会分析并分配任务给其他代理。</font>
3. **<font style="color:rgb(63, 63, 63);">DevOps代理（DevOps agent）</font>**<font style="color:rgb(63, 63, 63);">：项目经理代理将任务分配给DevOps代理（DevOps agent）。</font>
4. **<font style="color:rgb(63, 63, 63);">技术负责人代理（Tech lead agent）</font>**<font style="color:rgb(63, 63, 63);">：DevOps代理将任务进一步分配给技术负责人代理（Tech lead agent）。</font>
5. **<font style="color:rgb(63, 63, 63);">软件开发工程师代理（SDE agent）</font>**<font style="color:rgb(63, 63, 63);">：技术负责人代理将任务分配给软件开发工程师代理（SDE agent）。</font>
6. **<font style="color:rgb(63, 63, 63);">执行任务</font>**<font style="color:rgb(63, 63, 63);">：每个代理根据分配的任务执行相应的操作，并将结果反馈给上一级代理。</font>
7. **<font style="color:rgb(63, 63, 63);">结果反馈</font>**<font style="color:rgb(63, 63, 63);">：最终，所有代理完成任务后，将结果反馈给项目经理代理。</font>
8. **<font style="color:rgb(63, 63, 63);">综合响应</font>**<font style="color:rgb(63, 63, 63);">：项目经理代理综合所有代理的结果，生成最终的响应（Response），返回给用户。</font>

:::color4
<font style="color:rgb(63, 63, 63);">这种模式通过多个代理协同工作，可以更高效地处理复杂任务，确保任务的有序执行和结果的及时反馈。</font>

:::

