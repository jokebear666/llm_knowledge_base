# ⓺ Dify实战项目：基于deepseek的每日新闻咨询+语音播报工作流

<!-- source: yuque://zhongxian-iiot9/hlyypb/tv3hdp68iwuhyxuz -->

# <font style="color:rgb(51, 51, 51);">前言</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>****<font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(51, 51, 51);">Dify 是一款开源的 LLM 应用开发平台，旨在帮助开发者快速构建和部署基于大语言模型的应用程序。其核心能力包括</font>**<font style="color:#ED740C;">可视化编排工作流</font>**<font style="color:#ED740C;">、</font>**<font style="color:#ED740C;">Agent 框架</font>**<font style="color:#ED740C;">、</font>**<font style="color:#ED740C;">RAG（检索增强生成）集成</font>**<font style="color:#ED740C;">、</font>**<font style="color:#ED740C;">多模型支持</font>**<font style="color:#ED740C;">和</font>**<font style="color:#ED740C;">生产级监控</font>**<font style="color:rgb(51, 51, 51);">。今天就带大家体验一下</font>**<font style="color:#ED740C;">基于 DeepSeek R1 & V3 模型的AI资讯每日新闻+语音播报工作流的工作流</font>**<font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">项目地址：</font>**[https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow](https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650879313-32ee9ada-18af-4f98-9db2-6097079df159.png)

:::color5
**<font style="color:#601BDE;">2.整体功能介绍</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">上面的工作流主要由几块组成</font>

1. **<font style="color:rgb(51, 51, 51);">新闻内容爬取：</font>**<font style="color:rgb(51, 51, 51);">使用</font>**<font style="color:#74B602;">crawl4ai</font>**<font style="color:rgb(51, 51, 51);"> 爬取AI新闻资讯网站获取每日最新的新闻资讯，这块内容我们通过python代码编写来实现的</font>
2. **<font style="color:rgb(51, 51, 51);">大模型调用：</font>**<font style="color:rgb(51, 51, 51);">对dify提供http请求接口，通过大语言模型DeepSeek R1 & V3 模型对其获取的新闻内容进行总结，</font>
3. **<font style="color:rgb(51, 51, 51);">TTS语音模型：</font>**<font style="color:rgb(51, 51, 51);">然后在调用我们之前讲过的自定义第三方语音TTS来实现的。其中TTS语音的模型也是硅基流动提供的FunAudioLLM/CosyVoice2-0.5B模型来实现。</font>

<font style="color:rgb(51, 51, 51);">总体的流程大致就上面所述，下面介绍一下这个工作流节点详细内容。</font>

:::color5
**<font style="color:#601BDE;">1.实现的效果预览</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::info
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650251250-fe81c10c-87ff-4ded-a0df-ca0a62fedb2e.png)

:::

:::info
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650277253-608e4cc5-9f34-4f12-90b7-dbb075e19557.png)

:::

# <font style="color:rgb(51, 51, 51);">工作流实现</font>
:::color5
**<font style="color:#601BDE;">1.开始节点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">这个开始节点我们这里设置了一个新闻获取条数，主要通过下拉选项来实现的。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749651399659-a6671c28-e763-43e9-a1b4-408fb8454732.png)

:::color5
**<font style="color:#601BDE;">2.新闻条数设置</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">这里考虑模型对文本总结的时间以及生成语音TTS时间我们设置2条新闻。（设置的新闻条目越多，工作处理的时间也会越长）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650300964-fb9468c9-0c95-4a83-9587-6f77bd0c8909.png)

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">代码处理</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(51, 51, 51);">这个地方主要是我们用到了</font>**<font style="color:#ED740C;">crawl4ai</font>**<font style="color:rgb(51, 51, 51);"> 这个爬虫框架，通过这个爬虫程序来实现AI新闻的获取。我们这里使用</font>**<font style="color:#ED740C;">fastapi做成一个http请求接口提供dify调用。</font>**

:::

