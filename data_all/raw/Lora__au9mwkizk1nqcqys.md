# Lora

<!-- source: yuque://zhongxian-iiot9/hlyypb/au9mwkizk1nqcqys -->

# 总结
| **方法** | **核心改进** | **参数量** | **显存占用** | **计算开销** | **适用场景** |
| --- | --- | --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">LoRA</font>** | <font style="color:rgb(51, 51, 51);">低秩分解固定秩</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">通用高效微调</font> |
| **<font style="color:rgb(51, 51, 51);">QLoRA</font>** | <font style="color:rgb(51, 51, 51);">4-bit量化 + LoRA</font> | <font style="color:rgb(51, 51, 51);">最低</font> | <font style="color:rgb(51, 51, 51);">最低</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">显存严格受限</font> |
| **<font style="color:rgb(51, 51, 51);">AdaLoRA</font>** | <font style="color:rgb(51, 51, 51);">动态调整秩</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">高性能需求</font> |


**选择建议：**

+ <font style="color:rgb(51, 51, 51);">显存不足 → QLoRA</font>
+ <font style="color:rgb(51, 51, 51);">均衡参数效率与效果 → LoRA</font>
+ <font style="color:rgb(51, 51, 51);">追求最佳效果 → AdaLoRA</font>



### `<font style="color:#601BDE;">1. LoRA的背景&原理</font>`<font style="color:#D22D8D;">（by草莓师姐）</font>
:::warning
**<font style="color:#1f2329;">简介</font>**<font style="color:#1f2329;">：在预训练⼤规模模型时，微调整个模型的参数可能会带来较⼤的计算和存储开销。对于像 LLAMA、Qwen这样的⼤型模型，直接微调所有参数不仅⾮常耗时，还需要⼤量的存储资源。</font>

:::

### `<font style="color:#601BDE;">2. LoRA的原理</font>`<font style="color:#D22D8D;">（by草莓师姐）</font>
<font style="color:#1f2329;">LoRA 通过引⼊</font>**<u><font style="color:#ED740C;">低秩矩阵分解，</font></u>**<font style="color:#1f2329;">在微调时不再调整原始模型的所有权重，⽽是通过将权重矩阵分解成两个较⼩的低秩矩阵来表⽰权重的变化。尽管预训练模型拥有⼤量的参数，</font>**<font style="color:#601BDE;background-color:#D9DFFC;">但许多参数在特定任务的微   调过程中实际上是不活跃的</font>**<font style="color:#1f2329;">。LoRA通过低秩分解的⽅式，只更新那些对特定任务最重要的参数，这样  做可以在保持模型性能的同时，显著减少微调所需的计算资源和时间。</font>

<font style="color:#1f2329;">假设某个层的权重矩阵为 W∈R</font><sup><font style="color:#1f2329;">d×k</font></sup><font style="color:#1f2329;">  ，LoRA 不微调 W本⾝ ，⽽是通过两个低秩矩阵 A∈R</font><sup><font style="color:#1f2329;">d×r</font></sup><font style="color:#1f2329;">和B∈R</font><sup><font style="color:#1f2329;">r×k</font></sup><font style="color:#1f2329;">来近似微调权重矩阵。LoRA 的权重更新公式为：</font>

:::success
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741247466604-557c1bf5-d5be-447f-b3b1-248b3a32a9bd.png)



:::

:::success
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740802848765-4a5854c3-0ebf-4809-b37f-ebc86cb9ebb3.png)

+ _<font style="color:#1f2329;">W</font>_<sub><font style="color:#1f2329;">new</font></sub><font style="color:#1f2329;">：微调后的权重矩阵。</font>
+ <font style="color:#1456f0;"></font>_<font style="color:#1f2329;">W </font>_<font style="color:#1f2329;">：预训练模型的原始权重矩阵 ，保持不变。</font>
+ _<font style="color:#1f2329;">A </font>_<font style="color:#1f2329;">和 </font>_<font style="color:#1f2329;">B  </font>_<font style="color:#1f2329;">：低秩矩阵 ， </font>_<font style="color:#1f2329;">A </font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">近似于权重变化量 </font><font style="color:#1f2329;">Δ</font>_<font style="color:#1f2329;">W </font>_<font style="color:#1f2329;">。</font>
+ _<font style="color:#1f2329;">α  </font>_<font style="color:#1f2329;">：⼀个缩放因⼦ ，⽤来调节低秩矩阵的影响。</font>
+ _<font style="color:#1f2329;">r  </font>_<font style="color:#1f2329;">：秩的⼤⼩，表⽰低秩矩阵</font>_<font style="color:#1f2329;">A</font>_<font style="color:#1f2329;">和</font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">的维度，通常</font>_<font style="color:#1f2329;">r </font>_<font style="color:#1f2329;">≪ </font>_<font style="color:#1f2329;">d</font>_<font style="color:#1f2329;">, </font>_<font style="color:#1f2329;">k </font>_<font style="color:#1f2329;">，从⽽⼤⼤减少需要训练的参数数量。</font>

:::

:::danger
<font style="color:#1f2329;">LoRA 的核⼼思想是将权重的变化 </font><font style="color:#1f2329;">Δ</font>_<font style="color:#1f2329;">W</font>_<font style="color:#1f2329;">通过两个⼩型矩阵的乘积进⾏表⽰，</font>**<font style="color:#ED740C;">利⽤低秩矩阵分解的⽅式有效降低参数量</font>**<font style="color:#1f2329;">。这样只需要训练低秩矩阵的参数，⽽不是完整的权重矩阵。</font>

:::

### `<font style="color:#601BDE;">3. LoRA的优点</font>`<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**高效性：**<font style="color:#1f2329;">通过低秩矩阵分解，⼤幅减少了需要微调  的参数量。在⼤规模  预训练模型中，LoRA仅引⼊⼀⼩部分新的  参数，节省了存储空  间和计算开销。</font>

:::

:::color3
**<font style="color:#1f2329;">冻结主⼲模型：</font>**<font style="color:#1f2329;">LoRA 保持原始模型的主⼲   权重</font>_<font style="color:#1f2329;">W </font>_<font style="color:#1f2329;">不变，仅调   整</font>_<font style="color:#1f2329;">A</font>_<font style="color:#1f2329;">和</font>_<font style="color:#1f2329;">B</font>_<font style="color:#1f2329;">矩阵。这使得可以在多个任务  之间共享同⼀个预训  练模型，⽽不同任务  只需要微调少量的低  秩矩阵。</font>

:::

:::color3
**<font style="color:#1f2329;">通⽤性强：</font>**<font style="color:#1f2329;">LoRA 可以应⽤在模型的多种层次结构（如   ⾃注意⼒层、前馈⽹   络层等），⼴泛适⽤   于各类Transformer   模型。</font>

<font style="color:#1f2329;"></font>

:::



# LoRA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">LoRA 的核⼼思想是将权重的变化 </font><font style="color:#1f2329;">Δ</font>_<font style="color:#1f2329;">W</font>_<font style="color:#1f2329;">通过两个⼩型矩阵的乘积进⾏表⽰，</font>**<font style="color:#d83931;">利⽤低秩矩阵分解的⽅式有效降低参数量</font>**<font style="color:#1f2329;">。这样只需要训练低秩矩阵的参数，⽽不是完整的权重矩阵。</font>

:::

