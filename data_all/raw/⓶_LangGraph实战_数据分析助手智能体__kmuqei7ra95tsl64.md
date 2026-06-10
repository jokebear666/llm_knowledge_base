# ⓶ LangGraph实战：数据分析助手智能体

<!-- source: yuque://zhongxian-iiot9/hlyypb/kmuqei7ra95tsl64 -->

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">本期我们将通过一个实战项目，带大家使用 LangGraph 搭建一个使用自然语言操作数据库查询和分析的智能数据分析助手，并将其接入 Agent Chat UI 界面。通过这个完整案例，你将进一步掌握 LangGraph 的全流程开发能力，轻松应对日常工作中编写 SQL 语句的难题，提升数据处理效率。</font>

:::

## <font style="color:rgb(25, 27, 31);">LangGraph 智能数据分析助手架构</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">LangGraph智能数据分析助手的架构如下图所示，开发使用的大模型是</font>`[<font style="color:rgb(9, 64, 142);">DeepSeek-3.1</font>](https://zhida.zhihu.com/search?content_id=263120832&content_type=Article&match_order=1&q=DeepSeek-3.1&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">，Agent使用LangGraph高阶预构建图的API </font>`<font style="color:rgb(25, 27, 31);">create_react_agent</font>`<font style="color:rgb(25, 27, 31);">。数据分析助手最重要的两个工具是</font>`[<font style="color:rgb(9, 64, 142);">NL2Python</font>](https://zhida.zhihu.com/search?content_id=263120832&content_type=Article&match_order=1&q=NL2Python&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">和</font>`[<font style="color:rgb(9, 64, 142);">NL2SQL</font>](https://zhida.zhihu.com/search?content_id=263120832&content_type=Article&match_order=1&q=NL2SQL&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">, 借助大模型将自然语言转化为SQL语句，并使用Python解释器执行代码。</font>

:::

:::color5
**<font style="color:#601BDE;">1.整体架构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">项目完成编写后我们使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LangGraph cli</font>`<font style="color:rgb(25, 27, 31);">一键本地部署，同时使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LangSmith</font>`<font style="color:rgb(25, 27, 31);">和</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LangGraph Studio</font>`<font style="color:rgb(25, 27, 31);">进行可视化调试。前端框架我们使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Agent Chat UI</font>`<font style="color:rgb(25, 27, 31);">快速对接服务并构建应用。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764301322695-94e104d7-282c-48eb-8ac5-e7c3d959bcde.png)

## <font style="color:rgb(25, 27, 31);">NL2SQL，NL2Python工具函数编写流程</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">新建</font>`<font style="color:rgb(25, 27, 31);">langgrapn_dataanalysis</font>`<font style="color:rgb(25, 27, 31);">文件夹作为项目目录，在文件夹中新建</font>`<font style="color:rgb(25, 27, 31);">graph.py</font>`<font style="color:rgb(25, 27, 31);">用于编写智能体相关的代码, 新建</font>`<font style="color:rgb(25, 27, 31);">requirements.txt</font>`<font style="color:rgb(25, 27, 31);">用于写入依赖库，新建</font>`<font style="color:rgb(25, 27, 31);">.env</font>`<font style="color:rgb(25, 27, 31);">文件用于写入环境变量，</font>`<font style="color:rgb(25, 27, 31);">langgraph.json</font>`<font style="color:rgb(25, 27, 31);">设置项目的依赖配置。同时本项目需要提前安装完成</font>`<font style="color:rgb(25, 27, 31);">mysql</font>`<font style="color:rgb(25, 27, 31);">数据库，默认大家已经安装。</font>

