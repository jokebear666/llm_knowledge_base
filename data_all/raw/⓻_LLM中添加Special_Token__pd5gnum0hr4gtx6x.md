# ⓻ LLM中添加Special Token

<!-- source: yuque://zhongxian-iiot9/hlyypb/pd5gnum0hr4gtx6x -->

# <font style="color:rgb(63, 63, 63);">Special Token</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(63, 63, 63);">在SFT（Supervised Fine-Tuning）阶段为LLM添加special_token（例如用于分隔用户和助手的</font>`<font style="color:#5C8D07;"><|user|>，<|assistant|></font>`<font style="color:rgb(63, 63, 63);">等）是一个非常常见的操作，但如果处理不当，确实会严重影响模型原有的性能。</font>

:::

:::color3
**简介：**<font style="color:rgb(63, 63, 63);">为了尽可能保持原模型的训练效果，你需要遵循一套系统性的策略，核心思想是：</font>**<font style="color:#ED740C;">让新token的初始状态尽可能“平滑”地融入现有模型，并通过高效的微调方式让模型“温柔”地学会其用法</font>**<font style="color:rgb(63, 63, 63);">。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758529354931-d489cb39-c1ad-469a-93f3-33a92514d9c8.png)

# <font style="color:rgb(63, 63, 63);">核心问题所在</font>
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">核心问题在于：</font><font style="color:#000000;">新添加的token在模型的</font>**<font style="color:#ED740C;">词向量矩阵（Embedding Matrix）和输出层（LM Head）中没有对应的、经过预训练的向量</font>**<font style="color:#000000;">，它们是“从零开始”的，这会给模型带来巨大的扰动。</font>

:::

:::color5
**<font style="color:#601BDE;">1.核心问题 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:#117CEE;">随机初始化的Embedding</font>**<font style="color:rgb(63, 63, 63);">：当你调用</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">model.resize_token_embeddings()</font>`<font style="color:rgb(63, 63, 63);">时，新增的token向量默认是随机初始化的。这个随机向量与模型中其他经过数十亿token预训练、具有丰富语义信息的向量相比，完全是“噪声”。模型在处理它时会感到困惑。</font>
2. **<font style="color:#117CEE;">随机初始化的LM Head</font>**<font style="color:rgb(63, 63, 63);">：同样，在模型的输出层（通常是</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">lm_head</font>`<font style="color:rgb(63, 63, 63);">），也增加了一个新的、随机初始化的logit，模型在预测这个新token时完全是瞎猜。</font>
3. **<font style="color:#117CEE;">训练初期的梯度震荡</font>**<font style="color:rgb(63, 63, 63);">：在SFT初期，当模型遇到这些新token时，会产生巨大的loss和梯度，这些梯度会反向传播并剧烈地更新模型参数，可能会破坏掉模型在预训练阶段学到的通用知识，导致“灾难性遗忘”（Catastrophic Forgetting）。</font>

# <font style="color:rgb(63, 63, 63);">核心步骤</font>
### <font style="color:rgb(63, 63, 63);">步骤一：向Tokenizer中添加新Token</font>
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">这是基础操作，确保你的tokenizer能够识别和编码新的特殊token。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 定义新的特殊token
special_tokens_to_add = ["<|user|>", "<|assistant|>", "<|endoftext|>"] 

# 添加到tokenizer
tokenizer.add_special_tokens({
    "additional_special_tokens": special_tokens_to_add,
    "pad_token": "<|endoftext|>" # 也可以用已有的，或新加一个
})

# 验证一下
print(f"Tokenizer vocabulary size: {len(tokenizer)}")
```

### <font style="color:rgb(63, 63, 63);">步骤二：调整模型Embedding和LM Head的大小</font>
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">模型需要知道词汇表变大了，并为新token分配空间。</font>

:::

```python
model.resize_token_embeddings(len(tokenizer))

