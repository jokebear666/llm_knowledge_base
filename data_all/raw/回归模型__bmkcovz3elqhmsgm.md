# 回归模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/bmkcovz3elqhmsgm -->

# 回归模型
| **算法** | **核心特点** | **适用场景** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">线性回归</font> | <font style="color:rgb(51, 51, 51);">简单快速、线性假设</font> | <font style="color:rgb(51, 51, 51);">低维线性数据</font> |
| <font style="color:rgb(51, 51, 51);">逻辑斯特回归</font> | <font style="color:rgb(51, 51, 51);">输出概率解释性强</font> | <font style="color:rgb(51, 51, 51);">二分类，多分类</font> |
| <font style="color:rgb(51, 51, 51);">岭回归/Lasso</font> | <font style="color:rgb(51, 51, 51);">正则化防止过拟合/特征选择</font> | <font style="color:rgb(51, 51, 51);">高维数据、共线性问题</font> |
| <font style="color:rgb(51, 51, 51);">决策树</font> | <font style="color:rgb(51, 51, 51);">非线性、可解释性</font> | <font style="color:rgb(51, 51, 51);">中小规模非结构化数据</font> |
| <font style="color:rgb(51, 51, 51);">随机森林</font> | <font style="color:rgb(51, 51, 51);">集成提升稳定性</font> | <font style="color:rgb(51, 51, 51);">高维非线性数据</font> |
| <font style="color:rgb(51, 51, 51);">GBRT</font> | <font style="color:rgb(51, 51, 51);">高精度、残差学习</font> | <font style="color:rgb(51, 51, 51);">复杂非线性关系</font> |
| <font style="color:rgb(51, 51, 51);">SVR</font> | <font style="color:rgb(51, 51, 51);">核方法处理非线性</font> | <font style="color:rgb(51, 51, 51);">小样本高维数据</font> |
| <font style="color:rgb(51, 51, 51);">神经网络</font> | <font style="color:rgb(51, 51, 51);">超高复杂度建模</font> | <font style="color:rgb(51, 51, 51);">大规模数据、计算资源充足</font> |


**<font style="color:rgb(51, 51, 51);">改进通用方法</font>**

1. **<font style="color:rgb(51, 51, 51);">数据预处理</font>**<font style="color:rgb(51, 51, 51);">：标准化、异常值处理。</font>
2. **<font style="color:rgb(51, 51, 51);">特征工程</font>**<font style="color:rgb(51, 51, 51);">：多项式扩展、交互特征。</font>
3. **<font style="color:rgb(51, 51, 51);">模型调参</font>**<font style="color:rgb(51, 51, 51);">：网格搜索/贝叶斯优化超参数。</font>
4. **<font style="color:rgb(51, 51, 51);">集成方法</font>**<font style="color:rgb(51, 51, 51);">：Stacking 或 Blending 多模型。</font>

# <font style="color:rgb(51, 51, 51);">线性回归 (Linear Regression)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：假设因变量</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">y</font>_<font style="color:rgb(51, 51, 51);">y</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">和自变量</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">X</font>_<font style="color:rgb(51, 51, 51);">X</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">存在线性关系，通过最小化预测值与真实值的残差平方和（RSS）拟合参数。</font>
+ **<font style="color:rgb(51, 51, 51);">数学形式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641064334-f0fca9bc-7a7e-4203-afe0-e51edb863d60.png)

<font style="color:rgb(51, 51, 51);">其中 β</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 为参数，ϵ 为误差项。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：均方误差（MSE）</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641143089-66118d7e-3749-4247-978d-53e2a7bf66ce.png)
2. **<font style="color:rgb(51, 51, 51);">参数求解</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">闭式解</font>**<font style="color:rgb(51, 51, 51);">（解析解）：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641147978-b31611a9-29c3-41c0-82f6-d9c2e1ff811f.png)
    - **<font style="color:rgb(51, 51, 51);">梯度下降</font>**<font style="color:rgb(51, 51, 51);">（迭代解）：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641156620-c802320e-60e3-4a4d-903e-6b9c2a12e371.png)

<font style="color:rgb(51, 51, 51);">其中 α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);"> 为学习率。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：简单高效、可解释性强、计算复杂度低（</font><font style="color:rgb(51, 51, 51);">O</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">p</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);">O</font>_<font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">n</font>__<font style="color:rgb(51, 51, 51);">p</font>_<font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：对非线性关系不敏感、易受多重共线性和异常值影响。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">特征与目标呈线性关系（如房价预测、销售量预测）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">添加正则化项（Lasso/Ridge）。</font>
+ <font style="color:rgb(51, 51, 51);">使用多项式特征扩展非线性能力。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

