# ⓹ 多轮对话

<!-- source: yuque://zhongxian-iiot9/hlyypb/um5n84kbgctl6gfv -->

# SFT Packing<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**SFT** **Packing是将不同的文本序列数据，打包到同一个样本序列中。

+ <font style="color:rgb(25, 27, 31);">通常在训练中，我们对于一条文本数据，</font>**<font style="color:#117CEE;">需要将其padding到batch中最大长度（或者是padding到模型截断长度），然后进行计算。这样我们就会浪费一部分算力在padding的token上</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ <font style="color:rgb(25, 27, 31);">通过Packing的方法，</font>**<font style="color:#ED740C;">我们将多条数据packing到一起，有效的减少了padding的token数量，可以帮助我们加速训练。</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**SFT Packing详解**](https://zhuanlan.zhihu.com/p/707329908)** **[**任务型多轮对话（一）**](https://zhuanlan.zhihu.com/p/679487747)

:::

SFT packing：将短句拼接为长句，加速训练， 适用于样本量几十万以上量级，样本长短不一；少量样本场景下，可以不开启。

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">通常，我们把经过预训练（pretrain）阶段得到的模型称为base模型。这个阶段主流的数据组织方式叫packing。在不采用packing的时候，为了将不同长度的句子组成一个batch tensor，我们需要进行填充（pad），这个填充过程既可以按照batch内最长句子填充，也可以按照模型最长输入长度填充。</font>

<font style="color:rgb(25, 27, 31);">为了防止一个batch内存在许多的<pad>token，浪费计算资源，packing直接采取多条示例的拼接方法。下图是传统方法和packing的对比：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744116008445-a20f3b99-5da9-45d8-b023-00d753202867.png)

<font style="color:rgb(25, 27, 31);">为了区分不同的训练示例，我们在不同示例之间加上一个分割标记sep token，注意力窗口不会跨示例。这个注意力模式叫块对角矩阵（BlockDiagonalMask）【本质上是在示例内的下三角矩阵】，而不是传统的全局下三角矩阵。由此，就消除了对pad token的需要</font>

:::color5
**<font style="color:#601BDE;">2.Non-Packing SFT</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">首先看一下没有使用Packing的SFT训练方式，这里数据分为单轮数据和多轮数据。</font>

1. **单轮数据**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744082983209-d373ab71-3805-45b1-8ca0-5eb1f980e7f0.png)

<font style="color:rgb(25, 27, 31);">这里我们模型接受的输入是prompt，需要预测的结果是response，最后计算response上token的loss。</font>

2. **<font style="color:rgb(25, 27, 31);">多轮数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">多轮数据的构建这里就有一些不同，最开始使用DeepSpeed-Chat的时候，这里的方式就是把多轮数据拆分为多个单轮数据进行训练。考虑一个多轮数据为 </font><font style="color:rgb(25, 27, 31);">[p1,r1,p2,r2,p3,r3]</font><font style="color:rgb(25, 27, 31);"> ，则进行如下构建方式：</font>

  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744083083690-408bcc34-db96-4738-a3b4-bbdad5fac78a.png)

<font style="color:rgb(25, 27, 31);">基于上面的方式，我们训练的时候就将</font>**<font style="color:#74B602;">一个三轮对话数据拆分为了三条数据，这样数据层面没有损失</font>**<font style="color:rgb(25, 27, 31);">，但是</font>**<font style="color:#117CEE;">数据量大了N倍，训练的效率比较低</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

```python
[
  {
    "instruction": "用户指令（必填）",
    "input": "用户输入（选填）",
    "output": "模型回答（必填）",
    "system": "系统提示词（选填）",
    "history": [
      ["第一轮指令（选填）", "第一轮回答（选填）"],
      ["第二轮指令（选填）", "第二轮回答（选填）"]
    ]
  }
]
```



