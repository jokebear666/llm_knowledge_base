# 激活函数

<!-- source: yuque://zhongxian-iiot9/hlyypb/dvzytvzftes1ly7h -->

# Softmax
:::color3
**简介**：<font style="color:rgb(51, 51, 51);">Softmax是一种</font>**<font style="color:rgb(51, 51, 51);">归一化函数</font>**<font style="color:rgb(51, 51, 51);">，核心作用是将</font>**<font style="color:#ED740C;">任意实数向量转换为概率分布（和为1，值域[0,1]）</font>**<font style="color:rgb(51, 51, 51);">，特点包括：</font>

+ **<font style="color:rgb(51, 51, 51);">指数放大效应</font>**<font style="color:rgb(51, 51, 51);">：较大的输入值会被赋予更高的概率，突出主导类别。</font>
+ **<font style="color:rgb(51, 51, 51);">可导性</font>**<font style="color:rgb(51, 51, 51);">：梯度计算友好，便于反向传播优化模型。</font>
+ **<font style="color:rgb(51, 51, 51);">与交叉熵的关联</font>**<font style="color:rgb(51, 51, 51);">：在多分类任务中，常与交叉熵损失（Cross-Entropy Loss）联合使用，简化梯度计算，提升训练效率。</font>

:::

:::color5
**<font style="color:#601BDE;">1.公式</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741679904394-32830358-59d1-4a3a-9d8c-8bc4aa5d6793.png)

+ **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：实数向量</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">[</font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">…</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">n</font><font style="color:rgb(51, 51, 51);">]</font>**<font style="color:rgb(51, 51, 51);">z</font>**<font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">[</font>_<font style="color:rgb(51, 51, 51);">z</font>_<font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">z</font>_<font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);">…</font><font style="color:rgb(51, 51, 51);">,</font>_<font style="color:rgb(51, 51, 51);">z</font>__<font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);">]</font><font style="color:rgb(51, 51, 51);">，通常为神经网络的原始输出（logits）。</font>
+ **<font style="color:rgb(51, 51, 51);">处理步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对每个元素</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">z</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">计算指数</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">e</font>__<font style="color:rgb(51, 51, 51);">z</font>__<font style="color:rgb(51, 51, 51);">i</font>_<font style="color:rgb(51, 51, 51);">，确保结果为正。</font>
    - <font style="color:rgb(51, 51, 51);">将所有指数结果求和，并对每个指数值归一化，得到概率分布。</font>
+ **<font style="color:rgb(51, 51, 51);">数值稳定性优化</font>**<font style="color:rgb(51, 51, 51);">：实际计算时，为避免指数爆炸（如 zi</font>_<font style="color:rgb(51, 51, 51);">zi</font>_<font style="color:rgb(51, 51, 51);"> 值过大），会减去最大值：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741679946900-69a8497e-2552-46eb-a014-acc8a0521dfc.png)

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

**<font style="color:rgb(51, 51, 51);">① 多分类神经网络</font>**

+ **<font style="color:rgb(51, 51, 51);">输出层</font>**<font style="color:rgb(51, 51, 51);">：在图像分类（如ResNet）、文本分类（如BERT）中，将logits映射为类别概率。  
</font>_<font style="color:rgb(51, 51, 51);">示例</font>_<font style="color:rgb(51, 51, 51);">：MNIST手写数字识别（10个类别），输出层通过Softmax生成每个数字的概率。</font>

**<font style="color:rgb(51, 51, 51);">② 注意力机制</font>**

+ **<font style="color:rgb(51, 51, 51);">权重分配</font>**<font style="color:rgb(51, 51, 51);">：Transformer模型中，Softmax用于计算注意力权重，决定不同位置信息的重要性。  
</font>_<font style="color:rgb(51, 51, 51);">示例</font>_<font style="color:rgb(51, 51, 51);">：在“我 爱 你”的翻译中，模型通过注意力权重聚焦“love”对应“爱”。</font>

**<font style="color:rgb(51, 51, 51);">③ 强化学习</font>**

+ **<font style="color:rgb(51, 51, 51);">策略函数</font>**<font style="color:rgb(51, 51, 51);">：在策略梯度方法中，将动作偏好（如Q值）转化为概率分布，指导智能体决策。  
</font>_<font style="color:rgb(51, 51, 51);">示例</font>_<font style="color:rgb(51, 51, 51);">：AlphaGo选择落子位置时，使用Softmax平衡探索与利用。</font>

**<font style="color:rgb(51, 51, 51);">温度缩放（变体应用）</font>**

+ **<font style="color:rgb(51, 51, 51);">知识蒸馏</font>**<font style="color:rgb(51, 51, 51);">：引入温度参数 T</font>_<font style="color:rgb(51, 51, 51);">T</font>_<font style="color:rgb(51, 51, 51);"> 控制输出平滑度：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741679994050-59470795-2018-4d22-a72d-ad5bdddb7d8f.png)

