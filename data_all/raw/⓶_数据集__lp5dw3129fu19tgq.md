# ⓶ 数据集

<!-- source: yuque://zhongxian-iiot9/hlyypb/lp5dw3129fu19tgq -->

# 数据集
| **维度** | **召回** | **粗排** | **精排** | **重排** |
| --- | --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据范围</font>** | <font style="color:rgb(51, 51, 51);">全量候选池</font> | <font style="color:rgb(51, 51, 51);">召回后的候选集</font> | <font style="color:rgb(51, 51, 51);">粗排后的候选集</font> | <font style="color:rgb(51, 51, 51);">精排后的排序列表</font> |
| **<font style="color:rgb(51, 51, 51);">负样本</font>** | <font style="color:rgb(51, 51, 51);">全局随机负采样</font> | <font style="color:rgb(51, 51, 51);">曝光未点击</font> | <font style="color:rgb(51, 51, 51);">曝光未点击（纠偏）</font> | <font style="color:rgb(51, 51, 51);">列表级负排列</font> |
| **<font style="color:rgb(51, 51, 51);">特征复杂度</font>** | <font style="color:rgb(51, 51, 51);">简单（ID+基础属性）</font> | <font style="color:rgb(51, 51, 51);">中（静态统计特征）</font> | <font style="color:rgb(51, 51, 51);">复杂（实时+交叉特征）</font> | <font style="color:rgb(51, 51, 51);">列表级全局特征</font> |
| **<font style="color:rgb(51, 51, 51);">标签定义</font>** | <font style="color:rgb(51, 51, 51);">单一交互行为（0/1）</font> | <font style="color:rgb(51, 51, 51);">单目标/多目标</font> | <font style="color:rgb(51, 51, 51);">多目标联合优化</font> | <font style="color:rgb(51, 51, 51);">列表级整体指标</font> |
| **<font style="color:rgb(51, 51, 51);">实时性要求</font>** | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">极高（在线学习）</font> |


## <font style="color:rgb(51, 51, 51);">1. 召回（Recall）</font>
**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：从全量候选集中快速筛选潜在相关物品。  
</font>**<font style="color:rgb(51, 51, 51);">训练数据特点</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(255, 255, 255);">复制</font>

| **维度** | **说明** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据量</font>** | **<font style="color:rgb(51, 51, 51);">全量数据</font>**<font style="color:rgb(51, 51, 51);">：覆盖所有用户和物品的长周期数据（如数周甚至数月）。</font> |
| **<font style="color:rgb(51, 51, 51);">样本构造</font>** | <font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">正样本</font>**<font style="color:rgb(51, 51, 51);">：用户显式反馈（点击、购买）或隐式反馈（长停留、重复播放）。   </font><font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">负样本</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">全局随机负采样</font>**<font style="color:rgb(51, 51, 51);">（从未交互的候选池中随机选取，比例较高）。</font> |
| **<font style="color:rgb(51, 51, 51);">特征设计</font>** | <font style="color:rgb(51, 51, 51);">- 轻量级特征：用户ID、物品ID、基础属性（类别、标签）。   </font><font style="color:rgb(51, 51, 51);">- 较少使用实时特征（如实时行为序列）。</font> |
| **<font style="color:rgb(51, 51, 51);">标签定义</font>** | <font style="color:rgb(51, 51, 51);">二元标签（0/1），直接关联用户与物品的交互行为。</font> |
| **<font style="color:rgb(51, 51, 51);">时间窗口</font>** | <font style="color:rgb(51, 51, 51);">长窗口（如30天以上），强调长期兴趣覆盖。</font> |


**<font style="color:rgb(51, 51, 51);">关键点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">负样本需多样性</font>**<font style="color:rgb(51, 51, 51);">：通过全局随机负采样避免模型偏向局部热点内容。</font>
+ **<font style="color:rgb(51, 51, 51);">特征简单</font>**<font style="color:rgb(51, 51, 51);">：模型需快速响应，避免复杂特征影响计算效率（如双塔模型仅需分离用户侧和物品侧特征）。</font>



## <font style="color:rgb(51, 51, 51);">2. 粗排（Pre-Ranking）</font>
**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：对召回结果进行初步排序，筛选高相关候选。  
</font>**<font style="color:rgb(51, 51, 51);">训练数据特点</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(255, 255, 255);">复制</font>

