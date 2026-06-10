# ⓼ 大模型微调实战：Qwen2.5-7B

<!-- source: yuque://zhongxian-iiot9/hlyypb/kue09vol1xy7z06q -->

# <font style="color:rgba(0, 0, 0, 0.9);">一、训练全流程总览</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(15, 17, 21);">随着大模型技术的快速发展，如何高效地对通用基座模型进行领域适配与能力对齐成为关键挑战。Qwen2.5-7B等开源模型为微调实践提供了良好基础，本文以实战为导向，系统介绍从预训练、SFT到偏好对齐的全流程微调方法，结合代码示例，助力开发者快速实现领域模型的高效定制。</font>

:::

:::color3
**简介：**本文包含以下内容

+ <font style="color:rgba(0, 0, 0, 0.9);">概念与流程：预训练 → 继续预训练（领域自适应） → 指令微调（SFT） → 偏好对齐（DPO/ORPO/KTO） → 强化学习对齐（PPO）。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">可复用的代码模板：Hugging Face/TRL/PEFT、ms-swift 命令行。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">LoRA/QLoRA 的落地做法（rank、target_modules、合并权重）。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">数据格式与 chat 模板的关键坑位（Qwen 的 chat_template）。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758250317358-14900afe-cf6d-407a-97eb-5594bb93856b.png)

:::color5
**<font style="color:#601BDE;">1.说明 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">代码示例默认以 Qwen/Qwen2.5-7B(-Instruct) 为例。如果你已有 Qwen3 的 HuggingFace 权重，直接把 MODEL_ID 换成对应 id 即可。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">GPU 建议：SFT/QLoRA 单卡 24–48GB 足够（batch 小一点 + 累积梯度）；PPO/DPO 视模型大小和数据量，一般多卡更舒适。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">环境建议：transformers>=4.41, trl>=0.8, peft>=0.11, bitsandbytes>=0.43, datasets, accelerate, deepspeed（可选）。</font>

:::color5
**<font style="color:#601BDE;">2.流程总览</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758250367068-ada98179-b02e-4965-a8ab-32bf3b532370.png)

+ <font style="color:rgba(0, 0, 0, 0.9);">预训练（Pretraining）</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">目标：大规模无监督自回归（next-token prediction），学习通用语言能力。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">数据：网页、代码、书籍，多语种清洗、去重、毒性过滤。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">继续预训练（Continued/Domain Adaptive Pretraining）</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">用你的领域语料（金融/法务/医疗/企业内部知识）对基础模型再训练数万步，提升领域覆盖与术语分布。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">指令微调（SFT）</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">用指令-回答/对话样本教模型“按指令办事”。常配合 LoRA/QLoRA 降显存。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">偏好对齐（Alignment）</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">DPO/ORPO/KTO/SimPO：用偏好对（preferred vs rejected）做直接对比优化。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">RLHF（PPO/RLAIF/GRPO）：用奖励模型/规则/AI 反馈作为奖励信号做策略优化。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">安全与工具能力</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">安全基座（拒答/去有害）、工具使用（函数调用）、检索增强（RAG）。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">评测与蒸馏</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">任务集评测（MMLU、C-Eval、GSM8K、AlignBench 等），蒸馏成小模型部署。</font>

# <font style="color:rgb(52, 54, 61);background-color:rgb(253, 253, 254);">二、环境安装（通用）</font>
```bash
# 基础依赖
pip install -U "transformers>=4.41" "datasets>=2.19" "accelerate>=0.33" "peft>=0.11" \
               "trl>=0.8" "bitsandbytes>=0.43" "evaluate" "scikit-learn"
# 可选：deepspeed/flash-attn（需要匹配 CUDA 环境）
pip install -U deepspeed
# pip install flash-attn --no-build-isolation  # 仅在你确认环境匹配时装
```