**背景：**<font style="color:#1f2329;">在预训练⼤规模模型时，微调整个模型的参数可能会带来较⼤的计算和存储开销。对于LLM这样的⼤型模型，直接微调所有参数不仅⾮常耗时，还需要⼤量的存储资源。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741247466604-557c1bf5-d5be-447f-b3b1-248b3a32a9bd.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:#1f2329;">LoRA 通过引⼊</font><font style="color:#d83931;">低秩矩阵分解</font><font style="color:#1f2329;">，在微调时不再调整原始模型的所有权重，⽽是通过将权重矩阵分解成两个较⼩的低秩矩阵来表⽰权重的变化。尽管预训练模型拥有⼤量的参数，</font><font style="color:#6425d0;">但许多参数在特定任务的微   调过程中实际上是不活跃的</font><font style="color:#1f2329;">。LoRA通过低秩分解的⽅式，只更新那些对特定任务最重要的参数，这样做可以在保持模型性能的同时，显著减少微调所需的计算资源和时间。</font>

<font style="color:#1f2329;">假设某个层的权重矩阵为 W∈R</font><sup><font style="color:#1f2329;">d ×k</font></sup><font style="color:#1f2329;">  ，LoRA 不微调 W本⾝ ，⽽是通过两个低秩矩阵  A∈R</font><sup><font style="color:#1f2329;">d ×r</font></sup><font style="color:#1f2329;"> 和B∈R</font><sup><font style="color:#1f2329;">r ×k </font></sup><font style="color:#1f2329;">来近似微调权重矩阵。LoRA 的权重更新公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740368233477-55bd4c15-dce7-4997-8033-c999b7888764.png)

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">W</font><sub><font style="color:#1f2329;">new</font></sub><font style="color:#1f2329;">：微调后的权重矩阵。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">W</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">：预训练模型的原始权重矩阵</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，保持不变。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">A</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">和</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">B</font><font style="color:#1f2329;">  </font><font style="color:#1f2329;">：低秩矩阵</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">，</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">A</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">×</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">B</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">近似于权</font><font style="color:#1f2329;">重变化量 </font><font style="color:#1f2329;">Δ</font><font style="color:#1f2329;">W</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">• </font> alpha(α) <font style="color:#1f2329;"> ：⼀个缩放因⼦ ，⽤来调节低秩矩阵的影响，经验上可以按照 2*r设置。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">r  ：秩的⼤⼩，表⽰低秩矩阵A和B 的维度，通常r ≪ d, k ，从⽽⼤⼤减少需要训练的参数数量。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:#1f2329;">高效性</font>**<font style="color:#1f2329;">：通过低秩矩阵分解，⼤幅减少了需要微调的参数量。在⼤规模预训练模型中，LoRA仅引⼊⼀⼩部分新的  参数，节省了存储空  间和计算开销。</font>
+ **<font style="color:#1f2329;">冻结主⼲模型</font>**<font style="color:#1f2329;">：LoRA 保持原始模型的主⼲权重W 不变，仅调整A和B矩阵。这使得可以在多个任务  之间共享同⼀个预训  练模型，⽽不同任务只需要微调少量的低  秩矩阵。</font>
+ **<font style="color:#1f2329;">通⽤性强</font>**<font style="color:#1f2329;">：LoRA 可以应⽤在模型的多种层次结构（如   ⾃注意⼒层、前馈⽹   络层等），⼴泛适⽤   于各类Transformer模型。</font>

**缺点：**

1. **<font style="color:rgb(51, 51, 51);">性能限制</font>**<font style="color:rgb(51, 51, 51);">：由于只调整低秩矩阵，某些复杂任务可能无法达到全参数微调的性能。</font>
2. **<font style="color:rgb(51, 51, 51);">额外复杂性</font>**<font style="color:rgb(51, 51, 51);">：引入低秩矩阵可能增加模型设计和训练的复杂性，需要额外的调优来选择低秩的维度等超参数。</font>
3. **<font style="color:rgb(51, 51, 51);">适用性</font>**<font style="color:rgb(51, 51, 51);">：对于某些应用场景，LoRA的效果可能不如全模型微调，因此在选择方法时需综合考虑任务要求。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">大模型（如 Qwen、LLaMA）的轻量微调。</font>
+ <font style="color:rgb(51, 51, 51);">资源受限场景（单卡训练）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">动态调整秩（如 AdaLoRA）。</font>
+ <font style="color:rgb(51, 51, 51);">结合其他高效微调技术（如前缀微调）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn

class LoRALayer(nn.Module):
    def __init__(self, original_layer, rank=8, alpha=16):
        super().__init__()
        self.original_layer = original_layer  # Frozen original weights
        d, k = original_layer.weight.shape
        self.A = nn.Parameter(torch.randn(d, rank))  # 初始化A
        self.B = nn.Parameter(torch.zeros(rank, k))  # 初始化B
        self.alpha = alpha / rank  # 缩放因子

    def forward(self, x):
        orig_out = self.original_layer(x)
        lora_out = (x @ self.A @ self.B) * self.alpha
        return orig_out + lora_out

# 替换原模型的线性层
original_linear = nn.Linear(768, 768)
lora_linear = LoRALayer(original_linear, rank=8)

```

## lora如何初始化矩阵
:::color3
<font style="color:rgb(51, 51, 51);">简介：</font><font style="color:#1f2329;">在 LoRA 的实现中，矩阵B初始化为</font>**<font style="color:#ED740C;">零矩阵</font>**<font style="color:#1f2329;">，矩阵A使⽤</font>**<font style="color:#ED740C;">随机⾼斯分布初始化</font>**<font style="color:#1f2329;">，这样做的主要⽬的是在微调开始时确保权重调整 ΔW= 0是零矩阵，从⽽稳定训练过程并保持模型在初始阶段的表现与预训练模型⼀致。</font>

:::

:::color5
**<font style="color:#601BDE;">1.权重初始化</font>**

:::

1. **<font style="color:#1f2329;">A使⽤</font>****<font style="color:#ED740C;">随机⾼斯分布初始化</font>**

<font style="color:#1f2329;">尽管B初始化为零，但A使⽤随机⾼斯分布进⾏初始化。这是为了确保在训练过程中，当B不再为零矩阵时，A </font>**<font style="color:#74B602;">能够提供多样的参数更新⽅向</font>**<font style="color:#1f2329;">。具体原因包括：</font>

+ **<font style="color:#1f2329;">增强表示能力：</font>**<font style="color:#1f2329;">随机初始化A可以确保它具有丰富的表⽰能⼒，使得低秩矩阵</font>_<font style="color:#1f2329;">A</font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">能够探索⼴泛的权重调整空间。随机初始化提供了不同的起始点，从⽽能够在训练过程中捕捉更多的特征。</font>
+ **<font style="color:#1f2329;">避免对称性问题：</font>**<font style="color:#1f2329;">如果A初始为零或相同的值，可能会限制模型在调整过程中学习到多样化的特征。随机初始化打破了这种对称性，使得矩阵</font>_<font style="color:#1f2329;">A </font>_<font style="color:#1f2329;">能够在训练过程中学到更复杂的特征组合。</font>
+ **<font style="color:#1f2329;">提供有效的梯度信息</font>**<font style="color:#1f2329;">：随机初始化A 可以防⽌梯度更新过程中出现梯度消失的问题。初始化时提供的⾮零梯度信息可以加速收敛，帮助模型更快地找到适应任务的最优参数。</font>
2. **<font style="color:#1f2329;">矩阵B初始化为</font>****<font style="color:#ED740C;">零矩阵</font>**<font style="color:#ED740C;">  
</font><font style="color:#1f2329;">	LoRA 的⽬标是在不改变预训练模型原始权重W 的情况下，通过微调来对模型进⾏轻量级的适配。如果在微调⼀开始，矩阵A和B 的初始值导致较⼤的权重变化（即 ΔW </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740369218633-51a5a960-ff98-4ff3-875f-4116f857a361.png)<font style="color:#1f2329;">0 ），模型的表现可能会发⽣突变，偏离原本的预训练模型表现，从⽽导致不稳定的训练过程。通过将B初始化为零矩阵，ΔW = A × B  ⼀开始为零矩阵，这样确保了在微调开始时：</font>

<font style="color:#1f2329;">W</font><sub><font style="color:#1f2329;">new</font></sub><font style="color:#1f2329;">=W +ΔW = W +0 = W</font>

:::color5
**<font style="color:#601BDE;">2.权重初始化目的</font>**

:::

<font style="color:#1f2329;">通过将  </font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">初始化为零矩阵以及将  </font>_<font style="color:#1f2329;">A  </font>_<font style="color:#1f2329;">随机初始化，LoRA 保证了模型在微调开始时的稳定性，并能逐渐引⼊权重更新。</font><font style="color:#d83931;">这种初始化⽅式确保了模型在训练初期不会出现性能波动，同时提供了⾜够的参数  ⾃由度来进⾏有效的任务适配，从⽽使 LoRA 在微调过程中能够实现⾼效且稳定的性能提升。</font>

## lora需要微调哪些层(lora_target)？如何选择？
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">lora_target</font>`<font style="color:rgb(51, 51, 51);">指在预训练模型中应用LoRA适配器的具体模块（如线性层）。选择目标模块需权衡以下因素：</font>

