# DPO

<!-- source: yuque://zhongxian-iiot9/hlyypb/wvix41y9tas2t76x -->

:::color3
**简介**<font style="color:#1f2329;">：DirectPreferenceOptimization (DPO) 是⼀种新的强化学习算法，特别设计⽤于解决偏好学习</font><font style="color:#1f2329;">（Preference Learning）问题。</font><font style="color:rgb(51, 51, 51);">可视为RLHF的简化变体，省去了</font>**<font style="color:#ED740C;">奖励模型训练环节</font>**<font style="color:rgb(51, 51, 51);">，</font>**<font style="color:#de7802;">核⼼思想是通过优化⽤户或专家给定的偏好信号，⽽⾮直接优化奖励函数</font>**<font style="color:#de7802;">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[https://zhuanlan.zhihu.com/p/27332009509](https://zhuanlan.zhihu.com/p/27332009509)

:::

**核心思想**：<font style="color:rgb(25, 27, 31);">DPO 就像是直接告诉 LLM：“响应 A 比响应 B 更好。多生成像 A 这样的响应，少生成像 B 这样的响应！”它省略了 RL 中用于策略优化的奖励模型这一中间环节</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739169076873-0a688045-7da4-4706-bb72-e2432e14f928.png)

### <font style="color:#1f2329;">原理</font>
:::color5
#### <font style="color:#601BDE;">1.训练步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

1. **<font style="color:rgb(25, 27, 31);">偏好数据仍然是关键</font>**<font style="color:rgb(25, 27, 31);">：与 PPO 一样，DPO 仍然从相同的关键成分开始：人类偏好数据（成对的响应，带有标签，指示哪个响应更受青睐）。人类反馈仍然是基础！</font>
2. **<font style="color:rgb(25, 27, 31);">直接策略更新（分类式损失——直接使用 logits！）</font>**<font style="color:rgb(25, 27, 31);">：这是 DPO 的魔法所在。DPO </font>**<font style="color:#74B602;">使用一个特殊的损失函数直接比较两个模型的 logits</font>**<font style="color:rgb(25, 27, 31);">（概率之前的原始输出分数）：</font>
    - **<font style="color:rgb(25, 27, 31);">当前模型（正在训练中）</font>**<font style="color:rgb(25, 27, 31);">：我们将首选响应（响应 A）和非首选响应（响应 B）都输入到我们正在训练的当前 LLM 中，得到两者的 logits。</font>
    - **<font style="color:rgb(25, 27, 31);">参考模型（旧版本）</font>**<font style="color:rgb(25, 27, 31);">：我们还将响应 A 和响应 B 输入到一个参考模型中。这通常是 LLM 的旧版本（比如我们开始时的 SFT 模型）。我们也会从参考模型中得到 logits。</font>
    - <font style="color:rgb(25, 27, 31);">DPO 的损失函数直接</font>**<font style="color:#74B602;">使用这两个模型的 logits 来计算损失</font>**<font style="color:rgb(25, 27, 31);">，这与分类任务中使用的二元交叉熵损失非常相似。这个损失函数旨在：</font>
        * **<font style="color:rgb(25, 27, 31);">增加首选响应的 logits（和概率）</font>**<font style="color:rgb(25, 27, 31);">：让当前模型在未来更有可能生成像响应 A 这样的响应。</font>
        * **<font style="color:rgb(25, 27, 31);">减少非首选响应的 logits（和概率）</font>**<font style="color:rgb(25, 27, 31);">：让当前模型在未来更不可能生成像响应 B 这样的响应。</font>
        * **<font style="color:rgb(25, 27, 31);">保持接近参考模型（隐式 KL 控制）</font>**<font style="color:rgb(25, 27, 31);">：损失函数还隐式地鼓励当前模型在行为上保持与参考模型的接近（使用参考模型的 logits），这有助于稳定性，类似于 PPO 的 KL 惩罚，但直接嵌入在损失函数中！</font>

:::color5
#### <font style="color:#601BDE;">2.偏好模型建立 Bradley-Terry Model</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(25, 27, 31);">Bradley–Terry model被用于对事物间的比较关系进行建模，比如说棋类比赛，棋手之间往往互有胜负，Bradley–Terry model可以根据这些胜负信息去为所有的职业棋手建模，为他们赋予一个内在的“分数”，通过这个分数可以一定程度上反应棋手的水平，并预测两个棋手之间对局的胜负概率。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741681327077-8e842277-0475-48c3-b7a4-7f17a29a620f.png)

