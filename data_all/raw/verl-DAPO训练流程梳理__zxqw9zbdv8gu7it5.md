# verl-DAPO训练流程梳理

<!-- source: yuque://zhongxian-iiot9/hlyypb/zxqw9zbdv8gu7it5 -->

## 项目背景与框架简介
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(31, 31, 31);">推理规模化使大语言模型具备了前所未有的推理能力，其中强化学习是引发复杂推理的核心技术。然而，最先进的推理大语言模型的关键技术细节往往被隐藏（如 OpenAI 的博客和 DeepSeek R1 技术报告），因此社区仍然难以复现他们的强化学习训练结果。</font>

:::

:::color3
**简介：**字节提出<font style="color:rgb(31, 31, 31);">解耦裁剪和动态采样策略优化</font>**<font style="color:#ED740C;">DAPO（Decoupled Clip and Dynamic sAmpling Policy Optimization，DAPO）</font>**<font style="color:rgb(31, 31, 31);">算法。此外，开源了基于 verl 框架构建的训练代码，以及精心策划和处理的数据集。开源系统的这些组件增强了可复现性，并支持未来大规模 LLM 强化学习的研究。</font>本章节旨在介绍 `verl` 框架的核心定位、适用场景，以及基于`verl`的<font style="color:rgb(25, 27, 31);">DAPO训练流程梳理。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/volcengine/verl](https://github.com/volcengine/verl)

**paper：**[https://arxiv.org/pdf/2503.14476](https://arxiv.org/pdf/2503.14476)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770289951810-26c5b992-5240-44c8-8b73-ddf83e1e9320.png)

:::color5
**<font style="color:#601bde;">1. 框架定义 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

verl 是一个专用于大语言模型（LLM）强化学习（RL）训练的开源框架。它旨在解决分布式训练、模型推理以及 Reward 计算等复杂工程问题，支持用户通过 PPO、GRPO、DAPO 等算法高效进行 LLM 的 RL 训练。

:::color5
**<font style="color:#601bde;">2.VeRL 核心优势</font>**

:::

选择 `verl` 框架进行开发主要基于以下考量：

+ 多算法支持：原生支持 PPO、GRPO、DAPO、REINFORCE++ 等多种主流算法，仅需修改配置即可切换。
+ 分布式友好：基于 Ray 构建，自动处理多机多卡训练的资源调度。
+ 推理引擎灵活：兼容 vLLM 和 SGLang，保障生成速度。
+ 模块化设计：代码结构清晰，便于阅读与二次开发。

## 训练入口与流程概览
:::color3
**简介：**本章解析 DAPO 算法训练任务的入口，并提供全局视角的训练流程图，帮助理解系统整体运作机制。

:::

:::color5
**<font style="color:#601bde;">1. 启动入口分析 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

以 `recipe/dapo/run_dapo_qwen2.5_32b_rollout_corr.sh` 脚本为例，该脚本用于启动 Qwen2.5 32B 模型的 DAPO 训练。核心执行命令如下：

```tsx
python3 -m recipe.dapo.main_dapo \
    data.train_files="${TRAIN_FILE}" \
    # ... 一大堆参数配置
```

实际的 Python 入口文件为 `recipe/dapo/main_dapo.py`。该文件包含一个被 `@hydra.main` 装饰的 `main` 函数，负责加载配置并调用 `run_ppo()` 启动训练。

:::color5
**<font style="color:#601bde;">2. 全局流程图</font>**

:::

下图展示了训练过程的全局视角：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770199038147-a323ba46-7b7a-46b1-baa9-0f10e6d19461.png)

## 初始化阶段详解
:::color3
**简介：**本章节详细拆解 `TaskRunner.run()` 中的初始化步骤，包括模型加载、Worker 选择、角色分配及 Trainer 的构建。

:::

:::color5
**<font style="color:#601bde;">1. 加载 Tokenizer 与 Processor </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

系统首先从远程路径（如 HDFS）下载模型并加载处理工具`processor` 主要用于多模态模型，纯文本模型通常为 `None`。

```python
local_path = copy_to_local(config.actor_rollout_ref.model.path)
tokenizer = hf_tokenizer(local_path, trust_remote_code=trust_remote_code)
processor = hf_processor(local_path, trust_remote_code=trust_remote_code, use_fast=True)
```

:::color5
**<font style="color:#601bde;">2. 选择 Worker 类型</font>**

:::

根据配置文件中的 `strategy` 字段，系统决定使用 FSDP 或 Megatron 作为训练后端。通常建议先使用 FSDP 跑通流程。

```python
if config.actor_rollout_ref.actor.strategy in {"fsdp", "fsdp2"}:
    from verl.workers.fsdp_workers import AsyncActorRolloutRefWorker, CriticWorker
elif config.actor_rollout_ref.actor.strategy == "megatron":
    from verl.workers.megatron_workers import AsyncActorRolloutRefWorker, CriticWorker
```

:::color5
**<font style="color:#601bde;">3. 配置角色（Role）与资源池</font>**

:::

`verl` 使用 `Role` 枚举区分不同的 Worker 角色，并通过 Ray 的 Resource Pool 管理 GPU 资源。

| **<font style="color:rgb(25, 27, 31);">Role</font>** | **<font style="color:rgb(25, 27, 31);">作用</font>** |
| :--- | :--- |
| <font style="color:rgb(25, 27, 31);">ActorRollout</font> | <font style="color:rgb(25, 27, 31);">Actor模型 + 推理引擎</font> |
| <font style="color:rgb(25, 27, 31);">Critic</font> | <font style="color:rgb(25, 27, 31);">Critic模型（如果用PPO的话）</font> |
| <font style="color:rgb(25, 27, 31);">RefPolicy</font> | <font style="color:rgb(25, 27, 31);">参考模型（计算KL用）</font> |
| <font style="color:rgb(25, 27, 31);">RewardModel</font> | <font style="color:rgb(25, 27, 31);">Reward模型（如果用模型来打分的话）</font> |


:::color5
**<font style="color:#601bde;">4. 加载 Reward Manager </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

`Reward Manager` 负责计算样本奖励，支持基于 LLM 的 Reward Model 或启发式规则。DAPO 算法使用 `DAPORewardManager`。

```python
reward_fn = load_reward_manager(
    config,
    tokenizer,
    0,
    max_resp_len=config.data.max_response_length,
    overlong_buffer_cfg=config.reward_model.overlong_buffer,
)
```

:::color5
**<font style="color:#601bde;">5. 初始化 Trainer</font>**

:::

最后，系统初始化 `RayDAPOTrainer` 并调用 `fit()` 开始训练循环。

```python
trainer = RayDAPOTrainer(
    config=config,
    tokenizer=tokenizer,
    processor=processor,
    role_worker_mapping=role_worker_mapping,
    resource_pool_manager=resource_pool_manager,
    ray_worker_group_cls=ray_worker_group_cls,
    reward_fn=reward_fn,
    val_reward_fn=val_reward_fn,
)
trainer.init_workers()
trainer.fit()
```

## 训练循环与推理生成机制
:::color3
**简介：**本章节深入分析模型训练的核心循环，重点阐述 `AgentLoopManager` 如何调度 vLLM 进行高效推理生成。

:::

:::color5
**<font style="color:#601bde;">1. 训练循环概览 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

正式训练环节包含：前向推理 ➡️ 计算 Loss (Reward) ➡️ 计算梯度并反向传播。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770199191772-a6d801a8-af0f-45c2-bba9-2c32326f1856.png)

