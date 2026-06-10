# 大规模 RL 是如何训练的：从预训练到强化学习

<!-- source: yuque://zhongxian-iiot9/hlyypb/tno4w4stbd4gps5d -->

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">一句话总览</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">：Scaling 是过去十年 AI 进步最核心的驱动力。如今它正经历第二次蜕变——</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">从预训练走向强化学习（RL）</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">。本文系统梳理 Scaling Law 从预训练到 RL 的演化脉络：哪些规律依然成立，哪些假设彻底失效，以及面对混乱的 RL 设计空间，研究者们正在如何重新建立秩序。</font><font style="color:rgb(100, 37, 208);background-color:rgb(240, 244, 255);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">Ilya Sutskever 曾说，</font>**<font style="color:rgb(0, 0, 0);">Scaling</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">这一个词改变了整个领域的思维方式。本文以 Cameron R. Wolfe 博士的长篇技术博客《RL Scaling Laws for LLMs》为线索展开。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085051254-5b77e438-fd0c-4268-a73e-1daecbe6105d.png)

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">「机器学习以前的做法是，人们不断摆弄各种东西，试图得到有趣的结果……后来 Scaling 的洞见出现了。Scaling Law、GPT-3，所有人突然意识到我们应该去 Scaling。Scaling 只是一个词，但它无比强大——因为它直接告诉人们该怎么做。」</font>

<font style="color:rgb(143, 149, 158);background-color:rgb(245, 246, 247);">—— Ilya Sutskever</font>

## <font style="color:rgb(0, 0, 0);">🗺️</font><font style="color:rgb(0, 0, 0);"> 全文脉络</font>
<font style="color:rgb(0, 0, 0);">下面这张图是全文的导航——从预训练 Scaling Law 出发，过渡到 RL，再深入 RL 的算法、正则化与三篇核心 Scaling 研究，最后对比两类 Scaling Law 的本质差异。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085051427-eae7fac4-e319-4dd6-b86a-c4a4fab67a51.png)

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

---

# <font style="color:rgb(0, 0, 0);">01 · Scaling Law 基础</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">核心结论</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">：向预训练投入更多算力（更大的模型、更多数据），就能获得更好的性能。这种关系可以被</font><font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);"> </font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">Scaling Law</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">精确预测——甚至在训练之前就能估算大模型的表现。</font><font style="color:rgb(100, 37, 208);background-color:rgb(246, 241, 254);">（by草莓师姐）</font>

## <font style="color:rgb(0, 0, 0);">什么是幂律</font>
<font style="color:rgb(0, 0, 0);">预训练过程可以用</font>**<font style="color:rgb(0, 0, 0);">幂律</font>**<font style="color:rgb(0, 0, 0);">建模。最简单的幂律描述两个量的关系：</font><font style="color:rgb(0, 0, 0);">$$y = a \times x^$$</font><font style="color:rgb(0, 0, 0);">，其中</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">$$$$</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">控制曲线纵向位置，</font><font style="color:rgb(0, 0, 0);">$$$$</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">控制陡峭程度或方向。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085051443-fcad9a10-becc-4908-bb70-1bac09441ea9.png)

<font style="color:rgb(0, 0, 0);">但 LLM Scaling Law 的图像是</font>**<font style="color:rgb(0, 0, 0);">上下翻转</font>**<font style="color:rgb(0, 0, 0);">的——这是</font>**<font style="color:rgb(0, 0, 0);">逆</font>****<font style="color:rgb(0, 0, 0);">幂律</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">$$y = a \times (1/x)^$$</font><font style="color:rgb(0, 0, 0);">，在对数坐标下呈现标志性的线性关系。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085051506-9674fd66-7b5d-4e51-9301-ed40e0c4b6d0.png)

<font style="color:rgb(0, 0, 0);">在 LLM 预训练中，通过逆幂律建模的两个量是：</font>

