# ⓹ MCP实战入门：让大模型获取实时天气信息

<!-- source: yuque://zhongxian-iiot9/hlyypb/hkxed3ni9d6i31ok -->

:::color1
**<font style="color:rgb(63, 63, 63);">背景：</font>**<font style="color:rgb(63, 63, 63);">本文将带您了解大模型上下文协议(Model Context Protocol, MCP)，并通过一个获取实时天气信息的实战项目，手把手教您如何实现AI模型与外部工具的无缝交互。</font>

:::

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">1.什么是Model Context Protocol (MCP)?</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">MCP （Model Context Protocol，模型上下文协议）定义了应用程序和 AI 模型之间交换上下文信息的方式。这使得开发者能够</font>**<font style="color:rgb(25, 27, 31);">以一致的方式将各种数据源、工具和功能连接到 AI 模型</font>**<font style="color:rgb(25, 27, 31);">（一个中间协议层），就像 </font>**<font style="color:#ED740C;">USB-C </font>**<font style="color:rgb(25, 27, 31);">让不同设备能够通过相同的接口连接一样。MCP 的目标是创建一个</font>**<font style="color:#ED740C;">通用标准，使 AI 应用程序的开发和集成变得更加简单和统一。</font>**MCP<font style="color:rgb(25, 27, 31);">为LLM提供了</font>**<font style="color:#ED740C;">一套标准化协议</font>**<font style="color:rgb(25, 27, 31);">，旨在为LLM方便调用各类数据源和工具</font>

