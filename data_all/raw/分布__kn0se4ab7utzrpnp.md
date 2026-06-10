# 分布

<!-- source: yuque://zhongxian-iiot9/hlyypb/kn0se4ab7utzrpnp -->

# <font style="color:rgb(51, 51, 51);">分布选择原则</font>
1. **<font style="color:rgb(51, 51, 51);">问题类型</font>**<font style="color:rgb(51, 51, 51);">：离散事件（二项/泊松） vs 连续测量（正态/指数）。</font>
2. **<font style="color:rgb(51, 51, 51);">数据特征</font>**<font style="color:rgb(51, 51, 51);">：对称性、尾部厚度、边界（如仅非负值）。</font>
3. **<font style="color:rgb(51, 51, 51);">生成机制</font>**<font style="color:rgb(51, 51, 51);">：例如事件是否独立（泊松过程）、是否涉及成功/失败（二项）。</font>

<font style="color:rgb(51, 51, 51);">通过结合领域知识和统计检验（如 KS 检验）可最终确定最优分布。</font>

# 一、离散分布
## 二项分布
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">描述 </font>**<font style="color:rgb(51, 51, 51);">n 次独立伯努利试验中成功次数 k</font>**<font style="color:rgb(51, 51, 51);"> 的概率分布，单次试验成功概率为 p。</font>

:::

**<font style="color:rgb(51, 51, 51);">率质量函数 (PMF)</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740626438679-bc0aaae1-71f6-4e62-882c-2f33e1c4d746.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算组合数 C(n,k)；</font>
2. <font style="color:rgb(51, 51, 51);">计算 p</font><sup><font style="color:rgb(51, 51, 51);">k</font></sup><font style="color:rgb(51, 51, 51);"> 和 (1−p)</font><sup><font style="color:rgb(51, 51, 51);">n−k</font></sup><font style="color:rgb(51, 51, 51);">；</font>
3. <font style="color:rgb(51, 51, 51);">三者相乘得概率值。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：易于理解，适用于二元结果场景。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：假设试验独立且概率固定，现实中可能不成立。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">抛硬币正面次数</font>
+ <font style="color:rgb(51, 51, 51);">产品合格率检验</font>
+ <font style="color:rgb(51, 51, 51);">广告点击率预测</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import numpy as np
from scipy.stats import binom

n, p = 10, 0.3
k = np.arange(0, n+1)
pmf = binom.pmf(k, n, p)  # 计算PMF
mean, var = binom.stats(n, p)  # 计算均值与方差

```

## <font style="color:rgb(51, 51, 51);">泊松分布 (Poisson Distribution)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">描述 </font>**<font style="color:rgb(51, 51, 51);">单位时间/空间内随机事件发生次数</font>**<font style="color:rgb(51, 51, 51);"> 的分布，参数 λ 表示平均发生次数。</font>

:::

**<font style="color:rgb(51, 51, 51);">概率质量函数 (PMF)</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740626495145-1d5cff06-4fd5-4619-b310-0b1e150042b3.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算 λ</font><sup><font style="color:rgb(51, 51, 51);">k</font></sup><font style="color:rgb(51, 51, 51);">；</font>
2. <font style="color:rgb(51, 51, 51);">计算 e</font><sup><font style="color:rgb(51, 51, 51);">−λ</font></sup><font style="color:rgb(51, 51, 51);">；</font>
3. <font style="color:rgb(51, 51, 51);">计算 k!</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">；</font>
4. <font style="color:rgb(51, 51, 51);">三者相除得概率值。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：易于理解，适用于二元结果场景。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：假设试验独立且概率固定，现实中可能不成立。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">抛硬币正面次数</font>
+ <font style="color:rgb(51, 51, 51);">产品合格率检验</font>
+ <font style="color:rgb(51, 51, 51);">广告点击率预测</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from scipy.stats import poisson

lambda_ = 5  # 平均发生次数
k = 3
prob = poisson.pmf(k, lambda_)  # 计算P(X=3)

```



## <font style="color:rgb(51, 51, 51);">几何分布 (Geometric Distribution)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">描述 </font>**<font style="color:rgb(51, 51, 51);">首次成功所需的伯努利试验次数</font>**<font style="color:rgb(51, 51, 51);">，单次成功概率为 p。</font>

:::

**<font style="color:rgb(51, 51, 51);">概率质量函数 (PMF)</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740626978277-b15abcd0-1727-4cf8-b1d1-d83a5aa7b7f1.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">首次中奖需要的抽奖次数</font>
+ <font style="color:rgb(51, 51, 51);">设备首次故障前的工作周期</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python