:::color5
**<font style="color:#601BDE;">1.服务端代码</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">这服务端代码主要的目的就是爬取</font>[https://www.aibase.com ](https://www.aibase.com )<font style="color:rgb(51, 51, 51);">最新的新闻资讯。将以上代码部署到服务器中，如果没有服务器可以在本地电脑上部署一个python服务。</font>

```python
import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

app = FastAPI()

# 获取新闻列表页面的所有新闻URL
def get_news_urls():
    url = "https://www.aibase.com/zh/news"
    response = requests.get(url)
    news_urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找所有新闻链接
        news_items = soup.find_all('a', href=True)
        for item in news_items:
            link = item['href']
            # 过滤出符合新闻详情页的链接
            if '/zh/news/' in link and len(link.split('/')) > 3:
                full_url = f"https://www.aibase.com{link}"
                news_urls.append(full_url)
    else:
        print(f"请求失败，状态码: {response.status_code}")
    return news_urls

# 提取单个新闻文章的数据
async def extract_ai_news_article(url):
    print(f"\n--- 提取新闻文章数据: {url} ---")
    # 定义提取 schema
    schema = {
        "name": "AIbase News Article",
        "baseSelector": "div.pb-32",  # 主容器的 CSS 选择器
        "fields": [
            {
                "name": "title",
                "selector": "h1",
                "type": "text",
            },
            {
                "name": "publication_date",
                "selector": "div.flex.flex-col > div.flex.flex-wrap > span:nth-child(6)",
                "type": "text",
            },
            {
                "name": "content",
                "selector": "div.post-content",
                "type": "text",
            },
        ],
    }
    # 创建提取策略
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    # 使用 AsyncWebCrawler 进行爬取
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            extraction_strategy=extraction_strategy,
            bypass_cache=True,  # 忽略缓存，确保获取最新内容
        )
        if not result.success:
            print(f"页面爬取失败: {url}")
            return None
        # 解析提取的内容
        extracted_data = json.loads(result.extracted_content)
        print(f"成功提取新闻: {extracted_data[0]['title']}")
        return extracted_data[0]

# 主函数：获取所有新闻URL并逐一提取详细数据
async def fetch_news(limit: int = 5):
    # 获取所有新闻URL
    news_urls = get_news_urls()
    print(f"共找到 {len(news_urls)} 条新闻链接")
    # 限制新闻数量
    news_urls = news_urls[:limit]
    news_data_list = []
    newsdetail = ""
    # 循环处理每个新闻URL
    for index, url in enumerate(news_urls, start=1):
        news_data = await extract_ai_news_article(url)
        if news_data:
            # 添加到新闻数据列表
            news_data_list.append(news_data)
            # 拼接新闻详情字符串
            content = news_data.get("content", "无法提取内容")
            newsdetail += f"今天新闻第{index}条内容：{content}；\n"
    return news_data_list, newsdetail

# FastAPI 接口
@app.get("/news/")
async def get_news(limit: int = Query(5, description="返回的新闻数量")):
    news_data, newsdetail = await fetch_news(limit)
    return {"news": news_data, "newsdetail": newsdetail}

# 运行 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)
```

:::color5
**<font style="color:#601BDE;">2.客户端调用代码</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">接下来我们需要dify工作流中使用代码执行来调用这个服务端代码。</font>