+ **<font style="color:rgb(63, 63, 63);">MCP官方文档</font>**<font style="color:rgb(63, 63, 63);">：</font>[https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
+ **<font style="color:rgb(63, 63, 63);">MCP快速入门</font>**<font style="color:rgb(63, 63, 63);">：</font>[https://modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
+ **<font style="color:rgb(63, 63, 63);">项目源码</font>**<font style="color:rgb(63, 63, 63);">：</font>[https://github.com/FlyAIBox/mcp-in-action/tree/qweather_0.1/mcp_demo](https://github.com/FlyAIBox/mcp-in-action/tree/qweather_0.1/mcp_demo)
+ **<font style="color:rgb(63, 63, 63);">和风天气API</font>**<font style="color:rgb(63, 63, 63);">：</font>[https://dev.qweather.com/](https://dev.qweather.com/)

:::

:::success
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743952374832-99ebc1ab-cf55-4cb9-8b8f-21ae8fb434a6.png)

:::

:::success
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742873867932-067648a6-c67a-421e-8d24-f49f284f0e0b.png)

:::

:::color5
**<font style="color:#601BDE;">1.MCP的优点</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">MCP (Model Context Protocol) 代表了 AI 与外部工具和数据交互的标准建立。</font><font style="color:#D22D8D;"></font>

1. **<font style="color:rgb(25, 27, 31);">MCP 的本质</font>**<font style="color:rgb(25, 27, 31);">：它是一个统一的协议标准，使 AI 模型能够以一致的方式连接各种数据源和工具，类似于 AI 世界的"USB-C"接口。</font>
2. **<font style="color:rgb(25, 27, 31);">MCP 的价值</font>**<font style="color:rgb(25, 27, 31);">：它解决了传统 function call 的平台依赖问题，提供了更统一、开放、安全、灵活的工具调用机制，让用户和开发者都能从中受益。</font>
3. **<font style="color:rgb(25, 27, 31);">使用与开发</font>**<font style="color:rgb(25, 27, 31);">：对于普通用户，MCP 提供了丰富的现成工具，</font>**<font style="color:rgb(25, 27, 31);">用户可以在不了解任何技术细节的情况下使用</font>**<font style="color:rgb(25, 27, 31);">；对于开发者，MCP 提供了清晰的架构和 SDK，使工具开发变得相对简单。</font>

<font style="color:rgb(25, 27, 31);">MCP 还处于发展初期，但其潜力巨大。更重要的是生态吧，基于统一标准下构筑的生态也会正向的促进整个领域的发展。</font>



## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">2.为什么需要MCP？对比传统方法</font>
:::color5
**<font style="color:#601BDE;">1.大模型与外界交互的方式</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

| **<font style="color:rgb(63, 63, 63);">特性</font>** | **<font style="color:rgb(63, 63, 63);">传统REST API</font>** | **<font style="color:rgb(63, 63, 63);">Function Calling</font>** | **<font style="color:rgb(63, 63, 63);">MCP</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(63, 63, 63);">实现方式</font> | <font style="color:rgb(63, 63, 63);">直接调用HTTP接口</font> | <font style="color:rgb(63, 63, 63);">模型输出JSON格式工具调用</font> | <font style="color:rgb(63, 63, 63);">标准化协议</font> |
| <font style="color:rgb(63, 63, 63);">安全性</font> | <font style="color:rgb(63, 63, 63);">中等（需手动处理）</font> | <font style="color:rgb(63, 63, 63);">中等（解析不稳定）</font> | <font style="color:rgb(63, 63, 63);">高（沙箱隔离）</font> |
| <font style="color:rgb(63, 63, 63);">集成难度</font> | <font style="color:rgb(63, 63, 63);">高（需自行实现）</font> | <font style="color:rgb(63, 63, 63);">中等（需处理解析错误）</font> | <font style="color:rgb(63, 63, 63);">低（标准接口）</font> |
| <font style="color:rgb(63, 63, 63);">交互方式</font> | <font style="color:rgb(63, 63, 63);">异步、单向</font> | <font style="color:rgb(63, 63, 63);">半同步</font> | <font style="color:rgb(63, 63, 63);">同步、双向</font> |
| <font style="color:rgb(63, 63, 63);">上下文感知</font> | <font style="color:rgb(63, 63, 63);">无</font> | <font style="color:rgb(63, 63, 63);">有限</font> | <font style="color:rgb(63, 63, 63);">完整</font> |
| <font style="color:rgb(63, 63, 63);">适用场景</font> | <font style="color:rgb(63, 63, 63);">简单集成</font> | <font style="color:rgb(63, 63, 63);">单次调用</font> | <font style="color:rgb(63, 63, 63);">复杂工具链</font> |


:::color5
**<font style="color:#601BDE;">2.传统REST API的局限</font>**<font style="color:#D22D8D;"></font>

:::

<font style="color:rgb(63, 63, 63);">传统方式中，开发者需要：</font>

1. <font style="color:rgb(63, 63, 63);">解析模型输出</font>
2. <font style="color:rgb(63, 63, 63);">识别API调用意图</font>
3. <font style="color:rgb(63, 63, 63);">手动构造API请求</font>
4. <font style="color:rgb(63, 63, 63);">将结果返回给模型</font>

<font style="color:rgb(63, 63, 63);">这种方式不仅繁琐，而且容易出错，特别是当需要处理多个API调用或复杂逻辑时。</font>

:::color5
**<font style="color:#601BDE;">3.Function Calling的进步与局限</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);">Function Calling（如OpenAI的函数调用或Anthropic的Tool Use）是一种改进，</font>**<font style="color:#74B602;">模型可以直接输出结构化的JSON来表示函数调用意图</font>**<font style="color:rgb(63, 63, 63);">。但它仍有局限：</font>

1. <font style="color:rgb(63, 63, 63);">输出格式不稳定，</font>**<font style="color:#117CEE;">需要额外验证和错误处理</font>**
2. <font style="color:rgb(63, 63, 63);">安全边界模糊，需要开发者自行实现安全措施</font>
3. <font style="color:rgb(63, 63, 63);">缺乏标准化，不同模型实现差异大</font>

:::color5
**<font style="color:#601BDE;">4.MCP的优势</font>**<font style="color:#D22D8D;"></font>

:::

<font style="color:rgb(63, 63, 63);">MCP通过标准化协议解决了上述问题：</font>

1. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">标准接口</font>**<font style="color:rgb(63, 63, 63);">：提供统一的工具定义和调用方式</font>
2. **<font style="color:rgb(0, 152, 116);">安全隔离</font>**<font style="color:rgb(63, 63, 63);">：工具在沙箱环境中执行，减少安全风险</font>
3. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">双向通信</font>**<font style="color:rgb(63, 63, 63);">：模型和工具可以进行实时交互</font>
4. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">环境感知</font>**<font style="color:rgb(63, 63, 63);">：工具可以访问完整上下文</font>
5. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">简化开发</font>**<font style="color:rgb(63, 63, 63);">：开发者只需实现工具逻辑，协议处理由MCP框架管理</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">3.MCP天气工具实战项目</font>
:::color3
**<font style="color:rgb(63, 63, 63);">简介：</font>**<font style="color:rgb(63, 63, 63);">下面，我们将通过一个实际项目，展示如何使用MCP创建一个天气信息工具，让AI模型能够查询实时天气数据。</font>

:::

:::color5
**<font style="color:#601BDE;">1.项目介绍</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);">这是一个基于MCP的天气工具演示项目，通过和风天气API获取实时天气数据，提供以下功能：</font>

1. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">天气预警查询</font>**<font style="color:rgb(63, 63, 63);">：获取指定城市的天气灾害预警信息</font>
2. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">天气预报查询</font>**<font style="color:rgb(63, 63, 63);">：获取指定城市未来几天的天气预报</font>

:::color5
**<font style="color:#601BDE;">2.项目架构</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);">项目分为三个主要部分：</font>

```plain
┌─────────────┐     stdio    ┌──────────────┐
│             │◄────────────►│              │
│  MCP 客户端  │              │  MCP 服务器   │
│             │              │              │
└─────────────┘              └──────────────┘
                                   ▲
                                   │
                              调试 │
                                   │
                                   ▼
                            ┌─────────────┐
                            │             │
                            │MCP Inspector│
                            │             │
                            └─────────────┘
```

1. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">MCP服务器</font>**<font style="color:rgb(63, 63, 63);">：提供天气工具的核心实现</font>
2. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">MCP客户端</font>**<font style="color:rgb(63, 63, 63);">：连接服务器，发送工具调用请求</font>
3. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">MCP Inspector</font>**<font style="color:rgb(63, 63, 63);">：用于调试和测试服务器</font>

:::color5
**<font style="color:#601BDE;">3.环境准备</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);">开始前，我们需要准备以下环境：</font>

+ <font style="color:rgb(63, 63, 63);">Python 3.10.12 或更高版本</font>
+ <font style="color:rgb(63, 63, 63);">NodeJS 22.14.0+ 和 NPM 10.9.2+（用于MCP Inspector）</font>
+ <font style="color:rgb(63, 63, 63);">和风天气API Key和API Host（</font><font style="color:rgb(87, 107, 149);">注册地址</font><sup><font style="color:rgb(87, 107, 149);">[1]</font></sup><font style="color:rgb(63, 63, 63);">）【具体流程参考文末】</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">4.实战步骤</font>
:::color5
**<font style="color:#601BDE;">1.第一步：创建MCP服务器</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);">MCP服务器是提供工具功能的核心部分。以下是实现天气服务器的核心代码：</font>

