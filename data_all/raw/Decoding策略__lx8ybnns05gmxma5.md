# Decoding策略

<!-- source: yuque://zhongxian-iiot9/hlyypb/lx8ybnns05gmxma5 -->

# 基础
## 选择decoding策略的依据
+ **任务需求**
    - <font style="color:rgb(51, 51, 51);">如果任务对生成速度要求高，且内容连贯性更重要，可以选择贪心解码。</font>
    - <font style="color:rgb(51, 51, 51);">如果需要生成高质量、多样化的内容，可以结合束搜索和温式重组，寻找生成质量和多样性的平衡。</font>
    - <font style="color:rgb(51, 51, 51);">对于需要强制多样化输出的任务，如多回答生成，可以选择多样性解码或覆盖机制。</font>
+ **模型与数据**
    - <font style="color:rgb(51, 51, 51);">大模型通常具有较高的计算能力，可以支持更为复杂的解码策略，如束搜索和多样性解码。</font>
    - <font style="color:rgb(51, 51, 51);">对于较小的模型或资源受限的场景，贪心解码是更合适的选择。</font>
+ **生成场景**
    - <font style="color:rgb(51, 51, 51);">在实时应用中，贪心解码因其高效性而被广泛采用。</font>
    - <font style="color:rgb(51, 51, 51);">对于离线处理的任务，可以采用更为复杂和耗时的解码策略，如多样性解码和覆盖机制。</font>

## <font style="color:rgb(51, 51, 51);">各解码策略的对比</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739867226054-e3490263-24b0-4f20-b6e4-05068f1821bd.png)

# <font style="color:rgb(51, 51, 51);">贪心解码（Greedy Decoding）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：贪心解码是一种简单直接的解码方法。它在每一步生成中，选择当前概率最高的下一个词，直到生成完整的序列。这种方法基于“局部最优”的原则，逐个字符地构建输出。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">简单高效</font>**<font style="color:rgb(51, 51, 51);">：实现简单，计算速度快。</font>
+ **<font style="color:rgb(51, 51, 51);">生成流畅</font>**<font style="color:rgb(51, 51, 51);">：通常生成的文本较为连贯和有意义。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">缺乏多样性</font>**<font style="color:rgb(51, 51, 51);">：总是选择概率最高的词，可能导致生成内容缺乏多样性和创新性。</font>
+ **<font style="color:rgb(51, 51, 51);">忽略全局最优</font>**<font style="color:rgb(51, 51, 51);">：可能因为局部最优而导致全局生成效果不理想。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于对生成速度要求较高，且内容连贯性优先于多样性的场景，如实时聊天机器人。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
import torch
import torch.nn.functional as F

