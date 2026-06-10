# ⓸ LLM在推荐系统的应用

<!-- source: yuque://zhongxian-iiot9/hlyypb/bgt7h0i56gkl8rai -->

:::color1
如何在推荐领域应用大模型，业界有不少研究和相关工作，大致可以分为2个方向：(1) scaling law；(2) 多模态。

:::

推荐模型scaling law

受大语言模型scaling law的启发，不少从业者研究如何将推荐模型本身做大做复杂，使得scaling law在推荐模型上也成立。业界当前难以在推荐模型上看到scaling law，不少工作在扩大模型容量后，并未看到效果对应的提升，关于这点的实际尝试和思考，在后续会分享。因此，业界提出一些新的思路将推荐模型本身做大，如meta提出的两种思路，一种是对模型按模块堆叠，另一种是在框架设计上进行生成式地推荐。具体的分享在推荐大模型系列，戳

+ [大模型 | meta2024 wukong: 推荐模型本身如何做大](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/ZsjKX22crbcs1BqW6VKDyQ)
+ [大模型 | meta2024 wukong: 实际应用及其对推荐模型做大的启发](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/2g-KrRDLViSbR4OHAWuQIw)
+ [大模型 | meta [ICML2024]: 生成式推荐，开辟新方向](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/uGsNC3Uc5o8A0xgpuzDo6w)



# LLM表征
## <font style="color:rgb(25, 27, 31);">阿里 SCL & SimTier & MAKE：多模态表征在广告CTR预估上的应用</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">现阶段推荐系统很大程度上依赖于</font>[<font style="color:rgb(9, 64, 142);">ID特征</font>](https://zhida.zhihu.com/search?content_id=248702958&content_type=Article&match_order=1&q=ID%E7%89%B9%E5%BE%81&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的学习, 探索多模态表征在推荐系统中的落地应用被认为是缓解该问题的有效手段之一。</font>**<font style="color:#74B602;">多模态表征能够为推荐系统引入一定的语义信息, 而这通常是ID特征难以刻画的。</font>**

<font style="color:rgb(25, 27, 31);">出于训练成本以及收敛速度的考虑, 多模态表征在推荐系统中的应用一般是two-stage的, 首先是</font>**<font style="color:#74B602;">预训练得到多模态表征, 然后是将预训练后的多模态表征与推荐系统融合</font>**<font style="color:rgb(25, 27, 31);">。因此, 将多模态表征应用于推荐系统需要重点解决两类问题:</font>

1. **<font style="color:rgb(25, 27, 31);">如何设计预训练任务以获取高质量的多模态表征:</font>**<font style="color:rgb(25, 27, 31);"> 推荐系统是业务目标驱动的, 如果直接</font>**<font style="color:#117CEE;">使用不加业务数据训练/微调的多模态表征, 最终在应用效果上可能会大打折扣</font>**<font style="color:rgb(25, 27, 31);">, 甚至可能因为引入了与推荐任务无关的噪声信号, 导致数据负向。</font>
2. **<font style="color:rgb(25, 27, 31);">如何将多模态表征融合到ID特征主导的推荐模型:</font>**<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:#117CEE;">多模态表征与ID模态表征存在着</font>**[**<font style="color:#117CEE;">语义鸿沟问题</font>**](https://zhida.zhihu.com/search?content_id=248702958&content_type=Article&match_order=1&q=%E8%AF%AD%E4%B9%89%E9%B8%BF%E6%B2%9F%E9%97%AE%E9%A2%98&zhida_source=entity)**<font style="color:#117CEE;">, 将多模态表征直接当作特征在推荐系统上使用, 大多数是没有收益的</font>**<font style="color:rgb(25, 27, 31);">。此外, 多模态表征的维度一般都比较高, 落地应用还需要额外的工程能力支持, 如何在成本可控的约束下引入多模态表征进行训练和推理也是一个不小的技术挑战。</font>

<font style="color:rgb(25, 27, 31);">基于这两类问题, 论文提出了如下图所示的</font>[<font style="color:rgb(9, 64, 142);">两阶段训练框架</font>](https://zhida.zhihu.com/search?content_id=248702958&content_type=Article&match_order=1&q=%E4%B8%A4%E9%98%B6%E6%AE%B5%E8%AE%AD%E7%BB%83%E6%A1%86%E6%9E%B6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">, 下面分别介绍。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**淘宝引入了一个两阶段框架，包括：

+ **SCL（Semantic-aware Contrastive Learning）**：语义感知的对比学习，对多模态表示进行预训练以捕捉语义相似性。
+ **SimTimer & MAKE**：将这些表示与现有的基于ID的模型集成。

**paper：**[**https://arxiv.org/pdf/2407.19467**](https://arxiv.org/pdf/2407.19467)

**参考：**[**CIKM'24 | 淘宝: 多模态表征在广告CTR预估上的新突破**](https://zhuanlan.zhihu.com/p/741012720)**  **[**基于原生图文信息的多模态预估模型**](https://mp.weixin.qq.com/s/XWMOSypjF9XrwqwZsEXF7g)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743408367063-d1dae6d7-c47e-46f3-b906-4217df41661b.png)

### 预训练多模态表征<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介**：<font style="color:rgb(25, 27, 31);">直接使用通用的多模态表征</font>**<font style="color:#117CEE;">可能无法细粒度刻画出在模态上对用户行为可能很重要的细微差异</font>**<font style="color:rgb(25, 27, 31);">, 如下图所示, 最左侧是用户搜索的图片, 中间和右侧是视觉模态上非常接近的两个图片, 但相比而言, 左图与中间图在图案上相对于右图更一致, </font>**<font style="color:#117CEE;">这些细微差别如果不引入场景数据学习, 可能很难被捕获到。</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744169902781-2728f265-de4a-4827-883e-d3278051a1cb.png)

:::color5
**<font style="color:#601BDE;">1.正样本构造（相似样本） </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">要让表征能够学习到</font>**<font style="color:#74B602;">度量场景特点的语义相似度</font>**<font style="color:rgb(25, 27, 31);">, 最核心的是如何定义构造语义相似(正样本)和不相似(负样本)的样本对。</font>

<font style="color:rgb(25, 27, 31);">相似样本需要结合用户行为来构造, 在电商场景, 用户的</font>**<font style="color:#74B602;">搜索-购买行为链</font>**<font style="color:rgb(25, 27, 31);">可以用来定义语义相似商品Pair</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744170499786-30f0ca03-f6e1-4ca7-a2f3-ee803e58aab4.png)

+ <font style="color:rgb(25, 27, 31);">对于图片, 可以拿用户搜索的图片, 与用户最终所购买的商品的图片, 作为视觉模态的正样本Pair。</font>
+ <font style="color:rgb(25, 27, 31);">对于文本, 也是类似, 拿用户搜索的文本, 与用户最终所购买商品的文本描述作为文本模态的正样本Pair。</font>

<font style="color:rgb(25, 27, 31);">同时, 作者认为, 像swing i2i这样常见的基于用户行为定义的相似度指标, 可能并不适合作为多模态预训练的label, 因为这样可能会导致</font>**<font style="color:#2F4BDA;">多模态Encoder的学习退化为ID表征</font>**<font style="color:rgb(25, 27, 31);">，学习不到商品的多模态语义信息。</font>

:::color5
**<font style="color:#601BDE;">2.负样本构建 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">in-batch负采样</font>**<font style="color:rgb(25, 27, 31);">：负样本的构造最简单的方式就是in-batch负采样, 但这种方式会</font>**<font style="color:#2F4BDA;">受限于batch size的大小</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">MoCo动量更新</font>**<font style="color:rgb(25, 27, 31);">：通常认为, 扩大负样本的数量可以进一步提升效果。因此, 作者参考MoCo的动量更新方法, 设置了个</font>**<font style="color:#74B602;">更大的memory bank用于采样更多的负样本</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">难负样本</font>**<font style="color:rgb(25, 27, 31);">：此外, 作者还额外增加了一些难负样本的学习, 作者把一次搜索返回的结果中, 把那些</font>**<font style="color:#74B602;">被用户点击但没有购买行为的商品所对应的图片, 作为难负样本</font>**<font style="color:rgb(25, 27, 31);">, 认为它们与正样本具有一定的视觉相似, 但又有一些差别。</font>

:::color5
**<font style="color:#601BDE;">3.训练 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744170698242-8fdcb19a-dbbf-4a57-a8ab-b075b63e5aa6.png)  


  
**<font style="color:rgb(25, 27, 31);">对比学习</font>**<font style="color:rgb(25, 27, 31);">：对于普通的负样本, 作者使用InfoNCE损失, 以期在表征空间拉近语义相似样本对的距离，疏远语义不相似样本对的距离。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744170804635-1b9a1290-5c8a-4992-a9e9-d4bab67de73b.png)

> <font style="color:rgb(25, 27, 31);">τ</font><font style="color:rgb(25, 27, 31);">为温度系数</font>
>
> <font style="color:rgb(25, 27, 31);">K</font><font style="color:rgb(25, 27, 31);">是memory bank的大小, 作者设置为196800</font>
>

**Triplet损失：**<font style="color:rgb(25, 27, 31);">对于难负样本, 作者使用</font>**<font style="color:#74B602;">Triplet损失</font>**<font style="color:rgb(25, 27, 31);">强化正负样本的距离差距。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735808961-9670d114-6037-4ac9-aed2-01ca8aa2bf87.png)

> _<font style="color:rgb(51, 51, 51);">a</font>_<font style="color:rgb(51, 51, 51);">: Anchor样本（基准样本）</font>
>
> <font style="color:rgb(51, 51, 51);">p</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">: Positive样本（同类样本）</font>
>
> <font style="color:rgb(51, 51, 51);">n</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">: Negative样本（异类样本）</font>
>
> <font style="color:rgb(51, 51, 51);">d(⋅): 距离度量（通常用余弦距离）</font>
>
> <font style="color:rgb(51, 51, 51);">α: 边际参数(margin)，控制正负样本间距</font>
>

<font style="color:rgb(25, 27, 31);">最后, 将两者进行按一定超参进行融合</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744170848536-53f659b2-05a3-4d9d-9c20-14d46cfb2eac.png)



### 多模态表征应用**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">最直接使用多模态表征的方式, 是在对用户行为序列做Target Attention时, </font>**<font style="color:#ECAA04;">将多模态表征和ID Embed一起Concat起来使用</font>**<font style="color:rgb(25, 27, 31);">, 但作者发现, 这种方式可能有些</font>**<font style="color:#117CEE;">"费力不讨好"</font>**<font style="color:rgb(25, 27, 31);">, 作者给出了下面的一些观察与思考。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743408367063-d1dae6d7-c47e-46f3-b906-4217df41661b.png)

