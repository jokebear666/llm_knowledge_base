# 超参数

<!-- source: yuque://zhongxian-iiot9/hlyypb/kuggf894chsix1uz -->

# 超参数
```python
{
  "learning_rate": 1e-4,
  "batch_size": 4096,              # 配合梯度累积实现
  "warmup_steps": 10000,           # 前10k步预热
  "total_steps": 1000000,
  "adam_betas": (0.9, 0.999),
  "weight_decay": 0.01,
  "gradient_clipping": 1.0,
  "dropout": 0.1,
}
```

**调整建议**

1. **<font style="color:rgb(51, 51, 51);">从小规模实验开始</font>**<font style="color:rgb(51, 51, 51);">：在大规模训练前，用小规模数据调整超参数。</font>
2. **<font style="color:rgb(51, 51, 51);">监控损失曲线</font>**<font style="color:rgb(51, 51, 51);">：观察训练/验证损失是否稳定下降。</font>
3. **<font style="color:rgb(51, 51, 51);">参考已有配置</font>**<font style="color:rgb(51, 51, 51);">：如Hugging Face或Megatron-LM的公开参数。</font>
4. **<font style="color:rgb(51, 51, 51);">自动化调参</font>**<font style="color:rgb(51, 51, 51);">：使用网格搜索或贝叶斯优化（资源允许时）。</font>

  


# 学习率 
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">控制参数更新的步长，是影响模型收敛性和稳定性的关键参数。</font>

:::

:::color5
**<font style="color:#601BDE;">1.对训练的影响</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">过大</font>**<font style="color:rgb(51, 51, 51);">：可能导致震荡（loss剧烈波动）或不收敛。</font>
+ **<font style="color:rgb(51, 51, 51);">过小</font>**<font style="color:rgb(51, 51, 51);">：训练速度慢，可能陷入局部极小值。</font>

:::color5
**<font style="color:#601BDE;">2.推荐设置</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">初始值</font>**<font style="color:rgb(51, 51, 51);">：通常在</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">1e-5</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">到</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">1e-4</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">之间（例如BERT用</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">1e-4</font>`<font style="color:rgb(51, 51, 51);">，GPT-3用</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">6e-5</font>`<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">调度策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">预热（Warmup）</font>**<font style="color:rgb(51, 51, 51);">：前1-2%的训练步数逐步提高学习率（如从0线性增加到目标值），避免早期梯度不稳定。</font>
    - **<font style="color:rgb(51, 51, 51);">衰减</font>**<font style="color:rgb(51, 51, 51);">：采用余弦衰减或线性衰减，逐步降低学习率。</font>
+ **<font style="color:rgb(51, 51, 51);">自适应优化器</font>**<font style="color:rgb(51, 51, 51);">：如Adam默认学习率为 </font>`<font style="color:rgb(51, 51, 51);">3e-4</font>`<font style="color:rgb(51, 51, 51);">，但需根据任务调整。</font>

## 学习率和batchsize的关联 & 影响
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：两者的相互影响</font>

+ **<font style="color:rgb(51, 51, 51);">梯度方差</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Batch size 越大，梯度估计方差越小。</font>
    - <font style="color:rgb(51, 51, 51);">学习率需要配合梯度方差调整：</font>**<font style="color:rgb(51, 51, 51);">方差小 → 允许更大的学习率</font>**<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">更新方向</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">小 batch size 的梯度噪声相当于隐式正则化，可能提升泛化性。</font>
    - **<font style="color:#ED740C;">大 batch size 需要更高的学习率补偿梯度的“平滑性”</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

**<font style="color:rgb(51, 51, 51);">1. 学习率的作用</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：学习率控制参数更新的步长。</font>
+ **<font style="color:rgb(51, 51, 51);">过大</font>**<font style="color:rgb(51, 51, 51);">：参数更新剧烈，可能导致震荡甚至发散。</font>
+ **<font style="color:rgb(51, 51, 51);">过小</font>**<font style="color:rgb(51, 51, 51);">：收敛速度慢，易陷入局部极小值。</font>

