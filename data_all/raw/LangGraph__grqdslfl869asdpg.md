# LangGraph

<!-- source: yuque://zhongxian-iiot9/hlyypb/grqdslfl869asdpg -->

# LangGraph架构详解
## <font style="color:rgb(25, 27, 31);">LangGraph基础核心概念详解</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">LangGraph是一个专门用于构建任意工作流程（Workflow）和智能体（Agent）的基础设施框架。与许多追求简化操作的</font>[<font style="color:rgb(9, 64, 142);">No-code</font>](https://zhida.zhihu.com/search?content_id=262094555&content_type=Article&match_order=1&q=No-code&zhida_source=entity)<font style="color:rgb(25, 27, 31);">或</font>[<font style="color:rgb(9, 64, 142);">Low-code</font>](https://zhida.zhihu.com/search?content_id=262094555&content_type=Article&match_order=1&q=Low-code&zhida_source=entity)<font style="color:rgb(25, 27, 31);">开发框架不同，LangGraph选择了一条更加透明和可控的道路——它不对提示词或架构进行过度的抽象封装，而是直接为开发者提供核心优势。</font>

:::

:::color3
**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**https://github.com/langchain-ai/langgraph**](https://github.com/langchain-ai/langgraph)

:::

:::color5
**<font style="color:#601BDE;">1.LangGraph核心优势 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">图结构架构：支持循环、回溯和复杂的控制流</font>
2. <font style="color:rgb(25, 27, 31);">状态管理：拥有强大的中央状态组件，确保上下文连续性</font>
3. <font style="color:rgb(25, 27, 31);">多智能体支持：天然适合构建多个智能体协作的场景</font>
4. <font style="color:rgb(25, 27, 31);">调试支持：LangSmith Studio 提供图结构的可视化调试能力</font>

:::color5
**<font style="color:#601BDE;">2.LangGraph基础核心概念</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758013280773-5eb747c9-c54c-4503-a187-e2197be8ffa1.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);">中心概念：</font>[<font style="color:rgb(9, 64, 142);">StateGraph</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=StateGraph&zhida_source=entity)<font style="color:rgb(25, 27, 31);">作为整个框架的中心，是应用的蓝图和容器，定义并组织其他组件</font>

<font style="color:rgb(25, 27, 31);">核心三要素：</font>

