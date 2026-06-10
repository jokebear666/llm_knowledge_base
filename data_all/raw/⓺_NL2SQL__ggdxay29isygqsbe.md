# ⓺ NL2SQL

<!-- source: yuque://zhongxian-iiot9/hlyypb/ggdxay29isygqsbe -->

# NL2SQL
## 定义 <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(63, 63, 63);">背景</font>**<font style="color:rgb(63, 63, 63);">：文本到 SQL 系统的重要性不言而喻。在当今数据驱动的时代，如医疗、物流、金融等众多行业，快速准确地获取数据洞察对于决策制定和业务运营效率的提升起着至关重要的作用。然而，SQL 的专业语法往往成为非技术用户获取数据的一大障碍。文本到 SQL 系统的出现，使得</font>**<font style="color:#74B602;">这些非专业用户能够以自然语言与数据库进行交互，无需深入学习 SQL 语法，即可高效获取所需信息</font>**<font style="color:rgb(63, 63, 63);">，极大地推动了数据的普及化应用。</font>

:::

:::color3
**简介：**<font style="color:rgb(1, 1, 1);">NL2SQL，也称为Text-to-SQL，是将自然语言查询转换为可在关系数据库上执行的SQL查询的任务。目标是</font>**<font style="color:#74B602;">生成准确反映用户意图的SQL，确保执行后得到适当的结果</font>**<font style="color:rgb(1, 1, 1);">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(1, 1, 1);">项目地址</font>**<font style="color:rgb(1, 1, 1);">：</font>[NL2SQL Handbook](https://github.com/HKUSTDial/NL2SQL_Handbook)

