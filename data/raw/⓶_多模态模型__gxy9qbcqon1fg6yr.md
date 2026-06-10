# ⓶ 多模态模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/gxy9qbcqon1fg6yr -->

##  CLIP
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
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import vit_b_16  # Using a pre-trained ViT model

class SimpleTokenizer(nn.Module):
    # 这里是一个简化的tokenizer
    def __init__(self, vocab_size, embed_dim):
        super(SimpleTokenizer, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embed_dim)

    def forward(self, input_ids):
        return self.embeddings(input_ids)  # 返回词嵌入

class CLIP(nn.Module):
    def __init__(self, vocab_size, embed_dim, image_size):
        super(CLIP, self).__init__()
        self.visual_encoder = vit_b_16(pretrained=True)  # 使用预训练的ViT模型
        self.visual_encoder.heads = nn.Identity()  # 去掉头部以只保留特征层
        self.tokenizer = SimpleTokenizer(vocab_size, embed_dim)
        self.text_projection = nn.Linear(embed_dim, embed_dim)  # 用于将文本嵌入映射到相同维度

    def encode_image(self, image):
        # 图像编码
        with torch.no_grad():
            features = self.visual_encoder(image)  # 输出维度 (B, embed_dim)
        return features

    def encode_text(self, text):
        # 文本编码
        text_embeddings = self.tokenizer(text)  # 输出维度 (B, seq_len, embed_dim)
        text_embeddings = text_embeddings.mean(dim=1)  # 取平均，输出维度 (B, embed_dim)
        return self.text_projection(text_embeddings)  # 投影到图片特征空间

    def forward(self, images, texts):
        image_features = self.encode_image(images)
        text_features = self.encode_text(texts)
        
        # 归一化特征
        image_features = F.normalize(image_features, dim=-1)
        text_features = F.normalize(text_features, dim=-1)
        
        # 计算点积相似度
        logits = image_features @ text_features.t()  # 输出维度 (B, B)
        return logits

# 维度说明：
# images: (B, 3, 224, 224) -> B是批量大小，3是通道数，224x224是图像大小
# texts: (B, seq_len) -> seq_len是文本序列长度
# 训练伪代码
model = CLIP()
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for images, texts in dataloader:
    logits = model(images, texts)
    labels = torch.arange(len(images))
    loss = F.cross_entropy(logits, labels) + F.cross_entropy(logits.t(), labels)
    loss.backward()
    optimizer.step()
```

### <font style="color:rgb(51, 51, 51);">InfoNCE</font>
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



### LLAVA与CLIP对齐的对比
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

## <font style="color:rgb(31, 35, 40);">SigLIP</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">SigLIP（</font>**<font style="color:rgb(51, 51, 51);">Sigmoid Loss for Language Image Pre-Training</font>**<font style="color:rgb(51, 51, 51);">）是 Google DeepMind 在 2023 年提出的多模态对比学习模型，基于经典 CLIP 架构改进。传统 CLIP 采用 Softmax 交叉熵损失，面临</font>**<font style="color:rgb(51, 51, 51);">负样本偏差</font>**<font style="color:rgb(51, 51, 51);">（大量不相关负样本对训练效率的影响）和</font>**<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">（需计算所有负样本对）的问题。SigLIP 通过 </font>**<font style="color:rgb(51, 51, 51);">Sigmoid 损失函数</font>**<font style="color:rgb(51, 51, 51);">和创新负采样策略，显著提升了训练效率和模型性能。</font>

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **损失函数改进**：
    - <font style="color:rgb(51, 51, 51);">将 CLIP 的对称 Softmax 损失替换为</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Sigmoid 损失</font>**<font style="color:rgb(51, 51, 51);">，直接优化正样本对的相似度。</font>
    - <font style="color:rgb(51, 51, 51);">数学形式：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086031060-31ade1c1-d5c3-46b4-bc1a-ed325c425689.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 s</font><sub><font style="color:rgb(51, 51, 51);">ij</font></sub><font style="color:rgb(51, 51, 51);">是图像-文本相似度，τ为温度系数，λ 负样本权重。</font>
2. **动态负采样**：
    - <font style="color:rgb(51, 51, 51);">每个 Batch 中仅采样部分负样本（如 1/4），降低计算量。</font>
    - <font style="color:rgb(51, 51, 51);">采用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Difficulty-aware 采样</font>**<font style="color:rgb(51, 51, 51);">：优先选择与正样本相似度高的困难负样本。</font>
3. **训练效率优化**：
    - <font style="color:rgb(51, 51, 51);">去除 CLIP 的对称损失设计，单模态编码器可独立训练。</font>
    - <font style="color:rgb(51, 51, 51);">支持超大 Batch Size（可达百万级）训练。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Web 级图文对：LAION-2B（SigLIP 专用子集）、ALIGN 的 JFT-3B。</font>
    - <font style="color:rgb(51, 51, 51);">合成数据：通过图像描述生成模型（如 PaLI）增强文本多样性。</font>
+ **<font style="color:rgb(51, 51, 51);">数据清洗</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">基于 CLIP 相似度过滤低质量样本（阈值保留 Top 30%）。</font>
    - <font style="color:rgb(51, 51, 51);">语言过滤（保留英语、西班牙语等主要语言）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51);">SigLIP 沿用 CLIP 的双塔架构</font>

**<font style="color:rgb(51, 51, 51);">关键差异</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">投影层设计</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">独立可学习温度参数 τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">，非共享权重。</font>
    - <font style="color:rgb(51, 51, 51);">投影层维度可调整（默认 512 维）。</font>
2. **<font style="color:rgb(51, 51, 51);">编码器选择</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像编码器：ViT-G/14（基于 EVA-02 预训练）、ResNet-RS-152。</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器：BERT-style Transformer，最大长度 64。</font>
3. **<font style="color:rgb(51, 51, 51);">高效分块实现：</font>**

**<font style="color:rgb(25, 27, 31);">对比训练通常利用数据并行性</font>**<font style="color:rgb(25, 27, 31);">。当数据分布在D个设备上时计算损失，需要收集所有嵌入，这涉及到昂贵的全收集操作(</font>**<font style="color:rgb(25, 27, 31);">all-gathers</font>**<font style="color:rgb(25, 27, 31);">)，更重要的是，</font>**<font style="color:rgb(25, 27, 31);">需要实例化一个内存密集型的</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">|B|×|B|</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">两两相似度矩阵</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">然而，</font>**<font style="color:rgb(25, 27, 31);">Sigmoid损失特别适合于一种内存高效、快速且数值稳定的实现方式，</font>****<font style="color:#74B602;">这种方式改善了上述两个问题。将每个设备上的批量大小表示为 </font>**<font style="color:#74B602;">b=|B|/D</font><font style="color:rgb(25, 27, 31);"> ，损失可以重新表述为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086494587-891d2071-1a7e-44c5-b43b-e9dd721f728f.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086480464-f79f2096-17bc-4dcd-9f37-78d018a282ac.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练初始化**：
    - <font style="color:rgb(51, 51, 51);">图像编码器：加载 EVA-02 或 ResNet 预训练权重。</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器：随机初始化或加载 BERT 权重。</font>
2. **对比学习训练**：
    - **<font style="color:rgb(51, 51, 51);">输入构造</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">Batch 内图像-文本对：正样本为匹配对，负样本来自同 Batch 其他样本。</font>
        * <font style="color:rgb(51, 51, 51);">动态采样 25% 负样本参与损失计算。</font>
    - **<font style="color:rgb(51, 51, 51);">损失计算</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">计算所有正样本对的 Sigmoid 概率。</font>
        * <font style="color:rgb(51, 51, 51);">仅对采样的负样本计算 1−σ(s</font><sub><font style="color:rgb(51, 51, 51);">ij</font></sub><font style="color:rgb(51, 51, 51);">)。</font>
    - **<font style="color:rgb(51, 51, 51);">梯度更新</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">采用 LAMB 优化器，支持超大 Batch（可达 1M）。</font>
        * <font style="color:rgb(51, 51, 51);">学习率 warmup 至 1e-3，余弦衰减调度。</font>
3. **微调阶段（可选）**：
    - <font style="color:rgb(51, 51, 51);">冻结图像编码器，仅微调文本编码器适配下游任务。</font>
    - <font style="color:rgb(51, 51, 51);">添加任务特定头部（如分类层）。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">训练效率提升：相比 CLIP，达到相同性能需 1/10 计算量。</font>
2. <font style="color:rgb(51, 51, 51);">更优的零样本性能：在 ImageNet 零样本分类上超越 CLIP 5%~10%。</font>
3. <font style="color:rgb(51, 51, 51);">支持超大 Batch Size：适合分布式训练。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">对温度参数</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">敏感，需精细调参。</font>
2. <font style="color:rgb(51, 51, 51);">文本多样性受限：依赖预训练文本编码器的能力。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">零样本图像分类</font>**<font style="color:rgb(51, 51, 51);">：直接匹配文本标签特征。</font>
2. **<font style="color:rgb(51, 51, 51);">跨模态检索</font>**<font style="color:rgb(51, 51, 51);">：图文互搜（如 Google Images 搜索）。</font>
3. **<font style="color:rgb(51, 51, 51);">多模态内容审核</font>**<font style="color:rgb(51, 51, 51);">：识别图文不一致的违规内容。</font>
4. **<font style="color:rgb(51, 51, 51);">机器人视觉导航</font>**<font style="color:rgb(51, 51, 51);">：结合文本指令理解环境。</font>
5. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：为生成模型（如 Stable Diffusion）提供跨模态对齐信号。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合损失函数</font>**<font style="color:rgb(51, 51, 51);">：结合 Sigmoid 损失与 KL 散度损失（对齐分布）。</font>
2. **<font style="color:rgb(51, 51, 51);">多粒度对比</font>**<font style="color:rgb(51, 51, 51);">：引入局部区域-短语对齐（类似 ALBEF）。</font>
3. **<font style="color:rgb(51, 51, 51);">动态温度调整</font>**<font style="color:rgb(51, 51, 51);">：根据训练阶段自动调节</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);">。</font>
4. **<font style="color:rgb(51, 51, 51);">跨模态蒸馏</font>**<font style="color:rgb(51, 51, 51);">：用 SigLIP 指导小型任务模型训练。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SigLIP(nn.Module):
    def __init__(self, image_encoder, text_encoder, proj_dim=512):
        super().__init__()
        self.image_encoder = image_encoder  # 例如 ViT
        self.text_encoder = text_encoder    # 例如 BERT
        self.image_proj = nn.Linear(image_encoder.output_dim, proj_dim)
        self.text_proj = nn.Linear(text_encoder.config.hidden_size, proj_dim)
        self.temperature = nn.Parameter(torch.ones([]) * 0.07)  # 可学习温度参数

    def forward(self, images, texts):
        # 编码图像和文本
        image_feats = self.image_encoder(images)  # (B, D_img)
        text_feats = self.text_encoder(texts.input_ids, attention_mask=texts.attention_mask).last_hidden_state[:,0]  # (B, D_text)
        
        # 投影并归一化
        image_emb = F.normalize(self.image_proj(image_feats), dim=-1)  # (B, D)
        text_emb = F.normalize(self.text_proj(text_feats), dim=-1)     # (B, D)
        
        # 计算相似度矩阵
        logits = image_emb @ text_emb.T  # (B, B)
        logits = logits / self.temperature.exp()
        return logits

def siglip_loss(logits, neg_sample_ratio=0.25):
    batch_size = logits.size(0)
    labels = torch.arange(batch_size, device=logits.device)  # 对角线为正样本
    
    # 正样本损失
    pos_logits = logits.diag().unsqueeze(-1)  # (B,1)
    pos_loss = -F.logsigmoid(pos_logits).mean()
    
    # 负样本采样
    neg_mask = ~torch.eye(batch_size, dtype=torch.bool, device=logits.device)
    neg_logits = logits[neg_mask].view(batch_size, -1)  # (B, B-1)
    
    # 动态选择困难负样本
    k = int(neg_sample_ratio * (batch_size - 1))
    topk_values, _ = torch.topk(neg_logits, k=k, dim=1)
    sampled_neg = topk_values  # (B, k)
    
    # 负样本损失
    neg_loss = -torch.log(1 - torch.sigmoid(sampled_neg)).mean()
    
    return pos_loss + neg_loss

# 使用示例
image_encoder = vit_base_patch16_224(pretrained=True)
text_encoder = BertModel.from_pretrained('bert-base-uncased')
model = SigLIP(image_encoder, text_encoder)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

# 训练循环
for images, texts in dataloader:
    logits = model(images, texts)
    loss = siglip_loss(logits)
    loss.backward()
    optimizer.step()

```



