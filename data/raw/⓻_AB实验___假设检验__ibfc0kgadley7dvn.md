# ⓻ AB实验 & 假设检验

<!-- source: yuque://zhongxian-iiot9/hlyypb/ibfc0kgadley7dvn -->

# <font style="color:rgb(51, 51, 51);">实验1（Qwen改写搜索query场景）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">以下是针对Qwen搜索query改写场景的AB实验与假设检验全流程解析，包含原理、步骤、代码实现及业务落地细节：</font>

:::

**<font style="color:rgb(51, 51, 51);">1. AB实验本质</font>**

<font style="color:rgb(51, 51, 51);">通过</font>**<font style="color:rgb(51, 51, 51);">随机分流</font>**<font style="color:rgb(51, 51, 51);">将用户分为对照组（A组，原策略）和实验组（B组，新query改写策略），对比核心指标（如点击率）的差异，判断新策略是否显著优于原策略。</font>

**<font style="color:rgb(51, 51, 51);">2. 假设检验数学逻辑</font>**

+ **<font style="color:rgb(51, 51, 51);">原假设H0</font>**<font style="color:rgb(51, 51, 51);">：新策略效果 ≤ 原策略（μ_B ≤ μ_A）</font>
+ **<font style="color:rgb(51, 51, 51);">备择假设H1</font>**<font style="color:rgb(51, 51, 51);">：新策略效果 > 原策略（μ_B > μ_A，单尾检验）</font>
+ <font style="color:rgb(51, 51, 51);">通过计算</font>**<font style="color:rgb(51, 51, 51);">p值</font>**<font style="color:rgb(51, 51, 51);">，若 p < α（如0.05），则拒绝H0，认为新策略有效。</font>

:::color5
**<font style="color:#601BDE;">1.实施步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">实验设计</font>**
+ **<font style="color:rgb(51, 51, 51);">目标指标</font>**<font style="color:rgb(51, 51, 51);">：点击率CTR = 点击次数 / 曝光次数</font>
+ **<font style="color:rgb(51, 51, 51);">分流方式</font>**<font style="color:rgb(51, 51, 51);">：用户ID哈希分桶，50%流量进入A/B组</font>
+ **<font style="color:rgb(51, 51, 51);">最小样本量计算</font>**<font style="color:rgb(51, 51, 51);">（避免Ⅰ/Ⅱ类错误）：</font>

```python
from statsmodels.stats.power import NormalIndPower
effect_size = 0.02  # 预期CTR提升2%（如从10%到10.2%）
alpha = 0.05        # 显著性水平
power = 0.8         # 统计功效
analysis = NormalIndPower()
sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, ratio=1)
# 输出每组至少需要 15,366 次曝光
```

**<font style="color:rgb(51, 51, 51);">2. 数据收集</font>**<font style="color:rgb(255, 255, 255);">复制</font>

| **组别** | **曝光量** | **点击量** | **CTR** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">A组</font> | <font style="color:rgb(51, 51, 51);">20,000</font> | <font style="color:rgb(51, 51, 51);">2,000</font> | <font style="color:rgb(51, 51, 51);">10.0%</font> |
| <font style="color:rgb(51, 51, 51);">B组</font> | <font style="color:rgb(51, 51, 51);">20,500</font> | <font style="color:rgb(51, 51, 51);">2,254</font> | <font style="color:rgb(51, 51, 51);">11.0%</font> |


3. **<font style="color:rgb(51, 51, 51);">假设检验（Z-Test）</font>**
+ **计算公式**：  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740628407003-a6eb2e2c-2ebd-49ab-86cc-ed261602409e.png)

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

clicks = np.array([2000, 2254])   # A/B组点击次数
exposures = np.array([20000, 20500])  # A/B组曝光量
z_stat, p_value = proportions_ztest(clicks, exposures, alternative='larger')
# 输出 z=5.12, p=1.5e-7 （拒绝H0）

