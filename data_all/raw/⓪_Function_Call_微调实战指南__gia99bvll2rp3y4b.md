# ⓪ Function Call 微调实战指南

<!-- source: yuque://zhongxian-iiot9/hlyypb/gia99bvll2rp3y4b -->

:::success
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">面试中如果问到：</font>**<font style="color:rgb(83, 88, 97);">“你做过 Function Call 微调吗？难点是什么？”</font>**

<font style="color:rgb(25, 27, 31);">很多同学只能回答：“构造对话数据……”，“定义 schema……”，“训练一下就好了……”</font>

<font style="color:rgb(25, 27, 31);">今天这一篇文章，我就带大家把核心逻辑彻底讲清楚，让你在面试中能从容地解释：</font>

**<font style="color:#74B602;">一个工业级 Function Call 微调项目，为什么难？难在哪里？我们是怎么解决这些问题的？</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765265999622-1ce1e7d9-9748-40b0-b91c-54f16e5b3601.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765262647744-95f77bb7-db8c-4a4c-b715-0e05ded32aba.png)

## <font style="color:rgb(25, 27, 31);">一、Function Call 难点是什么</font>
:::color3
**简介：**<font style="color:#000000;">一句话讲本质，难点不在工具本身，而在“决策”，模型到底</font>**<font style="color:#ED740C;">什么时候调用、调用哪个、调用顺序是什么、缺信息时要不要追问、多轮对话怎么推进</font>**<font style="color:#000000;">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
“帮我订一个上海外滩附近 2000 左右的酒店。”（by草莓师姐）
```

:::success
**<font style="color:#5C8D07;">经过训练的模型</font>**

1. **<font style="color:rgb(25, 27, 31);">识别意图</font>**<font style="color:rgb(25, 27, 31);">：这是“酒店查询”</font>
2. **<font style="color:rgb(25, 27, 31);">判断缺信息</font>**<font style="color:rgb(25, 27, 31);">：缺日期 → 必须反问</font>
3. **<font style="color:rgb(25, 27, 31);">追问用户</font>**<font style="color:rgb(25, 27, 31);">：入住/离店时间是多少？</font>
4. <font style="color:rgb(25, 27, 31);">用户回答日期后，开始依次调用。</font>
5. <font style="color:rgb(25, 27, 31);">综合酒店信息 + 评价，输出推荐结果</font>

:::

:::danger
**<font style="color:#E746A4;">未经训练的模型</font>**

+ <font style="color:rgb(25, 27, 31);">不问日期，直接调用工具（导致工具报错）</font>
+ <font style="color:rgb(25, 27, 31);">或者只调用 recommend_hotels 就回复（导致信息残缺）</font>
+ <font style="color:rgb(25, 27, 31);">或者问一堆无关紧要的问题（破坏体验）</font>
+ <font style="color:rgb(25, 27, 31);">或者根本不调用工具，只是生成一大段废话</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765264296119-82ac0650-71ae-4f36-99fb-1717a330bdc8.png)

:::color5
**<font style="color:#601BDE;">1.未经训练的模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">不问日期，直接调用工具（导致工具报错）</font>
+ <font style="color:rgb(25, 27, 31);">或者只调用 recommend_hotels 就回复（导致信息残缺）</font>
+ <font style="color:rgb(25, 27, 31);">或者问一堆无关紧要的问题（破坏体验）</font>
+ <font style="color:rgb(25, 27, 31);">或者根本不调用工具，只是生成一大段废话（AI 常犯的错误）</font>

:::color5
**<font style="color:#601BDE;">2.经过训练的模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">识别意图</font>**<font style="color:rgb(25, 27, 31);">：这是“酒店查询”</font>
2. **<font style="color:rgb(25, 27, 31);">判断缺信息</font>**<font style="color:rgb(25, 27, 31);">：缺日期 → 必须反问</font>
3. **<font style="color:rgb(25, 27, 31);">追问用户</font>**<font style="color:rgb(25, 27, 31);">：入住/离店时间是多少？</font>
4. <font style="color:rgb(25, 27, 31);">用户回答日期后，开始依次调用：</font>
    - <font style="color:rgb(25, 27, 31);">recommend_hotels</font>
    - <font style="color:rgb(25, 27, 31);">get_hotel_reviews（对每家推荐酒店调用）</font>
5. <font style="color:rgb(25, 27, 31);">综合酒店信息 + 评价，输出推荐结果</font>

**<font style="color:rgb(25, 27, 31);">Function Call 训练的目标不是让模型“会调用工具”，而是让它“根据业务逻辑正确调用工具”。</font>**

## <font style="color:rgb(25, 27, 31);">二、为什么要做 Function Call 微调？</font>
:::color3
**简介：**面试官大概率会补充提问：光靠 prompt 不够吗？你可以从三个角度回答：<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765265545819-ec971205-19b4-4c80-a2a1-b81e6461cfc5.png)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">Prompt 本质是“规则”，无法覆盖分支逻辑</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">以「旅行规划」为例：</font>

```python
如果缺目的地 → 必须单独反问
如果缺日期 → 必须反问
如果攻略为空 → 不调用天气工具
如果攻略有结果 → 按顺序调用攻略→天气
```

<font style="color:rgb(25, 27, 31);">这些是</font>**<font style="color:rgb(25, 27, 31);">业务流程</font>**<font style="color:rgb(25, 27, 31);">，不是自然语言能稳定表达的。</font>

<font style="color:rgb(25, 27, 31);">LLM 的大脑并不是一个 if-else 程序，只靠 prompt 无法保证稳定执行分支逻辑。</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">Prompt 不能让模型学习“工具链式调用”</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">比如完整的链式调用：</font>

```python
query → recommend_hotels → get_hotel_reviews → final answer
```

<font style="color:rgb(25, 27, 31);">prompt 只能告诉模型“请调用工具”， 但无法让模型</font>**<font style="color:rgb(25, 27, 31);">真正理解工具之间的依赖关系</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">Prompt 不能让模型学习“追问逻辑”与“信息补全流程”</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">以酒店查询为例：</font>

```plain
“帮我查下希尔顿酒店怎么样？”
```

<font style="color:rgb(25, 27, 31);">模型必须学会：</font>

1. <font style="color:rgb(25, 27, 31);">提取酒店名称</font>
2. <font style="color:rgb(25, 27, 31);">判断信息是否足够</font>
3. <font style="color:rgb(25, 27, 31);">调用 get_hotel_reviews</font>
4. <font style="color:rgb(25, 27, 31);">再整理评价输出</font>

<font style="color:rgb(25, 27, 31);">而 prompt 很难让模型稳定执行这套流程。</font>

<font style="color:rgb(25, 27, 31);">所以必须通过 Function Call 微调，让模型真正学会：</font>

+ <font style="color:rgb(25, 27, 31);">如何判断意图</font>
+ <font style="color:rgb(25, 27, 31);">什么时候反问</font>
+ <font style="color:rgb(25, 27, 31);">什么时候工具调用</font>
+ <font style="color:rgb(25, 27, 31);">工具调用顺序</font>
+ <font style="color:rgb(25, 27, 31);">工具调用依赖关系</font>
+ <font style="color:rgb(25, 27, 31);">工具失败后怎么优雅 fallback</font>
+ <font style="color:rgb(25, 27, 31);">多轮对话如何推进</font>
+ <font style="color:rgb(25, 27, 31);">如何合成最终回复</font>

<font style="color:rgb(25, 27, 31);">这些是意识层面的「技能」，不可能通过 prompt “死报菜名”实现。</font>

## <font style="color:rgb(25, 27, 31);">三、Function Call 微调的项目到底长什么样？</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">这里用</font>**<font style="color:rgb(25, 27, 31);">旅行助手 Agent</font>**<font style="color:rgb(25, 27, 31);">来讲解，支持以下功能：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:#F38F39;background-color:#E8F7CF;">旅行规划(RAG + 天气)</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">问路导航（地图工具）</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">酒店推荐(推荐 + 评价)</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">多轮追问</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">链式调用</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">分支逻辑</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">工具失败 fallback</font>**

**<font style="color:#F38F39;background-color:#E8F7CF;">工具结果生成自然语言</font>**

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">Agent 的整体逻辑图</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765265246239-3d13c439-dae0-4464-99b5-becc0553903f.png)

<font style="color:rgb(25, 27, 31);">这个 Agent 的整体逻辑图是这样的：</font>

```plain
识别意图 → 分发到 4 个工作流 → 多轮对话 → 工具链调用 → 合成智能回复
```

<font style="color:rgb(25, 27, 31);">四个工作流分别是：</font>

1. **<font style="color:rgb(25, 27, 31);">旅行规划、问路导航、酒店查询、闲聊/拒答</font>**

<font style="color:rgb(25, 27, 31);">单看“旅行规划”，你会发现这是一个非常完整的链路：</font>

```plain
用户：你好，国庆我想去西安玩 5 天，能帮我规划吗？
→ 意图识别：旅行规划
→ 信息判断：目的地 + 时间 + 天数齐全
→ 按顺序调用
   search_travel_guide
   get_weather_info