## EVA-CLIP
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：《</font><font style="color:rgb(34, 34, 38);">EVA-CLIP: Improved Training Techniques for CLIP at Scale》</font>

**<font style="color:rgb(51, 51, 51);">CLIP的局限性</font>**<font style="color:rgb(51, 51, 51);">：OpenAI的CLIP模型通过对比学习实现图像-文本对齐，但受限于模型规模（如最大ViT-L/14）和训练效率。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">扩展需求</font>**<font style="color:rgb(51, 51, 51);">：大规模视觉-语言预训练需要更高容量模型，但直接放大CLIP会面临训练不稳定、收敛困难等问题。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">EVA-CLIP目标</font>**<font style="color:rgb(51, 51, 51);">：智源研究院提出EVA-CLIP，通过渐进式扩展策略训练更大模型（如ViT-G/14），突破性能天花板。</font>

:::

<font style="color:rgb(51, 51, 51);">EVA-CLIP通过渐进式扩展和训练策略优化，显著提升了视觉-语言对齐能力，为多模态任务提供了强大的基础模型。其核心创新在于平衡模型规模与训练稳定性，未来可向高效推理和少样本学习方向发展。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741093312252-7dc4f848-6e70-4a81-97b4-4d3042ce32f5.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">渐进式扩展（Evolving Scaling）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">从小模型（ViT-B）开始逐步放大到ViT-G，复用中间参数，稳定训练过程。</font>
    - <font style="color:rgb(51, 51, 51);">避免直接训练超大模型的优化困难。</font>
+ **<font style="color:rgb(51, 51, 51);">锁定图像塔（Locked-image Tuning）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">在预训练后冻结图像编码器，仅微调文本编码器，减少过拟合风险。</font>
+ **<font style="color:rgb(51, 51, 51);">混合分辨率训练</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">动态调整输入图像分辨率（如224x224与336x336交替）提升泛化性。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像-文本对</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">公开数据：LAION-2B、COCO、Visual Genome等。</font>
    - <font style="color:rgb(51, 51, 51);">专有数据：经过清洗的网页爬取数据（约5B对）。</font>
+ **<font style="color:rgb(51, 51, 51);">数据筛选</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">基于CLIP相似度过滤低质量图文对。</font>
    - <font style="color:rgb(51, 51, 51);">平衡多语言数据（中/英占比约1:3）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">基于ViT架构，最大支持ViT-Giant（ViT-G，宽度1408，层数40）。</font>
    - <font style="color:rgb(51, 51, 51);">引入</font>**<font style="color:rgb(51, 51, 51);">EVA-ViT</font>**<font style="color:rgb(51, 51, 51);">改进：</font>
        * <font style="color:rgb(51, 51, 51);">使用</font>**<font style="color:#74B602;">动态位置编码（Dynamic Position Bias）</font>**<font style="color:rgb(51, 51, 51);">替代固定位置编码。</font>
        * <font style="color:rgb(51, 51, 51);">替换部分FFN层为卷积增强局部感知。</font>
+ **<font style="color:rgb(51, 51, 51);">文本编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Transformer结构（与CLIP相同，12层，宽度512）。</font>
+ **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">独立线性层将图像/文本特征映射到共享对比空间（维度：4096）。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练阶段**：
    - **<font style="color:rgb(51, 51, 51);">数据</font>**<font style="color:rgb(51, 51, 51);">：4B图像-文本对，混合分辨率输入。</font>
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：对比损失（InfoNCE），最大化匹配对的相似度。</font>
    - **<font style="color:rgb(51, 51, 51);">优化</font>**<font style="color:rgb(51, 51, 51);">：AdamW，学习率预热+余弦衰减，批量大小32K。</font>
2. **锁定微调阶段**：
    - <font style="color:rgb(51, 51, 51);">冻结视觉编码器参数。</font>
    - <font style="color:rgb(51, 51, 51);">仅更新文本编码器和投影层参数。</font>
    - <font style="color:rgb(51, 51, 51);">目标：提升特定任务（如零样本分类）的泛化性。</font>
3. **混合训练策略**：
    - <font style="color:rgb(51, 51, 51);">交替使用不同分辨率输入（如50% 224x224，50% 336x336）。</font>
    - <font style="color:rgb(51, 51, 51);">动态掩码部分图像块以增强鲁棒性。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">性能显著超越CLIP（ViT-G在ImageNet零样本达80.5%）。</font>
