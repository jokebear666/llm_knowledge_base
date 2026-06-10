# GRPO

<!-- source: yuque://zhongxian-iiot9/hlyypb/ee6r13rktcl3w53t -->

## <font style="color:#000000;">GRPO（G</font><font style="color:rgb(64, 64, 64);">roup Relative Policy Optimization</font>**<font style="color:rgb(25, 27, 31);">）</font>**
:::color3
**简介****<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(64, 64, 64);">在DeepSeek-R1模型中，使用到的强化学习算法GRPO其实是DeepSeek之前的文章</font>_**<font style="color:rgb(64, 64, 64);">《DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models》</font>**_

<font style="color:rgb(64, 64, 64);">在目前大语言模型中进行微调的流程中，一般在SFT阶段之后，进一步通过强化学习对模型进行优化可以显著提升其性能。而</font>**<font style="color:rgb(64, 64, 64);">Group Relative Policy Optimization (GRPO)，就是使用在该阶段，替换传统的PPO算法。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**参考资料**：[DeepSeek的GRPO算法是什么？](https://www.zhihu.com/question/10766825126/answer/88583863333)

**源码实现**：[https://github.com/huggingface/open-r1/blob/main/src/open_r1/rewards.py](https://github.com/huggingface/open-r1/blob/main/src/open_r1/rewards.py)

**代码实现：**[GRPO核心代码实践](https://zhuanlan.zhihu.com/p/23349133287)

:::

**<font style="color:rgb(25, 27, 31);">GRPO 是一种在线学习算法（online learning algorithm），这意味着它通过使用训练过程中由训练模型自身生成的数据来迭代改进。GRPO 的目标直觉是最大化生成补全（completions）的优势函数（advantage），同时确保模型保持在参考策略（reference policy）附近。</font>**

<font style="color:rgb(25, 27, 31);">GRPO 就像是 PPO 的精简版。</font>**<font style="color:#74B602;">它保留了 PPO 的核心思想，但去掉了独立的价值函数（辅助教练），使其更轻量、更快速。</font>**

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1765884045150-71a5a958-2a2a-4fec-b53f-140f3259f672.tif?x-oss-process=image/format,png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">重要性采样是GRPO的核心机制：通过复用旧策略的样本，用重要性权重</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318225466-daf74867-a20b-48f4-aeb3-d16b300241be.png)<font style="color:rgb(25, 27, 31);">调整新策略的优化方向。</font>
2. <font style="color:rgb(25, 27, 31);">优势函数的作用：标准化后的奖励 </font><font style="color:rgb(25, 27, 31);">Ai</font><font style="color:rgb(25, 27, 31);"> 帮助策略区分高价值样本和低价值样本，引导模型优先提升高奖励输出的概率。</font>
3. <font style="color:rgb(25, 27, 31);">GRPO的工程优势：省去Critic价值模型，仅依赖组内奖励统计量，适合资源受限的场景。</font>

:::color5
**<font style="color:#601BDE;">2.与DPO/PPO的区别</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **<font style="color:rgb(25, 27, 31);">特性</font>** | **<font style="color:rgb(25, 27, 31);">PPO</font>** | **<font style="color:rgb(25, 27, 31);">DPO</font>** | **<font style="color:rgb(25, 27, 31);">GRPO</font>** |
| :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">是否需要奖励模型</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">是</font> |
| <font style="color:rgb(25, 27, 31);">是否需要辅助教练（价值函数）</font> | <font style="color:rgb(25, 27, 31);">是</font> | <font style="color:rgb(25, 27, 31);">否</font> | <font style="color:rgb(25, 27, 31);">否</font> |
| <font style="color:rgb(25, 27, 31);">训练效率</font> | <font style="color:rgb(25, 27, 31);">中等</font> | <font style="color:rgb(25, 27, 31);">高</font> | <font style="color:rgb(25, 27, 31);">高</font> |
| <font style="color:rgb(25, 27, 31);">适用场景</font> | <font style="color:rgb(25, 27, 31);">通用</font> | <font style="color:rgb(25, 27, 31);">简单任务</font> | <font style="color:rgb(25, 27, 31);">复杂推理任务</font> |


**<font style="color:#74B602;">为了解决PPO的缺点</font>**<font style="color:rgb(64, 64, 64);">，我们提出了 </font>**<font style="color:rgb(64, 64, 64);">Group Relative Policy Optimization (GRPO)</font>**<font style="color:rgb(64, 64, 64);">，不再需要像PPO那样加入额外的价值函数近似</font>_**<font style="color:rgb(64, 64, 64);">，而是直接使用多个采样输出的平均奖励作为Baseline</font>**_<font style="color:rgb(64, 64, 64);">，显著减少了训练资源的使用。</font>

**<font style="color:rgb(64, 64, 64);">GRPO与PPO的关联与区别：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812555603-dbee0aac-d740-44a1-9f32-60f3ef699f3a.png)

1. <font style="color:rgb(25, 27, 31);">PPO通常依赖一个独立的价值模型（Critic）来估计优势 </font><font style="color:rgb(25, 27, 31);">Ai</font><font style="color:rgb(25, 27, 31);">，需要额外训练一个模型。</font>
2. <font style="color:rgb(25, 27, 31);">GRPO的创新点：直接使用组内样本的奖励计算基线（如 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741318126920-e319b774-623c-4c5c-9e45-829567f9719b.png)<font style="color:rgb(25, 27, 31);">），无需Critic模型，降低了计算成本。</font>
3. **<font style="color:rgb(25, 27, 31);">GRPO 直接比较候选响应的群体，无需额外的批评者模型</font>**<font style="color:rgb(25, 27, 31);">。对于给定的问题 q，GRPO 首先从当前策略 πθold 生成 G 个不同的响应 {o1, o2, ..., oG}。然后 GRPO 根据这些响应采取行动，并将获得的奖励表示为 {r1, r2, ..., rG}。通过计算它们的均值和标准差进行归一化，GRPO 确定这些响应的相对质量：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335086191-20af6668-2361-421b-a820-49700da58c3c.png)