1. **<font style="color:rgb(51, 51, 51);">任务敏感度</font>**<font style="color:rgb(51, 51, 51);">：选择对下游任务敏感的模块。</font>
2. **<font style="color:rgb(51, 51, 51);">参数效率</font>**<font style="color:rgb(51, 51, 51);">：以最少新增参数达到最优效果。</font>
3. **<font style="color:rgb(51, 51, 51);">计算资源</font>**<font style="color:rgb(51, 51, 51);">：目标模块越多，显存和计算量越大。</font>

:::

**常见配置参考**

| **模型类型** | **推荐**`**lora_target**`**模块** | **适用任务** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">LLaMA-7B/13B</font> | `<font style="color:rgb(51, 51, 51);">["q_proj", "v_proj"]</font>` | <font style="color:rgb(51, 51, 51);">通用指令微调</font> |
| <font style="color:rgb(51, 51, 51);">GPT-J</font> | `<font style="color:rgb(51, 51, 51);">["q_proj", "v_proj", "out_proj"]</font>` | <font style="color:rgb(51, 51, 51);">文本生成</font> |
| <font style="color:rgb(51, 51, 51);">BERT-base</font> | `<font style="color:rgb(51, 51, 51);">["query", "value", "intermediate.dense"]</font>` | <font style="color:rgb(51, 51, 51);">文本分类、QA</font> |
| <font style="color:rgb(51, 51, 51);">T5</font> | `<font style="color:rgb(51, 51, 51);">["q", "v", "o", "wi", "wo"]</font>`<br/><font style="color:rgb(51, 51, 51);">（对应注意力层和FFN）</font> | <font style="color:rgb(51, 51, 51);">翻译、摘要</font> |
| <font style="color:rgb(51, 51, 51);">ViT</font> | `<font style="color:rgb(51, 51, 51);">["query", "value", "mlp.fc1", "mlp.fc2"]</font>` | <font style="color:rgb(51, 51, 51);">图像分类</font> |


**选择原则**

+ **<font style="color:rgb(51, 51, 51);">通用推荐</font>**<font style="color:rgb(51, 51, 51);">：从注意力层的</font>`<font style="color:rgb(51, 51, 51);">q_proj</font>`<font style="color:rgb(51, 51, 51);">和</font>`<font style="color:rgb(51, 51, 51);">v_proj</font>`<font style="color:rgb(51, 51, 51);">开始，按需扩展至FFN。</font>
+ **<font style="color:rgb(51, 51, 51);">关键原则</font>**<font style="color:rgb(51, 51, 51);">：通过实验验证选择，平衡任务需求与资源限制。</font>
+ **<font style="color:rgb(51, 51, 51);">未来方向</font>**<font style="color:rgb(51, 51, 51);">：自动化目标模块搜索（如基于梯度重要性评估）。</font>

:::color5
**<font style="color:#601BDE;">1.基于模型架构选择</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">Transformer模型（如LLaMA、GPT）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">注意力层（Self-Attention）</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * `<font style="color:rgb(51, 51, 51);">query</font>`<font style="color:rgb(51, 51, 51);">（Q）、</font>`<font style="color:rgb(51, 51, 51);">key</font>`<font style="color:rgb(51, 51, 51);">（K）、</font>`<font style="color:rgb(51, 51, 51);">value</font>`<font style="color:rgb(51, 51, 51);">（V）投影层：捕捉输入交互（</font>**<font style="color:rgb(51, 51, 51);">必选Q、V</font>**<font style="color:rgb(51, 51, 51);">）。</font>
        * `<font style="color:rgb(51, 51, 51);">output</font>`<font style="color:rgb(51, 51, 51);">（O）投影层：影响注意力聚合结果（可选）。</font>
    - **<font style="color:rgb(51, 51, 51);">前馈网络（FFN）</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * `<font style="color:rgb(51, 51, 51);">up_proj</font>`<font style="color:rgb(51, 51, 51);">（升维层）、</font>`<font style="color:rgb(51, 51, 51);">down_proj</font>`<font style="color:rgb(51, 51, 51);">（降维层）：调整特征变换（适合知识密集型任务）。</font>
    - **<font style="color:rgb(51, 51, 51);">典型配置</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
target_modules = ["q_proj", "v_proj"]  # 通用推荐
target_modules = ["q_proj", "v_proj", "down_proj", "up_proj"]  # 包含FFN层
```

+ **<font style="color:rgb(51, 51, 51);">BERT类模型（编码器结构）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">注意力层</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">query</font>`<font style="color:rgb(51, 51, 51);">、</font>`<font style="color:rgb(51, 51, 51);">value</font>`<font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:rgb(51, 51, 51);">全连接层</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">intermediate.dense</font>`<font style="color:rgb(51, 51, 51);">（升维）、</font>`<font style="color:rgb(51, 51, 51);">output.dense</font>`<font style="color:rgb(51, 51, 51);">（降维）。</font>
    - **<font style="color:rgb(51, 51, 51);">典型配置</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
target_modules = ["query", "value", "intermediate.dense"]
```

:::color5
**<font style="color:#601BDE;">2.基于任务选择</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">自然语言理解（NLU）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">关注</font>**<font style="color:rgb(51, 51, 51);">注意力机制</font>**<font style="color:rgb(51, 51, 51);">：优先选择Q、V，调整输入交互。</font>
    - **<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：文本分类、实体识别。</font>
    - **<font style="color:rgb(51, 51, 51);">配置</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">["q_proj", "v_proj"]</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">自然语言生成（NLG）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">扩展至</font>**<font style="color:rgb(51, 51, 51);">FFN层</font>**<font style="color:rgb(51, 51, 51);">：生成需复杂特征变换。</font>
    - **<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：对话生成、文本摘要。</font>
    - **<font style="color:rgb(51, 51, 51);">配置</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">["q_proj", "v_proj", "down_proj", "up_proj"]</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">跨模态任务（如图文对齐）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">覆盖</font>**<font style="color:rgb(51, 51, 51);">所有投影层</font>**<font style="color:rgb(51, 51, 51);">：包括交叉注意力模块。</font>
    - **<font style="color:rgb(51, 51, 51);">配置</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">["q_proj", "k_proj", "v_proj", "cross_attn"]</font>`<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">3.基于资源选择</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">低资源场景</font>**<font style="color:rgb(51, 51, 51);">（单卡显存<24GB）：</font>
    - **<font style="color:rgb(51, 51, 51);">精简目标模块</font>**<font style="color:rgb(51, 51, 51);">：仅选择顶层Transformer的Q、V。</font>
    - **<font style="color:rgb(51, 51, 51);">降低秩（r）</font>**<font style="color:rgb(51, 51, 51);">：设</font>`<font style="color:rgb(51, 51, 51);">r=4</font>`<font style="color:rgb(51, 51, 51);">或</font>`<font style="color:rgb(51, 51, 51);">r=8</font>`<font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:rgb(51, 51, 51);">示例配置</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
