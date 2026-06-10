# GSPO

<!-- source: yuque://zhongxian-iiot9/hlyypb/cd150egfxzzyf0h9 -->

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756286800058-5c1ddb48-e389-410e-83a3-83010c95c2b1.png)

:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>[<font style="color:#000000;">Qwen3</font>](https://zhida.zhihu.com/search?content_id=260883180&content_type=Article&match_order=1&q=Qwen3&zhida_source=entity)<font style="color:#000000;"> 最新</font>[<font style="color:#000000;">GSPO</font>](https://zhida.zhihu.com/search?content_id=260883180&content_type=Article&match_order=1&q=GSPO&zhida_source=entity)<font style="color:#000000;">强化学习方法，把</font><font style="color:rgb(25, 27, 31);">奖励计算从token级别 改成了sequence 级别，</font>**<font style="color:#74B602;">解决了LLM 过多的关注token导致训练不稳定的问题</font>**<font style="color:rgb(25, 27, 31);">，而且主流的强化学习框架，</font>[<font style="color:#000000;">TRL</font>](https://zhida.zhihu.com/search?content_id=260883180&content_type=Article&match_order=1&q=TRL&zhida_source=entity)<font style="color:#000000;">，</font>[<font style="color:#000000;">Verl</font>](https://zhida.zhihu.com/search?content_id=260883180&content_type=Article&match_order=1&q=Verl&zhida_source=entity)<font style="color:#000000;"> 都</font><font style="color:rgb(25, 27, 31);">已经立马进行了支持，也显示出GSPO的价值。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">Qwen 团队提出了一种名为</font>**<font style="color:#ED740C;">「</font>**[**<font style="color:#ED740C;">组序列策略优化</font>**](https://zhida.zhihu.com/search?content_id=260894336&content_type=Article&match_order=1&q=%E7%BB%84%E5%BA%8F%E5%88%97%E7%AD%96%E7%95%A5%E4%BC%98%E5%8C%96&zhida_source=entity)**<font style="color:#ED740C;">」（Group Sequence Policy Optimization, GSPO）</font>**<font style="color:rgb(25, 27, 31);">的新型强化学习算法，尝试解决训练超大规模语言模型时遇到的不稳定和效率低下的问题。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

**paper：**[Group Sequence Policy Optimization](https://arxiv.org/pdf/2507.18071)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756286822640-85cca5f2-8483-4d51-96e8-3411c38706e7.png)

:::color5
**<font style="color:#601BDE;">1.创新点 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ <font style="color:rgb(25, 27, 31);">与以往算法（如</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">GRPO</font>](https://zhida.zhihu.com/search?content_id=260894336&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）在单个 token 层面进行调整不同，GSPO 的核心思想是在整个句子或段落（sequence）的层面上进行评估和优化。</font>
+ <font style="color:rgb(25, 27, 31);">它认为，奖励是给整个回复的，那么模型的更新也应该基于整个回复的表现，而不是拆分到每个词。</font>
+ <font style="color:rgb(25, 27, 31);">论文通过实验证明，GSPO 不仅训练过程更稳定、效率更高，尤其是在训练复杂的混合专家（MoE）模型时表现出色，还简化了训练系统的设计。</font>
+ <font style="color:rgb(25, 27, 31);">这一算法的成功应用，是最新 Qwen3 模型性能显著提升的关键因素之一。</font>

## <font style="color:rgb(25, 27, 31);">一、背景知识：LLM 强化学习</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">当前主流的 LLM 的训练，基本分为三个步骤：</font>

1. **<font style="color:rgb(25, 27, 31);">预训练</font>**<font style="color:rgb(25, 27, 31);">：让模型阅读互联网上几乎所有的文本，学会语言的规律和海量的知识。</font>
2. **<font style="color:rgb(25, 27, 31);">监督微调</font>**<font style="color:rgb(25, 27, 31);">：用高质量的问答数据对模型进行调教，让它学会按指令进行对话。</font>
3. **<font style="color:rgb(25, 27, 31);">强化学习</font>**<font style="color:rgb(25, 27, 31);">：目标是提升模型的推理、遵循复杂指令等高阶能力。</font>

<font style="color:rgb(25, 27, 31);">我们重点关注第三步。目前 LLM 的 RL 阶段，最主流的算法是 </font>**<font style="color:rgb(25, 27, 31);">PPO（Proximal Policy Optimization）</font>**<font style="color:rgb(25, 27, 31);"> 以及其衍生品。</font>

:::

:::color5
**<font style="color:#601BDE;">1.PPO：小步快跑，保持稳定</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">PPO 的核心思想是「小步快跑，保持稳定」。比如一下你在训练一只宠物狗（LLM）：</font>

+ **<font style="color:rgb(25, 27, 31);">指令（Prompt）</font>**<font style="color:rgb(25, 27, 31);">：你对它说「握手」。</font>
+ **<font style="color:rgb(25, 27, 31);">动作（Response）</font>**<font style="color:rgb(25, 27, 31);">：它可能抬起了左脚。</font>
+ **<font style="color:rgb(25, 27, 31);">奖励（Reward）</font>**<font style="color:rgb(25, 27, 31);">：你觉得还不错，给它一个 80 分的奖励。</font>
+ **<font style="color:rgb(25, 27, 31);">学习（Optimization）</font>**<font style="color:rgb(25, 27, 31);">：PPO 算法会微调狗的「大脑」（模型参数），让它下次更有可能做出「抬左脚」这个动作。</font>

<font style="color:rgb(25, 27, 31);">为了防止狗一下子学「野」了，做出一些奇怪的动作，PPO 会确保每次更新后的新策略和旧策略不会相差太远。这就是「近端（Proximal）」的含义。</font>

<font style="color:rgb(25, 27, 31);">这个过程依赖一个至关重要的数学工具——</font>[**<font style="color:rgb(9, 64, 142);">重要性采样</font>**](https://zhida.zhihu.com/search?content_id=260894336&content_type=Article&match_order=1&q=%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">（Importance Sampling）</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">2.重要性采样</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">在训练中，为了提高效率，我们通常是用「旧模型」生成一大批数据，然后用这批数据来更新「新模型」。这就带来一个问题：用旧模型的数据来指导新模型，会不会有偏差？</font>

<font style="color:rgb(25, 27, 31);">会的。重要性采样就是解决这个问题的，它的思想是：我们可以通过给旧的每个数据点乘以一个「权重」，来修正它的代表性，从而估算出当前的情况。</font>

<font style="color:rgb(25, 27, 31);">这个权重就是</font>**<font style="color:rgb(25, 27, 31);">重要性权重（Importance Ratio）</font>**<font style="color:rgb(25, 27, 31);">，它的计算方式很简单：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756287303586-c933f12e-3315-483b-9973-afd99dc10fd8.png)

<font style="color:rgb(25, 27, 31);">如果一个动作在新策略下变得更可能出现，它的权重就大于 1，反之小于 1。通过这个权重，PPO 就能利用旧数据安全地更新模型了。</font>

:::color5
**<font style="color:#601BDE;">3.PPO 的局限</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">PPO 有一个巨大的实践难题：它需要一个额外的</font>**<font style="color:rgb(25, 27, 31);">价值模型（Value Model）</font>**<font style="color:rgb(25, 27, 31);">，或者叫 Critic 模型。注意，不要把价值模型和奖励模型弄混淆。价值模型不是提供额外的奖励来源，而是通过学习预测未来的期望回报，提供了一个动态的基准，用来校准 RM 提供的原始奖励信号，生成更稳定、信息量更大的 Advantage 信号，从而稳定并加速 PPO 的训练。</font>

<font style="color:rgb(25, 27, 31);">目前常见的做法，价值模型会给</font>**<font style="color:rgb(25, 27, 31);">每一个 token</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">打分，而且它和策略模型本身一样大，训练它既耗费资源又困难，而且估算往往不准，成为整个系统中最脆弱的一环。</font>

## <font style="color:rgb(25, 27, 31);">二、前人的做法</font>
:::color5
**<font style="color:#601BDE;">1.GRPO：用平均分充当基线</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">为了摆脱昂贵的价值模型，DeepSeek 团队提出了</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">GRPO（Group Relative Policy Optimization）</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">算法。</font>

<font style="color:rgb(25, 27, 31);">GRPO 的想法是：我不需要一个额外的价值模型来给打一个「绝对分」，而是采样多次，直接用奖励模型的平均值来充当这个「基线」，或者叫「优势」（Advantage）。</font>

<font style="color:rgb(25, 27, 31);">具体来说，针对同一个问题，GRPO 让模型生成一组（比如 4 个）不同的回答。然后，一个奖励模型会给这 4 个回答分别打一个总分。</font>

+ <font style="color:rgb(25, 27, 31);">回答 A：95 分</font>
+ <font style="color:rgb(25, 27, 31);">回答 B：70 分</font>
+ <font style="color:rgb(25, 27, 31);">回答 C：85 分</font>
+ <font style="color:rgb(25, 27, 31);">回答 D：80 分</font>

<font style="color:rgb(25, 27, 31);">平均分是 82.5 分。那么：</font>

+ <font style="color:rgb(25, 27, 31);">回答 A 的</font>**<font style="color:rgb(25, 27, 31);">优势（Advantage）</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">就是正的，因为它高于平均分。</font>
+ <font style="color:rgb(25, 27, 31);">回答 B 的优势就是负的，因为它低于平均分。</font>

<font style="color:rgb(25, 27, 31);">这样，GRPO 就巧妙地绕过了价值模型，通过组内排名的相对优势来指导模型学习。对于优势为正的回答，模型会学习增加它出现的概率；对于优势为负的，则降低其概率。</font>

:::color5
**<font style="color:#601BDE;">2.GRPO 的局限</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen 团队指出，GRPO 在应用 PPO 的核心机制——重要性采样时，犯了一个错误：GRPO 在 token 级别计算重要性权重，而不是在整个序列级别。</font>

<font style="color:rgb(25, 27, 31);">在数学上，重要性采样理论要求我们对从一个分布中采出的</font>**<font style="color:rgb(25, 27, 31);">多个样本</font>**<font style="color:rgb(25, 27, 31);">求平均，才能准确修正分布的偏差。而 GRPO 在每个时间步，只基于</font>**<font style="color:rgb(25, 27, 31);">一个</font>**<font style="color:rgb(25, 27, 31);">采样出的词元y</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);">来计算权重，这个权重充满了随机噪声，失去了修正分布的意义。</font>

<font style="color:rgb(25, 27, 31);">这种噪声会随着回答的变长而不断累积，最终像滚雪球一样，引发灾难性的</font>**<font style="color:rgb(25, 27, 31);">模型崩溃</font>**<font style="color:rgb(25, 27, 31);">。尤其是在训练深度更深、结构更复杂的</font>**<font style="color:rgb(25, 27, 31);">混合专家（MoE）模型</font>**<font style="color:rgb(25, 27, 31);">时，这种不稳定性会被急剧放大。</font>

:::color5
**<font style="color:#601BDE;">3.</font>**[**<font style="color:#601BDE;">路由回放</font>**](https://zhida.zhihu.com/search?content_id=260894336&content_type=Article&match_order=1&q=%E8%B7%AF%E7%94%B1%E5%9B%9E%E6%94%BE&zhida_source=entity)**<font style="color:#601BDE;">（Routing Replay）</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">为了让 GRPO 这类算法能在混合专家（MoE）模型上稳定运行，研究者们采用了一种名为</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">「路由回放」（Routing Replay）</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的策略。</font>

<font style="color:rgb(25, 27, 31);">可以将 MoE 模型类比为一个拥有众多专家的咨询公司。每次处理一个词元时，都会由一个「路由网络」指派几位最相关的专家参与计算。问题在于，模型参数稍有更新，这个「指派名单」就可能发生变化，导致前后两次计算缺乏可比性。</font>

<font style="color:rgb(25, 27, 31);">「路由回放」的作用：</font>

+ <font style="color:rgb(25, 27, 31);">在模型生成数据时，记录下每个词元由哪些专家处理。</font>
+ <font style="color:rgb(25, 27, 31);">在模型优化、需要进行新旧对比时，强制新模型「回放」这套完全相同的专家指派名单。</font>

<font style="color:rgb(25, 27, 31);">尽管有效，但这毕竟是一个额外的「补丁」，增加了系统复杂性，也限制了模型自由探索更优专家组合的能力。而 GSPO 的出现，则从根本上解决了这个问题，让这个补丁变得不再必要。</font>

## <font style="color:rgb(25, 27, 31);">三、GSPO 的核心机制</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介：</font>**<font style="color:rgb(25, 27, 31);">GSPO 的核心思想简单而深刻：</font>**<font style="color:rgb(25, 27, 31);">奖励的单位，应该与优化的单位相匹配。</font>**

<font style="color:rgb(25, 27, 31);">奖励是给</font>**<font style="color:rgb(25, 27, 31);">整个回答序列</font>**<font style="color:rgb(25, 27, 31);">的，那么我们的重要性权重和优化过程，也应该在</font>**<font style="color:rgb(25, 27, 31);">序列（Sequence）</font>**<font style="color:rgb(25, 27, 31);"> 的层面上进行。这就像老师批改作文，是通读全文后给出一个总分和评语，而不是逐字逐句地打分。</font>

:::

:::color5
**<font style="color:#601BDE;">1.序列级重要性权重</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">GSPO 抛弃了 GRPO 的词元级权重，定义了一个全新的</font>**<font style="color:rgb(25, 27, 31);">序列级重要性权重</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756287357704-d75ad0be-8e55-42d1-868b-368b2ad27de6.png)

<font style="color:rgb(25, 27, 31);">其中：</font>

+ ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756287366816-33920b35-db91-4aa0-aa4a-74e98e55b030.png)<font style="color:rgb(25, 27, 31);">：这是整个序列  在新旧策略下的概率比。它直观地反映了：对于旧模型生成的这个回答，我们的新模型是更「喜欢」它了（概率变高），还是更「讨厌」它了（概率变低）。这才是对重要性采样的正确应用。</font>
+ ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756287373435-d0f77326-f607-4b3c-a40c-dfc8a2b91dd0.png)<font style="color:rgb(25, 27, 31);">：代表对序列长度</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756287392981-4b33a8c5-2211-4cdc-8cf1-8c657c1f167c.png)<font style="color:rgb(25, 27, 31);">开方，相当于取</font>**<font style="color:rgb(25, 27, 31);">几何平均值</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">为什么要取几何平均？</font>**