<font style="color:rgb(25, 27, 31);">其中 Ai 表示第 i 个答案的相对质量。</font>**<font style="color:#ED740C;">GRPO 鼓励模型偏好群体内奖励值较高的更好答案</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.训练步骤（简化版）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">生成一组响应</font>**<font style="color:rgb(25, 27, 31);">：对于每个提示，从 LLM 中生成多个响应的一组。</font>
2. **<font style="color:rgb(25, 27, 31);">对组进行打分（奖励模型）</font>**<font style="color:rgb(25, 27, 31);">：获取组内所有响应的奖励分数。</font>
3. **<font style="color:rgb(25, 27, 31);">计算组内相对优势（GRAE，基于组的优势骨架）</font>**<font style="color:rgb(25, 27, 31);">：通过比较每个响应的奖励与组内平均奖励来计算优势。在组内对奖励进行归一化以得到优势。</font>
    1. <font style="color:rgb(25, 27, 31);">GRPO 的魔法成分在于它如何估计优势。</font>**<font style="color:#74B602;">它不是使用辅助教练，而是使用一组由 LLM 生成的相同提示的响应来估计每个响应相对于组内其他响应的“好坏”</font>**<font style="color:rgb(25, 27, 31);">。</font>
4. **<font style="color:rgb(25, 27, 31);">优化策略（使用 GRAE 的 PPO 风格目标函数）</font>**<font style="color:rgb(25, 27, 31);">：使用一个 PPO 风格的目标函数更新 LLM 的策略，但使用这些组内相对优势。</font>

:::color5
**<font style="color:#601BDE;">4.实现步骤</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

为了理解 GRPO 的工作原理，可以将其分解为四个主要步骤：

1. ** 生成补全（Generating completions）**

<font style="color:rgb(25, 27, 31);">在每一个训练步骤中，我们从提示（prompts）中采样一个批次（batch），并为每个提示生成一组 G 个补全（completions）（记为 o</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><font style="color:rgb(25, 27, 31);">）。</font>

