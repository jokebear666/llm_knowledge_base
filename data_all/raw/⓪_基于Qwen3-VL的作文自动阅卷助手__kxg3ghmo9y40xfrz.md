# ⓪ 基于Qwen3-VL的作文自动阅卷助手

<!-- source: yuque://zhongxian-iiot9/hlyypb/kxg3ghmo9y40xfrz -->

:::success
**简介：**本项目旨在基于 **<font style="color:#74B602;">Qwen3-vl-30B-A3B-Instruct </font>**模型，革新传统作文批改模式，通过智能化的技术手段，精准应对 K-12 及高等教育中作文评估的三大核心挑战：

+ 📉 **减轻负担：**大幅降低教师繁重的批改工作量。
+ ⚖️ **减少偏差：**消除评分过程中的主观因素，确保公平性。
+ ⚡ **即时反馈：**实现学生写作的即时评估与指导。<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::color3
**核心方案：**该助手通过对**<font style="color:#ED740C;">高质量中文作文数据进行指令微调（Instruction Tuning）</font>**，使大语言模型深度对齐具体的评分标准。

+ **多维度分析：**模型能够快速、客观、一致地完成作文的深度分析与评分。
+ **高效支持：**为教学场景提供科学、智能的辅助工具。
+ **技术支撑：**采用**<font style="color:#ED740C;"> LLaMA Factory 作为微调框架</font>**。凭借其成熟便捷的 WebUI 操作界面，极大地简化了模型的训练、推理与部署流程，为项目提供了理想的工具支持。

**微调平台：**[**LLaMA-Factory-Online**](https://www.llamafactory.online/register?agentID=user-dYSsExlm0F)

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768621088954-32d36b32-2e15-4adf-8388-452efe5024c4.png)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768489455868-0a2c82f9-a5e4-4f63-8b6b-aed09d055d70.png)

#### 
## <font style="color:rgb(28, 30, 33);">配置概览</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">使用推荐资源（H800*1）进行微调时微调过程总时长约45min。</font><font style="color:#D22D8D;">(by草莓师姐)</font>

:::

| **<font style="color:rgb(28, 30, 33);">配置参数</font>** | **<font style="color:rgb(28, 30, 33);">配置项</font>** | **<font style="color:rgb(28, 30, 33);">是否预置</font>** | **<font style="color:rgb(28, 30, 33);">说明</font>** |
| --- | :--- | :--- | --- |
| <font style="color:rgb(28, 30, 33);">模型</font> | <font style="color:rgb(28, 30, 33);">Qwen3-vl-30B-A3B-Instruct</font> | <font style="color:rgb(28, 30, 33);">是</font> | <font style="color:rgb(28, 30, 33);">稀疏激活，仅3B参数激活，支持高分辨率动态切换。</font> |
| <font style="color:rgb(28, 30, 33);">数据集</font> | <font style="color:rgb(28, 30, 33);">AES_Dataset</font> | <font style="color:rgb(28, 30, 33);">否（提供下载链接）</font> | <font style="color:rgb(28, 30, 33);">这是一个专注于中国高中阶段的中文作文数据集，具有鲜明的教育领域特征。该数据集包含300篇精选作文样本。</font> |
| <font style="color:rgb(28, 30, 33);">GPU</font> | <font style="color:rgb(28, 30, 33);">H800*1（推荐）</font> | <font style="color:rgb(28, 30, 33);">-</font> | <font style="color:rgb(28, 30, 33);">-</font> |
| <font style="color:rgb(28, 30, 33);">微调方法</font> | <font style="color:rgb(28, 30, 33);">lora</font> | <font style="color:rgb(28, 30, 33);">-</font> | <font style="color:rgb(28, 30, 33);">显著降低计算与存储成本，兼具高性能与部署灵活性。</font> |


![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768619857435-f5562527-a3c2-4d28-b415-a4248276a3de.png)

## <font style="color:rgb(28, 30, 33);">操作步骤</font>
### <font style="color:rgb(28, 30, 33);">步骤一：数据准备</font>
:::color3
**简介：**本项目选用 **<font style="color:#ED740C;">AES_Dataset</font>** 作为核心训练数据。这是一个专注于中国高中阶段的中文作文数据集，具有鲜明的教育领域特征，对模型能力提出了以下要求：<font style="color:#D22D8D;">(by草莓师姐)</font>

