# 大模型训练框架

<!-- source: yuque://zhongxian-iiot9/hlyypb/dhzx6nrqmxtv49ue -->

# LLaMA-Factory
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">LLAMA Factory</font>**<font style="color:rgb(51, 51, 51);"> 是一个基于 </font>**<font style="color:rgb(51, 51, 51);">Hugging Face Transformers</font>**<font style="color:rgb(51, 51, 51);"> 的开源项目，专注于为大型语言模型（Large Language Models, LLMs）提供高效、灵活且用户友好的微调（Fine-tuning）框架，</font><font style="color:rgb(25, 27, 31);">是一个封装比较完善的LLM微调工具，它能够帮助用户快速地训练和微调大多数LLM模型。</font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
2. **<font style="color:rgb(51, 51, 51);">文档</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://llama-factory.readthedocs.io](https://llama-factory.readthedocs.io/)
3. **<font style="color:rgb(51, 51, 51);">Hugging Face 模型库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://huggingface.co/models](https://huggingface.co/models)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761211610168-c1c86315-a6ca-4fc0-99ae-fba585c74b84.png)

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

+ **<font style="color:rgb(25, 27, 31);">各种模型</font>**<font style="color:rgb(25, 27, 31);">: LLaMA, LLaVA, Mistral, Mixtral-MoE, Qwen, Yi, Gemma, Baichuan, ChatGLM, Phi, etc.</font>
+ **<font style="color:rgb(25, 27, 31);">集成训练方法</font>**<font style="color:rgb(25, 27, 31);">: (Continuous) pre-training, (multimodal) supervised fine-tuning, reward modeling, PPO, DPO and ORPO.</font>
+ **<font style="color:rgb(25, 27, 31);">Scalable resources</font>**<font style="color:rgb(25, 27, 31);">: 32-bit full-tuning, 16-bit freeze-tuning, 16-bit LoRA and 2/4/8-bit QLoRA via</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">AQLM</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=AQLM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">/</font>[<font style="color:rgb(9, 64, 142);">AWQ</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=AWQ&zhida_source=entity)<font style="color:rgb(25, 27, 31);">/</font>[<font style="color:rgb(9, 64, 142);">GPTQ</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=GPTQ&zhida_source=entity)<font style="color:rgb(25, 27, 31);">/</font>[<font style="color:rgb(9, 64, 142);">LLM.int8</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=LLM.int8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">.</font>
+ **<font style="color:rgb(25, 27, 31);">Advanced algorithms</font>**<font style="color:rgb(25, 27, 31);">: GaLore, BAdam, DoRA, LongLoRA, LLaMA Pro, Mixture-of-Depths, LoRA+, LoftQ and Agent tuning.</font>
+ **<font style="color:rgb(25, 27, 31);">实用tricks</font>**<font style="color:rgb(25, 27, 31);">:</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">FlashAttention-2</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=FlashAttention-2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">, Unsloth,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">RoPE scaling</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=RoPE+scaling&zhida_source=entity)<font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">NEFTune</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=NEFTune&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">and</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">rsLoRA</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=rsLoRA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">.</font>
+ **<font style="color:rgb(25, 27, 31);">实验监控</font>**<font style="color:rgb(25, 27, 31);">:</font>[<font style="color:rgb(9, 64, 142);">LlamaBoard</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=LlamaBoard&zhida_source=entity)<font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">TensorBoard</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=TensorBoard&zhida_source=entity)<font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">Wandb</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=Wandb&zhida_source=entity)<font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font>[<font style="color:rgb(9, 64, 142);">MLflow</font>](https://zhida.zhihu.com/search?content_id=243191153&content_type=Article&match_order=1&q=MLflow&zhida_source=entity)<font style="color:rgb(25, 27, 31);">, etc.</font>
+ **<font style="color:rgb(25, 27, 31);">推理集成</font>**<font style="color:rgb(25, 27, 31);">: OpenAI-style API, Gradio UI and CLI with vLLM worker.</font>

**框架架构**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761211714455-f023db98-5b7c-4c69-b468-314d2f172b4e.png)

**支持模型**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761211776624-cbacc860-9615-4fc0-ad99-4e6758508de6.png)

:::color5
**<font style="color:#601BDE;">2.支持训练方法</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761211730245-dc5d3300-25a0-4427-9400-5c5ce2cc2df6.png)

:::color5
**<font style="color:#601BDE;">3.安装与使用</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">安装依赖</font>**

```bash
pip install llama-factory
# 或从源码安装
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -r requirements.txt

```

2. **<font style="color:rgb(51, 51, 51);">快速启动</font>**

```bash
# 使用 LoRA 微调 LLaMA-7B 模型
python train.py \
  --model_name_or_path meta-llama/Llama-2-7b-hf \
  --dataset alpaca_en \
  --lora_target_modules q_proj v_proj \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 8 \
  --lr 2e-4 \
  --output_dir ./output
```

3. **<font style="color:rgb(51, 51, 51);">配置文件驱动</font>**

<font style="color:rgb(51, 51, 51);">通过 YAML 文件定义训练参数：</font>

```yaml
# configs/alpaca_lora.yaml
model_name_or_path: meta-llama/Llama-2-7b-hf
dataset: alpaca_en
lora:
  target_modules: ["q_proj", "v_proj"]
  r: 8
  lora_alpha: 32
training:
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 8
  learning_rate: 2e-4
  num_train_epochs: 3
```

运行命令

```bash
python train.py --config configs/alpaca_lora.yaml
```



