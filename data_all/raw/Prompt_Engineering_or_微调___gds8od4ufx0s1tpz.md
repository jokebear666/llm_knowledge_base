# Prompt Engineering or 微调？

<!-- source: yuque://zhongxian-iiot9/hlyypb/gds8od4ufx0s1tpz -->

 

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">通常在微调之前会先进行prompt尝试，改几遍prompt会再sft/rl，但是往往忽略了一个问题：</font>**<font style="color:#74B602;">大模型的能力已经非常强了，真的需要sft/rl吗？</font>**<font style="color:rgb(25, 27, 31);">有没有可能是prompt写的不够好或者cot/rag等方法用的不够好所以才需要做sft/rl呢？</font>

:::

:::color3
**简介：**在大模型应用落地的过程中，一个非常现实又关键的问题是：**<font style="color:#ED740C;">到底是我的 prompt 写得不够好，还是模型本身能力不足，才导致效果达不到预期？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

这个问题之所以重要，是因为它直接决定了你后续的技术路径——是继续**<font style="color:#74B602;">优化 prompt、引入 CoT或 RAG，还是投入大量资源去做 SFT甚至 RLHF</font>**。

今天我们就从工程实践和算法原理两个层面，拆解这个问题，给出一套可操作的判断框架。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760958321517-1e0774da-ddea-45c3-9969-74ef0ff36613.png)



  




### 一、先问自己：你的任务真的需要微调吗？
:::color3
**简介：**很多人一上来就想着微调，但其实80% 的场景，通过 prompt 工程 + RAG + CoT 就能解决。微调不是万能药，它有明确的适用边界。**<font style="color:#ED740C;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

根据业界经验，以下几类任务通常**不需要微调**：

+ **通用问答**（如客服 FAQ、知识查询）：用 RAG 拉取最新知识即可。
+ **结构化输出**（如 JSON、表格）：通过清晰的 prompt 模板 + few-shot 示例就能稳定输出。
+ **多步推理**（如数学题、逻辑题）：CoT 或 Self-Consistency 等技巧效果显著。
+ **风格模仿**（如写邮件、写文案）：few-shot + system prompt 足够。

而真正需要微调的场景，往往是：

+ **领域术语密集**（如医疗、法律、金融）：模型对专业词汇理解偏差大。
+ **输出格式高度定制**（如特定协议、内部 DSL）：通用模型无法对齐。
+ **行为模式固化**（如必须拒绝某些请求、必须引用来源）：靠 prompt 容易“翻车”。
+ **低延迟高吞吐要求**：RAG 或长 prompt 会拖慢推理速度。

所以第一步，先判断你的任务是否属于“微调必要区”。

---

### 二、如何系统评估 prompt 是否还有优化空间？
:::color3
**简介**：假设你的任务确实复杂，但还不确定是否该微调。这时候可以做以下几件事

:::

:::color5
**<font style="color:#601BDE;">1.构建“prompt 梯度测试”</font>****<font style="color:#ED740C;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

不要只写一个 prompt 就下结论。你应该设计一个**prompt 演进序列**：

+ Baseline：最简单的指令（如“请回答以下问题”）
+ 加 system prompt（如“你是一个严谨的金融分析师”）
+ 加 few-shot 示例（2~5 个高质量样例）
+ 加 CoT 引导（如“请逐步推理”）
+ 加输出约束（如“请用 JSON 格式，字段包括…”）

然后在同一个测试集上跑这 5 个版本，看准确率/一致性是否显著提升。

举个例子：如果你的任务是“从合同中提取关键条款”，初始 prompt 可能只有 60% 准确率，但加上 3 个 few-shot 示例 + CoT 后，可能直接提升到 85%。这时候微调的边际收益就很低了。

:::color5
**<font style="color:#601BDE;">2.检查模型是否“知道但不说”</font>**

:::

有时候模型其实具备知识，但没被 prompt 激活。你可以用“探测性提问”验证：

+ 先问：“你知道 XX 概念吗？” → 如果回答“知道”，说明知识存在。
+ 再问具体任务 → 如果答错，说明是 prompt 引导问题，不是能力问题。

:::color5
**<font style="color:#601BDE;">3.对比不同基座模型的表现</font>**

:::

用同样的 prompt，在 Qwen、DeepSeek、LongCat-Flash、GPT-4 等模型上跑一遍。

+ 如果**所有模型都表现差**，那很可能是 prompt 设计问题（比如任务描述模糊、缺少约束）。
+ 如果**只有你的目标模型差**，而 GPT-4 能搞定，那说明基座能力确实不足，可能需要微调或换更强的 base。

 	值得一提的是，像 LongCat-Flash 这类 MoE 架构模型（560B 总参数，激活约 27B），在 agentic 任务（如工具调用、多轮交互）上表现突出，IFEval 指令遵循得分高达 89.65%，甚至超过 GPT-4.1。如果你的任务涉及复杂指令执行，不妨先试试这类强基座，而不是急着微调 。

