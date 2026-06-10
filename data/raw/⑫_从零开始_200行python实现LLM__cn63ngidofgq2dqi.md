# ⑫ 从零开始:200行python实现LLM

<!-- source: yuque://zhongxian-iiot9/hlyypb/cn63ngidofgq2dqi -->

_<font style="color:rgba(255, 255, 255, 0.3);">年05月29日 08:1</font>_ _<font style="color:rgba(255, 255, 255, 0.3);">浙</font>_

# 前言
:::color3
**<font style="color:rgb(62, 62, 62);">简介：</font>**<font style="color:rgb(62, 62, 62);">大语言模型（LLM）很火，讨论的文章铺天盖地，但对于没有机器学习背景的人来说，看多了只是粗浅了解了一堆概念，疑惑只增不减。本文尝试从零开始，用python实现一个极简但完整的大语言模型，在过程中把各种概念“具象化”，让大家亲眼看到、亲手写出self-attention机制、transformer模型，亲自感受下训练、推理中会遇到的一些问题</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748657117543-e76e8985-17a4-476c-a90a-41d90fb22e05.png)

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1748657103029-193077f6-b4f2-4369-855d-2ba80d909b81.jpeg)

:::color5
**<font style="color:#601BDE;">1.本文适用范围及目标</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">‒</font><font style="color:rgb(62, 62, 62);">✅</font><font style="color:rgb(62, 62, 62);">只需会写基本的python代码；</font>

<font style="color:rgb(62, 62, 62);">‒</font><font style="color:rgb(62, 62, 62);">✅</font><font style="color:rgb(62, 62, 62);">尝试实现完整的语言模型（但由于层数、dataset限制，只会写诗词）；</font>

<font style="color:rgb(62, 62, 62);">‒</font><font style="color:rgb(62, 62, 62);">❌</font><font style="color:rgb(62, 62, 62);">不解释数学、机器学习原理性的知识，只做到“能用”为止；</font>

<font style="color:rgb(62, 62, 62);">‒</font><font style="color:rgb(62, 62, 62);">❌</font><font style="color:rgb(62, 62, 62);">不依赖抽象层次高的框架，用到的部分也会做解释；</font>

:::color5
**<font style="color:#601BDE;">2.代码链接</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

```python
‒karpathy/nanoGPT：https://github.com/karpathy/nanoGPT
‒simpx/buildyourownllm：https://github.com/simpx/buildyourownllm
‒《深度学习入门 基于Python的理论与实现》
[1]https://github.com/karpathy/nanoGPT)
[2]https://github.com/simpx/buildyourownllm/
[3]https://github.com/simpx/buildyourownllm/blob/main/simplemodel_with_comments.py
[4]https://github.com/simpx/buildyourownllm/blob/main/simplebigrammodel_with_comments.py
[5]https://github.com/simpx/buildyourownllm/blob/main/simplebigrammodel_torch.py
[6]https://github.com/simpx/buildyourownllm/blob/main/babygpt_v1.py
```

<font style="color:rgb(62, 62, 62);">相关代码都在Github仓库：</font>

<font style="color:rgb(62, 62, 62);"></font><font style="color:rgb(62, 62, 62);">simpx/buildyourownllm</font><font style="color:rgb(62, 62, 62);"> [2]上，建议先clone下来，并通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">pip install torch</font>`<font style="color:rgb(62, 62, 62);"> 安装唯一的依赖后，在仓库目录下运行各个代码体验过程。</font>

<font style="color:rgb(62, 62, 62);">动手写代码最容易把抽象的概念具象化，非常建议使用vscode + ipynb的组合调试文中的代码，鉴于篇幅，不额外介绍工具。</font>

<font style="color:rgb(62, 62, 62);">本文先介绍“从零基础到Bigram模型”，下一篇文章再介绍“从Bigram模型到LLM”。</font>

# 先用传统方式实现一个“诗词生成器”
:::color3
<font style="color:rgb(62, 62, 62);">让我们忘记机器学习，用传统思路来实现一个“诗词生成器”。</font>

:::

:::color5
**<font style="color:#601BDE;">1.数据集</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">观察一下我们的数据集 </font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">ci.t</font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">xt</font>`<font style="color:rgb(62, 62, 62);"> ，里面包含了宋和南唐的词，我们的目标是实现一个生成类似诗词的工具。</font>

```python
$ head -n 8 ci.txt虞美人 李煜春花秋月何时了，往事知多少？小楼昨夜又东风，故国不堪回首月明中。雕栏玉砌应犹在，只是朱颜改。问君能有几多愁？恰似一江春水向东流。
乌夜啼 李煜昨夜风兼雨，帘帏飒飒秋声。
```

:::color5
**<font style="color:#601BDE;">2.诗词生成器</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">词是由一堆字组成的，那么一个简单的想法，我们可以通过计算每个字后面出现各个字的概率。</font>

<font style="color:rgb(62, 62, 62);">然后根据这些概率，不断的递归生成“下一个字”，生成的字多了，截断一部分，就是一首词了。</font>

<font style="color:rgb(62, 62, 62);">具体思路为：</font>