+ <font style="color:rgb(51, 51, 51);">渐进式扩展策略稳定，可训练超10B参数模型。</font>
+ <font style="color:rgb(51, 51, 51);">混合分辨率提升跨尺度泛化能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">训练计算成本极高（需数千块GPU）。</font>
+ <font style="color:rgb(51, 51, 51);">依赖海量数据清洗，工程复杂度高。</font>
+ <font style="color:rgb(51, 51, 51);">超大模型推理延迟较高。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">零样本分类</font>**<font style="color:rgb(51, 51, 51);">：直接匹配图像与类别文本描述。</font>
+ **<font style="color:rgb(51, 51, 51);">图文检索</font>**<font style="color:rgb(51, 51, 51);">：跨模态搜索（图搜文/文搜图）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态生成</font>**<font style="color:rgb(51, 51, 51);">：作为图像生成模型（如Stable Diffusion）的编码器。</font>
+ **<font style="color:rgb(51, 51, 51);">细粒度理解</font>**<font style="color:rgb(51, 51, 51);">：结合检测/分割模型提升场景理解。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化部署</font>**<font style="color:rgb(51, 51, 51);">：知识蒸馏到小模型（如ViT-B）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态增强</font>**<font style="color:rgb(51, 51, 51);">：融合音频/视频数据扩展应用边界。</font>
+ **<font style="color:rgb(51, 51, 51);">动态分辨率推理</font>**<font style="color:rgb(51, 51, 51);">：根据输入内容自适应调整分辨率。</font>
+ **<font style="color:rgb(51, 51, 51);">提示学习</font>**<font style="color:rgb(51, 51, 51);">：引入可训练提示（Prompt Tuning）提升少样本能力。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch import nn
from transformers import ViTModel, BertModel

class EVACLIP(nn.Module):
    def __init__(self, vit_model="eva_vit_g", text_model="bert-base"):
        super().__init__()
        # 视觉编码器
        self.visual = ViTModel.from_pretrained(vit_model)
        # 文本编码器
        self.text = BertModel.from_pretrained(text_model)
        # 投影层
        self.visual_proj = nn.Linear(1408, 4096)  # ViT-G隐藏层维度1408
        self.text_proj = nn.Linear(768, 4096)     # BERT-base隐藏层维度768
        
    def forward(self, images, input_ids, attention_mask):
        # 图像特征提取
        vis_features = self.visual(images).last_hidden_state[:, 0, :]  # [CLS] token
        vis_emb = self.visual_proj(vis_features)
        
        # 文本特征提取
        text_features = self.text(input_ids, attention_mask).last_hidden_state[:, 0, :]
        text_emb = self.text_proj(text_features)
        
        # 归一化
        vis_emb = vis_emb / vis_emb.norm(dim=-1, keepdim=True)
        text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
        
        return vis_emb, text_emb

# 对比损失计算
def contrastive_loss(logits, temperature=0.07):
    labels = torch.arange(logits.size(0), device=logits.device)
    loss_i = nn.CrossEntropyLoss()(logits / temperature, labels)
    loss_t = nn.CrossEntropyLoss()(logits.t() / temperature, labels)
    return (loss_i + loss_t) / 2

```

```python
model = EVACLIP()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

for batch in dataloader:
    images, texts = batch
    # 文本编码
    text_inputs = tokenizer(texts, padding=True, return_tensors="pt")
    # 前向计算
    vis_emb, text_emb = model(images, text_inputs.input_ids, text_inputs.attention_mask)
    # 计算相似度矩阵
    logits = vis_emb @ text_emb.t() * torch.exp(torch.tensor(100.0))
    # 损失计算
    loss = contrastive_loss(logits)
    # 反向传播
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

```

## <font style="color:rgb(51, 51, 51);">FLAVA</font>
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">多模态统一需求</font>**<font style="color:rgb(51, 51, 51);">：传统多模态模型（如CLIP、ViLBERT）通常需单独训练单模态编码器，导致跨模态任务与单模态任务性能难以兼顾。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">Meta AI的突破</font>**<font style="color:rgb(51, 51, 51);">：2022年提出的FLAVA旨在构建统一的视觉-语言基础模型，</font>**<font style="color:rgb(51, 51, 51);">同时支持单模态（纯文本/图像）和跨模态任务</font>**<font style="color:rgb(51, 51, 51);">，解决多场景适配问题。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741159070937-0efc1844-07a0-41e3-9f81-5c26321e9fd5.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">统一架构设计</font>**<font style="color:rgb(51, 51, 51);">：单模态（文本/图像）与多模态共享同一Transformer骨干网络，参数复用率超90%。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务联合预训练</font>**<font style="color:rgb(51, 51, 51);">：同时优化文本MLM、图像MAE、图文对比（ITC）、图文匹配（ITM）等6种损失函数。</font>
+ **<font style="color:rgb(51, 51, 51);">模态解耦与融合</font>**<font style="color:rgb(51, 51, 51);">：支持单模态独立推理（如文本分类）和跨模态联合推理（如VQA）。</font>
+ **<font style="color:rgb(51, 51, 51);">零样本泛化</font>**<font style="color:rgb(51, 51, 51);">：通过prompt tuning适配下游任务，无需微调。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多模态数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图文对：Conceptual Captions（CC3M）、SBU Captions等（共4M对）。</font>
+ **<font style="color:rgb(51, 51, 51);">单模态数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">文本：Wikipedia、BookCorpus（纯文本语料）。</font>
    - <font style="color:rgb(51, 51, 51);">图像：ImageNet-1K（纯图像分类数据）。</font>
+ **<font style="color:rgb(51, 51, 51);">预处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">文本：BERT式WordPiece分词（词表30K）。</font>
    - <font style="color:rgb(51, 51, 51);">图像：ViT式分块（224x224→16x16 patches）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741159083598-e81701c6-cef1-4f0e-bb10-bc33519fda20.png)

+ **<font style="color:rgb(51, 51, 51);">单模态编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">文本编码器</font>**<font style="color:rgb(51, 51, 51);">：12层Transformer（类似BERT），处理文本序列。</font>
    - **<font style="color:rgb(51, 51, 51);">图像编码器</font>**<font style="color:rgb(51, 51, 51);">：12层Vision Transformer（ViT），处理图像块序列。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">共享参数的12层Transformer，输入为</font>`<font style="color:rgb(51, 51, 51);">[CLS] + 文本emb + [SEP] + 图像emb</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">特殊Token</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - `<font style="color:rgb(51, 51, 51);">[CLS]</font>`<font style="color:rgb(51, 51, 51);">：聚合多模态表征，用于分类任务。</font>
    - `<font style="color:rgb(51, 51, 51);">[SEP]</font>`<font style="color:rgb(51, 51, 51);">：分隔文本与图像输入。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **单模态预训练**：
    - <font style="color:rgb(51, 51, 51);">文本：MLM（掩码语言建模），掩码率15%。</font>
    - <font style="color:rgb(51, 51, 51);">图像：MAE（掩码自编码），掩码率75%。</font>
2. **多模态联合训练**：
    - **<font style="color:rgb(51, 51, 51);">对比学习（ITC）</font>**<font style="color:rgb(51, 51, 51);">：图文对相似度最大化，负样本来自同batch。</font>
    - **<font style="color:rgb(51, 51, 51);">匹配任务（ITM）</font>**<font style="color:rgb(51, 51, 51);">：二分类判断图文是否匹配。</font>
    - **<font style="color:rgb(51, 51, 51);">多模态MLM</font>**<font style="color:rgb(51, 51, 51);">：联合掩码文本+图像块，预测被掩内容。</font>
3. **零样本适配**：
    - <font style="color:rgb(51, 51, 51);">使用Prompt模板（如</font>`<font style="color:rgb(51, 51, 51);">"A photo of [CLS]"</font>`<font style="color:rgb(51, 51, 51);">）直接生成分类结果。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">统一的单/多模态处理能力，减少部署成本。</font>