+ <font style="color:rgb(25, 27, 31);">State：全局共享信息，所有节点都可以访问和修改</font>
+ [<font style="color:rgb(9, 64, 142);">Node</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=Node&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：执行具体功能的处理单元，接收状态并返回更新</font>
+ [<font style="color:rgb(9, 64, 142);">Edge</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=Edge&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：定义节点间的连接关系，决定执行流程</font>

<font style="color:rgb(25, 27, 31);">状态管理链：</font>

+ <font style="color:rgb(25, 27, 31);">State -></font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Checkponiter</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=Checkponiter&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">-></font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Thread</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=Thread&zhida_source=entity)
+ <font style="color:rgb(25, 27, 31);">检查点器负责持久化状态，线程是独立的执行实例，每个线程都拥有自己的状态</font>

<font style="color:rgb(25, 27, 31);">执行控制链</font>

+ <font style="color:rgb(25, 27, 31);">Thread </font><font style="color:rgb(25, 27, 31);">↔</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Breakpointer</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=Breakpointer&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">↔</font><font style="color:rgb(25, 27, 31);"> Time Travel</font>
+ <font style="color:rgb(25, 27, 31);">断点允许暂停执行，进行人机交互，时间旅行允许回到历史状态点重新执行</font>

<font style="color:rgb(25, 27, 31);">节点扩展</font>

+ <font style="color:rgb(25, 27, 31);">Node -> python函数、Tool、LLM、...</font>
+ <font style="color:rgb(25, 27, 31);">节点</font>

<font style="color:rgb(25, 27, 31);">流程控制</font>

+ <font style="color:rgb(25, 27, 31);">Edge -></font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">ConditionalEdge</font>](https://zhida.zhihu.com/search?content_id=257576170&content_type=Article&match_order=1&q=ConditionalEdge&zhida_source=entity)
+ <font style="color:rgb(25, 27, 31);">条件边根据状态动态决定下一个节点，是实现智能控制流的关键</font>

## <font style="color:rgb(25, 27, 31);">思维链（Chain of Thought）</font>
:::color5
**<font style="color:#601BDE;">1.关键关系</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">状态包含问题和推理步骤</font>
+ <font style="color:rgb(25, 27, 31);">节点间是线性流程，每个节点增强推理深度</font>
+ <font style="color:rgb(25, 27, 31);">边是固定的，不需要条件判断  
</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758014303792-9a65e2fd-baae-42be-b30e-c3bd4dc1dd64.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">自我反思（Self Reflection）</font>
:::color5
**<font style="color:#601BDE;">1.关键关系</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">状态包含初始回答和反思结果</font>
+ <font style="color:rgb(25, 27, 31);">条件边基于反思质量决定是结束还是继续改进</font>
+ <font style="color:rgb(25, 27, 31);">形成反馈循环，直到达到质量标准</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758013477647-2d1a720c-aa0b-42f8-bfce-4cc79ae22371.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">多智能体协作（Multi - Agent）</font>
:::color5
**<font style="color:#601BDE;">1.关键关系</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">状态包含各专家意见和批评</font>
+ <font style="color:rgb(25, 27, 31);">节点代表不同角色的智能体</font>
+ <font style="color:rgb(25, 27, 31);">并行边表示同时咨询多个专家</font>
+ <font style="color:rgb(25, 27, 31);">汇聚边表示综合多方意</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758013525720-23607b07-4f06-49eb-a706-d2b120c3c0d4.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);">  
</font>

## <font style="color:rgb(25, 27, 31);">验证-修正循环（Verify-and-Correct）</font>
:::color5
**<font style="color:#601BDE;">1.关键关系</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">状态包含生成内容和验证结果</font>
+ <font style="color:rgb(25, 27, 31);">条件边基于验证结果决定流向</font>
+ <font style="color:rgb(25, 27, 31);">修正节点连回验证节点形成循环</font>
+ <font style="color:rgb(25, 27, 31);">计数器状态防止无限循环</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758013644485-5a1104e5-e6e2-4321-84ab-f1e22ab7fa14.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">树搜索决策（Tree Search）</font>
:::color5
**<font style="color:#601BDE;">1.关键关系</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">状态包含当前节点和探索历史</font>
+ <font style="color:rgb(25, 27, 31);">节点代表搜索树的操作步骤</font>
+ <font style="color:rgb(25, 27, 31);">条件边基于搜索深度和结果质量决定</font>
+ <font style="color:rgb(25, 27, 31);">循环边实现树的深度优先或广度优先搜索</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1758013753901-d39e5356-551f-4335-bc15-88a01fe5553c.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);"></font>

# <font style="color:rgb(25, 27, 31);">LangGraph入门实战</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>[<font style="color:rgb(9, 64, 142);">LangGraph</font>](https://zhida.zhihu.com/search?content_id=240318583&content_type=Article&match_order=1&q=LangGraph&zhida_source=entity)<font style="color:rgb(51, 51, 51);"> 是在 LangChain 基础上的一个库，是 LangChain 的 LangChain Expression Language （</font>[<font style="color:rgb(9, 64, 142);">LCEL</font>](https://zhida.zhihu.com/search?content_id=240318583&content_type=Article&match_order=1&q=LCEL&zhida_source=entity)<font style="color:rgb(51, 51, 51);">）的扩展。能够利用有向无环图的方式，去协调多个LLM或者状态，使用起来比 LCEL 会复杂，但是逻辑会更清晰。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">由于OpenAI访问不方便，我们统一使用</font>[<font style="color:rgb(9, 64, 142);">智普AI</font>](https://zhida.zhihu.com/search?content_id=240318583&content_type=Article&match_order=1&q=%E6%99%BA%E6%99%AEAI&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的大模型进行下面的实践。智普AI的接口和OpenAI的比较类似，因此也可以使用OpenAI的tools的接口，目前还没有发现第二家如此方便的接口。实际使用起来，还是比较丝滑的，虽然有一些小问题。我们下面以ToolAgent的思想，利用LangGraph去实现一个可以调用工具的Agent。</font>

:::

:::color5
**<font style="color:#601BDE;">1.langgraph安装</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">注意，这个库需要自己去安装，默认的LangChain不会安装这个库。</font>

```bash
pip install langgraph
```

## <font style="color:rgb(25, 27, 31);">定义工具以及LLM</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">工具的定义，可以参考这篇文章，写的比较详细了，比较方便的就是使用 tools 这个注解。</font>

