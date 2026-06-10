# ⓵ 模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/nrg1odtusnscn02m -->

# 推荐模型
```python
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




| **模型** | **核心思想** | **适用场景** | **优点** | **缺点** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">矩阵分解</font> | <font style="color:rgb(51, 51, 51);">隐语义分解</font> | <font style="color:rgb(51, 51, 51);">显式评分预测</font> | <font style="color:rgb(51, 51, 51);">缓解数据稀疏</font> | <font style="color:rgb(51, 51, 51);">冷启动问题严重</font> |
| <font style="color:rgb(51, 51, 51);">协同过滤</font> | <font style="color:rgb(51, 51, 51);">群体行为相似</font> | <font style="color:rgb(51, 51, 51);">中小规模推荐</font> | <font style="color:rgb(51, 51, 51);">无需特征工程</font> | <font style="color:rgb(51, 51, 51);">数据稀疏时失效</font> |
| <font style="color:rgb(51, 51, 51);">Wide & Deep</font> | <font style="color:rgb(51, 51, 51);">记忆+泛化联合训练</font> | <font style="color:rgb(51, 51, 51);">大规模稀疏特征</font> | <font style="color:rgb(51, 51, 51);">平衡记忆与泛化</font> | <font style="color:rgb(51, 51, 51);">依赖人工特征设计</font> |
| <font style="color:rgb(51, 51, 51);">DIN</font> | <font style="color:rgb(51, 51, 51);">动态兴趣注意力</font> | <font style="color:rgb(51, 51, 51);">长行为序列CTR预估</font> | <font style="color:rgb(51, 51, 51);">捕捉多样化兴趣</font> | <font style="color:rgb(51, 51, 51);">计算复杂度高</font> |
| <font style="color:rgb(51, 51, 51);">DeepFM</font> | <font style="color:rgb(51, 51, 51);">自动捕捉低阶和高阶特征交互。</font> | <font style="color:rgb(51, 51, 51);">适用于点击率预估（CTR）等任务</font> | <font style="color:rgb(51, 51, 51);">无需人工设计特征交叉（如Wide & Deep）。</font> | <font style="color:rgb(51, 51, 51);">计算复杂度较高，尤其在高维稀疏场景。</font> |


# 召回模型
## 2.1 矩阵分解
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">将用户-物品评分矩阵 R∈R</font><sup><font style="color:rgb(51, 51, 51);">m×n</font></sup><font style="color:rgb(51, 51, 51);">分解为低维用户矩阵 U∈R</font><sup><font style="color:rgb(51, 51, 51);">m×k</font></sup><font style="color:rgb(51, 51, 51);">和物品矩阵 V∈R</font><sup><font style="color:rgb(51, 51, 51);">n×k</font></sup><font style="color:rgb(51, 51, 51);">，通过内积近似预测评分：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298104961-3c78a1e6-ed3d-4dcd-907b-240e8a740d80.png)

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">初始化</font>**<font style="color:rgb(51, 51, 51);">：随机生成用户矩阵</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">U</font>_<font style="color:rgb(51, 51, 51);">U</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">和物品矩阵</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">V</font>_<font style="color:rgb(51, 51, 51);">V</font>_<font style="color:rgb(51, 51, 51);">。</font>
2. **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：最小化观测评分的均方误差，加入L2正则化防止过拟合：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298146767-5b9769aa-6432-4d5a-9dea-8f17bd5e4745.png)

3. **<font style="color:rgb(51, 51, 51);">优化</font>**<font style="color:rgb(51, 51, 51);">：使用梯度下降或交替最小二乘法（ALS）更新参数。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：缓解数据稀疏性，隐式特征捕捉能力强。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：冷启动问题突出，无法处理非评分行为（如点击）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">显式反馈数据（如电影评分预测）。</font>
+ <font style="color:rgb(51, 51, 51);">经典数据集：MovieLens、Netflix Prize。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">BiasSVD</font>**<font style="color:rgb(51, 51, 51);">：引入用户偏置 bi</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">和物品偏置 bj：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298173068-f101331c-8ede-41dd-bac8-7305b90efb5a.png)
+ **<font style="color:rgb(51, 51, 51);">时间动态</font>**<font style="color:rgb(51, 51, 51);">：考虑用户兴趣随时间变化（TimeSVD++）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn

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

# 示例数据
users = torch.LongTensor([0, 1, 2])
items = torch.LongTensor([3, 4, 5])
ratings = torch.FloatTensor([5.0, 3.5, 4.0])

# 训练过程
model = MatrixFactorization(n_users=1000, n_items=2000, latent_dim=64)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

for epoch in range(100):
    preds = model(users, items)
    loss = loss_fn(preds, ratings)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

```



## 2.2 协同过滤
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">基于群体行为数据，利用用户或物品的相似性进行推荐：</font>

+ **<font style="color:rgb(51, 51, 51);">User-based CF</font>**<font style="color:rgb(51, 51, 51);">：推荐相似用户喜欢的物品。</font>
+ **<font style="color:rgb(51, 51, 51);">Item-based CF</font>**<font style="color:rgb(51, 51, 51);">：推荐与用户历史物品相似的物品。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">相似度计算</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">余弦相似度</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298252930-c746ae82-1e91-4947-bb6b-73e56338d6d0.png)
    - **<font style="color:rgb(51, 51, 51);">皮尔逊相关系数</font>**<font style="color:rgb(51, 51, 51);">：中心化后的余弦相似度。</font>
2. **<font style="color:rgb(51, 51, 51);">邻居选择</font>**<font style="color:rgb(51, 51, 51);">：选取Top-K相似用户或物品。</font>
3. **<font style="color:rgb(51, 51, 51);">评分预测</font>**<font style="color:rgb(51, 51, 51);">：加权平均邻居的评分。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：无需物品特征，直观易实现。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：数据稀疏时效果差，计算复杂度高。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">用户/物品数量适中的中小型系统。</font>
+ <font style="color:rgb(51, 51, 51);">冷启动缓解场景（结合内容过滤）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">Slope One算法</font>**<font style="color:rgb(51, 51, 51);">：简化加权预测过程。</font>
+ **<font style="color:rgb(51, 51, 51);">混合模型</font>**<font style="color:rgb(51, 51, 51);">：与内容推荐结合（如LightFM）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 用户-物品评分矩阵（示例）
R = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 2, 4, 0],
    [0, 0, 5, 2]
])

# 计算用户相似度矩阵
user_sim = cosine_similarity(R)

def predict_rating(user_id, item_id, k=2):
    # 找到最相似的k个用户（排除自己）
    similar_users = np.argsort(-user_sim[user_id])[1:k+1]
    # 计算加权评分
    weighted_sum = np.sum([user_sim[user_id, u] * R[u, item_id] for u in similar_users])
    sim_sum = np.sum([user_sim[user_id, u] for u in similar_users])
    return weighted_sum / sim_sum if sim_sum != 0 else 0