```python
{
  "instruction": "我想吃中餐",
  "input": "",
  "output": "好的，以下是一些中餐的推荐：\n\n火锅：如果你想吃辣的、热气腾腾的火锅，可以去尝试一下川味火锅或者麻辣火锅，这些可口的火锅在中国很受欢迎。\n\n粤菜：粤菜是中国南方广东省的菜系，口味清淡，讲究原汁原味。广东菜的标志性菜品包括烧鹅、蚝油牛肉、云吞、糯米鸡等等。\n\n湘菜：湘菜是中国湖南省的菜系，以酸、辣、香为特色。湘菜的代表性菜品包括剁椒鱼头、口味虾、毛氏红烧肉等等。\n\n川菜：川菜是中国四川省的菜系，口味麻辣，非常有特色。川菜的代表性菜品包括水煮鱼、麻婆豆腐、宫保鸡丁等等。\n\n以上是一些中餐的推荐，希望能为你提供帮助。",
  "history": [
    [
      "今天吃什么",
      "你想要吃哪种菜系的餐点呢？比如中餐、西餐、日餐等等。或者你有特殊的饮食偏好，比如素食、无麸质食品、低卡路里饮食等等，请告诉我你的需求，我会尽力为你提供有用的建议。"
    ],
    [
      "今天吃什么",
      "你想要吃哪种菜系的餐点呢？比如中餐、西餐、日餐等等。或者你有特殊的饮食偏好，比如素食、无麸质食品、低卡路里饮食等等，请告诉我你的需求，我会尽力为你提供有用的建议。"
    ]
  ]
}
```



:::color5
**<font style="color:#601BDE;">3.SFT Packing</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

Packing是将不同的文本序列数据，打包到同一个样本序列中。

+ <font style="color:rgb(25, 27, 31);">通常在训练中，我们对于一条文本数据，</font>**<font style="color:#117CEE;">需要将其padding到batch中最大长度（或者是padding到模型截断长度），然后进行计算。这样我们就会浪费一部分算力在padding的token上</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ <font style="color:rgb(25, 27, 31);">通过Packing的方法，</font>**<font style="color:#ED740C;">我们将多条数据packing到一起，有效的减少了padding的token数量，可以帮助我们加速训练。</font>**

:::color5
**<font style="color:#601BDE;">4.Llama Factory 中的 SFT Packing </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">多轮数据 Llama Factory</font>**

<font style="color:rgb(25, 27, 31);">在LLaMA Factory中会更加高效一些，对于</font>**<font style="color:#74B602;">多轮数据无需拆分，直接拼接到一起训练</font>**<font style="color:rgb(25, 27, 31);">。这里因为Causal Language Model的</font>**<font style="color:#74B602;">attention mask是一个下三角矩阵，保证当前token只能关注到自身以及自身之前的token</font>**<font style="color:rgb(25, 27, 31);">，这样就会保证我们在</font>**<font style="color:#74B602;">预测答案r1的时候，模型看到的只有p1，而不会看到后面的位置</font>**<font style="color:rgb(25, 27, 31);">。基于这个机制我们便可以计算整个多轮对话所有response的logits，</font>**<font style="color:rgb(25, 27, 31);">然后计算loss的时候仅仅考虑response部分，将所有prompt部分忽略掉即可</font>**<font style="color:rgb(25, 27, 31);">。如下图所示，这里构建labels的时候，我们将所有prompt-token对应的label置为-100（IGNORE INDEX），这样我们就可以只计算response部分的loss。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744083583669-81f51cd5-08d1-4605-ad2c-24a10573742d.png)

:::color5
**<font style="color:#601BDE;">5.SFT Packing - Version 1 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">这里最开始LLaMA Factory的实现方式如下：</font>

```python
total_length = len(input_ids)  # 这里将所有的数据合并到一起，得到所有token的长度
block_size = data_args.cutoff_len # 将截断长度设置为一个block的长度

total_length = (total_length // block_size) * block_size # 那么所有的block个数是 total length // block size

# 将数据按照block size进行切分，最终得到切分后的blocks
for i in range(0, total_length, block_size):
    if not all(label == IGNORE_INDEX for label in labels[i : i + block_size]):
        model_inputs["input_ids"].append(input_ids[i : i + block_size])
        model_inputs["attention_mask"].append([1] * block_size)
        model_inputs["labels"].append(labels[i : i + block_size])
```