def greedy_decode(model, input_ids, max_length, device='cuda'):
    # 初始化输出
    outputs = input_ids
    for i in range(max_length):
        # 前向传播
        outputs = model(outputs, attention_mask=torch.ones(outputs.size(), device=device))
        # 获取预测概率
        logits = outputs.logits[:, -1, :]
        # 选择概率最高的词
        next_token = torch.argmax(logits, dim=-1).unsqueeze(-1)
        # 将下一个词附加到输出序列中
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```



# <font style="color:rgb(51, 51, 51);">束搜索（Beam Search）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">束搜索是一种贪心策略的扩展，通过保留多个候选序列来生成最终的输出。在每一步生成中，系统会保存若干个可能性较高的序列（束），并根据一定的分数筛选和扩展这些候选序列，最终选择得分最高的序列作为输出。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">多样性增强</font>**<font style="color:rgb(51, 51, 51);">：通过保留多个候选序列，束搜索能够生成更多样化的输出。</font>
+ **<font style="color:rgb(51, 51, 51);">提升生成质量</font>**<font style="color:rgb(51, 51, 51);">：在保持一定多样性的同时，生成质量通常优于单纯的贪心解码。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">计算开销高</font>**<font style="color:rgb(51, 51, 51);">：保留多个候选序列增加了计算量，尤其是当束宽较大时，计算时间显著增加。</font>
+ **<font style="color:rgb(51, 51, 51);">内存需求大</font>**<font style="color:rgb(51, 51, 51);">：在处理大规模序列时，存储和处理多个候选序列需要更多的内存资源。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于对生成质量有一定要求，且可以接受一定计算开销的场景，如机器翻译、文本摘要。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def beam_search_decode(model, input_ids, max_length, beam_width=3, device='cuda'):
    # 初始化输出
    current_sequences = [input_ids]
    scores = [0.0]
    
    for i in range(max_length):
        new_sequences = []
        new_scores = []
        for seq in current_sequences:
            outputs = model(seq, attention_mask=torch.ones(seq.size(), device=device))
            logits = outputs.logits[:, -1, :]
            topk_indices = torch.topk(logits, beam_width).indices
            for idx in topk_indices:
                new_seq = torch.cat([seq, idx.unsqueeze(-1)], dim=-1)
                new_seq_score = scores[current_sequences.index(seq)] + F.log_softmax(logits[idx], dim=-1).item()
                new_sequences.append(new_seq)
                new_scores.append(new_seq_score)
        
        # 根据得分排序并保留前beam_width个
        combined = list(zip(new_sequences, new_scores))
        combined.sort(key=lambda x: -x[1])
        current_sequences = [cs[0] for cs in combined[:beam_width]]
        scores = [cs[1] for cs in combined[:beam_width]]
    
    # 返回得分最高的序列
    best_seq = current_sequences[0]
    return best_seq
```





# <font style="color:rgb(51, 51, 51);">温式重组（Temperature Sampling）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">温式重组通过调整生成过程中的温度参数来平衡探索与确定性。较大的温度值会增加多样性，但可能导致生成内容不连贯；较小的温度值则更倾向于选择概率高的词，生成内容更为保守和流畅。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">增加多样性</font>**<font style="color:rgb(51, 51, 51);">：通过调节温度，可以在生成过程中引入更多变异性，提升创意生成任务的效果。</font>
+ **<font style="color:rgb(51, 51, 51);">灵活性高</font>**<font style="color:rgb(51, 51, 51);">：可以根据具体需求动态调整温度参数，实现生成策略的灵活控制。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">不稳定性</font>**<font style="color:rgb(51, 51, 51);">：高温可能导致生成内容的不连贯性和不可预测性，影响生成质量。</font>
+ **<font style="color:rgb(51, 51, 51);">计算复杂度</font>**<font style="color:rgb(51, 51, 51);">：概率计算和采样的引入增加了生成过程的计算复杂度。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于需要多样化输出的任务，如创意写作、诗歌生成等。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def temperature_sampling_decode(model, input_ids, max_length, temperature=1.0, device='cuda'):
    outputs = input_ids
    for i in range(max_length):
        outputs = model(outputs, attention_mask=torch.ones(outputs.size(), device=device))
        logits = outputs.logits[:, -1, :] / temperature
        # 采样下一个词
        next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
        next_token = next_token.squeeze(-1).unsqueeze(-1)
        # 更新输出
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```

<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">多样性解码（Diverse Decoding）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">多样性解码是一种通过引入额外的约束或机制，强制生成更多样化输出的策略。常见的实现方法包括使用遮蔽机制（如随机屏蔽部分已生成的内容，强制模型探索不同的生成路径）、或者在生成过程中引入排序损失。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">显著提升多样性</font>**<font style="color:rgb(51, 51, 51);">：通过引入遮蔽机制或多样性损失，能够有效生成更多样化的输出。</font>
+ **<font style="color:rgb(51, 51, 51);">适应复杂任务</font>**<font style="color:rgb(51, 51, 51);">：特别适用于需要多个正确答案的情况，如多语种生成、多义词处理。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">复杂性增加</font>**<font style="color:rgb(51, 51, 51);">：引入额外机制增加了实现和计算的复杂性。</font>
+ **<font style="color:rgb(51, 51, 51);">生成质量不稳定</font>**<font style="color:rgb(51, 51, 51);">：过多地追求多样性可能导致生成内容的质量下降。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于需要生成多样化输出的任务，如多回答生成、多语言翻译等。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def diverse_decoding(model, input_ids, max_length, diversity_weight=0.1):
    outputs = input_ids
    for i in range(max_length):
        outputs = model(outputs, attention_mask=torch.ones(outputs.size()))
        # 获取预测概率
        logits = outputs.logits[:, -1, :]
        # 引入多样性惩罚
        log_prob = F.log_softmax(logits, dim=-1)
        # 随机屏蔽部分词，增加多样性
        masked_logits = (log_prob + torch.randn_like(log_prob) * diversity_weight).log_softmax(dim=-1)
        # 采样下一个词
        next_token = torch.multinomial(masked_logits.exp(), num_samples=1)
        next_token = next_token.squeeze(-1).unsqueeze(-1)
        # 更新输出
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```