# 预测用户0对物品2的评分
print(predict_rating(0, 2))  # 输出示例：3.2
```

## 2.3 双塔模型
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">双塔模型是推荐系统中应用非常广泛的模型，如果说只用一个模型，那么非双塔莫属，既可以召回，又可以排序。</font>

:::

:::color3
**简介：**双塔模型经典又简单，就是NLP领域的 query 和 document，推荐领域的 user 和 item，多模态检索领域的图像和文字等，都可以用双塔表示，分别把两个领域的特征编码成一个向量，然后向量相似度进行召回。

参考：[https://zhuanlan.zhihu.com/p/335112207](https://zhuanlan.zhihu.com/p/335112207)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744187067192-b85161fb-efa0-4ab8-8710-e5db23841a6c.png)

| **维度** | **双塔召回模型** | **双塔精排（CTR）模型** |
| --- | --- | --- |
| **<font style="color:rgb(13, 18, 57);">目标</font>** | <font style="color:rgb(13, 18, 57);">高效初筛候选物品池</font> | <font style="color:rgb(13, 18, 57);">精准计算正样本概率</font> |
| **<font style="color:rgb(13, 18, 57);">输出</font>** | <font style="color:rgb(13, 18, 57);">特征嵌入向量及相似度</font> | <font style="color:rgb(13, 18, 57);">点击概率（二值分类）</font> |
| **<font style="color:rgb(13, 18, 57);">训练方式</font>** | <font style="color:rgb(13, 18, 57);">使用对比损失（Contrastive）</font> | <font style="color:rgb(13, 18, 57);">交叉熵损失（Cross-Entropy）</font> |
| **<font style="color:rgb(13, 18, 57);">特征</font>** | <font style="color:rgb(13, 18, 57);">通常不需复杂交互特征</font> | <font style="color:rgb(13, 18, 57);">可引入标签特征（如历史行为）</font> |
| **<font style="color:rgb(13, 18, 57);">速度</font>** | <font style="color:rgb(13, 18, 57);">高（计算相似度矩阵快速）</font> | <font style="color:rgb(13, 18, 57);">低（DNN需处理复杂特征组合）</font> |


:::color5
**<font style="color:#601BDE;">1.模型特征</font>**

:::

<font style="color:rgb(25, 27, 31);">模型特征包含用户特征、上下文特征和物料特征三种，其中用户特征和上下文特征用于用户塔，物料特征用于物料塔。</font>

+ **<font style="color:rgb(25, 27, 31);">用户特征</font>**<font style="color:rgb(25, 27, 31);">：通常有用户id，用户历史点击、观看、点赞历史，用户性别、年龄、地域等profile信息，用户消费历史兴趣画像等</font>
+ **<font style="color:rgb(25, 27, 31);">上下文特征</font>**<font style="color:rgb(25, 27, 31);">：通常有手机品牌、系统、版本等信息，访问频道，当前网络情况，定位信息等</font>
+ **<font style="color:rgb(25, 27, 31);">物料特征</font>**<font style="color:rgb(25, 27, 31);">：通常有物料id，物料作者id，物料一级二级分类、关键词、主题等挖掘信息，预训练语义向量，物料的统计类特征</font>

<font style="color:rgb(25, 27, 31);">其他信息还包括预训练的id向量等。</font>

:::color5
**<font style="color:#601BDE;">2.样本构建</font>**

:::

+ <font style="color:rgb(25, 27, 31);">正样本一般设定为用户的正向行为，比如点击、点赞、观看等。</font>
+ <font style="color:rgb(25, 27, 31);">负样本的讨论比较多，可以分为一下几种情况：</font>
1. <font style="color:rgb(25, 27, 31);">曝光未点击  
</font><font style="color:rgb(25, 27, 31);">排序算法一般采用曝光未点击作为负样本，如果训练一个双塔模型，采用曝光未点击，最后是能够达到跟排序模型类似的效果的。召回的效果指标也不差，更可以当做粗排和召回中的排序来用。</font>
2. <font style="color:rgb(25, 27, 31);">随机负采样  
</font><font style="color:rgb(25, 27, 31);">使用比较多的召回算法中用到的随机负采样，比较经典的论文就是2016年的</font>[<font style="color:rgb(9, 64, 142);">YouTubeDNN</font>](https://zhida.zhihu.com/search?content_id=221853110&content_type=Article&match_order=1&q=YouTubeDNN&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。在全量item中随机选取一定数据的item，有的是完全随机，也可以按照出现频率做选择，出现越多选中概率越大。</font>
3. <font style="color:rgb(25, 27, 31);">粗排样本  
</font><font style="color:rgb(25, 27, 31);">有从链路一致性角度考虑，粗排的学习目标应该是精排，为了跟精排统一，粗排的负样本应该是精排排名靠后的样本，而不是曝光未点击。因此，精排中排名靠后的样本，可以作为粗排的负样本。  
</font><font style="color:rgb(25, 27, 31);">from：</font>[https://zhuanlan.zhihu.com/p/446977887](https://zhuanlan.zhihu.com/p/446977887)<font style="color:rgb(25, 27, 31);"></font>
4. <font style="color:rgb(25, 27, 31);">batch内负采样  
</font><font style="color:rgb(25, 27, 31);">YouTube 2019 出的一篇论文，采用的是batch 内负采样。文章使用所有正向行为比如点击当做正样本，然后再batch内负采样作为负样本，其关注点是如果batch内都是正样本，但是却过多的当成了负样本，而且正样本出现得越多，当成负样本的概率越大，很不合理。文中对负样本重要度做了一个平衡，根据样本出现的频率，出现的越多，重要度越低，这样能够把流行的item的重要度降低下来。  
</font><font style="color:rgb(25, 27, 31);">from: Sampling-bias-corrected neural modeling for large corpus item recommendations  
</font><font style="color:rgb(25, 27, 31);">Google Play的一篇双塔采用的全局随机负采样和batch内负采样混合采样，既能保证batch内采样的高效训练，又能把全局长尾item作为负样本，能够训练到，而且能够设定样本分布。  
</font><font style="color:rgb(25, 27, 31);">from: </font>[https://zhuanlan.zhihu.com/p/533449018](https://zhuanlan.zhihu.com/p/533449018)<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">阿里开源的easyrec也是在batch内负采样，不过batch内既包含正样本又包含负样本，这样没有了流行正样本过多当成负样本的顾虑。可以直接进行随机batch内负采样。另外示例代码中给出的loss还能够实现了对hard样本加权的逻辑，对预测的正样本与负样本对的差值大于0的，减弱loss，反之增大loss。  
</font><font style="color:rgb(25, 27, 31);">from: </font>[https://zhuanlan.zhihu.com/p/475117993](https://zhuanlan.zhihu.com/p/475117993)<font style="color:rgb(25, 27, 31);"></font>

<font style="color:rgb(25, 27, 31);">在实际工作中，既要考虑效果又要考虑实际基础设施情况，我们在阿里的easyrec中batch负采样基础上，加上曝光未点击，能够同时获得recall@k，和AUC的同步提升。</font>

:::color5
**<font style="color:#601BDE;">3.模型训练</font>**

:::

<font style="color:rgb(25, 27, 31);">模型特征经过Embedding层后，再过多层MLP，最终输出 user 和item的Embedding，两个Embedding做点积，作为最终预估分。</font>

**召回目标：**

<font style="color:rgb(25, 27, 31);">用cosine相似度作为预估分，即对最后一层Embedding层进行l2归一化，这样预估分含义为向量角度，不受向量的模的影响。然而cosine值的至于范围仅有[-1, 1]范围，在预估分达到-2.2左右时，才能较好的拟合CTR为0.1左右的样本集合。因此，范围限制过于严格，大多会给预估值除以一个小数，比如0.2，称为温度系数，或锐度化系数。</font>

**<font style="color:rgb(25, 27, 31);">排序目标：</font>**

<font style="color:rgb(25, 27, 31);">根据不同目标，拟定不同的loss，来进行模型的优化。</font>

+ <font style="color:rgb(25, 27, 31);">点击率预估：采用交叉熵loss。</font>
+ <font style="color:rgb(25, 27, 31);">时长预估：采用MSE loss，当然时长一般需要进行log变换或者分位数变换。</font>

**<font style="color:rgb(25, 27, 31);">优化器与学习率</font>**<font style="color:rgb(25, 27, 31);">：定义好了目标函数和对应目标函数需要优化的变量之后，可以选定优化器，进行梯度下降优化了。不同优化器一般会有不同的学习率，不同的参数也会使用不同的优化器和学习率去优化。不同特征的出现频度不一样，因此，不同的特征都需要根据频度设定自己的学习率，这点非常重要，对效果影响也比较大。</font>

:::color5
**<font style="color:#601BDE;">4.优缺点</font>**

:::

**优点**

1. <font style="color:rgb(25, 27, 31);">模型原理简单，比较好实现。</font>
2. <font style="color:rgb(25, 27, 31);">模型能够使用几乎所有特征，比起单用id或单用某些属性特征的召回算法，效果较好。</font>
3. <font style="color:rgb(25, 27, 31);">模型能够使用除了交叉结构以外的所有结构（也有一些改进模型突破这点）。</font>
4. <font style="color:rgb(25, 27, 31);">能够提前预先计算 item 侧向量，线上计算复杂度小，使用近邻查找技术很容易计算百万级规模以上的物料。</font>
5. <font style="color:rgb(25, 27, 31);">可以复用排序算法的特征工程及上线流程，减少工程复杂度。</font>
6. <font style="color:rgb(25, 27, 31);">通过多种采样技术能够实现对应召回模型和粗排排序模型，模型结构、流程代码可复用。</font>
7. <font style="color:rgb(25, 27, 31);">正是由于使用了全部特征，能够实现无行为 item 的冷启动，且有这较高准确度。</font>
8. <font style="color:rgb(25, 27, 31);">可以通过模型的实时预测，实现新 item 的实时推荐，达到几乎秒级更新，比较适合新闻等对冷启动需求较强的场景。</font>

**<font style="color:rgb(25, 27, 31);">缺点</font>**

1. <font style="color:rgb(25, 27, 31);">两塔分离，造成了两塔特征不能交叉，只能等到最终向量才能交互。这个问题也是困扰双塔模式的根本问题，很多特征交叉的模型都无法使用，也导致限制了双塔的精度提升的上限。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

**<font style="color:rgb(25, 27, 31);">离线评估指标</font>**

<font style="color:rgb(25, 27, 31);">一般采用未来一段时间（一天）数据作为测试集进行评估。</font>

1. <font style="color:rgb(25, 27, 31);">AUC：不论在召回和排序模型中，AUC都是一个重要指标，在排序中更重要，针对特征维度统计的GAUC，更能在特征场景有重要意义。</font>
2. <font style="color:rgb(25, 27, 31);">Recall@K：在预测的前k个样本中，是正样本的个数。</font>
3. <font style="color:rgb(25, 27, 31);">AverageRank：对于一个正样本的1情况，随机取100个负样本，求得正样本的平均排名</font>
4. <font style="color:rgb(25, 27, 31);">NDCG: 考虑到排序不同位置的重要程度，对不同位置赋予不同权重值，得出评价分数。为了不同排名top k之间可比，使用最优DCG进行归一化，得到归一化后的评价指标。</font>

<font style="color:rgb(25, 27, 31);">参考：</font>[https://ils.unc.edu/courses/2013_spring/inls509_001/lectures/10-EvaluationMetrics.pdf](https://link.zhihu.com/?target=https%3A//ils.unc.edu/courses/2013_spring/inls509_001/lectures/10-EvaluationMetrics.pdf)

**<font style="color:rgb(25, 27, 31);">线上评估指标</font>**

<font style="color:rgb(25, 27, 31);">线上指标一般采用人均曝光、人均刷新、人均点击、点击率、人均时长、人均互动，留存等指标判定。</font>

:::color5
**<font style="color:#601BDE;">6.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class UserTower(nn.Module):
    """用户侧编码塔"""
    def __init__(self, user_feature_dim, embedding_dim):
        super().__init__()
        self.user_mlp = nn.Sequential(
            nn.Linear(user_feature_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, embedding_dim)
        )
    
    def forward(self, user_features):
        # 将用户特征稠密化并归一化输出为embedding向量
        user_emb = self.user_mlp(user_features)
        user_emb = F.normalize(user_emb, p=2, dim=1)  # L2归一化
        return user_emb

class ItemTower(nn.Module):
    """物品侧编码塔"""
    def __init__(self, item_feature_dim, embedding_dim):
        super().__init__()
        self.item_mlp = nn.Sequential(
            nn.Linear(item_feature_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, embedding_dim)
        )
    
    def forward(self, item_features):
        item_emb = self.item_mlp(item_features)
        item_emb = F.normalize(item_emb, p=2, dim=1)  # L2归一化
        return item_emb

class TwoTowerRecommender(nn.Module):
    """双塔召回模型主类"""
    def __init__(self, user_dim, item_dim, embedding_dim):
        super().__init__()
        self.user_tower = UserTower(user_dim, embedding_dim)
        self.item_tower = ItemTower(item_dim, embedding_dim)
        
    def forward(self, user_x, item_x):
        user_embed = self.user_tower(user_x)
        item_embed = self.item_tower(item_x)
        # 计算 Cosine相似度或逐元素相乘求内积
        sim_scores = (user_embed * item_embed).sum(dim=1)  # 内积形式
        return sim_scores, user_embed, item_embed
    
    def contrastive_loss(self, user_embs, item_embs, pos_indices, neg_indices):
        """
        对比损失函数（BPR loss形式）
        Args:
            user_embs: N用户向量
            item_embs: M物品向量
            pos_indices: 正样本掩码 (N x M)
            neg_indices: 负样本掩码 (N x M)
        """
        scores = user_embs @ item_embs.T  # (N x D) @ (D x M) = N x M相似矩阵
        pos_loss = (1.0 - scores[pos_indices]).clamp(min=0)  # sigmoid_u_i -1
        neg_loss = (scores[neg_indices]).clamp(min=0)
        loss = pos_loss.mean() + neg_loss.mean()
        return loss

# 初始化模型和优化器
embedding_size = 64
model = TwoTowerRecommender(user_dim=100, item_dim=200, embedding_dim=embedding_size)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 前向计算（假设输入已标准化处理）
user_batch = torch.randn(32, 100)  # 假设32用户，100维特征
item_batch = torch.randn(32, 200)  # 32物品
sim, u_embs, i_embs = model(user_batch, item_batch)

# 计算对比损失（假设pos/neg索引生成）
pos_mask = torch.eye(32,32)  # 简化示例：对角线为正样本
neg_mask = ~pos_mask
loss = model.contrastive_loss(u_embs, i_embs, pos_mask, neg_mask)
loss.backward()
optimizer.step()
```

