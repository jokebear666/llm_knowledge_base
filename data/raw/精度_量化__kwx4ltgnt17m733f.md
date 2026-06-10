# 精度&量化

<!-- source: yuque://zhongxian-iiot9/hlyypb/kwx4ltgnt17m733f -->

# 量化
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">量化（Quantization）是通过降低模型参数和激活值的数值精度（如从32位浮点FP32转为8位整数INT8），以减小模型体积、提升推理速度并降低功耗的技术。核心原理是在精度损失可控的前提下，用低比特表示高精度数据。</font>

:::

<font style="color:rgb(51, 51, 51);">常</font>**<font style="color:rgb(51, 51, 51);">见方法分类：</font>**

1. **线性量化**：
    - **<font style="color:rgb(51, 51, 51);">对称量化</font>**<font style="color:rgb(51, 51, 51);">：量化范围对称（如[-α, α]），适合处理零附近分布的数据（如激活值）。</font>
    - **<font style="color:rgb(51, 51, 51);">非对称量化</font>**<font style="color:rgb(51, 51, 51);">：量化范围可不对称（如[min, max]），更灵活但计算复杂度略高。</font>
2. **对数量化**：将浮点数映射为指数形式（如2^n），适合权重分布跨度大的场景。
3. **混合精度量化**：不同层使用不同比特位宽（如关键层用FP16，其余用INT8）。
4. **训练后量化（PTQ）**：直接对预训练模型量化，无需额外训练。
5. **量化感知训练（QAT）**：在训练中模拟量化误差，提升量化后模型精度。

:::color5
**<font style="color:#601BDE;">1.量化算法对比</font>**

:::

| **算法** | **核心思想** | **适用场景** | **计算开销** | **精度保持** |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">线性量化</font> | <font style="color:rgb(51, 51, 51);">线性映射到整数范围</font> | <font style="color:rgb(51, 51, 51);">通用模型、边缘设备</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">中</font> |
| <font style="color:rgb(51, 51, 51);">对数量化</font> | <font style="color:rgb(51, 51, 51);">对数非线性映射</font> | <font style="color:rgb(51, 51, 51);">高动态范围数据</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">低-中</font> |
| <font style="color:rgb(51, 51, 51);">混合精度量化</font> | <font style="color:rgb(51, 51, 51);">动态分配不同位宽</font> | <font style="color:rgb(51, 51, 51);">资源受限的高精度需求场景</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">高</font> |
| <font style="color:rgb(51, 51, 51);">分组量化</font> | <font style="color:rgb(51, 51, 51);">子组独立量化</font> | <font style="color:rgb(51, 51, 51);">大模型、高动态数据</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">中</font> |
| <font style="color:rgb(51, 51, 51);">GPTQ</font> | <font style="color:rgb(51, 51, 51);">二阶误差补偿</font> | <font style="color:rgb(51, 51, 51);">低比特LLM量化</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">高</font> |
| <font style="color:rgb(51, 51, 51);">AWQ</font> | <font style="color:rgb(51, 51, 51);">激活感知的缩放因子调整</font> | <font style="color:rgb(51, 51, 51);">激活敏感型模型</font> | <font style="color:rgb(51, 51, 51);">中</font> | <font style="color:rgb(51, 51, 51);">高</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">移动端/边缘设备</font>**<font style="color:rgb(51, 51, 51);">：如手机实时翻译、自动驾驶中的低延迟推理。</font>
2. **<font style="color:rgb(51, 51, 51);">云端大模型部署</font>**<font style="color:rgb(51, 51, 51);">：降低服务成本（如LLaMA-7B量化后仅需2GB内存）。</font>
3. **<font style="color:rgb(51, 51, 51);">IoT设备</font>**<font style="color:rgb(51, 51, 51);">：资源受限环境下的语音识别（如智能音箱）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合精度量化</font>**<font style="color:rgb(51, 51, 51);">：关键层保留FP16，其他层用INT8（如Transformer的Attention层）。</font>
2. **<font style="color:rgb(51, 51, 51);">动态量化</font>**<font style="color:rgb(51, 51, 51);">：推理时根据输入动态调整量化参数（PyTorch支持）。</font>
3. **<font style="color:rgb(51, 51, 51);">分组量化</font>**<font style="color:rgb(51, 51, 51);">：将权重分块（如128元素/组），每组独立量化，减小误差。</font>
4. **<font style="color:rgb(51, 51, 51);">GPTQ</font>**<font style="color:rgb(51, 51, 51);">：基于二阶导数信息，逐层优化量化权重，最小化误差（公式：</font><font style="color:rgb(51, 51, 51);">arg</font><font style="color:rgb(51, 51, 51);">⁡</font><font style="color:rgb(51, 51, 51);">min</font><font style="color:rgb(51, 51, 51);">⁡</font><font style="color:rgb(51, 51, 51);">W</font><font style="color:rgb(51, 51, 51);">^</font><font style="color:rgb(51, 51, 51);">∣</font><font style="color:rgb(51, 51, 51);">∣</font><font style="color:rgb(51, 51, 51);">W</font><font style="color:rgb(51, 51, 51);">X</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">W</font><font style="color:rgb(51, 51, 51);">^</font><font style="color:rgb(51, 51, 51);">X</font><font style="color:rgb(51, 51, 51);">∣</font><font style="color:rgb(51, 51, 51);">∣</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">ar</font><font style="color:rgb(51, 51, 51);">g</font><font style="color:rgb(51, 51, 51);">min</font>_<font style="color:rgb(51, 51, 51);">W</font>_<font style="color:rgb(51, 51, 51);">^</font><font style="color:rgb(51, 51, 51);">∣∣</font>_<font style="color:rgb(51, 51, 51);">W</font>__<font style="color:rgb(51, 51, 51);">X</font>_<font style="color:rgb(51, 51, 51);">−</font>_<font style="color:rgb(51, 51, 51);">W</font>_<font style="color:rgb(51, 51, 51);">^</font>_<font style="color:rgb(51, 51, 51);">X</font>_<font style="color:rgb(51, 51, 51);">∣</font><font style="color:rgb(51, 51, 51);">∣</font><font style="color:rgb(51, 51, 51);">2</font><font style="color:rgb(51, 51, 51);">）。</font>
5. **<font style="color:rgb(51, 51, 51);">AWQ（Activation-aware Quantization）</font>**<font style="color:rgb(51, 51, 51);">：保护重要权重通道，根据激活分布调整量化粒度。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
from torch.quantization import quantize_dynamic

# 原始模型
model = torch.nn.Transformer(d_model=512)
model.eval()

# 动态量化（权重INT8，激活值FP32）
quantized_model = quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

```

```python
def quantize_tensor(x, num_bits=8):
    x_min = x.min()
    x_max = x.max()
    scale = (x_max - x_min) / (2**num_bits - 1)
    zero_point = torch.round(-x_min / scale)
    x_quant = torch.clamp(torch.round(x / scale + zero_point), 0, 2**num_bits-1)
    return x_quant, scale, zero_point

def dequantize_tensor(x_quant, scale, zero_point):
    return (x_quant - zero_point) * scale

# 示例：量化全连接层权重
fc = torch.nn.Linear(1024, 512)
weight = fc.weight.data
weight_quant, scale, zp = quantize_tensor(weight)
weight_dequant = dequantize_tensor(weight_quant.float(), scale, zp)

# 计算量化误差
mse_loss = torch.mean((weight - weight_dequant)**2)
print(f"Quantization MSE: {mse_loss:.4f}")