<font style="color:rgb(25, 27, 31);">以上是模型对目标 </font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 的比较（或者胜负）关系的建模， </font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);"> 是 </font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 的内在分数， </font><font style="color:rgb(25, 27, 31);">P(i>j)</font><font style="color:rgb(25, 27, 31);"> 是 </font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);"> 优于 </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 的概率。</font>

**<font style="color:#74B602;">在RLHF场景下，Bradley–Terry model可以用来对人类偏好进行建模。 </font>****<font style="color:#74B602;">β</font>****<font style="color:#74B602;"> 是我们希望Reward Model对于每条样本计算出的模型返回的内在分数，而结果 </font>****<font style="color:#74B602;">P</font>****<font style="color:#74B602;"> 代表了人类偏好的概率</font>**<font style="color:rgb(25, 27, 31);">。在实际当中，我们会收集到标注员对样本间两两比较的结果，我们会使用</font>**<font style="color:#74B602;">最大似然估计 Maximum likelihood estimation</font>**<font style="color:rgb(25, 27, 31);">去优化Reward Model，使RM得到的分数对样本间比较结果的预测最大程度上和训练数据保持一致。</font>

:::color5
#### <font style="color:#601BDE;">3.偏好比较</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">为了优化偏好模型，DPO ⾸先需要定义偏好的⽐较⽅式。在给定⼀对动作 </font><font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">i</font>_</sub><font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">j </font>_</sub><font style="color:#1f2329;">)</font><font style="color:#1f2329;">和状态</font>_<font style="color:#1f2329;">s </font>_<font style="color:#1f2329;">的情况   下，模型需要判断哪个动作更被偏好。这可以通过定义⼀个偏好⽐较函数</font>_<font style="color:#1f2329;">P</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">i </font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">≻ </font>_<font style="color:#1f2329;">a</font>_<sub>_<font style="color:#1f2329;">j</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">，</font>**<font style="color:#d83931;">即在状态</font>**_**<font style="color:#1f2329;">s </font>**_**<font style="color:#d83931;">下，动作</font>**_**<font style="color:#1f2329;">a</font>**_<sub>_**<font style="color:#1f2329;">i</font>**_</sub>_**<font style="color:#1f2329;"> </font>**_**<font style="color:#d83931;">相较于</font>**_**<font style="color:#1f2329;">a</font>**_<sub>_**<font style="color:#1f2329;">j</font>**_</sub>_**<font style="color:#1f2329;"> </font>**_**<font style="color:#d83931;">更被偏好的概率</font>**<font style="color:#1f2329;">。该概率可以通过偏好模型计算得到：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739167079623-7b923bea-d6d2-41bd-b5cd-2bc7f2d26bc3.png)

<font style="color:#1f2329;">这个公式是通过 softmax 函数得出的，表⽰在两个动作之间，哪个更有可能被偏好。</font>

:::color5
#### <font style="color:#601BDE;">4.损失函数</font>
:::

<font style="color:#1f2329;">为了训练偏好模型，DPO 使⽤了基于</font>**<font style="color:#ED740C;">⼆元交叉熵的损失函数</font>**<font style="color:#1f2329;">。这⼀损失函数旨在最⼩化模型预测偏好与实际⽤⼾（或专家）偏好之间的差异。</font>

<font style="color:rgb(25, 27, 31);">可以这样理解：</font>**<font style="color:#74B602;">DPO 的损失函数就像一个“偏好指南针”，直接根据首选和非首选响应的相对 logits 指导 LLM 的权重，而无需显式预测奖励。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739170478873-a3f6923e-acf8-45dd-85e0-a0b715ca4620.png)

<font style="color:#1f2329;">这个损失函数的⽬的是使模型对</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">+和</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">− 的评分差尽可能⼤，从⽽确保模型更倾向于选择</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">+作为偏好选项。</font>**<font style="color:#2ea121;background-color:#f0fbef;">通过最⼩化这个损失函数，偏好模型会不断调整其参数，使得预测出的偏好分布越来越接近真实的⽤户偏好分布。</font>**

