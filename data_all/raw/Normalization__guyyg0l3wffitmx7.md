# Normalization

<!-- source: yuque://zhongxian-iiot9/hlyypb/guyyg0l3wffitmx7 -->

# Normalization
| **方法** | **归一化维度** | **适用场景** | **优点** | **缺点** |
| --- | --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">BatchNorm</font>** | <font style="color:rgb(51, 51, 51);">批量维度 (N)</font> | <font style="color:rgb(51, 51, 51);">大Batch Size的CNN</font> | <font style="color:rgb(51, 51, 51);">加速训练，正则化</font> | <font style="color:rgb(51, 51, 51);">依赖Batch Size</font> |
| **<font style="color:rgb(51, 51, 51);">LayerNorm</font>** | <font style="color:rgb(51, 51, 51);">特征维度 (C/H/W)</font> | <font style="color:rgb(51, 51, 51);">NLP、RNN、小批量</font> | <font style="color:rgb(51, 51, 51);">对序列数据友好</font> | <font style="color:rgb(51, 51, 51);">对CNN效果一般</font> |
| **<font style="color:rgb(51, 51, 51);">GroupNorm</font>** | <font style="color:rgb(51, 51, 51);">分组通道 (C/G)</font> | <font style="color:rgb(51, 51, 51);">小批量、目标检测/视频任务</font> | <font style="color:rgb(51, 51, 51);">灵活性强，不依赖Batch Size</font> | <font style="color:rgb(51, 51, 51);">需手动调组数</font> |


<font style="color:rgb(51, 51, 51);">选择时需根据任务类型、数据分布和硬件条件权衡。例如：</font>

+ **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">：优先BatchNorm。</font>
+ **<font style="color:rgb(51, 51, 51);">Transformer模型</font>**<font style="color:rgb(51, 51, 51);">：选择LayerNorm。</font>
+ **<font style="color:rgb(51, 51, 51);">目标检测</font>**<font style="color:rgb(51, 51, 51);">：使用GroupNorm或SyncBN。</font>



应用场景对比：

+ **BatchNorm**：适用于大多数深度前馈神经网络和卷积神经网络，尤其在批量大小较大的情况下表现优异。但在小批量情况下，可能需要调整epsilon参数以避免不稳定的归一化结果。
+ **LayerNorm**：适合处理序列数据（如RNN、Transformer）和嵌入层，特别是在小批量或单样本训练时表现稳定。LayerNorm在语言模型和生成模型中尤为常用。
+ **RMSNorm**：在计算速度和稳定性之间提供了一个好的折中方案，适合需要快速计算且希望保持BatchNorm优势的场景。RMSNorm在大规模数据和高性能计算中表现良好。

# BatchNorm
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">对每层输入进行标准化（减均值、除标准差），加速训练并轻微正则化。</font>

<font style="color:rgb(51, 51, 51);">BatchNorm通过对每个特征通道在</font>**<font style="color:#ED740C;">批量维度</font>**<font style="color:rgb(51, 51, 51);">上进行归一化（即对同一通道的不同样本数据做归一化），缓解内部协变量偏移问题。核心思想是</font>**<font style="color:#ED740C;">在批维度上对输入，使得输入分布稳定在零均值和单位方差附近，从而加速模型训练</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算当前批次的均值 μ和方差 σ2：对于输入张量 </font><font style="color:rgb(51, 51, 51);">X∈R</font><sup><font style="color:rgb(51, 51, 51);">N×C×H×W</font></sup><font style="color:rgb(51, 51, 51);">（N为batch size，C为通道数）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470042065-f8e76a75-271f-4d69-a050-10da05b67a24.png)

2. <font style="color:rgb(51, 51, 51);">标准化：其中 </font><font style="color:rgb(51, 51, 51);">ϵ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是防止除零的小常数。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470069951-e1119ad5-b757-4839-9991-d017c0177971.png)