```

## 线性量化：
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">线性量化将浮点数值范围线性映射到整数范围。通过定义</font>**<font style="color:rgb(51, 51, 51);">缩放因子（scale）</font>****<font style="color:rgb(51, 51, 51);">和</font>****<font style="color:rgb(51, 51, 51);">零点（zero-point）</font>**<font style="color:rgb(51, 51, 51);">，将浮点数转换为定点整数，公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467085442-fdfbd675-a1bb-4315-8b38-66b9dee15389.png)

<font style="color:rgb(51, 51, 51);">反量化时，通过逆操作恢复近似原始值：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467093783-e468d763-d727-4806-bb80-31412e5be726.png)

#### <font style="color:rgb(51, 51, 51);">变种</font>
+ **<font style="color:rgb(51, 51, 51);">对称量化</font>**<font style="color:rgb(51, 51, 51);">：数据范围关于0对称（如[-α, α]），零点固定为0。</font>
+ **<font style="color:rgb(51, 51, 51);">非对称量化</font>**<font style="color:rgb(51, 51, 51);">：数据范围不对称（如[min, max]），需计算零点偏移。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">确定量化范围</font>**<font style="color:rgb(51, 51, 51);">：选择最小/最大值（非对称）或最大绝对值（对称）。</font>
2. **<font style="color:rgb(51, 51, 51);">计算量化参数</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467127972-2175e377-3985-4666-9d63-e847e2de6113.png)

<font style="color:rgb(51, 51, 51);">对称量化时：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467138595-45d9802f-90b5-40f3-9d38-b20e57487090.png)

3. **<font style="color:rgb(51, 51, 51);">量化与反量化</font>**<font style="color:rgb(51, 51, 51);">：应用上述公式转换。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算简单，硬件友好。</font>
    - <font style="color:rgb(51, 51, 51);">广泛支持（如TensorRT、TFLite）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对非均匀分布数据敏感（如长尾分布）。</font>
    - <font style="color:rgb(51, 51, 51);">动态范围较大时精度损失明显。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">图像分类模型（如ResNet、MobileNet）的权重量化。</font>
+ <font style="color:rgb(51, 51, 51);">边缘设备推理（低计算资源场景）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态范围调整</font>**<font style="color:rgb(51, 51, 51);">：基于输入数据动态调整量化参数。</font>
+ **<font style="color:rgb(51, 51, 51);">子通道量化</font>**<font style="color:rgb(51, 51, 51);">：将张量划分为子通道，独立量化（类似分组量化）。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def linear_quantize(tensor, bits=8, symmetric=False):
    if symmetric:
        max_val = torch.max(torch.abs(tensor))
        scale = (2 * max_val) / (2**bits - 1)
        zero_point = 0
    else:
        min_val, max_val = tensor.min(), tensor.max()
        scale = (max_val - min_val) / (2**bits - 1)
        zero_point = torch.round(-min_val / scale)
    
    quantized = torch.clamp(torch.round(tensor / scale) + zero_point, 0, 2**bits - 1)
    dequantized = (quantized - zero_point) * scale
    return quantized, dequantized, scale, zero_point

# 示例（非对称量化）
tensor = torch.randn(3, 3) * 10
quantized, dequantized, scale, zp = linear_quantize(tensor, bits=8, symmetric=False)

```



## 对数量化：
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">对数量化将浮点数量化为固定基数的指数形式，利用对数的非线性特性压缩动态范围。其核心公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467561323-88c5c165-b88e-4159-825a-1f962786ee01.png)

<font style="color:rgb(51, 51, 51);">其中，</font>`<font style="color:rgb(51, 51, 51);">base</font>`<font style="color:rgb(51, 51, 51);">是预设的底数（如2），量化后的值为离散的指数值。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">确定基数（base）</font>**<font style="color:rgb(51, 51, 51);">：通常选择2的幂（如2, 4）。</font>
2. **<font style="color:rgb(51, 51, 51);">计算指数值</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467587334-3b107194-bb97-4adf-8ad9-54fcb73deeff.png)
3. **<font style="color:rgb(51, 51, 51);">生成量化值</font>**<font style="color:rgb(51, 51, 51);">：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740467593294-099e808c-6180-4fa5-8c2d-da1afa1a68f8.png)
4. **<font style="color:rgb(51, 51, 51);">处理零值</font>**<font style="color:rgb(51, 51, 51);">：单独保留符号为0的位置。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">高效处理高动态范围数据（如语音信号）。</font>
    - <font style="color:rgb(51, 51, 51);">乘法计算可转换为加法（指数相加）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">低动态范围区域分辨率差。</font>
    - <font style="color:rgb(51, 51, 51);">基数选择敏感，需手动调参。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">语音处理模型（如WaveNet）。</font>
+ <font style="color:rgb(51, 51, 51);">高动态范围传感器数据压缩。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">自适应基数选择</font>**<font style="color:rgb(51, 51, 51);">：根据数据分布动态调整基数。</font>
+ **<font style="color:rgb(51, 51, 51);">混合对数-线性量化</font>**<font style="color:rgb(51, 51, 51);">：对小数值使用线性量化，大数值用对数量化。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def log_quantize(tensor, base=2.0):
    # 避免对0取对数
    eps = 1e-8
    sign = torch.sign(tensor)
    abs_tensor = torch.abs(tensor) + eps
    # 计算指数并四舍五入
    exponent = torch.round(torch.log(abs_tensor) / torch.log(torch.tensor(base)))
    # 生成量化值
    quantized = sign * (base ** exponent)
    quantized[torch.abs(tensor) < eps] = 0.0  # 恢复零值
    return quantized

# 示例
tensor = torch.tensor([0.0, 0.1, 1.0, 5.0, 10.0])
quantized = log_quantize(tensor, base=2.0)
# 输出: tensor([0.0000, 0.125, 1.0, 4.0, 8.0])

```



## 混合精度量化：
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:#1f2329;">混合精度（Mixed Precision）训练是⼀种通过结合不同数值精度（如FP32和FP16）进⾏深度学习模型训练的⽅法，旨在提⾼计算效率并减少内存占⽤ ，同时在保持模型精度的前提下优化训练性能。其核⼼思想是，模型中的某些操作对数值精度要求较⾼，⽽另⼀些操作可以使⽤较低精度完成，从⽽在性能与精度之间找到平衡。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737619735461-27377ba8-8d8f-4b65-a525-e229a3f13f16.png)

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**详细计算步骤**

1. <font style="color:#245bdb;">初始化</font><font style="color:#1f2329;">：模型的神经⽹络权重参数最初以</font><font style="color:#dc9b04;">FP32</font><font style="color:#1f2329;">形式存储。</font>
2. <font style="color:#245bdb;">权重转换</font><font style="color:#1f2329;">：将神经⽹络的权重参数从</font><font style="color:#dc9b04;">FP32转换为FP16</font><font style="color:#1f2329;">，⽤于后续的计算。</font>
3. <font style="color:#1456f0;"> </font><font style="color:#245bdb;">前向传播与反向传播</font><font style="color:#245bdb;">  </font><font style="color:#1f2329;">：在前向和反向传播计算中</font><font style="color:#dc9b04;">使⽤FP16</font><font style="color:#1f2329;">完成主要的矩阵运算和激活函数计算，以减少内存占⽤并加速计算。反向传播过程中，梯度也使⽤FP16进⾏计算。</font>
4. <font style="color:#245bdb;">梯度转换</font><font style="color:#245bdb;">  </font><font style="color:#1f2329;">：将FP16的梯度转换回FP32，确保在梯度更新过程中使⽤更⾼精度的计算，避免精度丢失。</font>
5. <font style="color:#245bdb;">梯度更新</font><font style="color:#245bdb;"> </font><font style="color:#1f2329;">：FP32的梯度与学习率（learning rate）相乘，保证精度较⼩的数值不会因浮点数的限制⽽丢失。</font>
6. <font style="color:#245bdb;">权重更新 </font><font style="color:#1f2329;">：使⽤更新后的FP32梯度更新⽹络的FP32权重。</font>

:::color5
**<font style="color:#601BDE;">2.损失缩放</font>**

:::

<font style="color:#1f2329;">在混合精度训练中，由于FP16的数值表⽰范围较⼩，特别是在反向传播过程中，</font>**<font style="color:#74B602;">较⼩的梯度值可能会因为精度不⾜⽽变为零</font>**<font style="color:#1f2329;">。</font>

<font style="color:#1f2329;">为了解决这个问题，引⼊了损失缩放技术。</font>**<font style="color:#74B602;">在反向传播前，将损失值按某个系数进⾏放⼤，确保反向传播时梯度值⾜够⼤，避免FP16下的数值下溢</font>**<font style="color:#1f2329;">。计算完成后，再将梯度缩⼩相应倍数，以保证数值正确性。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:#000000;">优点</font>**

+ <font style="color:#1456f0;">更快的计算速度</font><font style="color:#1f2329;">：FP16的计算速度通常⽐FP32快⼀倍或更多，尤其在⽀持混合精度计算的硬件上（如NVIDIA的Tensor Cores），这⼀加速效应尤为明显。</font>
+ <font style="color:#1456f0;">更高的内存利用率：</font><font style="color:#1f2329;">FP16使⽤更少的内存，这使得在相同的硬件环境下可以训练更⼤的模型或使⽤更⼤的batch size，从⽽提⾼了训练效率。</font>

**<font style="color:#1f2329;">缺点</font>**

+ <font style="color:#245bdb;">数值不稳定性</font><font style="color:#1f2329;">：FP16的精度较低，容易发⽣数值下溢或上溢问题，尤其是在梯度较⼩时。引⼊损失缩放机制能够有效防⽌这种问题发⽣。</font>
+ <font style="color:#1456f0;">硬件要求</font><font style="color:#1f2329;">：混合精度训练需要特定硬件（如NVIDIA Tensor Cores）和软件（如CUDA和cuDNN） 的⽀持。幸运的是，主流的深度学习框架如PyTorch和TensorFlow已经原⽣⽀持混合精度训练。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:#1f2329;">混合精度训练⼴泛应⽤于⼤规模模型训练任务中，特别是需要⼤批量数据和复杂⽹络的场景，如BERT、GPT系列模型等。在计算密集型硬件上，通过混合精度技术能够显著提⾼模型训练的性能，同时减少内存开销，使得在相同资源下能够训练更⼤的模型或处理更⼤的数据集。</font>

+ <font style="color:rgb(51, 51, 51);">多任务模型（如目标检测+分割）。</font>
+ <font style="color:rgb(51, 51, 51);">资源受限但需高精度的场景（如自动驾驶）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">自动化比特分配</font>**<font style="color:rgb(51, 51, 51);">：基于强化学习或NAS自动搜索最优位宽。</font>
+ **<font style="color:rgb(51, 51, 51);">硬件协同设计</font>**<font style="color:rgb(51, 51, 51);">：与芯片厂商合作优化混合精度计算单元。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def mixed_precision_quantize(tensor, ratio=0.3, high_bits=8, low_bits=4):
    # 计算通道重要性（L2范数）
    channel_norms = torch.norm(tensor, p=2, dim=0)
    sorted_indices = torch.argsort(channel_norms, descending=True)
    
    # 分配高/低比特通道
    num_high = int(tensor.shape[1] * ratio)
    high_bit_channels = sorted_indices[:num_high]
    low_bit_channels = sorted_indices[num_high:]
    
    # 分通道量化
    quantized_tensor = torch.zeros_like(tensor)
    # 高比特部分
    quantized_high, _, _, _ = linear_quantize(tensor[:, high_bit_channels], bits=high_bits)
    quantized_tensor[:, high_bit_channels] = quantized_high
    # 低比特部分
    quantized_low, _, _, _ = linear_quantize(tensor[:, low_bit_channels], bits=low_bits)
    quantized_tensor[:, low_bit_channels] = quantized_low
    
    return quantized_tensor

# 示例
tensor = torch.randn(256, 512)  # [Batch, Channels]
quantized = mixed_precision_quantize(tensor, ratio=0.2, high_bits=8, low_bits=4)

```