1. **<font style="color:rgb(0, 0, 0);">测试损失 L</font>**<font style="color:rgb(0, 0, 0);">：下一个 token 预测 / 交叉熵损失（在同分布留出验证集上计算）。</font>
2. **<font style="color:rgb(0, 0, 0);">预训练</font>****<font style="color:rgb(0, 0, 0);">算力</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">C</font>**<font style="color:rgb(0, 0, 0);">：通过训练 FLOPs 估算，</font><font style="color:rgb(0, 0, 0);">$$C = 6 \times N \times $$</font><font style="color:rgb(0, 0, 0);">（N 为参数量，D 为处理的 token 数）。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">为什么系数是 6？</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">每个训练步执行一次前向传播（≈2N FLOPs/token）和一次反向传播（≈前向的 2 倍），合计每 token 约</font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);"> </font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">6N FLOPs</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">，再乘以总 token 数，即得</font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">$$C = 6N$$</font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">。</font>

## <font style="color:rgb(0, 0, 0);">神经 Scaling Law [13] 与 Chinchilla [14]</font>
<font style="color:rgb(0, 0, 0);">两篇奠基性论文确立了预训练 Scaling 的基本原则。文献 [13] 发现，在不受其他因素瓶颈制约时，</font>**<font style="color:rgb(0, 0, 0);">模型参数量、数据规模、训练</font>****<font style="color:rgb(0, 0, 0);">算力</font>**<font style="color:rgb(0, 0, 0);">三者各自与测试损失呈幂律关系。</font><font style="color:rgb(100, 37, 208);">（by草莓师姐）</font>

| **<font style="color:rgb(0, 0, 0);">论文</font>** | **<font style="color:rgb(0, 0, 0);">核心贡献</font>** | **<font style="color:rgb(0, 0, 0);">关键结论</font>** |
| :--- | :--- | :--- |
| **<font style="color:rgb(0, 0, 0);">神经 Scaling Law [13]</font>**<font style="color:rgb(0, 0, 0);"> (Kaplan, 2020)</font> | <font style="color:rgb(0, 0, 0);">验证三因素的幂律关系</font> | <font style="color:rgb(0, 0, 0);">算力跨 8 个数量级、模型规模跨 6 个、数据跨 2 个，性能平滑提升。固定算力下，</font>**<font style="color:rgb(0, 0, 0);">用更大模型训更少数据</font>**<font style="color:rgb(0, 0, 0);">更优</font> |
| **<font style="color:rgb(0, 0, 0);">Chinchilla [14]</font>**<font style="color:rgb(0, 0, 0);"> (Hoffmann, 2022)</font> | <font style="color:rgb(0, 0, 0);">最优算力分配</font> | <font style="color:rgb(0, 0, 0);">训练 400+ 模型发现 [13] 导致</font>**<font style="color:rgb(0, 0, 0);">训练不足</font>**<font style="color:rgb(0, 0, 0);">；算力最优时，</font>**<font style="color:rgb(0, 0, 0);">模型规模与数据规模应等比例增加</font>** |


![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085051467-c73467c7-ff85-405a-bf40-9b7653e4e4db.png)

**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">容易被误读的一点</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：幂律图多用对数坐标。换回普通坐标后，曲线形状类似</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">指数衰减</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">——这说明随着规模扩大，提升 LLM 质量会变得</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">指数级更困难</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">。</font>

---

# <font style="color:rgb(0, 0, 0);">02 · 超越预训练的 Scaling Law</font>
<font style="color:rgb(0, 0, 0);">推理模型的出现彻底改变了算力格局。过去算力主要投入预训练，后训练只是优化风格的小环节；而现在，</font>**<font style="color:rgb(0, 0, 0);">RL</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">训练阶段解锁了当今</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">LLM</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">最重要的能力</font>**<font style="color:rgb(0, 0, 0);">——从测试时思考到智能体能力。</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">「将 RL 算力 Scaling 正在成为推进 LLM 发展的关键范式……DeepSeek-R1-Zero 在 RL 训练上使用了 10 万 H800 GPU 小时，占其预训练算力的 3.75%。这种 RL 算力的大幅增加在前沿 LLM 迭代中被进一步放大：从 o1 到 o3 增加了超过 10 倍，Grok-3 到 Grok-4 也有类似飞跃。」</font><font style="color:rgb(100, 37, 208);background-color:rgb(245, 246, 247);">（by草莓师姐）</font>

<font style="color:rgb(143, 149, 158);background-color:rgb(245, 246, 247);">—— 来自 [1]</font>

