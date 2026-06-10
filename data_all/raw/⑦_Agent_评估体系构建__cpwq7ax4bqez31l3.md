# ⑦ Agent 评估体系构建

<!-- source: yuque://zhongxian-iiot9/hlyypb/cpwq7ax4bqez31l3 -->

:::color3
**简介：**本文深入探讨特定类型 Agent 的具体评估策略。涵盖**<font style="color:#ED740C;">编码 Agent、研究搜索 Agent、对话聊天 Agent 及计算机操作 Agent 等四类典型应用场景</font>**，并结合实际案例与权威基准（如 SWE-bench、BrowseComp 等），详细解析各类型 Agent 的**<font style="color:#ED740C;">评估维度、指标体系及构建方法</font>**。

**项目代码：**[https://github.com/WakeUp-Jin/Practical-Guide-to-Context-Engineering](https://github.com/WakeUp-Jin/Practical-Guide-to-Context-Engineering)

:::

:::color5
**<font style="color:#601bde;">1. 分析参考来源 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

本文的分析基于以下核心文献与基准测试资源：

+ 文章链接：[https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
+ 𝜏-Bench：[https://arxiv.org/abs/2406.12045](https://arxiv.org/abs/2406.12045)
+ τ2-Bench：[https://arxiv.org/abs/2506.07982](https://arxiv.org/abs/2506.07982)
+ BrowseComp：[https://arxiv.org/abs/2504.12516](https://arxiv.org/abs/2504.12516)
+ 《Agent评估指南》：[https://mp.weixin.qq.com/s/k_G0ppEzdFDHP9k56lSw0g](https://mp.weixin.qq.com/s/k_G0ppEzdFDHP9k56lSw0g)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772266318777-4a1eefa9-d487-4cc9-aa96-96efcb0920c9.png)



## 一、评估编码 Agent 的方法
:::color3
**简介：**编码 Agent 的核心职能包括**<font style="color:#ED740C;">编写、测试及调试代码</font>**，其工作模式类似于人类开发者在代码库中的检索与操作。鉴于其任务通常具有明确的规格要求，确定性评分器（Deterministic Graders） 是评估此类 Agent 的理想选择。

:::

:::color5
**<font style="color:#601bde;">1. 评估维度一：代码功能性与测试通过率</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

首要评估标准在于**<font style="color:#74B602;">代码是否能够成功运行以及是否通过既定测试</font>**。以下介绍两种主流的编程评估基准：

1. SWE-bench Verified
2. Terminal-Bench  
基准详解：
+ Terminal-Bench：侧重于端到端的全流程测试。它不仅关注单一编译错误的修复，更涵盖从开始到结束的完整编译与部署过程。
    - 典型案例：部署 Web 应用程序、从零搭建 MySQL 数据库。
+ SWE-bench Verified：侧重于“单元测试”层面的验证。
    - 常规流程：
        * 向 Agent 提供一个真实的编程问题。
        * Agent 编写相应的修复代码。
        * 运行测试套件，验证 Agent 编写的代码能否通过测试。

:::color5
**<font style="color:#601bde;">2. 评估维度二：工作过程的合理性与效率</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

在拥有测试案例集或测试函数来验证结果的基础上，评估编码 Agent 的工作过程同样至关重要。**<font style="color:#74B602;">除了关注最终测试结果的通过与否，还需考察任务执行过程的合理性与优雅程度</font>**。  
对此，可引入以下两种补充评估方法：

1. 基于启发式规则的代码质量评估：利用静态代码规则检查代码质量，而非仅依赖测试结果。评估指标包括：
    - 代码复杂度
    - 代码重复率
    - 命名规范性
    - 安全漏洞检测
    - 性能问题分析
    - 代码可读性
2. 基于模型的行为评估：利用大模型（LLM）对 Agent 执行任务的**<font style="color:#74B602;">中间过程（即行为轨迹）进行评估</font>**。  
行为评估案例说明：
    - 任务目标：查询数据库中的用户信息。
    - Agent A 方案：直接查询所有用户信息，随后在内存中进行过滤。
    - Agent B 方案：使用 `where` 语句进行条件查询，直接返回所需数据。  
分析：虽然 A 与 B 均完成了任务，但 Agent B 的做法更符合规范，性能更优。  
结论：编码 Agent 的评估应包含两个主要方向：执行结果（Result）与执行过程（Process）。

:::color5
**<font style="color:#601bde;">3. 编码 Agent 评估配置案例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

以下是一个完整的评估配置示例，实际应用中可根据需求动态调整配置项：

```yaml
task:
  id: "fix-auth-bypass_1" # 任务ID：修复认证绕过漏洞_1

  desc: "修复当密码字段为空时的认证绕过漏洞..."

  graders:  # 评分器
    - type: deterministic_tests  # 确定性测试
      required:
        - test_empty_pw_rejected.js    # 拒绝空密码的测试
        - test_null_pw_rejected.js     # 拒绝null密码的测试

    - type: llm_rubric  # LLM评分标准
      rubric: prompts/code_quality.md  # 代码质量评分提示词文件

    - type: static_analysis  # 静态代码分析
      commands:
        - eslint      # 代码风格检查
        - tsc         # TypeScript类型检查

    - type: state_check  # 状态检查
      expect:
        security_logs:
          event_type: "auth_blocked"  # 期望安全日志中有认证阻止事件

    - type: tool_calls  # 工具调用检查
      required:
        - tool: read_file
          params:
            path: "src/auth/*"  # 读取认证代码
        - tool: edit_file       # 编辑文件
        - tool: run_tests       # 运行测试

  tracked_metrics:  # 追踪指标
    - type: transcript  # 对话记录指标
      metrics:
        - n_turns          # 对话轮数
        - n_toolcalls      # 工具调用次数
        - n_total_tokens   # 总token消耗

    - type: latency  # 延迟指标
      metrics:
        - time_to_first_token     # 首token时间
        - output_tokens_per_sec   # 输出速度（tokens/秒）
        - time_to_last_token      # 总完成时间


```

## 二、评估对话 Agent 的方法
:::color3
**简介：**对话代理（Conversational Agent）广泛应用于客户支持、销售或辅导等领域。与传统聊天机器人不同，它们具备状态保持、工具调用及在对话中采取行动的能力。此类 Agent 的评估不仅关注任务完成度，更面临独特的挑战：**<font style="color:#ED740C;">互动本身的质量必须纳入评估范畴</font>**。

:::

:::color5
**<font style="color:#601bde;">1. 评估的核心挑战与策略</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

虽然编程和研究代理也涉及多轮交互，但对话代理的特殊性在于**<font style="color:#117CEE;">互动体验直接影响评估结果</font>**。有效的评估通常依赖于可验证的最终状态结果以及能够捕捉任务完成度与互动质量的综合评分标准。  
	与其他评估不同，对话代理通常需要引入第二个 LLM 来模拟用户（User Simulator）。例如，在对齐审计代理中，通过长时间的对抗性对话来测试模型的表现。

:::color5
**<font style="color:#601bde;">2. 评估维度一：可验证的最终状态</font>**

:::

该维度关注对话 Agent 最终是否完成了既定任务。

+ 典型任务：客服退款、修改收货地址、生成报价单等。

:::color5
**<font style="color:#601bde;">3. 评估维度二：互动质量评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

这是相比其他类型 Agent 的独特挑战：互动过程的质量是评估的重要组成部分。  
场景案例：客服退款

+ Agent A：
    - 用户："我要退款"
    - Agent："订单号？"
    - 用户："12345"
    - Agent："已退款"
    - 评价：任务虽完成，但态度生硬，体验较差。
+ Agent B：
    - 用户："我要退款"
    - Agent："很抱歉给您带来不便。请问是哪个订单呢？"
    - 用户："12345"
    - Agent："我查到了您的订单，符合退款条件。我现在为您处理，预计3-5个工作日到账。还有其他需要帮助的吗？"
    - 评价：任务完成，且交互体验良好。  
结论：对话 Agent 的评估标准应为 “最终状态验证 + 交互质量评估”。

:::color5
**<font style="color:#601bde;">4. 多维度评估标准与基准测试</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

衡量对话 Agent 有效性的标准通常是多维度的：

1. 状态检查：用户的问题和诉求是否得到解决。
2. 文本上下文约束：是否在规定轮次（如 10 轮）内完成任务。
3. LLM 评估：语气是否恰当、态度是否良好。  
推荐基准测试：  
针对零售支持和航空预订等领域的多轮交互场景，推荐使用以下两个基准，它们均利用 LLM 扮演用户角色进行测试：
+ 𝜏-Bench
+ τ2-Bench（𝜏-Bench 的后续版本）  
在开发类似场景的客服对话 Agent 时，可利用这两个基准评估 Agent 的有效性。

:::color5
**<font style="color:#601bde;">5. 对话 Agent 评估配置案例</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```yaml
graders:
  # 1. LLM评分标准
  - type: llm_rubric
    rubric: prompts/support_quality.md  # 客服质量评分提示词文件
    assertions: # 列出来的评分的重点角度
      - "Agent对客户的沮丧表现出同理心"
      - "解决方案被清晰地解释"
      - "Agent的回复基于fetch_policy工具的结果"

  # 2. 状态检查
  - type: state_check
    expect:  # 期望的最终状态
      tickets:
        status: resolved      # 工单状态：已解决
      refunds:
        status: processed     # 退款状态：已处理

  # 3. 工具调用检查
  - type: tool_calls
    required:  # 必须调用的工具
      - tool: verify_identity              # 验证身份

      - tool: process_refund               # 处理退款
        params:
          amount: "<=100"                  # 金额必须 ≤ 100

      - tool: send_confirmation            # 发送确认

  # 4. 对话记录约束
  - type: transcript
    max_turns: 10  # 最大对话轮数：10轮

tracked_metrics:  # 追踪指标
  # 1. 对话记录指标
  - type: transcript
    metrics:
      - n_turns          # 对话轮数
      - n_toolcalls      # 工具调用次数
      - n_total_tokens   # 总token消耗

  # 2. 延迟指标
  - type: latency
    metrics:
      - time_to_first_token     # 首token时间
      - output_tokens_per_sec   # 输出速度（tokens/秒）
      - time_to_last_token      # 总完成时间

```

## 三、评估研究 Agent 的方法
:::color3
**简介：**研究 Agent 的核心任务是**<font style="color:#ED740C;">收集、综合和分析信息，最终产出如答案或报告等成果</font>**。与编码 Agent 的单元测试不同，研究 Agent 的输出质量评估难以做到完全确定性，通常需根据具体任务进行相对判断。

:::

:::color5
**<font style="color:#601bde;">1. 评估的核心原则与挑战</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

主要评估方向：

+ 搜索与研究是否全面。
+ 信息来源是否良好且正确。  
领域差异性：  
不同领域的任务（如市场研究与技术调研）需要设定不同的评估标准。  
独特挑战：  
研究 Agent 的评估面临诸多不确定性：专家可能对综合内容的全面性存在分歧；真实情况会随参考内容的更新而变化；且更长、更开放式的输出容易产生更多错误空间。

:::color5
**<font style="color:#601bde;">2. 评估基准：BrowseComp</font>**

:::

BrowseComp 是 OpenAI 发布的一个针对 AI 代理浏览能力的基准测试，专门评估 AI 能否在开放网络中找到“难以发现”的信息。该基准的设计特点在于：问题难以解决，但答案易于验证（通常是一个词或短语），极大地方便了开发者的评估工作。  
案例说明：

+ 问题："在悉尼歌剧院附近的植物园里有一座铜雕塑，雕塑中的男人手里拿着什么物体？"
+ 任务拆解：
    1. 定位悉尼歌剧院附近的植物园。
    2. 找到该植物园内的铜雕塑信息。
    3. 识别雕塑细节（男人手持的物体）。

:::color5
**<font style="color:#601bde;">3. 评估构建方法：组合评分器</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

构建研究 Agent 评估体系的一般方法是组合多种类型的评分器：

1. 基础性检查：验证每一个声明是否都有对应的来源支持。
2. 覆盖性检查：检查来源中的关键信息是否都已包含并被使用。
3. 来源质量检查：评估引用资料的权威性，避免仅因搜索排名靠前而盲目采用。  
以下示例展示了这三种检查的主要方向：  
![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772265692099-0ad84bc4-e084-4d00-896f-48f8d6f12f79.png)

## 四、评估计算机使用 Agent 的方法
:::color3
**简介：**计算机使用 Agent 通过与人类相同的界面（GUI）与软件进行交互，包括**<font style="color:#ED740C;">屏幕截图、鼠标点击、键盘输入和滚动等操作</font>**，而非依赖 API 或代码执行。这意味着计算机 Agent 理论上可以使用任何带有图形用户界面的程序。

:::

:::color5
**<font style="color:#601bde;">1. 评估逻辑：界面与后端逻辑并重</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

评估此类 Agent 时，不能仅关注界面是否正确显示，更需**<font style="color:#74B602;">验证软件背后的逻辑是否正确执行</font>**。  
典型评估框架：

1. WebArena：专注于基于浏览器的任务测试。它使用 URL 和页面状态检查来验证 Agent 是否正确导航，同时对涉及数据修改的任务进行后端状态验证（例如：确认订单确实已在系统下单，而不仅仅是确认页面显示了“成功”）。
2. OSWorld：将评估范围扩展至完整的操作系统控制。脚本会在任务完成后检查各种产物，包括文件系统状态、应用程序配置、数据库内容以及 UI 元素属性。

:::color5
**<font style="color:#601bde;">2. 关键设计思路：DOM 操作 vs 屏幕截图</font>**

:::

在开发浏览器 Agent 时，需在 Token 效率和延迟之间取得平衡。

+ 基于 DOM 的交互：执行速度快，但消耗大量 Token。
+ 基于屏幕截图的交互：速度较慢，但 Token 效率更高。  
官方原文引用与解读：

> “浏览器使用代理需要在 token 效率和延迟之间取得平衡。基于 DOM 的交互执行速度快但消耗大量 token，而基于屏幕截图的交互速度较慢但 token 效率更高。例如，当要求 Claude 总结维基百科时，从 DOM 中提取文本更高效。当在亚马逊上寻找新笔记本电脑保护套时，截图更高效（因为提取整个 DOM 会消耗大量 token）。在我们的 Claude for Chrome 产品中，我们开发了评估方法来检查代理是否为每个场景选择了正确的工具。这使我们能够更快、更准确地完成基于浏览器的任务。”  
策略建议：
>

1. 文本密集型网页：如果网页文本较多，直接读取 DOM 元素更加高效，且信息密度大，能有效过滤无用的网页标签。
2. 结构复杂/分散型网页：如果网页 DOM 结构庞大且文本信息非常分散（典型如电商网站、商品推荐任务），建议采用截图方式，视觉信息会更高效且清晰。

## 五、总结
:::color3
**简介：**无论智能体类型如何，其行为在每次运行中都可能存在变化，这增加了评估结果解释的难度。为了捕捉这种细微差异，我们需要引入特定的统计指标来衡量 Agent 的潜力与稳定性。

:::

:::color5
**<font style="color:#601bde;">1. 评估的不确定性与挑战</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

每个任务的成功率可能波动较大，例如在某个任务上达到 90%，而在另一个任务上仅有 50%。此外，一个在某次评估中通过的任务，在下一次运行中可能会失败。因此，我们需要测量智能体在某个任务上成功的频率（即试验的比例）。

:::color5
**<font style="color:#601bde;">2. 关键指标一：pass@k（衡量潜力）</font>**

:::

定义：pass@k衡量代理在 k 次尝试中至少获得一个正确解决方案的可能性。  
特性：  
随着 k 的增加，pass@k分数会上升——更多的“射门机会”意味着至少 1 次成功的几率更高。

+ pass@1：表示模型在第一次尝试就成功完成了任务。在编程场景中，我们通常最关心 pass@1。
+ 在其他场景下，只要有一个解决方案有效，尝试多次也是可以接受的。  
案例解释（pass@3）：  
假设总共有 5 个任务。在 3 次机会中，有 3 个任务至少成功了一次，因此 pass@3=60%  
注意：如果在任务三中，Agent 在第 4 次机会才执行成功，则不计入 pass@3 的统计标准，视为无效。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772265722861-0786d2c3-caac-454c-b5ac-d060f4baa2cf.png)

:::color5
**<font style="color:#601bde;">3. 关键指标二：pass^k（衡量稳定性）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

定义：pass^k 衡量所有 k 次试验均成功的概率。  
特性：  
随着 k 的增加，pass^k 会下降，因为要求在更多试验中保持一致性是一个更难达到的标准。

+ 计算示例：如果代理每次试验的成功率为 75%，运行 3 次试验，则全部 3 次试验成功的概率是 ((0.75)^3≈42%。
+ 该指标对于面向用户的代理尤其重要，因为用户期望每次都能获得可靠的行为。

:::color5
**<font style="color:#601bde;">4. 指标对比与选择</font>**

:::

这两个指标分别捕捉了 Agent 的不同特性：

1. pass@k（可用性/潜力）：说明 Agent 的上限在哪里，给予足够机会时它能做到什么程度。
2. pass^k（稳定性/可靠性）：说明 Agent 有多靠谱，衡量其在任务中的一致性。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1772265751773-22a0eefa-5106-4056-9a90-9cef77f4c07f.png)  
趋势分析：  
随着试验次数的增加，pass@k和 pass^k 会出现分化。

+ 在 k=1k=1k=1 时，两者相同（均等于单次试验成功率）。
+ 到 k=10k=10k=10 时，呈现截然相反的趋势：pass@k趋近 100%，而 pass^k 降至 0%。  
结论：  
两种指标均有价值，选择哪种取决于产品需求：
+ 对于工具类应用：只要有一次成功就很重要，应使用 pass@kpass@kpass@k。
+ 对于代理类应用：一致性是关键，应使用 pass^k。