:::color5
#### <font style="color:#601BDE;">5.策略优化</font>
:::

<font style="color:#1f2329;">通过学习到的偏好模型</font>_<font style="color:#1f2329;">P</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">，我们可以将其⽤于⽣成策略</font>_<font style="color:#1f2329;">π</font>_<sub>_<font style="color:#1f2329;">θ</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">。DPO 的策略优化过程直接依赖 于偏好模型，即策略的概率分布可以通过偏好模型的 softmax 输出进⾏参数化：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739167383799-dd59e4e2-551d-4979-8634-8ec0ad621766.png)

<font style="color:#1f2329;">这意味着 DPO 的策略优化并不依赖于传统的奖励信号，⽽是完全基于偏好信号进⾏优化。通过优化偏好损失函数，我们可以间接优化策略的性能，使其更符合⽤户的期望。</font>

:::color5
#### <font style="color:#601BDE;">6.优缺点</font>
:::

**<font style="color:rgb(13, 18, 57);">优点</font>**

1. **<font style="color:rgb(13, 18, 57);">高效性</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">绕过奖励建模</font>**<font style="color:rgb(13, 18, 57);">：DPO无需显式训练奖励模型（Reward Model），直接通过偏好数据优化策略，减少了训练流程的复杂性。</font>
    - **<font style="color:rgb(13, 18, 57);">计算成本低</font>**<font style="color:rgb(13, 18, 57);">：传统RLHF需要交替优化奖励模型和策略（如PPO），而DPO通过闭式解直接优化目标函数，降低了计算开销。</font>
2. **<font style="color:rgb(13, 18, 57);">稳定性</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">避免强化学习的不稳定性</font>**<font style="color:rgb(13, 18, 57);">：PPO等算法需要精细的超参数调优，而DPO基于监督学习框架，训练过程更稳定，不易出现策略崩溃（policy collapse）。</font>
3. **<font style="color:rgb(13, 18, 57);">实现简单</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">代码复杂度低</font>**<font style="color:rgb(13, 18, 57);">：仅需对损失函数进行梯度优化（类似分类任务），无需实现复杂的强化学习逻辑（如价值函数、重要性采样等）。</font>

**<font style="color:rgb(13, 18, 57);">缺点</font>**

1. **<font style="color:rgb(13, 18, 57);">对偏好数据的强依赖</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">数据质量敏感</font>**<font style="color:rgb(13, 18, 57);">：DPO直接依赖成对偏好数据（如正/负样本对），若数据存在噪声或偏见，模型可能继承这些缺陷。</font>
    - **<font style="color:rgb(13, 18, 57);">数据量需求</font>**<font style="color:rgb(13, 18, 57);">：需要大量高质量的偏好标注数据，成本较高，且可能受限于标注者的主观偏好。</font>
2. **<font style="color:rgb(13, 18, 57);">理论假设限制</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">基于Bradley-Terry模型</font>**<font style="color:rgb(13, 18, 57);">：假设人类偏好仅由两个选项的奖励差值决定，无法建模更复杂的偏好关系（如多选项排序或上下文相关偏好）。</font>
    - **<font style="color:rgb(13, 18, 57);">无法处理非对称偏好</font>**<font style="color:rgb(13, 18, 57);">：例如，若用户更喜欢“短回答”但标注者更关注“准确性”，DPO可能难以平衡两者。</font>
3. **<font style="color:rgb(13, 18, 57);">对参考模型的依赖</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">参考模型的质量影响结果</font>**<font style="color:rgb(13, 18, 57);">：DPO的损失函数基于参考模型（通常为初始SFT模型）的输出分布，若参考模型性能较差，可能限制最终模型的表现。</font>
4. **<font style="color:rgb(13, 18, 57);">扩展性挑战</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">大规模数据效率</font>**<font style="color:rgb(13, 18, 57);">：当偏好数据规模极大时，DPO的计算效率可能下降，而传统RLHF通过预训练奖励模型可部分缓解这一问题。</font>