3. **<font style="color:rgb(51, 51, 51);">仿射变换</font>**<font style="color:rgb(51, 51, 51);">：引入可学习的参数 </font><font style="color:rgb(51, 51, 51);">γc</font><font style="color:rgb(51, 51, 51);"> 和 </font><font style="color:rgb(51, 51, 51);">βc</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470091885-7687d55e-e0b7-4973-912e-4bf8ebc2489f.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">加速模型收敛，允许更大的学习率。</font>
    - <font style="color:rgb(51, 51, 51);">减少对参数初始化的依赖。</font>
    - <font style="color:rgb(51, 51, 51);">有一定正则化效果（因小批量统计噪声）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Batch Size较小时效果不稳定。</font>
    - <font style="color:rgb(51, 51, 51);">对序列模型（如RNN）不友好。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">深层网络（如ResNet）</font>
+ <font style="color:rgb(51, 51, 51);">训练不稳定的场景</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">Batch Renormalization</font>**<font style="color:rgb(51, 51, 51);">：允许动态调整标准化范围。</font>
+ **<font style="color:rgb(51, 51, 51);">SyncBN</font>**<font style="color:rgb(51, 51, 51);">：多卡训练时同步不同设备的统计量。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch

class ManualBatchNorm1d:
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        self.gamma = torch.ones(num_features)   # 缩放参数
        self.beta = torch.zeros(num_features)   # 偏移参数
        self.eps = eps
        self.momentum = momentum
        
        # 全局统计量
        self.running_mean = torch.zeros(num_features)
        self.running_var = torch.ones(num_features)
        
    def __call__(self, x, training=True):
        if training:
            # 计算当前 batch 的均值和方差
            batch_mean = x.mean(dim=0)
            batch_var = x.var(dim=0, unbiased=False)
            
            # 更新全局统计量
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * batch_mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * batch_var
        else:
            batch_mean = self.running_mean
            batch_var = self.running_var
        
        # 归一化
        x_hat = (x - batch_mean) / torch.sqrt(batch_var + self.eps)
        return self.gamma * x_hat + self.beta

# 示例用法
x = torch.randn(32, 64)  # (batch_size, num_features)
bn = ManualBatchNorm1d(64)
out = bn(x, training=True)

```





# LayerNorm
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">LayerNorm对</font>**<font style="color:rgb(51, 51, 51);">单个样本的所有特征</font>**<font style="color:rgb(51, 51, 51);">进行归一化（即对同一样本的不同通道/神经元做归一化），常用于处理变长序列或小批量数据。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算当前批次的均值 μ和方差 σ2：对于输入张量 </font><font style="color:rgb(51, 51, 51);">X∈R</font><sup><font style="color:rgb(51, 51, 51);">N×D</font></sup><font style="color:rgb(51, 51, 51);">（D为特征维度）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470633369-5ebd789d-ad0b-4b21-b863-f46ef04365d3.png)

2. <font style="color:rgb(51, 51, 51);">标准化：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470652940-83f8a552-857e-486c-9e89-6bbb07733ed1.png)

3. **<font style="color:rgb(51, 51, 51);">仿射变换</font>**<font style="color:rgb(51, 51, 51);">：参数 </font><font style="color:rgb(51, 51, 51);">γ</font><font style="color:rgb(51, 51, 51);">和 </font><font style="color:rgb(51, 51, 51);">β</font><font style="color:rgb(51, 51, 51);">的维度为 </font><font style="color:rgb(51, 51, 51);"></font><font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470679364-dc09e1c7-a196-444c-ae71-7b84fbf2b6d0.png)

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">不依赖Batch Size，适合小批量或在线学习。</font>
    - <font style="color:rgb(51, 51, 51);">对序列模型友好（如Transformer）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">在CNN中效果可能弱于BatchNorm。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">NLP模型（如Transformer、BERT）。</font>
+ <font style="color:rgb(51, 51, 51);">RNN/LSTM时序模型。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">RMS Norm</font>**<font style="color:rgb(51, 51, 51);">：移除均值中心化，仅用方差归一化。</font>
+ **<font style="color:rgb(51, 51, 51);">Adaptive LayerNorm</font>**<font style="color:rgb(51, 51, 51);">：动态调整归一化参数。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class ManualLayerNorm:
    def __init__(self, normalized_shape, eps=1e-5):
        self.gamma = torch.ones(normalized_shape)  # 缩放参数
        self.beta = torch.zeros(normalized_shape)  # 偏移参数
        self.eps = eps
        
    def __call__(self, x):
        # 计算最后N个维度的均值和方差（例如输入为[B, C, H, W]，则对C/H/W计算）
        dims = [-i for i in range(1, len(self.gamma.shape)+1)]
        mean = x.mean(dim=dims, keepdim=True)
        var = x.var(dim=dims, keepdim=True, unbiased=False)
        
        # 归一化
        x_hat = (x - mean) / torch.sqrt(var + self.eps)
        return self.gamma * x_hat + self.beta

# 示例用法
x = torch.randn(32, 128, 10, 10)  # (B, C, H, W)
ln = ManualLayerNorm(x.shape[1:])  # 对后3个维度归一化
out = ln(x)

```



