# ⑭ GRPO+Qwen2.5，7B大模型微调实战

<!-- source: yuque://zhongxian-iiot9/hlyypb/bltdu4pq79o6wt1f -->

# GRPO+Qwen2.5，7B大模型微调实战
:::success
**<font style="color:rgb(0, 0, 0);">背景：</font>**<font style="color:rgb(0, 0, 0);">国外技术大佬介绍如何训练领域特定模型的文章，作者使用 GRPO 微调 qwen2.5-coder-7B，实现了一个生成日程表的大模型。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">他分享了教程、代码、模型以及实践中的收获，</font><font style="color:rgb(0, 128, 255);">感兴趣的同学可以参考以下内容详细阅读：</font>

+ **<font style="color:rgb(0, 0, 0);">教程：</font>**[https://huggingface.co/blog/anakin87/qwen-scheduler-grpo](https://huggingface.co/blog/anakin87/qwen-scheduler-grpo)
+ **<font style="color:rgb(0, 0, 0);">代码：</font>**[https://github.com/anakin87/qwen-scheduler-grpo](https://github.com/anakin87/qwen-scheduler-grpo)
+ **<font style="color:rgb(0, 0, 0);">模型：</font>**[https://huggingface.co/anakin87](https://huggingface.co/anakin87)

:::

:::color3
**简介：**<font style="color:rgb(0, 0, 0);">给模型提供一份事件列表（包含开始和结束时间），并告知它哪些事件是高优先级的。目标是创建一个日程安排，使所选事件的总加权时长达到最大化。</font>

<font style="color:rgb(0, 0, 0);">在这种设定下，高优先级事件的权重为 2，普通事件的权重为 1。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747211082753-748dc67f-3862-47f7-a6ee-3c49292210a3.png)

# 示例输入<font style="color:#D22D8D;"></font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">这是 prompt 的一个精简版本（你可以在后面的内容找到完整的 prompt）。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
Task: create an optimized schedule based on the given events.
Rules: ...
You must use this format:  
<think>...</think>
<schedule>
<event>
<name>...</name>
<start>...</start>
<end>...</end>
</event>
...
</schedule>
---
Events:
- Event A (01:27 - 01:42)
- Event B (01:15 - 02:30)
- Event C (15:43 - 17:43)
Priorities:
- Event B
```

# 示例输出<font style="color:#D22D8D;"></font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">经过一番研究，作者发现这类问题属于区间调度问题。这个特定的问题是加权区间调度问题的变体，使用动态规划可以高效地解决它。</font>

<font style="color:rgb(0, 0, 0);">这使我们能够轻松计算出任何给定输入的最佳得分，而这个得分就是模型在训练过程中要努力达到的目标。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
<think>A detailed reasoning</think>
<schedule>
<event>
<name>Event B</name>
<start>01:15</start>
<end>02:30</end>
</event>
<event>
<name>Event C</name>
<start>15:43</start>
<end>17:43</end>
</event>
</schedule>
```

# 数据集生成<font style="color:#D22D8D;"></font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">既然问题已经被清晰地定义好了，下面就可以开始构建用于训练和评估模型的数据集了。</font>

<font style="color:rgb(0, 0, 0);">数据集中每一行的核心内容只是一条提示信息，其中包含了供模型进行日程安排的事件列表以及优先级信息。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">与监督微调（SFT）不同的是，这里无需提供模型应该遵循的参考生成内容。这就是为什么在像数学这类可验证的领域中，为 GRPO 构建数据集往往更容易的原因之一。</font>

<font style="color:rgb(0, 0, 0);">我们还在每一行数据中加入了最优得分（即最大可能的加权时长）。模型在训练过程中不会看到这个得分，但我们会用它来计算奖励，从而引导模型朝着正确的方向学习。</font>

<font style="color:rgb(0, 128, 255);">鉴于这些要求，编写数据集生成脚本相对容易：</font>

+ <font style="color:rgb(0, 0, 0);">使用来自不同类别的活动名称（音乐节、大学相关活动、科技会议等等）。</font>
+ <font style="color:rgb(0, 0, 0);">每个示例包含数量随机（在 4 到 8 个之间）、时长各异的活动。</font>
+ <font style="color:rgb(0, 0, 0);">确保一些活动存在时间上的重叠。</font>
+ <font style="color:rgb(0, 0, 0);">随机将某些活动标记为优先活动。</font>

<font style="color:rgb(0, 0, 0);">我们生成了 500 个示例用于训练集，100 个示例用于测试集。</font>

:::color5
**<font style="color:#601BDE;">1.数据集生成脚本</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**生成代码**：[https://github.com/anakin87/qwen-scheduler-grpo/blob/main/dataset_generation/generate.py](https://github.com/anakin87/qwen-scheduler-grpo/blob/main/dataset_generation/generate.py)

```python
"""
Event Scheduling Dataset Generator

This module generates synthetic event scheduling problems with the following characteristics:
- Random number of events (4-8) with varying durations
- Events can overlap with a controlled probability
- Some events are marked as priority events
- Each problem includes an optimal score calculation
"""

import random
from bisect import bisect_right
import json
import datasets

# Set seeds for reproducibility
random.seed(42)

# Event generation constants
MAX_EVENTS = 8
MIN_EVENTS = 4
DURATIONS = [15, 30, 45, 60, 75, 90, 105, 120]
MAX_START_HOUR = 21  # Ensures events finish within the day

# Overlap probability and constraints
OVERLAP_PROBABILITY = 0.2
MIN_OVERLAPS = 1  # Must have at least one overlap
MAX_OVERLAP_RATIO = 0.4  # Maximum 40% of events can overlap

# Priority selection constraints
MIN_PRIORITY_RATIO = 0.2  # Minimum 20% of events are priority
MAX_PRIORITY_RATIO = 0.4  # Maximum 40% of events are priority

# Load the events categories names
with open("events_categories_names.json", "r") as f:
    events_categories_names = json.load(f)


def minutes_to_time(minutes):
    """Convert minutes since midnight to HH:MM time string.

    Args:
        minutes (int): Number of minutes since midnight

    Returns:
        str: Time in HH:MM format
    """
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def time_to_minutes(time_str):
    """Convert HH:MM time string to minutes since midnight.

    Args:
        time_str (str): Time in HH:MM format

    Returns:
        int: Number of minutes since midnight
    """
    hours, mins = map(int, time_str.split(":"))
    return hours * 60 + mins


def count_overlapping_events(events):
    """Count the number of overlapping event pairs in a schedule.

    Args:
        events (list): List of events, where each event is a tuple of (name, start_time, end_time)

    Returns:
        int: Number of overlapping event pairs
    """
    overlapping_count = 0
    for j in range(len(events)):
        for k in range(j + 1, len(events)):
            e1_start = time_to_minutes(events[j][1])
            e1_end = time_to_minutes(events[j][2])
            e2_start = time_to_minutes(events[k][1])
            e2_end = time_to_minutes(events[k][2])

            if e1_start <= e2_end and e2_start <= e1_end:
                overlapping_count += 1
    return overlapping_count


def random_event():
    """Generate a random event with random start time and duration.

    Returns:
        tuple: (start_time, end_time) in HH:MM format
    """
    start_mins = random.randint(0, MAX_START_HOUR * 60 + 59)
    duration = random.choice(DURATIONS)
    end_mins = start_mins + duration
    return minutes_to_time(start_mins), minutes_to_time(end_mins)


def overlapping_event(prev_event):
    """Generate an event that overlaps with a previous event.

    Args:
        prev_event (tuple): Previous event tuple (name, start_time, end_time)

    Returns:
        tuple: (start_time, end_time) in HH:MM format
    """
    prev_start_mins = time_to_minutes(prev_event[1])
    prev_end_mins = time_to_minutes(prev_event[2])
    start_mins = random.randint(prev_start_mins, prev_end_mins - 1)
    duration = random.choice(DURATIONS)
    end_mins = start_mins + duration
    return minutes_to_time(start_mins), minutes_to_time(end_mins)


def generate_events():
    """Generate a valid schedule of events with controlled overlap and priority constraints.

    Returns:
        tuple: (events, priority_list) where:
            - events: List of (name, start_time, end_time) tuples
            - priority_list: List of event names marked as priority
    """
    category = random.choice(list(events_categories_names.keys()))
    while True:  # Keep trying until we get a valid schedule
        event_names = list(events_categories_names[category])  # create a copy

        events = []
        n_events = random.randint(MIN_EVENTS, MAX_EVENTS)

        for i in range(1, n_events + 1):
            event_name = random.choice(event_names)
            event_names.remove(event_name)

            if i == 1 or random.random() >= OVERLAP_PROBABILITY or not events:
                event_start, event_end = random_event()
            else:
                event_start, event_end = overlapping_event(random.choice(events))

            events.append((event_name, event_start, event_end))
            events.sort(key=lambda x: x[1])

        total_overlaps = count_overlapping_events(events)

        # Check if we have a valid schedule
        if total_overlaps >= MIN_OVERLAPS and total_overlaps <= MAX_OVERLAP_RATIO * len(
            events
        ):
            # Select priority events
            min_priority = max(1, int(len(events) * MIN_PRIORITY_RATIO))
            max_priority = int(len(events) * MAX_PRIORITY_RATIO)
            n_priority = random.randint(min_priority, max_priority)

            priority_events = random.sample(events, n_priority)
            priority_list = [e[0] for e in priority_events]

            events = sorted(events, key=lambda x: time_to_minutes(x[1]))

            return events, priority_list


def compute_optimal_score(events, priority_list):
    """Compute the optimal score for a schedule using dynamic programming.

    This implements a weighted interval scheduling algorithm where priority events
    have double the weight of regular events.
    We want to maximize the total weighted duration of the events.

    Inspired by: https://algo.monster/liteproblems/1235

    Args:
        events (list): List of (name, start_time, end_time) tuples
        priority_list (list): List of event names marked as priority

    Returns:
        int: Maximum possible score for the schedule
    """
    start_times = []
    end_times = []
    profits = []
    for event in events:
        start_times.append(time_to_minutes(event[1]))
        end_times.append(time_to_minutes(event[2]))
        weight = 2 if event[0] in priority_list else 1
        duration = time_to_minutes(event[2]) - time_to_minutes(event[1])
        profits.append(weight * duration)

    # Combine the job information into a single list and sort by end time.
    jobs = sorted(zip(end_times, start_times, profits))

    # Get the total number of jobs.
    number_of_jobs = len(jobs)

    # Initialize dynamic programming table with 0 profits.
    dp = [0] * (number_of_jobs + 1)

    # Iterate over the jobs.
    for i, (current_end_time, current_start_time, current_profit) in enumerate(jobs):
        # Find the rightmost job that doesn't conflict with the current job's start time.
        # Use binary search for efficient querying. 'hi' is set to the current index 'i' for optimization.
        index = bisect_right(jobs, current_start_time, hi=i, key=lambda x: x[0])

        # Update the DP table by choosing the maximum of either taking the current job or not.
        # If taking the current job, add its profit to the total profit of non-conflicting jobs.
        dp[i + 1] = max(dp[i], dp[index] + current_profit)

    # Return the maximum profit which is the last element in the DP table.
    return dp[number_of_jobs]


def generate_row():
    """Generate a single scheduling problem with all required information.

    Returns:
        dict: Dictionary containing:
            - events: List of events with times
            - priority_events: List of priority event names
            - optimal_score: Maximum possible score
            - prompt: Human-readable description of the problem
    """
    dict_events = {}
    events, priority_list = generate_events()
    dict_events["events"] = events
    dict_events["priority_events"] = priority_list

    dict_events["optimal_score"] = compute_optimal_score(events, priority_list)

    prompt = (
        "Events:\n"
        + "\n".join([f"- {event[0]} ({event[1]} - {event[2]})" for event in events])
        + "\n\n"
    )
    prompt += "Priorities:\n" + "\n".join(
        [f"- {priority}" for priority in priority_list]
    )
    dict_events["prompt"] = prompt

    return dict_events


def generate_dataset():
    """Generate a complete dataset of scheduling problems and upload to Hugging Face."""
    dataset_list = []
    for _ in range(600):
        dataset_list.append(generate_row())
    dataset = datasets.Dataset.from_list(dataset_list)
    dataset = dataset.train_test_split(test_size=100, seed=42)
    # uncomment to push the dataset
    # dataset.push_to_hub("anakin87/events-scheduling")


if __name__ == "__main__":
    generate_dataset()
```

:::color5
**<font style="color:#601BDE;">2.数据集</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**数据集链接**：[https://huggingface.co/datasets/anakin87/events-scheduling](https://huggingface.co/datasets/anakin87/events-scheduling)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747205873985-ed5c1693-1c02-4368-ae80-6635f10591cc.png)

**数据集生成**

+ 我们使用不同类别的事件名称(🎶 音乐节，🎓 大学，🧑‍💻 技术会议。..).
+ 每个示例包括具有不同持续时间的随机数量的事件（在4到8之间）。
+ 我们确保一些事件重叠。
+ 我们随机将一些事件标记为优先级。
+ 我们为训练集生成了500个示例，为测试集生成了100个示例。
+ 您可以在此处找到数据集生成脚本。

**描述**

+ events：事件列表。每个事件都是一个包含事件名称、开始时间和结束时间的列表。
+ priority_events：包含该示例中指定为高优先级的事件名称的列表（随机选择）。
+ optimal_score：给定事件/优先级可实现的最佳总加权持续时间（整数分数），使用确定性算法计算。权重1表示正常，权重2表示优先级。如果你使用像GRPO这样的RL技术，它可以用于计算奖励。
+ prompt：一个字符串，仅包含该示例的事件和优先级的格式化列表。它旨在插入到一个更大的用户提示中，其中包括任务描述和规则。我的实验中使用的系统和用户提示可以在这里找到。



# 训练
:::color5
**<font style="color:#601BDE;">1.完整训练notebook</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

[https://github.com/anakin87/qwen-scheduler-grpo/blob/main/train_grpo.ipynb](https://github.com/anakin87/qwen-scheduler-grpo/blob/main/train_grpo.ipynb)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747211269672-ecb9064d-7437-4206-bf7a-1f493077b220.png)

:::color5
**<font style="color:#601BDE;">2.训练框架：Hugging Face TRL</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">现在有几个训练库支持 GRPO。Hugging Face TRL 是一个很好的选择，它也支持使用 vLLM 在训练期间更快地生成样本。</font>

<font style="color:rgb(0, 0, 0);">在这个例子中，我们决定使用 Unsloth，它是一个对 TRL 进行修补以大幅减少 GPU 内存使用的库。此处使用 NVIDIA A6000 GPU（48GB VRAM），但经过小的调整，你可以在免费的 Colab/Kaggle 实例上用 16GB VRAM 复制同样的实验。</font>

<font style="color:rgb(0, 0, 0);">如果你的 GPU 很差，Unsloth 可以很好地进行实验，但是会有一些令人沮丧的错误，我们稍后会看到</font>

+ **<font style="color:rgb(0, 0, 0);">Hugging Face TRL</font>**<font style="color:rgb(0, 0, 0);">：</font>[https://huggingface.co/docs/trl/index](https://huggingface.co/docs/trl/index)
+ **<font style="color:rgb(0, 0, 0);">Unsloth</font>**<font style="color:rgb(0, 0, 0);">：</font>[https://docs.unsloth.ai/](https://docs.unsloth.ai/)

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">这里决定训练 Qwen2.5-Coder-7B-Instruct，这是 Qwen 系列中一款专门针对代码的语言模型。</font>

<font style="color:rgb(0, 128, 255);">这个选择有点基于经验，但主要有两个考虑因素：</font>

+ <font style="color:rgb(0, 0, 0);">作者首先尝试了较小的模型（0.5B 和 1.5B），但这些非常小的模型产生的推理几乎毫无意义。这是第一个经验教训：如果基础模型的预训练或规模使其能力与期望相差甚远，GRPO 也无法创造奇迹。</font>
+ <font style="color:rgb(0, 0, 0);">使用了代码模型而非通用模型，部分原因是这在数学任务中很常见，另一部分原因是这个模型在遵循所需格式（<think>, <schedule>等）方面已经相当出色。</font>

<font style="color:rgb(0, 0, 0);">现在使用 Unsloth 加载模型，用 QLoRA 对其进行训练以节省 GPU 资源。</font>

```python
from unsloth import FastLanguageModel
max_seq_length = 2048
lora_rank = 32
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct",
    max_seq_length = max_seq_length,
    load_in_4bit = True,
    fast_inference = True,
    max_lora_rank = lora_rank,
    gpu_memory_utilization = 0.85, # Reduce if out of memory
)
model = FastLanguageModel.get_peft_model(
    model,
    r = lora_rank,
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ], # Remove QKVO if out of memory
    lora_alpha = lora_rank,
    use_gradient_checkpointing = "unsloth", # Enable long context finetuning
    random_state = 3407,)
```

<font style="color:rgb(0, 0, 0);">如果你的显存小于 48GB，可以调整几个参数：</font>`<font style="color:rgb(0, 0, 0);">gpu_memory_utilization</font>`<font style="color:rgb(0, 0, 0);">、</font>`<font style="color:rgb(0, 0, 0);">lora_rank </font>`<font style="color:rgb(0, 0, 0);">和 </font>`<font style="color:rgb(0, 0, 0);">target_modules</font>`<font style="color:rgb(0, 0, 0);">；后两个参数会影响模型的学习能力。</font>

:::color5
**<font style="color:#601BDE;">4.数据集准备</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">数据集中的每个示例都包含事件和优先级。我们对数据集进行预处理，以系统消息和用户消息的形式添加一般任务描述和说明。</font>

```python
import datasets
SYSTEM_PROMPT = """You are a precise event scheduler.
1. First, reason through the problem inside <think> and </think> tags. Here you can create drafts, 
compare alternatives, and check for mistakes.
2. When confident, output the final schedule inside <schedule> and </schedule> tags. 
Your schedule must strictly follow the rules provided by the user."""
USER_PROMPT ="""Task: create an optimized schedule based on the given events.
Rules:
- The schedule MUST be in strict chronological order. 
  Do NOT place priority events earlier unless their actual start time is earlier.
- Event start and end times are ABSOLUTE. NEVER change, shorten, adjust, or split them.
- Priority events (weight = 2) carry more weight than normal events (weight = 1), 
  but they MUST still respect chronological order.
- Maximize the sum of weighted event durations.
- No overlaps allowed. In conflicts, include the event with the higher weighted time.
- Some events may be excluded if needed to meet these rules.
You must use this format:  
<think>...</think>
<schedule>
<event>
<name>...</name>
<start>...</start>
<end>...</end>
</event>
...
</schedule>
---
"""
ds = datasets.load_dataset("anakin87/events-scheduling", split="train")
ds = ds.map(
    lambda x: {
        "prompt": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT + x["prompt"]},
        ]
    }
)
```

:::color5
**<font style="color:#601BDE;">5.奖励函数</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">GRPO 是一种强化学习算法，在该算法中，对于每个提示，会从模型中生成多个样本（在我们的例子中是 8 个）。在训练过程中，模型的参数会被更新，以生成具有高奖励的回复。</font>

<font style="color:rgb(0, 0, 0);">因此，虽然在数据集中不需要生成的文本，但奖励函数的设计至关重要。</font>

<font style="color:rgb(0, 0, 0);">在像从 GSM8K 中学习这样较为简单的问题中，一种常见的选择是定义多个奖励函数并将它们相加：</font>

+ <font style="color:rgb(0, 0, 0);">一种方法是检查输出格式是否正确。</font>
+ <font style="color:rgb(0, 0, 0);">另一种方法是检查最终答案是否与已知解决方案相符。</font>

<font style="color:rgb(0, 0, 0);">在我们的实验中，可以很容易地为格式设计一个奖励函数。</font>

```python
import re
overall_pattern = (r"<think>.+</think>.*<schedule>.*(<event>.*<name>.+</name>.*<start>\d{2}:\d{2}</start>.*"
                   r"<end>\d{2}:\d{2}</end>.*</event>)+.*</schedule>")
overall_regex = re.compile(overall_pattern, re.DOTALL)
def format_reward(prompts, completions, **kwargs):
    responses = [completion[0]['content'] for completion in completions]
    return [0.0 if not overall_regex.match(response) else 10.0 for response in responses]
```

<font style="color:rgb(0, 0, 0);">现在，要评判日程安排本身的质量更难。</font>

<font style="color:rgb(0, 128, 255);">一个有效的日程安排具有以下特点：</font>

+ <font style="color:rgb(0, 0, 0);">活动源自原始提示（不存在臆造的活动或更改的时间）。</font>
+ <font style="color:rgb(0, 0, 0);">活动按时间顺序排列。</font>
+ <font style="color:rgb(0, 0, 0);">不存在活动重叠。</font>
+ <font style="color:rgb(0, 0, 0);">活动至少有两项。</font>

<font style="color:rgb(0, 0, 0);">我们还希望鼓励模型生成一个能使总加权时长最大化的时间表。</font>

<font style="color:rgb(0, 0, 0);">在确定下面所示的解决方案之前，作者对不同数量的奖励函数进行了试验，得出了一些观察结果。</font>

+ <font style="color:rgb(0, 0, 0);">作者尝试对分数使用单一奖励函数，如果日程安排有效（满足上述所有标准），则奖励为日程安排分数/最优分数，否则为 0。结果发现这是个糟糕的主意，因为它太不连续，而且大多数时候返回 0，无法为模型的学习提供足够的信号。</font>
+ <font style="color:rgb(0, 0, 0);">另一方面，作者尝试使用了几种奖励函数，分别对应上述每个要求：已有事件、时间顺序、无重叠等。在这种情况下，他发现即使模型在学习某些东西，但训练在生成良好的日程安排方面并不有效。使用过多的奖励函数也可能会有弊端。</font>

<font style="color:rgb(0, 0, 0);">在“奖励过多”阶段，作者遇到了一个经典的强化学习问题：奖励作弊。起初作者忘了舍弃活动少于两个的日程安排。</font>

<font style="color:rgb(0, 0, 0);">突然间，奖励看起来很不错！模型在格式、时间顺序、无重叠等方面都获得了高分……</font>

<font style="color:rgb(0, 0, 0);">查看了实际输出，发现它找到了一个漏洞：它只是生成只有一个活动的日程安排（通常是高优先级的活动）。</font>

<font style="color:rgb(0, 0, 0);">这完美地满足了大多数单个奖励函数。这并非模型聪明，而是奖励设置可被利用。</font>

<font style="color:rgb(0, 0, 0);">最终作者采用了一个奖励函数，该函数鼓励生成按时间顺序排列的日程安排，另一个奖励函数则用于最大化得分。</font>

<font style="color:rgb(0, 0, 0);">如下所示，他试图在这两个奖励函数中纳入并因此优先考虑其他要求。</font><font style="color:#D22D8D;">by草莓师姐）</font>

```python

def sorted_events_reward(completions, **kwargs):
    scores = []
    responses = [completion[0]['content'] for completion in completions]
    for response in responses:
        scheduled_events = get_events(response)
        # not a valid schedule: should be discarded
        if len(scheduled_events) < 2:
            scores.append(0.0)
            continue
        scheduled_events_minutes = [(ev[0], time_to_minutes(ev[1]), time_to_minutes(ev[2])) 
                                  for ev in scheduled_events]
        if all(scheduled_events_minutes[i][1] < scheduled_events_minutes[i+1][1] 
                  for i in range(len(scheduled_events_minutes)-1)):
            scores.append(20.0)
        else:
            scores.append(0)
    return scores
def score_reward(prompts, completions, events, priority_events, optimal_score, **kwargs):
    scores = []
    responses = [completion[0]['content'] for completion in completions]
    for content, valid_events, priorities, opt_score in zip(responses, events, priority_events, optimal_score):
        scheduled_events = get_events(content)
        # Get valid scheduled events
        existing_events = {ev for ev in scheduled_events if [ev[0], ev[1], ev[2]] in valid_events}
        # penalize choosing nonexistent events or less than 2 events (not a valid schedule)
        if len(existing_events)<len(scheduled_events) or len(existing_events) < 2:
            scores.append(0.0)
            continue
        # Convert to minutes
        existing_events_minutes = [(ev[0], time_to_minutes(ev[1]), time_to_minutes(ev[2])) 
                                  for ev in existing_events]
        # remove overlapping events and remove both events - to penalize overlaps
        overlapping_events = set()
        for j in range(len(existing_events_minutes)):
            for k in range(j + 1, len(existing_events_minutes)):
                if (existing_events_minutes[j][1] <= existing_events_minutes[k][2] and 
                    existing_events_minutes[j][2] >= existing_events_minutes[k][1]):
                    overlapping_events.add(existing_events_minutes[j])
                    overlapping_events.add(existing_events_minutes[k])
        existing_events_minutes = [ev for ev in existing_events_minutes 
                                  if ev not in overlapping_events]
        # Calculate score
        score = sum(2 * (ev[2] - ev[1]) if ev[0] in priorities 
                   else ev[2] - ev[1] for ev in existing_events_minutes)
        scores.append((score/opt_score) * 70)
    return scores
```

<font style="color:rgb(0, 128, 255);">简而言之，在实验中使用了以下奖励函数：</font><font style="color:#D22D8D;">by草莓师姐）</font>

+ <font style="color:rgb(0, 0, 0);">格式（0 - 10）</font>
+ <font style="color:rgb(0, 0, 0);">排序后的事件（0 - 20）</font>
+ <font style="color:rgb(0, 0, 0);">分数（0 - 70）。</font>

<font style="color:rgb(0, 0, 0);">累积奖励的范围可以在 0 到 100 之间。</font>

<font style="color:rgb(0, 0, 0);">作者在这一步上反复尝试了很多次。正如将看到的，它仍然不完美，但它让模型开始学习了。</font>

:::color5
**<font style="color:#601BDE;">6.开始训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from trl import GRPOConfig, GRPOTrainer
tokenized_prompts = [tokenizer.apply_chat_template(prompt, tokenize=True, add_generation_prompt=True) 
                      for prompt in ds['prompt']]
exact_max_prompt_length = max([len(tokenized_prompt) for tokenized_prompt in tokenized_prompts])
max_prompt_length = 448  # manually adjusted
new_model_id="anakin87/qwen-scheduler-7b-grpo"
training_args = GRPOConfig(
    learning_rate = 8e-6,
    adam_beta1 = 0.9,
    adam_beta2 = 0.99,
    weight_decay = 0.1,
    warmup_ratio = 0.01,
    lr_scheduler_type = "cosine",
    optim = "paged_adamw_8bit",
    logging_steps = 1,
    per_device_train_batch_size = 8,
    gradient_accumulation_steps = 1,
    num_generations = 8, # Decrease if out of memory
    max_prompt_length = max_prompt_length,
    max_completion_length = max_seq_length - max_prompt_length,
    max_grad_norm = 0.1,
    output_dir = "outputs",
    overwrite_output_dir = True,
    push_to_hub = True,
    hub_model_id=new_model_id,
    hub_strategy="every_save",
    save_strategy="steps",
    save_steps=50,
    save_total_limit=1,
    num_train_epochs=3,
)
trainer = GRPOTrainer(
    model = model,
    processing_class = tokenizer,
    reward_funcs=[
        format_reward,
        sorted_events_reward,
        score_reward,
    ],
    args = training_args,
    train_dataset = ds,
)
trainer.train()
```

`<font style="color:rgb(0, 0, 0);">max_prompt_length </font>`<font style="color:rgb(0, 0, 0);">是提示的最大长度。过长的提示将被截断。我们可以轻松计算出这个值，然后手动调整。</font>

`<font style="color:rgb(0, 0, 0);">num_generations </font>`<font style="color:rgb(0, 0, 0);">是 GRPO 的一个关键参数，表示为每个提示生成的样本数量。</font>

<font style="color:rgb(0, 0, 0);">该算法通过比较不同的样本进行学习，并引导模型生成具有更高奖励的样本。</font>

<font style="color:rgb(0, 0, 0);">更多的样本为其提供了更多的学习信息，有可能带来更好的结果，但生成这些样本需要更多的时间和内存。</font>

:::color5
**<font style="color:#601BDE;">7.训练效果</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747206357210-fe357b01-c63c-42d7-ac5b-4f27dfda22a8.png)

<font style="color:rgb(0, 0, 0);">我们可以看到模型在训练过程中奖励有所提升。从一开始，样本在格式一致性方面就获得了不错的分数。</font>

<font style="color:rgb(0, 0, 0);">随着时间的推移，在遵循时间顺序以及日程安排方面获得良好分数的情况有所改善，这表明模型实际上学习到了奖励函数中规定的行为。</font>

<font style="color:rgb(0, 0, 0);">其他记录的指标，如 </font>`<font style="color:rgb(0, 0, 0);">reward_std</font>`<font style="color:rgb(0, 0, 0);">（奖励组内的平均标准差）和 KL 散度（模型与参考模型之间的平均 KL 散度），显示出可接受的值。</font>

:::color5
**<font style="color:#601BDE;">8.样本检查</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**简介：**<font style="color:rgb(25, 27, 31);">在训练过程中，我们记录生成样本的一个随机子集。你可以在</font>[此处](https://link.zhihu.com/?target=https%3A//huggingface.co/anakin87/qwen-scheduler-7b-grpo/raw/main/completion_samples.txt)<font style="color:rgb(25, 27, 31);">浏览完整日志。</font>

<font style="color:rgb(25, 27, 31);">查看这些生成情况既有趣又有启发性。正是通过这种方式，作者意识到较小的模型就是无法掌握：随着时间推移，它们的推理能力并没有显著提升。以下是在不同训练阶段针对相同输入提示的一个示例：</font>

```python
Events:
- Analyzing product performance (04:33 - 06:03)
- One-on-one with manager (08:41 - 08:56)
- Client call with Acme Corp (09:13 - 10:58)
- Meeting with Lisa at café (10:14 - 11:14)
- Updating website content (12:21 - 13:36)
- Preparing PTO handover (16:07 - 17:37)
- Marketing standup on Zoom (17:58 - 19:43)
- Brainstorming with Luke and Patrick (19:11 - 19:56)

Priorities:
- Analyzing product performance
- Meeting with Lisa at café
```

```python
<think>
The goal is to create a schedule that maximizes the sum of weighted event durations while respecting 
the chronological order, priorities, and non-overlapping constraints. Let\'s analyze the events and 
prioritize them:

1. **Analyzing product performance**: Start time: 04:33, End time: 06:03, Priority: 2
2. **One-on-one with manager**: Start time: 08:41, End time: 08:56, Priority: 1
3. **Client call with Acme Corp**: Start time: 09:13, End time: 10:58, Priority: 1
4. **Meeting with Lisa at café**: Start time: 10:14, End time: 11:14, Priority: 2
5. **Updating website content**: Start time: 12:21, End time: 13:36, Priority: 1
6. **Preparing PTO handover**: Start time: 16:07, End time: 17:37, Priority: 1
7. **Marketing standup on Zoom**: Start time: 17:58, End time: 19:43, Priority: 1
8. **Brainstorming with Luke and Patrick**: Start time: 19:11, End time: 19:56, Priority: 1

Given the priorities, we must ensure that "Analyzing product performance" and "Meeting with Lisa 
at café" are included. Let\'s try to fit the rest while avoiding overlaps:

1. **Analyzing product performance**: 04:33 - 06:03 (Priority 2)
2. **One-on-one with manager**: 08:41 - 08:56 (Priority 1)
3. **Client call with Acme Corp**: 09:13 - 10:58 (Priority 1)
4. **Meeting with Lisa at café**: 10:14 - 11:14 (Priority 2)
5. **Updating website content**: 12:21 - 13:36 (Priority 1)
6. **Preparing PTO handover**: 16:07 - 17:37 (Priority 1)

The next event, "Marketing standup on Zoom", starts at 17:58, but the availability is only until
 19:43. We can fit "Brainstorming with Luke and Patrick" from 19:11 to 19:56 before the standup.

1. **Analyzing product performance**: 04:33 - 06:03 (Priority 2)
2. **One-on-one with manager**: 08:41 - 08:56 (Priority 1)
3. **Client call with Acme Corp**: 09:13 - 10:58 (Priority 1)
4. **Meeting with Lisa at café**: 10:14 - 11:14 (Priority 2)
5. **Updating website content**: 12:21 - 13:36 (Priority 1)
6. **Preparing PTO handover**: 16:07 - 17:37 (Priority 1)
7. **Brainstorming with Luke and Patrick**: 19:11 - 19:56 (Priority 1)

Final schedule:
- Analyzing product performance: 04:33 - 06:03
- One-on-one with manager: 08:41 - 08:56
- Client call with Acme Corp: 09:13 - 10:58
- Meeting with Lisa at café: 10:14 - 11:14
- Updating website content: 12:21 - 13:36
- Preparing PTO handover: 16:07 - 17:37
- Brainstorming with Luke and Patrick: 19:11 - 19:56

This schedule respects the chronological order, includes the high-priority events, and avoids 
any overlaps.
</think>
<schedule>
<event>
<name>Analyzing product performance</name>
<start>04:33</start>
<end>06:03</end>
</event>
<event>
<name>One-on-one with manager</name>
<start>08:41</start>
<end>08:56</end>
</event>
<event>
<name>Client call with Acme Corp</name>
<start>09:13</start>
<end>10:58</end>
</event>
<event>
<name>Meeting with Lisa at café</name>
<start>10:14</start>
<end>11:14</end>
</event>
<event>
<name>Updating website content</name>
<start>12:21</start>
<end>13:36</end>
</event>
<event>
<name>Preparing PTO handover</name>
<start>16:07</start>
<end>17:37</end>
</event>
<event>
<name>Brainstorming with Luke and Patrick</name>
<start>19:11</start>
<end>19:56</end>
</event>
</schedule>
```

<font style="color:rgb(25, 27, 31);">在这个样本中，尽管推理过程很长，但模型在最终的日程安排中放入了两个重叠的事件。查看样本很不错，但我们需要系统的评估。</font>



# 评估
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了进行评估，我们可以使用事件调度数据集的测试集，模型之前从未见过该测试集。</font>

<font style="color:rgb(25, 27, 31);">我们将评估阶段分为两个步骤：</font>

+ <font style="color:rgb(25, 27, 31);">推理：为每个测试提示生成一个日程安排。</font>
+ <font style="color:rgb(25, 27, 31);">评分：根据我们的规则（格式正确、至少2个事件、仅存在的事件、按时间顺序、无重叠）检查每个生成的日程安排。如果违反任何规则，该日程安排在该提示下得分为0。如果有效，其得分是</font>`<font style="color:rgb(25, 27, 31);">(weighted_duration/optimal_weighted_duration) * 100</font>`<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">你可以在</font>[GitHub存储库](https://link.zhihu.com/?target=https%3A//github.com/anakin87/qwen-scheduler-grpo/tree/main/evaluation)<font style="color:rgb(25, 27, 31);">中找到这些脚本。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color5
**<font style="color:#601BDE;">1.效果对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在推理过程中出现了Unsloth错误。用Unsloth训练的模型无法可靠地转换为标准的Hugging Face Transformers模型；尝试这样做可能会得到一个不同的模型。这是一个</font>[已知问题](https://link.zhihu.com/?target=https%3A//github.com/unslothai/unsloth/issues/2009)<font style="color:rgb(25, 27, 31);">。如果在生产工作中需要这样做，比如说，用vLLM进行服务，这将是一个重大障碍，而且相当令人沮丧。</font>

<font style="color:rgb(25, 27, 31);">由于Unsloth对TRL进行了补丁，因此改编代码并使用TRL相当容易，而且TRL更稳定。只需注意，你将需要更多的GPU显存。</font>

<font style="color:rgb(25, 27, 31);">比较qwen-scheduler-7b-grpo（我们的模型）、Qwen2.5-Coder-7B-Instruct（原始模型）以及Qwen2.5-Coder-14B-Instruct（同一模型家族中更大的模型）。</font>

<font style="color:rgb(25, 27, 31);">由于样本表明模型在第2个epoch到第3个epoch之间可能变差了，作者还评估了第2个epoch结束时的检查点。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747206985452-9ea51391-2943-444b-8d46-6cd8962ba7c6.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747206994614-18e61154-b50a-4f5b-9350-6e421e361b87.png)

<font style="color:rgb(25, 27, 31);">从以上对比可以看出：</font>

+ <font style="color:rgb(25, 27, 31);">GRPO肯定起作用了！它在引导模型产生期望行为方面相当有效。</font>
+ <font style="color:rgb(25, 27, 31);">经过调优的模型在这项任务中的表现甚至超过了规模是其两倍的模型。</font>
+ <font style="color:rgb(25, 27, 31);">该模型几乎完美地学会了格式、时间顺序，并且只使用现有事件。</font>
+ <font style="color:rgb(25, 27, 31);">该模型在处理重叠问题上仍有困难，这在测试集中很大一部分样本中都很明显。</font>



# 改进
:::color3
**<font style="color:rgb(25, 27, 31);">简介：</font>**<font style="color:rgb(25, 27, 31);">主要问题肯定是重叠现象。我们可以看到，模型并没有有效地学会避免这些重叠。此外，在第3个训练周期中出现的轻微性能下降，可能表明模型正在学习一种并非最优的策略。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color5
**<font style="color:#601BDE;">1.奖励函数的思路：</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">• 更强的重叠惩罚：在score_reward函数中，从分数计算中剔除重叠事件。我们可以实施更严厉的惩罚...</font>

<font style="color:rgb(25, 27, 31);">• 专门的重叠奖励：或者，添加一个仅检查重叠情况的奖励函数。</font>

<font style="color:rgb(25, 27, 31);">奖励函数默认是累加的，因此，根据对惩罚的设计方式，这两种不同的方法在数学上可能是等效的。</font>



# 总结
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">在本文中，详细介绍了如何使用GRPO在一项新的可验证任务上对语言模型进行后训练：根据一系列事件和优先级创建日程安排。</font>

<font style="color:rgb(25, 27, 31);">涵盖了问题定义、数据集生成、基础模型选择、奖励函数设计、使用Unsloth进行训练以及评估等方面。通过实际操作，对GRPO以及在大语言模型中应用强化学习有了一些认识。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color5
**<font style="color:#601BDE;">1.对于可验证任务，GRPO非常出色</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">它简化了典型的强化学习设置（例如在PPO中使用的设置）：无需价值模型；奖励模型通常被确定性奖励函数所取代（具有可验证奖励的强化学习）。由于数据集只需要提示（无需生成内容），数据收集比监督微调（SFT）要容易得多，成本也低得多。</font>

:::color5
**<font style="color:#601BDE;">2.启发模型行为</font>**

:::

<font style="color:rgb(25, 27, 31);">使用GRPO及类似算法进行启发，更多是从训练好的模型中引出期望的行为，而非向其教授全新的内容。如果你需要从根本上获得新技能，指令微调（以及蒸馏）可能会更有效。</font>

:::color5
**<font style="color:#601BDE;">3.基础模型很重要</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">如果在采样过程中，基础模型在任务上从未表现出有前景的行为，那么GRPO可能对你的问题无效。你可能首先需要一个更大或更好的基础模型。</font>

:::color5
**<font style="color:#601BDE;">4.“顿悟时刻”可能被过度炒作了</font>**

:::

<font style="color:rgb(25, 27, 31);">在DeepSeek-R1论文中，作者表明，在GRPO过程中，“模型学会以拟人化的语气进行反思”。这是奇迹吗？最近的研究表明，基础模型也有类似的行为。</font>

:::color5
**<font style="color:#601BDE;">5.奖励函数的设计至关重要</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">奖励应该体现目标，提供一个可学习的信号（对模型的一种激励），并且要具有稳健性。如果它们不稳健，你可能会遇到奖励作弊的情况：模型找到捷径来最大化奖励，而实际上并没有解决你心中所想的问题。</font>

:::color5
**<font style="color:#601BDE;">6.Unsloth：对节省GPU资源很有用，但要注意</font>**

:::

<font style="color:rgb(25, 27, 31);">如果你没有太多的GPU资源，或者处于实验阶段，Unsloth可能会有帮助。这些人在GPU效率方面做出了令人印象深刻的成果。然而，目前这个库存在难以解决的漏洞，这使得它不适合用于严肃的应用场景。如果你有足够的显存，TRL会更稳定。</font>





# 参考文献
+ <font style="color:rgb(25, 27, 31);">Qwen Scheduler GRPO</font>
    - [<u>GitHub repository</u>](https://link.zhihu.com/?target=https%3A//github.com/anakin87/qwen-scheduler-grpo)<font style="color:rgb(25, 27, 31);">: 在这里可以找到用于该实验的所有代码.</font>
    - [<u>Hugging Face collection</u>](https://link.zhihu.com/?target=https%3A//huggingface.co/collections/anakin87/qwen-scheduler-grpo-680bcc583e817390525a8837)<font style="color:rgb(25, 27, 31);">: 数据集和模型.</font>
+ <font style="color:rgb(25, 27, 31);">GRPO 论文和资源</font>
    - [<u>DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models</u>](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2402.03300)
    - [<u>Hugging Face Reasoning Course</u>](https://link.zhihu.com/?target=https%3A//huggingface.co/learn/llm-course/en/chapter12)
    - [<u>DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning</u>](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2501.12948v1)
    - [<u>There May Not be Aha Moment in R1-Zero-like Training — A Pilot Study</u>](https://link.zhihu.com/?target=https%3A//oatllm.notion.site/oat-zero)
    - [<u>Understanding R1-Zero-Like Training: A Critical Perspective</u>](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2503.20783)
    - [<u>Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?</u>](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2504.13837)
    - [<u>Interconnects blog by Nathan Lambert</u>](https://link.zhihu.com/?target=https%3A//www.interconnects.ai/)
+ <font style="color:rgb(25, 27, 31);">Practical resources  
</font>
    - [<u>GRPO TRL docs</u>](https://link.zhihu.com/?target=https%3A//huggingface.co/docs/trl/main/en/grpo_trainer)
    - [<u>GRPO learning from GSM8K with TRL - by William Brown</u>](https://link.zhihu.com/?target=https%3A//gist.github.com/willccbb/4676755236bb08cab5f4e54a0475d6fb)
    - [<u>GRPO Unsloth docs</u>](https://link.zhihu.com/?target=https%3A//docs.unsloth.ai/basics/reasoning-grpo-and-rl)