<font style="color:rgb(25, 27, 31);">作者分别提出了</font>[<font style="color:rgb(9, 64, 142);">SimTier方法</font>](https://zhida.zhihu.com/search?content_id=248702958&content_type=Article&match_order=1&q=SimTier%E6%96%B9%E6%B3%95&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和</font>[<font style="color:rgb(9, 64, 142);">MAKE方法</font>](https://zhida.zhihu.com/search?content_id=248702958&content_type=Article&match_order=1&q=MAKE%E6%96%B9%E6%B3%95&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">SimTier (Similarities between Target Item and user Interacted)</font>**<font style="color:rgb(25, 27, 31);">：通过构造</font>**<font style="color:#74B602;">语义相似度分布来简化多模态表征的使用方式</font>**<font style="color:rgb(25, 27, 31);">。</font>
+ **<font style="color:rgb(25, 27, 31);">MAKE</font>**** (MultimodAl Knowledge Extractor)**<font style="color:rgb(25, 27, 31);">：通过构造插件式的多模态模块, 将与</font>**<font style="color:#74B602;">多模态表征相关参数的优化与其他参数优化分离开来</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">1.SimTier & MAKE模块结构图 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744171591210-de8a82a7-f97a-4609-989a-eb35219514e7.png)

:::color5
**<font style="color:#601BDE;">2.SimTier方法：构造语义相似度分布 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">SimTier的思想是通过构造</font>**<font style="color:#74B602;">Target Item与用户行为序列的语义相似度分桶的频次分布</font>**<font style="color:rgb(25, 27, 31);">, 然后把这个</font>**<font style="color:#74B602;">分布当作特征来使用</font>**<font style="color:rgb(25, 27, 31);">。下面结合一个例子来解释。</font>

1. **<font style="color:rgb(25, 27, 31);">相似度计算</font>**<font style="color:rgb(25, 27, 31);">：假设target Item的多模态表征为</font><font style="color:rgb(25, 27, 31);">v</font><sub><font style="color:rgb(25, 27, 31);">c</font></sub><font style="color:rgb(25, 27, 31);">, 用户的行为序列长度为100, 可以基于</font><font style="color:rgb(25, 27, 31);">v</font><sub><font style="color:rgb(25, 27, 31);">c</font></sub><font style="color:rgb(25, 27, 31);">与这100个行为序列所对应的多模态表征分别计算Cos相似度得分, 这样会得到范围在[-1.0, 1.0]的100个相似度分数,</font>
2. **<font style="color:rgb(25, 27, 31);">频次分桶</font>**<font style="color:rgb(25, 27, 31);">：基于预设定的等宽分桶后, 如按0.1大小分成20个分桶, 就会得到20个频次统计分布, 如(3, 2, ..., 0, 3)这样20维大小的数据, 然后再把这</font>**<font style="color:#74B602;">20维的数据作为特征与其它ID Embed一起使用</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">作者还很贴心地给出了TensorFlow版的伪代码实现, 其实核心就4行代码实现也是相当直接。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744171880451-ec24d45c-a569-47a9-954b-f79e0b880545.png)

:::color5
**<font style="color:#601BDE;">3.MAKE方法 (MultimodAl Knowledge Extractor)：解耦多模态表征和ID特征的优化过程 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">为了克服</font>**<font style="color:#117CEE;">多模态序列建模与ID序列建模训练收敛不一致的问题,</font>**<font style="color:rgb(25, 27, 31);"> 作者单独为多模态序列建模的多模块知识抽取模块(</font>**<font style="color:rgb(25, 27, 31);">M</font>**<font style="color:rgb(25, 27, 31);">ultimod</font>**<font style="color:rgb(25, 27, 31);">A</font>**<font style="color:rgb(25, 27, 31);">l </font>**<font style="color:rgb(25, 27, 31);">K</font>**<font style="color:rgb(25, 27, 31);">nowledge </font>**<font style="color:rgb(25, 27, 31);">E</font>**<font style="color:rgb(25, 27, 31);">xtractor, MAKE), 将与</font>**<font style="color:#74B602;">多模态表征相关参数的优化与其他参数优化分离开来, 以支持多模态模块的多Epoch训练</font>**<font style="color:rgb(25, 27, 31);">。MAKE 模块包括以下两个步骤:</font>

1. **<font style="color:rgb(25, 27, 31);">多Epoch训练纯多模态序列建模模块</font>**

<font style="color:rgb(25, 27, 31);">这一部分使用了常规的DIN, 只是将ID Embed替换成多模态表征。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744172275986-e69d280e-080d-47f2-8c61-7603723685bc.png)

2. **<font style="color:rgb(25, 27, 31);">多模态知识与ID模型融合</font>**

<font style="color:rgb(25, 27, 31);">为了让ID模型主导的模型也能融合多模态知识, 作者将DIN的输出</font><font style="color:rgb(25, 27, 31);">v</font><sub><font style="color:rgb(25, 27, 31);">MAKE</font></sub><font style="color:rgb(25, 27, 31);">, MAKE模块浅层MLP的中间层输出, 以及最后的Logits</font>**<font style="color:#74B602;">分别与ID模型对应地进行拼接</font>**<font style="color:rgb(25, 27, 31);">, 再进行联合训练。</font>

### 在线部署 **<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(25, 27, 31);">简介</font>**<font style="color:rgb(25, 27, 31);">：将多模态表征应用于推荐, 不仅是算法层面上的问题, 对工程实现也有一定的挑战。阿里的工程能力还是很耐打的, 作者自述新商品/新广告从创建到对应表征可以被下游应用的时延已经降低至秒级，多模态特征覆盖率提升至99%+, 下面是所对应线上应用的流程图。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744172473659-926ee874-7eff-4d79-a822-c695160df528.png)

为了最大化多模态表征的效果，我们需要保障多模态表征在用户行为序列侧和target商品侧的特征覆盖率。这要求我们构建高效的实时表征产出能力，使得新建商品/广告能够迅速请求多模态encoder生成表征，供模型训练和在线预测使用。

为此，我们也对系统架构进行了升级，如图所示，在接收到上游触发源（新商品/新广告）的消息后，我们会请求多模态encoder模型，实时推理得到商品主图/广告创意embedding，并写入多模态索引表。下游ODL训练任务和在线预估引擎可以从索引中查询表征进行应用。通过表征实时推理能力的建设，，新商品/新广告从创建到对应表征可以被下游应用的时延降低至秒级，多模态特征覆盖率提升至99%以上 - 这不仅提升了多模态表征的效果，还大大缓解了新广告的冷启动问题。

自2023年中期以来，原生图像、文本表征已经在阿里妈妈展示广告系统中的粗排、精排和融合模型中全量上线，带来了显著的业务收益。例如，在精排CTR预估模型中引入图像表征取得大盘CTR+3.5%，RPM+1.5%，ROI+2.9%的提升。特别地，对于新广告（创建时间在最近24小时内）提升更加显著，CTR+6.9%，RPM+3.7%，ROI+7.7%，这也验证了多模态信息在缓解冷启动问题上的效果。

### 实验分析**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.预训练对比 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

我们将SCL与其他一系列广泛应用的预训练方法进行了对比。

+ CLIP-O：基于通用数据集预训练的CLIP模型；
+ CLIP-E：在电商场景中基于CLIP-O模型进行微调的版本，使用对齐的商品描述和商品图片；
+ SCL：本文提出的语义感知的对比学习方法。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744172789718-8ae3c97a-dc9c-419a-ae0d-b15a79b79042.png)

各个预训练方法的效果对比详见图8。从中我们可以得到两个结论。首先，SCL预训练方法优于其他不考虑语义相似性的方法，这显示了语义感知预训练的必要性。其次，Momentum Contrast（MoCo）和Triplet loss（引入hard negative）等负样本增强技术可以进一步提升多模态表征的质量，这说明负样本的选择对表征质量有很大影响。

:::color5
**<font style="color:#601BDE;">2.CTR预估模型对比 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

我们将SimTier和MAKE与其他方法进行了对比，包括

+ 基于ID的生产基线模型（ID-based model）；
+ 原始表征应用（vector）方法，即直接引入原始embedding，进行target attention等计算；
+ 相似度方法（SimScore）：SimScore方法可以看作是Vector方法的简化版本。它将每个历史行为与Target的相似度作为辅助信息引入模型。

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1744172877126-6ccf91dd-ed2a-4288-8045-529ef642f486.webp)

图9. 不同多模态应用方法的对比。

实验结果如图9所示，从中我们可以得到两个结论，首先SimTier和MAKE显著优于其他方法。其次，SimTier和MAKE叠加后可以进一步提升预估效果，相比于基于ID的模型，GAUC提升+1.25%，AUC提升+0.75%。此外我们也验证了多模态表征对于长尾商品的帮助，更详尽的实验分析见论文6.3。



## 快手LEARN：<font style="color:rgb(25, 27, 31);">LLM Embedding用于电商广告推荐</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">现有推荐系统主要还是依赖ID Embed, 这导致在长尾内容和冷启动场景中效果欠佳。随着近年来LLM的突破性进展, 利用LLM强大的内容理解能力辅助推荐被认为是缓解该问题的一个有效途径。</font>

<font style="color:rgb(25, 27, 31);">作者提到, 现阶段很多文献都是基于"</font>[<font style="color:rgb(9, 64, 142);">Rec-to-LLM</font>](https://zhida.zhihu.com/search?content_id=252967539&content_type=Article&match_order=1&q=Rec-to-LLM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">"的思路来实现的,这种方法通常将推荐域(目标域)的</font>[<font style="color:rgb(9, 64, 142);">User-Item交互数据</font>](https://zhida.zhihu.com/search?content_id=252967539&content_type=Article&match_order=1&q=User-Item%E4%BA%A4%E4%BA%92%E6%95%B0%E6%8D%AE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">转换成LLM开放世界(源域)的文本格式，并设计特定任务的提示，将推荐数据转换为会话格式，以兼容LLM的处理模式。但是, 这种方法存在比较多的缺点:</font>

+ **<font style="color:rgb(25, 27, 31);">计算效率太低:</font>**<font style="color:rgb(25, 27, 31);"> 推荐场景下用户的行为序列是非常长的, </font>**<font style="color:#117CEE;">LLM在处理这么长的用户行为序列非常低效</font>**<font style="color:rgb(25, 27, 31);">, 无法满足业务落地应用的性能要求。</font>
+ **<font style="color:rgb(25, 27, 31);">灾难性遗忘:</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">推荐系统是User-Item的协同数据主导的, 而LLM学习的是开放世界知识, 这两类知识信息存在非常大的差异, 这样基于用户行为数据去微调LLM常会导致灾难性遗忘开放世界知识。</font>
+ **<font style="color:rgb(25, 27, 31);">性能下降:</font>**<font style="color:rgb(25, 27, 31);"> LLM的预训练目标是下一词元预测, 而推荐系统依赖User-Item的协同, 这种训练目标上的不一致性, 使得LLM不能很好的适应推荐任务。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了克服这些问题, 作者提出了基于"LLM-to-Rec"的思路的LEARN方法(LLM-Driven Knowledge Adaptive Recommendation)。</font>**<font style="color:#ED740C;">这种方法使用LLM做特征抽取, 让抽取出来的信息去适应推荐系统本身的训练目标,</font>**<font style="color:rgb(25, 27, 31);"> 更好的兼容推荐系统并满足实际业务落地的性能要求。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**paper：**[**LEARN: Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application**](https://arxiv.org/pdf/2405.03988)

**参考：**[**https://zhuanlan.zhihu.com/p/19726061487**](https://zhuanlan.zhihu.com/p/19726061487)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134289047-fb89cc86-35a3-47d3-bd82-f06932ff27ac.png)

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">作者所提LEARN方法的整体框架如下图所示, 它是一个双塔结构的模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134418336-c59fd089-820d-4e4c-b79c-87e7e0fbfe80.png)

> 我们的LLM驱动的knowledge自适应推荐（LEARN）框架的说明。LEARN框架采用双塔架构，包括User塔和Item塔。User塔处理历史交互以生成用户嵌入E<sup>user</sup>，而Item塔处理目标交互以生成item嵌入E<sup>item</sup>。User塔和Item塔（a）利用因果注意机制。Item塔（b）采用self-attention机制。在没有偏好对齐模块的情况下，Item Tower（c）直接利用内容嵌入作为Item embedding。
>

<font style="color:rgb(25, 27, 31);">可以看到, 这里会将用户历史行为序列将时间排序后再截断成两部分, 前面部分称为历史交互序列</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134352888-4ac87a3b-fe03-45d1-8b5b-4a65f19d6850.png)

<font style="color:rgb(25, 27, 31);">作为用户塔的输入, 后面部分作者把它称为target交互序列</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134365959-5faba9a1-49b0-4d12-a5ba-cbde62c75b39.png)<font style="color:rgb(25, 27, 31);"> </font>