# <font style="color:rgba(0, 0, 0, 0.9);">三、继续预训练（领域自适应 Pretraining）</font>
:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">适合你已有一批纯文本/代码语料，想让基础模型更懂你的领域。</font>

:::

:::color5
**<font style="color:#601BDE;">1.数据准备（举例）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">data/train.txt 与 data/val.txt：每行一段原始文本（已清洗去重）。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">继续预训练用“base”模型（非 Instruct）更合适。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">启用 packing（group_texts）能显著提高吞吐。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">大模型建议配合 DeepSpeed ZeRO-2/3、多卡和梯度检查点。</font>

```python
import os, torch
from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments,
default_data_collator)
MODEL_ID = "Qwen/Qwen2.5-7B"  # 若你有 Qwen3 base，换成对应 id
BLOCK_SIZE = 4096
# 1) 数据集
ds = load_dataset("text", data_files={"train": "data/train.txt", "validation": "data/val.txt"})
# 2) 分词
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"
def tokenize_fn(batch):
    return tokenizer(batch["text"])
tokenized = ds.map(tokenize_fn, batched=True, remove_columns=["text"])
def group_texts(examples):
    # 拼接后按 BLOCK_SIZE 切块（提高吞吐）
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = (len(concatenated["input_ids"]) // BLOCK_SIZE) * BLOCK_SIZE
    result = {
        k: [t[i:i+BLOCK_SIZE] for i in range(0, total_length, BLOCK_SIZE)]
        for k, t in concatenated.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result
lm_dataset = tokenized.map(group_texts, batched=True)
# 3) 模型
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)
model.gradient_checkpointing_enable()
model.config.use_cache = False  # 训练时关闭缓存
# 4) 训练器
args = TrainingArguments(
    output_dir="outputs/qwen-continued-pretrain",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    learning_rate=1e-4,
    num_train_epochs=1,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=10,
    save_steps=1000,
    save_total_limit=2,
    bf16=True,
    weight_decay=0.1,
    report_to="none",
    dataloader_num_workers=4,
    # deepspeed="ds_zero2.json",  # 可选：大模型建议开启
)
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=lm_dataset["train"],
    eval_dataset=lm_dataset["validation"],
    data_collator=default_data_collator,
)
trainer.train()
trainer.save_model("outputs/qwen-continued-pretrain/ckpt")
tokenizer.save_pretrained("outputs/qwen-continued-pretrain/ckpt")
```

# <font style="color:rgba(0, 0, 0, 0.9);">四、指令微调 SFT（LoRA/QLoRA）</font>
:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">数据格式（推荐 messages 格式，方便套 chat_template）</font>

:::

:::color5
**<font style="color:#601BDE;">1.数据准备</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">train.jsonl（每行一个样本）：</font>

```json
{"messages": [
  {"role":"system","content":"你是 helpful 的中文助理"},
  {"role":"user","content":"用 3 点说明 LoRA 的优势"},
  {"role":"assistant","content":"1) 显存友好 ... 2) 速度快 ... 3) 易于迁移 ..."}
]}
```

+ <font style="color:rgb(52, 54, 61);background-color:rgb(253, 253, 254);">代码（TRL + PEFT，QLoRA）</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">target_modules 对 Qwen/LLaMA 系列常见投影层足够；实际以模型结构为准可做微调。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">QLoRA 推荐 r=16/32，learning_rate 2e-4~5e-5 视 batch/任务而定。</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">数据用 messages + chat_template 能避免标签错位、特殊 token 漏标等坑。</font>