```python

class CTR_TwoTowerModel(nn.Module):
    def __init__(self, user_dim, item_dim, hidden_dim=128):
        super().__init__()
        # 用户和物品共享编码结构，但参数不共享
        self.user_tower = nn.Sequential(
            FeatureEmbedding(user_dim),
            nn.Linear(user_dim, 64),  # 隐藏层
            nn.ReLU(),
            nn.Linear(64, hidden_dim)
        )
        self.item_tower = nn.Sequential(
            FeatureEmbedding(item_dim),
            nn.Linear(item_dim, 64),
            nn.ReLU(),
            nn.Linear(64, hidden_dim)
        )
        
        # 复合层：拼接双塔输出后进行DNN预测
        self.composite_nn = nn.Sequential(
            nn.Linear(hidden_dim*2, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)  # 输出点击率概率（logits）
        )
    
    def forward(self, user_x, item_x):
        u_emb = self.user_tower(user_x)
        i_emb = self.item_tower(item_x)
        combined = torch.cat([u_emb, i_emb], dim=1)  # 拼接特征
        logits = self.composite_nn(combined)
        return torch.sigmoid(logits.squeeze())

# 初始化与前向计算
model = CTR_TwoTowerModel(user_dim=100, item_dim=200)
user_batch = torch.rand(64, 100)
item_batch = torch.rand(64, 200)
click_prob = model(user_batch, item_batch)  # 输出64个预测概率

# 训练逻辑（假设存在标签真实值）
criterion = nn.BCELoss()
loss = criterion(click_prob, torch.randint(0,2,(64,)))  # 假标签
loss.backward()
```