:::color5
#### <font style="color:#601BDE;">6.代码实现</font>
:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def dpo_loss(policy_logits_preferred, policy_logits_dispreferred, ref_logits_preferred, ref_logits_dispreferred, beta_kl):
    """概念性 DPO 损失函数（简化版——直接使用 logits）。"""

    # 1. 从 logits 中获取对数概率（当前和参考模型的首选和非首选响应）
    policy_logprob_preferred = F.log_softmax(policy_logits_preferred, dim=-1).gather(...)  # 提取首选响应中实际标记的对数概率
    policy_logprob_dispreferred = F.log_softmax(policy_logits_dispreferred, dim=-1).gather(...)  # 提取非首选响应中实际标记的对数概率
    ref_policy_logprob_preferred = F.log_softmax(ref_logits_preferred, dim=-1).gather(...)  # 同样适用于参考模型
    ref_policy_logprob_dispreferred = F.log_softmax(ref_logits_dispreferred, dim=-1).gather(...)

    # 2. 计算对数比率（使用对数概率——如前所述）
    log_ratio = policy_logprob_preferred - policy_logprob_dispreferred - (ref_policy_logprob_preferred - ref_policy_logprob_dispreferred)

    # 3. 偏好概率（Bradley-Terry 模型——隐式奖励信号）
    preference_prob = 1 / (1 + np.exp(-beta_kl * log_ratio))

    # 4. 二元交叉熵损失（直接优化策略）
    dpo_loss = -np.log(preference_prob + 1e-8)
    return dpo_loss