<font style="color:rgb(0, 0, 0);">o1 的发布揭示了两个新的 Scaling 维度：</font>**<font style="color:rgb(0, 0, 0);">①</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">RL</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">训练</font>****<font style="color:rgb(0, 0, 0);">算力</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">和</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">② 推理时算力</font>**<font style="color:rgb(0, 0, 0);">。随后开源的 DeepSeek-R1 [15] 性能与 o1 相当，使推理能力成为新标准。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">承上启下</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：预训练有成熟的 Scaling Law 指导算力投入，但 RL 还没有。鉴于算力是 AI 进步的主要瓶颈，我们</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">迫切需要 RL 的 Scaling Law</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">来理解和预测大规模 RL 训练的结果。</font>

---

# <font style="color:rgb(0, 0, 0);">03 · 强化学习背景：GRPO</font>
<font style="color:rgb(0, 0, 0);">要理解 RL 的 Scaling 特性，必须先理解 RL 训练过程。本节重点介绍</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">GRPO</font>**<font style="color:rgb(0, 0, 0);">——目前推理模型大规模 RL 训练中最常用的算法（DeepSeek-R1 即用它）。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085051858-54a183f3-8b75-4f86-95af-4cfaef297d18.png)

## <font style="color:rgb(0, 0, 0);">GRPO 相对 PPO 的核心改变</font>
<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">GRPO 最大的改变在于</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">优势估计方式</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">：它</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">放弃了价值模型（Critic）</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">，转而为每个提示采样一「组」完成序列，用组内奖励的均值和标准差归一化来估计优势，从而大幅降低内存与算力开销。</font><font style="color:rgb(100, 37, 208);background-color:rgb(246, 241, 254);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">下图对比了 PPO 与 GRPO 的优势估计路径：</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

<font style="color:rgb(0, 0, 0);">具体而言，完成序列</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">$$$$</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">的优势通过组内归一化计算，组内每个完成序列的所有 token 共享同一优势值：</font>

<font style="color:rgb(0, 0, 0);">$$A_i = \frac{r_i - \text{mean}(\{r_1,...,r_G\})}{\text{std}(\{r_1,...,r_G\})$$</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781085052124-a2d878ed-36ad-4c33-9f4d-2887c228899f.png)

## <font style="color:rgb(0, 0, 0);">损失函数与聚合</font>
<font style="color:rgb(0, 0, 0);">GRPO 损失与 PPO 相似，核心是</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">token 级策略比率</font>**<font style="color:rgb(0, 0, 0);">（重要性比率），并采用相同的截断机制，取截断与未截断目标的最小值。默认聚合方式：</font>

1. <font style="color:rgb(0, 0, 0);">对每个完成序列内的 token 级损失取平均；</font>
2. <font style="color:rgb(0, 0, 0);">对组内各完成序列的损失再取平均。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">常见误解</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：GRPO 并没有消除奖励模型的需求——它的原始论文 [4] 就用了奖励模型。去除奖励模型是</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">可验证奖励</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">的优势，GRPO 的真正贡献是</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">消除了价值模型</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">。此外 GRPO 通常需要较大批次以保证优势估计可靠。</font>

---

# <font style="color:rgb(0, 0, 0);">04 · GRPO 的近期变体</font>
<font style="color:rgb(0, 0, 0);">DeepSeek-R1 爆红后，研究者提出大量 GRPO 改进。下图把主流变体按"</font>**<font style="color:rgb(0, 0, 0);">它们各自解决什么问题</font>**<font style="color:rgb(0, 0, 0);">"归类：</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

## <font style="color:rgb(0, 0, 0);">逐一解析</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">GSPO（组序列策略优化）[5]</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">· 解决 token 级比率高方差</font><font style="color:rgb(100, 37, 208);background-color:rgb(240, 244, 255);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">GRPO 的错位：优势在</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">序列级</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">计算，策略比率却在</font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);"> </font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">token 级</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">计算。token 级比率方差大，单个 token 可能主导损失甚至引发数值不稳定（长序列、大型 MoE 尤其突出）。GSPO 改在</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">序列级</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">计算重要性比率（用 token 概率的几何平均的对数形式），使不同长度序列可比，数值更稳。被 Qwen3-235B-A22B 等采用。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">DAPO（动态采样策略优化）[6]</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">· 一套实用改进的集合</font>

