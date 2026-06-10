# ⓶ 向量检索

<!-- source: yuque://zhongxian-iiot9/hlyypb/owgqno4zr7xq07hw -->

# <font style="color:rgb(51, 51, 51);"> 向量检索库</font>
## 如何选择向量检索库
| **数据库** | **核心特点** | **适用场景** | **局限性** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">FAISS</font>** | <font style="color:rgb(51, 51, 51);">Facebook 开源库，单机高性能，支持 GPU 加速</font> | <font style="color:rgb(51, 51, 51);">小规模数据、离线场景</font> | <font style="color:rgb(51, 51, 51);">无分布式支持，需自行管理存储</font> |
| **<font style="color:rgb(51, 51, 51);">Milvus</font>** | 高性能向量检索<br/>灵活的存储与计算分离 | <font style="color:rgb(51, 51, 51);">大规模数据</font> | <font style="color:rgb(51, 51, 51);"></font> |
| **<font style="color:rgb(51, 51, 51);">Annoy</font>** | <font style="color:rgb(51, 51, 51);">Spotify 开源，轻量级，基于树的索引</font> | <font style="color:rgb(51, 51, 51);">快速原型开发、中等规模数据集</font> | <font style="color:rgb(51, 51, 51);">索引构建时间长，不支持动态更新</font> |
| **<font style="color:rgb(51, 51, 51);">Pinecone</font>** | <font style="color:rgb(51, 51, 51);">全托管云服务，自动索引优化，低延迟 API</font> | <font style="color:rgb(51, 51, 51);">企业级生产环境，无运维需求</font> | <font style="color:rgb(51, 51, 51);">成本较高，依赖云服务</font> |
| **<font style="color:rgb(51, 51, 51);">Weaviate</font>** | <font style="color:rgb(51, 51, 51);">结合向量搜索与图数据库能力，支持语义标签过滤</font> | <font style="color:rgb(51, 51, 51);">多模态数据联合检索</font> | <font style="color:rgb(51, 51, 51);">社区生态较小，学习曲线陡峭</font> |
| **<font style="color:rgb(51, 51, 51);">Qdrant</font>** | <font style="color:rgb(51, 51, 51);">Rust 开发，高性能，支持过滤与混合搜索</font> | <font style="color:rgb(51, 51, 51);">高吞吐低延迟场景（如广告推荐）</font> | <font style="color:rgb(51, 51, 51);">分布式功能仍在完善中</font> |
| **<font style="color:rgb(51, 51, 51);">Vespa</font>** | <font style="color:rgb(51, 51, 51);">支持文本+向量混合搜索，内置排序模型</font> | <font style="color:rgb(51, 51, 51);">复杂检索逻辑（如电商搜索）</font> | <font style="color:rgb(51, 51, 51);">配置复杂，资源消耗较大</font> |


**选择依据**

1. **数据规模**
    - <font style="color:rgb(51, 51, 51);">十亿级+：Milvus、Vespa（分布式扩展）。</font>
    - <font style="color:rgb(51, 51, 51);">百万级：FAISS、Annoy（单机部署）。</font>
2. **业务需求**
    - <font style="color:rgb(51, 51, 51);">多模态检索：Weaviate、Milvus（插件扩展）。</font>
    - <font style="color:rgb(51, 51, 51);">云原生与低运维：Pinecone、Milvus Cloud。</font>
3. **延迟与召回率**
    - <font style="color:rgb(51, 51, 51);">低延迟（<10ms）：Qdrant、Pinecone。</font>
    - <font style="color:rgb(51, 51, 51);">高召回率：Milvus + HNSW 索引。</font>

## Milvus
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Milvus 是一款开源的</font>**<font style="color:rgb(51, 51, 51);">向量数据库</font>**<font style="color:rgb(51, 51, 51);">，专为处理海量向量数据的存储、检索和分析而设计，尤其适用于机器学习、推荐系统、图像/视频检索等需要高效相似性搜索的场景。以下是关于 Milvus 的详细介绍及与其他向量数据库的对比分析。</font>

:::