# Megatron
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(15, 17, 21);">Megatron 是由 NVIDIA 开发的一个强大的开源工具集，专门用于大规模训练巨型Transformer模型。它提供了两个主要组件：</font>**<font style="color:rgb(15, 17, 21);">Megatron-LM 参考实现</font>**<font style="color:rgb(15, 17, 21);">为训练最先进的基础模型提供了开箱即用的解决方案；而</font>**<font style="color:rgb(15, 17, 21);">Megatron Core 可组合库</font>**<font style="color:rgb(15, 17, 21);">则为开发者提供了高度优化的基础模块，用以构建自定义的、高性能的训练框架。无论是想快速复现主流大模型，还是需要深度定制训练流程，Megatron 都能提供极致的分布式训练性能和灵活性。</font><font style="color:rgb(51, 51, 51);"></font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761212096169-6415c497-0d8f-4d93-b546-7b2e8b262f6b.png)

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:rgb(15, 17, 21);">通用核心特性：</font>**

+ **<font style="color:rgb(15, 17, 21);">极致性能</font>**<font style="color:rgb(15, 17, 21);">：为最新的 NVIDIA GPU 硬件优化，实现顶尖的训练与推理速度。</font>
+ **<font style="color:rgb(15, 17, 21);">强大的分布式训练</font>**<font style="color:rgb(15, 17, 21);">：支持并整合了多种并行策略，包括张量并行（TP）、流水线并行（PP）和数据并行（DP），以应对千亿乃至万亿参数模型的训练挑战。</font>
+ **<font style="color:rgb(15, 17, 21);">广泛的模型支持</font>**<font style="color:rgb(15, 17, 21);">：预置了包括 GPT、LLaMA、Qwen、Mixtral、Mamba 等在内的多种主流模型架构。</font>

**<font style="color:rgb(15, 17, 21);">Megatron-LM 参考实现的特性：</font>**

+ **<font style="color:rgb(15, 17, 21);">端到端解决方案</font>**<font style="color:rgb(15, 17, 21);">：提供从数据准备、模型训练到评估的全套脚本和示例。</font>
+ **<font style="color:rgb(15, 17, 21);">快速实验</font>**<font style="color:rgb(15, 17, 21);">：基于经过验证的模型配置，方便研究团队快速进行迭代和实验。</font>
+ **<font style="color:rgb(15, 17, 21);">研究与学习</font>**<font style="color:rgb(15, 17, 21);">：非常适合用于学习分布式训练的概念与最佳实践。</font>

**<font style="color:rgb(15, 17, 21);">Megatron Core 可组合库的特性：</font>**

+ **<font style="color:rgb(15, 17, 21);">模块化与可组合性</font>**<font style="color:rgb(15, 17, 21);">：提供注意力机制、MLP 等Transformer组件的优化构建块，可以像搭积木一样自定义训练框架。</font>
+ **<font style="color:rgb(15, 17, 21);">高度灵活性</font>**<font style="color:rgb(15, 17, 21);">：支持定制训练循环、优化器和数据管道，满足前沿研究和生产的需求。</font>
+ **<font style="color:rgb(15, 17, 21);">底层优化</font>**<font style="color:rgb(15, 17, 21);">：包含高度优化的 GPU 内核、高效的内存管理机制以及对 FP16、BF16 和 FP8 等混合精度训练的原生支持。</font>

**项目架构**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761212126886-7e1b68d4-c478-4cf5-a51f-c860968e5a92.png)

**并行策略示例**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761212186411-86556be6-c975-408e-aed9-12d1d5bdfa33.png)

:::color5
**<font style="color:#601BDE;">2.性能优化方案</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761212444501-0a804d11-03de-41a5-86e0-4d8404d4c184.png)

1. **<font style="color:rgb(31, 35, 40);">FlashAttention</font>**

FlashAttention是一种快速且内存高效的注意力算法。我们建议使用默认用法，即通过Transformer Engine使用cuDNN来引起注意，并在FP8内核的正向传播上提供高达50%的加速，在反向传播上提供84%的加速。flash attn包也通过--use flash attn得到支持。

2. **<font style="color:rgb(31, 35, 40);">Mixed Precision Training</font>**

```bash
--fp16                    # Standard FP16
--bf16                    # BFloat16 (recommended for large models)
--fp8-hybrid              # FP8 training (Hopper, Ada, and Blackwell GPUs)
```

1. **<font style="color:rgb(31, 35, 40);">Activation Checkpointing and Recomputation</font>**

```bash
# For limited memory
--recompute-activations

# For extreme memory constraints
--recompute-granularity full \
--recompute-method uniform
```

1. **<font style="color:rgb(31, 35, 40);">Data Parallelism Communication Overlap</font>**

```bash
--overlap-grad-reduce
--overlap-param-gather
```

1. **<font style="color:rgb(31, 35, 40);">Distributed Optimizer</font>**

```bash
--use-distributed-optimizer
```

:::color5
**<font style="color:#601BDE;">3.安装与使用</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

1. **安装**

```bash
# 1. Install Megatron Core with required dependencies
pip install --no-build-isolation megatron-core[mlm,dev]

# 2. Clone repository for examples
git clone https://github.com/NVIDIA/Megatron-LM.git
cd Megatron-LM
pip install --no-build-isolation .[mlm,dev]
```

2. **简单示例**

```bash
# Distributed training example (2 GPUs, mock data)
torchrun --nproc_per_node=2 examples/run_simple_mcore_train_loop.py
```

3. **<font style="color:rgb(31, 35, 40);">LLama-3 训练示例</font>**

```bash
# 8 GPUs, FP8 precision, mock data
./examples/llama/train_llama3_8b_fp8.sh
```

4. **<font style="color:rgb(31, 35, 40);">Data Preparation</font>**

```bash
{"text": "Your training text here..."}
{"text": "Another training sample..."}
```

```bash
python tools/preprocess_data.py \
    --input data.jsonl \
    --output-prefix processed_data \
    --tokenizer-type HuggingFaceTokenizer \
    --tokenizer-model /path/to/tokenizer.model \
    --workers 8 \
    --append-eod
```