print(f"Model input embedding size: {model.get_input_embeddings().weight.shape[0]}")
print(f"Model output head size: {model.get_output_embeddings().weight.shape[0]}")
```

### <font style="color:rgb(63, 63, 63);">步骤三：【最关键】初始化新Token的Embedding</font>
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">不要使用默认的随机初始化！这是保持模型性能的关键。你有以下几种优质选择：</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">策略A：使用现有Token Embedding的均值（最推荐、最通用）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">这种方法假设新token的语义应该是一个“中性”的、不带来强烈偏见的起始点。取所有或部分现有token embedding的平均值，可以有效地将新token放置在语义空间的中心位置，减少对模型的初始冲击。</font>

```python
import torch

# 获取旧的embedding矩阵和lm_head矩阵
input_embeddings = model.get_input_embeddings()
output_embeddings = model.get_output_embeddings()

# 计算旧词汇表的平均embedding
old_vocab_size = input_embeddings.weight.shape[0] - len(special_tokens_to_add)
avg_embedding = input_embeddings.weight.data[:old_vocab_size].mean(dim=0, keepdim=True)

# 将这个平均值赋给所有新的token
with torch.no_grad():
    # 初始化input embeddings
    input_embeddings.weight.data[old_vocab_size:] = avg_embedding.clone()

    # 如果lm_head和input_embeddings是绑定的，这一步可能不是必须的，但为了保险起见可以做
    if output_embeddings is not None and output_embeddings.weight.shape[0] == len(tokenizer):
        output_embeddings.weight.data[old_vocab_size:] = avg_embedding.clone()

print("New special token embeddings have been initialized with the average of old embeddings.")
```

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">策略B：使用语义相近的Token Embedding</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">如果你的新token有明确的语义，可以找一个或多个现有的、语义相近的token来初始化它。 例如，对于<|user|>，你可以使用 “user”, “User”, “human” 等token的embedding的平均值。</font>

```python
# 示例：用 "user" 和 "assistant" 的embedding来初始化
user_token_id = tokenizer.encode("user", add_special_tokens=False)[0]
assistant_token_id = tokenizer.encode("assistant", add_special_tokens=False)[0]

user_embedding = input_embeddings.weight.data[user_token_id].clone()
assistant_embedding = input_embeddings.weight.data[assistant_token_id].clone()

new_user_token_id = tokenizer.convert_tokens_to_ids("<|user|>")
new_assistant_token_id = tokenizer.convert_tokens_to_ids("<|assistant|>")

with torch.no_grad():
    input_embeddings.weight.data[new_user_token_id] = user_embedding
    input_embeddings.weight.data[new_assistant_token_id] = assistant_embedding
    # ... 对其他新token和lm_head做同样操作
这种方法更精确，但操作更繁琐，且不一定总能找到合适的对应词。
```

### <font style="color:rgb(63, 63, 63);">步骤四：选择合适的微调方法</font>
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">初始化完成后，如何训练也至关重要。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">策略A：使用PEFT（如LoRA）进行微调（强烈推荐）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">Parameter-Efficient Fine-Tuning (PEFT) 是保持原模型性能的利器。LoRA（Low-Rank Adaptation）通过在模型的线性层旁边增加小型的、可训练的“适配器”矩阵来进行微调，而</font>**<font style="color:rgb(250, 81, 81);">原始模型的绝大部分权重保持冻结</font>**<font style="color:rgb(63, 63, 63);">。</font>

+ <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(250, 81, 81);">为什么有效？</font>**<font style="color:rgb(63, 63, 63);"> 因为它不会去剧烈改动预训练好的权重，从而最大程度地保留了模型的通用能力。训练的重点放在了学习新token的用法和遵循SFT指令上。</font>
+ <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(250, 81, 81);">操作</font>**<font style="color:rgb(63, 63, 63);">：在使用peft库时，你可以选择将embed_tokens和lm_head也作为LoRA的目标模块（target_modules），这样模型在学习LoRA适配器的同时，也能微调新token的embedding。</font>

```python
from peft import LoraConfig, get_peft_model