### 双塔多目标模型
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744187402903-04b9392a-46e4-4efb-a31a-4944662533ac.png)

<font style="color:rgb(25, 27, 31);">双塔模型比单塔实现多目标要复杂一点，需要对应目标分别生成user向量和item向量，多个目标就会生成多个user向量和多个item向量。item侧向量由于需要离线预测，因此，可以离线预测完拼接存好，线上再拆分开用。或者直接存储多套向量。由于存储资源问题，也可将item侧向量共享，具体使用方式结合业务需要使用。</font>

<font style="color:rgb(25, 27, 31);">多目标在图文和视频场景一般有点击率、观看时长、互动率等。点击率和互动率一般采用交叉熵loss优化目标，观看时长一般会进行时长的变换，如取log、开方、分段取累积分位数等，然后采用MSE等回归loss优化。</font>

<font style="color:rgb(25, 27, 31);">参考：快手时长因果消偏 </font>[https://zhuanlan.zhihu.com/p/55](https://zhuanlan.zhihu.com/p/557463255)

### **<font style="color:rgb(25, 27, 31);">百度的双塔模型</font>**
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744187544232-019edacb-60a3-41b3-81ca-2a49230878f4.png)

<font style="color:rgb(25, 27, 31);">百度的双塔模型分别使用复杂的网络对用户相关的特征和广告相关的特征进行 embedding，分别形成两个独立的塔，在最后的交叉层之前用户特征和广告特征之间没有任何交互。这种方案就是训练时引入更多的特征完成复杂网络离线训练，然后将得到的 user embedding 和 item embedding 存入 </font>[<font style="color:rgb(9, 64, 142);">Redis</font>](https://zhida.zhihu.com/search?content_id=162599646&content_type=Article&match_order=1&q=Redis&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 这一类内存数据库中。</font>

<font style="color:rgb(25, 27, 31);">线上预测时使用 LR、</font>[<font style="color:rgb(9, 64, 142);">浅层 NN</font>](https://zhida.zhihu.com/search?content_id=162599646&content_type=Article&match_order=1&q=%E6%B5%85%E5%B1%82+NN&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 等轻量级模型或者更方便的相似距离计算方式。这也是业界很多大厂采用的推荐系统的构造方式。</font>

### **<font style="color:rgb(25, 27, 31);">谷歌的双塔模型</font>**


![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744187489266-eb2572c0-25cc-427a-8a79-1c7289b53d5c.jpeg)

<font style="color:rgb(25, 27, 31);">2019 年谷歌推出自己的双塔模型，文章的核心思想是：在大规模的推荐系统中，利用双塔模型对 user-item 对的交互关系进行建模，从而学习【用户，上下文】向量和【item】向量的关联。</font>**<font style="color:rgb(25, 27, 31);">针对大规模流数据，提出 in-batch softmax 损失函数与</font>**[**<font style="color:rgb(9, 64, 142);">流数据频率估计方法</font>**](https://zhida.zhihu.com/search?content_id=162599646&content_type=Article&match_order=1&q=%E6%B5%81%E6%95%B0%E6%8D%AE%E9%A2%91%E7%8E%87%E4%BC%B0%E8%AE%A1%E6%96%B9%E6%B3%95&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">更好的适应 item 的多种数据分布。</font>**

<font style="color:rgb(25, 27, 31);">利用双塔模型构建 YouTube 视频推荐系统，对于用户侧的塔根据用户观看视频特征构建 user embedding，对于视频侧的塔根据视频特征构建 video emebdding。两个塔分别是相互独立的网络。</font>

# 粗排模型
## <font style="color:rgb(51, 51, 51);">双塔DNN模型</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744186733260-0e75fe57-3b4e-4284-8f86-72069fc941fe.png)

+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">用户塔和物品塔独立计算特征，最后通过内积计算相似度</font>
    - <font style="color:rgb(51, 51, 51);">离线预计算物品向量，在线实时计算用户向量</font>
+ **<font style="color:rgb(51, 51, 51);">计算步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. <font style="color:rgb(51, 51, 51);">用户特征（历史行为/画像）输入用户塔得到用户向量</font>
    2. <font style="color:rgb(51, 51, 51);">物品特征（内容/统计）输入物品塔得到物品向量</font>
    3. <font style="color:rgb(51, 51, 51);">计算余弦相似度或点积得分</font>
+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：计算效率高（O(1)复杂度）</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：无法捕捉交叉特征</font>
+ **<font style="color:rgb(51, 51, 51);">改进</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">加入交叉注意力层（牺牲一定速度）</font>
    - <font style="color:rgb(51, 51, 51);">知识蒸馏（用精排模型指导训练）</font>
    - <font style="color:rgb(51, 51, 51);">多目标优化（CTR+时长等）</font>

```python
import torch
import torch.nn as nn

class TwoTower(nn.Module):
    def __init__(self, user_dim, item_dim, hidden_size):
        super().__init__()
        # 用户塔
        self.user_tower = nn.Sequential(
            nn.Linear(user_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size)
        )
        # 物品塔 
        self.item_tower = nn.Sequential(
            nn.Linear(item_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size)
        )
    
    def forward(self, user_feat, item_feat):
        user_emb = self.user_tower(user_feat)  # [B, H]
        item_emb = self.item_tower(item_feat)  # [N, H]
        scores = torch.matmul(user_emb, item_emb.T)  # [B, N]
        return scores

# 使用示例
model = TwoTower(user_dim=128, item_dim=256, hidden_size=64)
user_feat = torch.randn(32, 128)  # 32个用户
item_feat = torch.randn(1000, 256) # 1000个物品
scores = model(user_feat, item_feat) # 32x1000

```

# 精排模型
## 4.1 Wide&Deep
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Google提出的联合训练框架，平衡记忆（Wide部分）与泛化（Deep部分）：</font>

+ **<font style="color:rgb(51, 51, 51);">Wide部分</font>**<font style="color:rgb(51, 51, 51);">：线性模型，捕获显式特征交互（如交叉特征）。</font>
+ **<font style="color:rgb(51, 51, 51);">Deep部分</font>**<font style="color:rgb(51, 51, 51);">：深度神经网络，学习隐式高阶特征。</font>

:::

<font style="color:rgb(25, 27, 31);">WideAndDeep 不是一个特定的模型，更是一类”思想“模型的统称，基本的模型图如下</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744188235022-c9d89bae-43b5-4a81-9100-36b6a593de6f.png)

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744188279656-2f9ea916-20e0-4149-a3ab-3da8c4e2cbc3.jpeg)

<font style="color:rgb(25, 27, 31);">Google将网络设计成这个样子，解释是说Wide部分有”记忆“能力，Deep部分有”泛化“能力。在使用过程中可以根据输入特征的特点将特征输入到wide 或者 deep 部分，一般可以遵循以下要点：</font>

<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">Wide特征</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">1.1根据业务先验知识或特征工程等方法，可以判断模型和此类特征强线性相关，比如在ctr场景，商品的价格，销量等，这类特征可以直接对模型性能有本质贡献，不用深度网络去泛化；  
</font><font style="color:rgb(25, 27, 31);">1.2 非常稀疏one-hot的特征；  
</font><font style="color:rgb(25, 27, 31);">1.3 根据根据业务先验知识，对one-hot特征再进行特征组合后的特征  
</font><font style="color:rgb(25, 27, 31);">1.4 Wide特征需要根据以前分享的特征工程知识做特征处理</font>

<font style="color:rgb(25, 27, 31);">  
</font>**<font style="color:rgb(25, 27, 31);">Deep特征</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">凡是不属于1.1和1.2的特征都可以放入deep部分，甚至一些多模态的特征如图片经过cnn的编码向量、一些预训练模型的输出结果比如bert对新闻标题的编码等，类似的特征都可以加入deep网络，当成一个黑盒去训练。  
</font><font style="color:rgb(25, 27, 31);">一般来说deep的one-hot特征维度不会很高不会太稀疏，deep的one-hot特征一般会加入embedding层，随模型一起训练从而得到更好的特征表示</font>

<font style="color:rgb(25, 27, 31);"></font>

**<font style="color:rgb(25, 27, 31);">联合训练</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">Wide和Deep两部分是一起训练，如果Wide特征非常稀疏，考虑</font>[<font style="color:rgb(9, 64, 142);">L1正则化</font>](https://zhida.zhihu.com/search?content_id=157923494&content_type=Article&match_order=1&q=L1%E6%AD%A3%E5%88%99%E5%8C%96&zhida_source=entity)<font style="color:rgb(25, 27, 31);">让模型参数稀疏，增加模型泛化性能和减少处理耗时  
</font><font style="color:rgb(25, 27, 31);">总的来说，WideAndDeep 就是一个广义的线性模型，加上一部分DNN网络来处理一些不好做特征工程的特征，最终两部分网络的输出做为特征共同进入全连接层进行目标函数拟合。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">输入特征</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Wide部分：稀疏特征（如用户ID、历史行为）的交叉组合。</font>
    - <font style="color:rgb(51, 51, 51);">Deep部分：Embedding后的类别特征 + 数值特征。</font>
2. **<font style="color:rgb(51, 51, 51);">联合输出</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298468355-c30329d6-77fa-4939-865f-9f964a1c969e.png)

    - <font style="color:rgb(51, 51, 51);">ϕ(x)</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：手工设计的交叉特征。</font>
    - <font style="color:rgb(51, 51, 51);">a(L)</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：深度网络最后一层激活值。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：平衡记忆与泛化，适合大规模稀疏数据。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：依赖特征工程，交叉特征需人工设计。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">具有丰富用户行为数据的场景（如Google Play推荐）。</font>