| **维度** | **说明** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据量</font>** | **<font style="color:rgb(51, 51, 51);">召回后数据</font>**<font style="color:rgb(51, 51, 51);">：仅包含召回阶段输出的候选集（千级到万级）。</font> |
| **<font style="color:rgb(51, 51, 51);">样本构造</font>** | <font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">正样本</font>**<font style="color:rgb(51, 51, 51);">：用户与召回候选的交互行为。   </font><font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">负样本</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">曝光未点击</font>**<font style="color:rgb(51, 51, 51);">（更贴近真实场景，避免全局负采样）。</font> |
| **<font style="color:rgb(51, 51, 51);">特征设计</font>** | <font style="color:rgb(51, 51, 51);">- 用户/物品静态特征（年龄、性别、品类）。   </font><font style="color:rgb(51, 51, 51);">- 简单动态特征（如近7天点击次数）。</font> |
| **<font style="color:rgb(51, 51, 51);">标签定义</font>** | <font style="color:rgb(51, 51, 51);">二元标签（是否</font>**<font style="color:#74B602;">点击/转化</font>**<font style="color:rgb(51, 51, 51);">），可能引入多目标（如点击率、收藏率）。</font> |
| **<font style="color:rgb(51, 51, 51);">时间窗口</font>** | <font style="color:rgb(51, 51, 51);">中窗口（如7-14天），平衡实时性与稳定性。</font> |


**<font style="color:rgb(51, 51, 51);">关键点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">负样本更精准</font>**<font style="color:rgb(51, 51, 51);">：仅使用召回阶段候选中的未交互样本，减少噪声。</font>
+ **<font style="color:rgb(51, 51, 51);">特征复杂度提升</font>**<font style="color:rgb(51, 51, 51);">：相比召回引入更多统计类特征（如用户历史CTR）。</font>



## <font style="color:rgb(51, 51, 51);">3. 精排（Ranking）</font>
**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：精准预估用户对候选的偏好，生成最终排序。  
</font>**<font style="color:rgb(51, 51, 51);">训练数据特点</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(255, 255, 255);">复制</font>

| **维度** | **说明** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据量</font>** | **<font style="color:rgb(51, 51, 51);">粗排后数据</font>**<font style="color:rgb(51, 51, 51);">：经过粗排筛选的高质量候选（百级到千级）。</font> |
| **<font style="color:rgb(51, 51, 51);">样本构造</font>** | <font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">正样本</font>**<font style="color:rgb(51, 51, 51);">：用户与精排候选的交互行为。   </font><font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">负样本</font>**<font style="color:rgb(51, 51, 51);">：曝光未点击（需解决样本选择偏差，可能引入纠偏方法如IPS）。</font> |
| **<font style="color:rgb(51, 51, 51);">特征设计</font>** | <font style="color:rgb(51, 51, 51);">- 丰富实时特征：用户实时行为序列（最近点击、搜索词）、上下文特征（时间、地点）。   </font><font style="color:rgb(51, 51, 51);">- 高阶交叉特征（如用户-物品交叉统计）。</font> |
| **<font style="color:rgb(51, 51, 51);">标签定义</font>** | <font style="color:rgb(51, 51, 51);">多目标优化（</font>**<font style="color:#74B602;">CTR、CVR、观看时长</font>**<font style="color:rgb(51, 51, 51);">），可能引入多任务学习框架。</font> |
| **<font style="color:rgb(51, 51, 51);">时间窗口</font>** | <font style="color:rgb(51, 51, 51);">短窗口（如1-7天），强调实时兴趣捕捉。</font> |


**<font style="color:rgb(51, 51, 51);">关键点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">特征细粒度</font>**<font style="color:rgb(51, 51, 51);">：使用用户实时行为（如最近5次点击的品类）、物品动态属性（如实时热度）。</font>
+ **<font style="color:rgb(51, 51, 51);">样本纠偏</font>**<font style="color:rgb(51, 51, 51);">：精排阶段的曝光数据存在选择偏差（仅能看到粗排筛选后的结果），需通过逆倾向评分（IPS）等方法校准。</font>