**<font style="color:rgb(1, 1, 1);">paper</font>**<font style="color:rgb(1, 1, 1);">：</font>[https://arxiv.org/pdf/2408.05109](https://arxiv.org/pdf/2408.05109)

**参考：**[万字长文详解Text-to-SQL](https://mp.weixin.qq.com/s/vahLyvMZNXIO4HDAqH3UOA)   [大模型Text2SQL全栈技术最新综述](https://mp.weixin.qq.com/s/tkWd5EFnD6lt23-NrU0Ddg)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318712614-43131216-cb4b-4dd3-a771-9a909fdf242b.png)

:::color5
**<font style="color:#601BDE;">1.人类工作流程 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:black;">理解自然语言查询</font>**<font style="color:rgb(1, 1, 1);">：首先理解用户的意图，识别NL中的关键部分，例如实体或属性、时间上下文和特定条件。</font>
+ **<font style="color:black;">链接数据库架构和检索内容</font>**<font style="color:rgb(1, 1, 1);">：基于对NL的理解，检查数据库架构和内容，识别生成SQL所需的相关表、列和单元格值。</font>
+ **<font style="color:black;">将NL意图转换为SQL</font>**<font style="color:rgb(1, 1, 1);">：最后，根据对NL和数据库概念的理解，编写相应的SQL查询。</font>

:::color5
**<font style="color:#601BDE;">2.NL2SQL示例 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">当用户提出自然语言查询：“</font>**<font style="color:rgb(63, 63, 63);">Where can I find a gas station with power less than 2 miles from the University of Louisiana at Lafayette?</font>**<font style="color:rgb(63, 63, 63);">”时，一个高效的文本到 SQL 系统能够精准解析用户意图，自动生成相应的SQL查询：</font>

```plsql
SELECT STATION_NAME, location
FROM gas_stations
WHERE fuel_available = 'Yes'  
AND distance < 2  
AND ST_Distance_Sphere(Point(long, lat),   Point(University_Long,University_Lat)) < 2;
```

<font style="color:rgb(63, 63, 63);">从而从数据库中准确提取出距离路易斯安那大学拉斐特分校 2 英里范围内有供电的加油站信息。这一过程不仅展示了文本到 SQL 系统的强大功能，更凸显了其在简化数据查询、提升数据可用性方面的重要价值。</font>

:::color5
**<font style="color:#601BDE;">3.NL2SQL的生命周期 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">基于大模型的NL2SQL整个生命周期，从以下四个方面进行：</font>

<font style="color:rgb(25, 27, 31);">（1）模型：NL2SQL转换技术不仅解决了自然语言的歧义和不明确性问题，而且还正确地将自然语言与数据库模式和实例映射；</font>

<font style="color:rgb(25, 27, 31);">（2）数据：从训练数据的收集，由于训练数据稀缺导致的数据合成，到NL2SQL基准测试；</font>

<font style="color:rgb(25, 27, 31);">（3）评估：使用不同的指标和粒度从多个角度评估NL2SQL方法；</font>

<font style="color:rgb(25, 27, 31);">（4）错误分析：分析NL2SQL错误以找到根本原因，并指导NL2SQL模型的发展。此外，我们还提供了开发NL2SQL解决方案的经验法则。最后，我们讨论了LLMs时代NL2SQL的研究挑战和开放性问题。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318622470-7eb6710e-93ef-4fdc-a5f8-df675bb7bbf0.png)

1. **<font style="color:rgb(25, 27, 31);">NL2SQL模型演化流图</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">从2004年开始，NL2SQL 的解决方案经历了多个发展阶段，包括基于规则的方法、神经网络基础方法、</font>[<font style="color:rgb(9, 64, 142);">预训练语言模型</font>](https://zhida.zhihu.com/search?content_id=254203174&content_type=Article&match_order=1&q=%E9%A2%84%E8%AE%AD%E7%BB%83%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（PLM）基础方法和大型语言模型（LLM）基础方法。</font>

<font style="color:rgb(25, 27, 31);">图片上方列出了各个阶段的重要模型，如PRECISE、BELA、ATHENA、SQLizer、Spider、SParC、ChatGPT等。下方列出了NL2SQL任务的数据集，如WikiSQL、Spider、SParC等</font>

    - <font style="color:rgb(25, 27, 31);">NL2SQL任务的输入：自然语言查询（NL Query）和数据库（Database）。</font>
    - <font style="color:rgb(25, 27, 31);">NL2SQL任务的输出：SQL查询（SQL Query）。</font>
2. **<font style="color:rgb(25, 27, 31);">Benchmarks 和 训练数据合成</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">训练数据构建方法：从数据库开始，通过不同的方法生成自然语言查询，然后转换为SQL查询。主要有以下三种方法：</font>

    - <font style="color:rgb(25, 27, 31);">人工标注</font>
    - <font style="color:rgb(25, 27, 31);">基于规则生成</font>
    - <font style="color:rgb(25, 27, 31);">用大模型生成（LLMs）</font>
3. **<font style="color:rgb(25, 27, 31);">NL2SQL评估</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">整个NL2SQL生命周期是一个循环过程，从数据集开始（如Spider、BIRD、Dr.Spider、WikiSQL等）-> 到使用模型生成SQL（如DAIL-SQL、DINSQL等模型）-> 评估（Execution Accuracy 执行准确率、Exact-Match 完全匹配准确率）-> Filter（SQL的复杂性/特征、数据领域）-> 评估（定量评估/定性评估）-> Analysis（可视化分析/可视化仪表板）</font>

4. **<font style="color:rgb(25, 27, 31);">NL2SQL错误分析</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">错误类型：图中展示了SQL查询中常见的错误类型及其比例，如SELECT（25.5%）、WHERE（15.2%）、FROM（15.3%）、GROUP BY（16.6%）等。</font>

## 挑战**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
| **<font style="color:rgb(25, 27, 31);">类型\难度等级</font>** | **<font style="color:rgb(25, 27, 31);">1星</font>** | **<font style="color:rgb(25, 27, 31);">2星</font>** | **<font style="color:rgb(25, 27, 31);">3星</font>** | **<font style="color:rgb(25, 27, 31);">4星</font>** | **<font style="color:rgb(25, 27, 31);">5星</font>** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">NL 挑战</font> | <font style="color:rgb(25, 27, 31);">词元级别识别</font> | <font style="color:rgb(25, 27, 31);">同义词识别</font> | <font style="color:rgb(25, 27, 31);">同义词理解</font> | <font style="color:rgb(25, 27, 31);">领域知识查询识别</font> | <font style="color:rgb(25, 27, 31);">多轮对话</font> |
| <font style="color:rgb(25, 27, 31);">DB 挑战</font> | <font style="color:rgb(25, 27, 31);">单表查询</font> | <font style="color:rgb(25, 27, 31);">多表查询</font> | <font style="color:rgb(25, 27, 31);">复杂模式的多表</font> | <font style="color:rgb(25, 27, 31);">大量表和值</font> | <font style="color:rgb(25, 27, 31);">真实世界数据库</font> |
| <font style="color:rgb(25, 27, 31);">NL2SQL 挑战</font> | <font style="color:rgb(25, 27, 31);">单表 SQL</font> | <font style="color:rgb(25, 27, 31);">多表 SQL</font> | <font style="color:rgb(25, 27, 31);">高级 SQL 特性支持</font> | <font style="color:rgb(25, 27, 31);">适应变化的模式</font> | <font style="color:rgb(25, 27, 31);">高效 SQL 生成</font> |


![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318642441-7710b996-ce9b-4fca-85c7-28d65ee5a747.png)

:::color5
**<font style="color:#601BDE;">1.不确定的自然语言查询 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">C1: 不确定的自然语言查询。</font>**<font style="color:rgb(25, 27, 31);">自然语言查询由于歧义和不明确性常常包含不确定性。在NL2SQL任务中，与自然语言相关的挑战可以总结如下：</font>

+ <font style="color:rgb(25, 27, 31);">词汇歧义：当一个单词有多种含义时就会发生这种情况。例如，“bat”这个词可以指代一种动物，也可以指棒球棒（名词），或者指挥动的动作（动词）。</font>
+ <font style="color:rgb(25, 27, 31);">句法歧义：当一个句子可以有多种解析方式时就会发生这种情况。例如，在句子“玛丽用望远镜看到了那个男人”中，短语“with the telescope”可以表示玛丽使用望远镜看到了那个男人，或者那个男人拥有望远镜。</font>
+ <font style="color:rgb(25, 27, 31);">不明确性：当语言表达缺乏足够的细节来清晰地传达特定的意图或含义时就会发生这种情况。例如，“2023年劳动节”在美国指的是9月4日，但在中国指的是5月1日。</font>

:::color5
**<font style="color:#601BDE;">2.复杂数据库和脏数据 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">C2：复杂数据库和脏数据。</font>**<font style="color:rgb(25, 27, 31);">NL2SQL任务需要对数据库模式有深入的理解，包括表名、列、关系和数据属性。现代模式的复杂性和大数据量使这项任务特别具有挑战性。</font>

+ <font style="color:rgb(25, 27, 31);">表之间的复杂关系：数据库通常包含数百个具有复杂相互关系的表。NL2SQL解决方案必须准确理解和利用这些关系来生成SQL查询。</font>
+ <font style="color:rgb(25, 27, 31);">属性和值的歧义性：数据库中模糊不清的值和属性可能会使NL2SQL系统难以识别正确的上下文。</font>
+ <font style="color:rgb(25, 27, 31);">特定领域的模式设计：不同领域通常具有独特的数据库设计和模式模式。跨领域的模式设计变化使得开发通用的NL2SQL解决方案变得困难。</font>
+ <font style="color:rgb(25, 27, 31);">大型和脏数据：在大型数据库中有效处理大量数据至关重要，因为将所有数据作为输入进行处理是不切实际的。此外，脏数据（如缺失值、重复项或不一致性）如果管理不当，可能会导致错误的查询结果（例如，影响WHERE子句）。</font>

:::color5
**<font style="color:#601BDE;">3.NL2SQL翻译 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">C3：NL2SQL翻译。</font>**<font style="color:rgb(25, 27, 31);">NL2SQL任务与将高级编程语言编译为低级机器语言不同，因为它通常在输入的自然语言和输出的SQL查询之间存在多对一的映射。具体来说，NL2SQL任务面临几个独特的挑战：</font>

+ <font style="color:rgb(25, 27, 31);">自由形式的自然语言与受限和正式的SQL：自然语言是灵活的，而SQL查询必须遵循严格的语法。将自然语言翻译成SQL需要精确性以确保生成的查询是可执行的。</font>
+ <font style="color:rgb(25, 27, 31);">多种可能的SQL查询：单个自然语言查询可以对应多个满足查询意图的SQL查询，这导致在确定适当的SQL翻译时存在歧义（参见图2(a)中的例子）。</font>
+ <font style="color:rgb(25, 27, 31);">数据库模式依赖性：NL2SQL翻译高度依赖于底层数据库模式。如图2(a)和(b)所示，相同的自然语言可能会根据模式变化产生不同的SQL查询。这要求NL2SQL模型在训练数据和现实世界模式差异之间架起桥梁。</font>

:::color5
**<font style="color:#601BDE;">4.开发NL2SQL解决方案中的技术挑战 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">C4：开发NL2SQL解决方案中的技术挑战。</font>**<font style="color:rgb(25, 27, 31);">开发强大的NL2SQL解决方案需要解决几个关键的技术挑战，包括：</font>

+ <font style="color:rgb(25, 27, 31);">成本效益解决方案：部署NL2SQL模型，特别是那些使用大型语言模型的模型，需要显著的资源，如硬件和/或API成本。在模型性能和成本效益之间实现最佳平衡仍然是一个关键挑战。</font>
+ <font style="color:rgb(25, 27, 31);">模型效率：模型大小和性能之间通常存在权衡，较大的模型通常能产生更好的结果。在不牺牲准确性的情况下优化效率是必要的，特别是在需要低延迟的交互式查询场景中。</font>
+ <font style="color:rgb(25, 27, 31);">SQL效率：NL2SQL模型生成的SQL必须既正确又优化以提高性能。这包括优化连接操作、索引使用和查询结构。高效的查询可以减少数据库负载，提高系统响应速度和吞吐量。</font>
+ <font style="color:rgb(25, 27, 31);">训练数据不足和噪声：获取高质量的NL2SQL训练数据是具有挑战性的。公共数据集通常有限，可能包含噪声注释，影响模型性能。注释需要数据库专业知识，增加成本，而NL2SQL任务的复杂性常常导致错误。</font>
+ <font style="color:rgb(25, 27, 31);">可信度和可靠性：NL2SQL模型必须可信且可靠，始终在不同的数据集和场景中产生准确的结果。可信度需要透明度，允许用户理解和验证生成的SQL。</font>

## 技术方案**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.技术方案演变 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318673543-be33b34b-6f89-4378-8f04-e7640d08815e.png)

+ **<font style="color:black;">基于规则的方法</font>**<font style="color:rgb(1, 1, 1);">：早期研究主要集中在使用预定义规则或语义解析器来理解自然语言查询并将其转换为SQL查询。</font>
+ **<font style="color:black;">基于神经网络的方法</font>**<font style="color:rgb(1, 1, 1);">：为了解决基于规则的方法的局限性，研究者开始利用神经网络来解决NL2SQL任务，例如使用序列到序列模型或图神经网络。</font>
+ **<font style="color:black;">基于预训练语言模型的方法</font>**<font style="color:rgb(1, 1, 1);">：随着BERT和T5等预训练语言模型的出现，基于PLM的NL2SQL方法在多个基准数据集上取得了竞争性的性能。</font>
+ **<font style="color:black;">大型语言模型时代</font>**<font style="color:rgb(1, 1, 1);">：随着LLMs的出现，NL2SQL技术取得了显著进展，LLMs具有卓越的语言理解和新出现的能力，例如使用提示来执行NL2SQL任务。</font>

### 预处理策略**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">预处理步骤在NL2SQL翻译过程中至关重要，因为它识别相关的表和列（即模式链接）并检索支持SQL查询生成所需的数据库内容或单元格值（即数据库内容检索）。此外，它通过</font>**<font style="color:#ED740C;">整合特定领域的知识（即附加信息获取）来丰富上下文</font>**<font style="color:rgb(25, 27, 31);">，这可以提高对查询上下文的理解并纠正错误以防止其传播。</font>

:::

:::color5
**<font style="color:#601BDE;">1.架构链接（选表、字段）  Schema Linking</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">模式链接旨在</font>**<font style="color:#74B602;">识别与给定自然语言查询相关的表和列</font>**<font style="color:rgb(25, 27, 31);">，确保在有限输入内准确映射和处理关键信息。这一步骤对于提高NL2SQL任务的性能至关重要。在LLM时代，由于LLM的输入长度限制，模式链接变得更加关键。</font>

+ **<font style="color:black;">目的</font>**<font style="color:rgb(1, 1, 1);">：</font>**<font style="color:#74B602;">确定与给定自然语言查询相关的表格和列</font>**<font style="color:rgb(1, 1, 1);">，确保在有限的输入内准确映射和处理关键信息，提高NL2SQL任务的性能。</font>
+ **<font style="color:black;">方法分类</font>**<font style="color:rgb(1, 1, 1);">：</font><font style="color:rgb(25, 27, 31);">我们将现有的模式链接策略分为三类，基于其特征：1）基于字符串匹配的模式链接，2）基于神经网络的模式链接，以及3）基于上下文学习的模式链接。</font>
    - **<font style="color:black;">基于字符串匹配的方法</font>**<font style="color:rgb(1, 1, 1);">：</font><font style="color:rgb(25, 27, 31);">早期研究主要关注于模式链接的字符串匹配技术。这些方法使用自然语言查询和模式之间的</font>**<font style="color:#74B602;">相似性度量</font>**<font style="color:rgb(25, 27, 31);">来识别相关映射。这种方法通常使用精确匹配和近似匹配技术。</font>
    - **<font style="color:black;">基于神经网络的方法</font>**<font style="color:rgb(1, 1, 1);">：使用深度神经网络来匹配数据库架构和自然语言查询，有效解析语言和数据库结构之间的复杂语义关系。</font>
    - **<font style="color:black;">基于上下文学习的方法</font>**<font style="color:rgb(1, 1, 1);">：利用大型语言模型（如GPT-4）的强推理能力直接</font>**<font style="color:#74B602;">从NL查询中识别和链接相关的数据库架构组件</font>**<font style="color:rgb(1, 1, 1);">。</font>

:::color5
**<font style="color:#601BDE;">2.数据库内容检索 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">数据库内容检索专注于高效</font>**<font style="color:#74B602;">提取特定SQL子句（如WHERE）所需的单元格值</font>**<font style="color:rgb(25, 27, 31);">。我们将现有的数据库内容检索策略根据其特征分为三类：1）基于字符串匹配的方法，2）基于神经网络的方法，以及 3）数据库内容检索的索引策略。</font>

+ **<font style="color:black;">目的</font>**<font style="color:rgb(1, 1, 1);">：通过文本搜索算法和数据库索引高效检索单元格值。</font>
+ **<font style="color:black;">策略分类</font>**<font style="color:rgb(1, 1, 1);">：</font>
    - **<font style="color:black;">基于字符串匹配的方法</font>**<font style="color:rgb(1, 1, 1);">：通过字符串匹配查找与给定NL查询相关的单元格值序列。</font>
    - **<font style="color:black;">基于神经网络的方法</font>**<font style="color:rgb(1, 1, 1);">：神经网络通过多层非线性变换学习复杂数据格式和语义表示，以捕获语义特征，缓解同义词问题。</font>
    - **<font style="color:black;">索引策略</font>**<font style="color:rgb(1, 1, 1);">：索引是提高数据库内容检索效率的关键方法，允许更快地访问相关单元格值。</font>

> <font style="color:rgb(25, 27, 31);">CHESS使用局部敏感哈希进行近似最近邻域搜索，索引唯一单元格值以快速找到与自然语言查询最相关的匹配项。这种方法加快了比较编辑距离和语义嵌入的过程。CodeS采用粗到细匹配策略。它使用BM25[90]构建粗粒度搜索的索引，识别候选值，然后通过应用最长公共子串算法评估与自然语言的相似性，从而精确定位最相关的单元格值。</font>
>

:::color5
**<font style="color:#601BDE;">3.额外信息获取 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">额外信息，如领域知识，在增强NL2SQL模型对自然语言查询、模式链接和整体NL2SQL翻译的理解中起着至关重要。这些信息可以为NL2SQL骨干模型或特定模块</font>**<font style="color:#74B602;">提供示例、领域知识、公式证据和格式信息</font>**<font style="color:rgb(25, 27, 31);">，从而提高生成结果的质量。我们将现有策略分为以下两组：1）基于样本的方法，和2）基于检索的方法。</font>

+ **<font style="color:black;">作用</font>**<font style="color:rgb(1, 1, 1);">：额外信息（例如领域知识）在提高NL2SQL模型理解NL查询、执行架构链接和NL2SQL翻译方面发挥着重要作用。</font>
+ **<font style="color:black;">应用</font>**<font style="color:rgb(1, 1, 1);">：研究人员经常将额外信息作为文本输入（提示）的一部分，连同少数示例一起输入，以提高模型的理解和翻译质量。</font>
    1. **<font style="color:rgb(25, 27, 31);">基于样本的方法</font>**<font style="color:rgb(25, 27, 31);">：随着LLM和上下文学习技术的进步，研究人员经常在文本输入（即提示）中结合示例和额外信息。DIN-SQL通过多个阶段的少样本学习整合额外信息，如</font>**<font style="color:#74B602;">模式链接、查询分类、任务分解和自我校正</font>**<font style="color:rgb(25, 27, 31);">。这使得DIN-SQL能够处理复杂模式链接、多表连接和嵌套查询等挑战。</font>
    2. **<font style="color:rgb(25, 27, 31);">基于检索的方法</font>**<font style="color:rgb(25, 27, 31);">：为了提高准确性和效率，一些研究人员采用基于相似性的检索方法。</font>**<font style="color:rgb(25, 27, 31);">例如，PET-SQL构建问题框架和问题-SQL对的池，选择与目标查询最相似的k个示例，然后用于提示。</font>**<font style="color:rgb(25, 27, 31);">当数据库缺乏基于文本的额外信息时，研究人员设计方法检索和转换外部知识为自然语言。</font>

### <font style="color:rgb(0, 0, 0);">NL2SQL翻译方法</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">深入探讨了使用语言模型进行NL2SQL翻译的方法。这些方法包括编码策略、解码策略和特定于任务的提示策略，以及如何利用中间表示来优化NL2SQL翻译过程。</font>

:::

:::color5
**<font style="color:#601BDE;">1.编码策略</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318766676-39ef9624-2c6d-48dc-8c69-74bfe641f4ce.png)