+ <font style="color:rgb(51, 51, 51);">需要同时处理稀疏和稠密特征的任务。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">DeepFM</font>**<font style="color:rgb(51, 51, 51);">：用FM替代Wide部分，自动学习特征交叉。</font>
+ **<font style="color:rgb(51, 51, 51);">AutoCross</font>**<font style="color:rgb(51, 51, 51);">：自动化特征交叉生成。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn

class WideAndDeep(nn.Module):
    def __init__(self, wide_dim, deep_dims, embed_dims, hidden_units):
        super().__init__()
        # Wide部分（输入需包含交叉特征）
        self.wide = nn.Linear(wide_dim, 1)
        
        # Deep部分嵌入层
        self.embeddings = nn.ModuleList([
            nn.Embedding(num_emb, dim) for num_emb, dim in embed_dims
        ])
        
        # Deep部分全连接
        deep_input_dim = sum(dim for _, dim in embed_dims) + deep_dims
        self.dnn = nn.Sequential(
            nn.Linear(deep_input_dim, hidden_units[0]),
            nn.ReLU(),
            nn.Linear(hidden_units[0], hidden_units[1]),
            nn.ReLU()
        )
        self.deep_out = nn.Linear(hidden_units[1], 1)
        
    def forward(self, wide_x, deep_sparse_x, deep_dense_x):
        # Wide部分
        wide_logit = self.wide(wide_x)
        
        # Deep部分
        embedded = [emb(deep_sparse_x[:,i]) for i, emb in enumerate(self.embeddings)]
        embedded = torch.cat(embedded + [deep_dense_x], dim=1)
        deep_out = self.dnn(embedded)
        deep_logit = self.deep_out(deep_out)
        
        # 联合输出
        return torch.sigmoid(wide_logit + deep_logit)

# 示例参数
model = WideAndDeep(
    wide_dim=10,  # Wide部分输入维度
    deep_dims=5,  # 数值型特征维度
    embed_dims=[(100, 8), (50, 4)],  # 类别型特征嵌入配置
    hidden_units=[64, 32]
)