# <font style="color:rgb(51, 51, 51);">ms-swift</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">ms-swift 是 ModelScope 社区官方推出的轻量级可扩展微调框架。它支持超过 450 个纯文本大型模型和 150 多个多模态大型模型，覆盖了从模型训练到部署的整个流程。该框架支持包括 LoRA、QLoRA 在内的多种轻量级微调方法，以及分布式训练、量化训练和强化学习人类反馈（RLHF）训练。</font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/modelscope/ms-swift](https://github.com/modelscope/ms-swift)
2. **<font style="color:rgb(51, 51, 51);">说明文档</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://swift.readthedocs.io/en/latest/GetStarted/Quick-start.html](https://swift.readthedocs.io/en/latest/GetStarted/Quick-start.html)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761213005639-eb51cdef-9f59-405b-8185-335d1aa5e181.png)

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

🍎 **模型类型：**

支持600+纯文本大型模型、300+多模态大型模型，以及All-to-All多模态模型、序列分类模型和嵌入模型，涵盖从训练到部署的整个过程。

数据集类型：配备150多种预训练、微调、人工对齐、多模态数据集，并支持自定义数据集。

硬件支持：兼容CPU、RTX系列、T4/V100、A10/A100/H100、Ascend NPU、MPS等。

轻量级训练：支持轻量级微调方法，如LoRA、QLoRA、DoRA、LoRA+、ReFT、RS LoRA、LLaMAPro、Adapter、GaLore、Q-GaLore、LISA、UnSloth、Liger Kernel。

分布式训练：支持分布式数据并行（DDP）、device_map简单模型并行、DeepSpeed ZeRO2/ZeRO3、FSDP、megatron等分布式训练技术。

量化训练：支持训练BNB、AWQ、GPTQ、AQLM、HQQ、EETQ等量化模型。

🍊 **RLHF训练：**

支持纯文本和多模态大型模型的人类对齐训练方法，如DPO、GRPO、RM、PPO、GKD、KTO、CPO、SimPO、ORPO。

🍓 **多模态训练：**

支持图像、视频和音频等不同模态的训练，用于VQA、字幕、OCR和接地等任务。

🥥 **megatron并行：**

支持使用megatron平行技术加速CPT/SFT/DPO/KTO/RM，目前兼容200多个纯文本大型模型、100多个多模态大型模型。

接口训练：通过接口提供训练、推理、评估、量化等功能，完成整个大型模型管道。

插件和扩展：支持自定义模型和数据集扩展，以及对损失、指标、训练器、损失规模、回调、优化器等组件的自定义。

🍉 **工具箱功能：**

不仅为大型模型和多模态大型模型提供训练支持，还涵盖了推理、评估、量化和部署的整个过程。

推理加速：支持PyTorch、vLLM、SGLang、LmDeploy等推理加速引擎，并提供用于加速推理、部署和评估模块的OpenAI API。

模型评估：使用EvalScope作为评估后端，支持对纯文本和多模态模型的100多个数据集进行评估。

模型量化：支持AWQ、GPTQ、FP8和BNB量化导出，模型可以使用vLLM/SGLang/LmDeploy进行推理加速和继续训练。

**训练框架对比**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761213228641-a6fc7eee-7338-44db-95d6-e4f91f1793bd.png)

**框架结构**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761213241794-0b185516-0eaf-4567-8ad3-5d4d455a4f78.png)

:::color5
**<font style="color:#601BDE;">2.支持训练方法</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761213023719-2887b0c3-ea83-497f-ae3c-9eb22dc5bd7a.png)

:::color5
**<font style="color:#601BDE;">3.安装与使用</font>**

:::

1. <font style="color:rgb(31, 35, 40);">To install using pip:</font>

```bash
pip install ms-swift -U
```

2. <font style="color:rgb(31, 35, 40);">To install from source:</font>

```bash
# pip install git+https://github.com/modelscope/ms-swift.git

git clone https://github.com/modelscope/ms-swift.git
cd ms-swift
pip install -e .
```

3. <font style="color:rgb(31, 35, 40);">在单个3090 GPU上对Qwen2.5-7B-Instruct进行10分钟的自我认知微调：</font>

```bash
# 22GB
CUDA_VISIBLE_DEVICES=0 \
swift sft \
    --model Qwen/Qwen2.5-7B-Instruct \
    --train_type lora \
    --dataset 'AI-ModelScope/alpaca-gpt4-data-zh#500' \
              'AI-ModelScope/alpaca-gpt4-data-en#500' \
              'swift/self-cognition#500' \
    --torch_dtype bfloat16 \
    --num_train_epochs 1 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --learning_rate 1e-4 \
    --lora_rank 8 \
    --lora_alpha 32 \
    --target_modules all-linear \
    --gradient_accumulation_steps 16 \
    --eval_steps 50 \
    --save_steps 50 \
    --save_total_limit 2 \
    --logging_steps 5 \
    --max_length 2048 \
    --output_dir output \
    --system 'You are a helpful assistant.' \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 4 \
    --model_author swift \
    --model_name swift-robot
```

  


# <font style="color:rgb(51, 51, 51);">unsloth</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">unsloth 旨在显著加快大型语言模型的微调速度（高达 2 倍）并降低内存使用（高达 80%）。它支持包括 Llama、DeepSeek、Gemma 和 Mistral 等多种模型。unsloth 利用高度优化的 OpenAI Triton 内核和手动反向传播引擎来实现性能提升。它支持全参数微调、预训练以及 4 位、8 位和 16 位的高效训练（通过 bitsandbytes 实现 QLoRA/LoRA），并声称在加速和减少内存使用的同时不会损失精度。</font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/unslothai/unsloth](https://github.com/unslothai/unsloth)
2. **官方文档：**[https://docs.unsloth.ai/get-started/beginner-start-here](https://docs.unsloth.ai/get-started/beginner-start-here)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761216063506-047612ee-0e07-4f7d-a24d-97c2290eeb52.png)

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

+ <font style="color:rgb(15, 17, 21);">支持全参数微调、预训练、4位量化、16位与8位训练</font>
+ <font style="color:rgb(15, 17, 21);">兼容所有模型（包括TTS、多模态、BERT等）——凡可在Transformers中运行的模型，皆可适配Unsloth。</font>
+ <font style="color:rgb(15, 17, 21);">作为最高效的强化学习训练库，显存占用降低80%，支持GRPO、GSPO、DrGRPO、DAPO等算法。</font>  
<font style="color:rgb(15, 17, 21);">精准无损——零精度损失，未采用任何近似计算。</font>
+ <font style="color:rgb(15, 17, 21);">支持NVIDIA（2018年起）、AMD、Intel GPU及DGX Spark平台，最低CUDA算力7.0（兼容V100、T4、Titan V、RTX 20/30/40系列、A100、H100、L40等）。</font>
+ <font style="color:rgb(15, 17, 21);">适配Linux、WSL及Windows操作系统。</font>
+ <font style="color:rgb(15, 17, 21);">全部内核基于OpenAI Triton语言开发，搭载手动反向传播引擎。</font>

**框架架构**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761211714455-f023db98-5b7c-4c69-b468-314d2f172b4e.png)

