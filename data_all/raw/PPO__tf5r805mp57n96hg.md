# PPO

<!-- source: yuque://zhongxian-iiot9/hlyypb/tf5r805mp57n96hg -->

# PPO（<font style="color:rgb(64, 64, 64);">Proximal Policy Optimization </font>）
:::color3
**简介：**PPO（ProximalPolicyOptimization，近端策略优化）是⼀种常⽤的强化学习算法，属于策略优化⽅法，**<font style="color:#ED740C;">是RLHF中策略优化的执行者，根据奖励模型提供的奖励更新策略参数</font>**。其核⼼思想是通过限制策略更新的幅度来提升训练的稳定性，避免策略在每次更新中发⽣较⼤变化，从⽽防⽌训练过程中的不稳定和策略崩溃。

参考：[图解大模型RLHF系列之：人人都能看懂的PPO原理与源码解读](https://zhuanlan.zhihu.com/p/677607581)

:::

**<font style="color:rgb(25, 27, 31);">PPO（Proximal Policy Optimization）</font>**<font style="color:rgb(25, 27, 31);"> 是一种用于强化学习的策略优化算法，由 </font>[<font style="color:rgb(9, 64, 142);">OpenAI</font>](https://zhida.zhihu.com/search?content_id=710831409&content_type=Answer&match_order=1&q=OpenAI&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 提出。</font>**<font style="color:#74B602;">它通过限制策略更新的幅度，确保训练过程的稳定性。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743411227505-2e7ff874-cac1-4444-b52e-bab4bafff841.png)

<font style="color:rgb(25, 27, 31);">如上图，</font>**<font style="color:rgb(25, 27, 31);">在RLHF-PPO阶段，一共有四个主要模型</font>**<font style="color:rgb(25, 27, 31);">，分别是：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

+ [**<font style="color:rgb(9, 64, 142);">Actor Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Actor+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：演员模型</font>**<font style="color:rgb(25, 27, 31);">，这就是我们想要训练的目标语言模型</font>
+ [**<font style="color:rgb(9, 64, 142);">Critic Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Critic+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：评论家模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是预估总收益</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">V</font><font style="color:rgb(25, 27, 31);">t</font>
+ [**<font style="color:rgb(9, 64, 142);">Reward Model</font>**](https://zhida.zhihu.com/search?content_id=238709685&content_type=Article&match_order=1&q=Reward+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">：奖励模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是计算即时收益</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">R</font><font style="color:rgb(25, 27, 31);">t</font>
+ **<font style="color:rgb(25, 27, 31);">Reference Model：参考模型</font>**<font style="color:rgb(25, 27, 31);">，它的作用是在RLHF阶段给语言模型增加一些“约束”，防止语言模型训歪（朝不受控制的方向更新，效果可能越来越差）</font>

<font style="color:rgb(25, 27, 31);">其中:</font>

+ **<font style="color:rgb(25, 27, 31);">Actor/Critic Model</font>**<font style="color:rgb(25, 27, 31);">在RLHF阶段是</font>**<font style="color:rgb(25, 27, 31);">需要训练</font>**<font style="color:rgb(25, 27, 31);">的（图中给这两个模型加了粗边，就是表示这个含义）；而</font>**<font style="color:rgb(25, 27, 31);">Reward/Reference Model</font>**<font style="color:rgb(25, 27, 31);">是</font>**<font style="color:rgb(25, 27, 31);">参数冻结</font>**<font style="color:rgb(25, 27, 31);">的。</font>
+ <font style="color:rgb(25, 27, 31);">Critic/Reward/Reference Model共同组成了一个“奖励-loss”计算体系（我自己命名的，为了方便理解），我们综合它们的结果计算loss，用于更新Actor和Critic Model</font>

:::color5
#### <font style="color:#601BDE;">0.核心思想</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">PPO</font><font style="color:#1f2329;">通过⼀种</font><font style="color:#d83931;">剪辑损失函数（</font><font style="color:#d83931;">Clipped</font><font style="color:#d83931;">Surrogate</font><font style="color:#d83931;">Objective</font><font style="color:#d83931;">）</font><font style="color:#1f2329;">来实现策略的优化</font><font style="color:#1f2329;">，它的</font><font style="color:#2ea121;">⽬标是确保策</font>

<font style="color:#2ea121;">略更新时不会偏离当前策略太多。它克服了传统策略梯度⽅法</font><font style="color:#1f2329;">（如</font><font style="color:#1f2329;">TRPO</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">Trust Region Policy</font><font style="color:#1f2329;"> Optimization</font><font style="color:#1f2329;">）复杂的约束问题</font><font style="color:#1f2329;">，保持了性能的同时降低了实现难</font><font style="color:#1f2329;">度。</font>

<font style="color:#1f2329;">传统的策略优化⽬标是直接优化策略</font>_<font style="color:#1f2329;">π</font>__<font style="color:#1f2329;">θ</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">a</font>_<font style="color:#1f2329;">∣</font>_<font style="color:#1f2329;">s</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，使得给定状态下的⾏为能够最⼤化累计奖励。</font><font style="color:#1f2329;">PPO</font><font style="color:#1f2329;">在此</font><font style="color:#1f2329;">基础上</font><font style="color:#1f2329;">，通过引⼊⼀个重要的⽐例项 </font><font style="color:#1f2329;">"</font><font style="color:#1f2329;">probability</font><font style="color:#1f2329;">ratio</font><font style="color:#1f2329;">"</font>_<font style="color:#1f2329;">r</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">来度量新旧策略之间的差异：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739167940952-02d9fc31-9544-4f84-ae56-1f41d5009ab0.png)

<font style="color:#1f2329;">其中，</font>_<font style="color:#1f2329;">π</font>__<font style="color:#1f2329;">θ</font>_<sub><font style="color:#1f2329;">old</font></sub><font style="color:#1f2329;">  是更新前的策略，⽽  </font>_<font style="color:#1f2329;">π</font>__<font style="color:#1f2329;">θ  </font>_<font style="color:#1f2329;">是更新后的策略。该⽐率表⽰在同⼀状态-⾏为对</font><font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t </font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">下，新旧策略选择该⾏为的概率之⽐。如果这个⽐率偏离1过多，说明更新后的策略与原始策略差异较⼤，可能会导致训练不稳定。</font>

:::color5
#### <font style="color:#601BDE;">1.PPO关键角色 </font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

+ **<font style="color:rgb(25, 27, 31);">策略（LLM）</font>**<font style="color:rgb(25, 27, 31);">：我们正在训练的 LLM，用于生成更好的文本。</font>
+ **<font style="color:rgb(25, 27, 31);">奖励模型</font>**<font style="color:rgb(25, 27, 31);">：根据人类偏好对文本打分的 AI 裁判。</font>
+ **<font style="color:rgb(25, 27, 31);">价值函数（辅助教练）</font>**<font style="color:rgb(25, 27, 31);">：另一个 AI 模型，充当“辅助教练”。它估计每个状态的“好坏”（当前文本生成的前景如何）。这有助于 PPO 进行更智能的更新。</font>

:::color5
#### <font style="color:#601BDE;">2.PPO训练步骤</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

1. **<font style="color:rgb(25, 27, 31);">生成文本（Rollout）</font>**<font style="color:rgb(25, 27, 31);">：LLM（策略）为不同的提示生成大量文本样本。</font>
2. **<font style="color:rgb(25, 27, 31);">奖励模型打分</font>**<font style="color:rgb(25, 27, 31);">：奖励模型对每个文本样本进行打分。</font>
3. **<font style="color:rgb(25, 27, 31);">计算优势函数（广义优势估计</font>**[**<font style="color:rgb(9, 64, 142);">GAE</font>**](https://zhida.zhihu.com/search?content_id=254489057&content_type=Article&match_order=1&q=GAE&zhida_source=entity)**<font style="color:rgb(25, 27, 31);"> —— “好多少”分数）</font>**<font style="color:rgb(25, 27, 31);">：这就是 GAE 的作用！它是一种巧妙的方法，用于计算每个单词选择的优劣，考虑奖励和价值函数的预测。</font>
4. **<font style="color:rgb(25, 27, 31);">优化 LLM（策略更新）</font>**<font style="color:rgb(25, 27, 31);">：我们更新 LLM 的策略，以最大化一个特殊的 PPO 目标函数。这个目标函数现在有三个关键部分：</font>
    - **<font style="color:rgb(25, 27, 31);">鼓励更高奖励</font>**<font style="color:rgb(25, 27, 31);">：它推动 LLM 生成能够获得更高分数的文本。</font>
    - **<font style="color:rgb(25, 27, 31);">限制策略变化（剪切代理目标）</font>**<font style="color:rgb(25, 27, 31);">：它防止策略在一次更新中变化过大，确保稳定性。</font>
    - **<font style="color:rgb(25, 27, 31);">KL 散度惩罚</font>**<font style="color:rgb(25, 27, 31);">：如果新策略与旧策略偏离太远，它会增加惩罚，进一步增强稳定性。</font>
    - **<font style="color:rgb(25, 27, 31);">熵奖励</font>**<font style="color:rgb(25, 27, 31);">：它还包括一个熵奖励。简单来说，熵衡量 LLM 文本生成的“随机性”或“多样性”。增加熵奖励可以鼓励 LLM 更多地探索，而不是总是生成相同、可预测的响应。它有助于防止 LLM 过早变得“过于确定”，从而错过可能更好的策略。</font>
5. **<font style="color:rgb(25, 27, 31);">更新价值函数（辅助教练更新）</font>**<font style="color:rgb(25, 27, 31);">：训练价值函数成为一个更好的“辅助教练”——更准确地预测不同文本生成的“好坏”。</font>

:::color5
#### <font style="color:#601BDE;">3.损失函数</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">PPO的损失函数是基于策略⽐率</font>_<font style="color:#1f2329;">r</font>_<sub>_<font style="color:#1f2329;">t</font>_</sub>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">θ</font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">进⾏定义的，它有两种主要形式：</font><font style="color:#2ea121;">剪辑形式</font><font style="color:#1f2329;">和</font><font style="color:#2ea121;">KL散度形式</font><font style="color:#1f2329;">。</font>

1. **<font style="color:#1f2329;">剪辑损失函数</font>**<font style="color:#1f2329;">：它通过对策略更新的⽐率进⾏剪辑来避免策略⼤幅度更新。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739168127764-ee2268cb-48e8-4264-9a98-c3cb6de17cc1.png)

2. **基于KL散度的PPO**：<font style="color:#1f2329;">KL散度⽤于度量新旧策略分布的差异，通常定义为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739168140722-4d78b942-5dbc-4c33-a2b9-f6533f57a9a9.png)

:::color5
#### <font style="color:#601BDE;">4.优势函数At的估计(Advantage)    GAE（广义优势估计）</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

<font style="color:#1f2329;">在PPO中 ，优势函数</font>_<font style="color:#1f2329;">A</font>_<sup>_<font style="color:#1f2329;">t</font>_</sup><sup>_<font style="color:#1f2329;"> </font>_</sup>_<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">的准确估计对策略的优化效果⾄关重要。</font>

<font style="color:#1f2329;">通常</font><font style="color:#1f2329;">，优势函数被定义为当前策略相对于基准策略的相对表现：</font>_<font style="color:#1f2329;">A</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">=</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">−</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">V</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">其中：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font>_<font style="color:#1f2329;">Q</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t</font>_<font style="color:#1f2329;">,</font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">是给定状态和⾏为下的动作值函数</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，表</font><font style="color:#1f2329;">⽰采取动作</font><font style="color:#1f2329;"> </font>_<font style="color:#1f2329;">a</font>__<font style="color:#1f2329;">t</font>__<font style="color:#1f2329;">  </font>_<font style="color:#1f2329;">后的预期回报；</font>

<font style="color:#1456f0;">•  </font>_<font style="color:#1f2329;">V </font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t </font>_<font style="color:#1f2329;">) </font><font style="color:#1f2329;">是状态值函数 ，表⽰在状态 </font>_<font style="color:#1f2329;">s</font>__<font style="color:#1f2329;">t  </font>_<font style="color:#1f2329;">下的预期回报。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739168798867-dadb2d0c-de65-47b9-beca-a2cffac8775b.png)

**<font style="color:rgb(25, 27, 31);">为什么选择 GAE？（蒙特卡洛与时间差分 —— 方差与偏差）</font>**

+ **<font style="color:rgb(25, 27, 31);">蒙特卡洛（MC）—— 高方差，低偏差</font>**<font style="color:rgb(25, 27, 31);">：想象一下等到整个文本生成后再获得奖励，然后将该奖励分配给文本中的每一个单词。就像只有在小狗完成整个“坐下、待命、取回”动作序列后才给予奖励。对整个序列的奖励是准确的，但对单个动作（“坐下”与“待命”与“取回”）的信号非常嘈杂。高方差，学习速度慢。</font>
+ **<font style="color:rgb(25, 27, 31);">时间差分（TD）—— 低方差，高偏差</font>**<font style="color:rgb(25, 27, 31);">：想象一下在每个单词生成后给予奖励。“好单词！”“普通单词！”“很棒的单词！”信号不那么嘈杂，学习速度更快。但是，我们只是局部地判断单词，没有考虑整个文本的长期质量。可能会有偏差，可能会错过“大局”。</font>
+ **<font style="color:rgb(25, 27, 31);">GAE —— 平衡</font>**<font style="color:rgb(25, 27, 31);">：广义优势估计（GAE）就像“多步 TD”。它考虑了多个步骤（单词）上的奖励，平衡了方差（MC）与偏差（TD）之间的权衡。就像不仅在结束时给予奖励，还在价值函数预测的指导下，为沿途的“小步骤”给予奖励。</font>

:::color5
#### <font style="color:#601BDE;">5.优缺点</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

**优点**

+ <font style="color:#1f2329;">更新稳定：通过剪辑⽐率或KL散度约束，PPO限制了每次更新的幅度，</font><font style="color:#d83931;">防⽌策略发⽣剧烈变化，从⽽提⾼了算法的稳定性</font><font style="color:#1f2329;">。</font>
+ <font style="color:#1f2329;">与TRPO相⽐，PPO⽆需复杂的约束优化算法，易于实现和调整超参数。</font>
+ <font style="color:#1f2329;">适用性强：PPO适⽤于离散和连续动作空间，⼴泛应⽤于各种强化学习任务。</font>

**<font style="color:rgb(64, 64, 64);">缺点</font>**<font style="color:rgb(64, 64, 64);">：</font>

+ <font style="color:rgb(64, 64, 64);">PPO 中的</font>_**<font style="color:rgb(64, 64, 64);">值函数通常是一个与策略模型大小相当的模型</font>**_<font style="color:rgb(64, 64, 64);">，</font>_**<font style="color:#DF2A3F;">这带来了显著的内存和计算负担</font>**_<font style="color:rgb(64, 64, 64);">。</font>
+ <font style="color:rgb(64, 64, 64);">在 LLMs 的上下文中，值函数在训练过程中被用作优势计算中的Baseline，但通常只有最后一个 token 会被奖励模型赋予奖励分数，这可能使得值函数的训练变得复杂。</font>

:::color5
#### <font style="color:#601BDE;">6.代码实现</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::

```python
# 注意：这不是实际公式。
# 这是一个高度简化的预期目标版本
def ppo_loss_with_gae_entropy(old_policy_logprobs, new_policy_logprobs, advantages, kl_penalty_coef, clip_epsilon, entropy_bonus_coef):
    """概念性 PPO 损失函数，带有 GAE 和熵奖励（简化版）。"""

    ratio = np.exp(new_policy_logprobs - old_policy_logprobs)  # 概率比

    # 剪切代理目标（限制策略变化）
    surrogate_objective = np.minimum(ratio * advantages, np.clip(ratio, 1 - clip_epsilon, 1 + clip_epsilon) * advantages)
    policy_loss = -np.mean(surrogate_objective)

    # KL 散度惩罚（保持接近旧策略）
    kl_divergence = np.mean(new_policy_logprobs - old_policy_logprobs)
    kl_penalty = kl_penalty_coef * kl_divergence

    # 熵奖励（鼓励探索）
    entropy = -np.mean(new_policy_logprobs)  # 简化版熵（概率越高 = 熵越低，取负值以最大化熵）
    entropy_bonus = entropy_bonus_coef * entropy

    total_loss = policy_loss + kl_penalty - entropy_bonus  # 减去熵奖励，因为我们希望*最大化*熵
    return total_loss
```

```python
import tensorflow as tf
import gym
import numpy as np

class PPO:
    def __init__(self, env, hidden_size=64, batch_size=64, clip_ratio=0.2, learning_rate=1e-4):
        self.env = env
        self.batch_size = batch_size
        self.clip_ratio = clip_ratio

        # 定义神经网络
        self.actor = self.build_actor(hidden_size)
        self.critic = self.build_critic(hidden_size)

        self.optimizer_actor = tf.keras.optimizers.Adam(learning_rate)
        self.optimizer_critic = tf.keras.optimizers.Adam(learning_rate)

    def build_actor(self, hidden_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_size, activation='relu'),
            tf.keras.layers.Dense(self.env.action_space.n, activation='softmax')
        ])
        return model

    def build_critic(self, hidden_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(hidden_size, activation='relu'),
            tf.keras.layers.Dense(1, activation='linear')
        ])
        return model

    def get_action(self, state):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        action_probs = self.actor(state)
        action = tf.random.categorical(tf.math.log(action_probs), 1)
        return action.numpy()[0]

    def compute_value(self, state):
        state = tf.convert_to_tensor(state, dtype=tf.float32)
        return self.critic(state)

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

            # 将轨迹转为Tensor
            states = tf.convert_to_tensor([t[0] for t in trajectories], dtype=tf.float32)
            actions = tf.convert_to_tensor([t[1] for t in trajectories], dtype=tf.int32)
            rewards = tf.convert_to_tensor([t[2] for t in trajectories], dtype=tf.float32)
            next_states = tf.convert_to_tensor([t[3] for t in trajectories], dtype=tf.float32)
            dones = tf.convert_to_tensor([t[4] for t in trajectories], dtype=tf.float32)

            # 计算V值和下一个V值
            vs = self.critic(states)
            next_vs = self.critic(next_states)
            # 计算优势
            advantages = rewards + (1 - dones) * self.gamma * next_vs - vs

            # 策略概率
            old_p = self.actor(tf.convert_to_tensor(states, dtype=tf.float32))
            old_p = tf.gather(old_p, actions, batch_dims=1)
            old_p = tf.stop_gradient(old_p)

            with tf.GradientTape() as actor_tape:
                new_p = self.actor(tf.convert_to_tensor(states, dtype=tf.float32))
                new_p = tf.gather(new_p, actions, batch_dims=1)
                ratio = tf.exp(tf.math.log(new_p + 1e-10) - tf.math.log(old_p + 1e-10))
                clip_ratio = tf.clip_by_value(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
                loss_actor = tf.reduce_mean(-tf.minimum(ratio * advantages, clip_ratio * advantages))

            with tf.GradientTape() as critic_tape:
                current_v = self.critic(tf.convert_to_tensor(states, dtype=tf.float32))
                loss_critic = tf.reduce_mean((rewards + tf.stop_gradient(advantages)) - current_v)

            # 更新Actor
            gradients_actor = actor_tape.gradient(loss_actor, self.actor.trainable_weights)
            self.optimizer_actor.apply_gradients(zip(gradients_actor, self.actor.trainable_weights))

            # 更新Critic
            gradients_critic = critic_tape.gradient(loss_critic, self.critic.trainable_weights)
            self.optimizer_critic.apply_gradients(zip(gradients_critic, self.critic.trainable_weights))

            print(f"Episode {episode}, Reward: {episode_reward}")

        print("Training completed.")

```



# PPO实践：<font style="color:rgb(51, 51, 51);">基于PPO的Qwen商品问答助手训练</font>
:::color3
**<font style="color:rgb(51, 51, 51);"></font>****<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：训练商品问答助手在电商场景中生成符合以下要求的回答：</font>

+ <font style="color:rgb(51, 51, 51);">准确性（商品参数正确）</font>
+ <font style="color:rgb(51, 51, 51);">合规性（不出现虚假宣传）</font>
+ <font style="color:rgb(51, 51, 51);">用户友好性（语言自然流畅）</font>
+ <font style="color:rgb(51, 51, 51);">价值观对齐（环保/伦理等声明需谨慎）</font>

**<font style="color:rgb(51, 51, 51);">技术框架</font>**<font style="color:rgb(51, 51, 51);">：PPO（Proximal Policy Optimization）为核心算法，整合四大模型实现RLHF（基于人类反馈的强化学习）</font>

:::

:::color5
**<font style="color:#601BDE;">1.4个模型实现</font>**

:::

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">1. Critic Model（价值模型）</font>**

+ **项目中的角色**：
    - **<font style="color:#74B602;">评估当前对话状态的价值</font>**<font style="color:rgb(51, 51, 51);">（预测未来累计奖励）</font>
    - <font style="color:rgb(51, 51, 51);">在PPO的</font>**<font style="color:rgb(51, 51, 51);">优势函数计算</font>**<font style="color:rgb(51, 51, 51);">中起关键作用</font>
    - <font style="color:rgb(51, 51, 51);">示例：当用户询问"有机棉T恤的环保性如何？"时，Critic会评估当前回答是否可能引发后续追问（如认证标准细节）</font>
+ **实现细节**：

```python
# 输入：当前对话状态（编码后的文本+历史记录）
# 输出：价值估计标量
class Critic(nn.Module):
    def forward(self, state_emb):
        return self.value_head(state_emb)  # [batch_size, 1]
```

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">2. Actor Model（策略模型）</font>**

+ **项目中的角色**：
    - <font style="color:rgb(51, 51, 51);">作为</font>**<font style="color:rgb(51, 51, 51);">可优化策略</font>**<font style="color:rgb(51, 51, 51);">生成回答</font>
    - <font style="color:rgb(51, 51, 51);">通过PPO更新逐步改进回答质量</font>
    - <font style="color:rgb(51, 51, 51);">示例：在生成"这款T恤通过GOTS认证"时，动态调整专业术语的使用比例</font>
+ **实现细节**：

```python
# 输入：用户问题文本
# 输出：回答的概率分布
class Actor(nn.Module):
    def forward(self, input_ids):
        logits = self.lm_head(input_ids)  # 语言模型输出
        return Categorical(logits=logits)
```

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">3. Reward Model（奖励模型）</font>**

+ **项目中的角色**：
    - <font style="color:rgb(51, 51, 51);">提供多维奖励信号：</font>
        * **<font style="color:rgb(51, 51, 51);">基础奖励</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:#74B602;">回答相关性（BERTScore）</font>**
        * **<font style="color:rgb(51, 51, 51);">安全奖励</font>**<font style="color:rgb(51, 51, 51);">：敏感词检测（如"绝对无害"等绝对化表述）</font>
        * **<font style="color:rgb(51, 51, 51);">价值观奖励</font>**<font style="color:rgb(51, 51, 51);">：环保声明验证（连接商品数据库校验）</font>
    - <font style="color:rgb(51, 51, 51);">示例：对回答"采用零污染工艺"触发数据库核查，若未找到认证则扣分</font>
+ **奖励函数设计**：

```python
def calculate_reward(response):
    safety = 1 - 0.2*contains_risk_terms(response) 
    accuracy = bertscore(query, response) 
    value_alignment = check_certifications(response) 
    return 0.4*safety + 0.5*accuracy + 0.1*value_alignment
```

**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">4. Reference Model（参考模型）</font>**

+ **项目中的角色**：
    - <font style="color:rgb(51, 51, 51);">作为</font>**<font style="color:rgb(51, 51, 51);">冻结的初始策略</font>**<font style="color:rgb(51, 51, 51);">（</font>**<font style="color:#74B602;">SFT微调后的Qwen基础模型</font>**<font style="color:rgb(51, 51, 51);">）</font>
    - <font style="color:rgb(51, 51, 51);">通过KL散度约束防止过度优化导致语言不自然</font>
    - <font style="color:rgb(51, 51, 51);">示例：当PPO策略开始生成过度正式的回答时，通过KL惩罚保持口语化风格</font>
+ **约束实现**：

```python
# 计算当前策略与参考策略的KL散度
kl_penalty = kl_div(
    F.log_softmax(actor_logits, dim=-1),
    F.log_softmax(ref_model_logits, dim=-1)
).mean()
```

:::color5
**<font style="color:#601BDE;">2.训练过程</font>**

:::

1. **初始化阶段**：
    - <font style="color:rgb(51, 51, 51);">Reference Model：加载经过监督微调（SFT）的Qwen-7B</font>
    - <font style="color:rgb(51, 51, 51);">Actor：克隆Reference Model参数作为初始策略</font>
    - <font style="color:rgb(51, 51, 51);">Critic：独立训练的价值网络</font>
    - <font style="color:rgb(51, 51, 51);">Reward Model：基于人工标注的10万条对比回答对训练</font>
2. **数据收集**：
    - <font style="color:rgb(51, 51, 51);">采样流程：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741675218636-212cda94-487c-49be-92dd-a308ee71b54e.png)

3. **PPO迭代训练**：
    - <font style="color:rgb(51, 51, 51);">关键更新步骤：</font>

```python
# 计算优势函数
advantages = rewards + gamma * critic(next_states) - critic(states)

# PPO损失计算
ratio = (actor_logprob - old_logprob).exp()
surr1 = ratio * advantages
surr2 = torch.clamp(ratio, 1-eps, 1+eps) * advantages
policy_loss = -torch.min(surr1, surr2) + beta * kl_penalty
```

:::color5
**<font style="color:#601BDE;">3.关键维度对比</font>**

:::

| **维度** | **Critic** | **Actor** | **Reward Model** | **Reference Model** |
| --- | --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">更新频率</font>** | <font style="color:rgb(51, 51, 51);">每个PPO迭代更新</font> | <font style="color:rgb(51, 51, 51);">主更新对象</font> | <font style="color:rgb(51, 51, 51);">预训练后冻结</font> | <font style="color:rgb(51, 51, 51);">完全冻结</font> |
| **<font style="color:rgb(51, 51, 51);">项目中的数据依赖</font>** | <font style="color:rgb(51, 51, 51);">环境交互轨迹</font> | <font style="color:rgb(51, 51, 51);">PPO梯度更新</font> | <font style="color:rgb(51, 51, 51);">人工标注的偏好数据</font> | <font style="color:rgb(51, 51, 51);">SFT训练数据</font> |
| **<font style="color:rgb(51, 51, 51);">显存占用</font>** | <font style="color:rgb(51, 51, 51);">约2GB（独立网络）</font> | <font style="color:rgb(51, 51, 51);">约14GB（7B模型）</font> | <font style="color:rgb(51, 51, 51);">约7GB（冻结）</font> | <font style="color:rgb(51, 51, 51);">约7GB（冻结）</font> |
| **<font style="color:rgb(51, 51, 51);">失败案例干预</font>** | <font style="color:rgb(51, 51, 51);">价值估计偏差导致收敛慢</font> | <font style="color:rgb(51, 51, 51);">生成不合规内容</font> | <font style="color:rgb(51, 51, 51);">奖励黑客攻击</font> | <font style="color:rgb(51, 51, 51);">KL约束过强导致创新性下降</font> |


:::color5
**<font style="color:#601BDE;">4.实际部署挑战</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">Reward Model的偏差控制</font>**<font style="color:rgb(51, 51, 51);">：需定期用新标注数据更新，防止模型利用奖励漏洞（如添加无意义环保术语刷分）</font>
2. **<font style="color:rgb(51, 51, 51);">Critic的价值过估计</font>**<font style="color:rgb(51, 51, 51);">：采用Double Critic架构和周期性延迟更新</font>
3. **<font style="color:rgb(51, 51, 51);">Reference Model的滞后性</font>**<font style="color:rgb(51, 51, 51);">：每季度更新一次参考模型以吸收新知识</font>
4. **<font style="color:rgb(51, 51, 51);">多目标权衡</font>**<font style="color:rgb(51, 51, 51);">：通过动态奖励加权（如促销期间适当提升销售话术权重）</font>

<font style="color:rgb(51, 51, 51);">通过这种架构，Qwen商品问答助手在测试中实现了：</font>

+ **<font style="color:rgb(51, 51, 51);">回答准确率</font>**<font style="color:rgb(51, 51, 51);">提升27%（相比纯SFT）</font>
+ **<font style="color:rgb(51, 51, 51);">合规违规率</font>**<font style="color:rgb(51, 51, 51);">下降至0.3%</font>
+ **<font style="color:rgb(51, 51, 51);">用户满意度</font>**<font style="color:rgb(51, 51, 51);">达到92.7%</font>



