# ⓸ NL2Regex

<!-- source: yuque://zhongxian-iiot9/hlyypb/fxrf4ipfx9hrudiy -->

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：最近的研究调查了使用生成语言模型通过基于语义的方法生成正则表达式。然而，这些方法在实际应用中显示出缺点，</font>**<font style="color:#117CEE;">特别是在功能正确性方面</font>**<font style="color:rgb(51, 51, 51);">，功能正确性是指用户再现预期功能输入的能力。</font>

:::

:::color3
**简介：**<font style="color:rgb(51, 51, 51);">为了解决这个问题，我们提出了一种称为</font>**<font style="color:#ED740C;">单元测试驱动强化学习（UTD-RL）的新方法</font>**<font style="color:rgb(51, 51, 51);">。我们的方法与以前的方法不同，它考虑了</font>**<font style="color:#ED740C;">函数正确性</font>**<font style="color:rgb(51, 51, 51);">的关键方面，并使用</font>**<font style="color:#ED740C;">策略梯度技术将其转化为可微梯度反馈</font>**<font style="color:rgb(51, 51, 51);">。其中可以通过</font>**<font style="color:#ED740C;">单元测试来评估函数的正确性</font>**<font style="color:rgb(51, 51, 51);">，单元测试是一种确保正则表达式符合其设计并按预期执行的测试方法。</font>

**paper：**[**Enhancing Language Model with Unit Test Techniques for Efficient Regular Expression Generation**](https://aclanthology.org/2023.emnlp-industry.2.pdf)

:::

:::color5
**<font style="color:#601BDE;">1.Pipeline</font>**

:::

整个流程由3个步骤组成：

1. prompt生成：将从原始上下文生成提示
2. SFT：其中包含从第一步生成的提示
3. RL：实现了单元测试驱动的强化学习

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744265183546-47997ffd-c93d-4d2e-a9d9-5e44e3712e0b.png)

:::color5
**<font style="color:#601BDE;">2.Unit test  单元测试</font>**

:::

对生成的正则表达式和目标正则表达式进行单元测试。

+ 如果提取的结果相同，则认为测试用例通过。
+ 否则，测试用例将失败。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744265589666-0dcc2563-d909-4b92-8128-ced60d86ac91.png)

:::color5
**<font style="color:#601BDE;">3.应用pipeline</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744265459306-c2fd5a69-f350-4f54-8de8-9bde4df89dfd.png)

1. <font style="color:rgb(51, 51, 51);">LLM根据用户的请求生成正则表达式。</font>
2. <font style="color:rgb(51, 51, 51);">执行单元测试,以评估正则表达式的有效性。</font>
    1. <font style="color:rgb(51, 51, 51);">如果单元测试的结果超过阈值，则认为正则表达式有效。</font>
    2. <font style="color:rgb(51, 51, 51);">没有超过阈值：输入提示与失败的案例连接起来，以重新生成正则表达式。</font>