```python
import requests
import json
def main(arg1: str) -> dict:
    try:
        # 构造请求URL和参数
        url = 'http://127.0.0.1:8086/news/'
        limit = arg1

        # 发送GET请求
        response = requests.get(url, params={'limit': limit})

        # 检查响应状态码
        if response.status_code == 200:
            # 请求成功，处理结果
            result = response.json()

            # 提取新闻数据和新闻详情字符串
            news_list = result.get('news', [])
            newsdetail = result.get('newsdetail', "")

            # 确保 news_list 是一个列表
            if not isinstance(news_list, list):
                return {"error": "服务端返回的新闻数据格式不正确，'news' 字段应为列表。"}

            # 格式化新闻数据（如果需要）
            formatted_news = []
            for news_item in news_list:
                if isinstance(news_item, dict):  # 如果是字典，直接添加
                    formatted_news.append(news_item)
                elif isinstance(news_item, str):  # 如果是字符串，尝试解析为字典
                    try:
                        news_dict = json.loads(news_item)  # 使用 json.loads 解析字符串
                        formatted_news.append(news_dict)
                    except Exception as e:
                        print(f"解析新闻数据时出错: {e}")
                else:
                    print("无效的新闻数据格式")

            # 返回格式化的新闻数据和新闻详情字符串
            return {"news": formatted_news, "newsdetail": newsdetail}
        else:
            # 请求失败，返回错误信息
            return {"error": f"请求失败，状态码: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # 捕获请求异常
        return {"error": f"请求出错: {str(e)}"}
```

<font style="color:rgb(51, 51, 51);">这个我们简单解释一下，输入参数就是开始节点中item值；输出变量有2个 一个是news 数据类型是个数组，第二个参数是newsdetail 是新闻详细内容。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650376544-75f00d92-63ed-4f20-8d0d-17531d98f0bc.png)

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">LLM大语言模型</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(51, 51, 51);">接下来这块就是我们非常熟悉的llm大语言模型的部分了，我们这里用到了硅基流动提供的 </font>**<font style="color:#ED740C;">DeepSeek V3 </font>**<font style="color:rgb(51, 51, 51);">模型。</font>

:::

:::color5
**<font style="color:#601BDE;">1.硅基流动提供的 DeepSeek V3 模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">关于硅基的模型可以在官方网站获取详细信息。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650385226-213df315-d759-4854-9781-8a534cd816f8.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650396499-9ca1ed63-ad67-49e3-9706-5b811764ab94.png)

:::color5
**<font style="color:#601BDE;">2.系统提示词</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
请帮我对以下文章内容进行总结，包括用三个部分，摘要，文章要点
🏷文章要点用数字序号列出。
不要使用'**'加粗标题优化输出格式。
```

<font style="color:rgb(51, 51, 51);">系统提示词比较简单，主要就是让模型给我把详细AI新闻总结 摘要，文章要点等信息。</font>

:::color5
**<font style="color:#601BDE;">3.用户提示词</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">这个用户提示词就是上个节点中出来的news信息</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650407807-be2d2a9b-b7a2-4e3d-adb4-0def6dd7d349.png)

# <font style="color:rgb(51, 51, 51);">模版转换</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(51, 51, 51);">这个工作流节点主要用到了模版转换功能，主要目的是</font>**<font style="color:#ED740C;">将LLM大语言模型总结的信息和新闻详细信息通过字符串拼接起来</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.字符串拼接</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">输入变量有2个，1个是llmtext ,1个是newsdetail。主要的功能就是字符串的拼接。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650418940-f20fa65a-0f27-4235-a4c5-7bcd853515aa.png)

# <font style="color:rgb(51, 51, 51);">语音播报</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(51, 51, 51);">调用了第三方自定义的语音播报插件功能。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">自定义工具实现文本转语音</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">这里我们拖拽一个自定义工具实现文本转语音，关于这块可以参考我之前文章</font>

[<font style="color:rgb(125, 144, 169);">dify案例分享-文生图片OCR识别加语音播报，AI工作流一键搞定</font>](https://mp.weixin.qq.com/s?__biz=Mzg3OTYzMjc1NQ==&mid=2247485287&idx=1&sn=e5727bfbf82c74abaac0ffa660694beb&scene=21#wechat_redirect)

<font style="color:rgb(51, 51, 51);">在工作流 画布中 点击“添加节点”- 选择工具- 自定义工具-选择自定义工具</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650437393-87ec9a0d-e09c-4824-80a5-ab4b96fda4de.png)

<font style="color:rgb(51, 51, 51);">关于自定义工具，这里有3个参数。</font>

1. <font style="color:rgb(51, 51, 51);">input  用户输入的提示词。这里我们直接接入上面流程中文本翻译的结果即可。</font>
2. <font style="color:rgb(51, 51, 51);">model 这个主要是填写语音翻译的模型，我这里填写的是FunAudioLLM/CosyVoice2-0.5B</font>
3. <font style="color:rgb(51, 51, 51);">voice   这里主要是填写模型对应的音色， 我这里填写的是FunAudioLLM/CosyVoice2-0.5B:david</font>

<font style="color:rgb(51, 51, 51);">我这里用到了硅基的模型，这里是需要根据他们的API 来填写。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650452564-a7bbc70d-30bf-4552-8b4b-b7d48848ae23.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650464591-3edf5eb1-fa73-4ac4-965e-57d5526f33c7.png)

<font style="color:rgb(51, 51, 51);">关于这块代码，我已经上传github，大家自行获取。地址（</font><font style="color:rgb(51, 51, 51);">https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow</font><font style="color:rgb(51, 51, 51);">）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650479914-f190d0fc-4535-4381-81b0-47ab290a9b86.png)

<font style="color:rgb(51, 51, 51);">流程节点截图如下</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650487649-c4668a10-6512-4755-8c91-e967ebdeaae6.png)

# <font style="color:rgb(51, 51, 51);">文字转音频TTS</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(51, 51, 51);">接下来我们需要有个代码转换对上个节点中</font>**<font style="color:#ED740C;">自定义工具返回数据进行处理</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.数据处理代码</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">输入的参数就是arg1  它的值就是自定义工具返回数据字符串</font>

```python
def main(arg1: str) -> str:
    # 首先解析外层的 JSON 字符串
    data = json.loads(arg1)
    filename=data['filename']
    url=data['etag']
    markdown_result = f"<audio controls><source src='{url}' type='audio/mpeg'>{filename}</audio>"
    return {"result": markdown_result}