<font style="color:rgb(25, 27, 31);">未安装mysql大家可参考博客:</font>[<font style="color:rgb(9, 64, 142);">MySQL安装和配置教程（超详细版本）</font>](https://zhuanlan.zhihu.com/p/654087404)%E3%80%82)

:::

### <font style="color:rgb(25, 27, 31);">安装依赖环境</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">requirements.txt</font>`<font style="color:rgb(25, 27, 31);">中写入依赖的Python函数库如下, 在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">anaconda</font>`<font style="color:rgb(25, 27, 31);">虚拟环境</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">langgraphenv</font>`<font style="color:rgb(25, 27, 31);">中执行</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pip install -r requirements.txt</font>`<font style="color:rgb(25, 27, 31);">安装虚拟环境。</font>

:::

:::color5
**<font style="color:#601BDE;">1.依赖环境</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
pip install -r requirements.txt
```

```python
langgraph
langchain-core
langchain-deepseek
langchain-tavily
python-dotenv
langsmith
pydantic
matplotlib
seaborn
pandas
IPython
langchain_mcp_adapters
uv
pymysql
```



### <font style="color:rgb(25, 27, 31);">环境变量编写</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">.env</font>`<font style="color:rgb(25, 27, 31);">文件中写入环境变量如下</font>

<font style="color:rgb(25, 27, 31);">关于langsmith的相关配置和api_key的申请可参考</font>[<font style="color:rgb(9, 64, 142);">LangGraph开发工具使用</font>](https://zhuanlan.zhihu.com/p/1948890741226050365)

:::

:::color5
**<font style="color:#601BDE;">1.环境变量</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
DEEPSEEK_API_KEY=你注册的deepseek api key
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=你注册的langsmith api key
LANGSMITH_PROJECT=langgraph_data_analysis
HOST=localhost
USER=你的mysql用户名
MYSQL_PW=你的mysql数据库密码
DB_NAME=你的mysql数据库名称
PORT=你的mysql端口
```

### <font style="color:rgb(25, 27, 31);">数据库相关工具编写</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">graph.py</font>`<font style="color:rgb(25, 27, 31);">文件中引入相关依赖:</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">相关依赖</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import matplotlib
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pymysql

# 加载环境变量
load_dotenv(override=True)
```

:::color5
**<font style="color:#601BDE;">2.SQL查询</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">graph.py</font>`<font style="color:rgb(25, 27, 31);">中编写函数</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">sql_inter</font>`<font style="color:rgb(25, 27, 31);">用于执行MySQL数据库的查询工作。具体逻辑是首先使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pymysql</font>`<font style="color:rgb(25, 27, 31);">连接好数据库服务器，然后执行大模型生成的SQL语句完成相关动作。</font>

```python
# 创建SQL查询工具
description = """
当用户需要进行数据库查询工作时，请调用该函数。
该函数用于在指定MySQL服务器上运行一段SQL代码，完成数据查询相关工作，
并且当前函数是使用pymsql连接MySQL数据库。
本函数只负责运行SQL代码并进行数据查询，若要进行数据提取，则使用另一个extract_data函数。
"""


# 定义结构化参数模型
class SQLQuerySchema(BaseModel):
    sql_query: str = Field(description=description)


# 封装为 LangGraph 工具
@tool(args_schema=SQLQuerySchema)
def sql_inter(sql_query: str) -> str:
    """
    当用户需要进行数据库查询工作时，请调用该函数。
    该函数用于在指定MySQL服务器上运行一段SQL代码，完成数据查询相关工作，
    并且当前函数是使用pymsql连接MySQL数据库。
    本函数只负责运行SQL代码并进行数据查询，若要进行数据提取，则使用另一个extract_data函数。
    :param sql_query: 字符串形式的SQL查询语句，用于执行对MySQL中telco_db数据库中各张表进行查询，并获得各表中的各类相关信息
    :return：sql_query在MySQL中的运行结果。
    """
    # print("正在调用 sql_inter 工具运行 SQL 查询...")

    # 加载环境变量
    load_dotenv(override=True)
    host = os.getenv('HOST')
    user = os.getenv('USER')
    mysql_pw = os.getenv('MYSQL_PW')
    db = os.getenv('DB_NAME')
    port = os.getenv('PORT')

    # 创建连接
    connection = pymysql.connect(
        host=host,
        user=user,
        passwd=mysql_pw,
        db=db,
        port=int(port),
        charset='utf8'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            # print("SQL 查询已成功执行，正在整理结果...")
    finally:
        connection.close()

    # 将结果以 JSON 字符串形式返回
    return json.dumps(results, ensure_ascii=False)
```

:::color5
**<font style="color:#601BDE;">3.数据提取工具</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">graph.py</font>`<font style="color:rgb(25, 27, 31);">中编写函数</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">extract_data</font>`<font style="color:rgb(25, 27, 31);">用于提取查询出数据表中的相关数据，并将提取的结果作为</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pandas</font>`<font style="color:rgb(25, 27, 31);">对象保存在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">df_name</font>`<font style="color:rgb(25, 27, 31);">变量中。这里可能有同学要问为什么要分开编写数据库相关的函数呢？这是因为对于外部函数的功能细分往往会带来更加稳定的智能体执行效果，设想一个函数包含很多的参数和逻辑，大模型在选择函数和生成的参数时出错的概率自然会变大。</font>

```python
# 创建数据提取工具
# 定义结构化参数
class ExtractQuerySchema(BaseModel):
    sql_query: str = Field(description="用于从 MySQL 提取数据的 SQL 查询语句。")
    df_name: str = Field(description="指定用于保存结果的 pandas 变量名称（字符串形式）。")


# 注册为 Agent 工具
@tool(args_schema=ExtractQuerySchema)
def extract_data(sql_query: str, df_name: str) -> str:
    """
    用于在MySQL数据库中提取一张表到当前Python环境中，注意，本函数只负责数据表的提取，
    并不负责数据查询，若需要在MySQL中进行数据查询，请使用sql_inter函数。
    同时需要注意，编写外部函数的参数消息时，必须是满足json格式的字符串，
    :param sql_query: 字符串形式的SQL查询语句，用于提取MySQL中的某张表。
    :param df_name: 将MySQL数据库中提取的表格进行本地保存时的变量名，以字符串形式表示。
    :return：表格读取和保存结果
    """
    print("正在调用 extract_data 工具运行 SQL 查询...")

    load_dotenv(override=True)
    host = os.getenv('HOST')
    user = os.getenv('USER')
    mysql_pw = os.getenv('MYSQL_PW')
    db = os.getenv('DB_NAME')
    port = os.getenv('PORT')

    # 创建数据库连接
    connection = pymysql.connect(
        host=host,
        user=user,
        passwd=mysql_pw,
        db=db,
        port=int(port),
        charset='utf8'
    )

    try:
        # 执行 SQL 并保存为全局变量
        df = pd.read_sql(sql_query, connection)
        globals()[df_name] = df
        # print("数据成功提取并保存为全局变量：", df_name)
        return f"成功创建 pandas 对象 `{df_name}`，包含从 MySQL 提取的数据。"
    except Exception as e:
        return f"执行失败：{e}"
    finally:
        connection.close()
```

### <font style="color:rgb(25, 27, 31);">Python解释器相关工具的编写</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">graph.py</font>`<font style="color:rgb(25, 27, 31);">文件中编写Python代码解释器相关的工具。考虑到实际应用情况，这里同样编写两个外部函数，分别用于执行普通的Pyhton代码和绘图类代码</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">python_inter	</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">这里首先编写</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">python_inter</font>`<font style="color:rgb(25, 27, 31);">用于执行普通python类代码（</font>**<font style="color:rgb(25, 27, 31);">注意：</font>**<font style="color:rgb(25, 27, 31);"> 在代码执行过程中容易出现对全局变量重复赋值的情况，可以在异常中捕获并处理相关情况）</font>

```python
# 创建Python代码执行工具
# Python代码执行工具结构化参数说明
class PythonCodeInput(BaseModel):
    py_code: str = Field(description="一段合法的 Python 代码字符串，例如 '2 + 2' 或 'x = 3\ny = x * 2'")


@tool(args_schema=PythonCodeInput)
def python_inter(py_code):
    """
    当用户需要编写Python程序并执行时，请调用该函数。
    该函数可以执行一段Python代码并返回最终结果，需要注意，本函数只能执行非绘图类的代码，若是绘图相关代码，则需要调用fig_inter函数运行。
    """
    g = globals()
    try:
        # 尝试如果是表达式，则返回表达式运行结果
        return str(eval(py_code, g))
    # 若报错，则先测试是否是对相同变量重复赋值
    except Exception as e:
        global_vars_before = set(g.keys())
        try:
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        # 若存在新变量
        if new_vars:
            result = {var: g[var] for var in new_vars}
            # print("代码已顺利执行，正在进行结果梳理...")
            return str(result)
        else:
            # print("代码已顺利执行，正在进行结果梳理...")
            return "已经顺利执行代码"
```

:::color5
**<font style="color:#601BDE;">2.</font>**`**<font style="color:#601BDE;">fig_inter</font>**`<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">graph.py</font>`<font style="color:rgb(25, 27, 31);">文件中编写执行可视化Python代码的相关函数</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">fig_inter</font>`<font style="color:rgb(25, 27, 31);">，注意</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">fig_inter</font>`<font style="color:rgb(25, 27, 31);">函数需要两个参数，一个是</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">py_code</font>`<font style="color:rgb(25, 27, 31);">表示需要运行的python绘图代码，另一个是</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">fname</font>`<font style="color:rgb(25, 27, 31);">表示最后要输出的图像对象的文件名。</font>

<font style="color:rgb(25, 27, 31);">（</font>**<font style="color:rgb(25, 27, 31);">注意:</font>**<font style="color:rgb(25, 27, 31);"> 要自定义图片存放的文件夹到Agent Chat UI的文件夹中，因为</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Agent Chat UI</font>`<font style="color:rgb(25, 27, 31);">前端只能从指定的文件夹中渲染图片）。</font>

```python
# 创建绘图工具
# 绘图工具结构化参数说明
class FigCodeInput(BaseModel):
    py_code: str = Field(description="要执行的 Python 绘图代码，必须使用 matplotlib/seaborn 创建图像并赋值给变量")
    fname: str = Field(description="图像对象的变量名，例如 'fig'，用于从代码中提取并保存为图片")


@tool(args_schema=FigCodeInput)
def fig_inter(py_code: str, fname: str) -> str:
    """
    当用户需要使用 Python 进行可视化绘图任务时，请调用该函数。

    注意：
    1. 所有绘图代码必须创建一个图像对象，并将其赋值为指定变量名（例如 `fig`）。
    2. 必须使用 `fig = plt.figure()` 或 `fig = plt.subplots()`。
    3. 不要使用 `plt.show()`。
    4. 请确保代码最后调用 `fig.tight_layout()`。
    5. 所有绘图代码中，坐标轴标签（xlabel、ylabel）、标题（title）、图例（legend）等文本内容，必须使用英文描述。

    示例代码：
    fig = plt.figure(figsize=(10,6))
    plt.plot([1,2,3], [4,5,6])
    fig.tight_layout()
    """
    # print("正在调用fig_inter工具运行Python代码...")

    current_backend = matplotlib.get_backend()
    matplotlib.use('Agg')

    local_vars = {"plt": plt, "pd": pd, "sns": sns}

    # 设置图像保存路径（这里一定要设置为前端agent chat ui文件夹中的public目录下）
    base_dir = r"D:\Learning\Learning\大模型\LangChain\Python\langgraph_dataanalysis\agent-chat-ui-main\public\\"
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)  # 自动创建 images 文件夹（如不存在）

    try:
        g = globals()
        exec(py_code, g, local_vars)
        g.update(local_vars)

        fig = local_vars.get(fname, None)
        if fig:
            image_filename = f"{fname}.png"
            abs_path = os.path.join(images_dir, image_filename)  # 绝对路径
            rel_path = os.path.join("images", image_filename)  # 返回相对路径（给前端用）

            fig.savefig(abs_path, bbox_inches='tight')
            return f"图片已保存，路径为: {rel_path}"
        else:
            return "图像对象未找到，请确认变量名正确并为 matplotlib 图对象。"
    except Exception as e:
        return f"执行失败：{e}"
    finally:
        plt.close('all')
        matplotlib.use(current_backend)
```

### <font style="color:rgb(25, 27, 31);">提示词及工具组件的封装</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">工具函数已经编写完全，接下来只要定义大模型和提示词即可利用</font>`<font style="color:rgb(25, 27, 31);">create_react_agent</font>`<font style="color:rgb(25, 27, 31);">预构建图API来定义图结构智能体了。为确保工具调用的准确性，我们编写了复杂的提示词定义了大模型角色、功能、可用工具及其优先级等。</font>

:::

:::color5
**<font style="color:#601BDE;">1.Prompt构建</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
# 创建提示词模板
prompt = """
你是一名经验丰富的智能数据分析助手，擅长帮助用户高效完成以下任务：

1. **数据库查询：**
   - 当用户需要获取数据库中某些数据或进行SQL查询时，请调用`sql_inter`工具，该工具已经内置了pymysql连接MySQL数据库的全部参数，包括数据库名称、用户名、密码、端口等，你只需要根据用户需求生成SQL语句即可。
   - 你需要准确根据用户请求生成SQL语句，例如 `SELECT * FROM 表名` 或包含条件的查询。

2. **数据表提取：**
   - 当用户希望将数据库中的表格导入Python环境进行后续分析时，请调用`extract_data`工具。
   - 你需要根据用户提供的表名或查询条件生成SQL查询语句，并将数据保存到指定的pandas变量中。

3. **非绘图类任务的Python代码执行：**
   - 当用户需要执行Python脚本或进行数据处理、统计计算时，请调用`python_inter`工具。
   - 仅限执行非绘图类代码，例如变量定义、数据分析等。

4. **绘图类Python代码执行：**
   - 当用户需要进行可视化展示（如生成图表、绘制分布等）时，请调用`fig_inter`工具。
   - 你可以直接读取数据并进行绘图，不需要借助`python_inter`工具读取图片。
   - 你应根据用户需求编写绘图代码，并正确指定绘图对象变量名（如 `fig`）。
   - 当你生成Python绘图代码时必须指明图像的名称，如fig = plt.figure()或fig = plt.subplots()创建图像对象，并赋值为fig。
   - 不要调用plt.show()，否则图像将无法保存。

**工具使用优先级：**
- 如需数据库数据，请先使用`sql_inter`或`extract_data`获取，再执行Python分析或绘图。
- 如需绘图，请先确保数据已加载为pandas对象。

**回答要求：**
- 所有回答均使用**简体中文**，清晰、礼貌、简洁。
- 如果调用工具返回结构化JSON数据，你应提取其中的关键信息简要说明，并展示主要结果。
- 若需要用户提供更多信息，请主动提出明确的问题。
- 如果有生成的图片文件，请务必在回答中使用Markdown格式插入图片，如：![Categorical Features vs Churn](images/fig.png)
- 不要仅输出图片路径文字。

**风格：**
- 专业、简洁、以数据驱动。
- 不要编造不存在的工具或数据。

请根据以上原则为用户提供精准、高效的协助。
"""

# 创建工具列表
tools = [python_inter, fig_inter, sql_inter, extract_data]

# 创建模型
model = ChatDeepSeek(model="deepseek-chat")

# 创建图 （Agent）
graph = create_react_agent(model=model, tools=tools, prompt=prompt)
```

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">langgraph配置</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);"> 在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">langgraph.json</font>`<font style="color:rgb(25, 27, 31);">文件中写入如下配置，定义当前Agent的名称为</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">data_agent</font>`<font style="color:rgb(25, 27, 31);">:</font>

```python
{
    "dependencies": [" ./"],
    "graphs":{
        "data_agent": "./graph.py:graph"
    },
    "env": ".env"
}
```

## <font style="color:rgb(25, 27, 31);">数据助手智能体部署上线</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在项目文件夹</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">langgrapn_dataanalysis</font>`<font style="color:rgb(25, 27, 31);">下执行</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">langgraph dev</font>`<font style="color:rgb(25, 27, 31);">命令，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">langgraph-cli</font>`<font style="color:rgb(25, 27, 31);">即可自动开启后端服务。第一个url表示部署服务的api, 第二个url表示LangGraph Studio的地址，第三个url表示部署服务的api文档。</font>

:::

:::color5
**<font style="color:#601BDE;">1.启动agent</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
langgraph dev
```

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1764302524732-1a608101-f0a8-4087-8b4a-83ec4d7f6040.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);">我们首先访问第二个地址打开</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LangGraph Studio</font>`<font style="color:rgb(25, 27, 31);">的界面，输入“你好，好久不见，请介绍一下你自己”，可以看到智能体清晰认识到自己数据分析智能助手的定位。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1764302537640-d2efea0e-184f-4796-9336-0bb6e7d08ee5.tif?x-oss-process=image/format,png)

:::color5
**<font style="color:#601BDE;">2.Agent测试</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">简单测试一下我们数据助手调用工具函数的能力，我们输入指令：“帮我查询数据库中一共有几张表?", 可以看到LangGraph成功调用了</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">sql_inter</font>`<font style="color:rgb(25, 27, 31);">工具查询数据库中的表格，因为我们</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">test</font>`<font style="color:rgb(25, 27, 31);">数据库是新建的，所以其中并没有表，而我们已有的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">custom</font>`<font style="color:rgb(25, 27, 31);">数据库中有一张</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">customers</font>`<font style="color:rgb(25, 27, 31);">表，LangGraph返回的结果与预期正确。</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1764302544147-b56fff8d-7dc3-410e-8de7-a6d2ba140f99.tif?x-oss-process=image/format,png)

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1764302547433-c383e983-49cf-4df9-a161-b1afb7fd3e84.tif?x-oss-process=image/format,png)

