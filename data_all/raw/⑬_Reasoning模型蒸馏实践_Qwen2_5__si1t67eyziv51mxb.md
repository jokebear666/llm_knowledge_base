# ⑬ Reasoning模型蒸馏实践：Qwen2.5

<!-- source: yuque://zhongxian-iiot9/hlyypb/si1t67eyziv51mxb -->

# 前言
:::success
**背景**：DeepSeek-R1的爆火让更多开发者注意到模型蒸馏技术——这种让小模型也能"开小灶"习得大模型知识精华的秘诀。今天我们就用Qwen2.5-1.5B小模型（相当于AI界的初中生）来进行实践！<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748573465276-eacedeae-51c8-4bd0-84ce-05a4e09a1396.png)

📝 三步速成法：<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::color1
🔍 什么是模型蒸馏？

就像普通学生跟着学霸学解题思路：

-教师模型 = 学霸本霸（比如DeepSeek-R1）

-学生模型 = 需要进步的Qwen2.5-1.5B

-蒸馏数据 = 学霸的解题笔记

:::

:::color1
**步骤一**

制造"学霸笔记"（构造蒸馏数据）

-让学霸模型处理大量题目

-记录它的解题过程和参考答案

-整理成适合小模型学习的训练集

:::

:::color1
**步骤二**

特训小模型（训练阶段）



-重点模仿学霸的解题思路



:::

:::color1
**步骤三**

考试验收（模型评测）

-准备数学题等测试卷

-对比特训前后的考试成绩

-观察逻辑推理能力的提升效果

:::

跟着这个流程，小模型也能获得学霸的真传！不需要昂贵硬件，用常规显卡就能训练，赶紧试试这个AI界的"开小灶"秘籍吧~



# 构造蒸馏数据
:::color3
**简介：**为了让小模型也有合适的学习资料，我们需要从高质量开源数学数据集，例如AI-MO/NuminaMath-CoT中获取蒸馏数据<font style="color:#D22D8D;"> (by草莓师姐)</font>

**项目地址**：AI-MO/NuminaMath-CoT：