```



# <font style="color:rgb(51, 51, 51);">逻辑斯特回归（Logistic Regression）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">逻辑斯特回归是一种广义线性模型（GLM），</font>**<font style="color:rgb(51, 51, 51);">用于解决二分类问题</font>**<font style="color:rgb(51, 51, 51);">，通过概率映射预测类别标签。其核心是通过 </font>**<font style="color:rgb(51, 51, 51);">Sigmoid 函数</font>**<font style="color:rgb(51, 51, 51);">将线性组合的输入映射到 [0,1] 区间，输出样本属于正类的概率。</font>

:::

:::color5
**<font style="color:#601BDE;">1.核心原理</font>**

:::

1. **假设函数 (Hypothesis)**：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740642941648-23285c91-61d3-4546-bb23-56eb14fb9f0a.png)

其中，![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740642974167-2c697405-5953-4a7c-88b1-ad0f45c6928e.png)是 Sigmoid 函数，θ__为模型参数。

2. **概率解释**：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740642958390-baf72115-2b22-4bce-a135-8669a744ab80.png)

3. **<font style="color:rgb(51, 51, 51);">决策边界</font>**
+ <font style="color:rgb(51, 51, 51);">逻辑斯蒂回归的决策边界是超平面 θ</font><sup><font style="color:rgb(51, 51, 51);">T</font></sup><font style="color:rgb(51, 51, 51);">x=0，当 hθ(x)≥0.5 时预测为类别 1，否则为类别 0。</font>

:::color5
**<font style="color:#601BDE;">2.模型训练与优化</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">损失函数</font>**
+ **<font style="color:rgb(51, 51, 51);">交叉熵损失（Cross-Entropy Loss）：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643035489-c1dc97f9-bce6-49a4-930b-9f23974a123f.png)

<font style="color:rgb(51, 51, 51);">该函数衡量预测概率分布与真实标签分布的差异。</font>

2. **<font style="color:rgb(51, 51, 51);">参数估计</font>**
+ **最大似然估计（MLE）**：  
通过最大化对数似然函数求解参数：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643050388-28c5cda5-2293-484e-a560-3278900a81d9.png)

+ **梯度计算**：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643057958-ebef4c36-c208-440e-ab83-066895abaea4.png)

3. **<font style="color:rgb(51, 51, 51);">优化算法</font>**
+ **<font style="color:rgb(51, 51, 51);">梯度下降法</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643084490-7c34cbb9-b85b-43a0-97a8-8779921fa902.png)

<font style="color:rgb(51, 51, 51);">其中 α</font><font style="color:rgb(51, 51, 51);">为学习率，迭代直至收敛。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">输出概率解释性强</font> | <font style="color:rgb(51, 51, 51);">仅能处理线性可分或近似线性问题</font> |
| <font style="color:rgb(51, 51, 51);">训练效率高 (O(n⋅p))</font> | <font style="color:rgb(51, 51, 51);">对异常值敏感</font> |
| <font style="color:rgb(51, 51, 51);">支持 L1/L2 正则化防止过拟合</font> | <font style="color:rgb(51, 51, 51);">特征空间需要手动设计非线性组合</font> |
| <font style="color:rgb(51, 51, 51);">模型参数可解释性高</font> | <font style="color:rgb(51, 51, 51);">多重共线性可能导致参数估计不稳定</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **二分类任务**
    - <font style="color:rgb(51, 51, 51);">垃圾邮件检测（输入：邮件文本特征，输出：是否垃圾邮件）</font>
    - <font style="color:rgb(51, 51, 51);">客户流失预测（输入：用户行为数据，输出：是否流失）</font>
    - <font style="color:rgb(51, 51, 51);">疾病诊断（输入：医学指标，输出：患病/健康）</font>
2. **多分类扩展**  
通过 **One-vs-Rest (OvR)** 或 **Softmax 回归** 实现多分类（如手写数字识别）。

<font style="color:rgb(51, 51, 51);">逻辑斯蒂回归以简洁的数学形式和高效的计算性能，成为二分类问题的基准模型。通过正则化、特征工程等改进策略，可适应复杂场景。其概率输出特性在金融风控、医疗诊断等需量化风险评估的领域尤为重要。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 正则化</font>**

+ **<font style="color:rgb(51, 51, 51);">L1 正则化（Lasso）</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">稀疏化参数，自动特征选择：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643162512-29a08433-65aa-4552-bd98-eed0d2fd7270.png)

+ **<font style="color:rgb(51, 51, 51);">L2 正则化（Ridge）</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">防止过拟合，提升泛化能力：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643168387-4e8b52d0-c709-45ff-a3ef-f68ec62c1e64.png)

**<font style="color:rgb(51, 51, 51);">2. 处理类别不平衡</font>**

+ **<font style="color:rgb(51, 51, 51);">加权损失函数</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">对少数类样本赋予更高权重</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740643177822-e010d346-cab2-45d9-9fb1-a4b727f503d5.png)

+ <font style="color:rgb(51, 51, 51);">其中 w1 和 w0 分别为正负类权重。</font>

**<font style="color:rgb(51, 51, 51);">3. 非线性扩展</font>**

+ **<font style="color:rgb(51, 51, 51);">多项式特征工程</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">添加高阶项或交互项（如 x1</font><sup><font style="color:rgb(51, 51, 51);">2</font></sup><font style="color:rgb(51, 51, 51);">,x</font><sub><font style="color:rgb(51, 51, 51);">1</font></sub><font style="color:rgb(51, 51, 51);">x</font><sub><font style="color:rgb(51, 51, 51);">2</font></sub><font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">核逻辑斯蒂回归</font>**<font style="color:rgb(51, 51, 51);">：  
</font><font style="color:rgb(51, 51, 51);">通过核函数隐式映射到高维空间（需自定义实现）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

# 基模型
model = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs')

# 带类别权重的模型（处理不平衡数据）
model_balanced = LogisticRegression(class_weight={0:1, 1:10})

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC:", roc_auc_score(y_test, y_proba))

```

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, lr=0.01, epochs=1000):
    n, p = X.shape
    theta = np.zeros(p)
    
    for _ in range(epochs):
        z = X.dot(theta)
        h = sigmoid(z)
        gradient = X.T.dot(h - y) / n
        theta -= lr * gradient
    return theta

