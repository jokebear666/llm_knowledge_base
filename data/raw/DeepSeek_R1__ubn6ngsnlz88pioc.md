# DeepSeek R1

<!-- source: yuque://zhongxian-iiot9/hlyypb/ubn6ngsnlz88pioc -->

R1-zero 虽然涌现出了强大的思考能力，但其思考过程可读性差，不适合直接面向用户。R1 的目标是在 R1-zero 的基础上，实现用户友好、推理增强以及更好的通用能力。

#### 阶段一：推理能力强化（Reasoning Focus）
本阶段主要在 Code、Math、Science、Logic Reasoning 等有明确解答方案、可计算 Rule-based Reward 的任务上训练。

##### 1. Cold Start（冷启动）
构造并收集少量长 CoT 数据微调模型，作为 RL 的起点。主要采集方式如下（文章指出 CoT 的 Reasoning Pattern 至关重要）：

+ Few-shot Prompting：构建 CoT 的 Few-shot prompt 作为 Seed Data，引导模型生成带反思和验证的长 CoT。
+ 直接蒸馏：蒸馏 DeepSeek-R1-Zero 的输出。为了保证可读性，在 Prompt 中加入 Summary 过程：`|special_token|<reasoning_process>|special_token|<summary>`，并进行人工过滤。
+ 人工后处理：通过人工润色问题的解答过程，构建高质量长 CoT 数据。

##### 2. R1-zero 范式的 RL 训练
对 Cold-start 后的模型进行 RL 自探索。

+ 改进点：引入语言一致性 Reward（Language Consistency Reward）。计算 CoT 思考过程中目标语言单词的比例，解决 R1-zero 思考过程语言混合的问题（虽然会导致轻微掉点）。

#### 阶段二：通用能力提升（General Focus）
##### 1. SFT（监督微调）
利用第一阶段得到的模型，对其他难以计算 Rule Reward 的数据进行拒绝采样（Rejection Sampling），构建长 CoT 数据。

+ 评估方式：将 GT 和模型生成的回复输入 Deepseek V3，由 V3 判别答案正确性。
+ 过滤规则：保留正确答案，并预先过滤掉语言混合、含代码块、长括号等格式错误的思考过程。
+ 数据构成：
    - Reasoning 数据：约 600k 条。
    - Non-reasoning 数据：约 200k 条。部分复用 V3 数据，部分通过 Prompt 让 V3 生成长 CoT。对于简单问题，直接抛弃长 CoT。

##### 2. RL（强化学习）
+ Reasoning 数据：直接采用 Rule-based Reward。
+ 非 Reasoning 数据：采用 Generative Model-based Reward。
+ 策略：不同 Domain 采用不同的 Training Prompt，继续使用 GRPO 训练。

> 小结：R1 的每一步调整均基于上一步模型，且能采用 CoT 的环节都尽可能采用了 CoT。
>