<font style="color:rgb(51, 51, 51);">高温（</font><font style="color:rgb(51, 51, 51);">T>1</font>_<font style="color:rgb(51, 51, 51);">T</font>_<font style="color:rgb(51, 51, 51);">>1</font><font style="color:rgb(51, 51, 51);">）使分布更均匀，用于教师模型传递“暗知识”给学生模型。</font>  


:::color5
**<font style="color:#601BDE;">3.不适用于隐藏层激活</font>**

:::

<font style="color:rgb(51, 51, 51);">Softmax是</font>**<font style="color:rgb(51, 51, 51);">输出层的专用激活函数</font>**<font style="color:rgb(51, 51, 51);">，适用于多分类和注意力权重归一化，但隐藏层通常选择其他激活函数（如ReLU）。使用时需结合任务需求设计网络结构。</font>

```python
import math

def softmax(z):
    # 数值稳定性处理：减去最大值防止指数爆炸
    max_z = max(z)
    # 计算调整后的指数值
    exp_z = [math.exp(zi - max_z) for zi in z]
    # 计算所有指数值的和
    sum_exp = sum(exp_z)
    # 归一化为概率分布
    return [ez / sum_exp for ez in exp_z]

# 示例输入
z = [1.0, 2.0, 3.0]
probabilities = softmax(z)
print(probabilities)  # 输出近似为 [0.0900, 0.2447, 0.6652]
```



# Sigmoid
:::color3
**简介**：Sigmoid函数是一种常用的激活函数，主要用于二分类问题。Sigmoid函数将输入压缩到(0,1)区间，适用于输出需要概率解释的场景。

:::

公式：![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739850198562-fd8cd5b1-6a40-4500-bdcf-9e68089f29cb.png)

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

+ **优点**：
    - 输出在0到1之间，适合二分类。
    - 输出对称，易于求导。
+ **缺点**：
    - 梯度消失：当输入远离0时，导数趋近于0，影响梯度传播。
    - 计算开销较高。

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ 二分类任务。
+ 输出层需要概率输出的场景。

```python
def sigmoid(x):
    """
    Sigmoid激活函数
    :param x: 输入张量，形状为 (N, *)，N为批量大小，其余为特征维度
    :return: 输出张量，形状与输入相同
    """
    # Sigmoid函数的计算过程
    return 1 / (1 + torch.exp(-x))
```





# ReLU
:::color3
**简介**：ReLU是广泛使用的激活函数，适用于深层网络。ReLU将输入大于0的部分保持为原值，小于等于0的部分设为0。

:::

公式：<font style="color:#000000;">ReLU(</font>_<font style="color:#000000;">x</font>_<font style="color:#000000;">)=max(0,</font>_<font style="color:#000000;">x</font>_<font style="color:#000000;">)</font>

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

+ **优点**：
    - 计算高效，梯度为1时易于传播。
    - 避免梯度消失问题。
+ **缺点**：
    - [**<font style="color:rgb(9, 64, 142);">神经元死亡</font>**](https://zhida.zhihu.com/search?content_id=174191457&content_type=Article&match_order=1&q=%E7%A5%9E%E7%BB%8F%E5%85%83%E6%AD%BB%E4%BA%A1&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">的问题(ReLU Dying)</font>**<font style="color:rgb(25, 27, 31);">： 问题是指当出现异常输入时，在</font>**<font style="color:#117CEE;">反向传播中会产生大的梯度，这种大的梯度会导致神经元死亡和梯度消失</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **改进版**：Leaky ReLU, SiLU。

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ 大多数神经网络的隐藏层。
+ 特征提取和深层网络。

```python
def relu(x):
    """
    ReLU激活函数
    :param x: 输入张量，形状为 (N, *)，N为批量大小，其余为特征维度
    :return: 输出张量，形状与输入相同
    """
    return torch.where(x > 0, x, torch.tensor(0.0, device=x.device))
```



# ReLU6
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ReLU6（Rectified Linear Unit 6）是ReLU激活函数的改进版本，</font>**<font style="color:#ED740C;">在移动端深度学习中广泛使用</font>**<font style="color:rgb(51, 51, 51);">。其核心思想是通过</font>**<font style="color:rgb(51, 51, 51);">上限截断</font>**<font style="color:rgb(51, 51, 51);">控制激活值范围，数学表达式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740541344492-fd91c9ff-9683-4a08-9c1c-a985d8990b78.png)

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">前向传播</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">输入值</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">x</font>_<font style="color:rgb(51, 51, 51);">x</font>_
2. <font style="color:rgb(51, 51, 51);">执行下限截断：max⁡(0,x)</font>
3. <font style="color:rgb(51, 51, 51);">执行上限截断：min⁡(结果,6)</font>

**<font style="color:rgb(51, 51, 51);">反向传播</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740541363245-93dc4fb1-ec23-4b52-bd47-ea72675f6382.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**核心特性**