```

### <font style="color:#1f2329;">偏好学习与传统强化学习区别</font>
<font style="color:#1f2329;">传统的强化学习通过最⼤化累积奖励来训练策略</font>

:::color3
<font style="color:#1f2329;">然⽽</font>**<font style="color:#d83931;">在 DPO 中，⽬标是最⼤化偏好模型的准确性，⽽不是累积奖励</font>**<font style="color:#d83931;">。</font><font style="color:#1f2329;">因此，DPO 并不直接依赖环境   提供的奖励信号，⽽是通过优化偏好⽐较损失函数</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;">来训练策略。这种优化过程更符合⼈类偏好的决策⽅式。</font>

:::

### <font style="color:#1f2329;">扩展与优化</font>
<font style="color:#1f2329;">为了提⾼DPO 的效率和稳定性，常见的优化技术包括：</font>

1. **<font style="color:#117CEE;">偏好采样策略</font>**<font style="color:#1f2329;">：通过经验回放池采样不同的偏好⽐较对，确保训练样本的多样性。</font>
2. **<font style="color:#117CEE;">策略约束</font>**<font style="color:#1f2329;">：类似于 PPO（Proximal Policy Optimization）中的剪切策略，通过限制每次策略更新的</font>

<font style="color:#1f2329;">幅度来避免过度更新，保证训练的稳定性。</font>

### <font style="color:#1f2329;">DPO与PPO/RLHF的对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**传统 RLHF 流程:  **

人类偏好数据 → 训练 Reward Model → PPO 优化策略 → 最终策略

**DPO 流程:  **

人类偏好数据 → 直接优化策略（隐式定义奖励） → 最终策略

:::

:::color5
#### <font style="color:#601BDE;">1.PPO/RLHF步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

1. **<font style="color:rgb(25, 27, 31);">训练 </font>**[**<font style="color:rgb(9, 64, 142);">reward model</font>**](https://zhida.zhihu.com/search?content_id=237414431&content_type=Article&match_order=1&q=reward+model&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：训练数据是同一个 prompt 的 2 个回答，让人或 </font>[<font style="color:rgb(9, 64, 142);">GPT4</font>](https://zhida.zhihu.com/search?content_id=237414431&content_type=Article&match_order=1&q=GPT4&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 标注哪个回答更好，reward model 会去优化如下的 loss：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741676118461-abbf8b53-017a-4e99-9fdb-44853020d533.png)**     （1）**

<font style="color:rgb(25, 27, 31);">其中 </font><font style="color:rgb(25, 27, 31);">r</font><sub><font style="color:rgb(25, 27, 31);">ϕ</font></sub><font style="color:rgb(25, 27, 31);"> 就是 reward model 用来给回答打分。</font><font style="color:rgb(25, 27, 31);">D</font><font style="color:rgb(25, 27, 31);"> 是训练数据集，</font><font style="color:rgb(25, 27, 31);">x</font><font style="color:rgb(25, 27, 31);"> 是 prompt，</font><font style="color:rgb(25, 27, 31);">y</font><sub><font style="color:rgb(25, 27, 31);">win</font></sub><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">y</font><sub><font style="color:rgb(25, 27, 31);">lose</font></sub><font style="color:rgb(25, 27, 31);"> 分别是好的回答和不好的回答。也就是说，要尽可能</font>**<font style="color:#74B602;">让好的回答的得分比不好的回答高</font>**<font style="color:rgb(25, 27, 31);">，拉大他们之间的差别。</font>

2. <font style="color:rgb(25, 27, 31);">第二步是用 RL 算法来提升模型的得分。使用的 loss 是：</font>

      ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741676192460-51bb0326-cdfc-48a0-b364-02a8629bf0d2.png)**（2）**  
<font style="color:rgb(25, 27, 31);">其中 </font><font style="color:rgb(25, 27, 31);">π</font><sub><font style="color:rgb(25, 27, 31);">θ</font></sub><font style="color:rgb(25, 27, 31);"> 是我们在训练的 LLM，</font><font style="color:rgb(25, 27, 31);">π</font><sub><font style="color:rgb(25, 27, 31);">ref</font></sub><sub><font style="color:rgb(25, 27, 31);"> </font></sub><font style="color:rgb(25, 27, 31);">是训练的初始值。</font>**<font style="color:#74B602;">这个 loss （偏好loss + KL散度loss）意思是希望 LLM 输出的回答的评分能尽可能高，同时 </font>****<font style="color:#74B602;">π</font>**<sub>**<font style="color:#74B602;">θ</font>**</sub>**<font style="color:#74B602;"> 不要偏离 </font>****<font style="color:#74B602;">π</font>**<sub>**<font style="color:#74B602;">ref</font>**</sub><sub>**<font style="color:#74B602;"> </font>**</sub>**<font style="color:#74B602;">太多，保证它还能正常做回答</font>**<font style="color:rgb(25, 27, 31);">，不要训成一个评分很高但是回答乱码的东西。</font>

:::color5
#### <font style="color:#601BDE;">2.DPO步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:rgb(25, 27, 31);">DPO 的作者们意识到，上述公式（2）是有显式解的。DPO 通过公式转换</font>**<font style="color:#ED740C;">把 RLHF 无损地转化为了 SFT</font>**<font style="color:rgb(25, 27, 31);">，在训练的时候</font>**<font style="color:#ED740C;">不再需要同时跑 4 个模型（reward model, ref model, critic, actor），而是只用跑 actor 和 ref 2 个模型</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
#### <font style="color:#601BDE;">3.目标和应用场景对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ <font style="color:#1f2329;">PPO是⼀种⽤于强化学习的</font><font style="color:#d83931;">策略优化算法</font><font style="color:#1f2329;">。其⽬的是通过与环境交互，</font><font style="color:#d83931;">在累计⻓期奖励的基础上优化策略</font><font style="color:#1f2329;">。PPO主要⽤于训练智能体如何通过连续的动作获得最⼤的累计奖励。</font>
+ <font style="color:#1f2329;">DPO是⼀种</font><font style="color:#245bdb;">偏好优化算法</font><font style="color:#1f2329;">，主要⽤于偏好学习任务（如⼤模型的偏好微调）。</font><font style="color:#245bdb;">它的⽬标是通过直接从⼈类偏好数据中优化策略，使得输出更加符合⽤户偏好</font><font style="color:#1f2329;">，⽽不是通过显式的奖励模型进⾏优化。</font>

:::color5
#### <font style="color:#601BDE;">4.优化目标对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ <font style="color:#d83931;">PPO通过限制策略更新的幅度，来保证策略的稳定性，避免策略发⽣过⼤的变化。其⽬标函数通过引⼊⼀个剪辑函数来实现这⼀点。</font><font style="color:#1f2329;"></font>
+ <font style="color:#245bdb;">DPO跳过了显式奖励模型的训练过程，直接从偏好数据中优化策略。</font><font style="color:#1f2329;">它的⽬标函数是最⼤化偏好分布下的对数似然</font>

:::color5
#### <font style="color:#601BDE;">5.应用任务对比</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ <u><font style="color:#d83931;">PPO 适⽤于典型的强化学习任务</font></u><font style="color:#1f2329;">，如在游戏环境中训练智能体、机器⼈控制等。PPO算法通常在  奖励信号稀疏的情况下表现出⾊，通过不断交互  和调整策略，逐步提⾼累计奖励。</font>
+ <u><font style="color:#245bdb;">DPO 更适⽤于偏好学习任务</font></u><font style="color:#1f2329;">，如在⼤型语⾔模型上进⾏⼈类偏好微调。它不需要通过环境交互来  优化，⽽是通过⼈类提供的偏好数据直接优化⽣  成模型的输出。相⽐于PPO的强化学习场景，</font>

<font style="color:#1f2329;">DPO避免了复杂的奖励模型构建。</font>

| **<font style="color:rgb(51, 51, 51);">维度</font>** | **<font style="color:rgb(51, 51, 51);">PPO + Reward Model</font>** | **<font style="color:rgb(51, 51, 51);">DPO</font>** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">是否需要 Reward Model</font>** | <font style="color:rgb(51, 51, 51);">是（显式训练）</font> | <font style="color:rgb(51, 51, 51);">否（隐式通过偏好数据定义奖励）</font> |
| **<font style="color:rgb(51, 51, 51);">优化目标</font>** | <font style="color:rgb(51, 51, 51);">最大化 Reward Model 的预测奖励</font> | <font style="color:rgb(51, 51, 51);">直接最大化人类偏好的似然</font> |
| **<font style="color:rgb(51, 51, 51);">计算复杂度</font>** | <font style="color:rgb(51, 51, 51);">高（需策略采样、奖励模型推理、PPO 更新）</font> | <font style="color:rgb(51, 51, 51);">低（类似监督学习，单阶段优化）</font> |
| **<font style="color:rgb(51, 51, 51);">潜在问题</font>** | <font style="color:rgb(51, 51, 51);">Reward Hacking（策略利用奖励模型漏洞）</font> | <font style="color:rgb(51, 51, 51);">依赖偏好数据的质量和覆盖度</font> |
| **<font style="color:#1f2329;">⽬标函数</font>** | <font style="color:#1f2329;">最⼤化⻓期奖励</font><font style="color:#1f2329;">，加⼊</font><font style="color:#1f2329;">KL</font><font style="color:#1f2329;">约</font><font style="color:#1f2329;">束和剪裁机制</font> | <font style="color:#1f2329;">最⼤化⼈类偏好</font><font style="color:#1f2329;">，直接优化策</font><font style="color:#1f2329;">略不需要显式奖励模型</font> |
| **<font style="color:#1f2329;">适⽤场景</font>** | <font style="color:#1f2329;">强化学习</font><font style="color:#1f2329;">，智能体交互场景</font> | <font style="color:#1f2329;">偏好学习</font><font style="color:#1f2329;">，语⾔模型微调等</font> |
| **<font style="color:#1f2329;">策略更新⽅式</font>** | <font style="color:#1f2329;">基于剪裁的策略⽐率更新</font> | <font style="color:#1f2329;">基于</font><font style="color:#1f2329;">KL</font><font style="color:#1f2329;">散度和⼈类偏好直接</font><font style="color:#1f2329;">调整策略</font> |
| **<font style="color:#1f2329;">优化⽅法</font>** | <font style="color:#1f2329;">通过策略梯度法更新</font> | <font style="color:#1f2329;">通过对数似然优化偏好数据下</font><font style="color:#1f2329;">的策略</font> |


### <font style="color:#1f2329;">DPO实践：LLM中偏好数据收集与正负样本构建</font>
:::color5
#### <font style="color:#601BDE;">1.数据收集</font>
:::

<font style="color:#1f2329;">我们可以通过以下步骤来收集偏好数据：</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">模型⽣成候选对话回复：给定⼀个⽤⼾输⼊（如⽤⼾问题或聊天对话），⽣成模型会给出多种候选回复。假设⽤⼾输⼊是：</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⽤⼾输⼊：</font><font style="color:#1f2329;">“</font><font style="color:#1f2329;">天⽓怎么样？</font><font style="color:#1f2329;">”</font>

<font style="color:#1456f0;">◦</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">模型⽣成的两条回复分别为：</font>

<font style="color:#1456f0;">i.</font><font style="color:#1456f0;">   </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">1</font><font style="color:#1f2329;">：“</font><font style="color:#1f2329;">今天的天⽓⾮常好</font><font style="color:#1f2329;">，晴朗⽆云。</font><font style="color:#1f2329;">”</font>

<font style="color:#1456f0;">ii.</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">2</font><font style="color:#1f2329;">：</font><font style="color:#1f2329;">“</font><font style="color:#1f2329;">不清楚天⽓</font><font style="color:#1f2329;">，您可以查⼀下天⽓预报。</font><font style="color:#1f2329;">”</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">⼈类反馈：接下来，系统会展⽰这两条回复给⼈类评审员。评审员基于回复的⾃然性、相关性、信息量等⽅⾯，选择其中更符合⽤⼾需求的回复。例如，评审员选择了回复1，因为它更加具体且回  答了⽤⼾的问题。</font>

:::color5
#### <font style="color:#601BDE;">2.偏好数据生成</font>
:::

<font style="color:#1f2329;">根据⼈类评审员的选择，我们得到如下的偏好数据：</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">回复1 ≻ 回复2 ，即回复1被评为更优</font>

:::color5
#### <font style="color:#601BDE;">3.构造正负样本</font>
:::

<font style="color:#1f2329;">根据评审员的反馈，构造正负样本：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">正样本：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">1</font><font style="color:#1f2329;">作为正样本</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，因为它更符合⽤⼾的偏好。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">负样本：</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">回复</font><font style="color:#1f2329;">2</font><font style="color:#1f2329;">作为负样本</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，因为它被评为相对较差的回复。</font>

<font style="color:#1f2329;">这对正负样本可以⽤于DPO的训练，其中模型将被优化为更倾向于⽣成类似回复1的答案，⽽抑制⽣成回复2这样的回答。</font>

:::color5
#### <font style="color:#601BDE;">4.多轮对话扩展</font>
:::

<font style="color:#1f2329;">在多轮对话系统中，⽤⼾不仅对单个回复进⾏评估，还可以对⼀段完整的对话进⾏反馈。此时，系统可以根据⽤户与模型交互过程中整段对话的质量进⾏偏好标注。</font>

<font style="color:#2ea121;">例如，⽤户对整个对话中的某⼀轮次的回复给予正向反馈（如点赞或正⾯评价），那么该轮次中的回复可以作为正样本，其他候选可以作为负样本。</font>

:::color5
#### <font style="color:#601BDE;">5.使用反馈模型优化</font>
:::

<font style="color:#1f2329;">通过收集⼤量类似的偏好数据，模型能够不断改进⽣成的质量。在DPO的框架下，模型通过最⼤化偏好模型对正负样本的预测准确率，逐步优化输出结果，使其更符合⼈类偏好。</font>

```python
import tensorflow as tf
import gym
import numpy as np