<font style="color:rgb(25, 27, 31);">会作为Item塔的输入。</font>

:::color5
**<font style="color:#601BDE;">2.User塔</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">User塔由两个模块组成, 分别是内容抽取模块和偏好对齐模块, 如下图所示:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134738511-1f06ecbe-587b-447c-bc6d-b67a2ad98a4e.png)

1. **内容抽取模块（CEX， Context Extraction Module）**

<font style="color:rgb(25, 27, 31);">对于用户行为序列</font><font style="color:rgb(25, 27, 31);">U</font><sup><font style="color:rgb(25, 27, 31);">hist</font></sup><font style="color:rgb(25, 27, 31);">中的每个Item, 先按下图的提示组织其文本描述(包括</font>**<font style="color:#74B602;">标题、类别、品牌、价格、关键词和属性</font>**<font style="color:rgb(25, 27, 31);">):</font>

```python
Item Prompt:
    The item information is given as follows. Item title is "{Title}". This item belongs to "{Category}" and brand is "{Brand}". The price is "{Price}". The key words of items are "{Keywords}". The item supports "{Attributes}".
```

<font style="color:rgb(25, 27, 31);">然后, 将这些Item描述输入到参数冻结的预训练LLM(论文使用了</font>[<font style="color:rgb(9, 64, 142);">Baichuan2-7B</font>](https://zhida.zhihu.com/search?content_id=252967539&content_type=Article&match_order=1&q=Baichuan2-7B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)中, 然后再将最后一层的</font>**<font style="color:#74B602;">隐层向量做AvgPooling后得到该Item最后的内容表征</font>****<font style="color:#74B602;">E</font>**<sup>**<font style="color:#74B602;">c</font>**</sup><font style="color:rgb(25, 27, 31);">。</font>

2. **偏好对齐模块（PAL, Preference Alignment Module）**

<font style="color:rgb(25, 27, 31);">使用前面处理的用户历史行为内容表征序列</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134986118-4662e5a1-f5e2-4fa4-aeda-235ae1b95777.png)<font style="color:rgb(25, 27, 31);">为输入, 先通过内容映射层做维度变换, 再将它们输入到类似因果注意力机制的Transformer编码器中, 最后使用线性映射降维(至64维)得到User Embed </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745134997039-42152069-56c2-4abc-aed9-05d7d0407578.png)<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.Item塔</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Item塔以</font><font style="color:rgb(25, 27, 31);">U</font><sub><font style="color:rgb(25, 27, 31);">i</font></sub><sup><font style="color:rgb(25, 27, 31);">tar</font></sup><font style="color:rgb(25, 27, 31);">为输入, 同样也是先过前面的内容抽取模块(CEX), 只是后面这里有3个变种:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745135289821-6e7765f5-f2f5-4ab3-88da-3a9fa0471c85.png)![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745135337672-447312b6-2ff4-4109-be29-92c42c60f1a4.png)

+ **<font style="color:rgb(25, 27, 31);">变体1:</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">采用与User塔相同的架构和权重, 都使用了因果注意力机制, 只是这里不是处理用户历史交互序列, 而是Target交互序列</font>
+ **<font style="color:rgb(25, 27, 31);">变体2:</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">同样也是采用与User塔相同的架构和权重, 只是把因果注意力机制替换成只关注自己的内容本身的自注意力机制</font>
+ **<font style="color:rgb(25, 27, 31);">变体3:</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">使用内容Embed作为Item Embed，直接跳过对齐模块</font>

<font style="color:rgb(25, 27, 31);">这样, 变体1相当于让User塔与Item塔去做sequence-to-sequence的对齐, 变体2相当于让User塔与Item塔去做sequence-to-item的对齐, 而变体3相当于要让可学习的User塔去匹配冻结LLM输出的Item塔, 属于Rec-to-LLM的模式。</font>

<font style="color:rgb(25, 27, 31);">在训练时, 变体1会将整个用户Target交互序列</font><font style="color:rgb(25, 27, 31);">U</font><sup><font style="color:rgb(25, 27, 31);">tar</font></sup><font style="color:rgb(25, 27, 31);">作为输入，而变体2和变体3则是独立处理Target交互序列的每个Item。而在推理时, 这3个变体都只输入单个Item去生成Item Embedding。</font>

<font style="color:rgb(25, 27, 31);">后面的实验效果上, </font>**<font style="color:#74B602;">变体1>变体2>变体3</font>**<font style="color:rgb(25, 27, 31);">。变体3最差挺好理解的, 毕竟是Rec-to-LLM的范式, 而变体1比变体2好, 作者的解释是"We believe that LEARN with ItemTower(a), which uses sequence-to-sequence alignment, allows the model to better capture long-term user interests compared to the sequence-to-item alignment used in ItemTower(b)"。坦白说, 笔者并不认可这种解释, 笔者认为变体1和变体2在现有数据集方式下的比较本身就不公平。作者的数据集是直接拆分出了前后两个seq, 那变体1使用了因果注意力机制自然是能更好的适配这种seq-2-seq的数据, 而变体2更接近next item prediction的模式, 本身就不是很兼容, 如果把数据集处理成能兼容next item prediciton的方式, 变体2的效果不一定会比变体1差, 只能说是在作者设定的训练数据集的处理方式下, </font>**<font style="color:#74B602;">变体1会比变体2更适配训练数据</font>**<font style="color:rgb(25, 27, 31);">。而之所以使用拆分成前后两个序列, 主要是因为下面作者的训练Loss(Pinterest提出的dense all action loss)是用了从前后两个序列采样去做对比学习的训练方式。</font>

:::color5
**<font style="color:#601BDE;">4.训练目标</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在Loss上, 作者使用</font>[<font style="color:rgb(9, 64, 142);">PinnerFormer</font>](https://zhida.zhihu.com/search?content_id=252967539&content_type=Article&match_order=1&q=PinnerFormer&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的dense all action loss。具体的, 作者会从同一用户的历史交互序列</font><font style="color:rgb(25, 27, 31);">U</font><sup><font style="color:rgb(25, 27, 31);">hist</font></sup><font style="color:rgb(25, 27, 31);">中采样了</font><font style="color:rgb(25, 27, 31);">N</font><sup><font style="color:rgb(25, 27, 31);">h</font></sup><font style="color:rgb(25, 27, 31);">个Item(默认为10), 再从该用户的Target交互序列</font><font style="color:rgb(25, 27, 31);">U</font><sup><font style="color:rgb(25, 27, 31);">tar</font></sup><font style="color:rgb(25, 27, 31);">中采样了</font><font style="color:rgb(25, 27, 31);">N</font><sup><font style="color:rgb(25, 27, 31);">t</font></sup><font style="color:rgb(25, 27, 31);">个Item(默认为10), 总共构造出</font><font style="color:rgb(25, 27, 31);">N</font><sub><font style="color:rgb(25, 27, 31);">h</font></sub><font style="color:rgb(25, 27, 31);">×N</font><sub><font style="color:rgb(25, 27, 31);">t</font></sub><font style="color:rgb(25, 27, 31);">个正样本pair, 再与同一批次中其他用户的Target Item Embedding构造出数量为共</font><font style="color:rgb(25, 27, 31);">N</font><sub><font style="color:rgb(25, 27, 31);">h</font></sub><font style="color:rgb(25, 27, 31);">×(bs−1)</font><font style="color:rgb(25, 27, 31);">的负样本pair。这里的采样策略下面会介绍。</font>

<font style="color:rgb(25, 27, 31);">再使用对比学习计算对应的Loss:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745135579086-d101b27f-280e-4df7-8677-b8490e0c3bc4.png)

:::color5
**<font style="color:#601BDE;">5.采样策略</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在短视频场景下, 用户交互序列是非常长的, 作者做了前面两阶段采样:</font>

+ **<font style="color:rgb(25, 27, 31);">Stage1:</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">从完整的用户历史/目标交互中执行随机抽样，作为用户塔的输入，确保用于建模用户兴趣的数据是无偏的。</font>
+ **<font style="color:rgb(25, 27, 31);">Stage2:</font>**<font style="color:rgb(25, 27, 31);"> 在构造正负样本pairs时, 使用样本</font>**<font style="color:#74B602;">加权采样方式以提高近期交互Item的采样概率</font>**<font style="color:rgb(25, 27, 31);">, 因为这更能反应用户的当前兴趣并且与用户偏好的Target Item更相关。这里第</font><font style="color:rgb(25, 27, 31);">i</font><font style="color:rgb(25, 27, 31);">个Item的采样概率设为:</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745135713781-641460fc-6f97-4aec-9a60-b83e3eb78208.png)<font style="color:rgb(25, 27, 31);">。其中, </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745135720485-fa941a91-57f2-4316-a15a-04fe88cbff11.png)<font style="color:rgb(25, 27, 31);">, 超参</font><font style="color:rgb(25, 27, 31);">α</font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">分别设置为10和10000, 而</font><font style="color:rgb(25, 27, 31);">N</font><font style="color:rgb(25, 27, 31);">是从Stage1采样后的序列长度。</font>

:::color5
**<font style="color:#601BDE;">6.如何在精排中使用</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">前面的双塔框架是用于召回, 作者还将这些User Embed和Item Embed用于精排模型做特征增强化, 不过这里不是直接拿它去使用, 而是在前置环节做了适配, 用了</font>[<font style="color:rgb(9, 64, 142);">CVR任务</font>](https://zhida.zhihu.com/search?content_id=252967539&content_type=Article&match_order=1&q=CVR%E4%BB%BB%E5%8A%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">来辅助学习这里的融合机制, 具体见下图:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745135880929-483c5e1c-047e-4c00-bb15-074b70a315dc.png)

<font style="color:rgb(25, 27, 31);">这里有意思的地方是, 为什么是CVR任务, 而不是CTR任务呢。这里笔者的理解是, 由于这里的输入主要是</font>**<font style="color:#74B602;">商品详情页的内容信息, 这些内容信息与转化肯定是更相关</font>**<font style="color:rgb(25, 27, 31);">, 但是如果是图片这种容易骗点击的模态信息的话, 那监督信号就应该用CTR了。</font>

:::color5
**<font style="color:#601BDE;">7.实验</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">与各baseline模型的对比</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136060491-c5f661ad-647c-47e1-9146-a2fa4a890035.png)

+ <font style="color:rgb(25, 27, 31);">NDCG指标</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136085988-8c032d01-0b60-4306-b185-2fce9abd47b0.png)

<font style="color:rgb(25, 27, 31);">LLM embedding对比ID、bert生成的Embedding</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136111949-a5e4ca63-0e2b-4649-8d47-3a465da0c95e.png)

<font style="color:rgb(25, 27, 31);">精排模型的AUC指标</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136164084-e58a6410-36ca-416e-992f-8798fcaf0864.png)

<font style="color:rgb(25, 27, 31);">PAL模块不同规模参数的LLM的表现</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136128430-fff78927-e72a-4618-aaa6-c4f45192589c.png)

<font style="color:rgb(25, 27, 31);">拆分冷启和长尾的提升</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136169968-7f5594be-e538-4b3f-870b-c43721c30bf2.png)

+ <font style="color:rgb(25, 27, 31);">整体CVR和收入提升</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745136180161-9cade44d-7247-4ea3-8c97-469e40139189.png)<font style="color:rgb(25, 27, 31);">  
  
</font>

# <font style="color:rgb(51, 51, 51);">生成式推荐</font>
## 快手<font style="color:rgb(0, 0, 0);">OneRec</font><font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(0, 0, 0);">现代推荐通常遵循着</font>**<font style="color:#74B602;">"召回-粗排-精排"这样多层级联的范式, 以平衡系统时延和精度, </font>**<font style="color:rgb(0, 0, 0);">而生成式推荐系统则是希望</font>**<font style="color:#74B602;">跳过这种多层级联模式, 没有召回粗排环节, 直接"一步到位"的进行内容推荐</font>**<font style="color:rgb(0, 0, 0);">。</font>

