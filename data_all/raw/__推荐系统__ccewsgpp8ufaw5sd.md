# 🔟 推荐系统

<!-- source: yuque://zhongxian-iiot9/hlyypb/ccewsgpp8ufaw5sd -->

# <font style="color:rgb(51, 51, 51);">推荐系统</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">推荐系统（Recommendation System）是一种信息过滤工具，通过分析用户行为、物品特征和上下文信息，预测用户对物品的偏好，广泛应用于电商、社交媒体、视频平台等领域。</font>

:::

```plain
推荐系统
├── **召回阶段（Recall）**
│   ├── 协同过滤（基于用户/物品的协同）
│   └── 双塔模型（用户塔 & 物品塔的向量化召回）
│
└── **排序阶段（Ranking）**
    ├── 精排模型（精准排序）
    │   ├── Wide&Deep（记忆与泛化结合）
    │   ├── DeepFM（Wide&Deep + 因子分解机）
    │   ├── DIN（用户兴趣注意力网络）
    │   └── MMoE（多任务学习）
    │── 粗排模型
    └── 重排模型  
```

| **阶段** | **输入规模** | **输出规模** | **模型复杂度** | **核心目标** | **典型优化指标** |
| --- | --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">召回</font> | <font style="color:rgb(51, 51, 51);">百万级</font> | <font style="color:rgb(51, 51, 51);">千级</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">覆盖潜在相关物品</font> | <font style="color:rgb(51, 51, 51);">召回率、覆盖率</font> |
| <font style="color:rgb(51, 51, 51);">粗排</font> | <font style="color:rgb(51, 51, 51);">千级</font> | <font style="color:rgb(51, 51, 51);">百级</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">初步筛选高相关候选</font> | <font style="color:rgb(51, 51, 51);">AUC、CTR</font> |
| <font style="color:rgb(51, 51, 51);">精排</font> | <font style="color:rgb(51, 51, 51);">百级</font> | <font style="color:rgb(51, 51, 51);">十~百级</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">精准个性化排序</font> | <font style="color:rgb(51, 51, 51);">CTR、CVR、GMV</font> |
| <font style="color:rgb(51, 51, 51);">重排</font> | <font style="color:rgb(51, 51, 51);">十~百级</font> | <font style="color:rgb(51, 51, 51);">十~百级</font> | <font style="color:rgb(51, 51, 51);">灵活（规则/模型）</font> | <font style="color:rgb(51, 51, 51);">优化列表整体效果</font> | <font style="color:rgb(51, 51, 51);">多样性、停留时长、留存率</font> |


:::color5
**<font style="color:#601BDE;">1.推荐系统分类</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">基于内容的推荐</font>**<font style="color:rgb(51, 51, 51);">（Content-Based）  
</font><font style="color:rgb(51, 51, 51);">原理：根据用户历史行为分析物品特征，推荐相似物品。  
</font><font style="color:rgb(51, 51, 51);">核心：特征提取（如文本TF-IDF、图像CNN）、用户画像建模。</font>
2. **<font style="color:rgb(51, 51, 51);">协同过滤</font>**<font style="color:rgb(51, 51, 51);">（Collaborative Filtering, CF）  
</font><font style="color:rgb(51, 51, 51);">原理：利用群体行为数据（用户-物品交互矩阵），找到相似用户或物品进行推荐。  
</font><font style="color:rgb(51, 51, 51);">类型：</font>
    - <font style="color:rgb(51, 51, 51);">User-based CF：推荐相似用户喜欢的物品</font>
    - <font style="color:rgb(51, 51, 51);">Item-based CF：推荐与用户历史物品相似的物品</font>
3. **<font style="color:rgb(51, 51, 51);">混合推荐</font>**<font style="color:rgb(51, 51, 51);">（Hybrid）  
</font><font style="color:rgb(51, 51, 51);">结合内容推荐和协同过滤，如加权、级联或特征融合。</font>

:::color5
**<font style="color:#601BDE;">2.经典算法</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 矩阵分解（Matrix Factorization, MF）</font>**

