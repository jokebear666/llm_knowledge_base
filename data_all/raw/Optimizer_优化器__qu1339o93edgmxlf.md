# Optimizer 优化器

<!-- source: yuque://zhongxian-iiot9/hlyypb/qu1339o93edgmxlf -->

# <font style="color:rgb(51, 51, 51);">随机梯度下降（SGD）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">SGD是一种简单的优化方法，它通过随机选取一个样本或小批量样本，计算梯度，并沿负梯度方向更新参数。SGD适用于数据量大的情况，但收敛速度较慢。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">选择一个批量数据。</font>
2. <font style="color:rgb(51, 51, 51);">计算该批量数据的梯度。</font>
3. <font style="color:rgb(51, 51, 51);">按照学习率更新参数： </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878541776-3e25c497-42b5-4d02-b572-5e5e1de03768.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：简单易实现，适用于任何问题。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：收敛速度慢，容易陷入鞍点，需要手动调整学习率。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于数据量较小或初始阶段的模型训练。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

<font style="color:rgb(51, 51, 51);">引入动量、学习率衰减。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def SGD(params, learning_rate):
    for param in params:
        param.data -= learning_rate * param.grad.data
```



# <font style="color:rgb(51, 51, 51);">AdaGrad</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">AdaGrad通过自适应调整学习率，根据历史梯度平方的累计来调整每个参数的学习率。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算梯度。</font>
2. <font style="color:rgb(51, 51, 51);">计算历史梯度平方的累加：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878578355-03ab9be2-e31b-4c0b-93b6-fe11aa5c2f04.png)
3. <font style="color:rgb(51, 51, 51);">更新参数： </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878586542-02afbe43-7f30-4c88-b7bd-00441011069a.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：适合稀疏数据，自适应学习率。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：参数更新可能过快导致停止。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适合处理稀疏特征的数据。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

<font style="color:rgb(51, 51, 51);">逐步衰减梯度平方的积累。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def AdaGrad(params, learning_rate=0.01, epsilon=1e-10):
    for param in params:
        param.adam += (param.grad.data ** 2)
        param.grad.data /= (epsilon + torch.sqrt(param.adam))
        param.data -= learning_rate * param.grad.data
```

# <font style="color:rgb(51, 51, 51);">Adam（Adaptive Moment Estimation）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Adam结合了动量（SGD的改进）和自适应学习率（AdaGrad），通过计算一阶矩（动量）和二阶矩（自适应学习率）来优化参数更新。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878627560-54ab3792-3bcb-49be-be5b-78fb46fef80d.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：快速收敛，适应性强。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：可能导致参数偏移。。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于大多数问题，尤其是深度神经网络。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