:::color5
**<font style="color:#601bde;">2. 生成入口与架构 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

生成逻辑的入口位于 `RayDAPOTrainer.fit()`：

```python
with marked_timer("gen", timing_raw, "red"):
    gen_batch_output = self.async_rollout_manager.generate_sequences(gen_batch_output)
```

  
`AgentLoopManager` 的架构如下图所示：

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770202526351-29a89242-f6b5-460c-80f4-0c0db27b7d0f.png)

:::color5
**<font style="color:#601bde;">3. 生成流程详解 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

调用 `generate_sequences()` 后的执行步骤如下：

+ Step 1: 任务分发  
Batch 被切分给多个 Worker 并行处理。

```python
# verl/experimental/agent_loop/agent_loop.py 第942-949行
chunkes = prompts.chunk(len(self.agent_loop_workers))
outputs = ray.get([
    worker.generate_sequences.remote(chunk)
    for worker, chunk in zip(self.agent_loop_workers, chunkes, strict=True)
])
```

+ Step 2: Worker 处理  
Worker 实例化对应的 AgentLoop（如 `SingleTurnAgentLoop`）并运行。

```python
# verl/experimental/agent_loop/agent_loop.py 第506-515行
agent_loop = hydra.utils.instantiate(
    config=agent_loop_config,
    trainer_config=DictConfigWrap(config=self.config),
    server_manager=self.server_manager,
    tokenizer=self.tokenizer,
    processor=self.processor,
    dataset_cls=self.dataset_cls,
    dataset_config=self.config.data,
)
output: AgentLoopOutput = await agent_loop.run(sampling_params, **kwargs)
```

+ Step 3: 执行生成  
`SingleTurnAgentLoop` 处理多模态数据、应用 Chat Template，并调用 Server Manager。