+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：将用户-物品评分矩阵分解为低秩用户矩阵和物品矩阵，通过内积预测评分。</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740297076211-fddfc7e8-6c46-4000-b454-79c66bf63563.png)
+ **<font style="color:rgb(51, 51, 51);">计算步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. <font style="color:rgb(51, 51, 51);">初始化用户矩阵 U</font>_<font style="color:rgb(51, 51, 51);">U</font>_<font style="color:rgb(51, 51, 51);">和物品矩阵 V</font>
    2. <font style="color:rgb(51, 51, 51);">定义损失函数（如均方误差 + L2正则化）：</font>
    3. ![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740297087060-df994419-6387-403f-87b9-1cefd75a6805.png)
    4. <font style="color:rgb(51, 51, 51);">使用梯度下降或交替最小二乘法（ALS）优化。</font>
+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：缓解数据稀疏性，可解释性强。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：冷启动问题，难以捕捉高阶特征。</font>
+ **<font style="color:rgb(51, 51, 51);">应用场景</font>**<font style="color:rgb(51, 51, 51);">：评分预测（如MovieLens电影推荐）。</font>
+ **<font style="color:rgb(51, 51, 51);">改进方法</font>**<font style="color:rgb(51, 51, 51);">：加入偏置项（BiasSVD）、时间动态（TimeSVD++）。</font>

**<font style="color:rgb(51, 51, 51);">2. Wide & Deep 模型</font>**

+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">（Google, 2016）：结合线性模型（Wide部分）和深度神经网络（Deep部分）：</font>
    - <font style="color:rgb(51, 51, 51);">Wide：记忆用户历史行为（如交叉特征）</font>
    - <font style="color:rgb(51, 51, 51);">Deep：泛化长尾特征（如Embedding层）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740297100412-3dfab0b7-ee09-474d-83be-1382935b5f0c.png)

+ **<font style="color:rgb(51, 51, 51);">计算步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. <font style="color:rgb(51, 51, 51);">输入特征分为稀疏特征（如用户ID）和稠密特征（如年龄）。</font>
    2. <font style="color:rgb(51, 51, 51);">Wide部分使用线性模型 + 特征交叉。</font>
    3. <font style="color:rgb(51, 51, 51);">Deep部分通过Embedding + MLP提取高阶特征。</font>
    4. <font style="color:rgb(51, 51, 51);">联合训练两个部分的输出。</font>
+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：平衡记忆与泛化能力。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：特征工程依赖性强。</font>
+ **<font style="color:rgb(51, 51, 51);">应用场景</font>**<font style="color:rgb(51, 51, 51);">：Google Play应用推荐。</font>

**<font style="color:rgb(51, 51, 51);">3. 深度兴趣网络（Deep Interest Network, DIN）</font>**

+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">（阿里, 2017）：针对用户历史行为，使用注意力机制动态捕捉兴趣。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740297121468-064ecff4-50a0-41fe-9dd5-7426c4f2dd26.png)

<font style="color:rgb(51, 51, 51);">其中 a(⋅)是注意力得分，va</font>**<font style="color:rgb(51, 51, 51);"></font>**<font style="color:rgb(51, 51, 51);">是候选物品向量。</font>

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：解决用户兴趣多样性问题。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：计算复杂度高。</font>
+ **<font style="color:rgb(51, 51, 51);">应用场景</font>**<font style="color:rgb(51, 51, 51);">：电商场景（如淘宝商品推荐）。</font>

:::color5
**<font style="color:#601BDE;">3.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">冷启动问题</font>**<font style="color:rgb(51, 51, 51);">：融合内容特征（如LightFM）、使用元学习。</font>
2. **<font style="color:rgb(51, 51, 51);">多样性推荐</font>**<font style="color:rgb(51, 51, 51);">：多目标优化（如MMOE）、强化学习。</font>
3. **<font style="color:rgb(51, 51, 51);">实时性</font>**<font style="color:rgb(51, 51, 51);">：在线学习（如FTRL）、流式计算。</font>
4. **<font style="color:rgb(51, 51, 51);">可解释性</font>**<font style="color:rgb(51, 51, 51);">：注意力机制可视化、因果推理。</font>

:::color5
**<font style="color:#601BDE;">4.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.optim as optim