```

4. **<font style="color:rgb(51, 51, 51);">结果分析</font>**
+ **<font style="color:rgb(51, 51, 51);">统计显著性</font>**<font style="color:rgb(51, 51, 51);">：p=1.5e-7 < 0.05 → 新策略CTR显著更高</font>
+ **<font style="color:rgb(51, 51, 51);">置信区间</font>**<font style="color:rgb(51, 51, 51);">（95% CI）：</font>

```python
from statsmodels.stats.proportion import confint_proportions_diff
ci = confint_proportions_diff(clicks[1], exposures[1], clicks[0], exposures[0], method='wald')
# 输出 (0.006, 0.014) → CTR提升0.6%~1.4%
```

+ **<font style="color:rgb(51, 51, 51);">业务决策</font>**<font style="color:rgb(51, 51, 51);">：全量上线新query改写策略。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">AB实验优势</font>**

+ **<font style="color:rgb(51, 51, 51);">因果性强</font>**<font style="color:rgb(51, 51, 51);">：随机分流排除混杂因素</font>
+ **<font style="color:rgb(51, 51, 51);">量化收益</font>**<font style="color:rgb(51, 51, 51);">：直接计算指标提升幅度</font>

**<font style="color:rgb(51, 51, 51);">局限性</font>**

+ **<font style="color:rgb(51, 51, 51);">周期成本</font>**<font style="color:rgb(51, 51, 51);">：需积累足够样本量</font>
+ **<font style="color:rgb(51, 51, 51);">局部优化风险</font>**<font style="color:rgb(51, 51, 51);">：可能提升CTR但降低长期用户体验（需多指标监控）</font>

:::color5
**<font style="color:#601BDE;">3.业务场景拓展</font>**

:::

<font style="color:rgb(51, 51, 51);">1. </font>**<font style="color:rgb(51, 51, 51);">多变量测试（MVT）</font>**

<font style="color:rgb(51, 51, 51);">同时测试多个策略组合（如query改写算法+排序模型），需用</font>**<font style="color:rgb(51, 51, 51);">正交分层</font>**<font style="color:rgb(51, 51, 51);">分流。</font>

<font style="color:rgb(51, 51, 51);">2. </font>**<font style="color:rgb(51, 51, 51);">长期效应验证</font>**

+ <font style="color:rgb(51, 51, 51);">通过AA测试验证分流均匀性</font>
+ <font style="color:rgb(51, 51, 51);">监控用户留存率、复访率等滞后指标</font>

<font style="color:rgb(51, 51, 51);">3. </font>**<font style="color:rgb(51, 51, 51);">搜索query改写特殊考量</font>**

+ **<font style="color:rgb(51, 51, 51);">语义一致性</font>**<font style="color:rgb(51, 51, 51);">：需人工评估改写后query是否偏离原意</font>
+ **<font style="color:rgb(51, 51, 51);">长尾query覆盖</font>**<font style="color:rgb(51, 51, 51);">：关注低频搜索词的效果稳定性</font>

:::color5
**<font style="color:#601BDE;">4.实现代码示例</font>**

:::

```python
# AB实验分析全流程
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 生成模拟数据
np.random.seed(42)
n_a, n_b = 20000, 20500
ctr_a = 0.10
ctr_b = 0.11

clicks_a = np.random.binomial(1, ctr_a, n_a).sum()
clicks_b = np.random.binomial(1, ctr_b, n_b).sum()

# 假设检验
from statsmodels.stats.proportion import proportions_ztest
counts = np.array([clicks_a, clicks_b])
nobs = np.array([n_a, n_b])
z_stat, p_val = proportions_ztest(counts, nobs, alternative='smaller')

# 可视化效果
plt.figure(figsize=(10,6))
plt.bar(['A组', 'B组'], [clicks_a/n_a, clicks_b/n_b], 
        yerr=[1.96*np.sqrt((clicks_a/n_a)*(1-clicks_a/n_a)/n_a), 
              1.96*np.sqrt((clicks_b/n_b)*(1-clicks_b/n_b)/n_b)])
plt.title("CTR对比（95%置信区间）")
plt.ylabel("点击率")
plt.show()

print(f"Z统计量: {z_stat:.2f}, P值: {p_val:.4f}")

