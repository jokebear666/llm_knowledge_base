# ⑪ Qwen2-VL：多模态大模型微调实战

<!-- source: yuque://zhongxian-iiot9/hlyypb/aiheinlknsykaun3 -->

:::color3
**简介**：作为在Qwen-VL基础上迭代的最新版本，Qwen2-VL在视觉理解上达到非常先进的性能。**<font style="color:#ECAA04;">不再使用Q-former,而是直接使用MLP进行对齐。</font>**<font style="color:rgba(0, 0, 0, 0.9);">本文我们将简要介绍基于 transformers、peft 等框架，使用 Qwen2-VL-2B-Instruct 模型在COCO2014图像描述 上进行</font>Lora<font style="color:rgba(0, 0, 0, 0.9);">微调训练。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

+ **paper : **[**https://arxiv.org/pdf/2409.12191**](https://arxiv.org/pdf/2409.12191)
+ **<font style="color:rgba(0, 0, 0, 0.9);">训练过程</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>[**Qwen2-VL-finetune**](https://swanlab.cn/@ZeyiLin/Qwen2-VL-finetune/runs/pkgest5xhdn3ukpdy6kv5/chart)
+ **<font style="color:rgba(0, 0, 0, 0.9);">Github：</font>**
    - **<font style="color:rgb(0, 128, 255);">代码仓库（</font>**<u><font style="color:rgb(0, 128, 255);">https://github.com/Zeyi-Lin/LLM-Finetune/tree/main/qwen2_vl</font></u>**<font style="color:rgb(0, 128, 255);">）</font>**<font style="color:rgba(0, 0, 0, 0.9);">、</font>
    - **<font style="color:rgb(0, 128, 255);">self-llm（</font>**<u><font style="color:rgb(0, 128, 255);">https://github.com/datawhalechina/self-llm</font></u>**<font style="color:rgb(0, 128, 255);">）</font>**
+ **<font style="color:rgba(0, 0, 0, 0.9);">数据集：</font>**[**coco_2014_caption**](https://modelscope.cn/datasets/modelscope/coco_2014_caption/summary)
+ **<font style="color:rgba(0, 0, 0, 0.9);">模型：</font>**[**Qwen2-VL-2B-Instruct**](https://modelscope.cn/models/Qwen/Qwen2-VL-2B-Instruct)
+ **<font style="color:rgba(0, 0, 0, 0.9);">OCR微调版：</font>**[**Qwen2-VL-Latex-OCR**](https://zhuanlan.zhihu.com/p/10705293665)

:::

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1733472157254-037f1f85-1f1b-4cf5-8fc7-24d39969869f.jpeg)

:::color5
**<font style="color:#601BDE;">1.Qwen-VL创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">对各种分辨率和比例的图像的先进理解</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 在视觉理解基准上达到最先进的性能，包括 MathVista、DocVQA、RealWorldQA、MTVQA 等。</font>
+ **<font style="color:rgb(51, 51, 51);">理解超过 20 分钟的视频</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 能够处理超过 20 分钟的视频，提供高质量的视频问答、对话、内容创作等功能。</font>
+ **<font style="color:rgb(51, 51, 51);">可操作手机、机器人等设备的智能体</font>**<font style="color:rgb(51, 51, 51);">：具备复杂推理和决策能力的 Qwen2-VL 可以与手机、机器人等设备集成，基于视觉环境和文本指令进行自动操作。</font>
+ **<font style="color:rgb(51, 51, 51);">多语言支持</font>**<font style="color:rgb(51, 51, 51);">：为了服务全球用户，Qwen2-VL 除了支持英语和中文外，现在还能够理解图像中不同语言的文本，包括大多数欧洲语言、日语、韩语、阿拉伯语、越南语等。</font>

**<font style="color:rgb(0, 128, 255);">Lora 是一种高效微调方法，深入了解其原理可参见笔记：</font>**[**LoRA**](https://www.yuque.com/zhongxian-iiot9/gi3w2u/cgil121ar06pez6m)

<font style="color:rgba(0, 0, 0, 0.9);">代码、数据、模型、训练过程链接见文末～</font>

# <font style="color:rgba(0, 0, 0, 0.9);">环境配置</font>
:::color3
<font style="color:rgba(0, 0, 0, 0.9);">环境配置分为三步</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgba(0, 0, 0, 0.9);">确保你的电脑上至少有一张英伟达显卡，并已安装好了CUDA环境。</font>
2. <font style="color:rgba(0, 0, 0, 0.9);">安装Python（版本>=3.8）以及能够调用CUDA加速的PyTorch。</font>
3. <font style="color:rgba(0, 0, 0, 0.9);">安装Qwen2-VL微调相关的第三方库，可以使用以下命令：</font>

```python
python -m pip install --upgrade pip
# 更换 pypi 源加速库的安装
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install modelscope==1.18.0
pip install transformers==4.46.2
pip install sentencepiece==0.2.0
pip install accelerate==1.1.1
pip install datasets==2.18.0
pip install peft==0.13.2
pip install swanlab==0.3.25
pip install qwen-vl-utils==0.0.8
```

# <font style="color:rgba(0, 0, 0, 0.9);">准备数据集</font>
:::color3
<font style="color:rgba(0, 0, 0, 0.9);">本节使用的是 </font>**<u><font style="color:rgb(0, 128, 255);">coco_2014_caption</font></u>**<font style="color:rgba(0, 0, 0, 0.9);"> 数据集（中的500张图），该数据集主要用于多模态（Image-to-Text）任务。</font>

:::

:::color5
**<font style="color:#601BDE;">1.数据集介绍</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

COCO 2014 Caption数据集是Microsoft Common Objects in Context (COCO)数据集的一部分，主要用于图像描述任务。该数据集包含了大约40万张图像，每张图像都有至少1个人工生成的英文描述语句。这些描述语句旨在帮助计算机理解图像内容，并为图像自动生成描述提供训练数据。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749444870119-cc85a24d-3a4b-468a-a2a9-2b51032a269d.png)

<font style="color:rgba(0, 0, 0, 0.9);">在本节的任务中，我们主要使用其中的前500张图像，并对它进行处理和格式调整，目标是组合成如下格式的json文件：</font>

```python
[
{
    "id": "identity_1",
    "conversations": [
      {
        "from": "user",
        "value": "COCO Yes: <|vision_start|>图像文件路径<|vision_end|>"
      },
      {
        "from": "assistant",
        "value": "A snow skier assessing the mountain before starting to sky"
      }
    ]
},
...
]
```

<font style="color:rgba(0, 0, 0, 0.9);">其中，"from"是角色（user代表人类，assistant代表模型），"value"是聊天的内容，其中</font>`<font style="color:rgb(0, 122, 170);background-color:rgb(238, 238, 238);"><|vision_start|></font>`<font style="color:rgba(0, 0, 0, 0.9);">和</font>`<font style="color:rgb(0, 122, 170);background-color:rgb(238, 238, 238);"><|vision_end|></font>`<font style="color:rgba(0, 0, 0, 0.9);">是Qwen2-VL模型识别图像的标记，中间可以放图像的文件路径，也可以是URL。</font>

:::color5
**<font style="color:#601BDE;">2.数据集下载与处理方式</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgba(0, 0, 0, 0.9);">我们需要做四件事情：</font>**
    - <font style="color:rgba(0, 0, 0, 0.9);">通过</font>Modelscope<font style="color:rgba(0, 0, 0, 0.9);">下载coco_2014_caption数据集</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">加载数据集，将图像保存到本地</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">将图像路径和描述文本转换为一个csv文件</font>
    - <font style="color:rgba(0, 0, 0, 0.9);">将csv文件转换为json文件</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">使用下面的代码完成从数据下载到生成csv的过程：</font>**

<font style="color:rgba(0, 0, 0, 0.9);">data2csv.py：</font>

```python

# 导入所需的库
from modelscope.msdatasets import MsDataset
import os
import pandas as pd

MAX_DATA_NUMBER = 500

# 检查目录是否已存在
if not os.path.exists('coco_2014_caption'):
    # 从modelscope下载COCO 2014图像描述数据集
    ds =  MsDataset.load('modelscope/coco_2014_caption', subset_name='coco_2014_caption', split='train')
    print(len(ds))
    # 设置处理的图片数量上限
    total = min(MAX_DATA_NUMBER, len(ds))

    # 创建保存图片的目录
    os.makedirs('coco_2014_caption', exist_ok=True)

    # 初始化存储图片路径和描述的列表
    image_paths = []
    captions = []

    for i in range(total):
        # 获取每个样本的信息
        item = ds[i]
        image_id = item['image_id']
        caption = item['caption']
        image = item['image']

        # 保存图片并记录路径
        image_path = os.path.abspath(f'coco_2014_caption/{image_id}.jpg')
        image.save(image_path)

        # 将路径和描述添加到列表中
        image_paths.append(image_path)
        captions.append(caption)

        # 每处理50张图片打印一次进度
        if (i + 1) % 50 == 0:
            print(f'Processing {i+1}/{total} images ({(i+1)/total*100:.1f}%)')

    # 将图片路径和描述保存为CSV文件
    df = pd.DataFrame({
        'image_path': image_paths,
        'caption': captions
    })

    # 将数据保存为CSV文件
    df.to_csv('./coco-2024-dataset.csv', index=False)

    print(f'数据处理完成，共处理了{total}张图片')

else:
    print('coco_2014_caption目录已存在,跳过数据处理步骤')
```

**<font style="color:rgba(0, 0, 0, 0.9);">3. 在同一目录下，用以下代码，将csv文件转换为json文件：</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgba(0, 0, 0, 0.9);">csv2json.py：</font>

```python
import pandas as pd
import json

# 载入CSV文件
df = pd.read_csv('./coco-2024-dataset.csv')
conversations = []

# 添加对话数据
for i in range(len(df)):
    conversations.append({
        "id": f"identity_{i+1}",
        "conversations": [
            {
                "from": "user",
                "value": f"COCO Yes: <|vision_start|>{df.iloc[i]['image_path']}<|vision_end|>"
            },
            {
                "from": "assistant", 
                "value": df.iloc[i]['caption']
            }
        ]
    })

# 保存为Json
with open('data_vl.json', 'w', encoding='utf-8') as f:
    json.dump(conversations, f, ensure_ascii=False, indent=2
```

<font style="color:rgba(0, 0, 0, 0.9);">此时目录下会多出两个文件：</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">coco-2024-dataset.csv</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">data_vl.json</font>

<font style="color:rgba(0, 0, 0, 0.9);">至此，我们完成了数据集的准备。</font>

# <font style="color:rgba(0, 0, 0, 0.9);">模型下载与加载</font>
:::color3
<font style="color:rgb(60, 60, 67);">使用modelscope下载Qwen2-VL-2B-Instruct模型，然后把它加载到Transformers中进行训练：</font>

:::

:::color5
**<font style="color:#601BDE;">1.模型下载</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from modelscope import snapshot_download, AutoTokenizer
from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq, Qwen2VLForConditionalGeneration, AutoProcessor
import torch

# 在modelscope上下载Qwen2-VL模型到本地目录下
model_dir = snapshot_download("Qwen/Qwen2-VL-2B-Instruct", cache_dir="./", revision="master")

# 使用Transformers加载模型权重
tokenizer = AutoTokenizer.from_pretrained("./Qwen/Qwen2-VL-2B-Instruct/", use_fast=False, trust_remote_code=True)
# 特别的，Qwen2-VL-2B-Instruct模型需要使用Qwen2VLForConditionalGeneration来加载
model = Qwen2VLForConditionalGeneration.from_pretrained("./Qwen/Qwen2-VL-2B-Instruct/", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True,)
model.enable_input_require_grads()  # 开启梯度检查点时，要执行该方法
```

<font style="color:rgb(60, 60, 67);">模型大小为 4.5GB，下载模型大概需要 5 分钟。</font>

:::color5
**<font style="color:#601BDE;">2.集成SwanLab</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<u><font style="color:rgb(0, 128, 255);">SwanLab</font></u>**<font style="color:rgba(0, 0, 0, 0.9);"> 是一个开源的模型训练记录工具。SwanLab面向AI研究者，提供了训练可视化、自动日志记录、超参数记录、实验对比、多人协同等功能。在SwanLab上，研究者能基于直观的可视化图表发现训练问题，对比多个实验找到研究灵感，并通过在线链接的分享与基于组织的多人协同训练，打破团队沟通的壁垒。</font>

<font style="color:rgba(0, 0, 0, 0.9);">SwanLab与Transformers已经做好了集成，用法是在Trainer的</font>`<font style="color:rgb(0, 122, 170);background-color:rgb(238, 238, 238);">callbacks</font>`<font style="color:rgba(0, 0, 0, 0.9);">参数中添加</font>`<font style="color:rgb(0, 122, 170);background-color:rgb(238, 238, 238);">SwanLabCallback</font>`<font style="color:rgba(0, 0, 0, 0.9);">实例，就可以自动记录超参数和训练指标，简化代码如下：</font>

```python
from swanlab.integration.transformers import SwanLabCallback
from transformers import Trainer

swanlab_callback = SwanLabCallback()

trainer = Trainer(
    ...
    callbacks=[swanlab_callback],
)
```

<font style="color:rgba(0, 0, 0, 0.9);">首次使用SwanLab，需要先</font><font style="color:rgba(0, 0, 0, 0.9);">在</font>**<u><font style="color:rgb(0, 128, 255);">官网</font></u>**<font style="color:rgba(0, 0, 0, 0.9);">注册</font><font style="color:rgba(0, 0, 0, 0.9);">一个账号，然后在用户设置页面复制你的</font>API Key<font style="color:rgba(0, 0, 0, 0.9);">，然后在训练开始提示登录时粘贴即可，后续无需再次登录：</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1749442840581-5c8ff4b8-6809-4518-a938-ee777ea1dd7d.webp)

<font style="color:rgba(0, 0, 0, 0.9);">更多用法可参考</font>**<u><font style="color:rgb(0, 128, 255);">快速开始</font></u>**<font style="color:rgba(0, 0, 0, 0.9);">、</font>**<u><font style="color:rgb(0, 128, 255);">Transformers集成</font></u>**<font style="color:rgba(0, 0, 0, 0.9);">。</font>

# <font style="color:rgba(0, 0, 0, 0.9);">开始微调</font>
:::color3
**<font style="color:rgba(0, 0, 0, 0.9);">本节代码做了以下几件事：</font>**

1. <font style="color:rgba(0, 0, 0, 0.9);">下载并加载Qwen2-VL-2B-Instruct模型</font>
2. <font style="color:rgba(0, 0, 0, 0.9);">加载数据集，取前496条数据参与训练，4条数据进行主观评测</font>
3. <font style="color:rgba(0, 0, 0, 0.9);">配置Lora，参数为r=64, lora_alpha=16, lora_dropout=0.05</font>
4. <font style="color:rgba(0, 0, 0, 0.9);">使用SwanLab记录训练过程，包括超参数、指标和最终的模型输出结果</font>
5. <font style="color:rgba(0, 0, 0, 0.9);">训练2个epoch</font>

:::

:::color5
**<font style="color:#601BDE;">1.代码的目录结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
|———— train.py
|———— coco_2014_caption
|———— coco-2024-dataset.csv
|———— data_vl.json
|———— data2csv.py
|———— csv2json.py
```

:::color5
**<font style="color:#601BDE;">2.完整代码如下</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">train.py：</font>

```python
import torch
from datasets import Dataset
from modelscope import snapshot_download, AutoTokenizer
from swanlab.integration.transformers import SwanLabCallback
from qwen_vl_utils import process_vision_info
from peft import LoraConfig, TaskType, get_peft_model, PeftModel
from transformers import (
TrainingArguments,
Trainer,
DataCollatorForSeq2Seq,
Qwen2VLForConditionalGeneration,
AutoProcessor,
)
import swanlab
import json


def process_func(example):
    """
    将数据集进行预处理
    """
    MAX_LENGTH = 8192
    input_ids, attention_mask, labels = [], [], []
    conversation = example["conversations"]
    input_content = conversation[0]["value"]
    output_content = conversation[1]["value"]
    file_path = input_content.split("<|vision_start|>")[1].split("<|vision_end|>")[0]  # 获取图像路径
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": f"{file_path}",
                    "resized_height": 280,
                    "resized_width": 280,
                },
                {"type": "text", "text": "COCO Yes:"},
            ],
        }
    ]
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )  # 获取文本
    image_inputs, video_inputs = process_vision_info(messages)  # 获取数据数据（预处理过）
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = {key: value.tolist() for key, value in inputs.items()} #tensor -> list,为了方便拼接
    instruction = inputs

    response = tokenizer(f"{output_content}", add_special_tokens=False)


    input_ids = (
        instruction["input_ids"][0] + response["input_ids"] + [tokenizer.pad_token_id]
    )

    attention_mask = instruction["attention_mask"][0] + response["attention_mask"] + [1]
    labels = (
        [-100] * len(instruction["input_ids"][0])
        + response["input_ids"]
        + [tokenizer.pad_token_id]
    )
    if len(input_ids) > MAX_LENGTH:  # 做一个截断
        input_ids = input_ids[:MAX_LENGTH]
        attention_mask = attention_mask[:MAX_LENGTH]
        labels = labels[:MAX_LENGTH]

    input_ids = torch.tensor(input_ids)
    attention_mask = torch.tensor(attention_mask)
    labels = torch.tensor(labels)
    inputs['pixel_values'] = torch.tensor(inputs['pixel_values'])
    inputs['image_grid_thw'] = torch.tensor(inputs['image_grid_thw']).squeeze(0)  #由（1,h,w)变换为（h,w）
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels,
            "pixel_values": inputs['pixel_values'], "image_grid_thw": inputs['image_grid_thw']}


def predict(messages, model):
    # 准备推理
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # 生成输出
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    return output_text[0]


# 在modelscope上下载Qwen2-VL模型到本地目录下
model_dir = snapshot_download("Qwen/Qwen2-VL-2B-Instruct", cache_dir="./", revision="master")

# 使用Transformers加载模型权重
tokenizer = AutoTokenizer.from_pretrained("./Qwen/Qwen2-VL-2B-Instruct/", use_fast=False, trust_remote_code=True)
processor = AutoProcessor.from_pretrained("./Qwen/Qwen2-VL-2B-Instruct")

model = Qwen2VLForConditionalGeneration.from_pretrained("./Qwen/Qwen2-VL-2B-Instruct/", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True,)
model.enable_input_require_grads()  # 开启梯度检查点时，要执行该方法

# 处理数据集：读取json文件
# 拆分成训练集和测试集，保存为data_vl_train.json和data_vl_test.json
train_json_path = "data_vl.json"
with open(train_json_path, 'r') as f:
    data = json.load(f)
    train_data = data[:-4]
    test_data = data[-4:]

with open("data_vl_train.json", "w") as f:
    json.dump(train_data, f)

with open("data_vl_test.json", "w") as f:
    json.dump(test_data, f)

train_ds = Dataset.from_json("data_vl_train.json")
train_dataset = train_ds.map(process_func)

# 配置LoRA
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=False,  # 训练模式
    r=64,  # Lora 秩
    lora_alpha=16,  # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.05,  # Dropout 比例
    bias="none",
)

# 获取LoRA模型
peft_model = get_peft_model(model, config)

# 配置训练参数
args = TrainingArguments(
    output_dir="./output/Qwen2-VL-2B",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    logging_steps=10,
    logging_first_step=5,
    num_train_epochs=2,
    save_steps=100,
    learning_rate=1e-4,
    save_on_each_node=True,
    gradient_checkpointing=True,
    report_to="none",
)

# 设置SwanLab回调
swanlab_callback = SwanLabCallback(
    project="Qwen2-VL-finetune",
    experiment_name="qwen2-vl-coco2014",
    config={
        "model": "https://modelscope.cn/models/Qwen/Qwen2-VL-2B-Instruct",
        "dataset": "https://modelscope.cn/datasets/modelscope/coco_2014_caption/quickstart",
        "github": "https://github.com/datawhalechina/self-llm",
        "prompt": "COCO Yes: ",
        "train_data_number": len(train_data),
        "lora_rank": 64,
        "lora_alpha": 16,
        "lora_dropout": 0.1,
    },
)

# 配置Trainer
trainer = Trainer(
    model=peft_model,
    args=args,
    train_dataset=train_dataset,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True),
    callbacks=[swanlab_callback],
)

# 开启模型训练
trainer.train()

# ====================测试模式===================
# 配置测试参数
val_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=True,  # 训练模式
    r=64,  # Lora 秩
    lora_alpha=16,  # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.05,  # Dropout 比例
    bias="none",
)

# 获取测试模型
val_peft_model = PeftModel.from_pretrained(model, model_id="./output/Qwen2-VL-2B/checkpoint-62", config=val_config)

# 读取测试数据
with open("data_vl_test.json", "r") as f:
    test_dataset = json.load(f)

test_image_list = []
for item in test_dataset:
    input_image_prompt = item["conversations"][0]["value"]
    # 去掉前后的<|vision_start|>和<|vision_end|>
    origin_image_path = input_image_prompt.split("<|vision_start|>")[1].split("<|vision_end|>")[0]

    messages = [{
        "role": "user", 
        "content": [
            {
            "type": "image", 
            "image": origin_image_path
            },
            {
            "type": "text",
            "text": "COCO Yes:"
            }
        ]}]

    response = predict(messages, val_peft_model)
    messages.append({"role": "assistant", "content": f"{response}"})
    print(messages[-1])

    test_image_list.append(swanlab.Image(origin_image_path, caption=response))

swanlab.log({"Prediction": test_image_list})

# 在Jupyter Notebook中运行时要停止SwanLab记录，需要调用swanlab.finish()
swanlab.finish()
```

<font style="color:rgba(0, 0, 0, 0.9);">看到下面的进度条即代表训练开始：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749443202041-f22c4f3a-0a6c-4c74-ba80-77c1d102aeef.png)

# <font style="color:rgba(0, 0, 0, 0.9);">训练结果演示</font>
:::color3
<font style="color:rgba(0, 0, 0, 0.9);">详细训练过程请看这里：</font>**<u><font style="color:rgb(0, 128, 255);">qwen2-vl-coco2014</font></u>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">在</font>`<font style="color:rgb(0, 122, 170);background-color:rgb(238, 238, 238);">Prediction</font>`<font style="color:rgba(0, 0, 0, 0.9);">图表中记录着模型最终的输出结果，可以看到模型在回答的风格上是用的COCO数据集的简短英文风格进行的描述：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749443352567-c7fefc47-f329-47c6-8537-0ea64b4cb309.png)

<font style="color:rgba(0, 0, 0, 0.9);">而同样的图像，没有被微调的模型输出结果如下：</font>

```python
1-没有微调：The image depicts a cozy living room with a rocking chair in the center, a bookshelf filled with books, and a table with a vase and a few other items. The walls are decorated with wallpaper, and there are curtains on the windows. The room appears to be well-lit, with sunlight streaming in from the windows.
1-微调后：A living room with a rocking chair, a bookshelf, and a table with a vase and a bowl.

2-没有微调：It looks like a family gathering or a party in a living room. There are several people sitting around a dining table, eating pizza. The room has a cozy and warm atmosphere.
2-微调后：A group of people sitting around a dining table eating pizza.
```

<font style="color:rgb(60, 60, 67);">可以明显看到微调后风格的变化。</font>

<font style="color:rgb(255, 255, 255);background-color:rgb(160, 160, 160);"></font>

# <font style="color:rgba(0, 0, 0, 0.9);">推理LoRA微调后的模型</font>
:::color3
<font style="color:rgba(0, 0, 0, 0.9);">加载lora微调后的模型，并进行推理：</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from peft import PeftModel, LoraConfig, TaskType

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=True,
    r=64,  # Lora 秩
    lora_alpha=16,  # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.05,  # Dropout 比例
    bias="none",
)

# default: Load the model on the available device(s)
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "./Qwen/Qwen2-VL-2B-Instruct", torch_dtype="auto", device_map="auto"
)
model = PeftModel.from_pretrained(model, model_id="./output/Qwen2-VL-2B/checkpoint-62", config=config)
processor = AutoProcessor.from_pretrained("./Qwen/Qwen2-VL-2B-Instruct")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "测试图像路径",
            },
            {"type": "text", "text": "COCO Yes:"},
        ],
    }
]