## <font style="color:rgb(51, 51, 51);">4. 重排（Re-Ranking）</font>
**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：优化推荐列表整体体验（多样性、业务规则）。  
</font>**<font style="color:rgb(51, 51, 51);">训练数据特点</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(255, 255, 255);">复制</font>

| **维度** | **说明** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">数据量</font>** | **<font style="color:rgb(51, 51, 51);">精排后数据</font>**<font style="color:rgb(51, 51, 51);">：精排输出的排序列表（十到百级）。</font> |
| **<font style="color:rgb(51, 51, 51);">样本构造</font>** | <font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">列表级正样本</font>**<font style="color:rgb(51, 51, 51);">：用户对推荐列表的整体反馈（如完播率、滑动深度）。   </font><font style="color:rgb(51, 51, 51);">-</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">列表级负样本</font>**<font style="color:rgb(51, 51, 51);">：随机打乱或低质量排列的列表。</font> |
| **<font style="color:rgb(51, 51, 51);">特征设计</font>** | <font style="color:rgb(51, 51, 51);">- 列表级特征：多样性指标（品类分布熵）、上下文连贯性（相邻物品相似度）。   </font><font style="color:rgb(51, 51, 51);">- 用户实时状态（如当前会话的已曝光品类）。</font> |
| **<font style="color:rgb(51, 51, 51);">标签定义</font>** | <font style="color:rgb(51, 51, 51);">列表级指标（如用户停留时长、互动率），可能引入强化学习的奖励信号。</font> |
| **<font style="color:rgb(51, 51, 51);">时间窗口</font>** | <font style="color:rgb(51, 51, 51);">极短窗口（如实时会话），强调即时反馈。</font> |


**<font style="color:rgb(51, 51, 51);">关键点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">上下文感知</font>**<font style="color:rgb(51, 51, 51);">：需建模物品间的相互影响（如避免同类物品扎堆）。</font>
+ **<font style="color:rgb(51, 51, 51);">强化学习</font>**<font style="color:rgb(51, 51, 51);">：部分场景使用在线学习，直接优化用户与列表的交互序列（如PPO算法）。</font>





# 数据不平衡如何处理
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在推荐系统中数据不平衡表现为：</font>

+ <font style="color:rgb(51, 51, 51);">召回阶段：正样本占比通常＜1%（如点击/购买），存在海量负样本</font>
+ <font style="color:rgb(51, 51, 51);">精排阶段：不同价值行为比例失衡（购买:收藏:点击≈1:10:100）</font>

:::

:::color5
**<font style="color:#601BDE;">1.召回模型解决方案</font>**

:::

1. **负采样优化：**  
• 随机负采样：基础方法，从非曝光或全库随机采样  
• Batch内负采样：利用同batch样本构建负例（YouTube DNN方案）  
• 混合负采样：随机负样本+曝光未点击样本  
• 对抗式负采样：通过GAN生成困难负样本

计算公式：  
 混合采样概率：P = α*P_random + (1-α)*P_hard

2. **损失函数改进：**  
• Focal Loss：抑制易分类样本权重  
FL(p_t) = -α_t(1-p_t)^γ log(p_t)  
（α=0.25, γ=2时效果最佳）
3. **温度缩放对比损失：**  
L = -log[exp(s_p/τ) / (exp(s_p/τ)+∑exp(s_n/τ))]  
τ＞1时平滑分布，缓解头部效应

:::color5
**<font style="color:#601BDE;">2.精排模型解决方案</font>**

:::

1. **样本重要性加权：**  
样本权重 = 1 + log(1 + 转化价值) × 时间衰减因子
2. **多目标学习：**  
**<font style="color:#74B602;">构建共享底层网络+多个任务塔结构</font>**：  
┌─点击率预测（主任务）  
├─收藏率预测（辅助任务）  
└─购买率预测（高价值任务）

损失函数：  
L = w1*_L_ctr + w2*_L_collect + w3*L_purchase  
（w3＞w2＞w1）

3. **序列建模：**  
使用Transformer编码用户行为序列：  
Attention(Q,K,V) = softmax(QK^T/√d)V

:::color5
**<font style="color:#601BDE;">3.优缺点对比</font>**

:::