+ **<font style="color:rgb(62, 62, 62);">准备</font>****<font style="color:rgb(62, 62, 62);">词汇表</font>****<font style="color:rgb(62, 62, 62);">：</font>**<font style="color:rgb(62, 62, 62);">将</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">ci.txt</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">出现的所有字去重，得到我们的词汇表，长度为</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">vocab_size</font><font style="color:rgb(62, 62, 62);">；</font>`
+ **<font style="color:rgb(62, 62, 62);">统计</font>****<font style="color:rgb(62, 62, 62);">频率</font>****<font style="color:rgb(62, 62, 62);">：</font>**<font style="color:rgb(62, 62, 62);">准备一个</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">vocab_size * vocab_size</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">的字典，统计每个词后出现别的词的频率；</font>
+ **<font style="color:rgb(62, 62, 62);">计算</font>****<font style="color:rgb(62, 62, 62);">概率</font>****<font style="color:rgb(62, 62, 62);">，生成新“字”：</font>**<font style="color:rgb(62, 62, 62);">根据频率计算概率，并随机采样，生成下一个字；</font>

<font style="color:rgb(62, 62, 62);">完整的代码如下（带注释版的见simplemodel_with_comments.py[3]）：</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

```python
import random

random.seed(42) # 去掉此行，获得随机结果

prompt = "春江"
max_new_token = 100

with open('ci.txt', 'r', encoding='utf-8') as f:
    text = f.read()

chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

transition = [[0 for _ in range(vocab_size)] for _ in range(vocab_size)]

for i in range(len(text) - 1):
    current_token_id = encode(text[i])[0]
    next_token_id = encode(text[i + 1])[0]
    transition[current_token_id][next_token_id] += 1

generated_token = encode(prompt)

for i in range(max_new_token - 1):
    current_token_id = generated_token[-1]
    logits = transition[current_token_id]
    total = sum(logits)
    logits = [logit / total for logit in logits]
    next_token_id = random.choices(range(vocab_size), weights=logits, k=1)[0]
    generated_token.append(next_token_id)
    current_token_id = next_token_id

print(decode(generated_token))
```

<font style="color:rgb(62, 62, 62);">直接通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">python simplemodel.py</font>`<font style="color:rgb(62, 62, 62);"> 即可运行，去掉</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">random.seed(42)</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">可以看到不同的输出结果。</font>

<font style="color:rgb(62, 62, 62);">在我的mac电脑上耗时2秒，效果如下：</font>

```python

$ python simplemodel.py
春江月 张先生疑被。

倦旅。
清歌声月边、莼鲈清唱，尽一卮酒红蕖花月，彩笼里繁蕊珠玑。
只今古。
浣溪月上宾鸿相照。
乞团，烟渚澜翻覆古1
半吐，还在蓬瀛烟沼。
木兰花露弓刀，更任东南楼缥缈。
黄柳，
```

<font style="color:rgb(62, 62, 62);">这像是一首名为“春江月”、作者为“张先生疑被。”的词，但其实我们只是实现了一个“下一个词预测器”。</font>

<font style="color:rgb(62, 62, 62);">在代码的眼里，只不过“春”字后面大概率是“江”，而“江”字后面大概率是“月”而已，它不知道什么是词，甚至不知道什么是一首词的开头、结尾。</font>

<font style="color:rgb(62, 62, 62);">这个字符序列层面的“意义”，实际上是由读者赋予的。</font>

:::color5
**<font style="color:#601BDE;">3.词汇表 - tokenizer</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">我们的“词汇表”，相当于LLM里的tokenizer，只不过我们直接使用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">ci.txt</font>`<font style="color:rgb(62, 62, 62);"> 里出现过的所有字符当做词汇表用。我们的词汇表只有6418个词汇，而真正的LLM有更大的vocab_size，以及更高效的编码，一些常用词组直接对应1个token，比如下面是qwen2.5的tokenizer。</font>

```python
>>> from transformers import AutoTokenizer
>>> tokenizer = AutoTokenizer.from_pretained('Qwen/Qwen2.5-0.5B')
>>> tokenizer.vocab_size
151643
>>> tokenizer.encode("春江花月夜")
[99528, 69177, 99232, 9754, 99530]
>>> tokenizer.encode("草莓师姐")
[107076]
>>> tokenizer.encode("草莓软糖")
[102661, 101935]
>>> tokenizer.encode("人工智能")
[104455]
>>> tokenizer.decode([102661, 104455, 101935])
'草莓人工智能'
```

<font style="color:rgb(62, 62, 62);">qwen2.5使用了一个大小为151643的词汇表，其中常见的词汇“草莓师姐”、“人工智能”都只对应1个token，而在我们的词汇表里，1个字符永远对应1个token，编码效率较低。</font>

:::color5
**<font style="color:#601BDE;">4.模型、训练、推理</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">我们刚刚实现的“模型”，实际是就是自然语言N-gram模型中的“Bigram模型”。这是一种基于统计的语言模型，用于预测一个词出现的概率，在这个模型中，假设句子中的每个字只依赖于其前面的一个字。具体的实现就是一个词频字典</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">tra</font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nsiti</font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">on</font>`<font style="color:rgb(62, 62, 62);">，而所谓的“训练”过程就是遍历所有数据，统计“下一个词”出现的频率。但我们的“推理”过程还是非常像真正的LLM的，步骤如下：</font>

1. <font style="color:rgb(62, 62, 62);">我们从</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">transition</font>`<font style="color:rgb(62, 62, 62);"> 中获取下一个token的logits（logits是机器学习中常用的术语，表示最后一层的原始输出值），我们可以把</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">logits[i]</font>`<font style="color:rgb(62, 62, 62);">简单理解为“下一个token_id是i的得分”，因此logits肯定是长度为vocab_size的字典；</font>
2. <font style="color:rgb(62, 62, 62);">获得“得分字典”后，使用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">[logit / total for logit in logits]</font>`<font style="color:rgb(62, 62, 62);"> 做归一化处理，这是为了下一步更好的做随机采样。在这里我们使用最简单的线性归一，不考虑total为0的情况；</font>
3. <font style="color:rgb(62, 62, 62);">根据归一后的“得分字典”，使用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">random.choices</font>`<font style="color:rgb(62, 62, 62);"> 随机获取一个token id并返回；</font>
4. <font style="color:rgb(62, 62, 62);">循环反复，直到获得足够多的token。</font>

