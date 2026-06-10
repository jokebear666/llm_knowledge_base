# ① AutoResearch 四种常见循环和通用分析框架

<!-- source: yuque://zhongxian-iiot9/hlyypb/ge6y1z5k8tpwg45t -->

**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">核心命题</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">：AutoResearch = 基模 + Agent Loop。当基模固定时，</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">方法循环的设计就成了竞争的本质</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 244, 255);">。</font>

<font style="color:rgb(0, 0, 0);">这篇文章讲一下 AutoResearch 发展到现在的几种常见循环设计，以及一个通用的分析框架——当有新的 AutoResearch 方法出现时，你可以使用这个分析框架直接得出这个新方法的优劣势。</font><font style="color:rgb(100, 37, 208);">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084837735-605b47ba-270a-4753-b6ee-99e4ac5f0ae6.png)

## <font style="color:rgb(0, 0, 0);">🗺️</font><font style="color:rgb(0, 0, 0);"> 四种循环总览</font>
<font style="color:rgb(0, 0, 0);">四种循环按「探索能力」由弱到强演化：</font>**<font style="color:rgb(0, 0, 0);">线性 → 树搜索 → 遗传进化 → 异步多 Agent</font>**<font style="color:rgb(0, 0, 0);">。下图是全文导航。</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

**<font style="color:rgb(0, 0, 0);">线性循环</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084837780-01b64a23-4142-4e23-9b7e-fd7e47a3ab5b.png)![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084837791-83e3efee-b61c-47b7-92f0-6723a25d1b68.png)

**<font style="color:rgb(0, 0, 0);">树搜索循环</font>**

**<font style="color:rgb(0, 0, 0);">遗传进化池循环</font>**

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084837786-8bdeac9d-cc71-4b80-98cc-d8c0d4a95e08.png)![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084837791-a9e55975-cc49-4982-b091-6da813b2bb75.png)

**<font style="color:rgb(0, 0, 0);">异步多Agent循环</font>**

# <font style="color:rgb(0, 0, 0);">01 · 四种循环</font>
## <font style="color:rgb(0, 0, 0);">1.1 线性循环 Keep-or-Discard</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">代表系统</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：Karpathy autoresearch（2025）</font><font style="color:rgb(100, 37, 208);background-color:rgb(255, 245, 235);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">线性循环是最简单也最直觉的循环设计：每次尝试一个想法，如果结果更好就保留，否则回退。Karpathy 的 autoresearch 只有三个文件，循环逻辑由一个 Markdown 指令（</font>`<font style="color:rgb(0, 0, 0);">program.md</font>`<font style="color:rgb(0, 0, 0);">）定义。</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084838371-cc9a4b37-d72e-49a9-9681-c68551ecad3e.png)

<font style="color:rgb(0, 0, 0);">设计的最大亮点在于「</font>**<font style="color:rgb(0, 0, 0);">固定 5 分钟的时间预算</font>**<font style="color:rgb(0, 0, 0);">」这个约束选择，它迫使 Agent 思考的是"什么改动能在极短训练后就产生可测量的收益"，淘汰了那些需要训练很久才能看到效果的方案。人类的参与在编辑完</font><font style="color:rgb(0, 0, 0);"> </font>`<font style="color:rgb(0, 0, 0);">program.md</font>`<font style="color:rgb(0, 0, 0);">后达到了最小化，这个循环不会停下来问人类的意见，而是会自主执行，直到人类手动中断。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">简洁带来的结构性局限</font>**

1. <font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">它无法并行探索多个方向</font>
2. <font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">失败实验的经验没有被结构化保存（可能反复尝试同一个 idea 死循环）</font>
3. <font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">短时间约束容易让框架陷入局部最优</font>
4. <font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">只看最终指标这个标量反馈无法传达"为什么失败"，可解释性不够</font>

## <font style="color:rgb(0, 0, 0);">1.2 树搜索循环</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">代表系统</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：AIDE（2024）、AI Scientist v2（2025）</font><font style="color:rgb(100, 37, 208);background-color:rgb(255, 245, 235);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">树搜索的核心思想是：不要把解空间的探索限制在一条线性路径上，而是维护一棵搜索树，允许同时保持多个探索方向，并在任意节点发起新的分支。树的每个节点是一个完整的代码解决方案，边是代码变换操作。</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">树搜索相比线性循环的根本优势在于</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">回溯能力和方案多样性</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">。当某条路径走进死胡同时，线性循环只能通过</font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);"> </font>`<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">git reset</font>`<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">回到上一步然后尝试另一个方向，而树搜索可以回到树中</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">任意一个历史节点</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">重新出发。</font>

<font style="color:rgb(0, 0, 0);">听起来有点抽象，下面以 AIDE 的具体实现为例。AIDE 中的每个节点是一个完整的、可独立运行的 Python 脚本，是一个从数据加载到模型训练到输出指标的完整 ML pipeline。有三种算子类型（算子代表对节点的更改）：</font>

