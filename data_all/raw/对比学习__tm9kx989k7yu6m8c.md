# 对比学习

<!-- source: yuque://zhongxian-iiot9/hlyypb/tm9kx989k7yu6m8c -->

# 对比学习
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">对比学习是一种</font>**<font style="color:rgb(51, 51, 51);">自监督学习</font>**<font style="color:rgb(51, 51, 51);">方法，通过构建正样本对（similar pairs）和负样本对（dissimilar pairs），让模型学习到数据的内在特征表示。核心目标是：</font>

+ **<font style="color:rgb(51, 51, 51);">拉近正样本</font>**<font style="color:rgb(51, 51, 51);">（anchor与positive）在特征空间中的距离。</font>
+ **<font style="color:rgb(51, 51, 51);">推开负样本</font>**<font style="color:rgb(51, 51, 51);">（anchor与negative）在特征空间中的距离。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：生成正样本对（如对同一图像做裁剪、旋转等变换）。</font>
+ **<font style="color:rgb(51, 51, 51);">编码器（Encoder）</font>**<font style="color:rgb(51, 51, 51);">：将输入映射到低维特征空间。</font>
+ **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：衡量正负样本对的相似度差异（如InfoNCE）。</font>



# 文本对比学习(SimCSE为例)
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">文本对比学习通过自监督方式学习语义表示，SimCSE的成功验证了简单而有效的设计理念。其核心价值在于：</font>

1. <font style="color:rgb(51, 51, 51);">突破标注数据限制</font>
2. <font style="color:rgb(51, 51, 51);">获得高质量文本表示</font>
3. <font style="color:rgb(51, 51, 51);">增强模型语义理解能力</font>

<font style="color:rgb(51, 51, 51);">未来发展趋势可能包括：</font>

+ <font style="color:rgb(51, 51, 51);">多语言对比学习</font>
+ <font style="color:rgb(51, 51, 51);">跨模态对比迁移</font>
+ <font style="color:rgb(51, 51, 51);">动态温度系数调整</font>
+ <font style="color:rgb(51, 51, 51);">基于知识增强的对比学习</font>

:::

:::color5
**<font style="color:#601BDE;">1.SimCSE原理</font>**

:::

通过构造相似样本对，使同类文本在表示空间中更接近，不同类更远。

1. **<font style="color:rgb(51, 51, 51);">SimCSE架构</font>**
    1. **<font style="color:rgb(51, 51, 51);">单编码器结构</font>**<font style="color:rgb(51, 51, 51);">：BERT/RoBERTa等Transformer模型</font>
    2. **<font style="color:rgb(51, 51, 51);">对比策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">无监督：同一句子两次前向传播（不同dropout mask）</font>
        * <font style="color:rgb(51, 51, 51);">有监督：NLI数据集构造三元组</font>
    3. **<font style="color:rgb(51, 51, 51);">池化层</font>**<font style="color:rgb(51, 51, 51);">：采用[CLS]表征或平均池化</font>
2. **SimCSE的核心创新在于：**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740734593819-e291dd3e-11ae-4d23-869a-ecf95ab51b01.png)

<font style="color:rgb(51, 51, 51);">其中：</font>

+ <font style="color:rgb(51, 51, 51);">h</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">+</font></sup><font style="color:rgb(51, 51, 51);">：通过dropout构造的正样本</font>
+ <font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：温度系数（通常取0.05）</font>

:::color5
<font style="color:#601BDE;">2.训练步骤</font>

:::

**<font style="color:rgb(51, 51, 51);">1. 数据构造</font>**

+ **无监督模式**：

```python
# 同一批次两次前向
embeddings1 = model(input_ids, attention_mask)
embeddings2 = model(input_ids, attention_mask)  # 不同dropout
```

+ **有监督模式**：

```python
# NLI数据集构建三元组
(premise, entailment, contradiction)
```

**<font style="color:rgb(51, 51, 51);">2. 特征提取</font>**

```python
class SimCSE(nn.Module):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder  # BERT/RoBERTa等
        self.pooler = lambda x: x.last_hidden_state[:,0]  # [CLS]池化

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids, attention_mask)
        return self.pooler(outputs)
```

**<font style="color:rgb(51, 51, 51);">3. 对比损失计算</font>**