:::color5
**<font style="color:#601BDE;">1.</font>**<font style="color:rgb(51, 51, 51);">Milvus 的核心特性</font>

:::

1. **高性能向量检索**
    - <font style="color:rgb(51, 51, 51);">支持多种索引类型（如 IVF_FLAT、HNSW、ANNOY），适配不同召回率与延迟需求。</font>
    - <font style="color:rgb(51, 51, 51);">分布式架构可横向扩展，处理十亿级向量数据，响应毫秒级查询。</font>
2. **灵活的存储与计算分离**
    - <font style="color:rgb(51, 51, 51);">存储层支持对象存储（如 S3）、分布式文件系统（如 MinIO）与本地存储。</font>
    - <font style="color:rgb(51, 51, 51);">计算层通过 Kubernetes 动态调度资源，实现弹性伸缩。</font>
3. **多数据模态支持**
    - <font style="color:rgb(51, 51, 51);">不仅支持数值型向量，还可扩展处理文本、图像、音视频等多模态特征。</font>
4. **企业级功能**
    - <font style="color:rgb(51, 51, 51);">数据分区、RBAC 权限控制、数据持久化与灾备，支持生产环境部署。</font>
    - <font style="color:rgb(51, 51, 51);">提供 RESTful API、Python/Java SDK，与主流 AI 框架（如 PyTorch、TensorFlow）无缝集成。</font>

## <font style="color:rgb(51, 51, 51);">Faiss</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Faiss（Facebook AI Similarity Search）是Meta AI实验室开发的高效向量相似度搜索库，专门用于解决大规模向量检索问题。</font>

:::

:::color5
**<font style="color:#601BDE;">1.核心原理设计</font>**

:::

1. **量化压缩技术**：
+ **乘积量化（Product Quantization, PQ）**：  
将高维向量分割为m个子空间，每个子空间进行k-means聚类，用log2(k)位存储聚类中心索引。

```plain
# PQ压缩示例
d = 128          # 原始维度
m = 8            # 子空间数量
bits = 8         # 每子空间比特数
nlist = 2**bits  # 每子空间码本大小
```

+ **残差量化（Residual Quantization）**：  
通过多级量化逐步逼近原始向量，公式：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740644537044-4598c998-aa62-4b7d-8663-edf6d8d65771.png)

2. **索引结构设计**：
    - **倒排索引（IVF）**：  
先粗聚类（nlist个簇），搜索时仅查询最近几个簇的向量

```plain
IVF搜索流程：
1. 计算query向量与所有粗聚类中心的距离
2. 选择前nprobe个最近簇
3. 在这些簇内进行精细搜索
```

    - **HNSW（Hierarchical Navigable Small World）**：  
基于图结构的层级导航，复杂度O(log n)

:::color5
**<font style="color:#601BDE;">2.索引类型</font>**

:::

| 索引类型 | 适用场景 | 内存消耗 | 精度 | 速度 |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">FlatIndex</font> | <font style="color:rgb(51, 51, 51);">小数据集精确搜索</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">100%</font> | <font style="color:rgb(51, 51, 51);">慢</font> |
| <font style="color:rgb(51, 51, 51);">IVF+Flat</font> | <font style="color:rgb(51, 51, 51);">中等规模平衡场景</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">95-98%</font> | <font style="color:rgb(51, 51, 51);">较快</font> |
| <font style="color:rgb(51, 51, 51);">IVF+PQ</font> | <font style="color:rgb(51, 51, 51);">大规模高压缩场景</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">85-95%</font> | <font style="color:rgb(51, 51, 51);">快</font> |
| <font style="color:rgb(51, 51, 51);">HNSW</font> | <font style="color:rgb(51, 51, 51);">超大规模低延迟场景</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">98-99%</font> | <font style="color:rgb(51, 51, 51);">最快</font> |
| <font style="color:rgb(51, 51, 51);">GPU_IVF_PQ</font> | <font style="color:rgb(51, 51, 51);">超十亿级数据实时检索</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">80-90%</font> | <font style="color:rgb(51, 51, 51);">极快</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **电商推荐系统**：
    - <font style="color:rgb(51, 51, 51);">使用HNSW实现10ms内检索10^8商品向量</font>
    - <font style="color:rgb(51, 51, 51);">结合用户行为序列构建动态索引</font>