**<font style="color:rgb(51, 51, 51);">2. Batch size 的作用</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：单个迭代（iteration）中用于计算梯度的样本数。</font>
+ **<font style="color:rgb(51, 51, 51);">过大</font>**<font style="color:rgb(51, 51, 51);">：梯度估计方差小，但内存占用高、训练速度慢。</font>
+ **<font style="color:rgb(51, 51, 51);">过小</font>**<font style="color:rgb(51, 51, 51);">：梯度估计噪声大，收敛不稳定。</font>  


:::color5
**<font style="color:#601BDE;">1.实验规律</font>**

:::

| **Batch Size** | **学习率调整策略** | **适用场景** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">小 (B < 256)</font> | <font style="color:rgb(51, 51, 51);">线性缩放（η ∝ B）</font> | <font style="color:rgb(51, 51, 51);">常规数据规模</font> |
| <font style="color:rgb(51, 51, 51);">大 (B ≥ 1024)</font> | <font style="color:rgb(51, 51, 51);">平方根缩放（η ∝ √B）</font> | <font style="color:rgb(51, 51, 51);">超大规模分布式训练</font> |
| <font style="color:rgb(51, 51, 51);">极大 (B ≥ 1e4)</font> | <font style="color:rgb(51, 51, 51);">渐进式缩放（如 η ∝ B^0.3）</font> | <font style="color:rgb(51, 51, 51);">极端 batch size 场景</font> |


:::color5
**<font style="color:#601BDE;">2.实验现象与结论</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 固定学习率 vs 调整学习率</font>**

+ **<font style="color:rgb(51, 51, 51);">不调整学习率</font>**<font style="color:rgb(51, 51, 51);">：增大 batch size 可能导致：</font>
    - **<font style="color:rgb(51, 51, 51);">收敛慢</font>**<font style="color:rgb(51, 51, 51);">：相同 epoch 下更新次数减少。</font>
    - **<font style="color:rgb(51, 51, 51);">泛化差</font>**<font style="color:rgb(51, 51, 51);">：梯度噪声减少，模型易过拟合。</font>
+ **<font style="color:rgb(51, 51, 51);">调整学习率</font>**<font style="color:rgb(51, 51, 51);">：按缩放规则提升学习率可保持收敛速度。</font>

**<font style="color:rgb(51, 51, 51);">2. 学习率预热（Warmup）</font>**

+ **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：大 batch size + 高初始学习率 → 训练初期不稳定。</font>
+ **<font style="color:rgb(51, 51, 51);">解决方案</font>**<font style="color:rgb(51, 51, 51);">：逐步提升学习率（如前 5% 的迭代从 0 线性增长到目标值）。</font>

**<font style="color:rgb(51, 51, 51);">3. 泛化性能的 trade-off</font>**

+ **<font style="color:rgb(51, 51, 51);">小 batch size</font>**<font style="color:rgb(51, 51, 51);">：噪声提供隐式正则化，泛化性可能更好（需更多迭代）。</font>
+ **<font style="color:rgb(51, 51, 51);">大 batch size</font>**<font style="color:rgb(51, 51, 51);">：需显式正则化（如权重衰减、Dropout）补偿噪声缺失。</font>

:::color5
**<font style="color:#601BDE;">3.实践调参建议</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">确定基线</font>**<font style="color:rgb(51, 51, 51);">：选择一个合理的 batch size（如 256）和学习率（如 0.1）。</font>
2. **<font style="color:rgb(51, 51, 51);">调整 batch size</font>**<font style="color:rgb(51, 51, 51);">：根据硬件条件扩大或缩小。</font>
3. **<font style="color:rgb(51, 51, 51);">按规则缩放学习率</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Batch size 扩大 4 倍 → 学习率扩大 4 倍（线性）或 2 倍（平方根）。</font>
4. **<font style="color:rgb(51, 51, 51);">微调学习率</font>**<font style="color:rgb(51, 51, 51);">：通过训练曲线（loss/accuracy）进一步优化。</font>
5. <font style="color:rgb(51, 51, 51);">特殊场景处理</font>
    - **<font style="color:rgb(51, 51, 51);">分布式训练</font>**<font style="color:rgb(51, 51, 51);">：总 batch size = 单卡 batch size × 卡数，学习率需同步缩放。</font>
    - **<font style="color:rgb(51, 51, 51);">梯度累积（Gradient Accumulation）</font>**<font style="color:rgb(51, 51, 51);">：等效增大 batch size，学习率需按累积步数缩放。</font>
    - **<font style="color:rgb(51, 51, 51);">自适应优化器（Adam等）</font>**<font style="color:rgb(51, 51, 51);">：对学习率敏感性较低，但仍需适当调整。</font>