## 
## <font style="color:rgb(51, 51, 51);">分组量化</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">分组量化将权重或激活张量划分为多个子组（Group），每个子组独立进行量化。每个组内使用不同的缩放因子（scale）和零点（zero-point），从而减少全局量化误差。通过分组，可以更好地适应不同区域的数据分布差异。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">分组划分</font>**<font style="color:rgb(51, 51, 51);">：将权重或激活张量按通道或空间维度划分为多个子组。</font>
+ **<font style="color:rgb(51, 51, 51);">组内量化</font>**<font style="color:rgb(51, 51, 51);">：对每个子组分别计算量化参数（scale, zero-point）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740455535663-f47da486-aec3-4a57-b03f-e7a52d6a8c5e.png)

+ **<font style="color:rgb(51, 51, 51);">量化与反量化</font>**<font style="color:rgb(51, 51, 51);">：对每组进行量化和反量化：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740455542992-b4c01bc1-5b48-4016-97a2-6387f2e72d7b.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">减少大张量因全局量化导致的误差。</font>
    - <font style="color:rgb(51, 51, 51);">灵活性强，可针对不同子组优化。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">增加存储量化参数（scale/zero-point）的开销。</font>
    - <font style="color:rgb(51, 51, 51);">计算复杂度略高于全局量化。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">大模型（如LLM）的权重量化。</font>
+ <font style="color:rgb(51, 51, 51);">高动态范围的数据分布（如激活值）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态分组策略</font>**<font style="color:rgb(51, 51, 51);">：根据数据分布自动调整组大小。</font>
+ **<font style="color:rgb(51, 51, 51);">混合精度分组</font>**<font style="color:rgb(51, 51, 51);">：敏感组使用更高量化比特数。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch

def group_quantize(tensor, group_size=128, bits=8):
    orig_shape = tensor.shape
    tensor = tensor.view(-1, group_size)  # 分组
    scales = []
    zero_points = []
    quantized = []
    for g in tensor:
        max_val, min_val = g.max(), g.min()
        scale = (max_val - min_val) / (2**bits - 1)
        zero_point = torch.round(-min_val / scale)
        q_g = torch.clamp(torch.round(g / scale) + zero_point, 0, 2**bits-1)
        quantized.append(q_g)
        scales.append(scale)
        zero_points.append(zero_point)
    return {
        "quantized": torch.stack(quantized).view(orig_shape),
        "scales": torch.stack(scales),
        "zero_points": torch.stack(zero_points),
    }

# 示例
tensor = torch.randn(512, 512)
quantized = group_quantize(tensor, group_size=64, bits=8)

```



## <font style="color:rgb(51, 51, 51);">GPTQ（Generative Post-Training Quantization）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">GPTQ（</font><font style="color:rgb(51, 51, 51);">Generative Post-Training Quantization</font><font style="color:rgb(51, 51, 51);">）是一种基于二阶信息的权重量化方法，通过逐层优化最小化均方误差（MSE）。核心思想是利用Hessian矩阵近似损失函数的曲率，调整未量化权重以补偿量化误差。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">分块处理</font>**<font style="color:rgb(51, 51, 51);">：将权重矩阵按列分块。</font>
2. **<font style="color:rgb(51, 51, 51);">Hessian逆计算</font>**<font style="color:rgb(51, 51, 51);">：计算当前块的Hessian逆矩阵</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">H</font><font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">1</font>_<font style="color:rgb(51, 51, 51);">H</font>_<font style="color:rgb(51, 51, 51);">−</font><font style="color:rgb(51, 51, 51);">1</font><font style="color:rgb(51, 51, 51);">。</font>
3. **<font style="color:rgb(51, 51, 51);">量化补偿</font>**<font style="color:rgb(51, 51, 51);">：对每个权重列 w</font>_<font style="color:rgb(51, 51, 51);">w</font>_<font style="color:rgb(51, 51, 51);">，计算量化误差 ΔwΔ</font>_<font style="color:rgb(51, 51, 51);">w</font>_<font style="color:rgb(51, 51, 51);">，并更新后续未量化的权重：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740455652134-9b1a9368-bdcc-4473-8e94-ba658329d153.png)

4. **<font style="color:rgb(51, 51, 51);">迭代量化</font>**<font style="color:rgb(51, 51, 51);">：逐列量化并更新，直到所有块完成。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">高精度，适用于大模型（如LLaMA、GPT）。</font>
    - <font style="color:rgb(51, 51, 51);">支持低至2-4比特的量化。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算Hessian矩阵复杂度高。</font>
    - <font style="color:rgb(51, 51, 51);">逐列处理速度较慢。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">大规模生成模型（如GPT-3）的权重量化。</font>
+ <font style="color:rgb(51, 51, 51);">低比特量化需求场景。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">分块优化</font>**<font style="color:rgb(51, 51, 51);">：并行化处理多个块。</font>
+ **<font style="color:rgb(51, 51, 51);">Hessian近似</font>**<font style="color:rgb(51, 51, 51);">：使用对角矩阵或低秩近似加速计算。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def gptq_quantize_layer(weight, blocksize=128, bits=4):
    H = torch.inverse(compute_hessian(weight))  # 伪代码，Hessian计算需具体实现
    quant_weight = torch.zeros_like(weight)
    for i in range(0, weight.shape[1], blocksize):
        block = weight[:, i:i+blocksize]
        # 量化块并计算误差
        q_block, delta = quantize(block, bits)
        quant_weight[:, i:i+blocksize] = q_block
        # 更新后续未量化权重
        weight[:, i+blocksize:] -= H @ delta.T
    return quant_weight

```



## <font style="color:rgb(51, 51, 51);">AWQ（Activation-aware Quantization）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">AWQ通过分析激活值的分布，对权重的重要通道（Channel）分配更高的量化精度，保护对模型输出影响大的通道。核心思想是权重量化的缩放因子应与其对应激活的重要性相关。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">激活分析</font>**<font style="color:rgb(51, 51, 51);">：在少量校准数据上运行模型，收集激活的显著性（如通道的L2范数）。</font>
2. **<font style="color:rgb(51, 51, 51);">缩放因子调整</font>**<font style="color:rgb(51, 51, 51);">：根据激活显著性调整权重量化的缩放因子：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740455694536-ca1ceda5-c94f-4f22-986d-85d93e1dd275.png)

<font style="color:rgb(51, 51, 51);">其中 s</font>_<font style="color:rgb(51, 51, 51);">s</font>_<font style="color:rgb(51, 51, 51);"> 是基础缩放因子，α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);"> 是超参数。</font>