<font style="color:rgb(0, 0, 0);">编码策略涉及将自然语言和数据库架构转换为结构化格式，以便语言模型有效利用。这一转换对于将非结构化和半结构化数据转换为可用于生成SQL查询的格式至关重要。</font>

+ **<font style="color:black;">顺序编码</font>**<font style="color:rgb(1, 1, 1);">：将NL和数据库架构视为一系列标记。</font>
+ **<font style="color:black;">基于图的编码</font>**<font style="color:rgb(1, 1, 1);">：利用数据库的固有关系结构和输入数据的复杂相互依赖性。</font>
+ **<font style="color:black;">独立编码</font>**<font style="color:rgb(1, 1, 1);">：将NL的不同部分（如子句和条件）分别编码，然后在后期组合以生成最终的SQL。</font>

:::color5
**<font style="color:#601BDE;">2.解码策略 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318774441-9012b0e7-b431-4517-a6da-c483bbe41288.png)

<font style="color:rgb(0, 0, 0);">解码策略在NL2SQL翻译中扮演关键角色，负责将编码器生成的表示转换为目标SQL查询。</font>

+ **<font style="color:black;">贪婪搜索解码</font>**<font style="color:rgb(1, 1, 1);">：选择当前概率最高的标记作为输出。</font>
+ **<font style="color:black;">束搜索解码</font>**<font style="color:rgb(1, 1, 1);">：保留多个候选序列，探索更大的搜索空间。</font>
+ **<font style="color:black;">约束感知增量解码</font>**<font style="color:rgb(1, 1, 1);">：在解码过程中逐步添加约束，确保生成的SQL查询在语法上正确。</font>