target_modules = ["layers.30.q_proj", "layers.30.v_proj"]  # 仅顶层
```

+ **<font style="color:rgb(51, 51, 51);">高资源场景</font>**<font style="color:rgb(51, 51, 51);">（多卡训练）：</font>
    - **<font style="color:rgb(51, 51, 51);">全模块覆盖</font>**<font style="color:rgb(51, 51, 51);">：包括所有注意力层和FFN。</font>
    - **<font style="color:rgb(51, 51, 51);">示例配置</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "down_proj", "up_proj"]
```

:::color5
**<font style="color:#601BDE;">4.实验验证</font>**

:::

1. **消融实验**：
    - <font style="color:rgb(51, 51, 51);">对比不同</font>`<font style="color:rgb(51, 51, 51);">lora_target</font>`<font style="color:rgb(51, 51, 51);">组合的验证集损失。</font>
    - **<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：测试仅Q、仅V、Q+V等组合的性能差异。</font>
2. **参数效率分析**：
    - <font style="color:rgb(51, 51, 51);">记录参数量与效果的关系，选择帕累托最优（如效果提升>5%而参数量增加<10%）。</font>
3. **可视化分析**：
    - <font style="color:rgb(51, 51, 51);">使用工具（如</font>`<font style="color:rgb(51, 51, 51);">tensorboard</font>`<font style="color:rgb(51, 51, 51);">）监控不同模块的梯度幅度，选择梯度活跃的模块。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from peft import LoraConfig, get_peft_model

# 案例1：LLaMA-7B指令微调（仅Q、V）
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # 关键模块
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# 案例2：BERT文本分类（含FFN）
lora_config = LoraConfig(
    r=4,
    lora_alpha=16,
    target_modules=["query", "value", "intermediate.dense"],  # 注意力层+FFN
    modules_to_save=["classifier"],  # 分类头不冻结
    lora_dropout=0.05,
    task_type="SEQ_CLS"
)

model = get_peft_model(base_model, lora_config)

```

```python
args="--stage sft \
    --model_name_or_path=$MODEL_NAME \
    --do_train \
    --file_name=data/data.json \
    --prompt=instruction \
    --query=input \
    --response=output \
    --template=$PROMPT_TEMPLATE \
    --finetuning_type lora \
    --lora_target=c_attn,attn.c_proj,w1,w2,mlp.c_proj \
    --output_dir=local/tmp/ckpt_save_path/ \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 100 \
    --max_steps 200 \
    --learning_rate=$LR \
    --cutoff_len=1024 \
    --preprocessing_num_workers=8 \
    --dataloader_num_workers=4 \
    --plot_loss \
    --quantization_bit ${QUANTIZATION_BIT} \
    --bf16"
```

## lora的秩r/缩放因子alpha如何设置？
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">秩（r）</font>**<font style="color:rgb(51, 51, 51);">：LoRA低秩矩阵的维度，</font>**<font style="color:#ED740C;">控制参数更新矩阵的表达能力</font>**<font style="color:rgb(51, 51, 51);">。</font>

+ <font style="color:rgb(51, 51, 51);">物理意义：决定LoRA矩阵的"信息容量"，</font>**<font style="color:#ED740C;">r越大表示允许更复杂的参数更新</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ <font style="color:rgb(51, 51, 51);">计算量：新增参数量为</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">r×(d_in + d_out)</font>`<font style="color:rgb(51, 51, 51);">，其中d_in/d_out为原全连接层的输入/输出维度。</font>

**<font style="color:rgb(51, 51, 51);">缩放因子（alpha）</font>**<font style="color:rgb(51, 51, 51);">：控制LoRA权重增量ΔW的全局缩放比例。</font>

+ <font style="color:rgb(51, 51, 51);">数学形式：ΔW = alpha * (A × B)，其中A∈ℝ^{d×r}, B∈ℝ^{r×k}，原始权重为W∈ℝ^{d×k}。</font>
+ <font style="color:rgb(51, 51, 51);">作用：</font>**<font style="color:#ED740C;">调节LoRA更新量对原始权重的调整幅度</font>**<font style="color:rgb(51, 51, 51);">，影响模型收敛速度和稳定性。</font>

:::

<font style="color:rgb(51, 51, 51);">通过系统化的参数设置和实验验证，可以充分发挥LoRA在参数高效微调中的优势。建议配合wandb等可视化工具监控训练动态，及时调整参数组合。</font>

**最佳实现**

| **模型规模** | **任务类型** | **推荐r** | **推荐alpha** | **学习率** |
| :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">7B</font> | <font style="color:rgb(51, 51, 51);">对话生成</font> | <font style="color:rgb(51, 51, 51);">8</font> | <font style="color:rgb(51, 51, 51);">32</font> | <font style="color:rgb(51, 51, 51);">3e-4</font> |
| <font style="color:rgb(51, 51, 51);">13B</font> | <font style="color:rgb(51, 51, 51);">指令跟随</font> | <font style="color:rgb(51, 51, 51);">16</font> | <font style="color:rgb(51, 51, 51);">64</font> | <font style="color:rgb(51, 51, 51);">2e-4</font> |
| <font style="color:rgb(51, 51, 51);">70B</font> | <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">32</font> | <font style="color:rgb(51, 51, 51);">128</font> | <font style="color:rgb(51, 51, 51);">1e-4</font> |


:::color5
**<font style="color:#601BDE;">1.r和alpha如何设置</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">秩r的选择</font>**
+ **初始参考值**：
    - <font style="color:rgb(51, 51, 51);">论文推荐：对于7B~13B模型，常用r=8或16；175B模型可用r=64。</font>
    - <font style="color:rgb(51, 51, 51);">经验公式：</font>`<font style="color:rgb(51, 51, 51);">r ≈ log2(N/1e9)</font>`<font style="color:rgb(51, 51, 51);">，其中N为模型参数量（如13B模型：log2(13)≈3.7 → r=8）。</font>
+ **任务复杂度匹配**：
    - <font style="color:rgb(51, 51, 51);">简单任务（分类/单领域SFT）：r=4~16</font>
    - <font style="color:rgb(51, 51, 51);">复杂任务（多轮对话/代码生成）：r=16~64</font>
    - <font style="color:rgb(51, 51, 51);">极端案例：BigCode的StarCoder微调使用r=64</font>
+ **硬件限制**：
    - <font style="color:rgb(51, 51, 51);">显存不足时优先降低r而非alpha（如从r=16→8可减少50%新增参数量）</font>
2. **<font style="color:rgb(51, 51, 51);">alpha的设置</font>**
+ **黄金比例法则**：
    - <font style="color:rgb(51, 51, 51);">保持</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">alpha/r ≈ 2~8</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">的比例（例如r=8时alpha=16~64）</font>
    - <font style="color:rgb(51, 51, 51);">物理意义：通过alpha补偿低秩矩阵的降维信息损失</font>
+ **学习率联动**：
    - <font style="color:rgb(51, 51, 51);">alpha越大，等效学习率越高（ΔW=alpha*(A×B)）</font>
    - <font style="color:rgb(51, 51, 51);">典型组合：当alpha=32，r=8时，推荐学习率lr=3e-4</font>
+ **动态调整策略**：
    - <font style="color:rgb(51, 51, 51);">初始阶段：设置alpha/r=4（快速收敛）</font>
    - <font style="color:rgb(51, 51, 51);">后期微调：降低alpha比例（稳定训练）</font>