```python
def contrastive_loss(embeddings, temperature=0.05):
    # embeddings: [batch_size, hidden_dim]
    batch_size = embeddings.size(0)

    # 余弦相似度矩阵
    sim_matrix = torch.cosine_similarity(
        embeddings.unsqueeze(1), 
        embeddings.unsqueeze(0), 
        dim=-1
    )  # [batch_size, batch_size]

    # 构造标签（对角线为正样本）
    labels = torch.arange(batch_size).to(embeddings.device)

    # 计算交叉熵损失
    loss = F.cross_entropy(
        sim_matrix / temperature, 
        labels
    )
    return loss
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点：</font>**

1. <font style="color:rgb(51, 51, 51);">简单有效：仅需标准Transformer结构</font>
2. <font style="color:rgb(51, 51, 51);">数据高效：无监督版本仅需普通文本</font>
3. <font style="color:rgb(51, 51, 51);">通用性强：适用多种文本任务</font>
4. <font style="color:rgb(51, 51, 51);">各向同性：缓解BERT的anisotropy问题</font>

**<font style="color:rgb(51, 51, 51);">缺点：</font>**

1. <font style="color:rgb(51, 51, 51);">对batch size敏感（需大batch）</font>
2. <font style="color:rgb(51, 51, 51);">随机dropout可能破坏语义</font>
3. <font style="color:rgb(51, 51, 51);">难以处理细粒度相似度</font>
4. <font style="color:rgb(51, 51, 51);">长文本编码效果下降</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

| **应用领域** | **典型任务** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">语义检索</font> | <font style="color:rgb(51, 51, 51);">问答系统/搜索引擎</font> |
| <font style="color:rgb(51, 51, 51);">文本聚类</font> | <font style="color:rgb(51, 51, 51);">新闻分类/用户画像</font> |
| <font style="color:rgb(51, 51, 51);">文本匹配</font> | <font style="color:rgb(51, 51, 51);">复述检测/自然语言推理</font> |
| <font style="color:rgb(51, 51, 51);">数据增强</font> | <font style="color:rgb(51, 51, 51);">文本生成/去噪</font> |
| <font style="color:rgb(51, 51, 51);">迁移学习</font> | <font style="color:rgb(51, 51, 51);">下游任务微调</font> |


:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **数据增强优化**：
    - <font style="color:rgb(51, 51, 51);">ESimCSE：词重复+删除增强</font>
    - <font style="color:rgb(51, 51, 51);">PromptBERT：基于模板的构造方法</font>
2. **负样本增强**：
    - <font style="color:rgb(51, 51, 51);">ConSERT：跨模型负样本</font>
    - <font style="color:rgb(51, 51, 51);">DiffCSE：基于差异的对比学习</font>
3. **损失函数改进**：
    - <font style="color:rgb(51, 51, 51);">Margin loss：引入边界控制</font>
    - <font style="color:rgb(51, 51, 51);">Triplet loss：显式构建三元组</font>
4. **架构改进**：
    - <font style="color:rgb(51, 51, 51);">SBERT：孪生网络结构</font>
    - <font style="color:rgb(51, 51, 51);">COIL：token级对比学习</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
# 典型训练配置
batch_size = 64       # 建议>=64
learning_rate = 3e-5  # BERT类模型常用
max_length = 32       # 短文本效果更好
temperature = 0.05    # 温度系数
epochs = 3            # 通常3-10轮

import torch
from transformers import AutoModel, AutoTokenizer

class SimCSE:
    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def encode(self, texts, batch_size=32):
        # 文本向量化
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            inputs = self.tokenizer(
                batch, 
                padding=True, 
                truncation=True, 
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                emb = outputs.last_hidden_state[:,0]  # [CLS] pooling
                embeddings.append(emb.cpu())
                
        return torch.cat(embeddings, dim=0)

# 训练示例
model = SimCSE()
optimizer = torch.optim.AdamW(model.model.parameters(), lr=5e-5)

for batch in dataloader:
    # 两次前向获得正样本对
    emb1 = model.model(**batch) 
    emb2 = model.model(**batch)  # 不同dropout
    
    # 计算对比损失
    loss = contrastive_loss(torch.cat([emb1, emb2]))
    
    loss.backward()
    optimizer.step()

```

#### 
<font style="color:rgb(51, 51, 51);"></font>

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">图文对比学习(CLIP为例)</font><font style="color:#D22D8D;">（by草莓师姐）</font>
<font style="color:rgb(51, 51, 51);">以CLIP模型为例，从原理到代码实现系统解析多模态对比学习</font>

