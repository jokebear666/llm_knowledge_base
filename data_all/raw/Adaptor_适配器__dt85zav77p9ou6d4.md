# Adaptor 适配器

<!-- source: yuque://zhongxian-iiot9/hlyypb/dt85zav77p9ou6d4 -->

# 基础				
<font style="color:#1f2329;">⼤模型中的Adapter是⼀种</font><font style="color:#de7802;">轻量级的模型微调技术</font><font style="color:#1f2329;">，旨在在⼤规模预训练模型的基础上，</font><font style="color:#de7802;">通过插⼊少量可训练的参数来实现特定任务的微调</font><font style="color:#1f2329;">，⽽⽆需重新训练整个模型。Adapter⽅法有效 地降低了微调⼤模型的计算和存储成本，同时保留了预训练模型的能⼒和知识。</font>

## 背景&原理
![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733993181985-13e52234-59e3-4c5a-adb7-38a009a33848.png)

## 1.2 优缺点
+ 优点
    - **参数效率高**：Adapter只微调少量新引⼊的参数，避免了对整个⼤模型的微调。⽐如，BERT-base有1.1亿   参数，⽽典型的Adapter模块可能只有⼏百万参数，微调时显著减少了需要调整的参数量。
    - **任务间参数共享**：adapter使得不同任务的参数模 块可以独⽴微调，但基础的预 训练模型参数仍然保持共享。这种⽅法允许多个任务共享相同的⼤模型，只需存储各个任务的Adapter参数。
    - **训练稳定**：由于Adapter只更新⼩部分参 数，相⽐全参数微调，训练过程更为稳定，并且对较⼩的数据集也更加友好，避免了过拟合
+ **缺点**：
    - <font style="color:rgb(51, 51, 51);">需要额外设计适配器的结构。</font>
    - <font style="color:rgb(51, 51, 51);">适配器的插入可能改变模型的原始表现。</font>

# <font style="color:#1f2329;">HoulsbyAdapter：</font>
<font style="color:#1f2329;">HoulsbyAdapter的实现⽅式是在Transformer的每⼀层的⾃注意⼒块和前馈⽹络之间插⼊⼀个Adapter模块。这种设计没有直接修改原始权重矩阵，⽽是</font><font style="color:#d83931;">通过增加新的可训练层来实现微调</font><font style="color:#1f2329;">。</font>

<font style="color:#1f2329;">具体结构如下：</font>

+ <font style="color:#1456f0;"> </font><font style="color:#1f2329;">Adapter模块结构：通常包括⼀个降维层、⾮线性激活函数（如ReLU或GELU）和⼀个升维层。</font>
+ <font style="color:#1f2329;">数据流过程：对于给定的输⼊ h ，经过⾃注意⼒和前馈⽹络后，再通过Adapter模块进⾏额外的特征变换。整个过程可以表⽰为：hout=Adapter(h)+h</font>

<font style="color:#1f2329;">目这种⽅法的特点是，Adapter模块不与原始权重矩阵直接交互，⽽是作为独⽴的层插⼊，并在 前向过程中通过残差连接与原始⽹络输出融合。</font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">HoulsbyAdapter通过引入专家模型的方式，使模型在特定任务上进行专精处理。每组HoulsbyAdapter由一个 gating网络和多个专家网络组成，能够动态地将输入分配给不同的专家网络进行处理。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **初始化模型**：
    - <font style="color:rgb(51, 51, 51);">加载预训练的LLM。</font>
2. **插入 gating网络和专家网络**：
    - <font style="color:rgb(51, 51, 51);">在选定的层中，插入 gating网络和一组专家网络。</font>
3. **前向传播**：
    - <font style="color:rgb(51, 51, 51);">使用 gating网络计算专家的权重。</font>
    - <font style="color:rgb(51, 51, 51);">根据 gating权重，结合各专家的输出，得到最终的特征。</font>
4. **微调训练**：
    - <font style="color:rgb(51, 51, 51);">优化 gating网络和专家网络的参数，保持模型其他部分不变。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">专家专精：通过专家网络实现更精细的任务处理。</font>
    - <font style="color:rgb(51, 51, 51);">动态分配： gating机制能够根据输入动态分配专家。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">参数复杂： gating和专家网络增加了模型的参数数量。</font>
    - <font style="color:rgb(51, 51, 51);">训练难度大：需要设计和优化高质量的 gating和专家网络。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">多任务学习</font>