```



## <font style="color:rgb(51, 51, 51);">4.2 DIN(Deep Interest Network)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">阿里提出的动态兴趣模型，通过注意力机制加权用户历史行为：</font>

+ **<font style="color:rgb(51, 51, 51);">注意力得分</font>**<font style="color:rgb(51, 51, 51);">：候选物品与历史物品的相关性。</font>
+ **<font style="color:rgb(51, 51, 51);">用户表示</font>**<font style="color:rgb(51, 51, 51);">：加权求和历史行为向量：v</font><sub><font style="color:rgb(51, 51, 51);">u</font></sub><font style="color:rgb(51, 51, 51);">=∑</font><sub><font style="color:rgb(51, 51, 51);">i=1</font></sub><font style="color:rgb(51, 51, 51);">Ta(v</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><font style="color:rgb(51, 51, 51);">,v</font><sub><font style="color:rgb(51, 51, 51);">a</font></sub><font style="color:rgb(51, 51, 51);">)v</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><font style="color:rgb(51, 51, 51);">其中 va是候选物品向量，a(⋅)是注意力网络。</font>

paper：[https://arxiv.org/pdf/1706.06978](https://arxiv.org/pdf/1706.06978)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744188458010-9564e01e-0275-470c-880c-8d8add2d2397.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">Embedding层</font>**<font style="color:rgb(51, 51, 51);">：将用户行为序列、候选物品映射为向量。</font>
2. **<font style="color:rgb(51, 51, 51);">注意力网络</font>**<font style="color:rgb(51, 51, 51);">：a(v</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><font style="color:rgb(51, 51, 51);">,v</font><sub><font style="color:rgb(51, 51, 51);">a</font></sub><font style="color:rgb(51, 51, 51);">)=softmax(wT</font><sub><font style="color:rgb(51, 51, 51);">σ</font></sub><font style="color:rgb(51, 51, 51);">(W[v</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><font style="color:rgb(51, 51, 51);">;v</font><sub><font style="color:rgb(51, 51, 51);">a</font></sub><font style="color:rgb(51, 51, 51);">]+b))</font>
3. **<font style="color:rgb(51, 51, 51);">池化层</font>**<font style="color:rgb(51, 51, 51);">：加权求和得到用户兴趣表示。</font>
4. **<font style="color:rgb(51, 51, 51);">预测层</font>**<font style="color:rgb(51, 51, 51);">：拼接兴趣向量与其他特征，通过MLP输出点击率。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：动态捕捉多样化兴趣，适合长行为序列。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：计算复杂度高，需优化注意力计算。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">电商场景（如淘宝商品推荐）。</font>
+ <font style="color:rgb(51, 51, 51);">长用户行为序列的CTR预估。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">DIEN</font>**<font style="color:rgb(51, 51, 51);">：引入GRU建模兴趣演化。</font>
+ **<font style="color:rgb(51, 51, 51);">SIM</font>**<font style="color:rgb(51, 51, 51);">：长短期兴趣分离与检索。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class DIN(nn.Module):
    def __init__(self, item_num, embed_dim, hidden_units):
        super().__init__()
        self.item_embed = nn.Embedding(item_num, embed_dim)
        self.attention = nn.Sequential(
            nn.Linear(4 * embed_dim, 80),
            nn.ReLU(),
            nn.Linear(80, 40),
            nn.ReLU(),
            nn.Linear(40, 1)
        )
        self.fc = nn.Sequential(
            nn.Linear(2 * embed_dim, hidden_units[0]),
            nn.ReLU(),
            nn.Linear(hidden_units[0], hidden_units[1]),
            nn.ReLU(),
            nn.Linear(hidden_units[1], 1)
        )
    
    def forward(self, user_hist, candidate_item):
        # 嵌入层
        hist_embed = self.item_embed(user_hist)  # [B, T, D]
        cand_embed = self.item_embed(candidate_item)  # [B, D]
        
        # 扩展候选商品维度
        cand_repeat = cand_embed.unsqueeze(1).repeat(1, hist_embed.size(1), 1)  # [B, T, D]
        
        # 计算注意力得分
        attn_input = torch.cat([hist_embed, cand_repeat, hist_embed * cand_repeat], dim=-1)
        attn_scores = self.attention(attn_input).squeeze(-1)  # [B, T]
        attn_weights = torch.softmax(attn_scores, dim=-1)
        
        # 加权池化
        user_interest = torch.sum(hist_embed * attn_weights.unsqueeze(-1), dim=1)  # [B, D]
        
        # 拼接特征并预测
        concat = torch.cat([user_interest, cand_embed], dim=-1)
        return torch.sigmoid(self.fc(concat))

# 示例参数
model = DIN(
    item_num=10000,   # 商品数量
    embed_dim=32,     # 嵌入维度
    hidden_units=[64, 32]
)

# 输入示例
user_hist = torch.randint(0, 10000, (128, 50))  # batch_size=128, 序列长度=50
candidate = torch.randint(0, 10000, (128,))
output = model(user_hist, candidate)  # 预测用户对候选商品的点击概率

```



## 4.3 DeepFM
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">DeepFM（Deep Factorization Machine）是一种结合了因子分解机（FM）和深度神经网络（DNN）的推荐系统模型，旨在自动捕捉低阶和高阶特征交互，适用于点击率预估（CTR）等任务。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744188364898-2de77523-a360-4206-bb98-9a0b79c339d0.png)

:::color5
**<font style="color:#601BDE;">1.原理</font>**

:::

<font style="color:rgb(51, 51, 51);">DeepFM通过以下两部分联合建模特征交互：</font>

1. **FM部分**：捕捉特征间的二阶线性交互。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298875593-91c9280e-b368-42e9-ab55-804da9966a9e.png)

其中：<font style="color:rgb(51, 51, 51);">w0 为全局偏置，wi 为一阶权重，vi为特征隐向量，⟨⋅,⋅⟩为向量内积，建模二阶特征交叉。</font>

2. **DNN部分**：通过多层神经网络捕捉高阶非线性交互。
    - <font style="color:rgb(51, 51, 51);">输入：特征嵌入向量的拼接。</font>
    - <font style="color:rgb(51, 51, 51);">结构：多层全连接层（如ReLU激活函数）。</font>

**<font style="color:rgb(51, 51, 51);">联合输出</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298907062-90ad3db1-3f17-4628-a584-8a2a7c1672bc.png)

<font style="color:rgb(51, 51, 51);">其中，σ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为Sigmoid函数，用于输出概率值。</font>

:::color5
**<font style="color:#601BDE;">2.计算步骤</font>**

:::

1. **输入处理**：
    - <font style="color:rgb(51, 51, 51);">数值特征：直接输入。</font>
    - <font style="color:rgb(51, 51, 51);">类别特征：通过嵌入层（Embedding）转换为稠密向量。</font>
2. **FM部分计算**：
    - <font style="color:rgb(51, 51, 51);">一阶项：线性加权和。</font>
    - <font style="color:rgb(51, 51, 51);">二阶项：隐向量内积求和，优化计算复杂度：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298921836-42b1d398-189e-4598-8dff-03e07ef22019.png)

3. **DNN部分计算**：
    - <font style="color:rgb(51, 51, 51);">嵌入层：将各特征域的嵌入向量拼接为输入。</font>
    - <font style="color:rgb(51, 51, 51);">多层感知机（MLP）：通过全连接层提取高阶特征。</font>
4. **联合训练**：
    - <font style="color:rgb(51, 51, 51);">FM与DNN共享嵌入层参数。</font>
    - <font style="color:rgb(51, 51, 51);">使用交叉熵损失函数：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740298934103-a23c0adf-4a30-43c7-b9e4-18050a4600e6.png)

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

<font style="color:rgb(255, 255, 255);">复制</font>

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">自动学习低阶（FM）与高阶（DNN）特征交互。</font> | <font style="color:rgb(51, 51, 51);">计算复杂度较高，尤其在高维稀疏场景。</font> |
| <font style="color:rgb(51, 51, 51);">无需人工设计特征交叉（如Wide & Deep）。</font> | <font style="color:rgb(51, 51, 51);">超参数较多（如嵌入维度、网络层数）。</font> |
| <font style="color:rgb(51, 51, 51);">共享嵌入层，减少参数量。</font> | <font style="color:rgb(51, 51, 51);">对长序列行为建模能力有限。</font> |


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">CTR预估</font>**<font style="color:rgb(51, 51, 51);">：广告点击率预测（如Criteo数据集）。</font>
+ **<font style="color:rgb(51, 51, 51);">推荐系统</font>**<font style="color:rgb(51, 51, 51);">：电商商品推荐（如淘宝猜你喜欢）。</font>
+ **<font style="color:rgb(51, 51, 51);">排序模型</font>**<font style="color:rgb(51, 51, 51);">：信息流内容排序（如新闻、短视频）。</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **特征工程优化**：
    - <font style="color:rgb(51, 51, 51);">引入注意力机制（如AFM）动态加权特征交互。</font>
    - <font style="color:rgb(51, 51, 51);">结合用户行为序列建模（如DIEN）。</font>