:::color3
**<font style="color:rgb(51, 51, 51);">核心思想：</font>**

<font style="color:rgb(51, 51, 51);">通过对比学习将不同模态（如图像-文本）映射到同一潜在空间，使匹配的样本对距离更近，不匹配的更远。CLIP的核心公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735486640-ffd361d0-724d-4b70-bb6f-25f479fe15cf.png)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735548727-251dbecf-fe08-4e85-a1ce-6509358d36bf.png)

:::color5
**<font style="color:#601BDE;">1.CLIP架构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">双编码器结构</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像编码器（ViT/ResNet）</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器（Transformer）</font>
2. **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：将不同模态的特征映射到同一空间</font>
3. **<font style="color:rgb(51, 51, 51);">对比目标</font>**<font style="color:rgb(51, 51, 51);">：最大化正样本对的相似度，最小化负样本对</font>

:::color5
**<font style="color:#601BDE;">2.训练步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据预处理</font>**
    - <font style="color:rgb(51, 51, 51);">图像：Resize到224x224，随机裁剪/翻转</font>
    - <font style="color:rgb(51, 51, 51);">文本：截断/填充到固定长度（CLIP使用76 tokens）</font>
2. **<font style="color:rgb(51, 51, 51);">特征提取</font>**

```python
# 伪代码示例
image_features = image_encoder(image_batch)  # [batch_size, emb_dim]
text_features = text_encoder(text_batch)     # [batch_size, emb_dim]
```

3. **<font style="color:rgb(51, 51, 51);">相似度矩阵计算</font>**

```python
# 归一化
image_emb = image_features / image_features.norm(dim=-1, keepdim=True)
text_emb = text_features / text_features.norm(dim=-1, keepdim=True)

# 计算相似度矩阵
logit_scale = nn.Parameter(torch.ones([]) * np.log(1/0.07))
logits_per_image = logit_scale * image_emb @ text_emb.t()  # [N, N]
logits_per_text = logits_per_image.t()                     # [N, N]
```

4. **<font style="color:rgb(51, 51, 51);">对比损失计算</font>**

<font style="color:rgb(51, 51, 51);">使用对称交叉熵损失：</font>

```python
labels = torch.arange(batch_size)  # 对角矩阵表示正样本对

loss_i = F.cross_entropy(logits_per_image, labels)
loss_t = F.cross_entropy(logits_per_text, labels)
total_loss = (loss_i + loss_t)/2
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点：</font>**

1. <font style="color:rgb(51, 51, 51);">零样本推理能力</font>
2. <font style="color:rgb(51, 51, 51);">跨模态检索高效</font>
3. <font style="color:rgb(51, 51, 51);">对噪声数据鲁棒性强</font>
4. <font style="color:rgb(51, 51, 51);">无需手工标注（利用自然监督信号）</font>

**<font style="color:rgb(51, 51, 51);">缺点：</font>**

1. <font style="color:rgb(51, 51, 51);">需要超大规模数据（CLIP训练用了4亿对）</font>
2. <font style="color:rgb(51, 51, 51);">模态间细粒度对齐困难</font>
3. <font style="color:rgb(51, 51, 51);">计算成本极高（CLIP训练需592 V100 days）</font>
4. <font style="color:rgb(51, 51, 51);">文本描述歧义性问题</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

| **场景** | **典型应用** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">零样本分类</font> | <font style="color:rgb(51, 51, 51);">ImageNet分类无需训练</font> |
| <font style="color:rgb(51, 51, 51);">跨模态检索</font> | <font style="color:rgb(51, 51, 51);">图文互搜（如Google Images）</font> |
| <font style="color:rgb(51, 51, 51);">生成模型引导</font> | <font style="color:rgb(51, 51, 51);">DALL-E、Stable Diffusion的文本条件生成</font> |
| <font style="color:rgb(51, 51, 51);">视频理解</font> | <font style="color:rgb(51, 51, 51);">视频-文本对齐（如VideoCLIP）</font> |
| <font style="color:rgb(51, 51, 51);">多模态推理</font> | <font style="color:rgb(51, 51, 51);">Visual Question Answering</font> |


:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **训练效率优化**：
    - <font style="color:rgb(51, 51, 51);">FLIP（随机mask图像块加速训练）</font>
    - <font style="color:rgb(51, 51, 51);">DeCLIP（数据增强+动量蒸馏）</font>
2. **对齐增强**：
    - <font style="color:rgb(51, 51, 51);">ALIGN：使用噪声更大的网页数据</font>
    - <font style="color:rgb(51, 51, 51);">FILIP：细粒度token级对比</font>
3. **架构改进**：
    - <font style="color:rgb(51, 51, 51);">BLIP：引入跨模态注意力</font>
    - <font style="color:rgb(51, 51, 51);">FLAVA：统一多模态编码器</font>
4. **损失函数改进**：
    - <font style="color:rgb(51, 51, 51);">CoOp：可学习的prompt模板</font>
    - <font style="color:rgb(51, 51, 51);">SLIP：结合自监督学习损失</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
# 典型CLIP训练配置
batch_size = 32768    # 需超大显存
learning_rate = 5e-5  # 使用学习率warmup
epochs = 32           # 实际需要更多epoch
temperature = 0.07    # logit缩放因子

import torch
import torch.nn as nn

class CLIP(nn.Module):
    def __init__(self, image_encoder, text_encoder, emb_dim=512):
        super().__init__()
        self.image_encoder = image_encoder
        self.text_encoder = text_encoder
        self.image_proj = nn.Linear(2048, emb_dim)  # ResNet50为例
        self.text_proj = nn.Linear(512, emb_dim)    # Transformer为例
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1/0.07))

    def forward(self, images, texts):
        # 特征提取
        image_feats = self.image_encoder(images)  # [bs, 2048]
        text_feats = self.text_encoder(texts)     # [bs, 512]
        
        # 投影到共同空间
        image_emb = self.image_proj(image_feats)
        text_emb = self.text_proj(text_feats)
        
        # 归一化
        image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)
        text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
        
        # 计算相似度
        logits = self.logit_scale.exp() * image_emb @ text_emb.t()
        return logits

# 训练伪代码
model = CLIP(image_encoder, text_encoder)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for images, texts in dataloader:
    logits = model(images, texts)
    labels = torch.arange(len(images))
    loss = F.cross_entropy(logits, labels) + F.cross_entropy(logits.t(), labels)
    loss.backward()
    optimizer.step()

```