# 添加偏置项
X_train_b = np.c_[np.ones((X_train.shape[0], 1)), X_train]
theta = logistic_regression(X_train_b, y_train, lr=0.1, epochs=3000)

```

# <font style="color:rgb(51, 51, 51);">岭回归 (Ridge Regression)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：在线性回归的损失函数中添加 L2 正则化项，防止过拟合。</font>
+ **<font style="color:rgb(51, 51, 51);">数学形式</font>**<font style="color:rgb(51, 51, 51);">：</font>  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641234569-19bef8a5-d98e-4332-a853-516899158886.png)

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">参数求解：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641245134-d3a956eb-b813-49fd-98eb-8c1c5b5a14de.png)

<font style="color:rgb(51, 51, 51);">其中 λ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为正则化强度。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：解决多重共线性问题，提高模型稳定性。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：不进行特征选择，所有特征均保留。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">特征数量多且存在相关性（如基因数据）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">结合 L1 正则化（弹性网络）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.linear_model import Ridge

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
```





# <font style="color:rgb(51, 51, 51);">决策树回归</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：递归地将特征空间划分为区域，每个区域用均值预测。</font>
+ **<font style="color:rgb(51, 51, 51);">分裂准则</font>**<font style="color:rgb(51, 51, 51);">：最小化分裂后的 MSE：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641312390-33d6f466-2316-4a59-a4a9-53f6edc5faa9.png)

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：非线性建模、无需特征缩放。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：易过拟合、对数据微小变化敏感。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">非线性关系且需要可解释性（如客户分群预测）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">剪枝（设置最大深度）、集成方法（随机森林）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(max_depth=5)
model.fit(X_train, y_train)

```





# <font style="color:rgb(51, 51, 51);">随机森林回归</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：通过 Bagging 集成多棵决策树，输出平均预测值。</font>
+ **<font style="color:rgb(51, 51, 51);">随机性</font>**<font style="color:rgb(51, 51, 51);">：特征随机选择 + 样本自助采样（Bootstrap）。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：抗过拟合、处理高维数据。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：计算成本高、可解释性降低。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

```





# <font style="color:rgb(51, 51, 51);">梯度提升回归树 (GBRT)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：通过加法模型逐步拟合残差，使用梯度下降优化损失函数。</font>
+ **<font style="color:rgb(51, 51, 51);">数学形式</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740641376670-ae17773e-ab6b-4fbe-a11b-c3d312dcfbb2.png)

<font style="color:rgb(51, 51, 51);">其中 hm(x) 为第 m 棵树的预测值。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：高精度、灵活处理非线性。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：计算耗时、需调参（学习率、树数量）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.ensemble import GradientBoostingRegressor

model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

```





# <font style="color:rgb(51, 51, 51);">支持向量回归 (SVR)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：构建一个间隔带，最大化预测误差在容忍度（ϵ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">）内的样本数量。</font>
+ **<font style="color:rgb(51, 51, 51);">核技巧</font>**<font style="color:rgb(51, 51, 51);">：通过核函数（如 RBF）映射到高维空间处理非线性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：高维有效、鲁棒性强。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：计算复杂度高（O(n3)）、需调参（C,ϵ）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from sklearn.svm import SVR

model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
model.fit(X_train, y_train)

```

