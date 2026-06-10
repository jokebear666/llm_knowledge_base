# ⓼ prompt/COT

<!-- source: yuque://zhongxian-iiot9/hlyypb/nzo9u42bk1vmf7pg -->

# Prompt Engineering
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Prompt Engineering（提示工程）是通过设计优化输入文本（prompt）来引导大模型生成预期输出的技术。其核心原理基于大语言模型的两个关键特性：</font>

1. **模式匹配与概率预测**：
    - <font style="color:rgb(51, 51, 51);">模型基于海量文本的统计规律，通过Transformer架构捕捉文本模式</font>
    - <font style="color:rgb(51, 51, 51);">输出是计算下一个token的条件概率分布：</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739957835476-24f3b654-ee6d-4ad7-b53f-8e78bdd7acbe.png)
2. **上下文学习（In-context Learning）**：
    - <font style="color:rgb(51, 51, 51);">模型可通过提示中的示例/指令激活特定推理能力</font>
    - <font style="color:rgb(51, 51, 51);">零样本（Zero-shot）与少样本（Few-shot）学习的基础</font>
3. **注意力机制驱动**：通过设计prompt引导模型关注特定语义空间

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739957845854-8c9040c1-9c6a-48ce-af97-c941abf36090.png)

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **目标定义**
    - <font style="color:rgb(51, 51, 51);">明确任务类型（分类/生成/推理等）</font>
    - <font style="color:rgb(51, 51, 51);">确定评估指标（准确率、BLEU等）</font>
2. **提示模板设计**

```plain
# 示例模板
prompt_template = """
请完成以下情感分析任务（积极/消极）：
示例1：
输入：这款手机续航惊人
输出：积极

示例2：
输入：系统频繁卡顿
输出：消极

现在请分析：
输入：{user_input}
输出：
"""
```

3. **生成与评估**
    - <font style="color:rgb(51, 51, 51);">采样策略：temperature=0.7, top_p=0.9</font>
    - <font style="color:rgb(51, 51, 51);">评估输出质量：人工评估 + 自动指标</font>
4. **迭代优化**
    - <font style="color:rgb(51, 51, 51);">分析错误案例</font>
    - <font style="color:rgb(51, 51, 51);">调整提示结构/示例/指令</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优势</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">无训练成本：无需调整模型参数</font>
+ <font style="color:rgb(51, 51, 51);">即时生效：修改prompt可实时观察效果</font>
+ <font style="color:rgb(51, 51, 51);">可解释性强：人工可理解的优化过程</font>

**<font style="color:rgb(51, 51, 51);">局限</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">性能天花板：受限于模型原始能力</font>
+ <font style="color:rgb(51, 51, 51);">稳定性挑战：微小提示变化可能导致输出波动</font>
+ <font style="color:rgb(51, 51, 51);">复杂任务处理困难：多跳推理等任务效果受限</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

| <font style="color:rgb(51, 51, 51);">场景类型</font> | <font style="color:rgb(51, 51, 51);">示例</font> | <font style="color:rgb(51, 51, 51);">提示设计要点</font> |
| :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">文本生成</font> | <font style="color:rgb(51, 51, 51);">故事创作、邮件撰写</font> | <font style="color:rgb(51, 51, 51);">明确风格和结构要求</font> |
| <font style="color:rgb(51, 51, 51);">信息抽取</font> | <font style="color:rgb(51, 51, 51);">实体识别、关系提取</font> | <font style="color:rgb(51, 51, 51);">提供清晰输出格式示例</font> |
| <font style="color:rgb(51, 51, 51);">代码生成</font> | <font style="color:rgb(51, 51, 51);">Python函数生成、SQL查询</font> | <font style="color:rgb(51, 51, 51);">指定输入输出示例</font> |
| <font style="color:rgb(51, 51, 51);">复杂推理</font> | <font style="color:rgb(51, 51, 51);">数学解题、逻辑推理</font> | <font style="color:rgb(51, 51, 51);">分步思考链（Chain-of-Thought）</font> |
| <font style="color:rgb(51, 51, 51);">多模态任务</font> | <font style="color:rgb(51, 51, 51);">图文生成、视觉问答</font> | <font style="color:rgb(51, 51, 51);">跨模态对齐描述</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **结构化模板**

```plain
def create_prompt(context, examples):
    return f"""基于以下知识：
    {context}
    
    参考示例：
    {examples}
    
    请回答："""
```

2. **动态提示**

```python
def dynamic_prompt(query, history):
    history_str = "\n".join(history[-3:])
    return f"对话历史：{history_str}\n当前问题：{query}\n回答："
```

3. **元提示优化**

```plain
meta_prompt = """
你是一个提示优化专家，请帮我改进以下提示：
原始提示：{original_prompt}
改进目标：{improvement_goal}
建议的优化方案："""
```

4. **混合方法**
    - <font style="color:rgb(51, 51, 51);">结合检索增强（Retrieval-Augmented）</font>
    - <font style="color:rgb(51, 51, 51);">集成外部知识库</font>
    - <font style="color:rgb(51, 51, 51);">多模型协作提示</font>
5. **自动提示优化**
    - <font style="color:rgb(51, 51, 51);">AutoPrompt：基于梯度搜索最优提示词</font>
    - <font style="color:rgb(51, 51, 51);">遗传算法优化提示序列</font>
6. **多模态提示**

```plain
multimodal_prompt = """
[图像描述：一只棕熊在河边捕鱼]
根据图片内容回答：
问题：熊在什么环境中活动？
答案：
"""
```

7. **认知架构集成**
    - <font style="color:rgb(51, 51, 51);">结合思维树（Tree of Thoughts）</font>
    - <font style="color:rgb(51, 51, 51);">实现自我验证推理</font>
8. **安全增强设计**
    - <font style="color:rgb(51, 51, 51);">防御提示注入攻击</font>
    - <font style="color:rgb(51, 51, 51);">添加伦理约束指令</font>



# Prompt评估
:::color3
**<font style="color:#ED740C;">简介</font>**：评估Prompt的好坏需要一个全面和多维度的方法，结合自动评估指标、人工评估和用户反馈等多种手段。选择合适的评估方法和技术，能够有效提升Prompt的质量和生成效果，进而提高模型的整体性能和应用体验。通过不断优化和改进Prompt设计，可以实现更自然、更准确、更有效的自然语言。

:::

## 评估指标
:::color5
**<font style="color:#601BDE;">1.评估指标</font>**

:::

