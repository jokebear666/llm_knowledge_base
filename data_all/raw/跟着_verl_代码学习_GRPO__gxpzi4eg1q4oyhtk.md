# 跟着 verl 代码学习 GRPO

<!-- source: yuque://zhongxian-iiot9/hlyypb/gxpzi4eg1q4oyhtk -->

## <font style="color:rgb(25, 27, 31);">前言</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>[<font style="color:rgb(9, 64, 142);">verl</font>](https://zhida.zhihu.com/search?content_id=257013576&content_type=Article&match_order=1&q=verl&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 是现在非常火的 RL框架，而且已经支持了多个 RL算法（PPO, GRPO 等等），跟着 verl 的代码梳理一遍两个著名的RL算法，毕竟代码不会隐藏任何细节！</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">GRPO 算法是基于 PPO 算法改进来的，但是毕竟更简单，所以先从 GRPO 的流程开始学习，然后再看 PPO。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**https://github.com/volcengine/verl?tab=readme-ov-file**](https://github.com/volcengine/verl?tab=readme-ov-file)

**参考：**[**https://zhuanlan.zhihu.com/p/1899507365507732891**](https://zhuanlan.zhihu.com/p/1899507365507732891)** **[**https://www.zhihu.com/question/10766825126/answer/88583863333**](https://www.zhihu.com/question/10766825126/answer/88583863333)

:::

:::color5
**<font style="color:#601BDE;">1.GRPO 总体流程</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1757669784968-87bce253-c157-4060-b3d5-28d4836d99d1.png)

<font style="color:rgb(145, 150, 161);">grpo 与 ppo 算法对比</font>

<font style="color:rgb(25, 27, 31);">论文中这张图主要展示了 GRPO 和 PPO 的区别，隐藏了其他的细节，图中只能注意到以下几个关键点：</font>