:::color5
**<font style="color:#601BDE;">4.经典论文</font>**

:::

1. **《Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour》**
    - <font style="color:rgb(51, 51, 51);">提出线性缩放规则，在 256 GPU 上用 8192 batch size 成功训练 ImageNet。</font>
    - <font style="color:rgb(51, 51, 51);">需配合学习率预热和动量修正（momentum correction）。</font>
2. **《Revisiting Small Batch Training for Deep Neural Networks》**
    - <font style="color:rgb(51, 51, 51);">小 batch size（如 32-256）在相同计算量下泛化性能更优。</font>
    - <font style="color:rgb(51, 51, 51);">大 batch size 需延长训练时间（更多 epoch）以弥补更新次数的减少。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
from torch.optim import SGD

base_batch_size = 256
base_lr = 0.1

# 当前 batch size（假设扩大4倍）
current_batch_size = 1024
scale_factor = current_batch_size / base_batch_size

# 线性缩放学习率
adjusted_lr = base_lr * scale_factor  # 0.1 * 4 = 0.4

# 或平方根缩放
adjusted_lr_sqrt = base_lr * (scale_factor ** 0.5)  # 0.1 * 2 = 0.2

# 创建优化器
model = torch.nn.Linear(10, 2)
optimizer = SGD(model.parameters(), lr=adjusted_lr)

```





# scheduler
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">学习率调度器（Learning Rate Scheduler）：根据调整策略可分为：</font>

1. **<font style="color:rgb(51, 51, 51);">固定策略调度</font>**<font style="color:rgb(51, 51, 51);">：基于预定义规则调整（如步长衰减、余弦退火）。</font>
2. **<font style="color:rgb(51, 51, 51);">自适应调度</font>**<font style="color:rgb(51, 51, 51);">：根据训练动态调整（如监控验证损失）。</font>

:::

## <font style="color:rgb(51, 51, 51);">StepLR（步长衰减）</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

<font style="color:rgb(51, 51, 51);">每隔固定步数（</font>`<font style="color:rgb(51, 51, 51);">step_size</font>`<font style="color:rgb(51, 51, 51);">），将学习率乘以衰减因子</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">gamma</font>`<font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**

<font style="color:rgb(51, 51, 51);">初始学习率 l</font><sub><font style="color:rgb(51, 51, 51);">r0</font></sub><font style="color:rgb(51, 51, 51);">，更新公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740481472803-adb84e9a-8cf8-429c-8d7c-39ffbcdf09ae.png)

<font style="color:rgb(51, 51, 51);">t：当前 epoch 或 iteration。</font>

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ <font style="color:rgb(51, 51, 51);">优点：简单直观，计算高效。</font>
+ <font style="color:rgb(51, 51, 51);">缺点：学习率突变可能影响模型收敛。</font>

**<font style="color:rgb(51, 51, 51);">应用场景</font>**

<font style="color:rgb(51, 51, 51);">简单任务（如分类模型）的默认选择。</font>

**<font style="color:rgb(51, 51, 51);">改进方法</font>**

<font style="color:rgb(51, 51, 51);">结合 </font>`<font style="color:rgb(51, 51, 51);">Warmup</font>`<font style="color:rgb(51, 51, 51);"> 阶段避免初始震荡。</font>

```python
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR

optimizer = optim.SGD(model.parameters(), lr=0.1)
scheduler = StepLR(optimizer, step_size=30, gamma=0.1)  # 每30 epoch衰减为0.1倍

for epoch in range(100):
    train(...)
    scheduler.step()  # 更新学习率

```