2. ** 计算优势值（Computing the advantage）**

<font style="color:rgb(25, 27, 31);">对于每一个 G 序列，使用奖励模型（reward model）计算其奖励（reward）。为了与奖励模型的比较性质保持一致。通常奖励模型是基于同一问题的输出之间的比较数据集进行训练的。优势的计算反映了这些相对比较。其归一化公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327572180-c8af0f92-d170-4f1f-8c7a-4e9f796b8734.png)

<font style="color:rgb(25, 27, 31);">这种方法赋予了该方法其名称：</font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（Group Relative Policy Optimization, GRPO）</font>**

GRPO通过优化PPO算法，解决了**<font style="color:#74B602;">计算优势值时需要同时依赖奖励模型（reward model）和价值模型（value model）的问题，成功移除了value model（价值模型）</font>**，**<font style="color:#ED740C;">显著降低了推理时的内存占用和时间开销</font>**。**<font style="color:#ED740C;">Advantage（优势值）的核心价值在于为模型输出提供更精准的评估</font>**，不仅衡量答案的绝对质量，还通过相对比较（与其他回答的对比）来更全面地定位其优劣。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738812555603-dbee0aac-d740-44a1-9f32-60f3ef699f3a.png)

3. ** 估计KL散度（Estimating the KL divergence）**

在实际算法实现中，直接计算KL散度可能会面临一些挑战：

+ **计算复杂度高**：KL散度的定义涉及对两个概率分布的对数比值的期望计算。对于复杂的策略分布，直接计算KL散度可能需要大量的计算资源；
+ **数值稳定性**：在实际计算中，直接计算KL散度可能会遇到数值不稳定的问题，尤其是当两个策略的概率分布非常接近时，对数比值可能会趋近于零或无穷大。近似器可以通过引入一些数值稳定性的技巧（如截断或平滑）来避免这些问题；
+ **在线学习**：在强化学习中，策略通常需要在每一步或每几步更新一次。如果每次更新都需要精确计算KL散度，可能会导致训练过程变得非常缓慢。近似器可以快速估计KL散度，从而支持在线学习和实时更新。

**使用近似器来估计KL散度**

[Schulman et al. (2020)](https://link.zhihu.com/?target=http%3A//joschu.net/blog/kl-approx.html)<font style="color:rgb(25, 27, 31);"> 提出的</font>**<font style="color:#ED740C;">近似器</font>**<font style="color:rgb(25, 27, 31);">可以根据当前策略和参考策略的差异动态调整估计的精度，从而在保证计算效率的同时，尽可能减少估计误差，其定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327720687-37130509-39b0-441a-939c-99d21b3325cc.png)

<font style="color:rgb(25, 27, 31);">这个近似器的优势在于它只需要</font>**<font style="color:#ED740C;">计算当前策略和参考策略的概率比值，而不需要直接计算KL散度的积分或期望。因此，它可以在保证一定精度的同时，显著降低计算复杂度。</font>**

4. ** 计算损失（Computing the loss）**

<font style="color:rgb(25, 27, 31);">这一步的目标是最大化优势，同时确保模型保持在参考策略附近。因此，损失定义如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741327776028-b54b4f85-952c-4d47-abed-9fc4141d541e.png)

<font style="color:rgb(25, 27, 31);">其中第一项表示缩放后的优势，第二项通过KL散度惩罚与参考策略的偏离。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**优点**

1. 效率：GRPO无价值网络，相比PPO显存需求降低，训练速度提升。
2. 稳定性：GRPO组内相对优势减少方差，KL约束更惊喜，稳定性更高
3. 超参数敏感性：GRPO动态梯度正则化降低超参数敏感性
4. 扩展性：GRPO支持多任务联合优化，组内比较提升多样性

**缺点**

1. 适用动作空间：GRPO更依赖组内样本多样性，离散动作生产成本较高
2. 样本质量依赖：GRPO组内样本质量差时（如标准菜为0），优势估计时效

:::color5
**<font style="color:#601BDE;">4.伪代码实现</font>**

:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def grae_advantages(rewards):
    """概念性组相对优势估计（结果监督）。"""
    mean_reward = np.mean(rewards)
    std_reward = np.std(rewards)
    normalized_rewards = (rewards - mean_reward) / (std_reward + 1e-8)
    advantages = normalized_rewards  # 对于结果监督，优势 = 归一化奖励
    return advantages


def grpo_loss(old_policy_logprobs_group, new_policy_logprobs_group, group_advantages, kl_penalty_coef, clip_epsilon):
    """概念性 GRPO 损失函数（对一组响应取平均）。"""
    group_loss = 0
    for i in range(len(group_advantages)):  # 遍历组内的每个响应
        advantage = group_advantages[i]
        new_policy_logprob = new_policy_logprobs_group[i]
        old_policy_logprob = old_policy_logprobs_group[i]

        ratio = np.exp(new_policy_logprob - old_policy_logprob)
        clipped_ratio = np.clip(ratio, 1 - clip_epsilon, 1 + clip_epsilon)
        surrogate_objective = np.minimum(ratio * advantage, clipped_ratio * advantage)
        policy_loss = -surrogate_objective

        kl_divergence = new_policy_logprob - old_policy_logprob
        kl_penalty = kl_penalty_coef * kl_divergence
        group_loss += (policy_loss + kl_penalty)  # 累加组内每个响应的损失

    return group_loss / len(group_advantages)  # 对组内损失取平均
```

:::color5
**<font style="color:#601BDE;">3.核心代码</font>**

:::

1. **构造训练数据**：基于<font style="color:rgb(25, 27, 31);">Qwen-2.5-7B:</font>

```plain
'<|im_start|>system
用户和助手之间的对话。用户提出问题，助手解决问题。助手首先在脑海中思考推理过程，然后为用户提供答案。推理过程和答案分别包含在<think></think>和<answer></answer>标签中，即这里的<think>推理过程</think><answer>在这里回答</ansure><|im_end|>
<|im_start|>user
Kim今天参加数学考试的概率是$\frac{4}{7}$。Kim今天没有数学考试的可能性有多大？用普通分数表示你的答案<|im_end |>
<|im_start|>助手'
```

```json
“<think>这个问题给了我们金今天有数学考试的概率，即\\（\\frac{4}{7}\\）。一个事件没有发生的概率是1减去事件发生的概率。因此，我们需要从1中减去\\frac{14}{7}\\，得出金今天没有数学考试的概率。
要执行这个减法，我们可以将1表示为与\\frac[4}{7]\\具有相同分母的分数。这给了我们\\（1=\\frac[7}{7}\\ 
因此，金今天没有数学考试的概率是\\（\\frac{7}{7}-\\frac{14}{7]\\。
让我们进行减法运算以找到最终答案。
</think>
<answer>金今天没有数学考试的概率是\\（\\frac{3}{7}\\）</答案><|im_end|>“
```

2. **数据标注：**用<font style="color:rgb(25, 27, 31);">使用专业的数学verifier判断两个答案是否对，对的话reward就是1，否则就是0。这种设计非常适用于数学题等任务，因为答案的正确性可以直接通过对比来判断。</font>
3. **<font style="color:rgb(25, 27, 31);">奖励函数实现：</font>**<font style="color:rgb(25, 27, 31);">在 GRPO 中，奖励函数的设计至关重要。首先我们就来看看这个奖励函数是啥，代码中提供了一个简单的奖励函数 </font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">accuracy_reward</font>](https://zhida.zhihu.com/search?content_id=253691962&content_type=Article&match_order=1&q=accuracy_reward&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">，用于判断生成的输出是否正确。</font>

```python
def accuracy_reward(completions, solution, **kwargs):
    """Reward function that checks if the completion is the same as the ground truth."""
    contents = [completion[0]["content"] for completion in completions]
    rewards = []
    for content, sol in zip(contents, solution):
        gold_parsed = parse(
            sol,
            extraction_mode="first_match",
            extraction_config=[LatexExtractionConfig()],
        )
        if len(gold_parsed) != 0:
            # We require the answer to be provided in correct latex (no malformed operators)
            answer_parsed = parse(
                content,
                extraction_config=[
                    LatexExtractionConfig(
                        normalization_config=NormalizationConfig(
                            nits=False,
                            malformed_operators=False,
                            basic_latex=True,
                            equations=True,
                            boxed="all",
                            units=True,
                        ),
                        # Ensures that boxed is tried first
                        boxed_match_priority=0,
                        try_extract_without_anchor=False,
                    )
                ],
                extraction_mode="first_match",
            )
            # Reward 1 if the content is the same as the ground truth, 0 otherwise
            try:
                reward = float(verify(answer_parsed, gold_parsed))
            except Exception as e:
                print(f"verify failed: {e}, answer: {answer_parsed}, gold: {gold_parsed}")
                reward = 0.0
        else:
            # If the gold solution is not parseable, we reward 1 to skip this example
            reward = 1.0
            print("Failed to parse gold solution: ", sol)
        rewards.append(reward)

    return rewards