+ <font style="color:rgb(51, 51, 51);">零样本性能显著优于CLIP（ImageNet Acc 72.3% vs 68.3%）。</font>
+ <font style="color:rgb(51, 51, 51);">支持复杂多模态推理（需同时理解图文关系的任务）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">模型参数量大（350M），训练需数千GPU小时。</font>
+ <font style="color:rgb(51, 51, 51);">图像分块丢失局部细节，细粒度任务（如目标检测）需额外设计。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">跨模态检索</font>**<font style="color:rgb(51, 51, 51);">：图文互搜（电商产品搜索）。</font>
+ **<font style="color:rgb(51, 51, 51);">视觉问答（VQA）</font>**<font style="color:rgb(51, 51, 51);">：医疗报告图文联合分析。</font>
+ **<font style="color:rgb(51, 51, 51);">内容审核</font>**<font style="color:rgb(51, 51, 51);">：检测图文不一致的违规内容。</font>
+ **<font style="color:rgb(51, 51, 51);">教育辅助</font>**<font style="color:rgb(51, 51, 51);">：自动生成教材插图说明。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化</font>**<font style="color:rgb(51, 51, 51);">：知识蒸馏到小型化模型（如FLAVA-Tiny）。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务增强</font>**<font style="color:rgb(51, 51, 51);">：引入视频模态支持时序理解。</font>
+ **<font style="color:rgb(51, 51, 51);">局部感知</font>**<font style="color:rgb(51, 51, 51);">：融合CNN特征保留图像细节。</font>
+ **<font style="color:rgb(51, 51, 51);">增量学习</font>**<font style="color:rgb(51, 51, 51);">：在不遗忘旧任务的前提下扩展新模态。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import BertModel, ViTModel