3. **<font style="color:rgb(51, 51, 51);">量化执行</font>**<font style="color:rgb(51, 51, 51);">：使用调整后的缩放因子对权重进行量化。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">保留关键特征通道，精度损失小。</font>
    - <font style="color:rgb(51, 51, 51);">与激活分布解耦，适配不同输入。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">需要校准数据。</font>
    - <font style="color:rgb(51, 51, 51);">超参数调整敏感。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">对激活分布敏感的模型（如ViT、ResNet）。</font>
+ <font style="color:rgb(51, 51, 51);">低比特量化下的精度恢复。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">自动显著性评估</font>**<font style="color:rgb(51, 51, 51);">：通过梯度信息自动计算通道重要性。</font>
+ **<font style="color:rgb(51, 51, 51);">动态调整</font>**<font style="color:rgb(51, 51, 51);">：根据输入动态调整缩放因子。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def awq_quantize(weight, activation, bits=4, alpha=0.1):
    # 计算激活显著性（按通道L2范数）
    significance = torch.norm(activation, p=2, dim=0)
    significance /= significance.max()
    
    # 调整缩放因子
    base_scale = (weight.max() - weight.min()) / (2**bits - 1)
    scales = base_scale * (1 + alpha * significance)
    
    # 量化权重
    zero_point = torch.round(-weight.min() / scales)
    quantized = torch.clamp(torch.round(weight / scales) + zero_point, 0, 2**bits-1)
    return quantized, scales, zero_point

# 示例
weight = torch.randn(256, 256)
activation = torch.randn(1000, 256)  # 校准数据
quantized, scales, zp = awq_quantize(weight, activation, bits=4)

```



## Int4 & Int8量化
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">量化通过降低数值精度（FP32→INT8/INT4）压缩模型，提升推理速度。关键技术点：</font>

+ **<font style="color:rgb(51, 51, 51);">Scale/Zeropoint</font>**<font style="color:rgb(51, 51, 51);">：浮点数映射到整数的线性变换参数</font>
+ **<font style="color:rgb(51, 51, 51);">对称量化</font>**<font style="color:rgb(51, 51, 51);">（权重常用）：范围[-max, max]</font>
+ **<font style="color:rgb(51, 51, 51);">非对称量化</font>**<font style="color:rgb(51, 51, 51);">（激活常用）：范围[min, max]</font>

:::

| **指标** | **Int8量化** | **Int4量化** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">模型大小</font> | <font style="color:rgb(51, 51, 51);">减少75%</font> | <font style="color:rgb(51, 51, 51);">减少87.5%</font> |
| <font style="color:rgb(51, 51, 51);">计算延迟</font> | <font style="color:rgb(51, 51, 51);">2-3倍加速</font> | <font style="color:rgb(51, 51, 51);">理论4倍加速（需硬件支持）</font> |
| <font style="color:rgb(51, 51, 51);">精度损失</font> | <font style="color:rgb(51, 51, 51);">通常<1% (MNIST)</font> | <font style="color:rgb(51, 51, 51);">可能达3-5%</font> |
| <font style="color:rgb(51, 51, 51);">硬件支持</font> | <font style="color:rgb(51, 51, 51);">主流NPU/GPU支持</font> | <font style="color:rgb(51, 51, 51);">需要定制实现</font> |


:::color5
**<font style="color:#601BDE;">1.Int8量化实现</font>**

:::

1. **计算量化参数**：

```python
def quantize_tensor(x, num_bits=8):
    q_min = -2**(num_bits-1)
    q_max = 2**(num_bits-1)-1
    scale = torch.max(x.abs()) / q_max
    return scale, torch.quantize_per_tensor(x, scale, 0, torch.qint8)
```

2. **PyTorch原生支持**：

```python
# 原始浮点模型
model_fp32 = torch.nn.Linear(256, 128)

# 量化配置
model_fp32.qconfig = torch.quantization.default_qconfig