```







# <font style="color:rgb(51, 51, 51);">二、连续型分布</font>
## <font style="color:rgb(51, 51, 51);">1. 正态分布 (Normal Distribution)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">对称的钟形分布，参数为均值 μ 和标准差 σ。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">概率密度函数 (PDF)</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740626563923-62ddec16-f1ea-49ad-9fd4-8974cd6d9d90.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：中心极限定理保证大量独立变量和的分布趋近正态。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：对极端值敏感（厚尾数据不适用）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">人类身高/体重分布</font>
+ <font style="color:rgb(51, 51, 51);">测量误差建模</font>
+ <font style="color:rgb(51, 51, 51);">金融收益率的对数变换</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from scipy.stats import norm

mu, sigma = 0, 1
x = 1.96
pdf = norm.pdf(x, mu, sigma)  # 计算密度值
cdf = norm.cdf(x, mu, sigma)  # 计算累积概率P(X ≤ 1.96)

```







## <font style="color:rgb(51, 51, 51);">2.指数分布 (Exponential Distribution)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">描述 </font>**<font style="color:rgb(51, 51, 51);">独立事件发生的时间间隔</font>**<font style="color:rgb(51, 51, 51);">，参数 λ 表示单位时间发生率。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">概率密度函数 (PDF)</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740626692096-58bda048-34c9-467e-8b7a-ddaccf0df2b9.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">设备寿命建模</font>
+ <font style="color:rgb(51, 51, 51);">客户到达时间间隔</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from scipy.stats import expon

lambda_ = 0.5  # 发生率参数
scale = 1/lambda_  # Scipy中使用scale=1/λ
x = 2
pdf = expon.pdf(x, scale=scale)

```



## <font style="color:rgb(51, 51, 51);">3.</font>**<font style="color:rgb(51, 51, 51);">伽马分布 (Gamma Distribution)</font>**
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">描述 </font>**<font style="color:rgb(51, 51, 51);">n 个独立指数事件发生所需时间</font>**<font style="color:rgb(51, 51, 51);">，参数 α（形状参数）和 β（速率参数）。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">概率密度函数 (PDF)</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740626763017-5eb11431-42dc-4e01-8141-c6ad5b56abd7.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">累计降雨量分析</font>
+ <font style="color:rgb(51, 51, 51);">金融资产收益率建模</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from scipy.stats import expon

lambda_ = 0.5  # 发生率参数
scale = 1/lambda_  # Scipy中使用scale=1/λ
x = 2
pdf = expon.pdf(x, scale=scale)

```



## **<font style="color:rgb(51, 51, 51);">4. 卡方分布（Chi-square Distribution）</font>**
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：若 Z1,Z2,…,Zk是 </font>**<font style="color:rgb(51, 51, 51);">k 个独立的标准正态变量</font>**<font style="color:rgb(51, 51, 51);">（Zi∼N(0,1)），则它们的平方和服从自由度为 k的卡方分布：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740627775399-2900deed-f6a5-4ac2-bf0e-8c06654e06cf.png)
+ **<font style="color:rgb(51, 51, 51);">概率密度函数（PDF）</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740627786339-03e88b68-e0fd-478b-9fad-3666f6b564c2.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 Γ 是伽马函数，k 是自由度。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">确定自由度</font>**<font style="color:rgb(51, 51, 51);">：自由度 k</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">通常等于数据中独立变量的个数减去约束条件数（例如，卡方检验中的类别数减1）。</font>
2. **<font style="color:rgb(51, 51, 51);">计算统计量</font>**<font style="color:rgb(51, 51, 51);">：例如卡方检验中的统计量：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740627739477-1c7b0bb8-69dd-423a-9185-bcf09b50f625.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 Oi 是观测频数，Ei</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是期望频数。</font>
3. **<font style="color:rgb(51, 51, 51);">查表或计算 P 值</font>**<font style="color:rgb(51, 51, 51);">：根据卡方分布表或函数计算临界值或 P 值。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">适用于检验分类变量的独立性或拟合优度。</font>
    - <font style="color:rgb(51, 51, 51);">对样本量敏感，大样本时结果更稳定。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">要求观测值独立且期望频数不过小（通常</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">E</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">≥</font><font style="color:rgb(51, 51, 51);">5</font>_<font style="color:rgb(51, 51, 51);">E</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">≥</font><font style="color:rgb(51, 51, 51);">5</font><font style="color:rgb(51, 51, 51);">）。</font>
    - <font style="color:rgb(51, 51, 51);">对连续数据需先离散化（分箱）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">独立性检验</font>**<font style="color:rgb(51, 51, 51);">：检验两个分类变量是否独立（如性别与购物偏好）。</font>
