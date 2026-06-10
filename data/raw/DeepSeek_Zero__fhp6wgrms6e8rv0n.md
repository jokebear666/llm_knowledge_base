# DeepSeek Zero

<!-- source: yuque://zhongxian-iiot9/hlyypb/fhp6wgrms6e8rv0n -->

:::color3
+ <font style="color:rgb(0, 0, 0);">采用PPO改进版GRPO强化学习策略</font>
+ <font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">奖励模型：是RL学习方向的刺激信号。基于rule来设计奖励模型，包括2方面：准确性和format</font>
+ <font style="color:rgb(0, 0, 0);">输出模板：如下，比较简单。必须先输出think 过程；然后输出结果。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738811381629-646699d3-ab18-45a5-870f-7fba294ec66f.png)

:::color5
**<font style="color:#601BDE;">1. 核心理念</font>**

:::

简单来说，R1-zero 旨在从预训练模型（Base Model）出发，直接通过 RL（强化学习） 得到一个具有优秀 Reasoning（推理）能力的模型。Deepseek 希望通过这种自探索的方式，验证是否可以在无需任何“Ground Truth CoT（思维链）”引导的情况下，让模型自主学会思考并解决问题。

:::color5
**<font style="color:#601BDE;">2.训练实现</font>**

:::

通过 Prompt 控制 R1-zero 在训练过程中生成两部分内容：

+ 思考过程：由 `<think></think>` 包裹。
+ 最终答案：由 `<answer></answer>` 包裹。

:::color5
**<font style="color:#601BDE;">3.Reward（奖励）计算规则</font>**

:::

对生成的两部分内容，依照以下规则计算 Reward：

1. 准确率：答案是否与 Ground Truth (GT) 一致。
2. 格式：强制要求模型将所有的思考过程包裹在 `<think>` 标签内。

:::color5
**<font style="color:#601BDE;">4.算法与效果</font>**

:::

+ 算法：利用 GRPO 算法计算 Loss，Reward 用于计算该条 Response 的优势值。
+ 涌现现象：
    - 随着 RL 自探索的进行，准确率不断提升。
    - 模型生成的内容长度不断增加（Test-time scaling），证明模型通过生成对解题有用的 Token 来提升处理复杂问题的能力。
    - 自进化：无需显式要求，模型在自探索中演化出了自验证、搜索等高级功能。

:::color5
**<font style="color:#601BDE;">5. 核心理念</font>**

:::

<font style="color:rgb(0, 0, 0);">AIME2024数学推理效果提升非常明显，从15</font>**<font style="color:rgb(0, 0, 0);">.6%到71%</font>**<font style="color:rgb(0, 0, 0);">（达到了OpenAI-O1-0912水平）</font>

+ <font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">它坚定的表明，不借助监督学习(SFT) </font><font style="color:#DF2A3F;">只靠RL可以原生、自发的进化出来强大的reasoning能力</font><font style="color:rgb(0, 0, 0);">，比如反思、多种方式尝试等。</font>
+ <font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">内部分析表明，随着推理步数的增加，reasoning效果明显变化（蓝色曲线）；且通过多数投票方式majority voting，还能再提升效果到</font>**<font style="color:rgb(0, 0, 0);">86.7%</font>**
+ <font style="color:rgb(0, 0, 0);">模型会自发出现</font><font style="color:#DF2A3F;">拟人化的思考过程</font>**<font style="color:rgb(0, 0, 0);">。</font>**