| **<font style="color:rgb(0, 0, 0);">算子</font>** | **<font style="color:rgb(0, 0, 0);">作用与 Prompt</font>** | **<font style="color:rgb(0, 0, 0);">关键点</font>** |
| :--- | :--- | :--- |
| **<font style="color:rgb(0, 0, 0);">Draft </font>****<font style="color:rgb(0, 0, 0);">草稿</font>** | <font style="color:rgb(0, 0, 0);">从零生成全新方案。Prompt 含：任务描述、当前所有成功方案的摘要（Memory）、"不要重复已有方案"的指令</font> | <font style="color:rgb(0, 0, 0);">每个 draft 尝试不同建模方向——第一个用 XGBoost，第二个用神经网络，第三个用特征工程+线性模型</font> |
| **<font style="color:rgb(0, 0, 0);">Debug </font>****<font style="color:rgb(0, 0, 0);">调试</font>** | <font style="color:rgb(0, 0, 0);">针对有 bug 的节点。Prompt 含：完整 buggy 代码、终端输出（报错与 traceback）、"修复 bug"的指令</font> | <font style="color:rgb(0, 0, 0);">修复后仍有 bug 可继续 debug（直到深度上限）</font> |
| **<font style="color:rgb(0, 0, 0);">Improve </font>****<font style="color:rgb(0, 0, 0);">改进</font>** | <font style="color:rgb(0, 0, 0);">针对已能正常运行的节点。Prompt 含：当前完整代码、所有成功方案摘要、"提出单一可验证改进"的指令</font> | <font style="color:rgb(0, 0, 0);">关键约束是</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">atomic improvement</font>**<font style="color:rgb(0, 0, 0);">——每次只改一个东西，便于清楚归因效果</font> |


<font style="color:rgb(0, 0, 0);">AIDE 认为有 bug 的节点代表已投入精力但尚未成功的探索方向，值得修复，所以会从有 bug 且为叶节点且调试深度没有达到上限的节点中随机选一个进行调试。如果存在好的节点，选择指标最好的那个节点，对其进行改进。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084838880-470f094e-cfaf-4af8-8221-841df5418bb0.png)

**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">选择策略的演进</font>**

**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">① 贪婪策略（AIDE）</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">：总是选当前最优节点做 improve。优势是收敛很快，但如果 Draft 1 很早就获得了好指标，后续所有 improve 都会集中在它的子树上，其他 draft 的子树被"饿死"。</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">② MCTS 选择（ML-Master 等）</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">：用 UCB 公式解决这个问题：</font>

<font style="color:rgb(0, 0, 0);">$$UCB(node) = \bar{r} + C \cdot \sqrt{\frac{\ln N_{total}}{N_{node}}$$</font>

<font style="color:rgb(0, 0, 0);">第一项倾向于已知的好节点（</font>**<font style="color:rgb(0, 0, 0);">利用</font>**<font style="color:rgb(0, 0, 0);">），第二项倾向于被访问次数少的节点（</font>**<font style="color:rgb(0, 0, 0);">探索</font>**<font style="color:rgb(0, 0, 0);">）。系数 C 控制二者的平衡。即使 Draft 5 的初始指标较差，只要被访问次数少，UCB 就会给它"好奇心加分"，使系统偶尔去探索它。</font>

**<font style="color:rgb(0, 0, 0);">③ Agent 自主（类似 AI Scientist v2）</font>**<font style="color:rgb(0, 0, 0);">：完全抛弃公式化的选择策略，让 Agent 自主判断"现在应该深耕哪个方向"，利用语义理解做出更智能的选择。</font>

## <font style="color:rgb(0, 0, 0);">1.3 遗传进化池循环</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">代表系统</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：FunSearch（2023）、AlphaEvolve（2024）、GEPA（2025）</font><font style="color:rgb(100, 37, 208);background-color:rgb(255, 245, 235);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">遗传进化的核心思想来自生物演化：维护一个候选种群，通过选择优秀个体、对其施加突变（在这里由 LLM 完成）、评估后代的适应度，逐代推动种群向更优方向进化。</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">与树搜索不同的是，进化池中的个体之间</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">没有严格的父子拓扑</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(254, 255, 240);">——任何个体都可以被选为突变的起点，多个个体可以被交叉组合。</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

**<font style="color:rgb(0, 0, 0);">FunSearch</font>**<font style="color:rgb(0, 0, 0);">（DeepMind, 2023）使用</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0);">MAP-Elites</font>**<font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">算法维护种群——不只保留最优个体，而是在多个行为维度的每个 niche 中都保留最优个体，从而维持种群的多样性。但在 FunSearch 中，所有搜索规则（选择策略、评估标准、种群管理）都是人工硬编码的，LLM 只负责变体生成。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/29769680/1781084838535-b2133355-dbb1-4153-93f2-14697da971a8.png)

**<font style="color:rgb(0, 0, 0);">GEPA（2025）用文本反馈取代</font>****<font style="color:rgb(0, 0, 0);">标量</font>****<font style="color:rgb(0, 0, 0);">奖励</font>**<font style="color:rgb(0, 0, 0);">来驱动突变方向。具体而言，系统先对当前候选进行 rollout，记录完整的执行轨迹（包括每一步的推理过程、工具调用和输出），然后让 LLM 阅读这些轨迹来诊断问题、归因原因、提出有针对性的修改方案。</font>