```python
import torch
from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig)
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"  # 若有 Qwen3-Instruct，替换即可
DATA_PATH = "data/train.jsonl"
# 1) 量化配置（QLoRA）
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
# 2) tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"
# 3) 模型（4bit 量化）
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    quantization_config=bnb_config,
    device_map="auto",
)
model = prepare_model_for_kbit_training(model)
model.config.use_cache = False
# 4) LoRA 配置（Qwen/LLaMA 系常见 target_modules）
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    task_type="CAUSAL_LM",
    bias="none",
)
# 5) 数据集 + 应用 chat_template
raw = load_dataset("json", data_files={"train": DATA_PATH})
def to_text(example):
    # 将 messages 用 Qwen 的 chat_template 拼接成可训练文本
    prompt = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False,
        add_generation_prompt=False  # 训练时不加生成提示
    )
    return {"text": prompt}
dataset = raw["train"].map(to_text)
# 6) 训练参数
args = SFTConfig(
    output_dir="outputs/qwen-sft-lora",
    num_train_epochs=2,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=10,
    save_steps=500,
    bf16=True,
    max_seq_length=4096,
    packing=True,  # 将多样本 pack 进长序列，提高吞吐
    dataset_text_field="text",
    report_to="none",
)
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=args,
    peft_config=peft_config,
)
trainer.train()
trainer.model.save_pretrained("outputs/qwen-sft-lora/adapter")
tokenizer.save_pretrained("outputs/qwen-sft-lora/adapter")
```

+ <font style="color:rgb(52, 54, 61);background-color:rgb(253, 253, 254);">合并 LoRA（推理部署更方便）</font>

```python

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
BASE = "Qwen/Qwen2.5-7B-Instruct"
ADAPTER = "outputs/qwen-sft-lora/adapter"
OUT = "outputs/qwen-sft-merged"
tokenizer = AutoTokenizer.from_pretrained(BASE, trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
model = PeftModel.from_pretrained(base_model, ADAPTER)
model = model.merge_and_unload()  # 权重合并
model.save_pretrained(OUT)
tokenizer.save_pretrained(OUT)
```

<font style="color:rgba(0, 0, 0, 0.9);"></font>

# <font style="color:rgba(0, 0, 0, 0.9);">五、用 ms-swift 快速上手（SFT / DPO）</font>
:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">不同版本的 ms-swift CLI 参数略有差异，建议先执行 swift -h 或 swift sft -h 查看你本地版本帮助。下面给出常见用法范式（以 2.x 为例）。</font>

:::

:::color5
**<font style="color:#601BDE;">1.安装</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
pip install -U "ms-swift[llm]" modelscope
```

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">SFT（LoRA/QLoRA）</font>**

:::

```python
# 假设 data/train.jsonl 是上文 messages 格式
swift sft \
  --model_id_or_path Qwen/Qwen2.5-7B-Instruct \
  --train_file data/train.jsonl \
  --dataset_format messages \
  --chat_template qwen \
  --use_lora true \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_dropout 0.05 \
  --lora_target_modules q_proj k_proj v_proj o_proj gate_proj up_proj down_proj \
  --max_seq_len 4096 \
  --packing true \
  --bf16 true \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --learning_rate 2e-4 \
  --num_train_epochs 2 \
  --output_dir outputs/qwen-sft-lora
```

:::color5
**<font style="color:#601BDE;">3.DPO（偏好对齐，使用 prompt/choice 对）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">DPO（偏好对齐，使用 prompt/choice 对）</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">数据 dpo.jsonl（每行）：</font>

```python
{"prompt":"请写一段自我介绍","chosen":"我是一个乐观...","rejected":"我是个不靠谱..."}

```

+ <font style="color:rgba(0, 0, 0, 0.9);">DPO</font>

```python

swift dpo \
  --model_id_or_path Qwen/Qwen2.5-7B-Instruct \
  --train_file data/dpo.jsonl \
  --dataset_format preference \
  --prompt_field prompt --chosen_field chosen --rejected_field rejected \
  --use_lora true \
  --lora_r 16 \
  --max_seq_len 4096 \
  --bf16 true \
  --output_dir outputs/qwen-dpo-lora
```

+ <font style="color:rgba(0, 0, 0, 0.9);">合并 LoRA</font>

```python

swift export \
  --ckpt_dir outputs/qwen-sft-lora \
  --merge_lora true \
  --out_dir outputs/qwen-sft-merged