class DPO:
    def __init__(self, env, hidden_size=64, batch_size=64, discount_rate=0.99, learning_rate=1e-4):
        self.env = env
        self.batch_size = batch_size
        self.gamma = discount_rate

        # 初始化策略网络
        self.policy = self.build_policy(hidden_size)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate)

    def build_policy(self, hidden_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_size, activation='relu'),
            tf.keras.layers.Dense(self.env.action_space.n, activation='softmax')
        ])
        return model

    def get_action(self, state):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        action_probs = self.policy(state)
        action = tf.random.categorical(tf.math.log(action_probs), 1)
        return action.numpy()[0]

    def compute_loss(self, states, actions, rewards, next_states, dones):
        # 计算当前策略的概率
        old_p = self.policy(tf.convert_to_tensor(states, dtype=tf.float32))
        old_p = tf.gather(old_p, actions, batch_dims=1)
        old_p = tf.stop_gradient(old_p)

        new_p = self.policy(tf.convert_to_tensor(states, dtype=tf.float32))
        new_p = tf.gather(new_p, actions, batch_dims=1)

        # 计算优势 (可以使用更复杂的基线估计)
        V = self.value(tf.convert_to_tensor(states, dtype=tf.float32))  # 假设self.value是已有的价值函数
        next_V = self.value(tf.convert_to_tensor(next_states, dtype=tf.float32))
        advantages = rewards + self.gamma * next_V - V

        # 损失函数
        ratio = tf.exp(tf.math.log(new_p + 1e-10) - tf.math.log(old_p + 1e-10))
        loss = -tf.reduce_mean(tf.minimum(ratio * advantages, 1.0 * advantages))

        return loss

    def train(self, num_episodes=1000, max_steps=2000):
        for episode in range(num_episodes):
            trajectories = []
            state = self.env.reset()
            episode_reward = 0
            for step in range(max_steps):
                action = self.get_action(state)
                next_state, reward, done, _ = self.env.step(self.env.actions[action])
                trajectories.append((state, action, reward, next_state, done))
                episode_reward += reward
                state = next_state
                if done:
                    break

            # 转换为张量
            states = tf.convert_to_tensor([t[0] for t in trajectories], dtype=tf.float32)
            actions = tf.convert_to_tensor([t[1] for t in trajectories], dtype=tf.int32)
            rewards = tf.convert_to_tensor([t[2] for t in trajectories], dtype=tf.float32)
            next_states = tf.convert_to_tensor([t[3] for t in trajectories], dtype=tf.float32)
            dones = tf.convert_to_tensor([t[4] for t in trajectories], dtype=tf.float32)

            # 计算损失
            with tf.GradientTape() as tape:
                loss = self.compute_loss(states, actions, rewards, next_states, dones)

            gradients = tape.gradient(loss, self.policy.trainable_weights)
            self.optimizer.apply_gradients(zip(gradients, self.policy.trainable_weights))

            print(f"Episode {episode}, Reward: {episode_reward}")

        print("Training completed.")