| **<font style="color:rgb(0, 0, 0);">问题</font>** | **<font style="color:rgb(0, 0, 0);">DAPO 的对策</font>** |
| :--- | :--- |
| <font style="color:rgb(0, 0, 0);">熵崩溃（截断惩罚低概率探索 token）</font> | **<font style="color:rgb(0, 0, 0);">Clip Higher</font>**<font style="color:rgb(0, 0, 0);">：解耦上下截断界，ε_low=0.2、ε_high=0.28</font> |
| <font style="color:rgb(0, 0, 0);">全对组优势为零、稀释有效批次</font> | **<font style="color:rgb(0, 0, 0);">动态采样</font>**<font style="color:rgb(0, 0, 0);">：过滤满分提示，持续采样直到批次填满</font> |
| <font style="color:rgb(0, 0, 0);">长序列 token 贡献偏小</font> | <font style="color:rgb(0, 0, 0);">对批次中</font>**<font style="color:rgb(0, 0, 0);">所有 token</font>**<font style="color:rgb(0, 0, 0);">直接取平均（改进损失聚合）</font> |
| <font style="color:rgb(0, 0, 0);">超长完成序列</font> | <font style="color:rgb(0, 0, 0);">基于长度的</font>**<font style="color:rgb(0, 0, 0);">软惩罚</font>**<font style="color:rgb(0, 0, 0);">，接近上限时平滑增大</font> |


**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">Dr. GRPO（GRPO Done Right）[7]</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">· 去掉两个偏差</font>

1. **<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">响应级长度偏差</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">：用固定常数 MAX_TOKENS 替代序列级平均，把响应长度从聚合中剥离。</font>
2. **<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">问题级难度偏差</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">：从优势估计器中</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">去除</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">标准差</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">项</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">，避免极易/极难问题优势值过大。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">TIS（截断重要性采样）[9]</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">· 纠正推理/训练引擎不匹配</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">现代 RL 框架中，采样轨迹（vLLM/SGLang，低精度）与策略更新（FSDP/DeepSpeed）由</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">不同引擎</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">处理，导致 token 概率不可忽视的差异。TIS 在策略梯度中引入 learner/sampler 概率的重要性比率，并</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">单侧截断到最大值 ρ</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">，自动纠正不匹配。已被 verl、OpenInstruct 采用。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">CISPO（截断重要性采样权重策略优化）[8/10]</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">· 让被截断的 token 也能参与</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">重要的"分叉" token（如「啊哈」「等等」）初始概率低，更新后比率骤增随即被截断。在 MiniMax-M1 每批 16 次更新的设置下损害很大。CISPO 对截断后的比率施加</font><font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);"> </font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">stop gradient</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">，把比率当作</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">权重</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">，确保</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">所有 token（含被截断的）都以有限权重参与</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 241, 241);">策略梯度。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">TIS</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>****<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">vs CISPO（都用重要性比率，但目标不同）</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">：CISPO 用 PPO/GRPO 的比率定义，通过截断强制信任域，只改截断方式让所有 token 参与；TIS 用比率捕捉</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">引擎间</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">概率差异，纠正训练/推理不匹配。</font>

---

# <font style="color:rgb(0, 0, 0);">05 · RL 的正则化</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">KL</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);"> </font>****<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">散度</font>**

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">将策略锚定到参考策略（通常是基础模型），防止 LLM 变化过大。最常用的近似是当前/参考策略在 token 级对数概率的差值。</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">纳入方式两种：① 直接从奖励中减去（PPO）；② 作为惩罚项加入损失（GRPO）。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">熵</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">奖励</font>**

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">激励 LLM 保持不确定性，避免过于自信的 token 分布，防止阻碍探索的</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">熵</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">崩溃</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">。</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">通常每个 token 计算熵后在轨迹上取平均，用系数 β 缩放纳入奖励或损失。</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">近期 RL 流程中正则化使用已较少见，且因 GRPO 流行更倾向于</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">加入</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">损失函数</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">而非奖励。在大规模、以推理为导向的 RL 中，</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">偏离参考策略未必是坏事</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">，完全省略 KL 也越来越普遍。</font>

---

# <font style="color:rgb(0, 0, 0);">06 · Scaling RL 训练过程</font>
<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">「虽然 LLM 的 RL 算力已大规模 Scaling，但我们对如何 Scaling RL 的理解却没有跟上步伐；这一方法论仍然更多是一门艺术，而非科学。」</font><font style="color:rgb(100, 37, 208);background-color:rgb(245, 246, 247);">（by草莓师姐）</font>