| **特性** | **描述** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">有界输出</font>** | <font style="color:rgb(51, 51, 51);">输出范围固定为 [0,6]，提升数值稳定性</font> |
| **<font style="color:rgb(51, 51, 51);">稀疏激活</font>** | <font style="color:rgb(51, 51, 51);">保留ReLU的死亡神经元特性</font> |
| **<font style="color:rgb(51, 51, 51);">量化友好</font>** | <font style="color:rgb(51, 51, 51);">固定范围便于低精度计算和模型量化</font> |
| **<font style="color:rgb(51, 51, 51);">计算高效</font>** | <font style="color:rgb(51, 51, 51);">无指数/复杂运算，适合移动端</font> |


**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">在移动端设备（如ARM CPU）上速度比ReLU快约15%</font>
2. <font style="color:rgb(51, 51, 51);">防止激活值过大导致量化时精度损失</font>
3. <font style="color:rgb(51, 51, 51);">缓解梯度爆炸问题</font>

**<font style="color:rgb(51, 51, 51);">劣势</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">丢失极端值信息（如x>6的数据）</font>
2. <font style="color:rgb(51, 51, 51);">非零中心化特性可能影响网络收敛</font>
3. <font style="color:rgb(51, 51, 51);">在深层网络中可能加剧神经元死亡</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">移动端视觉模型</font>**<font style="color:rgb(51, 51, 51);">：MobileNet系列（V1/V2/V3）</font>
2. **<font style="color:rgb(51, 51, 51);">量化模型部署</font>**<font style="color:rgb(51, 51, 51);">：TensorFlow Lite量化方案</font>
3. **<font style="color:rgb(51, 51, 51);">低功耗设备</font>**<font style="color:rgb(51, 51, 51);">：IoT设备、边缘计算节点</font>
4. **<font style="color:rgb(51, 51, 51);">轻量级网络</font>**<font style="color:rgb(51, 51, 51);">：ShuffleNet、EfficientNet-Lite</font>

**<font style="color:rgb(51, 51, 51);">性能对比</font>**

<font style="color:rgb(51, 51, 51);">在MobileNetV2上的实验结果（ImageNet）：</font>

<font style="color:rgb(51, 51, 51);">ReLU6 已成为移动端深度学习模型的标准组件，在保证模型精度的同时显著优化了部署效率。当设计面向</font>**<font style="color:#ED740C;">边缘设备的轻量级网络</font>**<font style="color:rgb(51, 51, 51);">时，建议优先考虑使用 ReLU6 激活函数。</font>

| **激活函数** | **Top-1 Acc** | **推理延迟(ms)** | **量化后精度损失** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">ReLU</font> | <font style="color:rgb(51, 51, 51);">72.0%</font> | <font style="color:rgb(51, 51, 51);">38.2</font> | <font style="color:rgb(51, 51, 51);">3.7%</font> |
| <font style="color:rgb(51, 51, 51);">ReLU6</font> | <font style="color:rgb(51, 51, 51);">72.4%</font> | <font style="color:rgb(51, 51, 51);">32.1</font> | <font style="color:rgb(51, 51, 51);">0.9%</font> |
| <font style="color:rgb(51, 51, 51);">Swish</font> | <font style="color:rgb(51, 51, 51);">73.1%</font> | <font style="color:rgb(51, 51, 51);">45.6</font> | <font style="color:rgb(51, 51, 51);">2.8%</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">动态上界</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
class DynamicReLU6(nn.Module):
    def __init__(self):
        super().__init__()
        self.upper_bound = nn.Parameter(torch.tensor(6.0))
        
    def forward(self, x):
        return torch.clamp(x, 0, self.upper_bound)

```

2. **<font style="color:rgb(51, 51, 51);">混合激活策略</font>**<font style="color:rgb(51, 51, 51);">：</font>

```python
# 在浅层使用ReLU6，深层使用Swish
def hybrid_activation(x, layer_depth):
    if layer_depth < 3:
        return F.relu6(x)
    else:
        return x * torch.sigmoid(x)

```

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
#原生
import torch.nn as nn

relu6 = nn.ReLU6()
output = relu6(x)

#手动实现
class ReLU6(nn.Module):
    def forward(self, x):
        return torch.clamp(x, min=0, max=6)

#量化友好实现
def quant_relu6(x, scale, zero_point):
    x_int = torch.quantize_per_tensor(x, scale, zero_point, torch.qint8)
    x_int = torch.clamp(x_int, 0, 6/scale)
    return x_int.dequantize()
```