class FLAVA(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # 单模态编码器
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')
        self.image_encoder = ViTModel.from_pretrained('google/vit-base-patch16-224')
        # 多模态编码器（共享参数）
        self.multimodal_encoder = BertModel(self.text_encoder.config)
        # 投影头
        self.text_proj = torch.nn.Linear(768, 256)
        self.image_proj = torch.nn.Linear(768, 256)
        
    def forward(self, text_input, image_input):
        # 单模态编码
        text_emb = self.text_encoder(**text_input).last_hidden_state
        image_emb = self.image_encoder(pixel_values=image_input).last_hidden_state
        # 多模态融合
        multimodal_input = torch.cat([
            text_emb[:, 0:1],  # [CLS]
            text_emb[:, 1:], 
            torch.ones_like(text_emb[:, 0:1]) * 0.1,  # [SEP]
            image_emb
        ], dim=1)
        multimodal_output = self.multimodal_encoder(inputs_embeds=multimodal_input)
        # 对比学习投影
        text_proj = self.text_proj(text_emb[:, 0])
        image_proj = self.image_proj(image_emb[:, 0])
        return {
            "text_emb": text_proj,
            "image_emb": image_proj,
            "multimodal_cls": multimodal_output.last_hidden_state[:, 0]
        }

# 示例调用
model = FLAVA()
text_input = {"input_ids": torch.randint(0, 1000, (1, 32)), "attention_mask": torch.ones(1, 32)}
image_input = torch.randn(1, 3, 224, 224)
outputs = model(text_input, image_input)

```

```python
# 多任务损失计算
def multiview_loss(outputs, labels):
    # 对比损失
    logits = outputs["text_emb"] @ outputs["image_emb"].t() / 0.07
    contrastive_loss = F.cross_entropy(logits, labels)
    # 匹配损失（ITM）
    itm_logits = classifier(outputs["multimodal_cls"])
    itm_loss = F.binary_cross_entropy_with_logits(itm_logits, labels)
    # 总损失
    return contrastive_loss + 0.5 * itm_loss

# 零样本分类示例
def zero_shot_classify(image, class_names):
    text_inputs = [f"A photo of a {name}" for name in class_names]
    text_embs = model.encode_text(tokenize(text_inputs))
    image_emb = model.encode_image(image)
    similarity = image_emb @ text_embs.t()
    return torch.argmax(similarity)

```

## ALBEF
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ALBEF（Align before Fuse）是2021年提出的多模态视觉-语言预训练模型，旨在解决传统方法（如CLIP、ALIGN）中的模态对齐问题。传统模型通过对比学习对齐全局特征，但缺乏</font>**<font style="color:#ED740C;">细粒度语义对齐（如物体-属性关系）</font>**<font style="color:rgb(51, 51, 51);">。ALBEF通过</font>**<font style="color:rgb(51, 51, 51);">先对齐再融合</font>**<font style="color:rgb(51, 51, 51);">的策略，结合</font>**<font style="color:#ED740C;">对比学习与跨模态注意力机制</font>**<font style="color:rgb(51, 51, 51);">，提升多模态理解能力。</font>

:::

<font style="color:rgb(51, 51, 51);">ALBEF通过</font>**<font style="color:#74B602;">多阶段对齐策略和动量蒸馏</font>**<font style="color:rgb(51, 51, 51);">，显著提升了多模态任务的性能。其核心思想“</font>**<font style="color:#74B602;">先对齐再融合</font>**<font style="color:rgb(51, 51, 51);">”为后续模型（如BLIP、CoCa）提供了重要参考。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741072497939-e84345c0-2e45-4388-af59-c34384dd3230.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多阶段对齐策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. **<font style="color:rgb(51, 51, 51);">单模态对比学习</font>**<font style="color:rgb(51, 51, 51);">：通过图像-文本对比（ITC）初步对齐全局特征。</font>
    2. **<font style="color:rgb(51, 51, 51);">跨模态融合</font>**<font style="color:rgb(51, 51, 51);">：使用跨模态注意力（cross-attention）捕捉细粒度交互。</font>
    3. **<font style="color:rgb(51, 51, 51);">动量蒸馏</font>**<font style="color:rgb(51, 51, 51);">：通过动量模型生成伪标签，缓解数据噪声问题。</font>
+ **<font style="color:rgb(51, 51, 51);">动量编码器</font>**<font style="color:rgb(51, 51, 51);">：维护一个动量更新的图像/文本编码器，生成更稳定的特征表示，避免训练波动。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">预训练数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">4M图像-文本对</font>**<font style="color:rgb(51, 51, 51);">：来自Conceptual Captions、SBU Captions、COCO、Visual Genome等。</font>
    - **<font style="color:rgb(51, 51, 51);">噪声处理</font>**<font style="color:rgb(51, 51, 51);">：通过动量模型过滤低质量样本。</font>
+ **<font style="color:rgb(51, 51, 51);">下游任务数据</font>**<font style="color:rgb(51, 51, 51);">：图像检索（Flickr30K）、视觉问答（VQA2.0）、视觉推理（NLVR2）等。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51);">ALBEF包含三个核心模块：</font>

1. **单模态编码器**：
    - **<font style="color:rgb(51, 51, 51);">图像编码器</font>**<font style="color:rgb(51, 51, 51);">：ViT-B/16（12层Transformer，输出197×768特征）。</font>
    - **<font style="color:rgb(51, 51, 51);">文本编码器</font>**<font style="color:rgb(51, 51, 51);">：BERT-base（12层Transformer，输出[CLS]标记作为全局特征）。</font>
2. **多模态编码器**：
    - <font style="color:rgb(51, 51, 51);">6层Transformer，通过跨模态注意力融合图像（CLS标记）与文本特征。</font>
3. **动量编码器**：
    - <font style="color:rgb(51, 51, 51);">图像/文本编码器的动量版本（EMA更新），用于生成伪标签。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **ITC Loss（图像-文本对比）**：

```python
def itc_loss(image_emb, text_emb, temperature=0.07):
    logits = (image_emb @ text_emb.T) / temperature
    labels = torch.arange(logits.size(0)).to(logits.device)
    loss_i = nn.CrossEntropyLoss()(logits, labels)
    loss_t = nn.CrossEntropyLoss()(logits.T, labels)
    return (loss_i + loss_t) / 2
```

2. **ITM Loss（图像-文本匹配）**：  
多模态编码器输出二分类概率，判断图像-文本是否匹配。
3. **动量蒸馏**：使用动量模型生成软标签计算KL散度损失。

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **优点**：
    - <font style="color:rgb(51, 51, 51);">细粒度对齐：跨模态注意力捕捉物体-属性关系。</font>
    - <font style="color:rgb(51, 51, 51);">抗噪声：动量蒸馏提升对噪声数据的鲁棒性。</font>
    - <font style="color:rgb(51, 51, 51);">高效：对比学习预训练加速收敛。</font>
+ **缺点**：
    - <font style="color:rgb(51, 51, 51);">计算开销大：多模态编码器增加参数量。</font>
    - <font style="color:rgb(51, 51, 51);">依赖预训练数据：数据质量影响模型性能。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像-文本检索</font>**<font style="color:rgb(51, 51, 51);">：双向检索（图搜文/文搜图）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态推理</font>**<font style="color:rgb(51, 51, 51);">：如NLVR2（判断文本是否描述图像内容）。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化设计</font>**<font style="color:rgb(51, 51, 51);">：替换ViT为Swin Transformer减少计算量。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：引入更强的图像/文本增强策略（如Diffusion生成）。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务学习</font>**<font style="color:rgb(51, 51, 51);">：联合训练检索、生成、推理任务。</font>
+ **<font style="color:rgb(51, 51, 51);">知识蒸馏</font>**<font style="color:rgb(51, 51, 51);">：用ALBEF作为教师模型压缩小模型。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import BertModel, ViTModel

class ImageEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.vit = ViTModel.from_pretrained("google/vit-base-patch16-224")

    def forward(self, x):
        return self.vit(x).last_hidden_state[:, 0, :]  # [CLS] token

class TextEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")

    def forward(self, input_ids, attention_mask):
        return self.bert(input_ids, attention_mask).last_hidden_state[:, 0, :]

class MultimodalEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(d_model=768, nhead=12)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=6)

    def forward(self, image_emb, text_emb):
        combined = torch.cat([image_emb.unsqueeze(1), text_emb.unsqueeze(1)], dim=1)
        return self.transformer(combined)

class ALBEF(nn.Module):
    def __init__(self, momentum=0.995):
        super().__init__()
        self.img_encoder = ImageEncoder()
        self.txt_encoder = TextEncoder()
        self.multimodal_encoder = MultimodalEncoder()
        
        # Momentum encoders
        self.img_encoder_m = ImageEncoder()
        self.txt_encoder_m = TextEncoder()
        self._init_momentum_models()
        
    def _init_momentum_models(self):
        for param, param_m in zip(self.img_encoder.parameters(), self.img_encoder_m.parameters()):
            param_m.data.copy_(param.data)
            param_m.requires_grad = False
        # Similarly for text encoder...

    @torch.no_grad()
    def momentum_update(self, momentum=0.995):
        # EMA update for momentum encoders
        for param, param_m in zip(self.img_encoder.parameters(), self.img_encoder_m.parameters()):
            param_m.data = momentum * param_m.data + (1 - momentum) * param.data
        # Similarly for text encoder...

```



## BLIP
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">BLIP（Bootstrapping Language-Image Pre-training）</font>**<font style="color:rgb(51, 51, 51);"> 是 Salesforce Research 在 2022 年提出的视觉-语言预训练模型，旨在解决多模态任务中 </font><font style="color:#ED740C;">理解和生成 的统一性问题</font><font style="color:rgb(51, 51, 51);">。传统模型如 CLIP 仅擅长图文对齐，而生成模型如 DALL-E 缺乏细粒度理解能力。BLIP 通过融合多任务预训练和噪声数据清洗策略，显著提升了跨模态任务的性能。</font>

+ **<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>["BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation"](https://arxiv.org/abs/2201.12086)
+ **<font style="color:rgb(51, 51, 51);">官方代码</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/salesforce/BLIP](https://github.com/salesforce/BLIP)

:::

<font style="color:rgb(51, 51, 51);">通过 BLIP，研究者可在一个框架内同时解决</font>**<font style="color:#74B602;">视觉理解与生成任务</font>**<font style="color:rgb(51, 51, 51);">，为多模态 AI 应用提供了高效的基础模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740911608928-6827ba7c-3c3e-4682-9d02-d1c927b522fc.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **多模态混合框架（MED）**  
统一编码器-解码器架构，支持以下三种模式灵活切换：
    - **<font style="color:rgb(51, 51, 51);">单模态编码器</font>**<font style="color:rgb(51, 51, 51);">：提取图像和文本特征。</font>
    - **<font style="color:rgb(51, 51, 51);">图文交叉编码器</font>**<font style="color:rgb(51, 51, 51);">：深度融合多模态信息（用于理解任务）。</font>
    - **<font style="color:rgb(51, 51, 51);">条件解码器</font>**<font style="color:rgb(51, 51, 51);">：基于图像生成文本（用于生成任务）。</font>
2. **噪声数据清洗（Captioning & Filtering）**
    - **<font style="color:rgb(51, 51, 51);">Captioner</font>**<font style="color:rgb(51, 51, 51);">：用预训练模型为噪声图像生成高质量文本描述。</font>
    - **<font style="color:rgb(51, 51, 51);">Filter</font>**<font style="color:rgb(51, 51, 51);">：检测并过滤原始数据中的噪声文本-图像对。</font>
3. **多任务预训练目标**  
联合优化以下三个任务：
    - **<font style="color:rgb(51, 51, 51);">图文对比学习（Image-Text Contrastive, ITC）</font>**<font style="color:rgb(51, 51, 51);">：对齐图像和文本的嵌入空间。</font>
    - **<font style="color:rgb(51, 51, 51);">图文匹配（Image-Text Matching, ITM）</font>**<font style="color:rgb(51, 51, 51);">：判断图文是否匹配（二分类）。</font>
    - **<font style="color:rgb(51, 51, 51);">语言建模（Language Modeling, LM）</font>**<font style="color:rgb(51, 51, 51);">：基于图像生成文本描述。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">来源</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">干净数据：COCO、Visual Genome、Flickr30K 等标注数据集。</font>
    - <font style="color:rgb(51, 51, 51);">噪声数据：从网络爬取的 1.4 亿图文对（如 LAION）。</font>
+ **<font style="color:rgb(51, 51, 51);">处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用 BLIP 自身的</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Captioner</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">生成合成字幕，扩展高质量数据。</font>
    - <font style="color:rgb(51, 51, 51);">通过 </font>**<font style="color:rgb(51, 51, 51);">Filter</font>**<font style="color:rgb(51, 51, 51);"> 剔除原始噪声数据中的低质量样本。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740911955832-74df776a-425f-4b0a-bb01-81ab6f4131ad.png)

<font style="color:rgb(0, 0, 0);">caption-filter目的是提取更干净的训练数据（知识蒸馏），提升模型效果：</font>

    - <font style="color:rgb(0, 0, 0);">step1：用大规模数据集预训练一个 BLIP </font><font style="color:rgb(64, 64, 64);">模型</font>
    - <font style="color:rgb(0, 0, 0);">step2：用人工少量标注单独</font><font style="color:rgb(64, 64, 64);">finetune</font><font style="color:rgb(0, 0, 0);">两个子任务高精度模型</font><font style="color:rgb(64, 64, 64);">：</font><font style="color:rgb(0, 0, 0);">（1）</font><font style="color:rgb(64, 64, 64);">Fliter</font><font style="color:rgb(0, 0, 0);">模型（训练只用ITC、ITM损失）（2）</font><font style="color:rgb(64, 64, 64);">Captioner</font><font style="color:rgb(64, 64, 64);">模型</font><font style="color:rgb(0, 0, 0);">（训练只用LM损失）</font>
    - <font style="color:rgb(0, 0, 0);">step3：数据集通过</font><font style="color:rgb(64, 64, 64);">Fliter</font><font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">模型清洗，过滤掉其中噪声</font>
    - <font style="color:rgb(0, 0, 0);">step4：图片让</font><font style="color:rgb(64, 64, 64);">Captioner</font><font style="color:rgb(64, 64, 64);">模型</font><font style="color:rgb(0, 0, 0);">做图像文本生成，再用</font><font style="color:rgb(64, 64, 64);">Fliter</font><font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">模型对生成的结果做清洗</font>
    - <font style="color:rgb(0, 0, 0);">step5：用step3+step4得到的新的数据集重新训练 BLIP </font><font style="color:rgb(64, 64, 64);">模型</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">整体架构</font>**

```plain
BLIP 模型结构
├── 图像编码器（Image Encoder）: ViT/BERT 提取视觉特征
├── 文本编码器（Text Encoder）: BERT 提取文本特征
├── 图文交叉编码器（Cross-Encoder）: 多模态交互层（ITM 任务）
└── 条件解码器（Conditional Decoder）: 基于图像的文本生成（LM 任务）
```

2. **<font style="color:rgb(51, 51, 51);">关键组件</font>**
    1. **图像编码器**
        * <font style="color:rgb(51, 51, 51);">使用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Vision Transformer（ViT）</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">或</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">ResNet</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">提取图像特征。</font>
        * <font style="color:rgb(51, 51, 51);">输出：</font>`<font style="color:rgb(51, 51, 51);">[batch_size, num_patches, hidden_dim]</font>`
    2. **文本编码器/解码器**
        * <font style="color:rgb(51, 51, 51);">基于</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">BERT</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">架构，共享词嵌入层。</font>
        * <font style="color:rgb(51, 51, 51);">编码器：双向自注意力，输出文本特征。</font>
        * <font style="color:rgb(51, 51, 51);">解码器：因果自注意力（掩码），生成文本。</font>
    3. **多模态交互层**
        * <font style="color:rgb(51, 51, 51);">图像特征作为 Key/Value，文本特征作为 Query，通过交叉注意力融合。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

```python
# 图文对比学习（ITC）
def image_text_contrastive_loss(image_emb, text_emb, temperature=0.07):
    logits = (text_emb @ image_emb.T) / temperature
    labels = torch.arange(logits.size(0)).to(logits.device)
    loss = nn.CrossEntropyLoss()(logits, labels)
    return loss

# 图文匹配（ITM）
def image_text_matching_loss(cross_features, labels):
    logits = nn.Linear(768, 2)(cross_features[:, 0, :])  # [CLS] token
    loss = nn.CrossEntropyLoss()(logits, labels)
    return loss

# 语言建模（LM）
def language_modeling_loss(decoder_output, text_labels):
    logits = nn.Linear(768, vocab_size)(decoder_output)
    loss = nn.CrossEntropyLoss()(logits.view(-1, vocab_size), text_labels.view(-1))
    return loss

```

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 统一理解与生成任务，灵活性高</font> | <font style="color:rgb(51, 51, 51);">1. 模型参数量大，训练成本高</font> |
| <font style="color:rgb(51, 51, 51);">2. 噪声数据清洗提升数据质量</font> | <font style="color:rgb(51, 51, 51);">2. 依赖预训练图像编码器（如 ViT）的性能</font> |
| <font style="color:rgb(51, 51, 51);">3. 在少样本场景下表现优异</font> | <font style="color:rgb(51, 51, 51);">3. 生成文本的多样性和创造性有限</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像描述生成（Image Captioning）</font>**
2. **<font style="color:rgb(51, 51, 51);">视觉问答（Visual Question Answering, VQA）</font>**
3. **<font style="color:rgb(51, 51, 51);">图文检索（Image-Text Retrieval）</font>**
4. **<font style="color:rgb(51, 51, 51);">多模态对话系统（如医疗图像诊断报告生成）</font>**

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">模型轻量化：</font>**<font style="color:rgb(51, 51, 51);">使用蒸馏技术（如 TinyBLIP）压缩模型。</font>
2. **<font style="color:rgb(51, 51, 51);">数据增强：</font>**<font style="color:rgb(51, 51, 51);">结合扩散模型生成合成图像-文本对。</font>
3. **<font style="color:rgb(51, 51, 51);">多任务扩展：</font>**<font style="color:rgb(51, 51, 51);">引入目标检测（如 Region-of-Interest 特征）。</font>
4. **<font style="color:rgb(51, 51, 51);">长文本生成优化：</font>**<font style="color:rgb(51, 51, 51);">结合检索增强生成（RAG）提升生成连贯性。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch import nn
from transformers import BertModel, BertTokenizer, ViTModel

class BLIP(nn.Module):
    def __init__(self, config):
        super().__init__()
        # 图像编码器
        self.image_encoder = ViTModel.from_pretrained("google/vit-base-patch16-224")
        # 文本编码器
        self.text_encoder = BertModel.from_pretrained("bert-base-uncased")
        # 图文交叉编码器
        self.cross_encoder = nn.TransformerEncoderLayer(
            d_model=768, nhead=8, dim_feedforward=3072
        )
        # 条件解码器
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=768, nhead=8), num_layers=6
        )

    def forward(self, image, text):
        # 提取图像特征
        image_features = self.image_encoder(image).last_hidden_state
        # 提取文本特征
        text_features = self.text_encoder(text).last_hidden_state
        # 图文交叉编码（ITM 任务）
        cross_features = self.cross_encoder(
            src=text_features, 
            memory=image_features
        )
        # 生成文本（LM 任务）
        output = self.decoder(
            tgt=text_features, 
            memory=cross_features
        )
        return output