[https://www.modelscope.cn/datasets/AI-MO/NuminaMath-CoT/summary](https://www.modelscope.cn/datasets/AI-MO/NuminaMath-CoT/summary)

:::

:::color5
**<font style="color:#601BDE;">1.构造蒸馏数据</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

下面展示使用ModelScope的在线模型推理服务（[https://www.modelscope.cn/docs/model-service/API-Inference/intro](https://www.modelscope.cn/docs/model-service/API-Inference/intro)），用DeepSeek-R1作为教师模型，通过prompt构造的方式获取一个数学题的解题过程和参考答案。以下是Python代码示例：

```python

from openai import OpenAI
import os
system_prompt = (
        'A conversation between User and Assistant. The user asks a question, and the Assistant solves it. '
        'The assistant first thinks about the reasoning process in the mind and then provides the user '
        'with the answer. The reasoning process and answer are enclosed '
        'within <think> </think> and <answer> </answer> tags, respectively, '
        'i.e., <think> reasoning process here </think> <answer> answer here </answer>.'
)
prompt_template = r'{question}\nPlease reason step by step, and put your final answer within \boxed{{}}.'
question = 'Find all real numbers \( x, y, z \) such that \[ x + y + z = 3, \quad x^2 + y^2 + z^2 = 3, \quad x^3 + y^3 + z^3 = 3 \]'
client = OpenAI(
    api_key=os.getenv("MODELSCOPE_SDK_TOKEN"), # 请替换成您的 ModelScope SDK Token
    base_url="https://api-inference.modelscope.cn/v1/"
)
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1", # ModleScope Model-Id
    messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': prompt_template.format(question=question)
        }
    ],
    stream=True
)
for chunk in response:
    if hasattr(chunk.choices[0].delta, 'reasoning_content'):
        print(chunk.choices[0].delta.reasoning_content, end='', flush=True)
    if hasattr(chunk.choices[0].delta, 'content'):
        print(chunk.choices[0].delta.content, end='', flush=True)
```

输出如下<font style="color:#D22D8D;"> (by草莓师姐)</font>

```python

Okay, so I need to solve this system of equations:
x + y + z = 3,
x² + y² + z² = 3,
x³ + y³ + z³ = 3.
Hmm, let's see. These are symmetric equations, so maybe I can use some symmetric properties or formulas. Let me recall that for symmetric equations, using variables like sums and products might help. Let me denote S = x + y + z, which is given as 3. Then, the sum of squares is given by x² + y² + z² = 3. I also know that the sum of squares can be related to S and the pairwise products. The formula is:
x² + y² + z² = (x + y + z)² - 2(xy + yz + zx).
Plugging in the known values, 3 = (3)² - 2(xy + yz + zx). So, 3 = 9 - 2(xy + yz + zx). Let's solve for the sum of products:
2(xy + yz + zx) = 9 - 3 = 6 ⇒ xy + yz + zx = 3.
Okay, so now I have S = 3, and the sum of products is also 3. Now, moving on to the third equation, which is the sum of cubes: x³ + y³ + z³ = 3. There's a formula for the sum of cubes in terms of S, the sum of products, and the product xyz. The formula is:
x³ + y³ + z³ = (x + y + z)³ - 3(x + y + z)(xy + yz + zx) + 3xyz.
Plugging in the known values:
3 = 3³ - 3*3*3 + 3xyz.
Calculating each term:
3³ is 27,
3*3*3 is 27,
So,
3 = 27 - 27 + 3xyz ⇒ 3 = 0 + 3xyz ⇒ 3xyz = 3 ⇒ xyz = 1.
So now I have S = 3, sum of products = 3, and product = 1. These are the elementary symmetric sums. Therefore, the monic cubic polynomial whose roots are x, y, z is:
t³ - S t² + (xy + yz + zx) t - xyz = 0 ⇒ t³ - 3t² + 3t - 1 = 0.
So, solving this cubic equation should give me all real numbers x, y, z. Let me try to factor this cubic. Maybe it has rational roots? By Rational Root Theorem, possible roots are ±1. Let's test t=1:
1³ - 3*1² + 3*1 -1 = 1 -3 +3 -1 = 0. Yes, t=1 is a root. So, we can factor out (t -1). Let's perform polynomial division or use synthetic division.
Dividing t³ -3t² +3t -1 by (t -1):
Using synthetic division:
1 | 1  -3   3   -1
           1  -2    1
       1  -2    1    0
So, the quadratic factor is t² - 2t +1. Which factors further as (t -1)².
Therefore, the cubic factors as (t -1)³ = 0. So, all three roots are 1. Therefore, the solution is x = y = z =1.
Wait, but let me check if there could be other solutions. Suppose the cubic factors into (t-1)^3, which means that all three variables are 1. Let me verify if this satisfies the original equations.
First equation: 1 +1 +1 =3, yes.
Second: 1² +1² +1² =3, yes.
Third:1³ +1³ +1³=3, yes. So that works.
But wait, maybe there are other real solutions where variables are not all 1? Let's see. Since the cubic equation only has t=1 as a triple root, that's the only solution. Therefore, the only real solution is x=y=z=1.
But let me think again. Suppose that two variables are equal to 1 and the third is different. Let me test that. Suppose x =1, y=1, then z =3 -1 -1=1. So, z=1. So that's still all ones. Alternatively, if one variable is not 1, would that work?
Wait, suppose that x, y, z are all 1, which works. Suppose, for example, x=2, y=0, z=1. Then x+y+z=3. Check the sum of squares: 4 +0 +1=5 ≠3. So that doesn't work. Alternatively, maybe some other combination. But given that the cubic equation only has 1 as a root, multiplicity three, that suggests that all three variables must be 1.
Alternatively, perhaps complex roots, but the problem asks for real numbers. So, since the only real root is 1 with multiplicity three, the only real solution is x=y=z=1. Therefore, the answer is all variables equal to 1.<answer>
The only real solution is \( x = y = z = 1 \). Thus, the numbers are \(\boxed{1}\), \(\boxed{1}\), and \(\boxed{1}\).
Alternatively, since all variables are the same, it can be written as \(\boxed{1}\) for each variable.
**Final Answer**
The real numbers are \(\boxed{1}\), \(\boxed{1}\), and \(\boxed{1}\).
</answer>
```



# 训练模型
:::color3
**简介：**我们已经处理了一批数学题，生成了一个包含4000个样本的蒸馏数据集。每个样本包含题目、解题过程和参考答案。我们将其保存为JSONL格式，方便后续使用，数据集预览：<font style="color:#D22D8D;"> (by草莓师姐)</font>

**项目地址**：[https://www.modelscope.cn/datasets/modelscope/MathR/dataPeview](https://www.modelscope.cn/datasets/modelscope/MathR/dataPeview)

:::

:::color5
**<font style="color:#601BDE;">1.训练模型</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

接下来，我们将使用ms-swift（[https://github.com/modelscope/ms-swift](https://github.com/modelscope/ms-swift)）模型训练框架，用这批数据对Qwen2.5-1.5B模型进行训练。

+ 训练样本示例：

```python

[
  {
    "role": "user",
    "content": "A set of consecutive positive integers beginning with $1$ is written on a blackboard. One number is erased. The average (arithmetic mean) of the remaining numbers is $35\\frac{7}{17}$. What number was erased? \n$\\textbf{(A)}\\ 6\\qquad  \\textbf{(B)}\\ 7 \\qquad  \\textbf{(C)}\\ 8 \\qquad  \\textbf{(D)}\\  9\\qquad  \\textbf{(E)}\\ \\text{cannot be determined}$\nPlease reason step by step, and put your final answer within \boxed{}."
  },
  {
    "role": "assistant",
    "content": "
\nOkay, let's see. I need to figure out which ....... Answer is B.\n\n**Final Answer**\n\\boxed{B}\n\n\n
Given a set of consecutive positive integers starting ...... Average of remaining numbers: \\(\\frac{2408}{68} = \\frac{602}{17} = 35 \\frac{7}{17}\\)\n\nThus, the number erased is \\(\\boxed{B}\\)."
  }
]
```

:::danger
注意：受限于显存，我们使用LoRA技术对Qwen2.5-1.5B进行微调。LoRA是一种高效的模型微调方法，能够在不改变原始模型参数的情况下，通过添加低秩矩阵来实现模型的适应性调整。这样可以大幅降低训练成本和时间。如果有更强的显卡，可以考虑使用更多的训练数据以及全量参数微调。

:::

下面的命令中我们还使用了Swanlab（[https://github.com/SwanHubX/SwanLab](https://github.com/SwanHubX/SwanLab)）进行训练过程的可视化，可以方便的查看训练过程中loss等指标的变化情况，请替换下面的`YOUR_SWANLAB_TOKEN`

```python
!CUDA_VISIBLE_DEVICES=0 \
 swift sft \
    --model Qwen/Qwen2.5-1.5B-Instruct \
    --train_type lora \
    --lora_rank 16 \
    --torch_dtype bfloat16 \
    --dataset 'modelscope/MathR:clean' \
    --split_dataset_ratio 0 \
    --max_length 4096 \
    --num_train_epochs 1 \
    --per_device_train_batch_size 1 \
    --learning_rate 1e-5 \
    --gradient_accumulation_steps 16 \
    --save_steps 100 \
    --save_total_limit 10 \
    --logging_steps 5 \
    --report_to swanlab \
    --swanlab_token YOUR_SWANLAB_TOKEN \
    --swanlab_mode cloud
```

在控制台运行下面的命令，可以与训练后的模型进行对话，了解模型效果：<font style="color:#D22D8D;">(by草莓师姐)</font>

> 注意：把`adapters`参数替换成你训练好的模型路径，`--stream`参数设置为`true`表示使用流式推理，`--infer_backend`参数设置为`pt`表示使用PyTorch作为推理后端，`--temperature`参数设置为0表示不引入随机性，`--max_new_tokens`参数设置为2048表示生成的最大token数。
>

```python
swift infer \
--adapters 'output/Qwen2.5-1.5B-Instruct/v11-20250415-120200/checkpoint-81' \
--stream true \
--infer_backend pt \
--temperature 0 \
--max_new_tokens 2048
```

# 模型性能前后对比
:::color3
**简介：**在训练完成后，我们使用一组新的数学题对模型进行评测。这里我们使用gsm8k数据集（数学题数据集）来进行评测，可以在这里查看数据集<font style="color:#D22D8D;"> (by草莓师姐)</font>

**项目地址**：[https://www.modelscope.cn/datasets/modelscope/gsm8k/dataPeview](https://www.modelscope.cn/datasets/modelscope/gsm8k/dataPeview)

:::

:::color5
**<font style="color:#601BDE;">1.数据查看</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

```python
from evalscope import run_task, TaskConfig
task_config = TaskConfig(
    model="Qwen/Qwen2.5-1.5B-Instruct",  # 原始模型
    datasets=["gsm8k"],  # 数据集名称
    dataset_args={
        "gsm8k": {"few_shot_num": 0},  # few_shot_num: 0表示不使用few-shot
    },
    generation_config={
        "max_new_tokens": 4096,  # 生成的最大token数
        "temperature": 0,  # 生成的温度系数，0表示贪婪搜索
    },
    eval_batch_size=10,  # 评测时的batch size
    limit=100   # 评测数据集的大小，抽取前100条数据进行评测
)
run_task(task_config)
```

结果如下：

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1748572786075-d546721f-6c1f-49e8-a0ec-23d0a739abb8.webp)

为了评测训练之后的模型，需要运行下面的命令将我们训练的lora参数合并回原始模型，得到一个新的模型`Qwen2.5-1.5B-Instruct`，并将其保存到`checkpoint-xxx-merged`目录下。

```python

!swift export \
    --adapters /mnt/data/data/user/maoyunlin.myl/tools/course/distill/output/Qwen2.5-1.5B-Instruct/v11-20250415-120200/checkpoint-81 \
    --merge_lora true
```

```python

# 测试蒸馏训练后的模型
from evalscope import run_task, TaskConfig
# 记得替换下面的model路径
task_config = TaskConfig(
    model="/mnt/data/data/user/maoyunlin.myl/tools/course/distill/output/Qwen2.5-1.5B-Instruct/v11-20250415-120200/checkpoint-81-merged",
    datasets=["gsm8k"],
    dataset_args={
        "gsm8k": {"few_shot_num": 0},
    },
    generation_config={
        "max_new_tokens": 4096,
        "temperature": 0,
    },
    eval_batch_size=10,
    limit=100
)
run_task(task_config)
```

结果如下：<font style="color:#D22D8D;"> (by草莓师姐)</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1748572815763-54c86381-b6b4-4c66-a2d3-9d3605e41ed4.webp)

可视化结果

通过训练结果可以看到模型的回答准确率提升了12%，进步还是很可观的。我们还可以使用可视化工具来进一步分析模型的推理过程，帮助我们更好地理解模型的决策逻辑。

```python
import os
os.environ['GRADIO_ROOT_PATH'] = f"/{os.environ['JUPYTER_NAME']}/proxy/7860"
print(os.environ['GRADIO_ROOT_PATH'])
```

```python
!evalscope app
```

# 总结
:::color3
在这个教程中，我们详细演示了如何利用一个教师模型来蒸馏一个小模型的完整流程。内容涵盖三个关键环节：数据构造、模型训练和模型评测。通过这一方法，您可以高效地训练出属于自己的小模型。希望本教程能帮助您掌握这一技术，并灵活运用于实际项目中！

:::