# <font style="color:rgb(51, 51, 51);">长度惩罚（Length Penalty）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">长度惩罚是一种用于平衡生成序列长度和质量的策略。在评估生成序列时，对长度进行适当的惩罚或奖励，以鼓励生成更合适的长度。常用在束搜索中，避免模型为了获得高分而不断生成冗长的序列。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">平衡生成长度</font>**<font style="color:rgb(51, 51, 51);">：有效抑制过长或过短的生成序列，提高生成结果的合理性。</font>
+ **<font style="color:rgb(51, 51, 51);">增强评估准确性</font>**<font style="color:rgb(51, 51, 51);">：在模型评估中，长度惩罚可以提供更准确的分数，反映生成序列的实际质量。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">需要调整参数</font>**<font style="color:rgb(51, 51, 51);">：长度惩罚参数的选择需要根据具体任务进行调整，找到合适的平衡点。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于生成序列的长度控制，如机器翻译、文本摘要等任务。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def length_penalty(beam_sequences, sequence_lengths, alpha=0.7):
    # 计算长度惩罚
    penalized_scores = []
    for seq, length in zip(beam_sequences, sequence_lengths):
        penalty = (length ** alpha) / (1 + length)
        penalized_scores.append(seq.score * penalty)
    # 返回 penalized scores
    return penalized_scores
```

# 
# <font style="color:rgb(51, 51, 51);">覆盖机制（Coverage Mechanism）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">覆盖机制是一种用于生成过程中关注多样性的策略，在生成长序列时，确保模型在各时间段都能覆盖足够多的可能词项，避免生成重复或过于单一的内容。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">避免重复内容</font>**<font style="color:rgb(51, 51, 51);">：通过覆盖机制强制模型生成多样化的内容，减少重复。</font>
+ **<font style="color:rgb(51, 51, 51);">提升生成内容的信息量</font>**<font style="color:rgb(51, 51, 51);">：能够更好地捕捉和表达复杂的信息。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">实现复杂性</font>**
    - <font style="color:rgb(51, 51, 51);">引入覆盖机制增加了生成过程的复杂性，需要额外维护和更新覆盖向量。</font>
+ **<font style="color:rgb(51, 51, 51);">需要调整参数</font>**
    - <font style="color:rgb(51, 51, 51);">覆盖机制的参数设置需要经过调试，以达到最佳效果。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于生成较长序列的任务，如文本摘要、对话生成，特别是在需要避免重复内容的情况下。</font>

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
def coverage_mechanism(model, input_ids, max_length):
    # 初始化覆盖向量
    coverage = torch.zeros(max_length)
    outputs = input_ids
    for i in range(max_length):
        # 前向传播
        outputs = model(outputs, attention_mask=torch.ones(outputs.size()))
        # 获取预测概率
        logits = outputs.logits[:, -1, :]
        # 计算覆盖评分
        coverage_logits = logits + coverage
        next_token = torch.argmax(coverage_logits, dim=-1).unsqueeze(-1)
        # 更新覆盖向量
        coverage[i:] = coverage[i:] * 0.9  # 示例覆盖衰减
        coverage[i] += 1.0
        # 更新输出
        outputs = torch.cat([outputs, next_token], dim=-1)
    return outputs
```

# 