:::color5
**<font style="color:#601BDE;">2.参数见的相互作用</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">r与alpha的联合影响</font>**
+ 当r固定时：
    - <font style="color:rgb(51, 51, 51);">alpha过小 → 更新量不足 → 收敛慢</font>
    - <font style="color:rgb(51, 51, 51);">alpha过大 → 梯度震荡 → loss不稳定</font>
+ 当alpha/r比例固定时：
    - <font style="color:rgb(51, 51, 51);">r增大 → 模型容量↑，过拟合风险↑</font>
    - <font style="color:rgb(51, 51, 51);">r减小 → 模型容量↓，欠拟合风险↑</font>
2. **<font style="color:rgb(51, 51, 51);">与学习率的关系</font>**
+ <font style="color:rgb(51, 51, 51);">等效学习率公式：</font>

```plain
lr_eff ≈ lr_base * (alpha / r)
```

<font style="color:rgb(51, 51, 51);">例如：当基础学习率lr_base=1e-4，alpha=32，r=8时，等效学习率≈4e-4</font>

:::color5
**<font style="color:#601BDE;">3.典型案例</font>**

:::

**<font style="color:rgb(51, 51, 51);">案例1：对话微调（7B模型）</font>**

+ <font style="color:rgb(51, 51, 51);">初始设置：r=8, alpha=32（比例4:1）</font>
+ <font style="color:rgb(51, 51, 51);">现象：验证loss波动大</font>
+ <font style="color:rgb(51, 51, 51);">调整：降低alpha至16（比例2:1）→ 训练稳定</font>

**<font style="color:rgb(51, 51, 51);">案例2：代码生成（13B模型）</font>**

+ <font style="color:rgb(51, 51, 51);">初始设置：r=16, alpha=64（比例4:1）</font>
+ <font style="color:rgb(51, 51, 51);">现象：训练loss下降缓慢</font>
+ <font style="color:rgb(51, 51, 51);">调整：增大r到32，保持比例→ 模型容量提升，收敛加速</font>

:::color5
**<font style="color:#601BDE;">4.调优方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">始终保持alpha是r的整数倍（避免除不尽导致缩放异常）</font>
+ <font style="color:rgb(51, 51, 51);">不同层可设置不同r值（如Attention层r=16，FFN层r=8）</font>
+ <font style="color:rgb(51, 51, 51);">大模型训练后期可逐渐降低学习率并保持alpha不变</font>

## Lora训练有多少可学习参数？
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：以LLAMA-7B为例。</font><font style="color:rgb(51, 51, 51);">通过合理选择适配模块和秩 </font><font style="color:rgb(51, 51, 51);">r</font>_<font style="color:rgb(51, 51, 51);">r</font>_<font style="color:rgb(51, 51, 51);">，LoRA能在保持模型性能的同时显著降低训练成本。对于LLAMA-7B，典型配置下可学习参数约 </font>**<font style="color:rgb(51, 51, 51);">4~10M</font>**<font style="color:rgb(51, 51, 51);">，仅为原始模型的 </font>**<font style="color:rgb(51, 51, 51);">0.06%~0.15%</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

1. **lora参数**

<font style="color:rgb(51, 51, 51);">LoRA通过在预训练权重矩阵旁添加</font>**<font style="color:rgb(51, 51, 51);">低秩分解的适配器</font>**<font style="color:rgb(51, 51, 51);">，仅训练适配器参数，公式为：</font>

<font style="color:rgb(51, 51, 51);">W</font><sub><font style="color:rgb(51, 51, 51);">new</font></sub><font style="color:rgb(51, 51, 51);">=W</font><sub><font style="color:rgb(51, 51, 51);">pre-trained</font></sub><font style="color:rgb(51, 51, 51);">+B⋅A</font>

+ <font style="color:rgb(51, 51, 51);">A∈R</font><sup><font style="color:rgb(51, 51, 51);">d×r </font></sup><font style="color:rgb(51, 51, 51);">B∈R</font><sup><font style="color:rgb(51, 51, 51);">r×d</font></sup>
+ <font style="color:rgb(51, 51, 51);">r≪d（秩，通常取 8 或 16）</font>
+ <font style="color:rgb(51, 51, 51);">仅训练 A</font><font style="color:rgb(51, 51, 51);"> 和 B，冻结原权重 W</font>
2. **LLAMA参数**

| **参数** | **值** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">层数 L</font>_<font style="color:rgb(51, 51, 51);"></font>_ | <font style="color:rgb(51, 51, 51);">32</font> |
| <font style="color:rgb(51, 51, 51);">隐藏维度 d</font>_<font style="color:rgb(51, 51, 51);"></font>_ | <font style="color:rgb(51, 51, 51);">4096</font> |
| <font style="color:rgb(51, 51, 51);">注意力头数</font> | <font style="color:rgb(51, 51, 51);">32</font> |
| <font style="color:rgb(51, 51, 51);">前馈网络维度 d</font><sub><font style="color:rgb(51, 51, 51);">ff</font></sub> | <font style="color:rgb(51, 51, 51);">11008</font> |


:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 应用LoRA的模块选择</font>**

<font style="color:rgb(51, 51, 51);">通常选择以下模块应用LoRA：</font>

+ **<font style="color:rgb(51, 51, 51);">自注意力层</font>**<font style="color:rgb(51, 51, 51);">的 Q、V 矩阵（共2个/层）</font>
+ **<font style="color:rgb(51, 51, 51);">前馈网络</font>**<font style="color:rgb(51, 51, 51);">的两层（可选）</font>

**<font style="color:rgb(51, 51, 51);">2. 单层参数计算</font>**

+ **<font style="color:rgb(51, 51, 51);">单矩阵参数</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740569311660-aae699b8-b0cb-422c-acd7-9eab0845f63a.png)
+ **<font style="color:rgb(51, 51, 51);">每层参数</font>**<font style="color:rgb(51, 51, 51);">（假设仅Q、V矩阵）：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740569317927-3210e1a7-4276-499b-a69a-c46829746601.png)

**<font style="color:rgb(51, 51, 51);">3. 总参数计算</font>**

+ **<font style="color:rgb(51, 51, 51);">仅自注意力层</font>**<font style="color:rgb(51, 51, 51);">（32层）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740569328654-786560a8-e505-4336-9e03-e27cf4f4a66c.png)

+ **<font style="color:rgb(51, 51, 51);">包含前馈网络</font>**<font style="color:rgb(51, 51, 51);">（每层增加2个矩阵）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740569336143-563c3ec9-eb57-407c-915b-334769b4bcdf.png)

:::color5
**<font style="color:#601BDE;">2.参数量表</font>**

:::

| **应用范围** | **秩**** ****r**_**r**_ | **总参数** | **占比原始模型** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">自注意力Q、V</font> | <font style="color:rgb(51, 51, 51);">8</font> | <font style="color:rgb(51, 51, 51);">4.19M (0.06%)</font> | <font style="color:rgb(51, 51, 51);">7B → 7.004B</font> |
| <font style="color:rgb(51, 51, 51);">自注意力QKV</font> | <font style="color:rgb(51, 51, 51);">8</font> | <font style="color:rgb(51, 51, 51);">6.29M (0.09%)</font> | <font style="color:rgb(51, 51, 51);">7B → 7.006B</font> |
| <font style="color:rgb(51, 51, 51);">自注意力+前馈网络</font> | <font style="color:rgb(51, 51, 51);">8</font> | <font style="color:rgb(51, 51, 51);">10.49M (0.15%)</font> | <font style="color:rgb(51, 51, 51);">7B → 7.010B</font> |