2. **生物医药领域**：
    - <font style="color:rgb(51, 51, 51);">蛋白质结构检索：10^9级3D分子描述符向量</font>
    - <font style="color:rgb(51, 51, 51);">使用PQ将1TB数据压缩到40GB</font>
3. **金融风控系统**：
    - <font style="color:rgb(51, 51, 51);">交易行为模式检索：GPU集群实现毫秒级千亿量级检索</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **磁盘混合索引**：  
On-disk存储 + 内存缓存热点数据，支持10^12级别向量
2. **学习型量化**：

```python
# 使用深度网络学习量化器
learnable_quantizer = faiss.ProductQuantizer(d, M, nbits)
```

3. **联邦检索系统**：  
基于安全多方计算的分布式Faiss集群

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import faiss
import numpy as np

# 生成测试数据
d = 128
nb = 100000
nq = 1000
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((nq, d)).astype('float32')

# 构建IVF_PQ索引
nlist = 1024
quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexIVFPQ(quantizer, d, nlist, 8, 8)
index.train(xb)
index.add(xb)

# 搜索
k = 10
index.nprobe = 32
D, I = index.search(xq, k)

# 评估召回率
gt_index = faiss.IndexFlatL2(d)
gt_index.add(xb)
_, gt_I = gt_index.search(xq, k)
intersection = sum(len(set(a) & set(b)) for a,b in zip(I, gt_I))
recall = intersection / (k * nq)
print(f"Recall@{k}: {recall:.3f}")