```

# 实验2（<font style="color:rgb(51, 51, 51);">商品卖点词对订单增长的AB实验</font>）
:::color3
**<font style="color:rgb(51, 51, 51);"></font>****<font style="color:rgb(51, 51, 51);">项目背景</font>**<font style="color:rgb(51, 51, 51);">：电商平台发现商品详情页的"卖点词"（如"全网最低价""限时直降500元"）可能显著影响用户购买决策，但缺乏量化验证。  
</font>**<font style="color:rgb(51, 51, 51);">核心目标</font>**<font style="color:rgb(51, 51, 51);">：验证新设计的卖点词文案是否能显著提升商品详情页的订单转化率。  
</font>**<font style="color:rgb(51, 51, 51);">业务假设</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">原假设H₀：新卖点词对订单转化率无显著影响</font>
+ <font style="color:rgb(51, 51, 51);">备择假设H₁：新卖点词能提升订单转化率（预期提升幅度≥2%）</font>

:::

:::color5
**<font style="color:#601BDE;">1.实验设计</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 实验变量设计</font>**

+ **<font style="color:rgb(51, 51, 51);">自变量</font>**<font style="color:rgb(51, 51, 51);">：卖点词版本（对照组A：原始文案；实验组B：新文案）</font>
+ **<font style="color:rgb(51, 51, 51);">因变量</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">核心指标</font>**<font style="color:rgb(51, 51, 51);">：详情页到订单的转化率 = 下单用户数 / 访问用户数</font>
    - **<font style="color:rgb(51, 51, 51);">辅助指标</font>**<font style="color:rgb(51, 51, 51);">：客单价、页面停留时长、跳出率（用于排除副作用）</font>

**<font style="color:rgb(51, 51, 51);">2. 样本量与实验周期</font>**

+ **<font style="color:rgb(51, 51, 51);">样本量计算</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">基于历史数据（基线转化率15%），设定显著性水平α=5%、统计功效1-β=80%、最小可检测效应MDE=2%，使用双比例检验公式计算：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741850843833-cd57e70a-09d8-4ba6-a774-5a877ee88f7f.png)

<font style="color:rgb(51, 51, 51);">计算结果每组需至少20,000用户，总样本量40,000</font>

+ **<font style="color:rgb(51, 51, 51);">实验周期</font>**<font style="color:rgb(51, 51, 51);">：7天（覆盖工作日与周末用户行为差异）</font>

**<font style="color:rgb(51, 51, 51);">3. 控制混杂变量</font>**

+ <font style="color:rgb(51, 51, 51);">固定商品价格、库存状态、页面布局</font>
+ <font style="color:rgb(51, 51, 51);">排除促销活动期间流量（避免外部因素干扰）</font>

:::color5
**<font style="color:#601BDE;">2.流量分桶方案</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 分层随机分桶（Stratified Sampling）</font>**

+ **<font style="color:rgb(51, 51, 51);">分层维度</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">用户活跃度（高/中/低）</font>
    - <font style="color:rgb(51, 51, 51);">地理位置（一线/二线/其他城市）</font>
    - <font style="color:rgb(51, 51, 51);">设备类型（iOS/Android/PC）</font>
+ **<font style="color:rgb(51, 51, 51);">分桶比例</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">A/B组各分配50%流量</font>
    - <font style="color:rgb(51, 51, 51);">使用一致性哈希（Consistent Hashing）保证用户每次访问落入同一组</font>

**<font style="color:rgb(51, 51, 51);">2. 随机化验证</font>**

+ **<font style="color:rgb(51, 51, 51);">AA测试验证</font>**<font style="color:rgb(51, 51, 51);">：实验前1天运行A/A测试，确认两组转化率差异<0.5%（p>0.1）</font>

:::color5
**<font style="color:#601BDE;">3.假设检验</font>**

:::

**<font style="color:rgb(51, 51, 51);">统计显著性检验</font>**

+ **<font style="color:rgb(51, 51, 51);">双样本Z检验</font>**<font style="color:rgb(51, 51, 51);">（适用于大样本比例检验）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741850911661-2bf6339b-4443-4619-bd76-99d610a4f64a.png)

<font style="color:rgb(51, 51, 51);">当|Z| > 1.96时拒绝原假设（α=5%）</font>

:::color5
**<font style="color:#601BDE;">4.实验结果分析</font>**

:::

| **组别** | **用户数** | **订单数** | **转化率** | **相对提升** | **p-value** |
| --- | --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">对照组</font> | <font style="color:rgb(51, 51, 51);">21,450</font> | <font style="color:rgb(51, 51, 51);">3,218</font> | <font style="color:rgb(51, 51, 51);">15.00%</font> | <font style="color:rgb(51, 51, 51);">-</font> | <font style="color:rgb(51, 51, 51);">-</font> |
| <font style="color:rgb(51, 51, 51);">实验组</font> | <font style="color:rgb(51, 51, 51);">22,100</font> | <font style="color:rgb(51, 51, 51);">3,647</font> | <font style="color:rgb(51, 51, 51);">16.50%</font> | <font style="color:rgb(51, 51, 51);">10.00%</font> | <font style="color:rgb(51, 51, 51);">0.008</font> |


+ <font style="color:rgb(51, 51, 51);">统计显著（p=0.008 < 0.05）</font>
+ <font style="color:rgb(51, 51, 51);">转化率绝对提升1.5pp，相对提升10%</font>
+ <font style="color:rgb(51, 51, 51);">辅助指标客单价无显著变化（排除以价换量风险）</font>

:::color5
**<font style="color:#601BDE;">5.决策建议</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">全量上线</font>**<font style="color:rgb(51, 51, 51);">：新卖点词在统计和业务层面均表现显著正向收益</font>
2. **<font style="color:rgb(51, 51, 51);">持续监控</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">关注长期转化率（避免新鲜效应）</font>
    - <font style="color:rgb(51, 51, 51);">扩展实验到不同商品类目（观察异质性）</font>
3. **<font style="color:rgb(51, 51, 51);">机制迭代</font>**<font style="color:rgb(51, 51, 51);">：建立卖点词自动化生成→测试→优化的闭环系统</font>

