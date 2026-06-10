# ⓸ Agentic RAG 实战

<!-- source: yuque://zhongxian-iiot9/hlyypb/ole6a8l8oztgbyel -->

:::success
**<font style="color:rgb(51, 51, 51);">背景：</font>**<font style="color:rgb(25, 27, 31);">Agentic RAG这类系统通过集成自主代理，利用反射、规划、工具使用和多代理协作等核心代理模式，尝试克服</font>**<font style="color:#117CEE;">传统的RAG系统在知识检索和生成方面表现良好，但在处理动态、多步骤推理任务、适应性和复杂工作流编排方面存在不足</font>**<font style="color:rgb(25, 27, 31);">这些限制。</font>

:::

:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**在本教程中，我们将构建一个agentic RAG。当您希望LLM决定是从向量库检索上下文还是直接响应用户时，agentic RAG非常有用。在本教程结束时，我们将完成以下工作：<font style="color:#D22D8D;">(by草莓师姐)</font>

+ 获取并预处理将用于检索的文档。
+ 为这些文档建立语义搜索索引，并为代理创建检索工具。
+ 构建一个agentic RAG系统，可以决定何时使用检索工具。

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760345777270-a16262bf-382d-408c-bf08-4cf8e60a7130.png)

**Agentic RAG vs 传统RAG**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760347340127-2b1b08d8-8dc6-4509-97fa-8b0e69de0095.png)

**Langgraph视图**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760345777303-94680377-8a91-4efe-8f38-1b84c10657c1.png)



# Setup
:::color3
让下载所需的软件包并设置我们的API密钥：<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```bash
%%capture --no-stderr
%pip install -U --quiet langgraph "lang
chain[openai]" langchain-community langchain-text-splitters
```

```python
import getpass
import os


def _set_env(key: str):
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}:")


_set_env("OPENAI_API_KEY")
```

<font style="background-color:rgba(0, 191, 165, 0.1);">Tip：</font>注册LangSmith，快速发现问题并提高LangGraph项目的性能。LangSmith允许您使用跟踪数据来调试、测试和监视使用LangGraph构建的LLM应用程序。

# 1. 文档预处理
:::color3
获取要在RAG系统中使用的文档。我们将使用lilianweng优秀博客中的三个最新页面。我们将首先使用WebBaseLoader实用程序获取页面的内容：<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
from langchain_community.document_loaders import WebBaseLoader

urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

docs = [WebBaseLoader(url).load() for url in urls]
```

```python
docs[0][0].page_content.strip()[:1000]
```

将提取的文档拆分为更小的块，以便索引到我们的向量库中：

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)
```

```python
doc_splits[0].page_content.strip()
```

# 2. 构建检索工具
:::color3
现在我们有了拆分的文档，我们可以将它们索引到一个向量存储中，用于语义搜索。

:::

:::color5
**<font style="color:#601BDE;">构建embedding模型 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
```

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# 初始化嵌入模型，并创建向量库
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")  # 也可换为"BAAI/bge-small-zh-v1.5"处理中文
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, 
    embedding=embeddings  # 使用新的免费嵌入模型
)
```

:::color5
**<font style="color:#601BDE;">构建检索工具 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts.",
)
```

:::color5
**<font style="color:#601BDE;">使用检索工具</font>**

:::

```python
retriever_tool.invoke({"query": "types of reward hacking"})
```

# 3. 生成Query
:::color3
现在，我们将开始为我们的代理RAG图构建组件（节点和边）。请注意，这些组件将在MessagesState--graph状态下运行，该状态包含一个带有聊天消息列表的消息键。

:::

构建一个generate_query_or_response节点。它将调用LLM，根据当前图形状态（消息列表）生成响应。给定输入消息，它将决定使用检索器工具进行检索，或直接响应用户。请注意，我们通过.bind_tools让聊天模型访问我们之前创建的retrieve_tool：

```python
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model

response_model = init_chat_model("openai:gpt-4.1", temperature=0)


def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    response = (
        response_model
        .bind_tools([retriever_tool]).invoke(state["messages"])
    )
    return {"messages": [response]}
```

:::color5
**<font style="color:#601BDE;">测试需要语义搜索的问题： </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
input = {
    "messages": [
        {
            "role": "user",
            "content": "What does Lilian Weng say about types of reward hacking?",
        }
    ]
}
generate_query_or_respond(input)["messages"][-1].pretty_print()
```

:::color5
**<font style="color:#601BDE;">输出</font>**

:::

```python
================================== Ai Message ==================================
Tool Calls:
retrieve_blog_posts (call_tYQxgfIlnQUDMdtAhdbXNwIM)
Call ID: call_tYQxgfIlnQUDMdtAhdbXNwIM
Args:
query: types of reward hacking
```

# 4. 文档分级
:::color3
添加条件边--grade_documents--以确定检索到的文档是否与问题相关。**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

我们将使用具有结构化输出模式GradeDocuments的模型进行文档分级。grade_documents函数将根据评分决定（generate_answer或rewrite_question）返回要转到的节点的名称：

```python
from pydantic import BaseModel, Field
from typing import Literal

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
)


class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )


grader_model = init_chat_model("openai:gpt-4.1", temperature=0)


def grade_documents(
    state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """Determine whether the retrieved documents are relevant to the question."""
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments).invoke(
            [{"role": "user", "content": prompt}]
        )
    )
    score = response.binary_score

    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"
```

:::color5
**<font style="color:#601BDE;">测试相关文档</font>**

:::

```python
input = {
    "messages": convert_to_messages(
        [
            {
                "role": "user",
                "content": "What does Lilian Weng say about types of reward hacking?",
            },
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "1",
                        "name": "retrieve_blog_posts",
                        "args": {"query": "types of reward hacking"},
                    }
                ],
            },
            {
                "role": "tool",
                "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
                "tool_call_id": "1",
            },
        ]
    )
}
grade_documents(input)
```