# Preparation for inference
text = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
image_inputs, video_inputs = process_vision_info(messages)
inputs = processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt",
)
inputs = inputs.to("cuda")

# Inference: Generation of the output
generated_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)
```

<font style="color:rgba(0, 0, 0, 0.9);">  
</font>

# <font style="color:rgba(0, 0, 0, 0.9);">补充</font>
:::color3
<font style="color:rgba(0, 0, 0, 0.9);">详细硬件配置和参数说明</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgba(0, 0, 0, 0.9);">使用4张A100 40GB显卡，batch size为4，gradient accumulation steps为4，训练2个epoch的用时为1分钟57秒。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749443407247-cd7b91a5-6e4c-4fb6-b8d1-bcde0a4a6c66.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1749443422366-546f429e-d901-4c01-962f-5ea427e66575.png)

# <font style="color:rgba(0, 0, 0, 0.9);">注意</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">在微调脚本中，</font>`<font style="color:rgb(0, 122, 170);background-color:rgb(238, 238, 238);">val_peft_model</font>`<font style="color:rgba(0, 0, 0, 0.9);">加载的是一共固定的checkpoint文件，如果你添加了数据或超参数，请根据实际情况修改checkpoint文件路径。</font>

<font style="color:rgb(255, 255, 255);background-color:rgb(160, 160, 160);">9</font>

# <font style="color:rgba(0, 0, 0, 0.9);">相关资料</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">训练过程：</font>**<font style="color:rgb(0, 128, 255);">Qwen2-VL-finetune</font>**

**<font style="color:rgb(0, 128, 255);">（</font>**<u><font style="color:rgb(0, 128, 255);">https://swanlab.cn/@ZeyiLin/Qwen2-VL-finetune/runs/pkgest5xhdn3ukpdy6kv5/chart）</font></u>

+ <font style="color:rgba(0, 0, 0, 0.9);">Github：</font><font style="color:rgba(0, 0, 0, 0.9);"></font>

**<font style="color:rgb(0, 128, 255);">代码仓库（</font>**<u><font style="color:rgb(0, 128, 255);">https://github.com/Zeyi-Lin/LLM-Finetune/tree/main/qwen2_vl</font></u>**<font style="color:rgb(0, 128, 255);">）</font>**<font style="color:rgba(0, 0, 0, 0.9);">、</font><font style="color:rgba(0, 0, 0, 0.9);"></font>

**<font style="color:rgb(0, 128, 255);">self-llm（</font>**<u><font style="color:rgb(0, 128, 255);">https://github.com/datawhalechina/self-llm</font></u>**<font style="color:rgb(0, 128, 255);">）</font>**

+ <font style="color:rgba(0, 0, 0, 0.9);">数据集：</font>**<font style="color:rgb(0, 128, 255);">coco_2014_caption</font>**

**<font style="color:rgb(0, 128, 255);">（</font>**<u><font style="color:rgb(0, 128, 255);">https://modelscope.cn/datasets/modelscope/coco_2014_caption/summary</font></u>**<font style="color:rgb(0, 128, 255);">）</font>**

+ <font style="color:rgba(0, 0, 0, 0.9);">模型：</font>**<font style="color:rgb(0, 128, 255);">Qwen2-VL-2B-Instruct</font>**

**<font style="color:rgb(0, 128, 255);">（</font>**<u><font style="color:rgb(0, 128, 255);">https://modelscope.cn/models/Qwen/Qwen2-VL-2B-Instruct</font></u>**<font style="color:rgb(0, 128, 255);">）</font>**

+ <font style="color:rgba(0, 0, 0, 0.9);">OCR微调版：</font>**<font style="color:rgb(0, 128, 255);">Qwen2-VL-Latex-OCR</font>**

**<font style="color:rgb(0, 128, 255);">（</font>****<u><font style="color:rgb(0, 128, 255);">https://zhuanlan.zhihu.com/p/10705293665</font></u>****<font style="color:rgb(0, 128, 255);">）</font>**