## <font style="color:rgb(51, 51, 51);">CosineAnnealingLR（余弦退火）</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

+ <font style="color:rgb(51, 51, 51);">学习率按余弦函数从初始值 l</font><sub><font style="color:rgb(51, 51, 51);">r0</font></sub><font style="color:rgb(51, 51, 51);"> 平滑衰减到最小值 η</font><sub><font style="color:rgb(51, 51, 51);">min</font></sub><font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**

<font style="color:rgb(51, 51, 51);">周期 </font><font style="color:rgb(51, 51, 51);">T</font><font style="color:rgb(51, 51, 51);">，当前步数 </font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740481533226-712dbf5c-4b8e-4531-826d-9978711812c0.png)

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：平滑调整，避免剧烈波动。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：需手动设置周期 T</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">应用场景</font>**

<font style="color:rgb(51, 51, 51);">图像分类、目标检测等复杂任务。</font>

**<font style="color:rgb(51, 51, 51);">改进方法</font>**

+ **<font style="color:rgb(51, 51, 51);">CosineAnnealingWarmRestarts</font>**<font style="color:rgb(51, 51, 51);">：周期性重启以逃离局部最优。</font>

```python
from torch.optim.lr_scheduler import CosineAnnealingLR

scheduler = CosineAnnealingLR(optimizer, T_max=50, eta_min=1e-6)  # 周期50 epoch，最小学习率1e-6

```



## <font style="color:rgb(51, 51, 51);">ExponentialLR（指数衰减）</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

+ <font style="color:rgb(51, 51, 51);">每个 epoch 将学习率按指数函数连续衰减。</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**

<font style="color:rgb(51, 51, 51);">更新公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740481601210-ec98558d-157f-43d2-b589-baea9d9b2831.png)

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：连续衰减，适合精细调整。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：可能过早收敛到次优点。</font>

**<font style="color:rgb(51, 51, 51);">应用场景</font>**

+ <font style="color:rgb(51, 51, 51);">需要缓慢调整学习率的任务（如语言模型）。</font>

**<font style="color:rgb(51, 51, 51);">改进方法</font>**

+ <font style="color:rgb(51, 51, 51);">结合早停（Early Stopping）防止过拟合。</font>

```python
from torch.optim.lr_scheduler import ExponentialLR

scheduler = ExponentialLR(optimizer, gamma=0.95)  # 每epoch衰减为0.95倍

```



## <font style="color:rgb(51, 51, 51);">ReduceLROnPlateau（动态衰减）</font>
**<font style="color:rgb(51, 51, 51);">原理</font>**

+ <font style="color:rgb(51, 51, 51);">监控验证损失，若损失不再下降，则衰减学习率。</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**

+ <font style="color:rgb(51, 51, 51);">计算验证损失 Lval</font>_<font style="color:rgb(51, 51, 51);">L</font>_<font style="color:rgb(51, 51, 51);">val。</font>
+ <font style="color:rgb(51, 51, 51);">若 Lval</font>_<font style="color:rgb(51, 51, 51);">L</font>_<font style="color:rgb(51, 51, 51);">val 在 </font>`<font style="color:rgb(51, 51, 51);">patience</font>`<font style="color:rgb(51, 51, 51);"> 个 epoch 内未下降，则更新学习率：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740481696827-301b77d8-dc34-48b4-9719-12bb6bc247ce.png)

**<font style="color:rgb(51, 51, 51);">优缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：自适应调整，避免手动调参。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：依赖验证集质量，可能延迟响应。</font>

**<font style="color:rgb(51, 51, 51);">应用场景</font>**

+ <font style="color:rgb(51, 51, 51);">训练集和验证集分布一致的任务（如分割、检测）。</font>

**<font style="color:rgb(51, 51, 51);">改进方法</font>**

+ <font style="color:rgb(51, 51, 51);">动态调整 </font>`<font style="color:rgb(51, 51, 51);">patience</font>`<font style="color:rgb(51, 51, 51);"> 和 </font>`<font style="color:rgb(51, 51, 51);">gamma</font>`<font style="color:rgb(51, 51, 51);">（如根据训练阶段缩短 </font>`<font style="color:rgb(51, 51, 51);">patience</font>`<font style="color:rgb(51, 51, 51);">）。</font>