<font style="color:rgb(0, 0, 0);">近两年业界有不少公司落地了一些"生成式召回"的方案, 但这些方案本质上还是在现有多层级联范式下, 只是作为一路召回使用。快手这篇文章提出了一种End-to-End的生成式推荐方案OneRec, 是业界首次在工业界落地的生成式推荐方案。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(0, 0, 0);">作者所提OneRec方法的主要思路是首先对</font>**<font style="color:#ED740C;">Item的多模态表征使用残差量化方式进行tokenize</font>**<font style="color:rgb(0, 0, 0);">, 再基于Transformer的Encoder&Decoder方式进行训练, 同时还使用DPO进一步增强模型的偏好对齐能力, 下面详细介绍。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>

**paper：**[**https://arxiv.org/pdf/2502.18965**](https://arxiv.org/pdf/2502.18965)

**参考：**[**快手OneRec:无召回"一步到位"的生成式推荐方案**](https://mp.weixin.qq.com/s/MGiYBcuAGDTCldfDqVWjiA)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590718353-d7dd2726-29f8-46d6-a2f8-98a61376033d.png)

:::color5
**<font style="color:#601BDE;">1.</font>****<font style="color:#601BDE;">残差量化</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">记用户的行为序列为, 其中为序列长度, 而视频使用快手之前提出的QARM里经过推荐场景数据做Item对齐后的多模态表征来表示。这里Item对齐的思路主要是构造生成高质量的Item2Item的Pair对, 再通过对比学习来对齐。</font>

<font style="color:rgb(0, 0, 0);">快手推荐内容池数以亿计, 论文对视频的</font>**<font style="color:#74B602;">多模态表征使用残差量化的方式进行tokenize处理</font>**<font style="color:rgb(0, 0, 0);">。残差量化是RQ-VAE提出的方法, 推荐现在也是开始广泛应用起来了, 包括谷歌的Tiger以及前面提到的快手QARM。</font>

<font style="color:rgb(0, 0, 0);">这里简单介绍下残差量化方法。</font>**<font style="color:#74B602;">残差量化方法会有多层级的codebook</font>**<font style="color:rgb(0, 0, 0);">, 这些codebook的模整体上是</font>**<font style="color:#74B602;">逐层递减</font>**<font style="color:rgb(0, 0, 0);">的。以下面3层的codebook为例, 对于每个待量化的向量, 首先从第1个codebook中找到距离最近的向量, 得到其下标作为语义ID, 再计算原向量与最近邻向量的残差作为新的向量, 再从第2个codebook开始逐层进行得到各层的语义ID, </font>**<font style="color:#74B602;">将各层的语义ID拼接起来就是残差量化的语义ID了</font>**<font style="color:rgb(0, 0, 0);">。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743583126690-35d214e0-c8ec-4610-828b-c2ee01d66a2d.png)

<font style="color:rgb(0, 0, 0);">这些</font>**<font style="color:#74B602;">codebook通常是使用k-means的聚类算法得到的</font>**<font style="color:rgb(0, 0, 0);">, 将个聚类中心作为codebook的个向量。这里可能会遇到的一个问题是, 个簇大小不一, 甚至差距会非常大。为了构建一个相对平衡的codebook, 论文这里使用了下面</font>**<font style="color:rgb(0, 0, 0);">算法1</font>**<font style="color:rgb(0, 0, 0);">的方式来构造, 其思路用一句话概述就是, 强制让-means聚类的个簇大小完全一样, 这里不做赘述。</font>**<font style="color:#601BDE;"> </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591446067-c4429197-fdec-468e-945b-42e5b8fc84d9.png)

:::color5
**<font style="color:#601BDE;">2.</font>****<font style="color:#601BDE;">session-wise的list生成方式 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">不同于通常的point-wise的next item prediction方式, 作者所提OneRec方法考虑的是</font>**<font style="color:#74B602;">session-wise的list生成方式</font>**<font style="color:rgb(0, 0, 0);">, 其整体框架如下图所示:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590742993-699129ac-52eb-4f83-9b2c-6db63b38d5e5.png)

1. **<font style="color:rgb(0, 0, 0);">session会话数据筛选</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">这里的session被定义为一次服务请求下发的"一刷"(比如5个或10个视频)</font><font style="color:rgb(0, 0, 0);">。为了筛选出高质量的会话数据, 作者还制定了一些标准来筛选:</font>

+ <font style="color:rgb(1, 1, 1);">用户在会话中实际观看的短视频数量</font><font style="color:rgb(1, 1, 1);">5</font>
+ <font style="color:rgb(1, 1, 1);">用户观看会话的总时长超过一定阈值</font>
+ <font style="color:rgb(1, 1, 1);">用户有过交互, 如点赞、收藏或分享等</font>
2. **<font style="color:rgb(0, 0, 0);">Encoder&Decoder架构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">作者使用类似T5的Encoder&Decoder架构。其中, </font>**<font style="color:#74B602;">Encoder以长度为的用户行为序列的多模态语义ID为输入, Decoder以长度为的Session语义ID为输出</font>**<font style="color:rgb(0, 0, 0);">, 即:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743583347819-58ebecab-108a-47d9-8a29-ad43b7ec04b5.png)

<font style="color:rgb(0, 0, 0);">其中, 这里的</font><font style="color:rgb(0, 0, 0);">表示前面残差量化的多模态语义ID, 同时, 在训练时, Encoder部分增加特殊token <SEP>, Decoder部分也增加特殊token <BOS>, 这样, Decoder这里的输入就是:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743583354674-a660e912-ec87-4c0d-b10e-dbbd56870815.png)

<font style="color:rgb(0, 0, 0);">在快手短视频推荐这里, OneRec建模的用户行为序列长度=256, 看起来没有考虑长序列, 建模的Session长度为=5。</font>

:::color5
**<font style="color:#601BDE;">3.稀疏激活MoE</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">为了在有限的资源约束下提高参数规模, Decoder部分也借鉴LLM常用的混合专家模型的稀疏激活方式进行训练, 将FFN替换成MoE模块, 对于每个输入, 使用门控机制从个Experts中选择top-的Experts激活:</font><font style="color:rgb(51, 51, 51);">  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590472827-a1156e18-b928-4567-b6ec-a0602b7b667a.png)

<font style="color:rgb(0, 0, 0);">在快手短视频推荐场景里, 作者使用N</font><sub><font style="color:rgb(0, 0, 0);">MoE</font></sub><font style="color:rgb(0, 0, 0);">=24, 激活Expert的数量为N</font><sub><font style="color:rgb(0, 0, 0);">MoE</font></sub><font style="color:rgb(0, 0, 0);">=2</font>

:::color5
**<font style="color:#601BDE;">4.Next Token Predict</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">作者对Session列表的语义ID进行next token prediction, 并使用交叉熵计算损失:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590485127-b7dd9cd0-d67f-4cc4-adb3-ec12ea10565a.png)

<font style="color:rgb(0, 0, 0);">这样, 经过充分sesstion列表数据训练后的模型, 记为种子模型M。</font>

:::color5
**<font style="color:#601BDE;">5.DPO:偏好对齐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">前面基于Session的列表生成只负责自回归的Next Token Prediction, 并没有引入用户对Session列表推荐结果的正负反馈信号, 因此, 还需要施加一个基于用户偏好的Loss去对齐用户偏好。</font>

1. **训练奖励模型**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">奖励模型</font>_<font style="color:rgb(0, 0, 0);">R(u,S)</font>_<font style="color:rgb(0, 0, 0);">用于评估输出不同用户(通常使用对应的用户行为序列来表示)对Session列表</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590515328-00cb7b05-1591-4f2b-9035-70a37ec47d62.png)<font style="color:rgb(0, 0, 0);">的偏好程度.</font>

<font style="color:rgb(0, 0, 0);">为了让奖励模型</font>_<font style="color:rgb(0, 0, 0);">R</font>_<font style="color:rgb(0, 0, 0);">具备对Session列表进行排序的能力, 作者首先对Session的每个Item都作了target attention:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590533307-1ad6d81e-ed94-4dfb-86da-929247709436.png)

<font style="color:rgb(0, 0, 0);">再将Session内这个target-aware表征拼接起来, 作为Session的target-aware表征:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590547394-d8b5145a-4ae8-4caf-a344-51efea0a4a68.png)

<font style="color:rgb(0, 0, 0);">然后, 对session内的</font><font style="color:rgb(0, 0, 0);">个Item增加self-attention:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590636683-ce067867-2d5f-4eec-9a63-c26125ae3fa8.png)

<font style="color:rgb(0, 0, 0);">对于不同的目标, 作者使用不同的Tower进行多目标预测:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590643858-ae34feea-148f-44e2-95a4-29979c305c89.png)

<font style="color:rgb(0, 0, 0);">再使用交叉熵计算对应目标的Loss:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590653071-d0d6ee9f-7073-4c92-a85f-cfb9a4a09328.png)

2. **<font style="color:rgb(0, 0, 0);">迭代偏好对齐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">基于DPO的迭代偏好对齐的训练流程如下图所示:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590977098-6821f716-a6f6-41cb-9971-ba8e8acbaeaa.png)

<font style="color:rgb(0, 0, 0);">首先, 基于前面预训练的奖励模型R(u, S)以及当前的OneRec模型, 使用beam search生成N个结果, 记作:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743590998859-f20707b8-86f9-417b-8fd3-ce3221487bc4.png)

<font style="color:rgb(0, 0, 0);">并记奖励模型预测对应的reward为:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591013992-2eb150d1-d7b9-4231-83dd-aa09b0a59603.png)

<font style="color:rgb(0, 0, 0);">然后, 基于reward筛选出分数最高的session列表S</font><sub><font style="color:rgb(0, 0, 0);">u</font></sub><sup><font style="color:rgb(0, 0, 0);">w</font></sup><font style="color:rgb(0, 0, 0);">和分数最低的session列表S</font><sub><font style="color:rgb(0, 0, 0);">u</font></sub><sup><font style="color:rgb(0, 0, 0);">l</font></sup><font style="color:rgb(0, 0, 0);">组成数据集</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591084576-6dfe4d65-5bb7-4856-b5ce-dc184bdf7df1.png)<font style="color:rgb(0, 0, 0);">, 用于迭代训练+1步的模型M</font><sub><font style="color:rgb(0, 0, 0);">t+1</font></sub><font style="color:rgb(0, 0, 0);">, 训练使用DPO Loss:</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591026029-faa5f686-9814-4004-beb1-4c7d06c876db.png)

<font style="color:rgb(0, 0, 0);">为了减轻beam search推理过程中的计算负担, 作者仅随机抽取r</font><sub><font style="color:rgb(0, 0, 0);">DPO</font></sub><font style="color:rgb(0, 0, 0);"> = 1%的数据进行偏好对齐, 即在迭代训练过程中, 仅1%的样本Loss为</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591154799-4962f5a8-9e84-4015-913c-2b04e1eff7bc.png)<font style="color:rgb(0, 0, 0);">, 其余样本的Loss为</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591159930-151d2260-144c-4b11-bff9-2e654d148a55.png)<font style="color:rgb(0, 0, 0);">。</font>

:::color5
**<font style="color:#601BDE;">6.线上部署</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">下图描述了OneRec线上部署的整体框架, 其中:</font>

+ <font style="color:rgb(1, 1, 1);">beam search的beam size为128, 以平衡模型效果及耗时</font>
+ <font style="color:rgb(1, 1, 1);">由于采用MoE结构, 线上推理过程中仅13%的参数被激活</font>
+ <font style="color:rgb(1, 1, 1);">增加了一些KV缓存和混合精度计算等优化手段</font><font style="color:rgb(0, 0, 0);">  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591188220-d6f65120-6dbc-47a2-8ebf-9b0f8ed32447.png)