:::color5
**<font style="color:#601BDE;">3.计算量分析</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">内存节省</font>**<font style="color:rgb(51, 51, 51);">：相比全参数微调（7B → 7B），LoRA仅需训练 0.06%~0.15% 参数</font>
+ **<font style="color:rgb(51, 51, 51);">计算加速</font>**<font style="color:rgb(51, 51, 51);">：反向传播仅计算低秩矩阵梯度</font>
+ **<font style="color:rgb(51, 51, 51);">多任务支持</font>**<font style="color:rgb(51, 51, 51);">：不同任务可切换适配器（通过加载不同 A/B</font>_<font style="color:rgb(51, 51, 51);">A</font>_<font style="color:rgb(51, 51, 51);">/</font>_<font style="color:rgb(51, 51, 51);">B</font>_<font style="color:rgb(51, 51, 51);">）</font>

:::color5
**<font style="color:#601BDE;">4.lora配置建议</font>**

:::

| **场景** | **推荐配置** | **参数量估算** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">单任务微调</font> | <font style="color:rgb(51, 51, 51);">QV矩阵 + r=8</font> | <font style="color:rgb(51, 51, 51);">~4.2M</font> |
| <font style="color:rgb(51, 51, 51);">多任务适配</font> | <font style="color:rgb(51, 51, 51);">QKV矩阵 + r=16</font> | <font style="color:rgb(51, 51, 51);">~18.9M</font> |
| <font style="color:rgb(51, 51, 51);">复杂任务（代码生成）</font> | <font style="color:rgb(51, 51, 51);">QKV+前馈网络 + r=32</font> | <font style="color:rgb(51, 51, 51);">~67.1M</font> |


## Lora训练如何选择精度
:::color3
+ **<font style="color:rgb(51, 51, 51);">bfloat16</font>**<font style="color:rgb(51, 51, 51);">：大模型LoRA训练的默认选择，平衡动态范围和效率。</font>
+ **<font style="color:rgb(51, 51, 51);">float16</font>**<font style="color:rgb(51, 51, 51);">：旧硬件或显存受限时的替代方案，需配合混合精度。</font>
+ **<font style="color:rgb(51, 51, 51);">float32</font>**<font style="color:rgb(51, 51, 51);">：仅用于敏感任务或极小模型。</font>

:::

<font style="color:rgb(51, 51, 51);">LoRA（Low-Rank Adaptation）通过冻结原模型参数并训练低秩矩阵实现高效微调。精度选择需权衡以下因素：</font>

1. **<font style="color:rgb(51, 51, 51);">优先选择bfloat16的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">大模型场景</font>**<font style="color:rgb(51, 51, 51);">（如百亿参数以上）：bfloat16的动态范围与float32一致，避免梯度溢出问题。</font>
    - **<font style="color:rgb(51, 51, 51);">新一代硬件支持</font>**<font style="color:rgb(51, 51, 51);">（如NVIDIA A100/H100）：原生支持bfloat16加速，计算效率高。</font>
    - **<font style="color:rgb(51, 51, 51);">注重稳定性与速度平衡</font>**<font style="color:rgb(51, 51, 51);">：无需频繁调整损失缩放，适合大规模分布式训练。</font>
2. **<font style="color:rgb(51, 51, 51);">选择float16的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">硬件不支持bfloat16</font>**<font style="color:rgb(51, 51, 51);">（如V100或更早GPU）：需启用混合精度训练（AMP），结合float32主权重和损失缩放。</font>
    - **<font style="color:rgb(51, 51, 51);">显存受限</font>**<font style="color:rgb(51, 51, 51);">：float16比bfloat16在部分框架中优化更成熟，显存占用略低。</font>
    - **<font style="color:rgb(51, 51, 51);">小规模微调任务</font>**<font style="color:rgb(51, 51, 51);">：数据量小、任务简单时，数值不稳定风险较低。</font>
3. **<font style="color:rgb(51, 51, 51);">选择float32的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">极度敏感的微调任务</font>**<font style="color:rgb(51, 51, 51);">：如医学图像、科学计算等需要高精度梯度的场景。</font>
    - **<font style="color:rgb(51, 51, 51);">模型规模极小</font>**<font style="color:rgb(51, 51, 51);">：显存和计算开销可接受时，直接使用float32简化流程。</font>

# AdaLoRA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">AdaLoRA（AdaptiveLow-RankAdaptation）通过在微调模型时将权重矩阵分解为低秩</font>

<font style="color:#1f2329;">矩阵，并且引⼊了</font>**<font style="color:#ED740C;">⾃适应调整低秩（rank）的机制</font>**<font style="color:#1f2329;">。在此过程中，模型在不同层可以根据梯度信息⾃适应地调整分配给每层的秩值。这个机制通过动态调整秩值，在保持模型性能的同时有效减少了计算和内存需求。</font>

:::

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

<font style="color:rgb(51, 51, 51);">AdaLoRA 动态调整各层的秩 r</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">参数重要性评估</font>**<font style="color:rgb(51, 51, 51);">：通过梯度、敏感度分析或奇异值分解（SVD）确定各层的重要性。</font>
2. **<font style="color:rgb(51, 51, 51);">预算分配</font>**<font style="color:rgb(51, 51, 51);">：总参数预算下，重要性高的层分配更高秩。</font>
3. **<font style="color:rgb(51, 51, 51);">动态调整</font>**<font style="color:rgb(51, 51, 51);">：在训练中迭代调整秩，优化参数分配。</font>

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

1. <font style="color:#1f2329;">给定原始模型权重矩阵W ，通过 LoRA，我们将其分解为两个低秩矩阵：</font>

<font style="color:#1f2329;">W ≈W0 +△W=W0 +ABT</font>

<font style="color:#1f2329;">其中 ， W</font><font style="color:#1f2329;">0</font><font style="color:#1f2329;"> 是预训练模型的固定权重 ， A∈R</font><font style="color:#1f2329;">m ×r</font><font style="color:#1f2329;"> 和 B∈R</font><font style="color:#1f2329;">n ×r</font><font style="color:#1f2329;">   分别是低秩矩阵 ， r是低秩值。</font>

2. 通过⾃适应调整r，来使得不同层的权重矩阵分解具有不同的秩值。<font style="color:#1f2329;">使⽤Frobenius 范数等指标来动态调整：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740378226871-4f90811b-6a86-4446-aaab-95e50d2f7c44.png)

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ <font style="color:#1f2329;">AdaLoRA 主要⽤于模型微调。它可以在预训练模型的基础上，通过⾼效的低秩适应⽅法，针对特定任务进⾏细化微调。</font>
+ <font style="color:#1f2329;"> 动态调整秩值减少了资源浪费，同时保留了模型的强⼤性能，适合⽤于⼤模型的微调过程。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ <font style="color:rgb(51, 51, 51);">实现复杂，需维护动态结构。</font>
+ <font style="color:rgb(51, 51, 51);">重要性评估增加计算开销。</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">对微调效果要求高的场景。</font>
+ <font style="color:rgb(51, 51, 51);">异构模型层（不同层重要性差异大）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">更高效的重要性评估算法。</font>
+ <font style="color:rgb(51, 51, 51);">基于强化学习的自动秩分配。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
class AdaLoRALayer(LoRALayer):
    def __init__(self, original_layer, max_rank=16):
        super().__init__(original_layer, rank=max_rank)
        self.importance_scores = nn.Parameter(torch.ones(max_rank))  # 奇异值重要性
        
    def update_rank(self, target_rank):
        # 根据重要性保留前target_rank个分量
        idx = torch.argsort(self.importance_scores, descending=True)[:target_rank]
        self.A.data = self.A.data[:, idx]
        self.B.data = self.B.data[idx, :]
        self.importance_scores = nn.Parameter(self.importance_scores[idx])

# 在训练循环中定期调用update_rank()

