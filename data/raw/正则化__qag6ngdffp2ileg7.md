# 正则化

<!-- source: yuque://zhongxian-iiot9/hlyypb/qag6ngdffp2ileg7 -->

# 正则化
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">正则化的核心目标是 </font>**<font style="color:rgb(51, 51, 51);">防止模型过拟合</font>**<font style="color:rgb(51, 51, 51);">，通过约束模型复杂度或添加噪声提升泛化能力。主要分为以下类别：</font>

+ **<font style="color:rgb(51, 51, 51);">参数惩罚</font>**<font style="color:rgb(51, 51, 51);">：L1/L2正则化</font>
+ **<font style="color:rgb(51, 51, 51);">结构约束</font>**<font style="color:rgb(51, 51, 51);">：Dropout、DropConnect</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：输入扰动</font>
+ **<font style="color:rgb(51, 51, 51);">早停法</font>**<font style="color:rgb(51, 51, 51);">：基于验证集的训练控制</font>
+ **<font style="color:rgb(51, 51, 51);">标准化技术</font>**<font style="color:rgb(51, 51, 51);">：BatchNorm、LayerNorm</font>

:::

| **方法** | **核心思想** | **适用场景** | **计算开销** |
| --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">L1/L2正则化</font> | <font style="color:rgb(51, 51, 51);">参数惩罚</font> | <font style="color:rgb(51, 51, 51);">通用任务</font> | <font style="color:rgb(51, 51, 51);">低</font> |
| <font style="color:rgb(51, 51, 51);">Dropout</font> | <font style="color:rgb(51, 51, 51);">随机丢弃神经元</font> | <font style="color:rgb(51, 51, 51);">全连接层/CNN</font> | <font style="color:rgb(51, 51, 51);">中</font> |
| <font style="color:rgb(51, 51, 51);">数据增强</font> | <font style="color:rgb(51, 51, 51);">输入扰动</font> | <font style="color:rgb(51, 51, 51);">图像/文本数据</font> | <font style="color:rgb(51, 51, 51);">低</font> |
| <font style="color:rgb(51, 51, 51);">早停法</font> | <font style="color:rgb(51, 51, 51);">动态终止训练</font> | <font style="color:rgb(51, 51, 51);">所有模型</font> | <font style="color:rgb(51, 51, 51);">低</font> |
| <font style="color:rgb(51, 51, 51);">BatchNorm</font> | <font style="color:rgb(51, 51, 51);">标准化激活值</font> | <font style="color:rgb(51, 51, 51);">深层网络</font> | <font style="color:rgb(51, 51, 51);">中</font> |
| <font style="color:rgb(51, 51, 51);">标签平滑</font> | <font style="color:rgb(51, 51, 51);">软化标签</font> | <font style="color:rgb(51, 51, 51);">分类任务</font> | <font style="color:rgb(51, 51, 51);">低</font> |
| <font style="color:rgb(51, 51, 51);">权重约束</font> | <font style="color:rgb(51, 51, 51);">显式限制权重范围</font> | <font style="color:rgb(51, 51, 51);">RNN/对抗训练</font> | <font style="color:rgb(51, 51, 51);">低</font> |
| <font style="color:rgb(51, 51, 51);">随机深度</font> | <font style="color:rgb(51, 51, 51);">随机跳过网络层</font> | <font style="color:rgb(51, 51, 51);">超深残差网络</font> | <font style="color:rgb(51, 51, 51);">中</font> |




# L1正则
:::color3
**简介**

+ **<font style="color:rgb(51, 51, 51);">L1正则化（Lasso）</font>**<font style="color:rgb(51, 51, 51);">：向损失函数添加</font>**<font style="color:#ED740C;">权重绝对值之和</font>**<font style="color:rgb(51, 51, 51);">，推动稀疏权重，实现特征选择，适合高维数据分析</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">向损失函数中添加权重的</font>**<font style="color:rgb(51, 51, 51);">绝对值之和</font>**<font style="color:rgb(51, 51, 51);">作为惩罚项。其中，</font><font style="color:rgb(51, 51, 51);">λ</font><font style="color:rgb(51, 51, 51);">是正则化强度系数，</font><font style="color:rgb(51, 51, 51);">wi</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">是模型参数。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740469181313-c5827b38-72a3-4e12-84cc-038131228cc9.png)