<font style="color:rgb(25, 27, 31);"></font>





### <font style="color:rgb(25, 27, 31);">接入Agent Chat UI 前端应用</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">接下来我们围绕当前项目单独下载一个前端模板并运行，执行如下命令安装</font>`<font style="color:rgb(25, 27, 31);">agent-caht-ui</font>`<font style="color:rgb(25, 27, 31);">前端。（</font>**<font style="color:rgb(25, 27, 31);">注意：</font>**<font style="color:rgb(25, 27, 31);"> 使用</font>`<font style="color:rgb(25, 27, 31);">agent chat ui</font>`<font style="color:rgb(25, 27, 31);">前端需要安装npm, 大家可参考文章</font>[<font style="color:rgb(9, 64, 142);">出行规划Agent</font>](https://zhuanlan.zhihu.com/p/1941478487526446775)<font style="color:rgb(25, 27, 31);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.环境安装</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
git clone https://github.com/langchain-ai/agent-chat-ui.git //将agent-chat-ui 拉取到本地
cd agent-chat-ui // 进入agent-chat-ui项目目录
npm install // 安装agent-chat-ui相关依赖
npm run dev // 运行agent-chat-ui项目
```

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1764302678707-4c26244e-5665-4586-a65c-e0726a225bb2.tif?x-oss-process=image/format,png)

:::color5
**<font style="color:#601BDE;">2.进入前端页面</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">点击本地路径</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">http://localhost:3000</font>`<font style="color:rgb(25, 27, 31);">进入</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">agent-chat-ui</font>`<font style="color:rgb(25, 27, 31);">的相关网页，需要进行登录并测试，这里需要填写Agent名称，也就是我们在</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">langgraph.json</font>`<font style="color:rgb(25, 27, 31);">文件中定义的名称</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">data_agent</font>`<font style="color:rgb(25, 27, 31);">，并可选输入LangSmith的API Key，点击Continue即可顺利开启Agent Chat UI页面并进行对话</font>