1. <font style="color:rgb(25, 27, 31);">没有 Value Model 和输出 v（value）</font>
2. <font style="color:rgb(25, 27, 31);">同一个 q 得出了一组的 o（从 1 到 G）</font>
3. <font style="color:rgb(25, 27, 31);">计算 A（Advantage） 的算法从 GAE 变成了 Group Computation</font>
4. [<font style="color:rgb(9, 64, 142);">KL 散度</font>](https://zhida.zhihu.com/search?content_id=257013576&content_type=Article&match_order=1&q=KL+%E6%95%A3%E5%BA%A6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">计算不作用于 Reward Model，而是直接作用于 Policy Model</font>

<font style="color:rgb(25, 27, 31);">（其他细节看不懂，结合论文也依然比较抽象，因为我完全没有 RL 的知识基础，下文中我们结合代码会再一次尝试理解）</font>

<font style="color:rgb(25, 27, 31);">下面是根据 verl 代码自己 DIY 的流程图（帮助理解）：</font>

![](https://cdn.nlark.com/yuque/0/2025/tif/29769680/1757670360845-a4dacb77-71e7-43fe-8a1b-36ad4549b946.tif?x-oss-process=image/format,png)

## <font style="color:rgb(25, 27, 31);">第一步：Rollout</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">rollout 是一个强化学习专用词汇，指的是从一个特定的状态按照某个策略进行一些列动作和状态转移。</font>

:::

<font style="color:rgb(25, 27, 31);">在 LLM 语境下，“某个策略”就是 </font>[<font style="color:rgb(9, 64, 142);">actor model</font>](https://zhida.zhihu.com/search?content_id=257013576&content_type=Article&match_order=1&q=actor+model&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的初始状态，“进行一些列动作”指的就是推理，即输入 prompt 输出 response 的过程。</font>

```python
gen_batch_output = self.actor_rollout_wg.generate_sequences(gen_batch)
```

<font style="color:rgb(25, 27, 31);">其背后的实现一般就是是 vllm 或 sglang 这些常见推理框架的</font>**<font style="color:rgb(25, 27, 31);">离线推理</font>**<font style="color:rgb(25, 27, 31);">功能，这部分功能相对独立我们先不展开。</font>

### <font style="color:rgb(25, 27, 31);">权重同步</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">代码里面的 </font>`<font style="color:rgb(25, 27, 31);">rollout_sharding_manager</font>`<font style="color:rgb(25, 27, 31);"> 实现，它负责每一个大 step 结束后把刚刚训练好的 actor model 参数更新到 vllm 或 sglang，这样下一个大 step 的 rollout 采用的就是最新的模型权重（最新的策略）了。</font>

:::

<font style="color:rgb(25, 27, 31);">这是每一个大 step 里面真正要做的第一件事，在真正执行 rollout 之前。</font>

```python
class ActorRolloutRefWorker(Worker):
    # ...

    @register(dispatch_mode=Dispatch.DP_COMPUTE_PROTO)
    def generate_sequences(self, prompts: DataProto):
        # ...

        with self.rollout_sharding_manager:
            # ...

            prompts = self.rollout_sharding_manager.preprocess_data(prompts)
            output = self.rollout.generate_sequences(prompts=prompts)
            output = self.rollout_sharding_manager.postprocess_data(output)
```

`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">rollout_sharding_manager</font>`<font style="color:rgb(25, 27, 31);"> 的基类是 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">BaseShardingManager</font>`<font style="color:rgb(25, 27, 31);">：</font>

```python
class BaseShardingManager:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def preprocess_data(self, data: DataProto) -> DataProto:
        return data

    def postprocess_data(self, data: DataProto) -> DataProto:
        return data
```

`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">BaseShardingManager</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的派生类在各自的</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">__enter__</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">方法中实现了把 Actor Model 的权重 Sync 到 Rollout 实例的逻辑，以保证被</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">with self.rollout_sharding_manager</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">包裹的预处理和推理逻辑都是用的最新 Actor Model 权重。</font>

### <font style="color:rgb(25, 27, 31);">推理 N 次</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">GRPO 算法要求对每一个 prompt 都生成多个 response，后续才能根据组间对比得出相对于平均的优势（Advantage）</font>

:::

```yaml
actor_rollout_ref:
  rollout:
    # number of responses (i.e. num sample times)
    n: 1 # > 1 for grpo
```

<font style="color:rgb(25, 27, 31);">在 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">_build_rollout</font>`<font style="color:rgb(25, 27, 31);"> 的时候 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">actor_rollout_ref.rollout.n</font>`<font style="color:rgb(25, 27, 31);"> 被传给了 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">vLLMRollout</font>`<font style="color:rgb(25, 27, 31);"> 或其他的 Rollout 实现中，从而推理出 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">n</font>`<font style="color:rgb(25, 27, 31);"> 组 response：</font>

```python
class ActorRolloutRefWorker(Worker):
    def _build_rollout(self, trust_remote_code=False):
        # ...

        elif rollout_name == "vllm":
            # ...

            if vllm_mode == "customized":
                rollout = vLLMRollout(
                    actor_module=self.actor_module_fsdp,
                    config=self.config.rollout,
                    tokenizer=self.tokenizer,
                    model_hf_config=self.actor_model_config,
                )
```

## <font style="color:rgb(25, 27, 31);">第二步：计算 log prob</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">log 是 logit，prob 是 probability，合起来就是</font>**<font style="color:rgb(25, 27, 31);">对数概率</font>**<font style="color:rgb(25, 27, 31);">，举一个简单的例子来说明什么是 log prob：</font>

:::

```bash
词表仅有 5 个词：
    <pad> (ID 0)
    你好 (ID 1)
    世界 (ID 2)
    ! (ID 3)
    吗 (ID 4)

prompt：你好
prompt tokens: [1]

response：世界!
response tokens: [2,3]

模型前向传播得到完整的 logits 张量：
[
    [-1.0, 0.5, 2.0, -0.5, -1.5],    // 表示 “你好” 后接 “世界” 概率最高，数值为 2.0
    [-2.0, -1.0, 0.1, 3.0, 0.2]      // 表示 “你好世界” 后接 “!” 概率最高，数值为 3.0
]

对每个 logit 计算 softmax 得到：
[
    [-3.65, -2.15, -0.64, -3.15, -4.08],
    [-4.34, -3.32, -2.20, -0.20, -2.10]
]

提取实际 response 对应的数值：得到 log_probs：
[-0.64, -0.20]
```

:::color5
**<font style="color:#601BDE;">计算步骤</font>**

:::

1. <font style="color:rgb(25, 27, 31);">首先计算 prompt + response（来自 rollout）的完整 logits，即每一个 token 的概率分布</font>
2. <font style="color:rgb(25, 27, 31);">截取 response 部分的 logits</font>
3. <font style="color:rgb(25, 27, 31);">对每一个 logits 计算 log_sofmax（先 softmax，然后取对数），取出最终预测的 token 对应的 log_sofmax</font>
4. <font style="color:rgb(25, 27, 31);">最终输出 old_log_probs, size = [batchsize, seq_len]</font>

> **疑惑：**在上一步 Rollout 的时候我们不是已经进行过完整 batch 的推理了么？为什么现在还要重复进行一次 forward 来计算 log_prob，而不是在 generate 的过程中就把 log_prob 保存下来？  
**答：**因为 generate_sequences 阶段为了高效推理，不会保存每一个 token 的 log_prob，相反只关注整个序列的 log_prob。因此需要重新算一遍。
>

### <font style="color:rgb(25, 27, 31);">old log prob</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">指 Actor Model 对整个 batch 的数据（prompt + response）进行 forward 得到的 log_prob</font>

:::

```python
old_log_prob = self.actor_rollout_wg.compute_log_prob(batch)
```

<font style="color:rgb(25, 27, 31);">此处的 “old” 是相对于后续的 actor update 阶段，因为现在 actor model 还没有更新，所以依然采用的是旧策略 （ps：当前 step 的”旧策略“也是上一个大 step 的“新策略”）</font>

### <font style="color:rgb(25, 27, 31);">ref log prob</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">指 Ref Model 对整个 batch 的数据（prompt + response）进行 forward 得到的 log_prob</font>

:::

```python
ref_log_prob = self.ref_policy_wg.compute_ref_log_prob(batch)
```

<font style="color:rgb(25, 27, 31);">通常 Ref Model 就是整个强化学习开始之前 Actor Model 最初的模样，换句话说第一个大 step 开始的时候 Actor Model == Ref Model，且 old_log_prob == ref_log_prob</font>

<font style="color:rgb(25, 27, 31);">Ref Model 的作用是在后续计算 policy loss 之前，计算 KL 散度并作用于 policy loss，目的是让 actor model 不要和最初的</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">ref model</font>](https://zhida.zhihu.com/search?content_id=257013576&content_type=Article&match_order=1&q=ref+model&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">相差太远</font>

## <font style="color:rgb(25, 27, 31);">第三步：advantage</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">advantage 是对一个策略的好坏最直接的评价，其背后就是 Reward Model，甚至也许不是一个 Model，而是一个粗暴的 function，甚至一个 sandbox 把 prompt+response 执行后得出的结果。</font>

:::

<font style="color:rgb(25, 27, 31);">在 verl 中允许使用上述多种 Reward 方案中的一种或多种，并把得出的 score 做合</font>

```python
# compute reward model score
if self.use_rm:
    reward_tensor = self.rm_wg.compute_rm_score(batch)
    batch = batch.union(reward_tensor)

if self.config.reward_model.launch_reward_fn_async:
    future_reward = compute_reward_async.remote(batch, self.config, self.tokenizer)
else:
    reward_tensor, reward_extra_infos_dict = compute_reward(batch, self.reward_fn)
```

<font style="color:rgb(25, 27, 31);">然后用这个 score 计算最终的 advantage</font>

```python
# compute advantages, executed on the driver process
norm_adv_by_std_in_grpo = self.config.algorithm.get(
    "norm_adv_by_std_in_grpo", True
)  # GRPO adv normalization factor
batch = compute_advantage(
    batch,
    adv_estimator=self.config.algorithm.adv_estimator,
    gamma=self.config.algorithm.gamma,
    lam=self.config.algorithm.lam,
    num_repeat=self.config.actor_rollout_ref.rollout.n,
    norm_adv_by_std_in_grpo=norm_adv_by_std_in_grpo,
)
```

## <font style="color:rgb(25, 27, 31);">第四步：actor update（小循环）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在 PPOTrainer 中简单地一行调用，背后可是整个 GRPO 算法中最关键的步骤</font>

:::

```python
actor_output = self.actor_rollout_wg.update_actor(batch)
```

<font style="color:rgb(25, 27, 31);">在这里，会把上面提到的整个 batch 的数据再根据</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">actor_rollout_ref.actor.ppo_mini_batch_size</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">配置的值拆分成很多个 mini batch，然后对每一个 mini batch 数据进行一轮 forward + backward + optimize step，也就是小 step</font>

### <font style="color:rgb(25, 27, 31);">new log prob</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">每一个小 step 中首先会对 mini batch 的数据计算（new）log_prob，第一个小 step 得到的值还是和 old_log_prob 一模一样的</font>

:::

### <font style="color:rgb(25, 27, 31);">pg_loss</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">通过输入所有 Group 的 Advantage 以新旧策略的概率比例（old_log_prob 和 log_prob），得出 pg_loss（Policy Gradient），这是最终用于 backward 的 policy loss 的基础部分：</font>

:::

<font style="color:rgb(25, 27, 31);">再次描述一下 pg_loss 的意义，即衡量当前策略（log_prob）相比于旧策略（old_log_prob），在当前优势函数（advantage）指导下的改进程度。</font>

```python
pg_loss, pg_clipfrac, ppo_kl, pg_clipfrac_lower = compute_policy_loss(
    old_log_prob=old_log_prob,
    log_prob=log_prob,
    advantages=advantages,
    response_mask=response_mask,
    cliprange=clip_ratio,
    cliprange_low=clip_ratio_low,
    cliprange_high=clip_ratio_high,
    clip_ratio_c=clip_ratio_c,
    loss_agg_mode=loss_agg_mode,
)
```

### <font style="color:rgb(25, 27, 31);">entropy loss</font>
:::color3
**简介：**`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">entropy</font>`<font style="color:rgb(25, 27, 31);"> 指策略分布的熵 (Entropy)：策略对选择下一个动作（在这里是下一个 token）的不确定性程度。熵越高，表示策略输出的概率分布越均匀，选择各个动作的概率越接近，策略的探索性越强；熵越低，表示策略越倾向于选择少数几个高概率的动作，确定性越强。</font>

:::

`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">entropy_loss</font>`<font style="color:rgb(25, 27, 31);"> 指 entropy 的 平均值，是一个标量，表示探索性高低</font>

```python
if entropy_coeff != 0:
    entropy_loss = agg_loss(loss_mat=entropy, loss_mask=response_mask, loss_agg_mode=loss_agg_mode)

    # compute policy loss
    policy_loss = pg_loss - entropy_loss * entropy_coeff
else:
    policy_loss = pg_loss
```

### <font style="color:rgb(25, 27, 31);">计算 KL 散度</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">这里用到了前面 Ref Model 推出的 ref_log_prob，用这个来计算 KL 并作用于最后的 policy_loss，保证模型距离 Ref Model（初始的模型）偏差不会太大：</font>

:::

```python
if self.config.use_kl_loss:
    ref_log_prob = data["ref_log_prob"]
    # compute kl loss
    kld = kl_penalty(
        logprob=log_prob, ref_logprob=ref_log_prob, kl_penalty=self.config.kl_loss_type
    )
    kl_loss = agg_loss(
        loss_mat=kld, loss_mask=response_mask, loss_agg_mode=self.config.loss_agg_mode
    )

    policy_loss = policy_loss + kl_loss * self.config.kl_loss_coef
    metrics["actor/kl_loss"] = kl_loss.detach().item()
    metrics["actor/kl_coef"] = self.config.kl_loss_coef
```

### <font style="color:rgb(25, 27, 31);">反向计算</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">持续循环小 step，直到遍历完所有的 mini batch，Actor Model 就完成了本轮的训练，会在下一个大 step 前把权重 sync 到 Rollout实例当中，准备处理下一个大 batch 数据。</font>

:::

```python
loss.backward()
```