+ <font style="color:rgb(28, 30, 33);">逻辑推理能力</font>
+ <font style="color:rgb(28, 30, 33);">修辞赏析能力</font>
+ <font style="color:rgb(28, 30, 33);">价值观判断能力</font>

:::

> <font style="color:rgb(28, 30, 33);">数据集概览</font>
>
> + <font style="color:rgb(28, 30, 33);">样本数量：300篇精选作文（编号 </font>`<font style="color:rgb(28, 30, 33);">A-0001</font>`<font style="color:rgb(28, 30, 33);"> 至 </font>`<font style="color:rgb(28, 30, 33);">A-0300</font>`<font style="color:rgb(28, 30, 33);">）</font>
> + <font style="color:rgb(28, 30, 33);">内容涵盖：高中阶段常见的主题指导及相关议论文/记叙文</font>
>

#### <font style="color:rgb(28, 30, 33);">1. 数据集获取与上传</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">请按照以下步骤完成数据集的下载与云端部署：</font>

:::

1. <font style="color:rgb(28, 30, 33);">下载数据：单击 AES_Dataset</font>[下载链接](http://llamafactory-online-assets.oss-cn-beijing.aliyuncs.com/llamafactory-online/docs/v2.0/documents/xuhong/online/%E8%87%AA%E5%8A%A8%E9%98%85%E5%8D%B7/AES_Dataset.zip)<font style="color:rgb(28, 30, 33);"> 下载压缩包，并在本地解压。</font>
2. <font style="color:rgb(28, 30, 33);">上传数据：将解压后的文件上传至 LLaMA Factory Online 平台的文件管理系统。</font>
+ <font style="color:rgb(28, 30, 33);">具体操作指南请参考：</font>[SFTP上传下载](https://docs.llamafactory.online/docs/documents/guide/dataProcessing/SFTPupload)

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620064479-dd458333-64fd-4134-beee-06b980320722.png)

#### <font style="color:rgb(28, 30, 33);">2. 数据格式转换（文本转图片）</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">本步骤将作文文本格式转换为图片格式，请按以下流程操作：</font>

:::

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620078589-48e82b4e-094e-47cc-b8c4-3fc445798267.png)

:::color5
**<font style="color:#601BDE;">2.1 启动实例环境 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. <font style="color:rgb(28, 30, 33);">进入 LLaMA-Factory Online 平台，单击“控制台”。</font>
2. <font style="color:rgb(28, 30, 33);">在左侧导航栏选择“实例空间”，然后单击页面上的“开始微调”。</font>
3. <font style="color:rgb(28, 30, 33);">配置环境参数：</font>
+ <font style="color:rgb(28, 30, 33);">镜像：选择对应镜像 (如下图)</font>
+ <font style="color:rgb(28, 30, 33);">资源：选择“CPU”</font>
+ <font style="color:rgb(28, 30, 33);">核数：选择“2核” (如下图)</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620107564-4dc5bd64-e6a6-43e9-8576-fed19400f57a.png)

4. <font style="color:rgb(28, 30, 33);">单击“启动”。</font>

> 💡<font style="color:rgb(28, 30, 33);"> 费用提示  
</font><font style="color:rgb(28, 30, 33);">系统会根据所需资源及其相关参数，动态预估数据处理费用，您可在页面底部查看预估结果。</font>
>

:::color5
**<font style="color:#601BDE;">2.2 创建处理脚本 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. <font style="color:rgb(28, 30, 33);">实例启动后，单击 [VSCode处理专属数据] 页签进入编辑器（也可选择 JupyterLab）。</font>
2. <font style="color:rgb(28, 30, 33);">在左侧目录 </font>`<font style="color:rgb(28, 30, 33);">user-data/datasets/AES_Dataset</font>`<font style="color:rgb(28, 30, 33);"> 下新建一个 </font>`<font style="color:rgb(28, 30, 33);">.py</font>`<font style="color:rgb(28, 30, 33);"> 后缀的文件 (如图①)。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620346437-291db7e4-4df8-467d-9e16-58b59449dfe0.png)

3. <font style="color:rgb(28, 30, 33);">将以下代码复制并保存至该文件中 (如图②)：</font>