---

### 三、RAG 和 CoT 能替代微调吗？
:::color3
**简介：**很多人忽略了 RAG 和 CoT 的潜力。**<font style="color:#ED740C;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

+ **RAG 适合解决“知识缺失”问题**：比如你的业务数据每天更新，模型不可能 memorize 所有内容。这时候用向量库召回相关片段，再让模型生成，效果远好于微调（微调数据会过时）。
+ **CoT 适合解决“推理链断裂”问题**：对于数学、逻辑、代码类任务，显式要求模型“一步步思考”，能大幅提升准确率。甚至有研究显示，CoT 微调（用带推理链的数据训练）比普通 SFT 更有效 。

 一个经典案例：AIME 数学竞赛题。LongCat-Flash 在 AIME25 上 avg@10 达到 61.25，接近 Qwen3 MoE 的 68.33，远超 GPT-4.1 的 32.00。这背后离不开其多阶段训练中对推理能力的强化，包括 CoT 数据注入 。

所以，在决定微调前，先问：**我的问题是因为缺知识？还是缺推理？还是缺行为约束？**

+ 缺知识 → 用 RAG
+ 缺推理 → 用 CoT / Self-Ask
+ 缺行为约束 → 才考虑微调



### 四、什么时候微调是不可避免的？
:::color3
**简介：**当你满足以下全部条件时，微调才真正值得投入

:::

1. **任务高度专业化**：比如医疗诊断、法律条文解释，通用模型容易“一本正经胡说八道”。
2. **prompt 优化已到瓶颈**：即使加了 10 个 few-shot、CoT、RAG，准确率仍卡在 70% 以下。
3. **有高质量标注数据**：至少几百到几千条 clean 的 input-output 对。
4. **需要低延迟响应**：RAG 的检索+生成 pipeline 太慢，无法满足线上要求。

此时，你可以考虑：

+ **SFT**：快速对齐输出格式和领域知识。
+ **DPO/RLHF**：进一步对齐人类偏好（如安全性、流畅性）。

但注意：微调也有风险。比如过拟合小数据集、灾难性遗忘、推理速度下降等。所以务必做 A/B 测试。

---

### 五、一个实用决策流程图
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1760957977661-3df4cc76-f4dc-42d3-ab8d-a0c7252d4ded.png)



### 五、代码示例：如何自动化评估 prompt 效果
:::color3
**简介：**下面是一个简单的 Python 脚本框架，用于批量测试不同 prompt 的效果**<font style="color:#ED740C;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

通过这个脚本，你可以量化不同 prompt 策略的效果，避免“感觉不好就微调”的误区。

```python
from openai import OpenAI
import json

client = OpenAI(api_key="your-api-key", base_url="https://api.longcat.ai/v1")

test_cases = [
    {"input": "从以下合同中提取甲方名称：...", "expected": "XX公司"},
    # ... 更多样例
]

prompts = {
    "baseline": "请提取甲方名称：{text}",
    "cot": "请逐步分析合同内容，然后提取甲方名称：{text}",
    "few_shot": """示例1：
合同：甲方为ABC科技，乙方为XYZ集团。
输出：ABC科技

示例2：
合同：本协议由甲方（123有限公司）与乙方签署。
输出：123有限公司

请提取甲方名称：{text}"""
}

def evaluate_prompt(prompt_template):
    correct = 0
    for case in test_cases:
        response = client.chat.completions.create(
            model="longcat-flash-chat",
            messages=[{"role": "user", "content": prompt_template.format(text=case["input"])}]
        )
        pred = response.choices[0].message.content.strip()
        if case["expected"] in pred:  # 简单包含判断，实际可用更严谨的匹配
            correct += 1
    return correct / len(test_cases)

for name, tmpl in prompts.items():
    acc = evaluate_prompt(tmpl)
    print(f"{name}: {acc:.2%}")
```





### 结语
:::success
大模型的能力确实越来越强，像 LongCat-Flash 这样的 MoE 模型，在激活参数仅 27B 的情况下，就能在 agentic 任务上超越 GPT-4.1。这意味着，**很多你以为需要微调的问题，其实只是 prompt 没写对**。

在动手微调之前，请先穷尽 prompt 工程、RAG、CoT 等“零训练成本”的手段。只有当这些方法都失效，且你有足够数据和明确需求时，微调才是最优解。

毕竟，**最好的微调，是不用微调**。

:::