```

4. **GRPO trainer核心代码解析**

```python
def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
    if return_outputs:
        raise ValueError("The GRPOTrainer does not support returning outputs")
        # Compute the per-token log probabilities for the model

        prompt_ids, prompt_mask = inputs["prompt_ids"], inputs["prompt_mask"]
    completion_ids, completion_mask = inputs["completion_ids"], inputs["completion_mask"]
    input_ids = torch.cat([prompt_ids, completion_ids], dim=1)
    attention_mask = torch.cat([prompt_mask, completion_mask], dim=1)
    logits_to_keep = completion_ids.size(1)  # we only need to compute the logits for the completion tokens

    per_token_logps = self._get_per_token_logps(model, input_ids, attention_mask, logits_to_keep)

    # Compute the KL divergence between the model and the reference model
    if self.beta != 0.0:
        ref_per_token_logps = inputs["ref_per_token_logps"]
        per_token_kl = (
            torch.exp(ref_per_token_logps - per_token_logps) - (ref_per_token_logps - per_token_logps) - 1
        )

        # Compute the loss
        advantages = inputs["advantages"]
    # When using num_iterations == 1, old_per_token_logps == per_token_logps, so we can skip it's computation (see
    # _generate_and_score_completions) and use per_token_logps.detach() instead.
    old_per_token_logps = inputs["old_per_token_logps"] if self.num_iterations > 1 else per_token_logps.detach()
    coef_1 = torch.exp(per_token_logps - old_per_token_logps)
    coef_2 = torch.clamp(coef_1, 1 - self.epsilon, 1 + self.epsilon)
    per_token_loss1 = coef_1 * advantages.unsqueeze(1)
    per_token_loss2 = coef_2 * advantages.unsqueeze(1)
    per_token_loss = -torch.min(per_token_loss1, per_token_loss2)
    if self.beta != 0.0:
        per_token_loss = per_token_loss + self.beta * per_token_kl
        loss = (per_token_loss * completion_mask).sum() / completion_mask.sum()

    # Log the metrics
    mode = "eval" if self.control.should_evaluate else "train"

    if self.beta != 0.0:
        mean_kl = (per_token_kl * completion_mask).sum() / completion_mask.sum()
        self._metrics[mode]["kl"].append(self.accelerator.gather_for_metrics(mean_kl).mean().item())

        is_clipped = (per_token_loss1 < per_token_loss2).float()
    clip_ratio = (is_clipped * completion_mask).sum() / completion_mask.sum()
    self._metrics[mode]["clip_ratio"].append(self.accelerator.gather_for_metrics(clip_ratio).mean().item())
    return loss
