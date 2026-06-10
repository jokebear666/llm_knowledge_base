# ⓪ Agent：上下文工程的6大技巧

<!-- source: yuque://zhongxian-iiot9/hlyypb/kd0e94ksc1cfnawz -->

:::success
**<font style="color:#000000;">背景</font>**<font style="color:#000000;">：在</font>[<font style="color:#000000;">Manus</font>](https://manus.im/app)<font style="color:#000000;">项目的最初阶段，团队面临一个关键决策：</font>**<font style="color:#74B602;">是应该使用开源基础模型训练一个端到端的智能体模型，还是基于前沿模型的</font>**[**<font style="color:#74B602;">上下文学习</font>**](https://arxiv.org/abs/2301.00234)**<font style="color:#74B602;">能力构建一个智能体？</font>**<font style="color:#000000;"> 近年来，以GPT-3为代表的大语言模型兴起，催生了“上下文学习”的新范式。这彻底改变了AI应用的构建方式，使开发者无需漫长的模型微调，仅通过精心设计提示词即可快速赋予模型新能力。这一技术变革为AI代理的快速开发和迭代提供了可能，尤其适合追求产品市场匹配的初创团队。</font>

:::

:::color3
**简介：**<font style="color:rgb(15, 17, 21);">本文</font>**<font style="color:#ED740C;">基于Manus项目的实战经验</font>**<font style="color:rgb(15, 17, 21);">，</font>**<font style="color:#ED740C;">探讨AI代理的“上下文工程”</font>**<font style="color:rgb(15, 17, 21);">。文章开篇点明核心抉择：放弃传统微调，转而押注上下文工程。作者分享了这一决策背后的惨痛教训与显著优势——将迭代周期从数周缩短至几小时。文章承诺将揭示其通过反复试错总结出的“随机研究生下降”方法论与核心原则，旨在帮助其他开发者更高效地构建AI代理。</font><font style="color:#D22D8D;">(by草莓师姐)</font>

[**https://manus.im/zh-cn/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus**](https://manus.im/zh-cn/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1763113900753-f14bbe52-300c-491c-86b2-c4071c971617.png)

# <font style="color:rgb(34, 34, 34);">围绕 KV-Cache 做设计</font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">KV-Cache 命中率，是直接决定Agent的延迟和成本的关键指标。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763113755041-5b4d3a41-785d-4e1e-b304-90528ad87838.webp)

:::color5
**<font style="color:#601BDE;">1.AI Agent的运行方式 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(15, 17, 21);">用户输入</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">→</font>
2. **<font style="color:rgb(15, 17, 21);">模型决策</font>**<font style="color:rgb(15, 17, 21);">：模型根据当前完整的上下文选择下一个动作。 →</font>
3. **<font style="color:rgb(15, 17, 21);">执行动作</font>**<font style="color:rgb(15, 17, 21);">：所选择的动作（如Function Call）在沙箱环境中安全执行。 →</font>
4. **<font style="color:rgb(15, 17, 21);">更新上下文</font>**<font style="color:rgb(15, 17, 21);">：动作执行的结果被写回，成为上下文的一部分。 →</font>
5. **<font style="color:rgb(15, 17, 21);">循环迭代</font>**<font style="color:rgb(15, 17, 21);">：流程回到第2步，模型基于增长后的新上下文再次决策。 →</font>
6. **<font style="color:rgb(15, 17, 21);">...</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">→</font>
7. **<font style="color:rgb(15, 17, 21);">任务完成</font>**

<font style="color:rgb(0, 0, 0);">可以看出，上下文在每一步都会增长，而输出的Function Call结果通常相对较短，以 Manus 为例，平均输入与输出 token 的比例约为 100:1。幸运的是，拥有相同前缀的上下文可以利用 KV 缓存（KV-cache）机制，极大降低首个 token 生成时间和推理成本。以 Claude Sonnet 为例，缓存的输入 token 价格为 0.30 美元/百万 token，而未缓存的则高达 3 美元/百万 token，相差 10 倍，很夸张的节省了。</font>

:::color5
**<font style="color:#601BDE;">2.从上下文工程的角度看，提升 KV 缓存命中率的关键要点如下 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

+ <font style="color:rgb(1, 1, 1);">让 prompt 前缀绝对稳定：由于LLM的自回归属性，只要有一个 token 存在变动，就会让缓存从该 token 之后开始失效。一个常见的错误是在系统提示词的开始加入时间戳，尤其是精确到秒级，会直接让缓存命中率归0.</font>
+ <font style="color:rgb(1, 1, 1);">上下文只能追加：避免修改之前的动作以及观测结果，确保你的序列化过程是确定性的。很多编程语言和库在序列化 JSON 对象时并不保证键的顺序稳定，这会在悄无声息地破坏掉缓存。</font>
+ <font style="color:rgb(1, 1, 1);">需要时明确标记缓存断点：一些模型提供方或推理框架并不支持自动增量前缀缓存，需要手动在上下文中插入缓存断点。注意在设置断点时，要考虑潜缓存可能过期的时间，至少确保断点包含在系统提示词的结尾。</font>

<font style="color:rgb(0, 0, 0);">如果是使用vLLM等框架时，请记得打开 prefix caching，并用 session ID 把请求路由到同一worker。</font>



**<font style="color:rgb(34, 34, 34);"></font>**

# <font style="color:rgb(34, 34, 34);">利用Mask，而非删除</font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">Agent系统中，能力越多，那么工具就需要越多。尤其是MCP大火，如果允许用户自定义配置工具，会有人塞上百个来历不明的工具到你构建的动作空间里。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763113755026-fac8d8a1-2901-4aa2-a9a5-16851a545730.webp)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">工具数量与模型性能的关系 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(15, 17, 21);">Agent系统中工具越多，模型越容易选错行动或采取低效路径，导致性能下降。</font><font style="color:rgb(0, 0, 0);">显而易见，模型会更容易选错行动，或者采取低效路径，就是工具越多的Agent，可能越笨。</font>

<font style="color:rgb(0, 0, 0);">一般的做法就是动态加载/卸载工具，类似RAG一样，但Manus尝试过之后，都是血的教训</font>

+ <font style="color:rgb(1, 1, 1);">工具定义通常在上下文最前面，任何增删都会炸掉 KV-Cache。</font>
+ <font style="color:rgb(1, 1, 1);">在history里提到的工具一旦消失，模型会困惑甚至幻觉。</font>

<font style="color:rgb(0, 0, 0);">结论就是：除非绝对必要，否则避免在迭代中途动态增删工具。Manus 的解法就是，不动工具定义，利用上下文感知的状态机来管理工具，在解码阶段用 logits mask 阻止或强制选择某些动作。</font>

:::color5
**<font style="color:#601BDE;">2.实践优化：三大调用模式 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

 在实践中，大多数模型提供商和推理框架支持某种形式的响应预填充，这允许你在不修改工具定义的情况下约束动作空间。函数调用通常有三种模式（我们将使用 NousResearch 的 [Hermes 格式](https://github.com/NousResearch/Hermes-Function-Calling) 作为示例）：

+ 自动 – 模型可以选择调用或不调用函数。通过仅预填充回复前缀实现：<|im_start|>assistant
+ 必需 – 模型必须调用函数，但选择不受约束。通过预填充到工具调用令牌实现：<|im_start|>assistant<tool_call>
+ 指定 – 模型必须从特定子集中调用函数。通过预填充到函数名称的开头实现：<|im_start|>assistant<tool_call>{"name": "browser_ 通过这种方式，我们通过直接掩码token的logits来约束动作选择。例如，当用户提供新输入时，Manus必须立即回复而不是执行动作。我们还有意设计了具有一致前缀的动作名称——例如，所有与浏览器相关的工具都以browser_开头，命令行工具以shell_开头。这使我们能够轻松确保代理在给定状态下只从特定工具组中进行选择而无需使用有状态的logits处理器。



# <font style="color:rgb(34, 34, 34);">将文件系统作为上下文</font>
:::color3
**简介：**<font style="color:rgb(15, 17, 21);">针对代理系统中上下文过长和信息丢失的问题，提出将文件系统作为持久化外部记忆的解决方案，并探讨了状态空间模型在智能体环境中的潜力。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763113755042-aa5fb9b6-8fd8-427d-a05c-af347ef8ae5b.webp)

:::color5
**<font style="color:#601BDE;">1.三个常见的痛点</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

现代前沿LLM现在提供128K令牌或更多的上下文窗口。但在真实世界的代理场景中，这通常不够，有时甚至是一种负担。有三个常见的痛点：

1. 观察结果可能非常庞大，尤其是当代理与网页或PDF等非结构化数据交互时。很容易超出上下文限制。
2. 模型性能往往会下降，超过一定的上下文长度后，即使技术上支持该窗口大小。
3. 长输入成本高昂，即使使用前缀缓存。你仍然需要为传输和预填充每个token付费。

:::color5
**<font style="color:#601BDE;">2.将文件系统作为持久化外部记忆的解决方案 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

为了解决这个问题，许多代理系统实现了上下文截断或压缩策略。但过度激进的压缩不可避免地导致信息丢失。这个问题是根本性的：代理本质上必须根据所有先前状态预测下一个动作——而你无法可靠地预测哪个观察结果可能在十步之后变得至关重要。从逻辑角度看，任何不可逆的压缩都带有风险。 这就是为什么我们在Manus中将文件系统视为终极上下文：大小不受限制，天然持久化，并且代理可以直接操作。模型学会按需写入和读取文件——不仅将文件系统用作存储，还用作结构化的外部记忆。

1. **<font style="color:rgb(15, 17, 21);">上下文管理的根本矛盾</font>**<font style="color:rgb(15, 17, 21);">：代理需要依赖完整历史状态决策，但过度压缩上下文会导致关键信息丢失，影响长期决策可靠性。</font>
2. **<font style="color:rgb(15, 17, 21);">文件系统作为终极上下文</font>**<font style="color:rgb(15, 17, 21);">：利用文件系统不受限、持久化、可直接操作的特性，为代理提供结构化外部记忆，支持按需读写。</font>
3. **<font style="color:rgb(15, 17, 21);">可恢复的压缩策略</font>**<font style="color:rgb(15, 17, 21);">：通过保留URL、文档路径等关键元数据，实现无损压缩，既缩短上下文长度又确保信息可重新获取。</font>
4. **<font style="color:rgb(15, 17, 21);">状态空间模型的潜力</font>**<font style="color:rgb(15, 17, 21);">：SSM虽缺乏完整注意力机制，但若能结合基于文件的记忆系统，将长期状态外部化，可能成为高效智能体的新方向。</font>
5. **<font style="color:rgb(15, 17, 21);">未来展望</font>**<font style="color:rgb(15, 17, 21);">：基于SSM的智能体有望继承神经图灵机的优势，通过外部化记忆突破现有模型在长程依赖处理上的局限。</font>



# <font style="color:rgb(34, 34, 34);">通过复述操纵注意力</font>
:::color3
**简介：**<font style="color:rgb(15, 17, 21);">Manus系统在处理复杂任务时创建并持续更新待办文件（todo.md），通过自然语言复述目标来增强模型的注意力管理与任务一致性。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763113755035-b74cc972-bd6a-43f5-8962-7d661924e3d3.webp)

:::color5
**<font style="color:#601BDE;">1.通过复述操纵注意力</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

1. **<font style="color:rgb(15, 17, 21);">行为现象</font>**<font style="color:rgb(15, 17, 21);">：Manus在处理复杂任务时会主动创建并动态更新“todo.md”文件，逐步标记已完成项。</font>
2. **<font style="color:rgb(15, 17, 21);">机制本质</font>**<font style="color:rgb(15, 17, 21);">：该行为是系统主动引导注意力的策略，并非偶然，旨在通过自然语言复述目标增强任务连贯性。</font>
3. **<font style="color:rgb(15, 17, 21);">问题背景</font>**<font style="color:rgb(15, 17, 21);">：Manus平均每个任务需约50次工具调用，长上下文和复杂任务易导致模型偏离目标或遗忘初始意图。</font>
4. **<font style="color:rgb(15, 17, 21);">作用原理</font>**<font style="color:rgb(15, 17, 21);">：通过持续将待办事项更新至上下文末尾，使全局计划始终处于模型近期注意力范围内，缓解“信息丢失在中间”的问题。</font>
5. **<font style="color:rgb(15, 17, 21);">实现优势</font>**<font style="color:rgb(15, 17, 21);">：该方法仅依赖自然语言表达，无需调整系统架构，即可有效维持目标一致性，提升任务执行稳定性。</font>



# <font style="color:rgb(34, 34, 34);">保留错误内容在上下文中</font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">智能体一定会犯错，LLM的幻觉、环境的报错、工具的抽风，这不是BUG，而是现实。在多步任务中，失败不是例外，而是循环的一部分。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763113755152-43692634-1a4d-4c40-9499-5cd2dd248d9a.webp)

:::color5
**<font style="color:#601BDE;">1.保留错误的重要性</font>****<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(0, 0, 0);">常见做法是隐藏这些错误：清理痕迹、重试动作，或者重置模型状态，然后把它交给神奇的“温度”。看起来似乎更安全、更可控。但这会抹掉证据，模型学不到教训。</font>

<font style="color:rgb(0, 0, 0);">Manus发现：把错误留在上下文里，模型看到失败动作后，会隐式地更新其内部认知，降低重复犯错的概率。认为错误恢复能力是真正具备智能体行为的最明确的指标之一。</font>

1. **<font style="color:rgb(15, 17, 21);">错误的必然性</font>**<font style="color:rgb(15, 17, 21);">：代理犯错是常态而非异常，语言模型幻觉、环境错误、工具异常及边缘情况都会导致多步骤任务中的常规失败。</font>
2. **<font style="color:rgb(15, 17, 21);">错误处理的常见误区</font>**<font style="color:rgb(15, 17, 21);">：倾向于通过清理痕迹、重试操作或重置状态来隐藏错误，这种做法虽感觉可控，但移除了关键的适应证据。</font>
3. **<font style="color:rgb(15, 17, 21);">有效的改进方法</font>**<font style="color:rgb(15, 17, 21);">：将错误尝试完整保留在上下文中，使模型能通过观察失败行动及反馈结果，隐式更新内部信念，降低重复错误概率。</font>
4. **<font style="color:rgb(15, 17, 21);">错误恢复的指标意义</font>**<font style="color:rgb(15, 17, 21);">：错误恢复能力是真正代理行为的关键标志，但在当前学术研究和公共基准测试中，这一能力在理想化评估条件下仍未被充分重视。</font>





# <font style="color:rgb(34, 34, 34);">不要被few-shot误导</font>
:::color3
**简介：**<font style="color:rgb(0, 0, 0);">少样本提示（Few-shot Prompting）是提升LLM输出的常用手段，但在Agent系统中可能会适得其反。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1763113755550-c756bddb-3b83-48ec-b638-caf009414ee0.webp)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">少样本提示技术在智能体系统中的潜在风险 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(0, 0, 0);">LLM是出色的模仿者，若上下文里都是大量相似的动作-观测对，模型会倾向遵循这种形式，哪怕者并不是最优解。例如，当使用 Manus 协助审阅20 份简历时，Agent往往会因为上下文里出现了类似操作，就不断重复，陷入一种循环，最终导致行为漂移、过度泛化，有时产生幻觉。</font>

<font style="color:rgb(0, 0, 0);">Manus的做法：增加多样性。在动作和观察中引入少量结构化变化，例如采用不同序列化模板、措辞、在顺序或格式上加入噪音等，打破惯性。</font>

<font style="color:rgb(0, 0, 0);">总之，上下文越单一，智能体越脆弱。</font>

1. **<font style="color:rgb(15, 17, 21);">少样本提示的局限性</font>**<font style="color:rgb(15, 17, 21);">：虽然少样本提示能提升LLM输出质量，但在智能体系统中可能引发模型对历史模式的机械模仿，导致非最优决策。</font>
2. **<font style="color:rgb(15, 17, 21);">模式模仿的风险</font>**<font style="color:rgb(15, 17, 21);">：当上下文充满相似的行动-观察对时，模型会陷入固定行为节奏，在重复性任务中容易产生偏离、过度泛化或幻觉。</font>
3. **<font style="color:rgb(15, 17, 21);">具体案例说明</font>**<font style="color:rgb(15, 17, 21);">：Manus在简历审查任务中，因上下文示例单一，代理会重复相似行动模式而降低判断质量。</font>
4. **<font style="color:rgb(15, 17, 21);">解决方案</font>**<font style="color:rgb(15, 17, 21);">：通过行动和观察中引入结构化变化（如不同序列化模板、措辞调整、顺序或格式噪声）打破模式依赖，增强决策多样性。</font>
5. **<font style="color:rgb(15, 17, 21);">核心原则</font>**<font style="color:rgb(15, 17, 21);">：避免少样本学习的单一性陷阱，上下文的多样性直接影响智能体的适应性与鲁棒性。</font>







# 总结
:::color3
上下文工程仍然是一门新兴的科学——但对于智能体系统来说，它已经是必不可少的。模型可能变得更强大、更快速、更经济，但再多的原始能力也无法替代对记忆、环境和反馈的需求。你如何塑造上下文最终决定了你的智能体的行为方式：它运行的速度、恢复的效果以及扩展的范围。

在Manus，我们通过反复的重写、死胡同以及面向数百万用户的实际测试学到了这些经验。我们在这里分享的内容并非放之四海而皆准的真理——但这些是对我们有效的模式。如果它们能帮助你避免哪怕一次痛苦的迭代，那么这篇文章就达到了它的目的。

智能体的未来将一次构建一个上下文。好好设计它们吧。

:::