# GroupNorm
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">GroupNorm将通道分为若干组（Group），对每个组内的特征进行归一化。介于LayerNorm和InstanceNorm之间，适合小批量或动态Batch Size场景。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **分组**  
输入 X∈R<sup>N×C×H×W</sup>，将通道分为 G组，每组 C/G__通道。
2. **计算均值和方差**  
对每个样本 n_n_ 和组 g_g_：

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470730586-2616fb06-ab90-4b34-9dcf-b32893317bff.png)

3. **标准化与仿射变换**  
类似BatchNorm，但仅作用于组内。  


:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">不受Batch Size影响。</font>
    - <font style="color:rgb(51, 51, 51);">在目标检测、视频处理中表现稳定。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">需要手动选择组数 G</font>_<font style="color:rgb(51, 51, 51);">G</font>_<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">小批量训练（如目标检测模型Mask R-CNN）。</font>
+ <font style="color:rgb(51, 51, 51);">动态Batch Size任务（如视频分类）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">Switchable GroupNorm</font>**<font style="color:rgb(51, 51, 51);">：动态调整组数。</font>
+ **<font style="color:rgb(51, 51, 51);">Weight Standardization</font>**<font style="color:rgb(51, 51, 51);">：结合权重标准化提升效果。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
class ManualGroupNorm:
    def __init__(self, num_groups, num_channels, eps=1e-5):
        assert num_channels % num_groups == 0
        self.num_groups = num_groups
        self.eps = eps
        self.gamma = torch.ones(num_channels)  # 缩放参数
        self.beta = torch.zeros(num_channels)  # 偏移参数
        
    def __call__(self, x):
        batch_size, num_channels, *dims = x.shape
        group_size = num_channels // self.num_groups
        
        # 将通道分组 [B, C, H, W] => [B, G, C//G, H, W]
        x_grouped = x.view(batch_size, self.num_groups, group_size, *dims)
        
        # 计算每组均值和方差
        mean = x_grouped.mean(dim=[2,3,4], keepdim=True)  # 对组内所有特征计算
        var = x_grouped.var(dim=[2,3,4], keepdim=True, unbiased=False)
        
        # 归一化并恢复形状
        x_hat = (x_grouped - mean) / torch.sqrt(var + self.eps)
        x_hat = x_hat.view(batch_size, num_channels, *dims)
        
        return self.gamma[None, :, None, None] * x_hat + self.beta[None, :, None, None]

# 示例用法
x = torch.randn(32, 64, 28, 28)  # (B, C, H, W)
gn = ManualGroupNorm(num_groups=8, num_channels=64)
out = gn(x)