+ <font style="color:rgb(51, 51, 51);">领域适应</font>
+ <font style="color:rgb(51, 51, 51);">问答系统</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">参数共享：在专家网络之间共享部分参数，减少参数冗余。</font>
+ <font style="color:rgb(51, 51, 51);">简化 gating：使用更简单的 gating函数减少计算复杂度。</font>
+ <font style="color:rgb(51, 51, 51);">动态专家调整：根据任务需求动态增加或减少专家数量。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForMaskedLM, AutoTokenizer

class Expert(nn.Module):
    def __init__(self, dim, hidden_dim):
        super(Expert, self).__init__()
        self.fc = nn.Linear(dim, hidden_dim)
        self.relu = nn.ReLU()
        self.out = nn.Linear(hidden_dim, dim)
    
    def forward(self, x):
        x = self.relu(self.fc(x))
        x = self.out(x)
        return x

class _gate(nn.Module):
    def __init__(self, dim, num_experts):
        super(_gate, self).__init__()
        self.fc = nn.Linear(dim, num_experts)
    
    def forward(self, x):
        return F.softmax(self.fc(x), dim=-1)

class HoulsbyAdapter(nn.Module):
    def __init__(self, dim, hidden_dim, num_experts=4):
        super(HoulsbyAdapter, self).__init__()
        self.experts = nn.ModuleList([
            Expert(dim, hidden_dim) for _ in range(num_experts)
        ])
        self.gate = _gate(dim, num_experts)
    
    def forward(self, x):
        gate_weights = self.gate(x)
        expert_outputs = [expert(x) * gate_weights[:, i].unsqueeze(-1) for i, expert in enumerate(self.experts)]
        output = sum(expert_outputs)
        return output

class ModelWithHoulsbyAdapter(nn.Module):
    def __init__(self, base_model, adapter):
        super(ModelWithHoulsbyAdapter, self).__init__()
        self.base_model = base_model
        self.adapter = adapter

    def forward(self, input_ids):
        hidden_states = self.base_model(input_ids).last_hidden_state
        adapted_states = self.adapter(hidden_states)
        return adapted_states

# 示例用法
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-base')
base_model = AutoModelForMaskedLM.from_pretrained('facebook/bart-base')