# 5. 问题重写
:::color3
构建问题重写节点。

:::

检索工具可以返回可能不相关的文档，这表明需要改进原始用户问题。为此，我们将调用rewrite_question节点：

```python
REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)


def rewrite_question(state: MessagesState):
    """Rewrite the original user question."""
    messages = state["messages"]
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [{"role": "user", "content": response.content}]}
```

:::color5
**<font style="color:#601BDE;">测试输入 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
input = {
    "messages": convert_to_messages(
        [
            {
                "role": "user",
                "content": "What does Lilian Weng say about types of reward hacking?",
            },
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "1",
                        "name": "retrieve_blog_posts",
                        "args": {"query": "types of reward hacking"},
                    }
                ],
            },
            {"role": "tool", "content": "meow", "tool_call_id": "1"},
        ]
    )
}

response = rewrite_question(input)
print(response["messages"][-1]["content"])
```

:::color5
**<font style="color:#601BDE;">输出</font>**

:::

```python
What are the different types of reward hacking described by Lilian Weng, and how does she explain them?
```

# 6. 生成答案
:::color3
构建答案生成节点

:::

如果我们通过了评分器检查，我们可以根据原始问题和检索到的上下文生成最终答案：

```python
GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \n"
    "Context: {context}"
)


def generate_answer(state: MessagesState):
    """Generate an answer."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}
```

:::color5
**<font style="color:#601BDE;">测试输入 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
input = {
    "messages": convert_to_messages(
        [
            {
                "role": "user",
                "content": "What does Lilian Weng say about types of reward hacking?",
            },
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "1",
                        "name": "retrieve_blog_posts",
                        "args": {"query": "types of reward hacking"},
                    }
                ],
            },
            {
                "role": "tool",
                "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
                "tool_call_id": "1",
            },
        ]
    )
}

response = generate_answer(input)
response["messages"][-1].pretty_print()
```

:::color5
**<font style="color:#601BDE;">输出</font>**

:::

```python
================================== Ai Message ==================================

Lilian Weng categorizes reward hacking into two types: environment or goal misspecification, and reward tampering. She considers reward hacking as a broad concept that includes both of these categories. Reward hacking occurs when an agent exploits flaws or ambiguities in the reward function to achieve high rewards without performing the intended behaviors.
```

# 7. Graph构建
:::color3
构建langgraph的视图**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. 从generate_query_or_response开始，确定是否需要调用retrieve_tool。
2. 使用tools_condition路由到下一步：
    1. 如果generate_query_or_response返回了tool_calls，则调用retrieve_tool来检索上下文。
    2. 如过没有使用工具，直接回复用户。对检索到的文档内容与问题的相关性进行评分（Grade_documents），并转到下一步：
        1. 如果不相关，请使用rewrite_question重写问题，然后再次调用generate_query_or_response
        2. 如果相关，请继续生成e_answer，并使用ToolMessage和检索到的文档上下文生成最终响应

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

workflow = StateGraph(MessagesState)

# Define the nodes we will cycle between
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)

workflow.add_edge(START, "generate_query_or_respond")

# Decide whether to retrieve
workflow.add_conditional_edges(
    "generate_query_or_respond",
    # Assess LLM decision (call `retriever_tool` tool or respond to the user)
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "retrieve",
        END: END,
    },
)

# Edges taken after the `action` node is called.
workflow.add_conditional_edges(
    "retrieve",
    # Assess agent decision
    grade_documents,
)
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

# Compile
graph = workflow.compile()
```

:::color5
**<font style="color:#601BDE;">视图可视化</font>**

:::

```python
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760345777303-94680377-8a91-4efe-8f38-1b84c10657c1.png)

# 8. 运行agentic RAG
:::color3
运行langgraph视图

:::

```python
for chunk in graph.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "What does Lilian Weng say about types of reward hacking?",
            }
        ]
    }
):
    for node, update in chunk.items():
        print("Update from node", node)
        update["messages"][-1].pretty_print()
        print("\n\n")
```

:::color5
**<font style="color:#601BDE;">输出 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

```python
Update from node generate_query_or_respond
    ================================== Ai Message ==================================
    Tool Calls:
    retrieve_blog_posts (call_NYu2vq4km9nNNEFqJwefWKu1)
    Call ID: call_NYu2vq4km9nNNEFqJwefWKu1
    Args:
    query: types of reward hacking



    Update from node retrieve
    ================================= Tool Message ==================================
    Name: retrieve_blog_posts

    (Note: Some work defines reward tampering as a distinct category of misalignment behavior from reward hacking. But I consider reward hacking as a broader concept here.)
At a high level, reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering.

Why does Reward Hacking Exist?#

Pan et al. (2022) investigated reward hacking as a function of agent capabilities, including (1) model size, (2) action space resolution, (3) observation space noise, and (4) training time. They also proposed a taxonomy of three types of misspecified proxy rewards:

Let's Define Reward Hacking#
Reward shaping in RL is challenging. Reward hacking occurs when an RL agent exploits flaws or ambiguities in the reward function to obtain high rewards without genuinely learning the intended behaviors or completing the task as designed. In recent years, several related concepts have been proposed, all referring to some form of reward hacking:



Update from node generate_answer
================================== Ai Message ==================================

Lilian Weng categorizes reward hacking into two types: environment or goal misspecification, and reward tampering. She considers reward hacking as a broad concept that includes both of these categories. Reward hacking occurs when an agent exploits flaws or ambiguities in the reward function to achieve high rewards without performing the intended behaviors.
```



  