```





# RMS Norm<font style="color:#D22D8D;"></font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>RMSNorm则不涉及均值和⽅差的计算，⽽是通过**<font style="color:#ED740C;">均⽅根（RootMeanSquare, RMS）</font>**来进⾏规范化。其核⼼思想是基于输⼊的幅值（magnitude），⽽不依赖于其均值。

:::

<font style="color:#1f2329;">LayerNorm</font><font style="color:#1f2329;">和 </font><font style="color:#1f2329;">RMSNorm</font><font style="color:#1f2329;">都是有效的正则化⽅法</font><font style="color:#1f2329;">，但它们在核⼼的计算⽅式和应⽤场景上有所</font><font style="color:#1f2329;">不同：</font>

+ <font style="color:#1f2329;">LayerNorm更适合处理</font>**<font style="color:#74B602;">均值与⽅差对特征影响较⼤的任务</font>**<font style="color:#1f2329;"> ，特别是⼩批量数据和 NLP任务中。</font>
+ <font style="color:#1f2329;">RMSNorm 则适⽤于幅度归⼀化为主、特征幅度较⼤的场景，如深层神经⽹络或⾼维数据中，同时它的计算效率也更⾼。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:#1f2329;">RMSNorm 计算输⼊向量的均⽅根</font><font style="color:#1f2329;">RMS(</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">)</font><font style="color:#1f2329;">:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908081952-b4f1a48e-26e6-4c12-9fa4-44dd5e53401f.png)

2. <font style="color:#1f2329;">将输⼊向量</font>_<font style="color:#1f2329;">x</font>_<font style="color:#1f2329;">∈R</font>_<font style="color:#1f2329;">d  </font>_<font style="color:#1f2329;">⽤RMS 归⼀化  ( </font>_<font style="color:#1f2329;">ϵ  </font>_<font style="color:#1f2329;">⽤于防⽌除零错误）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908079138-379833dc-0909-46ff-be72-9b1fc60c711f.png)

3. <font style="color:#1f2329;">最后，通过可学习的参数</font>_<font style="color:#1f2329;">γ</font>_<font style="color:#1f2329;">⾏重缩放，并加上偏置</font>_<font style="color:#1f2329;">β  </font>_<font style="color:#1f2329;">: </font>_<font style="color:#1f2329;">y</font>_<font style="color:#1f2329;">=</font>_<font style="color:#1f2329;">γx</font>_<font style="color:black;">(</font><font style="color:black;">^</font><font style="color:black;">)</font><font style="color:#1f2329;">+</font>_<font style="color:#1f2329;">β</font>_

:::color5
**<font style="color:#601BDE;">2.应用场景对比</font>**

:::

+ **BatchNorm**：适用于大多数**<font style="color:#74B602;">深度前馈神经网络和卷积神经网络</font>**，尤其在批量大小较大的情况下表现优异。但在小批量情况下，可能需要调整epsilon参数以避免不稳定的归一化结果。
+ **LayerNorm**：适合处理**<font style="color:#74B602;">序列数据（如RNN、Transformer）和嵌入层</font>**，特别是在小批量或单样本训练时表现稳定。LayerNorm在语言模型和生成模型中尤为常用。
+ **RMSNorm**：在计算速度和稳定性之间提供了一个好的折中方案，**<font style="color:#74B602;">适合需要快速计算且希望保持BatchNorm优势的场景</font>**。RMSNorm在大规模数据和高性能计算中表现良好。

:::color5
**<font style="color:#601BDE;">3.实现代码示例</font>**

:::

```python
class RMSNorm(nn.Module):
    def __init__(self, features):
        super(RMSNorm, self).__init__()
        self.gamma = nn.Parameter(torch.ones(features))
        self.beta = nn.Parameter(torch.zeros(features))
        self.epsilon = 1e-5
    
    def forward(self, x):
        # 计算平方的平均值
        if x.ndim == 2:
            RMS = torch.sqrt(x.pow(2).mean(dim=0, keepdim=True) + self.epsilon)
        else:
            axes = list(range(x.ndim - 1))
            RMS = torch.sqrt(x.pow(2).mean(axes, keepdim=True) + self.epsilon)
        
        # 归一化
        x_normalized = x / RMS
        
        # 应用gamma和beta
        output = self.gamma * x_normalized + self.beta
        return output