## <font style="color:rgb(51, 51, 51);">InfoNCE</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">InfoNCE是一种基于噪声对比估计的损失函数，用于最大化正样本对的互信息（Mutual Information）。其公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740712765539-f4f8df7c-e753-44e7-af4b-4d48c28958fc.png)

+ _<font style="color:rgb(51, 51, 51);">z</font>_<sub>_<font style="color:rgb(51, 51, 51);">i</font>_</sub><font style="color:rgb(51, 51, 51);">：锚点样本（anchor）的特征。</font>
+ <font style="color:rgb(51, 51, 51);">z</font><sub><font style="color:rgb(51, 51, 51);">j</font></sub><sup><font style="color:rgb(51, 51, 51);">+</font></sup><font style="color:rgb(51, 51, 51);">：正样本的特征。</font>
+ <font style="color:rgb(51, 51, 51);">z</font><sub><font style="color:rgb(51, 51, 51);">k</font></sub><sup><font style="color:rgb(51, 51, 51);">−</font></sup><font style="color:rgb(51, 51, 51);">：负样本的特征。</font>
+ <font style="color:rgb(51, 51, 51);">s(⋅)：相似度函数（如余弦相似度）。</font>
+ <font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：温度系数（控制分布尖锐程度）。</font>
+ <font style="color:rgb(51, 51, 51);">N</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：负样本数量。</font>

:::

<font style="color:rgb(51, 51, 51);">对比学习通过构建正负样本对的对比任务，结合InfoNCE损失函数，已成为自监督学习中的核心方法，并在多个领域展现出强大的特征学习能力。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：一批样本 X={x1,x2,...,xB}。</font>
2. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：对每个样本生成两个增强视图 x</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">a</font></sup><font style="color:rgb(51, 51, 51);">,x</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">b</font></sup><font style="color:rgb(51, 51, 51);">。</font>
3. **<font style="color:rgb(51, 51, 51);">特征提取</font>**<font style="color:rgb(51, 51, 51);">：通过编码器得到特征</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740712844605-72ef504c-26c5-4149-8376-97cf871aae00.png)<font style="color:rgb(51, 51, 51);">。</font>
4. **<font style="color:rgb(51, 51, 51);">相似度计算</font>**<font style="color:rgb(51, 51, 51);">：对每个锚点特征</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">a</font>_<font style="color:rgb(51, 51, 51);">z</font>__<font style="color:rgb(51, 51, 51);">i</font>__<font style="color:rgb(51, 51, 51);">a</font>_<font style="color:rgb(51, 51, 51);">，计算：</font>
    - <font style="color:rgb(51, 51, 51);">正样本相似度：s(z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">a</font></sup><font style="color:rgb(51, 51, 51);">,z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">b</font></sup><font style="color:rgb(51, 51, 51);">)</font>
    - <font style="color:rgb(51, 51, 51);">负样本相似度：s(z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">a</font></sup><font style="color:rgb(51, 51, 51);">,z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">b</font></sup><font style="color:rgb(51, 51, 51);">), j≠i</font>