# 进行重构，更加有“机器学习风格”
:::color3
<font style="color:rgb(62, 62, 62);">接下来我们把Bigram模型的实现变得更加“机器学习风格”，以便帮助我们理解后面真实的pytorch代码，有pytorch背景的同学可以直接跳过本节。</font>

:::

:::color5
**<font style="color:#601BDE;">1.机器学习风格代码重构</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">完整的代码码如下（带注释版的见simplebigrammodel_with_comments.py[4]）：</font>

```python
import random
from typing import List

random.seed(42) # 去掉此行，获得随机结果
prompts = ["春江", "往事"]
max_new_token = 100
max_iters = 8000
batch_size = 32
block_size = 8
with open('ci.txt', 'r', encoding='utf-8') as f:
    text = f.read()
class Tokenizer:
    def __init__(self, text: str):
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}
    
    def encode(self, s: str) -> List[int]:
        return [self.stoi[c] for c in s]
    
    def decode(self, l: List[int]) -> str:
        return''.join([self.itos[i] for i in l])
class BigramLanguageModel():
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size
        self.transition = [[0 for _ in range(vocab_size)] 
                          for _ in range(vocab_size)]
        
    def __call__(self, x):
        # 方便直接调用model(x)
        return self.forward(x)
    
    def forward(self, idx: List[List[int]]) -> List[List[List[float]]]:
        '''
        输入idx，是一个二维数组，如[[1, 2, 3],
                                  [4, 5, 6]]
        表示同时希望推理的多个序列
        输出是一个三维数组，如[[[0.1, 0.2, 0.3, .. (vocab_size)],
                                [0.4, 0.5, 0.6, .. (vocab_size)],
                                [0.7, 0.8, 0.9, .. (vocab_size)]],
                               [[0.2, 0.3, 0.4, .. (vocab_size)],
                                [0.5, 0.6, 0.7, .. (vocab_size)],
                                [0.8, 0.9, 1.0, .. (vocab_size)]]]
        
        '''
        B = len(idx)  # 批次大小
        T = len(idx[0])  # 每一批的序列长度
        
        logits = [
            [[0.0 for _ in range(self.vocab_size)] 
             for _ in range(T)]
            for _ in range(B)
        ]
        
        for b in range(B):
            for t in range(T):
                current_token = idx[b][t]
                # 计算了每一个token的下一个token的概率
                logits[b][t] = self.transition[current_token]
                
        return logits
    def generate(self, idx: List[List[int]], max_new_tokens: int) -> List[int]:
        for _ in range(max_new_tokens):
            logits_batch = self(idx)
            for batch_idx, logits in enumerate(logits_batch):
                # 我们计算了每一个token的下一个token的概率
                # 但实际上我们只需要最后一个token的“下一个token的概率”
                logits = logits[-1]
                total = max(sum(logits),1)
                # 归一化
                logits = [logit / total for logit in logits]
                # 根据概率随机采样
                next_token = random.choices(
                    range(self.vocab_size),
                    weights=logits,
                    k=1
                )[0]
                idx[batch_idx].append(next_token)
        return idx
    
def get_batch(tokens, batch_size, block_size):
    '''
    随机获取一批数据x和y用于训练
    x和y都是二维数组，可以用于并行训练
    其中y数组内的每一个值，都是x数组内对应位置的值的下一个值
    格式如下：
    x = [[1, 2, 3],
         [9, 10, 11]]
    y = [[2, 3, 4],
         [10, 11, 12]]
    '''
    ix = random.choices(range(len(tokens) - block_size), k=batch_size)
    x, y = [], []
    for i in ix:
        x.append(tokens[i:i+block_size])
        y.append(tokens[i+1:i+block_size+1])
    return x, y
tokenizer = Tokenizer(text)
vocab_size = tokenizer.vocab_size
tokens = tokenizer.encode(text)
model = BigramLanguageModel(vocab_size)
# 训练
for iter in range(max_iters):
    x_batch, y_batch = get_batch(tokens, batch_size, block_size)
    for i in range(len(x_batch)):
        for j in range(len(x_batch[i])):
            x = x_batch[i][j]
            y = y_batch[i][j]
            model.transition[x][y] += 1
prompt_tokens = [tokenizer.encode(prompt) for prompt in prompts]
# 推理
result = model.generate(prompt_tokens, max_new_token)
# decode
for tokens in result:
    print(tokenizer.decode(tokens))
    print('-'*10)
```

<font style="color:rgb(62, 62, 62);">虽然有100多行代码，但实际上功能和上一个50行代码几乎是一样的，稍微运行、调试一下就能明白。</font>

<font style="color:rgb(62, 62, 62);">直接通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">python simplebigrammodel.py</font>`<font style="color:rgb(62, 62, 62);"> 即可运行，这一次会生成2个字符序列：</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

```python
春江红紫霄效颦。

怎。
兰修月。
两个事对西风酒伴寄我登临，看雪惊起步，总不与泪满南园春来。
最关上阅。
信断，名姝，夜正坐认旧武仙 朱弦。

岁，回。


看一丝竹。
愿皇受风，当。

妆一笑时，不堪
----------
往事多闲田舍、十三楚珪
酒困不须紫芝兰花痕皱，青步虹。
暗殿人物华高层轩者，临江渌池塘。
三峡。
天、彩霞冠
燕翻云垂杨、一声羌笛罢瑶觥船窗幽园春生阵。
长桥。
无恙，中有心期。

开处。
燕姹绿遍，烂□
----------
```