<font style="color:rgb(51, 51, 51);">AdamW（改进了参数更新方式）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class Adam:
    def __init__(self, params, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.params = params
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        for param in params:
            param.m = torch.zeros_like(param.data)
            param.v = torch.zeros_like(param.data)
    
    def step(self):
        for param in self.params:
            m = param.m
            v = param.v
            grad = param.grad.data
            m.mul_(self.beta1).add_(grad * (1 - self.beta1))
            v.mul_(self.beta2).add_(grad**2 * (1 - self.beta2))
            m_bar = m / (1 - self.beta1**param.step_count)
            v_bar = v / (1 - self.beta2**param.step_count)
            param.data -= self.learning_rate * m_bar / (torch.sqrt(v_bar) + self.epsilon)

```





# <font style="color:rgb(51, 51, 51);">AdamW</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">AdamW是Adam的改进版，通过分离权重更新和参数缩放来减少参数偏移。它在更新时先调整学习率，然后进行参数更新。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878687180-a384c29e-0faa-459c-93fb-25e04a945a57.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：减少参数偏移，适合处理权重衰减。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：计算复杂度稍高。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于需要权重衰减的情况。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class AdamW:
    def __init__(self, params, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, weight_decay=0.001):
        self.params = params
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        for param in params:
            param.m = torch.zeros_like(param.data)
            param.v = torch.zeros_like(param.data)
    
    def step(self):
        for param in self.params:
            if param.data.grad is None:
                continue
            m = param.m
            v = param.v
            grad = param.grad.data
            m.mul_(self.beta1).add_(grad * (1 - self.beta1))
            v.mul_(self.beta2).add_(grad**2 * (1 - self.beta2))
            m_bar = m / (1 - self.beta1**param.step_count)
            v_bar = v / (1 - self.beta2**param.step_count)
            denom = torch.sqrt(v_bar) + self.epsilon
            param.data -= self.learning_rate * m_bar / denom
            param.data *= 1 / (1 + self.learning_rate * self.weight_decay * param.step_count / (1 + param.step_count))

```





# <font style="color:rgb(51, 51, 51);">RMSprop</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">RMSprop使用指数加权移动平均来计算梯度的平方，适用于梯度变化剧烈的情况。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878722069-e4082339-050b-4090-b634-fd7ebbe37453.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：梯度变化适应性强。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：需手动选择学习率。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于RNN和神经网络训练。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

<font style="color:rgb(51, 51, 51);">结合自适应学习率策略。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class RMSprop:
    def __init__(self, params, learning_rate=0.001, alpha=0.99, epsilon=1e-8):
        self.params = params
        self.learning_rate = learning_rate
        self.alpha = alpha
        self.epsilon = epsilon
        for param in params:
            param.cache = torch.zeros_like(param.data)
    
    def step(self):
        for param in self.params:
            cache = param.cache
            grad = param.grad.data
            cache.mul_(self.alpha).add_(grad**2 * (1 - self.alpha))
            param.data -= self.learning_rate * grad / (torch.sqrt(cache) + self.epsilon)

```





# <font style="color:rgb(51, 51, 51);">Adamax</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Adamax是Adam的变体，使用L-infinity范数来计算梯度矩，适用于梯度较大的情况。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算梯度。</font>
2. <font style="color:rgb(51, 51, 51);">计算一阶矩和二阶矩。</font>
3. <font style="color:rgb(51, 51, 51);">使用Adamax更新规则： </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878770536-01cfb54c-9bd8-4e8e-9995-bd6e6e7eed61.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：更快的收敛速度。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：不适用于所有情况。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于梯度较大的深度网络。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class Adamax:
    def __init__(self, params, learning_rate=0.002, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.params = params
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        for param in params:
            param.m = torch.zeros_like(param.data)
            param.n = torch.zeros_like(param.data)
    
    def step(self):
        for param in self.params:
            m = param.m
            n = param.n
            grad = param.grad.data
            m.mul_(self.beta1).add_(grad * (1 - self.beta1))
            n.mul_(self.beta2).add_(grad.abs() * (1 - self.beta2))
            m_bar = m / (1 - self.beta1**param.step_count)
            n_bar = n / (1 - self.beta2**param.step_count)
            denom = torch.max(n_bar, torch.tensor(self.epsilon))
            param.data -= self.learning_rate * m_bar / denom

```





# <font style="color:rgb(51, 51, 51);">Adadelta</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Adadelta取消了学习率，使用历史梯度平方的平均值来调整参数更新。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739878821058-05b44aa4-ef49-4d8b-8050-839e88783bdc.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ <font style="color:rgb(51, 51, 51);">优点：无需学习率调整。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：参数更新可能振荡。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);">适用于不需要手动调整学习率的情况。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class Adadelta:
    def __init__(self, params, learning_rate=1.0, rho=0.99, epsilon=1e-8):
        self.params = params
        self.rho = rho
        self.epsilon = epsilon
        for param in params:
            param.cache = torch.zeros_like(param.data)
            param.delta = torch.zeros_like(param.data)
    
    def step(self):
        for param in self.params:
            cache = param.cache
            delta = param.delta
            grad = param.grad.data
            cache.mul_(self.rho).add_(grad**2 * (1 - self.rho))
            grad_scaled = grad / (torch.sqrt(cache) + self.epsilon)
            delta.mul_(self.rho).add_(grad_scaled**2 * (1 - self.rho))
            update = torch.sqrt(delta + self.epsilon) * grad_scaled
            param.data -= update
            param.cache.copy_(cache)
            param.delta.copy_(delta)

```