```

<font style="color:rgba(0, 0, 0, 0.9);">备注</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">ms-swift 还支持 ORPO/KTO/GRPO/SimPO、全参/部分层微调、Deepspeed/FSDP，一行命令即可切换策略。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">如果你的 ms-swift 本地帮助与上面不一致，以本地 -h 为准。</font>

# <font style="color:rgb(52, 54, 61);background-color:rgb(253, 253, 254);">六、偏好对齐：DPO（Hugging Face TRL 版）</font>
:::color3
**简介：**适合有成对偏好数据（prompt, chosen, rejected），可在 SFT 基础上再优化。

:::

:::color5
**<font style="color:#601BDE;">1.代码</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">DPO 对 LR 更敏感，建议 5e-6~2e-5。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">数据质量很关键：prompt 明确、chosen/rejected 差异清晰。</font>

```python
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig
from trl import DPOTrainer, DPOConfig
BASE = "Qwen/Qwen2.5-7B-Instruct"   # 或你上一步 SFT 合并后的权重
DATA = "data/dpo.jsonl"
tokenizer = AutoTokenizer.from_pretrained(BASE, use_fast=True, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
ds = load_dataset("json", data_files={"train": DATA})["train"]
# 数据字段需要是 prompt/chosen/rejected 字段的纯文本
# 如果你存的是 messages，需要先用 chat_template 生成 prompt 再映射
peft_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    task_type="CAUSAL_LM",
)
model = AutoModelForCausalLM.from_pretrained(
    BASE, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto"
)
model.config.use_cache = False
config = DPOConfig(
    output_dir="outputs/qwen-dpo-lora",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    learning_rate=5e-6,      # DPO 通常更小 LR
    num_train_epochs=1,
    max_length=1024,
    max_prompt_length=768,
    beta=0.1,                # 温度超参
    logging_steps=10,
    save_steps=500,
    bf16=True,
    report_to="none",
)
trainer = DPOTrainer(
    model=model,
    args=config,
    tokenizer=tokenizer,
    train_dataset=ds,
    peft_config=peft_config,
    # ref_model=None  # 省略则默认克隆一个参考模型；显存吃紧时可考虑传入 8bit/4bit 的 ref
)
trainer.train()
trainer.model.save_pretrained("outputs/qwen-dpo-lora/adapter")
tokenizer.save_pretrained("outputs/qwen-dpo-lora/adapter")
```

# <font style="color:rgb(52, 54, 61);background-color:rgb(253, 253, 254);">七、强化学习对齐：PPO（TRL）</font>
:::color3
**简介：**PPO 需要一个“奖励函数”。真实场景常用专门的 Reward Model（例如对 helpfulness/harmlessness 的打分）。这里给一个可跑通的演示版，用情感模型（正面=高分）代替。你可以替换为自己的 RM。

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">真实对齐要用与你任务匹配的 Reward Model（如中文对齐 RM、规则奖励或 RLAIF）。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">控制 KL（target_kl）避免模型崩坏；LR、采样温度、奖励量纲都很关键。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">PPO 显存较吃，建议小 batch + 累积，必要时 LoRA 化 PPO（进阶用法）。</font>

```python
import torch, random
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead, set_seed
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
REWARD_MODEL = "lvwerra/distilbert-imdb"  # 演示用；换成你的中文 Reward Model 更合理
set_seed(42)
# 1) 模型与分词器
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
policy = AutoModelForCausalLMWithValueHead.from_pretrained(
    MODEL_ID, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True
)
policy.config.use_cache = False
# 2) 奖励模型（分类打分，示例）
rm_tokenizer = AutoTokenizer.from_pretrained(REWARD_MODEL, use_fast=True)
reward_model = AutoModelForSequenceClassification.from_pretrained(
    REWARD_MODEL, torch_dtype=torch.bfloat16, device_map="auto"
)
def compute_reward(texts):
    # 返回一个 list[float] 作为奖励；这里用情感正面概率当奖励
    with torch.no_grad():
        inputs = rm_tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(reward_model.device)
        logits = reward_model(**inputs).logits
        if logits.shape[-1] == 2:
            probs = torch.softmax(logits, dim=-1)[:, 1]  # positive prob
            return probs.detach().float().cpu().tolist()
        else:
            # 若是回归 RM，直接取值
            return logits.squeeze(-1).detach().float().cpu().tolist()