:::color5
**<font style="color:#601BDE;">2.机器学习风格的一些约定</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">解释一下这100多行代码的实现：</font>

<font style="color:rgb(62, 62, 62);">我们用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">Tokenizer</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">类封装了词汇表，以便它能像qwen的词汇表一样被使用。</font>

<font style="color:rgb(62, 62, 62);">同时，我们实现了一个</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">BigramLanguageModel</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">类，这模仿pytorch里的</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nn.Module</font>`<font style="color:rgb(62, 62, 62);"> 写法，即：</font>

<font style="color:rgb(62, 62, 62);">1.参数在</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">__init__</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">中初始化；</font>

<font style="color:rgb(62, 62, 62);">2.推理在</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">forward</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">函数中实现，并通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">__call__</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">允许对象被直接调用；</font>

<font style="color:rgb(62, 62, 62);">3.序列生成在</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">generate</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">函数中实现；</font>

<font style="color:rgb(62, 62, 62);">最后，我们修改了数据加载的机制，如下：</font>

```python
def get_batch(tokens, batch_size, block_size):
    ix = random.choices(range(len(tokens) - block_size), k=batch_size)
    x, y = [], []
    for i in ix:
        x.append(tokens[i:i+block_size])
        y.append(tokens[i+1:i+block_size+1])
    return x, y
```

<font style="color:rgb(62, 62, 62);">每次调用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">get_batch</font>`<font style="color:rgb(62, 62, 62);"> 的时候，会随机返回两份数据，其中</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">y</font>`<font style="color:rgb(62, 62, 62);"> 数组中的每一个token，都是</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">x</font>`<font style="color:rgb(62, 62, 62);"> 数组内对应位置的token的下一个token。采用这样的写法，</font><font style="color:rgb(62, 62, 62);">是为了方便后续操</font><font style="color:rgb(62, 62, 62);">作。</font>

:::color5
**<font style="color:#601BDE;">3.批处理in，批处理out</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">这一个版本最难懂的地方，是数据都以多维数组的方式呈现，连推理结果返回的都是2个。</font>

<font style="color:rgb(62, 62, 62);">实际上，我们这里的“多维数组”，就是机器学习中的</font>**<font style="color:rgb(62, 62, 62);">“张量”（Tensor）</font>**<font style="color:rgb(62, 62, 62);">，是为了最终方便GPU处理而准备的。</font>

**<font style="color:rgb(62, 62, 62);">张量（Tensor）</font>**<font style="color:rgb(62, 62, 62);">是数学和物理学中用于表示多维数据的对象，广泛应用于机器学习、深度学习和计算机视觉等领域。在深度学习框架（如 TensorFlow 和 PyTorch）中，张量是数据的基本结构。</font>

<font style="color:rgb(62, 62, 62);">而我们代码中低效的for循环，未来在GPU中都会被高效的并行计算。</font>

<font style="color:rgb(62, 62, 62);">我们先以传统思维来仔细看一下</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">forward</font>`<font style="color:rgb(62, 62, 62);"> 函数的实现，以进一步理解“张量”和“批处理”。</font>

```python
def forward(self, idx: List[List[int]]) -> List[List[List[float]]]:
    B = len(idx)  # 批次大小
    T = len(idx[0])  # 每一批的序列长度
    
    logits = [
        [[0.0for _ in range(self.vocab_size)] 
         for _ in range(T)]
        for _ in range(B)
    ]
    
    for b in range(B):
        for t in range(T):
            current_token = idx[b][t]
            # 计算了每一个token的下一个token的概率
            logits[b][t] = self.transition[current_token]
            
    return logits
```

`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">forward</font>`<font style="color:rgb(62, 62, 62);"> 函数的入参是一个大小为B * T的二维数组，按照机器学习领域的说法，就是一个</font><font style="color:rgb(62, 62, 62);">形状</font><font style="color:rgb(62, 62, 62);">为(B, T)的“</font><font style="color:rgb(62, 62, 62);">张量</font><font style="color:rgb(62, 62, 62);">”，表示输入了“B”批次的数据，每个批次包含“T”个token。</font>

<font style="color:rgb(62, 62, 62);">这里B、T、C都是机器学习里的常用变量名，B（Batch Size）代表批量大小、T（Time Steps or Sequence Length）对于序列数据来说代表序列的长度、C（Channels）在图像处理中代表通道数，在语言模型中可以表示特征维度。</font>

<font style="color:rgb(62, 62, 62);">返回值</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">logits</font>`<font style="color:rgb(62, 62, 62);"> 是一个形状为(B, T, C)的张量（C等于vocab_size），它表示了“每个批次”的序列中，“每个token”的下一个token的频率。这么说起来很绕，其实只要想象成：“所有B*T个数的token，都有一张独立的表，表中记录了下一个出现的token是X的频率”。</font>

<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">logits</font><font style="color:rgb(62, 62, 62);"> 的大小为B * T * C，由于我们是Bigram模型，每个token的概率只和它上一个token有关，所以实际上我们只需要计算批次中最后一个token的logit就可以了，但为了和以后的模型统一，依旧保留了这些冗余计算。</font>

:::color4
**<font style="color:rgb(62, 62, 62);">好消息，我们现在已经有了一个能跑的玩具“模型”，它能根据概率预测下一个词，但却缺乏了真正的训练过程。</font>**

**<font style="color:rgb(62, 62, 62);">坏消息，在实现真正的机器学习之前，我们还是绕不开pytorch。不过幸运的是，我们只需要做到“知其然”即可。</font>**