**支持模型**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761216055510-809e9774-efc3-4ed8-9923-92269c5166c6.png)

:::color5
**<font style="color:#601BDE;">2.支持训练方法</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

强化学习，包括GRPO、GSPO、DrGRPO、DAPO、PPO、奖励建模、在线DPO，都与Uncloth合作。

RL笔记本列表：

+ <font style="color:rgb(31, 35, 40);">gpt-oss GSPO notebook:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-(20B)-GRPO.ipynb)
+ <font style="color:rgb(31, 35, 40);">Qwen2.5-VL GSPO notebook:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen2_5_7B_VL_GRPO.ipynb)
+ <font style="color:rgb(31, 35, 40);">Advanced Qwen3 GRPO notebook:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_(4B)-GRPO.ipynb)
+ <font style="color:rgb(31, 35, 40);">ORPO notebook:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3_(8B)-ORPO.ipynb)
+ <font style="color:rgb(31, 35, 40);">DPO Zephyr notebook:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Zephyr_(7B)-DPO.ipynb)
+ <font style="color:rgb(31, 35, 40);">KTO notebook:</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/drive/1MRgGtLWuZX4ypSfGguFgC-IblTvO2ivM?usp=sharing)
+ <font style="color:rgb(31, 35, 40);">SimPO notebook: </font>[<font style="color:rgb(9, 105, 218);">Link</font>](https://colab.research.google.com/drive/1Hs5oQDovOay4mFA6Y9lQhVJ8TnbFLFh2?usp=sharing)

:::color5
**<font style="color:#601BDE;">3.安装与使用</font>**

:::

**<font style="color:rgb(31, 35, 40);">Install with pip (recommended) for Linux devices:</font>**

```bash
pip install unsloth
```

**<font style="color:rgb(31, 35, 40);">To update Unsloth:</font>**

```bash
pip install --upgrade --force-reinstall --no-cache-dir unsloth unsloth_zoo
```

**微调gpt-oss-20b：**

```python
from unsloth import FastLanguageModel, FastModel
import torch
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
max_seq_length = 2048 # Supports RoPE Scaling internally, so choose any!
# Get LAION dataset
url = "https://huggingface.co/datasets/laion/OIG/resolve/main/unified_chip2.jsonl"
dataset = load_dataset("json", data_files = {"train" : url}, split = "train")

# 4bit pre quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/gpt-oss-20b-unsloth-bnb-4bit", #or choose any model

] # More models at https://huggingface.co/unsloth

model, tokenizer = FastModel.from_pretrained(
    model_name = "unsloth/gpt-oss-20b",
    max_seq_length = 2048, # Choose any for long context!
    load_in_4bit = True,  # 4-bit quantization. False = 16-bit LoRA.
    load_in_8bit = False, # 8-bit quantization
    load_in_16bit = False, # [NEW!] 16-bit LoRA
    full_finetuning = False, # Use for full fine-tuning.
    # token = "hf_...", # use one if using gated models
)

# Do model patching and add fast LoRA weights
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    max_seq_length = max_seq_length,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    tokenizer = tokenizer,
    args = SFTConfig(
        max_seq_length = max_seq_length,
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10,
        max_steps = 60,
        logging_steps = 1,
        output_dir = "outputs",
        optim = "adamw_8bit",
        seed = 3407,
    ),
)
trainer.train()

# Go to https://docs.unsloth.ai for advanced tips like
# (1) Saving to GGUF / merging to 16bit for vLLM
# (2) Continued training from a saved LoRA adapter
# (3) Adding an evaluation loop / OOMs
# (4) Customized chat templates
```

# trl
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(25, 27, 31);">TRL（Transformers Reinforcement Learning）</font>**<font style="color:rgb(25, 27, 31);"> 是 Hugging Face 推出的一个专门用于大语言模型对齐和微调的库。</font><font style="color:rgb(25, 27, 31);">它建立在</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Transformers</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">Accelerate</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">之上，兼容 Hugging Face 生态（Datasets、PEFT 等），并提供了简单易用的接口来实现：</font>

+ **<font style="color:rgb(25, 27, 31);">SFT（Supervised Fine-Tuning）</font>**<font style="color:rgb(25, 27, 31);">：通过已有标注数据进行监督训练。</font>
+ **<font style="color:rgb(25, 27, 31);">PPO（Proximal Policy Optimization）</font>**<font style="color:rgb(25, 27, 31);">：基于奖励模型进行强化学习优化。</font>
+ **<font style="color:rgb(25, 27, 31);">DPO（Direct Preference Optimization）</font>**<font style="color:rgb(25, 27, 31);">：直接基于偏好数据进行优化，避免训练奖励模型。</font>

<font style="color:rgb(25, 27, 31);">通过这些方法，TRL 能够高效完成模型对齐（alignment），如 </font>**<font style="color:rgb(25, 27, 31);">人类反馈强化学习（RLHF）</font>**<font style="color:rgb(25, 27, 31);"> 或 </font>**<font style="color:rgb(25, 27, 31);">偏好对齐（Preference Optimization）</font>**<font style="color:rgb(25, 27, 31);">。</font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/huggingface/trl](https://github.com/huggingface/trl)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761217251019-e04a2aae-b3e8-4b3a-a13d-b07e4278d99a.png)

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:rgb(15, 17, 21);">训练器</font>**<font style="color:rgb(15, 17, 21);">：通过SFTTrainer、GRPOTrainer、DPOTrainer、RewardTrainer等多种训练器，可轻松使用各类微调方法。</font>

**<font style="color:rgb(15, 17, 21);">高效且可扩展</font>**<font style="color:rgb(15, 17, 21);">：</font>

+ <font style="color:rgb(15, 17, 21);">利用</font><font style="color:rgb(15, 17, 21);">🤗</font><font style="color:rgb(15, 17, 21);"> Accelerate，通过DDP和DeepSpeed等方法实现从单GPU到多节点集群的灵活扩展</font>
+ <font style="color:rgb(15, 17, 21);">与</font><font style="color:rgb(15, 17, 21);">🤗</font><font style="color:rgb(15, 17, 21);"> PEFT完全集成，通过量化和LoRA/QLoRA技术，使普通硬件也能训练大模型</font>
+ <font style="color:rgb(15, 17, 21);">集成</font><font style="color:rgb(15, 17, 21);">🦥</font><font style="color:rgb(15, 17, 21);"> Unsloth，使用优化内核加速训练过程</font>
+ **<font style="color:rgb(15, 17, 21);">命令行界面(CLI)</font>**<font style="color:rgb(15, 17, 21);">：提供简洁接口，无需编写代码即可对模型进行微调</font>

:::color5
**<font style="color:#601BDE;">2.安装与使用</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

1. <font style="background-color:#FFFFFF;">Install the library using </font>`<font style="background-color:#FFFFFF;">pip</font>`<font style="background-color:#FFFFFF;">:</font>

```bash
pip install trl
```

2. `**<font style="background-color:#FFFFFF;">SFTTrainer</font>**`<font style="background-color:#FFFFFF;"> 以下是如何使用SFTTrainer的基本示例：</font>

```python
from trl import SFTTrainer
from datasets import load_dataset

dataset = load_dataset("trl-lib/Capybara", split="train")

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
)
trainer.train()
```

3. `**<font style="background-color:#FFFFFF;">GRPOTrainer</font>**`<font style="background-color:#FFFFFF;"> GRPOTrainer实现了比PPO更节省内存的组相对策略优化（GRPO）算法，并用于训练Deepseek AI的R1。</font>

```python
from datasets import load_dataset
from trl import GRPOTrainer

dataset = load_dataset("trl-lib/tldr", split="train")

# Dummy reward function: count the number of unique characters in the completions
def reward_num_unique_chars(completions, **kwargs):
    return [len(set(c)) for c in completions]

trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_num_unique_chars,
    train_dataset=dataset,
)
trainer.train()
```

# verl
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(15, 17, 21);">Verl</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">是一个灵活、高效且可用于生产环境的强化学习训练库，专为大语言模型设计。</font>

**<font style="color:rgb(15, 17, 21);">Verl</font>**<font style="color:rgb(15, 17, 21);"> 是论文《HybridFlow: A Flexible and Efficient RLHF Framework》所提出框架的开源实现。</font>

1. **<font style="color:rgb(51, 51, 51);">GitHub 仓库</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/volcengine/verl](https://github.com/volcengine/verl)
2. **paper**：[https://arxiv.org/pdf/2409.19256](https://arxiv.org/pdf/2409.19256)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761216533583-18c08784-7881-405e-be73-c43bf60ba132.png)

:::color5
**<font style="color:#601BDE;">1.核心特性</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

**<font style="color:rgb(15, 17, 21);">Verl 具备出色的灵活性与易用性，具体体现在：</font>**

+ **<font style="color:rgb(15, 17, 21);">轻松扩展多样化的 RL 算法</font>**<font style="color:rgb(15, 17, 21);">：其混合控制器编程模型能够灵活表示并高效执行复杂的训练后数据流。仅需几行代码即可构建如 GRPO、PPO 等强化学习数据流。</font>
+ **<font style="color:rgb(15, 17, 21);">通过模块化 API 无缝集成现有 LLM 基础设施</font>**<font style="color:rgb(15, 17, 21);">：该库解耦了计算与数据依赖，可与现有大语言模型框架（如 FSDP、Megatron-LM、vLLM、SGLang 等）无缝集成。</font>
+ **<font style="color:rgb(15, 17, 21);">灵活的设备映射</font>**<font style="color:rgb(15, 17, 21);">：支持将模型以多种方式部署到不同的 GPU 组上，从而实现高效的资源利用，并在不同规模的集群上具备良好的可扩展性。</font>
+ **<font style="color:rgb(15, 17, 21);">与流行的 HuggingFace 模型即装即用</font>**<font style="color:rgb(15, 17, 21);">。</font>

**<font style="color:rgb(15, 17, 21);">Verl 具备卓越的性能表现，其优势包括：</font>**

+ **<font style="color:rgb(15, 17, 21);">业界领先的吞吐量</font>**<font style="color:rgb(15, 17, 21);">：集成了顶尖的大语言模型训练与推理引擎，并实现了顶级的强化学习训练吞吐量。</font>
+ **<font style="color:rgb(15, 17, 21);">通过 3D 混合引擎实现高效的参与者模型重分片</font>**<font style="color:rgb(15, 17, 21);">：该技术消除了内存冗余，并显著减少了在训练阶段与生成阶段之间切换时的通信开销。</font>

**3种RLHF算法的数据流图**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761216688744-a4ea5627-ea70-4ae6-a1ec-deb53d94a7cf.png)

**HybridFlow框架架构**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761216738559-b3567d99-108b-4014-8442-ce817e43e91f.png)