```tsx
#多模态数据格式转换代码
#文本转图片
import os
from PIL import Image, ImageDraw, ImageFont

# ---------- 参数 ----------
INPUT_DIR  = "/workspace/user-data/datasets/AES_Dataset/essays"          # 原始 txt
OUTPUT_DIR = "/workspace/user-data/datasets/AES_Dataset/essays_png"     # 输出 png
WIDTH, HEIGHT = 1240, 1754      # A4 150 dpi
MARGIN        = 60              # 四边留白
FONT_SIZE     = 20
LINE_HEIGHT   = FONT_SIZE + 10
BG_COLOR, FG_COLOR = "white", "black"
FONT_PATH     = "/workspace/user-data/datasets/AES_Dataset/SIMHEI.TTF"  # 确保存在
# --------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

def pixel_wrap(text: str, font: ImageFont.FreeTypeFont, max_px: float, draw: ImageDraw.Draw):
    """逐字符量像素，强制折行，返回行列表"""
    lines, line = [], ""
    for ch in text:
        if draw.textlength(line + ch, font=font) <= max_px:
            line += ch
        else:
            if line:
                lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines

for txt_name in os.listdir(INPUT_DIR):
    if not txt_name.endswith(".txt"):
        continue
    with open(os.path.join(INPUT_DIR, txt_name), encoding="utf-8") as f:
        text = f.read().strip()

    img  = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    max_width = WIDTH - 2 * MARGIN   # 可打印像素宽度
    y = MARGIN
    for para in text.splitlines():
        if para.strip() == "":
            y += LINE_HEIGHT
            continue
        # 按像素折行
        for line in pixel_wrap(para, font, max_width, draw):
            draw.text((MARGIN, y), line, font=font, fill=FG_COLOR)
            y += LINE_HEIGHT
            if y > HEIGHT - MARGIN:
                break
        if y > HEIGHT - MARGIN:
            break

    out_path = os.path.join(OUTPUT_DIR, txt_name.replace(".txt", ".png"))
    img.save(out_path)
    print("saved", out_path)

print("✅ 全部转换完成，右侧无截字。输出目录：", OUTPUT_DIR)
```

:::color5
**<font style="color:#601BDE;">2.3 执行转换命令 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(28, 30, 33);">在 VSCode 页面新建一个终端（Terminal），依次执行以下命令：</font>

```tsx
conda activate /opt/conda/envs/lf
python /workspace/user-data/datasets/AES_Dataset/text_to_image.py
```

> ⚠️<font style="color:rgb(28, 30, 33);"> 注意  
</font><font style="color:rgb(28, 30, 33);">命令中的 </font>`<font style="color:rgb(28, 30, 33);">text_to_image.py</font>`<font style="color:rgb(28, 30, 33);"> 为本示例新建的文件名，请根据您实际创建的文件名进行替换。  
</font><font style="color:rgb(28, 30, 33);">当终端回显信息如下图所示时，说明格式转换成功。</font>
>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620385112-8dfb32b4-fbdf-41ab-9ab0-955a1627a063.png)

#### <font style="color:rgb(28, 30, 33);">3. 数据集注册</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">为了让系统识别新数据，需要修改配置文件。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(28, 30, 33);">请打开 </font>`<font style="color:rgb(28, 30, 33);">/workspace/llamafactory/data/dataset_info.json</font>`<font style="color:rgb(28, 30, 33);"> 配置文件 (如图①)，并配置如下内容以完成注册 (如图②)：</font>

```tsx
 "aes_data": {
    "file_name": "/workspace/user-data/datasets/AES_Dataset/aes_data.json",
    "formatting": "sharegpt",
    "columns": {
    "messages": "conversations",
    "images": "images"
    },
    "tags": {
    "role_tag": "from",
    "content_tag": "value",
    "user_tag": "user",
    "assistant_tag": "assistant"
    },
    "customized_status": 8,
    "total_tokens": "319459",
    "num_samples": "300",
    "avg_tokens": "1064.86"
}
```

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620412062-34d5deff-cbeb-4024-b800-90af6b2ea6bc.png)

#### <font style="color:rgb(28, 30, 33);">4. 数据集检测与验证</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">最后，请验证数据集格式是否符合要求：</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. <font style="color:rgb(28, 30, 33);">返回 LLaMA-Factory Online 控制台，单击左侧导航栏的“文件管理”。</font>
2. <font style="color:rgb(28, 30, 33);">找到目标数据集，单击右侧“操作”列的 “数据集检测”。  
</font>✅<font style="color:rgb(28, 30, 33);"> 验证标准：  
</font><font style="color:rgb(28, 30, 33);">如下图所示，若“数据集格式检测”结果显示为 “符合”，则表示数据集已准备就绪。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768620418984-931ac54f-339a-466f-866f-9107094ed6b9.png)