+ **<font style="color:rgb(51, 51, 51);">拟合优度检验</font>**<font style="color:rgb(51, 51, 51);">：检验样本数据是否符合某理论分布（如正态分布）。</font>
+ **<font style="color:rgb(51, 51, 51);">方差分析</font>**<font style="color:rgb(51, 51, 51);">：检验正态分布总体的方差是否相等。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import numpy as np
from scipy.stats import chi2

# 示例：卡方检验（独立性检验）
from scipy.stats import chi2_contingency

# 创建2x2列联表
obs = np.array([[50, 30], [40, 60]])
chi2_stat, p_value, dof, expected = chi2_contingency(obs)
print(f"卡方统计量: {chi2_stat:.2f}, P值: {p_value:.4f}, 自由度: {dof}")

# 卡方分布的概率计算
k = 3  # 自由度
x = 5  # 统计量值
pdf = chi2.pdf(x, k)      # 计算PDF在x处的值
cdf = chi2.cdf(x, k)      # 计算P(X ≤ x)
p_value = 1 - cdf         # 右尾概率P(X > x)

```





## **<font style="color:rgb(51, 51, 51);">5.t 分布（Student’s t-Distribution）</font>**
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：当总体标准差未知且样本量小（n<30</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">）时，用于估计正态分布总体均值的分布。</font>
+ **<font style="color:rgb(51, 51, 51);">概率密度函数（PDF）</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740628205805-ba496815-8a5f-4bbc-b125-1490abc814ad.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 ν=n−1 是自由度，n</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为样本量。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">计算样本均值 xˉ</font>**_**<font style="color:rgb(51, 51, 51);">x</font>**_**<font style="color:rgb(51, 51, 51);">ˉ 和样本标准差 s</font>**_**<font style="color:rgb(51, 51, 51);">s</font>**_<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740628219472-64a6278b-aeb2-4359-a196-6b19278316f1.png)
2. **<font style="color:rgb(51, 51, 51);">计算 t 统计量</font>**<font style="color:rgb(51, 51, 51);">：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740628225709-7c33f45a-0eb3-4b83-9bbe-334ef02cd51d.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 μ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 是假设的总体均值。</font>
3. **<font style="color:rgb(51, 51, 51);">查表或计算 P 值</font>**<font style="color:rgb(51, 51, 51);">：根据自由度和 t 值查 t 分布表或使用函数计算。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">小样本下更准确（相比正态分布）。</font>
    - <font style="color:rgb(51, 51, 51);">尾部比正态分布更厚，减少第一类错误风险。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">当样本量较大（</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">≥</font><font style="color:rgb(51, 51, 51);">30</font>_<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);">≥</font><font style="color:rgb(51, 51, 51);">30</font><font style="color:rgb(51, 51, 51);">）时，t 分布近似正态分布，此时优势不明显。</font>
    - <font style="color:rgb(51, 51, 51);">严格假设数据来自正态分布总体（可通过 Shapiro-Wilk 检验验证）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">单样本 t 检验</font>**<font style="color:rgb(51, 51, 51);">：检验样本均值是否等于某理论值（如药物效果是否显著）。</font>
+ **<font style="color:rgb(51, 51, 51);">双样本 t 检验</font>**<font style="color:rgb(51, 51, 51);">：比较两组独立样本的均值差异（如 A/B 测试）。</font>
+ **<font style="color:rgb(51, 51, 51);">置信区间估计</font>**<font style="color:rgb(51, 51, 51);">：构造总体均值的置信区间（如估计用户平均停留时间）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import numpy as np
from scipy.stats import t

# 示例：单样本t检验
sample = np.array([3.2, 3.5, 2.9, 3.1, 3.4])  # 样本数据
mu0 = 3.0  # 假设的总体均值
n = len(sample)
df = n - 1  # 自由度
t_stat = (np.mean(sample) - mu0) / (np.std(sample, ddof=1) / np.sqrt(n))
p_value = 2 * (1 - t.cdf(abs(t_stat), df))  # 双尾检验
print(f"t统计量: {t_stat:.2f}, P值: {p_value:.4f}")

# t分布的概率计算
x = 1.96  # t值
pdf = t.pdf(x, df)    # 计算PDF在x处的值
cdf = t.cdf(x, df)    # 计算P(T ≤ x)

```