# 转换为量化模型
model_int8 = torch.quantization.convert(model_fp32)
```

:::color5
**<font style="color:#601BDE;">2.Int4量化实现</font>**

:::

**<font style="color:rgb(51, 51, 51);">实现难点：</font>**

+ <font style="color:rgb(51, 51, 51);">缺少硬件原生支持</font>
+ <font style="color:rgb(51, 51, 51);">需要手动处理4bit打包</font>

**<font style="color:rgb(51, 51, 51);">代码实现：</font>**

```python
def int4_quantize(tensor):
    max_val = torch.max(torch.abs(tensor))
    scale = max_val / 7  # 4bit有符号范围[-8,7]

    # 量化
    quantized = torch.clamp(torch.round(tensor / scale), -8, 7)

    # 打包4bit到8bit存储
    packed = torch.zeros((tensor.numel() + 1) // 2, dtype=torch.uint8)
    for i in range(0, tensor.numel(), 2):
        val1 = (quantized.view(-1)[i].int() & 0x0F)
        val2 = (quantized.view(-1)[i+1].int() & 0x0F) << 4 if i+1 < tensor.numel() else 0
        packed[i//2] = val1 | val2

    return scale, packed

def int4_dequantize(scale, packed):
    unpacked = torch.zeros(packed.numel() * 2, dtype=torch.int8)
    for i in range(packed.numel()):
        unpacked[2*i] = (packed[i] & 0x0F).type(torch.int8)
        unpacked[2*i+1] = ((packed[i] >> 4) & 0x0F).type(torch.int8)
    return unpacked[:unpacked.numel()].float() * scale
```

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(53, 53, 53);">精度</font>
## <font style="color:rgb(53, 53, 53);">溢出问题（上溢/下溢）？</font>
:::color3
**<font style="color:#1f2329;">问题：</font>**<font style="color:#1f2329;">在深度学习模型的训练过程中，计算资源和训练速度是两个重要的考量因素。</font>使⽤较低精度  的浮点数（如 float16）可以减少内存占⽤和提⾼计算速度。然⽽，**<font style="color:#ED740C;">float16 的数值范围和精度较⼩，可能导致数值溢出（overflow）或下溢（underflow）</font>**，从⽽影响模型的训练效果。

:::

:::color5
**<font style="color:#601BDE;">1.浮点数的表示范围</font>**

:::

<font style="color:#1456f0;">1.  </font><font style="color:#1f2329;">float32（单精度浮点数）：其范围是约</font><font style="color:#1f2329;">−3.4×10</font><sup><font style="color:#1f2329;">38 </font></sup><font style="color:#1f2329;">到</font><font style="color:#1f2329;">3.4×10</font><sup><font style="color:#1f2329;">38 </font></sup><font style="color:#1f2329;">。</font>

<font style="color:#1456f0;">2.  </font><font style="color:#1f2329;">float16（半精度浮点数）：其范围是约  </font><font style="color:#1f2329;">−6.55×10</font><sup><font style="color:#1f2329;">4</font></sup><font style="color:#1f2329;"> 到</font><font style="color:#1f2329;">6.55×10</font><sup><font style="color:#1f2329;">4</font></sup><font style="color:#1f2329;"> 。</font>

<font style="color:#1f2329;">由于 </font>**<font style="color:#74B602;">float16 的指数位和尾数位较少，其能表⽰的数值范围⼤⼤缩⼩</font>**<font style="color:#1f2329;">。这在训练深度学习模型时，尤其是在反向传播过程中，可能会导致梯度的溢出或下溢。</font>

:::color5
**<font style="color:#601BDE;">1.如何解决溢出问题</font>**

:::

1. **使用混合精度**：
    - <font style="color:rgb(51, 51, 51);">使用 </font>`<font style="color:rgb(51, 51, 51);">mixed precision training</font>`<font style="color:rgb(51, 51, 51);">（混合精度训练），即在计算中结合了 </font>`<font style="color:rgb(51, 51, 51);">float16</font>`<font style="color:rgb(51, 51, 51);"> 和 </font>`<font style="color:rgb(51, 51, 51);">float32</font>`<font style="color:rgb(51, 51, 51);">。可以将模型的某些部分（如梯度计算）保留为 </font>`<font style="color:rgb(51, 51, 51);">float32</font>`<font style="color:rgb(51, 51, 51);">，而其他部分使用 </font>`<font style="color:rgb(51, 51, 51);">float16</font>`<font style="color:rgb(51, 51, 51);">。</font>
1. **<font style="color:rgb(51, 51, 51);">使用bfloat16替代float16</font>**<font style="color:#1456f0;"> :</font>
    1. <font style="color:#6425d0;">更⼤的数值范围：</font><font style="color:#1f2329;">减少溢出和下溢的可能性。</font>
    2. <font style="color:#6425d0;">计算效率：</font><font style="color:#1f2329;">接近 float16 的计算性能。</font>
2. **损失缩放（Loss Scaling）**：
    - <font style="color:rgb(51, 51, 51);">在使用</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">float16</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">时，可以通过损失缩放来减少溢出的可能性。具体方法是在计算损失时先将损失乘以一个系数（如 1024），然后在计算梯度时再将梯度缩回（除以同样的系数）。</font>
3. **使用合适的优化器**：
    - <font style="color:rgb(51, 51, 51);">某些优化器针对 </font>`<font style="color:rgb(51, 51, 51);">float16</font>`<font style="color:rgb(51, 51, 51);"> 更加友好，例如 </font>`<font style="color:rgb(51, 51, 51);">Adam</font>`<font style="color:rgb(51, 51, 51);"> 或 </font>`<font style="color:rgb(51, 51, 51);">LAMB</font>`<font style="color:rgb(51, 51, 51);">，可以试着使用这些优化器。</font>
4. **正则化**：
    - <font style="color:rgb(51, 51, 51);">适当的正则化（如 </font>`<font style="color:rgb(51, 51, 51);">dropout</font>`<font style="color:rgb(51, 51, 51);"> 或 </font>`<font style="color:rgb(51, 51, 51);">weight decay</font>`<font style="color:rgb(51, 51, 51);">）可以帮助控制模型的复杂性，从而减少数值不稳定性。</font>
5. **使用更高的精度**：
    - <font style="color:rgb(51, 51, 51);">如果以上方法都无法解决问题，可以考虑使用</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">float32</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">而不是</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">float16</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">进行训练，以确保数值稳定性。</font>
6. **优化数据预处理**：
    - <font style="color:rgb(51, 51, 51);">确保数据标准化（如归一化）在合适的范围内，避免因为输入数据问题引起的数值溢出。</font>



## Lora训练如何选择精度<font style="color:#D22D8D;"></font>
:::color3
+ **<font style="color:rgb(51, 51, 51);">bfloat16</font>**<font style="color:rgb(51, 51, 51);">：大模型LoRA训练的默认选择，平衡动态范围和效率。</font>
+ **<font style="color:rgb(51, 51, 51);">float16</font>**<font style="color:rgb(51, 51, 51);">：旧硬件或显存受限时的替代方案，需配合混合精度。</font>
+ **<font style="color:rgb(51, 51, 51);">float32</font>**<font style="color:rgb(51, 51, 51);">：仅用于敏感任务或极小模型。</font>

:::

<font style="color:rgb(51, 51, 51);">LoRA（Low-Rank Adaptation）通过冻结原模型参数并训练低秩矩阵实现高效微调。精度选择需权衡以下因素：</font>

1. **<font style="color:rgb(51, 51, 51);">优先选择bfloat16的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">大模型场景</font>**<font style="color:rgb(51, 51, 51);">（如百亿参数以上）：bfloat16的动态范围与float32一致，避免梯度溢出问题。</font>
    - **<font style="color:rgb(51, 51, 51);">新一代硬件支持</font>**<font style="color:rgb(51, 51, 51);">（如NVIDIA A100/H100）：原生支持bfloat16加速，计算效率高。</font>
    - **<font style="color:rgb(51, 51, 51);">注重稳定性与速度平衡</font>**<font style="color:rgb(51, 51, 51);">：无需频繁调整损失缩放，适合大规模分布式训练。</font>
2. **<font style="color:rgb(51, 51, 51);">选择float16的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">硬件不支持bfloat16</font>**<font style="color:rgb(51, 51, 51);">（如V100或更早GPU）：需启用混合精度训练（AMP），结合float32主权重和损失缩放。</font>
    - **<font style="color:rgb(51, 51, 51);">显存受限</font>**<font style="color:rgb(51, 51, 51);">：float16比bfloat16在部分框架中优化更成熟，显存占用略低。</font>
    - **<font style="color:rgb(51, 51, 51);">小规模微调任务</font>**<font style="color:rgb(51, 51, 51);">：数据量小、任务简单时，数值不稳定风险较低。</font>
3. **<font style="color:rgb(51, 51, 51);">选择float32的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">极度敏感的微调任务</font>**<font style="color:rgb(51, 51, 51);">：如医学图像、科学计算等需要高精度梯度的场景。</font>
    - **<font style="color:rgb(51, 51, 51);">模型规模极小</font>**<font style="color:rgb(51, 51, 51);">：显存和计算开销可接受时，直接使用float32简化流程。</font>



## LLM部署如何选择精度
```python
硬件检测
├── 支持fp8（H100） → 量化到fp8
├── 支持bf16（A100/H100） → 首选bf16
└── 仅支持fp16（A10/L40/L20） → 选择fp16
      ├── 显存不足 → 添加量化（AWQ/GPTQ）
      └── 存在溢出 → 混合精度+损失缩放
```

**部署建议：**

1. **H100集群**：
    - <font style="color:rgb(51, 51, 51);">使用fp8量化+张量并行，部署千亿参数模型</font>
    - <font style="color:rgb(51, 51, 51);">启用CUDA Graph优化端到端延迟</font>
2. **A100-80GB**：
    - <font style="color:rgb(51, 51, 51);">bf16精度部署70B模型</font>
    - <font style="color:rgb(51, 51, 51);">结合vLLM实现高吞吐服务（吞吐量>1000 token/s）</font>
3. **A10/L40**：
    - <font style="color:rgb(51, 51, 51);">fp16部署13B-34B模型</font>
    - <font style="color:rgb(51, 51, 51);">使用FlashAttention-2优化KV缓存</font>
4. **L20**：
    - <font style="color:rgb(51, 51, 51);">fp16部署7B以下模型</font>
    - <font style="color:rgb(51, 51, 51);">使用量化和模型切片（如llama.cpp GGML）</font>

:::color5
**<font style="color:#601BDE;">1.H100显卡：优先使用fp8/bf16</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">fp8（首选）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">显存占用比fp16再减半，吞吐量提升2-3倍</font>
    - <font style="color:rgb(51, 51, 51);">需要模型支持量化（如LLM.int8()）</font>
    - <font style="color:rgb(51, 51, 51);">示例代码（NVIDIA Transformer Engine）：</font>

```python
from transformer_engine import fp8_autocast
with fp8_autocast(enabled=True):
    outputs = model(inputs)
```

+ **<font style="color:rgb(51, 51, 51);">bf16</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">保留float32的动态范围，避免溢出</font>
    - <font style="color:rgb(51, 51, 51);">适合未量化的大模型（如70B+参数）</font>

:::color5
**<font style="color:#601BDE;">2.A100显卡：bf16 > fp16</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">bf16优先</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">利用Tensor Core加速，吞吐量比fp32高3倍</font>
    - <font style="color:rgb(51, 51, 51);">显存占用与fp16相同（2字节/参数）</font>
    - <font style="color:rgb(51, 51, 51);">PyTorch启用方式：</font>

```python
torch.set_float32_matmul_precision('high')  # 自动选择bf16
```

+ **<font style="color:rgb(51, 51, 51);">fp16备用</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">旧版框架兼容方案</font>
    - <font style="color:rgb(51, 51, 51);">需监控梯度溢出（添加损失缩放）</font>

:::color5
**<font style="color:#601BDE;">3.A10/L40/L20显卡：fp16为主</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">fp16量化部署</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">显存节省50%（相比fp32），适合24GB以下显存</font>
    - <font style="color:rgb(51, 51, 51);">使用NVIDIA Triton推理服务器：</font>

```bash
tritonserver --model-repository=/models --strict-model-config=false
```

+ **<font style="color:rgb(51, 51, 51);">动态混合精度</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对敏感层（如注意力输出）保留fp32</font>
    - <font style="color:rgb(51, 51, 51);">HuggingFace实现示例：</font>

```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b", 
    torch_dtype=torch.float16,
    device_map="auto"
)
```

## <font style="color:rgb(53, 53, 53);">float16、bfloat16、float32。</font>
:::color1
+ **<font style="color:rgb(51, 51, 51);">bfloat16</font>**<font style="color:rgb(51, 51, 51);">：大模型LoRA训练的默认选择，平衡动态范围和效率。</font>
+ **<font style="color:rgb(51, 51, 51);">float16</font>**<font style="color:rgb(51, 51, 51);">：旧硬件或显存受限时的替代方案，需配合混合精度。</font>
+ **<font style="color:rgb(51, 51, 51);">float32</font>**<font style="color:rgb(51, 51, 51);">：仅用于敏感任务或极小模型。</font>

:::

### 三种精度对比
:::color5
**<font style="color:#601BDE;">1.特性对比</font>**

:::

| **特性** | **float32** | **float16** | **bfloat16** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">字节数</font>** | <font style="color:rgb(51, 51, 51);">4字节</font> | <font style="color:rgb(51, 51, 51);">2字节</font> | <font style="color:rgb(51, 51, 51);">2字节</font> |
| **<font style="color:rgb(51, 51, 51);">符号位</font>** | <font style="color:rgb(51, 51, 51);">1位</font> | <font style="color:rgb(51, 51, 51);">1位</font> | <font style="color:rgb(51, 51, 51);">1位</font> |
| **<font style="color:rgb(51, 51, 51);">指数位</font>** | <font style="color:rgb(51, 51, 51);">8位（范围≈±1e38）</font> | <font style="color:rgb(51, 51, 51);">5位（范围≈±6e4）</font> | **<font style="color:rgb(51, 51, 51);">8位</font>**<font style="color:rgb(51, 51, 51);">（同float32）</font> |
| **<font style="color:rgb(51, 51, 51);">尾数位</font>** | <font style="color:rgb(51, 51, 51);">23位（高精度）</font> | <font style="color:rgb(51, 51, 51);">10位（中等精度）</font> | **<font style="color:rgb(51, 51, 51);">7位</font>**<font style="color:rgb(51, 51, 51);">（低精度）</font> |
| **<font style="color:rgb(51, 51, 51);">动态范围</font>** | <font style="color:rgb(51, 51, 51);">最广</font> | <font style="color:rgb(51, 51, 51);">较窄（易</font>**<font style="color:#ED740C;">溢出/下溢</font>**<font style="color:rgb(51, 51, 51);">）</font> | **<font style="color:rgb(51, 51, 51);">接近float32</font>** |
| **<font style="color:rgb(51, 51, 51);">硬件支持</font>** | <font style="color:rgb(51, 51, 51);">通用支持</font> | <font style="color:rgb(51, 51, 51);">主流GPU支持</font> | <font style="color:rgb(51, 51, 51);">新一代GPU（A100+）</font> |
| **<font style="color:rgb(51, 51, 51);">内存占用</font>** | <font style="color:rgb(51, 51, 51);">高（×2）</font> | <font style="color:rgb(51, 51, 51);">低</font> | <font style="color:rgb(51, 51, 51);">低</font> |
| **<font style="color:rgb(51, 51, 51);">适用场景</font>** | <font style="color:rgb(51, 51, 51);">高精度计算、小模型</font> | <font style="color:rgb(51, 51, 51);">混合精度训练</font> | <font style="color:rgb(51, 51, 51);">大模型训练</font> |


:::color5
**<font style="color:#601BDE;">2.优缺点对比</font>**

:::

| **** | **float32** | **float16** | **bfloat16** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">优点</font>** | <font style="color:rgb(51, 51, 51);">数值稳定，精度高，适合需要精确梯度更新的场景。</font> | <font style="color:rgb(51, 51, 51);">内存占用减半，计算速度快，支持混合精度训练。</font> | <font style="color:rgb(51, 51, 51);">动态范围与float32一致，内存占用低，适合大模型训练。</font> |
| **<font style="color:rgb(51, 51, 51);">缺点</font>** | <font style="color:rgb(51, 51, 51);">内存占用高，训练速度慢，不适合大模型。</font> | <font style="color:rgb(51, 51, 51);">动态范围窄，易导致梯度下溢/溢出（需配合损失缩放）。</font> | <font style="color:rgb(51, 51, 51);">尾数精度低，可能影响小数值的表示（但对大模型影响有限）。</font> |


:::color5
**<font style="color:#601BDE;">3.Lora训练如何选择精度</font>**

:::

<font style="color:rgb(51, 51, 51);">LoRA（Low-Rank Adaptation）通过冻结原模型参数并训练低秩矩阵实现高效微调。精度选择需权衡以下因素：</font>

1. **<font style="color:rgb(51, 51, 51);">优先选择bfloat16的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">大模型场景</font>**<font style="color:rgb(51, 51, 51);">（如百亿参数以上）：bfloat16的动态范围与float32一致，避免梯度溢出问题。</font>
    - **<font style="color:rgb(51, 51, 51);">新一代硬件支持</font>**<font style="color:rgb(51, 51, 51);">（如NVIDIA A100/H100）：原生支持bfloat16加速，计算效率高。</font>
    - **<font style="color:rgb(51, 51, 51);">注重稳定性与速度平衡</font>**<font style="color:rgb(51, 51, 51);">：无需频繁调整损失缩放，适合大规模分布式训练。</font>
2. **<font style="color:rgb(51, 51, 51);">选择float16的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">硬件不支持bfloat16</font>**<font style="color:rgb(51, 51, 51);">（如V100或更早GPU）：需启用混合精度训练（AMP），结合float32主权重和损失缩放。</font>
    - **<font style="color:rgb(51, 51, 51);">显存受限</font>**<font style="color:rgb(51, 51, 51);">：float16比bfloat16在部分框架中优化更成熟，显存占用略低。</font>
    - **<font style="color:rgb(51, 51, 51);">小规模微调任务</font>**<font style="color:rgb(51, 51, 51);">：数据量小、任务简单时，数值不稳定风险较低。</font>
3. **<font style="color:rgb(51, 51, 51);">选择float32的条件</font>**
    - **<font style="color:rgb(51, 51, 51);">极度敏感的微调任务</font>**<font style="color:rgb(51, 51, 51);">：如医学图像、科学计算等需要高精度梯度的场景。</font>
    - **<font style="color:rgb(51, 51, 51);">模型规模极小</font>**<font style="color:rgb(51, 51, 51);">：显存和计算开销可接受时，直接使用float32简化流程。</font>

### <font style="color:rgb(53, 53, 53);">float32</font><font style="color:#1f2329;">（FP32， </font><font style="color:rgb(51, 51, 51);">Floating-Point 32</font><font style="color:#1f2329;">）</font>
:::color3
**简介：**<font style="color:#1f2329;">float32（32位浮点数）具有较⾼的精度，包含</font><font style="color:#de7802;">8位指数和23位尾数</font><font style="color:#1f2329;">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:#1456f0;">优点</font>**

+ <font style="color:#d83931;">适⽤于需要极⾼精度的计算</font><font style="color:#1f2329;">，例如模型参数更新等。</font>
+ <font style="color:#1456f0;"></font><font style="color:#d83931;">能有效避免数值下溢和上溢</font><font style="color:#1f2329;">，因此稳定性较⾼。</font>

**<font style="color:#1456f0;">缺点</font>**

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">内存占⽤较⼤，特别是在训练⼤模型时，</font><font style="color:#dc9b04;">可能导致显存不⾜</font><font style="color:#1f2329;">。</font>
+ <font style="color:#1f2329;">计算速度较慢，因为它</font><font style="color:#dc9b04;">需要更多的存储空间和带宽</font><font style="color:#1f2329;">。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:#1f2329;">通常⽤于</font><font style="color:#2ea121;">模型训练的初始阶段或者极度敏感的参数（如某些权重矩阵的更新）</font><font style="color:#1f2329;">，尤其适合在⼩模型或⾼精度模型调优阶段。</font>

### <font style="color:#1f2329;">float 16 （FP16， </font><font style="color:rgb(51, 51, 51);">Floating-Point 32</font><font style="color:#1f2329;">）</font>
:::color3
**简介：**<font style="color:#1f2329;">float16（16位浮点数）仅有</font><font style="color:#de7802;">5位指数和10位尾数</font><font style="color:#1f2329;">，因此它的数值范围和精度都较低。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:#1456f0;">优点</font>**

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">占⽤的内存和带宽仅为float32的⼀半，</font><font style="color:#d83931;">⼤幅减少了显存需求</font><font style="color:#1f2329;">。</font>
+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">计算速度更快，特别是在⽀持半精度浮点运算的硬件（如NVIDIA的Tensor Cores）上，float16能</font><font style="color:#d83931;">显著提⾼计算效率</font><font style="color:#1f2329;">。</font>

**<font style="color:#1456f0;">缺点</font>**

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">数值范围较⼩，</font><font style="color:#dc9b04;">容易出现下溢和上溢问题</font><font style="color:#1f2329;">。</font>
+ <font style="color:#1f2329;">由于精度较低，在某些深度模型（如多层⽹络或需精确计算的任务）中可能不适⽤ ，</font><font style="color:#dc9b04;">容易影响训练稳定性</font><font style="color:#1f2329;">。</font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

<font style="color:#1f2329;">常⽤于需要</font><font style="color:#2ea121;">降低显存使⽤和提⾼计算速度的场景</font><font style="color:#1f2329;">，尤其是⼤型模型的中间层或加速训练阶段。</font>

### <font style="color:#1f2329;">bfloat16 （BF16）</font>
:::color3
**简介：**<font style="color:#1f2329;">bfloat16（16位浮点数）与float16类似，但其</font><font style="color:#de7802;">8位指数和7位尾数使得它具有float32的数值范围</font><font style="color:#1f2329;">，但精度⽐float32低。</font>

:::

:::color5
**<font style="color:#601BDE;">1.优缺点</font>**

:::

**<font style="color:#1456f0;">优点</font>**<font style="color:#1456f0;">   </font>

+ <font style="color:#1f2329;">兼具float32的数值范围和float16的存储优势，能够</font><font style="color:#d83931;">在低精度存储的情况下提供更好的数值稳定性</font><font style="color:#1f2329;">。</font>
+ <font style="color:#1456f0;"></font><font style="color:#d83931;">计算速度和内存占⽤都⽐float32⼩</font><font style="color:#1f2329;">，在某些硬件（如TPU）中具有良好的⽀持。</font>

**<font style="color:#1456f0;">缺点</font>**

+ <font style="color:#1f2329;">相较float32精度较低，</font><font style="color:#dc9b04;">可能导致某些极度依赖数值精度的模型出现轻微误差</font><font style="color:#1f2329;">。</font><font style="color:#1456f0;"> </font>

:::color5
**<font style="color:#601BDE;">2.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">深度学习加速</font>**<font style="color:rgb(51, 51, 51);">：BF16设计初衷就是为深度学习加速，在处理大型模型时，BF16能够提供更高的计算效率和更好的数值稳定性。</font>
+ **<font style="color:rgb(51, 51, 51);">训练和推理</font>**<font style="color:rgb(51, 51, 51);">：在需要处理大规模数据和高精度计算的场景中，BF16表现出色，尤其适用于需要处理极端值的科学计算和工程应用。</font>
+ **<font style="color:rgb(51, 51, 51);">高性能计算（HPC）</font>**<font style="color:rgb(51, 51, 51);">：BF16在高性能计算领域也有广泛的应用，特别是在需要平衡计算速度和数值精度的任务中。</font>

### <font style="color:#1f2329;">数值范围/精度对比</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737620799828-0a5793dc-427c-4797-91ef-4c1dac55373b.png)

:::color5
**<font style="color:#601BDE;">1.数值范围比较</font>**

:::

<font style="color:#d83931;">float32和bfloat16具有相同的数值范围，因为它们都使⽤8位指数部分</font><font style="color:#1f2329;">，这使得bfloat16能够处理 与float32相当的数值范围，降低了下溢和上溢的  风险。</font>

<font style="color:#1f2329;">⽽</font><font style="color:#d83931;">float16的数值范围较⼩，容易受到数值溢出影响</font><font style="color:#1f2329;">。</font>

:::color5
**<font style="color:#601BDE;">2.精度比较</font>**

:::

<font style="color:#245bdb;">float32的精度最⾼（23位尾数），适合需要⾼精度的计算任务。</font><font style="color:#1f2329;">float16的精度次之（10位尾数），在保持范围的同时牺牲了⼀些精度，但通常仍能满⾜⼤多数深度学习任务的需求。</font>

<font style="color:#1f2329;">bfloat16的精度（7位尾数）最低，但由于其更低的存储需求，适合对精度要求较低且需要计算加速的任务。</font>





# 混合精度
## 概念
<font style="color:#1f2329;background-color:#f0fbef;">混合精度（Mixed Precision）训练是⼀种通过结合不同数值精度（如FP32和FP16）进⾏深度学习模型训练的⽅法，旨在提⾼计算效率并减少内存占⽤ ，同时在保持模型精度的前提下优化训练性能。其核    ⼼思想是，模型中的某些操作对数值精度要求较⾼，⽽另⼀些操作可以使⽤较低精度完成，从⽽在性    能与精度之间找到平衡。</font>

## <font style="color:#1f2329;background-color:#f0fbef;">原理</font>
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1737619735461-27377ba8-8d8f-4b65-a525-e229a3f13f16.png)

  


1. <font style="color:#245bdb;background-color:#f5f6f7;">初始化</font><font style="color:#1f2329;">：模型的神经⽹络权重参数最初以</font><font style="color:#dc9b04;">FP32</font><font style="color:#1f2329;">形式存储。</font>
2. <font style="color:#245bdb;background-color:#f5f6f7;">权重转换</font><font style="color:#1f2329;">：将神经⽹络的权重参数从</font><font style="color:#dc9b04;">FP32转换为FP16</font><font style="color:#1f2329;">，⽤于后续的计算。</font>
3. <font style="color:#1456f0;"> </font><font style="color:#245bdb;background-color:#f5f6f7;">前向传播与反向传播</font><font style="color:#245bdb;">  </font><font style="color:#1f2329;">：在前向和反向传播计算中</font><font style="color:#dc9b04;">使⽤FP16</font><font style="color:#1f2329;">完成主要的矩阵运算和激活函数计算，以减少内存占⽤并加速计算。反向传播过程中，梯度也使⽤FP16进⾏计算。</font>
4. <font style="color:#245bdb;background-color:#f5f6f7;">梯度转换</font><font style="color:#245bdb;">  </font><font style="color:#1f2329;">：将FP16的梯度转换回FP32，确保在梯度更新过程中使⽤更⾼精度的计算，避免精度丢失。</font>
5. <font style="color:#245bdb;background-color:#f5f6f7;">梯度更新</font><font style="color:#245bdb;"> </font><font style="color:#1f2329;">：FP32的梯度与学习率（learning rate）相乘，保证精度较⼩的数值不会因浮点数的限制⽽丢失。</font>
6. <font style="color:#245bdb;background-color:#f5f6f7;">权重更新</font><font style="color:#245bdb;"> </font><font style="color:#1f2329;">：使⽤更新后的FP32梯度更新⽹络的FP32权重。</font>

## <font style="color:#1f2329;">损失缩放</font>
<font style="color:#1f2329;">在混合精度训练中，由于FP16的数值表⽰范围较⼩，特别是在反向传播过程中，较⼩的梯度值可能会因为精度不⾜⽽变为零。为了解决这个问题，引⼊了损失缩放技术。在反向传播前，将损失值按某个  系数进⾏放⼤，确保反向传播时梯度值⾜够⼤，避免FP16下的数值下溢。计算完成后，再将梯度缩⼩相应倍数，以保证数值正确性。</font>

## <font style="color:#1f2329;">优缺点</font>
**<font style="color:#000000;">优点</font>**

<font style="color:#1456f0;">更快的计算速度</font><font style="color:#1f2329;">：FP16的计算速度通常⽐FP32快⼀倍或更多，尤其在⽀持混合精度计算的硬件上</font>

<font style="color:#1f2329;">（如</font><font style="color:#1f2329;">NVIDIA</font><font style="color:#1f2329;">的</font><font style="color:#1f2329;">Tensor Cores</font><font style="color:#1f2329;">）</font><font style="color:#1f2329;">，</font><font style="color:#1f2329;">这⼀</font><font style="color:#1f2329;">加速效应尤为明显。</font>

<font style="color:#1456f0;">更高的内存利用率：</font><font style="color:#1f2329;">FP16使⽤更少的内存，这使得在相同的硬件环境下可以训练更⼤的模型或使⽤更⼤的batch size，从⽽提⾼了训练效率。</font>

**<font style="color:#1f2329;">缺点</font>**  
<font style="color:#245bdb;">数值不稳定性</font><font style="color:#1f2329;">：FP16的精度较低，容易发⽣数值下溢或上溢问题，尤其是在梯度较⼩时。引⼊损</font>

<font style="color:#1f2329;">失缩放机制能够有效防⽌这种问题发⽣。</font>

<font style="color:#1456f0;">硬件要求</font><font style="color:#1f2329;">：混合精度训练需要特定硬件（如NVIDIA Tensor Cores）和软件（如CUDA和cuDNN） 的⽀持。幸运的是，主流的深度学习框架如PyTorch和TensorFlow已经原⽣⽀持混合精度训练。</font>

## <font style="color:#1f2329;">应用场景</font>
<font style="color:#1f2329;">混合精度训练⼴泛应⽤于⼤规模模型训练任务中</font><font style="color:#1f2329;">，特别是需要⼤批量数据和复杂⽹络的场景</font><font style="color:#1f2329;">，如</font>

<font style="color:#1f2329;">BERT、GPT系列模型等。在计算密集型硬件上，通过混合精度技术能够显著提⾼模型训练的性能，同时减少内存开销，使得在相同资源下能够训练更⼤的模型或处理更⼤的数据集。</font>

<font style="color:#1f2329;"></font>

<font style="color:#1f2329;"></font>

# <font style="color:#1f2329;">Deepseek-R1 Int8 量化 </font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">美团搜索和推荐平台部对DeepSeek R1模型进行了INT8精度量化尝试，发现使用INT8量化后模型精度基本无损。基于INT8量化，DeepSeek R1模型解锁了芯片限制，可以部署到A100等其他型号GPU；并且相比BF16实现了50%的吞吐提升，进一步降低了推理成本。量化代码已经发布在了开源LLM推理框架SGLang上，量化模型已经发布到了Hugging Face社区，方便用户使用。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">参考</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>[https://mp.weixin.qq.com/s/TCkpG1Kn9tMYQeN2PCnwoA](https://mp.weixin.qq.com/s/TCkpG1Kn9tMYQeN2PCnwoA)

:::

**<font style="color:rgba(0, 0, 0, 0.9);">背景：</font>**<font style="color:rgba(0, 0, 0, 0.9);">DeepSeek R1横空出世后，吸引了众多公司和个人用户尝试其满血版本部署。然而原生版本的模型权重为FP8数据格式，对GPU芯片类型有严格限制，仅能被英伟达新型GPU支持（</font><font style="color:rgb(136, 136, 136);">如Ada、Hopper架构芯片</font><font style="color:rgba(0, 0, 0, 0.9);">），其他型号GPU（</font><font style="color:rgb(136, 136, 136);">如A100</font><font style="color:rgba(0, 0, 0, 0.9);">）无法直接部署。尽管我们可以将FP8权重反量化为BF16权重后，在A100等GPU上进行推理，但是这对显存的要求提升了一倍，推理吞吐也会下降。</font>

:::color5
**<font style="color:#601BDE;">1.DeepSeek R1 精度介绍</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">根据DeepSeek最新发布的技术报告，V3/R1突破性的训练成本控制</font>**<font style="color:#ED740C;">主要依托FP8精度训练方案</font>**<font style="color:rgba(0, 0, 0, 0.9);">。FP8是一种典型的模型量化技术，相较于业界常用的BF16精度，FP8精度通过将数据位宽减半显著降低了单次计算开销，但也会带来一定的精度损失。在实践中，DeepSeek R1采用了混合精度训练机制有效缓解了精度损失问题。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337466071-41be5e80-9280-4745-ae0c-a953d0b59699.png)

<font style="color:rgba(0, 0, 0, 0.9);">由于DeepSeek R1采用FP8精度训练，所以开源的原生权重就是FP8精度。在推理时，为了尽可能地降低模型精度损失，同时保持和FP8类似的推理吞吐，我们自然想到使用和FP8精度等位宽的INT8精度进行平替。同时，INT8精度被广泛硬件原生支持，基于INT8精度可以极大拓展DeepSeek模型的硬件部署范围。因此，我们开始探索INT8量化在DeepSeek R1上的可行性。</font>

:::color5
**<font style="color:#601BDE;">2.量化基本原理</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">模型量化是将</font>**<font style="color:#ED740C;">模型的权重和激活值</font>**<font style="color:rgba(0, 0, 0, 0.9);">等数据从高精度（</font><font style="color:rgb(136, 136, 136);">如BF16</font><font style="color:rgba(0, 0, 0, 0.9);">）转化为低精度（</font><font style="color:rgb(136, 136, 136);">如INT8</font><font style="color:rgba(0, 0, 0, 0.9);">），并尽可能保证转化前后模型效果一致的过程。以常见的INT8对称量化为例，量化过程如下所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337390429-4b8650fb-fb0f-492e-bd25-81ff88796695.png)

**<font style="color:rgba(0, 0, 0, 0.9);">1.计算缩放因子 x</font>**<sub>**<font style="color:rgba(0, 0, 0, 0.9);">scale</font>**</sub>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337407391-bf3653a0-7a14-47b6-a9b5-0f1cbebce50e.png)

**<font style="color:rgba(0, 0, 0, 0.9);">2.在适当位置做量化（Quant）和反量化（Dequant）</font>**

<font style="color:rgba(0, 0, 0, 0.9);">量化公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337424665-b2b3c903-2f7d-44f6-ab4d-68a75f7e7f68.png)

<font style="color:rgba(0, 0, 0, 0.9);">反量化公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337432779-1e890c7c-025f-4300-b770-2cb18f7834c3.png)

**<font style="color:rgba(0, 0, 0, 0.9);">3.FP16计算可以转为INT8计算</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337447498-535dedfa-e348-4c4e-8686-2ce5ecac4630.png)

:::color5
**<font style="color:#601BDE;">3.</font>****<font style="color:#601BDE;">量化方案设计</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">我们在综合考虑量化后模型的精度和推理性能后，选择了分块量化（</font><font style="color:rgb(136, 136, 136);">Block-wise Quantization</font><font style="color:rgba(0, 0, 0, 0.9);">）和通道量化（</font><font style="color:rgb(136, 136, 136);">Channel-wise Quantization</font><font style="color:rgba(0, 0, 0, 0.9);">）两种方案。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741337805945-8f9f5eb3-2787-46fd-a757-82b553e87c56.png)

1. **分块量化**

**<font style="color:rgba(0, 0, 0, 0.9);">优点：</font>**<font style="color:rgba(0, 0, 0, 0.9);">分块量化是DeepSeek V3/R1降低量化损失的关键技术之一。分块量化通过对权重矩阵的细粒度切分，将量化操作的范围控制在[128, 128]的矩阵内，</font>**<font style="color:#DF2A3F;">减少了分布分散的出现概率，从而很好地控制了每次量化过程中的损失。</font>**

**<font style="color:rgba(0, 0, 0, 0.9);">步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">为了尽可能地减少量化后模型的精度损失，我们延续了DeepSeek训练的量化策略。在实践中，由于DeepSeek官方并没有提供半精度浮点型（</font><font style="color:rgb(136, 136, 136);">BF16</font><font style="color:rgba(0, 0, 0, 0.9);">）的权重，因此首先需要将原生的FP8模型权重反量化成BF16，再分块量化成INT8精度。为了匹配权重的分块量化，激活值采用在线逐token-group的量化方式，</font>**<font style="color:#DF2A3F;">即每个token的嵌入向量分为多个组，逐组进行量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

2. **<font style="color:rgba(0, 0, 0, 0.9);">通道量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>

**<font style="color:rgba(0, 0, 0, 0.9);">优点</font>**<font style="color:rgba(0, 0, 0, 0.9);">：除了上述的分块量化外，我们还探索了更高效的通道量化，</font>**<font style="color:#ED740C;">即权重的每列为一组进行量化</font>**<font style="color:rgba(0, 0, 0, 0.9);">。通道量化在执行完INT8的矩阵乘法后，只需进行一次反量化计算，</font>**<font style="color:#ED740C;">计算开销相比分块量化更低</font>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">缺点</font>**<font style="color:rgba(0, 0, 0, 0.9);">：由于通道量化在量化一列元素时，更容易遇到离群值（</font><font style="color:rgb(136, 136, 136);">Outlier</font><font style="color:rgba(0, 0, 0, 0.9);">），因此相比分块量化会有更多的精度损失。</font>

**<font style="color:rgba(0, 0, 0, 0.9);">步骤：</font>**<font style="color:rgba(0, 0, 0, 0.9);">在具体实践中，同样地先将原生FP8的模型权重反量化成BF16，之后逐通道量化成INT8类型。同时，对激活值采用在线逐token量化，最大程度地减少activation的量化损失。</font>

:::color5
**<font style="color:#601BDE;">4.量化效果评估</font>**

:::

1. **精度**

<font style="color:rgba(0, 0, 0, 0.9);">我们分别应用上述两种量化方法，对开源的DeepSeek R1模型进行了INT8量化处理，并在GSM8K和MMLU两个数据集上对量化后的模型进行了精度评估。评估结果如下表所示，相比基线的BF16和FP8模型，两种INT8量化模型的精度基本无损。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741338057133-6ee0243a-711d-418e-b78c-324854de2376.png)

2. **<font style="color:rgba(0, 0, 0, 0.9);">推理速度</font>**

<font style="color:rgba(0, 0, 0, 0.9);">我们在知名开源推理框架SGLang上，对上述两种INT8量化方法进行了推理支持（</font><font style="color:rgba(0, 0, 0, 0.9);">分块量化</font><font style="color:rgba(0, 0, 0, 0.9);">、</font><font style="color:rgba(0, 0, 0, 0.9);">通道量化</font><font style="color:rgba(0, 0, 0, 0.9);">）。SGLang是当前SOTA的开源LLM推理框架，在DeepSeek系列模型上有着最优的推理性能，被业界广泛使用。</font>

<font style="color:rgba(0, 0, 0, 0.9);">以BF16模型为Baseline，我们在A100-80G GPU上对两种INT8模型进行了推理吞吐评估。得益于更低的显存要求，INT8量化模型仅需要16张A100 GPU即可推理，但是BF16模型需要32张A100 GPU。为了比较的公平性，我们统一在32张A100 GPU上进行吞吐测试。结果如下表所示，分块量化的INT8推理相比BF16可以提升33%的吞吐；通道量化的INT8推理得益于更低的反量化开销，可以进一步达到50%的吞吐提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741338086042-9b85a191-e2c6-4e85-b0ab-2b4a9242e84f.png)