<font style="color:rgb(143, 149, 158);background-color:rgb(245, 246, 247);">—— 来自 [1]</font>

<font style="color:rgb(0, 0, 0);">本节介绍三篇致力于建立 RL Scaling 秩序的核心论文。先用一张表把它们放在一起对比：</font>

| **<font style="color:rgb(0, 0, 0);">论文</font>** | **<font style="color:rgb(0, 0, 0);">Scaling 形式</font>** | **<font style="color:rgb(0, 0, 0);">主要问题</font>** | **<font style="color:rgb(0, 0, 0);">代表产出</font>** |
| :--- | :--- | :--- | :--- |
| **<font style="color:rgb(0, 0, 0);">[1]</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">RL</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">算力</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">Scaling 的艺术</font>** | <font style="color:rgb(0, 0, 0);">S 形（sigmoid）算力-性能曲线</font> | <font style="color:rgb(0, 0, 0);">如何系统识别可 Scaling 的 RL 方案</font> | **<font style="color:rgb(0, 0, 0);">ScaleRL</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">最优方案，验证至 10 万 GPU 小时</font> |
| **<font style="color:rgb(0, 0, 0);">[2]</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">RL</font>****<font style="color:rgb(0, 0, 0);"> </font>****<font style="color:rgb(0, 0, 0);">后训练的 Scaling 行为</font>** | <font style="color:rgb(0, 0, 0);">测试损失 vs 算力/数据的对数线性幂律</font> | <font style="color:rgb(0, 0, 0);">模型规模/数据/算力如何影响性能</font> | <font style="color:rgb(0, 0, 0);">跨模型 + 单模型外推；规模交叉现象</font> |
| **<font style="color:rgb(0, 0, 0);">[3] 采样</font>****<font style="color:rgb(0, 0, 0);">算力</font>****<font style="color:rgb(0, 0, 0);">最优 Scaling</font>** | <font style="color:rgb(0, 0, 0);">对 (B_p, n, M) 的算力受限优化</font> | <font style="color:rgb(0, 0, 0);">固定算力如何分配采样资源</font> | <font style="color:rgb(0, 0, 0);">增大每提示滚出数 n 比单纯延长训练更优</font> |


## <font style="color:rgb(0, 0, 0);">6.1 RL 算力 Scaling 的艺术 [1]</font>
<font style="color:rgb(0, 0, 0);">文献 [1] 用</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">S 形曲线</font>**<font style="color:rgb(0, 0, 0);">建模 RL 训练：奖励增益与算力（GPU 小时）的关系。</font>