<font style="color:rgb(25, 27, 31);">这里就是将所有的数据全部合并到一起，然后按照block_size(截断长度）进行切分，得到最终的数据。这是一个比较粗糙的做法，一个很明显的缺点是：</font>**<font style="color:#117CEE;">拼接的数据中，开头或者结尾的样本都丢失了信息，缺少上文或者下文。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744083928536-c2debf3d-3a00-4f70-9466-af9c85c6d8ff.png)

:::color5
**<font style="color:#601BDE;">5.SFT Packing - Version 2 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在最近的v8.0.2版本中，SFT Packing的实现方式如下：</font>

```python
model_inputs = {"input_ids": [], "attention_mask": [], "labels": []}
# 这里将长度排序，然后贪心检索最大长度加入，直到要超过cutoff-len
# 得到一个二维数组，里面是是每组数据包含的数据长度
# 如： [[2048],[1024,1023],[1000,1000,41],[500,500,500,500,40]]
knapsacks = greedy_knapsack(lengths, data_args.cutoff_len)

for knapsack in knapsacks:
    packed_input_ids, packed_labels = [], []
    for length in knapsack:
        index = length2indexes[length].pop()
        packed_input_ids += batch_input_ids[index]
        packed_labels += batch_labels[index]
    # 这里把padding位置的loss忽略掉，labels设置为IGNORE INDEX
    if len(packed_input_ids) < data_args.cutoff_len:
        pad_length = data_args.cutoff_len - len(packed_input_ids)
        packed_input_ids += [tokenizer.pad_token_id] * pad_length
        packed_labels += [IGNORE_INDEX] * pad_length

    if len(packed_input_ids) != data_args.cutoff_len:
        raise ValueError("The length of packed example should be identical to the cutoff length.")

    model_inputs["input_ids"].append(packed_input_ids)
    # 这里将所有的attention mask置为1
    model_inputs["attention_mask"].append([1] * data_args.cutoff_len)
    model_inputs["labels"].append(packed_labels)

```

<font style="color:rgb(25, 27, 31);">这里首先基于所有数据的长度进行检索，类似于背包问题，将其排序然后在截断长度之内贪心检索最合适的长度加入。例如排序之后我们得到如下数组：</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">[</font><font style="color:rgb(25, 27, 31);">[</font><font style="color:rgb(25, 27, 31);">2048</font><font style="color:rgb(25, 27, 31);">]</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">[</font><font style="color:rgb(25, 27, 31);">1024</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">1023</font><font style="color:rgb(25, 27, 31);">]</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">[</font><font style="color:rgb(25, 27, 31);">1000</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">1000</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">41</font><font style="color:rgb(25, 27, 31);">]</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">[</font><font style="color:rgb(25, 27, 31);">500</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">500</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">500</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">20</font><font style="color:rgb(25, 27, 31);">]</font><font style="color:rgb(25, 27, 31);">]</font>

+ <font style="color:rgb(25, 27, 31);">第一组数据包含一条样本，长度为2048</font>
+ <font style="color:rgb(25, 27, 31);">第二组数据包含两条样本，长度是1024+1023</font>
+ <font style="color:rgb(25, 27, 31);">最后一组数据包含四条数据，长度是500+500+500+20</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744084005993-9939dd6a-9c38-4847-983d-4db59ae57fa1.png)

<font style="color:rgb(25, 27, 31);">这样我们能够保证在截断长度之内塞下尽量多的数据，并且每一条数据都是完整的，这样就不会存在之前版本的上下文缺失问题。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">但是这样还有一个cross-contamination（交叉污染）问题。我们在不进行SFT Packing的情况下，</font>**<font style="color:rgb(25, 27, 31);">每一条样本的token只会关注自身以及样本之内自身之前的token</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#117CEE;">但是这里代码构建attention mask的时候，将所有的位置都置为了1，意味着当前token可以关注到之前文档中的token</font>**<font style="color:rgb(25, 27, 31);">，因此我们还需要对不同文档之间attention进行隔离。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744084042246-8468da74-1b76-4223-ba4e-83aa334eb70b.png)