```

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">与LayerNorm对比</font>**

:::

| <font style="color:#6425d0;">特性</font> | <font style="color:#6425d0;">LayerNorm</font> | <font style="color:#6425d0;">RMSNorm</font> |
| --- | --- | --- |
| <font style="color:#6425d0;">均值计算</font> | <font style="color:#1f2329;">需要计算均值</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908233712-8d585634-9951-4774-a2d5-7ec402dad6b4.png) | <font style="color:#1f2329;">不计算均值</font> |
| <font style="color:#6425d0;">⽅差计算</font> | <font style="color:#1f2329;">需要计算⽅差</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908233808-21921848-c4ab-4a09-aaf4-2923de9380e0.png) | <font style="color:black;"></font><br/><font style="color:#1f2329;">不计算⽅差</font> |
| <font style="color:#6425d0;">归⼀化⽅法</font> | <font style="color:#1f2329;">基于均值和⽅差</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908233805-45de0554-385a-4f9c-bf9c-425d2603c13d.png) | <font style="color:#1f2329;">基于均⽅根</font><font style="color:#1f2329;"> </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1738908233814-6a0bb2e6-b0bc-42f4-9c19-891c2cb7daa8.png) |
| <font style="color:#6425d0;">正则化对象</font> | <font style="color:#1f2329;">对输⼊进⾏零均值和单位⽅差的归⼀化</font> | <font style="color:#1f2329;">仅对输⼊幅值进⾏幅度归⼀化</font> |
| <font style="color:black;"></font><br/><font style="color:#6425d0;">计算复杂度</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">需要计算均值、⽅差</font><font style="color:#1f2329;">，复杂度较⾼</font> | <font style="color:#1f2329;">只计算均⽅根</font><font style="color:#1f2329;">，计算量更低</font> |
| <font style="color:#6425d0;">对⼩尺度特</font><font style="color:#6425d0;">征的影响</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">可能会导致较⼩的特征值被过度平滑</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">对特征值影响较⼩</font><font style="color:#1f2329;">，尤其是⼩尺度特征</font> |
| <font style="color:#6425d0;">⾼维数据表</font><font style="color:#6425d0;">现</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">在⾼维数据上表现良好</font> | <font style="color:#1f2329;">在⾼维数据上表现更稳定</font><font style="color:#1f2329;">，且具有更⾼</font><font style="color:#1f2329;">效率</font> |
| <font style="color:#6425d0;">在深层⽹络</font><font style="color:#6425d0;">中的效果</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">随着层数增加</font><font style="color:#1f2329;">，过度平滑问题较为显著</font> | <font style="color:#1f2329;">深层⽹络中效果更佳</font><font style="color:#1f2329;">，特征信息保留更</font><font style="color:#1f2329;"> 好</font> |
| <font style="color:#6425d0;">梯度回传的</font><font style="color:#6425d0;">稳定性</font> | <font style="color:#1f2329;">提供⼀定的梯度稳定性</font><font style="color:#1f2329;">，防⽌梯度爆炸或</font><font style="color:#1f2329;">消失</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">更稳定的梯度回传</font><font style="color:#1f2329;">，尤其在复杂模型中</font> |
| <font style="color:#6425d0;">对训练收敛</font><font style="color:#6425d0;">速度的影响</font> | <font style="color:black;"></font><br/><font style="color:#1f2329;">提供更稳定的收敛速度</font><font style="color:#1f2329;">，适⽤于⼀般任务</font> | <font style="color:#1f2329;">提供较快的收敛速度</font><font style="color:#1f2329;">，适⽤于需要更快</font><font style="color:#1f2329;">计算的任务</font> |






# PreNorm & PostNorm
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在 Transformer 架构中，</font>**<font style="color:rgb(51, 51, 51);">PreNorm</font>**<font style="color:rgb(51, 51, 51);"> 和 </font>**<font style="color:rgb(51, 51, 51);">PostNorm</font>**<font style="color:rgb(51, 51, 51);"> 是两种不同的 </font>**<font style="color:rgb(51, 51, 51);">层归一化（Layer Normalization）</font>**<font style="color:rgb(51, 51, 51);"> 位置设计，主要区别在于归一化层与残差连接的顺序。它们直接影响模型的训练稳定性、梯度传播效果和最终性能。</font>

**<font style="color:rgb(51, 51, 51);">PreNorm 更适合深层模型：</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);"> PreNorm 在残差分支外执行归一化，避免了梯度通过多个归一化层，缓解了梯度消失问题。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">Pre-Norm</font>**

+ <font style="color:#1f2329;">在Pre-Norm架构中 ，规范化操作（ RMSNorm或LayerNorm）是在</font>**<font style="color:#ED740C;">⾃注意⼒（Self-  Attention）或前馈神经⽹络（FFN）计算之前</font>**<font style="color:#1f2329;">进⾏的。也就是说，每⼀层的输⼊⾸先被归⼀化，然后再传递到注意⼒或前馈层。</font>
+ **<font style="color:#ED740C;">Pre-Norm能够确保在深层⽹络中输⼊的幅度始终处于稳定范围，这对⻓链路依赖的模型尤其有益。</font>**<font style="color:#1f2329;">通过归⼀化操作的提前进⾏，模型能以更加稳定的输⼊进⾏学习，从⽽有助于解决深层模型中梯度消失的问题。</font>

```python
# 输入 x
x = x + Sublayer(LayerNorm(x))  # Sublayer 可以是自注意力或前馈网络
```

**Post-Norm**

+ <font style="color:#1f2329;">在Post-Norm架构中，规范化操作是在</font>**<font style="color:#245bdb;">⾃注意⼒或FFN计算之后进⾏</font>**<font style="color:#1f2329;">的。模型⾸先经过未归⼀化的操作，最后将结果归⼀化以确保模型的输出平衡。</font>
+ <font style="color:#1f2329;">Post-Norm可以在训练初期获得较好的收敛效果，尤其是在浅层模型中表现良好。</font>**<font style="color:#245bdb;">然⽽，在深层⽹络中，Post-Norm的缺点是可能会导致训练过程中的梯度不稳定</font>**<font style="color:#1f2329;">，特别是随着⽹络深度的增加，梯度可能在传播过程中变得越来越不稳定。</font>
+ <font style="color:rgb(51, 51, 51);">PostNorm 的输出会被归一化，</font>**<font style="color:#117CEE;">需要更小的初始化</font>**<font style="color:rgb(51, 51, 51);">，参数初始化需更谨慎（如使用 </font>`<font style="color:rgb(51, 51, 51);">kaiming_normal_</font>`<font style="color:rgb(51, 51, 51);"> 或 </font>`<font style="color:rgb(51, 51, 51);">xavier_uniform_</font>`<font style="color:rgb(51, 51, 51);">）。</font>

```python
# 输入 x
x = LayerNorm(x + Sublayer(x))  # Sublayer 可以是自注意力或前馈网络
```

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

|  | PreNorm | PostNorm |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">优点</font>** | <font style="color:rgb(51, 51, 51);">- 梯度传播更稳定，适合深层模型   </font><font style="color:rgb(51, 51, 51);">- 训练初期收敛更快</font> | <font style="color:rgb(51, 51, 51);">- 输出严格归一化，训练过程更稳定   </font><font style="color:rgb(51, 51, 51);">- 适合浅层模型或简单任务</font> |
| **<font style="color:rgb(51, 51, 51);">缺点</font>** | <font style="color:rgb(51, 51, 51);">- 训练初期可能不稳定   </font><font style="color:rgb(51, 51, 51);">- 需要更精细的学习率调整</font> | <font style="color:rgb(51, 51, 51);">- 深层模型梯度可能消失   </font><font style="color:rgb(51, 51, 51);">- 训练速度较慢</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">PreNorm</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - **<font style="color:rgb(51, 51, 51);">GPT 系列</font>**<font style="color:rgb(51, 51, 51);">（如 GPT-2、GPT-3）、</font>**<font style="color:rgb(51, 51, 51);">T5</font>**<font style="color:rgb(51, 51, 51);">、</font>**<font style="color:rgb(51, 51, 51);">BART</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:#ED740C;">大多数现代大模型（尤其是深层模型）</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">PostNorm</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - **<font style="color:rgb(51, 51, 51);">原始 Transformer</font>**<font style="color:rgb(51, 51, 51);">（Vaswani et al., 2017）、</font>**<font style="color:rgb(51, 51, 51);">BERT</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">早期 Transformer 变体。</font>

:::color5
**<font style="color:#601BDE;">4.如何选择 PreNorm/PostNorm？</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">任务复杂度</font>**<font style="color:rgb(51, 51, 51);">: 简单任务用 PostNorm，复杂任务用 PreNorm。</font>
+ **<font style="color:rgb(51, 51, 51);">模型深度</font>**<font style="color:rgb(51, 51, 51);">: 深层模型优先选择 PreNorm。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn

class PreNormTransformerLayer(nn.Module):
    def __init__(self, dim, attention, ff):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        self.attention = attention
        self.ff = ff

    def forward(self, x):
        # 自注意力子层（PreNorm）
        x = x + self.attention(self.norm1(x))
        # 前馈子层（PreNorm）
        x = x + self.ff(self.norm2(x))
        return x

```

```python
class PostNormTransformerLayer(nn.Module):
    def __init__(self, dim, attention, ff):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        self.attention = attention
        self.ff = ff

    def forward(self, x):
        # 自注意力子层（PostNorm）
        x = self.norm1(x + self.attention(x))
        # 前馈子层（PostNorm）
        x = self.norm2(x + self.ff(x))
        return x

```