:::color5
**<font style="color:#601BDE;">3.特定任务的提示策略 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">在大型语言模型时代，提示工程可以发挥LLMs的能力，并已被广泛应用于自然语言处理。</font>

+ **<font style="color:black;">思维链</font>**<font style="color:rgb(1, 1, 1);">：推动模型顺序思考和推理任务目标。</font>
+ **<font style="color:black;">分解</font>**<font style="color:rgb(1, 1, 1);">：将最终任务分解为多个子任务，分别进行推理。</font>

:::color5
**<font style="color:#601BDE;">4.中间表示 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">中间表示（IR）是NL查询和SQL查询之间的桥梁，它是一个结构化但灵活的语法，捕捉NL查询的基本组成部分和关系，而无需SQL的严格语法规则。</font>

+ **<font style="color:black;">SQL-like 语法语言</font>**<font style="color:rgb(1, 1, 1);">：将用户查询转换为中间的SQL-like表达式。</font>
+ **<font style="color:black;">SQL-like 草图结构</font>**<font style="color:rgb(1, 1, 1);">：构建草图规则，将NL映射到SQL-like框架中。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318790284-0c0d1afd-515a-4ffc-9b8e-46114141deaa.png)

### 后处理策略**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">描述了在NL2SQL模型生成SQL之后，如何通过后处理步骤来优化和改进生成的SQL查询，以更好地满足用户的期望。</font>

