# 因果推理算法

<!-- source: yuque://zhongxian-iiot9/hlyypb/tkf5bykb7op2nap8 -->

# 因果推理算法
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：区分变量间的因果关系（X→Y）而非单纯相关性，解决反事实问题（"如果X改变，Y会如何变化？"）</font>

**<font style="color:rgb(51, 51, 51);">核心概念</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">因果图（DAG）</font>**<font style="color:rgb(51, 51, 51);">：可视化变量间的因果关系和混淆变量</font>
2. **<font style="color:rgb(51, 51, 51);">干预（do-operator）</font>**<font style="color:rgb(51, 51, 51);">：do(X=x)表示强制设定X的值</font>
3. **<font style="color:rgb(51, 51, 51);">潜在结果框架</font>**<font style="color:rgb(51, 51, 51);">：Y(x)表示X=x时的潜在结果</font>
4. **<font style="color:rgb(51, 51, 51);">混淆变量</font>**<font style="color:rgb(51, 51, 51);">：同时影响X和Y的变量（需控制）</font>

:::

**<font style="color:rgb(51, 51, 51);">关键公式</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">平均处理效应（ATE）：ATE = E[Y(1) - Y(0)]</font>
+ <font style="color:rgb(51, 51, 51);">反事实预测：Ŷ(x) = f(x, Z) 其中Z为混淆变量</font>

:::color5
**<font style="color:#601BDE;">1.主流算法及计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 双重机器学习（Double Machine Learning, DML）</font>**

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">通过正交化处理消除混淆变量影响</font>
+ <font style="color:rgb(51, 51, 51);">两阶段回归：Y~T+X 和 T~X，残差拟合</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">拆分数据为K折</font>
2. <font style="color:rgb(51, 51, 51);">每折训练两个模型：</font>
    - <font style="color:rgb(51, 51, 51);">倾向得分模型：g(X) = E[T|X]</font>
    - <font style="color:rgb(51, 51, 51);">结果模型：m(X) = E[Y|X]</font>
3. <font style="color:rgb(51, 51, 51);">计算残差：</font>
    - <font style="color:rgb(51, 51, 51);">Ỹ = Y - m̂(X)</font>
    - <font style="color:rgb(51, 51, 51);">T̃ = T - ĝ(X)</font>
4. <font style="color:rgb(51, 51, 51);">最终效应估计：θ̂ = (T̃^T Ỹ) / (T̃^T T̃)</font>

```python
import torch
import torch.nn as nn

class DML:
    def __init__(self):
        self.t_model = nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 1))
        self.y_model = nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 1))
        
    def fit(self, X, T, Y):
        # 训练倾向得分模型
        t_opt = torch.optim.Adam(self.t_model.parameters())
        for _ in range(100):
            t_pred = self.t_model(X).squeeze()
            loss = nn.MSELoss()(t_pred, T)
            t_opt.zero_grad()
            loss.backward()
            t_opt.step()
        
        # 训练结果模型
        y_opt = torch.optim.Adam(self.y_model.parameters())
        for _ in range(100):
            y_pred = self.y_model(X).squeeze()
            loss = nn.MSELoss()(y_pred, Y)
            y_opt.zero_grad()
            loss.backward()
            y_opt.step()
    
    def estimate_effect(self, X):
        with torch.no_grad():
            T_res = T - self.t_model(X).squeeze()
            Y_res = Y - self.y_model(X).squeeze()
            effect = (T_res.T @ Y_res) / (T_res.T @ T_res)
        return effect.item()

```

**<font style="color:rgb(51, 51, 51);">2. 因果森林（Causal Forest）</font>**

**<font style="color:rgb(51, 51, 51);">原理</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">基于随机森林的异质性处理效应估计</font>
+ <font style="color:rgb(51, 51, 51);">使用倾向得分加权的分裂准则</font>

**<font style="color:rgb(51, 51, 51);">计算步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">样本加权：w_i = T_i/e(X_i) + (1-T_i)/(1-e(X_i))</font>
2. <font style="color:rgb(51, 51, 51);">构建树时最大化：  
</font><font style="color:rgb(51, 51, 51);">Σ_w * (Y_i - μ(X_i)) * (T_i - e(X_i))</font>
3. <font style="color:rgb(51, 51, 51);">通过树间平均得到个体处理效应（ITE）</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **方法** | **优点** | **缺点** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">DML</font> | <font style="color:rgb(51, 51, 51);">高维数据有效，计算效率高</font> | <font style="color:rgb(51, 51, 51);">需要正确指定模型形式</font> |
| <font style="color:rgb(51, 51, 51);">因果森林</font> | <font style="color:rgb(51, 51, 51);">捕捉异质性效应，非参数方法</font> | <font style="color:rgb(51, 51, 51);">计算成本高，解释性差</font> |
| <font style="color:rgb(51, 51, 51);">Meta-Learner</font> | <font style="color:rgb(51, 51, 51);">灵活适配不同基模型</font> | <font style="color:rgb(51, 51, 51);">对数据不平衡敏感</font> |
| <font style="color:rgb(51, 51, 51);">DoWhy</font> | <font style="color:rgb(51, 51, 51);">提供完整因果推断流程</font> | <font style="color:rgb(51, 51, 51);">依赖正确因果图的指定</font> |