:::

# 5分钟简明pytorch教程
:::color3
<font style="color:rgb(62, 62, 62);">PyTorch 是一个开源的深度学习库，提供一系列非常方便的基础数据结构和函数，简化我们的操作。</font>

:::

:::color5
**<font style="color:#601BDE;">1.pytorch实现线性回归</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">下面是一个使用pytorch实现线性回归的简单例子：</font>

```python
import torch
from torch import nn
from torch.nn import functional as F

torch.manual_seed(42) # 随机数种子，方便复现

# 判断环境中是否有GPU
device = 'cuda'if torch.cuda.is_available() else'mps'if torch.mps.is_available() else'cpu'
print(f"Using {device} device")

# 1. 创建tensor演示
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([2.0, 4.0, 6.0])

# 2. 基本运算演示
print(x + y)                # 加法: tensor([3., 6., 9.])
print(x * y)                # 点乘: tensor([2., 8., 18.])
print(torch.matmul(x, y))   # 矩阵乘法: tensor(28.)
print(x @ y)                # 另一种矩阵乘写法: tensor(28.)
print(x.shape)              # tensor的形状: torch.Size([3])

# 3. 定义模型
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)  # 输入维度=1，输出维度=1
    
    def forward(self, x):
        return self.linear(x)

# 4. 生成训练数据
# 真实关系: y = 2x + 1
x_train = torch.rand(100, 1) * 10  # 生成 0-10 之间的随机数
y_train = 2 * x_train + 1 + torch.randn(100, 1) * 0.1  # 真实函数：y = 2x + 1 加上一些噪声
# 将数据移动到指定设备
x_train = x_train.to(device)
y_train = y_train.to(device)

# 5. 创建模型和优化器
model = SimpleNet().to(device)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

# 6. 训练循环
epochs = 5000

print("\n训练开始...")
for epoch in range(epochs):
    # 前向传播，预测结果
    y_pred = model(x_train)
    
    # 计算预测值和真实值之间的损失
    loss = criterion(y_pred, y_train)
    
    # 反向传播，修改模型参数
    optimizer.zero_grad() # 清除旧的梯度
    loss.backward() # 计算新的梯度 
    optimizer.step() # 更新参数：参数 -= 学习率 * 梯度
    
    if (epoch + 1) % 100 == 0:
        w = model.linear.weight.item()
        b = model.linear.bias.item()
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, w: {w:.2f}, b: {b:.2f}')

# 7. 打印结果
w = model.linear.weight.item()
b = model.linear.bias.item()
print(f'\n训练完成！')
print(f'学习到的函数: y = {w:.2f}x + {b:.2f}')
print(f'实际函数: y = 2.00x + 1.00')

# 8. 测试模型
test_x = torch.tensor([[0.0], [5.0], [10.0]]).to(device)
with torch.no_grad():
    test_y = model(test_x)
    print("\n预测结果：")
    for x, y in zip(test_x, test_y):
        print(f'x = {x.item():.1f}, y = {y.item():.2f}')
```

<font style="color:rgb(62, 62, 62);">通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">python pytorch_5min.py</font>`<font style="color:rgb(62, 62, 62);"> 即可运行：</font>

```python
$ python pytorch_5min.py 
Using mps device
tensor([3., 6., 9.])
tensor([ 2.,  8., 18.])
tensor(28.)
tensor(28.)
torch.Size([3])

训练开始...
Epoch [100/5000], Loss: 0.0988, w: 2.09, b: 0.41
Epoch [200/5000], Loss: 0.0420, w: 2.05, b: 0.64
...
Epoch [5000/5000], Loss: 0.0066, w: 2.00, b: 1.02

训练完成！
学习到的函数: y = 2.00x + 1.02
实际函数: y = 2.00x + 1.00

预测结果：
x = 0.0, y = 1.02
x = 5.0, y = 11.00
x = 10.0, y = 20.98
```

<font style="color:rgb(62, 62, 62);">这个例子中，最特别的是有真正的“训练”过程，“训练”究竟是什么？我们经常听到的“反向传播”、“梯度下降”、“学习率”又是什么？</font>

<font style="color:rgb(62, 62, 62);">鉴于这只是5分钟教程，我们只要记住后面我们所有的机器学习代码都是这样的结构即可。</font>

:::color5
**<font style="color:#601BDE;">2.tensor操作</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">这一部分详见代码，看完代码后才发现，大学时候的《线性代数》课程是多么重要。</font>

<font style="color:rgb(62, 62, 62);">这里最值得注意的是“矩阵相乘”，即“点积”、matmul操作，简写为“@”符号，是后面self-attention机制的核心。</font>

<font style="color:rgb(62, 62, 62);">矩阵乘还经常用作张量形状的变换，如形状为(B, T, embd)的张量和形状为(embd, C)的张量相乘，结果为(B, T, C)的张量 —— 这一点也经常被用到。</font>

<font style="color:rgb(62, 62, 62);">此外，</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">tensor.to(device)</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">可以把tensor数据移动到指定的设备，如GPU。</font>

:::color5
**<font style="color:#601BDE;">3.模型、神经网络的layer</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">我们的模型内部只有一个简单的线性层</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nn.Linear(1, 1)</font>`<font style="color:rgb(62, 62, 62);"> ，它输入输出都是一维张量。(1,1)的线性层实际上内部就是一个线性方程，对于输入任何数字x，它会输出x * w + b，实际上神经网络中的“layer”就是内含了一系列参数、可被训练的单元。通过输出</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nn.Linear</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">可以更清晰的看出实现。</font>

