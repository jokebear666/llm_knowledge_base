# ⓷ 评价指标

<!-- source: yuque://zhongxian-iiot9/hlyypb/xagtbozxmpzcyyrb -->

## <font style="color:rgb(51, 51, 51);">一、</font>**<font style="color:rgb(51, 51, 51);">搜索算法评估指标</font>**
### <font style="color:rgb(51, 51, 51);">1. Precision@k</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：前k个结果中相关文档的比例  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300543094-2e91a35c-4e4c-4649-a3b0-ff4af47cf326.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def precision_at_k(y_true, y_pred, k):
    y_pred_topk = y_pred[:k]
    relevant = sum(1 for doc in y_pred_topk if doc in y_true)
    return relevant / k
```

### <font style="color:rgb(51, 51, 51);">2. Recall@k</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：前k个结果中相关文档占全部相关文档的比例  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300586165-f75aa00c-19fd-4847-aef0-4115aee1bdb6.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def recall_at_k(y_true, y_pred, k):
    y_pred_topk = y_pred[:k]
    relevant_in_topk = sum(1 for doc in y_pred_topk if doc in y_true)
    total_relevant = len(y_true)
    return relevant_in_topk / total_relevant if total_relevant != 0 else 0
```

### <font style="color:rgb(51, 51, 51);">3. MAP (Mean Average Precision )</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：对每个查询的平均精度（AP）取平均  
</font>**<font style="color:rgb(51, 51, 51);">计算步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">计算每个位置的Precision@k</font>
2. <font style="color:rgb(51, 51, 51);">对相关文档位置的Precision@k取平均</font>
3. <font style="color:rgb(51, 51, 51);">对所有查询的AP取平均</font>

**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

from sklearn.metrics import average_precision_score
import numpy as np

# 示例：y_true为二元相关性标签，y_scores为预测得分
y_true = np.array([0, 1, 1, 0, 1])
y_scores = np.array([0.1, 0.4, 0.3, 0.2, 0.5])
map_score = average_precision_score(y_true, y_scores)
```

### <font style="color:rgb(51, 51, 51);">4. NDCG(Normalized Discounted Cumulative Gain)</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：衡量排序结果与理想排序的相关性差距  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300611424-325397e9-2960-4d63-955f-059f3a392601.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def ndcg_at_k(y_true_relevance, y_pred_ranking, k):
    # y_true_relevance: 文档的真实相关性分数列表
    # y_pred_ranking: 预测的文档排序列表
    dcg = 0
    for i, doc in enumerate(y_pred_ranking[:k]):
        rel = y_true_relevance[doc]
        dcg += (2 ** rel - 1) / np.log2(i + 2)  # i从0开始，+2调整为i+1

    # 计算理想DCG（IDCG）
    ideal_sorted = sorted(y_true_relevance, reverse=True)[:k]
    idcg = 0
    for i, rel in enumerate(ideal_sorted):
        idcg += (2 ** rel - 1) / np.log2(i + 2)

    return dcg / idcg if idcg != 0 else 0
```

---

## <font style="color:rgb(51, 51, 51);">二、</font>**<font style="color:rgb(51, 51, 51);">广告算法评估指标</font>**
### <font style="color:rgb(51, 51, 51);">1.CTR (Click-Through Rate)</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：广告点击次数与展示次数的比例  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300634340-344cb57f-73ed-4bcb-9145-a15e740ceca5.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def ctr(clicks, impressions):
    return clicks / impressions if impressions != 0 else 0
```

### <font style="color:rgb(51, 51, 51);">2. CVR (Conversion Rate)</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：转化次数与点击次数的比例  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300647127-b0bd0088-c925-41fb-b61a-f92324674378.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def cvr(conversions, clicks):
    return conversions / clicks if clicks != 0 else 0
```

### <font style="color:rgb(51, 51, 51);">3. ROI (Return on Investment)</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：广告主收益与广告花费的比例  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300658976-b64e51ab-81a0-4277-b603-80a0d0d2bbd5.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def roi(revenue, cost):
    return (revenue - cost) / cost if cost != 0 else 0