# 示例用法
config = {}
model = BLIP(config)
image = torch.randn(1, 3, 224, 224)  # 假设输入图像
text = torch.randint(0, 10000, (1, 32))  # 假设输入文本
output = model(image, text)
print(output.shape)  # torch.Size([1, 32, 768])

```





## BLIP2
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">BLIP-2（Bootstrapping Language-Image Pre-training）是Salesforce Research于2023年提出的多模态预训练模型，旨在高效融合视觉和语言模型。传统视觉语言模型（如CLIP、ALIGN）依赖端到端训练，计算成本高且难以直接利用大语言模型（LLM）。BLIP2通过冻结预训练视觉和语言模型参数，设计轻量级中间模块（Q-Former）实现模态对齐，显著降低了训练成本。</font>

:::

BLIP2通过创新的**<font style="color:#74B602;">两阶段训练和Q-Former设计</font>**，实现了高效的多模态对齐，成为视觉语言任务的新基准。未来可通过动态查询机制和混合微调策略进一步提升性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741073736253-1ab61f42-c942-4034-8eea-006ad2a4a68d.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **两阶段训练范式**：
    - **<font style="color:rgb(51, 51, 51);">Stage1</font>**<font style="color:rgb(51, 51, 51);">: 学习视觉-语言联合表示（冻结图像编码器）。</font>
    - **<font style="color:rgb(51, 51, 51);">Stage2</font>**<font style="color:rgb(51, 51, 51);">: 学习视觉到语言生成（冻结语言模型）。</font>
2. **Querying Transformer (Q-Former)**：
    - <font style="color:rgb(51, 51, 51);">通过可学习的查询向量（learnable queries）与图像特征交互，提取与文本对齐的视觉特征。</font>
    - <font style="color:rgb(51, 51, 51);">结合交叉注意力机制和自注意力机制，实现跨模态信息融合。</font>
3. **参数高效性**：
    - <font style="color:rgb(51, 51, 51);">冻结预训练模型参数（如ViT、EVA-CLIP、OPT、Flan-T5），仅训练Q-Former（约188M参数），大幅减少计算需求。</font>
4. **多任务预训练**：
    - <font style="color:rgb(51, 51, 51);">图像-文本对比学习（ITC）、图像-文本匹配（ITM）、图像描述生成（Captioning）。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：COCO、Visual Genome (VG)、CC3M、CC12M、SBU、LAION 400M。</font>
+ **<font style="color:rgb(51, 51, 51);">合成数据</font>**<font style="color:rgb(51, 51, 51);">：利用预训练模型生成噪声图像的文本描述（Boot strapping策略）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741073751893-dace8c1a-60b2-4d37-a4f4-87bacaaeb078.png)

1. **图像编码器（冻结）**：
    - <font style="color:rgb(51, 51, 51);">可选ViT、EVA-CLIP等，输出图像特征 Zv∈R</font><sup><font style="color:rgb(51, 51, 51);">Nv×d</font></sup><font style="color:rgb(51, 51, 51);">（Nv为图像块数，d</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为特征维度）。</font>
2. **Q-Former**：<font style="color:rgb(25, 27, 31);">核心是拿一组</font>**<font style="color:#ECAA04;">预定义好的、可学的、固定数量（M个）的Query tokens</font>**<font style="color:rgb(25, 27, 31);">，通过cross attention层去</font>**<font style="color:#74B602;">融合来自image encoder的image token信息</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - <font style="color:rgb(51, 51, 51);">输入：可学习查询向量 Q∈R</font><sup><font style="color:rgb(51, 51, 51);">Nq×d</font></sup><font style="color:rgb(51, 51, 51);">，Nq为查询数）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：</font>
        * **<font style="color:rgb(51, 51, 51);">图像-查询交叉注意力</font>**<font style="color:rgb(51, 51, 51);">：Q</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">与Zv交互。</font>
        * **<font style="color:rgb(51, 51, 51);">文本-查询自注意力</font>**<font style="color:rgb(51, 51, 51);">：将文本标记与Q</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">拼接后通过自注意力层。</font>
    - <font style="color:rgb(51, 51, 51);">输出：与文本对齐的视觉特征 Zq∈R</font><sup><font style="color:rgb(51, 51, 51);">Nq×d</font></sup><font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:#74B602;">Q-Former学到了什么：</font>**可视化了MLLM中Q-former训练后的输出，验证了**<font style="color:#ED740C;">Q-former确实是在视觉语义级别的压缩</font>**。下图可视化了MLLM中训练好的Q-former的输出，高亮了每个query token相对于原始图片patch的相关性矩阵。我们可以看到，**<font style="color:#ED740C;">将576 image tokens压缩成64 query tokens，每个query token在负责不同的visual concepts，包括不同的objects、attributes和background等等</font>**。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741864585512-f1209667-aa4c-4ef0-a0d4-ded42d069dc1.png)

3. **语言模型（冻结）**：
    - <font style="color:rgb(51, 51, 51);">可选OPT、Flan-T5等，接收Zq</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">作为视觉前缀（visual prompt）生成文本。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

<font style="color:rgb(51, 51, 51);">BLIP2 的训练分为两个阶段，</font>**<font style="color:rgb(51, 51, 51);">逐步解冻不同模块参数</font>**<font style="color:rgb(51, 51, 51);">以实现高效学习：</font><font style="color:rgb(255, 255, 255);">制</font>

| **阶段** | **目标** | **冻结模块** | **训练模块** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">Stage1</font>** | <font style="color:rgb(51, 51, 51);">视觉-语言表示对齐</font> | <font style="color:rgb(51, 51, 51);">图像编码器、语言模型</font> | <font style="color:rgb(51, 51, 51);">Q-Former</font> |
| **<font style="color:rgb(51, 51, 51);">Stage2</font>** | <font style="color:rgb(51, 51, 51);">视觉到语言的生成能力学习</font> | <font style="color:rgb(51, 51, 51);">图像编码器</font> | <font style="color:rgb(51, 51, 51);">Q-Former + 语言模型（可选）</font> |


**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">Stage1：视觉-语言联合表示学习</font>**

**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：让 Q-Former 学会从图像中提取与文本对齐的特征表示，多任务联合训练，同时使用三种预训练任务，共享 Q-Former 参数：</font>

+ **图像-文本对比学习（Image-Text Contrastive Learning, ITC）**
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：对比图像特征与文本特征相似度</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074304341-6d649817-383a-478b-b27d-7ab7bad5d899.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 s(I,T)为图像-文本相似度，τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 为温度系数</font>

+ **图像-文本匹配（Image-Text Matching, ITM）**
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：二分类判断图像-文本对是否匹配</font>
    - **<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">正样本：原始配对文本</font>
        * <font style="color:rgb(51, 51, 51);">负样本：通过 ITC 相似度选择最难的负样本（Hard Negative Mining）</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：二元交叉熵损失</font>
+ **图像描述生成（Image Captioning）**
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：以图像特征为条件生成文本描述</font>
    - **<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">：使用因果掩码的交叉注意力机制</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：交叉熵损失</font>



**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">Stage2：视觉到语言生成学习</font>**

**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：将视觉特征适配到语言模型的输入空间，实现视觉条件文本生成。</font>

1. **<font style="color:rgb(51, 51, 51);">特征投影</font>**

<font style="color:rgb(51, 51, 51);">通过线性层将 Q-Former 输出的视觉特征 Zq</font>_<font style="color:rgb(51, 51, 51);">Zq</font>_<font style="color:rgb(51, 51, 51);"> 映射到语言模型的输入空间：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074416797-8395e48e-302f-4c9b-9bd4-dfe863726f81.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074430494-8000b04a-a5af-4779-b625-26f8d65d0420.png)<font style="color:rgb(51, 51, 51);">为可学习投影矩阵</font>

2. **<font style="color:rgb(51, 51, 51);">生成式预训练</font>**
    - **<font style="color:rgb(51, 51, 51);">输入构造</font>**<font style="color:rgb(51, 51, 51);">：将投影后的视觉特征作为前缀（Visual Prompt）拼接到语言模型输入前</font>
    - **<font style="color:rgb(51, 51, 51);">训练任务</font>**<font style="color:rgb(51, 51, 51);">：基于视觉条件的文本生成（Captioning、VQA 等）</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：标准语言模型的自回归损失  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074437873-ff037058-da54-4a67-8e6c-95d6f8f2a84c.png)
3. **<font style="color:rgb(51, 51, 51);">语言模型适配</font>**
    - **<font style="color:rgb(51, 51, 51);">OPT/T5 处理差异</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">对于</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">OPT</font>**<font style="color:rgb(51, 51, 51);">（自回归模型）：直接输入视觉前缀</font>
        * <font style="color:rgb(51, 51, 51);">对于</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">T5</font>**<font style="color:rgb(51, 51, 51);">（编码器-解码器）：视觉特征仅输入解码器</font>
    - **<font style="color:rgb(51, 51, 51);">参数冻结策略</font>**<font style="color:rgb(51, 51, 51);">：默认冻结语言模型参数，但支持部分微调（如 LoRA）</font>

  
**<font style="background-color:#D9EAFC;">训练技巧与优化</font>**

1. **Bootstrapping 数据增强**
    - <font style="color:rgb(51, 51, 51);">使用预训练模型（如 BLIP）为噪声图像生成伪文本标签</font>
    - <font style="color:rgb(51, 51, 51);">通过质量过滤（Quality Filtering）保留高置信度样本</font>
2. **混合精度训练**
    - <font style="color:rgb(51, 51, 51);">使用 FP16/混合精度降低显存占用</font>
    - <font style="color:rgb(51, 51, 51);">梯度缩放（Gradient Scaling）防止下溢出</font>
3. **学习率策略**
    - <font style="color:rgb(51, 51, 51);">Stage1 使用余弦衰减调度（Cosine Decay）</font>
    - <font style="color:rgb(51, 51, 51);">Stage2 采用线性 warmup（1% 训练步数）</font>
4. **硬件优化**
    - <font style="color:rgb(51, 51, 51);">ZeRO-2 数据并行（DeepSpeed）</font>
    - <font style="color:rgb(51, 51, 51);">梯度检查点（Gradient Checkpointing）节省显存</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">高效利用预训练模型，避免从头训练。</font>
+ <font style="color:rgb(51, 51, 51);">参数效率高，训练成本仅为传统方法的1/10。</font>
+ <font style="color:rgb(51, 51, 51);">支持多种LLM（OPT、T5、Flan-T5）和视觉编码器。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">依赖预训练模型性能，无法微调视觉/语言模型。</font>
+ <font style="color:rgb(51, 51, 51);">多模态推理能力受限于Q-Former的表示能力。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像描述生成</font>**<font style="color:rgb(51, 51, 51);">（Image Captioning）</font>
2. **<font style="color:rgb(51, 51, 51);">视觉问答</font>**<font style="color:rgb(51, 51, 51);">（VQA）</font>
3. **<font style="color:rgb(51, 51, 51);">多模态对话系统</font>**
4. **<font style="color:rgb(51, 51, 51);">图像检索与文本检索</font>**
5. **<font style="color:rgb(51, 51, 51);">零样本视觉推理</font>**

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">部分参数微调</font>**<font style="color:rgb(51, 51, 51);">：对语言模型或图像编码器进行LoRA等轻量级微调。</font>
2. **<font style="color:rgb(51, 51, 51);">增强Q-Former容量</font>**<font style="color:rgb(51, 51, 51);">：增加层数或查询数量。</font>
3. **<font style="color:rgb(51, 51, 51);">引入更强大的预训练模型</font>**<font style="color:rgb(51, 51, 51);">：如PaLM作为LLM、ViT-G作为图像编码器。</font>
4. **<font style="color:rgb(51, 51, 51);">动态查询调整</font>**<font style="color:rgb(51, 51, 51);">：根据输入动态生成查询向量。</font>

  


:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
class QFormer(nn.Module):
    def __init__(self, num_queries=32, dim=768, num_heads=12):
        super().__init__()
        self.queries = nn.Parameter(torch.randn(num_queries, dim))
        self.cross_attn = nn.MultiheadAttention(dim, num_heads)
        self.self_attn = nn.MultiheadAttention(dim, num_heads)
        
    def forward(self, image_features, text_features):
        # 图像-查询交互
        visual_embeds, _ = self.cross_attn(
            self.queries.unsqueeze(1), 
            image_features.transpose(0, 1), 
            image_features.transpose(0, 1)
        )
        
        # 文本-查询交互
        combined = torch.cat([visual_embeds, text_features.transpose(0, 1)], dim=0)
        output, _ = self.self_attn(combined, combined, combined)
        return output.transpose(0, 1)

```

