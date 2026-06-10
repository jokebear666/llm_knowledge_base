# RLHF框架

<!-- source: yuque://zhongxian-iiot9/hlyypb/uw0xm8xuggddg0li -->

# OpenRLHF <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">自从O1和R1发布以来，社区涌现出了很多复现O1和R1的工作，大家都希望可以从0开始训练一个自己的</font>[<font style="color:rgb(9, 64, 142);">Reasoning Model</font>](https://zhida.zhihu.com/search?content_id=254658105&content_type=Article&match_order=1&q=Reasoning+Model&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。那么如果希望复现一下，自然需要一个合理的框架，因为RLHF至多需要同时有4个模型参与，所以对于大多数算法工作者而言（比如我）想要自己手搓一个框架实现这么多的功能往往是不太现实的，所以借助于一个完备、合适、恰当的框架是非常重要的。目前社区内知名度比较高、拓展性比较强的框架主要有3个：</font>

1. [OpnenRLHF](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF)
2. [VeRL](https://link.zhihu.com/?target=https%3A//github.com/volcengine/verl)
3. Ray
4. DeepSpeed-Chat

:::

:::color3
**简介：**<font style="color:rgb(31, 35, 40);">OpenRLHF 是一个基于 Ray、DeepSpeed 和 HF Transformers 构建的高性能 RLHF 框架：</font>

<font style="color:rgb(31, 35, 40);">更多细节请参考 </font>[PPT](https://docs.google.com/presentation/d/1JRhB1d7csofx0PIZBmfyBdMluxNd5JLPpUHrrvVhGnk/edit?usp=sharing)<font style="color:rgb(31, 35, 40);"> | </font>[技术报告](https://arxiv.org/abs/2405.11143)<font style="color:rgb(31, 35, 40);"> | </font>[使用文档](https://openrlhf.readthedocs.io/)

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)

**paper：**[**https://arxiv.org/pdf/2405.11143**](https://arxiv.org/pdf/2405.11143)

**使用文档：**[**https://openrlhf.readthedocs.io/en/latest/**](https://openrlhf.readthedocs.io/en/latest/)

**参考：**[**图解OpenRLHF中基于Ray的分布式训练流程**](https://zhuanlan.zhihu.com/p/12871616401)**  **[**浅析以 OpenRLHF 为代表的 post-training 系统的计算流程**](https://zhuanlan.zhihu.com/p/16370000391) <font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color5
**<font style="color:#601BDE;">1.创新点 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(31, 35, 40);">简单易用</font>**<font style="color:rgb(31, 35, 40);">: OpenRLHF 是目前可用的最简单的高性能 RLHF 库之一，无缝兼容 Huggingface 模型和数据集。</font>
+ **<font style="color:rgb(31, 35, 40);">高性能</font>**<font style="color:rgb(31, 35, 40);">: RLHF 训练中 80% 的时间用于样本生成阶段。得益于使用 Ray, Packing Samples 以及 vLLM 生成加速的能力，OpenRLHF 的性能是极致优化的 DeepSpeedChat with Hybrid Engine 的3~4倍以上。</font>
+ **<font style="color:rgb(31, 35, 40);">分布式 RLHF</font>**<font style="color:rgb(31, 35, 40);">: OpenRLHF 使用 Ray 将 Actor、Reward、Reference 和 Critic 模型分布到不同的 GPU 上，同时将 Adam 优化器放在 CPU 上。这使得使用多个 A100 80G GPU 和 vLLM 可以全面微调超过 70B+ 的模型 以及在多个 24GB RTX 4090 GPU 上微调 7B 模型。</font>
+ **<font style="color:rgb(31, 35, 40);">Hybrid Engine</font>**<font style="color:rgb(31, 35, 40);">: OpenRLHF 还支持 Hybrid engine，所有训练引擎和推理引擎共用 GPU 来避免资源闲置。</font>
+ **<font style="color:rgb(31, 35, 40);">PPO 实现技巧</font>**<font style="color:rgb(31, 35, 40);">: 集成了 PPO 的实现技巧以提高训练稳定性，详情参考 </font>[知乎](https://zhuanlan.zhihu.com/p/622134699)<font style="color:rgb(31, 35, 40);"> 和 </font>[Notion blog](https://hijkzzz.notion.site/rlhf-implementation-tricks?v=158d9a33ecc98132bf9e000c39227361)<font style="color:rgb(31, 35, 40);">.</font>

:::color5
**<font style="color:#601BDE;">2.PPO支持矩阵 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743417876145-59b7fe89-e01c-467d-8bac-aacb0e9afe1c.png)

:::color5
**<font style="color:#601BDE;">3.Scheduling Optimization 调度优化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

OpenRLHF的射线架构（Ray）。RLHF中的四个模型分布在不同的Ray的GPU，也可以自由合并或卸载以节省GPU。vLLM用于加速 actor生成。OpenRLHF使用NVIDIA Collective Communications Library（NCCL）将ZeRO引擎的权重同步到vLLM引擎。

我们的调度器设计允许使用Ray和DeepSpeed进行灵活的模型合并或卸载策略。例如，可以**<font style="color:#74B602;">合并actor,reference或critic,reward模型以节省GPU资源</font>**。除了高度可定制的算法实现的好处外，调度器还通过优化GPU来提高整体训练性能。下一节将讨论更多细节，但调度器优化是进一步提高效率的基石。

 Scheduling Optimization

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743417273664-d8eea981-9ec4-4911-89bf-e68429cc6c19.png)

:::color5
**<font style="color:#601BDE;">2.RLHF生成阶段 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

OpenRLHF的设计支持灵活放置具有各种算法实现的多个模型。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743672338227-214cd0c0-ddd2-41ae-8ce0-c348f55ecb13.png)

:::color5
**<font style="color:#601BDE;">3.RLHF学习阶段 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

OpenRLHF安排了两个可学习的模型，以最大限度地提高整体训练吞吐量

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743672330560-29bbad45-e8da-4658-903d-501eb44bb9e3.png)

:::color5
**<font style="color:#601BDE;">3.便捷使用 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

为了用户友好，OpenRLHF为支持的算法提供了一键式可训练脚本，与Hugging Face库完全兼容，用于指定模型和数据集名称或路径。以下是70B型号在16台A100上的RLHF训练配置：	

```python
pip install openrlhf[vllm]

ray start --head --node-ip-address 0.0.0.0
ray job submit -- python3 openrlhf.cli.train_ppo_ray \
    --ref_num_gpus_per_node 4 \ # Number of GPUs for Ref model
    --reward_num_gpus_per_node 4 \ # Number of GPUs for RM
    --critic_num_gpus_per_node 4 \ # Number of GPUs for Critic
    --actor_num_gpus_per_node 4 \ # Number of GPUs for Actor
    --vllm_num_engines 4 \ # Number of vLLM engines
    --vllm_tensor_parallel_size 2 \ # vLLM Tensor Parallel Size
    --colocate_actor_ref \ # Colocate Actor and Ref
    --colocate_critic_reward \ # Colocate Critic and RM
    --ref_reward_offload \ # Offload Ref and RM
    --pretrain {HF Model name or path after SFT} \
    --reward_pretrain {HF Reward model name or path} \
    --zero_stage 3 \ # DeepSpeed ZeRO stage
    --bf16 \ # Enable BF16
    --init_kl_coef 0.01 \ # KL penalty coefficient
    --prompt_data {HF Prompt dataset name or path} \
    --input_key {Prompt dataset input key}
    --apply_chat_template \ # Apply HF tokenizer template
    --normalize_reward \ # Enable Reward Normalization
    --adam_offload \ # Offload Adam Optimizer
    --flash_attn \ # Enable Flash Attention
    --save_path {Model output path}
```

:::color5
**<font style="color:#601BDE;">5.不同框架对比 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743417239914-442c429b-1989-4049-b33b-3b013d77af79.png)