2. **模型结构改进**：
    - **<font style="color:rgb(51, 51, 51);">Deep & Cross Network (DCN)</font>**<font style="color:rgb(51, 51, 51);">：用交叉网络替代FM，显式学习高阶交叉。</font>
    - **<font style="color:rgb(51, 51, 51);">xDeepFM</font>**<font style="color:rgb(51, 51, 51);">：引入压缩交互网络（CIN），增强显式高阶交互。</font>
3. **训练效率提升**：
    - <font style="color:rgb(51, 51, 51);">使用混合精度训练或模型蒸馏。</font>
    - <font style="color:rgb(51, 51, 51);">采用稀疏矩阵加速FM计算。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepFM(nn.Module):
    def __init__(self, feature_sizes, embedding_dim=10, hidden_dims=[256, 128]):
        """
        Args:
            feature_sizes (list): 各稀疏特征域的类别数，如 [user_num, item_num, cate_num]
            embedding_dim (int): 嵌入维度
            hidden_dims (list): Deep部分隐藏层维度
        """
        super(DeepFM, self).__init__()
        self.feature_sizes = feature_sizes
        self.num_fields = len(feature_sizes)  # 特征域数量
        
        # FM一阶项权重
        self.linear = nn.Embedding(sum(feature_sizes) + 1, 1)  # +1 for padding_idx
        self.bias = nn.Parameter(torch.randn(1))
        
        # FM二阶项及Deep共享嵌入层
        self.embedding_layers = nn.ModuleList([
            nn.Embedding(feature_size, embedding_dim) 
            for feature_size in feature_sizes
        ])
        
        # Deep部分MLP
        deep_input_dim = len(feature_sizes) * embedding_dim
        self.deep = nn.Sequential()
        for i, h in enumerate(hidden_dims):
            self.deep.add_module(f'fc{i}', nn.Linear(deep_input_dim, h))
            self.deep.add_module(f'relu{i}', nn.ReLU())
            deep_input_dim = h
        self.deep.add_module('output', nn.Linear(deep_input_dim, 1))
        
    def forward(self, x_sparse):
        """
        Args:
            x_sparse (LongTensor): 稀疏特征输入, shape=(batch_size, num_fields)
        """
        # === FM一阶项 ===
        linear_terms = torch.sum(self.linear(x_sparse), dim=1)  # (batch_size, 1)
        
        # === FM二阶项 ===
        # 嵌入层输出: [(batch_size, embed_dim)] * num_fields
        embeddings = [emb_layer(x_sparse[:, i]) for i, emb_layer in enumerate(self.embedding_layers)]
        
        # 平方和减和的平方计算二阶交互
        sum_square = torch.sum(torch.stack(embeddings), dim=0) ** 2  # (batch_size, embed_dim)
        square_sum = torch.sum(torch.stack([emb ** 2 for emb in embeddings]), dim=0)
        fm_second_order = 0.5 * (sum_square - square_sum).sum(dim=1, keepdim=True)  # (batch_size, 1)
        
        # === Deep部分 ===
        deep_input = torch.cat(embeddings, dim=1)  # (batch_size, num_fields * embed_dim)
        deep_output = self.deep(deep_input)  # (batch_size, 1)
        
        # === 合并输出 ===
        y_fm = linear_terms + fm_second_order
        y = self.bias + y_fm + deep_output
        return torch.sigmoid(y.squeeze(1))  # (batch_size,)

# 示例使用
if __name__ == "__main__":
    # 假设特征：用户ID（1000类）、物品ID（2000类）、类别ID（50类）
    feature_sizes = [1000, 2000, 50]
    model = DeepFM(feature_sizes, embedding_dim=16, hidden_dims=[256, 128])
    
    # 模拟输入：batch_size=32, 3个特征域
    x_sparse = torch.LongTensor(32, 3).random_(0, 1000)  # 各特征值需小于对应类别数
    output = model(x_sparse)
    print(output.shape)  # torch.Size([32])