```



<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">向量检索算法</font>
<font style="color:rgb(51, 51, 51);">### Python中的向量索引技术详解</font>

<font style="color:rgb(51, 51, 51);">向量索引是处理高维数据检索的核心技术，广泛应用于推荐系统、图像检索、NLP等领域。以下从七个维度全面解析其实现细节。</font>

#### <font style="color:rgb(51, 51, 51);">一、基本原理</font>
1. **<font style="color:rgb(51, 51, 51);">维度灾难</font>**<font style="color:rgb(51, 51, 51);">：传统索引方法在维度>10时效率急剧下降</font>
2. **<font style="color:rgb(51, 51, 51);">近似最近邻(ANN)</font>**<font style="color:rgb(51, 51, 51);">：牺牲精确度换取查询速度的核心思想</font>
3. **<font style="color:rgb(51, 51, 51);">空间映射策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">空间划分（KD-Tree, R-Tree）</font>
    - <font style="color:rgb(51, 51, 51);">哈希压缩（LSH）</font>
    - <font style="color:rgb(51, 51, 51);">向量量化（PQ, OPQ）</font>
    - <font style="color:rgb(51, 51, 51);">图结构（HNSW, NSG）</font>

#### <font style="color:rgb(51, 51, 51);">二、索引构建方法对比</font>
<font style="color:rgb(255, 255, 255);">复制</font>

| <font style="color:rgb(255, 255, 255);">方法</font> | <font style="color:rgb(255, 255, 255);">时间复杂度</font> | <font style="color:rgb(255, 255, 255);">空间复杂度</font> | <font style="color:rgb(255, 255, 255);">精度</font> | <font style="color:rgb(255, 255, 255);">适用维度</font> |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">KD-Tree</font> | <font style="color:rgb(51, 51, 51);">O(n log n)</font> | <font style="color:rgb(51, 51, 51);">O(n)</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);"><20</font> |
| <font style="color:rgb(51, 51, 51);">LSH</font> | <font style="color:rgb(51, 51, 51);">O(n)</font> | <font style="color:rgb(51, 51, 51);">O(nL)</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">任意</font> |
| <font style="color:rgb(51, 51, 51);">PQ</font> | <font style="color:rgb(51, 51, 51);">O(nk)</font> | <font style="color:rgb(51, 51, 51);">O(nm)</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">>100</font> |
| <font style="color:rgb(51, 51, 51);">HNSW</font> | <font style="color:rgb(51, 51, 51);">O(n log n)</font> | <font style="color:rgb(51, 51, 51);">O(n)</font> | <font style="color:rgb(51, 51, 51);">极高</font> | <font style="color:rgb(51, 51, 51);">>100</font> |


#### <font style="color:rgb(51, 51, 51);">三、核心算法计算步骤</font>
**<font style="color:rgb(51, 51, 51);">HNSW（Hierarchical Navigable Small World）示例</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">构建多层图结构（0层包含所有节点）</font>
2. <font style="color:rgb(51, 51, 51);">逐层概率衰减选择节点所在层</font>
3. <font style="color:rgb(51, 51, 51);">每层采用可导航小世界图结构</font>
4. <font style="color:rgb(51, 51, 51);">搜索时从顶层开始，逐步向下层细化</font>

<font style="color:rgb(51, 51, 51);">距离计算公式：  
</font><font style="color:rgb(51, 51, 51);">余弦相似度</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">A</font><font style="color:rgb(51, 51, 51);">⋅</font><font style="color:rgb(51, 51, 51);">B</font><font style="color:rgb(51, 51, 51);">∥</font><font style="color:rgb(51, 51, 51);">A</font><font style="color:rgb(51, 51, 51);">∥</font><font style="color:rgb(51, 51, 51);">∥</font><font style="color:rgb(51, 51, 51);">B</font><font style="color:rgb(51, 51, 51);">∥</font><font style="color:rgb(51, 51, 51);">余弦相似度</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">∥</font>**<font style="color:rgb(51, 51, 51);">A</font>**<font style="color:rgb(51, 51, 51);">∥∥</font>**<font style="color:rgb(51, 51, 51);">B</font>**<font style="color:rgb(51, 51, 51);">∥</font>**<font style="color:rgb(51, 51, 51);">A</font>**<font style="color:rgb(51, 51, 51);">⋅</font>**<font style="color:rgb(51, 51, 51);">B</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">欧氏距离</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">∑</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">d</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">A</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">B</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">欧氏距离</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">∑</font>_<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">1</font>_<font style="color:rgb(51, 51, 51);">d</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">A</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">−</font>_<font style="color:rgb(51, 51, 51);">B</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">2</font>

#### <font style="color:rgb(51, 51, 51);">四、优缺点分析</font>
**<font style="color:rgb(51, 51, 51);">KD-Tree</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 精确查找优秀</font>
+ <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 维度敏感性高，构建耗时</font>

**<font style="color:rgb(51, 51, 51);">LSH</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 常数级查询速度</font>
+ <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 哈希冲突导致精度损失</font>

**<font style="color:rgb(51, 51, 51);">PQ</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 高效压缩存储</font>
+ <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 子空间正交假设限制精度</font>

**<font style="color:rgb(51, 51, 51);">HNSW</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">✅</font><font style="color:rgb(51, 51, 51);"> 95%+召回率</font>
+ <font style="color:rgb(51, 51, 51);">❌</font><font style="color:rgb(51, 51, 51);"> 内存占用高，构建时间长</font>

#### <font style="color:rgb(51, 51, 51);">五、典型应用场景</font>
1. **<font style="color:rgb(51, 51, 51);">电商推荐</font>**<font style="color:rgb(51, 51, 51);">：用户向量最近邻检索（HNSW）</font>
2. **<font style="color:rgb(51, 51, 51);">图像检索</font>**<font style="color:rgb(51, 51, 51);">：百亿级特征库搜索（IVF-PQ）</font>
3. **<font style="color:rgb(51, 51, 51);">语义搜索</font>**<font style="color:rgb(51, 51, 51);">：文本嵌入快速匹配（LSH）</font>
4. **<font style="color:rgb(51, 51, 51);">生物信息学</font>**<font style="color:rgb(51, 51, 51);">：蛋白质结构相似性检索</font>

#### <font style="color:rgb(51, 51, 51);">六、性能优化策略</font>
1. **<font style="color:rgb(51, 51, 51);">混合索引</font>**<font style="color:rgb(51, 51, 51);">：IVF+HNSW（倒排索引引导图搜索）</font>
2. **<font style="color:rgb(51, 51, 51);">量化优化</font>**<font style="color:rgb(51, 51, 51);">：OPQ（正交投影提升量化效果）</font>
3. **<font style="color:rgb(51, 51, 51);">硬件加速</font>**<font style="color:rgb(51, 51, 51);">：GPU并行计算（Faiss-GPU）</font>
4. **<font style="color:rgb(51, 51, 51);">参数调优</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
python


# Faiss IVF参数优化示例
index = faiss.IndexIVFFlat(quantizer, dim, nlist)
index.train(data)  # 控制nlist平衡精度/速度
index.nprobe = 16  # 调整搜索范围
```