5. **<font style="color:rgb(51, 51, 51);">损失计算</font>**<font style="color:rgb(51, 51, 51);">：应用InfoNCE公式，对所有样本求平均损失。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">无需标签数据</font>**<font style="color:rgb(51, 51, 51);">：完全自监督学习。</font>
+ **<font style="color:rgb(51, 51, 51);">特征解耦性好</font>**<font style="color:rgb(51, 51, 51);">：学习到对下游任务泛化的特征。</font>
+ **<font style="color:rgb(51, 51, 51);">灵活性高</font>**<font style="color:rgb(51, 51, 51);">：适用于图像、文本、语音等多模态数据。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">：负样本数量直接影响计算量。</font>
+ **<font style="color:rgb(51, 51, 51);">对数据增强敏感</font>**<font style="color:rgb(51, 51, 51);">：依赖高质量的数据增强策略。</font>
+ **<font style="color:rgb(51, 51, 51);">样本选择偏差</font>**<font style="color:rgb(51, 51, 51);">：负样本可能包含潜在正样本（False Negative）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

| **领域** | **应用案例** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">计算机视觉</font>** | <font style="color:rgb(51, 51, 51);">图像分类、目标检测（如SimCLR、MoCo）</font> |
| **<font style="color:rgb(51, 51, 51);">自然语言处理</font>** | <font style="color:rgb(51, 51, 51);">文本相似度计算、句子嵌入（如SimCSE）</font> |
| **<font style="color:rgb(51, 51, 51);">语音处理</font>** | <font style="color:rgb(51, 51, 51);">说话人识别、语音表示学习</font> |
| **<font style="color:rgb(51, 51, 51);">跨模态学习</font>** | <font style="color:rgb(51, 51, 51);">图文匹配（如CLIP）</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">负样本优化</font>**
    - **<font style="color:rgb(51, 51, 51);">动量对比（MoCo）</font>**<font style="color:rgb(51, 51, 51);">：维护动态队列存储历史负样本。</font>
    - **<font style="color:rgb(51, 51, 51);">难负样本挖掘</font>**<font style="color:rgb(51, 51, 51);">：筛选与锚点相似度高的负样本。</font>
2. **<font style="color:rgb(51, 51, 51);">损失函数改进</font>**
    - **<font style="color:rgb(51, 51, 51);">NT-Xent（Normalized Temperature-scaled Cross Entropy）</font>**<font style="color:rgb(51, 51, 51);">：引入归一化和温度参数（SimCLR）。</font>
    - **<font style="color:rgb(51, 51, 51);">Triplet Loss</font>**<font style="color:rgb(51, 51, 51);">：基于锚点-正样本-负样本的三元组损失。</font>