| **方法** | **召回模型适用性** | **精排模型适用性** | **优点** | **缺点** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">负采样</font> | <font style="color:rgb(51, 51, 51);">★★★★☆</font> | <font style="color:rgb(51, 51, 51);">★★☆☆☆</font> | <font style="color:rgb(51, 51, 51);">实现简单</font> | <font style="color:rgb(51, 51, 51);">损失部分信息</font> |
| <font style="color:rgb(51, 51, 51);">Focal Loss</font> | <font style="color:rgb(51, 51, 51);">★★★☆☆</font> | <font style="color:rgb(51, 51, 51);">★★★★☆</font> | <font style="color:rgb(51, 51, 51);">无需改变数据分布</font> | <font style="color:rgb(51, 51, 51);">需调参优化</font> |
| <font style="color:rgb(51, 51, 51);">多任务学习</font> | <font style="color:rgb(51, 51, 51);">★★☆☆☆</font> | <font style="color:rgb(51, 51, 51);">★★★★☆</font> | <font style="color:rgb(51, 51, 51);">信息共享优势</font> | <font style="color:rgb(51, 51, 51);">增加计算复杂度</font> |
| <font style="color:rgb(51, 51, 51);">序列建模</font> | <font style="color:rgb(51, 51, 51);">★☆☆☆☆</font> | <font style="color:rgb(51, 51, 51);">★★★★☆</font> | <font style="color:rgb(51, 51, 51);">捕获时序关系</font> | <font style="color:rgb(51, 51, 51);">需要足够行为数据</font> |


:::color5
**<font style="color:#601BDE;">4.</font>**<font style="color:#601BDE;">工业级优化策略</font>

:::

1. 动态采样策略：
    - <font style="color:rgb(51, 51, 51);">根据实时表现调整采样率：困难样本采样率=错误率/(1-错误率)</font>
2. 增量课程学习：

```python
def curriculum_sampling(epoch):
    if epoch < 5:  # 初期阶段
        return 0.3  # 简单样本比例
    elif epoch < 10:
        return 0.6  # 中等难度
    else:
        return 0.9  # 困难样本
```

3. 特征级增强：
    - <font style="color:rgb(51, 51, 51);">对稀疏特征进行SMOTE过采样：</font>

```python
from imblearn.over_sampling import SMOTE
sm = SMOTE(k_neighbors=5)
X_res, y_res = sm.fit_resample(X_train, y_train)
```

:::color5
**<font style="color:#601BDE;">5.应用场景</font>**

:::

1. 电商推荐场景：
    - <font style="color:rgb(51, 51, 51);">召回阶段：采用混合负采样+温度缩放对比损失</font>
    - <font style="color:rgb(51, 51, 51);">精排阶段：使用多任务学习（CTR+CVR+客单价预测）</font>
2. 短视频推荐场景：
    - <font style="color:rgb(51, 51, 51);">召回阶段：Batch内负采样+Focal Loss</font>
    - <font style="color:rgb(51, 51, 51);">精排阶段：Transformer序列建模+观看时长加权</font>
3. 新闻推荐场景：
    - <font style="color:rgb(51, 51, 51);">召回阶段：基于用户阅读历史的对抗式负采样</font>
    - <font style="color:rgb(51, 51, 51);">精排阶段：多目标学习（点击率+阅读完成率）</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, inputs, targets):
        BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        pt = torch.exp(-BCE_loss)
        focal_loss = self.alpha * (1-pt)**self.gamma * BCE_loss
        return focal_loss.mean()

```

```python
def build_model():
    input = tf.keras.Input(shape=(256,))
    
    # Shared Bottom
    dense1 = Dense(128, activation='relu')(input)
    dense2 = Dense(64, activation='relu')(dense1)
    
    # Task Towers
    ctr_out = Dense(1, activation='sigmoid', name='ctr')(dense2)
    cvr_out = Dense(1, activation='sigmoid', name='cvr')(dense2)
    
    model = Model(inputs=input, outputs=[ctr_out, cvr_out])
    model.compile(
        optimizer='adam',
        loss={
            'ctr': tf.keras.losses.BinaryCrossentropy(),
            'cvr': tf.keras.losses.BinaryCrossentropy()
        },
        loss_weights={'ctr': 1.0, 'cvr': 3.0}
    )
    return model

```