1. **稀疏解特性**  
L1正则化的几何特性导致优化过程中倾向于将部分权重压缩为零。例如，在二维空间中，损失函数的等高线与L1菱形约束的切点更容易出现在坐标轴上（即某些权重为零）。  
**数学解释**：  
L1正则项在**<font style="color:#74B602;">零点不可导</font>**，优化时（如梯度下降）会推动**<font style="color:#74B602;">不重要特征的权重直接归零</font>**。

:::color5
**<font style="color:#601BDE;">2.为什么L2产生稀疏性</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数学证明（以线性回归为例）</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">假设损失函数为均方误差（MSE），加入L1正则化后优化目标为：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740469574448-46cb3718-ba11-4506-9418-0300483a8a82.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">次梯度条件要求：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740469582783-a3cb6796-0525-493f-a8f4-5ab2a7553a9b.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">当某一维度特征 xj对目标  的贡献不足时，λ会迫使 wj=0。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **** | **L1正则化** | **L2正则化** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">优点</font>** | <font style="color:rgb(51, 51, 51);">1. 特征选择（稀疏解）   </font><font style="color:rgb(51, 51, 51);">2. 可解释性高</font> | <font style="color:rgb(51, 51, 51);">1. 稳定优化（处处可导）   </font><font style="color:rgb(51, 51, 51);">2. 处理共线性</font> |
| **<font style="color:rgb(51, 51, 51);">缺点</font>** | <font style="color:rgb(51, 51, 51);">1. 非唯一解（特征高度相关时不稳定）   </font><font style="color:rgb(51, 51, 51);">2. 计算复杂</font> | <font style="color:rgb(51, 51, 51);">1. 无法特征选择   </font><font style="color:rgb(51, 51, 51);">2. 对异常值敏感</font> |


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">高维数据（特征数 > 样本数）</font>
+ <font style="color:rgb(51, 51, 51);">需要特征选择的场景（如基因数据、文本分类）</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">弹性网络（Elastic Net）</font>**<font style="color:rgb(51, 51, 51);">：结合L1+L2正则化。</font>
+ **<font style="color:rgb(51, 51, 51);">自适应L2</font>**<font style="color:rgb(51, 51, 51);">：不同层使用不同的 λ</font>_<font style="color:rgb(51, 51, 51);">λ</font>_<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
# L2正则化（直接通过优化器实现）
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

# L1正则化（手动添加）
l1_lambda = 0.001
loss = criterion(outputs, labels)
l1_norm = sum(p.abs().sum() for p in model.parameters())
loss += l1_lambda * l1_norm