```python
import os
import json
import httpx
import asyncio
from dotenv import load_dotenv
from modelcontextprotocol.server import (
create_server,
ServerConfig,
tools,
JsonSchema,
)

# 加载环境变量
load_dotenv()
API_KEY = os.getenv("QWEATHER_API_KEY")
API_HOST = os.getenv("QWEATHER_API_HOST", "https://XXX.qweather.com")

# 定义天气预警工具
@tools.tool(
    name="get_weather_warning",
    description="获取指定位置的天气灾害预警",
    parameters=JsonSchema(
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市ID或经纬度坐标（经度,纬度）\n例如：'101010100'（北京）或 '116.41,39.92'",
                },
            },
            "required": ["location"],
        }
    ),
)
asyncdefget_weather_warning(location: str) -> str:
    """
    获取指定位置的天气灾害预警
    
    参数:
        location: 城市ID或经纬度坐标（经度,纬度）
                例如：'101010100'（北京）或 '116.41,39.92'
        
    返回:
        格式化的预警信息字符串
    """
    asyncwith httpx.AsyncClient() as client:
    response = await client.get(
        f"{API_HOST}/v7/warning/now",
        params={
            "location": location,
            "key": API_KEY,
            "lang": "zh",
        },
    )
    data = response.json()

if data["code"] != "200":
    returnf"获取天气预警失败: {data['code']}"

    warnings = data.get("warning", [])
ifnot warnings:
return"当前没有天气预警信息"

result = []
for warning in warnings:
    result.append(
        f"预警ID: {warning['id']}\n"
        f"标题: {warning['title']}\n"
        f"发布时间: {warning['pubTime']}\n"
        f"开始时间: {warning['startTime']}\n"
        f"结束时间: {warning['endTime']}\n"
        f"预警类型: {warning['typeName']}\n"
        f"预警等级: {warning['severityName']} ({warning['level']})\n"
        f"发布单位: {warning['sender']}\n"
        f"状态: {warning['status']}\n"
        f"详细信息: {warning['text']}"
    )

    return"\n\n".join(result)

# 定义天气预报工具
@tools.tool(
    name="get_daily_forecast",
    description="获取指定位置的天气预报",
    parameters=JsonSchema(
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市ID或经纬度坐标（经度,纬度）\n例如：'101010100'（北京）或 '116.41,39.92'",
                },
                "days": {
                    "type": "integer",
                    "description": "预报天数，可选值为 3、7、10、15、30，默认为 3",
                    "enum": [3, 7, 10, 15, 30],
                    "default": 3,
                },
            },
            "required": ["location"],
        }
    ),
)
asyncdefget_daily_forecast(location: str, days: int = 3) -> str:
    """
    获取指定位置的天气预报
    
    参数:
        location: 城市ID或经纬度坐标（经度,纬度）
                例如：'101010100'（北京）或 '116.41,39.92'
        days: 预报天数，可选值为 3、7、10、15、30，默认为 3
        
    返回:
        格式化的天气预报字符串
    """
    # 根据天数选择API版本
    version = "3d"if days == 3else"7d"if days == 7else"10d"if days in [10, 15, 30] else"3d"
    
    asyncwith httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_HOST}/v7/weather/{version}",
            params={
                "location": location,
                "key": API_KEY,
                "lang": "zh",
            },
        )
        data = response.json()
        
        if data["code"] != "200":
            returnf"获取天气预报失败: {data['code']}"
        
        daily = data.get("daily", [])
        ifnot daily:
            return"无法获取天气预报信息"
            
        result = []
        for day in daily[:days]:  # 限制天数
            result.append(
                f"日期: {day['fxDate']}\n"
                f"日出: {day['sunrise']}  日落: {day['sunset']}\n"
                f"最高温度: {day['tempMax']}°C  最低温度: {day['tempMin']}°C\n"
                f"白天天气: {day['textDay']}  夜间天气: {day['textNight']}\n"
                f"白天风向: {day['windDirDay']} {day['windScaleDay']}级 ({day['windSpeedDay']}km/h)\n"
                f"夜间风向: {day['windDirNight']} {day['windScaleNight']}级 ({day['windSpeedNight']}km/h)\n"
                f"相对湿度: {day['humidity']}%\n"
                f"降水量: {day['precip']}mm\n"
                f"紫外线指数: {day['uvIndex']}\n"
                f"能见度: {day['vis']}km"
            )
        
        return"\n\n---\n\n".join(result)

# 主函数
asyncdefmain():
    config = ServerConfig()
    server = create_server(config)
    
    # 注册工具
    server.register_tool(get_weather_warning)
    server.register_tool(get_daily_forecast)
    
    # 启动服务器
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

:::color5
**<font style="color:#601BDE;">2.第二步：实现MCP客户端</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);">MCP客户端用于连接服务器并调用工具。以下是客户端的实现：</font>

```python
import asyncio
import json
import os
import signal
import subprocess
import sys
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE

from modelcontextprotocol.client import create_client, ClientConfig
from modelcontextprotocol.protocol.tool_schemas import ToolSchema

# 启动服务器进程
asyncdefstart_server_process():
server_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "server", "weather_server.py")
returnawait create_subprocess_exec(
    sys.executable, server_path,
    stdin=PIPE, stdout=PIPE, stderr=PIPE
)

# 主函数
asyncdefmain():
print("启动 MCP 服务器进程...")
server_process = await start_server_process()

# 配置客户端
config = ClientConfig()
client = create_client(config)

try:
    # 连接到服务器
    await client.connect_process(server_process)

    # 获取可用工具
    tools = await client.get_tools()
    print(f"已连接到服务器，可用工具: {len(tools)}")

    # 显示工具信息
    for tool in tools:
        print(f"  - {tool.name}: \n{tool.description}\n")

        print("使用 'help' 查看帮助，使用 'exit' 退出\n")

    # 命令行交互循环
    whileTrue:
    user_input = input("> ").strip()

    if user_input.lower() == "exit":
        break

    elif user_input.lower() == "help":
        print("\n可用命令:")
        print("  help - 显示此帮助信息")
        print("  list - 列出可用工具")
        print("  call <工具名> <参数JSON> - 调用工具")
        print("  exit - 退出程序")
        print("\n示例:")
        print('  call get_weather_warning {"location": "101010100"}')
        print("  call get_daily_forecast 116.41,39.92")
        print("  call get_daily_forecast 101010100 7")
        print()

    elif user_input.lower() == "list":
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:50]}...")
            print()

    elif user_input.lower().startswith("call "):
        # 解析命令
        parts = user_input[5:].strip().split(" ", 1)
        iflen(parts) < 1:
        print("错误: 需要指定工具名称")
        continue

tool_name = parts[0]

# 查找工具
tool = next((t for t in tools if t.name == tool_name), None)
ifnot tool:
print(f"错误: 找不到工具 '{tool_name}'")
continue

# 解析参数
args = {}
iflen(parts) > 1:
arg_text = parts[1].strip()

# 简单参数处理
ifnot arg_text.startswith("{"):
# 简单模式: call get_daily_forecast 101010100 7
simple_args = arg_text.split(" ")