```





# <font style="color:rgb(53, 53, 53);">qLoRA</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">QLoRA（Quantized Low-Rank Adaptation）是近年来在大规模语言模型训练中出现的一种技术。它是在LoRA（Low-Rank Adaptation）的方法基础上，引入了量化技术，以减少模型微调时所需的计算资源和内存占用。</font>

:::

:::color5
**<font style="color:#601BDE;">1.qLoRA原理</font>**

:::

1. **低秩分解**：与LoRA相似，QLoRA通过低秩分解来近似更新模型的权重，仅保留关键的潜在信息，从而降低更新所需的参数数量。
2. **权重量化**：在QLoRA中，模型权重被量化到较低的位宽（如8位或更低），这显著减少了内存占用。此外，量化后的模型在推理时也可以用更低的计算精度运行，进一步加快推理速度。
3. **组合效果**：通过结合低秩适应和量化，QLoRA能够在尽量不损失模型性能的前提下，实现在资源有限的环境中有效进行微调。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733992400531-5a8b04b0-f4ba-4756-b078-f8c224c9d364.png)

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">量化</font>**<font style="color:rgb(51, 51, 51);">：使用 NF4 对 W</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 量化，存储缩放因子（scale）和零点（zero point）。</font>
2. **<font style="color:rgb(51, 51, 51);">反量化</font>**<font style="color:rgb(51, 51, 51);">：计算时恢复为 16-bit 精度：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740377819974-2f213e77-dae4-412e-a04f-07fb8b0b25a2.png)
3. **<font style="color:rgb(51, 51, 51);">适配器计算</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740377827025-62ac6a84-88ec-4f88-bec6-0ebbf4ca81b8.png)

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点（QLoRA相较于LoRA）</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **内存效率**：QLoRA通过量化技术显著降低了内存占用，使得在更小的硬件上运行大模型微调成为可能。
2. **训练速度**：量化后的模型在推理和训练时通常可以加速，尤其是在使用现代硬件时，例如支持量化运算的GPU。
3. **适用性广**：QLoRA可以在各种场景下广泛应用，特别是资源有限的设备（如边缘设备）。

**<font style="color:rgb(51, 51, 51);">缺点（QLoRA相较于LoRA）</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **可能的精度损失**：量化过程中，若不合理，可能导致信息损失，从而影响模型最终的性能，尤其是在处理复杂任务时。
2. **实现复杂性**：与简单的LoRA相比，QLoRA可能需要更复杂的实现和调试，以确保量化不会影响性能。
3. **不适合所有场景**：若模型较小或资源较为充裕，使用QLoRA的优势可能不如预期，反而可能增加不必要的复杂性。

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">显存严重受限场景（如消费级 GPU）。</font>
+ <font style="color:rgb(51, 51, 51);">超大规模模型微调（如 LLaMA-65B）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优化量化策略（如双量化）。</font>
+ <font style="color:rgb(51, 51, 51);">混合精度训练（关键部分保留高精度）。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
from transformers import AutoModelForCausalLM
from bitsandbytes.nn import Linear4bit

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    load_in_4bit=True,  # 4-bit量化
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# 添加QLoRA适配器（需自定义适配器逻辑）

```





# DoRA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：DoRA: Weight-Decomposed Low-Rank Adaptation （</font><font style="color:rgb(25, 27, 31);">权重分解低阶适应</font><font style="color:rgb(51, 51, 51);">）。</font><font style="color:rgb(25, 27, 31);">DoRA首先</font>**<font style="color:#ED740C;">将预训练的权重分解为其幅度和方向分量，然后对两者进行微调</font>**<font style="color:rgb(25, 27, 31);">。 考虑到方向分量在参数方面的巨大规模，利用 LoRA 进行方向自适应，以实现高效的微调。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741245557544-35d29b84-5ab2-4651-8206-6f4200806a8e.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">权重分解</font>**<font style="color:rgb(25, 27, 31);">：DoRA首先对预训练模型的权重进行分解，</font>**<font style="color:#74B602;">将每个权重矩阵分解为幅度（magnitude）向量和方向（direction）矩阵。这种分解使得模型可以更好地控制权重的学习过程。</font>**
    1. 如上图所示，原来参数矩阵W的维度依旧是d*k，**<font style="color:#74B602;">新增了一个幅度向量m(1*k)</font>**。
    2. 绿色部分为需要被训练，而蓝色部分的参数表示在微调训练中是被冻结的。DoRA在训练A和B矩阵的时候，还是利用了LoRA的办法。然而新增了幅度M向量。
2. **<font style="color:rgb(25, 27, 31);">高效微调</font>**<font style="color:rgb(25, 27, 31);">：在微调过程中，DoRA使用LoRA进行方向性更新，只调整方向部分的参数，而保持幅度部分不变。这种方式可以减少需要调整的参数数量，提高微调的效率。这种方法相对于传统微调方法简化了任务，传统方法需要调整幅度和方向。</font>
3. **<font style="color:rgb(25, 27, 31);">学习能力和训练稳定性</font>**<font style="color:rgb(25, 27, 31);">：权重分解分析有助于DoRA增强模型的学习能力和训练稳定性。该方法旨在模拟全面微调的学习能力，同时避免任何额外的推理开销。</font>

```python
可以将矩阵的每列都看成向量，每列的权重矩阵都可以用大小和方向表示。例如可以将[2.0, 3.0]分解为0.5*[4, 6]。在进行完全微调时，梯度更新只是改变了列向量的方向，而幅度却保持几乎恒定。
```

:::color5
**<font style="color:#601BDE;">2.评估</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">常识推理</font>**<font style="color:rgb(25, 27, 31);">：在对</font>[<font style="color:rgb(9, 64, 142);">LLaMA-7B</font>](https://zhida.zhihu.com/search?content_id=239994801&content_type=Article&match_order=1&q=LLaMA-7B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">/13B进行常识推理任务评估时，DoRA优于LoRA和几种基准方法，实现了更高的准确性16，如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741245707779-251cea12-e83c-4651-977c-a181b131401b.png)

2. **<font style="color:rgb(25, 27, 31);">图像/视频-文本理解</font>**<font style="color:rgb(25, 27, 31);">：在使用VL-BART进行多任务评估中，涉及VQA、GQA、NVLR2、COCO Caption、TVQA、How2QA、TVC和YC2C等任务，DoRA在准确性方面始终优于LoRA。</font>



# DyLoRA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(77, 77, 77);">DyLoRA（Dynamic Low-Rank Adaptation）</font>**<font style="color:rgb(77, 77, 77);"> ，</font>**<font style="color:#ED740C;">DyLoRA通过动态调整低秩适配器的秩</font>**<font style="color:rgb(77, 77, 77);">，解决了传统LoRA在秩选择和动态调整方面的局限性，显著提高了预训练模型微调的效率和灵活性。</font>