class MatrixFactorization(nn.Module):
    def __init__(self, n_users, n_items, latent_dim):
        super().__init__()
        self.user_emb = nn.Embedding(n_users, latent_dim)
        self.item_emb = nn.Embedding(n_items, latent_dim)
        self.user_bias = nn.Embedding(n_users, 1)
        self.item_bias = nn.Embedding(n_items, 1)
        
    def forward(self, user, item):
        u_emb = self.user_emb(user)
        i_emb = self.item_emb(item)
        pred = (u_emb * i_emb).sum(dim=1) + self.user_bias(user).squeeze() + self.item_bias(item).squeeze()
        return pred

# 数据准备（假设已有用户-物品评分数据）
users = torch.LongTensor([0, 1, 2])  # 用户ID
items = torch.LongTensor([3, 4, 5])  # 物品ID
ratings = torch.FloatTensor([5.0, 3.5, 4.0])

# 模型训练
model = MatrixFactorization(n_users=1000, n_items=2000, latent_dim=64)
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    preds = model(users, items)
    loss = loss_fn(preds, ratings)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

```





# 搜索、广告、推荐算法的区别
:::color3
1. **<font style="color:rgb(51, 51, 51);">搜索</font>**<font style="color:rgb(51, 51, 51);">更依赖</font>**<font style="color:rgb(51, 51, 51);">文本语义理解</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">实时性优化</font>**<font style="color:rgb(51, 51, 51);">，强约束下追求精准匹配；</font>
2. **<font style="color:rgb(51, 51, 51);">广告</font>**<font style="color:rgb(51, 51, 51);">需平衡</font>**<font style="color:rgb(51, 51, 51);">多方利益博弈</font>**<font style="color:rgb(51, 51, 51);">，在经济学机制设计（如拍卖算法）上有独特要求；</font>
3. **<font style="color:rgb(51, 51, 51);">推荐</font>**<font style="color:rgb(51, 51, 51);">强调</font>**<font style="color:rgb(51, 51, 51);">用户兴趣挖掘</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">生态调控</font>**<font style="color:rgb(51, 51, 51);">，需解决数据稀疏性和马太效应问题。</font>

<font style="color:rgb(51, 51, 51);">实际系统中，三者常融合使用（如搜索广告、推荐中的广告插入），但核心目标差异决定了技术路径的分野。理解业务本质比单纯追求模型复杂度更重要。</font>

:::

| **维度** | **搜索算法** | **广告算法** | **推荐算法** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">核心目标</font>** | <font style="color:rgb(51, 51, 51);">精准匹配用户Query和结果</font> | <font style="color:rgb(51, 51, 51);">平衡用户体验与广告主收益</font> | <font style="color:rgb(51, 51, 51);">最大化用户长期兴趣满足</font> |
| **<font style="color:rgb(51, 51, 51);">输入信号</font>** | <font style="color:rgb(51, 51, 51);">Query + 用户短期意图</font> | <font style="color:rgb(51, 51, 51);">Query/上下文 + 用户画像</font> | <font style="color:rgb(51, 51, 51);">用户历史行为 + 上下文</font> |
| **<font style="color:rgb(51, 51, 51);">优化指标</font>** | <font style="color:rgb(51, 51, 51);">相关性、点击率、时效性</font> | <font style="color:rgb(51, 51, 51);">eCPM (CTR×Bid)、ROI</font> | <font style="color:rgb(51, 51, 51);">停留时长、CTR、多样性</font> |
| **<font style="color:rgb(51, 51, 51);">约束条件</font>** | <font style="color:rgb(51, 51, 51);">结果权威性、搜索时效性</font> | <font style="color:rgb(51, 51, 51);">广告主预算、频次控制</font> | <font style="color:rgb(51, 51, 51);">内容冷启动、生态健康度</font> |
| **<font style="color:rgb(51, 51, 51);">数据分布</font>** | <font style="color:rgb(51, 51, 51);">长尾Query占比高</font> | <font style="color:rgb(51, 51, 51);">头部广告主主导流量</font> | <font style="color:rgb(51, 51, 51);">用户行为稀疏性问题显著</font> |


## <font style="color:rgb(51, 51, 51);">2.1 四阶段技术对比</font>
#### <font style="color:rgb(51, 51, 51);">1.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">召回阶段（Recall）</font>**
+ **搜索**：
    - <font style="color:rgb(51, 51, 51);">倒排索引 + BM25文本匹配</font>
    - <font style="color:rgb(51, 51, 51);">Query扩展（同义词、语义改写）</font>
    - <font style="color:rgb(51, 51, 51);">实时性要求高（百毫秒内响应）</font>
+ **广告**：
    - <font style="color:rgb(51, 51, 51);">广告定向标签匹配（人群/兴趣/地域）</font>
    - <font style="color:rgb(51, 51, 51);">预算过滤（淘汰预算耗尽的广告主）</font>
    - <font style="color:rgb(51, 51, 51);">粗粒度eCPM预估（CTR×Bid初筛）</font>
+ **推荐**：
    - <font style="color:rgb(51, 51, 51);">多路召回（协同过滤、Embedding向量、热点内容）</font>
    - <font style="color:rgb(51, 51, 51);">用户实时行为触发召回（如最近点击的类别）</font>
    - <font style="color:rgb(51, 51, 51);">多样性控制（避免单一类型内容主导）</font>

#### <font style="color:rgb(51, 51, 51);">2.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">粗排（Pre-Ranking）</font>**
+ **搜索**：
    - <font style="color:rgb(51, 51, 51);">特征工程：TF-IDF、Query-Doc文本匹配分</font>
    - <font style="color:rgb(51, 51, 51);">轻量模型：LR或浅层NN快速筛选Top 1000</font>
+ **广告**：
    - <font style="color:rgb(51, 51, 51);">校准eCPM计算：CTR预估模型（浅层GBDT） × Bid</font>
    - <font style="color:rgb(51, 51, 51);">流量分配初筛（保证中小广告主曝光机会）</font>
+ **推荐**：
    - <font style="color:rgb(51, 51, 51);">多目标融合：CTR、时长、点赞率的加权排序</font>
    - <font style="color:rgb(51, 51, 51);">用户兴趣泛化（通过用户聚类补充稀疏行为）</font>

#### <font style="color:rgb(51, 51, 51);">3.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">精排（Ranking）</font>**
+ **搜索**：
    - <font style="color:rgb(51, 51, 51);">多模态模型：BERT等预训练模型理解语义</font>
    - <font style="color:rgb(51, 51, 51);">个性化排序：融合用户历史点击偏好</font>
    - <font style="color:rgb(51, 51, 51);">权威性加权（如Wikipedia结果优先）</font>
+ **广告**：
    - <font style="color:rgb(51, 51, 51);">博弈优化：GSP竞价机制下的eCPM最大化</font>
    - <font style="color:rgb(51, 51, 51);">多目标建模：CTR、CVR、转化价值的联合预估</font>
    - <font style="color:rgb(51, 51, 51);">预算平滑：保证广告主全天均匀消耗预算</font>
+ **推荐**：
    - <font style="color:rgb(51, 51, 51);">深度模型：Wide&Deep、YouTube DNN、多任务模型</font>
    - <font style="color:rgb(51, 51, 51);">实时特征：用户当前Session内的行为序列建模</font>
    - <font style="color:rgb(51, 51, 51);">生态调控：打压低质内容、扶持新内容冷启动</font>

#### <font style="color:rgb(51, 51, 51);">4.</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">重排（Re-Ranking）</font>**
+ **搜索**：
    - <font style="color:rgb(51, 51, 51);">去重策略（合并相似结果）</font>
    - <font style="color:rgb(51, 51, 51);">本地化优化（如优先展示用户所在地商家）</font>
    - <font style="color:rgb(51, 51, 51);">多样性插入（保证结果类型覆盖）</font>
+ **广告**：
    - <font style="color:rgb(51, 51, 51);">广告位频控（同一广告主不连续出现）</font>
    - <font style="color:rgb(51, 51, 51);">品牌安全过滤（避免竞品广告相邻）</font>
    - <font style="color:rgb(51, 51, 51);">动态创意优化（替换广告图片/文案）</font>
+ **推荐**：
    - <font style="color:rgb(51, 51, 51);">混排策略：图文、视频、直播等跨类型内容平衡</font>
    - <font style="color:rgb(51, 51, 51);">探索机制：插入低曝光优质内容（Bandit算法）</font>
    - <font style="color:rgb(51, 51, 51);">上下文敏感：根据当前内容推荐关联项（如看完电影推影评）</font>