```python
>>> layer = nn.Linear(1, 1)
>>> layer.weight.item(), layer.bias.item()
(0.8262009620666504, 0.9049515724182129)
>>> torch.tensor([[1.0],[2.]])
tensor([[1.],
        [2.]])
>>> layer(_)
tensor([[1.7312],
        [2.5574]], grad_fn=<AddmmBackward0>)
```

<font style="color:rgb(62, 62, 62);">手动计算一下就能发现，实际上layer的输出值，就是输入x * weight + bias的结果。</font>

<font style="color:rgb(62, 62, 62);">其中</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">grad_fn</font>`<font style="color:rgb(62, 62, 62);"> 是pytorch用来反向传播的关键，pytorch记住了这个tensor是怎么计算出来的，在后面的反向传播中被使用，对pytorch用户不可见。</font>

:::color5
**<font style="color:#601BDE;">4.反向传播和梯度下降</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">5分钟的教程只需要我们先硬记住一点，机器学习的“训练”就是这样一个过程：</font>

+ <font style="color:rgb(62, 62, 62);">先“前向传播”，计算出输出（如Linear层输出结果）。</font>
+ <font style="color:rgb(62, 62, 62);">再“反向传播”。</font>
    1. <font style="color:rgb(62, 62, 62);">通过“损失函数”计算出模型的输出和真实数据之间的“损失值”loss（如例子中的MSELoss损失函数）；</font>
    2. <font style="color:rgb(62, 62, 62);">计算“梯度”，利用损失函数对输出层的梯度进行计算，接着向前传播（反向传播）计算前一层的梯度，直到输入层（这一步pytorch能自动处理，不需要我们关心。可以简单理解为，“梯度”就是损失函数对各个参数的导数。核心目的就是为了计算出“</font>**<font style="color:rgb(62, 62, 62);">如何调整w和b的值来减少损失</font>**<font style="color:rgb(62, 62, 62);">”）；</font>
    3. <font style="color:rgb(62, 62, 62);">更新参数，“梯度”是一个向量，把“梯度”乘上我们的“学习率”再加上原来的参数，就是我们新的参数了。如果学习率大，那么每次更新的多，学习率小，每次更新的就少。“梯度下降”，就是我们通过迭代更新参数，以寻找到损失函数最小的过程；</font>

<font style="color:rgb(62, 62, 62);">这中间最复杂的求导、算梯度、更新每一层参数的操作，pytorch都自动完成了（前面看到的</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">grad_fn</font>`<font style="color:rgb(62, 62, 62);"> 就是用于这个过程），我们只需要知道在这个结构下，选择不同的优化器算法、损失函数实现、模型结构即可，剩下的交给pytorch。而“推理”，就只有“前向传播”，计算出输出即可。</font>

# 实现一个真正的Bigram模型
:::color3
<font style="color:rgb(62, 62, 62);">5分钟“精通”完pytorch，接下来我们来实现真正的pytorch版Bigram模型。</font>

:::

:::color5
**<font style="color:#601BDE;">1.pytorch版Bigram模型实现</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">首先，我们把前面的</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">simplebigrammodel.py</font>`<font style="color:rgb(62, 62, 62);"> ，用pytorch的tensor数据结构改造成一个新版本，代码见</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">simplebigrammodel_torch.py</font>`<font style="color:rgb(62, 62, 62);"> [5]，这里不再展开。通过这份代码，能在熟悉算法的基础上，进一步深刻理解</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">tenso</font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">r</font><font style="color:rgb(62, 62, 62);">。</font>`

`<font style="color:rgb(62, 62, 62);">然后，我们基于它进一步实现Bigram模型，后续我们的代码都将基于这个为基础，逐渐改出完整的gpt。</font>``<font style="color:rgb(62, 62, 62);">完整代码如下，也可以看</font>`<font style="color:rgb(62, 62, 62);">babygpt_v1.py[6]。</font>

```python
import torch
import torch.nn as nn
from torch.nn import functional as F
from typing import List
import time
torch.manual_seed(42)
prompts = ["春江", "往事"] # 推理的输入prompts
max_new_token = 100 # 推理生成的最大tokens数量
max_iters = 5000 # 训练的最大迭代次数
eval_iters = 100 # 评估的迭代次数
eval_interval = 200 # 评估的间隔
batch_size = 32 # 每个批次的大小
block_size = 8 # 每个序列的最大长度
learning_rate = 1e-2 # 学习率
n_embed = 32 # 嵌入层的维度
tain_data_ratio = 0.9 # 训练数据占数据集的比例，剩下的是验证数据
device = 'cuda'if torch.cuda.is_available() else'mps'if torch.mps.is_available() else'cpu'
with open('ci.txt', 'r', encoding='utf-8') as f:
    text = f.read()
class Tokenizer:
    def __init__(self, text: str):
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}
    
    def encode(self, s: str) -> List[int]:
        return [self.stoi[c] for c in s]
    
    def decode(self, l: List[int]) -> str:
        return''.join([self.itos[i] for i in l])
    