```



### <font style="color:#601bde;">DPO在智能客服中的应用</font>
#### **显著提升回复的“有用性”与“安全性” (Helpfulness & Safety)**
智能客服最核心的指标是解决率和合规性。

+ 减少幻觉（Hallucination）： 客服场景严禁胡编乱造。DPO 通过学习正负样本对（Positive/Negative Pairs），能让模型明确知道“什么是不该说的”。例如，当模型面对不知道的问题时，RLHF 可能会为了获得高奖励而编造答案，而 DPO 可以直接通过负样本惩罚这种行为，教会模型在不确定时诚实地回答“我不清楚”或转人工。
+ 对齐业务规范： 客服通常有严格的话术规范（SOP）。通过构建（符合SOP的回答 vs 不符合SOP的回答）的数据对，DPO 能强力约束模型遵循特定的语气、格式和业务逻辑。

#### **优化回复的语气与共情能力 (Tone & Empathy)**
在处理客诉或安抚用户情绪时，语气至关重要。

+ 风格对齐： 传统的 SFT（监督微调）只能教会模型“说什么”，很难教会“怎么说”。DPO 可以通过偏好数据，让模型通过对比学习，掌握更具亲和力、更专业或更具同理心的表达方式。
    - 例子：
        * 负样本： “你的包裹丢了，去联系快递公司。”（冷漠、推诿）
        * 正样本： “非常抱歉听到这个消息，我理解您现在的焦急。请您放心，我会立即帮您联系快递公司核实情况。”（共情、主动解决）
    - DPO 能有效拉大这两个回答在概率空间上的距离，使模型倾向于生成后者。

#### **解决“重复生成”与“废话文学” (Repetition & Verbosity)**
大模型在长文本生成时容易出现车轱辘话或过度客套。

+ 拒绝冗余： 在 DPO 数据集中，可以将“啰嗦、重复”的回答标记为负样本，将“简洁、切中要害”的回答标记为正样本。这能有效抑制模型生成那种看似礼貌实则无用的“废话文学”，提高沟通效率，降低用户的阅读成本。

#### **训练稳定性与效率的提升 (Stability & Efficiency)**
这虽然是工程层面的优化，但直接影响到客服系统的迭代速度。

+ 无需训练奖励模型（Reward Model）： 传统的 RLHF 需要先训练一个 Reward Model，再用 PPO 算法进行强化学习，过程复杂、超参数多且极不稳定。DPO 将强化学习问题转化为一个分类损失函数问题，直接在偏好数据上优化策略。
+ 迭代周期缩短： 对于客服系统，业务规则变化很快（如双十一活动规则）。DPO 的训练速度快、显存占用低，使得我们能够快速响应业务变更，通过少量新数据迅速微调模型上线。