```

## 4.4 MMoE
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">MMoE（Multi-gate Mixture-of-Experts）是Google在2018年提出的多任务学习模型，通过多专家结构和门控机制解决多任务间的差异性问题。以下是详细解析：</font>

:::

<font style="color:rgb(25, 27, 31);">MMoE模型的结构(下图c)</font>**<font style="color:rgb(25, 27, 31);">基于广泛使用的Shared-Bottom结构(下图a)和MoE结构</font>**<font style="color:rgb(25, 27, 31);">，其中图(b)是图(c)的一种特殊情况，下面依次介绍。</font>

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1744188620415-7ac5a341-3876-4617-90e3-dcc1b2495d79.jpeg)

1. **<font style="color:rgb(25, 27, 31);">多任务学习-Shared-Bottom Multi-task Model</font>**

**<font style="color:rgb(25, 27, 31);">Shared-Bottom</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">网络通常位于底部，表示为函数</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">f</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，多个任务共用这一层。往上，</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">K</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个子任务分别对应一个 tower network，表示为</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">，每个子任务的输出为：</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">h</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">f</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">x</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);">)</font>

**<font style="color:rgb(25, 27, 31);">优点：</font>**

+ <font style="color:rgb(25, 27, 31);">浅层参数共享，互相补充学习，任务相关性越高，模型的loss可以降低到更低</font>

**<font style="color:rgb(25, 27, 31);">缺点：</font>**

+ <font style="color:rgb(25, 27, 31);">任务没有好的相关性时，这种Hard parameter sharing会损害效果</font>
2. **<font style="color:rgb(25, 27, 31);">多专家学习-MOE</font>**

<font style="color:rgb(25, 27, 31);">前面的Shared-Bottom是一种Hard parameter sharing，会导致不相关任务联合学习效果不佳，为了解决这个问题，Google提出了Soft parameter sharing，</font>**<font style="color:rgb(25, 27, 31);">MOE</font>**<font style="color:rgb(25, 27, 31);">是其中的一种实现。</font>

3. **<font style="color:rgb(25, 27, 31);">多任务多专家学习-MMOE</font>**

**<font style="color:rgb(25, 27, 31);">MMOE</font>**<font style="color:rgb(25, 27, 31);">(Multi-gate Mixture-of-Experts)是在MOE的基础上，使用了多个门控网络， </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 个任就对应 </font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 个门控网络，模型结构如图3所示：</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：用多个专家网络（Experts）+ 任务专属门控网络（Gates）替代传统Shared-Bottom结构，动态学习不同任务的特征组合。</font>

1. **专家网络**（Experts）：
    - <font style="color:rgb(51, 51, 51);">多个独立的子网络，每个专家学习输入数据的不同特征表示。</font>
    - <font style="color:rgb(51, 51, 51);">专家之间参数不共享，增强模型表达能力。</font>
2. **门控网络**（Gates）：
    - <font style="color:rgb(51, 51, 51);">每个任务对应一个门控网络，计算各专家对该任务的权重。</font>
    - <font style="color:rgb(51, 51, 51);">通过Softmax归一化权重，加权融合专家输出。</font>
3. **多任务联合训练**：
    - <font style="color:rgb(51, 51, 51);">不同任务共享专家层，但通过门控机制实现差异化特征组合。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">输入层</font>**<font style="color:rgb(51, 51, 51);">：原始特征向量 x</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>
2. **<font style="color:rgb(51, 51, 51);">专家层</font>**<font style="color:rgb(51, 51, 51);">：Ei(x)=fi(x)，其中 fi 是第 i</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">个专家网络。</font>
3. **<font style="color:rgb(51, 51, 51);">门控网络</font>**<font style="color:rgb(51, 51, 51);">：对第 k个任务，门控权重</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740302327804-58b0dec3-8ed7-403a-b2fa-ba0b7657e959.png)
4. **<font style="color:rgb(51, 51, 51);">任务特征融合</font>**<font style="color:rgb(51, 51, 51);">：第 k个任务的融合特征 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740302338911-85a33d8f-85f0-4ea6-a3a9-e26dfd8d5393.png)
5. **<font style="color:rgb(51, 51, 51);">任务塔网络</font>**<font style="color:rgb(51, 51, 51);">：yk=Tk(hk)，Tk</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 是任务专属的塔网络。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">处理任务差异</font>**<font style="color:rgb(51, 51, 51);">：门控机制自适应调整专家权重，缓解任务冲突。</font>
2. **<font style="color:rgb(51, 51, 51);">灵活性强</font>**<font style="color:rgb(51, 51, 51);">：支持任意数量任务，扩展性好。</font>
3. **<font style="color:rgb(51, 51, 51);">特征复用</font>**<font style="color:rgb(51, 51, 51);">：共享专家层减少冗余计算。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">参数量大</font>**<font style="color:rgb(51, 51, 51);">：专家数量和门控网络增加计算成本。</font>
2. **<font style="color:rgb(51, 51, 51);">过拟合风险</font>**<font style="color:rgb(51, 51, 51);">：小数据集上易过拟合。</font>
3. **<font style="color:rgb(51, 51, 51);">门控收敛难</font>**<font style="color:rgb(51, 51, 51);">：需精细调整超参数。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">推荐系统</font>**<font style="color:rgb(51, 51, 51);">：同时预测点击率（CTR）、转化率（CVR）。</font>
2. **<font style="color:rgb(51, 51, 51);">广告排序</font>**<font style="color:rgb(51, 51, 51);">：兼顾点击率和广告收入。</font>
3. **<font style="color:rgb(51, 51, 51);">用户画像</font>**<font style="color:rgb(51, 51, 51);">：多标签预测（年龄、性别、兴趣）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">动态专家数量</font>**<font style="color:rgb(51, 51, 51);">：根据任务复杂度自动调整专家数。</font>
2. **<font style="color:rgb(51, 51, 51);">稀疏门控</font>**<font style="color:rgb(51, 51, 51);">：引入L1正则化稀疏权重，降低计算量。</font>
3. **<font style="color:rgb(51, 51, 51);">注意力机制</font>**<font style="color:rgb(51, 51, 51);">：用Attention增强门控的上下文感知能力。</font>
4. **<font style="color:rgb(51, 51, 51);">结合PLE</font>**<font style="color:rgb(51, 51, 51);">：华为提出的Progressive Layered Extraction，进一步分离共享/专属专家。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class Expert(nn.Module):
    def __init__(self, input_dim, expert_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, expert_dim),
            nn.ReLU(),
            nn.Linear(expert_dim, expert_dim),
            nn.ReLU()
        )
    
    def forward(self, x):
        return self.net(x)

class Gate(nn.Module):
    def __init__(self, input_dim, num_experts):
        super().__init__()
        self.gate = nn.Linear(input_dim, num_experts)
    
    def forward(self, x):
        return F.softmax(self.gate(x), dim=1)

class MMoE(nn.Module):
    def __init__(self, input_dim, num_experts, expert_dim, num_tasks, task_dims):
        super().__init__()
        self.experts = nn.ModuleList([Expert(input_dim, expert_dim) for _ in range(num_experts)])
        self.gates = nn.ModuleList([Gate(input_dim, num_experts) for _ in range(num_tasks)])
        self.towers = nn.ModuleList([nn.Linear(expert_dim, dim) for dim in task_dims])
    
    def forward(self, x):
        expert_outputs = [expert(x) for expert in self.experts]  # [num_experts, bs, expert_dim]
        expert_outputs = torch.stack(expert_outputs, dim=1)      # [bs, num_experts, expert_dim]
        
        outputs = []
        for gate, tower in zip(self.gates, self.towers):
            gate_weights = gate(x).unsqueeze(-1)                 # [bs, num_experts, 1]
            combined = (expert_outputs * gate_weights).sum(dim=1) # [bs, expert_dim]
            outputs.append(tower(combined))                      # Task-specific output
        
        return outputs  # List of task outputs

# 示例用法
input_dim = 128
num_experts = 4
expert_dim = 64
num_tasks = 2
task_dims = [1, 1]  # 回归任务输出1维

model = MMoE(input_dim, num_experts, expert_dim, num_tasks, task_dims)
x = torch.randn(32, input_dim)
outputs = model(x)  # 两个任务输出

```



# 重排模型
## MMR (<font style="color:rgb(51, 51, 51);">Maximal Marginal Relevance）</font>
+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：在相关性与多样性间权衡</font>
+ **<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740302861805-4a683e55-ef14-4adb-b001-9b1235fabb33.png)
+ **<font style="color:rgb(51, 51, 51);">实现代码</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
def mmr_rerank(score_dict, similarity_matrix, lambda_param=0.7, topk=10):
    selected = []
    candidates = sorted(score_dict.keys(), key=lambda x: score_dict[x], reverse=True)

    while len(selected) < topk:
        best_score = -float('inf')
        best_item = None

        for item in candidates:
            if item in selected:
                continue

            # 计算相关性部分
            rel_score = score_dict[item] 
            # 计算多样性惩罚项
            div_penalty = 0
            if selected:
                max_sim = max(similarity_matrix[item][s] for s in selected)
                div_penalty = max_sim

            total_score = lambda_param * rel_score - (1 - lambda_param) * div_penalty

            if total_score > best_score:
                best_score = total_score
                best_item = item

        selected.append(best_item)
        candidates.remove(best_item)

    return selected

```



## Transformer重排
+ **<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：使用self-attention捕捉item间关系</font>
+ **<font style="color:rgb(51, 51, 51);">架构</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
Input Embedding → Positional Encoding → 
Transformer Layers → Prediction Head
```

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：建模全局依赖关系</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：需要充足训练数据</font>

```python
class TransformerReranker(nn.Module):
    def __init__(self, dim, num_heads, num_layers):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=dim, nhead=num_heads
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        self.predictor = nn.Linear(dim, 1)
    
    def forward(self, item_embs):  # [seq_len, batch, dim]
        context_aware = self.transformer(item_embs)
        scores = self.predictor(context_aware).squeeze()
        return scores  # [seq_len, batch]

```