<font style="color:rgb(0, 0, 0);">$$\text{Reward Gain} = A \cdot \frac{1}{1 + (C_{mid}/C)^B$$</font>

<font style="color:rgb(0, 0, 0);">其中</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">A</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">是渐近奖励上限，</font>**<font style="color:rgb(0, 0, 0);">C_mid</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">是曲线中点算力，</font>**<font style="color:rgb(0, 0, 0);">B</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">是控制陡峭程度的效率指数。RL 训练呈现"早期几乎不变 → 快速提升 → 趋于平稳"的形态。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">关键取舍</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：当两种设置无法同时改善 A 和 B 时，[1] 把</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">渐近性能 A 的提升置于效率 B 之上</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">——因为效率降低可以靠延长训练弥补，而渐近性能上限难以恢复。</font>

**<font style="color:rgb(0, 0, 0);">ScaleRL 的诞生</font>**<font style="color:rgb(0, 0, 0);">：作者从基准设置出发，在 4K → 8K → 16K → 100K GPU 小时多阶段消融各种干预，用拟合的 Scaling Law 外推性能，从而高效筛选可 Scaling 的设计。下图是这套"消融—外推—整合"的工作流：</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

**<font style="color:rgb(0, 0, 0);">逐项消融的发现</font>**<font style="color:rgb(0, 0, 0);">（小规模 4–8K GPU 小时实验）：</font>

| **<font style="color:rgb(0, 0, 0);">维度</font>** | **<font style="color:rgb(0, 0, 0);">最佳选择</font>** | **<font style="color:rgb(0, 0, 0);">影响</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(0, 0, 0);">损失类型</font> | **<font style="color:rgb(0, 0, 0);">CISPO</font>**<font style="color:rgb(0, 0, 0);">（优于 GSPO、基准）</font> | <font style="color:rgb(0, 0, 0);">渐近性能 A ↑，效率略优</font> |
| <font style="color:rgb(0, 0, 0);">异步架构</font> | **<font style="color:rgb(0, 0, 0);">PipelineRL</font>**<font style="color:rgb(0, 0, 0);">（K=8 限制异步度）</font> | <font style="color:rgb(0, 0, 0);">A 相当但效率 B 显著更高</font> |
| <font style="color:rgb(0, 0, 0);">LM Head 精度</font> | **<font style="color:rgb(0, 0, 0);">FP32 全精度头</font>** | <font style="color:rgb(0, 0, 0);">A 与 B 同时改善（减少训推不匹配）</font> |
| <font style="color:rgb(0, 0, 0);">损失聚合</font> | **<font style="color:rgb(0, 0, 0);">DAPO 风格</font>** | <font style="color:rgb(0, 0, 0);">表现最佳</font> |
| <font style="color:rgb(0, 0, 0);">优势归一化</font> | <font style="color:rgb(0, 0, 0);">批次奖励标准差</font> | <font style="color:rgb(0, 0, 0);">影响小，略优</font> |
| <font style="color:rgb(0, 0, 0);">数据筛选</font> | <font style="color:rgb(0, 0, 0);">过滤零方差提示 + 不正样本重采样（移除通过率>90%）</font> | <font style="color:rgb(0, 0, 0);">渐近性能 ↑，避免浪费算力</font> |


**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">验证</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：用 8K GPU 小时拟合 sigmoid 曲线，准确预测了 16K 实验结束时的性能；进一步 Scaling 到</font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);"> </font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">10 万 GPU 小时</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">，外推依旧吻合，并能推广到 MoE 模型。</font><font style="color:rgb(100, 37, 208);background-color:rgb(240, 251, 239);">（by草莓师姐）</font>

## <font style="color:rgb(0, 0, 0);">6.2 RL 后训练的 Scaling 行为 [2]</font>
<font style="color:rgb(0, 0, 0);">用完整 Qwen-2.5 系列（0.5B–72B，含基础/指令模型，60+ 实验）研究，仅用原始 GRPO，发现 RL 也遵循</font>**<font style="color:rgb(0, 0, 0);">对数</font>****<font style="color:rgb(0, 0, 0);">线性</font>****<font style="color:rgb(0, 0, 0);">幂律</font>**<font style="color:rgb(0, 0, 0);">（测试损失=错误率=1−accuracy）：</font>

<font style="color:rgb(0, 0, 0);">$$L(N, X) = E(N) - K(N) \cdot \log $$</font>

<font style="color:rgb(0, 0, 0);">支持两种外推：</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">跨模型（inter-model）</font>**

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">用 0.5B–32B 的结果预测 72B 的性能。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">单模型（intra-model）</font>**

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">用早期训练轨迹预测后续训练性能。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">规模交叉现象</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：学习效率 K(N) 随模型规模呈饱和 S 形增长。固定算力下小模型能跑更多步，所以</font><font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);"> </font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">32B 在低算力预算下优于 72B</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">，但算力增大后出现交叉点，此后 72B 反超。本质是模型规模与训练步数的权衡。</font>

**<font style="color:rgb(0, 0, 0);">其他结论</font>**<font style="color:rgb(0, 0, 0);">：固定数据下更大模型样本效率更高；性能主要由总数据量 D_total 决定，对数据复用系数 τ 相对鲁棒（τ<25 无显著下降）。</font>

## <font style="color:rgb(0, 0, 0);">6.3 采样算力的最优 Scaling [3]</font>
<font style="color:rgb(0, 0, 0);">把 RL 总算力建模为</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">$$C = B_p \times n \times $$</font><font style="color:rgb(0, 0, 0);">（每批提示数 × 每提示滚出数 × 训练步数），聚焦如何分配</font>**<font style="color:rgb(0, 0, 0);">采样算力</font>**<font style="color:rgb(0, 0, 0);">（B_p、n）。下图是这套"从低算力外推最优分配"的实践流程：</font><font style="color:rgb(100, 37, 208);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">主要结论</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：随算力预算增加，最优</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">每提示滚出数 n</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">也增大并最终饱和——</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">把增量算力用于多采样 rollout，比单纯延长训练更好</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">。难数据集上最优 n 较小；B_p 在合理范围内主要影响训练稳定性。</font>