[使用智普清言的Tools功能实现ToolAgent](https://zhuanlan.zhihu.com/p/684444895)

:::

## <font style="color:rgb(25, 27, 31);">定义Agent的状态</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">LangGraph 中最基础的类型是 </font>[<font style="color:rgb(9, 64, 142);">StatefulGraph</font>](https://zhida.zhihu.com/search?content_id=240318583&content_type=Article&match_order=1&q=StatefulGraph&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，这种图就会在每一个Node之间传递不同的状态信息。然后每一个节点会根据自己定义的逻辑去更新这个状态信息。具体来说，可以继承 TypeDict 这个类去定义状态，下图我们就定义了有四个变量的信息。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">input</font>**<font style="color:rgb(25, 27, 31);">:这是输入字符串，代表用户的主要请求。</font>
+ **<font style="color:rgb(25, 27, 31);">chat_history</font>**<font style="color:rgb(25, 27, 31);">: 这是之前的对话信息，也作为输入信息传入.</font>
+ **<font style="color:rgb(25, 27, 31);">agent_outcome</font>**<font style="color:rgb(25, 27, 31);">: 这是来自代理的响应，可以是 AgentAction，也可以是 AgentFinish。如果是 AgentFinish，AgentExecutor 就应该结束，否则就应该调用请求的工具。</font>
+ **<font style="color:rgb(25, 27, 31);">intermediate_steps</font>**<font style="color:rgb(25, 27, 31);">: 这是代理在一段时间内采取的行动和相应观察结果的列表。每次迭代都会更新。</font>

```python
class AgentState(TypedDict):
    # The input string
    input: str
    # The list of previous messages in the conversation
    chat_history: list[BaseMessage]
    # The outcome of a given call to the agent
    # Needs `None` as a valid type, since this is what this will start as
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # List of actions and corresponding observations
    # Here we annotate this with `operator.add` to indicate that operations to
    # this state should be ADDED to the existing values (not overwrite it)
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
```

## <font style="color:rgb(25, 27, 31);">定义图中的节点</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在LangGraph中，节点一般是一个函数或者langchain中runnable的一种类。我们这里定义两个节点，agent和tool节点，其中agent节点就是决定执行什么样的行动，tool节点就是当agent节点选择执行某个行动时，去调用相应的工具。此外，还需要定义节点之间的连接，也就是边。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">条件判断的边</font>**<font style="color:rgb(25, 27, 31);">：定义图的走向，比如Agent要采取行动时，就需要接下来调用tools，如果Agent说当前的的任务已经完成了，则结束整个流程。</font>
+ **<font style="color:rgb(25, 27, 31);">普通的边</font>**<font style="color:rgb(25, 27, 31);">：调用工具后，始终需要返回到Agent，让Agent决定下一步的行动</font>

```python
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor

# This a helper class we have that is useful for running tools
# It takes in an agent action and calls that tool and returns the result
tool_executor = ToolExecutor(tools)


# Define the agent
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}


# Define the function to execute tools
def execute_tools(data):
    # Get the most recent agent_outcome - this is the key added in the `agent` above
    agent_action = data["agent_outcome"]
    print("agent action:{}".format(agent_action))
    output = tool_executor.invoke(agent_action[-1])
    return {"intermediate_steps": [(agent_action[-1], str(output))]}


# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    # If the agent outcome is an AgentFinish, then we return `exit` string
    # This will be used when setting up the graph to define the flow
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # Otherwise, an AgentAction is returned
    # Here we return `continue` string
    # This will be used when setting up the graph to define the flow
    else:
        return "continue"
```

## <font style="color:rgb(25, 27, 31);">定义图</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">我们可以定义整个图了。值得注意的是，</font>**条件判断的边和普通的边添加方式是不一样的**<font style="color:rgb(25, 27, 31);">。</font>

:::

<font style="color:rgb(25, 27, 31);">最后需要编译整个图，才能正常运行。</font>

```python
# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()
```

## <font style="color:rgb(25, 27, 31);">总代码</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">下面是所有的可执行代码，注意，需要将api_key替换为自己的api_key。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
# ！/usr/bin env python3
# -*- coding: utf-8 -*-
# author: yangyunlong time:2024/2/28
import datetime
import operator
from typing import TypedDict, Annotated, Union, Optional,Type,List

import requests
from langchain import hub
from langchain.agents import create_openai_tools_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, tool
from langchain_core.agents import AgentAction
from langchain_core.agents import AgentFinish
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor
from zhipu_llm import ChatZhipuAI

zhipuai_api_key = ""
glm3 = "glm-3-turbo"
glm4 = "glm-4"

chat_zhipu = ChatZhipuAI(
    temperature=0.8,
    api_key=zhipuai_api_key,
    model=glm3
)


class Tagging(BaseModel):
    """分析句子的情感极性，并输出句子对应的语言"""
    sentiment: str = Field(description="sentiment of text, should be `pos`, `neg`, or `neutral`")
    language: str = Field(description="language of text (should be ISO 639-1 code)")


class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")


@tool("tagging", args_schema=Tagging)
def tagging(s1: str, s2: str):
    """分析句子的情感极性，并输出句子对应的语言"""
    return "The sentiment is {a}, the language is {b}".format(a=s1, b=s2)


@tool("overview", args_schema=Overview)
def overview(summary: str, language: str, keywords: str):
    """Overview of a section of text."""
    return "Summary: {a}\nLanguage: {b}\nKeywords: {c}".format(a=summary, b=language, c=keywords)


@tool
def get_current_temperature(latitude: float, longitude: float):
    """Fetch current temperature for given coordinates."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # Parameters for the request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    # Make the request
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.utcnow()
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in
                 results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']

    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]

    return f'The current temperature is {current_temperature}°C'


tools = [tagging, overview, get_current_temperature]
# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-tools-agent")

# Construct the OpenAI Functions agent
agent_runnable = create_openai_tools_agent(chat_zhipu, tools, prompt)


class AgentState(TypedDict):
    # The input string
    input: str
    # The list of previous messages in the conversation
    chat_history: list[BaseMessage]
    # The outcome of a given call to the agent
    # Needs `None` as a valid type, since this is what this will start as
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # List of actions and corresponding observations
    # Here we annotate this with `operator.add` to indicate that operations to
    # this state should be ADDED to the existing values (not overwrite it)
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


# This a helper class we have that is useful for running tools
# It takes in an agent action and calls that tool and returns the result

tool_executor = ToolExecutor(tools)

# Define the agent
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}


# Define the function to execute tools
def execute_tools(data):
    # Get the most recent agent_outcome - this is the key added in the `agent` above
    agent_action = data["agent_outcome"]
    print("agent action:{}".format(agent_action))
    output = tool_executor.invoke(agent_action[-1])
    return {"intermediate_steps": [(agent_action[-1], str(output))]}


# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    # If the agent outcome is an AgentFinish, then we return `exit` string
    # This will be used when setting up the graph to define the flow
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # Otherwise, an AgentAction is returned
    # Here we return `continue` string
    # This will be used when setting up the graph to define the flow
    else:
        return "continue"


# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()

inputs = {"input": "what is the weather in NewYork", "chat_history": []}
result = app.invoke(inputs)
print(result["agent_outcome"].messages[0].content)
```

<font style="color:rgb(25, 27, 31);">  
  
</font>

# <font style="color:rgb(25, 27, 31);">总结</font>
:::success
**<font style="color:rgb(25, 27, 31);">状态关系(State)：所有模式都依赖状态存储中间结果</font>**

+ <font style="color:rgb(25, 27, 31);">思维链模式：状态存储推理步骤</font>
+ <font style="color:rgb(25, 27, 31);">自我反思模式：状态存储初始答案和反思</font>
+ <font style="color:rgb(25, 27, 31);">多智能体模式：状态存储各专家意见</font>
+ <font style="color:rgb(25, 27, 31);">验证-修正模式：状态存储验证结果和迭代计数</font>
+ <font style="color:rgb(25, 27, 31);">树搜索模式：状态存储搜索路径和评估结果</font>

:::

:::color3
**<font style="color:rgb(25, 27, 31);">节点(Node)：不同的认知或处理步骤</font>**

+ <font style="color:rgb(25, 27, 31);">思维链模式：节点是推理的各个阶段</font>
+ <font style="color:rgb(25, 27, 31);">自我反思模式：节点包括生成、反思和改进</font>
+ <font style="color:rgb(25, 27, 31);">多智能体模式：节点代表不同角色的智能体</font>
+ <font style="color:rgb(25, 27, 31);">验证-修正模式：节点实现生成-验证-修正循环</font>
+ <font style="color:rgb(25, 27, 31);">树搜索模式：节点实现搜索树的遍历操作</font>

:::

:::color5
**<font style="color:rgb(25, 27, 31);">边(Edge)关系:</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

+ <font style="color:rgb(25, 27, 31);">普通边：实现固定流程</font>
+ <font style="color:rgb(25, 27, 31);">条件边：实现动态决策</font>
+ <font style="color:rgb(25, 27, 31);">循环边：实现迭代改进</font>
+ <font style="color:rgb(25, 27, 31);">并行边：实现多智能体同时工作</font>

:::