class BabyGPT(nn.Module):
    def __init__(self, vocab_size: int, n_embd: int):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd) # 嵌入层，把token映射到n_embd维空间
        self.lm_head = nn.Linear(n_embd, vocab_size) # 线性层，把n_embd维空间映射到vocab_size维空间，
    def forward(self, idx, targets=None):
        tok_emb = self.token_embedding_table(idx) # 获得token的嵌入表示 (B,T,n_embd)
        logits = self.lm_head(tok_emb) # 通过线性层，把embedding结果重新映射回vocab_size维空间 (B,T,vocab_size)
        if targets is None: # 推理场景，不需要计算损失值
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C) # 把(B,T,C)的形状转换为(B*T,C)，因为交叉熵损失函数第一个参数只接受二维输入。这个操作并没有丢失信息
            targets = targets.view(B*T) # 把(B,T)的形状转换为(B*T)，因为交叉熵损失函数第二个参数只接受一维输入。这个操作并没有丢失信息
            loss = F.cross_entropy(logits, targets) # 计算交叉熵损失
        return logits, loss
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _ = self(idx) # logits的形状是(B,T,vocab_size)，每一个token都计算了下一个token的概率
            logits = logits[:, -1, :] # 实际上我们只需要最后一个token算出来的值
            probs = F.softmax(logits, dim=-1) # 使用softmax函数算概率分布，这里dim=-1表示对最后一个维度进行softmax
            idx_next = torch.multinomial(probs, num_samples=1) # 根据概率分布随机采样，这里num_samples=1表示采样一个token
            idx = torch.cat((idx, idx_next), dim=1) # 把采样的token拼接到序列后面
        return idx
tokenizer = Tokenizer(text)
vocab_size = tokenizer.vocab_size
raw_data = torch.tensor(tokenizer.encode(text), dtype=torch.long).to(device)
n = int(tain_data_ratio*len(raw_data))
data = {'train': raw_data[:n], 'val': raw_data[n:]}
def get_batch(data, batch_size, block_size):
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y
@torch.no_grad()
def estimate_loss(model, data, batch_size, block_size, eval_iters):
    '''
    计算模型在训练集和验证集上的损失
    '''
    out = {}
    model.eval() # 切换到评估模式
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            x, y = get_batch(data[split], batch_size, block_size)
            _, loss = model(x, y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train() # 切换回训练模式
    return out
model = BabyGPT(vocab_size, n_embed).to(device)
# 训练
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
start_time = time.time()
tokens_processed = 0
for iter in range(max_iters):
    x, y = get_batch(data['train'], batch_size, block_size)
    logits, loss = model(x, y)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()
    tokens_processed += batch_size * block_size
    if iter % eval_interval == 0:
        elapsed = time.time() - start_time
        tokens_per_sec = tokens_processed / elapsed if elapsed > 0else0
        losses = estimate_loss(model, data, batch_size, block_size, eval_iters)
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}, speed: {tokens_per_sec:.2f} tokens/sec")
# 推理
prompt_tokens = torch.stack([torch.tensor(tokenizer.encode(p)).to(device) for p in prompts])
# 生成
result = model.generate(prompt_tokens, max_new_token)
# 解码并打印结果
for tokens in result:
    print(tokenizer.decode(tokens.tolist()))
    print('-'*10)
```

`<font style="color:rgb(64, 64, 64);">在我的mac上通过 </font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">python babygpt_v1.py</font>`<font style="color:rgb(62, 62, 62);"> 运行，大概60k t/s的训练速度，而在4090上这个速度可以达到180k t/s。</font>

```python

$ python babygpt_v1.py 
step 0: train loss 8.9236, val loss 8.9194, speed: 1118.03 tokens/sec
step 200: train loss 5.8334, val loss 5.9927, speed: 50238.47 tokens/sec
step 400: train loss 5.5678, val loss 5.7631, speed: 56604.35 tokens/sec
step 600: train loss 5.4697, val loss 5.7274, speed: 59267.69 tokens/sec
step 800: train loss 5.3885, val loss 5.6038, speed: 60842.13 tokens/sec
step 1000: train loss 5.3467, val loss 5.5955, speed: 61404.86 tokens/sec
...
```

<font style="color:rgb(62, 62, 62);">这份代码也没有难点，实际上就是前面pytorch实现的线性回归模型和我们自己土方法实现的bigram模型的结合体，尤其是训练部分，基本上和前面线性回归是一样的，差别主要在模型上。</font>

:::color5
**<font style="color:#601BDE;">2.embedding层</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">这次我们的模型由一个</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nn.Embedding(vocab_size, n_embd)</font>`<font style="color:rgb(62, 62, 62);"> 层和一个</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nn.Linear(n_embd, vocab_size)</font>`<font style="color:rgb(62, 62, 62);"> 层组成。</font>

<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">nn.Embedding(vocab_size, n_embd)</font><font style="color:rgb(62, 62, 62);"> 可以简单理解成一个映射表，只不过它的key取值为0 ~ vocab_size-1，而它的value是一个n_embd维的参数。简单的理解为，通过embedding操作（嵌入操作），我们把一个离散的token，映射为了一个密集的向量。</font>

<font style="color:rgb(62, 62, 62);">实际上Embedding的实现真的就是一个lookup-table，如下所示：</font>

```python
>>> layer = nn.Embedding(10, 3)
>>> layer.weight.shape
torch.Size([10, 3])
>>> layer(torch.tensor(1))
tensor([0.4534, 1.1587, 1.6280], grad_fn=<EmbeddingBackward0>)
>>> layer.weight[torch.tensor(1)]
tensor([0.4534, 1.1587, 1.6280], grad_fn=<SelectBackward0>)
```

<font style="color:rgb(62, 62, 62);">Embedding内部就是保存了一个</font>`<font style="color:rgb(62, 62, 62);">(</font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">vocab_size, n_embd</font><font style="color:rgb(62, 62, 62);">)</font>`<font style="color:rgb(62, 62, 62);">的张量，“对tensor X执行嵌入操作”和“在weight中取key为X的值”效果是一样的。</font>

<font style="color:rgb(62, 62, 62);">Embedding通常作为各种模型的第一层，因为我们要把离散的“token”，映射为一些连续的“数值”，才可以继续后续的操作。两个token id之间是没有关系的，但两个Embedding的向量可以有距离、关联度等关系。</font>