**<font style="color:rgb(51, 51, 51);">1.1 相关性（Relevance）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成内容是否与用户意图和任务需求紧密相关。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>[评估](https://www.yuque.com/zhongxian-iiot9/gi3w2u/nlapi8xm5fmsnx3g)
    - **<font style="color:rgb(51, 51, 51);">ROUGE-N</font>**<font style="color:rgb(51, 51, 51);">（N-gram重叠率）：衡量生成文本与参考文本的词汇匹配度。</font>
    - **<font style="color:rgb(51, 51, 51);">BLEU</font>**<font style="color:rgb(51, 51, 51);">（双语评估研究指标）：常用于翻译任务，但也可用于评估生成文本与参考文本的相似性。</font>
    - **<font style="color:rgb(51, 51, 51);">BERTScore</font>**<font style="color:rgb(51, 51, 51);">：基于BERT的语义相似度计算，捕捉语义相关性而非字面匹配。</font>
    - **<font style="color:rgb(51, 51, 51);">人工评分</font>**<font style="color:rgb(51, 51, 51);">：通过人工判断生成内容是否符合主题（如1-5分评分）。</font>

**<font style="color:rgb(51, 51, 51);">1.2 准确性（Accuracy）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成信息的正确性和事实一致性。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Factual Accuracy</font>**<font style="color:rgb(51, 51, 51);">：通过外部知识库（如维基百科）验证生成内容的正确性。</font>
    - **<font style="color:rgb(51, 51, 51);">错误检测率</font>**<font style="color:rgb(51, 51, 51);">（Error Detection Rate）：统计生成内容中的明显事实错误或逻辑矛盾。</font>
    - **<font style="color:rgb(51, 51, 51);">专家评审</font>**<font style="color:rgb(51, 51, 51);">：由领域专家对技术性内容的准确性进行评分。</font>

**<font style="color:rgb(51, 51, 51);">1.3 多样性（Diversity）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成内容的丰富程度，避免重复或模板化。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">Distinct-N</font>**<font style="color:rgb(51, 51, 51);">：统计生成文本中不同n-gram的比例（如Distinct-1/2/3）。</font>
    - **<font style="color:rgb(51, 51, 51);">熵（Entropy）</font>**<font style="color:rgb(51, 51, 51);">：词汇分布的熵值越高，多样性越好。</font>
    - **<font style="color:rgb(51, 51, 51);">重复率（Repetition Rate）</font>**<font style="color:rgb(51, 51, 51);">：重复短语或句子的比例。</font>

**<font style="color:rgb(51, 51, 51);">1.4 效率（Efficiency）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：模型生成结果所需的计算资源和时间消耗。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">响应时间</font>**<font style="color:rgb(51, 51, 51);">（Latency）：从输入prompt到生成完整输出的耗时。</font>
    - **<font style="color:rgb(51, 51, 51);">Token数量</font>**<font style="color:rgb(51, 51, 51);">：生成内容的长度是否合理（过短可能信息不足，过长可能冗余）。</font>

**<font style="color:rgb(51, 51, 51);">1.5 鲁棒性（Robustness）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：对prompt微小变化的敏感度，能否稳定生成高质量结果。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">扰动测试</font>**<font style="color:rgb(51, 51, 51);">：对prompt进行同义词替换、语序调整等扰动后，统计输出一致性的变化。</font>
    - **<font style="color:rgb(51, 51, 51);">对抗性测试</font>**<font style="color:rgb(51, 51, 51);">：故意输入模糊或矛盾的prompt，观察模型能否合理应对。</font>

**<font style="color:rgb(51, 51, 51);">1.6 一致性（Consistency）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：在多轮对话或复杂任务中保持逻辑连贯，避免前后矛盾。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">自洽性检查</font>**<font style="color:rgb(51, 51, 51);">（Self-Consistency）：多次运行相同prompt，对比输出的核心观点是否一致。</font>
    - **<font style="color:rgb(51, 51, 51);">逻辑链验证</font>**<font style="color:rgb(51, 51, 51);">：对推理类任务（如数学问题）验证生成步骤的逻辑正确性。</font>

**<font style="color:rgb(51, 51, 51);">1.7 用户体验（User Experience）</font>**

+ **<font style="color:rgb(51, 51, 51);">定义</font>**<font style="color:rgb(51, 51, 51);">：生成结果是否符合用户个性化需求，包括语气、风格等。</font>
+ **<font style="color:rgb(51, 51, 51);">指标</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">用户满意度调查</font>**<font style="color:rgb(51, 51, 51);">：通过问卷或评分收集用户主观反馈。</font>
    - **<font style="color:rgb(51, 51, 51);">任务完成率</font>**<font style="color:rgb(51, 51, 51);">（Task Success Rate）：例如在客服场景中是否成功解决用户问题。</font>

## 评估方法
### 人工评估
:::color5
**<font style="color:#601BDE;">1.人工评估</font>**

:::

**定义**：人工评估是通过人工方式对模型输出的Prompt效果进行评估，是最为直接和主观的评估方法。

+ **优点**：能够捕捉到复杂的语言理解和生成能力，评估结果更为全面和准确。
+ **缺点**：耗时且成本高，结果可能受到评估者的主观影响。
+ **实施步骤**：
    1. **选择评估人员**：确保评估人员具备相关的专业知识和技能。
    2. **设计评估标准**：明确评估的维度，如准确性、相关性、流畅性等。
    3. **收集输出样本**：从模型中获取一定数量的Prompt输出。
    4. **评估与打分**：根据标准对每个Prompt进行评分。
    5. **分析结果**：汇总评分数据，找出问题和改进方向。

### 基于LLM的评估
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>利用LLM和指标对Prompt进行评估，是一种高效且客观的评估方式。

:::

:::color5
**<font style="color:#601BDE;">1.目标</font>**

:::

**<font style="color:rgb(51, 51, 51);">任务目标</font>**<font style="color:rgb(51, 51, 51);">：使用Qwen模型为电商商品生成吸引人的卖点文案。  
</font>**<font style="color:rgb(51, 51, 51);">示例商品</font>**<font style="color:rgb(51, 51, 51);">：无线蓝牙耳机  
</font>**<font style="color:rgb(51, 51, 51);">初始Prompt</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
你是一个电商文案专家，请为[无线蓝牙耳机]生成5条卖点，要求突出产品优势，语言简洁有力。
```

:::color5
**<font style="color:#601BDE;">2.评估流程</font>**

:::

<font style="color:rgb(51, 51, 51);">1. 评估目标</font>

+ **<font style="color:rgb(51, 51, 51);">核心指标</font>**<font style="color:rgb(51, 51, 51);">：相关性、吸引力、多样性、准确性、品牌调性。</font>
+ **<font style="color:rgb(51, 51, 51);">评估方式</font>**<font style="color:rgb(51, 51, 51);">：LLM自动评分 + 人工校验。</font>

<font style="color:rgb(51, 51, 51);">2. 整体流程</font>

```plain
生成候选文案 → LLM自动评分 → 人工抽检 → 统计指标 → 优化Prompt → 重复迭代
```

:::color5
**<font style="color:#601BDE;">3.评估方法1：</font>****<font style="color:#601BDE;">LLM作为评分器（自动评估）</font>**

:::

**<font style="color:rgb(51, 51, 51);">步骤</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">生成候选文案</font>**<font style="color:rgb(51, 51, 51);">：用待评估的prompt生成N条卖点（如N=20）。</font>
2. **<font style="color:rgb(51, 51, 51);">设计评分指令</font>**<font style="color:rgb(51, 51, 51);">：要求LLM（Qwen/GPT-4）从多维度打分。</font>
3. **<font style="color:rgb(51, 51, 51);">解析评分结果</font>**<font style="color:rgb(51, 51, 51);">：提取分数并统计平均分、方差等。</font>

<font style="color:rgb(51, 51, 51);">评分Prompt示例：</font>

```python
score_prompt = """
你是一个专业的电商文案评估AI，请根据以下标准为每条卖点打分（1-5分）：
1. **相关性**：是否准确描述产品真实功能（如续航、音质）。
2. **吸引力**：是否具有感染力，能激发购买欲望。
3. **多样性**：是否与其他卖点角度重复（技术/场景/人群）。

请严格按此JSON格式输出结果，仅返回JSON：
{
  "卖点1": {"相关性": 分数, "吸引力": 分数, "多样性": 分数},
  "卖点2": { ... }
}

待评估卖点：
{卖点列表}
"""
```

<font style="color:rgb(51, 51, 51);">代码实现（Python+Qwen）：</font>

```python
import json
from qwen_agent import QwenAgent

def evaluate_with_llm(prompts):
    agent = QwenAgent(api_key='your_api_key')
    response = agent.generate(
        prompt=score_prompt.format(卖点列表=prompts),
        temperature=0.1  # 降低随机性
    )
    try:
        scores = json.loads(response)
        return scores
    except:
        return {}  # 异常处理

# 示例输出
scores = {
    "超长续航50小时，告别频繁充电": {"相关性": 5, "吸引力": 4, "多样性": 2},
    "蓝牙5.3稳定连接，游戏无延迟": {"相关性": 5, "吸引力": 3, "多样性": 3}
}
```

:::color5
**<font style="color:#601BDE;">4.评估方法2：</font>****<font style="color:#601BDE;">LLM作为对比器（AB测试）</font>**

:::

**<font style="color:rgb(51, 51, 51);">用途</font>**<font style="color:rgb(51, 51, 51);">：比较不同prompt生成的文案质量。  
</font>**<font style="color:rgb(51, 51, 51);">Prompt设计</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
请判断以下两组卖点文案哪组更优，并给出理由：
- 组A（Prompt1生成）：{卖点列表A}
- 组B（Prompt2生成）：{卖点列表B}

评估标准：
1. 整体吸引力 2. 信息准确性 3. 角度多样性

输出格式：
{
  "winner": "A/B",
  "reason": "具体原因..."
}
```

:::color5
**<font style="color:#601BDE;">5.评估方法3：</font>****<font style="color:#601BDE;">LLM生成改写建议</font>**

:::

**<font style="color:rgb(51, 51, 51);">用途</font>**<font style="color:rgb(51, 51, 51);">：自动诊断prompt问题并给出优化方向。  
</font>**<font style="color:rgb(51, 51, 51);">Prompt设计</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
以下是一组针对无线蓝牙耳机的卖点文案：
{卖点列表}

请分析这些文案的不足，并从以下维度提出prompt改进建议：
1. 指令明确性 2. 示例补充 3. 约束条件

输出格式：
{
  "不足": ["问题1", "问题2"],
  "建议": ["建议1", "建议2"]
}
```

:::color5
**<font style="color:#601BDE;">6.评估指标计算</font>**

:::

**<font style="color:rgb(51, 51, 51);">1. 自动指标</font>**

```python
def calculate_metrics(scores):
    relevance = np.mean([v["相关性"] for v in scores.values()])
    attractiveness = np.mean([v["吸引力"] for v in scores.values()])
    diversity = np.mean([v["多样性"] for v in scores.values()])
    return {
        "相关性": round(relevance, 2),
        "吸引力": round(attractiveness, 2),
        "多样性": round(diversity, 2)
    }

# 示例结果：{"相关性": 4.8, "吸引力": 3.5, "多样性": 2.9}

```

**<font style="color:rgb(51, 51, 51);">2. 人工校验指标</font>**

+ **<font style="color:rgb(51, 51, 51);">准确性校验</font>**<font style="color:rgb(51, 51, 51);">：抽取10%的文案核对产品参数（如实际续航是否为20小时）。</font>
+ **<font style="color:rgb(51, 51, 51);">品牌调性匹配</font>**<font style="color:rgb(51, 51, 51);">：由运营人员标注是否符合品牌风格（是/否）。</font>

:::color5
**<font style="color:#601BDE;">7.案例</font>**

:::

<font style="color:rgb(51, 51, 51);">初始Prompt的问题诊断</font>

+ **<font style="color:rgb(51, 51, 51);">LLM生成的改进建议</font>**<font style="color:rgb(51, 51, 51);">：</font>

```json
{
  "不足": ["缺乏生成角度指导", "未限制抽象词汇"],
  "建议": ["添加技术/场景/人群的多角度要求", "禁止使用‘高性能’等模糊表述"]
}
```

<font style="color:rgb(51, 51, 51);">优化后的Prompt</font>

```plain
你是一名资深电商文案专家，请为[无线蓝牙耳机]生成5条卖点：
1. 必须覆盖以下角度：
   - 技术参数（如蓝牙版本、续航）
   - 使用场景（如通勤、运动）
   - 人群痛点（如戴久不痛）
2. 语言风格：年轻化，可使用感叹句/网络用语
3. 禁止使用以下词汇：高性能、高品质、卓越

参考示例：
1. “开盖即连！地铁追剧再不怕错过站~”
2. “狂甩不掉！健身房的隐形BGM神器”
```

<font style="color:rgb(51, 51, 51);">优化前后对比</font>

| **指标** | **优化前** | **优化后** |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">平均相关性</font> | <font style="color:rgb(51, 51, 51);">4.2</font> | <font style="color:rgb(51, 51, 51);">4.8</font> |
| <font style="color:rgb(51, 51, 51);">平均吸引力</font> | <font style="color:rgb(51, 51, 51);">3.1</font> | <font style="color:rgb(51, 51, 51);">4.3</font> |
| <font style="color:rgb(51, 51, 51);">多样性</font> | <font style="color:rgb(51, 51, 51);">2.4</font> | <font style="color:rgb(51, 51, 51);">4.1</font> |
| <font style="color:rgb(51, 51, 51);">品牌调性符合率</font> | <font style="color:rgb(51, 51, 51);">60%</font> | <font style="color:rgb(51, 51, 51);">90%</font> |


:::color5
**<font style="color:#601BDE;">8.常见问题与解法</font>**

:::

1. **LLM评分偏差**
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：LLM可能高估技术术语的吸引力。</font>
    - **<font style="color:rgb(51, 51, 51);">解法</font>**<font style="color:rgb(51, 51, 51);">：在评分prompt中加入人工标注的示例（Few-shot Learning）。</font>
2. **多样性计算不准**
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：仅依赖LLM主观评分可能不准。</font>
    - **<font style="color:rgb(51, 51, 51);">解法</font>**<font style="color:rgb(51, 51, 51);">：结合CLIP计算文案-场景匹配度，或使用Sentence-BERT计算语义相似度。</font>
3. **评估成本高**
    - **<font style="color:rgb(51, 51, 51);">问题</font>**<font style="color:rgb(51, 51, 51);">：评估大量文案时API成本上升。</font>
    - **<font style="color:rgb(51, 51, 51);">解法</font>**<font style="color:rgb(51, 51, 51);">：先用小模型（如Qwen-1.8B）初筛，再用大模型精评。</font>

# prompt优化
## <font style="color:rgba(0, 0, 0, 0.9);">GRAD-SUM：用梯度汇总优化你的提示词</font>
:::color3
**<font style="color:#ED740C;">简介</font>**：<font style="color:rgb(0, 0, 0);">GRAD-SUM的核心思想是将gradient-based优化技术与自然语言处理相结合。它不仅可以自动优化prompt，还能根据用户定义的任务描述和评估标准进行个性化调整。GRAD-SUM引入了一个全新的</font>**<font style="color:#ED740C;">gradient summarization</font>**<font style="color:rgb(0, 0, 0);">模块。这个模块能够有效地概括和综合多个反馈，从而生成更加通用和强大的prompt。为了验证梯度汇总模块的效果，研究团队进行了消融实验。结果显示，引入梯度汇总模块平均提升了5%的性能。这证明了该模块在提高prompt泛化能力方面的关键作用。</font>

**<font style="color:#ED740C;">paper </font>**<font style="color:rgb(0, 0, 0);">: </font>[https://arxiv.org/pdf/2407.12865v1](https://arxiv.org/pdf/2407.12865v1)   [GRAD-SUM](https://mp.weixin.qq.com/s/hpp24EkbrPJpA-pTb7_Ndw)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1739848343439-2d22a9ee-35b9-492e-b230-310ab87fb6f0.png)

:::color5
**<font style="color:#601BDE;">实现步骤</font>**

:::

**<font style="color:rgb(0, 0, 0);">1. 生成模块：构建基础</font>**

<font style="color:rgb(0, 0, 0);">生成模块需要三个关键元素：数据集、prompt和用于生成输出的LLM。这个模块的作用是根据给定的prompt和数据集生成初始响应。</font>

**<font style="color:rgb(0, 0, 0);">2. 评估模块：智能判断</font>**

<font style="color:rgb(0, 0, 0);">评估模块接收生成的响应，并根据用户定义的评估标准进行评分。这里的一个创新点是使用LLM作为评判器，这使得GRAD-SUM能够适应各种复杂的评估场景。</font>

**<font style="color:rgb(0, 0, 0);">3. 梯度生成模块：精准反馈</font>**

<font style="color:rgb(0, 0, 0);">梯度生成模块分析评估结果，并为每个未达到满分的响应生成改进建议。这些建议就像是传统机器学习中的"梯度"，指导着prompt的优化方向。</font>

**<font style="color:rgb(0, 0, 0);">4. 梯度汇总模块：智慧凝练</font>**

<font style="color:rgb(0, 0, 0);">这是GRAD-SUM最独特的创新。梯度汇总模块将所有单独的改进建议综合成一个统一的、通用的优化方向。这确保了优化后的prompt不会过度拟合某些特定样本，而是能够在整个数据集上表现良好。</font><font style="color:rgb(0, 0, 0);">以往的方法，如</font><font style="color:rgb(0, 0, 0);">(Pryzant et al.</font><font style="color:rgb(0, 0, 0);">，</font><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">2023)</font><font style="color:rgb(0, 0, 0);">提出的技术，往往是基于单个输出的反馈来生成新的</font><font style="color:rgb(0, 0, 0);">prompt</font><font style="color:rgb(0, 0, 0);">。这种方法容易导致生成的</font><font style="color:rgb(0, 0, 0);">prompt</font><font style="color:rgb(0, 0, 0);">过于特定，难以泛化到整个数据集。</font>

**<font style="color:rgb(0, 0, 0);">5. Prompt编辑模块：精准优化</font>**

<font style="color:rgb(0, 0, 0);">最后，prompt编辑模块根据汇总的梯度信息生成新的candidate prompts。这个过程使用了beam search技术，保留了多个潜在的优化方向，进一步提高了优化的效果。</font>



```python
#优化前
你需要解决一个问题。以下是问题：{question}

#优化后
你需要解决一个小学数学问题。请按照以下详细步骤，确保解答清晰准确：
1. 确定数学运算：首先确定所需的数学运算类型（例如，加法、减法、乘法、除法）。在你的回答中明确指出这一点，并解释为什么这个问题需要这种运算。
2. 概述思路：提供一个逻辑且结构化的方法来解决问题。详细解释你的推理过程，就像你在教学生这个概念一样。确保每一步都与前一步相连，逻辑清晰，易于理解。
3. 步骤计算：将问题分解为较小的、可管理的步骤。详细展示每一步的计算过程，说明你是如何得出解答的。包括所有的中间步骤和结果，以提供全面的理解。
4. 验证准确性：在得到答案后，重新检查你的计算和最终数值答案，以确保其准确性。解释你是如何验证答案正确性的，例如使用反向运算或通过另一种方法检查。
5. 最终答案：以清晰准确的方式呈现最终答案，确保易于理解。明确指出答案已经过验证，确保准确无误。
以下是问题：{question}
```



:::color5
**<font style="color:#601BDE;">优点</font>**

:::

1. <font style="color:rgb(0, 0, 0);">高度灵活：适用于各种任务和场景</font>
2. <font style="color:rgb(0, 0, 0);">成本效益：优化过程高效，节省时间和资源</font>
3. <font style="color:rgb(0, 0, 0);">性能卓越：在多个基准测试中consistently优于现有方法</font>
4. <font style="color:rgb(0, 0, 0);">易于使用：只需提供任务描述和评估标准，无需复杂设置</font>
5. <font style="color:rgba(0, 0, 0, 0.9);">泛化能力：生成的新prompt能够更好地适应整个数据集，而不仅仅是某些特定样本。</font>



```python
from openai import OpenAI
import re
import time

def optimize_prompt(initial_prompt, task_description, evaluation_criteria):
    """GRAD-SUM优化流程"""
    current_prompts = [initial_prompt]
    best_score = 0
    best_prompt = initial_prompt
    
    for iteration in range(MAX_ITERATIONS):
        print(f"\nIteration {iteration + 1}")
        all_candidates = []
        for prompt in current_prompts:
            candidates = generate_candidates(prompt, task_description)
            all_candidates.extend(candidates)
        
        # 评估所有候选prompts
        evaluated_candidates = [(candidate, evaluate_prompt(candidate, evaluation_criteria)) for candidate in all_candidates]
```



## <font style="color:rgb(51, 51, 51);">AutoPrompt：基于梯度搜索最优提示词</font>


# CoT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">但对于复杂的任务，如数学问题、编程或逻辑推理，仅仅得到一个“首选”的最终答案是不够的。我们希望 LLM 也能正确推理，展示它的“思考过程”。</font>

<font style="color:rgb(25, 27, 31);">这就是链式思考（Chain-of-Thought, </font>[<font style="color:rgb(9, 64, 142);">CoT</font>](https://zhida.zhihu.com/search?content_id=254489057&content_type=Article&match_order=1&q=CoT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）推理的作用！</font>**<font style="color:#ED740C;">可以将其视为要求 LLM 在给出最终答案之前“展示它的解题步骤”</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742962850618-2fbe627f-7946-4bd2-9598-0f52c1bbdc90.png)

:::color5
**<font style="color:#601BDE;">1.示例</font>**

:::

```python
“如果一辆火车以 60 英里/小时的速度行驶 2 小时，它行驶了多远？”
```

```python
<thought> 
步骤 1：确定公式：距离 = 速度 × 时间  
步骤 2：从问题中提取速度：速度 = 60 英里/小时  
步骤 3：从问题中提取时间：时间 = 2 小时  
步骤 4：计算距离：距离 = 60 英里/小时 × 2 小时 = 120 英里  
</thought>  
<answer>  
120 英里  
</answer>
```

:::color5
**<font style="color:#601BDE;">2.COT的作用</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">透明性</font>**<font style="color:rgb(25, 27, 31);">：CoT 让 LLM 的推理过程更加透明和易于理解。我们可以看到它是如何得出答案的，而不仅仅是答案本身。</font>
+ **<font style="color:rgb(25, 27, 31);">提高准确性</font>**<font style="color:rgb(25, 27, 31);">：对于复杂问题，强迫 LLM 逐步推理通常会导致更准确的最终答案。这就像将一个难题分解为更小、更简单的步骤。</font>
+ **<font style="color:rgb(25, 27, 31);">可调试性</font>**<font style="color:rgb(25, 27, 31);">：如果 LLM 得出错误答案，CoT 可以帮助我们调试并理解它的推理过程在哪里出错了。</font>

:::color5
**<font style="color:#601BDE;">3.COT如何与RLHF结合？</font>**

:::

+ **<font style="color:#ED740C;">奖励正确的推理，而不仅仅是答案</font>**<font style="color:rgb(25, 27, 31);">：我们可以设计奖励模型（或 DPO/GRPO 的偏好数据集），当 LLM 生成的思考链：</font>
    - **<font style="color:rgb(25, 27, 31);">正确</font>**<font style="color:rgb(25, 27, 31);">：推理步骤逻辑严谨且得出正确答案。</font>
    - **<font style="color:rgb(25, 27, 31);">有帮助</font>**<font style="color:rgb(25, 27, 31);">：推理步骤清晰、易于理解且很好地解释了解题过程。</font>
+ **<font style="color:rgb(25, 27, 31);">CoT 的奖励信号示例：</font>**
    - **<font style="color:rgb(25, 27, 31);">输出 1（正确的 CoT）</font>**<font style="color:rgb(25, 27, 31);">：包含一个正确的思考链，得出正确答案。奖励：</font>**<font style="color:#ED740C;">+0.9（高奖励）</font>**
    - **<font style="color:rgb(25, 27, 31);">输出 2（无 CoT 或错误的 CoT）</font>**<font style="color:rgb(25, 27, 31);">：要么只给出答案，要么推理过程有缺陷。奖励：</font>**<font style="color:#74B602;">+0.2（低奖励）</font>**

<font style="color:rgb(25, 27, 31);">然后我们可以使用 PPO、DPO 或 GRPO 训练 LLM，生成更多像输出 1（有良好 CoT）的响应，减少像输出 2（没有良好 CoT）的响应。</font>

:::color4
<font style="color:rgb(25, 27, 31);">解锁 LLM 的推理能力：通过偏好学习奖励良好的 CoT，我们本质上是在教 LLM 如何逐步思考。这是解锁它们全部推理潜力并使它们成为更可靠的解题者的关键一步。</font>

:::



## STaR
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">STaR旨在解决如何提高语言模型在复杂推理任务上的性能，例如数学问题解答或常识问答。STaR（Self-Taught Reasoner）算法的原理是通过迭代地利用少量推理示例（rationales）和大量没有推理的大数据集，来引导模型逐步提升执行更复杂推理的能力。STaR算法的核心是一个简单的循环过程。</font>

**paper：**[**STaR: Self-Taught Reasoner Bootstrapping Reasoning With Reasoning**](https://arxiv.org/pdf/2203.14465)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058832190-3fe2056a-2c4d-41bf-b16e-603f95cfae05.png)

:::color5
**<font style="color:#601BDE;">1.STaR步骤</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743058931163-f7d26519-849a-45b0-aaed-a33cc528406c.png)

:::color5
**<font style="color:#601BDE;">2.评估</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">算术（Arithmetic）</font>**<font style="color:rgb(25, 27, 31);">：验证模型在解决不同位数的加法问题上的性能。STaR显著提高了模型在多位数加法问题上的准确率。特别是引入合理化（rationalization）步骤后，模型的性能提升更为显著。</font>
2. **<font style="color:rgb(25, 27, 31);">常识推理（Commonsense Reasoning）</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">CommonsenseQA</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=CommonsenseQA&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（CQA）数据集，评估模型在多项选择常识问题上的表现。在CommonsenseQA数据集上，STaR在开发集上的准确率超过了仅使用少量样本提示的基线（增加了35.9%），并且与直接预测答案的基线相比也有显著提升（增加了12.5%）。当与比STaR模型大30倍的模型相比时，STaR的性能与之相当（72.5% vs 73.0%）。</font>
3. **<font style="color:rgb(25, 27, 31);">小学数学（Grade School Math）</font>**<font style="color:rgb(25, 27, 31);">：利用</font>[<font style="color:rgb(9, 64, 142);">GSM8K</font>](https://zhida.zhihu.com/search?content_id=248326273&content_type=Article&match_order=1&q=GSM8K&zhida_source=entity)<font style="color:rgb(25, 27, 31);">数据集，测试模型解决自然语言表述的数学问题的能力。STaR显著提高了模型在GSM8K数据集上的性能，即使训练数据较少（无合理化的模型使用了25.0%的数据，合理化的模型使用了28.7%的数据）。</font>



# MCoT(多模态CoT)
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">随着大型语言模型（LLMs）的快速发展，人工智能领域迎来了前所未有的变革。然而，现实世界的复杂性要求AI不仅仅能处理文本信息，还需要能够理解和推理来自图像、视频、音频等多种模态的数据。多模态</font>[<font style="color:rgb(9, 64, 142);">思维链推理</font>](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E6%80%9D%E7%BB%B4%E9%93%BE%E6%8E%A8%E7%90%86&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（MCoT）正是为了解决这一问题而提出的。</font>**<font style="color:#74B602;">MCoT通过将思维链推理（CoT）扩展到多模态领域，使得AI能够在处理复杂任务时，像人类一样进行逐步推理。</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742971757076-e4227a3a-b3e6-4743-b268-c27e583e90fa.png)

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">思维链推理（CoT）是一种通过将复杂问题分解为一系列中间步骤来进行推理的技术。MCoT则在此基础上，将推理过程扩展到多模态数据中。</font>**<font style="color:#ED740C;">MCoT的核心思想是通过逐步推理来处理来自不同模态的信息，从而提高推理的透明度和准确性。</font>**

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**https://github.com/yaotingwangofficial/Awesome-MCoT**](https://github.com/yaotingwangofficial/Awesome-MCoT)

**paper：**[**https://arxiv.org/pdf/2503.12605**](https://arxiv.org/pdf/2503.12605)

**参考：**[**多模态思维链（MCoT）推理综述**](https://zhuanlan.zhihu.com/p/32278799470)

:::

:::color5
**<font style="color:#601BDE;">1.MCoT发展时间线</font>**

:::

<font style="color:rgb(25, 27, 31);">MCoT的研究近年来备受关注，尤其是在与</font>[<font style="color:rgb(9, 64, 142);">多模态大语言模型</font>](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（MLLMs）的结合中取得了显著进展。然而，尽管MCoT在多个领域取得了成功，但仍面临着诸多挑战。本文首次系统性地综述了MCoT推理的研究现状，旨在为这一领域的未来发展提供指导。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742971982378-a835d906-5058-4c3c-a32b-caacc5cd10ab.png)

:::color5
**<font style="color:#601BDE;">2.思维范式</font>**

:::

<font style="color:rgb(25, 27, 31);">MCoT的推理过程可以采用不同的思维范式，包括链式、树状和图状结构。链式结构适用于线性推理，而树状和图状结构则允许更复杂的推理路径。这些不同的结构使得MCoT能够灵活应对各种复杂的推理任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742972655335-038ca02d-392b-4d0a-894b-8861ce6b6ed6.png)<font style="color:rgb(25, 27, 31);">  
</font>

:::color5
**<font style="color:#601BDE;">3.多模态大模型</font>**

:::

<font style="color:rgb(25, 27, 31);">多模态大语言模型（MLLMs）是MCoT的核心技术之一。这些模型能够处理来自不同模态的数据，并生成相应的推理结果。近年来，MLLMs在图像、视频、音频等领域的理解和生成任务中取得了显著进展。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742972755449-b5f46768-485f-4dc3-b6d2-56dffa298b58.png)



## 不同模态下的MCoT
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742972872622-1353a380-ea37-4953-a0c2-58eafab1608e.png)

:::color5
**<font style="color:#601BDE;">1.图像推理</font>**

:::

<font style="color:rgb(25, 27, 31);">图像推理是MCoT应用最为广泛的领域之一，尤其是在</font>[<font style="color:rgb(9, 64, 142);">视觉问答</font>](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E9%97%AE%E7%AD%94&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（VQA）任务中。早期的研究如</font>**<font style="color:rgb(25, 27, 31);">IPVR</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Multimodal-CoT</font>**<font style="color:rgb(25, 27, 31);">，通过</font>**<font style="color:#74B602;">生成中间推理步骤（即“思维链”）</font>**<font style="color:rgb(25, 27, 31);">来提高视觉问答的准确性。例如，IPVR提出了</font>**<font style="color:#74B602;">“看、想、确认”的三阶段框架</font>**<font style="color:rgb(25, 27, 31);">，将感知与推理解耦，显著提升了推理的透明度和准确性。</font>

<font style="color:rgb(25, 27, 31);">后续的研究进一步优化了这一范式。例如，</font>**<font style="color:rgb(25, 27, 31);">MC-CoT</font>**<font style="color:rgb(25, 27, 31);">通过自一致性训练和</font>**<font style="color:#74B602;">多数投票机制来提高推理质量</font>**<font style="color:rgb(25, 27, 31);">，尤其是在小型模型中表现优异。</font>**<font style="color:rgb(25, 27, 31);">SoT</font>**<font style="color:rgb(25, 27, 31);">则通过动态选择推理范式（如概念链、分块符号和专家词典），显著提升了推理效率。</font>**<font style="color:rgb(25, 27, 31);">CoCoT</font>**<font style="color:rgb(25, 27, 31);">通过对比</font>**<font style="color:#74B602;">分析多张输入图像的相似性和差异性</font>**<font style="color:rgb(25, 27, 31);">，增强了多图像理解能力。</font>

<font style="color:rgb(25, 27, 31);">此外，</font>[<font style="color:rgb(9, 64, 142);">结构化推理机制</font>](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E7%BB%93%E6%9E%84%E5%8C%96%E6%8E%A8%E7%90%86%E6%9C%BA%E5%88%B6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">也被提出以增强可控性和可解释性。例如，</font>**<font style="color:rgb(25, 27, 31);">DDCoT</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Socratic Questioning</font>**<font style="color:rgb(25, 27, 31);">采用分阶段推理过程，系统化地优化多模态输出。</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Spot</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">TextCoT</font>**<font style="color:rgb(25, 27, 31);">则通过优先</font>**<font style="color:#74B602;">分析感兴趣区域，提升了上下文理解能力。</font>**

:::color5
**<font style="color:#601BDE;">2.视频推理</font>**

:::

<font style="color:rgb(25, 27, 31);">视频推理不仅需要处理静态图像信息，还需要理解时间动态，尤其是在长视频中。</font>**<font style="color:rgb(25, 27, 31);">CaVIR</font>**<font style="color:rgb(25, 27, 31);">通过</font>[<font style="color:rgb(9, 64, 142);">零样本MCoT</font>](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E9%9B%B6%E6%A0%B7%E6%9C%ACMCoT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">方法增强了意图问答的准确性，而</font>**<font style="color:rgb(25, 27, 31);">VideoAgent</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">HM-Prompt</font>**<font style="color:rgb(25, 27, 31);">则利用</font>**<font style="color:#74B602;">零样本MCoT提高了长视频推理能力，减少了幻觉现象。</font>**

<font style="color:rgb(25, 27, 31);">对于复杂的视频理解任务，</font>**<font style="color:rgb(25, 27, 31);">Video-of-Thought</font>**<font style="color:rgb(25, 27, 31);">提出了一个</font>**<font style="color:#74B602;">五阶段的推理框架，包括任务和目标识别、对象跟踪、动作分析、排序问答和答案验证</font>**<font style="color:rgb(25, 27, 31);">。这一结构化方法确保了对视频内容的全面理解。</font>**<font style="color:rgb(25, 27, 31);">CaRDiff</font>**<font style="color:rgb(25, 27, 31);">则将复杂的视频任务分解为</font>**<font style="color:#74B602;">caption生成、显著性推理和边界框生成等子组</font>**<font style="color:rgb(25, 27, 31);">件，指导扩散过程生成显著对象掩码。</font>

<font style="color:rgb(25, 27, 31);">此外，MCoT在医疗视频分析和情感计算等专业领域也展现了强大的应用潜力。例如，</font>**<font style="color:rgb(25, 27, 31);">TI-PREGO</font>**<font style="color:rgb(25, 27, 31);">通过结合ICL和自动思维链（ACoT）识别自我中心视频中的程序错误。</font>

:::color5
**<font style="color:#601BDE;">3.3D推理</font>**

:::

<font style="color:rgb(25, 27, 31);">3D推理涉及复杂的形状、空间关系和物理属性，传统方法依赖手动标注和固定规则，而MCoT通过将复杂任务分解为可管理的步骤，显著提高了3D生成和理解的效率。</font>

<font style="color:rgb(25, 27, 31);">例如，</font>**<font style="color:rgb(25, 27, 31);">3D-PreMise</font>**<font style="color:rgb(25, 27, 31);">利用MCoT指导LLMs生成</font>**<font style="color:#74B602;">3D形状和编程参数</font>**<font style="color:rgb(25, 27, 31);">，简化了对象合成过程。</font>**<font style="color:rgb(25, 27, 31);">L3GO</font>**<font style="color:rgb(25, 27, 31);">则引入了Chain-of-3D-Thought，通过</font>**<font style="color:#74B602;">迭代试错和工具调用在模拟环境中生成3D图像</font>**<font style="color:rgb(25, 27, 31);">，增强了适应性和精度。</font>**<font style="color:rgb(25, 27, 31);">Gen2Sim</font>**<font style="color:rgb(25, 27, 31);">通过生成3D资产作为MCoT输入，推动了机器人技能学习。</font>

:::color5
**<font style="color:#601BDE;">4.音频&语音</font>**

:::

<font style="color:rgb(25, 27, 31);">MCoT在音频和语音处理中的应用也取得了显著进展。例如，</font>**<font style="color:rgb(25, 27, 31);">CoT-ST</font>**<font style="color:rgb(25, 27, 31);">将语音翻译分解为</font>**<font style="color:#74B602;">语音识别和翻译两个阶段</font>**<font style="color:rgb(25, 27, 31);">，显著提高了翻译的准确性。</font>**<font style="color:rgb(25, 27, 31);">Audio-CoT</font>**<font style="color:rgb(25, 27, 31);">则将传统的CoT引入音频理解和推理任务中，而</font>**<font style="color:rgb(25, 27, 31);">Audio-Reasoner</font>**<font style="color:rgb(25, 27, 31);">通过四步结构化推理框架（</font>**<font style="color:#74B602;">如规划、字幕生成、推理和总结</font>**<font style="color:rgb(25, 27, 31);">）实现了长链MCoT推理。</font>

<font style="color:rgb(25, 27, 31);">在生成任务中，</font>**<font style="color:rgb(25, 27, 31);">SpatialSonic</font>**<font style="color:rgb(25, 27, 31);">利用MCoT推导</font>**<font style="color:#74B602;">相关属性和字幕，支持空间音频生成</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">SpeechGPT-Gen</font>**<font style="color:rgb(25, 27, 31);">则引入了Chain-of-Information-Generation方法，系统化地建模语义和感知信息，促进了自然语音生成。</font>

:::color5
**<font style="color:#601BDE;">5.表格&图表</font>**

:::

<font style="color:rgb(25, 27, 31);">表格和图表的复杂布局和隐含模式对LLMs提出了挑战。MCoT通过逐步推理，显著提高了对结构化数据的理解能力。例如，</font>**<font style="color:rgb(25, 27, 31);">LayoutLLM</font>**<font style="color:rgb(25, 27, 31);">通过</font>**<font style="color:#74B602;">布局感知预训练增强了文档理解能力</font>**<font style="color:rgb(25, 27, 31);">，而</font>**<font style="color:rgb(25, 27, 31);">TableGPT</font>**<font style="color:rgb(25, 27, 31);">引入了Chain-of-Command方法，系统化地处理表格问题。</font>

**<font style="color:rgb(25, 27, 31);">Chain-of-Table</font>**<font style="color:rgb(25, 27, 31);">则通过</font>**<font style="color:#74B602;">动态生成必要的操作和参数，重构表格以保留相关信息</font>**<font style="color:rgb(25, 27, 31);">，显著提升了表格理解能力。</font>**<font style="color:rgb(25, 27, 31);">Refocus</font>**<font style="color:rgb(25, 27, 31);">通过模拟人类注意力，生成</font>**<font style="color:#74B602;">视觉思维（如添加高亮或掩码区域）</font>**<font style="color:rgb(25, 27, 31);">，进一步改善了表格理解。</font>

:::color5
**<font style="color:#601BDE;">6.跨模态推理</font>**

:::

<font style="color:rgb(25, 27, 31);">跨模态推理涉及多个模态的协同处理。例如，</font>**<font style="color:rgb(25, 27, 31);">AVQA-CoT</font>**<font style="color:rgb(25, 27, 31);">通过将</font>**<font style="color:#74B602;">复杂查询分解为简单的子问题</font>**<font style="color:rgb(25, 27, 31);">，逐步解决音频-视觉问答任务。</font>**<font style="color:rgb(25, 27, 31);">SegPref</font>**<font style="color:rgb(25, 27, 31);">则利用VLLMs检测视觉场景中的</font>**<font style="color:#74B602;">潜在发声对象，结合文本推理和掩码解码器进行音频-视觉分割</font>**<font style="color:rgb(25, 27, 31);">，减少了对视觉特征的过度依赖。</font>



## MCoT方法论
:::color5
**<font style="color:#601BDE;">1.推理构建</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973368855-810b8ee5-e9db-4140-ac7f-d2efc917aa95.png)

<font style="color:rgb(25, 27, 31);">MCoT推理的方法论主要分为基于提示、基于计划和基于学习的方法。</font>

+ **<font style="color:rgb(25, 27, 31);">基于提示的方法</font>**<font style="color:rgb(25, 27, 31);">：通过</font>**<font style="color:#74B602;">精心设计的提示引导模型生成推理步骤</font>**<font style="color:rgb(25, 27, 31);">。例如，简单的指令“逐步思考以理解给定的文本和图像输入”可以作为零样本提示，引导模型生成推理步骤。</font>**<font style="color:rgb(25, 27, 31);">PromptCoT</font>**<font style="color:rgb(25, 27, 31);">通过优化输入提示，显著提升了图像合成的推理质量。</font>
+ **<font style="color:rgb(25, 27, 31);">基于计划的方法</font>**<font style="color:rgb(25, 27, 31);">：允许模型在推理过程中</font>**<font style="color:#74B602;">动态探索和优化推理路径</font>**<font style="color:rgb(25, 27, 31);">。例如，</font>**<font style="color:rgb(25, 27, 31);">MM-ToT</font>**<font style="color:rgb(25, 27, 31);">利用GPT-4和Stable Diffusion生成多模态输出，应用DFS和BFS选择最优输出。</font>**<font style="color:rgb(25, 27, 31);">HoT</font>**<font style="color:rgb(25, 27, 31);">则通过超边连接多个推理节点，增强了多模态推理能力。</font>
+ **<font style="color:rgb(25, 27, 31);">基于学习的方法</font>**<font style="color:rgb(25, 27, 31);">：通过</font>**<font style="color:#74B602;">训练或微调模型</font>**<font style="color:rgb(25, 27, 31);">，使其具备推理能力。例如，</font>**<font style="color:rgb(25, 27, 31);">Multimodal-CoT</font>**<font style="color:rgb(25, 27, 31);">通过微调包含推理数据的数据集，激活了模型的推理潜力。</font>**<font style="color:rgb(25, 27, 31);">G-CoT</font>**<font style="color:rgb(25, 27, 31);">则利用ChatGPT生成推理数据，通过微调将推理能力转移到自动驾驶任务中。</font>

:::color5
**<font style="color:#601BDE;">2.结构化推理</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973354431-8a559b4e-f141-47e7-987c-618e4e69fe29.png)

<font style="color:rgb(25, 27, 31);">结构推理框架通过定义明确的推理阶段，增强了推理过程的可控性和可解释性。</font>

+ **<font style="color:rgb(25, 27, 31);">异步模态建模</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">IPVR</font>**<font style="color:rgb(25, 27, 31);">引入了“</font>**<font style="color:#74B602;">看、想、确认</font>**<font style="color:rgb(25, 27, 31);">”的三阶段框架，将感知与推理解耦。</font>**<font style="color:rgb(25, 27, 31);">Visualization-of-Thought</font>**<font style="color:rgb(25, 27, 31);">通过生成2D网格文本表示，模拟心理意象，指导搜索和导航任务。</font>
+ **<font style="color:rgb(25, 27, 31);">定义程序阶段</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">BDoG</font>**<font style="color:rgb(25, 27, 31);">采用固定的辩论-总结流程，而</font>**<font style="color:rgb(25, 27, 31);">Det-CoT</font>**<font style="color:rgb(25, 27, 31);">则将VQA推理形式化为</font>**<font style="color:#74B602;">模板化的指令解析、子任务分解和执行。</font>**
+ **<font style="color:rgb(25, 27, 31);">自主程序阶段</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">PS-CoT</font>**<font style="color:rgb(25, 27, 31);">允许LLMs自主生成任务解决计划，而</font>**<font style="color:rgb(25, 27, 31);">DDCoT</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">AVQA-CoT</font>**<font style="color:rgb(25, 27, 31);">则将问题分解为</font>**<font style="color:#74B602;">子问题进行迭代解决。</font>**

:::color5
**<font style="color:#601BDE;">3.信息增强</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973428826-a5e0ec4c-1db5-4fc7-9b0c-7f702a2fb706.png)

<font style="color:rgb(25, 27, 31);">通过整合专家工具和外部知识，MCoT推理的全面性得到了显著提升。</font>

+ **<font style="color:rgb(25, 27, 31);">使用专家工具</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Image</font>**<font style="color:rgb(25, 27, 31);">通过生成</font>**<font style="color:#74B602;">辅助图表来增强数学或几何问题的推理能力</font>**<font style="color:rgb(25, 27, 31);">。</font>**<font style="color:rgb(25, 27, 31);">Det-CoT</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Cantor</font>**<font style="color:rgb(25, 27, 31);">则利用图像操作工具（如放大、标尺标记）提升细粒度视觉分析。</font>
+ **<font style="color:rgb(25, 27, 31);">使用世界知识检索</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">RAGAR</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Action</font>**<font style="color:rgb(25, 27, 31);">利用</font>**<font style="color:#74B602;">检索增强生成（RAG）整合领域特定或常识知识，增强推理过程。</font>**
+ **<font style="color:rgb(25, 27, 31);">利用上下文知识检索</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">DCoT</font>**<font style="color:rgb(25, 27, 31);">优先处理图像中的感兴趣区域，而</font>**<font style="color:rgb(25, 27, 31);">MCoT-Memory</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Video-of-Thought</font>**<font style="color:rgb(25, 27, 31);">则通过场景图表示建模对象或概念之间的关系。</font>

:::color5
**<font style="color:#601BDE;">4.目标粒度</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973574266-1b4ebf4f-ca50-473a-a4ec-02d033125b5e.png)

<font style="color:rgb(25, 27, 31);">MCoT推理的目标粒度从粗粒度理解到细粒度理解不等。</font>

+ **<font style="color:rgb(25, 27, 31);">粗粒度理解</font>**<font style="color:rgb(25, 27, 31);">：适用于VQA等任务，例如</font>**<font style="color:rgb(25, 27, 31);">Multimodal-CoT</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">Audio-CoT</font>**<font style="color:rgb(25, 27, 31);">，旨在实现对给定多模态信息的概览。</font>
+ **<font style="color:rgb(25, 27, 31);">细粒度理解</font>**<font style="color:rgb(25, 27, 31);">：例如，</font>**<font style="color:rgb(25, 27, 31);">CPSeg</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">CoTDet</font>**<font style="color:rgb(25, 27, 31);">通过LLMs细化接地参考，增强文本提示与目标视觉实例的对齐。</font>

:::color5
**<font style="color:#601BDE;">5.多模态推理</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973609323-6d4ac838-744f-4756-9740-f866f479457a.png)

<font style="color:rgb(25, 27, 31);">MCoT推理不仅限于文本推理，还可以生成多模态的推理步骤。例如，</font>**<font style="color:rgb(25, 27, 31);">Visual-CoT</font>**<font style="color:rgb(25, 27, 31);">通过</font>**<font style="color:#74B602;">生成中间视觉状态来填补逻辑空白</font>**<font style="color:rgb(25, 27, 31);">，而</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Image</font>**<font style="color:rgb(25, 27, 31);">则通过生成辅助图表增强数学或几何问题的推理能力。</font>

:::color5
**<font style="color:#601BDE;">6.测试时扩展</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973644283-2c4f3306-601d-4219-80df-3bad7da85cb7.png)

<font style="color:rgb(25, 27, 31);">测试时扩展通过增加推理步骤的计算资源，显著提高了推理的深度和质量。例如，</font>**<font style="color:rgb(25, 27, 31);">Qwen-QwQ</font>**<font style="color:rgb(25, 27, 31);">通过</font>**<font style="color:#74B602;">监督微调激活了长链推理能力</font>**<font style="color:rgb(25, 27, 31);">，而</font>**<font style="color:rgb(25, 27, 31);">Macro-o1</font>**<font style="color:rgb(25, 27, 31);">则通过</font>**<font style="color:#74B602;">蒙特卡洛树搜索（MCTS）激活外部慢思维能力。</font>**



## MCoT应用
:::color5
**<font style="color:#601BDE;">1.</font>**[**<font style="color:#601BDE;">嵌入式AI</font>**](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E5%B5%8C%E5%85%A5%E5%BC%8FAI&zhida_source=entity)

:::

<font style="color:rgb(25, 27, 31);">MCoT在嵌入式AI中的应用显著提升了机器人的规划、操作和导航能力。例如，</font>**<font style="color:rgb(25, 27, 31);">EmbodiedGPT</font>**<font style="color:rgb(25, 27, 31);">通过MCoT将任务分解为可执行的子目标，而</font>**<font style="color:rgb(25, 27, 31);">E-CoT</font>**<font style="color:rgb(25, 27, 31);">则通过文本命令的顺序执行增强了机器人控制。</font>

:::color5
**<font style="color:#601BDE;">2.代理系统</font>**

:::

<font style="color:rgb(25, 27, 31);">AI驱动的代理系统通过MCoT增强了自主交互和内容生成能力。例如，</font>**<font style="color:rgb(25, 27, 31);">Auto-GUI</font>**<font style="color:rgb(25, 27, 31);">利用MCoT直接操作图形界面，提高了效率，而</font>**<font style="color:rgb(25, 27, 31);">SmartAgent</font>**<font style="color:rgb(25, 27, 31);">则通过Chain-of-User-Thought推理提供个性化推荐。</font>

:::color5
**<font style="color:#601BDE;">3.自动驾驶</font>**

:::

<font style="color:rgb(25, 27, 31);">MCoT在自动驾驶中的应用提高了决策的适应性和可解释性。例如，</font>**<font style="color:rgb(25, 27, 31);">DriveCoT</font>**<font style="color:rgb(25, 27, 31);">将MCoT集成到端到端驾驶系统中，显著提升了驾驶性能，而</font>**<font style="color:rgb(25, 27, 31);">PKRD-CoT</font>**<font style="color:rgb(25, 27, 31);">则通过零样本MCoT提示解决了感知、知识、推理和决策问题。</font>

:::color5
**<font style="color:#601BDE;">4.</font>**[**<font style="color:#601BDE;">医疗与健康</font>**](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E5%8C%BB%E7%96%97%E4%B8%8E%E5%81%A5%E5%BA%B7&zhida_source=entity)

:::

<font style="color:rgb(25, 27, 31);">MCoT在医疗领域的应用包括视频压力检测、手术三重识别等任务。例如，</font>**<font style="color:rgb(25, 27, 31);">StressSelfRefine</font>**<font style="color:rgb(25, 27, 31);">通过心理学启发的“描述、评估、突出”过程检测视频中的压力，而</font>**<font style="color:rgb(25, 27, 31);">MedCoT</font>**<font style="color:rgb(25, 27, 31);">则通过分层专家系统提升了医学视觉问答的准确性。</font>

:::color5
**<font style="color:#601BDE;">5.</font>**[**<font style="color:#601BDE;">社会与人文</font>**](https://zhida.zhihu.com/search?content_id=255478112&content_type=Article&match_order=1&q=%E7%A4%BE%E4%BC%9A%E4%B8%8E%E4%BA%BA%E6%96%87&zhida_source=entity)

:::

<font style="color:rgb(25, 27, 31);">MCoT在人文和社会科学中的应用包括情感计算、教育等。例如，</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Empathetic</font>**<font style="color:rgb(25, 27, 31);">通过MCoT促进共情对话生成，而</font>**<font style="color:rgb(25, 27, 31);">Chain-of-Exemplar</font>**<font style="color:rgb(25, 27, 31);">则扩展了MCoT在教育领域的应用。</font>

:::color5
**<font style="color:#601BDE;">6.多模态生成</font>**

:::

<font style="color:rgb(25, 27, 31);">MCoT在图像和3D生成中的应用显著提升了生成质量。例如，</font>**<font style="color:rgb(25, 27, 31);">PARM++通过迭代的清晰度和潜力评估生成高质量图像，而L3GO</font>**<font style="color:rgb(25, 27, 31);">则通过Chain-of-3D-Thought生成非常规3D对象。</font>

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">MCoT数据集 & Benchmark</font>
<font style="color:rgb(25, 27, 31);">尽管MCoT取得了显著进展，但仍面临诸多挑战。例如，计算可持续性和慢思维悖论、跨模态符号操作的神经符号集成、动态环境适应和自适应链长等。未来的研究应关注这些挑战，以推动MCoT向更广泛的应用场景发展。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742973868040-bfad22c3-756e-48dd-a5c7-36041150b79c.png)