```python
# verl/experimental/agent_loop/single_turn_agent_loop.py 第40-65行
async def run(self, sampling_params: dict[str, Any], **kwargs) -> AgentLoopOutput:
    messages = list(kwargs["raw_prompt"])
    
    # 1. 提取图片/视频（多模态）
    multi_modal_data = await self.process_vision_info(messages)
    
    # 2. 应用chat template，tokenize
    prompt_ids = await self.apply_chat_template(messages, ...)
    
    # 3. 调用推理引擎生成
    output = await self.server_manager.generate(
        request_id=uuid4().hex,
        prompt_ids=prompt_ids,
        sampling_params=sampling_params,
        ...
    )
    
    return AgentLoopOutput(...)
```



+ Step 4: vLLM 调用  
`AsyncLLMServerManager` 进行负载均衡（最小请求数策略 + Sticky Session），最终调用 vLLM 的 `AsyncLLMEngine` 生成 Token。

```python
# verl/experimental/agent_loop/agent_loop.py 第114-122行
async def generate(self, request_id, *, prompt_ids, sampling_params, ...):
    server = self._choose_server(request_id)  # 负载均衡
    output = await server.generate.remote(
        request_id=uuid4().hex,
        prompt_ids=prompt_ids,
        sampling_params=sampling_params,
        ...
    )
    return output
```





## 奖励计算体系
:::color3
**简介：**本章节解析 `DAPORewardManager` 的内部逻辑，包括分数计算、长度惩罚机制以及动态采样策略。

:::

:::color5
**<font style="color:#601bde;">1. 计算入口 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

奖励计算入口位于 `dapo_ray_trainer.py`：

```python
with marked_timer("reward", timing_raw, "yellow"):
    # ... 如果有reward model，先算rm_scores
    reward_tensor, reward_extra_infos_dict = compute_reward(new_batch, self.reward_fn)
    new_batch.batch["token_level_scores"] = reward_tensor
```

:::color5
**<font style="color:#601bde;">2. DAPORewardManager 逻辑</font>**

:::

`DAPORewardManager` 遍历 Batch 数据并执行以下关键操作：

1. 解码与提取：提取 Prompt、Response 和 Ground Truth。
2. 计算分数：调用配置的 `compute_score` 函数（支持自定义）。
3. 长度惩罚 (Overlong Penalty)：若回复超出预期长度，施加惩罚。

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770202662606-2b5719d3-2dd2-4e22-8b7a-ee07f1da47f3.png)

4. 赋值：由于 DAPO 是 outcome-based reward，奖励值被放置在序列的最后一个有效 Token 位置。

```python
def __call__(self, data: DataProto, return_dict: bool = False):
    reward_tensor = torch.zeros_like(data.batch["responses"], dtype=torch.float32)
    
    for i in range(len(data)):
        data_item = data[i]
        
        # 1. 提取prompt和response
        prompt_str = self.tokenizer.decode(valid_prompt_ids, skip_special_tokens=True)
        response_str = self.tokenizer.decode(valid_response_ids, skip_special_tokens=True)
        
        # 2. 获取ground truth
        ground_truth = data_item.non_tensor_batch["reward_model"]["ground_truth"]
        
        # 3. 调用compute_score计算分数
        result = self.compute_score(
            data_source=data_source,
            solution_str=response_str,
            ground_truth=ground_truth,
            extra_info=extra_info,
        )
        
        # 4. 处理overlong penalty
        if self.overlong_buffer_cfg.enable:
            exceed_len = valid_response_length - expected_len
            overlong_reward = min(-exceed_len / overlong_buffer_len * overlong_penalty_factor, 0)
            reward += overlong_reward
        
        # 5. 把reward放到最后一个token的位置
        reward_tensor[i, valid_response_length - 1] = reward
```

:::color5
**<font style="color:#601bde;">3. 动态采样 (Dynamic Sampling) </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

DAPO 会过滤掉同一 Prompt 下多个回复 Reward 相同的样本（因其 Advantage 计算时标准差为 0，无训练价值）。若过滤后样本不足，会触发补全生成。

```python
# dapo_ray_trainer.py 第244-267行
prompt_uid2metric_vals = defaultdict(list)
for uid, metric_val in zip(new_batch.non_tensor_batch["uid"], new_batch.non_tensor_batch[metric_name]):
    prompt_uid2metric_vals[uid].append(metric_val)

prompt_uid2metric_std = {}
for prompt_uid, metric_vals in prompt_uid2metric_vals.items():
    prompt_uid2metric_std[prompt_uid] = np.std(metric_vals)

# 只保留std > 0的
kept_prompt_uids = [
    uid for uid, std in prompt_uid2metric_std.items()
    if std > 0 or len(prompt_uid2metric_vals[uid]) == 1
]
```