:::color5
**<font style="color:#601BDE;">7.效果评测</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(0, 0, 0);">主要结论</font>**
    - <font style="color:rgb(1, 1, 1);">会话生成方法明显优于传统基于点积的方法和Tiger等point-wise生成方法</font>
    - <font style="color:rgb(1, 1, 1);">小比例的DPO训练就能带来不错的收益</font>
    - <font style="color:rgb(1, 1, 1);">所提出IPA策略优于现有的各种DPO变体</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591224495-dd02ae29-1b59-4d97-adf7-645cbdcc06c0.png)

+ **<font style="color:rgb(34, 34, 34);">语义ID预测概率的可视化</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">OneRec+IPA比OneRec基线方法表现出预测分布的显著置信度偏移, 说明提出的偏好对齐策略有效地鼓励基础模型产生更置信的偏好生成模式。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591254770-8ba71c6c-1ee8-4c60-85fe-1cd56c337e86.png)

+ **<font style="color:rgb(0, 0, 0);">AB实验</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(0, 0, 0);">总观看时长提升1.68%，平均观看时长提升6.56%, 所以是渗透掉了吗?</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743591297534-8dbe91b7-63b8-4be3-be3e-9e40e29fa33c.png)



# 生成式排序
## 小红书 GenRank
:::success
**<font style="color:#000000;">背景</font>**<font style="color:#000000;">：在当今的信息爆炸时代，推荐系统已成为社交媒体平台的核心组件，帮助用户在海量信息中发现个性化的内容。小红书的“发现页”作为一款服务于数亿用户的产品，</font>**<font style="color:#74B602;">面临着如何在保持高效率的同时提升推荐效果的挑战</font>**<font style="color:#000000;">。本文将深入探讨生成式排序系统在大规模工业场景中的应用，并介绍GenRank架构如何在这一领域取得突破。</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>**

:::

:::color3
**简介：TLDR:** 生成式推荐作为一种新兴范式，在信息检索领域展现出巨大潜力。然而，生成式排序系统在大规模工业环境中的有效性和可行性仍待深入研究。本文通过在小红书的“发现页”推荐系统中进行实验，提出了GenRank架构，显著提升了用户满意度，同时保持了与现有生产系统相当的计算资源消耗。**<font style="color:#D22D8D;">(by草莓师姐)</font>**

**paper：**[**https://arxiv.org/pdf/2505.04180**](https://arxiv.org/pdf/2505.04180)

**参考：**[**https://mp.weixin.qq.com/s/2d0lbyXN_KEPfCcQnjRHQg**](https://mp.weixin.qq.com/s/2d0lbyXN_KEPfCcQnjRHQg)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748485477827-6e7d8446-468d-4d91-8462-f07ddd4989d2.png)

> GenRank的模型架构。与采用item-oriented结构的现有方法相比，例如HSTU，我们的解决方案采用了action-oriented结构。
>

:::color5
**<font style="color:#601BDE;">1.生成式排序的挑战与机遇 </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748485203586-63edc377-6f6e-437b-9e8b-5ba30cee4f2d.png)

> 左：小红树的Explore Feed产品截图。右图：工业推荐系统的级联流程图，其中每个阶段都需要处理大量item。
>

推荐系统通常采用级联管道架构，包括检索、预排序、排序和策略四个阶段。在排序阶段，系统需要对每个候选item进行精确预测。**<font style="color:#117CEE;">传统的排序方法主要依赖于多层感知机和嵌入范式</font>**，**<font style="color:#74B602;">而生成式推荐则将推荐问题转化为序列生成任务，直接从用户历史行为中预测目标行为。</font>**

尽管生成式推荐在理论上具有优势，**<font style="color:#117CEE;">但在大规模工业环境中，其有效性和可行性仍面临诸多挑战</font>**。一方面，生成式架构需要处理海量数据，对计算资源和存储资源提出了极高的要求；另一方面，如何在保持性能的同时优化计算效率，是生成式排序系统亟待解决的问题。

:::color5
**<font style="color:#601BDE;">2.问题设置 </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

:::

本文研究的是生成式推荐在排序阶段的应用。在这个阶段，推荐系统需要对一组预定义的任务进行预测，例如**<font style="color:#74B602;">预测用户点击某个候选item的概率，或者用户在看到候选item时预期停留的时间</font>**。为了构建用于离线实验的数据集，从小红书的“发现页”收集了15天内数百亿条item曝光日志。输入特征包括以下三种类型：

+ **分类特征**：用户ID、itemID、用户历史行为、标签等。
+ **数值特征**：用户年龄、item发布时间、作者粉丝数等。
+ **冻结嵌入**：多模态item嵌入、基于图的作者嵌入等。

数值特征通过预定义的边界进行离散化，分类特征则通过嵌入表转换为稠密嵌入。由预训练模型提供的冻结嵌入作为辅助信息，为相关特征提供先验知识。使用ROC曲线下面积（AUC）作为离线评估指标。值得注意的是，在本文的设置中，AUC的绝对增加0.0010被认为是显著的，因为它通常会在在线环境中为数亿用户带来0.5%的指标提升。

:::color5
**<font style="color:#601BDE;">3.生成式范式的关键机制 </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

:::

生成式推荐与传统范式的主要区别在于其独特的序列交互方式和训练样本的组织方式。**<font style="color:#74B602;">生成式排序采用自回归的方式进行序列交互，即模型在预测下一个动作时，只依赖于之前的历史行为和候选item</font>**。这种自回归方式在生成式排序中至关重要，因为它能够保留模型在预训练阶段学到的能力，即使在没有预训练的情况下也能保持有效性。

此外，生成式排序将用户在一段时间内的行为分组为一个训练样本，而不是像传统方法那样将每个行为日志作为一个独立的样本。这种组织方式有助于提高梯度估计的稳定性，并减少信息泄露的风险。然而，实验结果表明，生成式推荐的有效性主要来源于其架构，而不是训练样本的组织方式。

<font style="color:rgb(25, 27, 31);">生成式精排在工业级大规模场景下的有效性仍未得到充分探索，从两个维度展开实验分析：</font>

1. **<font style="color:#117CEE;">范式差异的机制分析</font>****<font style="color:#601BDE;"> </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

<font style="color:rgb(25, 27, 31);">与传统范式通过历史行为学习复杂特征交互不同，生成式推荐将精排重构为序列转导任务，如图1所示。这种模式下，生成式精排在</font>**<font style="color:rgb(25, 27, 31);">序列交互方式</font>**<font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">训练样本组织</font>**<font style="color:rgb(25, 27, 31);">两个维度存在显著差异。</font>

**<font style="color:#117CEE;">（1）序列交互方式：自回归特性</font>**<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">	HSTU仅在候选物品对应位置计算损失，如图1右边网络所示，可视为以用户信息和候选物品为输入提示的监督微调。大语言模型在监督微调阶段采用自回归</font>方式，是为了保持预训练获得的能力。但生成式推荐并无预训练阶段，那自回归是否真的必要？

<font style="color:rgb(25, 27, 31);">通过两组实验验证：</font>

+ <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">历史行为位置计算损失：</font>**<font style="color:rgb(25, 27, 31);">即使仅包含少量历史位置，AUC仍下降超1%。这与"单周期问题"相关，模型会从稀疏特征中学习错误模式</font>
+ **<font style="color:rgb(25, 27, 31);">全可见注意力掩码替换：</font>**<font style="color:rgb(25, 27, 31);">类似T5模型的做法，在历史位置采用完全可见的注意力掩码以最大化特征交互，该改动导致AUC降低超0.15%，且模型规模越大下降越显著。</font>

<font style="color:rgb(25, 27, 31);">实验证明自回归机制对生成式精排效果具有决定性作用。  
</font>**<font style="color:#117CEE;">（2）训练样本组织：时序分组策略</font>**

<font style="color:rgb(25, 27, 31);">传统范式通常采用逐点组织（每个训练样本对应一条曝光日志），而生成式推荐将用户时序相邻的行为合并为单个训练样本。论文提出两个潜在优势假设：</font>

+ **<font style="color:rgb(25, 27, 31);">梯度稳定性</font>**<font style="color:rgb(25, 27, 31);">：同一请求的曝光日志特征（特别是用户特征）高度重叠，批次处理可提升梯度估计稳定性</font>
+ **<font style="color:rgb(25, 27, 31);">信息泄漏规避</font>**<font style="color:rgb(25, 27, 31);">：分布式训练中样本处理顺序可能违背真实时序，导致模型在训练观察曝光日志前就通过历史行为推测用户偏好</font>

<font style="color:rgb(25, 27, 31);">但实证结果并未充分支持这两个假设：当改用逐点顺序处理分组样本时，AUC仅轻微下降。</font>**<font style="color:#74B602;">这表明生成式推荐的有效性主要源于架构设计，而非样本组织方式</font>**

2. **<font style="color:#117CEE;">模块兼容性验证</font>****<font style="color:#601BDE;"> </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

<font style="color:rgb(25, 27, 31);">为比较两种范式下模块的影响差异，通过实验测量了各模块带来的性能增益。重点选取了工业级精排系统常用的四个核心模块：用于序列建模的</font>[<font style="color:rgb(9, 64, 142);">SIM</font>](https://zhida.zhihu.com/search?content_id=258160031&content_type=Article&match_order=1&q=SIM&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、个性化表征学习的</font>[<font style="color:rgb(9, 64, 142);">PPNet</font>](https://zhida.zhihu.com/search?content_id=258160031&content_type=Article&match_order=1&q=PPNet&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、提供先验知识的内容嵌入以及多任务学习的</font>[<font style="color:rgb(9, 64, 142);">PLE</font>](https://zhida.zhihu.com/search?content_id=258160031&content_type=Article&match_order=1&q=PLE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">实验结果表明：</font>

+ <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">兼容性模块</font>**<font style="color:rgb(25, 27, 31);">：SIM、PPNet和PLE在两种范式下取得的提升幅度相当，说明生成式范式与这些模块具有良好兼容性</font>
+ **<font style="color:rgb(25, 27, 31);">增效模块</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">内容嵌入在生成式范式下带来的AUC提升达到传统范式的两倍以上</font>**<font style="color:rgb(25, 27, 31);">。这是由于内容嵌入的生成式训练方式与其在下游任务中的应用保持了架构一致性。</font>

<font style="color:rgb(25, 27, 31);">特征工程的影响研究揭示了更深层的发现：</font>

+ <font style="color:rgb(25, 27, 31);">虽然HSTU主张生成式推荐器能充分表达统计模式而可移除人工特征，但实验显示：</font>
    - <font style="color:rgb(25, 27, 31);">多数特征对生成式架构收益甚微</font>
    - <font style="color:rgb(25, 27, 31);">特定实时统计特征（尤其是基于时间窗口的特征）仍能显著提升性能，因其为模型提供了直接信号</font>
+ <font style="color:rgb(25, 27, 31);">计算效率优势：	</font>
    - <font style="color:rgb(25, 27, 31);">传统特征工程的高计算开销限制了精排模型实时处理大规模候选集的能力</font>
    - <font style="color:rgb(25, 27, 31);">生成式架构通过最小化特征需求提升推理扩展性</font>
    - [<font style="color:rgb(9, 64, 142);">KV缓存机制</font>](https://zhida.zhihu.com/search?content_id=258160031&content_type=Article&match_order=1&q=KV%E7%BC%93%E5%AD%98%E6%9C%BA%E5%88%B6&zhida_source=entity)<font style="color:rgb(25, 27, 31);">使生成式架构能更高效地应对候选集规模增长</font>

<font style="color:rgb(25, 27, 31);">随着计算开销的持续降低，生成式架构有望在未来系统中实现精排与粗排阶段的统一。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法 </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

:::

为了解决上述问题，提出了GenRank架构。GenRank的核心创新在于**<font style="color:#74B602;">将item视为位置信息，专注于迭代预测用户行为，从而显著提高了系统的效率。</font>**<font style="color:rgb(25, 27, 31);">GenRank，通过</font>**<font style="color:rgb(25, 27, 31);">物品-动作重组机制</font>**<font style="color:rgb(25, 27, 31);">和</font>[**<font style="color:rgb(9, 64, 142);">时空偏置优化</font>**](https://zhida.zhihu.com/search?content_id=258160031&content_type=Article&match_order=1&q=%E6%97%B6%E7%A9%BA%E5%81%8F%E7%BD%AE%E4%BC%98%E5%8C%96&zhida_source=entity)<font style="color:rgb(25, 27, 31);">两大创新，实现大规模精排任务的高效训练与推理。如表1所示，相比基线方法HSTU，采用动作导向重组使训练速度提升78.7%，时空偏置优化进一步带来25.0%加速，最终实现94.8%的总训练加速，同时测试集AUC指标略有提升。</font>

具体来说，GenRank采用了以下关键技术：

1. **<font style="color:#117CEE;">行为导向的序列组织</font>****<font style="color:#601BDE;"> </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748485477827-6e7d8446-468d-4d91-8462-f07ddd4989d2.png)

> GenRank模型架构，与HSTU采用面向项目（Item）的组织不同，其采用面向行动（Action）的组织。
>

传统的序列推荐方法将item作为基本单位，而GenRank则将动作作为序列生成的基本单位，item则作为上下文信号引导生成过程。这种设计将注意力机制的输入序列长度减少了一半，大幅降低了计算成本。

<font style="color:rgb(25, 27, 31);">传统序列推荐方法通常以物品为基本单元构建模型，这种架构被称为</font>**<font style="color:rgb(25, 27, 31);">物品导向范式</font>**<font style="color:rgb(25, 27, 31);">。为适配精排任务的动作感知需求，HSTU将动作令牌作为序列中的附加模态（图2a），使模型能根据上下文预测物品或动作。虽然这种设计支持检索与精排的统一框架，但序列长度翻倍导致显著计算开销。</font>

<font style="color:rgb(25, 27, 31);">GenRank提出</font>**<font style="color:rgb(25, 27, 31);">动作导向范式</font>**<font style="color:rgb(25, 27, 31);">的创新思路，将物品视为位置信息，专注于迭代预测与物品关联的动作（如图2（b）所示），注意力机制输入序列长度减半，注意力计算成本降低75%，线性投影成本减少50%。</font>

<font style="color:rgb(25, 27, 31);">技术实现如上图所示，每个位置的令牌嵌入由物品嵌入与动作嵌入相加构成 ei=ϕ(xi)+ψ(ai)</font>_<font style="color:rgb(25, 27, 31);">ei</font>_<font style="color:rgb(25, 27, 31);">=</font>_<font style="color:rgb(25, 27, 31);">ϕ</font>_<font style="color:rgb(25, 27, 31);">(</font>_<font style="color:rgb(25, 27, 31);">xi</font>_<font style="color:rgb(25, 27, 31);">)+</font>_<font style="color:rgb(25, 27, 31);">ψ</font>_<font style="color:rgb(25, 27, 31);">(</font>_<font style="color:rgb(25, 27, 31);">ai</font>_<font style="color:rgb(25, 27, 31);">)，采用掩码动作嵌入 ej=ϕ(xj)+M</font>_<font style="color:rgb(25, 27, 31);">ej</font>_<font style="color:rgb(25, 27, 31);">=</font>_<font style="color:rgb(25, 27, 31);">ϕ</font>_<font style="color:rgb(25, 27, 31);">(</font>_<font style="color:rgb(25, 27, 31);">xj</font>_<font style="color:rgb(25, 27, 31);">)+</font>_<font style="color:rgb(25, 27, 31);">M</font>_<font style="color:rgb(25, 27, 31);">，并通过候选掩码防止信息泄漏。</font>

2. **<font style="color:#117CEE;">位置与时间偏差</font>****<font style="color:#601BDE;"> </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748485819257-9f2fe7f7-07a8-44c3-b2a4-d3785877e15b.png)

> 输入表示和候选掩码。(a) GenRank的输入表示包含五种嵌入。(b)候选掩码：用一个历史行为和两个候选项来描述用户序列的掩码结构。
>

为了进一步优化计算效率，GenRank引入了新的位置和时间嵌入设计。这些嵌入只需要线性I/O操作，显著减少了系统开销。此外，GenRank采用了无参数的ALiBi偏差作为注意力机制中的相对位置和时间偏差，进一步降低了计算成本。<font style="color:rgb(25, 27, 31);">HSTU采用可学习的相对注意力偏置编码时空信息，虽能提升性能，但随序列长度呈平方级增长的I/O操作成为计算瓶颈。GenRank提出仅需线性I/O的高效设计方案。</font>

**<font style="color:rgb(25, 27, 31);">a.三重嵌入体系</font>**<font style="color:rgb(25, 27, 31);">：</font>

+ **<font style="color:rgb(25, 27, 31);">位置嵌入</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">：记录物品在用户序列中的索引，同请求候选物品共享位置</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748486771835-805bde71-2a2c-42a1-aa16-c1dbe2ba6361.png)

+ **<font style="color:rgb(25, 27, 31);">请求索引嵌入</font>**<font style="color:rgb(25, 27, 31);">：标记同请求物品的分组关系</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748486801855-878787ec-8380-4cf5-add7-0e2e193791c1.png)

+ **<font style="color:rgb(25, 27, 31);">请求间隔时间嵌入</font>**<font style="color:rgb(25, 27, 31);">：量化用户活跃程度</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748486792114-97e6e498-9ee0-49e4-b463-93b6a3aefa13.png)