# 基于Qwen的因果推理，<font style="color:rgb(51, 51, 51);">评估"限时折扣"对GMV的真实影响</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">项目背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">目标：评估"限时折扣"对GMV的真实影响</font>
+ <font style="color:rgb(51, 51, 51);">挑战：存在选择偏差（价格敏感用户更可能点击优惠）</font>

<font style="color:rgb(51, 51, 51);">通过将因果推理与大语言模型结合，在电商场景中实现了从相关分析到因果决策的跨越，为精细化运营提供了可靠的理论支撑。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740645768495-7c1e18bf-9b47-4ea8-ad16-67386819fe7e.png)

:::color5
**<font style="color:#601BDE;">1.实施步骤</font>**

:::

1. **数据准备**：
    - <font style="color:rgb(51, 51, 51);">特征：用户画像（Qwen生成的embedding）、历史行为、上下文特征</font>
    - <font style="color:rgb(51, 51, 51);">处理变量：是否使用优惠券（T）</font>
    - <font style="color:rgb(51, 51, 51);">结果变量：订单金额（Y）</font>
2. **构建因果图**：

```python
from dowhy import CausalModel
model = CausalModel(
    data=df,
    treatment='use_coupon',
    outcome='order_value',
    graph="digraph {use_coupon->order_value; user_type->use_coupon; user_type->order_value}"
)
```

3. **效应估计**：

```python
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand,
                                 method_name="backdoor.econml.dml.DML",
                                 control_value=0,
                                 treatment_value=1,
                                 target_units="ate")
# Output: ATE = 58.6元 (p<0.05)
```

4. **策略优化**：
    - <font style="color:rgb(51, 51, 51);">对价格弹性高的用户定向发券</font>
    - <font style="color:rgb(51, 51, 51);">动态调整优惠力度：优惠力度 = base_discount + 0.3 * ITE</font>

:::color5
**<font style="color:#601BDE;">2.挑战与解决方案</font>**

:::

1. **未观测混淆变量**：
    - <font style="color:rgb(51, 51, 51);">使用工具变量（如：优惠券发放时间）</font>
    - <font style="color:rgb(51, 51, 51);">敏感性分析：E[Y|T,X] = τT + βX + ε 的ε分布检验</font>
2. **数据稀疏性**：
    - <font style="color:rgb(51, 51, 51);">Qwen数据增强：生成反事实样本</font>

```plain
python


prompt = f"假设用户没有领取优惠券，描述其可能的购物行为：{user_info}"
counterfactual = qwen.generate(prompt)
```

3. **实时性要求**：
    - <font style="color:rgb(51, 51, 51);">部署方案：</font>

```plain
用户请求 → Qwen实时特征提取 → 因果模型计算ITE → 策略引擎 → 返回优惠力度
```

:::color5
**<font style="color:#601BDE;">3.最佳实践建议</font>**

:::

1. **特征工程**：
    - <font style="color:rgb(51, 51, 51);">使用Qwen分析用户评论："价格合理" → 价格敏感度得分</font>
    - <font style="color:rgb(51, 51, 51);">提取会话中的因果表述："因为打折才购买" → 打标为confounder</font>
2. **模型监控**：
    - <font style="color:rgb(51, 51, 51);">定期检测SUTVA（稳定单元处理值假设）</font>
    - <font style="color:rgb(51, 51, 51);">计算协变量平衡：|E[X|T=1] - E[X|T=0]| < 0.1σ</font>
3. **伦理考量**：
    - <font style="color:rgb(51, 51, 51);">避免价格歧视：设置ITE应用上限</font>
    - <font style="color:rgb(51, 51, 51);">提供因果解释：用Qwen生成个性化说明</font>

```plain
"我们推荐此优惠，因为类似用户使用后购买概率提升62%"
```

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **混淆变量处理**：
    - <font style="color:rgb(51, 51, 51);">使用Qwen生成用户心理特征（如价格敏感度）</font>
    - <font style="color:rgb(51, 51, 51);">构建动态因果图：G = (V,E), V ∈ {Qwen_emb, T, Y}</font>
2. **模型优化**：

```python
class QwenDML(nn.Module):
    def __init__(self, qwen):
        super().__init__()
        self.qwen = qwen.freeze()
        self.t_head = nn.Linear(4096, 1)
        self.y_head = nn.Linear(4096, 1)

    def forward(self, text):
        emb = self.qwen.encode(text)
        t_pred = self.t_head(emb)
        y_pred = self.y_head(emb)
        return t_pred, y_pred
```

3. **评估验证**：
    - <font style="color:rgb(51, 51, 51);">通过A/A测试验证估计无偏性</font>
    - <font style="color:rgb(51, 51, 51);">计算ERU（Empirical Coverage Rate）：P(真实Y ∈ 预测区间) ≥ 95%</font>