→ 综合工具结果
→ 输出一份完整的旅行计划
```

:::color5
**<font style="color:#601BDE;">2.对话消息结构示例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">下面是其中一个真实工具调用的对话消息结构（简化版）：</font>

```json

{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_xxx",
      "type": "function",
      "function": {
        "name": "search_travel_guide",
        "arguments": "{\"location\": \"西安\"}"
      }
    },
    {
      "id": "call_yyy",
      "type": "function",
      "function": {
        "name": "get_weather_info",
        "arguments": "{\"location\": \"西安\", \"num_days\": 5}"
      }
    }
  ]
}
```

<font style="color:rgb(25, 27, 31);">工具返回后，再格式化成自然语言：</font>

```json
{
  "role": "assistant",
  "content": "根据攻略和天气，为您定制了西安 5 日旅行计划..."
}
```

<font style="color:rgb(25, 27, 31);">SFT 微调的目标，就是让模型自动输出上面这样的消息结构。</font>

## <font style="color:rgb(25, 27, 31);">四、真正的难点：如何构造一套能训练出效果的 SFT 数据？</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">这部分是 Function Call 项目的灵魂。很多人失败就是因为：数据太少、覆盖不全、不会构造多轮对话</font>

<font style="color:rgb(25, 27, 31);">工具调用不标准等原因。我们采用的是</font>**<font style="color:rgb(25, 27, 31);">“</font>**[**<font style="color:rgb(9, 64, 142);">数据沙盒</font>**](https://zhida.zhihu.com/search?content_id=267192874&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E6%B2%99%E7%9B%92&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">”体系</font>**<font style="color:rgb(25, 27, 31);">：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1765266145402-dda1b037-f71e-4226-81cc-b556f087fc95.png)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">定义标签体系（五大工作流 × 分支）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">类型</font>** | **<font style="color:rgb(25, 27, 31);">数量（训练集）</font>** |
| :--- | :--- |
| <font style="color:rgb(25, 27, 31);">旅行规划（不需要反问）</font> | <font style="color:rgb(25, 27, 31);">320</font> |
| <font style="color:rgb(25, 27, 31);">旅行规划（需要反问）</font> | <font style="color:rgb(25, 27, 31);">40</font> |
| <font style="color:rgb(25, 27, 31);">问路（不需要反问）</font> | <font style="color:rgb(25, 27, 31);">80</font> |
| <font style="color:rgb(25, 27, 31);">问路（需要反问）</font> | <font style="color:rgb(25, 27, 31);">16</font> |
| <font style="color:rgb(25, 27, 31);">酒店查询（不需要反问）</font> | <font style="color:rgb(25, 27, 31);">160</font> |
| <font style="color:rgb(25, 27, 31);">酒店查询（需要反问）</font> | <font style="color:rgb(25, 27, 31);">32</font> |
| <font style="color:rgb(25, 27, 31);">旅行闲聊</font> | <font style="color:rgb(25, 27, 31);">80</font> |
| <font style="color:rgb(25, 27, 31);">拒答</font> | <font style="color:rgb(25, 27, 31);">80</font> |


<font style="color:rgb(25, 27, 31);">每一类都覆盖“必须会”的分支逻辑。</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">构造 100+ 城市沙盒</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">城市名称、城市坐标、地标系统、旅行景点库、酒店池、天气模拟……</font>

<font style="color:rgb(25, 27, 31);">目的就是让模型能够：</font>

+ <font style="color:rgb(25, 27, 31);">处理不同城市</font>
+ <font style="color:rgb(25, 27, 31);">不同场景</font>
+ <font style="color:rgb(25, 27, 31);">不同日期</font>
+ <font style="color:rgb(25, 27, 31);">不同的工具结果</font>

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">构造 40 种随机用户画像</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">每条数据都附带：</font>

+ <font style="color:rgb(25, 27, 31);">用户名</font>
+ <font style="color:rgb(25, 27, 31);">城市 ID</font>
+ <font style="color:rgb(25, 27, 31);">起点坐标</font>
+ <font style="color:rgb(25, 27, 31);">出发日期范围</font>

<font style="color:rgb(25, 27, 31);">这些是系统消息必须包含的信息：</font>

```json
{
  "role": "system",
  "content": "## 用户信息\n- 用户名: 草莓师姐\n- 当前城市ID: 101010100\n- 出发日期: 2025-09-18\n- 起点坐标: 116.481028,39.989643"
}
```

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">生成 30+ 种模板、多轮追问模板</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">例如同一个需求：</font>

```plain
我想找个上海外滩附近的酒店
帮我在魔都找住宿
在外滩有什么 2000 左右的酒店
```

<font style="color:rgb(25, 27, 31);">模型必须学会理解各种表达方式。</font>

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">严格模拟工具调用链</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">例如酒店查询：</font>

```plain
用户提问 → 判断是否缺城市 → 判断是否缺日期/预算 → recommend_hotels → get_hotel_reviews → final
```

<font style="color:rgb(25, 27, 31);">必须全部出现。</font>



  