```



# L2正则
:::color3
**简介**

<font style="color:rgb(51, 51, 51);">L2正则化（Ridge）：添加</font><font style="color:#ED740C;">权重平方和，</font>保证**<font style="color:rgb(51, 51, 51);">权重衰减与平滑性，</font>**<font style="color:rgb(51, 51, 51);">提高模型泛化性</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">向损失函数中添加权重的</font>**<font style="color:rgb(51, 51, 51);">平方和</font>**<font style="color:rgb(51, 51, 51);">作为惩罚项：</font>  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740469220447-9b69a184-5c62-4799-8700-3696a3ec5fd7.png)  
<font style="color:rgb(51, 51, 51);"> 注意：</font><font style="color:rgb(51, 51, 51);">λ22</font>_<font style="color:rgb(51, 51, 51);">λ</font>_<font style="color:rgb(51, 51, 51);"> 的系数是为了求导后形式简化。</font>

1. **权重收缩**  
L2正则化**<font style="color:#74B602;">对权重施加均等的惩罚，使权重趋向于较小的值但不为零</font>**。例如，损失函数的等高线与L2圆形约束的切点通常不在坐标轴上。  
**数学解释**：  
L2正则项的导数连续，梯度下降时权重按比例缩小：![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740469311936-528e98f9-66b6-4474-ae63-caf037200da4.png)。

:::color5
**<font style="color:#601BDE;">2.为什么能防止过拟合？</font>**

:::

1. **奥卡姆剃刀原理**  
正则化通过惩罚复杂模型（大权重），迫使模型选择更简单的假设，提升泛化能力。
2. **偏差-方差权衡**
    - <font style="color:rgb(51, 51, 51);">L1：通过特征选择减少方差（丢弃不重要特征）</font>
    - <font style="color:rgb(51, 51, 51);">L2：通过权重衰减限制模型复杂度，降低方差</font>
3. **优化视角**
    - <font style="color:rgb(51, 51, 51);">L1的稀疏性减少模型参数数量，降低过拟合风险。</font>
    - <font style="color:rgb(51, 51, 51);">L2的权重衰减抑制参数敏感度，缓解对噪声的过拟合。</font>

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

| **** | **L1正则化** | **L2正则化** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">优点</font>** | <font style="color:rgb(51, 51, 51);">1. 特征选择（稀疏解）   </font><font style="color:rgb(51, 51, 51);">2. 可解释性高</font> | <font style="color:rgb(51, 51, 51);">1. 稳定优化（处处可导）   </font><font style="color:rgb(51, 51, 51);">2. 处理共线性</font> |
| **<font style="color:rgb(51, 51, 51);">缺点</font>** | <font style="color:rgb(51, 51, 51);">1. 非唯一解（特征高度相关时不稳定）   </font><font style="color:rgb(51, 51, 51);">2. 计算复杂</font> | <font style="color:rgb(51, 51, 51);">1. 无法特征选择   </font><font style="color:rgb(51, 51, 51);">2. 对异常值敏感</font> |


:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">防止过拟合（通用场景）</font>
+ <font style="color:rgb(51, 51, 51);">处理特征共线性（如线性回归）</font>

:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">弹性网络（Elastic Net）</font>**<font style="color:rgb(51, 51, 51);">：结合L1+L2正则化。</font>
+ **<font style="color:rgb(51, 51, 51);">自适应L2</font>**<font style="color:rgb(51, 51, 51);">：不同层使用不同的 λ</font>_<font style="color:rgb(51, 51, 51);">λ</font>_<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
# L2正则化（直接通过优化器实现）
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

# L1正则化（手动添加）
l1_lambda = 0.001
loss = criterion(outputs, labels)
l1_norm = sum(p.abs().sum() for p in model.parameters())
loss += l1_lambda * l1_norm

```



# Dropout
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">在训练时以概率 p</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">随机丢弃神经元，迫使网络不依赖单一特征。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">前向传播时，按概率 p将神经元输出置零。</font>
2. <font style="color:rgb(51, 51, 51);">测试时，所有神经元激活，但权重乘以 1−p（缩放补偿）。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">简单高效，广泛适用</font> | <font style="color:rgb(51, 51, 51);">增加训练时间</font> |
| <font style="color:rgb(51, 51, 51);">破坏共适应，增强鲁棒性</font> | <font style="color:rgb(51, 51, 51);">可能丢失重要信息</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">全连接层（CNN/RNN中均可使用）</font>
+ <font style="color:rgb(51, 51, 51);">过拟合风险高的复杂模型</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">Spatial Dropout</font>**<font style="color:rgb(51, 51, 51);">：在CNN中按通道丢弃整个特征图。</font>
+ **<font style="color:rgb(51, 51, 51);">DropConnect</font>**<font style="color:rgb(51, 51, 51);">：随机断开权重连接而非神经元。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
# 在模型定义中添加Dropout层
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)

```



# 数据增强
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">通过对训练数据施加随机变换（旋转、裁剪等），增加数据多样性。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">定义数据变换组合（如随机裁剪+翻转+颜色抖动）。</font>
2. <font style="color:rgb(51, 51, 51);">在数据加载时实时应用变换。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">不增加计算负担（预处理阶段）</font> | <font style="color:rgb(51, 51, 51);">对非图像数据效果有限</font> |
| <font style="color:rgb(51, 51, 51);">直接提升数据多样性</font> | <font style="color:rgb(51, 51, 51);">变换策略依赖领域知识</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">图像分类、目标检测</font>
+ <font style="color:rgb(51, 51, 51);">小样本学习任务</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">AutoAugment</font>**<font style="color:rgb(51, 51, 51);">：自动搜索最优增强策略。</font>
+ **<font style="color:rgb(51, 51, 51);">Mixup</font>**<font style="color:rgb(51, 51, 51);">：线性插值生成新样本。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
# 图像数据增强
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor()
])

```