# 配置LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], # 根据模型结构调整
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    # modules_to_save=["embed_tokens", "lm_head"] # 这是一个选项，可以让embedding层和输出层也参与训练
)

# 应用LoRA到模型
peft_model = get_peft_model(model, lora_config)
peft_model.print_trainable_parameters()
```

**<font style="color:rgb(250, 81, 81);">注意</font>**<font style="color:rgb(63, 63, 63);">：</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">modules_to_save</font>`<font style="color:rgb(63, 63, 63);">会让指定的模块（如embedding层）进行全参数微调，而不是LoRA微调。这对于新token是必要的，因为它们需要从头学习。LoRA则保护了其他层的权重。</font>

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">策略B：分阶段微调（如果不用LoRA）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">如果你坚持全量微调（Full Fine-tuning），可以考虑一个“预热”阶段：</font>

+ **<font style="color:rgb(250, 81, 81);">第一阶段</font>**<font style="color:rgb(63, 63, 63);">：冻结模型绝大部分层，只训练embed_tokens和lm_head层。使用包含新token的语料进行少量步数的训练。这能让新token的embedding先“稳定下来”，找到一个比较合理的位置。</font>
+ **<font style="color:rgb(250, 81, 81);">第二阶段</font>**<font style="color:rgb(63, 63, 63);">：解冻所有层，进行完整的SFT。这种方法比直接全量微调要平滑，但比LoRA更耗资源且风险更高。</font>

# <font style="color:rgb(63, 63, 63);">总结与最佳实践</font>
:::color3
**简介：**<font style="color:rgb(63, 63, 63);">遵循以上策略，你就可以在SFT阶段平稳地引入</font>`**<font style="color:#ED740C;background-color:rgba(27, 31, 35, 0.05);">special_token</font>**`<font style="color:rgb(63, 63, 63);">，同时最大程度地保留大模型强大的基础能力</font>

:::

1. **<font style="color:rgb(250, 81, 81);">添加Token</font>**<font style="color:rgb(63, 63, 63);">：使用</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">tokenizer.add_special_tokens</font>`<font style="color:rgb(63, 63, 63);">。</font>
2. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(250, 81, 81);">调整模型大小</font>**<font style="color:rgb(63, 63, 63);">：使用</font>`<font style="color:rgb(221, 17, 68);background-color:rgba(27, 31, 35, 0.05);">model.resize_token_embeddings</font>`<font style="color:rgb(63, 63, 63);">。</font>
3. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(250, 81, 81);">智能初始化（关键）：强烈推荐使用所有旧token embedding的均值来初始化新token的embedding</font>**<font style="color:rgb(63, 63, 63);">。这是效果和简便性之间最好的平衡。</font>
4. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(250, 81, 81);">高效微调（关键）：强烈推荐使用LoRA进行SFT</font>**<font style="color:rgb(63, 63, 63);">。它能有效防止灾难性遗忘，将训练的“火力”集中在任务适应和新token学习上，而不是破坏原有知识。确保SFT数据中充分、正确地使用了这些新token。</font>
5. <font style="color:rgb(63, 63, 63);"></font>**<font style="color:rgb(250, 81, 81);">数据质量</font>**<font style="color:rgb(63, 63, 63);">：确保你的SFT数据格式统一，新添加的special_token被正确地用作结构分隔符。模型需要通过大量高质量的样本来学习它们的“语法”功能。</font>
6. **<font style="color:rgb(250, 81, 81);">评估</font>**<font style="color:rgb(63, 63, 63);">：在SFT后，不仅要评估模型在目标任务上的表现，还应该在一些通用的基准（如MMLU、C-Eval）上进行测试，以检查模型的通用能力是否出现大幅下降。</font>