3. **<font style="color:rgb(51, 51, 51);">架构改进</font>**
    - **<font style="color:rgb(51, 51, 51);">不对称编码器</font>**<font style="color:rgb(51, 51, 51);">：使用不同参数的编码器处理正负样本（如BYOL）。</font>
    - **<font style="color:rgb(51, 51, 51);">投影头（Projection Head）</font>**<font style="color:rgb(51, 51, 51);">：在编码器后增加MLP层映射到子空间。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ContrastiveLoss(nn.Module):
    def __init__(self, temperature=0.5):
        super().__init__()
        self.temperature = temperature

    def forward(self, features):
        # features: [2*N, D]（前N个为锚点，后N个为正样本）
        batch_size = features.shape[0] // 2
        labels = torch.cat([torch.arange(batch_size) for _ in range(2)], dim=0)
        labels = (labels.unsqueeze(0) == labels.unsqueeze(1)).float().to(features.device)
        
        # 计算相似度矩阵
        similarity_matrix = F.cosine_similarity(features.unsqueeze(1), features.unsqueeze(0), dim=-1)
        
        # 排除对角线（自身相似度）
        mask = torch.eye(labels.shape[0], dtype=torch.bool).to(features.device)
        labels = labels[~mask].view(labels.shape[0], -1)
        similarity_matrix = similarity_matrix[~mask].view(similarity_matrix.shape[0], -1)
        
        # 选取正样本和负样本
        positives = similarity_matrix[labels.bool()].view(labels.shape[0], -1)
        negatives = similarity_matrix[~labels.bool()].view(similarity_matrix.shape[0], -1)
        
        # 计算InfoNCE损失
        logits = torch.cat([positives, negatives], dim=1)
        labels = torch.zeros(logits.shape[0], dtype=torch.long).to(features.device)
        logits = logits / self.temperature
        loss = F.cross_entropy(logits, labels)
        return loss

# 使用示例
encoder = nn.Linear(2048, 128)  # 假设输入维度2048，输出维度128
projector = nn.Sequential(nn.Linear(128, 256), nn.ReLU(), nn.Linear(256, 128))

x = torch.randn(64, 2048)  # 输入数据（batch_size=32，每个样本生成两个视图）
features = encoder(x)
features = projector(features)
loss_fn = ContrastiveLoss(temperature=0.5)
loss = loss_fn(features)
print(loss.item())

```

## LLAVA与CLIP对齐的对比
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">CLIP</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐 是其核心能力，通过</font>**<font style="color:#ED740C;">对比学习（Contrastive Learning）</font>**<font style="color:rgb(25, 27, 31);">将图像和文本映射到统一的语义空间。</font>

**<font style="color:rgb(25, 27, 31);">LLaVA</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐的核心是通过一个</font>**<font style="color:#ED740C;">轻量级线性投影层将视觉特征映射到语言模型的词嵌入空间</font>**<font style="color:rgb(25, 27, 31);">，结合两阶段训练策略实现高效对齐。以下是详细的技术分解：</font>

**<font style="color:rgb(51, 51, 51);">参考</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://zhuanlan.zhihu.com/p/27728623876](https://zhuanlan.zhihu.com/p/27728623876)

:::

:::color5
**<font style="color:#601BDE;">1.CLIP多模态对齐</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849995591-667a0c79-beab-443f-931c-f351159cd7c4.png)

1. 模型结构
    - <font style="color:rgb(25, 27, 31);">图像编码器：例如 Vision Transformer（ViT）或 ResNet，将图像编码为特征向量。</font>
    - <font style="color:rgb(25, 27, 31);">文本编码器：例如 Transformer，将文本编码为特征向量。</font>
2. 对齐方法
    - <font style="color:rgb(25, 27, 31);">输入：</font>
        * <font style="color:rgb(25, 27, 31);">图像：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[img_1, img_2, ..., img_N]</font>`
        * <font style="color:rgb(25, 27, 31);">文本：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[text_1, text_2, ..., text_N]</font>`
    - <font style="color:rgb(25, 27, 31);">步骤：</font>
        * **<font style="color:rgb(25, 27, 31);">a.特征提取：</font>**
            + <font style="color:rgb(25, 27, 31);">图像特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">I = image_encoder(img_1), ..., image_encoder(img_N)</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">→ 维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
            + <font style="color:rgb(25, 27, 31);">文本特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">T = text_encoder(text_1), ..., text_encoder(text_N)</font>`<font style="color:rgb(25, 27, 31);"> → 维度 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
        * **<font style="color:rgb(25, 27, 31);">b.相似度计算：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">计算所有图像和文本的余弦相似度矩阵</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S</font>`<font style="color:rgb(25, 27, 31);">，维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, N]</font>`<font style="color:rgb(25, 27, 31);">：</font>

```plain
S[i][j] = cosine_similarity(I[i], T[j])
```

    - <font style="color:rgb(25, 27, 31);">理想情况下，对角线元素 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S[i][i]</font>`<font style="color:rgb(25, 27, 31);"> 应最大（匹配对），非对角线元素应较小（不匹配对）</font>
        * **<font style="color:rgb(25, 27, 31);">c.对比损失（InfoNCE）：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">对每个图像</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">i</font>`<font style="color:rgb(25, 27, 31);">，计算其与所有文本的相似度，通过 softmax 得到概率分布：</font>