```

<font style="color:rgb(51, 51, 51);">这个代码主要目的处理返回结果后生产TTS语言播报markdown_result</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650499873-58680230-1e7d-4b3f-ae5e-d5976d2151d2.png)

# <font style="color:rgb(51, 51, 51);">内容输出</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">这个节点就比较简单的主要是目的是输出LLM大语言模型总结的AI新闻内容,在把语音播报的TTS语音部分输出出来。</font>

:::

:::color5
**<font style="color:#601BDE;">1.内容输出</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(51, 51, 51);">有2个输出参数，一个是模版转换的文本内容，一个是文字转音频文件处理结果</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650506546-d023e2b7-a1ee-4f7b-93ef-9091ab614f84.png)

<font style="color:rgb(51, 51, 51);">以上我们就完成了工作流的配置。</font>

# <font style="color:rgb(51, 51, 51);">工作流体验</font>
<font style="color:rgb(51, 51, 51);">大家可以点击这个</font><font style="color:rgb(51, 51, 51);">体验</font><font style="color:rgb(51, 51, 51);">地址（http://101.126.84.227:88/chat/sGsc8dVLyFHODT0V）来感受一下，效果如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650516808-8a887a2d-d672-47a1-80b5-81933a5e9211.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749650540149-cae193f7-8ae5-41d6-8b32-9e980e9a2be5.png)

<font style="color:rgb(51, 51, 51);">如果大家没有硅基流动的账号，可以点击</font><font style="color:rgb(51, 51, 51);">https://cloud.siliconflow.cn/i/e0f6GCrN</font><font style="color:rgb(51, 51, 51);">地址来注册，目前硅基的政策是新户注册送14块钱，14块钱够玩一阵子了。</font>

# <font style="color:rgb(51, 51, 51);">总结</font>
<font style="color:rgb(51, 51, 51);">今天我们给大家带来使用硅基流动的模型DeepSeek R1 & V3 加语音播报实现一个AI每日新闻资讯的+语音播报的工作流。感兴趣的小伙伴可以参考我上面的文档操作一遍，体验一下DeepSeek R1 & V3 模型的强大，今天的分享就到这里我们下个文章见。</font>