```python
from torch.optim.lr_scheduler import ReduceLROnPlateau

scheduler = ReduceLROnPlateau(
    optimizer, mode='min', factor=0.1, patience=10, verbose=True
)

for epoch in range(100):
    train_loss = train(...)
    val_loss = validate(...)
    scheduler.step(val_loss)  # 根据验证损失更新学习率

```



# Batchsize
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">单次前向/反向传播的样本数，影响训练速度和泛化能力。</font>

:::

:::color5
**<font style="color:#601BDE;">1.对训练的影响</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">大批量</font>**<font style="color:rgb(51, 51, 51);">：提高计算效率，但可能降低泛化性能（需调整学习率）。</font>
+ **<font style="color:rgb(51, 51, 51);">小批量</font>**<font style="color:rgb(51, 51, 51);">：噪声更多，可能提升泛化，但训练速度慢。</font>

:::color5
**<font style="color:#601BDE;">2.推荐设置</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">硬件限制</font>**<font style="color:rgb(51, 51, 51);">：尽可能接近GPU/TPU内存上限。</font>
+ **<font style="color:rgb(51, 51, 51);">学习率联动</font>**<font style="color:rgb(51, 51, 51);">：增大批量时按</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">sqrt(batch_size)</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">比例增大学习率（如从</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">1e-4</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">到</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">3e-4</font>`<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">梯度累积</font>**<font style="color:rgb(51, 51, 51);">：通过多步小批量模拟大批量（如每4步累积后更新参数）。</font>

<font style="color:rgb(51, 51, 51);"></font>

# <font style="color:rgb(51, 51, 51);">训练步数/周期数（Training Steps/Epochs）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">决定模型训练的总迭代次数。</font>

:::

:::color5
**<font style="color:#601BDE;">1.对训练的影响</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">过少</font>**<font style="color:rgb(51, 51, 51);">：欠拟合。</font>
+ **<font style="color:rgb(51, 51, 51);">过多</font>**<font style="color:rgb(51, 51, 51);">：过拟合，计算资源浪费。</font>

:::color5
**<font style="color:#601BDE;">2.推荐设置</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">预训练</font>**<font style="color:rgb(51, 51, 51);">：通常需数万到百万步（如GPT-3训练300B tokens）。</font>
+ **<font style="color:rgb(51, 51, 51);">微调</font>**<font style="color:rgb(51, 51, 51);">：根据数据量调整，使用早停（Early Stopping）监控验证集损失。</font>



# top_K
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在生成每个词时，模型仅保留概率最高的前</font>`<font style="color:rgb(51, 51, 51);">k</font>`<font style="color:rgb(51, 51, 51);">个词作为候选，并从中随机采样。</font>

**<font style="color:#ED740C;">top_k越小，相关性越高，多样性越低。</font>**

:::