**<font style="color:rgb(25, 27, 31);">b.ALiBi增强设计</font>**<font style="color:rgb(25, 27, 31);">：</font>

+ <font style="color:rgb(25, 27, 31);">引入无参数的相对位置-时间偏置，对远距离查询-键对施加递增惩罚</font>
+ <font style="color:rgb(25, 27, 31);">与Flash Attention融合后仅增加极小计算开销，避免O(N²)内存访问</font>

<font style="color:rgb(25, 27, 31);">最终输入表征如公式(1)所示，通过时空信息的高效融合，在保持建模能力的同时显著降低系统负载。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1748486697822-164dde02-a50f-4038-8082-114156f0e17e.png)

:::color5
**<font style="color:#601BDE;">5.实验验证与效果 </font>****<font style="color:#D22D8D;">(by草莓师姐)</font>**

:::

1. **<font style="color:#117CEE;">离线指标</font>**
+ <font style="color:rgb(25, 27, 31);">主任务AUC与GAUC[29,3]提升均超0.0020</font>
+ <font style="color:rgb(25, 27, 31);">其他任务提升区间0.0005~0.0015</font>
2. **<font style="color:#117CEE;">线上核心指标</font>**

| **<font style="color:rgb(25, 27, 31);">指标</font>** | **<font style="color:rgb(25, 27, 31);">停留时长</font>** | **<font style="color:rgb(25, 27, 31);">阅读量</font>** | **<font style="color:rgb(25, 27, 31);">互动量</font>** | **<font style="color:rgb(25, 27, 31);">7日留存率(LT7)</font>** |
| :--- | :--- | :--- | :--- | :--- |
| <font style="color:rgb(25, 27, 31);">提升幅度</font> | <font style="color:rgb(25, 27, 31);">+0.3345%</font> | <font style="color:rgb(25, 27, 31);">+0.6325%</font> | <font style="color:rgb(25, 27, 31);">+1.2474%</font> | <font style="color:rgb(25, 27, 31);">+0.1481%</font> |


3. **<font style="color:#117CEE;">关键发现</font>**
+ <font style="color:rgb(25, 27, 31);">冷启动物品提升尤为显著，源于GenRank对内容嵌入中世界知识的增强利用能力</font>
+ <font style="color:rgb(25, 27, 31);">资源开销与生产模型相当：</font>
    - <font style="color:rgb(25, 27, 31);">训练成本较高，但推理与存储成本更低</font>
    - <font style="color:rgb(25, 27, 31);">P99响应时间优化25%+，展现显著的实时扩展潜力</font>

通过在线A/B实验验证了GenRank的有效性和可行性。实验结果表明，GenRank在用户满意度方面取得了显著提升，同时在计算资源消耗上与现有生产系统相当。具体来说，GenRank在冷启动项目上的表现尤为突出，这得益于其对内容嵌入的增强利用。

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1748485996754-4cb096ac-a751-422e-8212-a2c7f1c0bac6.webp)

> 发现页场景下的在线A/B测试结果
>

下表总结了在训练性能方面的结果。使用HSTU作为基线方法。利用行动为导向的组织速度提高了78.7%，而采用提出的位置和时间偏差方法速度提高了25.0%。总的来说，GenRank在训练过程中实现了总加速比94.8%，在测试集上的AUC略有提高。

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1748485996756-0d296f7f-b3bc-49b6-b68b-f8bafef5324a.webp)

GenRank的提出为生成式排序系统在大规模工业环境中的应用提供了新的思路。通过创新的架构设计和高效的计算策略，GenRank不仅提升了推荐效果，还为未来推荐系统的发展提供了宝贵的实践经验。

# <font style="color:rgb(51, 51, 51);">召回 + </font><font style="color:rgb(51, 51, 51);">LLM精排</font><font style="color:rgb(51, 51, 51);"></font>
<font style="color:rgb(51, 51, 51);">以LLAMA在电商商品推荐为例</font>

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">大型语言模型（LLM）如LLAMA在推荐系统中的核心应用逻辑是通过对</font>**<font style="color:#ED740C;">用户行为、商品属性和上下文信息的语义理解</font>**<font style="color:rgb(51, 51, 51);">，生成个性化推荐。其核心优势在于：</font>

1. **<font style="color:rgb(51, 51, 51);">语义理解</font>**<font style="color:rgb(51, 51, 51);">：解析用户历史行为（如点击、购买）和商品描述的深层语义。</font>
2. **<font style="color:rgb(51, 51, 51);">上下文建模</font>**<font style="color:rgb(51, 51, 51);">：结合用户会话中的短期兴趣（如最近浏览）和长期偏好。</font>
3. **<font style="color:rgb(51, 51, 51);">生成能力</font>**<font style="color:rgb(51, 51, 51);">：直接生成推荐结果或预测用户兴趣标签。</font>

:::

<font style="color:rgb(51, 51, 51);">以电商推荐为例，LLAMA的输入可能包括：</font>

+ <font style="color:rgb(51, 51, 51);">用户历史行为序列（如</font>`<font style="color:rgb(51, 51, 51);">购买A, 浏览B, 收藏C</font>`<font style="color:rgb(51, 51, 51);">）</font>
+ <font style="color:rgb(51, 51, 51);">商品元数据（标题、类目、描述）</font>
+ <font style="color:rgb(51, 51, 51);">上下文特征（时间、设备、场景）</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">以下为基于LLAMA的推荐系统典型流程：</font>

**<font style="color:rgb(51, 51, 51);">1. 数据预处理</font>**

+ **<font style="color:rgb(51, 51, 51);">用户行为序列</font>**<font style="color:rgb(51, 51, 51);">：将用户行为编码为时间序列，如</font>`<font style="color:rgb(51, 51, 51);">[item_id_1, item_id_2, ...]</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">商品文本特征提取</font>**<font style="color:rgb(51, 51, 51);">：将商品标题、描述等文本通过LLM编码为向量（如768维）。</font>
+ **<font style="color:rgb(51, 51, 51);">用户画像构建</font>**<font style="color:rgb(51, 51, 51);">：聚合历史行为，生成用户兴趣向量。</font>

**<font style="color:rgb(51, 51, 51);">2. 输入构造</font>**

<font style="color:rgb(51, 51, 51);">将用户和商品信息转换为自然语言提示（Prompt），例如：</font>

```plain
text