# SiLU
[https://blog.csdn.net/mddCSDN/article/details/127010114](https://blog.csdn.net/mddCSDN/article/details/127010114)

:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**[<font style="color:rgb(252, 85, 49);">Sigmoid</font>](https://so.csdn.net/so/search?q=Sigmoid&spm=1001.2101.3001.7020)<font style="color:rgb(77, 77, 77);">和ReLU的改进版，</font>**<font style="color:#ED740C;">其核心思想将Sigmoid的门控机制与线性变换结合</font>**<font style="color:rgb(77, 77, 77);">。SiLU具备无上界有下界、平滑、非单调的特性。SiLU在深层</font><font style="color:rgb(78, 161, 219) !important;">模型</font><font style="color:rgb(77, 77, 77);">上的效果优于 ReLU。可以看做是平滑的ReLU</font>激活函数<font style="color:rgb(77, 77, 77);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740540644268-89e1cc53-072e-4974-a24a-e8b698130c6f.png)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740540548694-d73cf4d5-72d4-4b8d-bced-fa9fbd22da50.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **前向传播**：

```python
def silu(x):
    sigmoid = 1 / (1 + np.exp(-x))  # 计算Sigmoid
    return x * sigmoid              # 元素相乘
```

2. **反向传播**（梯度计算）：

```python
def silu_grad(x):
    sigmoid = 1 / (1 + np.exp(-x))
    return sigmoid * (1 + x * (1 - sigmoid))
```

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">相比ReLU提升模型精度（ImageNet上+0.9%）</font>
2. <font style="color:rgb(51, 51, 51);">梯度更平滑，优化过程更稳定</font>
3. <font style="color:rgb(51, 51, 51);">适合深层网络和注意力机制</font>

**<font style="color:rgb(51, 51, 51);">劣势</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">计算成本较高（需计算Sigmoid）</font>
2. <font style="color:rgb(51, 51, 51);">硬件加速支持不如ReLU成熟</font>
3. <font style="color:rgb(51, 51, 51);">输出范围无界（可能需配合归一化）</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">Transformer架构</font>**<font style="color:rgb(51, 51, 51);">：替代GELU用于注意力层</font>
2. **<font style="color:rgb(51, 51, 51);">图像分类网络</font>**<font style="color:rgb(51, 51, 51);">：如EfficientNet系列</font>
3. **<font style="color:rgb(51, 51, 51);">生成对抗网络</font>**<font style="color:rgb(51, 51, 51);">：稳定GAN训练过程</font>
4. **<font style="color:rgb(51, 51, 51);">小样本学习</font>**<font style="color:rgb(51, 51, 51);">：增强模型表示能力</font>

**<font style="color:rgb(51, 51, 51);">性能对比：</font>**

<font style="color:rgb(51, 51, 51);">在ResNet-50上的实验结果（ImageNet）：</font>

<font style="color:rgb(51, 51, 51);">通过合理应用SiLU，可在多数深度学习任务中获得更优的模型性能，但其计算成本需在实际部署时权衡考量。建议在Transformer、GAN等复杂模型架构中优先尝试。</font>

| **激活函数** | **Top-1 Acc** | **训练速度（iter/s）** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">ReLU</font> | <font style="color:rgb(51, 51, 51);">76.2%</font> | <font style="color:rgb(51, 51, 51);">4.3</font> |
| <font style="color:rgb(51, 51, 51);">SiLU</font> | <font style="color:rgb(51, 51, 51);">77.1%</font> | <font style="color:rgb(51, 51, 51);">3.8</font> |
| <font style="color:rgb(51, 51, 51);">GELU</font> | <font style="color:rgb(51, 51, 51);">76.8%</font> | <font style="color:rgb(51, 51, 51);">3.6</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **参数化SiLU**：  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740540787307-939d7675-3479-4d45-a482-56cb805f3cea.png)  
（β作为可学习参数）
2. **Hard-Swish**：  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740540797946-a2b563fe-5733-47cd-a63c-a64bc8e0783f.png)  
（MobileNetV3采用）
3. **动态调整机制**：

```python
# 自适应β示例
class AdaptiveSwish(nn.Module):
    def __init__(self):
        super().__init__()
        self.beta = nn.Parameter(torch.tensor(1.0))

    def forward(self, x):
        return x * torch.sigmoid(self.beta * x)

```

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
#torch原生
import torch.nn as nn

silu = nn.SiLU()  # PyTorch 1.7+
output = silu(x)