```python
import torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Blip2Processor, Blip2ForConditionalGeneration

# 示例：使用HuggingFace预训练模型
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载预训练模型
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
model.to(device)

# 处理输入
image = ...  # PIL Image
questions = ["Describe this image in detail."]

# 生成回答
inputs = processor(images=image, text=questions, return_tensors="pt").to(device, torch.float16)
output_ids = model.generate(**inputs, max_new_tokens=100)
answer = processor.decode(output_ids[0], skip_special_tokens=True)
print(answer)

```

```python
import torch
from torch import nn
from transformers import AutoModel

class BLIP2Trainer(nn.Module):
    def __init__(self, image_encoder, q_former, text_decoder):
        super().__init__()
        self.image_encoder = image_encoder  # 冻结参数
        self.q_former = q_former
        self.text_decoder = text_decoder    # 冻结参数
        
        # 投影层
        self.visual_proj = nn.Linear(q_former.dim, text_decoder.config.hidden_size)
        
    def forward(self, images, text_ids):
        # Stage1 前向
        with torch.no_grad():
            image_features = self.image_encoder(images)  # (B, N, D_img)
            
        # Q-Former 处理
        query_outputs = self.q_former(
            image_features, 
            text_embeds=self.text_decoder.get_input_embeddings()(text_ids)
        )  # (B, N_q, D_q)
        
        # Stage2 投影
        visual_embeds = self.visual_proj(query_outputs)  # (B, N_q, D_lm)
        
        # 语言模型生成
        outputs = self.text_decoder(
            input_ids=text_ids,
            inputs_embeds=visual_embeds,
            attention_mask=...,
        )
        return outputs

# 训练循环示例
model = BLIP2Trainer(...)
optimizer = torch.optim.AdamW(model.q_former.parameters(), lr=1e-4)

for images, texts in dataloader:
    # 计算多任务损失
    itc_loss = compute_itc(image_features, text_embeds)
    itm_loss = compute_itm(image_features, text_embeds)
    cap_loss = model(images, text_ids).loss
    
    total_loss = itc_loss + itm_loss + cap_loss
    total_loss.backward()
    optimizer.step()

```