<font style="color:rgb(62, 62, 62);">由于我们只实现了一个Bigram模型，下一个词只和上一个词有关，而Embedding内部恰好能表示一种A到B的映射关系，所以这里我们的模型主体就是Embedding本身，我们训练的直接就是Embedding内的参数。</font>

# lm_head层
:::color3
<font style="color:rgb(62, 62, 62);">lm_head(Language Model Head)是我们的输出层，几乎所有模型最后一层都是这么一个</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">Linear</font>`<font style="color:rgb(62, 62, 62);"> 层，它的用途是把我们中间各种layer算出来的结果，最终映射到</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">vocab_size</font>`<font style="color:rgb(62, 62, 62);"> 维的向量里去。因为我们最终要算的，就是</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">vocab_size</font>`<font style="color:rgb(62, 62, 62);"> 个词里，每个词出现的概率。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">语言模型的常见流程如下示意图，模型间主要的差异都在中间层上，LLM也不例外：</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1748654837028-f9a1d656-7165-4f8f-98ae-41a1b65f9aba.webp)

# 损失函数、归一函数和采样
:::color5
**<font style="color:#601BDE;">1.损失函数、归一函数和采样</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">在</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">forward</font>`<font style="color:rgb(62, 62, 62);"> 实现中，我们使用交叉熵函数作为损失函数，且为了满足交叉熵函数对于参数的要求，我们把(B, T, C)的张量，变形为(B * T, C)，不需要理解交叉熵函数计算方式，只需知道它得出了两个tensor的差值即可。</font>

<font style="color:rgb(62, 62, 62);">我们使用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">softmax</font>`<font style="color:rgb(62, 62, 62);"> 代替前面的线性归一函数做归一化，也省去了考虑</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">total</font>`<font style="color:rgb(62, 62, 62);"> 值为0的情况，并且用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">torch.multinomial</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">代替</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">random.choices</font>`<font style="color:rgb(62, 62, 62);"> 作为采样函数。</font>

:::color5
**<font style="color:#601BDE;">1.训练</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">训练部分代码和5分钟pytorch教程中的没太多差别，我们用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">AdamW</font>`<font style="color:rgb(62, 62, 62);"> 优化器替换了</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">SGD</font>`<font style="color:rgb(62, 62, 62);"> 优化器，具体原因这里不展开解释，只要知道这就是不一样的调整参数的算法即可。</font>

<font style="color:rgb(62, 62, 62);">并且我们每处理一些数据，就尝试输出当前模型，在训练数据和校验数据上的损失值。以便我们观察模型是否过拟合了训练数据。</font>

<font style="color:rgb(62, 62, 62);">如果数据足够多、耗时足够久的话，我们在这里可以用</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">torch.save</font>`<font style="color:rgb(62, 62, 62);"> 方法把参数保存下来，也就是checkpoint。</font>

# 回顾和Next
:::color3
<font style="color:rgb(62, 62, 62);">令人兴奋，目前为止，我们用131行python代码，实现了一个语言模型，居然能生成看起来像是词的东西，It just works。</font><font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(62, 62, 62);">这个模型目前参数量为</font><font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">Embedding层:6148 (vocab_size) * 32 (n_embd) + Linear层6148 * 32 + 6148 = 399620</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);"> </font><font style="color:rgb(62, 62, 62);">，消耗</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">399620 * 4字节 = 1.52MB</font>`<font style="color:rgb(62, 62, 62);"> 空间，即一个0.0004B的参数，而qwen2.5最小的也是0.5B。</font>

<font style="color:rgb(62, 62, 62);">我们亲眼看到了模型的参数、layer、学习率、正向传播、反向传播、梯度等一堆概念。</font>

<font style="color:rgb(62, 62, 62);">如果对于模型流程和结构没太理解，可以问AI实现各种简单的demo，会发现结构大差不大；如果对于中间各种变量转换没太理解，强烈建议在调试中通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">.shape</font>`<font style="color:rgb(62, 62, 62);"> 观察各种tensor的形状变化、通过</font>`<font style="color:rgb(136, 136, 136);background-color:rgb(245, 245, 245);">.weight</font>`<font style="color:rgb(62, 62, 62);"> 观察各个layer的参数变量，来体会其中的细节。</font>



# <font style="color:rgb(62, 62, 62);">参考材料</font>
<font style="color:rgb(62, 62, 62);">‒karpathy/nanoGPT：https://github.com/karpathy/nanoGPT</font>

<font style="color:rgb(62, 62, 62);">‒simpx/buildyourownllm：https://github.com/simpx/buildyourownllm</font>

<font style="color:rgb(62, 62, 62);">‒《深度学习入门 基于Python的理论与实现》</font>

<font style="color:rgb(62, 62, 62);">[1]https://github.com/karpathy/nanoGPT)</font>

<font style="color:rgb(62, 62, 62);">[2]https://github.com/simpx/buildyourownllm/</font>

<font style="color:rgb(62, 62, 62);">[3]https://github.com/simpx/buildyourownllm/blob/main/simplemodel_with_comments.py</font>

<font style="color:rgb(62, 62, 62);">[4]https://github.com/simpx/buildyourownllm/blob/main/simplebigrammodel_with_comments.py</font>

<font style="color:rgb(62, 62, 62);">[5]https://github.com/simpx/buildyourownllm/blob/main/simplebigrammodel_torch.py</font>

<font style="color:rgb(62, 62, 62);">[6]https://github.com/simpx/buildyourownllm/blob/main/babygpt_v1.py</font>