<font style="color:rgb(25, 27, 31);">一个句子的概率是所有词元概率的连乘积。一个长句子的概率会是一个极小的数（比如 10</font><sup><font style="color:rgb(25, 27, 31);">-100</font></sup><font style="color:rgb(25, 27, 31);">）。如果不做处理，长短句的权重会天差地别，导致数值计算极其不稳定。</font>

<font style="color:rgb(25, 27, 31);">取几何平均，就好像把整个句子的「权重增益」平均分配到每个词元上，将重要性权重拉回到一个合理的、可比较的范围（比如 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[0.5, 2.0]</font>`<font style="color:rgb(25, 27, 31);">）。这增强了算法的稳定性和鲁棒性。</font>

:::color5
**<font style="color:#601BDE;">2.梯度对比：GSPO 为何更稳定？</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">我们可以通过对比梯度更新的「指挥信号」来理解两者的差异：</font>

+ **<font style="color:rgb(25, 27, 31);">GRPO 的指挥信号</font>**<font style="color:rgb(25, 27, 31);">：对于一个好回答，它会对里面的每个词说：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">A词，你很重要，给你1.2倍的权重去学习！B词，你一般般，给你0.9倍的权重</font>`<font style="color:rgb(25, 27, 31);">…… 这些权重充满噪声，指令互相矛盾，模型学起来晕头转向。</font>
+ **<font style="color:rgb(25, 27, 31);">GSPO 的指挥信号</font>**<font style="color:rgb(25, 27, 31);">：对于一个好回答，它会先给出一个总体的评价，比如 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">这个回答整体不错，权重是1.1</font>`<font style="color:rgb(25, 27, 31);">，然后对里面的所有词说：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">大家是一个团队，都朝着这个1.1倍权重的方调整</font>`<font style="color:rgb(25, 27, 31);">。</font>

:::color4
**<font style="color:rgb(25, 27, 31);">GRPO（token 级）</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">更关注每个 token 的精细优化，适合需要精准控制生成细节的任务（如机器翻译、代码生成），但可能受异常 token 影响较大。</font>

**<font style="color:rgb(25, 27, 31);">GSPO（sequence 级）</font>**<font style="color:rgb(25, 27, 31);"> 通过句子级平均平滑了 token 级波动，训练更稳定，适合以句子整体质量为导向的任务（如摘要生成、问答），但牺牲了部分 token 级优化精度。所以GSPO 还有一个GSPO-token的版本，是为了去解决多轮对话中一些，特殊token的生成效果问题。</font>

:::

## <font style="color:rgb(25, 27, 31);">四、实验效果</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介：</font>**<font style="color:rgb(25, 27, 31);">Qwen 团队在 MoE 模型（Qwen3-30B-A3B-Base）和复杂的数学、编程任务上对 GSPO 和 GRPO 进行了对比。</font>

:::

:::color5
**<font style="color:#601BDE;">1.发现一：更稳、更快、更强</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756286822640-85cca5f2-8483-4d51-96e8-3411c38706e7.png)

<font style="color:rgb(25, 27, 31);">在相同计算资源下，GSPO 在训练奖励和下游任务性能上，都稳定且持续地优于 GRPO。</font>

:::color5
**<font style="color:#601BDE;">2.发现二：反直觉的「裁剪悖论」</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">PPO 类算法都有一个「裁剪（clipping）」机制，用于丢弃那些与当前模型偏差太大的样本。实验中出现了一个非常反直觉的现象：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1756287761874-c37c202a-af29-4a3d-8b54-587da174470f.png)

<font style="color:rgb(25, 27, 31);">GSPO 裁剪掉的词元比例远高于 GRPO，两者相差近两个数量级。这听起来是不是很奇怪？丢弃了更多的数据，学习效果反而更好？</font>

<font style="color:rgb(25, 27, 31);">可以这样理解：</font>

+ **<font style="color:rgb(25, 27, 31);">GRPO 的策略</font>**<font style="color:rgb(25, 27, 31);">：像一个新手投资者，分析了 1000 个项目，觉得每个都沾点边，于是给每个都投了点钱。结果是，大部分投资的微小收益被少数的巨大亏损所抵消，整体回报率很低。它利用了所有数据，但这些数据充满了噪声。</font>
+ **<font style="color:rgb(25, 27, 31);">GSPO 的策略</font>**<font style="color:rgb(25, 27, 31);">：像一个经验丰富的投资大师，同样分析了 1000 个项目，但它有极其严格的筛选标准（序列级裁剪）。最终，它只挑选了 50 个最优质的项目进行重仓。虽然它「浪费」了研究另外 950 个项目的时间，但这 50 笔高质量的投资带来了惊人的回报。</font>

<font style="color:rgb(25, 27, 31);">GSPO 的成功告诉我们：</font>**<font style="color:rgb(25, 27, 31);">在强化学习中，学习信号的质量远比数量重要。</font>**<font style="color:rgb(25, 27, 31);"> 通过严格的序列级筛选，GSPO 确保了每一次模型更新都来自于「高信噪比」的优质样本，因此学习过程更高效、方向更正确。</font>

:::color5
**<font style="color:#601BDE;">3.发现三：MoE 上的有效性</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">混合专家（MoE）模型是当前大模型发展的前沿方向，它通过稀疏激活部分网络来节省计算，但这也给 RL 训练带来了独特的稳定性挑战。</font>

+ **<font style="color:rgb(25, 27, 31);">MoE 的困境</font>**<font style="color:rgb(25, 27, 31);">：在 MoE 模型中，参数更新后，对于同一个输入，被激活的「专家」网络可能会发生变化。</font>
+ **<font style="color:rgb(25, 27, 31);">GRPO</font>**<font style="color:rgb(25, 27, 31);">：这对于 GRPO 是致命的。它的词元级权重</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的分子和分母可能是由完全不同的子网络计算出来的，比较它们毫无意义，导致权重剧烈波动。为了解决这个问题，研究者们不得不设计复杂的「路由回放（Routing Replay）」策略，增加了系统的复杂度和开销。</font>
+ **<font style="color:rgb(25, 27, 31);">GSPO</font>**<font style="color:rgb(25, 27, 31);">：GSPO 则完全没有这个烦恼。因为它关注的是宏观的、整个序列的概率，这个指标对于底层具体的专家组合变化不那么敏感。就像一家大公司的 CEO，他关心的是公司本季度的总体财报（序列概率），而不是某个具体部门的人员微调（专家路由变化）。</font>

<font style="color:rgb(25, 27, 31);">实验证明，GSPO 无需任何额外技巧，就能稳定地训练 MoE 模型，大大简化了训练流程。</font>

## <font style="color:rgb(25, 27, 31);">五、总结</font>
:::color5
**<font style="color:#601BDE;">1.贡献</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **<font style="color:rgb(25, 27, 31);">理论创新</font>**<font style="color:rgb(25, 27, 31);">：明确指出 GRPO 等算法在词元级重要性采样上的理论缺陷，提出优化单位应与奖励单位（序列）一致，回归重要性采样的正确用法。</font>
+ **<font style="color:rgb(25, 27, 31);">算法提升</font>**<font style="color:rgb(25, 27, 31);">：提出 GSPO 新算法，通过序列级权重计算和裁剪，显著提升训练稳定性、收敛效率和最终性能，并用长度归一化（几何平均）解决不同长度序列的数值稳定问题。</font>
+ **<font style="color:rgb(25, 27, 31);">工程简化</font>**<font style="color:rgb(25, 27, 31);">：彻底解决 MoE 训练不稳定问题，移除对「路由回放」等复杂技巧的依赖，简化 RL 训练流程，并提升对数值精度差异的容忍度，降低工程复杂度。</font>
+ **<font style="color:rgb(25, 27, 31);">实际验证</font>**<font style="color:rgb(25, 27, 31);">：GSPO 已在 Qwen3 等大规模模型中成功应用，展现出工业级的有效性和可靠性。</font>

:::color5
**<font style="color:#601BDE;">2.局限</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **<font style="color:rgb(25, 27, 31);">粗粒度奖励</font>**<font style="color:rgb(25, 27, 31);">：GSPO 只对整个序列赋予单一奖励，无法区分长回复中的优劣部分，可能导致学习效率不高。</font>
+ **<font style="color:rgb(25, 27, 31);">仍然依赖奖励模型</font>**<font style="color:rgb(25, 27, 31);">：性能高度依赖奖励模型的质量，若奖励模型有偏见或缺陷，GSPO 会放大这些问题。</font>
+ **<font style="color:rgb(25, 27, 31);">场景适用性</font>**<font style="color:rgb(25, 27, 31);">：在需要词元级反馈的任务（如代码调试）中，GSPO 的「一刀切」优化方式可能不如细粒度方法。</font>
+ **<font style="color:rgb(25, 27, 31);">实验范围有限</font>**<font style="color:rgb(25, 27, 31);">：目前实验主要集中在数学和编程等推理任务，对开放性、主观性强的领域（如创意写作、情感对话）效果尚需进一步验证。</font>