<font style="color:rgb(25, 27, 31);">（</font>**<font style="color:rgb(25, 27, 31);">特别注意：</font>**<font style="color:rgb(25, 27, 31);"> 一定要将</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">graph.py</font>`<font style="color:rgb(25, 27, 31);">中图片的输出路径设置为</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">agent-chat-ui</font>`<font style="color:rgb(25, 27, 31);">文件夹中的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">public</font>`<font style="color:rgb(25, 27, 31);">文件夹）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764309729205-9ad0d16f-4645-42e8-8192-8550c56fdf72.png)



## <font style="color:rgb(25, 27, 31);">数据助手智能体项目演示</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">部署完成后我们需要尝试并实验</font>`<font style="color:rgb(25, 27, 31);">Agent Chat UI</font>`<font style="color:rgb(25, 27, 31);">的相关功能，测试数据是否可以被正确查询，是否可以执行正确代码得到可视化图表，可视化图表是否可以在前端正常展示。</font>

:::

:::color5
**<font style="color:#601BDE;">1.项目演示</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">输入指令：“查询test数据库中movies表中不同电影的电影评分，并绘制条形图展示，同时输出电影评分最高的电影及其主演和得分”</font>

<font style="color:rgb(25, 27, 31);">查看输出效果，可以看到智能体成功绘制了三部电影的电影评分并得到最高电影是“小电影，主演为苍进空"的正确结论。限于篇幅原因，这里就不再进行更多测试，大家可以在本地自行实现数据分析助手项目并完成更多的创意和测试。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764309741196-b66f6edc-de9c-4796-b6bf-ac84104b1191.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1764309750201-582d07f1-6cf6-435f-86bb-ce07c45507d4.png)

## <font style="color:rgb(25, 27, 31);">总结</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">本篇分享带大家从0到1搭建具备前端可视化功能的数据分析助手智能体，可以将我们的自然语言自动转化为SQL语句并执行操作，大大辅助了数据科学人员的日常工作。同时该智能体可自动执行代码并完成对从数据库中提取数据的分析和可视化，希望大家在亲自动手编写的过程中可以复习我们LangGraph全生态工具的开发流程，并以此创造性的编写更多有趣好用的智能体。</font>

:::





**<font style="color:rgb(255, 255, 255);">送礼物</font>**





  