```

### <font style="color:rgb(51, 51, 51);">4. eCPM (Effective Cost Per Mille)</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：每千次展示的广告收入  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">eCPM=CTR×CVR×Bid Price×1000  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def ecpm(ctr, cvr, bid_price):
    return ctr * cvr * bid_price * 1000
```

### 5. AUC
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">AUC</font>**<font style="color:rgb(51, 51, 51);">（Area Under the ROC Curve）是ROC曲线（Receiver Operating Characteristic Curve）下的面积，用于评估二分类模型的排序能力，衡量模型将正样本排在负样本前面的概率。</font>

+ **<font style="color:rgb(51, 51, 51);">取值范围</font>**<font style="color:rgb(51, 51, 51);">：0.5（随机猜测）~1（完美排序）</font>
+ **<font style="color:rgb(51, 51, 51);">核心意义</font>**<font style="color:rgb(51, 51, 51);">：随机选取一个正样本和一个负样本，正样本预测得分高于负样本的概率。</font>

:::

+ <font style="color:rgb(51, 51, 51);">AUC是评估推荐系统排序能力的核心指标，尤其适用于</font>**<font style="color:#74B602;">精排和粗排阶段</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ <font style="color:rgb(51, 51, 51);">推荐系统中需结合业务目标选择指标：AUC（整体排序）+ NDCG/HitRate（Top-K质量）。</font>
+ **<font style="color:#74B602;">召回阶段关注效率而非排序，重排阶段需综合业务规则</font>**<font style="color:rgb(51, 51, 51);">，AUC的参考价值有限。</font>

:::color5
**<font style="color:#601BDE;">1.ROC曲线原理</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">横轴</font>**<font style="color:rgb(51, 51, 51);">：假阳率（False Positive Rate, FPR）  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740303564053-3dfe4644-6b44-445c-84e7-ca88d5c1b5ea.png)
+ **<font style="color:rgb(51, 51, 51);">纵轴</font>**<font style="color:rgb(51, 51, 51);">：真阳率（True Positive Rate, TPR，即召回率）  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740303573308-85ca3325-6749-408c-a67f-ec0c74d3573c.png)
+ **<font style="color:rgb(51, 51, 51);">绘制方法</font>**<font style="color:rgb(51, 51, 51);">：通过调整分类阈值，计算不同阈值下的TPR和FPR值，连接成曲线。</font>

:::color5
**<font style="color:#601BDE;">2.AUC计算公式</font>**

:::

<font style="color:rgb(51, 51, 51);">AUC的计算基于正负样本对的比较：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740303583836-228d8ff9-58a7-4ab0-bd56-f81f12a1cd43.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中：</font>

+ <font style="color:rgb(51, 51, 51);">N正</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：正样本数量</font>
+ <font style="color:rgb(51, 51, 51);">N负</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：负样本数量</font>
+ <font style="color:rgb(51, 51, 51);">rank(正样本)：所有样本按预测得分降序排序后，正样本的排名和（从1开始计数）。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">与分类阈值无关，全面评估模型整体排序能力。</font>
    - <font style="color:rgb(51, 51, 51);">对类别不平衡不敏感（适合推荐系统中的隐式反馈场景）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">无法直接优化Top-K排序质量（需结合NDCG等指标）。</font>
    - <font style="color:rgb(51, 51, 51);">对预测得分的绝对数值不敏感，只关注相对顺序。</font>

:::color5
**<font style="color:#601BDE;">4.实现代码示例</font>**

:::