#### <font style="color:rgb(51, 51, 51);">七、完整代码实现（Faiss+HNSW）</font>
```plain
python


import faiss
import numpy as np

# 生成示例数据
d = 128  # 维度
nb = 100000  # 数据库大小
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')

# 构建HNSW索引
index = faiss.IndexHNSWFlat(d, 32)  # 32为邻接节点数
index.hnsw.efConstruction = 40  # 构建时邻居数
index.add(xb)

# 查询示例
k = 5  # 返回最近邻数
xq = np.random.random((1, d)).astype('float32')
index.hnsw.efSearch = 64  # 搜索时遍历数
D, I = index.search(xq, k)

print("最近邻索引:", I)
print("距离:", D)
```

#### <font style="color:rgb(51, 51, 51);">八、性能对比测试</font>
<font style="color:rgb(51, 51, 51);">在SIFT1M数据集（100万128维向量）上的表现：</font>

<font style="color:rgb(255, 255, 255);">复制</font>

| <font style="color:rgb(255, 255, 255);">方法</font> | <font style="color:rgb(255, 255, 255);">构建时间</font> | <font style="color:rgb(255, 255, 255);">查询延迟</font> | <font style="color:rgb(255, 255, 255);">召回率@10</font> |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">HNSW</font> | <font style="color:rgb(51, 51, 51);">98s</font> | <font style="color:rgb(51, 51, 51);">2.1ms</font> | <font style="color:rgb(51, 51, 51);">98.7%</font> |
| <font style="color:rgb(51, 51, 51);">IVF-PQ</font> | <font style="color:rgb(51, 51, 51);">45s</font> | <font style="color:rgb(51, 51, 51);">3.8ms</font> | <font style="color:rgb(51, 51, 51);">92.3%</font> |
| <font style="color:rgb(51, 51, 51);">LSH</font> | <font style="color:rgb(51, 51, 51);">12s</font> | <font style="color:rgb(51, 51, 51);">0.8ms</font> | <font style="color:rgb(51, 51, 51);">65.4%</font> |


#### <font style="color:rgb(51, 51, 51);">九、未来发展方向</font>
1. <font style="color:rgb(51, 51, 51);">学习型索引（Learned Indexes）</font>
2. <font style="color:rgb(51, 51, 51);">异构计算架构优化</font>
3. <font style="color:rgb(51, 51, 51);">动态更新支持</font>
4. <font style="color:rgb(51, 51, 51);">多模态联合索引</font>

#### <font style="color:rgb(51, 51, 51);">十、选型建议</font>
+ **<font style="color:rgb(51, 51, 51);">精度优先</font>**<font style="color:rgb(51, 51, 51);">：选择HNSW或NSG</font>
+ **<font style="color:rgb(51, 51, 51);">内存敏感</font>**<font style="color:rgb(51, 51, 51);">：使用PQ系列方法</font>
+ **<font style="color:rgb(51, 51, 51);">实时更新</font>**<font style="color:rgb(51, 51, 51);">：考虑DiskANN</font>
+ **<font style="color:rgb(51, 51, 51);">超大规模</font>**<font style="color:rgb(51, 51, 51);">：分布式方案（如Milvus）</font>

<font style="color:rgb(51, 51, 51);">通过合理选择索引策略，可以在千万级高维数据上实现毫秒级响应，同时保持90%以上的召回精度。实际应用中建议结合业务场景进行压力测试，不同数据分布可能显著影响算法表现。</font>