### <font style="color:rgb(28, 30, 33);">步骤二：模型训练</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">我们使用</font>[**LLaMA Factory Online**](https://www.llamafactory.online/register?agentID=user-dYSsExlm0F)<font style="color:rgb(28, 30, 33);">通过任务模式运行微调任务，操作详情如下。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. <font style="color:rgb(28, 30, 33);">进入</font>[**LLaMA Factory Online**](https://www.llamafactory.online/register?agentID=user-dYSsExlm0F)<font style="color:rgb(28, 30, 33);">平台，单击“控制台”，进入控制台后单击左侧导航栏的“模型微调”进入页面。</font>
2. <font style="color:rgb(28, 30, 33);">选择基础模型和数据集，进行参数配置。如下表所示，具体可参考下图。</font>
    - <font style="color:rgb(28, 30, 33);">资源配置。推荐卡数为1卡。</font>
    - <font style="color:rgb(28, 30, 33);">选择价格模式。本实践选择“极速尊享”。</font>
    - <font style="color:rgb(28, 30, 33);">开始训练。单击“开始训练”按钮，开始模型训练。</font>

| **<font style="color:rgb(28, 30, 33);">配置参数</font>** | **<font style="color:rgb(28, 30, 33);">参数说明</font>** | **<font style="color:rgb(28, 30, 33);">参数</font>** |
| :--- | --- | --- |
| **<font style="color:rgb(28, 30, 33);">基础配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">model</font> | <font style="color:rgb(28, 30, 33);">训练用的基模型。</font> | <font style="color:rgb(28, 30, 33);">Qwen3-VL-30B-A3B-Instruct</font> |
| <font style="color:rgb(28, 30, 33);">dataset</font> | <font style="color:rgb(28, 30, 33);">训练使用的数据集名称。</font> | <font style="color:rgb(28, 30, 33);">aes_data</font> |
| <font style="color:rgb(28, 30, 33);">stage</font> | <font style="color:rgb(28, 30, 33);">训练方式</font> | <font style="color:rgb(28, 30, 33);">sft</font> |
| <font style="color:rgb(28, 30, 33);">finetuning_type</font> | <font style="color:rgb(28, 30, 33);">微调方法</font> | <font style="color:rgb(28, 30, 33);">lora</font> |
| **<font style="color:rgb(28, 30, 33);">进阶配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">LR Scheduling Type</font> | <font style="color:rgb(28, 30, 33);">动态调整学习率的方式。</font> | <font style="color:rgb(28, 30, 33);">cosine</font> |
| <font style="color:rgb(28, 30, 33);">Max Gradient Norm</font> | <font style="color:rgb(28, 30, 33);">梯度裁剪的最大范数，用于防止梯度爆炸。</font> | <font style="color:rgb(28, 30, 33);">1.0</font> |
| **<font style="color:rgb(28, 30, 33);">训练配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">Learning Rate</font> | <font style="color:rgb(28, 30, 33);">学习率</font> | <font style="color:rgb(28, 30, 33);">5e-05</font> |
| <font style="color:rgb(28, 30, 33);">Epochs</font> | <font style="color:rgb(28, 30, 33);">训练轮数</font> | <font style="color:rgb(28, 30, 33);">3</font> |
| <font style="color:rgb(28, 30, 33);">per_device_train_batch_size</font> | <font style="color:rgb(28, 30, 33);">单GPU批处理大小。</font> | <font style="color:rgb(28, 30, 33);">2</font> |
| <font style="color:rgb(28, 30, 33);">Gradient Accumulation</font> | <font style="color:rgb(28, 30, 33);">梯度累计，将一个完整批次的梯度计算拆分为多个小批次，逐步累积梯度，最后统一更新模型参数。</font> | <font style="color:rgb(28, 30, 33);">4</font> |
| <font style="color:rgb(28, 30, 33);">Save steps</font> | <font style="color:rgb(28, 30, 33);">训练过程中每隔多少个训练步保存一次模型。</font> | <font style="color:rgb(28, 30, 33);">200</font> |
| <font style="color:rgb(28, 30, 33);">Warmup Ratio</font> | <font style="color:rgb(28, 30, 33);">将学习率从零增加到初始值的训练步数比例。</font> | <font style="color:rgb(28, 30, 33);">0</font> |
| <font style="color:rgb(28, 30, 33);">Chat Template</font> | <font style="color:rgb(28, 30, 33);">基模型的对话模版，训练和推理时构造prompt的模版。</font> | <font style="color:rgb(28, 30, 33);">qwen3</font> |
| **<font style="color:rgb(28, 30, 33);">效率与性能配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">Mixed Precision Train</font> | <font style="color:rgb(28, 30, 33);">混合精度训练，模型在训练或推理时所使用的数据精度格式，如 FP32、FP16 或 BF16。</font> | <font style="color:rgb(28, 30, 33);">bf16</font> |
| **<font style="color:rgb(28, 30, 33);">数据参数配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">Max Sample Size</font> | <font style="color:rgb(28, 30, 33);">每个数据集的最大样本数：设置后，每个数据集的样本数将被截断至指定的 max_samples。</font> | <font style="color:rgb(28, 30, 33);">100000</font> |
| <font style="color:rgb(28, 30, 33);">Cutoff Length</font> | <font style="color:rgb(28, 30, 33);">输入的最大 token 数，超过该长度会被截断。</font> | <font style="color:rgb(28, 30, 33);">2048</font> |
| <font style="color:rgb(28, 30, 33);">Preprocess Workers</font> | <font style="color:rgb(28, 30, 33);">预处理时使用的进程数量。</font> | <font style="color:rgb(28, 30, 33);">32</font> |
| **<font style="color:rgb(28, 30, 33);">日志配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">Logging Steps</font> | <font style="color:rgb(28, 30, 33);">日志打印步数。</font> | <font style="color:rgb(28, 30, 33);">5</font> |
| **<font style="color:rgb(28, 30, 33);">LoRA配置</font>** |  |  |
| <font style="color:rgb(28, 30, 33);">Lora Rank</font> | <font style="color:rgb(28, 30, 33);">LoRA 微调的本征维数 r，r 越大可训练的参数越多。</font> | <font style="color:rgb(28, 30, 33);">8</font> |
| <font style="color:rgb(28, 30, 33);">LoRA Scalling Factor</font> | <font style="color:rgb(28, 30, 33);">LoRA 缩放系数。一般情况下为 lora_rank * 2。</font> | <font style="color:rgb(28, 30, 33);">16</font> |
| <font style="color:rgb(28, 30, 33);">Random dropout</font> | <font style="color:rgb(28, 30, 33);">LoRA 微调中的 dropout 率</font> | <font style="color:rgb(28, 30, 33);">0</font> |
| <font style="color:rgb(28, 30, 33);">LoRA Modules</font> | <font style="color:rgb(28, 30, 33);">Lora作用模块</font> | <font style="color:rgb(28, 30, 33);">all</font> |