```plain
p_image2text(i) = exp(S[i][i]/τ) / sum_{j=1}^N exp(S[i][j]/τ)
```

        * <font style="color:rgb(25, 27, 31);">对每个文本</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">j</font>`<font style="color:rgb(25, 27, 31);">，同理计算</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">p_text2image(j)</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">总损失为两个方向的交叉熵之和：</font>
        * <font style="color:rgb(25, 27, 31);">其中 τ 是温度参数，控制分布集中程度。</font>

```plain
loss = -1/(2N) * sum_{i=1}^N [log(p_image2text(i)) + log(p_text2image(i))]
```

:::color5
**<font style="color:#601BDE;">2.LLAVA多模态对齐</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849977575-d145922b-3207-4c22-a51a-e5519ce67e37.png)

1. **模型架构**
    1. <font style="color:rgb(25, 27, 31);">视觉编码器：CLIP-ViT-L/14（输出维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[H, W, D_img] = [16, 16, 1024]</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    2. <font style="color:rgb(25, 27, 31);">线性投影层（对齐模块）：单层全连接网络（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj ∈ R^{D_img × D_text}</font>`<font style="color:rgb(25, 27, 31);">），将图像特征转换为语言模型兼容的维度（如</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text=4096</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    3. <font style="color:rgb(25, 27, 31);">语言模型：</font>[<font style="color:rgb(9, 64, 142);">Vicuna</font>](https://zhida.zhihu.com/search?content_id=254568449&content_type=Article&match_order=1&q=Vicuna&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（LLaMA架构的指令微调版本），词嵌入维度为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text</font>`<font style="color:rgb(25, 27, 31);">。</font>
2. **对齐步骤**
    1. **<font style="color:rgb(25, 27, 31);">视觉特征处理</font>**
        * <font style="color:rgb(25, 27, 31);">输入图像：尺寸</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">224×224</font>`<font style="color:rgb(25, 27, 31);">，通过ViT划分为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">16×16</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个patch，输出特征图</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[16×16, 1024]</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">特征扁平化：将空间维度合并为序列，得到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×1024</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的特征矩阵。</font>
        * <font style="color:rgb(25, 27, 31);">线性投影：通过 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj</font>`<font style="color:rgb(25, 27, 31);"> 将每个patch特征转换为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">4096</font>`<font style="color:rgb(25, 27, 31);"> 维，得到 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);"> 的视觉token序列。</font>
    2. **<font style="color:rgb(25, 27, 31);">步骤2：与文本token拼接</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">将视觉token（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);">）与文本token（如问题“描述这张图片”）拼接，形成联合输入序列。</font>
        * <font style="color:rgb(25, 27, 31);">示例：输入序列 = [IMG_1, IMG_2, ..., IMG_256] + [Q1, Q2, ..., Qn]</font>
        * <font style="color:rgb(25, 27, 31);">语言模型（Vicuna）将此序列视为“多模态prompt”，自回归生成答案。</font>
    3. **<font style="color:rgb(25, 27, 31);">预训练（特征对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：对齐视觉与语言特征，使投影后的视觉token能被语言模型“理解”。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用约 600K 图像-文本对（来自CC3M等），构造单轮指令数据（如“请描述图像” + 人工标注描述）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">冻结参数：</font>**<font style="color:#ED740C;">视觉编码器和语言模型权重固定</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">仅训练投影层：通过最小化语言模型的交叉熵损失，优化视觉到文本的映射。</font>
            + <font style="color:rgb(25, 27, 31);">关键公式：</font>
    4. **<font style="color:rgb(25, 27, 31);">阶段2：指令微调（任务对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：提升模型对复杂指令（如推理、问答）的响应能力。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用158K GPT-4生成的指令-答案对（涵盖描述、推理、对话等任务）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">解冻语言模型：</font>**<font style="color:#ED740C;">微调语言模型参数（LoRA或全参数微调）</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">联合优化：投影层和语言模型共同更新，强化跨模态交互。</font>
            + <font style="color:rgb(25, 27, 31);">示例任务：</font>
                - <font style="color:rgb(25, 27, 31);">输入：图像 + “图中的小狗是什么颜色？”</font>
                - <font style="color:rgb(25, 27, 31);">输出：语言模型需结合视觉token（如“黑色毛发”）生成答案“黑色”。</font>

# 
