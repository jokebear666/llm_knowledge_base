# ⓷ Multi-Agent实战：智能合同审核

<!-- source: yuque://zhongxian-iiot9/hlyypb/rmoqff9fcgke652h -->

 

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">随着大型语言模型（LLM）能力的飞速发展，将多个专业化的 AI Agent 组合成一个协作系统已成为构建复杂应用的主流范式。这种多 Agent 架构不仅能提高任务处理的准确性和鲁棒性，还能有效应对幻觉（Hallucinations）、流程管理和性能评估等挑战。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">本文将深入探讨如何利用 </font>**<font style="color:rgb(25, 27, 31);">LangGraph</font>**<font style="color:rgb(25, 27, 31);">实现一个完备的</font>**<font style="color:rgb(25, 27, 31);">“智能合同审核与风险分析系统”</font>**<font style="color:rgb(25, 27, 31);">。我们将采用 Supervisor（主管） 架构，并详细讲解 LangGraph 中的</font>[<font style="color:rgb(9, 64, 142);">状态管理</font>](https://zhida.zhihu.com/search?content_id=266154127&content_type=Article&match_order=1&q=%E7%8A%B6%E6%80%81%E7%AE%A1%E7%90%86&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、</font>[<font style="color:rgb(9, 64, 142);">工具定义</font>](https://zhida.zhihu.com/search?content_id=266154127&content_type=Article&match_order=1&q=%E5%B7%A5%E5%85%B7%E5%AE%9A%E4%B9%89&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、短期/长期记忆，以及</font>[**<font style="color:rgb(9, 64, 142);">人机协作</font>**](https://zhida.zhihu.com/search?content_id=266154127&content_type=Article&match_order=1&q=%E4%BA%BA%E6%9C%BA%E5%8D%8F%E4%BD%9C&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">（</font>**[**<font style="color:rgb(9, 64, 142);">Human-in-the-Loop</font>**](https://zhida.zhihu.com/search?content_id=266154127&content_type=Article&match_order=1&q=Human-in-the-Loop&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">, HITL）</font>**<font style="color:rgb(25, 27, 31);">功能。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1762852889101-408bdeff-92e4-4b38-b174-9256a07bc757.tif?x-oss-process=image/format,png)

# <font style="color:rgb(25, 27, 31);">1. 核心架构与工业案例：智能合同审核系统</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">我们将构建一个用于审核商业合同的 Agent 系统。用户上传合同文本，系统需自动完成条款抽取、潜在风险评估，并根据用户历史偏好给出定制化建议。</font>

:::

## <font style="color:rgb(25, 27, 31);">1.1 系统架构（</font>[<font style="color:rgb(9, 64, 142);">Supervisor 模式</font>](https://zhida.zhihu.com/search?content_id=266154127&content_type=Article&match_order=1&q=Supervisor+%E6%A8%A1%E5%BC%8F&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）</font>
:::color5
**<font style="color:#601BDE;">主管（Supervisor）模式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:#000000;">由一个中心 Agent 负责任务路由和协调，将复杂任务分派给专业化的子 Agent。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1762852838076-a8407e01-247d-41f5-9c45-557a93ca1f5c.tif?x-oss-process=image/format,png)

## <font style="color:rgb(25, 27, 31);">1.2 LangGraph 状态（State）定义</font>
:::color5
**<font style="color:#601BDE;">状态（State）定义</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在 LangGraph 中，</font>**<font style="color:rgb(25, 27, 31);">状态（State）</font>**<font style="color:rgb(25, 27, 31);">是贯穿整个 Agent 流程的共享数据结构，它像 Agent 的“短期记忆”一样，保存了当前的对话历史、数据和上下文。我们使用 TypedDict 定义状态模式（State Schema）：</font>

```python
from typing_extensions import TypedDict  
from typing import Annotated, List  
from langgraph.graph.message import AnyMessage, add_messages  
from langgraph.managed.is_last_step import RemainingSteps

# LangGraph 状态定义
class ContractState(TypedDict):  
    """  
    合同审核 Agent 的共享状态，定义了流经图节点的所有数据结构。  
    """  
    # 客户/项目标识符，用于长期记忆检索  
    project_id: str  

    # 核心合同文本，从用户输入中提取  
    contract_text: str  

    # 完整的会话历史，用于短期记忆和上下文维护  
    messages: Annotated[List[AnyMessage], add_messages]   

    # 从长期记忆中加载的用户风险偏好  
    loaded_memory: str   

    # 当前合同分析的风险报告摘要  
    risk_report: str   

    # 循环计数器，防止无限递归  
    remaining_steps: RemainingSteps
```

**<font style="color:rgb(25, 27, 31);">关键讲解：</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">1. messages: 使用</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Annotated[..., add_messages]</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">确保每次 Agent 或工具的输出自动添加到历史消息列表，这是 LangGraph 短期记忆的关键实现。  
</font><font style="color:rgb(25, 27, 31);">2. loaded_memory: 用于加载长期记忆（如用户定义的“高风险”合同条款类型），以实现个性化分析。</font>

# <font style="color:rgb(25, 27, 31);">2. Agent 职责与工具（Tools）定义</font>
:::color3
**简介：****<font style="color:rgb(25, 27, 31);">工具（Tools）</font>**<font style="color:rgb(25, 27, 31);">是赋予 Agent 外部能力的函数，例如数据库查询、API 调用或文件操作。</font>

:::

## <font style="color:rgb(25, 27, 31);">2.1 合同条款抽取 Agent (Extraction Agent)</font>
:::color5
**<font style="color:#601BDE;">职责： 从合同文本中精确提取特定条款（如赔偿、终止、违约责任）并进行摘要。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from langchain_core.tools import tool  
import json

@tool  
def extract_clause_summary(contract_text: str, clause_name: str) -> str:  
    """  
    从合同文本中抽取指定条款的摘要。  

    Args:  
        contract_text (str): 待审核的完整合同文本。  
        clause_name (str): 想要抽取的条款名称 (例如: '终止条款' 或 '赔偿责任')。  

    Returns:  
        str: 抽取到的条款原文及其精炼摘要。  
    """  
    # 模拟工具执行：实际中此处会调用一个 RAG 或 Clause Extraction 模型  
    if "赔偿责任" in clause_name:  
        return "条款摘要: 赔偿责任上限为合同总金额的50%。"  
    elif "终止条款" in clause_name:  
        return "条款摘要: 任意一方提前30天书面通知即可终止。"  
    else:  
        return f"找不到或无法解析条款: {clause_name}。"

# 将工具集合绑定到 LLM
extraction_tools = [extract_clause_summary]
```

## <font style="color:rgb(25, 27, 31);">2.2 法律风险评估 Agent (Risk Agent)</font>
:::color5
**<font style="color:#601BDE;">职责： 根据抽取到的条款和用户偏好，评估潜在的法律和合规风险。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
@tool  
def check_regulatory_compliance(clause_summary: str) -> str:  
    """  
    对照外部法律法规库，检查条款的合规性。  

    Args:  
        clause_summary (str): 待检查的条款摘要。  

    Returns:  
        str: 合规性检查结果，包括潜在的外部风险。  
    """  
    # 模拟工具执行：实际中此处会调用一个外部法规 API  
    if "合同总金额的50%" in clause_summary:  
        return "合规检查结果: 成功。但在特定行业（如金融）中，此类免责条款可能面临监管挑战。"  
    else:  
        return "合规检查结果: 未发现外部法规风险。"

# 将工具集合绑定到 LLM
risk_tools = [check_regulatory_compliance]
```

## <font style="color:rgb(25, 27, 31);">2.3 Agent 模型与提示词（Prompts）</font>
:::color5
**<font style="color:#601BDE;">我们使用 langchain_openai 或任何兼容的 LLM，并定义中文的系统提示词。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from langchain_openai import ChatOpenAI  
from langchain_core.prompts import ChatPromptTemplate  from langchain_core.messages import SystemMessage

# 假设已设置 OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 1. 抽取 Agent 的提示词
extraction_prompt = ChatPromptTemplate.from_messages([  
    SystemMessage(  
        "你是一个专业的合同条款抽取专家。你的任务是根据用户要求，精确使用提供的工具从合同文本中抽取和总结指定条款。"  
        "如果用户的问题需要查询数据库或执行特定操作，你必须使用提供的工具。"  
        "如果不需要工具或已完成信息获取，请给出精炼的总结并停止。"  
    ),  
    ("placeholder", "{messages}"), # 占位符用于接收历史消息和上下文  
])

# 2. 风险 Agent 的提示词
risk_prompt = ChatPromptTemplate.from_messages([  
    SystemMessage(  
        "你是一个严谨的法律风险评估师。你的任务是分析合同条款，并结合用户的长期记忆（风险偏好）和外部法规，评估潜在风险。"  
        "请给出明确的风险等级（低/中/高）和建议。必须使用提供的工具进行外部法规检查。"  
    ),  
    ("placeholder", "{messages}"),  
])

# 3. 主管 Agent 的提示词
supervisor_prompt = ChatPromptTemplate.from_messages([  
    SystemMessage(  
        "你是一个高级多 Agent 系统的主管。你的任务是根据用户最新的请求，将任务路由到正确的子 Agent 或决定是否需要人工介入。"  
        "可用的子 Agent 有：合同条款抽取 Agent (extraction_agent) 和 法律风险评估 Agent (risk_agent)。"  
        "如果任务完成或无法继续，请回复 'FINISH'。"  
    ),  
    ("placeholder", "{messages}"),  
])
```

# <font style="color:rgb(25, 27, 31);">3. 短期记忆与长期记忆（Memory）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">多 Agent 系统必须具备记忆能力，LangGraph 通过 </font>**<font style="color:rgb(25, 27, 31);">Checkpointer</font>**<font style="color:rgb(25, 27, 31);"> 实现短期记忆，通过 </font>**<font style="color:rgb(25, 27, 31);">Store</font>**<font style="color:rgb(25, 27, 31);"> 实现长期记忆。</font>

:::

## <font style="color:rgb(25, 27, 31);">3.1 短期记忆 (Short-Term Memory)</font>
:::color5
**<font style="color:#601BDE;">MemorySaver（检查点机制）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">短期记忆由 MemorySaver（检查点机制）提供，它记录并恢复图的完整状态（包括 messages 列表），从而保持当前会话的上下文。</font>

```python
from langgraph.checkpoint.memory import MemorySaver

# 短期记忆：记录和恢复每一次 LangGraph 运行的完整状态
checkpointer = MemorySaver()
```

## <font style="color:rgb(25, 27, 31);">3.2 长期记忆 (Long-Term Memory)</font>
:::color5
**<font style="color:#601BDE;">InMemoryStore</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">长期记忆用于存储跨会话的持久信息，例如用户的个性化设置（如合同风险容忍度）。这里我们使用 InMemoryStore 模拟。</font>

```python
from langgraph.store.memory import InMemoryStore  
from pydantic import BaseModel, Field

# 用于 Pydantic 模型定义用户偏好，实现结构化存储
class UserProfile(BaseModel):  
    risk_tolerance: str = Field(description="用户偏好的合同风险容忍度：激进、平衡或保守。")  
    preferred_clauses: List[str] = Field(description="用户最关注的关键条款列表。")

long_term_store = InMemoryStore()

# 长期记忆操作节点
def load_memory(state: ContractState) -> ContractState:  
    """从长期存储加载用户偏好。"""  
    project_id = state.get("project_id", "default")  
    memory = long_term_store.get(project_id)  
    if memory:  
        # 假设内存存储了 UserProfile 对象  
        user_profile = memory.get("memory_profile", UserProfile(risk_tolerance="平衡", preferred_clauses=[]))  
        return {"loaded_memory": f"用户风险偏好: {user_profile.risk_tolerance}, 关注条款: {', '.join(user_profile.preferred_clauses)}"}  
    return {"loaded_memory": "未找到历史偏好。"}

def create_memory(state: ContractState) -> ContractState:  
    """根据本次会话更新长期存储中的用户偏好。"""  
    # 模拟从会话中提取新的偏好并更新 UserProfile  
    new_preference = "保守" # 假设 LLM 根据本次风险报告得出的结论  

    # 在实际系统中，LLM 会使用一个工具来解析 messages 并输出结构化的 UserProfile  
    project_id = state.get("project_id", "default")  
    updated_profile = UserProfile(  
        risk_tolerance=new_preference,   
        preferred_clauses=["赔偿责任", "违约责任"]  
    )  
    long_term_store.put(project_id, {"memory_profile": updated_profile})  
    print(f"n[INFO] 长期记忆已更新：项目 {project_id} 的风险偏好设置为 {new_preference}")  
    return {} # 不更新状态，只执行副作用
```

# <font style="color:rgb(25, 27, 31);">4. 人机协作（Human-in-the-Loop, HITL）与节点定义</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在合同审核这种高风险场景中，</font>**<font style="color:rgb(25, 27, 31);">人机协作</font>**<font style="color:rgb(25, 27, 31);">至关重要。我们添加一个专门的节点，用于在发现高风险或不确定性时暂停流程，等待人工确认或干预。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

## <font style="color:rgb(25, 27, 31);">4.1 HITL 节点</font>
```python
from langchain_core.messages import HumanMessage, AIMessage

def human_in_the_loop_node(state: ContractState):  
    """  
    当主管 Agent 判断需要人工介入时，发送通知并等待人工输入。  
    """  
    # 检查主管 Agent 是否要求 FINISH 或人工介入  
    last_message = state["messages"][-1]  

    # 假设主管 Agent 在消息中指明了需要人工介入  
    if "FINISH" not in last_message.content:  
        # 模拟人工介入逻辑  
        print("nn>>>>>>>>>>>>>>>>>>>>>>>>>>>>")  
        print("⚠️ **高风险警报：Agent 无法独自处理。**")  
        print(f"Agent 最新回复: {last_message.content}")  
        print("等待人工审核和输入...n")  

        # 在实际应用中，这里会有一个阻塞/异步等待 UI 界面的人工输入  
        human_input = input("请输入人工审核后的指令或确认信息 (例如: '风险确认，继续生成报告'): ")  
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>n")  

        # 将人工输入作为新的 HumanMessage 添加到状态中，供 Agent 重新处理  
        return {"messages": [HumanMessage(content=f"人工审核指令: {human_input}")]}  

    # 如果主管 Agent 已经回复 FINISH，则直接结束  
    return state
```

## <font style="color:rgb(25, 27, 31);">4.2 定义核心节点</font>
:::color5
**<font style="color:#601BDE;">节点（Node）定义</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">LangGraph 中的</font>**<font style="color:rgb(25, 27, 31);">节点（Node）</font>**<font style="color:rgb(25, 27, 31);">是图中的核心执行单元，接收当前状态，执行逻辑（调用 LLM、工具或自定义函数），然后返回新的状态。我们为抽取 Agent 和风险 Agent 各自设置一个 LLM 节点和一个工具调用节点。</font>

```python
from langgraph.prebuilt import ToolExecutor, ToolNode, create_react_agent  
from langgraph.graph import StateGraph, END, START

# 1. 创建 Agent (LLM + Tools)
def create_sub_agent(llm, tools, system_prompt):  
    """  
    创建 ReAct Agent (LLM 绑定工具) 和对应的 ToolExecutor。  
    """  
    tool_executor = ToolExecutor(tools)  
    agent_runnable = create_react_agent(llm=llm.bind_tools(tools), tools=tools, checkpointer=checkpointer, prompt=system_prompt)  
    return agent_runnable, tool_executor

# 创建两个子 Agent
extraction_agent, extraction_executor = create_sub_agent(llm, extraction_tools, extraction_prompt)  
risk_agent, risk_executor = create_sub_agent(llm, risk_tools, risk_prompt)

# LangGraph 预置的 ToolNode 用于执行工具
extraction_tool_node = ToolNode(extraction_executor)  
risk_tool_node = ToolNode(risk_executor)
```

# <font style="color:rgb(25, 27, 31);">5. 构建与运行 LangGraph 流程</font>
## <font style="color:rgb(25, 27, 31);">5.1 主管 Agent 和条件路由</font>
:::color5
**<font style="color:#601BDE;">主管 Agent </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">主管 Agent 将根据其对用户意图的理解，决定下一个被激活的子 Agent。</font>

```python
from langgraph.prebuilt import create_supervisor

# 定义主管 Agent 的路由逻辑 (哪些节点是可调用的子 Agent)
members = ["extraction_agent", "risk_agent"]  
supervisor_agent = create_supervisor(  
    llm=llm,   
    agents=members,  
    system_prompt=supervisor_prompt,  
    handle_messages_correctly=True # 确保消息格式正确  
)

# 定义路由函数：如果 LLM 调用工具，则执行工具；否则结束或交给主管
def check_for_tool_call(state: ContractState) -> str:  
    """检查最后一个消息是否包含工具调用。"""  
    last_message = state["messages"][-1]  
    if last_message.tool_calls:  
        return "continue"  
    return "end"

# 定义主图的路由函数：主管 Agent 的下一步
def route_supervisor(state: ContractState) -> str:  
    """检查主管 Agent 的输出，路由到相应的 Agent 或人工介入。"""  
    last_message = state["messages"][-1]  

    # 假设主管 Agent 的输出是下一个 Agent 的名称 (e.g., 'extraction_agent')  
    if "extraction_agent" in last_message.content:  
        return "extraction_agent"  
    if "risk_agent" in last_message.content:  
        return "risk_agent"  

    # 如果主管 Agent 认为任务需要人工介入  
    if "人工介入" in last_message.content or "FINISH" not in last_message.content:  
        return "human_in_the_loop"   

    # 否则，结束流程并保存记忆  
    return "create_memory"
```

## <font style="color:rgb(25, 27, 31);">5.2 组装最终的多 Agent 系统</font>
```python
# 构建主图
builder = StateGraph(ContractState)

# 1. 添加业务逻辑节点
builder.add_node("load_memory", load_memory)  
builder.add_node("create_memory", create_memory)  
builder.add_node("human_in_the_loop", human_in_the_loop_node)  
builder.add_node("supervisor", supervisor_agent)

# 2. 添加子 Agent 及其工具执行节点  
# 抽取 Agent  
builder.add_node("extraction_agent", extraction_agent)  
builder.add_edge("extraction_agent", "extraction_tool_node", check_for_tool_call)  
builder.add_node("extraction_tool_node", extraction_tool_node)  
builder.add_edge("extraction_tool_node", "extraction_agent")

# 风险 Agent
builder.add_node("risk_agent", risk_agent)  
builder.add_edge("risk_agent", "risk_tool_node", check_for_tool_call)  
builder.add_node("risk_tool_node", risk_tool_node)  
builder.add_edge("risk_tool_node", "risk_agent")

# 3. 设置流程起点和核心路由  
# 起点  
builder.set_entry_point("load_memory")

# 记忆加载 -> 主管
builder.add_edge("load_memory", "supervisor")

# 主管 -> 路由 (决定下一个 Agent, 人工介入, 或结束流程)
builder.add_conditional_edges(  
    "supervisor",  
    route_supervisor,  
    {  
        "extraction_agent": "extraction_agent",  
        "risk_agent": "risk_agent",  
        "human_in_the_loop": "human_in_the_loop",  
        "create_memory": "create_memory",  
    }  
)

# 子 Agent/工具执行完成 -> 返回给主管
builder.add_edge("extraction_agent", "supervisor") # LLM 回答完成，返回主管  
builder.add_edge("risk_agent", "supervisor")       # LLM 回答完成，返回主管  
builder.add_edge("extraction_tool_node", "extraction_agent")  
builder.add_edge("risk_tool_node", "risk_agent")

# 人工介入完成 -> 返回给主管重新处理人工指令
builder.add_edge("human_in_the_loop", "supervisor")

# 记忆保存 -> 结束
builder.add_edge("create_memory", END)

# 编译最终的 Agent 图
contract_review_app = builder.compile(checkpointer=checkpointer)
```

## <font style="color:rgb(25, 27, 31);">5.3 最终 Agent 流程图</font>
:::color5
**<font style="color:#601BDE;">LangGraph 流程图</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">以下是包含所有关键功能（记忆、Agent、人机协作）的完整 LangGraph 流程图：</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1762852883884-274b07e6-0f1e-4cf7-8019-73c1420a8e95.tif?x-oss-process=image/format,png)



**<font style="color:rgb(255, 255, 255);">送礼物</font>**