![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604195-2458f925-c8bd-42e8-ae8c-2b4f8e4316ac.png)

:::color4
**<font style="color:rgb(0, 49, 0);">提示</font>**

<font style="color:rgb(0, 49, 0);">配置模型与数据集后，系统将根据所需资源及其相关参数，动态预估任务运行时长及微调费用，您可在页面底部查看预估结果。</font>

:::

3. **<font style="color:rgb(28, 30, 33);">通过任务中心查看任务状态。</font>**<font style="color:rgb(28, 30, 33);"> </font><font style="color:rgb(28, 30, 33);">在左侧边栏选择”任务中心“，即可看到刚刚提交的任务。可以通过单击任务框，可查看任务的详细信息、超参数、训练追踪和日志。</font><font style="color:rgb(28, 30, 33);"> </font>![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604245-15a01eee-5f23-4be9-a9d3-9f5701c56b8e.png)
4. <font style="color:rgb(28, 30, 33);">任务完成后，模型自动保存在"文件管理->模型->output"文件夹中。可在"任务中心->基本信息->模型成果"处查看保存路径。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604550-fe90600e-e947-4a90-94fe-e69053d31f78.png)<font style="color:rgb(28, 30, 33);"> </font>

<font style="color:rgb(28, 30, 33);">loss结果：通过loss曲线可以看出训练有效且逐步收敛，但存在一定波动，可通过调整训练策略（如增大 batch_size、微调学习率）进一步优化稳定性。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604573-6d8e0ebc-f946-40f6-b703-03cc0273514a.png)

<font style="color:rgb(28, 30, 33);"></font>