adapter = HoulsbyAdapter(base_model.config.d_model, base_model.config.d_model // 2, num_experts=4)
adapter_model = ModelWithHoulsbyAdapter(base_model, adapter)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(adapter_model.parameters(), lr=1e-3)

# 准备数据
texts = [...]  # 加载文本数据
labels = [...]  # 加载对应标签

train_dataset = Dataset(texts, labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 微调过程
for epoch in range(num_epochs):
    adapter_model.train()
    for batch, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = adapter_model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

# 评估
adapter_model.eval()
correct = 0
total = 0
with torch.no_grad():
    for x, y in val_loader:
        outputs = adapter_model(x)
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == y).sum().item()
        total += y.size(0)
print(f"Validation Accuracy: {correct / total:.3f}")

```





# <font style="color:#1f2329;">ParallelAdapter：</font>
<font style="color:#1f2329;">ParallelAdapter与HoulsbyAdapter不同，它与Transformer的层是平⾏的⼯作⽅式。它的输出与原始Transformer层的输出进⾏融合，有点类似于残差⽹络。具体来说：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">特征融合：</font><font style="color:#1f2329;">Parallel</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">不会直接修改</font><font style="color:#1f2329;">Transformer</font><font style="color:#1f2329;">的层输出</font><font style="color:#1f2329;">，⽽是将</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">模块的输出与</font><font style="color:#1f2329;">Transformer</font><font style="color:#1f2329;">层输出相加或进⾏其他融合操作。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">结构差异：不同于直接插⼊的HoulsbyAdapter，ParallelAdapter像是并⾏执⾏的⼦⽹络，其输出与Transformer的层输出同时存在，然后通过融合策略（如加权平均）得到最终输出。</font>

<font style="color:#1f2329;">这种⽅法依然没有对原始的权重矩阵进⾏低秩分解或直接修改，⽽是通过增加并⾏的结构来辅助特征学习。</font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ParallelAdapter通过并行引入多组适配器，提升模型的表示能力。这种方法允许在多个层或不同的模块中同时引入适配器，通过并行计算加速训练过程。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **初始化模型**：
    - <font style="color:rgb(51, 51, 51);">加载预训练的LLM。</font>
2. **并行插入适配器**：
    - <font style="color:rgb(51, 51, 51);">在多个层或模块中插入适配器，形成并行的处理流程。</font>
3. **并行前向传播**：
    - <font style="color:rgb(51, 51, 51);">在前向传播过程中，同时处理多个适配器的输出，进行特征的融合。</font>
4. **并行微调训练**：
    - <font style="color:rgb(51, 51, 51);">同时优化所有适配器的参数，加速训练过程。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">并行加速：通过并行计算提升训练效率。</font>
    - <font style="color:rgb(51, 51, 51);">参数灵活：允许在不同层引入适配器，提升模型整体适应能力。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">并行复杂：需要设计和实现并行的计算流程。</font>
    - <font style="color:rgb(51, 51, 51);">参数量增加：并行引入适配器会显著增加模型的参数数量。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">并行计算加速</font>
+ <font style="color:rgb(51, 51, 51);">多层次特征增强</font>
+ <font style="color:rgb(51, 51, 51);">复杂任务处理</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">分块并行：将适配器分块处理，降低并行实现的复杂度。</font>
+ <font style="color:rgb(51, 51, 51);">参数共享：在并行适配器之间共享部分参数，减少参数冗余。</font>
+ <font style="color:rgb(51, 51, 51);">动态并行调整：根据任务需求动态调整并行适配器的数量和计算流程。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForMaskedLM, AutoTokenizer

class ParallelAdapter(nn.Module):
    def __init__(self, dim, num_parallel=2):
        super(ParallelAdapter, self).__init__()
        self.adapters = nn.ModuleList([
            nn.Linear(dim, dim//num_parallel) for _ in range(num_parallel)
        ])
    
    def forward(self, x):
        outputs = [adapter(x) for adapter in self.adapters]
        return torch.cat(outputs, dim=-1)

class ModelWithParallelAdapter(nn.Module):
    def __init__(self, base_model, adapter):
        super(ModelWithParallelAdapter, self).__init__()
        self.base_model = base_model
        self.adapter = adapter

    def forward(self, input_ids):
        hidden_states = self.base_model(input_ids).last_hidden_state
        adapted_states = self.adapter(hidden_states)
        return adapted_states

# 示例用法
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-base')
base_model = AutoModelForMaskedLM.from_pretrained('facebook/bart-base')

adapter = ParallelAdapter(base_model.config.d_model, num_parallel=2)
adapter_model = ModelWithParallelAdapter(base_model, adapter)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(adapter_model.parameters(), lr=1e-3)

# 准备数据
texts = [...]  # 加载文本数据
labels = [...]  # 加载对应标签

train_dataset = Dataset(texts, labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 并行训练过程
for epoch in range(num_epochs):
    adapter_model.train()
    for batch, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = adapter_model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

# 评估阶段
adapter_model.eval()
correct = 0
total = 0
with torch.no_grad():
    for x, y in val_loader:
        outputs = adapter_model(x)
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == y).sum().item()
        total += y.size(0)
print(f"Validation Accuracy: {correct / total:.3f}")

```



# <font style="color:#1f2329;">Compacter：</font>
<font style="color:#1f2329;">Compacter</font><font style="color:#1f2329;">是</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">⽅法的⼀种优化变体</font><font style="color:#1f2329;">，它通过低秩分解技术减少了</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">模块的参数量。具</font><font style="color:#1f2329;"> 体⽽⾔</font><font style="color:#1f2329;">，它通过将</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">模块的权重矩阵表⽰为⼏个低秩矩阵的乘</font><font style="color:#1f2329;">积来实现参数压缩：</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">低秩分解：类似于</font><font style="color:#1f2329;">LoRA</font><font style="color:#1f2329;">的思想</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">Compacter</font><font style="color:#1f2329;">对</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">模块内部的权重矩阵进⾏低秩分解</font><font style="color:#1f2329;">，即将⼀ </font><font style="color:#1f2329;">个⼤的矩阵拆分为两个或多个⼩的矩阵</font><font style="color:#1f2329;">，这样可以减少训练参数量。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">参数更新⽅式：虽然使⽤了低秩分解，但它仅限于Adapter模块内部的权重更新，并不会直接去修改Transformer原始的权重矩阵。也就是说，Compacter对原有的⼤模型参数是保持冻结的，只对插⼊的低秩结构进⾏训练。</font>

<font style="color:#1f2329;"></font>

# LoRA (Low-RankAdaptation)：
<font style="color:#1f2329;">与Adapter类似的思想，但LoRA通过在注意⼒权重矩阵上进⾏低 秩近似来减少训练参数。LoRA也是⼀种插⼊性微调技术，主要在Transformer的⾃注意⼒模块中插⼊低秩矩阵更新。</font>

**应用场景**

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">LoRA通过低秩分解的方式，在不显著增加参数量的前提下，提升模型的适应能力。具体来说，LoRA为模型中的某些线性层（如全连接层、自注意力层）引入低秩的适配器矩阵，这些矩阵能够以较小的参数量捕捉到任务相关的特征。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **初始化模型**：
    - <font style="color:rgb(51, 51, 51);">加载预训练的LLM。</font>
2. **插入适配器矩阵**：
    - <font style="color:rgb(51, 51, 51);">在选定的层（如注意力查询、键、值投影层）中，插入一对低秩的适配器矩阵。</font>
3. **前向传播**：
    - <font style="color:rgb(51, 51, 51);">在前向传播过程中，通过适配器矩阵调整输入特征。</font>
4. **微调训练**：
    - <font style="color:rgb(51, 51, 51);">只优化适配器矩阵的参数，保持模型其他参数不变。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">参数高效：低秩矩阵显著减少了参数数量。</font>
    - <font style="color:rgb(51, 51, 51);">适合小样本数据：适用于数据量有限的微调任务。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">适应能力有限：低秩矩阵可能无法充分捕捉复杂的任务特征。</font>
    - <font style="color:rgb(51, 51, 51);">层次选择敏感：需要选择合适的层进行适配器的插入。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">⾃然语⾔处理（</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">NLP</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;"> </font><font style="color:#1f2329;">：</font><font style="color:#1f2329;">任务包括情感分析、命名</font><font style="color:#1f2329;">实体识别、机器翻译等。</font>

<font style="color:#1456f0;">•</font><font style="color:#1456f0;">  </font><font style="color:#1f2329;">跨语⾔模型微调：</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">被证明可以适应多语⾔环境中的任</font><font style="color:#1f2329;">务</font><font style="color:#1f2329;">，在不同语⾔之间共享⼤模型</font><font style="color:#1f2329;">，微</font><font style="color:#1f2329;">调不同语⾔任务的</font><font style="color:#1f2329;">Adapter</font><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">•  </font><font style="color:#1f2329;">多任务学习：Adapter能够有效实现同⼀个⼤模型在多个任务之间的共享，避免了每个任务都需要 单独训练⼀个完整的模型。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">增加秩值：通过提高秩值来增强适配器的表达能力。</font>
+ <font style="color:rgb(51, 51, 51);">多层次适配器：在多个层次插入适配器矩阵，提升模型整体适应能力。</font>
+ <font style="color:rgb(51, 51, 51);">结合其他技术：与其他适配器方法（如HoulsbyAdapter）结合，综合利用不同优势。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import AutoModelForMaskedLM, AutoTokenizer

class LoRAAdapter(nn.Module):
    def __init__(self, dim, rank=8):
        super(LoRAAdapter, self).__init__()
        self.W_a = nn.Parameter(torch.randn(dim, rank))
        self.W_b = nn.Parameter(torch.randn(rank, dim))
    
    def forward(self, x):
        return F.relu(torch.mm(x, self.W_a)) @ self.W_b

class LLaMAWithLoRA(nn.Module):
    def __init__(self, base_model, adapter_config):
        super(LLaMAWithLoRA, self).__init__()
        self.base_model = base_model
        self.adapter = LoRAAdapter(adapter_config['dim'], rank=adapter_config['rank'])
    
    def forward(self, input_ids):
        hidden_states = self.base_model(input_ids).last_hidden_state
        adapted_states = self.adapter(hidden_states)
        return adapted_states

# 示例用法
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-base')
base_model = AutoModelForMaskedLM.from_pretrained('facebook/bart-base')

adapter_config = {
    'dim': base_model.config.d_model,
    'rank': 8
}

adapter_base = LLaMAWithLoRA(base_model, adapter_config)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(adapter_base.parameters(), lr=1e-3)

# 准备数据
texts = [...]  # 加载文本数据
labels = [...]  # 加载对应标签

train_dataset = Dataset(texts, labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 训练过程
for epoch in range(num_epochs):
    adapter_base.train()
    for batch, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = adapter_base(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

# 评估模型
adapter_base.eval()
correct = 0
total = 0
with torch.no_grad():
    for x, y in val_loader:
        outputs = adapter_base(x)
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == y).sum().item()
        total += y.size(0)
print(f"Validation Accuracy: {correct / total:.3f}")

```