## Rollout Correction 机制
:::color3
**简介：**探讨如何解决 vLLM 推理（BF16）与 FSDP 训练（FP32）精度不一致带来的概率分布差异问题。

:::

:::color5
**<font style="color:#601bde;">1. 问题背景 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

推理与训练环境的精度差异会导致概率分布偏离，影响训练稳定性。DAPO 引入 Rollout Correction 包含以下三种机制。

:::color5
**<font style="color:#601bde;">2. Truncated Importance Sampling (TIS)</font>**

:::

通过计算重要性权重并进行截断，防止权重过大导致模型崩溃。  
![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1770202696720-e1bfd347-7cd8-4731-9288-22180f54d50b.png)

```python
# verl/trainer/ppo/rollout_corr_helper.py 第367-371行
if rollout_is == "token":
    log_ratio_safe = torch.clamp(log_ratio, min=-SAFETY_BOUND, max=SAFETY_BOUND)
    rollout_is_weights = torch.exp(log_ratio_safe)
elif rollout_is == "sequence":
    # sequence-level: 整个序列的权重是各token权重的乘积
    log_ratio_sum = verl_F.masked_sum(log_ratio, response_mask, axis=-1)
    rollout_is_weights = torch.exp(log_ratio_sum_safe)
```

:::color5
**<font style="color:#601bde;">3. Rejection Sampling (RS) </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

直接丢弃重要性权重偏离过大的样本。

<font style="color:rgb(25, 27, 31);">支持三种粒度：</font>

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">token</font>`<font style="color:rgb(25, 27, 31);">: 每个token单独判断</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">sequence</font>`<font style="color:rgb(25, 27, 31);">: 整个序列的乘积</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">geometric</font>`<font style="color:rgb(25, 27, 31);">: 整个序列的几何平均</font>

```python
# verl/trainer/ppo/rollout_corr_helper.py 第164行
mask = (rollout_is_weights >= lower_threshold) & (rollout_is_weights <= upper_threshold)
```

:::color5
**<font style="color:#601bde;">4. Token Veto</font>**

:::

若某个 Token 的概率比极小（如 < 1e-4），表明分布差异巨大，直接丢弃整个序列。

```python
# verl/trainer/ppo/rollout_corr_helper.py 第664-677行
catastrophic_tokens = (log_ratio < log_veto_threshold) & response_mask.bool()
has_catastrophic = catastrophic_tokens.any(dim=-1, keepdim=True)
veto_mask = (~has_catastrophic).float()
modified_response_mask = modified_response_mask * veto_mask
```

  


## 优势计算与模型更新
:::color3
**简介：**本章节说明基于 GRPO 的 Advantage 计算逻辑以及最终的模型参数更新过程。

:::

:::color5
**<font style="color:#601bde;">1. Advantage 计算 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

DAPO 默认采用 GRPO 的计算方式：对同一 Prompt 的多个回复进行分组，计算组内标准化 Advantage。

```python
def compute_grpo_outcome_advantage(token_level_rewards, response_mask, index, epsilon=1e-6, norm_adv_by_std_in_grpo=True):
    scores = token_level_rewards.sum(dim=-1)  # 把token-level的reward求和得到sequence-level
    
    # 按group（同一个prompt的多个回复）分组
    id2score = defaultdict(list)
    for idx, uid in enumerate(index):
        id2score[uid].append(scores[idx])
    
    # 计算每个group的mean和std
    id2mean = {uid: torch.mean(torch.stack(s)) for uid, s in id2score.items()}
    id2std = {uid: torch.std(torch.stack(s)) for uid, s in id2score.items()}
    
    # 计算advantage: (score - mean) / std
    for idx, uid in enumerate(index):
        if norm_adv_by_std_in_grpo:
            scores[idx] = (scores[idx] - id2mean[uid]) / (id2std[uid] + epsilon)
        else:
            scores[idx] = scores[idx] - id2mean[uid]  # Dr.GRPO的做法
    
    return scores.unsqueeze(-1) * response_mask, scores.unsqueeze(-1) * response_mask
```

:::color5
**<font style="color:#601bde;">2. 模型更新</font>**

:::

计算完 Advantage 后，调用 Actor Worker 执行梯度更新。DAPO 通常采用非对称的 Clip 范围（如 `0.2` 到 `0.28`）以鼓励探索。

```python
# dapo_ray_trainer.py 第341-345行
if self.config.trainer.critic_warmup <= self.global_steps:
    with marked_timer("update_actor", timing_raw, "red"):
        actor_output = self.actor_rollout_wg.update_actor(batch)
    actor_output_metrics = reduce_metrics(actor_output.meta_info["metrics"])
    metrics.update(actor_output_metrics)
```