**<font style="color:rgb(0, 0, 0);">难度相关的</font>****<font style="color:rgb(0, 0, 0);">正则化</font>**<font style="color:rgb(0, 0, 0);">：简单数据集用熵奖励 + KL（延迟熵爆炸）；困难数据集不用任何正则化（避免熵爆炸）。学习率随批次大小的</font>**<font style="color:rgb(0, 0, 0);">平方根</font>**<font style="color:rgb(0, 0, 0);">缩放。</font>

---

# <font style="color:rgb(0, 0, 0);">07 · RL 与预训练 Scaling Law 的本质对比</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">核心发现</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">：两个领域中的"Scaling Law"是</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">截然不同</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">的概念。预训练高度标准化，RL 则混乱、定制化、领域特异。</font><font style="color:rgb(100, 37, 208);background-color:rgb(240, 244, 255);">（by草莓师姐）</font>

| **<font style="color:rgb(0, 0, 0);">维度</font>** | **<font style="color:rgb(0, 0, 0);">预训练 Scaling Law</font>** | **<font style="color:rgb(0, 0, 0);">RL Scaling Law</font>** |
| :--- | :--- | :--- |
| **<font style="color:rgb(0, 0, 0);">衡量性能（Y 轴）</font>** | <font style="color:rgb(0, 0, 0);">交叉熵损失，稳定、普适</font> | <font style="color:rgb(0, 0, 0);">奖励 / 准确率，嘈杂、领域特异</font> |
| **<font style="color:rgb(0, 0, 0);">定义</font>****<font style="color:rgb(0, 0, 0);">算力</font>****<font style="color:rgb(0, 0, 0);">（X 轴）</font>** | <font style="color:rgb(0, 0, 0);">干净：C = 6ND</font> | <font style="color:rgb(0, 0, 0);">含采样+更新，难精确定义（FLOPs 或 GPU 小时）</font> |
| **<font style="color:rgb(0, 0, 0);">外推方式</font>** | <font style="color:rgb(0, 0, 0);">主要跨模型</font> | <font style="color:rgb(0, 0, 0);">跨模型 + 单模型（预测特定配置是否可行）</font> |
| **<font style="color:rgb(0, 0, 0);">标准化程度</font>** | <font style="color:rgb(0, 0, 0);">高，方法成熟</font> | <font style="color:rgb(0, 0, 0);">低，旋钮多，配置微变即改变趋势</font> |


## <font style="color:rgb(0, 0, 0);">实践要点</font>
1. **<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">特定设置内可预测</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：单模型外推可在训练早期判断设置可行性；跨模型外推提供洞见但未必跨配置迁移。</font>
2. **<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">设计决策非单一维度</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：有的影响学习效率（可靠延长训练弥补），有的影响渐近性能（难恢复）。许多 GRPO 变体主要利好效率与稳定性。</font>
3. **<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">更大模型通常更好</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">，但算力/数据紧张时小模型反而有利（学习效率随规模饱和）。</font>
4. **<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">投入更多</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">算力</font>****<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">的方式</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：多训练步 or 每步更多推理算力。尽管算力以推理为主，多数 Scaling Law 表明</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">把算力分配给采样完成序列</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">是有益的；RL 对数据复用鲁棒、受益于大批次。</font>

---

**<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">参考文献（节选）</font>**

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [1] The art of scaling RL compute for LLMs, arXiv:2510.13786</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [2] Scaling behaviors of LLM RL post-training, arXiv:2509.25300</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [3] IsoCompute Playbook, arXiv:2603.12151</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [4] DeepSeekMath (GRPO), arXiv:2402.03300</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [5] GSPO, arXiv:2507.18071</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [6] DAPO, arXiv:2503.14476</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [7] Dr. GRPO, arXiv:2503.20783</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [8/10] MiniMax-M1, arXiv:2506.13585</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [9] Off-policy RL (TIS)</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [11] PipelineRL, arXiv:2509.19128</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [13] Scaling laws for neural LM, arXiv:2001.08361</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [14] Chinchilla, arXiv:2203.15556</font><font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);"> </font>

<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">· [15] DeepSeek-R1, arXiv:2501.12948</font>