:::color5
**<font style="color:#601BDE;">5.SFT Packing - Version 3 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">最新的LLaMA Facoty正在修正这个错误，在这个</font>[Issue](https://link.zhihu.com/?target=https%3A//github.com/hiyouga/LLaMA-Factory/pull/4224)<font style="color:rgb(25, 27, 31);">中。我们具体来看一下代码：</font>

<font style="color:rgb(25, 27, 31);">首先是构建Packing数据的时候：</font>

```python
model_inputs = {"input_ids": [], "attention_mask": [], "labels": []}
# 这里将长度排序，然后贪心检索最大长度加入，直到要超过cutoff-len
# 得到一个二维数组，里面是是每组数据包含的数据长度
# 如： [[2048],[1024,1023],[1000,1000,41],[500,500,500,500,40]]
knapsacks = greedy_knapsack(lengths, data_args.cutoff_len)
for knapsack in knapsacks:
    packed_input_ids, packed_attention_masks, packed_labels = [], [], []
    for i, length in enumerate(knapsack):
        index = length2indexes[length].pop()
        packed_input_ids += batch_input_ids[index]
        packed_labels += batch_labels[index]
        # 这里分为两种做法
        if data_args.neat_packing:
            # 将attention mask进行区分，不同文档使用不同的标识符，然后padding部分用0标识
            # 例如 [1,1,1,1,2,2,2,3,3,3,0,0]
            packed_attention_masks += [i + 1] * len(batch_input_ids[index])  # start from 1
        else:
            # 这里还是按照之前全部置为1
            packed_attention_masks += [1] * len(batch_input_ids[index])

    # 这里把padding位置的loss忽略掉，labels设置为IGNORE INDEX
    if len(packed_input_ids) < data_args.cutoff_len:
        pad_length = data_args.cutoff_len - len(packed_input_ids)
        packed_input_ids += [tokenizer.pad_token_id] * pad_length
        packed_labels += [IGNORE_INDEX] * pad_length
        if data_args.neat_packing:
            packed_attention_masks += [0] * pad_length
        else:
            packed_attention_masks += [1] * pad_length  # more efficient flash_attn

    if len(packed_input_ids) != data_args.cutoff_len:
        raise ValueError("The length of packed example should be identical to the cutoff length.")

    model_inputs["input_ids"].append(packed_input_ids)
    model_inputs["attention_mask"].append(packed_attention_masks)
    model_inputs["labels"].append(packed_labels)
```

<font style="color:rgb(25, 27, 31);">这里相较于之前加入了一些改动，对attention mask进行区分，不同文档使用不同的标识符，然后padding部分用0标识。例如：</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">[</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">1</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">2</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">3</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">3</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">3</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">3</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">4</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">4</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">4</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">0</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);">0</font><font style="color:rgb(25, 27, 31);">]</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">,表示前5个token是第一个文档，第6-9个token是第二个文档，最后两个token是padding。</font>