**RLHF框架比较**：OpenRLHF支持使用Ray的多奖励模型，并使用vLLM加速流行的HuggingFace模型。与Hugging Face库的兼容性确保了该框架的用户友好性。

**Limits**：DSChat的HybridEngine仅支持有限范围的模型架构，例如[Deepspeed](https://github.com/microsoft/DeepSpeed/issues/4954.)相比之下，OpenRLHF支持所有主流架构，包括使用DeepSpeed和vLLM的MoE，请参阅文档[vLLM教程](https://docs.vllm.ai/en/latest/models/supported_)

## <font style="color:rgb(25, 27, 31);">OpenRLHF中基于Ray的分布式训练流程 </font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color1
**简介：**<font style="color:rgb(25, 27, 31);">本文着重分析</font>[OpenRLHF](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF)<font style="color:rgb(25, 27, 31);">中的</font>[<font style="color:rgb(9, 64, 142);">PPO-Ray</font>](https://zhida.zhihu.com/search?content_id=251597453&content_type=Article&match_order=1&q=PPO-Ray&zhida_source=entity)<font style="color:rgb(25, 27, 31);">训练架构设计，共分成五块：</font>

1. **<font style="color:rgb(25, 27, 31);">为什么用Ray</font>**
2. **<font style="color:rgb(25, 27, 31);">使用图例抽象出整体训练流程</font>**
3. **<font style="color:rgb(25, 27, 31);">Ray核心知识速过</font>**
4. **<font style="color:rgb(25, 27, 31);">使用图例进一步抽象出核心代码细节，包括：</font>**
    - <font style="color:rgb(25, 27, 31);">训练入口</font>
    - <font style="color:rgb(25, 27, 31);">部署PPO-Actor/Ref/Critic/RM实例</font>
    - <font style="color:rgb(25, 27, 31);">部署vllm_engines实例</font>
    - <font style="color:rgb(25, 27, 31);">PPO-Actor与vllm_engines之间的通讯</font>
    - <font style="color:rgb(25, 27, 31);">PPO-Actor/Critic训练</font>

**<font style="color:rgb(25, 27, 31);">5. RLHF-PPO算法细节介绍 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)

**paper：**[**https://arxiv.org/pdf/2405.11143**](https://arxiv.org/pdf/2405.11143)

**使用文档：**[**https://openrlhf.readthedocs.io/en/latest/**](https://openrlhf.readthedocs.io/en/latest/)

**参考：**[**https://zhuanlan.zhihu.com/p/12871616401**](https://zhuanlan.zhihu.com/p/12871616401)

:::

### 为什么适用Ray <font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介：对于通常的rlhf框架，在训练时会在单卡上</font>****<font style="color:#117CEE;">同时部署actor/ref/reward/critic四类模型</font>**<font style="color:rgb(25, 27, 31);">，这种单一的部署方式可能存在如下问题：</font>

+ **<font style="color:rgb(25, 27, 31);">难以突破单卡显存的限制。</font>**
+ **<font style="color:rgb(25, 27, 31);">无法实现更多的并行计算</font>**<font style="color:rgb(25, 27, 31);">。例如在收集exp阶段，拿到</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">(prompt, responses)</font>`<font style="color:rgb(25, 27, 31);">结果的四类模型其实可以做并行推理；在训练阶段，拿到exp的actor和critic也可以做并行训练。但受到单卡显存等因素影响，通常的rlhf框架中使用更多的是串行。</font>
+ **<font style="color:rgb(25, 27, 31);">无法独立优化训练和推理过程</font>**<font style="color:rgb(25, 27, 31);">。诸如vllm之类的框架，是可以用来提升actor生成</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">(prompt, responses)</font>`<font style="color:rgb(25, 27, 31);">的速度的，而对于其它模型，我们也可能会视算法需要有不同的推理需求。因此我们期望能更加灵活地设计训练、推理过程</font>

:::

:::color5
**<font style="color:#601BDE;">1.Ray的作用 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">而解决以上问题，</font>**<font style="color:rgb(25, 27, 31);">需要开发者能设计一套较为灵活的分布式计算框架</font>**<font style="color:rgb(25, 27, 31);">，能够实现资源定制化分配、分布式调度、节点内外通信等目标，同时相关的代码不能太复杂，能够让使用者更专注于算法部分的研发。</font>**<font style="color:rgb(25, 27, 31);">而</font>****<font style="color:#74B602;">Ray天然可以帮我们做这件事：我们只需提供自己的资源分配方案，告诉Ray我想怎么部署这些模型</font>****<font style="color:rgb(25, 27, 31);">，不管是分开还是合并部署Ray都可以帮我们实现。而复杂的调度策略和通信等事项，就由Ray在后台去做，我们无需关心这个过程。</font>**

**<font style="color:rgb(25, 27, 31);"></font>**

### <font style="color:rgb(25, 27, 31);">独立部署 </font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
<font style="color:rgb(25, 27, 31);">简介：这个例子展示如何完全独立部署各个模型。假设我们有3台node，每台node 8张卡。以下展示其中一种可行的部署方式</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743750469184-c8871147-6057-4626-aed4-55ba604d5adc.jpeg)

:::color5
**<font style="color:#601BDE;">1.部署4类模型 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

在这个例子中，4类模型分开部署在node0和node1上。

以Actor为例，它分布在“node0的gpu0/1 + node1的gpu0/1”上。

**这一点是由Ray实现的：我们自己定制化资源分配的方案，进而管控模型的分配方式。**

**而当实际训练时，我们还可进一步引入**[**<font style="color:rgb(9, 64, 142);">Deepspeed zero</font>**](https://zhida.zhihu.com/search?content_id=251597453&content_type=Article&match_order=1&q=Deepspeed+zero&zhida_source=entity)**做优化**：以Actor为例，上图中的4个Actor构成zero中的数据并行组（world_size = 4），根据zero的配置，我们可以在这4张卡间做optimizer/gradients/weights的切片。

:::color5
**<font style="color:#601BDE;">2.部署vllm_engines </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">前文说过，对于Actor模型，在收集exp阶段我们可以采用</font>**<font style="color:#74B602;">vllm之类的框架加速</font>**`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">(prompt, responses)</font>`<font style="color:rgb(25, 27, 31);">的生成。在这个例子中：</font>

+ <font style="color:rgb(25, 27, 31);">1个vllm_engine维护着一个vllm实例，每个vllm实例下维护一个完整的Actor模型，这里我们还假设一个vllm实例按tp_size = 2的方法切割模型。</font>
+ <font style="color:rgb(25, 27, 31);">在node2中，共有4个vllm_engines（也即4个vllm实例），</font>**<font style="color:rgb(25, 27, 31);">这种分配方式是通过Ray实现的。而每个vllm实例内的分布式推理则是由vllm自己管控。</font>**

:::color5
**<font style="color:#601BDE;">3.Actor与vllm_engines之间的通讯 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">我们称：</font>

+ <font style="color:rgb(25, 27, 31);">vllm_engines中的actor为vllm_actor</font>
+ <font style="color:rgb(25, 27, 31);">node0/1中的actor为ds_actor</font>

<font style="color:rgb(25, 27, 31);">在整个训练过程中，</font>**<font style="color:#74B602;">vllm_actor需要和ds_actor保持权重一致</font>**<font style="color:rgb(25, 27, 31);">。我们来看这个一致性是如何维护的：</font>

1. **<font style="color:rgb(25, 27, 31);">初始化阶段</font>**

<font style="color:rgb(25, 27, 31);">假设</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pretrain</font>`<font style="color:rgb(25, 27, 31);">路径下存储着sft模型，当我们首次开始训练时，ds_actor和vllm_actor都直接从</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pretrain</font>`<font style="color:rgb(25, 27, 31);">中加载权重，两者互不影响，独立加载。  
</font>**<font style="color:rgb(25, 27, 31);">2. 训练中</font>**

<font style="color:rgb(25, 27, 31);">在1个step结束后，ds_actor需要把更新后的权重broadcast给vllm_actor，具体步骤如下：</font>

+ **<font style="color:rgb(25, 27, 31);">首先，对</font>**`**<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ds_rank0 + all_vllm_ranks</font>**`**<font style="color:rgb(25, 27, 31);">创建一个通讯组</font>**<font style="color:rgb(25, 27, 31);">。在本例中:</font>
    - <font style="color:rgb(25, 27, 31);">node0/gpu0上的actor是ds_rank0</font>
    - <font style="color:rgb(25, 27, 31);">node2中所有的gpu构成all_vllm_ranks。</font>
    - <font style="color:rgb(25, 27, 31);">我们就是把这两者纳入一个通讯组内，这个通讯组的world_size = 9。如果我们多一台node3来做vllm_engines，那么这个通讯组的world_size = 17，以此类推。</font>
+ **<font style="color:rgb(25, 27, 31);">假设我们使用ds_zero1/2</font>**<font style="color:rgb(25, 27, 31);">，则ds_rank0上维护的是完整的actor权重，我们把ds_rank0上的权重broadcast到每一个vllm_rank，如有设置tp，vllm会自动帮我们完整接下来的模型切割。</font>
+ **<font style="color:rgb(25, 27, 31);">假设我们使用ds_zero3</font>**<font style="color:rgb(25, 27, 31);">，则ds_rank0上只维护部分actor权重，那么：</font>
    - <font style="color:rgb(25, 27, 31);">ds_rank0先从ds_actor组内all gather回完整的模型权重</font>
    - <font style="color:rgb(25, 27, 31);">再将完整的模型权重brocast给每一个vllm_rank</font>

**<font style="color:rgb(25, 27, 31);">3. 从检查点恢复训练（load_checkpoint）</font>**

<font style="color:rgb(25, 27, 31);">当我们需要从检查点恢复训练时，ds_actor会负责把检查点权重broadcast给vllm_actor，方式同2。</font>

:::color5
**<font style="color:#601BDE;">4.整体运行流程 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743750469184-c8871147-6057-4626-aed4-55ba604d5adc.jpeg)

<font style="color:rgb(25, 27, 31);">结合流程图，我们来简述一下整体运作流程。</font>

+ <font style="color:rgb(25, 27, 31);">首先明确一些表达。例如，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">node0中的Actor0/1 + node1中的Actor0/1</font>`<font style="color:rgb(25, 27, 31);">属于相同的数据并行组，所以接下来我们会用它们在dp组中的rank来描述它们，也就是分别改称Actor0/1/2/3。对于其余三类模型也是同理。</font>
+ <font style="color:rgb(25, 27, 31);">接着进行分组：</font>
    - `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Actor0 / Ref0 / RM0 / Critic0 / vllm_engine0</font>`<font style="color:rgb(25, 27, 31);">为一组</font>
    - `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Actor1 / Ref1 / RM1 / Critic1 / vllm_engine1</font>`<font style="color:rgb(25, 27, 31);">为一组</font>
    - `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Actor2 / Ref2 / RM2 / Critic2 / vllm_engine2</font>`<font style="color:rgb(25, 27, 31);">为一组</font>
    - `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">Actor3 / Ref3 / RM3 / Critic3 / vllm_engine3</font>`<font style="color:rgb(25, 27, 31);">为一组</font>
+ **<font style="color:rgb(25, 27, 31);">你可以把每一组想象成原来的一张单卡，那么它的作用就是负责一个micro_batch的训练，</font>**<font style="color:rgb(25, 27, 31);">这样我们就能大致想象到它们之间是如何配合运作的了。需要注意的是，在我们的例子中，这些实例都是一一对应的（各自有4个实例），但在实际操作中，根据不同用户的资源配置，不一定存在这个一一对应的关系。例如你可能用4卡部署Actor，2卡部署Critic，8个vllm_engines...以此类推。</font>**<font style="color:rgb(25, 27, 31);">不管怎样，我们应该尽量在处理micro_bathes的各个组间均匀分配负载，在代码里相关的操作如下：</font>**
    - [为每个actor分配其对应的critic/reward/ref，并启动每个分组的训练](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/launcher.py#L278-L299)
    - [为每个actor分配对应的vllm_engine，并使用vllm_engine进行推理](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ppo_utils/experience_maker.py#L627)



## 共同部署 <font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">同样，我们可以按照自己的需求，选择性地在单卡上部署不同种类的模型，例如下面的例子中，actor/ref共部署，critic/reward共部署，图例如下，运作流程和独立部署相似，这里不赘述：</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743751458976-a6dd958d-e303-4c89-a188-fbb9f4b52b6c.jpeg)

## Ray的核心概念 <font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">在传统的编程中，我们经常使用到2个核心概念：function和class</font>**<font style="color:rgb(25, 27, 31);">。而在分布式系统中，我们希望可以分布式并行执行这些function和class。</font>**<font style="color:#ED740C;">Ray使用装饰器</font>**`**<font style="color:#ED740C;background-color:rgb(248, 248, 250);">@ray.remote</font>**`**<font style="color:#ED740C;">来将function包装成</font>****<u><font style="color:#ED740C;">Ray task</font></u>****<font style="color:#ED740C;">，将class包装成</font>****<u><font style="color:#ED740C;">Ray actor</font></u>****<font style="color:#ED740C;">，包装过后的结果可以在远端并行执行</font>**<font style="color:rgb(25, 27, 31);">。接下来我们就来细看task/actor（注意，这里的actor是ray中的概念，不是rlhf-ppo中actor模型的概念）</font>

:::

:::color5
**<font style="color:#601BDE;">1.Ray Task </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
import ray
ray.init()

@ray.remote
def f(x):
    return x * x
# ===================================================================
# 创建driver进程，运行main
# ===================================================================
if __name__ == "__main__":
    # ===================================================================
    # 创建4个worker进程，可以在远端并行执行。
    # 每执行1次f.remote(i)，会发生以下事情：
    # - 创建1个worker进程，它将在远端执行函数f(i)
    # - 在driver进程上立刻返回一个引用（feature）,该引用指向f(i)远程计算的结果
    # ===================================================================
    futures = [f.remote(i) for i in range(4)]
    # ===================================================================
    # 阻塞/同步操作：等待4个worker进程全部计算完毕
    # ===================================================================
    results = ray.get(futures)) 
    # ===================================================================
    # 确保全部计算完毕后，在driver进程上print结果
    # ===================================================================
    print(f"The final result is: {results}") # [0, 1, 4, 9]
```

:::color5
**<font style="color:#601BDE;">2.Ray Actor </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
import ray
ray.init()

@ray.remote
class Counter(object):
    def __init__(self):
        self.x = 0
    
    def inc(self):
        self.x += 1
    
    def get_value(self):
        return self.x

# ===================================================================
# 创建driver进程，运行main
# ===================================================================
if __name__ == "__main__":
    # ===================================================================
    # 创建1个worker进程，具体做了以下事情：
    # - 在远端创建Counter实例
    # - 在driver端即刻返回对该实例的引用c（称为actor handler）
    # - 我们可以在Ray集群的任何节点上传递和使用这个actor handler。即在任何地方，
    #   我们可以通过c来invoke它对应Counter实例下的各种方法
    # ===================================================================
    c = Counter.remote()

    # ===================================================================
    # 阻塞/同步：通过c来invoke远端Counter实例的get_value()方法，并确保方法执行完毕。
    # 执行完毕后才能接着执行driver进程上剩下的代码操作
    # ===================================================================
    print(ray.get(c.get_value.remote()))  # 0
    
    # ===================================================================
    # Increment the counter twice and check the value again.
    # 道理同上，不赘述
    # ===================================================================
    c.inc.remote()
    c.inc.remote()
    print(ray.get(c.get_value.remote()))  # 2
```

:::color5
**<font style="color:#601BDE;">3.Ray Cluster架构简图 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">现在我们已经通过以上例子对Ray运作原理有了一些基本感知，我们来进一步探索一个</font>[ray cluster的组成](https://link.zhihu.com/?target=https%3A//docs.google.com/document/d/1tBw9A4j62ruI5omIJbMxly-la5w4q_TjyJgJL_jN2fI/preview%3Ftab%3Dt.0)<font style="color:rgb(25, 27, 31);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743752367906-fd4af6a4-9c42-481e-829e-812b0b063371.png)

<font style="color:rgb(145, 150, 161);">图片来自Ray官方2022年白皮书，访问需梯子：https://docs.google.com/document/d/1tBw9A4j62ruI5omIJbMxly-la5w4q_TjyJgJL_jN2fI/preview?tab=t.0#heading=h.iyrm5j2gcdoq</font>

+ <font style="color:rgb(25, 27, 31);">在一个ray cluster中，会有一台head node和若干worker node</font>
+ **<font style="color:rgb(25, 27, 31);">Driver process</font>**<font style="color:rgb(25, 27, 31);">是一种特殊的worker process，它一般负责执行top-level application（例如python中的</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">__main__</font>`<font style="color:rgb(25, 27, 31);">），它负责提交想要执行的任务，但却不负责实际执行它们。理论上driver process可以运行在任何一台node内，但默认创建在head node内。</font>
+ **<font style="color:rgb(25, 27, 31);">Worker process</font>**<font style="color:rgb(25, 27, 31);">负责实际任务的执行（执行Ray Task或Ray Actor中的方法）。</font>
+ **<font style="color:rgb(25, 27, 31);">每台node中还有一个Raylet process</font>**<font style="color:rgb(25, 27, 31);">，它负责管控每台node的调度器和共享资源的分配。</font>
+ **<font style="color:rgb(25, 27, 31);">Head node中的GCS</font>**<font style="color:rgb(25, 27, 31);">将会负责维护整个ray cluster的相关服务。</font>

## 代码细节 <font style="color:#D22D8D;">（by草莓师姐）</font>
:::color1
**简介：**<font style="color:rgb(25, 27, 31);">本章将解读更多代码实践上的重要细节。我们通过图例的方式抽象出代码运行的过程，而具体代码可参考文中给出的相关链接</font>

:::

### 训练入口 <font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介</font>**<font style="color:rgb(25, 27, 31);">：在main中我们启动了driver进程，并执行训练函数</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">train(args)</font>`<font style="color:rgb(25, 27, 31);"></font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[ppo_ray相关的训练入口](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/cli/train_ppo_ray.py)

:::

:::color5
**<font style="color:#601BDE;">1.创新点 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在main中我们启动了driver进程，并执行训练函数</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">train(args)</font>`<font style="color:rgb(25, 27, 31);">，这里主要做了如下几件事：</font>

+ **<font style="color:rgb(25, 27, 31);">在ray集群上部署Actor/Ref/Critic/RM实例</font>**
+ **<font style="color:rgb(25, 27, 31);">在ray集群上部署vllm_engines实例</font>**
+ **<font style="color:rgb(25, 27, 31);">配置Actor和vllm_engines之间的通讯，用于传递权重</font>**
+ **<font style="color:rgb(25, 27, 31);">训练Actor和Critic模型</font>**

<font style="color:rgb(25, 27, 31);">我们依次来解读这几个关键步骤。</font>**<font style="color:rgb(25, 27, 31);">同时为了在表述上消除歧义，我们接下来谈到“Actor”时，会使用</font>**[**<font style="color:rgb(9, 64, 142);">Ray-Actor</font>**](https://zhida.zhihu.com/search?content_id=251597453&content_type=Article&match_order=1&q=Ray-Actor&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">和PPO-Actor来做区分</font>**<font style="color:rgb(25, 27, 31);">，从之前的介绍中可知，Ray-Actor是指部署在Ray集群中的远端class，PPO-Actor/Ref/Critic/RM都属于Ray-Actor。</font>

### <font style="color:rgb(25, 27, 31);">部署Actor/Ref/Critic/RM实例</font>
:::color5
**<font style="color:#601BDE;">1.独立部署 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">我们以PPO-Actor为例，看代码是如何将其部署到Ray集群上的。</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743752642136-62de63d7-e2cd-40d3-9a4b-f3bd5b7487f9.jpeg)

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">PPORayActorGroup</font>`<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">创建在driver进程上，可将它理解成一种部署方案，专门负责部署PPO中的4类模型</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">PPORayActorGroup</font>`<font style="color:rgb(25, 27, 31);">中维护着</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">self._actor_handlers</font>`<font style="color:rgb(25, 27, 31);">，它是一个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">List[ray.actor.ActorHandle]</font>`<font style="color:rgb(25, 27, 31);">，列表中每个元素表示某个远端Ray-Actor的引用，而这个远端Ray-Actor可以是PPO-Actor/Ref/Critic/RM实例。如前文所说，我们可以在ray集群中的任何位置调用这个handler，来对相应的远端Ray-Actor执行操作。</font>
+ <font style="color:rgb(25, 27, 31);">在本例中，我们创建了4个Ray-Actor（1个master-actor，3个worker_actor）。每个Ray-Actor都运行在一个worker进程中。在创建Ray-Actor的同时，我们也会去修改worker进程的环境变量。后续当我们在这些worker进程中启动ds_zero相关的分布式配置时，ds会读取这些环境变量信息，这样我们就知道哪些Ray-Actor同时又构成ds中的数据并行组。</font>
+ <font style="color:rgb(25, 27, 31);">使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">PPORayActorGroup</font>`<font style="color:rgb(25, 27, 31);">部署模型实例的代码如下：</font>

```python
model = PPORayActorGroup(
        # 为部署该模型的全部实例，我们想用多少台node，例如本例中为2
        args.actor_num_nodes,
        # 为部署该模型的全部实例，我们每台node上想用多少gpu，例如本例中为2
        args.actor_num_gpus_per_node,
        # Actor/Critic/Reward/ReferenceRayActor
        ActorModelRayActor, 
        # pg可理解为，在ray cluster中锁定/预留一片资源，然后只在这片资源上部署该模型全部实例。
        # （pg维护在Head Node的GCS上，参见3.3）
        # 例如本例中，pg锁定的资源为node0 gpu0/1, node1 gpu0/1，
        # 我们只在上面部署ActorModelRayActor全部实例
        pg=pg,
        # 当我们在pg指向的预留资源中分配模型实例时，再进一步指定每个实例占据一张gpu的多少部分
        # 等于1说明每个实例占满一张gpu，即“非共同部署”
        # 小于1说明每个实例只占部分gpu，即“共同部署”，例如PPO-Actor/Ref共同部署在一张卡上
        num_gpus_per_actor=0.75 if pg else 1,
    )
```

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">创建在远端worker进程上，是Ray-Actor</font>**<font style="color:rgb(25, 27, 31);">。它包含了设置ds_zero分布式环境、加载模型权重、数据集准备、optimizer/scheduler准备、训练等一系列操作。</font>[PPORayActorGroup代码](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/launcher.py%23L143)

:::color5
**<font style="color:#601BDE;">2.共同部署 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">我们以PPO-Actor为例，看代码是如何将其部署到Ray集群上的。</font>  
 ![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743753643309-b403ae9c-2bdd-4670-a427-8133d8b18043.jpeg)

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">PPORayActorGroup</font>`<font style="color:rgb(25, 27, 31);">：在driver进程上创建2个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">PPORayActorGroup</font>`<font style="color:rgb(25, 27, 31);">，分别管理PPO-Actor，PPO-Ref的部署</font>
+ <font style="color:rgb(25, 27, 31);">使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">actor_model = PPORayActorGroup(..., pg = pg, num_gpus_per_actor=0.75)</font>`<font style="color:rgb(25, 27, 31);">创建PPO-Actor部署方案实例；使用</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ref_model = PPORayActorGroup(..., pg = pg, num_gpus_per_actor=0.25)</font>`<font style="color:rgb(25, 27, 31);">创建PPO-Ref部署方案实例</font>
+ <font style="color:rgb(25, 27, 31);">这里，两个方案实例使用的pg都是同一个，即这个pg都指向“1台node，每台node 8张卡”这片预留好的资源。</font>
+ `**<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">num_gpus_per_actor = 0.75/0.25</font>**`**<font style="color:rgb(25, 27, 31);">是一种创建trick</font>**<font style="color:rgb(25, 27, 31);">，虽然我们的最终目的是为了让PPO-Actor和PPO-Ref对半分一张卡（对半=共享，不是指显存上对半分），但是：</font>
    - <font style="color:rgb(25, 27, 31);">假设设置为0.5，当我们实际部署</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">时，Ray先在单卡上部署1个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">实例，当它准备部署第二个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">实例时，它发现由于每个实例只占0.5块卡，因此完全可以把第2个实例接着第1个实例在同一张卡上部署，这样就导致最终无法让PPO-Actor和PPO-Ref共享一张卡</font>
    - <font style="color:rgb(25, 27, 31);">假设设置0.75，当我们在单卡上部署完1个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">实例后，ray发现单卡剩下的空间不足以部署第2个</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">实例，所以就会把第二个实例部署到别的卡上，这样最终实现PPO-Actor和PPO-Ref共享一张卡</font>
    - <font style="color:rgb(25, 27, 31);">所以，这个设置是为了达到不同类型模型的实例共享一张卡的目的，而并非真正指模型实际占据的单卡显存空间。</font>
+ <font style="color:rgb(25, 27, 31);">最后，在这一步中，我们对全部</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">ActorModelRayActor</font>`<font style="color:rgb(25, 27, 31);">共创建8个worker进程，对全部</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">RefenreceModelRayActor</font>`<font style="color:rgb(25, 27, 31);">共创建8个worker进程，一共创建16个工作进程。</font>

[PPORayActorGroup代码](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/launcher.py#L143)



### <font style="color:rgb(25, 27, 31);">部署vllm_engines实例 </font><font style="color:#D22D8D;">（by草莓师姐）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743753742147-6116f216-34c2-4597-a859-d10762127093.jpeg)

+ `<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">create_vllm_engines</font>`<font style="color:rgb(25, 27, 31);">：在driver端，我们通过运行该函数来创建</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">vllm_engines</font>`<font style="color:rgb(25, 27, 31);">，过程相似于4.2节中的介绍，信息都在图中，这里不赘述。</font>
+ `[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">LLMRayActor</font>](https://zhida.zhihu.com/search?content_id=251597453&content_type=Article&match_order=1&q=LLMRayActor&zhida_source=entity)`<font style="color:rgb(25, 27, 31);">：worker端Ray-Actor，它主要是把vllm实例进行了一些包装，包装的目的是为了让ds_rank0和all vllm ranks间可以进行PPO-Actor的权重通讯（参见2.1（3））</font>
+ <font style="color:rgb(25, 27, 31);">在上面的例子中，我们会创建4个worker进程（不占gpu资源，只占cpu资源），用于运行管理4个vllm_engine。</font>**<font style="color:rgb(25, 27, 31);">在每个worker进程内，vllm实例还会创建属于自己的worker进程做分布式运行</font>**<font style="color:rgb(25, 27, 31);">（这些worker进程会实际占据gpu资源）。</font>

<font style="color:rgb(83, 88, 97);">相关代码参见：  
</font>[vllm_engine代码](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/vllm_engine.py)

[vllm_worker_wrap代码](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/vllm_worker_wrap.py)



### <font style="color:rgb(25, 27, 31);">PPO-Actor/Critic Training </font><font style="color:#D22D8D;">（by草莓师姐）</font>
![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743753850182-510d520e-f165-4d3f-80b8-c34110547c80.jpeg)

<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">正如2.1（4）中所说，我们将部署在ray集群上的PPO-Actor/Ref/Critic/RM实例们进行分组，每组分别负责一份micro-batch的训练，</font>**<font style="color:rgb(25, 27, 31);">上图刻画了某个组内的训练流程。一组内的训练流程发起自PPO-Actor实例（fit方法），注意不同颜色的worker0表示的是不同工作进程。</font>**<font style="color:rgb(25, 27, 31);">共分成如下步骤执行。</font>

<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">Step1：发送prompts，并从vllm_engine上收集(prompt, response)。</font>**

<font style="color:rgb(83, 88, 97);">代码参见：</font>[experience_maker](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ppo_utils/experience_maker.py#L627)<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">Step2：从Ref/Reward/Critic上收集并处理exps</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(83, 88, 97);">代码参见：</font>[experience_maker](https://github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ppo_utils/experience_maker.py#L492)<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">Step3: 确保将处理后的exps传送给Critic，并行执行Actor和Critic的训练</font>**

<font style="color:rgb(83, 88, 97);">将exps传送给Critic：</font>[experience_maker](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ppo_utils/experience_maker.py%23L470)<font style="color:rgb(83, 88, 97);">  
</font><font style="color:rgb(83, 88, 97);">Actor训练：</font>[ppo_actor](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/ppo_actor.py%23L125)<font style="color:rgb(83, 88, 97);">  
</font><font style="color:rgb(83, 88, 97);">Critic训练：</font>[ppo_actor](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/ppo_actor.py%23L122)<font style="color:rgb(83, 88, 97);">  
</font><font style="color:rgb(83, 88, 97);">我们在Actor实例所在的worker进程上出发Actor和Critic的训练。以上代码只给出了训练入口，更多细节需要顺着入口去阅读。</font><font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">Step4：vllm_engine权重更新。</font>**

<font style="color:rgb(83, 88, 97);">代码参见：</font>[ppo_actor](https://link.zhihu.com/?target=https%3A//github.com/OpenRLHF/OpenRLHF/blob/bb46342711a203c457df2fbca5967fd0549557e0/openrlhf/trainer/ray/ppo_actor.py%23L130)  
 