### <font style="color:rgb(28, 30, 33);">步骤三：模型评估</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">使用推荐资源（H800*1）进行微调时微调过程总时长约45min。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. <font style="color:rgb(28, 30, 33);">单击页面左侧导航栏“模型评估”，进行评估训练配置。</font>
2. <font style="color:rgb(28, 30, 33);">微调模型选择上一步骤微调后的模型，评估数据集选择文件管理处：</font>`<font style="color:rgb(28, 30, 33);background-color:rgb(246, 247, 248);">aes_data</font>`<font style="color:rgb(28, 30, 33);">。其他参数设置如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604617-66cbc0ac-ecb2-46d2-813d-6eba05b3b399.png)

3. <font style="color:rgb(28, 30, 33);">可以在“任务中心->模型评估”下看到评估任务的运行状态。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604799-083a2988-4159-42b0-96bf-d06b2fb1287f.png)

4. <font style="color:rgb(28, 30, 33);">单击</font>![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604760-13bc939d-c541-4d28-8a1a-6b3506aff3b1.png)<font style="color:rgb(28, 30, 33);">图标，进入任务基本信息查看页面。用户可查看评估任务的基本信息、日志，评估结束后，可查看评估结果如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486604977-e4dc0e3f-c526-465f-b53a-c46ee7ab6f28.png)

<font style="color:rgb(28, 30, 33);">评估结果显示：ROUGE-1/ROUGE-2指标表现不错，说明生成内容在 “字词、短语层面” 与参考文本的覆盖度、匹配度较高；BLEU-4处于中等水平，意味着生成文本与参考文本的长短语重合度还有提升空间。</font>

### <font style="color:rgb(28, 30, 33);">步骤四：模型对话</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">使用推荐资源（H800*1）进行微调时微调过程总时长约45min。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. <font style="color:rgb(28, 30, 33);">单击左侧导航栏“模型对话”按钮进入模型对话页面。</font>
2. <font style="color:rgb(28, 30, 33);">在微调模型处选择微调的模型名称（如图①）。单击右上角“开始对话”，在弹出的“LORA模型对话限时免费”对话框，单击“立即对话”。</font>
3. <font style="color:rgb(28, 30, 33);">在输入框上传一张作文图片（如图②），并输入问题（如图③），单击发送（如图④）；在对话框中查看对话详情（如图⑤）。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1768486605006-dac24903-54d3-4118-bc87-1f97a9e07d39.png)

<font style="color:rgb(28, 30, 33);">模型输出结果解读：这个阅卷结果维度完整、判断客观，既肯定了作文在结构逻辑、思想深度、语言表达上的优势，也精准点出了衔接的不足，其给出的得分与作文的实际质量匹配度较高，是一份专业的作文评析。</font>

## <font style="color:rgb(28, 30, 33);">总结</font>
:::color3
**简介：**<font style="color:rgb(28, 30, 33);">本项目是聚焦 K-12 至高等教育场景 的智能教学辅助工具，旨在通过大语言模型技术推动教学反馈环节的智能化与高效化。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

#### 💡<font style="color:rgb(28, 30, 33);"> 解决的核心痛点</font>
<font style="color:rgb(28, 30, 33);">传统作文批改面临三大难题，本助手致力于提供针对性解决方案：</font>

+ <font style="color:rgb(28, 30, 33);">教师负担重：解决批量批改耗时耗力的问题。</font>
+ <font style="color:rgb(28, 30, 33);">评分偏差大：消除人工评分的主观性差异，确保公平。</font>
+ <font style="color:rgb(28, 30, 33);">反馈滞后：解决学生无法及时获得修改建议的困境。</font>

#### 🛠️<font style="color:rgb(28, 30, 33);"> 技术实现与优势</font>
+ <font style="color:rgb(28, 30, 33);">核心模型：基于 Qwen3-vl-30B-A3B-Instruct 打造。</font>
+ <font style="color:rgb(28, 30, 33);">精准对齐：借助自动作文评分（AES）技术，针对高质量中文作文数据集完成 LoRA 微调，实现了与标准化评分标准的精准对齐。</font>
+ <font style="color:rgb(28, 30, 33);">高效算力：依托 LLaMA Factory Online 平台提供的高性能 GPU 支持，完美兼顾了阅卷效率与成本优势。</font>

#### 🚀<font style="color:rgb(28, 30, 33);"> 应用价值</font>
+ <font style="color:rgb(28, 30, 33);">对教师：有效减轻批改压力，释放教学精力。</font>
+ <font style="color:rgb(28, 30, 33);">对学生：提供客观量化的评估结果与即时的写作反馈，助力写作能力迭代。</font>