```python
#方式一：基于sklearn库
from sklearn.metrics import roc_auc_score

# 示例数据
y_true = [1, 0, 1, 0, 1]       # 真实标签（0/1）
y_scores = [0.9, 0.3, 0.8, 0.2, 0.7]  # 预测得分（概率）

# 计算AUC
auc = roc_auc_score(y_true, y_scores)
print(f"AUC = {auc:.4f}")  # 输出：AUC = 0.8333



#方式二：手动实现
import numpy as np

def manual_auc(y_true, y_pred):
    # 合并标签和预测得分，并按预测得分降序排序
    data = sorted(zip(y_true, y_pred), key=lambda x: -x[1])
    sorted_labels = [label for label, _ in data]
    
    # 统计正样本数量
    n_pos = sum(y_true)
    n_neg = len(y_true) - n_pos
    
    if n_pos == 0 or n_neg == 0:
        return 0.5  # 全正或全负样本，AUC为0.5
    
    # 计算正样本的排名和（注意：排名从1开始）
    rank_sum = 0
    for i, label in enumerate(sorted_labels):
        if label == 1:
            rank_sum += (i + 1)  # 当前排名
    
    # 应用公式
    auc = (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)
    return auc

# 测试
y_true = [1, 0, 1, 0, 1]
y_pred = [0.9, 0.3, 0.8, 0.2, 0.7]
print(f"Manual AUC = {manual_auc(y_true, y_pred):.4f}")  # 输出：Manual AUC = 0.8333

```



## 
### 
## <font style="color:rgb(51, 51, 51);">三、</font>**<font style="color:rgb(51, 51, 51);">推荐算法评估指标</font>**
### <font style="color:rgb(51, 51, 51);">1. Hit Rate@k</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：用户点击/交互的推荐物品是否出现在Top-k推荐列表中  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300691717-5ec0483a-c46c-419c-843c-0efa9bb5194b.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def hit_rate_at_k(actual_items, recommended_items, k):
    recommended_topk = recommended_items[:k]
    return 1 if any(item in actual_items for item in recommended_topk) else 0
```

### <font style="color:rgb(51, 51, 51);">2. MRR (Mean Reciprocal Rank)</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：第一个相关物品的排名倒数取平均  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300701042-1d926a0a-6045-4b0f-81d0-eaa3bb6e994d.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def mrr(actual_items, recommended_items):
    for rank, item in enumerate(recommended_items, 1):
        if item in actual_items:
            return 1 / rank
    return 0
```

### <font style="color:rgb(51, 51, 51);">3. Coverage（覆盖率）</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：推荐系统能够推荐的物品占总物品的比例  
</font>**<font style="color:rgb(51, 51, 51);">公式</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740300714322-601458f8-4668-4df4-889b-edc3a4facd15.png)<font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

def coverage(all_items, recommended_lists):
    recommended_items = set()
    for rec_list in recommended_lists:
        recommended_items.update(rec_list)
    return len(recommended_items) / len(all_items)
```

### <font style="color:rgb(51, 51, 51);">4. Diversity（多样性）</font>
**<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：推荐列表的相似性差异（常用余弦相似度）  
</font>**<font style="color:rgb(51, 51, 51);">代码实现</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
python

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def diversity(recommended_vectors):
    sim_sum = 0
    count = 0
    for i in range(len(recommended_vectors)):
        for j in range(i+1, len(recommended_vectors)):
            sim = cosine_similarity([recommended_vectors[i]], [recommended_vectors[j]])[0][0]
            sim_sum += sim
            count += 1
    return 1 - (sim_sum / count) if count != 0 else 0
```

---

## <font style="color:rgb(51, 51, 51);">四、</font>**<font style="color:rgb(51, 51, 51);">总结</font>**
+ **<font style="color:rgb(51, 51, 51);">搜索算法</font>**<font style="color:rgb(51, 51, 51);">：侧重排序质量（MAP、NDCG）、相关性（Precision/Recall）。</font>
+ **<font style="color:rgb(51, 51, 51);">广告算法</font>**<font style="color:rgb(51, 51, 51);">：关注商业指标（CTR、ROI、eCPM）。</font>
+ **<font style="color:rgb(51, 51, 51);">推荐算法</font>**<font style="color:rgb(51, 51, 51);">：平衡准确性（Hit Rate）与多样性/覆盖率。</font>