# Early Stop
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">监控验证集损失，当连续多轮未改善时停止训练，防止过拟合。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">每个epoch后计算验证集损失。</font>
2. <font style="color:rgb(51, 51, 51);">若损失在 N</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">个epoch内未下降，终止训练。</font>
3. <font style="color:rgb(51, 51, 51);">恢复最佳模型参数。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">无需修改模型结构</font> | <font style="color:rgb(51, 51, 51);">需要额外验证集</font> |
| <font style="color:rgb(51, 51, 51);">节省计算资源</font> | <font style="color:rgb(51, 51, 51);">可能过早停止（局部最优）</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">所有需要迭代训练的任务</font>
+ <font style="color:rgb(51, 51, 51);">资源受限的模型训练</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">动态阈值</font>**<font style="color:rgb(51, 51, 51);">：根据训练阶段调整停止条件。</font>
+ **<font style="color:rgb(51, 51, 51);">模型检查点</font>**<font style="color:rgb(51, 51, 51);">：保存中间最优模型。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
best_val_loss = float('inf')
patience = 5
trigger_times = 0

for epoch in range(100):
    # 训练步骤...
    # 验证步骤...
    val_loss = validate(model, val_loader)
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        trigger_times = 0
        torch.save(model.state_dict(), 'best_model.pth')
    else:
        trigger_times += 1
        if trigger_times >= patience:
            print("Early stopping!")
            break

```





# BatchNorm
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">对每层输入进行标准化（减均值、除标准差），加速训练并轻微正则化。</font>

<font style="color:rgb(51, 51, 51);">BatchNorm通过对每个特征通道在</font>**<font style="color:#ED740C;">批量维度</font>**<font style="color:rgb(51, 51, 51);">上进行归一化（即对同一通道的不同样本数据做归一化），缓解内部协变量偏移问题。核心思想是</font>**<font style="color:#ED740C;">通过标准化每一层的输入，使得输入分布稳定在零均值和单位方差附近，从而加速模型训练</font>**<font style="color:rgb(51, 51, 51);">。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. <font style="color:rgb(51, 51, 51);">计算当前批次的均值 μ和方差 σ2：对于输入张量 </font><font style="color:rgb(51, 51, 51);">X∈R</font><sup><font style="color:rgb(51, 51, 51);">N×C×H×W</font></sup><font style="color:rgb(51, 51, 51);">（N为batch size，C为通道数）：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740470042065-f8e76a75-271f-4d69-a050-10da05b67a24.png)

2. <font style="color:rgb(51, 51, 51);">标准化：其中 </font><font style="color:rgb(51, 51, 51);">ϵ</font>_<font style="color:rgb(51, 51, 51);">ϵ</font>_<font style="color:rgb(51, 51, 51);"> 是防止除零的小常数。</font>

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
# 在模型定义中添加BN层
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3)
        self.bn1 = nn.BatchNorm2d(64)
        self.fc = nn.Linear(64*28*28, 10)
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        return self.fc(x.view(x.size(0), -1))

```





# 标签平滑
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">LayerNorm对</font>**<font style="color:rgb(51, 51, 51);">单个样本的所有特征</font>**<font style="color:rgb(51, 51, 51);">进行归一化（即对同一样本的不同通道/神经元做归一化），常用于处理变长序列或小批量数据。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">修改标签为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740469823925-5b5a967c-952d-45d5-b785-1c63dbdb5e40.png)

<font style="color:rgb(51, 51, 51);">其中 </font><font style="color:rgb(51, 51, 51);">K</font>_<font style="color:rgb(51, 51, 51);">K</font>_<font style="color:rgb(51, 51, 51);"> 为类别数，</font><font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);"> 为平滑系数（通常0.1）。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">减少过拟合风险</font> | <font style="color:rgb(51, 51, 51);">需要调整平滑系数</font> |
| <font style="color:rgb(51, 51, 51);">提升模型校准性</font> | <font style="color:rgb(51, 51, 51);">可能降低模型置信度</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">分类任务（尤其是类别不平衡时）</font>
+ <font style="color:rgb(51, 51, 51);">对抗训练</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">自适应平滑系数</font>**<font style="color:rgb(51, 51, 51);">：根据训练阶段动态调整 α</font>_<font style="color:rgb(51, 51, 51);">α</font>_<font style="color:rgb(51, 51, 51);">。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
def label_smoothing_loss(pred, target, alpha=0.1, classes=10):
    target = F.one_hot(target, classes).float()
    target = (1 - alpha) * target + alpha / classes
    return F.cross_entropy(pred, target)
```