:::

:::color5
**<font style="color:#601BDE;">1.SQL校正策略（SQL Correction Strategies） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:black;">目的</font>**<font style="color:rgb(1, 1, 1);">：修正由模型生成的SQL中的语法错误。</font>
+ **<font style="color:black;">方法</font>**<font style="color:rgb(1, 1, 1);">：例如DIN-SQL提出的自我校正模块，通过不同的提示指导模型识别和纠正错误。</font>

:::color5
**<font style="color:#601BDE;">2.输出一致性（Output Consistency） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:black;">目的</font>**<font style="color:rgb(1, 1, 1);">：提高模型输出的一致性。</font>
+ **<font style="color:black;">方法</font>**<font style="color:rgb(1, 1, 1);">：例如C3-SQL提出的自我一致性方法，通过采样多个不同的推理路径并选择最一致的答案来提高输出质量。</font>

:::color5
**<font style="color:#601BDE;">3.执行引导策略（Execution-Guided Strategies） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:black;">目的</font>**<font style="color:rgb(1, 1, 1);">：使用SQL查询的执行结果来指导后续处理。</font>
+ **<font style="color:black;">方法</font>**<font style="color:rgb(1, 1, 1);">：如ZeroNL2SQL通过可执行性检查过程不断生成SQL查询，并反馈错误信息给LLMs以实现可执行查询。</font>

:::color5
**<font style="color:#601BDE;">4.N-best重排策略（N-best Rerankers Strategies） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:black;">目的</font>**<font style="color:rgb(1, 1, 1);">：对原始模型生成的前n个结果进行重排序，通常使用更大的模型或结合额外的知识源。</font>
+ **<font style="color:black;">方法</font>**<font style="color:rgb(1, 1, 1);">：如Bertrand-dr使用BERT模型作为重排器来改进多个NL2SQL模型。</font>

## 评估**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.NL2SQL 现有方法 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318744329-9ad8e621-4a48-4157-ab9d-77a390f87ede.png)

:::color5
**<font style="color:#601BDE;">2.NL2SQL benchmark </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

随着NL2SQL的进步，benchmark涵盖的各种数据集在下图所示，<font style="color:rgb(0, 0, 0);">数据集从早期的单一领域、简单SQL查询发展到跨领域、多轮对话和多语言挑战的复杂数据集。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743318847318-b3346f30-d826-44af-a8cc-8146c0a3510a.png)