用户最近购买了"无线蓝牙耳机"，浏览了"运动水壶"，过去常购买电子产品。
根据用户历史行为，推荐5个相关商品：
```

**<font style="color:rgb(51, 51, 51);">3. 推荐生成</font>**

+ **<font style="color:rgb(51, 51, 51);">召回阶段</font>**<font style="color:rgb(51, 51, 51);">（可选）：用LLM生成候选商品ID或关键词，结合传统召回（如协同过滤）。</font>
+ **<font style="color:rgb(51, 51, 51);">精排阶段</font>**<font style="color:rgb(51, 51, 51);">：LLMA直接生成推荐结果或预测CTR（点击率）。</font>

**<font style="color:rgb(51, 51, 51);">4. 输出解析</font>**

+ <font style="color:rgb(51, 51, 51);">解析LLM生成的文本，提取商品ID或名称。</font>
+ <font style="color:rgb(51, 51, 51);">结合商品库检索实际商品信息。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 强语义理解（如"健身器材"与"蛋白粉"的关联）</font> | <font style="color:rgb(51, 51, 51);">1. 推理延迟高（生成式模型耗时）</font> |
| <font style="color:rgb(51, 51, 51);">2. 处理长尾商品和冷启动问题</font> | <font style="color:rgb(51, 51, 51);">2. 可能生成不存在的商品（幻觉问题）</font> |
| <font style="color:rgb(51, 51, 51);">3. 支持多模态输入（文本+图像特征）</font> | <font style="color:rgb(51, 51, 51);">3. 依赖高质量商品描述数据</font> |
| <font style="color:rgb(51, 51, 51);">4. 可解释性强（生成推荐理由）</font> | <font style="color:rgb(51, 51, 51);">4. 难以实时更新用户行为</font> |


:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">个性化首页推荐</font>**<font style="color:rgb(51, 51, 51);">：根据用户长期兴趣生成商品列表。</font>
2. **<font style="color:rgb(51, 51, 51);">搜索增强</font>**<font style="color:rgb(51, 51, 51);">：理解模糊查询（如"适合夏天的轻薄外套"）。</font>
3. **<font style="color:rgb(51, 51, 51);">搭配推荐</font>**<font style="color:rgb(51, 51, 51);">：基于已选商品生成互补品（如"手机+保护壳"）。</font>
4. **<font style="color:rgb(51, 51, 51);">冷启动用户</font>**<font style="color:rgb(51, 51, 51);">：通过人口统计信息和初始行为生成推荐。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">降低延迟</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">模型蒸馏</font>**<font style="color:rgb(51, 51, 51);">：训练轻量级模型（如TinyLLAMA）。</font>
    - **<font style="color:rgb(51, 51, 51);">缓存机制</font>**<font style="color:rgb(51, 51, 51);">：缓存高频用户推荐结果。</font>
2. **<font style="color:rgb(51, 51, 51);">增强实时性</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">将实时行为通过向量编码注入Prompt。</font>
    - <font style="color:rgb(51, 51, 51);">结合传统模型（如RNN）处理实时序列。</font>
3. **<font style="color:rgb(51, 51, 51);">减少幻觉</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">约束生成空间（仅输出候选商品ID）。</font>
    - <font style="color:rgb(51, 51, 51);">后处理过滤不存在商品。</font>
4. **<font style="color:rgb(51, 51, 51);">领域知识注入</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">在预训练阶段融入电商知识图谱。</font>
    - <font style="color:rgb(51, 51, 51);">微调时加入商品属性预测任务。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch

# 加载模型和分词器
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

def generate_recommendation(user_history):
    # 构造Prompt
    prompt = f"""
    用户行为序列：[购买无线蓝牙耳机, 浏览运动水壶, 搜索健身手环]
    商品库：无线耳机、运动水壶、蛋白粉、瑜伽垫、智能手表
    生成推荐（最多3个）：
    """
    
    # 编码输入
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # 生成结果
    outputs = model.generate(
        inputs.input_ids,
        max_length=200,
        temperature=0.7,
        num_return_sequences=1
    )
    
    # 解析输出
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("推荐：")[-1].strip()

# 示例输出
print(generate_recommendation())
# 可能输出：1. 智能手表 2. 蛋白粉 3. 瑜伽垫

```





# <font style="color:rgb(51, 51, 51);">LLM如何处理用户行为序列</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">LLM（如LLAMA）处理用户行为序列的核心是</font>**<font style="color:rgb(51, 51, 51);">将用户历史行为建模为序列数据</font>**<font style="color:rgb(51, 51, 51);">，利用Transformer架构的自注意力机制捕捉行为间的复杂依赖关系。具体原理如下：</font>

+ **<font style="color:rgb(51, 51, 51);">序列建模</font>**<font style="color:rgb(51, 51, 51);">：用户行为（点击、加购、购买等）按时间顺序构成序列，LLM通过位置编码（如LLAMA的RoPE）保留时序信息。</font>
+ **<font style="color:rgb(51, 51, 51);">自注意力机制</font>**<font style="color:rgb(51, 51, 51);">：分析行为间的关联（如“浏览手机→查看耳机”可能暗示跨品类兴趣）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态融合</font>**<font style="color:rgb(51, 51, 51);">：将商品ID、文本描述、图像特征等编码为统一向量，丰富上下文信息。</font>
+ **<font style="color:rgb(51, 51, 51);">预训练+微调</font>**<font style="color:rgb(51, 51, 51);">：LLAMA通过大规模语料预训练获得通用语义理解，再在电商行为数据上微调，学习领域特异性模式。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

**<font style="color:rgb(51, 51, 51);">步骤1：数据预处理</font>**

+ **<font style="color:rgb(51, 51, 51);">行为序列构建</font>**<font style="color:rgb(51, 51, 51);">：截取用户最近N个行为（如N=50），保留时序。例如：  
</font>`<font style="color:rgb(51, 51, 51);">[商品A_点击, 商品B_详情页停留, 商品C_加购]</font>`
+ **<font style="color:rgb(51, 51, 51);">特征编码</font>**<font style="color:rgb(51, 51, 51);">：将商品ID、类目、价格等离散/连续特征嵌入为向量（如256维）。</font>

**<font style="color:rgb(51, 51, 51);">步骤2：模型输入构造</font>**

+ **<font style="color:rgb(51, 51, 51);">Token化</font>**<font style="color:rgb(51, 51, 51);">：每个行为转换为向量，形式为：</font>`<font style="color:rgb(51, 51, 51);">[行为类型嵌入 + 商品嵌入 + 时间间隔嵌入]</font>`
+ **<font style="color:rgb(51, 51, 51);">位置编码</font>**<font style="color:rgb(51, 51, 51);">：LLAMA使用RoPE（Rotary Position Embedding），增强位置敏感性。</font>
+ **<font style="color:rgb(51, 51, 51);">输入格式</font>**<font style="color:rgb(51, 51, 51);">：</font>`<font style="color:rgb(51, 51, 51);">[CLS] + 行为序列 + [SEP] + 候选商品嵌入</font>`<font style="color:rgb(51, 51, 51);">（用于预测任务）</font>

**<font style="color:rgb(51, 51, 51);">步骤3：模型处理</font>**

+ **<font style="color:rgb(51, 51, 51);">Transformer层</font>**<font style="color:rgb(51, 51, 51);">：通过多头自注意力计算行为间权重，例如发现“加购”行为对后续“购买”的强关联。</font>
+ **<font style="color:rgb(51, 51, 51);">序列池化</font>**<font style="color:rgb(51, 51, 51);">：取</font>`<font style="color:rgb(51, 51, 51);">[CLS]</font>`<font style="color:rgb(51, 51, 51);">向量或最后一层隐状态作为用户兴趣表征。</font>

**<font style="color:rgb(51, 51, 51);">步骤4：输出预测</font>**

+ **<font style="color:rgb(51, 51, 51);">候选商品打分</font>**<font style="color:rgb(51, 51, 51);">：计算用户表征与所有候选商品向量的相似度（如余弦相似度）。</font>
+ **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：交叉熵损失（预测下一交互商品）或对比学习损失（增强正负样本区分）。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">长程依赖建模</font>**<font style="color:rgb(51, 51, 51);">：自注意力机制可捕捉相隔较远的行为关联（如周前浏览影响当前购买）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态融合能力</font>**<font style="color:rgb(51, 51, 51);">：同时处理文本、图像、结构化特征。</font>
+ **<font style="color:rgb(51, 51, 51);">零样本推荐</font>**<font style="color:rgb(51, 51, 51);">：预训练模型对冷启动商品有一定泛化能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(51, 51, 51);">计算开销大</font>**<font style="color:rgb(51, 51, 51);">：实时推理时对长序列的O(N²)复杂度影响性能。</font>
+ **<font style="color:rgb(51, 51, 51);">数据稀疏性</font>**<font style="color:rgb(51, 51, 51);">：低频用户行为序列短，模型易过拟合。</font>
+ **<font style="color:rgb(51, 51, 51);">实时更新难</font>**<font style="color:rgb(51, 51, 51);">：用户最新行为需快速纳入模型，传统微调方式延迟高。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">个性化推荐</font>**<font style="color:rgb(51, 51, 51);">：根据历史行为实时生成“猜你喜欢”列表。</font>
+ **<font style="color:rgb(51, 51, 51);">会话式推荐</font>**<font style="color:rgb(51, 51, 51);">：结合用户实时对话调整推荐策略（如“我要找适合沙漠徒步的鞋子”）。</font>
+ **<font style="color:rgb(51, 51, 51);">流失预警</font>**<font style="color:rgb(51, 51, 51);">：通过行为序列突变（如活跃用户突然减少点击）预测流失风险。</font>
+ **<font style="color:rgb(51, 51, 51);">跨域推荐</font>**<font style="color:rgb(51, 51, 51);">：利用LLM的迁移学习能力，从视频观看行为推荐电商商品。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化推理</font>**<font style="color:rgb(51, 51, 51);">：使用知识蒸馏（如用TinyLLAMA压缩模型）或模型剪枝。</font>
+ **<font style="color:rgb(51, 51, 51);">增量学习</font>**<font style="color:rgb(51, 51, 51);">：引入记忆网络，动态更新用户兴趣表征。</font>
+ **<font style="color:rgb(51, 51, 51);">图神经网络结合</font>**<font style="color:rgb(51, 51, 51);">：将行为序列构建为商品关系图，捕捉高阶连接（如GNN+Transformer混合模型）。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务学习</font>**<font style="color:rgb(51, 51, 51);">：同时优化CTR、CVR、停留时长等多目标。</font>
+ **<font style="color:rgb(51, 51, 51);">负采样策略</font>**<font style="color:rgb(51, 51, 51);">：应对海量商品，训练时随机采样负样本提升效率。</font>
+ **<font style="color:rgb(51, 51, 51);">RoPE位置编码</font>**<font style="color:rgb(51, 51, 51);">：在自注意力计算前注入位置信息，增强序列感知。</font>
+ **<font style="color:rgb(51, 51, 51);">动态填充</font>**<font style="color:rgb(51, 51, 51);">：根据用户行为长度动态调整padding，减少计算浪费。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import LlamaModel, LlamaConfig