#手动实现
class SiLU(nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(x)

```

# 
# leaky_relu
:::color3
**简介**：Leaky ReLU是对ReLU的改进，解决死神经元问题。Leaky ReLU在输入小于0时，输出一个较小的正斜率，避免梯度消失。

:::

公式：![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739850297880-d76fac81-fccd-4e4e-929b-0fa760c62d6d.png)

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

+ **优点**：
    - 解决ReLU的死神经元问题。
    - 计算高效。
+ **缺点**：
    - 超参数α_α_需要调整。
    - 输出可能存在负值。

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ ReLU的替代品，适用于ReLU出现死神经元的场景。
+ 特征学习和深层网络。

```python
def leaky_relu(x, negative_slope=0.01):
    """
    Leaky ReLU激活函数
    :param x: 输入张量，形状为 (N, *)，N为批量大小，其余为特征维度
    :param negative_slope: 负斜率，常用值为0.01
    :return: 输出张量，形状与输入相同
    """
    return torch.where(x > 0, x, negative_slope * x)  # x > 0 则返回x，否则返回negative_slope * x
```

# ELU
:::color3
**<font style="color:#000000;">简介</font>**<font style="color:#000000;">：</font><font style="color:rgb(25, 27, 31);">ELU (Exponential Linear Units) 指数线性单元：</font>**<font style="color:#ED740C;">具有relu的优势，没有神经元死亡问题</font>**<font style="color:rgb(25, 27, 31);">，输出均值接近0，实际上PReLU和Leaky ReLU都有这一优点。有负数饱和区域，从而对噪声有一些鲁棒性。可以看做是</font>**<font style="color:#ED740C;">介于ReLU和Leaky ReLU之间的一个函数</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::

[**<font style="color:rgb(9, 64, 142);">神经元死亡</font>**](https://zhida.zhihu.com/search?content_id=174191457&content_type=Article&match_order=1&q=%E7%A5%9E%E7%BB%8F%E5%85%83%E6%AD%BB%E4%BA%A1&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">的问题(ReLU Dying)</font>**<font style="color:rgb(25, 27, 31);">： 问题是指当出现异常输入时，在</font>**<font style="color:#117CEE;">反向传播中会产生大的梯度，这种大的梯度会导致神经元死亡和梯度消失</font>**<font style="color:rgb(25, 27, 31);">。</font>

公式：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742527044537-5358fd1c-c683-4a23-9c4c-86f8e5ce22a3.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742527065001-309c523e-fd3a-4eb0-9bf9-2ed18736ebe1.png)

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

**<font style="color:rgb(25, 27, 31);">优点：</font>**

+ <font style="color:rgb(25, 27, 31);">它在所有点上都是连续的和可微的。</font>
+ <font style="color:rgb(25, 27, 31);">与其他线性非饱和激活函数（如 ReLU 及其变体）相比，它有着更快的训练时间。</font>
+ <font style="color:rgb(25, 27, 31);">与 ReLU 不同，</font>**<font style="color:#74B602;">它没有神经元死亡的问题</font>**<font style="color:rgb(25, 27, 31);">。 这是因为 ELU 的梯度对于所有负值都是非零的。</font>
+ <font style="color:rgb(25, 27, 31);">作为非饱和激活函数，它不会遇到梯度爆炸或消失的问题。</font>
+ <font style="color:rgb(25, 27, 31);">与其他激活函数（如 ReLU 和变体、Sigmoid 和双曲正切）相比，它实现了更高的准确性。</font>

**<font style="color:rgb(25, 27, 31);">缺点：</font>**

+ <font style="color:rgb(25, 27, 31);">与 ReLU 及其变体相比，由于负输入涉及非线性，因此计算速度较慢。 然而，在训练期间，ELU 的更快收敛足以弥补这一点。 但是在测试期间，ELU 的性能会比 ReLU 及其变体慢。</font>

:::color5
**<font style="color:#601BDE;">代码实现</font>**

:::

```python

```

# tanh
:::color3
**简介**：Tanh是一种双曲正切函数，输出在-1到1之间，适用于生成中间值。Tanh在输入较大的正负值时，输出趋近于1和-1，在中间区域变化较为平缓。

:::

公式：![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739850246963-197834cb-b38d-4cc1-bc69-c75e3bcb6c53.png)

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

+ **优点**：
    - 输出对称，适合处理负数。
    - 输出范围在-1到1之间，有助于后续层的处理。
+ **缺点**：
    - 存在梯度消失问题，尤其是当输入值接近-1或1时。
    - 计算开销较高。

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ 控制理论和时间序列模型。
+ 输出层需要对称范围的场景。

```python
def tanh(x):
    """
    Tanh激活函数
    :param x: 输入张量，形状为 (N, *)，N为批量大小，其余为特征维度
    :return: 输出张量，形状与输入相同
    """
    # Tanh函数的计算过程
    exp_x = torch.exp(x)      # 计算e^(x)
    exp_neg_x = torch.exp(-x) # 计算e^(-x)
    return (exp_x - exp_neg_x) / (exp_x + exp_neg_x)  # (e^(x) - e^(-x)) / (e^(x) + e^(-x))
```

# GLU
:::color3
**简介**：Glu是一种门控机制，适用于序列模型和图像处理。Glu结合了线性变换和门控机制，动态控制信息流。在GLU中，⼀个线性变换的结果通过Sigmoid函数进⾏⻔控，将其输出的值限制在0到1之间，作为“⻔控因⼦”去控制另⼀个线性变换的输出。这种结构可以动态调整信息流，使得⽹络对不同输⼊进⾏有选择的响应。

:::

公式：![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739850346956-c24d21b5-4945-449e-a9d6-9d51e3d83111.png)

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

+ **优点**：
    - 门控机制适应性强，适合动态特征选择。
    - 适合处理序列数据和图像。
+ **缺点**：
    - 计算复杂度较高。
    - 需要显式学习 gating 参数，可能引入额外的复杂度。

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ 语言模型和时间序列预测。
+ 图像处理和特征提取。

:::color5
**<font style="color:#601BDE;">为什么用门控？</font>**

:::

<font style="color:#1f2329;">⻔控机制通过将</font><font style="color:#2ea121;">输⼊与 sigmoid计算的结果逐元素相乘，可以有选择地抑制或放⼤某些输⼊</font><font style="color:#1f2329;">，这类似于让⽹络能够“决定”哪些信息是重要</font>

:::color5
**<font style="color:#601BDE;">为什么用Hadamard积？</font>**

:::

<font style="color:#1f2329;">Hadamard 积</font><font style="color:#6425d0;">允许对每个元素进⾏独⽴控制</font><font style="color:#1f2329;">。在 GLU 中，⽹络会计算两组输出，</font>

<font style="color:#1f2329;">⼀个是线性变换的输出</font>_<font style="color:#1f2329;">XW</font>_<font style="color:#1f2329;">1 </font><font style="color:#1f2329;">+ </font>_<font style="color:#1f2329;">b</font>_<font style="color:#1f2329;">1 ，另⼀个是通过 sigmoid激活的⻔控输出</font>_<font style="color:#1f2329;">σ</font>_<font style="color:#1f2329;">(</font>_<font style="color:#1f2329;">XW</font>_<font style="color:#1f2329;">2 </font><font style="color:#1f2329;">+ </font>_<font style="color:#1f2329;">b</font>_<font style="color:#1f2329;">2 </font><font style="color:#1f2329;">)</font><font style="color:#1f2329;">。</font>

```python
def glu(x, mask=None):
    channels = x.size(1)
    gate = torch.sigmoid(torch.bmm(x, x.permute(0, 2, 1)) / (channels**0.5))
    return x * gate
```

# GELU
:::color3
**简介**：[_**<font style="color:rgb(9, 64, 142);">高斯误差线性单元激活函数</font>**_](https://zhida.zhihu.com/search?content_id=187782758&content_type=Article&match_order=1&q=%E9%AB%98%E6%96%AF%E8%AF%AF%E5%B7%AE%E7%BA%BF%E6%80%A7%E5%8D%95%E5%85%83%E6%BF%80%E6%B4%BB%E5%87%BD%E6%95%B0&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（</font>[<font style="color:rgb(9, 64, 142);">Gaussian Error Linear Units</font>](https://zhida.zhihu.com/search?content_id=187782758&content_type=Article&match_order=1&q=Gaussian+Error+Linear+Units&zhida_source=entity)<font style="color:rgb(25, 27, 31);">(GELUS)）在最近的 Transformer 模型（谷歌的 </font>[<font style="color:rgb(9, 64, 142);">BERT</font>](https://zhida.zhihu.com/search?content_id=187782758&content_type=Article&match_order=1&q=BERT&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和 OpenAI 的 </font>[<font style="color:rgb(9, 64, 142);">GPT-2</font>](https://zhida.zhihu.com/search?content_id=187782758&content_type=Article&match_order=1&q=GPT-2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）中得到了应用。GELU 的论文来自 2016 年。</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://arxiv.org/pdf/1606.08415](https://arxiv.org/pdf/1606.08415)

:::

<font style="color:rgb(25, 27, 31);">GELUS：</font>_**<font style="color:rgb(25, 27, 31);">双曲正切函数 tanh</font>**_<font style="color:rgb(25, 27, 31);">与</font>_**<font style="color:rgb(25, 27, 31);">近似数值</font>**_<font style="color:rgb(25, 27, 31);">的组合。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742526672690-b1f89521-9c59-457c-9e9d-f33594dcc439.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742526532087-0bb696e9-0b9e-4d00-a29d-abec4ddc74e1.png)

**应用模型**：InternViT

:::color5
**<font style="color:#601BDE;">原理</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">ReLU缺点</font>**<font style="color:rgb(25, 27, 31);">：我们都知道ReLU激活函数，ReLU激活函数在x>0时对输入x执行</font>**<font style="color:rgb(25, 27, 31);">恒等映射</font>**<font style="color:rgb(25, 27, 31);">，在x<=0时对输入x执行</font>**<font style="color:rgb(25, 27, 31);">零映射</font>**<font style="color:rgb(25, 27, 31);">。ReLU虽然提供了非线性，但也有</font>**<font style="color:#117CEE;">缺点：在x=0处不可导，函数曲线不平滑</font>****<font style="color:rgb(25, 27, 31);">。</font>**
+ <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">GELU改进：</font>**<font style="color:rgb(25, 27, 31);">那能不能对ReLU的缺点进行改进呢？这个改进就是GELU！这个改进很好理解！就是理解要 </font><font style="color:rgb(25, 27, 31);">P(X≤x)</font><font style="color:rgb(25, 27, 31);"> ！</font>

<font style="color:rgb(25, 27, 31);">P(X≤x),X∼N(0,1)</font><font style="color:rgb(25, 27, 31);"> 代表一个</font>[<font style="color:rgb(9, 64, 142);">高斯随机变量</font>](https://zhida.zhihu.com/search?content_id=235249220&content_type=Article&match_order=1&q=%E9%AB%98%E6%96%AF%E9%9A%8F%E6%9C%BA%E5%8F%98%E9%87%8F&zhida_source=entity)<font style="color:rgb(25, 27, 31);">小于给定输入x的概率，使得输入x以 </font><font style="color:rgb(25, 27, 31);">P(X≤x)</font><font style="color:rgb(25, 27, 31);"> 的概率被恒等映射， 以</font><font style="color:rgb(25, 27, 31);">1−P(X≤x)</font><font style="color:rgb(25, 27, 31);"> 的概率被零映射。</font>**<font style="color:#74B602;">GELU改进了ReLU在x=0处不可导，函数曲线不平滑的缺点！</font>**

<font style="color:rgb(25, 27, 31);">GELU可以看作 dropout的思想和relu的结合</font>**<font style="color:rgb(25, 27, 31);">，(在keras和torch的</font>**[**<font style="color:rgb(9, 64, 142);">transformer</font>**](https://zhida.zhihu.com/search?content_id=176467635&content_type=Article&match_order=1&q=transformer&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">实现的代码里都是直接用relu+dropout而没有使用gelu)</font>**<font style="color:rgb(25, 27, 31);"> ，主要是为激活函数引入了随机性使得模型训练过程更加鲁棒。近似表达式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742526672690-b1f89521-9c59-457c-9e9d-f33594dcc439.png)

:::color5
**<font style="color:#601BDE;">代码实现</font>**

:::

```python
def gelu(input_tensor):
    cdf = 0.5 * (1.0 + tf.erf(input_tensor / tf.sqrt(2.0)))
    return input_tesnsor*cdf
```

# <font style="color:#1f2329;">Swish</font>
:::color3
**简介**：Swish是一种自门控激活函数，兼具ReLU和Sigmoid的优势。Swish利用输入自适应地调整其输出，计算简单且效果优秀。

:::

<font style="color:#1f2329;">Swish是⼀种近年来提出的、性能优异的激活函数，它的表达式为：</font>

<font style="color:#1f2329;">Swishβ (x)=x ⋅σ(βx)                        </font>

+ <font style="color:#1f2329;">σ(x)是sigmoid函数:</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738910967865-2bd47244-6488-44f5-8b3d-2ce753f1abbd.png)
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">β 是⼀个可学习的参数 ，⽤于控制Swish的形状。</font>

<font style="color:#d83931;">Swish</font><font style="color:#d83931;">相较于传统的</font><font style="color:#d83931;">ReLU</font><font style="color:#d83931;">（</font><font style="color:#d83931;">Rectified</font><font style="color:#d83931;">Linear</font><font style="color:#d83931;">    </font><font style="color:#d83931;">Unit</font><font style="color:#d83931;">，修正线性单元）激活函数</font><font style="color:#d83931;">，具有光滑的⾮</font><font style="color:#d83931;">单调特性。</font>

<font style="color:#1f2329;">具体来说：当β= 0 时，Swish接近于线性函数；当β ⽆穷⼤时，它接近ReLU；</font>

:::color5
**<font style="color:#601BDE;">优缺点</font>**

:::

+ **优点**：
    - 自适应调整输出，效果优于ReLU。
    - 计算高效，适用于大规模训练。
+ **缺点**：
    - β_β_ 需要调整，增加模型复杂度。
    - 输出可能不是非负的。

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ 各类神经网络层。
+ 特征提取和分类任务。

```python
def swish(x, beta=1.0):
    return x * torch.sigmoid(beta * x)
```



# HardSwish
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">HardSwish 是 Google 在 2019 年提出的轻量级激活函数，作为 Swish 激活函数的改进版本。其核心思想是通过分段线性函数逼近原始 Swish 的非线性特性，同时保持计算效率。数学表达式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740540907077-9bd35a1b-edb0-4742-9239-188bb86bf868.png)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740540581406-5f2ee723-c9f1-41bc-b970-6f4e157e489e.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

分三段处理输入值：

1. **线性截断区**：当 x≤−3时，输出恒为 0
2. **线性保持区**：当 x≥3 时，输出等于输入
3. **近似计算区**：中间区间使用线性插值公式 x⋅(x+3)/6

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算效率高：无指数运算，适合移动端设备</font>
+ <font style="color:rgb(51, 51, 51);">数值稳定性好：避免梯度消失/爆炸问题</font>
+ <font style="color:rgb(51, 51, 51);">兼容低精度计算：在 FP16/INT8 量化中表现良好</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">非线性表达能力略弱于 Swish</font>
+ <font style="color:rgb(51, 51, 51);">需要手动设置阈值参数（-3 和 3）</font>
+ <font style="color:rgb(51, 51, 51);">对初始化参数敏感</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">移动端视觉模型（如 MobileNetV3）</font>
+ <font style="color:rgb(51, 51, 51);">边缘计算设备部署</font>
+ <font style="color:rgb(51, 51, 51);">需要量化的神经网络</font>
+ <font style="color:rgb(51, 51, 51);">实时性要求高的场景</font>

**<font style="color:rgb(51, 51, 51);">性能对比</font>**

| **指标** | **HardSwish** | **Swish** | **ReLU** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">计算时间 (ms)</font> | <font style="color:rgb(51, 51, 51);">1.2</font> | <font style="color:rgb(51, 51, 51);">3.8</font> | <font style="color:rgb(51, 51, 51);">0.8</font> |
| <font style="color:rgb(51, 51, 51);">Top-1 准确率</font> | <font style="color:rgb(51, 51, 51);">75.3%</font> | <font style="color:rgb(51, 51, 51);">75.6%</font> | <font style="color:rgb(51, 51, 51);">74.1%</font> |
| <font style="color:rgb(51, 51, 51);">内存占用 (MB)</font> | <font style="color:rgb(51, 51, 51);">12.3</font> | <font style="color:rgb(51, 51, 51);">15.7</font> | <font style="color:rgb(51, 51, 51);">11.8</font> |


**使用建议**

1. <font style="color:rgb(51, 51, 51);">在卷积层后直接使用</font>
2. <font style="color:rgb(51, 51, 51);">与 BatchNorm 层配合时注意初始化</font>
3. <font style="color:rgb(51, 51, 51);">量化训练时保持激活范围在 [-6, 6]</font>
4. <font style="color:rgb(51, 51, 51);">学习率可设置为 ReLU 的 0.8 倍</font>

<font style="color:rgb(51, 51, 51);">该激活函数已广泛应用于</font>**<font style="color:#74B602;">移动端视觉模型设计</font>**<font style="color:rgb(51, 51, 51);">，在 ImageNet 数据集上相比 ReLU 能带来约 0.5-1.2% 的精度提升，同时保持计算效率。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">自适应阈值</font>**<font style="color:rgb(51, 51, 51);">：根据输入分布动态调整阈值</font>

```python
class AdaptiveHardSwish(nn.Module):
    def __init__(self):
        super().__init__()
        self.threshold = nn.Parameter(torch.tensor([-3.0, 3.0]))
```

2. **<font style="color:rgb(51, 51, 51);">混合激活</font>**<font style="color:rgb(51, 51, 51);">：与 ReLU6 结合使用</font>
3. **<font style="color:rgb(51, 51, 51);">平滑过渡</font>**<font style="color:rgb(51, 51, 51);">：添加可学习的过渡区间</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn

class HardSwish(nn.Module):
    def __init__(self, inplace=False):
        super(HardSwish, self).__init__()
        self.inplace = inplace

    def forward(self, x):
        return x * torch.clamp(x + 3, 0, 6) / 6

```





# SwiGLU
:::color3
**简介**：SwiGLU激活函数作为LLaMA模型的改进之⼀，通过将GLU中的Sigmoid替换为Swish，使得模型在复杂任务中的表现得到了显著提升。其平滑的激活特性、灵活的⾮线性响应以及⻔控机制共同作⽤ ，提升了模型的表达能⼒和计算效率。**<font style="color:#ED740C;">SwiGLU结合了Swish的自门控特性和GLU的门控线性机制，增强特征选择能力。</font>**

:::

:::color5
1. **<font style="color:#601BDE;">原理</font>**

:::

<font style="color:#1f2329;">SwiGLU</font><font style="color:#1f2329;">是通过将</font><font style="color:#1f2329;">GLU</font><font style="color:#1f2329;">中的</font><font style="color:#1f2329;">Sigmoid</font><font style="color:#1f2329;">函数替换为</font><font style="color:#1f2329;">Sw</font><font style="color:#1f2329;">ish</font><font style="color:#1f2329;">函数得到的</font><font style="color:#1f2329;">，其表达式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739850603849-084b656f-ef37-48e6-bb26-c9fd2df9271c.png)<font style="color:#1f2329;">     </font>