:::color5
**<font style="color:#601BDE;">2.基于verl的优秀工作</font>**<font style="color:#D22D8D;">  (by草莓师姐)</font>

:::

+ [<font style="color:rgb(9, 105, 218);">TinyZero</font>](https://github.com/Jiayi-Pan/TinyZero)<font style="color:rgb(31, 35, 40);">: a reproduction of </font>**<font style="color:rgb(31, 35, 40);">DeepSeek R1 Zero</font>**<font style="color:rgb(31, 35, 40);"> recipe for reasoning tasks </font>
+ [<font style="color:rgb(9, 105, 218);">SkyThought</font>](https://github.com/NovaSky-AI/SkyThought)<font style="color:rgb(31, 35, 40);">: RL training for Sky-T1-7B by NovaSky AI team. </font>
+ [<font style="color:rgb(9, 105, 218);">simpleRL-reason</font>](https://github.com/hkust-nlp/simpleRL-reason)<font style="color:rgb(31, 35, 40);">: SimpleRL-Zoo: Investigating and Taming Zero Reinforcement Learning for Open Base Models in the Wild </font>
+ [<font style="color:rgb(9, 105, 218);">Easy-R1</font>](https://github.com/hiyouga/EasyR1)<font style="color:rgb(31, 35, 40);">: </font>**<font style="color:rgb(31, 35, 40);">Multi-modal</font>**<font style="color:rgb(31, 35, 40);"> RL training framework </font>
+ [<font style="color:rgb(9, 105, 218);">OpenManus-RL</font>](https://github.com/OpenManus/OpenManus-RL)<font style="color:rgb(31, 35, 40);">: LLM Agents RL tunning framework for multiple agent environments. </font>
+ [<font style="color:rgb(9, 105, 218);">rllm</font>](https://github.com/agentica-project/rllm)<font style="color:rgb(31, 35, 40);">: async RL training with </font>[<font style="color:rgb(9, 105, 218);">verl-pipeline</font>](https://github.com/agentica-project/verl-pipeline)<font style="color:rgb(31, 35, 40);"> </font>
+ [<font style="color:rgb(9, 105, 218);">RAGEN</font>](https://github.com/ZihanWang314/ragen)<font style="color:rgb(31, 35, 40);">: a general-purpose reasoning </font>**<font style="color:rgb(31, 35, 40);">agent</font>**<font style="color:rgb(31, 35, 40);"> training framework </font>
+ [<font style="color:rgb(9, 105, 218);">Search-R1</font>](https://github.com/PeterGriffinJin/Search-R1)<font style="color:rgb(31, 35, 40);">: RL with reasoning and </font>**<font style="color:rgb(31, 35, 40);">searching (tool-call)</font>**<font style="color:rgb(31, 35, 40);"> interleaved LLMs </font>
+ [<font style="color:rgb(9, 105, 218);">ReSearch</font>](https://github.com/Agent-RL/ReSearch)<font style="color:rgb(31, 35, 40);">: Learning to </font>**<font style="color:rgb(31, 35, 40);">Re</font>**<font style="color:rgb(31, 35, 40);">ason with </font>**<font style="color:rgb(31, 35, 40);">Search</font>**<font style="color:rgb(31, 35, 40);"> for LLMs via Reinforcement Learning </font>
+ [<font style="color:rgb(9, 105, 218);">Skywork-OR1</font>](https://github.com/SkyworkAI/Skywork-OR1)<font style="color:rgb(31, 35, 40);">: Skywork open reaonser series </font>
+ [<font style="color:rgb(9, 105, 218);">ToRL</font>](https://github.com/GAIR-NLP/ToRL)<font style="color:rgb(31, 35, 40);">: Scaling tool-integrated RL </font>
+ [<font style="color:rgb(9, 105, 218);">Absolute Zero Reasoner</font>](https://github.com/LeapLabTHU/Absolute-Zero-Reasoner)<font style="color:rgb(31, 35, 40);">: </font>[<font style="color:rgb(9, 105, 218);">A no human curated data self-play framework for reasoning</font>](https://arxiv.org/abs/2505.03335)<font style="color:rgb(31, 35, 40);"> </font>
+ [<font style="color:rgb(9, 105, 218);">verl-agent</font>](https://github.com/langfengQ/verl-agent)<font style="color:rgb(31, 35, 40);">: A scalable training framework for </font>**<font style="color:rgb(31, 35, 40);">long-horizon LLM/VLM agents</font>**<font style="color:rgb(31, 35, 40);">, along with a new algorithm </font>**<font style="color:rgb(31, 35, 40);">GiGPO</font>**<font style="color:rgb(31, 35, 40);"> </font>
+ [<font style="color:rgb(9, 105, 218);">RL-Factory</font>](https://github.com/Simple-Efficient/RL-Factory)<font style="color:rgb(31, 35, 40);">: An easy and efficient RL post-training framework for Agentic Learning </font>
+ [<font style="color:rgb(9, 105, 218);">ReTool</font>](https://retool-rl.github.io/)<font style="color:rgb(31, 35, 40);">: ReTool: reinforcement learning for strategic tool use in LLMs. Code release is in progress...</font>
+ [<font style="color:rgb(9, 105, 218);">verl-tool</font>](https://github.com/TIGER-AI-Lab/verl-tool)<font style="color:rgb(31, 35, 40);">: An unified and easy-to-extend tool-agent training framework based on verl</font>
+ [<font style="color:rgb(9, 105, 218);">PRIME</font>](https://github.com/PRIME-RL/PRIME)<font style="color:rgb(31, 35, 40);">: Process reinforcement through implicit rewards </font>
+ [<font style="color:rgb(9, 105, 218);">MemAgent</font>](https://github.com/BytedTsinghua-SIA/MemAgent)<font style="color:rgb(31, 35, 40);">: MemAgent: Reshaping Long-Context LLM with Multi-Conv RL based Memory Agent </font>
+ [<font style="color:rgb(9, 105, 218);">POLARIS</font>](https://github.com/ChenxinAn-fdu/POLARIS)<font style="color:rgb(31, 35, 40);">: A Post-training recipe for scaling RL on Advanced Reasoning models </font>
+ [<font style="color:rgb(9, 105, 218);">GUI-R1</font>](https://github.com/ritzz-ai/GUI-R1)<font style="color:rgb(31, 35, 40);">: </font>**<font style="color:rgb(31, 35, 40);">GUI-R1</font>**<font style="color:rgb(31, 35, 40);">: A Generalist R1-style Vision-Language Action Model For </font>**<font style="color:rgb(31, 35, 40);">GUI Agents</font>**<font style="color:rgb(31, 35, 40);"> </font>

:::color5
**<font style="color:#601BDE;">3.安装与使用</font>**

:::

**<font style="color:rgb(31, 35, 40);">快速开始:</font>**

+ [<font style="color:rgb(9, 105, 218);">Installation</font>](https://verl.readthedocs.io/en/latest/start/install.html)
+ [<font style="color:rgb(9, 105, 218);">Quickstart</font>](https://verl.readthedocs.io/en/latest/start/quickstart.html)
+ [<font style="color:rgb(9, 105, 218);">Programming Guide</font>](https://verl.readthedocs.io/en/latest/hybrid_flow.html)<font style="color:rgb(31, 35, 40);"> </font><font style="color:rgb(31, 35, 40);">&</font><font style="color:rgb(31, 35, 40);"> </font>[<font style="color:rgb(9, 105, 218);">Tech Talk</font>](https://hcqnc.xetlk.com/sl/3vACOK)<font style="color:rgb(31, 35, 40);"> </font><font style="color:rgb(31, 35, 40);">(in Chinese)</font>
+ [<font style="color:rgb(9, 105, 218);">PPO in verl</font>](https://verl.readthedocs.io/en/latest/algo/ppo.html)
+ [<font style="color:rgb(9, 105, 218);">GRPO in verl</font>](https://verl.readthedocs.io/en/latest/algo/grpo.html)

**<font style="color:rgb(31, 35, 40);">PPO示例 step-by-step:</font>**

+ [<font style="color:rgb(9, 105, 218);">Prepare Data for Post-Training</font>](https://verl.readthedocs.io/en/latest/preparation/prepare_data.html)
+ [<font style="color:rgb(9, 105, 218);">Implement Reward Function for Dataset</font>](https://verl.readthedocs.io/en/latest/preparation/reward_function.html)
+ [<font style="color:rgb(9, 105, 218);">PPO Example Architecture</font>](https://verl.readthedocs.io/en/latest/examples/ppo_code_architecture.html)
+ [<font style="color:rgb(9, 105, 218);">Config Explanation</font>](https://verl.readthedocs.io/en/latest/examples/config.html)

**<font style="color:rgb(31, 35, 40);">可复现的baseline</font>**

+ [<font style="color:rgb(9, 105, 218);">RL performance on coding, math</font>](https://verl.readthedocs.io/en/latest/algo/baseline.html)

**<font style="color:rgb(31, 35, 40);">关于代码解释和高级用法（扩展）</font>**

+ [<font style="color:rgb(9, 105, 218);">Add Models with the FSDP Backend</font>](https://verl.readthedocs.io/en/latest/advance/fsdp_extension.html)
+ [<font style="color:rgb(9, 105, 218);">Add Models with the Megatron-LM Backend</font>](https://verl.readthedocs.io/en/latest/advance/megatron_extension.html)
+ [<font style="color:rgb(9, 105, 218);">Multi-turn Rollout Support</font>](https://verl.readthedocs.io/en/latest/sglang_multiturn/multiturn.html)
+ [<font style="color:rgb(9, 105, 218);">Search Tool Integration</font>](https://verl.readthedocs.io/en/latest/sglang_multiturn/search_tool_example.html)
+ [<font style="color:rgb(9, 105, 218);">Sandbox Fusion Integration</font>](https://verl.readthedocs.io/en/latest/examples/sandbox_fusion_example.html)
+ [<font style="color:rgb(9, 105, 218);">Deployment using Separate GPU Resources</font>](https://github.com/volcengine/verl/tree/main/examples/split_placement)
+ [<font style="color:rgb(9, 105, 218);">Extend to Other RL(HF) algorithms</font>](https://verl.readthedocs.io/en/latest/advance/dpo_extension.html)
+ [<font style="color:rgb(9, 105, 218);">Ray API design tutorial</font>](https://verl.readthedocs.io/en/latest/advance/placement.html)

**<font style="color:rgb(31, 35, 40);">社区博客</font>**

+ [<font style="color:rgb(9, 105, 218);">When Reasoning Models Break Tokenization: The Hidden Complexity of Multiturn Training</font>](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/rlhf/verl/multi-turn/fast_tokenization/multiturn_tokenization_and_masking.md)
+ [<font style="color:rgb(9, 105, 218);">verl deployment on AWS SageMaker</font>](https://medium.com/@kaige.yang0110/run-verl-on-sagemaker-using-4x8-l40s-gpus-8e6d5c3c61d3)
+ [<font style="color:rgb(9, 105, 218);">verl x SGLang Multi-turn Code Walkthrough</font>](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/rlhf/verl/multi-turn/code-walk-through/readme_EN.md)
+ [<font style="color:rgb(9, 105, 218);">Optimizing SGLang Memory Usage in verl</font>](https://hebiao064.github.io/rl-memory-management)
+ [<font style="color:rgb(9, 105, 218);">SGLang, verl, OpenBMB and Tsinghua University: Pioneering End-to-End Multi-Turn RLHF</font>](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/rlhf/verl/multi-turn/verl-multiturn-rollout-Release.md)
+ [<font style="color:rgb(9, 105, 218);">Reinforcement Learning from Human Feedback on AMD GPUs with verl and ROCm Integration</font>](https://rocm.blogs.amd.com/artificial-intelligence/verl-large-scale/README.html)
+ [<font style="color:rgb(9, 105, 218);">veMLP x verl ：玩转强化学习训练</font>](https://mp.weixin.qq.com/s/7nbqxk4knMGd-hQE9ls2tA)
+ [<font style="color:rgb(9, 105, 218);">使用 verl 进行 GRPO 分布式强化学习训练最佳实践</font>](https://www.volcengine.com/docs/6459/1463942)
+ [<font style="color:rgb(9, 105, 218);">HybridFlow verl 原文浅析</font>](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/rlhf/verl/readme.md)
+ [<font style="color:rgb(9, 105, 218);">最高提升 20 倍吞吐量！豆包大模型团队发布全新 RLHF 框架，现已开源！</font>](https://team.doubao.com/en/blog/%E6%9C%80%E9%AB%98%E6%8F%90%E5%8D%8720%E5%80%8D%E5%90%9E%E5%90%90%E9%87%8F-%E8%B1%86%E5%8C%85%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9B%A2%E9%98%9F%E5%8F%91%E5%B8%83%E5%85%A8%E6%96%B0-rlhf-%E6%A1%86%E6%9E%B6-%E7%8E%B0%E5%B7%B2%E5%BC%80%E6%BA%90)

# OpenRLHF <font style="color:#D22D8D;"></font>
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

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1761212857246-bd342764-8b1d-4071-8b6f-a838eea0efd7.png)

:::color5
**<font style="color:#601BDE;">1.创新点 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(31, 35, 40);">简单易用</font>**<font style="color:rgb(31, 35, 40);">: OpenRLHF 是目前可用的最简单的高性能 RLHF 库之一，无缝兼容 Huggingface 模型和数据集。</font>
+ **<font style="color:rgb(31, 35, 40);">高性能</font>**<font style="color:rgb(31, 35, 40);">: RLHF 训练中 80% 的时间用于样本生成阶段。得益于使用 Ray, Packing Samples 以及 vLLM 生成加速的能力，OpenRLHF 的性能是极致优化的 DeepSpeedChat with Hybrid Engine 的3~4倍以上。</font>
+ **<font style="color:rgb(31, 35, 40);">分布式 RLHF</font>**<font style="color:rgb(31, 35, 40);">: OpenRLHF 使用 Ray 将 Actor、Reward、Reference 和 Critic 模型分布到不同的 GPU 上，同时将 Adam 优化器放在 CPU 上。这使得使用多个 A100 80G GPU 和 vLLM 可以全面微调超过 70B+ 的模型 以及在多个 24GB RTX 4090 GPU 上微调 7B 模型。</font>
+ **<font style="color:rgb(31, 35, 40);">Hybrid Engine</font>**<font style="color:rgb(31, 35, 40);">: OpenRLHF 还支持 Hybrid engine，所有训练引擎和推理引擎共用 GPU 来避免资源闲置。</font>
+ **<font style="color:rgb(31, 35, 40);">PPO 实现技巧</font>**<font style="color:rgb(31, 35, 40);">: 集成了 PPO 的实现技巧以提高训练稳定性，详情参考 </font>[知乎](https://zhuanlan.zhihu.com/p/622134699)<font style="color:rgb(31, 35, 40);"> 和 </font>[Notion blog](https://hijkzzz.notion.site/rlhf-implementation-tricks?v=158d9a33ecc98132bf9e000c39227361)<font style="color:rgb(31, 35, 40);">.</font>

:::color5
**<font style="color:#601BDE;">2.PPO支持矩阵 </font>**<font style="color:#D22D8D;"></font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743417876145-59b7fe89-e01c-467d-8bac-aacb0e9afe1c.png)

:::color5
**<font style="color:#601BDE;">3.Scheduling Optimization 调度优化 </font>**<font style="color:#D22D8D;"></font>

:::

OpenRLHF的射线架构（Ray）。RLHF中的四个模型分布在不同的Ray的GPU，也可以自由合并或卸载以节省GPU。vLLM用于加速 actor生成。OpenRLHF使用NVIDIA Collective Communications Library（NCCL）将ZeRO引擎的权重同步到vLLM引擎。

我们的调度器设计允许使用Ray和DeepSpeed进行灵活的模型合并或卸载策略。例如，可以**<font style="color:#74B602;">合并actor,reference或critic,reward模型以节省GPU资源</font>**。除了高度可定制的算法实现的好处外，调度器还通过优化GPU来提高整体训练性能。下一节将讨论更多细节，但调度器优化是进一步提高效率的基石。

 Scheduling Optimization

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743417273664-d8eea981-9ec4-4911-89bf-e68429cc6c19.png)

:::color5
**<font style="color:#601BDE;">4.RLHF生成阶段 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

OpenRLHF的设计支持灵活放置具有各种算法实现的多个模型。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743672338227-214cd0c0-ddd2-41ae-8ce0-c348f55ecb13.png)

:::color5
**<font style="color:#601BDE;">5.RLHF学习阶段 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

OpenRLHF安排了两个可学习的模型，以最大限度地提高整体训练吞吐量

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743672330560-29bbad45-e8da-4658-903d-501eb44bb9e3.png)

:::color5
**<font style="color:#601BDE;">6.便捷使用 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

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
**<font style="color:#601BDE;">7.不同框架对比 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743417239914-442c429b-1989-4049-b33b-3b013d77af79.png)

**RLHF框架比较**：OpenRLHF支持使用Ray的多奖励模型，并使用vLLM加速流行的HuggingFace模型。与Hugging Face库的兼容性确保了该框架的用户友好性。

**Limits**：DSChat的HybridEngine仅支持有限范围的模型架构，例如[Deepspeed](https://github.com/microsoft/DeepSpeed/issues/4954.)相比之下，OpenRLHF支持所有主流架构，包括使用DeepSpeed和vLLM的MoE，请参阅文档[vLLM教程](https://docs.vllm.ai/en/latest/models/supported_)