:::color5
**<font style="color:#601BDE;">1.作用</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">控制多样性</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">k</font>`<font style="color:rgb(51, 51, 51);">较小时（如</font>`<font style="color:rgb(51, 51, 51);">k=10</font>`<font style="color:rgb(51, 51, 51);">），候选词范围窄，生成结果更保守；</font>`<font style="color:rgb(51, 51, 51);">k</font>`<font style="color:rgb(51, 51, 51);">较大时（如</font>`<font style="color:rgb(51, 51, 51);">k=100</font>`<font style="color:rgb(51, 51, 51);">），多样性增加，但可能包含低质量词。</font>
+ **<font style="color:rgb(51, 51, 51);">避免低概率词</font>**<font style="color:rgb(51, 51, 51);">：排除长尾分布中的无关词，</font>**<font style="color:#74B602;">提升生成相关性</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">2.示例</font>**

:::

+ <font style="color:rgb(51, 51, 51);">若生成“天空是___”，模型预测候选词为“蓝色”（概率0.6）、“灰色”（0.3）、“晴朗”（0.1）。当</font>`<font style="color:rgb(51, 51, 51);">k=2</font>`<font style="color:rgb(51, 51, 51);">时，仅从“蓝色”和“灰色”中采样。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

**<font style="color:rgb(51, 51, 51);">适用场景</font>**<font style="color:rgb(51, 51, 51);">：需要平衡生成质量与多样性的任务，如对话生成。</font>

# top_P
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">从累积概率超过阈值</font>`<font style="color:rgb(51, 51, 51);">p</font>`<font style="color:rgb(51, 51, 51);">的最小候选词集合中采样。例如，</font>`<font style="color:rgb(51, 51, 51);">p=0.9</font>`<font style="color:rgb(51, 51, 51);">时，按概率从高到低累加，直到总和≥0.9，仅从这些词中选取。</font>

**<font style="color:#ED740C;">top_p越小，相关性越高，多样性越低。</font>**

:::

**top_p**：<font style="color:rgb(51, 51, 51);">推荐 0.9~0.95。</font>

:::color5
**<font style="color:#601BDE;">1.作用</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态调整候选词数量</font>**<font style="color:rgb(51, 51, 51);">：根据上下文置信度自适应选择。若模型对某些词高度确定（如累积概率迅速达到</font>`<font style="color:rgb(51, 51, 51);">p</font>`<font style="color:rgb(51, 51, 51);">），则候选词少；若不确定（概率分散），候选词多。</font>
+ **<font style="color:rgb(51, 51, 51);">灵活性与稳定性</font>**<font style="color:rgb(51, 51, 51);">：相比</font>`<font style="color:rgb(51, 51, 51);">top_k</font>`<font style="color:rgb(51, 51, 51);">，更适应不同概率分布的场景。</font>

:::color5
**<font style="color:#601BDE;">2.示例</font>**

:::

+ <font style="color:rgb(51, 51, 51);">若预测概率分布为[0.5, 0.3, 0.1, 0.05, ...]，当</font>`<font style="color:rgb(51, 51, 51);">p=0.8</font>`<font style="color:rgb(51, 51, 51);">时，仅选择前两个词（累积0.8）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

**<font style="color:rgb(51, 51, 51);">适用场景</font>**<font style="color:rgb(51, 51, 51);">：开放域任务（如故事生成），需动态</font>**<font style="color:#74B602;">调整生成多样性</font>**<font style="color:rgb(51, 51, 51);">。</font>

# temperature
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">调整softmax前的logits分布形状，公式为：</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741168011107-41223aab-362d-4abb-b527-4f063be85721.png)

**<font style="color:rgb(51, 51, 51);">t：</font>**<font style="color:rgb(51, 51, 51);">通常取 0.7~1.0（>1.0增加多样性，<0.7更确定）。</font>

:::color5
**<font style="color:#601BDE;">1.作用</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">高温度（T > 1）</font>**<font style="color:rgb(51, 51, 51);">：平滑概率分布，低概率词被提升，</font>**<font style="color:#74B602;">生成结果更多样化、随机性强</font>**<font style="color:rgb(51, 51, 51);">，但可能不连贯。</font>
+ **<font style="color:rgb(51, 51, 51);">低温度（T → 0）</font>**<font style="color:rgb(51, 51, 51);">：尖锐化分布，高概率词主导，</font>**<font style="color:#74B602;">生成结果更确定、保守</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">2.示例</font>**

:::

+ <font style="color:rgb(51, 51, 51);">原始logits为</font>`<font style="color:rgb(51, 51, 51);">[3.0, 2.0, 1.0]</font>`
    - <font style="color:rgb(51, 51, 51);">温度</font>`<font style="color:rgb(51, 51, 51);">T=2</font>`<font style="color:rgb(51, 51, 51);">时概率接近</font>`<font style="color:rgb(51, 51, 51);">[0.56, 0.29, 0.15]</font>`
    - <font style="color:rgb(51, 51, 51);">温度</font>`<font style="color:rgb(51, 51, 51);">T=0.5</font>`<font style="color:rgb(51, 51, 51);">时变为</font>`<font style="color:rgb(51, 51, 51);">[0.82, 0.16, 0.02]</font>`<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">高温度：创意文本生成、探索性任务。</font>
+ <font style="color:rgb(51, 51, 51);">低温度：事实性问答、代码生成等需准确性的任务。</font>

# <font style="color:rgb(51, 51, 51);">top_k, top_p, temperature组合</font>
<font style="color:rgb(51, 51, 51);">通过合理配置这些参数，可以显著优化模型生成结果的质量与多样性。</font>

**<font style="color:rgb(51, 51, 51);">对比</font>**

| **参数** | **调控方式** | **优点** | **缺点** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">Top-k</font>** | <font style="color:rgb(51, 51, 51);">固定候选词数量</font> | <font style="color:rgb(51, 51, 51);">简单直观，避免低概率词</font> | <font style="color:rgb(51, 51, 51);">固定k可能不适合所有上下文场景</font> |
| **<font style="color:rgb(51, 51, 51);">Top-p</font>** | <font style="color:rgb(51, 51, 51);">动态调整候选词集合</font> | <font style="color:rgb(51, 51, 51);">自适应概率分布，灵活性高</font> | <font style="color:rgb(51, 51, 51);">计算略复杂，需排序和累加概率</font> |
| **<font style="color:rgb(51, 51, 51);">Temperature</font>** | <font style="color:rgb(51, 51, 51);">调整概率分布形状</font> | <font style="color:rgb(51, 51, 51);">精细控制生成随机性</font> | <font style="color:rgb(51, 51, 51);">需与其他参数配合，单独使用可能不稳定</font> |


**参数建议：**

1. **<font style="color:rgb(51, 51, 51);">温度 τ</font>**_**<font style="color:rgb(51, 51, 51);"></font>**_<font style="color:rgb(51, 51, 51);">：通常取 0.7~1.0（>1.0增加多样性，<0.7更确定）。</font>
2. **<font style="color:rgb(51, 51, 51);">Top-P</font>**<font style="color:rgb(51, 51, 51);">：推荐 0.9~0.95。</font>
3. **<font style="color:rgb(51, 51, 51);">束宽 k</font>**_**<font style="color:rgb(51, 51, 51);"></font>**_<font style="color:rgb(51, 51, 51);">：机器翻译常用 4~8，文本生成可能更低（2~4）。</font>

**<font style="color:rgb(51, 51, 51);">典型组合</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">高多样性</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">temperature=0.8</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">+</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">top_p=0.9</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">高确定性</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">temperature=0.2</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">+</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">top_k=50</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">平衡模式</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">temperature=0.5</font>`<font style="color:rgb(51, 51, 51);"> + </font>`<font style="color:rgb(51, 51, 51);">top_p=0.8</font>`<font style="color:rgb(51, 51, 51);">。</font>