**<font style="color:rgb(77, 77, 77);">paper</font>**<font style="color:rgb(77, 77, 77);">:</font>[https://arxiv.org/pdf/2210.07558](https://arxiv.org/pdf/2210.07558)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741244997243-2048a855-4634-42d8-b79b-dee25d9ac657.png)

:::color5
**<font style="color:#601BDE;">1.研究背景</font>**

:::

1. 预训练模型的微调成本：随着预训练模型（PMs）规模的不断增长，对它们进行微调变得越来越昂贵且资源密集。
2. 低秩适配器（LoRA）：通过引入可学习的低秩模块（LoRA块）来微调预训练模型，保持主要权重不变，从而提高参数效率。然而，LoRA存在两个主要问题：
    - **<font style="color:#74B602;">固定的秩大小</font>**：训练后无法修改，需要重新训练。
    - **<font style="color:#74B602;">秩的优化需要穷举搜索</font>**：耗时且计算成本高。

:::color5
**<font style="color:#601BDE;">2.原理</font>**

:::

<font style="color:rgb(77, 77, 77);">DyLoRA技术：提出了一种动态低秩适应技术，通过在训练过程中对不同秩的学习表示进行排序，为一系列秩而非单一秩训练LoRA块。</font>

+ **<font style="color:#74B602;">动态性</font>**<font style="color:rgb(77, 77, 77);">：DyLoRA在推理时可以动态调整秩，无需重新训练。</font>
+ **<font style="color:#74B602;">无搜索</font>**<font style="color:rgb(77, 77, 77);">：避免了为LoRA选择最佳秩的昂贵搜索过程。</font>

**关键结论：**

+ **<font style="color:#117CEE;">动态性和效率</font>**<font style="color:rgb(77, 77, 77);">：DyLoRA通过动态调整秩，显著提高了训练效率，同时保持了与LoRA相当的性能。</font>
+ **<font style="color:#117CEE;">无搜索优势</font>**<font style="color:rgb(77, 77, 77);">：DyLoRA避免了为LoRA选择最佳秩的搜索过程，降低了计算成本。</font>
+ **<font style="color:#117CEE;">广泛的适用性</font>**<font style="color:rgb(77, 77, 77);">：DyLoRA在多种自然语言处理任务上表现出色，适用于不同的预训练模型和任务类型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741245227866-3b02fc1d-5212-4898-8e48-208c109fdacb.png)

:::color5
**<font style="color:#601BDE;">3.缺点</font>**

:::

+ **<font style="color:rgb(77, 77, 77);">超参数选择</font>**<font style="color:rgb(77, 77, 77);">：尽管DyLoRA在秩选择上具有优势，但选择最佳的标量参数仍需进一步研究。</font>
+ **<font style="color:rgb(77, 77, 77);">分布影响</font>**<font style="color:rgb(77, 77, 77);">：需要进一步研究不同分布对不同下游任务的影响。</font>
+ **<font style="color:rgb(77, 77, 77);">秩范围选择</font>**<font style="color:rgb(77, 77, 77);">：需要进一步研究选择特定秩范围的影响。</font>



# MoRA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(0, 0, 0);">MoRA的核心创新在于采用</font>**<font style="color:#ED740C;">高阶方阵替代LoRA的低秩矩阵</font>**<font style="color:rgb(0, 0, 0);">，并引入巧妙的</font>**<font style="color:#ED740C;">压缩解压算子</font>**<font style="color:rgb(0, 0, 0);">，实现参数更新的高效和灵活。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741245975828-12af4d91-08cb-4252-b9ce-2dfc999fc01f.png)

:::color5
**<font style="color:#601BDE;">1.背景</font>**

:::

<font style="color:rgb(25, 27, 31);">本文在相同设置下对LoRA的各种任务进行了全面的评估，其中包括指令调优、数学推理和持续训练。作者发现类LoRA 的方法在这些任务中表现了相当的性能，</font>**<font style="color:#74B602;">并且它们在指令调优方面的性能与 FFT 相当，但在数学推理和</font>**[**<font style="color:#74B602;">持续预训练</font>**](https://zhida.zhihu.com/search?content_id=243511587&content_type=Article&match_order=1&q=%E6%8C%81%E7%BB%AD%E9%A2%84%E8%AE%AD%E7%BB%83&zhida_source=entity)**<font style="color:#74B602;">方面存在不足</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">2.为什么类LoRA的方法在指令调优效果好，在知识获取效果差？</font>**

:::

<font style="color:rgb(25, 27, 31);">本文作者认为</font>**<font style="color:#74B602;">指令调优(instruct tuning)主要侧重于与格式的交互，而不是获取知识和能力</font>**<font style="color:rgb(25, 27, 31);">，而这些知识和能力几乎完全是在预训练期间学习的。</font>

<font style="color:rgb(25, 27, 31);">除此之外，作者还观察到LoRA 在处理其他需要通过微调来</font>**<font style="color:#74B602;">增强知识和能力</font>**<font style="color:rgb(25, 27, 31);">的任务时却遇到了困难，为此，本文作者认为低秩更新矩阵 很难估计 FFT 中的满秩更新，特别是在</font>**<font style="color:#74B602;">需要记忆特定领域知识的持续预训练</font>**<font style="color:rgb(25, 27, 31);">等内存密集型任务中。</font>

:::color5
**<font style="color:#601BDE;">3.MoRA原理</font>**

:::

1. **方阵替代低秩矩阵**

<font style="color:rgb(0, 0, 0);">MoRA的关键在于使用</font>**<font style="color:#74B602;">方阵M取代LoRA的低秩矩阵A和B</font>**<font style="color:rgb(0, 0, 0);">，从而将参数更新的</font>**<font style="color:#74B602;">秩提升</font>**<font style="color:rgb(0, 0, 0);">。如上图所示，假设原权重矩阵W的维度为d×k，LoRA的参数量为(d+k)r，则MoRA的方阵M维度为</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741246287919-79e7a7af-7d2c-4216-a83e-48674ce34d11.png)<font style="color:rgb(0, 0, 0);">,其中</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741246293436-60602497-270c-4195-b3e5-30aea40fe8fe.png)<font style="color:rgb(0, 0, 0);">。</font>

<font style="color:rgb(0, 0, 0);">这一设计使得MoRA的</font>**<font style="color:#74B602;">更新自由度较LoRA实现了质的飞跃</font>**<font style="color:rgb(0, 0, 0);">。以d=4096， k=4096为例，当r=8时，LoRA的秩至多为8，而MoRA的秩可达256。高阶方阵赋予了MoRA更强大的表达能力和更新灵活性。</font>

2. **<font style="color:rgb(0, 0, 0);">压缩算子f_comp和解压缩算子f_decomp</font>**

<font style="color:rgb(0, 0, 0);">为了适应方阵运算，MoRA引入了压缩算子f_comp和解压缩算子f_decomp。它们的作用是调整输入输出的维度，使之与方阵M匹配。具体而言：</font>

1. <font style="color:rgb(0, 0, 0);">f_comp：将输入的维度从k压缩至r</font><sup><font style="color:rgb(0, 0, 0);">hat</font></sup>
2. <font style="color:rgb(0, 0, 0);">f_decomp：将中间结果的维度从提升至d。在文章中，MoRA设计了多种压缩解压方案，包括：</font>
    1. <font style="color:rgb(0, 0, 0);">截断：直接截取部分维度</font>
    2. <font style="color:rgb(0, 0, 0);">共享：将多个维度合并，共享同一个值</font>
    3. <font style="color:rgb(0, 0, 0);">解耦：将输入</font>reshape<font style="color:rgb(0, 0, 0);">为矩阵，然后与M做矩阵乘法</font>
    4. <font style="color:rgb(0, 0, 0);">旋转：在解耦的基础上引入</font>旋转矩阵<font style="color:rgb(0, 0, 0);">，增强表达能力</font>

:::color5
**<font style="color:#601BDE;">4.效果评估</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">为进一步检验MoRA的全面性，研究者选取了指令微调、数学推理和持续预训练三大典型场景，让MoRA与LoRA和FFT同台竞技。结果下表所示，MoRA的表现令人印象深刻：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741245961714-3db554b5-e29d-47e2-ab11-4c482d6a76cb.png)

+ <font style="color:rgba(0, 0, 0, 0.9);">在指令微调上，MoRA与LoRA表现相当，且在秩较小如r=8时更胜一筹。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">在数学推理上，MoRA在GSM8K数据集上再次力压群雄。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">最引人瞩目的是持续预训练，MoRA在生物医学和金融领域远超LoRA。</font>

<font style="color:rgba(0, 0, 0, 0.9);">而当秩提升到256时，MoRA在数学推理上更是逼近了FFT的性能。这些优异的成绩，无不得益于MoRA强大的知识获取和记忆能力。在三大场景的激烈角逐中，MoRA交出了一份闪亮的"成绩单"，展现了高阶更新范式的巨大潜力。</font>