<font style="color:rgb(25, 27, 31);">你可能会有一些疑问，怎么attention mask还能长这样，不应该是一个0、1组成的数组吗？当然，这里并不是我们最终输入的attention mask。</font>**<font style="color:#74B602;">往常我们输入的attention mask是一个0、1数组，然后再模型内部会转变成一个4D mask</font>**<font style="color:rgb(25, 27, 31);">。之前4D mask是不支持自定义的，只能在模型内部进行转换，但是现在</font>[<font style="color:rgb(9, 64, 142);">transformers</font>](https://zhida.zhihu.com/search?content_id=245315792&content_type=Article&match_order=1&q=transformers&zhida_source=entity)<font style="color:rgb(25, 27, 31);">支持自定义4D mask了，我们可以依据前面的attention mask来自定义我们的4D mask来区分不同文档。</font>

**4D MASK**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">首先我们看一下什么是4D mask，通常我们输入的attention mask是一个二维数组，维度是[bs, seq_len]，由0、1组成。然后在模型内部，会变成一个4D 矩阵，维度是 </font>**<font style="color:#74B602;">[bs, num_heads, seq_len, seq_len]</font>**<font style="color:rgb(25, 27, 31);">。对于batch中的一条数据而言，attention mask转换如下，就构成了一个维度是[1, seq_len, seq_len]的attention mask：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744084196664-29994201-2307-4e2b-bba5-5300141e991c.png)

<font style="color:rgb(25, 27, 31);">对batch中每一条数据进行上面的操作，然后复制num_heads份，就可以构成4D mask，维度是[bs, num_heads, seq_len, seq_len]。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">上面是4D mask的一些概念，那么回到之前LLaMA Factory中，我们在attention mask中对不同文档进行区分，接下里在构建数据的时候，会对attention mask进行转换，构建一个自定义的4D attention mask。代码如下：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

```python
def prepare_4d_attention_mask(attention_mask_with_indices: "torch.Tensor", dtype: "torch.dtype") -> "torch.Tensor":
    r"""
    Expands the attention mask with indices from (batch_size, seq_len) to (batch_size, 1, seq_len, seq_len),
    while handles packed sequences and transforms the mask to lower triangular form to prevent future peeking.
    （by草莓师姐）
    e.g.
    ```
    [[1, 1, 2, 2, 2, 0]]
    ```
    ->
    ```
    [
        [
            [
                [o, x, x, x, x, x],
                [o, o, x, x, x, x],
                [x, x, o, x, x, x],
                [x, x, o, o, x, x],
                [x, x, o, o, o, x],
                [x, x, x, x, x, x],
            ]
        ]
    ]
    ```
    where `o` equals to `0.0`, `x` equals to `min_dtype`.
    """
    bsz, seq_len = attention_mask_with_indices.size()
    # 获取-inf的值
    min_dtype = torch.finfo(dtype).min
    ## 这里把我们之前的attention mask由 [bs, seq_len], 变为[bs, 1, seq_len, seq_len]
    expanded_mask = attention_mask_with_indices[:, None, None, :].expand(bsz, 1, seq_len, seq_len)
    # 创建一个二进制的attention mask， 非0的值设置为1，否则为0
    padding_mask = torch.where(expanded_mask != 0, 1, 0)
    # 创建一个对角掩码矩阵（block-diagonal mask）
    # 这里判断expand mask矩阵和转秩后的expand mask是否相等，相等的地方是1，不相等是0
    # 前面我们讲不同文档设置不同的id，这里就可以发挥出作用了，同一文档之间id相同
    attention_mask_4d = torch.eq(expanded_mask, expanded_mask.transpose(-1, -2)).int() * padding_mask
    # 创建一个下三角矩阵，Causal Language Model的标配
    attention_mask_4d *= torch.tril(torch.ones((seq_len, seq_len), dtype=torch.long))
    # 转换一下4D矩阵， 1的位置变成0， 0的位置变成-inf，用于后续sofmax计算
    attention_mask_4d = torch.where(attention_mask_4d != 0, torch.tensor(0, dtype=dtype), min_dtype)
    return attention_mask_4d
```

<font style="color:rgb(25, 27, 31);">通过这一步，我们就作出了一个需要的4D mask， 我们期望同一个文档之间的token能够进行attention，不同文档之间的token不能进行attention。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744084143954-fee9eac1-bd18-4ee3-8efa-8ab7f9a8e828.png)