## <font style="color:rgb(0, 0, 0);">1.4 异步多 Agent 进化循环</font>
**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">代表系统</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(255, 245, 235);">：CORAL（2026）</font><font style="color:rgb(100, 37, 208);background-color:rgb(255, 245, 235);">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">前面三种循环本质上都是单一搜索过程（即使内部有多个角色参与，搜索的状态空间仍然是统一管理的）。以 CORAL 为代表的方法使用</font>**<font style="color:rgb(0, 0, 0);">多个 Agent 各自独立运行完整的搜索循环，通过共享持久记忆间接协调，无需任何显式通信协议</font>**<font style="color:rgb(0, 0, 0);">。</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">共享持久记忆</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">以文件系统的形式实现，分为三个目录：</font>

+ `<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">attempts/</font>`<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">存储所有历史评估记录（JSON 格式，按 commit hash 索引）</font>
+ `<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">notes/</font>`<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">存储观察和反思（Markdown 格式，支持合并和分类）</font>
+ `<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">skills/</font>`<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);"> </font><font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">存储可复用的过程和工具（包含自然语言描述和可执行脚本）</font>

<font style="color:rgb(0, 0, 0);background-color:rgb(246, 241, 254);">每个 Agent 通过符号链接访问共享记忆，按需读取以避免上下文过载，并且 Agent 可以主动整理和重组记忆结构。</font>

---

# <font style="color:rgb(0, 0, 0);">02 · 通用分析框架</font>
<font style="color:rgb(0, 0, 0);">在分析具体系统之前，先建立一个通用的分析框架。任何 AutoResearch 方法循环都可以从以下</font>**<font style="color:rgb(0, 0, 0);">四个维度</font>**<font style="color:rgb(0, 0, 0);">进行解构：</font>

<font style="color:rgb(0, 0, 0);">暂时无法在飞书文档外展示此内容</font>

| **<font style="color:rgb(0, 0, 0);">维度</font>** | **<font style="color:rgb(0, 0, 0);">决定了什么</font>** | **<font style="color:rgb(0, 0, 0);">演进谱系</font>** |
| :--- | :--- | :--- |
| **<font style="color:rgb(0, 0, 0);">🧭</font>****<font style="color:rgb(0, 0, 0);"> 搜索拓扑</font>** | <font style="color:rgb(0, 0, 0);">系统在解空间中的行走方式</font> | <font style="color:rgb(0, 0, 0);">线性路径（走一步保留或回退）→ 树形分支（多方向并随时回溯）→ 遗传池（种群选择突变演化）→ 异步并行（多 Agent 共享记忆间接协调）</font> |
| **<font style="color:rgb(0, 0, 0);">📡</font>****<font style="color:rgb(0, 0, 0);"> 反馈信号</font>** | <font style="color:rgb(0, 0, 0);">系统从每次实验中能学到多少</font> | <font style="color:rgb(0, 0, 0);">标量奖励（只知"好了多少"）→ 结构化指标（多维评估）→ 文本反馈（完整诊断：哪个模块出问题、哪种策略有潜力）</font> |
| **<font style="color:rgb(0, 0, 0);">🧠</font>****<font style="color:rgb(0, 0, 0);"> 记忆架构</font>** | <font style="color:rgb(0, 0, 0);">系统能否从历史中学习</font> | <font style="color:rgb(0, 0, 0);">无记忆 → Git 历史（可回溯但缺结构化查询）→ 解树（保留搜索完整拓扑）→ 文件系统池（多 Agent 并发读写）→ 知识图谱（最丰富语义结构、跨项目复利）</font> |
| **<font style="color:rgb(0, 0, 0);">🎮</font>****<font style="color:rgb(0, 0, 0);"> 决策主体</font>** | <font style="color:rgb(0, 0, 0);">"谁在控制搜索过程"</font> | <font style="color:rgb(0, 0, 0);">人类硬编码所有搜索规则、LLM 只是被调用的突变算子 → Agent 逐步获得决定搜索策略的自主权（选方向、何时放弃、如何综合经验）</font> |


**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">怎么用这个框架</font>**<font style="color:rgb(0, 0, 0);background-color:rgb(240, 251, 239);">：拿到一个新方法，依次问这四个问题——它的搜索拓扑是哪种？反馈信号有多丰富？记忆架构能否复用历史？决策主体是人还是 Agent？四个答案一组合，优劣势就自然浮现。信息越丰富、自主性越高，下一步决策的质量就越高，但获取和处理的成本也越大。</font>

---

**<font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">参考</font>**

1. <font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">https://github.com/karpathy/autoresearch</font>
2. <font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">https://arxiv.org/abs/2403.17373</font>
3. <font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">https://github.com/SakanaAI/AI-Scientist-v2</font>
4. <font style="color:rgb(0, 0, 0);background-color:rgb(245, 246, 247);">DeepMind · FunSearch Blog</font>