**<font style="color:rgb(51, 51, 51);">调整建议</font>**

1. **<font style="color:rgb(51, 51, 51);">任务类型</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">创意生成：高</font>`<font style="color:rgb(51, 51, 51);">temperature</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">+</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">top_p</font>`<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">事实性输出：低</font>`<font style="color:rgb(51, 51, 51);">temperature</font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">+</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">top_k</font>`<font style="color:rgb(51, 51, 51);">。</font>
2. **<font style="color:rgb(51, 51, 51);">逐步实验</font>**<font style="color:rgb(51, 51, 51);">：从默认值（如</font>`<font style="color:rgb(51, 51, 51);">temperature=1</font>`<font style="color:rgb(51, 51, 51);">,</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">top_p=0.9</font>`<font style="color:rgb(51, 51, 51);">）开始，逐步调整并评估生成质量。</font>
3. **<font style="color:rgb(51, 51, 51);">避免极端值</font>**<font style="color:rgb(51, 51, 51);">：如</font>`<font style="color:rgb(51, 51, 51);">temperature=0</font>`<font style="color:rgb(51, 51, 51);">可能导致重复，</font>`<font style="color:rgb(51, 51, 51);">top_k=1</font>`<font style="color:rgb(51, 51, 51);">则退化为贪心搜索。</font>