```

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

### **<font style="color:rgb(34, 35, 40);">结果监督强化学习与 GRPO：</font>**
<font style="color:rgb(64, 64, 64);">对于每个问题 q，从旧策略模型 πθ_old 中抽取一组输出 {o1, o2, ..., oG}。然后使用奖励模型对这些输出进行评分，产生相应的 G 个奖励 r={r1, r2, ..., rG}。随后，通过减去组平均值并除以组标准差来对这些奖励进行标准化处理。结果监督在每个输出 oi 的末尾提供标准化的奖励，并将输出中所有token的优势 Aˆi,t 设定为该标准化奖励，即 Aˆi,t = (ri - mean(r)) / std(r)，然后通过最大化方程（3）中定义的目标来优化策略。</font>

### **<font style="color:rgb(34, 35, 40);">过程监督强化学习与GRPO:</font>**
<font style="color:rgb(64, 64, 64);">结果监督仅在每个输出结束时提供奖励，这可能不足以有效监督复杂数学任务中的策略。遵循历史方法，我们还探讨了过程监督，它在每个推理步骤结束时提供奖励。</font>

<font style="color:rgb(64, 64, 64);">具体来说，给定问题 q 和 G 个抽样输出 {o1, o2, ..., oG}，使用过程奖励模型对每个输出步骤进行评分，从而得到相应的奖励：R={{rindex(1), ..., rindex(K1)}, ..., {rindex(1)11G, ..., rindex(KG)G}}，其中 index(j) 是第 j 步的结束标记索引，Ki 是第 i 个输出中的总步数。</font>

<font style="color:rgb(64, 64, 64);">我们也用平均值和标准差对这些奖励进行标准化处理，即 ˜rindex(j)i = (rindex(j) - mean(R)) / std(R)。接下来，过程监督计算每个标记的优势作为后续步骤的标准化奖励之和，即 Aˆi,t = ∑index(j)≥t ˜rindex(j)i，并通过最大化方程（3）中定义的目标来优化策略。</font>

### **<font style="color:rgb(34, 35, 40);">迭代强化学习与GRPO：</font>**
<font style="color:rgb(64, 64, 64);">在强化学习的训练进程中，随着策略模型的不断进化，旧的奖励模型可能不足以有效地监督当前的策略模型。因此，为了应对这个问题，我们引入了带有组相对策略优化（Group Relative Policy Optimization, GRPO）的迭代强化学习方法。</font>

<font style="color:rgb(64, 64, 64);">具体来说，在每次迭代中，</font><font style="color:#DF2A3F;">基于当前策略模型生成的数据创建新的奖励模型训练集</font><font style="color:rgb(64, 64, 64);">，并通过一种包含重播机制的方法来持续训练奖励模型，其中历史数据占比10%。这一过程有助于确保奖励模型能够跟上策略模型的进步，从而更有效地指导后续的训练。</font>

### **<font style="color:rgb(34, 35, 40);">DeepSeekMath-RL的训练与评估：</font>**
<font style="color:rgb(64, 64, 64);">在本节中，我们详细描述了DeepSeekMath-RL模型的训练和评估过程。首先介绍了用于监督学习阶段的数据集，并讨论了强化学习(RL)训练设置。随后，展示了评估结果，并将DeepSeekMath-RL与不同的基线方法进行了比较。</font>

### **<font style="color:rgb(34, 35, 40);">监督学习数据集</font>**
<font style="color:rgb(64, 64, 64);">为了训练DeepSeekMath-RL的基础策略模型，我们使用了一个包含3500万个数学问题的数据集进行监督学习。这些问题是通过从互联网上爬取得到的，并经过清理以确保其适合用于训练。此外，对于奖励模型的训练，我们额外收集了一个由高质量回答组成的数据集，这些回答是通过抽样自旧策略模型生成的答案，并经过人工标注者筛选和改进得到的。这个奖励模型训练集包含了约1600万个问题-答案对。</font>

### **<font style="color:rgb(34, 35, 40);">强化学习训练设置</font>**
<font style="color:rgb(64, 64, 64);">在强化学习阶段，我们采用了先前部分中介绍的方法：结果监督、过程监督以及迭代GRPO。为了保证训练的稳定性，我们采取了一系列措施，包括但不限于：</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(64, 64, 64);">使用监督学习阶段训练出的模型作为初始化；</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(64, 64, 64);">在更新策略时，结合历史数据（约占10%）来保持训练的连续性和稳定性；</font>

<font style="color:rgb(64, 64, 64);">●</font><font style="color:rgb(64, 64, 64);">调整学习率和其他超参数以优化性能。</font>

### **<font style="color:rgb(34, 35, 40);">关于强化学习的理解：</font>**
#### <font style="color:rgb(34, 35, 40);">朝向统一范式：</font>
<font style="color:rgb(64, 64, 64);">在本节中，我们提供了一个统一的范式来分析不同的训练方法，如SFT、RFT、DPO、PPO、GRPO，并进一步进行实验以探索该统一范式的因素。一般来说，关于参数 </font>_<font style="color:rgb(64, 64, 64);">θ</font>_<font style="color:rgb(64, 64, 64);"> 的训练方法的梯度可以写成：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738813294301-1bc1be1f-ce05-44db-a151-7a361c9514a9.png)

<font style="color:rgb(64, 64, 64);">存在三个关键组成部分：1）数据源 </font>_<font style="color:rgb(64, 64, 64);">D</font>_<font style="color:rgb(64, 64, 64);">，它决定了训练数据；2）奖励函数 </font>_<font style="color:rgb(64, 64, 64);">πθold</font>_<font style="color:rgb(64, 64, 64);">，它是训练奖励信号的来源；3）算法 </font>_<font style="color:rgb(64, 64, 64);">A</font>_<font style="color:rgb(64, 64, 64);">：它处理训练数据和奖励信号以确定梯度系数 </font>_<font style="color:rgb(64, 64, 64);">A</font>_<font style="color:rgb(64, 64, 64);">(</font>_<font style="color:rgb(64, 64, 64);">s</font>_<font style="color:rgb(64, 64, 64);">,</font>_<font style="color:rgb(64, 64, 64);">a</font>_<font style="color:rgb(64, 64, 64);">,</font>_<font style="color:rgb(64, 64, 64);">i</font>_<font style="color:rgb(64, 64, 64);">,</font>_<font style="color:rgb(64, 64, 64);">πθold</font>_<font style="color:rgb(64, 64, 64);">)，该系数决定了对数据的惩罚或强化的大小。我们根据这样一个统一的范式分析了几种代表性方法：</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">监督微调（SFT）</font>**<font style="color:rgb(64, 64, 64);">：SFT在人类选择的SFT数据上对预训练模型进行微调。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">拒绝采样微调（RFT）</font>**<font style="color:rgb(64, 64, 64);">：RFT进一步在SFT模型采样的输出上对SFT模型进行微调，这些输出基于SFT问题进行了过滤。RFT根据答案的正确性过滤输出。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">直接偏好优化（DPO）</font>**<font style="color:rgb(64, 64, 64);">：DPO通过在SFT模型采样的输出上使用成对的DPO损失来微调SFT模型。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">在线拒绝采样微调（Online RFT）</font>**<font style="color:rgb(64, 64, 64);">：与RFT不同，Online RFT使用实时策略模型进行初始化，并通过实时策略模型采样的增强输出进行微调。</font>

<font style="color:rgb(64, 64, 64);">●</font>**<font style="color:rgb(64, 64, 64);">PPO/GRPO</font>**<font style="color:rgb(64, 64, 64);">：PPO/GRPO使用SFT模型初始化策略模型，并使用实时策略模型采样的输出进行强化。</font>

<font style="color:rgb(64, 64, 64);"></font>

#### <font style="color:rgb(64, 64, 64);">为什么强化学习有效？</font>
<font style="color:rgb(64, 64, 64);">在本文中，我们在一个子集的指令微调数据上进行了强化学习，并且在指令微调模型的基础上取得了显著的性能提升。为了进一步解释为什么强化学习有效，我们在两个基准测试上评估了SFT和RL DeepSeekMath 7B的Pass@K和Maj@K准确率。如图7所示，RL增强了Maj@K的性能，但没有增强Pass@K。这些发现表明，</font><font style="color:#DF2A3F;">RL通过使输出分布更加稳健来增强模型的整体性能，换句话说，似乎改进是归因于从TopK中提升正确响应，而不是增强基本能力。</font>