# 检查是否为天气预报工具
                        if tool_name == "get_daily_forecast":
                            iflen(simple_args) >= 1:
                                args["location"] = simple_args[0]
                            iflen(simple_args) >= 2:
                                try:
                                    args["days"] = int(simple_args[1])
                                except ValueError:
                                    print("错误: days 参数必须是整数")
                                    continue
                        elif tool_name == "get_weather_warning":
                            iflen(simple_args) >= 1:
                                args["location"] = simple_args[0]
                        else:
                            print("错误: 简单参数模式仅支持预定义工具")
                            continue
                    else:
                        # JSON模式: call get_weather_warning {"location": "101010100"}
                        try:
                            args = json.loads(arg_text)
                        except json.JSONDecodeError:
                            print("错误: 无效的JSON参数")
                            continue
                
                print("正在调用工具...\n")
                try:
                    # 调用工具
                    result = await client.call_tool(tool_name, args)
                    print("结果:")
                    print(result)
                    print()
                except Exception as e:
                    print(f"错误: {str(e)}")
                    print()
            
            else:
                print("未知命令，使用 'help' 查看帮助")
                print()
    
    finally:
        # 关闭连接和进程
        await client.close()
        if server_process.returncode isNone:
            server_process.terminate()
            try:
                await asyncio.wait_for(server_process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                server_process.kill()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n已退出")
```

:::color5
**<font style="color:#601BDE;">3.第三步：使用MCP Inspector调试</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(63, 63, 63);background-color:rgb(247, 247, 247);">首先在</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">.env</font>`<font style="color:rgb(63, 63, 63);background-color:rgb(247, 247, 247);">文件配置</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">QWEATHER_API_KEY</font>`<font style="color:rgb(63, 63, 63);background-color:rgb(247, 247, 247);">和 </font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">QWEATHER_API_KEY</font>`

<font style="color:rgb(63, 63, 63);">MCP Inspector是调试MCP服务器的利器，提供可视化界面：</font>

1. <font style="color:rgb(63, 63, 63);">安装Inspector：</font>

```bash
npm install -g @modelcontextprotocol/inspector
```

2. <font style="color:rgb(63, 63, 63);">启动Inspector：</font>

```bash
mcp dev server/weather_server.py
```

3. <font style="color:rgb(63, 63, 63);">在浏览器访问 </font>[http://localhost:6274](http://localhost:6274)

<font style="color:rgb(63, 63, 63);">Inspector界面可以让您直观地查看工具定义、测试调用并查看结果。</font>

+ **<font style="color:rgb(0, 152, 116);">查看可用工具及其描述</font>**<font style="color:rgb(63, 63, 63);"></font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749784444704-974a29b8-9dc2-4a37-83d4-ff3a68ec25bd.png)

<font style="color:rgb(136, 136, 136);">查看可用工具及其描述</font>

+ **<font style="color:rgb(0, 152, 116);">查询北京未来3天天气</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749784462605-4e4a139c-a660-418e-9e2f-a8a9a1d24257.png)

<font style="color:rgb(136, 136, 136);">查询北京未来3天天气</font>

+ **<font style="color:rgb(0, 152, 116);">查询北京灾害预警</font>**<font style="color:rgb(63, 63, 63);"></font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749784479742-40ba8f9a-aa0e-42f1-8f6d-0d74826bca14.png)

<font style="color:rgb(136, 136, 136);">查询北京灾害预警</font>

**<font style="color:rgb(0, 152, 116);background-color:rgb(247, 247, 247);">提示</font>**<font style="color:rgb(63, 63, 63);background-color:rgb(247, 247, 247);">：MCP Inspector 提供了更直观的界面来测试和调试 MCP 服务器，特别适合开发和调试复杂工具。</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">5.实际效果展示</font>
:::color3
<font style="color:rgb(63, 63, 63);">首先在</font>`<font style="color:rgb(221, 17, 68);">.env</font>`<font style="color:rgb(63, 63, 63);">文件配置</font>`<font style="color:rgb(221, 17, 68);">QWEATHER_API_KEY</font>`<font style="color:rgb(63, 63, 63);">和 </font>`<font style="color:rgb(221, 17, 68);">QWEATHER_API_KEY</font>`

<font style="color:rgb(63, 63, 63);">启动程序</font>`<font style="color:rgb(221, 17, 68);">python client/mcp_client.py</font>`

:::

:::color5
**<font style="color:#601BDE;">1.天气预警查询</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

```python
> call get_weather_warning {"location": "101010100"}
正在调用工具...

结果:
预警ID: 10123020120230713145500551323468
标题: 杭州市气象台发布高温黄色预警[III级/较重]
发布时间: 2023-07-13T14:55+08:00
开始时间: 2023-07-13T14:55+08:00
结束时间: 2023-07-14T14:55+08:00
预警类型: 高温
预警等级: Moderate (Yellow)
发布单位: 杭州市气象台
状态: active
详细信息: 杭州市气象台2023年07月13日14时55分发布高温黄色预警信号：预计未来24小时内最高气温将达到37℃以上，请注意防暑降温。
```

:::color5
**<font style="color:#601BDE;">2.天气预报查询</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

```python
> call get_daily_forecast 101010100 3
正在调用工具...

结果:
日期: 2023-07-13
日出: 04:54  日落: 19:44
最高温度: 32°C  最低温度: 22°C
白天天气: 多云  夜间天气: 阴
白天风向: 东南风 3级 (19km/h)
夜间风向: 东南风 3级 (16km/h)
相对湿度: 75%
降水量: 0mm
紫外线指数: 7
能见度: 25km

---

日期: 2023-07-14
日出: 04:55  日落: 19:43
最高温度: 33°C  最低温度: 23°C
白天天气: 多云  夜间天气: 阴
白天风向: 东南风 3级 (21km/h)
夜间风向: 东风 3级 (15km/h)
相对湿度: 72%
降水量: 0mm
紫外线指数: 8
能见度: 25km

---

日期: 2023-07-15
日出: 04:56  日落: 19:43
最高温度: 34°C  最低温度: 23°C
白天天气: 多云  夜间天气: 多云
白天风向: 东南风 3级 (18km/h)
夜间风向: 东风 3级 (14km/h)
相对湿度: 70%
降水量: 0mm
紫外线指数: 9
能见度: 25km
```

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">MCP的进阶应用</font>
<font style="color:rgb(63, 63, 63);">MCP不仅限于天气查询，还可以实现：</font>

1. <font style="color:rgb(63, 63, 63);">1. </font>**<font style="color:rgb(0, 152, 116);">文件操作</font>**<font style="color:rgb(63, 63, 63);">：读写文件、处理上传文件</font>
2. <font style="color:rgb(63, 63, 63);">2. </font>**<font style="color:rgb(0, 152, 116);">数据库交互</font>**<font style="color:rgb(63, 63, 63);">：查询和修改数据库</font>
3. <font style="color:rgb(63, 63, 63);">3. </font>**<font style="color:rgb(0, 152, 116);">多媒体处理</font>**<font style="color:rgb(63, 63, 63);">：处理图像、音频、视频</font>
4. <font style="color:rgb(63, 63, 63);">4. </font>**<font style="color:rgb(0, 152, 116);">复杂工作流</font>**<font style="color:rgb(63, 63, 63);">：多工具链式调用</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">MCP开发最佳实践</font>
1. <font style="color:rgb(63, 63, 63);">1. </font>**<font style="color:rgb(0, 152, 116);">工具设计</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 单一职责：每个工具只做一件事</font>
    - <font style="color:rgb(63, 63, 63);">• 明确参数：详细描述每个参数的用途</font>
    - <font style="color:rgb(63, 63, 63);">• 健壮错误处理：优雅处理各类异常情况</font>
2. <font style="color:rgb(63, 63, 63);">2. </font>**<font style="color:rgb(0, 152, 116);">安全考虑</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 输入验证：使用JSON Schema验证输入</font>
    - <font style="color:rgb(63, 63, 63);">• 权限控制：限制工具访问范围</font>
    - <font style="color:rgb(63, 63, 63);">• 资源限制：防止资源滥用</font>
3. <font style="color:rgb(63, 63, 63);">3. </font>**<font style="color:rgb(0, 152, 116);">调试技巧</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 使用MCP Inspector可视化调试</font>
    - <font style="color:rgb(63, 63, 63);">• 日志记录：添加详细日志</font>
    - <font style="color:rgb(63, 63, 63);">• 参数测试：测试边界条件和异常输入</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">结语</font>
<font style="color:rgb(63, 63, 63);">MCP为AI模型与外部系统的交互提供了标准化、安全、高效的解决方案。通过本文的天气工具实战项目，您已经掌握了MCP的基本应用。随着大模型应用的普及，MCP将在AI工具链开发中扮演越来越重要的角色。</font>

<font style="color:rgb(63, 63, 63);">希望这篇入门指南能帮助您开始MCP之旅，构建更强大、更安全的AI应用。欢迎在评论区分享您的想法和实践经验！</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">6.附录</font>
### <font style="color:rgb(63, 63, 63);">和风天气 API 注册与使用</font>
<font style="color:rgb(63, 63, 63);">要使用本项目，需要先注册和风天气开发者账号并获取 API Key：</font>

1. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">注册和风天气开发者账号</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 访问 </font><font style="color:rgb(87, 107, 149);">和风天气开发服务</font><sup><font style="color:rgb(87, 107, 149);">[2]</font></sup>
    - <font style="color:rgb(63, 63, 63);">• 点击"注册"，按照提示完成账号注册</font>
2. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">创建项目并获取 API Key</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 登录开发者控制台</font>
    - <font style="color:rgb(63, 63, 63);">• 点击"项目管理" -> "创建项目"</font>
    - <font style="color:rgb(63, 63, 63);">• 填写项目名称、创建凭据</font>
    - <font style="color:rgb(63, 63, 63);">• 创建成功后，在项目详情页可以获取 API Key</font><font style="color:rgb(63, 63, 63);">  
</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749783251286-ddb430b6-32b4-40a9-b010-33ac19bf9ac1.png)

<font style="color:rgb(136, 136, 136);">和风天气API Key</font>

3. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">开发者的API Host</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 登录开发者控制台</font>
    - <font style="color:rgb(63, 63, 63);">• 点击"头像" -> "设置"，或直接访问https://console.qweather.com/setting?lang=zh</font>
    - <font style="color:rgb(63, 63, 63);">• 查看API Host</font><font style="color:rgb(63, 63, 63);">  
</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749783264382-84b1e840-4bbf-4ce1-87e3-bdf7c7d50d39.png)

<font style="color:rgb(136, 136, 136);">和风天气API Host</font>

4. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(0, 152, 116);">API 使用说明</font>**<font style="color:rgb(63, 63, 63);">：</font>
    - <font style="color:rgb(63, 63, 63);">• 免费版API有调用次数限制，详情请参考</font><font style="color:rgb(87, 107, 149);">和风天气定价页面</font><sup><font style="color:rgb(87, 107, 149);">[3]</font></sup>
    - <font style="color:rgb(63, 63, 63);">• 支持通过城市ID或经纬度坐标查询天气信息</font>
    - <font style="color:rgb(63, 63, 63);">• 城市ID可通过</font><font style="color:rgb(87, 107, 149);">和风天气城市查询API</font><sup><font style="color:rgb(87, 107, 149);">[4]</font></sup><font style="color:rgb(63, 63, 63);">获取</font>

## <font style="color:rgb(255, 255, 255);background-color:rgb(0, 152, 116);">参考资源</font>
+ <font style="color:rgb(63, 63, 63);">• MCP官方文档：https://modelcontextprotocol.io/</font>
+ <font style="color:rgb(63, 63, 63);">• MCP快速入门：https://modelcontextprotocol.io/quickstart/server</font>
+ <font style="color:rgb(63, 63, 63);">• 项目源码：https://github.com/FlyAIBox/mcp-in-action/tree/qweather_0.1/mcp_demo</font>
+ <font style="color:rgb(63, 63, 63);">• 和风天气API：https://dev.qweather.com/</font>

#### <font style="color:rgb(0, 152, 116);">引用链接</font>
`<font style="color:rgb(63, 63, 63);">[1]</font>`<font style="color:rgb(63, 63, 63);"> 注册地址: </font>_<font style="color:rgb(63, 63, 63);">https://dev.qweather.com/</font>_<font style="color:rgb(63, 63, 63);">  
</font>`<font style="color:rgb(63, 63, 63);">[2]</font>`<font style="color:rgb(63, 63, 63);"> 和风天气开发服务: </font>_<font style="color:rgb(63, 63, 63);">https://dev.qweather.com/</font>_<font style="color:rgb(63, 63, 63);">  
</font>`<font style="color:rgb(63, 63, 63);">[3]</font>`<font style="color:rgb(63, 63, 63);"> 和风天气定价页面: </font>_<font style="color:rgb(63, 63, 63);">https://dev.qweather.com/docs/pricing/</font>_<font style="color:rgb(63, 63, 63);">  
</font>`<font style="color:rgb(63, 63, 63);">[4]</font>`<font style="color:rgb(63, 63, 63);"> 和风天气城市查询API: </font>_<font style="color:rgb(63, 63, 63);">https://dev.qweather.com/docs/api/geoapi/</font>_<font style="color:rgb(63, 63, 63);">  
</font>

<font style="color:rgb(10, 10, 10);"></font>