# 多轮对话
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">为了让大模型能更好的响应人类的指令，FLAN-T5工作率先提出了指令微调（</font>[<font style="color:rgb(9, 64, 142);">instruction tuning</font>](https://zhida.zhihu.com/search?content_id=242619863&content_type=Article&match_order=1&q=instruction+tuning&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）这个概念，我们不细讲encoder-decoder时期的情况，从大模型时刻直接开始。大模型时刻的指令微调不仅仅考虑了对人类指令和多任务的适应性，更是希望能将角色系统融入大模型中，从而让大模型变成chat模型，这类型的模型很多，比如</font>[<font style="color:rgb(9, 64, 142);">Qwen1.5-7B-chat</font>](https://zhida.zhihu.com/search?content_id=242619863&content_type=Article&match_order=1&q=Qwen1.5-7B-chat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，Gemma-2B-it【此处it就是指令微调的缩写】等等，【指令微调并不直接产生chat model，只是其中必不可少的一步】</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">多轮对话里必不可少的存在“角色”这个概念，因为和大模型的对话仅限于用户和模型，所以极大多数的</font>**<font style="color:rgb(25, 27, 31);">对话模板（</font>**<font style="color:rgb(25, 27, 31);">template</font>**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">里都只考虑了两个角色——user和assistant。【注意，对话模板只有非base模型才需要，所以很多的base模型的tokenizer里并不携带chat_template】</font>