## INSTRUCT-BLIP
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：多模态模型旨在融合视觉和语言信息，完成跨模态任务（如图像描述、视觉问答等）。BLIP（Bootstrapping Language-Image Pre-training）通过联合训练视觉编码器和文本解码器，显著提升了多模态任务性能。然而，传统模型在</font>**<font style="color:rgb(51, 51, 51);">灵活遵循多样化指令</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">零样本任务泛化</font>**<font style="color:rgb(51, 51, 51);">方面存在局限。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">Instruct-BLIP</font>**<font style="color:rgb(51, 51, 51);"> 应运而生，结合</font>**<font style="color:rgb(51, 51, 51);">指令微调（Instruction Tuning）</font>**<font style="color:rgb(51, 51, 51);"> 技术，赋予模型根据自然语言指令动态调整行为的能力，使其能够处理更广泛的任务（如对话、推理等），无需针对每个任务单独训练。</font>

:::

<font style="color:rgb(0, 0, 0);">基于Blip2模型微调，</font>**<font style="color:#74B602;">把指令加到Q-Former中去，让图片也能看到指令。</font>**

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">指令驱动的多任务学习</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">将不同任务（VQA、图像描述、对话等）统一为“指令-输出”格式，增强模型对任务意图的理解。</font>
2. **<font style="color:rgb(51, 51, 51);">轻量级适配器设计</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">在视觉编码器和文本解码器之间插入</font>**<font style="color:rgb(51, 51, 51);">Q-Former（Query Transformer）</font>**<font style="color:rgb(51, 51, 51);">，仅微调解码器和适配器参数，大幅降低训练成本。</font>
3. **<font style="color:rgb(51, 51, 51);">混合指令数据集构建</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">整合26个公开数据集，通过模板将其转化为指令形式，覆盖多样化任务类型。</font>
4. **<font style="color:rgb(51, 51, 51);">零样本泛化能力</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">通过指令微调，模型可处理未见过的任务描述，如根据新指令生成特定风格的图像描述。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">来源</font>**<font style="color:rgb(51, 51, 51);">：26个公开数据集，包括：</font>
    - **<font style="color:rgb(51, 51, 51);">VQA类</font>**<font style="color:rgb(51, 51, 51);">：VQA v2、OK-VQA、A-OKVQA</font>
    - **<font style="color:rgb(51, 51, 51);">图像描述类</font>**<font style="color:rgb(51, 51, 51);">：COCO、TextCaps</font>
    - **<font style="color:rgb(51, 51, 51);">视觉推理类</font>**<font style="color:rgb(51, 51, 51);">：NLVR2、ScienceQA</font>
    - **<font style="color:rgb(51, 51, 51);">对话类</font>**<font style="color:rgb(51, 51, 51);">：LLaVA-Instruct</font>
+ **<font style="color:rgb(51, 51, 51);">处理方式</font>**<font style="color:rgb(51, 51, 51);">：将每个样本转换为“</font>**<font style="color:rgb(51, 51, 51);">指令-输入-输出</font>**<font style="color:rgb(51, 51, 51);">”三元组。</font>

```python
示例：
指令：请描述这张图片中人物的动作。
输入：图像 + 文本“图中的人在做什么？”
输出：一个人在骑自行车。
```

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074129337-897c5c05-f29d-4941-8bd7-664d1e733e93.png)

+ **<font style="color:rgb(51, 51, 51);">视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：ViT（Vision Transformer）或 CLIP-ViT，提取图像特征。</font>
+ **<font style="color:rgb(51, 51, 51);">Q-Former</font>**<font style="color:rgb(51, 51, 51);">（核心创新）：</font>
    - <font style="color:rgb(51, 51, 51);">通过可学习的查询向量（Query Vectors）与图像特征交互，生成与任务相关的视觉特征。</font>
    - <font style="color:rgb(51, 51, 51);">包含跨模态注意力层，融合文本指令与视觉信息。</font>
+ **<font style="color:rgb(51, 51, 51);">文本解码器</font>**<font style="color:rgb(51, 51, 51);">：Flan-T5 或 Vicuna，根据指令生成文本输出。</font>
+ **<font style="color:rgb(51, 51, 51);">参数冻结策略</font>**<font style="color:rgb(51, 51, 51);">：仅训练Q-Former和文本解码器，视觉编码器保持冻结。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">预训练阶段</font>**<font style="color:rgb(51, 51, 51);">（可选）：</font>
    - <font style="color:rgb(51, 51, 51);">使用图像-文本对数据（如COCO）训练视觉编码器和Q-Former，学习基础跨模态对齐。</font>
2. **<font style="color:rgb(51, 51, 51);">指令微调阶段</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：图像 + 文本指令（如“请描述图中场景”）。</font>
    - **<font style="color:rgb(51, 51, 51);">输出</font>**<font style="color:rgb(51, 51, 51);">：目标文本（如“阳光下的海滩上有椰子树”）。</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：标准交叉熵损失，优化生成文本与真实标签的匹配度。</font>
    - **<font style="color:rgb(51, 51, 51);">训练细节</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">Batch size：128</font>
        * <font style="color:rgb(51, 51, 51);">学习率：1e-5（解码器）、3e-5（Q-Former）</font>
        * <font style="color:rgb(51, 51, 51);">优化器：AdamW</font>
        * <font style="color:rgb(51, 51, 51);">训练周期：3-5 epochs</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">多任务统一框架，减少任务特定设计。</font>
    - <font style="color:rgb(51, 51, 51);">零样本泛化能力强，适应新指令。</font>
    - <font style="color:rgb(51, 51, 51);">训练高效，仅微调部分参数。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">依赖大量指令数据构造。</font>
    - <font style="color:rgb(51, 51, 51);">复杂推理任务（如多步数学推理）性能有限。</font>
    - <font style="color:rgb(51, 51, 51);">图像分辨率固定（如224x224），细节信息可能丢失。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉问答</font>**<font style="color:rgb(51, 51, 51);">：回答关于图像内容的复杂问题。</font>
+ **<font style="color:rgb(51, 51, 51);">教育辅助</font>**<font style="color:rgb(51, 51, 51);">：根据教材插图生成题目解析。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态对话</font>**<font style="color:rgb(51, 51, 51);">：结合图像与文本进行自然对话。</font>
+ **<font style="color:rgb(51, 51, 51);">内容生成</font>**<font style="color:rgb(51, 51, 51);">：根据指令生成营销文案或故事。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：引入更多语言风格的指令模板，提升多样性。</font>
2. **<font style="color:rgb(51, 51, 51);">高分辨率处理</font>**<font style="color:rgb(51, 51, 51);">：采用图像分块策略，保留细节。</font>
3. **<font style="color:rgb(51, 51, 51);">动态参数分配</font>**<font style="color:rgb(51, 51, 51);">：根据任务复杂度调整Q-Former参数量。</font>
4. **<font style="color:rgb(51, 51, 51);">强化学习</font>**<font style="color:rgb(51, 51, 51);">：通过人类反馈（RLHF）优化生成结果。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# 加载预训练模型与处理器
processor = Blip2Processor.from_pretrained("Salesforce/instructblip-flan-t5-xxl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/instructblip-flan-t5-xxl")

# 示例输入
image = Image.open("beach.jpg").convert("RGB")
instruction = "请描述这张图片中的场景。"

# 预处理
inputs = processor(
    images=image,
    text=instruction,
    return_tensors="pt",
    padding="max_length",
    max_length=32
)

# 生成输出
output_ids = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.7
)

# 解码结果
result = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
print(result)  # 输出：图片展示了一个阳光明媚的海滩，沙滩上有几棵椰子树...

```



# 