<font style="color:#1f2329;">在这⾥，</font><font style="color:#2ea121;">Swish取代了原有的Sigmoid作为⻔控激活函数，这样就能在更平滑的激活函数下实现类似的⻔控机制</font><font style="color:#1f2329;">。与GLU相⽐，SwiGLU引⼊了更复杂的⾮线性变化，使得⽹络对不同输⼊的响应更加灵活。通过这种⽅式，SwiGLU能够在保持计算效率的同时提升模型的表现。</font>

:::color5
2. **<font style="color:#601BDE;">优缺点</font>**

:::

**优点**

<font style="color:#1f2329;">SwiGLU结合了Swish和GLU的优点，具有以下主要优势：</font>

+ 平滑激活 ：Swish函数提供了平滑的梯度变化，避免了像ReLU那样的“死区”问题。这有助于提升模型的收敛速度和稳定性。
+ 门控机制：通过引⼊⻔控机制，SwiGLU可以选择性地控制信息流动，允许模型根据输⼊调整输出的强度，从⽽提⾼表达能⼒。
+ 更好的性能：<font style="color:#1f2329;">与传统的ReLU或GLU相⽐，SwiGLU在实践中常常带来更好的性能，尤其是在⼤规模语⾔模型中。</font>

**<font style="color:#000000;">缺点</font>**

+ 梯度消失：当输入远离0时，导数趋近于0，影响梯度传播。
+ 计算开销较高。			

:::color5
**<font style="color:#601BDE;">应用场景</font>**

:::

+ 复杂的特征提取任务。
+ 高维数据处理和图像识别。

```python
def swiglu(x):
    dims = x.dim() - 1
    gate = torch.sigmoid(torch.conv2d(x, torch.ones((x.size(1), 1, 1, 1), device=x.device)))
    return x * gate
```

### 