**参考：**[**任务型多轮对话（一）**](https://zhuanlan.zhihu.com/p/679487747)[多轮对话的训练过程详解](https://zhuanlan.zhihu.com/p/695202364)

:::

多轮对话数据示例

```python
[
  {
    "instruction": "用户指令（必填）",
    "input": "用户输入（选填）",
    "output": "模型回答（必填）",
    "system": "系统提示词（选填）",
    "history": [
      ["第一轮指令（选填）", "第一轮回答（选填）"],
      ["第二轮指令（选填）", "第二轮回答（选填）"]
    ]
  }
]
```



```python
{
  "instruction": "我想吃中餐",
  "input": "",
  "output": "好的，以下是一些中餐的推荐：\n\n火锅：如果你想吃辣的、热气腾腾的火锅，可以去尝试一下川味火锅或者麻辣火锅，这些可口的火锅在中国很受欢迎。\n\n粤菜：粤菜是中国南方广东省的菜系，口味清淡，讲究原汁原味。广东菜的标志性菜品包括烧鹅、蚝油牛肉、云吞、糯米鸡等等。\n\n湘菜：湘菜是中国湖南省的菜系，以酸、辣、香为特色。湘菜的代表性菜品包括剁椒鱼头、口味虾、毛氏红烧肉等等。\n\n川菜：川菜是中国四川省的菜系，口味麻辣，非常有特色。川菜的代表性菜品包括水煮鱼、麻婆豆腐、宫保鸡丁等等。\n\n以上是一些中餐的推荐，希望能为你提供帮助。",
  "history": [
    [
      "今天吃什么",
      "你想要吃哪种菜系的餐点呢？比如中餐、西餐、日餐等等。或者你有特殊的饮食偏好，比如素食、无麸质食品、低卡路里饮食等等，请告诉我你的需求，我会尽力为你提供有用的建议。"
    ],
    [
      "今天吃什么",
      "你想要吃哪种菜系的餐点呢？比如中餐、西餐、日餐等等。或者你有特殊的饮食偏好，比如素食、无麸质食品、低卡路里饮食等等，请告诉我你的需求，我会尽力为你提供有用的建议。"
    ]
  ]
}
```



:::color5
**<font style="color:#601BDE;">1.单轮训练过程</font>**

:::

1. **单轮数据：**

```plain
chat_dict = [
                {"role": "user", "content": U},
                {"role": "assistant", "content": A},
            ]
```

2. **<font style="color:rgb(25, 27, 31);">input_ids</font>**

<font style="color:rgb(25, 27, 31);">input_ids= [BOS][INST]U[\INST]A[EOS]</font>

> <font style="color:rgb(25, 27, 31);">BOS：用来引导decoder部分开始解码</font>
>
> <font style="color:rgb(25, 27, 31);">EOS：用来标志decoder生成结束的。</font>
>
> <font style="color:rgb(25, 27, 31);">[INST]：</font>[<font style="color:rgb(9, 64, 142);">LLAMA2-chat</font>](https://zhida.zhihu.com/search?content_id=242619863&content_type=Article&match_order=1&q=LLAMA2-chat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的对话模板中user标识</font>
>
> <font style="color:rgb(25, 27, 31);">[/INST]： </font>[<font style="color:rgb(9, 64, 142);">LLAMA2-chat</font>](https://zhida.zhihu.com/search?content_id=242619863&content_type=Article&match_order=1&q=LLAMA2-chat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的对话模板中assistant标识</font>
>

3. **Labels**

<font style="color:rgb(25, 27, 31);">可以根据</font>**<font style="color:rgb(25, 27, 31);">学习模式</font>**<font style="color:rgb(25, 27, 31);">来确定LABELS。</font>

+ <font style="color:rgb(25, 27, 31);">初步</font>**<font style="color:rgb(25, 27, 31);">学习模式</font>**<font style="color:rgb(25, 27, 31);">：[BOS][INST]U[\INST] → A[EOS]。</font>
+ <font style="color:rgb(25, 27, 31);">真正学习模式： [/INST] → A ， A → [EOS]。根据</font>**<font style="color:#74B602;">next token prediciton的性质，我们需要做一些移位操作</font>**

```python
Input: [BOS][INST]U[\INST]A[EOS]
label:   x    x   x   x   A[EOS]
```

```python
Input: [BOS][INST]U[\INST]A[EOS]
label:         x  x   x   x  A [EOS]
```

:::color5
**<font style="color:#601BDE;">2.多轮训练过程</font>**

:::

1. **多轮数据：**

```plain
chat_dict = [
                {"role": "user", "content": U1},
                {"role": "assistant", "content": A1},
                {"role": "user", "content": U2},
                {"role": "assistant", "content": A2},
            ]
```

2. **<font style="color:rgb(25, 27, 31);">input_ids</font>**

<font style="color:rgb(25, 27, 31);">input_ids= [BOS][INST]U1[\INST]A1[EOS][BOS][INST]U2[\INST]A2[EOS]</font>

> <font style="color:rgb(25, 27, 31);">BOS：用来引导decoder部分开始解码</font>
>
> <font style="color:rgb(25, 27, 31);">EOS：用来标志decoder生成结束的。</font>
>
> <font style="color:rgb(25, 27, 31);">[INST]：</font>[<font style="color:rgb(9, 64, 142);">LLAMA2-chat</font>](https://zhida.zhihu.com/search?content_id=242619863&content_type=Article&match_order=1&q=LLAMA2-chat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的对话模板中user标识</font>
>
> <font style="color:rgb(25, 27, 31);">[/INST]： </font>[<font style="color:rgb(9, 64, 142);">LLAMA2-chat</font>](https://zhida.zhihu.com/search?content_id=242619863&content_type=Article&match_order=1&q=LLAMA2-chat&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的对话模板中assistant标识</font>
>

3. **Labels**

<font style="color:rgb(25, 27, 31);">可以根据</font>**<font style="color:rgb(25, 27, 31);">学习模式</font>**<font style="color:rgb(25, 27, 31);">来确定LABELS。</font>

+ <font style="color:rgb(25, 27, 31);">初步</font>**<font style="color:rgb(25, 27, 31);">学习模式</font>**<font style="color:rgb(25, 27, 31);">：[BOS][INST]U[\INST] → A[EOS]。</font>
+ <font style="color:rgb(25, 27, 31);">真正学习模式： [/INST] → A ， A → [EOS]。根据</font>**<font style="color:#74B602;">next token prediciton的性质，我们需要做一些移位操作</font>**

```plain
Input: [BOS][INST]U1[\INST]A1[EOS][BOS][INST]U2[\INST]A2[EOS]
label:         x  x    x   x  A1  [EOS]   x  x    x   x  A2  [EOS]
```