# 3) 构造 PPO 数据集（prompt 列）
prompts = [
    "写一段鼓励同事的中文短文。",
    "给出 3 条积极向上的生活建议。",
    "请用友善的语气回答：如何学习新技术更有效？",
    "写一段对用户的正面反馈。"
]
ppo_ds = Dataset.from_dict({"prompt": prompts})
# 4) PPO 配置
config = PPOConfig(
    model_name=MODEL_ID,
    learning_rate=1e-6,          # PPO 通常更小 LR
    batch_size=4,
    mini_batch_size=2,
    gradient_accumulation_steps=4,
    target_kl=0.1,
    ppo_epochs=4,
    log_with=None,
)
trainer = PPOTrainer(
    config=config,
    model=policy,
    tokenizer=tokenizer,
    dataset=ppo_ds,
)
# 5) 训练循环（示例：小步数演示）
gen_kwargs = dict(max_new_tokens=128, top_p=0.9, temperature=0.7, do_sample=True)
for epoch in range(2):
    for batch in trainer.dataloader:
        queries = batch["prompt"]
        # a) 生成回复
        query_tensors = [tokenizer(q, return_tensors="pt").to(policy.device)["input_ids"][0] for q in queries]
        responses = []
        response_tensors = []
        for q_t in query_tensors:
            r_t = trainer.generate(q_t.unsqueeze(0), **gen_kwargs)
            response_tensors.append(r_t[0])
            responses.append(tokenizer.decode(r_t[0], skip_special_tokens=True))
        # b) 计算奖励（对 prompt+response 文本）
        texts = []
        for q, r in zip(queries, responses):
            texts.append(q + "\n" + r)
        rewards = compute_reward(texts)
        rewards = [torch.tensor(reward).to(policy.device) for reward in rewards]
        # c) PPO 更新
        stats = trainer.step(query_tensors, response_tensors, rewards)
        trainer.log_stats(stats, batch, rewards)
# 保存
policy.save_pretrained("outputs/qwen-ppo")
tokenizer.save_pretrained("outputs/qwen-ppo")
```

# <font style="color:rgb(52, 54, 61);background-color:rgb(253, 253, 254);">八、评测、部署与常见坑</font>
:::color5
**<font style="color:#601BDE;">1.评测</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">综合：MMLU（中英）、C-Eval（中文学科）、GSM8K（数学）、BBH、AlignBench（对齐）。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">指标：准确率、长度、拒答率（安全）、幻觉率（可人工/自动评测结合）。</font>

:::color5
**<font style="color:#601BDE;">2.部署</font>**

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">vLLM 高吞吐推理；支持 LoRA 热插拔、KV Cache、连续批处理。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">量化：AWQ/GPTQ（离线），bitsandbytes（在线 8/4bit）。</font>

:::color5
**<font style="color:#601BDE;">3.常见坑</font>**

:::

+ <font style="color:rgba(0, 0, 0, 0.9);">Chat 模板：messages → apply_chat_template 必须一致，训练/推理同模板。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">标签错位：SFT 时确保只有 assistant 段落有 label，prompt 部分 label 应该是 -100（用模板正确构造可避免）。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">Max length 截断：训练/生成的 max_length 与模型 rope/rope_scaling 要一致。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">LoRA 目标层：不同架构名称可能略有不同，先 print(model) 或参考官方配置。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">数据清洗：去重、去噪、脱敏；不良样本少量也会严重拖后腿。</font>