class LlamaRecommender(nn.Module):
    def __init__(self, item_dim, num_items):
        super().__init__()
        # 初始化LLAMA配置（简化版）
        config = LlamaConfig(hidden_size=256, num_attention_heads=4)
        self.llama = LlamaModel(config)
        # 商品嵌入层
        self.item_embed = nn.Embedding(num_items, item_dim)
        # 行为类型嵌入（点击、购买等）
        self.behavior_embed = nn.Embedding(3, item_dim)  # 假设3种行为
        # 预测头
        self.fc = nn.Linear(config.hidden_size, num_items)

    def forward(self, item_ids, behavior_types):
        # 获取商品和行为嵌入
        item_embs = self.item_embed(item_ids)  # [B, L, D]
        behavior_embs = self.behavior_embed(behavior_types)  # [B, L, D]
        # 合并特征
        inputs_embeds = item_embs + behavior_embs
        # LLAMA处理序列
        outputs = self.llama(inputs_embeds=inputs_embeds)
        sequence_output = outputs.last_hidden_state  # [B, L, H]
        # 预测下一个商品
        logits = self.fc(sequence_output[:, -1, :])  # 取最后一个位置预测
        return logits

# 示例使用
model = LlamaRecommender(item_dim=256, num_items=10000)
item_seq = torch.LongTensor([[1, 5, 3]])  # 商品ID序列
behavior_seq = torch.LongTensor([[0, 1, 0]])  # 行为类型序列
logits = model(item_seq, behavior_seq)
loss = nn.CrossEntropyLoss()(logits, torch.LongTensor([2]))  # 假设下一商品是3

```





# 小红书与抖音推荐系统对比：推荐系统的区别
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">抖音和小红书的推荐系统在算法设计上存在显著差异，主要源于二者</font>**<font style="color:#ED740C;">内容形态、用户行为和数据结构</font>**<font style="color:rgb(51, 51, 51);">的差异。</font>

:::

:::color5
**<font style="color:#601BDE;">1.核心原理对比</font>**

:::

<font style="color:rgb(51, 51, 51);">1. </font>**<font style="color:rgb(51, 51, 51);">抖音推荐系统</font>**

+ **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：最大化用户停留时长和互动率（点赞/评论/分享）。</font>
+ **<font style="color:rgb(51, 51, 51);">核心算法</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">多模态内容理解</font>**<font style="color:rgb(51, 51, 51);">：使用CNN+3D-ResNet提取视频帧特征，CLIP模型对齐视频与文本。</font>
    - **<font style="color:rgb(51, 51, 51);">实时兴趣建模</font>**<font style="color:rgb(51, 51, 51);">：Transformer序列模型（如BST）捕捉用户短期行为序列（滑动、停留、互动）。</font>
    - **<font style="color:rgb(51, 51, 51);">多目标优化</font>**<font style="color:rgb(51, 51, 51);">：MMoE（Multi-gate Mixture-of-Experts）联合优化点赞、完播率、关注等目标。</font>
    - **<font style="color:rgb(51, 51, 51);">强化学习</font>**<font style="color:rgb(51, 51, 51);">：部分场景使用DRL（Deep Reinforcement Learning）建模长期用户价值。</font>

**<font style="color:rgb(51, 51, 51);">2. 小红书推荐系统</font>**

+ **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：平衡内容质量匹配与社区生态建设。</font>
+ **<font style="color:rgb(51, 51, 51);">核心算法</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">图文内容理解</font>**<font style="color:rgb(51, 51, 51);">：BERT+ViT提取文本和图像特征，构建多模态Embedding。</font>
    - **<font style="color:rgb(51, 51, 51);">社交图谱增强</font>**<font style="color:rgb(51, 51, 51);">：GraphSAGE处理用户-内容-标签异构图，挖掘潜在社区关系。</font>
    - **<font style="color:rgb(51, 51, 51);">长尾分发机制</font>**<font style="color:rgb(51, 51, 51);">：ESMM（Entire Space Multi-task Model）建模曝光->点击->收藏的级联转化。</font>
    - **<font style="color:rgb(51, 51, 51);">冷启动策略</font>**<font style="color:rgb(51, 51, 51);">：基于内容相似度的Item-CF和知识图谱补全。</font>

:::color5
**<font style="color:#601BDE;">2.算法流程对比</font>**

:::

1. **抖音典型推荐系统流程**

```python
# 伪代码示例：实时推荐流程
def douyin_recommend(user, current_video):
    # 1. 实时特征提取
    user_embed = RealTimeUserModel(user.last_10_actions)  # Transformer编码最近10个行为
    video_embed = VideoEncoder(current_video)  # 多模态编码
    
    # 2. 召回层（毫秒级）
    candidates = [
        CollaborativeFiltering(user),        # 协同过滤
        HotRanking(time_window="2h"),        # 实时热榜
        FollowedCreators(user)               # 关注创作者
    ]
    
    # 3. 精排层（深度模型）
    scores = MMoE_Model.predict(
        concat(user_embed, video_embed, user.cross_features)
    )
    
    # 4. 多样性控制
    final_list = DiversitySampler(
        candidates, scores, 
        constraints={
            "category_dist": "entropy>0.8", 
            "creator": "<=2/same_creator"
        }
    )
    return final_list

# 多任务MMoE模型
class MMoE_Model(nn.Module):
    def __init__(self, input_dim, num_experts=4, num_tasks=2):
        super().__init__()
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.ReLU()
            ) for _ in range(num_experts)])
        
        self.gates = nn.ModuleList([
            nn.Linear(input_dim, num_experts)
            for _ in range(num_tasks)])
        
        self.towers = nn.ModuleList([
            nn.Linear(64, 1) for _ in range(num_tasks)])
    
    def forward(self, x):
        expert_outputs = [e(x) for e in self.experts]
        outputs = []
        for gate, tower in zip(self.gates, self.towers):
            gate_weights = torch.softmax(gate(x), dim=1)
            combined = sum(w.unsqueeze(2)*e for w,e in zip(gate_weights.T, expert_outputs))
            outputs.append(tower(combined).squeeze())
        return outputs  # [task1_logit, task2_logit]


```

2. **小红书典型推荐系统流程**

```python
# 伪代码示例：图文推荐流程
def xiaohongshu_recommend(user):
    # 1. 离线特征准备
    user_long_term = BERT_UserProfile(user.posts, searches)  # 长期兴趣建模
    social_graph = GraphSAGE(user.followers)                 # 社交特征
    
    # 2. 多路召回
    candidates = [
        ContentBased(TextCNN(user.liked_posts)),  # 内容相似
        KnowledgeGraph_Expand(user.interests),    # 知识图谱扩展
        SocialRecommend(user.friends_activity)    # 社交关系推荐
    ]
    
    # 3. 多任务精排
    ctr, cvr = ESMM_Model.predict(
        concat(user_long_term, social_graph, item.features)
    )
    
    # 4. 生态调控
    final_list = EcoFilter(
        candidates, 
        rules={
            "new_creator_boost": 1.2, 
            "ads_ratio": "<15%"
        }
    )
    return final_list

```

:::color5
**<font style="color:#601BDE;">3.算法对比</font>**

:::

| **维度** | **抖音** | **小红书** |
| --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">实时性</font>** | <font style="color:rgb(51, 51, 51);">毫秒级更新行为序列，在线学习更新频率高</font> | <font style="color:rgb(51, 51, 51);">分钟级更新，侧重离线特征</font> |
| **<font style="color:rgb(51, 51, 51);">特征工程</font>** | <font style="color:rgb(51, 51, 51);">侧重视频完播率、互动密度等连续行为</font> | <font style="color:rgb(51, 51, 51);">强调文本语义、收藏深度等离散行为</font> |
| **<font style="color:rgb(51, 51, 51);">冷启动</font>** | <font style="color:rgb(51, 51, 51);">利用同城/相似用户快速试探</font> | <font style="color:rgb(51, 51, 51);">依赖内容质量分+人工审核机制</font> |
| **<font style="color:rgb(51, 51, 51);">多样性控制</font>** | <font style="color:rgb(51, 51, 51);">滑动窗口多样性注入（动态插播异类内容）</font> | <font style="color:rgb(51, 51, 51);">基于社区规则的静态比例控制</font> |
| **<font style="color:rgb(51, 51, 51);">生态治理</font>** | <font style="color:rgb(51, 51, 51);">后置内容安全审核</font> | <font style="color:rgb(51, 51, 51);">前置创作者等级+内容质量分</font> |


:::color5
**<font style="color:#601BDE;">4.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">抖音推荐系统</font>**

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">实时反馈闭环效率高（用户行为→模型更新<5分钟）</font>
    - <font style="color:rgb(51, 51, 51);">多目标平衡能力强（完播率/互动率等指标联合优化）</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">容易陷入信息茧房（同质内容过度强化）</font>
    - <font style="color:rgb(51, 51, 51);">对冷门创作者不友好（马太效应显著）</font>

**<font style="color:rgb(51, 51, 51);">小红书推荐系统</font>**

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">长尾内容分发效果好（UGC内容生命周期长）</font>
    - <font style="color:rgb(51, 51, 51);">社区氛围维护能力强（通过社交关系增强推荐）</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">实时推荐效率较低（依赖离线特征更新）</font>
    - <font style="color:rgb(51, 51, 51);">多模态对齐难度大（图文匹配精度待提升）</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">抖音适用场景</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">即时娱乐消费（如热点挑战、流行音乐）</font>
    - <font style="color:rgb(51, 51, 51);">广告投放（高流量快速触达）</font>
+ **<font style="color:rgb(51, 51, 51);">小红书适用场景</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">决策型内容推荐（如美妆评测、旅游攻略）</font>
    - <font style="color:rgb(51, 51, 51);">垂直社区建设（如母婴、健身领域）</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">抖音优化方向</font>**
1. <font style="color:rgb(51, 51, 51);">引入因果推断消除曝光偏差（IPS加权）</font>
2. <font style="color:rgb(51, 51, 51);">增加跨域推荐（从抖音火山版迁移兴趣）</font>
3. <font style="color:rgb(51, 51, 51);">使用扩散模型生成多样性候选集</font>
+ **<font style="color:rgb(51, 51, 51);">小红书优化方向</font>**
1. <font style="color:rgb(51, 51, 51);">构建实时特征管道（Flink流处理）</font>
2. <font style="color:rgb(51, 51, 51);">改进多模态对比学习（CLIP优化）</font>
3. <font style="color:rgb(51, 51, 51);">设计创作者成长模型（激励长尾内容）</font>



# 小红书与抖音内容展示对比：多个笔记 VS 单个视频
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">从算法设计角度分析小红书多笔记展示与抖音单视频展示的核心区别</font>

:::

:::color5
**<font style="color:#601BDE;">1.优化目标对比</font>**

:::

**小红书**：推荐算法可能更注重**<font style="color:#74B602;">多样性和用户兴趣的广度</font>**。因为它同时展示多个笔记，可能更依赖封面和标题的吸引力，可能需要考虑**<font style="color:#74B602;">不同内容之间的平衡，比如不同类型、主题或者互动率</font>**。

**抖音**：单列设计让用户专注于一个视频，算法可能需要更精准地预测用户即时兴趣，因此算法需要**<font style="color:#74B602;">更精准的CTR预测</font>**，因为每次滑动都直接影响用户留存。

:::color5
**<font style="color:#601BDE;">2.推荐策略对比</font>**

:::

**小红书**：可能希望用户探索更多内容，增加停留时间。

**抖音**：强调沉浸式体验，**<font style="color:#74B602;">提高单个内容的观看时长</font>**。

:::color5
**<font style="color:#601BDE;">3.推荐模型对比</font>**

:::

**小红书**：使用**<font style="color:#74B602;">多目标优化，同时考虑点击率、多样性、新鲜度等多个指标</font>**。

**抖音**：可能更关注**<font style="color:#74B602;">完播率、互动率等单一目标的优化</font>**。此外，实时反馈的处理也会不同，抖音需要快速根据用户的滑动行为调整推荐。



